# WS154 — Payment Payment Orchestration board 8

**10 screens · 23 operations · 22 schemas · 9 permissions**

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

- **Every control that can be refused must be gated.** 9 permissions apply here:
  `AI_CONFIGURE, ORDER_MODIFY, ORDER_REFUND_APPROVE, ORDER_VIEW, PAYMENT_CONFIGURE, PAYMENT_DISPUTE, PAYMENT_VIEW, RISK_INVESTIGATE, RISK_REVIEW`. A control nobody can use must say so,
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
| `ADM-629` | Payment Risk & Fraud Command Center\t166 | B–D | 0 | 18 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-630` | Payment Risk Rule & Decision Engine\t167 | B–D | 0 | 0 | 6 | 8 | 0 | 0 | — | notStarted (—) |
| `ADM-631` | Velocity, Behavioral & Transaction Risk Controls\t168 | B–D | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `ADM-632` | Risk Lists, Signals & Payment Control Center\t169 | B–D | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `ADM-633` | Fraud Alert, Investigation & Case Management\t170 | B–D | 0 | 44 | 6 | 29 | 0 | 0 | — | notStarted (—) |
| `ADM-634` | Chargeback & Dispute Command Center\t172 | B–D | 0 | 26 | 6 | 5 | 0 | 0 | — | notStarted (—) |
| `ADM-635` | Chargeback Evidence & Representment Workspace\t173 | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-636` | Payment Performance & Conversion Analytics\t174 | B–D | 3 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-637` | AI Fraud, Anomaly & Payment Intelligence Center\t175 | B–D | 0 | 0 | 6 | 29 | 0 | 0 | — | notStarted (—) |
| `ADM-638` | Payment Executive Intelligence, Risk Simulator & AI Advisor\t176 | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-633, ADM-635, ADM-636 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-629` Payment Risk & Fraud Command Center\t166

**Provide real-time operational visibility over fraud, suspicious transactions, payment risk and chargebacks across the TICVAI ecosystem.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Show; Analyze) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/payment-risk-fraud-command-center-t166-adm-629` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getPaymentPerformance` ?from |
| Group by | select | — | Method · Provider · Card type · Channel · Authentication outcome · Venue | `getPaymentPerformance` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Payment Attempts** (metric tile)

**Approved Transactions** (metric tile)

**Declined Transactions** (metric tile)

**Risk-Blocked Transactions** (metric tile)

**Risk-Review Transactions** (metric tile)

**Suspected Fraud Value** (metric tile)

**Confirmed Fraud Value** (metric tile)

**Chargebacks** (metric tile)

**Chargeback Value** (metric tile)

**Chargeback Rate** (metric tile)

**Open Disputes** (metric tile)

**High-Risk Transactions** (metric tile)

**Every payment risk fraud** (data table)

| Shows | Format | Notes |
|---|---|---|
| Low risk | text | not in the schema: `Low Risk` |
| Medium risk | text | not in the schema: `Medium Risk` |
| High risk | text | not in the schema: `High Risk` |
| Critical risk | text | not in the schema: `Critical Risk` |
| Fraud attempts | text | not in the schema: `Fraud attempts` |
| Blocked fraud | text | not in the schema: `Blocked fraud` |
| Confirmed fraud | text | not in the schema: `Confirmed fraud` |
| Chargebacks | text | not in the schema: `Chargebacks` |
| False positives | text | not in the schema: `False positives` |

**The selected payment risk fraud** (detail panel): The pack groups this record's detail under its own headings: “Breakdown”.

| Shows | Format | Notes |
|---|---|---|
| Low risk | text | not in the schema: `Low Risk` |
| Medium risk | text | not in the schema: `Medium Risk` |
| High risk | text | not in the schema: `High Risk` |
| Critical risk | text | not in the schema: `Critical Risk` |
| Fraud attempts | text | not in the schema: `Fraud attempts` |
| Blocked fraud | text | not in the schema: `Blocked fraud` |
| Confirmed fraud | text | not in the schema: `Confirmed fraud` |
| Chargebacks | text | not in the schema: `Chargebacks` |
| False positives | text | not in the schema: `False positives` |

**Data it reads**: `getPaymentPerformance` (onLoad, Risk and fraud at a glance)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-630` Payment Risk Rule & Decision Engine\t167: *Payment Risk Rule & Decision Engine\t167*
- → `ADM-631` Velocity, Behavioral & Transaction Risk Controls\t168: *Velocity, Behavioral & Transaction Risk Controls\t168*
- → `ADM-632` Risk Lists, Signals & Payment Control Center\t169: *Risk Lists, Signals & Payment Control Center\t169*
- → `ADM-633` Fraud Alert, Investigation & Case Management\t170: *Fraud Alert, Investigation & Case Management\t170*
- → `ADM-634` Chargeback & Dispute Command Center\t172: *Chargeback & Dispute Command Center\t172*
- → `ADM-635` Chargeback Evidence & Representment Workspace\t173: *Chargeback Evidence & Representment Workspace\t173*
- → `ADM-636` Payment Performance & Conversion Analytics\t174: *Payment Performance & Conversion Analytics\t174*
- → `ADM-637` AI Fraud, Anomaly & Payment Intelligence Center\t175: *AI Fraud, Anomaly & Payment Intelligence Center\t175*
- → `ADM-638` Payment Executive Intelligence, Risk Simulator & AI Advisor\t176: *Payment Executive Intelligence, Risk Simulator & AI Advisor\t176*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment risk fraud list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment risk fraud untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment risk fraud yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment risk fraud are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getPaymentPerformance` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-629` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-629`
- Workshop pack: Payment_Payment_Orchestration.pdf board 8
- Flow F263 *Payment Payment Orchestration board 8: Payment Risk & Fraud Command Center\t166*, step 1: Opens Payment Risk & Fraud Command Center\t166 → Provide real-time operational visibility over fraud, suspicious transactions, payment risk and chargebacks across the TICVAI ecosystem.
- Flow F263 *Payment Payment Orchestration board 8: Payment Risk & Fraud Command Center\t166*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F263 *Payment Payment Orchestration board 8: Payment Risk & Fraud Command Center\t166*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F263 *Payment Payment Orchestration board 8: Payment Risk & Fraud Command Center\t166*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F263 *Payment Payment Orchestration board 8: Payment Risk & Fraud Command Center\t166*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F263 *Payment Payment Orchestration board 8: Payment Risk & Fraud Command Center\t166*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F263 *Payment Payment Orchestration board 8: Payment Risk & Fraud Command Center\t166*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F263 *Payment Payment Orchestration board 8: Payment Risk & Fraud Command Center\t166*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F263 branch at step 1 (expected): when Nothing has been set up on Payment Risk & Fraud Command Center\t166 yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F263 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-629?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-630`, `ADM-631`, `ADM-632`, `ADM-633`, `ADM-634`, `ADM-635`, `ADM-636`, `ADM-637`, `ADM-638`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-630` Payment Risk Rule & Decision Engine\t167

**Allow administrators to configure deterministic payment risk rules and actions.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_MODIFY`, `ORDER_VIEW`, `PAYMENT_CONFIGURE` (1 operate, 1 read, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/payment-risk-rule-decision-engine-t167-adm-630` |

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 0 operations.** Unserved: Allow, Monitor, Require additional verification, Route to manual review, Block, Trigger alert. Each needs … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Allow (primary button) | navigation or local | — | — | — | — |
| Monitor (secondary button) | navigation or local | — | — | — | — |
| Require additional verification (secondary button) | navigation or local | — | — | — | — |
| Route to manual review (secondary button) | navigation or local | — | — | — | — |
| Block (secondary button) | navigation or local | — | — | — | — |
| Trigger alert (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listFraudRules` (onLoad, Show refund-abuse and charge fraud rules)

**Where the user goes next**

- → `ADM-629` Payment Risk & Fraud Command Center\t166: *Back to Payment Risk & Fraud Command Center\t166*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment risk rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment risk rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment risk rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment risk rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setPaymentRiskRules` → `PAYMENT_CONFIGURE` (configure) · staff
- `listFraudRules` → `ORDER_VIEW` (read) · staff
- `setFraudRules` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.3.2 | System shall detect excessive failed payment attempts. | Unified Operations Dashboard | CONTRACTED | `setPaymentRiskRules` |
| 8.3.3 | System shall detect repeated payment attempts. | Unified Operations Dashboard | CONTRACTED | `setPaymentRiskRules` |
| 8.3.54 | System shall support blacklist management. | Unified Operations Dashboard | CONTRACTED | `setPaymentRiskRules` |
| 5.3.33 | Identify suspicious activities including excessive refunds, duplicate accounts, ticket abuse, fraud indicators, and chargebacks. | F&B & Guest Management | CONTRACTED | `setFraudRules` |
| 8.3.7 | System shall detect transactions from blocked countries. | Unified Operations Dashboard | CONTRACTED | `setFraudRules` |
| 8.3.17 | System shall detect excessive refunds by customer. | Unified Operations Dashboard | CONTRACTED | `setFraudRules` |
| 8.3.19 | System shall detect repeated refund requests. | Unified Operations Dashboard | CONTRACTED | `setFraudRules` |
| 8.3.20 | System shall detect refund activity exceeding thresholds. | Unified Operations Dashboard | CONTRACTED | `setFraudRules` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-630` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-630`
- Workshop pack: Payment_Payment_Orchestration.pdf board 8
- Flow F263 *Payment Payment Orchestration board 8: Payment Risk & Fraud Command Center\t166*, step 2: Works in Payment Risk Rule & Decision Engine\t167 → Allow administrators to configure deterministic payment risk rules and actions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-630?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Allow, Monitor, Require additional verification, Route to manual review, Block, Trigger alert.
- [ ] Every transition is wired: `ADM-629`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`, `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-631` Velocity, Behavioral & Transaction Risk Controls\t168

**Manage high-frequency and abnormal payment activity.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/velocity-behavioral-transaction-risk-controls-t168-adm-631` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Customer, Device, Payment instrument reference/token, Venue, POS. Each needs an operation, or needs … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Customer (primary button) | navigation or local | — | — | — | — |
| Device (secondary button) | navigation or local | — | — | — | — |
| Payment instrument reference/token (secondary button) | navigation or local | — | — | — | — |
| Venue (secondary button) | navigation or local | — | — | — | — |
| POS (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-629` Payment Risk & Fraud Command Center\t166: *Back to Payment Risk & Fraud Command Center\t166*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The velocity behavioral transaction list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the velocity behavioral transaction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No velocity behavioral transaction yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the velocity behavioral transaction are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setPaymentRiskRules` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.3.2 | System shall detect excessive failed payment attempts. | Unified Operations Dashboard | CONTRACTED | `setPaymentRiskRules` |
| 8.3.3 | System shall detect repeated payment attempts. | Unified Operations Dashboard | CONTRACTED | `setPaymentRiskRules` |
| 8.3.54 | System shall support blacklist management. | Unified Operations Dashboard | CONTRACTED | `setPaymentRiskRules` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-631` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-631`
- Workshop pack: Payment_Payment_Orchestration.pdf board 8
- Flow F263 *Payment Payment Orchestration board 8: Payment Risk & Fraud Command Center\t166*, step 4: Works in Velocity, Behavioral & Transaction Risk Controls\t168 → Manage high-frequency and abnormal payment activity.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-631?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Customer, Device, Payment instrument reference/token, Venue, POS.
- [ ] Every transition is wired: `ADM-629`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-632` Risk Lists, Signals & Payment Control Center\t169

**Provide centralized management of approved payment risk lists and signals.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/risk-lists-signals-payment-control-center-t169-adm-632` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Trusted device, Blocked instrument reference, High-risk device, Review list. Each needs an operation, or … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Trusted device (primary button) | navigation or local | — | — | — | — |
| Blocked instrument reference (secondary button) | navigation or local | — | — | — | — |
| High-risk device (secondary button) | navigation or local | — | — | — | — |
| Review list (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-629` Payment Risk & Fraud Command Center\t166: *Back to Payment Risk & Fraud Command Center\t166*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The risk lists signals list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the risk lists signals untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No risk lists signals yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the risk lists signals are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setPaymentRiskRules` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.3.2 | System shall detect excessive failed payment attempts. | Unified Operations Dashboard | CONTRACTED | `setPaymentRiskRules` |
| 8.3.3 | System shall detect repeated payment attempts. | Unified Operations Dashboard | CONTRACTED | `setPaymentRiskRules` |
| 8.3.54 | System shall support blacklist management. | Unified Operations Dashboard | CONTRACTED | `setPaymentRiskRules` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-632` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-632`
- Workshop pack: Payment_Payment_Orchestration.pdf board 8
- Flow F263 *Payment Payment Orchestration board 8: Payment Risk & Fraud Command Center\t166*, step 6: Works in Risk Lists, Signals & Payment Control Center\t169 → Provide centralized management of approved payment risk lists and signals.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-632?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Trusted device, Blocked instrument reference, High-risk device, Review list.
- [ ] Every transition is wired: `ADM-629`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-633` Fraud Alert, Investigation & Case Management\t170

**Convert suspicious activity into controlled investigation cases.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_REFUND_APPROVE`, `RISK_INVESTIGATE`, `RISK_REVIEW` (3 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | `alertId` (navigation), `caseId` (navigation), `chargebackId` (navigation), `entityRef` (navigation), `entityType` (navigation) |
| Route | `/commercial/fraud-alert-investigation-case-management-t170-adm-633` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Open · Monitoring · Dismissed · False positive · Escalated | `listRiskAlerts` ?status |
| Band | radio group | — | Low · Medium · High · Critical | `listRiskAlerts` ?band |
| Kind | select | — | Transaction · Velocity · Entity · Network · Staff leakage · Scan abuse · Account takeover · Chargeback | `listRiskAlerts` ?kind |
| Entity type | select | — | Customer · Account · Device · Payment token · Credential · Cluster · Staff · Wallet · Ip address | `listRiskAlerts` ?entityType |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every fraud alert investigation** (data table)

| Shows | Format | Notes |
|---|---|---|
| Case ID | text | not in the schema: `Case ID` |
| Risk level | text | not in the schema: `Risk level` |
| Customer | text | not in the schema: `Customer` |
| Transaction | text | not in the schema: `Transaction` |
| Order | text | not in the schema: `Order` |
| Payment method | text | not in the schema: `Payment method` |
| Provider | text | not in the schema: `Provider` |
| Amount | text | not in the schema: `Amount` |
| Currency | text | not in the schema: `Currency` |
| Device | text | not in the schema: `Device` |
| Channel | text | not in the schema: `Channel` |
| Risk score | text | not in the schema: `Risk score` |
| Rules triggered | text | not in the schema: `Rules triggered` |
| AI signals | text | not in the schema: `AI signals` |
| Related transactions | text | not in the schema: `Related transactions` |
| Previous transactions | text | not in the schema: `Previous transactions` |
| Failed payments | text | not in the schema: `Failed payments` |
| Refunds | text | not in the schema: `Refunds` |
| Chargebacks | text | not in the schema: `Chargebacks` |
| Devices | text | not in the schema: `Devices` |
| Payment instruments | text | not in the schema: `Payment instruments` |
| Customer accounts | text | not in the schema: `Customer accounts` |

**The selected fraud alert investigation** (detail panel): The pack groups this record's detail under its own headings: “Detected”.

| Shows | Format | Notes |
|---|---|---|
| Case ID | text | not in the schema: `Case ID` |
| Risk level | text | not in the schema: `Risk level` |
| Customer | text | not in the schema: `Customer` |
| Transaction | text | not in the schema: `Transaction` |
| Order | text | not in the schema: `Order` |
| Payment method | text | not in the schema: `Payment method` |
| Provider | text | not in the schema: `Provider` |
| Amount | text | not in the schema: `Amount` |
| Currency | text | not in the schema: `Currency` |
| Device | text | not in the schema: `Device` |
| Channel | text | not in the schema: `Channel` |
| Risk score | text | not in the schema: `Risk score` |
| Rules triggered | text | not in the schema: `Rules triggered` |
| AI signals | text | not in the schema: `AI signals` |
| Related transactions | text | not in the schema: `Related transactions` |
| Previous transactions | text | not in the schema: `Previous transactions` |
| Failed payments | text | not in the schema: `Failed payments` |
| Refunds | text | not in the schema: `Refunds` |
| Chargebacks | text | not in the schema: `Chargebacks` |
| Devices | text | not in the schema: `Devices` |
| Payment instruments | text | not in the schema: `Payment instruments` |
| Customer accounts | text | not in the schema: `Customer accounts` |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Add note, Link transactions, Link customers/accounts, Request additional review, Mark confirmed fraud, Mark legitimate, Add risk-list entry, Escalate, Close case. Each needs attaching to the control it gates, or the screen needs the control.

**Data it reads**: `listChargebacks` (onLoad, Cases to investigate); `listRiskAlerts` (onLoad, Risk alerts)

**Where the user goes next**

- → `ADM-629` Payment Risk & Fraud Command Center\t166: *Back to Payment Risk & Fraud Command Center\t166*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fraud alert investigation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fraud alert investigation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No fraud alert investigation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the fraud alert investigation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already closed, or a proposed action is still awaiting approval (`case-actions-open`).; 409 The alert is already decided (`alert-not-open`).; 409 The case is already decided (`won`, `lost`, `accepted` or `expired`). (PaymentProblem); 409 The case is closed (`case-closed`). |

#### Permissions

- `listChargebacks` → `ORDER_REFUND_APPROVE` (operate) · staff
- `getEntityRisk` → `RISK_REVIEW` (operate) · staff
- `listRiskAlerts` → `RISK_REVIEW` (operate) · staff
- `decideRiskAlert` → `RISK_REVIEW` (operate) · staff
- `createRiskCase` → `RISK_INVESTIGATE` (operate) · staff
- `getRiskCase` → `RISK_INVESTIGATE` (operate) · staff
- `addRiskCaseEvidence` → `RISK_INVESTIGATE` (operate) · staff
- `expandRiskNetwork` → `RISK_INVESTIGATE` (operate) · staff
- `proposeRiskAction` → `RISK_INVESTIGATE` (operate) · staff
- `closeRiskCase` → `RISK_INVESTIGATE` (operate) · staff
- `assignChargeback` → `ORDER_REFUND_APPROVE` (operate) · staff
- `getChargebackAnalytics` → `ORDER_REFUND_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

29 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.1.54 | Calculate risk scores using user behavior, location, device, permission sensitivity and historical activity. High-risk requests may require additional verification. | F&B POS | CONTRACTED_PARTIAL | `getEntityRisk` |
| 8.3.6 | System shall detect unusual purchasing patterns. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.14 | System shall calculate chargeback risk scores. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.21 | System shall calculate refund fraud risk scores. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.33 | System shall detect suspicious device changes. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.39 | System shall detect suspicious devices. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.41 | System shall detect unusual purchase behavior. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.43 | System shall identify behavioral anomalies. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.44 | System shall calculate behavioral risk scores. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.45 | System shall assign risk scores to customers. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.47 | System shall assign risk scores to devices. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 7.1.55 | Detect suspicious access patterns including unusual login locations, failed login spikes, privilege escalation attempts and abnormal transaction behavior. | F&B POS | CONTRACTED | `listRiskAlerts` |
| … 17 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-633` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-633`
- Workshop pack: Payment_Payment_Orchestration.pdf board 8
- Flow F263 *Payment Payment Orchestration board 8: Payment Risk & Fraud Command Center\t166*, step 8: Works in Fraud Alert, Investigation & Case Management\t170 → Convert suspicious activity into controlled investigation cases.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-633?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-629`.
- [ ] Every gated control is gated: `ORDER_REFUND_APPROVE`, `RISK_INVESTIGATE`, `RISK_REVIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-634` Chargeback & Dispute Command Center\t172

**Provide centralized operational management for provider/acquirer chargebacks and payment disputes.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_REFUND_APPROVE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Display) — counts over a population, then the population |
| Offline | online only |
| Opens with | `chargebackId` (navigation) |
| Route | `/commercial/chargeback-dispute-command-center-t172-adm-634` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Period from | date picker | — | — | `getChargebackAnalytics` ?periodFrom |
| Period to | date picker | — | — | `getChargebackAnalytics` ?periodTo |
| Group by | select | Reason | Reason · Provider · Outcome · Venue · Month · Product · Product category · Customer | `getChargebackAnalytics` ?groupBy |
| Min chargebacks | number field | — | min 1 | `getChargebackAnalytics` ?minChargebacks |
| Product | picker: choose a product | — | — | `getChargebackAnalytics` ?productId |
| Provider | picker: choose a provider | — | — | `getChargebackAnalytics` ?providerId |
| Period from | date picker | — | — | `getChargebackAnalytics` ?periodFrom |
| Period to | date picker | — | — | `getChargebackAnalytics` ?periodTo |
| Group by | select | Reason | Reason · Provider · Outcome · Venue · Month · Product · Product category · Customer | `getChargebackAnalytics` ?groupBy |
| Min chargebacks | number field | — | min 1 | `getChargebackAnalytics` ?minChargebacks |
| Product | picker: choose a product | — | — | `getChargebackAnalytics` ?productId |
| Provider | picker: choose a provider | — | — | `getChargebackAnalytics` ?providerId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**New Chargebacks** (metric tile)

**Open Chargebacks** (metric tile)

**Chargeback Value** (metric tile)

**Chargeback Rate** (metric tile)

**Response Due** (metric tile)

**Won** (metric tile)

**Lost** (metric tile)

**Accepted** (metric tile)

**Represented** (metric tile)

**Recovery Value** (metric tile)

**Every chargeback dispute \t172** (data table)

| Shows | Format | Notes |
|---|---|---|
| Chargeback ID | text | not in the schema: `Chargeback ID` |
| Original payment | text | not in the schema: `Original Payment` |
| Order | text | not in the schema: `Order` |
| Customer | text | not in the schema: `Customer` |
| Provider | text | not in the schema: `Provider` |
| Acquirer | text | not in the schema: `Acquirer` |
| Merchant account | text | not in the schema: `Merchant account` |
| Amount | text | not in the schema: `Amount` |
| Currency | text | not in the schema: `Currency` |
| Reason code | text | not in the schema: `Reason code` |
| Received date | text | not in the schema: `Received date` |
| Response deadline | text | not in the schema: `Response deadline` |
| Status | text | not in the schema: `Status` |

**The selected chargeback dispute \t172** (detail panel): The pack groups this record's detail under its own headings: “Important”.

| Shows | Format | Notes |
|---|---|---|
| Chargeback ID | text | not in the schema: `Chargeback ID` |
| Original payment | text | not in the schema: `Original Payment` |
| Order | text | not in the schema: `Order` |
| Customer | text | not in the schema: `Customer` |
| Provider | text | not in the schema: `Provider` |
| Acquirer | text | not in the schema: `Acquirer` |
| Merchant account | text | not in the schema: `Merchant account` |
| Amount | text | not in the schema: `Amount` |
| Currency | text | not in the schema: `Currency` |
| Reason code | text | not in the schema: `Reason code` |
| Received date | text | not in the schema: `Received date` |
| Response deadline | text | not in the schema: `Response deadline` |
| Status | text | not in the schema: `Status` |

**Data it reads**: `listChargebacks` (onLoad, Chargebacks and disputes); `getChargebackAnalytics` (onLoad, Chargeback analytics panel); `getChargebackAnalytics` (onLoad, Chargeback analytics, groupBy product/customer)

**Where the user goes next**

- → `ADM-629` Payment Risk & Fraud Command Center\t166: *Back to Payment Risk & Fraud Command Center\t166*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The chargeback dispute \t172 list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the chargeback dispute \t172 untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No chargeback dispute \t172 yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the chargeback dispute \t172 are still there. The pack's own statuses are Received — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The case already has an outcome, or was `accepted` by the venue (a conceded case cannot be won), or the fiscal period for the decision date is not open. (PaymentProblem); 409 The case is already decided (`won`, `lost`, `accepted` or `expired`). (PaymentProblem); 409 The case is already decided or past its deadline — `won`, `lost`, `accepted` or `expired` (`chargebackClosed`). … |

#### Permissions

- `listChargebacks` → `ORDER_REFUND_APPROVE` (operate) · staff
- `respondToChargeback` → `ORDER_REFUND_APPROVE` (operate) · staff
- `recordChargeback` → `ORDER_REFUND_APPROVE` (operate) · staff, service
- `assignChargeback` → `ORDER_REFUND_APPROVE` (operate) · staff
- `recordChargebackOutcome` → `ORDER_REFUND_APPROVE` (operate) · staff, service
- `getChargebackAnalytics` → `ORDER_REFUND_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.7.92 | The system shall support chargeback notification handling, dispute management, evidence collection, investigation workflows, resolution tracking, and financial adjustments. Track chargeback status … | F&B & Guest Management | CONTRACTED | `recordChargeback` |
| 8.3.11 | System shall identify transactions with elevated chargeback risk. | Unified Operations Dashboard | CONTRACTED | `recordChargeback` |
| 4.2.21 | The system shall provide tools for tracking chargebacks, managing disputes, storing evidence, monitoring resolution status, and generating chargeback analytics. | Bundles and Promotions | CONTRACTED | `getChargebackAnalytics` |
| 8.3.12 | System shall identify customers with repeated chargebacks. | Unified Operations Dashboard | CONTRACTED | `getChargebackAnalytics` |
| 8.3.13 | System shall identify products with elevated chargeback rates. | Unified Operations Dashboard | CONTRACTED | `getChargebackAnalytics` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-634` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-634`
- Workshop pack: Payment_Payment_Orchestration.pdf board 8
- Flow F263 *Payment Payment Orchestration board 8: Payment Risk & Fraud Command Center\t166*, step 10: Works in Chargeback & Dispute Command Center\t172 → Provide centralized operational management for provider/acquirer chargebacks and payment disputes.
- ADR-0033 *Every asynchronous handoff has an outbox and a place to fail* (`docs/adr/0033-outbox-and-dead-letters.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-634?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-629`.
- [ ] Every gated control is gated: `ORDER_REFUND_APPROVE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-635` Chargeback Evidence & Representment Workspace\t173

**Help Payment Operations collect, review and submit the evidence needed to respond to disputes. This is particularly important for TICVAI because ticketing transactions generate strong operational evidence.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_DISPUTE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `chargebackId` (navigation) |
| Route | `/commercial/chargeback-evidence-representment-workspace-t173-adm-635` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Submit chargeback evidence (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-629` Payment Risk & Fraud Command Center\t166: *Back to Payment Risk & Fraud Command Center\t166*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The chargeback evidence representment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the chargeback evidence representment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No chargeback evidence representment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the chargeback evidence representment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `submitChargebackEvidence` → `PAYMENT_DISPUTE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-635` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-635`
- Workshop pack: Payment_Payment_Orchestration.pdf board 8
- Flow F263 *Payment Payment Orchestration board 8: Payment Risk & Fraud Command Center\t166*, step 12: Works in Chargeback Evidence & Representment Workspace\t173 → Help Payment Operations collect, review and submit the evidence needed to respond to disputes. This is particularly important for TICVAI because ticketing transactions generate strong operational …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-635?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Submit chargeback evidence, Cancel.
- [ ] Every transition is wired: `ADM-629`.
- [ ] Every gated control is gated: `PAYMENT_DISPUTE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-636` Payment Performance & Conversion Analytics\t174

**Provide comprehensive analytics across the complete Payment & Payment Orchestration module. This screen is not only fraud analytics. It provides payment-business performance intelligence.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Captured) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/payment-performance-conversion-analytics-t174-adm-636` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search payment performance conversion | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by provider, acquirer, payment method, card scheme, digital wallet, venue and 5 more — which are present is a decision the pack already made. | — |
| 78% | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getPaymentPerformance` ?from |
| Group by | select | — | Method · Provider · Card type · Channel · Authentication outcome · Venue | `getPaymentPerformance` ?groupBy |

#### Outputs: what the screen shows and produces

**Data it reads**: `getPaymentPerformance` (onLoad, Conversion and where sales are lost)

**Where the user goes next**

- → `ADM-629` Payment Risk & Fraud Command Center\t166: *Back to Payment Risk & Fraud Command Center\t166*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment performance conversion configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment performance conversion untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment performance conversion configured yet. Carries the create action and says what the platform does in the meantime. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment performance conversion are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getPaymentPerformance` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-636` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-636`
- Workshop pack: Payment_Payment_Orchestration.pdf board 8
- Flow F263 *Payment Payment Orchestration board 8: Payment Risk & Fraud Command Center\t166*, step 14: Works in Payment Performance & Conversion Analytics\t174 → Provide comprehensive analytics across the complete Payment & Payment Orchestration module. This screen is not only fraud analytics. It provides payment-business performance intelligence.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-636?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-629`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-637` AI Fraud, Anomaly & Payment Intelligence Center\t175

**Provide governed AI/ML capabilities for fraud detection and payment anomaly identification.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `ORDER_REFUND_APPROVE`, `PAYMENT_VIEW`, `RISK_REVIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `entityRef` (navigation), `entityType` (navigation) |
| Route | `/commercial/ai-fraud-anomaly-payment-intelligence-center-t175-adm-637` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getPaymentPerformance` ?from |
| Group by | select | — | Method · Provider · Card type · Channel · Authentication outcome · Venue | `getPaymentPerformance` ?groupBy |
| Status | radio group | — | Open · Monitoring · Dismissed · False positive · Escalated | `listRiskAlerts` ?status |
| Band | radio group | — | Low · Medium · High · Critical | `listRiskAlerts` ?band |
| Kind | select | — | Transaction · Velocity · Entity · Network · Staff leakage · Scan abuse · Account takeover · Chargeback | `listRiskAlerts` ?kind |
| Entity type | select | — | Customer · Account · Device · Payment token · Credential · Cluster · Staff · Wallet · Ip address | `listRiskAlerts` ?entityType |
| Period from | date picker | — | — | `getChargebackAnalytics` ?periodFrom |
| Period to | date picker | — | — | `getChargebackAnalytics` ?periodTo |
| Group by | select | Reason | Reason · Provider · Outcome · Venue · Month · Product · Product category · Customer | `getChargebackAnalytics` ?groupBy |
| Min chargebacks | number field | — | min 1 | `getChargebackAnalytics` ?minChargebacks |
| Product | picker: choose a product | — | — | `getChargebackAnalytics` ?productId |
| Provider | picker: choose a provider | — | — | `getChargebackAnalytics` ?providerId |
| Period from | date picker | — | — | `getChargebackAnalytics` ?periodFrom |
| Period to | date picker | — | — | `getChargebackAnalytics` ?periodTo |
| Group by | select | Reason | Reason · Provider · Outcome · Venue · Month · Product · Product category · Customer | `getChargebackAnalytics` ?groupBy |
| Min chargebacks | number field | — | min 1 | `getChargebackAnalytics` ?minChargebacks |
| … 2 more | | | | `operations.json` |

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

**Data it reads**: `getPaymentPerformance` (onLoad, Anomalies in payment behaviour); `listRiskAlerts` (onLoad, Risk alerts); `getChargebackAnalytics` (onLoad, Chargeback analytics panel); `getChargebackAnalytics` (onLoad, Chargeback trend beside payment risk)

**Where the user goes next**

- → `ADM-629` Payment Risk & Fraud Command Center\t166: *Back to Payment Risk & Fraud Command Center\t166*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fraud anomaly payment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fraud anomaly payment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No fraud anomaly payment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the fraud anomaly payment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The outcome map declines without `declineGoverned` (`decline-not-governed`). |

#### Permissions

- `getPaymentPerformance` → `PAYMENT_VIEW` (read) · staff
- `getEntityRisk` → `RISK_REVIEW` (operate) · staff
- `configureRiskStrategy` → `AI_CONFIGURE` (configure) · staff
- `listRiskAlerts` → `RISK_REVIEW` (operate) · staff
- `getChargebackAnalytics` → `ORDER_REFUND_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

29 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.1.54 | Calculate risk scores using user behavior, location, device, permission sensitivity and historical activity. High-risk requests may require additional verification. | F&B POS | CONTRACTED_PARTIAL | `getEntityRisk` |
| 8.3.6 | System shall detect unusual purchasing patterns. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.14 | System shall calculate chargeback risk scores. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.21 | System shall calculate refund fraud risk scores. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.33 | System shall detect suspicious device changes. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.39 | System shall detect suspicious devices. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.41 | System shall detect unusual purchase behavior. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.43 | System shall identify behavioral anomalies. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.44 | System shall calculate behavioral risk scores. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.45 | System shall assign risk scores to customers. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.47 | System shall assign risk scores to devices. | Unified Operations Dashboard | CONTRACTED | `getEntityRisk` |
| 8.3.48 | System shall support configurable risk thresholds. | Unified Operations Dashboard | CONTRACTED | `configureRiskStrategy` |
| … 17 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-637` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-637`
- Workshop pack: Payment_Payment_Orchestration.pdf board 8
- Flow F263 *Payment Payment Orchestration board 8: Payment Risk & Fraud Command Center\t166*, step 16: Works in AI Fraud, Anomaly & Payment Intelligence Center\t175 → Provide governed AI/ML capabilities for fraud detection and payment anomaly identification.
- ADR-0053 *Owners keep their deterministic rules; AI owns cross-entity risk, alerts and cases* (`docs/adr/0053-risk-layer-ownership.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-637?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-629`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `ORDER_REFUND_APPROVE`, `PAYMENT_VIEW`, `RISK_REVIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-638` Payment Executive Intelligence, Risk Simulator & AI Advisor\t176

**Provide executive-level intelligence and a safe simulation environment for payment, fraud and risk strategies.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `PAYMENT_CONFIGURE` (2 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Show; Monitor) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/payment-executive-intelligence-risk-simulator-ai-advisor-adm-638` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Total Payment Value** (metric tile)

**Payment Success Rate** (metric tile)

**Authorization Rate** (metric tile)

**Payment Cost** (metric tile)

**Refund Rate** (metric tile)

**Fraud Rate** (metric tile)

**Chargeback Rate** (metric tile)

**Settlement Accuracy** (metric tile)

**Provider Performance** (metric tile)

**Payment Conversion** (metric tile)

**↓** (metric tile)

**Where the user goes next**

- → `ADM-629` Payment Risk & Fraud Command Center\t166: *Back to Payment Risk & Fraud Command Center\t166*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment executive intelligence list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment executive intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment executive intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment executive intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `simulatePaymentConfiguration` → `PAYMENT_CONFIGURE` (configure) · staff
- `backtestRiskStrategy` → `AI_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-638` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS94 Payment Payment Orchestration Board 8.dc.html#adm-638`
- Workshop pack: Payment_Payment_Orchestration.pdf board 8
- Flow F263 *Payment Payment Orchestration board 8: Payment Risk & Fraud Command Center\t166*, step 18: Works in Payment Executive Intelligence, Risk Simulator & AI Advisor\t176 → Provide executive-level intelligence and a safe simulation environment for payment, fraud and risk strategies.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-638?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-629`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `PAYMENT_CONFIGURE`.
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
"addRiskCaseEvidence": {"method":"POST","path":"/risk/cases/{caseId}/evidence","contract":"ai","summary":"Add evidence to a case","permission":"RISK_INVESTIGATE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiRiskCaseEvidence","responds":"AiRiskCaseEvidence"},
"assignChargeback": {"method":"POST","path":"/chargebacks/{chargebackId}/assign","contract":"orders","summary":"Give a chargeback to an investigator, with a note","permission":"ORDER_REFUND_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Chargeback"},
"backtestRiskStrategy": {"method":"POST","path":"/risk/strategy/backtest","contract":"ai","summary":"Backtest a draft strategy","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRiskBacktest"},
"closeRiskCase": {"method":"POST","path":"/risk/cases/{caseId}/close","contract":"ai","summary":"Close a case with an outcome","permission":"RISK_INVESTIGATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRiskCase"},
"configureRiskStrategy": {"method":"PUT","path":"/risk/strategy","contract":"ai","summary":"Set the risk strategy","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiRiskStrategy","responds":"AiRiskStrategy"},
"createRiskCase": {"method":"POST","path":"/risk/cases","contract":"ai","summary":"Open an investigation","permission":"RISK_INVESTIGATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRiskCase"},
"decideRiskAlert": {"method":"POST","path":"/risk/alerts/{alertId}/decide","contract":"ai","summary":"Dismiss, monitor, mark false positive, or escalate","permission":"RISK_REVIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRiskAlert"},
"expandRiskNetwork": {"method":"GET","path":"/risk/network","contract":"ai","summary":"Expand the relationship graph around an entity","permission":"RISK_INVESTIGATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"entityType","in":"query","required":true},{"name":"entityRef","in":"query","required":true},{"name":"hops","in":"query","required":null},{"name":"maxNodes","in":"query","required":null}],"requestBody":null,"responds":"AiRiskNetwork"},
"getChargebackAnalytics": {"method":"GET","path":"/chargebacks/analytics","contract":"orders","summary":"Chargeback rate, win and loss, by reason, provider, outcome and period","permission":"ORDER_REFUND_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"periodFrom","in":"query","required":true},{"name":"periodTo","in":"query","required":true},{"name":"groupBy","in":"query","required":null},{"name":"minChargebacks","in":"query","required":null},{"name":"productId","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"providerId","in":"query","required":null}],"requestBody":null,"responds":"OrdChargebackAnalytics"},
"getEntityRisk": {"method":"GET","path":"/risk/entities/{entityType}/{entityRef}","contract":"ai","summary":"Current risk of an entity","permission":"RISK_REVIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"AiEntityRisk"},
"getPaymentPerformance": {"method":"GET","path":"/payment-performance","contract":"payments","summary":"Authorisation rate, conversion and where payments are lost","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"PaymentPerformanceRow"},
"getRiskCase": {"method":"GET","path":"/risk/cases/{caseId}","contract":"ai","summary":"A case with its evidence and actions","permission":"RISK_INVESTIGATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiRiskCaseDetail"},
"listChargebacks": {"method":"GET","path":"/chargebacks","contract":"orders","summary":"Open disputes, by deadline","permission":"ORDER_REFUND_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFraudRules": {"method":"GET","path":"/fraud-rules","contract":"orders","summary":"The rules evaluated before a charge","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRiskAlerts": {"method":"GET","path":"/risk/alerts","contract":"ai","summary":"Risk alerts","permission":"RISK_REVIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"band","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"entityType","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"proposeRiskAction": {"method":"POST","path":"/risk/cases/{caseId}/actions","contract":"ai","summary":"Propose a restrictive action from a case","permission":"RISK_INVESTIGATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRiskCaseAction"},
"recordChargeback": {"method":"POST","path":"/chargebacks/intake","contract":"orders","summary":"Take in a chargeback notified by a provider","permission":"ORDER_REFUND_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Chargeback"},
"recordChargebackOutcome": {"method":"POST","path":"/chargebacks/{chargebackId}/outcome","contract":"orders","summary":"Record the bank's decision and adjust the ledger","permission":"ORDER_REFUND_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Chargeback"},
"respondToChargeback": {"method":"POST","path":"/chargebacks/{chargebackId}/respond","contract":"orders","summary":"Submit evidence, or accept the loss","permission":"ORDER_REFUND_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Chargeback"},
"setFraudRules": {"method":"PUT","path":"/fraud-rules","contract":"orders","summary":"Change what holds a transaction","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"FraudRuleSet","responds":"FraudRuleSet"},
"setPaymentRiskRules": {"method":"PUT","path":"/payment-risk-rules","contract":"payments","summary":"Velocity, behaviour, lists and what a hit does","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"PaymentRiskRules","responds":"PaymentRiskRules"},
"simulatePaymentConfiguration": {"method":"POST","path":"/payment-configuration/simulate","contract":"payments","summary":"What a guest would be offered, and what it would cost","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RoutingContext","responds":"PaymentConfigurationSimulation"},
"submitChargebackEvidence": {"method":"POST","path":"/chargebacks/{chargebackId}/evidence","contract":"payments","summary":"Assemble and send a representment","permission":"PAYMENT_DISPUTE","offlineCapable":null,"conflictPolicy":"append","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ChargebackEvidence","responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiEntityRisk": {"type":"object","x-ticvai-persistence":"ai.entity_risk","description":"**Current risk per entity** (design 5.3, AIP-128): customer, account, device, payment token, credential, cluster or staff member, computed asynchronously from composite signals — no single signal decides (M21).","required":["entityType","entityRef","score","band"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"entityType":{"type":"string","enum":["customer","account","device","paymentToken","credential","cluster","staff","ipAddress"]},"entityRef":{"type":"string","description":"The entity id, or a hashed device id, hashed IP address or provider token reference. Never a card number or a raw IP address."},"score":{"type":"integer","minimum":0,"maximum":100},"band":{"type":"string","enum":["low","medium","high","critical"],"description":"Design 5.6: a risk score and band, never a probability."},"signals":{"type":"object","additionalProperties":true,"description":"Contributing signals with their weights and freshness. Since 29 September (build) they include chargeback count and rate (`order.chargebackRecorded`), password resets (`identity.credentialResetRequested`), IP velocity and country mismatch, and storefront browsing features (`storefront.sessionEvent`)."},"lastEventAt":{"type":"string","format":"date-time","nullable":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiRiskAlert": {"type":"object","x-ticvai-persistence":"ai.risk_alert","description":"**A risk alert** (AIP-109): raised by scoring or re-scoring. **Alert, case and confirmed fraud are kept distinct** (AIP-163): an alert is a signal to look, not a finding.","required":["kind","entityType","entityRef","band","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["transaction","velocity","entity","network","staffLeakage","scanAbuse","accountTakeover","chargeback"]},"entityType":{"type":"string","enum":["customer","account","device","paymentToken","credential","cluster","staff","wallet","ipAddress"]},"entityRef":{"type":"string"},"score":{"type":"integer","minimum":0,"maximum":100},"band":{"type":"string","enum":["low","medium","high","critical"],"description":"Design 5.6: a risk score and band, never a probability."},"reasonCodes":{"type":"array","items":{"type":"string"}},"correlationKey":{"type":"string","nullable":true},"assessmentId":{"type":"string","format":"uuid","nullable":true},"status":{"type":"string","enum":["open","monitoring","dismissed","falsePositive","escalated"],"readOnly":true},"caseId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.risk_case"},"raisedAt":{"type":"string","format":"date-time","readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"decisionNote":{"type":"string","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiRiskBacktest": {"type":"object","x-ticvai-persistence":"none — computed over ai.risk_assessment and labelled outcomes","description":"What a draft strategy would have done over a past window: review rate, recall and precision against analyst-labelled outcomes, and false-positive rate by segment (AIP-143).","required":["evaluated"],"properties":{"evaluated":{"type":"integer"},"reviewRate":{"type":"number"},"recall":{"type":"number","nullable":true},"precision":{"type":"number","nullable":true},"bySegment":{"type":"array","items":{"type":"object","properties":{"segment":{"type":"string","enum":["family","b2b","reseller","member","other"]},"falsePositiveRate":{"type":"number"}}}},"outcomeCounts":{"type":"object","additionalProperties":true}}},
"AiRiskCase": {"type":"object","x-ticvai-persistence":"ai.risk_case","description":"**An investigation** (AIP-150..160). Its evidence and actions are `ai.case_evidence` and `ai.case_action`. The summary is written by a model from structured evidence only (AIP-153); the outcome is a person's.","required":["reference","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"reference":{"type":"string","readOnly":true},"title":{"type":"string"},"status":{"type":"string","enum":["open","investigating","pendingAction","closed"],"readOnly":true},"priority":{"type":"string","enum":["low","medium","high","critical"]},"entities":{"type":"array","items":{"type":"object","properties":{"entityType":{"type":"string","enum":["customer","account","device","paymentToken","credential","cluster","staff"]},"entityRef":{"type":"string"}}}},"alertIds":{"type":"array","items":{"type":"string","format":"uuid"}},"assigneePrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal"},"summary":{"type":"string","nullable":true,"readOnly":true},"outcome":{"type":"string","enum":["confirmedFraud","notFraud","inconclusive"],"nullable":true,"readOnly":true},"closureNote":{"type":"string","nullable":true,"readOnly":true},"openedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"openedAt":{"type":"string","format":"date-time","readOnly":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"closedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiRiskCaseAction": {"type":"object","x-ticvai-persistence":"ai.case_action","description":"**A restrictive action proposed from a case** (AIP-136). It goes to the owning module through the action pipeline, never straight from review; at the first-release ceiling (L1 advisory, design 3.8) it is a recommendation the owning module's operator applies. **Scoped through its case.**","required":["caseId","action","targetContract"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"caseId":{"type":"string","format":"uuid","x-ticvai-references":"ai.risk_case"},"action":{"type":"string","enum":["blockPaymentToken","suspendAccount","restrictWallet","revokeEntitlement","flagCustomer","requireStepUp","holdRefunds","lockIdentity"]},"targetContract":{"type":"string"},"targetOperation":{"type":"string"},"targetRef":{"type":"string"},"rationale":{"type":"string"},"status":{"type":"string","enum":["recommended","planned","awaitingApproval","applied","rejected","failed"],"readOnly":true},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan"},"proposedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"proposedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AiRiskCaseDetail": {"type":"object","x-ticvai-persistence":"none — ai.risk_case with its evidence, actions and alerts","description":"A case with everything attached to it.","required":["case"],"properties":{"case":{"$ref":"#/components/schemas/AiRiskCase"},"evidence":{"type":"array","items":{"$ref":"#/components/schemas/AiRiskCaseEvidence"}},"actions":{"type":"array","items":{"$ref":"#/components/schemas/AiRiskCaseAction"}},"alerts":{"type":"array","items":{"$ref":"#/components/schemas/AiRiskAlert"}}}},
"AiRiskCaseEvidence": {"type":"object","x-ticvai-persistence":"ai.case_evidence","description":"**Case evidence** (AIP-155): `jsonb` plus an immutable Blob copy. **Scoped through its case** (`platform.apply_parent_rls`). Never edited; a correction is new evidence.","required":["caseId","kind","label"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"caseId":{"type":"string","format":"uuid","x-ticvai-references":"ai.risk_case"},"kind":{"type":"string","enum":["assessment","alert","transaction","networkSnapshot","note","document"]},"ref":{"type":"string","nullable":true},"content":{"type":"object","additionalProperties":true,"nullable":true},"blobRef":{"type":"string","nullable":true,"readOnly":true,"description":"The immutable (WORM) copy."},"label":{"type":"string","enum":["source","derived","modelInferred"]},"contentHash":{"type":"string","readOnly":true},"addedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"addedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AiRiskEdge": {"type":"object","x-ticvai-persistence":"ai.risk_edge","description":"**A relationship-graph edge** (design 2.4, AIP-111): shared device, token or account, with strength. Queried 1 to 3 hops by `expandRiskNetwork`; no graph database.","required":["fromEntityType","fromEntityRef","toEntityType","toEntityRef","relation"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"fromEntityType":{"type":"string","enum":["customer","account","device","paymentToken","credential","cluster","staff","ipAddress"]},"fromEntityRef":{"type":"string"},"toEntityType":{"type":"string","enum":["customer","account","device","paymentToken","credential","cluster","staff","ipAddress"]},"toEntityRef":{"type":"string"},"relation":{"type":"string","enum":["sharedDevice","sharedToken","sharedAccount","sharedContact","sharedIp","transfer","companion","staffCustomer"]},"strength":{"type":"number","minimum":0,"maximum":1},"firstSeenAt":{"type":"string","format":"date-time"},"lastSeenAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiRiskNetwork": {"type":"object","x-ticvai-persistence":"none — read from ai.risk_edge and ai.entity_risk","description":"A bounded 1..3-hop neighbourhood of an entity (AIP-111).","required":["nodes","edges"],"properties":{"nodes":{"type":"array","items":{"$ref":"#/components/schemas/AiEntityRisk"}},"edges":{"type":"array","items":{"$ref":"#/components/schemas/AiRiskEdge"}},"truncated":{"type":"boolean","description":"The hop or node limit cut the result."}}},
"AiRiskStrategy": {"type":"object","x-ticvai-persistence":"ai.risk_strategy","description":"**The tenant's risk strategy** (C10, AIP-096..165): weighted rule contributions, thresholds, modes and the map from band to outcome by channel and value (AIP-100). **Fail-open with holds, not declines, by default** (decided 29 September, decision 6): `decline` appears in `outcomeMap` only where the tenant governed it.","required":["version","mode","thresholds"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"version":{"type":"integer","minimum":1,"readOnly":true},"mode":{"type":"string","enum":["monitor","enforce"],"description":"Monitor records outcomes without acting; how a new strategy earns trust."},"weights":{"type":"object","additionalProperties":true,"description":"Contribution of each rule and signal to the composite 0..100 score."},"thresholds":{"type":"object","properties":{"monitor":{"type":"integer","minimum":0,"maximum":100},"stepUp":{"type":"integer","minimum":0,"maximum":100},"holdForReview":{"type":"integer","minimum":0,"maximum":100},"decline":{"type":"integer","minimum":0,"maximum":100,"nullable":true}}},"outcomeMap":{"type":"array","items":{"type":"object","properties":{"band":{"type":"string","enum":["low","medium","high","critical"]},"channel":{"type":"string","nullable":true},"minAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"outcome":{"type":"string","enum":["allow","monitor","stepUp","holdForReview","decline"]}}}},"failMode":{"type":"string","enum":["open","holdForReview"],"default":"open","description":"On timeout or AI down. Never a silent decline (AIP-110)."},"declineGoverned":{"type":"boolean","default":false,"description":"Set only through `configureRiskStrategy` by `AI_APPROVE`; without it no `decline` outcome is accepted."},"modelEnabled":{"type":"boolean","default":false,"readOnly":true,"description":"Adds the promoted model's score where one is promoted for this tenant (design 3.5)."},"status":{"type":"string","enum":["draft","active","superseded"],"readOnly":true},"publishedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"Chargeback": {"type":"object","x-ticvai-persistence":"orders.chargeback + orders.chargeback_evidence + orders.chargeback_investigation_log","description":"BL-118, CF-144. **A chargeback is not a refund**, and treating it as one is how a venue loses them by default.\nA refund is a decision the venue makes. **A chargeback is a decision a bank makes, on a clock the venue does not control** — evidence is due in days, a deadline missed is a case lost regardless of merit, and there is a fee either way.\nThe money is already gone when this record is created. **Representment is an argument, not a reversal.**\n","required":["id","paymentId","amount","reason","status","evidenceDueBy"],"properties":{"id":{"type":"string","format":"uuid"},"paymentId":{"type":"string","format":"uuid"},"providerId":{"type":"string","format":"uuid"},"providerCaseReference":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"feeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reason":{"type":"string","enum":["fraudulent","productNotReceived","productUnacceptable","duplicate","subscriptionCancelled","creditNotProcessed","unrecognised","other"],"description":"**The scheme's reason code, mapped.** Which evidence wins depends entirely on it — a *product not received* case is answered by a scan record and a *fraudulent* case is not.\n"},"status":{"type":"string","enum":["received","underReview","evidenceSubmitted","won","lost","accepted","expired"]},"evidenceDueBy":{"type":"string","format":"date-time","description":"**The field the whole record exists for.** A deadline missed is a case lost on merit nobody read, and it is the one date that must reach a person rather than a report.\n"},"evidenceSubmittedAt":{"type":"string","format":"date-time","nullable":true},"evidence":{"type":"array","description":"**What the platform can prove**, assembled rather than typed: the order, the scan that admitted them, the delivery, the terms accepted, the IP and device. A venue answering a chargeback by hand is a venue answering it late.\nHeld as rows of `orders.chargeback_evidence`, one per item (29 September, build: a list of objects needs its own table to be stored at all).\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["order","scanRecord","deliveryProof","termsAccepted","communication","deviceFingerprint","other"]},"reference":{"type":"string"}}}},"outcomeAt":{"type":"string","format":"date-time","nullable":true},"schemeReasonCode":{"type":"string","nullable":true,"description":"The card scheme's own reason code as notified, beside the mapped `reason` (5.7.92)."},"notifiedAt":{"type":"string","format":"date-time","nullable":true,"description":"When the provider notified the case; the date its debit posts to (`recordChargeback`)."},"assigneePrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who is investigating (`assignChargeback`)."},"investigationLog":{"type":"array","description":"Notes from `assignChargeback` and `recordChargebackOutcome`, oldest first, with who wrote each and when. Append-only. Held as rows of `orders.chargeback_investigation_log` (29 September, build).","items":{"type":"object","properties":{"note":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"}}}},"debitJournalEntryId":{"type":"string","format":"uuid","nullable":true,"description":"The `chargebackDebit` (and `chargebackFee`) entry posted at intake."},"outcomeJournalEntryId":{"type":"string","format":"uuid","nullable":true,"description":"The `chargebackReversal` entry posted when the case is won, or the additional fee when lost."}}},
"ChargebackEvidence": {"type":"object","x-ticvai-persistence":"payments.chargeback_evidence","description":"Board 8.7. **The platform holds every document already.**","required":["chargebackId"],"properties":{"chargebackId":{"type":"string","format":"uuid"},"narrative":{"type":"string","nullable":true},"documents":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["authorisationRecord","receipt","termsAccepted","admissionScan","deliveryProof","communicationLog","refundPolicy","other"]},"assetId":{"type":"string","format":"uuid"},"autoAssembled":{"type":"boolean","default":true}}}},"submittedAt":{"type":"string","format":"date-time","nullable":true},"deadlineAt":{"type":"string","format":"date-time","nullable":true},"outcome":{"type":"string","enum":["pending","won","lost","withdrawn"],"nullable":true},"scopePath":{"type":"string"}}},
"FraudRule": {"type":"object","x-ticvai-persistence":"orders.fraud_rule","description":"BL-118. **Evaluated before the charge, and it holds rather than refuses.**\nA rule that declines outright turns a false positive into a lost sale with an angry guest. **A rule that flags for review turns it into a delay** — and at a gate, review means a supervisor rather than a rejection.\n","required":["id","name","condition","action","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"condition":{"type":"object","description":"Velocity, amount, issuer country, device reuse, mismatched billing.","additionalProperties":true},"appliesTo":{"type":"string","description":"**`refund` rules are evaluated on `createRefund` and `createRefundRequest`** (5.3.33, 29 September build pass), before the money moves: a hold sends the refund to approval rather than refusing it. `charge` rules are evaluated before a charge, as before.","enum":["charge","refund"],"default":"charge"},"signal":{"type":"string","nullable":true,"description":"The measured signal where the rule is one of the named ones; `condition` carries anything else. **`refundCount`, `refundValue` and `refundRatio` detect excessive refunds by one guest** (or one payment card, per `subjectKey`) over `windowDays`: the number of refunds, their total value, or refunds as a share of what that guest bought in the window. **Counted over every sales channel** (5.3.33): tickets, F&B, retail (a retail return raises its refund here, `RetailReturn.refundId`) and every other line, because every refund is an `orders.refund` whichever channel sold it. The access `excessiveRefunds` signal is the gate-side view of ticket refunds only.","enum":["velocityCount","velocityAmount","issuerCountry","deviceReuse","billingMismatch","refundCount","refundValue","refundRatio"]},"subjectKey":{"type":"string","enum":["guest","paymentToken","device"],"default":"guest"},"threshold":{"type":"number","nullable":true},"windowDays":{"type":"integer","minimum":1,"nullable":true},"action":{"type":"string","enum":["allow","flagForReview","requireStepUp","hold","decline"]},"riskWeight":{"type":"integer"},"isActive":{"type":"boolean"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"FraudRuleSet": {"type":"object","x-ticvai-persistence":"none — the whole set of orders.fraud_rule rows, in evaluation order","description":"**The whole set in one body**, as `setFraudRules` requires: a rule set edited one rule at a time spends time in states nobody intended. A rule left out of the set is deactivated, never deleted.\n","required":["rules"],"properties":{"rules":{"type":"array","description":"In evaluation order.","items":{"$ref":"#/components/schemas/FraudRule"}}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"OrdChargebackAnalytics": {"x-ticvai-persistence":"none — computed from orders.chargeback and orders.payment on the reporting replica","type":"object","description":"4.2.21. Chargeback measures for a period, in total and per group.","required":["periodFrom","periodTo","groupBy","totals","groups"],"properties":{"periodFrom":{"type":"string","format":"date"},"periodTo":{"type":"string","format":"date"},"groupBy":{"type":"string"},"totals":{"$ref":"#/components/schemas/OrdChargebackMeasures"},"groups":{"type":"array","items":{"allOf":[{"$ref":"#/components/schemas/OrdChargebackMeasures"},{"type":"object","required":["key"],"properties":{"key":{"type":"string","description":"The reason, provider id, outcome, venue id, month (`YYYY-MM`), product id, product category id, or guest `subjectId` (`anonymous` for purchases with no guest) of the group."},"label":{"type":"string","nullable":true,"description":"The display name of the group's key. Null for `customer` unless the caller holds `GUEST_VIEW_PII`."}}}]}}}},
"OrdChargebackMeasures": {"x-ticvai-persistence":"none — computed","type":"object","properties":{"chargebackCount":{"type":"integer"},"chargebackAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"cardPaymentCount":{"type":"integer"},"chargebackRateByCount":{"type":"number","description":"Chargebacks received per card payment captured in the period, as a fraction."},"chargebackRateByValue":{"type":"number"},"decidedCount":{"type":"integer"},"wonCount":{"type":"integer"},"lostCount":{"type":"integer"},"acceptedCount":{"type":"integer"},"expiredCount":{"type":"integer","description":"Lost to a missed evidence deadline."},"winRate":{"type":"number","nullable":true,"description":"Won over decided (won, lost, expired); null with none decided."},"recoveredAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"feeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"openCount":{"type":"integer"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PaymentConfigurationSimulation": {"type":"object","description":"Boards 1.10 and 5.10. **Eight boards of configuration that compose, silently.**","properties":{"offeredMethods":{"type":"array","items":{"type":"object","properties":{"methodId":{"type":"string","format":"uuid"},"name":{"type":"string"},"routesTo":{"type":"string","nullable":true},"estimatedCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"surcharge":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"suppressedMethods":{"type":"array","items":{"type":"object","properties":{"methodId":{"type":"string","format":"uuid"},"reason":{"type":"string"}}}},"findings":{"type":"array","items":{"type":"object","properties":{"severity":{"type":"string","enum":["blocking","warning"]},"message":{"type":"string"}}}}}},
"PaymentPerformanceRow": {"type":"object","description":"Board 8.8. **The last and most expensive place a venue loses a sale.**","properties":{"key":{"type":"string"},"label":{"type":"string"},"attempts":{"type":"integer"},"authorised":{"type":"integer"},"declined":{"type":"integer"},"errored":{"type":"integer"},"abandoned":{"type":"integer"},"authorisationRate":{"type":"number"},"conversionRate":{"type":"number"},"averageValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"topDeclineReason":{"type":"string","nullable":true}}},
"PaymentRiskRules": {"type":"object","x-ticvai-persistence":"payments.risk_rules","description":"Boards 8.2 to 8.4. **Distinct from `wallet` risk** — this watches card presentation.\n","properties":{"rules":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"signal":{"type":"string","enum":["cardAcrossAccounts","accountAcrossCards","deviceAcrossCards","velocityCount","velocityAmount","issuerCountryMismatch","highRiskBin","listHit","repeatedDecline"]},"threshold":{"type":"number","nullable":true},"windowMinutes":{"type":"integer","nullable":true},"listCode":{"type":"string","nullable":true},"action":{"type":"string","enum":["scoreOnly","challenge","refuse","allowAndFlag","raiseCase"]}}}},"lists":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"kind":{"type":"string","enum":["blockCard","blockBin","blockEmail","blockDevice","blockIp","allowAlways"],"description":"`blockIp` entries are IPv4 or IPv6 addresses or CIDR ranges (no wider than /16 for IPv4 or /32 for IPv6, so one entry cannot block a country's mobile network), matched at the edge (29 September, build pass; 8.3.8)."},"entries":{"type":"integer","readOnly":true}}}},"scopePath":{"type":"string"}}},
"RoutingContext": {"type":"object","required":["amount"],"properties":{"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"methodId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"channel":{"type":"string","nullable":true},"cardScheme":{"type":"string","nullable":true},"cardIssuerCountry":{"type":"string","nullable":true},"cardPresent":{"type":"boolean","default":false},"customerId":{"type":"string","format":"uuid","nullable":true}}}
}
```
