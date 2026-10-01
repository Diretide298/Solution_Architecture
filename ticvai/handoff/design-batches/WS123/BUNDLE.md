# WS123 — AI Governance board 3

**10 screens · 7 operations · 15 schemas · 2 permissions**

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
  `AI_AUDIT_VIEW, AI_USE`. A control nobody can use must say so,
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
| `ADM-539` | AI Explainability & Audit Command Center | B–D | 2 | 0 | 6 | 4 | 0 | 0 | — | notStarted (—) |
| `ADM-540` | AI Decision Explorer & Search | B–D | 3 | 0 | 6 | 4 | 2 | 0 | — | notStarted (—) |
| `ADM-541` | AI Decision Explanation Workspace | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-542` | Data, Feature & Evidence Provenance | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-543` | Candidate, Rule & Decision Path Trace | B–D | 0 | 12 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `ADM-544` | Model, Provider & AI Runtime Trace | B–D | 0 | 44 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-545` | Governance, Approval & Human Decision Trace | B–D | 0 | 0 | 6 | 0 | 1 | 3 | — | notStarted (—) |
| `ADM-546` | Execution & Business Outcome Trace | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-547` | AI Audit Record & Evidence Package | B–D | 0 | 0 | 6 | 4 | 0 | 0 | — | notStarted (—) |
| `ADM-548` | AI Trace Investigation & Replay Simulator | B–D | 0 | 12 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-541, ADM-542, ADM-543, ADM-544, ADM-545, ADM-546, ADM-548 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-539` AI Explainability & Audit Command Center

**Provide management, governance teams and authorized auditors with one central view of AI decisions, explanations, trace completeness and audit status across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/ai-explainability-audit-command-center-adm-539` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search explainability audit | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, capability, risk, model, provider and 4 more — which are present is a decision the pack already made. | — |

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

**AI Decisions Today** (metric tile)

**Governed AI Actions** (metric tile)

**Automated Decisions** (metric tile)

**Human-Reviewed Decisions** (metric tile)

**Human Overrides** (metric tile)

**Blocked Decisions** (metric tile)

**Explainability Coverage** (metric tile)

**Complete Decision Traces** (metric tile)

**Incomplete Traces** (metric tile)

**Audit Warnings** (metric tile)

**Data it reads**: `searchAiDecisions` (onLoad, Find AI decisions)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-540` AI Decision Explorer & Search: *AI Decision Explorer & Search*
- → `ADM-541` AI Decision Explanation Workspace: *AI Decision Explanation Workspace*
- → `ADM-542` Data, Feature & Evidence Provenance: *Data, Feature & Evidence Provenance*
- → `ADM-543` Candidate, Rule & Decision Path Trace: *Candidate, Rule & Decision Path Trace*
- → `ADM-544` Model, Provider & AI Runtime Trace: *Model, Provider & AI Runtime Trace*
- → `ADM-545` Governance, Approval & Human Decision Trace: *Governance, Approval & Human Decision Trace*
- → `ADM-546` Execution & Business Outcome Trace: *Execution & Business Outcome Trace*
- → `ADM-547` AI Audit Record & Evidence Package: *AI Audit Record & Evidence Package*
- → `ADM-548` AI Trace Investigation & Replay Simulator: *AI Trace Investigation & Replay Simulator*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The explainability audit list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the explainability audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No explainability audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the explainability audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `searchAiDecisions` → `AI_AUDIT_VIEW` (read) · staff

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

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-539` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS16 AI Governance Board 3.dc.html#adm-539`
- Workshop pack: AI_Governance_Reference.pdf board 3
- Flow F232 *AI Governance board 3: AI Explainability & Audit Command Center*, step 1: Opens AI Explainability & Audit Command Center → Provide management, governance teams and authorized auditors with one central view of AI decisions, explanations, trace completeness and audit status across TICVAI.
- Flow F232 *AI Governance board 3: AI Explainability & Audit Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F232 *AI Governance board 3: AI Explainability & Audit Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F232 *AI Governance board 3: AI Explainability & Audit Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F232 *AI Governance board 3: AI Explainability & Audit Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F232 *AI Governance board 3: AI Explainability & Audit Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F232 *AI Governance board 3: AI Explainability & Audit Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F232 *AI Governance board 3: AI Explainability & Audit Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F232 branch at step 1 (expected): when Nothing has been set up on AI Explainability & Audit Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F232 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-539?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-540`, `ADM-541`, `ADM-542`, `ADM-543`, `ADM-544`, `ADM-545`, `ADM-546`, `ADM-547`, `ADM-548`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-540` AI Decision Explorer & Search

**Allow authorized users to locate any AI decision or AI-driven action across TICVAI. This becomes the entry point when someone asks: “Why did TICVAI do this?” Search By Support: Decision ID Trace ID Approval ID Execution ID Transaction ID Customer Reference Session ID User Product Ticket Order Venue AI Capability Model Version Date / Time Example Search Transaction ORD-928410 Results: Time AI Capability Decision Related Object Result 13:42 Recommendation AI Fast Pass ORD-928410 Accepted 13:44 Recommendation AI Family Meal ORD-928410 Ignored 13:46 Fraud AI Risk Assessment ORD-928410 Low Risk Decision Card Selecting a decision displays: Decision ID DEC-49102 Capability Recommendation Engine Customer CUS-****821 Channel B2C Journey Stage Checkout Decision Recommend Fast Pass Rank #1 Confidence 87% Model REC-v3.2 Status Delivered Relationship Search Allow navigation: Customer → Session → Decision → Delivery → Transaction**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `decisionRecordId` (navigation) |
| Route | `/platform/ai-decision-explorer-search-adm-540` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |
| Venue | select field | — | — | — | — | Sent as `venueId` (18 September minutes, M18-03: searchable by venue). | — |
| Customer | search field | — | — | — | — | Sent as `subjectRef`, the guest profile id (M18-03: searchable by customer). | `searchAiDecisions` |

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

**Detail panel** (detail panel): One record, read-only.

**Data it reads**: `searchAiDecisions` (onLoad, Find AI decisions)

**Where the user goes next**

- → `ADM-539` AI Explainability & Audit Command Center: *Back to AI Explainability & Audit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The decision search list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the decision search untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No decision search yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the decision search are still there. Names the active filter and offers to clear it. |
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

- AI decisions are searchable by venue and by customer. *(agreed · MoM 18 Sep 2026, M18-03 · DI-957)*
- Every AI decision is searchable in an AI decision explorer by customer, venue or AI capability, showing the data/model behind it, the governing rule, any human override, who approved it and when it was published. *(agreed · MoM 18 Sep 2026, 4.3 AI Governance — Explainability, Decision Trace & Audit · DI-934)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-540` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS16 AI Governance Board 3.dc.html#adm-540`
- Workshop pack: AI_Governance_Reference.pdf board 3
- Flow F232 *AI Governance board 3: AI Explainability & Audit Command Center*, step 2: Works in AI Decision Explorer & Search → Allow authorized users to locate any AI decision or AI-driven action across TICVAI. This becomes the entry point when someone asks: “Why did TICVAI do this?” Search By Support: Decision ID Trace ID …

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-540?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-539`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-541` AI Decision Explanation Workspace

**Explain a selected AI decision in a clear business-readable format.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `decisionRecordId` (navigation) |
| Route | `/platform/ai-decision-explanation-workspace-adm-541` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Depth | segmented control | Business | Business · Governance · Technical | `getAiDecisionTrace` ?depth |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Data it reads**: `getAiDecisionTrace` (onLoad, The full trace of a decision)

**Where the user goes next**

- → `ADM-539` AI Explainability & Audit Command Center: *Back to AI Explainability & Audit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The decision explanation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the decision explanation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No decision explanation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the decision explanation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getAiDecisionTrace` → `AI_AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every AI decision is searchable in an AI decision explorer by customer, venue or AI capability, showing the data/model behind it, the governing rule, any human override, who approved it and when it was published. *(agreed · MoM 18 Sep 2026, 4.3 AI Governance — Explainability, Decision Trace & Audit · DI-934)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-541` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS16 AI Governance Board 3.dc.html#adm-541`
- Workshop pack: AI_Governance_Reference.pdf board 3
- Flow F232 *AI Governance board 3: AI Explainability & Audit Command Center*, step 4: Works in AI Decision Explanation Workspace → Explain a selected AI decision in a clear business-readable format.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-541?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-539`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-542` Data, Feature & Evidence Provenance

**Show exactly which data and evidence contributed to an AI decision and where each item originated. This is critical for trust.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `decisionRecordId` (navigation) |
| Route | `/platform/data-feature-evidence-provenance-adm-542` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Depth | segmented control | Business | Business · Governance · Technical | `getAiDecisionTrace` ?depth |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Data it reads**: `getAiDecisionTrace` (onLoad, The full trace of a decision)

**Where the user goes next**

- → `ADM-539` AI Explainability & Audit Command Center: *Back to AI Explainability & Audit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The data feature evidence list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the data feature evidence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No data feature evidence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the data feature evidence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getAiDecisionTrace` → `AI_AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-542` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS16 AI Governance Board 3.dc.html#adm-542`
- Workshop pack: AI_Governance_Reference.pdf board 3
- Flow F232 *AI Governance board 3: AI Explainability & Audit Command Center*, step 6: Works in Data, Feature & Evidence Provenance → Show exactly which data and evidence contributed to an AI decision and where each item originated. This is critical for trust.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-542?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-539`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-543` Candidate, Rule & Decision Path Trace

**Explain how TICVAI moved from all possible options to the final AI decision. This is particularly important for recommendation, fraud, pricing and configuration decisions. Example — Recommendation 48 Potential Products ↓ 42 Active 6 removed ↓ 35 Channel Eligible 7 removed ↓ 28 Date / Time Eligible 7 removed ↓ 22 Customer Eligible 6 removed ↓ 18 Capacity Available 4 removed ↓ 14 Passed Exclusions 4 removed ↓ 10 Passed Guardrails 4 removed ↓ 10 Ranked ↓ Fast Pass #1**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW`, `AI_USE` (1 read, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `decisionId` (navigation), `decisionRecordId` (navigation) |
| Route | `/platform/candidate-rule-decision-path-trace-adm-543` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Depth | segmented control | Business | Business · Governance · Technical | `getAiDecisionTrace` ?depth |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every candidate rule decision** (data table)

| Shows | Format | Notes |
|---|---|---|
| Rule | text | not in the schema: `Rule` |
| CAP 014 | text | not in the schema: `CAP-014` |
| PASS | text | not in the schema: `PASS` |
| Exclusion trace | text | not in the schema: `Exclusion Trace` |
| VIP tour | text | not in the schema: `VIP Tour` |
| Remaining capacity = 0 | text | not in the schema: `Remaining Capacity = 0` |

**The selected candidate rule decision** (detail panel): The pack groups this record's detail under its own headings: “Candidate Table”, “Governance”, “Approval”, “Signals”.

| Shows | Format | Notes |
|---|---|---|
| Rule | text | not in the schema: `Rule` |
| CAP 014 | text | not in the schema: `CAP-014` |
| PASS | text | not in the schema: `PASS` |
| Exclusion trace | text | not in the schema: `Exclusion Trace` |
| VIP tour | text | not in the schema: `VIP Tour` |
| Remaining capacity = 0 | text | not in the schema: `Remaining Capacity = 0` |

**Data it reads**: `getAiDecisionTrace` (onLoad, The full trace of a decision)

**Where the user goes next**

- → `ADM-539` AI Explainability & Audit Command Center: *Back to AI Explainability & Audit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The candidate rule decision list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the candidate rule decision untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No candidate rule decision yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the candidate rule decision are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `explainRecommendationDecision` → `AI_USE` (operate) · staff
- `getAiDecisionTrace` → `AI_AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.20 | System shall support recommendation explainability. | Unified Operations Dashboard | CONTRACTED | `explainRecommendationDecision` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every AI decision is searchable in an AI decision explorer by customer, venue or AI capability, showing the data/model behind it, the governing rule, any human override, who approved it and when it was published. *(agreed · MoM 18 Sep 2026, 4.3 AI Governance — Explainability, Decision Trace & Audit · DI-934)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-543` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS16 AI Governance Board 3.dc.html#adm-543`
- Workshop pack: AI_Governance_Reference.pdf board 3
- Flow F232 *AI Governance board 3: AI Explainability & Audit Command Center*, step 8: Works in Candidate, Rule & Decision Path Trace → Explain how TICVAI moved from all possible options to the final AI decision. This is particularly important for recommendation, fraud, pricing and configuration decisions. Example — Recommendation 48 …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-543?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-539`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`, `AI_USE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-544` Model, Provider & AI Runtime Trace

**Record which AI technology produced or contributed to the decision. This gives TICVAI provider and model traceability without duplicating AI Platform configuration.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW`, `AI_USE` (1 read, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `decisionRecordId` (navigation) |
| Route | `/platform/model-provider-ai-runtime-trace-adm-544` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Layer | segmented control | — | Platform · Tenant | `listAiModels` ?layer |
| Producer type | radio group | — | Llm · Embedding · Reranker · Classical · Rule | `listAiModels` ?producerType |
| Depth | segmented control | Business | Business · Governance · Technical | `getAiDecisionTrace` ?depth |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every model provider runtime** (data table)

| Shows | Format | Notes |
|---|---|---|
| AI capability | text | not in the schema: `AI Capability` |
| Engine | text | not in the schema: `Engine` |
| Provider | text | not in the schema: `Provider` |
| Model | text | not in the schema: `Model` |
| Model version | text | not in the schema: `Model Version` |
| Deployment reference | text | not in the schema: `Deployment Reference` |
| Prompt / template version reference | text | not in the schema: `Prompt / Template Version Reference` |
| Rule engine version | text | not in the schema: `Rule Engine Version` |
| Feature set version | text | not in the schema: `Feature Set Version` |
| Knowledge source version | text | not in the schema: `Knowledge Source Version` |
| Request timestamp | text | not in the schema: `Request Timestamp` |
| Response timestamp | text | not in the schema: `Response Timestamp` |
| Latency | text | not in the schema: `Latency` |
| Tokens / compute where applicable | text | not in the schema: `Tokens / Compute where applicable` |
| Provider request reference | text | not in the schema: `Provider Request Reference` |
| Fallback used | text | not in the schema: `Fallback Used` |
| Retry count | text | not in the schema: `Retry Count` |
| Primary provider | text | not in the schema: `Primary Provider` |
| ↓ | text | not in the schema: `↓` |
| Timeout | text | not in the schema: `Timeout` |
| Fallback provider | text | not in the schema: `Fallback Provider` |
| Success | text | not in the schema: `Success` |

**The selected model provider runtime** (detail panel): The pack groups this record's detail under its own headings: “Prompt Template”, “Latency”, “Version Traceability”, “Important Boundary”.

| Shows | Format | Notes |
|---|---|---|
| AI capability | text | not in the schema: `AI Capability` |
| Engine | text | not in the schema: `Engine` |
| Provider | text | not in the schema: `Provider` |
| Model | text | not in the schema: `Model` |
| Model version | text | not in the schema: `Model Version` |
| Deployment reference | text | not in the schema: `Deployment Reference` |
| Prompt / template version reference | text | not in the schema: `Prompt / Template Version Reference` |
| Rule engine version | text | not in the schema: `Rule Engine Version` |
| Feature set version | text | not in the schema: `Feature Set Version` |
| Knowledge source version | text | not in the schema: `Knowledge Source Version` |
| Request timestamp | text | not in the schema: `Request Timestamp` |
| Response timestamp | text | not in the schema: `Response Timestamp` |
| Latency | text | not in the schema: `Latency` |
| Tokens / compute where applicable | text | not in the schema: `Tokens / Compute where applicable` |
| Provider request reference | text | not in the schema: `Provider Request Reference` |
| Fallback used | text | not in the schema: `Fallback Used` |
| Retry count | text | not in the schema: `Retry Count` |
| Primary provider | text | not in the schema: `Primary Provider` |
| ↓ | text | not in the schema: `↓` |
| Timeout | text | not in the schema: `Timeout` |
| Fallback provider | text | not in the schema: `Fallback Provider` |
| Success | text | not in the schema: `Success` |

**Data it reads**: `listAiModels` (onLoad, The model catalogue); `getAiDecisionTrace` (onLoad, The full trace of a decision)

**Where the user goes next**

- → `ADM-539` AI Explainability & Audit Command Center: *Back to AI Explainability & Audit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The model provider runtime list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the model provider runtime untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No model provider runtime yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the model provider runtime are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAiModels` → `AI_USE` (operate) · staff
- `getAiDecisionTrace` → `AI_AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-544` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS16 AI Governance Board 3.dc.html#adm-544`
- Workshop pack: AI_Governance_Reference.pdf board 3
- Flow F232 *AI Governance board 3: AI Explainability & Audit Command Center*, step 10: Works in Model, Provider & AI Runtime Trace → Record which AI technology produced or contributed to the decision. This gives TICVAI provider and model traceability without duplicating AI Platform configuration.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-544?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-539`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-545` Governance, Approval & Human Decision Trace

**Connect Board 1 and Board 2 governance activity to the AI decision.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `decisionRecordId` (navigation) |
| Route | `/platform/governance-approval-human-decision-trace-adm-545` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Depth | segmented control | Business | Business · Governance · Technical | `getAiDecisionTrace` ?depth |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Data it reads**: `getAiDecisionTrace` (onLoad, The full trace of a decision)

**Where the user goes next**

- → `ADM-539` AI Explainability & Audit Command Center: *Back to AI Explainability & Audit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance approval human list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance approval human untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No governance approval human yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the governance approval human are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getAiDecisionTrace` → `AI_AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every AI decision is searchable in an AI decision explorer by customer, venue or AI capability, showing the data/model behind it, the governing rule, any human override, who approved it and when it was published. *(agreed · MoM 18 Sep 2026, 4.3 AI Governance — Explainability, Decision Trace & Audit · DI-934)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-545` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS16 AI Governance Board 3.dc.html#adm-545`
- Workshop pack: AI_Governance_Reference.pdf board 3
- Flow F232 *AI Governance board 3: AI Explainability & Audit Command Center*, step 12: Works in Governance, Approval & Human Decision Trace → Connect Board 1 and Board 2 governance activity to the AI decision.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-545?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-539`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-546` Execution & Business Outcome Trace

**Connect the AI decision to what actually happened in TICVAI. A good AI audit cannot stop at: “AI recommended X.” It needs to know: Was X actually executed, and what was the outcome? Execution Trace Example: AI Proposal Change Adult Weekend Price ↓ Approved AED 150 ↓ Execution Authorization AUTH-9281 ↓ Pricing API Update Pricing Profile ↓ Execution Result SUCCESS Before / After Before Adult Weekend = AED 140 After Adult Weekend = AED 150 Execution Metadata Execution ID Owning Module API / Service Start Time Completion Time Result Retry Failure Rollback Final State**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW`, `AI_USE` (1 read, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `decisionRecordId` (navigation), `planId` (navigation) |
| Route | `/platform/execution-business-outcome-trace-adm-546` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Depth | segmented control | Business | Business · Governance · Technical | `getAiDecisionTrace` ?depth |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Data it reads**: `getAiDecisionTrace` (onLoad, The full trace of a decision)

**Where the user goes next**

- → `ADM-539` AI Explainability & Audit Command Center: *Back to AI Explainability & Audit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The execution business outcome list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the execution business outcome untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No execution business outcome yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the execution business outcome are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `getAiDecisionTrace` → `AI_AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-546` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS16 AI Governance Board 3.dc.html#adm-546`
- Workshop pack: AI_Governance_Reference.pdf board 3
- Flow F232 *AI Governance board 3: AI Explainability & Audit Command Center*, step 14: Works in Execution & Business Outcome Trace → Connect the AI decision to what actually happened in TICVAI. A good AI audit cannot stop at: “AI recommended X.” It needs to know: Was X actually executed, and what was the outcome? Execution Trace …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-546?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-539`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-547` AI Audit Record & Evidence Package

**Create a complete, tamper-evident audit package for an AI decision or group of decisions.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/ai-audit-record-evidence-package-adm-547` |

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 0 operations.** Unserved: Single Decision, Customer Journey, AI Capability, Incident, Model Version, Governance Policy. Each needs an … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

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

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Single Decision (primary button) | navigation or local | — | — | — | — |
| Customer Journey (secondary button) | navigation or local | — | — | — | — |
| AI Capability (secondary button) | navigation or local | — | — | — | — |
| Incident (secondary button) | navigation or local | — | — | — | — |
| Model Version (secondary button) | navigation or local | — | — | — | — |
| Governance Policy (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `searchAiDecisions` (onLoad, Find AI decisions)

**Where the user goes next**

- → `ADM-539` AI Explainability & Audit Command Center: *Back to AI Explainability & Audit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The audit record evidence list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the audit record evidence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No audit record evidence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the audit record evidence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `searchAiDecisions` → `AI_AUDIT_VIEW` (read) · staff
- `exportAiEvidencePackage` → `AI_AUDIT_VIEW` (read) · staff

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

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-547` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS16 AI Governance Board 3.dc.html#adm-547`
- Workshop pack: AI_Governance_Reference.pdf board 3
- Flow F232 *AI Governance board 3: AI Explainability & Audit Command Center*, step 16: Works in AI Audit Record & Evidence Package → Create a complete, tamper-evident audit package for an AI decision or group of decisions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-547?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Single Decision, Customer Journey, AI Capability, Incident, Model Version, Governance Policy.
- [ ] Every transition is wired: `ADM-539`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-548` AI Trace Investigation & Replay Simulator

**Allow authorized governance/technical teams to reconstruct an AI decision and understand whether the same conditions would produce the same or a different outcome. This should be a powerful investigation tool.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Compare) and no metric row |
| Offline | online only |
| Opens with | `decisionRecordId` (navigation) |
| Route | `/platform/ai-trace-investigation-replay-simulator-adm-548` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Depth | segmented control | Business | Business · Governance · Technical | `getAiDecisionTrace` ?depth |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every trace investigation replay** (data table)

| Shows | Format | Notes |
|---|---|---|
| 2 | text | not in the schema: `Model v3.2` |
| 3 | text | not in the schema: `Model v3.3` |
| Alternative policy replay | text | not in the schema: `Alternative Policy Replay` |
| 4 | text | not in the schema: `Governance v1.4` |
| 5 | text | not in the schema: `Governance v1.5` |
| Comparison | text | not in the schema: `Comparison` |

**The selected trace investigation replay** (detail panel): The pack groups this record's detail under its own headings: “Original Time”, “Result”, “Exact Historical Replay”, “Element Original Replay”, “Eligibility Same Same”, “Authorized investigator can record”.

| Shows | Format | Notes |
|---|---|---|
| 2 | text | not in the schema: `Model v3.2` |
| 3 | text | not in the schema: `Model v3.3` |
| Alternative policy replay | text | not in the schema: `Alternative Policy Replay` |
| 4 | text | not in the schema: `Governance v1.4` |
| 5 | text | not in the schema: `Governance v1.5` |
| Comparison | text | not in the schema: `Comparison` |

**Data it reads**: `getAiDecisionTrace` (onLoad, The full trace of a decision)

**Where the user goes next**

- → `ADM-539` AI Explainability & Audit Command Center: *Back to AI Explainability & Audit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The trace investigation replay list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the trace investigation replay untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No trace investigation replay yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the trace investigation replay are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getAiDecisionTrace` → `AI_AUDIT_VIEW` (read) · staff
- `replayAiDecision` → `AI_AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-548` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS16 AI Governance Board 3.dc.html#adm-548`
- Workshop pack: AI_Governance_Reference.pdf board 3
- Flow F232 *AI Governance board 3: AI Explainability & Audit Command Center*, step 18: Works in AI Trace Investigation & Replay Simulator → Allow authorized governance/technical teams to reconstruct an AI decision and understand whether the same conditions would produce the same or a different outcome. This should be a powerful …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-548?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-539`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`.
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

### In P09 · Platform

- **Open question.** Open: should AI monitoring live in one centralised AI command dashboard or be distributed as widgets in each functional module's own dashboard? Allam: Softlabs' call; the current proposal is illustrative and Softlabs may propose a better structure. *(open · MoM 18 Sep 2026, 4.4 AI Governance — Risk, Compliance & Continuous Monitoring · DI-936)*

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"explainRecommendationDecision": {"method":"GET","path":"/recommendations/decisions/{decisionId}/explanation","contract":"ai","summary":"Why these recommendations","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"depth","in":"query","required":null}],"requestBody":null,"responds":"AiRecommendationExplanation"},
"exportAiEvidencePackage": {"method":"POST","path":"/evidence-packages","contract":"ai","summary":"Export an evidence package","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getActionPlan": {"method":"GET","path":"/action-plans/{planId}","contract":"ai","summary":"A plan with its steps","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiActionPlanDetail"},
"getAiDecisionTrace": {"method":"GET","path":"/decision-records/{decisionRecordId}/trace","contract":"ai","summary":"The full trace of a decision","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"depth","in":"query","required":null}],"requestBody":null,"responds":"AiDecisionTrace"},
"listAiModels": {"method":"GET","path":"/models","contract":"ai","summary":"The model catalogue","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"layer","in":"query","required":null},{"name":"producerType","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"replayAiDecision": {"method":"POST","path":"/decision-records/{decisionRecordId}/replay","contract":"ai","summary":"Re-simulate a decision","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiReplayResult"},
"searchAiDecisions": {"method":"GET","path":"/decision-records","contract":"ai","summary":"Find AI decisions","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"capabilityKey","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"subjectRef","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"traceId","in":"query","required":null},{"name":"policyVersion","in":"query","required":null},{"name":"modelVersion","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiActionPlan": {"type":"object","x-ticvai-persistence":"ai.action_plan","description":"**A plan: plan, validate, simulate, approve, execute, with rollback** (design 2.2 D, 3.8; AIC-086..107). Independent of any conversation (AIC-102). Its steps are `ai.action_step`; the change set is hashed so what was approved is what runs (AIC-181).","required":["origin","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"origin":{"type":"string","enum":["configurationSession","generateConfiguration","assistant","riskCase","operationalRequirement","rollback"]},"originRef":{"type":"string","nullable":true},"summary":{"type":"string"},"status":{"type":"string","enum":["draft","validated","simulated","awaitingApproval","approved","executing","paused","completed","partiallyCompleted","failed","compensated","cancelled","rolledBack"],"readOnly":true},"autonomyLevel":{"$ref":"#/components/schemas/AiAutonomyLevel"},"approvalTier":{"type":"integer","minimum":1,"maximum":2,"description":"The approval tier (1 or 2), the floor the approvals matrix adds to (design 3.8). Not an autonomy level."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request, where tier 2 or the matrix caught the plan."},"proposedActionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.proposed_action","description":"The `ai.proposed_action` the plan is presented as for a decision."},"changeSetHash":{"type":"string","readOnly":true},"governanceOutcome":{"allOf":[{"$ref":"#/components/schemas/AiGovernanceOutcome"}],"readOnly":true},"policyVersionRef":{"type":"string","readOnly":true,"description":"The governance policy version that decided it."},"simulation":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"Current versus proposed state, channels, future orders and issued tickets affected (flow D step 4)."},"partialCompletionAllowed":{"type":"boolean","default":false,"description":"Where governance allows a partial completion; otherwise a failure compensates in reverse dependency order (AIC-098, AIC-134)."},"rollbackOfPlanId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.action_plan"},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiActionPlanDetail": {"type":"object","x-ticvai-persistence":"none — ai.action_plan with its ai.action_step rows","description":"A plan with its steps in DAG order.","required":["plan","steps"],"properties":{"plan":{"$ref":"#/components/schemas/AiActionPlan"},"steps":{"type":"array","items":{"$ref":"#/components/schemas/AiActionStep"}}}},
"AiActionStep": {"type":"object","x-ticvai-persistence":"ai.action_step","description":"One step of a plan: a registered tool against `targetContract.targetOperation` at a contract version (AIC-095), with payload, provenance, compensation and the idempotency key `plan:{id}:step:{n}`. **Scoped through its plan** (`platform.apply_parent_rls`). Each step records its target object's version; drift pauses the plan (AIC-182).","required":["planId","stepNumber","toolKey","targetContract","targetOperation","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"planId":{"type":"string","format":"uuid","x-ticvai-references":"ai.action_plan"},"stepNumber":{"type":"integer","minimum":1},"dependsOn":{"type":"array","items":{"type":"integer","minimum":1},"description":"Step numbers that must succeed first. The plan is a DAG."},"toolKey":{"type":"string"},"targetContract":{"type":"string"},"targetOperation":{"type":"string"},"contractVersion":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body of `targetOperation`, validated against it before the plan is approved."},"provenance":{"$ref":"#/components/schemas/AiProvenance"},"idempotencyKey":{"type":"string","readOnly":true},"targetObjectRef":{"type":"string","nullable":true},"targetObjectVersion":{"type":"string","nullable":true,"description":"The version the step was planned against. A different version at execution is drift."},"reversible":{"type":"boolean"},"compensation":{"type":"object","additionalProperties":true,"nullable":true},"status":{"type":"string","enum":["pending","validated","running","succeeded","failed","compensated","skipped","paused"],"readOnly":true},"attempts":{"type":"integer","minimum":0,"maximum":3,"readOnly":true,"description":"Bounded at 3 (AIC-135)."},"lastError":{"type":"string","nullable":true,"readOnly":true},"resultRef":{"type":"string","nullable":true,"readOnly":true,"description":"The owning service's response: success is its answer, not a model's judgement (AIC-097)."},"startedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"AiCapability": {"type":"string","description":"What a capability needs, not which provider serves it. This indirection is what makes \"no provider SDK in capability code\" enforceable.\n**`speechToText` and `textToSpeech` added 18 August (BL-164)** — voice added rather than declined. **Speech is the capability where UAE residency is hardest to satisfy**: the major providers run it in fewer regions than text, and a guest speaking into a kiosk is producing personal data in the moment. `AiProvider.residency` already carries the constraint and **speech is the capability most likely to fail it**, which is why it is separate rather than folded into `chat`.\n","enum":["chat","embedding","vision","rerank","speechToText","textToSpeech"]},
"AiDecisionRecord": {"type":"object","x-ticvai-persistence":"ai.decision_record","description":"**The standard record for every governed decision** (design 3.9, C12; AIC-193..209): a recommendation summary, a risk assessment, a forecast publication, a plan step, an assistant answer at significant depth, a governance block, a Help me choose suggestion. **Append-only; corrections are annotations; hash-chained per tenant** so tampering is detectable (AIC-203, AIC-204). **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["traceId","capabilityKey","outcome","recordHash"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"traceId":{"type":"string"},"capabilityKey":{"type":"string"},"task":{"type":"string","nullable":true},"subjectKind":{"type":"string","nullable":true},"subjectRef":{"type":"string","nullable":true},"inputsRef":{"type":"string","nullable":true,"description":"Where the inputs are kept (Blob or `ai.activity`), never the prompt text itself."},"evidence":{"$ref":"#/components/schemas/AiEvidenceItemList"},"producer":{"type":"string","nullable":true},"modelVersion":{"type":"string","nullable":true},"promptTemplateVersion":{"type":"string","nullable":true},"featureSetVersion":{"type":"string","nullable":true},"knowledgeVersion":{"type":"string","nullable":true},"ruleVersions":{"type":"object","additionalProperties":true,"nullable":true},"governanceOutcome":{"allOf":[{"$ref":"#/components/schemas/AiGovernanceOutcome"}],"nullable":true},"policyVersion":{"type":"string","nullable":true},"approvals":{"type":"object","additionalProperties":true,"nullable":true,"description":"Approval requests and their decisions."},"humanDecision":{"type":"object","additionalProperties":true,"nullable":true,"description":"Override or intervention, where a person changed the outcome."},"executionResult":{"type":"object","additionalProperties":true,"nullable":true},"outcomeRef":{"type":"string","nullable":true,"description":"The business outcome it links to (an order, a published version, a closed case)."},"outcome":{"type":"string","enum":["answered","refused","allowed","blocked","executed","failed","approvedThenFailed","published","suggested"],"description":"`approvedThenFailed` is kept distinct from `executed` (design 1.2 Audit)."},"annotations":{"type":"array","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"byPrincipalId":{"type":"string","format":"uuid"},"note":{"type":"string"}}},"readOnly":true,"description":"Corrections, appended; the original fields are never edited."},"previousHash":{"type":"string","readOnly":true},"recordHash":{"type":"string","readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiDecisionTrace": {"type":"object","x-ticvai-persistence":"none — ai.decision_record with the rows it references","description":"**The full trace of one decision** (ADM-540..546): record, evidence, candidates and rules, model and runtime, governance and approvals, execution and business outcome. Depth is gated by permission (AIC-195).","required":["record"],"properties":{"record":{"$ref":"#/components/schemas/AiDecisionRecord"},"depth":{"type":"string","enum":["business","governance","technical"]},"explanation":{"type":"string","description":"Built from structured evidence, never a model's chain of thought (AIC-192)."},"activity":{"type":"array","items":{"$ref":"#/components/schemas/AiInteraction"},"description":"The model calls behind it (`technical` depth)."},"plan":{"allOf":[{"$ref":"#/components/schemas/AiActionPlanDetail"}],"nullable":true},"interventions":{"type":"array","items":{"$ref":"#/components/schemas/AiIntervention"}},"chainVerified":{"type":"boolean","description":"The hash chain around this record verifies."}}},
"AiEvidenceItemList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The evidence of one decision record, stored with it.","items":{"$ref":"#/components/schemas/AiEvidenceItem"}},
"AiGovernanceOutcome": {"type":"string","enum":["allow","allowWithConditions","prepareOnly","approvalRequired","escalate","block"],"description":"What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). `block` is an answer, not an error, and is logged as outcome `refused`."},
"AiInteraction": {"type":"object","x-ticvai-persistence":"ai.activity","required":["id","principalId","capability","outcome","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"conversationId":{"type":"string","format":"uuid","nullable":true},"principalId":{"type":"string","format":"uuid"},"audience":{"type":"string","enum":["staff","guest"],"description":"**Billing divides on this.** Staff usage is bounded by headcount; guest usage is bounded by footfall and curiosity, and a venue cannot stop guests asking questions.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest, where the audience is `guest`. `principalId` is null in that case — **a guest is not a principal**, and attributing their tokens to a staff member would be wrong twice.\n"},"billableToTenantId":{"type":"string","format":"uuid","description":"Resolved from `scopePath` at write time, not derived later. **Billing must not depend on walking a scope tree that has since been reorganised.**\n"},"scopePath":{"type":"string"},"capability":{"type":"string"},"prompt":{"type":"string"},"response":{"type":"string"},"sources":{"$ref":"#/components/schemas/AiSourceList"},"outcome":{"type":"string","enum":["answered","refused","applied","rejected","failed"]},"refusalReason":{"type":"string","nullable":true},"provider":{"$ref":"#/components/schemas/AiProviderKind"},"model":{"type":"string"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"cost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"x-ticvai-column":"cost_amount","description":"What the call cost at the provider. **Money like every other amount** (naming-and-style 5.1) — it replaces an integer `costMinor` that carried no currency or scale, which AED and OMR read differently.\n"},"latencyMs":{"type":"integer"},"maskedFieldCount":{"type":"integer","description":"How many fields were redacted. Zero on a prompt touching guest data is a defect."},"traceId":{"type":"string"},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"description":"The `ai.decision_record` this call belongs to, where it was part of a governed decision (AI design 2.3, 3.9). Null for a call audited by this row alone."},"cacheLayer":{"type":"string","nullable":true,"enum":["guardrail","semantic","exact","negative","analytics"],"description":"Which cache answered, where one did (AI design 3.6). Null for a model call."},"createdAt":{"type":"string","format":"date-time"}}},
"AiIntervention": {"type":"object","x-ticvai-persistence":"ai.intervention","description":"**A person stepping in** (AIC-187, ADM-535, ADM-536): an override, pause, resume, stop, retry or rollback, with the original AI decision and the human one side by side.","required":["kind","targetKind","targetRef"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["override","pause","resume","cancel","retry","rollback","capabilityPause","capabilityResume"]},"targetKind":{"type":"string","enum":["plan","step","decision","capability"]},"targetRef":{"type":"string"},"decisionRecordId":{"type":"string","format":"uuid","nullable":true},"originalDecision":{"type":"object","additionalProperties":true,"nullable":true},"humanDecision":{"type":"object","additionalProperties":true,"nullable":true},"reason":{"type":"string","maxLength":2000},"principalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiModel": {"type":"object","x-ticvai-persistence":"ai.model","description":"**The model catalogue** (design 3.1 Registry, 3.3; AIC-013, AIC-026). One row per model a task can be routed to: large language models, embedding and reranking models, and classical models (LightGBM, statistical forecasters) registered the same way so lifecycle, release and audit are uniform. **Platform rows** are mastered in the control plane and replicated read-only into each tenant database with the tenant root as `scopePath`; a tenant row exists only where bring-your-own-key is enabled for the tenant.","required":["layer","modelName","producerType"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"layer":{"type":"string","enum":["platform","tenant"]},"providerKind":{"allOf":[{"$ref":"#/components/schemas/AiProviderKind"}],"nullable":true},"producerType":{"type":"string","enum":["llm","embedding","reranker","classical","rule"]},"modelName":{"type":"string","description":"The deployment or model name as the provider knows it, or the package and version for a classical model."},"capabilities":{"type":"array","items":{"$ref":"#/components/schemas/AiCapability"}},"contextTokens":{"type":"integer","nullable":true},"toolCalling":{"type":"boolean","default":false},"structuredOutput":{"type":"boolean","default":false},"languages":{"type":"array","items":{"type":"string"}},"residency":{"type":"string","nullable":true,"description":"Where inference happens. Checked against `tenancy.RegionSettings.allowedAiResidencies`."},"inputCostPerMillionTokens":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"outputCostPerMillionTokens":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"lifecycle":{"type":"object","description":"Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production.","properties":{"development":{"type":"string","enum":["draft","pilot","active","retired"]},"staging":{"type":"string","enum":["draft","pilot","active","retired"]},"production":{"type":"string","enum":["draft","pilot","active","retired"]}}},"isDefaultForTasks":{"type":"array","items":{"type":"string"},"description":"Tasks this model is the default for (AIC-010), e.g. `assistant.guest.answer`, `config.extract`."},"taskFitness":{"type":"array","readOnly":true,"description":"**Evaluated fitness per task** (21 September minutes, M21-09, our proposal): a score from the task's golden set (`runAiEvaluation`) and the band the task needs. Below `floor` the model is underpowered for the task; far above `ceiling` it is overpowered (it costs more than the task needs). `setAiProvider` returns a warning (`AiProvider.fitnessWarnings`) when a choice falls outside the band, and ADM-037 shows the band beside `setAiModel`; neither refuses on it.","items":{"type":"object","required":["taskKey","score"],"properties":{"taskKey":{"type":"string"},"score":{"type":"number","minimum":0,"maximum":1},"floor":{"type":"number","minimum":0,"maximum":1},"ceiling":{"type":"number","minimum":0,"maximum":1,"nullable":true},"evaluationRunId":{"type":"string","format":"uuid","nullable":true},"evaluatedAt":{"type":"string","format":"date-time"}}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiProviderKind": {"type":"string","enum":["openai","gemini","anthropic","azureOpenai","localLlm","openaiCompatible"],"description":"`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n"},
"AiRecommendationExplanation": {"type":"object","x-ticvai-persistence":"none — built from ai.rec_decision and its decision record","description":"Why these items (AIR-193..202), at three depths each gated by permission (AIC-195): business, governance, technical.","required":["decisionId","depth"],"properties":{"decisionId":{"type":"string","format":"uuid"},"depth":{"type":"string","enum":["business","governance","technical"]},"funnel":{"type":"object","additionalProperties":true},"exclusions":{"type":"object","additionalProperties":true},"items":{"type":"array","items":{"type":"object","properties":{"trackingId":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid"},"reasons":{"type":"array","items":{"type":"string"}},"scoreBreakdown":{"type":"object","additionalProperties":true,"nullable":true}}}},"versions":{"type":"object","additionalProperties":true,"nullable":true,"description":"Strategy, model and feature-set versions. `technical` depth only."}}},
"AiReplayResult": {"type":"object","x-ticvai-persistence":"none — a re-simulation, never stored as a decision","description":"**A re-simulation, labelled as one** (AIC-206, ADM-548): the same inputs through today's or the recorded versions. It runs no production action and is never evidence of what happened.","required":["decisionRecordId","label","sameOutcome"],"properties":{"decisionRecordId":{"type":"string","format":"uuid"},"label":{"type":"string","enum":["reSimulation"]},"versionsUsed":{"type":"string","enum":["recorded","current"]},"sameOutcome":{"type":"boolean"},"original":{"type":"object","additionalProperties":true},"replayed":{"type":"object","additionalProperties":true},"differences":{"type":"array","items":{"type":"string"}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}}
}
```
