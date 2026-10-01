# WS57 — Sales Channel Management board 1

**10 screens · 11 operations · 21 schemas · 2 permissions**

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
  `PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `ADM-258` | Sales Channel Command Center | B–D | 0 | 24 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-259` | Channel Creation & Profile Configuration | B–D | 14 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-260` | Product & Catalogue Assignment | B–D | 0 | 20 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-261` | Channel Pricing & Commercial Profile Assignment | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-262` | Inventory, Capacity & Channel Allocation | B–D | 0 | 14 | 6 | 0 | 2 | 4 | — | notStarted (generated) |
| `ADM-263` | Channel Sales Schedule & Availability Windows | B–D | 46 | 140 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-264` | Customer & Eligibility Rules by Channel | B–D | 51 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-265` | Channel Sales Rules, Limits & Restrictions | B–D | 63 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-266` | Channel Fees, Payment & Fulfillment Configuration | B–D | 11 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-267` | Channel Publication, Readiness & AI Validation | B–D | 1 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-261, ADM-262 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-258` Sales Channel Command Center

**Provide administrators with one centralized view of every TICVAI sales channel and its current operational/configuration status.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each record should display) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/sales-channel-command-center-adm-258` |

**Known gaps.** **The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: POS, Mobile POS, Flying POS, Call Center, API, Partner Portal, Third-Party Channel, Custom Channel. Each …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel type | select | — | B2C web · B2C mobile app · POS · Mobile POS · Flying POS · Kiosk · Call centre · B2B portal · Reseller · Ota · API · Partner portal … | `listSaleChannel` ?channelType |
| Status | select | — | Draft · Configuration · Validation · Approved · Scheduled · Active · Suspended · Disabled · Archived | `listSaleChannel` ?status |
| Venue | text field | — | — | `listSaleChannel` ?venue |
| Brand | text field | — | — | `listSaleChannel` ?brand |
| Search | text field | — | — | `listSaleChannel` ?search |
| Channel | text field | — | — | `listChannelSaleSchedule` ?channel |
| Product | text field | — | — | `listChannelSaleSchedule` ?product |
| Event | text field | — | — | `listChannelSaleSchedule` ?event |
| From | date picker | — | — | `listChannelSaleSchedule` ?from |
| To | date picker | — | — | `listChannelSaleSchedule` ?to |
| Channel | text field | — | — | `listChannelSaleRule` ?channel |
| Product | text field | — | — | `listChannelSaleRule` ?product |
| Rule level | radio group | — | Platform · Product · Channel · Contract partner | `listChannelSaleRule` ?ruleLevel |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Total Channels** (metric tile)

**Active Channels** (metric tile)

**Inactive Channels** (metric tile)

**Channels in Draft** (metric tile)

**Channels With Errors** (metric tile)

**Products Distributed** (metric tile)

**Channels With Capacity Alerts** (metric tile)

**Channels With Pricing Issues** (metric tile)

**Scheduled Activations** (metric tile)

**Scheduled Deactivations** (metric tile)

**Every sales channel** (data table, from `listSaleChannel`)

| Shows | Format | Notes |
|---|---|---|
| Channel | text | Channel ID |
| Channel name | text | Channel Name |
| Channel type | chip: B2C web, B2C mobile app, POS, Mobile POS, Flying POS, Kiosk… | Channel Type (pack p.3-4 Channel Types). |
| Brand | text | Brand |
| Venue scope | text | Venue/Scope: the channel's operational scope level and the name of the scoped item (e.g. |
| Products | 1,234 | Products: number of products assigned to the channel |
| Currency | text | Currency: ISO 4217 code |
| Status | text | Status: draft, configuration, validation, approved, scheduled, active, suspended, disabled or archived (the pack's suggested lifecycle, p.5) |
| Publication status | text | Publication Status: unpublished, pendingApproval, scheduled or published (decided 29 September, readiness close-out) |
| Integration status | text | Integration Status: notRequired, notConfigured, connected, degraded or offline (decided 29 September, readiness close-out) |
| Last updated | 1 Oct 2026, 14:30 | Last Updated |
| Owner | text | Owner: the channel's commercial owner (user ID) |

**The selected sales channel** (detail panel): The pack groups this record's detail under its own headings: “Channel Readiness Alert”.

| Shows | Format | Notes |
|---|---|---|
| Channel | text | Channel ID |
| Channel name | text | Channel Name |
| Channel type | chip: B2C web, B2C mobile app, POS, Mobile POS, Flying POS, Kiosk… | Channel Type (pack p.3-4 Channel Types). |
| Brand | text | Brand |
| Venue scope | text | Venue/Scope: the channel's operational scope level and the name of the scoped item (e.g. |
| Products | 1,234 | Products: number of products assigned to the channel |
| Currency | text | Currency: ISO 4217 code |
| Status | text | Status: draft, configuration, validation, approved, scheduled, active, suspended, disabled or archived (the pack's suggested lifecycle, p.5) |
| Publication status | text | Publication Status: unpublished, pendingApproval, scheduled or published (decided 29 September, readiness close-out) |
| Integration status | text | Integration Status: notRequired, notConfigured, connected, degraded or offline (decided 29 September, readiness close-out) |
| Last updated | 1 Oct 2026, 14:30 | Last Updated |
| Owner | text | Owner: the channel's commercial owner (user ID) |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Create Channel, Edit, Duplicate, Activate, Suspend, Disable, View Products, View Capacity, Validate, Schedule, Open Analytics. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| POS (primary button) | navigation or local | — | — | — | — |
| Mobile POS (secondary button) | navigation or local | — | — | — | — |
| Flying POS (secondary button) | navigation or local | — | — | — | — |
| Call Center (secondary button) | navigation or local | — | — | — | — |
| API (secondary button) | navigation or local | — | — | — | — |
| Partner Portal (secondary button) | navigation or local | — | — | — | — |
| Third-Party Channel (secondary button) | navigation or local | — | — | — | — |
| Custom Channel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listSaleChannel` (onLoad, Sales Channel Command Center); `listChannelSaleSchedule` (onLoad, Channel Sales Schedule & Availability Windows); `listChannelSaleRule` (onLoad, Channel Sales Rules, Limits & Restrictions)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-259` Channel Creation & Profile Configuration: *Works in Channel Creation & Profile Configuration*; calls `listSaleChannel`
- → `ADM-260` Product & Catalogue Assignment: *Works in Product & Catalogue Assignment*; calls `listSaleChannel`
- → `ADM-261` Channel Pricing & Commercial Profile Assignment: *Works in Channel Pricing & Commercial Profile Assignment*; calls `listSaleChannel`
- → `ADM-262` Inventory, Capacity & Channel Allocation: *Works in Inventory, Capacity & Channel Allocation*; calls `listSaleChannel`
- → `ADM-266` Channel Fees, Payment & Fulfillment Configuration: *Works in Channel Fees, Payment & Fulfillment Configuration*; calls `listSaleChannel`
- → `ADM-267` Channel Publication, Readiness & AI Validation: *Works in Channel Publication, Readiness & AI Validation*; calls `listSaleChannel`
- → `ADM-263` Channel Sales Schedule & Availability Windows: *Works in Channel Sales Schedule & Availability Windows*; carries `ruleId`; calls `listSaleChannel`
- → `ADM-264` Customer & Eligibility Rules by Channel: *Works in Customer & Eligibility Rules by Channel*; carries `ruleId`; calls `listSaleChannel`
- → `ADM-265` Channel Sales Rules, Limits & Restrictions: *Works in Channel Sales Rules, Limits & Restrictions*; carries `ruleId`; calls `listSaleChannel`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sales channel list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sales channel untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sales channel yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the sales channel are still there. The pack's own statuses are → Disabled → Archived — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listSaleChannel` → `PRODUCT_VIEW` (read) · staff
- `listChannelSaleSchedule` → `PRODUCT_VIEW` (read) · staff
- `listChannelSaleRule` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-258` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-258`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 1
- Flow F166 *Sales Channel Management board 1: Sales Channel Command Center*, step 1: Opens Sales Channel Command Center → Provide administrators with one centralized view of every TICVAI sales channel and its current operational/configuration status.
- Flow F166 *Sales Channel Management board 1: Sales Channel Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F166 *Sales Channel Management board 1: Sales Channel Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F166 *Sales Channel Management board 1: Sales Channel Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F166 *Sales Channel Management board 1: Sales Channel Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F166 *Sales Channel Management board 1: Sales Channel Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F166 *Sales Channel Management board 1: Sales Channel Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F166 *Sales Channel Management board 1: Sales Channel Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F166 branch at step 1 (expected): when Nothing has been set up on Sales Channel Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F166 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-258?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: POS, Mobile POS, Flying POS, Call Center, API, Partner Portal, Third-Party Channel, Custom Channel.
- [ ] Every transition is wired: `ADM-002`, `ADM-259`, `ADM-260`, `ADM-261`, `ADM-262`, `ADM-266`, `ADM-267`, `ADM-263`, `ADM-264`, `ADM-265`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-259` Channel Creation & Profile Configuration

**Create and define a sales channel before products and commercial rules are assigned.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/channel-creation-profile-configuration-adm-259` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Channel Name | select field | — | — | — | — | — | — |
| Channel Code | select field | — | — | — | — | — | — |
| Channel Type | select field | — | — | — | — | — | — |
| Internal Description | select field | — | — | — | — | — | — |
| Customer-Facing Name | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Brand | select field | — | — | — | — | — | — |
| Business Unit | select field | — | — | — | — | — | — |
| Country | select field | — | — | — | — | — | — |
| Market | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Time Zone | select field | — | — | — | — | — | — |
| Owner | select field | — | — | — | — | — | — |
| Responsible Department | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-258` Sales Channel Command Center: *Returns to the board's landing screen*; calls `createChannelProfile`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel creation profile configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel creation profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel creation profile configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `createChannelProfile` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Sales channels (onsite, B2C, B2B, kiosk) configured per venue; a product is available on all channels or restricted to some. Channel-specific pricing required, e.g. online cheaper than onsite/counter. *(agreed · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-580)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-259` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-259`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 1
- Flow F166 *Sales Channel Management board 1: Sales Channel Command Center*, step 2: Works in Channel Creation & Profile Configuration → Create and define a sales channel before products and commercial rules are assigned.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-259?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create.
- [ ] Every transition is wired: `ADM-258`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-260` Product & Catalogue Assignment

**Control exactly which products are available through each sales channel.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/product-catalogue-assignment-adm-260` |

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Assign Products, Remove Products, Disable, Copy Assignment, Import Assignment. Each needs an operation, or …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every product catalogue** (data table, from `setProductCatalogue`)

| Shows | Format | Notes |
|---|---|---|
| Product | text | Product ID |
| Product type | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | Product Type |
| Venue | text | Venue ID |
| Status | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Status: the product's own lifecycle state in Product Catalogue |
| Validity | text | Validity: the product's validity period as set in Product Catalogue, shown for reference |
| Channel status | text | Channel Status: enabled, disabled or scheduled on this channel (decided 29 September, readiness close-out) |
| Pricing status | text | Pricing Status: valid, missing or expired for this channel (from ADM-261) (decided 29 September, readiness close-out) |
| Capacity status | text | Capacity Status: allocated, sharedPool or none for this channel (from ADM-262) (decided 29 September, readiness close-out) |
| Effective from | 1 Oct 2026 | Effective From |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |

**The selected product catalogue** (detail panel): The pack groups this record's detail under its own headings: “Administrators can assign”, “Global Channel Catalogue”, “Venue Catalogue”, “For example”, “Important Architecture”, “This screen only determines”.

| Shows | Format | Notes |
|---|---|---|
| Product | text | Product ID |
| Product type | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | Product Type |
| Venue | text | Venue ID |
| Status | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Status: the product's own lifecycle state in Product Catalogue |
| Validity | text | Validity: the product's validity period as set in Product Catalogue, shown for reference |
| Channel status | text | Channel Status: enabled, disabled or scheduled on this channel (decided 29 September, readiness close-out) |
| Pricing status | text | Pricing Status: valid, missing or expired for this channel (from ADM-261) (decided 29 September, readiness close-out) |
| Capacity status | text | Capacity Status: allocated, sharedPool or none for this channel (from ADM-262) (decided 29 September, readiness close-out) |
| Effective from | 1 Oct 2026 | Effective From |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Assign Products (primary button) | navigation or local | — | — | — | — |
| Remove Products (destructive button) | navigation or local | — | — | — | — |
| Disable (destructive button) | navigation or local | — | — | — | — |
| Set Effective Dates (secondary button) | navigation or local | — | — | — | — |
| Copy Assignment (secondary button) | navigation or local | — | — | — | — |
| Import Assignment (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-258` Sales Channel Command Center: *Returns to the board's landing screen*; calls `setProductCatalogue`

**What opens over it**

- confirmDialog *Remove Products*: **Remove Products on a product catalogue is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *Disable*: **Disable on a product catalogue is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product catalogue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product catalogue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product catalogue yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product catalogue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setProductCatalogue` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-260` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-260`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 1
- Flow F166 *Sales Channel Management board 1: Sales Channel Command Center*, step 4: Works in Product & Catalogue Assignment → Control exactly which products are available through each sales channel.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-260?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Assign Products, Remove Products, Disable, Set Effective Dates, Copy Assignment, Import Assignment.
- [ ] Every transition is wired: `ADM-258`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-261` Channel Pricing & Commercial Profile Assignment

**Determine which pricing configuration a channel consumes.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/channel-pricing-commercial-profile-assignment-adm-261` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-258` Sales Channel Command Center: *Returns to the board's landing screen*; calls `setChannelPricingCommercial`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel pricing commercial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel pricing commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel pricing commercial yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the channel pricing commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setChannelPricingCommercial` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- UX reference: a competitor's pricing matrix that configures channel-and-variant pricing in one matrix view (e.g. adult/child x onsite/online/kiosk). Qossai: not to copy it, but match or improve on it. *(client request · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-582)*
- Sales channels (onsite, B2C, B2B, kiosk) configured per venue; a product is available on all channels or restricted to some. Channel-specific pricing required, e.g. online cheaper than onsite/counter. *(agreed · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-580)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-261` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-261`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 1
- Flow F166 *Sales Channel Management board 1: Sales Channel Command Center*, step 6: Works in Channel Pricing & Commercial Profile Assignment → Determine which pricing configuration a channel consumes.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-261?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `ADM-258`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-262` Inventory, Capacity & Channel Allocation

**Control how much product inventory or event capacity is available to each sales channel.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/inventory-capacity-channel-allocation-adm-262` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | text field | — | — | `listInventoryCapacityChannel` ?product |
| Event | text field | — | — | `listInventoryCapacityChannel` ?event |
| Channel | text field | — | — | `listInventoryCapacityChannel` ?channel |
| Venue | text field | — | — | `listInventoryCapacityChannel` ?venue |
| Allocation type | radio group | — | Shared pool · Dedicated · Percentage · Dynamic | `listInventoryCapacityChannel` ?allocationType |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every inventory capacity channel** (data table, from `listInventoryCapacityChannel`)

| Shows | Format | Notes |
|---|---|---|
| Allocated | 1,234 | Allocated |
| Sold | 1,234 | Sold |
| Held | 1,234 | Held |
| Remaining | 1,234 | Remaining |
| Utilization | 1,234.5 | Utilization %: sold plus held over allocated, 0-100 |
| Released | 1,234 | Released: units given back to the shared pool by a release rule |
| Returned | 1,234 | Returned: units returned manually |

**The selected inventory capacity channel** (detail panel): The pack groups this record's detail under its own headings: “Shared Pool”, “Dedicated Allocation”, “Percentage Allocation”, “Dynamic Allocation”.

| Shows | Format | Notes |
|---|---|---|
| Allocated | 1,234 | Allocated |
| Sold | 1,234 | Sold |
| Held | 1,234 | Held |
| Remaining | 1,234 | Remaining |
| Utilization | 1,234.5 | Utilization %: sold plus held over allocated, 0-100 |
| Released | 1,234 | Released: units given back to the shared pool by a release rule |
| Returned | 1,234 | Returned: units returned manually |

**Data it reads**: `listInventoryCapacityChannel` (onLoad, Inventory, Capacity & Channel Allocation)

**Where the user goes next**

- → `ADM-258` Sales Channel Command Center: *Returns to the board's landing screen*; calls `listInventoryCapacityChannel`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The inventory capacity channel list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the inventory capacity channel untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No inventory capacity channel yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the inventory capacity channel are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listInventoryCapacityChannel` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Inventory centralised or split per channel by percentage/quantity (e.g. 50% online / 50% onsite). Qossai: automatic migration rules, e.g. when B2C sells out pull a configured 20% from B2B, in the same configuration area. *(agreed · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-581)*
- Inventory pools split capacity by ticket type (e.g. 50% GA, 30% child, 20% senior) and/or sales channel (e.g. 50% online, 50% on-site), configurable at venue/event level, under a hierarchy global → attraction → product → variant → time slot. On cancel/refund/reschedule the business chooses whether capacity is released or held. *(agreed · MoM 25 Aug 2026, 4.6 Performances & Capacity Management; 4.11 UX Simplification & Distributed Inventory · DI-457)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-262` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-262`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 1
- Flow F166 *Sales Channel Management board 1: Sales Channel Command Center*, step 8: Works in Inventory, Capacity & Channel Allocation → Control how much product inventory or event capacity is available to each sales channel.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-262?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-258`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-263` Channel Sales Schedule & Availability Windows

**Control when each channel is permitted to sell.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `ruleId` (navigation) |
| Route | `/commercial/channel-sales-schedule-availability-windows-adm-263` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | text field | — | — | `listChannelSaleSchedule` ?channel |
| Product | text field | — | — | `listChannelSaleSchedule` ?product |
| Event | text field | — | — | `listChannelSaleSchedule` ?event |
| From | date picker | — | — | `listChannelSaleSchedule` ?from |
| To | date picker | — | — | `listChannelSaleSchedule` ?to |

**Form: Save channel sales rule** (modal, opened by *Save channel sales rule*; *Save channel sales rule* calls `setChannelSalesRule`, *Cancel* sends nothing)

**Collects what `setChannelSalesRule` sends before it is called.** Required: `id`, `scopePath`, `salesChannelId`, `ruleKind`, `isActive`. Optional: `productId`, `name`, `ruleLevel`, `overridesProductRule`, `effectiveFrom`, `effectiveTo`, `salesStartDate`, `salesStartTime`, `salesEndDate`, `salesEndTime`, `timeZone`, `daysOfWeek` and 31 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Sales channel `salesChannelId` | picker: choose a sales channel | required | — | — | shows names, sends the id | — | `setChannelSalesRule` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `setChannelSalesRule` body |
| Rule kind `ruleKind` | segmented control | required | — | Sales window · Sales limit · Eligibility | — | — | `setChannelSalesRule` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `setChannelSalesRule` body |
| Rule level `ruleLevel` | radio group | optional | Channel | Platform · Product · Channel · Contract partner | — | — | `setChannelSalesRule` body |
| Overrides product rule `overridesProductRule` | toggle | optional | off | — | — | — | `setChannelSalesRule` body |
| Effective from `effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setChannelSalesRule` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setChannelSalesRule` body |
| Is active `isActive` | toggle | required | on | — | — | — | `setChannelSalesRule` body |
| Sales start date `salesStartDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setChannelSalesRule` body |
| Sales start time `salesStartTime` | time picker | optional | — | — | HH:mm, 24-hour | — | `setChannelSalesRule` body |
| Sales end date `salesEndDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setChannelSalesRule` body |
| Sales end time `salesEndTime` | time picker | optional | — | — | HH:mm, 24-hour | — | `setChannelSalesRule` body |
| Time zone `timeZone` | text field | optional | — | max length 64 | — | — | `setChannelSalesRule` body |
| Days of week `daysOfWeek` | multi-select chips | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setChannelSalesRule` body |
| Hours of operation `hoursOfOperation` | key and value settings | optional | — | — | — | `[{opensAt, closesAt}]`. | `setChannelSalesRule` body |
| Blackout dates `blackoutDates` | list of values (chips) | optional | — | — | — | ISO dates. | `setChannelSalesRule` body |
| Event relative window `eventRelativeWindow` | key and value settings | optional | — | — | — | `{anchor, opensMinutesBefore, closesMinutesBefore}`. | `setChannelSalesRule` body |
| Minimum lead days `minimumLeadDays` | number field (days) | optional | — | min 0 | — | — | `setChannelSalesRule` body |
| Minimum quantity `minimumQuantity` | number field | optional | — | min 0 | — | — | `setChannelSalesRule` body |
| Maximum quantity `maximumQuantity` | number field | optional | — | min 1 | — | — | `setChannelSalesRule` body |
| Maximum per transaction `maximumPerTransaction` | number field | optional | — | min 1 | — | — | `setChannelSalesRule` body |
| Maximum per customer `maximumPerCustomer` | number field | optional | — | min 1 | — | — | `setChannelSalesRule` body |
| Maximum per day `maximumPerDay` | number field | optional | — | min 1 | — | — | `setChannelSalesRule` body |
| Maximum per event `maximumPerEvent` | number field | optional | — | min 1 | — | — | `setChannelSalesRule` body |
| Maximum per product `maximumPerProduct` | number field | optional | — | min 1 | — | — | `setChannelSalesRule` body |
| Is reservation permitted `isReservationPermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is hold permitted `isHoldPermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is payment link permitted `isPaymentLinkPermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is partial payment permitted `isPartialPaymentPermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is split payment permitted `isSplitPaymentPermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is discount permitted `isDiscountPermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is promo code permitted `isPromoCodePermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is exchange permitted `isExchangePermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is reschedule permitted `isReschedulePermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is upgrade permitted `isUpgradePermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Restrictions `restrictions` | multi-select chips | optional | — | No refunds · No cash payment · No complimentary · No manual discount · No same day sales · No seat changes | — | — | `setChannelSalesRule` body |
| Eligibility dimension `eligibilityDimension` | select | optional | — | Customer type · Membership · Loyalty tier · Country · Residency · Age · Corporate account · Partner · Customer segment · Promo eligibility · Authentication status · Purchase history … | — | — | `setChannelSalesRule` body |
| Eligibility operator `eligibilityOperator` | select | optional | — | Equals · Not equals · In · Not in · Greater than or equal · Less than or equal · Between | — | — | `setChannelSalesRule` body |
| Eligibility values `eligibilityValues` | list of values (chips) | optional | — | — | — | — | `setChannelSalesRule` body |
| Eligibility effect `eligibilityEffect` | segmented control | optional | — | Allow · Deny | — | — | `setChannelSalesRule` body |
| Is guest allowed `isGuestAllowed` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is login required `isLoginRequired` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is membership required `isMembershipRequired` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is corporate account required `isCorporateAccountRequired` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| … 1 more | | | | | | the rest are in `schemas.json` | `setChannelSalesRule` body |

Errors to draw in the form: 409 `ruleConflict`.; 422 `invalidRange` or `eligibilityIncomplete`.

#### Outputs: what the screen shows and produces

**Shown**

**Active selling periods** (metric tile, from `listChannelSaleSchedule`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Sales start date | 1 Oct 2026 | Sales Start Date |
| Sales start time | text | Sales Start Time, HH:MM local to timeZone |
| Sales end date | 1 Oct 2026 | Sales End Date |
| Sales end time | text | Sales End Time, HH:MM local to timeZone |
| Time zone | text | Time Zone: IANA name |
| Days of week | list or chips (count when long) | Days of Week the channel sells; empty means every day |
| Hours of operation | list or chips (count when long) | Hours of Operation: HH:MM ranges within each selling day |
| Opens at | text | — |
| Closes at | text | — |
| Blackout dates | list or chips (count when long) | Blackout Dates |
| Event relative windows | grouped details | Event-relative windows (pack p.11: B2C opens 90 days before, OTA closes 4 hours before, kiosk opens 2 hours before admission; MoM: onsite … |
| Anchor | chip: Event start, Admission start, Event end | — |
| Opens minutes before | 1,234 | — |
| Closes minutes before | 1,234 | — |
| Channel | text | Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258) |
| Product | text | Product ID the window applies to; empty for every product on the channel |
| Minimum lead days | 1,234 | Minimum days between purchase and visit: 0 allows same-day, 1 is the MoM's next-day minimum for online sales (MoM 31 Aug §4.11) |
| AI insights | list or chips (count when long) | Unusual schedule configurations AI detects (pack p.12, e.g. OTA closing after admission has ended). |
| Next cursor | text | — |

**Scheduled openings** (metric tile, from `listChannelSaleSchedule`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Sales start date | 1 Oct 2026 | Sales Start Date |
| Sales start time | text | Sales Start Time, HH:MM local to timeZone |
| Sales end date | 1 Oct 2026 | Sales End Date |
| Sales end time | text | Sales End Time, HH:MM local to timeZone |
| Time zone | text | Time Zone: IANA name |
| Days of week | list or chips (count when long) | Days of Week the channel sells; empty means every day |
| Hours of operation | list or chips (count when long) | Hours of Operation: HH:MM ranges within each selling day |
| Opens at | text | — |
| Closes at | text | — |
| Blackout dates | list or chips (count when long) | Blackout Dates |
| Event relative windows | grouped details | Event-relative windows (pack p.11: B2C opens 90 days before, OTA closes 4 hours before, kiosk opens 2 hours before admission; MoM: onsite … |
| Anchor | chip: Event start, Admission start, Event end | — |
| Opens minutes before | 1,234 | — |
| Closes minutes before | 1,234 | — |
| Channel | text | Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258) |
| Product | text | Product ID the window applies to; empty for every product on the channel |
| Minimum lead days | 1,234 | Minimum days between purchase and visit: 0 allows same-day, 1 is the MoM's next-day minimum for online sales (MoM 31 Aug §4.11) |
| AI insights | list or chips (count when long) | Unusual schedule configurations AI detects (pack p.12, e.g. OTA closing after admission has ended). |
| Next cursor | text | — |

**Scheduled closures** (metric tile, from `listChannelSaleSchedule`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Sales start date | 1 Oct 2026 | Sales Start Date |
| Sales start time | text | Sales Start Time, HH:MM local to timeZone |
| Sales end date | 1 Oct 2026 | Sales End Date |
| Sales end time | text | Sales End Time, HH:MM local to timeZone |
| Time zone | text | Time Zone: IANA name |
| Days of week | list or chips (count when long) | Days of Week the channel sells; empty means every day |
| Hours of operation | list or chips (count when long) | Hours of Operation: HH:MM ranges within each selling day |
| Opens at | text | — |
| Closes at | text | — |
| Blackout dates | list or chips (count when long) | Blackout Dates |
| Event relative windows | grouped details | Event-relative windows (pack p.11: B2C opens 90 days before, OTA closes 4 hours before, kiosk opens 2 hours before admission; MoM: onsite … |
| Anchor | chip: Event start, Admission start, Event end | — |
| Opens minutes before | 1,234 | — |
| Closes minutes before | 1,234 | — |
| Channel | text | Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258) |
| Product | text | Product ID the window applies to; empty for every product on the channel |
| Minimum lead days | 1,234 | Minimum days between purchase and visit: 0 allows same-day, 1 is the MoM's next-day minimum for online sales (MoM 31 Aug §4.11) |
| AI insights | list or chips (count when long) | Unusual schedule configurations AI detects (pack p.12, e.g. OTA closing after admission has ended). |
| Next cursor | text | — |

**Blackouts** (metric tile, from `listChannelSaleSchedule`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Sales start date | 1 Oct 2026 | Sales Start Date |
| Sales start time | text | Sales Start Time, HH:MM local to timeZone |
| Sales end date | 1 Oct 2026 | Sales End Date |
| Sales end time | text | Sales End Time, HH:MM local to timeZone |
| Time zone | text | Time Zone: IANA name |
| Days of week | list or chips (count when long) | Days of Week the channel sells; empty means every day |
| Hours of operation | list or chips (count when long) | Hours of Operation: HH:MM ranges within each selling day |
| Opens at | text | — |
| Closes at | text | — |
| Blackout dates | list or chips (count when long) | Blackout Dates |
| Event relative windows | grouped details | Event-relative windows (pack p.11: B2C opens 90 days before, OTA closes 4 hours before, kiosk opens 2 hours before admission; MoM: onsite … |
| Anchor | chip: Event start, Admission start, Event end | — |
| Opens minutes before | 1,234 | — |
| Closes minutes before | 1,234 | — |
| Channel | text | Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258) |
| Product | text | Product ID the window applies to; empty for every product on the channel |
| Minimum lead days | 1,234 | Minimum days between purchase and visit: 0 allows same-day, 1 is the MoM's next-day minimum for online sales (MoM 31 Aug §4.11) |
| AI insights | list or chips (count when long) | Unusual schedule configurations AI detects (pack p.12, e.g. OTA closing after admission has ended). |
| Next cursor | text | — |

**Conflicts** (metric tile, from `listChannelSaleSchedule`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Sales start date | 1 Oct 2026 | Sales Start Date |
| Sales start time | text | Sales Start Time, HH:MM local to timeZone |
| Sales end date | 1 Oct 2026 | Sales End Date |
| Sales end time | text | Sales End Time, HH:MM local to timeZone |
| Time zone | text | Time Zone: IANA name |
| Days of week | list or chips (count when long) | Days of Week the channel sells; empty means every day |
| Hours of operation | list or chips (count when long) | Hours of Operation: HH:MM ranges within each selling day |
| Opens at | text | — |
| Closes at | text | — |
| Blackout dates | list or chips (count when long) | Blackout Dates |
| Event relative windows | grouped details | Event-relative windows (pack p.11: B2C opens 90 days before, OTA closes 4 hours before, kiosk opens 2 hours before admission; MoM: onsite … |
| Anchor | chip: Event start, Admission start, Event end | — |
| Opens minutes before | 1,234 | — |
| Closes minutes before | 1,234 | — |
| Channel | text | Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258) |
| Product | text | Product ID the window applies to; empty for every product on the channel |
| Minimum lead days | 1,234 | Minimum days between purchase and visit: 0 allows same-day, 1 is the MoM's next-day minimum for online sales (MoM 31 Aug §4.11) |
| AI insights | list or chips (count when long) | Unusual schedule configurations AI detects (pack p.12, e.g. OTA closing after admission has ended). |
| Next cursor | text | — |

**Event dates** (metric tile, from `listChannelSaleSchedule`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Sales start date | 1 Oct 2026 | Sales Start Date |
| Sales start time | text | Sales Start Time, HH:MM local to timeZone |
| Sales end date | 1 Oct 2026 | Sales End Date |
| Sales end time | text | Sales End Time, HH:MM local to timeZone |
| Time zone | text | Time Zone: IANA name |
| Days of week | list or chips (count when long) | Days of Week the channel sells; empty means every day |
| Hours of operation | list or chips (count when long) | Hours of Operation: HH:MM ranges within each selling day |
| Opens at | text | — |
| Closes at | text | — |
| Blackout dates | list or chips (count when long) | Blackout Dates |
| Event relative windows | grouped details | Event-relative windows (pack p.11: B2C opens 90 days before, OTA closes 4 hours before, kiosk opens 2 hours before admission; MoM: onsite … |
| Anchor | chip: Event start, Admission start, Event end | — |
| Opens minutes before | 1,234 | — |
| Closes minutes before | 1,234 | — |
| Channel | text | Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258) |
| Product | text | Product ID the window applies to; empty for every product on the channel |
| Minimum lead days | 1,234 | Minimum days between purchase and visit: 0 allows same-day, 1 is the MoM's next-day minimum for online sales (MoM 31 Aug §4.11) |
| AI insights | list or chips (count when long) | Unusual schedule configurations AI detects (pack p.12, e.g. OTA closing after admission has ended). |
| Next cursor | text | — |

**Every channel sales schedule** (data table, from `listChannelSaleSchedule`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Sales start date | 1 Oct 2026 | Sales Start Date |
| Sales start time | text | Sales Start Time, HH:MM local to timeZone |
| Sales end date | 1 Oct 2026 | Sales End Date |
| Sales end time | text | Sales End Time, HH:MM local to timeZone |
| Time zone | text | Time Zone: IANA name |
| Days of week | list or chips (count when long) | Days of Week the channel sells; empty means every day |
| Hours of operation | list or chips (count when long) | Hours of Operation: HH:MM ranges within each selling day |
| Opens at | text | — |
| Closes at | text | — |
| Blackout dates | list or chips (count when long) | Blackout Dates |
| Event relative windows | grouped details | Event-relative windows (pack p.11: B2C opens 90 days before, OTA closes 4 hours before, kiosk opens 2 hours before admission; MoM: onsite … |
| Anchor | chip: Event start, Admission start, Event end | — |
| Opens minutes before | 1,234 | — |
| Closes minutes before | 1,234 | — |
| Channel | text | Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258) |
| Product | text | Product ID the window applies to; empty for every product on the channel |
| Minimum lead days | 1,234 | Minimum days between purchase and visit: 0 allows same-day, 1 is the MoM's next-day minimum for online sales (MoM 31 Aug §4.11) |
| AI insights | list or chips (count when long) | Unusual schedule configurations AI detects (pack p.12, e.g. OTA closing after admission has ended). |
| Next cursor | text | — |

**The selected channel sales schedule** (detail panel): The pack groups this record's detail under its own headings: “Channel-Specific Scheduling”, “Automated Actions”.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save channel sales rule (primary button) | `setChannelSalesRule` PUT `/channel-sales-rules/{ruleId}` | ChannelSalesRule | ChannelSalesRule | 409 `ruleConflict`.; 422 `invalidRange` or `eligibilityIncomplete`. | gated `PRODUCT_CONFIGURE`; opens modal first |

**Data it reads**: `listChannelSaleSchedule` (onLoad, Channel Sales Schedule & Availability Windows)

**Where the user goes next**

- → `ADM-258` Sales Channel Command Center: *Returns to the board's landing screen*; calls `listChannelSaleSchedule`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel sales schedule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel sales schedule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel sales schedule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the channel sales schedule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `ruleConflict`.; 422 `invalidRange` or `eligibilityIncomplete`. |

#### Permissions

- `listChannelSaleSchedule` → `PRODUCT_VIEW` (read) · staff
- `setChannelSalesRule` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Start/stop-sell per channel: e.g. a distant desert safari allows no same-day online booking (next day minimum), while onsite stays open to sell-out or a cutoff (e.g. 15 minutes before a timed show). Guest date/time pickers must reflect the channel's window. *(client request · MoM 31 Aug 2026, 4.11 Sales schedule & validity · DI-583)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-263` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-263`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 1
- Flow F166 *Sales Channel Management board 1: Sales Channel Command Center*, step 10: Works in Channel Sales Schedule & Availability Windows → Control when each channel is permitted to sell.

#### Acceptance for the design

- [ ] Every input above is drawn (46), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (140 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-263?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save channel sales rule.
- [ ] Every transition is wired: `ADM-258`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-264` Customer & Eligibility Rules by Channel

**Determine who is allowed to purchase through a particular channel.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `ruleId` (navigation) |
| Route | `/commercial/customer-eligibility-rules-by-channel-adm-264` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Guest allowed | select field | — | — | — | — | — | — |
| Login required | select field | — | — | — | — | — | — |
| Membership required | select field | — | — | — | — | — | — |
| Corporate account required | select field | — | — | — | — | — | — |
| Identity verification required | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | text field | — | — | `listCustomerEligibilityRule` ?channel |
| Product | text field | — | — | `listCustomerEligibilityRule` ?product |
| Dimension | select | — | Customer type · Membership · Loyalty tier · Country · Residency · Age · Corporate account · Partner · Customer segment · Promo eligibility · Authentication status · Purchase history … | `listCustomerEligibilityRule` ?dimension |

**Form: Save channel sales rule** (modal, opened by *Save channel sales rule*; *Save channel sales rule* calls `setChannelSalesRule`, *Cancel* sends nothing)

**Collects what `setChannelSalesRule` sends before it is called.** Required: `id`, `scopePath`, `salesChannelId`, `ruleKind`, `isActive`. Optional: `productId`, `name`, `ruleLevel`, `overridesProductRule`, `effectiveFrom`, `effectiveTo`, `salesStartDate`, `salesStartTime`, `salesEndDate`, `salesEndTime`, `timeZone`, `daysOfWeek` and 31 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Sales channel `salesChannelId` | picker: choose a sales channel | required | — | — | shows names, sends the id | — | `setChannelSalesRule` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `setChannelSalesRule` body |
| Rule kind `ruleKind` | segmented control | required | — | Sales window · Sales limit · Eligibility | — | — | `setChannelSalesRule` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `setChannelSalesRule` body |
| Rule level `ruleLevel` | radio group | optional | Channel | Platform · Product · Channel · Contract partner | — | — | `setChannelSalesRule` body |
| Overrides product rule `overridesProductRule` | toggle | optional | off | — | — | — | `setChannelSalesRule` body |
| Effective from `effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setChannelSalesRule` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setChannelSalesRule` body |
| Is active `isActive` | toggle | required | on | — | — | — | `setChannelSalesRule` body |
| Sales start date `salesStartDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setChannelSalesRule` body |
| Sales start time `salesStartTime` | time picker | optional | — | — | HH:mm, 24-hour | — | `setChannelSalesRule` body |
| Sales end date `salesEndDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setChannelSalesRule` body |
| Sales end time `salesEndTime` | time picker | optional | — | — | HH:mm, 24-hour | — | `setChannelSalesRule` body |
| Time zone `timeZone` | text field | optional | — | max length 64 | — | — | `setChannelSalesRule` body |
| Days of week `daysOfWeek` | multi-select chips | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setChannelSalesRule` body |
| Hours of operation `hoursOfOperation` | key and value settings | optional | — | — | — | `[{opensAt, closesAt}]`. | `setChannelSalesRule` body |
| Blackout dates `blackoutDates` | list of values (chips) | optional | — | — | — | ISO dates. | `setChannelSalesRule` body |
| Event relative window `eventRelativeWindow` | key and value settings | optional | — | — | — | `{anchor, opensMinutesBefore, closesMinutesBefore}`. | `setChannelSalesRule` body |
| Minimum lead days `minimumLeadDays` | number field (days) | optional | — | min 0 | — | — | `setChannelSalesRule` body |
| Minimum quantity `minimumQuantity` | number field | optional | — | min 0 | — | — | `setChannelSalesRule` body |
| Maximum quantity `maximumQuantity` | number field | optional | — | min 1 | — | — | `setChannelSalesRule` body |
| Maximum per transaction `maximumPerTransaction` | number field | optional | — | min 1 | — | — | `setChannelSalesRule` body |
| Maximum per customer `maximumPerCustomer` | number field | optional | — | min 1 | — | — | `setChannelSalesRule` body |
| Maximum per day `maximumPerDay` | number field | optional | — | min 1 | — | — | `setChannelSalesRule` body |
| Maximum per event `maximumPerEvent` | number field | optional | — | min 1 | — | — | `setChannelSalesRule` body |
| Maximum per product `maximumPerProduct` | number field | optional | — | min 1 | — | — | `setChannelSalesRule` body |
| Is reservation permitted `isReservationPermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is hold permitted `isHoldPermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is payment link permitted `isPaymentLinkPermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is partial payment permitted `isPartialPaymentPermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is split payment permitted `isSplitPaymentPermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is discount permitted `isDiscountPermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is promo code permitted `isPromoCodePermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is exchange permitted `isExchangePermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is reschedule permitted `isReschedulePermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is upgrade permitted `isUpgradePermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Restrictions `restrictions` | multi-select chips | optional | — | No refunds · No cash payment · No complimentary · No manual discount · No same day sales · No seat changes | — | — | `setChannelSalesRule` body |
| Eligibility dimension `eligibilityDimension` | select | optional | — | Customer type · Membership · Loyalty tier · Country · Residency · Age · Corporate account · Partner · Customer segment · Promo eligibility · Authentication status · Purchase history … | — | — | `setChannelSalesRule` body |
| Eligibility operator `eligibilityOperator` | select | optional | — | Equals · Not equals · In · Not in · Greater than or equal · Less than or equal · Between | — | — | `setChannelSalesRule` body |
| Eligibility values `eligibilityValues` | list of values (chips) | optional | — | — | — | — | `setChannelSalesRule` body |
| Eligibility effect `eligibilityEffect` | segmented control | optional | — | Allow · Deny | — | — | `setChannelSalesRule` body |
| Is guest allowed `isGuestAllowed` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is login required `isLoginRequired` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is membership required `isMembershipRequired` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is corporate account required `isCorporateAccountRequired` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| … 1 more | | | | | | the rest are in `schemas.json` | `setChannelSalesRule` body |

Errors to draw in the form: 409 `ruleConflict`.; 422 `invalidRange` or `eligibilityIncomplete`.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save channel sales rule (primary button) | `setChannelSalesRule` PUT `/channel-sales-rules/{ruleId}` | ChannelSalesRule | ChannelSalesRule | 409 `ruleConflict`.; 422 `invalidRange` or `eligibilityIncomplete`. | gated `PRODUCT_CONFIGURE`; opens modal first |

**Data it reads**: `listCustomerEligibilityRule` (onLoad, Customer & Eligibility Rules by Channel)

**Where the user goes next**

- → `ADM-258` Sales Channel Command Center: *Returns to the board's landing screen*; calls `listCustomerEligibilityRule`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer eligibility rules configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer eligibility rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer eligibility rules configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `ruleConflict`.; 422 `invalidRange` or `eligibilityIncomplete`. |

#### Permissions

- `listCustomerEligibilityRule` → `PRODUCT_VIEW` (read) · staff
- `setChannelSalesRule` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-264` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-264`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 1
- Flow F166 *Sales Channel Management board 1: Sales Channel Command Center*, step 12: Works in Customer & Eligibility Rules by Channel → Determine who is allowed to purchase through a particular channel.

#### Acceptance for the design

- [ ] Every input above is drawn (51), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-264?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save channel sales rule.
- [ ] Every transition is wired: `ADM-258`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-265` Channel Sales Rules, Limits & Restrictions

**Configure operational restrictions that apply specifically to a sales channel.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `ruleId` (navigation) |
| Route | `/commercial/channel-sales-rules-limits-restrictions-adm-265` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Minimum Quantity | select field | — | — | — | — | — | — |
| Maximum Quantity | select field | — | — | — | — | — | — |
| Maximum Per Transaction | select field | — | — | — | — | — | — |
| Maximum Per Customer | select field | — | — | — | — | — | — |
| Maximum Per Day | select field | — | — | — | — | — | — |
| Maximum Per Event | select field | — | — | — | — | — | — |
| Maximum Per Product | select field | — | — | — | — | — | — |
| Reservation permitted | select field | — | — | — | — | — | — |
| Hold permitted | select field | — | — | — | — | — | — |
| Payment link permitted | select field | — | — | — | — | — | — |
| Partial payment permitted | select field | — | — | — | — | — | — |
| Split payment permitted | select field | — | — | — | — | — | — |
| Discount permitted | select field | — | — | — | — | — | — |
| Promo code permitted | select field | — | — | — | — | — | — |
| Upgrade permitted | select field | — | — | — | — | — | — |
| Exchange permitted | select field | — | — | — | — | — | — |
| Reschedule permitted | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | text field | — | — | `listChannelSaleRule` ?channel |
| Product | text field | — | — | `listChannelSaleRule` ?product |
| Rule level | radio group | — | Platform · Product · Channel · Contract partner | `listChannelSaleRule` ?ruleLevel |

**Form: Save channel sales rule** (modal, opened by *Save channel sales rule*; *Save channel sales rule* calls `setChannelSalesRule`, *Cancel* sends nothing)

**Collects what `setChannelSalesRule` sends before it is called.** Required: `id`, `scopePath`, `salesChannelId`, `ruleKind`, `isActive`. Optional: `productId`, `name`, `ruleLevel`, `overridesProductRule`, `effectiveFrom`, `effectiveTo`, `salesStartDate`, `salesStartTime`, `salesEndDate`, `salesEndTime`, `timeZone`, `daysOfWeek` and 31 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Sales channel `salesChannelId` | picker: choose a sales channel | required | — | — | shows names, sends the id | — | `setChannelSalesRule` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `setChannelSalesRule` body |
| Rule kind `ruleKind` | segmented control | required | — | Sales window · Sales limit · Eligibility | — | — | `setChannelSalesRule` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `setChannelSalesRule` body |
| Rule level `ruleLevel` | radio group | optional | Channel | Platform · Product · Channel · Contract partner | — | — | `setChannelSalesRule` body |
| Overrides product rule `overridesProductRule` | toggle | optional | off | — | — | — | `setChannelSalesRule` body |
| Effective from `effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setChannelSalesRule` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setChannelSalesRule` body |
| Is active `isActive` | toggle | required | on | — | — | — | `setChannelSalesRule` body |
| Sales start date `salesStartDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setChannelSalesRule` body |
| Sales start time `salesStartTime` | time picker | optional | — | — | HH:mm, 24-hour | — | `setChannelSalesRule` body |
| Sales end date `salesEndDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setChannelSalesRule` body |
| Sales end time `salesEndTime` | time picker | optional | — | — | HH:mm, 24-hour | — | `setChannelSalesRule` body |
| Time zone `timeZone` | text field | optional | — | max length 64 | — | — | `setChannelSalesRule` body |
| Days of week `daysOfWeek` | multi-select chips | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setChannelSalesRule` body |
| Hours of operation `hoursOfOperation` | key and value settings | optional | — | — | — | `[{opensAt, closesAt}]`. | `setChannelSalesRule` body |
| Blackout dates `blackoutDates` | list of values (chips) | optional | — | — | — | ISO dates. | `setChannelSalesRule` body |
| Event relative window `eventRelativeWindow` | key and value settings | optional | — | — | — | `{anchor, opensMinutesBefore, closesMinutesBefore}`. | `setChannelSalesRule` body |
| Minimum lead days `minimumLeadDays` | number field (days) | optional | — | min 0 | — | — | `setChannelSalesRule` body |
| Minimum quantity `minimumQuantity` | number field | optional | — | min 0 | — | — | `setChannelSalesRule` body |
| Maximum quantity `maximumQuantity` | number field | optional | — | min 1 | — | — | `setChannelSalesRule` body |
| Maximum per transaction `maximumPerTransaction` | number field | optional | — | min 1 | — | — | `setChannelSalesRule` body |
| Maximum per customer `maximumPerCustomer` | number field | optional | — | min 1 | — | — | `setChannelSalesRule` body |
| Maximum per day `maximumPerDay` | number field | optional | — | min 1 | — | — | `setChannelSalesRule` body |
| Maximum per event `maximumPerEvent` | number field | optional | — | min 1 | — | — | `setChannelSalesRule` body |
| Maximum per product `maximumPerProduct` | number field | optional | — | min 1 | — | — | `setChannelSalesRule` body |
| Is reservation permitted `isReservationPermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is hold permitted `isHoldPermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is payment link permitted `isPaymentLinkPermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is partial payment permitted `isPartialPaymentPermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is split payment permitted `isSplitPaymentPermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is discount permitted `isDiscountPermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is promo code permitted `isPromoCodePermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is exchange permitted `isExchangePermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is reschedule permitted `isReschedulePermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is upgrade permitted `isUpgradePermitted` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Restrictions `restrictions` | multi-select chips | optional | — | No refunds · No cash payment · No complimentary · No manual discount · No same day sales · No seat changes | — | — | `setChannelSalesRule` body |
| Eligibility dimension `eligibilityDimension` | select | optional | — | Customer type · Membership · Loyalty tier · Country · Residency · Age · Corporate account · Partner · Customer segment · Promo eligibility · Authentication status · Purchase history … | — | — | `setChannelSalesRule` body |
| Eligibility operator `eligibilityOperator` | select | optional | — | Equals · Not equals · In · Not in · Greater than or equal · Less than or equal · Between | — | — | `setChannelSalesRule` body |
| Eligibility values `eligibilityValues` | list of values (chips) | optional | — | — | — | — | `setChannelSalesRule` body |
| Eligibility effect `eligibilityEffect` | segmented control | optional | — | Allow · Deny | — | — | `setChannelSalesRule` body |
| Is guest allowed `isGuestAllowed` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is login required `isLoginRequired` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is membership required `isMembershipRequired` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| Is corporate account required `isCorporateAccountRequired` | toggle | optional | — | — | — | — | `setChannelSalesRule` body |
| … 1 more | | | | | | the rest are in `schemas.json` | `setChannelSalesRule` body |

Errors to draw in the form: 409 `ruleConflict`.; 422 `invalidRange` or `eligibilityIncomplete`.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save channel sales rule (primary button) | `setChannelSalesRule` PUT `/channel-sales-rules/{ruleId}` | ChannelSalesRule | ChannelSalesRule | 409 `ruleConflict`.; 422 `invalidRange` or `eligibilityIncomplete`. | gated `PRODUCT_CONFIGURE`; opens modal first |

**Data it reads**: `listChannelSaleRule` (onLoad, Channel Sales Rules, Limits & Restrictions)

**Where the user goes next**

- → `ADM-258` Sales Channel Command Center: *Returns to the board's landing screen*; calls `listChannelSaleRule`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel sales rules configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel sales rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel sales rules configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `ruleConflict`.; 422 `invalidRange` or `eligibilityIncomplete`. |

#### Permissions

- `listChannelSaleRule` → `PRODUCT_VIEW` (read) · staff
- `setChannelSalesRule` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-265` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-265`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 1
- Flow F166 *Sales Channel Management board 1: Sales Channel Command Center*, step 14: Works in Channel Sales Rules, Limits & Restrictions → Configure operational restrictions that apply specifically to a sales channel.

#### Acceptance for the design

- [ ] Every input above is drawn (63), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-265?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save channel sales rule.
- [ ] Every transition is wired: `ADM-258`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-266` Channel Fees, Payment & Fulfillment Configuration

**Define the commercial and fulfillment behavior associated with each channel.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/channel-fees-payment-fulfillment-configuration-adm-266` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Digital Ticket | select field | — | — | — | — | — | — |
| Email | select field | — | — | — | — | — | — |
| Mobile App | select field | — | — | — | — | — | — |
| Apple/Google Wallet | select field | — | — | — | — | — | — |
| Print at Home | select field | — | — | — | — | — | — |
| POS Print | select field | — | — | — | — | — | — |
| Kiosk Print | select field | — | — | — | — | — | — |
| RFID | select field | — | — | — | — | — | — |
| NFC | select field | — | — | — | — | — | — |
| Wristband | select field | — | — | — | — | — | — |
| Collection | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-258` Sales Channel Command Center: *Returns to the board's landing screen*; calls `setChannelFeePayment`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel fees payment configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel fees payment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel fees payment configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setChannelFeePayment` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-266` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-266`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 1
- Flow F166 *Sales Channel Management board 1: Sales Channel Command Center*, step 16: Works in Channel Fees, Payment & Fulfillment Configuration → Define the commercial and fulfillment behavior associated with each channel.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-266?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-258`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-267` Channel Publication, Readiness & AI Validation

**Perform final validation before a sales channel or channel/product configuration becomes commercially active. Board 2 manages the live operational layer of TICVAI's sales-channel ecosystem after channels have been configured and activated in Board 1.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration works) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/channel-publication-readiness-ai-validation-adm-267` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| 4.1.1 Channel Publication, Readiness & AI | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Validate, Preview, Submit for Approval, Schedule Activation, Activate, Return for Changes, Suspend. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish (primary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel publication readiness configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel publication readiness untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel publication readiness configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `publishChannelReadinessValidation` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-267` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-267`
- Workshop pack: Sales_Channel_Management_Reference.pdf board 1
- Flow F166 *Sales Channel Management board 1: Sales Channel Command Center*, step 18: Works in Channel Publication, Readiness & AI Validation → Perform final validation before a sales channel or channel/product configuration becomes commercially active. Board 2 manages the live operational layer of TICVAI's sales-channel ecosystem after …

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-267?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish, What publishing changes.
- [ ] No transition is declared; back returns where the user came from.
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

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createChannelProfile": {"method":"POST","path":"/channel-profile","contract":"catalogue","summary":"Channel Creation & Profile Configuration","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ChannelCreationProfileConfigurationInput","responds":"ChannelCreationProfileConfigurationView"},
"listChannelSaleRule": {"method":"GET","path":"/channel-sale-rule","contract":"catalogue","summary":"Channel Sales Rules, Limits & Restrictions","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"ruleLevel","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listChannelSaleSchedule": {"method":"GET","path":"/channel-sale-schedule","contract":"catalogue","summary":"Channel Sales Schedule & Availability Windows","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCustomerEligibilityRule": {"method":"GET","path":"/customer-eligibility-rule","contract":"catalogue","summary":"Customer & Eligibility Rules by Channel","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"dimension","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listInventoryCapacityChannel": {"method":"GET","path":"/inventory-capacity-channel","contract":"catalogue","summary":"Inventory, Capacity & Channel Allocation","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"product","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"allocationType","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSaleChannel": {"method":"GET","path":"/sale-channel","contract":"catalogue","summary":"Sales Channel Command Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channelType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"brand","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"publishChannelReadinessValidation": {"method":"PUT","path":"/channel-readiness-validation","contract":"catalogue","summary":"Channel Publication, Readiness & AI Validation","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ChannelPublicationReadinessAiValidationInput","responds":"ChannelPublicationReadinessAiValidationView"},
"setChannelFeePayment": {"method":"PUT","path":"/channel-fee-payment","contract":"catalogue","summary":"Channel Fees, Payment & Fulfillment Configuration","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ChannelFeesPaymentFulfillmentConfigurationInput","responds":"ChannelFeesPaymentFulfillmentConfigurationView"},
"setChannelPricingCommercial": {"method":"PUT","path":"/channel-pricing-commercial","contract":"catalogue","summary":"Channel Pricing & Commercial Profile Assignment","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ChannelPricingCommercialProfileAssignmentInput","responds":"ChannelPricingCommercialProfileAssignmentView"},
"setChannelSalesRule": {"method":"PUT","path":"/channel-sales-rules/{ruleId}","contract":"catalogue","summary":"Create or replace a channel sales window, limit or eligibility rule","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ChannelSalesRule","responds":"ChannelSalesRule"},
"setProductCatalogue": {"method":"PUT","path":"/product-catalogue","contract":"catalogue","summary":"Product & Catalogue Assignment","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ProductCatalogueAssignmentInput","responds":"ProductCatalogueAssignmentView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ChannelCreationProfileConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Channel Creation & Profile Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"channelName":{"type":"string","description":"Channel Name (internal)","maxLength":120},"channelCode":{"type":"string","description":"Channel Code: unique within the tenant, 2-20 upper-case letters, digits or hyphens (decided 29 September, readiness close-out)","pattern":"^[A-Z0-9-]{2,20}$"},"channelType":{"type":"string","enum":["b2cWeb","b2cMobileApp","pos","mobilePos","flyingPos","kiosk","callCentre","b2bPortal","reseller","ota","api","partnerPortal","marketplace","thirdPartyChannel","customChannel"],"description":"Channel Type (pack p.3-4 Channel Types). The type decides which configuration applies (p.6); each type reports under one SalesChannel value (see salesChannel)"},"internalDescription":{"type":"string","description":"Internal Description"},"customerFacingName":{"type":"string","description":"Customer-Facing Name","maxLength":120},"brand":{"type":"string","description":"Brand ID"},"businessUnit":{"type":"string","description":"Business Unit ID"},"country":{"type":"string","description":"Country: ISO 3166-1 alpha-2","pattern":"^[A-Z]{2}$"},"market":{"type":"string","description":"Market (a configured market code)"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"timeZone":{"type":"string","description":"Time Zone: IANA name, e.g. Asia/Dubai"},"owner":{"type":"string","description":"Owner (user ID)"},"responsibleDepartment":{"type":"string","description":"Responsible Department"},"venue":{"type":"string","description":"Venue ID: required for the POS types (pack p.6) and when scopeLevel is venue","nullable":true},"workstationGroups":{"type":"array","items":{"type":"string"},"description":"Workstation groups (IDs) that may sell on a POS-type channel (pack p.6)"},"cashierAccess":{"type":"array","items":{"type":"string"},"description":"Cashier access: role IDs allowed to sell on a POS-type channel (pack p.6)"},"webstore":{"type":"string","description":"Webstore ID for a B2C-type channel (pack p.6)","nullable":true},"domainBrand":{"type":"string","description":"Domain/brand: the storefront domain for a B2C-type channel (pack p.6)","nullable":true},"digitalCustomerJourney":{"type":"string","description":"Digital customer journey: the checkout journey template ID for a B2C-type channel (pack p.6)","nullable":true},"partner":{"type":"string","description":"Partner ID for an OTA, reseller or partner channel (pack p.6); the partner record lives in B2B/OTA","nullable":true},"apiConnection":{"type":"string","description":"API connection: the connector ID from ADM-269 for an OTA/API channel (pack p.6); the external platform is named as data on the connector","nullable":true},"commercialOwner":{"type":"string","description":"Commercial Owner (user ID)"},"operationalOwner":{"type":"string","description":"Operational Owner (user ID)"},"technicalOwner":{"type":"string","description":"Technical Owner (user ID)"},"financeOwner":{"type":"string","description":"Finance Owner (user ID)"},"scopeLevel":{"type":"string","enum":["global","country","region","venue","attraction","event","location","businessUnit"],"description":"Operational Scope level (pack p.6)"},"scopeId":{"type":"string","description":"ID of the scoped item (country code, region, venue, attraction, event, location or business unit); empty for global","nullable":true},"salesChannel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel","description":"The shared reporting dimension for this channel; defaults from channelType (see listSaleChannel) (decided 29 September, readiness close-out)"}}},
"ChannelCreationProfileConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel Creation & Profile Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"channelName":{"type":"string","description":"Channel Name (internal)","maxLength":120},"channelCode":{"type":"string","description":"Channel Code: unique within the tenant, 2-20 upper-case letters, digits or hyphens (decided 29 September, readiness close-out)","pattern":"^[A-Z0-9-]{2,20}$"},"channelType":{"type":"string","enum":["b2cWeb","b2cMobileApp","pos","mobilePos","flyingPos","kiosk","callCentre","b2bPortal","reseller","ota","api","partnerPortal","marketplace","thirdPartyChannel","customChannel"],"description":"Channel Type (pack p.3-4 Channel Types). The type decides which configuration applies (p.6); each type reports under one SalesChannel value (see salesChannel)"},"internalDescription":{"type":"string","description":"Internal Description"},"customerFacingName":{"type":"string","description":"Customer-Facing Name","maxLength":120},"tenant":{"type":"string","description":"Tenant"},"brand":{"type":"string","description":"Brand ID"},"businessUnit":{"type":"string","description":"Business Unit ID"},"country":{"type":"string","description":"Country: ISO 3166-1 alpha-2","pattern":"^[A-Z]{2}$"},"market":{"type":"string","description":"Market (a configured market code)"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"timeZone":{"type":"string","description":"Time Zone: IANA name, e.g. Asia/Dubai"},"owner":{"type":"string","description":"Owner (user ID)"},"responsibleDepartment":{"type":"string","description":"Responsible Department"},"venue":{"type":"string","description":"Venue ID: required for the POS types (pack p.6) and when scopeLevel is venue","nullable":true},"workstationGroups":{"type":"array","items":{"type":"string"},"description":"Workstation groups (IDs) that may sell on a POS-type channel (pack p.6)"},"cashierAccess":{"type":"array","items":{"type":"string"},"description":"Cashier access: role IDs allowed to sell on a POS-type channel (pack p.6)"},"webstore":{"type":"string","description":"Webstore ID for a B2C-type channel (pack p.6)","nullable":true},"domainBrand":{"type":"string","description":"Domain/brand: the storefront domain for a B2C-type channel (pack p.6)","nullable":true},"digitalCustomerJourney":{"type":"string","description":"Digital customer journey: the checkout journey template ID for a B2C-type channel (pack p.6)","nullable":true},"partner":{"type":"string","description":"Partner ID for an OTA, reseller or partner channel (pack p.6); the partner record lives in B2B/OTA","nullable":true},"apiConnection":{"type":"string","description":"API connection: the connector ID from ADM-269 for an OTA/API channel (pack p.6); the external platform is named as data on the connector","nullable":true},"commercialOwner":{"type":"string","description":"Commercial Owner (user ID)"},"operationalOwner":{"type":"string","description":"Operational Owner (user ID)"},"technicalOwner":{"type":"string","description":"Technical Owner (user ID)"},"financeOwner":{"type":"string","description":"Finance Owner (user ID)"},"scopeLevel":{"type":"string","enum":["global","country","region","venue","attraction","event","location","businessUnit"],"description":"Operational Scope level (pack p.6)"},"scopeId":{"type":"string","description":"ID of the scoped item (country code, region, venue, attraction, event, location or business unit); empty for global","nullable":true},"salesChannel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel","description":"The shared reporting dimension for this channel; defaults from channelType (see listSaleChannel) (decided 29 September, readiness close-out)"},"channelId":{"type":"string","description":"Channel ID, assigned by TICVAI","readOnly":true},"status":{"type":"string","description":"Status: draft, configuration, validation, approved, scheduled, active, suspended, disabled or archived (the pack's suggested lifecycle, p.5); a new channel starts in draft","readOnly":true}}},
"ChannelFeesPaymentFulfillmentConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Channel Fees, Payment & Fulfillment Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"channelId":{"type":"string","description":"Channel ID"},"fees":{"type":"array","items":{"type":"object","properties":{"feeType":{"type":"string","enum":["booking","transaction","channel","service","delivery","payment"]},"feeProfileId":{"type":"string"}}},"description":"Fee Associations (pack p.14-15): which approved fee profile applies for each fee type; amounts are the Pricing/Fee Engine's"},"paymentMethods":{"type":"array","items":{"type":"string","enum":["card","cash","digitalWallet","paymentLink","accountCredit","b2bCredit"]},"description":"Payment Methods the channel may expose (pack p.15)"},"otherPaymentMethodCodes":{"type":"array","items":{"type":"string"},"description":"Other configured payment methods, by their Payment configuration code"},"fulfillmentMethods":{"type":"array","items":{"type":"string","enum":["digitalTicket","email","mobileApp","appleGoogleWallet","printAtHome","posPrint","kioskPrint","rfid","nfc","wristband","collection","voucher","apiTicketDelivery","bulkCsvExport"]},"description":"Fulfillment Methods (pack p.15-16; bulkCsvExport is the pre-generated ticket batch for partners that do not integrate, MoM 31 Aug §4.3)"}}},
"ChannelFeesPaymentFulfillmentConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel Fees, Payment & Fulfillment Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"channelId":{"type":"string","description":"Channel ID"},"fees":{"type":"array","items":{"type":"object","properties":{"feeType":{"type":"string","enum":["booking","transaction","channel","service","delivery","payment"]},"feeProfileId":{"type":"string"}}},"description":"Fee Associations (pack p.14-15): which approved fee profile applies for each fee type; amounts are the Pricing/Fee Engine's"},"paymentMethods":{"type":"array","items":{"type":"string","enum":["card","cash","digitalWallet","paymentLink","accountCredit","b2bCredit"]},"description":"Payment Methods the channel may expose (pack p.15)"},"otherPaymentMethodCodes":{"type":"array","items":{"type":"string"},"description":"Other configured payment methods, by their Payment configuration code"},"fulfillmentMethods":{"type":"array","items":{"type":"string","enum":["digitalTicket","email","mobileApp","appleGoogleWallet","printAtHome","posPrint","kioskPrint","rfid","nfc","wristband","collection","voucher","apiTicketDelivery","bulkCsvExport"]},"description":"Fulfillment Methods (pack p.15-16; bulkCsvExport is the pre-generated ticket batch for partners that do not integrate, MoM 31 Aug §4.3)"},"validationIssues":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["paymentMethodNotApproved","feeProfileMissing","mediaProfileMissing","incompatibleCombination"]},"message":{"type":"string"}}},"description":"Validation (pack p.16): incompatible combinations, e.g. RFID fulfilment with no RFID media profile for the venue/channel"}}},
"ChannelPricingCommercialProfileAssignmentInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is catalogue.price_list at 6%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Channel Pricing & Commercial Profile Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *For each assignment* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.","properties":{"priceProfile":{"type":"string","description":"Price Profile: the ID of the approved price list or profile consumed (the Pricing Engine calculates the price)"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"venue":{"type":"string","description":"Venue ID","nullable":true},"event":{"type":"string","description":"Event ID","nullable":true},"product":{"type":"string","description":"Product ID","nullable":true},"customerSegment":{"type":"string","description":"Customer Segment ID","nullable":true},"priority":{"type":"integer","description":"Priority: when several assignments match, the lower number wins","minimum":1},"channelId":{"type":"string","description":"Channel ID"},"pricingSource":{"type":"string","enum":["standardPriceList","channelPriceList","b2bRate","resellerRate","otaRate","posPrice","promotionalPriceProfile","dynamicPricingProfile"],"description":"Pricing Association (pack p.8): which kind of approved pricing this assignment consumes"},"overridePermission":{"type":"string","description":"Override Permission: the permission a user needs to override price on this channel","nullable":true},"fixedPriceOnly":{"type":"boolean","description":"Price Override Governance: use fixed price only"},"promotionAllowed":{"type":"boolean","description":"Price Override Governance: apply promotion"},"discountAllowed":{"type":"boolean","description":"Price Override Governance: apply discount"},"priceOverrideAllowed":{"type":"boolean","description":"Price Override Governance: override price"},"overrideRequiresApproval":{"type":"boolean","description":"Price Override Governance: require approval for override"},"dynamicPricingAllowed":{"type":"boolean","description":"Price Override Governance: use dynamic pricing"}},"x-ticvai-record-definition":"For each assignment"},
"ChannelPricingCommercialProfileAssignmentView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel Pricing & Commercial Profile Assignment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"priceProfile":{"type":"string","description":"Price Profile: the ID of the approved price list or profile consumed (the Pricing Engine calculates the price)"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"venue":{"type":"string","description":"Venue ID","nullable":true},"event":{"type":"string","description":"Event ID","nullable":true},"product":{"type":"string","description":"Product ID","nullable":true},"customerSegment":{"type":"string","description":"Customer Segment ID","nullable":true},"priority":{"type":"integer","description":"Priority: when several assignments match, the lower number wins","minimum":1},"channelId":{"type":"string","description":"Channel ID"},"pricingSource":{"type":"string","enum":["standardPriceList","channelPriceList","b2bRate","resellerRate","otaRate","posPrice","promotionalPriceProfile","dynamicPricingProfile"],"description":"Pricing Association (pack p.8): which kind of approved pricing this assignment consumes"},"overridePermission":{"type":"string","description":"Override Permission: the permission a user needs to override price on this channel","nullable":true},"fixedPriceOnly":{"type":"boolean","description":"Price Override Governance: use fixed price only"},"promotionAllowed":{"type":"boolean","description":"Price Override Governance: apply promotion"},"discountAllowed":{"type":"boolean","description":"Price Override Governance: apply discount"},"priceOverrideAllowed":{"type":"boolean","description":"Price Override Governance: override price"},"overrideRequiresApproval":{"type":"boolean","description":"Price Override Governance: require approval for override"},"dynamicPricingAllowed":{"type":"boolean","description":"Price Override Governance: use dynamic pricing"},"validationIssues":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["missingPrice","expiredPrice","currencyMismatch","conflictingProfiles","invalidOverride"]},"message":{"type":"string"}}},"description":"Price Validation (pack p.9)"}}},
"ChannelPublicationReadinessAiValidationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Channel Publication, Readiness & AI Validation submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"channelId":{"type":"string","description":"Channel ID"},"action":{"type":"string","enum":["validate","preview","submitForApproval","scheduleActivation","activate","returnForChanges","suspend"],"description":"Publication Action (pack p.17)"},"scheduledAt":{"type":"string","format":"date-time","description":"Activation time for scheduleActivation","nullable":true},"reason":{"type":"string","description":"Reason: mandatory when overriding warnings or returning for changes","nullable":true},"overrideWarnings":{"type":"boolean","description":"Proceed despite warnings (needs the override permission and a reason); critical issues cannot be overridden"}}},
"ChannelPublicationReadinessAiValidationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel Publication, Readiness & AI Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"channelId":{"type":"string","description":"Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"},"status":{"type":"string","description":"Status after the action: draft, configuration, validation, approved, scheduled, active, suspended, disabled or archived (the pack's suggested lifecycle, p.5)"},"readinessScore":{"type":"number","description":"Channel Readiness %","minimum":0,"maximum":100},"checklist":{"type":"array","items":{"type":"object","properties":{"area":{"type":"string","enum":["channelProfile","products","pricing","capacity","schedule","eligibility","salesRules","payment","fulfillment","integration"]},"result":{"type":"string","enum":["passed","warning","failed","notRequired"]},"scorePercent":{"type":"number"}}},"description":"Readiness Checklist (pack p.16) with each area's score (p.17)"},"issues":{"type":"array","items":{"type":"object","properties":{"severity":{"type":"string","enum":["critical","high","medium","low","recommendation"]},"area":{"type":"string","enum":["channelProfile","products","pricing","capacity","schedule","eligibility","salesRules","payment","fulfillment","integration"]},"code":{"type":"string"},"message":{"type":"string"}}},"description":"Issues by Issue Severity (pack p.17)"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI Validation findings (pack p.17, e.g. B2B price above the public promotional price, allocations exceeding capacity). Advisory only: nothing is changed until a user acts."}}},
"ChannelSalesRule": {"type":"object","x-ticvai-persistence":"catalogue.channel_sales_rule","description":"**When, how much and to whom a channel may sell** (29 September, data model DM3). Merges the channel sales schedule (ADM-261), sales limits and restrictions (ADM-265) and customer eligibility by channel (ADM-262): each is a rule on a channel, optionally for one product, with an effective window. `ruleKind` says which group of fields applies; the others are null. A product-level rule is overridden only where `overridesProductRule`.","required":["id","scopePath","salesChannelId","ruleKind","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"salesChannelId":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid","nullable":true},"ruleKind":{"type":"string","enum":["salesWindow","salesLimit","eligibility"]},"name":{"type":"string","maxLength":200,"nullable":true},"ruleLevel":{"type":"string","enum":["platform","product","channel","contractPartner"],"default":"channel"},"overridesProductRule":{"type":"boolean","default":false},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean","default":true},"salesStartDate":{"type":"string","format":"date","nullable":true},"salesStartTime":{"type":"string","format":"time","nullable":true},"salesEndDate":{"type":"string","format":"date","nullable":true},"salesEndTime":{"type":"string","format":"time","nullable":true},"timeZone":{"type":"string","maxLength":64,"nullable":true},"daysOfWeek":{"type":"array","items":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]}},"hoursOfOperation":{"type":"object","additionalProperties":true,"nullable":true,"description":"`[{opensAt, closesAt}]`."},"blackoutDates":{"type":"array","items":{"type":"string"},"description":"ISO dates."},"eventRelativeWindow":{"type":"object","additionalProperties":true,"nullable":true,"description":"`{anchor, opensMinutesBefore, closesMinutesBefore}`."},"minimumLeadDays":{"type":"integer","nullable":true,"minimum":0},"minimumQuantity":{"type":"integer","nullable":true,"minimum":0},"maximumQuantity":{"type":"integer","nullable":true,"minimum":1},"maximumPerTransaction":{"type":"integer","nullable":true,"minimum":1},"maximumPerCustomer":{"type":"integer","nullable":true,"minimum":1},"maximumPerDay":{"type":"integer","nullable":true,"minimum":1},"maximumPerEvent":{"type":"integer","nullable":true,"minimum":1},"maximumPerProduct":{"type":"integer","nullable":true,"minimum":1},"isReservationPermitted":{"type":"boolean","nullable":true},"isHoldPermitted":{"type":"boolean","nullable":true},"isPaymentLinkPermitted":{"type":"boolean","nullable":true},"isPartialPaymentPermitted":{"type":"boolean","nullable":true},"isSplitPaymentPermitted":{"type":"boolean","nullable":true},"isDiscountPermitted":{"type":"boolean","nullable":true},"isPromoCodePermitted":{"type":"boolean","nullable":true},"isExchangePermitted":{"type":"boolean","nullable":true},"isReschedulePermitted":{"type":"boolean","nullable":true},"isUpgradePermitted":{"type":"boolean","nullable":true},"restrictions":{"type":"array","items":{"type":"string","enum":["noRefunds","noCashPayment","noComplimentary","noManualDiscount","noSameDaySales","noSeatChanges"]}},"eligibilityDimension":{"type":"string","enum":["customerType","membership","loyaltyTier","country","residency","age","corporateAccount","partner","customerSegment","promoEligibility","authenticationStatus","purchaseHistory","salesTerritory",null],"nullable":true},"eligibilityOperator":{"type":"string","enum":["equals","notEquals","in","notIn","greaterThanOrEqual","lessThanOrEqual","between",null],"nullable":true},"eligibilityValues":{"type":"array","items":{"type":"string"}},"eligibilityEffect":{"type":"string","enum":["allow","deny",null],"nullable":true},"isGuestAllowed":{"type":"boolean","nullable":true},"isLoginRequired":{"type":"boolean","nullable":true},"isMembershipRequired":{"type":"boolean","nullable":true},"isCorporateAccountRequired":{"type":"boolean","nullable":true},"isIdentityVerificationRequired":{"type":"boolean","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ChannelSalesRulesLimitsRestrictionsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel Sales Rules, Limits & Restrictions displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"minimumQuantity":{"type":"integer","description":"Minimum Quantity per transaction","minimum":1,"nullable":true},"maximumQuantity":{"type":"integer","description":"Maximum Quantity; empty for no limit","minimum":1,"nullable":true},"maximumPerTransaction":{"type":"integer","description":"Maximum Per Transaction; empty for no limit","minimum":1,"nullable":true},"maximumPerCustomer":{"type":"integer","description":"Maximum Per Customer; empty for no limit","minimum":1,"nullable":true},"maximumPerDay":{"type":"integer","description":"Maximum Per Day; empty for no limit","minimum":1,"nullable":true},"maximumPerEvent":{"type":"integer","description":"Maximum Per Event; empty for no limit","minimum":1,"nullable":true},"maximumPerProduct":{"type":"integer","description":"Maximum Per Product; empty for no limit","minimum":1,"nullable":true},"reservationPermitted":{"type":"boolean","description":"Reservation permitted"},"holdPermitted":{"type":"boolean","description":"Hold permitted"},"paymentLinkPermitted":{"type":"boolean","description":"Payment link permitted"},"partialPaymentPermitted":{"type":"boolean","description":"Partial payment permitted"},"discountPermitted":{"type":"boolean","description":"Discount permitted"},"promoCodePermitted":{"type":"boolean","description":"Promo code permitted"},"exchangePermitted":{"type":"boolean","description":"Exchange permitted"},"reschedulePermitted":{"type":"boolean","description":"Reschedule permitted"},"ruleId":{"type":"string","description":"Rule ID"},"channelId":{"type":"string","description":"Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"},"product":{"type":"string","description":"Product ID; empty for every product on the channel","nullable":true},"ruleLevel":{"type":"string","enum":["platform","product","channel","contractPartner"],"description":"Rule Priority level (pack p.14)"},"overridesProductRule":{"type":"boolean","description":"Channel Overrides: this channel rule overrides a general product rule"},"splitPaymentPermitted":{"type":"boolean","description":"Split payment permitted"},"upgradePermitted":{"type":"boolean","description":"Upgrade permitted"},"restrictions":{"type":"array","items":{"type":"string","enum":["noRefunds","noCashPayment","noComplimentary","noManualDiscount","noSameDaySales","noSeatChanges"]},"description":"Channel Restrictions (pack p.14 examples as a closed list) (decided 29 September, readiness close-out)"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true}}},
"ChannelSalesScheduleAvailabilityWindowsSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Channel Sales Schedule & Availability Windows.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"activeSellingPeriods":{"type":"integer","description":"Active selling periods"},"scheduledOpenings":{"type":"integer","description":"Scheduled openings"},"scheduledClosures":{"type":"integer","description":"Scheduled closures"},"blackouts":{"type":"integer","description":"Blackouts"},"conflicts":{"type":"integer","description":"Conflicts"},"eventDates":{"type":"integer","description":"Event dates"}}},
"ChannelSalesScheduleAvailabilityWindowsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel Sales Schedule & Availability Windows displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"salesStartDate":{"type":"string","format":"date","description":"Sales Start Date","nullable":true},"salesStartTime":{"type":"string","description":"Sales Start Time, HH:MM local to timeZone","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true},"salesEndDate":{"type":"string","format":"date","description":"Sales End Date","nullable":true},"salesEndTime":{"type":"string","description":"Sales End Time, HH:MM local to timeZone","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true},"timeZone":{"type":"string","description":"Time Zone: IANA name"},"daysOfWeek":{"type":"array","items":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"description":"Days of Week the channel sells; empty means every day"},"hoursOfOperation":{"type":"array","items":{"type":"object","properties":{"opensAt":{"type":"string"},"closesAt":{"type":"string"}}},"description":"Hours of Operation: HH:MM ranges within each selling day"},"blackoutDates":{"type":"array","items":{"type":"string","format":"date"},"description":"Blackout Dates"},"eventRelativeWindows":{"type":"object","nullable":true,"description":"Event-relative windows (pack p.11: B2C opens 90 days before, OTA closes 4 hours before, kiosk opens 2 hours before admission; MoM: onsite closes 15 min before a timed show). Offsets in minutes before the anchor; negative means after","properties":{"anchor":{"type":"string","enum":["eventStart","admissionStart","eventEnd"]},"opensMinutesBefore":{"type":"integer","nullable":true},"closesMinutesBefore":{"type":"integer","nullable":true}}},"channelId":{"type":"string","description":"Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"},"product":{"type":"string","description":"Product ID the window applies to; empty for every product on the channel","nullable":true},"minimumLeadDays":{"type":"integer","description":"Minimum days between purchase and visit: 0 allows same-day, 1 is the MoM's next-day minimum for online sales (MoM 31 Aug §4.11)","minimum":0,"default":0},"aiInsights":{"type":"array","items":{"type":"string"},"description":"Unusual schedule configurations AI detects (pack p.12, e.g. OTA closing after admission has ended). Advisory only: nothing is changed until a user acts."}}},
"CustomerEligibilityRulesByChannelView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Customer & Eligibility Rules by Channel displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"guestAllowed":{"type":"boolean","description":"Guest allowed"},"loginRequired":{"type":"boolean","description":"Login required"},"membershipRequired":{"type":"boolean","description":"Membership required"},"corporateAccountRequired":{"type":"boolean","description":"Corporate account required"},"identityVerificationRequired":{"type":"boolean","description":"Identity verification required"},"ruleId":{"type":"string","description":"Rule ID"},"ruleName":{"type":"string","description":"Rule name, e.g. UAE Resident Offer"},"channelId":{"type":"string","description":"Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"},"product":{"type":"string","description":"Product ID; empty for every product on the channel","nullable":true},"dimension":{"type":"string","enum":["customerType","membership","loyaltyTier","country","residency","age","corporateAccount","partner","customerSegment","promoEligibility","authenticationStatus","purchaseHistory","salesTerritory"],"description":"Eligibility Dimension (pack p.12)"},"operator":{"type":"string","enum":["equals","notEquals","in","notIn","greaterThanOrEqual","lessThanOrEqual","between"],"description":"How values are compared (decided 29 September, readiness close-out)"},"values":{"type":"array","items":{"type":"string"},"description":"Values the dimension is compared with (e.g. residency = AE, customer account type = approvedTravelAgent)"},"effect":{"type":"string","enum":["allow","deny"],"description":"Whether a match allows or denies purchase on the channel"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"Contradictory channel/customer rules AI detects (pack p.13). Advisory only: nothing is changed until a user acts."}}},
"InventoryCapacityChannelAllocationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Inventory, Capacity & Channel Allocation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"productEvent":{"type":"string","description":"Product/Event: the product or event ID the pool belongs to"},"capacityPool":{"type":"string","description":"Capacity Pool ID"},"channel":{"type":"string","description":"Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"},"allocation":{"type":"number","description":"Allocation: units for dedicated, percent of the pool for percentage; empty for sharedPool","minimum":0,"nullable":true},"minimum":{"type":"integer","description":"Minimum units the channel keeps (not released below this)","minimum":0,"nullable":true},"maximum":{"type":"integer","description":"Maximum units the channel may reach, including dynamic growth","minimum":0,"nullable":true},"replenishmentRule":{"type":"object","nullable":true,"description":"Replenishment Rule: automatic migration from another channel (MoM 31 Aug §4.11, e.g. when B2C sells out pull 20% from B2B)","properties":{"sourceChannelId":{"type":"string"},"trigger":{"type":"string","enum":["soldOut","belowThreshold"]},"thresholdUnits":{"type":"integer","nullable":true},"sharePercent":{"type":"number","nullable":true},"units":{"type":"integer","nullable":true}}},"oversellAllowance":{"type":"integer","description":"Oversell allowance in units; 0 means no oversell","minimum":0,"default":0},"waitlistBehavior":{"type":"string","enum":["none","joinWaitlist","notifyOnRelease"],"description":"Waitlist behavior where applicable (decided 29 September, readiness close-out)"},"allocated":{"type":"integer","description":"Allocated"},"sold":{"type":"integer","description":"Sold"},"held":{"type":"integer","description":"Held"},"remaining":{"type":"integer","description":"Remaining"},"utilization":{"type":"number","description":"Utilization %: sold plus held over allocated, 0-100","minimum":0,"maximum":100},"released":{"type":"integer","description":"Released: units given back to the shared pool by a release rule"},"returned":{"type":"integer","description":"Returned: units returned manually"},"allocationType":{"type":"string","enum":["sharedPool","dedicated","percentage","dynamic"],"description":"Allocation Type (pack p.10)"},"releaseThreshold":{"type":"integer","description":"Release Threshold: unsold units above which the excess returns to the shared pool (pack p.10, e.g. 300)","nullable":true},"releaseHoursBeforeEvent":{"type":"integer","description":"Release point relative to the event, in hours before start (pack p.10, e.g. 48)","nullable":true},"releaseDate":{"type":"string","format":"date-time","description":"Release Date: fixed release point, used instead of the event-relative one","nullable":true},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI reallocation suggestions (pack p.11). Advisory only: nothing is changed until a user acts."}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProductCatalogueAssignmentInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Product & Catalogue Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"channelId":{"type":"string","description":"Channel ID"},"assignmentMethod":{"type":"string","enum":["individualProduct","productFamily","productCategory","event","attraction","venueCatalogue","productCollection","entireApprovedCatalogue"],"description":"Assignment Method (pack p.7)"},"targetIds":{"type":"array","items":{"type":"string"},"description":"IDs of the products, families, categories, events, attractions, venue catalogues or collections assigned; empty for entireApprovedCatalogue"},"excludedProductIds":{"type":"array","items":{"type":"string"},"description":"Channel-specific overrides: products excluded from what is inherited (pack p.8, e.g. B2C excludes corporate tickets)"},"enabled":{"type":"boolean","description":"Enable or disable the assignment on the channel"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true}}},
"ProductCatalogueAssignmentView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Product & Catalogue Assignment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"product":{"type":"string","description":"Product ID"},"productType":{"$ref":"#/components/schemas/ProductKind","description":"Product Type"},"venue":{"type":"string","description":"Venue ID"},"status":{"$ref":"#/components/schemas/ProductLifecycleState","description":"Status: the product's own lifecycle state in Product Catalogue"},"validity":{"type":"string","description":"Validity: the product's validity period as set in Product Catalogue, shown for reference"},"channelStatus":{"type":"string","description":"Channel Status: enabled, disabled or scheduled on this channel (decided 29 September, readiness close-out)"},"pricingStatus":{"type":"string","description":"Pricing Status: valid, missing or expired for this channel (from ADM-261) (decided 29 September, readiness close-out)"},"capacityStatus":{"type":"string","description":"Capacity Status: allocated, sharedPool or none for this channel (from ADM-262) (decided 29 September, readiness close-out)"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"channelId":{"type":"string","description":"Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"},"assignmentMethod":{"type":"string","enum":["individualProduct","productFamily","productCategory","event","attraction","venueCatalogue","productCollection","entireApprovedCatalogue"],"description":"Assignment Method the product came in by (pack p.7)"},"inheritedFrom":{"type":"string","enum":["globalChannelCatalogue","venueCatalogue","channelOverride"],"description":"Inheritance level the assignment comes from (pack p.7-8)"},"validationIssues":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["draftProduct","retiredProduct","missingPricing","missingEntitlement","outsideValidity","unavailableForChannel"]},"message":{"type":"string"}}},"description":"Validation (pack p.8): why this product should not be published on the channel"}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"SalesChannelCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Sales Channel Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"totalChannels":{"type":"integer","description":"Total Channels"},"activeChannels":{"type":"integer","description":"Active Channels"},"inactiveChannels":{"type":"integer","description":"Inactive Channels"},"channelsInDraft":{"type":"integer","description":"Channels in Draft"},"channelsWithErrors":{"type":"integer","description":"Channels With Errors"},"productsDistributed":{"type":"integer","description":"Products Distributed: distinct products assigned to at least one active channel"},"channelsWithCapacityAlerts":{"type":"integer","description":"Channels With Capacity Alerts"},"channelsWithPricingIssues":{"type":"integer","description":"Channels With Pricing Issues"},"scheduledActivations":{"type":"integer","description":"Scheduled Activations"},"scheduledDeactivations":{"type":"integer","description":"Scheduled Deactivations"}}},
"SalesChannelCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Sales Channel Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"channelId":{"type":"string","description":"Channel ID"},"channelName":{"type":"string","description":"Channel Name"},"channelType":{"type":"string","enum":["b2cWeb","b2cMobileApp","pos","mobilePos","flyingPos","kiosk","callCentre","b2bPortal","reseller","ota","api","partnerPortal","marketplace","thirdPartyChannel","customChannel"],"description":"Channel Type (pack p.3-4 Channel Types). The type decides which configuration applies (p.6); each type reports under one SalesChannel value (see salesChannel)"},"brand":{"type":"string","description":"Brand"},"venueScope":{"type":"string","description":"Venue/Scope: the channel's operational scope level and the name of the scoped item (e.g. a venue name, or Global)"},"products":{"type":"integer","description":"Products: number of products assigned to the channel"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"status":{"type":"string","description":"Status: draft, configuration, validation, approved, scheduled, active, suspended, disabled or archived (the pack's suggested lifecycle, p.5)"},"publicationStatus":{"type":"string","description":"Publication Status: unpublished, pendingApproval, scheduled or published (decided 29 September, readiness close-out)"},"integrationStatus":{"type":"string","description":"Integration Status: notRequired, notConfigured, connected, degraded or offline (decided 29 September, readiness close-out)"},"lastUpdated":{"type":"string","format":"date-time","description":"Last Updated"},"owner":{"type":"string","description":"Owner: the channel's commercial owner (user ID)"},"salesChannel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel","description":"The shared reporting dimension this channel's sales are attributed to (b2cWeb -> guestWeb, b2cMobileApp -> guestApp, the POS types -> pos, callCentre, b2bPortal -> b2b, ota and marketplace -> ota, api, reseller/partnerPortal/thirdPartyChannel -> partner; a custom channel picks one) (decided 29 September, readiness close-out)"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"Configuration problems AI flags on this channel (pack p.5, e.g. products assigned without a valid price profile for the channel). Advisory only: nothing is changed until a user acts."}}}
}
```
