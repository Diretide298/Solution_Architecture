# P01-engagement-support-01 — P01 · Engagement & Support

**6 screens · 24 operations · 43 schemas · 4 permissions**

Platform P01 Guest Web · ships as **guest** ·
guest audience · web ·
online only

## Who this is for

**guest on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `AI_USE, CASE_MANAGE, CASE_VIEW, MARKETING_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store. Offline, a screen shows what was already loaded, under the banner below.
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
| `WEB-025` | Help Centre / FAQ | A | 13 | 44 | 5 | 9 | 5 | 0 | guest | review (client-verified) |
| `WEB-026` | Survey & Feedback | A | 16 | 0 | 5 | 7 | 2 | 0 | guest | review (client-verified) |
| `WEB-027` | Newsletter Subscription | A | 20 | 35 | 6 | 11 | 1 | 0 | guest | review (client-verified) |
| `WEB-028` | Contact & Venue Information | A | 0 | 17 | 5 | 0 | 0 | 0 | guest | review (client-verified) |
| `WEB-044` | AI Concierge – Home | A | 15 | 15 | 6 | 35 | 4 | 0 | guest | review (client-verified) |
| `WEB-046` | In-Venue Notifications | A | 11 | 12 | 6 | 5 | 2 | 0 | guest | review (client-verified) |

## Thin screens in this batch

**WEB-028 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `WEB-025` Help Centre / FAQ

**Answer a question without needing a person.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Engagement & Support · wave 1 · needs the `core` module |
| Block | Block A · ticket #17994 (APP-WEB-WEB-025) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getTenantAppStatus` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **The offline banner shows.** Cases already loaded stay read-only with their age, so a guest can see what they raised without believing a reply arrived. **Raising a case and replying are disabled offline** — both need the connection (decided 28 September, audit R148) — and the screen says how to … |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-and-support/help-centre-faq` |

**What the spec says about it.** Same content the AI concierge grounds on. One source, two surfaces. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Rev 3 (decided 29 September).** The guest Help screen shows the app status and a public, localised *What's new* (GAP-B2). Built as one implementation with WEB-045, both ids kept (GAP-D3). The live agent is reached through the concierge handover (`handoverToAgent` on WEB-044; GAP-B3, already).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Open · In progress · Awaiting guest · Escalated · Resolved · Closed | `listCases` ?status |
| Assigned to principal | picker: choose an assigned to principal | — | — | `listCases` ?assignedToPrincipalId |
| Breached sla | toggle | — | — | `listCases` ?breachedSla |
| Priority | radio group | — | Low · Normal · High · Urgent | `listCases` ?priority |
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

**The tenant app status** (detail panel, from `getTenantAppStatus`)

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
| Recent changes | list or chips (count when long) | Staff only. Names the principal behind each change, so it never reaches a public response. |

**Every case** (data table, from `listCases`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7. |
| Case number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Subject | the name it points at, never the id | — |
| Guest name | text | Resolved from `pii.subject` when the case is read, never stored on the case. A name copied onto a case row is personal data outside the … |
| Subject | text | The case's one-line title, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps … |
| Kind | chip: Lost property, Complaint, Question, Accessibility, Refund request, Other | What the guest said it was about, where the guest raised it. |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`. |
| Recorded at | 1 Oct 2026, 14:30 | Device time the case was raised — the start of the SLA clock. |
| Synced at | 1 Oct 2026, 14:30 | Server time the case arrived. Equal to `recordedAt` for a case raised online. |
| Category | the name it points at, never the id | — |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |
| Priority | chip: Low, Normal, High, Urgent | — |

**What's new** (card list, from `getTenantAppStatus`): Newest first, at most 10: version, date and the localised release notes, from `getTenantAppStatus` `whatsNew` (a public field; the staff-only `recentChanges` stays staff only).

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
| Create case (primary button) | `createCase` POST `/cases` | CreateCaseRequest | Case | — | opens modal first |

**Data it reads**: `getTenantAppStatus` (onLoad, App status and recent changes); `listCases` (onLoad, Cases this guest has open)

**Where the user goes next**

- → `WEB-027` Newsletter Subscription: *Newsletter Subscription*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Articles load |
| Error (`?state=error`) | Could not load |
| Empty, first run (`?state=emptyFirstRun`) | No articles — offers contact instead of an empty help centre |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** Cases already loaded stay read-only with their age, so a guest can see what they raised without believing a reply arrived. **Raising a case and replying are disabled offline** — both need the connection (decided 28 September, audit R148) — and the screen says how to reach staff in person instead: the guest services desk, or any member of staff. |

#### Permissions

- `getTenantAppStatus` → no permission · device, guest
- `createCase` → `CASE_MANAGE` (configure) · staff, guest, partner
- `listCases` → `CASE_VIEW` (read) · staff, guest, partner

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Duplicate screens become one implementation covering several screen IDs (mobile Transfer + Delivery & Sharing; web Wishlist / Devices & Consent; Help Centre + Help & Accessibility as one Help view with FAQ, cases, policies, accessibility tabs). Ticket-selection functions belong on GST-008. Web gets a Group Booking view. *(agreed · design review 29 Sep 2026, GAP-D3 · D. Duplicate screens merged; group booking on web · DI-1078)*
- Web screens carry: cart promo code (valid/invalid/expired) and empty basket with confirm; interrupted-payment recovery ("we are checking with your bank" → success/failed/unknown); reprint/resend tickets; UAE Pass sign-in, link guest checkout, sign out; support cases and Sahli handoff; FX rates with timestamp; remaining entitlements. *(agreed · design review 29 Sep 2026, GAP-B3 · B. Web — missing functions on existing screens · DI-1074)*
- The guest Help screen shows app status and a public, localised "what's new" (release notes). *(agreed · design review 29 Sep 2026, GAP-B2 · B. Help: app status + recent changes · DI-1073)*
- Support chat is native to TICVAI: a built-in AI chat assistant answers first, then escalates to a human "CR representative" role in the platform; offered white-labelled as a subscription add-on for smaller clients. *(agreed · MoM 12 Aug 2026, 10. Customer Support / Chat Integration Approach · DI-256)*
- Configurable FAQ section plus Terms & Conditions, Privacy Policy and Cookie Policy with an accept/deny prompt. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-191)*

Also apply: 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

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

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-025` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Header 'Help'*. Differences: Also carries policies and the accessibility statement (YAML WEB-045) and the case list (YAML WEB-034's listMyCases) on the same page.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state.
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-025?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create case.
- [ ] Every transition is wired: `WEB-027`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 5 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-026` Survey & Feedback

**Work with survey & feedback for this venue.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block A · ticket #18226 (APP-WEB-WEB-026) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the screen declares only writes (`submitReview`) and no read of a population — it is settings, not a list |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-and-support/survey-and-feedback` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

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

**Where the user goes next**

- → `WEB-027` Newsletter Subscription: *Newsletter Subscription*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Survey loads |
| Error (`?state=error`) | **Could not submit. The answers are kept on the form, and the guest retries by pressing Submit again** — nothing resends by itself: guest web is online-only (docs/architecture/offline-and-sync.md, *B2C web: None*), so there is no outbox behind this screen. The retry reuses the first attempt's `Idempotency-Key`, so a submit that did reach the server before the failure is not recorded as a second review. |
| Empty, first run (`?state=emptyFirstRun`) | — |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |

#### Permissions

- `submitReview` → no permission · guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

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

Also apply: 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-026` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match partial): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Account → 'Reviews & feedback'*. Differences: List of visits to rate with toast actions; no rating form or survey questions are drawn.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-026?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Submit review.
- [ ] Every transition is wired: `WEB-027`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-027` Newsletter Subscription

**Record newsletter subscription for this venue.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Engagement & Support · wave 2 · needs the `marketing` module |
| Block | Block A · ticket #18191 (APP-WEB-WEB-027) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listGuestDevices` reads the population and `getWishlist` reads one of them — list, select, act |
| Offline | **Not available, and the offline banner says why.** A consent change must reach the server to mean anything. |
| Opens with | `deviceId` (deepLink), `itemId` (deepLink), `subjectId` (session) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation … |
| Route | `/engagement-and-support/newsletter-subscription` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

#### Inputs: what the user enters or picks

**Form: Record consent** (modal, opened by *Record consent*; *Record consent* calls `recordConsent`, *Cancel* sends nothing)

**Collects what `recordConsent` sends before it is called.** Required: `purpose`, `decision`, `noticeVersion`, `source`, `recordedAt`. Optional: `channels`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Purpose `purpose` | select | required | — | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | — | — | `recordConsent` body |
| Decision `decision` | segmented control | required | — | Granted · Withdrawn · Not asked | — | — | `recordConsent` body |
| Channels `channels` | multi-select chips | optional | — | Email · SMS · Whatsapp · Push · In app · Post | — | Omit to apply to every channel the purpose covers. | `recordConsent` body |
| Notice version `noticeVersion` | text field | required | — | — | — | — | `recordConsent` body |
| Source `source` | select | required | — | Guest app · Website · Kiosk · POS · Call centre · Import · Agent recorded · Cookie banner · Checkout | — | `checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents` … | `recordConsent` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordConsent` body |

Errors to draw in the form: 400 Notice version unknown, or the purpose is not configured

**Form: Add to wishlist** (modal, opened by *Add to wishlist*; *Add to wishlist* calls `addToWishlist`, *Cancel* sends nothing)

**Collects what `addToWishlist` sends before it is called.** Required: `variantId`. Optional: `performanceId`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Variant `variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `addToWishlist` body |
| Performance `performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | Saving a specific date rather than the product generally. | `addToWishlist` body |
| Note `note` | text area | optional | — | max length 200 | — | — | `addToWishlist` body |

Errors to draw in the form: 404 Variant not found or not sellable in this venue

**Form: Register guest device** (modal, opened by *Register guest device*; *Register guest device* calls `registerGuestDevice`, *Cancel* sends nothing)

**Collects what `registerGuestDevice` sends before it is called.** Required: `platform`, `token`. Optional: `appVersion`, `osVersion`, `deviceModel`, `locale`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Platform `platform` | segmented control | required | — | Ios · Android · Web | — | — | `registerGuestDevice` body |
| Token `token` | text area | required | — | max length 512 | — | — | `registerGuestDevice` body |
| App version `appVersion` | text field | optional | — | — | — | — | `registerGuestDevice` body |
| Os version `osVersion` | text field | optional | — | — | — | — | `registerGuestDevice` body |
| Device model `deviceModel` | text field | optional | — | — | — | — | `registerGuestDevice` body |
| Locale `locale` | text field | optional | — | — | — | — | `registerGuestDevice` body |

**Form: Save marketing subscription** (modal, opened by *Save marketing subscription*; *Save marketing subscription* calls `setMarketingSubscription`, *Cancel* sends nothing)

**Collects what `setMarketingSubscription` sends before it is called.** Required: `id`, `subjectId`, `channel`, `listName`, `isSubscribed`. Optional: `source`, `unsubscribeToken`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Channel `channel` | segmented control | required | — | Email · SMS · Push | — | — | `setMarketingSubscription` body |
| List name `listName` | text field | required | — | — | — | — | `setMarketingSubscription` body |
| Is subscribed `isSubscribed` | toggle | required | — | — | — | — | `setMarketingSubscription` body |
| Source `source` | text field | optional | — | — | — | Where the opt-in happened, because a regulator asks. | `setMarketingSubscription` body |
| Unsubscribe token `unsubscribeToken` | text field | optional | — | — | — | Unsubscribe must work without a login. The link in a message carries the token and `setMarketingSubscription` accepts it in place of a session. | `setMarketingSubscription` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every guest device** (data table, from `listGuestDevices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Subject | the name it points at, never the id | — |
| Platform | chip: Ios, Android, Web | — |
| Token fingerprint | text | Hash of the token, not the token. The token itself is write-only — returning it would put a push credential in every response a support … |
| App version | text | — |
| Os version | text | — |
| Device model | text | — |
| Locale | text | — |
| Status | chip: Active, Revoked, Failed | — |
| Failure count | 1,234 | Consecutive delivery failures. Past the threshold the device is marked failed and stops being targeted — a dead token retried forever is … |
| Registered at | 1 Oct 2026, 14:30 | — |
| Last seen at | 1 Oct 2026, 14:30 | — |

**The selected guest device** (detail panel, from `listGuestDevices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Subject | the name it points at, never the id | — |
| Platform | chip: Ios, Android, Web | — |
| Token fingerprint | text | Hash of the token, not the token. The token itself is write-only — returning it would put a push credential in every response a support … |
| Token ref | text | A vault reference to the push token, written by the server from `registerGuestDevice.token` — the same pattern as … |
| App version | text | — |
| Os version | text | — |
| Device model | text | — |
| Locale | text | — |
| Status | chip: Active, Revoked, Failed | — |
| Failure count | 1,234 | Consecutive delivery failures. Past the threshold the device is marked failed and stops being targeted — a dead token retried forever is … |
| Registered at | 1 Oct 2026, 14:30 | — |
| Last seen at | 1 Oct 2026, 14:30 | — |
| Revoked at | 1 Oct 2026, 14:30 | — |

**The marketing subscription** (detail panel, from `getMarketingSubscription`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Subject | the name it points at, never the id | The guest — from the guest session, or from `unsubscribeToken` when there is no session. |
| Channel | chip: Email, SMS, Push | — |
| List name | text | — |
| Is subscribed | yes / no (icon or chip) | — |
| Source | text | Where the opt-in happened, because a regulator asks. |
| Unsubscribe token | text | Unsubscribe must work without a login. The link in a message carries the token and `setMarketingSubscription` accepts it in place of a … |

**The wishlist** (detail panel, from `getWishlist`)

| Shows | Format | Notes |
|---|---|---|
| Subject | the name it points at, never the id | — |
| Items | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Record consent (primary button) | `recordConsent` POST `/guests/{subjectId}/consents` | RecordConsentRequest | ConsentState | 400 Notice version unknown, or the purpose is not configured | opens modal first |
| Add to wishlist (secondary button) | `addToWishlist` POST `/guests/{subjectId}/wishlist` | inline | Wishlist | 404 Variant not found or not sellable in this venue | opens modal first |
| Register guest device (secondary button) | `registerGuestDevice` POST `/guests/{subjectId}/devices` | inline | GuestDevice | — | opens modal first |
| Remove from wishlist (destructive button) | `removeFromWishlist` DELETE `/guests/{subjectId}/wishlist/{itemId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Revoke guest device (destructive button) | `revokeGuestDevice` DELETE `/guests/{subjectId}/devices/{deviceId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Save marketing subscription (secondary button) | `setMarketingSubscription` PUT `/marketing-subscriptions` | MarketingSubscription | MarketingSubscription | — | opens modal first |

**Data it reads**: `getWishlist` (onLoad, Read a guest's saved items); `listGuestDevices` (onLoad, A guest's registered devices); `getMarketingSubscription` (onLoad, What this guest has opted into)

**What opens over it**

- confirmDialog *Remove from wishlist*: **Names what `removeFromWishlist` changes and what it leaves alone**, in the consequence rather than the verb. A newsletter subscription this affects should be identified in the dialog, not just counted.
- confirmDialog *Revoke guest device*: **Names what `revokeGuestDevice` changes and what it leaves alone**, in the consequence rather than the verb. A newsletter subscription this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | — |
| Error (`?state=error`) | Could not subscribe. **Consent is not recorded on a failed request**, because a subscription the guest believes happened and did not is worse than a visible failure |
| Empty, first run (`?state=emptyFirstRun`) | — |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the current filters. **The filters are named and clearable from here** — an empty list with the filter state hidden elsewhere is a person who thinks the data is gone. **Added 25 August with the derived list component**: a screen that lists has to say what it shows when the list is empty, and this screen gained the list before it gained the sentence. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **Not available, and the offline banner says why.** A consent change must reach the server to mean anything. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Notice version unknown, or the purpose is not configured |

#### Permissions

- `recordConsent` → no permission · guest
- `addToWishlist` → no permission · guest
- `getWishlist` → no permission · guest
- `listGuestDevices` → no permission · guest
- `registerGuestDevice` → no permission · guest
- `removeFromWishlist` → no permission · guest
- `revokeGuestDevice` → no permission · guest
- `getMarketingSubscription` → `MARKETING_VIEW` (read) · guest
- `setMarketingSubscription` → `MARKETING_VIEW` (read) · guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| 2.6.44 | System shall allow guests to save tickets, memberships, events, packages, add-ons, F&B items, retail products, and experiences to a wishlist for future purchase. Wishlist items shall remain linked to … | Ticketing Sales | CONTRACTED | `addToWishlist` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Consent policy governs marketing/newsletter/survey communications; customers who do not opt in must not receive promotional communications. *(client request · MoM 20 Aug 2026, 4.3 Consent, Data Privacy & Retention · DI-378)*

Also apply: 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Footer*, set in `CMS-007` Page Builder:

Also set there, as content the tenant writes: social links: platform.

*SEO metadata*, set in `CMS-013` SEO & Metadata:

Also set there, as content the tenant writes: locale.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-027` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match partial): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Account → 'Newsletters'; Contact page → 'Choose newsletters'*. Differences: Per-venue and channel toggles only for signed-in guests; no signed-out email sign-up form.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (35 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-027?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Record consent, Add to wishlist, Register guest device, Remove from wishlist, Revoke guest device, Save marketing subscription.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-028` Contact & Venue Information

**Find contact & venue information for this venue.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Engagement & Support · wave 1 · needs the `core` module |
| Block | Block A · ticket #17818 (APP-WEB-WEB-028) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getTenantAppStatus` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-and-support/contact-and-venue-information` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Contact bound 28 September** to `getTenantAppStatus.contact` (decided 28 September, audit R073 (f)).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**The tenant app status** (detail panel, from `getTenantAppStatus`)

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
| Recent changes | list or chips (count when long) | Staff only. Names the principal behind each change, so it never reaches a public response. |

**How to reach the venue** (detail panel, from `getTenantAppStatus`): **From `getTenantAppStatus.contact`** (decided 28 September, audit R073 (f)): phone, email, WhatsApp, address and opening hours, set from CMS-001 through `setMaintenanceMode`. Each is optional and a missing one is left out rather than shown blank.

| Shows | Format | Notes |
|---|---|---|
| Phone | +971 50 123 4567 | — |
| Email | email, tap to write | — |
| Whatsapp | text | — |
| Address | in the reader's language | — |
| Opening hours | in the reader's language | Prose, as the guest reads it. The bookable hours are the catalogue's. |

**Data it reads**: `getTenantAppStatus` (onLoad, App status and recent changes)

**Where the user goes next**

- → `WEB-027` Newsletter Subscription: *Newsletter Subscription*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Venue details |
| Error (`?state=error`) | Could not load. Falls back to the tenant contact details from the cached config |
| Empty, first run (`?state=emptyFirstRun`) | — |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |

#### Permissions

- `getTenantAppStatus` → no permission · device, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

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

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-028` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Footer 'Contact', or Discover → 'Contact & venue info'*. Differences: Links to parking and accessibility from the contact cards; otherwise matches.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-028?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `WEB-027`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-044` AI Concierge – Home

**Ask, and be answered or handed to a person.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Engagement & Support · wave 2 · needs the `ai` module |
| Block | Block A · ticket #18193 (APP-WEB-WEB-044) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getGuestMenu` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Not available, and the offline banner says why.** The assistant needs the connection; conversations already loaded stay readable. |
| Opens with | `conversationId` (deepLink), `outletId` (session), `messageId` (navigation) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared link, a scanned code and a … |
| Route | `/ai-concierge` |

**What the spec says about it.** **A concierge in a browser is a concierge.** ADR-0020 keeps it read-only against the transactional core regardless of surface. **Renamed 31 August** from *AI Concierge*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest. **Cross-surface parity, 31 August**: added getGuestMenu. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations. **Rev 3 (decided 29 September, rev 3 CFG-5).** The concierge entry shows as mascot art when `BookingFlowConfig.conciergeMascot` is on (default on), otherwise as a plain button.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| At | date and time picker | — | — | `getGuestMenu` ?at |
| Language | language picker | — | — | `getGuestMenu` ?language |

**Form: Send conversation message** (modal, opened by *Send conversation message*; *Send conversation message* calls `sendConversationMessage`, *Cancel* sends nothing)

**Collects what `sendConversationMessage` sends before it is called.** Required: `body`. Optional: `attachments`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Body `body` | text area | required | — | max length 4000 | — | — | `sendConversationMessage` body |
| Attachments `attachments` | repeatable rows | optional | — | — | — | — | `sendConversationMessage` body |
| Asset `attachments[].assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `sendConversationMessage` body |
| Kind `attachments[].kind` | select | optional | — | Image · Video · Document · Ticket · QR · Payment link | — | — | `sendConversationMessage` body |

**Form: Create AI conversation** (modal, opened by *Create AI conversation*; *Create AI conversation* calls `createAiConversation`, *Cancel* sends nothing)

**Collects what `createAiConversation` sends before it is called.** Required: `module`. Optional: `locale`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Module `module` | select | required | — | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | — | Which part of the platform the conversation is about (8.4.1). | `createAiConversation` body |
| Locale `locale` | text field | optional | — | — | — | 8.4.3. Multilingual, and Arabic is not an afterthought here. | `createAiConversation` body |

**Form: Send AI message** (modal, opened by *Send AI message*; *Send AI message* calls `sendAiMessage`, *Cancel* sends nothing)

**Collects what `sendAiMessage` sends before it is called.** Required: `content`. Optional: `collectionIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Content `content` | text area | required | — | min length 1; max length 8000 | — | — | `sendAiMessage` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | Restrict retrieval to named collections. Absent means every collection the principal may read. | `sendAiMessage` body |

**Form: Handover to agent** (modal, opened by *Handover to agent*; *Handover to agent* calls `handoverToAgent`, *Cancel* sends nothing)

**Collects what `handoverToAgent` sends before it is called.** Required: `reason`. Optional: `summary`, `preferredQueueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Guest requested · Assistant refused · Assistant failed · Out of scope · Negative sentiment · Complex intent · Payment issue | — | — | `handoverToAgent` body |
| Summary `summary` | text field | optional | — | — | — | The assistant's own summary of what the guest wants, so the agent opens with context rather than reading a transcript while somebody waits. | `handoverToAgent` body |
| Preferred queue `preferredQueueId` | picker: choose a preferred queue | optional | — | — | shows names, sends the id | — | `handoverToAgent` body |

Errors to draw in the form: 409 No agent available. Returns the reason and offers a case, rather than queuing a guest for somebody who is not there. (HandoverRefusedProblem)

**Form: Request suggestion** (modal, opened by *Request suggestion*; *Request suggestion* calls `requestSuggestion`, *Cancel* sends nothing)

**Collects what `requestSuggestion` sends before it is called.** Required: `kind`. Optional: `subjectRef`, `horizon`, `context`. Dismissing sends nothing; the screen behind is unchanged.

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

**AI Concierge** (card list)

**Detail** (detail panel)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create AI conversation (primary button) | `createAiConversation` POST `/conversations` | inline | AiConversation | — | opens modal first |
| Send AI message (secondary button) | `sendAiMessage` POST `/conversations/{conversationId}/messages` | inline | AiMessage | — | opens modal first |
| Handover to agent (secondary button) | `handoverToAgent` POST `/conversations/{conversationId}/handover` | inline | Conversation | 409 No agent available. Returns the reason and offers a case, rather than queuing a guest for somebody who is not there. (HandoverRefusedProblem) | opens modal first |
| Request suggestion (secondary button) | `requestSuggestion` POST `/ai/suggestions` | inline | Suggestion | 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem) | opens modal first |
| Send conversation message (secondary button) | `sendConversationMessage` POST `/conversations/{conversationId}/messages` | inline | ConversationMessage | — | opens modal first |

**Data it reads**: `getGuestMenu` (onLoad, The menu a guest sees); `listAiConversations` (onLoad, Earlier conversations)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Content resolves in place. |
| Error (`?state=error`) | Could not load. **The rest of the site is unaffected.** |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing here yet for this venue.** Names what turns it on rather than showing an empty panel. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches. |
| Permission denied (`?state=emptyNoAccess`) | **Sign in to see this.** A guest who is not signed in is offered the door, not refused. |
| Offline (`?state=offline`) | **Not available, and the offline banner says why.** The assistant needs the connection; conversations already loaded stay readable. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 No agent available. Returns the reason and offers a case, rather than queuing a guest for somebody who is not there. (HandoverRefusedProblem); 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem) |

#### Permissions

- `createAiConversation` → `AI_USE` (operate) · staff, guest
- `sendAiMessage` → `AI_USE` (operate) · staff, guest
- `handoverToAgent` → no permission · guest
- `requestSuggestion` → `AI_USE` (operate) · staff, guest
- `getGuestMenu` → no permission · guest, staff
- `listAiConversations` → `AI_USE` (operate) · staff, guest
- `sendConversationMessage` → `CASE_MANAGE` (configure) · staff, guest
- `recordAnswerFeedback` → `AI_USE` (operate) · staff, guest

**A refused user sees:** **Sign in to see this.** A guest who is not signed in is offered the door, not refused.

#### Requirements it meets

35 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.4.1 | System shall provide a conversational AI assistant across all platform modules. | Unified Operations Dashboard | CONTRACTED | `createAiConversation` |
| 8.4.2 | System shall support natural language interaction. | Unified Operations Dashboard | CONTRACTED | `createAiConversation` |
| 8.4.3 | System shall support multilingual AI interactions. | Unified Operations Dashboard | CONTRACTED | `createAiConversation` |
| 8.1.5 | Explainability System shall provide reasoning and confidence indicators where available. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.19 | System shall support AI-powered ticketing assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.20 | System shall support AI-powered support assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 18.10.1 | AI Assistant - System shall provide an AI assistant for employees. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.3 | Operational Queries - Users shall retrieve operational information through AI. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.4 | Work Order Assistance - AI shall assist users with work order activities. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.5 | Knowledge Base Assistance - AI shall provide access to operational knowledge and procedures. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 22.8.4 | AI Chatbot Assistant | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.13 | AI Intent Recognition | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| … 23 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The concierge (Sahli) shows as mascot art or as a plain button; setting "Concierge mascot", default on. *(agreed · design review 29 Sep 2026, CFG-5 · Sahli mascot (on/off) · DI-1069)*
- The AI chat box answers guided/predefined queries (booking status, rescheduling) and logs guest conversation history across channels (WhatsApp, web, Instagram, Facebook) with per-channel conversion attribution. *(client request · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-388)*
- AI concierge answers natural-language guest questions (ticketing, F&B, retail, venue info, timings) grounded in the venue's configured data. *(client request · MoM 10 Aug 2026, 4.6 AI Functions, Lost & Found, Reviews, Loyalty · DI-207)*
- **Open question.** AI concierge chat design is deferred until a dedicated AI workshop settles the technical approach (third-party LLM with PII masking) and the token/billing model. *(open · MoM 10 Aug 2026, 4.2 AI Concierge Chat — Open Item · DI-195)*

Also apply: 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

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

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-044` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Floating 'Ask Sahli' button on every page*. Differences: A floating chat panel rather than a home screen; no conversation history list (listAiConversations).
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-044?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create AI conversation, Send AI message, Handover to agent, Request suggestion, Send conversation message.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-046` In-Venue Notifications

**Queue calls, order updates, venue notices.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Engagement & Support · wave 2 · needs the `marketing` module |
| Block | Block A · ticket #18168 (APP-WEB-WEB-046) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · light theme |
| Pattern | configEditor (compact density): `listMyNotifications` reads the feed (decided 29 September, rev 3 GAP-C1); the location-session claim stays a form on the same screen, so the pattern is kept until the screen is redrawn |
| Offline | **The offline banner shows.** Notices already received stay listed. New queue calls and order updates arrive once the connection is back, and the banner is the warning that they may be late. |
| Opens with | nothing: it opens on its own · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared link, a scanned code and a … |
| Route | `/in-venue-notifications` |

**What the spec says about it.** **Web push is weaker than native and it is not absent.** A guest with a tab open gets their queue call; the app does it better and the web does it. **Back in the first release** (decided 29 September, rev 3 GAP-C1): the notifications feed is needed in the first release, which reverses audit R242's deferral of this screen. The `deferred` block is removed and the screen returns to `wave: 2`, where it sat before R242. Queue calls and order status still also show on the queue and order screens, which poll.

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

**Detail** (detail panel)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Claim location session (primary button) | `claimLocationSession` POST `/location-sessions` | inline | LocationSession | 400 Neither a location code nor a seat reference supplied; 409 Code expired or unknown, the location is out of service, or no outlet currently delivers to it — a cabana is useless as an address if nothing serves it. | — |
| Mark all as read (secondary button) | `markMyNotificationsRead` POST `/me/notifications/read` | inline | inline | — | — |

**Data it reads**: `listMyNotifications` (onLoad, The guest's notification feed, newest first: queue calls …)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Content resolves in place. |
| Error (`?state=error`) | Could not load. **The rest of the site is unaffected.** |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing here yet for this venue.** Names what turns it on rather than showing an empty panel. |
| Permission denied (`?state=emptyNoAccess`) | **Sign in to see this.** A guest who is not signed in is offered the door, not refused. |
| Offline (`?state=offline`) | **The offline banner shows.** Notices already received stay listed. New queue calls and order updates arrive once the connection is back, and the banner is the warning that they may be late. |
| Empty, no results (`?state=emptyNoResults`) | **No unread notifications.** Names the Unread only filter and offers to show all; the read ones are still there. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither a location code nor a seat reference supplied; 409 Code expired or unknown, the location is out of service, or no outlet currently delivers to it — a cabana is useless as an address if nothing serves it. |

#### Permissions

- `claimLocationSession` → no permission · guest
- `listMyNotifications` → no permission · guest
- `markMyNotificationsRead` → no permission · guest

**A refused user sees:** **Sign in to see this.** A guest who is not signed in is offered the door, not refused.

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

- The in-venue notifications feed is needed in the first release on web and mobile (R242 deferral reversed). *(agreed · design review 29 Sep 2026, GAP-C1 · C. Wave 2: In-Venue Notifications · DI-1075)*
- A visual venue map highlights long-queue rides vs low-queue alternatives so operations can redirect guests, e.g. a notification suggesting a nearby ride with a shorter wait. *(client request · MoM 7 Sep 2026, 4.17 AI guest flow optimization · DI-682)*

Also apply: 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-046` · status **review** · provenance client-verified
- Prototype (rev 3 (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Summit Peaks → header 'At the venue' → Alerts*. Differences: Deferred in the YAML (release later, R242: no in-app feed in the first release), but the prototype draws it as a live section, so the client will expect it.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-046?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline, emptyNoResults.
- [ ] Every action is wired with its success and its failure: Claim location session, Mark all as read.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**P01 reference designs** (from `handoff/design-batches/apps/1-guest-app/README.md`)

- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the website. Rev 3 with the 29 September fixes and the 30 September feedback (group booking with a headcount, multi-park counters, surf session tickets, the swim-ability answer, transport stations and departures, popular route cards; `CLIENT-RESPONSE-30SEP.md` beside it). The client approved it for development once W1 to W10 are in.
- `sources/designs/guest-rev3-30-september/TICVAI Visit Planner.dc.html`: the visit planner. WEB-050 Plan Your Visit is this file.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-026, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-038, DI-040, DI-042, DI-044, DI-045, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P01 as a whole** (23: 3 open, 20 closed). Open first; a closed row says where it went on 30 September.

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker)*
- **S9** Final UI/UX for the website and the mobile app *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **T1** Feedback on the revised website and mobile wireframes *(Allam / Qossai · Open · due 1 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A28** Review the 'Viva Ticket' website as a reference for ticket-flow variations *(Softlabs Design Team · Low · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A29** Collate design references/inspiration and share with TICVAI, organized by mobile app, website, and admin/back-office pages *(Softlabs (Sahil & Aishwarya) · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A55** Implement per-tenant module visibility toggles (e.g., hide Dining, Retail, or other services) configurable independently for the guest website and mobile app *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker)*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker)*
- **A115** Apply HA selectively to revenue-critical components (ticketing, POS, B2C) same-region, with multi-region DR as an optional add-on *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 24 Aug 2026 · workshop tracker)*
- **A118** Commission the third-party penetration test before go-live (ticketing, B2C, B2B, mobile apps) and resolve all severities *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 24 Aug 2026 · workshop tracker)*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker)*
- **A174** Cross-check the six previously-scoped wallet types against Allam's documentation and deliver the three wireframe flows (ticketing, F&B, retail) plus the revised B2C flow *(Chinmay Parab / Pradnya Yeram / Allam · High · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker)*
- … 9 more in `handoff/design-inputs/task-tracker-index.json`

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

### Across P01 Guest Web

- Step-indicator style is configurable, the same as on the web: bars, dots, counters or step names. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1093)*
- **Open question.** Real venue photos, clips and logos are still to come from the client; designs use stand-ins. Slots expected: a photo per ticket card and clip per card, a square shot per extra/shop item, one landscape poster per venue for the single-event page. Photos ≥1600 px, clips mp4 6–12 s, no audio. *(open · design review 29 Sep 2026, Asset list — TICVAI Guest Booking · DI-1080)*
- The tenant picks which logo lockup sits in the nav bar and a logo variant (Light, Dark, Duotone) whose colours drive the theme. *(agreed · design review 29 Sep 2026, CFG-4 · Brand logo + Logo palette (Light/Dark/Duotone) · DI-1068)*
- Theme settings: surface style Glass (default) or Solid cards; button style Solid (default), Outline or Pill. *(agreed · design review 29 Sep 2026, CFG-3 · Surfaces (Glass/Solid) and Buttons (Solid/Outline/Pill) · DI-1067)*
- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Guest-facing copy may say "session" (surf sessions, timed sessions) as a glossary exception, like "Booking". *(agreed · design review 29 Sep 2026, CFG-10 · 'Sessions can be added, edited or closed from Config -> Sessions' · DI-1064)*
- Never ask the same thing twice: table zone is picked on the table map (no zone step before it); height is asked once (height bands on the water-park day pass are the eligibility check); party/school summaries prefill headcount, child's name and age from the earlier form. *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): repeated steps removed · DI-1000)*
- Confirmed final: cart sliding in from the right or bottom, card size options, and cart-sidebar placement left or right; Qossai specifically liked the compact card size. No further changes requested. *(agreed · MoM 24 Sep 2026, 4.10 Guest Web App — Card Layout & Cart Configuration Confirmed · DI-991)*
- Headers are reserved for standard elements only (venue image, category tabs, language bar, profile icon), applied consistently; date/availability selection belongs in the main content below the header, never in the header. Header/layout patterns must be adapted for mobile, which looks and behaves differently. *(agreed · MoM 24 Sep 2026, 4.9 Guest Web App — Specific UX Feedback (Header/Date Placement Standardization) · DI-990)*
- A language button (EN / العربية) sits in the header next to the profile icon, web and mobile. Arabic flips the whole layout right-to-left and switches interface text (navigation, buttons, booking steps, ticket names and tags, cart, seat map, checkout, account). Venue, show and dish names stay as written. *(client request · design review 23 Sep 2026, Header 2. Language icon in the header · DI-975)*
- Replace "Sign in / Create account" in the header with a single profile icon. It opens one screen with Log in and Register tabs; signed-in guests get their account menu from the same icon. *(client request · design review 23 Sep 2026, Header 1. One profile icon in the header that opens login / register · DI-974)*
- Allam's model reference: a simple card-based family-entertainment-centre site with minimal clicks, a right-side cart drawer, "help me choose", clear categories, video that autoplays when a guest taps "read more", adapting seamlessly between desktop and mobile. Allam and Qossai want this simplicity to guide the guest experience. *(client request · MoM 18 Sep 2026, 4.14 Guest Website UX Review — Upsell/Cross-Sell Placement & Reference Sites · DI-952)*
- **Open question.** Allam expects a large volume of feedback on the guest web/mobile prototype; detailed feedback goes to a separate dedicated session with Qossai and Allam. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-888)*
- The reviewed prototype is the actual guest-facing B2C site customers browse and book from, not a CMS tool. A separate, more limited white-label interface lets a client adjust colours, fonts and layout from a menu of options; not yet built in the prototype. *(agreed · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-887)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*
- Qossai is dissatisfied with the current B2C guest platform build and wants a separate vision session; references: the "Little Explorer" site and Six Flags. Six Flags cues: single-page flow. *(client request · MoM 8 Sep 2026, 4.20 Planning & Next Steps · DI-736)*
- Allam: most guests book from a smartphone, so the mobile version of the booking flows is the higher priority to validate (only desktop shown). *(client request · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough · DI-684)*
- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*
- Configurable cookie consent banner (accept/reject) per website; some cookies flagged mandatory (non-rejectable), others optional; templated and configurable in the system. *(client request · MoM 1 Sep 2026, 4.13 Privacy Consent & Cookie Policy · DI-617)*
- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*
- Confirmed: a guest always books a product or package — never a resource (a specific room, vehicle or instructor by itself) directly — on every sales channel, including the guest/mobile app; the product's configuration determines which resources are booked behind the scenes. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-502)*
- Six Flags Kidiya reference: fixed header with configurable navigation (logo, Explore/Tickets/Passes, sub-menus), every item toggleable via the CMS. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-424)*
- Allam: the venue's main website is fully venue-managed; after "Book Now" the white-label B2C flow keeps the venue's header/footer branding while product selection, cart and checkout are TICVAI-managed. Header/footer links to non-checkout pages redirect to the main venue site. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-397)*
- Ticketing, F&B and retail share one cart and checkout, one unified receipt and one QR/wristband per customer — no separate receipts or wristbands per product line. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-293)*
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)*
- Qossai: the TICVAI name must always remain visible to end users of a client-branded guest app (e.g. a "Made by TICVAI" credit) and cannot be removed by the client. *(agreed · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-250)*
- Qossai: present products with video rather than static images (as Talabat-style apps do); see benchmark app "222" for further inspiration. *(client request · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-222)*
- Qossai shared reference apps (Al Qadiya / Six Flags Saudi Arabia, and "The District" by Zomato) and cited their use of video over static images as design inspiration. *(client request · MoM 5 Aug 2026, 13. Mobile / POS App Design References · DI-146)*
- A single cart/order must take mixed purchases (e.g. family tickets plus gift vouchers) with one unified checkout and identity capture. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-141)*
- Base ticket-booking UX (web and mobile) on current market best practice rather than the demoed references as-is; Allam recommends the "Viva Ticket" website as a reference for the flow variations. *(agreed · MoM 3 Aug 2026, 10. Reference Material & Design Research · DI-125)*
- A multi-language toggle switches the entire site's content. *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-120)*
- Allam: banner, header, footer and background color are CMS-configurable per client, but site structure and navigation flow are fixed and adapt automatically to product configuration (dated, non-dated, seated, membership products surface the right fields). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-119)*
- All sites are fully mobile-responsive; e.g. the desktop calendar view collapses into a mobile-optimized layout. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-113)*
- A "powered by [platform]" footer credit is fixed and not client-editable. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-111)*
- One client can run multiple branded sites from the same setup, e.g. two brands sharing a footer but with distinct headers and hero banners. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-110)*
- White-label sites share one platform/template but each is configured independently: header, footer, logo, colors, fonts and hero banner are client-editable from the backend. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-108)*
- Selling reference layout: clean top navigation; category tabs with counts (All Events 32, Exhibitions, Guided Tours ...); sort and type chips (Price, Rating, Popular; General, Seated, Multipass, Scheduled, Rental); content cards with large image, type badge, rating, tags (LIMITED, NEW, BESTSELLER), availability ("180 available", "11 left") and "from" price; persistent cart on the right with member discount, totals and "Checkout Securely". *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, items 2-5 · DI-026)*
- Preliminary perceived-performance targets: web pages load in under about 3 seconds, mobile app loads in under about 2 seconds, ticket validation responds in under 500 milliseconds. *(agreed · MoM 28 Jul 2026, 18. Performance and Scalability · DI-015)*

**14 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addToWishlist": {"method":"POST","path":"/guests/{subjectId}/wishlist","contract":"marketing-crm","summary":"Save an item","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Wishlist"},
"claimLocationSession": {"method":"POST","path":"/location-sessions","contract":"fnb","summary":"Tell the platform where the guest is","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"LocationSession"},
"createAiConversation": {"method":"POST","path":"/conversations","contract":"ai","summary":"Open a conversation","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiConversation"},
"createCase": {"method":"POST","path":"/cases","contract":"marketing-crm","summary":"Raise a service case","permission":"CASE_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCaseRequest","responds":"Case"},
"getGuestMenu": {"method":"GET","path":"/outlets/{outletId}/guest-menu","contract":"fnb","summary":"The menu a guest sees","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"at","in":"query","required":null},{"name":"language","in":"query","required":null}],"requestBody":null,"responds":"GuestMenu"},
"getMarketingSubscription": {"method":"GET","path":"/marketing-subscriptions","contract":"marketing-crm","summary":"What this guest has opted into","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"MarketingSubscription"},
"getTenantAppStatus": {"method":"GET","path":"/tenant-config/status","contract":"white-label","summary":"App status and recent changes","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"TenantAppStatus"},
"getWishlist": {"method":"GET","path":"/guests/{subjectId}/wishlist","contract":"marketing-crm","summary":"Read a guest's saved items","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[],"requestBody":null,"responds":"Wishlist"},
"handoverToAgent": {"method":"POST","path":"/conversations/{conversationId}/handover","contract":"marketing-crm","summary":"Pass an assistant conversation to a person","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Conversation"},
"listAiConversations": {"method":"GET","path":"/conversations","contract":"ai","summary":"A principal's conversation history","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCases": {"method":"GET","path":"/cases","contract":"marketing-crm","summary":"List service cases","permission":"CASE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"assignedToPrincipalId","in":"query","required":null},{"name":"breachedSla","in":"query","required":null},{"name":"priority","in":"query","required":null},{"name":"membershipId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listGuestDevices": {"method":"GET","path":"/guests/{subjectId}/devices","contract":"marketing-crm","summary":"A guest's registered devices","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMyNotifications": {"method":"GET","path":"/me/notifications","contract":"marketing-crm","summary":"The signed-in guest's notification feed","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null},{"name":"unreadOnly","in":"query","required":null},{"name":"venueId","in":"query","required":null}],"requestBody":null,"responds":"Page"},
"markMyNotificationsRead": {"method":"POST","path":"/me/notifications/read","contract":"marketing-crm","summary":"Mark the signed-in guest's notifications read","permission":null,"offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"recordAnswerFeedback": {"method":"POST","path":"/messages/{messageId}/feedback","contract":"ai","summary":"Say whether an answer helped","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiAnswerFeedback"},
"recordConsent": {"method":"POST","path":"/guests/{subjectId}/consents","contract":"marketing-crm","summary":"Record a consent decision","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RecordConsentRequest","responds":"ConsentState"},
"registerGuestDevice": {"method":"POST","path":"/guests/{subjectId}/devices","contract":"marketing-crm","summary":"Register a device for push","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestDevice"},
"removeFromWishlist": {"method":"DELETE","path":"/guests/{subjectId}/wishlist/{itemId}","contract":"marketing-crm","summary":"Remove a saved item","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"requestSuggestion": {"method":"POST","path":"/ai/suggestions","contract":"ai","summary":"Ask for an answer, however it is currently produced","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Suggestion"},
"revokeGuestDevice": {"method":"DELETE","path":"/guests/{subjectId}/devices/{deviceId}","contract":"marketing-crm","summary":"Revoke a device registration","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"sendAiMessage": {"method":"POST","path":"/conversations/{conversationId}/messages","contract":"ai","summary":"Ask","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiMessage"},
"sendConversationMessage": {"method":"POST","path":"/conversations/{conversationId}/messages","contract":"marketing-crm","summary":"Say something, as a guest or an agent","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConversationMessage"},
"setMarketingSubscription": {"method":"PUT","path":"/marketing-subscriptions","contract":"marketing-crm","summary":"Subscribe or unsubscribe","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MarketingSubscription","responds":"MarketingSubscription"},
"submitReview": {"method":"POST","path":"/reviews","contract":"marketing-crm","summary":"Submit a review","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SubmitReviewRequest","responds":"Review"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiAnswerFeedback": {"type":"object","x-ticvai-persistence":"ai.answer_feedback","description":"**What a person thought of an answer** (AIC-062). One label per message per person; it feeds the golden sets and the knowledge-gap list, never an online update (design 3.5).","required":["messageId","rating"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"messageId":{"type":"string","format":"uuid","x-ticvai-references":"ai.message"},"conversationId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.conversation"},"rating":{"type":"string","enum":["helpful","notHelpful"]},"reason":{"type":"string","enum":["wrong","outdated","incomplete","notGrounded","unsafe","other"],"nullable":true},"comment":{"type":"string","nullable":true,"maxLength":1000},"audience":{"type":"string","enum":["staff","guest"],"readOnly":true},"principalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"subjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The guest, where the audience is `guest`."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiConversation": {"type":"object","x-ticvai-persistence":"ai.conversation","required":["id","principalId","module","startedAt"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"module":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},"locale":{"type":"string"},"messageCount":{"type":"integer"},"startedAt":{"type":"string","format":"date-time"},"lastMessageAt":{"type":"string","format":"date-time"}}},
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"AiMessage": {"type":"object","x-ticvai-persistence":"ai.message","required":["id","conversationId","role","content","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"conversationId":{"type":"string","format":"uuid"},"role":{"type":"string","enum":["user","assistant","system"]},"content":{"type":"string"},"sources":{"$ref":"#/components/schemas/AiSourceList"},"confidence":{"type":"number","nullable":true,"description":"8.1.5, 8.3.67. **Nullable on purpose** — a provider that does not report confidence must yield null rather than an invented number, and an interface showing 0.9 because the code defaulted it is worse than showing nothing.\n"},"rationale":{"type":"string","nullable":true,"description":"8.3.68, 8.3.69."},"proposedAction":{"allOf":[{"$ref":"#/components/schemas/ProposedAction"}],"nullable":true,"description":"Present where the answer suggests a change. **A draft, never applied here.**"},"traceId":{"type":"string"},"provider":{"$ref":"#/components/schemas/AiProviderKind"},"model":{"type":"string"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"latencyMs":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"}}},
"AiProviderKind": {"type":"string","enum":["openai","gemini","anthropic","azureOpenai","localLlm","openaiCompatible"],"description":"`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n"},
"AiSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**The sources an answer was grounded in, stored with the answer** (8.3.70). One `jsonb` column on the row that carries it — `ai.message.sources` and `ai.activity.sources` — because the grounding audit reads the list as it was when the answer was given, and a source is never queried on its own.\n","items":{"$ref":"#/components/schemas/AiSource"}},
"AllergenCode": {"type":"string","description":"**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n","enum":["gluten","crustaceans","eggs","fish","peanuts","soybeans","milk","nuts","celery","mustard","sesame","sulphites","lupin","molluscs"]},
"AppAvailability": {"type":"string","description":"**The sold-out or closed signal (decided 28 September, audit R073).** `open` is the normal state. `soldOut` shows WEB-029's sold-out state across the app while browsing still works; `closed` shows the closed state (a weather closure, a private event). Neither refuses a request on its own: it is what the guest is told, and a sale is still refused by availability where it applies. Set with `setMaintenanceMode`.\n","enum":["open","soldOut","closed"],"default":"open"},
"Case": {"x-ticvai-persistence":"marketing.case","x-ticvai-retired-columns":["guest_name","subject","is_sla_breached"],"type":"object","required":["id","caseNumber","subject","status","priority","createdAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7."},"caseNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity. Assigned when the case reaches the server, so a retry with the same `id` keeps its number.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true},"guestName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"**Resolved from `pii.subject` when the case is read, never stored on the case.** A name copied onto a case row is personal data outside the erasable store (ADR-0023), and it had no source anyway — no request carries it. Returned only to callers holding `GUEST_VIEW_PII`, as `searchGuests` does.\n"},"subject":{"type":"string","x-ticvai-column":"title","description":"**The case's one-line title**, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps `subject` because screens bind it.\n"},"kind":{"allOf":[{"$ref":"#/components/schemas/CaseKind"}],"nullable":true,"description":"What the guest said it was about, where the guest raised it."},"channel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"description":"How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`."},"recordedAt":{"type":"string","format":"date-time","description":"Device time the case was raised — the start of the SLA clock."},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the case arrived. Equal to `recordedAt` for a case raised online."},"categoryId":{"type":"string","format":"uuid","nullable":true},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The `ServiceQueue` the case waits in, set by routing (`CaseRoutingRule.queueId`). Null once routed straight to an agent. (decided 29 September, data model for the agreed operations)"},"membershipId":{"type":"string","format":"uuid","nullable":true,"description":"The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. (decided 29 September, coordinator decision DM4, writers pass)"},"status":{"$ref":"#/components/schemas/CaseStatus"},"priority":{"$ref":"#/components/schemas/CasePriority"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"relatedOrderId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"isSlaBreached":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"**Computed when read, never stored.** True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` (or to now, while unresolved), less `slaPausedSeconds`, is past the target that set `slaDueAt`. A stored flag would need a job to flip it at the moment of breach, and no such job is designed; `listCases?breachedSla` filters on the same computation.\n"},"slaPausedSeconds":{"type":"integer","description":"Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock.\n"},"escalationCount":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"CaseKind": {"type":"string","description":"**What the guest says the case is about**, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.\n**`other` only with a note (decided 28 September, audit R222).** A case raised as `other` must carry a non-empty `detail` (`raiseMyCase`), or it is refused with 400; the notes are reviewed quarterly to add the real kinds they reveal.\n","enum":["lostProperty","complaint","question","accessibility","refundRequest","other"]},
"CasePriority": {"type":"string","enum":["low","normal","high","urgent"]},
"CaseStatus": {"type":"string","enum":["open","inProgress","awaitingGuest","escalated","resolved","closed"]},
"ConsentDecision": {"type":"string","enum":["granted","withdrawn","notAsked"]},
"ConsentPurpose": {"type":"string","enum":["marketing","personalisation","profiling","thirdPartySharing","aiProcessing","transactional"]},
"ConsentSource": {"type":"string","enum":["guestApp","website","kiosk","pos","callCentre","import","agentRecorded","cookieBanner","checkout"],"description":"`checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents`, bound to the order and the verified contact. `cookieBanner` (29 September, build; BL-073 §4b): a decision made on the cookie banner or preference centre and moved onto the guest by `claimDeviceConsent`. Kept apart from `website`, a form submission, because the audit trail (2.6.56) has to tell the two apart."},
"ConsentState": {"x-ticvai-persistence":"none — projection over consent_record","type":"object","required":["subjectId","purposes"],"properties":{"subjectId":{"type":"string","format":"uuid"},"purposes":{"type":"array","items":{"type":"object","required":["purpose","decision","requiresRenewal"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"decision":{"$ref":"#/components/schemas/ConsentDecision"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string","nullable":true},"requiresRenewal":{"type":"boolean","description":"True where the notice has been superseded since consent was given."},"decidedAt":{"type":"string","format":"date-time","nullable":true}}}}}},
"Conversation": {"type":"object","x-ticvai-persistence":"marketing.conversation","description":"22.8. **A conversation is not a case.** A case is a ticket measured in hours; a conversation is a live session measured in seconds, with somebody waiting. A conversation may create a case; it is not one.\n","required":["id","channel","state"],"properties":{"id":{"type":"string","format":"uuid"},"telephony":{"type":"object","nullable":true,"description":"BL-083. **`ConversationChannel` included `voice` with nothing behind it** — the model anticipated telephony and stopped at the enum.\n**Not an integration, a binding.** Genesys, Avaya, Amazon Connect, Teams and 3CX all do call control themselves; what the platform needs is the call bound to the guest and the case, so **an agent who answers already knows who is calling and what about.**\n","properties":{"providerCallId":{"type":"string"},"direction":{"type":"string","enum":["inbound","outbound","transferred"]},"fromNumberMasked":{"type":"string","nullable":true,"description":"**Masked, and it is still personal data.** A phone number identifies a person more reliably than a name does.\n"},"recordingRef":{"type":"string","nullable":true,"description":"Held by the provider, referenced here. **Recording consent is jurisdictional and the platform does not assume it** — a reference with no consent record is a recording nobody may play.\n"},"agentState":{"type":"string","enum":["available","onCall","wrapUp","away","offline"],"nullable":true}}},"assistSessionId":{"type":"string","format":"uuid","nullable":true,"description":"BL-094. **`startKioskAssist` recorded a staff member helping a guest and `createCase` recorded a service interaction, and neither referenced the other** — so the traceability 2.13.20 asks for had no link to follow.\n**The link is here rather than on the assist session**, because a case may span several assists and an assist belongs to at most one case.\n"},"channel":{"$ref":"#/components/schemas/ConversationChannel"},"state":{"$ref":"#/components/schemas/ConversationState"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"22.8.3. Resolved from phone, email, membership number or a signed-in session. **A conversation with none of those stays anonymous rather than being guessed at.**\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"assignedPrincipalId":{"type":"string","format":"uuid","nullable":true},"queueId":{"type":"string","format":"uuid","nullable":true},"queuePosition":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onRead","description":"Place among the unclaimed conversations in `queueId`, from the live agent queue (audit R149). Null once claimed."},"estimatedWaitSeconds":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onRead","description":"From the live agent queue — the conversations ahead divided across that queue's agents online now (audit R149). Null once claimed."},"handoverReason":{"type":"string","nullable":true,"enum":["guestRequested","assistantRefused","assistantFailed","outOfScope","negativeSentiment","complexIntent","paymentIssue"]},"handoverSummary":{"type":"string","nullable":true,"description":"**The assistant's own account of what the guest wants**, so an agent opens with context rather than reading a transcript while somebody waits.\n"},"sentiment":{"type":"string","nullable":true,"enum":["positive","neutral","negative","escalating"],"description":"22.8.16. **`escalating` is a routing signal**, not a report line."},"intent":{"type":"string","nullable":true,"description":"22.8.13. What the guest appears to want, used for routing."},"locale":{"type":"string"},"caseId":{"type":"string","format":"uuid","nullable":true,"description":"22.8.12. Where the conversation raised one."},"messages":{"type":"array","items":{"$ref":"#/components/schemas/ConversationMessage"}},"firstResponseSeconds":{"type":"integer","nullable":true,"readOnly":true},"startedAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true},"outcome":{"type":"string","nullable":true,"enum":["resolved","caseRaised","abandonedByGuest","timedOut","spam"]}}},
"ConversationChannel": {"type":"string","enum":["webChat","inAppChat","whatsapp","sms","email","kiosk","voice"]},
"ConversationMessage": {"type":"object","x-ticvai-persistence":"marketing.conversation_message + marketing.conversation_message_attachment","required":["id","sender","body","sentAt"],"properties":{"id":{"type":"string","format":"uuid"},"sender":{"type":"string","enum":["guest","agent","assistant","system"],"description":"**Resolved, never declared.** The assistant is labelled as one — a guest talking to a bot that presents as a person is a complaint waiting for the moment they find out.\n"},"senderPrincipalId":{"type":"string","format":"uuid","nullable":true},"body":{"type":"string"},"attachments":{"type":"array","items":{"type":"object","properties":{"assetId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["image","video","document","ticket","qr","paymentLink"]}}}},"aiInteractionId":{"type":"string","format":"uuid","nullable":true,"description":"Where the assistant sent it. **Links the message to its tokens and cost**, so a conversation's spend is attributable (CF-14).\n"},"sentAt":{"type":"string","format":"date-time"},"readAt":{"type":"string","format":"date-time","nullable":true}}},
"ConversationState": {"type":"string","description":"**`withAssistant` and `queued` are different, and the second has a person waiting.** Merging them makes the service level unmeasurable, because time with a bot is not time in a queue.\n","enum":["withAssistant","queued","withAgent","waitingOnGuest","resolved","abandoned","timedOut"]},
"CreateCaseRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","subject","description","channel","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"subject":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":10000},"categoryId":{"type":"string","format":"uuid"},"membershipId":{"type":"string","format":"uuid","nullable":true,"description":"The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. Must belong to `subjectId` when both are given (422). (decided 29 September, coordinator decision DM4, writers pass)"},"priority":{"allOf":[{"$ref":"#/components/schemas/CasePriority"}],"default":"normal"},"kind":{"$ref":"#/components/schemas/CaseKind"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"venueId":{"type":"string","format":"uuid"},"relatedOrderId":{"type":"string"},"attachmentRefs":{"type":"array","description":"Stored on the opening `CaseMessage`, not on the case.","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time","description":"Device time the case was raised. The server stamps `Case.syncedAt` on arrival."}}},
"DeliveryLocationKind": {"type":"string","description":"4.6.26. One concept, because a runner needs one instruction.","enum":["table","seat","cabana","sunbed","poolside","box","suite","lawn","collectionPoint","namedLocation"]},
"GuestDevice": {"type":"object","x-ticvai-persistence":"marketing.guest_device","required":["id","subjectId","platform","status","registeredAt"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"platform":{"type":"string","enum":["ios","android","web"]},"tokenFingerprint":{"type":"string","description":"Hash of the token, not the token. The token itself is write-only — returning it would put a push credential in every response a support agent can read.\n"},"tokenRef":{"type":"string","writeOnly":true,"description":"**A vault reference to the push token**, written by the server from `registerGuestDevice.token` — the same pattern as `PaymentProvider.credentialRef`. Never the token and never returned; the sender resolves it at send time. Without it a registered device could not be sent to.\n"},"appVersion":{"type":"string","nullable":true},"osVersion":{"type":"string","nullable":true},"deviceModel":{"type":"string","nullable":true},"locale":{"type":"string","nullable":true},"status":{"type":"string","enum":["active","revoked","failed"]},"failureCount":{"type":"integer","description":"Consecutive delivery failures. Past the threshold the device is marked failed and stops being targeted — a dead token retried forever is wasted quota and a misleading delivery rate.\n"},"registeredAt":{"type":"string","format":"date-time"},"lastSeenAt":{"type":"string","format":"date-time","nullable":true},"revokedAt":{"type":"string","format":"date-time","nullable":true}}},
"GuestMenu": {"type":"object","x-ticvai-persistence":"none — projection over menu, item and availability","required":["outletId","menuId","name","inForceUntil","sections"],"properties":{"outletId":{"type":"string","format":"uuid"},"menuId":{"type":"string","format":"uuid"},"name":{"type":"string"},"inForceUntil":{"type":"string","format":"date-time","nullable":true,"description":"When this menu stops applying. The client shows it, because a guest browsing breakfast at 10:55 should know.\n"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer"},"sections":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"sortOrder":{"type":"integer"},"items":{"type":"array","items":{"type":"object","required":["menuItemId","name","price","isAvailable","allergens"],"properties":{"menuItemId":{"type":"string","format":"uuid"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"imageAssetRef":{"type":"string","nullable":true},"isAvailable":{"type":"boolean","description":"Marked, not removed. A guest who saw a dish yesterday and cannot find it today assumes the app is broken; \"sold out\" is an answer.\n"},"unavailableReason":{"type":"string","nullable":true},"allergens":{"type":"array","description":"Always present. Not a field a tenant may choose to omit.","items":{"$ref":"#/components/schemas/AllergenCode"}},"preparationMinutes":{"type":"integer","nullable":true},"modifierGroups":{"type":"array","items":{"$ref":"#/components/schemas/ModifierGroup"}}}}}}}}}},
"GuestNotification": {"type":"object","description":"One in-app message as the guest sees it. A view of `marketing.message_dispatch`, channel `inApp`.","required":["id","title","queuedAt","read"],"properties":{"id":{"type":"string"},"kind":{"type":"string","enum":["queueCall","orderReady","bookingChange","venueAlert","offer","other"]},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedText"},"venueId":{"type":"string","format":"uuid","nullable":true},"deepLink":{"type":"string","nullable":true,"description":"Where tapping the notification leads in the app (an order, a queue ticket, a booking)."},"queuedAt":{"type":"string","format":"date-time"},"read":{"type":"boolean"}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"LocationSession": {"type":"object","x-ticvai-persistence":"fnb.location_session","required":["id","locationId","kind","label","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/DeliveryLocationKind"},"label":{"type":"string"},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"The outlet serving this location. Where several serve it, the guest chooses and this is set on the first order.\n"},"visitId":{"type":"string","format":"uuid","nullable":true,"description":"The table visit this session orders onto, where the location is a table. Absent for a cabana or a seat, which have no visit concept — the order stands alone.\n"},"joinedExistingVisit":{"type":"boolean"},"subjectId":{"type":"string","format":"uuid"},"expiresAt":{"type":"string","format":"date-time","description":"Sessions expire so a guest who leaves cannot order to a lounger now occupied by someone else.\n"}}},
"MarketingSubscription": {"type":"object","x-ticvai-persistence":"marketing.subscription","x-ticvai-retired-columns":["guest_id","subscribed"],"description":"**Drafted 4 September.** What a guest asked to receive. **Deliberately separate from `marketing.consent`** - consent is what the law allows, a subscription is what the person wants, and a system that stores one and reports the other is the reason unsubscribe links stop working.","required":["id","subjectId","channel","listName","isSubscribed"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","readOnly":true,"description":"The guest — from the guest session, or from `unsubscribeToken` when there is no session."},"channel":{"type":"string","enum":["email","sms","push"]},"listName":{"type":"string"},"isSubscribed":{"type":"boolean"},"source":{"type":"string","description":"Where the opt-in happened, because a regulator asks."},"unsubscribeToken":{"writeOnly":true,"type":"string","description":"**Unsubscribe must work without a login.** The link in a message carries the token and `setMarketingSubscription` accepts it in place of a session. **Write-only: never returned**, so a `MARKETING_VIEW` holder reading subscriptions cannot act as the guest."},"updatedAt":{"readOnly":true,"type":"string","format":"date-time"}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MinimumAppVersion": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n","properties":{"ios":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"},"android":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"}}},
"ModifierGroup": {"x-ticvai-persistence":"fnb.modifier_group + fnb.modifier_option","type":"object","description":"**An F&B modifier is a choice added to a dish at the moment of ordering** — *no onions*, *extra cheese*, *cooked medium*. **It is not an Attribute**, the axis that generates catalogue variants (naming-and-style §3 lists *Modifier* as a banned synonym for that), and the two must not be merged: a variant is a different product with its own stock, a modifier is an instruction on a line with at most a price delta.\n","required":["id","code","name","minSelections","maxSelections","options"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"minSelections":{"type":"integer","minimum":0,"description":"Greater than zero makes the group required."},"maxSelections":{"type":"integer","minimum":1},"options":{"type":"array","minItems":1,"items":{"type":"object","required":["id","name","priceDelta"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"priceDelta":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isDefault":{"type":"boolean"},"isAvailable":{"type":"boolean"},"allergens":{"type":"array","description":"What choosing this option adds to the dish. `attachModifierGroup` refuses a group that adds one the item does not declare, and `verifyAllergens` reports it as `via` `modifier`.","items":{"$ref":"#/components/schemas/AllergenCode"}}}}},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"ModuleKey": {"type":"string","enum":["ticketsAndBooking","membership","events","attractions","virtualQueue","diningAndFnb","shop","parking","gamification","photoGallery","wallet","loyalty","lostAndFound","map","visitPlanner"],"description":"`visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown."},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"RecordConsentRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["purpose","decision","noticeVersion","source","recordedAt"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"decision":{"$ref":"#/components/schemas/ConsentDecision"},"channels":{"type":"array","description":"Omit to apply to every channel the purpose covers.","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string"},"source":{"$ref":"#/components/schemas/ConsentSource"},"recordedAt":{"type":"string","format":"date-time"}}},
"Review": {"x-ticvai-persistence":"marketing.review","allOf":[{"$ref":"#/components/schemas/SubmitReviewRequest"},{"type":"object","required":["status"],"properties":{"status":{"type":"string","enum":["pendingModeration","published","hidden","rejected"]},"response":{"type":"string","nullable":true},"responseIsPublic":{"type":"boolean"},"respondedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"openedCaseId":{"type":"string","nullable":true,"description":"Case raised automatically where the rating fell below the venue's threshold. Feedback that goes nowhere is worse than no feedback mechanism.\n"}}}]},
"SubmitReviewRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","rating","venueId","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"relatedOrderId":{"type":"string"},"rating":{"type":"integer","minimum":1,"maximum":5},"body":{"type":"string","maxLength":5000},"aspects":{"type":"array","description":"Aspect chips — the closed set the description always named.","uniqueItems":true,"items":{"type":"string","enum":["exhibitions","staff","cleanliness","food","value"]}},"recordedAt":{"type":"string","format":"date-time"}}},
"Suggestion": {"type":"object","x-ticvai-persistence":"ai.suggestion","description":"One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n","required":["id","kind","basis","maturity","producedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SuggestionKind"},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"scopePath":{"type":"string"},"subjectRef":{"type":"string","nullable":true,"description":"What it is about — a product, an outlet, an item, a party."},"value":{"type":"object","additionalProperties":true,"description":"The suggestion itself. Shape depends on `kind`."},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1,"description":"**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"},"explanation":{"type":"string","description":"**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"},"inputs":{"type":"object","additionalProperties":true,"description":"What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"},"producerRef":{"type":"string","description":"The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"SuggestionKind": {"type":"string","description":"What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n","enum":["price","replenishment","requisition","demandForecast","prepPlan","menuEngineering","staffing","slaTarget","waitTime","upsell","segmentation","anomaly","scenario","sendTime","wasteRisk","queueBalancing","itinerary"]},
"TenantAppStatus": {"x-ticvai-persistence":"none — computed","type":"object","description":"Computed on read. The published fields come from the current `ConfigVersion`, the maintenance fields from the tenant's `tenant_config` row (`setMaintenanceMode`), and the draft fields from the working draft. **Fields marked staff only are left out of a response to a caller without a staff session** (`getTenantAppStatus`).\n","required":["tenantId","isPublished","isInMaintenance"],"properties":{"tenantId":{"type":"string","format":"uuid"},"isPublished":{"type":"boolean","x-ticvai-derived":"onRead","description":"True once any version has been published."},"publishedVersion":{"type":"string","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"draftVersion":{"type":"string","description":"Staff only."},"hasUnpublishedChanges":{"type":"boolean","x-ticvai-derived":"onRead","description":"Staff only. The working draft differs from the current version's `snapshot`."},"activeModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isEnabled` true."},"licensedModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isLicensed` true."},"activePageCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. Content pages that are `published` and enabled."},"isInMaintenance":{"type":"boolean"},"maintenanceMessage":{"$ref":"#/components/schemas/LocalisedText"},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"$ref":"#/components/schemas/MinimumAppVersion"},"contact":{"$ref":"#/components/schemas/VenueContact"},"availability":{"$ref":"#/components/schemas/AppAvailability"},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"What the sold-out or closed screen says (WEB-029). Null shows the default wording."},"venues":{"type":"array","maxItems":200,"x-ticvai-derived":"onRead","description":"**Public: the venues a guest can pick** (decided 28 September, audit R267; schema named 29 September, readiness close-out, our build plan). The source of the venue picker on WEB-001 and GST-001, returned with or without a session. **Published only**: a venue is listed when its scope node is active (`tenancy.OrgUnit.isActive`) and it is in the tenant's current published `ConfigVersion`; a venue added or reactivated since the last publish appears after the next publish, and a draft never reaches a guest. Ordered by `name`. Empty when nothing is published.\n","items":{"type":"object","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid","description":"**The venue's scope node** (`tenancy.OrgUnit.id`, level venue): what every guest screen that declares `venueId` `from: session` reads once the guest picks it."},"name":{"type":"string","maxLength":200,"description":"The venue's name (`tenancy.OrgUnit.name`)."},"city":{"type":"string","maxLength":120,"nullable":true,"description":"Shown under the name so two venues with similar names can be told apart."},"openingHoursToday":{"type":"object","nullable":true,"description":"Today's opening hours in the venue's time zone, from `tenancy.VenueSettings` opening hours. Null when the venue is closed today or has none set.","properties":{"opens":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"},"closes":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"}}}}}},"whatsNew":{"type":"array","maxItems":10,"x-ticvai-derived":"onRead","description":"**Public: the guest \"what's new\"** (decided 29 September, rev 3 GAP-B2). Newest first, at most 10, from `platform-ops.Release.guestReleaseNotes` of the releases the tenant's cell has received; a release with no guest notes is skipped. Returned with or without a staff session.\n","items":{"type":"object","required":["version","publishedAt","notes"],"properties":{"version":{"type":"string","description":"The release version."},"publishedAt":{"type":"string","format":"date-time","description":"When the release reached the tenant's cell."},"notes":{"$ref":"#/components/schemas/LocalisedText"}}}},"recentChanges":{"type":"array","description":"Staff only. Names the principal behind each change, so it never reaches a public response.","items":{"type":"object","properties":{"area":{"type":"string"},"description":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"}}}}}},
"VenueContact": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n","properties":{"phone":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true},"whatsapp":{"type":"string","nullable":true},"address":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Prose, as the guest reads it. The bookable hours are the catalogue's."}}},
"Wishlist": {"type":"object","required":["subjectId","items"],"x-ticvai-persistence":"none — wrapper. The items are the table, keyed by subject","properties":{"subjectId":{"type":"string","format":"uuid"},"items":{"type":"array","x-ticvai-persistence":"marketing.wishlist_item","items":{"type":"object","required":["id","variantId","addedAt","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"productName":{"type":"string"},"performanceId":{"type":"string","format":"uuid","nullable":true},"performanceStartsAt":{"type":"string","format":"date-time","nullable":true},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money","description":"The variant's current list price when the wishlist is read. Stored as `list_price` (naming-and-style 5.1 bans a bare `price` column); the wire keeps `price`."},"imageAssetRef":{"type":"string","nullable":true},"isAvailable":{"type":"boolean","description":"False where the product has been withdrawn or the performance has passed. Returned rather than dropped — a guest who saved something and finds it silently gone assumes the feature is broken.\n"},"unavailableReason":{"type":"string","nullable":true},"note":{"type":"string","nullable":true},"addedAt":{"type":"string","format":"date-time"}}}}}}
}
```
