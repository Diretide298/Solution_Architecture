# P02-engagement-support-02 — P02 · Engagement & Support (2 of 2)

**2 screens · 7 operations · 17 schemas · 3 permissions**

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
  `AI_USE, CASE_MANAGE, CASE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **3 of these operations work offline**: createCase, getVisitPlan, getWaitTimes
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
| `GST-059` | Plan in Progress | A | 9 | 31 | 6 | 4 | 0 | 1 | guest | notStarted (designed) |
| `GST-068` | Help & My Cases | A | 17 | 36 | 6 | 11 | 3 | 0 | guest | notStarted (client-verified) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `GST-059` Plan in Progress

**Today's plan while you are in the venue, re-ordered against live waits.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #18218 (APP-MOB-GST-059) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | listDetail (comfortable density): `listProducts` reads the population and `getWaitTimes` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `planId` (GST-053), `venueId` (session), `itemId` (navigation) · cold entry: Opened from a reminder on the visit day: today's plan, or an offer to make one when there is none. `itemId` is the plan item the guest taps Swap on, picked on … |
| Route | `/general/plan-my-day-in-progress` |

**What the spec says about it.** Minuted 10 Aug §4.9. **The in-visit half of GST-051** — one capability, two moments. ** wired 24 August.** The board drew four bespoke AI endpoints for itinerary planning; **one operation with a kind answers all of them** (ADR-0028), and recording the outcome is what lets a model replace the heuristic later. **`recordSuggestionOutcome` removed from the guest surface.** `check-screens` refused it and was right: **a guest does not record an outcome — the platform observes what they did.** A guest app that self-reports whether it took the advice is a training label the guest could forge, and the observation belongs server-side where the plan and the visit can be compared. **Out of the first release** (decided 28 September, audit R187): the itinerary planner is deferred and this screen is `wave: 4` with a `deferred` block. Kept, not deleted, for the release that builds it. **Itinerary suggestion removed 28 September** (decided 28 September, audit R209): the planner is deferred (R187) and `requestSuggestion` refuses a guest anything but prepPlan, upsell and waitTime, so this screen no longer asks for a day plan. **Rev 3 (decided 29 September).** Had stayed in wave 4 (GAP-C3); superseded the same day by the re-plan below. **Brought into Block A on 29 September** (Chinmay, the 29 September re-plan, MOB-6): a rules-based planner with the AI planner agent on top. This supersedes audit R187, the deferral half of R209 and rev 3 GAP-C3; the `deferred` block is removed and the screen is wave 1. **Mobile v4 role (MOB-6): "Plan in Progress".** Today's plan against live waits …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |
| Version | number field | — | min 1 | `getVisitPlan` ?version |

**Sent by *Re-order my day*** (`updateVisitPlan`; no form is declared, so these are filled from the screen or collected inline)

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

**Today** (timeline, from `getVisitPlan`): Today's items with done, now and next; each ride with its live wait.

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

**Waits changed** (banner, from `getWaitTimes`): When a wait makes the next item late, proposes a re-order or a swap (`listVisitPlanAlternatives`); the guest decides.

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
| Re-order my day (primary button) | `updateVisitPlan` PUT `/visit-plans/{planId}` | VisitPlanUpdate | VisitPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `baseVersion` is not the current version (`plan-version-conflict`), or the plan is already `booked` … | — |
| Swap (secondary button) | `listVisitPlanAlternatives` GET `/visit-plans/{planId}/items/{itemId}/alternatives` | — | VisitPlanAlternative (paged) | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Data it reads**: `getWaitTimes` (onLoad, Wait times across a venue); `getVisitPlan` (onLoad, The plan: days, timed items and add-on suggestions, at its …)

**Where the user goes next**

- → `GST-053` Your Plan: *See the whole plan*; carries `planId`
- → `GST-038` At the Venue: *Directions (At the Venue, Map)*
- → `GST-001` Home: *Home tab*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The plan builds in place; the inputs stay on screen. |
| Error (`?state=error`) | Could not load the plan. Names what failed; the inputs are kept so trying again costs nothing. |
| Empty, first run (`?state=emptyFirstRun`) | No plan for today: offers to make one (GST-051). |
| Empty, no results (`?state=emptyNoResults`) | Nothing suits the whole party on that day (for example every ride is over a child's height): says so and offers to change the answers. |
| Permission denied (`?state=emptyNoAccess`) | A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it. |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `baseVersion` is not the current version (`plan-version-conflict`), or the plan is already `booked` (`plan-booked`; a booked plan is read-only, generate a new …; 422 A change names an item not on the plan, a `revertTo` version that does not exist, or a point the party is not eligible for (`item-not-eligible`, with the rule … |

#### Permissions

- `getWaitTimes` → no permission · guest, public
- `getVisitPlan` → no permission · guest
- `updateVisitPlan` → no permission · guest
- `listVisitPlanAlternatives` → no permission · guest

**A refused user sees:** A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |

#### Client meeting inputs

None names this screen.

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · names this screen)*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-059` · status **notStarted** · provenance designed · **Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no …
- Prototype (Mobile App v4, 29 September 2026, verified —, match none): `sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html`, view **
- Drawn by: Claude Code, 30 September 2026, drawn in the Mobile App v4 look
- Flow F49 *A guest plans a day and follows it*, step 6: They follow it through the day. → **Re-ordered as waits change**, with the guest deciding. A plan fixed at 9am is a plan abandoned by 11.
- ADR-0028 *Seventeen modules, and the data boundary decides where they split* (`docs/adr/0028-service-decomposition.md`)
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (31 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-059?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Re-order my day, Swap.
- [ ] Every transition is wired: `GST-053`, `GST-038`, `GST-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-068` Help & My Cases

****A guest could not raise a complaint.** Twelve case operations existed and every one of them was staff-side — a guest with a problem had to find somebody.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 2 · needs the `core` module |
| Block | Block A · ticket #18177 (APP-MOB-GST-068) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | listDetail (comfortable density): `listCases` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The offline banner shows.** Cases already loaded stay read-only with their age, so a guest can see what they raised without believing a reply arrived. **Raising a case and replying are disabled offline** — both need the connection (decided 28 September, audit R148) — and the screen says how to … |
| Opens with | `subjectId` (session) · cold entry: **Resolves from the session.** A guest arriving cold is asked to sign in and returned here afterwards — never a 404, and never a screen that silently shows … |
| Route | `/account/help-my-cases` |

**What the spec says about it.** **A guest could not raise a complaint.** Twelve case operations existed and every one of them was staff-side — a guest with a problem had to find somebody. **The AI concierge and a human case are one thread here.** A conversation that could not answer becomes a case rather than a dead end, which is what `listAiConversations` beside `listCases` is for.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Open · In progress · Awaiting guest · Escalated · Resolved · Closed | — | Sends `?status=` to `listCases`. | `listCases` ?status |
| Assigned to principal id | picker: choose an assigned to principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?assignedToPrincipalId=` to `listCases`. | `listCases` ?assignedToPrincipalId |
| Breached sla | toggle | optional | — | — | — | Sends `?breachedSla=` to `listCases`. | `listCases` ?breachedSla |
| Priority | radio group | optional | — | Low · Normal · High · Urgent | — | Sends `?priority=` to `listCases`. | `listCases` ?priority |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Membership | picker: choose a membership | — | — | `listCases` ?membershipId |

**Form: Create case** (modal, opened by *Create case*; *Create case* calls `createCase`, *Cancel* sends nothing)

**Collects what `createCase` sends before it is called.** Required: `id`, `subject`, `description`, `channel`, `recordedAt`. Optional: `subjectId`, `categoryId`, `priority`, `kind`, `venueId`, `relatedOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createCase` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `createCase` body |
| Subject `subject` | text field | required | — | max length 200 | — | — | `createCase` body |
| Description `description` | text area | required | — | max length 10000 | — | — | `createCase` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `createCase` body |
| Membership `membershipId` | picker: choose a membership | optional | — | — | shows names, sends the id | The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. | `createCase` body |
| Priority `priority` | radio group | optional | Normal | Low · Normal · High · Urgent | — | — | `createCase` body |
| Kind `kind` | select | optional | — | Lost property · Complaint · Question · Accessibility · Refund request · Other; Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.; A case raised as `other` must carry a non-empty `detail` … | — | What the guest says the case is about, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. | `createCase` body |
| Channel `channel` | select | required | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `createCase` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createCase` body |
| Related order `relatedOrderId` | text field | optional | — | — | — | — | `createCase` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | Stored on the opening `CaseMessage`, not on the case. | `createCase` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time the case was raised. The server stamps `Case.syncedAt` on arrival. | `createCase` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every case** (data table, from `listCases`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7. |
| Case number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Subject | the name it points at, never the id | — |
| Guest name | text | Resolved from `pii.subject` when the case is read, never stored on the case. A name copied onto a case row is personal data outside the … |
| Subject | text | The case's one-line title, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps … |
| Category | the name it points at, never the id | — |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |
| Priority | chip: Low, Normal, High, Urgent | — |
| Assigned to principal | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Related order | text | — |
| Sla due at | 1 Oct 2026, 14:30 | — |

**Every AI conversation** (data table, from `listAiConversations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Scope path | text | — |
| Module | chip: Tickets and booking, Membership, Events, Attractions, Virtual queue, Dining and fnb… | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not … |
| Locale | text | — |
| Message count | 1,234 | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Last message at | 1 Oct 2026, 14:30 | — |

**The selected case** (detail panel, from `listCases`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7. |
| Case number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Subject | the name it points at, never the id | — |
| Guest name | text | Resolved from `pii.subject` when the case is read, never stored on the case. A name copied onto a case row is personal data outside the … |
| Subject | text | The case's one-line title, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps … |
| Category | the name it points at, never the id | — |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |
| Priority | chip: Low, Normal, High, Urgent | — |
| Assigned to principal | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Related order | text | — |
| Sla due at | 1 Oct 2026, 14:30 | — |
| Is sla breached | yes / no (icon or chip) | Computed when read, never stored. True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` … |
| Sla paused seconds | 1,234 | Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock. |
| Escalation count | 1,234 | — |
| Resolved at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create case (primary button) | `createCase` POST `/cases` | CreateCaseRequest | Case | — | works offline; opens modal first |

**Data it reads**: `listCases` (onLoad, List service cases); `listAiConversations` (onLoad, A principal's conversation history)

**Where the user goes next**

- → `GST-039` Profile: *Profile*; carries `subjectId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Content loads. |
| Error (`?state=error`) | Could not load. **Says what failed and offers one way onward**, never a bare failure. |
| Empty, first run (`?state=emptyFirstRun`) | **No cases open.** The concierge sits here too — most questions never become a case, and that is the intent. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing here yet.** The scope is what narrowed it — naming the scope is what stops somebody concluding the record does not exist. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **The offline banner shows.** Cases already loaded stay read-only with their age, so a guest can see what they raised without believing a reply arrived. **Raising a case and replying are disabled offline** — both need the connection (decided 28 September, audit R148) — and the screen says how to reach staff in person instead: the guest services desk, or any member of staff. |

#### Permissions

- `createCase` → `CASE_MANAGE` (configure) · staff, guest, partner
- `listCases` → `CASE_VIEW` (read) · staff, guest, partner
- `listAiConversations` → `AI_USE` (operate) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.66 | Guest Support - System shall provide guest support channels. | Guest Mobile App & Branding | CONTRACTED | `createCase` |
| 19.2.70 | Complaint Management - System shall support guest complaints. | Guest Mobile App & Branding | CONTRACTED | `createCase` |
| 2.8.12 | System shall allow agents to create, assign, escalate, track, and resolve guest cases including complaints, refund requests, service requests, incidents, and operational issues. Cases shall be linked … | Ticketing Sales | CONTRACTED | `createCase` |
| 5.3.34 | Link guest profiles with customer service cases, complaints, incidents, refunds, investigations, and follow-up activities. | F&B & Guest Management | CONTRACTED | `createCase` |
| 22.3.1 | Case Creation | Marketing & CRM | CONTRACTED | `createCase` |
| 22.3.2 | Case Classification | Marketing & CRM | CONTRACTED | `createCase` |
| 22.3.3 | Case Assignment | Marketing & CRM | CONTRACTED | `createCase` |
| 22.8.12 | Case Creation & Escalation | Marketing & CRM | CONTRACTED | `createCase` |
| 22.2.17 | Case & Support History | Marketing & CRM | CONTRACTED | `listCases` |
| 8.4.29 | System shall expose AI services through APIs. | Unified Operations Dashboard | CONTRACTED | `listAiConversations` |
| 8.4.30 | System shall maintain AI interaction history. | Unified Operations Dashboard | CONTRACTED | `listAiConversations` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group ticket upgrades are business-configurable (off by default); where allowed a group raises an upgrade request (e.g. via chat/support) rather than self-serving like an individual. *(agreed · MoM 1 Sep 2026, 4.9 Clarified (group upgrades) · DI-607)*
- Cases can be logged from the customer app/website and from the call-centre/admin side, with category, priority, channel and SLA-based escalation rules. *(client request · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-390)*
- Support chat is native to TICVAI: a built-in AI chat assistant answers first, then escalates to a human "CR representative" role in the platform; offered white-labelled as a subscription add-on for smaller clients. *(agreed · MoM 12 Aug 2026, 10. Customer Support / Chat Integration Approach · DI-256)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-068` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 2 → Help & my cases*. Differences: The YAML lists AI conversations here (listAiConversations); the prototype shows them on the concierge home instead.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0030 *A deep link is a pointer, not authorisation* (`docs/adr/0030-deep-link-cold-entry.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state.
- [ ] Every output is drawn (36 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-068?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create case.
- [ ] Every transition is wired: `GST-039`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**3 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createCase": {"method":"POST","path":"/cases","contract":"marketing-crm","summary":"Raise a service case","permission":"CASE_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCaseRequest","responds":"Case"},
"getVisitPlan": {"method":"GET","path":"/visit-plans/{planId}","contract":"venue-map","summary":"A visit plan, at its current version or an earlier one","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"version","in":"query","required":null}],"requestBody":null,"responds":"VisitPlan"},
"getWaitTimes": {"method":"GET","path":"/queues/wait-times","contract":"queue","summary":"Wait times across a venue","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":true},{"name":"category","in":"query","required":null}],"requestBody":null,"responds":"WaitTime"},
"listAiConversations": {"method":"GET","path":"/conversations","contract":"ai","summary":"A principal's conversation history","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCases": {"method":"GET","path":"/cases","contract":"marketing-crm","summary":"List service cases","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"assignedToPrincipalId","in":"query","required":null},{"name":"breachedSla","in":"query","required":null},{"name":"priority","in":"query","required":null},{"name":"membershipId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVisitPlanAlternatives": {"method":"GET","path":"/visit-plans/{planId}/items/{itemId}/alternatives","contract":"venue-map","summary":"What could take this item's place","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"updateVisitPlan": {"method":"PUT","path":"/visit-plans/{planId}","contract":"venue-map","summary":"Swap, remove, add, move or undo, as a new version","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisitPlanUpdate","responds":"VisitPlan"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiConversation": {"type":"object","x-ticvai-persistence":"ai.conversation","required":["id","principalId","module","startedAt"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"module":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},"locale":{"type":"string"},"messageCount":{"type":"integer"},"startedAt":{"type":"string","format":"date-time"},"lastMessageAt":{"type":"string","format":"date-time"}}},
"Case": {"x-ticvai-persistence":"marketing.case","x-ticvai-retired-columns":["guest_name","subject","is_sla_breached"],"type":"object","required":["id","caseNumber","subject","status","priority","createdAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7."},"caseNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity. Assigned when the case reaches the server, so a retry with the same `id` keeps its number.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true},"guestName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"**Resolved from `pii.subject` when the case is read, never stored on the case.** A name copied onto a case row is personal data outside the erasable store (ADR-0023), and it had no source anyway — no request carries it. Returned only to callers holding `GUEST_VIEW_PII`, as `searchGuests` does.\n"},"subject":{"type":"string","x-ticvai-column":"title","description":"**The case's one-line title**, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps `subject` because screens bind it.\n"},"kind":{"allOf":[{"$ref":"#/components/schemas/CaseKind"}],"nullable":true,"description":"What the guest said it was about, where the guest raised it."},"channel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"description":"How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`."},"recordedAt":{"type":"string","format":"date-time","description":"Device time the case was raised — the start of the SLA clock."},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the case arrived. Equal to `recordedAt` for a case raised online."},"categoryId":{"type":"string","format":"uuid","nullable":true},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The `ServiceQueue` the case waits in, set by routing (`CaseRoutingRule.queueId`). Null once routed straight to an agent. (decided 29 September, data model for the agreed operations)"},"membershipId":{"type":"string","format":"uuid","nullable":true,"description":"The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. (decided 29 September, coordinator decision DM4, writers pass)"},"status":{"$ref":"#/components/schemas/CaseStatus"},"priority":{"$ref":"#/components/schemas/CasePriority"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"relatedOrderId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"isSlaBreached":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"**Computed when read, never stored.** True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` (or to now, while unresolved), less `slaPausedSeconds`, is past the target that set `slaDueAt`. A stored flag would need a job to flip it at the moment of breach, and no such job is designed; `listCases?breachedSla` filters on the same computation.\n"},"slaPausedSeconds":{"type":"integer","description":"Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock.\n"},"escalationCount":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"CaseKind": {"type":"string","description":"**What the guest says the case is about**, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.\n**`other` only with a note (decided 28 September, audit R222).** A case raised as `other` must carry a non-empty `detail` (`raiseMyCase`), or it is refused with 400; the notes are reviewed quarterly to add the real kinds they reveal.\n","enum":["lostProperty","complaint","question","accessibility","refundRequest","other"]},
"CasePriority": {"type":"string","enum":["low","normal","high","urgent"]},
"CaseStatus": {"type":"string","enum":["open","inProgress","awaitingGuest","escalated","resolved","closed"]},
"CreateCaseRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","subject","description","channel","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"subject":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":10000},"categoryId":{"type":"string","format":"uuid"},"membershipId":{"type":"string","format":"uuid","nullable":true,"description":"The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. Must belong to `subjectId` when both are given (422). (decided 29 September, coordinator decision DM4, writers pass)"},"priority":{"allOf":[{"$ref":"#/components/schemas/CasePriority"}],"default":"normal"},"kind":{"$ref":"#/components/schemas/CaseKind"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"venueId":{"type":"string","format":"uuid"},"relatedOrderId":{"type":"string"},"attachmentRefs":{"type":"array","description":"Stored on the opening `CaseMessage`, not on the case.","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time","description":"Device time the case was raised. The server stamps `Case.syncedAt` on arrival."}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"QueueStatus": {"type":"string","enum":["open","paused","closed","atCapacity"]},
"VisitPlan": {"type":"object","x-ticvai-persistence":"venuemap.visit_plan","description":"**A guest's visit plan** (29 September, MOB-6): the Plan tab. One row per plan; its items are `venuemap.visit_plan_item` rows carrying the version they belong to, so every earlier version stays readable and undo is a new version equal to an old one. **Owned by the guest session**, like a cart: `subjectId` when signed in, `sessionRef` for an anonymous device session, claimed on sign-in.\n","required":["id","venueId","status","version","days"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","readOnly":true,"description":"Derived from `venueId`."},"subjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"marketing.guest_profile","description":"The signed-in guest. From the session, never from the body."},"sessionRef":{"type":"string","nullable":true,"readOnly":true,"description":"The anonymous device session that owns the plan until sign-in."},"status":{"type":"string","enum":["draft","booked","archived"],"readOnly":true,"description":"`booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date."},"version":{"type":"integer","minimum":1,"readOnly":true,"description":"The current version. Every `updateVisitPlan` adds one."},"source":{"type":"string","enum":["rules","preset","aiAgent"],"readOnly":true,"description":"What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. **The guest sees which**, as every AI answer says what it is based on.\n"},"inputs":{"$ref":"#/components/schemas/VisitPlanRequest"},"mapVersion":{"type":"integer","readOnly":true,"description":"The published map version the plan was laid out on."},"cartId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"orders.cart","description":"The cart `bookVisitPlan` filled."},"excluded":{"type":"array","readOnly":true,"description":"**What was left out and why**, e.g. a coaster excluded because one of the party is under its 120 cm minimum. Shown on GST-053, so the planner never looks as if it forgot.\n","items":{"type":"object","properties":{"pointId":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","enum":["heightRule","ageRule","closedOnDate","notInInterests","noTime","notAtVenue"],"description":"`notAtVenue` (30 September, MoM 4.7): a must-include point that is at none of the plan's venues, so no day could hold it.\n"}}}},"unmatchedPreferences":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"**A preference a day's venue cannot meet is said, never faked** (30 September client meeting, MoM 4.7, Allam's requirement). One entry per day and preference that no point of that day's venue matches: a cuisine (`cuisineTags`), a shop (`retailTags`) or an interest (`interestTags`). `availableAtVenueIds` names the tenant's other active venues whose published map does match, so GST-053 and WEB-050 can say *Indian food is at the other park (day 2)* instead of quietly placing a restaurant the party cannot reach. Empty when every preference is met on every day. Worked out on read for the version read (a swap can meet or lose a preference), never stored.\n","items":{"type":"object","required":["date","venueId","preference","tag"],"properties":{"date":{"type":"string","format":"date"},"venueId":{"type":"string","format":"uuid","description":"The day's venue, which has no match."},"preference":{"type":"string","enum":["cuisine","retail","interest"]},"tag":{"type":"string","maxLength":30},"availableAtVenueIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Other active venues of the tenant where the tag is matched. Empty when none is."}}}},"days":{"type":"array","readOnly":true,"description":"One per date, in order. The items of the version read.","items":{"type":"object","required":["date","venueId","items"],"properties":{"date":{"type":"string","format":"date"},"venueId":{"type":"string","format":"uuid","description":"**The venue this day is planned at** (30 September, MoM 4.7): `VisitPlanRequest.dayVenues` for the date, else `venueId`. Every item of the day is at this venue.\n"},"opensAt":{"type":"string","nullable":true},"closesAt":{"type":"string","nullable":true},"items":{"type":"array","items":{"$ref":"#/components/schemas/VisitPlanItem"}}}}},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"VisitPlanAlternative": {"type":"object","x-ticvai-persistence":"none — computed on read","description":"One candidate for a swap (29 September, MOB-6).","required":["kind","venueId","startsAt","reason"],"properties":{"kind":{"type":"string","enum":["attraction","show","meal","shop","rest"]},"venueId":{"type":"string","format":"uuid","description":"The item's day venue; an alternative is never from another venue (30 September, MoM 4.7)."},"pointId":{"type":"string","format":"uuid","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"name":{"type":"string"},"startsAt":{"type":"string","format":"date-time"},"durationMinutes":{"type":"integer"},"walkMinutes":{"type":"integer","nullable":true},"expectedWaitMinutes":{"type":"integer","nullable":true},"matchedInterests":{"type":"array","items":{"type":"string"}},"reason":{"type":"string","description":"Why it is offered, in words the sheet shows, e.g. *Same thrill level, 4 minutes closer*."}}},
"VisitPlanItem": {"type":"object","x-ticvai-persistence":"venuemap.visit_plan_item","description":"**One timed stop on a plan day** (29 September, MOB-6). Rows are kept per `planVersion`: a change writes the day's items again under the new version, and an older version's rows are never updated.\n","required":["id","planId","planVersion","date","sequence","kind","startsAt","endsAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"planId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"venuemap.visit_plan"},"planVersion":{"type":"integer","minimum":1,"readOnly":true},"date":{"type":"string","format":"date"},"sequence":{"type":"integer","minimum":1},"kind":{"type":"string","enum":["attraction","show","meal","shop","rest","travel"],"description":"`meal` is a stop at a dining point (restaurant, cafe or food kiosk); `shop` is a retail stop at a shop or a retail kiosk (30 September client meeting, MoM 4.7: retail is placed from the day venue's own points, as dining is).\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"**The venue of this stop** (30 September client meeting, MoM 4.7): always the day's venue, and the venue whose map `pointId` is on. Carried on the item so the screens, `bookVisitPlan` and the AI planner agent read it rather than infer it. **Worked out on read, not stored**: from the plan's `inputs` (`dayVenues` for the item's date, else `venueId`). A stored `venue_id` would move the item rows from the plan's own row-level policy to a venue policy and hide a second park's items from the guest who owns the plan.\n"},"pointId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"venuemap.point"},"productId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"catalogue.product","description":"What is bought for this stop, where it is bought. Null for a free stop."},"bundleId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"promotions.bundle","description":"A meal combo or package, from the point's `featuredOffer`."},"performanceId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"catalogue.performance"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"walkMinutesBefore":{"type":"integer","minimum":0,"nullable":true},"expectedWaitMinutes":{"type":"integer","minimum":0,"nullable":true,"description":"The typical wait at that hour when the plan was laid out; GST-059 replaces it with the live one."},"addOnSuggestion":{"type":"object","nullable":true,"description":"A suggested add-on for this stop, e.g. Fast Track where the wait is long. Never added by itself.","properties":{"productId":{"type":"string","format":"uuid"},"reason":{"type":"string"}}},"addOnAccepted":{"type":"boolean","default":false},"pinned":{"type":"boolean","default":false,"description":"The guest fixed this stop; a re-lay moves other stops around it."},"note":{"type":"string","nullable":true,"maxLength":200}}},
"VisitPlanRequest": {"type":"object","x-ticvai-persistence":"none — request only; kept as `inputs` on venuemap.visit_plan","description":"What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050.\n","required":["venueId","dates","party"],"properties":{"venueId":{"type":"string","format":"uuid","description":"The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. Every date is planned at this venue unless `dayVenues` puts it somewhere else.\n"},"dayVenues":{"type":"array","maxItems":7,"description":"**Which venue on which date, in a multi-venue tenant** (30 September client meeting, MoM 4.7, Allam's requirement). One entry per date that is not at `venueId`; each date of `dates` at most once. Each venue must be an active venue of the caller's tenant (the options `getTenantAppStatus.venues` lists), else 422 `venue-not-in-tenant`. **Each day is then planned from that venue's own published map only**: its rides, its dining and its retail points, never another venue's.\n","items":{"type":"object","required":["date","venueId"],"properties":{"date":{"type":"string","format":"date"},"venueId":{"type":"string","format":"uuid"}}}},"dates":{"type":"array","minItems":1,"maxItems":7,"items":{"type":"string","format":"date"}},"party":{"type":"array","minItems":1,"maxItems":20,"description":"One entry per person. **Height where the guest knows it, age otherwise**: height is what ride eligibility rules test, and an age band is the fallback the rule may also state. Nothing here identifies a person.\n","items":{"type":"object","properties":{"heightCm":{"type":"integer","minimum":40,"maximum":230,"nullable":true},"ageYears":{"type":"integer","minimum":0,"maximum":120,"nullable":true}}}},"pace":{"type":"string","enum":["packed","relaxed"],"default":"relaxed"},"interestTags":{"type":"array","maxItems":12,"description":"The same closed list as `VenuePoint.interestTags`.","items":{"type":"string"}},"cuisineTags":{"type":"array","maxItems":8,"description":"Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). A cuisine no dining point of the day's venue serves is not forced into the day; it is reported in `VisitPlan.unmatchedPreferences`.\n","items":{"type":"string"}},"retailTags":{"type":"array","maxItems":8,"description":"**Shops the party would like to visit** (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options), e.g. `souvenirs`, `toys`, `apparel`, `essentials`. Matched per day against `VenuePoint.retailTags` of that day's venue's shops and retail kiosks; an unmatched tag is reported, as a cuisine is.\n","items":{"type":"string","maxLength":30}},"mustIncludePointIds":{"type":"array","maxItems":10,"description":"Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never placed on another venue's day.\n","items":{"type":"string","format":"uuid"}},"preset":{"type":"string","nullable":true,"enum":["highlights","family","thrillSeeker","waterDay","relaxed","showsAndDining"],"description":"A ready-made day plan (GST-052 Suggested Itineraries): the preset fixes the interests and the pace, and the party still decides eligibility.\n"},"presetKey":{"type":"string","nullable":true,"maxLength":64,"pattern":"^[a-z][a-zA-Z0-9]*$","description":"The ready-made plan the guest took on GST-052 (30 September, second wave of the 29 September pass, MOB-6): one of the built-in `preset` keys above, or a key of a ready-made plan the venue defines. **The same rules planner runs**: the preset only supplies interests, pace and must-include points, and the party still decides eligibility. When both `preset` and `presetKey` are sent they must name the same plan; `presetKey` is the field new clients send. An unknown key is refused 422 `unknown-preset`.\n"},"startTime":{"type":"string","nullable":true,"pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"When the party arrives. Null means opening time."},"locale":{"type":"string","nullable":true}}},
"VisitPlanUpdate": {"type":"object","x-ticvai-persistence":"none — request only; lands as a new version of venuemap.visit_plan_item rows","description":"What `updateVisitPlan` takes (29 September, MOB-6).","required":["baseVersion","changes"],"properties":{"baseVersion":{"type":"integer","minimum":1},"changes":{"type":"array","minItems":1,"maxItems":20,"items":{"type":"object","required":["op"],"properties":{"op":{"type":"string","enum":["swap","remove","add","move","pin","acceptAddOn","declineAddOn","revertTo"]},"itemId":{"type":"string","format":"uuid","nullable":true},"date":{"type":"string","format":"date","nullable":true},"pointId":{"type":"string","format":"uuid","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"startsAt":{"type":"string","format":"date-time","nullable":true},"version":{"type":"integer","nullable":true,"description":"For `revertTo`, the earlier version to restore (undo)."}}}}}},
"WaitTime": {"x-ticvai-persistence":"none — computed from readings and throughput","type":"object","required":["queueId","waitMinutes","source","asOf","isStale"],"properties":{"queueId":{"type":"string","format":"uuid"},"queueName":{"$ref":"#/components/schemas/LocalisedText"},"attractionProductId":{"type":"string","format":"uuid","nullable":true},"attractionCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. Read from catalogue, not stored here.\n"},"status":{"$ref":"#/components/schemas/QueueStatus"},"waitMinutes":{"type":"integer","nullable":true,"description":"Null where the queue is closed or no estimate is available."},"source":{"$ref":"#/components/schemas/WaitTimeSource"},"isStale":{"type":"boolean","description":"The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as current, and it is not hidden (decided 28 September, audit R080 (b)): the screen shows `waitMinutes` with its `asOf` and a stale marker.\n"},"heightRequirementCm":{"type":"integer","nullable":true},"zone":{"type":"string","nullable":true},"asOf":{"type":"string","format":"date-time","description":"When the figure was produced — the queue's `waitTimeAsOf`."}}},
"WaitTimeSource": {"type":"string","description":"Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed.\n","enum":["sensor","throughput","manual","unavailable"]}
}
```
