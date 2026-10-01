# WS184 — Upsell,CrossSellEngine board 5

**10 screens · 7 operations · 11 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `AI_USE, GUEST_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `ADM-679` | Personalization & NBO Command Center | B–D | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `ADM-680` | Customer Recommendation Profile | B–D | 0 | 0 | 6 | 6 | 0 | 0 | — | notStarted (—) |
| `ADM-681` | Customer Feature & Signal Configuration | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-682` | Propensity Model & Customer Intent Manager | B–D | 0 | 14 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `ADM-683` | Next-Best-Offer Decision Studio | B–D | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-684` | Personalized Ranking & Decision Policy Builder | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-685` | Customer Preference, Fatigue & Suppression Intelligence | B–D | 0 | 14 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-686` | Anonymous, Known & Identity-Transition Personalization.123 | B–D | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-687` | AI Explainability, Confidence & Model Governance | B–D | 0 | 14 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-688` | Personalization Simulator & Next-Best-Offer Lab | B–D | 12 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-680, ADM-681, ADM-682, ADM-683, ADM-685, ADM-686, ADM-687 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-679` Personalization & NBO Command Center

**Provide centralized visibility into the operation and commercial impact of personalized recommendations.**

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
| Route | `/commercial/personalization-nbo-command-center-adm-679` |

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

**Personalized Recommendations** (metric tile)

**Personalized Customers/Sessions** (metric tile)

**Next-Best-Offers Generated** (metric tile)

**NBO Acceptance Rate** (metric tile)

**Personalized Conversion** (metric tile)

**Incremental Revenue** (metric tile)

**Personalized AOV Uplift** (metric tile)

**Recommendation Relevance** (metric tile)

**AI Confidence** (metric tile)

**Rule-Based Fallback Rate** (metric tile)

**Suppressed Recommendations** (metric tile)

**AI Opportunities** (metric tile)

**Data it reads**: `getRecommendationPerformance` (onLoad, Personalisation performance)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-680` Customer Recommendation Profile: *Customer Recommendation Profile*
- → `ADM-681` Customer Feature & Signal Configuration: *Customer Feature & Signal Configuration*
- → `ADM-682` Propensity Model & Customer Intent Manager: *Propensity Model & Customer Intent Manager*
- → `ADM-683` Next-Best-Offer Decision Studio: *Next-Best-Offer Decision Studio*
- → `ADM-684` Personalized Ranking & Decision Policy Builder: *Personalized Ranking & Decision Policy Builder*
- → `ADM-685` Customer Preference, Fatigue & Suppression Intelligence: *Customer Preference, Fatigue & Suppression Intelligence*
- → `ADM-686` Anonymous, Known & Identity-Transition Personalization.123: *Anonymous, Known & Identity-Transition Personalization.123*
- → `ADM-687` AI Explainability, Confidence & Model Governance: *AI Explainability, Confidence & Model Governance*
- → `ADM-688` Personalization Simulator & Next-Best-Offer Lab: *Personalization Simulator & Next-Best-Offer Lab*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The personalization nbo list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the personalization nbo untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No personalization nbo yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the personalization nbo are still there. Names the active filter and offers to clear it. |
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-679` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-679`
- Workshop pack: Upsell,CrossSellEngine.pdf board 5
- Flow F291 *Upsell,CrossSellEngine board 5: Personalization & NBO Command Center*, step 1: Opens Personalization & NBO Command Center → Provide centralized visibility into the operation and commercial impact of personalized recommendations.
- Flow F291 *Upsell,CrossSellEngine board 5: Personalization & NBO Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F291 *Upsell,CrossSellEngine board 5: Personalization & NBO Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F291 *Upsell,CrossSellEngine board 5: Personalization & NBO Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F291 *Upsell,CrossSellEngine board 5: Personalization & NBO Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F291 *Upsell,CrossSellEngine board 5: Personalization & NBO Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F291 *Upsell,CrossSellEngine board 5: Personalization & NBO Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F291 *Upsell,CrossSellEngine board 5: Personalization & NBO Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F291 branch at step 1 (expected): when Nothing has been set up on Personalization & NBO Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F291 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-679?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-680`, `ADM-681`, `ADM-682`, `ADM-683`, `ADM-684`, `ADM-685`, `ADM-686`, `ADM-687`, `ADM-688`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-680` Customer Recommendation Profile

**Provide the recommendation engine's commercially relevant customer context used for personalization. This should not become another CRM profile screen. CRM remains the authoritative source of customer information. Board 5 displays only the attributes relevant to recommendation decisioning.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE`, `GUEST_VIEW` (1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `subjectId` (navigation), `decisionId` (navigation) |
| Route | `/commercial/customer-recommendation-profile-adm-680` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getCustomerRecommendationProfile` (onLoad, What the engine knows about a customer)

**Where the user goes next**

- → `ADM-679` Personalization & NBO Command Center: *Back to Personalization & NBO Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer recommendation profile list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer recommendation profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer recommendation profile yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer recommendation profile are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getGuestProfile` → `GUEST_VIEW` (read) · staff, guest
- `getCustomerRecommendationProfile` → `AI_USE` (operate) · staff
- `explainRecommendationDecision` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.8 | APIs shall support guest profile creation, updates, segmentation, communication preferences and activity history retrieval. | Developer & API Management | CONTRACTED | `getGuestProfile` |
| 22.2.27 | CRM APIs | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 22.2.28 | CRM Audit Trail | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 8.6.14 | System shall provide recommendations based on purchase history. | Unified Operations Dashboard | CONTRACTED | `getCustomerRecommendationProfile` |
| 8.6.15 | System shall provide recommendations based on customer segments. | Unified Operations Dashboard | CONTRACTED | `getCustomerRecommendationProfile` |
| 8.6.20 | System shall support recommendation explainability. | Unified Operations Dashboard | CONTRACTED | `explainRecommendationDecision` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-680` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-680`
- Workshop pack: Upsell,CrossSellEngine.pdf board 5
- Flow F291 *Upsell,CrossSellEngine board 5: Personalization & NBO Command Center*, step 2: Works in Customer Recommendation Profile → Provide the recommendation engine's commercially relevant customer context used for personalization. This should not become another CRM profile screen. CRM remains the authoritative source of …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-680?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-679`.
- [ ] Every gated control is gated: `AI_USE`, `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-681` Customer Feature & Signal Configuration

**Control which approved data signals the AI may use when calculating personalized recommendations. This is critical for governance and explainability.**

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
| Route | `/commercial/customer-feature-signal-configuration-adm-681` |

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

- → `ADM-679` Personalization & NBO Command Center: *Back to Personalization & NBO Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer feature signal list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer feature signal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer feature signal yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer feature signal are still there. Names the active filter and offers to clear it. |
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-681` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-681`
- Workshop pack: Upsell,CrossSellEngine.pdf board 5
- Flow F291 *Upsell,CrossSellEngine board 5: Personalization & NBO Command Center*, step 4: Works in Customer Feature & Signal Configuration → Control which approved data signals the AI may use when calculating personalized recommendations. This is critical for governance and explainability.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-681?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `ADM-679`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-682` Propensity Model & Customer Intent Manager

**Calculate the likelihood that a guest will take specific commercial actions.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/propensity-model-customer-intent-manager-adm-682` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … **Propensity Model & Customer Intent Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so …

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

**Every propensity model customer** (data table)

| Shows | Format | Notes |
|---|---|---|
| Model name | text | not in the schema: `Model name` |
| Model version | text | not in the schema: `Model version` |
| Last updated | text | not in the schema: `Last updated` |
| Training period | text | not in the schema: `Training period` |
| Confidence | text | not in the schema: `Confidence` |
| Population | text | not in the schema: `Population` |
| Data freshness | text | not in the schema: `Data freshness` |

**The selected propensity model customer** (detail panel): The pack groups this record's detail under its own headings: “Membershi”, “Family”, “Meal”, “Propensity Bands”, “Important”.

| Shows | Format | Notes |
|---|---|---|
| Model name | text | not in the schema: `Model name` |
| Model version | text | not in the schema: `Model version` |
| Last updated | text | not in the schema: `Last updated` |
| Training period | text | not in the schema: `Training period` |
| Confidence | text | not in the schema: `Confidence` |
| Population | text | not in the schema: `Population` |
| Data freshness | text | not in the schema: `Data freshness` |

**Data it reads**: `getRecommendationPerformance` (onLoad, Propensity and intent)

**Where the user goes next**

- → `ADM-679` Personalization & NBO Command Center: *Back to Personalization & NBO Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The propensity model customer list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the propensity model customer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No propensity model customer yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the propensity model customer are still there. Names the active filter and offers to clear it. |
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-682` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-682`
- Workshop pack: Upsell,CrossSellEngine.pdf board 5
- Flow F291 *Upsell,CrossSellEngine board 5: Personalization & NBO Command Center*, step 6: Works in Propensity Model & Customer Intent Manager → Calculate the likelihood that a guest will take specific commercial actions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-682?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-679`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-683` Next-Best-Offer Decision Studio

**This is the core screen of Board 5. Combine all eligible candidates and determine the strongest personalized recommendation.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE`, `PRODUCT_CONFIGURE` (1 operate, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `strategyId` (navigation), `decisionId` (navigation) |
| Route | `/commercial/next-best-offer-decision-studio-adm-683` |

**Known gaps.** **Next-Best-Offer Decision Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-679` Personalization & NBO Command Center: *Back to Personalization & NBO Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The next-best-offer decision list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the next-best-offer decision untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No next-best-offer decision yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the next-best-offer decision are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `updateRecommendationStrategy` → `PRODUCT_CONFIGURE` (configure) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-683` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-683`
- Workshop pack: Upsell,CrossSellEngine.pdf board 5
- Flow F291 *Upsell,CrossSellEngine board 5: Personalization & NBO Command Center*, step 8: Works in Next-Best-Offer Decision Studio → This is the core screen of Board 5. Combine all eligible candidates and determine the strongest personalized recommendation.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-683?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `ADM-679`.
- [ ] Every gated control is gated: `AI_USE`, `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-684` Personalized Ranking & Decision Policy Builder

**Configure how TICVAI converts AI scores and commercial factors into the final recommendation ranking.**

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
| Route | `/commercial/personalized-ranking-decision-policy-builder-adm-684` |

**Known gaps.** **The pack names 10 actions on this screen and the screen declares 0 operations.** Unserved: Customer propensity, Product affinity, Historical acceptance, Revenue, Incremental revenue, Capacity … **Personalized Ranking & Decision Policy Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Customer propensity (primary button) | navigation or local | — | — | — | — |
| Product affinity (secondary button) | navigation or local | — | — | — | — |
| Historical acceptance (secondary button) | navigation or local | — | — | — | — |
| Revenue (secondary button) | navigation or local | — | — | — | — |
| Incremental revenue (secondary button) | navigation or local | — | — | — | — |
| Capacity (secondary button) | navigation or local | — | — | — | — |
| Inventory (secondary button) | navigation or local | — | — | — | — |
| Commercial priority (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-679` Personalization & NBO Command Center: *Back to Personalization & NBO Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The personalized ranking decision list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the personalized ranking decision untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No personalized ranking decision yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the personalized ranking decision are still there. Names the active filter and offers to clear it. |
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-684` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-684`
- Workshop pack: Upsell,CrossSellEngine.pdf board 5
- Flow F291 *Upsell,CrossSellEngine board 5: Personalization & NBO Command Center*, step 10: Works in Personalized Ranking & Decision Policy Builder → Configure how TICVAI converts AI scores and commercial factors into the final recommendation ranking.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-684?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Customer propensity, Product affinity, Historical acceptance, Revenue, Incremental revenue, Capacity, Inventory, Commercial priority.
- [ ] Every transition is wired: `ADM-679`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-685` Customer Preference, Fatigue & Suppression Intelligence

**Prevent personalization from becoming repetitive or intrusive. Board 4 provides general journey frequency controls. Board 5 adds customer-specific behavioral suppression.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/customer-preference-fatigue-suppression-intelligence-adm-685` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every customer preference fatigue** (data table)

| Shows | Format | Notes |
|---|---|---|
| Repeated declines | text | not in the schema: `Repeated declines` |
| Repeated ignores | text | not in the schema: `Repeated ignores` |
| Recent purchase | text | not in the schema: `Recent purchase` |
| Previous acceptance | text | not in the schema: `Previous acceptance` |
| Category preference | text | not in the schema: `Category preference` |
| Recommendation fatigue | text | not in the schema: `Recommendation fatigue` |
| Channel response | text | not in the schema: `Channel response` |

**The selected customer preference fatigue** (detail panel): The pack groups this record's detail under its own headings: “Photo Package”, “System action”, “Customer consistently accepts”, “Explicit Preferences”.

| Shows | Format | Notes |
|---|---|---|
| Repeated declines | text | not in the schema: `Repeated declines` |
| Repeated ignores | text | not in the schema: `Repeated ignores` |
| Recent purchase | text | not in the schema: `Recent purchase` |
| Previous acceptance | text | not in the schema: `Previous acceptance` |
| Category preference | text | not in the schema: `Category preference` |
| Recommendation fatigue | text | not in the schema: `Recommendation fatigue` |
| Channel response | text | not in the schema: `Channel response` |

**Where the user goes next**

- → `ADM-679` Personalization & NBO Command Center: *Back to Personalization & NBO Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer preference fatigue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer preference fatigue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer preference fatigue yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer preference fatigue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-685` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-685`
- Workshop pack: Upsell,CrossSellEngine.pdf board 5
- Flow F291 *Upsell,CrossSellEngine board 5: Personalization & NBO Command Center*, step 12: Works in Customer Preference, Fatigue & Suppression Intelligence → Prevent personalization from becoming repetitive or intrusive. Board 4 provides general journey frequency controls. Board 5 adds customer-specific behavioral suppression.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-685?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-679`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-686` Anonymous, Known & Identity-Transition Personalization.123

**Allow useful recommendations even when TICVAI does not yet know the customer's identity.**

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
| Route | `/commercial/anonymous-known-identity-transition-personalization-123-adm-686` |

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

- → `ADM-679` Personalization & NBO Command Center: *Back to Personalization & NBO Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The anonymous known identity-transition list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the anonymous known identity-transition untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No anonymous known identity-transition yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the anonymous known identity-transition are still there. Names the active filter and offers to clear it. |
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-686` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-686`
- Workshop pack: Upsell,CrossSellEngine.pdf board 5
- Flow F291 *Upsell,CrossSellEngine board 5: Personalization & NBO Command Center*, step 14: Works in Anonymous, Known & Identity-Transition Personalization.123 → Allow useful recommendations even when TICVAI does not yet know the customer's identity.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-686?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-679`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-687` AI Explainability, Confidence & Model Governance

**Make personalized AI decisions understandable and governable.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `decisionId` (navigation) |
| Route | `/commercial/ai-explainability-confidence-model-governance-adm-687` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every explainability confidence model** (data table)

| Shows | Format | Notes |
|---|---|---|
| Model | text | not in the schema: `Model` |
| Version | text | not in the schema: `Version` |
| Deployment date | text | not in the schema: `Deployment date` |
| Owner | text | not in the schema: `Owner` |
| Status | text | not in the schema: `Status` |
| Confidence threshold | text | not in the schema: `Confidence threshold` |
| Fallback policy | text | not in the schema: `Fallback policy` |

**The selected explainability confidence model** (detail panel): The pack groups this record's detail under its own headings: “Annual Family Membership”, “Confidence”, “Show ranked contributors”.

| Shows | Format | Notes |
|---|---|---|
| Model | text | not in the schema: `Model` |
| Version | text | not in the schema: `Version` |
| Deployment date | text | not in the schema: `Deployment date` |
| Owner | text | not in the schema: `Owner` |
| Status | text | not in the schema: `Status` |
| Confidence threshold | text | not in the schema: `Confidence threshold` |
| Fallback policy | text | not in the schema: `Fallback policy` |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Disable model, Change approved threshold, Switch to rules, Suspend recommendation category. Each needs attaching to the control it gates, or the screen needs the control.

**Where the user goes next**

- → `ADM-679` Personalization & NBO Command Center: *Back to Personalization & NBO Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The explainability confidence model list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the explainability confidence model untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No explainability confidence model yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the explainability confidence model are still there. Names the active filter and offers to clear it. |
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-687` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-687`
- Workshop pack: Upsell,CrossSellEngine.pdf board 5
- Flow F291 *Upsell,CrossSellEngine board 5: Personalization & NBO Command Center*, step 16: Works in AI Explainability, Confidence & Model Governance → Make personalized AI decisions understandable and governable.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-687?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-679`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-688` Personalization Simulator & Next-Best-Offer Lab

**Allow administrators to simulate how TICVAI would personalize recommendations for different customers before deploying changes.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/personalization-simulator-next-best-offer-lab-adm-688` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Customer or synthetic profile | text field | — | — | — | — | — | — |
| Segment | select field | — | — | — | — | — | — |
| Membership | select field | — | — | — | — | — | — |
| Loyalty | select field | — | — | — | — | — | — |
| Historical spend | select field | — | — | — | — | — | — |
| Visit frequency | select field | — | — | — | — | — | — |
| Purchase history | select field | — | — | — | — | — | — |
| Current basket | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Journey stage | select field | — | — | — | — | — | — |
| Date/time | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-679` Personalization & NBO Command Center: *Back to Personalization & NBO Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The personalization simulator next-best-offer configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the personalization simulator next-best-offer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No personalization simulator next-best-offer configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-688` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-688`
- Workshop pack: Upsell,CrossSellEngine.pdf board 5
- Flow F291 *Upsell,CrossSellEngine board 5: Personalization & NBO Command Center*, step 18: Works in Personalization Simulator & Next-Best-Offer Lab → Allow administrators to simulate how TICVAI would personalize recommendations for different customers before deploying changes.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-688?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-679`.
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
"explainRecommendationDecision": {"method":"GET","path":"/recommendations/decisions/{decisionId}/explanation","contract":"ai","summary":"Why these recommendations","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"depth","in":"query","required":null}],"requestBody":null,"responds":"AiRecommendationExplanation"},
"getCustomerRecommendationProfile": {"method":"GET","path":"/recommendations/customers/{subjectId}/profile","contract":"ai","summary":"What the engine knows about a customer","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiCustomerRecommendationProfile"},
"getGuestProfile": {"method":"GET","path":"/guests/{subjectId}","contract":"marketing-crm","summary":"Read a guest profile","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuestProfileDetail"},
"getRecommendationPerformance": {"method":"GET","path":"/recommendation-performance","contract":"promotions","summary":"Impressions, acceptance, revenue and incremental lift","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"RecommendationPerformance"},
"setRecommendationSuppression": {"method":"PUT","path":"/recommendation-suppressions","contract":"promotions","summary":"Fatigue limits, frequency caps and hard exclusions","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RecommendationSuppression","responds":"RecommendationSuppression"},
"simulateRecommendationStrategy": {"method":"POST","path":"/recommendation-simulations","contract":"promotions","summary":"Replay a strategy against history before it goes live","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RecommendationPerformance"},
"updateRecommendationStrategy": {"method":"PUT","path":"/recommendation-strategies/{strategyId}","contract":"promotions","summary":"Change a strategy","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"RecommendationStrategy","responds":"RecommendationStrategy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiCustomerRecommendationProfile": {"type":"object","x-ticvai-persistence":"none — assembled from features, ai.rec_decline and ai.rec_event","description":"What the engine knows about one customer for recommendations (ADM-680): segment, affinities, declines, consent flags and recent decisions. Sensitive data never becomes a feature (AIR-185).","required":["subjectId"],"properties":{"subjectId":{"type":"string","format":"uuid"},"segment":{"type":"string","nullable":true},"personalisationAllowed":{"type":"boolean"},"affinities":{"type":"array","items":{"type":"object","properties":{"categoryRef":{"type":"string"},"strength":{"type":"number"}}}},"declines":{"type":"array","items":{"$ref":"#/components/schemas/AiRecommendationDecline"}},"recentDecisions":{"type":"array","items":{"$ref":"#/components/schemas/AiRecommendationDecision"}},"featureFreshAt":{"type":"string","format":"date-time","nullable":true}}},
"AiRecommendationDecision": {"type":"object","x-ticvai-persistence":"ai.rec_decision","description":"**One compact recommendation decision** (design 2.2 A, 3.1 Recommendation): funnel counts, exclusion reasons (AIR-032), versions, scores and the final set. Written after the response, never before it. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["placement","mode","items"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"placement":{"type":"string","enum":["productPage","cart","checkout","postPurchase","preVisit","inVenue","posBasket","kioskBasket","fnbMenu","retailBasket","seatUpgrade","membership","email","homepage","loyalty"]},"channel":{"type":"string"},"cartId":{"type":"string","format":"uuid","nullable":true},"sessionRef":{"type":"string","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"mode":{"type":"string","enum":["personalised","contextual","rulesOnly","fallback"],"description":"Personalised only where context is sufficient and consent allows (AIR-114, AIR-187)."},"strategyRef":{"type":"string","nullable":true},"strategyVersion":{"type":"integer","nullable":true},"modelVersion":{"type":"string","nullable":true},"featureSetVersion":{"type":"string","nullable":true},"funnel":{"type":"object","additionalProperties":true,"description":"Candidate counts at each stage: generated, eligible, ranked, returned."},"exclusions":{"type":"object","additionalProperties":true,"description":"Removed candidates by reason: unsaleable, capacity, inventory, owned, inCart, conflict, declined, frequencyCap, guardrail."},"items":{"$ref":"#/components/schemas/AiRecommendationItemList"},"experimentArm":{"type":"string","nullable":true},"latencyMs":{"type":"integer"},"expiresAt":{"type":"string","format":"date-time","description":"Decision TTL: 30 s where capacity-sensitive, 30 min otherwise (AIR-208)."},"decidedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiRecommendationDecline": {"type":"object","x-ticvai-persistence":"ai.rec_decline","description":"**The cross-channel decline store** (AIR-065). Keyed on customer or session, so a declined offer is not repeated at the kiosk after the app. **Only an explicit decline counts; \"ignored\" is not a decline** (decided 29 September, decision 7).","required":["declinedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"sessionRef":{"type":"string","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true,"description":"The declined product. Null where a non-product item was declined (`itemRef`)."},"itemRef":{"type":"string","nullable":true,"description":"For a declined `offer`, `reward` or `challenge` item (29 September, build): its `promotionId`, `couponRef`, `rewardId` or `challengeId`, prefixed with the kind (`offer:`, `reward:`, `challenge:`), resolved from the event's `trackingId`."},"placement":{"type":"string","enum":["productPage","cart","checkout","postPurchase","preVisit","inVenue","posBasket","kioskBasket","fnbMenu","retailBasket","seatUpgrade","membership","email","homepage","loyalty"]},"channel":{"type":"string","nullable":true},"declinedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiRecommendationExplanation": {"type":"object","x-ticvai-persistence":"none — built from ai.rec_decision and its decision record","description":"Why these items (AIR-193..202), at three depths each gated by permission (AIC-195): business, governance, technical.","required":["decisionId","depth"],"properties":{"decisionId":{"type":"string","format":"uuid"},"depth":{"type":"string","enum":["business","governance","technical"]},"funnel":{"type":"object","additionalProperties":true},"exclusions":{"type":"object","additionalProperties":true},"items":{"type":"array","items":{"type":"object","properties":{"trackingId":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid"},"reasons":{"type":"array","items":{"type":"string"}},"scoreBreakdown":{"type":"object","additionalProperties":true,"nullable":true}}}},"versions":{"type":"object","additionalProperties":true,"nullable":true,"description":"Strategy, model and feature-set versions. `technical` depth only."}}},
"ConsentState": {"x-ticvai-persistence":"none — projection over consent_record","type":"object","required":["subjectId","purposes"],"properties":{"subjectId":{"type":"string","format":"uuid"},"purposes":{"type":"array","items":{"type":"object","required":["purpose","decision","requiresRenewal"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"decision":{"$ref":"#/components/schemas/ConsentDecision"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string","nullable":true},"requiresRenewal":{"type":"boolean","description":"True where the notice has been superseded since consent was given."},"decidedAt":{"type":"string","format":"date-time","nullable":true}}}}}},
"GuestProfile": {"x-ticvai-persistence":"marketing.guest_profile","type":"object","required":["subjectId","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"subjectId":{"type":"string","format":"uuid","description":"Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger.\n"},"displayName":{"type":"string","nullable":true},"email":{"type":"string","nullable":true},"phone":{"type":"string","nullable":true},"preferredLanguage":{"type":"string","nullable":true},"preferredChannel":{"$ref":"#/components/schemas/MessageChannel"},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells. Marketing acts locally."},"tags":{"type":"array","items":{"type":"string"}},"engagementScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"description":"22.2.20 and 22.2.21. **`lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not.** They are different questions: a guest who spent a lot once and a guest who visits monthly have the same LTV and need opposite treatment.\n**Recency, frequency and breadth, not spend** — spend is already `lifetimeValue`, and folding it in here would make one number twice.\n"},"engagementTier":{"type":"string","nullable":true,"enum":["new","active","occasional","lapsing","lapsed","dormant"],"description":"5.3.19. **Automatic classification, computed rather than assigned.** `lapsing` is the tier the whole field exists for — **a guest who has not been for a while and still might is the only one marketing can change**, and lumping them with `lapsed` wastes the window.\n"},"lifetimeValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"visitCount":{"type":"integer"},"lastVisitAt":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"},"mergedIntoSubjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`**, which retain it as a redirect rather than deleting it. A read that lands here follows it; a second merge of a profile that has one is refused as `alreadyMerged`.\n"},"mergedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"GuestProfileDetail": {"x-ticvai-persistence":"marketing.guest_profile","allOf":[{"$ref":"#/components/schemas/GuestProfile"},{"type":"object","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"consents":{"$ref":"#/components/schemas/ConsentState"},"loyalty":{"$ref":"#/components/schemas/LoyaltyPosition"},"openCaseCount":{"type":"integer"},"recentOrderIds":{"type":"array","items":{"type":"string"}},"membershipIds":{"type":"array","items":{"type":"string","format":"uuid"}},"notes":{"type":"string","nullable":true}}}]},
"LoyaltyPosition": {"x-ticvai-persistence":"marketing.loyalty_position","type":"object","required":["subjectId","programmeId","pointsBalance","tierCode"],"properties":{"leaderboardNickname":{"type":"string","nullable":true,"maxLength":24,"description":"BL-173. **The name shown on a leaderboard, chosen by the guest.** Offered whenever they reach the board and changeable afterwards; `setLeaderboardNickname` is the only thing that writes it.\n**Null means the guest has not chosen one yet, and the board shows a generated `Player-4821` in its place** — never `pii.subject.display_name`, which would disclose silently on the day a guest first placed and is the case this field exists to prevent.\n**The generated name is computed at read time and not stored here.** Writing it would make *\"has this guest chosen a name\"* unanswerable, and that flag is what the prompt-on-reaching-the-board depends on.\n"},"subjectId":{"type":"string","format":"uuid"},"programmeId":{"type":"string","format":"uuid"},"pointsBalance":{"type":"integer"},"lifetimePoints":{"type":"integer"},"tierId":{"type":"string","format":"uuid","nullable":true,"description":"**The tier this row's `tierCode` and `tierName` are a copy of.** Added 20 September with `marketing.programme_tier`: the two strings were a cache of something that did not exist, and a cache with no source cannot be rebuilt or audited.\n"},"tierCode":{"type":"string"},"tierName":{"type":"string"},"pointsToNextTier":{"type":"integer","nullable":true},"nextExpiryPoints":{"type":"integer","nullable":true},"nextExpiryAt":{"type":"string","format":"date-time","nullable":true}}},
"RecommendationPerformance": {"type":"object","description":"Board 6.5. **Attributed and incremental reported apart** — the first flatters.","properties":{"key":{"type":"string"},"label":{"type":"string"},"impressions":{"type":"integer"},"clicks":{"type":"integer"},"accepted":{"type":"integer"},"acceptanceRate":{"type":"number"},"attributedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"holdoutAcceptanceRate":{"type":"number","nullable":true},"lift":{"type":"number","nullable":true}}},
"RecommendationStrategy": {"type":"object","x-ticvai-persistence":"promotions.recommendation_strategy","description":"Upsell board 1. **Objective, placement, ranking and guardrail in one record**, because any one of them alone produces a recommender that is either aimless or dangerous.\n","required":["code","name","objective"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"objective":{"type":"string","enum":["attachRevenue","averageOrderValue","upgradeRate","visitFrequency","inventoryBalance","guestSatisfaction"]},"kinds":{"type":"array","items":{"type":"string","enum":["upsell","upgrade","crossSell","bundle","nextBestOffer","reactivation"]}},"itemKinds":{"type":"array","description":"What the strategy may put in a slot (29 September, build pass, group G2, from group G1's handoff; 8.6.30 to 8.6.36, 5.4.21, 22.6.18): `product` (the default and the behaviour before), `offer` (a live promotion marked `recommendable`), `reward` (a marketing-crm loyalty reward the guest can redeem) and `challenge` (a challenge they can join). Mirrors `ai.decideRecommendations` item kinds.","default":["product"],"items":{"type":"string","enum":["product","offer","reward","challenge"]}},"placements":{"type":"array","description":"`homepage` (8.6.10) and `loyalty` (5.4.21, 22.6.18) added 29 September (build pass, group G2), matching the placements `ai.decideRecommendations` fills.","items":{"type":"string","enum":["productPage","cart","checkout","postPurchase","preVisitEmail","inVenueApp","kiosk","pos","signage","callCentre","homepage","loyalty"]}},"channels":{"type":"array","items":{"type":"string"}},"maxRecommendations":{"type":"integer","default":3,"description":"**A guardrail before it is a layout choice.** Nine upsells at checkout is not a denser page, it is an abandoned basket.\n"},"minConfidence":{"type":"number","nullable":true},"rankingWeights":{"type":"object","additionalProperties":{"type":"number"},"description":"Propensity, margin, inventory pressure, affinity, recency."},"requireAvailability":{"type":"boolean","default":true},"excludeInBasket":{"type":"boolean","default":true},"guardrails":{"type":"object","properties":{"maxDiscountPercent":{"type":"number","nullable":true},"minMarginPercent":{"type":"number","nullable":true},"neverRecommendCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requireHumanApproval":{"type":"boolean","default":false}}},"status":{"type":"string","enum":["draft","active","paused","retired"]},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"scopePath":{"type":"string"}}},
"RecommendationSuppression": {"type":"object","x-ticvai-persistence":"promotions.recommendation_suppression","description":"Boards 1.7 and 5.7. **Fatigue is why a good recommender stops working.**","properties":{"scopePath":{"type":"string"},"maxImpressionsPerProductPerDay":{"type":"integer","nullable":true},"maxImpressionsPerGuestPerSession":{"type":"integer","nullable":true},"cooldownAfterDismissDays":{"type":"integer","nullable":true},"cooldownAfterAcceptDays":{"type":"integer","nullable":true},"hardExclusions":{"type":"array","items":{"type":"object","properties":{"segmentId":{"type":"string","format":"uuid","nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string"}}}}}}
}
```
