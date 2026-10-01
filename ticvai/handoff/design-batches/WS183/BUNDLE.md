# WS183 — Upsell,CrossSellEngine board 4

**10 screens · 6 operations · 4 schemas · 3 permissions**

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
| `ADM-669` | Journey & Context Command Center | B–D | 0 | 0 | 6 | 3 | 0 | 6 | — | notStarted (—) |
| `ADM-670` | Customer Journey Map & Touchpoint Designer | B–D | 8 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `ADM-671` | Real-Time Context Rule Engine | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-672` | Pre-Purchase & Booking Journey Recommendation Manager | B–D | 6 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `ADM-673` | Post-Purchase & Pre-Visit Recommendation Manager | B–D | 5 | 0 | 6 | 0 | 0 | 4 | — | notStarted (—) |
| `ADM-674` | In-Venue & Location-Aware Recommendation Engine | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-675` | Visit State, Itinerary & Time-Aware Recommendation | B–D | 0 | 0 | 6 | 0 | 0 | 1 | — | notStarted (—) |
| `ADM-676` | Omnichannel Recommendation Synchronization | B–D | 0 | 14 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-677` | Contextual Trigger, Frequency & Experience Controls | B–D | 7 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-678` | Journey Simulator, Decision Trace & AI Optimization | B–D | 0 | 0 | 6 | 1 | 0 | 6 | — | notStarted (—) |

## Thin screens in this batch

**ADM-674, ADM-676, ADM-678 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-669` Journey & Context Command Center

**Provide centralized visibility into recommendation activity across the complete customer journey.**

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
| Route | `/commercial/journey-context-command-center-adm-669` |

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

**Active Journey Strategies** (metric tile)

**Active Touchpoints** (metric tile)

**Recommendation Sessions** (metric tile)

**Recommendations Presented** (metric tile)

**Acceptance Rate** (metric tile)

**Journey Conversion** (metric tile)

**Contextual Revenue** (metric tile)

**Post-Purchase Revenue** (metric tile)

**In-Venue Revenue** (metric tile)

**AOV Uplift** (metric tile)

**Suppressed Recommendations** (metric tile)

**AI Journey Opportunities** (metric tile)

**Data it reads**: `getRecommendationPerformance` (onLoad, By journey stage)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-670` Customer Journey Map & Touchpoint Designer: *Customer Journey Map & Touchpoint Designer*
- → `ADM-671` Real-Time Context Rule Engine: *Real-Time Context Rule Engine*
- → `ADM-672` Pre-Purchase & Booking Journey Recommendation Manager: *Pre-Purchase & Booking Journey Recommendation Manager*
- → `ADM-673` Post-Purchase & Pre-Visit Recommendation Manager: *Post-Purchase & Pre-Visit Recommendation Manager*
- → `ADM-674` In-Venue & Location-Aware Recommendation Engine: *In-Venue & Location-Aware Recommendation Engine*
- → `ADM-675` Visit State, Itinerary & Time-Aware Recommendation: *Visit State, Itinerary & Time-Aware Recommendation*
- → `ADM-676` Omnichannel Recommendation Synchronization: *Omnichannel Recommendation Synchronization*
- → `ADM-677` Contextual Trigger, Frequency & Experience Controls: *Contextual Trigger, Frequency & Experience Controls*
- → `ADM-678` Journey Simulator, Decision Trace & AI Optimization: *Journey Simulator, Decision Trace & AI Optimization*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The journey context list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the journey context untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No journey context yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the journey context are still there. Names the active filter and offers to clear it. |
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

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-669` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS181 Upsell,CrossSellEngine Board 4.dc.html#adm-669`
- Workshop pack: Upsell,CrossSellEngine.pdf board 4
- Flow F290 *Upsell,CrossSellEngine board 4: Journey & Context Command Center*, step 1: Opens Journey & Context Command Center → Provide centralized visibility into recommendation activity across the complete customer journey.
- Flow F290 *Upsell,CrossSellEngine board 4: Journey & Context Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F290 *Upsell,CrossSellEngine board 4: Journey & Context Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F290 *Upsell,CrossSellEngine board 4: Journey & Context Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F290 *Upsell,CrossSellEngine board 4: Journey & Context Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F290 *Upsell,CrossSellEngine board 4: Journey & Context Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F290 *Upsell,CrossSellEngine board 4: Journey & Context Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F290 *Upsell,CrossSellEngine board 4: Journey & Context Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F290 branch at step 1 (expected): when Nothing has been set up on Journey & Context Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F290 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-669?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-670`, `ADM-671`, `ADM-672`, `ADM-673`, `ADM-674`, `ADM-675`, `ADM-676`, `ADM-677`, `ADM-678`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-670` Customer Journey Map & Touchpoint Designer

**Allow TICVAI administrators to visually configure the customer journey and recommendation-enabled touchpoints.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§For each node configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/customer-journey-map-touchpoint-designer-adm-670` |

**Known gaps.** **Customer Journey Map & Touchpoint Designer declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Recommendations enabled | select field | — | — | — | — | — | — |
| Recommendation types | select field | — | — | — | — | — | — |
| Maximum recommendations | select field | — | — | — | — | — | — |
| Strategy | select field | — | — | — | — | — | — |
| Placement | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Ranking model | select field | — | — | — | — | — | — |
| Suppression policy | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRecommendationStrategies` ?status |
| Placement | text field | — | — | `listRecommendationStrategies` ?placement |

#### Outputs: what the screen shows and produces

**Data it reads**: `listRecommendationStrategies` (onLoad, Touchpoints in use)

**Where the user goes next**

- → `ADM-669` Journey & Context Command Center: *Back to Journey & Context Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer journey map configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer journey map untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer journey map configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listRecommendationStrategies` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-670` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS181 Upsell,CrossSellEngine Board 4.dc.html#adm-670`
- Workshop pack: Upsell,CrossSellEngine.pdf board 4
- Flow F290 *Upsell,CrossSellEngine board 4: Journey & Context Command Center*, step 2: Works in Customer Journey Map & Touchpoint Designer → Allow TICVAI administrators to visually configure the customer journey and recommendation-enabled touchpoints.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-670?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-669`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-671` Real-Time Context Rule Engine

**Determine recommendation behavior using the customer's current transactional and operational context.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/real-time-context-rule-engine-adm-671` |

**Known gaps.** **The pack names 9 actions on this screen and the screen declares 0 operations.** Unserved: Current product, Basket value, Guest count, Guest type, Current venue, Selected date, Selected timeslot … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Current product (primary button) | navigation or local | — | — | — | — |
| Basket value (secondary button) | navigation or local | — | — | — | — |
| Guest count (secondary button) | navigation or local | — | — | — | — |
| Guest type (secondary button) | navigation or local | — | — | — | — |
| Current venue (secondary button) | navigation or local | — | — | — | — |
| Selected date (secondary button) | navigation or local | — | — | — | — |
| Selected timeslot (secondary button) | navigation or local | — | — | — | — |
| Current channel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-669` Journey & Context Command Center: *Back to Journey & Context Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The real-time context rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the real-time context rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No real-time context rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the real-time context rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-671` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS181 Upsell,CrossSellEngine Board 4.dc.html#adm-671`
- Workshop pack: Upsell,CrossSellEngine.pdf board 4
- Flow F290 *Upsell,CrossSellEngine board 4: Journey & Context Command Center*, step 4: Works in Real-Time Context Rule Engine → Determine recommendation behavior using the customer's current transactional and operational context.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-671?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Current product, Basket value, Guest count, Guest type, Current venue, Selected date, Selected timeslot, Current channel.
- [ ] Every transition is wired: `ADM-669`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-672` Pre-Purchase & Booking Journey Recommendation Manager

**Manage recommendation behavior before transaction completion.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/pre-purchase-booking-journey-recommendation-manager-adm-672` |

**Known gaps.** **Pre-Purchase & Booking Journey Recommendation Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Recommendation count | select field | — | — | — | — | — | — |
| Recommendation category | select field | — | — | — | — | — | — |
| Ranking | select field | — | — | — | — | — | — |
| Display priority | select field | — | — | — | — | — | — |
| Frequency | select field | — | — | — | — | — | — |
| Suppression | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-669` Journey & Context Command Center: *Back to Journey & Context Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pre-purchase booking journey configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pre-purchase booking journey untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pre-purchase booking journey configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `updateRecommendationStrategy` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-672` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS181 Upsell,CrossSellEngine Board 4.dc.html#adm-672`
- Workshop pack: Upsell,CrossSellEngine.pdf board 4
- Flow F290 *Upsell,CrossSellEngine board 4: Journey & Context Command Center*, step 6: Works in Pre-Purchase & Booking Journey Recommendation Manager → Manage recommendation behavior before transaction completion.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-672?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-669`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-673` Post-Purchase & Pre-Visit Recommendation Manager

**Continue the commercial journey after payment while respecting the guest's existing purchase and visit plan.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/post-purchase-pre-visit-recommendation-manager-adm-673` |

**Known gaps.** **Post-Purchase & Pre-Visit Recommendation Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Immediately after purchase | select field | — | — | — | — | — | — |
| X days before visit | text field | — | — | — | — | — | — |
| X hours before visit | text field | — | — | — | — | — | — |
| Visit morning | select field | — | — | — | — | — | — |
| Before first redemption | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-669` Journey & Context Command Center: *Back to Journey & Context Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The post-purchase pre-visit recommendation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the post-purchase pre-visit recommendation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No post-purchase pre-visit recommendation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `updateRecommendationStrategy` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-673` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS181 Upsell,CrossSellEngine Board 4.dc.html#adm-673`
- Workshop pack: Upsell,CrossSellEngine.pdf board 4
- Flow F290 *Upsell,CrossSellEngine board 4: Journey & Context Command Center*, step 8: Works in Post-Purchase & Pre-Visit Recommendation Manager → Continue the commercial journey after payment while respecting the guest's existing purchase and visit plan.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-673?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-669`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-674` In-Venue & Location-Aware Recommendation Engine

**Support context-aware recommendations while the guest is physically visiting the venue. This directly addresses the matrix's requirement for location-aware in-venue upsell/cross-sell.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/in-venue-location-aware-recommendation-engine-adm-674` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-669` Journey & Context Command Center: *Back to Journey & Context Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The in-venue location-aware recommendation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the in-venue location-aware recommendation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No in-venue location-aware recommendation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the in-venue location-aware recommendation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-674` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS181 Upsell,CrossSellEngine Board 4.dc.html#adm-674`
- Workshop pack: Upsell,CrossSellEngine.pdf board 4
- Flow F290 *Upsell,CrossSellEngine board 4: Journey & Context Command Center*, step 10: Works in In-Venue & Location-Aware Recommendation Engine → Support context-aware recommendations while the guest is physically visiting the venue. This directly addresses the matrix's requirement for location-aware in-venue upsell/cross-sell.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-674?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `ADM-669`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-675` Visit State, Itinerary & Time-Aware Recommendation

**Make recommendations aware of what the customer has already done and what remains possible during the visit.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Show) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/visit-state-itinerary-time-aware-recommendation-adm-675` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Purchased products** (metric tile)

**Reserved timeslots** (metric tile)

**Completed activities** (metric tile)

**Remaining activities** (metric tile)

**Available time** (metric tile)

**Venue closing time** (metric tile)

**Where the user goes next**

- → `ADM-669` Journey & Context Command Center: *Back to Journey & Context Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The visit state itinerary list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the visit state itinerary untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No visit state itinerary yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the visit state itinerary are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `updateRecommendationStrategy` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'plan your adventure')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-675` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS181 Upsell,CrossSellEngine Board 4.dc.html#adm-675`
- Workshop pack: Upsell,CrossSellEngine.pdf board 4
- Flow F290 *Upsell,CrossSellEngine board 4: Journey & Context Command Center*, step 12: Works in Visit State, Itinerary & Time-Aware Recommendation → Make recommendations aware of what the customer has already done and what remains possible during the visit.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-675?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-669`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-676` Omnichannel Recommendation Synchronization

**Coordinate recommendations across channels so customers receive a consistent experience.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/omnichannel-recommendation-synchronization-adm-676` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRecommendationStrategies` ?status |
| Placement | text field | — | — | `listRecommendationStrategies` ?placement |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every omnichannel recommendation synchronization** (data table)

| Shows | Format | Notes |
|---|---|---|
| Presented | text | not in the schema: `Presented` |
| Viewed | text | not in the schema: `Viewed` |
| Selected | text | not in the schema: `Selected` |
| Declined | text | not in the schema: `Declined` |
| Purchased | text | not in the schema: `Purchased` |
| Suppressed | text | not in the schema: `Suppressed` |
| Expired | text | not in the schema: `Expired` |

**The selected omnichannel recommendation synchronization** (detail panel): The pack groups this record's detail under its own headings: “Supported Channels”, “The engine determines whether to”, “B2C”, “App”, “Customer”, “POS”.

| Shows | Format | Notes |
|---|---|---|
| Presented | text | not in the schema: `Presented` |
| Viewed | text | not in the schema: `Viewed` |
| Selected | text | not in the schema: `Selected` |
| Declined | text | not in the schema: `Declined` |
| Purchased | text | not in the schema: `Purchased` |
| Suppressed | text | not in the schema: `Suppressed` |
| Expired | text | not in the schema: `Expired` |

**Data it reads**: `listRecommendationStrategies` (onLoad, Across channels)

**Where the user goes next**

- → `ADM-669` Journey & Context Command Center: *Back to Journey & Context Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The omnichannel recommendation synchronization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the omnichannel recommendation synchronization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No omnichannel recommendation synchronization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the omnichannel recommendation synchronization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listRecommendationStrategies` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-676` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS181 Upsell,CrossSellEngine Board 4.dc.html#adm-676`
- Workshop pack: Upsell,CrossSellEngine.pdf board 4
- Flow F290 *Upsell,CrossSellEngine board 4: Journey & Context Command Center*, step 14: Works in Omnichannel Recommendation Synchronization → Coordinate recommendations across channels so customers receive a consistent experience.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-676?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-669`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-677` Contextual Trigger, Frequency & Experience Controls

**Control exactly when a recommendation is triggered and prevent excessive customer interaction.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/contextual-trigger-frequency-experience-controls-adm-677` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Maximum recommendations/session | select field | — | — | — | — | — | — |
| Maximum/day | select field | — | — | — | — | — | — |
| Maximum/visit | select field | — | — | — | — | — | — |
| Maximum/channel | select field | — | — | — | — | — | — |
| Maximum per product | select field | — | — | — | — | — | — |
| Cooling period | select field | — | — | — | — | — | — |
| Repeat threshold | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-669` Journey & Context Command Center: *Back to Journey & Context Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The contextual trigger frequency configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the contextual trigger frequency untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No contextual trigger frequency configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setRecommendationSuppression` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-677` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS181 Upsell,CrossSellEngine Board 4.dc.html#adm-677`
- Workshop pack: Upsell,CrossSellEngine.pdf board 4
- Flow F290 *Upsell,CrossSellEngine board 4: Journey & Context Command Center*, step 16: Works in Contextual Trigger, Frequency & Experience Controls → Control exactly when a recommendation is triggered and prevent excessive customer interaction.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-677?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-669`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-678` Journey Simulator, Decision Trace & AI Optimization

**Allow administrators to simulate an entire customer journey and see how recommendations change over time.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE`, `PRODUCT_CONFIGURE` (1 operate, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `decisionId` (navigation) |
| Route | `/commercial/journey-simulator-decision-trace-ai-optimization-adm-678` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-669` Journey & Context Command Center: *Back to Journey & Context Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The journey simulator decision list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the journey simulator decision untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No journey simulator decision yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the journey simulator decision are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `simulateRecommendationStrategy` → `PRODUCT_CONFIGURE` (configure) · staff
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

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-678` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS181 Upsell,CrossSellEngine Board 4.dc.html#adm-678`
- Workshop pack: Upsell,CrossSellEngine.pdf board 4
- Flow F290 *Upsell,CrossSellEngine board 4: Journey & Context Command Center*, step 18: Works in Journey Simulator, Decision Trace & AI Optimization → Allow administrators to simulate an entire customer journey and see how recommendations change over time.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-678?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-669`.
- [ ] Every gated control is gated: `AI_USE`, `PRODUCT_CONFIGURE`.
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
"explainRecommendationDecision": {"method":"GET","path":"/recommendations/decisions/{decisionId}/explanation","contract":"ai","summary":"Why these recommendations","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"depth","in":"query","required":null}],"requestBody":null,"responds":"AiRecommendationExplanation"},
"getRecommendationPerformance": {"method":"GET","path":"/recommendation-performance","contract":"promotions","summary":"Impressions, acceptance, revenue and incremental lift","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"RecommendationPerformance"},
"listRecommendationStrategies": {"method":"GET","path":"/recommendation-strategies","contract":"promotions","summary":"The strategies deciding what gets offered where","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"placement","in":"query","required":null}],"requestBody":null,"responds":"RecommendationStrategy"},
"setRecommendationSuppression": {"method":"PUT","path":"/recommendation-suppressions","contract":"promotions","summary":"Fatigue limits, frequency caps and hard exclusions","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RecommendationSuppression","responds":"RecommendationSuppression"},
"simulateRecommendationStrategy": {"method":"POST","path":"/recommendation-simulations","contract":"promotions","summary":"Replay a strategy against history before it goes live","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RecommendationPerformance"},
"updateRecommendationStrategy": {"method":"PUT","path":"/recommendation-strategies/{strategyId}","contract":"promotions","summary":"Change a strategy","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"RecommendationStrategy","responds":"RecommendationStrategy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiRecommendationExplanation": {"type":"object","x-ticvai-persistence":"none — built from ai.rec_decision and its decision record","description":"Why these items (AIR-193..202), at three depths each gated by permission (AIC-195): business, governance, technical.","required":["decisionId","depth"],"properties":{"decisionId":{"type":"string","format":"uuid"},"depth":{"type":"string","enum":["business","governance","technical"]},"funnel":{"type":"object","additionalProperties":true},"exclusions":{"type":"object","additionalProperties":true},"items":{"type":"array","items":{"type":"object","properties":{"trackingId":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid"},"reasons":{"type":"array","items":{"type":"string"}},"scoreBreakdown":{"type":"object","additionalProperties":true,"nullable":true}}}},"versions":{"type":"object","additionalProperties":true,"nullable":true,"description":"Strategy, model and feature-set versions. `technical` depth only."}}},
"RecommendationPerformance": {"type":"object","description":"Board 6.5. **Attributed and incremental reported apart** — the first flatters.","properties":{"key":{"type":"string"},"label":{"type":"string"},"impressions":{"type":"integer"},"clicks":{"type":"integer"},"accepted":{"type":"integer"},"acceptanceRate":{"type":"number"},"attributedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"holdoutAcceptanceRate":{"type":"number","nullable":true},"lift":{"type":"number","nullable":true}}},
"RecommendationStrategy": {"type":"object","x-ticvai-persistence":"promotions.recommendation_strategy","description":"Upsell board 1. **Objective, placement, ranking and guardrail in one record**, because any one of them alone produces a recommender that is either aimless or dangerous.\n","required":["code","name","objective"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"objective":{"type":"string","enum":["attachRevenue","averageOrderValue","upgradeRate","visitFrequency","inventoryBalance","guestSatisfaction"]},"kinds":{"type":"array","items":{"type":"string","enum":["upsell","upgrade","crossSell","bundle","nextBestOffer","reactivation"]}},"itemKinds":{"type":"array","description":"What the strategy may put in a slot (29 September, build pass, group G2, from group G1's handoff; 8.6.30 to 8.6.36, 5.4.21, 22.6.18): `product` (the default and the behaviour before), `offer` (a live promotion marked `recommendable`), `reward` (a marketing-crm loyalty reward the guest can redeem) and `challenge` (a challenge they can join). Mirrors `ai.decideRecommendations` item kinds.","default":["product"],"items":{"type":"string","enum":["product","offer","reward","challenge"]}},"placements":{"type":"array","description":"`homepage` (8.6.10) and `loyalty` (5.4.21, 22.6.18) added 29 September (build pass, group G2), matching the placements `ai.decideRecommendations` fills.","items":{"type":"string","enum":["productPage","cart","checkout","postPurchase","preVisitEmail","inVenueApp","kiosk","pos","signage","callCentre","homepage","loyalty"]}},"channels":{"type":"array","items":{"type":"string"}},"maxRecommendations":{"type":"integer","default":3,"description":"**A guardrail before it is a layout choice.** Nine upsells at checkout is not a denser page, it is an abandoned basket.\n"},"minConfidence":{"type":"number","nullable":true},"rankingWeights":{"type":"object","additionalProperties":{"type":"number"},"description":"Propensity, margin, inventory pressure, affinity, recency."},"requireAvailability":{"type":"boolean","default":true},"excludeInBasket":{"type":"boolean","default":true},"guardrails":{"type":"object","properties":{"maxDiscountPercent":{"type":"number","nullable":true},"minMarginPercent":{"type":"number","nullable":true},"neverRecommendCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requireHumanApproval":{"type":"boolean","default":false}}},"status":{"type":"string","enum":["draft","active","paused","retired"]},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"scopePath":{"type":"string"}}},
"RecommendationSuppression": {"type":"object","x-ticvai-persistence":"promotions.recommendation_suppression","description":"Boards 1.7 and 5.7. **Fatigue is why a good recommender stops working.**","properties":{"scopePath":{"type":"string"},"maxImpressionsPerProductPerDay":{"type":"integer","nullable":true},"maxImpressionsPerGuestPerSession":{"type":"integer","nullable":true},"cooldownAfterDismissDays":{"type":"integer","nullable":true},"cooldownAfterAcceptDays":{"type":"integer","nullable":true},"hardExclusions":{"type":"array","items":{"type":"object","properties":{"segmentId":{"type":"string","format":"uuid","nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string"}}}}}}
}
```
