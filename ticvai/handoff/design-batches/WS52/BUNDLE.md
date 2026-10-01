# WS52 — Promotions   Bundles Management board 8

**10 screens · 11 operations · 13 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `PRICE_CONFIGURE, PRICE_VIEW`. A control nobody can use must say so,
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
| `ADM-208` | Stacking & Conflict Command Center | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-209` | Promotion Priority & Hierarchy Manager | B–D | 0 | 0 | 6 | 0 | 0 | 2 | — | notStarted (generated) |
| `ADM-210` | Promotion Stacking Rule Builder | B–D | 0 | 0 | 6 | 0 | 0 | 2 | — | notStarted (generated) |
| `ADM-211` | Promotion Exclusion & Compatibility Matrix | B–D | 0 | 16 | 6 | 0 | 0 | 2 | — | notStarted (generated) |
| `ADM-212` | Discount Calculation & Application Sequence | B–D | 6 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-213` | Best Offer & Customer Benefit Resolver | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-214` | Discount Cap & Maximum Benefit Controller | B–D | 9 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-215` | Conflict Detection & Resolution Center | B–D | 0 | 2 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-216` | Promotion Decision Trace & Transaction Explainer | B–D | 0 | 0 | 6 | 0 | 0 | 2 | — | notStarted (generated) |
| `ADM-217` | Conflict Simulation & AI Optimization | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-209, ADM-210, ADM-211, ADM-213, ADM-216, ADM-217 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-208` Stacking & Conflict Command Center

**Provide centralized operational visibility into promotion interactions across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/stacking-conflict-command-center-adm-208` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Promotion Rules** (metric tile)

**Stackable Promotions** (metric tile)

**Exclusive Promotions** (metric tile)

**Priority Rules** (metric tile)

**Conflicts Detected** (metric tile)

**Critical Conflicts** (metric tile)

**Auto-Resolved Conflicts** (metric tile)

**Transactions with Multiple Offers** (metric tile)

**Average Promotions per Transaction** (metric tile)

**Discount Exposure** (metric tile)

**Prevented Over-Discount** (metric tile)

**Revenue Protected** (metric tile)

**Data it reads**: `listStackingConflict` (onLoad, Stacking & Conflict Command Center)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-209` Promotion Priority & Hierarchy Manager: *Works in Promotion Priority & Hierarchy Manager*; calls `listStackingConflict`
- → `ADM-210` Promotion Stacking Rule Builder: *Works in Promotion Stacking Rule Builder*; calls `listStackingConflict`
- → `ADM-211` Promotion Exclusion & Compatibility Matrix: *Works in Promotion Exclusion & Compatibility Matrix*; calls `listStackingConflict`
- → `ADM-212` Discount Calculation & Application Sequence: *Works in Discount Calculation & Application Sequence*; calls `listStackingConflict`
- → `ADM-213` Best Offer & Customer Benefit Resolver: *Works in Best Offer & Customer Benefit Resolver*; calls `listStackingConflict`
- → `ADM-214` Discount Cap & Maximum Benefit Controller: *Works in Discount Cap & Maximum Benefit Controller*; calls `listStackingConflict`
- → `ADM-215` Conflict Detection & Resolution Center: *Works in Conflict Detection & Resolution Center*; calls `listStackingConflict`
- → `ADM-216` Promotion Decision Trace & Transaction Explainer: *Works in Promotion Decision Trace & Transaction Explainer*; calls `listStackingConflict`
- → `ADM-217` Conflict Simulation & AI Optimization: *Works in Conflict Simulation & AI Optimization*; calls `listStackingConflict`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The stacking conflict list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the stacking conflict untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No stacking conflict yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the stacking conflict are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listStackingConflict` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-208` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS113 Promotions   Bundles Management Board 8.dc.html#adm-208`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 8
- Flow F161 *Promotions Bundles Management board 8: Stacking & Conflict Command Center*, step 1: Opens Stacking & Conflict Command Center → Provide centralized operational visibility into promotion interactions across TICVAI.
- Flow F161 *Promotions Bundles Management board 8: Stacking & Conflict Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F161 *Promotions Bundles Management board 8: Stacking & Conflict Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F161 *Promotions Bundles Management board 8: Stacking & Conflict Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F161 *Promotions Bundles Management board 8: Stacking & Conflict Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F161 *Promotions Bundles Management board 8: Stacking & Conflict Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F161 *Promotions Bundles Management board 8: Stacking & Conflict Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F161 *Promotions Bundles Management board 8: Stacking & Conflict Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F161 branch at step 1 (expected): when Nothing has been set up on Stacking & Conflict Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F161 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-208?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-209`, `ADM-210`, `ADM-211`, `ADM-212`, `ADM-213`, `ADM-214`, `ADM-215`, `ADM-216`, `ADM-217`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-209` Promotion Priority & Hierarchy Manager

**Define the relative priority of different promotion families and individual offers.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/promotion-priority-hierarchy-manager-adm-209` |

**Known gaps.** **Promotion Priority & Hierarchy Manager declares no operation that writes anything** — its only declared call is `listPromotionPriorityHierarchy`, a read. The name promises authoring and the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listPromotionPriorityHierarchy` (onLoad, Promotion Priority & Hierarchy Manager)

**Where the user goes next**

- → `ADM-208` Stacking & Conflict Command Center: *Returns to the board's landing screen*; calls `listPromotionPriorityHierarchy`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The promotion priority hierarchy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the promotion priority hierarchy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No promotion priority hierarchy yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the promotion priority hierarchy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPromotionPriorityHierarchy` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-209` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS113 Promotions   Bundles Management Board 8.dc.html#adm-209`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 8
- Flow F161 *Promotions Bundles Management board 8: Stacking & Conflict Command Center*, step 2: Works in Promotion Priority & Hierarchy Manager → Define the relative priority of different promotion families and individual offers.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-209?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-208`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-210` Promotion Stacking Rule Builder

**Define which promotions can be combined.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/promotion-stacking-rule-builder-adm-210` |

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

- → `ADM-208` Stacking & Conflict Command Center: *Returns to the board's landing screen*; calls `setPromotionStackingRule`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The promotion stacking rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the promotion stacking rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No promotion stacking rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the promotion stacking rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setPromotionStackingRule` → `PRICE_CONFIGURE` (configure) · staff
- `setPromotionRule` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-210` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS113 Promotions   Bundles Management Board 8.dc.html#adm-210`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 8
- Flow F161 *Promotions Bundles Management board 8: Stacking & Conflict Command Center*, step 4: Works in Promotion Stacking Rule Builder → Define which promotions can be combined.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-210?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `ADM-208`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-211` Promotion Exclusion & Compatibility Matrix

**Provide administrators with a visual matrix showing which promotion categories can interact.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Clicking a relationship should show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/promotion-exclusion-compatibility-matrix-adm-211` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every promotion exclusion compatibility** (data table, from `listPromotionExclusionCompatibility`)

| Shows | Format | Notes |
|---|---|---|
| Applicable products | 1,234 | Applicable products |
| Applicable venues | 1,234 | Applicable venues |
| Channels | 1,234 | Channels |
| Customer segments | 1,234 | Customer segments |
| Rule | text | Rule |
| Priority | text | Priority |
| Effective dates | 1,234 | Effective dates |
| Exceptions | 1,234 | Exceptions |

**The selected promotion exclusion compatibility** (detail panel): The pack groups this record's detail under its own headings: “Coupo Members Loyal Ban BOG”, “Membershi”, “Use”, “Conflict Detection”.

| Shows | Format | Notes |
|---|---|---|
| Applicable products | 1,234 | Applicable products |
| Applicable venues | 1,234 | Applicable venues |
| Channels | 1,234 | Channels |
| Customer segments | 1,234 | Customer segments |
| Rule | text | Rule |
| Priority | text | Priority |
| Effective dates | 1,234 | Effective dates |
| Exceptions | 1,234 | Exceptions |

**Data it reads**: `listPromotionExclusionCompatibility` (onLoad, Promotion Exclusion & Compatibility Matrix)

**Where the user goes next**

- → `ADM-208` Stacking & Conflict Command Center: *Returns to the board's landing screen*; calls `listPromotionExclusionCompatibility`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The promotion exclusion compatibility list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the promotion exclusion compatibility untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No promotion exclusion compatibility yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the promotion exclusion compatibility are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPromotionExclusionCompatibility` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-211` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS113 Promotions   Bundles Management Board 8.dc.html#adm-211`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 8
- Flow F161 *Promotions Bundles Management board 8: Stacking & Conflict Command Center*, step 6: Works in Promotion Exclusion & Compatibility Matrix → Provide administrators with a visual matrix showing which promotion categories can interact.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-211?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-208`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-212` Discount Calculation & Application Sequence

**Control the mathematical order in which multiple permitted benefits are calculated.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure whether promotion applies) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/discount-calculation-application-sequence-adm-212` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Before tax | select field | — | — | — | — | — | — |
| After tax | select field | — | — | — | — | — | — |
| Before fee | select field | — | — | — | — | — | — |
| After fee | select field | — | — | — | — | — | — |
| Product only | select field | — | — | — | — | — | — |
| Transaction total | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listDiscountCalculationApplication` (onLoad, Discount Calculation & Application Sequence)

**Where the user goes next**

- → `ADM-208` Stacking & Conflict Command Center: *Returns to the board's landing screen*; calls `listDiscountCalculationApplication`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The discount calculation application configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the discount calculation application untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No discount calculation application configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listDiscountCalculationApplication` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-212` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS113 Promotions   Bundles Management Board 8.dc.html#adm-212`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 8
- Flow F161 *Promotions Bundles Management board 8: Stacking & Conflict Command Center*, step 8: Works in Discount Calculation & Application Sequence → Control the mathematical order in which multiple permitted benefits are calculated.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-212?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-208`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-213` Best Offer & Customer Benefit Resolver

**Determine which promotion or combination gives the guest the correct/best permitted commercial outcome.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/best-offer-customer-benefit-resolver-adm-213` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listBestOfferCustomer` (onLoad, Best Offer & Customer Benefit Resolver)

**Where the user goes next**

- → `ADM-208` Stacking & Conflict Command Center: *Returns to the board's landing screen*; calls `listBestOfferCustomer`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The best offer customer list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the best offer customer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No best offer customer yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the best offer customer are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listBestOfferCustomer` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-213` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS113 Promotions   Bundles Management Board 8.dc.html#adm-213`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 8
- Flow F161 *Promotions Bundles Management board 8: Stacking & Conflict Command Center*, step 10: Works in Best Offer & Customer Benefit Resolver → Determine which promotion or combination gives the guest the correct/best permitted commercial outcome.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-213?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-208`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-214` Discount Cap & Maximum Benefit Controller

**Prevent stacked promotions from exceeding financial or contractual limits.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Configured maximum) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/discount-cap-maximum-benefit-controller-adm-214` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Maximum total discount % | text field | — | — | — | — | — | — |
| Maximum total discount amount | text field | — | — | — | — | — | — |
| Minimum transaction value | select field | — | — | — | — | — | — |
| Minimum product price | select field | — | — | — | — | — | — |
| Minimum margin | select field | — | — | — | — | — | — |
| Maximum free-item value | select field | — | — | — | — | — | — |
| Maximum promotional benefit | select field | — | — | — | — | — | — |
| Maximum promotions per basket | text field | — | — | — | — | — | — |
| 30% | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listDiscountCapMaximum` (onLoad, Discount Cap & Maximum Benefit Controller)

**Where the user goes next**

- → `ADM-208` Stacking & Conflict Command Center: *Returns to the board's landing screen*; calls `listDiscountCapMaximum`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The discount cap maximum configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the discount cap maximum untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No discount cap maximum configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listDiscountCapMaximum` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-214` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS113 Promotions   Bundles Management Board 8.dc.html#adm-214`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 8
- Flow F161 *Promotions Bundles Management board 8: Stacking & Conflict Command Center*, step 12: Works in Discount Cap & Maximum Benefit Controller → Prevent stacked promotions from exceeding financial or contractual limits.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-214?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-208`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-215` Conflict Detection & Resolution Center

**Detect promotion conflicts during both configuration and runtime.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Detect) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/conflict-detection-resolution-center-adm-215` |

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Best price, Reject transaction where necessary. Each needs an operation, or needs removing from the screen …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every conflict detection resolution** (data table, from `listConflictDetectionResolution`)

| Shows | Format | Notes |
|---|---|---|
| Conflict type | chip: Same product, Same audience, Same channel, Same validity, Incompatible promotions … | Conflict detected. |

**The selected conflict detection resolution** (detail panel): The pack groups this record's detail under its own headings: “Customer qualifies for”, “Eligibility”, “Compatibility”, “Priority”, “Calculation sequence”, “Discount cap”.

| Shows | Format | Notes |
|---|---|---|
| Conflict type | chip: Same product, Same audience, Same channel, Same validity, Incompatible promotions … | Conflict detected. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Best price (primary button) | navigation or local | — | — | — | — |
| Reject transaction where necessary (destructive button) | navigation or local | — | — | — | — |

**Data it reads**: `listConflictDetectionResolution` (onLoad, Conflict Detection & Resolution Center)

**Where the user goes next**

- → `ADM-208` Stacking & Conflict Command Center: *Returns to the board's landing screen*; calls `listConflictDetectionResolution`

**What opens over it**

- confirmDialog *Reject transaction where necessary*: **Reject transaction where necessary on a conflict detection resolution is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The conflict detection resolution list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the conflict detection resolution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No conflict detection resolution yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the conflict detection resolution are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listConflictDetectionResolution` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-215` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS113 Promotions   Bundles Management Board 8.dc.html#adm-215`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 8
- Flow F161 *Promotions Bundles Management board 8: Stacking & Conflict Command Center*, step 14: Works in Conflict Detection & Resolution Center → Detect promotion conflicts during both configuration and runtime.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-215?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Best price, Reject transaction where necessary.
- [ ] Every transition is wired: `ADM-208`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-216` Promotion Decision Trace & Transaction Explainer

**Provide complete explainability of how TICVAI arrived at the final promotional price. This screen will be extremely important for: Customer service Finance Operations Audit Partner disputes Technical support**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/promotion-decision-trace-transaction-explainer-adm-216` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listPromotionDecisionTrace` (onLoad, Promotion Decision Trace & Transaction Explainer)

**Where the user goes next**

- → `ADM-208` Stacking & Conflict Command Center: *Returns to the board's landing screen*; calls `listPromotionDecisionTrace`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The promotion decision trace list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the promotion decision trace untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No promotion decision trace yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the promotion decision trace are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPromotionDecisionTrace` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-216` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS113 Promotions   Bundles Management Board 8.dc.html#adm-216`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 8
- Flow F161 *Promotions Bundles Management board 8: Stacking & Conflict Command Center*, step 16: Works in Promotion Decision Trace & Transaction Explainer → Provide complete explainability of how TICVAI arrived at the final promotional price. This screen will be extremely important for: Customer service Finance Operations Audit Partner disputes Technical …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-216?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-208`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-217` Conflict Simulation & AI Optimization

**Test promotion interaction scenarios before publishing campaigns.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/conflict-simulation-ai-optimization-adm-217` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Change priority, Allow stacking, Create exclusions, Change calculation sequence, Change discount cap, Override margin floor, Create emergency rule, Activate hierarchy changes. Each needs attaching to the control it gates, or the screen needs the control.

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listConflict` (onLoad, Conflict Simulation & AI Optimization)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The conflict simulation optimization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the conflict simulation optimization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No conflict simulation optimization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the conflict simulation optimization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listConflict` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-217` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS113 Promotions   Bundles Management Board 8.dc.html#adm-217`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 8
- Flow F161 *Promotions Bundles Management board 8: Stacking & Conflict Command Center*, step 18: Works in Conflict Simulation & AI Optimization → Test promotion interaction scenarios before publishing campaigns.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-217?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PRICE_VIEW`.
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

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listBestOfferCustomer": {"method":"GET","path":"/best-offer-customer","contract":"promotions","summary":"Best Offer & Customer Benefit Resolver","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BestOfferCustomerBenefitResolverView"},
"listConflict": {"method":"GET","path":"/conflict","contract":"promotions","summary":"Conflict Simulation & AI Optimization","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ConflictSimulationAiOptimizationView"},
"listConflictDetectionResolution": {"method":"GET","path":"/conflict-detection-resolution","contract":"promotions","summary":"Conflict Detection & Resolution Center","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ConflictDetectionResolutionCenterView"},
"listDiscountCalculationApplication": {"method":"GET","path":"/discount-calculation-application","contract":"promotions","summary":"Discount Calculation & Application Sequence","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"DiscountCalculationApplicationSequenceView"},
"listDiscountCapMaximum": {"method":"GET","path":"/discount-cap-maximum","contract":"promotions","summary":"Discount Cap & Maximum Benefit Controller","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"DiscountCapMaximumBenefitControllerView"},
"listPromotionDecisionTrace": {"method":"GET","path":"/promotion-decision-trace","contract":"promotions","summary":"Promotion Decision Trace & Transaction Explainer","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PromotionDecisionTraceTransactionExplainerView"},
"listPromotionExclusionCompatibility": {"method":"GET","path":"/promotion-exclusion-compatibility","contract":"promotions","summary":"Promotion Exclusion & Compatibility Matrix","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PromotionExclusionCompatibilityMatrixView"},
"listPromotionPriorityHierarchy": {"method":"GET","path":"/promotion-priority-hierarchy","contract":"promotions","summary":"Promotion Priority & Hierarchy Manager","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PromotionPriorityHierarchyManagerView"},
"listStackingConflict": {"method":"GET","path":"/stacking-conflict","contract":"promotions","summary":"Stacking & Conflict Command Center","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"StackingConflictCommandCenterView"},
"setPromotionRule": {"method":"PUT","path":"/promotion-rule","contract":"promotions","summary":"Promotion Rule Builder","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PromotionRuleBuilderInput","responds":"PromotionRuleBuilderView"},
"setPromotionStackingRule": {"method":"PUT","path":"/promotion-stacking-rule","contract":"promotions","summary":"Promotion Stacking Rule Builder","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PromotionStackingRuleBuilderInput","responds":"PromotionStackingRuleBuilderView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"BestOfferCustomerBenefitResolverView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Best Offer & Customer Benefit Resolver displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"resolutionStrategy":{"type":"string","enum":["highestPriority","bestCustomerPrice","highestMargin","campaignPreference","contractualPriority"],"description":"Configured strategy. Default highestPriority: conflicts resolve through the configured hierarchy, not lowest-price-wins (MoM 1 Sep)"},"eligibleOffers":{"type":"array","items":{"type":"string"},"description":"Eligible offers and combinations with their saving"},"appliedOffers":{"type":"array","items":{"type":"string"},"description":"Offer or combination applied"},"saving":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Customer saving"},"customerMessage":{"type":"string","description":"What the sales channel shows, e.g. 'Best available offer applied automatically'"}}},
"ConflictDetectionResolutionCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Conflict Detection & Resolution Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"conflictType":{"type":"string","enum":["sameProduct","sameAudience","sameChannel","sameValidity","incompatiblePromotions","missingHierarchy","missingStackingRule","discountCapBreach","circularDependency"],"description":"Conflict detected."},"resolutionMethod":{"type":"string","enum":["automatic","ruleBased","bestPrice","priority","manualIntervention"],"description":"How the conflict is resolved."},"conflictId":{"type":"string","description":"Conflict ID"},"promotions":{"type":"array","items":{"type":"string"},"description":"Promotions in conflict"},"detectedAt":{"type":"string","format":"date-time","description":"When detected"},"resolved":{"type":"boolean","description":"Whether the conflict has been resolved"}}},
"ConflictSimulationAiOptimizationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Conflict Simulation & AI Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"customerSegment":{"type":"string","description":"Customer segment"},"membership":{"type":"string","description":"Membership"},"loyalty":{"type":"string","description":"Loyalty"},"products":{"type":"string","description":"Products"},"basket":{"type":"string","description":"Basket"},"coupon":{"type":"string","description":"Coupon"},"channel":{"type":"string","description":"Channel"},"venue":{"type":"string","description":"Venue"},"paymentMethod":{"type":"string","description":"Payment method"},"dateTime":{"type":"string","format":"date-time","description":"Date/time"},"combinations":{"type":"array","items":{"type":"string"},"description":"Candidate combinations with saving, margin and validity"},"recommendedCombination":{"type":"string","description":"Recommended combination"}}},
"DiscountCalculationApplicationSequenceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Discount Calculation & Application Sequence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"calculationModel":{"type":"string","enum":["sequential","additivePercentage","fixedThenPercentage","percentageThenFixed","bestPriceOnly","highestValueDiscountOnly","lowestPriceResult","priorityOrder"],"description":"How several discounts combine."},"taxBasis":{"type":"string","enum":["beforeTax","afterTax"],"description":"Whether the promotion applies before or after tax."},"feeBasis":{"type":"string","enum":["beforeFee","afterFee"],"description":"Whether the promotion applies before or after fees."},"applicationLevel":{"type":"string","enum":["productOnly","transactionTotal"],"description":"What the promotion applies to."}}},
"DiscountCapMaximumBenefitControllerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Discount Cap & Maximum Benefit Controller displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"maximumTotalDiscount":{"type":"number","description":"Maximum total discount %"},"maximumTotalDiscountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum total discount amount"},"minimumTransactionValue":{"type":"string","description":"Minimum transaction value"},"minimumProductPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Minimum product price"},"minimumMargin":{"type":"number","description":"Minimum margin"},"maximumFreeItemValue":{"type":"string","description":"Maximum free-item value"},"maximumPromotionalBenefit":{"type":"string","description":"Maximum promotional benefit"},"maximumPromotionsPerBasket":{"type":"string","description":"Maximum promotions per basket"},"potentialCombinedBenefit":{"type":"number","description":"Potential combined benefit, percent"},"configuredMaximum":{"type":"number","description":"Configured maximum, percent"},"limitLevel":{"type":"string","enum":["tenant","venue","category","campaign","customer","partner","channel","product","transaction"],"description":"Where the limit is set."},"onExceed":{"type":"string","enum":["reduceDiscount","useBestPermittedCombination","requireApproval"],"description":"What happens when the combined benefit exceeds the cap."}}},
"PromotionDecisionTraceTransactionExplainerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion Decision Trace & Transaction Explainer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"totalSaving":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Total saving"},"transactionId":{"type":"string","description":"Transaction ID"},"evaluatedPromotions":{"type":"array","items":{"type":"string"},"description":"Promotions evaluated"},"eligiblePromotions":{"type":"array","items":{"type":"string"},"description":"Promotions the transaction was eligible for"},"rejectedPromotions":{"type":"array","items":{"type":"string"},"description":"Promotions rejected, each with its reason"},"appliedPromotions":{"type":"array","items":{"type":"string"},"description":"Promotions applied, in application order"},"steps":{"type":"array","items":{"type":"string"},"description":"Decision steps in order (eligibility, hierarchy, stacking, caps, best permitted combination)"}}},
"PromotionExclusionCompatibilityMatrixView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion Exclusion & Compatibility Matrix displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"applicableProducts":{"type":"integer","description":"Applicable products"},"applicableVenues":{"type":"integer","description":"Applicable venues"},"channels":{"type":"integer","description":"Channels"},"customerSegments":{"type":"integer","description":"Customer segments"},"rule":{"type":"string","description":"Rule"},"priority":{"type":"string","description":"Priority"},"effectiveDates":{"type":"integer","description":"Effective dates"},"exceptions":{"type":"integer","description":"Exceptions"},"relationship":{"type":"string","enum":["allowed","notAllowed","conditional","priorityBased","notConfigured"],"description":"Compatibility between the two promotion types."},"promotionTypeA":{"type":"string","description":"Row promotion type"},"promotionTypeB":{"type":"string","description":"Column promotion type"}}},
"PromotionPriorityHierarchyManagerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion Priority & Hierarchy Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"promotionFamily":{"type":"string","description":"Promotion family"},"promotion":{"type":"string","description":"Promotion"},"priorityNumber":{"type":"string","description":"Priority number"},"priorityGroup":{"type":"string","description":"Priority group"},"effectiveDates":{"type":"string","description":"Effective dates"},"channel":{"type":"string","description":"Channel"},"venue":{"type":"string","description":"Venue"},"customerSegment":{"type":"string","description":"Customer segment"},"tenant":{"type":"string","description":"Tenant"},"businessEntity":{"type":"string","description":"Business entity"},"productCategory":{"type":"string","description":"Product category"},"customerType":{"type":"string","description":"Customer type"},"campaign":{"type":"string","description":"Campaign"}}},
"PromotionRuleBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; saved as a `promotions.promotion_rule` row (PromotionRule, ruleType benefit) (DM5, 29 September: data model for the agreed operations)","description":"**What Promotion Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"ruleName":{"type":"string","description":"Rule name"},"ruleId":{"type":"string","description":"Rule ID"},"promotion":{"type":"string","description":"Promotion"},"description":{"type":"string","description":"Description"},"owner":{"type":"string","description":"Owner"},"businessEntity":{"type":"string","description":"Business entity"},"venue":{"type":"string","description":"Venue"},"ruleStatus":{"type":"string","description":"Rule status"},"priority":{"type":"string","description":"Priority"},"percentageDiscount":{"type":"number","description":"Percentage discount"},"fixedDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed discount"},"fixedSellingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed selling price"},"freeProduct":{"type":"string","description":"Free product"},"freeTicket":{"type":"string","description":"Free ticket"},"addedValue":{"type":"string","description":"Added value"},"voucher":{"type":"string","description":"Voucher"},"rewardEntitlement":{"type":"string","description":"Reward entitlement"},"nestedConditionGroups":{"type":"string","description":"Nested condition groups"},"multipleOutcomes":{"type":"string","description":"Multiple outcomes"},"ruleOrdering":{"type":"string","description":"Rule ordering"}}},
"PromotionRuleBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleName":{"type":"string","description":"Rule name"},"ruleId":{"type":"string","description":"Rule ID"},"promotion":{"type":"string","description":"Promotion"},"description":{"type":"string","description":"Description"},"owner":{"type":"string","description":"Owner"},"businessEntity":{"type":"string","description":"Business entity"},"venue":{"type":"string","description":"Venue"},"ruleStatus":{"type":"string","description":"Rule status"},"priority":{"type":"string","description":"Priority"},"percentageDiscount":{"type":"number","description":"Percentage discount"},"fixedDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed discount"},"fixedSellingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed selling price"},"freeProduct":{"type":"string","description":"Free product"},"freeTicket":{"type":"string","description":"Free ticket"},"addedValue":{"type":"string","description":"Added value"},"voucher":{"type":"string","description":"Voucher"},"rewardEntitlement":{"type":"string","description":"Reward entitlement"},"nestedConditionGroups":{"type":"string","description":"Nested condition groups"},"multipleOutcomes":{"type":"string","description":"Multiple outcomes"},"ruleOrdering":{"type":"string","description":"Rule ordering"}}},
"PromotionStackingRuleBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; the configurable part of a `promotions.stacking_rule` row (StackingRule composes it) (DM5, 29 September: data model for the agreed operations)","description":"**What Promotion Stacking Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"scope":{"type":"string","enum":["entireTransaction","product","productCategory","individualTicket","bundleComponent","customer","channel"],"description":"What the rule applies to."},"stackingModel":{"type":"string","enum":["fullyStackable","nonStackable","conditional","categoryStacking","maximumN"],"description":"Stacking model"},"maximumPromotions":{"type":"integer","description":"For maximumN: most promotions per transaction"},"promotionTypeA":{"type":"string","description":"First promotion type in the rule"},"promotionTypeB":{"type":"string","description":"Second promotion type in the rule"},"canStack":{"type":"boolean","description":"Whether A can stack with B"}}},
"PromotionStackingRuleBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion Stacking Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"scope":{"type":"string","enum":["entireTransaction","product","productCategory","individualTicket","bundleComponent","customer","channel"],"description":"What the rule applies to."},"stackingModel":{"type":"string","enum":["fullyStackable","nonStackable","conditional","categoryStacking","maximumN"],"description":"Stacking model"},"maximumPromotions":{"type":"integer","description":"For maximumN: most promotions per transaction"},"promotionTypeA":{"type":"string","description":"First promotion type in the rule"},"promotionTypeB":{"type":"string","description":"Second promotion type in the rule"},"canStack":{"type":"boolean","description":"Whether A can stack with B"}}},
"StackingConflictCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Stacking & Conflict Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"activePromotionRules":{"type":"integer","description":"Active Promotion Rules"},"stackablePromotions":{"type":"integer","description":"Stackable Promotions"},"exclusivePromotions":{"type":"integer","description":"Exclusive Promotions"},"priorityRules":{"type":"integer","description":"Priority Rules"},"conflictsDetected":{"type":"string","description":"Conflicts Detected"},"criticalConflicts":{"type":"integer","description":"Critical Conflicts"},"autoResolvedConflicts":{"type":"integer","description":"Auto-Resolved Conflicts"},"transactionsWithMultipleOffers":{"type":"string","description":"Transactions with Multiple Offers"},"averagePromotionsPerTransaction":{"type":"number","description":"Average Promotions per Transaction"},"discountExposure":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount Exposure"},"preventedOverDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Prevented Over-Discount"},"revenueProtected":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue Protected"},"promotionType":{"type":"string","enum":["vs","couponVs","couponVsCoupon","bogoVsDiscount","bundleVs","membershipVs","loyaltyVs","bankOfferVs","partnerOfferVs","specialPriceVs"],"description":"Vocabulary listed under Conflict Categories."},"information":{"type":"string","description":"Information"},"warning":{"type":"string","description":"Warning"},"high":{"type":"string","description":"High"},"critical":{"type":"string","description":"Critical"}}}
}
```
