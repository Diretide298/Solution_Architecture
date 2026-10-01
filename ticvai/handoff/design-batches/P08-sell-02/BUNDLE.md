# P08-sell-02 — P08 · Sell (2 of 4)

**10 screens · 42 operations · 56 schemas · 15 permissions**

Platform P08 Venue Management · ships as **venue-management** ·
staff audience · web ·
online only

## Who this is for

**staff on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 15 permissions apply here:
  `ACCESS_VALIDATE, AI_USE, CAPACITY_CONFIGURE, EVENT_CONFIGURE, ORDER_CREATE, ORDER_VIEW, PERFORMANCE_CONFIGURE, PRODUCT_CONFIGURE, PRODUCT_VIEW, REGION_CONFIGURE, SCOPE_VIEW, TENANT_CONFIGURE`…. A control nobody can use must say so,
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
| `BO-018` | Allocation & Holds | B–D | 14 | 26 | 6 | 3 | 2 | 0 | — | notStarted (generated) |
| `BO-019` | Closures & Blackouts | B–D | 44 | 40 | 6 | 38 | 1 | 0 | — | notStarted (generated) |
| `BO-037` | Offline Package Status | B–D | 52 | 57 | 6 | 10 | 0 | 0 | — | notStarted (generated) |
| `BO-063` | Opening Hours & Calendar | B–D | 47 | 63 | 6 | 55 | 2 | 0 | — | notStarted (generated) |
| `BO-102` | Sell | B–D | 2 | 42 | 6 | 68 | 0 | 0 | — | notStarted (generated) |
| `BO-109` | Menu Builder & POS Layout Designer | B–D | 37 | 14 | 6 | 8 | 2 | 2 | — | notStarted (generated) |
| `BO-110` | Recipe & BOM Management | A | 10 | 8 | 6 | 6 | 2 | 2 | — | notStarted (generated) |
| `BO-111` | Ingredient Substitution, Allergen & Nutrition | B–D | 31 | 11 | 5 | 6 | 1 | 0 | — | notStarted (generated) |
| `BO-112` | Production Planning & Production Sheets | B–D | 20 | 0 | 5 | 9 | 1 | 0 | — | notStarted (generated) |
| `BO-113` | Central Kitchen & Commissary Management | B–D | 23 | 0 | 5 | 9 | 0 | 3 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-018` Allocation & Holds

**See who is holding capacity, and release it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `ORDER_CREATE`, `PRODUCT_VIEW` (1 configure, 1 operate, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listInventoryHolds` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `inventoryHoldId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/allocation-holds` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Channel capacity id | picker: choose a channel capacity (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?channelCapacityId=` to `listInventoryHolds`. | `listInventoryHolds` ?channelCapacityId |
| Holder workstation id | picker: choose a holder workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?holderWorkstationId=` to `listInventoryHolds`. | `listInventoryHolds` ?holderWorkstationId |
| Status | radio group | optional | — | Active · Expired · Released · Force released · Converted | — | Sends `?status=` to `listInventoryHolds`. | `listInventoryHolds` ?status |

**Form: Acquire inventory hold** (modal, opened by *Acquire inventory hold*; *Acquire inventory hold* calls `acquireInventoryHold`, *Cancel* sends nothing)

**Collects what `acquireInventoryHold` sends before it is called.** Required: `id`, `channelCapacityId`, `requestedUnits`, `ttlSeconds`. Optional: `channel`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Holder kind `holderKind` | segmented control | optional | Workstation | Workstation · Cart | — | Who holds the units (decided 29 September, SD-023). A till, kiosk or edge node holds as a `workstation`; a guest's web or app cart holds as a `cart`, acquired by the order service. | `acquireInventoryHold` body |
| Cart `cartId` | picker: choose a cart | optional | — | Required when `holderKind` is `cart`, else `400`. | shows names, sends the id | Required when `holderKind` is `cart`, else `400`. Sent by the order service from `orders.addCartLine` (SD-023, 29 September). | `acquireInventoryHold` body |
| Channel `channel` | select | optional | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | Which channel's allocation to draw from. Defaults to the session's channel. | `acquireInventoryHold` body |
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key. | `acquireInventoryHold` body |
| Channel capacity `channelCapacityId` | picker: choose a channel capacity | required | — | — | shows names, sends the id | — | `acquireInventoryHold` body |
| Requested units `requestedUnits` | number field | required | — | min 1 | — | — | `acquireInventoryHold` body |
| Ttl seconds `ttlSeconds` | number field (seconds) | required | 900 | min 30; max 3600 | — | Short TTLs limit stranding when a terminal dies; long TTLs survive longer outages. | `acquireInventoryHold` body |

Errors to draw in the form: 403 Not permitted at the requested scope (`forbidden`), or a `cart` hold for a performance whose waiting room is on without a valid admission token …; 409 No units remain, or the envelope is seated — seated inventory cannot be leased because a seat map is not a count.

**Form: Release inventory hold** (modal, opened by *Release inventory hold*; *Release inventory hold* calls `relinquishInventoryHold`, *Cancel* sends nothing)

**Collects what `relinquishInventoryHold` sends before it is called.** Required: `consumedUnits`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Consumed units `consumedUnits` | number field | required | — | min 0 | — | — | `relinquishInventoryHold` body |

Errors to draw in the form: 400 `consumedUnits` is more than `grantedUnits`, or less than the consumption already reported on this hold — units reported sold stay sold.; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The hold is not `active`: it was already released, force-released or has expired, and its units are already back in the pool.

**Form: Renew inventory hold** (modal, opened by *Renew inventory hold*; *Renew inventory hold* calls `renewInventoryHold`, *Cancel* sends nothing)

**Collects what `renewInventoryHold` sends before it is called.** Required: `consumedUnits`. Optional: `additionalUnits`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Consumed units `consumedUnits` | number field | required | — | min 0 | — | — | `renewInventoryHold` body |
| Additional units `additionalUnits` | number field | optional | — | min 0 | — | Request more on top of the existing hold. | `renewInventoryHold` body |

Errors to draw in the form: 400 `consumedUnits` is more than `grantedUnits`, or less than the consumption already reported on this hold.; 409 The hold is not `active` — it expired, or was released or force-released. Acquire a new one.

**Sent by *Force release inventory hold*** (`forceReleaseInventoryHold`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `forceReleaseInventoryHold` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every inventory hold** (data table, from `listInventoryHolds`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | — |
| Channel capacity | the name it points at, never the id | — |
| Holder workstation | the name it points at, never the id | The holding workstation when `holderKind` is `workstation`; null on a cart hold, because a browser has none (SD-023, 29 September). |
| Parent lease | text | Present when sub-leased from a venue edge node. |
| Requested units | 1,234 | — |
| Channel | chip: POS, Kiosk, Web, Mobile, B2B, Ota… | Allocation this lease draws from. |
| Granted units | 1,234 | May be less than requested — a partial grant is not an error. Constrained by the channel's remaining allocation plus the general pool … |
| Consumed units | 1,234 | — |
| Status | chip: Active, Expired, Released, Force released, Converted | `states/lease.yaml`. `expired` is set by that model's timer transition when `expiresAt` passes without a renewal, not by any operation in … |
| Acquired at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Released at | 1 Oct 2026, 14:30 | — |

**The selected inventory hold** (detail panel, from `listInventoryHolds`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | — |
| Channel capacity | the name it points at, never the id | — |
| Holder workstation | the name it points at, never the id | The holding workstation when `holderKind` is `workstation`; null on a cart hold, because a browser has none (SD-023, 29 September). |
| Parent lease | text | Present when sub-leased from a venue edge node. |
| Requested units | 1,234 | — |
| Channel | chip: POS, Kiosk, Web, Mobile, B2B, Ota… | Allocation this lease draws from. |
| Granted units | 1,234 | May be less than requested — a partial grant is not an error. Constrained by the channel's remaining allocation plus the general pool … |
| Consumed units | 1,234 | — |
| Status | chip: Active, Expired, Released, Force released, Converted | `states/lease.yaml`. `expired` is set by that model's timer transition when `expiresAt` passes without a renewal, not by any operation in … |
| Acquired at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Released at | 1 Oct 2026, 14:30 | — |
| Force released by principal | the name it points at, never the id | — |
| Force release reason | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Acquire inventory hold (primary button) | `acquireInventoryHold` POST `/inventory-holds` | AcquireLeaseRequest | InventoryHold | 403 Not permitted at the requested scope (`forbidden`), or a `cart` hold for a performance whose waiting room is on without a valid admission token …; 409 No units remain, or the envelope is seated — seated inventory … | opens modal first |
| Force release inventory hold (destructive button) | `forceReleaseInventoryHold` POST `/inventory-holds/{inventoryHoldId}/force-release` | inline | InventoryHold | 403 Authenticated but not permitted at the requested scope | — |
| Release inventory hold (secondary button) | `relinquishInventoryHold` DELETE `/inventory-holds/{inventoryHoldId}` | inline | InventoryHold | 400 `consumedUnits` is more than `grantedUnits`, or less than the consumption already reported on this hold — units reported sold stay sold.; 404 The resource does not exist, or is outside the caller's scope. This … | opens modal first |
| Renew inventory hold (secondary button) | `renewInventoryHold` POST `/inventory-holds/{inventoryHoldId}/renew` | inline | InventoryHold | 400 `consumedUnits` is more than `grantedUnits`, or less than the consumption already reported on this hold.; 409 The hold is not `active` — it expired, or was released or force-released. Acquire a new one. | opens modal first |

**Data it reads**: `listInventoryHolds` (onLoad, List leases)

**Where the user goes next**

- → `BO-007` Product Directory: *Product Directory*
- → `BO-009` Pricing Rules: *Pricing Rules*

**What opens over it**

- confirmDialog *Force release inventory hold*: **Names what `forceReleaseInventoryHold` changes and what it leaves alone**, in the consequence rather than the verb. A allocation holds this affects should be identified in the dialog, not just counted. **Collects what `forceReleaseInventoryHold` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The allocation holds list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the allocation holds untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No allocation holds yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on channelCapacityId, holderWorkstationId, status and the allocation holds are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listInventoryHolds` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `consumedUnits` is more than `grantedUnits`, or less than the consumption already reported on this hold — units reported sold stay sold.; 400 `consumedUnits` is more than `grantedUnits`, or less than the consumption already reported on this hold.; 409 No units remain, or the envelope is seated — seated inventory cannot be leased because a seat map is not a count.; 409 The hold is not `active` … |

#### Permissions

- `listInventoryHolds` → `PRODUCT_VIEW` (read) · staff
- `acquireInventoryHold` → `ORDER_CREATE` (operate) · staff, service
- `forceReleaseInventoryHold` → `CAPACITY_CONFIGURE` (configure) · staff
- `relinquishInventoryHold` → `ORDER_CREATE` (operate) · staff
- `renewInventoryHold` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listInventoryHolds` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.9.4 | The system should allow configuration of a holding time for a capacity-based product. When a capacity-based product is added to the cart, the capacity should be reserved for configurable X minutes … | Ticketing Sales | CONTRACTED | `acquireInventoryHold` |
| 5.5.21 | Support reserving entitlements before use and automatic release if unused. | F&B & Guest Management | CONTRACTED | `acquireInventoryHold` |
| 7.4.47 | Reserve inventory during checkout and release automatically if payment is not completed within configurable timeout. Support reservation, purchased, expired and released statuses. | F&B POS | CONTRACTED | `acquireInventoryHold` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Inventory pools split capacity by ticket type (e.g. 50% GA, 30% child, 20% senior) and/or sales channel (e.g. 50% online, 50% on-site), configurable at venue/event level, under a hierarchy global → attraction → product → variant → time slot. On cancel/refund/reschedule the business chooses whether capacity is released or held. *(agreed · MoM 25 Aug 2026, 4.6 Performances & Capacity Management; 4.11 UX Simplification & Distributed Inventory · DI-457)*
- "Envelopes" split a performance's capacity by channel (e.g. of 100: 30 B2C, 40 B2B, 30 on-site); each channel shows only its own share as available. Configured once and applied to all linked performances. *(agreed · MoM 7 Aug 2026, 15. Capacity Splitting via Envelopes · DI-170)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-018` · status **notStarted** · provenance generated
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)
- ADR-0031 *Contention is leased, not locked — and where a lock is unavoidable it is named* (`docs/adr/0031-contention-and-locking.md`)
- ADR-0066 *The on-sale waiting room sits at the edge, apart from the ride queue* (`docs/adr/0066-the-on-sale-waiting-room-is-separate-from-the-ride-queue.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-018?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Acquire inventory hold, Force release inventory hold, Release inventory hold, Renew inventory hold.
- [ ] Every transition is wired: `BO-007`, `BO-009`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `ORDER_CREATE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-019` Closures & Blackouts

**Stop selling something, for a reason.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `EVENT_CONFIGURE`, `PERFORMANCE_CONFIGURE`, `PRODUCT_VIEW`, `VENUE_MAP_MANAGE` (3 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listPerformances` reads the population and `getEvent` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `eventId` (deepLink), `performanceId` (deepLink), `mapId` (navigation), `pathId` (navigation) · cold entry: **A link to a performance that has happened.** Offers the next performance of the same event. |
| Route | `/venue-operations/closures-blackouts` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Drawn 26 August** — `Seat Board 2.dc.html` frame `seat-2d`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?from=` to `listPerformances`. | `listPerformances` ?from |
| To | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?to=` to `listPerformances`. | `listPerformances` ?to |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Section code | text field | — | — | `getSeatAvailability` ?sectionCode |
| Category | picker: choose a category | — | — | `getSeatAvailability` ?categoryId |
| Available only | toggle | off | — | `getSeatAvailability` ?availableOnly |
| Mode | segmented control | Auto | Auto · Graphical · List | `getSeatAvailability` ?mode |

**Form: Create event** (modal, opened by *Create event*; *Create event* calls `createEvent`, *Cancel* sends nothing)

**Collects what `createEvent` sends before it is called.** Required: `code`, `name`, `venueId`. Optional: `parentEventId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64; A code already used by any event in the tenant is refused with `409 duplicate-code`. | — | Unique per tenant (decided 28 September, audit R108). A code already used by any event in the tenant is refused with `409 duplicate-code`. | `createEvent` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createEvent` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createEvent` body |
| Parent event `parentEventId` | picker: choose a parent event | optional | — | — | shows names, sends the id | — | `createEvent` body |

Errors to draw in the form: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …

**Form: Create performances** (modal, opened by *Create performances*; *Create performances* calls `createPerformances`, *Cancel* sends nothing)

**Collects what `createPerformances` sends before it is called.** Required: `startsAt`, `endsAt`. Optional: `admissionRulesId`, `seatMapId`, `recurrence`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPerformances` body |
| Ends at `endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPerformances` body |
| Admission rules `admissionRulesId` | picker: choose an admission rules | optional | — | — | shows names, sends the id | — | `createPerformances` body |
| Seat map `seatMapId` | picker: choose a seat map | optional | — | — | shows names, sends the id | — | `createPerformances` body |
| Language `language` | text field | optional | — | max length 35; pattern `^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$` | — | As `Performance.language`; every performance of a generated series takes it (decided 29 September, rev 3 REV3-17). | `createPerformances` body |
| Format `format` | text field | optional | — | max length 40 | — | As `Performance.format` (decided 29 September, rev 3 REV3-17). | `createPerformances` body |
| Recurrence `recurrence` | group | optional | — | — | — | Generate a series rather than a single performance. Read in the region's time zone: the Region owns the zone and every venue inherits it without override (tenancy), so … | `createPerformances` body |
| Interval minutes `recurrence.intervalMinutes` | number field (minutes) | optional | — | min 1 | — | — | `createPerformances` body |
| Until `recurrence.until` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPerformances` body |
| Days of week `recurrence.daysOfWeek` | list of values (chips) | optional | — | — | — | — | `createPerformances` body |

**Form: Recommend seats** (modal, opened by *Recommend seats*; *Recommend seats* calls `recommendSeats`, *Cancel* sends nothing)

**Collects what `recommendSeats` sends before it is called.** Required: `partySize`, `strategy`. Optional: `categoryIds`, `maxPrice`, `accessibleCount`, `maxOptions`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Party size `partySize` | stepper or slider | required | — | min 1; max 50 | — | — | `recommendSeats` body |
| Strategy `strategy` | radio group | required | — | Best available · Best value · Closest to stage · Accessible · Contiguous | — | — | `recommendSeats` body |
| Categorys `categoryIds` | multi-picker: choose categorys | optional | — | — | — | — | `recommendSeats` body |
| Max price `maxPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `recommendSeats` body |
| Accessible count `accessibleCount` | number field | optional | 0 | — | — | Wheelchair spaces in the party. Companions are added automatically. | `recommendSeats` body |
| Max options `maxOptions` | number field | optional | 3 | max 10 | — | — | `recommendSeats` body |

Errors to draw in the form: 404 No selection satisfies the constraints

**Form: Save event** (modal, opened by *Save event*; *Save event* calls `updateEvent`, *Cancel* sends nothing)

**Collects what `updateEvent` sends before it is called.** Nothing in the body is required. Optional: `name`, `parentEventId`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateEvent` body |
| Parent event `parentEventId` | picker: choose a parent event | optional | — | — | shows names, sends the id | — | `updateEvent` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateEvent` body |

**Form: Save performance** (modal, opened by *Save performance*; *Save performance* calls `updatePerformance`, *Cancel* sends nothing)

**Collects what `updatePerformance` sends before it is called.** Nothing in the body is required. Optional: `startsAt`, `endsAt`, `status`, `admissionRulesId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Starts at `startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePerformance` body |
| Ends at `endsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePerformance` body |
| Status `status` | segmented control | optional | — | Scheduled · On sale · Suspended | — | — | `updatePerformance` body |
| Admission rules `admissionRulesId` | picker: choose an admission rules | optional | — | — | shows names, sends the id | — | `updatePerformance` body |
| Language `language` | text field | optional | — | max length 35; pattern `^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$` | — | As `Performance.language` (decided 29 September, rev 3 REV3-17). | `updatePerformance` body |
| Format `format` | text field | optional | — | max length 40 | — | As `Performance.format` (decided 29 September, rev 3 REV3-17). | `updatePerformance` body |

Errors to draw in the form: 409 A timing change on a performance with sold tickets, or a `status` move the state model does not allow.

**Form: Save path closure** (modal, opened by *Save path closure*; *Save path closure* calls `setPathClosure`, *Cancel* sends nothing)

**Collects what `setPathClosure` sends before it is called.** Required: `isClosed`. Optional: `reason` (maintenance, incident, event, weather, crowding, other), `note`, `force`, `expectedReopenAt`. **Choosing Other makes the note required** — the form will not confirm without it and the server refuses 400 (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Is closed `isClosed` | toggle | required | — | — | — | — | `setPathClosure` body |
| Reason `reason` | select | optional | — | Maintenance · Incident · Event · Weather · Crowding · Other | — | `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222); refused `400` without one, and the notes are reviewed quarterly so the common … | `setPathClosure` body |
| Note `note` | text area | optional | — | max length 500 | — | Free text. Required where the reason is `other` (audit R222). | `setPathClosure` body |
| Force `force` | toggle | optional | off | — | — | Close it even though something becomes unreachable. | `setPathClosure` body |
| Expected reopen at `expectedReopenAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setPathClosure` body |

Errors to draw in the form: 400 Validation failed; 409 Closing this strands a point, and the response names which in `strandedPoints`. *"Cannot close"* on a park with two hundred paths is not actionable. (PathClosureProblem)

**Sent by *Cancel performance*** (`cancelPerformance`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 1000 | — | — | `cancelPerformance` body |
| Guest message `guestMessage` | key and value settings | optional | — | — | — | — | `cancelPerformance` body |
| Refund percentage `refundPercentage` | stepper or slider | optional | 100 | min 0; max 100 | — | — | `cancelPerformance` body |
| Offer alternative performance `offerAlternativePerformanceId` | picker: choose an offer alternative performance | optional | — | — | shows names, sends the id | — | `cancelPerformance` body |
| Dry run `dryRun` | toggle | optional | off | — | — | — | `cancelPerformance` body |
| Supervisor step up `supervisorStepUp` | group | optional | — | — | — | Required unless `dryRun` (audit R144, proposed by the coordinator). | `cancelPerformance` body |
| Principal `supervisorStepUp.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | The supervisor signing. Recorded against the act. | `cancelPerformance` body |
| Credential `supervisorStepUp.credential` | text area | required | — | max length 512 | — | The supervisor's staff PIN, as they sign in at a till with it. A PIN, never a password (audit R123 (7)). | `cancelPerformance` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every performance** (data table, from `listPerformances`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Event | the name it points at, never the id | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Approval request | the name it points at, never the id | BL-048. The approval chain and the occurrence lifecycle sat on different entities, so neither was complete: `states/performance.yaml` … |
| Requires approval to cancel | yes / no (icon or chip) | Cancelling a sold performance is the one transition that needs a name against it. |
| Status | chip: Scheduled, On sale, Sold out, Suspended, Cancelled, Completed | — |
| Admission rules | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |

**Every event** (data table, from `listEvents`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Parent event | the name it points at, never the id | For grouped events. |
| Performance count | 1,234 | How many performances the event has. Counted by the server; never sent by a client. |
| Is active | yes / no (icon or chip) | — |

**The selected performance** (detail panel, from `getPerformance`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Event | the name it points at, never the id | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Approval request | the name it points at, never the id | BL-048. The approval chain and the occurrence lifecycle sat on different entities, so neither was complete: `states/performance.yaml` … |
| Requires approval to cancel | yes / no (icon or chip) | Cancelling a sold performance is the one transition that needs a name against it. |
| Status | chip: Scheduled, On sale, Sold out, Suspended, Cancelled, Completed | — |
| Admission rules | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |

**The seat availability** (detail panel, from `getSeatAvailability`)

| Shows | Format | Notes |
|---|---|---|
| Performance | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |
| Render mode | chip: Graphical, List | The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat … |
| Totals | grouped details | — |
| By category | list or chips (count when long) | — |
| Seats | list or chips (count when long) | — |

**The event** (detail panel, from `getEvent`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Parent event | the name it points at, never the id | For grouped events. |
| Performance count | 1,234 | How many performances the event has. Counted by the server; never sent by a client. |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Cancel performance (destructive button) | `cancelPerformance` POST `/performances/{performanceId}/cancel` | inline | PerformanceCancellationResult | 403 The supervisor step-up is missing or failed (audit R144). The PIN did not verify, or the principal does not hold `PERFORMANCE_CONFIGURE` at this venue.; 409 The performance is `cancelled`, `completed` or `soldOut`. … | step-up: pin (Cancels a performance and queues refunds to every holder; a supervisor signs it in place (proposed by the coordinator …) |
| Create event (secondary button) | `createEvent` POST `/events` | CreateEventRequest | Event | 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … | opens modal first |
| Create performances (secondary button) | `createPerformances` POST `/events/{eventId}/performances` | CreatePerformancesRequest | inline | — | opens modal first |
| Recommend seats (secondary button) | `recommendSeats` POST `/performances/{performanceId}/seat-recommendations` | SeatRecommendationRequest | inline | 404 No selection satisfies the constraints | opens modal first |
| Save event (secondary button) | `updateEvent` PATCH `/events/{eventId}` | inline | Event | — | opens modal first |
| Save performance (secondary button) | `updatePerformance` PATCH `/performances/{performanceId}` | inline | Performance | 409 A timing change on a performance with sold tickets, or a `status` move the state model does not allow. | opens modal first |
| Save path closure (secondary button) | `setPathClosure` POST `/venue-maps/{mapId}/paths/{pathId}/closure` | inline | PathClosureResult | 400 Validation failed; 409 Closing this strands a point, and the response names which in `strandedPoints`. *"Cannot close"* on a park with two hundred paths is not actionable. (PathClosureProblem) | opens modal first |

**Data it reads**: `getPerformance` (onLoad, Read a performance); `getSeatAvailability` (onLoad, Seat status for a performance); `listEvents` (onLoad, List events)

**Where the user goes next**

- → `BO-001` Queue Directory: *Queue Directory*; carries `eventId`
- → `BO-007` Product Directory: *Product Directory*
- → `BO-009` Pricing Rules: *Pricing Rules*

**What opens over it**

- confirmDialog *Cancel performance*: **Names what `cancelPerformance` changes and what it leaves alone**, in the consequence rather than the verb. A closures blackouts this affects should be identified in the dialog, not just counted. **Collects what `cancelPerformance` sends before it is called.** Required: `reason`. Optional …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The closures blackouts list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the closures blackouts untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No closures blackouts yet. Offers Create event (`createEvent`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on from, to and the closures blackouts are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listPerformances` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 409 A timing change on a performance with sold tickets, or a `status` move the state model does not allow.; 409 Closing this strands a point, and the response names which in `strandedPoints`. *"Cannot close"* on … |

#### Permissions

- `listPerformances` → `PRODUCT_VIEW` (read) · staff, guest
- `cancelPerformance` → `PERFORMANCE_CONFIGURE` (configure) · staff · step-up pin
- `createEvent` → `EVENT_CONFIGURE` (configure) · staff
- `createPerformances` → `PERFORMANCE_CONFIGURE` (configure) · staff
- `getEvent` → `PRODUCT_VIEW` (read) · staff
- `getPerformance` → `PRODUCT_VIEW` (read) · staff, guest
- `getSeatAvailability` → `PRODUCT_VIEW` (read) · staff, guest
- `listEvents` → `PRODUCT_VIEW` (read) · staff
- `recommendSeats` → `PRODUCT_VIEW` (read) · staff, guest
- `updateEvent` → `EVENT_CONFIGURE` (configure) · staff
- `updatePerformance` → `PERFORMANCE_CONFIGURE` (configure) · staff
- `setPathClosure` → `VENUE_MAP_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listPerformances` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

38 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.34 | Time Slot Reservations - System shall support time slot reservations. | Guest Mobile App & Branding | CONTRACTED | `listPerformances` |
| 2.6.15 | - Time slots for events | Ticketing Sales | CONTRACTED | `listPerformances` |
| 2.7.16 | - Dedicated sales calendar | Ticketing Sales | CONTRACTED | `listPerformances` |
| 1.3.20 | System shall support event cancellation workflows including refunds, exchanges, notifications and audit tracking. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.3.21 | System shall support changing event dates, times and venues while automatically updating tickets, reservations and guest communications. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.4.4 | The system should propagate any changes made to the properties of a product to the already sold tickets as well. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.4.16 | System shall identify affected tickets, reservations, memberships, events and integrations before applying product changes. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.3.1 | The system should allow creation of events such as performances, workshops, activities or guided-tours. | Ticketing Catalogue | CONTRACTED | `createEvent` |
| 1.3.14 | Ability to create events with metadata (name, type, venue, date, time, organizer). The events could be free marketing, paid marketing events or show-tech events. | Ticketing Catalogue | CONTRACTED | `createEvent` |
| 1.3.29 | System shall support events spanning multiple venues, halls, spaces or locations under a single event. | Ticketing Catalogue | CONTRACTED | `createEvent` |
| 1.1.2 | The system should be able to sell dated tickets for attractions that allow access only for selected dates by guest. Special day tickets should also be supported. These are dated tickets that skip … | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.1.4 | The system should provide an easy-to-use interface for creation and configuration of timeslots. A calendar view should be available for the user to define the timeslot and recurrence rules. The user … | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| … 26 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Weekday/calendar rules give different validity and pricing to weekday-only vs. all-days products (e.g. Global Village). Blockout dates exclude some ticket types (e.g. memberships) on public holidays/special days, requiring a separate ticket for those dates. *(client request · MoM 25 Aug 2026, 4.5 Validity Management & Expiry Rules · DI-452)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-019` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Seat Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/Seat Board 2.dc.html`
- Client design-board frames: `Seat Board 2.dc.html#seat-2d`

#### Acceptance for the design

- [ ] Every input above is drawn (44), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-019?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Cancel performance, Create event, Create performances, Recommend seats, Save event, Save performance, Save path closure.
- [ ] Every transition is wired: `BO-001`, `BO-007`, `BO-009`.
- [ ] Every gated control is gated: `EVENT_CONFIGURE`, `PERFORMANCE_CONFIGURE`, `PRODUCT_VIEW`, `VENUE_MAP_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-037` Offline Package Status

**Know what each device is enforcing right now.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 1 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_VALIDATE`, `ORDER_CREATE`, `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW`… (2 operate, 3 read, 2 configure); in the flows as technician |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCatalogueBundles` reads the population and `getLatestBundle` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `version` (deepLink) · cold entry: **A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is … |
| Route | `/venue-operations/offline-package-status` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board**, answering 2 board screen(s): Offline Operations Dashboard; Offline Product & Data Cache Management. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Owns POS board frame(s) POS-5A, POS-5C** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Since | text field | — | — | `getLatestBundle` ?since |
| Since version | number field | — | — | `getOfflinePackage` ?sinceVersion |
| Valid from | date and time picker | — | — | `getOfflinePackage` ?validFrom |
| Valid to | date and time picker | — | — | `getOfflinePackage` ?validTo |
| Workstation | picker: choose a workstation | — | — | `listSyncRejections` ?workstationId |
| Kind | radio group | — | Order · Payment · Refund · Void · Scan | `listSyncRejections` ?kind |
| Resolved | toggle | — | — | `listSyncRejections` ?resolved |
| Sale board kind | radio group | — | Ticketing · Fnb · Retail · Mixed | `listWorkstations` ?saleBoardKind |

**Form: Publish bundle** (modal, opened by *Publish bundle*; *Publish bundle* calls `publishBundle`, *Cancel* sends nothing)

**Collects what `publishBundle` sends before it is called.** Required: `venueId`. Optional: `note`, `staleAfterHours`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `publishBundle` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `publishBundle` body |
| Stale after hours `staleAfterHours` | number field (hours) | optional | — | min 1 | — | How long a terminal may trade on this bundle before refusing. Defaults to the venue's configured bound. | `publishBundle` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 409 A publish is already in progress for this venue

**Form: Report bundle applied** (modal, opened by *Report bundle applied*; *Report bundle applied* calls `reportBundleApplied`, *Cancel* sends nothing)

**Collects what `reportBundleApplied` sends before it is called.** Required: `appliedAt`, `outcome`. Optional: `error`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Applied at `appliedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `reportBundleApplied` body |
| Outcome `outcome` | segmented control | required | — | Applied · Rolled back · Signature invalid | — | — | `reportBundleApplied` body |
| Error `error` | text field | optional | — | — | — | — | `reportBundleApplied` body |

**Form: Save offline policy** (modal, opened by *Save offline policy*; *Save offline policy* calls `setOfflinePolicy`, *Cancel* sends nothing)

**Collects what `setOfflinePolicy` sends before it is called.** Required: `scopePath`. Optional: `id`, `maxOfflineHours`, `allowedOffline`, `offlineValueCeiling`, `offlineTransactionCeiling`, `onCeilingBreach`, `requiresManagerToExtend`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scope path `scopePath` | text field | required | — | pattern `^[a-z0-9_]+(\.[a-z0-9_]+)*$` | — | The node this policy is for, and the key `setOfflinePolicy` upserts on. The body names its target here, because the path does not. | `setOfflinePolicy` body |
| Max offline hours `maxOfflineHours` | stepper or slider (hours) | optional | 24 | min 1; max 72 | — | After which the workstation refuses to sell rather than keep journalling. A till three days offline holding 900 unsynced sales is a reconciliation nobody can do and a fraud nobody … | `setOfflinePolicy` body |
| Allowed offline `allowedOffline` | multi-select chips | optional | — | Sale · Refund · Exchange · Entitlement issue · Entitlement validate · Loyalty accrual · Loyalty redemption · Wallet spend · Price override · Discount · Void line · No sale; Selling from a cached catalogue is safe; issuing a refund is not, because the original … | — | What may happen with no network, by data class. Selling from a cached catalogue is safe; issuing a refund is not, because the original sale cannot be verified. | `setOfflinePolicy` body |
| Offline value ceiling `offlineValueCeiling` | money field | optional | — | Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129). | AED, 2 decimals shown (up to 4 accepted), currency from the … | Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129). | `setOfflinePolicy` body |
| Offline transaction ceiling `offlineTransactionCeiling` | number field | optional | — | min 1; max 5000 | — | A ceiling on count as well as value. Nine hundred small sales and one large one are different risks, and a value ceiling alone catches only the second. | `setOfflinePolicy` body |
| On ceiling breach `onCeilingBreach` | segmented control | optional | Block new sales | Warn · Block new sales · Block all | — | — | `setOfflinePolicy` body |
| Requires manager to extend `requiresManagerToExtend` | toggle | optional | on | — | — | — | `setOfflinePolicy` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Sync orders** (modal, opened by *Sync orders*; *Sync orders* calls `syncOrders`, *Cancel* sends nothing)

**Collects what `syncOrders` sends before it is called.** Required: `deviceId`, `orders`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Device `deviceId` | picker: choose a device | required | — | — | shows names, sends the id | — | `syncOrders` body |
| Orders `orders` | repeatable rows | required | — | at least 1; at most 200 | — | — | `syncOrders` body |
| ID `orders[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. | `syncOrders` body |
| Venue `orders[].venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `syncOrders` body |
| Channel `orders[].channel` | select | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `syncOrders` body |
| Shift `orders[].shiftId` | picker: choose a shift | optional | — | — | shows names, sends the id | — | `syncOrders` body |
| Subject `orders[].subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | Null for an anonymous sale. Identity and entitlement are separate. | `syncOrders` body |
| Guest link `orders[].guestLinkId` | text field | optional | — | — | — | Present where the guest is linked across cells. | `syncOrders` body |
| Catalogue bundle version `orders[].catalogueBundleVersion` | text field | optional | — | — | — | The bundle the client priced from. Lets the server explain a variance rather than merely report one. | `syncOrders` body |
| Lines `orders[].lines` | repeatable rows | required | — | at least 1 | — | — | `syncOrders` body |
| ID `orders[].lines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `syncOrders` body |
| Variant `orders[].lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `syncOrders` body |
| Recommendation `orders[].lines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `syncOrders` body |
| Performance `orders[].lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `syncOrders` body |
| Booked window `orders[].lines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `syncOrders` body |
| Inventory hold `orders[].lines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `syncOrders` body |
| Seats `orders[].lines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `syncOrders` body |
| Resource hold `orders[].lines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `syncOrders` body |
| Attributes `orders[].lines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `syncOrders` body |
| Quantity `orders[].lines[].quantity` | number field | required | — | min 1 | — | — | `syncOrders` body |
| Eligibility declaration `orders[].lines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `syncOrders` body |
| Quoted unit price `orders[].lines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `syncOrders` body |
| Holder name `orders[].lines[].holderName` | text field | optional | — | — | — | — | `syncOrders` body |
| Data mask values `orders[].lines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `syncOrders` body |
| Recorded at `orders[].recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `syncOrders` body |
| Sequence `orders[].sequence` | number field | required | — | min 1 | — | Monotonic per device. Processed in this order. | `syncOrders` body |
| Payments `orders[].payments` | repeatable rows | required | — | — | — | — | `syncOrders` body |
| ID `orders[].payments[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header. | `syncOrders` body |
| Order `orders[].payments[].orderId` | picker: choose an order | required | — | — | shows names, sends the id | — | `syncOrders` body |
| Tender `orders[].payments[].tender` | select | required | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | — | `wallet` is a digital wallet (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 … | `syncOrders` body |
| Amount `orders[].payments[].amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `syncOrders` body |
| Tender currency `orders[].payments[].tenderCurrency` | text field | optional | — | pattern `^[A-Z]{3}$` | — | The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. | `syncOrders` body |
| Tender amount `orders[].payments[].tenderAmount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the guest handed over, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). | `syncOrders` body |
| Wallet authorisation `orders[].payments[].walletAuthorisationId` | text field | optional | — | — | — | Cross-cell wallet hold, where the guest's home cell is elsewhere. | `syncOrders` body |
| Wallet hold `orders[].payments[].walletHoldId` | picker: choose a wallet hold | optional | — | — | shows names, sends the id | For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table. | `syncOrders` body |
| Return URL `orders[].payments[].returnUrl` | URL field | optional | — | — | https:// | Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). | `syncOrders` body |
| Terminal `orders[].payments[].terminalId` | picker: choose a terminal | optional | — | — | shows names, sends the id | The card terminal to instruct, for a card payment at a till (ECR flow, SD-034). | `syncOrders` body |
| Device `orders[].payments[].deviceId` | picker: choose a device | optional | — | — | shows names, sends the id | — | `syncOrders` body |
| Recorded at `orders[].payments[].recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `syncOrders` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every bundle** (data table, from `listCatalogueBundles`)

| Shows | Format | Notes |
|---|---|---|
| Venue | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Published by | the name it points at, never the id | — |
| Content hash | text | — |
| Signature key | text | Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle. |
| Stale after | 1 Oct 2026, 14:30 | — |
| Size bytes | 1,234 | — |
| Note | text | — |
| Applied by workstations | 1,234 | — |

**Every sync rejection** (data table, from `listSyncRejections`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Workstation | the name it points at, never the id | — |
| Kind | chip: Order, Payment, Refund, Void, Scan | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Rejected at | 1 Oct 2026, 14:30 | — |
| Problem | grouped details | RFC 9457 problem details. Every error response uses this shape. |
| Payload | grouped details | Deliberately open: the journal entry exactly as the till sent it. Its shape is the request schema for `kind` — an `OfflineOrder` for … |
| Resolved at | 1 Oct 2026, 14:30 | — |
| Resolved by principal | the name it points at, never the id | — |
| Resolution | chip: Posted, Voided, Refunded | What `resolveSyncRejection` recorded. Null while the rejection waits. |
| Resolved record | the name it points at, never the id | The order, void or refund the resolution produced — what stops the entry being posted twice. |

**Every workstation** (data table, from `listWorkstations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Region | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Scope path | text | — |
| Sale board | grouped details | Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. |
| Access point | the name it points at, never the id | Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point. |
| Devices | list or chips (count when long) | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |

**The selected bundle** (detail panel, from `listCatalogueBundles`)

| Shows | Format | Notes |
|---|---|---|
| Venue | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Published by | the name it points at, never the id | — |
| Content hash | text | — |
| Signature key | text | Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle. |
| Stale after | 1 Oct 2026, 14:30 | — |
| Size bytes | 1,234 | — |
| Note | text | — |
| Applied by workstations | 1,234 | — |

**The offline package** (detail panel, from `getOfflinePackage`)

| Shows | Format | Notes |
|---|---|---|
| Generated at | 1 Oct 2026, 14:30 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Access point | the name it points at, never the id | — |
| Entitlements | list or chips (count when long) | Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device … |
| Delegated rights | list or chips (count when long) | Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits … |
| Blacklist | list or chips (count when long) | Media codes to deny outright regardless of entitlement state. |
| Admission rules | list or chips (count when long) | — |

**The catalogue bundle** (detail panel, from `getLatestBundle`)

| Shows | Format | Notes |
|---|---|---|
| Venue | the name it points at, never the id | — |
| Is delta | yes / no (icon or chip) | — |
| Base version | text | Present when `isDelta`. The version this delta applies to. |
| Signature | text | Detached signature over `contentHash`. The terminal verifies before applying and rolls back on failure — a half-applied catalogue is never … |
| Signature key | text | — |
| Content hash | text | — |
| Stale after | 1 Oct 2026, 14:30 | — |
| Payload | grouped details | Products, variants, price lists, prices, tax codes, events, performances, envelope definitions, data mask field definitions and the venue's … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Publish bundle (primary button) | `publishBundle` POST `/catalogue/bundles` | inline | BundleSummary | 403 Authenticated but not permitted at the requested scope; 409 A publish is already in progress for this venue | opens modal first |
| Report bundle applied (secondary button) | `reportBundleApplied` POST `/catalogue/bundles/{version}/applied` | inline | — | — | opens modal first |
| Save offline policy (secondary button) | `setOfflinePolicy` PUT `/offline-policy` | OfflinePolicy | OfflinePolicy | 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Sync orders (secondary button) | `syncOrders` POST `/sync/orders` | inline | OrderSyncResult | — | emits `order.paid`, `sync.rejectionRaised`; opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listCatalogueBundles` (onLoad, List published bundles); `getLatestBundle` (onLoad, Pull the current bundle for this workstation's venue); `getOfflinePackage` (onLoad, Entitlement and rule set for offline validation); `listSyncRejections` (onLoad, Entries the server refused); `listWorkstations` (onLoad, List workstations)

**Where the user goes next**

- → `BO-007` Product Directory: *Product Directory*
- → `BO-009` Pricing Rules: *Pricing Rules*
- → `BO-128` Live Workstation Health Monitor: *The fleet is monitored*; carries `workstationId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline package status list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline package status untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline package status yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCatalogueBundles` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listCatalogueBundles` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A publish is already in progress for this venue |

#### Permissions

- `listCatalogueBundles` → `PRODUCT_VIEW` (read) · staff, guest
- `getLatestBundle` → `PRODUCT_VIEW` (read) · staff
- `publishBundle` → `PRODUCT_CONFIGURE` (configure) · staff
- `reportBundleApplied` → `PRODUCT_VIEW` (read) · staff
- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `listSyncRejections` → `ORDER_VIEW` (read) · staff
- `listWorkstations` → `SCOPE_VIEW` (read) · staff
- `setOfflinePolicy` → `TENANT_CONFIGURE` (configure) · staff
- `syncOrders` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listCatalogueBundles` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.4.7 | System shall allow publishing products to selected sales channels including Website, Mobile App, POS, API and Reseller channels. | Ticketing Catalogue | CONTRACTED | `publishBundle` |
| 2.13.38 | Offline Access Validation | Ticketing Sales | CONTRACTED | `getOfflinePackage` |
| 3.1.5 | Access control devices shall validate dynamic QR codes using secure offline cryptographic validation without requiring continuous connectivity to the central platform. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.1.10 | System shall support embedding entitlement information within secure QR, RFID, NFC, mobile wallet, and digital credential tokens. Embedded information may include ticket type, seat assignment, event … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.49 | The validity check logic allows offline validity check. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.75 | The access control can be operated in offline mode. Turnstiles can perform access control in absence of database access (database unavailable or not reachable). Key access control criteria can be … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.3.30 | Distributed Policy Evaluation - System shall support local policy evaluation when offline. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 18.1.3 | Offline Mode - System shall support offline operation. | Employee Mobile App & AI Assistant | CONTRACTED | `getOfflinePackage` |
| 2.3.1 | The system should support offline mode for POS and Kiosk: - Ability to switch automatically to offline mode in case of server outage / network loss - Definition of which functionality will be lost in … | Ticketing Sales | CONTRACTED | `syncOrders` |
| 2.14.2 | For all sales at POS, it is possible to have an offline mode. | Ticketing Sales | CONTRACTED | `syncOrders` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-037` · status **notStarted** · provenance generated · **Drawn by Claude Design on `POS Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/POS Board 5.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 5.dc.html#pos-5a`, `POS Board 5.dc.html#pos-5c`, `Retail Board 3.dc.html#ret-3j`
- Flow F89 *Offline policy is set, cached, monitored and reconciled*, step 3: Each device's cached package is checked. → **What each device is enforcing right now**, not what was configured.
- Flow F89 *Offline policy is set, cached, monitored and reconciled*, step 5: What the tills did offline is reconciled. → **Every rejected offline sale is seen by a person.** A rejection nobody reads is money nobody collects.
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (52), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (57 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-037?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Publish bundle, Report bundle applied, Save offline policy, Sync orders, What publishing changes.
- [ ] Every transition is wired: `BO-007`, `BO-009`, `BO-128`.
- [ ] Every gated control is gated: `ACCESS_VALIDATE`, `ORDER_CREATE`, `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW`, `TENANT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-063` Opening Hours & Calendar

**Say when the venue is open, including the exceptions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 1 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `EVENT_CONFIGURE`, `PERFORMANCE_CONFIGURE`, `PRODUCT_VIEW`, `REGION_CONFIGURE`, `TENANT_VIEW` (3 configure, 2 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listPerformances` reads the population and `getPerformance` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `eventId` (deepLink), `outletId` (deepLink), `performanceId` (deepLink) · cold entry: An outlet opened from the directory. |
| Route | `/venue-operations/opening-hours-calendar` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board**, answering 2 board screen(s): Operating Hours & Service Periods; Operating Hours & Sales Periods. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Drawn 26 August** — `Seat Board 1.dc.html` frame `seat-1c`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?from=` to `listPerformances`. | `listPerformances` ?from |
| To | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?to=` to `listPerformances`. | `listPerformances` ?to |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Section code | text field | — | — | `getSeatAvailability` ?sectionCode |
| Category | picker: choose a category | — | — | `getSeatAvailability` ?categoryId |
| Available only | toggle | off | — | `getSeatAvailability` ?availableOnly |
| Mode | segmented control | Auto | Auto · Graphical · List | `getSeatAvailability` ?mode |

**Form: Create performances** (modal, opened by *Create performances*; *Create performances* calls `createPerformances`, *Cancel* sends nothing)

**Collects what `createPerformances` sends before it is called.** Required: `startsAt`, `endsAt`. Optional: `admissionRulesId`, `seatMapId`, `recurrence`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPerformances` body |
| Ends at `endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPerformances` body |
| Admission rules `admissionRulesId` | picker: choose an admission rules | optional | — | — | shows names, sends the id | — | `createPerformances` body |
| Seat map `seatMapId` | picker: choose a seat map | optional | — | — | shows names, sends the id | — | `createPerformances` body |
| Language `language` | text field | optional | — | max length 35; pattern `^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$` | — | As `Performance.language`; every performance of a generated series takes it (decided 29 September, rev 3 REV3-17). | `createPerformances` body |
| Format `format` | text field | optional | — | max length 40 | — | As `Performance.format` (decided 29 September, rev 3 REV3-17). | `createPerformances` body |
| Recurrence `recurrence` | group | optional | — | — | — | Generate a series rather than a single performance. Read in the region's time zone: the Region owns the zone and every venue inherits it without override (tenancy), so … | `createPerformances` body |
| Interval minutes `recurrence.intervalMinutes` | number field (minutes) | optional | — | min 1 | — | — | `createPerformances` body |
| Until `recurrence.until` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPerformances` body |
| Days of week `recurrence.daysOfWeek` | list of values (chips) | optional | — | — | — | — | `createPerformances` body |

**Form: Create event** (modal, opened by *Create event*; *Create event* calls `createEvent`, *Cancel* sends nothing)

**Collects what `createEvent` sends before it is called.** Required: `code`, `name`, `venueId`. Optional: `parentEventId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64; A code already used by any event in the tenant is refused with `409 duplicate-code`. | — | Unique per tenant (decided 28 September, audit R108). A code already used by any event in the tenant is refused with `409 duplicate-code`. | `createEvent` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createEvent` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createEvent` body |
| Parent event `parentEventId` | picker: choose a parent event | optional | — | — | shows names, sends the id | — | `createEvent` body |

Errors to draw in the form: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …

**Form: Recommend seats** (modal, opened by *Recommend seats*; *Recommend seats* calls `recommendSeats`, *Cancel* sends nothing)

**Collects what `recommendSeats` sends before it is called.** Required: `partySize`, `strategy`. Optional: `categoryIds`, `maxPrice`, `accessibleCount`, `maxOptions`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Party size `partySize` | stepper or slider | required | — | min 1; max 50 | — | — | `recommendSeats` body |
| Strategy `strategy` | radio group | required | — | Best available · Best value · Closest to stage · Accessible · Contiguous | — | — | `recommendSeats` body |
| Categorys `categoryIds` | multi-picker: choose categorys | optional | — | — | — | — | `recommendSeats` body |
| Max price `maxPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `recommendSeats` body |
| Accessible count `accessibleCount` | number field | optional | 0 | — | — | Wheelchair spaces in the party. Companions are added automatically. | `recommendSeats` body |
| Max options `maxOptions` | number field | optional | 3 | max 10 | — | — | `recommendSeats` body |

Errors to draw in the form: 404 No selection satisfies the constraints

**Form: Save event** (modal, opened by *Save event*; *Save event* calls `updateEvent`, *Cancel* sends nothing)

**Collects what `updateEvent` sends before it is called.** Nothing in the body is required. Optional: `name`, `parentEventId`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateEvent` body |
| Parent event `parentEventId` | picker: choose a parent event | optional | — | — | shows names, sends the id | — | `updateEvent` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateEvent` body |

**Form: Save performance** (modal, opened by *Save performance*; *Save performance* calls `updatePerformance`, *Cancel* sends nothing)

**Collects what `updatePerformance` sends before it is called.** Nothing in the body is required. Optional: `startsAt`, `endsAt`, `status`, `admissionRulesId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Starts at `startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePerformance` body |
| Ends at `endsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePerformance` body |
| Status `status` | segmented control | optional | — | Scheduled · On sale · Suspended | — | — | `updatePerformance` body |
| Admission rules `admissionRulesId` | picker: choose an admission rules | optional | — | — | shows names, sends the id | — | `updatePerformance` body |
| Language `language` | text field | optional | — | max length 35; pattern `^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$` | — | As `Performance.language` (decided 29 September, rev 3 REV3-17). | `updatePerformance` body |
| Format `format` | text field | optional | — | max length 40 | — | As `Performance.format` (decided 29 September, rev 3 REV3-17). | `updatePerformance` body |

Errors to draw in the form: 409 A timing change on a performance with sold tickets, or a `status` move the state model does not allow.

**Form: Save outlet** (modal, opened by *Save outlet*; *Save outlet* calls `updateOutlet`, *Cancel* sends nothing)

**Collects what `updateOutlet` sends before it is called.** Nothing in the body is required. Optional: `name`, `stockLocationId`, `costCenterId`, `openingHours`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateOutlet` body |
| Stock location `stockLocationId` | picker: choose a stock location | optional | — | — | shows names, sends the id | — | `updateOutlet` body |
| Cost center `costCenterId` | picker: choose a cost center | optional | — | — | shows names, sends the id | — | `updateOutlet` body |
| Opening hours `openingHours` | repeatable rows | optional | — | — | — | Replaces the whole weekly pattern. An empty array clears it. | `updateOutlet` body |
| Day `openingHours[].day` | select | required | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `updateOutlet` body |
| From `openingHours[].from` | time picker | required | — | — | HH:mm, 24-hour | Local time, 24-hour `HH:MM`, when the outlet opens. | `updateOutlet` body |
| To `openingHours[].to` | time picker | required | — | — | HH:mm, 24-hour | Local time, 24-hour `HH:MM`, when the outlet closes. | `updateOutlet` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateOutlet` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Sent by *Cancel performance*** (`cancelPerformance`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 1000 | — | — | `cancelPerformance` body |
| Guest message `guestMessage` | key and value settings | optional | — | — | — | — | `cancelPerformance` body |
| Refund percentage `refundPercentage` | stepper or slider | optional | 100 | min 0; max 100 | — | — | `cancelPerformance` body |
| Offer alternative performance `offerAlternativePerformanceId` | picker: choose an offer alternative performance | optional | — | — | shows names, sends the id | — | `cancelPerformance` body |
| Dry run `dryRun` | toggle | optional | off | — | — | — | `cancelPerformance` body |
| Supervisor step up `supervisorStepUp` | group | optional | — | — | — | Required unless `dryRun` (audit R144, proposed by the coordinator). | `cancelPerformance` body |
| Principal `supervisorStepUp.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | The supervisor signing. Recorded against the act. | `cancelPerformance` body |
| Credential `supervisorStepUp.credential` | text area | required | — | max length 512 | — | The supervisor's staff PIN, as they sign in at a till with it. A PIN, never a password (audit R123 (7)). | `cancelPerformance` body |

#### Outputs: what the screen shows and produces

**Shown**

**Calendar** (calendar view, from `listPerformances`): Opening days and performances placed in the venue calendar. Day, week, month and agenda views; the day starts at the venue's `calendarDayStartHour`. Sends the visible window as `from`/`to` and the category filter as `categoryId`.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Event | the name it points at, never the id | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Approval request | the name it points at, never the id | BL-048. The approval chain and the occurrence lifecycle sat on different entities, so neither was complete: `states/performance.yaml` … |
| Requires approval to cancel | yes / no (icon or chip) | Cancelling a sold performance is the one transition that needs a name against it. |
| Status | chip: Scheduled, On sale, Sold out, Suspended, Cancelled, Completed | — |
| Admission rules | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |
| Language | text | The language the performance is given in, as a BCP 47 tag (`en`, `ar`, `fr`, `de`, `zh`, `ru`, `ar-AE`). |
| Format | text | How it is presented, free text the venue chooses, e.g. `2D`, `3D`, `IMAX`, `subtitled`. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Every performance** (data table, from `listPerformances`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Event | the name it points at, never the id | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Approval request | the name it points at, never the id | BL-048. The approval chain and the occurrence lifecycle sat on different entities, so neither was complete: `states/performance.yaml` … |
| Requires approval to cancel | yes / no (icon or chip) | Cancelling a sold performance is the one transition that needs a name against it. |
| Status | chip: Scheduled, On sale, Sold out, Suspended, Cancelled, Completed | — |
| Admission rules | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |

**Every event** (data table, from `listEvents`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Parent event | the name it points at, never the id | For grouped events. |
| Performance count | 1,234 | How many performances the event has. Counted by the server; never sent by a client. |
| Is active | yes / no (icon or chip) | — |

**The selected performance** (detail panel, from `getPerformance`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Event | the name it points at, never the id | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Approval request | the name it points at, never the id | BL-048. The approval chain and the occurrence lifecycle sat on different entities, so neither was complete: `states/performance.yaml` … |
| Requires approval to cancel | yes / no (icon or chip) | Cancelling a sold performance is the one transition that needs a name against it. |
| Status | chip: Scheduled, On sale, Sold out, Suspended, Cancelled, Completed | — |
| Admission rules | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |

**The event** (detail panel, from `getEvent`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Parent event | the name it points at, never the id | For grouped events. |
| Performance count | 1,234 | How many performances the event has. Counted by the server; never sent by a client. |
| Is active | yes / no (icon or chip) | — |

**The seat availability** (detail panel, from `getSeatAvailability`)

| Shows | Format | Notes |
|---|---|---|
| Performance | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |
| Render mode | chip: Graphical, List | The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat … |
| Totals | grouped details | — |
| By category | list or chips (count when long) | — |
| Seats | list or chips (count when long) | — |

**The venue settings** (detail panel, from `getVenueSettings`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Venue | the name it points at, never the id | From the path of `setVenueSettings`. |
| Currency code | text | `readOnly` is the freeze. `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the … |
| Currency scale | 1,234 | Scale travels with currency (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency … |
| Support hours | grouped details | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. |
| Quiet hours | grouped details | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. |
| Biometrics | grouped details | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. |
| Segregated access | grouped details | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a … |
| Alerting | grouped details | CF-134. On-platform notification, marked as read. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Create performances (primary button) | `createPerformances` POST `/events/{eventId}/performances` | CreatePerformancesRequest | inline | — | opens modal first |
| Cancel performance (destructive button) | `cancelPerformance` POST `/performances/{performanceId}/cancel` | inline | PerformanceCancellationResult | 403 The supervisor step-up is missing or failed (audit R144). The PIN did not verify, or the principal does not hold `PERFORMANCE_CONFIGURE` at this venue.; 409 The performance is `cancelled`, `completed` or `soldOut`. … | step-up: pin (Cancels a performance and queues refunds to every holder; a supervisor signs it in place (proposed by the coordinator …) |
| Create event (secondary button) | `createEvent` POST `/events` | CreateEventRequest | Event | 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … | opens modal first |
| Recommend seats (secondary button) | `recommendSeats` POST `/performances/{performanceId}/seat-recommendations` | SeatRecommendationRequest | inline | 404 No selection satisfies the constraints | opens modal first |
| Save event (secondary button) | `updateEvent` PATCH `/events/{eventId}` | inline | Event | — | opens modal first |
| Save performance (secondary button) | `updatePerformance` PATCH `/performances/{performanceId}` | inline | Performance | 409 A timing change on a performance with sold tickets, or a `status` move the state model does not allow. | opens modal first |
| Save outlet (secondary button) | `updateOutlet` PATCH `/outlets/{outletId}` | inline | Outlet | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Data it reads**: `getPerformance` (onLoad, Read a performance); `getSeatAvailability` (onLoad, Seat status for a performance); `listEvents` (onLoad, List events); `getVenueSettings` (onLoad, Operational settings for this venue)

**Where the user goes next**

- → `BO-001` Queue Directory: *Queue Directory*; carries `eventId`
- → `BO-007` Product Directory: *Product Directory*
- → `BO-009` Pricing Rules: *Pricing Rules*

**What opens over it**

- confirmDialog *Cancel performance*: **Names what `cancelPerformance` changes and what it leaves alone**, in the consequence rather than the verb. A opening hours calendar this affects should be identified in the dialog, not just counted. **Collects what `cancelPerformance` sends before it is called.** Required: `reason`. Optional …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The opening hours calendar list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the opening hours calendar untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No opening hours calendar yet. Offers Create performances (`createPerformances`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on from, to and the opening hours calendar are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listPerformances` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 409 A timing change on a performance with sold tickets, or a `status` move the state model does not allow.; 409 The performance is `cancelled`, `completed` or `soldOut`. `states/performance.yaml` cancels only … |

#### Permissions

- `listPerformances` → `PRODUCT_VIEW` (read) · staff, guest
- `getPerformance` → `PRODUCT_VIEW` (read) · staff, guest
- `createPerformances` → `PERFORMANCE_CONFIGURE` (configure) · staff
- `cancelPerformance` → `PERFORMANCE_CONFIGURE` (configure) · staff · step-up pin
- `createEvent` → `EVENT_CONFIGURE` (configure) · staff
- `getEvent` → `PRODUCT_VIEW` (read) · staff
- `getSeatAvailability` → `PRODUCT_VIEW` (read) · staff, guest
- `listEvents` → `PRODUCT_VIEW` (read) · staff
- `recommendSeats` → `PRODUCT_VIEW` (read) · staff, guest
- `updateEvent` → `EVENT_CONFIGURE` (configure) · staff
- `updatePerformance` → `PERFORMANCE_CONFIGURE` (configure) · staff
- `getVenueSettings` → `TENANT_VIEW` (read) · staff
- `updateOutlet` → `REGION_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listPerformances` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

55 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.34 | Time Slot Reservations - System shall support time slot reservations. | Guest Mobile App & Branding | CONTRACTED | `listPerformances` |
| 2.6.15 | - Time slots for events | Ticketing Sales | CONTRACTED | `listPerformances` |
| 2.7.16 | - Dedicated sales calendar | Ticketing Sales | CONTRACTED | `listPerformances` |
| 1.1.2 | The system should be able to sell dated tickets for attractions that allow access only for selected dates by guest. Special day tickets should also be supported. These are dated tickets that skip … | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.1.4 | The system should provide an easy-to-use interface for creation and configuration of timeslots. A calendar view should be available for the user to define the timeslot and recurrence rules. The user … | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.1.85 | Performance-based validity | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.1.86 | Performance date/time validity | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.3.2 | The system should allow configuration of event details such as start time (date & time), end time, duration of event, capacity (amount of places that can be sold for an event), seating categories … | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.3.3 | The system should support multiple occurrences/sessions, defined by a date, time, space, capacity and/or seating arrangement. | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.3.20 | System shall support event cancellation workflows including refunds, exchanges, notifications and audit tracking. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.3.21 | System shall support changing event dates, times and venues while automatically updating tickets, reservations and guest communications. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.4.4 | The system should propagate any changes made to the properties of a product to the already sold tickets as well. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| … 43 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- The operating calendar is configurable: a midnight-to-midnight transaction day or an alternative such as 6am to 6am. *(agreed · MoM 7 Aug 2026, 2. System Organization: Tenant & Site Setup · DI-149)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-063` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Seat Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/Seat Board 1.dc.html`
- Client design-board frames: `Seat Board 1.dc.html#seat-1c`

#### Acceptance for the design

- [ ] Every input above is drawn (47), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (63 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-063?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create performances, Cancel performance, Create event, Recommend seats, Save event, Save performance, Save outlet.
- [ ] Every transition is wired: `BO-001`, `BO-007`, `BO-009`.
- [ ] Every gated control is gated: `EVENT_CONFIGURE`, `PERFORMANCE_CONFIGURE`, `PRODUCT_VIEW`, `REGION_CONFIGURE`, `TENANT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-102` Sell

**Everything in sell, and what in it needs attention.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `PRODUCT_VIEW`, `TENANT_VIEW` (1 operate, 2 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listUpsellRules` reads the population and `getVenueSettings` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: **Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more … |
| Route | `/sell` |

**What the spec says about it.** Section landing. **14 screens reach the entry point through here** — before 20 August they reached it through nothing.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Placement | select | optional | — | Product detail · Cart · Checkout · Post purchase · At gate · In venue | — | Sends `?placement=` to `listUpsellRules`. | `listUpsellRules` ?placement |
| Search sell | search field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Every upsell rule** (data table, from `listUpsellRules`): **Read-only at the venue** (decided 28 September, audit R183) — upsell rules are created and deleted at region level; the venue sees the rules of its region in force, with no create, edit or delete here.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Name | text | — |
| Placement | chip: Product detail, Cart, Checkout, Post purchase, At gate, In venue | — |
| Trigger variants | list or chips (count when long) | — |
| Trigger categorys | list or chips (count when long) | — |
| Suggested variants | list or chips (count when long) | — |
| Suggested bundle | the name it points at, never the id | — |
| Channels | list or chips (count when long) | Empty applies to every channel. Restriction is opt-in — a rule that fires on the website but not at a counter is a guest experience … |
| Priority | 1,234 | — |
| Max suggestions | 1,234 | — |
| Is active | yes / no (icon or chip) | — |
| Region | the name it points at, never the id | The region that owns the rule. Upsell rules are owned at region and read at venue (decided 28 September, audit R183); set from the caller's … |

**Card list** (card list): 14 screens, each with what needs attention.

**The selected upsell rule** (detail panel, from `listUpsellRules`): **Read-only at the venue** (decided 28 September, audit R183) — upsell rules are created and deleted at region level; the venue sees the rules of its region in force, with no create, edit or delete here.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Name | text | — |
| Placement | chip: Product detail, Cart, Checkout, Post purchase, At gate, In venue | — |
| Trigger variants | list or chips (count when long) | — |
| Trigger categorys | list or chips (count when long) | — |
| Suggested variants | list or chips (count when long) | — |
| Suggested bundle | the name it points at, never the id | — |
| Channels | list or chips (count when long) | Empty applies to every channel. Restriction is opt-in — a rule that fires on the website but not at a counter is a guest experience … |
| Priority | 1,234 | — |
| Max suggestions | 1,234 | — |
| Is active | yes / no (icon or chip) | — |
| Region | the name it points at, never the id | The region that owns the rule. Upsell rules are owned at region and read at venue (decided 28 September, audit R183); set from the caller's … |

**The upsell suggestion** (detail panel, from `getUpsellSuggestions`)

| Shows | Format | Notes |
|---|---|---|
| Variant | the name it points at, never the id | — |
| Bundle | the name it points at, never the id | — |
| Name | text | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Discounted price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Source | chip: Rule, Recommendation | A configured rule always outranks a model. |
| Rule | the name it points at, never the id | — |
| Rank | 1,234 | — |
| Rationale | text | — |

**The venue settings** (detail panel, from `getVenueSettings`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Venue | the name it points at, never the id | From the path of `setVenueSettings`. |
| Currency code | text | `readOnly` is the freeze. `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the … |
| Currency scale | 1,234 | Scale travels with currency (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency … |
| Support hours | grouped details | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. |
| Quiet hours | grouped details | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. |
| Biometrics | grouped details | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. |
| Segregated access | grouped details | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a … |
| Alerting | grouped details | CF-134. On-platform notification, marked as read. |

**Data it reads**: `getVenueSettings` (onLoad, What is enabled here); `listUpsellRules` (onLoad, Upsell rules in force, read-only — owned at region (decided …); `decideRecommendations` (onLoad, Fill a recommendation slot)

**Where the user goes next**

- → `BO-007` Product Directory: *Product Directory*
- → `BO-009` Pricing Rules: *Pricing Rules*
- → `BO-010` Promotions & Coupons: *Promotions & Coupons*
- → `BO-011` Packages & Bundles: *Packages & Bundles*
- → `BO-012` Membership Products: *Membership Products*
- → `BO-013` Channel & Distribution: *Channel & Distribution*
- → `BO-014` Catalogue Publishing: *Catalogue Publishing*
- → `BO-015` Performance Calendar: *Performance Calendar*
- → `BO-016` Performance Template: *Performance Template*
- → `BO-017` Capacity Management: *Capacity Management*
- → `BO-018` Allocation & Holds: *Allocation & Holds*
- → `BO-019` Closures & Blackouts: *Closures & Blackouts*
- → `BO-037` Offline Package Status: *Offline Package Status*
- → `BO-063` Opening Hours & Calendar: *Opening Hours & Calendar*
- → `BO-109` Menu Builder & POS Layout Designer: *Menu Builder & POS Layout Designer*
- → `BO-110` Recipe & BOM Management: *Recipe & BOM Management*
- → `BO-111` Ingredient Substitution, Allergen & Nutrition: *Ingredient Substitution, Allergen & Nutrition*
- → `BO-112` Production Planning & Production Sheets: *Production Planning & Production Sheets*
- → `BO-113` Central Kitchen & Commissary Management: *Central Kitchen & Commissary Management*
- → `BO-114` Variants, Attributes, Barcode & RFID Management: *Variants, Attributes, Barcode & RFID Management*
- → `BO-115` Category, Brand & Merchandise Hierarchy: *Category, Brand & Merchandise Hierarchy*
- → `BO-116` Merchandising & Product Presentation: *Merchandising & Product Presentation*
- → `BO-117` Product Import, Governance & AI Configuration Assistant: *Product Import, Governance & AI Configuration Assistant*
- → `BO-118` Campaign & Audience Management: *Campaign & Audience Management*
- → `BO-119` Cross-Sell, Upsell & Recommendation Rules: *Cross-Sell, Upsell & Recommendation Rules*
- → `BO-120` Omnichannel Commerce & Journey Configuration: *Omnichannel Commerce & Journey Configuration*
- → `BO-121` Personalized Offers & Guest Engagement: *Personalized Offers & Guest Engagement*
- → `BO-122` POS Experience Dashboard: *POS Experience Dashboard*
- → `BO-123` POS Profile Management: *POS Profile Management*
- → `BO-124` Layout & Journey Builder: *Layout & Journey Builder*
- → `BO-125` Product & Category Button Configuration: *Product & Category Button Configuration*
- → `BO-126` Deployment, Preview & Audit: *Deployment, Preview & Audit*
- → `BO-142` Store Rules, Controls & Permissions: *Store Rules, Controls & Permissions*
- → `BO-143` Retail Global Settings & Controls: *Retail Global Settings & Controls*
- → `BO-1190` Donation Campaigns: *Donation Campaigns*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list, with counts. |
| Error (`?state=error`) | Could not load. Venue Home is still reachable. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing configured in sell yet.** The action is the first thing to set up, not a blank list. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter. |
| Permission denied (`?state=emptyNoAccess`) | You do not have permission for sell. **Said plainly** — an empty section reads as broken. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getVenueSettings` → `TENANT_VIEW` (read) · staff
- `listUpsellRules` → `PRODUCT_VIEW` (read) · staff
- `decideRecommendations` → `AI_USE` (operate) · staff, guest, anonymous
- `recordRecommendationEvents` → `AI_USE` (operate) · staff, guest, anonymous
- `getUpsellSuggestions` → `PRODUCT_VIEW` (read) · staff, guest

**A refused user sees:** You do not have permission for sell. **Said plainly** — an empty section reads as broken.

#### Requirements it meets

68 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.46 | Personalized Offers - System shall provide personalized offers. | Guest Mobile App & Branding | CONTRACTED | `decideRecommendations` |
| 1.1.33 | AI shall recommend suitable ticket products, upgrades, bundles and promotions based on guest profile, behavior and purchase history. | Ticketing Catalogue | CONTRACTED | `decideRecommendations` |
| 1.1.34 | AI shall recommend upgrades, add-ons and premium experiences during the purchasing journey. | Ticketing Catalogue | CONTRACTED | `decideRecommendations` |
| 1.1.35 | AI shall automatically recommend ticket bundles, packages and complementary products to maximize guest value and revenue. | Ticketing Catalogue | CONTRACTED | `decideRecommendations` |
| 2.6.46 | AI shall recommend relevant tickets, memberships, packages, upgrades, add-ons, F&B, retail products, and experiences based on browsing behavior, purchase history, guest profile, selected products … | Ticketing Sales | CONTRACTED | `decideRecommendations` |
| 2.13.45 | AI Assisted Recommendations | Ticketing Sales | CONTRACTED | `decideRecommendations` |
| 2.14.18 | AI recommends upgrades, renewals and offers. | Ticketing Sales | CONTRACTED | `decideRecommendations` |
| 3.7.9 | System shall generate personalized recommendations for attractions, experiences, memberships, annual passes, F&B products, retail products, upgrades, and add-ons using AI and behavioral analytics. | Admission and Access | CONTRACTED | `decideRecommendations` |
| 4.1.14 | AI recommends higher-value products and add-ons. | Bundles and Promotions | CONTRACTED | `decideRecommendations` |
| 4.1.15 | AI recommends complementary products. | Bundles and Promotions | CONTRACTED | `decideRecommendations` |
| 4.4.30 | Provide AI-driven upsell and cross-sell recommendations based on customer profile, purchase history, loyalty status, seasonality, and basket contents. | Bundles and Promotions | CONTRACTED | `decideRecommendations` |
| 5.4.21 | Recommend rewards and offers. | F&B & Guest Management | CONTRACTED | `decideRecommendations` |
| … 56 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-102` · status **notStarted** · provenance generated
- ADR-0052 *One recommendation engine; runtime in AI, configuration in Promotions* (`docs/adr/0052-one-recommendation-engine.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (42 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-102?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-007`, `BO-009`, `BO-010`, `BO-011`, `BO-012`, `BO-013`, `BO-014`, `BO-015`, `BO-016`, `BO-017`, `BO-018`, `BO-019`, `BO-037`, `BO-063`, `BO-109`, `BO-110`, `BO-111`, `BO-112`, `BO-113`, `BO-114`, `BO-115`, `BO-116`, `BO-117`, `BO-118`, `BO-119`, `BO-120`, `BO-121`, `BO-122`, `BO-123`, `BO-124`, `BO-125`, `BO-126`, `BO-142`, `BO-143`, `BO-1190`.
- [ ] Every gated control is gated: `AI_USE`, `PRODUCT_VIEW`, `TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-109` Menu Builder & POS Layout Designer

**Menu Builder & POS Layout Designer — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `WORKSTATION_CONFIGURE` (2 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listMenus` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session), `menuId` (deepLink), `saleBoardId` (deepLink) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. |
| Route | `/sell/menu-builder-pos-layout-designer` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Drawn 31 August** — `FnB Board 2.dc.html` frame `fnb-2b`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Menu Builder &amp; POS Layout Designer* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Outlet id | picker: choose an outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?outletId=` to `listMenus`. | `listMenus` ?outletId |
| Active at | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?activeAt=` to `listMenus`. | `listMenus` ?activeAt |
| Search menu builder | search field | — | — | — | — | — | — |

**Form: Save menu sections** (modal, opened by *Save menu sections*; *Save menu sections* calls `setMenuSections`, *Cancel* sends nothing)

**Collects what `setMenuSections` sends before it is called.** Required: `sections`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Sections `sections` | repeatable rows | required | — | — | — | — | `setMenuSections` body |
| Code `sections[].code` | text field | required | — | — | — | — | `setMenuSections` body |
| Name `sections[].name` | text field | required | — | — | — | — | `setMenuSections` body |
| Sort order `sections[].sortOrder` | number field | required | — | — | — | — | `setMenuSections` body |
| Items `sections[].items` | repeatable rows | optional | — | — | — | The section's items, in sale-board order. An item's membership is `MenuItem.menuSectionId`. | `setMenuSections` body |
| ID `sections[].items[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setMenuSections` body |
| Product variant `sections[].items[].productVariantId` | picker: choose a product variant | required | — | — | shows names, sends the id | The catalogue variant this item sells. Pricing and tax come from there — a menu is a presentation of the catalogue, not a second catalogue. | `setMenuSections` body |
| Name `sections[].items[].name` | text field | required | — | — | — | — | `setMenuSections` body |
| Description `sections[].items[].description` | text area | optional | — | — | — | — | `setMenuSections` body |
| Price `sections[].items[].price` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setMenuSections` body |
| Sort order `sections[].items[].sortOrder` | number field | optional | — | — | — | — | `setMenuSections` body |
| Modifier groups `sections[].items[].modifierGroupIds` | multi-picker: choose modifier groups | optional | — | — | — | — | `setMenuSections` body |
| Station `sections[].items[].stationId` | picker: choose a station | optional | — | — | shows names, sends the id | — | `setMenuSections` body |
| Is stock tracked `sections[].items[].isStockTracked` | toggle | optional | — | Stock-tracked items cannot be sold offline. | — | True where a recipe exists. Stock-tracked items cannot be sold offline. | `setMenuSections` body |
| Is available `sections[].items[].isAvailable` | toggle | required | — | — | — | — | `setMenuSections` body |
| Unavailable reason `sections[].items[].unavailableReason` | text field | optional | — | — | — | — | `setMenuSections` body |
| Restore at `sections[].items[].restoreAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand. | `setMenuSections` body |
| Preparation minutes `sections[].items[].preparationMinutes` | number field (minutes) | optional | — | — | — | — | `setMenuSections` body |
| Allergens `sections[].items[].allergens` | multi-select chips | optional | — | Gluten · Crustaceans · Eggs · Fish · Peanuts · Soybeans · Milk · Nuts · Celery · Mustard · Sesame · Sulphites … | — | — | `setMenuSections` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Save sale board** (modal, opened by *Save sale board*; *Save sale board* calls `updateSaleBoard`, *Cancel* sends nothing)

**Collects what `updateSaleBoard` sends before it is called.** Required: `id`, `code`, `name`, `venueId`, `kind`, `pages`. Optional: `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `updateSaleBoard` body |
| Name `name` | text field | required | — | max length 200 | — | — | `updateSaleBoard` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `updateSaleBoard` body |
| Kind `kind` | radio group | required | — | Ticketing · Fnb · Retail · Mixed | — | — | `updateSaleBoard` body |
| Pages `pages` | repeatable rows | required | — | at least 1 | — | — | `updateSaleBoard` body |
| Name `pages[].name` | text field | required | — | — | — | — | `updateSaleBoard` body |
| Sort order `pages[].sortOrder` | number field | required | — | — | — | — | `updateSaleBoard` body |
| Tiles `pages[].tiles` | repeatable rows | required | — | — | — | — | `updateSaleBoard` body |
| Position `pages[].tiles[].position` | number field | required | — | — | — | — | `updateSaleBoard` body |
| Kind `pages[].tiles[].kind` | radio group | required | — | Product · Category · Action · Spacer | — | — | `updateSaleBoard` body |
| Variant `pages[].tiles[].variantId` | picker: choose a variant | optional | — | — | shows names, sends the id | — | `updateSaleBoard` body |
| Label `pages[].tiles[].label` | text field | optional | — | — | — | — | `updateSaleBoard` body |
| Colour `pages[].tiles[].colour` | text field | optional | — | — | — | — | `updateSaleBoard` body |
| Image `pages[].tiles[].imageAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `updateSaleBoard` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateSaleBoard` body |

Errors to draw in the form: 400 A tile references an unknown or unsellable variant; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

#### Outputs: what the screen shows and produces

**Shown**

**Every menu** (data table, from `listMenus`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Outlet | the name it points at, never the id | — |
| Availability | grouped details | When this menu is in force. Absent means always. |
| Sections | list or chips (count when long) | — |
| Is active | yes / no (icon or chip) | — |

**The selected menu** (detail panel, from `listMenus`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Outlet | the name it points at, never the id | — |
| Availability | grouped details | When this menu is in force. Absent means always. |
| Sections | list or chips (count when long) | — |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save menu sections (primary button) | `setMenuSections` PUT `/menus/{menuId}/sections` | inline | Menu | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| Save sale board (secondary button) | `updateSaleBoard` PUT `/sale-boards/{saleBoardId}` | SaleBoard | SaleBoard | 400 A tile references an unknown or unsellable variant; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Data it reads**: `listMenus` (onLoad, List menus)

**Where the user goes next**

- → `BO-102` Sell: *Sell*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The menu pos layout list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the menu pos layout untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No menu pos layout yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on outletId, activeAt and the menu pos layout are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listMenus` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A tile references an unknown or unsellable variant |

#### Permissions

- `listMenus` → `PRODUCT_VIEW` (read) · staff
- `setMenuSections` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateSaleBoard` → `WORKSTATION_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listMenus` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.22 | The system should provide the option to split menu items by sections for specific locations of the outlet. For example: one menu section going to kitchen and the other going to the drink bar. The … | Bundles and Promotions | CONTRACTED | `setMenuSections` |
| 4.9.3 | The system should provide the option to remotely configure visibility and placement of available menu items available for sale on POS screen. The function should be limited to only users accounts … | Bundles and Promotions | CONTRACTED | `setMenuSections` |
| 4.9.4 | The system should be able to design a menu button layout page can be copied and re-used in multiple locations if the need arises | Bundles and Promotions | CONTRACTED | `setMenuSections` |
| 2.1.9 | The system should allow the interface of POS solution to be configurable: - Configurable hot keys on touch screen to link to a specific action. - Configuration of various sales screens (buttons … | Ticketing Sales | CONTRACTED | `updateSaleBoard` |
| 2.12.19 | Order Sales 1) The POS home page displays available products by category, for the current POS. 2) Staff can click a specific product to add it to the cart; quantity can be adjusted 3) The system … | Ticketing Sales | CONTRACTED | `updateSaleBoard` |
| 2.1.32 | System shall allow guests to purchase food and beverage items through self-service kiosks. The kiosk shall support menu browsing, product customization, combo meals, upsell recommendations … | Ticketing Sales | CONTRACTED | data `Menu` |
| 2.1.33 | System shall allow guests to purchase retail merchandise through self-service kiosks. The kiosk shall support product browsing, inventory validation, variant selection (size, color, style) … | Ticketing Sales | CONTRACTED | data `Menu` |
| 4.6.13 | The system should have a interface for kiosks where the guest should be able to place order via the self service option all the way till completing payments. | Bundles and Promotions | CONTRACTED | data `Menu` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Menu Builder defines the front-end POS layout per outlet — categories, item tiles (image, name, price) and configurable button sizes for fast-selling items. Agreed the current (reference) layout is a reference only and the UI/UX can be improved. *(agreed · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-326)*
- Drag-and-drop POS "sales board" designer placing products and system functions (ticket list, reservation list, transaction list, media lookup) as buttons with custom fonts and colours. Allam: the old interface is NOT a design reference — functional concept only. *(agreed · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-157)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A82** Design the F&B Command Center suite: a real-time cross-outlet sales/operations dashboard, the F&B Stock Command Center (stock value, low-stock alerts, recipe-based consumption, batch/wastage tracking, replenishment … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'recipe')*
- **A83** Design the Menu & Product Command Center and Menu Builder (recipe/product mapping alerts, drag-and-drop POS layout, chargeable/free modifiers with min/max rules, combo meals with upgrade options) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'menu & product')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-109` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 2.dc.html`
- Client design-board frames: `FnB Board 2.dc.html#fnb-2b`

#### Acceptance for the design

- [ ] Every input above is drawn (37), with its required mark, default, format and its error state (400, 403, 404, 412).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-109?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save menu sections, Save sale board.
- [ ] Every transition is wired: `BO-102`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `WORKSTATION_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-110` Recipe & BOM Management

**Recipe & BOM Management — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `fnb` module |
| Block | Block A · ticket #20701 (APP-SETUP-BO-110) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listRecipes` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. |
| Route | `/sell/recipe-bom-management` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search | text field | optional | — | — | — | Sends `?search=` to `listRecipes`. | `listRecipes` ?search |
| Menu item id | picker: choose a menu item (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?menuItemId=` to `listRecipes`. | `listRecipes` ?menuItemId |
| Search recipe | search field | — | — | — | — | — | — |

**Form: Save recipe** (modal, opened by *Save recipe*; *Save recipe* calls `setRecipe`, *Cancel* sends nothing)

**Collects what `setRecipe` sends before it is called.** Required: `menuItemId`, `ingredients`. Optional: `yield`, `costPerPortion`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Menu item `menuItemId` | picker: choose a menu item | required | — | — | shows names, sends the id | — | `setRecipe` body |
| Yield `yield` | number field | optional | — | min 0 | — | Portions produced by one execution. | `setRecipe` body |
| Ingredients `ingredients` | repeatable rows | required | — | at least 1 | — | — | `setRecipe` body |
| Inventory item `ingredients[].inventoryItemId` | picker: choose an inventory item | required | — | — | shows names, sends the id | — | `setRecipe` body |
| Quantity `ingredients[].quantity` | number field | required | — | min 0 | — | — | `setRecipe` body |
| Unit `ingredients[].unit` | text field | required | — | — | — | — | `setRecipe` body |
| Is optional `ingredients[].isOptional` | toggle | optional | off | — | — | — | `setRecipe` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

#### Outputs: what the screen shows and produces

**Shown**

**Every recipe** (data table, from `listRecipes`)

| Shows | Format | Notes |
|---|---|---|
| Menu item | the name it points at, never the id | — |
| Yield | 1,234.5 | Portions produced by one execution. |
| Ingredients | list or chips (count when long) | — |
| Cost per portion | AED 1,234.50 | Computed, never entered (decided 28 September, audit R125 (9)): the sum of each ingredient quantity at its current inventory cost, divided … |

**The selected recipe** (detail panel, from `listRecipes`)

| Shows | Format | Notes |
|---|---|---|
| Menu item | the name it points at, never the id | — |
| Yield | 1,234.5 | Portions produced by one execution. |
| Ingredients | list or chips (count when long) | — |
| Cost per portion | AED 1,234.50 | Computed, never entered (decided 28 September, audit R125 (9)): the sum of each ingredient quantity at its current inventory cost, divided … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save recipe (primary button) | `setRecipe` PUT `/recipes` | Recipe | Recipe | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |

**Data it reads**: `listRecipes` (onLoad, List recipes)

**Where the user goes next**

- → `BO-102` Sell: *Sell*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recipe bom list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recipe bom untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recipe bom yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on search, menuItemId and the recipe bom are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listRecipes` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listRecipes` → `PRODUCT_VIEW` (read) · staff
- `setRecipe` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listRecipes` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.7.6 | The system should have the ability to add or remove ingredients from a recipe product in a user friendly top-down approach. | Bundles and Promotions | CONTRACTED | `setRecipe` |
| 4.8.1 | The system should have the ability to add and remove multiple ingredients on one type of recipe order, while there are other recipe products on the same order without any modifications. | Bundles and Promotions | CONTRACTED | `setRecipe` |
| 4.8.4 | Create and manage recipes linked to menu items including ingredients, quantities, portions and preparation instructions. | Bundles and Promotions | CONTRACTED | `setRecipe` |
| 4.8.6 | Automatically calculate recipe costs based on ingredient costs and quantities. | Bundles and Promotions | CONTRACTED | `setRecipe` |
| 10.1.2 | The system should be able to sync all the recipes from the inventory management on real-time or timed intervals, to be able to display products and menu buttons. | Games & F&B Integration | CONTRACTED | `setRecipe` |
| 10.1.3 | The system should be able to sync all the recipe orders to manage and reflect on inventory and order management reports and further use this data for re-order levels. | Games & F&B Integration | CONTRACTED | `setRecipe` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Recipe & BOM captures ingredient quantity, unit, cost (from purchase data), preparation time, yield, selling price and margin. Ingredient substitution uses an alternate ingredient automatically when the primary is out of stock; production planning aggregates recipe requirements to forecast prepared-item quantities. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-329)*
- Menu & Product Command Center tracks menus, active recipes and products, and flags products without mapped recipes or with unavailable ingredients. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-325)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A82** Design the F&B Command Center suite: a real-time cross-outlet sales/operations dashboard, the F&B Stock Command Center (stock value, low-stock alerts, recipe-based consumption, batch/wastage tracking, replenishment … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'recipe')*
- **A83** Design the Menu & Product Command Center and Menu Builder (recipe/product mapping alerts, drag-and-drop POS layout, chargeable/free modifiers with min/max rules, combo meals with upgrade options) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'menu & product')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-110` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-110?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save recipe.
- [ ] Every transition is wired: `BO-102`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-111` Ingredient Substitution, Allergen & Nutrition

**Ingredient Substitution, Allergen & Nutrition — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`setRecipe`, `updateMenu`, `setSubstitutionRules`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | `venueId` (session), `menuId` (deepLink), `menuItemId` (deepLink), `recipeId` (navigation) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. An item opened from the menu. **Allergen verification … |
| Route | `/sell/ingredient-substitution-allergen-nutrition` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| menuItemId | picker: choose a menu item (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `Recipe.menuItemId` |
| yield | number field | optional | — | min 0 | — | Portions produced by one execution. | `Recipe.yield` |
| ingredients | repeatable rows | optional | — | at least 1 | — | — | `Recipe.ingredients` |
| costPerPortion | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Computed, never entered (decided 28 September, audit R125 (9)): the sum of each ingredient quantity at its current inventory cost, divided by `yield`. | `Recipe.costPerPortion` |
| Search ingredient substitution, allergen | search field | — | — | — | — | — | — |

**Form: Save menu** (modal, opened by *Save menu*; *Save menu* calls `updateMenu`, *Cancel* sends nothing)

**Collects what `updateMenu` sends before it is called.** Nothing in the body is required. Optional: `name`, `availability`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateMenu` body |
| Availability `availability` | group | optional | — | — | — | When this menu is in force. Absent means always. | `updateMenu` body |
| Days of week `availability.daysOfWeek` | list of values (chips) | optional | — | — | — | — | `updateMenu` body |
| Start time `availability.startTime` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | Wall-clock time, in the Region's time zone. | `updateMenu` body |
| End time `availability.endTime` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | Wall-clock time, in the Region's time zone. | `updateMenu` body |
| Valid from `availability.validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Calendar day, in the Region's time zone, not UTC. | `updateMenu` body |
| Valid to `availability.validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Calendar day, in the Region's time zone, not UTC. | `updateMenu` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateMenu` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Save substitution rules** (modal, opened by *Save substitution rules*; *Save substitution rules* calls `setSubstitutionRules`, *Cancel* sends nothing)

**Collects what `setSubstitutionRules` sends before it is called.** Required: `rules`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Rules `rules` | repeatable rows | required | — | — | — | — | `setSubstitutionRules` body |
| ID `rules[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setSubstitutionRules` body |
| Recipe `rules[].recipeId` | picker: choose a recipe | required | — | — | shows names, sends the id | The recipe the rule applies to (decided 28 September, audit R125 (10)). Not a menu item and not the whole venue: a swap that is safe in one dish is not safe in another. | `setSubstitutionRules` body |
| From ingredient `rules[].fromIngredientId` | picker: choose a from ingredient | required | — | — | shows names, sends the id | — | `setSubstitutionRules` body |
| To ingredient `rules[].toIngredientId` | picker: choose a to ingredient | required | — | — | shows names, sends the id | — | `setSubstitutionRules` body |
| Ratio `rules[].ratio` | number field | optional | 1 | — | — | Not always one to one. Fresh herbs to dried is roughly three to one, and a rule that assumes parity produces a dish nobody would serve. | `setSubstitutionRules` body |
| Allergens added `rules[].allergensAdded` | multi-select chips | optional | — | Gluten · Crustaceans · Eggs · Fish · Peanuts · Soybeans · Milk · Nuts · Celery · Mustard · Sesame · Sulphites … | — | — | `setSubstitutionRules` body |
| Allergens removed `rules[].allergensRemoved` | multi-select chips | optional | — | Gluten · Crustaceans · Eggs · Fish · Peanuts · Soybeans · Milk · Nuts · Celery · Mustard · Sesame · Sulphites … | — | — | `setSubstitutionRules` body |
| Conditions `rules[].conditions` | multi-select chips | optional | — | Out of stock · Seasonal · Guest request · Cost saving · Always | — | — | `setSubstitutionRules` body |
| Requires approval `rules[].requiresApproval` | toggle | optional | off | — | — | True where the swap changes an allergen. A chef may substitute freely within a claim; changing the claim is somebody else's decision. | `setSubstitutionRules` body |
| Is active `rules[].isActive` | toggle | optional | on | — | — | — | `setSubstitutionRules` body |

Errors to draw in the form: 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Sent by *Save recipe*** (`setRecipe`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Menu item `menuItemId` | picker: choose a menu item | required | — | — | shows names, sends the id | — | `setRecipe` body |
| Yield `yield` | number field | optional | — | min 0 | — | Portions produced by one execution. | `setRecipe` body |
| Ingredients `ingredients` | repeatable rows | required | — | at least 1 | — | — | `setRecipe` body |
| Inventory item `ingredients[].inventoryItemId` | picker: choose an inventory item | required | — | — | shows names, sends the id | — | `setRecipe` body |
| Quantity `ingredients[].quantity` | number field | required | — | min 0 | — | — | `setRecipe` body |
| Unit `ingredients[].unit` | text field | required | — | — | — | — | `setRecipe` body |
| Is optional `ingredients[].isOptional` | toggle | optional | off | — | — | — | `setRecipe` body |

#### Outputs: what the screen shows and produces

**Shown**

**Last allergen verdict** (detail panel, from `verifyAllergens`): **Shows the last automatic verdict** — `matches`, `undeclared` (with `via` and `sourceRef`, shown first), `overDeclared` — from the check the server runs after every recipe, substitution or modifier change, with when it ran (decided 28 September, audit R241). **The contract records the verdict but exposes no read of it yet**, so until one exists this panel shows the result of the latest manual …

| Shows | Format | Notes |
|---|---|---|
| Menu item | the name it points at, never the id | — |
| Matches | yes / no (icon or chip) | — |
| Declared | list or chips (count when long) | — |
| Actual | list or chips (count when long) | — |
| Undeclared | list or chips (count when long) | Present in the dish and absent from the label. The dangerous direction, and the response leads with it. |
| Allergen | text | — |
| Via | chip: Ingredient, Substitution, Modifier, Shared equipment | — |
| Source ref | text | — |
| Over declared | list or chips (count when long) | Labelled and no longer present. Safe, and still worth fixing — a menu that over-declares teaches guests the labels are guesses. |
| Checked at | 1 Oct 2026, 14:30 | — |
| Trigger | chip: Manual, Recipe changed, Substitution changed, Modifier changed | What ran the check. `manual` is the Verify button; the others are the automatic run after that change (audit R241). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save recipe (primary button) | `setRecipe` PUT `/recipes` | Recipe | Recipe | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | — |
| Save menu (secondary button) | `updateMenu` PATCH `/menus/{menuId}` | inline | Menu | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| Save substitution rules (secondary button) | `setSubstitutionRules` PUT `/substitution-rules` | inline | SubstitutionRule[] | 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| Re-check allergens (manual) (secondary button) | `verifyAllergens` POST `/menu-items/{menuItemId}/verify-allergens` | — | AllergenVerdict | — | — |

**Where the user goes next**

- → `BO-102` Sell: *Sell*
- → `BO-045` Menu Management: *The draft is scheduled for Monday rather than published now*; carries `menuId`, `menuItemId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved ingredient substitution allergen. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ingredient substitution allergen untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ingredient substitution allergen configured. The form opens empty and `setRecipe` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_CONFIGURE`, which `setRecipe` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `setRecipe` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateMenu` → `PRODUCT_CONFIGURE` (configure) · staff
- `setSubstitutionRules` → `PRODUCT_CONFIGURE` (configure) · staff
- `verifyAllergens` → `PRODUCT_VIEW` (read) · staff
- `setIngredientSubstitutes` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_CONFIGURE`, which `setRecipe` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.7.6 | The system should have the ability to add or remove ingredients from a recipe product in a user friendly top-down approach. | Bundles and Promotions | CONTRACTED | `setRecipe` |
| 4.8.1 | The system should have the ability to add and remove multiple ingredients on one type of recipe order, while there are other recipe products on the same order without any modifications. | Bundles and Promotions | CONTRACTED | `setRecipe` |
| 4.8.4 | Create and manage recipes linked to menu items including ingredients, quantities, portions and preparation instructions. | Bundles and Promotions | CONTRACTED | `setRecipe` |
| 4.8.6 | Automatically calculate recipe costs based on ingredient costs and quantities. | Bundles and Promotions | CONTRACTED | `setRecipe` |
| 10.1.2 | The system should be able to sync all the recipes from the inventory management on real-time or timed intervals, to be able to display products and menu buttons. | Games & F&B Integration | CONTRACTED | `setRecipe` |
| 10.1.3 | The system should be able to sync all the recipe orders to manage and reflect on inventory and order management reports and further use this data for re-order levels. | Games & F&B Integration | CONTRACTED | `setRecipe` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Recipe & BOM captures ingredient quantity, unit, cost (from purchase data), preparation time, yield, selling price and margin. Ingredient substitution uses an alternate ingredient automatically when the primary is out of stock; production planning aggregates recipe requirements to forecast prepared-item quantities. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-329)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-111` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 2.dc.html`
- Drawn by: Claude Design F&B pack, 24 August
- Client design-board frames: `FnB Board 2.dc.html#fnb-2l`
- Flow F31 *A menu is drafted, scheduled and rolled back*, step 3: An item's recipe changed, so its allergens are re-verified. → **A substituted ingredient changes the allergen claim.** BL-127 built allergens without linking substitution, and `verifyAllergens` is the one remaining gap this step names.
- Flow F93 *A recipe changes and its allergen claim is re-verified*, step 1: Ingredient Substitution, Allergen & Nutrition. → **Drawn by the client as FNB-2L.**
- Flow F93 branch at step 1 (medium): when A step is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` decides — the journey is shorter, not broken.

#### Acceptance for the design

- [ ] Every input above is drawn (31), with its required mark, default, format and its error state (400, 412).
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-111?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save recipe, Save menu, Save substitution rules, Re-check allergens (manual).
- [ ] Every transition is wired: `BO-102`, `BO-045`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-112` Production Planning & Production Sheets

**Production Planning & Production Sheets — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`planProductionRun`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. |
| Route | `/sell/production-planning-production-sheets` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| id | picker: choose an id (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `ProductionRun.id` |
| recipeId | picker: choose a recipe (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `ProductionRun.recipeId` |
| producingOutletId | picker: choose a producing outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `ProductionRun.producingOutletId` |
| forOutletIds | multi-picker: choose for outlets | optional | — | — | — | Where it goes. A central kitchen produces for outlets that did not make it. | `ProductionRun.forOutletIds` |
| plannedQuantity | number field | optional | — | — | — | — | `ProductionRun.plannedQuantity` |
| actualQuantity | number field | optional | — | — | — | BL-126. Theoretical against actual is the whole point of recording this. | `ProductionRun.actualQuantity` |
| scheduledFor | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `ProductionRun.scheduledFor` |
| status | radio group | optional | — | Planned · In progress · Completed · Cancelled | — | — | `ProductionRun.status` |
| varianceReason | text field | optional | — | — | — | — | `ProductionRun.varianceReason` |
| Search production planning | search field | — | — | — | — | — | — |

**Sent by *Plan production run*** (`planProductionRun`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `planProductionRun` body |
| Recipe `recipeId` | picker: choose a recipe | required | — | — | shows names, sends the id | — | `planProductionRun` body |
| Station `stationId` | picker: choose a station | optional | — | — | shows names, sends the id | The station whose prep list this run is on. Copied from the plan line on release, where runs are grouped by station (audit R125 (7)). | `planProductionRun` body |
| Producing outlet `producingOutletId` | picker: choose a producing outlet | optional | — | — | shows names, sends the id | — | `planProductionRun` body |
| For outlets `forOutletIds` | multi-picker: choose for outlets | optional | — | — | — | Where it goes. A central kitchen produces for outlets that did not make it. | `planProductionRun` body |
| Planned quantity `plannedQuantity` | number field | required | — | — | — | — | `planProductionRun` body |
| Actual quantity `actualQuantity` | number field | optional | — | — | — | BL-126. Theoretical against actual is the whole point of recording this. | `planProductionRun` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `planProductionRun` body |
| Status `status` | radio group | required | — | Planned · In progress · Completed · Cancelled | — | — | `planProductionRun` body |
| Variance reason `varianceReason` | text field | optional | — | — | — | — | `planProductionRun` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Plan production run (primary button) | `planProductionRun` POST `/production-runs` | ProductionRun | ProductionRun | — | — |

**Where the user goes next**

- → `BO-009` Pricing Rules: *Pricing Rules*; calls `planProductionRun`
- → `BO-102` Sell: *Sell*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved production planning production. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the production planning production untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No production planning production configured. The form opens empty and `planProductionRun` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_CONFIGURE`, which `planProductionRun` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `planProductionRun` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_CONFIGURE`, which `planProductionRun` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.36 | Compare theoretical recipe cost versus actual inventory consumption and wastage, highlighting variances and operational inefficiencies. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.7 | Manage recipe yields, shrinkage, wastage and final portions. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.12 | Plan kitchen production quantities based on expected demand. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.13 | Manage batch preparation and production runs. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.16 | Generate production sheets for kitchen operations. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.17 | Support central kitchen and commissary operations supplying multiple outlets, including production batches, transfers, yields, and planning. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.18 | Generate replenishment requests automatically based on demand forecasts, stock levels, and attendance projections. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.19 | Generate production schedules using reservations, attendance forecasts, event schedules, and inventory availability. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 5.1.10 | Manage kitchen production capacity. | F&B & Guest Management | CONTRACTED | data `ProductionRun` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Recipe & BOM captures ingredient quantity, unit, cost (from purchase data), preparation time, yield, selling price and margin. Ingredient substitution uses an alternate ingredient automatically when the primary is out of stock; production planning aggregates recipe requirements to forecast prepared-item quantities. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-329)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-112` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 2.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 2.dc.html#ret-2e`

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-112?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Plan production run.
- [ ] Every transition is wired: `BO-009`, `BO-102`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-113` Central Kitchen & Commissary Management

**Central Kitchen & Commissary Management — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`planProductionRun`, `completeProductionRun`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | `venueId` (session), `runId` (deepLink) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. |
| Route | `/sell/central-kitchen-commissary-management` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| id | picker: choose an id (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `ProductionRun.id` |
| recipeId | picker: choose a recipe (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `ProductionRun.recipeId` |
| producingOutletId | picker: choose a producing outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `ProductionRun.producingOutletId` |
| forOutletIds | multi-picker: choose for outlets | optional | — | — | — | Where it goes. A central kitchen produces for outlets that did not make it. | `ProductionRun.forOutletIds` |
| plannedQuantity | number field | optional | — | — | — | — | `ProductionRun.plannedQuantity` |
| actualQuantity | number field | optional | — | — | — | BL-126. Theoretical against actual is the whole point of recording this. | `ProductionRun.actualQuantity` |
| scheduledFor | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `ProductionRun.scheduledFor` |
| status | radio group | optional | — | Planned · In progress · Completed · Cancelled | — | — | `ProductionRun.status` |
| varianceReason | text field | optional | — | — | — | — | `ProductionRun.varianceReason` |
| Search central kitchen | search field | — | — | — | — | — | — |

**Form: Complete production run** (modal, opened by *Complete production run*; *Complete production run* calls `completeProductionRun`, *Cancel* sends nothing)

**Collects what `completeProductionRun` sends before it is called.** Required: `actualQuantity`, `recordedAt`. Optional: `varianceReason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Actual quantity `actualQuantity` | number field | required | — | — | — | — | `completeProductionRun` body |
| Variance reason `varianceReason` | text field | optional | — | — | — | — | `completeProductionRun` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `completeProductionRun` body |

Errors to draw in the form: 409 The run is not `inProgress` (states/production-run.yaml). Names its current status.

**Sent by *Plan production run*** (`planProductionRun`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `planProductionRun` body |
| Recipe `recipeId` | picker: choose a recipe | required | — | — | shows names, sends the id | — | `planProductionRun` body |
| Station `stationId` | picker: choose a station | optional | — | — | shows names, sends the id | The station whose prep list this run is on. Copied from the plan line on release, where runs are grouped by station (audit R125 (7)). | `planProductionRun` body |
| Producing outlet `producingOutletId` | picker: choose a producing outlet | optional | — | — | shows names, sends the id | — | `planProductionRun` body |
| For outlets `forOutletIds` | multi-picker: choose for outlets | optional | — | — | — | Where it goes. A central kitchen produces for outlets that did not make it. | `planProductionRun` body |
| Planned quantity `plannedQuantity` | number field | required | — | — | — | — | `planProductionRun` body |
| Actual quantity `actualQuantity` | number field | optional | — | — | — | BL-126. Theoretical against actual is the whole point of recording this. | `planProductionRun` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `planProductionRun` body |
| Status `status` | radio group | required | — | Planned · In progress · Completed · Cancelled | — | — | `planProductionRun` body |
| Variance reason `varianceReason` | text field | optional | — | — | — | — | `planProductionRun` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Plan production run (primary button) | `planProductionRun` POST `/production-runs` | ProductionRun | ProductionRun | — | — |
| Complete production run (secondary button) | `completeProductionRun` POST `/production-runs/{runId}/complete` | inline | ProductionRun | 409 The run is not `inProgress` (states/production-run.yaml). Names its current status. | opens modal first |

**Where the user goes next**

- → `BO-102` Sell: *Sell*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved central kitchen commissary. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the central kitchen commissary untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No central kitchen commissary configured. The form opens empty and `planProductionRun` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_CONFIGURE`, which `planProductionRun` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The run is not `inProgress` (states/production-run.yaml). Names its current status. |

#### Permissions

- `planProductionRun` → `PRODUCT_CONFIGURE` (configure) · staff
- `completeProductionRun` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_CONFIGURE`, which `planProductionRun` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.36 | Compare theoretical recipe cost versus actual inventory consumption and wastage, highlighting variances and operational inefficiencies. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.7 | Manage recipe yields, shrinkage, wastage and final portions. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.12 | Plan kitchen production quantities based on expected demand. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.13 | Manage batch preparation and production runs. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.16 | Generate production sheets for kitchen operations. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.17 | Support central kitchen and commissary operations supplying multiple outlets, including production batches, transfers, yields, and planning. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.18 | Generate replenishment requests automatically based on demand forecasts, stock levels, and attendance projections. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.19 | Generate production schedules using reservations, attendance forecasts, event schedules, and inventory availability. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 5.1.10 | Manage kitchen production capacity. | F&B & Guest Management | CONTRACTED | data `ProductionRun` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A20** Double-check requirement matrix for kitchen display system (KDS) integration scope *(Chinmay Parab · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'kitchen')*
- **A52** Design on-seat / location-based F&B delivery: seat-linked QR codes for seated events, and physical location QR codes (e.g., per beach chair/table) for open venues, routing kitchen orders to the scanned location *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'kitchen')*
- **A84** Design kitchen station routing and KDS/printer rules (with fallback device logic), including course-wise ordering and a live "fired" ticket timer *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'kitchen')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-113` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 2.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 2.dc.html#ret-2d`

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-113?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Plan production run, Complete production run.
- [ ] Every transition is wired: `BO-102`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P08 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-030, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-043, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051, DI-052 (each is in the design inputs below).

**Workshop tracker rows about P08 as a whole** (1: 1 open, 0 closed). Open first; a closed row says where it went on 30 September.

- **S8** Venue Management back-end configuration wireframes *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*

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

### Across P08 Venue Management

- Qossai: configuration screens should consolidate related functionality, potentially merging 3-4 previously separate screens into one, rather than the repetitive one-screen-per-concept pattern of the AI-built reference system. *(agreed · MoM 24 Sep 2026, 4.5 Screen Consolidation Philosophy · DI-987)*
- **Open question.** Open: should AI monitoring live in one centralised AI command dashboard or be distributed as widgets in each functional module's own dashboard? Allam: Softlabs' call; the current proposal is illustrative and Softlabs may propose a better structure. *(open · MoM 18 Sep 2026, 4.4 AI Governance — Risk, Compliance & Continuous Monitoring · DI-936)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- **Open question.** Allam: a user's visibility must be restrictable to specific outlets (an F&B manager of one outlet should not see other outlets' items); also relevant for ticketing/event-specific access. Implementation approach still open. *(open · MoM 18 Aug 2026, 4.6 Role-Based & Outlet-Level Access Control — Open Item · DI-331)*
- Access loads automatically at login on POS and web/admin. A user with one role logs straight in; a user with several roles (e.g. admin, cashier, supervisor, manager) is prompted to choose which role to use. *(agreed · MoM 12 Aug 2026, 4. Multiple Roles per User and Role Switching · DI-249)*
- Back office is role-driven from any device: a finance user signing in from a workstation, laptop or home sees only finance reports and related information. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-248)*
- Built-in help menu with step-by-step tutorials with screenshots for common tasks (e.g. how to sell a ticket at the POS). *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-160)*
- Custom data-capture fields ("data mask") at account, event, extended-ticket and product level: field types text, dropdown, radio, true/false; multi-language labels; validation (min/max length, required/optional); reusable value lists (e.g. country list). Standard fields come out of the box. *(agreed · MoM 7 Aug 2026, 6. Data Mask: Flexible Custom Data Capture · DI-155)*
- Load/traffic dashboards respect the tenancy model: a venue manager sees traffic for their own venue only. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-061)*
- Allam: queue management is built into the system (not third-party) so traffic entering the site can be throttled from the back office itself. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-060)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Documentation deliverable includes user guides and help content; the preview shows a TICVAI Help Center with categories (Getting Started, Events, Tickets, Orders, Payments, Memberships, Access Control, Reports, Integrations), a "Welcome to TICVAI" getting-started article and Quick Links (Create an Event, Set Pricing, Manage Access, View Reports). *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - What We Deliver / Key Deliverables Preview · DI-052)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- AI Assistant panel: a short framing ("Based on last 30 days, here are 3 actions that can improve your revenue") then actionable recommendations, each with its potential impact (e.g. "Increase pricing for VIP seats, +12%") and a chevron, plus "View all recommendations". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - AI Panels · DI-043)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Back-office shell: collapsible left sidebar with Overview, Events, Tickets, Orders, Customers, Memberships, Access Control, POS, Reports, Analytics, AI Assistant, Settings, and the signed-in user (name, role) at the bottom; top bar with global search (Cmd+K), current time and date, Notifications with unread dot, and user menu. *(agreed · Design Vision Book 29 Jul 2026, 04 Dashboard Vision (p4) - navigation shell · DI-030)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*
- Reports and historical searches must still retrieve archived transactions when required; the retention period (e.g. keep 3 of 5+ years live) is configurable per customer, archival manual or automated. *(agreed · MoM 28 Jul 2026, 23. Database Optimisation and Archiving · DI-018)*
- Back-office controls for the waiting room: configurable maximum active users and admission intervals, set per customer and venue. *(agreed · MoM 28 Jul 2026, 19. Auto-scaling and Virtual Waiting Room · DI-017)*

### In P08 · Sell

- Allam: back-end configuration is the most critical part; the screens must make visually clear how administrators configure products, pricing per channel, attributes/components, entitlements, validity and access permissions, comparable to the structured product/metric-sheet approach of an earlier reference system. *(agreed · MoM 24 Sep 2026, 4.3 Back-End Configuration Detail — Requested Format (Screens, Not Just Functional Lists) · DI-985)*
- Chinmay: reduce the number of configuration screens/pages and consolidate related settings/toggles to avoid a long, click-heavy admin flow; Allam agreed, citing the previous system's demo as a starting reference. *(agreed · MoM 25 Aug 2026, 4.11 UX Simplification & Distributed Inventory · DI-474)*
- Retail dashboard gives a consolidated real-time view across outlets — total retail sales, total and average transactions, store performance snapshot, system alerts and out-of-stock indicators — viewable by day, week or month. *(client request · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-349)*
- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*

**11 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"acquireInventoryHold": {"method":"POST","path":"/inventory-holds","contract":"catalogue","summary":"Acquire an inventory hold","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"AcquireLeaseRequest","responds":"InventoryHold"},
"cancelPerformance": {"method":"POST","path":"/performances/{performanceId}/cancel","contract":"catalogue","summary":"Cancel a performance","permission":"PERFORMANCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PerformanceCancellationResult"},
"completeProductionRun": {"method":"POST","path":"/production-runs/{runId}/complete","contract":"fnb","summary":"Record what was actually made","permission":"PRODUCT_CONFIGURE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProductionRun"},
"createEvent": {"method":"POST","path":"/events","contract":"catalogue","summary":"Create an event","permission":"EVENT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateEventRequest","responds":"Event"},
"createPerformances": {"method":"POST","path":"/events/{eventId}/performances","contract":"catalogue","summary":"Create performances, singly or by schedule","permission":"PERFORMANCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"CreatePerformancesRequest","responds":null},
"decideRecommendations": {"method":"POST","path":"/recommendations/decide","contract":"ai","summary":"Fill a recommendation slot","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRecommendationResult"},
"forceReleaseInventoryHold": {"method":"POST","path":"/inventory-holds/{inventoryHoldId}/force-release","contract":"catalogue","summary":"Reclaim a stranded inventory hold","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"InventoryHold"},
"getEvent": {"method":"GET","path":"/events/{eventId}","contract":"catalogue","summary":"Read an event","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Event"},
"getLatestBundle": {"method":"GET","path":"/catalogue/bundles/latest","contract":"catalogue","summary":"Pull the current bundle for this workstation's venue","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":"since","in":"query","required":null},{"name":"If-None-Match","in":"header","required":null}],"requestBody":null,"responds":"CatalogueBundle"},
"getOfflinePackage": {"method":"GET","path":"/access/offline-package","contract":"access","summary":"Entitlement and rule set for offline validation","permission":"ACCESS_VALIDATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":"sinceVersion","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":"validFrom","in":"query","required":true},{"name":"validTo","in":"query","required":true},{"name":"If-None-Match","in":"header","required":null}],"requestBody":null,"responds":"OfflinePackage"},
"getPerformance": {"method":"GET","path":"/performances/{performanceId}","contract":"catalogue","summary":"Read a performance","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Performance"},
"getSeatAvailability": {"method":"GET","path":"/performances/{performanceId}/seat-availability","contract":"seating","summary":"Seat status for a performance","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"sectionCode","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"availableOnly","in":"query","required":null},{"name":"mode","in":"query","required":null}],"requestBody":null,"responds":"SeatAvailability"},
"getVenueSettings": {"method":"GET","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Operational settings for this venue","permission":"TENANT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VenueSettings"},
"listCatalogueBundles": {"method":"GET","path":"/catalogue/bundles","contract":"catalogue","summary":"List published catalogue bundles","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BundleSummary"},
"listEvents": {"method":"GET","path":"/events","contract":"catalogue","summary":"List events","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listInventoryHolds": {"method":"GET","path":"/inventory-holds","contract":"catalogue","summary":"List inventory holds","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channelCapacityId","in":"query","required":null},{"name":"holderWorkstationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMenus": {"method":"GET","path":"/menus","contract":"fnb","summary":"List menus","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":"activeAt","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPerformances": {"method":"GET","path":"/events/{eventId}/performances","contract":"catalogue","summary":"List performances of an event","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"language","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRecipes": {"method":"GET","path":"/recipes","contract":"fnb","summary":"List recipes","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"search","in":"query","required":null},{"name":"menuItemId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSyncRejections": {"method":"GET","path":"/sync/rejections","contract":"orders","summary":"Entries the server refused","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"resolved","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listUpsellRules": {"method":"GET","path":"/upsell-rules","contract":"promotions","summary":"List upsell and cross-sell rules","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"placement","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkstations": {"method":"GET","path":"/workstations","contract":"tenancy","summary":"List workstations","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"saleBoardKind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"planProductionRun": {"method":"POST","path":"/production-runs","contract":"fnb","summary":"Plan a batch, for one outlet or several","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ProductionRun","responds":"ProductionRun"},
"publishBundle": {"method":"POST","path":"/catalogue/bundles","contract":"catalogue","summary":"Compute, sign and publish a catalogue bundle","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"BundleSummary"},
"recommendSeats": {"method":"POST","path":"/performances/{performanceId}/seat-recommendations","contract":"seating","summary":"Recommend seats for a party","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SeatRecommendationRequest","responds":null},
"recordRecommendationEvents": {"method":"POST","path":"/recommendations/events","contract":"ai","summary":"Report what happened to recommended items","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"relinquishInventoryHold": {"method":"DELETE","path":"/inventory-holds/{inventoryHoldId}","contract":"catalogue","summary":"Return unsold units","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"InventoryHold"},
"renewInventoryHold": {"method":"POST","path":"/inventory-holds/{inventoryHoldId}/renew","contract":"catalogue","summary":"Extend an inventory hold's TTL","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"InventoryHold"},
"reportBundleApplied": {"method":"POST","path":"/catalogue/bundles/{version}/applied","contract":"catalogue","summary":"Report that a workstation applied a bundle","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setIngredientSubstitutes": {"method":"PUT","path":"/recipes/{recipeId}/substitutes","contract":"fnb","summary":"Define approved substitutions","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"recipeId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":"FnbIngredientSubstitute","responds":"FnbIngredientSubstitute"},
"setMenuSections": {"method":"PUT","path":"/menus/{menuId}/sections","contract":"fnb","summary":"Set menu sections and their item ordering","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Menu"},
"setOfflinePolicy": {"method":"PUT","path":"/offline-policy","contract":"tenancy","summary":"What a workstation may do with no network, and for how long","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OfflinePolicy","responds":"OfflinePolicy"},
"setPathClosure": {"method":"POST","path":"/venue-maps/{mapId}/paths/{pathId}/closure","contract":"venue-map","summary":"Close a route during works or an incident","permission":"VENUE_MAP_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PathClosureResult"},
"setRecipe": {"method":"PUT","path":"/recipes","contract":"fnb","summary":"Define a recipe for a menu item","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"Recipe","responds":"Recipe"},
"setSubstitutionRules": {"method":"PUT","path":"/substitution-rules","contract":"fnb","summary":"What may replace what","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SubstitutionRule"},
"syncOrders": {"method":"POST","path":"/sync/orders","contract":"orders","summary":"Replay orders recorded offline","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderSyncResult"},
"updateEvent": {"method":"PATCH","path":"/events/{eventId}","contract":"catalogue","summary":"Amend an event","permission":"EVENT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Event"},
"updateMenu": {"method":"PATCH","path":"/menus/{menuId}","contract":"fnb","summary":"Amend a menu","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Menu"},
"updateOutlet": {"method":"PATCH","path":"/outlets/{outletId}","contract":"tenancy","summary":"Amend an outlet","permission":"REGION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Outlet"},
"updatePerformance": {"method":"PATCH","path":"/performances/{performanceId}","contract":"catalogue","summary":"Amend a performance","permission":"PERFORMANCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Performance"},
"updateSaleBoard": {"method":"PUT","path":"/sale-boards/{saleBoardId}","contract":"tenancy","summary":"Update a sale board","permission":"WORKSTATION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SaleBoard","responds":"SaleBoard"},
"verifyAllergens": {"method":"POST","path":"/menu-items/{menuItemId}/verify-allergens","contract":"fnb","summary":"Does this dish still match its claim?","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AllergenVerdict"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessAccreditationCredential": {"type":"object","x-ticvai-persistence":"access.accreditation_credential","x-ticvai-agreed":"29 September: build pass (group OWN, from group RA's handoff; BL-181); the events accreditation.credentialIssued and accreditation.holderStatusChanged name access as their critical consumer","description":"**What a gate needs to admit an accredited person, kept by `access`** (29 September, build). Written only by the consumers of `accreditation.credentialIssued` (a row per credential; a replacement sets the replaced row's `admits` false) and `accreditation.holderStatusChanged` (every credential of the holder: `admits` false unless the holder is `active`, validity taken from the event). Read by `validateAccess` and shipped in the offline package. The record of truth stays in `accreditation`; this is a copy shaped for the gate, never edited by a person.","required":["id","holderId","encodedIdentifier","admits","scopePath"],"properties":{"id":{"type":"string","format":"uuid","description":"The accreditation credential's id (`credentialId` on the events)."},"holderId":{"type":"string","format":"uuid"},"programmeId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","description":"printedBadge, mobileCredential, qr, nfcCard, rfidCard or wristband, as issued."},"encodedIdentifier":{"type":"string","x-ticvai-unique":"tenant","description":"What the gate reads from the credential. Never sent to webhook subscribers."},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"zoneIds":{"type":"array","description":"The holder's effective zones, from the event (`effectiveZones`).","items":{"type":"string","format":"uuid"}},"holderStatus":{"type":"string","enum":["active","suspended","revoked","expired","archived"],"description":"The holder's status as last published; only `active` admits."},"admits":{"type":"boolean","description":"False once the credential is replaced or the holder is not active."},"sourceChangedAt":{"type":"string","format":"date-time","description":"The `issuedAt` or `changedAt` of the event last applied; an older event arriving late is ignored."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005), the accreditation programme's scope."}}},
"AccessDynamicPolicy": {"type":"object","x-ticvai-persistence":"access.dynamic_policy","description":"One guest-admission dynamic (attribute-based) policy with its current content - type, context or identity it tests, condition expression, result, priority, zones, validity, status and current version. Not identity.authorisation_policy, which is staff permission (declared 29 September, data-model close-out DM1).\n\n**Guest admission lives here and nowhere else** (ADR-0068, accepted 1 October). `validateAccess` online and the gate offline evaluate the same active version: `getOfflinePackage` carries it, and every `scan_event` records the policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`) and the set it was decided under (`policySetVersion`). The condition is `conditionRule`, a closed JSON format (`AdmissionRule`), not free text. Identity's staff-permission engine was renamed `AuthorisationPolicy` on the same day, so \"access policy\" means this.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). **This one governs who may pass which gate**: admission of a guest, pass holder, accreditation holder or employee at an access point, decided in validation with results a gate acts on (allow, deny, review, requireId, requireBiometric, requireCompanion, requireSupervisor). **identity `AuthorisationPolicy` governs who may do what in the software**: a principal's permissions on operations and screens, decided by identity `evaluateAccess`. An employee's badge opening a staff door is decided here; the same employee approving a refund is decided in identity. Effectiveness is reported per engine: `listDynamicPolicyEffectiveness` here, `listAuthorisationPolicyEffectiveness` in identity.","required":["id","scopePath","name","policyType","conditionRule","result","status","currentVersion"],"properties":{"id":{"type":"string","format":"uuid","description":"The policyId"},"venueId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node; where it applies further is access.policy_scope_assignment"},"name":{"type":"string","maxLength":200},"policyType":{"type":"string","enum":["guestAttribute","accreditation","occupancy","employee","risk","membership","timeEvent"]},"contextType":{"type":"string","enum":["date","day","time","season","event","performance","specialEvent","holiday","operatingCalendar","occupancy","attractionStatus"],"nullable":true,"description":"Context/time/event policies (setContextTimeEvent)"},"identityType":{"type":"string","enum":["guest","member","annualPassHolder","employee","contractor","vendor","performer","media","vip","security","emergencyServices","eventStaff"],"nullable":true,"description":"Identity-based policies (listIdentityMembershipAccreditation)"},"conditionRule":{"$ref":"#/components/schemas/AdmissionRule","description":"The condition, in the closed JSON rule format evaluated the same way online and at the gate (ADR-0068; replaces the free-text `conditionExpression`)."},"result":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"]},"priority":{"type":"integer","nullable":true},"allowedZoneIds":{"type":"array","items":{"type":"string","format":"uuid"}},"deniedZoneIds":{"type":"array","items":{"type":"string","format":"uuid"}},"monitorThresholdPercent":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"description":"Occupancy policies. Percent at which the band becomes Monitor"},"restrictThresholdPercent":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"description":"Occupancy policies. Percent at which the band becomes Restrict"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"The grant expires automatically at validTo"},"status":{"type":"string","enum":["draft","pendingApproval","active","inactive","expired"],"default":"draft"},"currentVersion":{"type":"integer","minimum":1,"description":"The version in force (access.dynamic_policy_version)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AcquireLeaseRequest": {"type":"object","description":"The body of `acquireInventoryHold`. **Named before the 26 August rename** (lease to `InventoryHold`); the name stays because generated code is keyed on it.","required":["id","channelCapacityId","requestedUnits","ttlSeconds"],"properties":{"holderKind":{"$ref":"#/components/schemas/InventoryHoldHolderKind"},"cartId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `holderKind` is `cart`, else `400`. Sent by the order service from `orders.addCartLine` (SD-023, 29 September)."},"channel":{"allOf":[{"$ref":"#/components/schemas/Channel"}],"description":"Which channel's allocation to draw from. Defaults to the session's channel. A lease is granted against a channel allocation, not against raw capacity.\n"},"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key."},"channelCapacityId":{"type":"string","format":"uuid"},"requestedUnits":{"type":"integer","minimum":1},"ttlSeconds":{"type":"integer","minimum":30,"maximum":3600,"default":900,"description":"Short TTLs limit stranding when a terminal dies; long TTLs survive longer outages. The venue's default balances the two: **15 minutes (900 seconds), from the venue setting `cartLeaseSeconds`** with a tenant default (decided 28 September, audit R169; proposed, client to correct under audit R094).\n"}}},
"AiRecommendationItem": {"type":"object","x-ticvai-persistence":"none — held in jsonb on ai.rec_decision.items, through AiRecommendationItemList","description":"One recommended item. **Carries a Pricing price reference, never a computed price** (AIR-029).","required":["trackingId","rank"],"properties":{"trackingId":{"type":"string","format":"uuid","description":"Echoed on every `recordRecommendationEvents` event and as `orders.addCartLine.recommendationId`, so attribution never guesses."},"productId":{"type":"string","format":"uuid","nullable":true,"description":"The product recommended. **Exactly one of `productId`, `promotionId` or `couponRef`, `rewardId` or `challengeId` is set, by `kind`** (29 September, build): `offer` carries a promotion or coupon, `reward` a loyalty reward, `challenge` a challenge, every other kind a product."},"promotionId":{"type":"string","format":"uuid","nullable":true,"description":"For `offer`, a published promotion the guest is eligible for. Promotions computes the discount at the basket, never the engine."},"couponRef":{"type":"string","nullable":true,"description":"For `offer`, a coupon campaign; a code is assigned only when the guest takes it (`promotions.assignCoupon`)."},"rewardId":{"type":"string","format":"uuid","nullable":true,"description":"For `reward`, a marketing-crm loyalty reward the guest can redeem."},"challengeId":{"type":"string","format":"uuid","nullable":true,"description":"For `challenge`, a marketing-crm challenge the guest can join."},"kind":{"type":"string","enum":["upsell","crossSell","upgrade","bundle","addOn","membership","nextBestOffer","offer","reward","challenge"]},"rank":{"type":"integer","minimum":1},"priceRef":{"type":"string","nullable":true,"description":"The Pricing reference the channel resolves to a price. AI never computes a price."},"reasonTemplateKey":{"type":"string","nullable":true,"description":"The template reason (decided 29 September, decision 9): no model writes guest-visible reasons."},"reasonText":{"type":"string","nullable":true,"description":"The rendered template in the session locale, where the channel shows reasons."},"confidenceBand":{"type":"string","enum":["high","medium","low"],"description":"Design 5.6: a band, never a bare percentage."},"score":{"type":"number","nullable":true,"description":"Normalised score. **Returned to staff callers only**; a guest response omits it."}}},
"AiRecommendationResult": {"type":"object","x-ticvai-persistence":"none — written as ai.rec_decision after the response","description":"The recommendation slot's content (design 2.2 A). Empty `items` is a valid answer: the slot stays empty.","required":["decisionId","mode","items","expiresAt"],"properties":{"decisionId":{"type":"string","format":"uuid"},"placement":{"type":"string","enum":["productPage","cart","checkout","postPurchase","preVisit","inVenue","posBasket","kioskBasket","fnbMenu","retailBasket","seatUpgrade","membership","email","homepage","loyalty"]},"mode":{"type":"string","enum":["personalised","contextual","rulesOnly","fallback"]},"items":{"type":"array","items":{"$ref":"#/components/schemas/AiRecommendationItem"}},"expiresAt":{"type":"string","format":"date-time"}}},
"AllergenCode": {"type":"string","description":"**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n","enum":["gluten","crustaceans","eggs","fish","peanuts","soybeans","milk","nuts","celery","mustard","sesame","sulphites","lupin","molluscs"]},
"AllergenVerdict": {"x-ticvai-persistence":"fnb.allergen_verdict","type":"object","description":"One allergen check of one dish (decided 28 September, audit R241). Written by the server on every automatic run and by `verifyAllergens` on a manual re-check; `getAllergenVerification` reads the latest.\n","required":["menuItemId","matches","checkedAt","trigger"],"properties":{"menuItemId":{"type":"string","format":"uuid"},"matches":{"type":"boolean"},"declared":{"type":"array","items":{"type":"string"}},"actual":{"type":"array","items":{"type":"string"}},"undeclared":{"type":"array","description":"**Present in the dish and absent from the label.** The dangerous direction, and the response leads with it.\n","items":{"type":"object","properties":{"allergen":{"type":"string"},"via":{"type":"string","enum":["ingredient","substitution","modifier","sharedEquipment"]},"sourceRef":{"type":"string"}}}},"overDeclared":{"type":"array","description":"Labelled and no longer present. **Safe, and still worth fixing** — a menu that over-declares teaches guests the labels are guesses.\n","items":{"type":"string"}},"checkedAt":{"type":"string","format":"date-time","readOnly":true},"trigger":{"type":"string","readOnly":true,"description":"What ran the check. `manual` is the Verify button; the others are the automatic run after that change (audit R241).","enum":["manual","recipeChanged","substitutionChanged","modifierChanged"]}}},
"BundleSummary": {"x-ticvai-persistence":"none — projection over bundle","type":"object","description":"One published catalogue bundle — the signed snapshot terminals pull (ADR-0013). Not `promotions.Bundle`, which is a sellable product made of other products.","required":["version","venueId","publishedAt","publishedBy","contentHash","staleAfter","sizeBytes"],"properties":{"version":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"publishedAt":{"type":"string","format":"date-time"},"publishedBy":{"type":"string","format":"uuid"},"contentHash":{"type":"string"},"signatureKeyId":{"type":"string","description":"Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle.\n"},"staleAfter":{"type":"string","format":"date-time"},"sizeBytes":{"type":"integer"},"note":{"type":"string"},"appliedByWorkstations":{"type":"integer"}}},
"CatalogueBundle": {"x-ticvai-persistence":"catalogue.published_bundle","type":"object","required":["version","venueId","isDelta","signature","signatureKeyId","contentHash","staleAfter","payload"],"properties":{"version":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"isDelta":{"type":"boolean"},"baseVersion":{"type":"string","nullable":true,"description":"Present when `isDelta`. The version this delta applies to."},"signature":{"type":"string","description":"Detached signature over `contentHash`. The terminal verifies before applying and rolls back on failure — a half-applied catalogue is never traded against.\n"},"signatureKeyId":{"type":"string"},"contentHash":{"type":"string"},"staleAfter":{"type":"string","format":"date-time"},"payload":{"type":"object","description":"Products, variants, price lists, prices, tax codes, events, performances, envelope definitions, data mask field definitions and the venue's sale boards. Shape is versioned with the bundle format, not with this API.\n","additionalProperties":true,"properties":{"saleBoards":{"type":"array","description":"**The venue's sale boards as `tenancy.listSaleBoards` returns them**, read from `platform.sale_board` when the bundle is snapshotted (decided 28 September, audit R129 (4)). A board changed by `updateSaleBoard` reaches terminals here, with the next bundle, and never mid-transaction.\n","items":{"type":"object","additionalProperties":true}}}}}},
"CatalogueState": {"x-ticvai-persistence":"none — computed from workstation bundle_version","type":"object","description":"The workstation's local catalogue position. A terminal beyond `staleAfter` must refuse to trade rather than transact against stale prices.\n","required":["appliedBundleVersion","appliedAt","staleAfter","isStale"],"properties":{"appliedBundleVersion":{"type":"string"},"appliedAt":{"type":"string","format":"date-time"},"staleAfter":{"type":"string","format":"date-time","description":"Beyond this the terminal refuses to trade."},"isStale":{"type":"boolean"},"pendingBundleVersion":{"type":"string","nullable":true,"description":"Published but not yet applied."}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"CreateEventRequest": {"type":"object","required":["code","name","venueId"],"properties":{"code":{"type":"string","maxLength":64,"x-ticvai-unique":"tenant","description":"**Unique per tenant** (decided 28 September, audit R108). A code already used by any event in the tenant is refused with `409 duplicate-code`.\n"},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"parentEventId":{"type":"string","format":"uuid"}}},
"CreateOrderRequest": {"type":"object","required":["id","venueId","channel","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. Offline replay through `syncOrders` carries no header, and this id alone deduplicates there.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"#/components/schemas/Channel"},"shiftId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null for an anonymous sale. Identity and entitlement are separate."},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells."},"catalogueBundleVersion":{"type":"string","description":"The bundle the client priced from. Lets the server explain a variance rather than merely report one.\n"},"lines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"recordedAt":{"type":"string","format":"date-time"}}},
"CreatePaymentRequest": {"type":"object","required":["id","orderId","tender","amount","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. Omit for a payment in the venue's own currency."},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**What the guest handed over**, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). For cash, change is the difference.\n"},"walletAuthorisationId":{"type":"string","nullable":true,"description":"Cross-cell wallet hold, where the guest's home cell is elsewhere."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"description":"For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table."},"returnUrl":{"type":"string","format":"uri","nullable":true,"description":"Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). Required for a card payment from the guest web or app."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal to instruct, for a card payment at a till (ECR flow, SD-034)."},"deviceId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"CreatePerformancesRequest": {"type":"object","required":["startsAt","endsAt"],"properties":{"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"admissionRulesId":{"type":"string","format":"uuid"},"seatMapId":{"type":"string","format":"uuid"},"language":{"type":"string","nullable":true,"maxLength":35,"pattern":"^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$","description":"As `Performance.language`; every performance of a generated series takes it (decided 29 September, rev 3 REV3-17)."},"format":{"type":"string","nullable":true,"maxLength":40,"description":"As `Performance.format` (decided 29 September, rev 3 REV3-17)."},"recurrence":{"type":"object","description":"Generate a series rather than a single performance. **Read in the region's time zone**: the Region owns the zone and every venue inherits it without override (tenancy), so `daysOfWeek` are the region's calendar days and `until` is compared on the region's clock.\n","properties":{"intervalMinutes":{"type":"integer","minimum":1},"until":{"type":"string","format":"date-time"},"daysOfWeek":{"type":"array","items":{"type":"integer","minimum":0,"maximum":6}}}}}},
"DeploymentProfile": {"type":"string","description":"How this workstation obtains catalogue and inventory (ADR-0013).\n- `terminalLocal` — own SQLite, leases direct from the cell. Small venues, 4G sites - `venueEdge` — own SQLite, distributed via the venue edge node which holds the\n  venue lease and sub-leases to terminals. Mid and large venues, stadium gates\n- `thin` — no local catalogue, server reads. Non-transactional surfaces only\n","enum":["terminalLocal","venueEdge","thin"]},
"DeviceBinding": {"x-ticvai-persistence":"platform.device","type":"object","required":["kind","driver"],"properties":{"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Driver identifier. Adding a vendor is a driver plus configuration, never a core change — every venue arrives with hardware not previously seen.\n"},"identifier":{"type":"string","description":"Serial","port or network address.":null},"isRequired":{"type":"boolean","default":false,"description":"When true, the workstation refuses to open a shift if the device is absent.\n"}}},
"Event": {"x-ticvai-persistence":"catalogue.event","type":"object","required":["id","code","name","venueId","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentEventId":{"type":"string","format":"uuid","nullable":true,"description":"For grouped events."},"performanceCount":{"type":"integer","readOnly":true,"description":"How many performances the event has. Counted by the server; never sent by a client."},"isActive":{"type":"boolean"}}},
"FnbIngredientSubstitute": {"type":"object","x-ticvai-persistence":"fnb.ingredient_substitute","description":"**Taken from the backend workbook, 20 September.** Defines approved ingredient substitutions for F&B preparation.","required":["fromInventoryItemId","toInventoryItemId","substitutionRatio","requiresApproval","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"fromInventoryItemId":{"type":"string","format":"uuid"},"toInventoryItemId":{"type":"string","format":"uuid"},"substitutionRatio":{"type":"number"},"conditionsJson":{"type":"string","nullable":true},"allergensAddedJson":{"type":"string","nullable":true},"allergensRemovedJson":{"type":"string","nullable":true},"requiresApproval":{"type":"boolean"},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"}}},
"InventoryHold": {"x-ticvai-persistence":"catalogue.inventory_hold","type":"object","required":["id","channelCapacityId","holderKind","grantedUnits","consumedUnits","status","acquiredAt","expiresAt"],"properties":{"id":{"type":"string"},"channelCapacityId":{"type":"string","format":"uuid"},"holderKind":{"$ref":"#/components/schemas/InventoryHoldHolderKind"},"holderWorkstationId":{"type":"string","format":"uuid","nullable":true,"description":"The holding workstation when `holderKind` is `workstation`; null on a cart hold, because a browser has none (SD-023, 29 September)."},"holderCartId":{"type":"string","format":"uuid","nullable":true,"description":"The holding cart (`orders.cart`) when `holderKind` is `cart` (SD-023, 29 September)."},"convertedOrderId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The paid order the hold was converted for, set by `convertInventoryHold`."},"convertedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"parentLeaseId":{"type":"string","nullable":true,"description":"Present when sub-leased from a venue edge node."},"requestedUnits":{"type":"integer"},"channel":{"allOf":[{"$ref":"#/components/schemas/Channel"}],"description":"Allocation this lease draws from."},"grantedUnits":{"type":"integer","description":"May be less than requested — a partial grant is not an error. Constrained by the channel's remaining allocation plus the general pool, never by raw capacity.\n"},"consumedUnits":{"type":"integer"},"status":{"$ref":"#/components/schemas/LeaseStatus"},"acquiredAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"},"releasedAt":{"type":"string","format":"date-time","nullable":true},"forceReleasedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"forceReleaseReason":{"type":"string","nullable":true}}},
"InventoryHoldHolderKind": {"type":"string","enum":["workstation","cart"],"default":"workstation","description":"**Who holds the units** (decided 29 September, SD-023). A till, kiosk or edge node holds as a `workstation`; a guest's web or app cart holds as a `cart`, acquired by the order service. A browser has no workstation, so a cart hold carries `cartId` and no `holderWorkstationId`.\n"},
"LeaseStatus": {"type":"string","description":"`states/lease.yaml`. **`expired` is set by that model's timer transition when `expiresAt` passes without a renewal**, not by any operation in this contract. The job that runs the timer is the sweeper ADR-0037 deferred: it returns an expired hold's unconsumed units to `remaining` in the same guarded statement as a release (SD-023, 29 September), and **writes `inventoryHold.expired` to the outbox in the same transaction** (SD-023/SD-033, applied 30 September; `events/inventoryHold-expired.yaml`), so the cart that held the units hears of it before checkout. A `converted` hold is never swept.\n**`converted` is set by `convertInventoryHold`** when the order that holds the units is paid (decided 29 September, SD-023); its units are `sold` and the sweeper never touches it.\n","enum":["active","expired","released","forceReleased","converted"]},
"Menu": {"x-ticvai-persistence":"fnb.menu","type":"object","required":["id","code","name","outletId","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"outletId":{"type":"string","format":"uuid"},"availability":{"$ref":"#/components/schemas/MenuAvailability"},"sections":{"type":"array","items":{"$ref":"#/components/schemas/MenuSection"}},"isActive":{"type":"boolean"},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `MenuVersion.version` live now. Null for a menu never published."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"MenuAvailability": {"x-ticvai-persistence":"none — embedded in menu","type":"object","description":"When this menu is in force. Absent means always. Days, times and dates are all read in the Region's time zone, not UTC.","properties":{"daysOfWeek":{"type":"array","items":{"type":"integer","minimum":0,"maximum":6}},"startTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Wall-clock time, in the Region's time zone."},"endTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Wall-clock time, in the Region's time zone."},"validFrom":{"type":"string","format":"date","nullable":true,"description":"Calendar day, in the Region's time zone, not UTC."},"validTo":{"type":"string","format":"date","nullable":true,"description":"Calendar day, in the Region's time zone, not UTC."}}},
"MenuItem": {"x-ticvai-persistence":"fnb.menu_item","type":"object","required":["id","productVariantId","name","price","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"productVariantId":{"type":"string","format":"uuid","description":"The catalogue variant this item sells. Pricing and tax come from there — a menu is a presentation of the catalogue, not a second catalogue.\n"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"sortOrder":{"type":"integer"},"modifierGroupIds":{"type":"array","items":{"type":"string","format":"uuid"}},"stationId":{"type":"string","format":"uuid","nullable":true},"menuSectionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The section the item sits in, set by `setMenuSections` and `applyMenuActions` (`moveSection`)."},"isStockTracked":{"type":"boolean","description":"True where a recipe exists. Stock-tracked items cannot be sold offline."},"isAvailable":{"type":"boolean"},"unavailableReason":{"type":"string","nullable":true},"restoreAt":{"type":"string","format":"date-time","nullable":true,"description":"When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand."},"preparationMinutes":{"type":"integer","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}}}},
"MenuSection": {"x-ticvai-persistence":"fnb.menu_section","type":"object","required":["code","name","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string"},"name":{"type":"string"},"sortOrder":{"type":"integer"},"items":{"type":"array","description":"The section's items, in sale-board order. An item's membership is `MenuItem.menuSectionId`.","items":{"$ref":"#/components/schemas/MenuItem"}}}},
"OfflineOrder": {"x-ticvai-persistence":"none — client-side journal, not server storage","allOf":[{"$ref":"#/components/schemas/CreateOrderRequest"},{"type":"object","required":["sequence","payments"],"properties":{"sequence":{"type":"integer","minimum":1,"description":"Monotonic per device. Processed in this order."},"payments":{"type":"array","items":{"$ref":"#/components/schemas/CreatePaymentRequest"}}}}]},
"OfflinePackage": {"x-ticvai-persistence":"none — generated artefact in object storage","type":"object","required":["etag","generatedAt","validFrom","validTo","accessPointId","entitlements"],"properties":{"etag":{"type":"string"},"generatedAt":{"type":"string","format":"date-time"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"accessPointId":{"type":"string","format":"uuid"},"entitlementsVersion":{"type":"integer","description":"The highest `access.entitlement` change included (SD-052, 29 September). A refresh sends it as `sinceVersion` and receives only what changed after it, so a 60,000-guest venue is not re-sent whole."},"policySetVersion":{"type":"string","description":"**The active admission policy version the package carries** (ADR-0068, 1 October): a fingerprint of the `(id, currentVersion)` of every policy in `dynamicPolicies`, computed the same way by `validateAccess` online. Every scan the gate records carries it (`ScanEvent.policySetVersion`), so a scan decided offline under a set that has since changed is visible at sync rather than assumed equal."},"dynamicPolicies":{"type":"array","description":"The active guest-admission dynamic policies for this access point's zones (SD-052), each at its active version with its `conditionRule` (ADR-0068), so an offline gate applies the same rules as an online one.","items":{"$ref":"#/components/schemas/AccessDynamicPolicy"}},"entitlements":{"type":"array","description":"Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device removes them.","items":{"type":"object","required":["ticketId","mediaCodes","validFrom","validTo","entriesAllowed","reentryAllowed"],"properties":{"ticketId":{"type":"string","format":"uuid","description":"The `Entitlement.id`."},"mediaCodes":{"type":"array","items":{"type":"string"},"description":"A ticket may carry several media over its life."},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"performanceId":{"type":"string","format":"uuid","nullable":true},"entriesAllowed":{"type":"integer","nullable":true},"entriesUsed":{"type":"integer"},"reentryAllowed":{"type":"boolean"},"admissionRulesId":{"type":"string","format":"uuid"}}}},"delegatedRights":{"type":"array","description":"Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits when the inter-cell link is down — the same reason locally issued entitlements are included.\n","items":{"type":"object","required":["rightId","ticketId","issuingCellId","validFrom","validTo","entriesAllowed","entriesConsumed"],"properties":{"rightId":{"type":"string"},"ticketId":{"type":"string","format":"uuid","description":"The `Entitlement.id` in the issuing cell."},"issuingCellId":{"type":"string"},"guestLinkId":{"type":"string","nullable":true},"mediaCodes":{"type":"array","items":{"type":"string"}},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"entriesAllowed":{"type":"integer","nullable":true},"entriesConsumed":{"type":"integer"},"admissionRulesId":{"type":"string","format":"uuid"}}}},"blacklist":{"type":"array","items":{"type":"string"},"description":"Media codes to deny outright regardless of entitlement state."},"admissionRules":{"type":"array","items":{"type":"object","required":["id","openMinutesBefore","closeMinutesAfter"],"properties":{"id":{"type":"string","format":"uuid"},"openMinutesBefore":{"type":"integer"},"closeMinutesAfter":{"type":"integer"},"maxDurationMinutes":{"type":"integer","nullable":true},"requiresExitBeforeReentry":{"type":"boolean"}}}},"accreditationCredentials":{"type":"array","description":"Accreditation credentials that admit at this access point, from access.accreditation_credential (29 September, build; BL-181). Only rows that admit are included; a credential dropped from one package to the next no longer admits.","items":{"$ref":"#/components/schemas/AccessAccreditationCredential"}}}},
"OfflinePolicy": {"type":"object","x-ticvai-persistence":"platform.offline_policy","description":"Board 5 of the client's POS set. **ADR-0013 makes the POS local-first and nothing configured the policy** — one of only two things in 36 board screens the package genuinely could not do.\nCF-115 reframed offline into three data classes: catalogue and policy always local, contended inventory leased, transactional facts journalled. **This is where a venue says how far that goes for them.**\n**One per scope node, keyed on `scopePath`** (pull audit R162). `id` is server-owned and absent where `getOfflinePolicy` returns the defaults for a node with nothing saved.\n**The `minimum` and `maximum` on each field are proposed, client to correct (decided 28 September, audit R129).** A value outside them is refused `400`, `errors[]` naming the field.\n","required":["scopePath"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$","description":"**The node this policy is for, and the key `setOfflinePolicy` upserts on.** The body names its target here, because the path does not.\n"},"maxOfflineHours":{"type":"integer","default":24,"minimum":1,"maximum":72,"description":"**After which the workstation refuses to sell rather than keep journalling.** A till three days offline holding 900 unsynced sales is a reconciliation nobody can do and a fraud nobody can detect. Bounds 1 to 72 hours: proposed, client to correct (audit R129).\n"},"allowedOffline":{"type":"array","description":"**What may happen with no network**, by data class. Selling from a cached catalogue is safe; issuing a refund is not, because the original sale cannot be verified.\n","items":{"type":"string","enum":["sale","refund","exchange","entitlementIssue","entitlementValidate","loyaltyAccrual","loyaltyRedemption","walletSpend","priceOverride","discount","voidLine","noSale"]}},"offlineValueCeiling":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129).\n"},"offlineTransactionCeiling":{"type":"integer","nullable":true,"minimum":1,"maximum":5000,"description":"**A ceiling on count as well as value.** Nine hundred small sales and one large one are different risks, and a value ceiling alone catches only the second. Bounds 1 to 5,000: proposed, client to correct (audit R129).\n"},"onCeilingBreach":{"type":"string","enum":["warn","blockNewSales","blockAll"],"default":"blockNewSales"},"requiresManagerToExtend":{"type":"boolean","default":true}}},
"OpeningHoursWindow": {"type":"object","description":"26 September, pull audit R088. **One weekly window an outlet is open.** `Outlet.openingHours` was an array of untyped objects. The shape is the one `supportHours.windows` already uses — a day and a from/to — with the times as local `HH:MM` in the region's time zone. Several windows on one day are a split shift, such as lunch and dinner.\n","required":["day","from","to"],"properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time, 24-hour `HH:MM`, when the outlet opens."},"to":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time, 24-hour `HH:MM`, when the outlet closes."}}},
"OrderSyncResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["accepted","results"],"properties":{"accepted":{"type":"integer"},"stoppedAtSequence":{"type":"integer","nullable":true,"description":"First entry that hit a **transient** failure (SD-028, 29 September): a refusal on the merits no longer stops the batch. Null when every entry was accepted, duplicate or quarantined. The client retries from here and never past it.\n"},"results":{"type":"array","items":{"type":"object","required":["id","sequence","status"],"properties":{"id":{"type":"string","format":"uuid","description":"The `OfflineOrder.id` this result is about."},"sequence":{"type":"integer"},"status":{"type":"string","enum":["accepted","duplicate","rejected","blockedByRejection"],"description":"`rejected`: refused on its merits and quarantined in `sync.rejection`; the batch continues. `blockedByRejection`: depends on a rejected entry for the same order (a void, a refund, a later payment) and is quarantined with it (SD-028, 29 September)."},"orderNumber":{"type":"string","nullable":true},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Posted to the variance account. Not surfaced to the cashier."},"varianceExceedsThreshold":{"type":"boolean","description":"True when review is required per the venue's variance threshold."},"rejectionId":{"type":"string","nullable":true,"description":"For a `rejected` or `blockedByRejection` entry, the `sync.rejection` row it was quarantined into (SD-028). The batch carried on past it."},"error":{"$ref":"../shared/common.yaml#/components/schemas/Problem"}}}}}},
"Outlet": {"type":"object","x-ticvai-persistence":"platform.outlet","required":["id","code","name","venueId","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/OutletKind"},"zone":{"type":"string","nullable":true},"stockLocationId":{"type":"string","format":"uuid","nullable":true,"description":"Where this outlet draws stock from. A shop and its stockroom are one location; a bar drawing from a central cellar is not.\n"},"costCenterId":{"type":"string","format":"uuid","nullable":true,"description":"Revenue and cost attribution. Outlet is the natural grain for both."},"openingHours":{"type":"array","description":"The weekly pattern, one entry per window. Several windows on a day are allowed.","items":{"$ref":"#/components/schemas/OpeningHoursWindow"}},"isActive":{"type":"boolean"}}},
"OutletKind": {"type":"string","enum":["shop","restaurant","bar","cafe","kiosk","gameFloor","ticketOffice","mobile"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PathClosureResult": {"description":"What `setPathClosure` returns: the path, and **what a forced closure cut off**, named.\n","allOf":[{"$ref":"#/components/schemas/VenuePath"},{"type":"object","properties":{"strandedPoints":{"type":"array","readOnly":true,"description":"Points no longer reachable because of this closure. Empty unless `force` was used.\n","items":{"$ref":"#/components/schemas/StrandedPoint"}}}}]},
"Performance": {"x-ticvai-persistence":"catalogue.performance","type":"object","required":["id","eventId","startsAt","endsAt","status"],"properties":{"id":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"description":"BL-048. **The approval chain and the occurrence lifecycle sat on different entities**, so neither was complete: `states/performance.yaml` models scheduled, onSale, soldOut, suspended, cancelled and completed properly, and nothing said which of those transitions somebody had to sign.\n**Set on the transition that needs it, not on the performance.** Publishing a performance is routine; cancelling one that has sold is the act somebody signs — and binding approval to the whole entity would have required a signature to reschedule a wet Tuesday.\n"},"requiresApprovalToCancel":{"type":"boolean","default":true,"description":"**Cancelling a sold performance is the one transition that needs a name against it.** `assessProductChange` already answers how many tickets are affected; this decides who has to look at that number before the button works.\n"},"status":{"type":"string","enum":["scheduled","onSale","soldOut","suspended","cancelled","completed"]},"admissionRulesId":{"type":"string","format":"uuid","nullable":true},"seatMapId":{"type":"string","format":"uuid","nullable":true},"language":{"type":"string","nullable":true,"maxLength":35,"pattern":"^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$","description":"The language the performance is given in, as a BCP 47 tag (`en`, `ar`, `fr`, `de`, `zh`, `ru`, `ar-AE`). **A guided tour at 10:00 in French and one at 10:00 in Arabic are two performances**, so a guest who picks a language sees only the tours in it (`listPerformances` `language`). Null when the performance is not language-specific (decided 29 September, rev 3 REV3-17).\n"},"format":{"type":"string","nullable":true,"maxLength":40,"description":"How it is presented, free text the venue chooses, e.g. `2D`, `3D`, `IMAX`, `subtitled`. A cinema screening shows language and format together. Null when it does not apply (decided 29 September, rev 3 REV3-17).\n"}}},
"PerformanceCancellationResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["performanceId","dryRun","affectedOrders","refundExposure"],"properties":{"performanceId":{"type":"string","format":"uuid"},"dryRun":{"type":"boolean"},"affectedOrders":{"type":"integer"},"affectedGuests":{"type":"integer"},"refundExposure":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the cancellation costs. Returned before committing, so the person cancelling sees the number at the moment they decide.\n"},"bulkRefundBatchId":{"type":"string","nullable":true,"description":"**Null on this response.** The refund batch is created by `orders` when it consumes `performance.cancelled` (F09), after this call has returned, and is queued there for approval — refunds are not issued automatically. Read it from orders, not from here.\n"},"notificationsQueued":{"type":"integer"}}},
"Point": {"type":"object","required":["x","y"],"properties":{"x":{"type":"number"},"y":{"type":"number"}}},
"ProductionRun": {"type":"object","x-ticvai-persistence":"fnb.production_run","description":"BL-129. **A central kitchen makes 400 portions at 6am for four outlets**, and nothing modelled that — orders consume stock and no operation produced any.\n**Production converts ingredients into a sellable item**, which is a stock movement in both directions at once, and treating it as two unrelated adjustments loses the yield.\n","required":["id","recipeId","plannedQuantity","status"],"properties":{"id":{"type":"string","format":"uuid"},"recipeId":{"type":"string","format":"uuid"},"productionPlanId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The plan whose release created this run. Null for a run planned directly."},"stationId":{"type":"string","format":"uuid","nullable":true,"description":"**The station whose prep list this run is on.** Copied from the plan line on release, where runs are grouped by station (audit R125 (7)).\n"},"producingOutletId":{"type":"string","format":"uuid"},"forOutletIds":{"type":"array","description":"**Where it goes.** A central kitchen produces for outlets that did not make it.\n","items":{"type":"string","format":"uuid"}},"plannedQuantity":{"type":"number"},"actualQuantity":{"type":"number","nullable":true,"description":"BL-126. **Theoretical against actual is the whole point of recording this.** A recipe says 400 portions from the ingredients issued; the run says how many were made, and the gap is waste, theft or a recipe that is wrong.\n"},"scheduledFor":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["planned","inProgress","completed","cancelled"]},"varianceReason":{"type":"string","nullable":true}}},
"Recipe": {"x-ticvai-persistence":"fnb.recipe + fnb.recipe_ingredient","type":"object","required":["menuItemId","ingredients"],"properties":{"menuItemId":{"type":"string","format":"uuid"},"yield":{"type":"number","minimum":0,"description":"Portions produced by one execution."},"ingredients":{"type":"array","minItems":1,"items":{"type":"object","required":["inventoryItemId","quantity","unit"],"properties":{"inventoryItemId":{"type":"string","format":"uuid"},"quantity":{"type":"number","minimum":0},"unit":{"type":"string"},"isOptional":{"type":"boolean","default":false}}}},"costPerPortion":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"**Computed, never entered** (decided 28 September, audit R125 (9)): the sum of each ingredient quantity at its current inventory cost, divided by `yield`. Recomputed when the recipe or an ingredient cost changes.\n"}}},
"SaleBoard": {"x-ticvai-persistence":"platform.sale_board","type":"object","required":["id","code","name","venueId","kind","pages"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SaleBoardKind"},"pages":{"type":"array","minItems":1,"items":{"type":"object","required":["name","sortOrder","tiles"],"properties":{"name":{"type":"string"},"sortOrder":{"type":"integer"},"tiles":{"type":"array","items":{"type":"object","required":["position","kind"],"properties":{"position":{"type":"integer"},"kind":{"type":"string","enum":["product","category","action","spacer"]},"variantId":{"type":"string","format":"uuid","nullable":true},"label":{"type":"string"},"colour":{"type":"string","nullable":true},"imageAssetRef":{"type":"string","nullable":true}}}}}}},"isActive":{"type":"boolean"}}},
"SaleBoardKind": {"type":"string","enum":["ticketing","fnb","retail","mixed"]},
"SeatAvailability": {"x-ticvai-persistence":"none — computed from seat, hold and block","type":"object","required":["performanceId","seatMapId","renderMode","totals","seats"],"properties":{"performanceId":{"type":"string","format":"uuid"},"seatMapId":{"type":"string","format":"uuid"},"renderMode":{"type":"string","enum":["graphical","list"],"description":"The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat map's `noGeometry` state), so the client sells from categories and best-available groups and does not draw a plan. `graphical` means every seat carries `position`.\n"},"totals":{"type":"object","properties":{"total":{"type":"integer"},"available":{"type":"integer"},"held":{"type":"integer"},"sold":{"type":"integer"},"blocked":{"type":"integer"},"buffered":{"type":"integer"}}},"byCategory":{"type":"array","items":{"type":"object","properties":{"categoryId":{"type":"string","format":"uuid"},"available":{"type":"integer"},"sold":{"type":"integer"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"sections":{"type":"array","description":"The map's sections with what a guest screen needs to show the view from each (decided 29 September, rev 3 23SEP-14): the photo where the venue supplied one, otherwise null and the client renders the view from `boundary` and the seat positions. In this response so WEB-007 and GST-049 need no second call.\n","items":{"type":"object","required":["code","name"],"properties":{"code":{"type":"string"},"name":{"type":"string"},"viewAssetId":{"type":"string","format":"uuid","nullable":true,"description":"As `Section.viewAssetId`. Null means render the view from geometry."},"boundary":{"type":"array","nullable":true,"items":{"$ref":"#/components/schemas/Point"},"description":"As `Section.boundary`. Null when `renderMode` is `list`."}}}},"seats":{"type":"array","items":{"type":"object","required":["seatId","status"],"properties":{"seatId":{"type":"string"},"status":{"$ref":"#/components/schemas/SeatStatus"},"categoryId":{"type":"string","format":"uuid","nullable":true},"displayLabel":{"type":"string","description":"What the guest sees, e.g. `A2-7-11`, as on `Seat`."},"position":{"allOf":[{"$ref":"#/components/schemas/Point"}],"nullable":true,"description":"The seat's coordinates on the map, as on `Seat`. Present when `renderMode` is `graphical`; null when it is `list`."}}}}}},
"SeatRecommendation": {"x-ticvai-persistence":"none — computed","type":"object","required":["seatIds","totalPrice","isContiguous","rank"],"properties":{"seatIds":{"type":"array","items":{"type":"string"}},"displayLabels":{"type":"array","items":{"type":"string"}},"totalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"categoryId":{"type":"string","format":"uuid"},"isContiguous":{"type":"boolean"},"rank":{"type":"integer","description":"Best first."},"rationale":{"type":"string","description":"Why this option was chosen — closest to stage, best value in category, only contiguous block remaining. Shown to a call-centre agent, not the guest.\n"}}},
"SeatRecommendationRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["partySize","strategy"],"properties":{"partySize":{"type":"integer","minimum":1,"maximum":50},"strategy":{"$ref":"#/components/schemas/SeatRecommendationStrategy"},"categoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"maxPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"accessibleCount":{"type":"integer","default":0,"description":"Wheelchair spaces in the party. Companions are added automatically."},"maxOptions":{"type":"integer","default":3,"maximum":10}}},
"SeatRecommendationStrategy": {"type":"string","enum":["bestAvailable","bestValue","closestToStage","accessible","contiguous"]},
"SeatStatus": {"type":"string","enum":["available","held","sold","blocked","buffered","unavailable"]},
"StrandedPoint": {"type":"object","x-ticvai-persistence":"none — computed from the graph","required":["pointId","name","kind","isCritical"],"properties":{"pointId":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string"},"isCritical":{"type":"boolean","description":"First aid, an emergency exit or an assembly point, the same set as `GraphValidation.criticalUnreachable`. **The one the operator must read first.**\n"}}},
"SubstitutionRule": {"type":"object","x-ticvai-persistence":"fnb.substitution_rule","description":"Board 2L, 24 August. **What may replace what, and under what conditions.** A kitchen substitutes constantly — a supplier is short, an item is 86'd, a guest asks — and the package had no way to say which swaps are allowed.\n**The rule exists so `verifyAllergens` has something to check against.** A substitution with no rule behind it is a decision made at the pass by whoever is standing there.\n**`allergensAdded` and `allergensRemoved` are the fields this table is for.** Swapping butter for margarine removes dairy and may add soy — **and a dish still labelled dairy-free after a swap nobody checked is the failure this prevents.**\n","required":["id","recipeId","fromIngredientId","toIngredientId"],"properties":{"id":{"type":"string","format":"uuid"},"recipeId":{"type":"string","format":"uuid","description":"**The recipe the rule applies to** (decided 28 September, audit R125 (10)). Not a menu item and not the whole venue: a swap that is safe in one dish is not safe in another.\n"},"fromIngredientId":{"type":"string","format":"uuid"},"toIngredientId":{"type":"string","format":"uuid"},"ratio":{"type":"number","default":1,"description":"**Not always one to one.** Fresh herbs to dried is roughly three to one, and a rule that assumes parity produces a dish nobody would serve.\n"},"allergensAdded":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}},"allergensRemoved":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}},"conditions":{"type":"array","items":{"type":"string","enum":["outOfStock","seasonal","guestRequest","costSaving","always"]}},"requiresApproval":{"type":"boolean","default":false,"description":"**True where the swap changes an allergen.** A chef may substitute freely within a claim; changing the claim is somebody else's decision.\n"},"isActive":{"type":"boolean","default":true}}},
"SupervisorStepUp": {"type":"object","description":"**A supervisor signs the act in place, on the device making the call** (decided 28 September, audit R144). Used where the decision is a same-device step-up rather than an approval request: reopening a shift, recounting a stock count, a retail return above the venue threshold, and (proposed by the coordinator, client to confirm) closing a stock transfer short and cancelling a performance.\n\n**The verification rule, the same on every operation that takes it:** the server checks `credential` against `principalId`; that principal must hold the operation's `x-ticvai-permission` at the operation's scope, must be active at that venue, and must not be the person whose act is being reversed where the operation says so. Any failure is a `403` (`supervisor-step-up-refused`) and nothing is written. **No approval request is raised**, and the operation declares `x-ticvai-step-up: pin`.\n","required":["principalId","credential"],"properties":{"principalId":{"type":"string","format":"uuid","description":"The supervisor signing. Recorded against the act."},"credential":{"type":"string","maxLength":512,"writeOnly":true,"description":"The supervisor's staff PIN, as they sign in at a till with it. **A PIN, never a password** (audit R123 (7)). Never stored or returned."}}},
"SyncRejection": {"x-ticvai-persistence":"sync.rejection","type":"object","required":["id","workstationId","kind","rejectedAt","problem"],"properties":{"id":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["order","payment","refund","void","scan"]},"recordedAt":{"type":"string","format":"date-time"},"rejectedAt":{"type":"string","format":"date-time"},"problem":{"$ref":"../shared/common.yaml#/components/schemas/Problem"},"payload":{"type":"object","additionalProperties":true,"description":"**Deliberately open: the journal entry exactly as the till sent it.** Its shape is the request schema for `kind` — an `OfflineOrder` for `order`, a `CreatePaymentRequest` for `payment` — kept verbatim so the supervisor resolves what was actually recorded, not a re-typed copy.\n"},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"resolution":{"type":"string","nullable":true,"readOnly":true,"enum":["posted","voided","refunded"],"description":"What `resolveSyncRejection` recorded. Null while the rejection waits."},"resolvedRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The order, void or refund the resolution produced — what stops the entry being posted twice."}}},
"UpsellPlacement": {"type":"string","enum":["productDetail","cart","checkout","postPurchase","atGate","inVenue"]},
"UpsellRule": {"x-ticvai-persistence":"promotions.upsell_rule","type":"object","required":["id","name","placement","triggerVariantIds","suggestedVariantIds"],"properties":{"id":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid","readOnly":true,"description":"The region that owns the rule. Upsell rules are owned at region and read at venue (decided 28 September, audit R183); set from the caller's region scope on create.\n"},"name":{"type":"string","maxLength":200},"placement":{"$ref":"#/components/schemas/UpsellPlacement"},"triggerVariantIds":{"type":"array","items":{"type":"string","format":"uuid"}},"triggerCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"suggestedVariantIds":{"type":"array","minItems":1,"items":{"type":"string","format":"uuid"}},"suggestedBundleId":{"type":"string","format":"uuid","nullable":true},"channels":{"type":"array","description":"Empty applies to every channel. Restriction is opt-in — a rule that fires on the website but not at a counter is a guest experience inconsistency.\n","items":{"type":"string"}},"priority":{"type":"integer","default":0},"maxSuggestions":{"type":"integer","default":3},"isActive":{"type":"boolean"}}},
"VenuePath": {"type":"object","x-ticvai-persistence":"venuemap.path","description":"19.2.56. **The navigation graph.** The map supplies it; routing over it is a client concern, because a phone with the map cached routes offline and a server round-trip per step does not.\n","required":["id","mapId","fromPointId","toPointId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes the path."},"fromPointId":{"type":"string","format":"uuid"},"toPointId":{"type":"string","format":"uuid"},"geometry":{"type":"string","nullable":true,"description":"The centreline this edge follows, as an encoded polyline. **A walkway in a drawing is a polygon and a route is a line down the middle of it**, so extraction thins the polygon to a centreline and splits it at every fork.\nNull where the path was drawn on screen as a straight connection, which is normal for a venue with no walkway layer.\n"},"distanceMetres":{"type":"number","nullable":true,"readOnly":true,"description":"Computed by the server from `geometry` and the georeference. **Along the centreline, not point to point.** A path that curves round a lake is longer than the distance between its ends, and a guest told 80 metres who walks 200 stops trusting the map.\nRequires a georeference for real units; without one, distances are in drawing units and routing still works because **only the ratios matter to a shortest path.**\n"},"isStepFree":{"type":"boolean","default":true,"description":"**The single most important attribute on this object.** A wheelchair user routed up a staircase has been failed by the map, not by the venue.\n"},"isIndoor":{"type":"boolean","default":false},"restrictedByPointId":{"type":"string","format":"uuid","nullable":true,"description":"**Where a path is one-way, it is because of a thing on it — not because of the path.** Removed `isOneWay` on 18 August: a pedestrian walkway has no direction, and the three cases that look one-way are all a gate or a queue.\nA turnstile is one-way and `access.AccessPoint.direction` already says so. A queue line is one-way and `queue` owns it. **Putting the restriction on the path duplicated both and would have drifted from them** — a gate reconfigured to bidirectional would leave a path still marked one-way, and nothing would have noticed.\nSet where a path passes through an access point. The router reads the direction from the point.\n"},"closedReason":{"type":"string","nullable":true,"readOnly":true,"description":"Set by `setPathClosure` during works or an incident, never by sending it here. **A closed path removes routes rather than hiding the path**, so a guest sees why rather than wondering where it went.\n"}}},
"VenueSettings": {"type":"object","x-ticvai-persistence":"platform.venue_settings","description":"**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setVenueSettings`."},"calendarDayStartHour":{"type":"integer","minimum":0,"maximum":23,"nullable":true,"default":6,"description":"**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"nullable":true,"readOnly":true,"description":"**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"},"supportHours":{"type":"object","description":"CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n","properties":{"mode":{"type":"string","enum":["alwaysOn","businessHours","custom","none"]},"timezone":{"type":"string","description":"IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"},"windows":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time the desk opens."},"to":{"type":"string","description":"Wall-clock time the desk closes."}}}},"outOfHoursMessage":{"type":"string","nullable":true}}},"quietHours":{"type":"object","nullable":true,"description":"**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n","properties":{"from":{"type":"string","description":"Wall-clock time sending stops","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time sending resumes","in the region's time zone.":null}}},"biometrics":{"type":"object","nullable":true,"description":"CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n","properties":{"isEnabled":{"type":"boolean","default":false,"description":"**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"},"dpiaReference":{"type":"string","nullable":true,"maxLength":200,"description":"**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"},"consentNoticeAcknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"},"faceTagPurgeMinutesAfterClose":{"type":"integer","nullable":true,"default":0,"description":"BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"}}},"segregatedAccess":{"type":"object","nullable":true,"description":"CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n","properties":{"isEnabled":{"type":"boolean","default":false},"appliesToAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"schedule":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"admits":{"type":"string","enum":["all","women","womenAndChildren","families","members"]}}}},"entitlementGated":{"type":"boolean","default":true,"readOnly":true,"description":"**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"},"genderVerification":{"type":"string","enum":["off","staffAssisted","deviceAssisted"],"default":"off","description":"`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"},"overrideRateAlertThreshold":{"type":"number","nullable":true,"description":"Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"}}},"alerting":{"type":"object","description":"CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n","properties":{"channel":{"type":"string","enum":["dashboardPanel","dashboardAndEmail","dashboardAndWhatsapp"],"default":"dashboardPanel"},"acknowledgementRequired":{"type":"boolean","default":true},"escalateAfterMinutes":{"type":"integer","nullable":true}}},"displayCurrencies":{"type":"array","nullable":true,"description":"**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"cartLeaseSeconds":{"type":"integer","nullable":true,"minimum":30,"maximum":3600,"default":900,"description":"**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"},"cartHoldExtensionMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":5,"description":"How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."},"cartMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."},"resaleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":168,"default":24,"description":"Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."},"exchangeCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."},"rescheduleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."},"reservationMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."},"shiftVarianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"},"catalogue":{"type":"object","nullable":true,"properties":{"maxVariantsPerProduct":{"type":"integer","nullable":true,"minimum":1,"maximum":2000,"default":200,"description":"Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."},"waitlistOfferHoldMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":1440,"default":30,"description":"How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":10,"description":"A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationCount":{"type":"integer","nullable":true,"minimum":1,"default":50,"description":"A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."}}},"inventory":{"type":"object","nullable":true,"properties":{"overReceiptTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":5,"description":"Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."},"countVarianceTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":2,"description":"Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."},"countVarianceApprovalAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"}}},"seating":{"type":"object","nullable":true,"properties":{"seatHoldExtensionSeconds":{"type":"integer","nullable":true,"minimum":60,"maximum":1800,"default":300,"description":"What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."},"seatHoldMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":2,"description":"How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."},"maxSeatsPerGuestOrder":{"type":"integer","nullable":true,"minimum":1,"maximum":50,"default":10,"description":"**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"}}},"promotions":{"type":"object","nullable":true,"properties":{"maxDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":30,"description":"The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."},"nearZeroLinePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"}}},"fnb":{"type":"object","nullable":true,"properties":{"recallWindowMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":60,"default":10,"description":"Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."},"compEscalationAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"},"foodSafetyLeadPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"}}},"queue":{"type":"object","nullable":true,"properties":{"crossQueueLimit":{"type":"integer","nullable":true,"minimum":1,"maximum":10,"default":2,"description":"Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."}}},"reporting":{"type":"object","nullable":true,"properties":{"inlineRunRowLimit":{"type":"integer","nullable":true,"minimum":1000,"maximum":100000,"default":5000,"description":"Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."},"dashboardRefreshBudgetPerMinute":{"type":"integer","nullable":true,"minimum":1,"default":24,"description":"Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."}}},"marketing":{"type":"object","nullable":true,"properties":{"attributionWindowDays":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":7,"description":"Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."}}},"identity":{"type":"object","nullable":true,"properties":{"guestOtpMaxAttempts":{"type":"integer","nullable":true,"minimum":3,"maximum":10,"default":5,"description":"Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"},"guestTwoStep":{"type":"object","nullable":true,"description":"**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."},"stepUpActions":{"type":"array","uniqueItems":true,"description":"The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n","items":{"type":"string","enum":["changeContactDetails","changePassword","managePaymentMethods","transferTickets","deleteAccount"]},"default":["changeContactDetails","changePassword","managePaymentMethods","deleteAccount"]}}}}}}},
"Workstation": {"x-ticvai-persistence":"platform.workstation","type":"object","required":["id","code","name","venueId","regionId","scopePath","saleBoard","currency","currencyScale","timeZone"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"saleBoard":{"type":"object","description":"Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. What the operator may then DO within it is governed by their permissions.\n","required":["id","kind"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SaleBoardKind"},"name":{"type":"string"}}},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point.\n"},"devices":{"type":"array","items":{"$ref":"#/components/schemas/DeviceBinding"}},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"timeZone":{"type":"string"},"deploymentProfile":{"$ref":"#/components/schemas/DeploymentProfile"},"edgeNodeId":{"type":"string","format":"uuid","nullable":true,"description":"Present when `deploymentProfile` is `venueEdge`."},"healthScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"readOnly":true,"description":"Board 1 of the client's POS set. **A number a manager can sort by** — the package held `lastHeartbeatAt` and a heartbeat timestamp is not a score.\nThe client's board shows 1,248 workstations at 96% healthy, and **the value of that figure is that it ranks**: a fleet dashboard exists so somebody can open the worst one first.\n**Derived from its devices, its heartbeat age, its firmware currency and its error rate.** Read-only, because a workstation that could set its own score would.\n**The formula, proposed, client to correct (audit R096 (2)):** score = 40% device online share (the share of its devices reporting online) + 25% heartbeat freshness (100 at one minute old or less, 0 at 15 minutes or more, linear between) + 20% firmware and profile currency (100 on the latest, 50 one version behind, 0 older) + 15% error rate (100 at 0 errors an hour, 0 at 10 or more, linear between), rounded to a whole number. **Below 80 is a warning and below 60 a failure.**\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"description":"Which profile this workstation runs, and at which version. **The client's board shows a fleet split four ways — 72% latest, 18.8% one behind, 6.1% outdated** — and the package had a firmware version field and no profile.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks*.\n"},"catalogueState":{"$ref":"#/components/schemas/CatalogueState"},"offlineCapable":{"type":"boolean","description":"Derived from `deploymentProfile`. False only for `thin`. Under local-first, catalogue READS are always local on transactional surfaces; this flag governs whether WRITES can be queued.\n"},"isActive":{"type":"boolean"}}}
}
```
