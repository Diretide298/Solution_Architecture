# WS141 — Marketing CRM Configuration Reference v1.0 board 7

**10 screens · 19 operations · 25 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `AI_CONFIGURE, AI_USE, CASE_MANAGE, CASE_VIEW, GUEST_VIEW`. A control nobody can use must say so,
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
| `BO-794` | Omnichannel Command Center | B–D | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-795` | Unified Inbox | B–D | 0 | 0 | 6 | 4 | 0 | 0 | — | notStarted (—) |
| `BO-796` | Guest Conversation 360 | B–D | 0 | 0 | 6 | 3 | 1 | 0 | — | notStarted (—) |
| `BO-797` | AI Chatbot Configuration | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-798` | Intent & Knowledge Management | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-799` | Agent Workspace | B–D | 0 | 0 | 6 | 8 | 0 | 0 | — | notStarted (—) |
| `BO-800` | Routing & Queue Management | B–D | 8 | 13 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `BO-801` | Sales & Service Actions | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-802` | Sentiment, Quality & Escalation | B–D | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-803` | Chat Analytics & Audit | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-794, BO-795, BO-796, BO-797, BO-798, BO-799, BO-801, BO-802, BO-803 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-794` Omnichannel Command Center

**Monitor conversation demand, service level and commercial contribution. Show open, waiting, SLA-risk and escalated conversations, bot containment, agent handover, response and resolution time. Display CSAT, conversions, revenue and queue/channel/venue distribution with trend and capacity indicators. Surface outages, knowledge gaps, negative sentiment spikes and overloaded queues. Provide role-specific drill-down for supervisors, agents, sales, support and administrators. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/omnichannel-command-center-bo-794` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| State | select | — | With assistant · Queued · With agent · Waiting on guest · Resolved · Abandoned · Timed out | `listConversations` ?state |
| Assigned to me | toggle | — | — | `listConversations` ?assignedToMe |
| Channel | select | — | Web chat · In app chat · Whatsapp · SMS · Email · Kiosk · Voice | `listConversations` ?channel |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listConversations` (onLoad, Conversations across channels)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-795` Unified Inbox: *Unified Inbox*; carries `conversationId`
- → `BO-796` Guest Conversation 360: *Guest Conversation 360*; carries `conversationId`
- → `BO-797` AI Chatbot Configuration: *AI Chatbot Configuration*
- → `BO-798` Intent & Knowledge Management: *Intent & Knowledge Management*
- → `BO-799` Agent Workspace: *Agent Workspace*; carries `conversationId`
- → `BO-800` Routing & Queue Management: *Routing & Queue Management*
- → `BO-801` Sales & Service Actions: *Sales & Service Actions*
- → `BO-802` Sentiment, Quality & Escalation: *Sentiment, Quality & Escalation*; carries `caseId`
- → `BO-803` Chat Analytics & Audit: *Chat Analytics & Audit*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The omnichannel list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the omnichannel untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No omnichannel yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the omnichannel are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listConversations` → `CASE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.8.1 | Omnichannel Inbox | Marketing & CRM | CONTRACTED | `listConversations` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-794` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-794`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 7
- Flow F250 *Marketing CRM Configuration Reference v1.0 board 7: Omnichannel Command Center*, step 1: Opens Omnichannel Command Center → Monitor conversation demand, service level and commercial contribution. Show open, waiting, SLA-risk and escalated conversations, bot containment, agent handover, response and resolution time. …
- Flow F250 *Marketing CRM Configuration Reference v1.0 board 7: Omnichannel Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F250 *Marketing CRM Configuration Reference v1.0 board 7: Omnichannel Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F250 *Marketing CRM Configuration Reference v1.0 board 7: Omnichannel Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F250 *Marketing CRM Configuration Reference v1.0 board 7: Omnichannel Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F250 *Marketing CRM Configuration Reference v1.0 board 7: Omnichannel Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F250 *Marketing CRM Configuration Reference v1.0 board 7: Omnichannel Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F250 *Marketing CRM Configuration Reference v1.0 board 7: Omnichannel Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F250 branch at step 1 (expected): when Nothing has been set up on Omnichannel Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F250 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-794?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-795`, `BO-796`, `BO-797`, `BO-798`, `BO-799`, `BO-800`, `BO-801`, `BO-802`, `BO-803`.
- [ ] Every gated control is gated: `CASE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-795` Unified Inbox

**Consolidate all guest conversations into one manageable queue. Ingest email, SMS, WhatsApp, social, webchat, mobile-app chat and supported voice/messaging channels. Provide queue and channel filters, assignment, priority, unread state, SLA clock, search and saved views. Display the active conversation, rich messages, attachments, delivery/read status and internal notes. Prevent duplicate threads through identity and conversation correlation and retain the source channel. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_MANAGE`, `CASE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `conversationId` (navigation) |
| Route | `/engagement-support/unified-inbox-bo-795` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| State | select | — | With assistant · Queued · With agent · Waiting on guest · Resolved · Abandoned · Timed out | `listConversations` ?state |
| Assigned to me | toggle | — | — | `listConversations` ?assignedToMe |
| Channel | select | — | Web chat · In app chat · Whatsapp · SMS · Email · Kiosk · Voice | `listConversations` ?channel |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Claim conversation (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listConversations` (onLoad, The unified inbox)

**Where the user goes next**

- → `BO-794` Omnichannel Command Center: *Back to Omnichannel Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The unified list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the unified untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No unified yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the unified are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already claimed by another agent |

#### Permissions

- `listConversations` → `CASE_VIEW` (read) · staff
- `claimConversation` → `CASE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.8.1 | Omnichannel Inbox | Marketing & CRM | CONTRACTED | `listConversations` |
| 22.8.6 | Agent Workspace | Marketing & CRM | CONTRACTED | `claimConversation` |
| 22.8.17 | Conversation Routing | Marketing & CRM | CONTRACTED | `claimConversation` |
| 22.8.18 | Queue Management | Marketing & CRM | CONTRACTED | `claimConversation` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-795` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-795`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 7
- Flow F250 *Marketing CRM Configuration Reference v1.0 board 7: Omnichannel Command Center*, step 2: Works in Unified Inbox → Consolidate all guest conversations into one manageable queue. Ingest email, SMS, WhatsApp, social, webchat, mobile-app chat and supported voice/messaging channels. Provide queue and channel filters …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-795?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Claim conversation, Cancel.
- [ ] Every transition is wired: `BO-794`.
- [ ] Every gated control is gated: `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-796` Guest Conversation 360

**Combine conversation history with the identified guest's CRM context. Resolve the guest and display profile, value, tickets, reservations, membership, loyalty, wallet and open cases. Configuration Scope of Work / Version 1.0 36 Show all prior conversations across channels in chronological order with intent, outcome and agent/bot ownership. Allow authorized users to open linked records without losing the current conversation. Mask or restrict sensitive information and show confidence when identity is uncertain. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW`, `GUEST_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `conversationId` (navigation), `guestId` (navigation) |
| Route | `/engagement-support/guest-conversation-360-bo-796` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Where the user goes next**

- → `BO-794` Omnichannel Command Center: *Back to Omnichannel Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest conversation 360 list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest conversation 360 untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest conversation 360 yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the guest conversation 360 are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getConversation` → `CASE_VIEW` (read) · staff
- `getGuestTimeline` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.3.8 | Omnichannel Communication Tracking | Marketing & CRM | CONTRACTED | `getConversation` |
| 22.8.2 | Guest Conversation History | Marketing & CRM | CONTRACTED | `getConversation` |
| 22.8.26 | Conversation Audit Trail | Marketing & CRM | CONTRACTED | `getConversation` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The AI chat box answers guided/predefined queries (booking status, rescheduling) and logs guest conversation history across channels (WhatsApp, web, Instagram, Facebook) with per-channel conversion attribution. *(client request · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-388)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-796` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-796`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 7
- Flow F250 *Marketing CRM Configuration Reference v1.0 board 7: Omnichannel Command Center*, step 4: Works in Guest Conversation 360 → Combine conversation history with the identified guest's CRM context. Resolve the guest and display profile, value, tickets, reservations, membership, loyalty, wallet and open cases. Configuration …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-796?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-794`.
- [ ] Every gated control is gated: `CASE_VIEW`, `GUEST_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-797` AI Chatbot Configuration

**Configure the AI assistant's identity, scope and operating controls. Set bot name, personality, tone, supported languages, channels, operating hours and brand/venue context. Configure confidence thresholds, fallback, authentication, guest-data access and maximum automated turns. Define permitted sales/service actions, prohibited topics, safe responses and human-handover conditions. Version, approve, test and audit configuration before deployment to any channel. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/ai-chatbot-configuration-bo-797` |

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

- → `BO-794` Omnichannel Command Center: *Back to Omnichannel Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The chatbot list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the chatbot untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No chatbot yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the chatbot are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A venue row would widen the tenant's configuration or the AI policy. |

#### Permissions

- `setCustomerServiceCopilot` → `AI_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The AI chat box answers guided/predefined queries (booking status, rescheduling) and logs guest conversation history across channels (WhatsApp, web, Instagram, Facebook) with per-channel conversion attribution. *(client request · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-388)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-797` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-797`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 7
- Flow F250 *Marketing CRM Configuration Reference v1.0 board 7: Omnichannel Command Center*, step 6: Works in AI Chatbot Configuration → Configure the AI assistant's identity, scope and operating controls. Set bot name, personality, tone, supported languages, channels, operating hours and brand/venue context. Configure confidence …
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-797?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-794`.
- [ ] Every gated control is gated: `AI_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-798` Intent & Knowledge Management

**Manage what the assistant understands and the information it may use. Maintain intents, example phrases, entities, synonyms, redirects, confidence and response variants. Connect approved FAQs, product data, policies, manuals and structured knowledge with freshness and ownership. Provide test console, expected result, source citation, ambiguity handling and low-confidence review queue. Track knowledge consumers, sync status, changes and answer-quality feedback. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_CONFIGURE`, `AI_USE` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/intent-knowledge-management-bo-798` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Open · Assigned · Answered · Dismissed | `listKnowledgeGaps` ?status |
| Kind | segmented control | — | Knowledge · Analytics | `listKnowledgeGaps` ?kind |
| Audience | segmented control | — | Staff · Guest | `listKnowledgeGaps` ?audience |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listKnowledgeGaps` (onLoad, Questions the assistant could not answer)

**Where the user goes next**

- → `BO-794` Omnichannel Command Center: *Back to Omnichannel Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The intent knowledge list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the intent knowledge untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No intent knowledge yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the intent knowledge are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A venue row would widen the tenant's configuration or the AI policy. |

#### Permissions

- `setCustomerServiceCopilot` → `AI_CONFIGURE` (configure) · staff
- `listKnowledgeGaps` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-798` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-798`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 7
- Flow F250 *Marketing CRM Configuration Reference v1.0 board 7: Omnichannel Command Center*, step 8: Works in Intent & Knowledge Management → Manage what the assistant understands and the information it may use. Maintain intents, example phrases, entities, synonyms, redirects, confidence and response variants. Connect approved FAQs …
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-798?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-794`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-799` Agent Workspace

**Give live agents the context and tools required to resolve conversations efficiently. Provide active conversation, transcript, guest context, AI reply suggestion, canned responses and translation. Support rich messages, attachments, internal notes, tags, tasks, transfer and supervisor assistance. Expose authorized ticket, reservation, membership, loyalty, wallet and case actions without switching applications. Track agent presence, typing, ownership, response time, action outcomes and complete transcript history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work / Version 1.0 37**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `conversationId` (navigation) |
| Route | `/engagement-support/agent-workspace-bo-799` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Send conversation message (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-794` Omnichannel Command Center: *Back to Omnichannel Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The agent list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the agent untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No agent yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the agent are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 No agent available. Returns the reason and offers a case, rather than queuing a guest for somebody who is not there. (HandoverRefusedProblem) |

#### Permissions

- `sendConversationMessage` → `CASE_MANAGE` (configure) · staff, guest
- `handoverToAgent` → no permission · guest
- `setCallDisposition` → `CASE_MANAGE` (configure) · staff
- `startKioskAssist` → `CASE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.8.20 | Rich Messaging Support | Marketing & CRM | CONTRACTED | `sendConversationMessage` |
| 22.8.22 | Payment Link Integration | Marketing & CRM | CONTRACTED | `sendConversationMessage` |
| 22.8.24 | Mobile App Chat Center | Marketing & CRM | CONTRACTED | `sendConversationMessage` |
| 19.2.67 | Live Chat - System shall support live chat. | Guest Mobile App & Branding | CONTRACTED | `handoverToAgent` |
| 19.2.68 | AI Chat Assistant - System shall provide AI chat assistance. | Guest Mobile App & Branding | CONTRACTED | `handoverToAgent` |
| 19.2.72 | AI Concierge - System shall provide AI concierge services. | Guest Mobile App & Branding | CONTRACTED | `handoverToAgent` |
| 22.8.5 | Live Agent Handover | Marketing & CRM | CONTRACTED | `handoverToAgent` |
| 2.1.25 | Authorized staff shall be able to remotely assist guests using self-service kiosks, troubleshoot issues, and support checkout completion. | Ticketing Sales | CONTRACTED | `startKioskAssist` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-799` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-799`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 7
- Flow F250 *Marketing CRM Configuration Reference v1.0 board 7: Omnichannel Command Center*, step 10: Works in Agent Workspace → Give live agents the context and tools required to resolve conversations efficiently. Provide active conversation, transcript, guest context, AI reply suggestion, canned responses and translation. …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-799?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Send conversation message, Cancel.
- [ ] Every transition is wired: `BO-794`.
- [ ] Every gated control is gated: `CASE_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-800` Routing & Queue Management

**Route work to the correct team and balance workload. Create rules by intent, skill, department, venue, attraction, language, guest tier, priority and SLA risk. Configure queues, capacity, operating hours, overflow, assignment method, workload limits and fallback. Provide live queue counts, wait time, agent utilization, reassignment, pickup and supervisor override. Record the evaluated rule, routing reason, transfers and any manual intervention. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_MANAGE`, `CASE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/routing-queue-management-bo-800` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Parent category id | picker: choose a parent category (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?parentCategoryId=` to `listCaseCategories`. | `listCaseCategories` ?parentCategoryId |
| Top level only | toggle | optional | off | — | — | Sends `?topLevelOnly=` to `listCaseCategories`. | `listCaseCategories` ?topLevelOnly |
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listCaseCategories`. | `listCaseCategories` ?isActive |
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listServiceQueues`. | `listServiceQueues` ?isActive |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Queue | picker: choose a queue | — | — | `listAgentWorkloadAvailability` ?queueId |
| Team | text field | — | max length 100 | `listAgentWorkloadAvailability` ?team |
| Status | select | — | Available · Busy · On call · Chatting · After call work · Break · Training · Offline | `listAgentWorkloadAvailability` ?status |
| Skill | text field | — | max length 60 | `listAgentWorkloadAvailability` ?skill |
| Language | text field | — | max length 10 | `listAgentWorkloadAvailability` ?language |

**Form: Save service queue definition** (modal, opened by *Save service queue definition*; *Save service queue definition* calls `setServiceQueueDefinition`, *Cancel* sends nothing)

**Collects what `setServiceQueueDefinition` sends before it is called.** Required: `id`, `code`, `name`, `isActive`. Optional: `overflowWaitSeconds`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 60 | — | — | `setServiceQueueDefinition` body |
| Name `name` | text field | required | — | max length 150 | — | — | `setServiceQueueDefinition` body |
| Overflow wait seconds `overflowWaitSeconds` | number field (seconds) | optional | — | min 0 | — | The queue's overflow threshold; a case waiting longer marks the queue `critical`. | `setServiceQueueDefinition` body |
| Is active `isActive` | toggle | required | on | — | — | — | `setServiceQueueDefinition` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Retiring a queue that an active routing rule names, or that an unresolved case still waits in.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Every case category** (data table, from `listCaseCategories`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Parent category | the name it points at, never the id | Set on a subcategory; null on a top-level category. |
| Default priority | chip: Low, Normal, High, Urgent | The priority a case in this category starts at before routing factors apply. |
| Is active | yes / no (icon or chip) | — |
| Scope path | text | The partition key (ADR-0005). |

**Every service queue** (data table, from `listServiceQueues`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Overflow wait seconds | 1,234 | The queue's overflow threshold; a case waiting longer marks the queue `critical`. |
| Is active | yes / no (icon or chip) | — |
| Scope path | text | The partition key (ADR-0005). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Save service queue definition (primary button) | `setServiceQueueDefinition` PUT `/service-queues` | ServiceQueue | ServiceQueue | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Retiring a queue that an active routing rule names, or that an unresolved case still waits in. | gated `CASE_MANAGE`; opens modal first |

**Data it reads**: `listAgentWorkloadAvailability` (onLoad, Who is free); `listCaseCategories` (onLoad, List case categories and subcategories); `listServiceQueues` (onLoad, List customer-service queues)

**Where the user goes next**

- → `BO-794` Omnichannel Command Center: *Back to Omnichannel Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The routing queue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the routing queue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No routing queue yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the routing queue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types.; 409 Retiring a queue that an active routing rule names, or that an unresolved case still waits in. |

#### Permissions

- `setIntelligentRoutingSkill` → `CASE_MANAGE` (configure) · staff
- `listAgentWorkloadAvailability` → `CASE_VIEW` (read) · staff
- `listCaseCategories` → `CASE_VIEW` (read) · staff
- `listServiceQueues` → `CASE_VIEW` (read) · staff
- `setServiceQueueDefinition` → `CASE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Routing/queue configuration (reservation, general, membership & billing, technical support queues with priority and SLA policy) routes AI-agent conversations by detected query intent. *(agreed · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-389)*
- Decision: data retention/archival (e.g. 3–5 years live before archival) and chat/case conversation retention (e.g. default one month, extendable) are configurable per tenant/venue at setup, with system defaults admins can override. *(agreed · MoM 20 Aug 2026, 4.3 Consent; 4.8 AI Chat Box; 5. Key Decisions · DI-380)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-800` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-800`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 7
- Flow F250 *Marketing CRM Configuration Reference v1.0 board 7: Omnichannel Command Center*, step 12: Works in Routing & Queue Management → Route work to the correct team and balance workload. Create rules by intent, skill, department, venue, attraction, language, guest tier, priority and SLA risk. Configure queues, capacity, operating …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (13 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-800?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel, Save service queue definition.
- [ ] Every transition is wired: `BO-794`.
- [ ] Every gated control is gated: `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-801` Sales & Service Actions

**Allow agents and AI to perform governed transactional actions. Create or modify tickets and reservations and view capacity, eligibility, price and policy before confirmation. Manage membership information, loyalty rewards and wallet top-ups within configured authority. Generate secure payment links, vouchers, QR tickets, forms and rich messages and confirm delivery. Create and escalate cases and require authentication, approval or live-agent control for sensitive actions. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/sales-service-actions-bo-801` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save order booking ticket (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-794` Omnichannel Command Center: *Back to Omnichannel Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sales service actions list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sales service actions untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sales service actions yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the sales service actions are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types.; 422 The action is not permitted for this order under its policies; the problem names the policy. |

#### Permissions

- `setOrderBookingTicket` → `CASE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-801` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-801`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 7
- Flow F250 *Marketing CRM Configuration Reference v1.0 board 7: Omnichannel Command Center*, step 14: Works in Sales & Service Actions → Allow agents and AI to perform governed transactional actions. Create or modify tickets and reservations and view capacity, eligibility, price and policy before confirmation. Manage membership …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-801?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save order booking ticket, Cancel.
- [ ] Every transition is wired: `BO-794`.
- [ ] Every gated control is gated: `CASE_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-802` Sentiment, Quality & Escalation

**Detect conversation risk and support consistent service quality. Analyze sentiment, emotion, urgency, intent confidence, compliance and quality score in near real time. Configure thresholds for supervisor alert, priority change, queue transfer, case creation or live- agent takeover. Provide transcript review, AI rationale, quality checklist, coaching notes and appeal/override controls. Monitor false positives, bias, model drift and outcomes and audit automated and human escalations. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_MANAGE`, `CASE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `caseId` (navigation) |
| Route | `/engagement-support/sentiment-quality-escalation-bo-802` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Agent principal | picker: choose an agent principal | — | — | `listQualityAgentEvaluation` ?agentPrincipalId |
| Evaluator principal | picker: choose an evaluator principal | — | — | `listQualityAgentEvaluation` ?evaluatorPrincipalId |
| Source type | select | — | Call · Chat · Email · Whatsapp · Case · Complaint | `listQualityAgentEvaluation` ?sourceType |
| Status | segmented control | — | Draft · Scored · Acknowledged | `listQualityAgentEvaluation` ?status |
| Critical failure only | toggle | — | — | `listQualityAgentEvaluation` ?criticalFailureOnly |
| From | date and time picker | — | — | `listQualityAgentEvaluation` ?from |
| To | date and time picker | — | — | `listQualityAgentEvaluation` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listQualityAgentEvaluation` (onLoad, Sentiment, quality and escalation)

**Where the user goes next**

- → `BO-794` Omnichannel Command Center: *Back to Omnichannel Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sentiment quality escalation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sentiment quality escalation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sentiment quality escalation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the sentiment quality escalation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listQualityAgentEvaluation` → `CASE_VIEW` (read) · staff
- `escalateCase` → `CASE_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.3.6 | Case Escalation Management | Marketing & CRM | CONTRACTED | `escalateCase` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-802` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-802`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 7
- Flow F250 *Marketing CRM Configuration Reference v1.0 board 7: Omnichannel Command Center*, step 16: Works in Sentiment, Quality & Escalation → Detect conversation risk and support consistent service quality. Analyze sentiment, emotion, urgency, intent confidence, compliance and quality score in near real time. Configure thresholds for …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-802?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-794`.
- [ ] Every gated control is gated: `CASE_MANAGE`, `CASE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-803` Chat Analytics & Audit

**Measure channel, chatbot and agent performance and preserve conversation evidence. Report volume, response, resolution, abandonment, containment, handover, transfer, conversion, revenue and CSAT. Compare channel, queue, venue, intent, language, bot version, agent and time period. Configuration Scope of Work / Version 1.0 38 Provide conversation drill-down, action trace, AI/human ownership, case links and payment/sales outcome. Audit messages, transfers, AI actions, escalations, administrative changes and data access. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work / Version 1.0 39 Board 8 - Case Management, SLA & Service Recovery Figure 8. High-definition configuration board with all 10 screens. Configuration Scope of Work / Version 1.0 40**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/chat-analytics-audit-bo-803` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Subject | picker: choose a subject | — | — | `listUnifiedInteractionCommunication` ?subjectId |
| Keyword | text field | — | min length 2; max length 200 | `listUnifiedInteractionCommunication` ?keyword |
| From | date and time picker | — | — | `listUnifiedInteractionCommunication` ?from |
| To | date and time picker | — | — | `listUnifiedInteractionCommunication` ?to |
| Channel | select | — | Email · Phone · Live chat · Whatsapp · SMS · Web form · Mobile app · B2C portal · Social · POS front desk · Internal note · Automated notification | `listUnifiedInteractionCommunication` ?channel |
| Agent principal | picker: choose an agent principal | — | — | `listUnifiedInteractionCommunication` ?agentPrincipalId |
| Case | picker: choose a case | — | — | `listUnifiedInteractionCommunication` ?caseId |
| Order | picker: choose an order | — | — | `listUnifiedInteractionCommunication` ?orderId |
| Ticket | text field | — | — | `listUnifiedInteractionCommunication` ?ticketId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listUnifiedInteractionCommunication` (onLoad, Chat analytics and audit)

**Where the user goes next**

- → `BO-794` Omnichannel Command Center: *Back to Omnichannel Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The chat analytics audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the chat analytics audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No chat analytics audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the chat analytics audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listUnifiedInteractionCommunication` → `CASE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-803` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS76 Marketing CRM Configuration Reference v1.0 Board 7.dc.html#bo-803`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 7
- Flow F250 *Marketing CRM Configuration Reference v1.0 board 7: Omnichannel Command Center*, step 18: Works in Chat Analytics & Audit → Measure channel, chatbot and agent performance and preserve conversation evidence. Report volume, response, resolution, abandonment, containment, handover, transfer, conversion, revenue and CSAT. …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-803?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-794`.
- [ ] Every gated control is gated: `CASE_VIEW`.
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

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"claimConversation": {"method":"POST","path":"/conversations/{conversationId}/claim","contract":"marketing-crm","summary":"An agent takes it","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Conversation"},
"escalateCase": {"method":"POST","path":"/cases/{caseId}/escalate","contract":"marketing-crm","summary":"Escalate a case","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Case"},
"getConversation": {"method":"GET","path":"/conversations/{conversationId}","contract":"marketing-crm","summary":"One conversation and everything before it","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"Conversation"},
"getGuestTimeline": {"method":"GET","path":"/guests/{guestId}/timeline","contract":"marketing-crm","summary":"Everything this guest did, in order, across the platform","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"kinds","in":"query","required":null},{"name":"venueId","in":"query","required":null}],"requestBody":null,"responds":"GuestTimelineEvent"},
"handoverToAgent": {"method":"POST","path":"/conversations/{conversationId}/handover","contract":"marketing-crm","summary":"Pass an assistant conversation to a person","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Conversation"},
"listAgentWorkloadAvailability": {"method":"GET","path":"/agent-workload-availability","contract":"marketing-crm","summary":"Agent Workload, Availability & Workforce Control","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":false},{"name":"queueId","in":"query","required":false},{"name":"team","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"skill","in":"query","required":false},{"name":"language","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCaseCategories": {"method":"GET","path":"/case-categories","contract":"marketing-crm","summary":"List case categories and subcategories","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"parentCategoryId","in":"query","required":false},{"name":"topLevelOnly","in":"query","required":false},{"name":"isActive","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listConversations": {"method":"GET","path":"/conversations","contract":"marketing-crm","summary":"The omnichannel inbox","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"state","in":"query","required":null},{"name":"assignedToMe","in":"query","required":null},{"name":"channel","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listKnowledgeGaps": {"method":"GET","path":"/knowledge-gaps","contract":"ai","summary":"Questions the assistant could not answer","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"audience","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listQualityAgentEvaluation": {"method":"GET","path":"/quality-agent-evaluation","contract":"marketing-crm","summary":"Quality Management & Agent Evaluation","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"agentPrincipalId","in":"query","required":false},{"name":"evaluatorPrincipalId","in":"query","required":false},{"name":"sourceType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"criticalFailureOnly","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listServiceQueues": {"method":"GET","path":"/service-queues","contract":"marketing-crm","summary":"List customer-service queues","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"isActive","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listUnifiedInteractionCommunication": {"method":"GET","path":"/unified-interaction-communication","contract":"marketing-crm","summary":"Unified Interaction & Communication History","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"subjectId","in":"query","required":false},{"name":"keyword","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"agentPrincipalId","in":"query","required":false},{"name":"caseId","in":"query","required":false},{"name":"orderId","in":"query","required":false},{"name":"ticketId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"sendConversationMessage": {"method":"POST","path":"/conversations/{conversationId}/messages","contract":"marketing-crm","summary":"Say something, as a guest or an agent","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConversationMessage"},
"setCallDisposition": {"method":"POST","path":"/conversations/{conversationId}/disposition","contract":"marketing-crm","summary":"Why the conversation ended, and any callback","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CallDisposition","responds":"CallDisposition"},
"setCustomerServiceCopilot": {"method":"PUT","path":"/customer-service-copilot","contract":"marketing-crm","summary":"Configure the customer-service copilot","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiCustomerServiceCopilotKnowledgeWorkspaceInput","responds":"AiCustomerServiceCopilotKnowledgeWorkspaceView"},
"setIntelligentRoutingSkill": {"method":"PUT","path":"/intelligent-routing-skill","contract":"marketing-crm","summary":"Create or change a case routing rule","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"IntelligentRoutingSkillsAssignmentEngineInput","responds":"IntelligentRoutingSkillsAssignmentEngineView"},
"setOrderBookingTicket": {"method":"PUT","path":"/order-booking-ticket","contract":"marketing-crm","summary":"Evaluate or perform a service action on an order from a case","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OrderBookingTicketServiceWorkspaceInput","responds":"OrderBookingTicketServiceWorkspaceView"},
"setServiceQueueDefinition": {"method":"PUT","path":"/service-queues","contract":"marketing-crm","summary":"Create or change a customer-service queue","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ServiceQueue","responds":"ServiceQueue"},
"startKioskAssist": {"method":"POST","path":"/kiosk-assists","contract":"marketing-crm","summary":"A staff member helps a guest at a kiosk, remotely","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KioskAssistSession"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AgentWorkloadAvailabilityWorkforceControlView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.agent_service_profile (new), marketing.agent_availability, marketing.case, marketing.conversation, marketing.service_queue (new) and workforce.shift","description":"One agent's live status and workload. Rates are over the period since the agent's current shift started, or the venue's current day when no shift is rostered.","required":["principalId","agentName","status","activeCases"],"properties":{"principalId":{"type":"string","format":"uuid"},"agentName":{"type":"string","description":"The agent's display name."},"team":{"type":"string","nullable":true},"skills":{"type":"array","items":{"type":"string"}},"languages":{"type":"array","items":{"type":"string"}},"status":{"type":"string","enum":["available","busy","onCall","chatting","afterCallWork","break","training","offline"]},"activeCases":{"type":"integer","minimum":0},"chats":{"type":"integer","minimum":0,"description":"Conversations the agent holds now."},"calls":{"type":"integer","minimum":0,"description":"Voice conversations in progress (0 or 1)."},"queues":{"type":"array","items":{"type":"object","required":["queueId","queueName"],"properties":{"queueId":{"type":"string","format":"uuid"},"queueName":{"type":"string"}}}},"slaRiskCases":{"type":"integer","minimum":0,"description":"The agent's open cases at risk or breached."},"averageHandleSeconds":{"type":"integer","minimum":0,"nullable":true},"resolutionRate":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Cases resolved over cases handled."},"utilization":{"type":"number","minimum":0,"description":"Active cases and conversations over `maxConcurrentCases`; above 1 means overloaded."},"workloadBand":{"type":"string","enum":["available","normal","overloaded"],"description":"`overloaded` at utilization 0.9 or above, `available` below 0.5."},"availabilityExpiresAt":{"type":"string","format":"date-time","nullable":true}}},
"AiCustomerServiceCopilotKnowledgeWorkspaceInput": {"type":"object","x-ticvai-persistence":"marketing.service_copilot_config","description":"The customer-service copilot's configuration for one scope (pack 10.1.10). A field left out takes its default, not its old value.","required":["scopeLevel","dataSources","draftChannels"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopeLevel":{"type":"string","enum":["tenant","venue"]},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005), and the upsert key: one row per scope."},"isEnabled":{"type":"boolean","default":false},"dataSources":{"type":"array","description":"The authorised data the copilot may read, always within the asking agent's own permissions.","items":{"type":"string","enum":["customer","cases","orders","tickets","products","servicePolicies","pricing","payments","membership","wallet","groupBookings","interactionHistory","knowledgeBase"]}},"knowledgeCollectionIds":{"type":"array","description":"`ai.knowledge_collection` rows holding service procedures, product information, refund rules, ticket policies, venue instructions, FAQs and internal SOPs.","items":{"type":"string","format":"uuid"}},"draftChannels":{"type":"array","items":{"type":"string","enum":["email","chat","whatsapp","caseResponse","internalEscalation"]}},"brandTone":{"type":"string","maxLength":1000,"nullable":true,"description":"Tone guidance applied to every draft."},"replyInCustomerLanguage":{"type":"boolean","default":true},"autoSend":{"type":"array","default":[],"description":"Channels where an approved automation may send without an agent. Empty means every customer-facing message waits for a person.","items":{"type":"string","enum":["email","chat","whatsapp"]}},"patternDetection":{"type":"object","description":"Flags a systemic problem when many cases share one cause.","properties":{"isEnabled":{"type":"boolean","default":true},"minimumCases":{"type":"integer","minimum":2,"default":25},"windowHours":{"type":"integer","minimum":1,"maximum":720,"default":168}}},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AiCustomerServiceCopilotKnowledgeWorkspaceView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.service_copilot_config (new), ai.policy and ai.knowledge_collection","description":"The stored configuration and what is in effect at that scope after the tenant row and the AI policy are applied.","required":["configuration","effective"],"properties":{"configuration":{"$ref":"#/components/schemas/AiCustomerServiceCopilotKnowledgeWorkspaceInput"},"effective":{"type":"object","description":"The narrowest of this row, its tenant row and `getAiPolicy`.","properties":{"isEnabled":{"type":"boolean"},"dataSources":{"type":"array","items":{"type":"string"}},"draftChannels":{"type":"array","items":{"type":"string"}},"autoSend":{"type":"array","items":{"type":"string"}},"aiCapabilities":{"type":"array","description":"`AiPolicy.enabledCapabilities` at this scope.","items":{"type":"string"}}}},"knowledgeCollections":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"documentCount":{"type":"integer","minimum":0}}}}}},
"AiKnowledgeGap": {"type":"object","x-ticvai-persistence":"ai.knowledge_gap","description":"**A question the assistant could not answer**, grouped so the content owner gets a task, not a log (AIC-061, AIC-062). Also written for an analytics question outside the semantic model (design 5.7).","required":["question","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"question":{"type":"string","description":"The normalised question."},"examples":{"type":"array","items":{"type":"string"},"description":"Up to ten phrasings as asked, with personal data masked."},"occurrences":{"type":"integer","minimum":1,"readOnly":true},"audience":{"type":"string","enum":["staff","guest"]},"locale":{"type":"string","nullable":true},"kind":{"type":"string","enum":["knowledge","analytics"]},"suggestedCollectionId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.knowledge_collection"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal"},"status":{"type":"string","enum":["open","assigned","answered","dismissed"]},"resolvedDocumentId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.knowledge_document"},"lastAskedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"CallDisposition": {"type":"object","description":"BL-082. **A conversation could be closed and nothing recorded why it ended** — information, no sale, sale successful. **That is the measure a contact centre runs on**, and its absence makes every conversation look identical in a report.\n","required":["outcome"],"properties":{"outcome":{"type":"string","enum":["information","resolved","noSale","saleCompleted","callbackScheduled","escalated","wrongNumber","abandoned","unreachable"]},"callbackAt":{"type":"string","format":"date-time","nullable":true,"description":"**An agent could not schedule a callback with the case attached**, so a promise to ring back lived in somebody's notebook.\n"},"callbackAssignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"note":{"type":"string","nullable":true}}},
"Case": {"x-ticvai-persistence":"marketing.case","x-ticvai-retired-columns":["guest_name","subject","is_sla_breached"],"type":"object","required":["id","caseNumber","subject","status","priority","createdAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7."},"caseNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity. Assigned when the case reaches the server, so a retry with the same `id` keeps its number.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true},"guestName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"**Resolved from `pii.subject` when the case is read, never stored on the case.** A name copied onto a case row is personal data outside the erasable store (ADR-0023), and it had no source anyway — no request carries it. Returned only to callers holding `GUEST_VIEW_PII`, as `searchGuests` does.\n"},"subject":{"type":"string","x-ticvai-column":"title","description":"**The case's one-line title**, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps `subject` because screens bind it.\n"},"kind":{"allOf":[{"$ref":"#/components/schemas/CaseKind"}],"nullable":true,"description":"What the guest said it was about, where the guest raised it."},"channel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"description":"How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`."},"recordedAt":{"type":"string","format":"date-time","description":"Device time the case was raised — the start of the SLA clock."},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the case arrived. Equal to `recordedAt` for a case raised online."},"categoryId":{"type":"string","format":"uuid","nullable":true},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The `ServiceQueue` the case waits in, set by routing (`CaseRoutingRule.queueId`). Null once routed straight to an agent. (decided 29 September, data model for the agreed operations)"},"membershipId":{"type":"string","format":"uuid","nullable":true,"description":"The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. (decided 29 September, coordinator decision DM4, writers pass)"},"status":{"$ref":"#/components/schemas/CaseStatus"},"priority":{"$ref":"#/components/schemas/CasePriority"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"relatedOrderId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"isSlaBreached":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"**Computed when read, never stored.** True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` (or to now, while unresolved), less `slaPausedSeconds`, is past the target that set `slaDueAt`. A stored flag would need a job to flip it at the moment of breach, and no such job is designed; `listCases?breachedSla` filters on the same computation.\n"},"slaPausedSeconds":{"type":"integer","description":"Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock.\n"},"escalationCount":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"CaseCategory": {"type":"object","x-ticvai-persistence":"marketing.case_category","description":"**The venue's case taxonomy**: categories and, under them, subcategories (`parentCategoryId`). `Case.categoryId` and the routing rules' `match.categoryIds` point here; `createCaseClassificationIntelligent` recommends one. Maintained by `setCaseCategoryDefinition`, read by `listCaseCategories` (decided 29 September, writers pass). (decided 29 September, data model for the agreed operations)\n","required":["id","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":60},"name":{"type":"string","maxLength":150},"parentCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"Set on a subcategory; null on a top-level category."},"defaultPriority":{"allOf":[{"$ref":"#/components/schemas/CasePriority"}],"nullable":true,"description":"The priority a case in this category starts at before routing factors apply."},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CaseKind": {"type":"string","description":"**What the guest says the case is about**, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.\n**`other` only with a note (decided 28 September, audit R222).** A case raised as `other` must carry a non-empty `detail` (`raiseMyCase`), or it is refused with 400; the notes are reviewed quarterly to add the real kinds they reveal.\n","enum":["lostProperty","complaint","question","accessibility","refundRequest","other"]},
"CasePriority": {"type":"string","enum":["low","normal","high","urgent"]},
"CaseStatus": {"type":"string","enum":["open","inProgress","awaitingGuest","escalated","resolved","closed"]},
"Conversation": {"type":"object","x-ticvai-persistence":"marketing.conversation","description":"22.8. **A conversation is not a case.** A case is a ticket measured in hours; a conversation is a live session measured in seconds, with somebody waiting. A conversation may create a case; it is not one.\n","required":["id","channel","state"],"properties":{"id":{"type":"string","format":"uuid"},"telephony":{"type":"object","nullable":true,"description":"BL-083. **`ConversationChannel` included `voice` with nothing behind it** — the model anticipated telephony and stopped at the enum.\n**Not an integration, a binding.** Genesys, Avaya, Amazon Connect, Teams and 3CX all do call control themselves; what the platform needs is the call bound to the guest and the case, so **an agent who answers already knows who is calling and what about.**\n","properties":{"providerCallId":{"type":"string"},"direction":{"type":"string","enum":["inbound","outbound","transferred"]},"fromNumberMasked":{"type":"string","nullable":true,"description":"**Masked, and it is still personal data.** A phone number identifies a person more reliably than a name does.\n"},"recordingRef":{"type":"string","nullable":true,"description":"Held by the provider, referenced here. **Recording consent is jurisdictional and the platform does not assume it** — a reference with no consent record is a recording nobody may play.\n"},"agentState":{"type":"string","enum":["available","onCall","wrapUp","away","offline"],"nullable":true}}},"assistSessionId":{"type":"string","format":"uuid","nullable":true,"description":"BL-094. **`startKioskAssist` recorded a staff member helping a guest and `createCase` recorded a service interaction, and neither referenced the other** — so the traceability 2.13.20 asks for had no link to follow.\n**The link is here rather than on the assist session**, because a case may span several assists and an assist belongs to at most one case.\n"},"channel":{"$ref":"#/components/schemas/ConversationChannel"},"state":{"$ref":"#/components/schemas/ConversationState"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"22.8.3. Resolved from phone, email, membership number or a signed-in session. **A conversation with none of those stays anonymous rather than being guessed at.**\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"assignedPrincipalId":{"type":"string","format":"uuid","nullable":true},"queueId":{"type":"string","format":"uuid","nullable":true},"queuePosition":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onRead","description":"Place among the unclaimed conversations in `queueId`, from the live agent queue (audit R149). Null once claimed."},"estimatedWaitSeconds":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onRead","description":"From the live agent queue — the conversations ahead divided across that queue's agents online now (audit R149). Null once claimed."},"handoverReason":{"type":"string","nullable":true,"enum":["guestRequested","assistantRefused","assistantFailed","outOfScope","negativeSentiment","complexIntent","paymentIssue"]},"handoverSummary":{"type":"string","nullable":true,"description":"**The assistant's own account of what the guest wants**, so an agent opens with context rather than reading a transcript while somebody waits.\n"},"sentiment":{"type":"string","nullable":true,"enum":["positive","neutral","negative","escalating"],"description":"22.8.16. **`escalating` is a routing signal**, not a report line."},"intent":{"type":"string","nullable":true,"description":"22.8.13. What the guest appears to want, used for routing."},"locale":{"type":"string"},"caseId":{"type":"string","format":"uuid","nullable":true,"description":"22.8.12. Where the conversation raised one."},"messages":{"type":"array","items":{"$ref":"#/components/schemas/ConversationMessage"}},"firstResponseSeconds":{"type":"integer","nullable":true,"readOnly":true},"startedAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true},"outcome":{"type":"string","nullable":true,"enum":["resolved","caseRaised","abandonedByGuest","timedOut","spam"]}}},
"ConversationChannel": {"type":"string","enum":["webChat","inAppChat","whatsapp","sms","email","kiosk","voice"]},
"ConversationMessage": {"type":"object","x-ticvai-persistence":"marketing.conversation_message + marketing.conversation_message_attachment","required":["id","sender","body","sentAt"],"properties":{"id":{"type":"string","format":"uuid"},"sender":{"type":"string","enum":["guest","agent","assistant","system"],"description":"**Resolved, never declared.** The assistant is labelled as one — a guest talking to a bot that presents as a person is a complaint waiting for the moment they find out.\n"},"senderPrincipalId":{"type":"string","format":"uuid","nullable":true},"body":{"type":"string"},"attachments":{"type":"array","items":{"type":"object","properties":{"assetId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["image","video","document","ticket","qr","paymentLink"]}}}},"aiInteractionId":{"type":"string","format":"uuid","nullable":true,"description":"Where the assistant sent it. **Links the message to its tokens and cost**, so a conversation's spend is attributable (CF-14).\n"},"sentAt":{"type":"string","format":"date-time"},"readAt":{"type":"string","format":"date-time","nullable":true}}},
"ConversationState": {"type":"string","description":"**`withAssistant` and `queued` are different, and the second has a person waiting.** Merging them makes the service level unmeasurable, because time with a bot is not time in a queue.\n","enum":["withAssistant","queued","withAgent","waitingOnGuest","resolved","abandoned","timedOut"]},
"GuestTimelineEvent": {"type":"object","description":"Board 1.5. **Facts, notes and predictions distinguished on the row.**","properties":{"id":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"kind":{"type":"string","enum":["purchase","ticketUsed","reservation","visit","membershipChange","loyalty","wallet","campaign","message","case","survey","waiver","note","prediction"]},"nature":{"type":"string","enum":["operationalFact","userNote","aiDerived"],"description":"**A prediction and a gate scan are both useful and only one happened.**"},"summary":{"type":"string"},"channel":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"sourceContract":{"type":"string","nullable":true},"sourceReferenceId":{"type":"string","format":"uuid","nullable":true},"value":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"outcome":{"type":"string","nullable":true}}},
"IntelligentRoutingSkillsAssignmentEngineInput": {"type":"object","x-ticvai-persistence":"marketing.case_routing_rule","description":"One case routing rule (pack 10.2.3). Empty match lists match everything; all non-empty lists must match.","required":["code","name","strategy","rank","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":60,"description":"The natural key, e.g. `eventDayArabic`."},"name":{"type":"string","maxLength":150},"rank":{"type":"integer","minimum":1,"description":"Lower is tried first."},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The queue this rule routes into; null routes straight to an agent."},"match":{"type":"object","properties":{"categoryIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Case categories and subcategories (`Case.categoryId`)."},"kinds":{"type":"array","items":{"$ref":"#/components/schemas/CaseKind"}},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"customerLanguages":{"type":"array","items":{"type":"string","maxLength":10},"description":"BCP-47 tags, e.g. `ar`, `en`."},"customerTypes":{"type":"array","items":{"type":"string","enum":["individual","member","vip","corporate","group","partner"]}},"membershipTierIds":{"type":"array","items":{"type":"string","format":"uuid"}},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"eventIds":{"type":"array","items":{"type":"string","format":"uuid"}},"productIds":{"type":"array","items":{"type":"string","format":"uuid"}},"priorities":{"type":"array","items":{"$ref":"#/components/schemas/CasePriority"}},"eventWithinHours":{"type":"integer","minimum":0,"nullable":true,"description":"Event proximity - matches only when the case's event starts within this many hours."}}},"strategy":{"type":"string","enum":["roundRobin","leastBusy","skillBased","priorityBased","languageBased","customerTierBased","aiRecommended"]},"requiredSkills":{"type":"array","items":{"type":"string","maxLength":60},"description":"Skills an agent must hold (`AgentServiceProfile.skills`), e.g. `ticketing`, `refunds`."},"requireLanguageMatch":{"type":"boolean","default":true,"description":"Only agents who speak the customer's language are candidates."},"maxUtilizationRate":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Agents above this workload are skipped."},"respectSlaCapability":{"type":"boolean","default":true,"description":"Skip agents whose current queue would push the case past its SLA."},"stickyOwnership":{"type":"boolean","default":false,"description":"Prefer the agent who last handled the customer or the reopened case, if available."},"stickyWindowHours":{"type":"integer","minimum":1,"nullable":true},"fallbackQueueId":{"type":"string","format":"uuid","nullable":true,"description":"Where the case goes when no candidate agent is available."},"isActive":{"type":"boolean"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"IntelligentRoutingSkillsAssignmentEngineView": {"description":"A routing rule as stored, with how often it has matched.","x-ticvai-persistence":"none — the marketing.case_routing_rule (new) row plus a count over marketing.case","allOf":[{"$ref":"#/components/schemas/IntelligentRoutingSkillsAssignmentEngineInput"},{"type":"object","properties":{"matchedLast7Days":{"type":"integer","minimum":0,"readOnly":true},"lastMatchedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}}]},
"KioskAssistSession": {"type":"object","x-ticvai-persistence":"marketing.kiosk_assist_session","description":"2.1.25. A staff member acting on a kiosk session remotely. **The guest can always see it and always end it** — remote assistance a guest cannot see or stop is surveillance.\n","required":["id","deviceId","staffPrincipalId","startedAt"],"properties":{"id":{"type":"string","format":"uuid"},"deviceId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"staffPrincipalId":{"type":"string","format":"uuid"},"staffDisplayName":{"type":"string","description":"**Shown on the kiosk.** A guest being helped should know by whom.\n"},"cartId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","enum":["guestCalled","healthAlert","stuckSession","paymentIssue","proactive"]},"endedBy":{"type":"string","nullable":true,"enum":["staff","guest","timeout"]},"actionsTaken":{"type":"array","description":"**Every action recorded as the staff member's**, not the kiosk's. A cashier completing a guest's checkout remotely is a staff action on a guest cart.\n","items":{"type":"object","properties":{"operationId":{"type":"string"},"at":{"type":"string","format":"date-time"}}}},"startedAt":{"type":"string","format":"date-time"},"endedAt":{"type":"string","format":"date-time","nullable":true}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"OrderBookingTicketServiceWorkspaceInput": {"type":"object","x-ticvai-persistence":"marketing.case_service_action","x-ticvai-record-definition":"Permitted Service Actions (one per executed action)","description":"One service action on an order, taken from a case. Only an `execute` stores a row.","required":["id","mode","orderId"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7; equals the `Idempotency-Key` header."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"mode":{"type":"string","enum":["evaluate","execute"]},"caseId":{"type":"string","format":"uuid","description":"Required with `execute`; the action is recorded on this case."},"orderId":{"type":"string","format":"uuid"},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Omit for the whole order."},"action":{"type":"string","description":"Required with `execute`.","enum":["resendTicket","downloadTicket","reissue","transfer","changeName","reschedule","exchange","upgrade","cancel"]},"targetPerformanceId":{"type":"string","format":"uuid","description":"For `reschedule` and `exchange`, the option chosen from the evaluation."},"targetProductId":{"type":"string","format":"uuid","description":"For `exchange` and `upgrade`."},"recipientSubjectId":{"type":"string","format":"uuid","description":"For `transfer` and `changeName`, the new ticket holder."},"deliveryChannel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"description":"For `resendTicket`."},"reason":{"type":"string","maxLength":500},"status":{"type":"string","readOnly":true,"enum":["completed","pendingPayment","refused","failed"]},"downstreamOperation":{"type":"string","readOnly":true,"description":"The operation that performed it, e.g. `rescheduleOrder`."},"downstreamReference":{"type":"string","readOnly":true,"nullable":true},"performedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"OrderBookingTicketServiceWorkspaceView": {"type":"object","x-ticvai-persistence":"none — projection over orders.sales_order, orders.order_line, orders.payment, access.entitlement, marketing.case_service_action (new) and the policies each owning operation reads","description":"The order as a service agent sees it, what may be done to it, and what was done.","required":["orderId","order","availableActions"],"properties":{"orderId":{"type":"string","format":"uuid"},"order":{"type":"string","description":"The order number shown to the guest."},"subjectId":{"type":"string","format":"uuid","nullable":true},"purchaseDate":{"type":"string","format":"date-time"},"channel":{"type":"string","description":"The sales channel the order came through."},"products":{"type":"integer","minimum":0},"tickets":{"type":"integer","minimum":0},"eventId":{"type":"string","format":"uuid","nullable":true},"dateTime":{"type":"string","format":"date-time","nullable":true,"description":"The performance start."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"payment":{"type":"string","enum":["paid","partiallyPaid","unpaid","partiallyRefunded","refunded"]},"fulfillment":{"type":"string","enum":["pending","issued","delivered","failed"]},"ticketStatus":{"type":"string","enum":["valid","partiallyUsed","used","expired","cancelled"]},"availableActions":{"type":"array","items":{"type":"object","required":["action","isPermitted"],"properties":{"action":{"type":"string","enum":["resendTicket","downloadTicket","reissue","transfer","changeName","reschedule","exchange","upgrade","cancel","requestRefund"]},"isPermitted":{"type":"boolean"},"refusedBy":{"type":"string","nullable":true,"enum":["ticketPolicy","servicePolicy","orderStatus","eventDate","customerEntitlement","permission"]},"policyReference":{"type":"string","nullable":true},"options":{"type":"array","description":"Alternatives for `reschedule`, `exchange` and `upgrade`, earliest first.","items":{"type":"object","properties":{"performanceId":{"type":"string","format":"uuid","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true},"startsAt":{"type":"string","format":"date-time","nullable":true},"available":{"type":"boolean"},"priceDifferencePerTicket":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"priceDifferenceTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}}},"lastAction":{"allOf":[{"$ref":"#/components/schemas/OrderBookingTicketServiceWorkspaceInput"}],"nullable":true,"description":"The action just executed; null on `evaluate`."}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"QualityManagementAgentEvaluationView": {"type":"object","x-ticvai-persistence":"marketing.quality_evaluation","description":"One quality evaluation of one interaction (pack 10.2.7). Resolution time and SLA outcome are read from the case, not entered.","required":["id","agentPrincipalId","sourceType","evaluatedBy","status","criteria"],"properties":{"id":{"type":"string","format":"uuid"},"agentPrincipalId":{"type":"string","format":"uuid"},"evaluatorPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The caller who scored it; null while only the AI has."},"sourceType":{"type":"string","enum":["call","chat","email","whatsapp","case","complaint"]},"caseId":{"type":"string","format":"uuid","nullable":true},"conversationId":{"type":"string","format":"uuid","nullable":true},"evaluatedBy":{"type":"string","enum":["human","ai"]},"status":{"type":"string","enum":["draft","scored","acknowledged"]},"criteria":{"type":"array","maxItems":30,"items":{"type":"object","required":["criterion","score","maxScore"],"properties":{"criterion":{"type":"string","maxLength":60,"description":"The tenant's criterion code; the pack's defaults are `greeting`, `customerVerification`, `understanding`, `accuracy`, `policyCompliance`, `communicationQuality`, `empathy`, `resolution`, `documentation`, `closing`."},"score":{"type":"integer","minimum":0},"maxScore":{"type":"integer","minimum":1},"comment":{"type":"string","maxLength":1000,"nullable":true}}}},"criticalFailures":{"type":"array","items":{"type":"string","enum":["incorrectRefund","privacyViolation","unauthorisedCompensation","incorrectTicketInformation","securityVerificationFailure","other"]}},"overallScore":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"readOnly":true,"description":"Criteria score as a percentage; 0 when any critical failure is recorded."},"aiFindings":{"type":"array","readOnly":true,"items":{"type":"object","required":["area","finding"],"properties":{"area":{"type":"string","enum":["policyAdherence","requiredStatements","tone","accuracy","resolutionQuality","missingCaseDocumentation"]},"finding":{"type":"string","maxLength":500},"confidence":{"type":"number","minimum":0,"maximum":1}}}},"feedback":{"type":"string","maxLength":2000,"nullable":true},"coachingActions":{"type":"array","items":{"type":"object","required":["type"],"properties":{"type":{"type":"string","enum":["productTraining","policyTraining","communicationCoaching","systemTraining"]},"note":{"type":"string","maxLength":500,"nullable":true},"dueAt":{"type":"string","format":"date-time","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true}}}},"resolutionSeconds":{"type":"integer","minimum":0,"nullable":true,"readOnly":true},"slaMet":{"type":"boolean","nullable":true,"readOnly":true},"agentComment":{"type":"string","maxLength":1000,"nullable":true},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"evaluatedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ServiceQueue": {"type":"object","x-ticvai-persistence":"marketing.service_queue","description":"**A customer-service queue** (e.g. `eventDaySupport`). Cases (`Case.queueId`), routing rules (`queueId`, `fallbackQueueId`) and agents (`AgentAvailability.queueIds`) name it; `listContact` and `listAgentWorkloadAvailability` report per queue. Maintained by `setServiceQueueDefinition`, read by `listServiceQueues` (decided 29 September, writers pass). (decided 29 September, data model for the agreed operations)\n","required":["id","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":60},"name":{"type":"string","maxLength":150},"overflowWaitSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"The queue's overflow threshold; a case waiting longer marks the queue `critical`."},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"UnifiedInteractionCommunicationHistoryView": {"type":"object","x-ticvai-persistence":"none — projection over marketing.case_message, marketing.conversation_message, marketing.conversation (telephony), marketing.message_dispatch and marketing.kiosk_assist_session","description":"One interaction on the timeline. `social` and `whatsapp` appear only where that channel is integrated.","required":["id","occurredAt","channel","direction","actorKind","source","recordId"],"properties":{"id":{"type":"string","description":"Stable across pages; the source and record id combined."},"occurredAt":{"type":"string","format":"date-time"},"channel":{"type":"string","enum":["email","phone","liveChat","whatsapp","sms","webForm","mobileApp","b2cPortal","social","posFrontDesk","internalNote","automatedNotification"]},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest; the name is resolved on screen through `getGuestProfile` under GUEST_VIEW_PII."},"actorKind":{"type":"string","enum":["guest","agent","system","ai"]},"actorPrincipalId":{"type":"string","format":"uuid","nullable":true},"direction":{"type":"string","enum":["inbound","outbound","internal"]},"subject":{"type":"string","nullable":true},"excerpt":{"type":"string","maxLength":500,"nullable":true},"relatedCaseId":{"type":"string","format":"uuid","nullable":true},"relatedOrderId":{"type":"string","nullable":true},"relatedTicketId":{"type":"string","nullable":true},"attachmentRefs":{"type":"array","items":{"type":"string"}},"sentiment":{"type":"string","nullable":true,"enum":["positive","neutral","negative"],"description":"Where sentiment analysis is enabled; AI-derived."},"source":{"type":"string","enum":["caseMessage","conversationMessage","call","messageDispatch","kioskAssist"]},"recordId":{"type":"string","description":"The row in the source table."}}}
}
```
