# WS59 — Ticket Media   Credential Management board 1

**10 screens · 16 operations · 18 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `ACCESS_POINT_CONFIGURE, AUDIT_VIEW, SCOPE_VIEW`. A control nobody can use must say so,
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
| `BO-334` | Virtual Ticket Command Center | B–D | 2 | 26 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-335` | Virtual Ticket Identity & Master Record Configuration | A | 9 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-336` | Virtual Ticket Status & Lifecycle Model | B–D | 7 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-337` | Media Type & Credential Technology Registry | B–D | 18 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-338` | Multi-Media Binding & Association Rules | B–D | 36 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-339` | Credential Identity, Token & Reference Mapping | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-340` | Entitlement & Cross-Media Synchronization Rules | B–D | 7 | 2 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-341` | Media Activation, Priority & Fallback Rules | B–D | 6 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-342` | Media Replacement, Revocation & Rebinding Rules | B–D | 22 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-343` | Virtual Ticket Architecture Testing, Governance & Audit | B–D | 9 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-336, BO-339, BO-340 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-334` Virtual Ticket Command Center

**Provide administrators and operations teams with a centralized view of all Virtual Tickets and their associated media across TICVAI. This is the primary administrative entry point into the Virtual Ticket architecture.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AUDIT_VIEW`, `SCOPE_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each record should show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/virtual-ticket-command-center-bo-334` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search virtual ticket | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by brand, venue, event, product, performance, ticket type and 7 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Brand | text field | — | — | `listVirtualTicket` ?brand |
| Venue | text field | — | — | `listVirtualTicket` ?venue |
| Event | text field | — | — | `listVirtualTicket` ?event |
| Performance | text field | — | — | `listVirtualTicket` ?performance |
| Channel | text field | — | — | `listVirtualTicket` ?channel |
| Customer | text field | — | — | `listVirtualTicket` ?customer |
| Virtual ticket status | text field | — | — | `listVirtualTicket` ?virtualTicketStatus |
| Media type | text field | — | — | `listVirtualTicket` ?mediaType |
| Product | text field | — | — | `listVirtualTicket` ?product |
| Ticket type | text field | — | — | `listVirtualTicket` ?ticketType |
| Number of media | text field | — | — | `listVirtualTicket` ?numberOfMedia |
| Validity | text field | — | — | `listVirtualTicket` ?validity |
| Usage status | text field | — | — | `listVirtualTicket` ?usageStatus |
| Change type | text field | — | — | `listVirtualTicketArchitecture` ?changeType |

#### Outputs: what the screen shows and produces

**Shown**

**Total Virtual Tickets** (metric tile)

**Active** (metric tile)

**Pending Activation** (metric tile)

**Suspended** (metric tile)

**Used / Consumed** (metric tile)

**Partially Consumed** (metric tile)

**Expired** (metric tile)

**Cancelled** (metric tile)

**Revoked** (metric tile)

**Virtual Tickets with Multiple Media** (metric tile)

**Virtual Tickets with No Active Media** (metric tile)

**Media Binding Exceptions** (metric tile)

**Credential Synchronization Issues** (metric tile)

**Every virtual ticket** (data table, from `listVirtualTicket`)

| Shows | Format | Notes |
|---|---|---|
| Virtual ticket | text | Virtual Ticket ID |
| Product | text | Product |
| Event performance | text | Event / Performance |
| Ticket holder | text | Ticket Holder |
| Order reference | text | Order Reference |
| Ticket type | text | Ticket Type |
| Seat resource where applicable | text | Seat / Resource where applicable |
| Ticket status | chip: Created, Pending fulfillment, Active, Partially used, Used, Expired… | Virtual Ticket status (lifecycle 15.1.3) |
| Usage status | chip: Unused, Partially used, Used | How much of the entitlement is consumed |
| Number of linked media | 1,234 | Number of Linked Media |
| Primary media | text | Primary Media |
| Last credential activity | 1 Oct 2026, 14:30 | Last Credential Activity |
| Last modified | 1 Oct 2026, 14:30 | Last Modified |

**The selected virtual ticket** (detail panel): The pack groups this record's detail under its own headings: “VT-2026-009821”.

| Shows | Format | Notes |
|---|---|---|
| Virtual ticket | text | Virtual Ticket ID |
| Product | text | Product |
| Event performance | text | Event / Performance |
| Ticket holder | text | Ticket Holder |
| Order reference | text | Order Reference |
| Ticket type | text | Ticket Type |
| Seat resource where applicable | text | Seat / Resource where applicable |
| Ticket status | chip: Created, Pending fulfillment, Active, Partially used, Used, Expired… | Virtual Ticket status (lifecycle 15.1.3) |
| Usage status | chip: Unused, Partially used, Used | How much of the entitlement is consumed |
| Number of linked media | 1,234 | Number of Linked Media |
| Primary media | text | Primary Media |
| Last credential activity | 1 Oct 2026, 14:30 | Last Credential Activity |
| Last modified | 1 Oct 2026, 14:30 | Last Modified |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** View Virtual Ticket, View Media, Bind Media, Replace Media, Suspend, Reactivate, Revoke Media, View Usage, View Audit, Diagnose Credential. Each needs attaching to the control it gates, or the screen needs the control.

**Data it reads**: `listVirtualTicket` (onLoad, Virtual Ticket Command Center); `listVirtualTicketStatus` (onLoad, Virtual Ticket Status & Lifecycle Model); `listVirtualTicketArchitecture` (onLoad, Virtual Ticket Architecture Testing, Governance & Audit)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-335` Virtual Ticket Identity & Master Record Configuration: *Works in Virtual Ticket Identity & Master Record Configuration*; calls `listVirtualTicket`
- → `BO-336` Virtual Ticket Status & Lifecycle Model: *Works in Virtual Ticket Status & Lifecycle Model*; calls `listVirtualTicket`
- → `BO-337` Media Type & Credential Technology Registry: *Works in Media Type & Credential Technology Registry*; calls `listVirtualTicket`
- → `BO-338` Multi-Media Binding & Association Rules: *Works in Multi-Media Binding & Association Rules*; calls `listVirtualTicket`
- → `BO-339` Credential Identity, Token & Reference Mapping: *Works in Credential Identity, Token & Reference Mapping*; calls `listVirtualTicket`
- → `BO-340` Entitlement & Cross-Media Synchronization Rules: *Works in Entitlement & Cross-Media Synchronization Rules*; calls `listVirtualTicket`
- → `BO-341` Media Activation, Priority & Fallback Rules: *Works in Media Activation, Priority & Fallback Rules*; calls `listVirtualTicket`
- → `BO-342` Media Replacement, Revocation & Rebinding Rules: *Works in Media Replacement, Revocation & Rebinding Rules*; calls `listVirtualTicket`
- → `BO-343` Virtual Ticket Architecture Testing, Governance & Audit: *Works in Virtual Ticket Architecture Testing, Governance & Audit*; calls `listVirtualTicket`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The virtual ticket list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the virtual ticket untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No virtual ticket yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the virtual ticket are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listVirtualTicket` → `SCOPE_VIEW` (read) · staff
- `listVirtualTicketStatus` → `SCOPE_VIEW` (read) · staff
- `listVirtualTicketArchitecture` → `AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- A ticket is always one virtual record; QR, RFID, NFC, face and future credentials (e.g. hotel room key, city transit card) are interchangeable media linked to it. Screens should show one ticket with its linked media, not separate tickets per medium. *(agreed · MoM 2 Sep 2026, 5. Key Decisions & Agreements · DI-652)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-334` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-334`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 1: Opens Virtual Ticket Command Center → Provide administrators and operations teams with a centralized view of all Virtual Tickets and their associated media across TICVAI. This is the primary administrative entry point into the Virtual …
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F168 branch at step 1 (expected): when Nothing has been set up on Virtual Ticket Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F168 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-334?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-335`, `BO-336`, `BO-337`, `BO-338`, `BO-339`, `BO-340`, `BO-341`, `BO-342`, `BO-343`.
- [ ] Every gated control is gated: `AUDIT_VIEW`, `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-335` Virtual Ticket Identity & Master Record Configuration

**Define the authoritative Virtual Ticket object used throughout TICVAI. This screen is extremely important because the Virtual Ticket—not the QR/RFID/card— is the master ticket record.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block A · ticket #20684 (APP-SETUP-BO-335) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/virtual-ticket-identity-master-record-configuration-bo-335` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| ID generation pattern | select field | — | — | — | — | — | — |
| Ticket classification | select field | — | — | — | — | — | — |
| Ticket ownership model | select field | — | — | — | — | — | — |
| Holder assignment requirements | select field | — | — | — | — | — | — |
| Transferability reference | select field | — | — | — | — | — | — |
| Validity model | select field | — | — | — | — | — | — |
| Consumption model | select field | — | — | — | — | — | — |
| Entitlement model | select field | — | — | — | — | — | — |
| Media requirements | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-334` Virtual Ticket Command Center: *Returns to the board's landing screen*; calls `setVirtualTicketIdentity`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The virtual ticket identity configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the virtual ticket identity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No virtual ticket identity configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setVirtualTicketIdentity` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Media = any identifier a ticket is presented by (QR, RFID/wristband, facial recognition, other). Virtual ticket media IDs configurable by prefix, suffix and length; several media can link to one ticket (e.g. a season pass by face, QR or RFID as fallbacks). *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-608)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-335` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-335`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 2: Works in Virtual Ticket Identity & Master Record Configuration → Define the authoritative Virtual Ticket object used throughout TICVAI. This screen is extremely important because the Virtual Ticket—not the QR/RFID/card— is the master ticket record.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-335?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-334`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-336` Virtual Ticket Status & Lifecycle Model

**Configure the standardized lifecycle of a Virtual Ticket independently from the lifecycle of individual media.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/virtual-ticket-status-lifecycle-model-bo-336` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Form: Save ticket status transition** (modal, opened by *Save ticket status transition*; *Save ticket status transition* calls `setTicketStatusTransition`, *Cancel* sends nothing)

**Collects what `setTicketStatusTransition` sends before it is called.** Required: `id`, `fromStatus`, `toStatus`, `allowed`, `requiresAuthorizedException`, `scopePath`. Optional: `originatingSources`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setTicketStatusTransition` body |
| From status `fromStatus` | select | required | — | Created · Pending fulfillment · Active · Partially used · Used · Expired · Suspended · Cancelled · Voided · Reissued superseded · Refunded · Transferred … | — | — | `setTicketStatusTransition` body |
| To status `toStatus` | select | required | — | Created · Pending fulfillment · Active · Partially used · Used · Expired · Suspended · Cancelled · Voided · Reissued superseded · Refunded · Transferred … | — | Unique with fromStatus per scope | `setTicketStatusTransition` body |
| Allowed `allowed` | toggle | required | — | — | — | — | `setTicketStatusTransition` body |
| Requires authorized exception `requiresAuthorizedException` | toggle | required | off | — | — | Allowed only with an authorised exception, e.g. | `setTicketStatusTransition` body |
| Originating sources `originatingSources` | multi-select chips | optional | — | Order management · Cancellation · Refund · Upgrade conversion · Ticket transfer · Membership · Expiry · Access usage · Authorized operator · API · Scheduled process | — | — | `setTicketStatusTransition` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node | `setTicketStatusTransition` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 The transition is not in the entitlement state model.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save ticket status transition (primary button) | `setTicketStatusTransition` PUT `/ticket-status-transitions` | AccessTicketStatusTransition | AccessTicketStatusTransition | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 422 The transition is not in the entitlement state model. | gated `ACCESS_POINT_CONFIGURE`; opens modal first; produces a document or message: Set a Virtual Ticket status transition rule |

**Data it reads**: `listVirtualTicketStatus` (onLoad, Virtual Ticket Status & Lifecycle Model)

**Where the user goes next**

- → `BO-334` Virtual Ticket Command Center: *Returns to the board's landing screen*; calls `listVirtualTicketStatus`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The virtual ticket status list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the virtual ticket status untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No virtual ticket status yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the virtual ticket status are still there. The pack's own statuses are Order Management — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 The transition is not in the entitlement state model. |

#### Permissions

- `listVirtualTicketStatus` → `SCOPE_VIEW` (read) · staff
- `setTicketStatusTransition` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Entitlement statuses: active, reserved, consumed, transferred, expired, refunded/cancelled; views show entitlements nearing expiry, real-time consumption per customer, and whether a ticket has been upgraded. *(client request · MoM 7 Sep 2026, 4.10 / 4.11 Entitlements Lifecycle & Usage · DI-670)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-336` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-336`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 4: Works in Virtual Ticket Status & Lifecycle Model → Configure the standardized lifecycle of a Virtual Ticket independently from the lifecycle of individual media.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-336?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save ticket status transition.
- [ ] Every transition is wired: `BO-334`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-337` Media Type & Credential Technology Registry

**Maintain the centralized catalogue of credential technologies supported by TICVAI. This makes the credential architecture extensible rather than hard-coded.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§For each technology configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/media-type-credential-technology-registry-bo-337` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Media Type ID | select field | — | — | — | — | — | — |
| Name | select field | — | — | — | — | — | — |
| Category | select field | — | — | — | — | — | — |
| Provider | select field | — | — | — | — | — | — |
| Technology | select field | — | — | — | — | — | — |
| Token format | select field | — | — | — | — | — | — |
| Generation method | select field | — | — | — | — | — | — |
| Validation mechanism | select field | — | — | — | — | — | — |
| Supports visual design | select field | — | — | — | — | — | — |
| Supports dynamic update | select field | — | — | — | — | — | — |
| Supports revocation | select field | — | — | — | — | — | — |
| Supports expiration | select field | — | — | — | — | — | — |
| Supports offline reference | select field | — | — | — | — | — | — |
| Supports replacement | select field | — | — | — | — | — | — |
| Supports encryption/signing | select field | — | — | — | — | — | — |
| Supported channels | select field | — | — | — | — | — | — |
| Supported devices | select field | — | — | — | — | — | — |
| Integration adapter | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listMediaTypeTechnology` (onLoad, Media Type & Technology Library); `listMediaTypeCredential` (onLoad, Media Type & Credential Technology Registry)

**Where the user goes next**

- → `BO-334` Virtual Ticket Command Center: *Returns to the board's landing screen*; calls `listMediaTypeCredential`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The media type credential configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the media type credential untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No media type credential configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listMediaTypeTechnology` → `SCOPE_VIEW` (read) · staff
- `listMediaTypeCredential` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Media = any identifier a ticket is presented by (QR, RFID/wristband, facial recognition, other). Virtual ticket media IDs configurable by prefix, suffix and length; several media can link to one ticket (e.g. a season pass by face, QR or RFID as fallbacks). *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-608)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-337` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-337`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 6: Works in Media Type & Credential Technology Registry → Maintain the centralized catalogue of credential technologies supported by TICVAI. This makes the credential architecture extensible rather than hard-coded.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-337?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-334`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-338` Multi-Media Binding & Association Rules

**Configure how one Virtual Ticket can be associated with multiple media simultaneously. This is one of the most important screens in Area 15.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `ruleId` (navigation) |
| Route | `/access-venue/multi-media-binding-association-rules-bo-338` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Allowed media | select field | — | — | — | — | — | — |
| Mandatory media | select field | — | — | — | — | — | — |
| Optional media | select field | — | — | — | — | — | — |
| Maximum active media | select field | — | — | — | — | — | — |
| Minimum media required | select field | — | — | — | — | — | — |
| Primary media | select field | — | — | — | — | — | — |
| Secondary media | select field | — | — | — | — | — | — |
| Backup media | select field | — | — | — | — | — | — |
| Temporary media | select field | — | — | — | — | — | — |
| Media combination | select field | — | — | — | — | — | — |
| Simultaneous activation | select field | — | — | — | — | — | — |
| Exclusive activation | select field | — | — | — | — | — | — |

**Form: Save media binding rule** (modal, opened by *Save media binding rule*; *Save media binding rule* calls `setMediaBindingRule`, *Cancel* sends nothing)

**Collects what `setMediaBindingRule` sends before it is called.** Required: `id`, `scopePath`. Optional: `allowedMediaTypeIds`, `mandatoryMediaTypeIds`, `optionalMediaTypeIds`, `primaryMediaTypeId`, `secondaryMediaTypeIds`, `backupMediaTypeIds`, `temporaryMediaTypeIds`, `minimumMediaRequired`, `maximumActiveMedia`, `mediaCombinations`, `simultaneousActivation`, `exclusiveActivation` and 10 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setMediaBindingRule` body |
| Allowed media types `allowedMediaTypeIds` | multi-picker: choose allowed media types | optional | — | — | — | — | `setMediaBindingRule` body |
| Mandatory media types `mandatoryMediaTypeIds` | multi-picker: choose mandatory media types | optional | — | — | — | — | `setMediaBindingRule` body |
| Optional media types `optionalMediaTypeIds` | multi-picker: choose optional media types | optional | — | — | — | — | `setMediaBindingRule` body |
| Primary media type `primaryMediaTypeId` | picker: choose a primary media type | optional | — | — | shows names, sends the id | — | `setMediaBindingRule` body |
| Secondary media types `secondaryMediaTypeIds` | multi-picker: choose secondary media types | optional | — | — | — | — | `setMediaBindingRule` body |
| Backup media types `backupMediaTypeIds` | multi-picker: choose backup media types | optional | — | — | — | — | `setMediaBindingRule` body |
| Temporary media types `temporaryMediaTypeIds` | multi-picker: choose temporary media types | optional | — | — | — | — | `setMediaBindingRule` body |
| Minimum media required `minimumMediaRequired` | number field | optional | 0 | min 0 | — | — | `setMediaBindingRule` body |
| Maximum active media `maximumActiveMedia` | number field | optional | — | min 1 | — | — | `setMediaBindingRule` body |
| Media combinations `mediaCombinations` | list of values (chips) | optional | — | — | — | Permitted media combinations | `setMediaBindingRule` body |
| Simultaneous activation `simultaneousActivation` | list of values (chips) | optional | — | — | — | Media that may be active at the same time, e.g. | `setMediaBindingRule` body |
| Exclusive activation `exclusiveActivation` | list of values (chips) | optional | — | — | — | Media whose activation revokes another, e.g. | `setMediaBindingRule` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `setMediaBindingRule` body |
| Ticket type `ticketType` | text field | optional | — | max length 100 | — | — | `setMediaBindingRule` body |
| Event `eventId` | text field | optional | — | — | — | — | `setMediaBindingRule` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `setMediaBindingRule` body |
| Customer type `customerType` | text field | optional | — | max length 100 | — | — | `setMediaBindingRule` body |
| Membership `membership` | text field | optional | — | max length 100 | — | — | `setMediaBindingRule` body |
| Channel `channel` | text field | optional | — | max length 50 | — | — | `setMediaBindingRule` body |
| Age category `ageCategory` | text field | optional | — | max length 50 | — | — | `setMediaBindingRule` body |
| Country `country` | text field | optional | — | max length 2 | — | ISO 3166-1 alpha-2 | `setMediaBindingRule` body |
| Access environment `accessEnvironment` | text field | optional | — | max length 100 | — | — | `setMediaBindingRule` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node | `setMediaBindingRule` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 Minimum above maximum, or an unknown media type.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save media binding rule (primary button) | `setMediaBindingRule` PUT `/media-binding-rules` | AccessMediaBindingRule | AccessMediaBindingRule | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |
| Delete media binding rule (destructive button) | `deleteMediaBindingRule` DELETE `/media-binding-rules/{ruleId}` | — | — | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE` |

**Data it reads**: `listMultiMediaBinding` (onLoad, Multi-Media Binding & Association Rules)

**Where the user goes next**

- → `BO-334` Virtual Ticket Command Center: *Returns to the board's landing screen*; calls `listMultiMediaBinding`

**What opens over it**

- confirmDialog *Delete media binding rule*: **Names what `deleteMediaBindingRule` changes and what it leaves alone**, in the consequence rather than the verb. A record this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-media binding association configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-media binding association untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-media binding association configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 Minimum above maximum, or an unknown media type. |

#### Permissions

- `listMultiMediaBinding` → `SCOPE_VIEW` (read) · staff
- `setMediaBindingRule` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `deleteMediaBindingRule` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A ticket is always one virtual record; QR, RFID, NFC, face and future credentials (e.g. hotel room key, city transit card) are interchangeable media linked to it. Screens should show one ticket with its linked media, not separate tickets per medium. *(agreed · MoM 2 Sep 2026, 5. Key Decisions & Agreements · DI-652)*
- Media = any identifier a ticket is presented by (QR, RFID/wristband, facial recognition, other). Virtual ticket media IDs configurable by prefix, suffix and length; several media can link to one ticket (e.g. a season pass by face, QR or RFID as fallbacks). *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-608)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-338` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-338`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 8: Works in Multi-Media Binding & Association Rules → Configure how one Virtual Ticket can be associated with multiple media simultaneously. This is one of the most important screens in Area 15.

#### Acceptance for the design

- [ ] Every input above is drawn (36), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-338?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save media binding rule, Delete media binding rule.
- [ ] Every transition is wired: `BO-334`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-339` Credential Identity, Token & Reference Mapping

**Define how individual media identifiers resolve securely back to the authoritative Virtual Ticket.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/credential-identity-token-reference-mapping-bo-339` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Virtual ticket | text field | — | — | `listCredentialIdentityToken` ?virtualTicketId |
| Media type | text field | — | — | `listCredentialIdentityToken` ?mediaType |
| Credential reference | text field | — | — | `listCredentialIdentityToken` ?credentialReference |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Key references (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listCredentialIdentityToken` (onLoad, Credential Identity, Token & Reference Mapping)

**Where the user goes next**

- → `BO-334` Virtual Ticket Command Center: *Returns to the board's landing screen*; calls `listCredentialIdentityToken`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The credential identity token list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the credential identity token untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No credential identity token yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the credential identity token are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCredentialIdentityToken` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-339` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-339`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 10: Works in Credential Identity, Token & Reference Mapping → Define how individual media identifiers resolve securely back to the authoritative Virtual Ticket.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-339?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Key references.
- [ ] Every transition is wired: `BO-334`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-340` Entitlement & Cross-Media Synchronization Rules

**Ensure all media attached to a Virtual Ticket share the same authoritative ticket and entitlement state.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Detect) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/entitlement-cross-media-synchronization-rules-bo-340` |

#### Inputs: what the user enters or picks

**Form: Save credential event propagation rule** (modal, opened by *Save credential event propagation rule*; *Save credential event propagation rule* calls `setCredentialEventPropagationRule`, *Cancel* sends nothing)

**Collects what `setCredentialEventPropagationRule` sends before it is called.** Required: `id`, `triggerEvent`, `scopePath`. Optional: `revocationAction`, `propagationTargets`, `monitoredConditions`, `propagation`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setCredentialEventPropagationRule` body |
| Trigger event `triggerEvent` | select | required | — | Entry · Exit · Redemption · Partial consumption · Cancellation · Refund · Suspension · Reactivation · Transfer · Exchange · Upgrade · Reissue … | — | Unique per scope; one vocabulary for both screens that read it (decided 29 September, writers pass) | `setCredentialEventPropagationRule` body |
| Revocation action `revocationAction` | segmented control | optional | — | Invalidate · Suspend · Replace | — | What happens to the credential; refund, exchange and reissue always revoke | `setCredentialEventPropagationRule` body |
| Propagation targets `propagationTargets` | multi-select chips | optional | — | Central platform · Mobile app · Gate network · Offline revocation package · Wallet credential service | — | — | `setCredentialEventPropagationRule` body |
| Monitored conditions `monitoredConditions` | multi-select chips | optional | — | Delayed updates · Conflicting states · Offline transactions pending synchronization · Provider update failures · Stale wallet credentials | — | — | `setCredentialEventPropagationRule` body |
| Propagation `propagation` | text area | optional | — | max length 500 | — | How the Virtual Ticket state change reaches every bound medium | `setCredentialEventPropagationRule` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node | `setCredentialEventPropagationRule` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Every entitlement cross-media synchronization** (data table, from `listEntitlementCrossMedia`)

| Shows | Format | Notes |
|---|---|---|
| Monitored conditions | list or chips (count when long) | Synchronisation problems detected and alerted |

**The selected entitlement cross-media synchronization** (detail panel): The pack groups this record's detail under its own headings: “Critical Principle”, “For example, TICVAI must prevent”, “Instead”, “Face Credential”, “Virtual Ticket resolved”, “Access transaction recorded”.

| Shows | Format | Notes |
|---|---|---|
| Monitored conditions | list or chips (count when long) | Synchronisation problems detected and alerted |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save credential event propagation rule (primary button) | `setCredentialEventPropagationRule` PUT `/credential-event-propagation-rules` | AccessCredentialEventPropagationRule | AccessCredentialEventPropagationRule | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | gated `ACCESS_POINT_CONFIGURE`; opens modal first; produces a document or message: Set how a ticket lifecycle event propagates to the credential |

**Data it reads**: `listEntitlementCrossMedia` (onLoad, Entitlement & Cross-Media Synchronization Rules)

**Where the user goes next**

- → `BO-334` Virtual Ticket Command Center: *Returns to the board's landing screen*; calls `listEntitlementCrossMedia`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The entitlement cross-media synchronization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the entitlement cross-media synchronization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No entitlement cross-media synchronization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the entitlement cross-media synchronization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listEntitlementCrossMedia` → `SCOPE_VIEW` (read) · staff
- `setCredentialEventPropagationRule` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-340` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-340`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 12: Works in Entitlement & Cross-Media Synchronization Rules → Ensure all media attached to a Virtual Ticket share the same authoritative ticket and entitlement state.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-340?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save credential event propagation rule.
- [ ] Every transition is wired: `BO-334`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-341` Media Activation, Priority & Fallback Rules

**Configure when each credential becomes active and how alternative media behave if the preferred credential cannot be used.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/media-activation-priority-fallback-rules-bo-341` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Temporary media | select field | — | — | — | — | — | — |
| Validity duration | select field | — | — | — | — | — | — |
| One-time use | select field | — | — | — | — | — | — |
| Automatic expiration | select field | — | — | — | — | — | — |
| Replacement behavior | select field | — | — | — | — | — | — |
| Original-media impact | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| On ticket activation (primary button) | navigation or local | — | — | — | — |
| On download (secondary button) | navigation or local | — | — | — | — |
| On wallet installation (secondary button) | navigation or local | — | — | — | — |
| On event date (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listMediaActivationPriority` (onLoad, Media Activation, Priority & Fallback Rules)

**Where the user goes next**

- → `BO-334` Virtual Ticket Command Center: *Returns to the board's landing screen*; calls `listMediaActivationPriority`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The media activation priority configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the media activation priority untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No media activation priority configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listMediaActivationPriority` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Media = any identifier a ticket is presented by (QR, RFID/wristband, facial recognition, other). Virtual ticket media IDs configurable by prefix, suffix and length; several media can link to one ticket (e.g. a season pass by face, QR or RFID as fallbacks). *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-608)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-341` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-341`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 14: Works in Media Activation, Priority & Fallback Rules → Configure when each credential becomes active and how alternative media behave if the preferred credential cannot be used.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-341?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: On ticket activation, On download, On wallet installation, On event date.
- [ ] Every transition is wired: `BO-334`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-342` Media Replacement, Revocation & Rebinding Rules

**Configure controlled handling of lost, stolen, damaged, compromised or replaced credential media.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/media-replacement-revocation-rebinding-rules-bo-342` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Reissue allowed | select field | — | — | — | — | — | — |
| Number of replacements | select field | — | — | — | — | — | — |
| Replacement fee reference | select field | — | — | — | — | — | — |
| Approval required | select field | — | — | — | — | — | — |
| Identity verification | select field | — | — | — | — | — | — |
| Old media automatically revoked | text field | — | — | — | — | — | — |
| Grace period | select field | — | — | — | — | — | — |
| Simultaneous media policy | select field | — | — | — | — | — | — |
| Reason mandatory | select field | — | — | — | — | — | — |
| Supervisor approval | select field | — | — | — | — | — | — |

**Sent by *Save replacement rule*** (`setMediaReplacementRevocation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Replacement reason `replacementReason` | select | required | — | Lost · Stolen · Damaged · Compromised · Customer changed phone · RFID failure · Wristband replacement · QR compromise · Wallet replacement · Face re enrollment · Incorrect assignment | — | The reason this rule is for, in the vocabulary of `replaceCredential`, so the rule a replacement reads is keyed the way the replacement names it (decided 29 September, writers … | `setMediaReplacementRevocation` body |
| Outcome `outcome` | radio group | required | — | Replace · Rebind · Suspend media · Revoke media | — | What happens to the media | `setMediaReplacementRevocation` body |
| Number of replacements `numberOfReplacements` | number field | optional | — | min 0 | — | Maximum replacements per credential | `setMediaReplacementRevocation` body |
| Replacement fee reference `replacementFeeReference` | text field | optional | — | — | — | Catalogue product charged for the replacement; empty is free | `setMediaReplacementRevocation` body |
| Approval required `approvalRequired` | toggle | optional | off | — | — | — | `setMediaReplacementRevocation` body |
| Supervisor approval `supervisorApproval` | toggle | optional | off | — | — | — | `setMediaReplacementRevocation` body |
| Identity verification `identityVerification` | toggle | optional | on | — | — | — | `setMediaReplacementRevocation` body |
| Old media automatically revoked `oldMediaAutomaticallyRevoked` | toggle | optional | on | — | — | — | `setMediaReplacementRevocation` body |
| Grace period `gracePeriod` | text field | optional | — | — | — | ISO 8601 duration the old media stays valid; empty is none | `setMediaReplacementRevocation` body |
| Simultaneous media policy `simultaneousMediaPolicy` | segmented control | optional | One active | One active · Allow both during grace | — | — | `setMediaReplacementRevocation` body |
| Reason mandatory `reasonMandatory` | toggle | optional | on | — | — | — | `setMediaReplacementRevocation` body |
| Reissue allowed `reissueAllowed` | toggle | optional | on | — | — | — | `setMediaReplacementRevocation` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Wallet credential replacement (primary button) | navigation or local | — | — | — | — |
| Printed ticket replacement (secondary button) | navigation or local | — | — | — | — |
| Suspend Media (destructive button) | navigation or local | — | — | — | — |
| Revoke Media (destructive button) | navigation or local | — | — | — | — |
| Replace Media (secondary button) | navigation or local | — | — | — | — |
| Save replacement rule (primary button) | `setMediaReplacementRevocation` PUT `/media-replacement-revocation` | MediaReplacementRevocationRebindingRulesInput | MediaReplacementRevocationRebindingRulesView | 422 replacementFeeReference names no catalogue product | — |

**Data it reads**: `listMediaReplacementRevocation` (onLoad, Media Replacement, Revocation & Rebinding Rules)

**Where the user goes next**

- → `BO-334` Virtual Ticket Command Center: *Returns to the board's landing screen*; calls `listMediaReplacementRevocation`

**What opens over it**

- confirmDialog *Suspend Media*: **Suspend Media on a media replacement revocation is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *Revoke Media*: **Revoke Media on a media replacement revocation is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The media replacement revocation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the media replacement revocation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No media replacement revocation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 replacementFeeReference names no catalogue product |

#### Permissions

- `listMediaReplacementRevocation` → `SCOPE_VIEW` (read) · staff
- `setMediaReplacementRevocation` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-342` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-342`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 16: Works in Media Replacement, Revocation & Rebinding Rules → Configure controlled handling of lost, stolen, damaged, compromised or replaced credential media.

#### Acceptance for the design

- [ ] Every input above is drawn (22), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-342?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Wallet credential replacement, Printed ticket replacement, Suspend Media, Revoke Media, Replace Media, Save replacement rule.
- [ ] Every transition is wired: `BO-334`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-343` Virtual Ticket Architecture Testing, Governance & Audit

**Provide the final testing and governance environment for Virtual Ticket and multi-media configurations. Board 1 established what the Virtual Ticket is and how multiple credentials can point to the same authoritative ticket. Board 2 defines how each media type is created, designed, configured, branded, populated with data, previewed, tested and published.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AUDIT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration Simulator; Configuration Owner; AI Configuration Review) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/virtual-ticket-architecture-testing-governance-audit-bo-343` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| → Technical Review | select field | — | — | — | — | — | — |
| → Security Review where applicable | text field | — | — | — | — | — | — |
| → Operations Review | select field | — | — | — | — | — | — |
| → Approval | select field | — | — | — | — | — | — |
| → Publication | select field | — | — | — | — | — | — |
| configured lost-credential security policy.” | text field | — | — | — | — | — | — |
| Replacement/Rebinding → Test & Govern | text field | — | — | — | — | — | — |
| Multi-Format Ticket Media Design Studio—including dedicated design/configuration | text field | — | — | — | — | — | — |
| Preview → Validate → Approve & Publish | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Change type | text field | — | — | `listVirtualTicketArchitecture` ?changeType |

#### Outputs: what the screen shows and produces

**Data it reads**: `listVirtualTicketArchitecture` (onLoad, Virtual Ticket Architecture Testing, Governance & Audit)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The virtual ticket architecture configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the virtual ticket architecture untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No virtual ticket architecture configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listVirtualTicketArchitecture` → `AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-343` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS165 Ticket Media   Credential Management Board 1.dc.html#bo-343`
- Workshop pack: Ticket_Media___Credential_Management_Reference.pdf board 1
- Flow F168 *Ticket Media Credential Management board 1: Virtual Ticket Command Center*, step 18: Works in Virtual Ticket Architecture Testing, Governance & Audit → Provide the final testing and governance environment for Virtual Ticket and multi-media configurations. Board 1 established what the Virtual Ticket is and how multiple credentials can point to the …

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-343?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
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

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"deleteMediaBindingRule": {"method":"DELETE","path":"/media-binding-rules/{ruleId}","contract":"access","summary":"Delete a multi-media binding rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listCredentialIdentityToken": {"method":"GET","path":"/credential-identity-token","contract":"access","summary":"Credential Identity, Token & Reference Mapping","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"virtualTicketId","in":"query","required":false},{"name":"mediaType","in":"query","required":false},{"name":"credentialReference","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listEntitlementCrossMedia": {"method":"GET","path":"/entitlement-cross-media","contract":"access","summary":"Entitlement & Cross-Media Synchronization Rules","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"EntitlementCrossMediaSynchronizationRulesView"},
"listMediaActivationPriority": {"method":"GET","path":"/media-activation-priority","contract":"access","summary":"Media Activation, Priority & Fallback Rules","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaActivationPriorityFallbackRulesView"},
"listMediaReplacementRevocation": {"method":"GET","path":"/media-replacement-revocation","contract":"access","summary":"Media Replacement, Revocation & Rebinding Rules","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaReplacementRevocationRebindingRulesView"},
"listMediaTypeCredential": {"method":"GET","path":"/media-type-credential","contract":"access","summary":"Media Type & Credential Technology Registry","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaTypeCredentialTechnologyRegistryView"},
"listMediaTypeTechnology": {"method":"GET","path":"/media-type-technology","contract":"access","summary":"Media Type & Technology Library","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaTypeTechnologyLibraryView"},
"listMultiMediaBinding": {"method":"GET","path":"/multi-media-binding","contract":"access","summary":"Multi-Media Binding & Association Rules","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MultiMediaBindingAssociationRulesView"},
"listVirtualTicket": {"method":"GET","path":"/virtual-ticket","contract":"access","summary":"Virtual Ticket Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"brand","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"performance","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"customer","in":"query","required":false},{"name":"virtualTicketStatus","in":"query","required":false},{"name":"mediaType","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"ticketType","in":"query","required":false},{"name":"numberOfMedia","in":"query","required":false},{"name":"validity","in":"query","required":false},{"name":"usageStatus","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVirtualTicketArchitecture": {"method":"GET","path":"/virtual-ticket-architecture","contract":"access","summary":"Virtual Ticket Architecture Testing, Governance & Audit","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"changeType","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVirtualTicketStatus": {"method":"GET","path":"/virtual-ticket-statu","contract":"access","summary":"Virtual Ticket Status & Lifecycle Model","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"VirtualTicketStatusLifecycleModelView"},
"setCredentialEventPropagationRule": {"method":"PUT","path":"/credential-event-propagation-rules","contract":"access","summary":"Set how a ticket lifecycle event propagates to the credential","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessCredentialEventPropagationRule","responds":"AccessCredentialEventPropagationRule"},
"setMediaBindingRule": {"method":"PUT","path":"/media-binding-rules","contract":"access","summary":"Create or replace a multi-media binding rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessMediaBindingRule","responds":"AccessMediaBindingRule"},
"setMediaReplacementRevocation": {"method":"PUT","path":"/media-replacement-revocation","contract":"access","summary":"Save a media replacement rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MediaReplacementRevocationRebindingRulesInput","responds":"MediaReplacementRevocationRebindingRulesView"},
"setTicketStatusTransition": {"method":"PUT","path":"/ticket-status-transitions","contract":"access","summary":"Set a Virtual Ticket status transition rule","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessTicketStatusTransition","responds":"AccessTicketStatusTransition"},
"setVirtualTicketIdentity": {"method":"PUT","path":"/virtual-ticket-identity","contract":"access","summary":"Virtual Ticket Identity & Master Record Configuration","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VirtualTicketIdentityMasterRecordConfigurationInput","responds":"VirtualTicketIdentityMasterRecordConfigurationView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessCredentialEventPropagationRule": {"type":"object","x-ticvai-persistence":"access.credential_event_propagation_rule","description":"For one ticket lifecycle event, the revocation action on the credential and how the change propagates to every bound medium, with the conditions monitored (declared 29 September, data-model close-out DM1).","required":["id","triggerEvent","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"triggerEvent":{"type":"string","enum":["entry","exit","redemption","partialConsumption","cancellation","refund","suspension","reactivation","transfer","exchange","upgrade","reissue","expiry","replacement","manualInvalidation","fraudLock","accountSuspension"],"description":"Unique per scope; one vocabulary for both screens that read it (decided 29 September, writers pass)"},"revocationAction":{"type":"string","nullable":true,"enum":["invalidate","suspend","replace"],"description":"What happens to the credential; refund, exchange and reissue always revoke"},"propagationTargets":{"type":"array","items":{"type":"string","enum":["centralPlatform","mobileApp","gateNetwork","offlineRevocationPackage","walletCredentialService"]}},"monitoredConditions":{"type":"array","items":{"type":"string","enum":["delayedUpdates","conflictingStates","offlineTransactionsPendingSynchronization","providerUpdateFailures","staleWalletCredentials"]}},"propagation":{"type":"string","maxLength":500,"nullable":true,"description":"How the Virtual Ticket state change reaches every bound medium"},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessMediaBindingRule": {"type":"object","x-ticvai-persistence":"access.media_binding_rule","description":"One multi-media binding rule - which media a Virtual Ticket may, must or may optionally carry, in which roles and combinations - for the scope named by its conditions (declared 29 September, data-model close-out DM1).","required":["id","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"allowedMediaTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"mandatoryMediaTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"optionalMediaTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"primaryMediaTypeId":{"type":"string","format":"uuid","nullable":true},"secondaryMediaTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"backupMediaTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"temporaryMediaTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"minimumMediaRequired":{"type":"integer","minimum":0,"default":0},"maximumActiveMedia":{"type":"integer","minimum":1,"nullable":true},"mediaCombinations":{"type":"array","items":{"type":"string"},"description":"Permitted media combinations"},"simultaneousActivation":{"type":"array","items":{"type":"string"},"description":"Media that may be active at the same time, e.g. face with RFID"},"exclusiveActivation":{"type":"array","items":{"type":"string"},"description":"Media whose activation revokes another, e.g. RFID activated revokes temporary paper"},"productId":{"type":"string","format":"uuid","nullable":true},"ticketType":{"type":"string","maxLength":100,"nullable":true},"eventId":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"customerType":{"type":"string","maxLength":100,"nullable":true},"membership":{"type":"string","maxLength":100,"nullable":true},"channel":{"type":"string","maxLength":50,"nullable":true},"ageCategory":{"type":"string","maxLength":50,"nullable":true},"country":{"type":"string","maxLength":2,"nullable":true,"description":"ISO 3166-1 alpha-2"},"accessEnvironment":{"type":"string","maxLength":100,"nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessTicketStatusTransition": {"type":"object","x-ticvai-persistence":"access.ticket_status_transition","description":"One Virtual Ticket lifecycle transition rule - from status, to status, whether allowed, whether it needs an authorised exception and where it may originate (declared 29 September, data-model close-out DM1). Seeded from states/entitlement-status.yaml when a venue is created; setTicketStatusTransition may narrow a move, never add one (decided 29 September, writers pass).","required":["id","fromStatus","toStatus","allowed","requiresAuthorizedException","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"fromStatus":{"type":"string","enum":["created","pendingFulfillment","active","partiallyUsed","used","expired","suspended","cancelled","voided","reissuedSuperseded","refunded","transferred","blocked"]},"toStatus":{"type":"string","enum":["created","pendingFulfillment","active","partiallyUsed","used","expired","suspended","cancelled","voided","reissuedSuperseded","refunded","transferred","blocked"],"description":"Unique with fromStatus per scope"},"allowed":{"type":"boolean"},"requiresAuthorizedException":{"type":"boolean","default":false,"description":"Allowed only with an authorised exception, e.g. used to active"},"originatingSources":{"type":"array","items":{"type":"string","enum":["orderManagement","cancellation","refund","upgradeConversion","ticketTransfer","membership","expiry","accessUsage","authorizedOperator","api","scheduledProcess"]}},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CredentialIdentityTokenReferenceMappingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Identity, Token & Reference Mapping displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"credentialBindingId":{"type":"string","description":"Credential Binding ID"},"virtualTicketId":{"type":"string","description":"Virtual Ticket ID"},"mediaType":{"type":"string","description":"Media Type"},"credentialReference":{"type":"string","description":"Credential Reference"},"tokenIdentifier":{"type":"string","description":"Token or identifier, masked in administrative views"},"providerReference":{"type":"string","description":"Provider Reference"},"issuedDate":{"type":"string","format":"date-time","description":"Issued Date"},"activationDate":{"type":"string","format":"date-time","description":"Activation Date"},"expiry":{"type":"string","format":"date-time","description":"Expiry"},"status":{"type":"string","enum":["pending","active","suspended","revoked","expired"],"description":"Credential binding status"},"version":{"type":"string","description":"Version"},"securityProfile":{"type":"string","description":"Security profile"},"protectionMethods":{"type":"array","items":{"type":"string","enum":["tokenization","hashing","encryption","signedPayloads","keyReferences","masking"]},"description":"How the credential value is protected"}},"required":["credentialBindingId","virtualTicketId","mediaType"]},
"EntitlementCrossMediaSynchronizationRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Entitlement & Cross-Media Synchronization Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"triggerEvent":{"type":"string","enum":["entry","exit","redemption","partialConsumption","cancellation","refund","suspension","reactivation","transfer","upgrade","expiry","replacement"],"description":"Ticket event this synchronisation rule handles"},"monitoredConditions":{"type":"array","items":{"type":"string","enum":["delayedUpdates","conflictingStates","offlineTransactionsPendingSynchronization","providerUpdateFailures","staleWalletCredentials"]},"description":"Synchronisation problems detected and alerted"},"propagation":{"type":"string","description":"How the Virtual Ticket state change reaches every bound medium"}},"required":["triggerEvent"]},
"MediaActivationPriorityFallbackRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Media Activation, Priority & Fallback Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"mediaTypeId":{"type":"string","description":"Media type this rule applies to"},"activationTrigger":{"type":"string","enum":["immediateOnIssuance","onTicketActivation","onDownload","onWalletInstallation","onRfidAssignment","onFaceEnrollment","onFirstUse","onEventDate","manualActivation","scheduledActivation"],"description":"When this medium becomes active"},"temporaryMedia":{"type":"boolean","description":"Temporary media"},"validityDuration":{"type":"string","description":"ISO 8601 duration, e.g. PT30M"},"oneTimeUse":{"type":"boolean","description":"One-time use"},"automaticExpiration":{"type":"boolean","description":"Automatic expiration"},"replacementBehavior":{"type":"string","description":"Replacement behavior"},"originalMediaImpact":{"type":"string","description":"Original-media impact"},"fallbackMediaTypes":{"type":"array","items":{"type":"string"},"description":"Ordered media to use if this one cannot be used, e.g. face unavailable then RFID"}},"required":["mediaTypeId","activationTrigger"]},
"MediaReplacementRevocationRebindingRulesInput": {"type":"object","x-ticvai-persistence":"none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)","description":"**What Media Replacement, Revocation & Rebinding Rules submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.","required":["replacementReason","outcome"],"properties":{"replacementReason":{"type":"string","enum":["lost","stolen","damaged","compromised","customerChangedPhone","rfidFailure","wristbandReplacement","qrCompromise","walletReplacement","faceReEnrollment","incorrectAssignment"],"description":"The reason this rule is for, in the vocabulary of `replaceCredential`, so the rule a replacement reads is keyed the way the replacement names it (decided 29 September, writers pass). The old keys map: lostRfidCard to lost or rfidFailure, damagedWristband to wristbandReplacement, compromisedQr to qrCompromise, newMobileDevice to customerChangedPhone, walletCredentialReplacement to walletReplacement, faceReEnrollment unchanged, printedTicketReplacement to damaged, incorrectCredentialAssignment to incorrectAssignment."},"outcome":{"type":"string","enum":["replace","rebind","suspendMedia","revokeMedia"],"description":"What happens to the media"},"numberOfReplacements":{"type":"integer","minimum":0,"description":"Maximum replacements per credential"},"replacementFeeReference":{"type":"string","description":"Catalogue product charged for the replacement; empty is free"},"approvalRequired":{"type":"boolean","default":false},"supervisorApproval":{"type":"boolean","default":false},"identityVerification":{"type":"boolean","default":true},"oldMediaAutomaticallyRevoked":{"type":"boolean","default":true},"gracePeriod":{"type":"string","description":"ISO 8601 duration the old media stays valid; empty is none"},"simultaneousMediaPolicy":{"type":"string","enum":["oneActive","allowBothDuringGrace"],"default":"oneActive"},"reasonMandatory":{"type":"boolean","default":true},"reissueAllowed":{"type":"boolean","default":true}}},
"MediaReplacementRevocationRebindingRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Media Replacement, Revocation & Rebinding Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"outcome":{"type":"string","enum":["replace","rebind","suspendMedia","revokeMedia"],"description":"What happens to the media (decided 29 September, VM close-out)"},"replacementReason":{"type":"string","enum":["lost","stolen","damaged","compromised","customerChangedPhone","rfidFailure","wristbandReplacement","qrCompromise","walletReplacement","faceReEnrollment","incorrectAssignment"],"description":"The reason this rule is for, in the vocabulary of `replaceCredential`, so the rule a replacement reads is keyed the way the replacement names it (decided 29 September, writers pass). The old keys map: lostRfidCard to lost or rfidFailure, damagedWristband to wristbandReplacement, compromisedQr to qrCompromise, newMobileDevice to customerChangedPhone, walletCredentialReplacement to walletReplacement, faceReEnrollment unchanged, printedTicketReplacement to damaged, incorrectCredentialAssignment to incorrectAssignment."},"numberOfReplacements":{"type":"integer","description":"Number of replacements"},"replacementFeeReference":{"type":"string","description":"Reference to a fee in pricing configuration; no amount is held here"},"approvalRequired":{"type":"boolean","description":"Approval required"},"identityVerification":{"type":"boolean","description":"Identity verification"},"oldMediaAutomaticallyRevoked":{"type":"boolean","description":"Old media automatically revoked"},"gracePeriod":{"type":"string","description":"ISO 8601 duration, e.g. PT30M"},"simultaneousMediaPolicy":{"type":"string","description":"Simultaneous media policy"},"reasonMandatory":{"type":"boolean","description":"Reason mandatory"},"supervisorApproval":{"type":"boolean","description":"Supervisor approval"},"reissueAllowed":{"type":"boolean","description":"Reissue allowed"}},"required":["replacementReason"]},
"MediaTypeCredentialTechnologyRegistryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Media Type & Credential Technology Registry displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"mediaTypeId":{"type":"string","description":"Media Type ID"},"name":{"type":"string","description":"Name"},"category":{"type":"string","enum":["digital","physical","biometric","future"],"description":"Media category"},"provider":{"type":"array","items":{"type":"string"},"description":"Provider integrations that implement this media type (media type is not the vendor)"},"technology":{"type":"string","description":"Technology"},"tokenFormat":{"type":"string","description":"Token format"},"generationMethod":{"type":"string","description":"Generation method"},"validationMechanism":{"type":"string","description":"Validation mechanism"},"supportsVisualDesign":{"type":"boolean","description":"Supports visual design"},"supportsDynamicUpdate":{"type":"boolean","description":"Supports dynamic update"},"supportsRevocation":{"type":"boolean","description":"Supports revocation"},"supportsExpiration":{"type":"boolean","description":"Supports expiration"},"supportsOfflineReference":{"type":"boolean","description":"Supports offline reference"},"supportsReplacement":{"type":"boolean","description":"Supports replacement"},"supportsEncryption":{"type":"boolean","description":"Supports encryption"},"supportsSigning":{"type":"boolean","description":"Supports signing"},"supportedChannels":{"type":"array","items":{"type":"string"},"description":"Supported channels"},"supportedDevices":{"type":"array","items":{"type":"string"},"description":"Supported devices"},"integrationAdapter":{"type":"string","description":"Integration adapter"}},"required":["mediaTypeId","name","category"]},
"MediaTypeTechnologyLibraryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Media Type & Technology Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"active":{"type":"boolean","description":"False once retired through `setMediaTypeTechnology`; issued credentials stay valid (decided 29 September, VM close-out)"},"mediaType":{"type":"string","enum":["linearBarcode","twoDimensionalBarcode","qr","rfidContact","rfidProximity","rfidIso15693","rfidOtherStandard","appCredential","mobileWallet","paperTicket","wristband","plasticCard","hotelCard","facePass","faceTag","partnerQr","externalBarcode","thirdPartyCredential"],"description":"The kind of medium this profile defines"},"technology":{"type":"string","enum":["barcode","rfid","nfc","magneticStripe","mobile","physical","biometric","external"],"description":"Technology family"},"encodingFormat":{"type":"string","description":"encoding format"},"supportedReaderTypes":{"type":"array","items":{"type":"string"},"description":"supported reader types"},"onlineOfflineCapability":{"type":"string","enum":["onlineOnly","offlineOnly","onlineAndOffline"],"description":"online/offline capability"},"writableReadOnly":{"type":"string","enum":["writable","readOnly"],"description":"writable/read-only"},"securityClassification":{"type":"string","description":"security classification"},"applicableVenues":{"type":"array","items":{"type":"string"},"description":"Venue ids"},"applicableProducts":{"type":"array","items":{"type":"string"},"description":"Product ids"},"mediaTypeId":{"type":"string","description":"Media type profile identifier"},"name":{"type":"string","description":"Profile name"}}},
"MultiMediaBindingAssociationRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Multi-Media Binding & Association Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleId":{"type":"string","description":"Binding rule ID"},"allowedMedia":{"type":"array","items":{"type":"string"},"description":"Media type IDs allowed"},"mandatoryMedia":{"type":"array","items":{"type":"string"},"description":"Media type IDs required"},"optionalMedia":{"type":"array","items":{"type":"string"},"description":"Media type IDs optional"},"maximumActiveMedia":{"type":"integer","description":"Maximum active media"},"minimumMediaRequired":{"type":"integer","description":"Minimum media required"},"primaryMedia":{"type":"string","description":"Primary media"},"secondaryMedia":{"type":"array","items":{"type":"string"},"description":"Secondary media"},"backupMedia":{"type":"array","items":{"type":"string"},"description":"Backup media"},"temporaryMedia":{"type":"array","items":{"type":"string"},"description":"Temporary media"},"mediaCombination":{"type":"array","items":{"type":"string"},"description":"Permitted media combinations"},"simultaneousActivation":{"type":"array","items":{"type":"string"},"description":"Media that may be active at the same time, e.g. face with RFID"},"exclusiveActivation":{"type":"array","items":{"type":"string"},"description":"Media whose activation revokes another, e.g. RFID activated revokes temporary paper"},"product":{"type":"string","description":"Product"},"ticketType":{"type":"string","description":"Ticket Type"},"event":{"type":"string","description":"Event"},"venue":{"type":"string","description":"Venue"},"customerType":{"type":"string","description":"Customer Type"},"membership":{"type":"string","description":"Membership"},"channel":{"type":"string","description":"Channel"},"age":{"type":"string","description":"Age"},"country":{"type":"string","description":"Country"},"accessEnvironment":{"type":"string","description":"Access environment"}},"required":["ruleId"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"VirtualTicketArchitectureTestingGovernanceAuditView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Virtual Ticket Architecture Testing, Governance & Audit displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"changeType":{"type":"string","enum":["configurationChange","mediaBinding","rebinding","activation","suspension","revocation","replacement","resolverChange","ruleChange","approval"],"description":"What kind of change was recorded"},"actor":{"type":"string","description":"Actor"},"timestamp":{"type":"string","format":"date-time","description":"Timestamp"},"before":{"type":"string","description":"State before the change"},"after":{"type":"string","description":"State after the change"}}},
"VirtualTicketCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Virtual Ticket Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"virtualTicketId":{"type":"string","description":"Virtual Ticket ID"},"product":{"type":"string","description":"Product"},"eventPerformance":{"type":"string","description":"Event / Performance"},"ticketHolder":{"type":"string","description":"Ticket Holder"},"orderReference":{"type":"string","description":"Order Reference"},"ticketType":{"type":"string","description":"Ticket Type"},"seatResourceWhereApplicable":{"type":"string","description":"Seat / Resource where applicable"},"ticketStatus":{"type":"string","enum":["created","pendingFulfillment","active","partiallyUsed","used","expired","suspended","cancelled","voided","reissuedSuperseded","refunded","transferred","blocked"],"description":"Virtual Ticket status (lifecycle 15.1.3)"},"usageStatus":{"type":"string","enum":["unused","partiallyUsed","used"],"description":"How much of the entitlement is consumed"},"numberOfLinkedMedia":{"type":"integer","description":"Number of Linked Media"},"primaryMedia":{"type":"string","description":"Primary Media"},"lastCredentialActivity":{"type":"string","format":"date-time","description":"Last Credential Activity"},"lastModified":{"type":"string","format":"date-time","description":"Last Modified"},"validFrom":{"type":"string","format":"date-time","description":"Valid from"},"validTo":{"type":"string","format":"date-time","description":"Valid to"}}},
"VirtualTicketCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"totalVirtualTickets":{"type":"integer","description":"Total Virtual Tickets"},"active":{"type":"integer","description":"Active"},"pendingActivation":{"type":"integer","description":"Pending Activation"},"suspended":{"type":"integer","description":"Suspended"},"usedConsumed":{"type":"integer","description":"Used / Consumed"},"partiallyConsumed":{"type":"integer","description":"Partially Consumed"},"expired":{"type":"integer","description":"Expired"},"cancelled":{"type":"integer","description":"Cancelled"},"revoked":{"type":"integer","description":"Revoked"},"virtualTicketsWithMultipleMedia":{"type":"integer","description":"Virtual Tickets with Multiple Media"},"virtualTicketsWithNoActiveMedia":{"type":"integer","description":"Virtual Tickets with No Active Media"},"mediaBindingExceptions":{"type":"integer","description":"Media Binding Exceptions"},"credentialSynchronizationIssues":{"type":"integer","description":"Credential Synchronization Issues"}}},
"VirtualTicketIdentityMasterRecordConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Virtual Ticket Identity & Master Record Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"venueId":{"type":"string","description":"Venue this configuration applies to"},"idGenerationPattern":{"type":"string","description":"Virtual Ticket ID format: prefix, suffix and length"},"ticketClassification":{"type":"string","description":"Ticket classification"},"ticketOwnershipModel":{"type":"string","description":"Ticket ownership model"},"holderAssignmentRequirements":{"type":"string","description":"Holder assignment requirements"},"transferabilityReference":{"type":"string","description":"Transferability reference"},"validityModel":{"type":"string","description":"Validity model"},"consumptionModel":{"type":"string","description":"Consumption model"},"entitlementModel":{"type":"string","description":"Entitlement model"},"mediaRequirements":{"type":"array","items":{"type":"string"},"description":"Media types a ticket of this configuration must carry"}},"required":["venueId"]},
"VirtualTicketIdentityMasterRecordConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Virtual Ticket Identity & Master Record Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venueId":{"type":"string","description":"Venue this configuration applies to"},"idGenerationPattern":{"type":"string","description":"Virtual Ticket ID format: prefix, suffix and length"},"ticketClassification":{"type":"string","description":"Ticket classification"},"ticketOwnershipModel":{"type":"string","description":"Ticket ownership model"},"holderAssignmentRequirements":{"type":"string","description":"Holder assignment requirements"},"transferabilityReference":{"type":"string","description":"Transferability reference"},"validityModel":{"type":"string","description":"Validity model"},"consumptionModel":{"type":"string","description":"Consumption model"},"entitlementModel":{"type":"string","description":"Entitlement model"},"mediaRequirements":{"type":"array","items":{"type":"string"},"description":"Media types a ticket of this configuration must carry"}},"required":["venueId"]},
"VirtualTicketStatusLifecycleModelView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Virtual Ticket Status & Lifecycle Model displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"fromStatus":{"type":"string","enum":["created","pendingFulfillment","active","partiallyUsed","used","expired","suspended","cancelled","voided","reissuedSuperseded","refunded","transferred","blocked"],"description":"Status the transition starts from"},"toStatus":{"type":"string","enum":["created","pendingFulfillment","active","partiallyUsed","used","expired","suspended","cancelled","voided","reissuedSuperseded","refunded","transferred","blocked"],"description":"Status the transition leads to"},"originatingSources":{"type":"array","items":{"type":"string","enum":["orderManagement","cancellation","refund","upgradeConversion","ticketTransfer","membership","expiry","accessUsage","authorizedOperator","api","scheduledProcess"]},"description":"Where this transition may originate"},"allowed":{"type":"boolean","description":"Whether the transition is allowed"},"requiresAuthorizedException":{"type":"boolean","description":"Allowed only with an authorised exception, e.g. Used to Active"}},"required":["fromStatus","toStatus"]}
}
```
