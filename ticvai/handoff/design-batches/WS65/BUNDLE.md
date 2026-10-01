# WS65 — Ticket Upgrade, Exchange & Conversion board 1

**10 screens · 10 operations · 13 schemas · 2 permissions**

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
  `ORDER_CREATE, ORDER_VIEW`. A control nobody can use must say so,
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
| `ADM-308` | Upgrade & Conversion Command Center | B–D | 2 | 24 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-309` | Upgrade & Conversion Path Builder | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-310` | Upgrade Eligibility & Qualification Rules | B–D | 7 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-311` | Upgrade Timing, Usage & Ticket Status Rules | B–D | 13 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-312` | Upgrade Financial Treatment & Price Difference Rules | B–D | 10 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-313` | Pro-Rata, Residual Value & Entitlement Credit Configuration | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-314` | Person-Type, Product & Entitlement Conversion Rules | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-315` | Bulk, Group & Assisted Upgrade Operations | B–D | 9 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-316` | Upgrade Execution, Credential Regeneration & Channel Controls | B–D | 8 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-317` | Upgrade History, Exception Management & Audit Explorer | B–D | 2 | 2 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-309, ADM-313, ADM-314 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-308` Upgrade & Conversion Command Center

**Provide administrators and operations teams with one centralized view of all ticket upgrade, exchange and conversion configurations and operational activity.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each configuration displays) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/upgrade-conversion-command-center-adm-308` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search upgrade conversion | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, event, product, transaction type, channel, customer segment and 2 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Event | text field | — | — | `listUpgradeConversion` ?event |
| Product | text field | — | — | `listUpgradeConversion` ?product |
| Customer segment | text field | — | — | `listUpgradeConversion` ?customerSegment |
| Rule status | text field | — | — | `listUpgradeConversion` ?ruleStatus |
| Effective date | text field | — | — | `listUpgradeConversion` ?effectiveDate |
| Venue | text field | — | — | `listUpgradeConversion` ?venue |
| Transaction type | text field | — | — | `listUpgradeConversion` ?transactionType |
| Channel | text field | — | — | `listUpgradeConversion` ?channel |

#### Outputs: what the screen shows and produces

**Shown**

**Active Upgrade Paths** (metric tile)

**Active Conversion Rules** (metric tile)

**Products Eligible for Upgrade** (metric tile)

**Products Excluded** (metric tile)

**Upgrades Today** (metric tile)

**Conversions Today** (metric tile)

**Upgrade Revenue** (metric tile)

**Pending Exceptions** (metric tile)

**Failed Conversions** (metric tile)

**Expiring Rules** (metric tile)

**Configuration Conflicts** (metric tile)

**Manual Overrides** (metric tile)

**Every upgrade conversion** (data table, from `listUpgradeConversion`)

| Shows | Format | Notes |
|---|---|---|
| Rule | text | Rule ID |
| Rule name | text | Rule Name |
| Source product | text | Source Product |
| Target product | text | Target Product |
| Transaction type | chip: Upgrade, Downgrade, Exchange, Conversion, Person type conversion, Product conversion | Transaction type |
| Venue | text | Venue |
| Channel | text | Channel |
| Effective period | 1 Oct 2026, 14:30 | Effective Period |
| Financial method | text | Financial Method |
| Approval requirement | text | Approval Requirement |
| Status | text | Status |
| Owner | text | Owner |

**The selected upgrade conversion** (detail panel): The pack groups this record's detail under its own headings: “Upgrade”, “Downgrade”, “Exchange”, “Conversion”, “Person-Type Conversion”, “Product Conversion”.

| Shows | Format | Notes |
|---|---|---|
| Rule | text | Rule ID |
| Rule name | text | Rule Name |
| Source product | text | Source Product |
| Target product | text | Target Product |
| Transaction type | chip: Upgrade, Downgrade, Exchange, Conversion, Person type conversion, Product conversion | Transaction type |
| Venue | text | Venue |
| Channel | text | Channel |
| Effective period | 1 Oct 2026, 14:30 | Effective Period |
| Financial method | text | Financial Method |
| Approval requirement | text | Approval Requirement |
| Status | text | Status |
| Owner | text | Owner |

**Data it reads**: `listUpgradeConversion` (onLoad, Upgrade & Conversion Command Center)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-309` Upgrade & Conversion Path Builder: *Works in Upgrade & Conversion Path Builder*; calls `listUpgradeConversion`
- → `ADM-310` Upgrade Eligibility & Qualification Rules: *Works in Upgrade Eligibility & Qualification Rules*; calls `listUpgradeConversion`
- → `ADM-311` Upgrade Timing, Usage & Ticket Status Rules: *Works in Upgrade Timing, Usage & Ticket Status Rules*; calls `listUpgradeConversion`
- → `ADM-312` Upgrade Financial Treatment & Price Difference Rules: *Works in Upgrade Financial Treatment & Price Difference Rules*; calls `listUpgradeConversion`
- → `ADM-313` Pro-Rata, Residual Value & Entitlement Credit Configuration: *Works in Pro-Rata, Residual Value & Entitlement Credit Configuration*; calls `listUpgradeConversion`
- → `ADM-314` Person-Type, Product & Entitlement Conversion Rules: *Works in Person-Type, Product & Entitlement Conversion Rules*; calls `listUpgradeConversion`
- → `ADM-315` Bulk, Group & Assisted Upgrade Operations: *Works in Bulk, Group & Assisted Upgrade Operations*; calls `listUpgradeConversion`
- → `ADM-316` Upgrade Execution, Credential Regeneration & Channel Controls: *Works in Upgrade Execution, Credential Regeneration & Channel Controls*; calls `listUpgradeConversion`
- → `ADM-317` Upgrade History, Exception Management & Audit Explorer: *Works in Upgrade History, Exception Management & Audit Explorer*; calls `listUpgradeConversion`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The upgrade conversion list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the upgrade conversion untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No upgrade conversion yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the upgrade conversion are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listUpgradeConversion` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Upgrade dashboard shows upgrade/exchange volume and upgrade revenue for a period. Paths define which product upgrades to which (adult ticket to membership; lower to higher membership tier), with downgrade paths where allowed. *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-602)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-308` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS171 Ticket Upgrade, Exchange & Conversion Board 1.dc.html#adm-308`
- Workshop pack: Ticket Upgrade, Exchange & Conversion_Reference.pdf board 1
- Flow F174 *Ticket Upgrade, Exchange & Conversion board 1: Upgrade & Conversion Command …*, step 1: Opens Upgrade & Conversion Command Center → Provide administrators and operations teams with one centralized view of all ticket upgrade, exchange and conversion configurations and operational activity.
- Flow F174 *Ticket Upgrade, Exchange & Conversion board 1: Upgrade & Conversion Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F174 *Ticket Upgrade, Exchange & Conversion board 1: Upgrade & Conversion Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F174 *Ticket Upgrade, Exchange & Conversion board 1: Upgrade & Conversion Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F174 *Ticket Upgrade, Exchange & Conversion board 1: Upgrade & Conversion Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F174 *Ticket Upgrade, Exchange & Conversion board 1: Upgrade & Conversion Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F174 *Ticket Upgrade, Exchange & Conversion board 1: Upgrade & Conversion Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F174 *Ticket Upgrade, Exchange & Conversion board 1: Upgrade & Conversion Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F174 branch at step 1 (expected): when Nothing has been set up on Upgrade & Conversion Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F174 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-308?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-309`, `ADM-310`, `ADM-311`, `ADM-312`, `ADM-313`, `ADM-314`, `ADM-315`, `ADM-316`, `ADM-317`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-309` Upgrade & Conversion Path Builder

**Define exactly which products/tickets may be converted into which other products. This becomes the central conversion relationship engine.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_CREATE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/upgrade-conversion-path-builder-adm-309` |

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

- → `ADM-308` Upgrade & Conversion Command Center: *Returns to the board's landing screen*; calls `setUpgradeConversionPath`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The upgrade conversion path list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the upgrade conversion path untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No upgrade conversion path yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the upgrade conversion path are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setUpgradeConversionPath` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Upgrade dashboard shows upgrade/exchange volume and upgrade revenue for a period. Paths define which product upgrades to which (adult ticket to membership; lower to higher membership tier), with downgrade paths where allowed. *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-602)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-309` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS171 Ticket Upgrade, Exchange & Conversion Board 1.dc.html#adm-309`
- Workshop pack: Ticket Upgrade, Exchange & Conversion_Reference.pdf board 1
- Flow F174 *Ticket Upgrade, Exchange & Conversion board 1: Upgrade & Conversion Command …*, step 2: Works in Upgrade & Conversion Path Builder → Define exactly which products/tickets may be converted into which other products. This becomes the central conversion relationship engine.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-309?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `ADM-308`.
- [ ] Every gated control is gated: `ORDER_CREATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-310` Upgrade Eligibility & Qualification Rules

**Determine whether a particular ticket/customer/transaction qualifies for a configured upgrade or conversion path. A path existing does not automatically mean every ticket can use it.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure eligibility for) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/upgrade-eligibility-qualification-rules-adm-310` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Valid | select field | — | — | — | — | — | — |
| Unused | select field | — | — | — | — | — | — |
| Partially Used | select field | — | — | — | — | — | — |
| Used | select field | — | — | — | — | — | — |
| Expired | select field | — | — | — | — | — | — |
| Cancelled | select field | — | — | — | — | — | — |
| Suspended | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listUpgradeEligibilityQualification` (onLoad, Upgrade Eligibility & Qualification Rules)

**Where the user goes next**

- → `ADM-308` Upgrade & Conversion Command Center: *Returns to the board's landing screen*; calls `listUpgradeEligibilityQualification`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The upgrade eligibility qualification configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the upgrade eligibility qualification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No upgrade eligibility qualification configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listUpgradeEligibilityQualification` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Upgrade eligibility checks validity/usage. Cases: seated ticket to a better section same day, paying the difference at the counter; general admission to season pass with the amount paid credited. Windows: before use, after use within a window, or until a cutoff (event ticket until the guest exits). *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-603)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-310` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS171 Ticket Upgrade, Exchange & Conversion Board 1.dc.html#adm-310`
- Workshop pack: Ticket Upgrade, Exchange & Conversion_Reference.pdf board 1
- Flow F174 *Ticket Upgrade, Exchange & Conversion board 1: Upgrade & Conversion Command …*, step 4: Works in Upgrade Eligibility & Qualification Rules → Determine whether a particular ticket/customer/transaction qualifies for a configured upgrade or conversion path. A path existing does not automatically mean every ticket can use it.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-310?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-308`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-311` Upgrade Timing, Usage & Ticket Status Rules

**Define how ticket lifecycle state affects upgrade and conversion behavior. This deserves its own screen because a ticket may already have been partially consumed.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure treatment of; Configure; Configure whether) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/upgrade-timing-usage-ticket-status-rules-adm-311` |

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Before Expiry, Grace Period. Each needs an operation, or needs removing from the screen; this is the Phase 3 …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Used Admissions | select field | — | — | — | — | — | — |
| Unused Admissions | select field | — | — | — | — | — | — |
| Remaining Days | select field | — | — | — | — | — | — |
| Remaining Stored Value | select field | — | — | — | — | — | — |
| Remaining Benefits | select field | — | — | — | — | — | — |
| Invalidate | select field | — | — | — | — | — | — |
| Supersede | select field | — | — | — | — | — | — |
| Retain for History | select field | — | — | — | — | — | — |
| Link to New Ticket | text field | — | — | — | — | — | — |
| Partially Retain Entitlement | select field | — | — | — | — | — | — |
| Never Eligible | select field | — | — | — | — | — | — |
| Eligible Within Grace Period | text field | — | — | — | — | — | — |
| Supervisor Exception Allowed | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Before Expiry (primary button) | navigation or local | — | — | — | — |
| Grace Period (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listUpgradeTimingUsage` (onLoad, Upgrade Timing, Usage & Ticket Status Rules)

**Where the user goes next**

- → `ADM-308` Upgrade & Conversion Command Center: *Returns to the board's landing screen*; calls `listUpgradeTimingUsage`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The upgrade timing usage configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the upgrade timing usage untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No upgrade timing usage configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listUpgradeTimingUsage` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Upgrade eligibility checks validity/usage. Cases: seated ticket to a better section same day, paying the difference at the counter; general admission to season pass with the amount paid credited. Windows: before use, after use within a window, or until a cutoff (event ticket until the guest exits). *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-603)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-311` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS171 Ticket Upgrade, Exchange & Conversion Board 1.dc.html#adm-311`
- Workshop pack: Ticket Upgrade, Exchange & Conversion_Reference.pdf board 1
- Flow F174 *Ticket Upgrade, Exchange & Conversion board 1: Upgrade & Conversion Command …*, step 6: Works in Upgrade Timing, Usage & Ticket Status Rules → Define how ticket lifecycle state affects upgrade and conversion behavior. This deserves its own screen because a ticket may already have been partially consumed.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-311?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Before Expiry, Grace Period.
- [ ] Every transition is wired: `ADM-308`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-312` Upgrade Financial Treatment & Price Difference Rules

**Define how the financial relationship between the old and new product should be treated.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure whether target pricing uses; Configure whether existing) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/upgrade-financial-treatment-price-difference-rules-adm-312` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Current Selling Price | select field | — | — | — | — | — | — |
| Original-Date Price | select field | — | — | — | — | — | — |
| Upgrade-Specific Rate | select field | — | — | — | — | — | — |
| Contracted Rate | select field | — | — | — | — | — | — |
| Membership Rate | select field | — | — | — | — | — | — |
| Fixed Upgrade Price | select field | — | — | — | — | — | — |
| Promotion | select field | — | — | — | — | — | — |
| Membership Discount | select field | — | — | — | — | — | — |
| Voucher | select field | — | — | — | — | — | — |
| Corporate Discount | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listUpgradeFinancialTreatment` (onLoad, Upgrade Financial Treatment & Price Difference Rules)

**Where the user goes next**

- → `ADM-308` Upgrade & Conversion Command Center: *Returns to the board's landing screen*; calls `listUpgradeFinancialTreatment`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The upgrade financial treatment configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the upgrade financial treatment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No upgrade financial treatment configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listUpgradeFinancialTreatment` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Usage-based upgrades are pro-rata: e.g. 2 months used of a 1-year silver membership is credited and only the balance to the higher tier is charged. Attribute upgrades: a child ticket (sold by height) found to be adult on arrival is upgraded with the difference charged. *(agreed · MoM 1 Sep 2026, 4.9 Upgrade financial treatment · DI-604)*
- Upgrade eligibility checks validity/usage. Cases: seated ticket to a better section same day, paying the difference at the counter; general admission to season pass with the amount paid credited. Windows: before use, after use within a window, or until a cutoff (event ticket until the guest exits). *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-603)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-312` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS171 Ticket Upgrade, Exchange & Conversion Board 1.dc.html#adm-312`
- Workshop pack: Ticket Upgrade, Exchange & Conversion_Reference.pdf board 1
- Flow F174 *Ticket Upgrade, Exchange & Conversion board 1: Upgrade & Conversion Command …*, step 8: Works in Upgrade Financial Treatment & Price Difference Rules → Define how the financial relationship between the old and new product should be treated.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-312?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-308`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-313` Pro-Rata, Residual Value & Entitlement Credit Configuration

**Handle complex upgrades where part of the original product has already been consumed.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_CREATE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/pro-rata-residual-value-entitlement-credit-configuration-adm-313` |

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

- → `ADM-308` Upgrade & Conversion Command Center: *Returns to the board's landing screen*; calls `setProRataResidual`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pro-rata residual value list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pro-rata residual value untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pro-rata residual value yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pro-rata residual value are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setProRataResidual` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Usage-based upgrades are pro-rata: e.g. 2 months used of a 1-year silver membership is credited and only the balance to the higher tier is charged. Attribute upgrades: a child ticket (sold by height) found to be adult on arrival is upgraded with the difference charged. *(agreed · MoM 1 Sep 2026, 4.9 Upgrade financial treatment · DI-604)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-313` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS171 Ticket Upgrade, Exchange & Conversion Board 1.dc.html#adm-313`
- Workshop pack: Ticket Upgrade, Exchange & Conversion_Reference.pdf board 1
- Flow F174 *Ticket Upgrade, Exchange & Conversion board 1: Upgrade & Conversion Command …*, step 10: Works in Pro-Rata, Residual Value & Entitlement Credit Configuration → Handle complex upgrades where part of the original product has already been consumed.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-313?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `ADM-308`.
- [ ] Every gated control is gated: `ORDER_CREATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-314` Person-Type, Product & Entitlement Conversion Rules

**Handle conversions that change more than simply the commercial level of a ticket.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/person-type-product-entitlement-conversion-rules-adm-314` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listPersonTypeProduct` (onLoad, Person-Type, Product & Entitlement Conversion Rules)

**Where the user goes next**

- → `ADM-308` Upgrade & Conversion Command Center: *Returns to the board's landing screen*; calls `listPersonTypeProduct`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The person-type product entitlement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the person-type product entitlement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No person-type product entitlement yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the person-type product entitlement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPersonTypeProduct` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Usage-based upgrades are pro-rata: e.g. 2 months used of a 1-year silver membership is credited and only the balance to the higher tier is charged. Attribute upgrades: a child ticket (sold by height) found to be adult on arrival is upgraded with the difference charged. *(agreed · MoM 1 Sep 2026, 4.9 Upgrade financial treatment · DI-604)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-314` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS171 Ticket Upgrade, Exchange & Conversion Board 1.dc.html#adm-314`
- Workshop pack: Ticket Upgrade, Exchange & Conversion_Reference.pdf board 1
- Flow F174 *Ticket Upgrade, Exchange & Conversion board 1: Upgrade & Conversion Command …*, step 12: Works in Person-Type, Product & Entitlement Conversion Rules → Handle conversions that change more than simply the commercial level of a ticket.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-314?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-308`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-315` Bulk, Group & Assisted Upgrade Operations

**Support operational upgrades involving multiple tickets rather than requiring staff to process each individually.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select by; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/bulk-group-assisted-upgrade-operations-adm-315` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Upgrade Selected, Convert Product, Change Person Type, Move to Alternative Performance. Each needs an …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Order | select field | — | — | — | — | — | — |
| Reservation | select field | — | — | — | — | — | — |
| Group | select field | — | — | — | — | — | — |
| Event | select field | — | — | — | — | — | — |
| Performance | select field | — | — | — | — | — | — |
| Ticket Type | select field | — | — | — | — | — | — |
| Seat Section | select field | — | — | — | — | — | — |
| Customer Segment | select field | — | — | — | — | — | — |
| Process eligible tickets and exclude failures | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Order | text field | — | — | `listBulkGroupAssisted` ?order |
| Reservation | text field | — | — | `listBulkGroupAssisted` ?reservation |
| Group | text field | — | — | `listBulkGroupAssisted` ?group |
| Event | text field | — | — | `listBulkGroupAssisted` ?event |
| Performance | text field | — | — | `listBulkGroupAssisted` ?performance |
| Ticket type | text field | — | — | `listBulkGroupAssisted` ?ticketType |
| Seat section | text field | — | — | `listBulkGroupAssisted` ?seatSection |
| Customer segment | text field | — | — | `listBulkGroupAssisted` ?customerSegment |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Upgrade Selected (primary button) | navigation or local | — | — | — | — |
| Convert Product (secondary button) | navigation or local | — | — | — | — |
| Change Person Type (secondary button) | navigation or local | — | — | — | — |
| Move to Alternative Performance (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listBulkGroupAssisted` (onLoad, Bulk, Group & Assisted Upgrade Operations)

**Where the user goes next**

- → `ADM-308` Upgrade & Conversion Command Center: *Returns to the board's landing screen*; calls `listBulkGroupAssisted`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The bulk group assisted configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the bulk group assisted untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No bulk group assisted configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listBulkGroupAssisted` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group ticket upgrades are business-configurable (off by default); where allowed a group raises an upgrade request (e.g. via chat/support) rather than self-serving like an individual. *(agreed · MoM 1 Sep 2026, 4.9 Clarified (group upgrades) · DI-607)*
- Staff can upgrade multiple tickets in one action. "Quick upgrade" is a direct single-path upgrade (gold > platinum); "flexible upgrade" lets the guest choose among several eligible targets. *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-605)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-315` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS171 Ticket Upgrade, Exchange & Conversion Board 1.dc.html#adm-315`
- Workshop pack: Ticket Upgrade, Exchange & Conversion_Reference.pdf board 1
- Flow F174 *Ticket Upgrade, Exchange & Conversion board 1: Upgrade & Conversion Command …*, step 14: Works in Bulk, Group & Assisted Upgrade Operations → Support operational upgrades involving multiple tickets rather than requiring staff to process each individually.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-315?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Upgrade Selected, Convert Product, Change Person Type, Move to Alternative Performance.
- [ ] Every transition is wired: `ADM-308`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-316` Upgrade Execution, Credential Regeneration & Channel Controls

**Control what happens operationally once an upgrade or conversion is approved and financially completed.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_CREATE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Depending on configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/upgrade-execution-credential-regeneration-channel-contro-adm-316` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Regenerate QR | select field | — | — | — | — | — | — |
| Invalidate Old QR | select field | — | — | — | — | — | — |
| Update Dynamic QR | select field | — | — | — | — | — | — |
| Update RFID | select field | — | — | — | — | — | — |
| Update NFC | select field | — | — | — | — | — | — |
| Update Wallet Pass | select field | — | — | — | — | — | — |
| Reissue Ticket | select field | — | — | — | — | — | — |
| Preserve Existing Credential | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-308` Upgrade & Conversion Command Center: *Returns to the board's landing screen*; calls `createUpgradeCredentialRegeneration`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The upgrade execution credential configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the upgrade execution credential untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No upgrade execution credential configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `createUpgradeCredentialRegeneration` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staff can upgrade multiple tickets in one action. "Quick upgrade" is a direct single-path upgrade (gold > platinum); "flexible upgrade" lets the guest choose among several eligible targets. *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-605)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-316` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS171 Ticket Upgrade, Exchange & Conversion Board 1.dc.html#adm-316`
- Workshop pack: Ticket Upgrade, Exchange & Conversion_Reference.pdf board 1
- Flow F174 *Ticket Upgrade, Exchange & Conversion board 1: Upgrade & Conversion Command …*, step 16: Works in Upgrade Execution, Credential Regeneration & Channel Controls → Control what happens operationally once an upgrade or conversion is approved and financially completed.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-316?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create.
- [ ] Every transition is wired: `ADM-308`.
- [ ] Every gated control is gated: `ORDER_CREATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-317` Upgrade History, Exception Management & Audit Explorer

**Provide complete operational and financial traceability for every upgrade, downgrade, exchange and conversion.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/upgrade-history-exception-management-audit-explorer-adm-317` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search upgrade history exception | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by ticket, order, customer, event, product, agent and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Ticket | text field | — | — | `listUpgradeException` ?ticket |
| Event | text field | — | — | `listUpgradeException` ?event |
| Product | text field | — | — | `listUpgradeException` ?product |
| Date | text field | — | — | `listUpgradeException` ?date |
| Exception | text field | — | — | `listUpgradeException` ?exception |
| Order | text field | — | — | `listUpgradeException` ?order |
| Customer | text field | — | — | `listUpgradeException` ?customer |
| Agent | text field | — | — | `listUpgradeException` ?agent |
| Channel | text field | — | — | `listUpgradeException` ?channel |
| Transaction type | text field | — | — | `listUpgradeException` ?transactionType |

#### Outputs: what the screen shows and produces

**Shown**

**Every upgrade history exception** (data table, from `listUpgradeException`)

| Shows | Format | Notes |
|---|---|---|
| Exception type | chip: Eligibility override, Financial override, Expired ticket exception, Manual credit … | Exception or override. |

**The selected upgrade history exception** (detail panel): The pack groups this record's detail under its own headings: “Store”, “Standard Admission”, “Manual Override”, “Require”, “Source-to-target”, “Controls”.

| Shows | Format | Notes |
|---|---|---|
| Exception type | chip: Eligibility override, Financial override, Expired ticket exception, Manual credit … | Exception or override. |

**Data it reads**: `listUpgradeException` (onLoad, Upgrade History, Exception Management & Audit Explorer)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The upgrade history exception list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the upgrade history exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No upgrade history exception yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the upgrade history exception are still there. The pack's own statuses are controls — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listUpgradeException` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-317` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS171 Ticket Upgrade, Exchange & Conversion Board 1.dc.html#adm-317`
- Workshop pack: Ticket Upgrade, Exchange & Conversion_Reference.pdf board 1
- Flow F174 *Ticket Upgrade, Exchange & Conversion board 1: Upgrade & Conversion Command …*, step 18: Works in Upgrade History, Exception Management & Audit Explorer → Provide complete operational and financial traceability for every upgrade, downgrade, exchange and conversion.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-317?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ORDER_VIEW`.
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

**12 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createUpgradeCredentialRegeneration": {"method":"POST","path":"/upgrade-credential-regeneration","contract":"orders","summary":"Upgrade Execution, Credential Regeneration & Channel Controls","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"UpgradeExecutionCredentialRegenerationChannelControlInput","responds":"UpgradeExecutionCredentialRegenerationChannelControlView"},
"listBulkGroupAssisted": {"method":"GET","path":"/bulk-group-assisted","contract":"orders","summary":"Bulk, Group & Assisted Upgrade Operations","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"order","in":"query","required":false},{"name":"reservation","in":"query","required":false},{"name":"group","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"performance","in":"query","required":false},{"name":"ticketType","in":"query","required":false},{"name":"seatSection","in":"query","required":false},{"name":"customerSegment","in":"query","required":false}],"requestBody":null,"responds":"BulkGroupAssistedUpgradeOperationsView"},
"listPersonTypeProduct": {"method":"GET","path":"/person-type-product","contract":"orders","summary":"Person-Type, Product & Entitlement Conversion Rules","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PersonTypeProductEntitlementConversionRulesView"},
"listUpgradeConversion": {"method":"GET","path":"/upgrade-conversion","contract":"orders","summary":"Upgrade & Conversion Command Center","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"event","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"customerSegment","in":"query","required":false},{"name":"ruleStatus","in":"query","required":false},{"name":"effectiveDate","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"transactionType","in":"query","required":false},{"name":"channel","in":"query","required":false}],"requestBody":null,"responds":"UpgradeConversionCommandCenterView"},
"listUpgradeEligibilityQualification": {"method":"GET","path":"/upgrade-eligibility-qualification","contract":"orders","summary":"Upgrade Eligibility & Qualification Rules","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"UpgradeEligibilityQualificationRulesView"},
"listUpgradeException": {"method":"GET","path":"/upgrade-exception","contract":"orders","summary":"Upgrade History, Exception Management & Audit Explorer","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"ticket","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"date","in":"query","required":false},{"name":"exception","in":"query","required":false},{"name":"order","in":"query","required":false},{"name":"customer","in":"query","required":false},{"name":"agent","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"transactionType","in":"query","required":false}],"requestBody":null,"responds":"UpgradeHistoryExceptionManagementAuditExplorerView"},
"listUpgradeFinancialTreatment": {"method":"GET","path":"/upgrade-financial-treatment","contract":"orders","summary":"Upgrade Financial Treatment & Price Difference Rules","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"UpgradeFinancialTreatmentPriceDifferenceRulesView"},
"listUpgradeTimingUsage": {"method":"GET","path":"/upgrade-timing-usage","contract":"orders","summary":"Upgrade Timing, Usage & Ticket Status Rules","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"UpgradeTimingUsageTicketStatusRulesView"},
"setProRataResidual": {"method":"PUT","path":"/pro-rata-residual","contract":"orders","summary":"Pro-Rata, Residual Value & Entitlement Credit Configuration","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"ProRataResidualValueEntitlementCreditConfigurationInput","responds":"ProRataResidualValueEntitlementCreditConfigurationView"},
"setUpgradeConversionPath": {"method":"PUT","path":"/upgrade-conversion-path","contract":"orders","summary":"Upgrade & Conversion Path Builder","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"UpgradeConversionPathBuilderInput","responds":"UpgradeConversionPathBuilderView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"BulkGroupAssistedUpgradeOperationsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Bulk, Group & Assisted Upgrade Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"bulkAction":{"type":"string","enum":["upgradeAll","upgradeSelected","convertProduct","changePersonType","applyComplimentaryUpgrade","applyFixedUpgrade","moveToAlternativePerformance"],"description":"Bulk action previewed"},"selectedCount":{"type":"integer","description":"Tickets selected"},"eligibleCount":{"type":"integer","description":"Tickets eligible"},"notEligibleCount":{"type":"integer","description":"Tickets not eligible"},"ineligibilityReasons":{"type":"array","items":{"type":"string"},"description":"Reasons with counts, e.g. already used, expired, target unavailable"},"totalOriginalEligibleValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Total original eligible value"},"totalTargetValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Total target value"},"totalUpgradeDifference":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Total upgrade difference"},"fees":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fees"},"taxes":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Taxes"},"finalCollectionOrRefund":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Final collection or refund requirement"},"partialProcessing":{"type":"string","enum":["processEligibleExcludeFailures","failEntireBatch"],"description":"Partial processing policy"}}},
"PersonTypeProductEntitlementConversionRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Person-Type, Product & Entitlement Conversion Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"conversionType":{"type":"string","enum":["childAdult","juniorAdult","seniorAdult","residentTourist","standardMember","customPersonTypes"],"description":"Person-type conversion."},"entitlementTreatment":{"type":"string","enum":["retained","replaced","added","removed","alreadyConsumed"],"description":"What happens to each entitlement on conversion."},"targetRequirements":{"type":"array","items":{"type":"string","enum":["age","residency","corporateAssociation","identityVerification","otherEligibilityRules"]},"description":"What the target product may require."},"sourceProduct":{"type":"string","description":"Source product"},"targetProduct":{"type":"string","description":"Target product"}}},
"ProRataResidualValueEntitlementCreditConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; lands in the pro-rata columns of `orders.upgrade_rule` (DM5, 29 September)","description":"**What Pro-Rata, Residual Value & Entitlement Credit Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"appliesTo":{"type":"array","items":{"type":"string","enum":["multiDayPasses","memberships","annualPasses","multiAttractionProducts","packages","storedEntitlements"]},"description":"Products this policy applies to"},"proRataMethod":{"type":"string","enum":["timeBased","usageBased","valueBased","entitlementBased","fixedCredit"],"description":"Remaining days over original days; remaining uses over total uses; remaining commercial value; value of unconsumed benefits; or a configured fixed amount"},"fixedCreditAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"For fixedCredit: the configured amount"},"maximumCreditPercent":{"type":"number","description":"Maximum credit, percent of the original value"},"minimumUpgradeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Minimum upgrade amount"},"creditExpiryDays":{"type":"integer","description":"Days the credit stays usable"},"nonCreditableComponents":{"type":"array","items":{"type":"string"},"description":"Components that earn no credit"},"excludeFees":{"type":"boolean","description":"Fees are not credited"},"taxTreatment":{"type":"string","description":"How tax on the credit is treated"},"negativeDifferenceTreatment":{"type":"string","enum":["noRefund","refundDifference","walletCredit","voucherCredit","supervisorApproval"],"description":"When the target is worth less than the credit. No package default: the venue chooses when it enables downgrades"}}},
"ProRataResidualValueEntitlementCreditConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Pro-Rata, Residual Value & Entitlement Credit Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"appliesTo":{"type":"array","items":{"type":"string","enum":["multiDayPasses","memberships","annualPasses","multiAttractionProducts","packages","storedEntitlements"]},"description":"Products this policy applies to"},"proRataMethod":{"type":"string","enum":["timeBased","usageBased","valueBased","entitlementBased","fixedCredit"],"description":"Remaining days over original days; remaining uses over total uses; remaining commercial value; value of unconsumed benefits; or a configured fixed amount"},"fixedCreditAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"For fixedCredit: the configured amount"},"maximumCreditPercent":{"type":"number","description":"Maximum credit, percent of the original value"},"minimumUpgradeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Minimum upgrade amount"},"creditExpiryDays":{"type":"integer","description":"Days the credit stays usable"},"nonCreditableComponents":{"type":"array","items":{"type":"string"},"description":"Components that earn no credit"},"excludeFees":{"type":"boolean","description":"Fees are not credited"},"taxTreatment":{"type":"string","description":"How tax on the credit is treated"},"negativeDifferenceTreatment":{"type":"string","enum":["noRefund","refundDifference","walletCredit","voucherCredit","supervisorApproval"],"description":"When the target is worth less than the credit. No package default: the venue chooses when it enables downgrades"}}},
"UpgradeConversionCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Upgrade & Conversion Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"activeUpgradePaths":{"type":"integer","description":"Active Upgrade Paths"},"activeConversionRules":{"type":"integer","description":"Active Conversion Rules"},"productsEligibleForUpgrade":{"type":"string","description":"Products Eligible for Upgrade"},"productsExcluded":{"type":"string","description":"Products Excluded"},"upgradesToday":{"type":"string","description":"Upgrades Today"},"conversionsToday":{"type":"string","description":"Conversions Today"},"pendingExceptions":{"type":"integer","description":"Pending Exceptions"},"failedConversions":{"type":"integer","description":"Failed Conversions"},"expiringRules":{"type":"integer","description":"Expiring Rules"},"configurationConflicts":{"type":"integer","description":"Configuration Conflicts"},"manualOverrides":{"type":"integer","description":"Manual Overrides"},"ruleId":{"type":"string","description":"Rule ID"},"ruleName":{"type":"string","description":"Rule Name"},"sourceProduct":{"type":"string","description":"Source Product"},"targetProduct":{"type":"string","description":"Target Product"},"transactionType":{"type":"string","enum":["upgrade","downgrade","exchange","conversion","personTypeConversion","productConversion"],"description":"Transaction type"},"venue":{"type":"string","description":"Venue"},"channel":{"type":"string","description":"Channel"},"effectivePeriod":{"type":"string","format":"date-time","description":"Effective Period"},"financialMethod":{"type":"string","description":"Financial Method"},"approvalRequirement":{"type":"string","description":"Approval Requirement"},"status":{"type":"string","description":"Status"},"owner":{"type":"string","description":"Owner"}}},
"UpgradeConversionPathBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; lands in `orders.upgrade_rule` (DM5, 29 September)","description":"**What Upgrade & Conversion Path Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"pathName":{"type":"string","description":"Path name"},"pathCode":{"type":"string","description":"Path code"},"sourceProduct":{"type":"string","description":"Source product"},"targetProduct":{"type":"string","description":"Target product"},"transactionType":{"type":"string","enum":["upgrade","downgrade","exchange","conversion","personTypeConversion","productConversion"],"description":"Transaction type"},"venue":{"type":"string","description":"Venue"},"event":{"type":"string","description":"Event"},"performance":{"type":"string","description":"Performance"},"effectiveFrom":{"type":"string","format":"date-time","description":"Effective from"},"effectiveTo":{"type":"string","format":"date-time","description":"Effective to"},"allowedChannels":{"type":"array","items":{"type":"string"},"description":"Allowed channels"},"customerSegment":{"type":"string","description":"Customer segment"},"active":{"type":"boolean","description":"Whether the path is in use"},"direction":{"type":"string","enum":["oneWay","bidirectional"],"description":"One-way, or bidirectional where commercially permitted"},"chainedUpgradeAllowed":{"type":"boolean","description":"Whether this path may chain into a further upgrade (Standard to Premium to VIP)"}}},
"UpgradeConversionPathBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Upgrade & Conversion Path Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"pathName":{"type":"string","description":"Path name"},"pathCode":{"type":"string","description":"Path code"},"sourceProduct":{"type":"string","description":"Source product"},"targetProduct":{"type":"string","description":"Target product"},"transactionType":{"type":"string","enum":["upgrade","downgrade","exchange","conversion","personTypeConversion","productConversion"],"description":"Transaction type"},"venue":{"type":"string","description":"Venue"},"event":{"type":"string","description":"Event"},"performance":{"type":"string","description":"Performance"},"effectiveFrom":{"type":"string","format":"date-time","description":"Effective from"},"effectiveTo":{"type":"string","format":"date-time","description":"Effective to"},"allowedChannels":{"type":"array","items":{"type":"string"},"description":"Allowed channels"},"customerSegment":{"type":"string","description":"Customer segment"},"active":{"type":"boolean","description":"Whether the path is in use"},"direction":{"type":"string","enum":["oneWay","bidirectional"],"description":"One-way, or bidirectional where commercially permitted"},"chainedUpgradeAllowed":{"type":"boolean","description":"Whether this path may chain into a further upgrade (Standard to Premium to VIP)"}}},
"UpgradeEligibilityQualificationRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Upgrade Eligibility & Qualification Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ticketStatus":{"type":"string","description":"Ticket Status"},"product":{"type":"string","description":"Product"},"ticketType":{"type":"string","description":"Ticket Type"},"event":{"type":"string","description":"Event"},"performance":{"type":"string","description":"Performance"},"visitDate":{"type":"string","format":"date-time","description":"Visit Date"},"timeslot":{"type":"string","description":"Timeslot"},"customerType":{"type":"string","description":"Customer Type"},"customerSegment":{"type":"string","description":"Customer Segment"},"membership":{"type":"string","description":"Membership"},"loyaltyTier":{"type":"string","description":"Loyalty Tier"},"channel":{"type":"string","description":"Channel"},"venue":{"type":"string","description":"Venue"},"location":{"type":"string","description":"Location"},"purchaseDate":{"type":"string","format":"date-time","description":"Purchase Date"},"purchaseChannel":{"type":"string","description":"Purchase Channel"},"originalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Original Price"},"promotionUsed":{"type":"string","description":"Promotion Used"},"usageStatus":{"type":"string","description":"Usage Status"},"previousUpgrade":{"type":"string","description":"Previous Upgrade"},"previousConversion":{"type":"number","description":"Previous Conversion"},"redemptionHistory":{"type":"string","description":"Redemption History"},"eligibleTicketStatuses":{"type":"array","items":{"type":"string","enum":["valid","unused","partiallyUsed","expired","cancelled","suspended"]},"description":"Ticket statuses from which the upgrade is allowed."},"ineligibilityReason":{"type":"string","description":"Why a ticket is not eligible, shown to staff and guest"}}},
"UpgradeExecutionCredentialRegenerationChannelControlInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; the execution lands in `orders.upgrade`, the credential treatment and channels come from `orders.upgrade_rule` (DM5, 29 September)","description":"**What Upgrade Execution, Credential Regeneration & Channel Controls submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"newEntitlement":{"type":"integer","description":"New Entitlement"},"newAccessRights":{"type":"integer","description":"New Access Rights"},"newZone":{"type":"integer","description":"New Zone"},"newDate":{"type":"string","format":"date-time","description":"New Date"},"newPerformance":{"type":"integer","description":"New Performance"},"oldCredentialInvalidation":{"type":"string","description":"Old Credential Invalidation"},"credentialTreatment":{"type":"string","enum":["regenerateQr","invalidateOldQr","preserveExistingCredential"],"description":"What happens to the credential."},"availableChannels":{"type":"array","items":{"type":"string","enum":["b2cSelfService","mobileApp","pos","callCenter","boxOffice","kiosk","b2b","reseller","api"]},"description":"Channels the upgrade is available through. The guest app and web are included (MoM 1 Sep)."},"generatedDocuments":{"type":"array","items":{"type":"string","enum":["updatedTicket","updatedReceipt","updatedInvoice","confirmationEmail","smsWhatsapp","walletPassUpdate"]},"description":"What execution produces."}}},
"UpgradeExecutionCredentialRegenerationChannelControlView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Upgrade Execution, Credential Regeneration & Channel Controls displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"newEntitlement":{"type":"integer","description":"New Entitlement"},"newAccessRights":{"type":"integer","description":"New Access Rights"},"newZone":{"type":"integer","description":"New Zone"},"newDate":{"type":"string","format":"date-time","description":"New Date"},"newPerformance":{"type":"integer","description":"New Performance"},"oldCredentialInvalidation":{"type":"string","description":"Old Credential Invalidation"},"credentialTreatment":{"type":"string","enum":["regenerateQr","invalidateOldQr","preserveExistingCredential"],"description":"What happens to the credential."},"availableChannels":{"type":"array","items":{"type":"string","enum":["b2cSelfService","mobileApp","pos","callCenter","boxOffice","kiosk","b2b","reseller","api"]},"description":"Channels the upgrade is available through. The guest app and web are included (MoM 1 Sep)."},"generatedDocuments":{"type":"array","items":{"type":"string","enum":["updatedTicket","updatedReceipt","updatedInvoice","confirmationEmail","smsWhatsapp","walletPassUpdate"]},"description":"What execution produces."}}},
"UpgradeFinancialTreatmentPriceDifferenceRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Upgrade Financial Treatment & Price Difference Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"targetPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Target Price"},"credit":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Credit"},"priceDifference":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price Difference"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount"},"fees":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fees"},"tax":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Tax"},"rounding":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Rounding"},"finalAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Final Amount"},"priceSource":{"type":"string","enum":["currentSellingPrice","originalDatePrice","upgradeSpecificRate","contractedRate","membershipRate","fixedUpgradePrice"],"description":"Price the target is valued at."},"carryForwardDiscounts":{"type":"array","items":{"type":"string","enum":["promotion","membershipDiscount","voucher","corporateDiscount"]},"description":"Existing discounts carried into the upgrade."},"financialMethod":{"type":"string","enum":["fullDifference","fixedUpgradeFee","percentageUpgrade","proRata","creditBased","noCredit","complimentary"],"description":"Financial method: target price less eligible original value; a fixed fee; a percentage of target; pro-rata on remaining validity; original value as credit; no credit; or complimentary where authorised"},"dynamicPriceTreatment":{"type":"string","enum":["currentDynamicPrice","protectedUpgradeRate","configuredRate"],"description":"When the target is dynamically priced, which rate the upgrade uses"}}},
"UpgradeHistoryExceptionManagementAuditExplorerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Upgrade History, Exception Management & Audit Explorer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"transactionId":{"type":"string","description":"Transaction ID"},"originalTicket":{"type":"string","description":"Original Ticket"},"newTicket":{"type":"integer","description":"New Ticket"},"sourceProduct":{"type":"string","description":"Source Product"},"targetProduct":{"type":"string","description":"Target Product"},"customer":{"type":"string","description":"Customer"},"order":{"type":"string","description":"Order"},"transactionType":{"type":"string","description":"Transaction Type"},"originalValue":{"type":"string","description":"Original Value"},"eligibleCredit":{"type":"string","description":"Eligible Credit"},"priceDifference":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price Difference"},"fees":{"type":"string","description":"Fees"},"tax":{"type":"string","description":"Tax"},"paymentRefund":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Payment/Refund"},"channel":{"type":"string","description":"Channel"},"agent":{"type":"string","description":"Agent"},"dateTime":{"type":"string","format":"date-time","description":"Date/Time"},"rule":{"type":"string","description":"Rule"},"status":{"type":"string","description":"Status"},"reason":{"type":"string","description":"Reason"},"user":{"type":"string","description":"User"},"role":{"type":"string","description":"Role"},"approval":{"type":"string","description":"Approval"},"supportingNote":{"type":"string","description":"Supporting Note"},"timestamp":{"type":"string","format":"date-time","description":"Timestamp"},"exceptionType":{"type":"string","enum":["eligibilityOverride","financialOverride","expiredTicketException","manualCredit","complimentaryUpgrade","failedCredentialUpdate","failedPaymentReconciliation","channelSynchronizationFailure"],"description":"Exception or override."}}},
"UpgradeTimingUsageTicketStatusRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Upgrade Timing, Usage & Ticket Status Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"partiallyConsumed":{"type":"string","description":"Partially Consumed"},"usedAdmissions":{"type":"string","description":"Used Admissions"},"unusedAdmissions":{"type":"string","description":"Unused Admissions"},"remainingDays":{"type":"string","description":"Remaining Days"},"remainingStoredValue":{"type":"string","description":"Remaining Stored Value"},"remainingBenefits":{"type":"string","description":"Remaining Benefits"},"neverEligible":{"type":"string","description":"Never Eligible"},"supervisorExceptionAllowed":{"type":"boolean","description":"Supervisor Exception Allowed"},"permittedWindows":{"type":"array","items":{"type":"string","enum":["beforeFirstUse","afterFirstUse","beforeVisit","duringVisit","afterVisit","beforeExpiry","gracePeriod"]},"description":"When the upgrade is allowed."},"originalTicketTreatment":{"type":"string","enum":["invalidate","supersede","retainForHistory","partiallyRetainEntitlement"],"description":"What happens to the original ticket."}}}
}
```
