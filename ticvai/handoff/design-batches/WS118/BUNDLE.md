# WS118 — AI Configuration Assistant board 3

**10 screens · 21 operations · 26 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `AI_APPROVE, AI_AUDIT_VIEW, AI_CONFIGURE, AI_USE, PRODUCT_CONFIGURE`. A control nobody can use must say so,
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
| `ADM-489` | AI Configuration Readiness Center | B–D | 14 | 8 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-490` | Configuration Validation Results | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-491` | AI Recommendations & Best-Practice Review | B–D | 0 | 14 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-492` | Configuration Approval Workflow | B–D | 0 | 0 | 6 | 1 | 0 | 3 | — | notStarted (—) |
| `ADM-493` | AI Configuration Execution Center | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-494` | Execution Progress & Dependency Monitor | B–D | 0 | 42 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-495` | Configuration Results & Object Mapping | B–D | 0 | 16 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-496` | Configuration Change & Modification Assistant | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-497` | Configuration History, Versions & Rollback | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-498` | AI Configuration Audit & Governance | B–D | 2 | 10 | 6 | 4 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-490, ADM-491, ADM-492, ADM-494, ADM-495, ADM-496 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-489` AI Configuration Readiness Center

**Provide a final readiness assessment before the proposed Configuration Plan can enter approval or execution. This is the first governance gate.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE` (1 configure, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `planId` (navigation), `venueId` (session) |
| Route | `/platform/ai-configuration-readiness-center-adm-489` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Capability key | text field | — | — | `getEffectiveAiPolicy` ?capabilityKey |
| Scope path | text field | — | — | `getEffectiveAiPolicy` ?scopePath |
| Environment | radio group | — | Development · Sandbox · Staging · Production | `getEffectiveAiPolicy` ?environment |

**Form: Save venue AI profile** (modal, opened by *Save venue AI profile*; *Save venue AI profile* calls `setAiVenueSettings`, *Cancel* sends nothing)

**Collects what `setAiVenueSettings` sends before it is called.** Required: `venueId`, `venueType`. Every other figure is optional and defaults to the starting pattern for the venue type, so a venue that knows only its type still gets answers.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setAiVenueSettings` body |
| Venue type `venueType` | select | required | — | Water park · Theme park · Family entertainment centre · Museum · Arena · Zoo aquarium · Other | — | — | `setAiVenueSettings` body |
| Is outdoor `isOutdoor` | toggle | optional | on | — | — | Outdoor venues take the summer-heat and weather effects. | `setAiVenueSettings` body |
| Capacity `capacity` | number field | optional | — | min 1 | — | — | `setAiVenueSettings` body |
| Opening hours `openingHours` | repeatable rows | optional | — | — | — | The usual week. Exceptions come from the venue calendar. | `setAiVenueSettings` body |
| Day of week `openingHours[].dayOfWeek` | stepper or slider | optional | — | min 1; max 7 | — | — | `setAiVenueSettings` body |
| Opens at `openingHours[].opensAt` | text field | optional | — | — | — | — | `setAiVenueSettings` body |
| Closes at `openingHours[].closesAt` | text field | optional | — | — | — | — | `setAiVenueSettings` body |
| Typical weekday attendance `typicalWeekdayAttendance` | number field | optional | — | min 0 | — | — | `setAiVenueSettings` body |
| Typical weekend attendance `typicalWeekendAttendance` | number field | optional | — | min 0 | — | — | `setAiVenueSettings` body |
| Peak months `peakMonths` | list of values (chips) | optional | — | — | — | — | `setAiVenueSettings` body |
| Average spend `averageSpend` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setAiVenueSettings` body |
| Fnb attach rate `fnbAttachRate` | stepper or slider (%) | optional | — | min 0; max 1 | — | — | `setAiVenueSettings` body |
| Staff productivity `staffProductivity` | key and value settings | optional | — | — | — | Per role, units per staff hour, e.g. `{"cashier": 40, "gate": 300}`. | `setAiVenueSettings` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

#### Outputs: what the screen shows and produces

**Shown**

**Configuration Objects** (metric tile)

**Ready** (metric tile)

**Warnings** (metric tile)

**Blocking Issues** (metric tile)

**Approval Requirements** (metric tile)

**AI Recommendations** (metric tile)

**Modules Affected** (metric tile)

**Production Impact** (metric tile)

**Venue AI profile** (detail panel, from `getAiVenueSettings`): **What every AI answer stands on before the venue has history** (29 September, AI functions review). Collected at onboarding, here or by the configuration assistant in conversation.

| Shows | Format | Notes |
|---|---|---|
| Venue type | chip: Water park, Theme park, Family entertainment centre, Museum, Arena, Zoo aquarium… | — |
| Capacity | 1,234 | — |
| Opening hours | list or chips (count when long) | The usual week. Exceptions come from the venue calendar. |
| Typical weekday attendance | 1,234 | — |
| Typical weekend attendance | 1,234 | — |
| Peak months | list or chips (count when long) | — |
| Average spend | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Fnb attach rate | 12.5% | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save venue AI profile (primary button) | `setAiVenueSettings` PUT `/venues/{venueId}/ai-settings` | AiVenueSettings | AiVenueSettings | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Data it reads**: `getEffectiveAiPolicy` (onLoad, The policy in force for a capability at a scope); `getActionPlan` (onLoad, A plan with its steps); `getAiVenueSettings` (onLoad, The venue AI profile the baselines use)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-490` Configuration Validation Results: *Configuration Validation Results*; carries `planId`
- → `ADM-491` AI Recommendations & Best-Practice Review: *AI Recommendations & Best-Practice Review*
- → `ADM-492` Configuration Approval Workflow: *Configuration Approval Workflow*; carries `planId`
- → `ADM-493` AI Configuration Execution Center: *AI Configuration Execution Center*; carries `planId`
- → `ADM-494` Execution Progress & Dependency Monitor: *Execution Progress & Dependency Monitor*; carries `planId`, `stepNumber`
- → `ADM-495` Configuration Results & Object Mapping: *Configuration Results & Object Mapping*; carries `planId`
- → `ADM-496` Configuration Change & Modification Assistant: *Configuration Change & Modification Assistant*
- → `ADM-497` Configuration History, Versions & Rollback: *Configuration History, Versions & Rollback*; carries `planId`
- → `ADM-498` AI Configuration Audit & Governance: *AI Configuration Audit & Governance*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The readiness list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the readiness untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No readiness yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the readiness are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getEffectiveAiPolicy` → `AI_USE` (operate) · staff
- `getActionPlan` → `AI_USE` (operate) · staff
- `getAiVenueSettings` → `AI_USE` (operate) · staff
- `setAiVenueSettings` → `AI_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-489` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-489`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 1: Opens AI Configuration Readiness Center → Provide a final readiness assessment before the proposed Configuration Plan can enter approval or execution. This is the first governance gate.
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F227 branch at step 1 (expected): when Nothing has been set up on AI Configuration Readiness Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F227 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-489?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save venue AI profile.
- [ ] Every transition is wired: `ADM-002`, `ADM-490`, `ADM-491`, `ADM-492`, `ADM-493`, `ADM-494`, `ADM-495`, `ADM-496`, `ADM-497`, `ADM-498`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-490` Configuration Validation Results

**Provide detailed evidence that the proposed configuration has passed all required TICVAI validation layers. Screen 1 provides the summary; Screen 2 provides the technical and business evidence.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `planId` (navigation) |
| Route | `/platform/configuration-validation-results-adm-490` |

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

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps)

**Where the user goes next**

- → `ADM-489` AI Configuration Readiness Center: *Back to AI Configuration Readiness Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The validation results list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the validation results untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No validation results yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the validation results are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The plan is executing or finished; simulate a rollback plan instead. |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `simulateActionPlan` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-490` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-490`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 2: Works in Configuration Validation Results → Provide detailed evidence that the proposed configuration has passed all required TICVAI validation layers. Screen 1 provides the summary; Screen 2 provides the technical and business evidence.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-490?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-489`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-491` AI Recommendations & Best-Practice Review

**Separate mandatory configuration from AI recommendations so the administrator understands what This is important for trust and governance.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track) and no metric row |
| Offline | online only |
| Opens with | `decisionKey` (navigation), `sessionId` (session) |
| Route | `/platform/ai-recommendations-best-practice-review-adm-491` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | text field | — | — | `getConfigurationBlueprint` ?module |
| Decision class | segmented control | — | Required · Recommended · Optional | `getConfigurationBlueprint` ?decisionClass |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every recommendations best-practice review** (data table)

| Shows | Format | Notes |
|---|---|---|
| Recommendation | text | not in the schema: `Recommendation` |
| Family package | text | not in the schema: `Family Package` |
| Decision | text | not in the schema: `Decision` |
| Rejected | text | not in the schema: `Rejected` |
| By | text | not in the schema: `By` |
| Administrator | text | not in the schema: `Administrator` |
| Reason | text | not in the schema: `Reason` |

**The selected recommendations best-practice review** (detail panel): The pack groups this record's detail under its own headings: “Where available”.

| Shows | Format | Notes |
|---|---|---|
| Recommendation | text | not in the schema: `Recommendation` |
| Family package | text | not in the schema: `Family Package` |
| Decision | text | not in the schema: `Decision` |
| Rejected | text | not in the schema: `Rejected` |
| By | text | not in the schema: `By` |
| Administrator | text | not in the schema: `Administrator` |
| Reason | text | not in the schema: `Reason` |

**Data it reads**: `getConfigurationBlueprint` (onLoad, The blueprint so far)

**Where the user goes next**

- → `ADM-489` AI Configuration Readiness Center: *Back to AI Configuration Readiness Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendations best-practice review list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendations best-practice review untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendations best-practice review yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendations best-practice review are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The session is no longer open for decisions (`session-not-open`). |

#### Permissions

- `getConfigurationBlueprint` → `AI_USE` (operate) · staff
- `decideBlueprintRecommendation` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-491` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-491`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 4: Works in AI Recommendations & Best-Practice Review → Separate mandatory configuration from AI recommendations so the administrator understands what This is important for trust and governance.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-491?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-489`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-492` Configuration Approval Workflow

**Route the proposed AI configuration through TICVAI's existing RBAC/PBAC and approval governance before execution. The AI Assistant should reuse the central TICVAI approval engine, not create an independent approval system.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE`, `PRODUCT_CONFIGURE` (1 operate, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `actionId` (navigation), `planId` (navigation) |
| Route | `/platform/configuration-approval-workflow-adm-492` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve workflow (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `listProposedActions` (onLoad, What the assistant has proposed and nobody has decided)

**Where the user goes next**

- → `ADM-489` AI Configuration Readiness Center: *Back to AI Configuration Readiness Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval workflow list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval workflow yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval workflow are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213). |

#### Permissions

- `approveWorkflow` → `PRODUCT_CONFIGURE` (configure) · staff
- `getActionPlan` → `AI_USE` (operate) · staff
- `listProposedActions` → `AI_USE` (operate) · staff
- `decideProposedAction` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.4 | Approval Before Execution AI recommendations affecting pricing or financial operations shall require approval before execution | Unified Operations Dashboard | CONTRACTED | `decideProposedAction` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-492` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-492`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 6: Works in Configuration Approval Workflow → Route the proposed AI configuration through TICVAI's existing RBAC/PBAC and approval governance before execution. The AI Assistant should reuse the central TICVAI approval engine, not create an …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-492?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve workflow, Cancel.
- [ ] Every transition is wired: `ADM-489`.
- [ ] Every gated control is gated: `AI_USE`, `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-493` AI Configuration Execution Center

**Execute the approved Configuration Plan against the appropriate TICVAI modules in a controlled and traceable sequence. This is where proposed configuration becomes real TICVAI configuration.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_USE` (2 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `planId` (navigation) |
| Route | `/platform/ai-configuration-execution-center-adm-493` |

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
| Cancel action plan (destructive button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps)

**Where the user goes next**

- → `ADM-489` AI Configuration Readiness Center: *Back to AI Configuration Readiness Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The execution list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the execution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No execution yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the execution are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The plan is already finished.; 409 The plan is not executing. |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `pauseActionPlan` → `AI_APPROVE` (operate) · staff
- `cancelActionPlan` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-493` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-493`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 8: Works in AI Configuration Execution Center → Execute the approved Configuration Plan against the appropriate TICVAI modules in a controlled and traceable sequence. This is where proposed configuration becomes real TICVAI configuration.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-493?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel action plan, Cancel.
- [ ] Every transition is wired: `ADM-489`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-494` Execution Progress & Dependency Monitor

**Provide a detailed real-time view of execution dependencies, failures, retries, and downstream configuration status.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_USE` (2 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `planId` (navigation), `stepNumber` (navigation) |
| Route | `/platform/execution-progress-dependency-monitor-adm-494` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every execution progress dependency** (data table)

| Shows | Format | Notes |
|---|---|---|
| Venue ✓ | text | not in the schema: `Venue ✓` |
| ↓ | text | not in the schema: `↓` |
| Operating calendar ✓ | text | not in the schema: `Operating Calendar ✓` |
| Products ✓ | text | not in the schema: `Products ✓` |
| Timeslots ✓ | text | not in the schema: `Timeslots ✓` |
| Capacity ● | text | not in the schema: `Capacity ●` |
| Pricing ○ | text | not in the schema: `Pricing ○` |
| Channels ○ | text | not in the schema: `Channels ○` |
| Media ○ | text | not in the schema: `Media ○` |
| Access ○ | text | not in the schema: `Access ○` |
| Status | text | not in the schema: `Status` |
| Waiting | text | not in the schema: `Waiting` |
| Executing | text | not in the schema: `Executing` |
| Success | text | not in the schema: `Success` |
| Warning | text | not in the schema: `Warning` |
| Failed | text | not in the schema: `Failed` |
| Skipped | text | not in the schema: `Skipped` |
| Rolled back | text | not in the schema: `Rolled Back` |
| Failure example | text | not in the schema: `Failure Example` |
| 🔴 pricing profile creation failed | text | not in the schema: `🔴 Pricing Profile Creation Failed` |
| Weekend adult pricing | text | not in the schema: `Weekend Adult Pricing` |

**The selected execution progress dependency** (detail panel): The pack groups this record's detail under its own headings: “Blocked”, “Retry History”, “Resolution Applied”.

| Shows | Format | Notes |
|---|---|---|
| Venue ✓ | text | not in the schema: `Venue ✓` |
| ↓ | text | not in the schema: `↓` |
| Operating calendar ✓ | text | not in the schema: `Operating Calendar ✓` |
| Products ✓ | text | not in the schema: `Products ✓` |
| Timeslots ✓ | text | not in the schema: `Timeslots ✓` |
| Capacity ● | text | not in the schema: `Capacity ●` |
| Pricing ○ | text | not in the schema: `Pricing ○` |
| Channels ○ | text | not in the schema: `Channels ○` |
| Media ○ | text | not in the schema: `Media ○` |
| Access ○ | text | not in the schema: `Access ○` |
| Status | text | not in the schema: `Status` |
| Waiting | text | not in the schema: `Waiting` |
| Executing | text | not in the schema: `Executing` |
| Success | text | not in the schema: `Success` |
| Warning | text | not in the schema: `Warning` |
| Failed | text | not in the schema: `Failed` |
| Skipped | text | not in the schema: `Skipped` |
| Rolled back | text | not in the schema: `Rolled Back` |
| Failure example | text | not in the schema: `Failure Example` |
| 🔴 pricing profile creation failed | text | not in the schema: `🔴 Pricing Profile Creation Failed` |
| Weekend adult pricing | text | not in the schema: `Weekend Adult Pricing` |

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps)

**Where the user goes next**

- → `ADM-489` AI Configuration Readiness Center: *Back to AI Configuration Readiness Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The execution progress dependency list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the execution progress dependency untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No execution progress dependency yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the execution progress dependency are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not resumable: the plan is not paused (`plan-not-paused`), or a target object changed since planning (`plan-drifted`).; 409 Not retryable: the step has not failed (`step-not-failed`) or has used its 3 attempts (`retry-limit-reached`).; 409 The plan is not executing. |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `pauseActionPlan` → `AI_APPROVE` (operate) · staff
- `resumeActionPlan` → `AI_APPROVE` (operate) · staff
- `retryActionStep` → `AI_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-494` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-494`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 10: Works in Execution Progress & Dependency Monitor → Provide a detailed real-time view of execution dependencies, failures, retries, and downstream configuration status.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (42 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-494?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-489`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-495` Configuration Results & Object Mapping

**Show exactly what TICVAI objects were created or changed after successful execution.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_USE` (2 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `planId` (navigation) |
| Route | `/platform/configuration-results-object-mapping-adm-495` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every results object mapping** (data table)

| Shows | Format | Notes |
|---|---|---|
| VEN 1028 | text | not in the schema: `VEN-1028` |
| ↓ | text | not in the schema: `↓` |
| TKT 4012 | text | not in the schema: `TKT-4012` |
| SCH 0291 | text | not in the schema: `SCH-0291` |
| CAP 0218 | text | not in the schema: `CAP-0218` |
| PRC 3002 | text | not in the schema: `PRC-3002` |
| MED 0082 | text | not in the schema: `MED-0082` |
| ACC 0142 | text | not in the schema: `ACC-0142` |

**The selected results object mapping** (detail panel): The pack groups this record's detail under its own headings: “Object Mapping”, “Created does not necessarily mean”, “Pending”.

| Shows | Format | Notes |
|---|---|---|
| VEN 1028 | text | not in the schema: `VEN-1028` |
| ↓ | text | not in the schema: `↓` |
| TKT 4012 | text | not in the schema: `TKT-4012` |
| SCH 0291 | text | not in the schema: `SCH-0291` |
| CAP 0218 | text | not in the schema: `CAP-0218` |
| PRC 3002 | text | not in the schema: `PRC-3002` |
| MED 0082 | text | not in the schema: `MED-0082` |
| ACC 0142 | text | not in the schema: `ACC-0142` |

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps)

**Where the user goes next**

- → `ADM-489` AI Configuration Readiness Center: *Back to AI Configuration Readiness Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The results object mapping list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the results object mapping untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No results object mapping yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the results object mapping are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Nothing to roll back: the plan has no completed step (`plan-not-applied`). |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `rollbackActionPlan` → `AI_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-495` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-495`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 12: Works in Configuration Results & Object Mapping → Show exactly what TICVAI objects were created or changed after successful execution.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-495?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-489`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-496` Configuration Change & Modification Assistant

**Allow administrators to return later and modify existing TICVAI configuration through natural-language AI. This is what transforms the feature from an onboarding wizard into a permanent AI configuration capability.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `sessionId` (session) |
| Route | `/platform/configuration-change-modification-assistant-adm-496` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Prepare Change / Ask More / Cancel. Each needs an operation, or needs removing from the screen; this is the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Prepare Change / Ask More / Cancel (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-489` AI Configuration Readiness Center: *Back to AI Configuration Readiness Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The change modification assistant list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the change modification assistant untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No change modification assistant yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the change modification assistant are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The blueprint is not ready: a required decision is open or deferred (AIC-115).; 409 The session is no longer discovering (`session-not-open`). |

#### Permissions

- `startConfigurationSession` → `AI_USE` (operate) · staff
- `answerConfigurationQuestion` → `AI_USE` (operate) · staff
- `buildConfigurationPlan` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-496` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-496`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 14: Works in Configuration Change & Modification Assistant → Allow administrators to return later and modify existing TICVAI configuration through natural-language AI. This is what transforms the feature from an onboarding wizard into a permanent AI …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-496?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Prepare Change / Ask More / Cancel, Cancel.
- [ ] Every transition is wired: `ADM-489`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-497` Configuration History, Versions & Rollback

**Maintain complete version history for AI-created and AI-modified configuration and provide governed rollback capability where technically possible.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_USE` (2 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `planId` (navigation) |
| Route | `/platform/configuration-history-versions-rollback-adm-497` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Discovering · Blueprint ready · Planned · Executing · Completed · Abandoned | `listConfigurationSessions` ?status |
| Intent | radio group | — | Create · Modify · Extend · Clone | `listConfigurationSessions` ?intent |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `listConfigurationSessions` (onLoad, Configuration-assistant sessions)

**Where the user goes next**

- → `ADM-489` AI Configuration Readiness Center: *Back to AI Configuration Readiness Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The history versions rollback list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the history versions rollback untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No history versions rollback yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the history versions rollback are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Nothing to roll back: the plan has no completed step (`plan-not-applied`). |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `rollbackActionPlan` → `AI_APPROVE` (operate) · staff
- `listConfigurationSessions` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-497` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-497`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 16: Works in Configuration History, Versions & Rollback → Maintain complete version history for AI-created and AI-modified configuration and provide governed rollback capability where technically possible.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-497?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-489`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-498` AI Configuration Audit & Governance

**Provide an immutable governance record showing how AI participated in every configuration decision and execution. This is essential for an enterprise AI system.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Header KPIs; Show) and a per-row directory (§For each configuration value show) — counts over a population, then the population |
| Offline | online only |
| Opens with | `decisionRecordId` (navigation) |
| Route | `/platform/ai-configuration-audit-governance-adm-498` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search audit governance | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, user, date, session, configuration plan and 13 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Capability key | text field | — | — | `searchAiDecisions` ?capabilityKey |
| Outcome | select | — | Answered · Refused · Allowed · Blocked · Executed · Failed · Approved then failed · Published · Suggested | `searchAiDecisions` ?outcome |
| Subject ref | text field | — | — | `searchAiDecisions` ?subjectRef |
| Trace | text field | — | — | `searchAiDecisions` ?traceId |
| Policy version | text field | — | — | `searchAiDecisions` ?policyVersion |
| Model version | text field | — | — | `searchAiDecisions` ?modelVersion |
| From | date and time picker | — | — | `searchAiDecisions` ?from |
| To | date and time picker | — | — | `searchAiDecisions` ?to |

#### Outputs: what the screen shows and produces

**Shown**

**AI Configuration Sessions** (metric tile)

**AI Recommendations** (metric tile)

**Accepted** (metric tile)

**Rejected** (metric tile)

**Executed Changes** (metric tile)

**Rollbacks** (metric tile)

**Approval Overrides** (metric tile)

**Failed Executions** (metric tile)

**User Request** (metric tile)

**↓** (metric tile)

**AI Interpretation** (metric tile)

**Blueprint Decision** (metric tile)

**Configuration Object** (metric tile)

**Validation** (metric tile)

**Approval** (metric tile)

**Execution** (metric tile)

**Audit Requirements** (metric tile)

**Original User Intent** (metric tile)

**AI Recommendation** (metric tile)

**User Decision** (metric tile)

**Configuration Plan** (metric tile)

**Before / After** (metric tile)

**Validation Results** (metric tile)

**Failure / Retry** (metric tile)

**Rollback** (metric tile)

**Timestamp** (metric tile)

**Actor** (metric tile)

**Correlation / Trace ID** (metric tile)

**Every audit governance** (data table)

| Shows | Format | Notes |
|---|---|---|
| Source | text | not in the schema: `Source` |
| 👤 user provided | text | not in the schema: `👤 User Provided` |
| 🤖 AI recommended | text | not in the schema: `🤖 AI Recommended` |
| ⚙ system derived | text | not in the schema: `⚙ System Derived` |
| 📋 existing configuration | text | not in the schema: `📋 Existing Configuration` |

**The selected audit governance** (detail panel): The pack groups this record's detail under its own headings: “Objects”, “Timeslots 24 System Derived Operations”, “Critical Execution Architecture”, “The architecture should be”, “Owning TICVAI Modules”, “Execution Dependency Engine”.

| Shows | Format | Notes |
|---|---|---|
| Source | text | not in the schema: `Source` |
| 👤 user provided | text | not in the schema: `👤 User Provided` |
| 🤖 AI recommended | text | not in the schema: `🤖 AI Recommended` |
| ⚙ system derived | text | not in the schema: `⚙ System Derived` |
| 📋 existing configuration | text | not in the schema: `📋 Existing Configuration` |

**Data it reads**: `searchAiDecisions` (onLoad, Find AI decisions)

**Where the user goes next**

- → `ADM-489` AI Configuration Readiness Center: *Back to AI Configuration Readiness Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The audit governance list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the audit governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No audit governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the audit governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `searchAiDecisions` → `AI_AUDIT_VIEW` (read) · staff
- `getAiDecisionTrace` → `AI_AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.6 | AI-based Dynamic Pricing Promotion | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |
| 8.2.58 | System shall maintain forecasting audit logs. | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |
| 8.3.53 | System shall maintain fraud audit trails. | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |
| 8.6.29 | System shall support recommendation audit trails. | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI-prepared configuration keeps full version history, e.g. every price change shows who suggested it, who approved it and when it was published. *(client request · MoM 18 Sep 2026, 4.7 AI Configuration Assistant — Approval, Execution & Audit Trail · DI-938)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-498` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS11 AI Configuration Assistant Board 3.dc.html#adm-498`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 3
- Flow F227 *AI Configuration Assistant board 3: AI Configuration Readiness Center*, step 18: Works in AI Configuration Audit & Governance → Provide an immutable governance record showing how AI participated in every configuration decision and execution. This is essential for an enterprise AI system.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-498?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-489`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

### In P09 · Platform

- **Open question.** Open: should AI monitoring live in one centralised AI command dashboard or be distributed as widgets in each functional module's own dashboard? Allam: Softlabs' call; the current proposal is illustrative and Softlabs may propose a better structure. *(open · MoM 18 Sep 2026, 4.4 AI Governance — Risk, Compliance & Continuous Monitoring · DI-936)*

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"answerConfigurationQuestion": {"method":"POST","path":"/configuration-sessions/{sessionId}/answers","contract":"ai","summary":"Answer the current question","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiConfigurationTurn"},
"approveWorkflow": {"method":"PUT","path":"/workflow","contract":"catalogue","summary":"Approval Workflow Designer","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalWorkflowDesignerInput","responds":"ApprovalWorkflowDesignerView"},
"buildConfigurationPlan": {"method":"POST","path":"/configuration-sessions/{sessionId}/plan","contract":"ai","summary":"Compile the blueprint into a plan","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlanDetail"},
"cancelActionPlan": {"method":"POST","path":"/action-plans/{planId}/cancel","contract":"ai","summary":"Cancel a plan","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlan"},
"decideBlueprintRecommendation": {"method":"POST","path":"/configuration-sessions/{sessionId}/decisions/{decisionKey}","contract":"ai","summary":"Accept, modify, reject or defer a blueprint decision","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiBlueprintDecision"},
"decideProposedAction": {"method":"POST","path":"/proposed-actions/{actionId}/decide","contract":"ai","summary":"Approve or reject a proposal","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProposedAction"},
"getActionPlan": {"method":"GET","path":"/action-plans/{planId}","contract":"ai","summary":"A plan with its steps","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiActionPlanDetail"},
"getAiDecisionTrace": {"method":"GET","path":"/decision-records/{decisionRecordId}/trace","contract":"ai","summary":"The full trace of a decision","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"depth","in":"query","required":null}],"requestBody":null,"responds":"AiDecisionTrace"},
"getAiVenueSettings": {"method":"GET","path":"/venues/{venueId}/ai-settings","contract":"ai","summary":"The venue AI profile the baselines stand on","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiVenueSettings"},
"getConfigurationBlueprint": {"method":"GET","path":"/configuration-sessions/{sessionId}/blueprint","contract":"ai","summary":"The blueprint so far","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"module","in":"query","required":null},{"name":"decisionClass","in":"query","required":null}],"requestBody":null,"responds":"AiBlueprintView"},
"getEffectiveAiPolicy": {"method":"GET","path":"/governance/effective-policy","contract":"ai","summary":"The policy in force for a capability at a scope","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"capabilityKey","in":"query","required":true},{"name":"scopePath","in":"query","required":null},{"name":"environment","in":"query","required":null}],"requestBody":null,"responds":"AiEffectivePolicy"},
"listConfigurationSessions": {"method":"GET","path":"/configuration-sessions","contract":"ai","summary":"Configuration-assistant sessions","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"intent","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProposedActions": {"method":"GET","path":"/proposed-actions","contract":"ai","summary":"What the assistant has proposed and nobody has decided","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProposedAction"},
"pauseActionPlan": {"method":"POST","path":"/action-plans/{planId}/pause","contract":"ai","summary":"Pause an executing plan","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlan"},
"resumeActionPlan": {"method":"POST","path":"/action-plans/{planId}/resume","contract":"ai","summary":"Resume a paused plan","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlan"},
"retryActionStep": {"method":"POST","path":"/action-plans/{planId}/steps/{stepNumber}/retry","contract":"ai","summary":"Retry a failed step","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionStep"},
"rollbackActionPlan": {"method":"POST","path":"/action-plans/{planId}/rollback","contract":"ai","summary":"Plan a rollback","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"searchAiDecisions": {"method":"GET","path":"/decision-records","contract":"ai","summary":"Find AI decisions","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"capabilityKey","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"subjectRef","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"traceId","in":"query","required":null},{"name":"policyVersion","in":"query","required":null},{"name":"modelVersion","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setAiVenueSettings": {"method":"PUT","path":"/venues/{venueId}/ai-settings","contract":"ai","summary":"Set the venue AI profile","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiVenueSettings","responds":"AiVenueSettings"},
"simulateActionPlan": {"method":"POST","path":"/action-plans/{planId}/simulate","contract":"ai","summary":"Validate and simulate a plan without changing anything","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlanDetail"},
"startConfigurationSession": {"method":"POST","path":"/configuration-sessions","contract":"ai","summary":"Start the configuration assistant","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiConfigurationSession"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiActionPlan": {"type":"object","x-ticvai-persistence":"ai.action_plan","description":"**A plan: plan, validate, simulate, approve, execute, with rollback** (design 2.2 D, 3.8; AIC-086..107). Independent of any conversation (AIC-102). Its steps are `ai.action_step`; the change set is hashed so what was approved is what runs (AIC-181).","required":["origin","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"origin":{"type":"string","enum":["configurationSession","generateConfiguration","assistant","riskCase","operationalRequirement","rollback"]},"originRef":{"type":"string","nullable":true},"summary":{"type":"string"},"status":{"type":"string","enum":["draft","validated","simulated","awaitingApproval","approved","executing","paused","completed","partiallyCompleted","failed","compensated","cancelled","rolledBack"],"readOnly":true},"autonomyLevel":{"$ref":"#/components/schemas/AiAutonomyLevel"},"approvalTier":{"type":"integer","minimum":1,"maximum":2,"description":"The approval tier (1 or 2), the floor the approvals matrix adds to (design 3.8). Not an autonomy level."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request, where tier 2 or the matrix caught the plan."},"proposedActionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.proposed_action","description":"The `ai.proposed_action` the plan is presented as for a decision."},"changeSetHash":{"type":"string","readOnly":true},"governanceOutcome":{"allOf":[{"$ref":"#/components/schemas/AiGovernanceOutcome"}],"readOnly":true},"policyVersionRef":{"type":"string","readOnly":true,"description":"The governance policy version that decided it."},"simulation":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"Current versus proposed state, channels, future orders and issued tickets affected (flow D step 4)."},"partialCompletionAllowed":{"type":"boolean","default":false,"description":"Where governance allows a partial completion; otherwise a failure compensates in reverse dependency order (AIC-098, AIC-134)."},"rollbackOfPlanId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.action_plan"},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiActionPlanDetail": {"type":"object","x-ticvai-persistence":"none — ai.action_plan with its ai.action_step rows","description":"A plan with its steps in DAG order.","required":["plan","steps"],"properties":{"plan":{"$ref":"#/components/schemas/AiActionPlan"},"steps":{"type":"array","items":{"$ref":"#/components/schemas/AiActionStep"}}}},
"AiActionStep": {"type":"object","x-ticvai-persistence":"ai.action_step","description":"One step of a plan: a registered tool against `targetContract.targetOperation` at a contract version (AIC-095), with payload, provenance, compensation and the idempotency key `plan:{id}:step:{n}`. **Scoped through its plan** (`platform.apply_parent_rls`). Each step records its target object's version; drift pauses the plan (AIC-182).","required":["planId","stepNumber","toolKey","targetContract","targetOperation","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"planId":{"type":"string","format":"uuid","x-ticvai-references":"ai.action_plan"},"stepNumber":{"type":"integer","minimum":1},"dependsOn":{"type":"array","items":{"type":"integer","minimum":1},"description":"Step numbers that must succeed first. The plan is a DAG."},"toolKey":{"type":"string"},"targetContract":{"type":"string"},"targetOperation":{"type":"string"},"contractVersion":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body of `targetOperation`, validated against it before the plan is approved."},"provenance":{"$ref":"#/components/schemas/AiProvenance"},"idempotencyKey":{"type":"string","readOnly":true},"targetObjectRef":{"type":"string","nullable":true},"targetObjectVersion":{"type":"string","nullable":true,"description":"The version the step was planned against. A different version at execution is drift."},"reversible":{"type":"boolean"},"compensation":{"type":"object","additionalProperties":true,"nullable":true},"status":{"type":"string","enum":["pending","validated","running","succeeded","failed","compensated","skipped","paused"],"readOnly":true},"attempts":{"type":"integer","minimum":0,"maximum":3,"readOnly":true,"description":"Bounded at 3 (AIC-135)."},"lastError":{"type":"string","nullable":true,"readOnly":true},"resultRef":{"type":"string","nullable":true,"readOnly":true,"description":"The owning service's response: success is its answer, not a model's judgement (AIC-097)."},"startedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"AiAutonomyLevel": {"type":"integer","minimum":0,"maximum":4,"description":"**One autonomy scale for every capability** (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). 0 disabled; 1 advisory (explains and recommends, nothing is drafted to run); 2 prepare (drafts a proposal a person applies in the owning screen); 3 execute with approval (the plan runs after approval, through owning APIs); 4 controlled auto (runs without approval, only for listed low-risk reversible actions inside pre-approved ranges). **Not the approval tier**: `ProposedAction.approvalLevel` is the tier."},
"AiBlueprintDecision": {"type":"object","x-ticvai-persistence":"ai.blueprint_decision","description":"One decision in a blueprint and what the administrator did with it. **Scoped through its blueprint** (`platform.apply_parent_rls`).","required":["blueprintId","decisionKey","decisionClass","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"blueprintId":{"type":"string","format":"uuid","x-ticvai-references":"ai.blueprint"},"decisionKey":{"type":"string"},"module":{"type":"string"},"decisionClass":{"type":"string","enum":["required","recommended","optional"]},"question":{"type":"string","nullable":true},"value":{"type":"object","additionalProperties":true,"nullable":true},"provenance":{"$ref":"#/components/schemas/AiProvenance"},"sourceId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.config_source","description":"The attached document the value was extracted from (29 September, build; `attachConfigurationSource`)."},"sourceCitation":{"type":"string","nullable":true,"maxLength":200,"description":"Where in it, e.g. `page 4`, `sheet Prices!B7`, `logo region`."},"recommendation":{"type":"object","additionalProperties":true,"nullable":true,"description":"What the assistant recommends and why (ADM-491): mandatory configuration and best practice kept apart."},"status":{"type":"string","enum":["open","accepted","modified","rejected","deferred"]},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"note":{"type":"string","nullable":true}}},
"AiBlueprintView": {"type":"object","x-ticvai-persistence":"none — ai.blueprint with its ai.blueprint_decision rows","description":"A blueprint with its decisions.","required":["blueprint","decisions"],"properties":{"blueprint":{"$ref":"#/components/schemas/AiConfigurationBlueprint"},"decisions":{"type":"array","items":{"$ref":"#/components/schemas/AiBlueprintDecision"}}}},
"AiConfigurationBlueprint": {"type":"object","x-ticvai-persistence":"ai.blueprint","description":"**The blueprint** (design 2.2 D step 2, ADM-478): decisions, severity-graded issues and a dependency map. **Never `ready` while a required decision is deferred** (AIC-115).","required":["sessionId","version","readiness"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"sessionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.config_session"},"version":{"type":"integer","minimum":1},"readiness":{"type":"string","enum":["notReady","readyWithWarnings","ready"],"readOnly":true},"requiredOpen":{"type":"integer","minimum":0,"readOnly":true,"description":"Required decisions not yet accepted or modified."},"issues":{"$ref":"#/components/schemas/AiBlueprintIssueList"},"dependencyMap":{"type":"object","additionalProperties":true,"readOnly":true,"description":"Configuration objects and the order they depend on each other, by module."},"summary":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiConfigurationQuestion": {"type":"object","x-ticvai-persistence":"none — chosen per turn from the configuration knowledge model","description":"**The next question, chosen by the configuration knowledge model, not by the language model** (design 2.2 D, AIC-111). The model only extracts a structured answer against `answerSchema`.","required":["questionKey","text","decisionClass"],"properties":{"questionKey":{"type":"string"},"text":{"type":"string"},"module":{"type":"string","nullable":true},"decisionClass":{"type":"string","enum":["required","recommended","optional"]},"answerType":{"type":"string","enum":["freeText","singleChoice","multiChoice","number","date","confirm"]},"options":{"type":"array","items":{"type":"string"}},"why":{"type":"string","nullable":true,"description":"Why it is asked: which configuration branch it opens or closes."},"answerSchema":{"type":"object","additionalProperties":true,"nullable":true,"description":"JSON Schema the extracted answer must satisfy."}}},
"AiConfigurationSession": {"type":"object","x-ticvai-persistence":"ai.config_session","description":"**A configuration-assistant session** (design 2.2 D steps 1-2, C7; ADM-469..478). Discovery runs from the configuration knowledge model; every value carries provenance.","required":["intent","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"intent":{"type":"string","enum":["create","modify","extend","clone"]},"venueType":{"type":"string","nullable":true,"description":"Museum, theme park, water park, zoo, aquarium, theatre, stadium, festival, conference..."},"sourceScopePath":{"type":"string","nullable":true,"description":"The setup being cloned or extended."},"status":{"type":"string","enum":["discovering","blueprintReady","planned","executing","completed","abandoned"],"readOnly":true},"progressPercent":{"type":"integer","minimum":0,"maximum":100,"readOnly":true},"nextQuestion":{"allOf":[{"$ref":"#/components/schemas/AiConfigurationQuestion"}],"nullable":true,"readOnly":true},"conversationId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.conversation"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan"},"locale":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"startedAt":{"type":"string","format":"date-time","readOnly":true},"lastActivityAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiConfigurationTurn": {"type":"object","x-ticvai-persistence":"none — the answer is written to ai.blueprint_decision and the session","description":"The result of one answer: what was extracted with its provenance, the next question and progress.","required":["session"],"properties":{"session":{"$ref":"#/components/schemas/AiConfigurationSession"},"extracted":{"type":"array","items":{"type":"object","properties":{"decisionKey":{"type":"string"},"value":{"type":"object","additionalProperties":true,"nullable":true},"provenance":{"$ref":"#/components/schemas/AiProvenance"}}}},"nextQuestion":{"allOf":[{"$ref":"#/components/schemas/AiConfigurationQuestion"}],"nullable":true},"clarificationsNeeded":{"type":"array","items":{"type":"string"}}}},
"AiDecisionRecord": {"type":"object","x-ticvai-persistence":"ai.decision_record","description":"**The standard record for every governed decision** (design 3.9, C12; AIC-193..209): a recommendation summary, a risk assessment, a forecast publication, a plan step, an assistant answer at significant depth, a governance block, a Help me choose suggestion. **Append-only; corrections are annotations; hash-chained per tenant** so tampering is detectable (AIC-203, AIC-204). **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["traceId","capabilityKey","outcome","recordHash"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"traceId":{"type":"string"},"capabilityKey":{"type":"string"},"task":{"type":"string","nullable":true},"subjectKind":{"type":"string","nullable":true},"subjectRef":{"type":"string","nullable":true},"inputsRef":{"type":"string","nullable":true,"description":"Where the inputs are kept (Blob or `ai.activity`), never the prompt text itself."},"evidence":{"$ref":"#/components/schemas/AiEvidenceItemList"},"producer":{"type":"string","nullable":true},"modelVersion":{"type":"string","nullable":true},"promptTemplateVersion":{"type":"string","nullable":true},"featureSetVersion":{"type":"string","nullable":true},"knowledgeVersion":{"type":"string","nullable":true},"ruleVersions":{"type":"object","additionalProperties":true,"nullable":true},"governanceOutcome":{"allOf":[{"$ref":"#/components/schemas/AiGovernanceOutcome"}],"nullable":true},"policyVersion":{"type":"string","nullable":true},"approvals":{"type":"object","additionalProperties":true,"nullable":true,"description":"Approval requests and their decisions."},"humanDecision":{"type":"object","additionalProperties":true,"nullable":true,"description":"Override or intervention, where a person changed the outcome."},"executionResult":{"type":"object","additionalProperties":true,"nullable":true},"outcomeRef":{"type":"string","nullable":true,"description":"The business outcome it links to (an order, a published version, a closed case)."},"outcome":{"type":"string","enum":["answered","refused","allowed","blocked","executed","failed","approvedThenFailed","published","suggested"],"description":"`approvedThenFailed` is kept distinct from `executed` (design 1.2 Audit)."},"annotations":{"type":"array","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"byPrincipalId":{"type":"string","format":"uuid"},"note":{"type":"string"}}},"readOnly":true,"description":"Corrections, appended; the original fields are never edited."},"previousHash":{"type":"string","readOnly":true},"recordHash":{"type":"string","readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiDecisionTrace": {"type":"object","x-ticvai-persistence":"none — ai.decision_record with the rows it references","description":"**The full trace of one decision** (ADM-540..546): record, evidence, candidates and rules, model and runtime, governance and approvals, execution and business outcome. Depth is gated by permission (AIC-195).","required":["record"],"properties":{"record":{"$ref":"#/components/schemas/AiDecisionRecord"},"depth":{"type":"string","enum":["business","governance","technical"]},"explanation":{"type":"string","description":"Built from structured evidence, never a model's chain of thought (AIC-192)."},"activity":{"type":"array","items":{"$ref":"#/components/schemas/AiInteraction"},"description":"The model calls behind it (`technical` depth)."},"plan":{"allOf":[{"$ref":"#/components/schemas/AiActionPlanDetail"}],"nullable":true},"interventions":{"type":"array","items":{"$ref":"#/components/schemas/AiIntervention"}},"chainVerified":{"type":"boolean","description":"The hash chain around this record verifies."}}},
"AiEffectivePolicy": {"type":"object","x-ticvai-persistence":"none — resolved from published policy versions, exceptions and ai.policy","description":"**The policy in force for a capability at a scope** (AIC-153, AIC-165; ADM-525, ADM-528): the intersection of the capability, governance policy and the tenant or venue AI policy, with where each part came from.","required":["capabilityKey","autonomyLevel","rules"],"properties":{"capabilityKey":{"type":"string"},"scopePath":{"type":"string"},"autonomyLevel":{"$ref":"#/components/schemas/AiAutonomyLevel"},"autonomyCeiling":{"$ref":"#/components/schemas/AiAutonomyLevel"},"rules":{"type":"array","items":{"type":"object","properties":{"rule":{"$ref":"#/components/schemas/AiGovernanceRule"},"policyKey":{"type":"string"},"version":{"type":"integer"},"scopePath":{"type":"string"}}}},"exceptions":{"type":"array","items":{"$ref":"#/components/schemas/AiPolicyException"}},"conflicts":{"type":"array","items":{"type":"object","properties":{"description":{"type":"string"},"resolvedTo":{"$ref":"#/components/schemas/AiGovernanceOutcome"}}},"description":"Conflicting rules and the more restrictive result they resolved to (AIC-161)."},"resolvedAt":{"type":"string","format":"date-time"}}},
"AiEvidenceItemList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The evidence of one decision record, stored with it.","items":{"$ref":"#/components/schemas/AiEvidenceItem"}},
"AiGovernanceOutcome": {"type":"string","enum":["allow","allowWithConditions","prepareOnly","approvalRequired","escalate","block"],"description":"What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). `block` is an answer, not an error, and is logged as outcome `refused`."},
"AiGovernanceRule": {"type":"object","x-ticvai-persistence":"none — held in the jsonb rules column of ai.governance_policy_version, through AiGovernanceRuleList","description":"One rule of a governance policy version: which actions on which data, under which conditions, get which outcome (AIC-147..160).","required":["effect"],"properties":{"effect":{"$ref":"#/components/schemas/AiGovernanceOutcome"},"capabilityKeys":{"type":"array","items":{"type":"string"},"description":"Registered capabilities it applies to. Empty means every capability the policy names."},"actions":{"type":"array","items":{"type":"string","enum":["read","analyze","recommend","generate","prepare","create","modify","publish","execute","delete"]},"description":"ADM-523: what AI may do, from reading to executing."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories (ADM-524), e.g. `customerContact`, `payment`, `financial`, `operational`."},"purposes":{"type":"array","items":{"type":"string"},"description":"Permitted purposes for those categories (AIC-156, AIR-182)."},"maxAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Above this value the effect escalates one step (for example to `approvalRequired`)."},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Roles the rule applies to; empty means every role."},"environments":{"type":"array","items":{"type":"string","enum":["development","sandbox","staging","production"]},"description":"ADM-525. Empty means every environment. **`sandbox`** (18 September minutes, M18-01): the developer sandbox and a tenant's trial environment, governed apart from staging so a rule can allow in sandbox what it blocks in production."},"conditions":{"type":"object","additionalProperties":true,"nullable":true,"description":"Conditions attached to an `allowWithConditions` effect, for example `maskFields` or `requireCitation`."}}},
"AiInteraction": {"type":"object","x-ticvai-persistence":"ai.activity","required":["id","principalId","capability","outcome","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"conversationId":{"type":"string","format":"uuid","nullable":true},"principalId":{"type":"string","format":"uuid"},"audience":{"type":"string","enum":["staff","guest"],"description":"**Billing divides on this.** Staff usage is bounded by headcount; guest usage is bounded by footfall and curiosity, and a venue cannot stop guests asking questions.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest, where the audience is `guest`. `principalId` is null in that case — **a guest is not a principal**, and attributing their tokens to a staff member would be wrong twice.\n"},"billableToTenantId":{"type":"string","format":"uuid","description":"Resolved from `scopePath` at write time, not derived later. **Billing must not depend on walking a scope tree that has since been reorganised.**\n"},"scopePath":{"type":"string"},"capability":{"type":"string"},"prompt":{"type":"string"},"response":{"type":"string"},"sources":{"$ref":"#/components/schemas/AiSourceList"},"outcome":{"type":"string","enum":["answered","refused","applied","rejected","failed"]},"refusalReason":{"type":"string","nullable":true},"provider":{"$ref":"#/components/schemas/AiProviderKind"},"model":{"type":"string"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"cost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"x-ticvai-column":"cost_amount","description":"What the call cost at the provider. **Money like every other amount** (naming-and-style 5.1) — it replaces an integer `costMinor` that carried no currency or scale, which AED and OMR read differently.\n"},"latencyMs":{"type":"integer"},"maskedFieldCount":{"type":"integer","description":"How many fields were redacted. Zero on a prompt touching guest data is a defect."},"traceId":{"type":"string"},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"description":"The `ai.decision_record` this call belongs to, where it was part of a governed decision (AI design 2.3, 3.9). Null for a call audited by this row alone."},"cacheLayer":{"type":"string","nullable":true,"enum":["guardrail","semantic","exact","negative","analytics"],"description":"Which cache answered, where one did (AI design 3.6). Null for a model call."},"createdAt":{"type":"string","format":"date-time"}}},
"AiIntervention": {"type":"object","x-ticvai-persistence":"ai.intervention","description":"**A person stepping in** (AIC-187, ADM-535, ADM-536): an override, pause, resume, stop, retry or rollback, with the original AI decision and the human one side by side.","required":["kind","targetKind","targetRef"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["override","pause","resume","cancel","retry","rollback","capabilityPause","capabilityResume"]},"targetKind":{"type":"string","enum":["plan","step","decision","capability"]},"targetRef":{"type":"string"},"decisionRecordId":{"type":"string","format":"uuid","nullable":true},"originalDecision":{"type":"object","additionalProperties":true,"nullable":true},"humanDecision":{"type":"object","additionalProperties":true,"nullable":true},"reason":{"type":"string","maxLength":2000},"principalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiPolicyException": {"type":"object","x-ticvai-persistence":"ai.policy_exception","description":"**A temporary, recorded exception to a governance policy** (AIC-162, ADM-526): an expiry, an approver and compensating controls. Governance is never bypassed silently.","required":["policyId","reason","expiresAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"policyId":{"type":"string","format":"uuid","x-ticvai-references":"ai.governance_policy"},"capabilityKey":{"type":"string","nullable":true},"reason":{"type":"string","maxLength":2000},"compensatingControls":{"type":"array","items":{"type":"string"}},"startsAt":{"type":"string","format":"date-time","nullable":true},"expiresAt":{"type":"string","format":"date-time","description":"Required. An exception with no end is a policy change, and goes through publication."},"status":{"type":"string","enum":["active","expired","revoked"],"readOnly":true},"approvedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"revokedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"revokedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"revokeReason":{"type":"string","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiProvenance": {"type":"string","enum":["confirmed","aiRecommended","inferred","unknown"],"description":"**Where a configuration value came from** (design 2.2 D, AIC-111): said by the administrator, recommended by the assistant, inferred from other answers, or not known yet. Shown beside every value; no confidence number is shown for configuration (design 5.6)."},
"AiVenueSettings": {"type":"object","x-ticvai-persistence":"ai.venue_settings","description":"**The venue AI profile** (29 September, AI functions review): the figures a venue gives at onboarding so every data-driven answer is useful before it has history. One row per venue; configuration, not history. Defaults come from the starting pattern for `venueType`, which TICVAI writes from published sources and made-up example curves, **never from another tenant's data** (AI-D01, AIP-149).","required":["venueId","venueType"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"venueType":{"type":"string","enum":["waterPark","themePark","familyEntertainmentCentre","museum","arena","zooAquarium","other"]},"isOutdoor":{"type":"boolean","default":true,"description":"Outdoor venues take the summer-heat and weather effects."},"capacity":{"type":"integer","minimum":1,"nullable":true},"openingHours":{"type":"array","description":"The usual week. Exceptions come from the venue calendar.","items":{"type":"object","properties":{"dayOfWeek":{"type":"integer","minimum":1,"maximum":7},"opensAt":{"type":"string"},"closesAt":{"type":"string"}}}},"typicalWeekdayAttendance":{"type":"integer","minimum":0,"nullable":true},"typicalWeekendAttendance":{"type":"integer","minimum":0,"nullable":true},"peakMonths":{"type":"array","items":{"type":"integer","minimum":1,"maximum":12}},"averageSpend":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"fnbAttachRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"staffProductivity":{"type":"object","additionalProperties":{"type":"number"},"description":"Per role, units per staff hour, e.g. `{\"cashier\": 40, \"gate\": 300}`. Defaults from the pattern."},"startingPatternKey":{"type":"string","readOnly":true,"description":"The pattern and version in use, e.g. `waterPark@3`."},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"ApprovalWorkflowDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Approval Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"workflowName":{"type":"string","description":"Workflow name"},"applicableProductTypes":{"type":"array","items":{"$ref":"#/components/schemas/ProductKind"},"description":"Applicable product types; empty = all"},"venue":{"type":"string","description":"Venue id; empty = all venues","nullable":true},"department":{"type":"string","description":"Department","nullable":true},"changeTypes":{"type":"array","items":{"type":"string","enum":["newProduct","description","price","validity","capacity","entitlement","eligibility","tax","channel","media","policy","relationship","retirement"]},"description":"Change types routed to this workflow (Conditional Approval: e.g. price -> Commercial + Finance)"},"approvalStages":{"type":"array","items":{"type":"object","properties":{"order":{"type":"integer","description":"Stage order; stages sharing an order run in parallel, otherwise sequential"},"name":{"type":"string"},"approverRole":{"type":"string","nullable":true},"specificApproverId":{"type":"string","nullable":true},"approvalGroupId":{"type":"string","nullable":true},"mandatory":{"type":"boolean"},"slaHours":{"type":"integer","description":"SLA in hours"},"escalateToRole":{"type":"string","nullable":true,"description":"Escalation when the SLA is missed"},"delegationAllowed":{"type":"boolean"},"reminderEveryHours":{"type":"integer","nullable":true,"description":"Reminder frequency"}}},"description":"Approval stages, e.g. Product Manager -> Commercial Manager -> Operations -> Finance -> Final Approval; each stage names a role, a specific approver or a group"},"rejectionBehavior":{"type":"string","enum":["returnToDraft","returnToPreviousStage","closeRequest"],"description":"What happens on rejection; default returnToDraft (decided 29 September, readiness close-out)"},"resubmissionBehavior":{"type":"string","enum":["restartFromFirstStage","resumeAtRejectingStage"],"description":"Where a resubmitted request re-enters; default restartFromFirstStage (decided 29 September, readiness close-out)"},"workflowId":{"type":"string","description":"Existing workflow to change; empty to create","format":"uuid","nullable":true}}},
"ApprovalWorkflowDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Approval Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflowName":{"type":"string","description":"Workflow name"},"applicableProductTypes":{"type":"array","items":{"$ref":"#/components/schemas/ProductKind"},"description":"Applicable product types; empty = all"},"venue":{"type":"string","description":"Venue id; empty = all venues","nullable":true},"department":{"type":"string","description":"Department","nullable":true},"changeTypes":{"type":"array","items":{"type":"string","enum":["newProduct","description","price","validity","capacity","entitlement","eligibility","tax","channel","media","policy","relationship","retirement"]},"description":"Change types routed to this workflow (Conditional Approval: e.g. price -> Commercial + Finance)"},"approvalStages":{"type":"array","items":{"type":"object","properties":{"order":{"type":"integer","description":"Stage order; stages sharing an order run in parallel, otherwise sequential"},"name":{"type":"string"},"approverRole":{"type":"string","nullable":true},"specificApproverId":{"type":"string","nullable":true},"approvalGroupId":{"type":"string","nullable":true},"mandatory":{"type":"boolean"},"slaHours":{"type":"integer","description":"SLA in hours"},"escalateToRole":{"type":"string","nullable":true,"description":"Escalation when the SLA is missed"},"delegationAllowed":{"type":"boolean"},"reminderEveryHours":{"type":"integer","nullable":true,"description":"Reminder frequency"}}},"description":"Approval stages, e.g. Product Manager -> Commercial Manager -> Operations -> Finance -> Final Approval; each stage names a role, a specific approver or a group"},"rejectionBehavior":{"type":"string","enum":["returnToDraft","returnToPreviousStage","closeRequest"],"description":"What happens on rejection; default returnToDraft (decided 29 September, readiness close-out)"},"resubmissionBehavior":{"type":"string","enum":["restartFromFirstStage","resumeAtRejectingStage"],"description":"Where a resubmitted request re-enters; default restartFromFirstStage (decided 29 September, readiness close-out)"},"workflowId":{"type":"string","description":"Workflow id","format":"uuid"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}}
}
```
