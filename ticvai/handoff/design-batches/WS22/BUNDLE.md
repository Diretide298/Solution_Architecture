# WS22 — B2B, Reseller & OTA Partner Management board 2

**10 screens · 0 operations · 0 schemas · 0 permissions**

Platform P10 Partner Web · ships as **ticvai-control** ·
partner audience · web ·
online only

## Who this is for

**partner on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
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
| `PTR-032` | Commercial Agreement Command Center | B–D | 2 | 30 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `PTR-033` | Agreement & Contract Terms Builder | B–D | 26 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `PTR-034` | Partner Rate & Net Pricing Configuration | B–D | 10 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `PTR-035` | Commission, Margin & Incentive Management | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `PTR-036` | Credit Limit & Exposure Management | B–D | 11 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `PTR-037` | Deposit, Guarantee & Financial Security Management | B–D | 0 | 6 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `PTR-038` | Payment Terms, Billing & Account Configuration | B–D | 0 | 14 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `PTR-039` | Commercial Allocation, Quota & Commitment Management | B–D | 0 | 14 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `PTR-040` | Booking Limits, Commercial Exceptions & Approval | B–D | 18 | 0 | 5 | 0 | 1 | 6 | — | notStarted (generated) |
| `PTR-041` | Commercial Agreement 360°, Health & AI Review | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**PTR-035, PTR-041 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `PTR-032` Commercial Agreement Command Center

**Provide commercial and finance teams with a centralized view of all partner agreements and their current commercial health.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each agreement should show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/commercial-agreement-command-center-ptr-032` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search commercial agreement | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by partner, partner type, brand, venue, country, agreement type and 5 more — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Shown**

**Active Agreements** (metric tile)

**Draft Agreements** (metric tile)

**Pending Approval** (metric tile)

**Agreements Expiring Soon** (metric tile)

**Expired Agreements** (metric tile)

**Partners on Credit Hold** (metric tile)

**Total Approved Credit** (metric tile)

**Current Credit Exposure** (metric tile)

**Outstanding Receivables** (metric tile)

**Active Commercial Allocations** (metric tile)

**Agreements With Exceptions** (metric tile)

**Commercial Risk Alerts** (metric tile)

**Every commercial agreement** (data table, from `listCommercialAgreement`)

| Shows | Format | Notes |
|---|---|---|
| Agreement ID | text | not in the schema: `CommercialAgreementCommandCenterView.agreementId` |
| Partner | text | not in the schema: `CommercialAgreementCommandCenterView.partner` |
| Agreement type | text | not in the schema: `CommercialAgreementCommandCenterView.agreementType` |
| Brand venue | text | not in the schema: `CommercialAgreementCommandCenterView.brandVenue` |
| Market | text | not in the schema: `CommercialAgreementCommandCenterView.market` |
| Valid from | text | not in the schema: `CommercialAgreementCommandCenterView.validFrom` |
| Valid to | text | not in the schema: `CommercialAgreementCommandCenterView.validTo` |
| Pricing model | text | not in the schema: `CommercialAgreementCommandCenterView.pricingModel` |
| Commission model | text | not in the schema: `CommercialAgreementCommandCenterView.commissionModel` |
| Credit term days | text | not in the schema: `CommercialAgreementCommandCenterView.creditTermDays` |
| Credit limit | text | not in the schema: `CommercialAgreementCommandCenterView.creditLimit` |
| Current exposure | text | not in the schema: `CommercialAgreementCommandCenterView.currentExposure` |
| Allocation model | text | not in the schema: `CommercialAgreementCommandCenterView.allocationModel` |
| Agreement status | text | not in the schema: `CommercialAgreementCommandCenterView.agreementStatus` |
| Commercial owner | text | not in the schema: `CommercialAgreementCommandCenterView.commercialOwner` |

**The selected commercial agreement** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Agreement ID | text | not in the schema: `CommercialAgreementCommandCenterView.agreementId` |
| Partner | text | not in the schema: `CommercialAgreementCommandCenterView.partner` |
| Agreement type | text | not in the schema: `CommercialAgreementCommandCenterView.agreementType` |
| Brand venue | text | not in the schema: `CommercialAgreementCommandCenterView.brandVenue` |
| Market | text | not in the schema: `CommercialAgreementCommandCenterView.market` |
| Valid from | text | not in the schema: `CommercialAgreementCommandCenterView.validFrom` |
| Valid to | text | not in the schema: `CommercialAgreementCommandCenterView.validTo` |
| Pricing model | text | not in the schema: `CommercialAgreementCommandCenterView.pricingModel` |
| Commission model | text | not in the schema: `CommercialAgreementCommandCenterView.commissionModel` |
| Credit term days | text | not in the schema: `CommercialAgreementCommandCenterView.creditTermDays` |
| Credit limit | text | not in the schema: `CommercialAgreementCommandCenterView.creditLimit` |
| Current exposure | text | not in the schema: `CommercialAgreementCommandCenterView.currentExposure` |
| Allocation model | text | not in the schema: `CommercialAgreementCommandCenterView.allocationModel` |
| Agreement status | text | not in the schema: `CommercialAgreementCommandCenterView.agreementStatus` |
| Commercial owner | text | not in the schema: `CommercialAgreementCommandCenterView.commercialOwner` |

**Data it reads**: `listCommercialAgreement` (onLoad, Commercial Agreement Command Center); `listCommercialAgreementHealth` (onLoad, Commercial Agreement 360°, Health & AI Review)

**Where the user goes next**

- → `PTR-033` Agreement & Contract Terms Builder: *Works in Agreement & Contract Terms Builder*; calls `listCommercialAgreement`
- → `PTR-034` Partner Rate & Net Pricing Configuration: *Works in Partner Rate & Net Pricing Configuration*; calls `listCommercialAgreement`
- → `PTR-037` Deposit, Guarantee & Financial Security Management: *Works in Deposit, Guarantee & Financial Security Management*; calls `listCommercialAgreement`
- → `PTR-038` Payment Terms, Billing & Account Configuration: *Works in Payment Terms, Billing & Account Configuration*; calls `listCommercialAgreement`
- → `PTR-040` Booking Limits, Commercial Exceptions & Approval: *Works in Booking Limits, Commercial Exceptions & Approval*; calls `listCommercialAgreement`
- → `PTR-041` Commercial Agreement 360°, Health & AI Review: *Works in Commercial Agreement 360°, Health & AI Review*; calls `listCommercialAgreement`
- → `PTR-035` Commission, Margin & Incentive Management: *Works in Commission, Margin & Incentive Management*; carries `agreementId`; calls `listCommercialAgreement`
- → `PTR-036` Credit Limit & Exposure Management: *Works in Credit Limit & Exposure Management*; carries `agreementId`; calls `listCommercialAgreement`
- → `PTR-039` Commercial Allocation, Quota & Commitment Management: *Works in Commercial Allocation, Quota & Commitment Management*; carries `agreementId`; calls `listCommercialAgreement`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial agreement list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial agreement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial agreement yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial agreement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Agreements overview shows active and pending agreements; partner pricing discounts configurable by quantity, amount, percentage or tiered volume bands (e.g. 10% up to 1,000 tickets, 15% from 1,000-5,000); commission rate per ticket sold. *(client request · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-554)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-032` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-032`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 2
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 1: Opens Commercial Agreement Command Center → Provide commercial and finance teams with a centralized view of all partner agreements and their current commercial health.
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F131 branch at step 1 (expected): when Nothing has been set up on Commercial Agreement Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F131 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-032?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `PTR-033`, `PTR-034`, `PTR-037`, `PTR-038`, `PTR-040`, `PTR-041`, `PTR-035`, `PTR-036`, `PTR-039`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-033` Agreement & Contract Terms Builder

**Create the structured commercial agreement governing the partner relationship.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Configure/reference) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/agreement-contract-terms-builder-ptr-033` |

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Manual Renewal, Renewal Notice Period, Renewal Approval. Each needs an operation, or needs removing from the …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Agreement ID | select field | — | — | — | — | — | — |
| Agreement Name | select field | — | — | — | — | — | — |
| Partner | select field | — | — | — | — | — | — |
| Agreement Type | select field | — | — | — | — | — | — |
| Contract Reference | select field | — | — | — | — | — | — |
| Legal Entity | select field | — | — | — | — | — | — |
| Brand | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Territory | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Effective From | select field | — | — | — | — | — | — |
| Effective To | select field | — | — | — | — | — | — |
| Renewal Type | select field | — | — | — | — | — | — |
| Commercial Owner | select field | — | — | — | — | — | — |
| Finance Owner | select field | — | — | — | — | — | — |
| Payment Terms | select field | — | — | — | — | — | — |
| Commission Terms | select field | — | — | — | — | — | — |
| Pricing Basis | select field | — | — | — | — | — | — |
| Credit Terms | select field | — | — | — | — | — | — |
| Allocation Terms | select field | — | — | — | — | — | — |
| Cancellation Conditions | select field | — | — | — | — | — | — |
| Refund Conditions | select field | — | — | — | — | — | — |
| Booking Restrictions | select field | — | — | — | — | — | — |
| Settlement Terms | select field | — | — | — | — | — | — |
| Minimum Commitment | select field | — | — | — | — | — | — |
| Sales Target | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Manual Renewal (primary button) | navigation or local | — | — | — | — |
| Renewal Notice Period (secondary button) | navigation or local | — | — | — | — |
| Renewal Approval (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `PTR-032` Commercial Agreement Command Center: *Returns to the board's landing screen*; calls `setAgreementContractTerm`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The agreement contract terms configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the agreement contract terms untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No agreement contract terms configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Agreements overview shows active and pending agreements; partner pricing discounts configurable by quantity, amount, percentage or tiered volume bands (e.g. 10% up to 1,000 tickets, 15% from 1,000-5,000); commission rate per ticket sold. *(client request · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-554)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-033` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-033`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 2
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 2: Works in Agreement & Contract Terms Builder → Create the structured commercial agreement governing the partner relationship.

#### Acceptance for the design

- [ ] Every input above is drawn (26), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-033?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Manual Renewal, Renewal Notice Period, Renewal Approval.
- [ ] Every transition is wired: `PTR-032`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-034` Partner Rate & Net Pricing Configuration

**Define the commercial pricing basis available to a partner without recreating TICVAI's Pricing Engine.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure by) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-rate-net-pricing-configuration-ptr-034` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Partner | select field | — | — | — | — | — | — |
| Agreement | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Product Family | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Event | select field | — | — | — | — | — | — |
| Ticket Type | select field | — | — | — | — | — | — |
| Price Category | select field | — | — | — | — | — | — |
| Market | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `PTR-032` Commercial Agreement Command Center: *Returns to the board's landing screen*; calls `setPartnerRateNet`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner rate net configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner rate net untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner rate net configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Agreements overview shows active and pending agreements; partner pricing discounts configurable by quantity, amount, percentage or tiered volume bands (e.g. 10% up to 1,000 tickets, 15% from 1,000-5,000); commission rate per ticket sold. *(client request · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-554)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-034` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-034`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 2
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 4: Works in Partner Rate & Net Pricing Configuration → Define the commercial pricing basis available to a partner without recreating TICVAI's Pricing Engine.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-034?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `PTR-032`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-035` Commission, Margin & Incentive Management

**Configure how partner commissions and commercial incentives are calculated.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `agreementId` (navigation) |
| Route | `/partners/commission-margin-incentive-management-ptr-035` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Form: Save partner commission rules** (modal, opened by *Save partner commission rules*; *Save partner commission rules* calls `setPartnerCommissionRules`, *Cancel* sends nothing)

**Collects what `setPartnerCommissionRules` sends before it is called.** Required: `rules`. Dismissing sends nothing; the screen behind is unchanged.

`setPartnerCommissionRules` is not in any contract: draw the form greyed and list it in FINDINGS.md.

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Campaign Incentive (primary button) | navigation or local | — | — | — | — |
| Save partner commission rules (secondary button) | `setPartnerCommissionRules` (not in any contract) | — | — | — | — |

**Data it reads**: `listCommissionMarginIncentive` (onLoad, Commission, Margin & Incentive Management)

**Where the user goes next**

- → `PTR-032` Commercial Agreement Command Center: *Returns to the board's landing screen*; calls `listCommissionMarginIncentive`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commission margin incentive list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commission margin incentive untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commission margin incentive yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commission margin incentive are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Agreements overview shows active and pending agreements; partner pricing discounts configurable by quantity, amount, percentage or tiered volume bands (e.g. 10% up to 1,000 tickets, 15% from 1,000-5,000); commission rate per ticket sold. *(client request · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-554)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-035` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-035`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 2
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 6: Works in Commission, Margin & Incentive Management → Configure how partner commissions and commercial incentives are calculated.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-035?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Campaign Incentive, Save partner commission rules.
- [ ] Every transition is wired: `PTR-032`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-036` Credit Limit & Exposure Management

**Control the financial exposure TICVAI permits for partners buying on account. This should be one of the strongest finance-control screens in the B2B module.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `agreementId` (navigation) |
| Route | `/partners/credit-limit-exposure-management-ptr-036` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Credit Enabled | select field | — | — | — | — | — | — |
| Approved Credit Limit | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Temporary Credit Limit | select field | — | — | — | — | — | — |
| Effective Dates | select field | — | — | — | — | — | — |
| Credit Owner | select field | — | — | — | — | — | — |
| Risk Classification | select field | — | — | — | — | — | — |
| Approval Authority | select field | — | — | — | — | — | — |
| Warning at 70% | select field | — | — | — | — | — | — |
| High Risk at 90% | text field | — | — | — | — | — | — |
| Block at 100% | select field | — | — | — | — | — | — |

**Form: Save partner credit profile** (modal, opened by *Save partner credit profile*; *Save partner credit profile* calls `setPartnerCreditProfile`, *Cancel* sends nothing)

**Collects what `setPartnerCreditProfile` sends before it is called.** Required: `id`, `partnerId`, `agreementId`, `creditEnabled`, `creditStatus`. Optional: `temporaryCreditLimit`, `temporaryLimitUntil`, `creditOwnerPrincipalId`, `approvalAuthority`, `riskClassification`, `warningThresholdPercent`, `highRiskThresholdPercent`, `blockThresholdPercent`, `effectiveFrom`, `effectiveTo`, `approvalRequestId`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.

`setPartnerCreditProfile` is not in any contract: draw the form greyed and list it in FINDINGS.md.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Increase Limit, Reduce Limit, Temporary Increase, Place Credit Hold, Release Hold, Block Credit Transactions. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save partner credit profile (primary button) | `setPartnerCreditProfile` (not in any contract) | — | — | — | — |

**Data it reads**: `listCreditLimitExposure` (onLoad, Credit Limit & Exposure Management)

**Where the user goes next**

- → `PTR-032` Commercial Agreement Command Center: *Returns to the board's landing screen*; calls `listCreditLimitExposure`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credit limit exposure configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credit limit exposure untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credit limit exposure configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Three partner payment models: (1) credit limit, invoiced monthly and settled by cheque/bank transfer; (2) prepayment wallet funded by bank transfer or online top-up and drawn down per sale; (3) pay-per-transaction by card. *(agreed · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-555)*
- B2B account financial tab shows credit limit, credit days and a linked account-specific price list; accounts can be a main account with child (agent) accounts; every account shows its full sales/transaction history, as does a B2C customer profile. *(client request · MoM 7 Aug 2026, 11. Accounts Management (B2B and B2C) · DI-162)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-036` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-036`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 2
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 8: Works in Credit Limit & Exposure Management → Control the financial exposure TICVAI permits for partners buying on account. This should be one of the strongest finance-control screens in the B2B module.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-036?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save partner credit profile.
- [ ] Every transition is wired: `PTR-032`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-037` Deposit, Guarantee & Financial Security Management

**Manage financial security required to support partner credit or commercial access.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `partnerId` (session) |
| Route | `/partners/deposit-guarantee-financial-security-management-ptr-037` |

#### Inputs: what the user enters or picks

**Form: Save partner security** (modal, opened by *Save partner security*; *Save partner security* calls `setPartnerSecurity`, *Cancel* sends nothing)

**Collects what `setPartnerSecurity` sends before it is called.** Required: `id`, `partnerId`, `securityType`, `amount`, `currency`, `effectiveDate`, `verificationStatus`. Optional: `agreementId`, `issuingInstitution`, `reference`, `expiryDate`, `documentId`, `expiryAction`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.

`setPartnerSecurity` is not in any contract: draw the form greyed and list it in FINDINGS.md.

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every deposit guarantee financial** (data table, from `listDepositGuaranteeFinancial`)

| Shows | Format | Notes |
|---|---|---|
| Credit exposure | text | not in the schema: `DepositGuaranteeFinancialSecurityManagementView.creditExposure` |
| Security coverage | text | not in the schema: `DepositGuaranteeFinancialSecurityManagementView.securityCoverage` |
| Unsecured exposure | text | not in the schema: `DepositGuaranteeFinancialSecurityManagementView.unsecuredExposure` |

**The selected deposit guarantee financial** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Credit exposure | text | not in the schema: `DepositGuaranteeFinancialSecurityManagementView.creditExposure` |
| Security coverage | text | not in the schema: `DepositGuaranteeFinancialSecurityManagementView.securityCoverage` |
| Unsecured exposure | text | not in the schema: `DepositGuaranteeFinancialSecurityManagementView.unsecuredExposure` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Cash Deposit (primary button) | navigation or local | — | — | — | — |
| Security Deposit (secondary button) | navigation or local | — | — | — | — |
| Prepayment Balance (secondary button) | navigation or local | — | — | — | — |
| Other Approved Security (secondary button) | navigation or local | — | — | — | — |
| Save partner security (secondary button) | `setPartnerSecurity` (not in any contract) | — | — | — | — |

**Data it reads**: `listDepositGuaranteeFinancial` (onLoad, Deposit, Guarantee & Financial Security Management)

**Where the user goes next**

- → `PTR-032` Commercial Agreement Command Center: *Returns to the board's landing screen*; calls `listDepositGuaranteeFinancial`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The deposit guarantee financial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the deposit guarantee financial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No deposit guarantee financial yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the deposit guarantee financial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Three partner payment models: (1) credit limit, invoiced monthly and settled by cheque/bank transfer; (2) prepayment wallet funded by bank transfer or online top-up and drawn down per sale; (3) pay-per-transaction by card. *(agreed · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-555)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-037` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-037`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 2
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 10: Works in Deposit, Guarantee & Financial Security Management → Manage financial security required to support partner credit or commercial access.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-037?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Cash Deposit, Security Deposit, Prepayment Balance, Other Approved Security, Save partner security.
- [ ] Every transition is wired: `PTR-032`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-038` Payment Terms, Billing & Account Configuration

**Define how the partner pays TICVAI and how transactions are financially grouped.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/payment-terms-billing-account-configuration-ptr-038` |

**Known gaps.** **The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Immediate Payment, Credit Account, Deposit Balance, Bank Transfer, Card, Prepaid Balance, Other approved …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every payment terms billing** (data table, from `setPaymentTermBilling`)

| Shows | Format | Notes |
|---|---|---|
| Current balance | text | not in the schema: `PaymentTermsBillingAccountConfigurationView.currentBalance` |
| Outstanding | text | not in the schema: `PaymentTermsBillingAccountConfigurationView.outstanding` |
| Overdue | text | not in the schema: `PaymentTermsBillingAccountConfigurationView.overdue` |
| Available credit | text | not in the schema: `PaymentTermsBillingAccountConfigurationView.availableCredit` |
| Last payment | text | not in the schema: `PaymentTermsBillingAccountConfigurationView.lastPayment` |
| Next invoice | text | not in the schema: `PaymentTermsBillingAccountConfigurationView.nextInvoice` |
| Oldest outstanding invoice | text | not in the schema: `PaymentTermsBillingAccountConfigurationView.oldestOutstandingInvoice` |

**The selected payment terms billing** (detail panel): The pack groups this record's detail under its own headings: “Important Boundary”.

| Shows | Format | Notes |
|---|---|---|
| Current balance | text | not in the schema: `PaymentTermsBillingAccountConfigurationView.currentBalance` |
| Outstanding | text | not in the schema: `PaymentTermsBillingAccountConfigurationView.outstanding` |
| Overdue | text | not in the schema: `PaymentTermsBillingAccountConfigurationView.overdue` |
| Available credit | text | not in the schema: `PaymentTermsBillingAccountConfigurationView.availableCredit` |
| Last payment | text | not in the schema: `PaymentTermsBillingAccountConfigurationView.lastPayment` |
| Next invoice | text | not in the schema: `PaymentTermsBillingAccountConfigurationView.nextInvoice` |
| Oldest outstanding invoice | text | not in the schema: `PaymentTermsBillingAccountConfigurationView.oldestOutstandingInvoice` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Immediate Payment (primary button) | navigation or local | — | — | — | — |
| Credit Account (secondary button) | navigation or local | — | — | — | — |
| Deposit Balance (secondary button) | navigation or local | — | — | — | — |
| Bank Transfer (secondary button) | navigation or local | — | — | — | — |
| Card (secondary button) | navigation or local | — | — | — | — |
| Payment Link (secondary button) | navigation or local | — | — | — | — |
| Prepaid Balance (secondary button) | navigation or local | — | — | — | — |
| Other approved method (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `PTR-032` Commercial Agreement Command Center: *Returns to the board's landing screen*; calls `setPaymentTermBilling`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment terms billing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment terms billing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment terms billing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment terms billing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Three partner payment models: (1) credit limit, invoiced monthly and settled by cheque/bank transfer; (2) prepayment wallet funded by bank transfer or online top-up and drawn down per sale; (3) pay-per-transaction by card. *(agreed · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-555)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-038` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-038`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 2
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 12: Works in Payment Terms, Billing & Account Configuration → Define how the partner pays TICVAI and how transactions are financially grouped.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-038?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Immediate Payment, Credit Account, Deposit Balance, Bank Transfer, Card, Payment Link, Prepaid Balance, Other approved method.
- [ ] Every transition is wired: `PTR-032`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-039` Commercial Allocation, Quota & Commitment Management

**Define the commercial commitment of inventory to a partner. This differs from Area 4's operational channel allocation.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `agreementId` (navigation) |
| Route | `/partners/commercial-allocation-quota-commitment-management-ptr-039` |

#### Inputs: what the user enters or picks

**Form: Save partner allocations** (modal, opened by *Save partner allocations*; *Save partner allocations* calls `setPartnerAllocations`, *Cancel* sends nothing)

**Collects what `setPartnerAllocations` sends before it is called.** Required: `allocations`. Dismissing sends nothing; the screen behind is unchanged.

`setPartnerAllocations` is not in any contract: draw the form greyed and list it in FINDINGS.md.

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every commercial allocation quota** (data table, from `listCommercialAllocationQuota`)

| Shows | Format | Notes |
|---|---|---|
| Allocated | text | not in the schema: `CommercialAllocationQuotaCommitmentManagementView.allocated` |
| Booked | text | not in the schema: `CommercialAllocationQuotaCommitmentManagementView.booked` |
| Sold | text | not in the schema: `CommercialAllocationQuotaCommitmentManagementView.sold` |
| Returned | text | not in the schema: `CommercialAllocationQuotaCommitmentManagementView.returned` |
| Remaining | text | not in the schema: `CommercialAllocationQuotaCommitmentManagementView.remaining` |
| Utilization | text | not in the schema: `CommercialAllocationQuotaCommitmentManagementView.utilization` |
| Commitment achievement | text | not in the schema: `CommercialAllocationQuotaCommitmentManagementView.commitmentAchievement` |

**The selected commercial allocation quota** (detail panel): The pack groups this record's detail under its own headings: “Area 4 asks”, “This screen asks”, “Integration”.

| Shows | Format | Notes |
|---|---|---|
| Allocated | text | not in the schema: `CommercialAllocationQuotaCommitmentManagementView.allocated` |
| Booked | text | not in the schema: `CommercialAllocationQuotaCommitmentManagementView.booked` |
| Sold | text | not in the schema: `CommercialAllocationQuotaCommitmentManagementView.sold` |
| Returned | text | not in the schema: `CommercialAllocationQuotaCommitmentManagementView.returned` |
| Remaining | text | not in the schema: `CommercialAllocationQuotaCommitmentManagementView.remaining` |
| Utilization | text | not in the schema: `CommercialAllocationQuotaCommitmentManagementView.utilization` |
| Commitment achievement | text | not in the schema: `CommercialAllocationQuotaCommitmentManagementView.commitmentAchievement` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Guaranteed Allocation (primary button) | navigation or local | — | — | — | — |
| On-Request Allocation (secondary button) | navigation or local | — | — | — | — |
| Shared Allocation (secondary button) | navigation or local | — | — | — | — |
| Fixed Quantity (secondary button) | navigation or local | — | — | — | — |
| Percentage Allocation (secondary button) | navigation or local | — | — | — | — |
| Rolling Allocation (secondary button) | navigation or local | — | — | — | — |
| Seasonal Allocation (secondary button) | navigation or local | — | — | — | — |
| Take-or-pay where commercially applicable (secondary button) | navigation or local | — | — | — | — |
| Save partner allocations (secondary button) | `setPartnerAllocations` (not in any contract) | — | — | — | — |

**Data it reads**: `listCommercialAllocationQuota` (onLoad, Commercial Allocation, Quota & Commitment Management)

**Where the user goes next**

- → `PTR-032` Commercial Agreement Command Center: *Returns to the board's landing screen*; calls `listCommercialAllocationQuota`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial allocation quota list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial allocation quota untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial allocation quota yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial allocation quota are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Inventory can be reserved for a specific partner; booking limits cap tickets per transaction or transactions per day, per partner or overall. *(client request · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-556)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-039` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-039`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 2
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 14: Works in Commercial Allocation, Quota & Commitment Management → Define the commercial commitment of inventory to a partner. This differs from Area 4's operational channel allocation.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-039?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Guaranteed Allocation, On-Request Allocation, Shared Allocation, Fixed Quantity, Percentage Allocation, Rolling Allocation, Seasonal Allocation, Take-or-pay where commercially …, Save partner allocations.
- [ ] Every transition is wired: `PTR-032`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-040` Booking Limits, Commercial Exceptions & Approval

**Control transaction limits and provide a governed mechanism for commercial exceptions.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/booking-limits-commercial-exceptions-approval-ptr-040` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Price Exception, Credit Exception, Allocation Exception. Each needs an operation, or needs removing from the …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Maximum Tickets Per Booking | text field | — | — | — | — | — | — |
| Maximum Booking Value | select field | — | — | — | — | — | — |
| Daily Booking Limit | select field | — | — | — | — | — | — |
| Monthly Booking Limit | select field | — | — | — | — | — | — |
| Event Limit | select field | — | — | — | — | — | — |
| Product Limit | select field | — | — | — | — | — | — |
| Hold Limit | select field | — | — | — | — | — | — |
| Reservation Duration | select field | — | — | — | — | — | — |
| Cancellation Limit | select field | — | — | — | — | — | — |
| Partner | select field | — | — | — | — | — | — |
| Agreement | select field | — | — | — | — | — | — |
| Request Type | select field | — | — | — | — | — | — |
| Current Rule | select field | — | — | — | — | — | — |
| Requested Exception | select field | — | — | — | — | — | — |
| Amount/Impact | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |
| Effective Period | select field | — | — | — | — | — | — |
| Requester | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Price Exception (primary button) | navigation or local | — | — | — | — |
| Credit Exception (secondary button) | navigation or local | — | — | — | — |
| Allocation Exception (secondary button) | navigation or local | — | — | — | — |
| Booking Limit Exception (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `PTR-032` Commercial Agreement Command Center: *Returns to the board's landing screen*; calls `approveBookingLimitCommercial`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The booking limits commercial configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the booking limits commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No booking limits commercial configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Inventory can be reserved for a specific partner; booking limits cap tickets per transaction or transactions per day, per partner or overall. *(client request · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-556)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-040` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-040`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 2
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 16: Works in Booking Limits, Commercial Exceptions & Approval → Control transaction limits and provide a governed mechanism for commercial exceptions.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-040?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Price Exception, Credit Exception, Allocation Exception, Booking Limit Exception.
- [ ] Every transition is wired: `PTR-032`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-041` Commercial Agreement 360°, Health & AI Review

**Give management a single consolidated view of the complete commercial relationship with a partner. Board 3 manages the day-to-day operational and financial relationship with active B2B, reseller and OTA partners. The three boards now form a clean lifecycle: Board 1 — Who is the partner? Onboarding → Organization → Users → Territory → Compliance → Permissions → Activation Board 2 — Under what commercial terms can they transact? Agreement → Rates → Commission → Credit → Security → Billing → Allocation → Limits Board 3 — What happens once the partner starts doing business? Orders → Reservations → Cancellations → Statements → Reconciliation → Commission Settlement → Disputes → Performance → Risk → AI Optimization A key principle for Board 3 is that it should provide a Partner Operations 360° without rebuilding functionality already owned by Orders, Finance, Ticketing, Payment or Channel Management.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/commercial-agreement-360-health-ai-review-ptr-041` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Start Renewal, Request Commercial Review, Change Terms, Request Credit Review, Create Exception, Suspend Commercial Access. Each needs attaching to the control it gates, or the screen needs the control.

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listCommercialAgreementHealth` (onLoad, Commercial Agreement 360°, Health & AI Review)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial agreement 360° list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial agreement 360° untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial agreement 360° yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial agreement 360° are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Partner documents (e.g. trade licence, VAT certificate) follow a review/accept/reject/resubmit flow; approval status runs lead > submitted > active > suspended; a partner 360 view consolidates profile, agreement and payment information in one view. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-550)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-041` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-041`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 2
- Flow F131 *B2B, Reseller & OTA Partner Management board 2: Commercial Agreement Command …*, step 18: Works in Commercial Agreement 360°, Health & AI Review → Give management a single consolidated view of the complete commercial relationship with a partner. Board 3 manages the day-to-day operational and financial relationship with active B2B, reseller and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-041?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P10 as a whole** (12: 0 open, 12 closed). Open first; a closed row says where it went on 30 September.

- **A89** Build corporate/B2B self-service onboarding (trade licence & VAT upload → approve/reject → rate setup → credential issuance) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker)*
- **A135** Manage group, family and corporate/allocation ticket types inside the unified product screen rather than separate screens *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 25 Aug 2026 · workshop tracker)*
- **A170** Build family and corporate wallets (parent-funded child wristbands, per-member allowances, parent-only top-up, guest self-service family setup, department-segregated corporate funds, bidirectional transfer as a venue … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker)*
- **A178** Build B2B partner management (configurable profiles, onboarding workflow, sub-agents, territory and distribution rights, venue association with per-venue pricing, document compliance repository, action permissions … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A179** Support all three B2B/OTA routes (direct portal · bidirectional API with external OTAs · bulk pre-generated QR CSV for non-integrating partners), with an existing OTA integration reusable by configuration *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A180** Build B2B agreements & payment models (tiered volume discounts, commission rates, credit limit vs. prepaid wallet vs. card, partner-reserved inventory, booking limits) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A181** Build B2B settlement & reconciliation (per-partner operations dashboard, statements of account, exception management for unsettled transfers, dispute handling, AI partner performance view) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A184** Build group, school and corporate sales (inquiry dashboard, configurable customer categories, package builder against live inventory and resources, versioned quotations with discount approval, conversion to confirmed … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A208** Check amendments and cancellations against policy before allowing refund, cancellation or reschedule, track booking financial status, and support deposits for school and corporate bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 1 Sep 2026 · workshop tracker)*
- **A231** Build the live operations dashboard and group/B2B admission profile (real-time attendance by venue and gate, gate status, turnstile mode reconfigurable through the day, entry stats by category) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker)*
- **C35** Share the wallet-configuration reference documentation (foundation, funding, stored value, family/corporate, gift cards, payments, fraud/risk, API) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 27 Aug 2026 · workshop tracker)*
- **C44** Confirm how B2B/reseller-issued tickets are handled under a fully-dynamic-QR event policy *(Qossai · Pending → 30 Sep: Closed, Moved to T10 · 2 Sep 2026 · workshop tracker)*

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

### Across P10 Partner Web

- **Open question.** Qossai proposes a POS-style interface for high-volume resellers (hotels, travel agents) instead of a B2C-style site with login: assigned tickets and partner prices after login, optional cash drawer, sent-ticket history and resend, balance view. Chinmay wireframes both options; decide after review. *(open · MoM 29 Sep 2026, 3. B2B / reseller portal · DI-1023)*
- Qossai: partners may use the TICVAI B2B portal directly with a white-label-style B2B credential (similar to B2C), or integrate via API (preferred for OTAs such as Ticketmaster, Platinum List, BookMyShow). *(agreed · MoM 31 Aug 2026, 4.3 Clarified (integration models) · DI-552)*
- Partner access controls define which actions a partner may perform (e.g. refund, reschedule); the partner portal should only offer the actions granted. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-551)*
- Allam: B2B Portal option — partners without their own platform use a TICVAI B2B portal structured like the B2C store but behind login credentials, showing pre-configured partner pricing and products, with commission tracked the same way. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-134)*
- The POS/tablet application carries TICVAI's own branding and UI direction; the B2C and B2B mobile applications are white-label by design. *(agreed · MoM 31 Jul 2026, 15. Monday UI/UX Session Planning · DI-084)*
- Qossai: the target product is a white-label application supporting both B2C and B2B mobile use cases, built around three to four distinct flows (e.g. admission ticket flow, seat assignment flow). *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-056)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

**12 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{

}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{

}
```
