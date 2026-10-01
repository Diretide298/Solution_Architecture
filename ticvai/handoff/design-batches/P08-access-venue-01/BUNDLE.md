# P08-access-venue-01 — P08 · Access & Venue (1 of 3)

**10 screens · 65 operations · 82 schemas · 22 permissions**

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

- **Every control that can be refused must be gated.** 22 permissions apply here:
  `ACCESS_POINT_CONFIGURE, AI_USE, ASSET_MANAGE, ASSET_VIEW, EVENT_CONFIGURE, MAINTENANCE_APPROVE, MAINTENANCE_EXECUTE, MARKETING_MANAGE, MARKETING_SEND, MARKETING_VIEW, ORDER_REFUND_APPROVE, ORDER_REFUND_BULK`…. A control nobody can use must say so,
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
| `BO-001` | Queue Directory | A | 80 | 97 | 6 | 37 | 1 | 6 | — | notStarted (generated) |
| `BO-002` | Queue Configuration | B–D | 80 | 71 | 6 | 49 | 4 | 6 | — | notStarted (generated) |
| `BO-003` | Queue Integration Setup | B–D | 12 | 23 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-004` | Manual Wait Time Entry | B–D | 66 | 56 | 6 | 24 | 2 | 6 | — | notStarted (generated) |
| `BO-005` | Queue Monitor | A | 109 | 86 | 6 | 57 | 3 | 6 | — | notStarted (generated) |
| `BO-006` | Parking Configuration | A | 18 | 38 | 6 | 9 | 2 | 2 | — | notStarted (generated) |
| `BO-030` | Work Order Verification | B–D | 42 | 44 | 6 | 31 | 0 | 2 | — | notStarted (generated) |
| `BO-031` | Asset Register | B–D | 42 | 36 | 6 | 23 | 2 | 0 | — | notStarted (generated) |
| `BO-032` | Admission Profiles | A | 94 | 22 | 6 | 12 | 1 | 0 | — | notStarted (generated) |
| `BO-033` | Blacklist Management | A | 3 | 12 | 6 | 2 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-001` Queue Directory

**See every queue in the venue and whether its data is arriving.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `queue` module |
| Block | Block A · ticket #17954 (APP-SETUP-BO-001) |
| Who uses it | venue staff holding `EVENT_CONFIGURE`, `PERFORMANCE_CONFIGURE`, `PRODUCT_VIEW`, `QUEUE_MANAGE`, `QUEUE_VIEW` (3 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listQueues` reads the population and `getEvent` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `eventId` (deepLink), `feedId` (deepLink), `queueId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/queue-management/queue-directory` |

**What the spec says about it.** A queue on the manual adaptor shows "manual" rather than "no feed". It is configured and working; treating it as unconfigured makes the health view lie. **Was the declared entry point to the whole back office until 20 August**, which is why 93 screens were unreachable. Now reached from BO-100 through its section.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listQueues`. | `listQueues` ?venueId |
| Open only | toggle | optional | off | — | — | Sends `?openOnly=` to `listQueues`. | `listQueues` ?openOnly |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |

**Form: Call next parties** (modal, opened by *Call next parties*; *Call next parties* calls `callNextParties`, *Cancel* sends nothing)

**Collects what `callNextParties` sends before it is called.** Nothing in the body is required. Optional: `partyCount`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Party count `partyCount` | number field | optional | — | min 1 | — | Defaults to the queue's capacity per cycle. | `callNextParties` body |

**Form: Configure queue feed** (modal, opened by *Configure queue feed*; *Configure queue feed* calls `configureQueueFeed`, *Cancel* sends nothing)

**Collects what `configureQueueFeed` sends before it is called.** Required: `id`, `queueId`, `adaptor`, `isEnabled`. Optional: `adaptorName`, `credentialsRef`, `expectedIntervalSeconds`, `health`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `configureQueueFeed` body |
| Queue `queueId` | picker: choose a queue | required | — | — | shows names, sends the id | — | `configureQueueFeed` body |
| Adaptor `adaptor` | segmented control | required | — | Generic · Mock · Vendor adaptor | — | Vendor adaptors are bespoke work (ADR-0012). `generic` is the inbound API any system can post to; `mock` lets the feature be built and demonstrated with no vendor at all. | `configureQueueFeed` body |
| Adaptor name `adaptorName` | text field | optional | — | — | — | Named vendor where `adaptor` is `vendorAdaptor`. | `configureQueueFeed` body |
| Credentials ref `credentialsRef` | text field | optional | — | — | — | Key vault reference. Credentials are never returned. | `configureQueueFeed` body |
| Expected interval seconds `expectedIntervalSeconds` | number field (seconds) | optional | 60 | — | — | Beyond this without a reading, the feed is considered quiet. | `configureQueueFeed` body |
| Is enabled `isEnabled` | toggle | required | — | — | — | — | `configureQueueFeed` body |

Errors to draw in the form: 400 Unknown adaptor, or credentials missing for the selected adaptor; 409 The feed with this `id` belongs to a different queue.

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

**Form: Create queue** (modal, opened by *Create queue*; *Create queue* calls `createQueue`, *Cancel* sends nothing)

**Collects what `createQueue` sends before it is called.** Required: `code`, `name`, `venueId`, `capacityPerCycle`, `cycleMinutes`. Optional: `attractionProductId`, `assetId`, `accessPointId`, `kind`, `operatingWindows`, `parentQueueId`, `loadBalanceWithQueueIds`, `inQueueOfferEnabled`, `notifyBeforeCallMinutes`, `maxPartySize`, `returnWindowMinutes`, `heightRequirementCm` and 2 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createQueue` body |
| Name `name` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createQueue` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createQueue` body |
| Attraction product `attractionProductId` | picker: choose an attraction product | optional | — | — | shows names, sends the id | — | `createQueue` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. | `createQueue` body |
| Access point `accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | — | `createQueue` body |
| Kind `kind` | select | optional | Standby | Standby · Single rider · Fast pass · Virtual · Accessible · Group only · Staff only | — | 5.6.x. A ride has several queues and the model had one. | `createQueue` body |
| Operating windows `operatingWindows` | repeatable rows | optional | — | — | — | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen. | `createQueue` body |
| Day `operatingWindows[].day` | select | required | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `createQueue` body |
| From `operatingWindows[].from` | time picker | required | — | — | HH:mm, 24-hour | Venue local time, 24-hour `HH:MM`, when the queue starts running. | `createQueue` body |
| To `operatingWindows[].to` | time picker | required | — | — | HH:mm, 24-hour | Venue local time, 24-hour `HH:MM`, when the queue stops running. | `createQueue` body |
| Last entry minutes before `operatingWindows[].lastEntryMinutesBefore` | number field (minutes) | optional | 0 | — | — | When the queue stops accepting, which is before it stops running. A guest joining two minutes before close waits twenty and is turned away at the front. | `createQueue` body |
| Parent queue `parentQueueId` | picker: choose a parent queue | optional | — | — | shows names, sends the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that is expressed without either queue … | `createQueue` body |
| Load balance with queues `loadBalanceWithQueueIds` | multi-picker: choose load balance with queues | optional | — | — | — | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. | `createQueue` body |
| In queue offer enabled `inQueueOfferEnabled` | toggle | optional | off | — | — | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. | `createQueue` body |
| Notify before call minutes `notifyBeforeCallMinutes` | number field (minutes) | optional | 5 | — | — | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line is visible. | `createQueue` body |
| Capacity per cycle `capacityPerCycle` | number field | required | — | min 1 | — | — | `createQueue` body |
| Cycle minutes `cycleMinutes` | number field (minutes) | required | — | min 0 | — | — | `createQueue` body |
| Max party size `maxPartySize` | number field | optional | 6 | — | — | — | `createQueue` body |
| Return window minutes `returnWindowMinutes` | number field (minutes) | optional | 15 | — | — | How long a called party has to arrive before the entry expires. | `createQueue` body |
| Height requirement cm `heightRequirementCm` | number field | optional | — | — | — | — | `createQueue` body |
| Fast pass allocation percent `fastPassAllocationPercent` | stepper or slider | optional | 0 | min 0; max 100 | — | Share of each cycle reserved for Fast Pass holders. | `createQueue` body |
| Zone `zone` | text field | optional | — | — | — | — | `createQueue` body |
| Fast pass `fastPass` | group | optional | — | — | — | The lane's Fast Pass block (decided 29 September, VM close-out). Null on a queue that takes no Fast Pass. | `createQueue` body |
| Entitlement products `fastPass.entitlementProductIds` | multi-picker: choose entitlement products | required | — | — | — | Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need. | `createQueue` body |
| Loyalty tiers `fastPass.loyaltyTierIds` | multi-picker: choose loyalty tiers | optional | — | — | — | 5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. | `createQueue` body |
| Promotions `fastPass.promotionIds` | multi-picker: choose promotions | optional | — | — | — | 5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. | `createQueue` body |
| Accessibility priority `fastPass.accessibilityPriority` | toggle | optional | off | — | — | 5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. | `createQueue` body |
| Return window minutes `fastPass.returnWindowMinutes` | number field (minutes) | optional | 60 | min 1; max 240 | — | How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan. | `createQueue` body |
| Max per guest per day `fastPass.maxPerGuestPerDay` | number field | optional | — | min 1 | — | Fast Pass redemptions one guest may make on this lane per day; null is no cap. | `createQueue` body |
| Allowed access points `fastPass.allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Access points that redeem Fast Pass for this lane; empty is the queue's own. | `createQueue` body |

Errors to draw in the form: 400 Validation failed

**Form: Save queue status** (modal, opened by *Save queue status*; *Save queue status* calls `setQueueStatus`, *Cancel* sends nothing)

**Collects what `setQueueStatus` sends before it is called.** Required: `status`, `reason`. Optional: `guestMessage`, `expectedReopenAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | radio group | required | — | Open · Paused · Closed · At capacity | — | — | `setQueueStatus` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `setQueueStatus` body |
| Guest message `guestMessage` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setQueueStatus` body |
| Expected reopen at `expectedReopenAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setQueueStatus` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Save wait time** (modal, opened by *Save wait time*; *Save wait time* calls `setWaitTime`, *Cancel* sends nothing)

**Collects what `setWaitTime` sends before it is called.** Required: `waitMinutes`. Optional: `expiresInMinutes`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Wait minutes `waitMinutes` | number field (minutes) | required | — | min 0 | — | — | `setWaitTime` body |
| Expires in minutes `expiresInMinutes` | number field (minutes) | optional | 30 | min 1 | — | How long this manual figure stands before the queue reverts. | `setWaitTime` body |
| Note `note` | text area | optional | — | max length 200 | — | — | `setWaitTime` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Save event** (modal, opened by *Save event*; *Save event* calls `updateEvent`, *Cancel* sends nothing)

**Collects what `updateEvent` sends before it is called.** Nothing in the body is required. Optional: `name`, `parentEventId`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateEvent` body |
| Parent event `parentEventId` | picker: choose a parent event | optional | — | — | shows names, sends the id | — | `updateEvent` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateEvent` body |

**Form: Save queue** (modal, opened by *Save queue*; *Save queue* calls `updateQueue`, *Cancel* sends nothing)

**Collects what `updateQueue` sends before it is called.** Nothing in the body is required. Optional: `name`, `capacityPerCycle`, `cycleMinutes`, `maxPartySize`, `returnWindowMinutes`, `heightRequirementCm`, `fastPassAllocationPercent`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | The same locale-to-text map `createQueue` takes and `Queue` returns, so an edit form round-trips the name. | `updateQueue` body |
| Capacity per cycle `capacityPerCycle` | number field | optional | — | min 1 | — | — | `updateQueue` body |
| Cycle minutes `cycleMinutes` | number field (minutes) | optional | — | min 0 | — | — | `updateQueue` body |
| Max party size `maxPartySize` | number field | optional | — | min 1 | — | — | `updateQueue` body |
| Return window minutes `returnWindowMinutes` | number field (minutes) | optional | — | min 1 | — | — | `updateQueue` body |
| Height requirement cm `heightRequirementCm` | number field | optional | — | — | — | — | `updateQueue` body |
| Fast pass allocation percent `fastPassAllocationPercent` | stepper or slider | optional | — | min 0; max 100 | — | — | `updateQueue` body |
| Fast pass `fastPass` | group | optional | — | — | — | The lane's Fast Pass block (decided 29 September, VM close-out). Replaces the whole block; null removes it. | `updateQueue` body |
| Entitlement products `fastPass.entitlementProductIds` | multi-picker: choose entitlement products | required | — | — | — | Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need. | `updateQueue` body |
| Loyalty tiers `fastPass.loyaltyTierIds` | multi-picker: choose loyalty tiers | optional | — | — | — | 5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. | `updateQueue` body |
| Promotions `fastPass.promotionIds` | multi-picker: choose promotions | optional | — | — | — | 5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. | `updateQueue` body |
| Accessibility priority `fastPass.accessibilityPriority` | toggle | optional | off | — | — | 5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. | `updateQueue` body |
| Return window minutes `fastPass.returnWindowMinutes` | number field (minutes) | optional | 60 | min 1; max 240 | — | How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan. | `updateQueue` body |
| Max per guest per day `fastPass.maxPerGuestPerDay` | number field | optional | — | min 1 | — | Fast Pass redemptions one guest may make on this lane per day; null is no cap. | `updateQueue` body |
| Allowed access points `fastPass.allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Access points that redeem Fast Pass for this lane; empty is the queue's own. | `updateQueue` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every queue** (data table, from `listQueues`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Venue | the name it points at, never the id | — |
| Attraction product | the name it points at, never the id | — |
| Asset | the image or video | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. |
| Access point | the name it points at, never the id | — |
| Kind | chip: Standby, Single rider, Fast pass, Virtual, Accessible, Group only… | 5.6.x. A ride has several queues and the model had one. |
| Operating windows | list or chips (count when long) | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for … |
| Parent queue | the name it points at, never the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that … |
| Load balance with queues | list or chips (count when long) | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. |
| In queue offer enabled | yes / no (icon or chip) | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. |
| Notify before call minutes | 1,234 | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line … |

**Every queue feed** (data table, from `listQueueFeeds`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Queue | the name it points at, never the id | — |
| Adaptor | chip: Generic, Mock, Vendor adaptor | Vendor adaptors are bespoke work (ADR-0012). `generic` is the inbound API any system can post to; `mock` lets the feature be built and … |
| Adaptor name | text | Named vendor where `adaptor` is `vendorAdaptor`. |
| Credentials ref | text | Key vault reference. Credentials are never returned. |
| Expected interval seconds | 1,234 | Beyond this without a reading, the feed is considered quiet. |
| Is enabled | yes / no (icon or chip) | — |
| Health | grouped details | Whether the feed is currently reporting, computed on read — what `listQueueFeeds` promises per row. |

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

**Every waiting guest** (data table, from `listQueueEntries`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client-generated UUIDv7 from `JoinQueueRequest.id`, and the `entryId` every entry path takes. |
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Subject | the name it points at, never the id | — |
| Party number | 1,234 | What the guest sees and what appears on signage. |
| Party size | 1,234 | — |
| Status | chip: Waiting, Called, Redeemed, Expired, No show, Cancelled… | — |
| Position in queue | 1,234 | — |
| Parties ahead | 1,234 | — |
| Estimated call at | 1 Oct 2026, 14:30 | — |
| Is fast pass | yes / no (icon or chip) | — |
| Entitlement | text | — |

**Data table** (data table): Current wait, source, feed health, status

**Banner** (banner): Queues whose feed has gone quiet. The first thing a duty manager checks

**The selected queue** (detail panel, from `listQueues`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Venue | the name it points at, never the id | — |
| Attraction product | the name it points at, never the id | — |
| Asset | the image or video | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. |
| Access point | the name it points at, never the id | — |
| Kind | chip: Standby, Single rider, Fast pass, Virtual, Accessible, Group only… | 5.6.x. A ride has several queues and the model had one. |
| Operating windows | list or chips (count when long) | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for … |
| Parent queue | the name it points at, never the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that … |
| Load balance with queues | list or chips (count when long) | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. |
| In queue offer enabled | yes / no (icon or chip) | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. |
| Notify before call minutes | 1,234 | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line … |
| Capacity per cycle | 1,234 | — |
| Cycle minutes | 1,234.5 | — |
| Max party size | 1,234 | — |
| Return window minutes | 1,234 | How long a called party has to arrive before the entry expires. |

**The queue** (detail panel, from `getQueue`)

| Shows | Format | Notes |
|---|---|---|
| Now serving party number | 1,234 | — |
| Last called at | 1 Oct 2026, 14:30 | — |
| Throughput last hour | 1,234 | — |
| No show rate percent | 1,234.5 | — |
| Feed | grouped details | — |

**The queue feed health** (detail panel, from `getQueueFeedHealth`)

| Shows | Format | Notes |
|---|---|---|
| Feed | the name it points at, never the id | — |
| Adaptor | chip: Generic, Mock, Vendor adaptor | Vendor adaptors are bespoke work (ADR-0012). `generic` is the inbound API any system can post to; `mock` lets the feature be built and … |
| Is healthy | yes / no (icon or chip) | Healthy means the last reading arrived within the feed's expected interval (decided 28 September, audit R106 (1)): `lastReadingAt` is no … |
| Is quiet | yes / no (icon or chip) | No reading within the expected interval. The wait time falls back to throughput-derived and is marked stale rather than freezing at the … |
| Last reading at | 1 Oct 2026, 14:30 | — |
| Expected interval seconds | 1,234 | The feed's `expectedIntervalSeconds` — the interval `isQuiet` is judged against, returned here so a health panel does not need the feed row … |
| Readings last hour | 1,234 | — |
| Discarded last hour | 1,234 | Out-of-order readings rejected in the last hour — rows of `queue.reading` for this feed with `disposition: discardedOutOfOrder`. |

**The wait time** (detail panel, from `getWaitTimes`)

| Shows | Format | Notes |
|---|---|---|
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Attraction product | the name it points at, never the id | — |
| Attraction category | the name it points at, never the id | The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Source | chip: Sensor, Throughput, Manual, Unavailable | Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

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
| Call next parties (primary button) | `callNextParties` POST `/queues/{queueId}/call-next` | inline | inline | — | opens modal first |
| Configure queue feed (secondary button) | `configureQueueFeed` PUT `/queue-feeds` | QueueFeed | QueueFeed | 400 Unknown adaptor, or credentials missing for the selected adaptor; 409 The feed with this `id` belongs to a different queue. | opens modal first |
| Create event (secondary button) | `createEvent` POST `/events` | CreateEventRequest | Event | 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … | opens modal first |
| Create performances (secondary button) | `createPerformances` POST `/events/{eventId}/performances` | CreatePerformancesRequest | inline | — | opens modal first |
| Create queue (secondary button) | `createQueue` POST `/queues` | CreateQueueRequest | Queue | 400 Validation failed | opens modal first |
| Save queue status (secondary button) | `setQueueStatus` PUT `/queues/{queueId}/status` | inline | QueueStatusResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Save wait time (secondary button) | `setWaitTime` PUT `/queues/{queueId}/wait-time` | inline | WaitTime | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Test queue feed (secondary button) | `testQueueFeed` POST `/queue-feeds/{feedId}/test` | — | FeedTestResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Save event (secondary button) | `updateEvent` PATCH `/events/{eventId}` | inline | Event | — | opens modal first |
| Save queue (secondary button) | `updateQueue` PATCH `/queues/{queueId}` | inline | Queue | — | opens modal first |

**Data it reads**: `listQueues` (onLoad, Every queue with its current wait); `listQueueFeeds` (onLoad, Feed health per queue); `getWaitTimes` (onLoad, Wait times across a venue); `listEvents` (onLoad, List events)

**Where the user goes next**

- → `BO-003` Queue Integration Setup: *Queue Integration Setup*; carries `feedId`
- → `BO-004` Manual Wait Time Entry: *Manual Wait Time Entry*; carries `queueId`
- → `BO-005` Queue Monitor: *Queue Monitor*; carries `queueId`
- → `BO-006` Parking Configuration: *Parking Configuration*
- → `BO-002` Queue Configuration: *Cancels it and states the reason*; carries `performanceId`, `queueId`; calls `listPerformances`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The queue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the queue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No queue yet. Offers Create event (`createEvent`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, openOnly and the queue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `QUEUE_VIEW`, which `listQueues` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Unknown adaptor, or credentials missing for the selected adaptor; 400 Validation failed; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 409 The feed with this `id` belongs to a different queue. |

#### Permissions

- `listQueues` → `QUEUE_VIEW` (read) · staff, guest
- `listQueueFeeds` → `QUEUE_MANAGE` (configure) · staff
- `listPerformances` → `PRODUCT_VIEW` (read) · staff, guest
- `callNextParties` → `QUEUE_MANAGE` (configure) · staff
- `configureQueueFeed` → `QUEUE_MANAGE` (configure) · staff
- `createEvent` → `EVENT_CONFIGURE` (configure) · staff
- `createPerformances` → `PERFORMANCE_CONFIGURE` (configure) · staff
- `createQueue` → `QUEUE_MANAGE` (configure) · staff
- `getEvent` → `PRODUCT_VIEW` (read) · staff
- `getQueue` → `QUEUE_VIEW` (read) · staff
- `getQueueFeedHealth` → `QUEUE_MANAGE` (configure) · staff
- `getWaitTimes` → no permission · guest, public
- `listEvents` → `PRODUCT_VIEW` (read) · staff
- `listQueueEntries` → `QUEUE_VIEW` (read) · staff
- `setQueueStatus` → `QUEUE_MANAGE` (configure) · staff
- `setWaitTime` → `QUEUE_MANAGE` (configure) · staff
- `testQueueFeed` → `QUEUE_MANAGE` (configure) · staff
- `updateEvent` → `EVENT_CONFIGURE` (configure) · staff
- `updateQueue` → `QUEUE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `QUEUE_VIEW`, which `listQueues` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

37 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.34 | Time Slot Reservations - System shall support time slot reservations. | Guest Mobile App & Branding | CONTRACTED | `listPerformances` |
| 2.6.15 | - Time slots for events | Ticketing Sales | CONTRACTED | `listPerformances` |
| 2.7.16 | - Dedicated sales calendar | Ticketing Sales | CONTRACTED | `listPerformances` |
| 1.3.1 | The system should allow creation of events such as performances, workshops, activities or guided-tours. | Ticketing Catalogue | CONTRACTED | `createEvent` |
| 1.3.14 | Ability to create events with metadata (name, type, venue, date, time, organizer). The events could be free marketing, paid marketing events or show-tech events. | Ticketing Catalogue | CONTRACTED | `createEvent` |
| 1.3.29 | System shall support events spanning multiple venues, halls, spaces or locations under a single event. | Ticketing Catalogue | CONTRACTED | `createEvent` |
| 1.1.2 | The system should be able to sell dated tickets for attractions that allow access only for selected dates by guest. Special day tickets should also be supported. These are dated tickets that skip … | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.1.4 | The system should provide an easy-to-use interface for creation and configuration of timeslots. A calendar view should be available for the user to define the timeslot and recurrence rules. The user … | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.1.85 | Performance-based validity | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.1.86 | Performance date/time validity | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.3.2 | The system should allow configuration of event details such as start time (date & time), end time, duration of event, capacity (amount of places that can be sold for an event), seating categories … | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.3.3 | The system should support multiple occurrences/sessions, defined by a date, time, space, capacity and/or seating arrangement. | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| … 25 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- VQ configuration: rides enabled/disabled per day, queue/express split, target wait time and return-window duration, and handling of early or late arrivals at the ride's entry scanner. *(client request · MoM 7 Sep 2026, 4.13 Virtual Queue - Mobile Journey & Configuration · DI-676)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-001` · status **notStarted** · provenance generated
- Flow F09 *Event is cancelled and refunded*, step 1: Finds the performance → Sees what is sold and what it is worth
- ADR-0012 *Queue Integration — Adaptor-First, Vendor Deferred* (`docs/adr/0012-queue-integration-adaptor-first.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (80), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (97 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-001?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Call next parties, Configure queue feed, Create event, Create performances, Create queue, Save queue status, Save wait time, Test queue feed, Save event, Save queue.
- [ ] Every transition is wired: `BO-003`, `BO-004`, `BO-005`, `BO-006`, `BO-002`.
- [ ] Every gated control is gated: `EVENT_CONFIGURE`, `PERFORMANCE_CONFIGURE`, `PRODUCT_VIEW`, `QUEUE_MANAGE`, `QUEUE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-002` Queue Configuration

**Create a queue and set how it behaves.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `queue` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PERFORMANCE_CONFIGURE`, `PRODUCT_VIEW`, `QUEUE_MANAGE`, `QUEUE_VIEW` (2 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listQueueEntries` reads the population and `getPerformance` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `performanceId` (BO-001), `queueId` (BO-001) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/queue-management/queue-configuration` |

**What the spec says about it.** **Drawn 26 August** — `Seat Board 2.dc.html` frame `seat-2c`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Waiting · Called · Redeemed · Expired · No show · Cancelled · Released | — | Sends `?status=` to `listQueueEntries`. | `listQueueEntries` ?status |
| Name | text field | — | — | — | — | — | — |
| Attraction or resource | select field | — | — | — | — | — | — |
| Capacity per call | number field | — | — | — | — | — | — |
| Guests may join from the app | toggle | — | — | — | — | — | — |
| Redemption window (minutes) | number field | — | — | — | — | How long after being called before the entry expires | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Section code | text field | — | — | `getSeatAvailability` ?sectionCode |
| Category | picker: choose a category | — | — | `getSeatAvailability` ?categoryId |
| Available only | toggle | off | — | `getSeatAvailability` ?availableOnly |
| Mode | segmented control | Auto | Auto · Graphical · List | `getSeatAvailability` ?mode |
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |
| Open only | toggle | off | — | `listQueues` ?openOnly |

**Form: Create queue** (modal, opened by *Create queue*; *Create queue* calls `createQueue`, *Cancel* sends nothing)

**Collects what `createQueue` sends before it is called.** Required: `code`, `name`, `venueId`, `capacityPerCycle`, `cycleMinutes`. Optional: `attractionProductId`, `assetId`, `accessPointId`, `kind`, `operatingWindows`, `parentQueueId`, `loadBalanceWithQueueIds`, `inQueueOfferEnabled`, `notifyBeforeCallMinutes`, `maxPartySize`, `returnWindowMinutes`, `heightRequirementCm` and 2 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createQueue` body |
| Name `name` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createQueue` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createQueue` body |
| Attraction product `attractionProductId` | picker: choose an attraction product | optional | — | — | shows names, sends the id | — | `createQueue` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. | `createQueue` body |
| Access point `accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | — | `createQueue` body |
| Kind `kind` | select | optional | Standby | Standby · Single rider · Fast pass · Virtual · Accessible · Group only · Staff only | — | 5.6.x. A ride has several queues and the model had one. | `createQueue` body |
| Operating windows `operatingWindows` | repeatable rows | optional | — | — | — | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen. | `createQueue` body |
| Day `operatingWindows[].day` | select | required | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `createQueue` body |
| From `operatingWindows[].from` | time picker | required | — | — | HH:mm, 24-hour | Venue local time, 24-hour `HH:MM`, when the queue starts running. | `createQueue` body |
| To `operatingWindows[].to` | time picker | required | — | — | HH:mm, 24-hour | Venue local time, 24-hour `HH:MM`, when the queue stops running. | `createQueue` body |
| Last entry minutes before `operatingWindows[].lastEntryMinutesBefore` | number field (minutes) | optional | 0 | — | — | When the queue stops accepting, which is before it stops running. A guest joining two minutes before close waits twenty and is turned away at the front. | `createQueue` body |
| Parent queue `parentQueueId` | picker: choose a parent queue | optional | — | — | shows names, sends the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that is expressed without either queue … | `createQueue` body |
| Load balance with queues `loadBalanceWithQueueIds` | multi-picker: choose load balance with queues | optional | — | — | — | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. | `createQueue` body |
| In queue offer enabled `inQueueOfferEnabled` | toggle | optional | off | — | — | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. | `createQueue` body |
| Notify before call minutes `notifyBeforeCallMinutes` | number field (minutes) | optional | 5 | — | — | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line is visible. | `createQueue` body |
| Capacity per cycle `capacityPerCycle` | number field | required | — | min 1 | — | — | `createQueue` body |
| Cycle minutes `cycleMinutes` | number field (minutes) | required | — | min 0 | — | — | `createQueue` body |
| Max party size `maxPartySize` | number field | optional | 6 | — | — | — | `createQueue` body |
| Return window minutes `returnWindowMinutes` | number field (minutes) | optional | 15 | — | — | How long a called party has to arrive before the entry expires. | `createQueue` body |
| Height requirement cm `heightRequirementCm` | number field | optional | — | — | — | — | `createQueue` body |
| Fast pass allocation percent `fastPassAllocationPercent` | stepper or slider | optional | 0 | min 0; max 100 | — | Share of each cycle reserved for Fast Pass holders. | `createQueue` body |
| Zone `zone` | text field | optional | — | — | — | — | `createQueue` body |
| Fast pass `fastPass` | group | optional | — | — | — | The lane's Fast Pass block (decided 29 September, VM close-out). Null on a queue that takes no Fast Pass. | `createQueue` body |
| Entitlement products `fastPass.entitlementProductIds` | multi-picker: choose entitlement products | required | — | — | — | Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need. | `createQueue` body |
| Loyalty tiers `fastPass.loyaltyTierIds` | multi-picker: choose loyalty tiers | optional | — | — | — | 5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. | `createQueue` body |
| Promotions `fastPass.promotionIds` | multi-picker: choose promotions | optional | — | — | — | 5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. | `createQueue` body |
| Accessibility priority `fastPass.accessibilityPriority` | toggle | optional | off | — | — | 5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. | `createQueue` body |
| Return window minutes `fastPass.returnWindowMinutes` | number field (minutes) | optional | 60 | min 1; max 240 | — | How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan. | `createQueue` body |
| Max per guest per day `fastPass.maxPerGuestPerDay` | number field | optional | — | min 1 | — | Fast Pass redemptions one guest may make on this lane per day; null is no cap. | `createQueue` body |
| Allowed access points `fastPass.allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Access points that redeem Fast Pass for this lane; empty is the queue's own. | `createQueue` body |

Errors to draw in the form: 400 Validation failed

**Form: Save queue** (modal, opened by *Save queue*; *Save queue* calls `updateQueue`, *Cancel* sends nothing)

**Collects what `updateQueue` sends before it is called.** Nothing in the body is required. Optional: `name`, `capacityPerCycle`, `cycleMinutes`, `maxPartySize`, `returnWindowMinutes`, `heightRequirementCm`, `fastPassAllocationPercent`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | The same locale-to-text map `createQueue` takes and `Queue` returns, so an edit form round-trips the name. | `updateQueue` body |
| Capacity per cycle `capacityPerCycle` | number field | optional | — | min 1 | — | — | `updateQueue` body |
| Cycle minutes `cycleMinutes` | number field (minutes) | optional | — | min 0 | — | — | `updateQueue` body |
| Max party size `maxPartySize` | number field | optional | — | min 1 | — | — | `updateQueue` body |
| Return window minutes `returnWindowMinutes` | number field (minutes) | optional | — | min 1 | — | — | `updateQueue` body |
| Height requirement cm `heightRequirementCm` | number field | optional | — | — | — | — | `updateQueue` body |
| Fast pass allocation percent `fastPassAllocationPercent` | stepper or slider | optional | — | min 0; max 100 | — | — | `updateQueue` body |
| Fast pass `fastPass` | group | optional | — | — | — | The lane's Fast Pass block (decided 29 September, VM close-out). Replaces the whole block; null removes it. | `updateQueue` body |
| Entitlement products `fastPass.entitlementProductIds` | multi-picker: choose entitlement products | required | — | — | — | Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need. | `updateQueue` body |
| Loyalty tiers `fastPass.loyaltyTierIds` | multi-picker: choose loyalty tiers | optional | — | — | — | 5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. | `updateQueue` body |
| Promotions `fastPass.promotionIds` | multi-picker: choose promotions | optional | — | — | — | 5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. | `updateQueue` body |
| Accessibility priority `fastPass.accessibilityPriority` | toggle | optional | off | — | — | 5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. | `updateQueue` body |
| Return window minutes `fastPass.returnWindowMinutes` | number field (minutes) | optional | 60 | min 1; max 240 | — | How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan. | `updateQueue` body |
| Max per guest per day `fastPass.maxPerGuestPerDay` | number field | optional | — | min 1 | — | Fast Pass redemptions one guest may make on this lane per day; null is no cap. | `updateQueue` body |
| Allowed access points `fastPass.allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Access points that redeem Fast Pass for this lane; empty is the queue's own. | `updateQueue` body |

**Form: Call next parties** (modal, opened by *Call next parties*; *Call next parties* calls `callNextParties`, *Cancel* sends nothing)

**Collects what `callNextParties` sends before it is called.** Nothing in the body is required. Optional: `partyCount`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Party count `partyCount` | number field | optional | — | min 1 | — | Defaults to the queue's capacity per cycle. | `callNextParties` body |

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

**Form: Save queue status** (modal, opened by *Save queue status*; *Save queue status* calls `setQueueStatus`, *Cancel* sends nothing)

**Collects what `setQueueStatus` sends before it is called.** Required: `status`, `reason`. Optional: `guestMessage`, `expectedReopenAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | radio group | required | — | Open · Paused · Closed · At capacity | — | — | `setQueueStatus` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `setQueueStatus` body |
| Guest message `guestMessage` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setQueueStatus` body |
| Expected reopen at `expectedReopenAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setQueueStatus` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Save wait time** (modal, opened by *Save wait time*; *Save wait time* calls `setWaitTime`, *Cancel* sends nothing)

**Collects what `setWaitTime` sends before it is called.** Required: `waitMinutes`. Optional: `expiresInMinutes`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Wait minutes `waitMinutes` | number field (minutes) | required | — | min 0 | — | — | `setWaitTime` body |
| Expires in minutes `expiresInMinutes` | number field (minutes) | optional | 30 | min 1 | — | How long this manual figure stands before the queue reverts. | `setWaitTime` body |
| Note `note` | text area | optional | — | max length 200 | — | — | `setWaitTime` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

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

**Every waiting guest** (data table, from `listQueueEntries`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client-generated UUIDv7 from `JoinQueueRequest.id`, and the `entryId` every entry path takes. |
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Subject | the name it points at, never the id | — |
| Party number | 1,234 | What the guest sees and what appears on signage. |
| Party size | 1,234 | — |
| Status | chip: Waiting, Called, Redeemed, Expired, No show, Cancelled… | — |
| Position in queue | 1,234 | — |
| Parties ahead | 1,234 | — |
| Estimated call at | 1 Oct 2026, 14:30 | — |
| Is fast pass | yes / no (icon or chip) | — |
| Entitlement | text | — |

**Every queue** (data table, from `listQueues`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Venue | the name it points at, never the id | — |
| Attraction product | the name it points at, never the id | — |
| Asset | the image or video | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. |
| Access point | the name it points at, never the id | — |
| Kind | chip: Standby, Single rider, Fast pass, Virtual, Accessible, Group only… | 5.6.x. A ride has several queues and the model had one. |
| Operating windows | list or chips (count when long) | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for … |
| Parent queue | the name it points at, never the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that … |
| Load balance with queues | list or chips (count when long) | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. |
| In queue offer enabled | yes / no (icon or chip) | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. |
| Notify before call minutes | 1,234 | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line … |

**The selected waiting guest** (detail panel, from `listQueueEntries`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client-generated UUIDv7 from `JoinQueueRequest.id`, and the `entryId` every entry path takes. |
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Subject | the name it points at, never the id | — |
| Party number | 1,234 | What the guest sees and what appears on signage. |
| Party size | 1,234 | — |
| Status | chip: Waiting, Called, Redeemed, Expired, No show, Cancelled… | — |
| Position in queue | 1,234 | — |
| Parties ahead | 1,234 | — |
| Estimated call at | 1 Oct 2026, 14:30 | — |
| Is fast pass | yes / no (icon or chip) | — |
| Entitlement | text | — |
| Called at | 1 Oct 2026, 14:30 | — |
| Return window ends at | 1 Oct 2026, 14:30 | — |
| Redeemed at | 1 Oct 2026, 14:30 | — |
| Admitted count | 1,234 | — |

**The queue** (detail panel, from `getQueue`)

| Shows | Format | Notes |
|---|---|---|
| Now serving party number | 1,234 | — |
| Last called at | 1 Oct 2026, 14:30 | — |
| Throughput last hour | 1,234 | — |
| No show rate percent | 1,234.5 | — |
| Feed | grouped details | — |

**The seat availability** (detail panel, from `getSeatAvailability`)

| Shows | Format | Notes |
|---|---|---|
| Performance | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |
| Render mode | chip: Graphical, List | The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat … |
| Totals | grouped details | — |
| By category | list or chips (count when long) | — |
| Seats | list or chips (count when long) | — |

**The wait time** (detail panel, from `getWaitTimes`)

| Shows | Format | Notes |
|---|---|---|
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Attraction product | the name it points at, never the id | — |
| Attraction category | the name it points at, never the id | The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Source | chip: Sensor, Throughput, Manual, Unavailable | Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

**The performance** (detail panel, from `getPerformance`)

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create queue (primary button) | `createQueue` POST `/queues` | CreateQueueRequest | Queue | 400 Validation failed | opens modal first |
| Save queue (secondary button) | `updateQueue` PATCH `/queues/{queueId}` | inline | Queue | — | opens modal first |
| Cancel performance (destructive button) | `cancelPerformance` POST `/performances/{performanceId}/cancel` | inline | PerformanceCancellationResult | 403 The supervisor step-up is missing or failed (audit R144). The PIN did not verify, or the principal does not hold `PERFORMANCE_CONFIGURE` at this venue.; 409 The performance is `cancelled`, `completed` or `soldOut`. … | step-up: pin (Cancels a performance and queues refunds to every holder; a supervisor signs it in place (proposed by the coordinator …) |
| Call next parties (secondary button) | `callNextParties` POST `/queues/{queueId}/call-next` | inline | inline | — | opens modal first |
| Recommend seats (secondary button) | `recommendSeats` POST `/performances/{performanceId}/seat-recommendations` | SeatRecommendationRequest | inline | 404 No selection satisfies the constraints | opens modal first |
| Save queue status (secondary button) | `setQueueStatus` PUT `/queues/{queueId}/status` | inline | QueueStatusResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Save wait time (secondary button) | `setWaitTime` PUT `/queues/{queueId}/wait-time` | inline | WaitTime | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Save performance (secondary button) | `updatePerformance` PATCH `/performances/{performanceId}` | inline | Performance | 409 A timing change on a performance with sold tickets, or a `status` move the state model does not allow. | opens modal first |
| Save (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `getPerformance` (onLoad, Read a performance); `getQueue` (onLoad, Read a queue with live position); `getSeatAvailability` (onLoad, Seat status for a performance); `getWaitTimes` (onLoad, Wait times across a venue); `listQueueEntries` (onLoad, List entries in a queue); `listQueues` (onLoad, List queues)

**Where the user goes next**

- → `BO-023` Refunds & Exchanges: *Reviews the refund exposure*; calls `cancelPerformance`
- → `BO-001` Queue Directory: *Queue Directory*; carries `eventId`, `feedId`, `queueId`
- → `BO-003` Queue Integration Setup: *Queue Integration Setup*; carries `feedId`
- → `BO-004` Manual Wait Time Entry: *Manual Wait Time Entry*; carries `queueId`

**What opens over it**

- confirmDialog *Cancel performance*: **Names what `cancelPerformance` changes and what it leaves alone**, in the consequence rather than the verb. A queue this affects should be identified in the dialog, not just counted. **Collects what `cancelPerformance` sends before it is called.** Required: `reason`. Optional: `guestMessage` …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The queue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the queue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No queue yet. Offers Create queue (`createQueue`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status and the queue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `getPerformance` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A timing change on a performance with sold tickets, or a `status` move the state model does not allow.; 409 The performance is `cancelled`, `completed` or `soldOut`. `states/performance.yaml` cancels only from `scheduled`, `onSale` and `suspended`. |

#### Permissions

- `createQueue` → `QUEUE_MANAGE` (configure) · staff
- `updateQueue` → `QUEUE_MANAGE` (configure) · staff
- `cancelPerformance` → `PERFORMANCE_CONFIGURE` (configure) · staff · step-up pin
- `callNextParties` → `QUEUE_MANAGE` (configure) · staff
- `getPerformance` → `PRODUCT_VIEW` (read) · staff, guest
- `getQueue` → `QUEUE_VIEW` (read) · staff
- `getSeatAvailability` → `PRODUCT_VIEW` (read) · staff, guest
- `getWaitTimes` → no permission · guest, public
- `listQueueEntries` → `QUEUE_VIEW` (read) · staff
- `listQueues` → `QUEUE_VIEW` (read) · staff, guest
- `recommendSeats` → `PRODUCT_VIEW` (read) · staff, guest
- `setQueueStatus` → `QUEUE_MANAGE` (configure) · staff
- `setWaitTime` → `QUEUE_MANAGE` (configure) · staff
- `updatePerformance` → `PERFORMANCE_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `getPerformance` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

49 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.6.4 | VIP / Priority Handling: Separate or fast-track queues for premium guests. | F&B & Guest Management | CONTRACTED | `createQueue` |
| 5.6.7 | Support priority queueing for VIP guests, annual pass holders, premium packages, loyalty tiers, and accessibility requirements. | F&B & Guest Management | CONTRACTED_PARTIAL | `createQueue` |
| 5.6.12 | Automatically expire queue reservations after configurable grace periods. | F&B & Guest Management | CONTRACTED | `createQueue` |
| 1.3.20 | System shall support event cancellation workflows including refunds, exchanges, notifications and audit tracking. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.3.21 | System shall support changing event dates, times and venues while automatically updating tickets, reservations and guest communications. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.4.4 | The system should propagate any changes made to the properties of a product to the already sold tickets as well. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.4.16 | System shall identify affected tickets, reservations, memberships, events and integrations before applying product changes. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.3.15 | Define seating layouts, sections, pricing tiers, and total capacity. | Ticketing Catalogue | CONTRACTED | `getSeatAvailability` |
| 2.6.31 | Selling Event with a seat map, shared inventory with onsite sales. | Ticketing Sales | CONTRACTED | `getSeatAvailability` |
| 21.4.1 | Seat Status Management | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.2 | Seat Availability Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.3 | Seat Hold Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| … 37 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Qossai: walk-in, virtual-queue and VIP guests must be distinguished at the ride; VQ guests are never merged into the VIP line (would erode paid value); VQ arrivals need their own handling, e.g. a separate line or a QR scan within the arrival window. *(agreed · MoM 7 Sep 2026, 4.15 Virtual Queue - Three-Tier Guest Model · DI-678)*
- Allam: water-park guests rarely carry phones, so a kiosk at the ride lets a guest scan their wristband to book a queue slot and get a return time, then scan the wristband again to enter. *(agreed · MoM 7 Sep 2026, 4.14 Virtual Queue - Multi-Venue Applicability · DI-677)*
- VQ configuration: rides enabled/disabled per day, queue/express split, target wait time and return-window duration, and handling of early or late arrivals at the ride's entry scanner. *(client request · MoM 7 Sep 2026, 4.13 Virtual Queue - Mobile Journey & Configuration · DI-676)*
- Per-ride hourly capacity (e.g. 600/hour) split across express/fast-lane, virtual queue and walk-in (illustrative 75% general split walk-in/VQ, 25%/150 express); allocation adjusts dynamically if one lane is disproportionately busy. *(client request · MoM 7 Sep 2026, 4.12 Virtual Queue - Concept & Lane/Allocation Model · DI-674)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-002` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Seat Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/Seat Board 2.dc.html`
- Client design-board frames: `Seat Board 2.dc.html#seat-2c`
- Flow F09 *Event is cancelled and refunded*, step 2: Cancels it and states the reason → Sales stop immediately. Nothing new can be sold
- Flow F09 branch at step 2 (requiresStaff): when Performance is part of a bundle, The bundle component is cancelled and the rest stands. **A guest who bought ticket plus dinner plus parking loses the ticket, not the evening** — refunding the whole bundle takes money the venue kept …
- Flow F09 branch at step 2 (recoverable): when Fiscal period has closed over the original sale, The refund posts to the current period with a reference. It cannot post to a closed one — ADR on append-only.

#### Acceptance for the design

- [ ] Every input above is drawn (80), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (71 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-002?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create queue, Save queue, Cancel performance, Call next parties, Recommend seats, Save queue status, Save wait time, Save performance, Save.
- [ ] Every transition is wired: `BO-023`, `BO-001`, `BO-003`, `BO-004`.
- [ ] Every gated control is gated: `PERFORMANCE_CONFIGURE`, `PRODUCT_VIEW`, `QUEUE_MANAGE`, `QUEUE_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-003` Queue Integration Setup

**Connect a queue to an on-site system, or leave it on manual entry.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `queue` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `QUEUE_MANAGE` (1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listQueueFeeds` reads the population and `getQueueFeedHealth` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `feedId` (BO-001), `orderId` (deepLink), `venueId` (session) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/queue-management/queue-integration-setup` |

**What the spec says about it.** ADR-0012, adaptor-first. A named vendor is a driver behind a stable inbound shape, so adding one is configuration plus a driver rather than a core change. Vendor selection is CF-33a and deliberately late. **createRefund removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class). **Corrected 24 August**: removed applyManualDiscount, createOrder, exchangeOrderLines, getOrder, getOrderStatement, getRefundPolicy and 11 more. **A queue integration screen carried 15 order operations** — create an order, apply a discount, exchange lines, hold, refund — and four queue ones. Bulk-attach residue, and `requiresModule` was `ticketing` to match the operations rather than the screen. **Found by deriving the empty states.** `emptyNoAccess` came out reading *"needs `ORDER_CREATE` to create orders"* on a screen called Queue Integration Setup — **a generated sentence that was accurate to the data and absurd about the screen**, which is exactly what made it visible.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Adaptor | segmented control | optional | — | Generic · Mock · Vendor adaptor | — | **Follows the contract's `QueueFeedAdaptor`** — generic (the inbound API that sensor APIs, webhooks, MQTT, turnstile counts and cameras all post to), mock, or vendorAdaptor (with `adaptorName`) … | `QueueFeed.adaptor` |
| Endpoint or topic | text field | — | — | — | — | Shown for generic and vendorAdaptor feeds | — |
| Credential reference | text field | — | — | — | — | A key vault reference, never the secret. A secret typed into a form ends up in a screenshot | — |
| Expected interval (seconds) | number field | — | — | — | — | Drives the went-quiet alarm. Too tight and a duty manager learns to ignore it | — |
| Enabled | toggle | — | — | — | — | Disabled by default. A feed goes live only after a passing test | — |

**Form: Configure queue feed** (modal, opened by *Configure queue feed*; *Configure queue feed* calls `configureQueueFeed`, *Cancel* sends nothing)

**Collects what `configureQueueFeed` sends before it is called.** Required: `id`, `queueId`, `adaptor`, `isEnabled`. Optional: `adaptorName`, `credentialsRef`, `expectedIntervalSeconds`, `health`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `configureQueueFeed` body |
| Queue `queueId` | picker: choose a queue | required | — | — | shows names, sends the id | — | `configureQueueFeed` body |
| Adaptor `adaptor` | segmented control | required | — | Generic · Mock · Vendor adaptor | — | Vendor adaptors are bespoke work (ADR-0012). `generic` is the inbound API any system can post to; `mock` lets the feature be built and demonstrated with no vendor at all. | `configureQueueFeed` body |
| Adaptor name `adaptorName` | text field | optional | — | — | — | Named vendor where `adaptor` is `vendorAdaptor`. | `configureQueueFeed` body |
| Credentials ref `credentialsRef` | text field | optional | — | — | — | Key vault reference. Credentials are never returned. | `configureQueueFeed` body |
| Expected interval seconds `expectedIntervalSeconds` | number field (seconds) | optional | 60 | — | — | Beyond this without a reading, the feed is considered quiet. | `configureQueueFeed` body |
| Is enabled `isEnabled` | toggle | required | — | — | — | — | `configureQueueFeed` body |

Errors to draw in the form: 400 Unknown adaptor, or credentials missing for the selected adaptor; 409 The feed with this `id` belongs to a different queue.

#### Outputs: what the screen shows and produces

**Shown**

**Every queue feed** (data table, from `listQueueFeeds`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Queue | the name it points at, never the id | — |
| Adaptor | chip: Generic, Mock, Vendor adaptor | Vendor adaptors are bespoke work (ADR-0012). `generic` is the inbound API any system can post to; `mock` lets the feature be built and … |
| Adaptor name | text | Named vendor where `adaptor` is `vendorAdaptor`. |
| Credentials ref | text | Key vault reference. Credentials are never returned. |
| Expected interval seconds | 1,234 | Beyond this without a reading, the feed is considered quiet. |
| Is enabled | yes / no (icon or chip) | — |

**Detail panel** (detail panel): Five checks, plus the mapped sample reading and the raw payload. A source that is reachable and returns a shape nobody mapped looks like silence, not an error

**The selected queue feed** (detail panel, from `listQueueFeeds`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Queue | the name it points at, never the id | — |
| Adaptor | chip: Generic, Mock, Vendor adaptor | Vendor adaptors are bespoke work (ADR-0012). `generic` is the inbound API any system can post to; `mock` lets the feature be built and … |
| Adaptor name | text | Named vendor where `adaptor` is `vendorAdaptor`. |
| Credentials ref | text | Key vault reference. Credentials are never returned. |
| Expected interval seconds | 1,234 | Beyond this without a reading, the feed is considered quiet. |
| Is enabled | yes / no (icon or chip) | — |
| Health | grouped details | Whether the feed is currently reporting, computed on read — what `listQueueFeeds` promises per row. |

**The queue feed health** (detail panel, from `getQueueFeedHealth`)

| Shows | Format | Notes |
|---|---|---|
| Feed | the name it points at, never the id | — |
| Adaptor | chip: Generic, Mock, Vendor adaptor | Vendor adaptors are bespoke work (ADR-0012). `generic` is the inbound API any system can post to; `mock` lets the feature be built and … |
| Is healthy | yes / no (icon or chip) | Healthy means the last reading arrived within the feed's expected interval (decided 28 September, audit R106 (1)): `lastReadingAt` is no … |
| Is quiet | yes / no (icon or chip) | No reading within the expected interval. The wait time falls back to throughput-derived and is marked stale rather than freezing at the … |
| Last reading at | 1 Oct 2026, 14:30 | — |
| Expected interval seconds | 1,234 | The feed's `expectedIntervalSeconds` — the interval `isQuiet` is judged against, returned here so a health panel does not need the feed row … |
| Readings last hour | 1,234 | — |
| Discarded last hour | 1,234 | Out-of-order readings rejected in the last hour — rows of `queue.reading` for this feed with `disposition: discardedOutOfOrder`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Test connection (secondary button) | navigation or local | — | — | — | — |
| Configure queue feed (primary button) | `configureQueueFeed` PUT `/queue-feeds` | QueueFeed | QueueFeed | 400 Unknown adaptor, or credentials missing for the selected adaptor; 409 The feed with this `id` belongs to a different queue. | opens modal first |
| Test queue feed (secondary button) | `testQueueFeed` POST `/queue-feeds/{feedId}/test` | — | FeedTestResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Save (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `getQueueFeedHealth` (onLoad, Current feed state); `listQueueFeeds` (onLoad, List configured sensor feeds)

**Where the user goes next**

- → `BO-001` Queue Directory: *Queue Directory*; carries `feedId`, `queueId`
- → `BO-002` Queue Configuration: *Queue Configuration*; carries `queueId`
- → `BO-004` Manual Wait Time Entry: *Manual Wait Time Entry*; carries `queueId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The queue integration list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the queue integration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No queue integration yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listQueueFeeds` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `QUEUE_MANAGE`, which `getQueueFeedHealth` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Unknown adaptor, or credentials missing for the selected adaptor; 409 The feed with this `id` belongs to a different queue. |

#### Permissions

- `configureQueueFeed` → `QUEUE_MANAGE` (configure) · staff
- `testQueueFeed` → `QUEUE_MANAGE` (configure) · staff
- `getQueueFeedHealth` → `QUEUE_MANAGE` (configure) · staff
- `listQueueFeeds` → `QUEUE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `QUEUE_MANAGE`, which `getQueueFeedHealth` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Ride wait times come from the venue's sensor/camera counts via a live API (or a people count converted at a per-person rate) and are shown in the guest app; an AI "which ride to visit next" recommendation may follow. *(agreed · MoM 14 Aug 2026, 9. Queue Management · DI-299)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-003` · status **notStarted** · provenance generated
- ADR-0012 *Queue Integration — Adaptor-First, Vendor Deferred* (`docs/adr/0012-queue-integration-adaptor-first.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (23 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-003?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Test connection, Configure queue feed, Test queue feed, Save.
- [ ] Every transition is wired: `BO-001`, `BO-002`, `BO-004`.
- [ ] Every gated control is gated: `QUEUE_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-004` Manual Wait Time Entry

**Set a wait time by hand, whether or not a feed exists.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `queue` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_REFUND_APPROVE`, `ORDER_REFUND_BULK`, `QUEUE_MANAGE`, `QUEUE_VIEW` (2 operate, 1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | approvalInbox (compact density): `approveRefund` decides items that `listQueues` queues — every row is waiting for a person, so the empty state is success |
| Offline | online only |
| Opens with | `queueId` (BO-001), `refundId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/queue-management/manual-wait-time-entry` |

**What the spec says about it.** The screen the client asked for on 14 August. Available regardless of integration state — a venue with no sensors runs entirely from here, and a venue whose sensor failed falls back to it.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listQueues`. | `listQueues` ?venueId |
| Open only | toggle | optional | off | — | — | Sends `?openOnly=` to `listQueues`. | `listQueues` ?openOnly |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |
| Status | select | — | Waiting · Called · Redeemed · Expired · No show · Cancelled · Released | `listQueueEntries` ?status |

**Form: Save wait time** (modal, opened by *Save wait time*; *Save wait time* calls `setWaitTime`, *Cancel* sends nothing)

**Collects what `setWaitTime` sends before it is called.** Required: `waitMinutes`. Optional: `expiresInMinutes`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Wait minutes `waitMinutes` | number field (minutes) | required | — | min 0 | — | — | `setWaitTime` body |
| Expires in minutes `expiresInMinutes` | number field (minutes) | optional | 30 | min 1 | — | How long this manual figure stands before the queue reverts. | `setWaitTime` body |
| Note `note` | text area | optional | — | max length 200 | — | — | `setWaitTime` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Create bulk refund** (modal, opened by *Create bulk refund*; *Create bulk refund* calls `createBulkRefund`, *Cancel* sends nothing)

**Collects what `createBulkRefund` sends before it is called.** Required: `scope`, `reason`. Optional: `percentage`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scope `scope` | group | required | — | — | — | — | `createBulkRefund` body |
| Performance `scope.performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `createBulkRefund` body |
| Event `scope.eventId` | picker: choose an event | optional | — | — | shows names, sends the id | — | `createBulkRefund` body |
| Venue `scope.venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createBulkRefund` body |
| Date from `scope.dateFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createBulkRefund` body |
| Date to `scope.dateTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createBulkRefund` body |
| Percentage `percentage` | stepper or slider (%) | optional | 100 | min 0; max 100 | — | — | `createBulkRefund` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `createBulkRefund` body |

**Form: Approve refund** (modal, opened by *Approve refund*; *Approve refund* calls `approveRefund`, *Cancel* sends nothing)

**Collects what `approveRefund` sends before it is called.** Nothing in the body is required. Optional: `note`, `overridePercentage`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Note `note` | text area | optional | — | max length 500 | — | — | `approveRefund` body |
| Override percentage `overridePercentage` | stepper or slider | optional | — | min 0; max 100 | — | Approver may override the time-banded refund percentage. Recorded against the approving principal. | `approveRefund` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 409 The refund is not waiting for approval (`notPendingApproval`) — it was already approved, declined, completed or failed. (RefundPolicyProblem)

**Form: Call next parties** (modal, opened by *Call next parties*; *Call next parties* calls `callNextParties`, *Cancel* sends nothing)

**Collects what `callNextParties` sends before it is called.** Nothing in the body is required. Optional: `partyCount`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Party count `partyCount` | number field | optional | — | min 1 | — | Defaults to the queue's capacity per cycle. | `callNextParties` body |

**Form: Create queue** (modal, opened by *Create queue*; *Create queue* calls `createQueue`, *Cancel* sends nothing)

**Collects what `createQueue` sends before it is called.** Required: `code`, `name`, `venueId`, `capacityPerCycle`, `cycleMinutes`. Optional: `attractionProductId`, `assetId`, `accessPointId`, `kind`, `operatingWindows`, `parentQueueId`, `loadBalanceWithQueueIds`, `inQueueOfferEnabled`, `notifyBeforeCallMinutes`, `maxPartySize`, `returnWindowMinutes`, `heightRequirementCm` and 2 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createQueue` body |
| Name `name` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createQueue` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createQueue` body |
| Attraction product `attractionProductId` | picker: choose an attraction product | optional | — | — | shows names, sends the id | — | `createQueue` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. | `createQueue` body |
| Access point `accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | — | `createQueue` body |
| Kind `kind` | select | optional | Standby | Standby · Single rider · Fast pass · Virtual · Accessible · Group only · Staff only | — | 5.6.x. A ride has several queues and the model had one. | `createQueue` body |
| Operating windows `operatingWindows` | repeatable rows | optional | — | — | — | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen. | `createQueue` body |
| Day `operatingWindows[].day` | select | required | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `createQueue` body |
| From `operatingWindows[].from` | time picker | required | — | — | HH:mm, 24-hour | Venue local time, 24-hour `HH:MM`, when the queue starts running. | `createQueue` body |
| To `operatingWindows[].to` | time picker | required | — | — | HH:mm, 24-hour | Venue local time, 24-hour `HH:MM`, when the queue stops running. | `createQueue` body |
| Last entry minutes before `operatingWindows[].lastEntryMinutesBefore` | number field (minutes) | optional | 0 | — | — | When the queue stops accepting, which is before it stops running. A guest joining two minutes before close waits twenty and is turned away at the front. | `createQueue` body |
| Parent queue `parentQueueId` | picker: choose a parent queue | optional | — | — | shows names, sends the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that is expressed without either queue … | `createQueue` body |
| Load balance with queues `loadBalanceWithQueueIds` | multi-picker: choose load balance with queues | optional | — | — | — | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. | `createQueue` body |
| In queue offer enabled `inQueueOfferEnabled` | toggle | optional | off | — | — | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. | `createQueue` body |
| Notify before call minutes `notifyBeforeCallMinutes` | number field (minutes) | optional | 5 | — | — | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line is visible. | `createQueue` body |
| Capacity per cycle `capacityPerCycle` | number field | required | — | min 1 | — | — | `createQueue` body |
| Cycle minutes `cycleMinutes` | number field (minutes) | required | — | min 0 | — | — | `createQueue` body |
| Max party size `maxPartySize` | number field | optional | 6 | — | — | — | `createQueue` body |
| Return window minutes `returnWindowMinutes` | number field (minutes) | optional | 15 | — | — | How long a called party has to arrive before the entry expires. | `createQueue` body |
| Height requirement cm `heightRequirementCm` | number field | optional | — | — | — | — | `createQueue` body |
| Fast pass allocation percent `fastPassAllocationPercent` | stepper or slider | optional | 0 | min 0; max 100 | — | Share of each cycle reserved for Fast Pass holders. | `createQueue` body |
| Zone `zone` | text field | optional | — | — | — | — | `createQueue` body |
| Fast pass `fastPass` | group | optional | — | — | — | The lane's Fast Pass block (decided 29 September, VM close-out). Null on a queue that takes no Fast Pass. | `createQueue` body |
| Entitlement products `fastPass.entitlementProductIds` | multi-picker: choose entitlement products | required | — | — | — | Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need. | `createQueue` body |
| Loyalty tiers `fastPass.loyaltyTierIds` | multi-picker: choose loyalty tiers | optional | — | — | — | 5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. | `createQueue` body |
| Promotions `fastPass.promotionIds` | multi-picker: choose promotions | optional | — | — | — | 5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. | `createQueue` body |
| Accessibility priority `fastPass.accessibilityPriority` | toggle | optional | off | — | — | 5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. | `createQueue` body |
| Return window minutes `fastPass.returnWindowMinutes` | number field (minutes) | optional | 60 | min 1; max 240 | — | How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan. | `createQueue` body |
| Max per guest per day `fastPass.maxPerGuestPerDay` | number field | optional | — | min 1 | — | Fast Pass redemptions one guest may make on this lane per day; null is no cap. | `createQueue` body |
| Allowed access points `fastPass.allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Access points that redeem Fast Pass for this lane; empty is the queue's own. | `createQueue` body |

Errors to draw in the form: 400 Validation failed

**Form: Save queue status** (modal, opened by *Save queue status*; *Save queue status* calls `setQueueStatus`, *Cancel* sends nothing)

**Collects what `setQueueStatus` sends before it is called.** Required: `status`, `reason`. Optional: `guestMessage`, `expectedReopenAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | radio group | required | — | Open · Paused · Closed · At capacity | — | — | `setQueueStatus` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `setQueueStatus` body |
| Guest message `guestMessage` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setQueueStatus` body |
| Expected reopen at `expectedReopenAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setQueueStatus` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Save queue** (modal, opened by *Save queue*; *Save queue* calls `updateQueue`, *Cancel* sends nothing)

**Collects what `updateQueue` sends before it is called.** Nothing in the body is required. Optional: `name`, `capacityPerCycle`, `cycleMinutes`, `maxPartySize`, `returnWindowMinutes`, `heightRequirementCm`, `fastPassAllocationPercent`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | The same locale-to-text map `createQueue` takes and `Queue` returns, so an edit form round-trips the name. | `updateQueue` body |
| Capacity per cycle `capacityPerCycle` | number field | optional | — | min 1 | — | — | `updateQueue` body |
| Cycle minutes `cycleMinutes` | number field (minutes) | optional | — | min 0 | — | — | `updateQueue` body |
| Max party size `maxPartySize` | number field | optional | — | min 1 | — | — | `updateQueue` body |
| Return window minutes `returnWindowMinutes` | number field (minutes) | optional | — | min 1 | — | — | `updateQueue` body |
| Height requirement cm `heightRequirementCm` | number field | optional | — | — | — | — | `updateQueue` body |
| Fast pass allocation percent `fastPassAllocationPercent` | stepper or slider | optional | — | min 0; max 100 | — | — | `updateQueue` body |
| Fast pass `fastPass` | group | optional | — | — | — | The lane's Fast Pass block (decided 29 September, VM close-out). Replaces the whole block; null removes it. | `updateQueue` body |
| Entitlement products `fastPass.entitlementProductIds` | multi-picker: choose entitlement products | required | — | — | — | Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need. | `updateQueue` body |
| Loyalty tiers `fastPass.loyaltyTierIds` | multi-picker: choose loyalty tiers | optional | — | — | — | 5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. | `updateQueue` body |
| Promotions `fastPass.promotionIds` | multi-picker: choose promotions | optional | — | — | — | 5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. | `updateQueue` body |
| Accessibility priority `fastPass.accessibilityPriority` | toggle | optional | off | — | — | 5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. | `updateQueue` body |
| Return window minutes `fastPass.returnWindowMinutes` | number field (minutes) | optional | 60 | min 1; max 240 | — | How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan. | `updateQueue` body |
| Max per guest per day `fastPass.maxPerGuestPerDay` | number field | optional | — | min 1 | — | Fast Pass redemptions one guest may make on this lane per day; null is no cap. | `updateQueue` body |
| Allowed access points `fastPass.allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Access points that redeem Fast Pass for this lane; empty is the queue's own. | `updateQueue` body |

#### Outputs: what the screen shows and produces

**Shown**

**Waiting for a decision** (data table, from `listQueues`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Venue | the name it points at, never the id | — |
| Attraction product | the name it points at, never the id | — |
| Asset | the image or video | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. |
| Access point | the name it points at, never the id | — |
| Kind | chip: Standby, Single rider, Fast pass, Virtual, Accessible, Group only… | 5.6.x. A ride has several queues and the model had one. |
| Operating windows | list or chips (count when long) | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for … |
| Parent queue | the name it points at, never the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that … |
| Load balance with queues | list or chips (count when long) | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. |
| In queue offer enabled | yes / no (icon or chip) | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. |
| Notify before call minutes | 1,234 | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line … |

**Every waiting guest** (data table, from `listQueueEntries`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client-generated UUIDv7 from `JoinQueueRequest.id`, and the `entryId` every entry path takes. |
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Subject | the name it points at, never the id | — |
| Party number | 1,234 | What the guest sees and what appears on signage. |
| Party size | 1,234 | — |
| Status | chip: Waiting, Called, Redeemed, Expired, No show, Cancelled… | — |
| Position in queue | 1,234 | — |
| Parties ahead | 1,234 | — |
| Estimated call at | 1 Oct 2026, 14:30 | — |
| Is fast pass | yes / no (icon or chip) | — |
| Entitlement | text | — |

**Card list** (card list): One row per queue with a stepper and the current value

**Banner** (banner): Where a feed is live, a manual entry overrides it for a stated period and then reverts. A permanent silent override is how a broken sensor goes unnoticed for a season

**The selected queue** (detail panel, from `listQueues`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Venue | the name it points at, never the id | — |
| Attraction product | the name it points at, never the id | — |
| Asset | the image or video | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. |
| Access point | the name it points at, never the id | — |
| Kind | chip: Standby, Single rider, Fast pass, Virtual, Accessible, Group only… | 5.6.x. A ride has several queues and the model had one. |
| Operating windows | list or chips (count when long) | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for … |
| Parent queue | the name it points at, never the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that … |
| Load balance with queues | list or chips (count when long) | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. |
| In queue offer enabled | yes / no (icon or chip) | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. |
| Notify before call minutes | 1,234 | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line … |
| Capacity per cycle | 1,234 | — |
| Cycle minutes | 1,234.5 | — |
| Max party size | 1,234 | — |
| Return window minutes | 1,234 | How long a called party has to arrive before the entry expires. |

**The wait time** (detail panel, from `getWaitTimes`)

| Shows | Format | Notes |
|---|---|---|
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Attraction product | the name it points at, never the id | — |
| Attraction category | the name it points at, never the id | The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Source | chip: Sensor, Throughput, Manual, Unavailable | Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

**The queue** (detail panel, from `getQueue`)

| Shows | Format | Notes |
|---|---|---|
| Now serving party number | 1,234 | — |
| Last called at | 1 Oct 2026, 14:30 | — |
| Throughput last hour | 1,234 | — |
| No show rate percent | 1,234.5 | — |
| Feed | grouped details | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save wait time (primary button) | `setWaitTime` PUT `/queues/{queueId}/wait-time` | inline | WaitTime | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Create bulk refund (secondary button) | `createBulkRefund` POST `/refunds/bulk` | inline | RefundBatch | — | opens modal first |
| Approve refund (secondary button) | `approveRefund` POST `/refunds/{refundId}/approve` | inline | Refund | 403 Authenticated but not permitted at the requested scope; 409 The refund is not waiting for approval (`notPendingApproval`) — it was already approved, declined, completed or failed. (RefundPolicyProblem) | step-up: mfa (Money leaves. The one approval a compromised session is most obviously worth taking.); opens modal first |
| Call next parties (secondary button) | `callNextParties` POST `/queues/{queueId}/call-next` | inline | inline | — | opens modal first |
| Create queue (secondary button) | `createQueue` POST `/queues` | CreateQueueRequest | Queue | 400 Validation failed | opens modal first |
| Save queue status (secondary button) | `setQueueStatus` PUT `/queues/{queueId}/status` | inline | QueueStatusResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Save queue (secondary button) | `updateQueue` PATCH `/queues/{queueId}` | inline | Queue | — | opens modal first |
| Publish (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listQueues` (onLoad, Current values); `getQueue` (onLoad, Read a queue with live position); `getWaitTimes` (onLoad, Wait times across a venue); `listQueueEntries` (onLoad, List entries in a queue)

**Where the user goes next**

- → `BO-001` Queue Directory: *Queue Directory*; carries `feedId`, `queueId`
- → `BO-002` Queue Configuration: *Queue Configuration*; carries `queueId`
- → `BO-003` Queue Integration Setup: *Queue Integration Setup*; carries `feedId`
- → `BO-005` Queue Monitor: *Confirms guests were notified*; carries `queueId`; calls `createBulkRefund`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The manual wait time list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the manual wait time untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, openOnly and the manual wait time are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `QUEUE_VIEW`, which `listQueues` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The refund is not waiting for approval (`notPendingApproval`) — it was already approved, declined, completed or failed. (RefundPolicyProblem) |

#### Permissions

- `setWaitTime` → `QUEUE_MANAGE` (configure) · staff
- `listQueues` → `QUEUE_VIEW` (read) · staff, guest
- `createBulkRefund` → `ORDER_REFUND_BULK` (operate) · staff
- `approveRefund` → `ORDER_REFUND_APPROVE` (operate) · staff · step-up mfa
- `callNextParties` → `QUEUE_MANAGE` (configure) · staff
- `createQueue` → `QUEUE_MANAGE` (configure) · staff
- `getQueue` → `QUEUE_VIEW` (read) · staff
- `getWaitTimes` → no permission · guest, public
- `listQueueEntries` → `QUEUE_VIEW` (read) · staff
- `setQueueStatus` → `QUEUE_MANAGE` (configure) · staff
- `updateQueue` → `QUEUE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `QUEUE_VIEW`, which `listQueues` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

24 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.7.91 | The system shall support the complete refund lifecycle including refund request, approval, processing, settlement, completion, rejection, and cancellation. Track reason, approver, payment method … | F&B & Guest Management | CONTRACTED | `approveRefund` |
| 5.6.4 | VIP / Priority Handling: Separate or fast-track queues for premium guests. | F&B & Guest Management | CONTRACTED | `createQueue` |
| 5.6.7 | Support priority queueing for VIP guests, annual pass holders, premium packages, loyalty tiers, and accessibility requirements. | F&B & Guest Management | CONTRACTED_PARTIAL | `createQueue` |
| 5.6.12 | Automatically expire queue reservations after configurable grace periods. | F&B & Guest Management | CONTRACTED | `createQueue` |
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.2 | Real-time Queue Dashboard: Staff view of queue lengths, wait times, and customer flow. | F&B & Guest Management | CONTRACTED | `listQueueEntries` |
| 5.6.29 | Maintain complete audit logs for reservations, transfers, modifications, cancellations, and check-ins. | F&B & Guest Management | CONTRACTED | `listQueueEntries` |
| 5.6.24 | Automatically recover queue reservations after operational disruptions. | F&B & Guest Management | CONTRACTED | `setQueueStatus` |
| 5.6.25 | Support automatic queue suspension and guest reallocation when attractions become unavailable. | F&B & Guest Management | CONTRACTED | `setQueueStatus` |
| … 12 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Open: how per-ride occupancy is counted (entry sensors, manual security counts, CCTV/computer vision); Allam to check with Warner Bros. World, which has a visible wait-time display. Manual count entry stays a possible source. *(open · MoM 7 Sep 2026, 4.16 Wait-Time Calculation & People-Counting Technology · DI-680)*
- The client asked for a manual wait-time entry screen: set a wait time by hand whether or not a sensor feed exists; a venue with no sensors runs entirely from it and a failed sensor falls back to it. *(client request · MoM 14 Aug 2026, (cited in BO-004 notes) · DI-315)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-004` · status **notStarted** · provenance generated
- Flow F09 *Event is cancelled and refunded*, step 4: Authorises the bulk refund → Refunds queue against the original payment method
- Flow F09 branch at step 4 (requiresStaff): when Original payment method no longer valid, Refund fails and falls to a manual queue. Card expired, account closed. This is common at scale and needs a person.
- Flow F09 branch at step 4 (requiresStaff): when Some tickets already scanned, Partial performance — a show abandoned at the interval. **Refund policy differs from a full cancellation** and the split is a decision, not a rule.
- Flow F09 branch at step 4 (recoverable): when Seats were sold, Seats return to available. If the performance is rescheduled rather than cancelled they must be held, and the two paths diverge here.
- Flow F09 branch at step 4 (requiresStaff): when Entitlement is redeemable at another venue, Cross-cell. The redemption right must be revoked in the other cell too, and that cell may be unreachable.

#### Acceptance for the design

- [ ] Every input above is drawn (66), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (56 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-004?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save wait time, Create bulk refund, Approve refund, Call next parties, Create queue, Save queue status, Save queue, Publish.
- [ ] Every transition is wired: `BO-001`, `BO-002`, `BO-003`, `BO-005`.
- [ ] Every gated control is gated: `ORDER_REFUND_APPROVE`, `ORDER_REFUND_BULK`, `QUEUE_MANAGE`, `QUEUE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-005` Queue Monitor

**Watch queues during operation and call parties forward.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `marketing` module |
| Block | Block A · ticket #20777 (APP-SETUP-BO-005) |
| Who uses it | venue staff holding `AI_USE`, `MARKETING_MANAGE`, `MARKETING_SEND`, `MARKETING_VIEW`, `QUEUE_MANAGE`, `QUEUE_VIEW`… (3 operate, 2 configure, 2 read); in the flows as guest, venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listQueueEntries` reads the population and `getWaitTimes` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `campaignId` (deepLink), `queueId` (BO-001) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/queue-management/queue-monitor` |

**What the spec says about it.** Pulled to Wave 1 on 17 August (CF-101): F09 closes a cancelled event’s queue, and a Wave 1 flow cannot step through a Wave 2 screen. **Cross-platform navigation removed 24 August**: EMP-032. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Waiting · Called · Redeemed · Expired · No show · Cancelled · Released | — | Sends `?status=` to `listQueueEntries`. | `listQueueEntries` ?status |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Status | select | — | Draft · Scheduled · Sending · Paused · Completed · Stopped · Failed | `listCampaigns` ?status |
| Open only | toggle | off | — | `listQueues` ?openOnly |

**Form: Call next parties** (modal, opened by *Call next parties*; *Call next parties* calls `callNextParties`, *Cancel* sends nothing)

**Collects what `callNextParties` sends before it is called.** Nothing in the body is required. Optional: `partyCount`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Party count `partyCount` | number field | optional | — | min 1 | — | Defaults to the queue's capacity per cycle. | `callNextParties` body |

**Form: Create campaign** (modal, opened by *Create campaign*; *Create campaign* calls `createCampaign`, *Cancel* sends nothing)

**Collects what `createCampaign` sends before it is called.** Required: `name`, `kind`, `channel`, `segmentId`, `content`. Optional: `venueId`, `trigger`, `scheduledFor`, `consentPurpose`, `sendWindow`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `createCampaign` body |
| Kind `kind` | radio group | required | — | One off · Scheduled · Triggered · Recurring | — | — | `createCampaign` body |
| Channel `channel` | select | required | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `createCampaign` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createCampaign` body |
| Segment `segmentId` | picker: choose a segment | required | — | — | shows names, sends the id | — | `createCampaign` body |
| Content `content` | group | required | — | — | — | — | `createCampaign` body |
| Template `content.templateId` | picker: choose a template | required | — | — | shows names, sends the id | — | `createCampaign` body |
| Subject override `content.subjectOverride` | key and value settings | optional | — | — | — | — | `createCampaign` body |
| Merge defaults `content.mergeDefaults` | key and value settings | optional | — | — | — | Fallback values for the template's `mergeFields`, by name, used where a guest has no value. | `createCampaign` body |
| Promotion `content.promotionId` | picker: choose a promotion | optional | — | — | shows names, sends the id | Offer carried by the campaign. Coupon codes are issued from it. | `createCampaign` body |
| Trigger `trigger` | group | optional | — | — | — | — | `createCampaign` body |
| Event `trigger.event` | select | optional | — | Booking confirmed · Visit completed · Membership expiring · Birthday · Abandoned cart · First visit · Inactivity · Entitlement expiring | — | `entitlementExpiring` (29 September, build pass, group G2; 5.5.30) fires on `entitlement.expiringSoon`: a ticket or pass the guest still holds comes within its template's … | `createCampaign` body |
| Delay hours `trigger.delayHours` | number field (hours) | optional | — | — | — | — | `createCampaign` body |
| Conditions `trigger.conditions` | repeatable rows | optional | — | — | — | — | `createCampaign` body |
| Attribute `trigger.conditions[].attribute` | text field | required | — | — | — | Behavioural or profile attribute — visit count, last visit, lifetime value, product purchased, membership tier, venue visited, language. | `createCampaign` body |
| Operator `trigger.conditions[].operator` | select | required | — | Equals · Not equals · Greater than · Less than · Between · In · Not in · Exists · Not exists · Within days | — | — | `createCampaign` body |
| Value `trigger.conditions[].value` | field | optional | — | — | — | — | `createCampaign` body |
| Values `trigger.conditions[].values` | list of values (chips) | optional | — | — | — | — | `createCampaign` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCampaign` body |
| Consent purpose `consentPurpose` | select | optional | Marketing | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | — | — | `createCampaign` body |
| Send window `sendWindow` | group | optional | — | — | — | Hours during which sending is permitted. A promotional message at 3am is a complaint waiting to happen. | `createCampaign` body |
| Start time `sendWindow.startTime` | text field | optional | — | — | — | — | `createCampaign` body |
| End time `sendWindow.endTime` | text field | optional | — | — | — | — | `createCampaign` body |
| Time zone `sendWindow.timeZone` | text field | optional | — | — | — | — | `createCampaign` body |
| Send time mode `sendTimeMode` | segmented control | optional | Fixed | Fixed · Optimised | — | `optimised` sends each recipient at the hour `ai.requestSuggestion` (kind `sendTime`) gives for them, inside `sendWindow` (29 September, build pass, group G2; 22.3.19). | `createCampaign` body |
| Optimise channel `optimiseChannel` | toggle | optional | off | — | — | With `sendTimeMode` `optimised`, route each recipient to the channel the suggestion names, among the channels they consented to (22.9.16). | `createCampaign` body |
| Variants `variants` | repeatable rows | optional | — | at most 5 | — | A/B (or up to five-way) content and subject variants (29 September, build pass, group G2; 22.1.17, BO-772). | `createCampaign` body |
| Label `variants[].label` | text field | required | — | max length 20 | — | A, B, C... | `createCampaign` body |
| Subject override `variants[].subjectOverride` | key and value settings | optional | — | — | — | Subject line by locale. | `createCampaign` body |
| Template `variants[].templateId` | picker: choose a template | optional | — | — | shows names, sends the id | A different template for this variant; null uses the campaign's `content.templateId`. | `createCampaign` body |
| Split percent `variants[].splitPercent` | stepper or slider | optional | — | min 1; max 100 | — | Share of the test group; null splits evenly. | `createCampaign` body |
| Source `variants[].source` | segmented control | optional | Manual | Manual · AI draft | — | — | `createCampaign` body |
| AI decision record `variants[].aiDecisionRecordId` | text field | optional | — | — | — | The decision record of the `ai.proposeMarketingContent` draft it came from, for `aiDraft`. | `createCampaign` body |
| Ab test `abTest` | group | optional | — | Required when `variants` has two or more. | — | How the variants are tested. Required when `variants` has two or more. | `createCampaign` body |
| Test percent `abTest.testPercent` | stepper or slider | optional | 20 | min 5; max 100 | — | Share of the audience the variants are tested on; 100 splits everyone and picks no winner. | `createCampaign` body |
| Success metric `abTest.successMetric` | radio group | optional | Click rate | Open rate · Click rate · Conversion rate · Attributed revenue | — | — | `createCampaign` body |
| Decide after hours `abTest.decideAfterHours` | number field (hours) | optional | 4 | min 1; max 168 | — | — | `createCampaign` body |
| Winner rule `abTest.winnerRule` | segmented control | optional | Automatic | Automatic · Manual | — | — | `createCampaign` body |
| Minimum sample per variant `abTest.minimumSamplePerVariant` | number field | optional | 500 | min 1 | — | Below this many sends per variant no winner is declared automatically; a person picks. | `createCampaign` body |
| Winning variant `abTest.winningVariantId` | picker: choose a winning variant | optional | — | — | shows names, sends the id | Set by the automatic rule, or by a person through `updateCampaign`. | `createCampaign` body |

Errors to draw in the form: 400 Validation failed

**Form: Create queue** (modal, opened by *Create queue*; *Create queue* calls `createQueue`, *Cancel* sends nothing)

**Collects what `createQueue` sends before it is called.** Required: `code`, `name`, `venueId`, `capacityPerCycle`, `cycleMinutes`. Optional: `attractionProductId`, `assetId`, `accessPointId`, `kind`, `operatingWindows`, `parentQueueId`, `loadBalanceWithQueueIds`, `inQueueOfferEnabled`, `notifyBeforeCallMinutes`, `maxPartySize`, `returnWindowMinutes`, `heightRequirementCm` and 2 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createQueue` body |
| Name `name` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createQueue` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createQueue` body |
| Attraction product `attractionProductId` | picker: choose an attraction product | optional | — | — | shows names, sends the id | — | `createQueue` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. | `createQueue` body |
| Access point `accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | — | `createQueue` body |
| Kind `kind` | select | optional | Standby | Standby · Single rider · Fast pass · Virtual · Accessible · Group only · Staff only | — | 5.6.x. A ride has several queues and the model had one. | `createQueue` body |
| Operating windows `operatingWindows` | repeatable rows | optional | — | — | — | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen. | `createQueue` body |
| Day `operatingWindows[].day` | select | required | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `createQueue` body |
| From `operatingWindows[].from` | time picker | required | — | — | HH:mm, 24-hour | Venue local time, 24-hour `HH:MM`, when the queue starts running. | `createQueue` body |
| To `operatingWindows[].to` | time picker | required | — | — | HH:mm, 24-hour | Venue local time, 24-hour `HH:MM`, when the queue stops running. | `createQueue` body |
| Last entry minutes before `operatingWindows[].lastEntryMinutesBefore` | number field (minutes) | optional | 0 | — | — | When the queue stops accepting, which is before it stops running. A guest joining two minutes before close waits twenty and is turned away at the front. | `createQueue` body |
| Parent queue `parentQueueId` | picker: choose a parent queue | optional | — | — | shows names, sends the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that is expressed without either queue … | `createQueue` body |
| Load balance with queues `loadBalanceWithQueueIds` | multi-picker: choose load balance with queues | optional | — | — | — | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. | `createQueue` body |
| In queue offer enabled `inQueueOfferEnabled` | toggle | optional | off | — | — | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. | `createQueue` body |
| Notify before call minutes `notifyBeforeCallMinutes` | number field (minutes) | optional | 5 | — | — | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line is visible. | `createQueue` body |
| Capacity per cycle `capacityPerCycle` | number field | required | — | min 1 | — | — | `createQueue` body |
| Cycle minutes `cycleMinutes` | number field (minutes) | required | — | min 0 | — | — | `createQueue` body |
| Max party size `maxPartySize` | number field | optional | 6 | — | — | — | `createQueue` body |
| Return window minutes `returnWindowMinutes` | number field (minutes) | optional | 15 | — | — | How long a called party has to arrive before the entry expires. | `createQueue` body |
| Height requirement cm `heightRequirementCm` | number field | optional | — | — | — | — | `createQueue` body |
| Fast pass allocation percent `fastPassAllocationPercent` | stepper or slider | optional | 0 | min 0; max 100 | — | Share of each cycle reserved for Fast Pass holders. | `createQueue` body |
| Zone `zone` | text field | optional | — | — | — | — | `createQueue` body |
| Fast pass `fastPass` | group | optional | — | — | — | The lane's Fast Pass block (decided 29 September, VM close-out). Null on a queue that takes no Fast Pass. | `createQueue` body |
| Entitlement products `fastPass.entitlementProductIds` | multi-picker: choose entitlement products | required | — | — | — | Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need. | `createQueue` body |
| Loyalty tiers `fastPass.loyaltyTierIds` | multi-picker: choose loyalty tiers | optional | — | — | — | 5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. | `createQueue` body |
| Promotions `fastPass.promotionIds` | multi-picker: choose promotions | optional | — | — | — | 5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. | `createQueue` body |
| Accessibility priority `fastPass.accessibilityPriority` | toggle | optional | off | — | — | 5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. | `createQueue` body |
| Return window minutes `fastPass.returnWindowMinutes` | number field (minutes) | optional | 60 | min 1; max 240 | — | How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan. | `createQueue` body |
| Max per guest per day `fastPass.maxPerGuestPerDay` | number field | optional | — | min 1 | — | Fast Pass redemptions one guest may make on this lane per day; null is no cap. | `createQueue` body |
| Allowed access points `fastPass.allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Access points that redeem Fast Pass for this lane; empty is the queue's own. | `createQueue` body |

Errors to draw in the form: 400 Validation failed

**Form: Launch campaign** (modal, opened by *Launch campaign*; *Launch campaign* calls `launchCampaign`, *Cancel* sends nothing)

**Collects what `launchCampaign` sends before it is called.** Nothing in the body is required. Optional: `scheduledFor`, `confirmAudienceSize`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `launchCampaign` body |
| Confirm audience size `confirmAudienceSize` | number field | optional | — | When supplied and the evaluated size differs beyond tolerance, the launch is refused. | — | Guard against a segment that has grown unexpectedly. When supplied and the evaluated size differs beyond tolerance, the launch is refused. | `launchCampaign` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 409 Already launched (`alreadyLaunched`), audience size differs beyond tolerance (`audienceSizeChanged`), or every recipient was excluded (`noReachableRecipients`). (CampaignStateProblem)

**Form: Pause campaign** (modal, opened by *Pause campaign*; *Pause campaign* calls `pauseCampaign`, *Cancel* sends nothing)

**Collects what `pauseCampaign` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `pauseCampaign` body |

Errors to draw in the form: 409 The campaign is not `sending` (`statusDoesNotPermit`). (CampaignStateProblem)

**Form: Save queue status** (modal, opened by *Save queue status*; *Save queue status* calls `setQueueStatus`, *Cancel* sends nothing)

**Collects what `setQueueStatus` sends before it is called.** Required: `status`, `reason`. Optional: `guestMessage`, `expectedReopenAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | radio group | required | — | Open · Paused · Closed · At capacity | — | — | `setQueueStatus` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `setQueueStatus` body |
| Guest message `guestMessage` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setQueueStatus` body |
| Expected reopen at `expectedReopenAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setQueueStatus` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Save wait time** (modal, opened by *Save wait time*; *Save wait time* calls `setWaitTime`, *Cancel* sends nothing)

**Collects what `setWaitTime` sends before it is called.** Required: `waitMinutes`. Optional: `expiresInMinutes`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Wait minutes `waitMinutes` | number field (minutes) | required | — | min 0 | — | — | `setWaitTime` body |
| Expires in minutes `expiresInMinutes` | number field (minutes) | optional | 30 | min 1 | — | How long this manual figure stands before the queue reverts. | `setWaitTime` body |
| Note `note` | text area | optional | — | max length 200 | — | — | `setWaitTime` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Test send campaign** (modal, opened by *Test send campaign*; *Test send campaign* calls `testSendCampaign`, *Cancel* sends nothing)

**Collects what `testSendCampaign` sends before it is called.** Required: `recipients`. Optional: `sampleSubjectId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recipients `recipients` | list of values (chips) | required | — | at least 1; at most 10 | — | — | `testSendCampaign` body |
| Sample subject `sampleSubjectId` | picker: choose a sample subject | optional | — | — | shows names, sends the id | Personalise using this guest's data. Otherwise placeholders are used. | `testSendCampaign` body |

**Form: Save campaign** (modal, opened by *Save campaign*; *Save campaign* calls `updateCampaign`, *Cancel* sends nothing)

**Collects what `updateCampaign` sends before it is called.** Nothing in the body is required. Optional: `name`, `isPaused`, `scheduledFor`, `content`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateCampaign` body |
| Is paused `isPaused` | toggle | optional | — | — | — | — | `updateCampaign` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateCampaign` body |
| Content `content` | group | optional | — | — | — | — | `updateCampaign` body |
| Template `content.templateId` | picker: choose a template | required | — | — | shows names, sends the id | — | `updateCampaign` body |
| Subject override `content.subjectOverride` | key and value settings | optional | — | — | — | — | `updateCampaign` body |
| Merge defaults `content.mergeDefaults` | key and value settings | optional | — | — | — | Fallback values for the template's `mergeFields`, by name, used where a guest has no value. | `updateCampaign` body |
| Promotion `content.promotionId` | picker: choose a promotion | optional | — | — | shows names, sends the id | Offer carried by the campaign. Coupon codes are issued from it. | `updateCampaign` body |

Errors to draw in the form: 409 `content` amended on a campaign that is no longer in `draft` (`statusDoesNotPermit`). (CampaignStateProblem)

**Form: Save queue** (modal, opened by *Save queue*; *Save queue* calls `updateQueue`, *Cancel* sends nothing)

**Collects what `updateQueue` sends before it is called.** Nothing in the body is required. Optional: `name`, `capacityPerCycle`, `cycleMinutes`, `maxPartySize`, `returnWindowMinutes`, `heightRequirementCm`, `fastPassAllocationPercent`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | The same locale-to-text map `createQueue` takes and `Queue` returns, so an edit form round-trips the name. | `updateQueue` body |
| Capacity per cycle `capacityPerCycle` | number field | optional | — | min 1 | — | — | `updateQueue` body |
| Cycle minutes `cycleMinutes` | number field (minutes) | optional | — | min 0 | — | — | `updateQueue` body |
| Max party size `maxPartySize` | number field | optional | — | min 1 | — | — | `updateQueue` body |
| Return window minutes `returnWindowMinutes` | number field (minutes) | optional | — | min 1 | — | — | `updateQueue` body |
| Height requirement cm `heightRequirementCm` | number field | optional | — | — | — | — | `updateQueue` body |
| Fast pass allocation percent `fastPassAllocationPercent` | stepper or slider | optional | — | min 0; max 100 | — | — | `updateQueue` body |
| Fast pass `fastPass` | group | optional | — | — | — | The lane's Fast Pass block (decided 29 September, VM close-out). Replaces the whole block; null removes it. | `updateQueue` body |
| Entitlement products `fastPass.entitlementProductIds` | multi-picker: choose entitlement products | required | — | — | — | Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need. | `updateQueue` body |
| Loyalty tiers `fastPass.loyaltyTierIds` | multi-picker: choose loyalty tiers | optional | — | — | — | 5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. | `updateQueue` body |
| Promotions `fastPass.promotionIds` | multi-picker: choose promotions | optional | — | — | — | 5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. | `updateQueue` body |
| Accessibility priority `fastPass.accessibilityPriority` | toggle | optional | off | — | — | 5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. | `updateQueue` body |
| Return window minutes `fastPass.returnWindowMinutes` | number field (minutes) | optional | 60 | min 1; max 240 | — | How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan. | `updateQueue` body |
| Max per guest per day `fastPass.maxPerGuestPerDay` | number field | optional | — | min 1 | — | Fast Pass redemptions one guest may make on this lane per day; null is no cap. | `updateQueue` body |
| Allowed access points `fastPass.allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Access points that redeem Fast Pass for this lane; empty is the queue's own. | `updateQueue` body |

**Sent by *Stop campaign*** (`stopCampaign`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `stopCampaign` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every waiting guest** (data table, from `listQueueEntries`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client-generated UUIDv7 from `JoinQueueRequest.id`, and the `entryId` every entry path takes. |
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Subject | the name it points at, never the id | — |
| Party number | 1,234 | What the guest sees and what appears on signage. |
| Party size | 1,234 | — |
| Status | chip: Waiting, Called, Redeemed, Expired, No show, Cancelled… | — |
| Position in queue | 1,234 | — |
| Parties ahead | 1,234 | — |
| Estimated call at | 1 Oct 2026, 14:30 | — |
| Is fast pass | yes / no (icon or chip) | — |
| Entitlement | text | — |

**Every campaign** (data table, from `listCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: One off, Scheduled, Triggered, Recurring | — |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Venue | the name it points at, never the id | — |
| Segment | the name it points at, never the id | — |
| Content | grouped details | — |
| Trigger | grouped details | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Consent purpose | chip: Marketing, Personalisation, Profiling, Third party sharing, AI processing … | — |
| Send window | grouped details | Hours during which sending is permitted. A promotional message at 3am is a complaint waiting to happen. |
| ID | the name it points at, never the id | — |
| Budget cap | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Every queue** (data table, from `listQueues`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Venue | the name it points at, never the id | — |
| Attraction product | the name it points at, never the id | — |
| Asset | the image or video | The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running. |
| Access point | the name it points at, never the id | — |
| Kind | chip: Standby, Single rider, Fast pass, Virtual, Accessible, Group only… | 5.6.x. A ride has several queues and the model had one. |
| Operating windows | list or chips (count when long) | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for … |
| Parent queue | the name it points at, never the id | Where several queues share one capacity. The standby and single-rider lines at one ride draw from the same cycles, and a parent is how that … |
| Load balance with queues | list or chips (count when long) | BL-137. Two rides with the same theme and different waits, and nothing directed a guest to the shorter one. |
| In queue offer enabled | yes / no (icon or chip) | A guest with twenty minutes to wait is a guest with twenty minutes to buy something. |
| Notify before call minutes | 1,234 | BL-017, 19.2.61. A guest was not told their turn was approaching, which makes a virtual queue worse than a physical one — at least a line … |

**Metric tile** (metric tile): Waiting, called, expired, average wait

**Takings and admissions today** (metric tile, from `getKpiValues`): **Takings and admissions**, from `getKpiValues?kpiCodes=takings,admissions`; with no `period` the period is today in the venue's time zone (decided 28 September, audit R283).

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Period | text | — |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Chart** (chart): Wait over the day. Stale where the feed has gone quiet

**The selected waiting guest** (detail panel, from `listQueueEntries`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client-generated UUIDv7 from `JoinQueueRequest.id`, and the `entryId` every entry path takes. |
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Subject | the name it points at, never the id | — |
| Party number | 1,234 | What the guest sees and what appears on signage. |
| Party size | 1,234 | — |
| Status | chip: Waiting, Called, Redeemed, Expired, No show, Cancelled… | — |
| Position in queue | 1,234 | — |
| Parties ahead | 1,234 | — |
| Estimated call at | 1 Oct 2026, 14:30 | — |
| Is fast pass | yes / no (icon or chip) | — |
| Entitlement | text | — |
| Called at | 1 Oct 2026, 14:30 | — |
| Return window ends at | 1 Oct 2026, 14:30 | — |
| Redeemed at | 1 Oct 2026, 14:30 | — |
| Admitted count | 1,234 | — |

**The campaign** (detail panel, from `getCampaign`)

| Shows | Format | Notes |
|---|---|---|
| Performance | grouped details | — |

**The campaign performance** (detail panel, from `getCampaignPerformance`)

| Shows | Format | Notes |
|---|---|---|
| Campaign | the name it points at, never the id | — |
| Sent | 1,234 | — |
| Delivered | 1,234 | — |
| Opened | 1,234 | — |
| Clicked | 1,234 | — |
| Bounced | 1,234 | — |
| Complained | 1,234 | — |
| Unsubscribed | 1,234 | — |
| Attributed orders | 1,234 | — |
| Attributed revenue | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Attribution window days | 1,234 | The window these figures were attributed over, from `VenueSettings.marketing.attributionWindowDays` (proposed default 7, audit R094). |

**The queue** (detail panel, from `getQueue`)

| Shows | Format | Notes |
|---|---|---|
| Now serving party number | 1,234 | — |
| Last called at | 1 Oct 2026, 14:30 | — |
| Throughput last hour | 1,234 | — |
| No show rate percent | 1,234.5 | — |
| Feed | grouped details | — |

**The wait time** (detail panel, from `getWaitTimes`)

| Shows | Format | Notes |
|---|---|---|
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Attraction product | the name it points at, never the id | — |
| Attraction category | the name it points at, never the id | The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Source | chip: Sensor, Throughput, Manual, Unavailable | Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Call next parties (primary button) | `callNextParties` POST `/queues/{queueId}/call-next` | inline | inline | — | opens modal first |
| Create campaign (secondary button) | `createCampaign` POST `/campaigns` | CreateCampaignRequest | Campaign | 400 Validation failed | opens modal first |
| Create queue (secondary button) | `createQueue` POST `/queues` | CreateQueueRequest | Queue | 400 Validation failed | opens modal first |
| Launch campaign (secondary button) | `launchCampaign` POST `/campaigns/{campaignId}/launch` | inline | LaunchResult | 403 Authenticated but not permitted at the requested scope; 409 Already launched (`alreadyLaunched`), audience size differs beyond tolerance (`audienceSizeChanged`), or every recipient was excluded … | opens modal first |
| Pause campaign (secondary button) | `pauseCampaign` POST `/campaigns/{campaignId}/pause` | inline | Campaign | 409 The campaign is not `sending` (`statusDoesNotPermit`). (CampaignStateProblem) | opens modal first |
| Save queue status (secondary button) | `setQueueStatus` PUT `/queues/{queueId}/status` | inline | QueueStatusResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Save wait time (secondary button) | `setWaitTime` PUT `/queues/{queueId}/wait-time` | inline | WaitTime | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Stop campaign (destructive button) | `stopCampaign` POST `/campaigns/{campaignId}/stop` | inline | Campaign | 409 The campaign is not `sending` or `paused` (`statusDoesNotPermit`). (CampaignStateProblem) | — |
| Test send campaign (secondary button) | `testSendCampaign` POST `/campaigns/{campaignId}/test-send` | inline | inline | — | opens modal first |
| Unschedule campaign (secondary button) | `unscheduleCampaign` POST `/campaigns/{campaignId}/unschedule` | — | Campaign | 409 The campaign is not `scheduled` (`statusDoesNotPermit`) — once it is sending, it is paused or stopped instead. (CampaignStateProblem) | — |
| Save campaign (secondary button) | `updateCampaign` PATCH `/campaigns/{campaignId}` | inline | Campaign | 409 `content` amended on a campaign that is no longer in `draft` (`statusDoesNotPermit`). (CampaignStateProblem) | opens modal first |
| Save queue (secondary button) | `updateQueue` PATCH `/queues/{queueId}` | inline | Queue | — | opens modal first |
| Call next (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `getKpiValues` (onLoad, Today's takings and admissions tiles — …); `listQueueEntries` (onInterval, Who is waiting); `getWaitTimes` (onInterval, Current waits); `listCampaigns` (onLoad, From the flow it appears in); `getQueue` (onLoad, Read a queue with live position); `listQueues` (onLoad, List queues)

**Where the user goes next**

- → `BO-001` Queue Directory: *Queue Directory*; carries `feedId`, `queueId`
- → `BO-002` Queue Configuration: *Queue Configuration*; carries `queueId`
- → `BO-003` Queue Integration Setup: *Queue Integration Setup*; carries `feedId`
- → `EMP-032` Manual wait entry: *The feed dies and a supervisor types the wait*; carries `queueId`; calls `listQueues`

**What opens over it**

- confirmDialog *Stop campaign*: **Names what `stopCampaign` changes and what it leaves alone**, in the consequence rather than the verb. A queue this affects should be identified in the dialog, not just counted. **Collects what `stopCampaign` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The queue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the queue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No queue yet. Offers Create campaign (`createCampaign`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status and the queue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `QUEUE_VIEW`, which `listQueueEntries` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Already launched (`alreadyLaunched`), audience size differs beyond tolerance (`audienceSizeChanged`), or every recipient was excluded (`noReachableRecipients`). (CampaignStateProblem); 409 The campaign is not `scheduled` (`statusDoesNotPermit`) — once it is sending, it is paused or stopped instead. (CampaignStateProblem); 409 The campaign is not `sending` … |

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `listQueueEntries` → `QUEUE_VIEW` (read) · staff
- `callNextParties` → `QUEUE_MANAGE` (configure) · staff
- `getWaitTimes` → no permission · guest, public
- `listCampaigns` → `MARKETING_VIEW` (read) · staff
- `createCampaign` → `MARKETING_MANAGE` (configure) · staff
- `createQueue` → `QUEUE_MANAGE` (configure) · staff
- `getCampaign` → `MARKETING_VIEW` (read) · staff
- `getCampaignPerformance` → `MARKETING_VIEW` (read) · staff
- `getQueue` → `QUEUE_VIEW` (read) · staff
- `launchCampaign` → `MARKETING_SEND` (operate) · staff
- `listQueues` → `QUEUE_VIEW` (read) · staff, guest
- `pauseCampaign` → `MARKETING_MANAGE` (configure) · staff
- `setQueueStatus` → `QUEUE_MANAGE` (configure) · staff
- `setWaitTime` → `QUEUE_MANAGE` (configure) · staff
- `stopCampaign` → `MARKETING_SEND` (operate) · staff
- `testSendCampaign` → `MARKETING_MANAGE` (configure) · staff
- `unscheduleCampaign` → `MARKETING_MANAGE` (configure) · staff
- `updateCampaign` → `MARKETING_MANAGE` (configure) · staff
- `updateQueue` → `QUEUE_MANAGE` (configure) · staff
- `requestSuggestion` → `AI_USE` (operate) · staff, guest

**A refused user sees:** Shown when the caller lacks `QUEUE_VIEW`, which `listQueueEntries` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

57 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.6.2 | Real-time Queue Dashboard: Staff view of queue lengths, wait times, and customer flow. | F&B & Guest Management | CONTRACTED | `listQueueEntries` |
| 5.6.29 | Maintain complete audit logs for reservations, transfers, modifications, cancellations, and check-ins. | F&B & Guest Management | CONTRACTED | `listQueueEntries` |
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 22.1.1 | Campaign Creation | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.4 | Campaign Scheduling | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.12 | Ticketing Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.13 | Membership Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.14 | Loyalty Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.4.8 | Product & Event Integration | Marketing & CRM | CONTRACTED | `createCampaign` |
| … 45 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A visual venue map highlights long-queue rides vs low-queue alternatives so operations can redirect guests, e.g. a notification suggesting a nearby ride with a shorter wait. *(client request · MoM 7 Sep 2026, 4.17 AI guest flow optimization · DI-682)*
- Ops view shows current wait per ride with general and virtual-queue waits separately, and alerts for e.g. a growing express queue or unusually long overall queue. *(client request · MoM 7 Sep 2026, 4.17 Virtual Queue - Operations Dashboard & AI Guest Flow Optimization · DI-681)*
- **Open question.** Open: how per-ride occupancy is counted (entry sensors, manual security counts, CCTV/computer vision); Allam to check with Warner Bros. World, which has a visible wait-time display. Manual count entry stays a possible source. *(open · MoM 7 Sep 2026, 4.16 Wait-Time Calculation & People-Counting Technology · DI-680)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-005` · status **notStarted** · provenance generated
- Flow F09 *Event is cancelled and refunded*, step 5: Confirms guests were notified → Told before they travel, not after
- Flow F21 *A ride queue fills and a guest is redirected*, step 3: A supervisor sees the queue building → Before guests complain
- Flow F21 *A ride queue fills and a guest is redirected*, step 5: Parties are called → From the virtual queue
- Flow F09 branch at step 5 (abandonsFlow): when Guest has no contact details, An anonymous counter sale. **Nothing to notify.** They arrive to a closed door, and the only mitigation is signage.
- Flow F21 branch at step 3 (requiresStaff): when The asset goes out of service, **The queue closes and waiting parties are released, not silently dropped.** A guest holding a place for a closed ride will come back to ask.
- Flow F21 branch at step 5 (recoverable): when A called party does not arrive, Held for a window then skipped. Their place is not restored — **unlike a waitlist, where being asleep is not declining**, a called queue place expires because the ride is running.
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (109), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (86 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-005?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Call next parties, Create campaign, Create queue, Launch campaign, Pause campaign, Save queue status, Save wait time, Stop campaign, Test send campaign, Unschedule campaign, Save campaign, Save queue, Call next.
- [ ] Every transition is wired: `BO-001`, `BO-002`, `BO-003`, `EMP-032`.
- [ ] Every gated control is gated: `AI_USE`, `MARKETING_MANAGE`, `MARKETING_SEND`, `MARKETING_VIEW`, `QUEUE_MANAGE`, `QUEUE_VIEW`, `REPORT_VIEW_VENUE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-006` Parking Configuration

**Change how parking behaves here, and see which level the current value came from.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 2 · needs the `access` module |
| Block | Block A · ticket #18145 (APP-SETUP-BO-006) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `PARKING_CONFIGURE`, `SCOPE_VIEW` (2 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAccessPoints` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `accessPointId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/parking/parking-configuration` |

**What the spec says about it.** Placeholder. Parking was discussed on 14 August and the MoM has not yet been received. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: Answered by the 14 August MoM section 10, which this question was waiting for. Parking is barrier integration, in three models, and it is not space counting. (1) No integration - TICVAI issues its …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listAccessPoints`. | `listAccessPoints` ?venueId |

**Form: Save access point** (modal, opened by *Save access point*; *Save access point* calls `updateAccessPoint`, *Cancel* sends nothing)

**Collects what `updateAccessPoint` sends before it is called.** Nothing in the body is required. Optional: `name`, `direction`, `antiPassbackEnabled`, `requiresExitBeforeReentry`, `isActive`, `driver`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateAccessPoint` body |
| Direction `direction` | radio group | optional | — | Entry · Exit · Reentry · Crossover | — | — | `updateAccessPoint` body |
| Anti passback enabled `antiPassbackEnabled` | toggle | optional | — | — | — | — | `updateAccessPoint` body |
| Requires exit before reentry `requiresExitBeforeReentry` | toggle | optional | — | — | — | — | `updateAccessPoint` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateAccessPoint` body |
| Driver `driver` | text field | optional | — | — | — | Driver identifier for the controller behind this access point. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific. | `updateAccessPoint` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Save parking facility** (modal, opened by *Save parking facility*; *Save parking facility* calls `setParkingFacility`, *Cancel* sends nothing)

**Collects what `setParkingFacility` sends before it is called.** Required: `name`, `venueId`, `mode`. Optional: `id`, `capacity`, `takesPayment`, `vendorSwapTargetDays`, `vendorName`, `endpoint`, `credentialRef`, `pushLeadMinutes`, `accessPointIds`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | Server-assigned, and the upsert key of `setParkingFacility`. Absent in a body, it creates; present, it names the facility being replaced. | `setParkingFacility` body |
| Name `name` | text field | required | — | — | — | — | `setParkingFacility` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setParkingFacility` body |
| Mode `mode` | segmented control | required | — | None · Plate whitelist · QR handoff | — | CF-52, settled 14 August. Not variations of one thing — each decides what happens at sale and what a guest presents at the barrier. | `setParkingFacility` body |
| Capacity `capacity` | number field | optional | — | There is no live space count from the car park; a guest sees *full* only when capacity is reached, never an availability figure. | — | What "full" means in the first release (decided 28 September, audit R166): the facility is full when the issued `ParkingEntitlement`s valid for a time reach this number. | `setParkingFacility` body |
| Vendor name `vendorName` | text field | optional | — | — | — | Staff only — omitted from a guest's `listParkingFacilities` response. | `setParkingFacility` body |
| Endpoint `endpoint` | text field | optional | — | — | — | Staff only — omitted from a guest's `listParkingFacilities` response. | `setParkingFacility` body |
| Credential ref `credentialRef` | text field | optional | — | — | — | A vault reference, never the credential. Staff only — omitted from a guest's `listParkingFacilities` response. | `setParkingFacility` body |
| Push lead minutes `pushLeadMinutes` | number field (minutes) | optional | — | — | — | Staff only — omitted from a guest's `listParkingFacilities` response. How far ahead of the visit a plate is pushed. | `setParkingFacility` body |
| Access points `accessPointIds` | multi-picker: choose access points | optional | — | — | — | Where the platform validates its own code, in `none` and `qrHandoff` modes. | `setParkingFacility` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `setParkingFacility` body |

Errors to draw in the form: 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

#### Outputs: what the screen shows and produces

**Shown**

**Every access point** (data table, from `listAccessPoints`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| External credential sources | list or chips (count when long) | BL-108. A hotel room card admitting a guest to a water park — externally issued, and the platform validates it without having sold it. |
| Scan anomaly rules | list or chips (count when long) | BL-104. Rule-based scan anomalies, separated from the parked model-based engine — device sharing, simultaneous entries at two gates, an … |
| Operating mode | chip: Normal, Free flow, Drop arm, Closed, Podium, Maintenance | Set by the podium with `setTurnstileMode`, and it wins (audit R221). BL-107 and BL-109. |
| Vehicle location capture | yes / no (icon or chip) | BL-023. Nothing helped a guest find their vehicle. |
| Mode | chip: Free rotation, Closed | Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates … |
| Direction | chip: Entry, Exit, Reentry, Crossover | Fixed per access point (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium. |
| Anti passback enabled | yes / no (icon or chip) | — |

**Every parking facility** (data table, from `listParkingFacilities`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Server-assigned, and the upsert key of `setParkingFacility`. Absent in a body, it creates; present, it names the facility being replaced. |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Mode | chip: None, Plate whitelist, QR handoff | CF-52, settled 14 August. Not variations of one thing — each decides what happens at sale and what a guest presents at the barrier. |
| Capacity | 1,234 | What "full" means in the first release (decided 28 September, audit R166): the facility is full when the issued `ParkingEntitlement`s valid … |
| Takes payment | yes / no (icon or chip) | Always false, and stated rather than assumed (19.2.78, CF-124). The requirement asks the guest app to take parking payments; the client … |
| Vendor swap target days | 1,234 | A new parking vendor should take days, not weeks — Qossai, 14 August. The team has integrated parking APIs before and the architecture is … |
| Vendor name | text | Staff only — omitted from a guest's `listParkingFacilities` response. |
| Endpoint | text | Staff only — omitted from a guest's `listParkingFacilities` response. |
| Credential ref | text | A vault reference, never the credential. Staff only — omitted from a guest's `listParkingFacilities` response. |
| Push lead minutes | 1,234 | Staff only — omitted from a guest's `listParkingFacilities` response. How far ahead of the visit a plate is pushed. |
| Access points | list or chips (count when long) | Where the platform validates its own code, in `none` and `qrHandoff` modes. |

**Detail panel** (detail panel): TODO

**The selected access point** (detail panel, from `listAccessPoints`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| External credential sources | list or chips (count when long) | BL-108. A hotel room card admitting a guest to a water park — externally issued, and the platform validates it without having sold it. |
| Scan anomaly rules | list or chips (count when long) | BL-104. Rule-based scan anomalies, separated from the parked model-based engine — device sharing, simultaneous entries at two gates, an … |
| Operating mode | chip: Normal, Free flow, Drop arm, Closed, Podium, Maintenance | Set by the podium with `setTurnstileMode`, and it wins (audit R221). BL-107 and BL-109. |
| Vehicle location capture | yes / no (icon or chip) | BL-023. Nothing helped a guest find their vehicle. |
| Mode | chip: Free rotation, Closed | Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates … |
| Direction | chip: Entry, Exit, Reentry, Crossover | Fixed per access point (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium. |
| Anti passback enabled | yes / no (icon or chip) | — |
| Is active | yes / no (icon or chip) | — |
| Last heartbeat at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save access point (primary button) | `updateAccessPoint` PATCH `/access-points/{accessPointId}` | inline | AccessPoint | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Save parking facility (secondary button) | `setParkingFacility` PUT `/parking-facilities` | ParkingFacility | ParkingFacility | 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Data it reads**: `listAccessPoints` (onLoad, List access points); `listParkingFacilities` (onLoad, Car parks at a venue, and how each integrates)

**Where the user goes next**

- → `BO-001` Queue Directory: *Queue Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The parking list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the parking untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No parking yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId and the parking are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SCOPE_VIEW`, which `listAccessPoints` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listAccessPoints` → `SCOPE_VIEW` (read) · staff
- `updateAccessPoint` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `listParkingFacilities` → `PARKING_CONFIGURE` (configure) · staff, guest
- `setParkingFacility` → `PARKING_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `SCOPE_VIEW`, which `listAccessPoints` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.77 | Parking Locator - System shall help guests locate vehicles. | Guest Mobile App & Branding | CONTRACTED | data `AccessPoint` |
| 3.1.8 | The system shall detect suspicious QR usage patterns including device sharing, multiple simultaneous sessions, excessive activations, and abnormal access attempts, with configurable security … | Admission and Access | CONTRACTED | data `AccessPoint` |
| 3.2.32 | Real-time fraud-monitoring & unified identity lock (one media per visit, Face-change audit, POD/Nanny linkage) | Admission and Access | CONTRACTED | data `AccessPoint` |
| 3.2.57 | In case of emergency, a drop arm mode can be activated at turnstiles. No scan and no count are being performed. | Admission and Access | CONTRACTED | data `AccessPoint` |
| 3.2.61 | It is possible for the system to integrate with hotels room card management system in order to read the room card at access control points and have the ability to interface to the hotels property … | Admission and Access | CONTRACTED | data `AccessPoint` |
| 3.2.73 | The access control can support a Podium feature with functions such as but not limited to: -podium is either in the form of a keyboard interface on the turnstile or a handheld tablet operated by the … | Admission and Access | CONTRACTED | data `AccessPoint` |
| 3.4.1 | The payment can be done upfront or at exit. | Admission and Access | PARKED | data `ParkingFacility` |
| 7.4.12 | The system can manage Parking | F&B POS | PARKED | data `ParkingFacility` |
| 7.4.30 | For each PLU, it is possible to manage Parking tickets which can have a fixed rate per day or per hour. | F&B POS | PARKED | data `ParkingFacility` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Parking is barrier integration, not space counting: one configuration screen chooses a model - no integration (TICVAI QR checked by security), ANPR (guest enters a plate at checkout, pushed to the barrier whitelist) or QR handoff to the barrier. Pay-per-hour parking is out of scope. *(agreed · MoM 14 Aug 2026, 10 · DI-316)*
- Parking supports three models: (1) no integration — TICVAI QR verified manually by security; (2) plate number at checkout pushed to the parking system's ANPR whitelist; (3) TICVAI QR passed to the barrier. Hourly pay-on-exit parking stays on the parking system's own POS. *(agreed · MoM 14 Aug 2026, 10. Parking Integrations · DI-300)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A41** Analyse the integration effort for third-party systems (parking, ride/queue-timing sensors, etc.) to consume TAIS's own standardised API as the default integration model *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'parking')*
- **A42** Design the parking module to support both native QR-based validation (own solution) and a plate-number capture field for future ANPR/third-party parking integrations *(Softlabs Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'parking')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-006` · status **notStarted** · provenance generated
- ADR-0012 *Queue Integration — Adaptor-First, Vendor Deferred* (`docs/adr/0012-queue-integration-adaptor-first.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (38 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-006?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save access point, Save parking facility.
- [ ] Every transition is wired: `BO-001`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `PARKING_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-030` Work Order Verification

**See every gate and what it is doing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `maintenance` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MAINTENANCE_APPROVE`, `MAINTENANCE_EXECUTE`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VERIFY`, `WORK_ORDER_VIEW` (3 operate, 1 configure, 1 read); in the flows as technician |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listWorkOrders` reads the population and `getWorkOrder` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `workOrderId` (deepLink) · cold entry: A work order opened from a queue or an alert. |
| Route | `/venue-operations/access-point-directory` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Carried eight work-order operations.** An access point directory is `access`, not `maintenance` — the two share the word *point* and nothing else. **Rewired 20 August.** **Named `Access Point Directory` and carried nine work-order operations.** On 20 August I rewired it to access points; **F12 step 4 then refused, because a supervisor verifies a work order here.** The operations were right and the name was wrong — **the flow knew what the screen was for and the name did not.**

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Assigned to principal id | picker: choose an assigned to principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?assignedToPrincipalId=` to `listWorkOrders`. | `listWorkOrders` ?assignedToPrincipalId |
| Status | select | optional | — | Open · Assigned · In progress · Paused · Awaiting parts · Completed · Verified · Closed · Cancelled | — | Sends `?status=` to `listWorkOrders`. | `listWorkOrders` ?status |
| Priority | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | Sends `?priority=` to `listWorkOrders`. | `listWorkOrders` ?priority |
| Asset id | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | Sends `?assetId=` to `listWorkOrders`. | `listWorkOrders` ?assetId |
| Overdue only | toggle | optional | off | — | — | Sends `?overdueOnly=` to `listWorkOrders`. | `listWorkOrders` ?overdueOnly |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listWorkOrders` ?from |
| To | date and time picker | — | — | `listWorkOrders` ?to |
| Category | picker: choose a category | — | — | `listWorkOrders` ?categoryId |

**Form: Verify work order** (modal, opened by *Verify work order*; *Verify work order* calls `verifyWorkOrder`, *Cancel* sends nothing)

**Collects what `verifyWorkOrder` sends before it is called.** Required: `outcome`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | segmented control | required | — | Verified · Rejected | — | — | `verifyWorkOrder` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `verifyWorkOrder` body |

Errors to draw in the form: 403 Verifier is the technician who completed the work

**Form: Attach work order evidence** (modal, opened by *Attach work order evidence*; *Attach work order evidence* calls `attachWorkOrderEvidence`, *Cancel* sends nothing)

**Collects what `attachWorkOrderEvidence` sends before it is called.** Required: `kind`. Optional: `assetRef`, `text`, `capturedAt`, `stage`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Photo · Video · Document · Note · Signature | — | — | `attachWorkOrderEvidence` body |
| Asset ref `assetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | In the media store | `attachWorkOrderEvidence` body |
| Text `text` | text area | optional | — | max length 4000 | — | Where the kind is a note | `attachWorkOrderEvidence` body |
| Captured at `capturedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `attachWorkOrderEvidence` body |
| Stage `stage` | radio group | optional | — | Before · During · After · Sign off | — | — | `attachWorkOrderEvidence` body |

**Form: Complete work order** (modal, opened by *Complete work order*; *Complete work order* calls `completeWorkOrder`, *Cancel* sends nothing)

**Collects what `completeWorkOrder` sends before it is called.** Required: `resolution`, `recordedAt`. Optional: `resolutionCode`, `attachmentRefs`, `followUpRequired`, `followUpNote`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Resolution `resolution` | text area | required | — | min length 3; max length 5000 | — | — | `completeWorkOrder` body |
| Resolution code `resolutionCode` | select | optional | — | Repaired · Part replaced · Adjusted · Cleaned · No fault found · Referred external · Replaced · Deferred | — | — | `completeWorkOrder` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `completeWorkOrder` body |
| Follow up required `followUpRequired` | toggle | optional | off | — | — | — | `completeWorkOrder` body |
| Follow up note `followUpNote` | text area | optional | — | max length 1000 | — | — | `completeWorkOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `completeWorkOrder` body |

Errors to draw in the form: 400 Completion photographs required for this category and none supplied

**Form: Create work order** (modal, opened by *Create work order*; *Create work order* calls `createWorkOrder`, *Cancel* sends nothing)

**Collects what `createWorkOrder` sends before it is called.** Required: `id`, `title`, `venueId`, `priority`, `recordedAt`. Optional: `description`, `assetId`, `locationDescription`, `kind`, `categoryId`, `assignedToPrincipalId`, `dueAt`, `attachmentRefs`, `takeAssetOutOfService`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createWorkOrder` body |
| Title `title` | text field | required | — | max length 200 | — | — | `createWorkOrder` body |
| Description `description` | text area | optional | — | max length 5000 | — | — | `createWorkOrder` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createWorkOrder` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `createWorkOrder` body |
| Location description `locationDescription` | text area | optional | — | max length 500 | — | — | `createWorkOrder` body |
| Kind `kind` | radio group | optional | Corrective | Corrective · Planned · Inspection follow up · Incident corrective · Improvement | — | — | `createWorkOrder` body |
| Priority `priority` | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | Optional since 29 September (M17-01). Sent, it is `manual` and wins. | `createWorkOrder` body |
| Fault assessment `faultAssessment` | group | optional | — | — | — | What the person raising a fault says about it, which the priority score reads (M17-01). | `createWorkOrder` body |
| Safety risk `faultAssessment.safetyRisk` | toggle | optional | off | — | — | — | `createWorkOrder` body |
| Guest impact `faultAssessment.guestImpact` | segmented control | optional | None | None · Degraded · Closed | — | — | `createWorkOrder` body |
| Required qualification codes `requiredQualificationCodes` | list of values (chips) | optional | — | at most 10 | — | Skills the job needs, as qualification codes; `suggestWorkOrderAssignee` ranks by them (M17-13). | `createWorkOrder` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `createWorkOrder` body |
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | — | `createWorkOrder` body |
| Due at `dueAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createWorkOrder` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | Photo-first. Expected at creation, not added later from memory. | `createWorkOrder` body |
| Take asset out of service `takeAssetOutOfService` | toggle | optional | off | — | — | Raise and immediately suspend the asset. For a fault found on a live ride, the two are one action. | `createWorkOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createWorkOrder` body |

Errors to draw in the form: 400 Validation failed

**Sent by *Cancel work order*** (`cancelWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | radio group | required | — | Raised in error · Duplicate · Superseded · No longer required | — | — | `cancelWorkOrder` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `cancelWorkOrder` body |
| Superseded by work order `supersededByWorkOrderId` | picker: choose a superseded by work order | optional | — | — | shows names, sends the id | — | `cancelWorkOrder` body |

**Sent by *Close work order*** (`closeWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | radio group | required | — | Completed and verified · Not reproducible · Superseded by replacement · No longer applicable · Duplicate | — | — | `closeWorkOrder` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `closeWorkOrder` body |
| Duplicate of work order `duplicateOfWorkOrderId` | picker: choose a duplicate of work order | optional | — | — | shows names, sends the id | — | `closeWorkOrder` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every work order** (data table, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Root cause | chip: Wear and tear, Operator error, Guest damage, Manufacturing defect, Environmental … | Structured, because free text cannot be counted. *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault … |
| Root cause note | text | — |
| Escalated at | 1 Oct 2026, 14:30 | — |
| Escalation level | 1,234 | Escalation is a clock, not a decision. A work order on a ride nobody has accepted after twenty minutes escalates itself, because the … |
| ID | the name it points at, never the id | — |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |

**The selected work order** (detail panel, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Root cause | chip: Wear and tear, Operator error, Guest damage, Manufacturing defect, Environmental … | Structured, because free text cannot be counted. *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault … |
| Root cause note | text | — |
| Escalated at | 1 Oct 2026, 14:30 | — |
| Escalation level | 1,234 | Escalation is a clock, not a decision. A work order on a ride nobody has accepted after twenty minutes escalates itself, because the … |
| ID | the name it points at, never the id | — |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |
| Kind | chip: Corrective, Planned, Inspection follow up, Incident corrective, Improvement | — |
| Assigned to principal | the name it points at, never the id | — |
| Raised by principal | the name it points at, never the id | — |

**The work order** (detail panel, from `getWorkOrder`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Root cause | chip: Wear and tear, Operator error, Guest damage, Manufacturing defect, Environmental … | Structured, because free text cannot be counted. *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault … |
| Root cause note | text | — |
| Escalated at | 1 Oct 2026, 14:30 | — |
| Escalation level | 1,234 | Escalation is a clock, not a decision. A work order on a ride nobody has accepted after twenty minutes escalates itself, because the … |
| ID | the name it points at, never the id | — |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |
| Kind | chip: Corrective, Planned, Inspection follow up, Incident corrective, Improvement | — |
| Assigned to principal | the name it points at, never the id | — |
| Raised by principal | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Verify work order (primary button) | `verifyWorkOrder` POST `/work-orders/{workOrderId}/verify` | inline | WorkOrder | 403 Verifier is the technician who completed the work | opens modal first |
| Accept work order (secondary button) | `acceptWorkOrder` POST `/work-orders/{workOrderId}/accept` | — | WorkOrder | 409 Not assigned to this principal, or already accepted | — |
| Attach work order evidence (secondary button) | `attachWorkOrderEvidence` POST `/work-orders/{workOrderId}/attachments` | inline | WorkOrderAttachment | — | opens modal first |
| Cancel work order (destructive button) | `cancelWorkOrder` POST `/work-orders/{workOrderId}/cancel` | inline | WorkOrder | 409 Work has started. | — |
| Close work order (destructive button) | `closeWorkOrder` POST `/work-orders/{workOrderId}/close` | inline | WorkOrder | — | — |
| Complete work order (secondary button) | `completeWorkOrder` POST `/work-orders/{workOrderId}/complete` | inline | WorkOrder | 400 Completion photographs required for this category and none supplied | opens modal first |
| Create work order (secondary button) | `createWorkOrder` POST `/work-orders` | CreateWorkOrderRequest | WorkOrder | 400 Validation failed | opens modal first |

**Data it reads**: `listWorkOrders` (onLoad, List work orders)

**Where the user goes next**

- → `BO-070` Work Orders: *Work Orders*; carries `workOrderId`
- → `BO-031` Asset Register: *Asset returns to service*; carries `assetId`; calls `verifyWorkOrder`

**What opens over it**

- confirmDialog *Cancel work order*: **Names what `cancelWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A work order verification this affects should be identified in the dialog, not just counted. **Collects what `cancelWorkOrder` sends before it is called.** Required: `reason`. Optional …
- confirmDialog *Close work order*: **Names what `closeWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A work order verification this affects should be identified in the dialog, not just counted. **Collects what `closeWorkOrder` sends before it is called.** Required: `outcome`. Optional …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The work order verification list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the work order verification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No work order verification yet. Offers Create work order (`createWorkOrder`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on assignedToPrincipalId, status, priority, assetId, overdueOnly and the work order verification are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORK_ORDER_VIEW`, which `getWorkOrder` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Completion photographs required for this category and none supplied; 400 Validation failed; 409 Not assigned to this principal, or already accepted; 409 Work has started. |

#### Permissions

- `verifyWorkOrder` → `WORK_ORDER_VERIFY` (operate) · staff
- `acceptWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `attachWorkOrderEvidence` → `MAINTENANCE_EXECUTE` (operate) · staff
- `cancelWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `closeWorkOrder` → `MAINTENANCE_APPROVE` (operate) · staff
- `completeWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `createWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `getWorkOrder` → `WORK_ORDER_VIEW` (read) · staff
- `listWorkOrders` → `WORK_ORDER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WORK_ORDER_VIEW`, which `getWorkOrder` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

31 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.4.6 | Work Order Approval - System shall support work order approvals. | Maintenance & Safety Management | CONTRACTED | `verifyWorkOrder` |
| 17.4.7 | Work Order Closure - System shall support work order closure workflows. | Maintenance & Safety Management | CONTRACTED | `verifyWorkOrder` |
| 18.2.1 | Work Order Inbox - Users shall view assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.2 | Work Order Acceptance - Users shall accept assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.3 | Work Order Rejection - Users shall reject assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.4 | Work Order Start - Users shall start work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.5 | Work Order Pause - Users shall pause work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.6 | Work Order Completion - Users shall complete work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.7 | Work Order Closure - Authorized users shall close work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.5.1 | Photo Capture - Users shall capture photos. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| 18.5.2 | Video Capture - Users shall capture videos. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| 18.5.3 | Document Upload - Users shall upload documents. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| … 19 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-030` · status **notStarted** · provenance generated
- Flow F12 *Asset fails and closes a queue*, step 4: Supervisor verifies → **By someone other than the person who did the work.** Safety-critical assets cannot return without it
- Flow F12 branch at step 4 (requiresStaff): when Verifier is the person who did the work, **Refused.** This is the control, and it is enforced rather than trusted.

#### Acceptance for the design

- [ ] Every input above is drawn (42), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-030?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Verify work order, Accept work order, Attach work order evidence, Cancel work order, Close work order, Complete work order, Create work order.
- [ ] Every transition is wired: `BO-070`, `BO-031`.
- [ ] Every gated control is gated: `MAINTENANCE_APPROVE`, `MAINTENANCE_EXECUTE`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VERIFY`, `WORK_ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-031` Asset Register

**Define what a gate is and where it is.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `maintenance` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_MANAGE`, `ASSET_VIEW` (1 configure, 1 read); in the flows as technician |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAssets` reads the population and `getAsset` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `assetId` (deepLink) · cold entry: An asset opened from the register or a work order. |
| Route | `/venue-operations/access-point-configuration` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Carried seven asset operations.** A turnstile is an asset and configuring an access point is not asset management. **Rewired 20 August.** **Named `Access Point Configuration` and carried seven asset operations.** Same correction as BO-030 — F12 step 5 returns an asset to service here.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listAssets`. | `listAssets` ?venueId |
| Category id | picker: choose a category (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?categoryId=` to `listAssets`. | `listAssets` ?categoryId |
| Status | select | optional | — | In service · Out of service · Under maintenance · Awaiting parts · Retired · Disposed | — | Sends `?status=` to `listAssets`. | `listAssets` ?status |
| Maintenance due | toggle | optional | — | — | — | Sends `?maintenanceDue=` to `listAssets`. | `listAssets` ?maintenanceDue |
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |

**Form: Save asset** (modal, opened by *Save asset*; *Save asset* calls `updateAsset`, *Cancel* sends nothing)

**Collects what `updateAsset` sends before it is called.** Nothing in the body is required. Optional: `name`, `locationDescription`, `categoryId`, `warrantyExpiresAt`, `supplierId`, `documents`, `documentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateAsset` body |
| Location description `locationDescription` | text area | optional | — | max length 500 | — | — | `updateAsset` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateAsset` body |
| Warranty expires at `warrantyExpiresAt` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateAsset` body |
| Supplier `supplierId` | picker: choose a supplier | optional | — | — | shows names, sends the id | — | `updateAsset` body |
| Priority override `priorityOverride` | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | See `Asset.priorityOverride` (M17-01, 29 September). Null clears it. | `updateAsset` body |
| Documents `documents` | repeatable rows | optional | — | — | — | Replaces the asset's documents. One `asset_document` row each. | `updateAsset` body |
| Ref `documents[].ref` | text field | required | — | — | — | The document in the media store. | `updateAsset` body |
| Name `documents[].name` | text field | optional | — | max length 200 | — | — | `updateAsset` body |
| Kind `documents[].kind` | select | required | — | Manual · Sop · Certificate · Warranty · Drawing · Risk assessment | — | — | `updateAsset` body |
| Document refs `documentRefs` | list of values (chips) | optional | — | — | — | The refs alone, kept for callers that predate `documents`. Each becomes a document with no name and no kind. | `updateAsset` body |

**Form: Create asset** (modal, opened by *Create asset*; *Create asset* calls `createAsset`, *Cancel* sends nothing)

**Collects what `createAsset` sends before it is called.** Required: `assetTag`, `name`, `venueId`, `criticality`. Optional: `categoryId`, `locationDescription`, `manufacturer`, `model`, `serialNumber`, `commissionedAt`, `warrantyExpiresAt`, `supplierId`, `linkedProductIds`, `linkedAccessPointId`, `requiresInspectionToReturn`, `documents` and 1 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Asset tag `assetTag` | text field | required | — | max length 64 | — | Unique per venue (decided 28 September, audit R108). Two assets in one venue never share a tag; `createAsset` refuses a duplicate with `409` `duplicate-code`. | `createAsset` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createAsset` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createAsset` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `createAsset` body |
| Location description `locationDescription` | text area | optional | — | max length 500 | — | — | `createAsset` body |
| Criticality `criticality` | radio group | required | — | Safety critical · Revenue critical · Standard · Low | — | — | `createAsset` body |
| Priority override `priorityOverride` | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | "If this device goes down, raise this priority" (decided 17 September, M17-01). A corrective work order raised on this asset takes this priority instead of the score. | `createAsset` body |
| Manufacturer `manufacturer` | text field | optional | — | max length 200 | — | — | `createAsset` body |
| Model `model` | text field | optional | — | max length 200 | — | — | `createAsset` body |
| Serial number `serialNumber` | text field | optional | — | max length 128 | — | — | `createAsset` body |
| Commissioned at `commissionedAt` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createAsset` body |
| Warranty expires at `warrantyExpiresAt` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createAsset` body |
| Supplier `supplierId` | picker: choose a supplier | optional | — | — | shows names, sends the id | — | `createAsset` body |
| Linked products `linkedProductIds` | multi-picker: choose linked products | optional | — | — | — | Products this asset delivers. A fault here can stop them selling. | `createAsset` body |
| Linked access point `linkedAccessPointId` | picker: choose a linked access point | optional | — | — | shows names, sends the id | Access point this asset controls. Out of service blocks it. | `createAsset` body |
| Requires inspection to return `requiresInspectionToReturn` | toggle | optional | off | — | — | True means a completed inspection is required before return to service. A technician cannot simply declare a ride safe. | `createAsset` body |
| Documents `documents` | repeatable rows | optional | — | — | — | Manuals, procedures, certificates, each with its name and kind. Stored one row per document in `maintenance.asset_document`, which is where `AssetDetail.documents` reads them from. | `createAsset` body |
| Ref `documents[].ref` | text field | required | — | — | — | The document in the media store. | `createAsset` body |
| Name `documents[].name` | text field | optional | — | max length 200 | — | — | `createAsset` body |
| Kind `documents[].kind` | select | required | — | Manual · Sop · Certificate · Warranty · Drawing · Risk assessment | — | — | `createAsset` body |
| Document refs `documentRefs` | list of values (chips) | optional | — | — | — | The refs alone, kept for callers that predate `documents`. Each ref sent here is stored as an `asset_document` row with no name and no kind. | `createAsset` body |

Errors to draw in the form: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …

**Form: Save asset status** (modal, opened by *Save asset status*; *Save asset status* calls `setAssetStatus`, *Cancel* sends nothing)

**Collects what `setAssetStatus` sends before it is called.** Required: `status`, `reason`, `recordedAt`. Optional: `inspectionId`, `raiseWorkOrder`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | required | — | In service · Out of service · Under maintenance · Awaiting parts · Retired · Disposed | — | — | `setAssetStatus` body |
| Reason `reason` | text area | required | — | min length 3; max length 1000 | — | — | `setAssetStatus` body |
| Inspection `inspectionId` | picker: choose an inspection | optional | — | — | shows names, sends the id | Required for return to service where the asset demands it. | `setAssetStatus` body |
| Raise work order `raiseWorkOrder` | toggle | optional | off | — | — | — | `setAssetStatus` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setAssetStatus` body |

Errors to draw in the form: 409 Return to service attempted without the inspection this asset category requires.

#### Outputs: what the screen shows and produces

**Shown**

**Every asset** (data table, from `listAssets`)

| Shows | Format | Notes |
|---|---|---|
| Asset tag | text | Unique per venue (decided 28 September, audit R108). Two assets in one venue never share a tag; `createAsset` refuses a duplicate with … |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Category | the name it points at, never the id | — |
| Location description | text | — |
| Criticality | chip: Safety critical, Revenue critical, Standard, Low | — |
| Manufacturer | text | — |
| Model | text | — |
| Serial number | text | — |
| Commissioned at | 1 Oct 2026 | — |
| Warranty expires at | 1 Oct 2026 | — |
| Supplier | the name it points at, never the id | — |

**The selected asset** (detail panel, from `listAssets`)

| Shows | Format | Notes |
|---|---|---|
| Asset tag | text | Unique per venue (decided 28 September, audit R108). Two assets in one venue never share a tag; `createAsset` refuses a duplicate with … |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Category | the name it points at, never the id | — |
| Location description | text | — |
| Criticality | chip: Safety critical, Revenue critical, Standard, Low | — |
| Manufacturer | text | — |
| Model | text | — |
| Serial number | text | — |
| Commissioned at | 1 Oct 2026 | — |
| Warranty expires at | 1 Oct 2026 | — |
| Supplier | the name it points at, never the id | — |
| Linked products | list or chips (count when long) | Products this asset delivers. A fault here can stop them selling. |
| Linked access point | the name it points at, never the id | Access point this asset controls. Out of service blocks it. |
| Requires inspection to return | yes / no (icon or chip) | True means a completed inspection is required before return to service. A technician cannot simply declare a ride safe. |
| Documents | list or chips (count when long) | Manuals, procedures, certificates, each with its name and kind. Stored one row per document in `maintenance.asset_document`, which is where … |

**The asset history entry** (detail panel, from `getAssetHistory`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Work order, Inspection, Incident, Status change, Part replaced, Plan completed | — |
| Reference | the name it points at, never the id | The source row's id: a work order, inspection or incident, or an `asset_status_change` id. |
| Summary | text | — |
| Principal | the name it points at, never the id | — |
| Occurred at | 1 Oct 2026, 14:30 | — |

**The asset** (detail panel, from `getAsset`)

| Shows | Format | Notes |
|---|---|---|
| Open work orders | list or chips (count when long) | — |
| Maintenance plans | list or chips (count when long) | — |
| Documents | list or chips (count when long) | Manuals, procedures, certificates. What a technician needs on site. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save asset (primary button) | `updateAsset` PATCH `/assets/{assetId}` | inline | Asset | — | opens modal first |
| Create asset (secondary button) | `createAsset` POST `/assets` | CreateAssetRequest | Asset | 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … | opens modal first |
| Lookup asset (secondary button) | `lookupAsset` GET `/assets/lookup` | — | AssetDetail | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Save asset status (secondary button) | `setAssetStatus` PUT `/assets/{assetId}/status` | SetAssetStatusRequest | AssetStatusResult | 409 Return to service attempted without the inspection this asset category requires. | opens modal first |

**Data it reads**: `listAssets` (onLoad, List assets)

**Where the user goes next**

- → `BO-001` Queue Directory: *Queue Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset register list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset register untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No asset register yet. Offers Create asset (`createAsset`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, categoryId, status, maintenanceDue and the asset register are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ASSET_VIEW`, which `getAsset` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 409 Return to service attempted without the inspection this asset category requires. |

#### Permissions

- `updateAsset` → `ASSET_MANAGE` (configure) · staff
- `createAsset` → `ASSET_MANAGE` (configure) · staff
- `getAsset` → `ASSET_VIEW` (read) · staff
- `getAssetHistory` → `ASSET_VIEW` (read) · staff
- `listAssets` → `ASSET_VIEW` (read) · staff
- `lookupAsset` → `ASSET_VIEW` (read) · staff
- `setAssetStatus` → `ASSET_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `ASSET_VIEW`, which `getAsset` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

23 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.1.1 | Asset Master - System shall support centralized asset management. | Maintenance & Safety Management | CONTRACTED | `createAsset` |
| 17.1.2 | Asset Categories - System shall support asset categorization. | Maintenance & Safety Management | CONTRACTED | `createAsset` |
| 17.1.3 | Asset Location Management - System shall maintain asset locations. | Maintenance & Safety Management | CONTRACTED | `createAsset` |
| 17.1.5 | Asset Warranty Management - System shall maintain warranty information. | Maintenance & Safety Management | CONTRACTED | `createAsset` |
| 17.1.6 | Asset Documentation - System shall maintain manuals and technical documents. | Maintenance & Safety Management | CONTRACTED | `getAsset` |
| 17.5.10 | Safety Documentation - System shall support safety document management. | Maintenance & Safety Management | CONTRACTED | `getAsset` |
| 16.5.27 | Maintenance History - System shall maintain maintenance history. | Device Management | CONTRACTED | `getAssetHistory` |
| 17.1.8 | Asset History - System shall maintain complete asset history. | Maintenance & Safety Management | CONTRACTED | `getAssetHistory` |
| 17.3.7 | Service History - System shall maintain service history. | Maintenance & Safety Management | CONTRACTED | `getAssetHistory` |
| 18.3.4 | Asset History - Users shall view maintenance history. | Employee Mobile App & AI Assistant | CONTRACTED | `getAssetHistory` |
| 18.3.5 | Asset Documentation - Users shall access manuals and documents. | Employee Mobile App & AI Assistant | CONTRACTED | `getAssetHistory` |
| 18.3.1 | QR Asset Scanning - Users shall scan asset QR codes. | Employee Mobile App & AI Assistant | CONTRACTED | `lookupAsset` |
| … 11 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A 360-degree asset view, searchable via QR code, consolidates all asset details: attached documentation (installation manuals, wiring diagrams, safety inspection reports), warranty period and full lifecycle history (installed, maintained, operational, upcoming maintenance); a location view shows where each asset physically sits. *(client request · MoM 17 Sep 2026, 4.1 Asset Registry & Classification · DI-910)*
- Corrective-maintenance priority combines a configurable weighted scoring model (e.g. P1 emergency when guest operations are affected) with a direct per-asset priority override field: "if this specific device goes down, raise this priority level". *(agreed · MoM 17 Sep 2026, 4.3 Corrective & Emergency Maintenance · DI-909)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-031` · status **notStarted** · provenance generated
- Flow F12 *Asset fails and closes a queue*, step 5: Asset returns to service → The queue reopens and the guest app offers it again
- Flow F12 branch at step 5 (requiresStaff): when Queue does not reopen after the asset returns, The cascade failed. `maintenance.assetReturnedToService` has two critical consumers for this reason — a ride verified and back in service whose queue never reopened is a closed attraction nobody …

#### Acceptance for the design

- [ ] Every input above is drawn (42), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (36 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-031?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save asset, Create asset, Lookup asset, Save asset status.
- [ ] Every transition is wired: `BO-001`.
- [ ] Every gated control is gated: `ASSET_MANAGE`, `ASSET_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-032` Admission Profiles

**Set the rules a gate enforces, including offline.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `access` module |
| Block | Block A · ticket #17917 (APP-SETUP-BO-032) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAdmissionRules` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `profileId` (deepLink), `ruleId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/admission-rules` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**Form: Create admission rules** (modal, opened by *Create admission rules*; *Create admission rules* calls `createAdmissionRules`, *Cancel* sends nothing)

**Collects what `createAdmissionRules` sends before it is called.** Required: `id`, `code`, `name`, `openMinutesBefore`, `closeMinutesAfter`. Optional: `perProductRules`, `maxDurationMinutes`, `requiresExitBeforeReentry`, `maxReentries`, `allowedAccessPointIds`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createAdmissionRules` body |
| Per product rules `perProductRules` | repeatable rows | optional | — | — | — | BL-059. Transaction rules were per profile and a ticket type could not state its own. | `createAdmissionRules` body |
| Product `perProductRules[].productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `createAdmissionRules` body |
| Entries per day `perProductRules[].entriesPerDay` | number field | optional | — | — | — | — | `createAdmissionRules` body |
| Minimum gap minutes `perProductRules[].minimumGapMinutes` | number field (minutes) | optional | — | — | — | Anti-passback in minutes rather than a boolean. A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back … | `createAdmissionRules` body |
| Allowed access points `perProductRules[].allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | — | `createAdmissionRules` body |
| Biometric policy `perProductRules[].biometricPolicy` | segmented control | optional | — | Disabled · Offered · Preferred | — | BL-105, 3.2.9. The biometric check is a property of the product, not of the venue — memberships checked, day tickets not. | `createAdmissionRules` body |
| Max passes per biometric identity `perProductRules[].maxPassesPerBiometricIdentity` | number field | optional | — | min 1 | — | BL-096, 2.14.7. The annual-pass quota, keyed to biometric identity. | `createAdmissionRules` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createAdmissionRules` body |
| Open minutes before `openMinutesBefore` | number field (minutes) | required | — | — | — | How long before a performance validation opens. | `createAdmissionRules` body |
| Close minutes after `closeMinutesAfter` | number field (minutes) | required | — | — | — | — | `createAdmissionRules` body |
| Max duration minutes `maxDurationMinutes` | number field (minutes) | optional | — | — | — | — | `createAdmissionRules` body |
| Requires exit before reentry `requiresExitBeforeReentry` | toggle | optional | off | — | — | — | `createAdmissionRules` body |
| Max reentries `maxReentries` | number field | optional | — | — | — | — | `createAdmissionRules` body |
| Entry limit `entryLimit` | group | optional | — | — | — | How many times the credential may enter (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). | `createAdmissionRules` body |
| Mode `entryLimit.mode` | radio group | required | Unlimited | Unlimited · Once · N times · N per day · N per period | — | — | `createAdmissionRules` body |
| Count `entryLimit.count` | number field | optional | — | min 1 | — | N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it) | `createAdmissionRules` body |
| Period days `entryLimit.periodDays` | number field (days) | optional | — | min 1 | — | The period for nPerPeriod | `createAdmissionRules` body |
| Exit scan `exitScan` | segmented control | optional | Optional | Required · Optional · None | — | (decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. | `createAdmissionRules` body |
| Max exits `maxExits` | number field | optional | — | min 0 | — | Null is unlimited (decided 29 September, VM close-out) | `createAdmissionRules` body |
| Re entry window minutes `reEntryWindowMinutes` | number field (minutes) | optional | — | min 1 | — | Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out) | `createAdmissionRules` body |
| Same day only `sameDayOnly` | toggle | optional | on | — | — | Re-entry only on the day of the exit (decided 29 September, VM close-out) | `createAdmissionRules` body |
| Designated access points `designatedAccessPointIds` | multi-picker: choose designated access points | optional | — | — | — | Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out) | `createAdmissionRules` body |
| Validity `validity` | group | optional | — | — | — | When the credential is valid (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). | `createAdmissionRules` body |
| Anchor `validity.anchor` | radio group | required | — | Fixed range · After sale · After activation · After first use | — | fixedRange uses from and to; the others count days from the event | `createAdmissionRules` body |
| Days `validity.days` | number field | optional | — | min 1 | — | N days after the anchor; required unless the anchor is fixedRange | `createAdmissionRules` body |
| From `validity.from` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createAdmissionRules` body |
| To `validity.to` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Inclusive. | `createAdmissionRules` body |
| End of `validity.endOf` | radio group | optional | — | Day · Week · Month · Year | — | Validity runs to the end of the day, week, month or year the relative period ends in | `createAdmissionRules` body |
| Days of week `validity.daysOfWeek` | multi-select chips | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | Empty is every day | `createAdmissionRules` body |
| Day types `validity.dayTypes` | multi-select chips | optional | — | Peak dates · Off peak dates · Holidays · Seasons · Event dates | — | Calendar day types on which access is allowed; empty is every day type | `createAdmissionRules` body |
| Blackout dates `validity.blackoutDates` | list of values (chips) | optional | — | — | — | Dates on which access is refused whatever else allows it | `createAdmissionRules` body |
| Crossover `crossover` | group | optional | — | — | — | Crossover between parks (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. | `createAdmissionRules` body |
| Allowed park org units `crossover.allowedParkOrgUnitIds` | multi-picker: choose allowed park org units | required | — | at least 2 | — | — | `createAdmissionRules` body |
| Park order `crossover.parkOrder` | multi-picker: choose park order | optional | — | — | — | Required order of parks, if any; empty is any order | `createAdmissionRules` body |
| Same day only `crossover.sameDayOnly` | toggle | optional | on | — | — | — | `createAdmissionRules` body |
| Different day access `crossover.differentDayAccess` | toggle | optional | off | — | — | — | `createAdmissionRules` body |
| Day pattern `crossover.dayPattern` | segmented control | optional | Flexible within validity | Consecutive from first scan · Flexible within validity | — | — | `createAdmissionRules` body |
| Max park entries `crossover.maxParkEntries` | number field | optional | — | min 1 | — | Null is unlimited | `createAdmissionRules` body |
| Crossover quantity `crossover.crossoverQuantity` | number field | optional | — | min 1 | — | How many crossovers; null is unlimited | `createAdmissionRules` body |
| Crossover after time `crossover.crossoverAfterTime` | time picker | optional | — | — | HH:mm, 24-hour | Earliest venue-local time HH:MM a crossover is allowed | `createAdmissionRules` body |
| Prerequisite park org unit `crossover.prerequisiteParkOrgUnitId` | picker: choose a prerequisite park org unit | optional | — | — | shows names, sends the id | The park that must be entered first | `createAdmissionRules` body |
| Re entry after crossover `crossover.reEntryAfterCrossover` | toggle | optional | off | — | — | — | `createAdmissionRules` body |
| Allowed access points `allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Empty means any access point in the venue. | `createAdmissionRules` body |
| Re entry verification `reEntryVerification` | radio group | optional | Credential only | Credential only · Credential uv stamp · Credential face · Credential operator · Custom | — | What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1). | `createAdmissionRules` body |
| … 2 more | | | | | | the rest are in `schemas.json` | `createAdmissionRules` body |

**Form: Save admission rules** (modal, opened by *Save admission rules*; *Save admission rules* calls `updateAdmissionRules`, *Cancel* sends nothing)

**Collects what `updateAdmissionRules` sends before it is called.** Required: `id`, `code`, `name`, `openMinutesBefore`, `closeMinutesAfter`. Optional: `perProductRules`, `maxDurationMinutes`, `requiresExitBeforeReentry`, `maxReentries`, `allowedAccessPointIds`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `updateAdmissionRules` body |
| Per product rules `perProductRules` | repeatable rows | optional | — | — | — | BL-059. Transaction rules were per profile and a ticket type could not state its own. | `updateAdmissionRules` body |
| Product `perProductRules[].productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `updateAdmissionRules` body |
| Entries per day `perProductRules[].entriesPerDay` | number field | optional | — | — | — | — | `updateAdmissionRules` body |
| Minimum gap minutes `perProductRules[].minimumGapMinutes` | number field (minutes) | optional | — | — | — | Anti-passback in minutes rather than a boolean. A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back … | `updateAdmissionRules` body |
| Allowed access points `perProductRules[].allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | — | `updateAdmissionRules` body |
| Biometric policy `perProductRules[].biometricPolicy` | segmented control | optional | — | Disabled · Offered · Preferred | — | BL-105, 3.2.9. The biometric check is a property of the product, not of the venue — memberships checked, day tickets not. | `updateAdmissionRules` body |
| Max passes per biometric identity `perProductRules[].maxPassesPerBiometricIdentity` | number field | optional | — | min 1 | — | BL-096, 2.14.7. The annual-pass quota, keyed to biometric identity. | `updateAdmissionRules` body |
| Name `name` | text field | required | — | max length 200 | — | — | `updateAdmissionRules` body |
| Open minutes before `openMinutesBefore` | number field (minutes) | required | — | — | — | How long before a performance validation opens. | `updateAdmissionRules` body |
| Close minutes after `closeMinutesAfter` | number field (minutes) | required | — | — | — | — | `updateAdmissionRules` body |
| Max duration minutes `maxDurationMinutes` | number field (minutes) | optional | — | — | — | — | `updateAdmissionRules` body |
| Requires exit before reentry `requiresExitBeforeReentry` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Max reentries `maxReentries` | number field | optional | — | — | — | — | `updateAdmissionRules` body |
| Entry limit `entryLimit` | group | optional | — | — | — | How many times the credential may enter (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). | `updateAdmissionRules` body |
| Mode `entryLimit.mode` | radio group | required | Unlimited | Unlimited · Once · N times · N per day · N per period | — | — | `updateAdmissionRules` body |
| Count `entryLimit.count` | number field | optional | — | min 1 | — | N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it) | `updateAdmissionRules` body |
| Period days `entryLimit.periodDays` | number field (days) | optional | — | min 1 | — | The period for nPerPeriod | `updateAdmissionRules` body |
| Exit scan `exitScan` | segmented control | optional | Optional | Required · Optional · None | — | (decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. | `updateAdmissionRules` body |
| Max exits `maxExits` | number field | optional | — | min 0 | — | Null is unlimited (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Re entry window minutes `reEntryWindowMinutes` | number field (minutes) | optional | — | min 1 | — | Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Same day only `sameDayOnly` | toggle | optional | on | — | — | Re-entry only on the day of the exit (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Designated access points `designatedAccessPointIds` | multi-picker: choose designated access points | optional | — | — | — | Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out) | `updateAdmissionRules` body |
| Validity `validity` | group | optional | — | — | — | When the credential is valid (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). | `updateAdmissionRules` body |
| Anchor `validity.anchor` | radio group | required | — | Fixed range · After sale · After activation · After first use | — | fixedRange uses from and to; the others count days from the event | `updateAdmissionRules` body |
| Days `validity.days` | number field | optional | — | min 1 | — | N days after the anchor; required unless the anchor is fixedRange | `updateAdmissionRules` body |
| From `validity.from` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateAdmissionRules` body |
| To `validity.to` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Inclusive. | `updateAdmissionRules` body |
| End of `validity.endOf` | radio group | optional | — | Day · Week · Month · Year | — | Validity runs to the end of the day, week, month or year the relative period ends in | `updateAdmissionRules` body |
| Days of week `validity.daysOfWeek` | multi-select chips | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | Empty is every day | `updateAdmissionRules` body |
| Day types `validity.dayTypes` | multi-select chips | optional | — | Peak dates · Off peak dates · Holidays · Seasons · Event dates | — | Calendar day types on which access is allowed; empty is every day type | `updateAdmissionRules` body |
| Blackout dates `validity.blackoutDates` | list of values (chips) | optional | — | — | — | Dates on which access is refused whatever else allows it | `updateAdmissionRules` body |
| Crossover `crossover` | group | optional | — | — | — | Crossover between parks (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. | `updateAdmissionRules` body |
| Allowed park org units `crossover.allowedParkOrgUnitIds` | multi-picker: choose allowed park org units | required | — | at least 2 | — | — | `updateAdmissionRules` body |
| Park order `crossover.parkOrder` | multi-picker: choose park order | optional | — | — | — | Required order of parks, if any; empty is any order | `updateAdmissionRules` body |
| Same day only `crossover.sameDayOnly` | toggle | optional | on | — | — | — | `updateAdmissionRules` body |
| Different day access `crossover.differentDayAccess` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Day pattern `crossover.dayPattern` | segmented control | optional | Flexible within validity | Consecutive from first scan · Flexible within validity | — | — | `updateAdmissionRules` body |
| Max park entries `crossover.maxParkEntries` | number field | optional | — | min 1 | — | Null is unlimited | `updateAdmissionRules` body |
| Crossover quantity `crossover.crossoverQuantity` | number field | optional | — | min 1 | — | How many crossovers; null is unlimited | `updateAdmissionRules` body |
| Crossover after time `crossover.crossoverAfterTime` | time picker | optional | — | — | HH:mm, 24-hour | Earliest venue-local time HH:MM a crossover is allowed | `updateAdmissionRules` body |
| Prerequisite park org unit `crossover.prerequisiteParkOrgUnitId` | picker: choose a prerequisite park org unit | optional | — | — | shows names, sends the id | The park that must be entered first | `updateAdmissionRules` body |
| Re entry after crossover `crossover.reEntryAfterCrossover` | toggle | optional | off | — | — | — | `updateAdmissionRules` body |
| Allowed access points `allowedAccessPointIds` | multi-picker: choose allowed access points | optional | — | — | — | Empty means any access point in the venue. | `updateAdmissionRules` body |
| Re entry verification `reEntryVerification` | radio group | optional | Credential only | Credential only · Credential uv stamp · Credential face · Credential operator · Custom | — | What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1). | `updateAdmissionRules` body |
| … 2 more | | | | | | the rest are in `schemas.json` | `updateAdmissionRules` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before validity.from

#### Outputs: what the screen shows and produces

**Shown**

**Every admission rules** (data table, from `listAdmissionRules`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Server-assigned. Ignored in a `createAdmissionRules` or `updateAdmissionRules` body; on update the profile is the one the path names. |
| Code | text | — |
| Per product rules | list or chips (count when long) | BL-059. Transaction rules were per profile and a ticket type could not state its own. |
| Name | text | — |
| Open minutes before | 1,234 | How long before a performance validation opens. |
| Close minutes after | 1,234 | — |
| Max duration minutes | 1,234 | — |
| Requires exit before reentry | yes / no (icon or chip) | — |
| Max reentries | 1,234 | — |
| Allowed access points | list or chips (count when long) | Empty means any access point in the venue. |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**The selected admission rules** (detail panel, from `listAdmissionRules`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Server-assigned. Ignored in a `createAdmissionRules` or `updateAdmissionRules` body; on update the profile is the one the path names. |
| Code | text | — |
| Per product rules | list or chips (count when long) | BL-059. Transaction rules were per profile and a ticket type could not state its own. |
| Name | text | — |
| Open minutes before | 1,234 | How long before a performance validation opens. |
| Close minutes after | 1,234 | — |
| Max duration minutes | 1,234 | — |
| Requires exit before reentry | yes / no (icon or chip) | — |
| Max reentries | 1,234 | — |
| Allowed access points | list or chips (count when long) | Empty means any access point in the venue. |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create admission rules (primary button) | `createAdmissionRules` POST `/admission-rules` | AdmissionRules | AdmissionRules | — | opens modal first |
| Save admission rules (secondary button) | `updateAdmissionRules` PUT `/admission-rules/{profileId}` | AdmissionRules | AdmissionRules | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before … | opens modal first |

**Data it reads**: `listAdmissionRules` (onLoad, List admission profiles)

**Where the user goes next**

- → `BO-001` Queue Directory: *Queue Directory*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The admission profiles list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the admission profiles untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No admission profiles yet. Offers Create admission rules (`createAdmissionRules`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listAdmissionRules` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SCOPE_VIEW`, which `listAdmissionRules` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A count missing for an n* entry mode, days missing for a relative validity anchor, or validity.to before validity.from |

#### Permissions

- `listAdmissionRules` → `SCOPE_VIEW` (read) · staff
- `createAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `updateAdmissionRules` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `setEntryRulePoints` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `SCOPE_VIEW`, which `listAdmissionRules` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.7 | The system should support multiple validity rules access entitlements associated with a ticket. The available entry rules can be changed without required additional development effort for configuring … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.10 | The system should be able to expire a ticket if it is not used within a specified time (e.g. 20 minutes) from the admission time specified on the ticket or based on the time of the performance/event. … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.59 | Some tickets may be entitled to reentry. | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 3.2.70 | The access control rules can support all multi-park requirements, such as but not limited to: -multi-park access on different days, -crossover feature i.e. access to another park on the same day as … | Admission and Access | CONTRACTED | `listAdmissionRules` |
| 7.4.22 | For special ticket, it can be restricted to particular group of people and have precondition ex: companion ticket | F&B POS | CONTRACTED | `listAdmissionRules` |
| 7.4.25 | For each PLU, it is possible to manage Usage zone or attraction access control restriction | F&B POS | CONTRACTED | `listAdmissionRules` |
| 1.1.51 | Admission entitlement management | Ticketing Catalogue | CONTRACTED | `createAdmissionRules` |
| 3.2.34 | The access rules can be modified even after the ticket has been issued. | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.62 | It must be possible to change the access control organization process on special dates. Venue is organizing on regular basis free view days where the main gate access control doors are opened letting … | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 3.2.71 | The access control can support special requirements for special events such as but not limited to: -definition of a specific product that can capture attendance without physical admission, -special … | Admission and Access | CONTRACTED | `updateAdmissionRules` |
| 1.5.5 | The system should allow specification of rules and conditions associated with a ticket. These rules and conditions will govern the usage of the ticket and any transactions associated with a ticket … | Ticketing Catalogue | CONTRACTED | data `AdmissionRules` |
| 3.2.9 | The system should have the possibility to activate/deactivate the biometric check on some type of tickets. For example, membership passes, annual pass holder, multi day and multi attraction tickets. | Admission and Access | CONTRACTED | data `AdmissionRules` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Tiered access (e.g. Bronze/Silver/Gold): the client fills a matrix of which gates/attractions each tier may scan into; configured as location → admission profile → gate → access point, with explicit deny rules (e.g. Gold denied at the Silver/Bronze entrance). *(agreed · MoM 7 Aug 2026, 24. Tiered Ticketing & Access Control Deep Dive · DI-185)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-032` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (94), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-032?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create admission rules, Save admission rules.
- [ ] Every transition is wired: `BO-001`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-033` Blacklist Management

**Bar a media code outright.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `access` module |
| Block | Block A · ticket #17918 (APP-SETUP-BO-033) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listBlacklist` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `mediaCode` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/blacklist-management` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**Form: Add blacklist entry** (modal, opened by *Add blacklist entry*; *Add blacklist entry* calls `addBlacklistEntry`, *Cancel* sends nothing)

**Collects what `addBlacklistEntry` sends before it is called.** Required: `mediaCode`, `reason`. Optional: `expiresAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Media code `mediaCode` | text area | required | — | max length 256 | — | — | `addBlacklistEntry` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `addBlacklistEntry` body |
| Expires at `expiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `addBlacklistEntry` body |

Errors to draw in the form: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …

#### Outputs: what the screen shows and produces

**Shown**

**Every blacklist entry** (data table, from `listBlacklist`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | Unique within the tenant (decided 28 September, audit R108): one entry per code. |
| Reason | text | — |
| Added at | 1 Oct 2026, 14:30 | — |
| Added by principal | the name it points at, never the id | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**The selected blacklist entry** (detail panel, from `listBlacklist`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | Unique within the tenant (decided 28 September, audit R108): one entry per code. |
| Reason | text | — |
| Added at | 1 Oct 2026, 14:30 | — |
| Added by principal | the name it points at, never the id | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Add blacklist entry (primary button) | `addBlacklistEntry` POST `/blacklist` | inline | BlacklistEntry | 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … | opens modal first |
| Remove blacklist entry (destructive button) | `removeBlacklistEntry` DELETE `/blacklist/{mediaCode}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Data it reads**: `listBlacklist` (onLoad, List blacklisted media)

**Where the user goes next**

- → `BO-001` Queue Directory: *Queue Directory*

**What opens over it**

- confirmDialog *Remove blacklist entry*: **Names what `removeBlacklistEntry` changes and what it leaves alone**, in the consequence rather than the verb. A blacklist this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The blacklist list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the blacklist untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No blacklist yet. Offers Add blacklist entry (`addBlacklistEntry`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listBlacklist` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SCOPE_VIEW`, which `listBlacklist` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … |

#### Permissions

- `listBlacklist` → `SCOPE_VIEW` (read) · staff
- `addBlacklistEntry` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `removeBlacklistEntry` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `SCOPE_VIEW`, which `listBlacklist` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.6 | The system should be able to validate tickets and membership passes with different rules based on entitlements, manage black and white list of tickets. Upon a scanning a valid ticket, the system … | Admission and Access | CONTRACTED | `listBlacklist` |
| 3.1.4 | The system shall immediately invalidate dynamic QR codes when tickets are refunded, cancelled, transferred, exchanged, upgraded, or re-issued. | Admission and Access | CONTRACTED | `addBlacklistEntry` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-033` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-033?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Add blacklist entry, Remove blacklist entry.
- [ ] Every transition is wired: `BO-001`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
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

**16 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"acceptWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/accept","contract":"maintenance","summary":"The assignee takes the job","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"addBlacklistEntry": {"method":"POST","path":"/blacklist","contract":"access","summary":"Blacklist a media code","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"BlacklistEntry"},
"approveRefund": {"method":"POST","path":"/refunds/{refundId}/approve","contract":"orders","summary":"Approve a refund held for approval","permission":"ORDER_REFUND_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Refund"},
"attachWorkOrderEvidence": {"method":"POST","path":"/work-orders/{workOrderId}/attachments","contract":"maintenance","summary":"Photo, video, document, note or signature","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrderAttachment"},
"callNextParties": {"method":"POST","path":"/queues/{queueId}/call-next","contract":"queue","summary":"Call the next parties forward","permission":"QUEUE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"cancelPerformance": {"method":"POST","path":"/performances/{performanceId}/cancel","contract":"catalogue","summary":"Cancel a performance","permission":"PERFORMANCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PerformanceCancellationResult"},
"cancelWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/cancel","contract":"maintenance","summary":"Cancel a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"closeWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/close","contract":"maintenance","summary":"Administratively closed","permission":"MAINTENANCE_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"completeWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/complete","contract":"maintenance","summary":"Complete a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"configureQueueFeed": {"method":"PUT","path":"/queue-feeds","contract":"queue","summary":"Configure a sensor feed","permission":"QUEUE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"QueueFeed","responds":"QueueFeed"},
"createAdmissionRules": {"method":"POST","path":"/admission-rules","contract":"access","summary":"Create an admission profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AdmissionRules","responds":"AdmissionRules"},
"createAsset": {"method":"POST","path":"/assets","contract":"maintenance","summary":"Register an asset","permission":"ASSET_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateAssetRequest","responds":"Asset"},
"createBulkRefund": {"method":"POST","path":"/refunds/bulk","contract":"orders","summary":"Refund every order against an event, performance or date","permission":"ORDER_REFUND_BULK","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createCampaign": {"method":"POST","path":"/campaigns","contract":"marketing-crm","summary":"Create a campaign","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCampaignRequest","responds":"Campaign"},
"createEvent": {"method":"POST","path":"/events","contract":"catalogue","summary":"Create an event","permission":"EVENT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateEventRequest","responds":"Event"},
"createPerformances": {"method":"POST","path":"/events/{eventId}/performances","contract":"catalogue","summary":"Create performances, singly or by schedule","permission":"PERFORMANCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"CreatePerformancesRequest","responds":null},
"createQueue": {"method":"POST","path":"/queues","contract":"queue","summary":"Create a queue","permission":"QUEUE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateQueueRequest","responds":"Queue"},
"createWorkOrder": {"method":"POST","path":"/work-orders","contract":"maintenance","summary":"Raise a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateWorkOrderRequest","responds":"WorkOrder"},
"getAsset": {"method":"GET","path":"/assets/{assetId}","contract":"maintenance","summary":"Read an asset with history and documents","permission":"ASSET_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AssetDetail"},
"getAssetHistory": {"method":"GET","path":"/assets/{assetId}/history","contract":"maintenance","summary":"Service history","permission":"ASSET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getCampaign": {"method":"GET","path":"/campaigns/{campaignId}","contract":"marketing-crm","summary":"Read a campaign with performance","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CampaignDetail"},
"getCampaignPerformance": {"method":"GET","path":"/campaigns/{campaignId}/performance","contract":"marketing-crm","summary":"Delivery and engagement","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CampaignPerformance"},
"getEvent": {"method":"GET","path":"/events/{eventId}","contract":"catalogue","summary":"Read an event","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Event"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getPerformance": {"method":"GET","path":"/performances/{performanceId}","contract":"catalogue","summary":"Read a performance","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Performance"},
"getQueue": {"method":"GET","path":"/queues/{queueId}","contract":"queue","summary":"Read a queue with live position","permission":"QUEUE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"QueueDetail"},
"getQueueFeedHealth": {"method":"GET","path":"/queue-feeds/{feedId}/health","contract":"queue","summary":"Feed health","permission":"QUEUE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"QueueFeedHealth"},
"getSeatAvailability": {"method":"GET","path":"/performances/{performanceId}/seat-availability","contract":"seating","summary":"Seat status for a performance","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"sectionCode","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"availableOnly","in":"query","required":null},{"name":"mode","in":"query","required":null}],"requestBody":null,"responds":"SeatAvailability"},
"getWaitTimes": {"method":"GET","path":"/queues/wait-times","contract":"queue","summary":"Wait times across a venue","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":true},{"name":"category","in":"query","required":null}],"requestBody":null,"responds":"WaitTime"},
"getWorkOrder": {"method":"GET","path":"/work-orders/{workOrderId}","contract":"maintenance","summary":"Read a work order","permission":"WORK_ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WorkOrderDetail"},
"launchCampaign": {"method":"POST","path":"/campaigns/{campaignId}/launch","contract":"marketing-crm","summary":"Launch or schedule a campaign","permission":"MARKETING_SEND","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listAccessPoints": {"method":"GET","path":"/access-points","contract":"access","summary":"List access points","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAdmissionRules": {"method":"GET","path":"/admission-rules","contract":"access","summary":"List admission profiles","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAssets": {"method":"GET","path":"/assets","contract":"maintenance","summary":"List assets","permission":"ASSET_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"maintenanceDue","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listBlacklist": {"method":"GET","path":"/blacklist","contract":"access","summary":"List blacklisted media","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCampaigns": {"method":"GET","path":"/campaigns","contract":"marketing-crm","summary":"List campaigns","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listEvents": {"method":"GET","path":"/events","contract":"catalogue","summary":"List events","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listParkingFacilities": {"method":"GET","path":"/parking-facilities","contract":"access","summary":"Car parks at a venue, and how each integrates","permission":"PARKING_CONFIGURE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPerformances": {"method":"GET","path":"/events/{eventId}/performances","contract":"catalogue","summary":"List performances of an event","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"language","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listQueueEntries": {"method":"GET","path":"/queues/{queueId}/entries","contract":"queue","summary":"List entries in a queue","permission":"QUEUE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listQueueFeeds": {"method":"GET","path":"/queue-feeds","contract":"queue","summary":"List configured sensor feeds","permission":"QUEUE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"QueueFeed"},
"listQueues": {"method":"GET","path":"/queues","contract":"queue","summary":"List queues","permission":"QUEUE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"openOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkOrders": {"method":"GET","path":"/work-orders","contract":"maintenance","summary":"List work orders","permission":"WORK_ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assignedToPrincipalId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"priority","in":"query","required":null},{"name":"assetId","in":"query","required":null},{"name":"overdueOnly","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"lookupAsset": {"method":"GET","path":"/assets/lookup","contract":"maintenance","summary":"Find an asset by tag or QR","permission":"ASSET_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assetTag","in":"query","required":null},{"name":"serialNumber","in":"query","required":null}],"requestBody":null,"responds":"AssetDetail"},
"pauseCampaign": {"method":"POST","path":"/campaigns/{campaignId}/pause","contract":"marketing-crm","summary":"Pause a campaign mid-send","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Campaign"},
"recommendSeats": {"method":"POST","path":"/performances/{performanceId}/seat-recommendations","contract":"seating","summary":"Recommend seats for a party","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SeatRecommendationRequest","responds":null},
"removeBlacklistEntry": {"method":"DELETE","path":"/blacklist/{mediaCode}","contract":"access","summary":"Remove a blacklist entry","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"requestSuggestion": {"method":"POST","path":"/ai/suggestions","contract":"ai","summary":"Ask for an answer, however it is currently produced","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Suggestion"},
"setAssetStatus": {"method":"PUT","path":"/assets/{assetId}/status","contract":"maintenance","summary":"Take an asset out of service or return it","permission":"ASSET_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetAssetStatusRequest","responds":"AssetStatusResult"},
"setEntryRulePoints": {"method":"PUT","path":"/admission-rules/{ruleId}/points","contract":"access","summary":"Set the access points an admission rule covers","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"ruleId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":"AccessEntryRulePoint","responds":"AccessEntryRulePoint"},
"setParkingFacility": {"method":"PUT","path":"/parking-facilities","contract":"access","summary":"Configure a car park and its integration","permission":"PARKING_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ParkingFacility","responds":"ParkingFacility"},
"setQueueStatus": {"method":"PUT","path":"/queues/{queueId}/status","contract":"queue","summary":"Open, pause or close a queue","permission":"QUEUE_MANAGE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"QueueStatusResult"},
"setWaitTime": {"method":"PUT","path":"/queues/{queueId}/wait-time","contract":"queue","summary":"Manually set a wait time","permission":"QUEUE_MANAGE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WaitTime"},
"stopCampaign": {"method":"POST","path":"/campaigns/{campaignId}/stop","contract":"marketing-crm","summary":"Stop a campaign mid-send","permission":"MARKETING_SEND","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Campaign"},
"testQueueFeed": {"method":"POST","path":"/queue-feeds/{feedId}/test","contract":"queue","summary":"Test a feed before trusting it","permission":"QUEUE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FeedTestResult"},
"testSendCampaign": {"method":"POST","path":"/campaigns/{campaignId}/test-send","contract":"marketing-crm","summary":"Send a test to named recipients","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"unscheduleCampaign": {"method":"POST","path":"/campaigns/{campaignId}/unschedule","contract":"marketing-crm","summary":"Pull a scheduled campaign before it sends","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Campaign"},
"updateAccessPoint": {"method":"PATCH","path":"/access-points/{accessPointId}","contract":"access","summary":"Update an access point","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessPoint"},
"updateAdmissionRules": {"method":"PUT","path":"/admission-rules/{profileId}","contract":"access","summary":"Update an admission profile","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AdmissionRules","responds":"AdmissionRules"},
"updateAsset": {"method":"PATCH","path":"/assets/{assetId}","contract":"maintenance","summary":"Amend an asset","permission":"ASSET_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Asset"},
"updateCampaign": {"method":"PATCH","path":"/campaigns/{campaignId}","contract":"marketing-crm","summary":"Amend, pause or resume a campaign","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Campaign"},
"updateEvent": {"method":"PATCH","path":"/events/{eventId}","contract":"catalogue","summary":"Amend an event","permission":"EVENT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Event"},
"updatePerformance": {"method":"PATCH","path":"/performances/{performanceId}","contract":"catalogue","summary":"Amend a performance","permission":"PERFORMANCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Performance"},
"updateQueue": {"method":"PATCH","path":"/queues/{queueId}","contract":"queue","summary":"Amend queue configuration","permission":"QUEUE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Queue"},
"verifyWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/verify","contract":"maintenance","summary":"Supervisor verification","permission":"WORK_ORDER_VERIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessEntryRulePoint": {"type":"object","x-ticvai-persistence":"access.entry_rule_point","description":"**Taken from the backend workbook, 20 September.** Maps the access points that are allowed for an admission profile.","required":["admissionProfileId","accessPointId","isActive","createdAt"],"properties":{"admissionProfileId":{"type":"string","format":"uuid","readOnly":true},"accessPointId":{"type":"string","format":"uuid"},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"id":{"type":"string","format":"uuid","readOnly":true}}},
"AccessPoint": {"x-ticvai-persistence":"access.access_point","type":"object","required":["id","code","name","venueId","operatingMode","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"externalCredentialSources":{"allOf":[{"$ref":"#/components/schemas/ExternalCredentialSourceList"}],"description":"BL-108. **A hotel room card admitting a guest to a water park** — externally issued, and the platform validates it without having sold it.\n**The entitlement is created on first use, not on check-in.** A hotel with 400 rooms does not want 400 entitlements a night for guests who never visit.\n"},"scanAnomalyRules":{"allOf":[{"$ref":"#/components/schemas/ScanAnomalyRuleList"}],"description":"BL-104. **Rule-based scan anomalies, separated from the parked model-based engine** — device sharing, simultaneous entries at two gates, an impossible walking time between them.\n**These are deterministic and need no model**, which is why they are here and not in `ai`: two entries eight seconds apart at gates four hundred metres apart is arithmetic.\n"},"operatingMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}],"default":"normal","description":"**Set by the podium with `setTurnstileMode`, and it wins** (audit R221). BL-107 and BL-109. **A closed turnstile and one in emergency drop-arm mode look the same in the model and are opposite in meaning.** Closed refuses everybody; drop-arm lets everybody through, and it is the state that exists for an evacuation.\n**`podium` is a supervised validation position** — a member of staff directing a group through a lane, validating by eye against a list. It scans nothing and it is how school parties actually enter.\n**`freeFlow` counts without validating.** Useful at a free event, and a mode that must be visibly distinct from a broken reader.\n"},"vehicleLocationCapture":{"type":"boolean","default":false,"description":"BL-023. **Nothing helped a guest find their vehicle.** Where the access point is a car park entry, the level and zone are captured against the visit so the app can answer it — **the guest who cannot find their car at 11pm is the last impression of the day.**\n"},"mode":{"allOf":[{"$ref":"#/components/schemas/TurnstileMode"}],"nullable":true,"description":"Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates in its fixed `direction` (audit R221).\n"},"direction":{"allOf":[{"$ref":"#/components/schemas/Direction"}],"description":"**Fixed per access point** (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium.\n"},"antiPassbackEnabled":{"type":"boolean"},"requiresExitBeforeReentry":{"type":"boolean","default":false,"description":"Written by `createAccessPoint` and `updateAccessPoint`, and returned so the edit form reads back what it wrote."},"driver":{"type":"string","nullable":true,"description":"Driver identifier for the controller behind this access point, as written by `createAccessPoint` and `updateAccessPoint`. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific.\n"},"geofence":{"allOf":[{"$ref":"#/components/schemas/AccessPointGeofence"}],"nullable":true,"description":"Written by `setAccessPointGeofence`; null until one is set. **One `jsonb` column on the access point row** (`access.access_point.geofence`), read with the point when a handheld validates against it.\n"},"isActive":{"type":"boolean"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true}}},
"AccessPointGeofence": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"Where a handheld may validate for one access point, and what happens outside it. The body of `setAccessPointGeofence` and the value of `AccessPoint.geofence`.\n","required":["enforcement"],"properties":{"latitude":{"type":"number"},"longitude":{"type":"number"},"radiusMetres":{"type":"integer","minimum":5,"maximum":5000},"enforcement":{"type":"string","enum":["off","warn","deny"],"description":"`off` keeps the fence on record and checks nothing; `warn` lets a validation from outside the fence through with a warning; `deny` refuses it.\n"},"allowProximityBeacon":{"type":"boolean","description":"Accept a BLE proximity assertion in place of GPS. Better indoors."}}},
"AccessPointOperatingMode": {"type":"string","description":"BL-107 and BL-109. **What the gate does, and what the podium sets** (`setTurnstileMode`, decided 28 September, audit R221). `closed` refuses everybody; `dropArm` lets everybody through and exists for an evacuation; `podium` is supervised validation by eye; `freeFlow` counts without validating; `maintenance` takes the lane out of use.\n","enum":["normal","freeFlow","dropArm","closed","podium","maintenance"]},
"AdmissionRules": {"x-ticvai-persistence":"access.admission_rules","type":"object","required":["id","code","name","openMinutesBefore","closeMinutesAfter"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Server-assigned.** Ignored in a `createAdmissionRules` or `updateAdmissionRules` body; on update the profile is the one the path names.\n"},"code":{"type":"string","maxLength":64},"perProductRules":{"allOf":[{"$ref":"#/components/schemas/PerProductRuleList"}],"description":"BL-059. **Transaction rules were per profile and a ticket type could not state its own.** An annual pass allowing one entry per day and a single ticket allowing one entry ever are different rules, and forcing a profile per product multiplies profiles instead.\n"},"name":{"type":"string","maxLength":200},"openMinutesBefore":{"type":"integer","description":"How long before a performance validation opens."},"closeMinutesAfter":{"type":"integer"},"maxDurationMinutes":{"type":"integer","nullable":true},"requiresExitBeforeReentry":{"type":"boolean","default":false},"maxReentries":{"type":"integer","nullable":true},"entryLimit":{"type":"object","description":"**How many times the credential may enter** (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). Absent means `unlimited`.","required":["mode"],"properties":{"mode":{"type":"string","enum":["unlimited","once","nTimes","nPerDay","nPerPeriod"],"default":"unlimited"},"count":{"type":"integer","minimum":1,"description":"N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it)"},"periodDays":{"type":"integer","minimum":1,"description":"The period for nPerPeriod"}}},"exitScan":{"type":"string","enum":["required","optional","none"],"default":"optional","description":"(decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. `optional`: exits run in free rotation and headcount is inferred. `none`: the exit has no reader."},"maxExits":{"type":"integer","minimum":0,"nullable":true,"description":"Null is unlimited (decided 29 September, VM close-out)"},"reEntryWindowMinutes":{"type":"integer","minimum":1,"nullable":true,"description":"Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out)"},"sameDayOnly":{"type":"boolean","default":true,"description":"Re-entry only on the day of the exit (decided 29 September, VM close-out)"},"designatedAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out)"},"validity":{"type":"object","description":"**When the credential is valid** (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). The admission window above still applies inside it.","required":["anchor"],"properties":{"anchor":{"type":"string","enum":["fixedRange","afterSale","afterActivation","afterFirstUse"],"description":"fixedRange uses from and to; the others count days from the event"},"days":{"type":"integer","minimum":1,"description":"N days after the anchor; required unless the anchor is fixedRange"},"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date","description":"Inclusive. Must not be before from (`422`)"},"endOf":{"type":"string","enum":["day","week","month","year"],"nullable":true,"description":"Validity runs to the end of the day, week, month or year the relative period ends in"},"daysOfWeek":{"type":"array","items":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"description":"Empty is every day"},"dayTypes":{"type":"array","items":{"type":"string","enum":["peakDates","offPeakDates","holidays","seasons","eventDates"]},"description":"Calendar day types on which access is allowed; empty is every day type"},"blackoutDates":{"type":"array","items":{"type":"string","format":"date"},"description":"Dates on which access is refused whatever else allows it"}}},"crossover":{"type":"object","nullable":true,"description":"**Crossover between parks** (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. Null means the profile admits to one park only.","required":["allowedParkOrgUnitIds"],"properties":{"allowedParkOrgUnitIds":{"type":"array","minItems":2,"items":{"type":"string","format":"uuid"}},"parkOrder":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Required order of parks, if any; empty is any order"},"sameDayOnly":{"type":"boolean","default":true},"differentDayAccess":{"type":"boolean","default":false},"dayPattern":{"type":"string","enum":["consecutiveFromFirstScan","flexibleWithinValidity"],"default":"flexibleWithinValidity"},"maxParkEntries":{"type":"integer","minimum":1,"nullable":true,"description":"Null is unlimited"},"crossoverQuantity":{"type":"integer","minimum":1,"nullable":true,"description":"How many crossovers; null is unlimited"},"crossoverAfterTime":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Earliest venue-local time HH:MM a crossover is allowed"},"prerequisiteParkOrgUnitId":{"type":"string","format":"uuid","nullable":true,"description":"The park that must be entered first"},"reEntryAfterCrossover":{"type":"boolean","default":false}}},"allowedAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Empty means any access point in the venue."},"reEntryVerification":{"type":"string","enum":["credentialOnly","credentialUvStamp","credentialFace","credentialOperator","custom"],"default":"credentialOnly","description":"What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1)."},"ruleConditions":{"type":"object","nullable":true,"description":"The visual rule builder body `setVisualAccessRule` writes: `appliesTo` (products or credential types), `conditions`, `logic` (AND / OR / NOT over the conditions), `decision` (allow, deny, referToOperator, overrideEligible) and `consequences`. **One `jsonb` column on the rule row**, read with the rule and never queried on its own; the locations stay in `access.entry_rule_point` (added 29 September, data-model close-out DM1)."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"Asset": {"x-ticvai-persistence":"maintenance.asset","allOf":[{"$ref":"#/components/schemas/CreateAssetRequest"},{"type":"object","x-ticvai-retired-columns":["is_maintenance_overdue","document_refs"],"required":["id","status"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid","nullable":true,"description":"1.2.x. **Where this asset is also bookable.** An AV rig is an asset to maintain and a resource to allocate, and they are the same object seen from two sides.\n**`resources` owns the calendar and this owns the condition.** An asset out of service makes its resource unbookable, which is one link rather than two models of availability.\n"},"deviceId":{"type":"string","format":"uuid","nullable":true,"description":"BL-160. **Where this asset is also a registered device.** A turnstile is an asset to maintain and a device to operate, and — exactly as with `resourceId` above — they are the same object seen from two sides.\n**Nothing joined them before this.** A turnstile controller reporting `needsAttention` could not raise a work order against itself, and an engineer closing one had no way back to the device whose firmware caused it.\n**Null for most assets and for most devices.** A chiller is not a device and a signature pad is not on the asset register; the link is sparse, and it lives here rather than on `platform.device` because `platform` is the foundation tier and a foreign key pointing from it into `maintenance` would invert the tiers — every cell running a spine would carry a column for a satellite it may not deploy.\n"},"acquisitionCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"acquiredOn":{"type":"string","format":"date","nullable":true},"depreciation":{"type":"object","nullable":true,"description":"**Recorded here and posted by `finance`.** Depreciation is an accounting act and the asset register is where the useful life is actually known — an engineer knows a chiller lasts fifteen years and an accountant knows what to do about it.\n","properties":{"method":{"type":"string","enum":["straightLine","reducingBalance","unitsOfProduction","none"]},"usefulLifeMonths":{"type":"integer"},"residualValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"accumulatedDepreciation":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"retiredOn":{"type":"string","format":"date","nullable":true,"description":"**Retirement is not deletion.** A work order from three years ago still names this asset, and an inspection record with no asset is an inspection of nothing.\n"},"disposalProceeds":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"$ref":"#/components/schemas/AssetStatus"},"statusReason":{"type":"string","nullable":true},"openWorkOrderCount":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Work orders on this asset whose status is `open`, `assigned`, `inProgress`, `paused` or `awaitingParts` — the same set `AssetDetail.openWorkOrders` returns. **Maintained on write**: `createWorkOrder` and every transition into or out of that set (complete, cancel, close, reject back to open) adjust it in the same transaction as the work-order row.\n"},"nextMaintenanceDueAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The earliest `nextDueAt` among this asset's active maintenance plans; null when none has one. **Maintained on write**: recomputed whenever one of those plans is created, amended, suspended or has its `nextDueAt` moved by a completed work order. `listAssets?maintenanceDue` filters on this column against the clock.\n"},"isMaintenanceOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`nextMaintenanceDueAt` is in the past at the moment of the read. **Computed on read and not stored** — it depends on the clock, so a stored copy is stale the minute after it is written.\n"},"lastInspectionAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`performedAt` of the latest inspection submitted against this asset. **Maintained on write** by `submitInspection`, in the same transaction as the inspection row; an inspection synced late with an earlier `performedAt` does not move it back.\n"},"usageCounter":{"type":"number","nullable":true,"description":"Cycles, hours or kilometres. Drives usage-based maintenance."}}}]},
"AssetCriticality": {"type":"string","enum":["safetyCritical","revenueCritical","standard","low"]},
"AssetDetail": {"x-ticvai-persistence":"maintenance.asset","allOf":[{"$ref":"#/components/schemas/Asset"},{"type":"object","properties":{"openWorkOrders":{"type":"array","items":{"$ref":"#/components/schemas/WorkOrder"}},"maintenancePlans":{"type":"array","items":{"$ref":"#/components/schemas/MaintenancePlan"}},"documents":{"type":"array","description":"Manuals, procedures, certificates. What a technician needs on site. Read from `maintenance.asset_document`.\n","items":{"$ref":"#/components/schemas/AssetDocument"}}}}]},
"AssetDocument": {"x-ticvai-persistence":"maintenance.asset_document","type":"object","description":"A document attached to an asset — manual, procedure, certificate — with the name and kind a technician needs on site. **One row per document**, because `AssetDetail.documents` returns a name and a kind for each and a `text[]` of refs has nowhere to hold either.\n","required":["id","assetId","ref"],"properties":{"id":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"ref":{"type":"string","description":"The document in the media store."},"name":{"type":"string","maxLength":200,"nullable":true},"kind":{"allOf":[{"$ref":"#/components/schemas/AssetDocumentKind"}],"nullable":true,"description":"Null where the document arrived as a bare ref in `documentRefs`."}}},
"AssetDocumentInput": {"x-ticvai-persistence":"none — request only","type":"object","required":["ref","kind"],"properties":{"ref":{"type":"string","description":"The document in the media store."},"name":{"type":"string","maxLength":200},"kind":{"$ref":"#/components/schemas/AssetDocumentKind"}}},
"AssetDocumentKind": {"type":"string","enum":["manual","sop","certificate","warranty","drawing","riskAssessment"]},
"AssetHistoryEntry": {"x-ticvai-persistence":"none — union view over work orders, inspections, incidents and asset status changes","type":"object","description":"**Every kind has a source.** `workOrder` is a work-order row, `inspection` an inspection, `incident` an incident, `statusChange` a `maintenance.asset_status_change` row. `partReplaced` is a completed work order whose `resolutionCode` is `partReplaced`, and `planCompleted` a completed work order with a `sourcePlanId` — both read from `maintenance.work_order`, not stored twice.\n","required":["kind","occurredAt","summary"],"properties":{"kind":{"type":"string","enum":["workOrder","inspection","incident","statusChange","partReplaced","planCompleted"]},"referenceId":{"type":"string","format":"uuid","nullable":true,"description":"The source row's id: a work order, inspection or incident, or an `asset_status_change` id. A uuid, as every id is (ADR-0056).\n"},"summary":{"type":"string"},"principalId":{"type":"string","format":"uuid","nullable":true},"occurredAt":{"type":"string","format":"date-time"}}},
"AssetStatus": {"type":"string","enum":["inService","outOfService","underMaintenance","awaitingParts","retired","disposed"]},
"AssetStatusResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["asset","downstreamEffects"],"properties":{"asset":{"$ref":"#/components/schemas/Asset"},"downstreamEffects":{"type":"object","description":"What else changed. Surfaced so the person taking a ride out of service sees the commercial consequence at the moment they do it.\n","properties":{"productsSuspended":{"type":"array","items":{"type":"string","format":"uuid"}},"accessPointBlocked":{"type":"boolean"},"performancesAffected":{"type":"integer"},"workOrderId":{"type":"string","format":"uuid","nullable":true}}}}},
"BlacklistEntry": {"x-ticvai-persistence":"access.blacklist","type":"object","required":["mediaCode","reason","addedAt","addedByPrincipalId"],"properties":{"mediaCode":{"type":"string","x-ticvai-unique":"tenant","description":"**Unique within the tenant** (decided 28 September, audit R108): one entry per code. `addBlacklistEntry` refuses a second entry with `409 duplicate-code`. **One code space for both lists** (decided 29 September, writers pass): a code on the blacklist cannot also be whitelisted; adding it to the other list is the same `409 duplicate-code`. Move a code between lists by removing and re-adding it."},"reason":{"type":"string"},"addedAt":{"type":"string","format":"date-time"},"addedByPrincipalId":{"type":"string","format":"uuid"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"listType":{"type":"string","enum":["blacklist","whitelist"],"default":"blacklist","description":"A blacklist entry refuses the media; a whitelist entry is an approved exception to a restriction (added 29 September, data-model close-out DM1)."},"disableScope":{"type":"string","enum":["entireCredential","venueAccess","attractionAccess","reEntry","fastPass","specificEntitlement"],"default":"entireCredential","description":"What the entry disables (added 29 September, data-model close-out DM1)."},"distributedTo":{"type":"array","items":{"type":"string","enum":["centralPlatform","venueEdge","onlineGates","offlineRevocationPackage"]},"description":"Where the restriction has been distributed so far, as `listCredentialDisableBlacklist` returns it (added 29 September, data-model close-out DM1)."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"Campaign": {"x-ticvai-persistence":"marketing.campaign","allOf":[{"$ref":"#/components/schemas/CreateCampaignRequest"},{"type":"object","required":["id","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"budgetCap":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"budgetSpent":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"BL-169. **A campaign could spend without limit** — following the promotions `budgetCap` precedent. **Sending stops at the cap rather than overspending and reporting it**, because a marketing budget discovered after it was exceeded is a budget nobody set.\n"},"status":{"$ref":"#/components/schemas/CampaignStatus"},"isPaused":{"type":"boolean"},"createdByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"},"launchedAt":{"type":"string","format":"date-time","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true},"sentCount":{"type":"integer","readOnly":true,"x-ticvai-persisted":false,"description":"**How many messages went out**, counted from `marketing.message_dispatch` at read time rather than kept as a counter on the campaign row, so it cannot drift from the dispatch records it summarises. Test sends are not dispatches of the campaign and are not counted.\n"}}}]},
"CampaignContent": {"x-ticvai-persistence":"none — embedded in campaign","type":"object","required":["templateId"],"properties":{"templateId":{"type":"string","format":"uuid"},"subjectOverride":{"type":"object","additionalProperties":{"type":"string"}},"mergeDefaults":{"type":"object","description":"Fallback values for the template's `mergeFields`, by name, used where a guest has no value.","additionalProperties":{"type":"string"}},"promotionId":{"type":"string","format":"uuid","nullable":true,"description":"Offer carried by the campaign. Coupon codes are issued from it."}}},
"CampaignDetail": {"x-ticvai-persistence":"marketing.campaign","allOf":[{"$ref":"#/components/schemas/Campaign"},{"type":"object","properties":{"performance":{"$ref":"#/components/schemas/CampaignPerformance"}}}]},
"CampaignKind": {"type":"string","enum":["oneOff","scheduled","triggered","recurring"]},
"CampaignPerformance": {"x-ticvai-persistence":"none — aggregated from marketing.message_dispatch (isTest false)","type":"object","required":["campaignId","sent","delivered"],"properties":{"campaignId":{"type":"string","format":"uuid"},"sent":{"type":"integer"},"delivered":{"type":"integer"},"opened":{"type":"integer"},"clicked":{"type":"integer"},"bounced":{"type":"integer"},"complained":{"type":"integer"},"unsubscribed":{"type":"integer"},"attributedOrders":{"type":"integer"},"attributedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"attributionWindowDays":{"type":"integer","minimum":1,"description":"The window these figures were attributed over, from `VenueSettings.marketing.attributionWindowDays` (proposed default 7, audit R094)."},"variants":{"type":"array","description":"Per variant of an A/B campaign, from `MessageDispatch.campaignVariantId` (29 September, build pass, group G2; 22.1.17). Empty for a single-content campaign.","items":{"type":"object","properties":{"variantId":{"type":"string","format":"uuid"},"label":{"type":"string"},"sent":{"type":"integer"},"opened":{"type":"integer"},"clicked":{"type":"integer"},"attributedOrders":{"type":"integer"},"attributedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isWinner":{"type":"boolean"}}}},"sendTimeOptimisedCount":{"type":"integer","description":"Messages sent at a per-recipient optimised hour rather than the scheduled time."}}},
"CampaignStatus": {"type":"string","enum":["draft","scheduled","sending","paused","completed","stopped","failed"]},
"CampaignTrigger": {"x-ticvai-persistence":"none — embedded in campaign","type":"object","properties":{"event":{"type":"string","enum":["bookingConfirmed","visitCompleted","membershipExpiring","birthday","abandonedCart","firstVisit","inactivity","entitlementExpiring"],"description":"`entitlementExpiring` (29 September, build pass, group G2; 5.5.30) fires on `entitlement.expiringSoon`: a ticket or pass the guest still holds comes within its template's `expiryNoticeDays` of `validTo`. The notice period is set on the template, so `delayHours` shifts the send within it rather than setting it. An entitlement belonging to a membership is left to `membershipExpiring`, so a member is not told twice."},"delayHours":{"type":"integer"},"conditions":{"type":"array","items":{"$ref":"#/components/schemas/SegmentCriterion"}}}},
"ConsentPurpose": {"type":"string","enum":["marketing","personalisation","profiling","thirdPartySharing","aiProcessing","transactional"]},
"CreateAssetRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["assetTag","name","venueId","criticality"],"properties":{"assetTag":{"type":"string","maxLength":64,"x-ticvai-unique":"venue","description":"**Unique per venue** (decided 28 September, audit R108). Two assets in one venue never share a tag; `createAsset` refuses a duplicate with `409` `duplicate-code`. Two venues may each have an `A-001`.\n"},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"criticality":{"$ref":"#/components/schemas/AssetCriticality"},"priorityOverride":{"allOf":[{"$ref":"#/components/schemas/WorkOrderPriority"}],"nullable":true,"description":"**\"If this device goes down, raise this priority\"** (decided 17 September, M17-01). A corrective work order raised on this asset takes this priority instead of the score. Null means the score decides.\n"},"manufacturer":{"type":"string","maxLength":200},"model":{"type":"string","maxLength":200},"serialNumber":{"type":"string","maxLength":128},"commissionedAt":{"type":"string","format":"date"},"warrantyExpiresAt":{"type":"string","format":"date"},"supplierId":{"type":"string","format":"uuid"},"linkedProductIds":{"type":"array","description":"Products this asset delivers. A fault here can stop them selling.\n","items":{"type":"string","format":"uuid"}},"linkedAccessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Access point this asset controls. Out of service blocks it."},"requiresInspectionToReturn":{"type":"boolean","default":false,"description":"True means a completed inspection is required before return to service. A technician cannot simply declare a ride safe.\n"},"documents":{"type":"array","description":"Manuals, procedures, certificates, each with its name and kind. Stored one row per document in `maintenance.asset_document`, which is where `AssetDetail.documents` reads them from.\n","items":{"$ref":"#/components/schemas/AssetDocumentInput"}},"documentRefs":{"type":"array","x-ticvai-persisted":false,"description":"**The refs alone, kept for callers that predate `documents`.** Each ref sent here is stored as an `asset_document` row with no name and no kind. Returned as the refs of `documents`, computed on read — there is no second copy to fall out of step.\n","items":{"type":"string"}}}},
"CreateCampaignRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","kind","channel","segmentId","content"],"properties":{"name":{"type":"string","maxLength":200},"kind":{"$ref":"#/components/schemas/CampaignKind"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"venueId":{"type":"string","format":"uuid"},"segmentId":{"type":"string","format":"uuid"},"content":{"$ref":"#/components/schemas/CampaignContent"},"trigger":{"$ref":"#/components/schemas/CampaignTrigger"},"scheduledFor":{"type":"string","format":"date-time"},"consentPurpose":{"allOf":[{"$ref":"#/components/schemas/ConsentPurpose"}],"default":"marketing"},"sendWindow":{"type":"object","description":"Hours during which sending is permitted. A promotional message at 3am is a complaint waiting to happen.\n","properties":{"startTime":{"type":"string"},"endTime":{"type":"string"},"timeZone":{"type":"string"}}},"sendTimeMode":{"type":"string","enum":["fixed","optimised"],"default":"fixed","description":"`optimised` sends each recipient at the hour `ai.requestSuggestion` (kind `sendTime`) gives for them, inside `sendWindow` (29 September, build pass, group G2; 22.3.19). `fixed` is the behaviour before. Falls back to `scheduledFor` per recipient where there is no suggestion or AI is off."},"optimiseChannel":{"type":"boolean","default":false,"description":"With `sendTimeMode` `optimised`, route each recipient to the channel the suggestion names, among the channels they consented to (22.9.16). Off keeps `channel`."},"variants":{"type":"array","maxItems":5,"nullable":true,"description":"**A/B (or up to five-way) content and subject variants** (29 September, build pass, group G2; 22.1.17, BO-772). Each is a subject override and optionally a different template, written by a person or taken from an AI draft (`ai.proposeMarketingContent`, `source` `aiDraft`). Held as rows of `marketing.campaign_variant`. Null or empty is a single-content campaign.","items":{"$ref":"#/components/schemas/MarketingCampaignVariant"}},"abTest":{"type":"object","nullable":true,"description":"How the variants are tested. Required when `variants` has two or more.","properties":{"testPercent":{"type":"integer","minimum":5,"maximum":100,"default":20,"description":"Share of the audience the variants are tested on; 100 splits everyone and picks no winner."},"successMetric":{"type":"string","enum":["openRate","clickRate","conversionRate","attributedRevenue"],"default":"clickRate"},"decideAfterHours":{"type":"integer","minimum":1,"maximum":168,"default":4},"winnerRule":{"type":"string","enum":["automatic","manual"],"default":"automatic"},"minimumSamplePerVariant":{"type":"integer","minimum":1,"default":500,"description":"Below this many sends per variant no winner is declared automatically; a person picks."},"winningVariantId":{"type":"string","format":"uuid","nullable":true,"description":"Set by the automatic rule, or by a person through `updateCampaign`."}}}}},
"CreateEventRequest": {"type":"object","required":["code","name","venueId"],"properties":{"code":{"type":"string","maxLength":64,"x-ticvai-unique":"tenant","description":"**Unique per tenant** (decided 28 September, audit R108). A code already used by any event in the tenant is refused with `409 duplicate-code`.\n"},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"parentEventId":{"type":"string","format":"uuid"}}},
"CreatePerformancesRequest": {"type":"object","required":["startsAt","endsAt"],"properties":{"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"admissionRulesId":{"type":"string","format":"uuid"},"seatMapId":{"type":"string","format":"uuid"},"language":{"type":"string","nullable":true,"maxLength":35,"pattern":"^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$","description":"As `Performance.language`; every performance of a generated series takes it (decided 29 September, rev 3 REV3-17)."},"format":{"type":"string","nullable":true,"maxLength":40,"description":"As `Performance.format` (decided 29 September, rev 3 REV3-17)."},"recurrence":{"type":"object","description":"Generate a series rather than a single performance. **Read in the region's time zone**: the Region owns the zone and every venue inherits it without override (tenancy), so `daysOfWeek` are the region's calendar days and `until` is compared on the region's clock.\n","properties":{"intervalMinutes":{"type":"integer","minimum":1},"until":{"type":"string","format":"date-time"},"daysOfWeek":{"type":"array","items":{"type":"integer","minimum":0,"maximum":6}}}}}},
"CreateQueueRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","venueId","capacityPerCycle","cycleMinutes"],"properties":{"code":{"type":"string","maxLength":64},"name":{"$ref":"#/components/schemas/LocalisedText"},"venueId":{"type":"string","format":"uuid"},"attractionProductId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true,"description":"The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["standby","singleRider","fastPass","virtual","accessible","groupOnly","staffOnly"],"default":"standby","description":"5.6.x. **A ride has several queues and the model had one.** A single-rider line and a standby line at the same attraction draw from one capacity and fill at different rates, and modelling them as one queue makes both wait estimates wrong.\n**`accessible` is not a courtesy lane.** It has its own capacity because a guest who cannot stand in a switchback needs a place to wait, not priority.\n"},"operatingWindows":{"type":"array","description":"**When the queue runs, which is not when the venue is open.** A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen.\nStored one row per window in `queue.queue_operating_window` (see `Queue`), not as a column on the queue.\n","items":{"type":"object","required":["day","from","to"],"properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Venue local time, 24-hour `HH:MM`, when the queue starts running."},"to":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Venue local time, 24-hour `HH:MM`, when the queue stops running."},"lastEntryMinutesBefore":{"type":"integer","default":0,"description":"**When the queue stops accepting, which is before it stops running.** A guest joining two minutes before close waits twenty and is turned away at the front.\n"}}}},"parentQueueId":{"type":"string","format":"uuid","nullable":true,"description":"Where several queues share one capacity. **The standby and single-rider lines at one ride draw from the same cycles**, and a parent is how that is expressed without either queue owning the other.\n"},"loadBalanceWithQueueIds":{"type":"array","description":"BL-137. **Two rides with the same theme and different waits**, and nothing directed a guest to the shorter one. Load balancing is an offer, not an assignment — **a guest sent to a ride they did not choose is a guest who feels managed.**\n","items":{"type":"string","format":"uuid"}},"inQueueOfferEnabled":{"type":"boolean","default":false,"description":"**A guest with twenty minutes to wait is a guest with twenty minutes to buy something.** Offers surface in the wait screen and are the only reason a virtual queue earns its infrastructure.\n"},"notifyBeforeCallMinutes":{"type":"integer","default":5,"description":"BL-017, 19.2.61. **A guest was not told their turn was approaching**, which makes a virtual queue worse than a physical one — at least a line is visible.\n"},"capacityPerCycle":{"type":"integer","minimum":1},"cycleMinutes":{"type":"number","minimum":0},"maxPartySize":{"type":"integer","default":6},"returnWindowMinutes":{"type":"integer","default":15,"description":"How long a called party has to arrive before the entry expires."},"heightRequirementCm":{"type":"integer","nullable":true},"fastPassAllocationPercent":{"type":"number","minimum":0,"maximum":100,"default":0,"description":"Share of each cycle reserved for Fast Pass holders."},"zone":{"type":"string","nullable":true},"fastPass":{"allOf":[{"$ref":"#/components/schemas/QueueFastPass"}],"nullable":true,"description":"The lane's Fast Pass block (decided 29 September, VM close-out). Null on a queue that takes no Fast Pass.\n"}}},
"CreateWorkOrderRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","title","venueId","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"title":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":5000},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"kind":{"allOf":[{"$ref":"#/components/schemas/WorkOrderKind"}],"default":"corrective"},"priority":{"allOf":[{"$ref":"#/components/schemas/WorkOrderPriority"}],"description":"**Optional since 29 September** (M17-01). Sent, it is `manual` and wins. Absent, the asset's `priorityOverride` applies, and failing that the venue's `WorkOrderPriorityPolicy` scores the fault.\n"},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","maxItems":10,"items":{"type":"string"},"description":"Skills the job needs, as qualification codes; `suggestWorkOrderAssignee` ranks by them (M17-13)."},"categoryId":{"type":"string","format":"uuid"},"assignedToPrincipalId":{"type":"string","format":"uuid"},"dueAt":{"type":"string","format":"date-time"},"attachmentRefs":{"type":"array","description":"Photo-first. Expected at creation, not added later from memory.","items":{"type":"string"}},"takeAssetOutOfService":{"type":"boolean","default":false,"description":"Raise and immediately suspend the asset. For a fault found on a live ride, the two are one action.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"Direction": {"type":"string","enum":["entry","exit","reentry","crossover"]},
"Event": {"x-ticvai-persistence":"catalogue.event","type":"object","required":["id","code","name","venueId","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentEventId":{"type":"string","format":"uuid","nullable":true,"description":"For grouped events."},"performanceCount":{"type":"integer","readOnly":true,"description":"How many performances the event has. Counted by the server; never sent by a client."},"isActive":{"type":"boolean"}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"ExternalCredentialSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.external_credential_sources`). Read with the access point when a credential is presented; a source is never queried on its own.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["hotelRoomCard","corporateBadge","cityPass","transitCard","partnerToken"]},"providerName":{"type":"string"},"endpoint":{"type":"string"},"credentialRef":{"type":"string"},"grantsProductId":{"type":"string","format":"uuid"}}}},
"FeedTestResult": {"type":"object","x-ticvai-persistence":"none — computed, discarded","required":["succeeded","checks","testedAt"],"properties":{"succeeded":{"type":"boolean"},"checks":{"type":"array","items":{"type":"object","required":["check","passed"],"properties":{"check":{"type":"string","enum":["reachable","authenticated","payloadParsed","readingMapped","withinInterval"]},"passed":{"type":"boolean"},"detail":{"type":"string"},"latencyMs":{"type":"integer","nullable":true}}}},"sampleReading":{"allOf":[{"$ref":"#/components/schemas/QueueReading"}],"description":"What the source actually returned, mapped. Shown so a configurer can see whether \"people count 4\" means four people or four groups before it drives a board.\n"},"rawSample":{"type":"string","nullable":true,"description":"Truncated raw payload. The only way to diagnose a source that is reachable and returning a shape nobody mapped.\n"},"testedAt":{"type":"string","format":"date-time"}}},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MaintenancePlan": {"x-ticvai-persistence":"maintenance.preventive_plan","type":"object","required":["id","name","assetId","taskTemplate"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":200},"assetId":{"type":"string","format":"uuid"},"assetCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"Applies to every asset in the category rather than one."},"intervalDays":{"type":"integer","nullable":true,"description":"Elapsed-time trigger."},"usageInterval":{"type":"number","nullable":true,"description":"Usage trigger — cycles, hours, kilometres. **Whichever comes first** when both are set. A ride serviced every three months or ten thousand cycles is one plan.\n"},"leadTimeDays":{"type":"integer","default":7,"description":"How far ahead the work order is generated, so parts can be ordered before the job is already late.\n"},"taskTemplate":{"type":"object","required":["title","priority"],"properties":{"title":{"type":"string"},"description":{"type":"string"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"estimatedMinutes":{"type":"integer"},"inspectionTemplateId":{"type":"string","format":"uuid"},"requiredPartIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},"lastCompletedAt":{"type":"string","format":"date-time","nullable":true},"nextDueAt":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"}}},
"MarketingCampaignVariant": {"type":"object","x-ticvai-persistence":"marketing.campaign_variant","description":"One content or subject variant of a campaign, for an A/B test (22.1.17; 29 September, build pass, group G2, from group G1's handoff). Written with its campaign by `createCampaign` and `updateCampaign`.","required":["label"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"campaignId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"marketing.campaign"},"label":{"type":"string","maxLength":20,"description":"A, B, C..."},"subjectOverride":{"type":"object","nullable":true,"description":"Subject line by locale.","additionalProperties":{"type":"string"}},"templateId":{"type":"string","format":"uuid","nullable":true,"description":"A different template for this variant; null uses the campaign's `content.templateId`."},"splitPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"Share of the test group; null splits evenly."},"source":{"type":"string","enum":["manual","aiDraft"],"default":"manual"},"aiDecisionRecordId":{"type":"string","nullable":true,"description":"The decision record of the `ai.proposeMarketingContent` draft it came from, for `aiDraft`."},"isWinner":{"type":"boolean","default":false,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005), the campaign's."}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ParkingFacility": {"type":"object","x-ticvai-persistence":"access.parking_facility","required":["name","venueId","mode"],"properties":{"id":{"type":"string","format":"uuid","description":"**Server-assigned, and the upsert key of `setParkingFacility`.** Absent in a body, it creates; present, it names the facility being replaced. A client never mints one.\n"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"mode":{"$ref":"#/components/schemas/ParkingIntegrationMode"},"capacity":{"type":"integer","nullable":true,"description":"**What \"full\" means in the first release** (decided 28 September, audit R166): the facility is full when the issued `ParkingEntitlement`s valid for a time reach this number. There is no live space count from the car park; a guest sees *full* only when capacity is reached, never an availability figure. Null means no limit is enforced.\n"},"takesPayment":{"type":"boolean","readOnly":true,"default":false,"description":"**Always false, and stated rather than assumed** (19.2.78, CF-124). The requirement asks the guest app to take parking payments; the client decided on 14 August that it does not.\nAll three integration models are entitlement-based — the ticket carries the parking right and the platform pushes a plate or a code. **Pay-per-hour parking unrelated to a ticket runs on the parking system's own POS**, because taking that money here would make the venue an acquirer for parking, with a settlement path and a tax treatment nobody has designed.\nThe field exists so that a future reversal is a value change with a visible blast radius, rather than a silent gap somebody rediscovers.\n"},"vendorSwapTargetDays":{"type":"integer","readOnly":true,"default":5,"description":"**A new parking vendor should take days, not weeks** — Qossai, 14 August. The team has integrated parking APIs before and the architecture is expected to make the next one cheap.\nRecorded as a design constraint rather than a runtime value: **everything vendor-specific lives in `vendorName`, `endpoint` and `credentialRef`**, and the three modes are the adaptor surface (ADR-0012). A vendor needing a fourth mode is the signal this has been violated.\n"},"vendorName":{"type":"string","nullable":true,"description":"Staff only — omitted from a guest's `listParkingFacilities` response."},"endpoint":{"type":"string","nullable":true,"description":"Staff only — omitted from a guest's `listParkingFacilities` response."},"credentialRef":{"type":"string","nullable":true,"description":"A vault reference, never the credential. Staff only — omitted from a guest's `listParkingFacilities` response."},"pushLeadMinutes":{"type":"integer","nullable":true,"description":"Staff only — omitted from a guest's `listParkingFacilities` response. How far ahead of the visit a plate is pushed. **Too early and the whitelist fills with cars that will not arrive; too late and the guest is at the barrier.**\n"},"accessPointIds":{"type":"array","description":"Where the platform validates its own code, in `none` and `qrHandoff` modes.","items":{"type":"string","format":"uuid"}},"isActive":{"type":"boolean"}}},
"ParkingIntegrationMode": {"type":"string","description":"CF-52, settled 14 August. **Not variations of one thing** — each decides what happens at sale and what a guest presents at the barrier.\n","enum":["none","plateWhitelist","qrHandoff"]},
"PerProductRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the profile row** (`access.admission_rules.per_product_rules`). The rules are read with the profile and a rule is never queried on its own, so a child table would add a join for nothing.\n","items":{"type":"object","properties":{"productId":{"type":"string","format":"uuid"},"entriesPerDay":{"type":"integer","nullable":true},"minimumGapMinutes":{"type":"integer","nullable":true,"description":"**Anti-passback in minutes rather than a boolean.** A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back over a fence.\n"},"allowedAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"biometricPolicy":{"allOf":[{"$ref":"#/components/schemas/BiometricPolicy"}],"description":"BL-105, 3.2.9. **The biometric check is a property of the product, not of the venue** — memberships checked, day tickets not. It sits here rather than on the profile because `perProductRules` is already where a ticket type states its own terms, and a profile per product would multiply profiles to carry one flag.\n**Absent means `disabled`**, and `disabled` is the answer for every product until somebody chooses otherwise. **Inert while `VenueSettings.biometrics.isEnabled` is false**, so a rules profile copied to another venue cannot begin capturing faces there.\n"},"maxPassesPerBiometricIdentity":{"type":"integer","nullable":true,"minimum":1,"description":"BL-096, 2.14.7. **The annual-pass quota, keyed to biometric identity.** `enrolFacePass` already answers 409 where a face is on another annual pass; the constant behind that refusal was one and was invisible. **Null means unlimited** and is the answer for every product that is not an annual pass — a quota applied where nobody asked for one turns a family sharing a day ticket into a fraud alert.\n"}}}},
"Performance": {"x-ticvai-persistence":"catalogue.performance","type":"object","required":["id","eventId","startsAt","endsAt","status"],"properties":{"id":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"description":"BL-048. **The approval chain and the occurrence lifecycle sat on different entities**, so neither was complete: `states/performance.yaml` models scheduled, onSale, soldOut, suspended, cancelled and completed properly, and nothing said which of those transitions somebody had to sign.\n**Set on the transition that needs it, not on the performance.** Publishing a performance is routine; cancelling one that has sold is the act somebody signs — and binding approval to the whole entity would have required a signature to reschedule a wet Tuesday.\n"},"requiresApprovalToCancel":{"type":"boolean","default":true,"description":"**Cancelling a sold performance is the one transition that needs a name against it.** `assessProductChange` already answers how many tickets are affected; this decides who has to look at that number before the button works.\n"},"status":{"type":"string","enum":["scheduled","onSale","soldOut","suspended","cancelled","completed"]},"admissionRulesId":{"type":"string","format":"uuid","nullable":true},"seatMapId":{"type":"string","format":"uuid","nullable":true},"language":{"type":"string","nullable":true,"maxLength":35,"pattern":"^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$","description":"The language the performance is given in, as a BCP 47 tag (`en`, `ar`, `fr`, `de`, `zh`, `ru`, `ar-AE`). **A guided tour at 10:00 in French and one at 10:00 in Arabic are two performances**, so a guest who picks a language sees only the tours in it (`listPerformances` `language`). Null when the performance is not language-specific (decided 29 September, rev 3 REV3-17).\n"},"format":{"type":"string","nullable":true,"maxLength":40,"description":"How it is presented, free text the venue chooses, e.g. `2D`, `3D`, `IMAX`, `subtitled`. A cinema screening shows language and format together. Null when it does not apply (decided 29 September, rev 3 REV3-17).\n"}}},
"PerformanceCancellationResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["performanceId","dryRun","affectedOrders","refundExposure"],"properties":{"performanceId":{"type":"string","format":"uuid"},"dryRun":{"type":"boolean"},"affectedOrders":{"type":"integer"},"affectedGuests":{"type":"integer"},"refundExposure":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the cancellation costs. Returned before committing, so the person cancelling sees the number at the moment they decide.\n"},"bulkRefundBatchId":{"type":"string","nullable":true,"description":"**Null on this response.** The refund batch is created by `orders` when it consumes `performance.cancelled` (F09), after this call has returned, and is queued there for approval — refunds are not issued automatically. Read it from orders, not from here.\n"},"notificationsQueued":{"type":"integer"}}},
"Point": {"type":"object","required":["x","y"],"properties":{"x":{"type":"number"},"y":{"type":"number"}}},
"Queue": {"x-ticvai-persistence":"queue.queue + queue.queue_operating_window","allOf":[{"$ref":"#/components/schemas/CreateQueueRequest"},{"type":"object","required":["id","status","waitingPartyCount"],"properties":{"id":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/QueueStatus"},"statusReason":{"type":"string","nullable":true},"waitingPartyCount":{"type":"integer"},"waitingGuestCount":{"type":"integer"},"currentWaitMinutes":{"type":"integer","nullable":true},"waitTimeSource":{"$ref":"#/components/schemas/WaitTimeSource"},"waitTimeAsOf":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When `currentWaitMinutes` was last set, by whichever source set it. `WaitTime.asOf` reads this.\n"},"manualWaitExpiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"Set by `setWaitTime` as now plus `expiresInMinutes`. Past it, the manual figure is dropped and the queue reverts to its sensor or throughput estimate. Null when the current figure is not manual.\n"},"manualWaitNote":{"type":"string","maxLength":200,"nullable":true,"readOnly":true,"description":"The `note` given with the current manual figure. Cleared when it expires."},"expectedReopenAt":{"type":"string","format":"date-time","nullable":true}}}]},
"QueueDetail": {"x-ticvai-persistence":"queue.queue","allOf":[{"$ref":"#/components/schemas/Queue"},{"type":"object","properties":{"nowServingPartyNumber":{"type":"integer","nullable":true},"lastCalledAt":{"type":"string","format":"date-time","nullable":true},"throughputLastHour":{"type":"integer"},"noShowRatePercent":{"type":"number"},"feed":{"$ref":"#/components/schemas/QueueFeedHealth"}}}]},
"QueueEntryStatus": {"type":"string","enum":["waiting","called","redeemed","expired","noShow","cancelled","released"]},
"QueueFastPass": {"x-ticvai-persistence":"queue.queue","type":"object","description":"**Which Fast Pass entitlements this lane accepts, and how** (decided 29 September, VM close-out; pack 'Access Control Module' p.109, BO-221 Fast Pass & Attraction Access Journey). Fast Pass stays an entitlement owned by Product & Entitlement; this block is the lane's side of it: which products it honours, the return window, a per-guest daily cap and the access points that redeem it. Stored on the queue row. Only meaningful where `kind` is `fastPass` or `fastPassAllocationPercent` is above 0.\n**Four ways into priority, not one** (decided 29 September, build pass; 5.6.7 and 5.6.34). A guest joins this lane as priority when they hold an entitlement from `entitlementProductIds` (VIP, annual pass, premium package), are a member of a tier in `loyaltyTierIds`, qualify for a live promotion in `promotionIds`, or declare an accessibility need where `accessibilityPriority` is on. The first criterion met is recorded on the entry as `WaitingGuest.priorityBasis`. Every criterion is resolved by the server at join time; nothing the request asserts about a tier or a promotion is trusted. All four draw on the same reserved `fastPassAllocationPercent`, so widening who qualifies never widens the share of the ride they take.\n","required":["entitlementProductIds"],"properties":{"entitlementProductIds":{"type":"array","description":"Catalogue products whose entitlement admits to this lane. May be empty where priority comes only from a tier, a promotion or an accessibility need.\n","items":{"type":"string","format":"uuid"}},"loyaltyTierIds":{"type":"array","description":"5.6.7 and 5.6.34 (decided 29 September, build pass). Loyalty programme tiers (`marketing.programme_tier`) whose members join this lane as priority. Read from the guest's own loyalty position at join time, never from the request, so a guest cannot claim a tier they do not hold. Empty: tier grants nothing on this lane.\n","items":{"type":"string","format":"uuid"}},"promotionIds":{"type":"array","description":"5.6.34 (decided 29 September, build pass). Promotions that grant queue privilege on this lane while they are live. A guest qualifies when the promotion's conditions hold for them at join (the evaluation `promotions` already makes for a price), or by presenting its code in `JoinQueueRequest.promotionCode`. A paused or expired promotion grants nothing.\n","items":{"type":"string","format":"uuid"}},"accessibilityPriority":{"type":"boolean","default":false,"description":"5.6.7 (decided 29 September, build pass). A party that declares an accessibility need (`JoinQueueRequest.accessibilityNeedDeclared`) joins as priority. **Taken on trust**, because asking for proof at a ride entrance is worse than the occasional abuse; the declaration is on the entry, so the operator at the front sees it (`listQueueEntries`). A venue that wants proof sells or issues an accessibility pass and lists it in `entitlementProductIds` instead. **Not the `accessible` lane**: that is where a guest who cannot stand in a switchback waits; this moves them ahead in the lane they chose.\n"},"returnWindowMinutes":{"type":"integer","minimum":1,"maximum":240,"default":60,"description":"How long after the booked return time a Fast Pass holder may still enter. Proposed, our build plan.\n"},"maxPerGuestPerDay":{"type":"integer","minimum":1,"nullable":true,"description":"Fast Pass redemptions one guest may make on this lane per day; null is no cap."},"allowedAccessPointIds":{"type":"array","description":"Access points that redeem Fast Pass for this lane; empty is the queue's own.","items":{"type":"string","format":"uuid"}}}},
"QueueFeed": {"x-ticvai-persistence":"queue.feed","type":"object","required":["id","queueId","adaptor","isEnabled"],"properties":{"id":{"type":"string","format":"uuid"},"queueId":{"type":"string","format":"uuid"},"adaptor":{"$ref":"#/components/schemas/QueueFeedAdaptor"},"adaptorName":{"type":"string","nullable":true,"description":"Named vendor where `adaptor` is `vendorAdaptor`."},"credentialsRef":{"type":"string","nullable":true,"description":"Key vault reference. Credentials are never returned."},"expectedIntervalSeconds":{"type":"integer","default":60,"description":"Beyond this without a reading, the feed is considered quiet."},"isEnabled":{"type":"boolean"},"health":{"allOf":[{"$ref":"#/components/schemas/QueueFeedHealth"}],"readOnly":true,"x-ticvai-persisted":false,"description":"Whether the feed is currently reporting, computed on read — what `listQueueFeeds` promises per row. Ignored on input to `configureQueueFeed`.\n"}}},
"QueueFeedAdaptor": {"type":"string","description":"Vendor adaptors are bespoke work (ADR-0012). `generic` is the inbound API any system can post to; `mock` lets the feature be built and demonstrated with no vendor at all.\n**`manual` is not an adaptor.** A queue with no enabled feed runs on figures an operator sets through `setWaitTime`, and its `WaitTimeSource` reads `manual` — that is the whole of the manual path, and there is no feed row for it. Transports a screen might list (sensor API, webhook, MQTT, turnstile count, camera) all post to the one inbound API, which is `generic`; anything that needs code of its own to fetch or translate is `vendorAdaptor`.\n","enum":["generic","mock","vendorAdaptor"]},
"QueueFeedHealth": {"x-ticvai-persistence":"none — computed","type":"object","required":["feedId","isHealthy","isQuiet"],"properties":{"feedId":{"type":"string","format":"uuid"},"adaptor":{"$ref":"#/components/schemas/QueueFeedAdaptor"},"isHealthy":{"type":"boolean","description":"**Healthy means the last reading arrived within the feed's expected interval** (decided 28 September, audit R106 (1)): `lastReadingAt` is no older than `expectedIntervalSeconds`. It is the opposite of `isQuiet`, and nothing else (latency, discards) makes a reporting feed unhealthy.\n"},"isQuiet":{"type":"boolean","description":"No reading within the expected interval. The wait time falls back to throughput-derived and is marked stale rather than freezing at the last value.\n"},"lastReadingAt":{"type":"string","format":"date-time","nullable":true},"expectedIntervalSeconds":{"type":"integer","description":"The feed's `expectedIntervalSeconds` — the interval `isQuiet` is judged against, returned here so a health panel does not need the feed row as well.\n"},"readingsLastHour":{"type":"integer"},"discardedLastHour":{"type":"integer","description":"Out-of-order readings rejected in the last hour — rows of `queue.reading` for this feed with `disposition: discardedOutOfOrder`. Duplicates are not counted here: a duplicate has no row, and `submitQueueReading` reports it in its own `duplicates`.\n"}}},
"QueueReading": {"x-ticvai-persistence":"queue.reading","type":"object","required":["id","kind","value","observedAt"],"properties":{"id":{"type":"string","format":"uuid"},"feedId":{"type":"string","format":"uuid","readOnly":true,"description":"The feed that sent it, taken from the `submitQueueReading` body. Per-feed health counts by this, not by queue.\n"},"disposition":{"type":"string","readOnly":true,"enum":["applied","discardedOutOfOrder"],"description":"Set on receipt. A `discardedOutOfOrder` reading is kept so feed health can count it and never moves an estimate.\n"},"kind":{"type":"string","description":"Deliberately narrow. Anything richer would couple the platform to one vendor's model of a queue.\n","enum":["peopleCount","dwellSeconds","throughputPerHour","queueLengthMetres"]},"value":{"type":"number","minimum":0},"confidence":{"type":"number","minimum":0,"maximum":1},"observedAt":{"type":"string","format":"date-time"}}},
"QueueStatus": {"type":"string","enum":["open","paused","closed","atCapacity"]},
"QueueStatusResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["queue","affectedEntries"],"properties":{"queue":{"$ref":"#/components/schemas/Queue"},"affectedEntries":{"type":"object","description":"What happened to guests already waiting. Closing releases and notifies them — a guest holding a position for a ride that will not run should be told.\n","properties":{"released":{"type":"integer"},"held":{"type":"integer"},"notified":{"type":"integer"}}}}},
"Refund": {"x-ticvai-persistence":"orders.refund","type":"object","required":["id","orderId","amount","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"batchId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"**The rate on the original payment, not today's** (BL-087, CF-118).\n`Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the moment of sale, so the sale rate is always retrievable. **Refunding at today's rate repays a different amount of money than was taken** — a guest who paid 100 USD at 3.67 and is refunded at 3.72 gets back more AED than they gave, and the venue carries the difference on every refund.\nThe exposure runs both ways and neither direction is defensible: a guest short-changed by a moving rate has a complaint the venue cannot answer, because **the guest did nothing but wait.**\n"},"taxReversalEntryId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**A refund reverses the tax entry it created, and this is where that is stated rather than implied.** `reverseJournalEntry` and `calculateTax` both exist, so both halves were present and the obligation was assumed — **an implied obligation is one a developer can miss without failing anything.**\nNull only where the original sale carried no tax.\n"},"settleTo":{"type":"string","enum":["originalTender","advanceBalance","wireTransfer","storeCredit"],"default":"originalTender","description":"BL-086. **A refund could only go back the way it came.** A guest whose card has expired, a partner settling by wire, a guest who would rather have the credit — three real cases with one answer.\n**`originalTender` stays the default** because refunding elsewhere is how money laundering works, and anything else needs a reason.\n"},"fxVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Where the sale rate and the current rate differ, **the difference is booked as an FX variance rather than hidden in the refund**. `runFxRevaluation` already handles this class of movement and this is the same act at a smaller scale.\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPercentage":{"type":"number","description":"From the venue's time bands, or an approver override."},"status":{"type":"string","enum":["pendingApproval","pendingGateway","completed","declined","failed"]},"reason":{"type":"string"},"requestedByPrincipalId":{"type":"string","format":"uuid"},"secondaryPrincipalId":{"type":"string","format":"uuid","nullable":true},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"ledgerEntryId":{"type":"string","format":"uuid","nullable":true,"description":"Written before the gateway is called."},"gatewayReference":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"ResolutionCode": {"type":"string","enum":["repaired","partReplaced","adjusted","cleaned","noFaultFound","referredExternal","replaced","deferred"]},
"ScanAnomalyRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.scan_anomaly_rules`). Read with the access point at validation, and a rule is never queried on its own.\n","items":{"type":"object","properties":{"rule":{"type":"string","enum":["simultaneousEntry","impossibleTravelTime","rapidReentry","sharedDevice","velocityBreach"]},"action":{"type":"string","enum":["log","flag","requireSupervisor","deny"]},"thresholdSeconds":{"type":"integer","nullable":true}}}},
"SeatAvailability": {"x-ticvai-persistence":"none — computed from seat, hold and block","type":"object","required":["performanceId","seatMapId","renderMode","totals","seats"],"properties":{"performanceId":{"type":"string","format":"uuid"},"seatMapId":{"type":"string","format":"uuid"},"renderMode":{"type":"string","enum":["graphical","list"],"description":"The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat map's `noGeometry` state), so the client sells from categories and best-available groups and does not draw a plan. `graphical` means every seat carries `position`.\n"},"totals":{"type":"object","properties":{"total":{"type":"integer"},"available":{"type":"integer"},"held":{"type":"integer"},"sold":{"type":"integer"},"blocked":{"type":"integer"},"buffered":{"type":"integer"}}},"byCategory":{"type":"array","items":{"type":"object","properties":{"categoryId":{"type":"string","format":"uuid"},"available":{"type":"integer"},"sold":{"type":"integer"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"sections":{"type":"array","description":"The map's sections with what a guest screen needs to show the view from each (decided 29 September, rev 3 23SEP-14): the photo where the venue supplied one, otherwise null and the client renders the view from `boundary` and the seat positions. In this response so WEB-007 and GST-049 need no second call.\n","items":{"type":"object","required":["code","name"],"properties":{"code":{"type":"string"},"name":{"type":"string"},"viewAssetId":{"type":"string","format":"uuid","nullable":true,"description":"As `Section.viewAssetId`. Null means render the view from geometry."},"boundary":{"type":"array","nullable":true,"items":{"$ref":"#/components/schemas/Point"},"description":"As `Section.boundary`. Null when `renderMode` is `list`."}}}},"seats":{"type":"array","items":{"type":"object","required":["seatId","status"],"properties":{"seatId":{"type":"string"},"status":{"$ref":"#/components/schemas/SeatStatus"},"categoryId":{"type":"string","format":"uuid","nullable":true},"displayLabel":{"type":"string","description":"What the guest sees, e.g. `A2-7-11`, as on `Seat`."},"position":{"allOf":[{"$ref":"#/components/schemas/Point"}],"nullable":true,"description":"The seat's coordinates on the map, as on `Seat`. Present when `renderMode` is `graphical`; null when it is `list`."}}}}}},
"SeatRecommendation": {"x-ticvai-persistence":"none — computed","type":"object","required":["seatIds","totalPrice","isContiguous","rank"],"properties":{"seatIds":{"type":"array","items":{"type":"string"}},"displayLabels":{"type":"array","items":{"type":"string"}},"totalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"categoryId":{"type":"string","format":"uuid"},"isContiguous":{"type":"boolean"},"rank":{"type":"integer","description":"Best first."},"rationale":{"type":"string","description":"Why this option was chosen — closest to stage, best value in category, only contiguous block remaining. Shown to a call-centre agent, not the guest.\n"}}},
"SeatRecommendationRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["partySize","strategy"],"properties":{"partySize":{"type":"integer","minimum":1,"maximum":50},"strategy":{"$ref":"#/components/schemas/SeatRecommendationStrategy"},"categoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"maxPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"accessibleCount":{"type":"integer","default":0,"description":"Wheelchair spaces in the party. Companions are added automatically."},"maxOptions":{"type":"integer","default":3,"maximum":10}}},
"SeatRecommendationStrategy": {"type":"string","enum":["bestAvailable","bestValue","closestToStage","accessible","contiguous"]},
"SeatStatus": {"type":"string","enum":["available","held","sold","blocked","buffered","unavailable"]},
"SetAssetStatusRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["status","reason","recordedAt"],"properties":{"status":{"$ref":"#/components/schemas/AssetStatus"},"reason":{"type":"string","minLength":3,"maxLength":1000},"inspectionId":{"type":"string","format":"uuid","nullable":true,"description":"Required for return to service where the asset demands it."},"raiseWorkOrder":{"type":"boolean","default":false},"recordedAt":{"type":"string","format":"date-time"}}},
"Suggestion": {"type":"object","x-ticvai-persistence":"ai.suggestion","description":"One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n","required":["id","kind","basis","maturity","producedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SuggestionKind"},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"scopePath":{"type":"string"},"subjectRef":{"type":"string","nullable":true,"description":"What it is about — a product, an outlet, an item, a party."},"value":{"type":"object","additionalProperties":true,"description":"The suggestion itself. Shape depends on `kind`."},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1,"description":"**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"},"explanation":{"type":"string","description":"**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"},"inputs":{"type":"object","additionalProperties":true,"description":"What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"},"producerRef":{"type":"string","description":"The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"SuggestionKind": {"type":"string","description":"What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n","enum":["price","replenishment","requisition","demandForecast","prepPlan","menuEngineering","staffing","slaTarget","waitTime","upsell","segmentation","anomaly","scenario","sendTime","wasteRisk","queueBalancing","itinerary"]},
"SupervisorStepUp": {"type":"object","description":"**A supervisor signs the act in place, on the device making the call** (decided 28 September, audit R144). Used where the decision is a same-device step-up rather than an approval request: reopening a shift, recounting a stock count, a retail return above the venue threshold, and (proposed by the coordinator, client to confirm) closing a stock transfer short and cancelling a performance.\n\n**The verification rule, the same on every operation that takes it:** the server checks `credential` against `principalId`; that principal must hold the operation's `x-ticvai-permission` at the operation's scope, must be active at that venue, and must not be the person whose act is being reversed where the operation says so. Any failure is a `403` (`supervisor-step-up-refused`) and nothing is written. **No approval request is raised**, and the operation declares `x-ticvai-step-up: pin`.\n","required":["principalId","credential"],"properties":{"principalId":{"type":"string","format":"uuid","description":"The supervisor signing. Recorded against the act."},"credential":{"type":"string","maxLength":512,"writeOnly":true,"description":"The supervisor's staff PIN, as they sign in at a till with it. **A PIN, never a password** (audit R123 (7)). Never stored or returned."}}},
"TurnstileMode": {"type":"string","description":"**Reduced to two values — decided 28 September, audit R221.** Entry, exit, re-entry and crossover were the access point's `Direction` under another name, and two fields that could disagree left the gate to guess. Direction is fixed per access point; within `normal` or `podium` operation the turnstile may only be let spin free or held closed.\n","enum":["freeRotation","closed"]},
"WaitTime": {"x-ticvai-persistence":"none — computed from readings and throughput","type":"object","required":["queueId","waitMinutes","source","asOf","isStale"],"properties":{"queueId":{"type":"string","format":"uuid"},"queueName":{"$ref":"#/components/schemas/LocalisedText"},"attractionProductId":{"type":"string","format":"uuid","nullable":true},"attractionCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. Read from catalogue, not stored here.\n"},"status":{"$ref":"#/components/schemas/QueueStatus"},"waitMinutes":{"type":"integer","nullable":true,"description":"Null where the queue is closed or no estimate is available."},"source":{"$ref":"#/components/schemas/WaitTimeSource"},"isStale":{"type":"boolean","description":"The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as current, and it is not hidden (decided 28 September, audit R080 (b)): the screen shows `waitMinutes` with its `asOf` and a stale marker.\n"},"heightRequirementCm":{"type":"integer","nullable":true},"zone":{"type":"string","nullable":true},"asOf":{"type":"string","format":"date-time","description":"When the figure was produced — the queue's `waitTimeAsOf`."}}},
"WaitTimeSource": {"type":"string","description":"Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed.\n","enum":["sensor","throughput","manual","unavailable"]},
"WaitingGuest": {"x-ticvai-persistence":"queue.entry","type":"object","required":["id","queueId","partyNumber","partySize","status","joinedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client-generated UUIDv7 from `JoinQueueRequest.id`, and the `entryId` every entry path takes. `listMyWaitingGuests` gives it back to a guest who has lost it.\n"},"queueId":{"type":"string","format":"uuid"},"queueName":{"$ref":"#/components/schemas/LocalisedText"},"subjectId":{"type":"string","format":"uuid","nullable":true},"partyNumber":{"type":"integer","description":"What the guest sees and what appears on signage."},"partySize":{"type":"integer"},"status":{"$ref":"#/components/schemas/QueueEntryStatus"},"positionInQueue":{"type":"integer","nullable":true},"partiesAhead":{"type":"integer","nullable":true},"estimatedCallAt":{"type":"string","format":"date-time","nullable":true},"isFastPass":{"type":"boolean"},"priorityBasis":{"type":"string","enum":["none","entitlement","loyaltyTier","promotion","accessibility"],"default":"none","description":"Why this party is priority, when it is (decided 29 September, build pass; 5.6.7, 5.6.34): the first `QueueFastPass` criterion met at join, in the order entitlement, loyalty tier, promotion, accessibility. `isFastPass` is true whenever this is not `none`. Kept on the entry so a disputed priority can be explained afterwards.\n"},"priorityTierId":{"type":"string","format":"uuid","nullable":true,"description":"The loyalty tier that granted priority, where `priorityBasis` is `loyaltyTier`."},"priorityPromotionId":{"type":"string","format":"uuid","nullable":true,"description":"The promotion that granted priority, where `priorityBasis` is `promotion`."},"accessibilityNeedDeclared":{"type":"boolean","default":false,"description":"What the party declared at join, shown to the operator at the front."},"entitlementId":{"type":"string","nullable":true},"calledAt":{"type":"string","format":"date-time","nullable":true},"returnWindowEndsAt":{"type":"string","format":"date-time","nullable":true},"redeemedAt":{"type":"string","format":"date-time","nullable":true},"admittedCount":{"type":"integer","nullable":true},"joinedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkOrder": {"x-ticvai-persistence":"maintenance.work_order","x-ticvai-retired-columns":["is_overdue"],"type":"object","required":["id","workOrderNumber","title","venueId","status","priority","kind","createdAt"],"properties":{"downtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"},"rootCause":{"type":"string","nullable":true,"enum":["wearAndTear","operatorError","guestDamage","manufacturingDefect","environmental","softwareFault","powerFailure","deferredMaintenance","unknown"],"description":"**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"},"rootCauseNote":{"type":"string","nullable":true},"escalatedAt":{"type":"string","format":"date-time","nullable":true},"escalationLevel":{"type":"integer","default":0,"description":"**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"},"id":{"type":"string","format":"uuid"},"workOrderNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"title":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"assetName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"},"status":{"$ref":"#/components/schemas/WorkOrderStatus"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"priorityScore":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"readOnly":true,"description":"The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01)."},"prioritySource":{"type":"string","enum":["scored","assetOverride","manual"],"readOnly":true,"description":"Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`."},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","items":{"type":"string"},"description":"Skills the job needs (M17-13)."},"kind":{"$ref":"#/components/schemas/WorkOrderKind"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"raisedByPrincipalId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"},"locationDescription":{"type":"string","maxLength":500,"nullable":true,"description":"Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"},"elapsedMinutes":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"},"isTimerRunning":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"},"dueAt":{"type":"string","format":"date-time","nullable":true},"isOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"},"requiresVerification":{"type":"boolean"},"sourcePlanId":{"type":"string","format":"uuid","nullable":true},"sourceInspectionId":{"type":"string","format":"uuid","nullable":true},"sourceIncidentId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkOrderAttachment": {"type":"object","x-ticvai-persistence":"maintenance.work_order_attachment","required":["id","workOrderId","kind","capturedAt"],"properties":{"id":{"type":"string","format":"uuid"},"workOrderId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["photo","video","document","note","signature"]},"assetRef":{"type":"string","format":"uuid","nullable":true},"text":{"type":"string","nullable":true},"stage":{"type":"string","enum":["before","during","after","signOff"],"nullable":true},"capturedByPrincipalId":{"type":"string","format":"uuid"},"capturedAt":{"type":"string","format":"date-time","description":"Device time. **Distinct from when it synced** — a photo taken at 09:14 in a basement and uploaded at 11:40 is evidence of the first, not the second.\n"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkOrderDetail": {"x-ticvai-persistence":"maintenance.work_order","allOf":[{"$ref":"#/components/schemas/WorkOrder"},{"type":"object","properties":{"description":{"type":"string","nullable":true},"resolution":{"type":"string","nullable":true},"resolutionCode":{"$ref":"#/components/schemas/ResolutionCode"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"timeEntries":{"type":"array","items":{"type":"object","properties":{"action":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"pauseReason":{"type":"string","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}}},"parts":{"type":"array","items":{"type":"object","properties":{"inventoryItemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"quantity":{"type":"number"},"reservedQuantity":{"type":"number","description":"Still reserved for this work order and not yet issued (M17-02)."},"cost":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"labourCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"partsCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","x-ticvai-column":"net_cost_amount"},"completedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who called `completeWorkOrder`. **What `verifyWorkOrder` compares against** — the verifier may not be the technician who completed the work, and the assignee is not necessarily that person.\n"},"followUpRequired":{"type":"boolean","default":false},"followUpNote":{"type":"string","maxLength":1000,"nullable":true},"verificationOutcome":{"type":"string","enum":["verified","rejected"],"nullable":true,"description":"The latest `verifyWorkOrder` outcome."},"verificationNote":{"type":"string","maxLength":1000,"nullable":true},"verifiedAt":{"type":"string","format":"date-time","nullable":true},"verifiedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"cancelReason":{"type":"string","enum":["raisedInError","duplicate","superseded","noLongerRequired"],"nullable":true},"cancelNote":{"type":"string","maxLength":300,"nullable":true},"supersededByWorkOrderId":{"type":"string","format":"uuid","nullable":true,"description":"Set by `cancelWorkOrder` where the reason is `superseded`."},"cancelledAt":{"type":"string","format":"date-time","nullable":true},"closeOutcome":{"type":"string","enum":["completedAndVerified","notReproducible","supersededByReplacement","noLongerApplicable","duplicate"],"nullable":true},"closeNote":{"type":"string","maxLength":500,"nullable":true},"duplicateOfWorkOrderId":{"type":"string","format":"uuid","nullable":true,"description":"Set by `closeWorkOrder` where the outcome is `duplicate`."},"closedAt":{"type":"string","format":"date-time","nullable":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true}}}]},
"WorkOrderFaultAssessment": {"x-ticvai-persistence":"none — columns on maintenance.work_order","type":"object","description":"What the person raising a fault says about it, which the priority score reads (M17-01).","properties":{"safetyRisk":{"type":"boolean","default":false},"guestImpact":{"type":"string","enum":["none","degraded","closed"],"default":"none"}}},
"WorkOrderKind": {"type":"string","enum":["corrective","planned","inspectionFollowUp","incidentCorrective","improvement"]},
"WorkOrderPriority": {"type":"string","enum":["low","normal","high","urgent","emergency"]},
"WorkOrderStatus": {"type":"string","enum":["open","assigned","inProgress","paused","awaitingParts","completed","verified","closed","cancelled"]}
}
```
