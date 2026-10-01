# WS100 — Subscription Licensing AI Self Service board 3

**10 screens · 0 operations · 0 schemas · 0 permissions**

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

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
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
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/commercial-rules-engine-overview-adm-389` |

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
| Empty, first run (`?state=emptyFirstRun`) | No commercial rules overview yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial rules overview are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

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
- [ ] Sign-in is asked only where the spec asks for it.
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
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration Fields) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/vsi-model-builder-adm-390` |

**Known gaps.** **VSI Model Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations …

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

#### Permissions

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
- [ ] Sign-in is asked only where the spec asks for it.
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
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/vsi-scoring-tier-threshold-configuration-adm-391` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

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

#### Permissions

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
- [ ] Sign-in is asked only where the spec asks for it.
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
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/subscription-tier-configuration-adm-392` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

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

#### Permissions

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

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-392?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create plan, Cancel.
- [ ] Every transition is wired: `ADM-389`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-393` Tier Included Allowances

**Configure the resources included within each standard subscription tier.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration per Allowance) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/tier-included-allowances-adm-393` |

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

#### Permissions

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
- [ ] Sign-in is asked only where the spec asks for it.
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
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Commercial Configuration Fields; Separately configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/commercial-licensing-model-configuration-adm-394` |

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

#### Permissions

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
- [ ] Sign-in is asked only where the spec asks for it.
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
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration should support; Commercial rule can specify; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/billable-unit-minimum-guarantee-enforcement-rules-adm-395` |

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

#### Permissions

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
- [ ] Sign-in is asked only where the spec asks for it.
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
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Pack Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/overage-pricing-capacity-packs-adm-396` |

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

#### Permissions

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
- [ ] Sign-in is asked only where the spec asks for it.
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
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/commercial-model-rule-simulation-adm-397` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

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

**Where the user goes next**

- → `ADM-389` Commercial Rules Engine Overview: *Back to Commercial Rules Engine Overview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial model rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial model rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial model rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial model rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

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
- [ ] Sign-in is asked only where the spec asks for it.
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
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `planId` (navigation) |
| Route | `/tenants-licensing/rule-versioning-approval-publication-adm-398` |

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Revised Board 3 — Critical Architecture, 1. Operational Classification. Each needs an operation, or needs … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Revised Board 3 — Critical Architecture (primary button) | navigation or local | — | — | — | — |
| 1. Operational Classification (secondary button) | navigation or local | — | — | — | — |

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

#### Permissions

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

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-398?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Revised Board 3 — Critical Architecture, 1. Operational Classification.
- [ ] Every transition is wired: `ADM-389`.
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

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{

}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{

}
```
