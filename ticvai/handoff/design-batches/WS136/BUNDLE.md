# WS136 — Marketing CRM Configuration Reference v1.0 board 2

**10 screens · 23 operations · 26 schemas · 8 permissions**

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
  `AUDIT_VIEW, GUEST_MANAGE, GUEST_VIEW, GUEST_VIEW_PII, MARKETING_MANAGE, MARKETING_VIEW, TENANT_CONFIGURE, TENANT_VIEW`. A control nobody can use must say so,
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
| `BO-744` | Data Governance Center | B–D | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-745` | Identity Resolution Rules | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-746` | Duplicate Review & Merge | B–D | 0 | 0 | 6 | 0 | 4 | 2 | — | notStarted (—) |
| `BO-747` | Consent Policy Configuration | B–D | 0 | 0 | 6 | 1 | 1 | 4 | — | notStarted (—) |
| `BO-748` | Consent Capture & Versions | B–D | 0 | 0 | 6 | 10 | 0 | 4 | — | notStarted (—) |
| `BO-749` | Guest Preference Center | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-750` | Data Subject Requests | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-751` | Retention & Anonymization | B–D | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `BO-752` | Privacy & AI Governance | B–D | 0 | 0 | 6 | 0 | 0 | 4 | — | notStarted (—) |
| `BO-753` | Compliance Audit Dashboard | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-744, BO-745, BO-746, BO-747, BO-748, BO-749, BO-750, BO-751, BO-752, BO-753 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-744` Data Governance Center

**Provide a consolidated view of customer-data quality, consent and privacy operations. Show duplicate profiles, pending merges, consent coverage, expiring consent, data-subject requests, retention actions and incidents. Filter by tenant, brand, venue, region, jurisdiction, data category, severity and owner. Surface overdue work, legal deadlines and high-risk exceptions with drill-down to the governing record. Provide trend analysis and controlled exports for privacy, legal, security and audit teams. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/data-governance-center-bo-744` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listPrivacyCompliance` ?from |
| To | date and time picker | — | — | `listPrivacyCompliance` ?to |
| Brand | picker: choose a brand | — | — | `listPrivacyCompliance` ?brandId |
| Country | text field | — | pattern `^[A-Z]{2}$` | `listPrivacyCompliance` ?country |
| Channel | select | — | Guest app · Website · Kiosk · POS · Call centre · Import · Agent recorded · Cookie banner · Checkout | `listPrivacyCompliance` ?channel |
| Consent purpose | select | — | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | `listPrivacyCompliance` ?consentPurpose |
| Segment | picker: choose a segment | — | — | `listPrivacyCompliance` ?segmentId |
| Product | picker: choose a product | — | — | `listPrivacyCompliance` ?productId |
| Policy version | text field | — | — | `listPrivacyCompliance` ?policyVersion |
| Language | text field | — | — | `listPrivacyCompliance` ?language |
| Band | segmented control | — | Match · Possible match | `listDuplicateCandidates` ?band |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listPrivacyCompliance` (onLoad, Data quality and consent coverage); `listDuplicateCandidates` (onLoad, Pending merges)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-745` Identity Resolution Rules: *Identity Resolution Rules*
- → `BO-746` Duplicate Review & Merge: *Duplicate Review & Merge*
- → `BO-747` Consent Policy Configuration: *Consent Policy Configuration*
- → `BO-748` Consent Capture & Versions: *Consent Capture & Versions*
- → `BO-749` Guest Preference Center: *Guest Preference Center*
- → `BO-750` Data Subject Requests: *Data Subject Requests*
- → `BO-751` Retention & Anonymization: *Retention & Anonymization*
- → `BO-752` Privacy & AI Governance: *Privacy & AI Governance*
- → `BO-753` Compliance Audit Dashboard: *Compliance Audit Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The data governance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the data governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No data governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the data governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listPrivacyCompliance` → `GUEST_VIEW` (read) · staff
- `listDuplicateCandidates` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.63 | Reporting and Analytics Reports should include: Consent acceptance rate. Rejection rate. Preference selections by category. Geographic consent statistics. Compliance audit reports. | Ticketing Sales | CONTRACTED | `listPrivacyCompliance` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-744` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-744`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 2
- Flow F245 *Marketing CRM Configuration Reference v1.0 board 2: Data Governance Center*, step 1: Opens Data Governance Center → Provide a consolidated view of customer-data quality, consent and privacy operations. Show duplicate profiles, pending merges, consent coverage, expiring consent, data-subject requests, retention …
- Flow F245 *Marketing CRM Configuration Reference v1.0 board 2: Data Governance Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F245 *Marketing CRM Configuration Reference v1.0 board 2: Data Governance Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F245 *Marketing CRM Configuration Reference v1.0 board 2: Data Governance Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F245 *Marketing CRM Configuration Reference v1.0 board 2: Data Governance Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F245 *Marketing CRM Configuration Reference v1.0 board 2: Data Governance Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F245 *Marketing CRM Configuration Reference v1.0 board 2: Data Governance Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F245 *Marketing CRM Configuration Reference v1.0 board 2: Data Governance Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F245 branch at step 1 (expected): when Nothing has been set up on Data Governance Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F245 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-744?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-745`, `BO-746`, `BO-747`, `BO-748`, `BO-749`, `BO-750`, `BO-751`, `BO-752`, `BO-753`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-745` Identity Resolution Rules

**Configure how potential duplicates are detected and a master identity is selected. Build weighted exact, normalized and fuzzy matching rules for email, phone, name, date of birth, membership, loyalty, passport and external IDs. Define match, possible-match and no-match thresholds, source priority, survivorship and field- level confidence. Support jurisdictional restrictions, excluded sources, false-positive handling and rule simulation before activation. Version, approve and audit rules and record the rule/version used for every automated decision. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/identity-resolution-rules-bo-745` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getIdentityResolutionRules` (onLoad, Matching rules)

**Where the user goes next**

- → `BO-744` Data Governance Center: *Back to Data Governance Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The identity resolution rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the identity resolution rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No identity resolution rules yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the identity resolution rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getIdentityResolutionRules` → `GUEST_VIEW` (read) · staff
- `setIdentityResolutionRules` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Duplicate review & merge: matching rules (fuzzy name similarity, exact mobile, exact e-mail) flag likely duplicates, as on the sample screen (500 profiles, ~100 matched by mobile number). *(client request · MoM 20 Aug 2026, 4.2 Duplicate Detection, Identity Resolution & Merge Rules · DI-376)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-745` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-745`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 2
- Flow F245 *Marketing CRM Configuration Reference v1.0 board 2: Data Governance Center*, step 2: Works in Identity Resolution Rules → Configure how potential duplicates are detected and a master identity is selected. Build weighted exact, normalized and fuzzy matching rules for email, phone, name, date of birth, membership …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-745?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-744`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-746` Duplicate Review & Merge

**Allow trained users to review, merge, split or reject suspected duplicate profiles. Compare records side by side, highlight conflicts and display recommended master values with confidence and source provenance. Configuration Scope of Work / Version 1.0 11 Preview linked tickets, bookings, memberships, loyalty, wallet, cases, consents and documents before committing. Preserve all transaction history, identifiers, relationships and audit evidence and prevent unsafe automatic merges. Require reason codes and approval for high-risk merges and support controlled split/recovery where permitted. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `MARKETING_MANAGE`, `MARKETING_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `candidateId` (navigation) |
| Route | `/engagement-support/duplicate-review-merge-bo-746` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Band | segmented control | — | Match · Possible match | `listDuplicateCandidates` ?band |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows. **Only unverified matches arrive here** (decided 28 September, audit R120 (b)): a verified contact match attaches the order to the guest automatically at checkout, so this queue holds the matches no guest has proved.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getGuestMatchPolicy` (onLoad, How returning guests are recognised); `listDuplicateCandidates` (onLoad, Side by side)

**Where the user goes next**

- → `BO-744` Data Governance Center: *Back to Data Governance Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The duplicate review merge list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the duplicate review merge untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No duplicate review merge yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the duplicate review merge are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A record in `mergeSubjectIds` is already merged (`alreadyMerged`), or `keepSubjectId` is among them (`sameProfile`) (MergeRefusedProblem) |

#### Permissions

- `getGuestMatchPolicy` → `MARKETING_VIEW` (read) · staff
- `setGuestMatchPolicy` → `MARKETING_MANAGE` (configure) · staff
- `listDuplicateCandidates` → `GUEST_MANAGE` (configure) · staff
- `decideDuplicateCandidate` → `GUEST_MANAGE` (configure) · staff
- `mergeGuests` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Repeat guest checkouts with the same email (or phone) consolidate into one profile automatically; a manual merge-customer-profile function remains for edge cases (e.g. slightly different name spelling under the same email). Allam cited a system where 10 transactions created 10 profiles. *(agreed · MoM 18 Sep 2026, 4.8 Guest Checkout & Profile Deduplication — Extended Discussion · DI-941)*
- Decision: profiles are never merged automatically. Likely duplicates are notified to the customer (push or e-mail) and merge only on the customer's confirmation; an admin review queue tracks flagged duplicates independently of the customer's response. *(agreed · MoM 20 Aug 2026, 4.2 Duplicate Detection; 5. Key Decisions · DI-377)*
- Duplicate review & merge: matching rules (fuzzy name similarity, exact mobile, exact e-mail) flag likely duplicates, as on the sample screen (500 profiles, ~100 matched by mobile number). *(client request · MoM 20 Aug 2026, 4.2 Duplicate Detection, Identity Resolution & Merge Rules · DI-376)*
- Duplicate-profile detection and merge (common because of name transliteration variants) merging two profiles with their combined transaction history; account activate/deactivate. *(agreed · MoM 7 Aug 2026, 19. Maintenance Tools · DI-176)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A69** Implement duplicate-account detection and profile-merge functionality (consolidating two profiles into one, carrying over the combined transaction history) *(Softlabs Backend Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Aug 2026 · workshop tracker · keyword 'duplicate-account')*
- **A90** Implement consent-gated duplicate merge (fuzzy name / exact mobile / exact email matching, customer confirmation required, admin review queue, login-of-record rule) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'duplicate merge')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-746` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-746`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 2
- Flow F245 *Marketing CRM Configuration Reference v1.0 board 2: Data Governance Center*, step 4: Works in Duplicate Review & Merge → Allow trained users to review, merge, split or reject suspected duplicate profiles. Compare records side by side, highlight conflicts and display recommended master values with confidence and source …
- ADR-0045 *Every order carries a proven contact, and the gate is the checkout page* (`docs/adr/0045-every-order-carries-a-proven-contact.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-746?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-744`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-747` Consent Policy Configuration

**Define the legal and operational rules governing consent. Configure consent purposes, marketing categories, processing purposes and channel-specific permission for email, SMS, WhatsApp, push and direct mail. Define jurisdiction, lawful basis, age and guardian requirements, capture channels, expiry, renewal and hard/soft enforcement. Map policies to brands, venues, products, audiences and processing activities with precedence and conflict handling. Require legal review, effective dates, version control and immutable policy-change history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/consent-policy-configuration-bo-747` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save consent purposes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listConsentPurposes` (onLoad, Purposes and lawful bases)

**Where the user goes next**

- → `BO-744` Data Governance Center: *Back to Data Governance Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The consent policy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the consent policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No consent policy yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the consent policy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listConsentPurposes` → `GUEST_VIEW` (read) · staff, guest
- `setConsentPurposes` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.13.7 | Consent Expiration Management | Marketing & CRM | CONTRACTED | `setConsentPurposes` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Consent policy governs marketing/newsletter/survey communications; customers who do not opt in must not receive promotional communications. *(client request · MoM 20 Aug 2026, 4.3 Consent, Data Privacy & Retention · DI-378)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-747` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-747`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 2
- Flow F245 *Marketing CRM Configuration Reference v1.0 board 2: Data Governance Center*, step 6: Works in Consent Policy Configuration → Define the legal and operational rules governing consent. Configure consent purposes, marketing categories, processing purposes and channel-specific permission for email, SMS, WhatsApp, push and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-747?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save consent purposes, Cancel.
- [ ] Every transition is wired: `BO-744`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-748` Consent Capture & Versions

**Manage the content and lifecycle of guest consent statements. Create multilingual consent versions with acknowledgement text, links, effective dates and supported channels. Capture who consented, what they saw, when, where, by which channel and under which policy version. Support withdrawal, expiry, re-consent and guardian authorization without overwriting prior evidence. Publish only approved versions and make the active statement available consistently to all touchpoints. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `subjectId` (navigation) |
| Route | `/engagement-support/consent-capture-versions-bo-748` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Form | picker: choose a form | — | — | `listVersioningEffectiveDate` ?formId |
| Compare with | number field | — | min 1 | `listVersioningEffectiveDate` ?compareWith |
| Status | radio group | — | Draft · Published · Superseded · Retired | `listVersioningEffectiveDate` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listVersioningEffectiveDate` (onLoad, Consent versions)

**Where the user goes next**

- → `BO-744` Data Governance Center: *Back to Data Governance Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The consent capture versions list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the consent capture versions untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No consent capture versions yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the consent capture versions are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Notice version unknown, or the purpose is not configured; 400 Validation failed |

#### Permissions

- `listVersioningEffectiveDate` → `GUEST_VIEW` (read) · staff
- `recordConsent` → no permission · guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.3.9 | The system should allow the guest to explicitly opt in to receive any information from venue or its partners. | F&B & Guest Management | CONTRACTED | `recordConsent` |
| 5.3.18 | Maintain auditable consent records for Email, SMS, WhatsApp, Push Notifications, Marketing Communications, Privacy Policies, Terms & Conditions, and GDPR compliance. | F&B & Guest Management | CONTRACTED | `recordConsent` |
| 7.3.9 | Store and manage customer consent preferences for email, SMS, WhatsApp, push notifications and third-party marketing. Record consent status, source, timestamp, IP address and revocation history. … | F&B POS | CONTRACTED | `recordConsent` |
| 22.2.18 | Consent Management | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.4.5 | Subscription Management | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.13.1 | Consent Management Framework | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.13.2 | Marketing Consent Management | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.13.3 | Channel-Specific Consent | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.13.4 | Consent Capture Workflows | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.13.9 | Data Processing Consent | Marketing & CRM | CONTRACTED | `recordConsent` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-748` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-748`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 2
- Flow F245 *Marketing CRM Configuration Reference v1.0 board 2: Data Governance Center*, step 8: Works in Consent Capture & Versions → Manage the content and lifecycle of guest consent statements. Create multilingual consent versions with acknowledgement text, links, effective dates and supported channels. Capture who consented …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-748?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-744`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-749` Guest Preference Center

**Configure the guest-facing center for communication choices and privacy preferences. Expose subscription categories, topics, preferred channels, contact frequency, quiet hours and global or brand-level opt-outs. Apply identity verification and clearly distinguish transactional messages from optional marketing. Synchronize changes in real time to campaigns, journeys, chatbot, newsletters and notification delivery. Store an auditable receipt for every preference change and provide accessible, multilingual presentation. Configuration Scope of Work / Version 1.0 12 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

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
| Route | `/engagement-support/guest-preference-center-bo-749` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-744` Data Governance Center: *Back to Data Governance Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest preference list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest preference untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest preference yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the guest preference are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A marketing category that defaults to on, or names no consent purpose. |

#### Permissions

- `setCommunicationPreferenceMarketing` → `GUEST_MANAGE` (configure) · staff
- `getGuestConsents` → `GUEST_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-749` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-749`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 2
- Flow F245 *Marketing CRM Configuration Reference v1.0 board 2: Data Governance Center*, step 10: Works in Guest Preference Center → Configure the guest-facing center for communication choices and privacy preferences. Expose subscription categories, topics, preferred channels, contact frequency, quiet hours and global or …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-749?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-744`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-750` Data Subject Requests

**Manage privacy requests from intake through verified completion. Support access, rectification, portability, erasure, restriction and objection request types. Verify requester identity, calculate statutory deadlines, assign owners, gather approvals and track dependencies. Search connected systems, assemble export packages and document exclusions, legal holds or denied actions. Record communications, evidence, completion status and SLA performance in an immutable case history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_VIEW`, `GUEST_VIEW_PII` (1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/data-subject-requests-bo-750` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | segmented control | — | Submitted · In progress · Completed | `listDataSubjectCustomer` ?status |
| Request type | text field | — | max length 60 | `listDataSubjectCustomer` ?requestType |
| Subject | picker: choose a subject | — | — | `listDataSubjectCustomer` ?subjectId |
| Jurisdiction | text field | — | pattern `^[A-Z]{2}$` | `listDataSubjectCustomer` ?jurisdiction |
| Sla state | radio group | — | On track · At risk · Overdue · Escalated · No deadline | `listDataSubjectCustomer` ?slaState |
| Owner principal | picker: choose an owner principal | — | — | `listDataSubjectCustomer` ?ownerPrincipalId |
| From | date and time picker | — | — | `listDataSubjectCustomer` ?from |
| To | date and time picker | — | — | `listDataSubjectCustomer` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save data discovery access (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listDataSubjectCustomer` (onLoad, Privacy requests)

**Where the user goes next**

- → `BO-744` Data Governance Center: *Back to Data Governance Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The data subject requests list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the data subject requests untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No data subject requests yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the data subject requests are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 The request is not an access, export or correction request, is not `inProgress`, its identity is not verified, or the approver is the principal who generated … |

#### Permissions

- `listDataSubjectCustomer` → `GUEST_VIEW` (read) · staff
- `setDataDiscoveryAccess` → `GUEST_VIEW_PII` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Data-subject requests (access, correction, deletion) are tracked with status submitted → in progress → completed. *(client request · MoM 20 Aug 2026, 4.3 Consent, Data Privacy & Retention · DI-379)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-750` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-750`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 2
- Flow F245 *Marketing CRM Configuration Reference v1.0 board 2: Data Governance Center*, step 12: Works in Data Subject Requests → Manage privacy requests from intake through verified completion. Support access, rectification, portability, erasure, restriction and objection request types. Verify requester identity, calculate …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-750?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save data discovery access, Cancel.
- [ ] Every transition is wired: `BO-744`.
- [ ] Every gated control is gated: `GUEST_VIEW`, `GUEST_VIEW_PII`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-751` Retention & Anonymization

**Configure how long customer data is retained and what happens at expiry. Define policies by data category, jurisdiction, purpose, guest status, transaction type and source system. Support archive, anonymize, pseudonymize and delete actions, legal holds, fraud exceptions and scheduled execution. Preview affected records, dependencies and downstream consequences before high-impact actions. Produce completion evidence and reconcile results across analytics, search, documents, backups and integrations. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `TENANT_CONFIGURE`, `TENANT_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `dataClass` (navigation) |
| Route | `/engagement-support/retention-anonymization-bo-751` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Data class | select | — | Guest profile · Payment record · Financial record · Audit record · Approval record · Compliance inspection · Face tag biometric · Face pass biometric · AI prompts · AI conversations · AI decision records · AI metadata index | `listDataRetentionSettings` ?dataClass |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save data retention policy (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listDataRetentionSettings` (onLoad, Retention period per data class)

**Where the user goes next**

- → `BO-744` Data Governance Center: *Back to Data Governance Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The retention anonymization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the retention anonymization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No retention anonymization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the retention anonymization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A period below the class's legal minimum or above its legal maximum, a period sent for `aiMetadataIndex`, or a `followsDataClass` chain that loops; 422 `retainMonths` longer than the tenant's effective `guestProfile` retention period (tenancy `setDataRetentionSetting`); a rule here may only shorten it |

#### Permissions

- `setDataRetentionPolicy` → `GUEST_MANAGE` (configure) · staff
- `runDataRetention` → `GUEST_MANAGE` (configure) · staff
- `listDataRetentionSettings` → `TENANT_VIEW` (read) · staff
- `setDataRetentionSetting` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.13.15 | Data Retention Policies | Marketing & CRM | CONTRACTED | `setDataRetentionPolicy` |
| 4.3.4 | The system should support payment servers that provide the following functions: - Record transactions below the authorization threshold - Procure authorizations over the automatic authorization … | Bundles and Promotions | CONTRACTED | `setDataRetentionSetting` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: data retention/archival (e.g. 3–5 years live before archival) and chat/case conversation retention (e.g. default one month, extendable) are configurable per tenant/venue at setup, with system defaults admins can override. *(agreed · MoM 20 Aug 2026, 4.3 Consent; 4.8 AI Chat Box; 5. Key Decisions · DI-380)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-751` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-751`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 2
- Flow F245 *Marketing CRM Configuration Reference v1.0 board 2: Data Governance Center*, step 14: Works in Retention & Anonymization → Configure how long customer data is retained and what happens at expiry. Define policies by data category, jurisdiction, purpose, guest status, transaction type and source system. Support archive …
- ADR-0047 *How long data is kept, and where it goes next* (`docs/adr/0047-how-long-data-is-kept-and-where-it-goes-next.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-751?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save data retention policy, Cancel.
- [ ] Every transition is wired: `BO-744`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `TENANT_CONFIGURE`, `TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-752` Privacy & AI Governance

**Control privacy incidents and approved uses of customer data by AI. Track incident type, severity, affected data, containment, owner, notification obligations, mitigation and closure. Maintain approved models/use cases, prohibited data, risk level, purpose limitation and human- review requirements. Configure prompt/output retention, masking, vendor/model access and escalation for sensitive or high-impact decisions. Link controls to AI recommendations across CRM and preserve model, policy, reviewer and outcome evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/privacy-ai-governance-bo-752` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Brand | picker: choose a brand | — | — | `listPrivacy` ?brandId |
| Country | text field | — | pattern `^[A-Z]{2}$` | `listPrivacy` ?country |
| Request type | text field | — | max length 60 | `listPrivacy` ?requestType |
| Consent purpose | select | — | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | `listPrivacy` ?consentPurpose |
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listPrivacy` ?channel |
| Owner principal | picker: choose an owner principal | — | — | `listPrivacy` ?ownerPrincipalId |
| From | date and time picker | — | — | `listPrivacy` ?from |
| To | date and time picker | — | — | `listPrivacy` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listPrivacy` (onLoad, Approved AI uses and limits)

**Where the user goes next**

- → `BO-744` Data Governance Center: *Back to Data Governance Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The privacy governance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the privacy governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No privacy governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the privacy governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `recordPrivacyIncident` → `GUEST_MANAGE` (configure) · staff
- `listPrivacy` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-752` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-752`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 2
- Flow F245 *Marketing CRM Configuration Reference v1.0 board 2: Data Governance Center*, step 16: Works in Privacy & AI Governance → Control privacy incidents and approved uses of customer data by AI. Track incident type, severity, affected data, containment, owner, notification obligations, mitigation and closure. Maintain …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-752?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-744`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-753` Compliance Audit Dashboard

**Demonstrate consent and privacy compliance through measurable evidence. Configuration Scope of Work / Version 1.0 13 Report consent coverage and expiry, request volumes and SLA, retention completion, anonymization, deletion and incident trends. Drill down by jurisdiction, business unit, channel, policy, owner and data category. Provide controlled evidence packages, exception logs and audit exports with source references and timestamps. Restrict compliance information appropriately and record every view, export and administrative action. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work / Version 1.0 14 Board 3 - Audience Segmentation & Personalization Figure 3. High-definition configuration board with all 10 screens. Configuration Scope of Work / Version 1.0 15**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AUDIT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/compliance-audit-dashboard-bo-753` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Action | select | — | Consent granted · Consent withdrawn · Preference changed · Policy accepted · Privacy request created · Identity verified · Data export generated · Correction requested · Deletion approved · Anonymisation executed · Retention action · Legal hold … | `listPrivacyEvidenceCompliance` ?action |
| Report | select | — | Consent status · Consent withdrawal · Marketing permission · Privacy request sla · Deletion anonymisation · Retention · Policy acceptance · Minor guardian privacy · Cookie tracking compliance · Biometric privacy · Exception | `listPrivacyEvidenceCompliance` ?report |
| Subject | picker: choose a subject | — | — | `listPrivacyEvidenceCompliance` ?subjectId |
| Request | picker: choose a request | — | — | `listPrivacyEvidenceCompliance` ?requestId |
| Actor principal | picker: choose an actor principal | — | — | `listPrivacyEvidenceCompliance` ?actorPrincipalId |
| From | date and time picker | — | — | `listPrivacyEvidenceCompliance` ?from |
| To | date and time picker | — | — | `listPrivacyEvidenceCompliance` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listPrivacyEvidenceCompliance` (onLoad, Evidence for an audit)

**Where the user goes next**

- → `BO-744` Data Governance Center: *Back to Data Governance Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The compliance audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the compliance audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No compliance audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the compliance audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPrivacyEvidenceCompliance` → `AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-753` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS71 Marketing CRM Configuration Reference v1.0 Board 2.dc.html#bo-753`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 2
- Flow F245 *Marketing CRM Configuration Reference v1.0 board 2: Data Governance Center*, step 18: Works in Compliance Audit Dashboard → Demonstrate consent and privacy compliance through measurable evidence. Configuration Scope of Work / Version 1.0 13 Report consent coverage and expiry, request volumes and SLA, retention completion …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-753?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-744`.
- [ ] Every gated control is gated: `AUDIT_VIEW`.
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

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"decideDuplicateCandidate": {"method":"POST","path":"/duplicate-candidates/{candidateId}/decide","contract":"marketing-crm","summary":"Merge, reject or split","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DuplicateCandidate"},
"getGuestConsents": {"method":"GET","path":"/guests/{subjectId}/consents","contract":"marketing-crm","summary":"Read a guest's consent state","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ConsentState"},
"getGuestMatchPolicy": {"method":"GET","path":"/guest-match-policy","contract":"marketing-crm","summary":"How returning guests are recognised at checkout","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuestMatchPolicy"},
"getIdentityResolutionRules": {"method":"GET","path":"/identity-resolution-rules","contract":"marketing-crm","summary":"How duplicates are detected and a master is chosen","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"IdentityResolutionRules"},
"listConsentPurposes": {"method":"GET","path":"/consent-purposes","contract":"marketing-crm","summary":"Configured consent purposes","permission":"GUEST_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDataRetentionSettings": {"method":"GET","path":"/data-retention-settings","contract":"tenancy","summary":"How long the tenant keeps each class of data","permission":"TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"dataClass","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDataSubjectCustomer": {"method":"GET","path":"/data-subject-customer","contract":"marketing-crm","summary":"Data Subject / Customer Privacy Request Management","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":false},{"name":"requestType","in":"query","required":false},{"name":"subjectId","in":"query","required":false},{"name":"jurisdiction","in":"query","required":false},{"name":"slaState","in":"query","required":false},{"name":"ownerPrincipalId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDuplicateCandidates": {"method":"GET","path":"/duplicate-candidates","contract":"marketing-crm","summary":"Suspected duplicates awaiting a decision","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null},{"name":"band","in":"query","required":null}],"requestBody":null,"responds":"Page"},
"listPrivacy": {"method":"GET","path":"/privacy","contract":"marketing-crm","summary":"Privacy Operations Command Center","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"brandId","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"requestType","in":"query","required":false},{"name":"consentPurpose","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"ownerPrincipalId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false}],"requestBody":null,"responds":"PrivacyOperationsCommandCenterView"},
"listPrivacyCompliance": {"method":"GET","path":"/privacy-compliance","contract":"marketing-crm","summary":"Privacy Analytics & AI Compliance Intelligence","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"brandId","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"consentPurpose","in":"query","required":false},{"name":"segmentId","in":"query","required":false},{"name":"productId","in":"query","required":false},{"name":"policyVersion","in":"query","required":false},{"name":"language","in":"query","required":false}],"requestBody":null,"responds":"PrivacyAnalyticsAiComplianceIntelligenceView"},
"listPrivacyEvidenceCompliance": {"method":"GET","path":"/privacy-evidence-compliance","contract":"marketing-crm","summary":"Privacy Audit, Evidence & Compliance Reporting","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"action","in":"query","required":false},{"name":"report","in":"query","required":false},{"name":"subjectId","in":"query","required":false},{"name":"requestId","in":"query","required":false},{"name":"actorPrincipalId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVersioningEffectiveDate": {"method":"GET","path":"/versioning-effective-date","contract":"marketing-crm","summary":"Versioning, Effective Dates & Legal Change Control","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"formId","in":"query","required":false},{"name":"compareWith","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"mergeGuests": {"method":"POST","path":"/guests/merge","contract":"marketing-crm","summary":"Two records, one person","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MergeResult"},
"recordConsent": {"method":"POST","path":"/guests/{subjectId}/consents","contract":"marketing-crm","summary":"Record a consent decision","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RecordConsentRequest","responds":"ConsentState"},
"recordPrivacyIncident": {"method":"POST","path":"/privacy-incidents","contract":"marketing-crm","summary":"Log a personal-data breach and start the clock","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PrivacyIncident","responds":"PrivacyIncident"},
"runDataRetention": {"method":"POST","path":"/retention-runs","contract":"marketing-crm","summary":"Preview or execute a retention pass","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RetentionRunResult"},
"setCommunicationPreferenceMarketing": {"method":"PUT","path":"/communication-preference-marketing","contract":"marketing-crm","summary":"Communication Preference & Marketing Permission Configuration","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CommunicationPreferenceMarketingPermissionConfiguratInput","responds":"CommunicationPreferenceMarketingPermissionConfiguratView"},
"setConsentPurposes": {"method":"PUT","path":"/consent-purposes","contract":"marketing-crm","summary":"Configure consent purposes","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConsentPurposeConfig"},
"setDataDiscoveryAccess": {"method":"PUT","path":"/data-discovery-access","contract":"marketing-crm","summary":"Data Discovery, Access, Export & Correction Workspace","permission":"GUEST_VIEW_PII","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DataDiscoveryAccessExportCorrectionWorkspaceInput","responds":"DataDiscoveryAccessExportCorrectionWorkspaceView"},
"setDataRetentionPolicy": {"method":"PUT","path":"/retention-policies","contract":"marketing-crm","summary":"How long guest data is kept, and what happens at expiry","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DataRetentionPolicy","responds":"DataRetentionPolicy"},
"setDataRetentionSetting": {"method":"PUT","path":"/data-retention-settings/{dataClass}","contract":"tenancy","summary":"Set how long the tenant keeps one class of data","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TenantDataRetentionSetting","responds":"TenantDataRetentionSetting"},
"setGuestMatchPolicy": {"method":"PUT","path":"/guest-match-policy","contract":"marketing-crm","summary":"Set how returning guests are recognised","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GuestMatchPolicy","responds":"GuestMatchPolicy"},
"setIdentityResolutionRules": {"method":"PUT","path":"/identity-resolution-rules","contract":"marketing-crm","summary":"Matching weights, thresholds and survivorship","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"IdentityResolutionRules","responds":"IdentityResolutionRules"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CommunicationPreferenceMarketingPermissionConfiguratInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"One communication preference category, as the privacy administrator defines it (pack 17.1.4 Configuration).","required":["categoryCode","name","classification","availableChannels","defaultBehavior","customerEditable"],"properties":{"categoryCode":{"type":"string","maxLength":60,"description":"The natural key, e.g. `orderConfirmation`, `promotions`, `birthdayCampaigns`."},"name":{"type":"string","maxLength":150},"description":{"type":"string","maxLength":1000,"nullable":true},"classification":{"type":"string","enum":["transactional","marketing"],"description":"The pack's critical principle. Decides whether consent is needed at all."},"communicationType":{"type":"string","enum":["orderConfirmation","ticketDelivery","paymentInformation","eventChanges","securityMessages","promotions","newEvents","membershipOffers","loyaltyOffers","birthdayCampaigns","partnerOffers","surveys","other"]},"consentPurpose":{"allOf":[{"$ref":"#/components/schemas/ConsentPurpose"}],"nullable":true,"description":"Required for `marketing`. The purpose whose consent a send checks first."},"availableChannels":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/MessageChannel"}},"applicableBrandIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Empty means every brand of the tenant."},"applicableCountries":{"type":"array","items":{"type":"string","pattern":"^[A-Z]{2}$"},"description":"Empty means every country."},"customerEditable":{"type":"boolean","description":"Whether the guest may change it in the preference centre."},"defaultBehavior":{"type":"string","enum":["on","off"],"description":"`off` for every `marketing` category (opt-in)."},"reconfirmAfterMonths":{"type":"integer","minimum":1,"nullable":true,"description":"Ask the guest again after this long; null never."},"status":{"type":"string","enum":["active","retired"],"default":"active"}}},
"CommunicationPreferenceMarketingPermissionConfiguratView": {"x-ticvai-persistence":"marketing.communication_preference_type","description":"A stored communication preference category.","allOf":[{"$ref":"#/components/schemas/CommunicationPreferenceMarketingPermissionConfiguratInput"},{"type":"object","required":["id","version"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"version":{"type":"integer","minimum":1,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}}]},
"ConsentDecision": {"type":"string","enum":["granted","withdrawn","notAsked"]},
"ConsentPurpose": {"type":"string","enum":["marketing","personalisation","profiling","thirdPartySharing","aiProcessing","transactional"]},
"ConsentPurposeConfig": {"x-ticvai-persistence":"marketing.consent_purpose + marketing.consent_purpose_channel","type":"object","required":["purpose","channels","noticeVersion","isRequiredForService"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"displayName":{"type":"string"},"description":{"type":"string"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string","description":"Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured.\n"},"isRequiredForService":{"type":"boolean","description":"True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently.\n"},"expiresAfterMonths":{"type":"integer","nullable":true}}},
"ConsentSource": {"type":"string","enum":["guestApp","website","kiosk","pos","callCentre","import","agentRecorded","cookieBanner","checkout"],"description":"`checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents`, bound to the order and the verified contact. `cookieBanner` (29 September, build; BL-073 §4b): a decision made on the cookie banner or preference centre and moved onto the guest by `claimDeviceConsent`. Kept apart from `website`, a form submission, because the audit trail (2.6.56) has to tell the two apart."},
"ConsentState": {"x-ticvai-persistence":"none — projection over consent_record","type":"object","required":["subjectId","purposes"],"properties":{"subjectId":{"type":"string","format":"uuid"},"purposes":{"type":"array","items":{"type":"object","required":["purpose","decision","requiresRenewal"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"decision":{"$ref":"#/components/schemas/ConsentDecision"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string","nullable":true},"requiresRenewal":{"type":"boolean","description":"True where the notice has been superseded since consent was given."},"decidedAt":{"type":"string","format":"date-time","nullable":true}}}}}},
"DataDiscoveryAccessExportCorrectionWorkspaceInput": {"type":"object","x-ticvai-persistence":"marketing.privacy_export_package","description":"What a privacy user sends for one request (pack 17.2.5 Data Discovery, Export Package, Correction, Review).","required":["requestId"],"properties":{"requestId":{"type":"string","format":"uuid","description":"The privacy request (`setPrivacyRequest`); the natural key."},"identifiers":{"type":"array","description":"Extra identifiers to search by; the request's subject is always included.","items":{"type":"object","required":["type","value"],"properties":{"type":{"type":"string","enum":["customerId","email","mobile","membershipId","orderId","participantId","other"]},"value":{"type":"string","maxLength":200}}}},"sources":{"type":"array","description":"Sources to search; empty means all.","items":{"type":"string","enum":["customerProfile","orders","tickets","membership","loyalty","wallet","crm","marketing","paymentReferences","waiverRecords","resourceBookings","eventRegistrations","consentRecords","credentialReferences","connectedApplications"]}},"exportPackage":{"type":"object","nullable":true,"description":"Present to generate or progress the export package.","properties":{"includedSources":{"type":"array","items":{"type":"string","description":"A value of `sources`."}},"includedCategories":{"type":"array","items":{"type":"string","maxLength":80}},"exclusions":{"type":"array","items":{"type":"string","maxLength":200},"description":"Records withheld, each with a reason (e.g. another person's data, a legal hold)."},"sensitiveFieldHandling":{"type":"string","enum":["include","mask","exclude"],"default":"mask"},"format":{"type":"string","enum":["json","csv","pdf"],"default":"json"},"language":{"type":"string","description":"BCP 47 tag for the cover letter and field labels."},"passwordProtected":{"type":"boolean","default":true},"expiresAt":{"type":"string","format":"date-time"},"reviewAction":{"type":"string","nullable":true,"enum":["submitForReview","approve","reject","deliver"],"description":"Moves the package through generated -> privacyReview -> approved -> delivered."}}},"corrections":{"type":"array","description":"Correction requests to route to the system of record.","items":{"type":"object","required":["field","proposedValue"],"properties":{"field":{"type":"string","maxLength":100,"description":"e.g. `email`, `dateOfBirth`."},"proposedValue":{"type":"string","maxLength":500},"note":{"type":"string","maxLength":500,"nullable":true}}}}}},
"DataDiscoveryAccessExportCorrectionWorkspaceView": {"type":"object","x-ticvai-persistence":"marketing.privacy_export_package","description":"One request's discovery results, export package and routed corrections.","required":["requestId","results"],"properties":{"requestId":{"type":"string","format":"uuid"},"discoveredAt":{"type":"string","format":"date-time","readOnly":true},"results":{"type":"array","description":"Record counts per source; the records themselves go only into the export package.","items":{"type":"object","required":["source","recordCount"],"properties":{"source":{"type":"string","description":"A value of the input's `sources`."},"systemName":{"type":"string","nullable":true},"recordCount":{"type":"integer","minimum":0},"searchFailed":{"type":"boolean","default":false}}}},"exportPackage":{"type":"object","nullable":true,"readOnly":true,"properties":{"status":{"type":"string","enum":["generating","generated","privacyReview","approved","rejected","delivered","expired"]},"format":{"type":"string","enum":["json","csv","pdf"]},"generatedAt":{"type":"string","format":"date-time","nullable":true},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"deliveredAt":{"type":"string","format":"date-time","nullable":true},"expiresAt":{"type":"string","format":"date-time"},"assetId":{"type":"string","format":"uuid","nullable":true,"description":"The encrypted package in the asset store."},"dsarRequestId":{"type":"string","nullable":true,"description":"The cross-region fan-out that assembled it."}}},"corrections":{"type":"array","readOnly":true,"items":{"type":"object","required":["field","systemOfRecord","status"],"properties":{"field":{"type":"string"},"systemOfRecord":{"type":"string","description":"The owning contract/table, e.g. `pii.subject_contact`."},"operation":{"type":"string","nullable":true,"description":"The operation that performs it, e.g. `updateGuestProfile`."},"status":{"type":"string","enum":["routed","applied","rejected","manualActionRequired"]},"updatedAt":{"type":"string","format":"date-time"}}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"DataRetentionPolicy": {"type":"object","x-ticvai-persistence":"marketing.retention_policy","description":"Board 2.8. **The only routine operation that destroys data irrecoverably at scale.**","required":["code"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"dataCategory":{"type":"string"},"jurisdictions":{"type":"array","items":{"type":"string"}},"purposes":{"type":"array","items":{"type":"string"}},"guestStatus":{"type":"array","items":{"type":"string"}},"retainMonths":{"type":"integer","description":"At most the tenant's effective `guestProfile` period (tenancy `setDataRetentionSetting`, decided 29 September); a rule may only shorten it."},"action":{"type":"string","enum":["archive","anonymise","pseudonymise","delete"]},"legalHoldsRespected":{"type":"boolean","default":true},"fraudExceptionMonths":{"type":"integer","nullable":true},"approvalRequired":{"type":"boolean","default":true},"schedule":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"DataSubjectCustomerPrivacyRequestManagementView": {"type":"object","x-ticvai-persistence":"marketing.privacy_request","description":"One customer privacy request (pack 17.2.4 Case Information). The case layer over the cross-region `platform.dsar_request` fan-out, which it references when it raises one.","required":["subjectId","requestType","source","requesterRole","jurisdiction"],"properties":{"requestId":{"type":"string","format":"uuid","readOnly":true},"subjectId":{"type":"string","format":"uuid","description":"The person the request is about."},"requestType":{"type":"string","maxLength":60,"description":"A configured request type code (`setPrivacyRequestTypes`), e.g. `access`, `dataExport`, `correction`, `deletion`, `anonymisation`, `restriction`, `objection`, `consentWithdrawal`, `marketingOptOut`."},"source":{"type":"string","enum":["customerPortal","b2c","mobileApp","emailManual","customerService","pos","api"]},"requesterRole":{"type":"string","enum":["self","guardian","authorisedRepresentative"]},"requesterSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guardian or representative, when not `self`; verified like the subject."},"jurisdiction":{"type":"string","pattern":"^[A-Z]{2}$","description":"Selects the response period configured for this request type."},"submittedAt":{"type":"string","format":"date-time","readOnly":true},"dueAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"`submittedAt` plus the jurisdiction's configured response period; null when none is configured."},"deadlineConfigured":{"type":"boolean","readOnly":true},"daysRemaining":{"type":"integer","nullable":true,"readOnly":true,"description":"Negative once overdue; null without a deadline."},"atRisk":{"type":"boolean","readOnly":true,"description":"Inside the request type's configured warning window before `dueAt`."},"slaState":{"type":"string","readOnly":true,"enum":["onTrack","atRisk","overdue","escalated","noDeadline"]},"priority":{"type":"string","enum":["P1","P2","P3","P4"],"default":"P3"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"verificationMethod":{"type":"string","nullable":true,"enum":["accountLogin","otp","emailVerification","mobileVerification","idReview","manualVerification"],"description":"One of the methods the request type allows."},"verificationStatus":{"type":"string","enum":["notStarted","pending","verified","failed"],"default":"notStarted"},"status":{"type":"string","enum":["submitted","inProgress","completed"],"default":"submitted","description":"MoM 20 Aug lifecycle."},"stage":{"type":"string","maxLength":60,"nullable":true,"description":"The configured workflow step within `inProgress` (a stage code of the request type)."},"outcome":{"type":"string","nullable":true,"enum":["fulfilled","partiallyFulfilled","refused","withdrawnByRequester"],"description":"Required to complete. `refused` and `partiallyFulfilled` need `outcomeReason`."},"outcomeReason":{"type":"string","maxLength":1000,"nullable":true},"escalated":{"type":"boolean","default":false},"dsarRequestId":{"type":"string","nullable":true,"readOnly":true,"description":"The cross-region `DsarRequest.requestId`, when fulfilment fanned out."},"caseId":{"type":"string","format":"uuid","nullable":true,"description":"The customer-service case it came in through, if any."},"notes":{"type":"string","maxLength":4000,"nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"DuplicateCandidate": {"type":"object","x-ticvai-persistence":"marketing.duplicate_candidate","x-ticvai-retired-columns":["guest_ids"],"description":"Board 2.3. **Rejection is as valuable as merging**, or the same pair returns weekly.","properties":{"id":{"type":"string","format":"uuid"},"subjectIds":{"type":"array","description":"The profiles proposed as one person.","items":{"type":"string","format":"uuid"}},"score":{"type":"number"},"band":{"type":"string","enum":["match","possibleMatch"]},"matchedOn":{"type":"array","items":{"type":"string"}},"conflicts":{"type":"array","items":{"type":"object","properties":{"field":{"type":"string"},"values":{"type":"array","items":{"type":"string"}},"recommended":{"type":"string","nullable":true},"confidence":{"type":"number","nullable":true},"provenance":{"type":"string","nullable":true}}}},"linkedRecordCounts":{"type":"object","additionalProperties":{"type":"integer"},"description":"Tickets, bookings, memberships, loyalty, wallet, cases, consents, documents — **previewed before anything is committed**, because merging is not reversible in practice.\n"},"status":{"type":"string","enum":["pending","merged","rejected","split"]},"decidedBy":{"type":"string","format":"uuid","nullable":true},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"GuestMatchPolicy": {"type":"object","x-ticvai-persistence":"marketing.guest_match_policy","description":"How a guest checking out without an account is recognised. One per venue. **The rev 3 Config controls map here unchanged** (decided 29 September, rev 3 DG-1, no change): *Match returning guests by* is `matchBy`; *Guest checkout (code proof)* is the white-label FeatureToggle `guestCheckout`, off by default, with the code proved through `identity` and the match offered by `checkGuestCheckoutMatch` and `decideGuestCheckoutMatch`.\n","required":["matchBy"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"matchBy":{"type":"string","enum":["email","mobile","emailOrMobile"],"default":"email","description":"The key a returning guest is matched on. Design control: *Match returning guests by*."},"offerAtCheckout":{"type":"boolean","default":true,"description":"Whether a verified contact is matched at the payment step. On, a verified match attaches the order automatically (audit R120 (b)). Off means staff merge later only, and `checkGuestCheckoutMatch` skips the lookup entirely (audit R149)."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"IdentityResolutionRules": {"type":"object","x-ticvai-persistence":"marketing.identity_rules","description":"Board 2.2. **Three thresholds, and the middle band is the point.**","properties":{"matchers":{"type":"array","items":{"type":"object","properties":{"field":{"type":"string","enum":["email","phone","name","dateOfBirth","membershipNumber","loyaltyNumber","passportNumber","externalId","address"]},"comparison":{"type":"string","enum":["exact","normalised","fuzzy","phonetic"]},"weight":{"type":"number"},"required":{"type":"boolean","default":false}}}},"matchThreshold":{"type":"number"},"possibleMatchThreshold":{"type":"number"},"survivorship":{"type":"array","items":{"type":"object","properties":{"field":{"type":"string"},"rule":{"type":"string","enum":["mostRecent","oldest","highestSourcePriority","mostComplete","verifiedFirst","manual"]}}},"description":"**Per field, not per record.** The newer record has the better phone number and the older one has the loyalty history.\n"},"excludedSources":{"type":"array","items":{"type":"string"}},"jurisdictionRestrictions":{"type":"array","items":{"type":"string"}},"autoMergeAllowed":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"MergeResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["survivingSubjectId","absorbedSubjectId","transferred"],"properties":{"survivingSubjectId":{"type":"string","format":"uuid"},"absorbedSubjectId":{"type":"string","format":"uuid"},"transferred":{"type":"object","properties":{"orders":{"type":"integer"},"cases":{"type":"integer"},"loyaltyPoints":{"type":"integer","description":"The total points moved across every programme. The per-programme outcome is `loyaltyProgrammes`."}}},"loyaltyProgrammes":{"type":"array","description":"**One entry per loyalty programme either record belonged to (decided 28 September, audit R149).** Points are added and the higher tier is kept, per programme — a single points number cannot say which programme it belongs to.\n","items":{"type":"object","required":["programmeId","pointsAdded","resultingPoints"],"properties":{"programmeId":{"type":"string","format":"uuid"},"pointsAdded":{"type":"integer","description":"The absorbed record's balance in this programme, added to the survivor's."},"resultingPoints":{"type":"integer"},"tierKept":{"type":"string","nullable":true,"description":"The higher of the two records' tiers in this programme."}}}},"consentOutcome":{"type":"array","description":"Per purpose, the resulting position. Where the two profiles disagreed, the more restrictive position won.\n","items":{"type":"object","properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"result":{"$ref":"#/components/schemas/ConsentDecision"},"wasRestricted":{"type":"boolean"}}}}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PrivacyAnalyticsAiComplianceIntelligenceView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.consent_record, marketing.privacy_request (new), marketing.privacy_action (new), marketing.retention_policy, marketing.privacy_exception (new), marketing.consent_propagation (new), marketing.tracking_technology","description":"Privacy KPIs for a period (pack 17.2.10). Rates are 0-1 over the period's denominators.","required":["consentRate","withdrawalRate","marketingOptInRate"],"properties":{"consentRate":{"type":"number","minimum":0,"maximum":1,"description":"Granted over presented."},"withdrawalRate":{"type":"number","minimum":0,"maximum":1},"marketingOptInRate":{"type":"number","minimum":0,"maximum":1},"cookieAcceptanceByCategory":{"type":"array","items":{"type":"object","required":["category","acceptanceRate"],"properties":{"category":{"type":"string","enum":["functional","analytics","personalisation","marketing","other"]},"acceptanceRate":{"type":"number","minimum":0,"maximum":1}}}},"privacyRequests":{"type":"integer","minimum":0,"description":"Requests submitted in the period."},"privacyRequestsByType":{"type":"array","items":{"type":"object","properties":{"requestType":{"type":"string"},"count":{"type":"integer","minimum":0}}}},"averageResolutionSeconds":{"type":"integer","minimum":0,"nullable":true},"slaComplianceRate":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Completed within `dueAt`, over completed requests that had one."},"deletionCompletionRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"retentionComplianceRate":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Records actioned by their due date, over records due."},"policyAcceptanceRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"guardianConsentCompletionRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"privacyExceptions":{"type":"integer","minimum":0},"consentPropagationFailures":{"type":"integer","minimum":0},"consentFunnel":{"type":"array","description":"In order, each step's count and rate over the first step.","items":{"type":"object","required":["step","count"],"properties":{"step":{"type":"string","maxLength":80,"description":"e.g. privacyNoticeDisplayed, marketingConsentPresented, emailOptIn."},"count":{"type":"integer","minimum":0},"rate":{"type":"number","minimum":0,"maximum":1}}}},"riskFindings":{"type":"array","description":"AI findings for human investigation; none is acted on automatically.","items":{"type":"object","required":["kind","summary"],"properties":{"kind":{"type":"string","enum":["trendAnomaly","abandonmentByLanguage","supersededPolicyInUse","configurationMismatch","other"]},"summary":{"type":"string","maxLength":500},"severity":{"type":"string","enum":["low","medium","high"]},"detectedAt":{"type":"string","format":"date-time"},"exceptionId":{"type":"string","format":"uuid","nullable":true,"description":"Set once someone raised an exception from it."}}}},"asOf":{"type":"string","format":"date-time"}}},
"PrivacyAuditEvidenceComplianceReportingView": {"type":"object","x-ticvai-persistence":"marketing.privacy_audit_event","description":"One privacy audit event (pack 17.2.9 Audit Fields). Append-only; written by the operation that performed the event, never through an API.","required":["eventId","action","occurredAt"],"properties":{"eventId":{"type":"string","format":"uuid","readOnly":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"action":{"type":"string","enum":["consentGranted","consentWithdrawn","preferenceChanged","policyAccepted","privacyRequestCreated","identityVerified","dataExportGenerated","correctionRequested","deletionApproved","anonymisationExecuted","retentionAction","legalHold","administrativeOverride","configurationChange"]},"actorType":{"type":"string","enum":["customer","guardian","staff","system","ai"]},"actorPrincipalId":{"type":"string","format":"uuid","nullable":true},"actorRole":{"type":"string","nullable":true,"description":"The role the actor held at the time."},"source":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},"channel":{"type":"string","nullable":true,"description":"A `ConsentSource` value or the staff surface it came through."},"occurredAt":{"type":"string","format":"date-time"},"before":{"type":"object","nullable":true,"additionalProperties":true,"description":"The changed fields before, masked where the field is sensitive."},"after":{"type":"object","nullable":true,"additionalProperties":true},"reason":{"type":"string","maxLength":1000,"nullable":true},"approvalReference":{"type":"string","nullable":true,"description":"The approval that authorised it (privacy action approval, hold approval, package approval)."},"relatedRequestId":{"type":"string","format":"uuid","nullable":true},"relatedCaseId":{"type":"string","format":"uuid","nullable":true},"evidenceReference":{"type":"string","nullable":true,"description":"e.g. the consent evidence id, the policy version, the export asset id."}}},
"PrivacyIncident": {"type":"object","x-ticvai-persistence":"marketing.privacy_incident","description":"BL-176. **A personal-data breach has a regulator clock**, and UAE PDPL gives 72 hours from discovery. Nothing in the package recorded one.\n**Modelled on the maintenance incident pattern**, because the shape is the same — discovery, assessment, containment, notification, closure — and **the field that matters is the one that starts the clock.**\n","required":["id","discoveredAt","severity","status"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"discoveredAt":{"type":"string","format":"date-time","description":"**The clock starts here, not at occurrence.** 72 hours runs from discovery, which is why this is separate from `occurredAt` and why a discovery nobody recorded is a deadline nobody is counting.\n"},"occurredAt":{"type":"string","format":"date-time","nullable":true},"severity":{"type":"string","enum":["low","medium","high","critical"]},"affectedSubjectCount":{"type":"integer","nullable":true},"dataCategories":{"type":"array","items":{"type":"string","enum":["contact","identity","financial","biometric","health","location","behavioural","credentials"]}},"containedAt":{"type":"string","format":"date-time","nullable":true},"regulatorNotifiedAt":{"type":"string","format":"date-time","nullable":true,"description":"**Or a recorded reason for not notifying.** Deciding a breach is not notifiable is a legitimate decision and an undocumented one is indistinguishable from having missed it.\n"},"subjectsNotifiedAt":{"type":"string","format":"date-time","nullable":true},"notNotifiedRationale":{"type":"string","nullable":true},"status":{"type":"string","enum":["open","assessing","contained","notified","closed"]},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"PrivacyOperationsCommandCenterView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.guest_profile, marketing.consent_record, marketing.privacy_request (new), marketing.privacy_action (new), marketing.retention_policy, marketing.privacy_exception (new), marketing.privacy_incident","description":"The privacy operations position for the caller's scope and filters (pack 17.2.1).","required":["totalCustomerPrivacyProfiles","consentHealth","requestQueue"],"properties":{"totalCustomerPrivacyProfiles":{"type":"integer","minimum":0},"activeConsentRecords":{"type":"integer","minimum":0},"withdrawnConsents":{"type":"integer","minimum":0},"marketingOptIns":{"type":"integer","minimum":0},"marketingOptOuts":{"type":"integer","minimum":0},"pendingDataRightsRequests":{"type":"integer","minimum":0,"description":"Requests not yet `completed`."},"overdueRequests":{"type":"integer","minimum":0},"requestsWithoutDeadline":{"type":"integer","minimum":0,"description":"Open requests whose jurisdiction has no configured response period."},"pendingDeletionActions":{"type":"integer","minimum":0},"pendingAnonymization":{"type":"integer","minimum":0},"retentionActionsDue":{"type":"integer","minimum":0,"description":"Records inside the 90-day notice window before their retention action (ADR-0047 §6)."},"consentEvidenceExceptions":{"type":"integer","minimum":0},"privacyIncidentsExceptions":{"type":"integer","minimum":0,"description":"Open privacy exceptions plus open privacy incidents."},"policyReAcceptancePending":{"type":"integer","minimum":0,"description":"Customers whose accepted notice version has been superseded."},"consentHealth":{"type":"array","items":{"type":"object","required":["category","granted","withdrawn","declined"],"properties":{"category":{"type":"string","enum":["emailMarketing","smsMarketing","whatsappMarketing","pushMarketing","personalisation","analytics","location","biometrics","other"]},"otherLabel":{"type":"string","nullable":true,"description":"The configured purpose name, when `category` is `other`."},"granted":{"type":"integer","minimum":0},"withdrawn":{"type":"integer","minimum":0},"declined":{"type":"integer","minimum":0},"requiresRenewal":{"type":"integer","minimum":0}}}},"requestQueue":{"type":"array","description":"Open and recently completed requests by status and configured stage.","items":{"type":"object","required":["status","count"],"properties":{"status":{"type":"string","enum":["submitted","inProgress","completed"]},"stage":{"type":"string","nullable":true},"count":{"type":"integer","minimum":0},"atRisk":{"type":"integer","minimum":0},"overdue":{"type":"integer","minimum":0}}}},"alerts":{"type":"array","items":{"type":"object","required":["kind","count"],"properties":{"kind":{"type":"string","enum":["requestsApproachingDeadline","requestsOverdue","requestsWithoutDeadline","supersededNoticeAccepted","withdrawnConsentInMarketingExport","consentPropagationFailed","retentionActionFailed"]},"count":{"type":"integer","minimum":0},"detail":{"type":"string","maxLength":300,"nullable":true}}}},"asOf":{"type":"string","format":"date-time"}}},
"RecordConsentRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["purpose","decision","noticeVersion","source","recordedAt"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"decision":{"$ref":"#/components/schemas/ConsentDecision"},"channels":{"type":"array","description":"Omit to apply to every channel the purpose covers.","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string"},"source":{"$ref":"#/components/schemas/ConsentSource"},"recordedAt":{"type":"string","format":"date-time"}}},
"RetentionRunResult": {"type":"object","x-ticvai-persistence":"marketing.retention_run","description":"Board 2.8. **Completion evidence is the half that gets forgotten until an audit.**","properties":{"runId":{"type":"string","format":"uuid","x-ticvai-column":"id","description":"The run, stored as `marketing.retention_run`; `PrivacyAction.retentionRunId` points here. Preview runs are stored too, so an executed pass can be compared with what it previewed."},"policyId":{"type":"string","format":"uuid"},"mode":{"type":"string","enum":["preview","execute"]},"recordsAffected":{"type":"integer"},"byAction":{"type":"object","additionalProperties":{"type":"integer"}},"heldBack":{"type":"integer"},"heldBackReasons":{"type":"object","additionalProperties":{"type":"integer"}},"dependencies":{"type":"array","x-ticvai-persisted":false,"description":"Computed for the response; the executed run's detail is in the evidence asset.","items":{"type":"object","properties":{"surface":{"type":"string"},"count":{"type":"integer"},"consequence":{"type":"string"}}}},"evidenceAssetId":{"type":"string","format":"uuid","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"TenantDataRetentionClass": {"type":"string","description":"**The data classes a tenant sets a retention period for** (decided 29 September, Chinmay: all data retention is tenant configuration, one setting per class). Defaults are ADR-0047's and the AI system design's (section 8, decision 5); a legal limit is the only thing the platform enforces.\n| Class | Default | Counted from | Legal limit (refused) | |---|---|---|---| | `guestProfile` | 5 years | last activity | none | | `paymentRecord` | 10 years | created | at least 10 years (4.3.4) | | `financialRecord` | 7 years | created | at least 7 years (6.1.78) | | `auditRecord` | 2 years (authorisation and device audit) | created | none | | `approvalRecord` | 7 years (approvals board 6.7) | decided | none | | `complianceInspection` | 7 years | created | none | | `faceTagBiometric` | 7 days | ticket expiry | make-or-break | | `facePassBiometric` | follows `guestProfile` | last activity | make-or-break | | `aiPrompts` | 90 days (prompts and responses) | created | none | | `aiConversations` | 90 days | last activity | none | | `aiDecisionRecords` | follows `auditRecord` (decision records and the approvals of AI actions) | decided | none | | `aiMetadataIndex` | always follows `aiDecisionRecords` (summaries, entities, embeddings) | created | none |\n**ADR-0047's floors and ceilings that are not law are defaults now, not refusals** (the audit floor of one year, the proposed seven-year guest-profile ceiling, the Face Tag thirty-day ceiling). Platform-owned copies — the burst environment copy, a decommissioned cell — are not tenant data classes and are not here.\n","enum":["guestProfile","paymentRecord","financialRecord","auditRecord","approvalRecord","complianceInspection","faceTagBiometric","facePassBiometric","aiPrompts","aiConversations","aiDecisionRecords","aiMetadataIndex"]},
"TenantDataRetentionSetting": {"type":"object","x-ticvai-persistence":"tenancy.data_retention_setting","description":"**One tenant's retention period for one data class** (decided 29 September, Chinmay). One row per tenant and class, written by `setDataRetentionSetting`; a class with no row takes the platform default. The limit and default fields are the platform's catalogue, computed for the response and not stored on the row.\n","required":["dataClass"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"dataClass":{"allOf":[{"$ref":"#/components/schemas/TenantDataRetentionClass"}],"x-ticvai-unique":"tenant","description":"One row per class per tenant. On a write it comes from the path; a body value is ignored."},"retainAmount":{"type":"integer","nullable":true,"minimum":0,"description":"The tenant's period. Null with no `followsDataClass` means the platform default applies. Zero means the data is not kept past the transaction that produced it.\n"},"retainUnit":{"type":"string","nullable":true,"enum":["days","months","years"],"description":"Required with `retainAmount`."},"followsDataClass":{"allOf":[{"$ref":"#/components/schemas/TenantDataRetentionClass"}],"nullable":true,"description":"Keep this class for as long as another class is kept. Set by default for `aiDecisionRecords` (follows `auditRecord`), `facePassBiometric` (follows `guestProfile`) and `aiMetadataIndex` (follows `aiDecisionRecords`, and cannot be changed).\n"},"onExpiry":{"type":"string","enum":["archive","anonymise","delete"],"default":"archive","description":"ADR-0047's stages. `archive` moves the data to the archive instance, from where it is erased on the class's own schedule; derived stores (the AI index, search) purge at archive, not later.\n"},"anchor":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"enum":["createdAt","lastActivity","decidedAt","ticketExpiry"],"description":"What the period is counted from. Fixed per class by the platform."},"effectiveAmount":{"type":"integer","readOnly":true,"x-ticvai-persisted":false,"description":"The period actually applied, after follows and defaults are resolved."},"effectiveUnit":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"isDefault":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"True when the tenant has not set this class and the platform default applies."},"defaultAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false},"defaultUnit":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"legalMinimumAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"A floor the law sets. A shorter period is refused (`422`)."},"legalMaximumAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"A maximum the law sets. A longer period is refused (`422`). Null for every class until the biometric make-or-break is answered."},"legalLimitUnit":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"legalBasis":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"The law or requirement the limit comes from, e.g. `4.3.4`."},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"updatedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The tenant. Retention is set at tenant scope only."}}},
"VersioningEffectiveDatesLegalChangeControlView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.form_definition, marketing.waiver_version_control (new), marketing.form_submission and marketing.waiver_signature","description":"One version of one waiver and its change control (pack 11.1.8).","required":["formId","versionNumber","status","createdAt"],"properties":{"formId":{"type":"string","format":"uuid"},"waiverName":{"type":"string"},"versionNumber":{"type":"integer","minimum":1},"status":{"type":"string","enum":["draft","published","superseded","retired"],"description":"`FormDefinition.status` (states/form-definition.yaml)."},"lifecycleStatus":{"type":"string","enum":["draft","review","pendingApproval","approved","scheduled","published","suspended","expired","archived"]},"createdByUserId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"changeReason":{"type":"string","maxLength":1000,"nullable":true},"legalReviewer":{"type":"string","nullable":true,"description":"`FormDefinition.legalReviewedBy`."},"legalReviewedAt":{"type":"string","format":"date-time","nullable":true},"approvedByUserId":{"type":"string","format":"uuid","nullable":true},"approvedAt":{"type":"string","format":"date-time","nullable":true},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"resignRule":{"type":"string","enum":["noResign","resignAtNextBooking","resignBeforeNextVisit"],"description":"Whether people who signed an earlier version must sign this one."},"suspended":{"type":"boolean","default":false},"suspensionReason":{"type":"string","maxLength":500,"nullable":true},"signatureCount":{"type":"integer","minimum":0,"description":"Signatures taken against this exact version."},"comparison":{"type":"object","nullable":true,"description":"Present when `compareWith` is given.","properties":{"comparedWithVersion":{"type":"integer","minimum":1},"addedText":{"type":"array","items":{"type":"object","properties":{"blockKey":{"type":"string"},"language":{"type":"string"},"text":{"type":"string"}}}},"removedText":{"type":"array","items":{"type":"object","properties":{"blockKey":{"type":"string"},"language":{"type":"string"},"text":{"type":"string"}}}},"changedQuestions":{"type":"array","items":{"type":"string"},"description":"Field keys added, removed or changed."},"changedSignatoryRules":{"type":"array","items":{"type":"string"},"description":"Names of the signatory-rule properties that differ."},"changedAssociations":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Associations added, removed or changed between the two versions' publication."}}}}}
}
```
