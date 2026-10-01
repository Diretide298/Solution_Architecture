# P17-purchase-activation-01 — P17 · Purchase & Activation

**7 screens · 2 operations · 4 schemas · 2 permissions**

Platform P17 TICVAI Sign-up · ships as **ticvai-control** ·
public audience · web ·
online only

## Who this is for

**public on web.** Everything below is how you know what is
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
  `ACCOUNT_CONFIGURE, TENANT_CONFIGURE`. A control nobody can use must say so,
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
| `SGN-018` | Purchase / Trial Journey Selection | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `SGN-019` | Contract & Billing Cycle Selection | B–D | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `SGN-020` | Billing & Legal Entity Information | B–D | 0 | 0 | 6 | 8 | 1 | 0 | — | notStarted (—) |
| `SGN-021` | Payment Method & Settlement Setup | B–D | 34 | 0 | 6 | 17 | 1 | 0 | — | notStarted (—) |
| `SGN-022` | Order & Commercial Pricing Review | B–D | 0 | 10 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `SGN-023` | Commercial Agreement, Billable Definition & Customer Acceptance | B–D | 0 | 16 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `SGN-024` | Subscription Confirmation & Commercial Activation | B–D | 0 | 0 | 6 | 2 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**SGN-018, SGN-019, SGN-020, SGN-021, SGN-022, SGN-023, SGN-024 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `SGN-018` Purchase / Trial Journey Selection

**Determine how the customer enters the commercial activation journey.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Purchase & Activation · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | public |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/purchase-activation/purchase-trial-journey-selection-sgn-018` |

**What the spec says about it.** The self-service form of `ADM-409`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save trial configuration (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `SGN-011` Recommended Package Overview: *Back to Recommended Package Overview*
- → `SGN-019` Contract & Billing Cycle Selection: *Contract & Billing Cycle Selection*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The purchase trial journey list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the purchase trial journey untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No purchase trial journey yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the purchase trial journey are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- "Try it" is a single shared, pre-configured demo (sample products, working POS/admin sales flow, reporting) entered with shared credentials - evaluation only, cannot sell real tickets; not a per-prospect trial tenant. *(agreed · MoM 10 Sep 2026, 4.11 Demo Environment Scope · DI-831)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-018` · status **notStarted** · provenance —
- Workshop pack:  board 5

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-018?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save trial configuration, Cancel.
- [ ] Every transition is wired: `SGN-011`, `SGN-019`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-019` Contract & Billing Cycle Selection

**Define the contractual duration and billing/reconciliation cycle.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Purchase & Activation · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | public |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/purchase-activation/contract-billing-cycle-selection-sgn-019` |

**What the spec says about it.** The self-service form of `ADM-410`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Custom Term. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Custom Term (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `SGN-018` Purchase / Trial Journey Selection: *Back to Purchase / Trial Journey Selection*
- → `SGN-020` Billing & Legal Entity Information: *Billing & Legal Entity Information*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The contract billing cycle list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the contract billing cycle untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No contract billing cycle yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the contract billing cycle are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.2.2 | Monthly Billing - System shall support monthly subscriptions. | Subscription & Licensing Management | CONTRACTED | `setSubscription` |
| 20.2.3 | Annual Billing - System shall support annual subscriptions. | Subscription & Licensing Management | CONTRACTED | `setSubscription` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- After accepting (or negotiating and re-proposing) a commercial model, the purchase agreement captures billing cycle, contract period, invoicing frequency (monthly/annually), legal entity information and payment method (bank transfer, card, etc.). *(client request · MoM 10 Sep 2026, 4.10 Purchase Agreement, Billing Terms & Trial/Demo Environment · DI-830)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-019` · status **notStarted** · provenance —
- Workshop pack:  board 5

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-019?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Custom Term, Cancel.
- [ ] Every transition is wired: `SGN-018`, `SGN-020`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-020` Billing & Legal Entity Information

**Capture the legally correct customer and billing information.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Purchase & Activation · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | public staff holding `ACCOUNT_CONFIGURE` (1 configure) |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/purchase-activation/billing-legal-entity-information-sgn-020` |

**What the spec says about it.** The self-service form of `ADM-411`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Commercial Customer ≠ Operating Venue, Validate Entity / Save / Continue. Each needs an operation, or needs … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Commercial Customer ≠ Operating Venue (primary button) | navigation or local | — | — | — | — |
| Validate Entity / Save / Continue (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `SGN-019` Contract & Billing Cycle Selection: *Back to Contract & Billing Cycle Selection*
- → `SGN-021` Payment Method & Settlement Setup: *Payment Method & Settlement Setup*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The billing legal entity list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the billing legal entity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No billing legal entity yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the billing legal entity are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `createLegalEntity` → `ACCOUNT_CONFIGURE` (configure) · staff

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.7.38 | Support account ownership by business unit/site. | F&B & Guest Management | CONTRACTED | `createLegalEntity` |
| 5.7.49 | Support multiple sites/business entities. | F&B & Guest Management | CONTRACTED | `createLegalEntity` |
| 5.7.50 | Assign accounts to specific sites. | F&B & Guest Management | CONTRACTED | `createLegalEntity` |
| 5.7.51 | Site-level account reporting. | F&B & Guest Management | CONTRACTED | `createLegalEntity` |
| 5.7.52 | Site-level balance reporting. | F&B & Guest Management | CONTRACTED | `createLegalEntity` |
| 5.7.54 | Site-level revenue tracking. | F&B & Guest Management | CONTRACTED | `createLegalEntity` |
| 5.7.56 | Site-level accounting permissions. | F&B & Guest Management | CONTRACTED | `createLegalEntity` |
| 5.7.88 | The system shall support multiple legal entities, companies, business units, and attractions while maintaining separate accounting books, reporting structures, and financial controls. Shared products … | F&B & Guest Management | CONTRACTED | `createLegalEntity` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- After accepting (or negotiating and re-proposing) a commercial model, the purchase agreement captures billing cycle, contract period, invoicing frequency (monthly/annually), legal entity information and payment method (bank transfer, card, etc.). *(client request · MoM 10 Sep 2026, 4.10 Purchase Agreement, Billing Terms & Trial/Demo Environment · DI-830)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-020` · status **notStarted** · provenance —
- Workshop pack:  board 5

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-020?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Commercial Customer ≠ Operating Venue, Validate Entity / Save / Continue.
- [ ] Every transition is wired: `SGN-019`, `SGN-021`.
- [ ] Every gated control is gated: `ACCOUNT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-021` Payment Method & Settlement Setup

**Configure how TICVAI collects its fees.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Purchase & Activation · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | public staff holding `TENANT_CONFIGURE` (1 configure) |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/purchase-activation/payment-method-settlement-setup-sgn-021` |

**What the spec says about it.** The self-service form of `ADM-412`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). **Diverged from ADM-412 on 28 September; no longer `sameAs`.** ADM-412 gained the platform-staff tenant picker and grant step (audit R098), which does not apply to a prospect with no account and no tenant yet, so `tools/applied/apply-subscription-placement.py` no longer keeps the two in step. The payment-methods change of audit R275 (a) is applied here by hand.

**Known gaps.** **Payment Method & Settlement Setup declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Payment methods | multi select | — | — | — | — | **The methods follow the contract (decided 28 September, audit R275 (a))**: the options are the `PaymentProvider.supportedMethods` enum that `setPaymentProvider` accepts. The pack's Credit / Debit … | — |

**Sent by *Save payment provider*** (`setPaymentProvider`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setPaymentProvider` body |
| Name `name` | text field | required | — | — | — | — | `setPaymentProvider` body |
| Kind `kind` | select | required | — | Network international · Stripe · Adyen · Checkout · Cash · Wallet · Other | — | — | `setPaymentProvider` body |
| Supported methods `supportedMethods` | multi-select chips | optional | — | Card · Apple pay · Google pay · Samsung pay · Wallet · Bank transfer · Cash · Bnpl | — | — | `setPaymentProvider` body |
| Supported currencies `supportedCurrencies` | list of values (chips) | optional | — | — | — | — | `setPaymentProvider` body |
| Supports tokenisation `supportsTokenisation` | toggle | optional | — | — | — | The keystone. Recurring billing, wallet auto-reload, one-click checkout and payment links all require a stored credential, and none of them can be designed until this is answered … | `setPaymentProvider` body |
| Supports partial capture `supportsPartialCapture` | toggle | optional | on | — | — | — | `setPaymentProvider` body |
| Accepted on channels `acceptedOnChannels` | multi-select chips | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | BL-115. Which channels may use this provider. | `setPaymentProvider` body |
| Presentment currencies `presentmentCurrencies` | list of values (chips) | optional | — | — | — | BL-070. What a storefront may quote in, distinct from what it settles in. | `setPaymentProvider` body |
| Supports3ds `supports3ds` | toggle | optional | on | — | — | — | `setPaymentProvider` body |
| Terminal `terminal` | group | optional | — | — | — | BL-119. Terminal behaviour, where this provider drives a physical device. | `setPaymentProvider` body |
| Emv certification ref `terminal.emvCertificationRef` | text field | optional | — | — | — | — | `setPaymentProvider` body |
| Offline floor limit `terminal.offlineFloorLimit` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What a terminal may approve with no connection. Above it the sale waits; below it the venue carries the risk knowingly — and a floor limit of zero means a till stops when the line … | `setPaymentProvider` body |
| Supports offline approval `terminal.supportsOfflineApproval` | toggle | optional | off | — | — | — | `setPaymentProvider` body |
| Receipt signature required `terminal.receiptSignatureRequired` | toggle | optional | off | — | — | — | `setPaymentProvider` body |
| Supports tip on terminal `terminal.supportsTipOnTerminal` | toggle | optional | off | — | — | — | `setPaymentProvider` body |
| Credential ref `credentialRef` | text field | optional | — | — | — | A vault reference. Never the credential, never returned, and rotated without a contract change. | `setPaymentProvider` body |
| Scope level `scopeLevel` | segmented control | optional | — | Tenant · Region · Venue | — | — | `setPaymentProvider` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setPaymentProvider` body |
| Is active `isActive` | toggle | required | — | — | — | — | `setPaymentProvider` body |
| Routing `routing` | repeatable rows | optional | — | — | — | The ordered rules that send payments to this provider. `providerId` on each is this provider's `id`. | `setPaymentProvider` body |
| ID `routing[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setPaymentProvider` body |
| Priority `routing[].priority` | number field | required | — | — | — | — | `setPaymentProvider` body |
| Provider `routing[].providerId` | picker: choose a provider | required | — | — | shows names, sends the id | — | `setPaymentProvider` body |
| Conditions `routing[].conditions` | group | optional | — | — | — | Match on what is known before the charge — channel, currency, method, issuer country, amount band. | `setPaymentProvider` body |
| Channel `routing[].conditions.channel` | select | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing at nothing. | `setPaymentProvider` body |
| Currency `routing[].conditions.currency` | text field | optional | — | Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. | — | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per … | `setPaymentProvider` body |
| Method `routing[].conditions.method` | text field | optional | — | — | — | — | `setPaymentProvider` body |
| Issuer country `routing[].conditions.issuerCountry` | text field | optional | — | — | — | — | `setPaymentProvider` body |
| Min amount `routing[].conditions.minAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setPaymentProvider` body |
| Max amount `routing[].conditions.maxAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setPaymentProvider` body |
| Fallback provider `routing[].fallbackProviderId` | picker: choose a fallback provider | optional | — | — | shows names, sends the id | Where this provider declines or is unreachable. A decline is not always a fallback case — an insufficient-funds decline should not be retried elsewhere, and a gateway timeout … | `setPaymentProvider` body |
| Scope path `routing[].scopePath` | text field | optional | — | — | — | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — 49 tables were in that state, so a row … | `setPaymentProvider` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save payment provider (primary button) | `setPaymentProvider` PUT `/payment-providers` | SetPaymentProviderRequest | PaymentProvider | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | — |

**Where the user goes next**

- → `SGN-020` Billing & Legal Entity Information: *Back to Billing & Legal Entity Information*
- → `SGN-022` Order & Commercial Pricing Review: *Order & Commercial Pricing Review*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment method settlement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment method settlement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment method settlement yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment method settlement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setPaymentProvider` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.7.3 | Integrate with Stripe payment gateway and issue ticket and send confirmation email immediately after payment confirmation. | Ticketing Sales | CONTRACTED | `setPaymentProvider` |
| 4.2.9 | The system should be able to process payments by integrating with Stripe payment service provider. | Bundles and Promotions | CONTRACTED | `setPaymentProvider` |
| 2.6.33 | Website should be able to display multi currency and users should be able to switch the prices to the selected foreign currency. All the ticket prices, currency symbol to be shown based on the … | Ticketing Sales | CONTRACTED | data `PaymentProvider` |
| 2.9.1 | The system should display prices in multiple currencies in the B2C portal for guests comparison although the sale will be finalized always in local currency. | Ticketing Sales | CONTRACTED | data `PaymentProvider` |
| 4.2.10 | The system should support multiple different payments. The final list of payment methods will be dependent on the capabilities of the payment service provider. System should allow the admin team to … | Bundles and Promotions | CONTRACTED | data `PaymentProvider` |
| 4.2.12 | The system should support configuration of variable payment methods for different sales channels. Payment methods can be different from one sales channel to another. | Bundles and Promotions | CONTRACTED | data `PaymentProvider` |
| 4.2.14 | The system shall support integration with multiple payment gateways through a unified payment layer, allowing the business to switch or add gateways without changing business logic or sales channels. | Bundles and Promotions | CONTRACTED | data `PaymentProvider` |
| 4.2.15 | The system shall automatically select the most appropriate payment gateway based on configurable rules such as country, currency, sales channel, transaction amount, gateway availability, and … | Bundles and Promotions | CONTRACTED | data `PaymentProvider` |
| 4.2.16 | The system shall support secure tokenization of payment cards through PCI-compliant providers, allowing guests to securely save and reuse payment methods for future purchases. | Bundles and Promotions | CONTRACTED | data `PaymentProvider` |
| 4.3.28 | Automatically reload balances. | Bundles and Promotions | CONTRACTED | data `PaymentProvider` |
| 4.3.29 | Support recurring funding. | Bundles and Promotions | CONTRACTED | data `PaymentProvider` |
| 5.7.100 | The system shall support PCI-compliant integration architecture and secure payment processing. Sensitive cardholder information shall not be stored unless specifically certified and authorized. … | F&B & Guest Management | CONTRACTED | data `PaymentProvider` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- After accepting (or negotiating and re-proposing) a commercial model, the purchase agreement captures billing cycle, contract period, invoicing frequency (monthly/annually), legal entity information and payment method (bank transfer, card, etc.). *(client request · MoM 10 Sep 2026, 4.10 Purchase Agreement, Billing Terms & Trial/Demo Environment · DI-830)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-021` · status **notStarted** · provenance —
- Workshop pack:  board 5
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (34), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-021?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save payment provider.
- [ ] Every transition is wired: `SGN-020`, `SGN-022`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-022` Order & Commercial Pricing Review

**Show the complete financial arrangement before contractual acceptance. This screen must adapt dynamically to the commercial model. Example — Per Ticket + Minimum Guarantee**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Purchase & Activation · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | public |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/purchase-activation/order-commercial-pricing-review-sgn-022` |

**What the spec says about it.** The self-service form of `ADM-414`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every order commercial pricing** (data table)

| Shows | Format | Notes |
|---|---|---|
| Discount type | text | not in the schema: `Discount Type` |
| Value | text | not in the schema: `Value` |
| Period | text | not in the schema: `Period` |
| Approved by | text | not in the schema: `Approved By` |
| Expiry | text | not in the schema: `Expiry` |

**The selected order commercial pricing** (detail panel): The pack groups this record's detail under its own headings: “Rate”, “Expected Volume”, “Included Modules”, “Technical Capacity”, “Show where applicable”.

| Shows | Format | Notes |
|---|---|---|
| Discount type | text | not in the schema: `Discount Type` |
| Value | text | not in the schema: `Value` |
| Period | text | not in the schema: `Period` |
| Approved by | text | not in the schema: `Approved By` |
| Expiry | text | not in the schema: `Expiry` |

**Data it reads**: `previewSubscriptionChange` (onLoad, Order and pricing review)

**Where the user goes next**

- → `SGN-021` Payment Method & Settlement Setup: *Back to Payment Method & Settlement Setup*
- → `SGN-023` Commercial Agreement, Billable Definition & Customer Acceptance: *Commercial Agreement, Billable Definition & Customer Acceptance*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order commercial pricing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order commercial pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order commercial pricing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the order commercial pricing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.2.5 | Subscription Upgrade - System shall support subscription upgrades. | Subscription & Licensing Management | CONTRACTED | `previewSubscriptionChange` |
| 20.2.6 | Subscription Downgrade - System shall support subscription downgrades. | Subscription & Licensing Management | CONTRACTED | `previewSubscriptionChange` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- After accepting (or negotiating and re-proposing) a commercial model, the purchase agreement captures billing cycle, contract period, invoicing frequency (monthly/annually), legal entity information and payment method (bank transfer, card, etc.). *(client request · MoM 10 Sep 2026, 4.10 Purchase Agreement, Billing Terms & Trial/Demo Environment · DI-830)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-022` · status **notStarted** · provenance —
- Workshop pack:  board 5

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-022?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `SGN-021`, `SGN-023`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-023` Commercial Agreement, Billable Definition & Customer Acceptance

**This becomes one of the most important revised screens. The customer must understand and formally accept what TICVAI considers billable.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Purchase & Activation · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | public |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/purchase-activation/commercial-agreement-billable-definition-customer-accept-sgn-023` |

**What the spec says about it.** The self-service form of `ADM-415`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every commercial agreement billable** (data table)

| Shows | Format | Notes |
|---|---|---|
| Commercial model | text | not in the schema: `Commercial Model` |
| Contracted rate | text | not in the schema: `Contracted Rate` |
| Minimum guarantee | text | not in the schema: `Minimum Guarantee` |
| Guarantee period | text | not in the schema: `Guarantee Period` |
| Billing cycle | text | not in the schema: `Billing Cycle` |
| Contract duration | text | not in the schema: `Contract Duration` |
| Renewal | text | not in the schema: `Renewal` |
| Payment terms | text | not in the schema: `Payment Terms` |

**The selected commercial agreement billable** (detail panel): The pack groups this record's detail under its own headings: “For a transaction contract”, “For a per-ticket contract”, “Customer confirms”.

| Shows | Format | Notes |
|---|---|---|
| Commercial model | text | not in the schema: `Commercial Model` |
| Contracted rate | text | not in the schema: `Contracted Rate` |
| Minimum guarantee | text | not in the schema: `Minimum Guarantee` |
| Guarantee period | text | not in the schema: `Guarantee Period` |
| Billing cycle | text | not in the schema: `Billing Cycle` |
| Contract duration | text | not in the schema: `Contract Duration` |
| Renewal | text | not in the schema: `Renewal` |
| Payment terms | text | not in the schema: `Payment Terms` |

**Where the user goes next**

- → `SGN-022` Order & Commercial Pricing Review: *Back to Order & Commercial Pricing Review*
- → `SGN-024` Subscription Confirmation & Commercial Activation: *Subscription Confirmation & Commercial Activation*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial agreement billable list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial agreement billable untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial agreement billable yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial agreement billable are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- After accepting (or negotiating and re-proposing) a commercial model, the purchase agreement captures billing cycle, contract period, invoicing frequency (monthly/annually), legal entity information and payment method (bank transfer, card, etc.). *(client request · MoM 10 Sep 2026, 4.10 Purchase Agreement, Billing Terms & Trial/Demo Environment · DI-830)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-023` · status **notStarted** · provenance —
- Workshop pack:  board 5

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-023?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `SGN-022`, `SGN-024`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-024` Subscription Confirmation & Commercial Activation

**Create the formal active subscription/contract record after successful validation.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Purchase & Activation · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | public |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/purchase-activation/subscription-confirmation-commercial-activation-sgn-024` |

**What the spec says about it.** The self-service form of `ADM-417`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save subscription (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-594` Environment Ready & Handoff to AI Setup: *Environment Ready & Handoff to AI Setup*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The subscription confirmation commercial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the subscription confirmation commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No subscription confirmation commercial yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the subscription confirmation commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.2.2 | Monthly Billing - System shall support monthly subscriptions. | Subscription & Licensing Management | CONTRACTED | `setSubscription` |
| 20.2.3 | Annual Billing - System shall support annual subscriptions. | Subscription & Licensing Management | CONTRACTED | `setSubscription` |

#### Client meeting inputs

None names this screen.

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-024` · status **notStarted** · provenance —
- Workshop pack:  board 5

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-024?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save subscription, Cancel.
- [ ] Every transition is wired: `BO-594`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P17 reference designs** (from `handoff/design-batches/apps/6-ticvai-controller/README.md`)

- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the newest client-approved public look, for finish.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

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

### Across P17 TICVAI Sign-up

- The TICVAI marketing site should showcase demo versions of each platform (POS, kiosk, mobile app, menu management). *(client request · MoM 29 Sep 2026, 3. B2B / reseller portal · DI-1024)*
- Small/medium venues (e.g. 2 POS, 2 access points, basic B2C site) see pricing, subscribe and start configuring within a few days with no sales involvement; large/enterprise prospects stay sales-assisted (demo, consultative scoping) and enterprise-tier pricing is not exposed through self-service. *(agreed · MoM 10 Sep 2026, 4.9 Sales-Assisted vs. Self-Service Segmentation Philosophy · DI-829)*
- On top of the trade-license review, the applicant confirms access to the submitted domain email (link or OTP, 2FA-style) before portal access. *(agreed · MoM 10 Sep 2026, 4.8 Customer Portal Access, Authentication & Verification · DI-828)*
- Portal access exposes TICVAI pricing, so prospects submit contact details and a trade license as proof of a real venue, reviewed and approved by TICVAI before access is granted. *(agreed · MoM 10 Sep 2026, 4.8 Customer Portal Access, Authentication & Verification · DI-827)*
- Gap (Allam): screens don't show how a prospect logs into a secure portal to view their proposed package; account credentials (user ID and password) are created once onboarding is submitted so the prospect can access and track the proposal. *(client request · MoM 10 Sep 2026, 4.7 Package Builder & Module Marketplace · DI-826)*
- Prospect onboarding: a short questionnaire (venue type, user count, expected annual visitors, modules such as B2C, B2B, seat assignment) via a website/AI-assisted flow; small/medium venues auto-classified and self-configure via AI-assisted setup; enterprise routed to a sales-assisted demo. *(client request · MoM 9 Sep 2026, 4.19 Licensing & Subscription Model - Preliminary Concept · DI-807)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Small-customer self-service subscription flow: select required modules, pay online, enter venue and business details, environment is provisioned automatically, then the customer configures products, tickets, users and venue information and starts using the system. *(client request · MoM 28 Jul 2026, 6. Two Deployment and Commercial Models · DI-011)*

**6 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createLegalEntity": {"method":"POST","path":"/legal-entities","contract":"finance","summary":"Create a legal entity","permission":"ACCOUNT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LegalEntity","responds":"LegalEntity"},
"setPaymentProvider": {"method":"PUT","path":"/payment-providers","contract":"orders","summary":"Configure a gateway and its routing","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"SetPaymentProviderRequest","responds":"PaymentProvider"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"LegalEntity": {"x-ticvai-persistence":"ledger.legal_entity","type":"object","description":"Also the `createLegalEntity` body. **`id` and `scopePath` are server-owned** (`readOnly`) and ignored if sent.\n","required":["id","code","name","countryCode","currency","currencyScale","fiscalYearStartMonth"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"countryCode":{"type":"string","pattern":"^[A-Z]{2}$"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"taxRegistrationNumber":{"type":"string","nullable":true},"fiscalYearStartMonth":{"type":"integer","minimum":1,"maximum":12},"regionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"isActive":{"type":"boolean"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"PaymentProvider": {"type":"object","x-ticvai-persistence":"payments.provider","description":"BL-116, CF-131. **`Payment` carried `providerName` and `providerReference`, which records a provider and does not abstract one.**\nTwo gateways are confirmed for Phase 1 — **Network International and Stripe** — and that is exactly the number that forces this: **one gateway can be hard-coded and two cannot.**\nCredentials live in the vault and never here, following `ai.AiProvider` (ADR-0020's rule applied outside AI): **no surface ever holds a provider key.**\n","required":["id","name","kind","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","enum":["networkInternational","stripe","adyen","checkout","cash","wallet","other"]},"supportedMethods":{"type":"array","items":{"type":"string","enum":["card","applePay","googlePay","samsungPay","wallet","bankTransfer","cash","bnpl"]}},"supportedCurrencies":{"type":"array","items":{"type":"string"}},"supportsTokenisation":{"type":"boolean","description":"**The keystone.** Recurring billing, wallet auto-reload, one-click checkout and payment links all require a stored credential, and none of them can be designed until this is answered per provider.\n"},"supportsPartialCapture":{"type":"boolean","default":true},"acceptedOnChannels":{"type":"array","description":"BL-115. **Which channels may use this provider.** A kiosk taking cash and a website taking cards is not a policy either could infer, and a venue that accepts cash at a till and not online had no way to say so.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}},"presentmentCurrencies":{"type":"array","description":"BL-070. **What a storefront may quote in**, distinct from what it settles in. A guest sees GBP and the venue books AED — the display currency is the provider's capability and the settlement currency is the venue's (CF-114 on multi-currency).\n","items":{"type":"string"}},"supports3ds":{"type":"boolean","default":true},"terminal":{"type":"object","nullable":true,"description":"BL-119. **Terminal behaviour, where this provider drives a physical device.** Unstated until now, and every field here is one a certification body asks about.\n","properties":{"emvCertificationRef":{"type":"string","nullable":true},"offlineFloorLimit":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**What a terminal may approve with no connection.** Above it the sale waits; below it the venue carries the risk knowingly — and a floor limit of zero means a till stops when the line does.\n"},"supportsOfflineApproval":{"type":"boolean","default":false},"receiptSignatureRequired":{"type":"boolean","default":false},"supportsTipOnTerminal":{"type":"boolean","default":false}}},"credentialRef":{"type":"string","writeOnly":true,"description":"A vault reference. **Never the credential**, never returned, and rotated without a contract change.\n"},"scopeLevel":{"type":"string","enum":["tenant","region","venue"]},"scopePath":{"type":"string"},"isActive":{"type":"boolean"}}},
"PaymentRouting": {"type":"object","x-ticvai-persistence":"payments.routing_rule","description":"**Which provider takes a given payment, and why.** With two gateways the question is live from day one: a UAE card may cost less through one and an international card less through the other.\n**Ordered rules, first match wins, and a fallback that is not optional.** A gateway outage with no fallback is a venue that cannot sell.\n","required":["id","priority","providerId"],"properties":{"id":{"type":"string","format":"uuid"},"priority":{"type":"integer"},"providerId":{"type":"string","format":"uuid"},"conditions":{"type":"object","description":"**Match on what is known before the charge** — channel, currency, method, issuer country, amount band. Not on anything that requires asking the provider first.\n","properties":{"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"currency":{"type":"string","nullable":true,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"method":{"type":"string","nullable":true},"issuerCountry":{"type":"string","nullable":true},"minAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"fallbackProviderId":{"type":"string","format":"uuid","nullable":true,"description":"**Where this provider declines or is unreachable.** A decline is not always a fallback case — an insufficient-funds decline should not be retried elsewhere, and a gateway timeout should.\n"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"SetPaymentProviderRequest": {"x-ticvai-persistence":"none — request only; the provider lands in payments.provider and its rules in payments.routing_rule","description":"Request only. **A provider and the rules that route to it**, because `setPaymentProvider` is *\"configure a gateway and its routing\"* and writes both tables — and the provider schema alone carried no routing field, so the routing half had nothing to arrive in.\n","allOf":[{"$ref":"#/components/schemas/PaymentProvider"},{"type":"object","properties":{"routing":{"type":"array","description":"The ordered rules that send payments to this provider. `providerId` on each is this provider's `id`.","items":{"$ref":"#/components/schemas/PaymentRouting"}}}}]}
}
```
