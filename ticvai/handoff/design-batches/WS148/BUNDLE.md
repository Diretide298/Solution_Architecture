# WS148 — Payment Payment Orchestration board 2

**10 screens · 9 operations · 8 schemas · 3 permissions**

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
  `PAYMENT_CONFIGURE, PAYMENT_PROVIDER_MANAGE, PAYMENT_VIEW`. A control nobody can use must say so,
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
| `ADM-569` | Payment Orchestration Command Center\t27 | B–D | 0 | 10 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-570` | Gateway, PSP & Acquirer Directory\t28 | A | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-571` | Provider Connection & Adapter Configuration\t29 | B–D | 0 | 22 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-572` | Gateway Capability & Payment Method Mapping\t30 | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-573` | Payment Routing Rule Builder\t31 | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-574` | Routing Strategy, Priority & Load Distribution\t33 | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-575` | Failover, Retry & Resilience Manager\t34 | B–D | 8 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-576` | Provider Health, SLA & Performance Monitor\t35 | B–D | 0 | 10 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-577` | Provider Cost, Commercial & Routing Economics\t36 | B–D | 5 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-578` | Payment Routing Simulator, Decision Trace & AI Advisor\t37 | B–D | 0 | 6 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-570, ADM-572, ADM-574, ADM-578 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-569` Payment Orchestration Command Center\t27

**Provide real-time operational visibility across all payment gateways, PSPs and acquirers.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Display) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/payment-orchestration-command-center-t27-adm-569` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getPaymentProviderHealth` ?from |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Payment Attempts** (metric tile)

**Successful Authorizations** (metric tile)

**Authorization Rate** (metric tile)

**Successful Captures** (metric tile)

**Declined Transactions** (metric tile)

**Technical Failures** (metric tile)

**Routed Transactions** (metric tile)

**Rerouted Transactions** (metric tile)

**Failover Transactions** (metric tile)

**Active Providers** (metric tile)

**Provider Incidents** (metric tile)

**Average Processing Time** (metric tile)

**Every payment orchestration \t27** (data table)

| Shows | Format | Notes |
|---|---|---|
| Attempted value | text | not in the schema: `Attempted Value` |
| Authorized value | text | not in the schema: `Authorized Value` |
| Captured value | text | not in the schema: `Captured Value` |
| Failed value | text | not in the schema: `Failed Value` |
| Rerouted value | text | not in the schema: `Rerouted Value` |

**The selected payment orchestration \t27** (detail panel): The pack groups this record's detail under its own headings: “Provider Value Success Status”, “Provider AED”, “Provider AED Warnin”.

| Shows | Format | Notes |
|---|---|---|
| Attempted value | text | not in the schema: `Attempted Value` |
| Authorized value | text | not in the schema: `Authorized Value` |
| Captured value | text | not in the schema: `Captured Value` |
| Failed value | text | not in the schema: `Failed Value` |
| Rerouted value | text | not in the schema: `Rerouted Value` |

**Data it reads**: `getPaymentProviderHealth` (onLoad, Provider health); `listPaymentProviderConnections` (onLoad, Providers connected)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-570` Gateway, PSP & Acquirer Directory\t28: *Gateway, PSP & Acquirer Directory\t28*
- → `ADM-571` Provider Connection & Adapter Configuration\t29: *Provider Connection & Adapter Configuration\t29*; carries `connectionId`
- → `ADM-572` Gateway Capability & Payment Method Mapping\t30: *Gateway Capability & Payment Method Mapping\t30*
- → `ADM-573` Payment Routing Rule Builder\t31: *Payment Routing Rule Builder\t31*
- → `ADM-574` Routing Strategy, Priority & Load Distribution\t33: *Routing Strategy, Priority & Load Distribution\t33*
- → `ADM-575` Failover, Retry & Resilience Manager\t34: *Failover, Retry & Resilience Manager\t34*
- → `ADM-576` Provider Health, SLA & Performance Monitor\t35: *Provider Health, SLA & Performance Monitor\t35*
- → `ADM-577` Provider Cost, Commercial & Routing Economics\t36: *Provider Cost, Commercial & Routing Economics\t36*
- → `ADM-578` Payment Routing Simulator, Decision Trace & AI Advisor\t37: *Payment Routing Simulator, Decision Trace & AI Advisor\t37*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment orchestration \t27 list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment orchestration \t27 untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment orchestration \t27 yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment orchestration \t27 are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getPaymentProviderHealth` → `PAYMENT_VIEW` (read) · staff
- `listPaymentProviderConnections` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-569` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-569`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 1: Opens Payment Orchestration Command Center\t27 → Provide real-time operational visibility across all payment gateways, PSPs and acquirers.
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F257 branch at step 1 (expected): when Nothing has been set up on Payment Orchestration Command Center\t27 yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F257 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-569?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-570`, `ADM-571`, `ADM-572`, `ADM-573`, `ADM-574`, `ADM-575`, `ADM-576`, `ADM-577`, `ADM-578`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-570` Gateway, PSP & Acquirer Directory\t28

**Maintain the centralized directory of payment-processing providers connected to TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block A · ticket #20685 (APP-SETUP-ADM-570) |
| Who uses it | ticvai staff holding `PAYMENT_PROVIDER_MANAGE`, `PAYMENT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/gateway-psp-acquirer-directory-t28-adm-570` |

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Payment Gateway, Wallet Provider, Alternative Payment Provider. Each needs an operation, or needs removing … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Payment Gateway (primary button) | navigation or local | — | — | — | — |
| Wallet Provider (secondary button) | navigation or local | — | — | — | — |
| Alternative Payment Provider (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listPaymentProviderConnections` (onLoad, The directory)

**Where the user goes next**

- → `ADM-569` Payment Orchestration Command Center\t27: *Back to Payment Orchestration Command Center\t27*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gateway psp acquirer list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gateway psp acquirer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gateway psp acquirer yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the gateway psp acquirer are still there. The pack's own statuses are Draft — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPaymentProviderConnections` → `PAYMENT_VIEW` (read) · staff
- `createPaymentProviderConnection` → `PAYMENT_PROVIDER_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-570` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-570`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 2: Works in Gateway, PSP & Acquirer Directory\t28 → Maintain the centralized directory of payment-processing providers connected to TICVAI.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-570?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Payment Gateway, Wallet Provider, Alternative Payment Provider.
- [ ] Every transition is wired: `ADM-569`.
- [ ] Every gated control is gated: `PAYMENT_PROVIDER_MANAGE`, `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-571` Provider Connection & Adapter Configuration\t29

**Configure how TICVAI technically connects to each payment provider.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_PROVIDER_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | `connectionId` (navigation) |
| Route | `/commercial/provider-connection-adapter-configuration-t29-adm-571` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: API endpoint reference, Webhook configuration, Callback configuration, Retry configuration. Each needs an … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every provider connection adapter** (data table)

| Shows | Format | Notes |
|---|---|---|
| TICVAI adapter | text | not in the schema: `TICVAI Adapter` |
| Adapter version | text | not in the schema: `Adapter Version` |
| Provider API version | text | not in the schema: `Provider API Version` |
| Deployment version | text | not in the schema: `Deployment Version` |
| Last certification/test | text | not in the schema: `Last Certification/Test` |
| Status | text | not in the schema: `Status` |
| Credential status | text | not in the schema: `Credential status` |
| Last rotation | text | not in the schema: `Last rotation` |
| Expiry | text | not in the schema: `Expiry` |
| Certificate expiry | text | not in the schema: `Certificate expiry` |
| Owner | text | not in the schema: `Owner` |

**The selected provider connection adapter** (detail panel): The pack groups this record's detail under its own headings: “Credential Management”, “Never expose full”, “Result”.

| Shows | Format | Notes |
|---|---|---|
| TICVAI adapter | text | not in the schema: `TICVAI Adapter` |
| Adapter version | text | not in the schema: `Adapter Version` |
| Provider API version | text | not in the schema: `Provider API Version` |
| Deployment version | text | not in the schema: `Deployment Version` |
| Last certification/test | text | not in the schema: `Last Certification/Test` |
| Status | text | not in the schema: `Status` |
| Credential status | text | not in the schema: `Credential status` |
| Last rotation | text | not in the schema: `Last rotation` |
| Expiry | text | not in the schema: `Expiry` |
| Certificate expiry | text | not in the schema: `Certificate expiry` |
| Owner | text | not in the schema: `Owner` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| API endpoint reference (primary button) | navigation or local | — | — | — | — |
| Webhook configuration (secondary button) | navigation or local | — | — | — | — |
| Callback configuration (secondary button) | navigation or local | — | — | — | — |
| Retry configuration (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-569` Payment Orchestration Command Center\t27: *Back to Payment Orchestration Command Center\t27*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The provider connection adapter list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the provider connection adapter untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No provider connection adapter yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the provider connection adapter are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `createPaymentProviderConnection` → `PAYMENT_PROVIDER_MANAGE` (configure) · staff
- `testPaymentProviderConnection` → `PAYMENT_PROVIDER_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-571` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-571`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 4: Works in Provider Connection & Adapter Configuration\t29 → Configure how TICVAI technically connects to each payment provider.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-571?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: API endpoint reference, Webhook configuration, Callback configuration, Retry configuration.
- [ ] Every transition is wired: `ADM-569`.
- [ ] Every gated control is gated: `PAYMENT_PROVIDER_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-572` Gateway Capability & Payment Method Mapping\t30

**Map Board 1 payment methods to providers capable of processing them.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/gateway-capability-payment-method-mapping-t30-adm-572` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listPaymentProviderConnections` (onLoad, Capability against method)

**Where the user goes next**

- → `ADM-569` Payment Orchestration Command Center\t27: *Back to Payment Orchestration Command Center\t27*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gateway capability payment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gateway capability payment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gateway capability payment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the gateway capability payment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPaymentProviderConnections` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-572` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-572`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 6: Works in Gateway Capability & Payment Method Mapping\t30 → Map Board 1 payment methods to providers capable of processing them.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-572?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-569`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-573` Payment Routing Rule Builder\t31

**Configure the rules that determine which provider should receive each payment transaction.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE`, `PAYMENT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/payment-routing-rule-builder-t31-adm-573` |

**Known gaps.** **The pack names 8 actions on this screen and the screen declares 0 operations.** Unserved: Venue, Legal entity, Channel, Payment method, Transaction amount, Transaction type, Customer type where … **Payment Routing Rule Builder\t31 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Venue (primary button) | navigation or local | — | — | — | — |
| Legal entity (secondary button) | navigation or local | — | — | — | — |
| Channel (secondary button) | navigation or local | — | — | — | — |
| Payment method (secondary button) | navigation or local | — | — | — | — |
| Transaction amount (secondary button) | navigation or local | — | — | — | — |
| Transaction type (secondary button) | navigation or local | — | — | — | — |
| Customer type where appropriate (secondary button) | navigation or local | — | — | — | — |
| Weighted distribution (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listPaymentRoutingRules` (onLoad, Rules in force)

**Where the user goes next**

- → `ADM-569` Payment Orchestration Command Center\t27: *Back to Payment Orchestration Command Center\t27*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment routing rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment routing rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment routing rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment routing rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A rule routes to a provider that cannot take it |

#### Permissions

- `setPaymentRoutingRules` → `PAYMENT_CONFIGURE` (configure) · staff
- `listPaymentRoutingRules` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-573` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-573`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 8: Works in Payment Routing Rule Builder\t31 → Configure the rules that determine which provider should receive each payment transaction.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409, 412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-573?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Venue, Legal entity, Channel, Payment method, Transaction amount, Transaction type, Customer type where appropriate, Weighted distribution.
- [ ] Every transition is wired: `ADM-569`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`, `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-574` Routing Strategy, Priority & Load Distribution\t33

**Manage how payment traffic is distributed when several valid providers are available.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§AED Card / B2C) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/routing-strategy-priority-load-distribution-t33-adm-574` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Provider A: 60%** (metric tile)

**Provider B: 30%** (metric tile)

**Provider C: 10%** (metric tile)

**Where the user goes next**

- → `ADM-569` Payment Orchestration Command Center\t27: *Back to Payment Orchestration Command Center\t27*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The routing strategy priority list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the routing strategy priority untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No routing strategy priority yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the routing strategy priority are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A rule routes to a provider that cannot take it |

#### Permissions

- `setPaymentRoutingRules` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-574` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-574`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 10: Works in Routing Strategy, Priority & Load Distribution\t33 → Manage how payment traffic is distributed when several valid providers are available.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409, 412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-574?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-569`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-575` Failover, Retry & Resilience Manager\t34

**Maintain payment availability when a provider experiences a technical problem. This is one of the most important screens in the Payment Orchestration module.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/failover-retry-resilience-manager-t34-adm-575` |

**Known gaps.** **Failover, Retry & Resilience Manager\t34 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Primary provider | select field | — | — | — | — | — | — |
| Secondary provider | select field | — | — | — | — | — | — |
| Tertiary provider | select field | — | — | — | — | — | — |
| Trigger condition | select field | — | — | — | — | — | — |
| Retry limit | select field | — | — | — | — | — | — |
| Timeout | select field | — | — | — | — | — | — |
| Cooldown | select field | — | — | — | — | — | — |
| Recovery behavior | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-569` Payment Orchestration Command Center\t27: *Back to Payment Orchestration Command Center\t27*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The failover retry resilience configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the failover retry resilience untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No failover retry resilience configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setPaymentFailoverPolicy` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-575` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-575`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 12: Works in Failover, Retry & Resilience Manager\t34 → Maintain payment availability when a provider experiences a technical problem. This is one of the most important screens in the Payment Orchestration module.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-575?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-569`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-576` Provider Health, SLA & Performance Monitor\t35

**Monitor each provider's technical and transactional health.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Health Metrics) and a per-row directory (§Compare) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/provider-health-sla-performance-monitor-t35-adm-576` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getPaymentProviderHealth` ?from |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Availability** (metric tile)

**Authorization rate** (metric tile)

**Capture rate** (metric tile)

**Decline rate** (metric tile)

**Technical error rate** (metric tile)

**Timeout rate** (metric tile)

**Average latency** (metric tile)

**95th and 99th percentile latency where available** (metric tile)

**Webhook delay** (metric tile)

**Refund API health** (metric tile)

**Every provider health sla** (data table)

| Shows | Format | Notes |
|---|---|---|
| Today | text | not in the schema: `Today` |
| Yesterday | text | not in the schema: `Yesterday` |
| 7 days | text | not in the schema: `7 Days` |
| 30 days | text | not in the schema: `30 Days` |
| Historical baseline | text | not in the schema: `Historical baseline` |

**The selected provider health sla** (detail panel): The pack groups this record's detail under its own headings: “Health State”, “Authorization Rate”, “Normal Baseline”, “Change”.

| Shows | Format | Notes |
|---|---|---|
| Today | text | not in the schema: `Today` |
| Yesterday | text | not in the schema: `Yesterday` |
| 7 days | text | not in the schema: `7 Days` |
| 30 days | text | not in the schema: `30 Days` |
| Historical baseline | text | not in the schema: `Historical baseline` |

**Data it reads**: `getPaymentProviderHealth` (onLoad, Authorisation rate and latency)

**Where the user goes next**

- → `ADM-569` Payment Orchestration Command Center\t27: *Back to Payment Orchestration Command Center\t27*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The provider health sla list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the provider health sla untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No provider health sla yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the provider health sla are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getPaymentProviderHealth` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-576` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-576`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 14: Works in Provider Health, SLA & Performance Monitor\t35 → Monitor each provider's technical and transactional health.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-576?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-569`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-577` Provider Cost, Commercial & Routing Economics\t36

**Allow TICVAI to understand the commercial cost of routing transactions through different providers.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrator may define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/provider-cost-commercial-routing-economics-t36-adm-577` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Maximize Authorization | select field | — | — | — | — | — | — |
| Minimize Cost | select field | — | — | — | — | — | — |
| Minimize Latency | select field | — | — | — | — | — | — |
| Balanced | select field | — | — | — | — | — | — |
| Custom Governed Strategy | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getPaymentProviderEconomics` ?from |
| To | date picker | — | — | `getPaymentProviderEconomics` ?to |

#### Outputs: what the screen shows and produces

**Data it reads**: `getPaymentProviderEconomics` (onLoad, What each provider costs)

**Where the user goes next**

- → `ADM-569` Payment Orchestration Command Center\t27: *Back to Payment Orchestration Command Center\t27*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The provider cost commercial configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the provider cost commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No provider cost commercial configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getPaymentProviderEconomics` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-577` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-577`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 16: Works in Provider Cost, Commercial & Routing Economics\t36 → Allow TICVAI to understand the commercial cost of routing transactions through different providers.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-577?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-569`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-578` Payment Routing Simulator, Decision Trace & AI Advisor\t37

**Allow administrators to test exactly how a payment will be routed before deploying routing changes.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Credit Card can route through) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/payment-routing-simulator-decision-trace-ai-advisor-t37-adm-578` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every payment routing simulator** (data table)

| Shows | Format | Notes |
|---|---|---|
| Provider a | text | not in the schema: `Provider A` |
| Provider b | text | not in the schema: `Provider B` |
| Provider c | text | not in the schema: `Provider C` |

**The selected payment routing simulator** (detail panel): The pack groups this record's detail under its own headings: “AED 720”, “Provider A”, “Provider B”, “Provider C”, “Payment Request”, “Payment Method”.

| Shows | Format | Notes |
|---|---|---|
| Provider a | text | not in the schema: `Provider A` |
| Provider b | text | not in the schema: `Provider B` |
| Provider c | text | not in the schema: `Provider C` |

**Where the user goes next**

- → `ADM-569` Payment Orchestration Command Center\t27: *Back to Payment Orchestration Command Center\t27*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment routing simulator list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment routing simulator untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment routing simulator yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment routing simulator are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `simulatePaymentRouting` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-578` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS88 Payment Payment Orchestration Board 2.dc.html#adm-578`
- Workshop pack: Payment_Payment_Orchestration.pdf board 2
- Flow F257 *Payment Payment Orchestration board 2: Payment Orchestration Command Center\t27*, step 18: Works in Payment Routing Simulator, Decision Trace & AI Advisor\t37 → Allow administrators to test exactly how a payment will be routed before deploying routing changes.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-578?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-569`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`.
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
"createPaymentProviderConnection": {"method":"POST","path":"/payment-providers","contract":"payments","summary":"Connect a provider","permission":"PAYMENT_PROVIDER_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PaymentProviderConnection","responds":"PaymentProviderConnection"},
"getPaymentProviderEconomics": {"method":"GET","path":"/payment-providers/economics","contract":"payments","summary":"What each provider actually costs","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"ProviderEconomics"},
"getPaymentProviderHealth": {"method":"GET","path":"/payment-providers/health","contract":"payments","summary":"Authorisation rate, latency and availability, per provider","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null}],"requestBody":null,"responds":"ProviderHealth"},
"listPaymentProviderConnections": {"method":"GET","path":"/payment-providers","contract":"payments","summary":"Gateways, PSPs and acquirers, and what each can do","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"PaymentProviderConnection"},
"listPaymentRoutingRules": {"method":"GET","path":"/payment-routing-rules","contract":"payments","summary":"Which provider takes which transaction","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"PaymentRoutingRule"},
"setPaymentFailoverPolicy": {"method":"PUT","path":"/payment-failover-policy","contract":"payments","summary":"What happens when a provider fails, and when to stop trying","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"PaymentFailoverPolicy","responds":"PaymentFailoverPolicy"},
"setPaymentRoutingRules": {"method":"PUT","path":"/payment-routing-rules","contract":"payments","summary":"Route by method, currency, venue, amount, cost or share","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PaymentRoutingRule"},
"simulatePaymentRouting": {"method":"POST","path":"/payment-routing/simulate","contract":"payments","summary":"Where would this transaction go, and why","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RoutingContext","responds":"RoutingDecision"},
"testPaymentProviderConnection": {"method":"POST","path":"/payment-providers/{connectionId}/test","contract":"payments","summary":"Prove the connection works before anybody pays through it","permission":"PAYMENT_PROVIDER_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProviderTestResult"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"PaymentFailoverPolicy": {"type":"object","x-ticvai-persistence":"payments.failover_policy","description":"Board 2.7. **A decline is final; a timeout is not. Retrying the first is how a guest gets charged twice.**\n","properties":{"retryableOutcomes":{"type":"array","items":{"type":"string","enum":["timeout","connectionRefused","providerError5xx","rateLimited","issuerUnavailable"]},"description":"**Explicit, rather than \"anything that was not a success\".**"},"maxAttempts":{"type":"integer","default":2},"backoffMs":{"type":"integer","default":500},"failoverToNextProvider":{"type":"boolean","default":true},"circuitBreaker":{"type":"object","description":"**A hundred tills each discovering an outage independently is a hundred queues.**\n","properties":{"failureThresholdPercent":{"type":"number","default":25},"windowSeconds":{"type":"integer","default":60},"minimumSample":{"type":"integer","default":20},"openForSeconds":{"type":"integer","default":300},"alertOnOpen":{"type":"boolean","default":true}}},"scopePath":{"type":"string"}}},
"PaymentProviderConnection": {"type":"object","x-ticvai-persistence":"payments.provider_connection","description":"Boards 2.2 and 2.4. **Capability mapping is the part that gets skipped.**","required":["code","providerKind"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"providerKind":{"type":"string","enum":["gateway","psp","acquirer","walletProvider","bnplProvider"]},"environment":{"type":"string","enum":["sandbox","production"]},"credentialFingerprint":{"type":"string","readOnly":true,"description":"**Written, never read back.** Enough to confirm which key is in use without the key being retrievable from a screen.\n"},"capabilities":{"type":"object","properties":{"methods":{"type":"array","items":{"type":"string"}},"currencies":{"type":"array","items":{"type":"string"}},"partialCapture":{"type":"boolean","default":false},"multipleCapture":{"type":"boolean","default":false},"refundWindowDays":{"type":"integer","nullable":true},"tokenisation":{"type":"boolean","default":false},"threeDSecure":{"type":"boolean","default":false},"cardPresent":{"type":"boolean","default":false}}},"merchantAccountId":{"type":"string","format":"uuid","nullable":true},"status":{"type":"string","enum":["draft","testing","active","degraded","disabled"]},"lastTestedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"PaymentRoutingRule": {"type":"object","x-ticvai-persistence":"payments.routing_rule","description":"Boards 2.5 and 2.6. **Priority and distribution are both needed.**","required":["code"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"priority":{"type":"integer","default":0},"conditions":{"type":"object","properties":{"methodIds":{"type":"array","items":{"type":"string","format":"uuid"}},"currencies":{"type":"array","items":{"type":"string"}},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"channels":{"type":"array","items":{"type":"string"}},"minimumAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maximumAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"cardSchemes":{"type":"array","items":{"type":"string"}},"cardIssuerCountries":{"type":"array","items":{"type":"string"}}}},"targets":{"type":"array","items":{"type":"object","properties":{"connectionId":{"type":"string","format":"uuid"},"sharePercent":{"type":"integer","nullable":true},"rank":{"type":"integer"}}}},"strategy":{"type":"string","enum":["priorityOrder","loadShare","lowestCost","highestAuthRate"],"default":"priorityOrder"},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"ProviderEconomics": {"type":"object","description":"Board 2.9. **Cost per transaction is a routing input.**","properties":{"connectionId":{"type":"string","format":"uuid"},"providerName":{"type":"string"},"transactions":{"type":"integer"},"grossVolume":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"schemeFees":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"interchange":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"acquirerMargin":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"fxSpread":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargebackCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"effectiveRatePercent":{"type":"number"}}},
"ProviderHealth": {"type":"object","description":"Board 2.8. **Authorisation rate is the number, and it is not uptime.**","properties":{"connectionId":{"type":"string","format":"uuid"},"providerName":{"type":"string"},"transactions":{"type":"integer"},"authorisationRate":{"type":"number"},"baselineAuthorisationRate":{"type":"number","nullable":true},"declineRate":{"type":"number"},"errorRate":{"type":"number"},"p50LatencyMs":{"type":"integer"},"p95LatencyMs":{"type":"integer"},"circuitState":{"type":"string","enum":["closed","open","halfOpen"]},"status":{"type":"string","enum":["healthy","degraded","failing","disabled"]}}},
"ProviderTestResult": {"type":"object","description":"Board 3.10. **A provider configured and never tested fails on the first real transaction.**\n","properties":{"connectionId":{"type":"string","format":"uuid"},"testedAt":{"type":"string","format":"date-time"},"checks":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string","enum":["credentials","authorise","capture","refund","void","tokenise","webhook"]},"passed":{"type":"boolean"},"latencyMs":{"type":"integer","nullable":true},"detail":{"type":"string","nullable":true}}}},"overall":{"type":"string","enum":["pass","partial","fail"]}}},
"RoutingContext": {"type":"object","required":["amount"],"properties":{"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"methodId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"channel":{"type":"string","nullable":true},"cardScheme":{"type":"string","nullable":true},"cardIssuerCountry":{"type":"string","nullable":true},"cardPresent":{"type":"boolean","default":false},"customerId":{"type":"string","format":"uuid","nullable":true}}},
"RoutingDecision": {"type":"object","description":"Board 2.10. **Includes the rules that did not match**, because routing that is subtly wrong still succeeds.\n","properties":{"chosenConnectionId":{"type":"string","format":"uuid","nullable":true},"chosenProviderName":{"type":"string","nullable":true},"estimatedCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"trace":{"type":"array","items":{"type":"object","properties":{"ruleCode":{"type":"string"},"matched":{"type":"boolean"},"skippedBecause":{"type":"string","nullable":true},"candidateConnectionId":{"type":"string","format":"uuid","nullable":true}}}},"fallbackChain":{"type":"array","items":{"type":"string","format":"uuid"}}}}
}
```
