# WS147 — Payment Payment Orchestration board 1

**10 screens · 8 operations · 14 schemas · 3 permissions**

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
  `APPROVAL_REQUEST, PAYMENT_CONFIGURE, PAYMENT_VIEW`. A control nobody can use must say so,
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
| `ADM-559` | Payment Command Center\t7 | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-560` | Payment Method Catalogue\t8 | B–D | 0 | 4 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-561` | Payment Method Configuration\t9 | B–D | 16 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-562` | Channel & Touchpoint Payment Configuration\t10 | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-563` | Venue, Location & Business Unit Payment Assignment\t11 | B–D | 7 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-564` | Currency & Payment Currency Configuration\t12 | B–D | 5 | 0 | 6 | 0 | 0 | 4 | — | notStarted (—) |
| `ADM-565` | Payment Eligibility & Availability Rule Builder\t13 | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-566` | Payment Fees, Surcharges & Commercial Rules\t14 | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-567` | Payment Policy, Governance & Approval Manager\t15 | B–D | 7 | 0 | 6 | 5 | 0 | 3 | — | notStarted (—) |
| `ADM-568` | Payment Configuration Simulator & Validation Center\t16 | B–D | 0 | 8 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-560, ADM-562, ADM-568 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-559` Payment Command Center\t7

**Provide centralized visibility into payment operations and configuration across the tenant.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/payment-command-center-t7-adm-559` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | text field | — | — | `listPaymentMethods` ?channel |
| From | date and time picker | — | — | `getPaymentPerformance` ?from |
| Group by | select | — | Method · Provider · Card type · Channel · Authentication outcome · Venue | `getPaymentPerformance` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Total Payment Transactions** (metric tile)

**Successful Payments** (metric tile)

**Failed Payments** (metric tile)

**Payment Success Rate** (metric tile)

**Payment Value** (metric tile)

**Refund Value** (metric tile)

**Active Payment Methods** (metric tile)

**Active Gateways** (metric tile)

**Active Terminals** (metric tile)

**Active Currencies** (metric tile)

**Payment Exceptions** (metric tile)

**Configuration Alerts** (metric tile)

**Data it reads**: `listPaymentMethods` (onLoad, Methods in use); `getPaymentPerformance` (onLoad, How they are performing)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-560` Payment Method Catalogue\t8: *Payment Method Catalogue\t8*
- → `ADM-561` Payment Method Configuration\t9: *Payment Method Configuration\t9*
- → `ADM-562` Channel & Touchpoint Payment Configuration\t10: *Channel & Touchpoint Payment Configuration\t10*
- → `ADM-563` Venue, Location & Business Unit Payment Assignment\t11: *Venue, Location & Business Unit Payment Assignment\t11*
- → `ADM-564` Currency & Payment Currency Configuration\t12: *Currency & Payment Currency Configuration\t12*
- → `ADM-565` Payment Eligibility & Availability Rule Builder\t13: *Payment Eligibility & Availability Rule Builder\t13*
- → `ADM-566` Payment Fees, Surcharges & Commercial Rules\t14: *Payment Fees, Surcharges & Commercial Rules\t14*
- → `ADM-567` Payment Policy, Governance & Approval Manager\t15: *Payment Policy, Governance & Approval Manager\t15*
- → `ADM-568` Payment Configuration Simulator & Validation Center\t16: *Payment Configuration Simulator & Validation Center\t16*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment \t7 list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment \t7 untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment \t7 yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment \t7 are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPaymentMethods` → `PAYMENT_VIEW` (read) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-559` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-559`
- Workshop pack: Payment_Payment_Orchestration.pdf board 1
- Flow F256 *Payment Payment Orchestration board 1: Payment Command Center\t7*, step 1: Opens Payment Command Center\t7 → Provide centralized visibility into payment operations and configuration across the tenant.
- Flow F256 *Payment Payment Orchestration board 1: Payment Command Center\t7*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F256 *Payment Payment Orchestration board 1: Payment Command Center\t7*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F256 *Payment Payment Orchestration board 1: Payment Command Center\t7*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F256 *Payment Payment Orchestration board 1: Payment Command Center\t7*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F256 *Payment Payment Orchestration board 1: Payment Command Center\t7*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F256 *Payment Payment Orchestration board 1: Payment Command Center\t7*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F256 *Payment Payment Orchestration board 1: Payment Command Center\t7*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F256 branch at step 1 (expected): when Nothing has been set up on Payment Command Center\t7 yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F256 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-559?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-560`, `ADM-561`, `ADM-562`, `ADM-563`, `ADM-564`, `ADM-565`, `ADM-566`, `ADM-567`, `ADM-568`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-560` Payment Method Catalogue\t8

**Maintain the centralized catalogue of payment/tender types supported by TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE`, `PAYMENT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Cards) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/payment-method-catalogue-t8-adm-560` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | text field | — | — | `listPaymentMethods` ?channel |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every payment method catalogue\t8** (data table)

| Shows | Format | Notes |
|---|---|---|
| Credit card | text | not in the schema: `Credit card` |
| Debit card | text | not in the schema: `Debit card` |

**The selected payment method catalogue\t8** (detail panel): The pack groups this record's detail under its own headings: “Cash”, “Digital Payments”, “Stored / Controlled Value”, “Commercial / B2B”, “Other”, “Each method should contain”.

| Shows | Format | Notes |
|---|---|---|
| Credit card | text | not in the schema: `Credit card` |
| Debit card | text | not in the schema: `Debit card` |

**Data it reads**: `listPaymentMethods` (onLoad, The catalogue)

**Where the user goes next**

- → `ADM-559` Payment Command Center\t7: *Back to Payment Command Center\t7*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment method catalogue\t8 list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment method catalogue\t8 untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment method catalogue\t8 yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment method catalogue\t8 are still there. The pack's own statuses are Draft — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPaymentMethods` → `PAYMENT_VIEW` (read) · staff
- `createPaymentMethod` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-560` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-560`
- Workshop pack: Payment_Payment_Orchestration.pdf board 1
- Flow F256 *Payment Payment Orchestration board 1: Payment Command Center\t7*, step 2: Works in Payment Method Catalogue\t8 → Maintain the centralized catalogue of payment/tender types supported by TICVAI.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-560?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-559`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`, `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-561` Payment Method Configuration\t9

**Configure detailed behavior for each payment method.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§General Configuration; Configure whether the method allows) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `methodId` (navigation) |
| Route | `/commercial/payment-method-configuration-t9-adm-561` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Payment method name | select field | — | — | — | — | — | — |
| Internal code | select field | — | — | — | — | — | — |
| Customer-facing label | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Icon | select field | — | — | — | — | — | — |
| Tender category | select field | — | — | — | — | — | — |
| Provider | select field | — | — | — | — | — | — |
| Effective dates | select field | — | — | — | — | — | — |
| Sale | select field | — | — | — | — | — | — |
| Refund | select field | — | — | — | — | — | — |
| Partial refund | select field | — | — | — | — | — | — |
| Void | select field | — | — | — | — | — | — |
| Reversal | select field | — | — | — | — | — | — |
| Recurring payment | select field | — | — | — | — | — | — |
| Preauthorization where supported | select field | — | — | — | — | — | — |
| Capture where supported | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-559` Payment Command Center\t7: *Back to Payment Command Center\t7*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment method \t9 configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment method \t9 untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment method \t9 configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `updatePaymentMethod` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-561` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-561`
- Workshop pack: Payment_Payment_Orchestration.pdf board 1
- Flow F256 *Payment Payment Orchestration board 1: Payment Command Center\t7*, step 4: Works in Payment Method Configuration\t9 → Configure detailed behavior for each payment method.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-561?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-559`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-562` Channel & Touchpoint Payment Configuration\t10

**Control which payment methods are available on each sales channel.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `methodId` (navigation) |
| Route | `/commercial/channel-touchpoint-payment-configuration-t10-adm-562` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save payment method (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-559` Payment Command Center\t7: *Back to Payment Command Center\t7*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel touchpoint payment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel touchpoint payment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel touchpoint payment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the channel touchpoint payment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `updatePaymentMethod` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-562` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-562`
- Workshop pack: Payment_Payment_Orchestration.pdf board 1
- Flow F256 *Payment Payment Orchestration board 1: Payment Command Center\t7*, step 6: Works in Channel & Touchpoint Payment Configuration\t10 → Control which payment methods are available on each sales channel.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-562?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save payment method, Cancel.
- [ ] Every transition is wired: `ADM-559`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-563` Venue, Location & Business Unit Payment Assignment\t11

**Allow different venues and business units to operate different payment configurations. This is important for TICVAI's multi-venue architecture.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Business Area Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `methodId` (navigation) |
| Route | `/commercial/venue-location-business-unit-payment-assignment-t11-adm-563` |

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Digital Wallet, Gift Card, Card. Each needs an operation, or needs removing from the screen; this is the …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Ticketing | select field | — | — | — | — | — | — |
| F&B | select field | — | — | — | — | — | — |
| Retail | select field | — | — | — | — | — | — |
| Rental | select field | — | — | — | — | — | — |
| Membership | select field | — | — | — | — | — | — |
| Parking | select field | — | — | — | — | — | — |
| Other TICVAI modules | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Digital Wallet (primary button) | navigation or local | — | — | — | — |
| Gift Card (secondary button) | navigation or local | — | — | — | — |
| Card (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-559` Payment Command Center\t7: *Back to Payment Command Center\t7*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue location business configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue location business untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue location business configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `updatePaymentMethod` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-563` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-563`
- Workshop pack: Payment_Payment_Orchestration.pdf board 1
- Flow F256 *Payment Payment Orchestration board 1: Payment Command Center\t7*, step 8: Works in Venue, Location & Business Unit Payment Assignment\t11 → Allow different venues and business units to operate different payment configurations. This is important for TICVAI's multi-venue architecture.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-563?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Digital Wallet, Gift Card, Card.
- [ ] Every transition is wired: `ADM-559`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-564` Currency & Payment Currency Configuration\t12

**Define which currencies can be used for payment and how payment currencies interact with TICVAI's selling and accounting currencies.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `methodId` (navigation) |
| Route | `/commercial/currency-payment-currency-configuration-t12-adm-564` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Accepted currencies by channel | text field | — | — | — | — | — | — |
| Accepted currencies by payment method | text field | — | — | — | — | — | — |
| Venue restrictions | select field | — | — | — | — | — | — |
| Gateway compatibility | select field | — | — | — | — | — | — |
| Currency conversion requirement | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-559` Payment Command Center\t7: *Back to Payment Command Center\t7*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The currency payment currency configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the currency payment currency untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No currency payment currency configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `updatePaymentMethod` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A43** Design multi-currency display to support both manual FX-rate entry (with configurable margin) and an optional real-time third-party FX-rate API; confirm which payment gateway(s) support Dynamic Currency Conversion (DCC) *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'multi-currency')*
- **A44** Add a foreign-currency collection report (transactions collected broken down by foreign currency) to the Finance reporting suite *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'foreign currency')*
- **C23** Confirm foreign-currency display approach (manual FX-rate entry with margin vs. live third-party FX-rate API) and confirm the payment gateway that will support Dynamic Currency Conversion *(Qossai / Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'fx-rate')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'multi-currency')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-564` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-564`
- Workshop pack: Payment_Payment_Orchestration.pdf board 1
- Flow F256 *Payment Payment Orchestration board 1: Payment Command Center\t7*, step 10: Works in Currency & Payment Currency Configuration\t12 → Define which currencies can be used for payment and how payment currencies interact with TICVAI's selling and accounting currencies.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-564?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-559`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-565` Payment Eligibility & Availability Rule Builder\t13

**Determine whether a payment method should be available for a particular transaction.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `methodId` (navigation) |
| Route | `/commercial/payment-eligibility-availability-rule-builder-t13-adm-565` |

**Known gaps.** **The pack names 9 actions on this screen and the screen declares 0 operations.** Unserved: Channel, Venue, Product, Product category, Transaction amount, Customer type, Membership, Country/market … **Payment Eligibility & Availability Rule Builder\t13 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Channel (primary button) | navigation or local | — | — | — | — |
| Venue (secondary button) | navigation or local | — | — | — | — |
| Product (secondary button) | navigation or local | — | — | — | — |
| Product category (secondary button) | navigation or local | — | — | — | — |
| Transaction amount (secondary button) | navigation or local | — | — | — | — |
| Customer type (secondary button) | navigation or local | — | — | — | — |
| Membership (secondary button) | navigation or local | — | — | — | — |
| Country/market where applicable (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-559` Payment Command Center\t7: *Back to Payment Command Center\t7*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment eligibility availability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment eligibility availability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment eligibility availability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment eligibility availability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `updatePaymentMethod` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-565` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-565`
- Workshop pack: Payment_Payment_Orchestration.pdf board 1
- Flow F256 *Payment Payment Orchestration board 1: Payment Command Center\t7*, step 12: Works in Payment Eligibility & Availability Rule Builder\t13 → Determine whether a payment method should be available for a particular transaction.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-565?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Channel, Venue, Product, Product category, Transaction amount, Customer type, Membership, Country/market where applicable.
- [ ] Every transition is wired: `ADM-559`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-566` Payment Fees, Surcharges & Commercial Rules\t14

**Configure payment-related commercial rules where legally and contractually permitted.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `methodId` (navigation) |
| Route | `/commercial/payment-fees-surcharges-commercial-rules-t14-adm-566` |

**Known gaps.** **The pack names 8 actions on this screen and the screen declares 0 operations.** Unserved: Fixed payment fee, Percentage fee, Minimum fee, Maximum fee, Payment-method-specific fee, Channel-specific … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Fixed payment fee (primary button) | navigation or local | — | — | — | — |
| Percentage fee (secondary button) | navigation or local | — | — | — | — |
| Minimum fee (secondary button) | navigation or local | — | — | — | — |
| Maximum fee (secondary button) | navigation or local | — | — | — | — |
| Payment-method-specific fee (secondary button) | navigation or local | — | — | — | — |
| Channel-specific fee (secondary button) | navigation or local | — | — | — | — |
| Currency-specific fee (secondary button) | navigation or local | — | — | — | — |
| Waiver rule (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-559` Payment Command Center\t7: *Back to Payment Command Center\t7*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment fees surcharges list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment fees surcharges untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment fees surcharges yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment fees surcharges are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `updatePaymentMethod` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-566` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-566`
- Workshop pack: Payment_Payment_Orchestration.pdf board 1
- Flow F256 *Payment Payment Orchestration board 1: Payment Command Center\t7*, step 14: Works in Payment Fees, Surcharges & Commercial Rules\t14 → Configure payment-related commercial rules where legally and contractually permitted.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-566?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Fixed payment fee, Percentage fee, Minimum fee, Maximum fee, Payment-method-specific fee, Channel-specific fee, Currency-specific fee, Waiver rule.
- [ ] Every transition is wired: `ADM-559`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-567` Payment Policy, Governance & Approval Manager\t15

**Provide governance over sensitive payment configuration changes.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_REQUEST`, `PAYMENT_CONFIGURE`, `PAYMENT_VIEW` (1 operate, 1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/payment-policy-governance-approval-manager-t15-adm-567` |

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Effective from, Scheduled expiry. Each needs an operation, or needs removing from the screen; this is the … **Payment Policy, Governance & Approval Manager\t15 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Changed by | select field | — | — | — | — | — | — |
| Date/time | select field | — | — | — | — | — | — |
| Old value | select field | — | — | — | — | — | — |
| New value | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |
| Approval | select field | — | — | — | — | — | — |
| Effective date | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | text field | — | — | `listPaymentMethods` ?channel |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Effective from (primary button) | navigation or local | — | — | — | — |
| Scheduled expiry (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listPaymentMethods` (onLoad, What is being changed); `getPaymentRules` (onLoad, The rules currently in force)

**Where the user goes next**

- → `ADM-559` Payment Command Center\t7: *Back to Payment Command Center\t7*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment policy governance configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment policy governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment policy governance configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 An open request already exists for this subject. Two approvals for one refund is how a refund gets paid twice. (ApprovalStateProblem) |

#### Permissions

- `createApprovalRequest` → `APPROVAL_REQUEST` (operate) · staff
- `listPaymentMethods` → `PAYMENT_VIEW` (read) · staff
- `getPaymentRules` → `PAYMENT_VIEW` (read) · staff
- `setPaymentRules` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.59 | Complimentary entitlement redemption | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 1.2.64 | Employees shall submit requests from mobile app. | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 1.2.65 | Managers shall approve requests from mobile app. | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 11.1.51 | Draft Approval Requests - System shall support saving approval requests in draft status. | Approval Workflows & Governance | CONTRACTED | `createApprovalRequest` |
| 11.1.63 | API-Based Approval Processing - System shall expose approval workflows through APIs. | Approval Workflows & Governance | CONTRACTED | `createApprovalRequest` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-567` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-567`
- Workshop pack: Payment_Payment_Orchestration.pdf board 1
- Flow F256 *Payment Payment Orchestration board 1: Payment Command Center\t7*, step 16: Works in Payment Policy, Governance & Approval Manager\t15 → Provide governance over sensitive payment configuration changes.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (409, 412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-567?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Effective from, Scheduled expiry.
- [ ] Every transition is wired: `ADM-559`.
- [ ] Every gated control is gated: `APPROVAL_REQUEST`, `PAYMENT_CONFIGURE`, `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-568` Payment Configuration Simulator & Validation Center\t16

**Allow administrators to test payment configuration before publishing it. This is especially important because payment configuration errors can immediately stop sales.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Credit Card) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/payment-configuration-simulator-validation-center-t16-adm-568` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every payment simulator validation** (data table)

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |
| Gateway a — primary | text | not in the schema: `Gateway A — Primary` |
| Gateway b — secondary | text | not in the schema: `Gateway B — Secondary` |
| Gateway c — regional | text | not in the schema: `Gateway C — Regional` |

**The selected payment simulator validation** (detail panel): The pack groups this record's detail under its own headings: “Venue”, “Channel”, “B2C”, “Customer”, “Available payment methods”, “Unavailable”.

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |
| Gateway a — primary | text | not in the schema: `Gateway A — Primary` |
| Gateway b — secondary | text | not in the schema: `Gateway B — Secondary` |
| Gateway c — regional | text | not in the schema: `Gateway C — Regional` |

**Where the user goes next**

- → `ADM-559` Payment Command Center\t7: *Back to Payment Command Center\t7*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment simulator validation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment simulator validation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment simulator validation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment simulator validation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `simulatePaymentConfiguration` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-568` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS87 Payment Payment Orchestration Board 1.dc.html#adm-568`
- Workshop pack: Payment_Payment_Orchestration.pdf board 1
- Flow F256 *Payment Payment Orchestration board 1: Payment Command Center\t7*, step 18: Works in Payment Configuration Simulator & Validation Center\t16 → Allow administrators to test payment configuration before publishing it. This is especially important because payment configuration errors can immediately stop sales.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-568?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-559`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
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
"createApprovalRequest": {"method":"POST","path":"/approval-requests","contract":"approvals","summary":"Raise a request","permission":"APPROVAL_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateApprovalRequest","responds":"ApprovalRequest"},
"createPaymentMethod": {"method":"POST","path":"/payment-methods","contract":"payments","summary":"Add a payment method to the catalogue","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PaymentMethod","responds":"PaymentMethod"},
"getPaymentPerformance": {"method":"GET","path":"/payment-performance","contract":"payments","summary":"Authorisation rate, conversion and where payments are lost","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"PaymentPerformanceRow"},
"getPaymentRules": {"method":"GET","path":"/payments/rules","contract":"payments","summary":"Currency, eligibility and fee rules as one set","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PaymentRuleSet"},
"listPaymentMethods": {"method":"GET","path":"/payment-methods","contract":"payments","summary":"The methods this tenant can offer, and where","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"venueId","in":"query","required":null},{"name":"channel","in":"query","required":null}],"requestBody":null,"responds":"PaymentMethod"},
"setPaymentRules": {"method":"PUT","path":"/payments/rules","contract":"payments","summary":"Replace the payment rule set","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"PaymentRuleSet","responds":"PaymentRuleSet"},
"simulatePaymentConfiguration": {"method":"POST","path":"/payment-configuration/simulate","contract":"payments","summary":"What a guest would be offered, and what it would cost","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RoutingContext","responds":"PaymentConfigurationSimulation"},
"updatePaymentMethod": {"method":"PUT","path":"/payment-methods/{methodId}","contract":"payments","summary":"Change availability, fees and eligibility","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"PaymentMethod","responds":"PaymentMethod"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"CreateApprovalRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","kind","subjectContract","subjectType","subjectId","scopePath","summary"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"subjectContract":{"type":"string","description":"Which contract owns the thing being approved."},"subjectType":{"type":"string"},"subjectId":{"type":"string","description":"**A reference, never a copy.** A copy goes stale between raising and deciding, and an approver reading a stale copy approves something that no longer exists.\n"},"scopePath":{"type":"string"},"summary":{"type":"string","maxLength":300,"description":"What the approver sees in their queue before opening it."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"attributes":{"type":"object","additionalProperties":true},"justification":{"type":"string","maxLength":1000},"isDraft":{"type":"boolean","default":false,"description":"True saves the request at `draft` without routing it; `submitApprovalRequest` sends it later (decided 28 September, audit R129).\n"}}},
"PaymentConfigurationSimulation": {"type":"object","description":"Boards 1.10 and 5.10. **Eight boards of configuration that compose, silently.**","properties":{"offeredMethods":{"type":"array","items":{"type":"object","properties":{"methodId":{"type":"string","format":"uuid"},"name":{"type":"string"},"routesTo":{"type":"string","nullable":true},"estimatedCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"surcharge":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"suppressedMethods":{"type":"array","items":{"type":"object","properties":{"methodId":{"type":"string","format":"uuid"},"reason":{"type":"string"}}}},"findings":{"type":"array","items":{"type":"object","properties":{"severity":{"type":"string","enum":["blocking","warning"]},"message":{"type":"string"}}}}}},
"PaymentMethod": {"type":"object","x-ticvai-persistence":"payments.method","description":"Board 1.2. **A method is not a provider.**","required":["code","name","kind"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"type":"string","enum":["card","digitalWallet","bankTransfer","cash","storedValue","giftCard","voucher","onAccount","buyNowPayLater","paymentLink"]},"cardSchemes":{"type":"array","items":{"type":"string"}},"currencies":{"type":"array","items":{"type":"string"}},"channels":{"type":"array","items":{"type":"string"}},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"minimumAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maximumAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"surcharge":{"type":"object","nullable":true,"properties":{"percent":{"type":"number","nullable":true},"fixed":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"disclosedToGuest":{"type":"boolean","default":true,"description":"**Undisclosed surcharging is illegal in several of the markets this platform sells into.** The flag exists so the answer is a configuration somebody chose rather than a template nobody read.\n"}}},"refundable":{"type":"boolean","default":true},"partialRefundSupported":{"type":"boolean","default":true},"displayOrder":{"type":"integer","default":0},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"PaymentPerformanceRow": {"type":"object","description":"Board 8.8. **The last and most expensive place a venue loses a sale.**","properties":{"key":{"type":"string"},"label":{"type":"string"},"attempts":{"type":"integer"},"authorised":{"type":"integer"},"declined":{"type":"integer"},"errored":{"type":"integer"},"abandoned":{"type":"integer"},"authorisationRate":{"type":"number"},"conversionRate":{"type":"number"},"averageValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"topDeclineReason":{"type":"string","nullable":true}}},
"PaymentRuleSet": {"type":"object","x-ticvai-persistence":"none — composed from the three payment rule tables","description":"**Three tables, one decision.** Whether a guest may pay with this method, in this currency, and what it costs the venue are evaluated together at checkout. An administrator changing one without seeing the others is how a method becomes eligible in a currency it cannot settle.\n","properties":{"currencyRules":{"type":"array","items":{"$ref":"#/components/schemas/PaymentsCurrencyRule"}},"eligibilityRules":{"type":"array","items":{"$ref":"#/components/schemas/PaymentsEligibilityRule"}},"feeRules":{"type":"array","items":{"$ref":"#/components/schemas/PaymentsFeeRule"}}}},
"PaymentsCurrencyRule": {"type":"object","x-ticvai-persistence":"payments.currency_rule","description":"**Taken from the backend workbook, 20 September.** NEW TABLE. Defines payment-level currency rules such as accepted/settlement currency, min/max payment amount and rounding.","required":["paymentPolicyId","code","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"paymentPolicyId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","nullable":true},"channelId":{"type":"string","format":"uuid","nullable":true},"code":{"type":"string","maxLength":10},"settlementCurrencyCode":{"type":"string","maxLength":10,"nullable":true},"minPaymentAmount":{"type":"number","nullable":true},"maxPaymentAmount":{"type":"number","nullable":true},"roundingIncrement":{"type":"number","nullable":true},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time","nullable":true}}},
"PaymentsEligibilityRule": {"type":"object","x-ticvai-persistence":"payments.eligibility_rule","description":"**Taken from the backend workbook, 20 September.** NEW TABLE. Defines when a payment method is allowed or denied for a transaction.","required":["paymentPolicyId","paymentMethodId","effect","priority","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"paymentPolicyId":{"type":"string","format":"uuid"},"paymentMethodId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","nullable":true},"channelId":{"type":"string","format":"uuid","nullable":true},"businessArea":{"type":"string","maxLength":30,"nullable":true},"currencyCode":{"type":"string","maxLength":10,"nullable":true},"minOrderAmount":{"type":"number","nullable":true},"maxOrderAmount":{"type":"number","nullable":true},"effect":{"type":"string","maxLength":10},"priority":{"type":"integer"},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time","nullable":true}}},
"PaymentsFeeRule": {"type":"object","x-ticvai-persistence":"payments.fee_rule","description":"**Taken from the backend workbook, 20 September.** NEW TABLE. Defines payment-related fees or surcharges that may be applied to an order.","required":["paymentPolicyId","name","category","calculationType","value","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"paymentPolicyId":{"type":"string","format":"uuid"},"paymentMethodId":{"type":"string","format":"uuid","nullable":true},"providerId":{"type":"string","format":"uuid","nullable":true},"channelId":{"type":"string","format":"uuid","nullable":true},"businessArea":{"type":"string","maxLength":30,"nullable":true},"currencyCode":{"type":"string","maxLength":10,"nullable":true},"name":{"type":"string","maxLength":150},"category":{"type":"string","maxLength":20},"calculationType":{"type":"string","maxLength":20},"value":{"type":"number"},"minFee":{"type":"number","nullable":true},"maxFee":{"type":"number","nullable":true},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time","nullable":true}}},
"RoutingContext": {"type":"object","required":["amount"],"properties":{"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"methodId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"channel":{"type":"string","nullable":true},"cardScheme":{"type":"string","nullable":true},"cardIssuerCountry":{"type":"string","nullable":true},"cardPresent":{"type":"boolean","default":false},"customerId":{"type":"string","format":"uuid","nullable":true}}}
}
```
