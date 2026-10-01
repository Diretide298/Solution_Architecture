# WS29 — Membership   Annual Pass Management board 1

**10 screens · 8 operations · 11 schemas · 4 permissions**

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
  `PRICE_CONFIGURE, PRICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `BO-284` | Membership & Annual Pass Command Center | B–D | 0 | 28 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-285` | Membership Product & Tier Builder | B–D | 23 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-286` | Membership Eligibility & Qualification Rule Builder | B–D | 11 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-287` | Validity, Activation & Expiry Configuration | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-288` | Membership Entitlement & Admission Benefit Builder | B–D | 14 | 0 | 5 | 25 | 0 | 0 | — | notStarted (generated) |
| `BO-289` | Membership Usage, Visit & Consumption Rules | B–D | 0 | 0 | 6 | 9 | 0 | 0 | — | notStarted (generated) |
| `BO-290` | Family, Household & Dependent Membership Configuration | B–D | 21 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-291` | Membership Commercial, Pricing & Channel Association | B–D | 24 | 0 | 5 | 4 | 0 | 0 | — | notStarted (generated) |
| `BO-292` | Renewal, Auto-Renewal & Membership Continuity Configuration | B–D | 11 | 0 | 5 | 1 | 1 | 0 | — | notStarted (generated) |
| `BO-293` | Membership Product Validation, Approval, Publication & Versioning | B–D | 8 | 0 | 5 | 0 | 0 | 3 | — | notStarted (generated) |

## Thin screens in this batch

**BO-287, BO-289 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-284` Membership & Annual Pass Command Center

**Provide administrators with a centralized view of all membership, annual pass, season pass and subscription-style admission products.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Identify) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/membership-annual-pass-command-center-bo-284` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Membership Products** (metric tile, from `listMembershipAnnualPass`)

**Annual Pass Products** (metric tile, from `listMembershipAnnualPass`)

**Draft Products** (metric tile, from `listMembershipAnnualPass`)

**Active Members** (metric tile, from `listMembershipAnnualPass`)

**Family Memberships** (metric tile, from `listMembershipAnnualPass`)

**Memberships expiring soon** (metric tile, from `listMembershipAnnualPass`)

**Renewal-Enabled Products** (metric tile, from `listMembershipAnnualPass`)

**Suspended Products** (metric tile, from `listMembershipAnnualPass`)

**Products with configuration issues** (metric tile, from `listMembershipAnnualPass`)

**Average membership duration** (metric tile, from `listMembershipAnnualPass`)

**Every membership annual pass** (data table, from `listMembershipAnnualPass`)

| Shows | Format | Notes |
|---|---|---|
| Product ID | text | not in the schema: `MembershipAnnualPassCommandCenterView.productId` |
| Membership name | text | not in the schema: `MembershipAnnualPassCommandCenterView.membershipName` |
| Type | text | not in the schema: `MembershipAnnualPassCommandCenterView.type` |
| Tier | text | not in the schema: `MembershipAnnualPassCommandCenterView.tier` |
| Venue attraction | text | not in the schema: `MembershipAnnualPassCommandCenterView.venueAttraction` |
| Validity method | text | not in the schema: `MembershipAnnualPassCommandCenterView.validityMethod` |
| Activation method | text | not in the schema: `MembershipAnnualPassCommandCenterView.activationMethod` |
| Renewal mode | text | not in the schema: `MembershipAnnualPassCommandCenterView.renewalMode` |
| Membership structure | text | not in the schema: `MembershipAnnualPassCommandCenterView.membershipStructure` |
| Current members | text | not in the schema: `MembershipAnnualPassCommandCenterView.currentMembers` |
| Effective from | text | not in the schema: `MembershipAnnualPassCommandCenterView.effectiveFrom` |
| Status | text | not in the schema: `MembershipAnnualPassCommandCenterView.status` |
| Owner | text | not in the schema: `MembershipAnnualPassCommandCenterView.owner` |
| Validation issues | text | not in the schema: `MembershipAnnualPassCommandCenterView.validationIssues` |

**The selected membership annual pass** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Product ID | text | not in the schema: `MembershipAnnualPassCommandCenterView.productId` |
| Membership name | text | not in the schema: `MembershipAnnualPassCommandCenterView.membershipName` |
| Type | text | not in the schema: `MembershipAnnualPassCommandCenterView.type` |
| Tier | text | not in the schema: `MembershipAnnualPassCommandCenterView.tier` |
| Venue attraction | text | not in the schema: `MembershipAnnualPassCommandCenterView.venueAttraction` |
| Validity method | text | not in the schema: `MembershipAnnualPassCommandCenterView.validityMethod` |
| Activation method | text | not in the schema: `MembershipAnnualPassCommandCenterView.activationMethod` |
| Renewal mode | text | not in the schema: `MembershipAnnualPassCommandCenterView.renewalMode` |
| Membership structure | text | not in the schema: `MembershipAnnualPassCommandCenterView.membershipStructure` |
| Current members | text | not in the schema: `MembershipAnnualPassCommandCenterView.currentMembers` |
| Effective from | text | not in the schema: `MembershipAnnualPassCommandCenterView.effectiveFrom` |
| Status | text | not in the schema: `MembershipAnnualPassCommandCenterView.status` |
| Owner | text | not in the schema: `MembershipAnnualPassCommandCenterView.owner` |
| Validation issues | text | not in the schema: `MembershipAnnualPassCommandCenterView.validationIssues` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Monthly Membership (primary button) | navigation or local | — | — | — | — |
| Fixed-Term Membership (secondary button) | navigation or local | — | — | — | — |
| Corporate Membership (secondary button) | navigation or local | — | — | — | — |
| Family Membership (secondary button) | navigation or local | — | — | — | — |
| Individual Membership (secondary button) | navigation or local | — | — | — | — |
| Student Membership (secondary button) | navigation or local | — | — | — | — |
| VIP Membership (secondary button) | navigation or local | — | — | — | — |
| Custom Membership (secondary button) | navigation or local | — | — | — | — |
| Suspend membership product (destructive button) | `approveMembershipProductValidation` (not in any contract) | — | — | — | — |
| Reinstate membership product (secondary button) | `approveMembershipProductValidation` (not in any contract) | — | — | — | — |

**Data it reads**: `listMembershipAnnualPass` (onLoad, Membership & Annual Pass Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-285` Membership Product & Tier Builder: *Works in Membership Product & Tier Builder*; calls `listMembershipAnnualPass`
- → `BO-286` Membership Eligibility & Qualification Rule Builder: *Works in Membership Eligibility & Qualification Rule Builder*; calls `listMembershipAnnualPass`
- → `BO-287` Validity, Activation & Expiry Configuration: *Works in Validity, Activation & Expiry Configuration*; calls `listMembershipAnnualPass`
- → `BO-288` Membership Entitlement & Admission Benefit Builder: *Works in Membership Entitlement & Admission Benefit Builder*; calls `listMembershipAnnualPass`
- → `BO-289` Membership Usage, Visit & Consumption Rules: *Works in Membership Usage, Visit & Consumption Rules*; calls `listMembershipAnnualPass`
- → `BO-290` Family, Household & Dependent Membership Configuration: *Works in Family, Household & Dependent Membership Configuration*; calls `listMembershipAnnualPass`
- → `BO-291` Membership Commercial, Pricing & Channel Association: *Works in Membership Commercial, Pricing & Channel Association*; calls `listMembershipAnnualPass`
- → `BO-292` Renewal, Auto-Renewal & Membership Continuity Configuration: *Works in Renewal, Auto-Renewal & Membership Continuity Configuration*; calls `listMembershipAnnualPass`
- → `BO-293` Membership Product Validation, Approval, Publication & Versioning: *Works in Membership Product Validation, Approval, Publication & Versioning*; calls `listMembershipAnnualPass`

**What opens over it**

- confirmDialog *Suspend membership product*: **Names what suspending stops and what it leaves alone**: the membership product and version, every channel it stops selling on, and that members already holding it keep their entitlements until their own expiry. **Collects what `approveMembershipProductValidation` sends before it is called.** …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership annual pass list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership annual pass untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership annual pass yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the membership annual pass are still there. Names the active filter and offers to clear it. |
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-284` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-284`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 1: Opens Membership & Annual Pass Command Center → Provide administrators with a centralized view of all membership, annual pass, season pass and subscription-style admission products.
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F138 branch at step 1 (expected): when Nothing has been set up on Membership & Annual Pass Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F138 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-284?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Monthly Membership, Fixed-Term Membership, Corporate Membership, Family Membership, Individual Membership, Student Membership, VIP Membership, Custom Membership, Suspend membership product, Reinstate membership product.
- [ ] Every transition is wired: `BO-100`, `BO-285`, `BO-286`, `BO-287`, `BO-288`, `BO-289`, `BO-290`, `BO-291`, `BO-292`, `BO-293`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-285` Membership Product & Tier Builder

**Configure the fundamental definition and hierarchy of a membership/pass.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture; Define; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/membership-product-tier-builder-bo-285` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Membership Name | select field | — | — | — | — | — | — |
| Membership Code | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Membership Type | select field | — | — | — | — | — | — |
| Brand | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Attraction | select field | — | — | — | — | — | — |
| Market | select field | — | — | — | — | — | — |
| Currency Context | select field | — | — | — | — | — | — |
| Effective From | select field | — | — | — | — | — | — |
| Effective To | select field | — | — | — | — | — | — |
| Tier Level | select field | — | — | — | — | — | — |
| Display Order | select field | — | — | — | — | — | — |
| Upgrade Path | select field | — | — | — | — | — | — |
| Downgrade Path | select field | — | — | — | — | — | — |
| Parent Membership | select field | — | — | — | — | — | — |
| Replacement Membership | select field | — | — | — | — | — | — |
| Individual / Family / Corporate | text field | — | — | — | — | — | — |
| Named / Transferable | select field | — | — | — | — | — | — |
| Physical / Digital | select field | — | — | — | — | — | — |
| Renewable / Non-Renewable | select field | — | — | — | — | — | — |
| Auto-Renew Eligible | select field | — | — | — | — | — | — |
| Admission-Based / Benefit-Based / Hybrid | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-284` Membership & Annual Pass Command Center: *Returns to the board's landing screen*; calls `setMembershipProductTier`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership product tier configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership product tier untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership product tier configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setMembershipProgramme` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Membership/pass tickets: seasonal, monthly or annual classes with renewal/auto-renewal using a tokenised card-on-file billed ahead of expiry, subject to the guest's consent to terms and conditions. *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-448)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-285` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-285`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 2: Works in Membership Product & Tier Builder → Configure the fundamental definition and hierarchy of a membership/pass.

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-285?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-284`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-286` Membership Eligibility & Qualification Rule Builder

**Determine who is allowed to purchase, activate, hold or renew a particular membership.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Configure whether qualification requires) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/membership-eligibility-qualification-rule-builder-bo-286` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Multiple Memberships Allowed | select field | — | — | — | — | — | — |
| One Membership per Customer | text field | — | — | — | — | — | — |
| Mutually Exclusive Memberships | select field | — | — | — | — | — | — |
| Prerequisite Membership | select field | — | — | — | — | — | — |
| Existing Tier Requirement | select field | — | — | — | — | — | — |
| No Verification | select field | — | — | — | — | — | — |
| Customer Declaration | select field | — | — | — | — | — | — |
| Document Verification | select field | — | — | — | — | — | — |
| Identity Verification | select field | — | — | — | — | — | — |
| Staff Verification | select field | — | — | — | — | — | — |
| External Verification | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-284` Membership & Annual Pass Command Center: *Returns to the board's landing screen*; calls `setMembershipEligibilityQualification`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership eligibility qualification configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership eligibility qualification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership eligibility qualification configured yet. Carries the create action and says what the platform does in the meantime. |
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-286` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-286`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 4: Works in Membership Eligibility & Qualification Rule Builder → Determine who is allowed to purchase, activate, hold or renew a particular membership.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-286?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-284`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-287` Validity, Activation & Expiry Configuration

**Define exactly when a membership becomes valid, how long it remains valid and how it expires.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/validity-activation-expiry-configuration-bo-287` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-284` Membership & Annual Pass Command Center: *Returns to the board's landing screen*; calls `setValidityActivationExpiry`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The validity activation expiry list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the validity activation expiry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No validity activation expiry yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the validity activation expiry are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Validity types: fixed date range, rolling (e.g. 90 days from issue) and first-use activation (starts at first scan). Confirmed: first-use tickets need a fallback expiry (e.g. issue date + 30 days) if never scanned. *(agreed · MoM 25 Aug 2026, 4.5 Validity Management & Expiry Rules · DI-451)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-287` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-287`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 6: Works in Validity, Activation & Expiry Configuration → Define exactly when a membership becomes valid, how long it remains valid and how it expires.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-287?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-284`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-288` Membership Entitlement & Admission Benefit Builder

**Define exactly what the member receives. This is the heart of the membership product.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `templateId` (navigation) |
| Route | `/sell/membership-entitlement-admission-benefit-builder-bo-288` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue | select field | — | — | — | — | — | — |
| Attraction | select field | — | — | — | — | — | — |
| Event Type | select field | — | — | — | — | — | — |
| Admission Type | select field | — | — | — | — | — | — |
| Number of Visits | select field | — | — | — | — | — | — |
| Period | select field | — | — | — | — | — | — |
| Days | select field | — | — | — | — | — | — |
| Times | select field | — | — | — | — | — | — |
| Timeslots | select field | — | — | — | — | — | — |
| Per Day | select field | — | — | — | — | — | — |
| Per Week | select field | — | — | — | — | — | — |
| Per Month | select field | — | — | — | — | — | — |
| Per Membership Year | select field | — | — | — | — | — | — |
| Lifetime of Membership | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Attraction Access (primary button) | navigation or local | — | — | — | — |
| Event Access (secondary button) | navigation or local | — | — | — | — |
| Zone Access (secondary button) | navigation or local | — | — | — | — |
| Priority Entry (secondary button) | navigation or local | — | — | — | — |
| Guest Tickets (secondary button) | navigation or local | — | — | — | — |
| F&B Benefit (secondary button) | navigation or local | — | — | — | — |
| Retail Benefit (secondary button) | navigation or local | — | — | — | — |
| Rental Benefit (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listEntitlementTemplates` (onLoad, The membership plan templates whose benefits are set)

**Where the user goes next**

- → `BO-284` Membership & Annual Pass Command Center: *Returns to the board's landing screen*; calls `setMembershipEntitlementAdmission`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership entitlement admission configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership entitlement admission untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership entitlement admission configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setMembershipBenefit` → `PRODUCT_CONFIGURE` (configure) · staff
- `setPlanBenefits` → `PRODUCT_CONFIGURE` (configure) · staff
- `listEntitlementTemplates` → `PRODUCT_VIEW` (read) · staff
- `createEntitlementTemplate` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

25 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.32 | Membership & Annual Pass Sales | Ticketing Sales | CONTRACTED | `listEntitlementTemplates` |
| 2.14.11 | Support validity periods, renewals and expiry rules. | Ticketing Sales | CONTRACTED | `listEntitlementTemplates` |
| 5.3.15 | Maintain membership type, tier, status, activation date, expiration date, benefits, renewal history, suspension history, and usage history. | F&B & Guest Management | CONTRACTED | `listEntitlementTemplates` |
| 6.1.37 | The system should be able to provide aging report for ticketing & reward age. | Retail POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.21 | For each PLU, it is possible to manage a validity date range | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.23 | For each PLU, it is possible to manage Events having a scheduled usage, based on slot date and time | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.24 | For each PLU, it is possible to have Capacity management rules (valid until there is no available place) | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.29 | For each PLU, it is possible to Allow re-entry or not | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 1.1.5 | The system should be able to sell multiple day tickets for attractions. The number of days should be configurable. This type of ticket should require a start date to be specified before first entry. | Ticketing Catalogue | CONTRACTED | `createEntitlementTemplate` |
| 1.1.9 | The system should allow the validity period for a ticket to be configurable. For open-dated tickets, the validity period is intended to define the mandatory date by which the ticket must be used. For … | Ticketing Catalogue | CONTRACTED | `createEntitlementTemplate` |
| 1.1.11 | The system should allow the number of entitled access per ticket to be configurable (N entries to Y access areas). Some tickets will allow only access once per attraction while some tickets will … | Ticketing Catalogue | CONTRACTED | `createEntitlementTemplate` |
| 1.1.16 | System shall allow administrators to create reusable ticket templates containing pricing, validity, capacity, access rights, add-ons, restrictions and approval workflows. | Ticketing Catalogue | CONTRACTED | `createEntitlementTemplate` |
| … 13 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-288` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-288`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 8: Works in Membership Entitlement & Admission Benefit Builder → Define exactly what the member receives. This is the heart of the membership product.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-288?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Attraction Access, Event Access, Zone Access, Priority Entry, Guest Tickets, F&B Benefit, Retail Benefit, Rental Benefit.
- [ ] Every transition is wired: `BO-284`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-289` Membership Usage, Visit & Consumption Rules

**Control how membership entitlements may actually be consumed. Screen 13.1.5 defines what the member receives. Screen 13.1.6 defines how it may be used.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Maintain counters such as) and no metric row |
| Offline | online only |
| Opens with | `templateId` (navigation) |
| Route | `/sell/membership-usage-visit-consumption-rules-bo-289` |

#### Inputs: what the user enters or picks

**Form: Save membership usage policy** (modal, opened by *Save membership usage policy*; *Save membership usage policy* calls `setMembershipUsagePolicy`, *Cancel* sends nothing)

**Collects what `setMembershipUsagePolicy` sends before it is called.** Required: `membershipCode`, `reEntryPolicy`, `reservationRequirement`. Optional: `tier`, `maximumVisitsPerDay`, `maximumAdmissionsPerPeriod`, `admissionPeriod`, `reEntryCooldownMinutes`, `walkInAllowed`, `maximumAdvanceBookingDays`, `maximumActiveFutureReservations`, `concurrentReservations`, `noShowTreatment`, `noShowThreshold`, `noShowWindowDays` and 4 more. Dismissing sends nothing; the screen behind is unchanged.

`setMembershipUsagePolicy` is not in any contract: draw the form greyed and list it in FINDINGS.md.

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every membership usage visit** (data table, from `listMembershipUsageVisit`)

**The selected membership usage visit** (detail panel): The pack groups this record's detail under its own headings: “Unlimited annual visits”, “Access Integration”.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save membership usage policy (primary button) | `setMembershipUsagePolicy` (not in any contract) | — | — | — | — |

**Data it reads**: `listMembershipUsageVisit` (onLoad, Membership Usage, Visit & Consumption Rules); `listEntitlementTemplates` (onLoad, The membership plan templates whose usage rules are set)

**Where the user goes next**

- → `BO-284` Membership & Annual Pass Command Center: *Returns to the board's landing screen*; calls `listMembershipUsageVisit`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership usage visit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership usage visit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership usage visit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the membership usage visit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setPlanBenefits` → `PRODUCT_CONFIGURE` (configure) · staff
- `listEntitlementTemplates` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.32 | Membership & Annual Pass Sales | Ticketing Sales | CONTRACTED | `listEntitlementTemplates` |
| 2.14.11 | Support validity periods, renewals and expiry rules. | Ticketing Sales | CONTRACTED | `listEntitlementTemplates` |
| 5.3.15 | Maintain membership type, tier, status, activation date, expiration date, benefits, renewal history, suspension history, and usage history. | F&B & Guest Management | CONTRACTED | `listEntitlementTemplates` |
| 6.1.37 | The system should be able to provide aging report for ticketing & reward age. | Retail POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.21 | For each PLU, it is possible to manage a validity date range | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.23 | For each PLU, it is possible to manage Events having a scheduled usage, based on slot date and time | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.24 | For each PLU, it is possible to have Capacity management rules (valid until there is no available place) | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.29 | For each PLU, it is possible to Allow re-entry or not | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 2.14.7 | Annual-pass reservation quota engine linked to biometric identity, with self-service reschedule/cancel | Ticketing Sales | CONTRACTED | `setMembershipUsagePolicy` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-289` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-289`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 10: Works in Membership Usage, Visit & Consumption Rules → Control how membership entitlements may actually be consumed. Screen 13.1.5 defines what the member receives. Screen 13.1.6 defines how it may be used.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-289?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save membership usage policy.
- [ ] Every transition is wired: `BO-284`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-290` Family, Household & Dependent Membership Configuration

**Support memberships covering more than one person while preserving individual identities and entitlements.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Possible configured action) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/family-household-dependent-membership-configuration-bo-290` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Primary Member | select field | — | — | — | — | — | — |
| Secondary Adult | select field | — | — | — | — | — | — |
| Dependent | select field | — | — | — | — | — | — |
| Child | select field | — | — | — | — | — | — |
| Guardian | select field | — | — | — | — | — | — |
| Authorized Manager | select field | — | — | — | — | — | — |
| Minimum Age | select field | — | — | — | — | — | — |
| Maximum Age | select field | — | — | — | — | — | — |
| Relationship Requirement | select field | — | — | — | — | — | — |
| Verification Requirement | select field | — | — | — | — | — | — |
| Same Household Requirement where applicable | text field | — | — | — | — | — | — |
| Allowed | select field | — | — | — | — | — | — |
| Effective Date | select field | — | — | — | — | — | — |
| Frequency | select field | — | — | — | — | — | — |
| Fee | select field | — | — | — | — | — | — |
| Approval | select field | — | — | — | — | — | — |
| Eligibility Revalidation | select field | — | — | — | — | — | — |
| Grace Period | select field | — | — | — | — | — | — |
| Upgrade Required | select field | — | — | — | — | — | — |
| Renewal Correction | select field | — | — | — | — | — | — |
| Manual Review | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-284` Membership & Annual Pass Command Center: *Returns to the board's landing screen*; calls `setFamilyHouseholdDependent`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The family household dependent configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the family household dependent untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No family household dependent configured yet. Carries the create action and says what the platform does in the meantime. |
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-290` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-290`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 12: Works in Family, Household & Dependent Membership Configuration → Support memberships covering more than one person while preserving individual identities and entitlements.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-290?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-284`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-291` Membership Commercial, Pricing & Channel Association

**Connect the membership contract to TICVAI's central commercial engines without duplicating pricing configuration.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRICE_VIEW`, `PRODUCT_CONFIGURE` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure sale through; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `priceListId` (navigation) |
| Route | `/sell/membership-commercial-pricing-channel-association-bo-291` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| B2C | select field | — | — | — | — | — | — |
| Mobile App | select field | — | — | — | — | — | — |
| POS | select field | — | — | — | — | — | — |
| Call Center | select field | — | — | — | — | — | — |
| Box Office | select field | — | — | — | — | — | — |
| Kiosk | select field | — | — | — | — | — | — |
| B2B | select field | — | — | — | — | — | — |
| Corporate | select field | — | — | — | — | — | — |
| Reseller | select field | — | — | — | — | — | — |
| API | select field | — | — | — | — | — | — |
| Always Available | select field | — | — | — | — | — | — |
| Fixed Sales Window | select field | — | — | — | — | — | — |
| Seasonal Sale | select field | — | — | — | — | — | — |
| Invitation Only | select field | — | — | — | — | — | — |
| Capacity Limited | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listPriceLists` ?channel |

**Form: Save membership commercial config** (modal, opened by *Save membership commercial config*; *Save membership commercial config* calls `setMembershipCommercialConfig`, *Cancel* sends nothing)

**Collects what `setMembershipCommercialConfig` sends before it is called.** Required: `membershipCode`, `basePricingProfile`, `taxProfile`, `salesPeriod`. Optional: `feeProfile`, `upgradePricePolicy`, `promotionalPricingEligibility`, `paymentTerms`. Dismissing sends nothing; the screen behind is unchanged.

`setMembershipCommercialConfig` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Sent by *What publishing changes*** (`publishChannelAvailability`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Channels `channels` | repeatable rows | optional | — | — | — | Channels the product is published on, with channel-specific sites, POS groups, venues and effective dates | `publishChannelAvailability` body |
| Channel `channels[].channel` | select | optional | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `publishChannelAvailability` body |
| Enabled `channels[].enabled` | toggle | optional | — | — | — | — | `publishChannelAvailability` body |
| Sites `channels[].siteIds` | list of values (chips) | optional | — | — | — | Specific sites/webstores; empty = all | `publishChannelAvailability` body |
| POS groups `channels[].posGroupIds` | list of values (chips) | optional | — | — | — | Specific POS groups; empty = all | `publishChannelAvailability` body |
| Venues `channels[].venueIds` | list of values (chips) | optional | — | — | — | Availability by venue; empty = all the product's venues | `publishChannelAvailability` body |
| Effective from `channels[].effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishChannelAvailability` body |
| Effective to `channels[].effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishChannelAvailability` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | Product id | `publishChannelAvailability` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What publishing changes (publish gate) | `publishChannelAvailability` PUT `/channel-availability` | ChannelPublicationAvailabilityInput | ChannelPublicationAvailabilityView | — | — |
| Save membership commercial config (primary button) | `setMembershipCommercialConfig` (not in any contract) | — | — | — | — |

**Data it reads**: `listMembershipCommercialPricing` (onLoad, Membership Commercial, Pricing & Channel Association); `listPriceLists` (onLoad, The price lists a membership is priced on)

**Where the user goes next**

- → `BO-284` Membership & Annual Pass Command Center: *Returns to the board's landing screen*; calls `listMembershipCommercialPricing`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership commercial pricing configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership commercial pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership commercial pricing configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Currency or scale mismatch against the region |

#### Permissions

- `setPrices` → `PRICE_CONFIGURE` (configure) · staff
- `publishChannelAvailability` → `PRODUCT_CONFIGURE` (configure) · staff
- `listPriceLists` → `PRICE_VIEW` (read) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.10.4 | The system should allow sales of free tickets. These tickets can be configured as a standard ticket with a price of zero or as a full price ticket with a 100% discount. | Ticketing Sales | CONTRACTED | `setPrices` |
| 7.4.17 | For each PLU, it is possible to manage its Unit price and the related currency | F&B POS | CONTRACTED | `setPrices` |
| 7.4.19 | For each PLU, it is possible to manage its VAT rate | F&B POS | CONTRACTED | `setPrices` |
| 2.14.19 | System shall support recurring membership billing cycles including monthly, quarterly, annual, and configurable subscription periods. | Ticketing Sales | CONTRACTED | `setMembershipCommercialConfig` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-291` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-291`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 14: Works in Membership Commercial, Pricing & Channel Association → Connect the membership contract to TICVAI's central commercial engines without duplicating pricing configuration.

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-291?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: What publishing changes, Save membership commercial config.
- [ ] Every transition is wired: `BO-284`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRICE_VIEW`, `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-292` Renewal, Auto-Renewal & Membership Continuity Configuration

**Define how a membership moves from one validity period into the next.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; At renewal, configure whether) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/renewal-auto-renewal-membership-continuity-configuration-bo-292` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| 60 days before expiry | text field | — | — | — | — | — | — |
| Eligible Products | select field | — | — | — | — | — | — |
| Consent Requirement | select field | — | — | — | — | — | — |
| Payment Method Requirement | select field | — | — | — | — | — | — |
| Pre-Renewal Notification | select field | — | — | — | — | — | — |
| Retry Policy | select field | — | — | — | — | — | — |
| Failure Handling | select field | — | — | — | — | — | — |
| Same Tier Only | select field | — | — | — | — | — | — |
| Upgrade Allowed | select field | — | — | — | — | — | — |
| Downgrade Allowed | select field | — | — | — | — | — | — |
| Suggested Tier | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Manual Renewal (primary button) | navigation or local | — | — | — | — |
| Customer Self-Service Renewal (secondary button) | navigation or local | — | — | — | — |
| Agent-Assisted Renewal (secondary button) | navigation or local | — | — | — | — |
| Invitation-Only Renewal (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-284` Membership & Annual Pass Command Center: *Returns to the board's landing screen*; calls `setRenewalAutoMembership`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The renewal auto-renewal membership configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the renewal auto-renewal membership untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No renewal auto-renewal membership configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.14.20 | System shall support automatic membership renewal using stored payment methods, configurable renewal notices, renewal reminders, and renewal grace periods. | Ticketing Sales | CONTRACTED | `setRenewalAutoMembership` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Membership/pass tickets: seasonal, monthly or annual classes with renewal/auto-renewal using a tokenised card-on-file billed ahead of expiry, subject to the guest's consent to terms and conditions. *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-448)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-292` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-292`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 16: Works in Renewal, Auto-Renewal & Membership Continuity Configuration → Define how a membership moves from one validity period into the next.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-292?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Manual Renewal, Customer Self-Service Renewal, Agent-Assisted Renewal, Invitation-Only Renewal.
- [ ] Every transition is wired: `BO-284`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-293` Membership Product Validation, Approval, Publication & Versioning

**Provide the final governance layer before a membership/pass configuration becomes commercially available.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `membership` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Synchronize relevant configuration with; AI Configuration Review) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/membership-product-validation-approval-publication-versi-bo-293` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| B2C | select field | — | — | — | — | — | — |
| POS | select field | — | — | — | — | — | — |
| Mobile App | select field | — | — | — | — | — | — |
| Call Center | select field | — | — | — | — | — | — |
| B2B | select field | — | — | — | — | — | — |
| Access Control | select field | — | — | — | — | — | — |
| Ticketing | select field | — | — | — | — | — | — |
| Other dependent services | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve (primary button) | navigation or local | — | — | — | — |

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership product validation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership product validation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership product validation configured yet. Carries the create action and says what the platform does in the meantime. |
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

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-293` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-293`
- Workshop pack: Membership___Annual_Pass_Management_Reference.pdf board 1
- Flow F138 *Membership Annual Pass Management board 1: Membership & Annual Pass Command …*, step 18: Works in Membership Product Validation, Approval, Publication & Versioning → Provide the final governance layer before a membership/pass configuration becomes commercially available.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-293?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve.
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

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createEntitlementTemplate": {"method":"POST","path":"/entitlement-templates","contract":"catalogue","summary":"Create an entitlement template","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"EntitlementTemplate","responds":"EntitlementTemplate"},
"listEntitlementTemplates": {"method":"GET","path":"/entitlement-templates","contract":"catalogue","summary":"List entitlement templates","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"EntitlementTemplate"},
"listPriceLists": {"method":"GET","path":"/price-lists","contract":"catalogue","summary":"List price lists","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"publishChannelAvailability": {"method":"PUT","path":"/channel-availability","contract":"catalogue","summary":"Channel Publication & Availability","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ChannelPublicationAvailabilityInput","responds":"ChannelPublicationAvailabilityView"},
"setMembershipBenefit": {"method":"PUT","path":"/membership-benefits","contract":"catalogue","summary":"Define a benefit","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CatalogueMembershipBenefit","responds":"CatalogueMembershipBenefit"},
"setMembershipProgramme": {"method":"PUT","path":"/membership-programmes","contract":"catalogue","summary":"Define a membership programme","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CatalogueMembershipProgramme","responds":"CatalogueMembershipProgramme"},
"setPlanBenefits": {"method":"PUT","path":"/entitlement-templates/{templateId}/benefits","contract":"catalogue","summary":"Replace the benefits a plan grants","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"templateId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":"CataloguePlanBenefit","responds":"CataloguePlanBenefit"},
"setPrices": {"method":"PUT","path":"/price-lists/{priceListId}/prices","contract":"catalogue","summary":"Set prices in bulk","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CatalogueConfigStatus": {"type":"string","enum":["draft","active","inactive","retired"],"description":"**The status of a catalogue configuration record** (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles, package pricing and templates. `draft` is being prepared and is never used by a calculation; `active` is in use from its effective date; `inactive` is switched off and may be switched back; `retired` is kept for history only. A record already used by a live price becomes `active` through a published change request, not by an edit."},
"CatalogueMembershipBenefit": {"type":"object","x-ticvai-persistence":"catalogue.membership_benefit","description":"**Taken from the backend workbook, 20 September.** Defines a benefit that can be included in one or more membership plans.","required":["code","name","type","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":100},"name":{"type":"string","maxLength":150},"type":{"type":"string","maxLength":30},"description":{"type":"string","maxLength":500,"nullable":true},"value":{"type":"number","nullable":true},"unit":{"type":"string","maxLength":30,"nullable":true},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"}}},
"CatalogueMembershipProgramme": {"type":"object","x-ticvai-persistence":"catalogue.membership_programme","description":"**Taken from the backend workbook, 20 September.** Defines the overall membership programme available to customers.","required":["programId","programCode","programName","isActive","createdAt"],"properties":{"programId":{"type":"string","format":"uuid"},"programCode":{"type":"string","maxLength":100},"programName":{"type":"string","maxLength":150},"description":{"type":"string","maxLength":500,"nullable":true},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time","nullable":true}}},
"CataloguePlanBenefit": {"type":"object","x-ticvai-persistence":"catalogue.plan_benefit","description":"**Taken from the backend workbook, 20 September.** Maps membership benefits to plans and defines usage limits for each benefit.","required":["entitlementTemplateId","membershipBenefitId","priority","isActive","createdAt"],"properties":{"entitlementTemplateId":{"type":"string","format":"uuid"},"membershipBenefitId":{"type":"string","format":"uuid"},"usageLimit":{"type":"number","nullable":true},"usagePeriod":{"type":"string","maxLength":30,"nullable":true},"priority":{"type":"integer"},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"ChannelPublicationAvailabilityInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Channel Publication & Availability submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"channels":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/Channel"},"enabled":{"type":"boolean"},"siteIds":{"type":"array","items":{"type":"string"},"description":"Specific sites/webstores; empty = all"},"posGroupIds":{"type":"array","items":{"type":"string"},"description":"Specific POS groups; empty = all"},"venueIds":{"type":"array","items":{"type":"string"},"description":"Availability by venue; empty = all the product's venues"},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true}}},"description":"Channels the product is published on, with channel-specific sites, POS groups, venues and effective dates"},"productId":{"type":"string","description":"Product id","format":"uuid"}}},
"ChannelPublicationAvailabilityView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel Publication & Availability displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"channels":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/Channel"},"enabled":{"type":"boolean"},"siteIds":{"type":"array","items":{"type":"string"},"description":"Specific sites/webstores; empty = all"},"posGroupIds":{"type":"array","items":{"type":"string"},"description":"Specific POS groups; empty = all"},"venueIds":{"type":"array","items":{"type":"string"},"description":"Availability by venue; empty = all the product's venues"},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true}}},"description":"Channels the product is published on, with channel-specific sites, POS groups, venues and effective dates"},"publicationPreview":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/Channel"},"venueId":{"type":"string"},"exposed":{"type":"boolean"},"reason":{"type":"string","nullable":true}}},"description":"Preview of where the product will actually be on sale"},"validationIssues":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["channelNotConfigured","noPriceForChannel","noCapacityAllocation","productNotApproved","venueNotAssigned"]},"message":{"type":"string"}}},"description":"Missing channel dependencies (decided 29 September, readiness close-out)"},"productId":{"type":"string","description":"Product id","format":"uuid"},"issuedEntitlementsUnaffected":{"type":"integer","description":"Valid issued tickets/entitlements that remain valid whatever the channel change (pack p.10 Important Rule)"}}},
"EntitlementTemplate": {"x-ticvai-persistence":"catalogue.entitlement_template","type":"object","required":["id","code","name","validityKind"],"properties":{"description":{"type":"string","description":"**Validity, re-entry and transfer rules in prose.** \"Can I leave and come back\" is answered from here, and a name cannot answer it.\n"},"id":{"type":"string","format":"uuid","readOnly":true,"description":"Assigned by the server on create; `createEntitlementTemplate` does not take it."},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"validityKind":{"type":"string","enum":["singleUse","dated","dateRange","rolling","unlimited","countLimited"]},"validFromOffsetDays":{"type":"integer","nullable":true},"validForDays":{"type":"integer","nullable":true},"daysOfWeek":{"type":"array","nullable":true,"description":"1.1.7 and 1.1.82. **A camp ticket admits on Tuesdays and Thursdays for six weeks**, and `validityKind` had six values with no day pattern among them.\nThe shape is settled elsewhere in the package — `fnb.MenuAvailability` and `promotions.PromotionConditions` both carry it. **Null means every day**, which is what every existing entitlement means today.\n","items":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]}},"expiryAnchor":{"type":"string","nullable":true,"enum":["offsetDays","endOfMonth","endOfQuarter","endOfYear","fixedDate","seasonEnd"],"description":"1.1.90 to 1.1.92. **A pass bought on the 20th and expiring on the 31st cannot be expressed by an offset in days.** `offsetDays` is the existing behaviour and stays the default.\n`seasonEnd` anchors to the venue's own season rather than the calendar — a water park closing in October is not a quarter boundary.\n"},"expiryDate":{"type":"string","format":"date","nullable":true,"description":"Where `expiryAnchor` is `fixedDate`. Every pass expires the same day regardless of purchase."},"expiryNoticeDays":{"type":"integer","minimum":1,"maximum":180,"nullable":true,"description":"**How many days before `validTo` access raises `entitlement.expiringSoon`** for an entitlement of this template still `issued` or `partiallyConsumed` (29 September, build pass, group G2; 5.5.30). What a pre-expiry message or campaign is triggered by. Null, the default, means no notice: a day ticket needs none, an annual pass might want 30. An entitlement bought inside its own notice period raises nothing."},"carriesStoredValue":{"type":"boolean","default":false,"description":"BL-033. **A ticket that is also a wallet** — a resort pass with 200 dirhams of spend on it, deducted at a gate or a till.\n**The value is a `retail.Wallet` bound to the entitlement, not a balance on the ticket.** One balance mechanism (CF-126), so it holds authorisations, expires by credit type and appears in the same reports — a second balance on the entitlement would have been the seventh implementation.\n"},"includedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"validTimeWindows":{"type":"array","nullable":true,"description":"BL-036, 1.1.81 and 1.1.83. **A time-window entitlement needed a performance to express** — valid 09:00 to 13:00 on any day was a thing you built by creating performances.\n**A window is a property of the entitlement and a performance is an occurrence**, and conflating them means a morning pass generates 365 performances a year.\n","items":{"type":"object","properties":{"from":{"type":"string"},"to":{"type":"string"},"daysOfWeek":{"type":"array","items":{"type":"string"}}}}},"blackoutDates":{"type":"array","nullable":true,"description":"**Calendar exceptions on the entitlement.** An annual pass excluding public holidays is the normal case and had nowhere to live.\n","items":{"type":"string","format":"date"}},"fastTrackTier":{"type":"string","nullable":true,"enum":["none","priority","express","unlimited"],"description":"19.2.20, BL-015. **Fast track existed nowhere in the package** — not an enum value, not a description, not a screen.\n**An attribute of the entitlement rather than a queue class or a product kind**, because the same ride serves standby and fast-track guests from one capacity: `queue` already has `isFastPass` on an entry and needed something to read it from.\n"},"entriesAllowed":{"type":"integer","nullable":true,"description":"Null means unlimited. The Fast Pass consumption counter lives here."},"transportRestriction":{"type":"object","nullable":true,"description":"**The journey a transport pass is good for** (decided 29 September, rev 3 REV3-21). Set on the template `transport.createTransportPassType` creates, from the station pair the guest bought the pass for, and copied to the entitlement. `access` refuses a boarding scan whose departure does not serve both stations in a direction the restriction allows, and consumes one of `entriesAllowed` per boarding. Null on every other template.\n","required":["fromStationId","toStationId"],"properties":{"fromStationId":{"type":"string","format":"uuid","description":"A `transport.Station`."},"toStationId":{"type":"string","format":"uuid"},"bothDirections":{"type":"boolean","default":true,"description":"Valid from either station to the other, as the prototype sells it."},"routeIds":{"type":"array","description":"The routes it may be used on. Empty means any active route serving both stations.","items":{"type":"string","format":"uuid"}}}},"reentryAllowed":{"type":"boolean","default":false},"purchaseEligibility":{"type":"object","nullable":true,"description":"1.1.38, 1.1.121, 1.1.125, 1.1.126. **`admissionRulesId` governs where an entitlement admits, not who may buy it**, and `promotions.evaluatePromotions` gates a discount rather than a sale. Neither refuses a purchase.\n**Evaluated at add-to-cart, not at checkout.** A guest told at payment that they cannot buy a resident rate has already entered a card.\n","properties":{"minAgeYears":{"type":"integer","nullable":true},"maxAgeYears":{"type":"integer","nullable":true},"minHeightCm":{"type":"integer","nullable":true,"description":"**Height gates a ride and can gate a sale.** A ticket sold to somebody who cannot ride it is a refund at the gate.\n"},"residencyRequired":{"type":"boolean","default":false},"nationalities":{"type":"array","nullable":true,"items":{"type":"string"}},"minLoyaltyTier":{"type":"string","nullable":true},"requiresVerification":{"type":"boolean","default":false,"description":"**Whether the claim is checked or taken on trust.** A resident rate sold unverified and refused at the gate is worse than one that could not be bought.\n"}}},"personType":{"type":"string","nullable":true,"enum":["adult","child","infant","senior","student","resident","staff"],"description":"2.11.7. **Adult, child and senior existed only as `ProductVariant.axisValues` — a variant axis rather than an attribute of the holder.** So changing a child ticket to an adult one was an exchange to a different product, and an upgrade that should be a price difference became a cancel-and-rebuy.\nRecorded here as well as on the variant, because **the guest ages and the product does not.**\n"},"admissionRulesId":{"type":"string","format":"uuid","nullable":true},"isTransferable":{"type":"boolean","default":true},"canShareMedia":{"type":"boolean","default":true,"description":"Whether this entitlement may be appended to media a guest already holds (CF-58). False for anything surrendered at use — a single-entry ticket taken at the gate is not a claim token for a locker bought afterwards.\n"},"canClaimShopAndDrop":{"type":"boolean","default":false,"description":"Whether this entitlement may be scanned to claim goods left under 4.4.7. False for a single-entry ticket that is surrendered at the gate — a claim token the guest no longer holds is not a claim token.\n"},"isNameBound":{"type":"boolean","default":false,"description":"True requires a holder name at sale. Most entitlements carry none — identity and entitlement are separate concerns.\n"},"autoRenewDefault":{"type":"boolean","default":false,"description":"**Taken from their `membership_plan`, 20 September — the \"take those\" half of the TAKE BODY verdict.** `identity.customer_membership.auto_renew` carries the flag per holder and nothing said what it should start as.\n"},"renewalTermDays":{"type":"integer","nullable":true,"description":"What a renewal extends the membership by. `orders.membership_renewal` records `previousExpiryAt` and `newExpiryAt` and **the number between them lived nowhere**.\n"},"renewalGraceDays":{"type":"integer","default":0,"description":"How long after expiry a membership can still be renewed rather than rejoined. `membership_renewal.failureReason` implies a window and there was none, so a failed card on the expiry date had no defined consequence.\n"},"renewalVariantId":{"type":"string","format":"uuid","nullable":true,"description":"**What a renewal sells, which is usually not what joining sold.** A first-year price and a renewal price are different products, and pointing both at one variant makes a loyalty discount unrepresentable. Null means renewal sells the same thing.\n"},"crossesCells":{"type":"boolean","default":false,"description":"True propagates a redemption right to other cells on issue (ADR-0010).\n"},"isActive":{"type":"boolean"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.** Set by the server, never taken from a body."}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PriceList": {"x-ticvai-persistence":"catalogue.price_list","type":"object","required":["id","code","name","venueId","currency","currencyScale","channels"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire, removed from the table** — a client should not walk a hierarchy to read a figure, and the database should not hold nine million copies of AED. Four tables genuinely differ from their region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, `ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and cannot be anything else — storing it per row is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a client reading a figure should not walk a hierarchy to know what it means, and the database should not hold nine million copies of AED. Four tables genuinely differ from their region and keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.account`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a workstation with its own currency is a misconfiguration.**\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"priority":{"type":"integer","description":"Where lists overlap, higher priority wins."},"description":{"type":"string","nullable":true,"description":"Price list master fields (29 September, data model DM3), set with `setPriceListMaster` (ADM-058)."},"priceListType":{"type":"string","enum":["standardRetail","venue","attraction","event","membership","group","corporate","b2b","reseller","ota","internal","specialMarket"],"default":"standardRetail"},"status":{"allOf":[{"$ref":"#/components/schemas/CatalogueConfigStatus"}],"default":"active"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"tags":{"type":"array","items":{"type":"string"}},"legalEntityId":{"type":"string","format":"uuid","nullable":true},"brand":{"type":"string","maxLength":100,"nullable":true},"businessUnit":{"type":"string","maxLength":100,"nullable":true},"countryCode":{"type":"string","maxLength":2,"nullable":true,"pattern":"^[A-Z]{2}$"},"marketCode":{"type":"string","maxLength":40,"nullable":true},"scopeLevel":{"type":"string","enum":["global","country","market","brand","venue","event","businessUnit"],"default":"venue"},"defaultPriceCategoryId":{"type":"string","format":"uuid","nullable":true},"roundingProfileId":{"type":"string","format":"uuid","nullable":true},"priceResolutionPolicyId":{"type":"string","format":"uuid","nullable":true},"allowOverrides":{"type":"boolean","default":false},"allowInheritance":{"type":"boolean","default":true},"allowMultipleCurrencies":{"type":"boolean","default":false},"allowProductSpecificRates":{"type":"boolean","default":true},"clonedFromPriceListId":{"type":"string","format":"uuid","nullable":true},"currentVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The active `catalogue.price_list_version`."}}},
"SetPriceRequest": {"type":"object","required":["variantId","amount"],"properties":{"variantId":{"type":"string","format":"uuid"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxCodeId":{"type":"string","format":"uuid"}}}
}
```
