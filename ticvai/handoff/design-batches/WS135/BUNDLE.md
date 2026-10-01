# WS135 — Marketing CRM Configuration Reference v1.0 board 1

**10 screens · 21 operations · 28 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `CASE_VIEW, GUEST_MANAGE, GUEST_VIEW, GUEST_VIEW_PII, LEDGER_POST, MARKETING_MANAGE, MARKETING_VIEW, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `BO-734` | CRM Command Center | B–D | 1 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `BO-735` | Guest Directory | B–D | 13 | 21 | 6 | 16 | 1 | 0 | — | notStarted (—) |
| `BO-736` | Guest Master Configuration | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-737` | Customer 360 Profile | B–D | 0 | 0 | 6 | 0 | 3 | 0 | — | notStarted (—) |
| `BO-738` | Activity Timeline | B–D | 0 | 0 | 6 | 12 | 0 | 0 | — | notStarted (—) |
| `BO-739` | Contact & Preferences | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-740` | Family & Guardians | B–D | 0 | 0 | 6 | 3 | 1 | 0 | — | notStarted (—) |
| `BO-741` | Corporate & Groups | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-742` | Commerce & Documents | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-743` | AI Guest Intelligence | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-734, BO-736, BO-737, BO-738, BO-740, BO-741, BO-742, BO-743 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-734` CRM Command Center

**Give authorized users an operational and analytical overview of the customer base. Display total, new, active, inactive, registered and guest-checkout customers with tenant, brand, venue, region and date filters. Show VIP, high-value, family, corporate, group, churn-risk, duplicate and incomplete-profile indicators. Present LTV, engagement, growth, consent health and source-synchronization trends with drill- down to the underlying guests. Surface explainable AI insights and prioritized actions without bypassing consent, eligibility or access policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_VIEW`, `MARKETING_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/crm-command-center-bo-734` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Search | text field | — | Requires `GUEST_VIEW_PII`: matching on personal data discloses it, so a caller without that permission who passes `search` is refused with 403 rather than having the parameter ignored. | `searchGuests` ?search |
| Segment | picker: choose a segment | — | — | `searchGuests` ?segmentId |
| Has consent for | select | — | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | `searchGuests` ?hasConsentFor |
| Search | text field | — | max length 200 | `listSegments` ?search |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `searchGuests` (onLoad, Find a guest); `listSegments` (onLoad, Segment indicators)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-735` Guest Directory: *Guest Directory*; carries `subjectId`
- → `BO-736` Guest Master Configuration: *Guest Master Configuration*
- → `BO-737` Customer 360 Profile: *Customer 360 Profile*
- → `BO-738` Activity Timeline: *Activity Timeline*; carries `subjectId`
- → `BO-739` Contact & Preferences: *Contact & Preferences*
- → `BO-740` Family & Guardians: *Family & Guardians*; carries `subjectId`
- → `BO-741` Corporate & Groups: *Corporate & Groups*
- → `BO-742` Commerce & Documents: *Commerce & Documents*
- → `BO-743` AI Guest Intelligence: *AI Guest Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The crm list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the crm untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No crm yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the crm are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `searchGuests` → `GUEST_VIEW` (read) · staff
- `listSegments` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.14.25 | Segmentation & Attribution Audit Trail | Marketing & CRM | CONTRACTED | `listSegments` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- CRM guest dashboard shows active/inactive/duplicate profile counts and lifetime value, plus guest directory/search and segmentation by source (individual, corporate, group, travel agent, OTA). *(client request · MoM 20 Aug 2026, 4.1 CRM — Customer Profiles, Unique Fields & Family/Guardian Linking · DI-370)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-734` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-734`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 1: Opens CRM Command Center → Give authorized users an operational and analytical overview of the customer base. Display total, new, active, inactive, registered and guest-checkout customers with tenant, brand, venue, region and …
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F244 branch at step 1 (expected): when Nothing has been set up on CRM Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F244 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-734?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-735`, `BO-736`, `BO-737`, `BO-738`, `BO-739`, `BO-740`, `BO-741`, `BO-742`, `BO-743`.
- [ ] Every gated control is gated: `GUEST_VIEW`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-735` Guest Directory

**Provide a permission-controlled directory for locating and managing every guest record. Search by name, email, mobile, guest ID, external ID, ticket, booking, membership or loyalty identifier. Filter by profile status, segment, language, geography, membership, loyalty tier, wallet, LTV, engagement and churn risk. Support saved views, configurable columns, sorting, pagination, controlled export and auditable bulk actions. Open Customer 360 directly from a result while masking restricted personal or financial data by policy. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW`, `LEDGER_POST` (1 configure, 1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `subjectId` (navigation) |
| Route | `/engagement-support/guest-directory-bo-735` |

**What the spec says about it.** **Guest record operations moved here from BO-036 Device Registry on 28 September (audit R254)** — `updateGuestProfile`, `mergeGuestProfiles`, `getGuestLoyalty`, `adjustLoyaltyPoints` and `getConsentHistory`, with their panels and forms. They had been attached to the device registry by module resemblance; managing a guest record is this screen's purpose.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Search | text field | — | Requires `GUEST_VIEW_PII`: matching on personal data discloses it, so a caller without that permission who passes `search` is refused with 403 rather than having the parameter ignored. | `searchGuests` ?search |
| Segment | picker: choose a segment | — | — | `searchGuests` ?segmentId |
| Has consent for | select | — | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | `searchGuests` ?hasConsentFor |

**Form: Adjust loyalty points** (modal, opened by *Adjust loyalty points*; *Adjust loyalty points* calls `adjustLoyaltyPoints`, *Cancel* sends nothing)

**Collects what `adjustLoyaltyPoints` sends before it is called.** Required: `programmeId`, `points`, `reason`. Optional: `reversedLoyaltyPointsId`, `notes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Programme `programmeId` | picker: choose a programme | required | — | — | shows names, sends the id | — | `adjustLoyaltyPoints` body |
| Points `points` | number field | required | — | — | — | Signed. Negative removes points, and the balance may not go below zero. | `adjustLoyaltyPoints` body |
| Reason `reason` | segmented control | required | — | Goodwill · Correction · Expiry reversal | — | Goodwill, correction or expiry reversal, and nothing else (decided 28 September, audit R149). | `adjustLoyaltyPoints` body |
| Reversed loyalty points `reversedLoyaltyPointsId` | picker: choose a reversed loyalty points | optional | — | — | shows names, sends the id | The entry this reverses, when it is a reversal. Set it and the sign is checked against the original — a reversal that does not cancel what it names is a second grant wearing a … | `adjustLoyaltyPoints` body |
| Notes `notes` | text area | optional | — | max length 1000 | — | — | `adjustLoyaltyPoints` body |

Errors to draw in the form: 409 The entry being reversed is already reversed (`alreadyReversed`), or the balance would go negative (`balanceWouldGoNegative`) (LoyaltyRefusedProblem)

**Form: Save guest profile** (modal, opened by *Save guest profile*; *Save guest profile* calls `updateGuestProfile`, *Cancel* sends nothing)

**Collects what `updateGuestProfile` sends before it is called.** Nothing in the body is required. Optional: `displayName`, `preferredLanguage`, `preferredChannel`, `tags`, `notes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Display name `displayName` | text field | optional | — | max length 200 | — | — | `updateGuestProfile` body |
| Preferred language `preferredLanguage` | language picker | optional | — | — | ISO 639-1 code, shown as the language name | — | `updateGuestProfile` body |
| Preferred channel `preferredChannel` | select | optional | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `updateGuestProfile` body |
| Tags `tags` | list of values (chips) | optional | — | — | — | — | `updateGuestProfile` body |
| Notes `notes` | text area | optional | — | max length 2000 | — | — | `updateGuestProfile` body |

**Sent by *Merge guest profiles*** (`mergeGuestProfiles`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Duplicate subject `duplicateSubjectId` | picker: choose a duplicate subject | required | — | — | shows names, sends the id | — | `mergeGuestProfiles` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `mergeGuestProfiles` body |

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**The loyalty position** (detail panel, from `getGuestLoyalty`)

| Shows | Format | Notes |
|---|---|---|
| Leaderboard nickname | text | BL-173. The name shown on a leaderboard, chosen by the guest. |
| Subject | the name it points at, never the id | — |
| Programme | the name it points at, never the id | — |
| Points balance | 1,234 | — |
| Lifetime points | 1,234 | — |
| Tier | the name it points at, never the id | The tier this row's `tierCode` and `tierName` are a copy of. Added 20 September with `marketing.programme_tier`: the two strings were a … |
| Tier code | text | — |
| Tier name | text | — |
| Points to next tier | 1,234 | — |
| Next expiry points | 1,234 | — |
| Next expiry at | 1 Oct 2026, 14:30 | — |

**The consent** (detail panel, from `getConsentHistory`)

| Shows | Format | Notes |
|---|---|---|
| Purpose | chip: Marketing, Personalisation, Profiling, Third party sharing, AI processing … | — |
| Decision | chip: Granted, Withdrawn, Not asked | — |
| Channels | list or chips (count when long) | Omit to apply to every channel the purpose covers. |
| Notice version | text | — |
| Source | chip: Guest app, Website, Kiosk, POS, Call centre, Import… | `checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` … |
| Recorded at | 1 Oct 2026, 14:30 | — |
| ID | text | — |
| Subject | the name it points at, never the id | — |
| Recorded by principal | the name it points at, never the id | — |
| Superseded at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Adjust loyalty points (secondary button) | `adjustLoyaltyPoints` POST `/guests/{subjectId}/loyalty/adjust` | AdjustLoyaltyPointsRequest | LoyaltyAdjustmentResult | 409 The entry being reversed is already reversed (`alreadyReversed`), or the balance would go negative (`balanceWouldGoNegative`) (LoyaltyRefusedProblem) | opens modal first |
| Merge guest profiles (destructive button) | `mergeGuestProfiles` POST `/guests/{subjectId}/merge` | inline | MergeResult | 409 Either profile is already merged (`alreadyMerged`), or they are the same profile (`sameProfile`) (MergeRefusedProblem) | — |
| Save guest profile (secondary button) | `updateGuestProfile` PATCH `/guests/{subjectId}` | inline | GuestProfileDetail | — | opens modal first |

**Data it reads**: `searchGuests` (onLoad, The directory)

**Where the user goes next**

- → `BO-734` CRM Command Center: *Back to CRM Command Center*

**What opens over it**

- confirmDialog *Merge guest profiles*: **Names what `mergeGuestProfiles` changes and what it leaves alone**, in the consequence rather than the verb. A guest profile this affects should be identified in the dialog, not just counted. **Collects what `mergeGuestProfiles` sends before it is called.** Required: `duplicateSubjectId` …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the guest are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Either profile is already merged (`alreadyMerged`), or they are the same profile (`sameProfile`) (MergeRefusedProblem); 409 The entry being reversed is already reversed (`alreadyReversed`), or the balance would go negative (`balanceWouldGoNegative`) (LoyaltyRefusedProblem) |

#### Permissions

- `searchGuests` → `GUEST_VIEW` (read) · staff
- `getGuestProfile` → `GUEST_VIEW` (read) · staff, guest
- `adjustLoyaltyPoints` → `LEDGER_POST` (operate) · staff
- `getConsentHistory` → `GUEST_VIEW` (read) · staff
- `getGuestLoyalty` → `GUEST_VIEW` (read) · staff, service
- `mergeGuestProfiles` → `GUEST_MANAGE` (configure) · staff
- `updateGuestProfile` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.8 | APIs shall support guest profile creation, updates, segmentation, communication preferences and activity history retrieval. | Developer & API Management | CONTRACTED | `getGuestProfile` |
| 22.2.27 | CRM APIs | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 22.2.28 | CRM Audit Trail | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 1.1.58 | Earned benefit entitlement management | Ticketing Catalogue | CONTRACTED | `adjustLoyaltyPoints` |
| 22.13.5 | Consent Version Management | Marketing & CRM | CONTRACTED | `getConsentHistory` |
| 22.13.6 | Consent Audit Trail | Marketing & CRM | CONTRACTED | `getConsentHistory` |
| 5.3.4 | The system should allow specification of a field (e.g. email) or a combination of fields (e.g. name + date of birth) to serve as the unique identifier for each guest. The system should restrict … | F&B & Guest Management | CONTRACTED | `mergeGuestProfiles` |
| 5.3.22 | Identify duplicate guest profiles and allow administrative merge while preserving purchases, memberships, wallets, loyalty balances, reservations, and history. | F&B & Guest Management | CONTRACTED | `mergeGuestProfiles` |
| 7.3.7 | Identify duplicate customer profiles using email, mobile, passport, national ID or configurable matching rules. Allow authorized users to merge profiles into a master record while preserving purchase … | F&B POS | CONTRACTED | `mergeGuestProfiles` |
| 22.2.8 | Guest Identity Resolution | Marketing & CRM | CONTRACTED | `mergeGuestProfiles` |
| 22.2.9 | Guest Profile Merge | Marketing & CRM | CONTRACTED | `mergeGuestProfiles` |
| 2.8.4 | The system should allow call center agents to add and modify guest profile data | Ticketing Sales | CONTRACTED | `updateGuestProfile` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- CRM guest dashboard shows active/inactive/duplicate profile counts and lifetime value, plus guest directory/search and segmentation by source (individual, corporate, group, travel agent, OTA). *(client request · MoM 20 Aug 2026, 4.1 CRM — Customer Profiles, Unique Fields & Family/Guardian Linking · DI-370)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-735` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-735`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 2: Works in Guest Directory → Provide a permission-controlled directory for locating and managing every guest record. Search by name, email, mobile, guest ID, external ID, ticket, booking, membership or loyalty identifier. Filter …

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (21 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-735?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Adjust loyalty points, Merge guest profiles, Save guest profile.
- [ ] Every transition is wired: `BO-734`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`, `LEDGER_POST`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-736` Guest Master Configuration

**Configure the shared guest data model without software changes. Configuration Scope of Work / Version 1.0 6 Maintain standard and custom attributes, field groups, labels, data types, defaults, required flags and validation rules. Define primary and external identifiers, source-system priority, survivorship rules and profile- completeness scoring. Configure field visibility and editability by role, tenant, brand, venue, region and jurisdiction. Version and audit schema changes and expose approved attributes consistently through UI, API and events. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW`, `MARKETING_MANAGE` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/guest-master-configuration-bo-736` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save guest attribute model (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getGuestAttributeModel` (onLoad, The shared data model)

**Where the user goes next**

- → `BO-734` CRM Command Center: *Back to CRM Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest master list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest master untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest master yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the guest master are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getGuestAttributeModel` → `GUEST_VIEW` (read) · staff
- `setGuestAttributeModel` → `GUEST_MANAGE` (configure) · staff
- `setGuestExtraFields` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: at least one of e-mail or mobile number is mandatory at profile creation (not both — some customers decline e-mail); the system supports conditional "either/or" mandatory-field rules. *(agreed · MoM 20 Aug 2026, 4.1 CRM; 5. Key Decisions · DI-372)*
- Profile fields must be fully configurable/user-defined (e.g. nationality vs. country of residence), with per-field unique and required flags; group profiles (group name, description, contact person) are configured independently. *(client request · MoM 20 Aug 2026, 4.1 CRM — Customer Profiles, Unique Fields & Family/Guardian Linking · DI-371)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-736` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-736`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 4: Works in Guest Master Configuration → Configure the shared guest data model without software changes. Configuration Scope of Work / Version 1.0 6 Maintain standard and custom attributes, field groups, labels, data types, defaults …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-736?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save guest attribute model, Cancel.
- [ ] Every transition is wired: `BO-734`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`, `MARKETING_MANAGE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-737` Customer 360 Profile

**Present a consolidated, actionable view of one guest. Display identity, contacts, preferences, household, organization, membership, loyalty, wallet, tickets, bookings and visits. Show LTV, engagement, churn risk, communication eligibility, open cases, pending waivers and recent activity. Provide permission-controlled quick actions for communication, booking, case creation, campaign enrollment and profile maintenance. Allow role-based widget configuration while keeping the Customer Master Service as the system of record. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW`, `PRODUCT_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/customer-360-profile-bo-737` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Subject | picker: choose a subject | — | — | `listCustomerServiceProfile` ?subjectId |
| Dimension | select | — | Customer type · Customer segment · Account type · Crm segment · Vip status · Corporate customer · Employee staff · Partner customer · Guest registered user | `listCustomerSegmentProfile` ?dimension |
| Segment source | radio group | — | Crm · Membership · B2B partner · Corporate account · Customer profile | `listCustomerSegmentProfile` ?segmentSource |
| Customer | text field | — | — | `listCustomerSegmentProfile` ?customerId |
| Status | radio group | — | Draft · Active · Disabled · Expired | `listCustomerSegmentProfile` ?status |
| Search | text field | — | — | `listCustomerSegmentProfile` ?search |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listCustomerServiceProfile` (onLoad, Customer 360° Service Profile); `listCustomerSegmentProfile` (onLoad, Customer Segment & Profile Pricing Rules)

**Where the user goes next**

- → `BO-734` CRM Command Center: *Back to CRM Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer 360 profile list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer 360 profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer 360 profile yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer 360 profile are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCustomerServiceProfile` → `CASE_VIEW` (read) · staff
- `listCustomerSegmentProfile` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Repeat guest checkouts with the same email (or phone) consolidate into one profile automatically; a manual merge-customer-profile function remains for edge cases (e.g. slightly different name spelling under the same email). Allam cited a system where 10 transactions created 10 profiles. *(agreed · MoM 18 Sep 2026, 4.8 Guest Checkout & Profile Deduplication — Extended Discussion · DI-941)*
- Entitlements portfolio is used both by the guest (mobile app) and by customer service: one view of restrictions, wallet balance and all entitlements; a unified list across a visit (e.g. four admissions, two fast passes, a meal package, a parking entitlement). *(client request · MoM 7 Sep 2026, 4.9 Entitlements Portfolio - Structure, Family/Group & Assignment · DI-667)*
- Decision: one unified customer profile across ticketing, F&B and retail gives a 360° view of guest activity and avoids duplicates; e.g. a guest who buys tickets online and later dines is matched by name/mobile to the same profile. *(agreed · MoM 18 Aug 2026, 4.9 Unified Customer Profile · DI-339)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-737` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-737`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 6: Works in Customer 360 Profile → Present a consolidated, actionable view of one guest. Display identity, contacts, preferences, household, organization, membership, loyalty, wallet, tickets, bookings and visits. Show LTV …
- ADR-0023 *— Personal data lives apart from the append-only ledger* (`docs/adr/0023-pii-separation.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-737?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-734`.
- [ ] Every gated control is gated: `CASE_VIEW`, `PRODUCT_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-738` Activity Timeline

**Provide a chronological record of guest activity across the connected platform. Ingest purchases, ticket usage, reservations, visits, membership changes, loyalty, wallet, campaigns, messages, cases, surveys and waivers. Filter by date, channel, venue, event type, source system and outcome and open the related source transaction. Distinguish operational facts from user notes and AI-derived events and preserve event timestamps and source identifiers. Support reliable ordering, pagination and audit evidence without allowing historical events to be silently altered. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `guestId` (navigation), `subjectId` (navigation) |
| Route | `/engagement-support/activity-timeline-bo-738` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Where the user goes next**

- → `BO-734` CRM Command Center: *Back to CRM Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The activity timeline list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the activity timeline untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No activity timeline yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the activity timeline are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getGuestProfile` → `GUEST_VIEW` (read) · staff, guest
- `getGuestIntelligence` → `GUEST_VIEW` (read) · staff
- `getGuestRelationships` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.8 | APIs shall support guest profile creation, updates, segmentation, communication preferences and activity history retrieval. | Developer & API Management | CONTRACTED | `getGuestProfile` |
| 22.2.27 | CRM APIs | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 22.2.28 | CRM Audit Trail | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 5.3.25 | Generate AI insights such as predicted next visit, churn risk, preferred products, preferred attractions, lifetime value, and upsell recommendations. | F&B & Guest Management | CONTRACTED_PARTIAL | `getGuestIntelligence` |
| 5.4.22 | Identify customers at risk of disengagement. | F&B & Guest Management | CONTRACTED | `getGuestIntelligence` |
| 5.4.33 | AI provides personalized engagement and retention recommendations. | F&B & Guest Management | CONTRACTED | `getGuestIntelligence` |
| 22.2.22 | AI Guest Insights | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.2.23 | AI Churn Prediction | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.2.24 | AI Next Best Action | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.6.19 | AI Engagement Optimization | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.14.13 | AI Churn Prediction Segments | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.14.14 | AI Upgrade Opportunities | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-738` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-738`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 8: Works in Activity Timeline → Provide a chronological record of guest activity across the connected platform. Ingest purchases, ticket usage, reservations, visits, membership changes, loyalty, wallet, campaigns, messages, cases …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-738?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-734`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-739` Contact & Preferences

**Maintain verified contact information and service preferences for each guest. Manage multiple email addresses, phone numbers, physical addresses, emergency contacts and social identifiers. Record preferred language, channel, contact time, frequency, interests, favorite attractions and visit preferences. Store accessibility and dietary requirements with suitable sensitivity and role restrictions. Configuration Scope of Work / Version 1.0 7 Show verification, suppression and consent status while delegating legal enforcement to the shared Consent Service. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW`, `GUEST_VIEW_PII` (1 configure, 1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `guestId` (navigation), `verificationId` (navigation) |
| Route | `/engagement-support/contact-preferences-bo-739` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Pending · Verified · Rejected · Resubmission requested | `listGuestIdentityVerifications` ?status |
| Subject | picker: choose a subject | — | — | `listGuestIdentityVerifications` ?subjectId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listGuestIdentityVerifications` (onLoad, Guest ID documents awaiting review)

**Where the user goes next**

- → `BO-734` CRM Command Center: *Back to CRM Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The contact preferences list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the contact preferences untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No contact preferences yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the contact preferences are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already decided; 422 A rejection or resubmission request without a reason |

#### Permissions

- `getGuestTimeline` → `GUEST_VIEW` (read) · staff
- `listGuestIdentityVerifications` → `GUEST_VIEW_PII` (operate) · staff
- `decideGuestIdentityVerification` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-739` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-739`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 10: Works in Contact & Preferences → Maintain verified contact information and service preferences for each guest. Manage multiple email addresses, phone numbers, physical addresses, emergency contacts and social identifiers. Record …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-739?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-734`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`, `GUEST_VIEW_PII`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-740` Family & Guardians

**Model households, dependants and guardians while preserving each person's individual identity. Create family groups and link parent, guardian, spouse and dependant relationships with effective dates. Configure purchasing, booking, profile-management and waiver-signing authority for minors and dependants. Support shared or separate benefits, memberships, bookings and communications without merging individual profiles. Record additions, removals, authority changes and exceptions in a complete relationship audit trail. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `subjectId` (navigation) |
| Route | `/engagement-support/family-guardians-bo-740` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save guest preferences (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-734` CRM Command Center: *Back to CRM Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The family guardians list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the family guardians untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No family guardians yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the family guardians are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `updateGuestPreferences` → `GUEST_MANAGE` (configure) · staff, guest
- `getGuestProfile` → `GUEST_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.8 | APIs shall support guest profile creation, updates, segmentation, communication preferences and activity history retrieval. | Developer & API Management | CONTRACTED | `getGuestProfile` |
| 22.2.27 | CRM APIs | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 22.2.28 | CRM Audit Trail | Marketing & CRM | CONTRACTED | `getGuestProfile` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Family/guardian linking is core (e.g. father, spouse, daughter as one family unit), consistent with family tickets/memberships; the same linking model extends to operations-team entitlement relationships. *(agreed · MoM 20 Aug 2026, 4.1 CRM — Customer Profiles, Unique Fields & Family/Guardian Linking · DI-373)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-740` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-740`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 12: Works in Family & Guardians → Model households, dependants and guardians while preserving each person's individual identity. Create family groups and link parent, guardian, spouse and dependant relationships with effective dates. …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-740?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save guest preferences, Cancel.
- [ ] Every transition is wired: `BO-734`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-741` Corporate & Groups

**Link guests to corporate, school, travel and group structures. Support corporate accounts, schools, tour operators, travel agencies, resellers, clubs, teams and event groups. Define contacts, participant roles, billing relationships, booking authority and relationship validity periods. Display associated bookings, memberships, agreements and activity while respecting organizational access boundaries. Expose relationships to B2B, reservations, cases and reporting through secured services and APIs. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `guestId` (navigation) |
| Route | `/engagement-support/corporate-groups-bo-741` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save guest relationships (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-734` CRM Command Center: *Back to CRM Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The corporate groups list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the corporate groups untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No corporate groups yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the corporate groups are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getGuestRelationships` → `GUEST_VIEW` (read) · staff
- `setGuestRelationships` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- One unified flow for groups, schools and corporates: inquiry > package builder > quotation > approval > confirmed booking. *(agreed · MoM 31 Aug 2026, 4.7 Group Sales / 5. Key Decisions · DI-565)*
- Corporate/B2B profiles have a self-service onboarding flow: company profile (name, address, trade licence, VAT certificate) → admin approval/rejection → rate/product setup → credential issuance. *(client request · MoM 20 Aug 2026, 4.1 CRM — Customer Profiles, Unique Fields & Family/Guardian Linking · DI-375)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-741` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-741`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 14: Works in Corporate & Groups → Link guests to corporate, school, travel and group structures. Support corporate accounts, schools, tour operators, travel agencies, resellers, clubs, teams and event groups. Define contacts …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-741?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save guest relationships, Cancel.
- [ ] Every transition is wired: `BO-734`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-742` Commerce & Documents

**Consolidate the guest's commercial, service and document history. Provide tabs for tickets, reservations, memberships, loyalty, wallet, refunds, exchanges, transfers, upgrades and attendance. Display communications, cases, survey responses, ratings, reviews, waivers, identification documents and signed agreements. Link every item to its source transaction and show status, value, channel, venue, timestamps and authorized actions. Apply RBAC/PBAC, masking, retention, download and audit policies to financial, identity and legal records. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work / Version 1.0 8**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `guestId` (navigation) |
| Route | `/engagement-support/commerce-documents-bo-742` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save guest relationships (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-734` CRM Command Center: *Back to CRM Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commerce documents list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commerce documents untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commerce documents yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commerce documents are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setGuestRelationships` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-742` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-742`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 16: Works in Commerce & Documents → Consolidate the guest's commercial, service and document history. Provide tabs for tickets, reservations, memberships, loyalty, wallet, refunds, exchanges, transfers, upgrades and attendance. Display …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-742?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save guest relationships, Cancel.
- [ ] Every transition is wired: `BO-734`.
- [ ] Every gated control is gated: `GUEST_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-743` AI Guest Intelligence

**Turn the unified record into explainable customer insight and recommended actions. Calculate historical and predicted LTV, engagement, churn, inactivity, cancellation, affinity and upgrade propensity. Classify audiences and recommend the next campaign, offer, product, membership, reward, channel and next best action. Display contributing factors, confidence, model/version, expected impact and policy or data limitations. Require consent and eligibility checks, support accept/reject/feedback actions and audit all human and AI decisions. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work / Version 1.0 9 Board 2 - Identity Resolution, Consent & Data Privacy Figure 2. High-definition configuration board with all 10 screens. Configuration Scope of Work / Version 1.0 10**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_VIEW`, `GUEST_VIEW_PII` (1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `guestId` (navigation) |
| Route | `/engagement-support/ai-guest-intelligence-bo-743` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-734` CRM Command Center: *Back to CRM Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest intelligence list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the guest intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getGuestTimeline` → `GUEST_VIEW` (read) · staff
- `uploadGuestDocument` → `GUEST_VIEW_PII` (operate) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-743` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS70 Marketing CRM Configuration Reference v1.0 Board 1.dc.html#bo-743`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 1
- Flow F244 *Marketing CRM Configuration Reference v1.0 board 1: CRM Command Center*, step 18: Works in AI Guest Intelligence → Turn the unified record into explainable customer insight and recommended actions. Calculate historical and predicted LTV, engagement, churn, inactivity, cancellation, affinity and upgrade …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-743?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-734`.
- [ ] Every gated control is gated: `GUEST_VIEW`, `GUEST_VIEW_PII`.
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

**10 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"adjustLoyaltyPoints": {"method":"POST","path":"/guests/{subjectId}/loyalty/adjust","contract":"marketing-crm","summary":"Manually adjust points","permission":"LEDGER_POST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AdjustLoyaltyPointsRequest","responds":"LoyaltyAdjustmentResult"},
"decideGuestIdentityVerification": {"method":"POST","path":"/guest-identity-verifications/{verificationId}/decision","contract":"identity","summary":"Verify or refuse a guest's identity document","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"IdentityGuestVerification"},
"getConsentHistory": {"method":"GET","path":"/guests/{subjectId}/consents/history","contract":"marketing-crm","summary":"Full consent history","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getGuestAttributeModel": {"method":"GET","path":"/guest-attribute-model","contract":"marketing-crm","summary":"The shared guest data model","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"GuestAttributeModel"},
"getGuestIntelligence": {"method":"GET","path":"/guests/{guestId}/intelligence","contract":"marketing-crm","summary":"Value, engagement, churn and propensity, with their reasons","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuestIntelligence"},
"getGuestLoyalty": {"method":"GET","path":"/guests/{subjectId}/loyalty","contract":"marketing-crm","summary":"A guest's loyalty position","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"programmeId","in":"query","required":true}],"requestBody":null,"responds":"LoyaltyPosition"},
"getGuestProfile": {"method":"GET","path":"/guests/{subjectId}","contract":"marketing-crm","summary":"Read a guest profile","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuestProfileDetail"},
"getGuestRelationships": {"method":"GET","path":"/guests/{guestId}/relationships","contract":"marketing-crm","summary":"Household, guardians, corporate and group links","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuestRelationship"},
"getGuestTimeline": {"method":"GET","path":"/guests/{guestId}/timeline","contract":"marketing-crm","summary":"Everything this guest did, in order, across the platform","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"kinds","in":"query","required":null},{"name":"venueId","in":"query","required":null}],"requestBody":null,"responds":"GuestTimelineEvent"},
"listCustomerSegmentProfile": {"method":"GET","path":"/customer-segment-profile","contract":"catalogue","summary":"Customer Segment & Profile Pricing Rules","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"dimension","in":"query","required":false},{"name":"segmentSource","in":"query","required":false},{"name":"customerId","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCustomerServiceProfile": {"method":"GET","path":"/customer-service-profile","contract":"marketing-crm","summary":"Customer 360° Service Profile","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"subjectId","in":"query","required":true}],"requestBody":null,"responds":"Customer360ServiceProfileView"},
"listGuestIdentityVerifications": {"method":"GET","path":"/guest-identity-verifications","contract":"identity","summary":"Guest identity verifications, the review queue first","permission":"GUEST_VIEW_PII","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"subjectId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSegments": {"method":"GET","path":"/segments","contract":"marketing-crm","summary":"List segments","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"mergeGuestProfiles": {"method":"POST","path":"/guests/{subjectId}/merge","contract":"marketing-crm","summary":"Merge a duplicate profile into this one","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MergeResult"},
"searchGuests": {"method":"GET","path":"/guests","contract":"marketing-crm","summary":"Search guest profiles","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"search","in":"query","required":null},{"name":"segmentId","in":"query","required":null},{"name":"hasConsentFor","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setGuestAttributeModel": {"method":"PUT","path":"/guest-attribute-model","contract":"marketing-crm","summary":"Change the model, as a version","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GuestAttributeModel","responds":"GuestAttributeModel"},
"setGuestExtraFields": {"method":"PUT","path":"/guest-extra-fields","contract":"marketing-crm","summary":"Define the extra guest fields","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GuestExtraFieldDefinition","responds":"GuestExtraFieldDefinition"},
"setGuestRelationships": {"method":"PUT","path":"/guests/{guestId}/relationships","contract":"marketing-crm","summary":"Link people without merging them","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestRelationship"},
"updateGuestPreferences": {"method":"PUT","path":"/guests/{subjectId}/preferences","contract":"marketing-crm","summary":"The things a regular should not have to say twice","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"lastWriterWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GuestPreferences","responds":"GuestPreferences"},
"updateGuestProfile": {"method":"PATCH","path":"/guests/{subjectId}","contract":"marketing-crm","summary":"Amend a guest profile","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestProfileDetail"},
"uploadGuestDocument": {"method":"POST","path":"/guest-documents","contract":"marketing-crm","summary":"Store a guest photo, ID or signed document","permission":"GUEST_VIEW_PII","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GuestDocument","responds":"GuestDocument"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AdjustLoyaltyPointsRequest": {"type":"object","x-ticvai-persistence":"none — writes marketing.loyalty_points","description":"**A correction is a new entry, never an edit.** Reversing an entry writes a row pointing at it through `reversedLoyaltyPointsId`; granting goodwill writes a row with no reversal target. Either way the movement has a reason and an author, and the history stays walkable.\n","required":["programmeId","points","reason"],"properties":{"programmeId":{"type":"string","format":"uuid"},"points":{"type":"integer","description":"Signed. Negative removes points, and the balance may not go below zero."},"reason":{"type":"string","description":"**Goodwill, correction or expiry reversal, and nothing else (decided 28 September, audit R149).** A service-recovery grant is `goodwill`, a fraud or migration fix is `correction`, and returning points that expired in error is `expiryReversal`. None of them moves the tier or `lifetimePoints`.\n","enum":["goodwill","correction","expiryReversal"]},"reversedLoyaltyPointsId":{"type":"string","format":"uuid","nullable":true,"description":"The entry this reverses, when it is a reversal. **Set it and the sign is checked against the original** — a reversal that does not cancel what it names is a second grant wearing a correction's label.\n"},"notes":{"type":"string","maxLength":1000,"nullable":true}}},
"ConsentDecision": {"type":"string","enum":["granted","withdrawn","notAsked"]},
"ConsentPurpose": {"type":"string","enum":["marketing","personalisation","profiling","thirdPartySharing","aiProcessing","transactional"]},
"ConsentRecord": {"x-ticvai-persistence":"marketing.consent_record + marketing.consent_record_channel","allOf":[{"$ref":"#/components/schemas/RecordConsentRequest"},{"type":"object","required":["id","subjectId"],"properties":{"id":{"type":"string"},"subjectId":{"type":"string","format":"uuid"},"recordedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true,"description":"The order whose checkout carried the opt-in (source `checkout`, M18-15): the UUIDv7 of orders.sales_order. Null for every other source.","x-ticvai-references":"orders.sales_order"},"verifiedContactRef":{"type":"string","nullable":true,"maxLength":128,"description":"The verified contact the checkout opt-in was given against (ADR-0045), as the keyed hash the guest match policy uses; never the raw address. It is how a checkout consent given without an account is attached to the profile when the contact later matches one."},"supersededAt":{"type":"string","format":"date-time","nullable":true}}}]},
"ConsentState": {"x-ticvai-persistence":"none — projection over consent_record","type":"object","required":["subjectId","purposes"],"properties":{"subjectId":{"type":"string","format":"uuid"},"purposes":{"type":"array","items":{"type":"object","required":["purpose","decision","requiresRenewal"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"decision":{"$ref":"#/components/schemas/ConsentDecision"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string","nullable":true},"requiresRenewal":{"type":"boolean","description":"True where the notice has been superseded since consent was given."},"decidedAt":{"type":"string","format":"date-time","nullable":true}}}}}},
"CreateSegmentRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","criteria"],"properties":{"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid"},"match":{"type":"string","enum":["all","any"],"default":"all"},"criteria":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/SegmentCriterion"}},"excludeSegmentIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"Customer360ServiceProfileView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.guest_profile, pii.subject, pii.subject_contact, marketing.loyalty_position, marketing.guest_preference, marketing.consent_record, marketing.suppression, marketing.case, orders.sales_order, orders.reservation, orders.group_booking, access.entitlement and wallet.balance","description":"The service view of one guest. Fields the caller may not see are null, never omitted.","required":["customerId","customerSince","openCases","serviceAlerts"],"properties":{"customerId":{"type":"string","format":"uuid","description":"The guest's `subjectId`."},"customerName":{"type":"string","nullable":true,"description":"Null unless the caller holds GUEST_VIEW_PII."},"customerType":{"type":"string","enum":["individual","member","groupOrganiser","corporate","partner"]},"membershipStatus":{"type":"string","enum":["none","active","expiring","lapsed"]},"loyaltyTier":{"type":"string","nullable":true},"preferredLanguage":{"type":"string","maxLength":10,"nullable":true},"country":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"contactDetails":{"type":"object","description":"Masked (e.g. `j***@example.com`, `+971 ** *** 4821`) unless the caller holds GUEST_VIEW_PII.","properties":{"email":{"type":"string","nullable":true},"phone":{"type":"string","nullable":true}}},"customerSince":{"type":"string","format":"date-time"},"customerValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Lifetime net spend across the tenant."},"openCases":{"type":"integer","minimum":0},"riskAttentionIndicator":{"type":"string","enum":["none","attention","risk"],"description":"`attention` with an open complaint or an unresolved refund case; `risk` with a breached SLA or a repeat contact on the same issue."},"upcomingTickets":{"type":"integer","minimum":0},"activeMembership":{"type":"object","nullable":true,"properties":{"membershipId":{"type":"string"},"planName":{"type":"string"},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"walletBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"activeReservations":{"type":"integer","minimum":0},"futureGroupBookings":{"type":"integer","minimum":0},"openOrders":{"type":"integer","minimum":0},"serviceAlerts":{"type":"array","maxItems":20,"items":{"type":"object","required":["kind","message"],"properties":{"kind":{"type":"string","enum":["eventSoon","unresolvedRefundCase","membershipExpiring","openComplaint","communicationRestricted"]},"message":{"type":"string"},"referenceId":{"type":"string","nullable":true}}}},"preferredCommunicationChannel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"nullable":true},"marketingConsent":{"$ref":"#/components/schemas/ConsentDecision"},"accessibilityRequirements":{"type":"array","nullable":true,"description":"Null unless the caller holds GUEST_VIEW_PII.","items":{"type":"string"}},"communicationRestrictions":{"type":"array","description":"Channels the guest must not be contacted on (`getSuppressionList`).","items":{"$ref":"#/components/schemas/MessageChannel"}},"aiSummary":{"type":"object","nullable":true,"description":"Where the AI policy enables `summarise`. AI-derived and labelled as such.","properties":{"text":{"type":"string","maxLength":2000},"generatedAt":{"type":"string","format":"date-time"}}}}},
"CustomerSegmentProfilePricingRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Customer Segment & Profile Pricing Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleName":{"type":"string","description":"Rule Name"},"segment":{"type":"string","description":"Segment: the value the dimension must equal, e.g. VIP"},"applicableProducts":{"type":"array","items":{"type":"string"},"description":"Applicable Products: product ids or product category codes"},"priceList":{"type":"string","description":"Price List: the list whose rate the rule selects"},"rate":{"type":"string","description":"Rate: code of the rate used when the rule matches, e.g. VIP Adult"},"priority":{"type":"integer","description":"Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"},"status":{"type":"string","description":"Status: draft, active, disabled or expired"},"ruleId":{"type":"string","description":"Rule ID"},"dimension":{"type":"string","enum":["customerType","customerSegment","accountType","crmSegment","vipStatus","corporateCustomer","employeeStaff","partnerCustomer","guestRegisteredUser"],"description":"Supported Dimension (p.25) the rule tests"},"segmentSource":{"type":"string","enum":["crm","membership","b2bPartner","corporateAccount","customerProfile"],"description":"Customer Segment Source (p.26) the segment is read from"},"fallbackRate":{"type":"string","description":"Fallback (p.26): rate used when the customer no longer qualifies; the standard rate by default (decided 29 September, readiness close-out)"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true}}},
"GuestAttributeModel": {"type":"object","x-ticvai-persistence":"marketing.guest_attribute_model","description":"Board 1.3. **Visibility by jurisdiction is what makes this a model and not a form.**","properties":{"version":{"type":"integer"},"fieldGroups":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"label":{"type":"string"},"displayOrder":{"type":"integer"}}}},"attributes":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"label":{"type":"string"},"groupCode":{"type":"string"},"dataType":{"type":"string"},"standard":{"type":"boolean","default":false},"mandatory":{"type":"boolean","default":false},"defaultValue":{"nullable":true},"allowedValues":{"type":"array","items":{"type":"string"}},"validationExpression":{"type":"string","nullable":true},"sensitive":{"type":"boolean","default":false},"visibleToRoles":{"type":"array","items":{"type":"string"}},"editableByRoles":{"type":"array","items":{"type":"string"}},"lawfulInJurisdictions":{"type":"array","items":{"type":"string"},"description":"**Empty means everywhere.** A nationality field lawful in one jurisdiction and not another cannot be a column somebody ships.\n"},"countsTowardCompleteness":{"type":"boolean","default":false}}}},"identifiers":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"primary":{"type":"boolean","default":false},"sourceSystem":{"type":"string","nullable":true},"sourcePriority":{"type":"integer"}}}},"publishedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"GuestDocument": {"type":"object","x-ticvai-persistence":"marketing.guest_document","description":"BL-133. **No store for guest photos, avatars, IDs or signed documents anywhere.**\nDeliberately separate from `assets`, which holds a tenant's media library. **A guest's passport scan is not a marketing asset** — it has a different retention clock, a different access rule and a different reason to exist, and putting it in the same store means one careless query returns both.\n","required":["id","subjectId","kind","storageRef","retainUntil"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["avatar","idDocument","visa","signedWaiver","medicalNote","accessibilityEvidence","photo","other"]},"storageRef":{"type":"string","description":"**The stored object's key in the guest-document store**, which is deliberately not `assets` (BL-133). No operation in this contract issues one yet: `assets` `createUpload` is staff-only and writes the media library, so the upload step for this store is still to be designed.\n"},"contentType":{"type":"string"},"consentPurposeId":{"type":"string","format":"uuid"},"retainUntil":{"type":"string","format":"date","description":"**Required, not optional.** A guest document with no deletion date is a guest document kept forever, and the retention question is the one CF-64 is open on.\n**Kept until its purpose ends, then for the period client counsel sets (decided 28 September, audit R149).** The caller sets `retainUntil` to the end of the purpose (the visit, the waiver's validity, the visa's expiry) plus that period. **The period per `kind` is an open value**: until counsel names it, it is zero, so the document is deleted when the purpose ends.\n"},"uploadedAt":{"readOnly":true,"type":"string","format":"date-time"},"uploadedByPrincipalId":{"readOnly":true,"type":"string","format":"uuid","nullable":true}}},
"GuestExtraFieldDefinition": {"type":"object","x-ticvai-persistence":"none — composed from a field and its options","description":"**A select with no options is not a field**, so the options come back with the definition rather than from a second call.\n","required":["field"],"properties":{"field":{"$ref":"#/components/schemas/MarketingGuestExtraField"},"options":{"type":"array","items":{"$ref":"#/components/schemas/MarketingGuestExtraOption"}}}},
"GuestIntelligence": {"type":"object","description":"Board 1.10. **Explainable, or an agent will ignore it or over-trust it.**","properties":{"subjectId":{"type":"string","format":"uuid"},"scores":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["historicalLtv","predictedLtv","engagement","churnRisk","inactivityRisk","cancellationRisk","upgradePropensity","nextPurchasePropensity"]},"value":{"type":"number"},"band":{"type":"string","nullable":true},"confidence":{"type":"number","nullable":true},"modelId":{"type":"string","nullable":true},"modelVersion":{"type":"string","nullable":true},"computedAt":{"type":"string","format":"date-time"},"factors":{"type":"array","items":{"type":"object","properties":{"factor":{"type":"string"},"contribution":{"type":"number"}}}},"limitations":{"type":"array","items":{"type":"string"},"description":"**Policy and data limitations travel with the score**, so the rule that prediction never overrides consent cannot be forgotten downstream.\n"}}}},"affinities":{"type":"array","items":{"type":"object","properties":{"productCategoryId":{"type":"string","format":"uuid"},"label":{"type":"string"},"strength":{"type":"number"}}}},"nextBestActions":{"type":"array","items":{"type":"object","properties":{"action":{"type":"string"},"expectedImpact":{"type":"string","nullable":true},"confidence":{"type":"number","nullable":true}}}}}},
"GuestPreferences": {"type":"object","x-ticvai-persistence":"marketing.guest_preference","description":"**What the guest likes, kept apart from what they permit** (consent) and from who they are (the profile). One row per subject. `dietary` and `accessibility` are here rather than as tags because BL-134 gives them their own consent purpose and retention.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true},"subjectId":{"type":"string","format":"uuid","readOnly":true},"seatingPreference":{"type":"string","nullable":true,"maxLength":200},"drinkPreferences":{"type":"array","items":{"type":"string"}},"dietary":{"type":"array","description":"Also written by `updateMyProfile`.","items":{"type":"string"}},"accessibility":{"type":"array","description":"Also written by `updateMyProfile`.","items":{"type":"string"}},"preferredChannel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"x-ticvai-persisted":false,"description":"**Stored on the profile** (`GuestProfile.preferredChannel`) — carried here because the preference screen edits it beside the rest.\n"},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"GuestProfile": {"x-ticvai-persistence":"marketing.guest_profile","type":"object","required":["subjectId","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"subjectId":{"type":"string","format":"uuid","description":"Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger.\n"},"displayName":{"type":"string","nullable":true},"email":{"type":"string","nullable":true},"phone":{"type":"string","nullable":true},"preferredLanguage":{"type":"string","nullable":true},"preferredChannel":{"$ref":"#/components/schemas/MessageChannel"},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells. Marketing acts locally."},"tags":{"type":"array","items":{"type":"string"}},"engagementScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"description":"22.2.20 and 22.2.21. **`lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not.** They are different questions: a guest who spent a lot once and a guest who visits monthly have the same LTV and need opposite treatment.\n**Recency, frequency and breadth, not spend** — spend is already `lifetimeValue`, and folding it in here would make one number twice.\n"},"engagementTier":{"type":"string","nullable":true,"enum":["new","active","occasional","lapsing","lapsed","dormant"],"description":"5.3.19. **Automatic classification, computed rather than assigned.** `lapsing` is the tier the whole field exists for — **a guest who has not been for a while and still might is the only one marketing can change**, and lumping them with `lapsed` wastes the window.\n"},"lifetimeValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"visitCount":{"type":"integer"},"lastVisitAt":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"},"mergedIntoSubjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`**, which retain it as a redirect rather than deleting it. A read that lands here follows it; a second merge of a profile that has one is refused as `alreadyMerged`.\n"},"mergedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"GuestProfileDetail": {"x-ticvai-persistence":"marketing.guest_profile","allOf":[{"$ref":"#/components/schemas/GuestProfile"},{"type":"object","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"consents":{"$ref":"#/components/schemas/ConsentState"},"loyalty":{"$ref":"#/components/schemas/LoyaltyPosition"},"openCaseCount":{"type":"integer"},"recentOrderIds":{"type":"array","items":{"type":"string"}},"membershipIds":{"type":"array","items":{"type":"string","format":"uuid"}},"notes":{"type":"string","nullable":true}}}]},
"GuestRelationship": {"type":"object","x-ticvai-persistence":"marketing.guest_relationship","x-ticvai-retired-columns":["related_guest_id"],"description":"Boards 1.7 and 1.8. **Links people without merging them**, which is the whole design.\n","required":["relatedSubjectId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"relatedSubjectId":{"type":"string","format":"uuid","nullable":true},"organisationId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["parent","guardian","spouse","dependant","householdMember","employee","student","groupLeader","travelAgent","reseller"]},"authorities":{"type":"array","items":{"type":"string","enum":["purchaseFor","bookFor","manageProfile","signWaiver","viewHistory","receiveCommunications"]},"description":"**Four different permissions, not one relationship.** A guardianship granting all of them forever survives the child becoming an adult.\n"},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"sharedBenefits":{"type":"boolean","default":false},"verifiedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"GuestTimelineEvent": {"type":"object","description":"Board 1.5. **Facts, notes and predictions distinguished on the row.**","properties":{"id":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"kind":{"type":"string","enum":["purchase","ticketUsed","reservation","visit","membershipChange","loyalty","wallet","campaign","message","case","survey","waiver","note","prediction"]},"nature":{"type":"string","enum":["operationalFact","userNote","aiDerived"],"description":"**A prediction and a gate scan are both useful and only one happened.**"},"summary":{"type":"string"},"channel":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"sourceContract":{"type":"string","nullable":true},"sourceReferenceId":{"type":"string","format":"uuid","nullable":true},"value":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"outcome":{"type":"string","nullable":true}}},
"IdentityGuestVerification": {"type":"object","x-ticvai-persistence":"identity.guest_identity_verification","description":"**One guest identity-document verification** (5.3.21; decided 29 September, build pass): the document it checks, its status, the method and who decided. The document itself is `pii.subject_document`; this row holds no document number.","required":["id","subjectId","status","submittedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"subjectId":{"type":"string","format":"uuid"},"subjectDocumentId":{"type":"string","format":"uuid","description":"The `pii.subject_document` row submitted."},"documentKind":{"type":"string","enum":["passport","emiratesId","nationalId","drivingLicence","residencePermit","other"]},"documentNumberLast4":{"type":"string","maxLength":4,"nullable":true,"readOnly":true},"reason":{"type":"string","enum":["policyRequired","ageRestrictedPurchase","residentPricing","accountRecovery"]},"status":{"type":"string","enum":["pending","verified","rejected","resubmissionRequested"],"readOnly":true},"method":{"type":"string","enum":["manualReview","documentScanner","provider"],"nullable":true,"readOnly":true},"decisionReason":{"type":"string","maxLength":300,"nullable":true,"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"submittedAt":{"type":"string","format":"date-time","readOnly":true},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"documentImageDeletedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the scan (and any selfie) was deleted under the policy's retention."}}},
"LoyaltyAdjustmentResult": {"type":"object","x-ticvai-persistence":"none — composed from the entry posted and the resulting position","description":"**Both halves of an adjustment, because returning only the balance is the defect decision 8 named.** Until 20 September this operation moved `marketing.loyalty_position` and returned it, and posted nothing to `marketing.loyalty_points` — so a manual adjustment was the one movement in the system that could not be walked back to a reason.\n","required":["entry","position"],"properties":{"entry":{"$ref":"#/components/schemas/MarketingLoyaltyPoints"},"position":{"$ref":"#/components/schemas/LoyaltyPosition"}}},
"LoyaltyPosition": {"x-ticvai-persistence":"marketing.loyalty_position","type":"object","required":["subjectId","programmeId","pointsBalance","tierCode"],"properties":{"leaderboardNickname":{"type":"string","nullable":true,"maxLength":24,"description":"BL-173. **The name shown on a leaderboard, chosen by the guest.** Offered whenever they reach the board and changeable afterwards; `setLeaderboardNickname` is the only thing that writes it.\n**Null means the guest has not chosen one yet, and the board shows a generated `Player-4821` in its place** — never `pii.subject.display_name`, which would disclose silently on the day a guest first placed and is the case this field exists to prevent.\n**The generated name is computed at read time and not stored here.** Writing it would make *\"has this guest chosen a name\"* unanswerable, and that flag is what the prompt-on-reaching-the-board depends on.\n"},"subjectId":{"type":"string","format":"uuid"},"programmeId":{"type":"string","format":"uuid"},"pointsBalance":{"type":"integer"},"lifetimePoints":{"type":"integer"},"tierId":{"type":"string","format":"uuid","nullable":true,"description":"**The tier this row's `tierCode` and `tierName` are a copy of.** Added 20 September with `marketing.programme_tier`: the two strings were a cache of something that did not exist, and a cache with no source cannot be rebuilt or audited.\n"},"tierCode":{"type":"string"},"tierName":{"type":"string"},"pointsToNextTier":{"type":"integer","nullable":true},"nextExpiryPoints":{"type":"integer","nullable":true},"nextExpiryAt":{"type":"string","format":"date-time","nullable":true}}},
"MarketingGuestExtraField": {"type":"object","x-ticvai-persistence":"marketing.guest_extra_field","description":"**Taken from the backend workbook, 20 September.** NEW TABLE. Defines an extra field that Admin wants to add to the customer form, such as Date of Birth, Emergency Contact, or Jersey Size.","required":["tenantId","name","type","isRequired","displayOrder","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"tenantId":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":150},"type":{"type":"string","maxLength":30},"isRequired":{"type":"boolean"},"displayOrder":{"type":"integer"},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time","nullable":true}}},
"MarketingGuestExtraOption": {"type":"object","x-ticvai-persistence":"marketing.guest_extra_option","description":"**Taken from the backend workbook, 20 September.** NEW TABLE. Stores dropdown choices only when an extra field uses SELECT type, for example Language = English, Hindi, Marathi.","required":["fieldId","name","displayOrder","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"fieldId":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":150},"displayOrder":{"type":"integer"},"isActive":{"type":"boolean"}}},
"MarketingLoyaltyPoints": {"type":"object","x-ticvai-persistence":"marketing.loyalty_points","description":"**Taken from the backend workbook, 20 September.** Stores every loyalty point earn, redeem, expire, adjustment, or reversal transaction for a customer.","required":["programId","customerId","transactionType","points","balanceAfter","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"programId":{"type":"string","format":"uuid"},"customerId":{"type":"string","format":"uuid"},"transactionType":{"type":"string","maxLength":30},"points":{"type":"number"},"balanceAfter":{"type":"number"},"sourceType":{"type":"string","maxLength":50,"nullable":true},"sourceReferenceId":{"type":"string","format":"uuid","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true},"reversedLoyaltyPointsId":{"type":"string","format":"uuid","nullable":true},"notes":{"type":"string","maxLength":500,"nullable":true},"reason":{"type":"string","nullable":true,"description":"For a manual movement, `AdjustLoyaltyPointsRequest.reason`. Null for an accrual, a redemption or an expiry, whose `transactionType` and source already say why. The three manual types are the only ones (audit R149).","enum":["goodwill","correction","expiryReversal"]},"authorPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who posted a manual movement. Null where the platform posted it."},"createdAt":{"type":"string","format":"date-time"}}},
"MergeResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["survivingSubjectId","absorbedSubjectId","transferred"],"properties":{"survivingSubjectId":{"type":"string","format":"uuid"},"absorbedSubjectId":{"type":"string","format":"uuid"},"transferred":{"type":"object","properties":{"orders":{"type":"integer"},"cases":{"type":"integer"},"loyaltyPoints":{"type":"integer","description":"The total points moved across every programme. The per-programme outcome is `loyaltyProgrammes`."}}},"loyaltyProgrammes":{"type":"array","description":"**One entry per loyalty programme either record belonged to (decided 28 September, audit R149).** Points are added and the higher tier is kept, per programme — a single points number cannot say which programme it belongs to.\n","items":{"type":"object","required":["programmeId","pointsAdded","resultingPoints"],"properties":{"programmeId":{"type":"string","format":"uuid"},"pointsAdded":{"type":"integer","description":"The absorbed record's balance in this programme, added to the survivor's."},"resultingPoints":{"type":"integer"},"tierKept":{"type":"string","nullable":true,"description":"The higher of the two records' tiers in this programme."}}}},"consentOutcome":{"type":"array","description":"Per purpose, the resulting position. Where the two profiles disagreed, the more restrictive position won.\n","items":{"type":"object","properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"result":{"$ref":"#/components/schemas/ConsentDecision"},"wasRestricted":{"type":"boolean"}}}}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RecordConsentRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["purpose","decision","noticeVersion","source","recordedAt"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"decision":{"$ref":"#/components/schemas/ConsentDecision"},"channels":{"type":"array","description":"Omit to apply to every channel the purpose covers.","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string"},"source":{"$ref":"#/components/schemas/ConsentSource"},"recordedAt":{"type":"string","format":"date-time"}}},
"Segment": {"x-ticvai-persistence":"marketing.segment + marketing.segment_criterion","allOf":[{"$ref":"#/components/schemas/CreateSegmentRequest"},{"type":"object","required":["id","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"lastEvaluatedSize":{"type":"integer","nullable":true},"lastEvaluatedAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"}}}]}
}
```
