# WS150 — Payment Payment Orchestration board 4

**10 screens · 10 operations · 15 schemas · 5 permissions**

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
  `ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, PAYMENT_CONFIGURE, PAYMENT_VIEW`. A control nobody can use must say so,
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
| `ADM-589` | Digital Payments Command Center\t71 | B–D | 0 | 12 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-590` | Digital & Alternative Payment Method Manager\t71 | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-591` | Digital Wallet & Mobile Payment Configuration\t72 | B–D | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `ADM-592` | Payment Link Builder & Configuration\t73 | B–D | 13 | 0 | 6 | 4 | 0 | 0 | — | notStarted (—) |
| `ADM-593` | Payment Link Distribution & Customer Journey Manager\t74 | B–D | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `ADM-594` | Hosted Checkout, Redirect & Return Flow Configuration\t75 | B–D | 10 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `ADM-595` | Digital Payment Session & Transaction Monitor\t76 | B–D | 2 | 24 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-596` | Authentication, Tokenization & Recurring Payment Controls\t78 | B–D | 0 | 18 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-597` | Digital Payment Exception, Recovery & Expiry Center\t79 | B–D | 0 | 10 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-598` | Digital Payment Simulator, Conversion & AI Advisor\t80 | B–D | 13 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-591, ADM-597 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-589` Digital Payments Command Center\t71

**Provide centralized operational visibility across all digital and alternative payment journeys.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Compare) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/digital-payments-command-center-t71-adm-589` |

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

**Digital Payment Attempts** (metric tile)

**Successful Payments** (metric tile)

**Digital Payment Value** (metric tile)

**Success Rate** (metric tile)

**Payment Links Generated** (metric tile)

**Payment Links Paid** (metric tile)

**Payment Link Conversion** (metric tile)

**Wallet Transactions** (metric tile)

**Alternative Payment Transactions** (metric tile)

**Pending Payments** (metric tile)

**Expired Payment Requests** (metric tile)

**Failed Digital Payments** (metric tile)

**Every digital payments \t71** (data table)

| Shows | Format | Notes |
|---|---|---|
| B2 c | text | not in the schema: `B2C` |
| Mobile app | text | not in the schema: `Mobile App` |
| Call center | text | not in the schema: `Call Center` |
| B2 b | text | not in the schema: `B2B` |
| POS payment link | text | not in the schema: `POS Payment Link` |
| Partner/api | text | not in the schema: `Partner/API` |

**The selected digital payments \t71** (detail panel): The pack groups this record's detail under its own headings: “Show by”.

| Shows | Format | Notes |
|---|---|---|
| B2 c | text | not in the schema: `B2C` |
| Mobile app | text | not in the schema: `Mobile App` |
| Call center | text | not in the schema: `Call Center` |
| B2 b | text | not in the schema: `B2B` |
| POS payment link | text | not in the schema: `POS Payment Link` |
| Partner/api | text | not in the schema: `Partner/API` |

**Data it reads**: `getPaymentPerformance` (onLoad, Digital payment performance)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-590` Digital & Alternative Payment Method Manager\t71: *Digital & Alternative Payment Method Manager\t71*
- → `ADM-591` Digital Wallet & Mobile Payment Configuration\t72: *Digital Wallet & Mobile Payment Configuration\t72*
- → `ADM-592` Payment Link Builder & Configuration\t73: *Payment Link Builder & Configuration\t73*
- → `ADM-593` Payment Link Distribution & Customer Journey Manager\t74: *Payment Link Distribution & Customer Journey Manager\t74*
- → `ADM-594` Hosted Checkout, Redirect & Return Flow Configuration\t75: *Hosted Checkout, Redirect & Return Flow Configuration\t75*
- → `ADM-595` Digital Payment Session & Transaction Monitor\t76: *Digital Payment Session & Transaction Monitor\t76*
- → `ADM-596` Authentication, Tokenization & Recurring Payment Controls\t78: *Authentication, Tokenization & Recurring Payment Controls\t78*
- → `ADM-597` Digital Payment Exception, Recovery & Expiry Center\t79: *Digital Payment Exception, Recovery & Expiry Center\t79*
- → `ADM-598` Digital Payment Simulator, Conversion & AI Advisor\t80: *Digital Payment Simulator, Conversion & AI Advisor\t80*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The digital payments \t71 list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the digital payments \t71 untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No digital payments \t71 yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the digital payments \t71 are still there. Names the active filter and offers to clear it. |
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-589` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-589`
- Workshop pack: Payment_Payment_Orchestration.pdf board 4
- Flow F259 *Payment Payment Orchestration board 4: Digital Payments Command Center\t71*, step 1: Opens Digital Payments Command Center\t71 → Provide centralized operational visibility across all digital and alternative payment journeys.
- Flow F259 *Payment Payment Orchestration board 4: Digital Payments Command Center\t71*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F259 *Payment Payment Orchestration board 4: Digital Payments Command Center\t71*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F259 *Payment Payment Orchestration board 4: Digital Payments Command Center\t71*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F259 *Payment Payment Orchestration board 4: Digital Payments Command Center\t71*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F259 *Payment Payment Orchestration board 4: Digital Payments Command Center\t71*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F259 *Payment Payment Orchestration board 4: Digital Payments Command Center\t71*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F259 *Payment Payment Orchestration board 4: Digital Payments Command Center\t71*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F259 branch at step 1 (expected): when Nothing has been set up on Digital Payments Command Center\t71 yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F259 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-589?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-590`, `ADM-591`, `ADM-592`, `ADM-593`, `ADM-594`, `ADM-595`, `ADM-596`, `ADM-597`, `ADM-598`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-590` Digital & Alternative Payment Method Manager\t71

**Configure the digital payment experiences available through TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE`, `PAYMENT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `methodId` (navigation) |
| Route | `/commercial/digital-alternative-payment-method-manager-t71-adm-590` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Online card, Mobile/digital wallets, Redirect payments, Stored-value wallet, Future payment methods through … **Digital & Alternative Payment Method Manager\t71 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | text field | — | — | `listPaymentMethods` ?channel |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Online card (primary button) | navigation or local | — | — | — | — |
| Mobile/digital wallets (secondary button) | navigation or local | — | — | — | — |
| Redirect payments (secondary button) | navigation or local | — | — | — | — |
| Stored-value wallet (secondary button) | navigation or local | — | — | — | — |
| Future payment methods through adapters (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listPaymentMethods` (onLoad, Alternative methods)

**Where the user goes next**

- → `ADM-589` Digital Payments Command Center\t71: *Back to Digital Payments Command Center\t71*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The digital alternative payment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the digital alternative payment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No digital alternative payment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the digital alternative payment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPaymentMethods` → `PAYMENT_VIEW` (read) · staff
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-590` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-590`
- Workshop pack: Payment_Payment_Orchestration.pdf board 4
- Flow F259 *Payment Payment Orchestration board 4: Digital Payments Command Center\t71*, step 2: Works in Digital & Alternative Payment Method Manager\t71 → Configure the digital payment experiences available through TICVAI.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-590?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Online card, Mobile/digital wallets, Redirect payments, Stored-value wallet, Future payment methods through adapters.
- [ ] Every transition is wired: `ADM-589`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`, `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-591` Digital Wallet & Mobile Payment Configuration\t72

**Manage wallet-based and mobile digital payment methods.**

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
| Route | `/commercial/digital-wallet-mobile-payment-configuration-t72-adm-591` |

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

- → `ADM-589` Digital Payments Command Center\t71: *Back to Digital Payments Command Center\t71*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The digital wallet mobile list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the digital wallet mobile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No digital wallet mobile yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the digital wallet mobile are still there. Names the active filter and offers to clear it. |
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

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-591` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-591`
- Workshop pack: Payment_Payment_Orchestration.pdf board 4
- Flow F259 *Payment Payment Orchestration board 4: Digital Payments Command Center\t71*, step 4: Works in Digital Wallet & Mobile Payment Configuration\t72 → Manage wallet-based and mobile digital payment methods.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-591?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save payment method, Cancel.
- [ ] Every transition is wired: `ADM-589`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-592` Payment Link Builder & Configuration\t73

**Allow authorized users and systems to generate secure payment requests without requiring the customer to be physically present at a POS.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_CREATE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/payment-link-builder-configuration-t73-adm-592` |

**Known gaps.** **Payment Link Builder & Configuration\t73 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Order / transaction reference | text field | — | — | — | — | — | — |
| Customer reference | select field | — | — | — | — | — | — |
| Amount | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Payment methods | select field | — | — | — | — | — | — |
| Expiry | select field | — | — | — | — | — | — |
| Partial payment policy | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Return destination | select field | — | — | — | — | — | — |
| Business unit | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Channel/source | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-589` Digital Payments Command Center\t71: *Back to Digital Payments Command Center\t71*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment link \t73 configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment link \t73 untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment link \t73 configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `createPaymentLink` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.38 | The website should allow the customer to do payment for the booking / reservation made in the POS and send payment links sent to the customer. Customer should be able to view the cart and make … | Ticketing Sales | CONTRACTED | `createPaymentLink` |
| 2.8.8 | System shall allow call center agents to create reservations without immediate payment and generate secure payment links that can be sent via email, SMS, WhatsApp, or other supported communication … | Ticketing Sales | CONTRACTED | `createPaymentLink` |
| 2.12.28 | Reservations can be created and the payment links can be sent to the customer. After the succesful payment is done through online B2C portal, customer receives email confirmation | Ticketing Sales | CONTRACTED | `createPaymentLink` |
| 4.2.11 | The system should have the ability to send a payment link to the guest by email, that allows for online payment by the guest to complete a purchase. The validity of the feature should configurable by … | Bundles and Promotions | CONTRACTED | `createPaymentLink` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-592` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-592`
- Workshop pack: Payment_Payment_Orchestration.pdf board 4
- Flow F259 *Payment Payment Orchestration board 4: Digital Payments Command Center\t71*, step 6: Works in Payment Link Builder & Configuration\t73 → Allow authorized users and systems to generate secure payment requests without requiring the customer to be physically present at a POS.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-592?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-589`.
- [ ] Every gated control is gated: `ORDER_CREATE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-593` Payment Link Distribution & Customer Journey Manager\t74

**Manage how a generated payment request is delivered and how its lifecycle progresses.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `linkId` (navigation), `token` (deepLink) |
| Route | `/commercial/payment-link-distribution-customer-journey-manager-t74-adm-593` |

**Known gaps.** **Payment Link Distribution & Customer Journey Manager\t74 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Resend, Change approved delivery channel, Extend expiry, Cancel. Each needs attaching to the control it gates, or the screen needs the control.

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getPaymentLink` (onLoad, Its state)

**Where the user goes next**

- → `ADM-589` Digital Payments Command Center\t71: *Back to Digital Payments Command Center\t71*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment link distribution list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment link distribution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment link distribution yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment link distribution are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `resendPaymentLink` → `ORDER_MODIFY` (operate) · staff
- `getPaymentLink` → `ORDER_VIEW` (read) · guest, anonymous

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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-593` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-593`
- Workshop pack: Payment_Payment_Orchestration.pdf board 4
- Flow F259 *Payment Payment Orchestration board 4: Digital Payments Command Center\t71*, step 8: Works in Payment Link Distribution & Customer Journey Manager\t74 → Manage how a generated payment request is delivered and how its lifecycle progresses.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (410).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-593?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-589`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-594` Hosted Checkout, Redirect & Return Flow Configuration\t75

**Configure digital payment flows that require provider-hosted payment pages, redirects, SDKs, or asynchronous customer journeys.**

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
| Route | `/commercial/hosted-checkout-redirect-return-flow-configuration-t75-adm-594` |

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Hosted checkout, External payment authorization. Each needs an operation, or needs removing from the …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Provider | select field | — | — | — | — | — | — |
| Success return | select field | — | — | — | — | — | — |
| Failure return | select field | — | — | — | — | — | — |
| Cancel return | select field | — | — | — | — | — | — |
| Timeout | select field | — | — | — | — | — | — |
| Session expiry | select field | — | — | — | — | — | — |
| Callback | select field | — | — | — | — | — | — |
| Webhook | select field | — | — | — | — | — | — |
| Allowed domains/apps | select field | — | — | — | — | — | — |
| Branding profile reference | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Hosted checkout (primary button) | navigation or local | — | — | — | — |
| External payment authorization (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-589` Digital Payments Command Center\t71: *Back to Digital Payments Command Center\t71*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The hosted checkout redirect configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the hosted checkout redirect untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No hosted checkout redirect configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setHostedCheckoutConfiguration` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-594` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-594`
- Workshop pack: Payment_Payment_Orchestration.pdf board 4
- Flow F259 *Payment Payment Orchestration board 4: Digital Payments Command Center\t71*, step 10: Works in Hosted Checkout, Redirect & Return Flow Configuration\t75 → Configure digital payment flows that require provider-hosted payment pages, redirects, SDKs, or asynchronous customer journeys.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-594?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Hosted checkout, External payment authorization.
- [ ] Every transition is wired: `ADM-589`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-595` Digital Payment Session & Transaction Monitor\t76

**Provide operational teams with real-time visibility into digital payment sessions.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_CREATE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `paymentId` (navigation) |
| Route | `/commercial/digital-payment-session-transaction-monitor-t76-adm-595` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search digital payment session | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by payment id, order, payment link, customer reference, provider transaction, channel and 5 more — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Shown**

**Every digital payment session** (data table)

| Shows | Format | Notes |
|---|---|---|
| TICVAI payment ID | text | not in the schema: `TICVAI Payment ID` |
| Order ID | text | not in the schema: `Order ID` |
| Payment method | text | not in the schema: `Payment method` |
| Provider | text | not in the schema: `Provider` |
| Gateway | text | not in the schema: `Gateway` |
| Amount | text | not in the schema: `Amount` |
| Currency | text | not in the schema: `Currency` |
| Created | text | not in the schema: `Created` |
| Session expiry | text | not in the schema: `Session expiry` |
| Customer journey stage | text | not in the schema: `Customer journey stage` |
| Provider status | text | not in the schema: `Provider status` |
| TICVAI status | text | not in the schema: `TICVAI status` |

**The selected digital payment session** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| TICVAI payment ID | text | not in the schema: `TICVAI Payment ID` |
| Order ID | text | not in the schema: `Order ID` |
| Payment method | text | not in the schema: `Payment method` |
| Provider | text | not in the schema: `Provider` |
| Gateway | text | not in the schema: `Gateway` |
| Amount | text | not in the schema: `Amount` |
| Currency | text | not in the schema: `Currency` |
| Created | text | not in the schema: `Created` |
| Session expiry | text | not in the schema: `Session expiry` |
| Customer journey stage | text | not in the schema: `Customer journey stage` |
| Provider status | text | not in the schema: `Provider status` |
| TICVAI status | text | not in the schema: `TICVAI status` |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Check Status, Cancel Session, Regenerate Link, View Provider Events, View Decision Trace. Each needs attaching to the control it gates, or the screen needs the control.

**Where the user goes next**

- → `ADM-589` Digital Payments Command Center\t71: *Back to Digital Payments Command Center\t71*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The digital payment session list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the digital payment session untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No digital payment session yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the digital payment session are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `inquirePaymentStatus` → `ORDER_CREATE` (operate) · staff, guest, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-595` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-595`
- Workshop pack: Payment_Payment_Orchestration.pdf board 4
- Flow F259 *Payment Payment Orchestration board 4: Digital Payments Command Center\t71*, step 12: Works in Digital Payment Session & Transaction Monitor\t76 → Provide operational teams with real-time visibility into digital payment sessions.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-595?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-589`.
- [ ] Every gated control is gated: `ORDER_CREATE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-596` Authentication, Tokenization & Recurring Payment Controls\t78

**Manage digital-payment security capabilities and reusable payment references without turning TICVAI into a card vault.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/authentication-tokenization-recurring-payment-controls-t-adm-596` |

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: 3-D Secure, Strong Customer Authentication where applicable, Provider risk authentication. Each needs an … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every authentication tokenization recurring** (data table)

| Shows | Format | Notes |
|---|---|---|
| Payment instrument reference | text | not in the schema: `Payment Instrument Reference` |
| Provider | text | not in the schema: `Provider` |
| Token status | text | not in the schema: `Token Status` |
| Masked identifier where allowed | text | not in the schema: `Masked Identifier where allowed` |
| Card/instrument type | text | not in the schema: `Card/Instrument Type` |
| Expiry metadata where provided | text | not in the schema: `Expiry metadata where provided` |
| Customer/account relationship | text | not in the schema: `Customer/account relationship` |
| Created | text | not in the schema: `Created` |
| Last used | text | not in the schema: `Last Used` |

**The selected authentication tokenization recurring** (detail panel): The pack groups this record's detail under its own headings: “Tokenization”, “Token States”, “Consent / Mandate Reference”.

| Shows | Format | Notes |
|---|---|---|
| Payment instrument reference | text | not in the schema: `Payment Instrument Reference` |
| Provider | text | not in the schema: `Provider` |
| Token status | text | not in the schema: `Token Status` |
| Masked identifier where allowed | text | not in the schema: `Masked Identifier where allowed` |
| Card/instrument type | text | not in the schema: `Card/Instrument Type` |
| Expiry metadata where provided | text | not in the schema: `Expiry metadata where provided` |
| Customer/account relationship | text | not in the schema: `Customer/account relationship` |
| Created | text | not in the schema: `Created` |
| Last used | text | not in the schema: `Last Used` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| 3-D Secure (primary button) | navigation or local | — | — | — | — |
| Strong Customer Authentication where applicable (secondary button) | navigation or local | — | — | — | — |
| Provider risk authentication (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-589` Digital Payments Command Center\t71: *Back to Digital Payments Command Center\t71*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The authentication tokenization recurring list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the authentication tokenization recurring untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No authentication tokenization recurring yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the authentication tokenization recurring are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setPaymentAuthenticationPolicy` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-596` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-596`
- Workshop pack: Payment_Payment_Orchestration.pdf board 4
- Flow F259 *Payment Payment Orchestration board 4: Digital Payments Command Center\t71*, step 14: Works in Authentication, Tokenization & Recurring Payment Controls\t78 → Manage digital-payment security capabilities and reusable payment references without turning TICVAI into a card vault.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-596?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: 3-D Secure, Strong Customer Authentication where …, Provider risk authentication.
- [ ] Every transition is wired: `ADM-589`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-597` Digital Payment Exception, Recovery & Expiry Center\t79

**Centralize operational handling of incomplete or abnormal digital-payment journeys.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_CREATE`, `PAYMENT_CONFIGURE` (1 operate, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `paymentId` (navigation) |
| Route | `/commercial/digital-payment-exception-recovery-expiry-center-t79-adm-597` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every digital payment exception** (data table)

| Shows | Format | Notes |
|---|---|---|
| Age | text | not in the schema: `Age` |
| Severity | text | not in the schema: `Severity` |
| Owner | text | not in the schema: `Owner` |
| Status | text | not in the schema: `Status` |
| Resolution | text | not in the schema: `Resolution` |

**The selected digital payment exception** (detail panel): The pack groups this record's detail under its own headings: “Exception Types”, “Timed Out”, “Depending on condition”.

| Shows | Format | Notes |
|---|---|---|
| Age | text | not in the schema: `Age` |
| Severity | text | not in the schema: `Severity` |
| Owner | text | not in the schema: `Owner` |
| Status | text | not in the schema: `Status` |
| Resolution | text | not in the schema: `Resolution` |

**Where the user goes next**

- → `ADM-589` Digital Payments Command Center\t71: *Back to Digital Payments Command Center\t71*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The digital payment exception list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the digital payment exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No digital payment exception yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the digital payment exception are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setHostedCheckoutConfiguration` → `PAYMENT_CONFIGURE` (configure) · staff
- `inquirePaymentStatus` → `ORDER_CREATE` (operate) · staff, guest, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-597` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-597`
- Workshop pack: Payment_Payment_Orchestration.pdf board 4
- Flow F259 *Payment Payment Orchestration board 4: Digital Payments Command Center\t71*, step 16: Works in Digital Payment Exception, Recovery & Expiry Center\t79 → Centralize operational handling of incomplete or abnormal digital-payment journeys.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 412).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-597?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-589`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-598` Digital Payment Simulator, Conversion & AI Advisor\t80

**Allow administrators to validate digital payment journeys and identify conversion opportunities before deploying configuration changes.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select; Merchant Configuration; Captured) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/digital-payment-simulator-conversion-ai-advisor-t80-adm-598` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Payment method | select field | — | — | — | — | — | — |
| Provider | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Amount | select field | — | — | — | — | — | — |
| Customer type | select field | — | — | — | — | — | — |
| Device context | select field | — | — | — | — | — | — |
| Market | select field | — | — | — | — | — | — |
| Transaction type | select field | — | — | — | — | — | — |
| ✓ | select field | — | — | — | — | — | — |
| ↓ | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-589` Digital Payments Command Center\t71: *Back to Digital Payments Command Center\t71*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The digital payment simulator configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the digital payment simulator untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No digital payment simulator configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-598` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS90 Payment Payment Orchestration Board 4.dc.html#adm-598`
- Workshop pack: Payment_Payment_Orchestration.pdf board 4
- Flow F259 *Payment Payment Orchestration board 4: Digital Payments Command Center\t71*, step 18: Works in Digital Payment Simulator, Conversion & AI Advisor\t80 → Allow administrators to validate digital payment journeys and identify conversion opportunities before deploying configuration changes.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-598?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-589`.
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
"createPaymentLink": {"method":"POST","path":"/payment-links","contract":"orders","summary":"Send a guest a link to pay later","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PaymentLink"},
"getPaymentLink": {"method":"GET","path":"/payment-links/{token}","contract":"orders","summary":"What a guest holding a link is being asked to pay for","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":null},
"getPaymentPerformance": {"method":"GET","path":"/payment-performance","contract":"payments","summary":"Authorisation rate, conversion and where payments are lost","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"PaymentPerformanceRow"},
"inquirePaymentStatus": {"method":"POST","path":"/payments/{paymentId}/inquiry","contract":"orders","summary":"Ask the provider what actually happened","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Payment"},
"listPaymentMethods": {"method":"GET","path":"/payment-methods","contract":"payments","summary":"The methods this tenant can offer, and where","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"venueId","in":"query","required":null},{"name":"channel","in":"query","required":null}],"requestBody":null,"responds":"PaymentMethod"},
"resendPaymentLink": {"method":"POST","path":"/payment-links/{linkId}/resend","contract":"orders","summary":"Send it again, and retire the old one","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PaymentLink"},
"setHostedCheckoutConfiguration": {"method":"PUT","path":"/hosted-checkout-config","contract":"payments","summary":"Redirect, return and the journey back","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"HostedCheckoutConfig","responds":"HostedCheckoutConfig"},
"setPaymentAuthenticationPolicy": {"method":"PUT","path":"/payment-authentication-policy","contract":"payments","summary":"3-D Secure, tokenisation and recurring mandates","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"PaymentAuthenticationPolicy","responds":"PaymentAuthenticationPolicy"},
"simulatePaymentConfiguration": {"method":"POST","path":"/payment-configuration/simulate","contract":"payments","summary":"What a guest would be offered, and what it would cost","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RoutingContext","responds":"PaymentConfigurationSimulation"},
"updatePaymentMethod": {"method":"PUT","path":"/payment-methods/{methodId}","contract":"payments","summary":"Change availability, fees and eligibility","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"PaymentMethod","responds":"PaymentMethod"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CreateOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","variantId","quantity","quotedUnitPrice"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these."},"variantId":{"type":"string","format":"uuid"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Carried from the cart line at checkout; stored on `orders.order_line` and sent in `order.completed` lines.\n"},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"inventoryHoldId":{"type":"string","nullable":true,"description":"Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"},"description":"Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"quantity":{"type":"integer","minimum":1},"eligibilityDeclaration":{"type":"array","nullable":true,"x-ticvai-note":"One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n","items":{"type":"object","properties":{"ageBand":{"type":"string","enum":["infant","child","junior","adult","senior"],"description":"Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."},"ageYears":{"type":"integer","nullable":true},"heightBandIndex":{"type":"integer","nullable":true},"confidentSwimmer":{"type":"boolean","nullable":true,"description":"**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"},"guardianSigned":{"type":"boolean"}}},"description":"What was declared for each guest on this line, kept as the record staff check at the gate."},"quotedUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the client charged, from its local bundle."},"holderName":{"type":"string","nullable":true},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"HostedCheckoutConfig": {"type":"object","x-ticvai-persistence":"payments.hosted_checkout","description":"Board 4.6. **The return leg is where hosted checkout goes wrong.**","properties":{"returnUrl":{"type":"string"},"cancelUrl":{"type":"string"},"webhookUrl":{"type":"string","description":"**The authoritative settle path**, because a guest who closes the tab has still paid.\n"},"webhookSecretFingerprint":{"type":"string","readOnly":true},"sessionTimeoutMinutes":{"type":"integer","default":15},"orphanReconciliationWindowMinutes":{"type":"integer","default":60,"description":"For the ones that fall through both the redirect and the webhook."},"brandingAssetId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderLineDiscount": {"type":"object","description":"One discount applied to one order line (SD-008). Rows of `orders.order_line_discount`.","required":["id","amount","source"],"properties":{"id":{"type":"string","format":"uuid"},"promotionId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"promotions.promotion","description":"The promotion that gave it. Null for a manual discount."},"source":{"type":"string","enum":["promotion","promoCode","manual","bundle","member"]},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reason":{"type":"string","maxLength":200,"nullable":true,"description":"A cashier's reason for a manual discount."}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"PaymentAuthenticationPolicy": {"type":"object","x-ticvai-persistence":"payments.authentication_policy","description":"Board 4.8. **A commercial trade as much as a security one.**","properties":{"threeDSecureMode":{"type":"string","enum":["never","whenRequired","aboveThreshold","always"],"default":"whenRequired"},"threeDSecureThreshold":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"claimedExemptions":{"type":"array","items":{"type":"string","enum":["lowValue","trustedBeneficiary","transactionRiskAnalysis","recurring","merchantInitiated"]}},"tokenisationEnabled":{"type":"boolean","default":false},"tokenRetentionMonths":{"type":"integer","nullable":true},"recurringMandateRequired":{"type":"boolean","default":true,"description":"**A card stored for a renewal without a mandate is a renewal the venue cannot defend.**\n"},"mandateTextAssetId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"PaymentConfigurationSimulation": {"type":"object","description":"Boards 1.10 and 5.10. **Eight boards of configuration that compose, silently.**","properties":{"offeredMethods":{"type":"array","items":{"type":"object","properties":{"methodId":{"type":"string","format":"uuid"},"name":{"type":"string"},"routesTo":{"type":"string","nullable":true},"estimatedCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"surcharge":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"suppressedMethods":{"type":"array","items":{"type":"object","properties":{"methodId":{"type":"string","format":"uuid"},"reason":{"type":"string"}}}},"findings":{"type":"array","items":{"type":"object","properties":{"severity":{"type":"string","enum":["blocking","warning"]},"message":{"type":"string"}}}}}},
"PaymentLink": {"type":"object","x-ticvai-persistence":"orders.payment_link","description":"BL-072. **A booking taken at POS could not be paid later by the guest**, so a phone booking either took a card over the phone or was not taken.\n`createPaymentLink` was contracted on 18 August with no schema behind it and no guest-facing path. **The link existed and nobody could open it** — found on 20 August by walking the journey rather than the contract.\n**The link is the credential.** A guest holding one is anonymous: not signed in, and quite possibly without an account, because a phone booking is exactly the case where they have not registered. The token grants read of one order and payment against it, and nothing else.\n","required":["id","orderId","token","status","expiresAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"orderId":{"type":"string","format":"uuid"},"reservationId":{"type":"string","format":"uuid","nullable":true,"description":"Where the link was issued against a reservation rather than an order. **A reservation holds inventory and carries no money**, which is the whole reason a link is needed.\n"},"token":{"type":"string","format":"password","writeOnly":true,"description":"**Write-only, single purpose, and it is the only thing the guest presents.** Long enough not to be guessed and scoped to one order — **a token that can read a second order is a token that read somebody else's booking.**\n"},"status":{"type":"string","enum":["issued","viewed","paid","expired","cancelled","superseded"]},"channel":{"type":"string","enum":["email","sms","whatsapp","printed"]},"sentTo":{"type":"string","nullable":true,"description":"Masked. **The address it went to is how an operator answers *I never got it*** — and it is personal data, so it is masked here and resolved from `pii` when somebody with permission asks.\n"},"expiresAt":{"type":"string","format":"date-time","description":"**The expiry releases the hold, not just the link.** An unpaid link holding inventory is inventory nobody can sell, and a link that outlives its hold sells a seat twice.\n"},"releaseHoldOnExpiry":{"type":"boolean","default":true},"viewedAt":{"type":"string","format":"date-time","nullable":true},"paidAt":{"type":"string","format":"date-time","nullable":true},"resendCount":{"type":"integer","default":0,"description":"**A resend supersedes rather than duplicates.** Two live links against one order is two guests paying for the same booking, and the second payment is a refund somebody has to make.\n"},"issuedByPrincipalId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"PaymentLinkView": {"type":"object","x-ticvai-persistence":"none — projection of orders.payment_link for its holder","description":"What an anonymous holder of a payment link is shown about the link itself.","required":["status","expiresAt"],"properties":{"status":{"type":"string","enum":["issued","viewed","paid","expired","cancelled","superseded"]},"expiresAt":{"type":"string","format":"date-time"},"releaseHoldOnExpiry":{"type":"boolean"}}},
"PaymentMethod": {"type":"object","x-ticvai-persistence":"payments.method","description":"Board 1.2. **A method is not a provider.**","required":["code","name","kind"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"type":"string","enum":["card","digitalWallet","bankTransfer","cash","storedValue","giftCard","voucher","onAccount","buyNowPayLater","paymentLink"]},"cardSchemes":{"type":"array","items":{"type":"string"}},"currencies":{"type":"array","items":{"type":"string"}},"channels":{"type":"array","items":{"type":"string"}},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"minimumAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maximumAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"surcharge":{"type":"object","nullable":true,"properties":{"percent":{"type":"number","nullable":true},"fixed":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"disclosedToGuest":{"type":"boolean","default":true,"description":"**Undisclosed surcharging is illegal in several of the markets this platform sells into.** The flag exists so the answer is a configuration somebody chose rather than a template nobody read.\n"}}},"refundable":{"type":"boolean","default":true},"partialRefundSupported":{"type":"boolean","default":true},"displayOrder":{"type":"integer","default":0},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"PaymentPerformanceRow": {"type":"object","description":"Board 8.8. **The last and most expensive place a venue loses a sale.**","properties":{"key":{"type":"string"},"label":{"type":"string"},"attempts":{"type":"integer"},"authorised":{"type":"integer"},"declined":{"type":"integer"},"errored":{"type":"integer"},"abandoned":{"type":"integer"},"authorisationRate":{"type":"number"},"conversionRate":{"type":"number"},"averageValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"topDeclineReason":{"type":"string","nullable":true}}},
"RoutingContext": {"type":"object","required":["amount"],"properties":{"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"methodId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"channel":{"type":"string","nullable":true},"cardScheme":{"type":"string","nullable":true},"cardIssuerCountry":{"type":"string","nullable":true},"cardPresent":{"type":"boolean","default":false},"customerId":{"type":"string","format":"uuid","nullable":true}}},
"TenderKind": {"type":"string","description":"`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n","enum":["cash","card","wallet","voucher","bankTransfer","hotelCharge","installment","giftCard","complimentary"]}
}
```
