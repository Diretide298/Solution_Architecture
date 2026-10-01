# WS151 — Payment Payment Orchestration board 5

**10 screens · 16 operations · 16 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `CREDIT_MANAGE, ORDER_CREATE, ORDER_VIEW, PAYMENT_CONFIGURE, PAYMENT_VIEW, WALLET_VIEW`. A control nobody can use must say so,
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
| `ADM-599` | Mixed Tender & Credit Command Center\t93 | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-600` | Mixed Tender Rule & Combination Builder\t93 | B–D | 0 | 6 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-601` | Split Payment & Tender Allocation Manager\t94 | B–D | 4 | 9 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-602` | B2B Credit Account & Limit Manager\t95 | B–D | 7 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-603` | B2B Invoice, On-Account & Payment Terms Configuration\t96 | A | 10 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-604` | Stored Value, Gift Card & Voucher Tender Controls\t97 | B–D | 11 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `ADM-605` | Advanced Payment Eligibility, Sequence & Restriction Rules\t98 | B–D | 0 | 2 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-606` | Partial Payment, Failure & Recovery Manager\t100 | B–D | 0 | 4 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-607` | Mixed Tender Transaction Trace & Allocation Audit\t100 | B–D | 11 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-608` | Mixed Tender Simulator, Credit Exposure & AI Advisor\t102 | B–D | 0 | 10 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-600, ADM-606 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-599` Mixed Tender & Credit Command Center\t93

**Provide centralized operational visibility over mixed-tender and account-credit transactions.**

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
| Route | `/commercial/mixed-tender-credit-command-center-t93-adm-599` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Mixed-Tender Transactions** (metric tile)

**Mixed-Tender Value** (metric tile)

**Average Tenders per Transaction** (metric tile)

**B2B Credit Transactions** (metric tile)

**B2B Credit Utilized** (metric tile)

**Outstanding B2B Credit** (metric tile)

**Invoice / On-Account Transactions** (metric tile)

**Gift Card Contributions** (metric tile)

**Stored-Value Contributions** (metric tile)

**Split Payment Failures** (metric tile)

**Partially Paid Orders** (metric tile)

**Payment Allocation Exceptions** (metric tile)

**Data it reads**: `getMixedTenderRules` (onLoad, Tender rules in force)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-600` Mixed Tender Rule & Combination Builder\t93: *Mixed Tender Rule & Combination Builder\t93*
- → `ADM-601` Split Payment & Tender Allocation Manager\t94: *Split Payment & Tender Allocation Manager\t94*
- → `ADM-602` B2B Credit Account & Limit Manager\t95: *B2B Credit Account & Limit Manager\t95*
- → `ADM-603` B2B Invoice, On-Account & Payment Terms Configuration\t96: *B2B Invoice, On-Account & Payment Terms Configuration\t96*
- → `ADM-604` Stored Value, Gift Card & Voucher Tender Controls\t97: *Stored Value, Gift Card & Voucher Tender Controls\t97*
- → `ADM-605` Advanced Payment Eligibility, Sequence & Restriction Rules\t98: *Advanced Payment Eligibility, Sequence & Restriction Rules\t98*
- → `ADM-606` Partial Payment, Failure & Recovery Manager\t100: *Partial Payment, Failure & Recovery Manager\t100*
- → `ADM-607` Mixed Tender Transaction Trace & Allocation Audit\t100: *Mixed Tender Transaction Trace & Allocation Audit\t100*
- → `ADM-608` Mixed Tender Simulator, Credit Exposure & AI Advisor\t102: *Mixed Tender Simulator, Credit Exposure & AI Advisor\t102*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The mixed tender credit list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the mixed tender credit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No mixed tender credit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the mixed tender credit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getMixedTenderRules` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-599` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-599`
- Workshop pack: Payment_Payment_Orchestration.pdf board 5
- Flow F260 *Payment Payment Orchestration board 5: Mixed Tender & Credit Command Center\t93*, step 1: Opens Mixed Tender & Credit Command Center\t93 → Provide centralized operational visibility over mixed-tender and account-credit transactions.
- Flow F260 *Payment Payment Orchestration board 5: Mixed Tender & Credit Command Center\t93*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F260 *Payment Payment Orchestration board 5: Mixed Tender & Credit Command Center\t93*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F260 *Payment Payment Orchestration board 5: Mixed Tender & Credit Command Center\t93*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F260 *Payment Payment Orchestration board 5: Mixed Tender & Credit Command Center\t93*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F260 *Payment Payment Orchestration board 5: Mixed Tender & Credit Command Center\t93*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F260 *Payment Payment Orchestration board 5: Mixed Tender & Credit Command Center\t93*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F260 *Payment Payment Orchestration board 5: Mixed Tender & Credit Command Center\t93*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F260 branch at step 1 (expected): when Nothing has been set up on Mixed Tender & Credit Command Center\t93 yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F260 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-599?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-600`, `ADM-601`, `ADM-602`, `ADM-603`, `ADM-604`, `ADM-605`, `ADM-606`, `ADM-607`, `ADM-608`.
- [ ] Every gated control is gated: `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-600` Mixed Tender Rule & Combination Builder\t93

**Define which payment methods may be combined within a single transaction.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Card r t Credit; Card) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/mixed-tender-rule-combination-builder-t93-adm-600` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … **Mixed Tender Rule & Combination Builder\t93 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every mixed tender rule** (data table)

| Shows | Format | Notes |
|---|---|---|
| Card ✓ ✓ ✓ ✓ ✓ ✓ | text | not in the schema: `Card ✓ ✓ ✓ ✓ ✓ ✓` |
| Cash ✓ — ✓ ✓ ✓ ✓ | text | not in the schema: `Cash ✓ — ✓ ✓ ✓ ✓` |
| Voucher ✓ ✓ ✓* — ✓ ✓ | text | not in the schema: `Voucher ✓ ✓ ✓* — ✓ ✓` |

**The selected mixed tender rule** (detail panel): The pack groups this record's detail under its own headings: “Gift”, “Maximum”.

| Shows | Format | Notes |
|---|---|---|
| Card ✓ ✓ ✓ ✓ ✓ ✓ | text | not in the schema: `Card ✓ ✓ ✓ ✓ ✓ ✓` |
| Cash ✓ — ✓ ✓ ✓ ✓ | text | not in the schema: `Cash ✓ — ✓ ✓ ✓ ✓` |
| Voucher ✓ ✓ ✓* — ✓ ✓ | text | not in the schema: `Voucher ✓ ✓ ✓* — ✓ ✓` |

**Where the user goes next**

- → `ADM-599` Mixed Tender & Credit Command Center\t93: *Back to Mixed Tender & Credit Command Center\t93*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The mixed tender rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the mixed tender rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No mixed tender rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the mixed tender rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setMixedTenderRules` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-600` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-600`
- Workshop pack: Payment_Payment_Orchestration.pdf board 5
- Flow F260 *Payment Payment Orchestration board 5: Mixed Tender & Credit Command Center\t93*, step 2: Works in Mixed Tender Rule & Combination Builder\t93 → Define which payment methods may be combined within a single transaction.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-600?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-599`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-601` Split Payment & Tender Allocation Manager\t94

**Determine how an order total is allocated across several payment methods.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_CREATE`, `ORDER_VIEW`, `PAYMENT_CONFIGURE` (1 operate, 1 read, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/split-payment-tender-allocation-manager-t94-adm-601` |

**Known gaps.** **Split Payment & Tender Allocation Manager\t94 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Channel | text field | optional | — | max length 40 | — | Sends `?channel=` to `listPaymentAllocationRules`. | `listPaymentAllocationRules` ?channel |
| Terminal id | picker: choose a terminal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?terminalId=` to `listPaymentAllocationRules`. | `listPaymentAllocationRules` ?terminalId |
| Product id | picker: choose a product (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?productId=` to `listPaymentAllocationRules`. | `listPaymentAllocationRules` ?productId |
| Is active | toggle | optional | on | — | — | Sends `?isActive=` to `listPaymentAllocationRules`. | `listPaymentAllocationRules` ?isActive |

#### Outputs: what the screen shows and produces

**Shown**

**Every payment allocation rule** (data table, from `listPaymentAllocationRules`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Channel | text | — |
| Terminal | the name it points at, never the id | — |
| Product | the name it points at, never the id | — |
| Order type | text | — |
| Customer type | text | — |
| Allocation level | chip: Order level, Order line level, Product level, Tax fee component, Specific ticket … | — |
| Is active | yes / no (icon or chip) | — |
| Scope path | text | The partition key (ADR-0005). Operations write it at `venue` scope. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save multi payment split (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listPaymentAllocationRules` (onLoad, The venue's split-tender allocation rules)

**Where the user goes next**

- → `ADM-599` Mixed Tender & Credit Command Center\t93: *Back to Mixed Tender & Credit Command Center\t93*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The split payment tender list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the split payment tender untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No split payment tender yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the split payment tender are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setMultiPaymentSplit` → `ORDER_CREATE` (operate) · staff
- `setMixedTenderRules` → `PAYMENT_CONFIGURE` (configure) · staff
- `listPaymentAllocationRules` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-601` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-601`
- Workshop pack: Payment_Payment_Orchestration.pdf board 5
- Flow F260 *Payment Payment Orchestration board 5: Mixed Tender & Credit Command Center\t93*, step 4: Works in Split Payment & Tender Allocation Manager\t94 → Determine how an order total is allocated across several payment methods.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (403, 412).
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-601?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save multi payment split, Cancel.
- [ ] Every transition is wired: `ADM-599`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_VIEW`, `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-602` B2B Credit Account & Limit Manager\t95

**Manage payment credit facilities granted to authorized B2B customers, resellers, corporate clients or partners. This is not the general B2B customer profile. The B2B/CRM module remains authoritative for the customer/account itself. Board 5 owns the payment-credit capability.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `CREDIT_MANAGE`, `PAYMENT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/b2b-credit-account-limit-manager-t95-adm-602` |

**Known gaps.** **B2B Credit Account & Limit Manager\t95 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Credit limit | select field | — | — | — | — | — | — |
| Effective dates | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Allowed business units | select field | — | — | — | — | — | — |
| Allowed channels | select field | — | — | — | — | — | — |
| Payment terms | select field | — | — | — | — | — | — |
| Approval level | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Over limit only | toggle | — | — | `listB2bCreditAccounts` ?overLimitOnly |

#### Outputs: what the screen shows and produces

**Data it reads**: `listB2bCreditAccounts` (onLoad, On-account customers)

**Where the user goes next**

- → `ADM-599` Mixed Tender & Credit Command Center\t93: *Back to Mixed Tender & Credit Command Center\t93*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The b2b credit account configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the b2b credit account untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No b2b credit account configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listB2bCreditAccounts` → `PAYMENT_VIEW` (read) · staff
- `createB2bCreditAccount` → `CREDIT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-602` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-602`
- Workshop pack: Payment_Payment_Orchestration.pdf board 5
- Flow F260 *Payment Payment Orchestration board 5: Mixed Tender & Credit Command Center\t93*, step 6: Works in B2B Credit Account & Limit Manager\t95 → Manage payment credit facilities granted to authorized B2B customers, resellers, corporate clients or partners. This is not the general B2B customer profile. The B2B/CRM module remains authoritative …

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-602?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-599`.
- [ ] Every gated control is gated: `CREDIT_MANAGE`, `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-603` B2B Invoice, On-Account & Payment Terms Configuration\t96

**Configure how approved B2B customers can transact without immediate full payment.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | Block A · ticket #20691 (APP-SETUP-ADM-603) |
| Who uses it | ticvai staff holding `CREDIT_MANAGE`, `PAYMENT_CONFIGURE`, `PAYMENT_VIEW` (2 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `accountId` (navigation) |
| Route | `/commercial/b2b-invoice-on-account-payment-terms-configuration-t96-adm-603` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Customer/account | select field | — | — | — | — | — | — |
| Credit agreement | select field | — | — | — | — | — | — |
| Payment term | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Billing cycle | select field | — | — | — | — | — | — |
| Invoice requirement | select field | — | — | — | — | — | — |
| Purchase order requirement | select field | — | — | — | — | — | — |
| Approval requirement | select field | — | — | — | — | — | — |
| Transaction maximum | select field | — | — | — | — | — | — |
| Outstanding balance limit | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `getInstalmentPolicy` (onLoad, Show the instalment policy)

**Where the user goes next**

- → `ADM-599` Mixed Tender & Credit Command Center\t93: *Back to Mixed Tender & Credit Command Center\t93*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The b2b invoice on-account configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the b2b invoice on-account untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No b2b invoice on-account configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A share due at purchase outside 0-100, or more instalments than the frequency allows within the product's term. |

#### Permissions

- `setB2bPaymentTerms` → `CREDIT_MANAGE` (configure) · staff
- `getInstalmentPolicy` → `PAYMENT_VIEW` (read) · staff
- `setInstalmentPolicy` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-603` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-603`
- Workshop pack: Payment_Payment_Orchestration.pdf board 5
- Flow F260 *Payment Payment Orchestration board 5: Mixed Tender & Credit Command Center\t93*, step 8: Works in B2B Invoice, On-Account & Payment Terms Configuration\t96 → Configure how approved B2B customers can transact without immediate full payment.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (412, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-603?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-599`.
- [ ] Every gated control is gated: `CREDIT_MANAGE`, `PAYMENT_CONFIGURE`, `PAYMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-604` Stored Value, Gift Card & Voucher Tender Controls\t97

**Manage how stored-value instruments participate in payment without duplicating the Wallet or Voucher modules.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/stored-value-gift-card-voucher-tender-controls-t97-adm-604` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Can be used as tender | text field | — | — | — | — | — | — |
| Can combine with card | text field | — | — | — | — | — | — |
| Can combine with cash | text field | — | — | — | — | — | — |
| Can combine with B2B credit | text field | — | — | — | — | — | — |
| Minimum redemption | select field | — | — | — | — | — | — |
| Maximum redemption | select field | — | — | — | — | — | — |
| Full/partial balance usage | select field | — | — | — | — | — | — |
| Currency restrictions | select field | — | — | — | — | — | — |
| Product restrictions | select field | — | — | — | — | — | — |
| Venue restrictions | select field | — | — | — | — | — | — |
| Channel restrictions | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `getCreditConsumptionPolicy` (onLoad, The order within stored value)

**Where the user goes next**

- → `ADM-599` Mixed Tender & Credit Command Center\t93: *Back to Mixed Tender & Credit Command Center\t93*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The stored value gift configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the stored value gift untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No stored value gift configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setMixedTenderRules` → `PAYMENT_CONFIGURE` (configure) · staff
- `getCreditConsumptionPolicy` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-604` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-604`
- Workshop pack: Payment_Payment_Orchestration.pdf board 5
- Flow F260 *Payment Payment Orchestration board 5: Mixed Tender & Credit Command Center\t93*, step 10: Works in Stored Value, Gift Card & Voucher Tender Controls\t97 → Manage how stored-value instruments participate in payment without duplicating the Wallet or Voucher modules.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-604?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-599`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`, `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-605` Advanced Payment Eligibility, Sequence & Restriction Rules\t98

**Provide advanced transaction-level payment rules beyond the general method availability configured in Board 1.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Gift Card second) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/advanced-payment-eligibility-sequence-restriction-rules--adm-605` |

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Minimum card amount, Credit restriction, Voucher exclusivity. Each needs an operation, or needs removing … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every advanced payment eligibility** (data table)

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**The selected advanced payment eligibility** (detail panel): The pack groups this record's detail under its own headings: “Board 1 answers”, “Board 5 answers”, “AND”, “Voucher first”, “B2B Credit third”.

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Minimum card amount (primary button) | navigation or local | — | — | — | — |
| Credit restriction (secondary button) | navigation or local | — | — | — | — |
| Voucher exclusivity (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-599` Mixed Tender & Credit Command Center\t93: *Back to Mixed Tender & Credit Command Center\t93*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The advanced payment eligibility list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the advanced payment eligibility untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No advanced payment eligibility yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the advanced payment eligibility are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setMixedTenderRules` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-605` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-605`
- Workshop pack: Payment_Payment_Orchestration.pdf board 5
- Flow F260 *Payment Payment Orchestration board 5: Mixed Tender & Credit Command Center\t93*, step 12: Works in Advanced Payment Eligibility, Sequence & Restriction Rules\t98 → Provide advanced transaction-level payment rules beyond the general method availability configured in Board 1.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-605?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Minimum card amount, Credit restriction, Voucher exclusivity.
- [ ] Every transition is wired: `ADM-599`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-606` Partial Payment, Failure & Recovery Manager\t100

**Handle situations where some tenders succeed but another tender fails. This is one of the most important screens in Board 5.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Gift Card; Card) and no metric row |
| Offline | online only |
| Opens with | `caseId` (navigation) |
| Route | `/commercial/partial-payment-failure-recovery-manager-t100-adm-606` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … **Partial Payment, Failure & Recovery Manager\t100 declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| State | radio group | — | Scheduled · In progress · Exhausted · Recovered · Resolved manually | `listDunningCases` ?state |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every partial payment failure** (data table)

| Shows | Format | Notes |
|---|---|---|
| AED 200 ✓ | text | not in the schema: `AED 200 ✓` |
| AED 800 ✕ | text | not in the schema: `AED 800 ✕` |

**The selected partial payment failure** (detail panel): The pack groups this record's detail under its own headings: “AED 200 successfully consumed”, “Partial Payment States”, “Timeout”, “Partially Paid”.

| Shows | Format | Notes |
|---|---|---|
| AED 200 ✓ | text | not in the schema: `AED 200 ✓` |
| AED 800 ✕ | text | not in the schema: `AED 800 ✕` |

**Data it reads**: `getDunningPolicy` (onLoad, Read the retry schedule this venue runs); `listDunningCases` (onLoad, The queue, ordered by attempts remaining)

**Where the user goes next**

- → `ADM-599` Mixed Tender & Credit Command Center\t93: *Back to Mixed Tender & Credit Command Center\t93*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partial payment failure list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partial payment failure untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partial payment failure yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partial payment failure are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 An attempt schedule that would breach the policy's own guard — more attempts than `maxAttempts`, two attempts inside `minimumHoursBetweenAttempts`, or a … |

#### Permissions

- `setMixedTenderRules` → `PAYMENT_CONFIGURE` (configure) · staff
- `getDunningPolicy` → `PAYMENT_CONFIGURE` (configure) · staff
- `setDunningPolicy` → `PAYMENT_CONFIGURE` (configure) · staff
- `listDunningCases` → `PAYMENT_CONFIGURE` (configure) · staff
- `resolveDunningCase` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.14.22 | System shall support failed renewal payment recovery processes including configurable retry schedules, payment reminders, grace periods, service suspension, and account recovery workflows. | Ticketing Sales | CONTRACTED | `setDunningPolicy` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-606` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-606`
- Workshop pack: Payment_Payment_Orchestration.pdf board 5
- Flow F260 *Payment Payment Orchestration board 5: Mixed Tender & Credit Command Center\t93*, step 14: Works in Partial Payment, Failure & Recovery Manager\t100 → Handle situations where some tenders succeed but another tender fails. This is one of the most important screens in Board 5.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412, 422).
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-606?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-599`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-607` Mixed Tender Transaction Trace & Allocation Audit\t100

**Provide a complete financial and operational explanation of every multi-tender transaction.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ORDER_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/mixed-tender-transaction-trace-allocation-audit-t100-adm-607` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Operator/customer | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Rules applied | select field | — | — | — | — | — | — |
| Payment IDs | select field | — | — | — | — | — | — |
| Tender references | select field | — | — | — | — | — | — |
| Amounts | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Timestamps | select field | — | — | — | — | — | — |
| Overrides | select field | — | — | — | — | — | — |
| Approval | select field | — | — | — | — | — | — |
| Reversal/refund relationship | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listOrderPaymentDetail` (onLoad, Trace the allocation)

**Where the user goes next**

- → `ADM-599` Mixed Tender & Credit Command Center\t93: *Back to Mixed Tender & Credit Command Center\t93*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The mixed tender transaction configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the mixed tender transaction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No mixed tender transaction configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listOrderPaymentDetail` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-607` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-607`
- Workshop pack: Payment_Payment_Orchestration.pdf board 5
- Flow F260 *Payment Payment Orchestration board 5: Mixed Tender & Credit Command Center\t93*, step 16: Works in Mixed Tender Transaction Trace & Allocation Audit\t100 → Provide a complete financial and operational explanation of every multi-tender transaction.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-607?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-599`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-608` Mixed Tender Simulator, Credit Exposure & AI Advisor\t102

**Allow administrators to test complex tender combinations before activating rules.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PAYMENT_CONFIGURE`, `PAYMENT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Gift Card; Card; Gift Card AED 200) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/mixed-tender-simulator-credit-exposure-ai-advisor-t102-adm-608` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Require card for excess, Request approval, Reject B2B credit, Reduce credit allocation. Each needs an … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Over limit only | toggle | — | — | `listB2bCreditAccounts` ?overLimitOnly |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every mixed tender simulator** (data table)

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |
| AED 200 deducted | text | not in the schema: `AED 200 deducted` |
| No ticket/order | text | not in the schema: `No ticket/order` |
| No clear recovery process | text | not in the schema: `No clear recovery process` |
| → cash | text | not in the schema: `→ Cash` |

**The selected mixed tender simulator** (detail panel): The pack groups this record's detail under its own headings: “Order”, “AED 1,000 order”, “AED 1,000”, “Validate Tender Combination”, “Validate Balances / Credit”, “Process Tenders”.

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |
| AED 200 deducted | text | not in the schema: `AED 200 deducted` |
| No ticket/order | text | not in the schema: `No ticket/order` |
| No clear recovery process | text | not in the schema: `No clear recovery process` |
| → cash | text | not in the schema: `→ Cash` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Require card for excess (primary button) | navigation or local | — | — | — | — |
| Request approval (secondary button) | navigation or local | — | — | — | — |
| Reject B2B credit (destructive button) | navigation or local | — | — | — | — |
| Reduce credit allocation (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listB2bCreditAccounts` (onLoad, Credit exposure)

**Where the user goes next**

- → `ADM-599` Mixed Tender & Credit Command Center\t93: *Back to Mixed Tender & Credit Command Center\t93*

**What opens over it**

- confirmDialog *Reject B2B credit*: **Reject B2B credit on a mixed tender simulator is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The mixed tender simulator list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the mixed tender simulator untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No mixed tender simulator yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the mixed tender simulator are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `simulatePaymentConfiguration` → `PAYMENT_CONFIGURE` (configure) · staff
- `listB2bCreditAccounts` → `PAYMENT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-608` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS91 Payment Payment Orchestration Board 5.dc.html#adm-608`
- Workshop pack: Payment_Payment_Orchestration.pdf board 5
- Flow F260 *Payment Payment Orchestration board 5: Mixed Tender & Credit Command Center\t93*, step 18: Works in Mixed Tender Simulator, Credit Exposure & AI Advisor\t102 → Allow administrators to test complex tender combinations before activating rules.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-608?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Require card for excess, Request approval, Reject B2B credit, Reduce credit allocation.
- [ ] Every transition is wired: `ADM-599`.
- [ ] Every gated control is gated: `PAYMENT_CONFIGURE`, `PAYMENT_VIEW`.
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
"createB2bCreditAccount": {"method":"POST","path":"/b2b-credit-accounts","contract":"payments","summary":"Open an on-account relationship","permission":"CREDIT_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"B2bCreditAccount","responds":"B2bCreditAccount"},
"getCreditConsumptionPolicy": {"method":"GET","path":"/credit-consumption-policy","contract":"wallet","summary":"Which credit is spent first","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CreditConsumptionPolicy"},
"getDunningPolicy": {"method":"GET","path":"/dunning-policy","contract":"payments","summary":"How a failed recurring charge is chased","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"DunningPolicy"},
"getInstalmentPolicy": {"method":"GET","path":"/instalment-policy","contract":"payments","summary":"What may be paid in instalments, and on what terms","permission":"PAYMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"PayInstalmentPolicy"},
"getMixedTenderRules": {"method":"GET","path":"/mixed-tender-rules","contract":"payments","summary":"Which tenders may be combined, and in what order","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MixedTenderRules"},
"listB2bCreditAccounts": {"method":"GET","path":"/b2b-credit-accounts","contract":"payments","summary":"On-account customers, their limits and their exposure","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"overLimitOnly","in":"query","required":null}],"requestBody":null,"responds":"B2bCreditAccount"},
"listDunningCases": {"method":"GET","path":"/dunning-cases","contract":"payments","summary":"Recurring charges currently being chased","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"state","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrderPaymentDetail": {"method":"GET","path":"/order-payment-detail","contract":"orders","summary":"Order Payment Detail & Transaction Ledger","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderPaymentDetailTransactionLedgerView"},
"listPaymentAllocationRules": {"method":"GET","path":"/payment-allocation-rules","contract":"orders","summary":"The venue's split-tender allocation rules","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":null},{"name":"terminalId","in":"query","required":null},{"name":"productId","in":"query","required":null},{"name":"isActive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"resolveDunningCase": {"method":"POST","path":"/dunning-cases/{caseId}/resolve","contract":"payments","summary":"Stop chasing, with a reason","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"caseId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DunningCase"},
"setB2bPaymentTerms": {"method":"PUT","path":"/b2b-credit-accounts/{accountId}/terms","contract":"payments","summary":"Limit, terms, billing cycle and what happens at the limit","permission":"CREDIT_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"B2bPaymentTerms","responds":"B2bPaymentTerms"},
"setDunningPolicy": {"method":"PUT","path":"/dunning-policy","contract":"payments","summary":"Set the retry schedule and what happens when it runs out","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"DunningPolicy","responds":"DunningPolicy"},
"setInstalmentPolicy": {"method":"PUT","path":"/instalment-policy","contract":"payments","summary":"Set which products may be paid in instalments, how many and how often","permission":"PAYMENT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"PayInstalmentPolicy","responds":"PayInstalmentPolicy"},
"setMixedTenderRules": {"method":"PUT","path":"/mixed-tender-rules","contract":"payments","summary":"Split payment, tender sequence and restrictions","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"MixedTenderRules","responds":"MixedTenderRules"},
"setMultiPaymentSplit": {"method":"PUT","path":"/multi-payment-split","contract":"orders","summary":"Multi-Payment, Split Tender & Payment Allocation Configuration","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"MultiPaymentSplitTenderPaymentAllocationConfiguratioInput","responds":"MultiPaymentSplitTenderPaymentAllocationConfiguratioView"},
"simulatePaymentConfiguration": {"method":"POST","path":"/payment-configuration/simulate","contract":"payments","summary":"What a guest would be offered, and what it would cost","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RoutingContext","responds":"PaymentConfigurationSimulation"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"B2bCreditAccount": {"type":"object","x-ticvai-persistence":"payments.credit_account","description":"Board 5.4. **Exposure includes unbilled bookings, not just unpaid invoices.**","required":["organisationId"],"properties":{"id":{"type":"string","format":"uuid"},"organisationId":{"type":"string","format":"uuid"},"accountCode":{"type":"string"},"creditLimit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"outstandingInvoiced":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"outstandingUnbilled":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"availableCredit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["active","onHold","suspended","closed"]},"overLimit":{"type":"boolean","readOnly":true},"scopePath":{"type":"string"}}},
"B2bPaymentTerms": {"type":"object","x-ticvai-persistence":"payments.payment_terms","description":"Board 5.5. **What happens at the limit is the decision.**","properties":{"accountId":{"type":"string","format":"uuid"},"creditLimit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"paymentTermDays":{"type":"integer","default":30},"billingCycle":{"type":"string","enum":["perBooking","weekly","fortnightly","monthly"]},"purchaseOrderRequired":{"type":"boolean","default":false},"depositPercent":{"type":"number","nullable":true,"description":"1 September: *\"partial payment/deposit is supported for bulk bookings such as schools and corporates — e.g. a 20–30% deposit upfront with the balance due on or before arrival.\"*\n"},"balanceDue":{"type":"string","enum":["onArrival","beforeArrival","onTerms"],"default":"beforeArrival"},"atLimit":{"type":"string","enum":["refuse","warn","allowWithOverride"],"default":"allowWithOverride"},"overrideApprovalRole":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"CreditConsumptionPolicy": {"type":"object","x-ticvai-persistence":"wallet.consumption_policy","description":"Boards 3.5 and 3.7. **There is no neutral default**, which is why this is configuration.\n","properties":{"strategy":{"type":"string","enum":["expiringFirst","typePriority","nonRefundableFirst","manual"],"default":"expiringFirst","description":"**`expiringFirst` is the default because it is the one that does not quietly profit from the guest forgetting.**\n"},"typeOrder":{"type":"array","items":{"type":"string","format":"uuid"}},"withinTypeOrder":{"type":"string","enum":["fefo","fifo","lifo"],"default":"fefo"},"allowSplitTender":{"type":"boolean","default":true},"allowGuestChoice":{"type":"boolean","default":false,"description":"**Whether a guest may override the order at the till.** Rarely enabled, and the venues that want it want it badly.\n"},"scopePath":{"type":"string"}}},
"DeclineClass": {"type":"string","description":"BL-100. **Whether a failed charge may be tried again at all**, and the distinction is a merchant-account risk rather than a courtesy.\n`soft` — insufficient funds, a temporary hold, an issuer timeout. **Worth another attempt on another day**, and the whole reason a dunning schedule exists.\n`hard` — closed account, stolen card, do-not-honour, invalid number. **Never retried.** A hard decline put on a timetable is how a merchant ID gets flagged by the scheme, and the venue finds out when its acquirer calls.\n`unknown` — the provider gave no usable code. **Treated as `hard`**, because guessing `soft` optimises for one more attempt and risks the thing that cannot be undone.\n","enum":["soft","hard","unknown"]},
"DunningCase": {"x-ticvai-persistence":"payments.dunning_case","type":"object","description":"BL-100. **One recurring charge being chased**, and the row a venue works from.\n","required":["id","state","attemptsMade","firstFailedAt"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"orderId":{"type":"string","description":"The order whose renewal failed."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"state":{"$ref":"#/components/schemas/DunningState"},"declineClass":{"allOf":[{"$ref":"#/components/schemas/DeclineClass"}],"description":"**From the most recent attempt.** A case that begins `soft` and turns `hard` stops immediately rather than finishing its schedule — the card changed underneath it.\n"},"attemptsMade":{"type":"integer"},"nextAttemptAt":{"type":"string","format":"date-time","nullable":true,"description":"**Null where the case has ended or the decline is hard.** A scheduled time on a case nothing will act on is the field that makes a queue untrustworthy.\n"},"firstFailedAt":{"type":"string","format":"date-time"},"resolvedAt":{"type":"string","format":"date-time","nullable":true},"resolution":{"type":"string","nullable":true,"enum":["paidByOtherMeans","cardReplaced","writeOff","cancelledByGuest",null]},"resolutionNote":{"type":"string","nullable":true,"maxLength":500,"description":"**What `resolveDunningCase` was told, which had nowhere to land until now.** The enum above tells `writeOff` from `cardReplaced`; **which invoice, whose phone call and on what authority is the sentence beside it**, and the operation's own reasoning — that these reasons must be told apart afterwards — only works if the sentence survives.\n**Same shape as `marketing.case.resolution_note`**, which is a RAG source for exactly this reason: a resolution note is the most useful free text a support record holds.\n"},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who closed it.** A write-off with no name against it is the one resolution nobody can follow up, and it is also the one that moves money.\n"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Written at `venue` scope.\n"}}},
"DunningPolicy": {"x-ticvai-persistence":"payments.dunning_policy","type":"object","description":"2.14.19-2.14.23, BL-100. **How a failed recurring charge is chased, as a tenant policy rather than a platform constant.** A season pass at AED 300 a month and a locker subscription at AED 15 do not deserve the same number of attempts.\n","required":["maxAttempts","terminalAction"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"maxAttempts":{"type":"integer","minimum":1,"maximum":8,"default":4,"description":"**Capped at eight and defaulted to four.** The ceiling is not arbitrary: past a handful of attempts the recovery rate is close to nothing and the cost is a guest watching their bank app light up repeatedly for a charge they already know failed.\n"},"attemptOffsetDays":{"type":"array","items":{"type":"integer","minimum":0},"default":[0,3,7,14],"description":"**Days after the first failure, and the spacing is the part that matters.** Retrying at the same hour each day hits the same daily limit on the same card and tells the venue nothing it did not already know — **attempts spaced across the month straddle a payday**, which is the single thing that changes the answer for a soft decline.\n**Must be non-decreasing and no longer than `maxAttempts`**, enforced with 422 rather than by silently truncating a list somebody meant.\n"},"minimumHoursBetweenAttempts":{"type":"integer","default":24,"description":"**A floor under the offsets, because a schedule is edited by hand.** Two offsets on the same day are a typo that reads as a policy.\n"},"retryableDeclineClasses":{"type":"array","items":{"$ref":"#/components/schemas/DeclineClass"},"default":["soft"],"description":"**`soft` alone, and widening it is a deliberate act.** The field exists rather than being implied so that a venue that adds `unknown` has chosen to, and so an auditor can see that it did.\n"},"notifyGuestOnEachAttempt":{"type":"boolean","default":false,"description":"**False by default.** A guest told four times about one failed renewal reads it as four failures. The first and the last are the ones that mean something — the first because they can fix it, the last because their pass is about to change.\n"},"terminalAction":{"type":"string","enum":["suspendBilling","cancelRenewal"],"default":"suspendBilling","description":"**What happens when the attempts run out, and it deliberately stops short of admission.** `suspendBilling` stops charging and leaves the entitlement as it is; `cancelRenewal` also stops the next term. **Neither revokes entry.**\n`graceDays` on the renewal model already governs how long a pass keeps working, and the failure this separation prevents is concrete: **a guest at a gate on a family day out, refused because a card expired and a retry ran at 3am.** Ending somebody's access stays a staff decision with a name on it.\n"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Written at `tenant` scope.\n"}}},
"DunningState": {"type":"string","enum":["scheduled","inProgress","exhausted","recovered","resolvedManually"],"description":"BL-100. **`exhausted` and `recovered` are both endings and only one of them is a failure.** A schedule with a single terminal state cannot tell a venue whether dunning is working, which is the only question a venue asks of it.\n"},
"MixedTenderRules": {"type":"object","x-ticvai-persistence":"payments.mixed_tender_rules","description":"Boards 5.2 and 5.7. **Sequence is not cosmetic.**","properties":{"splitPaymentAllowed":{"type":"boolean","default":true},"maximumTenders":{"type":"integer","default":3},"tenderOrder":{"type":"array","items":{"type":"string"},"description":"**Across tender kinds.** `wallet` decides the order within stored value."},"allowedCombinations":{"type":"array","items":{"type":"object","properties":{"methodKinds":{"type":"array","items":{"type":"string"}},"allowed":{"type":"boolean"},"reason":{"type":"string","nullable":true}}}},"partialPaymentAllowed":{"type":"boolean","default":false},"onPartialFailure":{"type":"string","enum":["reverseAll","keepAndRetry","keepAndHold"],"default":"reverseAll","description":"**Three tenders in, the fourth fails.** Reversing all of it is the only answer that leaves the guest and the ledger in a state anybody can explain.\n"},"scopePath":{"type":"string"}}},
"MultiPaymentSplitTenderPaymentAllocationConfiguratioInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; lands in `orders.payment_allocation_rule` (DM5, 29 September)","description":"**What Multi-Payment, Split Tender & Payment Allocation Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"channel":{"type":"string","description":"Channel"},"venue":{"type":"string","description":"Venue"},"terminal":{"type":"string","description":"Terminal"},"product":{"type":"string","description":"Product"},"orderType":{"type":"string","description":"Order Type"},"customerType":{"type":"string","description":"Customer Type"},"allocationLevel":{"type":"string","enum":["orderLevel","orderLineLevel","productLevel","taxFeeComponent","specificTicket","deposit"],"description":"What a payment is allocated against."},"isActive":{"type":"boolean","default":true,"description":"False retires the rule for this match key (decided 29 September, writers pass)."}}},
"MultiPaymentSplitTenderPaymentAllocationConfiguratioView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Multi-Payment, Split Tender & Payment Allocation Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"channel":{"type":"string","description":"Channel"},"venue":{"type":"string","description":"Venue"},"terminal":{"type":"string","description":"Terminal"},"product":{"type":"string","description":"Product"},"orderType":{"type":"string","description":"Order Type"},"customerType":{"type":"string","description":"Customer Type"},"allocationLevel":{"type":"string","enum":["orderLevel","orderLineLevel","productLevel","taxFeeComponent","specificTicket","deposit"],"description":"What a payment is allocated against."}}},
"OrderPaymentDetailTransactionLedgerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Order Payment Detail & Transaction Ledger displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"orderNumber":{"type":"string","description":"Order Number"},"customer":{"type":"string","description":"Customer"},"orderTotal":{"type":"string","description":"Order Total"},"currency":{"type":"string","description":"Currency"},"paid":{"type":"string","description":"Paid"},"refunded":{"type":"string","description":"Refunded"},"outstanding":{"type":"string","description":"Outstanding"},"creditApplied":{"type":"string","description":"Credit Applied"},"paymentStatus":{"type":"integer","description":"Payment Status"},"settlementStatus":{"type":"integer","description":"Settlement Status"},"transactions":{"type":"array","description":"Every financial transaction on the order, one entry each","items":{"type":"object","properties":{"type":{"type":"string","enum":["authorization","capture","payment","deposit","additionalCollection","partialRefund","reversal","walletCredit","voucher","creditNote","adjustment"],"description":"Transaction type"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Amount"},"status":{"type":"string","description":"Status"},"gateway":{"type":"string","description":"Gateway"},"merchant":{"type":"string","description":"Merchant"},"terminal":{"type":"string","description":"Terminal"},"authorizationCode":{"type":"string","description":"Authorization code"},"gatewayTransactionId":{"type":"string","description":"Gateway transaction ID"},"settlementReference":{"type":"string","description":"Settlement reference"},"externalReference":{"type":"string","description":"External reference"},"occurredAt":{"type":"string","format":"date-time","description":"When"}}}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PayInstalmentPolicy": {"type":"object","x-ticvai-persistence":"payments.instalment_policy","description":"4.2.17, 2.14.19. Also the `setInstalmentPolicy` body.","properties":{"enabled":{"type":"boolean","default":false},"eligibleProductKinds":{"type":"array","items":{"type":"string","enum":["membership","annualPass","seasonPass","groupBooking","event"]}},"minimumOrderValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"allowedFrequencies":{"type":"array","items":{"type":"string","enum":["monthly","quarterly","custom"]}},"maximumInstalments":{"type":"integer","minimum":2},"dueAtPurchasePercent":{"type":"number","minimum":0,"maximum":100},"instalmentFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"requireStoredCard":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `tenant` scope."}}},
"PaymentAllocationRule": {"type":"object","x-ticvai-persistence":"orders.payment_allocation_rule","description":"**At what level a split-tender payment is allocated, per channel, terminal, product, order type or customer type** (DM5, 29 September: data model for the agreed operations; written by `setMultiPaymentSplit`). The tender limits themselves stay in `payments.mixed_tender_rules`; this row says what each tender is allocated against. Narrowest match wins; a row naming nothing is the venue default.","required":["id","allocationLevel","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"channel":{"type":"string","maxLength":40,"nullable":true},"terminalId":{"type":"string","format":"uuid","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true},"orderType":{"type":"string","maxLength":40,"nullable":true},"customerType":{"type":"string","maxLength":40,"nullable":true},"allocationLevel":{"type":"string","enum":["orderLevel","orderLineLevel","productLevel","taxFeeComponent","specificTicket","deposit"]},"isActive":{"type":"boolean"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"PaymentConfigurationSimulation": {"type":"object","description":"Boards 1.10 and 5.10. **Eight boards of configuration that compose, silently.**","properties":{"offeredMethods":{"type":"array","items":{"type":"object","properties":{"methodId":{"type":"string","format":"uuid"},"name":{"type":"string"},"routesTo":{"type":"string","nullable":true},"estimatedCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"surcharge":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"suppressedMethods":{"type":"array","items":{"type":"object","properties":{"methodId":{"type":"string","format":"uuid"},"reason":{"type":"string"}}}},"findings":{"type":"array","items":{"type":"object","properties":{"severity":{"type":"string","enum":["blocking","warning"]},"message":{"type":"string"}}}}}},
"RoutingContext": {"type":"object","required":["amount"],"properties":{"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"methodId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"channel":{"type":"string","nullable":true},"cardScheme":{"type":"string","nullable":true},"cardIssuerCountry":{"type":"string","nullable":true},"cardPresent":{"type":"boolean","default":false},"customerId":{"type":"string","format":"uuid","nullable":true}}}
}
```
