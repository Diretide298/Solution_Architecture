# P02-engagement-support-01 — P02 · Engagement & Support (1 of 2)

**10 screens · 31 operations · 78 schemas · 3 permissions**

Platform P02 Guest App · ships as **guest** ·
guest audience · mobileApp ·
offline-capable

## Who this is for

**guest on mobileApp.** Everything below is how you know what is
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
  `AI_USE, CASE_MANAGE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **10 of these operations work offline**: getTenantAppStatus, getVisitPlan, getWaitTimes, listCatalogueBundles, listMyNotifications, listProducts, listPublishedContentPages, listPublishedFaqs
  — and the rest do not. A surface that looks the same online and off is lying.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
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
| `GST-030` | In-Venue Notifications | A | 11 | 12 | 5 | 5 | 4 | 0 | guest | notStarted (client-verified) |
| `GST-031` | AI Concierge – Home | A | 11 | 7 | 5 | 30 | 3 | 0 | guest | notStarted (designed) |
| `GST-032` | AI Concierge – Chat | A | 37 | 26 | 6 | 34 | 3 | 0 | guest | notStarted (designed) |
| `GST-033` | AI Concierge – Contextual Help | A | 4 | 0 | 5 | 11 | 0 | 0 | guest | notStarted (client-verified) |
| `GST-035` | Feedback & Ratings | A | 23 | 0 | 4 | 7 | 2 | 0 | guest | notStarted (client-verified) |
| `GST-040` | Help & Support | A | 8 | 31 | 6 | 0 | 3 | 0 | guest | notStarted (client-verified) |
| `GST-051` | Plan | A | 26 | 0 | 7 | 7 | 8 | 1 | guest | notStarted (client-verified) |
| `GST-052` | Suggested Itineraries | A | 17 | 28 | 6 | 3 | 2 | 1 | guest | notStarted (designed) |
| `GST-053` | Your Plan | A | 15 | 91 | 7 | 9 | 8 | 1 | guest | notStarted (client-verified) |
| `GST-054` | AI Planner | A | 9 | 71 | 7 | 29 | 4 | 1 | guest | notStarted (client-verified) |

## Thin screens in this batch

**GST-033, GST-052 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `GST-030` In-Venue Notifications

**Work with in-venue notifications for this venue.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 2 · needs the `fnb` module |
| Block | Block A · ticket #18153 (APP-MOB-GST-030) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | configEditor (comfortable density): `listMyNotifications` reads the feed (decided 29 September, rev 3 GAP-C1); the location-session claim stays a form on the same screen, so the pattern is kept until the screen is redrawn |
| Offline | **The offline banner shows.** Notices already received stay listed. New queue calls and order updates arrive once the connection is back, and the banner is the warning that they may be late. |
| Opens with | `subjectId` (session) |
| Route | `/general/in-venue-notifications` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Back in the first release** (decided 29 September, rev 3 GAP-C1): the notifications feed is needed in the first release, which reverses audit R242's deferral of this screen. The `deferred` block is removed and the screen returns to `wave: 2`, where it sat before R242. Queue calls and order status still also show on the queue and order screens, which poll.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Location code | text field | — | — | — | — | — | — |
| Seat reference | text field | — | — | — | — | — | — |
| Party size | number field | — | — | — | — | — | — |
| Unread only | toggle | optional | off | — | — | Sends `?unreadOnly=` to `listMyNotifications`. | `listMyNotifications` ?unreadOnly |

**Sent by *Claim location session*** (`claimLocationSession`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Location code `locationCode` | text field | optional | — | Rotates; a stale code is refused. | — | From the QR or NFC tag. Rotates; a stale code is refused. | `claimLocationSession` body |
| Seat reference `seatReference` | group | optional | — | — | — | For seated venues where the seat is the address and there is no code to scan. Validated against the performance's seat map. | `claimLocationSession` body |
| Performance `seatReference.performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `claimLocationSession` body |
| Seat `seatReference.seatId` | text field | optional | — | — | — | — | `claimLocationSession` body |
| Party size `partySize` | number field | optional | — | min 1 | — | — | `claimLocationSession` body |

**Sent by *Mark all as read*** (`markMyNotificationsRead`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Ids `ids` | list of values (chips) | optional | — | at most 200 | — | — | `markMyNotificationsRead` body |
| All `all` | toggle | optional | off | — | — | — | `markMyNotificationsRead` body |

#### Outputs: what the screen shows and produces

**Shown**

**Notifications** (card list, from `listMyNotifications`): **Newest first, unread ones marked.** Each card shows the kind, title, body and when it was queued; tapping one opens its `deepLink` (an order, a queue ticket, a booking) and marks it read. `unreadCount` is the badge on the tab. Sends `?venueId=` for the venue the guest picked.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | text | — |
| Kind | chip: Queue call, Order ready, Booking change, Venue alert, Offer, Other | — |
| Title | in the reader's language | — |
| Body | in the reader's language | — |
| Venue | the name it points at, never the id | — |
| Deep link | text | Where tapping the notification leads in the app (an order, a queue ticket, a booking). |
| Queued at | 1 Oct 2026, 14:30 | — |
| Read | yes / no (icon or chip) | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Unread count | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Claim location session (primary button) | `claimLocationSession` POST `/location-sessions` | inline | LocationSession | 400 Neither a location code nor a seat reference supplied; 409 Code expired or unknown, the location is out of service, or no outlet currently delivers to it — a cabana is useless as an address if nothing serves it. | — |
| Mark all as read (secondary button) | `markMyNotificationsRead` POST `/me/notifications/read` | inline | inline | — | works offline |

**Data it reads**: `listMyNotifications` (onLoad, The guest's notification feed, newest first: queue calls …)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `GST-031` AI Concierge – Home: *AI Concierge – Home*; carries `outletId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The notification feed. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the in-venue notifications untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **No notifications yet.** Queue calls, order updates and venue notices appear here as the venue sends them. |
| Offline (`?state=offline`) | **The offline banner shows.** Notices already received stay listed. New queue calls and order updates arrive once the connection is back, and the banner is the warning that they may be late. |
| Empty, no results (`?state=emptyNoResults`) | **No unread notifications.** Names the Unread only filter and offers to show all; the read ones are still there. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither a location code nor a seat reference supplied; 409 Code expired or unknown, the location is out of service, or no outlet currently delivers to it — a cabana is useless as an address if nothing serves it. |

#### Permissions

- `claimLocationSession` → no permission · guest
- `listMyNotifications` → no permission · guest
- `markMyNotificationsRead` → no permission · guest

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.50 | Location Delivery - System shall support delivery to guest location. | Guest Mobile App & Branding | CONTRACTED | `claimLocationSession` |
| 4.6.23 | Allow guests to place orders through mobile applications. | Bundles and Promotions | CONTRACTED | `claimLocationSession` |
| 4.6.24 | Allow guests to order by scanning QR codes. | Bundles and Promotions | CONTRACTED | `claimLocationSession` |
| 4.6.25 | Allow ordering directly from guest seats. | Bundles and Promotions | CONTRACTED | `claimLocationSession` |
| 4.6.26 | Deliver orders to tables, seats, cabanas or designated locations. | Bundles and Promotions | CONTRACTED | `claimLocationSession` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Virtual queue join flow with a persistent status notification (e.g. "in queue, 25 minutes"). *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1090)*
- The in-venue notifications feed is needed in the first release on web and mobile (R242 deferral reversed). *(agreed · design review 29 Sep 2026, GAP-C1 · C. Wave 2: In-Venue Notifications · DI-1075)*
- Proactively upsell an express/fast-lane ticket to a guest facing a long wait (e.g. "buy express ticket for [amount]"). *(agreed · MoM 7 Sep 2026, 4.17 Revenue lever / 5. Key Decisions · DI-683)*
- A visual venue map highlights long-queue rides vs low-queue alternatives so operations can redirect guests, e.g. a notification suggesting a nearby ride with a shorter wait. *(client request · MoM 7 Sep 2026, 4.17 AI guest flow optimization · DI-682)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-030` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *DEFERRED (R242), still in the prototype: Account → All screens → Wave 2 → In-venue notifications; At-venue tab → Alerts*. Differences: The YAML defers this (no in-app notification feed in the first release), but the prototype still shows a feed and an Alerts tab, so the client will expect it.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-030?state=<state>`: loading, error, emptyFirstRun, offline, emptyNoResults.
- [ ] Every action is wired with its success and its failure: Claim location session, Mark all as read.
- [ ] Every transition is wired: `GST-001`, `GST-031`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-031` AI Concierge – Home

**The screen this app sits on. Everything else is entered from here and returns to it.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 2 · needs the `fnb` module |
| Block | Block A · ticket #18172 (APP-MOB-GST-031) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (comfortable density): `getGuestMenu` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Not available, and the offline banner says why.** The assistant needs the connection; conversations already loaded stay readable. |
| Opens with | `conversationId` (deepLink), `outletId` (deepLink) · cold entry: A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom. |
| Route | `/general/ai-concierge-home` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest concierge confirmed in Phase 1 on 17 August (CF-14), charged per token and bounded by `AiPolicy.guestCapabilityScope`.** Still degrades to the manual planner rather than to an error. **Cross-surface parity, 31 August**: added createAiConversation, handoverToAgent, requestSuggestion. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations. **Rev 3 (decided 29 September).** The concierge shows as mascot art when `BookingFlowConfig.conciergeMascot` is on (default), otherwise a plain button (CFG-5).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| At | date and time picker | — | — | `getGuestMenu` ?at |
| Language | language picker | — | — | `getGuestMenu` ?language |

**Form: Send AI message** (modal, opened by *Send AI message*; *Send AI message* calls `sendAiMessage`, *Cancel* sends nothing)

**Collects what `sendAiMessage` sends before it is called.** Required: `content`. Optional: `collectionIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Content `content` | text area | required | — | min length 1; max length 8000 | — | — | `sendAiMessage` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | Restrict retrieval to named collections. Absent means every collection the principal may read. | `sendAiMessage` body |

**Form: Create AI conversation** (modal, opened by *Create AI conversation*; *Create AI conversation* calls `createAiConversation`, *Cancel* sends nothing)

**Collects what `createAiConversation` sends before it is called.** Required: `module`. Optional: `locale`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Module `module` | select | required | — | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | — | Which part of the platform the conversation is about (8.4.1). | `createAiConversation` body |
| Locale `locale` | text field | optional | — | — | — | 8.4.3. Multilingual, and Arabic is not an afterthought here. | `createAiConversation` body |

**Form: Handover to agent** (modal, opened by *Handover to agent*; *Handover to agent* calls `handoverToAgent`, *Cancel* sends nothing)

**Collects what `handoverToAgent` sends before it is called.** Required: `reason`. Optional: `summary`, `preferredQueueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Guest requested · Assistant refused · Assistant failed · Out of scope · Negative sentiment · Complex intent · Payment issue | — | — | `handoverToAgent` body |
| Summary `summary` | text field | optional | — | — | — | The assistant's own summary of what the guest wants, so the agent opens with context rather than reading a transcript while somebody waits. | `handoverToAgent` body |
| Preferred queue `preferredQueueId` | picker: choose a preferred queue | optional | — | — | shows names, sends the id | — | `handoverToAgent` body |

Errors to draw in the form: 409 No agent available. Returns the reason and offers a case, rather than queuing a guest for somebody who is not there. (HandoverRefusedProblem)

**Form: Request suggestion** (modal, opened by *Request suggestion*; *Request suggestion* calls `requestSuggestion`, *Cancel* sends nothing)

**Collects what `requestSuggestion` sends before it is called.** Required: `kind`, offered as `prepPlan`, `upsell` or `waitTime` only — no `scenario`; an itinerary is asked on the Plan tab (GST-054, since 29 September). Optional: `subjectRef`, `horizon`, `context`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Price · Replenishment · Requisition · Demand forecast · Prep plan · Menu engineering · Staffing · Sla target · Wait time · Upsell · Segmentation · Anomaly …; Anything else is refused — a guest asking for `price` is a guest asking what the venue is willing to … | — | A guest caller may ask for `prepPlan`, `upsell`, `waitTime` and `itinerary` only. | `requestSuggestion` body |
| Subject ref `subjectRef` | text field | optional | — | — | — | — | `requestSuggestion` body |
| Horizon `horizon` | text field | optional | — | — | — | For a forecast — `nextService`, `7d`, `28d`, or an ISO period. | `requestSuggestion` body |
| Context `context` | key and value settings | optional | — | — | — | What the caller already knows. Passed rather than re-fetched so a suggestion made from a screen uses the numbers the screen is showing — advice computed from data the manager … | `requestSuggestion` body |

Errors to draw in the form: 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem)

#### Outputs: what the screen shows and produces

**Shown**

**The guest menu** (detail panel, from `getGuestMenu`)

| Shows | Format | Notes |
|---|---|---|
| Outlet | the name it points at, never the id | — |
| Menu | the name it points at, never the id | — |
| Name | text | — |
| In force until | 1 Oct 2026, 14:30 | When this menu stops applying. The client shows it, because a guest browsing breakfast at 10:55 should know. |
| Currency | text | — |
| Currency scale | 1,234 | — |
| Sections | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Send AI message (primary button) | `sendAiMessage` POST `/conversations/{conversationId}/messages` | inline | AiMessage | — | opens modal first |
| Create AI conversation (secondary button) | `createAiConversation` POST `/conversations` | inline | AiConversation | — | opens modal first |
| Handover to agent (secondary button) | `handoverToAgent` POST `/conversations/{conversationId}/handover` | inline | Conversation | 409 No agent available. Returns the reason and offers a case, rather than queuing a guest for somebody who is not there. (HandoverRefusedProblem) | opens modal first |
| Request suggestion (secondary button) | `requestSuggestion` POST `/ai/suggestions` | inline | Suggestion | 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem) | opens modal first |

**Data it reads**: `getGuestMenu` (onLoad, From the flow it appears in)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `GST-032` AI Concierge – Chat: *AI Concierge – Chat*; carries `conversationId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The concierge home, read by `getGuestMenu`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the concierge home untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No concierge home yet. Offers Create AI conversation (`createAiConversation`). |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **Not available, and the offline banner says why.** The assistant needs the connection; conversations already loaded stay readable. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 No agent available. Returns the reason and offers a case, rather than queuing a guest for somebody who is not there. (HandoverRefusedProblem); 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem) |

#### Permissions

- `getGuestMenu` → no permission · guest, staff
- `sendAiMessage` → `AI_USE` (operate) · staff, guest
- `createAiConversation` → `AI_USE` (operate) · staff, guest
- `handoverToAgent` → no permission · guest
- `requestSuggestion` → `AI_USE` (operate) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

30 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.9 | APIs shall support menu retrieval, order creation, order status, kitchen status, inventory updates and promotions. | Developer & API Management | CONTRACTED | `getGuestMenu` |
| 8.1.5 | Explainability System shall provide reasoning and confidence indicators where available. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.19 | System shall support AI-powered ticketing assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.20 | System shall support AI-powered support assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 18.10.1 | AI Assistant - System shall provide an AI assistant for employees. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.3 | Operational Queries - Users shall retrieve operational information through AI. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.4 | Work Order Assistance - AI shall assist users with work order activities. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.5 | Knowledge Base Assistance - AI shall provide access to operational knowledge and procedures. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 22.8.4 | AI Chatbot Assistant | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.13 | AI Intent Recognition | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.14 | AI Knowledge Base Integration | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.15 | AI Product Recommendations | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| … 18 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The concierge (Sahli) shows as mascot art or as a plain button; setting "Concierge mascot", default on. *(agreed · design review 29 Sep 2026, CFG-5 · Sahli mascot (on/off) · DI-1069)*
- AI concierge answers natural-language guest questions (ticketing, F&B, retail, venue info, timings) grounded in the venue's configured data. *(client request · MoM 10 Aug 2026, 4.6 AI Functions, Lost & Found, Reviews, Loyalty · DI-207)*
- **Open question.** AI concierge chat design is deferred until a dedicated AI workshop settles the technical approach (third-party LLM with PII masking) and the token/billing model. *(open · MoM 10 Aug 2026, 4.2 AI Concierge Chat — Open Item · DI-195)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Concierge mascot (`bookingFlow.conciergeMascot`) | Read only where the `aiConciergeChat` feature is on. | on | The concierge as mascot art or a plain button (decided 29 September, rev 3 CFG-5). |
| Settings: concierge mascot (`bookingFlow.venueOverrides[].settings.conciergeMascot`) | Read only where the `aiConciergeChat` feature is on. | on | The concierge as mascot art or a plain button (decided 29 September, rev 3 CFG-5). |

*SEO metadata*, set in `CMS-013` SEO & Metadata:

Also set there, as content the tenant writes: locale.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-031` · status **notStarted** · provenance designed · **Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no …
- Prototype (Mobile App v4, 29 September 2026, verified —, match none): `sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html`, view **
- Drawn by: Claude Code, 30 September 2026, drawn in the Mobile App v4 look
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-031?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Send AI message, Create AI conversation, Handover to agent, Request suggestion.
- [ ] Every transition is wired: `GST-001`, `GST-032`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-032` AI Concierge – Chat

**Add ai concierge – chat for this venue.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 2 · needs the `ticketing` module |
| Block | Block A · ticket #18197 (APP-MOB-GST-032) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (comfortable density): `getGuestOrderStatus` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Not available, and the offline banner says why.** The assistant needs the connection; conversations already loaded stay readable. |
| Opens with | `cartId` (session), `conversationId` (deepLink), `orderId` (deepLink), `messageId` (navigation) · cold entry: A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom. **A guest opening an order link weeks later.** Shows the … |
| Route | `/general/ai-concierge-chat` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest concierge confirmed in Phase 1 on 17 August (CF-14), charged per token and bounded by `AiPolicy.guestCapabilityScope`.** Still degrades to the manual planner rather than to an error.

#### Inputs: what the user enters or picks

**Form: Add cart line** (modal, opened by *Add cart line*; *Add cart line* calls `addCartLine`, *Cancel* sends nothing)

**Collects what `addCartLine` sends before it is called.** Required: `variantId`, `quantity`. Optional: `performanceId`, `seatIds`, `parentLineId`, `attributes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Variant `variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `addCartLine` body |
| Quantity `quantity` | number field | required | — | min 1 | — | — | `addCartLine` body |
| Performance `performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `addCartLine` body |
| Booked window `bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `addCartLine` body |
| Starts at `bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `addCartLine` body |
| Ends at `bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `addCartLine` body |
| Recommendation `recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `addCartLine` body |
| Table reservation `tableReservationId` | picker: choose a table reservation | optional | — | A booking that is not awaiting a deposit is refused 422 `depositNotDue`. | shows names, sends the id | A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's … | `addCartLine` body |
| Seats `seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). | — | At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on … | `addCartLine` body |
| Resource hold `resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and … | `addCartLine` body |
| Parent line `parentLineId` | picker: choose a parent line | optional | — | — | shows names, sends the id | For an add-on attaching to a ticket already in the cart. Removing the parent removes the child — a locker with no admission is not a sale. | `addCartLine` body |
| Attributes `attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `addCartLine` body |
| Transport `attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `addCartLine` body |
| Route `attributes.transport.routeId` | picker: choose a route | required | — | — | shows names, sends the id | The `transport.TransportRoute`. | `addCartLine` body |
| From station `attributes.transport.fromStationId` | picker: choose a from station | required | — | — | shows names, sends the id | Boarding station, a stop of the route. | `addCartLine` body |
| To station `attributes.transport.toStationId` | picker: choose a to station | required | — | — | shows names, sends the id | Alighting station, a later stop of the route. | `addCartLine` body |
| Passenger type code `attributes.transport.passengerTypeCode` | text field | optional | — | pattern `^[a-z][a-zA-Z0-9]{0,31}$` | — | The fare table's passenger type (`adult`, `child`, ...). Required on a one-way trip. | `addCartLine` body |
| Pass type `attributes.transport.passTypeId` | picker: choose a pass type | optional | — | — | shows names, sends the id | Pass purchase only. The `transport.PassType` bought for this station pair. | `addCartLine` body |
| Pass entitlement `attributes.transport.passEntitlementId` | picker: choose a pass entitlement | optional | — | — | shows names, sends the id | A seat reserved with a pass already owned. The line is zero-priced and validated against the pass (stations covered, an entry left, within validity). | `addCartLine` body |

Errors to draw in the form: 403 The performance's on-sale waiting room is on and the request has no valid admission token (ADR-0066).; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The booked window is missing, not allowed or the wrong length for the variant (`windowRequired`, `windowNotAllowed`, `windowLengthMismatch`; rev 3 REV3-13), or … (CartProblem)

**Form: Checkout cart** (modal, opened by *Checkout cart*; *Checkout cart* calls `checkoutCart`, *Cancel* sends nothing)

**Collects what `checkoutCart` sends before it is called.** Nothing in the body is required. Optional: `subjectId`, `attendees`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | The guest the order is for. A guest caller may name only themselves (`guestAuth` never widens to another subject); omitted, the cart's own `subjectId` is used. | `checkoutCart` body |
| Marketing consents `marketingConsents` | repeatable rows | optional | — | — | — | Marketing opt-ins given at checkout (29 September, M18-15). Shown unticked beside the terms; one entry per channel and purpose the guest ticked. | `checkoutCart` body |
| Channel `marketingConsents[].channel` | radio group | required | — | Email · SMS · Whatsapp · Push | — | — | `checkoutCart` body |
| Purpose `marketingConsents[].purpose` | text field | required | — | max length 60 | — | The consent purpose code (marketing ConsentPurpose), for example `marketing`. | `checkoutCart` body |
| Granted `marketingConsents[].granted` | toggle | required | — | True only when the guest ticked it. | — | True only when the guest ticked it. Never pre-ticked. | `checkoutCart` body |
| Notice version `marketingConsents[].noticeVersion` | text field | optional | — | max length 40 | — | The version of the consent notice shown. | `checkoutCart` body |
| Attendees `attendees` | repeatable rows | optional | — | — | — | The named holder for each cart line that needs one. Becomes `CreateOrderLine.holderName` on the order's matching line. | `checkoutCart` body |
| Line `attendees[].lineId` | picker: choose a line | required | — | — | shows names, sends the id | A `CartLine.id` in this cart. | `checkoutCart` body |
| Holder name `attendees[].holderName` | text field | required | — | — | — | — | `checkoutCart` body |

Errors to draw in the form: 403 The contact the tickets would go to is not proven — an unverified session (`sessionNotVerified`), or a guest checkout with no confirmed one-time code … (CartProblem); 409 A lease expired between the last read and checkout (`leaseExpired`), or a resource hold did (`resourceHoldInvalid`, rev 3 REV3-15). (CartProblem); 422 A required consent question is unanswered (`consentRequired`), or an answer blocks the booking (`consentAnswerBlocks`), with the lines in `lineIds` (decided 29 … (CartProblem)

**Form: Send AI message** (modal, opened by *Send AI message*; *Send AI message* calls `sendAiMessage`, *Cancel* sends nothing)

**Collects what `sendAiMessage` sends before it is called.** Required: `content`. Optional: `collectionIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Content `content` | text area | required | — | min length 1; max length 8000 | — | — | `sendAiMessage` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | Restrict retrieval to named collections. Absent means every collection the principal may read. | `sendAiMessage` body |

**Form: Send conversation message** (modal, opened by *Send conversation message*; *Send conversation message* calls `sendConversationMessage`, *Cancel* sends nothing)

**Collects what `sendConversationMessage` sends before it is called.** Required: `body`. Optional: `attachments`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Body `body` | text area | required | — | max length 4000 | — | — | `sendConversationMessage` body |
| Attachments `attachments` | repeatable rows | optional | — | — | — | — | `sendConversationMessage` body |
| Asset `attachments[].assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `sendConversationMessage` body |
| Kind `attachments[].kind` | select | optional | — | Image · Video · Document · Ticket · QR · Payment link | — | — | `sendConversationMessage` body |

**Form: Handover to agent** (modal, opened by *Handover to agent*; *Handover to agent* calls `handoverToAgent`, *Cancel* sends nothing)

**Collects what `handoverToAgent` sends before it is called.** Required: `reason`. Optional: `summary`, `preferredQueueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Guest requested · Assistant refused · Assistant failed · Out of scope · Negative sentiment · Complex intent · Payment issue | — | — | `handoverToAgent` body |
| Summary `summary` | text field | optional | — | — | — | The assistant's own summary of what the guest wants, so the agent opens with context rather than reading a transcript while somebody waits. | `handoverToAgent` body |
| Preferred queue `preferredQueueId` | picker: choose a preferred queue | optional | — | — | shows names, sends the id | — | `handoverToAgent` body |

Errors to draw in the form: 409 No agent available. Returns the reason and offers a case, rather than queuing a guest for somebody who is not there. (HandoverRefusedProblem)

#### Outputs: what the screen shows and produces

**Shown**

**The guest order status** (detail panel, from `getGuestOrderStatus`)

| Shows | Format | Notes |
|---|---|---|
| Order | text | — |
| Order number | text | — |
| Status | chip: Ordered, Accepted, In preparation, Ready, Served, Collected… | The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or … |
| Estimated ready at | 1 Oct 2026, 14:30 | — |
| Is ready for collection | yes / no (icon or chip) | — |
| Lines | list or chips (count when long) | Per-line status. A guest waiting on one dish should see which. |

**The cart** (detail panel, from `getCart`)

| Shows | Format | Notes |
|---|---|---|
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing … |
| Status | chip: Active, Expiring, Expired, Abandoned, Checked out | — |
| Lines | list or chips (count when long) | — |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Discount total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied promotions | list or chips (count when long) | Re-evaluated on every read. A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became … |
| Expires at | 1 Oct 2026, 14:30 | The earliest lease expiry in the cart, or the cart's own window where it holds none. |
| Extensions used | 1,234 | — |
| Max extensions | 1,234 | — |

**Order to confirm** (card list, from `createGuestFnbOrder`): An order the concierge proposes is a card in the conversation: items, total and Confirm, which places it (`createGuestFnbOrder`). No raw form.

| Shows | Format | Notes |
|---|---|---|
| Order | text | — |
| Order number | text | Short and readable. It gets called out across a counter. |
| Fulfilment | chip: Collect, Deliver to location, Table service, Deliver to address | How the order reaches the guest, in the request's terms: `collect` is `GuestOrderFulfilment.mode` `collection`; `deliverToAddress` is … |
| Delivery label | text | Where it is going, as a runner would read it. |
| Status | chip: Ordered, Accepted, In preparation, Ready, Served, Collected… | The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or … |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Estimated ready at | 1 Oct 2026, 14:30 | — |
| Collection point | text | — |
| Table label | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add cart line (secondary button) | `addCartLine` POST `/carts/{cartId}/lines` | AddCartLineRequest | Cart | 403 The performance's on-sale waiting room is on and the request has no valid admission token (ADR-0066).; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The … | opens modal first |
| Checkout cart (secondary button) | `checkoutCart` POST `/carts/{cartId}/checkout` | inline | Order | 403 The contact the tickets would go to is not proven — an unverified session (`sessionNotVerified`), or a guest checkout with no confirmed one-time code … (CartProblem); 409 A lease expired between the last read and … | emits `order.created`; opens modal first |
| Send AI message (secondary button) | `sendAiMessage` POST `/conversations/{conversationId}/messages` | inline | AiMessage | — | opens modal first |
| Send conversation message (secondary button) | `sendConversationMessage` POST `/conversations/{conversationId}/messages` | inline | ConversationMessage | — | opens modal first |
| Handover to agent (secondary button) | `handoverToAgent` POST `/conversations/{conversationId}/handover` | inline | Conversation | 409 No agent available. Returns the reason and offers a case, rather than queuing a guest for somebody who is not there. (HandoverRefusedProblem) | opens modal first |

**Data it reads**: `getGuestOrderStatus` (onLoad, Track an order Only when signed in (decided 2 October 2026 …); `getCart` (onLoad, The cart, priced and checked, right now With the guest …)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `GST-033` AI Concierge – Contextual Help: *AI Concierge – Contextual Help*; carries `conversationId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The concierge chat, read by `getGuestOrderStatus`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the concierge chat untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No concierge chat yet. Offers Create guest F&B order (`createGuestFnbOrder`). |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **Not available, and the offline banner says why.** The assistant needs the connection; conversations already loaded stay readable. |
| Empty, no results (`?state=emptyNoResults`) | Nothing the concierge found matches the question; it says so in the conversation and offers to hand over to a person. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A lease expired between the last read and checkout (`leaseExpired`), or a resource hold did (`resourceHoldInvalid`, rev 3 REV3-15). (CartProblem); 409 An item became unavailable, the quoted total no longer matches, the location session expired, or the outlet stopped taking orders.; 409 No agent available. Returns the reason and offers a case, rather than queuing a guest for somebody who is … |

#### Permissions

- `createGuestFnbOrder` → no permission · guest
- `getGuestOrderStatus` → no permission · guest
- `getCart` → no permission · guest, partner, staff
- `addCartLine` → no permission · guest, partner, staff
- `checkoutCart` → no permission · guest, partner
- `sendAiMessage` → `AI_USE` (operate) · staff, guest
- `sendConversationMessage` → `CASE_MANAGE` (configure) · staff, guest
- `handoverToAgent` → no permission · guest
- `recordAnswerFeedback` → `AI_USE` (operate) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

34 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.47 | Mobile Food Ordering - System shall support mobile food ordering. | Guest Mobile App & Branding | CONTRACTED | `createGuestFnbOrder` |
| 2.9.2 | The system should provide a service to enable the dynamic composition of the shop cart. The system must provide back all the information in real time, such as the performance availabilities of an … | Ticketing Sales | CONTRACTED | `getCart` |
| 2.9.5 | The system should highlight conflicting times at different attractions when trying to purchase tickets in the same time-slot for one guest. For example, if a ticket for Golf 1 to 2 pm has been added … | Ticketing Sales | CONTRACTED | `getCart` |
| 19.2.19 | Add-On Purchases - System shall support add-on purchases. | Guest Mobile App & Branding | CONTRACTED | `addCartLine` |
| 1.1.130 | The solution shall support donation solicitation during the customer checkout process. Functional Requirements Donation prompt at checkout. Optional donation acceptance. Multiple donation campaign … | Ticketing Catalogue | CONTRACTED | `addCartLine` |
| 2.12.1 | The system should have the ability for order entry: - Select an item to place on an order. - Indicate quantity of item selected - Apply a name to an order (e.g. Smith Party). Each admission on the … | Ticketing Sales | CONTRACTED | `addCartLine` |
| 2.12.29 | In order to improve Guest experience, it shall be possible to pre-order as many product or services as possible, including multi-park pass. | Ticketing Sales | CONTRACTED | `addCartLine` |
| 19.2.10 | Ticket Purchase - System shall support ticket purchases. | Guest Mobile App & Branding | CONTRACTED | `checkoutCart` |
| 19.2.23 | Membership Purchase - System shall support membership purchases. | Guest Mobile App & Branding | CONTRACTED | `checkoutCart` |
| 19.2.24 | Membership Renewal - System shall support membership renewals. | Guest Mobile App & Branding | CONTRACTED | `checkoutCart` |
| 19.2.53 | Product Purchases - System shall support merchandise purchases. | Guest Mobile App & Branding | CONTRACTED | `checkoutCart` |
| 1.1.98 | Membership renewals | Ticketing Catalogue | CONTRACTED | `checkoutCart` |
| … 22 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The AI chat box answers guided/predefined queries (booking status, rescheduling) and logs guest conversation history across channels (WhatsApp, web, Instagram, Facebook) with per-channel conversion attribution. *(client request · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-388)*
- AI concierge answers natural-language guest questions (ticketing, F&B, retail, venue info, timings) grounded in the venue's configured data. *(client request · MoM 10 Aug 2026, 4.6 AI Functions, Lost & Found, Reviews, Loyalty · DI-207)*
- **Open question.** AI concierge chat design is deferred until a dedicated AI workshop settles the technical approach (third-party LLM with PII masking) and the token/billing model. *(open · MoM 10 Aug 2026, 4.2 AI Concierge Chat — Open Item · DI-195)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-032` · status **notStarted** · provenance designed · **Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no …
- Prototype (Mobile App v4, 29 September 2026, verified —, match none): `sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html`, view **
- Drawn by: Claude Code, 30 September 2026, drawn in the Mobile App v4 look
- ADR-0045 *Every order carries a proven contact, and the gate is the checkout page* (`docs/adr/0045-every-order-carries-a-proven-contact.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)
- ADR-0066 *The on-sale waiting room sits at the edge, apart from the ride queue* (`docs/adr/0066-the-on-sale-waiting-room-is-separate-from-the-ride-queue.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (37), with its required mark, default, format and its error state (402, 403, 404, 409, 410, 422).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-032?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline, emptyNoResults.
- [ ] Every action is wired with its success and its failure: Add cart line, Checkout cart, Send AI message, Send conversation message, Handover to agent.
- [ ] Every transition is wired: `GST-001`, `GST-033`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-033` AI Concierge – Contextual Help

**Answer a question without needing a person.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 2 · needs the `ai` module |
| Block | Block A · ticket #18092 (APP-MOB-GST-033) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | configEditor (comfortable density): the screen declares only writes (`sendAiMessage`) and no read of a population — it is settings, not a list |
| Offline | **Not available, and the offline banner says why.** The assistant needs the connection; conversations already loaded stay readable. |
| Opens with | `conversationId` (deepLink) · cold entry: A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom. |
| Route | `/general/ai-concierge-contextual-help` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest concierge confirmed in Phase 1 on 17 August (CF-14), charged per token and bounded by `AiPolicy.guestCapabilityScope`.** Still degrades to the manual planner rather than to an error. **createPayment removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class). **Navigation repointed to P15 on 20 August** — the F&B screens it linked to moved out of the back office when the client board was adopted. **Cross-platform navigation removed 24 August**: BO-020. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Content | text field | — | — | — | — | Required. | — |
| Collection ids | multi select | — | — | — | — | — | — |

**Sent by *Send AI message*** (`sendAiMessage`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Content `content` | text area | required | — | min length 1; max length 8000 | — | — | `sendAiMessage` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | Restrict retrieval to named collections. Absent means every collection the principal may read. | `sendAiMessage` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Send AI message (primary button) | `sendAiMessage` POST `/conversations/{conversationId}/messages` | inline | AiMessage | — | — |

**Where the user goes next**

- → `GST-001` Home: *Home – Default*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved concierge contextual help. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the concierge contextual help untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No concierge contextual help configured. The form opens empty and `sendAiMessage` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **Not available, and the offline banner says why.** The assistant needs the connection; conversations already loaded stay readable. |

#### Permissions

- `sendAiMessage` → `AI_USE` (operate) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.5 | Explainability System shall provide reasoning and confidence indicators where available. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.19 | System shall support AI-powered ticketing assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.20 | System shall support AI-powered support assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 18.10.1 | AI Assistant - System shall provide an AI assistant for employees. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.3 | Operational Queries - Users shall retrieve operational information through AI. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.4 | Work Order Assistance - AI shall assist users with work order activities. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.5 | Knowledge Base Assistance - AI shall provide access to operational knowledge and procedures. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 22.8.4 | AI Chatbot Assistant | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.13 | AI Intent Recognition | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.14 | AI Knowledge Base Integration | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.15 | AI Product Recommendations | Marketing & CRM | CONTRACTED | `sendAiMessage` |

#### Client meeting inputs

None names this screen.

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-033` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 2 → AI concierge – contextual help*
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-033?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Send AI message.
- [ ] Every transition is wired: `GST-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-035` Feedback & Ratings

**Work with feedback & ratings for this venue.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block A · ticket #18222 (APP-MOB-GST-035) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | configEditor (comfortable density): the screen declares only writes (`submitReview`, `raiseMyCase`) and no read of a population — it is settings, not a list |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | nothing: it opens on its own |
| Route | `/general/feedback-and-ratings` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest case operations wired 24 August.** **No case operation was guest-callable** — a guest could raise nothing and read nothing, and `check-screens` refused the staff-permissioned ones on a guest surface. `listMyCases`, `raiseMyCase` and `replyToMyCase` are scoped to the caller rather than filtered by a subject parameter.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| id | picker: choose an id (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `SubmitReviewRequest.id` |
| subjectId | picker: choose a subject (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `SubmitReviewRequest.subjectId` |
| venueId | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `SubmitReviewRequest.venueId` |
| relatedOrderId | text field | optional | — | — | — | — | `SubmitReviewRequest.relatedOrderId` |
| rating | stepper or slider | optional | — | min 1; max 5 | — | — | `SubmitReviewRequest.rating` |
| body | text area | optional | — | max length 5000 | — | — | `SubmitReviewRequest.body` |
| aspects | multi-select chips | optional | — | Exhibitions · Staff · Cleanliness · Food · Value; no duplicates | — | Aspect chips — the closed set the description always named. | `SubmitReviewRequest.aspects` |
| recordedAt | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `SubmitReviewRequest.recordedAt` |

**Form: Raise my case** (modal, opened by *Raise my case*; *Raise my case* calls `raiseMyCase`, *Cancel* sends nothing)

**Collects what `raiseMyCase` sends before it is called.** Required: `id`, `kind`, `summary`, `recordedAt`. Optional: `detail`, `venueId`, `orderRef`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Created on the device, so a retry after a dropped connection carries the same id and is the same case. | `raiseMyCase` body |
| Kind `kind` | select | required | — | Lost property · Complaint · Question · Accessibility · Refund request · Other; Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.; A case raised as `other` must carry a non-empty `detail` … | — | What the guest says the case is about, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. | `raiseMyCase` body |
| Summary `summary` | text field | required | — | max length 200 | — | Lands in `Case.subject` — the case's one-line title. | `raiseMyCase` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time when the guest raised it. The server stamps `syncedAt` on arrival; both are kept (naming-and-style 5.2), because the SLA clock starts at `recordedAt`, not at the … | `raiseMyCase` body |
| Detail `detail` | text field | optional | — | — | — | Required, and not empty, when `kind` is `other` (decided 28 September, audit R222); a 400 otherwise. | `raiseMyCase` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `raiseMyCase` body |
| Order ref `orderRef` | text field | optional | — | — | — | — | `raiseMyCase` body |

Errors to draw in the form: 400 `kind` is `other` and `detail` is missing or empty (audit R222), or another field breaks the schema

**Sent by *Submit review*** (`submitReview`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `submitReview` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `submitReview` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `submitReview` body |
| Related order `relatedOrderId` | text field | optional | — | — | — | — | `submitReview` body |
| Rating `rating` | stepper or slider | required | — | min 1; max 5 | — | — | `submitReview` body |
| Body `body` | text area | optional | — | max length 5000 | — | — | `submitReview` body |
| Aspects `aspects` | multi-select chips | optional | — | Exhibitions · Staff · Cleanliness · Food · Value; no duplicates | — | Aspect chips — the closed set the description always named. | `submitReview` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `submitReview` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Submit review (primary button) | `submitReview` POST `/reviews` | SubmitReviewRequest | Review | — | — |
| Raise my case (secondary button) | `raiseMyCase` POST `/my/cases` | inline | Case | 400 `kind` is `other` and `detail` is missing or empty (audit R222), or another field breaks the schema | opens modal first |

**Where the user goes next**

- → `GST-001` Home: *Home – Default*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved feedback ratings. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the feedback ratings untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No feedback ratings configured. The form opens empty and `submitReview` saves the first one; it says what the platform does in the meantime. |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `kind` is `other` and `detail` is missing or empty (audit R222), or another field breaks the schema |

#### Permissions

- `submitReview` → no permission · guest
- `raiseMyCase` → no permission · guest

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.71 | Feedback Management - System shall support guest feedback. | Guest Mobile App & Branding | CONTRACTED | `submitReview` |
| 6.1.46 | The system should be able to report on the captured customer satisfaction feedback (based on number of stars or smiley faces, etc.) and report this monthly by attraction /location. | Retail POS | CONTRACTED | `submitReview` |
| 22.5.1 | Review Collection | Marketing & CRM | CONTRACTED | `submitReview` |
| 22.5.2 | Multi-Channel Review Capture | Marketing & CRM | CONTRACTED | `submitReview` |
| 22.5.14 | CRM Integration | Marketing & CRM | CONTRACTED | `submitReview` |
| 22.5.15 | Loyalty Integration | Marketing & CRM | CONTRACTED | `submitReview` |
| 22.5.16 | Membership Integration | Marketing & CRM | CONTRACTED | `submitReview` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Surveys trigger at configurable points: post-purchase, post-visit, post-ticket-scan, membership renewal and case closure. *(client request · MoM 20 Aug 2026, 4.9 Surveys & Gamification · DI-391)*
- Example site showed a live integration with a government satisfaction-survey ("happiness meter") service. *(client request · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-112)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-035` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 3 → Feedback & ratings*

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-035?state=<state>`: loading, error, emptyFirstRun, offline.
- [ ] Every action is wired with its success and its failure: Submit review, Raise my case.
- [ ] Every transition is wired: `GST-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-040` Help & Support

**Answer a question without needing a person.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 2 · needs the `marketing` module |
| Block | Block A · ticket #18174 (APP-MOB-GST-040) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (comfortable density): 3 independent reads and no read of one record — the screen watches a population rather than working one |
| Offline | **The offline banner shows.** Help already loaded stays readable, marked with its age. **Raising a case is disabled offline** — it needs the connection (decided 28 September, audit R148) — and the screen says how to reach staff in person instead: the guest services desk, or any member of staff. |
| Opens with | `caseId` (deepLink) · cold entry: A case opened from a notification or the list. **Optional** — the ordinary way in is to raise a new one, not to open an old one. |
| Route | `/general/help-and-support` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest case operations wired 24 August.** **No case operation was guest-callable** — a guest could raise nothing and read nothing, and `check-screens` refused the staff-permissioned ones on a guest surface. `listMyCases`, `raiseMyCase` and `replyToMyCase` are scoped to the caller rather than filtered by a subject parameter. **Rev 3 (decided 29 September).** The Help screen shows app status and a public *What's new* (GAP-B2).

**Known gaps.** Replaced by `listPublishedFaqs`, the guest read of the same data. Replaced by `listPublishedContentPages`, the guest read of the same data.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category code | text field | — | — | `listPublishedContentPages` ?categoryCode |
| Slug | text field | — | pattern `^[a-z0-9-]+$` | `listPublishedContentPages` ?slug |
| Kind | radio group | — | Privacy · Terms and conditions · Refund · Cookie · Accessibility | `listPublishedPolicies` ?kind |

**Form: Raise my case** (modal, opened by *Raise my case*; *Raise my case* calls `raiseMyCase`, *Cancel* sends nothing)

**Collects what `raiseMyCase` sends before it is called.** Required: `id`, `kind`, `summary`, `recordedAt`. Optional: `detail`, `venueId`, `orderRef`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Created on the device, so a retry after a dropped connection carries the same id and is the same case. | `raiseMyCase` body |
| Kind `kind` | select | required | — | Lost property · Complaint · Question · Accessibility · Refund request · Other; Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.; A case raised as `other` must carry a non-empty `detail` … | — | What the guest says the case is about, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. | `raiseMyCase` body |
| Summary `summary` | text field | required | — | max length 200 | — | Lands in `Case.subject` — the case's one-line title. | `raiseMyCase` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time when the guest raised it. The server stamps `syncedAt` on arrival; both are kept (naming-and-style 5.2), because the SLA clock starts at `recordedAt`, not at the … | `raiseMyCase` body |
| Detail `detail` | text field | optional | — | — | — | Required, and not empty, when `kind` is `other` (decided 28 September, audit R222); a 400 otherwise. | `raiseMyCase` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `raiseMyCase` body |
| Order ref `orderRef` | text field | optional | — | — | — | — | `raiseMyCase` body |

Errors to draw in the form: 400 `kind` is `other` and `detail` is missing or empty (audit R222), or another field breaks the schema

**Form: Reply to my case** (modal, opened by *Reply to my case*; *Reply to my case* calls `replyToMyCase`, *Cancel* sends nothing)

**Collects what `replyToMyCase` sends before it is called.** Required: `message`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Message `message` | text area | required | — | min length 1; max length 10000 | — | — | `replyToMyCase` body |

#### Outputs: what the screen shows and produces

**Shown**

**Questions and answers** (card list, from `listPublishedFaqs`): Categories in their order, each opening to its questions. Was the generated table 'Every faq category'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Name | in the reader's language | — |
| Entries | list or chips (count when long) | — |

**Help pages** (card list, from `listPublishedContentPages`): The live help pages; the accessibility ones open GST-057.

| Shows | Format | Notes |
|---|---|---|
| Title | in the reader's language | — |
| Icon | the image or video | — |

**Policies** (card list, from `listPublishedPolicies`): The current terms, privacy, refund, cookie and accessibility policies.

| Shows | Format | Notes |
|---|---|---|
| Title | text | — |
| Version | text | The version a consent records (a guest who consented to version 3 consented to version 3). |
| Effective from | 1 Oct 2026 | — |

**My cases** (card list, from `listMyCases`): Only when signed in: the cases this guest raised, newest first.

| Shows | Format | Notes |
|---|---|---|
| Case number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Subject | text | The case's one-line title, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps … |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |
| Recorded at | 1 Oct 2026, 14:30 | Device time the case was raised — the start of the SLA clock. |

**What's new** (card list, from `getTenantAppStatus`): Public, localised release notes from `getTenantAppStatus` `whatsNew`, newest first, at most 10; the staff-only `recentChanges` stays staff only.

| Shows | Format | Notes |
|---|---|---|
| Is published | yes / no (icon or chip) | True once any version has been published. |
| Published version | text | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Draft version | text | Staff only. |
| Has unpublished changes | yes / no (icon or chip) | Staff only. The working draft differs from the current version's `snapshot`. |
| Active module count | 1,234 | Staff only. `ModuleEnablement` rows with `isEnabled` true. |
| Licensed module count | 1,234 | Staff only. `ModuleEnablement` rows with `isLicensed` true. |
| Active page count | 1,234 | Staff only. Content pages that are `published` and enabled. |
| Is in maintenance | yes / no (icon or chip) | — |
| Maintenance message | in the reader's language | — |
| Expected back at | 1 Oct 2026, 14:30 | — |
| Minimum app version | grouped details | The oldest guest app build still allowed to run (decided 28 September, audit R073). |
| Ios | text | — |
| Android | text | — |
| Contact | grouped details | How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided … |
| Phone | +971 50 123 4567 | — |
| Email | email, tap to write | — |
| Whatsapp | text | — |
| Address | in the reader's language | — |
| Opening hours | in the reader's language | Prose, as the guest reads it. The bookable hours are the catalogue's. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Raise my case (primary button) | `raiseMyCase` POST `/my/cases` | inline | Case | 400 `kind` is `other` and `detail` is missing or empty (audit R222), or another field breaks the schema | opens modal first |
| Reply to my case (secondary button) | `replyToMyCase` POST `/my/cases/{caseId}/messages` | inline | CaseDetail | — | opens modal first |

**Data it reads**: `listPublishedFaqs` (onLoad, The published FAQs, readable before sign-in (GFIX-2)); `listPublishedContentPages` (onLoad, The live help and accessibility pages, readable before …); `listMyCases` (onLoad, The cases this guest raised Only when signed in (decided 2 …); `getTenantAppStatus` (onLoad, App status and the public *What's new*); `listPublishedPolicies` (onLoad, Terms, privacy, refund, cookie and accessibility policies …)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `WEB-034` Lost & Found: *They report something lost*; carries `caseId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Questions, pages and policies load in place; each list loads on its own. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the help support untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No help support yet. Offers Raise my case (`raiseMyCase`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listPublishedFaqs` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Reading help needs no sign-in (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-2)). **Raising or reading a case needs a signed-in guest**: one who is not signed in is offered sign-in and brought back to this screen; the questions, pages and policies stay readable. |
| Offline (`?state=offline`) | **The offline banner shows.** Help already loaded stays readable, marked with its age. **Raising a case is disabled offline** — it needs the connection (decided 28 September, audit R148) — and the screen says how to reach staff in person instead: the guest services desk, or any member of staff. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `kind` is `other` and `detail` is missing or empty (audit R222), or another field breaks the schema |

#### Permissions

- `listPublishedFaqs` → no permission · anonymous, guest, device
- `listPublishedContentPages` → no permission · anonymous, guest, device
- `listMyCases` → no permission · guest
- `raiseMyCase` → no permission · guest
- `replyToMyCase` → no permission · guest
- `getTenantAppStatus` → no permission · device, guest
- `listPublishedPolicies` → no permission · anonymous, guest, device

**A refused user sees:** Reading help needs no sign-in (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-2)). **Raising or reading a case needs a signed-in guest**: one who is not signed in is offered sign-in and brought back to this screen; the questions, pages and policies stay readable.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The guest Help screen shows app status and a public, localised "what's new" (release notes). *(agreed · design review 29 Sep 2026, GAP-B2 · B. Help: app status + recent changes · DI-1073)*
- Support chat is native to TICVAI: a built-in AI chat assistant answers first, then escalates to a human "CR representative" role in the platform; offered white-labelled as a subscription add-on for smaller clients. *(agreed · MoM 12 Aug 2026, 10. Customer Support / Chat Integration Approach · DI-256)*
- Configurable FAQ section plus Terms & Conditions, Privacy Policy and Cookie Policy with an accept/deny prompt. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-191)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Availability and maintenance*, set in `CMS-001` Tenant Workspace:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Availability and maintenance message (`maintenance.message`) | English and Arabic (Arabic right to left) | — | — |
| Expected back at (`maintenance.expectedBackAt`) | 1 Oct 2026, 14:30 (venue time zone) | — | — |
| Minimum app version: ios (`maintenance.minimumAppVersion.ios`) | pattern `^\d+\.\d+\.\d+$` | — | — |
| Minimum app version: android (`maintenance.minimumAppVersion.android`) | pattern `^\d+\.\d+\.\d+$` | — | — |
| Contact: phone (`maintenance.contact.phone`) | +971 5X XXX XXXX (E.164) | — | — |
| Contact: email (`maintenance.contact.email`) | name@example.ae | — | — |
| Contact: address (`maintenance.contact.address`) | English and Arabic (Arabic right to left) | — | — |
| Contact: opening hours (`maintenance.contact.openingHours`) | English and Arabic (Arabic right to left) | — | Prose, as the guest reads it. The bookable hours are the catalogue's. |
| Availability (`maintenance.availability`) | Open · Sold out · Closed | Open | The sold-out or closed signal (decided 28 September, audit R073). `open` is the normal state. |
| Availability message (`maintenance.availabilityMessage`) | English and Arabic (Arabic right to left) | — | — |

Also set there, as content the tenant writes: is in maintenance, minimum app version, contact, contact: whatsapp.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-040` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 2 → Help & support*
- Flow F54 *Something goes wrong in the venue*, step 1: They look for an answer first. → **Self-serve before a case.** A support queue full of questions the FAQ answers is a support queue nobody can staff.
- Flow F54 *Something goes wrong in the venue*, step 2: It does not answer, so they raise a case. → **One case mechanism** — a lost item, a bad meal and a refund query are the same object with a different subject.
- Flow F54 branch at step 2 (high): when It is urgent — a child, a medical issue., **Not a case.** The app surfaces how to reach staff physically, and `reportIncident` on the staff side (F69) is what actually happens. **A queue is the wrong response to an emergency.**
- Flow F54 branch at step 2 (medium): when The guest has no connection., **Raising and replying are disabled, not queued** (decided 28 September, audit R148). The screen says the case needs a connection and shows how to reach staff in person — the nearest guest services …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (31 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-040?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Raise my case, Reply to my case.
- [ ] Every transition is wired: `GST-001`, `WEB-034`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-051` Plan

**The Plan tab: tell the venue who is coming, when, at what pace and what you like, and get a day-by-day plan.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #18216 (APP-MOB-GST-051) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | multiStepForm (comfortable density): The v4 prototype asks six questions one at a time (who, heights, days, pace, likes, food) and ends on *Make my plan* |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `venueId` (session) · cold entry: The Plan tab; a cold arrival is the ordinary case and starts at the first question. |
| Route | `/general/plan-your-adventure-start` |

**What the spec says about it.** Minuted 10 Aug §4.9. Benchmarked against Skidata. Tied to a ticket purchase and saved as a personal visit profile. **Out of the first release** (decided 28 September, audit R187): the itinerary planner is deferred and this screen is `wave: 4` with a `deferred` block. Kept, not deleted, for the release that builds it. **Rev 3 (decided 29 September).** Had stayed in wave 4 (GAP-C3); superseded the same day by the re-plan below. **Brought into Block A on 29 September** (Chinmay, the 29 September re-plan, MOB-6): a rules-based planner with the AI planner agent on top. This supersedes audit R187, the deferral half of R209 and rev 3 GAP-C3; the `deferred` block is removed and the screen is wave 1. **Mobile v4 role (MOB-6): the Plan tab root, "Plan".** Inputs: party size, heights (or ages), dates, pace (packed, balanced or relaxed), interests and cuisine. The rules planner (`generateVisitPlan`) runs with no AI. The tab is hidden when the venue turns module `visitPlanner` off. **Multi-venue intelligence (client meeting 30 September, MoM 4.7, Allam; agreed by Chinmay).** In a multi-venue tenant each chosen day is at one park, and the planner uses **only the rides, dining and retail that exist at that park**: a cuisine or shop preference is checked against that park's own points, never assumed of every park (only one park has the Indian restaurant, so *Indian* places lunch there on that park's day and nowhere else). Retail and kiosk shops are now planner options alongside F&B (the gap a Softlabs teammate flagged). Contract: venue-map `generateVisitPlan` `dayVenues`, `retailTags` …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Adults | number field | — | — | — | — | Age 12 and over, at least 1, at most 8. | — |
| Children | number field | — | — | — | — | Age 3 to 11, 0-8. | — |
| How tall are the children? | select field | — | — | — | — | Per child: under 1.0 m, 1.0-1.2 m, 1.2-1.4 m, 1.4 m and over (or an age where the venue sets age rules). Rides over a child's limit are left out, from `ProductEligibilityRule`. | — |
| Which days are you visiting? | multi select | — | — | — | — | Up to three days; each day gets its own park at a multi-park venue. | — |
| Which park each day? | repeatable rows | optional | — | at most 200 | — | **Only in a multi-venue tenant** (more than one entry in `getTenantAppStatus.venues`); hidden otherwise. One choice per chosen day, defaulting to the venue picked on Home; sent as … | `TenantAppStatus.venues` |
| How busy should each day be? | select field | — | — | — | — | Packed, Balanced or Relaxed. | — |
| What are you most interested in? | multi select | — | — | — | — | Interest tags from the venue's points (`VenuePoint.interestTags`): thrill rides, family rides, shows, water, shopping. | — |
| Any shops you'd like to visit? | multi select | — | — | — | — | **Shown when Shopping is chosen above** (client meeting 30 September, MoM 4.7: retail and kiosk shops join F&B in the planner). Options are the `retailTags` of the shops and retail kiosks of the … | — |
| What would you like for lunch? | select field | — | — | — | — | **Cuisines from the dining points of the chosen parks only** (`VenuePoint.cuisineTags` of restaurants, cafes and food kiosks; client meeting 30 September, MoM 4.7). Lunch is planned at a restaurant … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |

**Sent by *Make my plan*** (`generateVisitPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. | `generateVisitPlan` body |
| Day venues `dayVenues` | repeatable rows | optional | — | at most 7; One entry per date that is not at `venueId`; each date of `dates` at most once. | — | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). | `generateVisitPlan` body |
| Date `dayVenues[].date` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `generateVisitPlan` body |
| Venue `dayVenues[].venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `generateVisitPlan` body |
| Dates `dates` | list of values (chips) | required | — | at least 1; at most 7 | — | — | `generateVisitPlan` body |
| Party `party` | repeatable rows | required | — | at least 1; at most 20 | — | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the fallback the rule may also state. | `generateVisitPlan` body |
| Height cm `party[].heightCm` | number field | optional | — | min 40; max 230 | — | — | `generateVisitPlan` body |
| Age years `party[].ageYears` | number field | optional | — | min 0; max 120 | — | — | `generateVisitPlan` body |
| Pace `pace` | segmented control | optional | Relaxed | Packed · Relaxed | — | — | `generateVisitPlan` body |
| Interest tags `interestTags` | list of values (chips) | optional | — | at most 12 | — | The same closed list as `VenuePoint.interestTags`. | `generateVisitPlan` body |
| Cuisine tags `cuisineTags` | list of values (chips) | optional | — | at most 8 | — | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). | `generateVisitPlan` body |
| Retail tags `retailTags` | list of values (chips) | optional | — | at most 8 | — | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options), e.g. | `generateVisitPlan` body |
| Must include points `mustIncludePointIds` | multi-picker: choose must include points | optional | — | at most 10 | — | Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never placed on another venue's day. | `generateVisitPlan` body |
| Preset `preset` | select | optional | — | Highlights · Family · Thrill seeker · Water day · Relaxed · Shows and dining | — | A ready-made day plan (GST-052 Suggested Itineraries): the preset fixes the interests and the pace, and the party still decides eligibility. | `generateVisitPlan` body |
| Preset key `presetKey` | text field | optional | — | max length 64; pattern `^[a-z][a-zA-Z0-9]*$`; An unknown key is refused 422 `unknown-preset`. | — | The ready-made plan the guest took on GST-052 (30 September, second wave of the 29 September pass, MOB-6): one of the built-in `preset` keys above, or a key of a ready-made plan … | `generateVisitPlan` body |
| Start time `startTime` | time picker | optional | — | — | HH:mm, 24-hour | When the party arrives. Null means opening time. | `generateVisitPlan` body |
| Locale `locale` | text field | optional | — | — | — | — | `generateVisitPlan` body |

#### Outputs: what the screen shows and produces

**Shown**

**Plan your visit · n of 6** (progress indicator): Six questions; Heights is skipped when no children are coming.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Make my plan (primary button) | `generateVisitPlan` POST `/visit-plans` | VisitPlanRequest | VisitPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A venue of the plan (`venueId` or a `dayVenues` venue) has no published map, or none of its points carries a … | — |
| Take a ready-made plan (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getWaitTimes` (onLoad, Wait times across a venue); `listProducts` (onLoad, List products); `getTenantAppStatus` (onLoad, The tenant's active venues, for the park-per-day choice in …)

**Where the user goes next**

- → `GST-053` Your Plan: *Make my plan*; carries `planId`; calls `generateVisitPlan`
- → `GST-052` Suggested Itineraries: *Take a ready-made plan*
- → `GST-001` Home: *Home tab*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The plan builds in place; the inputs stay on screen. |
| Error (`?state=error`) | Could not load the plan. Names what failed; the inputs are kept so trying again costs nothing. |
| Empty, first run (`?state=emptyFirstRun`) | No plan yet: the first question is shown. Nothing is saved until *Make my plan*. |
| Empty, no results (`?state=emptyNoResults`) | Nothing suits the whole party on that day (for example every ride is over a child's height): says so and offers to change the answers. |
| Preference not at venue (`?state=preferenceNotAtVenue`) | **A preference no chosen park can meet** (client meeting 30 September, MoM 4.7): a cuisine or shop tag with no matching point at any park of the plan is marked on its chip (*Not at the parks you chose*) before *Make my plan*; the plan is still made without it, never with a restaurant or shop from a park the party is not visiting. Where another park of the tenant has it, the chip says which, and choosing that park for a day brings it in. |
| Permission denied (`?state=emptyNoAccess`) | A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it. |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 422 A venue of the plan (`venueId` or a `dayVenues` venue) has no published map, or none of its points carries a planning duration (`venue-not-plannable`), so … |

#### Permissions

- `getWaitTimes` → no permission · guest, public
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `generateVisitPlan` → no permission · guest
- `getTenantAppStatus` → no permission · device, guest

**A refused user sees:** A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A preference a day's park cannot meet is said, not filled: a "Not at this park" banner per day names the cuisine or shop and the park that has it (e.g. "No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2)."), hidden when all are met. Lunch cuisine options name the parks serving them ("Indian - Summit Peaks only"). *(agreed · MoM 30 Sep 2026, 4.7 · DI-1113)*
- Allam: multi-venue visit planner. In a multi-venue tenant the guest picks a park per chosen day ("Which park each day?", hidden otherwise); each day tab names its park and every item, swap candidate and AI-planner suggestion comes only from that park's rides, dining and shops, never another park's. *(agreed · MoM 30 Sep 2026, 4.7 · DI-1112)*
- Retail/kiosk shops are added to the planner's venue-linked options alongside F&B (previously only F&B). *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1100)*
- Allam: the planner applies multi-venue intelligence; it checks actual venue-level amenities before including a preference, e.g. if only one of several parks has an Indian restaurant. It pulls only rides, F&B and retail available at each specific venue. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1099)*
- Itinerary planner (Yas Island planner reference): party composition (adults/children with height/age), visit dates, pace (packed/balanced/relaxed) and cuisine preferences feed an auto-generated, swappable multi-day itinerary with associated costing. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1098)*
- The visit planner is tied to a ticket purchase and saved as a personal visit profile; benchmarked against Skidata. *(agreed · MoM 10 Aug 2026, 4.9 · DI-242)*
- Chinmay: share an itinerary with a group via an in-app QR code a friend scans to join, or an invite-to-join. *(agreed · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-218)*
- "Plan Your Adventure": guided itinerary planner (Skidata benchmark) where the guest picks which rides/attractions and in what order ahead of time, tied to the ticket purchase and saved as a personal visit profile. *(client request · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-217)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · names this screen)*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Step indicator (`bookingFlow.stepIndicator`) | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | Bar | the step indicator above every booking step: bar, numbered, dots, segmented, breadcrumb, pills, ticks, or none |
| Settings: step indicator (`bookingFlow.venueOverrides[].settings.stepIndicator`) | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | Bar | — |

*Availability and maintenance*, set in `CMS-001` Tenant Workspace:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Availability and maintenance message (`maintenance.message`) | English and Arabic (Arabic right to left) | — | — |
| Expected back at (`maintenance.expectedBackAt`) | 1 Oct 2026, 14:30 (venue time zone) | — | — |
| Minimum app version: ios (`maintenance.minimumAppVersion.ios`) | pattern `^\d+\.\d+\.\d+$` | — | — |
| Minimum app version: android (`maintenance.minimumAppVersion.android`) | pattern `^\d+\.\d+\.\d+$` | — | — |
| Contact: phone (`maintenance.contact.phone`) | +971 5X XXX XXXX (E.164) | — | — |
| Contact: email (`maintenance.contact.email`) | name@example.ae | — | — |
| Contact: address (`maintenance.contact.address`) | English and Arabic (Arabic right to left) | — | — |
| Contact: opening hours (`maintenance.contact.openingHours`) | English and Arabic (Arabic right to left) | — | Prose, as the guest reads it. The bookable hours are the catalogue's. |
| Availability (`maintenance.availability`) | Open · Sold out · Closed | Open | The sold-out or closed signal (decided 28 September, audit R073). `open` is the normal state. |
| Availability message (`maintenance.availabilityMessage`) | English and Arabic (Arabic right to left) | — | — |

Also set there, as content the tenant writes: is in maintenance, minimum app version, contact, contact: whatsapp.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-051` · status **notStarted** · provenance client-verified
- Prototype (mobile v4 (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`, view *Plan tab (Plan your visit · 1 of 6)*
- Flow F49 *A guest plans a day and follows it*, step 1: They answer six questions (party, heights, days, pace, interests, lunch) and choose Make my plan. → **The rules planner, no AI.** A plan per day that leaves out rides over a child's height and plans lunch where the chosen cuisine is served. **Each day uses only its own park's rides, dining and …
- Flow F49 branch at step 1 (recoverable): when Nothing suits the whole party on the chosen day (every ride is over a child's height, or the park is closed)., **Refused with a reason**, naming the answer that ruled everything out, and the answers are kept so changing one costs nothing.
- Flow F49 branch at step 1 (recoverable): when A cuisine or shop the guest chose exists at none of the day's park's points (only one park has the Indian restaurant)., **Said, not faked** (client meeting 30 September, MoM 4.7): the day is planned from that park's own points, `unmatchedPreferences` names the park that has it, and the guest may move the day there by …
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (26), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-051?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, preferenceNotAtVenue, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Make my plan, Take a ready-made plan.
- [ ] Every transition is wired: `GST-053`, `GST-052`, `GST-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 8 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-052` Suggested Itineraries

**Ready-made day plans for this venue that a guest can take instead of answering questions.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #18228 (APP-MOB-GST-052) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | listDetail (comfortable density): `listProducts` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `venueId` (session) · cold entry: Lists the venue's ready-made plans; nothing is needed upstream. |
| Route | `/general/suggested-itineraries` |

**What the spec says about it.** Minuted 10 Aug §4.9. ** wired 24 August.** The board drew four bespoke AI endpoints for itinerary planning; **one operation with a kind answers all of them** (ADR-0028), and recording the outcome is what lets a model replace the heuristic later. **`recordSuggestionOutcome` removed from the guest surface.** `check-screens` refused it and was right: **a guest does not record an outcome — the platform observes what they did.** A guest app that self-reports whether it took the advice is a training label the guest could forge, and the observation belongs server-side where the plan and the visit can be compared. **Out of the first release** (decided 28 September, audit R187): the itinerary planner is deferred and this screen is `wave: 4` with a `deferred` block. Kept, not deleted, for the release that builds it. **Itinerary suggestion removed 28 September** (decided 28 September, audit R209): the planner is deferred (R187) and `requestSuggestion` refuses a guest anything but prepPlan, upsell and waitTime, so this screen no longer asks for a day plan. **Rev 3 (decided 29 September).** Had stayed in wave 4 (GAP-C3); superseded the same day by the re-plan below. **Brought into Block A on 29 September** (Chinmay, the 29 September re-plan, MOB-6): a rules-based planner with the AI planner agent on top. This supersedes audit R187, the deferral half of R209 and rev 3 GAP-C3; the `deferred` block is removed and the screen is wave 1. **Mobile v4 role (MOB-6): ready-made day plans per venue** the guest can take; each is rules-built by `generateVisitPlan` from preset inputs, then edited on …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |

**Sent by *Use this plan*** (`generateVisitPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. | `generateVisitPlan` body |
| Day venues `dayVenues` | repeatable rows | optional | — | at most 7; One entry per date that is not at `venueId`; each date of `dates` at most once. | — | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). | `generateVisitPlan` body |
| Date `dayVenues[].date` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `generateVisitPlan` body |
| Venue `dayVenues[].venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `generateVisitPlan` body |
| Dates `dates` | list of values (chips) | required | — | at least 1; at most 7 | — | — | `generateVisitPlan` body |
| Party `party` | repeatable rows | required | — | at least 1; at most 20 | — | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the fallback the rule may also state. | `generateVisitPlan` body |
| Height cm `party[].heightCm` | number field | optional | — | min 40; max 230 | — | — | `generateVisitPlan` body |
| Age years `party[].ageYears` | number field | optional | — | min 0; max 120 | — | — | `generateVisitPlan` body |
| Pace `pace` | segmented control | optional | Relaxed | Packed · Relaxed | — | — | `generateVisitPlan` body |
| Interest tags `interestTags` | list of values (chips) | optional | — | at most 12 | — | The same closed list as `VenuePoint.interestTags`. | `generateVisitPlan` body |
| Cuisine tags `cuisineTags` | list of values (chips) | optional | — | at most 8 | — | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). | `generateVisitPlan` body |
| Retail tags `retailTags` | list of values (chips) | optional | — | at most 8 | — | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options), e.g. | `generateVisitPlan` body |
| Must include points `mustIncludePointIds` | multi-picker: choose must include points | optional | — | at most 10 | — | Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never placed on another venue's day. | `generateVisitPlan` body |
| Preset `preset` | select | optional | — | Highlights · Family · Thrill seeker · Water day · Relaxed · Shows and dining | — | A ready-made day plan (GST-052 Suggested Itineraries): the preset fixes the interests and the pace, and the party still decides eligibility. | `generateVisitPlan` body |
| Preset key `presetKey` | text field | optional | — | max length 64; pattern `^[a-z][a-zA-Z0-9]*$`; An unknown key is refused 422 `unknown-preset`. | — | The ready-made plan the guest took on GST-052 (30 September, second wave of the 29 September pass, MOB-6): one of the built-in `preset` keys above, or a key of a ready-made plan … | `generateVisitPlan` body |
| Start time `startTime` | time picker | optional | — | — | HH:mm, 24-hour | When the party arrives. Null means opening time. | `generateVisitPlan` body |
| Locale `locale` | text field | optional | — | — | — | — | `generateVisitPlan` body |

#### Outputs: what the screen shows and produces

**Shown**

**Ready-made plans** (card list, from `listProducts`): The venue's preset plans (e.g. *Thrill day*, *Family day*, *Relaxed day*), each a set of planner inputs; **Use this plan** runs `generateVisitPlan` with those inputs and the guest's party size and date. Rules-built, not AI: seeded, not learned, on day one.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Family key | text | The same product at another location (decided 29 September, rev 3 REV3-18). Optional. |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |
| Category | the name it points at, never the id | Taken from their `fnb.product` and `retail.product`, 20 September. `catalogue.product_category` has existed since 20 August with two … |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | — |
| Is sellable | yes / no (icon or chip) | True only when live and carried by a published bundle. Approval and publication are different acts. |
| Is stock tracked | yes / no (icon or chip) | Taken from their `fnb.product`, 20 September. Whether a sale decrements stock, which is not what `isSellable` asks. |
| Has variants | yes / no (icon or chip) | — |
| Variant count | 1,234 | — |
| Segment tags | list or chips (count when long) | 7.3.5. A channel and a segment tag are mandatory and nothing required either. |
| Code schema | text | 7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. `Product.code` existed and nothing required a format, so a venue with three thousand … |

**Every bundle** (data table, from `listCatalogueBundles`): Bundles a preset plan can include (e.g. Fast Track).

| Shows | Format | Notes |
|---|---|---|
| Venue | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Published by | the name it points at, never the id | — |
| Signature key | text | Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle. |
| Stale after | 1 Oct 2026, 14:30 | — |
| Size bytes | 1,234 | — |
| Note | text | — |
| Applied by workstations | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Use this plan (primary button) | `generateVisitPlan` POST `/visit-plans` | VisitPlanRequest | VisitPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A venue of the plan (`venueId` or a `dayVenues` venue) has no published map, or none of its points carries a … | — |

**Data it reads**: `listProducts` (onLoad, List products); `listCatalogueBundles` (onLoad, List published bundles)

**Where the user goes next**

- → `GST-053` Your Plan: *Use this plan*; carries `planId`; calls `generateVisitPlan`
- → `GST-051` Plan: *Make my own*
- → `GST-001` Home: *Home tab*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The plan builds in place; the inputs stay on screen. |
| Error (`?state=error`) | Could not load the plan. Names what failed; the inputs are kept so trying again costs nothing. |
| Empty, first run (`?state=emptyFirstRun`) | The venue has no ready-made plans: says so and offers *Make my own* (GST-051). |
| Empty, no results (`?state=emptyNoResults`) | Nothing suits the whole party on that day (for example every ride is over a child's height): says so and offers to change the answers. |
| Permission denied (`?state=emptyNoAccess`) | A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it. |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 422 A venue of the plan (`venueId` or a `dayVenues` venue) has no published map, or none of its points carries a planning duration (`venue-not-plannable`), so … |

#### Permissions

- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `listCatalogueBundles` → `PRODUCT_VIEW` (read) · staff, guest
- `generateVisitPlan` → no permission · guest

**A refused user sees:** A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Itinerary planner (Yas Island planner reference): party composition (adults/children with height/age), visit dates, pace (packed/balanced/relaxed) and cuisine preferences feed an auto-generated, swappable multi-day itinerary with associated costing. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1098)*
- "Plan Your Adventure": guided itinerary planner (Skidata benchmark) where the guest picks which rides/attractions and in what order ahead of time, tied to the ticket purchase and saved as a personal visit profile. *(client request · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-217)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · names this screen)*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-052` · status **notStarted** · provenance designed · **Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no …
- Prototype (Mobile App v4, 29 September 2026, verified —, match none): `sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html`, view **
- Drawn by: Claude Code, 30 September 2026, drawn in the Mobile App v4 look
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)
- ADR-0028 *Seventeen modules, and the data boundary decides where they split* (`docs/adr/0028-service-decomposition.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-052?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Use this plan.
- [ ] Every transition is wired: `GST-053`, `GST-051`, `GST-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-053` Your Plan

**The plan, day by day: swap, remove or add items, undo, add Fast Track, then book the whole plan.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #18229 (APP-MOB-GST-053) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | listDetail (comfortable density): `listProducts` reads the population and `getCart` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `planId` (GST-051), `venueId` (session), `itemId` (navigation), `cartId` (session) · cold entry: A saved plan opened from a link or the Plan tab. A plan whose dates have passed says so and offers to plan again; a plan that is not this guest's is refused … |
| Route | `/general/build-your-own-itinerary` |

**What the spec says about it.** Minuted 10 Aug §4.9. **Group sharing agreed** — an in-app QR a friend scans to join the itinerary (Chinmay raised, Qossai confirmed). **Out of the first release** (decided 28 September, audit R187): the itinerary planner is deferred and this screen is `wave: 4` with a `deferred` block. Kept, not deleted, for the release that builds it. **Rev 3 (decided 29 September).** Had stayed in wave 4 (GAP-C3); superseded the same day by the re-plan below. **Brought into Block A on 29 September** (Chinmay, the 29 September re-plan, MOB-6): a rules-based planner with the AI planner agent on top. This supersedes audit R187, the deferral half of R209 and rev 3 GAP-C3; the `deferred` block is removed and the screen is wave 1. **Mobile v4 role (MOB-6): "Your Plan".** Per-day itinerary with swap, remove, add and undo (`updateVisitPlan` is versioned), add-ons such as Fast Track, and **Book this plan** → GST-041. **Multi-venue intelligence (client meeting 30 September, MoM 4.7, Allam).** Each day tab is one park, and every item on it (rides, dining, and now retail: shops and kiosks) is at that park; a preference the park cannot meet shows as *Not at this park* rather than being filled from another park.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Day tabs | select field | — | — | — | — | Day 1 · Fri 2 Oct · Summit Peaks … one tab per chosen day; the park is the day's `VisitPlan.days[].venueId` (client meeting 30 September, MoM 4.7). | — |
| Add Fast Track | toggle | — | — | — | — | An add-on from the plan's `addOnSuggestions` (the product GST-048 sells), priced per guest, with the queuing time it saves. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |
| Version | number field | — | min 1 | `getVisitPlan` ?version |

**Sent by *Remove*** (`updateVisitPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Base version `baseVersion` | number field | required | — | min 1 | — | — | `updateVisitPlan` body |
| Changes `changes` | repeatable rows | required | — | at least 1; at most 20 | — | — | `updateVisitPlan` body |
| Op `changes[].op` | select | required | — | Swap · Remove · Add · Move · PIN · Accept add on · Decline add on · Revert to | — | — | `updateVisitPlan` body |
| Item `changes[].itemId` | picker: choose an item | optional | — | — | shows names, sends the id | — | `updateVisitPlan` body |
| Date `changes[].date` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateVisitPlan` body |
| Point `changes[].pointId` | picker: choose a point | optional | — | — | shows names, sends the id | — | `updateVisitPlan` body |
| Performance `changes[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `updateVisitPlan` body |
| Starts at `changes[].startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateVisitPlan` body |
| Version `changes[].version` | number field | optional | — | — | — | For `revertTo`, the earlier version to restore (undo). | `updateVisitPlan` body |

**Sent by *Book this plan*** (`bookVisitPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Base version `baseVersion` | number field | required | — | min 1 | — | The version the guest is looking at. | `bookVisitPlan` body |
| Cart `cartId` | picker: choose a cart | optional | — | — | shows names, sends the id | The guest's open cart. Null creates one. | `bookVisitPlan` body |
| Items `itemIds` | multi-picker: choose items | optional | — | — | — | Only these items. Empty books every bookable item of every day. | `bookVisitPlan` body |
| Include add ons `includeAddOns` | toggle | optional | on | — | — | Also add the add-ons the guest accepted on the plan (`VisitPlanItem.addOnAccepted`). | `bookVisitPlan` body |

#### Outputs: what the screen shows and produces

**Shown**

**The day** (timeline, from `getVisitPlan`): Arrive, then each timed item (ride, show, lunch at a restaurant serving the chosen cuisine, a shop or kiosk stop) with its place and zone; Fast Track marked on the rides it covers. **Every item is at the day's park** (`VisitPlanItem.venueId`; client meeting 30 September, MoM 4.7): retail stops (`kind` `shop`: shops and retail kiosks) sit beside meals, both from that park's own points.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Subject | the name it points at, never the id | The signed-in guest. From the session, never from the body. |
| Session ref | text | The anonymous device session that owns the plan until sign-in. |
| Status | chip: Draft, Booked, Archived | `booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date. |
| Source | chip: Rules, Preset, AI agent | What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. |
| Inputs | grouped details | What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050. |
| Venue | the name it points at, never the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. |
| Day venues | list or chips (count when long) | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). |
| Date | 1 Oct 2026 | — |
| Venue | the name it points at, never the id | — |
| Dates | list or chips (count when long) | — |
| Party | list or chips (count when long) | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the … |
| Height cm | 1,234 | — |
| Age years | 1,234 | — |
| Pace | chip: Packed, Relaxed | — |
| Interest tags | list or chips (count when long) | The same closed list as `VenuePoint.interestTags`. |
| Cuisine tags | list or chips (count when long) | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). |
| Retail tags | list or chips (count when long) | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner … |
| Must include points | list or chips (count when long) | Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never … |

**Left out for your group** (banner, from `getVisitPlan`): Items left out because of a child's height, with the limit (e.g. *Freefall Tower (needs 1.40 m)*), and a must-see at none of the chosen parks (`notAtVenue`).

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Subject | the name it points at, never the id | The signed-in guest. From the session, never from the body. |
| Session ref | text | The anonymous device session that owns the plan until sign-in. |
| Status | chip: Draft, Booked, Archived | `booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date. |
| Source | chip: Rules, Preset, AI agent | What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. |
| Inputs | grouped details | What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050. |
| Venue | the name it points at, never the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. |
| Day venues | list or chips (count when long) | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). |
| Date | 1 Oct 2026 | — |
| Venue | the name it points at, never the id | — |
| Dates | list or chips (count when long) | — |
| Party | list or chips (count when long) | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the … |
| Height cm | 1,234 | — |
| Age years | 1,234 | — |
| Pace | chip: Packed, Relaxed | — |
| Interest tags | list or chips (count when long) | The same closed list as `VenuePoint.interestTags`. |
| Cuisine tags | list or chips (count when long) | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). |
| Retail tags | list or chips (count when long) | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner … |
| Must include points | list or chips (count when long) | Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never … |

**Not at this park** (banner, from `getVisitPlan`): **Per day, what the day's park could not offer** (client meeting 30 September, MoM 4.7): e.g. *No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2).* Names the other park from `availableAtVenueIds`, or says no park has it. Lunch that day is at the park's best other restaurant, marked as such. Hidden when every preference is met.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Subject | the name it points at, never the id | The signed-in guest. From the session, never from the body. |
| Session ref | text | The anonymous device session that owns the plan until sign-in. |
| Status | chip: Draft, Booked, Archived | `booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date. |
| Source | chip: Rules, Preset, AI agent | What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. |
| Inputs | grouped details | What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050. |
| Venue | the name it points at, never the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. |
| Day venues | list or chips (count when long) | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). |
| Date | 1 Oct 2026 | — |
| Venue | the name it points at, never the id | — |
| Dates | list or chips (count when long) | — |
| Party | list or chips (count when long) | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the … |
| Height cm | 1,234 | — |
| Age years | 1,234 | — |
| Pace | chip: Packed, Relaxed | — |
| Interest tags | list or chips (count when long) | The same closed list as `VenuePoint.interestTags`. |
| Cuisine tags | list or chips (count when long) | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). |
| Retail tags | list or chips (count when long) | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner … |
| Must include points | list or chips (count when long) | Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never … |

**Estimated total** (detail panel, from `getVisitPlan`): Estimated price for the group and days; the guest confirms dates and tickets in the basket.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Subject | the name it points at, never the id | The signed-in guest. From the session, never from the body. |
| Session ref | text | The anonymous device session that owns the plan until sign-in. |
| Status | chip: Draft, Booked, Archived | `booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date. |
| Source | chip: Rules, Preset, AI agent | What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. |
| Inputs | grouped details | What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050. |
| Venue | the name it points at, never the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. |
| Day venues | list or chips (count when long) | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). |
| Date | 1 Oct 2026 | — |
| Venue | the name it points at, never the id | — |
| Dates | list or chips (count when long) | — |
| Party | list or chips (count when long) | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the … |
| Height cm | 1,234 | — |
| Age years | 1,234 | — |
| Pace | chip: Packed, Relaxed | — |
| Interest tags | list or chips (count when long) | The same closed list as `VenuePoint.interestTags`. |
| Cuisine tags | list or chips (count when long) | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). |
| Retail tags | list or chips (count when long) | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner … |
| Must include points | list or chips (count when long) | Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never … |

**The wait time** (detail panel, from `getWaitTimes`): Live waits beside the rides on today's plan.

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
| Swap (secondary button) | `listVisitPlanAlternatives` GET `/visit-plans/{planId}/items/{itemId}/alternatives` | — | VisitPlanAlternative (paged) | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Remove (destructive button) | `updateVisitPlan` PUT `/visit-plans/{planId}` | VisitPlanUpdate | VisitPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `baseVersion` is not the current version (`plan-version-conflict`), or the plan is already `booked` … | — |
| + Add something (secondary button) | `listVisitPlanAlternatives` GET `/visit-plans/{planId}/items/{itemId}/alternatives` | — | VisitPlanAlternative (paged) | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Undo changes (secondary button) | `updateVisitPlan` PUT `/visit-plans/{planId}` | VisitPlanUpdate | VisitPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `baseVersion` is not the current version (`plan-version-conflict`), or the plan is already `booked` … | — |
| Book this plan (primary button) | `bookVisitPlan` POST `/visit-plans/{planId}/booking` | inline | VisitPlanBooking | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `baseVersion` is not current (`plan-version-conflict`), or the cart is not the caller's or is no longer open … | — |
| Refine with the AI planner (secondary button) | navigation or local | — | — | — | — |
| Change answers (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getCart` (onLoad, The cart, priced and checked, right now With the guest …); `listProducts` (onLoad, List products); `getWaitTimes` (onLoad, Wait times across a venue); `getVisitPlan` (onLoad, The plan: days, timed items and add-on suggestions, at its …)

**Where the user goes next**

- → `GST-041` Checkout Entry: *Book this plan*; carries `cartId`; calls `bookVisitPlan`
- → `GST-054` AI Planner: *Refine with the AI planner*; carries `planId`
- → `GST-051` Plan: *Change answers*
- → `GST-048` Upsell / Cross-Sell: *More add-ons*; carries `cartId`
- → `GST-059` Plan in Progress: *On the day: follow the plan*; carries `planId`
- → `GST-001` Home: *Home tab*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The plan builds in place; the inputs stay on screen. |
| Error (`?state=error`) | Could not load the plan. Names what failed; the inputs are kept so trying again costs nothing. |
| Empty, first run (`?state=emptyFirstRun`) | No plan yet: offers the questions (GST-051) or a ready-made plan (GST-052). |
| Empty, no results (`?state=emptyNoResults`) | Nothing suits the whole party on that day (for example every ride is over a child's height): says so and offers to change the answers. |
| Preference not at venue (`?state=preferenceNotAtVenue`) | **A day whose park cannot meet a preference** (client meeting 30 September, MoM 4.7): the day is shown in full with the *Not at this park* banner naming the cuisine or shop and where it is instead; nothing from another park is placed. *Change answers* (GST-051) lets the guest move that day to the park that has it. An empty swap sheet says the day's park has no other option of that kind, not that none exists anywhere. |
| Permission denied (`?state=emptyNoAccess`) | A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it. |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 409 `baseVersion` is not current (`plan-version-conflict`), or the cart is not the caller's or is no longer open (`cart-not-open`).; 409 `baseVersion` is not the current version (`plan-version-conflict`), or the plan is already `booked` … |

#### Permissions

- `getCart` → no permission · guest, partner, staff
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `getWaitTimes` → no permission · guest, public
- `getVisitPlan` → no permission · guest
- `updateVisitPlan` → no permission · guest
- `listVisitPlanAlternatives` → no permission · guest
- `bookVisitPlan` → no permission · guest

**A refused user sees:** A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.9.2 | The system should provide a service to enable the dynamic composition of the shop cart. The system must provide back all the information in real time, such as the performance availabilities of an … | Ticketing Sales | CONTRACTED | `getCart` |
| 2.9.5 | The system should highlight conflicting times at different attractions when trying to purchase tickets in the same time-slot for one guest. For example, if a ticket for Golf 1 to 2 pm has been added … | Ticketing Sales | CONTRACTED | `getCart` |
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A preference a day's park cannot meet is said, not filled: a "Not at this park" banner per day names the cuisine or shop and the park that has it (e.g. "No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2)."), hidden when all are met. Lunch cuisine options name the parks serving them ("Indian - Summit Peaks only"). *(agreed · MoM 30 Sep 2026, 4.7 · DI-1113)*
- Allam: multi-venue visit planner. In a multi-venue tenant the guest picks a park per chosen day ("Which park each day?", hidden otherwise); each day tab names its park and every item, swap candidate and AI-planner suggestion comes only from that park's rides, dining and shops, never another park's. *(agreed · MoM 30 Sep 2026, 4.7 · DI-1112)*
- Retail/kiosk shops are added to the planner's venue-linked options alongside F&B (previously only F&B). *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1100)*
- Allam: the planner applies multi-venue intelligence; it checks actual venue-level amenities before including a preference, e.g. if only one of several parks has an Indian restaurant. It pulls only rides, F&B and retail available at each specific venue. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1099)*
- Itinerary planner (Yas Island planner reference): party composition (adults/children with height/age), visit dates, pace (packed/balanced/relaxed) and cuisine preferences feed an auto-generated, swappable multi-day itinerary with associated costing. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1098)*
- Itinerary group sharing: an in-app QR code a friend scans to join the itinerary (Chinmay raised, Qossai confirmed). *(agreed · MoM 10 Aug 2026, 4.9 · DI-241)*
- Chinmay: share an itinerary with a group via an in-app QR code a friend scans to join, or an invite-to-join. *(agreed · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-218)*
- "Plan Your Adventure": guided itinerary planner (Skidata benchmark) where the guest picks which rides/attractions and in what order ahead of time, tied to the ticket purchase and saved as a personal visit profile. *(client request · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-217)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · names this screen)*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-053` · status **notStarted** · provenance client-verified
- Prototype (mobile v4 (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`, view *Plan tab → the six questions → Make my plan (Your plan)*
- Flow F49 *A guest plans a day and follows it*, step 2: They swap, remove and add items, undo a change and add Fast Track. → **Every change is a new version**, so undo is one step back. Swap candidates suit everyone in the party.
- Flow F49 *A guest plans a day and follows it*, step 4: They choose Book this plan. → The plan and its add-ons become cart lines; the guest confirms dates and tickets in the basket.
- Flow F49 branch at step 4 (recoverable): when An item sold out after the plan was made., The basket is not built for that item; the guest is told which one and offered a swap, and the rest of the plan is kept.
- ADR-0045 *Every order carries a proven contact, and the gate is the checkout page* (`docs/adr/0045-every-order-carries-a-proven-contact.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 403, 404, 409, 410, 422).
- [ ] Every output is drawn (91 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-053?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, preferenceNotAtVenue, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Swap, Remove, + Add something, Undo changes, Book this plan, Refine with the AI planner, Change answers.
- [ ] Every transition is wired: `GST-041`, `GST-054`, `GST-051`, `GST-048`, `GST-059`, `GST-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 8 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-054` AI Planner

**Ask the planner in your own words to change the plan; it refines the rules plan, and the rules plan stays if AI is unavailable.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 1 · needs the `ai` module |
| Block | Block A · ticket #18217 (APP-MOB-GST-054) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | listDetail (comfortable density): `listProducts` reads the population and `getWaitTimes` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `planId` (GST-053), `conversationId` (deepLink), `venueId` (session) · cold entry: A planner link from a notification: opens the plan and its conversation, or the plan alone if the conversation was closed. |
| Route | `/general/ai-optimized-itinerary` |

**What the spec says about it.** Minuted 10 Aug §4.9. **The AI half is Wave 2** — the manual planner must work without it (CF-41). **Guest concierge confirmed in Phase 1 on 17 August (CF-14), charged per token and bounded by `AiPolicy.guestCapabilityScope`.** Still degrades to the manual planner rather than to an error. ** wired 24 August.** The board drew four bespoke AI endpoints for itinerary planning; **one operation with a kind answers all of them** (ADR-0028), and recording the outcome is what lets a model replace the heuristic later. **`recordSuggestionOutcome` removed from the guest surface.** `check-screens` refused it and was right: **a guest does not record an outcome — the platform observes what they did.** A guest app that self-reports whether it took the advice is a training label the guest could forge, and the observation belongs server-side where the plan and the visit can be compared. **Out of the first release** (decided 28 September, audit R187): the itinerary planner is deferred and this screen is `wave: 4` with a `deferred` block. Kept, not deleted, for the release that builds it. **Itinerary suggestion removed 28 September** (decided 28 September, audit R209): the planner is deferred (R187) and `requestSuggestion` refuses a guest anything but prepPlan, upsell and waitTime, so this screen no longer asks for a day plan. **Rev 3 (decided 29 September).** Had stayed in wave 4 (GAP-C3); superseded the same day by the re-plan below. **Brought into Block A on 29 September** (Chinmay, the 29 September re-plan, MOB-6): a rules-based planner with the AI planner agent on top. This supersedes …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |
| Version | number field | — | min 1 | `getVisitPlan` ?version |

**Sent by *Apply this change*** (`updateVisitPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Base version `baseVersion` | number field | required | — | min 1 | — | — | `updateVisitPlan` body |
| Changes `changes` | repeatable rows | required | — | at least 1; at most 20 | — | — | `updateVisitPlan` body |
| Op `changes[].op` | select | required | — | Swap · Remove · Add · Move · PIN · Accept add on · Decline add on · Revert to | — | — | `updateVisitPlan` body |
| Item `changes[].itemId` | picker: choose an item | optional | — | — | shows names, sends the id | — | `updateVisitPlan` body |
| Date `changes[].date` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateVisitPlan` body |
| Point `changes[].pointId` | picker: choose a point | optional | — | — | shows names, sends the id | — | `updateVisitPlan` body |
| Performance `changes[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `updateVisitPlan` body |
| Starts at `changes[].startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateVisitPlan` body |
| Version `changes[].version` | number field | optional | — | — | — | For `revertTo`, the earlier version to restore (undo). | `updateVisitPlan` body |

#### Outputs: what the screen shows and produces

**Shown**

**Your plan** (timeline, from `getVisitPlan`): The current plan version, updated as the agent changes it.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Subject | the name it points at, never the id | The signed-in guest. From the session, never from the body. |
| Session ref | text | The anonymous device session that owns the plan until sign-in. |
| Status | chip: Draft, Booked, Archived | `booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date. |
| Source | chip: Rules, Preset, AI agent | What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. |
| Inputs | grouped details | What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050. |
| Venue | the name it points at, never the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. |
| Day venues | list or chips (count when long) | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). |
| Date | 1 Oct 2026 | — |
| Venue | the name it points at, never the id | — |
| Dates | list or chips (count when long) | — |
| Party | list or chips (count when long) | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the … |
| Height cm | 1,234 | — |
| Age years | 1,234 | — |
| Pace | chip: Packed, Relaxed | — |
| Interest tags | list or chips (count when long) | The same closed list as `VenuePoint.interestTags`. |
| Cuisine tags | list or chips (count when long) | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). |
| Retail tags | list or chips (count when long) | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner … |
| Must include points | list or chips (count when long) | Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never … |

**Ask the planner** (assistant panel, from `sendAiMessage`): e.g. *More shows, fewer coasters on day 2*. The agent calls `requestSuggestion` kind `itinerary` and applies the result with `updateVisitPlan`; Undo on GST-053 reverts it. **Grounded in each day's park** (client meeting 30 September, MoM 4.7): it proposes only rides, dining and shops (kiosks included) that the plan operations return for that day's venue; asked for something the park lacks …

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Conversation | the name it points at, never the id | — |
| Role | chip: User, Assistant, System | — |
| Content | text | — |
| Sources | list or chips (count when long) | The sources an answer was grounded in, stored with the answer (8.3.70). One `jsonb` column on the row that carries it — … |
| Kind | chip: Document, Product, Entitlement, Report, Record | — |
| ID | text | — |
| Title | text | — |
| Collection | the name it points at, never the id | — |
| Excerpt | text | — |
| Relevance | 1,234.5 | — |
| Confidence | 1,234.5 | 8.1.5, 8.3.67. Nullable on purpose — a provider that does not report confidence must yield null rather than an invented number, and an … |
| Rationale | text | 8.3.68, 8.3.69. |
| Proposed action | grouped details | Present where the answer suggests a change. A draft, never applied here. |
| ID | the name it points at, never the id | — |
| Interaction | the name it points at, never the id | — |
| Kind | chip: Pricing, Promotion, Operational, Financial, Configuration, Content… | `content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from … |
| Target contract | text | Which contract would perform it. The assistant never performs it itself. |
| Target operation | text | — |
| Payload | grouped details | The request body a person would submit, ready to review. Open on purpose: its shape is the request body of `targetOperation` in … |

**Planner unavailable** (banner, from `getVisitPlan`): **The rules plan never fails over to an error**: with AI off, not licensed or failing, the guest keeps the rules plan and the Plan tab works in full. Shown when AI is off for the venue, the tenant has no AI licence, or the call fails or times out.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Subject | the name it points at, never the id | The signed-in guest. From the session, never from the body. |
| Session ref | text | The anonymous device session that owns the plan until sign-in. |
| Status | chip: Draft, Booked, Archived | `booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date. |
| Source | chip: Rules, Preset, AI agent | What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. |
| Inputs | grouped details | What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050. |
| Venue | the name it points at, never the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. |
| Day venues | list or chips (count when long) | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). |
| Date | 1 Oct 2026 | — |
| Venue | the name it points at, never the id | — |
| Dates | list or chips (count when long) | — |
| Party | list or chips (count when long) | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the … |
| Height cm | 1,234 | — |
| Age years | 1,234 | — |
| Pace | chip: Packed, Relaxed | — |
| Interest tags | list or chips (count when long) | The same closed list as `VenuePoint.interestTags`. |
| Cuisine tags | list or chips (count when long) | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). |
| Retail tags | list or chips (count when long) | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner … |
| Must include points | list or chips (count when long) | Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never … |

**The wait time** (detail panel, from `getWaitTimes`): Live waits the agent plans around.

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
| Apply this change (primary button) | `updateVisitPlan` PUT `/visit-plans/{planId}` | VisitPlanUpdate | VisitPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `baseVersion` is not the current version (`plan-version-conflict`), or the plan is already `booked` … | — |
| Back to your plan (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getWaitTimes` (onLoad, Wait times across a venue); `getVisitPlan` (onLoad, The plan: days, timed items and add-on suggestions, at its …); `createAiConversation` (onLoad, Open the planner conversation for this plan Only when …)

**Where the user goes next**

- → `GST-053` Your Plan: *Back to your plan*; carries `planId`
- → `GST-059` Plan in Progress: *They follow it through the day*; carries `planId`
- → `GST-001` Home: *Home tab*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The plan builds in place; the inputs stay on screen. |
| Error (`?state=error`) | Could not load the plan. Names what failed; the inputs are kept so trying again costs nothing. |
| Empty, first run (`?state=emptyFirstRun`) | No conversation yet: the plan is shown with example requests. |
| Empty, no results (`?state=emptyNoResults`) | Nothing suits the whole party on that day (for example every ride is over a child's height): says so and offers to change the answers. |
| Permission denied (`?state=emptyNoAccess`) | A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it. |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| AI unavailable (`?state=aiUnavailable`) | **Falls back to the rules plan, never to an error** (MOB-6): the plan from `getVisitPlan` stays on screen with a short note, and the guest carries on editing it on GST-053. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `baseVersion` is not the current version (`plan-version-conflict`), or the plan is already `booked` (`plan-booked`; a booked plan is read-only, generate a new …; 422 A change names an item not on the plan, a `revertTo` version that does not exist, or a point the party is not eligible for (`item-not-eligible`, with the rule …; 422 A setting the answer cannot do without is missing (29 … |
| In progress (`plannerMode`) | starts at *rulesPlan*; *rulesPlan*: The rules plan is shown; the chat is open.; *refining*: The agent is working on a request.; *proposed*: A change is proposed, not yet saved.; *aiUnavailable*: **The rules plan never fails over to an error**: with AI off, not licensed or failing, the guest keeps the rules plan … |

#### Permissions

- `getWaitTimes` → no permission · guest, public
- `sendAiMessage` → `AI_USE` (operate) · staff, guest
- `getVisitPlan` → no permission · guest
- `updateVisitPlan` → no permission · guest
- `createAiConversation` → `AI_USE` (operate) · staff, guest
- `requestSuggestion` → `AI_USE` (operate) · staff, guest

**A refused user sees:** A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it.

#### Requirements it meets

29 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 8.1.5 | Explainability System shall provide reasoning and confidence indicators where available. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.19 | System shall support AI-powered ticketing assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.20 | System shall support AI-powered support assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 18.10.1 | AI Assistant - System shall provide an AI assistant for employees. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.3 | Operational Queries - Users shall retrieve operational information through AI. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.4 | Work Order Assistance - AI shall assist users with work order activities. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.5 | Knowledge Base Assistance - AI shall provide access to operational knowledge and procedures. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 22.8.4 | AI Chatbot Assistant | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| … 17 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A preference a day's park cannot meet is said, not filled: a "Not at this park" banner per day names the cuisine or shop and the park that has it (e.g. "No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2)."), hidden when all are met. Lunch cuisine options name the parks serving them ("Indian - Summit Peaks only"). *(agreed · MoM 30 Sep 2026, 4.7 · DI-1113)*
- Allam: multi-venue visit planner. In a multi-venue tenant the guest picks a park per chosen day ("Which park each day?", hidden otherwise); each day tab names its park and every item, swap candidate and AI-planner suggestion comes only from that park's rides, dining and shops, never another park's. *(agreed · MoM 30 Sep 2026, 4.7 · DI-1112)*
- Allam: the planner applies multi-venue intelligence; it checks actual venue-level amenities before including a preference, e.g. if only one of several parks has an Indian restaurant. It pulls only rides, F&B and retail available at each specific venue. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1099)*
- "Plan Your Adventure": guided itinerary planner (Skidata benchmark) where the guest picks which rides/attractions and in what order ahead of time, tied to the ticket purchase and saved as a personal visit profile. *(client request · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-217)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · names this screen)*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-054` · status **notStarted** · provenance client-verified
- Prototype (mobile v4 (30 September build), verified 2026-10-01, match partial): `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`, view *Ask Sahli (the assistant chat; v4 has no plan-specific chat)*. Differences: v4 draws the rules plan and a general assistant chat; it has no plan-specific chat. Built from this definition.
- Flow F49 *A guest plans a day and follows it*, step 3: They ask the AI planner to change the plan in their own words. → **The agent refines the rules plan** through the plan operations (`requestSuggestion` kind `itinerary`, guest-allowed since 29 September). With AI off or failing the rules plan stays.
- Flow F49 branch at step 3 (recoverable): when AI is off for the venue, not licensed, or the call fails or times out., **Falls back to the rules plan, never to an error.** The planner chat says it is unavailable; everything on GST-053 keeps working.
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)
- ADR-0028 *Seventeen modules, and the data boundary decides where they split* (`docs/adr/0028-service-decomposition.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (71 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-054?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline, aiUnavailable.
- [ ] Every action is wired with its success and its failure: Apply this change, Back to your plan.
- [ ] Every transition is wired: `GST-053`, `GST-059`, `GST-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

## Tenant configuration on every guest screen

Every guest screen in this batch is white-label. These elements are set by the tenant in the CMS and apply to every screen of the guest app (each screen's block lists the ones particular to it). **Draw with the default theme; on the key screens add one alternate tenant theme** (below), so a reviewer sees the brand is configuration, not paint. The full map, with the input-to-output examples: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Element | Configured in | Allowed values | Default | What it changes |
|---|---|---|---|---|
| Logo (`brand.logoAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo in the header or nav bar, the splash and the footer |
| Logo dark image (`brand.logoDarkAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo on dark backgrounds (falls back to the primary logo) |
| Logo variant (`brand.logoVariant`) | `CMS-002`, `CMS-004`, `ADM-016` | Light · Dark · Duotone | Light | which logo lockup sits in the nav bar, and whose colours drive the theme |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Splash image (`brand.splashImageAssetRefs`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG, JPG, SVG or MP4 from the media library | — | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). |
| Splash duration seconds (`brand.splashDurationSeconds`) | `CMS-002`, `CMS-004`, `ADM-016` | min 0; max 10 | 3 | — |
| Splash background colour (`brand.splashBackgroundColour`) | `CMS-002`, `CMS-004`, `ADM-016` | #RRGGBB | — | — |
| Show loading indicator (`brand.showLoadingIndicator`) | `CMS-002`, `CMS-004`, `ADM-016` | — | on | — |
| Intro video (`brand.introVideoAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode (`brand.introVideoMode`) | `CMS-002`, `CMS-004`, `ADM-016` | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | Off | When GST-001 plays it full screen. "Skip introduction" is always shown. |
| Primary colour (`theme.primaryColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | the brand colour (the `accentSolid` token): primary buttons (Book, Continue, Add to cart, Pay), the active step of the step indicator, selected date and time chips, focus rings |
| Secondary colour (`theme.secondaryColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | secondary buttons and secondary emphasis: unselected chips, secondary tabs |
| Accent colour (`theme.accentColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | highlights: badges (LIMITED, NEW, BESTSELLER), availability counts, sale prices |
| Background colour (`theme.backgroundColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | the page background behind every screen (the `ground` token) |
| Text colour (`theme.textColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | body text on the background |
| Dark mode (`theme.darkMode`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | the dark variant on a device in dark mode (mobile app); derived from the light theme when absent |
| Corner radius (`theme.cornerRadius`) | `CMS-005`, `CMS-003`, `ADM-016` | min 0; max 32 | — | the corners of cards, buttons, inputs, sheets and the cart (0 square to 22 the prototype's roundest) |
| Surface style (`theme.surfaceStyle`) | `CMS-005`, `CMS-003`, `ADM-016` | Glass · Solid | Glass | cards and panels: frosted glass (default) or opaque (the `surfaceRaised` token) |
| Button style (`theme.buttonStyle`) | `CMS-005`, `CMS-003`, `ADM-016` | Solid · Outline · Pill | Solid | every button's shape: solid fill, outline, or pill |
| Component colours (`theme.componentColours`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. |
| Primary latin (`fonts.primaryLatin`) | `CMS-003` | — | — | headings and body text in English |
| Primary arabic (`fonts.primaryArabic`) | `CMS-003` | Required when `ar` is among the tenant's languages (audit R163). | — | headings and body text in Arabic |
| Secondary latin (`fonts.secondaryLatin`) | `CMS-003` | — | — | the secondary face (eyebrows, numbers) in English |
| Secondary arabic (`fonts.secondaryArabic`) | `CMS-003` | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). | — | the secondary face in Arabic |
| Custom font images (`fonts.customFontAssetRefs`) | `CMS-003` | PNG, JPG, SVG or MP4 from the media library | — | Uploaded font files, as `MediaAsset` ids. |
| Header layout (`header.layout`) | `CMS-007` | Logo left · Logo centre · Logo with menu | — | the header: logo left, logo centred, or logo with the menu |
| Show logo (`header.showLogo`) | `CMS-007` | — | on | — |
| Show menu (`header.showMenu`) | `CMS-007` | — | on | — |
| Show notifications (`header.showNotifications`) | `CMS-007` | — | on | — |
| Background colour (`header.backgroundColour`) | `CMS-007` | #RRGGBB | — | — |
| Navigation kind (`navigation.kind`) | `CMS-009` | Bottom navigation · Drawer · Tabs | — | the main navigation: bottom tab bar, drawer, or tabs |
| Navigation items (`navigation.items`) | `CMS-009` | at most 12 | — | — |
| Buy button (`navigation.buyButton`) | `CMS-009` | — | — | The persistent Buy tickets button (decided 29 September, MOB-2). On every screen of the mobile app except the booking and checkout steps; it opens GST-003. |
| Footer columns (`footer.columns`) | `CMS-007` | — | — | — |
| Legal links (`footer.legalLinks`) | `CMS-007` | — | — | Required links, held separately from the free-form columns — a tenant reorganising their footer must not be able to remove the privacy notice by accident. |
| Copyright text (`footer.copyrightText`) | `CMS-007` | — | — | — |
| Social links (`footer.socialLinks`) | `CMS-007` | — | — | — |
| Languages (`languages.languages`) | `CMS-011`, `ADM-018` | at least 1 | — | the language button in the header; Arabic flips every screen right to left |
| Default language (`languages.defaultLanguage`) | `CMS-011`, `ADM-018` | ISO 639-1 code, shown as the language name | — | the language a first visit opens in |
| Modules (`modules.modules`) | `CMS-001` | — | — | — |
| Features (`features.features`) | `CMS-001` | — | — | — |
| Custom domain hostname (`domains.hostname`) | `CMS-017`, `ADM-017` | — | — | — |
| Custom domain kind (`domains.kind`) | `CMS-017`, `ADM-017` | Guest web · Guest app · Partner portal · Developer portal | — | — |
| Verification method (`domains.verificationMethod`) | `CMS-017`, `ADM-017` | Dns txt · Cname · Http file | Dns txt | — |
| Entity kind (`seo.entityKind`) | `CMS-013` | Content page · Product · Event · Performance · Membership · Promotion · Venue | — | — |
| Entity (`seo.entityId`) | `CMS-013` | shows names, sends the id | — | — |
| Locale (`seo.locale`) | `CMS-013` | — | — | — |
| SEO metadata title (`seo.title`) | `CMS-013` | — | — | — |
| Meta description (`seo.metaDescription`) | `CMS-013` | — | — | — |
| Keywords (`seo.keywords`) | `CMS-013` | — | — | — |
| Canonical URL (`seo.canonicalUrl`) | `CMS-013` | — | — | — |
| Slug (`seo.slug`) | `CMS-013` | — | — | 22.11.6. Human-readable, and changing one is a redirect rather than an edit — a slug that changes without a 301 is a page that was ranking and now is not. |
| Hreflang (`seo.hreflang`) | `CMS-013` | — | — | 22.11.11. Which URL serves which language, and getting this wrong on a bilingual venue site splits its own ranking between two versions of the same page. |
| Schema org type (`seo.schemaOrgType`) | `CMS-013` | — | — | — |
| Open graph (`seo.openGraph`) | `CMS-013` | — | — | — |
| Is auto generated (`seo.isAutoGenerated`) | `CMS-013` | — | on | 22.11.2. Generated by default and overridable. |
| No index (`seo.noIndex`) | `CMS-013` | — | off | — |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Component colours: primary CTA (`theme.componentColours.primaryCta`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | the one main call to action on each screen, when it should differ from the brand colour |
| Component colours: pay button (`theme.componentColours.payButton`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | the Pay button at checkout |
| Buy button: style (`navigation.buyButton.style`) | `CMS-009` | Raised · Floating · Flat · Hidden | Raised | the Buy tickets button in the tab bar: raised (default), floating, flat, or hidden |

**The alternate tenant theme (Coastal Aqua)**: Primary colour #0077B6; Secondary colour #023E8A; Accent colour #FFB703; Background colour #F5FAFC; Text colour #0B1324; Corner radius 18; Surface style Solid; Button style Pill; Logo variant Duotone; Header layout Logo centre; Step indicator Dots; Card layout Cards across; Card size Standard; Cart layout Floating icon; Fonts Poppins / Tajawal.
**Key screens to show in it:** `WEB-001`, `WEB-005`, `WEB-006`, `WEB-010`, `WEB-012`, `GST-001`, `GST-007`, `GST-041`, `KSK-002`, `KSK-003`.

**Never configurable:** The *Powered by TICVAI* credit in the footer is fixed and never client-editable (MoM 3 Aug, DI-111; MoM 12 Aug, DI-250). Semantic colour pairs (success, warning, danger, neutral) are not overridable: a tenant who recolours danger to their brand green has made a destructive confirmation look like a success (`screens/_design-tokens.yaml` whiteLabel). Site structure and the navigation flow are fixed and adapt to the product configuration (MoM 3 Aug, DI-119); a guest always books a product or package, never a resource (DI-502). A colour pair that fails 4.5:1 contrast is refused by the CMS, not warned (setTheme 400 ContrastProblem, audit R139).

## Reference designs and the trackers for this platform

**P02 reference designs** (from `handoff/design-batches/apps/1-guest-app/README.md`)

- `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`: Mobile App v4, the newest guest look (29 September, with the 30 September feedback in the booking flows). It replaces the 28 September Mobile v2 build.
- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the booking engine that runs inside the app. Keep both files in the same folder.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-026, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-038, DI-040, DI-042, DI-044, DI-045, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P02 as a whole** (30: 3 open, 27 closed). Open first; a closed row says where it went on 30 September.

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker)*
- **S9** Final UI/UX for the website and the mobile app *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **T1** Feedback on the revised website and mobile wireframes *(Allam / Qossai · Open · due 1 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A28** Review the 'Viva Ticket' website as a reference for ticket-flow variations *(Softlabs Design Team · Low · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A29** Collate design references/inspiration and share with TICVAI, organized by mobile app, website, and admin/back-office pages *(Softlabs (Sahil & Aishwarya) · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A55** Implement per-tenant module visibility toggles (e.g., hide Dining, Retail, or other services) configurable independently for the guest website and mobile app *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker)*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker)*
- **A115** Apply HA selectively to revenue-critical components (ticketing, POS, B2C) same-region, with multi-region DR as an optional add-on *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 24 Aug 2026 · workshop tracker)*
- **A118** Commission the third-party penetration test before go-live (ticketing, B2C, B2B, mobile apps) and resolve all severities *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 24 Aug 2026 · workshop tracker)*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker)*
- … 16 more in `handoff/design-inputs/task-tracker-index.json`

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

### Across P02 Guest App

- Font, header/footer (not yet in the current wireframe build), card size and layout are configurable in the mobile app, consistent with the web app's white-labelling approach. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1097)*
- Step-indicator style is configurable, the same as on the web: bars, dots, counters or step names. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1093)*
- Products can be presented in multiple card layout styles: carousel, video poster, split, etc. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1089)*
- The home-screen navigation bar layout is configurable: home/explore/map/buy-tickets in different arrangements. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1087)*
- The revised mobile app design is approved in direction: Qossai liked the opening video and visual polish, Allam the UI/graphics quality. Its flow is deliberately different from the web application (after front-end team input), not a reused structure. Detailed feedback to follow. *(agreed · MoM 30 Sep 2026, 4.4 Guest Mobile App — Revised Design Walkthrough · DI-1086)*
- Every web product and flow stays bookable in the mobile app (incl. cabanas, surf, 2D/3D stadium, theatre plan, bus route map), each with its own step order; a toggle switches back to one decision per screen. *(agreed · design review 29 Sep 2026, Mobile app (v4) — All web products and flows available · DI-1084)*
- Mobile app must not open straight into booking (client found it unclear). Tabs: Home · Explore · Plan · Tickets (Yas Island / Six Flags references), with a persistent "Buy tickets" button on every screen (raised centre button, or floating / flat per venue). *(agreed · design review 29 Sep 2026, Mobile app (v4) — Tabs Home · Explore · Plan · Tickets, persistent Buy tickets · DI-1081)*
- **Open question.** Real venue photos, clips and logos are still to come from the client; designs use stand-ins. Slots expected: a photo per ticket card and clip per card, a square shot per extra/shop item, one landscape poster per venue for the single-event page. Photos ≥1600 px, clips mp4 6–12 s, no audio. *(open · design review 29 Sep 2026, Asset list — TICVAI Guest Booking · DI-1080)*
- The tenant picks which logo lockup sits in the nav bar and a logo variant (Light, Dark, Duotone) whose colours drive the theme. *(agreed · design review 29 Sep 2026, CFG-4 · Brand logo + Logo palette (Light/Dark/Duotone) · DI-1068)*
- Theme settings: surface style Glass (default) or Solid cards; button style Solid (default), Outline or Pill. *(agreed · design review 29 Sep 2026, CFG-3 · Surfaces (Glass/Solid) and Buttons (Solid/Outline/Pill) · DI-1067)*
- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Guest-facing copy may say "session" (surf sessions, timed sessions) as a glossary exception, like "Booking". *(agreed · design review 29 Sep 2026, CFG-10 · 'Sessions can be added, edited or closed from Config -> Sessions' · DI-1064)*
- Optional intro video on opening the app, with a "Skip introduction" control. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1020)*
- A persistent "Buy tickets" button appears on every screen of the mobile app. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1017)*
- Mobile tabs: Home, Explore, Plan, Tickets (Yas Island / Six Flags references). *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1016)*
- The current mobile build goes straight into the booking journey and the client finds it unclear: redesign the UI. All web products and flows, including cabanas and surf, must remain available. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1015)*
- Never ask the same thing twice: table zone is picked on the table map (no zone step before it); height is asked once (height bands on the water-park day pass are the eligibility check); party/school summaries prefill headcount, child's name and age from the earlier form. *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): repeated steps removed · DI-1000)*
- Headers are reserved for standard elements only (venue image, category tabs, language bar, profile icon), applied consistently; date/availability selection belongs in the main content below the header, never in the header. Header/layout patterns must be adapted for mobile, which looks and behaves differently. *(agreed · MoM 24 Sep 2026, 4.9 Guest Web App — Specific UX Feedback (Header/Date Placement Standardization) · DI-990)*
- A language button (EN / العربية) sits in the header next to the profile icon, web and mobile. Arabic flips the whole layout right-to-left and switches interface text (navigation, buttons, booking steps, ticket names and tags, cart, seat map, checkout, account). Venue, show and dish names stay as written. *(client request · design review 23 Sep 2026, Header 2. Language icon in the header · DI-975)*
- Replace "Sign in / Create account" in the header with a single profile icon. It opens one screen with Log in and Register tabs; signed-in guests get their account menu from the same icon. *(client request · design review 23 Sep 2026, Header 1. One profile icon in the header that opens login / register · DI-974)*
- Allam's model reference: a simple card-based family-entertainment-centre site with minimal clicks, a right-side cart drawer, "help me choose", clear categories, video that autoplays when a guest taps "read more", adapting seamlessly between desktop and mobile. Allam and Qossai want this simplicity to guide the guest experience. *(client request · MoM 18 Sep 2026, 4.14 Guest Website UX Review — Upsell/Cross-Sell Placement & Reference Sites · DI-952)*
- **Open question.** Allam expects a large volume of feedback on the guest web/mobile prototype; detailed feedback goes to a separate dedicated session with Qossai and Allam. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-888)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*
- Allam: most guests book from a smartphone, so the mobile version of the booking flows is the higher priority to validate (only desktop shown). *(client request · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough · DI-684)*
- Accreditation is primarily completed in the web portal (document upload and photo checks suit a larger screen); the same submission is also available in the guest mobile app as a secondary option for individuals. *(agreed · MoM 7 Sep 2026, 4.8 Accreditation Channel Placement & API Access · DI-666)*
- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*
- Confirmed: a guest always books a product or package — never a resource (a specific room, vehicle or instructor by itself) directly — on every sales channel, including the guest/mobile app; the product's configuration determines which resources are booked behind the scenes. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-502)*
- Ticketing, F&B and retail share one cart and checkout, one unified receipt and one QR/wristband per customer — no separate receipts or wristbands per product line. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-293)*
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)*
- **Open question.** Open: publishing model — each client's own App/Play Store listing vs one universal TICVAI app where the user selects the venue; and a client module with customisation screens plus a CI/CD-linked publish action vs a canvas the client exports and publishes. Softlabs to present pros/cons. *(open · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-251)*
- Qossai: the TICVAI name must always remain visible to end users of a client-branded guest app (e.g. a "Made by TICVAI" credit) and cannot be removed by the client. *(agreed · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-250)*
- Qossai: present products with video rather than static images (as Talabat-style apps do); see benchmark app "222" for further inspiration. *(client request · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-222)*
- Qossai shared reference apps (Al Qadiya / Six Flags Saudi Arabia, and "The District" by Zomato) and cited their use of video over static images as design inspiration. *(client request · MoM 5 Aug 2026, 13. Mobile / POS App Design References · DI-146)*
- A single cart/order must take mixed purchases (e.g. family tickets plus gift vouchers) with one unified checkout and identity capture. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-141)*
- Base ticket-booking UX (web and mobile) on current market best practice rather than the demoed references as-is; Allam recommends the "Viva Ticket" website as a reference for the flow variations. *(agreed · MoM 3 Aug 2026, 10. Reference Material & Design Research · DI-125)*
- The POS/tablet application carries TICVAI's own branding and UI direction; the B2C and B2B mobile applications are white-label by design. *(agreed · MoM 31 Jul 2026, 15. Monday UI/UX Session Planning · DI-084)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Qossai: the target product is a white-label application supporting both B2C and B2B mobile use cases, built around three to four distinct flows (e.g. admission ticket flow, seat assignment flow). *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-056)*
- Selling reference layout: clean top navigation; category tabs with counts (All Events 32, Exhibitions, Guided Tours ...); sort and type chips (Price, Rating, Popular; General, Seated, Multipass, Scheduled, Rental); content cards with large image, type badge, rating, tags (LIMITED, NEW, BESTSELLER), availability ("180 available", "11 left") and "from" price; persistent cart on the right with member discount, totals and "Checkout Securely". *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, items 2-5 · DI-026)*
- Preliminary perceived-performance targets: web pages load in under about 3 seconds, mobile app loads in under about 2 seconds, ticket validation responds in under 500 milliseconds. *(agreed · MoM 28 Jul 2026, 18. Performance and Scalability · DI-015)*

**37 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addCartLine": {"method":"POST","path":"/carts/{cartId}/lines","contract":"orders","summary":"Add something","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"AddCartLineRequest","responds":"Cart"},
"bookVisitPlan": {"method":"POST","path":"/visit-plans/{planId}/booking","contract":"venue-map","summary":"Book this plan — turn it into cart lines","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"VisitPlanBooking"},
"checkoutCart": {"method":"POST","path":"/carts/{cartId}/checkout","contract":"orders","summary":"Turn the cart into an order","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"claimLocationSession": {"method":"POST","path":"/location-sessions","contract":"fnb","summary":"Tell the platform where the guest is","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"LocationSession"},
"createAiConversation": {"method":"POST","path":"/conversations","contract":"ai","summary":"Open a conversation","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiConversation"},
"createGuestFnbOrder": {"method":"POST","path":"/guest-orders","contract":"fnb","summary":"A guest orders food","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateGuestOrderRequest","responds":"GuestOrderResult"},
"generateVisitPlan": {"method":"POST","path":"/visit-plans","contract":"venue-map","summary":"Build a visit plan from the party, the dates and what they like","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisitPlanRequest","responds":"VisitPlan"},
"getCart": {"method":"GET","path":"/carts/{cartId}","contract":"orders","summary":"The cart, priced and checked, right now","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Cart"},
"getGuestMenu": {"method":"GET","path":"/outlets/{outletId}/guest-menu","contract":"fnb","summary":"The menu a guest sees","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"at","in":"query","required":null},{"name":"language","in":"query","required":null}],"requestBody":null,"responds":"GuestMenu"},
"getGuestOrderStatus": {"method":"GET","path":"/guest-orders/{orderId}","contract":"fnb","summary":"Track an order","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuestOrderStatus"},
"getTenantAppStatus": {"method":"GET","path":"/tenant-config/status","contract":"white-label","summary":"App status and recent changes","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"TenantAppStatus"},
"getVisitPlan": {"method":"GET","path":"/visit-plans/{planId}","contract":"venue-map","summary":"A visit plan, at its current version or an earlier one","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"version","in":"query","required":null}],"requestBody":null,"responds":"VisitPlan"},
"getWaitTimes": {"method":"GET","path":"/queues/wait-times","contract":"queue","summary":"Wait times across a venue","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":true},{"name":"category","in":"query","required":null}],"requestBody":null,"responds":"WaitTime"},
"handoverToAgent": {"method":"POST","path":"/conversations/{conversationId}/handover","contract":"marketing-crm","summary":"Pass an assistant conversation to a person","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Conversation"},
"listCatalogueBundles": {"method":"GET","path":"/catalogue/bundles","contract":"catalogue","summary":"List published catalogue bundles","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BundleSummary"},
"listMyCases": {"method":"GET","path":"/my/cases","contract":"marketing-crm","summary":"The cases this guest raised","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMyNotifications": {"method":"GET","path":"/me/notifications","contract":"marketing-crm","summary":"The signed-in guest's notification feed","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null},{"name":"unreadOnly","in":"query","required":null},{"name":"venueId","in":"query","required":null}],"requestBody":null,"responds":"Page"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPublishedContentPages": {"method":"GET","path":"/storefront/pages","contract":"white-label","summary":"The live content pages, readable before sign-in","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"categoryCode","in":"query","required":false},{"name":"slug","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPublishedFaqs": {"method":"GET","path":"/storefront/faqs","contract":"white-label","summary":"The published FAQs, readable before sign-in","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"PublishedFaqCategory"},
"listPublishedPolicies": {"method":"GET","path":"/storefront/policies","contract":"white-label","summary":"The tenant's current legal policies, readable before sign-in","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"kind","in":"query","required":false}],"requestBody":null,"responds":"PublishedPolicy"},
"listVisitPlanAlternatives": {"method":"GET","path":"/visit-plans/{planId}/items/{itemId}/alternatives","contract":"venue-map","summary":"What could take this item's place","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"markMyNotificationsRead": {"method":"POST","path":"/me/notifications/read","contract":"marketing-crm","summary":"Mark the signed-in guest's notifications read","permission":null,"offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"raiseMyCase": {"method":"POST","path":"/my/cases","contract":"marketing-crm","summary":"Report something — lost property, a complaint, a question","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Case"},
"recordAnswerFeedback": {"method":"POST","path":"/messages/{messageId}/feedback","contract":"ai","summary":"Say whether an answer helped","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiAnswerFeedback"},
"replyToMyCase": {"method":"POST","path":"/my/cases/{caseId}/messages","contract":"marketing-crm","summary":"Reply on a case the guest raised","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CaseDetail"},
"requestSuggestion": {"method":"POST","path":"/ai/suggestions","contract":"ai","summary":"Ask for an answer, however it is currently produced","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Suggestion"},
"sendAiMessage": {"method":"POST","path":"/conversations/{conversationId}/messages","contract":"ai","summary":"Ask","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiMessage"},
"sendConversationMessage": {"method":"POST","path":"/conversations/{conversationId}/messages","contract":"marketing-crm","summary":"Say something, as a guest or an agent","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConversationMessage"},
"submitReview": {"method":"POST","path":"/reviews","contract":"marketing-crm","summary":"Submit a review","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SubmitReviewRequest","responds":"Review"},
"updateVisitPlan": {"method":"PUT","path":"/visit-plans/{planId}","contract":"venue-map","summary":"Swap, remove, add, move or undo, as a new version","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisitPlanUpdate","responds":"VisitPlan"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AddCartLineRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["variantId","quantity"],"properties":{"variantId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Optional; sent by a page or till that shows the engine's recommendations. Not validated against the engine: an unknown id only fails to attribute.\n"},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's `deposit.variantId` and `quantity` 1. The price is the booking's `deposit.amount`. A booking that is not awaiting a deposit is refused 422 `depositNotDue`.\n"},"seatIds":{"type":"array","maxItems":50,"description":"At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). Over the limit is 422 `seatLimitExceeded`.","items":{"type":"string","format":"uuid"}},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and `quantity` is 1. The hold is the line's capacity; no inventory lease is taken."},"parentLineId":{"type":"string","format":"uuid","nullable":true,"description":"For an add-on attaching to a ticket already in the cart. **Removing the parent removes the child** — a locker with no admission is not a sale.\n"},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"}}},
"AiAnswerFeedback": {"type":"object","x-ticvai-persistence":"ai.answer_feedback","description":"**What a person thought of an answer** (AIC-062). One label per message per person; it feeds the golden sets and the knowledge-gap list, never an online update (design 3.5).","required":["messageId","rating"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"messageId":{"type":"string","format":"uuid","x-ticvai-references":"ai.message"},"conversationId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.conversation"},"rating":{"type":"string","enum":["helpful","notHelpful"]},"reason":{"type":"string","enum":["wrong","outdated","incomplete","notGrounded","unsafe","other"],"nullable":true},"comment":{"type":"string","nullable":true,"maxLength":1000},"audience":{"type":"string","enum":["staff","guest"],"readOnly":true},"principalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"subjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The guest, where the audience is `guest`."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiConversation": {"type":"object","x-ticvai-persistence":"ai.conversation","required":["id","principalId","module","startedAt"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"module":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},"locale":{"type":"string"},"messageCount":{"type":"integer"},"startedAt":{"type":"string","format":"date-time"},"lastMessageAt":{"type":"string","format":"date-time"}}},
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"AiMessage": {"type":"object","x-ticvai-persistence":"ai.message","required":["id","conversationId","role","content","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"conversationId":{"type":"string","format":"uuid"},"role":{"type":"string","enum":["user","assistant","system"]},"content":{"type":"string"},"sources":{"$ref":"#/components/schemas/AiSourceList"},"confidence":{"type":"number","nullable":true,"description":"8.1.5, 8.3.67. **Nullable on purpose** — a provider that does not report confidence must yield null rather than an invented number, and an interface showing 0.9 because the code defaulted it is worse than showing nothing.\n"},"rationale":{"type":"string","nullable":true,"description":"8.3.68, 8.3.69."},"proposedAction":{"allOf":[{"$ref":"#/components/schemas/ProposedAction"}],"nullable":true,"description":"Present where the answer suggests a change. **A draft, never applied here.**"},"traceId":{"type":"string"},"provider":{"$ref":"#/components/schemas/AiProviderKind"},"model":{"type":"string"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"latencyMs":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"}}},
"AiProviderKind": {"type":"string","enum":["openai","gemini","anthropic","azureOpenai","localLlm","openaiCompatible"],"description":"`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n"},
"AiSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**The sources an answer was grounded in, stored with the answer** (8.3.70). One `jsonb` column on the row that carries it — `ai.message.sources` and `ai.activity.sources` — because the grounding audit reads the list as it was when the answer was given, and a source is never queried on its own.\n","items":{"$ref":"#/components/schemas/AiSource"}},
"AllergenCode": {"type":"string","description":"**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n","enum":["gluten","crustaceans","eggs","fish","peanuts","soybeans","milk","nuts","celery","mustard","sesame","sulphites","lupin","molluscs"]},
"AppAvailability": {"type":"string","description":"**The sold-out or closed signal (decided 28 September, audit R073).** `open` is the normal state. `soldOut` shows WEB-029's sold-out state across the app while browsing still works; `closed` shows the closed state (a weather closure, a private event). Neither refuses a request on its own: it is what the guest is told, and a sale is still refused by availability where it applies. Set with `setMaintenanceMode`.\n","enum":["open","soldOut","closed"],"default":"open"},
"BookedWindow": {"type":"object","nullable":true,"x-ticvai-persistence":"none — embedded as window_starts_at and window_ends_at on orders.cart_line and orders.order_line","description":"**The booked time window of an hourly product, such as a meeting room** (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). The guest picks a date, a length and a start time from `resources.listProductStartTimes`; the length is the product's `length` variant (1 hour, 2 hours, half day, full day), priced per variant, so the price is the variant's. **`endsAt` minus `startsAt` must equal the chosen variant's length** (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. Required on a product with `catalogue.Product.requiresTimeWindow` true and refused on any other (`windowRequired`, `windowNotAllowed`). The room itself is not named here: the window holds capacity of the room type, and `resources.allocateResources` picks the room at checkout (26 August minute: a guest books a meeting room product, never a raw room).\n","required":["startsAt","endsAt"],"properties":{"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time","description":"After `startsAt`, on the same venue day."}}},
"BundleSummary": {"x-ticvai-persistence":"none — projection over bundle","type":"object","description":"One published catalogue bundle — the signed snapshot terminals pull (ADR-0013). Not `promotions.Bundle`, which is a sellable product made of other products.","required":["version","venueId","publishedAt","publishedBy","contentHash","staleAfter","sizeBytes"],"properties":{"version":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"publishedAt":{"type":"string","format":"date-time"},"publishedBy":{"type":"string","format":"uuid"},"contentHash":{"type":"string"},"signatureKeyId":{"type":"string","description":"Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle.\n"},"staleAfter":{"type":"string","format":"date-time"},"sizeBytes":{"type":"integer"},"note":{"type":"string"},"appliedByWorkstations":{"type":"integer"}}},
"Cart": {"type":"object","x-ticvai-persistence":"orders.cart","required":["id","venueId","channel","status","lines"],"properties":{"id":{"type":"string","format":"uuid"},"token":{"type":"string","readOnly":true,"description":"**How an anonymous guest returns to their cart**, including from a recovery email. Rotated on claim, so a link shared before signing in does not reach the account after.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null while anonymous. Set by `claimCart`."},"status":{"$ref":"#/components/schemas/CartStatus"},"lines":{"type":"array","items":{"$ref":"#/components/schemas/CartLine"}},"conflicts":{"type":"array","items":{"$ref":"#/components/schemas/CartConflict"}},"consentQuestions":{"type":"array","readOnly":true,"description":"**The consent questions this cart's products and flow ask** (decided 29 September, rev 3 REV3-26), computed on read at their current version as **the union of each line's published booking flow's `white-label.BookingFlow.settings.consentQuestionIds`** (the flow `getPublishedBookingFlow` resolves for the line's product: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig`, 29 September W12) **and every line's `catalogue.Product.consentQuestionIds`, each question once**: the flow's first, in its order, then each product's in cart-line order, a question already listed not repeated (its `lineIds` gain the line). The client asks them, in the order given, and sends the answers to `marketing.recordConsentAnswers`; `answered` then turns true. One or several, as the venue chose. `checkoutCart` refuses while a required one is unanswered.\n","items":{"allOf":[{"$ref":"../satellite/marketing-crm.yaml#/components/schemas/ConsentQuestion"},{"type":"object","properties":{"lineIds":{"type":"array","description":"The cart lines that ask it. Empty for a question the flow asks.","items":{"type":"string","format":"uuid"}},"answered":{"type":"boolean","description":"Every person (for `perPerson`) or the booking (for `perBooking`) has an answer."}}}]}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"discountTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPromotionIds":{"type":"array","description":"**Re-evaluated on every read.** A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became applicable should be.\n","items":{"type":"string","format":"uuid"}},"couponCodes":{"type":"array","readOnly":true,"description":"The promo codes the guest entered through `applyCartPromoCode` (decided 28 September, audit R073 (e)). **Sent as `couponCodes` on every promotions evaluation of this cart**, so a code is re-checked on each read like any promotion; a code that stops qualifying stays listed here and its promotion drops out of `appliedPromotionIds`.\n","items":{"type":"string","maxLength":100}},"expiresAt":{"type":"string","format":"date-time","description":"The earliest lease expiry in the cart, or the cart's own window where it holds none."},"extensionsUsed":{"type":"integer","readOnly":true},"maxExtensions":{"type":"integer","readOnly":true},"locale":{"type":"string"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time"}}},
"CartConflict": {"type":"object","x-ticvai-persistence":"none — computed on read","description":"2.9.5. Golf at 13:00 and karting at 13:00 for the same guest. **A prompt, not a refusal** — a party of four may legitimately split, and refusing would be wrong more often than right.\n","properties":{"kind":{"type":"string","enum":["overlappingTime","sameSessionDifferentVenue","exceedsPartySize","requiresPrerequisite","consentBlocksBooking"]},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"message":{"type":"string"},"isBlocking":{"type":"boolean","description":"Most are not. `requiresPrerequisite` is — an add-on with no ticket to attach to cannot be sold. So is `consentBlocksBooking`: a consent question answered with the answer the venue set to block the booking (decided 29 September, rev 3 REV3-26).\n"}}},
"CartLine": {"type":"object","x-ticvai-persistence":"orders.cart_line","required":["id","variantId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"productName":{"type":"string","readOnly":true},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid","nullable":true},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Set from `addCartLine`; checkout copies it to the order line.\n"},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"Set on a table deposit line only (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` this line secures. Priced from the deposit the booking snapshotted, not from the variant. Becomes an `orders.deposit` row at checkout, not revenue. A table booking with no deposit never has a line (rev 3 REV3-8).\n"},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"}},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"The `resources.ResourceHold` this line buys (decided 29 September, rev 3 REV3-15). While set, `leaseExpiresAt` is the hold's `expiresAt` and `inventoryHoldId` is null."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"parentLineId":{"type":"string","format":"uuid","nullable":true,"description":"The line this add-on is attached to, from `AddCartLineRequest.parentLineId`. Kept on the line because **removing the parent removes the child**, and `removeCartLine` has to be able to find the children.\n"},"overridePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"overrideReason":{"type":"string","nullable":true,"enum":["priceMatch","serviceRecovery","negotiated","damagedGoods","staffSale","error"],"description":"BL-085. **An operator could apply an approved discount and not enter a price.** A price match against a competitor and a service-recovery gesture are not discounts off a list — they are a number somebody decided.\n**Escalated above a configured threshold, and the reason is a closed set**: a free-text override reason is an override nobody can report on, and this is the field an auditor reads first.\n"},"feeKind":{"type":"string","nullable":true,"enum":["booking","transaction","service","delivery","convenience","cancellation"],"description":"**A fee is a line, not an adjustment.** `orders` already separates a service charge from a tip for the reason that applies here: **a guest is entitled to see what they are being charged for**, and a fee folded into the ticket price is a fee nobody can question.\nItemised at checkout, taxed on its own code, and refundable separately — **a cancellation fee is usually the one thing not refunded**, which only works if it is its own line.\n"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"inventoryHoldId":{"type":"string","nullable":true,"description":"The capacity held for this line — a `catalogue.InventoryHold.id`, typed as that id is. **Null for a product with no capacity** — a t-shirt needs stock, not a lease.\n"},"leaseExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"Shown to the guest. *\"Your seats are held for 6 minutes\"* is better than discovering it at checkout.\n"},"isAvailable":{"type":"boolean","readOnly":true,"description":"Re-checked on every read. **A line can become unavailable while the cart sits** — a lease expiring is not the same as the product selling out, and both land here.\n"}}},
"CartStatus": {"type":"string","enum":["active","expiring","expired","abandoned","checkedOut"]},
"Case": {"x-ticvai-persistence":"marketing.case","x-ticvai-retired-columns":["guest_name","subject","is_sla_breached"],"type":"object","required":["id","caseNumber","subject","status","priority","createdAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7."},"caseNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity. Assigned when the case reaches the server, so a retry with the same `id` keeps its number.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true},"guestName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"**Resolved from `pii.subject` when the case is read, never stored on the case.** A name copied onto a case row is personal data outside the erasable store (ADR-0023), and it had no source anyway — no request carries it. Returned only to callers holding `GUEST_VIEW_PII`, as `searchGuests` does.\n"},"subject":{"type":"string","x-ticvai-column":"title","description":"**The case's one-line title**, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps `subject` because screens bind it.\n"},"kind":{"allOf":[{"$ref":"#/components/schemas/CaseKind"}],"nullable":true,"description":"What the guest said it was about, where the guest raised it."},"channel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"description":"How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`."},"recordedAt":{"type":"string","format":"date-time","description":"Device time the case was raised — the start of the SLA clock."},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the case arrived. Equal to `recordedAt` for a case raised online."},"categoryId":{"type":"string","format":"uuid","nullable":true},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The `ServiceQueue` the case waits in, set by routing (`CaseRoutingRule.queueId`). Null once routed straight to an agent. (decided 29 September, data model for the agreed operations)"},"membershipId":{"type":"string","format":"uuid","nullable":true,"description":"The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. (decided 29 September, coordinator decision DM4, writers pass)"},"status":{"$ref":"#/components/schemas/CaseStatus"},"priority":{"$ref":"#/components/schemas/CasePriority"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"relatedOrderId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"isSlaBreached":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"**Computed when read, never stored.** True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` (or to now, while unresolved), less `slaPausedSeconds`, is past the target that set `slaDueAt`. A stored flag would need a job to flip it at the moment of breach, and no such job is designed; `listCases?breachedSla` filters on the same computation.\n"},"slaPausedSeconds":{"type":"integer","description":"Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock.\n"},"escalationCount":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"CaseDetail": {"x-ticvai-persistence":"marketing.case","allOf":[{"$ref":"#/components/schemas/Case"},{"type":"object","properties":{"description":{"type":"string"},"resolutionNote":{"type":"string","nullable":true},"messages":{"type":"array","items":{"$ref":"#/components/schemas/CaseMessage"}}}}]},
"CaseKind": {"type":"string","description":"**What the guest says the case is about**, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.\n**`other` only with a note (decided 28 September, audit R222).** A case raised as `other` must carry a non-empty `detail` (`raiseMyCase`), or it is refused with 400; the notes are reviewed quarterly to add the real kinds they reveal.\n","enum":["lostProperty","complaint","question","accessibility","refundRequest","other"]},
"CaseMessage": {"x-ticvai-persistence":"marketing.case_message","type":"object","required":["id","body","isInternal","authorKind","recordedAt"],"properties":{"resolution":{"type":"string","description":"**What was actually done about it.** Indexed for retrieval: an agent facing a complaint benefits more from how the last one was resolved than from a policy. Without this column `marketing.case` can only embed its subject line.\n"},"id":{"type":"string"},"body":{"type":"string"},"isInternal":{"type":"boolean"},"authorKind":{"type":"string","enum":["agent","guest","system","ai"]},"authorPrincipalId":{"type":"string","format":"uuid","nullable":true},"channel":{"$ref":"#/components/schemas/MessageChannel"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time","description":"Device time — `addCaseMessage` is offline-capable."},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the message arrived."}}},
"CasePriority": {"type":"string","enum":["low","normal","high","urgent"]},
"CaseStatus": {"type":"string","enum":["open","inProgress","awaitingGuest","escalated","resolved","closed"]},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"Conversation": {"type":"object","x-ticvai-persistence":"marketing.conversation","description":"22.8. **A conversation is not a case.** A case is a ticket measured in hours; a conversation is a live session measured in seconds, with somebody waiting. A conversation may create a case; it is not one.\n","required":["id","channel","state"],"properties":{"id":{"type":"string","format":"uuid"},"telephony":{"type":"object","nullable":true,"description":"BL-083. **`ConversationChannel` included `voice` with nothing behind it** — the model anticipated telephony and stopped at the enum.\n**Not an integration, a binding.** Genesys, Avaya, Amazon Connect, Teams and 3CX all do call control themselves; what the platform needs is the call bound to the guest and the case, so **an agent who answers already knows who is calling and what about.**\n","properties":{"providerCallId":{"type":"string"},"direction":{"type":"string","enum":["inbound","outbound","transferred"]},"fromNumberMasked":{"type":"string","nullable":true,"description":"**Masked, and it is still personal data.** A phone number identifies a person more reliably than a name does.\n"},"recordingRef":{"type":"string","nullable":true,"description":"Held by the provider, referenced here. **Recording consent is jurisdictional and the platform does not assume it** — a reference with no consent record is a recording nobody may play.\n"},"agentState":{"type":"string","enum":["available","onCall","wrapUp","away","offline"],"nullable":true}}},"assistSessionId":{"type":"string","format":"uuid","nullable":true,"description":"BL-094. **`startKioskAssist` recorded a staff member helping a guest and `createCase` recorded a service interaction, and neither referenced the other** — so the traceability 2.13.20 asks for had no link to follow.\n**The link is here rather than on the assist session**, because a case may span several assists and an assist belongs to at most one case.\n"},"channel":{"$ref":"#/components/schemas/ConversationChannel"},"state":{"$ref":"#/components/schemas/ConversationState"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"22.8.3. Resolved from phone, email, membership number or a signed-in session. **A conversation with none of those stays anonymous rather than being guessed at.**\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"assignedPrincipalId":{"type":"string","format":"uuid","nullable":true},"queueId":{"type":"string","format":"uuid","nullable":true},"queuePosition":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onRead","description":"Place among the unclaimed conversations in `queueId`, from the live agent queue (audit R149). Null once claimed."},"estimatedWaitSeconds":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onRead","description":"From the live agent queue — the conversations ahead divided across that queue's agents online now (audit R149). Null once claimed."},"handoverReason":{"type":"string","nullable":true,"enum":["guestRequested","assistantRefused","assistantFailed","outOfScope","negativeSentiment","complexIntent","paymentIssue"]},"handoverSummary":{"type":"string","nullable":true,"description":"**The assistant's own account of what the guest wants**, so an agent opens with context rather than reading a transcript while somebody waits.\n"},"sentiment":{"type":"string","nullable":true,"enum":["positive","neutral","negative","escalating"],"description":"22.8.16. **`escalating` is a routing signal**, not a report line."},"intent":{"type":"string","nullable":true,"description":"22.8.13. What the guest appears to want, used for routing."},"locale":{"type":"string"},"caseId":{"type":"string","format":"uuid","nullable":true,"description":"22.8.12. Where the conversation raised one."},"messages":{"type":"array","items":{"$ref":"#/components/schemas/ConversationMessage"}},"firstResponseSeconds":{"type":"integer","nullable":true,"readOnly":true},"startedAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true},"outcome":{"type":"string","nullable":true,"enum":["resolved","caseRaised","abandonedByGuest","timedOut","spam"]}}},
"ConversationChannel": {"type":"string","enum":["webChat","inAppChat","whatsapp","sms","email","kiosk","voice"]},
"ConversationMessage": {"type":"object","x-ticvai-persistence":"marketing.conversation_message + marketing.conversation_message_attachment","required":["id","sender","body","sentAt"],"properties":{"id":{"type":"string","format":"uuid"},"sender":{"type":"string","enum":["guest","agent","assistant","system"],"description":"**Resolved, never declared.** The assistant is labelled as one — a guest talking to a bot that presents as a person is a complaint waiting for the moment they find out.\n"},"senderPrincipalId":{"type":"string","format":"uuid","nullable":true},"body":{"type":"string"},"attachments":{"type":"array","items":{"type":"object","properties":{"assetId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["image","video","document","ticket","qr","paymentLink"]}}}},"aiInteractionId":{"type":"string","format":"uuid","nullable":true,"description":"Where the assistant sent it. **Links the message to its tokens and cost**, so a conversation's spend is attributable (CF-14).\n"},"sentAt":{"type":"string","format":"date-time"},"readAt":{"type":"string","format":"date-time","nullable":true}}},
"ConversationState": {"type":"string","description":"**`withAssistant` and `queued` are different, and the second has a person waiting.** Merging them makes the service level unmeasurable, because time with a bot is not time in a queue.\n","enum":["withAssistant","queued","withAgent","waitingOnGuest","resolved","abandoned","timedOut"]},
"CreateGuestOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","menuItemId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"menuItemId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1,"maximum":20},"modifierOptionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"note":{"type":"string","maxLength":200,"description":"Free text to the kitchen. Allergy notes belong here and are surfaced prominently on the ticket.\n"}}},
"CreateGuestOrderRequest": {"type":"object","required":["id","lines","quotedTotal","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"locationSessionId":{"type":"string","format":"uuid","nullable":true,"description":"From `claimLocationSession`. Where the order is going. Required for delivery to a table, seat, cabana or named location. Absent for collection, where the outlet is named instead.\n"},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"Required for collection. Ignored where a location session is supplied — the session names its outlet."},"fulfilment":{"allOf":[{"$ref":"#/components/schemas/GuestOrderFulfilment"}],"nullable":true,"description":"Required for takeaway and address delivery; refused with 422 when it breaks the outlet's `FnbDeliveryPolicy`."},"lines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateGuestOrderLine"}},"quotedTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the guest was shown. Checked against the server's recomputation — a guest is never trusted with a price, and a mismatch is refused rather than silently corrected in either direction.\n"},"paymentMethod":{"type":"string","enum":["card","wallet","roomCharge","addToTab"]},"recordedAt":{"type":"string","format":"date-time"}}},
"DeliveryLocationKind": {"type":"string","description":"4.6.26. One concept, because a runner needs one instruction.","enum":["table","seat","cabana","sunbed","poolside","box","suite","lawn","collectionPoint","namedLocation"]},
"FnbOrderStatus": {"type":"string","description":"The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or `delivered` at all, which made collection and delivery indistinguishable from a server putting a plate down.\n`accepted` matters because an outlet may refuse: past last orders, out of a key ingredient, or simply too far behind. A guest whose order sat in `placed` for ten minutes and was then rejected has a worse experience than one refused immediately.\n","enum":["ordered","accepted","inPreparation","ready","served","collected","delivered","cancelled","refunded"]},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"GuestMenu": {"type":"object","x-ticvai-persistence":"none — projection over menu, item and availability","required":["outletId","menuId","name","inForceUntil","sections"],"properties":{"outletId":{"type":"string","format":"uuid"},"menuId":{"type":"string","format":"uuid"},"name":{"type":"string"},"inForceUntil":{"type":"string","format":"date-time","nullable":true,"description":"When this menu stops applying. The client shows it, because a guest browsing breakfast at 10:55 should know.\n"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer"},"sections":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"sortOrder":{"type":"integer"},"items":{"type":"array","items":{"type":"object","required":["menuItemId","name","price","isAvailable","allergens"],"properties":{"menuItemId":{"type":"string","format":"uuid"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"imageAssetRef":{"type":"string","nullable":true},"isAvailable":{"type":"boolean","description":"Marked, not removed. A guest who saw a dish yesterday and cannot find it today assumes the app is broken; \"sold out\" is an answer.\n"},"unavailableReason":{"type":"string","nullable":true},"allergens":{"type":"array","description":"Always present. Not a field a tenant may choose to omit.","items":{"$ref":"#/components/schemas/AllergenCode"}},"preparationMinutes":{"type":"integer","nullable":true},"modifierGroups":{"type":"array","items":{"$ref":"#/components/schemas/ModifierGroup"}}}}}}}}}},
"GuestNotification": {"type":"object","description":"One in-app message as the guest sees it. A view of `marketing.message_dispatch`, channel `inApp`.","required":["id","title","queuedAt","read"],"properties":{"id":{"type":"string"},"kind":{"type":"string","enum":["queueCall","orderReady","bookingChange","venueAlert","offer","other"]},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedText"},"venueId":{"type":"string","format":"uuid","nullable":true},"deepLink":{"type":"string","nullable":true,"description":"Where tapping the notification leads in the app (an order, a queue ticket, a booking)."},"queuedAt":{"type":"string","format":"date-time"},"read":{"type":"boolean"}}},
"GuestOrderFulfilment": {"type":"object","x-ticvai-persistence":"fnb.order_fulfilment","description":"How a guest's order leaves the kitchen: collected, delivered to an address, or taken to a place in the venue.","required":["mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"orderId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-column":"service_order_id","description":"The guest order this fulfils (`FnbOrder.id`). Set by the server from the order it arrives with."},"mode":{"type":"string","enum":["collection","delivery","inVenue"],"description":"`collection` from a counter, `delivery` to an address outside the venue, `inVenue` to a table, seat, cabana or named location (the location session). `GuestOrderResult.fulfilment` reports the same choice."},"collectionAt":{"type":"string","format":"date-time","nullable":true},"windowStart":{"type":"string","format":"date-time","nullable":true},"windowEnd":{"type":"string","format":"date-time","nullable":true},"deliveryAddress":{"type":"object","nullable":true,"properties":{"building":{"type":"string","maxLength":200},"unit":{"type":"string","maxLength":60,"nullable":true},"emirate":{"type":"string","maxLength":60},"directions":{"type":"string","maxLength":500,"nullable":true}}},"deliveryFee":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true},"cutlery":{"type":"boolean","default":false},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"GuestOrderResult": {"type":"object","x-ticvai-persistence":"none — projection over fnb_order","required":["orderId","orderNumber","status","total"],"properties":{"orderId":{"type":"string"},"orderNumber":{"type":"string","description":"Short and readable. It gets called out across a counter."},"fulfilment":{"type":"string","enum":["collect","deliverToLocation","tableService","deliverToAddress"],"description":"How the order reaches the guest, in the request's terms: `collect` is `GuestOrderFulfilment.mode` `collection`; `deliverToAddress` is `delivery`; `inVenue` is `tableService` where the location session is a table and `deliverToLocation` for a seat, cabana or named location. `KitchenTicket.serviceMode` is the kitchen's view and uses `ServiceMode`."},"deliveryLabel":{"type":"string","nullable":true,"description":"Where it is going, as a runner would read it."},"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"estimatedReadyAt":{"type":"string","format":"date-time","nullable":true},"collectionPoint":{"type":"string","nullable":true},"tableLabel":{"type":"string","nullable":true}}},
"GuestOrderStatus": {"type":"object","x-ticvai-persistence":"none — projection over kitchen_ticket","required":["orderId","status","lines"],"properties":{"orderId":{"type":"string"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"estimatedReadyAt":{"type":"string","format":"date-time","nullable":true},"isReadyForCollection":{"type":"boolean"},"lines":{"type":"array","description":"Per-line status. A guest waiting on one dish should see which.","items":{"type":"object","properties":{"name":{"type":"string"},"quantity":{"type":"integer"},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"}}}}}},
"KitchenTicketStatus": {"type":"string","enum":["received","preparing","ready","served","recalled","cancelled"]},
"LocalisedRichText": {"x-ticvai-persistence":"none — jsonb column","type":"object","description":"Keyed by language code. Values are sanitised HTML.","additionalProperties":{"type":"string"}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"LocationSession": {"type":"object","x-ticvai-persistence":"fnb.location_session","required":["id","locationId","kind","label","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/DeliveryLocationKind"},"label":{"type":"string"},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"The outlet serving this location. Where several serve it, the guest chooses and this is set on the first order.\n"},"visitId":{"type":"string","format":"uuid","nullable":true,"description":"The table visit this session orders onto, where the location is a table. Absent for a cabana or a seat, which have no visit concept — the order stands alone.\n"},"joinedExistingVisit":{"type":"boolean"},"subjectId":{"type":"string","format":"uuid"},"expiresAt":{"type":"string","format":"date-time","description":"Sessions expire so a guest who leaves cannot order to a lounger now occupied by someone else.\n"}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MinimumAppVersion": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n","properties":{"ios":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"},"android":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"}}},
"ModifierGroup": {"x-ticvai-persistence":"fnb.modifier_group + fnb.modifier_option","type":"object","description":"**An F&B modifier is a choice added to a dish at the moment of ordering** — *no onions*, *extra cheese*, *cooked medium*. **It is not an Attribute**, the axis that generates catalogue variants (naming-and-style §3 lists *Modifier* as a banned synonym for that), and the two must not be merged: a variant is a different product with its own stock, a modifier is an instruction on a line with at most a price delta.\n","required":["id","code","name","minSelections","maxSelections","options"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"minSelections":{"type":"integer","minimum":0,"description":"Greater than zero makes the group required."},"maxSelections":{"type":"integer","minimum":1},"options":{"type":"array","minItems":1,"items":{"type":"object","required":["id","name","priceDelta"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"priceDelta":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isDefault":{"type":"boolean"},"isAvailable":{"type":"boolean"},"allergens":{"type":"array","description":"What choosing this option adds to the dish. `attachModifierGroup` refuses a group that adds one the item does not declare, and `verifyAllergens` reports it as `via` `modifier`.","items":{"$ref":"#/components/schemas/AllergenCode"}}}}},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"ModuleKey": {"type":"string","enum":["ticketsAndBooking","membership","events","attractions","virtualQueue","diningAndFnb","shop","parking","gamification","photoGallery","wallet","loyalty","lostAndFound","map","visitPlanner"],"description":"`visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown."},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderLineAttributes": {"type":"object","nullable":true,"additionalProperties":true,"x-ticvai-persistence":"none — embedded as attributes (jsonb) on orders.cart_line and orders.order_line","description":"Open attributes of a line, kept from the cart to the order line. **`transport` is the one with a defined shape** (decided 29 September, rev 3 REV3-21); other keys are free.\n","properties":{"transport":{"$ref":"#/components/schemas/TransportLineAttributes"}}},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"PolicyKind": {"type":"string","enum":["privacy","termsAndConditions","refund","cookie","accessibility"]},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true}}},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"PublishedContentPage": {"x-ticvai-persistence":"none — a public projection of whitelabel.content_page","type":"object","x-ticvai-agreed":"2 October: decided by Chinmay, fix before Block A starts (GFIX-2)","description":"A live content page as a guest reads it (`listPublishedContentPages`). Only published and enabled pages exist in this view, so it carries no status.","required":["id","slug","title","body"],"properties":{"id":{"type":"string","format":"uuid"},"slug":{"type":"string","pattern":"^[a-z0-9-]+$"},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedRichText"},"iconAssetRef":{"type":"string","format":"uuid","nullable":true},"categoryCode":{"type":"string","nullable":true},"sortOrder":{"type":"integer"}}},
"PublishedFaqCategory": {"x-ticvai-persistence":"none — a public projection of whitelabel.faq_category + whitelabel.faq_entry","type":"object","x-ticvai-agreed":"2 October: decided by Chinmay, fix before Block A starts (GFIX-2)","description":"One FAQ category with its published entries only (`listPublishedFaqs`).","required":["code","name","entries"],"properties":{"code":{"type":"string"},"name":{"$ref":"#/components/schemas/LocalisedText"},"sortOrder":{"type":"integer"},"entries":{"type":"array","items":{"type":"object","required":["id","question","answer"],"properties":{"id":{"type":"string","format":"uuid"},"question":{"$ref":"#/components/schemas/LocalisedText"},"answer":{"$ref":"#/components/schemas/LocalisedRichText"},"sortOrder":{"type":"integer"}}}}}},
"PublishedPolicy": {"x-ticvai-persistence":"none — a public projection of whitelabel.policy","type":"object","x-ticvai-agreed":"2 October: decided by Chinmay, fix before Block A starts (GFIX-2)","description":"The current version of one policy as a guest reads it (`listPublishedPolicies`). Who published it and the partition key stay on `Policy`.","required":["kind","version","body","effectiveFrom"],"properties":{"kind":{"$ref":"#/components/schemas/PolicyKind"},"title":{"type":"string"},"version":{"type":"string","description":"The version a consent records (a guest who consented to version 3 consented to version 3)."},"body":{"$ref":"#/components/schemas/LocalisedRichText"},"effectiveFrom":{"type":"string","format":"date"},"requiresReconsent":{"type":"boolean","description":"True when guests who consented to an earlier version are asked again on next launch."}}},
"QueueStatus": {"type":"string","enum":["open","paused","closed","atCapacity"]},
"Review": {"x-ticvai-persistence":"marketing.review","allOf":[{"$ref":"#/components/schemas/SubmitReviewRequest"},{"type":"object","required":["status"],"properties":{"status":{"type":"string","enum":["pendingModeration","published","hidden","rejected"]},"response":{"type":"string","nullable":true},"responseIsPublic":{"type":"boolean"},"respondedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"openedCaseId":{"type":"string","nullable":true,"description":"Case raised automatically where the rating fell below the venue's threshold. Feedback that goes nowhere is worse than no feedback mechanism.\n"}}}]},
"SubmitReviewRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","rating","venueId","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"relatedOrderId":{"type":"string"},"rating":{"type":"integer","minimum":1,"maximum":5},"body":{"type":"string","maxLength":5000},"aspects":{"type":"array","description":"Aspect chips — the closed set the description always named.","uniqueItems":true,"items":{"type":"string","enum":["exhibitions","staff","cleanliness","food","value"]}},"recordedAt":{"type":"string","format":"date-time"}}},
"Suggestion": {"type":"object","x-ticvai-persistence":"ai.suggestion","description":"One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n","required":["id","kind","basis","maturity","producedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SuggestionKind"},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"scopePath":{"type":"string"},"subjectRef":{"type":"string","nullable":true,"description":"What it is about — a product, an outlet, an item, a party."},"value":{"type":"object","additionalProperties":true,"description":"The suggestion itself. Shape depends on `kind`."},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1,"description":"**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"},"explanation":{"type":"string","description":"**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"},"inputs":{"type":"object","additionalProperties":true,"description":"What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"},"producerRef":{"type":"string","description":"The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"SuggestionKind": {"type":"string","description":"What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n","enum":["price","replenishment","requisition","demandForecast","prepPlan","menuEngineering","staffing","slaTarget","waitTime","upsell","segmentation","anomaly","scenario","sendTime","wasteRisk","queueBalancing","itinerary"]},
"TenantAppStatus": {"x-ticvai-persistence":"none — computed","type":"object","description":"Computed on read. The published fields come from the current `ConfigVersion`, the maintenance fields from the tenant's `tenant_config` row (`setMaintenanceMode`), and the draft fields from the working draft. **Fields marked staff only are left out of a response to a caller without a staff session** (`getTenantAppStatus`).\n","required":["tenantId","isPublished","isInMaintenance"],"properties":{"tenantId":{"type":"string","format":"uuid"},"isPublished":{"type":"boolean","x-ticvai-derived":"onRead","description":"True once any version has been published."},"publishedVersion":{"type":"string","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"draftVersion":{"type":"string","description":"Staff only."},"hasUnpublishedChanges":{"type":"boolean","x-ticvai-derived":"onRead","description":"Staff only. The working draft differs from the current version's `snapshot`."},"activeModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isEnabled` true."},"licensedModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isLicensed` true."},"activePageCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. Content pages that are `published` and enabled."},"isInMaintenance":{"type":"boolean"},"maintenanceMessage":{"$ref":"#/components/schemas/LocalisedText"},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"$ref":"#/components/schemas/MinimumAppVersion"},"contact":{"$ref":"#/components/schemas/VenueContact"},"availability":{"$ref":"#/components/schemas/AppAvailability"},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"What the sold-out or closed screen says (WEB-029). Null shows the default wording."},"venues":{"type":"array","maxItems":200,"x-ticvai-derived":"onRead","description":"**Public: the venues a guest can pick** (decided 28 September, audit R267; schema named 29 September, readiness close-out, our build plan). The source of the venue picker on WEB-001 and GST-001, returned with or without a session. **Published only**: a venue is listed when its scope node is active (`tenancy.OrgUnit.isActive`) and it is in the tenant's current published `ConfigVersion`; a venue added or reactivated since the last publish appears after the next publish, and a draft never reaches a guest. Ordered by `name`. Empty when nothing is published.\n","items":{"type":"object","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid","description":"**The venue's scope node** (`tenancy.OrgUnit.id`, level venue): what every guest screen that declares `venueId` `from: session` reads once the guest picks it."},"name":{"type":"string","maxLength":200,"description":"The venue's name (`tenancy.OrgUnit.name`)."},"city":{"type":"string","maxLength":120,"nullable":true,"description":"Shown under the name so two venues with similar names can be told apart."},"openingHoursToday":{"type":"object","nullable":true,"description":"Today's opening hours in the venue's time zone, from `tenancy.VenueSettings` opening hours. Null when the venue is closed today or has none set.","properties":{"opens":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"},"closes":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"}}}}}},"whatsNew":{"type":"array","maxItems":10,"x-ticvai-derived":"onRead","description":"**Public: the guest \"what's new\"** (decided 29 September, rev 3 GAP-B2). Newest first, at most 10, from `platform-ops.Release.guestReleaseNotes` of the releases the tenant's cell has received; a release with no guest notes is skipped. Returned with or without a staff session.\n","items":{"type":"object","required":["version","publishedAt","notes"],"properties":{"version":{"type":"string","description":"The release version."},"publishedAt":{"type":"string","format":"date-time","description":"When the release reached the tenant's cell."},"notes":{"$ref":"#/components/schemas/LocalisedText"}}}},"recentChanges":{"type":"array","description":"Staff only. Names the principal behind each change, so it never reaches a public response.","items":{"type":"object","properties":{"area":{"type":"string"},"description":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"}}}}}},
"VenueContact": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n","properties":{"phone":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true},"whatsapp":{"type":"string","nullable":true},"address":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Prose, as the guest reads it. The bookable hours are the catalogue's."}}},
"VisitPlan": {"type":"object","x-ticvai-persistence":"venuemap.visit_plan","description":"**A guest's visit plan** (29 September, MOB-6): the Plan tab. One row per plan; its items are `venuemap.visit_plan_item` rows carrying the version they belong to, so every earlier version stays readable and undo is a new version equal to an old one. **Owned by the guest session**, like a cart: `subjectId` when signed in, `sessionRef` for an anonymous device session, claimed on sign-in.\n","required":["id","venueId","status","version","days"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","readOnly":true,"description":"Derived from `venueId`."},"subjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"marketing.guest_profile","description":"The signed-in guest. From the session, never from the body."},"sessionRef":{"type":"string","nullable":true,"readOnly":true,"description":"The anonymous device session that owns the plan until sign-in."},"status":{"type":"string","enum":["draft","booked","archived"],"readOnly":true,"description":"`booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date."},"version":{"type":"integer","minimum":1,"readOnly":true,"description":"The current version. Every `updateVisitPlan` adds one."},"source":{"type":"string","enum":["rules","preset","aiAgent"],"readOnly":true,"description":"What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. **The guest sees which**, as every AI answer says what it is based on.\n"},"inputs":{"$ref":"#/components/schemas/VisitPlanRequest"},"mapVersion":{"type":"integer","readOnly":true,"description":"The published map version the plan was laid out on."},"cartId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"orders.cart","description":"The cart `bookVisitPlan` filled."},"excluded":{"type":"array","readOnly":true,"description":"**What was left out and why**, e.g. a coaster excluded because one of the party is under its 120 cm minimum. Shown on GST-053, so the planner never looks as if it forgot.\n","items":{"type":"object","properties":{"pointId":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","enum":["heightRule","ageRule","closedOnDate","notInInterests","noTime","notAtVenue"],"description":"`notAtVenue` (30 September, MoM 4.7): a must-include point that is at none of the plan's venues, so no day could hold it.\n"}}}},"unmatchedPreferences":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"**A preference a day's venue cannot meet is said, never faked** (30 September client meeting, MoM 4.7, Allam's requirement). One entry per day and preference that no point of that day's venue matches: a cuisine (`cuisineTags`), a shop (`retailTags`) or an interest (`interestTags`). `availableAtVenueIds` names the tenant's other active venues whose published map does match, so GST-053 and WEB-050 can say *Indian food is at the other park (day 2)* instead of quietly placing a restaurant the party cannot reach. Empty when every preference is met on every day. Worked out on read for the version read (a swap can meet or lose a preference), never stored.\n","items":{"type":"object","required":["date","venueId","preference","tag"],"properties":{"date":{"type":"string","format":"date"},"venueId":{"type":"string","format":"uuid","description":"The day's venue, which has no match."},"preference":{"type":"string","enum":["cuisine","retail","interest"]},"tag":{"type":"string","maxLength":30},"availableAtVenueIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Other active venues of the tenant where the tag is matched. Empty when none is."}}}},"days":{"type":"array","readOnly":true,"description":"One per date, in order. The items of the version read.","items":{"type":"object","required":["date","venueId","items"],"properties":{"date":{"type":"string","format":"date"},"venueId":{"type":"string","format":"uuid","description":"**The venue this day is planned at** (30 September, MoM 4.7): `VisitPlanRequest.dayVenues` for the date, else `venueId`. Every item of the day is at this venue.\n"},"opensAt":{"type":"string","nullable":true},"closesAt":{"type":"string","nullable":true},"items":{"type":"array","items":{"$ref":"#/components/schemas/VisitPlanItem"}}}}},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"VisitPlanAlternative": {"type":"object","x-ticvai-persistence":"none — computed on read","description":"One candidate for a swap (29 September, MOB-6).","required":["kind","venueId","startsAt","reason"],"properties":{"kind":{"type":"string","enum":["attraction","show","meal","shop","rest"]},"venueId":{"type":"string","format":"uuid","description":"The item's day venue; an alternative is never from another venue (30 September, MoM 4.7)."},"pointId":{"type":"string","format":"uuid","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"name":{"type":"string"},"startsAt":{"type":"string","format":"date-time"},"durationMinutes":{"type":"integer"},"walkMinutes":{"type":"integer","nullable":true},"expectedWaitMinutes":{"type":"integer","nullable":true},"matchedInterests":{"type":"array","items":{"type":"string"}},"reason":{"type":"string","description":"Why it is offered, in words the sheet shows, e.g. *Same thrill level, 4 minutes closer*."}}},
"VisitPlanBooking": {"type":"object","x-ticvai-persistence":"none — computed; the lines are orders.cart_line rows","description":"What `bookVisitPlan` returns (29 September, MOB-6): the cart handoff.","required":["planId","cartId","added","notAdded"],"properties":{"planId":{"type":"string","format":"uuid"},"cartId":{"type":"string","format":"uuid"},"added":{"type":"array","items":{"type":"object","properties":{"itemId":{"type":"string","format":"uuid"},"cartLineId":{"type":"string","format":"uuid"},"leaseExpiresAt":{"type":"string","format":"date-time","nullable":true}}}},"notAdded":{"type":"array","description":"Items that could not be added, with the `addCartLine` refusal each met.","items":{"type":"object","properties":{"itemId":{"type":"string","format":"uuid"},"reason":{"type":"string","description":"The orders `CartProblem` code, e.g. `soldOutForSession`, `productInfoOnly`, `seatLimitExceeded`."}}}},"freeItems":{"type":"integer","description":"Stops that need nothing bought."}}},
"VisitPlanItem": {"type":"object","x-ticvai-persistence":"venuemap.visit_plan_item","description":"**One timed stop on a plan day** (29 September, MOB-6). Rows are kept per `planVersion`: a change writes the day's items again under the new version, and an older version's rows are never updated.\n","required":["id","planId","planVersion","date","sequence","kind","startsAt","endsAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"planId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"venuemap.visit_plan"},"planVersion":{"type":"integer","minimum":1,"readOnly":true},"date":{"type":"string","format":"date"},"sequence":{"type":"integer","minimum":1},"kind":{"type":"string","enum":["attraction","show","meal","shop","rest","travel"],"description":"`meal` is a stop at a dining point (restaurant, cafe or food kiosk); `shop` is a retail stop at a shop or a retail kiosk (30 September client meeting, MoM 4.7: retail is placed from the day venue's own points, as dining is).\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"**The venue of this stop** (30 September client meeting, MoM 4.7): always the day's venue, and the venue whose map `pointId` is on. Carried on the item so the screens, `bookVisitPlan` and the AI planner agent read it rather than infer it. **Worked out on read, not stored**: from the plan's `inputs` (`dayVenues` for the item's date, else `venueId`). A stored `venue_id` would move the item rows from the plan's own row-level policy to a venue policy and hide a second park's items from the guest who owns the plan.\n"},"pointId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"venuemap.point"},"productId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"catalogue.product","description":"What is bought for this stop, where it is bought. Null for a free stop."},"bundleId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"promotions.bundle","description":"A meal combo or package, from the point's `featuredOffer`."},"performanceId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"catalogue.performance"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"walkMinutesBefore":{"type":"integer","minimum":0,"nullable":true},"expectedWaitMinutes":{"type":"integer","minimum":0,"nullable":true,"description":"The typical wait at that hour when the plan was laid out; GST-059 replaces it with the live one."},"addOnSuggestion":{"type":"object","nullable":true,"description":"A suggested add-on for this stop, e.g. Fast Track where the wait is long. Never added by itself.","properties":{"productId":{"type":"string","format":"uuid"},"reason":{"type":"string"}}},"addOnAccepted":{"type":"boolean","default":false},"pinned":{"type":"boolean","default":false,"description":"The guest fixed this stop; a re-lay moves other stops around it."},"note":{"type":"string","nullable":true,"maxLength":200}}},
"VisitPlanRequest": {"type":"object","x-ticvai-persistence":"none — request only; kept as `inputs` on venuemap.visit_plan","description":"What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050.\n","required":["venueId","dates","party"],"properties":{"venueId":{"type":"string","format":"uuid","description":"The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. Every date is planned at this venue unless `dayVenues` puts it somewhere else.\n"},"dayVenues":{"type":"array","maxItems":7,"description":"**Which venue on which date, in a multi-venue tenant** (30 September client meeting, MoM 4.7, Allam's requirement). One entry per date that is not at `venueId`; each date of `dates` at most once. Each venue must be an active venue of the caller's tenant (the options `getTenantAppStatus.venues` lists), else 422 `venue-not-in-tenant`. **Each day is then planned from that venue's own published map only**: its rides, its dining and its retail points, never another venue's.\n","items":{"type":"object","required":["date","venueId"],"properties":{"date":{"type":"string","format":"date"},"venueId":{"type":"string","format":"uuid"}}}},"dates":{"type":"array","minItems":1,"maxItems":7,"items":{"type":"string","format":"date"}},"party":{"type":"array","minItems":1,"maxItems":20,"description":"One entry per person. **Height where the guest knows it, age otherwise**: height is what ride eligibility rules test, and an age band is the fallback the rule may also state. Nothing here identifies a person.\n","items":{"type":"object","properties":{"heightCm":{"type":"integer","minimum":40,"maximum":230,"nullable":true},"ageYears":{"type":"integer","minimum":0,"maximum":120,"nullable":true}}}},"pace":{"type":"string","enum":["packed","relaxed"],"default":"relaxed"},"interestTags":{"type":"array","maxItems":12,"description":"The same closed list as `VenuePoint.interestTags`.","items":{"type":"string"}},"cuisineTags":{"type":"array","maxItems":8,"description":"Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). A cuisine no dining point of the day's venue serves is not forced into the day; it is reported in `VisitPlan.unmatchedPreferences`.\n","items":{"type":"string"}},"retailTags":{"type":"array","maxItems":8,"description":"**Shops the party would like to visit** (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options), e.g. `souvenirs`, `toys`, `apparel`, `essentials`. Matched per day against `VenuePoint.retailTags` of that day's venue's shops and retail kiosks; an unmatched tag is reported, as a cuisine is.\n","items":{"type":"string","maxLength":30}},"mustIncludePointIds":{"type":"array","maxItems":10,"description":"Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never placed on another venue's day.\n","items":{"type":"string","format":"uuid"}},"preset":{"type":"string","nullable":true,"enum":["highlights","family","thrillSeeker","waterDay","relaxed","showsAndDining"],"description":"A ready-made day plan (GST-052 Suggested Itineraries): the preset fixes the interests and the pace, and the party still decides eligibility.\n"},"presetKey":{"type":"string","nullable":true,"maxLength":64,"pattern":"^[a-z][a-zA-Z0-9]*$","description":"The ready-made plan the guest took on GST-052 (30 September, second wave of the 29 September pass, MOB-6): one of the built-in `preset` keys above, or a key of a ready-made plan the venue defines. **The same rules planner runs**: the preset only supplies interests, pace and must-include points, and the party still decides eligibility. When both `preset` and `presetKey` are sent they must name the same plan; `presetKey` is the field new clients send. An unknown key is refused 422 `unknown-preset`.\n"},"startTime":{"type":"string","nullable":true,"pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"When the party arrives. Null means opening time."},"locale":{"type":"string","nullable":true}}},
"VisitPlanUpdate": {"type":"object","x-ticvai-persistence":"none — request only; lands as a new version of venuemap.visit_plan_item rows","description":"What `updateVisitPlan` takes (29 September, MOB-6).","required":["baseVersion","changes"],"properties":{"baseVersion":{"type":"integer","minimum":1},"changes":{"type":"array","minItems":1,"maxItems":20,"items":{"type":"object","required":["op"],"properties":{"op":{"type":"string","enum":["swap","remove","add","move","pin","acceptAddOn","declineAddOn","revertTo"]},"itemId":{"type":"string","format":"uuid","nullable":true},"date":{"type":"string","format":"date","nullable":true},"pointId":{"type":"string","format":"uuid","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"startsAt":{"type":"string","format":"date-time","nullable":true},"version":{"type":"integer","nullable":true,"description":"For `revertTo`, the earlier version to restore (undo)."}}}}}},
"WaitTime": {"x-ticvai-persistence":"none — computed from readings and throughput","type":"object","required":["queueId","waitMinutes","source","asOf","isStale"],"properties":{"queueId":{"type":"string","format":"uuid"},"queueName":{"$ref":"#/components/schemas/LocalisedText"},"attractionProductId":{"type":"string","format":"uuid","nullable":true},"attractionCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. Read from catalogue, not stored here.\n"},"status":{"$ref":"#/components/schemas/QueueStatus"},"waitMinutes":{"type":"integer","nullable":true,"description":"Null where the queue is closed or no estimate is available."},"source":{"$ref":"#/components/schemas/WaitTimeSource"},"isStale":{"type":"boolean","description":"The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as current, and it is not hidden (decided 28 September, audit R080 (b)): the screen shows `waitMinutes` with its `asOf` and a stale marker.\n"},"heightRequirementCm":{"type":"integer","nullable":true},"zone":{"type":"string","nullable":true},"asOf":{"type":"string","format":"date-time","description":"When the figure was produced — the queue's `waitTimeAsOf`."}}},
"WaitTimeSource": {"type":"string","description":"Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed.\n","enum":["sensor","throughput","manual","unavailable"]}
}
```
