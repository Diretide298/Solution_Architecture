# WS44 — Product Lifecycle   Catalogue Governance board 2

**10 screens · 12 operations · 19 schemas · 3 permissions**

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
  `AI_APPROVE, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `ADM-128` | Product Governance Command Center | B–D | 6 | 228 | 6 | 0 | 3 | 0 | — | notStarted (generated) |
| `ADM-129` | Approval Workflow Designer | B–D | 18 | 0 | 5 | 0 | 2 | 3 | — | notStarted (generated) |
| `ADM-130` | Approval Review & Decision Workspace | B–D | 0 | 0 | 6 | 0 | 1 | 3 | — | notStarted (generated) |
| `ADM-131` | Product Version Management | B–D | 0 | 0 | 6 | 4 | 2 | 0 | — | notStarted (generated) |
| `ADM-132` | Rollback & Recovery Management | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-133` | Change Impact Analysis | B–D | 6 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-134` | Change Propagation & Dependency Control | B–D | 6 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-135` | Product Retirement, Suspension & Archive | B–D | 9 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-136` | Product Audit Trail & Change History | B–D | 16 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-137` | Governance Risk, AI Monitoring & Control Center | B–D | 4 | 18 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-130, ADM-132, ADM-133, ADM-134, ADM-137 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-128` Product Governance Command Center

**Provide management and administrators with a single control center for all product governance activities.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_APPROVE`, `PRODUCT_VIEW` (1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§The dashboard shall display; Each record should display) and no metric row |
| Offline | online only |
| Opens with | `findingId` (navigation) |
| Route | `/catalogue/product-governance-command-center-adm-128` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search product governance | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, product type, owner, department, status, risk and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product type | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProductGovernance` ?productType |
| Owner | text field | — | — | `listProductGovernance` ?owner |
| Department | text field | — | — | `listProductGovernance` ?department |
| Status | text field | — | — | `listProductGovernance` ?status |
| Risk | radio group | — | Low · Medium · High · Critical | `listProductGovernance` ?risk |
| Change type | select | — | New product · Description · Price · Validity · Capacity · Entitlement · Eligibility · Tax · Channel · Media · Policy · Relationship … | `listProductGovernance` ?changeType |
| Approver | text field | — | — | `listProductGovernance` ?approver |
| Effective from | date picker | — | — | `listProductGovernance` ?effectiveFrom |
| Effective to | date picker | — | — | `listProductGovernance` ?effectiveTo |
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listProductGovernance` ?channel |

**Form: Decide catalogue AI finding** (modal, opened by *Decide catalogue AI finding*; *Decide catalogue AI finding* calls `decideCatalogueAiFinding`, *Cancel* sends nothing)

**Collects what `decideCatalogueAiFinding` sends before it is called.** Required: `decision`. Optional: `comment`, `ownerPrincipalId`, `dueDate`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | radio group | required | — | Acknowledge · Accept · Dismiss · Resolve | — | — | `decideCatalogueAiFinding` body |
| Comment `comment` | text area | optional | — | max length 1000 | — | — | `decideCatalogueAiFinding` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | — | `decideCatalogueAiFinding` body |
| Due date `dueDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `decideCatalogueAiFinding` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `alreadyClosed`.; 422 `commentRequired`.

#### Outputs: what the screen shows and produces

**Shown**

**Products awaiting approval** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Changes awaiting approval** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Rejected changes** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Products with governance warnings** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Scheduled changes** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Products with unpublished changes** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Products with dependency conflicts** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Products approaching retirement** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Recently published versions** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**High risk configuration changes** (metric tile, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |
| Change request | the name it points at, never the id | Change request id |
| Product | the name it points at, never the id | Product id |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | Product's current lifecycle state |
| AI insights | list or chips (count when long) | AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Every product governance** (data table, from `listProductGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Failed publications/rollbacks | text | not in the schema: `Failed publications/rollbacks` |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |

**The selected product governance** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Failed publications/rollbacks | text | not in the schema: `Failed publications/rollbacks` |
| Product | text | Product name |
| Venue | text | Venue name |
| Product owner | text | Product owner (display name) |
| Change type | chip: New product, Description, Price, Validity, Capacity, Entitlement… | Change type (decided 29 September, readiness close-out) |
| Current version | 1,234 | Current version number (ProductVersion.version); empty for a new product |
| Proposed version | 1,234 | Proposed version number |
| Requested by | text | Requested by (display name) |
| Requested date | 1 Oct 2026, 14:30 | Requested date-time |
| Risk level | chip: Low, Medium, High, Critical | Risk level |
| Approval status | text | Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn |
| Effective date | 1 Oct 2026 | Effective date of the change; empty = on approval |
| Impacted channels | list or chips (count when long) | Impacted channels |
| Assigned approver | text | Assigned approver (display name) |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Decide catalogue AI finding (primary button) | `decideCatalogueAiFinding` POST `/ai-findings/{findingId}/decision` | inline | CatalogueAiFinding | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `alreadyClosed`.; 422 `commentRequired`. | gated `AI_APPROVE`; opens modal first |

**Data it reads**: `listProductGovernance` (onLoad, Product Governance Command Center)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-131` Product Version Management: *Product Version Management*; carries `productId`
- → `ADM-129` Approval Workflow Designer: *Works in Approval Workflow Designer*; calls `listProductGovernance`
- → `ADM-130` Approval Review & Decision Workspace: *Works in Approval Review & Decision Workspace*; calls `listProductGovernance`
- → `ADM-132` Rollback & Recovery Management: *Works in Rollback & Recovery Management*; calls `listProductGovernance`
- → `ADM-135` Product Retirement, Suspension & Archive: *Works in Product Retirement, Suspension & Archive*; calls `listProductGovernance`
- → `ADM-136` Product Audit Trail & Change History: *Works in Product Audit Trail & Change History*; calls `listProductGovernance`
- → `ADM-133` Change Impact Analysis: *Works in Change Impact Analysis*; carries `productId`; calls `listProductGovernance`
- → `ADM-134` Change Propagation & Dependency Control: *Works in Change Propagation & Dependency Control*; carries `productId`; calls `listProductGovernance`
- → `ADM-137` Governance Risk, AI Monitoring & Control Center: *Works in Governance Risk, AI Monitoring & Control Center*; carries `findingId`; calls `listProductGovernance`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product governance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `alreadyClosed`.; 422 `commentRequired`. |

#### Permissions

- `listProductGovernance` → `PRODUCT_VIEW` (read) · staff
- `decideCatalogueAiFinding` → `AI_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Changes to a published product (pricing, validity) go through approval and review, with rollback and version history. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-578)*
- Governance view shows product counts by status (draft, pending approval, approved, published); each price, terms or policy revision is a new version; publish rights are restricted to the authorised user/department; version history supports rollback to a prior published version. *(client request · MoM 25 Aug 2026, 4.10 AI Governance & Publish Workflow · DI-473)*

Also apply: 1 for P09 · Catalogue, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-128` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-128`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 1: Opens Product Governance Command Center → Provide management and administrators with a single control center for all product governance activities.
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F153 branch at step 1 (expected): when Nothing has been set up on Product Governance Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F153 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (228 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-128?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Decide catalogue AI finding.
- [ ] Every transition is wired: `ADM-002`, `ADM-131`, `ADM-129`, `ADM-130`, `ADM-132`, `ADM-135`, `ADM-136`, `ADM-133`, `ADM-134`, `ADM-137`.
- [ ] Every gated control is gated: `AI_APPROVE`, `PRODUCT_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-129` Approval Workflow Designer

**Configure reusable approval workflows governing product creation and modification.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Each workflow can define; Tax configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/catalogue/approval-workflow-designer-adm-129` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Workflow name | select field | — | — | — | — | — | — |
| Applicable product types | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Department | select field | — | — | — | — | — | — |
| Change type | select field | — | — | — | — | — | — |
| Approval stages | select field | — | — | — | — | — | — |
| Approver role | select field | — | — | — | — | — | — |
| Specific approver | select field | — | — | — | — | — | — |
| Approval group | select field | — | — | — | — | — | — |
| Sequential/parallel approval | select field | — | — | — | — | — | — |
| Mandatory/optional stage | select field | — | — | — | — | — | — |
| SLA | select field | — | — | — | — | — | — |
| Escalation | select field | — | — | — | — | — | — |
| Delegation | select field | — | — | — | — | — | — |
| Reminder frequency | select field | — | — | — | — | — | — |
| Rejection behavior | select field | — | — | — | — | — | — |
| Resubmission behavior | select field | — | — | — | — | — | — |
| → Finance | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-128` Product Governance Command Center: *Returns to the board's landing screen*; calls `approveWorkflow`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval workflow designer configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval workflow designer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval workflow designer configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `approveWorkflow` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Changes to a published product (pricing, validity) go through approval and review, with rollback and version history. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-578)*
- Governance view shows product counts by status (draft, pending approval, approved, published); each price, terms or policy revision is a new version; publish rights are restricted to the authorised user/department; version history supports rollback to a prior published version. *(client request · MoM 25 Aug 2026, 4.10 AI Governance & Publish Workflow · DI-473)*

Also apply: 1 for P09 · Catalogue, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-129` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-129`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 2: Works in Approval Workflow Designer → Configure reusable approval workflows governing product creation and modification.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-129?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve.
- [ ] Every transition is wired: `ADM-128`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-130` Approval Review & Decision Workspace

**Give approvers a clear interface for reviewing a proposed product or product change before making a decision.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/catalogue/approval-review-decision-workspace-adm-130` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-128` Product Governance Command Center: *Returns to the board's landing screen*; calls `approveReviewDecision`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval review decision list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval review decision untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval review decision yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval review decision are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `approveReviewDecision` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The preview/publish step shows how the ticket appears on the B2C front end and — at Chinmay's request — also the PDF ticket layout and Apple Wallet / Google Wallet formats, so the reviewer sees every output format. *(agreed · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference; 5. Key Decisions · DI-444)*

Also apply: 1 for P09 · Catalogue, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-130` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-130`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 4: Works in Approval Review & Decision Workspace → Give approvers a clear interface for reviewing a proposed product or product change before making a decision.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-130?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve, Cancel.
- [ ] Every transition is wired: `ADM-128`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-131` Product Version Management

**Maintain controlled versions of every governed product configuration. The source matrix specifically requires version history for products and the ability to roll back to earlier versions.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `productId` (navigation) · cold entry: **Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one, the screen says what is missing and offers that … |
| Route | `/catalogue/product-version-management-adm-131` |

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Basic product information, Pricing, Capacity, Entitlements, Channels. Each needs an operation, or needs … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Version 4.2 ↔ Version 4.1 (primary button) | navigation or local | — | — | — | — |
| Basic product information (secondary button) | navigation or local | — | — | — | — |
| Pricing (secondary button) | navigation or local | — | — | — | — |
| Capacity (secondary button) | navigation or local | — | — | — | — |
| Entitlements (secondary button) | navigation or local | — | — | — | — |
| Channels (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-128` Product Governance Command Center: *Returns to the board's landing screen*; calls `listProductVersions`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product version list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product version untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product version yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product version are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listProductVersions` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.4.9 | System shall maintain version history of all product configurations including pricing, rules, entitlements and capacities. | Ticketing Catalogue | CONTRACTED | `listProductVersions` |
| 1.4.10 | System shall allow authorized users to restore a previous version of a product configuration. | Ticketing Catalogue | CONTRACTED | `listProductVersions` |
| 1.4.11 | System shall support duplication of products including all associated configurations, rules, pricing and entitlements. | Ticketing Catalogue | CONTRACTED | `listProductVersions` |
| 2.9.7 | The system should guarantee the integrity of all pre-existing revenue by ensuring that when an amount is amended, the value of prior sales is not modified. | Ticketing Sales | CONTRACTED | `listProductVersions` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Changes to a published product (pricing, validity) go through approval and review, with rollback and version history. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-578)*
- Governance view shows product counts by status (draft, pending approval, approved, published); each price, terms or policy revision is a new version; publish rights are restricted to the authorised user/department; version history supports rollback to a prior published version. *(client request · MoM 25 Aug 2026, 4.10 AI Governance & Publish Workflow · DI-473)*

Also apply: 1 for P09 · Catalogue, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-131` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-131`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 6: Works in Product Version Management → Maintain controlled versions of every governed product configuration. The source matrix specifically requires version history for products and the ability to roll back to earlier versions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-131?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Version 4.2 ↔ Version 4.1, Basic product information, Pricing, Capacity, Entitlements, Channels.
- [ ] Every transition is wired: `ADM-128`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-132` Rollback & Recovery Management

**Safely restore an earlier product configuration when a newly published configuration causes an issue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/catalogue/rollback-recovery-management-adm-132` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `listRollbackRecovery` ?productId |
| Status | text field | — | — | `listRollbackRecovery` ?status |
| Scope | select | — | Entire product · Pricing association · Channel association · Validity configuration · Media · Policy · Entitlement configuration | `listRollbackRecovery` ?scope |
| Emergency | toggle | — | — | `listRollbackRecovery` ?emergency |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listRollbackRecovery` (onLoad, Rollback & Recovery Management)

**Where the user goes next**

- → `ADM-128` Product Governance Command Center: *Returns to the board's landing screen*; calls `listRollbackRecovery`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rollback recovery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rollback recovery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rollback recovery yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rollback recovery are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listRollbackRecovery` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Changes to a published product (pricing, validity) go through approval and review, with rollback and version history. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-578)*
- Governance view shows product counts by status (draft, pending approval, approved, published); each price, terms or policy revision is a new version; publish rights are restricted to the authorised user/department; version history supports rollback to a prior published version. *(client request · MoM 25 Aug 2026, 4.10 AI Governance & Publish Workflow · DI-473)*

Also apply: 1 for P09 · Catalogue, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-132` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-132`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 8: Works in Rollback & Recovery Management → Safely restore an earlier product configuration when a newly published configuration causes an issue.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-132?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-128`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-133` Change Impact Analysis

**Show administrators what will be affected before a product change is approved or published. This directly addresses the matrix requirement to perform impact analysis before product changes are published.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/catalogue/change-impact-analysis-adm-133` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Change request | picker: choose a change request | — | — | `listChangeImpactAnalysis` ?changeRequestId |
| Product | picker: choose a product | — | — | `listChangeImpactAnalysis` ?productId |
| Area | select | — | Future orders · Reservations · Issued tickets · Capacity · Pricing · Tax · Promotions · Membership · Entitlements · Access control · Sales channels · B2B partners … | `listChangeImpactAnalysis` ?area |
| Min risk | radio group | — | Low · Medium · High · Critical | `listChangeImpactAnalysis` ?minRisk |

**Sent by *Save product links*** (`setProductLinks`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Source product `sourceProductId` | picker: choose a source product | required | — | — | shows names, sends the id | — | `setProductLinks` body |
| Dependency type `dependencyType` | select | required | — | Parent product · Child product · Bundle · Add on · Upgrade · Membership · Package · Promotion · Price profile · Capacity pool · Entitlement · Sales channel … | — | — | `setProductLinks` body |
| Linked object `linkedObjectId` | picker: choose a linked object | required | — | — | shows names, sends the id | — | `setProductLinks` body |
| Linked object name `linkedObjectName` | text field | optional | — | max length 200 | — | — | `setProductLinks` body |
| Propagates changes `propagatesChanges` | toggle | optional | on | — | — | — | `setProductLinks` body |
| Overridden fields `overriddenFields` | list of values (chips) | optional | — | — | — | — | `setProductLinks` body |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save product links (primary button) | `setProductLinks` PUT `/products/{productId}/links` | ProductLink[] | ProductLink[] | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `circularDependency` or `duplicateLink`. | gated `PRODUCT_CONFIGURE` |

**Data it reads**: `listChangeImpactAnalysis` (onLoad, Change Impact Analysis)

**Where the user goes next**

- → `ADM-128` Product Governance Command Center: *Returns to the board's landing screen*; calls `listChangeImpactAnalysis`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The change impact analysis list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the change impact analysis untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No change impact analysis yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the change impact analysis are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `circularDependency` or `duplicateLink`. |

#### Permissions

- `listChangeImpactAnalysis` → `PRODUCT_VIEW` (read) · staff
- `setProductLinks` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Chinmay: before a change (e.g. to ticket validity) is confirmed, show which existing bookings, reservations or promotions are affected and alert admin and customer-facing teams. Higher-risk changes can be applied from a chosen future effective date. Allam agreed. *(agreed · MoM 31 Aug 2026, 4.10 Change impact analysis · DI-579)*

Also apply: 1 for P09 · Catalogue, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-133` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-133`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 10: Works in Change Impact Analysis → Show administrators what will be affected before a product change is approved or published. This directly addresses the matrix requirement to perform impact analysis before product changes are …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-133?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save product links.
- [ ] Every transition is wired: `ADM-128`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-134` Change Propagation & Dependency Control

**Control whether approved product changes should automatically propagate to related products or dependent configurations. The source matrix requires controlled propagation of changes to linked products.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/catalogue/change-propagation-dependency-control-adm-134` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `listChangePropagationDependency` ?productId |
| Change request | picker: choose a change request | — | — | `listChangePropagationDependency` ?changeRequestId |
| Dependency type | select | — | Parent product · Child product · Bundle · Add on · Upgrade · Membership · Package · Promotion · Price profile · Capacity pool · Entitlement · Sales channel … | `listChangePropagationDependency` ?dependencyType |
| Conflicts only | toggle | — | — | `listChangePropagationDependency` ?conflictsOnly |

**Sent by *Save product links*** (`setProductLinks`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Source product `sourceProductId` | picker: choose a source product | required | — | — | shows names, sends the id | — | `setProductLinks` body |
| Dependency type `dependencyType` | select | required | — | Parent product · Child product · Bundle · Add on · Upgrade · Membership · Package · Promotion · Price profile · Capacity pool · Entitlement · Sales channel … | — | — | `setProductLinks` body |
| Linked object `linkedObjectId` | picker: choose a linked object | required | — | — | shows names, sends the id | — | `setProductLinks` body |
| Linked object name `linkedObjectName` | text field | optional | — | max length 200 | — | — | `setProductLinks` body |
| Propagates changes `propagatesChanges` | toggle | optional | on | — | — | — | `setProductLinks` body |
| Overridden fields `overriddenFields` | list of values (chips) | optional | — | — | — | — | `setProductLinks` body |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save product links (primary button) | `setProductLinks` PUT `/products/{productId}/links` | ProductLink[] | ProductLink[] | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `circularDependency` or `duplicateLink`. | gated `PRODUCT_CONFIGURE` |

**Data it reads**: `listChangePropagationDependency` (onLoad, Change Propagation & Dependency Control)

**Where the user goes next**

- → `ADM-128` Product Governance Command Center: *Returns to the board's landing screen*; calls `listChangePropagationDependency`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The change propagation dependency list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the change propagation dependency untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No change propagation dependency yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the change propagation dependency are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `circularDependency` or `duplicateLink`. |

#### Permissions

- `listChangePropagationDependency` → `PRODUCT_VIEW` (read) · staff
- `setProductLinks` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Chinmay: before a change (e.g. to ticket validity) is confirmed, show which existing bookings, reservations or promotions are affected and alert admin and customer-facing teams. Higher-risk changes can be applied from a chosen future effective date. Allam agreed. *(agreed · MoM 31 Aug 2026, 4.10 Change impact analysis · DI-579)*

Also apply: 1 for P09 · Catalogue, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-134` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-134`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 12: Works in Change Propagation & Dependency Control → Control whether approved product changes should automatically propagate to related products or dependent configurations. The source matrix requires controlled propagation of changes to linked …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-134?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save product links.
- [ ] Every transition is wired: `ADM-128`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-135` Product Retirement, Suspension & Archive

**Provide a governed end-of-life process for products. The source matrix explicitly requires disabling or retiring products without affecting previously sold tickets.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrator defines) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/catalogue/product-retirement-suspension-archive-adm-135` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Suspend Sales, Temporarily Disable, End Sale, Archive. Each needs an operation, or needs removing from the …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Retirement date | select field | — | — | — | — | — | — |
| End-of-sale date | select field | — | — | — | — | — | — |
| Channels | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |
| Replacement product | select field | — | — | — | — | — | — |
| Existing reservation treatment | select field | — | — | — | — | — | — |
| Existing ticket treatment | select field | — | — | — | — | — | — |
| Communication requirements | select field | — | — | — | — | — | — |
| Reporting treatment | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Action | radio group | — | Suspend sales · Temporarily disable · End sale · Retire · Archive | `listProductRetirementSuspension` ?action |
| Lifecycle state | select | — | Draft · In review · Approved · Live · Withdrawn · Archived | `listProductRetirementSuspension` ?lifecycleState |
| Search | text field | — | — | `listProductRetirementSuspension` ?search |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Suspend Sales (destructive button) | navigation or local | — | — | — | — |
| Temporarily Disable (secondary button) | navigation or local | — | — | — | — |
| End Sale (destructive button) | navigation or local | — | — | — | — |
| Retire (secondary button) | navigation or local | — | — | — | — |
| Archive (destructive button) | navigation or local | — | — | — | — |

**Data it reads**: `listProductRetirementSuspension` (onLoad, Product Retirement, Suspension & Archive)

**Where the user goes next**

- → `ADM-128` Product Governance Command Center: *Returns to the board's landing screen*; calls `listProductRetirementSuspension`

**What opens over it**

- confirmDialog *Suspend Sales*: **Suspend Sales on a product retirement suspension is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *End Sale*: **End Sale on a product retirement suspension is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *Archive*: **Archive on a product retirement suspension is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product retirement suspension configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product retirement suspension untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product retirement suspension configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listProductRetirementSuspension` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Catalogue, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-135` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-135`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 14: Works in Product Retirement, Suspension & Archive → Provide a governed end-of-life process for products. The source matrix explicitly requires disabling or retiring products without affecting previously sold tickets.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-135?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Suspend Sales, Temporarily Disable, End Sale, Retire, Archive.
- [ ] Every transition is wired: `ADM-128`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-136` Product Audit Trail & Change History

**Provide a complete, immutable history of product configuration and governance activity. The matrix requires tracking configuration changes with timestamps and user information.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Each entry should capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/catalogue/product-audit-trail-change-history-adm-136` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search product audit trail | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by product, user, date, action, version, configuration area and 4 more — which are present is a decision the pack already made. | — |
| Date/time | select field | — | — | — | — | — | — |
| User | select field | — | — | — | — | — | — |
| Role | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Version | select field | — | — | — | — | — | — |
| Action | select field | — | — | — | — | — | — |
| Configuration area | select field | — | — | — | — | — | — |
| Previous value | select field | — | — | — | — | — | — |
| New value | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |
| Approval reference | select field | — | — | — | — | — | — |
| Source channel | select field | — | — | — | — | — | — |
| Environment | select field | — | — | — | — | — | — |
| IP/device metadata where applicable | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `listProductTrailChange` ?productId |
| User | picker: choose an user | — | — | `listProductTrailChange` ?userId |
| From | date and time picker | — | — | `listProductTrailChange` ?from |
| To | date and time picker | — | — | `listProductTrailChange` ?to |
| Action | select | — | Created · Updated · Submitted · Approved · Rejected · Changes requested · Scheduled · Published · Rolled back · Suspended · Retired · Archived … | `listProductTrailChange` ?action |
| Version | number field | — | — | `listProductTrailChange` ?version |
| Configuration area | select | — | Basic information · Validity · Pricing · Capacity · Entitlements · Eligibility · Media · Channels · Policies · Relationships · Lifecycle | `listProductTrailChange` ?configurationArea |
| Venue | picker: choose a venue | — | — | `listProductTrailChange` ?venue |
| Approval | text field | — | — | `listProductTrailChange` ?approval |
| Risk | radio group | — | Low · Medium · High · Critical | `listProductTrailChange` ?risk |
| Environment | radio group | — | Development · Sandbox · Uat · Staging · Production | `listProductTrailChange` ?environment |

#### Outputs: what the screen shows and produces

**Data it reads**: `listProductTrailChange` (onLoad, Product Audit Trail & Change History)

**Where the user goes next**

- → `ADM-128` Product Governance Command Center: *Returns to the board's landing screen*; calls `listProductTrailChange`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product audit trail configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product audit trail untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product audit trail configured yet. Carries the create action and says what the platform does in the meantime. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product audit trail are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listProductTrailChange` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Changes to a published product (pricing, validity) go through approval and review, with rollback and version history. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-578)*

Also apply: 1 for P09 · Catalogue, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-136` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-136`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 16: Works in Product Audit Trail & Change History → Provide a complete, immutable history of product configuration and governance activity. The matrix requires tracking configuration changes with timestamps and user information.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-136?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-128`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-137` Governance Risk, AI Monitoring & Control Center

**Use TICVAI intelligence to continuously identify catalogue governance risks rather than relying entirely on administrators to discover them manually.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Catalogue · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_APPROVE`, `PRODUCT_VIEW` (1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `findingId` (navigation) |
| Route | `/catalogue/governance-risk-ai-monitoring-control-center-adm-137` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Severity | radio group | — | Critical · High · Medium · Low | `listGovernanceRiskMonitoring` ?severity |
| Risk | select | — | Product without owner · Missing approval · Outdated pricing · Conflicting validity · Missing channel configuration · Orphaned dependency · Unused product · Duplicate product · Unusual configuration change · High override level · Scheduled publication conflict … | `listGovernanceRiskMonitoring` ?risk |
| Owner | text field | — | — | `listGovernanceRiskMonitoring` ?owner |
| Status | text field | — | — | `listGovernanceRiskMonitoring` ?status |

**Form: Decide catalogue AI finding** (modal, opened by *Decide catalogue AI finding*; *Decide catalogue AI finding* calls `decideCatalogueAiFinding`, *Cancel* sends nothing)

**Collects what `decideCatalogueAiFinding` sends before it is called.** Required: `decision`. Optional: `comment`, `ownerPrincipalId`, `dueDate`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | radio group | required | — | Acknowledge · Accept · Dismiss · Resolve | — | — | `decideCatalogueAiFinding` body |
| Comment `comment` | text area | optional | — | max length 1000 | — | — | `decideCatalogueAiFinding` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | — | `decideCatalogueAiFinding` body |
| Due date `dueDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `decideCatalogueAiFinding` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `alreadyClosed`.; 422 `commentRequired`.

#### Outputs: what the screen shows and produces

**Shown**

**Every governance risk monitoring** (data table, from `listGovernanceRiskMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Critical / high / medium / low | text | not in the schema: `Critical / High / Medium / Low` |
| Risk | chip: Product without owner, Missing approval, Outdated pricing, Conflicting validity … | Risk detected (AI Monitoring, pack p.26) |
| Product | text | Product name |
| Venue | text | Venue name |
| Business impact | text | Business impact, in plain language |
| Recommended action | text | Recommended action; advisory |
| Owner | text | Owner (display name) |
| Due date | 1 Oct 2026 | Due date |
| Status | text | Status: open, acknowledged, inRemediation, resolved or dismissed (decided 29 September, readiness close-out) |

**The selected governance risk monitoring** (detail panel): The pack groups this record's detail under its own headings: “Potential duplicate detected”, “Governance warning”, “Backend Screen Primary Responsibility”, “Restore previous”, “Pre-change impact”.

| Shows | Format | Notes |
|---|---|---|
| Critical / high / medium / low | text | not in the schema: `Critical / High / Medium / Low` |
| Risk | chip: Product without owner, Missing approval, Outdated pricing, Conflicting validity … | Risk detected (AI Monitoring, pack p.26) |
| Product | text | Product name |
| Venue | text | Venue name |
| Business impact | text | Business impact, in plain language |
| Recommended action | text | Recommended action; advisory |
| Owner | text | Owner (display name) |
| Due date | 1 Oct 2026 | Due date |
| Status | text | Status: open, acknowledged, inRemediation, resolved or dismissed (decided 29 September, readiness close-out) |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Decide catalogue AI finding (primary button) | `decideCatalogueAiFinding` POST `/ai-findings/{findingId}/decision` | inline | CatalogueAiFinding | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `alreadyClosed`.; 422 `commentRequired`. | gated `AI_APPROVE`; opens modal first |

**Data it reads**: `listGovernanceRiskMonitoring` (onLoad, Governance Risk, AI Monitoring & Control Center)

**Where the user goes next**

- → `ADM-128` Product Governance Command Center: *Product Governance Command Center*; carries `findingId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance risk monitoring list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance risk monitoring untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No governance risk monitoring yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the governance risk monitoring are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `alreadyClosed`.; 422 `commentRequired`. |

#### Permissions

- `listGovernanceRiskMonitoring` → `PRODUCT_VIEW` (read) · staff
- `decideCatalogueAiFinding` → `AI_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Catalogue, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-137` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-137`
- Workshop pack: Product_Lifecycle___Catalogue_Governance_Reference.pdf board 2
- Flow F153 *Product Lifecycle Catalogue Governance board 2: Product Governance Command …*, step 18: Works in Governance Risk, AI Monitoring & Control Center → Use TICVAI intelligence to continuously identify catalogue governance risks rather than relying entirely on administrators to discover them manually.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-137?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Decide catalogue AI finding.
- [ ] Every transition is wired: `ADM-128`.
- [ ] Every gated control is gated: `AI_APPROVE`, `PRODUCT_VIEW`.
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

### In P09 · Catalogue

- Chinmay: reduce the number of configuration screens/pages and consolidate related settings/toggles to avoid a long, click-heavy admin flow; Allam agreed, citing the previous system's demo as a starting reference. *(agreed · MoM 25 Aug 2026, 4.11 UX Simplification & Distributed Inventory · DI-474)*

**13 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"approveReviewDecision": {"method":"PUT","path":"/review-decision","contract":"catalogue","summary":"Approval Review & Decision Workspace","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalReviewDecisionWorkspaceInput","responds":"ApprovalReviewDecisionWorkspaceView"},
"approveWorkflow": {"method":"PUT","path":"/workflow","contract":"catalogue","summary":"Approval Workflow Designer","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalWorkflowDesignerInput","responds":"ApprovalWorkflowDesignerView"},
"decideCatalogueAiFinding": {"method":"POST","path":"/ai-findings/{findingId}/decision","contract":"catalogue","summary":"Acknowledge, accept, dismiss or resolve an AI finding","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CatalogueAiFinding"},
"listChangeImpactAnalysis": {"method":"GET","path":"/change-impact-analysi","contract":"catalogue","summary":"Change Impact Analysis","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"changeRequestId","in":"query","required":false},{"name":"productId","in":"query","required":false},{"name":"area","in":"query","required":false},{"name":"minRisk","in":"query","required":false}],"requestBody":null,"responds":"ChangeImpactAnalysisView"},
"listChangePropagationDependency": {"method":"GET","path":"/change-propagation-dependency","contract":"catalogue","summary":"Change Propagation & Dependency Control","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":false},{"name":"changeRequestId","in":"query","required":false},{"name":"dependencyType","in":"query","required":false},{"name":"conflictsOnly","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listGovernanceRiskMonitoring": {"method":"GET","path":"/governance-risk-monitoring","contract":"catalogue","summary":"Governance Risk, AI Monitoring & Control Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"severity","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"owner","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductGovernance": {"method":"GET","path":"/product-governance","contract":"catalogue","summary":"Product Governance Command Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":false},{"name":"productType","in":"query","required":false},{"name":"owner","in":"query","required":false},{"name":"department","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":"changeType","in":"query","required":false},{"name":"approver","in":"query","required":false},{"name":"effectiveFrom","in":"query","required":false},{"name":"effectiveTo","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductRetirementSuspension": {"method":"GET","path":"/product-retirement-suspension","contract":"catalogue","summary":"Product Retirement, Suspension & Archive","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"action","in":"query","required":false},{"name":"lifecycleState","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductTrailChange": {"method":"GET","path":"/product-trail-change","contract":"catalogue","summary":"Product Audit Trail & Change History","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":false},{"name":"userId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":"action","in":"query","required":false},{"name":"version","in":"query","required":false},{"name":"configurationArea","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"approval","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":"environment","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductVersions": {"method":"GET","path":"/products/{productId}/versions","contract":"catalogue","summary":"What this product used to be","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProductVersion"},
"listRollbackRecovery": {"method":"GET","path":"/rollback-recovery","contract":"catalogue","summary":"Rollback & Recovery Management","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"scope","in":"query","required":false},{"name":"emergency","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setProductLinks": {"method":"PUT","path":"/products/{productId}/links","contract":"catalogue","summary":"Replace what depends on a product","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ProductLink","responds":"ProductLink"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApprovalReviewDecisionWorkspaceInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Approval Review & Decision Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"decision":{"type":"string","enum":["approve","reject","requestChanges","reassign","delegate","escalate"],"description":"Approver action (pack p.18)"},"assignToPrincipalId":{"type":"string","description":"New approver for reassign/delegate/escalate","nullable":true},"changeRequestId":{"type":"string","description":"Change request id","format":"uuid"},"comment":{"type":"string","description":"Comment; required for reject and requestChanges","nullable":true}}},
"ApprovalReviewDecisionWorkspaceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Approval Review & Decision Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"approvalStatus":{"type":"string","description":"Approval status after this decision: pending, changesRequested, approved, rejected, escalated or withdrawn"},"requester":{"type":"string","description":"Requester (display name)"},"reasonForChange":{"type":"string","description":"Reason for change"},"businessJustification":{"type":"string","description":"Business justification"},"attachments":{"type":"array","items":{"type":"object","properties":{"fileId":{"type":"string"},"name":{"type":"string"}}},"description":"Attachments"},"effectiveDate":{"type":"string","description":"Effective date; empty = on approval","format":"date","nullable":true},"currentSales":{"type":"integer","description":"Tickets sold under the current version"},"futureReservations":{"type":"integer","description":"Future reservations of the product"},"channelsAffected":{"type":"array","items":{"$ref":"#/components/schemas/Channel"},"description":"Channels affected"},"pricingImpact":{"type":"string","description":"Pricing impact in plain language; the figures are in comparison"},"capacityImpact":{"type":"integer","description":"Change in capacity units (negative = reduction)"},"financeImpact":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Estimated revenue difference over future reservations and forecast sales; advisory"},"accessImpact":{"type":"string","description":"Access impact in plain language"},"changeRequestId":{"type":"string","description":"Change request id","format":"uuid"},"productId":{"type":"string","description":"Product id","format":"uuid"},"comparison":{"type":"array","items":{"type":"object","properties":{"configurationArea":{"type":"string","enum":["basicInformation","validity","pricing","capacity","entitlements","eligibility","media","channels","policies","relationships","lifecycle"]},"field":{"type":"string"},"currentValue":{"type":"string","nullable":true},"proposedValue":{"type":"string","nullable":true},"changed":{"type":"boolean"}}},"description":"Change comparison, current vs proposed; changed rows are highlighted"},"aiSummary":{"type":"string","description":"AI summary of the proposed change; advisory, the AI does not approve","nullable":true}}},
"ApprovalWorkflowDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Approval Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"workflowName":{"type":"string","description":"Workflow name"},"applicableProductTypes":{"type":"array","items":{"$ref":"#/components/schemas/ProductKind"},"description":"Applicable product types; empty = all"},"venue":{"type":"string","description":"Venue id; empty = all venues","nullable":true},"department":{"type":"string","description":"Department","nullable":true},"changeTypes":{"type":"array","items":{"type":"string","enum":["newProduct","description","price","validity","capacity","entitlement","eligibility","tax","channel","media","policy","relationship","retirement"]},"description":"Change types routed to this workflow (Conditional Approval: e.g. price -> Commercial + Finance)"},"approvalStages":{"type":"array","items":{"type":"object","properties":{"order":{"type":"integer","description":"Stage order; stages sharing an order run in parallel, otherwise sequential"},"name":{"type":"string"},"approverRole":{"type":"string","nullable":true},"specificApproverId":{"type":"string","nullable":true},"approvalGroupId":{"type":"string","nullable":true},"mandatory":{"type":"boolean"},"slaHours":{"type":"integer","description":"SLA in hours"},"escalateToRole":{"type":"string","nullable":true,"description":"Escalation when the SLA is missed"},"delegationAllowed":{"type":"boolean"},"reminderEveryHours":{"type":"integer","nullable":true,"description":"Reminder frequency"}}},"description":"Approval stages, e.g. Product Manager -> Commercial Manager -> Operations -> Finance -> Final Approval; each stage names a role, a specific approver or a group"},"rejectionBehavior":{"type":"string","enum":["returnToDraft","returnToPreviousStage","closeRequest"],"description":"What happens on rejection; default returnToDraft (decided 29 September, readiness close-out)"},"resubmissionBehavior":{"type":"string","enum":["restartFromFirstStage","resumeAtRejectingStage"],"description":"Where a resubmitted request re-enters; default restartFromFirstStage (decided 29 September, readiness close-out)"},"workflowId":{"type":"string","description":"Existing workflow to change; empty to create","format":"uuid","nullable":true}}},
"ApprovalWorkflowDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Approval Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflowName":{"type":"string","description":"Workflow name"},"applicableProductTypes":{"type":"array","items":{"$ref":"#/components/schemas/ProductKind"},"description":"Applicable product types; empty = all"},"venue":{"type":"string","description":"Venue id; empty = all venues","nullable":true},"department":{"type":"string","description":"Department","nullable":true},"changeTypes":{"type":"array","items":{"type":"string","enum":["newProduct","description","price","validity","capacity","entitlement","eligibility","tax","channel","media","policy","relationship","retirement"]},"description":"Change types routed to this workflow (Conditional Approval: e.g. price -> Commercial + Finance)"},"approvalStages":{"type":"array","items":{"type":"object","properties":{"order":{"type":"integer","description":"Stage order; stages sharing an order run in parallel, otherwise sequential"},"name":{"type":"string"},"approverRole":{"type":"string","nullable":true},"specificApproverId":{"type":"string","nullable":true},"approvalGroupId":{"type":"string","nullable":true},"mandatory":{"type":"boolean"},"slaHours":{"type":"integer","description":"SLA in hours"},"escalateToRole":{"type":"string","nullable":true,"description":"Escalation when the SLA is missed"},"delegationAllowed":{"type":"boolean"},"reminderEveryHours":{"type":"integer","nullable":true,"description":"Reminder frequency"}}},"description":"Approval stages, e.g. Product Manager -> Commercial Manager -> Operations -> Finance -> Final Approval; each stage names a role, a specific approver or a group"},"rejectionBehavior":{"type":"string","enum":["returnToDraft","returnToPreviousStage","closeRequest"],"description":"What happens on rejection; default returnToDraft (decided 29 September, readiness close-out)"},"resubmissionBehavior":{"type":"string","enum":["restartFromFirstStage","resumeAtRejectingStage"],"description":"Where a resubmitted request re-enters; default restartFromFirstStage (decided 29 September, readiness close-out)"},"workflowId":{"type":"string","description":"Workflow id","format":"uuid"}}},
"CatalogueAiFinding": {"type":"object","x-ticvai-persistence":"catalogue.ai_finding","description":"**Something the AI noticed about the catalogue or its channels, for a person to act on** (29 September, data model DM3). Merges governance risks (ADM-137) and channel optimisation recommendations (ADM-272). Advisory only: a finding never changes configuration; acting on it goes through the ordinary operations and their approvals. **Created by the AI monitoring job** (29 September, writers pass); a person acknowledges, accepts, dismisses or resolves it with `decideCatalogueAiFinding`, and the job resolves one whose condition has cleared (`states/catalogue-ai-finding.yaml`).","required":["id","scopePath","domain","findingType","status","detectedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"domain":{"type":"string","enum":["productGovernance","channel"]},"findingType":{"type":"string","maxLength":60,"description":"Governance: the `risk` value; channel: the recommendation `category`."},"productId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"salesChannelIds":{"type":"array","items":{"type":"string","format":"uuid"}},"severity":{"type":"string","enum":["critical","high","medium","low",null],"nullable":true},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1},"summary":{"type":"string","description":"The recommendation, or the risk in one line."},"explanation":{"type":"string","nullable":true},"businessImpact":{"type":"string","nullable":true},"recommendedAction":{"type":"string","nullable":true},"constraints":{"type":"array","items":{"type":"string"}},"signals":{"type":"array","items":{"type":"string"}},"simulation":{"type":"object","additionalProperties":true,"nullable":true,"description":"Channel findings: `{expectedUnitsSold, revenueImpact, channelUtilization, risk, contractualConstraints}`."},"requiredApproval":{"type":"string","maxLength":100,"nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"dueDate":{"type":"string","format":"date","nullable":true},"status":{"type":"string","enum":["open","acknowledged","accepted","dismissed","resolved"],"default":"open"},"modelVersion":{"type":"string","maxLength":60,"nullable":true},"detectedAt":{"type":"string","format":"date-time","readOnly":true},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"ChangeImpactAnalysisView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Change Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"area":{"type":"string","enum":["futureOrders","reservations","issuedTickets","capacity","pricing","tax","promotions","membership","entitlements","accessControl","salesChannels","b2bPartners","otas","pos","b2c","kiosk","media","finance","reporting"],"description":"Impact area (pack p.21-22)"},"changeRequestId":{"type":"string","description":"Change request analysed","format":"uuid"},"affectedCount":{"type":"integer","description":"How many items in this area are affected (orders, reservations, agreements, channels...)"},"riskLevel":{"type":"string","enum":["low","medium","high","critical"],"description":"Risk classification"},"explanation":{"type":"string","description":"AI explanation in business language; advisory","nullable":true}}},
"ChangePropagationDependencyControlView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Change Propagation & Dependency Control displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"dependencyType":{"type":"string","enum":["parentProduct","childProduct","bundle","addOn","upgrade","membership","package","promotion","priceProfile","capacityPool","entitlement","salesChannel","mediaTemplate"],"description":"Dependency type (pack pp.22-23)"},"propagate":{"type":"boolean","description":"Whether the change will propagate to this linked object"},"localOverrideConflict":{"type":"boolean","description":"The linked object has a local override the change would overwrite"},"linkId":{"type":"string","description":"Link id","format":"uuid"},"sourceProductId":{"type":"string","description":"Master product","format":"uuid"},"linkedObjectId":{"type":"string","description":"Linked product or configuration id"},"linkedObjectName":{"type":"string","description":"Linked object name"},"overriddenFields":{"type":"array","items":{"type":"string"},"description":"Fields the linked object overrides locally"}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"GovernanceRiskAiMonitoringControlCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Governance Risk, AI Monitoring & Control Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"risk":{"type":"string","enum":["productWithoutOwner","missingApproval","outdatedPricing","conflictingValidity","missingChannelConfiguration","orphanedDependency","unusedProduct","duplicateProduct","unusualConfigurationChange","highOverrideLevel","scheduledPublicationConflict","expiredCommercialConfiguration","activeAfterEventEnd","brokenDependency"],"description":"Risk detected (AI Monitoring, pack p.26)"},"product":{"type":"string","description":"Product name"},"venue":{"type":"string","description":"Venue name"},"businessImpact":{"type":"string","description":"Business impact, in plain language"},"recommendedAction":{"type":"string","description":"Recommended action; advisory"},"owner":{"type":"string","description":"Owner (display name)","nullable":true},"dueDate":{"type":"string","description":"Due date","format":"date","nullable":true},"status":{"type":"string","description":"Status: open, acknowledged, inRemediation, resolved or dismissed (decided 29 September, readiness close-out)"},"riskId":{"type":"string","description":"Risk id","format":"uuid"},"productId":{"type":"string","description":"Product id","format":"uuid","nullable":true},"severity":{"type":"string","enum":["critical","high","medium","low"],"description":"Severity (Risk Dashboard)"},"explanation":{"type":"string","description":"AI explanation, e.g. the two products share 96% of their configuration; advisory"},"detectedAt":{"type":"string","description":"Detected","format":"date-time"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProductAuditTrailChangeHistoryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Product Audit Trail & Change History displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"dateTime":{"type":"string","description":"Date/time","format":"date-time"},"user":{"type":"string","description":"User (display name)"},"role":{"type":"string","description":"Role at the time"},"product":{"type":"string","description":"Product name"},"version":{"type":"integer","nullable":true,"description":"Product version"},"action":{"type":"string","enum":["created","updated","submitted","approved","rejected","changesRequested","scheduled","published","rolledBack","suspended","retired","archived","imported","exported","duplicated"],"description":"Action (decided 29 September, readiness close-out)"},"configurationArea":{"type":"string","enum":["basicInformation","validity","pricing","capacity","entitlements","eligibility","media","channels","policies","relationships","lifecycle"],"description":"Configuration area"},"previousValue":{"type":"string","description":"Previous value","nullable":true},"newValue":{"type":"string","description":"New value","nullable":true},"reason":{"type":"string","description":"Reason","nullable":true},"approvalReference":{"type":"string","description":"Approval reference (change request id)","nullable":true},"sourceChannel":{"type":"string","enum":["backOffice","api","bulkImport","environmentTransfer","scheduler","aiAssistant"],"description":"Where the change was made (decided 29 September, readiness close-out)"},"environment":{"type":"string","enum":["development","sandbox","uat","staging","production"],"description":"Environment"},"deviceMetadata":{"type":"object","nullable":true,"properties":{"ipAddress":{"type":"string"},"userAgent":{"type":"string"},"deviceId":{"type":"string","nullable":true}},"description":"IP/device metadata where applicable"},"auditId":{"type":"string","description":"Audit entry id","format":"uuid"},"productId":{"type":"string","description":"Product id","format":"uuid"},"userId":{"type":"string","description":"User principal id","format":"uuid"}}},
"ProductGovernanceCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Product Governance Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"productsAwaitingApproval":{"type":"integer","description":"Products awaiting approval"},"changesAwaitingApproval":{"type":"integer","description":"Changes awaiting approval"},"rejectedChanges":{"type":"integer","description":"Rejected changes (last 30 days) (decided 29 September, readiness close-out)"},"productsWithGovernanceWarnings":{"type":"integer","description":"Products with governance warnings"},"scheduledChanges":{"type":"integer","description":"Scheduled changes"},"productsWithUnpublishedChanges":{"type":"integer","description":"Products with unpublished changes"},"productsWithDependencyConflicts":{"type":"integer","description":"Products with dependency conflicts"},"productsApproachingRetirement":{"type":"integer","description":"Products approaching retirement: retirement date within 30 days (decided 29 September, readiness close-out)"},"recentlyPublishedVersions":{"type":"integer","description":"Recently published versions: published in the last 7 days (decided 29 September, readiness close-out)"},"failedPublications":{"type":"integer","description":"Failed publications"},"failedRollbacks":{"type":"integer","description":"Failed rollbacks"},"highRiskConfigurationChanges":{"type":"integer","description":"High-risk configuration changes (riskLevel high or critical) awaiting decision"}}},
"ProductGovernanceCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Product Governance Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"product":{"type":"string","description":"Product name"},"venue":{"type":"string","description":"Venue name"},"productOwner":{"type":"string","description":"Product owner (display name)"},"changeType":{"type":"string","enum":["newProduct","description","price","validity","capacity","entitlement","eligibility","tax","channel","media","policy","relationship","retirement"],"description":"Change type (decided 29 September, readiness close-out)"},"currentVersion":{"type":"integer","nullable":true,"description":"Current version number (ProductVersion.version); empty for a new product"},"proposedVersion":{"type":"integer","description":"Proposed version number"},"requestedBy":{"type":"string","description":"Requested by (display name)"},"requestedDate":{"type":"string","description":"Requested date-time","format":"date-time"},"riskLevel":{"type":"string","enum":["low","medium","high","critical"],"description":"Risk level"},"approvalStatus":{"type":"string","description":"Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn"},"effectiveDate":{"type":"string","description":"Effective date of the change; empty = on approval","format":"date","nullable":true},"impactedChannels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"},"description":"Impacted channels"},"assignedApprover":{"type":"string","description":"Assigned approver (display name)","nullable":true},"changeRequestId":{"type":"string","description":"Change request id","format":"uuid"},"productId":{"type":"string","description":"Product id","format":"uuid"},"lifecycleState":{"allOf":[{"$ref":"#/components/schemas/ProductLifecycleState"}],"description":"Product's current lifecycle state"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27)"}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductLink": {"type":"object","x-ticvai-persistence":"catalogue.product_link","description":"**What depends on a product, so a change can be propagated or held** (29 September, data model DM3). ADM-134. `propagatesChanges` says whether an approved change to the source flows to the linked object; `overriddenFields` are the local overrides a propagation must not overwrite (a conflict is reported, not resolved silently).","required":["id","scopePath","sourceProductId","dependencyType","linkedObjectId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"sourceProductId":{"type":"string","format":"uuid"},"dependencyType":{"type":"string","enum":["parentProduct","childProduct","bundle","addOn","upgrade","membership","package","promotion","priceProfile","capacityPool","entitlement","salesChannel","mediaTemplate"]},"linkedObjectId":{"type":"string","format":"uuid"},"linkedObjectName":{"type":"string","maxLength":200,"nullable":true},"propagatesChanges":{"type":"boolean","default":true},"overriddenFields":{"type":"array","items":{"type":"string"}},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ProductRetirementSuspensionArchiveView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Product Retirement, Suspension & Archive displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"action":{"type":"string","enum":["suspendSales","temporarilyDisable","endSale","retire","archive"],"description":"End-of-life action (Available Actions, pack pp.23-24)"},"retirementDate":{"type":"string","description":"Retirement date","format":"date","nullable":true},"endOfSaleDate":{"type":"string","description":"End-of-sale date","format":"date","nullable":true},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"},"description":"Channels the action applies to; empty = all"},"reason":{"type":"string","description":"Reason"},"replacementProductId":{"type":"string","description":"Replacement product","format":"uuid","nullable":true},"existingReservationTreatment":{"type":"string","enum":["honour","moveToReplacement","cancel"],"description":"Existing reservation treatment; default honour (decided 29 September, readiness close-out)"},"existingTicketTreatment":{"type":"string","enum":["remainValid","exchangeForReplacement","invalidate"],"description":"Existing ticket treatment; default remainValid, and invalidate needs its own governed approval (decided 29 September, readiness close-out)"},"communicationRequirements":{"type":"string","description":"Communication requirements to holders and staff","nullable":true},"reportingTreatment":{"type":"string","enum":["keepInReports","reportUnderReplacement","historicalOnly"],"description":"Reporting treatment; default keepInReports (decided 29 September, readiness close-out)"},"activePromotions":{"type":"integer","description":"Active promotions"},"bundles":{"type":"integer","description":"Bundles"},"membershipBenefits":{"type":"integer","description":"Membership benefits"},"resellerAgreements":{"type":"integer","description":"Reseller agreements"},"futureReservations":{"type":"integer","description":"Future reservations"},"activePriceLists":{"type":"integer","description":"Active price lists"},"channelAssignments":{"type":"integer","description":"Channel assignments"},"productId":{"type":"string","description":"Product id","format":"uuid"},"productName":{"type":"string","description":"Product name"},"lifecycleState":{"allOf":[{"$ref":"#/components/schemas/ProductLifecycleState"}],"description":"Current lifecycle state"},"upgradePaths":{"type":"integer","description":"Upgrade paths"}}},
"ProductVersion": {"type":"object","x-ticvai-persistence":"catalogue.product_version","description":"1.1.47, 1.4.9 to 1.4.11. **Follows `white-label.ConfigVersion`** — the same pattern for the same reason, and the fourth place this mechanism was asked for.\n","required":["version","publishedAt","publishedByPrincipalId"],"properties":{"version":{"type":"integer"},"productId":{"type":"string","format":"uuid"},"publishedAt":{"type":"string","format":"date-time"},"publishedByPrincipalId":{"type":"string","format":"uuid"},"note":{"type":"string","nullable":true},"isCurrent":{"type":"boolean"},"contentHash":{"type":"string","description":"**Lets a diff be cheap and a no-op change be recognised.** Republishing an unchanged product should not create a version.\n"},"restoredFromVersion":{"type":"integer","nullable":true,"description":"Set where this version was created by a restore. **A restore is a new version, not a rewind** — a price that was wrong for three days stays visible, because a finance query run next quarter has to reproduce what was charged.\n"}}},
"RollbackRecoveryManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Rollback & Recovery Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"dependencies":{"type":"array","items":{"type":"string"},"description":"Dependencies identified for the rollback"},"reason":{"type":"string","description":"Rollback reason (mandatory)"},"executionMode":{"type":"string","enum":["immediate","scheduled"],"description":"Immediate (where authorised) or scheduled"},"status":{"type":"string","description":"Rollback status: requested, awaitingApproval, scheduled, executing, completed, failed or cancelled"},"scope":{"type":"array","items":{"type":"string","enum":["entireProduct","pricingAssociation","channelAssociation","validityConfiguration","media","policy","entitlementConfiguration"]},"description":"Rollback scope"},"rollbackId":{"type":"string","description":"Rollback id","format":"uuid"},"productId":{"type":"string","description":"Product id","format":"uuid"},"productName":{"type":"string","description":"Product name"},"fromVersion":{"type":"integer","description":"Current version rolled back from"},"toVersion":{"type":"integer","description":"Earlier version restored"},"emergency":{"type":"boolean","description":"Emergency rollback"},"scheduledAt":{"type":"string","description":"Scheduled time","format":"date-time","nullable":true},"requestedBy":{"type":"string","description":"Requested by (display name)"},"requestedAt":{"type":"string","description":"Requested","format":"date-time"},"completedAt":{"type":"string","description":"Completed","format":"date-time","nullable":true},"approvalReference":{"type":"string","description":"Approval reference","nullable":true}}}
}
```
