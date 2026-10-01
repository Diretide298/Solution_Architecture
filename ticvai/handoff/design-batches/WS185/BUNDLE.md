# WS185 — Upsell,CrossSellEngine board 6

**10 screens · 8 operations · 4 schemas · 3 permissions**

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
  `AI_USE, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `ADM-689` | Recommendation Performance Command Center | B–D | 2 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `ADM-690` | Recommendation Strategy & Placement Analytics | B–D | 0 | 30 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `ADM-691` | Recommendation Experiment & A/B Test Studio | B–D | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-692` | Experiment Results & Winner Decision Workspace | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-693` | Recommendation Attribution & Incrementality Analytics | B–D | 5 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `ADM-694` | AI Model Performance & Drift Monitor | B–D | 0 | 24 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `ADM-695` | Recommendation Governance & Deployment Control | B–D | 0 | 2 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-696` | AI Risk, Fairness, Explainability & Safety Center | B–D | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-697` | Recommendation Audit, Decision Trace & Investigation | B–D | 2 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-698` | AI Optimization & Recommendation Intelligence Lab | B–D | 0 | 2 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-690, ADM-694, ADM-697 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-689` Recommendation Performance Command Center

**Provide executive and operational visibility across the complete Recommendation Engine.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/recommendation-performance-command-center-adm-689` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search recommendation performance | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by upsell, cross-sell, membership, bundle, f&b, retail and 5 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getRecommendationPerformance` ?from |
| To | date and time picker | — | — | `getRecommendationPerformance` ?to |
| Group by | radio group | — | Strategy · Placement · Channel · Product · Experiment | `getRecommendationPerformance` ?groupBy |

#### Outputs: what the screen shows and produces

**Shown**

**Recommendations Generated** (metric tile)

**Recommendations Presented** (metric tile)

**Recommendations Accepted** (metric tile)

**Recommendation Conversion** (metric tile)

**Upsell Revenue** (metric tile)

**Cross-Sell Revenue** (metric tile)

**Estimated Incremental Revenue** (metric tile)

**AOV Uplift** (metric tile)

**Attach Rate** (metric tile)

**Incremental Margin** (metric tile)

**AI Recommendation Share** (metric tile)

**Rule-Based Recommendation Share** (metric tile)

**Suppression Rate** (metric tile)

**Active Experiments** (metric tile)

**Model Health** (metric tile)

**Data it reads**: `getRecommendationPerformance` (onLoad, The headline numbers)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-690` Recommendation Strategy & Placement Analytics: *Recommendation Strategy & Placement Analytics*
- → `ADM-691` Recommendation Experiment & A/B Test Studio: *Recommendation Experiment & A/B Test Studio*
- → `ADM-692` Experiment Results & Winner Decision Workspace: *Experiment Results & Winner Decision Workspace*
- → `ADM-693` Recommendation Attribution & Incrementality Analytics: *Recommendation Attribution & Incrementality Analytics*
- → `ADM-694` AI Model Performance & Drift Monitor: *AI Model Performance & Drift Monitor*
- → `ADM-695` Recommendation Governance & Deployment Control: *Recommendation Governance & Deployment Control*
- → `ADM-696` AI Risk, Fairness, Explainability & Safety Center: *AI Risk, Fairness, Explainability & Safety Center*
- → `ADM-697` Recommendation Audit, Decision Trace & Investigation: *Recommendation Audit, Decision Trace & Investigation*
- → `ADM-698` AI Optimization & Recommendation Intelligence Lab: *AI Optimization & Recommendation Intelligence Lab*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation performance list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation performance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation performance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getRecommendationPerformance` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.21 | System shall support recommendation performance analytics. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |
| 8.6.27 | System shall support recommendation dashboards. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |
| 8.6.28 | System shall support recommendation reporting. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-689` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-689`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 1: Opens Recommendation Performance Command Center → Provide executive and operational visibility across the complete Recommendation Engine.
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F292 branch at step 1 (expected): when Nothing has been set up on Recommendation Performance Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F292 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-689?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-690`, `ADM-691`, `ADM-692`, `ADM-693`, `ADM-694`, `ADM-695`, `ADM-696`, `ADM-697`, `ADM-698`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-690` Recommendation Strategy & Placement Analytics

**Determine which recommendation strategies, placements, channels and journey stages perform best.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Compare) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/recommendation-strategy-placement-analytics-adm-690` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getRecommendationPerformance` ?from |
| To | date and time picker | — | — | `getRecommendationPerformance` ?to |
| Group by | radio group | — | Strategy · Placement · Channel · Product · Experiment | `getRecommendationPerformance` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every recommendation strategy placement** (data table)

| Shows | Format | Notes |
|---|---|---|
| Ticket selection | text | not in the schema: `Ticket Selection` |
| Cart | text | not in the schema: `Cart` |
| Checkout | text | not in the schema: `Checkout` |
| Confirmation | text | not in the schema: `Confirmation` |
| Pre visit | text | not in the schema: `Pre-Visit` |
| Mobile app | text | not in the schema: `Mobile App` |
| In venue | text | not in the schema: `In-Venue` |
| Post visit | text | not in the schema: `Post-Visit` |
| B2 c | text | not in the schema: `B2C` |
| App | text | not in the schema: `App` |
| POS | text | not in the schema: `POS` |
| Kiosk | text | not in the schema: `Kiosk` |
| B2 b | text | not in the schema: `B2B` |
| Call center | text | not in the schema: `Call Center` |
| Api/partner | text | not in the schema: `API/Partner` |

**The selected recommendation strategy placement** (detail panel): The pack groups this record's detail under its own headings: “Strategy”, “Max”, “Relevance”, “Cart conversion”, “Checkout conversion”.

| Shows | Format | Notes |
|---|---|---|
| Ticket selection | text | not in the schema: `Ticket Selection` |
| Cart | text | not in the schema: `Cart` |
| Checkout | text | not in the schema: `Checkout` |
| Confirmation | text | not in the schema: `Confirmation` |
| Pre visit | text | not in the schema: `Pre-Visit` |
| Mobile app | text | not in the schema: `Mobile App` |
| In venue | text | not in the schema: `In-Venue` |
| Post visit | text | not in the schema: `Post-Visit` |
| B2 c | text | not in the schema: `B2C` |
| App | text | not in the schema: `App` |
| POS | text | not in the schema: `POS` |
| Kiosk | text | not in the schema: `Kiosk` |
| B2 b | text | not in the schema: `B2B` |
| Call center | text | not in the schema: `Call Center` |
| Api/partner | text | not in the schema: `API/Partner` |

**Data it reads**: `getRecommendationPerformance` (onLoad, By strategy and placement)

**Where the user goes next**

- → `ADM-689` Recommendation Performance Command Center: *Back to Recommendation Performance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation strategy placement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation strategy placement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation strategy placement yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation strategy placement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getRecommendationPerformance` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.21 | System shall support recommendation performance analytics. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |
| 8.6.27 | System shall support recommendation dashboards. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |
| 8.6.28 | System shall support recommendation reporting. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-690` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-690`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 2: Works in Recommendation Strategy & Placement Analytics → Determine which recommendation strategies, placements, channels and journey stages perform best.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-690?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-689`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-691` Recommendation Experiment & A/B Test Studio

**Allow TICVAI to scientifically test recommendation strategies rather than relying only on assumptions. Increase Family Meal cross-sell.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Measure) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/recommendation-experiment-a-b-test-studio-adm-691` |

**Known gaps.** **Recommendation Experiment & A/B Test Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Conversion** (metric tile)

**Attach rate** (metric tile)

**Revenue** (metric tile)

**Incremental revenue** (metric tile)

**AOV** (metric tile)

**Margin** (metric tile)

**Customer response** (metric tile)

**Recommendation fatigue** (metric tile)

**Data it reads**: `listRecommendationExperiments` (onLoad, Experiments running)

**Where the user goes next**

- → `ADM-689` Recommendation Performance Command Center: *Back to Recommendation Performance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation experiment test list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation experiment test untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation experiment test yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation experiment test are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listRecommendationExperiments` → `PRODUCT_VIEW` (read) · staff
- `createRecommendationExperiment` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.24 | System shall support recommendation A/B testing. | Unified Operations Dashboard | CONTRACTED | `createRecommendationExperiment` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-691` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-691`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 4: Works in Recommendation Experiment & A/B Test Studio → Allow TICVAI to scientifically test recommendation strategies rather than relying only on assumptions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-691?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-689`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-692` Experiment Results & Winner Decision Workspace

**Evaluate experiments and decide whether a recommendation strategy should be deployed.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `experimentId` (navigation) |
| Route | `/commercial/experiment-results-winner-decision-workspace-adm-692` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Declare Winner, Extend Test, Stop Test, Reject Result, Create Deployment Draft, Send for Approval. Each needs attaching to the control it gates, or the screen needs the control.

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listRecommendationExperiments` (onLoad, Results so far)

**Where the user goes next**

- → `ADM-689` Recommendation Performance Command Center: *Back to Recommendation Performance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The experiment results winner list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the experiment results winner untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No experiment results winner yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the experiment results winner are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `winningVariant` does not name one of the experiment's own variants.; 409 The experiment is not `running`. A draft never ran, and a concluded or abandoned experiment already has its outcome. |

#### Permissions

- `listRecommendationExperiments` → `PRODUCT_VIEW` (read) · staff
- `concludeRecommendationExperiment` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-692` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-692`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 6: Works in Experiment Results & Winner Decision Workspace → Evaluate experiments and decide whether a recommendation strategy should be deployed.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-692?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-689`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-693` Recommendation Attribution & Incrementality Analytics

**Determine whether a recommendation genuinely created additional commercial value. This is essential. A customer purchasing a recommended product does not automatically mean the recommendation caused the purchase.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/recommendation-attribution-incrementality-analytics-adm-693` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Recommendation tracking ID, Last recommendation, First recommendation, A/B experiment. Each needs an …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Same session | select field | — | — | — | — | — | — |
| 24 hours | select field | — | — | — | — | — | — |
| 7 days | select field | — | — | — | — | — | — |
| Until visit | select field | — | — | — | — | — | — |
| Custom | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getRecommendationPerformance` ?from |
| To | date and time picker | — | — | `getRecommendationPerformance` ?to |
| Group by | radio group | — | Strategy · Placement · Channel · Product · Experiment | `getRecommendationPerformance` ?groupBy |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Recommendation tracking ID (primary button) | navigation or local | — | — | — | — |
| Last recommendation (secondary button) | navigation or local | — | — | — | — |
| First recommendation (secondary button) | navigation or local | — | — | — | — |
| A/B experiment (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getRecommendationPerformance` (onLoad, Attributed against incremental)

**Where the user goes next**

- → `ADM-689` Recommendation Performance Command Center: *Back to Recommendation Performance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation attribution incrementality configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation attribution incrementality untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation attribution incrementality configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getRecommendationPerformance` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.21 | System shall support recommendation performance analytics. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |
| 8.6.27 | System shall support recommendation dashboards. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |
| 8.6.28 | System shall support recommendation reporting. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-693` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-693`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 8: Works in Recommendation Attribution & Incrementality Analytics → Determine whether a recommendation genuinely created additional commercial value. This is essential. A customer purchasing a recommended product does not automatically mean the recommendation caused …

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-693?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Recommendation tracking ID, Last recommendation, First recommendation, A/B experiment.
- [ ] Every transition is wired: `ADM-689`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-694` AI Model Performance & Drift Monitor

**Monitor whether recommendation and propensity models continue performing correctly after deployment. This screen is critical if TICVAI wants a serious AI architecture.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show; Detect) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/ai-model-performance-drift-monitor-adm-694` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getRecommendationPerformance` ?from |
| To | date and time picker | — | — | `getRecommendationPerformance` ?to |
| Group by | radio group | — | Strategy · Placement · Channel · Product · Experiment | `getRecommendationPerformance` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every model performance drift** (data table)

| Shows | Format | Notes |
|---|---|---|
| Model | text | not in the schema: `Model` |
| Version | text | not in the schema: `Version` |
| Purpose | text | not in the schema: `Purpose` |
| Deployment date | text | not in the schema: `Deployment date` |
| Status | text | not in the schema: `Status` |
| Last evaluation | text | not in the schema: `Last evaluation` |
| Data freshness | text | not in the schema: `Data freshness` |
| Input drift | text | not in the schema: `Input drift` |
| Behavioral drift | text | not in the schema: `Behavioral drift` |
| Performance drift | text | not in the schema: `Performance drift` |
| Segment drift | text | not in the schema: `Segment drift` |
| Product mix change | text | not in the schema: `Product mix change` |

**The selected model performance drift** (detail panel): The pack groups this record's detail under its own headings: “Models Could Include”.

| Shows | Format | Notes |
|---|---|---|
| Model | text | not in the schema: `Model` |
| Version | text | not in the schema: `Version` |
| Purpose | text | not in the schema: `Purpose` |
| Deployment date | text | not in the schema: `Deployment date` |
| Status | text | not in the schema: `Status` |
| Last evaluation | text | not in the schema: `Last evaluation` |
| Data freshness | text | not in the schema: `Data freshness` |
| Input drift | text | not in the schema: `Input drift` |
| Behavioral drift | text | not in the schema: `Behavioral drift` |
| Performance drift | text | not in the schema: `Performance drift` |
| Segment drift | text | not in the schema: `Segment drift` |
| Product mix change | text | not in the schema: `Product mix change` |

**Data it reads**: `getRecommendationPerformance` (onLoad, Model performance over time)

**Where the user goes next**

- → `ADM-689` Recommendation Performance Command Center: *Back to Recommendation Performance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The model performance drift list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the model performance drift untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No model performance drift yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the model performance drift are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getRecommendationPerformance` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.21 | System shall support recommendation performance analytics. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |
| 8.6.27 | System shall support recommendation dashboards. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |
| 8.6.28 | System shall support recommendation reporting. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-694` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-694`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 10: Works in AI Model Performance & Drift Monitor → Monitor whether recommendation and propensity models continue performing correctly after deployment. This screen is critical if TICVAI wants a serious AI architecture.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-694?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-689`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-695` Recommendation Governance & Deployment Control

**Control how new strategies, rules, models and AI changes move into production.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Monitor) and no metric row |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/recommendation-governance-deployment-control-adm-695` |

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Channel rollout, Venue rollout. Each needs an operation, or needs removing from the screen; this is the … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRecommendationStrategies` ?status |
| Placement | text field | — | — | `listRecommendationStrategies` ?placement |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every recommendation governance deployment** (data table)

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**The selected recommendation governance deployment** (detail panel): The pack groups this record's detail under its own headings: “Draft”, “Testing”, “Simulation”, “Approval”, “Scheduled”, “Active”.

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Channel rollout (primary button) | navigation or local | — | — | — | — |
| Venue rollout (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listRecommendationStrategies` (onLoad, What is deployed where)

**Where the user goes next**

- → `ADM-689` Recommendation Performance Command Center: *Back to Recommendation Performance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation governance deployment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation governance deployment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation governance deployment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation governance deployment are still there. The pack's own statuses are Recommendation strategy — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listRecommendationStrategies` → `PRODUCT_VIEW` (read) · staff
- `updateRecommendationStrategy` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-695` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-695`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 12: Works in Recommendation Governance & Deployment Control → Control how new strategies, rules, models and AI changes move into production.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-695?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Channel rollout, Venue rollout.
- [ ] Every transition is wired: `ADM-689`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-696` AI Risk, Fairness, Explainability & Safety Center

**Provide governance over how AI recommendation decisions behave across customer populations and business contexts.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `decisionId` (navigation) |
| Route | `/commercial/ai-risk-fairness-explainability-safety-center-adm-696` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Disable model, Disable recommendation type, Disable specific relationship, Raise confidence threshold … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Disable model (destructive button) | navigation or local | — | — | — | — |
| Disable recommendation type (destructive button) | navigation or local | — | — | — | — |
| Disable specific relationship (destructive button) | navigation or local | — | — | — | — |
| Raise confidence threshold (secondary button) | navigation or local | — | — | — | — |
| Emergency suspend (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-689` Recommendation Performance Command Center: *Back to Recommendation Performance Command Center*

**What opens over it**

- confirmDialog *Disable model*: **Disable model on a risk fairness explainability is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *Disable recommendation type*: **Disable recommendation type on a risk fairness explainability is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *Disable specific relationship*: **Disable specific relationship on a risk fairness explainability is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The risk fairness explainability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the risk fairness explainability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No risk fairness explainability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the risk fairness explainability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `explainRecommendationDecision` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.20 | System shall support recommendation explainability. | Unified Operations Dashboard | CONTRACTED | `explainRecommendationDecision` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-696` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-696`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 14: Works in AI Risk, Fairness, Explainability & Safety Center → Provide governance over how AI recommendation decisions behave across customer populations and business contexts.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-696?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Disable model, Disable recommendation type, Disable specific relationship, Raise confidence threshold, Emergency suspend.
- [ ] Every transition is wired: `ADM-689`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-697` Recommendation Audit, Decision Trace & Investigation

**Provide transaction-level explainability for Customer Service, Commercial, Audit, and technical investigation.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `decisionId` (navigation) |
| Route | `/commercial/recommendation-audit-decision-trace-investigation-adm-697` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search recommendation audit decision | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by recommendation id, transaction, customer/session where permitted, ticket, product, date and 3 more — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-689` Recommendation Performance Command Center: *Back to Recommendation Performance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation audit decision list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation audit decision untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation audit decision yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation audit decision are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `explainRecommendationDecision` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.20 | System shall support recommendation explainability. | Unified Operations Dashboard | CONTRACTED | `explainRecommendationDecision` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-697` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-697`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 16: Works in Recommendation Audit, Decision Trace & Investigation → Provide transaction-level explainability for Customer Service, Commercial, Audit, and technical investigation.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-697?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-689`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-698` AI Optimization & Recommendation Intelligence Lab

**Turn all Recommendation Engine data into actionable improvement opportunities. This is the final optimization screen for Module 2.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track; Measure) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/ai-optimization-recommendation-intelligence-lab-adm-698` |

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 0 operations.** Unserved: Simulate, Create Experiment, Create Draft, Send for Approval, Dismiss, Snooze. Each needs an operation, or … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every optimization recommendation intelligence** (data table)

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**The selected optimization recommendation intelligence** (detail panel): The pack groups this record's detail under its own headings: “Product Relationships”, “Ranking”, “Journey”, “Timing”, “Suppression”, “Strategy”.

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Simulate (primary button) | navigation or local | — | — | — | — |
| Create Experiment (secondary button) | navigation or local | — | — | — | — |
| Create Draft (secondary button) | navigation or local | — | — | — | — |
| Send for Approval (secondary button) | navigation or local | — | — | — | — |
| Dismiss (secondary button) | navigation or local | — | — | — | — |
| Snooze (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-689` Recommendation Performance Command Center: *Back to Recommendation Performance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The optimization recommendation intelligence list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the optimization recommendation intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No optimization recommendation intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the optimization recommendation intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `simulateRecommendationStrategy` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-698` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-698`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 18: Works in AI Optimization & Recommendation Intelligence Lab → Turn all Recommendation Engine data into actionable improvement opportunities. This is the final optimization screen for Module 2.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-698?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Simulate, Create Experiment, Create Draft, Send for Approval, Dismiss, Snooze.
- [ ] Every transition is wired: `ADM-689`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
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

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"concludeRecommendationExperiment": {"method":"POST","path":"/recommendation-experiments/{experimentId}/conclude","contract":"promotions","summary":"Declare a winner and roll it out","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RecommendationExperiment"},
"createRecommendationExperiment": {"method":"POST","path":"/recommendation-experiments","contract":"promotions","summary":"Split traffic between strategies","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RecommendationExperiment","responds":"RecommendationExperiment"},
"explainRecommendationDecision": {"method":"GET","path":"/recommendations/decisions/{decisionId}/explanation","contract":"ai","summary":"Why these recommendations","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"depth","in":"query","required":null}],"requestBody":null,"responds":"AiRecommendationExplanation"},
"getRecommendationPerformance": {"method":"GET","path":"/recommendation-performance","contract":"promotions","summary":"Impressions, acceptance, revenue and incremental lift","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"RecommendationPerformance"},
"listRecommendationExperiments": {"method":"GET","path":"/recommendation-experiments","contract":"promotions","summary":"A/B tests on placements and strategies","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RecommendationExperiment"},
"listRecommendationStrategies": {"method":"GET","path":"/recommendation-strategies","contract":"promotions","summary":"The strategies deciding what gets offered where","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"placement","in":"query","required":null}],"requestBody":null,"responds":"RecommendationStrategy"},
"simulateRecommendationStrategy": {"method":"POST","path":"/recommendation-simulations","contract":"promotions","summary":"Replay a strategy against history before it goes live","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RecommendationPerformance"},
"updateRecommendationStrategy": {"method":"PUT","path":"/recommendation-strategies/{strategyId}","contract":"promotions","summary":"Change a strategy","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"RecommendationStrategy","responds":"RecommendationStrategy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiRecommendationExplanation": {"type":"object","x-ticvai-persistence":"none — built from ai.rec_decision and its decision record","description":"Why these items (AIR-193..202), at three depths each gated by permission (AIC-195): business, governance, technical.","required":["decisionId","depth"],"properties":{"decisionId":{"type":"string","format":"uuid"},"depth":{"type":"string","enum":["business","governance","technical"]},"funnel":{"type":"object","additionalProperties":true},"exclusions":{"type":"object","additionalProperties":true},"items":{"type":"array","items":{"type":"object","properties":{"trackingId":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid"},"reasons":{"type":"array","items":{"type":"string"}},"scoreBreakdown":{"type":"object","additionalProperties":true,"nullable":true}}}},"versions":{"type":"object","additionalProperties":true,"nullable":true,"description":"Strategy, model and feature-set versions. `technical` depth only."}}},
"RecommendationExperiment": {"type":"object","x-ticvai-persistence":"promotions.recommendation_experiment","description":"Boards 6.3 and 6.4. **Fixed allocation, explicit conclusion, and a holdout.**","required":["code","variants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"placement":{"type":"string","nullable":true},"variants":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"strategyId":{"type":"string","format":"uuid","nullable":true},"allocationPercent":{"type":"integer"}}}},"holdoutPercent":{"type":"integer","default":5},"primaryMetric":{"type":"string"},"minimumSampleSize":{"type":"integer","nullable":true},"startedAt":{"type":"string","format":"date-time","nullable":true},"endedAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["draft","running","concluded","abandoned"]},"winningVariant":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"RecommendationPerformance": {"type":"object","description":"Board 6.5. **Attributed and incremental reported apart** — the first flatters.","properties":{"key":{"type":"string"},"label":{"type":"string"},"impressions":{"type":"integer"},"clicks":{"type":"integer"},"accepted":{"type":"integer"},"acceptanceRate":{"type":"number"},"attributedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"holdoutAcceptanceRate":{"type":"number","nullable":true},"lift":{"type":"number","nullable":true}}},
"RecommendationStrategy": {"type":"object","x-ticvai-persistence":"promotions.recommendation_strategy","description":"Upsell board 1. **Objective, placement, ranking and guardrail in one record**, because any one of them alone produces a recommender that is either aimless or dangerous.\n","required":["code","name","objective"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"objective":{"type":"string","enum":["attachRevenue","averageOrderValue","upgradeRate","visitFrequency","inventoryBalance","guestSatisfaction"]},"kinds":{"type":"array","items":{"type":"string","enum":["upsell","upgrade","crossSell","bundle","nextBestOffer","reactivation"]}},"itemKinds":{"type":"array","description":"What the strategy may put in a slot (29 September, build pass, group G2, from group G1's handoff; 8.6.30 to 8.6.36, 5.4.21, 22.6.18): `product` (the default and the behaviour before), `offer` (a live promotion marked `recommendable`), `reward` (a marketing-crm loyalty reward the guest can redeem) and `challenge` (a challenge they can join). Mirrors `ai.decideRecommendations` item kinds.","default":["product"],"items":{"type":"string","enum":["product","offer","reward","challenge"]}},"placements":{"type":"array","description":"`homepage` (8.6.10) and `loyalty` (5.4.21, 22.6.18) added 29 September (build pass, group G2), matching the placements `ai.decideRecommendations` fills.","items":{"type":"string","enum":["productPage","cart","checkout","postPurchase","preVisitEmail","inVenueApp","kiosk","pos","signage","callCentre","homepage","loyalty"]}},"channels":{"type":"array","items":{"type":"string"}},"maxRecommendations":{"type":"integer","default":3,"description":"**A guardrail before it is a layout choice.** Nine upsells at checkout is not a denser page, it is an abandoned basket.\n"},"minConfidence":{"type":"number","nullable":true},"rankingWeights":{"type":"object","additionalProperties":{"type":"number"},"description":"Propensity, margin, inventory pressure, affinity, recency."},"requireAvailability":{"type":"boolean","default":true},"excludeInBasket":{"type":"boolean","default":true},"guardrails":{"type":"object","properties":{"maxDiscountPercent":{"type":"number","nullable":true},"minMarginPercent":{"type":"number","nullable":true},"neverRecommendCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requireHumanApproval":{"type":"boolean","default":false}}},"status":{"type":"string","enum":["draft","active","paused","retired"]},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"scopePath":{"type":"string"}}}
}
```
