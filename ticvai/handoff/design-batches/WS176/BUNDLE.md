# WS176 — Seat Management Venue Mapping Reference v1.0 board 12

**10 screens · 31 operations · 30 schemas · 13 permissions**

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

- **Every control that can be refused must be gated.** 13 permissions apply here:
  `APPROVAL_CONFIGURE, CAPACITY_CONFIGURE, DEVICE_VIEW, PERMISSION_GRANT, PERMISSION_MANAGE, PERMISSION_VIEW, PRODUCT_VIEW, REGION_CONFIGURE, SCOPE_VIEW, SHIFT_OPEN, TENANT_CONFIGURE, TENANT_VIEW`…. A control nobody can use must say so,
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
| `BO-1061` | Platform Command Center | B–D | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-1062` | Tenant & Brand Context | B–D | 72 | 12 | 6 | 28 | 0 | 6 | — | notStarted (—) |
| `BO-1063` | Venue-Specific Configuration | B–D | 1 | 0 | 6 | 17 | 0 | 0 | — | notStarted (—) |
| `BO-1064` | Naming, Numbering & Localization | B–D | 0 | 0 | 6 | 6 | 0 | 0 | — | notStarted (—) |
| `BO-1065` | Currency, Timezone & Channels | B–D | 0 | 0 | 6 | 0 | 0 | 4 | — | notStarted (—) |
| `BO-1066` | Roles, Permissions & Masking | B–D | 0 | 0 | 6 | 12 | 1 | 5 | — | notStarted (—) |
| `BO-1067` | Seat Approval Workflows | B–D | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1068` | Lifecycle & Environment Promotion | B–D | 0 | 0 | 6 | 0 | 0 | 2 | — | notStarted (—) |
| `BO-1069` | Platform Health & Observability | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1070` | Setup, Clone & Inheritance | B–D | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-1061, BO-1062, BO-1064, BO-1065, BO-1066, BO-1067, BO-1068, BO-1069, BO-1070 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1061` Platform Command Center

**Provide a platform-wide view of tenant, venue and environment readiness. Show tenants, brands, venues, environments, active users, pending approvals, deployments and failed jobs. Display service status, API health, capacity, incidents and configuration exceptions. Restrict cross-tenant visibility to authorized platform roles and preserve every context switch. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW`, `VENUE_MAP_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/platform-command-center-bo-1061` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Draft · Validated · Published · Archived | `listSeatMaps` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listVenueMaps` (onLoad, Venues and their maps); `listSeatMaps` (onLoad, Seat maps across them)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-1062` Tenant & Brand Context: *Tenant & Brand Context*
- → `BO-1063` Venue-Specific Configuration: *Venue-Specific Configuration*
- → `BO-1064` Naming, Numbering & Localization: *Naming, Numbering & Localization*
- → `BO-1065` Currency, Timezone & Channels: *Currency, Timezone & Channels*
- → `BO-1066` Roles, Permissions & Masking: *Roles, Permissions & Masking*
- → `BO-1067` Seat Approval Workflows: *Seat Approval Workflows*
- → `BO-1068` Lifecycle & Environment Promotion: *Lifecycle & Environment Promotion*
- → `BO-1069` Platform Health & Observability: *Platform Health & Observability*
- → `BO-1070` Setup, Clone & Inheritance: *Setup, Clone & Inheritance*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The platform list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the platform untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No platform yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the platform are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listVenueMaps` → `VENUE_MAP_VIEW` (read) · staff
- `listSeatMaps` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.13.3 | Seat Management APIs | Seat Management & Venue Mapping | CONTRACTED | `listSeatMaps` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1061` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1061`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 1: Opens Platform Command Center → Provide a platform-wide view of tenant, venue and environment readiness. Show tenants, brands, venues, environments, active users, pending approvals, deployments and failed jobs. Display service …
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F285 branch at step 1 (expected): when Nothing has been set up on Platform Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F285 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1061?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-1062`, `BO-1063`, `BO-1064`, `BO-1065`, `BO-1066`, `BO-1067`, `BO-1068`, `BO-1069`, `BO-1070`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`, `VENUE_MAP_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1062` Tenant & Brand Context

**Configure the hierarchy and isolation boundary for seat management. Maintain tenant, legal entity, brand, region, venue ownership, status and data-residency classification. Configure tenant isolation, encryption context, export restriction, cross-brand sharing and support-access policy. Show inherited platform settings and the venues, users, integrations and environments within each context. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW`, `TENANT_CONFIGURE`, `TENANT_VIEW` (2 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `orgUnitId` (navigation) |
| Route | `/access-venue/tenant-brand-context-bo-1062` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Form: Save venue setting defaults** (modal, opened by *Save venue setting defaults*; *Save venue setting defaults* calls `setVenueSettingsDefaults`, *Cancel* sends nothing)

**Collects what `setVenueSettingsDefaults` sends before it is called.** The body is a `VenueSettings`: every field is the default a venue inherits where it leaves the setting null (decided 28 September, audit R094). Tenant scope; needs `TENANT_CONFIGURE`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Calendar day start hour `calendarDayStartHour` | stepper or slider | optional | 6 | min 0; max 23 | — | Where the venue's calendar day starts (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in … | `setVenueSettingsDefaults` body |
| Support hours `supportHours` | group | optional | — | — | — | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. | `setVenueSettingsDefaults` body |
| Mode `supportHours.mode` | radio group | optional | — | Always on · Business hours · Custom · None | — | — | `setVenueSettingsDefaults` body |
| Timezone `supportHours.timezone` | text field | optional | — | — | — | IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract. | `setVenueSettingsDefaults` body |
| Windows `supportHours.windows` | repeatable rows | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Day `supportHours.windows[].day` | select | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setVenueSettingsDefaults` body |
| From `supportHours.windows[].from` | text field | optional | — | — | — | Wall-clock time the desk opens. | `setVenueSettingsDefaults` body |
| To `supportHours.windows[].to` | text field | optional | — | — | — | Wall-clock time the desk closes. | `setVenueSettingsDefaults` body |
| Out of hours message `supportHours.outOfHoursMessage` | text field | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Quiet hours `quietHours` | group | optional | — | — | — | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. | `setVenueSettingsDefaults` body |
| From `quietHours.from` | text field | optional | — | — | — | Wall-clock time sending stops | `setVenueSettingsDefaults` body |
| To `quietHours.to` | text field | optional | — | — | — | Wall-clock time sending resumes | `setVenueSettingsDefaults` body |
| Biometrics `biometrics` | group | optional | — | — | — | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. | `setVenueSettingsDefaults` body |
| Is enabled `biometrics.isEnabled` | toggle | optional | off | Off by default, and turning it on is refused without the two fields below. | — | Off by default, and turning it on is refused without the two fields below. `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — a DPIA nobody can … | `setVenueSettingsDefaults` body |
| Dpia reference `biometrics.dpiaReference` | text field | optional | — | max length 200 | — | The venue's own reference for its Article 21 assessment. The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is … | `setVenueSettingsDefaults` body |
| Consent notice acknowledged at `biometrics.consentNoticeAcknowledgedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When somebody confirmed the consent forms are in place at the point of capture. A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice … | `setVenueSettingsDefaults` body |
| Face tag purge minutes after close `biometrics.faceTagPurgeMinutesAfterClose` | number field (minutes) | optional | 0 | — | — | BL-106. How long a same-visit Face Tag survives past the close of the operating day, and zero is the default because that is what 3.2.44 describes. | `setVenueSettingsDefaults` body |
| Segregated access `segregatedAccess` | group | optional | — | — | — | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a prayer-time closure. | `setVenueSettingsDefaults` body |
| Is enabled `segregatedAccess.isEnabled` | toggle | optional | off | — | — | — | `setVenueSettingsDefaults` body |
| Applies to access points `segregatedAccess.appliesToAccessPointIds` | multi-picker: choose applies to access points | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Schedule `segregatedAccess.schedule` | repeatable rows | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Day `segregatedAccess.schedule[].day` | select | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setVenueSettingsDefaults` body |
| From `segregatedAccess.schedule[].from` | text field | optional | — | — | — | Wall-clock time | `setVenueSettingsDefaults` body |
| To `segregatedAccess.schedule[].to` | text field | optional | — | — | — | Wall-clock time | `setVenueSettingsDefaults` body |
| Admits `segregatedAccess.schedule[].admits` | radio group | optional | — | All · Women · Women and children · Families · Members | — | — | `setVenueSettingsDefaults` body |
| Gender verification `segregatedAccess.genderVerification` | segmented control | optional | Off | Off · Staff assisted · Device assisted; Available only where the driver reports the capability, and the result is advisory to the steward rather than decisive at the turnstile (3. | — | `off` — the entitlement decides and a steward handles exceptions. The default, and what is contracted. | `setVenueSettingsDefaults` body |
| Override rate alert threshold `segregatedAccess.overrideRateAlertThreshold` | number field | optional | — | — | — | Where `deviceAssisted` is on. An override rate near zero means the steward has stopped deciding, and that is the number that says whether the human safeguard is working or … | `setVenueSettingsDefaults` body |
| Alerting `alerting` | group | optional | — | The panel is the default and email or WhatsApp only where the matrix names them — an operational alert that arrives by email is an alert nobody sees in time. | — | CF-134. On-platform notification, marked as read. | `setVenueSettingsDefaults` body |
| Channel `alerting.channel` | segmented control | optional | Dashboard panel | Dashboard panel · Dashboard and email · Dashboard and whatsapp | — | — | `setVenueSettingsDefaults` body |
| Acknowledgement required `alerting.acknowledgementRequired` | toggle | optional | on | — | — | — | `setVenueSettingsDefaults` body |
| Escalate after minutes `alerting.escalateAfterMinutes` | number field (minutes) | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Display currencies `displayCurrencies` | list of values (chips) | optional | — | A code the region has no rate for is refused `400`. | — | Which currencies this venue shows guests (decided 28 September, audit R120 (a)). | `setVenueSettingsDefaults` body |
| Cart lease seconds `cartLeaseSeconds` | number field (seconds) | optional | 900 | min 30; max 3600 | — | How long a cart holds capacity (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. | `setVenueSettingsDefaults` body |
| Cart hold extension minutes `cartHoldExtensionMinutes` | stepper or slider (minutes) | optional | 5 | min 1; max 30 | — | How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094). | `setVenueSettingsDefaults` body |
| Cart max extensions `cartMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). | `setVenueSettingsDefaults` body |
| Resale cutoff hours `resaleCutoffHours` | number field (hours) | optional | 24 | min 0; max 168 | — | Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). | `setVenueSettingsDefaults` body |
| Exchange cutoff hours `exchangeCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). | `setVenueSettingsDefaults` body |
| Reschedule cutoff hours `rescheduleCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). | `setVenueSettingsDefaults` body |
| Reservation max extensions `reservationMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094). | `setVenueSettingsDefaults` body |
| Shift variance threshold `shiftVarianceThreshold` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. | `setVenueSettingsDefaults` body |
| Catalogue `catalogue` | group | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Max variants per product `catalogue.maxVariantsPerProduct` | number field | optional | 200 | min 1; max 2000 | — | Variants one product may generate from its attributes (`setProductAttributes` refuses above it). | `setVenueSettingsDefaults` body |
| Waitlist offer hold minutes `catalogue.waitlistOfferHoldMinutes` | number field (minutes) | optional | 30 | min 1; max 1440 | — | How long a waitlist offer holds the released capacity for the guest it was offered to. | `setVenueSettingsDefaults` body |
| Bulk price change escalation percent `catalogue.bulkPriceChangeEscalationPercent` | stepper or slider | optional | 10 | min 0; max 100; A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). | — | A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). | `setVenueSettingsDefaults` body |
| Bulk price change escalation count `catalogue.bulkPriceChangeEscalationCount` | number field | optional | 50 | min 1; A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). | — | A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). | `setVenueSettingsDefaults` body |
| … 27 more | | | | | | the rest are in `schemas.json` | `setVenueSettingsDefaults` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Venue setting defaults** (detail panel, from `getVenueSettingsDefaults`): **The inherited settings** — the tenant's default for every venue setting, which a venue inherits wherever it leaves a limit null (decided 28 September, audit R094).

| Shows | Format | Notes |
|---|---|---|
| Support hours | grouped details | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. |
| Quiet hours | grouped details | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. |
| Alerting | grouped details | CF-134. On-platform notification, marked as read. |
| Display currencies | list or chips (count when long) | Which currencies this venue shows guests (decided 28 September, audit R120 (a)). |
| Shift variance threshold | AED 1,234.50 | Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. |
| Catalogue | grouped details | — |
| Inventory | grouped details | — |
| Seating | grouped details | — |
| Promotions | grouped details | — |
| Fnb | grouped details | — |
| Queue | grouped details | — |
| Reporting | grouped details | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save venue setting defaults (secondary button) | `setVenueSettingsDefaults` PUT `/venue-settings-defaults` | VenueSettings | VenueSettings | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | gated `TENANT_CONFIGURE`; opens modal first |

**Data it reads**: `getVenueSettingsDefaults` (onLoad, The tenant's default for every venue setting — the …)

**Where the user goes next**

- → `BO-1061` Platform Command Center: *Back to Platform Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tenant brand context list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tenant brand context untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tenant brand context yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the tenant brand context are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `getOrgUnit` → `SCOPE_VIEW` (read) · staff
- `getVenueSettingsDefaults` → `TENANT_VIEW` (read) · staff
- `setVenueSettingsDefaults` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

28 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.1.14 | The system shall isolate users, permissions, configurations, and data between tenants. Users shall only access data belonging to their assigned tenant unless explicitly authorized. | F&B POS | CONTRACTED | `getOrgUnit` |
| 7.1.53 | Allow separate authorization policies for each tenant in a multi-tenant environment without impacting other tenants. | F&B POS | CONTRACTED | `getOrgUnit` |
| 7.3.1 | The sales system shall be able to manage the data transactions for Multi Tenants Sites | F&B POS | CONTRACTED | `getOrgUnit` |
| 13.1.46 | Multi-Tenant API Access - System shall support tenant-specific API access. | Developer & API Management | CONTRACTED | `getOrgUnit` |
| 13.2.11 | Data Isolation - Sandbox data shall be isolated from production. | Developer & API Management | CONTRACTED | `getOrgUnit` |
| 15.5.1 | Tenant-Specific Inventory - System shall support tenant-specific inventory. | Inventory Management | CONTRACTED | `getOrgUnit` |
| 15.5.2 | Venue-Specific Inventory - System shall support venue-specific inventory. | Inventory Management | CONTRACTED | `getOrgUnit` |
| 16.9.51 | Multi-Tenant Device Management - System shall support tenant-specific device management. | Device Management | CONTRACTED | `getOrgUnit` |
| 16.9.52 | Venue-Specific Device Management - System shall support venue-specific device management. | Device Management | CONTRACTED | `getOrgUnit` |
| 21.13.1 | Multi-Tenant Support | Seat Management & Venue Mapping | CONTRACTED | `getOrgUnit` |
| 21.13.2 | Venue-Specific Configuration | Seat Management & Venue Mapping | CONTRACTED | `getOrgUnit` |
| 3.2.45 | Face Pass and Face Tag should support automatic gender recognition and reject customers who do not match the designated gender segment. | Admission and Access | CONTRACTED_PARTIAL | data `VenueSettings` |
| … 16 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1062` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1062`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 2: Works in Tenant & Brand Context → Configure the hierarchy and isolation boundary for seat management. Maintain tenant, legal entity, brand, region, venue ownership, status and data-residency classification. Configure tenant …

#### Acceptance for the design

- [ ] Every input above is drawn (72), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1062?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save venue setting defaults.
- [ ] Every transition is wired: `BO-1061`.
- [ ] Every gated control is gated: `SCOPE_VIEW`, `TENANT_CONFIGURE`, `TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1063` Venue-Specific Configuration

**Set local defaults without creating separate seat systems. Configure default map, lock/hold duration, naming, accessibility, sales channels, approvals and publishing policy. Map local entrances, devices, price/seat categories, operating calendars and venue-specific exceptions. Display which settings inherit from platform/tenant/brand and require justification for permitted overrides. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Configuration Scope of Work / Version 1.0 50 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `TENANT_CONFIGURE`, `TENANT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `venueId` (session) |
| Route | `/access-venue/venue-specific-configuration-bo-1063` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Seats per guest booking | stepper or slider | optional | 10 | min 1; max 50 | — | **How many seats one guest may take in one booking on Guest Web and the Guest App** (decided 29 September, rev 3 REV3-7). Default 10, from 1 to 50; left empty, the venue inherits the tenant default. … | `VenueSettings.seating.maxSeatsPerGuestOrder` |

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only. **Shows the configured limits** (decided 28 September, audit R094); a limit the venue has not set is null and shows the tenant default it inherits.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save venue settings (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getVenueSettings` (onLoad, Venue configuration)

**Where the user goes next**

- → `BO-1061` Platform Command Center: *Back to Platform Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue-specific list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue-specific untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue-specific yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the venue-specific are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 An enable the venue cannot evidence. Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender … |

#### Permissions

- `getVenueSettings` → `TENANT_VIEW` (read) · staff
- `setVenueSettings` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.45 | Face Pass and Face Tag should support automatic gender recognition and reject customers who do not match the designated gender segment. | Admission and Access | CONTRACTED_PARTIAL | data `VenueSettings` |
| 3.2.46 | Face Pass shouldt restrict male guests attempting to enter during Friday Ladies Night, which needs to be validated with rule-based facial recognition validation. | Admission and Access | CONTRACTED | data `VenueSettings` |
| 8.9.3 | System shall display queue lengths, estimated wait times, queue utilization, queue alerts, and queue prediction metrics. | Unified Operations Dashboard | CONTRACTED | data `VenueSettings` |
| 11.1.15 | Approval Breach Alerts - System shall notify users when approval SLA thresholds are exceeded. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.17 | Approval Notifications - System shall notify approvers when new approval requests are assigned. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.18 | Approval Reminder Notifications - System shall send reminder notifications for pending approvals. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.19 | Approval Outcome Notifications - System shall notify requestors when approvals are approved, rejected or escalated. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 15.1.32 | Overstock Alerts - System shall generate overstock alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 15.1.33 | Stock Shortage Alerts - System shall generate stock shortage alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 15.1.34 | Expiry Alerts - System shall generate expiry alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 16.4.23 | Device Alerts - System shall generate device alerts. | Device Management | CONTRACTED | data `VenueSettings` |
| 16.9.58 | Device Incident Management - System shall support device incident management. | Device Management | CONTRACTED | data `VenueSettings` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1063` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1063`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 4: Works in Venue-Specific Configuration → Set local defaults without creating separate seat systems. Configure default map, lock/hold duration, naming, accessibility, sales channels, approvals and publishing policy. Map local entrances …

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1063?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save venue settings, Cancel.
- [ ] Every transition is wired: `BO-1061`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`, `TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1064` Naming, Numbering & Localization

**Control how seat entities and values appear in each venue and language. Configure venue/section/row/seat code formats, numbering direction, padding, prefixes and reserved values. Maintain translated labels, supported languages, text direction, pluralization and fallback language. Validate uniqueness and preview labels on map, ticket, cart, POS, access device and report. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `regionId` (navigation), `seatMapId` (navigation) |
| Route | `/access-venue/naming-numbering-localization-bo-1064` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save seats (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-1061` Platform Command Center: *Back to Platform Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The naming numbering localization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the naming numbering localization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No naming numbering localization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the naming numbering localization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Map is published and the change is structural |

#### Permissions

- `updateSeats` → `CAPACITY_CONFIGURE` (configure) · staff
- `getRegionSettings` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.4.30 | Bulk Configuration and Updates AI can: Apply seat categories to thousands of seats simultaneously. Update pricing zones across multiple venues. Clone and modify existing seat maps. Generate … | Ticketing Catalogue | CONTRACTED | `updateSeats` |
| 21.1.1 | Drag & Drop Venue Builder | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |
| 21.1.2 | Section Builder | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |
| 21.1.3 | Row Builder | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |
| 21.1.4 | Seat Builder | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |
| 21.2.15 | Manual Adjustment Layer | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1064` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1064`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 6: Works in Naming, Numbering & Localization → Control how seat entities and values appear in each venue and language. Configure venue/section/row/seat code formats, numbering direction, padding, prefixes and reserved values. Maintain translated …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1064?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save seats, Cancel.
- [ ] Every transition is wired: `BO-1061`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1065` Currency, Timezone & Channels

**Configure regional display and channel availability. Set currency, rounding, date/time/number formats, timezone, week start and daylight-saving behavior. Enable web, mobile, POS, box office, call center, B2B, partner API and marketplace channels per venue. Define locale defaults and fail-safe behavior when a channel or currency is unavailable. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REGION_CONFIGURE`, `SHIFT_OPEN` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `regionId` (navigation) |
| Route | `/access-venue/currency-timezone-channels-bo-1065` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Include inactive | toggle | on | — | `listDenominations` ?includeInactive |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save region settings (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listDenominations` (onLoad, The notes and coins tills count)

**Where the user goes next**

- → `BO-1061` Platform Command Center: *Back to Platform Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The currency timezone channels list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the currency timezone channels untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No currency timezone channels yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the currency timezone channels are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Currency or scale change rejected because transactions exist in this region.; 422 A zero or negative value, or two entries with the same value and kind (problem type `denomination-invalid`). |

#### Permissions

- `listDenominations` → `SHIFT_OPEN` (operate) · staff
- `setDenominations` → `REGION_CONFIGURE` (configure) · staff
- `updateRegionSettings` → `REGION_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A43** Design multi-currency display to support both manual FX-rate entry (with configurable margin) and an optional real-time third-party FX-rate API; confirm which payment gateway(s) support Dynamic Currency Conversion (DCC) *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'multi-currency')*
- **A44** Add a foreign-currency collection report (transactions collected broken down by foreign currency) to the Finance reporting suite *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'foreign currency')*
- **C23** Confirm foreign-currency display approach (manual FX-rate entry with margin vs. live third-party FX-rate API) and confirm the payment gateway that will support Dynamic Currency Conversion *(Qossai / Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'fx-rate')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'multi-currency')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1065` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1065`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 8: Works in Currency, Timezone & Channels → Configure regional display and channel availability. Set currency, rounding, date/time/number formats, timezone, week start and daylight-saving behavior. Enable web, mobile, POS, box office, call …
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1065?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save region settings, Cancel.
- [ ] Every transition is wired: `BO-1061`.
- [ ] Every gated control is gated: `REGION_CONFIGURE`, `SHIFT_OPEN`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1066` Roles, Permissions & Masking

**Enforce least-privilege access to seat administration and operational data. Configure RBAC/PBAC for maps, layouts, inventory, locks, holds, pricing, reports, integrations and audit. Apply venue/region scope, field masking, temporary/delegated access, segregation of duties and emergency override. Preview effective access for a user/context and log sensitive read, export and administrative actions. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PERMISSION_GRANT`, `PERMISSION_MANAGE`, `PERMISSION_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `policyId` (navigation), `campaignId` (navigation), `itemId` (navigation) |
| Route | `/access-venue/roles-permissions-masking-bo-1066` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Draft · Pending approval · Active · Suspended · Retired | `listAuthorisationPolicies` ?status |
| Scope path | text field | — | — | `listAuthorisationPolicies` ?scopePath |
| Principal | picker: choose a principal | — | — | `listPermissionFindings` ?principalId |
| Role | picker: choose a role | — | — | `listPermissionFindings` ?roleId |
| Scope path | text field | — | — | `listPermissionFindings` ?scopePath |
| Kind | segmented control | — | Excessive · Missing · Conflicting | `listPermissionFindings` ?kind |
| Lookback days | number field (days) | 90 | min 7; max 365 | `listPermissionFindings` ?lookbackDays |
| Denied threshold | number field | 3 | min 1 | `listPermissionFindings` ?deniedThreshold |
| Draft policy | picker: choose a draft policy | — | — | `listPermissionFindings` ?draftPolicyId |
| Status | segmented control | — | Open · Completed · Expired | `listAccessReviewCampaigns` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create access policy (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listAuthorisationPolicies` (onLoad, Who may see and change what); `listPermissionFindings` (onLoad, Excessive, missing and conflicting permissions, or those a …); `listAccessReviewCampaigns` (onLoad, Access review campaigns and progress)

**Where the user goes next**

- → `BO-1061` Platform Command Center: *Back to Platform Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The roles permissions masking list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the roles permissions masking untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No roles permissions masking yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the roles permissions masking are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 400 `revoke` without a `reason`, or `certify` against a `revoke` recommendation without one.; 409 Already decided, or the campaign is no longer `open` (`campaign-closed`).; 409 The target version was never approved, is the current version, or the policy is retired |

#### Permissions

- `listAuthorisationPolicies` → `PERMISSION_VIEW` (read) · staff
- `createAuthorisationPolicy` → `PERMISSION_MANAGE` (configure) · staff
- `simulateAuthorisationPolicy` → `PERMISSION_VIEW` (read) · staff
- `updateAuthorisationPolicy` → `PERMISSION_MANAGE` (configure) · staff
- `setAuthorisationPolicyState` → `PERMISSION_MANAGE` (configure) · staff
- `createEmergencyAccessOverride` → `PERMISSION_MANAGE` (configure) · staff
- `listAuthorisationPolicyHistory` → `PERMISSION_VIEW` (read) · staff
- `restoreAuthorisationPolicyVersion` → `PERMISSION_MANAGE` (configure) · staff
- `listAuthorisationPolicyEffectiveness` → `PERMISSION_VIEW` (read) · staff
- `listPermissionFindings` → `PERMISSION_VIEW` (read) · staff
- `listAccessReviewCampaigns` → `PERMISSION_VIEW` (read) · staff
- `createAccessReviewCampaign` → `PERMISSION_MANAGE` (configure) · staff
- `listAccessReviewItems` → `PERMISSION_VIEW` (read) · staff
- `decideAccessReviewItem` → `PERMISSION_GRANT` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.1 | Allows permissions to be granted dynamically based on attributes and context rather than fixed roles only. | Admission and Access | CONTRACTED | `createAuthorisationPolicy` |
| 3.3.5 | Dynamic Rule Engine Administrators shall configure access policies without software development. | Admission and Access | CONTRACTED | `createAuthorisationPolicy` |
| 7.1.44 | Provide a no-code visual interface for building access policies using conditions, rules, logic operators, approval requirements and reusable components. | F&B POS | CONTRACTED | `createAuthorisationPolicy` |
| 3.3.25 | Policy Testing - System shall support simulation and testing of policies prior to deployment. | Admission and Access | CONTRACTED | `simulateAuthorisationPolicy` |
| 3.3.24 | Policy Versioning - System shall maintain versions of access policies. | Admission and Access | CONTRACTED | `updateAuthorisationPolicy` |
| 3.3.26 | Policy Approval Workflow - System shall support approval workflows for policy changes. | Admission and Access | CONTRACTED | `setAuthorisationPolicyState` |
| 3.3.6 | Emergency Override Authorized users may temporarily bypass restrictions with full audit logging | Admission and Access | CONTRACTED | `createEmergencyAccessOverride` |
| 7.1.40 | Allow supervisors to override access restrictions during emergencies. Require justification, approval workflow (optional), timestamp recording, audit logging and override expiration. | F&B POS | CONTRACTED | `createEmergencyAccessOverride` |
| 3.3.39 | Policy Change History - System shall maintain historical versions of policy changes. | Admission and Access | CONTRACTED | `listAuthorisationPolicyHistory` |
| 7.1.46 | Maintain historical versions of access policies, support comparison between versions and allow rollback to previous approved versions. | F&B POS | CONTRACTED | `restoreAuthorisationPolicyVersion` |
| 7.1.47 | Provide a sandbox environment to test authorization policies before deployment and identify conflicts, missing permissions and excessive permissions. | F&B POS | CONTRACTED | `listPermissionFindings` |
| 7.1.56 | Provide AI recommendations for role assignments, permission optimization, risk reduction, user provisioning and periodic access reviews. | F&B POS | CONTRACTED | `createAccessReviewCampaign` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Allam: add a "roles comparison" view letting an admin compare two roles side by side (e.g. confirm a cashier role lacks the refund/void permissions a supervisor role has). *(agreed · MoM 7 Aug 2026, 4. Roles & User Management · DI-153)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S2** Role-based access control: role and permission matrix *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'permission matrix')*
- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'rbac')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A97** Document the RBAC role-permission matrix (edit/view · view-only · hidden, per role per module, sub-permissions, default templates) *(Chinmay Parab · High · Ongoing → 30 Sep: Closed, Rolled into S2 · 20 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A130** Enforce venue-level admission capacity as superseding event capacity, with a blocking validation and an RBAC-gated override *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 25 Aug 2026 · workshop tracker · keyword 'rbac')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1066` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1066`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 10: Works in Roles, Permissions & Masking → Enforce least-privilege access to seat administration and operational data. Configure RBAC/PBAC for maps, layouts, inventory, locks, holds, pricing, reports, integrations and audit. Apply …
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1066?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create access policy, Cancel.
- [ ] Every transition is wired: `BO-1061`.
- [ ] Every gated control is gated: `PERMISSION_GRANT`, `PERMISSION_MANAGE`, `PERMISSION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1067` Seat Approval Workflows

**Configure governance paths for high-impact seat changes. Define workflow by map/layout, capacity, seat kill, hold, accessibility, pricing, integration and override change type. Set stages, approver roles, thresholds, quorum, SLA, escalation, delegation, comments and evidence. Prevent requester self-approval where segregation rules apply and preserve decision history. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 51**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/seat-approval-workflows-bo-1067` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save visual workflow (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-1061` Platform Command Center: *Back to Platform Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The seat approval workflows list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the seat approval workflows untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No seat approval workflows yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the seat approval workflows are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setVisualWorkflow` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1067` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1067`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 12: Works in Seat Approval Workflows → Configure governance paths for high-impact seat changes. Define workflow by map/layout, capacity, seat kill, hold, accessibility, pricing, integration and override change type. Set stages, approver …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1067?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save visual workflow, Cancel.
- [ ] Every transition is wired: `BO-1061`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1068` Lifecycle & Environment Promotion

**Move approved configuration safely from draft to production. Provide Draft, Test, Staging and Production contexts with version, owner, status and dependency checks. Promote signed configuration packages through required gates, automated tests and approvals. Support comparison, rollback, failed-promotion recovery and prohibition of direct unapproved production edits. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `profileId` (navigation) |
| Route | `/access-venue/lifecycle-environment-promotion-bo-1068` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-1061` Platform Command Center: *Back to Platform Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The lifecycle environment promotion list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the lifecycle environment promotion untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No lifecycle environment promotion yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the lifecycle environment promotion are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The named version is not deployable — it is still a `draft`, or this profile has no such version. |

#### Permissions

- `deployConfigurationProfile` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1068` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1068`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 14: Works in Lifecycle & Environment Promotion → Move approved configuration safely from draft to production. Provide Draft, Test, Staging and Production contexts with version, owner, status and dependency checks. Promote signed configuration …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1068?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-1061`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1069` Platform Health & Observability

**Monitor the technical services that protect seat-state correctness. Show API latency/error, event lag, lock service, inventory service, cache, database, queue and webhook health. Configure SLOs, thresholds, alerts, correlation, incident ownership and capacity forecasts by tenant/venue. Drill from a metric to traces, logs and affected performances without exposing restricted tenant data. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `workstationId` (session) |
| Route | `/access-venue/platform-health-observability-bo-1069` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Data it reads**: `getWorkstationHealth` (onLoad, Platform health)

**Where the user goes next**

- → `BO-1061` Platform Command Center: *Back to Platform Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The platform health observability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the platform health observability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No platform health observability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the platform health observability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getWorkstationHealth` → `DEVICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1069` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1069`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 16: Works in Platform Health & Observability → Monitor the technical services that protect seat-state correctness. Show API latency/error, event lag, lock service, inventory service, cache, database, queue and webhook health. Configure SLOs …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1069?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1061`.
- [ ] Every gated control is gated: `DEVICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1070` Setup, Clone & Inheritance

**Accelerate onboarding while keeping configuration lineage visible. Guide setup of tenant, brand, venue, locale, map, categories, locks/holds, channels, workflows and integrations. Clone an authorized source venue or template and choose which settings, maps and rules to copy or inherit. Show inherited, overridden, missing and conflicting settings and validate completeness before activation. Enforce tenant isolation and environment separation at UI, API, data, cache, event and export layers; venue overrides cannot weaken mandatory platform security or compliance policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 52 Board 13 - Seat APIs, Webhooks & Audit Governance Figure 13. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work / Version 1.0 53**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `TENANT_CONFIGURE` (2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `seatMapId` (navigation) |
| Route | `/access-venue/setup-clone-inheritance-bo-1070` |

**Known gaps.** **Setup, Clone & Inheritance declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-1061` Platform Command Center: *Back to Platform Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The clone inheritance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the clone inheritance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No clone inheritance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the clone inheritance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `cloneSeatMap` → `CAPACITY_CONFIGURE` (configure) · staff
- `setConfigurationProfile` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.3.2 | Event-Specific Layouts | Seat Management & Venue Mapping | CONTRACTED | `cloneSeatMap` |
| 21.3.3 | Layout Cloning | Seat Management & Venue Mapping | CONTRACTED | `cloneSeatMap` |
| 21.3.7 | Multi-Performance Layouts | Seat Management & Venue Mapping | CONTRACTED | `cloneSeatMap` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1070` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS151 Seat Management Venue Mapping Reference v1.0 Board 12.dc.html#bo-1070`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 12
- Flow F285 *Seat Management Venue Mapping Reference v1.0 board 12: Platform Command Center*, step 18: Works in Setup, Clone & Inheritance → Accelerate onboarding while keeping configuration lineage visible. Guide setup of tenant, brand, venue, locale, map, categories, locks/holds, channels, workflows and integrations. Clone an authorized …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1070?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-1061`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `TENANT_CONFIGURE`.
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

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"cloneSeatMap": {"method":"POST","path":"/seat-maps/{seatMapId}/clone","contract":"seating","summary":"Clone a map, optionally into another venue","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SeatMap"},
"createAccessReviewCampaign": {"method":"POST","path":"/access-review-campaigns","contract":"identity","summary":"Start an access review, one item per grant in scope","permission":"PERMISSION_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"IdentityAccessReviewCampaign","responds":"IdentityAccessReviewCampaign"},
"createAuthorisationPolicy": {"method":"POST","path":"/authorisation-policies","contract":"identity","summary":"Write a policy without writing code","permission":"PERMISSION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AuthorisationPolicy","responds":"AuthorisationPolicy"},
"createEmergencyAccessOverride": {"method":"POST","path":"/access-overrides","contract":"identity","summary":"Bypass the policy, loudly","permission":"PERMISSION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"EmergencyAccessOverride"},
"decideAccessReviewItem": {"method":"POST","path":"/access-review-items/{itemId}/decision","contract":"identity","summary":"Certify a grant, or revoke it","permission":"PERMISSION_GRANT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"IdentityAccessReviewItem"},
"deployConfigurationProfile": {"method":"POST","path":"/configuration-profiles/{profileId}/deploy","contract":"tenancy","summary":"Push a version to a fleet, in stages","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ProfileDeployment","responds":null},
"getOrgUnit": {"method":"GET","path":"/org-units/{orgUnitId}","contract":"tenancy","summary":"Read a scope node","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"OrgUnit"},
"getRegionSettings": {"method":"GET","path":"/regions/{regionId}/settings","contract":"tenancy","summary":"Read region settings","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"RegionSettings"},
"getVenueSettings": {"method":"GET","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Operational settings for this venue","permission":"TENANT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VenueSettings"},
"getVenueSettingsDefaults": {"method":"GET","path":"/venue-settings-defaults","contract":"tenancy","summary":"The tenant's default for every venue setting","permission":"TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"VenueSettings"},
"getWorkstationHealth": {"method":"GET","path":"/workstations/{workstationId}/health","contract":"tenancy","summary":"A score a manager can sort by, and what is dragging it down","permission":"DEVICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":null},
"listAccessReviewCampaigns": {"method":"GET","path":"/access-review-campaigns","contract":"identity","summary":"Access review campaigns, open first","permission":"PERMISSION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAccessReviewItems": {"method":"GET","path":"/access-review-campaigns/{campaignId}/items","contract":"identity","summary":"The grants a campaign asks somebody to certify or revoke","permission":"PERMISSION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"assignedToMe","in":"query","required":null},{"name":"findingKind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAuthorisationPolicies": {"method":"GET","path":"/authorisation-policies","contract":"identity","summary":"Attribute-based authorisation policies","permission":"PERMISSION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"scopePath","in":"query","required":null}],"requestBody":null,"responds":"AuthorisationPolicy"},
"listAuthorisationPolicyEffectiveness": {"method":"GET","path":"/authorisation-policy-effectiveness","contract":"identity","summary":"How each software-permission policy has behaved over a period","permission":"PERMISSION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"policyId","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAuthorisationPolicyHistory": {"method":"GET","path":"/authorisation-policies/{policyId}/history","contract":"identity","summary":"Every version, who changed it and why","permission":"PERMISSION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"AuthorisationPolicyVersion"},
"listDenominations": {"method":"GET","path":"/denominations","contract":"shift","summary":"The notes and coins a till counts","permission":"SHIFT_OPEN","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"includeInactive","in":"query","required":null}],"requestBody":null,"responds":"Denomination"},
"listPermissionFindings": {"method":"GET","path":"/permission-findings","contract":"identity","summary":"Excessive, missing and conflicting permissions, per principal or role","permission":"PERMISSION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"principalId","in":"query","required":null},{"name":"roleId","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"lookbackDays","in":"query","required":null},{"name":"deniedThreshold","in":"query","required":null},{"name":"draftPolicyId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSeatMaps": {"method":"GET","path":"/seat-maps","contract":"seating","summary":"List seat maps","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVenueMaps": {"method":"GET","path":"/venue-maps","contract":"venue-map","summary":"Maps for this venue","permission":"VENUE_MAP_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VenueMap"},
"restoreAuthorisationPolicyVersion": {"method":"POST","path":"/authorisation-policies/{policyId}/restore","contract":"identity","summary":"Put a previously approved policy version back, as a new version","permission":"PERMISSION_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AuthorisationPolicy"},
"setAuthorisationPolicyState": {"method":"POST","path":"/authorisation-policies/{policyId}/state","contract":"identity","summary":"Submit, approve, activate or retire a policy","permission":"PERMISSION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AuthorisationPolicy"},
"setConfigurationProfile": {"method":"PUT","path":"/configuration-profiles","contract":"tenancy","summary":"What a class of workstation is configured to be","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ConfigurationProfile","responds":"ConfigurationProfile"},
"setDenominations": {"method":"PUT","path":"/denominations","contract":"shift","summary":"Set the notes and coins a region's tills count","permission":"REGION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetDenominationsRequest","responds":"Denomination"},
"setVenueSettings": {"method":"PUT","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Set support hours, quiet hours, segregated access and alerting","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VenueSettings","responds":"VenueSettings"},
"setVenueSettingsDefaults": {"method":"PUT","path":"/venue-settings-defaults","contract":"tenancy","summary":"Set the tenant's default for every venue setting","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VenueSettings","responds":"VenueSettings"},
"setVisualWorkflow": {"method":"PUT","path":"/visual-workflow","contract":"approvals","summary":"Visual Workflow Designer","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisualWorkflowDesignerInput","responds":"VisualWorkflowDesignerView"},
"simulateAuthorisationPolicy": {"method":"POST","path":"/authorisation-policies/simulate","contract":"identity","summary":"What this policy would decide, before it decides anything","permission":"PERMISSION_VIEW","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessDecision"},
"updateAuthorisationPolicy": {"method":"PUT","path":"/authorisation-policies/{policyId}","contract":"identity","summary":"Change a policy, as a new version","permission":"PERMISSION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AuthorisationPolicy","responds":"AuthorisationPolicy"},
"updateRegionSettings": {"method":"PUT","path":"/regions/{regionId}/settings","contract":"tenancy","summary":"Update region settings","permission":"REGION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RegionSettings","responds":"RegionSettings"},
"updateSeats": {"method":"PATCH","path":"/seat-maps/{seatMapId}/seats","contract":"seating","summary":"Bulk-amend seats","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"BulkUpdateSeatsRequest","responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessCondition": {"type":"object","description":"**One attribute, one operator, one value** — and the attribute names are an enum rather than free text, because a policy that reads `venu.type` silently never matches.\nThe enum is the matrix, row by row: user (3.3.7), employee (3.3.8), membership (3.3.9), accreditation (3.3.10), customer segment (3.3.11), resource classification (3.3.12), venue (3.3.13), attraction (3.3.14), device (3.3.15), day of week (3.3.16), season (3.3.17), event (3.3.18), capacity (3.3.19), occupancy (3.3.20), risk score (3.3.21), location (3.3.2) and time (3.3.3).\n","required":["attribute","operator"],"properties":{"attribute":{"type":"string","enum":["user.attribute","employee.attribute","employee.onShift","membership.tier","membership.status","accreditation.type","accreditation.status","customer.segment","resource.classification","venue.attribute","venue.id","attraction.attribute","device.kind","device.id","device.trusted","time.ofDay","time.dayOfWeek","time.season","time.withinOperatingHours","event.id","event.status","capacity.utilisationPercent","occupancy.level","risk.score","ticket.status","location.scopePath"]},"key":{"type":"string","nullable":true,"description":"For the `*.attribute` forms — which attribute, by code."},"operator":{"type":"string","enum":["equals","notEquals","in","notIn","greaterThan","lessThan","between","contains","startsWith","exists"]},"value":{"nullable":true,"description":"The single comparand for `equals`, `notEquals`, `greaterThan`, `lessThan`, `contains` and `startsWith` — a string, number or boolean, by the attribute. Null for `exists`; `in`, `notIn` and `between` use `values`.\n"},"values":{"type":"array","items":{"type":"string"}}}},
"AccessContext": {"type":"object","description":"**Everything the decision is allowed to depend on.** Stated as one object so a simulation and a live decision see the same shape — a simulator that takes different inputs from the evaluator is testing something else.\n","properties":{"principalId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"permission":{"type":"string"},"scopePath":{"type":"string"},"venueId":{"type":"string","format":"uuid","nullable":true},"attractionId":{"type":"string","format":"uuid","nullable":true},"deviceId":{"type":"string","format":"uuid","nullable":true},"eventId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time","nullable":true},"attributes":{"type":"object","additionalProperties":true,"description":"**Deliberately an open map**, keyed by attribute (the `AccessCondition.attribute` vocabulary, with `key` for the `*.attribute` forms), each value the one a condition compares against. **Supplied attributes are a fallback, not the source.** The evaluator resolves what it can itself; a caller that could assert its own membership tier could assert any membership tier.\n"}}},
"AccessDecision": {"type":"object","x-ticvai-persistence":"identity.access_decision","description":"3.3.37. **The decision, the policy version behind it, and the attribute values it actually saw.** The third is what separates *the policy is wrong* from *the data was stale*.\n","properties":{"id":{"type":"string","format":"uuid"},"effect":{"type":"string","enum":["permit","deny"]},"decidedAt":{"type":"string","format":"date-time"},"decidedBy":{"type":"string","enum":["central","deviceBundle"],"description":"3.3.29 against 3.3.30 — which evaluator answered."},"principalId":{"type":"string","format":"uuid","nullable":true},"permission":{"type":"string"},"scopePath":{"type":"string"},"matchedPolicies":{"type":"array","items":{"type":"object","properties":{"policyId":{"type":"string","format":"uuid"},"version":{"type":"integer"},"effect":{"type":"string"},"matched":{"type":"boolean"},"failedCondition":{"type":"string","nullable":true}}}},"observedAttributes":{"type":"object","additionalProperties":true,"description":"**Deliberately an open map**, the same keys as `AccessContext.attributes`: the value of every attribute the evaluator actually read, whichever source it came from.\n"},"overrideId":{"type":"string","format":"uuid","nullable":true},"latencyMs":{"type":"integer","nullable":true},"scopePathIndex":{"type":"string"}}},
"AuthorisationPolicy": {"type":"object","x-ticvai-persistence":"identity.authorisation_policy","description":"3.3. **Conditions and an effect, evaluated by one engine.** A role says who you are; a policy says under what circumstances that is enough.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). The package has two: this one, and the access contract's `AccessDynamicPolicy` (`access.dynamic_policy`). **This one governs who may do what in the software**: a principal's permissions on operations and screens (`permissions` names them), narrowed or extended by who, where, when and on what device, and decided by `evaluateAccess`. **`AccessDynamicPolicy` governs who may pass which gate**: a guest's, holder's or employee's admission at an access point, decided in the gate's validation with results such as `requireId` or `requireSupervisor` that mean nothing to a permission check. A staff member's badge opening a staff door is a gate decision (access); the same staff member approving a refund is a permission decision (here).\n**Settled by ADR-0068 (accepted 1 October): guest admission lives in Access only.** This engine keeps staff authorisation and was renamed to say so: `identity.access_policy` became `identity.authorisation_policy`, its versions `identity.authorisation_policy_version`, and its operations `*AuthorisationPolicy*`. \"Access policy\" now means `AccessDynamicPolicy` and nothing else.\n","required":["code","name","effect"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"Assigned by the server on `createAuthorisationPolicy`; the path names the policy on update."},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"isTemplate":{"type":"boolean","default":false},"permissions":{"type":"array","items":{"type":"string"},"description":"**Which permissions this policy speaks to.** A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about.\n"},"conditions":{"type":"array","items":{"$ref":"#/components/schemas/AccessCondition"}},"combining":{"type":"string","enum":["allMustMatch","anyMayMatch"],"default":"allMustMatch"},"effect":{"type":"string","enum":["permit","deny"],"description":"**Deny wins over permit when two policies disagree.** 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of every mistake anybody has made.\n"},"priority":{"type":"integer","default":0},"scopePath":{"type":"string","description":"3.3.40 to 3.3.43. **Tenant, venue and cross-venue policies are one mechanism**, because `scope_path` is prefix-comparable — `uae.dubai` contains `uae.dubai.marina` — and inheritance is the prefix walk rather than a second table.\n"},"appliesToRoleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"status":{"type":"string","readOnly":true,"description":"**Moved only by `setAuthorisationPolicyState`.** A policy is created as a `draft`, and a status sent in a create or update body is ignored — otherwise a write could skip the approval 3.3.26 requires.\n","enum":["draft","pendingApproval","active","suspended","retired"]},"version":{"type":"integer","default":1,"readOnly":true,"description":"Set by the server; every `updateAuthorisationPolicy` writes a new version."},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"delegatedAdminRoleIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"3.3.35. **Who may edit this policy without being a platform administrator.** A venue manager tuning their own opening-hours rule should not need someone who can edit every tenant's.\n"}}},
"AuthorisationPolicyEffectiveness": {"type":"object","x-ticvai-persistence":"none — computed from identity.access_decision and identity.access_override over the requested period","description":"One `AuthorisationPolicy` over a period (3.3.48; decided 29 September, build pass).","required":["policyId","evaluations"],"properties":{"policyId":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"status":{"type":"string","enum":["draft","pendingApproval","active","suspended","retired"]},"versionsInPeriod":{"type":"array","items":{"type":"integer"},"description":"The versions that decided anything in the period."},"evaluations":{"type":"integer","minimum":0,"description":"Decisions that evaluated this policy."},"matched":{"type":"integer","minimum":0,"description":"Evaluations in which every condition held (or one, for `anyMayMatch`)."},"decisivePermits":{"type":"integer","minimum":0,"description":"Permits this policy decided."},"decisiveDenies":{"type":"integer","minimum":0,"description":"Denies this policy decided, deny winning over any permit."},"overridesAtScope":{"type":"integer","minimum":0,"description":"Emergency overrides opened in the period at or beneath the policy's scope for a permission it speaks to - the times people had to go around it."},"lastMatchedAt":{"type":"string","format":"date-time","nullable":true},"neverMatched":{"type":"boolean","description":"True when the policy was evaluated and never matched in the period, the usual sign of a condition written backwards or a policy nobody needs."},"trend":{"type":"array","description":"One point per day in the period.","items":{"type":"object","properties":{"date":{"type":"string","format":"date"},"evaluations":{"type":"integer"},"decisiveDenies":{"type":"integer"}}}}}},
"AuthorisationPolicyVersion": {"type":"object","x-ticvai-persistence":"identity.authorisation_policy_version","description":"3.3.36 and 3.3.39. **Who changed what, from what, and why.**","properties":{"policyId":{"type":"string","format":"uuid"},"version":{"type":"integer"},"changedBy":{"type":"string","format":"uuid"},"changedAt":{"type":"string","format":"date-time"},"reason":{"type":"string","nullable":true},"approvedBy":{"type":"string","format":"uuid","nullable":true},"previous":{"$ref":"#/components/schemas/AuthorisationPolicy"},"current":{"$ref":"#/components/schemas/AuthorisationPolicy"},"scopePath":{"type":"string"}}},
"BulkUpdateSeatsRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["selection"],"properties":{"selection":{"type":"object","description":"Seats to amend. Combine filters; an empty selection is rejected.","properties":{"seatIds":{"type":"array","items":{"type":"string"}},"sectionCodes":{"type":"array","items":{"type":"string"}},"rowLabels":{"type":"array","items":{"type":"string"}}}},"categoryId":{"type":"string","format":"uuid"},"attribute":{"$ref":"#/components/schemas/SeatAttribute"},"isActive":{"type":"boolean"}}},
"ConfigurationProfile": {"type":"object","x-ticvai-persistence":"platform.configuration_profile","description":"Board 1 of the client's POS design set, 20 August. **The board shows 1,248 workstations across four versions and the package modelled none of it** — a firmware version field on the workstation, and nothing that says what a workstation is configured to be.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks alone*, which is the only reason to version a profile at all.\n","required":["id","name","venueKindScope","version","status"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"scopePath":{"type":"string"},"venueKindScope":{"type":"array","description":"Which workstation types it applies to. **A ticketing counter and a kitchen display do not share a profile**, and a profile that claims to is a profile somebody deploys to the wrong fleet.\n","items":{"type":"string"}},"version":{"type":"integer","readOnly":true,"description":"**Immutable once deployed anywhere.** A change makes a new version, and the old one stays readable — a workstation still running v2.3 must be able to say what v2.3 was. Assigned by the server: 1 on create, and one more each time a change lands on a published version (see `setConfigurationProfile`).\n"},"settings":{"type":"object","additionalProperties":true},"status":{"type":"string","enum":["draft","published","deploying","deployed","superseded","rolledBack"],"description":"On input only `draft` or `published`; sending `published` publishes this version. The other four are set by deployment and refused on input.\n"},"deployedCount":{"type":"integer","readOnly":true},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"Denomination": {"x-ticvai-persistence":"platform.denomination","description":"**Raised in review by Tanmay: denominations belong in a table, not in JSON.** He is right, and the reason is stronger than storage tidiness — **`orders.cash_movement.denominations` was a jsonb blob, so a note that stops circulating has nothing to deactivate.**\n**The seed is `docs/active/seed-data-proposal.md` section 1** (audit R229, proposed, client to correct): notes 5, 10, 20, 50, 100, 200, 500 and 1000 AED; coins 25 fils, 50 fils and 1 AED. The zero-valued coin in the list first supplied (`Coin, 0, COIN`) is a transcription slip rather than a denomination, is not seeded, and is the kind of row a table refuses and a JSON blob accepts silently.\n**Ordered for counting, not by value.** A cashier counts notes highest first and coins in the order they sit in the drawer, and `sortOrder` is what makes the count screen match the physical tray.\"\n","type":"object","required":["currencyCode","kind","value"],"properties":{"id":{"type":"string","format":"uuid"},"currencyCode":{"type":"string"},"displayName":{"type":"string","description":"What the cashier reads — *AED 500*, *Coin*. Localised, because a count screen is read at speed."},"kind":{"type":"string","enum":["note","coin"]},"sortOrder":{"type":"integer","description":"**Counting order, not value order.** Notes highest first, coins as they sit in the tray.\n"},"isActive":{"type":"boolean","default":true,"description":"**The field that makes this a table.** A note withdrawn from circulation is deactivated and stays in the count history — **a JSON blob cannot deactivate anything**, and deleting the value would rewrite every past cash-up that used it.\n"},"value":{"x-ticvai-column":"face_value_amount","$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"EmergencyAccessOverride": {"type":"object","x-ticvai-persistence":"identity.access_override","description":"3.3.6. **Time-boxed at creation, alerted as well as logged.**","properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"permissions":{"type":"array","items":{"type":"string"}},"reason":{"type":"string"},"createdBy":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"},"revokedAt":{"type":"string","format":"date-time","nullable":true},"alertedTo":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"IdentityAccessReviewCampaign": {"type":"object","x-ticvai-persistence":"identity.access_review_campaign","description":"**A periodic access review** (7.1.35, 7.1.56; decided 29 September, build pass, group G2): which grants, reviewed by whom, by when. Its items are `identity.access_review_item`. Lifecycle in `states/access-review-campaign.yaml`.","required":["name","scopePath","reviewerMode","dueAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string","maxLength":200},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005), and what is reviewed: every grant at or below it. Inside the caller's own scope. Operations write it at `venue` scope."},"roleIds":{"type":"array","nullable":true,"description":"Only grants of these roles; null reviews every grant in scope.","items":{"type":"string","format":"uuid"}},"reviewerMode":{"type":"string","enum":["lineManager","named"],"description":"`lineManager`: each item goes to the holder's manager from their primary work assignment, falling back to the named reviewers where none is found. `named`: the named reviewers share the items."},"reviewerPrincipalIds":{"type":"array","nullable":true,"items":{"type":"string","format":"uuid"}},"dueAt":{"type":"string","format":"date-time"},"recurrence":{"type":"string","enum":["none","quarterly","semiAnnual","annual"],"default":"none"},"prefillFromFindings":{"type":"boolean","default":true},"lookbackDays":{"type":"integer","minimum":7,"maximum":365,"default":90},"status":{"type":"string","enum":["open","completed","expired"],"readOnly":true},"itemCount":{"type":"integer","readOnly":true},"decidedCount":{"type":"integer","readOnly":true,"description":"Kept by `decideAccessReviewItem` in the same write, so the campaign list needs no count query."},"revokedCount":{"type":"integer","readOnly":true},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"closedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"IdentityAccessReviewItem": {"type":"object","x-ticvai-persistence":"identity.access_review_item","description":"One grant under review in a campaign, with the finding that pre-filled it and the reviewer's decision (decided 29 September, build pass, group G2). Lifecycle in `states/access-review-item.yaml`.","required":["campaignId","delegatedAccessId","principalId","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"campaignId":{"type":"string","format":"uuid","x-ticvai-references":"identity.access_review_campaign"},"delegatedAccessId":{"type":"string","format":"uuid","x-ticvai-references":"identity.delegated_access","description":"The grant under review."},"principalId":{"type":"string","format":"uuid","x-ticvai-references":"identity.principal"},"roleId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.role"},"scopePath":{"type":"string","description":"The grant's scope. **The partition key** (ADR-0005)."},"reviewerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal"},"findingKind":{"type":"string","enum":["none","excessive","conflicting"],"default":"none"},"lastUsedAt":{"type":"string","format":"date-time","nullable":true},"recommendation":{"type":"string","enum":["certify","revoke","review"]},"status":{"type":"string","enum":["pending","certified","revoked","notReviewed"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"reason":{"type":"string","maxLength":1000,"nullable":true}}},
"IdentityPermissionFinding": {"type":"object","x-ticvai-persistence":"none — computed from grants (roles, delegations, policies) against identity.access_decision and identity.segregation_rule","description":"One excessive, missing or conflicting permission (7.1.47; decided 29 September, build pass).","required":["kind","principalId","permission"],"properties":{"kind":{"type":"string","enum":["excessive","missing","conflicting"]},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid","nullable":true,"description":"The role that grants it, for excessive and conflicting; the role whose peers hold it, for missing."},"permission":{"type":"string"},"conflictingPermission":{"type":"string","nullable":true,"description":"The other half of the pair, for conflicting."},"segregationRuleId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"grantedBy":{"type":"string","enum":["role","delegation","policy"],"nullable":true},"lastUsedAt":{"type":"string","format":"date-time","nullable":true,"description":"The last permit that used it; null when never used in the window."},"deniedCount":{"type":"integer","nullable":true,"description":"For missing, the denials in the window."},"peersHoldingPercent":{"type":"number","minimum":0,"maximum":100,"nullable":true,"description":"For missing, the share of the role's holders at the same scope who hold the permission."},"recommendation":{"type":"string","enum":["revoke","grant","review"]},"asDraft":{"type":"boolean","default":false,"description":"True when the finding exists only because of the `draftPolicyId` evaluated."}}},
"OrgUnit": {"x-ticvai-persistence":"platform.scope","type":"object","required":["id","level","path","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"level":{"$ref":"#/components/schemas/ScopeLevel"},"parentId":{"type":"string","format":"uuid","nullable":true},"path":{"type":"string","description":"Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`.","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"isActive":{"type":"boolean","description":"False causes every permission query at or beneath this node to resolve to DENY.\n"},"childCount":{"type":"integer","minimum":0}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Placement": {"x-ticvai-persistence":"none — embedded in region_settings","type":"object","description":"Read-only here. Set by the Control Plane at provisioning.\nEvery region is its own logical cell. Placement determines the infrastructure backing it, which is how cost is controlled without varying the split rule: `shared` puts several regions' databases on one cluster; `dedicated` and `isolated` give a region its own. Regions in different countries MUST have placements in their respective jurisdictions.\n","readOnly":true,"required":["mode"],"properties":{"mode":{"type":"string","enum":["shared","dedicated","isolated","clientHosted"]},"cellName":{"type":"string"},"cloudRegion":{"type":"string"}}},
"Point": {"type":"object","required":["x","y"],"properties":{"x":{"type":"number"},"y":{"type":"number"}}},
"ProfileDeployment": {"type":"object","x-ticvai-persistence":"platform.profile_deployment","description":"**A deployment is an event with a date, a target and an outcome** — the client's board shows recent deployments with all three and the package had no record of any.\n**Staged rather than all-at-once by default.** Pushing a profile to 1,248 workstations simultaneously is how a venue discovers a bad profile at every till at the same moment.\n","required":["id","profileId","version","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"profileId":{"type":"string","format":"uuid","readOnly":true,"description":"Taken from the path of `deployConfigurationProfile`."},"version":{"type":"integer","description":"The published version to deploy."},"targetWorkstationIds":{"type":"array","items":{"type":"string","format":"uuid"}},"targetFilter":{"type":"object","nullable":true,"description":"By department, type or venue, where the target is a set rather than a list.\n","properties":{"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"departmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"workstationTypes":{"type":"array","description":"The same workstation-type values `ConfigurationProfile.venueKindScope` holds.","items":{"type":"string"}}}},"strategy":{"type":"string","enum":["immediate","staged","onNextIdle"],"default":"onNextIdle"},"status":{"type":"string","enum":["queued","inProgress","completed","partiallyFailed","rolledBack"],"readOnly":true},"succeededCount":{"type":"integer","readOnly":true},"failedCount":{"type":"integer","readOnly":true},"failureReasons":{"type":"object","readOnly":true,"additionalProperties":{"type":"integer"},"description":"**Grouped, because 40 workstations failing for one reason is one problem** and a list of 40 rows is forty.\n"},"startedAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"RegionSettings": {"x-ticvai-persistence":"platform.region_settings","type":"object","required":["countryCode","currencyCode","currencyScale","timeZone","fiscalYearStartMonth"],"properties":{"countryCode":{"type":"string","pattern":"^[A-Z]{2}$","description":"ISO 3166-1 alpha-2. Determines the jurisdiction, and therefore the cell."},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"description":"Decimal places for this region's currency. Varies by currency — some use 2, some use 3. Money columns are numeric(18,4) and carry the scale explicitly, because a fixed 2-place type silently truncates 3-place currencies.\n"},"timeZone":{"type":"string","description":"IANA zone, e.g. `Asia/Dubai`."},"dateFormat":{"type":"string","default":"dd/MM/yyyy"},"numberFormat":{"type":"string","default":"#,##0.00"},"fiscalYearStartMonth":{"type":"integer","minimum":1,"maximum":12,"description":"Varies by country."},"allowedAiResidencies":{"type":"array","description":"**The region's compliance gate on AI providers** (decided 28 September, audit R203; ADR-0009). The `AiProvider.residency` values a tenant in this region may use; empty means no restriction. `ai.setAiProvider` refuses any other residency with `409 residency-refused`. A prompt carrying guest data that reaches a provider hosted elsewhere is a cross-border transfer, and this is where a region says which it allows.\n","default":[],"items":{"type":"string"}},"placement":{"$ref":"#/components/schemas/Placement"},"cellName":{"type":"string","readOnly":true,"description":"The cell serving this region. One cell per tenant per region (ADR-0014).\n"}}},
"ScopeLevel": {"type":"string","description":"**The eight organisational levels, plus `subject`.** Restored 24 August.\n`tenancy.yaml` holds the authoritative definition of the eight levels and this mirrors them so a contract can reference a level without depending on the whole tenancy surface. **Seven organisational levels plus `outlet`** — a commercial branch beside the organisational one (CF-138, ADR-0018). **A department has requisitions and rotas; an outlet has a menu and stock**, and modelling a restaurant as a department would put it in the staffing tree.\n\n**`subject` is the one value tenancy does not have, and it is not a level.** It is here because `check-package` reads this enum as the closed vocabulary for `x-ticvai-scope-level`, and some operations act on one guest's own resources, which sit in no node of the venue hierarchy. So `subject` is valid as an operation's scope level and never as a `ScopeRef.level`: every `ScopeRef` is a row of `platform.scope`, and those carry one of the eight.\n","enum":["tenant","brand","region","venue","department","subDepartment","workstation","outlet","subject"]},
"SeatAttribute": {"type":"string","description":"BL-168. **Extended from eight values on 18 August.** Amenity and view filters needed attributes the original set did not carry, and a guest filtering for *aisle seat with power* was filtering on something the model could not express.\n","enum":["standard","accessible","companion","obstructedView","restrictedLegroom","premium","houseSeat","buffer","aisle","endOfRow","extraLegroom","powerOutlet","tableService","shaded","covered","nearExit","nearAccessibleWc","wheelchairTransfer","limitedRecline","sofa","beanbag"]},
"SeatMap": {"x-ticvai-persistence":"seating.seat_map","allOf":[{"$ref":"#/components/schemas/SeatMapSummary"},{"type":"object","required":["sections"],"properties":{"description":{"type":"string","nullable":true},"viewBox":{"type":"object","description":"Coordinate space for rendering. Absent when there is no geometry.","nullable":true,"properties":{"width":{"type":"number"},"height":{"type":"number"}}},"stagePosition":{"$ref":"#/components/schemas/Point"},"sections":{"type":"array","items":{"$ref":"#/components/schemas/Section"}},"isActive":{"type":"boolean"}}}]},
"SeatMapStatus": {"type":"string","enum":["draft","validated","published","archived"]},
"SeatMapSummary": {"x-ticvai-persistence":"seating.seat_map","type":"object","required":["id","name","venueId","status","seatCount"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/SeatMapStatus"},"seatCount":{"type":"integer"},"sectionCount":{"type":"integer"},"hasGeometry":{"type":"boolean","description":"False when only a manifest has been imported. Such a map can be sold from a list but not rendered.\n"},"publishedAt":{"type":"string","format":"date-time","nullable":true}}},
"Section": {"x-ticvai-persistence":"seating.section","type":"object","required":["code","name","rowCount","seatCount"],"properties":{"code":{"type":"string"},"name":{"type":"string"},"rowCount":{"type":"integer"},"seatCount":{"type":"integer"},"boundary":{"type":"array","items":{"$ref":"#/components/schemas/Point"},"description":"Polygon for rendering. Absent without geometry."},"viewAssetId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"assets.MediaAsset","description":"**The view of the stage from this section, as a photo**, uploaded through `assets` like any other media (decided 29 September, rev 3 23SEP-14). Optional: where it is null the client renders the view from the imported geometry (the section `boundary`, the map's `stagePosition` and the seat positions), so a closer section shows a larger stage and fewer rows ahead. Set with `updateSeatMap` `sectionViews`, which is allowed on a published map because a photo does not change the map's shape.\n"},"rows":{"type":"array","items":{"type":"object","required":["label","seatCount"],"properties":{"label":{"type":"string"},"seatCount":{"type":"integer"},"numberingDirection":{"type":"string","enum":["leftToRight","rightToLeft"],"description":"Which end row numbering starts from. Not recoverable from a manifest and must be stated — it determines whether a guest finds their seat.\n"}}}},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"SetDenominationsRequest": {"type":"object","description":"Request only. One currency's complete list; anything not in it is deactivated. Entries match existing rows on `kind` and `value` (see `setDenominations`).\n","required":["scopePath","currencyCode","denominations"],"properties":{"scopePath":{"type":"string","description":"The region the write is made at — the materialised path of a `region` scope node. The caller's `REGION_CONFIGURE` grant must cover it.\n"},"currencyCode":{"type":"string","minLength":3,"maxLength":3},"denominations":{"type":"array","minItems":1,"items":{"type":"object","required":["displayName","kind","value","sortOrder"],"properties":{"displayName":{"type":"string","maxLength":60},"kind":{"type":"string","enum":["note","coin"]},"value":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"sortOrder":{"type":"integer","minimum":0},"isActive":{"type":"boolean","default":true}}}}}},
"VenueMap": {"type":"object","x-ticvai-persistence":"venuemap.map","description":"A park map, or a floor plan. **Several per venue** — a guest on the second floor should not be shown the ground floor's toilets.\n","required":["id","name","venueId","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","readOnly":true,"description":"Derived from `venueId`. Not sent by a client."},"kind":{"type":"string","enum":["park","floor","zone","parking"]},"floorLevel":{"type":"integer","nullable":true},"status":{"type":"string","enum":["draft","published","archived"],"readOnly":true,"description":"`draft` on create. Moves through `publishVenueMap` (`states/venue-map.yaml`), never by sending a value.\n"},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `VenueMapVersion.version` guests are served. Null until the first publish.\n"},"graphVersion":{"type":"integer","readOnly":true,"description":"**Bumped by a publish or a closure**, and returned as `VenueMapGraph.version`. Separate from `publishedVersion` because a closure changes the routes without creating a map version, and a closure that looked like a publish would lie about what changed.\n"},"isGeoreferenced":{"type":"boolean","readOnly":true,"description":"**Whether a guest can be located on it.** Without a georeference the map is a picture — useful, and not navigable.\n"},"baseAssetId":{"type":"string","format":"uuid","nullable":true,"description":"**The illustrated map a guest actually sees**, held in `assets` like any other media.\n**This is not the CAD drawing.** The drawing gives geometry — where things are, and how they connect. The base image is a designed illustration with the venue's own styling, and the two are different artefacts that happen to describe the same place. A park hands you an architect's plan and a beautiful painted map, and **the guest wants the second while the platform needs the first.**\nNull is valid. A map with geometry and no illustration renders as shapes — plain, and navigable.\n","x-ticvai-references":"assets.MediaAsset"},"baseImageAlignment":{"type":"object","nullable":true,"description":"**How the illustration lines up with the geometry.** They are drawn at different scales by different people, and a point placed on the plan lands in the wrong place on the painting unless something reconciles them.\nTwo known points is enough. **Without this the illustration is a picture behind the map rather than the map itself.**\n","properties":{"imageWidthPx":{"type":"integer"},"imageHeightPx":{"type":"integer"},"anchors":{"type":"array","minItems":2,"maxItems":4,"items":{"type":"object","properties":{"planX":{"type":"number"},"planY":{"type":"number"},"imageX":{"type":"number"},"imageY":{"type":"number"}}}}}},"tileSetRef":{"type":"string","nullable":true,"readOnly":true,"description":"Where a base image is large enough to need zoom levels. **A 12,000-pixel park map is not something a phone downloads on arrival**, and a guest opening the map on venue wifi at the gate is the worst moment to send twenty megabytes.\nGenerated from the base asset. Null means the image is small enough to serve whole.\n"},"boundsGeoJson":{"type":"string","nullable":true},"graphStatus":{"type":"string","readOnly":true,"enum":["notBuilt","connected","disconnected","partial"],"description":"**Whether every public point can actually be reached.** Computed at publish.\n`disconnected` means a point has no path to it at all — a toilet nobody can walk to is a toilet that does not exist. `partial` means every point is reachable and at least one only by steps, which is a different and quieter failure: **the map works until a wheelchair user opens it.**\n"}}},
"VenueSettings": {"type":"object","x-ticvai-persistence":"platform.venue_settings","description":"**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setVenueSettings`."},"calendarDayStartHour":{"type":"integer","minimum":0,"maximum":23,"nullable":true,"default":6,"description":"**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"nullable":true,"readOnly":true,"description":"**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"},"supportHours":{"type":"object","description":"CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n","properties":{"mode":{"type":"string","enum":["alwaysOn","businessHours","custom","none"]},"timezone":{"type":"string","description":"IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"},"windows":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time the desk opens."},"to":{"type":"string","description":"Wall-clock time the desk closes."}}}},"outOfHoursMessage":{"type":"string","nullable":true}}},"quietHours":{"type":"object","nullable":true,"description":"**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n","properties":{"from":{"type":"string","description":"Wall-clock time sending stops","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time sending resumes","in the region's time zone.":null}}},"biometrics":{"type":"object","nullable":true,"description":"CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n","properties":{"isEnabled":{"type":"boolean","default":false,"description":"**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"},"dpiaReference":{"type":"string","nullable":true,"maxLength":200,"description":"**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"},"consentNoticeAcknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"},"faceTagPurgeMinutesAfterClose":{"type":"integer","nullable":true,"default":0,"description":"BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"}}},"segregatedAccess":{"type":"object","nullable":true,"description":"CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n","properties":{"isEnabled":{"type":"boolean","default":false},"appliesToAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"schedule":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"admits":{"type":"string","enum":["all","women","womenAndChildren","families","members"]}}}},"entitlementGated":{"type":"boolean","default":true,"readOnly":true,"description":"**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"},"genderVerification":{"type":"string","enum":["off","staffAssisted","deviceAssisted"],"default":"off","description":"`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"},"overrideRateAlertThreshold":{"type":"number","nullable":true,"description":"Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"}}},"alerting":{"type":"object","description":"CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n","properties":{"channel":{"type":"string","enum":["dashboardPanel","dashboardAndEmail","dashboardAndWhatsapp"],"default":"dashboardPanel"},"acknowledgementRequired":{"type":"boolean","default":true},"escalateAfterMinutes":{"type":"integer","nullable":true}}},"displayCurrencies":{"type":"array","nullable":true,"description":"**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"cartLeaseSeconds":{"type":"integer","nullable":true,"minimum":30,"maximum":3600,"default":900,"description":"**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"},"cartHoldExtensionMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":5,"description":"How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."},"cartMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."},"resaleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":168,"default":24,"description":"Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."},"exchangeCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."},"rescheduleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."},"reservationMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."},"shiftVarianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"},"catalogue":{"type":"object","nullable":true,"properties":{"maxVariantsPerProduct":{"type":"integer","nullable":true,"minimum":1,"maximum":2000,"default":200,"description":"Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."},"waitlistOfferHoldMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":1440,"default":30,"description":"How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":10,"description":"A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationCount":{"type":"integer","nullable":true,"minimum":1,"default":50,"description":"A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."}}},"inventory":{"type":"object","nullable":true,"properties":{"overReceiptTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":5,"description":"Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."},"countVarianceTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":2,"description":"Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."},"countVarianceApprovalAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"}}},"seating":{"type":"object","nullable":true,"properties":{"seatHoldExtensionSeconds":{"type":"integer","nullable":true,"minimum":60,"maximum":1800,"default":300,"description":"What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."},"seatHoldMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":2,"description":"How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."},"maxSeatsPerGuestOrder":{"type":"integer","nullable":true,"minimum":1,"maximum":50,"default":10,"description":"**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"}}},"promotions":{"type":"object","nullable":true,"properties":{"maxDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":30,"description":"The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."},"nearZeroLinePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"}}},"fnb":{"type":"object","nullable":true,"properties":{"recallWindowMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":60,"default":10,"description":"Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."},"compEscalationAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"},"foodSafetyLeadPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"}}},"queue":{"type":"object","nullable":true,"properties":{"crossQueueLimit":{"type":"integer","nullable":true,"minimum":1,"maximum":10,"default":2,"description":"Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."}}},"reporting":{"type":"object","nullable":true,"properties":{"inlineRunRowLimit":{"type":"integer","nullable":true,"minimum":1000,"maximum":100000,"default":5000,"description":"Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."},"dashboardRefreshBudgetPerMinute":{"type":"integer","nullable":true,"minimum":1,"default":24,"description":"Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."}}},"marketing":{"type":"object","nullable":true,"properties":{"attributionWindowDays":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":7,"description":"Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."}}},"identity":{"type":"object","nullable":true,"properties":{"guestOtpMaxAttempts":{"type":"integer","nullable":true,"minimum":3,"maximum":10,"default":5,"description":"Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"},"guestTwoStep":{"type":"object","nullable":true,"description":"**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."},"stepUpActions":{"type":"array","uniqueItems":true,"description":"The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n","items":{"type":"string","enum":["changeContactDetails","changePassword","managePaymentMethods","transferTickets","deleteAccount"]},"default":["changeContactDetails","changePassword","managePaymentMethods","deleteAccount"]}}}}}}},
"VisualWorkflowDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; writes approvals.workflow_definition and a draft approvals.workflow_version (data model for the agreed operations, 29 September)","description":"**What Visual Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"definition":{"type":"string","description":"The workflow graph (nodes and connections) as a JSON document"},"nodeTypes":{"type":"array","items":{"type":"string","enum":["start","trigger","task","decision","approval","systemAction","notification","wait","timer","parallelBranch","merge","escalation","subWorkflow","end"]},"description":"Node kinds used in this workflow"},"workflowName":{"type":"string","description":"Workflow Name"},"module":{"type":"string","description":"Module"},"businessProcess":{"type":"string","description":"Business Process"},"owner":{"type":"string","description":"Owner"},"version":{"type":"string","description":"Version"},"priority":{"type":"string","description":"Priority"},"effectiveFrom":{"type":"string","description":"Effective Dates"},"validationIssues":{"type":"array","items":{"type":"string","enum":["deadEnds","missingOutcomes","circularLoops","missingAssignee","invalidActions"]},"description":"Design problems the designer found (read-only)"},"workflowId":{"type":"string","description":"Workflow identifier; absent on input to create a new workflow"},"trigger":{"type":"string","description":"What starts the workflow"},"effectiveTo":{"type":"string","format":"date-time","description":"Effective to"}},"required":["workflowName","module","definition"]},
"VisualWorkflowDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_definition and its draft approvals.workflow_version (data model for the agreed operations, 29 September)","description":"**What Visual Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"definition":{"type":"string","description":"The workflow graph (nodes and connections) as a JSON document"},"nodeTypes":{"type":"array","items":{"type":"string","enum":["start","trigger","task","decision","approval","systemAction","notification","wait","timer","parallelBranch","merge","escalation","subWorkflow","end"]},"description":"Node kinds used in this workflow"},"workflowName":{"type":"string","description":"Workflow Name"},"module":{"type":"string","description":"Module"},"businessProcess":{"type":"string","description":"Business Process"},"owner":{"type":"string","description":"Owner"},"version":{"type":"string","description":"Version"},"priority":{"type":"string","description":"Priority"},"effectiveFrom":{"type":"string","description":"Effective Dates"},"validationIssues":{"type":"array","items":{"type":"string","enum":["deadEnds","missingOutcomes","circularLoops","missingAssignee","invalidActions"]},"description":"Design problems the designer found (read-only)"},"workflowId":{"type":"string","description":"Workflow identifier; absent on input to create a new workflow"},"trigger":{"type":"string","description":"What starts the workflow"},"effectiveTo":{"type":"string","format":"date-time","description":"Effective to"}},"required":["workflowName","module","definition"]}
}
```
