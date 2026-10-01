# WS61 — Ticket Media   Credential Management board 3

**10 screens · 16 operations · 21 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `ACCESS_POINT_CONFIGURE, AUDIT_VIEW, ORDER_EXCHANGE, ORDER_REPRINT, REPORT_VIEW_VENUE, SCOPE_VIEW, TICKET_LOOKUP`. A control nobody can use must say so,
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
| `BO-354` | Credential Operations Command Center | B–D | 2 | 28 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-355` | Virtual Ticket & Credential 360° Workspace | B–D | 0 | 22 | 6 | 0 | 3 | 0 | — | notStarted (generated) |
| `BO-356` | Credential Generation & Issuance Monitor | B–D | 10 | 28 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-357` | Credential Delivery & Distribution Operations | B–D | 5 | 20 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-358` | Media Binding, Activation & Assignment Operations | B–D | 0 | 18 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-359` | Credential Replacement, Reissue, Revocation & Recovery | B–D | 11 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-360` | Failed Generation, Delivery & Credential Exception Management | B–D | 4 | 22 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-361` | Credential Usage & Cross-Media Traceability | B–D | 11 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-362` | Credential Security, Audit & Operational Evidence | B–D | 0 | 2 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-363` | Ticket Media Analytics & AI Operations Intelligence | B–D | 2 | 42 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-362 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-354` Credential Operations Command Center

**Provide Operations, Ticketing, Customer Service and Technical teams with a real-time command center covering all issued credential media. This is the operational starting point for Area 15.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each record should show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/credential-operations-command-center-bo-354` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search credential operations | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by brand, venue, event, product, date, media and 5 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Brand | text field | — | — | `listCredential` ?brand |
| Venue | text field | — | — | `listCredential` ?venue |
| Date | text field | — | — | `listCredential` ?date |
| Media | text field | — | — | `listCredential` ?media |
| Status | text field | — | — | `listCredential` ?status |
| Channel | text field | — | — | `listCredential` ?channel |
| Customer | text field | — | — | `listCredential` ?customer |
| Event | text field | — | — | `listCredential` ?event |
| Product | text field | — | — | `listCredential` ?product |
| Provider | text field | — | — | `listCredential` ?provider |
| Exception | text field | — | — | `listCredential` ?exception |

#### Outputs: what the screen shows and produces

**Shown**

**Virtual Tickets Issued** (metric tile)

**Credentials Generated** (metric tile)

**Active Credentials** (metric tile)

**Pending Generation** (metric tile)

**Pending Delivery** (metric tile)

**Pending Binding** (metric tile)

**Pending Activation** (metric tile)

**Suspended** (metric tile)

**Revoked** (metric tile)

**Expired** (metric tile)

**Failed Generation** (metric tile)

**Failed Delivery** (metric tile)

**Synchronization Exceptions** (metric tile)

**Multi-Media Virtual Tickets** (metric tile)

**Virtual Tickets Without Active Media** (metric tile)

**Every credential operations** (data table, from `listCredential`)

| Shows | Format | Notes |
|---|---|---|
| Virtual ticket | text | Virtual Ticket ID |
| Credential | text | Credential ID |
| Media type | text | Media Type |
| Customer participant | text | Customer / Participant |
| Product | text | Product |
| Event | text | Event |
| Credential status | chip: Pending generation, Generated, Pending activation, Active, Suspended, Revoked… | Credential status |
| Delivery status | chip: Not required, Pending, Sent, Delivered, Opened downloaded, Completed… | Delivery status (15.3.4) |
| Activation status | chip: Pending, Scheduled, Active, Not required | Activation status |
| Binding status | chip: Pending, Bound, Unbound, Failed | Binding status |
| Provider | text | Provider |
| Last activity | 1 Oct 2026, 14:30 | Last Activity |
| Exception | text | Exception |
| Owner | text | Owner |

**The selected credential operations** (detail panel): The pack groups this record's detail under its own headings: “Display credentials by”, “Provide indicators such as”.

| Shows | Format | Notes |
|---|---|---|
| Virtual ticket | text | Virtual Ticket ID |
| Credential | text | Credential ID |
| Media type | text | Media Type |
| Customer participant | text | Customer / Participant |
| Product | text | Product |
| Event | text | Event |
| Credential status | chip: Pending generation, Generated, Pending activation, Active, Suspended, Revoked… | Credential status |
| Delivery status | chip: Not required, Pending, Sent, Delivered, Opened downloaded, Completed… | Delivery status (15.3.4) |
| Activation status | chip: Pending, Scheduled, Active, Not required | Activation status |
| Binding status | chip: Pending, Bound, Unbound, Failed | Binding status |
| Provider | text | Provider |
| Last activity | 1 Oct 2026, 14:30 | Last Activity |
| Exception | text | Exception |
| Owner | text | Owner |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Open Virtual Ticket, Generate Credential, Resend, Activate, Suspend Media, Replace, Revoke, Diagnose, View History. Each needs attaching to the control it gates, or the screen needs the control.

**Data it reads**: `listCredential` (onLoad, Credential Operations Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-355` Virtual Ticket & Credential 360° Workspace: *Works in Virtual Ticket & Credential 360° Workspace*; calls `listCredential`
- → `BO-356` Credential Generation & Issuance Monitor: *Works in Credential Generation & Issuance Monitor*; calls `listCredential`
- → `BO-358` Media Binding, Activation & Assignment Operations: *Works in Media Binding, Activation & Assignment Operations*; calls `listCredential`
- → `BO-360` Failed Generation, Delivery & Credential Exception Management: *Works in Failed Generation, Delivery & Credential Exception Management*; calls `listCredential`
- → `BO-361` Credential Usage & Cross-Media Traceability: *Works in Credential Usage & Cross-Media Traceability*; calls `listCredential`
- → `BO-362` Credential Security, Audit & Operational Evidence: *Works in Credential Security, Audit & Operational Evidence*; calls `listCredential`
- → `BO-363` Ticket Media Analytics & AI Operations Intelligence: *Works in Ticket Media Analytics & AI Operations Intelligence*; calls `listCredential`
- → `BO-357` Credential Delivery & Distribution Operations: *Works in Credential Delivery & Distribution Operations*; carries `credentialId`; calls `listCredential`
- → `BO-359` Credential Replacement, Reissue, Revocation & Recovery: *Works in Credential Replacement, Reissue, Revocation & Recovery*; carries `credentialId`; calls `listCredential`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential operations list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCredential` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-354` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-354`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 1: Opens Credential Operations Command Center → Provide Operations, Ticketing, Customer Service and Technical teams with a real-time command center covering all issued credential media. This is the operational starting point for Area 15.
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F170 branch at step 1 (expected): when Nothing has been set up on Credential Operations Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F170 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-354?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-355`, `BO-356`, `BO-358`, `BO-360`, `BO-361`, `BO-362`, `BO-363`, `BO-357`, `BO-359`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-355` Virtual Ticket & Credential 360° Workspace

**Provide a complete operational view of one Virtual Ticket and every media credential currently or historically associated with it. This is one of the most important operational screens.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display; Identify) and a per-row directory (§For each media show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/virtual-ticket-credential-360-workspace-bo-355` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Virtual Ticket ID** (metric tile)

**Ticket Holder** (metric tile)

**Participant** (metric tile)

**Product** (metric tile)

**Event** (metric tile)

**Performance** (metric tile)

**Venue** (metric tile)

**Seat** (metric tile)

**Order** (metric tile)

**Ticket Status** (metric tile)

**Usage Status** (metric tile)

**Validity** (metric tile)

**Entitlements** (metric tile)

**Primary** (metric tile)

**Secondary** (metric tile)

**Fallback** (metric tile)

**Temporary** (metric tile)

**Revoked historical media** (metric tile)

**Every virtual ticket credential** (data table, from `setVirtualTicketCredential`)

| Shows | Format | Notes |
|---|---|---|
| Binding | text | Binding ID |
| Media type | text | Media type |
| Provider | text | Provider |
| Issued | 1 Oct 2026, 14:30 | Issued |
| Delivered | 1 Oct 2026, 14:30 | Delivered |
| Activated | 1 Oct 2026, 14:30 | Activated |
| Valid from/to | text | not in the schema: `Valid From/To` |
| Last update | 1 Oct 2026, 14:30 | Last update |
| Last presentation/use | text | not in the schema: `Last presentation/use` |
| Device reference where appropriate | text | Device/reference where appropriate |
| Status | chip: Pending, Active, Suspended, Revoked, Expired | Medium status |

**The selected virtual ticket credential** (detail panel): The pack groups this record's detail under its own headings: “Credential Wallet”, “Media Status”, “Dynamic QR Active”, “Apple Wallet Active”, “Old RFID RF-88410”, “Provide one chronological timeline”.

| Shows | Format | Notes |
|---|---|---|
| Binding | text | Binding ID |
| Media type | text | Media type |
| Provider | text | Provider |
| Issued | 1 Oct 2026, 14:30 | Issued |
| Delivered | 1 Oct 2026, 14:30 | Delivered |
| Activated | 1 Oct 2026, 14:30 | Activated |
| Valid from/to | text | not in the schema: `Valid From/To` |
| Last update | 1 Oct 2026, 14:30 | Last update |
| Last presentation/use | text | not in the schema: `Last presentation/use` |
| Device reference where appropriate | text | Device/reference where appropriate |
| Status | chip: Pending, Active, Suspended, Revoked, Expired | Medium status |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Generate Additional Media, Bind RFID, Add Wallet Pass, Initiate Face Enrollment, Replace Media, Suspend, Revoke, Resend, Refresh, Diagnose. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-354` Credential Operations Command Center: *Returns to the board's landing screen*; calls `setVirtualTicketCredential`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The virtual ticket credential list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the virtual ticket credential untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No virtual ticket credential yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the virtual ticket credential are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setVirtualTicketCredential` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A purchased ticket can be transferred to another guest (e.g. a friend); the system keeps the original purchaser and full transfer history. *(client request · MoM 7 Sep 2026, 4.9 Ownership and transfer · DI-669)*
- A ticket is always one virtual record; QR, RFID, NFC, face and future credentials (e.g. hotel room key, city transit card) are interchangeable media linked to it. Screens should show one ticket with its linked media, not separate tickets per medium. *(agreed · MoM 2 Sep 2026, 5. Key Decisions & Agreements · DI-652)*
- Resale keeps the original virtual ticket ID; only owner name and media (QR) change. An ownership change log shows the history against one ID (e.g. VT0010: Qossai > Allam > Chinmay). *(agreed · MoM 1 Sep 2026, 4.14 Decision (ticket ID on resale) · DI-620)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-355` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-355`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 2: Works in Virtual Ticket & Credential 360° Workspace → Provide a complete operational view of one Virtual Ticket and every media credential currently or historically associated with it. This is one of the most important operational screens.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-355?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-354`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-356` Credential Generation & Issuance Monitor

**Manage and monitor generation of credential instances from approved Board 2 media templates.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show; Display) and no metric row |
| Offline | online only |
| Opens with | `exceptionId` (navigation) |
| Route | `/access-venue/credential-generation-issuance-monitor-bo-356` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listCredentialGenerationIssuance` ?status |
| Trigger | text field | — | — | `listCredentialGenerationIssuance` ?trigger |
| Event | text field | — | — | `listCredentialGenerationIssuance` ?event |
| Venue | text field | — | — | `listCredentialGenerationIssuance` ?venue |

**Sent by *Manual Retry*** (`retryCredentialGeneration`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scope `scope` | segmented control | required | — | Selected · All eligible | — | — | `retryCredentialGeneration` body |
| Requests `requestIds` | list of values (chips) | optional | — | at most 500 | — | The failed generation requests (`CredentialGenerationIssuanceMonitorView.requestId`); required for selected | `retryCredentialGeneration` body |

**Sent by *Escalate*** (`resolveCredentialException`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | select | required | — | Retry · Regenerate · Use fallback · Escalate · Assign owner · Open technical case | — | — | `resolveCredentialException` body |
| Owner `ownerId` | text field | optional | — | — | — | Required for assignOwner and escalate | `resolveCredentialException` body |
| Fallback media kind `fallbackMediaKind` | radio group | optional | — | QR · Pdf · Printed ticket · RFID card · Wristband | — | Required for useFallback | `resolveCredentialException` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `resolveCredentialException` body |

**Sent by *Save retry policy*** (`setCredentialIssuanceRetryPolicy`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Automatic retry `automaticRetry` | toggle | required | on | — | — | — | `setCredentialIssuanceRetryPolicy` body |
| Max attempts `maxAttempts` | stepper or slider | optional | 3 | min 1; max 10 | — | — | `setCredentialIssuanceRetryPolicy` body |
| Backoff minutes `backoffMinutes` | number field (minutes) | optional | 5 | min 1; max 240 | — | Wait before the first retry; doubles on each attempt | `setCredentialIssuanceRetryPolicy` body |
| Escalate after attempts `escalateAfterAttempts` | stepper or slider | optional | 3 | min 1; max 10 | — | After this many failures the request becomes a credential exception with an owner; not more than maxAttempts | `setCredentialIssuanceRetryPolicy` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every credential generation issuance** (data table, from `listCredentialGenerationIssuance`)

| Shows | Format | Notes |
|---|---|---|
| → bound → ready → delivered | text | not in the schema: `→ Bound → Ready → Delivered` |
| Request | text | Request ID |
| Virtual ticket | text | Virtual Ticket |
| Media | text | Media |
| Template | text | Template |
| Template version | text | Template Version |
| Product | text | Product |
| Customer | text | Customer |
| Trigger | text | not in the schema: `Trigger` |
| Provider | text | Provider |
| Requested at | 1 Oct 2026, 14:30 | Requested At |
| Generated at | 1 Oct 2026, 14:30 | Generated At |
| Status | chip: Requested, Queued, Template resolved, Data mapped, Credential generated, Bound… | Generation stage |
| Error | text | Error |

**The selected credential generation issuance** (detail panel): The pack groups this record's detail under its own headings: “Generation Sources”, “Template Resolution”, “Bulk Generation”, “Failures may include”.

| Shows | Format | Notes |
|---|---|---|
| → bound → ready → delivered | text | not in the schema: `→ Bound → Ready → Delivered` |
| Request | text | Request ID |
| Virtual ticket | text | Virtual Ticket |
| Media | text | Media |
| Template | text | Template |
| Template version | text | Template Version |
| Product | text | Product |
| Customer | text | Customer |
| Trigger | text | not in the schema: `Trigger` |
| Provider | text | Provider |
| Requested at | 1 Oct 2026, 14:30 | Requested At |
| Generated at | 1 Oct 2026, 14:30 | Generated At |
| Status | chip: Requested, Queued, Template resolved, Data mapped, Credential generated, Bound… | Generation stage |
| Error | text | Error |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Automatic Retry (primary button) | navigation or local | — | — | — | — |
| Manual Retry (secondary button) | `retryCredentialGeneration` POST `/credential-generation-issuance/retry` | CredentialGenerationRetryInput | CredentialGenerationRetryResult | 422 scope selected with no requestIds | — |
| Retry Selected (secondary button) | `retryCredentialGeneration` POST `/credential-generation-issuance/retry` | CredentialGenerationRetryInput | CredentialGenerationRetryResult | 422 scope selected with no requestIds | — |
| Retry All Eligible (secondary button) | `retryCredentialGeneration` POST `/credential-generation-issuance/retry` | CredentialGenerationRetryInput | CredentialGenerationRetryResult | 422 scope selected with no requestIds | — |
| Escalate (secondary button) | `resolveCredentialException` POST `/credential-exceptions/{exceptionId}/resolve` | CredentialExceptionActionInput | FailedGenerationDeliveryCredentialExceptionManagemenView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The exception is already resolved; 422 ownerId missing for assignOwner or escalate, or fallbackMediaKind … | — |
| Save retry policy (primary button) | `setCredentialIssuanceRetryPolicy` PUT `/credential-issuance-retry-policy` | CredentialIssuanceRetryPolicyInput | CredentialIssuanceRetryPolicyView | 422 escalateAfterAttempts greater than maxAttempts | — |

**Data it reads**: `listCredentialGenerationIssuance` (onLoad, Credential Generation & Issuance Monitor); `getCredentialIssuanceRetryPolicy` (onLoad, The retry policy the monitor applies)

**Where the user goes next**

- → `BO-354` Credential Operations Command Center: *Returns to the board's landing screen*; calls `listCredentialGenerationIssuance`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential generation issuance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential generation issuance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential generation issuance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential generation issuance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The exception is already resolved; 422 escalateAfterAttempts greater than maxAttempts; 422 ownerId missing for assignOwner or escalate, or fallbackMediaKind missing for useFallback; 422 scope selected with no requestIds |

#### Permissions

- `listCredentialGenerationIssuance` → `SCOPE_VIEW` (read) · staff
- `getCredentialIssuanceRetryPolicy` → `SCOPE_VIEW` (read) · staff
- `setCredentialIssuanceRetryPolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `retryCredentialGeneration` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `resolveCredentialException` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-356` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-356`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 4: Works in Credential Generation & Issuance Monitor → Manage and monitor generation of credential instances from approved Board 2 media templates.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-356?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Automatic Retry, Manual Retry, Retry Selected, Retry All Eligible, Escalate, Save retry policy.
- [ ] Every transition is wired: `BO-354`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-357` Credential Delivery & Distribution Operations

**Manage how generated ticket media are delivered or made available to customers, participants and operational staff.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_REPRINT`, `SCOPE_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `credentialId` (navigation) |
| Route | `/access-venue/credential-delivery-distribution-operations-bo-357` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | text field | — | — | `listCredentialDeliveryDistribution` ?channel |
| Status | text field | — | — | `listCredentialDeliveryDistribution` ?status |

**Sent by *Send credential*** (`deliverCredential`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated delivery attempt id | `deliverCredential` body |
| Channel `channel` | select | required | — | Email · SMS link · Whatsapp · Download · Apple wallet · Google wallet · POS · API · Physical collection | — | — | `deliverCredential` body |
| Recipient `recipient` | text area | optional | — | max length 320 | — | Email address, phone number or collection point; empty sends to the recipient already on the credential | `deliverCredential` body |
| Recipient role `recipientRole` | select | optional | Ticket holder | Purchaser · Ticket holder · Participant · Guardian · Group leader · Authorized recipient | — | — | `deliverCredential` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `deliverCredential` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every credential delivery distribution** (data table, from `listCredentialDeliveryDistribution`)

| Shows | Format | Notes |
|---|---|---|
| Virtual ticket | text | Virtual Ticket |
| Media | text | Media |
| Recipient | text | Recipient |
| Channel | chip: Email, SMS link, Whatsapp, B2C account, Mobile app, Download… | Delivery channel |
| Destination | text | Destination, masked |
| Sent at | 1 Oct 2026, 14:30 | Sent At |
| Delivered at | 1 Oct 2026, 14:30 | Delivered At |
| Opened downloaded | 1 Oct 2026, 14:30 | When opened or downloaded |
| Attempt | 1,234 | Attempt |
| Status | chip: Not required, Pending, Sent, Delivered, Opened downloaded, Completed… | Delivery status |

**The selected credential delivery distribution** (detail panel): The pack groups this record's detail under its own headings: “Alternative states”, “Where allowed, support”.

| Shows | Format | Notes |
|---|---|---|
| Virtual ticket | text | Virtual Ticket |
| Media | text | Media |
| Recipient | text | Recipient |
| Channel | chip: Email, SMS link, Whatsapp, B2C account, Mobile app, Download… | Delivery channel |
| Destination | text | Destination, masked |
| Sent at | 1 Oct 2026, 14:30 | Sent At |
| Delivered at | 1 Oct 2026, 14:30 | Delivered At |
| Opened downloaded | 1 Oct 2026, 14:30 | When opened or downloaded |
| Attempt | 1,234 | Attempt |
| Status | chip: Not required, Pending, Sent, Delivered, Opened downloaded, Completed… | Delivery status |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| SMS Link (primary button) | navigation or local | — | — | — | — |
| WhatsApp integration (secondary button) | navigation or local | — | — | — | — |
| Download (secondary button) | navigation or local | — | — | — | — |
| Apple Wallet (secondary button) | navigation or local | — | — | — | — |
| Google Wallet (secondary button) | navigation or local | — | — | — | — |
| POS (secondary button) | navigation or local | — | — | — | — |
| API (secondary button) | navigation or local | — | — | — | — |
| Physical Collection (secondary button) | navigation or local | — | — | — | — |
| Send credential (primary button) | `deliverCredential` POST `/credentials/{credentialId}/deliveries` | CredentialDeliveryInput | CredentialDeliveryDistributionOperationsView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The credential is revoked or expired; 422 The channel does not suit the media type (a wallet pass for an RFID … | gated `ORDER_REPRINT` |

**Data it reads**: `listCredentialDeliveryDistribution` (onLoad, Credential Delivery & Distribution Operations)

**Where the user goes next**

- → `BO-354` Credential Operations Command Center: *Returns to the board's landing screen*; calls `listCredentialDeliveryDistribution`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential delivery distribution list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential delivery distribution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential delivery distribution yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential delivery distribution are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission: reading needs SCOPE_VIEW; **sending a credential needs ORDER_REPRINT** (K1, 29 September), and the Send action is hidden without it. Never an empty table. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The credential is revoked or expired; 422 The channel does not suit the media type (a wallet pass for an RFID card) |

#### Permissions

- `listCredentialDeliveryDistribution` → `SCOPE_VIEW` (read) · staff
- `deliverCredential` → `ORDER_REPRINT` (operate) · staff

**A refused user sees:** Names the missing permission: reading needs SCOPE_VIEW; **sending a credential needs ORDER_REPRINT** (K1, 29 September), and the Send action is hidden without it. Never an empty table.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: deferred seat assignment — sale confirmed at purchase as section + quantity; seats allocated internally; closer to the event ops/admin trigger a bulk e-mail issuing QR tickets with final seats. Immediate seat assignment remains for venues that need it. *(agreed · MoM 21 Aug 2026, 4.7 Deferred Seat Assignment Model; 5. Key Decisions · DI-423)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-357` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-357`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 6: Works in Credential Delivery & Distribution Operations → Manage how generated ticket media are delivered or made available to customers, participants and operational staff.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-357?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: SMS Link, WhatsApp integration, Download, Apple Wallet, Google Wallet, POS, API, Physical Collection, Send credential.
- [ ] Every transition is wired: `BO-354`.
- [ ] Every gated control is gated: `ORDER_REPRINT`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-358` Media Binding, Activation & Assignment Operations

**Manage credentials that require operational assignment or activation after ticket issuance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/media-binding-activation-assignment-operations-bo-358` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every media binding activation** (data table, from `setMediaBindingActivation`)

| Shows | Format | Notes |
|---|---|---|
| Virtual ticket | text | Virtual Ticket |
| Customer | text | Customer |
| Product | text | Product |
| Existing media | text | Existing Media |
| Credential ID uid | text | Credential ID / UID |
| Provider | text | Provider |
| Activation mode | chip: Activate now, Schedule, Activate on first use, Activate on collection, Temporary … | When the bound medium becomes active |
| Validity | text | Validity |
| Binding rule | text | Binding Rule |

**The selected media binding activation** (detail panel): The pack groups this record's detail under its own headings: “This is especially important for”, “Scan Virtual Ticket QR”, “Scan Wristband UID”, “Resolve Virtual Ticket”, “Bind”, “Activate”.

| Shows | Format | Notes |
|---|---|---|
| Virtual ticket | text | Virtual Ticket |
| Customer | text | Customer |
| Product | text | Product |
| Existing media | text | Existing Media |
| Credential ID uid | text | Credential ID / UID |
| Provider | text | Provider |
| Activation mode | chip: Activate now, Schedule, Activate on first use, Activate on collection, Temporary … | When the bound medium becomes active |
| Validity | text | Validity |
| Binding rule | text | Binding Rule |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Scan (primary button) | navigation or local | — | — | — | — |
| Batch assignment (secondary button) | navigation or local | — | — | — | — |
| Encoder assignment (secondary button) | navigation or local | — | — | — | — |
| Activate Now (secondary button) | navigation or local | — | — | — | — |
| Schedule (secondary button) | navigation or local | — | — | — | — |
| Activate on First Use (secondary button) | navigation or local | — | — | — | — |
| Activate on Collection (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-354` Credential Operations Command Center: *Returns to the board's landing screen*; calls `setMediaBindingActivation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The media binding activation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the media binding activation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No media binding activation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the media binding activation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setMediaBindingActivation` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-358` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-358`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 8: Works in Media Binding, Activation & Assignment Operations → Manage credentials that require operational assignment or activation after ticket issuance.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-358?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Scan, Batch assignment, Encoder assignment, Activate Now, Schedule, Activate on First Use, Activate on Collection.
- [ ] Every transition is wired: `BO-354`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-359` Credential Replacement, Reissue, Revocation & Recovery

**Manage operational credential changes while preserving the underlying Virtual Ticket.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_EXCHANGE`, `SCOPE_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure/reference) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `credentialId` (navigation) |
| Route | `/access-venue/credential-replacement-reissue-revocation-recovery-bo-359` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Immediate old-media revocation | select field | — | — | — | — | — | — |
| Grace period | select field | — | — | — | — | — | — |
| Maximum replacements | select field | — | — | — | — | — | — |
| Identity verification | select field | — | — | — | — | — | — |
| Supervisor approval | select field | — | — | — | — | — | — |
| Reason codes | select field | — | — | — | — | — | — |

**Sent by *Replace credential*** (`replaceCredential`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Lost · Stolen · Damaged · Compromised · Customer changed phone · RFID failure · Wristband replacement · QR compromise · Wallet replacement · Face re enrollment · Incorrect assignment | — | — | `replaceCredential` body |
| New media kind `newMediaKind` | text field | optional | — | — | — | Media type of the replacement (`MediaTypeTechnologyLibraryView.mediaType`); empty keeps the current kind | `replaceCredential` body |
| New media code `newMediaCode` | text field | optional | — | — | — | Code of the new physical media where one is encoded at the counter | `replaceCredential` body |
| Approval request `approvalRequestId` | picker: choose an approval request | optional | — | — | shows names, sends the id | The granted approval, where the replacement rule requires one | `replaceCredential` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `replaceCredential` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Customer changed phone (primary button) | navigation or local | — | — | — | — |
| Wristband replacement (secondary button) | navigation or local | — | — | — | — |
| Wallet replacement (secondary button) | navigation or local | — | — | — | — |
| Incorrect assignment (secondary button) | navigation or local | — | — | — | — |
| Replace credential (primary button) | `replaceCredential` POST `/credentials/{credentialId}/replace` | CredentialReplacementInput | CredentialOperationsCommandCenterView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 replacement-limit, or approval-required, or the credential is revoked | step-up: mfa (Moves a paid ticket onto new media; the old one stops working.); gated `ORDER_EXCHANGE` |

**Data it reads**: `listCredentialReplacementReissue` (onLoad, Credential Replacement, Reissue, Revocation & Recovery)

**Where the user goes next**

- → `BO-354` Credential Operations Command Center: *Returns to the board's landing screen*; calls `listCredentialReplacementReissue`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential replacement reissue configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential replacement reissue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential replacement reissue configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission: reading needs SCOPE_VIEW; **replacing a credential needs ORDER_EXCHANGE with step-up (mfa)** (K1, 29 September), and the Replace action is hidden without it. Never an empty table. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 replacement-limit, or approval-required, or the credential is revoked |

#### Permissions

- `listCredentialReplacementReissue` → `SCOPE_VIEW` (read) · staff
- `replaceCredential` → `ORDER_EXCHANGE` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission: reading needs SCOPE_VIEW; **replacing a credential needs ORDER_EXCHANGE with step-up (mfa)** (K1, 29 September), and the Replace action is hidden without it. Never an empty table.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Lost wristband/card: operations identify the guest (phone number or ID), locate the original transaction and transfer the balance to a replacement wristband/card. *(client request · MoM 27 Aug 2026, 4.10 Lost-media recovery · DI-538)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-359` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-359`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 10: Works in Credential Replacement, Reissue, Revocation & Recovery → Manage operational credential changes while preserving the underlying Virtual Ticket.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-359?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Customer changed phone, Wristband replacement, Wallet replacement, Incorrect assignment, Replace credential.
- [ ] Every transition is wired: `BO-354`.
- [ ] Every gated control is gated: `ORDER_EXCHANGE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-360` Failed Generation, Delivery & Credential Exception Management

**Provide one dedicated operational queue for credential-related failures.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `exceptionId` (navigation) |
| Route | `/access-venue/failed-generation-delivery-credential-exception-manageme-bo-360` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Severity | text field | — | — | `listFailedGenerationDelivery` ?severity |
| Failure type | text field | — | — | `listFailedGenerationDelivery` ?failureType |

**Sent by *Retry*** (`resolveCredentialException`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | select | required | — | Retry · Regenerate · Use fallback · Escalate · Assign owner · Open technical case | — | — | `resolveCredentialException` body |
| Owner `ownerId` | text field | optional | — | — | — | Required for assignOwner and escalate | `resolveCredentialException` body |
| Fallback media kind `fallbackMediaKind` | radio group | optional | — | QR · Pdf · Printed ticket · RFID card · Wristband | — | Required for useFallback | `resolveCredentialException` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `resolveCredentialException` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every failed generation delivery** (data table, from `listFailedGenerationDelivery`)

| Shows | Format | Notes |
|---|---|---|
| Severity | chip: Low, Medium, High, Critical | Severity, weighted by event proximity, arrival time, affected tickets, fallback availability, VIP and access impact |
| Virtual ticket | text | Virtual Ticket |
| Credential | text | Credential |
| Media | text | Media |
| Customer | text | Customer |
| Event | text | Event |
| Failure | text | Failure |
| Time | 1 Oct 2026, 14:30 | Time |
| Operational impact | text | Operational Impact |
| Retry status | text | not in the schema: `Retry Status` |
| Owner | text | Owner |

**The selected failed generation delivery** (detail panel): The pack groups this record's detail under its own headings: “Include”, “Consider”.

| Shows | Format | Notes |
|---|---|---|
| Severity | chip: Low, Medium, High, Critical | Severity, weighted by event proximity, arrival time, affected tickets, fallback availability, VIP and access impact |
| Virtual ticket | text | Virtual Ticket |
| Credential | text | Credential |
| Media | text | Media |
| Customer | text | Customer |
| Event | text | Event |
| Failure | text | Failure |
| Time | 1 Oct 2026, 14:30 | Time |
| Operational impact | text | Operational Impact |
| Retry status | text | not in the schema: `Retry Status` |
| Owner | text | Owner |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Retry (primary button) | `resolveCredentialException` POST `/credential-exceptions/{exceptionId}/resolve` | CredentialExceptionActionInput | FailedGenerationDeliveryCredentialExceptionManagemenView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The exception is already resolved; 422 ownerId missing for assignOwner or escalate, or fallbackMediaKind … | — |
| Regenerate (secondary button) | `resolveCredentialException` POST `/credential-exceptions/{exceptionId}/resolve` | CredentialExceptionActionInput | FailedGenerationDeliveryCredentialExceptionManagemenView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The exception is already resolved; 422 ownerId missing for assignOwner or escalate, or fallbackMediaKind … | — |
| Use Fallback (secondary button) | `resolveCredentialException` POST `/credential-exceptions/{exceptionId}/resolve` | CredentialExceptionActionInput | FailedGenerationDeliveryCredentialExceptionManagemenView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The exception is already resolved; 422 ownerId missing for assignOwner or escalate, or fallbackMediaKind … | — |
| Escalate (secondary button) | `resolveCredentialException` POST `/credential-exceptions/{exceptionId}/resolve` | CredentialExceptionActionInput | FailedGenerationDeliveryCredentialExceptionManagemenView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The exception is already resolved; 422 ownerId missing for assignOwner or escalate, or fallbackMediaKind … | — |
| Assign Owner (secondary button) | `resolveCredentialException` POST `/credential-exceptions/{exceptionId}/resolve` | CredentialExceptionActionInput | FailedGenerationDeliveryCredentialExceptionManagemenView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The exception is already resolved; 422 ownerId missing for assignOwner or escalate, or fallbackMediaKind … | — |
| Open Technical Case (secondary button) | `resolveCredentialException` POST `/credential-exceptions/{exceptionId}/resolve` | CredentialExceptionActionInput | FailedGenerationDeliveryCredentialExceptionManagemenView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The exception is already resolved; 422 ownerId missing for assignOwner or escalate, or fallbackMediaKind … | — |

**Data it reads**: `listFailedGenerationDelivery` (onLoad, Failed Generation, Delivery & Credential Exception …)

**Where the user goes next**

- → `BO-354` Credential Operations Command Center: *Returns to the board's landing screen*; calls `listFailedGenerationDelivery`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The failed generation delivery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the failed generation delivery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No failed generation delivery yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the failed generation delivery are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The exception is already resolved; 422 ownerId missing for assignOwner or escalate, or fallbackMediaKind missing for useFallback |

#### Permissions

- `listFailedGenerationDelivery` → `SCOPE_VIEW` (read) · staff
- `resolveCredentialException` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-360` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-360`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 12: Works in Failed Generation, Delivery & Credential Exception Management → Provide one dedicated operational queue for credential-related failures.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-360?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Retry, Regenerate, Use Fallback, Escalate, Assign Owner, Open Technical Case.
- [ ] Every transition is wired: `BO-354`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-361` Credential Usage & Cross-Media Traceability

**Provide end-to-end visibility into how the different media attached to one Virtual Ticket have been presented or used. This screen is for credential traceability, while Area 16 remains responsible for the actual access-control decision.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `TICKET_LOOKUP` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture/reference) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/credential-usage-cross-media-traceability-bo-361` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Virtual Ticket | select field | — | — | — | — | — | — |
| Credential | select field | — | — | — | — | — | — |
| Media | select field | — | — | — | — | — | — |
| Presentation timestamp | select field | — | — | — | — | — | — |
| Location | select field | — | — | — | — | — | — |
| Device | select field | — | — | — | — | — | — |
| External system | select field | — | — | — | — | — | — |
| Transaction type | select field | — | — | — | — | — | — |
| Result | select field | — | — | — | — | — | — |
| Entitlement impact | select field | — | — | — | — | — | — |
| Synchronization status | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Virtual ticket | text field | — | — | `listCredentialUsageCross` ?virtualTicket |
| Media | text field | — | — | `listCredentialUsageCross` ?media |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What happened to the master entitlement? (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listCredentialUsageCross` (onLoad, Credential Usage & Cross-Media Traceability)

**Where the user goes next**

- → `BO-354` Credential Operations Command Center: *Returns to the board's landing screen*; calls `listCredentialUsageCross`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential usage cross-media configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential usage cross-media untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential usage cross-media configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCredentialUsageCross` → `TICKET_LOOKUP` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-361` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-361`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 14: Works in Credential Usage & Cross-Media Traceability → Provide end-to-end visibility into how the different media attached to one Virtual Ticket have been presented or used. This screen is for credential traceability, while Area 16 remains responsible …

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-361?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: What happened to the master entitlement?.
- [ ] Every transition is wired: `BO-354`.
- [ ] Every gated control is gated: `TICKET_LOOKUP`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-362` Credential Security, Audit & Operational Evidence

**Maintain complete evidence of credential creation and lifecycle activity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AUDIT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Identify) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/credential-security-audit-operational-evidence-bo-362` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Virtual ticket | text field | — | — | `listCredentialSecurityOperational` ?virtualTicket |
| Action | text field | — | — | `listCredentialSecurityOperational` ?action |
| Actor | text field | — | — | `listCredentialSecurityOperational` ?actor |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every credential security audit** (data table, from `listCredentialSecurityOperational`)

| Shows | Format | Notes |
|---|---|---|
| Anomaly flags | list or chips (count when long) | Suspicious patterns flagged on this entry |

**The selected credential security audit** (detail panel): The pack groups this record's detail under its own headings: “Record”, “RFID-1001”, “Access Control”, “Evidence Export”.

| Shows | Format | Notes |
|---|---|---|
| Anomaly flags | list or chips (count when long) | Suspicious patterns flagged on this entry |

**Data it reads**: `listCredentialSecurityOperational` (onLoad, Credential Security, Audit & Operational Evidence)

**Where the user goes next**

- → `BO-354` Credential Operations Command Center: *Returns to the board's landing screen*; calls `listCredentialSecurityOperational`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential security audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential security audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential security audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential security audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCredentialSecurityOperational` → `AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-362` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-362`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 16: Works in Credential Security, Audit & Operational Evidence → Maintain complete evidence of credential creation and lifecycle activity.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-362?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-354`.
- [ ] Every gated control is gated: `AUDIT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-363` Ticket Media Analytics & AI Operations Intelligence

**Provide management and operations with analytics and AI intelligence across Virtual Tickets and credential media. This should be a serious operational intelligence layer—not simply a chatbot.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Analyze; Compare) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/ticket-media-analytics-ai-operations-intelligence-bo-363` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search ticket media analytics | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by brand, venue, event, product, channel, media and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Brand | text field | — | — | `listTicketMedia` ?brand |
| Venue | text field | — | — | `listTicketMedia` ?venue |
| Event | text field | — | — | `listTicketMedia` ?event |
| Product | text field | — | — | `listTicketMedia` ?product |
| Channel | text field | — | — | `listTicketMedia` ?channel |
| Media | text field | — | — | `listTicketMedia` ?media |
| Provider | text field | — | — | `listTicketMedia` ?provider |
| Device | text field | — | — | `listTicketMedia` ?device |
| Customer segment | text field | — | — | `listTicketMedia` ?customerSegment |
| Time period | text field | — | — | `listTicketMedia` ?timePeriod |

#### Outputs: what the screen shows and produces

**Shown**

**Every ticket media analytics** (data table, from `listTicketMedia`)

| Shows | Format | Notes |
|---|---|---|
| Credentials generated | 1,234 | Credentials Generated |
| Generation success | 1,234.5 | Generation Success % |
| Delivery success | 1,234.5 | Delivery Success % |
| Activation | 1,234.5 | Activation % |
| Wallet adoption | 1,234.5 | Percent |
| RFID adoption | 1,234.5 | Percent |
| Face credential adoption | 1,234.5 | Percent |
| Multi media adoption | 1,234.5 | Percent |
| Replacement rate | 12.5% | Replacement Rate |
| Revocation rate | 12.5% | Revocation Rate |
| Generation failure | 1,234.5 | Generation Failure % |
| Delivery failure | 1,234.5 | Delivery Failure % |
| Average generation time | 1,234.5 | Seconds |
| Average resolution time | 1,234.5 | Seconds |
| Media usage distribution | list or chips (count when long) | Share of eligible customers per media type; may exceed 100% in total |
| Provider uptime | 1,234.5 | Percent |
| Generation failures | 1,234 | Generation failures |
| Encoding failures | 1,234 | Encoding failures |
| Delivery failures | 1,234 | Delivery failures |
| Synchronization delay | 1,234.5 | Seconds |
| Replacement frequency | 1,234.5 | Replacement frequency |

**The selected ticket media analytics** (detail panel): The pack groups this record's detail under its own headings: “Eligible customers”, “Backend Screen”, “Credential Operations Command Center”, “Operational exceptions”, “ONE VIRTUAL TICKET”.

| Shows | Format | Notes |
|---|---|---|
| Credentials generated | 1,234 | Credentials Generated |
| Generation success | 1,234.5 | Generation Success % |
| Delivery success | 1,234.5 | Delivery Success % |
| Activation | 1,234.5 | Activation % |
| Wallet adoption | 1,234.5 | Percent |
| RFID adoption | 1,234.5 | Percent |
| Face credential adoption | 1,234.5 | Percent |
| Multi media adoption | 1,234.5 | Percent |
| Replacement rate | 12.5% | Replacement Rate |
| Revocation rate | 12.5% | Revocation Rate |
| Generation failure | 1,234.5 | Generation Failure % |
| Delivery failure | 1,234.5 | Delivery Failure % |
| Average generation time | 1,234.5 | Seconds |
| Average resolution time | 1,234.5 | Seconds |
| Media usage distribution | list or chips (count when long) | Share of eligible customers per media type; may exceed 100% in total |
| Provider uptime | 1,234.5 | Percent |
| Generation failures | 1,234 | Generation failures |
| Encoding failures | 1,234 | Encoding failures |
| Delivery failures | 1,234 | Delivery failures |
| Synchronization delay | 1,234.5 | Seconds |
| Replacement frequency | 1,234.5 | Replacement frequency |

**Data it reads**: `listTicketMedia` (onLoad, Ticket Media Analytics & AI Operations Intelligence)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ticket media analytics list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ticket media analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ticket media analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the ticket media analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listTicketMedia` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-363` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-363`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 3
- Flow F170 *Ticket Media Credential Management board 3: Credential Operations Command Center*, step 18: Works in Ticket Media Analytics & AI Operations Intelligence → Provide management and operations with analytics and AI intelligence across Virtual Tickets and credential media. This should be a serious operational intelligence layer—not simply a chatbot.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (42 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-363?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
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

**6 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"deliverCredential": {"method":"POST","path":"/credentials/{credentialId}/deliveries","contract":"access","summary":"Send a credential over a channel","permission":"ORDER_REPRINT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CredentialDeliveryInput","responds":"CredentialDeliveryDistributionOperationsView"},
"getCredentialIssuanceRetryPolicy": {"method":"GET","path":"/credential-issuance-retry-policy","contract":"access","summary":"Read the credential issuance retry policy","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CredentialIssuanceRetryPolicyView"},
"listCredential": {"method":"GET","path":"/credential","contract":"access","summary":"Credential Operations Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"brand","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"date","in":"query","required":false},{"name":"media","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"customer","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"provider","in":"query","required":false},{"name":"exception","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCredentialDeliveryDistribution": {"method":"GET","path":"/credential-delivery-distribution","contract":"access","summary":"Credential Delivery & Distribution Operations","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCredentialGenerationIssuance": {"method":"GET","path":"/credential-generation-issuance","contract":"access","summary":"Credential Generation & Issuance Monitor","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":false},{"name":"trigger","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCredentialReplacementReissue": {"method":"GET","path":"/credential-replacement-reissue","contract":"access","summary":"Credential Replacement, Reissue, Revocation & Recovery","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CredentialReplacementReissueRevocationRecoveryView"},
"listCredentialSecurityOperational": {"method":"GET","path":"/credential-security-operational","contract":"access","summary":"Credential Security, Audit & Operational Evidence","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"virtualTicket","in":"query","required":false},{"name":"action","in":"query","required":false},{"name":"actor","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCredentialUsageCross": {"method":"GET","path":"/credential-usage-cross","contract":"access","summary":"Credential Usage & Cross-Media Traceability","permission":"TICKET_LOOKUP","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"virtualTicket","in":"query","required":false},{"name":"media","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFailedGenerationDelivery": {"method":"GET","path":"/failed-generation-delivery","contract":"access","summary":"Failed Generation, Delivery & Credential Exception Management","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"severity","in":"query","required":false},{"name":"failureType","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTicketMedia": {"method":"GET","path":"/ticket-media","contract":"access","summary":"Ticket Media Analytics & AI Operations Intelligence","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"brand","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"media","in":"query","required":false},{"name":"provider","in":"query","required":false},{"name":"device","in":"query","required":false},{"name":"customerSegment","in":"query","required":false},{"name":"timePeriod","in":"query","required":false}],"requestBody":null,"responds":"TicketMediaAnalyticsAiOperationsIntelligenceView"},
"replaceCredential": {"method":"POST","path":"/credentials/{credentialId}/replace","contract":"access","summary":"Replace a credential's media","permission":"ORDER_EXCHANGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CredentialReplacementInput","responds":"CredentialOperationsCommandCenterView"},
"resolveCredentialException": {"method":"POST","path":"/credential-exceptions/{exceptionId}/resolve","contract":"access","summary":"Act on a credential exception","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CredentialExceptionActionInput","responds":"FailedGenerationDeliveryCredentialExceptionManagemenView"},
"retryCredentialGeneration": {"method":"POST","path":"/credential-generation-issuance/retry","contract":"access","summary":"Retry failed credential generation","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CredentialGenerationRetryInput","responds":"CredentialGenerationRetryResult"},
"setCredentialIssuanceRetryPolicy": {"method":"PUT","path":"/credential-issuance-retry-policy","contract":"access","summary":"Set the credential issuance retry policy","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CredentialIssuanceRetryPolicyInput","responds":"CredentialIssuanceRetryPolicyView"},
"setMediaBindingActivation": {"method":"PUT","path":"/media-binding-activation","contract":"access","summary":"Media Binding, Activation & Assignment Operations","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MediaBindingActivationAssignmentOperationsInput","responds":"MediaBindingActivationAssignmentOperationsView"},
"setVirtualTicketCredential": {"method":"PUT","path":"/virtual-ticket-credential","contract":"access","summary":"Virtual Ticket & Credential 360° Workspace","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VirtualTicketCredential360WorkspaceInput","responds":"VirtualTicketCredential360WorkspaceView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CredentialDeliveryDistributionOperationsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Delivery & Distribution Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"virtualTicket":{"type":"string","description":"Virtual Ticket"},"media":{"type":"string","description":"Media"},"recipient":{"type":"string","description":"Recipient"},"channel":{"type":"string","enum":["email","smsLink","whatsapp","b2cAccount","mobileApp","download","appleWallet","googleWallet","pos","boxOffice","kiosk","groupPortal","api","physicalCollection"],"description":"Delivery channel"},"destination":{"type":"string","description":"Destination, masked"},"sentAt":{"type":"string","format":"date-time","description":"Sent At"},"deliveredAt":{"type":"string","format":"date-time","description":"Delivered At"},"openedDownloaded":{"type":"string","format":"date-time","description":"When opened or downloaded"},"attempt":{"type":"integer","description":"Attempt"},"status":{"type":"string","enum":["notRequired","pending","sent","delivered","openedDownloaded","completed","failed","bounced","expired","cancelled"],"description":"Delivery status"},"recipientRole":{"type":"string","enum":["purchaser","ticketHolder","participant","guardian","groupLeader","authorizedRecipient"],"description":"Who the credential was delivered to"}}},
"CredentialDeliveryInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"Send, or send again, one credential over one channel (decided 29 September, VM close-out).","required":["id","channel"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated delivery attempt id"},"channel":{"type":"string","enum":["email","smsLink","whatsapp","download","appleWallet","googleWallet","pos","api","physicalCollection"]},"recipient":{"type":"string","maxLength":320,"description":"Email address, phone number or collection point; empty sends to the recipient already on the credential"},"recipientRole":{"type":"string","enum":["purchaser","ticketHolder","participant","guardian","groupLeader","authorizedRecipient"],"default":"ticketHolder"},"note":{"type":"string","maxLength":300}}},
"CredentialExceptionActionInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"One action on a credential exception in the failure queue (decided 29 September, VM close-out).","required":["action"],"properties":{"action":{"type":"string","enum":["retry","regenerate","useFallback","escalate","assignOwner","openTechnicalCase"]},"ownerId":{"type":"string","description":"Required for assignOwner and escalate"},"fallbackMediaKind":{"type":"string","enum":["qr","pdf","printedTicket","rfidCard","wristband"],"description":"Required for useFallback"},"note":{"type":"string","maxLength":500}}},
"CredentialGenerationIssuanceMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Generation & Issuance Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"trigger":{"type":"string","enum":["orderConfirmation","ticketIssuance","membershipActivation","customerRequest","staffAction","rfidCollection","walletRequest","faceEnrollment","api","bulkOperation","scheduledProcess"],"description":"What triggered generation"},"requestId":{"type":"string","description":"Request ID"},"virtualTicket":{"type":"string","description":"Virtual Ticket"},"media":{"type":"string","description":"Media"},"template":{"type":"string","description":"Template"},"templateVersion":{"type":"string","description":"Template Version"},"product":{"type":"string","description":"Product"},"customer":{"type":"string","description":"Customer"},"provider":{"type":"string","description":"Provider"},"requestedAt":{"type":"string","format":"date-time","description":"Requested At"},"generatedAt":{"type":"string","format":"date-time","description":"Generated At"},"status":{"type":"string","enum":["requested","queued","templateResolved","dataMapped","credentialGenerated","bound","ready","delivered","failed"],"description":"Generation stage"},"error":{"type":"string","description":"Error"},"brand":{"type":"string","description":"Brand"},"venue":{"type":"string","description":"Venue"},"event":{"type":"string","description":"Event"},"channel":{"type":"string","description":"Channel"},"language":{"type":"string","description":"Language"},"customerContext":{"type":"string","description":"Customer context"},"failureReason":{"type":"string","enum":["templateMissing","requiredDataMissing","providerUnavailable","invalidPayload","tokenGenerationFailure","walletGenerationFailure","encoderUnavailable"],"description":"Failure category when status is failed"}}},
"CredentialGenerationRetryInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"Retry failed credential generation, for selected requests or every eligible one (decided 29 September, VM close-out).","required":["scope"],"properties":{"scope":{"type":"string","enum":["selected","allEligible"]},"requestIds":{"type":"array","items":{"type":"string"},"maxItems":500,"description":"The failed generation requests (`CredentialGenerationIssuanceMonitorView.requestId`); required for selected"}}},
"CredentialGenerationRetryResult": {"type":"object","x-ticvai-persistence":"none — computed (decided 29 September, VM close-out)","description":"What a retry queued and what it skipped (decided 29 September, VM close-out).","required":["queued","skipped"],"properties":{"queued":{"type":"integer"},"skipped":{"type":"array","items":{"type":"object","properties":{"requestId":{"type":"string"},"reason":{"type":"string","enum":["notFailed","alreadyQueued","notRetryable"]}}}}}},
"CredentialIssuanceRetryPolicyInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"The tenant's automatic retry policy for failed credential generation (decided 29 September, VM close-out). Proposed defaults are ours (our build plan).","required":["automaticRetry"],"properties":{"automaticRetry":{"type":"boolean","default":true},"maxAttempts":{"type":"integer","minimum":1,"maximum":10,"default":3},"backoffMinutes":{"type":"integer","minimum":1,"maximum":240,"default":5,"description":"Wait before the first retry; doubles on each attempt"},"escalateAfterAttempts":{"type":"integer","minimum":1,"maximum":10,"default":3,"description":"After this many failures the request becomes a credential exception with an owner; not more than maxAttempts"}}},
"CredentialIssuanceRetryPolicyView": {"type":"object","x-ticvai-persistence":"access.credential_issuance_retry_policy","description":"The automatic retry policy in force, one per venue (decided 29 September, VM close-out).","required":["venueId","automaticRetry","maxAttempts","backoffMinutes","escalateAfterAttempts"],"properties":{"venueId":{"type":"string"},"automaticRetry":{"type":"boolean","default":true},"maxAttempts":{"type":"integer","minimum":1,"maximum":10,"default":3},"backoffMinutes":{"type":"integer","minimum":1,"maximum":240,"default":5},"escalateAfterAttempts":{"type":"integer","minimum":1,"maximum":10,"default":3},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","description":"The partition key (ADR-0005). Written at venue scope"}}},
"CredentialOperationsCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"virtualTicketId":{"type":"string","description":"Virtual Ticket ID"},"credentialId":{"type":"string","description":"Credential ID"},"mediaType":{"type":"string","description":"Media Type"},"customerParticipant":{"type":"string","description":"Customer / Participant"},"product":{"type":"string","description":"Product"},"event":{"type":"string","description":"Event"},"credentialStatus":{"type":"string","enum":["pendingGeneration","generated","pendingActivation","active","suspended","revoked","expired","failed"],"description":"Credential status"},"deliveryStatus":{"type":"string","enum":["notRequired","pending","sent","delivered","openedDownloaded","completed","failed","bounced","expired","cancelled"],"description":"Delivery status (15.3.4)"},"activationStatus":{"type":"string","enum":["pending","scheduled","active","notRequired"],"description":"Activation status"},"bindingStatus":{"type":"string","enum":["pending","bound","unbound","failed"],"description":"Binding status"},"provider":{"type":"string","description":"Provider"},"lastActivity":{"type":"string","format":"date-time","description":"Last Activity"},"exception":{"type":"string","description":"Exception"},"owner":{"type":"string","description":"Owner"}}},
"CredentialOperationsCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"virtualTicketsIssued":{"type":"integer","description":"Virtual Tickets Issued"},"credentialsGenerated":{"type":"integer","description":"Credentials Generated"},"activeCredentials":{"type":"integer","description":"Active Credentials"},"pendingGeneration":{"type":"integer","description":"Pending Generation"},"pendingDelivery":{"type":"integer","description":"Pending Delivery"},"pendingBinding":{"type":"integer","description":"Pending Binding"},"pendingActivation":{"type":"integer","description":"Pending Activation"},"suspended":{"type":"integer","description":"Suspended"},"revoked":{"type":"integer","description":"Revoked"},"expired":{"type":"integer","description":"Expired"},"failedGeneration":{"type":"integer","description":"Failed Generation"},"failedDelivery":{"type":"integer","description":"Failed Delivery"},"synchronizationExceptions":{"type":"integer","description":"Synchronization Exceptions"},"multiMediaVirtualTickets":{"type":"integer","description":"Multi-Media Virtual Tickets"},"virtualTicketsWithoutActiveMedia":{"type":"integer","description":"Virtual Tickets Without Active Media"},"dynamicQr":{"type":"integer","description":"Credentials of this media type"},"barcode":{"type":"integer","description":"Credentials of this media type"},"pdf":{"type":"integer","description":"Credentials of this media type"},"appleWallet":{"type":"integer","description":"Credentials of this media type"},"googleWallet":{"type":"integer","description":"Credentials of this media type"},"rfid":{"type":"integer","description":"Credentials of this media type"},"nfc":{"type":"integer","description":"Credentials of this media type"},"faceRecognitionReference":{"type":"integer","description":"Credentials of this media type"},"card":{"type":"integer","description":"Credentials of this media type"},"wristband":{"type":"integer","description":"Credentials of this media type"}}},
"CredentialReplacementInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"Replace the media of a credential while the Virtual Ticket stays the same (decided 29 September, VM close-out).","required":["reason"],"properties":{"reason":{"type":"string","enum":["lost","stolen","damaged","compromised","customerChangedPhone","rfidFailure","wristbandReplacement","qrCompromise","walletReplacement","faceReEnrollment","incorrectAssignment"]},"newMediaKind":{"type":"string","description":"Media type of the replacement (`MediaTypeTechnologyLibraryView.mediaType`); empty keeps the current kind"},"newMediaCode":{"type":"string","description":"Code of the new physical media where one is encoded at the counter"},"approvalRequestId":{"type":"string","format":"uuid","description":"The granted approval, where the replacement rule requires one"},"note":{"type":"string","maxLength":500}}},
"CredentialReplacementReissueRevocationRecoveryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Replacement, Reissue, Revocation & Recovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"reason":{"type":"string","enum":["lost","stolen","damaged","compromised","customerChangedPhone","rfidFailure","wristbandReplacement","qrCompromise","walletReplacement","faceReEnrollment","incorrectAssignment"],"description":"Replacement reason this policy covers"},"immediateOldMediaRevocation":{"type":"boolean","description":"Immediate old-media revocation"},"gracePeriod":{"type":"string","description":"ISO 8601 duration, e.g. PT30M"},"maximumReplacements":{"type":"integer","description":"Maximum replacements"},"identityVerification":{"type":"boolean","description":"Identity verification"},"supervisorApproval":{"type":"boolean","description":"Supervisor approval"},"reasonCodes":{"type":"array","items":{"type":"string"},"description":"Reason codes"},"recoveryAllowed":{"type":"boolean","description":"A suspended credential may be restored under this policy"}},"required":["reason"]},
"CredentialSecurityAuditOperationalEvidenceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Security, Audit & Operational Evidence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"virtualTicket":{"type":"string","description":"Virtual Ticket"},"credential":{"type":"string","description":"Credential"},"media":{"type":"string","description":"Media"},"action":{"type":"string","enum":["credentialRequested","generated","bound","delivered","activated","updated","presented","suspended","reactivated","replaced","revoked","expired","rebound","regenerated","deleted"],"description":"Lifecycle action recorded"},"before":{"type":"string","description":"Before"},"after":{"type":"string","description":"After"},"actor":{"type":"string","description":"Actor"},"source":{"type":"string","description":"Source"},"device":{"type":"string","description":"Device"},"dateTime":{"type":"string","format":"date-time","description":"Date/time"},"reason":{"type":"string","description":"Reason"},"approval":{"type":"string","description":"Approval"},"providerReference":{"type":"string","description":"Provider reference"},"relatedTransaction":{"type":"string","description":"Related transaction"},"anomalyFlags":{"type":"array","items":{"type":"string","enum":["excessiveRegeneration","repeatedReplacement","suspiciousRebinding","multipleCredentialAssignments","unexpectedProviderTokenChanges","unauthorizedAdministrativeActions"]},"description":"Suspicious patterns flagged on this entry"}}},
"CredentialUsageCrossMediaTraceabilityView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Usage & Cross-Media Traceability displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"virtualTicket":{"type":"string","description":"Virtual Ticket"},"credential":{"type":"string","description":"Credential"},"media":{"type":"string","description":"Media"},"presentationTimestamp":{"type":"string","format":"date-time","description":"Presentation timestamp"},"location":{"type":"string","description":"Location"},"device":{"type":"string","description":"Device"},"externalSystem":{"type":"string","description":"External system"},"transactionType":{"type":"string","description":"Transaction type"},"result":{"type":"string","description":"Result"},"entitlementImpact":{"type":"string","description":"Entitlement impact"},"synchronizationStatus":{"type":"string","description":"Synchronization status"}}},
"FailedGenerationDeliveryCredentialExceptionManagemenView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Failed Generation, Delivery & Credential Exception Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"exceptionId":{"type":"string","format":"uuid","description":"The key `resolveCredentialException` acts on (decided 29 September, VM close-out)"},"lastAction":{"type":"string","enum":["retry","regenerate","useFallback","escalate","assignOwner","openTechnicalCase"],"description":"The last action taken through `resolveCredentialException`"},"failureType":{"type":"string","enum":["generationFailed","bindingFailed","activationFailed","deliveryFailed","walletFailure","rfidEncodingFailure","duplicateCredential","invalidToken","providerFailure","synchronizationFailure","missingTemplate","missingRequiredData","expiredCredential","mappingFailure","unknownCredential"],"description":"Failure category"},"severity":{"type":"string","enum":["low","medium","high","critical"],"description":"Severity, weighted by event proximity, arrival time, affected tickets, fallback availability, VIP and access impact"},"virtualTicket":{"type":"string","description":"Virtual Ticket"},"credential":{"type":"string","description":"Credential"},"media":{"type":"string","description":"Media"},"customer":{"type":"string","description":"Customer"},"event":{"type":"string","description":"Event"},"failure":{"type":"string","description":"Failure"},"time":{"type":"string","format":"date-time","description":"Time"},"operationalImpact":{"type":"string","description":"Operational Impact"},"owner":{"type":"string","description":"Owner"},"retryStatus":{"type":"string","description":"Retry status"}}},
"MediaBindingActivationAssignmentOperationsInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Media Binding, Activation & Assignment Operations submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"credentialIdUid":{"type":"string","description":"Credential ID or UID read from the medium; for face, the biometric provider reference"},"virtualTicketId":{"type":"string","description":"Virtual Ticket the medium is bound to"},"mediaKind":{"type":"string","enum":["rfid","nfc","wristband","physicalCard","faceRecognition","temporaryCredential"],"description":"Medium being bound"},"captureMethod":{"type":"string","enum":["scan","tap","manualLookup","batchAssignment","encoderAssignment"],"description":"How the medium was read or assigned"},"activationMode":{"type":"string","enum":["activateNow","schedule","activateOnFirstUse","activateOnCollection","temporaryActivation"],"description":"When the bound medium becomes active"},"provider":{"type":"string","description":"Provider"},"scheduledAt":{"type":"string","format":"date-time","description":"Activation time when scheduled"}},"required":["virtualTicketId","mediaKind","credentialIdUid"]},
"MediaBindingActivationAssignmentOperationsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Media Binding, Activation & Assignment Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"virtualTicketId":{"type":"string","description":"Virtual Ticket the medium is bound to"},"mediaKind":{"type":"string","enum":["rfid","nfc","wristband","physicalCard","faceRecognition","temporaryCredential"],"description":"Medium being bound"},"virtualTicket":{"type":"string","description":"Virtual Ticket"},"customer":{"type":"string","description":"Customer"},"product":{"type":"string","description":"Product"},"existingMedia":{"type":"string","description":"Existing Media"},"credentialIdUid":{"type":"string","description":"Credential ID / UID"},"provider":{"type":"string","description":"Provider"},"activationMode":{"type":"string","enum":["activateNow","schedule","activateOnFirstUse","activateOnCollection","temporaryActivation"],"description":"When the bound medium becomes active"},"validity":{"type":"string","description":"Validity"},"bindingRule":{"type":"string","description":"Binding Rule"},"captureMethod":{"type":"string","enum":["scan","tap","manualLookup","batchAssignment","encoderAssignment"],"description":"How the medium was read or assigned"},"scheduledAt":{"type":"string","format":"date-time","description":"Activation time when scheduled"}},"required":["virtualTicketId","mediaKind","credentialIdUid"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"TicketMediaAnalyticsAiOperationsIntelligenceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Ticket Media Analytics & AI Operations Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"credentialsGenerated":{"type":"integer","description":"Credentials Generated"},"generationSuccess":{"type":"number","description":"Generation Success %"},"deliverySuccess":{"type":"number","description":"Delivery Success %"},"activation":{"type":"number","description":"Activation %"},"walletAdoption":{"type":"number","description":"Percent"},"rfidAdoption":{"type":"number","description":"Percent"},"faceCredentialAdoption":{"type":"number","description":"Percent"},"multiMediaAdoption":{"type":"number","description":"Percent"},"replacementRate":{"type":"number","description":"Replacement Rate"},"revocationRate":{"type":"number","description":"Revocation Rate"},"generationFailure":{"type":"number","description":"Generation Failure %"},"deliveryFailure":{"type":"number","description":"Delivery Failure %"},"averageGenerationTime":{"type":"number","description":"Seconds"},"averageResolutionTime":{"type":"number","description":"Seconds"},"mediaUsageDistribution":{"type":"array","items":{"type":"string"},"description":"Share of eligible customers per media type; may exceed 100% in total"},"providerUptime":{"type":"number","description":"Percent"},"generationFailures":{"type":"integer","description":"Generation failures"},"encodingFailures":{"type":"integer","description":"Encoding failures"},"deliveryFailures":{"type":"integer","description":"Delivery failures"},"synchronizationDelay":{"type":"number","description":"Seconds"},"replacementFrequency":{"type":"number","description":"Replacement frequency"},"credentialFailureRisk":{"type":"string","description":"Predicted; advisory"},"deliveryFailureProbability":{"type":"number","description":"Predicted, 0 to 1; advisory"},"mediaDemandForUpcomingEvents":{"type":"string","description":"Media demand for upcoming events"},"rfidWristbandStockRequirements":{"type":"string","description":"RFID/wristband stock requirements"},"operationalWorkload":{"type":"string","description":"Operational workload"},"likelyOnSiteReplacementVolumes":{"type":"integer","description":"Predicted; advisory"}}},
"VirtualTicketCredential360WorkspaceInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is access.entitlement at 9%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Virtual Ticket & Credential 360° Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *For each media show* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.","properties":{"virtualTicketId":{"type":"string","description":"Virtual Ticket ID"},"mediaRole":{"type":"string","enum":["primary","secondary","fallback","temporary","revokedHistorical"],"description":"Role of the medium on the ticket"},"bindingId":{"type":"string","description":"Binding ID"},"mediaType":{"type":"string","description":"Media type"},"provider":{"type":"string","description":"Provider"},"issued":{"type":"string","format":"date-time","description":"Issued"},"delivered":{"type":"string","format":"date-time","description":"Delivered"},"activated":{"type":"string","format":"date-time","description":"Activated"},"validFrom":{"type":"string","format":"date-time","description":"Valid From"},"validTo":{"type":"string","format":"date-time","description":"Valid To"},"lastUpdate":{"type":"string","format":"date-time","description":"Last update"},"lastPresentation":{"type":"string","format":"date-time","description":"Last presentation"},"lastUse":{"type":"string","format":"date-time","description":"Last use"},"deviceReferenceWhereAppropriate":{"type":"string","description":"Device/reference where appropriate"},"status":{"type":"string","enum":["pending","active","suspended","revoked","expired"],"description":"Medium status"}},"x-ticvai-record-definition":"For each media show","required":["virtualTicketId"]},
"VirtualTicketCredential360WorkspaceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Virtual Ticket & Credential 360° Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"virtualTicketId":{"type":"string","description":"Virtual Ticket ID"},"ticketHolder":{"type":"string","description":"Ticket Holder"},"participant":{"type":"string","description":"Participant"},"product":{"type":"string","description":"Product"},"event":{"type":"string","description":"Event"},"performance":{"type":"string","description":"Performance"},"venue":{"type":"string","description":"Venue"},"seat":{"type":"string","description":"Seat"},"order":{"type":"string","description":"Order"},"ticketStatus":{"type":"string","enum":["created","pendingFulfillment","active","partiallyUsed","used","expired","suspended","cancelled","voided","reissuedSuperseded","refunded","transferred","blocked"],"description":"Virtual Ticket status"},"usageStatus":{"type":"string","enum":["unused","partiallyUsed","used"],"description":"Usage status"},"validity":{"type":"string","description":"Validity"},"entitlements":{"type":"array","items":{"type":"string"},"description":"Entitlements on the ticket"},"mediaRole":{"type":"string","enum":["primary","secondary","fallback","temporary","revokedHistorical"],"description":"Role of the medium on the ticket"},"bindingId":{"type":"string","description":"Binding ID"},"mediaType":{"type":"string","description":"Media type"},"provider":{"type":"string","description":"Provider"},"issued":{"type":"string","format":"date-time","description":"Issued"},"delivered":{"type":"string","format":"date-time","description":"Delivered"},"activated":{"type":"string","format":"date-time","description":"Activated"},"validFrom":{"type":"string","format":"date-time","description":"Valid From"},"validTo":{"type":"string","format":"date-time","description":"Valid To"},"lastUpdate":{"type":"string","format":"date-time","description":"Last update"},"lastPresentation":{"type":"string","format":"date-time","description":"Last presentation"},"lastUse":{"type":"string","format":"date-time","description":"Last use"},"deviceReferenceWhereAppropriate":{"type":"string","description":"Device/reference where appropriate"},"status":{"type":"string","enum":["pending","active","suspended","revoked","expired"],"description":"Medium status"}},"required":["virtualTicketId"]}
}
```
