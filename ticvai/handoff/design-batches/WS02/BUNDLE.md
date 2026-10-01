# WS02 — Access Control board 2

**10 screens · 18 operations · 19 schemas · 4 permissions**

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
  `ACCESS_POINT_CONFIGURE, PRODUCT_CONFIGURE, PRODUCT_VIEW, SCOPE_VIEW`. A control nobody can use must say so,
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
| `BO-154` | Access Rule Command Center | B–D | 0 | 2 | 6 | 7 | 2 | 0 | — | notStarted (generated) |
| `BO-155` | Visual Access Rule Builder | A | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-156` | Entry, Exit & Re-entry Rules | B–D | 47 | 0 | 6 | 9 | 2 | 0 | — | notStarted (generated) |
| `BO-157` | Anti-Passback & Journey Sequence | B–D | 11 | 0 | 5 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-158` | Access Validity & Time Rules | B–D | 54 | 0 | 5 | 9 | 4 | 0 | — | notStarted (generated) |
| `BO-159` | Entitlement Consumption Engine | B–D | 10 | 0 | 6 | 0 | 3 | 0 | — | notStarted (generated) |
| `BO-160` | Multi-Park & Crossover Rules | B–D | 47 | 0 | 6 | 9 | 1 | 0 | — | notStarted (generated) |
| `BO-161` | Guest, Companion & Eligibility Rules | A | 18 | 8 | 5 | 1 | 1 | 0 | — | notStarted (generated) |
| `BO-162` | Group Admission & Quantity Validation | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-163` | Rule Simulation, Conflict Check & Publication | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-155, BO-156, BO-160, BO-162 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-154` Access Rule Command Center

**Central configuration dashboard for all access and entitlement rules.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Show) and a per-row directory (§Each rule displays) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/access-rule-command-center-bo-154` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listAccessRule` ?venue |
| Park | text field | — | — | `listAccessRule` ?park |
| Attraction | text field | — | — | `listAccessRule` ?attraction |
| Product | text field | — | — | `listAccessRule` ?product |
| Credential | text field | — | — | `listAccessRule` ?credential |
| Rule type | text field | — | — | `listAccessRule` ?ruleType |
| Status | text field | — | — | `listAccessRule` ?status |
| Date | text field | — | — | `listAccessRule` ?date |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Access Rules** (metric tile)

**Draft Rules** (metric tile)

**Scheduled Rules** (metric tile)

**Rules Pending Approval** (metric tile)

**Venues Covered** (metric tile)

**Products/Tickets Covered** (metric tile)

**Rules with Conflicts** (metric tile)

**Rules Using Biometrics** (metric tile)

**Rules Allowing Override** (metric tile)

**Offline-Compatible Rules** (metric tile)

**Recently Modified Rules** (metric tile)

**Upcoming Rule Changes** (metric tile)

**Every access rule** (data table, from `listAccessRule`)

| Shows | Format | Notes |
|---|---|---|
| Rule applies to location validity status | text | not in the schema: `Rule Applies To Location Validity Status` |

**The selected access rule** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Rule applies to location validity status | text | not in the schema: `Rule Applies To Location Validity Status` |

**Data it reads**: `listAccessRule` (onLoad, Access Rule Command Center); `listAdmissionRules` (onLoad, Every admission rule with its scope)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-155` Visual Access Rule Builder: *Works in Visual Access Rule Builder*; calls `listAccessRule`
- → `BO-156` Entry, Exit & Re-entry Rules: *Works in Entry, Exit & Re-entry Rules*; calls `listAccessRule`
- → `BO-158` Access Validity & Time Rules: *Works in Access Validity & Time Rules*; calls `listAccessRule`
- → `BO-159` Entitlement Consumption Engine: *Works in Entitlement Consumption Engine*; calls `listAccessRule`
- → `BO-160` Multi-Park & Crossover Rules: *Works in Multi-Park & Crossover Rules*; calls `listAccessRule`
- → `BO-162` Group Admission & Quantity Validation: *Works in Group Admission & Quantity Validation*; calls `listAccessRule`
- → `BO-163` Rule Simulation, Conflict Check & Publication: *Works in Rule Simulation, Conflict Check & Publication*; calls `listAccessRule`
- → `BO-157` Anti-Passback & Journey Sequence: *Works in Anti-Passback & Journey Sequence*; carries `ruleId`; calls `listAccessRule`
- → `BO-161` Guest, Companion & Eligibility Rules: *Works in Guest, Companion & Eligibility Rules*; carries `productId`; calls `listAccessRule`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access rule list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAccessRule` → `SCOPE_VIEW` (read) · staff
- `listAdmissionRules` → `SCOPE_VIEW` (read) · staff
- `createAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.7 | The system should support multiple validity rules access entitlements associated with a ticket. The available entry rules can be changed without required additional development effort for configuring … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.10 | The system should be able to expire a ticket if it is not used within a specified time (e.g. 20 minutes) from the admission time specified on the ticket or based on the time of the performance/event. … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.59 | Some tickets may be entitled to reentry. | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.70 | The access control rules can support all multi-park requirements, such as but not limited to: -multi-park access on different days, -crossover feature i.e. access to another park on the same day as … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 7.4.22 | For special ticket, it can be restricted to particular group of people and have precondition ex: companion ticket | F&B POS | CONTRACTED | `listAdmissionRules` |
| 7.4.25 | For each PLU, it is possible to manage Usage zone or attraction access control restriction | F&B POS | CONTRACTED | `listAdmissionRules` |
| 1.1.51 | Admission entitlement management | Ticketing Catalogue | CONTRACTED | `createAdmissionRules` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Access rules dashboard shows active rules, drafts and status. Rules: one entry per day vs unlimited or limited re-entry; exit scan required or exit in free rotation; turnstile modes (free rotation, entry, exit); anti-passback window with exit-before-re-entry option. *(client request · MoM 2 Sep 2026, 4.3 Access Rules - Entry/Exit, Anti-Passback & Validity · DI-626)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-154` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-154`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 1: Opens Access Rule Command Center → Central configuration dashboard for all access and entitlement rules.
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F112 branch at step 1 (expected): when Nothing has been set up on Access Rule Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F112 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-154?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-155`, `BO-156`, `BO-158`, `BO-159`, `BO-160`, `BO-162`, `BO-163`, `BO-157`, `BO-161`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-155` Visual Access Rule Builder

**Provide a no-code rule engine. This is where TICVAI should become significantly easier to configure than traditional access-control systems.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block A · ticket #20672 (APP-SETUP-BO-155) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/visual-access-rule-builder-bo-155` |

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

- → `BO-154` Access Rule Command Center: *Returns to the board's landing screen*; calls `setVisualAccessRule`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The visual access rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the visual access rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No visual access rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the visual access rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setVisualAccessRule` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Tiered access (e.g. Bronze/Silver/Gold): the client fills a matrix of which gates/attractions each tier may scan into; configured as location → admission profile → gate → access point, with explicit deny rules (e.g. Gold denied at the Silver/Bronze entrance). *(agreed · MoM 7 Aug 2026, 24. Tiered Ticketing & Access Control Deep Dive · DI-185)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-155` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-155`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 2: Works in Visual Access Rule Builder → Provide a no-code rule engine. This is where TICVAI should become significantly easier to configure than traditional access-control systems.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-155?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-154`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-156` Entry, Exit & Re-entry Rules

**Configure admission quantity and journey sequencing. The source matrix explicitly requires configurable quantities for entry, exit and same-day re-entry, anti- passback intervals, required exit before re-entry, and required entry before exit.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `profileId` (navigation) |
| Route | `/access-venue/entry-exit-re-entry-rules-bo-156` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Sent by *Save admission rules*** (`updateAdmissionRules`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `updateAdmissionRules` body |
| Per product rules `perProductRules` | repeatable rows | optional | — | — | — | BL-059. Transaction rules were per profile and a ticket type could not state its own. | `updateAdmissionRules` body |
| Product `perProductRules[].productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `updateAdmissionRules` body |
| Entries per day `perProductRules[].entriesPerDay` | number field | optional | — | — | — | — | `updateAdmissionRules` body |
| Minimum gap minutes `perProductRules[].minimumGapMinutes` | number field (minutes) | optional | — | — | — | Anti-passback in minutes rather than a boolean. A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back … | `updateAdmissionRules` body |
| Allowed access points `perProductRules[].allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | — | `updateAdmissionRules` body |
| Biometric policy `perProductRules[].biometricPolicy` | segmented control | optional | — | Disabled · Offered · Preferred | — | BL-105, 3.2.9. The biometric check is a property of the product, not of the venue — memberships checked, day tickets not. | `updateAdmissionRules` body |
| Max passes per biometric identity `perProductRules[].maxPassesPerBiometricIdentity` | number field | optional | — | min 1 | — | BL-096, 2.14.7. The annual-pass quota, keyed to biometric identity. | `updateAdmissionRules` body |
| Name `name` | text field | required | — | max length 200 | — | — | `updateAdmissionRules` body |
| Open minutes before `openMinutesBefore` | number field (minutes) | required | — | — | — | How long before a performance validation opens. | `updateAdmissionRules` body |
| Close minutes after `closeMinutesAfter` | number field (minutes) | required | — | — | — | — | `updateAdmissionRules` body |
| Max duration minutes `maxDurationMinutes` | number field (minutes) | optional | — | — | — | — | `updateAdmissionRules` body |
| Requires exit before reentry `requiresExitBeforeReentry` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Max reentries `maxReentries` | number field | optional | — | — | — | — | `updateAdmissionRules` body |
| Entry limit `entryLimit` | group | optional | — | — | — | How many times the credential may enter (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). | `updateAdmissionRules` body |
| Mode `entryLimit.mode` | radio group | required | Unlimited | Unlimited · Once · N times · N per day · N per period | — | — | `updateAdmissionRules` body |
| Count `entryLimit.count` | number field | optional | — | min 1 | — | N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it) | `updateAdmissionRules` body |
| Period days `entryLimit.periodDays` | number field (days) | optional | — | min 1 | — | The period for nPerPeriod | `updateAdmissionRules` body |
| Exit scan `exitScan` | segmented control | optional | Optional | Required · Optional · None | — | (decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. | `updateAdmissionRules` body |
| Max exits `maxExits` | number field | optional | — | min 0 | — | Null is unlimited (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Re entry window minutes `reEntryWindowMinutes` | number field (minutes) | optional | — | min 1 | — | Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Same day only `sameDayOnly` | toggle | optional | on | — | — | Re-entry only on the day of the exit (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Designated access points `designatedAccessPointIds` | multi-picker: choose designated access points | optional | — | — | — | Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Validity `validity` | group | optional | — | — | — | When the credential is valid (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). | `updateAdmissionRules` body |
| Anchor `validity.anchor` | radio group | required | — | Fixed range · After sale · After activation · After first use | — | fixedRange uses from and to; the others count days from the event | `updateAdmissionRules` body |
| Days `validity.days` | number field | optional | — | min 1 | — | N days after the anchor; required unless the anchor is fixedRange | `updateAdmissionRules` body |
| From `validity.from` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateAdmissionRules` body |
| To `validity.to` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Inclusive. | `updateAdmissionRules` body |
| End of `validity.endOf` | radio group | optional | — | Day · Week · Month · Year | — | Validity runs to the end of the day, week, month or year the relative period ends in | `updateAdmissionRules` body |
| Days of week `validity.daysOfWeek` | multi-select chips | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | Empty is every day | `updateAdmissionRules` body |
| Day types `validity.dayTypes` | multi-select chips | optional | — | Peak dates · Off peak dates · Holidays · Seasons · Event dates | — | Calendar day types on which access is allowed; empty is every day type | `updateAdmissionRules` body |
| Blackout dates `validity.blackoutDates` | list of values (chips) | optional | — | — | — | Dates on which access is refused whatever else allows it | `updateAdmissionRules` body |
| Crossover `crossover` | group | optional | — | — | — | Crossover between parks (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. | `updateAdmissionRules` body |
| Allowed park org units `crossover.allowedParkOrgUnitIds` | multi-picker: choose allowed park org units | required | — | at least 2 | — | — | `updateAdmissionRules` body |
| Park order `crossover.parkOrder` | multi-picker: choose park order | optional | — | — | — | Required order of parks, if any; empty is any order | `updateAdmissionRules` body |
| Same day only `crossover.sameDayOnly` | toggle | optional | on | — | — | — | `updateAdmissionRules` body |
| Different day access `crossover.differentDayAccess` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Day pattern `crossover.dayPattern` | segmented control | optional | Flexible within validity | Consecutive from first scan · Flexible within validity | — | — | `updateAdmissionRules` body |
| Max park entries `crossover.maxParkEntries` | number field | optional | — | min 1 | — | Null is unlimited | `updateAdmissionRules` body |
| Crossover quantity `crossover.crossoverQuantity` | number field | optional | — | min 1 | — | How many crossovers; null is unlimited | `updateAdmissionRules` body |
| Crossover after time `crossover.crossoverAfterTime` | time picker | optional | — | — | HH:mm, 24-hour | Earliest venue-local time HH:MM a crossover is allowed | `updateAdmissionRules` body |
| Prerequisite park org unit `crossover.prerequisiteParkOrgUnitId` | picker: choose a prerequisite park org unit | optional | — | — | shows names, sends the id | The park that must be entered first | `updateAdmissionRules` body |
| Re entry after crossover `crossover.reEntryAfterCrossover` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Allowed access points `allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Empty means any access point in the venue. | `updateAdmissionRules` body |
| Re entry verification `reEntryVerification` | radio group | optional | Credential only | Credential only · Credential uv stamp · Credential face · Credential operator · Custom | — | What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1). | `updateAdmissionRules` body |
| … 2 more | | | | | | the rest are in `schemas.json` | `updateAdmissionRules` body |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save admission rules (primary button) | `updateAdmissionRules` PUT `/admission-rules/{profileId}` | AdmissionRules | AdmissionRules | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before … | — |

**Data it reads**: `listEntryExitRule` (onLoad, Entry, Exit & Re-entry Rules); `listAdmissionRules` (onLoad, The admission profiles whose entry, exit and re-entry rules …)

**Where the user goes next**

- → `BO-154` Access Rule Command Center: *Returns to the board's landing screen*; calls `listEntryExitRule`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The entry exit re-entry list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the entry exit re-entry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No entry exit re-entry yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the entry exit re-entry are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before validity.from |

#### Permissions

- `listEntryExitRule` → `SCOPE_VIEW` (read) · staff
- `listAdmissionRules` → `SCOPE_VIEW` (read) · staff
- `updateAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.7 | The system should support multiple validity rules access entitlements associated with a ticket. The available entry rules can be changed without required additional development effort for configuring … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.10 | The system should be able to expire a ticket if it is not used within a specified time (e.g. 20 minutes) from the admission time specified on the ticket or based on the time of the performance/event. … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.59 | Some tickets may be entitled to reentry. | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.70 | The access control rules can support all multi-park requirements, such as but not limited to: -multi-park access on different days, -crossover feature i.e. access to another park on the same day as … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 7.4.22 | For special ticket, it can be restricted to particular group of people and have precondition ex: companion ticket | F&B POS | CONTRACTED | `listAdmissionRules` |
| 7.4.25 | For each PLU, it is possible to manage Usage zone or attraction access control restriction | F&B POS | CONTRACTED | `listAdmissionRules` |
| 3.2.34 | The access rules can be modified even after the ticket has been issued. | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.62 | It must be possible to change the access control organization process on special dates. Venue is organizing on regular basis free view days where the main gate access control doors are opened letting … | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.71 | The access control can support special requirements for special events such as but not limited to: -definition of a specific product that can capture attendance without physical admission, -special … | Admission and Access | CONTRACTED | `updateAdmissionRules` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Access rules dashboard shows active rules, drafts and status. Rules: one entry per day vs unlimited or limited re-entry; exit scan required or exit in free rotation; turnstile modes (free rotation, entry, exit); anti-passback window with exit-before-re-entry option. *(client request · MoM 2 Sep 2026, 4.3 Access Rules - Entry/Exit, Anti-Passback & Validity · DI-626)*
- If a guest exits without a matching checkout scan (e.g. a manually opened door), the system flags it and blocks the next re-entry scan until check-in/check-out is reconciled. *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-461)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-156` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-156`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 4: Works in Entry, Exit & Re-entry Rules → Configure admission quantity and journey sequencing. The source matrix explicitly requires configurable quantities for entry, exit and same-day re-entry, anti- passback intervals, required exit …

#### Acceptance for the design

- [ ] Every input above is drawn (47), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-156?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save admission rules.
- [ ] Every transition is wired: `BO-154`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-157` Anti-Passback & Journey Sequence

**Prevent credential sharing and impossible access sequences.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure required sequences such as) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `ruleId` (navigation) |
| Route | `/access-venue/anti-passback-journey-sequence-bo-157` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| ENTRY → EXIT → RE-ENTRY | text field | — | — | — | — | — | — |
| PARK A → CROSSOVER → PARK B | text field | — | — | — | — | — | — |
| MAIN ENTRY → ATTRACTION ENTRY | text field | — | — | — | — | — | — |

**Form: Save journey sequence rule** (modal, opened by *Save journey sequence rule*; *Save journey sequence rule* calls `setJourneySequenceRule`, *Cancel* sends nothing)

**Collects what `setJourneySequenceRule` sends before it is called.** Required: `id`, `scopePath`, `scope`. Optional: `venueId`, `name`, `windowMinutes`, `requiredSequence`, `violationResponses`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setJourneySequenceRule` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `setJourneySequenceRule` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node | `setJourneySequenceRule` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `setJourneySequenceRule` body |
| Scope `scope` | select | required | — | Credential · Guest · Gate · Attraction · Park · Venue | — | Level the anti-passback check applies at | `setJourneySequenceRule` body |
| Window minutes `windowMinutes` | number field (minutes) | optional | — | min 0 | — | — | `setJourneySequenceRule` body |
| Required sequence `requiredSequence` | list of values (chips) | optional | — | — | — | Ordered steps, e.g. | `setJourneySequenceRule` body |
| Violation responses `violationResponses` | multi-select chips | optional | — | Deny · Warning · Refer to operator · Require supervisor · Allow override · Trigger security alert | — | — | `setJourneySequenceRule` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save journey sequence rule (primary button) | `setJourneySequenceRule` PUT `/journey-sequence-rules` | AccessJourneySequenceRule | AccessJourneySequenceRule | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |
| Delete journey sequence rule (destructive button) | `deleteJourneySequenceRule` DELETE `/journey-sequence-rules/{ruleId}` | — | — | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE` |

**Data it reads**: `listAntiPassbackJourney` (onLoad, Anti-Passback & Journey Sequence)

**Where the user goes next**

- → `BO-154` Access Rule Command Center: *Returns to the board's landing screen*; calls `listAntiPassbackJourney`

**What opens over it**

- confirmDialog *Delete journey sequence rule*: **Names what `deleteJourneySequenceRule` changes and what it leaves alone**, in the consequence rather than the verb. A record this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The anti-passback journey sequence configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the anti-passback journey sequence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No anti-passback journey sequence configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listAntiPassbackJourney` → `SCOPE_VIEW` (read) · staff
- `setJourneySequenceRule` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `deleteJourneySequenceRule` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Access rules dashboard shows active rules, drafts and status. Rules: one entry per day vs unlimited or limited re-entry; exit scan required or exit in free rotation; turnstile modes (free rotation, entry, exit); anti-passback window with exit-before-re-entry option. *(client request · MoM 2 Sep 2026, 4.3 Access Rules - Entry/Exit, Anti-Passback & Validity · DI-626)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-157` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-157`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 6: Works in Anti-Passback & Journey Sequence → Prevent credential sharing and impossible access sequences.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-157?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save journey sequence rule, Delete journey sequence rule.
- [ ] Every transition is wired: `BO-154`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-158` Access Validity & Time Rules

**Determine when access is permitted.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `profileId` (navigation) |
| Route | `/access-venue/access-validity-time-rules-bo-158` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| weekdays | select field | — | — | — | — | — | — |
| weekends | select field | — | — | — | — | — | — |
| peak dates | select field | — | — | — | — | — | — |
| off-peak dates | select field | — | — | — | — | — | — |
| holidays | select field | — | — | — | — | — | — |
| seasons | select field | — | — | — | — | — | — |
| event dates | select field | — | — | — | — | — | — |

**Sent by *Save admission rules*** (`updateAdmissionRules`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `updateAdmissionRules` body |
| Per product rules `perProductRules` | repeatable rows | optional | — | — | — | BL-059. Transaction rules were per profile and a ticket type could not state its own. | `updateAdmissionRules` body |
| Product `perProductRules[].productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `updateAdmissionRules` body |
| Entries per day `perProductRules[].entriesPerDay` | number field | optional | — | — | — | — | `updateAdmissionRules` body |
| Minimum gap minutes `perProductRules[].minimumGapMinutes` | number field (minutes) | optional | — | — | — | Anti-passback in minutes rather than a boolean. A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back … | `updateAdmissionRules` body |
| Allowed access points `perProductRules[].allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | — | `updateAdmissionRules` body |
| Biometric policy `perProductRules[].biometricPolicy` | segmented control | optional | — | Disabled · Offered · Preferred | — | BL-105, 3.2.9. The biometric check is a property of the product, not of the venue — memberships checked, day tickets not. | `updateAdmissionRules` body |
| Max passes per biometric identity `perProductRules[].maxPassesPerBiometricIdentity` | number field | optional | — | min 1 | — | BL-096, 2.14.7. The annual-pass quota, keyed to biometric identity. | `updateAdmissionRules` body |
| Name `name` | text field | required | — | max length 200 | — | — | `updateAdmissionRules` body |
| Open minutes before `openMinutesBefore` | number field (minutes) | required | — | — | — | How long before a performance validation opens. | `updateAdmissionRules` body |
| Close minutes after `closeMinutesAfter` | number field (minutes) | required | — | — | — | — | `updateAdmissionRules` body |
| Max duration minutes `maxDurationMinutes` | number field (minutes) | optional | — | — | — | — | `updateAdmissionRules` body |
| Requires exit before reentry `requiresExitBeforeReentry` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Max reentries `maxReentries` | number field | optional | — | — | — | — | `updateAdmissionRules` body |
| Entry limit `entryLimit` | group | optional | — | — | — | How many times the credential may enter (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). | `updateAdmissionRules` body |
| Mode `entryLimit.mode` | radio group | required | Unlimited | Unlimited · Once · N times · N per day · N per period | — | — | `updateAdmissionRules` body |
| Count `entryLimit.count` | number field | optional | — | min 1 | — | N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it) | `updateAdmissionRules` body |
| Period days `entryLimit.periodDays` | number field (days) | optional | — | min 1 | — | The period for nPerPeriod | `updateAdmissionRules` body |
| Exit scan `exitScan` | segmented control | optional | Optional | Required · Optional · None | — | (decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. | `updateAdmissionRules` body |
| Max exits `maxExits` | number field | optional | — | min 0 | — | Null is unlimited (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Re entry window minutes `reEntryWindowMinutes` | number field (minutes) | optional | — | min 1 | — | Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Same day only `sameDayOnly` | toggle | optional | on | — | — | Re-entry only on the day of the exit (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Designated access points `designatedAccessPointIds` | multi-picker: choose designated access points | optional | — | — | — | Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Validity `validity` | group | optional | — | — | — | When the credential is valid (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). | `updateAdmissionRules` body |
| Anchor `validity.anchor` | radio group | required | — | Fixed range · After sale · After activation · After first use | — | fixedRange uses from and to; the others count days from the event | `updateAdmissionRules` body |
| Days `validity.days` | number field | optional | — | min 1 | — | N days after the anchor; required unless the anchor is fixedRange | `updateAdmissionRules` body |
| From `validity.from` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateAdmissionRules` body |
| To `validity.to` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Inclusive. | `updateAdmissionRules` body |
| End of `validity.endOf` | radio group | optional | — | Day · Week · Month · Year | — | Validity runs to the end of the day, week, month or year the relative period ends in | `updateAdmissionRules` body |
| Days of week `validity.daysOfWeek` | multi-select chips | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | Empty is every day | `updateAdmissionRules` body |
| Day types `validity.dayTypes` | multi-select chips | optional | — | Peak dates · Off peak dates · Holidays · Seasons · Event dates | — | Calendar day types on which access is allowed; empty is every day type | `updateAdmissionRules` body |
| Blackout dates `validity.blackoutDates` | list of values (chips) | optional | — | — | — | Dates on which access is refused whatever else allows it | `updateAdmissionRules` body |
| Crossover `crossover` | group | optional | — | — | — | Crossover between parks (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. | `updateAdmissionRules` body |
| Allowed park org units `crossover.allowedParkOrgUnitIds` | multi-picker: choose allowed park org units | required | — | at least 2 | — | — | `updateAdmissionRules` body |
| Park order `crossover.parkOrder` | multi-picker: choose park order | optional | — | — | — | Required order of parks, if any; empty is any order | `updateAdmissionRules` body |
| Same day only `crossover.sameDayOnly` | toggle | optional | on | — | — | — | `updateAdmissionRules` body |
| Different day access `crossover.differentDayAccess` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Day pattern `crossover.dayPattern` | segmented control | optional | Flexible within validity | Consecutive from first scan · Flexible within validity | — | — | `updateAdmissionRules` body |
| Max park entries `crossover.maxParkEntries` | number field | optional | — | min 1 | — | Null is unlimited | `updateAdmissionRules` body |
| Crossover quantity `crossover.crossoverQuantity` | number field | optional | — | min 1 | — | How many crossovers; null is unlimited | `updateAdmissionRules` body |
| Crossover after time `crossover.crossoverAfterTime` | time picker | optional | — | — | HH:mm, 24-hour | Earliest venue-local time HH:MM a crossover is allowed | `updateAdmissionRules` body |
| Prerequisite park org unit `crossover.prerequisiteParkOrgUnitId` | picker: choose a prerequisite park org unit | optional | — | — | shows names, sends the id | The park that must be entered first | `updateAdmissionRules` body |
| Re entry after crossover `crossover.reEntryAfterCrossover` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Allowed access points `allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Empty means any access point in the venue. | `updateAdmissionRules` body |
| Re entry verification `reEntryVerification` | radio group | optional | Credential only | Credential only · Credential uv stamp · Credential face · Credential operator · Custom | — | What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1). | `updateAdmissionRules` body |
| … 2 more | | | | | | the rest are in `schemas.json` | `updateAdmissionRules` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| From / To (primary button) | navigation or local | — | — | — | — |
| End of Day (destructive button) | navigation or local | — | — | — | — |
| End of Week (destructive button) | navigation or local | — | — | — | — |
| End of Month (destructive button) | navigation or local | — | — | — | — |
| Save admission rules (primary button) | `updateAdmissionRules` PUT `/admission-rules/{profileId}` | AdmissionRules | AdmissionRules | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before … | — |

**Data it reads**: `listAccessValidityTime` (onLoad, Access Validity & Time Rules); `listAdmissionRules` (onLoad, The admission profiles whose validity windows are edited …)

**Where the user goes next**

- → `BO-154` Access Rule Command Center: *Returns to the board's landing screen*; calls `listAccessValidityTime`

**What opens over it**

- confirmDialog *End of Day*: **End of Day on a access validity time is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *End of Week*: **End of Week on a access validity time is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *End of Month*: **End of Month on a access validity time is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access validity time configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access validity time untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access validity time configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before validity.from |

#### Permissions

- `listAccessValidityTime` → `SCOPE_VIEW` (read) · staff
- `listAdmissionRules` → `SCOPE_VIEW` (read) · staff
- `updateAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.7 | The system should support multiple validity rules access entitlements associated with a ticket. The available entry rules can be changed without required additional development effort for configuring … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.10 | The system should be able to expire a ticket if it is not used within a specified time (e.g. 20 minutes) from the admission time specified on the ticket or based on the time of the performance/event. … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.59 | Some tickets may be entitled to reentry. | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.70 | The access control rules can support all multi-park requirements, such as but not limited to: -multi-park access on different days, -crossover feature i.e. access to another park on the same day as … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 7.4.22 | For special ticket, it can be restricted to particular group of people and have precondition ex: companion ticket | F&B POS | CONTRACTED | `listAdmissionRules` |
| 7.4.25 | For each PLU, it is possible to manage Usage zone or attraction access control restriction | F&B POS | CONTRACTED | `listAdmissionRules` |
| 3.2.34 | The access rules can be modified even after the ticket has been issued. | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.62 | It must be possible to change the access control organization process on special dates. Venue is organizing on regular basis free view days where the main gate access control doors are opened letting … | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.71 | The access control can support special requirements for special events such as but not limited to: -definition of a specific product that can capture attendance without physical admission, -special … | Admission and Access | CONTRACTED | `updateAdmissionRules` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Validity date range plus blockout dates (e.g. public holidays, special event days); entry allowance consumption blocks use once exhausted; multi-park crossover (how many parks, same-day or one per day, consecutive or flexible days); companion rules (child ticket needs a qualifying adult). *(client request · MoM 2 Sep 2026, 4.3 / 4.4 Validity, Crossover & Companion Rules · DI-628)*
- Entitlements go beyond admission — e.g. a combo of park admission + an F&B item + a retail item, each redeemed by QR scan at its counter. Admission entitlements cap entries per ticket (e.g. max 2); product entitlements give a time-bound window (e.g. 60 minutes from first scan). *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-458)*
- Supporting configuration: ticket variants (adult/child/senior/VIP, configurable), waitlist, on-sale/off-sale timing and cut-offs, entitlement/access rules (single/multi-venue, entries, zones, early entry), fulfilment channels (email, WhatsApp, SMS), after-sales windows (upgrade, reschedule, cancel), dynamic/fixed pricing and promotions. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-437)*
- Entitlement settings: re-entry not allowed / once per day / unlimited; expiry end of week, month, year, variable date, from first use, or by performance date/time; group tickets by fixed price or fixed quantity; one ticket may link to several events. *(agreed · MoM 7 Aug 2026, 16. Entitlement Components: Re-entry, Expiration & Sale Restrictions · DI-171)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-158` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-158`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 8: Works in Access Validity & Time Rules → Determine when access is permitted.

#### Acceptance for the design

- [ ] Every input above is drawn (54), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-158?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: From / To, End of Day, End of Week, End of Month, Save admission rules.
- [ ] Every transition is wired: `BO-154`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-159` Entitlement Consumption Engine

**Determine what gets consumed when access is granted. This is critical because one credential may represent several different entitlements. The matrix specifically describes a single QR capable of carrying park admission, ride entitlement, meal voucher, coupon, photo voucher and re-entry rights.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/entitlement-consumption-engine-bo-159` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Sent by *Save consumption rule*** (`setEntitlementConsumption`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Rule `ruleId` | picker: choose a rule | optional | — | — | shows names, sends the id | Absent creates a rule | `setEntitlementConsumption` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setEntitlementConsumption` body |
| Credential type `credentialType` | text field | optional | — | — | — | Credential or product type the rule applies to | `setEntitlementConsumption` body |
| Entitlement type `entitlementType` | select | required | — | Park admission · Attraction admission · Ride · Fast pass · Meal · Voucher · Photo · Locker · Event · Experience · Re entry · Membership benefit … | — | — | `setEntitlementConsumption` body |
| Consumption order `consumptionOrder` | number field | optional | 1 | min 1 | — | Where one scan could consume several entitlements, lower is consumed first | `setEntitlementConsumption` body |
| Consumption per validation `consumptionPerValidation` | number field | optional | 1 | min 1 | — | Units one scan consumes | `setEntitlementConsumption` body |
| Quantity `quantity` | number field | optional | — | min 1 | — | Units the entitlement carries; ignored when unlimited | `setEntitlementConsumption` body |
| Unlimited `unlimited` | toggle | optional | off | — | — | — | `setEntitlementConsumption` body |
| One per attraction `onePerAttraction` | toggle | optional | off | — | — | — | `setEntitlementConsumption` body |
| Attractions `attractionIds` | list of values (chips) | optional | — | — | — | Empty means every attraction the entitlement covers | `setEntitlementConsumption` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Attraction Admission (primary button) | navigation or local | — | — | — | — |
| Voucher (secondary button) | navigation or local | — | — | — | — |
| Event (secondary button) | navigation or local | — | — | — | — |
| Experience (secondary button) | navigation or local | — | — | — | — |
| Membership benefit (secondary button) | navigation or local | — | — | — | — |
| Save consumption rule (primary button) | `setEntitlementConsumption` PUT `/entitlement-consumption` | EntitlementConsumptionEngineInput | EntitlementConsumptionEngineView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 Neither quantity nor unlimited given | — |

**Data it reads**: `listEntitlementConsumption` (onLoad, Entitlement Consumption Engine)

**Where the user goes next**

- → `BO-154` Access Rule Command Center: *Returns to the board's landing screen*; calls `listEntitlementConsumption`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The entitlement consumption list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the entitlement consumption untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No entitlement consumption yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the entitlement consumption are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 Neither quantity nor unlimited given |

#### Permissions

- `listEntitlementConsumption` → `SCOPE_VIEW` (read) · staff
- `setEntitlementConsumption` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Validity date range plus blockout dates (e.g. public holidays, special event days); entry allowance consumption blocks use once exhausted; multi-park crossover (how many parks, same-day or one per day, consecutive or flexible days); companion rules (child ticket needs a qualifying adult). *(client request · MoM 2 Sep 2026, 4.3 / 4.4 Validity, Crossover & Companion Rules · DI-628)*
- Entitlements go beyond admission — e.g. a combo of park admission + an F&B item + a retail item, each redeemed by QR scan at its counter. Admission entitlements cap entries per ticket (e.g. max 2); product entitlements give a time-bound window (e.g. 60 minutes from first scan). *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-458)*
- Entitlement settings: re-entry not allowed / once per day / unlimited; expiry end of week, month, year, variable date, from first use, or by performance date/time; group tickets by fixed price or fixed quantity; one ticket may link to several events. *(agreed · MoM 7 Aug 2026, 16. Entitlement Components: Re-entry, Expiration & Sale Restrictions · DI-171)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-159` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-159`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 10: Works in Entitlement Consumption Engine → Determine what gets consumed when access is granted. This is critical because one credential may represent several different entitlements. The matrix specifically describes a single QR capable of …

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-159?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Attraction Admission, Voucher, Event, Experience, Membership benefit, Save consumption rule.
- [ ] Every transition is wired: `BO-154`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-160` Multi-Park & Crossover Rules

**Configure complex access between multiple parks/venues. The matrix specifically requires multi-park access on different days, same-day crossover, park-specific entry quantities and conditional access based on previous park admission.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `profileId` (navigation) |
| Route | `/access-venue/multi-park-crossover-rules-bo-160` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Sent by *Save admission rules*** (`updateAdmissionRules`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `updateAdmissionRules` body |
| Per product rules `perProductRules` | repeatable rows | optional | — | — | — | BL-059. Transaction rules were per profile and a ticket type could not state its own. | `updateAdmissionRules` body |
| Product `perProductRules[].productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `updateAdmissionRules` body |
| Entries per day `perProductRules[].entriesPerDay` | number field | optional | — | — | — | — | `updateAdmissionRules` body |
| Minimum gap minutes `perProductRules[].minimumGapMinutes` | number field (minutes) | optional | — | — | — | Anti-passback in minutes rather than a boolean. A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back … | `updateAdmissionRules` body |
| Allowed access points `perProductRules[].allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | — | `updateAdmissionRules` body |
| Biometric policy `perProductRules[].biometricPolicy` | segmented control | optional | — | Disabled · Offered · Preferred | — | BL-105, 3.2.9. The biometric check is a property of the product, not of the venue — memberships checked, day tickets not. | `updateAdmissionRules` body |
| Max passes per biometric identity `perProductRules[].maxPassesPerBiometricIdentity` | number field | optional | — | min 1 | — | BL-096, 2.14.7. The annual-pass quota, keyed to biometric identity. | `updateAdmissionRules` body |
| Name `name` | text field | required | — | max length 200 | — | — | `updateAdmissionRules` body |
| Open minutes before `openMinutesBefore` | number field (minutes) | required | — | — | — | How long before a performance validation opens. | `updateAdmissionRules` body |
| Close minutes after `closeMinutesAfter` | number field (minutes) | required | — | — | — | — | `updateAdmissionRules` body |
| Max duration minutes `maxDurationMinutes` | number field (minutes) | optional | — | — | — | — | `updateAdmissionRules` body |
| Requires exit before reentry `requiresExitBeforeReentry` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Max reentries `maxReentries` | number field | optional | — | — | — | — | `updateAdmissionRules` body |
| Entry limit `entryLimit` | group | optional | — | — | — | How many times the credential may enter (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). | `updateAdmissionRules` body |
| Mode `entryLimit.mode` | radio group | required | Unlimited | Unlimited · Once · N times · N per day · N per period | — | — | `updateAdmissionRules` body |
| Count `entryLimit.count` | number field | optional | — | min 1 | — | N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it) | `updateAdmissionRules` body |
| Period days `entryLimit.periodDays` | number field (days) | optional | — | min 1 | — | The period for nPerPeriod | `updateAdmissionRules` body |
| Exit scan `exitScan` | segmented control | optional | Optional | Required · Optional · None | — | (decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. | `updateAdmissionRules` body |
| Max exits `maxExits` | number field | optional | — | min 0 | — | Null is unlimited (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Re entry window minutes `reEntryWindowMinutes` | number field (minutes) | optional | — | min 1 | — | Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Same day only `sameDayOnly` | toggle | optional | on | — | — | Re-entry only on the day of the exit (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Designated access points `designatedAccessPointIds` | multi-picker: choose designated access points | optional | — | — | — | Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Validity `validity` | group | optional | — | — | — | When the credential is valid (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). | `updateAdmissionRules` body |
| Anchor `validity.anchor` | radio group | required | — | Fixed range · After sale · After activation · After first use | — | fixedRange uses from and to; the others count days from the event | `updateAdmissionRules` body |
| Days `validity.days` | number field | optional | — | min 1 | — | N days after the anchor; required unless the anchor is fixedRange | `updateAdmissionRules` body |
| From `validity.from` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateAdmissionRules` body |
| To `validity.to` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Inclusive. | `updateAdmissionRules` body |
| End of `validity.endOf` | radio group | optional | — | Day · Week · Month · Year | — | Validity runs to the end of the day, week, month or year the relative period ends in | `updateAdmissionRules` body |
| Days of week `validity.daysOfWeek` | multi-select chips | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | Empty is every day | `updateAdmissionRules` body |
| Day types `validity.dayTypes` | multi-select chips | optional | — | Peak dates · Off peak dates · Holidays · Seasons · Event dates | — | Calendar day types on which access is allowed; empty is every day type | `updateAdmissionRules` body |
| Blackout dates `validity.blackoutDates` | list of values (chips) | optional | — | — | — | Dates on which access is refused whatever else allows it | `updateAdmissionRules` body |
| Crossover `crossover` | group | optional | — | — | — | Crossover between parks (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. | `updateAdmissionRules` body |
| Allowed park org units `crossover.allowedParkOrgUnitIds` | multi-picker: choose allowed park org units | required | — | at least 2 | — | — | `updateAdmissionRules` body |
| Park order `crossover.parkOrder` | multi-picker: choose park order | optional | — | — | — | Required order of parks, if any; empty is any order | `updateAdmissionRules` body |
| Same day only `crossover.sameDayOnly` | toggle | optional | on | — | — | — | `updateAdmissionRules` body |
| Different day access `crossover.differentDayAccess` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Day pattern `crossover.dayPattern` | segmented control | optional | Flexible within validity | Consecutive from first scan · Flexible within validity | — | — | `updateAdmissionRules` body |
| Max park entries `crossover.maxParkEntries` | number field | optional | — | min 1 | — | Null is unlimited | `updateAdmissionRules` body |
| Crossover quantity `crossover.crossoverQuantity` | number field | optional | — | min 1 | — | How many crossovers; null is unlimited | `updateAdmissionRules` body |
| Crossover after time `crossover.crossoverAfterTime` | time picker | optional | — | — | HH:mm, 24-hour | Earliest venue-local time HH:MM a crossover is allowed | `updateAdmissionRules` body |
| Prerequisite park org unit `crossover.prerequisiteParkOrgUnitId` | picker: choose a prerequisite park org unit | optional | — | — | shows names, sends the id | The park that must be entered first | `updateAdmissionRules` body |
| Re entry after crossover `crossover.reEntryAfterCrossover` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Allowed access points `allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Empty means any access point in the venue. | `updateAdmissionRules` body |
| Re entry verification `reEntryVerification` | radio group | optional | Credential only | Credential only · Credential uv stamp · Credential face · Credential operator · Custom | — | What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1). | `updateAdmissionRules` body |
| … 2 more | | | | | | the rest are in `schemas.json` | `updateAdmissionRules` body |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save admission rules (primary button) | `updateAdmissionRules` PUT `/admission-rules/{profileId}` | AdmissionRules | AdmissionRules | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before … | — |

**Data it reads**: `listMultiParkCrossover` (onLoad, Multi-Park & Crossover Rules); `listAdmissionRules` (onLoad, The admission profiles that carry crossover rules)

**Where the user goes next**

- → `BO-154` Access Rule Command Center: *Returns to the board's landing screen*; calls `listMultiParkCrossover`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-park crossover rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-park crossover rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-park crossover rules yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the multi-park crossover rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before validity.from |

#### Permissions

- `listMultiParkCrossover` → `SCOPE_VIEW` (read) · staff
- `listAdmissionRules` → `SCOPE_VIEW` (read) · staff
- `updateAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.7 | The system should support multiple validity rules access entitlements associated with a ticket. The available entry rules can be changed without required additional development effort for configuring … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.10 | The system should be able to expire a ticket if it is not used within a specified time (e.g. 20 minutes) from the admission time specified on the ticket or based on the time of the performance/event. … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.59 | Some tickets may be entitled to reentry. | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.70 | The access control rules can support all multi-park requirements, such as but not limited to: -multi-park access on different days, -crossover feature i.e. access to another park on the same day as … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 7.4.22 | For special ticket, it can be restricted to particular group of people and have precondition ex: companion ticket | F&B POS | CONTRACTED | `listAdmissionRules` |
| 7.4.25 | For each PLU, it is possible to manage Usage zone or attraction access control restriction | F&B POS | CONTRACTED | `listAdmissionRules` |
| 3.2.34 | The access rules can be modified even after the ticket has been issued. | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.62 | It must be possible to change the access control organization process on special dates. Venue is organizing on regular basis free view days where the main gate access control doors are opened letting … | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.71 | The access control can support special requirements for special events such as but not limited to: -definition of a specific product that can capture attendance without physical admission, -special … | Admission and Access | CONTRACTED | `updateAdmissionRules` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Validity date range plus blockout dates (e.g. public holidays, special event days); entry allowance consumption blocks use once exhausted; multi-park crossover (how many parks, same-day or one per day, consecutive or flexible days); companion rules (child ticket needs a qualifying adult). *(client request · MoM 2 Sep 2026, 4.3 / 4.4 Validity, Crossover & Companion Rules · DI-628)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-160` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-160`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 12: Works in Multi-Park & Crossover Rules → Configure complex access between multiple parks/venues. The matrix specifically requires multi-park access on different days, same-day crossover, park-specific entry quantities and conditional access …

#### Acceptance for the design

- [ ] Every input above is drawn (47), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-160?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save admission rules.
- [ ] Every transition is wired: `BO-154`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-161` Guest, Companion & Eligibility Rules

**Apply access conditions based on guest characteristics and relationships.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block A · ticket #17866 (APP-SETUP-BO-161) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW` (1 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/access-venue/guest-companion-eligibility-rules-bo-161` |

**Known gaps.** **Seven pack categories are not age categories and are not carried** (decided 28 September, audit R275 (b): the guest categories map onto the age rules). POD, POD Companion, Nanny, VIP, Member, Staff …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Infant | select field | — | — | — | — | Age band infant (under 3). Admitted when the rule's age range includes it (audit R275 (b)). | — |
| Child | select field | — | — | — | — | Age band child (3–12). Admitted when the rule's age range includes it (audit R275 (b)). | — |
| Junior | select field | — | — | — | — | Age band junior (13–17). Admitted when the rule's age range includes it (audit R275 (b)). | — |
| Adult | select field | — | — | — | — | Age band adult (18–59). Admitted when the rule's age range includes it (audit R275 (b)). | — |
| Senior | select field | — | — | — | — | Age band senior (60+). Admitted when the rule's age range includes it (audit R275 (b)). | — |
| Accompanied below age | number field | — | — | — | — | **Child Ticket + Assigned Adult Ticket** from the pack — a guest below this age must be accompanied (`accompaniedBelowAge`) (audit R275 (b)). | — |

**Form: Save age rule** (modal, opened by *Save age rule*; *Save age rule* calls `setProductEligibilityRule`, *Cancel* sends nothing)

**Collects what `setProductEligibilityRule` sends before it is called.** The guest categories are the age bands, so the categories chosen become `minAgeYears` and `maxAgeYears`; `accompaniedBelowAge`, the guardian-signature ages, `waiverRequired`, `swimAbility` and the height limits are optional (decided 28 September, audit R275 (b)). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Min age years `minAgeYears` | number field | optional | — | min 0 | — | — | `setProductEligibilityRule` body |
| Max age years `maxAgeYears` | number field | optional | — | min 0 | — | — | `setProductEligibilityRule` body |
| Min height cm `minHeightCm` | number field | optional | — | min 50; max 250 | — | — | `setProductEligibilityRule` body |
| Max height cm `maxHeightCm` | number field | optional | — | min 50; max 250 | — | — | `setProductEligibilityRule` body |
| Height bands cm `heightBandsCm` | list of values (chips) | optional | 120, 140 | — | — | Band edges the guest chooses between, e.g. under 1.20 m, 1.20–1.40 m, 1.40 m and over. | `setProductEligibilityRule` body |
| Accompanied below age `accompaniedBelowAge` | number field | optional | — | — | — | Under this age an adult must be present, e.g. 8 at the kids club. | `setProductEligibilityRule` body |
| Guardian signature age from `guardianSignatureAgeFrom` | number field | optional | — | — | — | — | `setProductEligibilityRule` body |
| Guardian signature age to `guardianSignatureAgeTo` | number field | optional | — | — | — | Ages needing a guardian's signature, e.g. 12–15 on a thrill ride. | `setProductEligibilityRule` body |
| Waiver required `waiverRequired` | toggle | optional | off | — | — | — | `setProductEligibilityRule` body |
| Swim ability `swimAbility` | segmented control | optional | Not required | Not required · Confident | — | Superseded for the guest's answer (decided 29 September, rev 3 REV3-26): the swim question is a consent, not a data field. | `setProductEligibilityRule` body |
| Refundable if ineligible at gate `refundableIfIneligibleAtGate` | toggle | optional | off | — | — | — | `setProductEligibilityRule` body |
| Required certification code `requiredCertificationCode` | text field | optional | — | max length 60 | — | A certification the participant must hold (decided 29 September, W4; added 30 September), e.g. | `setProductEligibilityRule` body |

Carried, not typed: `productId`

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

#### Outputs: what the screen shows and produces

**Shown**

**The age rule** (detail panel, from `getProductEligibilityRule`): **The guest categories are the age bands** (decided 28 September, audit R275 (b)) — Infant under 3, Child 3–12, Junior 13–17, Adult 18–59, Senior 60+ (`EligibilityDeclaration.ageBand`). A product admits the bands its `minAgeYears`/`maxAgeYears` cover; height stays its own limit.

| Shows | Format | Notes |
|---|---|---|
| Min age years | 1,234 | — |
| Max age years | 1,234 | — |
| Accompanied below age | 1,234 | Under this age an adult must be present, e.g. 8 at the kids club. |
| Guardian signature age from | 1,234 | — |
| Guardian signature age to | 1,234 | Ages needing a guardian's signature, e.g. 12–15 on a thrill ride. |
| Min height cm | 1,234 | — |
| Max height cm | 1,234 | — |
| Height bands cm | list or chips (count when long) | Band edges the guest chooses between, e.g. under 1.20 m, 1.20–1.40 m, 1.40 m and over. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save age rule (primary button) | `setProductEligibilityRule` PUT `/products/{productId}/eligibility-rule` | ProductEligibilityRule | ProductEligibilityRule | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Data it reads**: `getProductEligibilityRule` (onLoad, A product's age, height and supervision limits); `listGuestCompanionEligibility` (onLoad, Guest, Companion & Eligibility Rules)

**Where the user goes next**

- → `BO-154` Access Rule Command Center: *Returns to the board's landing screen*; calls `listGuestCompanionEligibility`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest companion eligibility configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest companion eligibility untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest companion eligibility configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `getProductEligibilityRule` → `PRODUCT_VIEW` (read) · staff, guest
- `setProductEligibilityRule` → `PRODUCT_CONFIGURE` (configure) · staff
- `listGuestCompanionEligibility` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.5.11 | Support configurable restrictions governing transfers, spending limits, age restrictions, membership rules, and entitlement usage. | F&B & Guest Management | CONTRACTED | data `ProductEligibilityRule` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Validity date range plus blockout dates (e.g. public holidays, special event days); entry allowance consumption blocks use once exhausted; multi-park crossover (how many parks, same-day or one per day, consecutive or flexible days); companion rules (child ticket needs a qualifying adult). *(client request · MoM 2 Sep 2026, 4.3 / 4.4 Validity, Crossover & Companion Rules · DI-628)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-161` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-161`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 14: Works in Guest, Companion & Eligibility Rules → Apply access conditions based on guest characteristics and relationships.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-161?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save age rule.
- [ ] Every transition is wired: `BO-154`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-162` Group Admission & Quantity Validation

**Handle B2B groups, school groups, tour groups and family/group tickets efficiently. The matrix specifically calls for faster admission for large B2B groups and the ability for one QR/group ticket to represent multiple admissions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/group-admission-quantity-validation-bo-162` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listGroupAdmissionQuantity` (onLoad, Group Admission & Quantity Validation)

**Where the user goes next**

- → `BO-154` Access Rule Command Center: *Returns to the board's landing screen*; calls `listGroupAdmissionQuantity`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group admission quantity list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group admission quantity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group admission quantity yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group admission quantity are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listGroupAdmissionQuantity` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group ticket QR options: one QR valid for a defined headcount, individual QR per member, or a single rotating/multi-use QR scanned until the headcount is exhausted. *(client request · MoM 31 Aug 2026, 4.8 Group Operations, Payment Links & Check-In · DI-569)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-162` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-162`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 16: Works in Group Admission & Quantity Validation → Handle B2B groups, school groups, tour groups and family/group tickets efficiently. The matrix specifically calls for faster admission for large B2B groups and the ability for one QR/group ticket to …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-162?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-154`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-163` Rule Simulation, Conflict Check & Publication

**No access rule should reach a live gate without being tested.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/rule-simulation-conflict-check-publication-bo-163` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Rule V1.0 (primary button) | navigation or local | — | — | — | — |
| Rule V1.1 (secondary button) | navigation or local | — | — | — | — |
| Rule V2.0 (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rule simulation conflict list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rule simulation conflict untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rule simulation conflict yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rule simulation conflict are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `publishRuleConflictCheck` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Simulation tool validates a rule (e.g. ticket allowed in Zone A and B, not C or D) via a virtual scan before publishing, without a real transaction. *(client request · MoM 2 Sep 2026, 4.5 Rule Simulation Tool · DI-629)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-163` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS19 Access Control Board 2.dc.html#bo-163`
- Workshop pack: Access Control Module_Reference.pdf board 2
- Flow F112 *Access Control board 2: Access Rule Command Center*, step 18: Works in Rule Simulation, Conflict Check & Publication → No access rule should reach a live gate without being tested.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-163?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Rule V1.0, Rule V1.1, Rule V2.0, What publishing changes.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**17 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createAdmissionRules": {"method":"POST","path":"/admission-rules","contract":"access","summary":"Create an admission profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AdmissionRules","responds":"AdmissionRules"},
"deleteJourneySequenceRule": {"method":"DELETE","path":"/journey-sequence-rules/{ruleId}","contract":"access","summary":"Delete a journey sequence rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getProductEligibilityRule": {"method":"GET","path":"/products/{productId}/eligibility-rule","contract":"catalogue","summary":"Who may take part: age, height, supervision","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productId","in":"path","required":true}],"requestBody":null,"responds":"ProductEligibilityRule"},
"listAccessRule": {"method":"GET","path":"/access-rule","contract":"access","summary":"Access Rule Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"park","in":"query","required":false},{"name":"attraction","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"credential","in":"query","required":false},{"name":"ruleType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"date","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAccessValidityTime": {"method":"GET","path":"/access-validity-time","contract":"access","summary":"Access Validity & Time Rules","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessValidityTimeRulesView"},
"listAdmissionRules": {"method":"GET","path":"/admission-rules","contract":"access","summary":"List admission profiles","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAntiPassbackJourney": {"method":"GET","path":"/anti-passback-journey","contract":"access","summary":"Anti-Passback & Journey Sequence","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AntiPassbackJourneySequenceView"},
"listEntitlementConsumption": {"method":"GET","path":"/entitlement-consumption","contract":"access","summary":"Entitlement Consumption Engine","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"EntitlementConsumptionEngineView"},
"listEntryExitRule": {"method":"GET","path":"/entry-exit-rule","contract":"access","summary":"Entry, Exit & Re-entry Rules","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"EntryExitReEntryRulesView"},
"listGroupAdmissionQuantity": {"method":"GET","path":"/group-admission-quantity","contract":"access","summary":"Group Admission & Quantity Validation","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GroupAdmissionQuantityValidationView"},
"listGuestCompanionEligibility": {"method":"GET","path":"/guest-companion-eligibility","contract":"access","summary":"Guest, Companion & Eligibility Rules","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestCompanionEligibilityRulesView"},
"listMultiParkCrossover": {"method":"GET","path":"/multi-park-crossover","contract":"access","summary":"Multi-Park & Crossover Rules","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MultiParkCrossoverRulesView"},
"publishRuleConflictCheck": {"method":"PUT","path":"/rule-conflict-check","contract":"access","summary":"Rule Simulation, Conflict Check & Publication","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RuleSimulationConflictCheckPublicationInput","responds":"RuleSimulationConflictCheckPublicationView"},
"setEntitlementConsumption": {"method":"PUT","path":"/entitlement-consumption","contract":"access","summary":"Save an entitlement consumption rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"EntitlementConsumptionEngineInput","responds":"EntitlementConsumptionEngineView"},
"setJourneySequenceRule": {"method":"PUT","path":"/journey-sequence-rules","contract":"access","summary":"Create or replace an anti-passback / journey sequence rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessJourneySequenceRule","responds":"AccessJourneySequenceRule"},
"setProductEligibilityRule": {"method":"PUT","path":"/products/{productId}/eligibility-rule","contract":"catalogue","summary":"Set age, height and supervision limits","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"productId","in":"path","required":true}],"requestBody":"ProductEligibilityRule","responds":"ProductEligibilityRule"},
"setVisualAccessRule": {"method":"PUT","path":"/visual-access-rule","contract":"access","summary":"Visual Access Rule Builder","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisualAccessRuleBuilderInput","responds":"VisualAccessRuleBuilderView"},
"updateAdmissionRules": {"method":"PUT","path":"/admission-rules/{profileId}","contract":"access","summary":"Update an admission profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AdmissionRules","responds":"AdmissionRules"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessJourneySequenceRule": {"type":"object","x-ticvai-persistence":"access.journey_sequence_rule","description":"One anti-passback / journey sequence rule - the level it applies at, the time window, the required order of scans and what a violation leads to (declared 29 September, data-model close-out DM1).","required":["id","scopePath","scope"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"name":{"type":"string","maxLength":200,"nullable":true},"scope":{"type":"string","enum":["credential","guest","gate","attraction","park","venue"],"description":"Level the anti-passback check applies at"},"windowMinutes":{"type":"integer","minimum":0,"nullable":true},"requiredSequence":{"type":"array","items":{"type":"string"},"description":"Ordered steps, e.g. entry, exit, reEntry"},"violationResponses":{"type":"array","items":{"type":"string","enum":["deny","warning","referToOperator","requireSupervisor","allowOverride","triggerSecurityAlert"]}},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessRuleCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Rule Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"ruleName":{"type":"string","description":"Rule, e.g. Standard Park Entry"},"appliesTo":{"type":"string","description":"Products or credentials the rule applies to"},"location":{"type":"string","description":"Where the rule applies"},"validity":{"type":"string","description":"When the rule applies"},"ruleType":{"type":"string"},"status":{"type":"string","enum":["draft","pendingApproval","scheduled","active","inactive"]}}},
"AccessRuleCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"activeAccessRules":{"type":"integer","description":"Active Access Rules"},"draftRules":{"type":"integer","description":"Draft Rules"},"scheduledRules":{"type":"integer","description":"Scheduled Rules"},"rulesPendingApproval":{"type":"integer","description":"Rules Pending Approval"},"venuesCovered":{"type":"integer","description":"Venues Covered"},"productsTicketsCovered":{"type":"integer","description":"Products/Tickets Covered"},"rulesWithConflicts":{"type":"integer","description":"Rules with Conflicts"},"rulesUsingBiometrics":{"type":"integer","description":"Rules Using Biometrics"},"rulesAllowingOverride":{"type":"integer","description":"Rules Allowing Override"},"offlineCompatibleRules":{"type":"integer","description":"Offline-Compatible Rules"},"recentlyModifiedRules":{"type":"integer","description":"Recently Modified Rules"},"upcomingRuleChanges":{"type":"integer","description":"Upcoming Rule Changes"}}},
"AccessValidityTimeRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Validity & Time Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"validityBasis":{"type":"string","enum":["fixedRange","daysAfterSale","daysAfterActivation","daysAfterFirstUse","endOfDay","endOfWeek","endOfMonth","endOfYear"]},"dayTypes":{"type":"array","items":{"type":"string","enum":["weekdays","weekends","peakDates","offPeakDates","holidays","seasons","eventDates"]},"description":"Calendar day types on which access is allowed"},"blackoutDates":{"type":"array","items":{"type":"string"},"description":"ISO dates on which access is refused"},"name":{"type":"string"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"validityDays":{"type":"integer","description":"N for the relative bases"},"timeWindowStart":{"type":"string","description":"Local time HH:MM, e.g. 09:00"},"timeWindowEnd":{"type":"string","description":"Local time HH:MM, e.g. 13:00"},"admissionToleranceMinutes":{"type":"integer"},"gracePeriodMinutes":{"type":"integer"},"noShowExpiryMinutes":{"type":"integer","description":"Credential expires this long after its admission/performance time if unused"}},"required":["ruleId","validityBasis"]},
"AdmissionRules": {"x-ticvai-persistence":"access.admission_rules","type":"object","required":["id","code","name","openMinutesBefore","closeMinutesAfter"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Server-assigned.** Ignored in a `createAdmissionRules` or `updateAdmissionRules` body; on update the profile is the one the path names.\n"},"code":{"type":"string","maxLength":64},"perProductRules":{"allOf":[{"$ref":"#/components/schemas/PerProductRuleList"}],"description":"BL-059. **Transaction rules were per profile and a ticket type could not state its own.** An annual pass allowing one entry per day and a single ticket allowing one entry ever are different rules, and forcing a profile per product multiplies profiles instead.\n"},"name":{"type":"string","maxLength":200},"openMinutesBefore":{"type":"integer","description":"How long before a performance validation opens."},"closeMinutesAfter":{"type":"integer"},"maxDurationMinutes":{"type":"integer","nullable":true},"requiresExitBeforeReentry":{"type":"boolean","default":false},"maxReentries":{"type":"integer","nullable":true},"entryLimit":{"type":"object","description":"**How many times the credential may enter** (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). Absent means `unlimited`.","required":["mode"],"properties":{"mode":{"type":"string","enum":["unlimited","once","nTimes","nPerDay","nPerPeriod"],"default":"unlimited"},"count":{"type":"integer","minimum":1,"description":"N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it)"},"periodDays":{"type":"integer","minimum":1,"description":"The period for nPerPeriod"}}},"exitScan":{"type":"string","enum":["required","optional","none"],"default":"optional","description":"(decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. `optional`: exits run in free rotation and headcount is inferred. `none`: the exit has no reader."},"maxExits":{"type":"integer","minimum":0,"nullable":true,"description":"Null is unlimited (decided 29 September, VM close-out)"},"reEntryWindowMinutes":{"type":"integer","minimum":1,"nullable":true,"description":"Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out)"},"sameDayOnly":{"type":"boolean","default":true,"description":"Re-entry only on the day of the exit (decided 29 September, VM close-out)"},"designatedAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out)"},"validity":{"type":"object","description":"**When the credential is valid** (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). The admission window above still applies inside it.","required":["anchor"],"properties":{"anchor":{"type":"string","enum":["fixedRange","afterSale","afterActivation","afterFirstUse"],"description":"fixedRange uses from and to; the others count days from the event"},"days":{"type":"integer","minimum":1,"description":"N days after the anchor; required unless the anchor is fixedRange"},"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date","description":"Inclusive. Must not be before from (`422`)"},"endOf":{"type":"string","enum":["day","week","month","year"],"nullable":true,"description":"Validity runs to the end of the day, week, month or year the relative period ends in"},"daysOfWeek":{"type":"array","items":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"description":"Empty is every day"},"dayTypes":{"type":"array","items":{"type":"string","enum":["peakDates","offPeakDates","holidays","seasons","eventDates"]},"description":"Calendar day types on which access is allowed; empty is every day type"},"blackoutDates":{"type":"array","items":{"type":"string","format":"date"},"description":"Dates on which access is refused whatever else allows it"}}},"crossover":{"type":"object","nullable":true,"description":"**Crossover between parks** (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. Null means the profile admits to one park only.","required":["allowedParkOrgUnitIds"],"properties":{"allowedParkOrgUnitIds":{"type":"array","minItems":2,"items":{"type":"string","format":"uuid"}},"parkOrder":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Required order of parks, if any; empty is any order"},"sameDayOnly":{"type":"boolean","default":true},"differentDayAccess":{"type":"boolean","default":false},"dayPattern":{"type":"string","enum":["consecutiveFromFirstScan","flexibleWithinValidity"],"default":"flexibleWithinValidity"},"maxParkEntries":{"type":"integer","minimum":1,"nullable":true,"description":"Null is unlimited"},"crossoverQuantity":{"type":"integer","minimum":1,"nullable":true,"description":"How many crossovers; null is unlimited"},"crossoverAfterTime":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Earliest venue-local time HH:MM a crossover is allowed"},"prerequisiteParkOrgUnitId":{"type":"string","format":"uuid","nullable":true,"description":"The park that must be entered first"},"reEntryAfterCrossover":{"type":"boolean","default":false}}},"allowedAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Empty means any access point in the venue."},"reEntryVerification":{"type":"string","enum":["credentialOnly","credentialUvStamp","credentialFace","credentialOperator","custom"],"default":"credentialOnly","description":"What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1)."},"ruleConditions":{"type":"object","nullable":true,"description":"The visual rule builder body `setVisualAccessRule` writes: `appliesTo` (products or credential types), `conditions`, `logic` (AND / OR / NOT over the conditions), `decision` (allow, deny, referToOperator, overrideEligible) and `consequences`. **One `jsonb` column on the rule row**, read with the rule and never queried on its own; the locations stay in `access.entry_rule_point` (added 29 September, data-model close-out DM1)."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"AntiPassbackJourneySequenceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Anti-Passback & Journey Sequence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"scope":{"type":"string","enum":["credential","guest","gate","attraction","park","venue"],"description":"Level the anti-passback check applies at"},"name":{"type":"string"},"windowMinutes":{"type":"integer","description":"Anti-passback time window"},"requiredSequence":{"type":"array","items":{"type":"string"},"description":"Ordered steps, e.g. entry, exit, reEntry"},"violationResponses":{"type":"array","items":{"type":"string"},"description":"Any of deny, warning, referToOperator, requireSupervisor, allowOverride, triggerSecurityAlert"}},"required":["ruleId","scope"]},
"EntitlementConsumptionEngineInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Entitlement Consumption Engine submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.","required":["name","entitlementType"],"properties":{"ruleId":{"type":"string","format":"uuid","description":"Absent creates a rule"},"name":{"type":"string","maxLength":200},"credentialType":{"type":"string","description":"Credential or product type the rule applies to"},"entitlementType":{"type":"string","enum":["parkAdmission","attractionAdmission","ride","fastPass","meal","voucher","photo","locker","event","experience","reEntry","membershipBenefit","custom"]},"consumptionOrder":{"type":"integer","minimum":1,"default":1,"description":"Where one scan could consume several entitlements, lower is consumed first"},"consumptionPerValidation":{"type":"integer","minimum":1,"default":1,"description":"Units one scan consumes"},"quantity":{"type":"integer","minimum":1,"description":"Units the entitlement carries; ignored when unlimited"},"unlimited":{"type":"boolean","default":false},"onePerAttraction":{"type":"boolean","default":false},"attractionIds":{"type":"array","items":{"type":"string"},"description":"Empty means every attraction the entitlement covers"}}},
"EntitlementConsumptionEngineView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Entitlement Consumption Engine displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"credentialType":{"type":"string","description":"Credential or product type the rule applies to (decided 29 September, VM close-out)"},"consumptionOrder":{"type":"integer","minimum":1,"description":"Where one scan could consume several entitlements, lower is consumed first (decided 29 September, VM close-out)"},"ruleId":{"type":"string"},"entitlementType":{"type":"string","enum":["parkAdmission","attractionAdmission","ride","fastPass","meal","voucher","photo","locker","event","experience","reEntry","membershipBenefit","custom"]},"quantity":{"type":"integer","description":"Quantity (the pack shows 3)"},"consumptionPerValidation":{"type":"integer","description":"Consumption per validation (the pack shows 1)"},"name":{"type":"string"},"unlimited":{"type":"boolean","description":"No quantity limit, e.g. Gold Fast Pass"},"attractionIds":{"type":"array","items":{"type":"string"},"description":"Attractions where it may be consumed"},"onePerAttraction":{"type":"boolean","description":"At most one use per attraction"}},"required":["ruleId","entitlementType"]},
"EntryExitReEntryRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Entry, Exit & Re-entry Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"entryMode":{"type":"string","enum":["unlimited","once","nTimes","nPerDay","nPerPeriod"]},"exitScan":{"type":"string","enum":["required","optional"],"description":"Optional means exits run in free rotation and headcount is inferred"},"exitMode":{"type":"string","enum":["unlimited","limited"]},"reEntryAllowed":{"type":"boolean","description":"Allowed / Not Allowed"},"maximumReEntries":{"type":"integer","description":"Maximum re-entries"},"sameDayOnly":{"type":"boolean","description":"Same-day only"},"designatedGateRequired":{"type":"boolean","description":"Designated gate required"},"exitRequiredFirst":{"type":"boolean","description":"Exit required first"},"reEntryWindow":{"type":"integer","description":"Minutes after exit within which re-entry is allowed"},"name":{"type":"string"},"appliesTo":{"type":"array","items":{"type":"string"},"description":"Tickets, products or access policies the rule governs"},"entryLimit":{"type":"integer","description":"N for nTimes, nPerDay, nPerPeriod"},"entryPeriod":{"type":"string","description":"ISO 8601 duration for nPerPeriod"},"exitLimit":{"type":"integer"}},"required":["ruleId","entryMode"]},
"GroupAdmissionQuantityValidationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Group Admission & Quantity Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"allowedGroupModes":{"type":"array","items":{"type":"string","enum":["entireGroup","partialGroup","multipleWaves","leaderGuests","singleQrMultiEntry","individualChildTicketsUnderGroup","prevalidatedB2bManifest"]}},"name":{"type":"string"},"productIds":{"type":"array","items":{"type":"string"},"description":"Group products the rule covers"},"maxGroupSize":{"type":"integer"}},"required":["ruleId","allowedGroupModes"]},
"GuestCompanionEligibilityRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Guest, Companion & Eligibility Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"guestCategory":{"type":"string","enum":["adult","child","junior","senior","pod","podCompanion","nanny","vip","member","staff","accreditation","customerSegment"]},"name":{"type":"string"},"requiredCompanionCategory":{"type":"string","description":"Category of the qualifying companion, e.g. adult"},"companionVerification":{"type":"string","enum":["linkedTicket","companionBiometric"]},"verifyAt":{"type":"array","items":{"type":"string","enum":["admission","exit","attraction"]},"description":"Where the companion is checked (decided 29 September, VM close-out)"},"attractionIds":{"type":"array","items":{"type":"string"}}},"required":["ruleId","guestCategory"]},
"MultiParkCrossoverRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Multi-Park & Crossover Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string"},"allowedParks":{"type":"array","items":{"type":"string"},"description":"allowed parks"},"parkOrder":{"type":"array","items":{"type":"string"},"description":"Required park order, if any"},"sameDayCrossover":{"type":"boolean","description":"same-day crossover"},"differentDayAccess":{"type":"boolean","description":"different-day access"},"numberOfParkEntries":{"type":"integer","description":"number of park entries"},"crossoverQuantity":{"type":"integer","description":"crossover quantity"},"crossoverTime":{"type":"string","description":"Earliest local time HH:MM a crossover is allowed"},"prerequisitePark":{"type":"string","description":"prerequisite park"},"reEntryAfterCrossover":{"type":"boolean","description":"re-entry after crossover"},"name":{"type":"string"},"dayPattern":{"type":"string","enum":["consecutiveFromFirstScan","flexibleWithinValidity"]}},"required":["ruleId","allowedParks"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PerProductRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the profile row** (`access.admission_rules.per_product_rules`). The rules are read with the profile and a rule is never queried on its own, so a child table would add a join for nothing.\n","items":{"type":"object","properties":{"productId":{"type":"string","format":"uuid"},"entriesPerDay":{"type":"integer","nullable":true},"minimumGapMinutes":{"type":"integer","nullable":true,"description":"**Anti-passback in minutes rather than a boolean.** A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back over a fence.\n"},"allowedAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"biometricPolicy":{"allOf":[{"$ref":"#/components/schemas/BiometricPolicy"}],"description":"BL-105, 3.2.9. **The biometric check is a property of the product, not of the venue** — memberships checked, day tickets not. It sits here rather than on the profile because `perProductRules` is already where a ticket type states its own terms, and a profile per product would multiply profiles to carry one flag.\n**Absent means `disabled`**, and `disabled` is the answer for every product until somebody chooses otherwise. **Inert while `VenueSettings.biometrics.isEnabled` is false**, so a rules profile copied to another venue cannot begin capturing faces there.\n"},"maxPassesPerBiometricIdentity":{"type":"integer","nullable":true,"minimum":1,"description":"BL-096, 2.14.7. **The annual-pass quota, keyed to biometric identity.** `enrolFacePass` already answers 409 where a face is on another annual pass; the constant behind that refusal was one and was invisible. **Null means unlimited** and is the answer for every product that is not an annual pass — a quota applied where nobody asked for one turns a family sharing a day ticket into a fraud alert.\n"}}}},
"ProductEligibilityRule": {"type":"object","x-ticvai-persistence":"catalogue.product_eligibility_rule","description":"Participation limits for one product. Absent means anyone may take part, and `getProductEligibilityRule` returns that absence as this schema with every limit null, never as a `404`.","properties":{"id":{"type":"string","format":"uuid","readOnly":true},"productId":{"type":"string","readOnly":true},"minAgeYears":{"type":"integer","minimum":0,"nullable":true},"maxAgeYears":{"type":"integer","minimum":0,"nullable":true},"minHeightCm":{"type":"integer","minimum":50,"maximum":250,"nullable":true},"maxHeightCm":{"type":"integer","minimum":50,"maximum":250,"nullable":true},"heightBandsCm":{"type":"array","items":{"type":"integer"},"default":[120,140],"description":"Band edges the guest chooses between, e.g. under 1.20 m, 1.20–1.40 m, 1.40 m and over."},"accompaniedBelowAge":{"type":"integer","nullable":true,"description":"Under this age an adult must be present, e.g. 8 at the kids club."},"guardianSignatureAgeFrom":{"type":"integer","nullable":true},"guardianSignatureAgeTo":{"type":"integer","nullable":true,"description":"Ages needing a guardian's signature, e.g. 12–15 on a thrill ride."},"waiverRequired":{"type":"boolean","default":false},"swimAbility":{"type":"string","enum":["notRequired","confident"],"default":"notRequired","deprecated":true,"description":"**Superseded for the guest's answer** (decided 29 September, rev 3 REV3-26): the swim question is a consent, not a data field. A venue attaches *Are you able to swim?* as a consent question (`Product.consentQuestionIds`), with its own text, version and whether it is asked per person or once per booking, and the answer is a consent record. Kept so existing rules read; a new product should use a consent question instead.\n"},"refundableIfIneligibleAtGate":{"type":"boolean","default":false},"requiredCertificationCode":{"type":"string","nullable":true,"maxLength":60,"description":"**A certification the participant must hold** (decided 29 September, W4; added 30 September), e.g. `padiOpenWater` for a dive. Null means none. Help me choose reads it: an answer whose `filter.certificationCode` names it with `holdsCertification: false` leaves the product out, and with `holdsCertification: true` (or no flag) keeps only products needing that certification or none. Proof, where the venue asks for it, is a consent question on the product (REV3-26), not this field."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"RuleSimulationConflictCheckPublicationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Rule Simulation, Conflict Check & Publication submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"step":{"type":"string","enum":["simulate","validate","schedule","publish","rollBack"]},"ruleVersionId":{"type":"string","description":"Rule version being simulated or published"},"credentialId":{"type":"string","description":"Credential used for the virtual scan"},"accessPointId":{"type":"string"},"simulatedAt":{"type":"string","format":"date-time"},"previousJourney":{"type":"array","items":{"type":"string"},"description":"Prior scans assumed for the simulation"},"decision":{"type":"string","enum":["allow","deny","referToOperator","overrideEligible"]},"decisionTrace":{"type":"array","items":{"type":"string"},"description":"Each condition checked and whether it passed"},"failedRuleId":{"type":"string"},"conflicts":{"type":"array","items":{"type":"string"},"description":"Conflicts found (advisory)"},"scheduledAt":{"type":"string","format":"date-time"}},"required":["ruleVersionId","step"]},
"RuleSimulationConflictCheckPublicationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Rule Simulation, Conflict Check & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"step":{"type":"string","enum":["simulate","validate","schedule","publish","rollBack"]},"ruleVersionId":{"type":"string","description":"Rule version being simulated or published"},"credentialId":{"type":"string","description":"Credential used for the virtual scan"},"accessPointId":{"type":"string"},"simulatedAt":{"type":"string","format":"date-time"},"previousJourney":{"type":"array","items":{"type":"string"},"description":"Prior scans assumed for the simulation"},"decision":{"type":"string","enum":["allow","deny","referToOperator","overrideEligible"]},"decisionTrace":{"type":"array","items":{"type":"string"},"description":"Each condition checked and whether it passed"},"failedRuleId":{"type":"string"},"conflicts":{"type":"array","items":{"type":"string"},"description":"Conflicts found (advisory)"},"scheduledAt":{"type":"string","format":"date-time"}},"required":["ruleVersionId","step"]},
"VisualAccessRuleBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Visual Access Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"decision":{"type":"string","enum":["allow","deny","referToOperator","overrideEligible"],"description":"THEN"},"name":{"type":"string"},"ruleId":{"type":"string"},"logic":{"type":"string","description":"Boolean expression combining the conditions with AND / OR / NOT"},"appliesTo":{"type":"array","items":{"type":"string"},"description":"Products or credential types (WHEN)"},"locationIds":{"type":"array","items":{"type":"string"},"description":"Venue, park, zone, attraction or gate IDs (AT)"},"conditions":{"type":"array","items":{"type":"string"},"description":"Conditions (IF), e.g. visitDate = today, remainingEntries > 0"},"consequences":{"type":"array","items":{"type":"string"},"description":"Actions performed on the decision, e.g. consumeEntry, incrementAttendance"}},"required":["ruleId","name","decision"]},
"VisualAccessRuleBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Visual Access Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"decision":{"type":"string","enum":["allow","deny","referToOperator","overrideEligible"],"description":"THEN"},"name":{"type":"string"},"ruleId":{"type":"string"},"logic":{"type":"string","description":"Boolean expression combining the conditions with AND / OR / NOT"},"appliesTo":{"type":"array","items":{"type":"string"},"description":"Products or credential types (WHEN)"},"locationIds":{"type":"array","items":{"type":"string"},"description":"Venue, park, zone, attraction or gate IDs (AT)"},"conditions":{"type":"array","items":{"type":"string"},"description":"Conditions (IF), e.g. visitDate = today, remainingEntries > 0"},"consequences":{"type":"array","items":{"type":"string"},"description":"Actions performed on the decision, e.g. consumeEntry, incrementAttendance"}},"required":["ruleId","name","decision"]}
}
```
