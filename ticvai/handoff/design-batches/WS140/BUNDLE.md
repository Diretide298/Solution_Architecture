# WS140 — Marketing CRM Configuration Reference v1.0 board 6

**10 screens · 16 operations · 16 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `AI_USE, GUEST_MANAGE, MARKETING_MANAGE, MARKETING_SEND, MARKETING_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
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
| `BO-784` | Communications Center | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-785` | Template Library | A | 0 | 0 | 6 | 18 | 1 | 0 | — | notStarted (—) |
| `BO-786` | Newsletter Builder | B–D | 0 | 0 | 6 | 12 | 0 | 0 | — | notStarted (—) |
| `BO-787` | Content Blocks & Product Feed | B–D | 0 | 0 | 6 | 12 | 0 | 6 | — | notStarted (—) |
| `BO-788` | Subscriptions & Preferences | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-789` | Transactional Notification Rules | B–D | 0 | 0 | 6 | 7 | 1 | 0 | — | notStarted (—) |
| `BO-790` | Scheduling, Priority & Approval | B–D | 0 | 0 | 6 | 0 | 0 | 3 | — | notStarted (—) |
| `BO-791` | Delivery, Retry & Failover | B–D | 0 | 0 | 6 | 6 | 1 | 0 | — | notStarted (—) |
| `BO-792` | Deliverability & Analytics | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-793` | AI Content, Translation & Audit | B–D | 0 | 0 | 6 | 12 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-784, BO-785, BO-786, BO-787, BO-788, BO-789, BO-790, BO-791, BO-792, BO-793 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-784` Communications Center

**Monitor outbound communication volume, delivery and engagement. Show messages sent, delivered, failed, opened, clicked, converted and unsubscribed with attributed revenue. Compare email, SMS, WhatsApp, push, in-app, web and operational channels and providers. Display active alerts for provider outage, high bounce, consent error, queue delay or retry exhaustion. Filter and drill down by tenant, brand, venue, region, template, category, channel and date. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/communications-center-bo-784` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listCommunicationService` ?from |
| To | date and time picker | — | — | `listCommunicationService` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listCommunicationService` (onLoad, Channel health and volume)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-785` Template Library: *Template Library*
- → `BO-786` Newsletter Builder: *Newsletter Builder*
- → `BO-787` Content Blocks & Product Feed: *Content Blocks & Product Feed*
- → `BO-788` Subscriptions & Preferences: *Subscriptions & Preferences*
- → `BO-789` Transactional Notification Rules: *Transactional Notification Rules*
- → `BO-790` Scheduling, Priority & Approval: *Scheduling, Priority & Approval*
- → `BO-791` Delivery, Retry & Failover: *Delivery, Retry & Failover*
- → `BO-792` Deliverability & Analytics: *Deliverability & Analytics*
- → `BO-793` AI Content, Translation & Audit: *AI Content, Translation & Audit*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The communications list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the communications untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No communications yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the communications are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listCommunicationService` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Communications dashboard shows activity across email, WhatsApp and SMS: delivered, pending, failed. Delivery queue tracks failed sends with automatic retry; routing/fallback rules send on an alternate channel if delivery fails. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-559)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-784` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-784`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 6
- Flow F249 *Marketing CRM Configuration Reference v1.0 board 6: Communications Center*, step 1: Opens Communications Center → Monitor outbound communication volume, delivery and engagement. Show messages sent, delivered, failed, opened, clicked, converted and unsubscribed with attributed revenue. Compare email, SMS …
- Flow F249 *Marketing CRM Configuration Reference v1.0 board 6: Communications Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F249 *Marketing CRM Configuration Reference v1.0 board 6: Communications Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F249 *Marketing CRM Configuration Reference v1.0 board 6: Communications Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F249 *Marketing CRM Configuration Reference v1.0 board 6: Communications Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F249 *Marketing CRM Configuration Reference v1.0 board 6: Communications Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F249 *Marketing CRM Configuration Reference v1.0 board 6: Communications Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F249 *Marketing CRM Configuration Reference v1.0 board 6: Communications Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F249 branch at step 1 (expected): when Nothing has been set up on Communications Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F249 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-784?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-785`, `BO-786`, `BO-787`, `BO-788`, `BO-789`, `BO-790`, `BO-791`, `BO-792`, `BO-793`.
- [ ] Every gated control is gated: `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-785` Template Library

**Centrally manage reusable message templates. Organize marketing, ticketing, reservation, membership, loyalty, wallet and operational templates by channel and purpose. Maintain brand, venue, language, version, owner, approval, validity and active/inactive status. Preview test data, validate required tokens, links, attachments and channel-specific constraints. Clone, archive and compare templates while preserving lineage and complete change history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block A · ticket #20779 (APP-SETUP-BO-785) |
| Who uses it | venue staff holding `AI_USE`, `MARKETING_MANAGE`, `MARKETING_VIEW`, `TENANT_CONFIGURE` (1 operate, 2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/template-library-bo-785` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listMessageTemplates` ?channel |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create message template (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listMessageTemplates` (onLoad, The template library)

**Where the user goes next**

- → `BO-784` Communications Center: *Back to Communications Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The template list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the template untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No template yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the template are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Unknown merge field, or a required language is missing; 409 Drafting is not allowed at this scope now: the capability is paused (`capability-paused`) or governance blocks it (`governance-blocked`, naming the policy and … |

#### Permissions

- `listMessageTemplates` → `MARKETING_VIEW` (read) · staff
- `createMessageTemplate` → `MARKETING_MANAGE` (configure) · staff
- `proposeMarketingContent` → `AI_USE` (operate) · staff
- `proposeTranslations` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.3 | The system should support email templates for e-ticket purchase confirmation supporting dynamic parameters. The email templates should be configurable per site, per event | Ticketing Sales | CONTRACTED | `listMessageTemplates` |
| 2.6.26 | It is expected that confirmation email can be generated including the number of tickets, the cost, the order number. | Ticketing Sales | CONTRACTED | `listMessageTemplates` |
| 22.1.2 | Campaign Templates | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.1.7 | Dynamic Personalization | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.9.1 | Notification Template Management | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.9.3 | Dynamic Personalization | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.9.22 | Rich Content Notifications | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.3.18 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.9 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.10 | AI Subject Line Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.9.17 | AI Language Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.14 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Sender identity per brand (from and reply-to, e.g. no-reply@venue.com, customerservice@venue.com). Templates fully configurable per channel (email, SMS, WhatsApp): header, logo, footer and content, for consistent branded communications. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-560)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-785` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-785`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 6
- Flow F249 *Marketing CRM Configuration Reference v1.0 board 6: Communications Center*, step 2: Works in Template Library → Centrally manage reusable message templates. Organize marketing, ticketing, reservation, membership, loyalty, wallet and operational templates by channel and purpose. Maintain brand, venue, language …
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-785?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create message template, Cancel.
- [ ] Every transition is wired: `BO-784`.
- [ ] Every gated control is gated: `AI_USE`, `MARKETING_MANAGE`, `MARKETING_VIEW`, `TENANT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-786` Newsletter Builder

**Create responsive, branded newsletters without coding. Provide drag-and-drop header, text, image, event, ticket, membership, loyalty, CTA, divider and footer blocks. Configuration Scope of Work / Version 1.0 31 Support personalization, dynamic content, reusable templates, language variants and desktop/mobile preview. Validate accessibility, links, unsubscribe content, sender details and deliverability before test or approval. Support draft, test send, review, approve, schedule, clone and version-management workflows. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `MARKETING_MANAGE` (1 operate, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/newsletter-builder-bo-786` |

**Known gaps.** **Newsletter Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create message template (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-784` Communications Center: *Back to Communications Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The newsletter list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the newsletter untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No newsletter yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the newsletter are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Unknown merge field, or a required language is missing; 409 Drafting is not allowed at this scope now: the capability is paused (`capability-paused`) or governance blocks it (`governance-blocked`, naming the policy and … |

#### Permissions

- `createMessageTemplate` → `MARKETING_MANAGE` (configure) · staff
- `proposeMarketingContent` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.1.2 | Campaign Templates | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.1.7 | Dynamic Personalization | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.9.1 | Notification Template Management | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.9.3 | Dynamic Personalization | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.9.22 | Rich Content Notifications | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.3.18 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.9 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.10 | AI Subject Line Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.9.17 | AI Language Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.14 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.16 | AI Website Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.17 | AI Mobile App Content Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-786` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-786`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 6
- Flow F249 *Marketing CRM Configuration Reference v1.0 board 6: Communications Center*, step 4: Works in Newsletter Builder → Create responsive, branded newsletters without coding. Provide drag-and-drop header, text, image, event, ticket, membership, loyalty, CTA, divider and footer blocks. Configuration Scope of Work / …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-786?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create message template, Cancel.
- [ ] Every transition is wired: `BO-784`.
- [ ] Every gated control is gated: `AI_USE`, `MARKETING_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-787` Content Blocks & Product Feed

**Connect communications to reusable content and live products. Maintain approved content blocks for banners, copy, events, tickets, memberships, loyalty, promotions, CTAs and footers. Configure live feeds from events, products, ticket inventory, capacity, pricing, promotions and recommendations. Define filters, sorting, fallback content, refresh interval, expiration and behavior when inventory is unavailable. Track which campaigns and templates use each block before editing or deactivation. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `MARKETING_MANAGE` (1 operate, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/content-blocks-product-feed-bo-787` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create message template (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-784` Communications Center: *Back to Communications Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The content blocks product list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the content blocks product untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No content blocks product yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the content blocks product are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Unknown merge field, or a required language is missing; 409 Drafting is not allowed at this scope now: the capability is paused (`capability-paused`) or governance blocks it (`governance-blocked`, naming the policy and … |

#### Permissions

- `createMessageTemplate` → `MARKETING_MANAGE` (configure) · staff
- `proposeMarketingContent` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.1.2 | Campaign Templates | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.1.7 | Dynamic Personalization | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.9.1 | Notification Template Management | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.9.3 | Dynamic Personalization | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.9.22 | Rich Content Notifications | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.3.18 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.9 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.10 | AI Subject Line Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.9.17 | AI Language Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.14 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.16 | AI Website Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.17 | AI Mobile App Content Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-787` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-787`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 6
- Flow F249 *Marketing CRM Configuration Reference v1.0 board 6: Communications Center*, step 6: Works in Content Blocks & Product Feed → Connect communications to reusable content and live products. Maintain approved content blocks for banners, copy, events, tickets, memberships, loyalty, promotions, CTAs and footers. Configure live …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-787?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create message template, Cancel.
- [ ] Every transition is wired: `BO-784`.
- [ ] Every gated control is gated: `AI_USE`, `MARKETING_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-788` Subscriptions & Preferences

**Manage newsletter subscriptions and messaging eligibility. Configure subscription categories, topics, channels, frequency, consent mapping, suppression and do-not-contact status. Search subscribers and view preferred channels, verification, consent source, status and last change. Support guest self-service and authorized administration while preventing forced marketing opt- in. Synchronize changes immediately to campaign, journey, newsletter and delivery services and audit them. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/subscriptions-preferences-bo-788` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getMarketingSubscription` (onLoad, What a guest is subscribed to)

**Where the user goes next**

- → `BO-784` Communications Center: *Back to Communications Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The subscriptions preferences list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the subscriptions preferences untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No subscriptions preferences yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the subscriptions preferences are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setMarketingSubscription` → `MARKETING_VIEW` (read) · guest
- `getMarketingSubscription` → `MARKETING_VIEW` (read) · guest
- `addSuppression` → `GUEST_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Consent and communication preference tracking records marketing/newsletter opt-in status per customer. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-562)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-788` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-788`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 6
- Flow F249 *Marketing CRM Configuration Reference v1.0 board 6: Communications Center*, step 8: Works in Subscriptions & Preferences → Manage newsletter subscriptions and messaging eligibility. Configure subscription categories, topics, channels, frequency, consent mapping, suppression and do-not-contact status. Search subscribers …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-788?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-784`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-789` Transactional Notification Rules

**Map operational events to the correct notification behavior. Configure rules for purchase, reservation, check-in, membership, loyalty, wallet, refund, cancellation, waitlist and operational events. Select template, channel, recipients, timing, priority, conditions, attachments and personalization mapping. Differentiate mandatory transactional notices from optional marketing and apply the correct consent policy. Test rules with sample events and prevent conflicting or duplicate notifications. Configuration Scope of Work / Version 1.0 32 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `MARKETING_MANAGE`, `MARKETING_VIEW` (1 operate, 1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/transactional-notification-rules-bo-789` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Ownership | segmented control | — | Platform · Crm | `listSystemTransactionalTemplate` ?ownership |
| Source module | select | — | Crm · Ticketing · Membership · Waiver · Group sales · Customer service · Finance · Wallet · Resource management · Access control · Other | `listSystemTransactionalTemplate` ?sourceModule |
| Business event | text field | — | — | `listSystemTransactionalTemplate` ?businessEvent |
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listSystemTransactionalTemplate` ?channel |
| Brand | picker: choose a brand | — | — | `listSystemTransactionalTemplate` ?brandId |
| Language | text field | — | — | `listSystemTransactionalTemplate` ?language |
| Status | segmented control | — | Draft · Published · Archived | `listSystemTransactionalTemplate` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save message trigger (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listSystemTransactionalTemplate` (onLoad, Transactional templates)

**Where the user goes next**

- → `BO-784` Communications Center: *Back to Communications Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The transactional notification rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the transactional notification rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No transactional notification rules yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the transactional notification rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 400 `sendTimeMode` `optimised` on a trigger whose `priority` is `operational` or `transactional` (29 September, build pass, group G2), or an `event` not in the …; 409 Drafting is not allowed at this scope now: the capability is paused (`capability-paused`) or governance blocks it (`governance-blocked`, naming the policy and … |

#### Permissions

- `listSystemTransactionalTemplate` → `MARKETING_VIEW` (read) · staff
- `setMessageTrigger` → `MARKETING_MANAGE` (configure) · staff
- `proposeMarketingContent` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.3.18 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.9 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.10 | AI Subject Line Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.9.17 | AI Language Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.14 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.16 | AI Website Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.17 | AI Mobile App Content Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Notification triggers must key off precise event states where needed: a post-visit survey only when the ticket was actually scanned/used, whereas a "how was your experience" follow-up can trigger off the sale. Trigger mapping must expose such event states. *(agreed · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-561)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-789` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-789`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 6
- Flow F249 *Marketing CRM Configuration Reference v1.0 board 6: Communications Center*, step 10: Works in Transactional Notification Rules → Map operational events to the correct notification behavior. Configure rules for purchase, reservation, check-in, membership, loyalty, wallet, refund, cancellation, waitlist and operational events. …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-789?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save message trigger, Cancel.
- [ ] Every transition is wired: `BO-784`.
- [ ] Every gated control is gated: `AI_USE`, `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-790` Scheduling, Priority & Approval

**Control message timing, urgency and governance. Support immediate, scheduled, recurring and event-relative delivery with timezone, windows and blackout periods. Configure Critical, High, Medium and Low priority, queue treatment, escalation and delivery deadline. Route selected templates and schedules through reviewer and approver stages with delegation and comments. Provide a final audience, content, channel, cost and policy pre-flight before activation. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/scheduling-priority-approval-bo-790` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listRoutingPriorityThrottling` ?channel |
| Country | text field | — | pattern `^[A-Z]{2}$` | `listRoutingPriorityThrottling` ?country |
| Brand | picker: choose a brand | — | — | `listRoutingPriorityThrottling` ?brandId |
| Priority class | radio group | — | P1 · P2 · P3 · P4 | `listRoutingPriorityThrottling` ?priorityClass |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listRoutingPriorityThrottling` (onLoad, Scheduling, priority and throttling)

**Where the user goes next**

- → `BO-784` Communications Center: *Back to Communications Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The scheduling priority approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the scheduling priority approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No scheduling priority approval yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the scheduling priority approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listRoutingPriorityThrottling` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-790` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-790`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 6
- Flow F249 *Marketing CRM Configuration Reference v1.0 board 6: Communications Center*, step 12: Works in Scheduling, Priority & Approval → Control message timing, urgency and governance. Support immediate, scheduled, recurring and event-relative delivery with timezone, windows and blackout periods. Configure Critical, High, Medium and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-790?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-784`.
- [ ] Every gated control is gated: `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-791` Delivery, Retry & Failover

**Configure reliable routing across communication providers and channels. Maintain primary, secondary and tertiary providers per channel, tenant, region and message category. Define retry count, delay, backoff, retryable errors, expiration and dead-letter handling. Configure channel failover order while rechecking consent, content compatibility and urgency. Provide message trace, provider response, failure reason, manual replay controls and audit history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_SEND`, `MARKETING_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `dispatchId` (navigation) |
| Route | `/engagement-support/delivery-retry-failover-bo-791` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Pending · Processing · Sent · Delivered · Failed · Retrying · Dead lettered · Cancelled | `listDeliveryQueueFailure` ?status |
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listDeliveryQueueFailure` ?channel |
| Source module | select | — | Crm · Ticketing · Membership · Waiver · Group sales · Customer service · Finance · Wallet · Resource management · Access control · Other | `listDeliveryQueueFailure` ?sourceModule |
| Business event | text field | — | — | `listDeliveryQueueFailure` ?businessEvent |
| Provider | picker: choose a provider | — | — | `listDeliveryQueueFailure` ?providerId |
| Priority | radio group | — | P1 · P2 · P3 · P4 | `listDeliveryQueueFailure` ?priority |
| Failure category | select | — | Provider unavailable · Invalid address · Invalid mobile · Rate limited · Authentication error · Template rejected · Timeout · Consent block · Unknown error | `listDeliveryQueueFailure` ?failureCategory |
| From | date and time picker | — | — | `listDeliveryQueueFailure` ?from |
| To | date and time picker | — | — | `listDeliveryQueueFailure` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listDeliveryQueueFailure` (onLoad, Failures and retries)

**Where the user goes next**

- → `BO-784` Communications Center: *Back to Communications Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The delivery retry failover list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the delivery retry failover untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No delivery retry failover yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the delivery retry failover are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listDeliveryQueueFailure` → `MARKETING_VIEW` (read) · staff
- `retryMessageDispatch` → `MARKETING_SEND` (operate) · staff, service

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.8.19 | Canned Responses | Marketing & CRM | CONTRACTED | `retryMessageDispatch` |
| 22.9.6 | Notification Priority Management | Marketing & CRM | CONTRACTED | `retryMessageDispatch` |
| 22.9.8 | Notification Preferences Center | Marketing & CRM | CONTRACTED | `retryMessageDispatch` |
| 22.9.20 | Notification Retry Management | Marketing & CRM | CONTRACTED | `retryMessageDispatch` |
| 22.9.21 | Channel Failover Management | Marketing & CRM | CONTRACTED | `retryMessageDispatch` |
| 22.13.8 | Guest Preference Center | Marketing & CRM | CONTRACTED | `retryMessageDispatch` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Communications dashboard shows activity across email, WhatsApp and SMS: delivered, pending, failed. Delivery queue tracks failed sends with automatic retry; routing/fallback rules send on an alternate channel if delivery fails. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-559)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-791` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-791`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 6
- Flow F249 *Marketing CRM Configuration Reference v1.0 board 6: Communications Center*, step 14: Works in Delivery, Retry & Failover → Configure reliable routing across communication providers and channels. Maintain primary, secondary and tertiary providers per channel, tenant, region and message category. Define retry count, delay …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-791?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-784`.
- [ ] Every gated control is gated: `MARKETING_SEND`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-792` Deliverability & Analytics

**Monitor technical delivery quality and commercial outcomes. Report sender reputation, inbox placement, hard/soft bounce, complaints, blocks, opens, clicks and conversions. Compare providers, domains, channels, templates, languages, brands and regions over time. Trace individual messages from generation to provider response and guest engagement where authorized. Alert on thresholds and attribute revenue using the shared marketing attribution framework. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/deliverability-analytics-bo-792` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listProviderHealthUsage` ?channel |
| Provider | picker: choose a provider | — | — | `listProviderHealthUsage` ?providerId |
| Brand | picker: choose a brand | — | — | `listProviderHealthUsage` ?brandId |
| Module | select | — | Crm · Ticketing · Membership · Waiver · Group sales · Customer service · Finance · Wallet · Resource management · Access control · Other | `listProviderHealthUsage` ?module |
| Country | text field | — | pattern `^[A-Z]{2}$` | `listProviderHealthUsage` ?country |
| Message class | radio group | — | Transactional · Operational · Service · Marketing | `listProviderHealthUsage` ?messageClass |
| Group by | select | — | Channel · Provider · Brand · Venue · Module · Country · Message class · Campaign · Event · Business unit | `listProviderHealthUsage` ?groupBy |
| From | date and time picker | — | — | `listProviderHealthUsage` ?from |
| To | date and time picker | — | — | `listProviderHealthUsage` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listProviderHealthUsage` (onLoad, Deliverability and cost)

**Where the user goes next**

- → `BO-784` Communications Center: *Back to Communications Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The deliverability analytics list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the deliverability analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No deliverability analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the deliverability analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listProviderHealthUsage` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-792` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-792`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 6
- Flow F249 *Marketing CRM Configuration Reference v1.0 board 6: Communications Center*, step 16: Works in Deliverability & Analytics → Monitor technical delivery quality and commercial outcomes. Report sender reputation, inbox placement, hard/soft bounce, complaints, blocks, opens, clicks and conversions. Compare providers, domains …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-792?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-784`.
- [ ] Every gated control is gated: `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-793` AI Content, Translation & Audit

**Use governed AI for communication creation and localization. Generate subject lines, titles, summaries and message variants by objective, tone, audience and channel. Translate content using approved languages, terminology glossary, brand rules and protected placeholders. Configuration Scope of Work / Version 1.0 33 Display confidence and changes, require manual review where configured and prevent unsupported claims. Retain prompt/context classification, model/version, output, edits, approver and publication audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work / Version 1.0 34 Board 7 - Omnichannel Inbox, AI Chatbot & Agent Workspace Figure 7. High-definition configuration board with all 10 screens. Configuration Scope of Work / Version 1.0 35**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `GUEST_MANAGE`, `TENANT_CONFIGURE` (1 operate, 2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `actionId` (navigation) |
| Route | `/engagement-support/ai-content-translation-audit-bo-793` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-784` Communications Center: *Back to Communications Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The content translation audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the content translation audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No content translation audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the content translation audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A language of a published version was changed.; 409 Drafting is not allowed at this scope now: the capability is paused (`capability-paused`) or governance blocks it (`governance-blocked`, naming the policy and …; 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213). |

#### Permissions

- `setLocalizationBrandingCustomer` → `GUEST_MANAGE` (configure) · staff
- `proposeMarketingContent` → `AI_USE` (operate) · staff
- `decideProposedAction` → `AI_USE` (operate) · staff
- `proposeTranslations` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.3.18 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.9 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.10 | AI Subject Line Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.9.17 | AI Language Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.14 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.16 | AI Website Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.17 | AI Mobile App Content Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 8.1.4 | Approval Before Execution AI recommendations affecting pricing or financial operations shall require approval before execution | Unified Operations Dashboard | CONTRACTED | `decideProposedAction` |
| 2.6.34 | Website should support multiple languages configured in the web backoffice. The intial translation should be done through AI and the backoffice user should have the ability to fix the translation if … | Ticketing Sales | CONTRACTED | `proposeTranslations` |
| 22.4.11 | AI Translation | Marketing & CRM | CONTRACTED | `proposeTranslations` |
| 22.9.18 | AI Translation Services | Marketing & CRM | CONTRACTED | `proposeTranslations` |
| 22.10.15 | AI Translation Services | Marketing & CRM | CONTRACTED | `proposeTranslations` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Translation workflow: text entered in English, machine-translated, then reviewed and validated by the tenant's own team in the back office/CMS before publishing; applies to website, POS and mobile app. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-081)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-793` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS75 Marketing CRM Configuration Reference v1.0 Board 6.dc.html#bo-793`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 6
- Flow F249 *Marketing CRM Configuration Reference v1.0 board 6: Communications Center*, step 18: Works in AI Content, Translation & Audit → Use governed AI for communication creation and localization. Generate subject lines, titles, summaries and message variants by objective, tone, audience and channel. Translate content using approved …
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-793?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-784`.
- [ ] Every gated control is gated: `AI_USE`, `GUEST_MANAGE`, `TENANT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**6 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addSuppression": {"method":"POST","path":"/consent/suppression-list","contract":"marketing-crm","summary":"Suppress an address","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Suppression"},
"createMessageTemplate": {"method":"POST","path":"/message-templates","contract":"marketing-crm","summary":"Create a message template","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MessageTemplate","responds":"MessageTemplate"},
"decideProposedAction": {"method":"POST","path":"/proposed-actions/{actionId}/decide","contract":"ai","summary":"Approve or reject a proposal","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProposedAction"},
"getMarketingSubscription": {"method":"GET","path":"/marketing-subscriptions","contract":"marketing-crm","summary":"What this guest has opted into","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"MarketingSubscription"},
"listCommunicationService": {"method":"GET","path":"/communication-service","contract":"marketing-crm","summary":"Communication Service Command Center","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venueId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false}],"requestBody":null,"responds":"CommunicationServiceCommandCenterView"},
"listDeliveryQueueFailure": {"method":"GET","path":"/delivery-queue-failure","contract":"marketing-crm","summary":"Delivery Queue, Failure & Retry Management","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"sourceModule","in":"query","required":false},{"name":"businessEvent","in":"query","required":false},{"name":"providerId","in":"query","required":false},{"name":"priority","in":"query","required":false},{"name":"failureCategory","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMessageTemplates": {"method":"GET","path":"/message-templates","contract":"marketing-crm","summary":"List message templates","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProviderHealthUsage": {"method":"GET","path":"/provider-health-usage","contract":"marketing-crm","summary":"Provider Health, Usage & Cost Monitoring","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"channel","in":"query","required":false},{"name":"providerId","in":"query","required":false},{"name":"brandId","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"module","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":"messageClass","in":"query","required":false},{"name":"groupBy","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false}],"requestBody":null,"responds":"ProviderHealthUsageCostMonitoringView"},
"listRoutingPriorityThrottling": {"method":"GET","path":"/routing-priority-throttling","contract":"marketing-crm","summary":"Routing, Priority, Throttling & Fallback Rules","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":"brandId","in":"query","required":false},{"name":"priorityClass","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSystemTransactionalTemplate": {"method":"GET","path":"/system-transactional-template","contract":"marketing-crm","summary":"System Transactional Template Registry","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"ownership","in":"query","required":false},{"name":"sourceModule","in":"query","required":false},{"name":"businessEvent","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"brandId","in":"query","required":false},{"name":"language","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"proposeMarketingContent": {"method":"POST","path":"/ai/content-drafts","contract":"ai","summary":"Draft marketing content for a person to edit and apply","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"proposeTranslations": {"method":"POST","path":"/ai/translate","contract":"ai","summary":"Fill translation gaps with a first pass, for a human to edit","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"retryMessageDispatch": {"method":"POST","path":"/message-dispatches/{dispatchId}/retry","contract":"marketing-crm","summary":"Send it again, or by another channel","permission":"MARKETING_SEND","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MessageDispatch"},
"setLocalizationBrandingCustomer": {"method":"PUT","path":"/localization-branding-customer","contract":"marketing-crm","summary":"Set a waiver version's languages, branding and channels","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LocalizationBrandingCustomerExperienceConfigurationInput","responds":"LocalizationBrandingCustomerExperienceConfigurationView"},
"setMarketingSubscription": {"method":"PUT","path":"/marketing-subscriptions","contract":"marketing-crm","summary":"Subscribe or unsubscribe","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MarketingSubscription","responds":"MarketingSubscription"},
"setMessageTrigger": {"method":"POST","path":"/message-triggers","contract":"marketing-crm","summary":"Fire a message from a platform event","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MessageTrigger","responds":"MessageTrigger"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CommunicationServiceCommandCenterView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.message_dispatch, marketing.message_dispatch_attempt (new), marketing.communication_provider (new)","description":"Platform KPIs and breakdowns for the communication service over the requested window. Counts are messages (one dispatch = one message on one channel), not recipients.\n","required":["windowFrom","windowTo","messagesProcessed","byChannel","byModule"],"properties":{"windowFrom":{"type":"string","format":"date-time"},"windowTo":{"type":"string","format":"date-time"},"messagesProcessed":{"type":"integer","minimum":0,"description":"Messages accepted by the service in the window (the pack's \"Messages Processed Today\")."},"delivered":{"type":"integer","minimum":0},"failed":{"type":"integer","minimum":0},"pending":{"type":"integer","minimum":0},"retrying":{"type":"integer","minimum":0},"averageDeliverySeconds":{"type":"number","minimum":0,"description":"Mean time from acceptance to provider-confirmed delivery, in (fractional) seconds."},"providerAvailabilityRate":{"type":"number","minimum":0,"maximum":1,"description":"Share of the window the active providers were reachable, weighted by volume."},"byChannel":{"type":"array","description":"Sent volume and health per channel, one row per provider on it (the pack's channel tiles and Channel Health table).","items":{"type":"object","required":["channel","sent"],"properties":{"channel":{"$ref":"#/components/schemas/MessageChannel"},"providerId":{"type":"string","format":"uuid"},"providerName":{"type":"string"},"sent":{"type":"integer","minimum":0},"successRate":{"type":"number","minimum":0,"maximum":1},"averageLatencySeconds":{"type":"number","minimum":0},"health":{"type":"string","enum":["healthy","warning","critical"]}}}},"byModule":{"type":"array","description":"Volume originating from each TICVAI module.","items":{"type":"object","required":["module","volume"],"properties":{"module":{"type":"string","enum":["crm","ticketing","membership","waiver","groupSales","customerService","finance","wallet","resourceManagement","accessControl","other"]},"volume":{"type":"integer","minimum":0},"successRate":{"type":"number","minimum":0,"maximum":1},"averageLatencySeconds":{"type":"number","minimum":0},"health":{"type":"string","enum":["healthy","warning","critical"]}}}},"alerts":{"type":"array","description":"Live operational alerts (failure-rate spikes, queued backlogs, providers near their rate limit).","items":{"type":"object","required":["kind","severity","message","raisedAt"],"properties":{"kind":{"type":"string","enum":["failureRateSpike","queueBacklog","rateLimitApproaching","providerDegraded","other"]},"severity":{"type":"string","enum":["info","warning","critical"]},"message":{"type":"string"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"providerId":{"type":"string","format":"uuid"},"raisedAt":{"type":"string","format":"date-time"}}}},"aiHealthSummary":{"type":"string","description":"AI-written plain-language summary of platform health; absent when AI processing is off for the tenant."}}},
"DeliveryQueueFailureRetryManagementView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.message_dispatch, marketing.message_dispatch_attempt (new), marketing.message_template, marketing.communication_provider (new)","description":"One communication in the delivery queue and where it stands.","required":["communicationId","channel","status","attempts","createdAt"],"properties":{"communicationId":{"type":"string","description":"marketing.message_dispatch id."},"sourceModule":{"type":"string","enum":["crm","ticketing","membership","waiver","groupSales","customerService","finance","wallet","resourceManagement","accessControl","other"]},"businessEvent":{"type":"string","description":"The originating event type, e.g. TicketIssued."},"businessEventId":{"type":"string","description":"The originating event instance, kept so a failed message can be replayed with its context."},"recipient":{"type":"string","description":"Address or number, masked (e.g. j***@example.com) unless the caller holds GUEST_VIEW_PII."},"subjectId":{"type":"string","format":"uuid"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"template":{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"}}},"provider":{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"}}},"priority":{"type":"string","enum":["P1","P2","P3","P4"]},"status":{"type":"string","enum":["pending","processing","sent","delivered","failed","retrying","deadLettered","cancelled"]},"attempts":{"type":"integer","minimum":0},"lastFailureCategory":{"type":"string","enum":["providerUnavailable","invalidAddress","invalidMobile","rateLimited","authenticationError","templateRejected","timeout","consentBlock","unknownError"]},"lastFailureMessage":{"type":"string"},"nextAttemptAt":{"type":"string","format":"date-time"},"createdAt":{"type":"string","format":"date-time"},"sentAt":{"type":"string","format":"date-time"}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"LocalizationBrandingCustomerExperienceConfigurationInput": {"description":"The request body of `setLocalizationBrandingCustomer`, the record itself; read-only properties are ignored.","allOf":[{"$ref":"#/components/schemas/LocalizationBrandingCustomerExperienceConfigurationView"}]},
"LocalizationBrandingCustomerExperienceConfigurationView": {"type":"object","x-ticvai-persistence":"marketing.waiver_localisation","description":"Languages, branding and channels of one waiver version (pack 11.1.9), keyed on `formId` + `formVersion`.","required":["formId","formVersion","sourceLanguage","languages"],"properties":{"formId":{"type":"string","format":"uuid"},"formVersion":{"type":"integer","minimum":1},"sourceLanguage":{"type":"string","maxLength":10,"description":"The language the legal text is written and reviewed in."},"languages":{"type":"array","minItems":1,"description":"Every language the version is offered in, the source language included. Arabic renders right to left.","items":{"type":"object","required":["language","required","translationStatus","approvalStatus"],"properties":{"language":{"type":"string","maxLength":10},"required":{"type":"boolean","description":"Publication waits for this language's approval."},"translationStatus":{"type":"string","enum":["notStarted","aiDrafted","inTranslation","inReview","complete"]},"translatorUserId":{"type":"string","format":"uuid","nullable":true},"reviewerUserId":{"type":"string","format":"uuid","nullable":true},"approvalStatus":{"type":"string","enum":["pending","approved","rejected"]},"lastUpdated":{"type":"string","format":"date-time","readOnly":true}}}},"branding":{"type":"object","properties":{"brandLogoAssetId":{"type":"string","format":"uuid","nullable":true},"venueLogoAssetId":{"type":"string","format":"uuid","nullable":true},"themeId":{"type":"string","nullable":true,"description":"The white-label theme it takes colours and typography from."},"header":{"$ref":"#/components/schemas/LocalisedText"},"footer":{"$ref":"#/components/schemas/LocalisedText"},"customerInstructions":{"$ref":"#/components/schemas/LocalisedText"},"confirmationMessage":{"$ref":"#/components/schemas/LocalisedText"},"supportEmail":{"type":"string","format":"email","nullable":true},"supportPhone":{"type":"string","maxLength":30,"nullable":true}}},"channels":{"type":"array","items":{"type":"string","enum":["b2cWeb","mobileApp","emailLink","qrLink","kiosk","posFrontDesk","groupPortal"]},"description":"Where the waiver is offered; every channel renders the same version and rules."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"MarketingSubscription": {"type":"object","x-ticvai-persistence":"marketing.subscription","x-ticvai-retired-columns":["guest_id","subscribed"],"description":"**Drafted 4 September.** What a guest asked to receive. **Deliberately separate from `marketing.consent`** - consent is what the law allows, a subscription is what the person wants, and a system that stores one and reports the other is the reason unsubscribe links stop working.","required":["id","subjectId","channel","listName","isSubscribed"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","readOnly":true,"description":"The guest — from the guest session, or from `unsubscribeToken` when there is no session."},"channel":{"type":"string","enum":["email","sms","push"]},"listName":{"type":"string"},"isSubscribed":{"type":"boolean"},"source":{"type":"string","description":"Where the opt-in happened, because a regulator asks."},"unsubscribeToken":{"writeOnly":true,"type":"string","description":"**Unsubscribe must work without a login.** The link in a message carries the token and `setMarketingSubscription` accepts it in place of a session. **Write-only: never returned**, so a `MARKETING_VIEW` holder reading subscriptions cannot act as the guest."},"updatedAt":{"readOnly":true,"type":"string","format":"date-time"}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MessageDispatch": {"x-ticvai-append-only":"queuedAt","x-ticvai-persistence":"marketing.message_dispatch","type":"object","required":["id","subjectId","channel","status","queuedAt"],"properties":{"id":{"type":"string"},"subjectId":{"type":"string","format":"uuid"},"campaignId":{"type":"string","format":"uuid","nullable":true},"channel":{"$ref":"#/components/schemas/MessageChannel"},"templateId":{"type":"string","format":"uuid"},"messageTriggerId":{"type":"string","format":"uuid","nullable":true,"description":"The `MessageTrigger` that fired it, and through its `event` the `BusinessEvent` and source module; null for a campaign or a direct send. Attempts are in `MessageDispatchAttempt`. (decided 29 September, data model for the agreed operations)"},"campaignVariantId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"marketing.campaign_variant","description":"The A/B variant sent (22.1.17; 29 September, build pass, group G2). Null for a single-content campaign or a triggered message."},"plannedSendAt":{"type":"string","format":"date-time","nullable":true,"description":"The per-recipient hour chosen by `sendTimeMode` `optimised` (22.3.19, 22.9.16); null when sent at the scheduled time."},"status":{"type":"string","enum":["queued","sent","delivered","opened","clicked","bounced","failed","suppressed"]},"failureReason":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true},"queuedAt":{"type":"string","format":"date-time"},"deliveredAt":{"type":"string","format":"date-time","nullable":true},"isTest":{"type":"boolean","default":false,"description":"A `testSendCampaign` message. Excluded from `CampaignPerformance` and `Campaign.sentCount`."},"openedAt":{"type":"string","format":"date-time","nullable":true,"description":"From the provider's engagement events. `CampaignPerformance.opened` counts these."},"clickedAt":{"type":"string","format":"date-time","nullable":true},"complainedAt":{"type":"string","format":"date-time","nullable":true},"unsubscribedAt":{"type":"string","format":"date-time","nullable":true}}},
"MessageTemplate": {"x-ticvai-persistence":"marketing.message_template","type":"object","required":["id","code","name","channel","bodies"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"channel":{"$ref":"#/components/schemas/MessageChannel"},"subjects":{"type":"object","description":"Per language. Email only.","additionalProperties":{"type":"string"}},"bodies":{"type":"object","description":"Per language, keyed by ISO 639-1 code.","additionalProperties":{"type":"string"}},"mergeFields":{"type":"array","items":{"type":"string"}},"missingLanguages":{"type":"array","readOnly":true,"description":"Enabled languages without a body. Flagged rather than silently falling back — a guest receiving English when they chose Arabic is a defect.\n","items":{"type":"string"}},"providerTemplateId":{"type":"string","nullable":true,"description":"Required for WhatsApp, where templates are pre-approved by the provider."},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand whose identity the template carries; null for the tenant default."},"ownership":{"type":"string","enum":["platform","crm"],"default":"crm","description":"`platform` = a transactional template owned by the communication service; `crm` = a marketing template owned by CRM (`listSystemTransactionalTemplate`). Content by language and version is in `MessageTemplateVersion`. (decided 29 September, data model for the agreed operations)"}}},
"MessageTrigger": {"type":"object","x-ticvai-persistence":"marketing.message_trigger","description":"**What fires a message.** Before, during and after a visit are one mechanism with a different sign on the offset.\n","required":["id","event","templateId","isActive"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"event":{"type":"string","description":"The platform event that fires it — `order.completed`, `access.validated`, `queue.turnApproaching`. **Named from the event catalogue** (`BusinessEvent.eventType`), so a trigger cannot bind to something nothing publishes. Its conditions are `MessageTriggerCondition` rows.\n**`entitlement.expiringSoon` is in the catalogue since 29 September** (build pass, group G2; 5.5.30): the pre-expiry reminder for a ticket or pass. Its anchor is the event time; the notice period is the template's `expiryNoticeDays`, so `offsetMinutes` is normally 0.\n"},"templateId":{"type":"string","format":"uuid"},"offsetMinutes":{"type":"integer","default":0,"description":"Negative fires before the anchor, positive after. **A reminder the day before a visit is -1440 against the performance**, not a separate concept.\n"},"anchor":{"type":"string","enum":["eventTime","performanceStart","visitEnd"],"default":"eventTime"},"priority":{"type":"string","enum":["operational","transactional","marketing"],"default":"transactional","description":"**A queue-turn alert and a monthly newsletter are not the same urgency and were the same dispatch.** `operational` bypasses batching and quiet hours; `marketing` never does.\n"},"sendTimeMode":{"type":"string","enum":["fixed","optimised"],"default":"fixed","description":"**Only for `priority` `marketing`** (29 September, build pass, group G2; 22.9.16): `optimised` holds the notification to the recipient's suggested hour from `ai.requestSuggestion` (kind `sendTime`) within the next 24 hours, on the suggested consented channel. `operational` and `transactional` messages are never delayed for it, and a `setMessageTrigger` asking for it on them is refused (400)."},"isActive":{"type":"boolean","default":true},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"ProviderHealthUsageCostMonitoringView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.message_dispatch, marketing.message_dispatch_attempt (new), marketing.communication_provider (new)","description":"Provider reliability, usage and cost for the window and filters.","required":["windowFrom","windowTo","volume","providers"],"properties":{"windowFrom":{"type":"string","format":"date-time"},"windowTo":{"type":"string","format":"date-time"},"volume":{"type":"integer","minimum":0},"successRate":{"type":"number","minimum":0,"maximum":1},"failureRate":{"type":"number","minimum":0,"maximum":1},"averageDeliverySeconds":{"type":"number","minimum":0},"averageApiLatencySeconds":{"type":"number","minimum":0},"availabilityRate":{"type":"number","minimum":0,"maximum":1},"retries":{"type":"integer","minimum":0},"fallbackCount":{"type":"integer","minimum":0,"description":"Messages delivered through a fallback provider or channel."},"cost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"costPerMessage":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"providers":{"type":"array","description":"Provider comparison.","items":{"type":"object","required":["providerId","channel","volume"],"properties":{"providerId":{"type":"string","format":"uuid"},"providerName":{"type":"string"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"volume":{"type":"integer","minimum":0},"successRate":{"type":"number","minimum":0,"maximum":1},"averageDeliverySeconds":{"type":"number","minimum":0},"costPerThousand":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"health":{"type":"string","enum":["healthy","warning","critical"]}}}},"breakdown":{"type":"array","description":"Usage and cost per value of the groupBy dimension.","items":{"type":"object","required":["key","volume"],"properties":{"key":{"type":"string","description":"The dimension value's id or code."},"label":{"type":"string"},"volume":{"type":"integer","minimum":0},"cost":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"alerts":{"type":"array","items":{"type":"object","required":["kind","message","raisedAt"],"properties":{"kind":{"type":"string","enum":["budgetThreshold","successRateBelowTarget","latencyAboveTarget","slaBreach"]},"message":{"type":"string"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"providerId":{"type":"string","format":"uuid"},"raisedAt":{"type":"string","format":"date-time"}}}},"slaTargets":{"type":"array","description":"Contractual provider targets, only where configured.","items":{"type":"object","required":["providerId","metric","target"],"properties":{"providerId":{"type":"string","format":"uuid"},"metric":{"type":"string","enum":["successRate","availabilityRate","averageDeliverySeconds"]},"target":{"type":"number"},"observed":{"type":"number"},"met":{"type":"boolean"}}}},"aiRecommendations":{"type":"array","description":"Advisory provider changes on cost/performance trade-offs.","items":{"type":"string"}}}},
"RoutingPriorityThrottlingFallbackRulesView": {"type":"object","x-ticvai-persistence":"marketing.communication_routing_rule","description":"One routing rule, read by listRoutingPriorityThrottling and written by setCommunicationRoutingRule. Unset selectors match anything; a rule with more selectors set is more specific.\n","required":["id","channel","providers","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"channel":{"$ref":"#/components/schemas/MessageChannel"},"country":{"type":"string","pattern":"^[A-Z]{2}$"},"brandId":{"type":"string","format":"uuid"},"messageClass":{"type":"string","enum":["transactional","operational","service","marketing"]},"priorityClass":{"type":"string","enum":["P1","P2","P3","P4"]},"recipientType":{"type":"string","enum":["customer","partner","employee"]},"providers":{"type":"array","description":"Tried in order; a provider below minimum health is skipped.","items":{"type":"object","required":["providerId","role"],"properties":{"providerId":{"type":"string","format":"uuid"},"providerName":{"type":"string","readOnly":true},"role":{"type":"string","enum":["primary","secondary","emergencyFallback"]}}}},"skipUnhealthyProviders":{"type":"boolean","description":"Route past providers whose health is degraded or worse."},"costAware":{"type":"boolean","description":"Among providers meeting the service and compliance rules, prefer the cheapest."},"channelFallback":{"type":"array","description":"Alternate channels, in order, when delivery on this channel fails; used only where consent and preferences permit.","items":{"$ref":"#/components/schemas/MessageChannel"}},"throttle":{"type":"object","properties":{"messagesPerSecond":{"type":"integer","minimum":1},"messagesPerMinute":{"type":"integer","minimum":1},"brandMessagesPerMinute":{"type":"integer","minimum":1,"description":"Cap across every rule for the same brand."},"eventMessagesPerMinute":{"type":"integer","minimum":1,"description":"Cap per originating business event."}}},"isActive":{"type":"boolean"},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"Suppression": {"x-ticvai-persistence":"marketing.suppression","type":"object","required":["channel","address","reason","suppressedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"address":{"type":"string"},"reason":{"type":"string"},"suppressedAt":{"type":"string","format":"date-time"},"suppressedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"SystemTransactionalTemplateRegistryView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.message_template, marketing.message_template_version (new), marketing.message_trigger","description":"One version of one template on one channel and language, with its content and variables.","required":["templateId","code","name","channel","language","version","status","ownership"],"properties":{"templateId":{"type":"string","format":"uuid","description":"marketing.message_template id."},"code":{"type":"string","description":"The human template ID (e.g. TICKET_CONFIRMATION)."},"name":{"type":"string"},"businessEvent":{"type":"string","description":"The registered business event this template answers (e.g. TicketIssued)."},"sourceModule":{"type":"string","enum":["crm","ticketing","membership","waiver","groupSales","customerService","finance","wallet","resourceManagement","accessControl","other"]},"channel":{"$ref":"#/components/schemas/MessageChannel"},"brandId":{"type":"string","format":"uuid"},"language":{"type":"string","description":"BCP 47 tag."},"version":{"type":"integer","minimum":1},"status":{"type":"string","enum":["draft","published","archived"]},"ownership":{"type":"string","enum":["platform","crm"],"description":"platform = transactional template owned here; crm = marketing template owned by CRM."},"subject":{"type":"string"},"header":{"type":"string"},"body":{"type":"string"},"footer":{"type":"string"},"ctaLabel":{"type":"string"},"ctaUrl":{"type":"string","description":"May contain variables, e.g. {{TicketLink}}."},"attachmentKinds":{"type":"array","items":{"type":"string","enum":["ticketPdf","invoicePdf","walletPass","calendarInvite","waiverPdf"]}},"variables":{"type":"array","description":"Dynamic variables the content uses (e.g. CustomerName, OrderNumber, EventDate, AmountDue).","items":{"type":"string"}},"publishedAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time"}}}
}
```
