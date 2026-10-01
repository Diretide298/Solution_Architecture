# WS27 — Group Sales   Corporate Booking Management board 1

**10 screens · 15 operations · 22 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, PRODUCT_CONFIGURE`. A control nobody can use must say so,
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
| `BO-264` | Group Sales Command Center | B–D | 0 | 24 | 6 | 0 | 3 | 0 | — | notStarted (generated) |
| `BO-265` | Group Enquiry & Opportunity Capture | B–D | 42 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-266` | Group Customer & Organization Profile | B–D | 15 | 16 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-267` | Group Requirements, Availability & Capacity Planner | B–D | 0 | 14 | 6 | 0 | 0 | 1 | — | notStarted (generated) |
| `BO-268` | Group Package & Experience Builder | B–D | 0 | 18 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-269` | Group Quotation Builder & Proposal Generation | B–D | 11 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-270` | Quote Revision, Negotiation & Version Management | B–D | 8 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-271` | Group Discount, Exception & Approval Workflow | B–D | 0 | 0 | 6 | 0 | 1 | 3 | — | notStarted (generated) |
| `BO-272` | Quote-to-Booking Conversion & Confirmation | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-273` | Group Booking 360° & Handover Workspace | B–D | 0 | 54 | 6 | 0 | 1 | 6 | — | notStarted (generated) |

## Thin screens in this batch

**BO-267, BO-271, BO-272, BO-273 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-264` Group Sales Command Center

**Provide the Group Sales team with a centralized commercial workspace showing the entire group-sales pipeline.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display; Show) and a per-row directory (§Each opportunity should display) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/group-sales-command-center-bo-264` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Customer type | text field | — | — | `listGroupSale2` ?customerType |
| Organization | text field | — | — | `listGroupSale2` ?organization |
| Venue | text field | — | — | `listGroupSale2` ?venue |
| Event | text field | — | — | `listGroupSale2` ?event |
| Sales owner | text field | — | — | `listGroupSale2` ?salesOwner |
| Group type | text field | — | — | `listGroupSale2` ?groupType |
| Product | text field | — | — | `listGroupSale2` ?product |
| Date | text field | — | — | `listGroupSale2` ?date |
| Campaign | text field | — | — | `listGroupSale2` ?campaign |
| Market | text field | — | — | `listGroupSale2` ?market |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**New Enquiries** (metric tile)

**Open Opportunities** (metric tile)

**Quotations Outstanding** (metric tile)

**Quotes Awaiting Approval** (metric tile)

**Confirmed Groups** (metric tile)

**Expected Guests** (metric tile)

**Pipeline Value** (metric tile)

**Confirmed Revenue** (metric tile)

**Conversion Rate** (metric tile)

**Average Group Value** (metric tile)

**Expiring Quotes** (metric tile)

**Sales Target Achievement** (metric tile)

**Follow-ups due** (metric tile)

**Quotes expiring** (metric tile)

**Customer responses** (metric tile)

**Approval requests** (metric tile)

**Deposits pending** (metric tile)

**Every group sales** (data table, from `listGroupSale`)

| Shows | Format | Notes |
|---|---|---|
| Enquiry | text | Enquiry ID |
| Organization customer | text | Organization/Customer |
| Group type | text | Group Type |
| Event attraction | text | Event/Attraction |
| Visit date | 1 Oct 2026, 14:30 | Visit Date |
| Guest count | 1,234 | Guest Count |
| Sales owner | text | Sales Owner |
| Estimated value | text | Estimated Value |
| Quote status | text | Quote Status |
| Probability | text | Probability |
| Next action | 1 Oct 2026, 14:30 | Next Action |
| Expected close date | 1 Oct 2026, 14:30 | Expected Close Date |

**The selected group sales** (detail panel): The pack groups this record's detail under its own headings: “Visualize”, “High Priority Opportunity”.

| Shows | Format | Notes |
|---|---|---|
| Enquiry | text | Enquiry ID |
| Organization customer | text | Organization/Customer |
| Group type | text | Group Type |
| Event attraction | text | Event/Attraction |
| Visit date | 1 Oct 2026, 14:30 | Visit Date |
| Guest count | 1,234 | Guest Count |
| Sales owner | text | Sales Owner |
| Estimated value | text | Estimated Value |
| Quote status | text | Quote Status |
| Probability | text | Probability |
| Next action | 1 Oct 2026, 14:30 | Next Action |
| Expected close date | 1 Oct 2026, 14:30 | Expected Close Date |

**Data it reads**: `listGroupSale2` (onLoad, Group Sales Analytics & AI Intelligence Center); `listGroupSale` (onLoad, Group Sales Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-265` Group Enquiry & Opportunity Capture: *Works in Group Enquiry & Opportunity Capture*; calls `listGroupSale`
- → `BO-266` Group Customer & Organization Profile: *Works in Group Customer & Organization Profile*; calls `listGroupSale`
- → `BO-267` Group Requirements, Availability & Capacity Planner: *Works in Group Requirements, Availability & Capacity Planner*; calls `listGroupSale`
- → `BO-268` Group Package & Experience Builder: *Works in Group Package & Experience Builder*; calls `listGroupSale`
- → `BO-269` Group Quotation Builder & Proposal Generation: *Works in Group Quotation Builder & Proposal Generation*; calls `listGroupSale`
- → `BO-270` Quote Revision, Negotiation & Version Management: *Works in Quote Revision, Negotiation & Version Management*; calls `listGroupSale`
- → `BO-271` Group Discount, Exception & Approval Workflow: *Works in Group Discount, Exception & Approval Workflow*; calls `listGroupSale`
- → `BO-272` Quote-to-Booking Conversion & Confirmation: *Works in Quote-to-Booking Conversion & Confirmation*; calls `listGroupSale`
- → `BO-273` Group Booking 360° & Handover Workspace: *Works in Group Booking 360° & Handover Workspace*; calls `listGroupSale`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group sales list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group sales untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group sales yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group sales are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listGroupSale2` → `ORDER_VIEW` (read) · staff
- `listGroupSale` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- One unified flow for groups, schools and corporates: inquiry > package builder > quotation > approval > confirmed booking. *(agreed · MoM 31 Aug 2026, 4.7 Group Sales / 5. Key Decisions · DI-565)*
- Sales-team dashboard shows group inquiries, opportunities and confirmed bookings and flags items needing attention. Customer types: individual (B2C/walk-in), group, school (with subcategories e.g. by curriculum/nationality), configurable to add more. *(client request · MoM 31 Aug 2026, 4.7 Group Sales & Corporate/School Bookings · DI-563)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-264` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-264`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 1
- Flow F136 *Group Sales Corporate Booking Management board 1: Group Sales Command Center*, step 1: Opens Group Sales Command Center → Provide the Group Sales team with a centralized commercial workspace showing the entire group-sales pipeline.
- Flow F136 *Group Sales Corporate Booking Management board 1: Group Sales Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F136 *Group Sales Corporate Booking Management board 1: Group Sales Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F136 *Group Sales Corporate Booking Management board 1: Group Sales Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F136 *Group Sales Corporate Booking Management board 1: Group Sales Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F136 *Group Sales Corporate Booking Management board 1: Group Sales Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F136 *Group Sales Corporate Booking Management board 1: Group Sales Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F136 *Group Sales Corporate Booking Management board 1: Group Sales Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F136 branch at step 1 (expected): when Nothing has been set up on Group Sales Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F136 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-264?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-265`, `BO-266`, `BO-267`, `BO-268`, `BO-269`, `BO-270`, `BO-271`, `BO-272`, `BO-273`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-265` Group Enquiry & Opportunity Capture

**Capture a new group-sales enquiry and convert it into a structured sales opportunity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/group-enquiry-opportunity-capture-bo-265` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Enquiry ID | select field | — | — | — | — | — | — |
| Customer/Organization | select field | — | — | — | — | — | — |
| Contact | select field | — | — | — | — | — | — |
| Group Type | select field | — | — | — | — | — | — |
| Requested Venue | select field | — | — | — | — | — | — |
| Requested Event/Experience | select field | — | — | — | — | — | — |
| Preferred Date | select field | — | — | — | — | — | — |
| Alternative Date | select field | — | — | — | — | — | — |
| Preferred Time | select field | — | — | — | — | — | — |
| Estimated Guests | select field | — | — | — | — | — | — |
| Adults | select field | — | — | — | — | — | — |
| Children | select field | — | — | — | — | — | — |
| Students | select field | — | — | — | — | — | — |
| Staff/Teachers | select field | — | — | — | — | — | — |
| Special Requirements | select field | — | — | — | — | — | — |
| Budget | select field | — | — | — | — | — | — |
| Notes | select field | — | — | — | — | — | — |
| Sales Owner | select field | — | — | — | — | — | — |
| Sales Team | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |
| Expected Value | select field | — | — | — | — | — | — |
| Probability | select field | — | — | — | — | — | — |
| Expected Close Date | select field | — | — | — | — | — | — |
| Lead Source | select field | — | — | — | — | — | — |
| Campaign | select field | — | — | — | — | — | — |
| Next Action | select field | — | — | — | — | — | — |

**Sent by *Capture enquiry*** (`createGroupEnquiry`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Source `source` | select | required | — | Website · Sales team · Campaign · Existing customer · Partner · Manual entry | — | Where the enquiry came from (decided 29 September, readiness close-out). | `createGroupEnquiry` body |
| Organisation `organisationId` | picker: choose an organisation | optional | — | — | shows names, sends the id | An organisation already on file; null when the enquirer is not yet one. | `createGroupEnquiry` body |
| Contact `contact` | group | required | — | — | — | — | `createGroupEnquiry` body |
| Name `contact.name` | text field | required | — | max length 120 | — | — | `createGroupEnquiry` body |
| Email `contact.email` | email field | optional | — | — | name@example.ae | — | `createGroupEnquiry` body |
| Phone `contact.phone` | phone field | optional | — | max length 30 | +971 5X XXX XXXX (E.164) | — | `createGroupEnquiry` body |
| Organisation name `contact.organisationName` | text field | optional | — | max length 200 | — | Who they are, when `organisationId` is null. | `createGroupEnquiry` body |
| Group size `groupSize` | number field | required | — | min 1 | — | — | `createGroupEnquiry` body |
| Preferred dates `preferredDates` | list of values (chips) | optional | — | — | — | — | `createGroupEnquiry` body |
| Requirements `requirements` | text area | optional | — | max length 2000 | — | — | `createGroupEnquiry` body |
| Sales owner principal `salesOwnerPrincipalId` | picker: choose a sales owner principal | optional | — | — | shows names, sends the id | The opportunity's owner. An enquiry is the opportunity (DM5, 29 September); the pipeline fields live on it rather than on a second table that would copy it. | `createGroupEnquiry` body |
| Priority `priority` | segmented control | optional | — | Low · Normal · High | — | — | `createGroupEnquiry` body |
| Expected value `expectedValue` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createGroupEnquiry` body |
| Probability `probability` | stepper or slider | optional | — | min 0; max 100 | — | Percent. | `createGroupEnquiry` body |
| Expected close date `expectedCloseDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createGroupEnquiry` body |
| Next action at `nextActionAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createGroupEnquiry` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Sales Team (primary button) | navigation or local | — | — | — | — |
| Campaign (secondary button) | navigation or local | — | — | — | — |
| Existing Customer (secondary button) | navigation or local | — | — | — | — |
| Manual Entry (secondary button) | navigation or local | — | — | — | — |
| Capture enquiry (primary button) | `createGroupEnquiry` POST `/group-enquiry-opportunity` | GroupEnquiryInput | GroupEnquiryOpportunityView | — | — |

**Data it reads**: `listGroupEnquiryOpportunity` (onLoad, Group Enquiry & Opportunity Capture)

**Where the user goes next**

- → `BO-264` Group Sales Command Center: *Returns to the board's landing screen*; calls `listGroupEnquiryOpportunity`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group enquiry opportunity configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group enquiry opportunity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group enquiry opportunity configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listGroupEnquiryOpportunity` → `ORDER_VIEW` (read) · staff
- `createGroupEnquiry` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Sales-team dashboard shows group inquiries, opportunities and confirmed bookings and flags items needing attention. Customer types: individual (B2C/walk-in), group, school (with subcategories e.g. by curriculum/nationality), configurable to add more. *(client request · MoM 31 Aug 2026, 4.7 Group Sales & Corporate/School Bookings · DI-563)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-265` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-265`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 1
- Flow F136 *Group Sales Corporate Booking Management board 1: Group Sales Command Center*, step 2: Works in Group Enquiry & Opportunity Capture → Capture a new group-sales enquiry and convert it into a structured sales opportunity.

#### Acceptance for the design

- [ ] Every input above is drawn (42), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-265?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Sales Team, Campaign, Existing Customer, Manual Entry, Capture enquiry.
- [ ] Every transition is wired: `BO-264`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-266` Group Customer & Organization Profile

**Maintain the customer or organization buying directly from TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW`, `PRODUCT_CONFIGURE` (1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/group-customer-organization-profile-bo-266` |

#### Inputs: what the user enters or picks

**Sent by *Save organisation profile*** (`setGroupCustomerOrganization`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Organisation `organisationId` | picker: choose an organisation | optional | — | — | shows names, sends the id | Null creates the organisation; an id replaces that profile. | `setGroupCustomerOrganization` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setGroupCustomerOrganization` body |
| Organisation type `organisationType` | select | required | — | School · Corporate · Travel agent · Event organizer · Association · Government · Other | — | What kind of buyer this is (decided 29 September, readiness close-out). | `setGroupCustomerOrganization` body |
| Contacts `contacts` | repeatable rows | optional | — | — | — | — | `setGroupCustomerOrganization` body |
| Role `contacts[].role` | radio group | required | — | Primary · Booking · Finance · Event day · Decision maker | — | — | `setGroupCustomerOrganization` body |
| Name `contacts[].name` | text field | required | — | max length 120 | — | — | `setGroupCustomerOrganization` body |
| Email `contacts[].email` | email field | optional | — | — | name@example.ae | — | `setGroupCustomerOrganization` body |
| Phone `contacts[].phone` | phone field | optional | — | max length 30 | +971 5X XXX XXXX (E.164) | — | `setGroupCustomerOrganization` body |
| Billing details `billingDetails` | group | optional | — | — | — | — | `setGroupCustomerOrganization` body |
| Billing name `billingDetails.billingName` | text field | optional | — | max length 200 | — | — | `setGroupCustomerOrganization` body |
| Billing email `billingDetails.billingEmail` | email field | optional | — | — | name@example.ae | — | `setGroupCustomerOrganization` body |
| Address `billingDetails.address` | text area | optional | — | max length 500 | — | — | `setGroupCustomerOrganization` body |
| Tax details `taxDetails` | group | optional | — | — | — | — | `setGroupCustomerOrganization` body |
| Tax registration number `taxDetails.taxRegistrationNumber` | text field | optional | — | max length 50 | — | — | `setGroupCustomerOrganization` body |
| Tax country `taxDetails.taxCountry` | text field | optional | — | pattern `^[A-Z]{2}$` | — | — | `setGroupCustomerOrganization` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every group customer organization** (data table, from `listGroupCustomerOrganization`)

| Shows | Format | Notes |
|---|---|---|
| Previous enquiries | 1,234 | Previous enquiries |
| Previous quotations | 1,234 | Previous quotations |
| Confirmed bookings | 1,234 | Confirmed bookings |
| Total guests | 1,234 | Total guests |
| Revenue | AED 1,234.50 | Revenue |
| Cancellation history | text | Cancellation history |
| Outstanding balance | AED 1,234.50 | Outstanding balance |
| Future bookings | 1,234 | Future bookings |

**The selected group customer organization** (detail panel): The pack groups this record's detail under its own headings: “Maintain”, “CRM Integration”.

| Shows | Format | Notes |
|---|---|---|
| Previous enquiries | 1,234 | Previous enquiries |
| Previous quotations | 1,234 | Previous quotations |
| Confirmed bookings | 1,234 | Confirmed bookings |
| Total guests | 1,234 | Total guests |
| Revenue | AED 1,234.50 | Revenue |
| Cancellation history | text | Cancellation history |
| Outstanding balance | AED 1,234.50 | Outstanding balance |
| Future bookings | 1,234 | Future bookings |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Event Organizer (primary button) | navigation or local | — | — | — | — |
| Save organisation profile (primary button) | `setGroupCustomerOrganization` PUT `/group-customer-organization` | GroupCustomerOrganizationInput | GroupCustomerOrganizationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | — |

**Data it reads**: `listGroupCustomerOrganization` (onLoad, Group Customer & Organization Profile)

**Where the user goes next**

- → `BO-264` Group Sales Command Center: *Returns to the board's landing screen*; calls `listGroupCustomerOrganization`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group customer organization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group customer organization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group customer organization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group customer organization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listGroupCustomerOrganization` → `ORDER_VIEW` (read) · staff
- `setGroupCustomerOrganization` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Sales-team dashboard shows group inquiries, opportunities and confirmed bookings and flags items needing attention. Customer types: individual (B2C/walk-in), group, school (with subcategories e.g. by curriculum/nationality), configurable to add more. *(client request · MoM 31 Aug 2026, 4.7 Group Sales & Corporate/School Bookings · DI-563)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-266` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-266`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 1
- Flow F136 *Group Sales Corporate Booking Management board 1: Group Sales Command Center*, step 4: Works in Group Customer & Organization Profile → Maintain the customer or organization buying directly from TICVAI.

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (404, 412).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-266?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Event Organizer, Save organisation profile.
- [ ] Every transition is wired: `BO-264`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-267` Group Requirements, Availability & Capacity Planner

**Determine whether TICVAI can accommodate the requested group before preparing a quotation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/group-requirements-availability-capacity-planner-bo-267` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every group requirements availability** (data table, from `listGroupRequirementAvailability`)

| Shows | Format | Notes |
|---|---|---|
| Event capacity | 1,234 | Event Capacity |
| Available capacity | 1,234 | Available Capacity |
| Existing groups | 1,234 | Existing Groups |
| Public sales | 1,234 | Public Sales |
| Operational holds | 1,234 | Operational Holds |
| Resource availability | text | Resource Availability |
| Timeslot availability | text | Timeslot Availability |

**The selected group requirements availability** (detail panel): The pack groups this record's detail under its own headings: “Calendar View”, “Capacity Reservation”, “Resource Dependencies”.

| Shows | Format | Notes |
|---|---|---|
| Event capacity | 1,234 | Event Capacity |
| Available capacity | 1,234 | Available Capacity |
| Existing groups | 1,234 | Existing Groups |
| Public sales | 1,234 | Public Sales |
| Operational holds | 1,234 | Operational Holds |
| Resource availability | text | Resource Availability |
| Timeslot availability | text | Timeslot Availability |

**Data it reads**: `listGroupRequirementAvailability` (onLoad, Group Requirements, Availability & Capacity Planner)

**Where the user goes next**

- → `BO-264` Group Sales Command Center: *Returns to the board's landing screen*; calls `listGroupRequirementAvailability`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group requirements availability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group requirements availability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group requirements availability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group requirements availability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listGroupRequirementAvailability` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'plan your adventure')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-267` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-267`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 1
- Flow F136 *Group Sales Corporate Booking Management board 1: Group Sales Command Center*, step 6: Works in Group Requirements, Availability & Capacity Planner → Determine whether TICVAI can accommodate the requested group before preparing a quotation.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-267?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-264`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-268` Group Package & Experience Builder

**Build a complete commercial package tailored to the group's requirements.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/group-package-experience-builder-bo-268` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every group package experience** (data table, from `setGroupPackageExperience`)

| Shows | Format | Notes |
|---|---|---|
| Standard price | AED 1,234.50 | Standard Price |
| Group rate | 12.5% | Group Rate |
| Discount | AED 1,234.50 | Discount |
| Complimentary quantity | 1,234 | Complimentary Quantity |
| Add on price | AED 1,234.50 | Add-on Price |
| Tax | text | Tax |
| Fees | 1,234 | Fees |
| Package total | text | Package Total |
| Price per guest | AED 1,234.50 | Price Per Guest |

**The selected group package experience** (detail panel): The pack groups this record's detail under its own headings: “School Discovery Package”, “Package Templates”.

| Shows | Format | Notes |
|---|---|---|
| Standard price | AED 1,234.50 | Standard Price |
| Group rate | 12.5% | Group Rate |
| Discount | AED 1,234.50 | Discount |
| Complimentary quantity | 1,234 | Complimentary Quantity |
| Add on price | AED 1,234.50 | Add-on Price |
| Tax | text | Tax |
| Fees | 1,234 | Fees |
| Package total | text | Package Total |
| Price per guest | AED 1,234.50 | Price Per Guest |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Group Ticket (primary button) | navigation or local | — | — | — | — |
| Meal Voucher (secondary button) | navigation or local | — | — | — | — |
| VIP Experience (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-264` Group Sales Command Center: *Returns to the board's landing screen*; calls `setGroupPackageExperience`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group package experience list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group package experience untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group package experience yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group package experience are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setGroupPackageExperience` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- One unified flow for groups, schools and corporates: inquiry > package builder > quotation > approval > confirmed booking. *(agreed · MoM 31 Aug 2026, 4.7 Group Sales / 5. Key Decisions · DI-565)*
- Package builder assembles admission, meals, workshops etc. against real-time availability and generates a quotation; negotiated revisions are kept as successive versions; extra discounts go through a configurable approval workflow. *(client request · MoM 31 Aug 2026, 4.7 Group Sales & Corporate/School Bookings · DI-564)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-268` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-268`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 1
- Flow F136 *Group Sales Corporate Booking Management board 1: Group Sales Command Center*, step 8: Works in Group Package & Experience Builder → Build a complete commercial package tailored to the group's requirements.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-268?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Group Ticket, Meal Voucher, VIP Experience.
- [ ] Every transition is wired: `BO-264`.
- [ ] Every gated control is gated: `ORDER_CREATE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-269` Group Quotation Builder & Proposal Generation

**Turn the configured group package into a professional customer quotation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture; Where configured, customer can) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/group-quotation-builder-proposal-generation-bo-269` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Quote Number | select field | — | — | — | — | — | — |
| Opportunity | select field | — | — | — | — | — | — |
| Customer | select field | — | — | — | — | — | — |
| Contact | select field | — | — | — | — | — | — |
| Quote Date | select field | — | — | — | — | — | — |
| Valid Until | select field | — | — | — | — | — | — |
| Visit Date | select field | — | — | — | — | — | — |
| Guest Count | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Sales Owner | select field | — | — | — | — | — | — |
| Accept / Reject / Request Changes | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-264` Group Sales Command Center: *Returns to the board's landing screen*; calls `setGroupQuotationProposal`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group quotation proposal configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group quotation proposal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group quotation proposal configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setGroupQuotationProposal` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- One unified flow for groups, schools and corporates: inquiry > package builder > quotation > approval > confirmed booking. *(agreed · MoM 31 Aug 2026, 4.7 Group Sales / 5. Key Decisions · DI-565)*
- Package builder assembles admission, meals, workshops etc. against real-time availability and generates a quotation; negotiated revisions are kept as successive versions; extra discounts go through a configurable approval workflow. *(client request · MoM 31 Aug 2026, 4.7 Group Sales & Corporate/School Bookings · DI-564)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-269` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-269`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 1
- Flow F136 *Group Sales Corporate Booking Management board 1: Group Sales Command Center*, step 10: Works in Group Quotation Builder & Proposal Generation → Turn the configured group package into a professional customer quotation.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-269?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-264`.
- [ ] Every gated control is gated: `ORDER_CREATE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-270` Quote Revision, Negotiation & Version Management

**Manage the commercial negotiation process without losing historical versions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/quote-revision-negotiation-version-management-bo-270` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Customer Request | select field | — | — | — | — | — | — |
| Internal Response | select field | — | — | — | — | — | — |
| Price Change | select field | — | — | — | — | — | — |
| Quantity Change | select field | — | — | — | — | — | — |
| Package Change | select field | — | — | — | — | — | — |
| Terms Change | select field | — | — | — | — | — | — |
| Date | select field | — | — | — | — | — | — |
| User | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listQuoteRevisionNegotiation` (onLoad, Quote Revision, Negotiation & Version Management)

**Where the user goes next**

- → `BO-264` Group Sales Command Center: *Returns to the board's landing screen*; calls `listQuoteRevisionNegotiation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The quote revision negotiation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the quote revision negotiation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No quote revision negotiation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listQuoteRevisionNegotiation` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Package builder assembles admission, meals, workshops etc. against real-time availability and generates a quotation; negotiated revisions are kept as successive versions; extra discounts go through a configurable approval workflow. *(client request · MoM 31 Aug 2026, 4.7 Group Sales & Corporate/School Bookings · DI-564)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-270` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-270`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 1
- Flow F136 *Group Sales Corporate Booking Management board 1: Group Sales Command Center*, step 12: Works in Quote Revision, Negotiation & Version Management → Manage the commercial negotiation process without losing historical versions.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-270?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-264`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-271` Group Discount, Exception & Approval Workflow

**Govern non-standard group pricing and commercial exceptions before a quote is committed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/group-discount-exception-approval-workflow-bo-271` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-264` Group Sales Command Center: *Returns to the board's landing screen*; calls `approveGroupDiscountException`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group discount exception list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group discount exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group discount exception yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group discount exception are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `approveGroupDiscountException` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Package builder assembles admission, meals, workshops etc. against real-time availability and generates a quotation; negotiated revisions are kept as successive versions; extra discounts go through a configurable approval workflow. *(client request · MoM 31 Aug 2026, 4.7 Group Sales & Corporate/School Bookings · DI-564)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-271` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-271`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 1
- Flow F136 *Group Sales Corporate Booking Management board 1: Group Sales Command Center*, step 14: Works in Group Discount, Exception & Approval Workflow → Govern non-standard group pricing and commercial exceptions before a quote is committed.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-271?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve, Cancel.
- [ ] Every transition is wired: `BO-264`.
- [ ] Every gated control is gated: `ORDER_CREATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-272` Quote-to-Booking Conversion & Confirmation

**Convert an accepted quotation into a confirmed TICVAI group booking without re-entering the commercial configuration.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_MODIFY`, `ORDER_VIEW` (2 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `groupBookingId` (navigation) |
| Route | `/sell/quote-to-booking-conversion-confirmation-bo-272` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create group booking (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listQuoteBookingConversion` (onLoad, Quote-to-Booking Conversion & Confirmation)

**Where the user goes next**

- → `BO-264` Group Sales Command Center: *Returns to the board's landing screen*; calls `listQuoteBookingConversion`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The quote-to-booking conversion confirmation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the quote-to-booking conversion confirmation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No quote-to-booking conversion confirmation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the quote-to-booking conversion confirmation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The order already has a group booking (`orderAlreadyGrouped`), or is voided (`orderVoided`), or `groupQuoteId` names a quote that cannot be converted … (GroupBookingProblem); 409 The status change goes backwards (`statusBackwards`), or the group is already cancelled or complete (`groupClosed`). (GroupBookingProblem) |

#### Permissions

- `listQuoteBookingConversion` → `ORDER_VIEW` (read) · staff
- `createGroupBooking` → `ORDER_CREATE` (operate) · staff
- `updateGroupBooking` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- One unified flow for groups, schools and corporates: inquiry > package builder > quotation > approval > confirmed booking. *(agreed · MoM 31 Aug 2026, 4.7 Group Sales / 5. Key Decisions · DI-565)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-272` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-272`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 1
- Flow F136 *Group Sales Corporate Booking Management board 1: Group Sales Command Center*, step 16: Works in Quote-to-Booking Conversion & Confirmation → Convert an accepted quotation into a confirmed TICVAI group booking without re-entering the commercial configuration.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 409, 412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-272?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create group booking, Cancel.
- [ ] Every transition is wired: `BO-264`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-273` Group Booking 360° & Handover Workspace

**Provide a consolidated view of the completed sales journey and hand the confirmed group cleanly from Sales to Operations. 360° Header Board 1 ended when the quotation was accepted and converted into a confirmed group booking. Board 2 takes over from confirmation until the group visit is completed and financially closed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/group-booking-360-handover-workspace-bo-273` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every group booking 360°** (data table, from `setGroupBookingHandover`)

| Shows | Format | Notes |
|---|---|---|
| Arrival | text | Arrival |
| Group check in | text | Group Check-In |
| Guides | 1,234 | Guides |
| Catering | text | Catering |
| Accessibility | text | Accessibility |
| Transport | text | Transport |
| Parking | text | Parking |
| Special instructions | 1,234 | Special Instructions |
| Resources | 1,234 | Resources |
| Original enquiry | text | Original Enquiry |
| Opportunity | text | Opportunity |
| Final quote | text | Final Quote |
| Discount | AED 1,234.50 | Discount |
| Approval | text | Approval |
| Agreed price | AED 1,234.50 | Agreed Price |
| Deposit | AED 1,234.50 | Deposit |
| Balance | AED 1,234.50 | Balance |
| Products | 1,234 | Products |
| Tickets | 1,234 | Tickets |
| Date time | 1 Oct 2026, 14:30 | Date/time |
| Capacity | 1,234 | Capacity |
| Seating | text | Seating where applicable |
| Package components | 1,234 | Package components |
| Organization | text | Organization |
| Main contact | text | Main Contact |
| Finance contact | text | Finance Contact |
| Event day contact | text | Event-Day Contact |

**The selected group booking 360°** (detail panel): The pack groups this record's detail under its own headings: “Backend Screen Primary Responsibility”, “Enquiry/opportunity”, “Multi-product package”, “Group Quotation Builder & Proposal”, “Quote Revision, Negotiation & Version”, “Group Discount, Exception & Approval”.

| Shows | Format | Notes |
|---|---|---|
| Arrival | text | Arrival |
| Group check in | text | Group Check-In |
| Guides | 1,234 | Guides |
| Catering | text | Catering |
| Accessibility | text | Accessibility |
| Transport | text | Transport |
| Parking | text | Parking |
| Special instructions | 1,234 | Special Instructions |
| Resources | 1,234 | Resources |
| Original enquiry | text | Original Enquiry |
| Opportunity | text | Opportunity |
| Final quote | text | Final Quote |
| Discount | AED 1,234.50 | Discount |
| Approval | text | Approval |
| Agreed price | AED 1,234.50 | Agreed Price |
| Deposit | AED 1,234.50 | Deposit |
| Balance | AED 1,234.50 | Balance |
| Products | 1,234 | Products |
| Tickets | 1,234 | Tickets |
| Date time | 1 Oct 2026, 14:30 | Date/time |
| Capacity | 1,234 | Capacity |
| Seating | text | Seating where applicable |
| Package components | 1,234 | Package components |
| Organization | text | Organization |
| Main contact | text | Main Contact |
| Finance contact | text | Finance Contact |
| Event day contact | text | Event-Day Contact |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group booking 360° list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group booking 360° untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group booking 360° yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group booking 360° are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setGroupBookingHandover` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Family/dependent view shows a family ticket's composition (e.g. two adults, two children) with each dependent's entitlements; equivalent views for school and corporate bookings. *(client request · MoM 7 Sep 2026, 4.9 Entitlements Portfolio - Structure, Family/Group & Assignment · DI-668)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-273` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-273`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 1
- Flow F136 *Group Sales Corporate Booking Management board 1: Group Sales Command Center*, step 18: Works in Group Booking 360° & Handover Workspace → Provide a consolidated view of the completed sales journey and hand the confirmed group cleanly from Sales to Operations. 360° Header Board 1 ended when the quotation was accepted and converted into …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (54 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-273?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ORDER_CREATE`.
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

### In P08 · Sell

- Allam: back-end configuration is the most critical part; the screens must make visually clear how administrators configure products, pricing per channel, attributes/components, entitlements, validity and access permissions, comparable to the structured product/metric-sheet approach of an earlier reference system. *(agreed · MoM 24 Sep 2026, 4.3 Back-End Configuration Detail — Requested Format (Screens, Not Just Functional Lists) · DI-985)*
- Chinmay: reduce the number of configuration screens/pages and consolidate related settings/toggles to avoid a long, click-heavy admin flow; Allam agreed, citing the previous system's demo as a starting reference. *(agreed · MoM 25 Aug 2026, 4.11 UX Simplification & Distributed Inventory · DI-474)*
- Retail dashboard gives a consolidated real-time view across outlets — total retail sales, total and average transactions, store performance snapshot, system alerts and out-of-stock indicators — viewable by day, week or month. *(client request · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-349)*
- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*

**13 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"approveGroupDiscountException": {"method":"PUT","path":"/group-discount-exception","contract":"orders","summary":"Group Discount, Exception & Approval Workflow","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"GroupDiscountExceptionApprovalWorkflowInput","responds":"GroupDiscountExceptionApprovalWorkflowView"},
"createGroupBooking": {"method":"POST","path":"/group-bookings","contract":"orders","summary":"Turn an order into a group booking","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateGroupBookingRequest","responds":"GroupBooking"},
"createGroupEnquiry": {"method":"POST","path":"/group-enquiry-opportunity","contract":"orders","summary":"Capture a group enquiry","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GroupEnquiryInput","responds":"GroupEnquiryOpportunityView"},
"listGroupCustomerOrganization": {"method":"GET","path":"/group-customer-organization","contract":"orders","summary":"Group Customer & Organization Profile","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GroupCustomerOrganizationProfileView"},
"listGroupEnquiryOpportunity": {"method":"GET","path":"/group-enquiry-opportunity","contract":"orders","summary":"Group Enquiry & Opportunity Capture","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GroupEnquiryOpportunityCaptureView"},
"listGroupRequirementAvailability": {"method":"GET","path":"/group-requirement-availability","contract":"orders","summary":"Group Requirements, Availability & Capacity Planner","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GroupRequirementsAvailabilityCapacityPlannerView"},
"listGroupSale": {"method":"GET","path":"/group-sale","contract":"orders","summary":"Group Sales Command Center","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GroupSalesCommandCenterView"},
"listGroupSale2": {"method":"GET","path":"/group-sale-2","contract":"orders","summary":"Group Sales Analytics & AI Intelligence Center","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"customerType","in":"query","required":false},{"name":"organization","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"salesOwner","in":"query","required":false},{"name":"groupType","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"date","in":"query","required":false},{"name":"campaign","in":"query","required":false},{"name":"market","in":"query","required":false}],"requestBody":null,"responds":"GroupSalesAnalyticsAiIntelligenceCenterView"},
"listQuoteBookingConversion": {"method":"GET","path":"/quote-booking-conversion","contract":"orders","summary":"Quote-to-Booking Conversion & Confirmation","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"QuoteToBookingConversionConfirmationView"},
"listQuoteRevisionNegotiation": {"method":"GET","path":"/quote-revision-negotiation","contract":"orders","summary":"Quote Revision, Negotiation & Version Management","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"QuoteRevisionNegotiationVersionManagementView"},
"setGroupBookingHandover": {"method":"PUT","path":"/group-booking-handover","contract":"orders","summary":"Group Booking 360° & Handover Workspace","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"GroupBooking360HandoverWorkspaceInput","responds":"GroupBooking360HandoverWorkspaceView"},
"setGroupCustomerOrganization": {"method":"PUT","path":"/group-customer-organization","contract":"orders","summary":"Save a group customer organisation's profile","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"GroupCustomerOrganizationInput","responds":"GroupCustomerOrganizationView"},
"setGroupPackageExperience": {"method":"PUT","path":"/group-package-experience","contract":"orders","summary":"Group Package & Experience Builder","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"GroupPackageExperienceBuilderInput","responds":"GroupPackageExperienceBuilderView"},
"setGroupQuotationProposal": {"method":"PUT","path":"/group-quotation-proposal","contract":"orders","summary":"Group Quotation Builder & Proposal Generation","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"GroupQuotationBuilderProposalGenerationInput","responds":"GroupQuotationBuilderProposalGenerationView"},
"updateGroupBooking": {"method":"PATCH","path":"/group-bookings/{groupBookingId}","contract":"orders","summary":"Confirm numbers, change the leader or cancel a group","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"UpdateGroupBookingRequest","responds":"GroupBooking"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CreateGroupBookingRequest": {"type":"object","description":"Request only. Persisted as `GroupBooking`.","required":["orderId","leaderSubjectId","expectedSize"],"properties":{"groupQuoteId":{"x-ticvai-references":"orders.group_quote","type":"string","format":"uuid","nullable":true,"description":"**The quote this booking converts** (BO-272). Must be the current version and `sent` or `accepted`; conversion sets its `groupBookingId` and moves a `sent` quote to `accepted` (decided 29 September, writers pass)."},"kind":{"type":"string","enum":["general","school","corporate","party"],"default":"general"},"packageProductId":{"type":"string","nullable":true,"description":"The school-trip format or party package."},"yearGroup":{"type":"string","maxLength":40,"nullable":true},"accessAndDietaryNeeds":{"type":"string","maxLength":1000,"nullable":true},"celebrantName":{"type":"string","maxLength":120,"nullable":true,"description":"The birthday child."},"celebrantTurningAge":{"type":"integer","minimum":1,"maximum":18,"nullable":true},"allergiesAndRequests":{"type":"string","maxLength":1000,"nullable":true},"finalHeadcountDueBy":{"type":"string","format":"date-time","nullable":true},"orderId":{"type":"string","format":"uuid"},"leaderSubjectId":{"type":"string","format":"uuid","description":"The person who pays, is called if the coach is late, and collects the names."},"organisationName":{"type":"string","maxLength":200,"nullable":true},"expectedSize":{"type":"integer","minimum":2},"minimumSize":{"type":"integer","minimum":1,"nullable":true},"attendeeCaptureRequired":{"type":"boolean","default":false},"attendeeCaptureDueBy":{"type":"string","format":"date-time","nullable":true}}},
"GroupBooking": {"type":"object","x-ticvai-persistence":"orders.group_booking","description":"BL-028. **`BO-026 Group Bookings` ran on generic order operations** — no group size, no quota, no leader, no per-attendee capture.\n**The leader is the point.** A school booking forty places has one person who pays, one who is called if the coach is late, and forty who need names collecting — and a generic order has one guest.\n","required":["id","orderId","leaderSubjectId","expectedSize","status"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["general","school","corporate","party"],"default":"general"},"packageProductId":{"type":"string","nullable":true,"description":"The school-trip format or party package."},"yearGroup":{"type":"string","maxLength":40,"nullable":true},"accessAndDietaryNeeds":{"type":"string","maxLength":1000,"nullable":true},"celebrantName":{"type":"string","maxLength":120,"nullable":true,"description":"The birthday child."},"celebrantTurningAge":{"type":"integer","minimum":1,"maximum":18,"nullable":true},"allergiesAndRequests":{"type":"string","maxLength":1000,"nullable":true},"finalHeadcountDueBy":{"type":"string","format":"date-time","nullable":true},"quoteSentAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"riskAssessmentSentAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"preferredDate":{"type":"string","format":"date","nullable":true,"description":"The date the guest asked for on `requestGroupBooking` — what its `409 dateUnavailable` is checked against. Null for a group a member of staff built from an order."},"orderId":{"type":"string","format":"uuid"},"leaderSubjectId":{"type":"string","format":"uuid"},"organisationName":{"type":"string","nullable":true},"expectedSize":{"type":"integer"},"confirmedSize":{"type":"integer","nullable":true},"minimumSize":{"type":"integer","nullable":true,"description":"**Below which the group rate does not apply.** A booking for forty that arrives as twelve is a pricing question somebody has to answer at the gate, and stating the threshold means answering it at booking instead.\n"},"attendeeCaptureRequired":{"type":"boolean","default":false,"description":"**Whether names are needed before admission.** A school trip usually needs them and a corporate day out usually does not, and the difference is a safeguarding requirement rather than a preference.\n"},"attendeeCaptureDueBy":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["provisional","confirmed","namesPending","complete","cancelled"]}}},
"GroupBooking360HandoverWorkspaceInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; lands in the handover columns of `orders.group_visit_plan` (DM5, 29 September)","description":"**What Group Booking 360° & Handover Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"notes":{"type":"string","description":"Notes"},"attachments":{"type":"string","description":"Attachments"},"handoverAcknowledgment":{"type":"string","description":"Handover acknowledgment"}}},
"GroupBooking360HandoverWorkspaceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Booking 360° & Handover Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"arrival":{"type":"string","description":"Arrival"},"groupCheckIn":{"type":"string","description":"Group Check-In"},"guides":{"type":"integer","description":"Guides"},"catering":{"type":"string","description":"Catering"},"accessibility":{"type":"string","description":"Accessibility"},"transport":{"type":"string","description":"Transport"},"parking":{"type":"string","description":"Parking"},"specialInstructions":{"type":"integer","description":"Special Instructions"},"resources":{"type":"integer","description":"Resources"},"originalEnquiry":{"type":"string","description":"Original Enquiry"},"opportunity":{"type":"string","description":"Opportunity"},"finalQuote":{"type":"string","description":"Final Quote"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount"},"approval":{"type":"string","description":"Approval"},"agreedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Agreed Price"},"deposit":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Deposit"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Balance"},"products":{"type":"integer","description":"Products"},"tickets":{"type":"integer","description":"Tickets"},"dateTime":{"type":"string","format":"date-time","description":"Date/time"},"capacity":{"type":"integer","description":"Capacity"},"packageComponents":{"type":"integer","description":"Package components"},"organization":{"type":"string","description":"Organization"},"mainContact":{"type":"string","description":"Main Contact"},"financeContact":{"type":"string","description":"Finance Contact"},"eventDayContact":{"type":"string","description":"Event-Day Contact"},"notes":{"type":"string","description":"Notes"},"attachments":{"type":"string","description":"Attachments"},"handoverAcknowledgment":{"type":"string","description":"Handover acknowledgment"},"seating":{"type":"string","description":"Seating where applicable"}}},
"GroupCustomerOrganizationInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `setGroupCustomerOrganization` takes (decided 29 September, readiness close-out).","required":["name","organisationType"],"properties":{"organisationId":{"type":"string","format":"uuid","nullable":true,"description":"Null creates the organisation; an id replaces that profile."},"name":{"type":"string","maxLength":200},"organisationType":{"type":"string","description":"What kind of buyer this is (decided 29 September, readiness close-out).","enum":["school","corporate","travelAgent","eventOrganizer","association","government","other"]},"contacts":{"type":"array","items":{"type":"object","required":["role","name"],"properties":{"role":{"type":"string","enum":["primary","booking","finance","eventDay","decisionMaker"]},"name":{"type":"string","maxLength":120},"email":{"type":"string","format":"email","nullable":true},"phone":{"type":"string","maxLength":30,"nullable":true}}}},"billingDetails":{"type":"object","nullable":true,"properties":{"billingName":{"type":"string","maxLength":200},"billingEmail":{"type":"string","format":"email","nullable":true},"address":{"type":"string","maxLength":500,"nullable":true}}},"taxDetails":{"type":"object","nullable":true,"properties":{"taxRegistrationNumber":{"type":"string","maxLength":50,"nullable":true},"taxCountry":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true}}}}},
"GroupCustomerOrganizationProfileView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Customer & Organization Profile displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"organizationName":{"type":"string","description":"Organization Name"},"customerId":{"type":"string","description":"Customer ID"},"country":{"type":"string","description":"Country"},"city":{"type":"string","description":"City"},"address":{"type":"string","description":"Address"},"taxVatInformation":{"type":"string","description":"Tax/VAT Information"},"preferredLanguage":{"type":"string","description":"Preferred Language"},"billingDetails":{"type":"string","description":"Billing Details"},"accountOwner":{"type":"string","description":"Account Owner"},"primaryContact":{"type":"string","description":"Primary Contact"},"bookingContact":{"type":"string","description":"Booking Contact"},"financeContact":{"type":"string","description":"Finance Contact"},"eventDayContact":{"type":"string","description":"Event-Day Contact"},"decisionMaker":{"type":"string","description":"Decision Maker"},"previousEnquiries":{"type":"integer","description":"Previous enquiries"},"previousQuotations":{"type":"integer","description":"Previous quotations"},"confirmedBookings":{"type":"integer","description":"Confirmed bookings"},"totalGuests":{"type":"integer","description":"Total guests"},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue"},"cancellationHistory":{"type":"string","description":"Cancellation history"},"outstandingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Outstanding balance"},"futureBookings":{"type":"integer","description":"Future bookings"},"registrationDetails":{"type":"string","description":"Registration Details where applicable"},"organizationType":{"type":"string","enum":["school","university","company","government","sportsClub","association","tourGroup","privateGroup","eventOrganizer","charity"],"description":"Organisation type (configurable; MoM 31 Aug)."}}},
"GroupCustomerOrganizationView": {"type":"object","x-ticvai-persistence":"orders.group_customer_organization + orders.group_customer_organization_contact","description":"**The organisation a group buys under.** Saved by `setGroupCustomerOrganization` (decided 29 September, readiness close-out); `listGroupCustomerOrganization` is the screen's projection over these.\n","required":["id","name","organisationType"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string","maxLength":200},"organisationType":{"type":"string","enum":["school","corporate","travelAgent","eventOrganizer","association","government","other"]},"contacts":{"type":"array","items":{"type":"object","required":["role","name"],"properties":{"role":{"type":"string","enum":["primary","booking","finance","eventDay","decisionMaker"]},"name":{"type":"string","maxLength":120},"email":{"type":"string","format":"email","nullable":true},"phone":{"type":"string","maxLength":30,"nullable":true}}}},"billingDetails":{"type":"object","nullable":true,"properties":{"billingName":{"type":"string","maxLength":200},"billingEmail":{"type":"string","format":"email","nullable":true},"address":{"type":"string","maxLength":500,"nullable":true}}},"taxDetails":{"type":"object","nullable":true,"properties":{"taxRegistrationNumber":{"type":"string","maxLength":50,"nullable":true},"taxCountry":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true}}},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"GroupDiscountExceptionApprovalWorkflowInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; the decision lands in the discount columns of `orders.group_quote` (DM5, 29 September)","description":"**What Group Discount, Exception & Approval Workflow submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"discount":{"type":"number","description":"Discount %"},"transactionValue":{"type":"string","description":"Transaction value"},"margin":{"type":"number","description":"Margin"},"customerType":{"type":"string","description":"Customer type"},"venue":{"type":"string","description":"Venue"},"event":{"type":"string","description":"Event"},"salesUser":{"type":"string","description":"Sales user"},"risk":{"type":"string","description":"Risk"},"customer":{"type":"string","description":"Customer"},"opportunity":{"type":"string","description":"Opportunity"},"quote":{"type":"string","description":"Quote"},"standardPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Standard Price"},"proposedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Proposed Price"},"marginImpact":{"type":"number","description":"Margin Impact"},"historicalCustomerValue":{"type":"string","description":"Historical Customer Value"},"reason":{"type":"string","description":"Reason"},"capacityImpact":{"type":"integer","description":"Capacity Impact"},"decision":{"type":"string","enum":["approve","reject","returnForChange"],"description":"Approver decision"},"comment":{"type":"string","description":"Comment"}}},
"GroupDiscountExceptionApprovalWorkflowView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Discount, Exception & Approval Workflow displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"discount":{"type":"number","description":"Discount %"},"transactionValue":{"type":"string","description":"Transaction value"},"margin":{"type":"number","description":"Margin"},"customerType":{"type":"string","description":"Customer type"},"venue":{"type":"string","description":"Venue"},"event":{"type":"string","description":"Event"},"salesUser":{"type":"string","description":"Sales user"},"risk":{"type":"string","description":"Risk"},"customer":{"type":"string","description":"Customer"},"opportunity":{"type":"string","description":"Opportunity"},"quote":{"type":"string","description":"Quote"},"standardPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Standard Price"},"proposedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Proposed Price"},"marginImpact":{"type":"number","description":"Margin Impact"},"historicalCustomerValue":{"type":"string","description":"Historical Customer Value"},"reason":{"type":"string","description":"Reason"},"capacityImpact":{"type":"integer","description":"Capacity Impact"},"decision":{"type":"string","enum":["approve","reject","returnForChange"],"description":"Approver decision"}}},
"GroupEnquiryInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `createGroupEnquiry` takes (decided 29 September, readiness close-out).","required":["source","contact","groupSize"],"properties":{"source":{"type":"string","description":"Where the enquiry came from (decided 29 September, readiness close-out).","enum":["website","salesTeam","campaign","existingCustomer","partner","manualEntry"]},"organisationId":{"type":"string","format":"uuid","nullable":true,"description":"An organisation already on file; null when the enquirer is not yet one."},"contact":{"type":"object","required":["name"],"properties":{"name":{"type":"string","maxLength":120},"email":{"type":"string","format":"email","nullable":true},"phone":{"type":"string","maxLength":30,"nullable":true},"organisationName":{"type":"string","maxLength":200,"nullable":true,"description":"Who they are, when `organisationId` is null."}}},"groupSize":{"type":"integer","minimum":1},"preferredDates":{"type":"array","items":{"type":"string","format":"date"}},"requirements":{"type":"string","maxLength":2000,"nullable":true},"salesOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The opportunity's owner. **An enquiry is the opportunity** (DM5, 29 September); the pipeline fields live on it rather than on a second table that would copy it."},"priority":{"type":"string","nullable":true,"enum":["low","normal","high"]},"expectedValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"probability":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"description":"Percent."},"expectedCloseDate":{"type":"string","format":"date","nullable":true},"nextActionAt":{"type":"string","format":"date-time","nullable":true}}},
"GroupEnquiryOpportunityCaptureView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Enquiry & Opportunity Capture displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"enquiryId":{"type":"string","description":"Enquiry ID"},"customerOrganization":{"type":"string","description":"Customer/Organization"},"contact":{"type":"string","description":"Contact"},"groupType":{"type":"string","description":"Group Type"},"requestedVenue":{"type":"string","description":"Requested Venue"},"requestedEvent":{"type":"string","description":"Requested Event"},"requestedExperience":{"type":"string","description":"Requested Experience"},"preferredDate":{"type":"string","format":"date-time","description":"Preferred Date"},"alternativeDate":{"type":"string","format":"date-time","description":"Alternative Date"},"preferredTime":{"type":"string","format":"date-time","description":"Preferred Time"},"estimatedGuests":{"type":"string","description":"Estimated Guests"},"adults":{"type":"string","description":"Adults"},"children":{"type":"string","description":"Children"},"students":{"type":"string","description":"Students"},"staffTeachers":{"type":"string","description":"Staff/Teachers"},"specialRequirements":{"type":"string","description":"Special Requirements"},"budget":{"type":"string","description":"Budget"},"notes":{"type":"string","description":"Notes"},"salesOwner":{"type":"string","description":"Sales Owner"},"priority":{"type":"string","description":"Priority"},"expectedValue":{"type":"string","description":"Expected Value"},"probability":{"type":"string","description":"Probability"},"expectedCloseDate":{"type":"string","format":"date-time","description":"Expected Close Date"},"nextAction":{"type":"string","format":"date-time","description":"Next Action"},"leadSource":{"type":"string","enum":["website","phone","email","walkIn","salesTeam","crm","referral","campaign","existingCustomer","manualEntry"],"description":"Where the enquiry came from."}}},
"GroupEnquiryOpportunityView": {"type":"object","x-ticvai-persistence":"orders.group_enquiry","description":"**One captured group enquiry.** Written by `createGroupEnquiry` (decided 29 September, readiness close-out); `listGroupEnquiryOpportunity` is the screen's projection over these.\n","required":["id","source","contact","groupSize","createdAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"source":{"type":"string","enum":["website","salesTeam","campaign","existingCustomer","partner","manualEntry"]},"organisationId":{"x-ticvai-references":"orders.group_customer_organization","type":"string","format":"uuid","nullable":true},"contact":{"type":"object","properties":{"name":{"type":"string","maxLength":120},"email":{"type":"string","format":"email","nullable":true},"phone":{"type":"string","maxLength":30,"nullable":true},"organisationName":{"type":"string","maxLength":200,"nullable":true}}},"groupSize":{"type":"integer","minimum":1},"preferredDates":{"type":"array","items":{"type":"string","format":"date"}},"requirements":{"type":"string","maxLength":2000,"nullable":true},"salesOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The opportunity's owner. **An enquiry is the opportunity** (DM5, 29 September); the pipeline fields live on it rather than on a second table that would copy it."},"priority":{"type":"string","nullable":true,"enum":["low","normal","high"]},"expectedValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"probability":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"description":"Percent."},"expectedCloseDate":{"type":"string","format":"date","nullable":true},"nextActionAt":{"type":"string","format":"date-time","nullable":true},"createdBy":{"type":"string","format":"uuid","readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true}}},
"GroupPackageExperienceBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; lands in the package columns of `orders.group_quote` (DM5, 29 September)","description":"**What Group Package & Experience Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"componentTypes":{"type":"array","items":{"type":"string","enum":["admissionTickets","groupTicket","guidedTour","reservedSeating","fB","mealVoucher","merchandise","transportation","parking","workshop","educationProgram","meetingRoom","vipExperience","addOns","rentalResources","educationalWorkshop"]},"description":"What the package combines."},"template":{"type":"string","enum":["schoolPackage","corporatePackage","birthdayPackage","vipGroupPackage","conferencePackage"],"description":"Reusable package template."},"packageName":{"type":"string","description":"Package name"},"guestCount":{"type":"integer","description":"Guests"},"components":{"type":"array","items":{"type":"string"},"description":"Products and services in the package"}}},
"GroupPackageExperienceBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Package & Experience Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"standardPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Standard Price"},"groupRate":{"type":"number","description":"Group Rate"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount"},"complimentaryQuantity":{"type":"integer","description":"Complimentary Quantity"},"addOnPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Add-on Price"},"tax":{"type":"string","description":"Tax"},"fees":{"type":"integer","description":"Fees"},"packageTotal":{"type":"string","description":"Package Total"},"pricePerGuest":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price Per Guest"},"componentTypes":{"type":"array","items":{"type":"string","enum":["admissionTickets","groupTicket","guidedTour","reservedSeating","fB","mealVoucher","merchandise","transportation","parking","workshop","educationProgram","meetingRoom","vipExperience","addOns","rentalResources","educationalWorkshop"]},"description":"What the package combines."},"template":{"type":"string","enum":["schoolPackage","corporatePackage","birthdayPackage","vipGroupPackage","conferencePackage"],"description":"Reusable package template."},"packageName":{"type":"string","description":"Package name"},"guestCount":{"type":"integer","description":"Guests"},"components":{"type":"array","items":{"type":"string"},"description":"Products and services in the package"}}},
"GroupQuotationBuilderProposalGenerationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; lands in `orders.group_quote` and its `orders.group_quote_line` rows (DM5, 29 September)","description":"**What Group Quotation Builder & Proposal Generation submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *For each line* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.","properties":{"quoteNumber":{"type":"string","description":"Quote Number"},"opportunity":{"type":"string","description":"Opportunity"},"customer":{"type":"string","description":"Customer"},"contact":{"type":"string","description":"Contact"},"quoteDate":{"type":"string","format":"date-time","description":"Quote Date"},"validUntil":{"type":"string","description":"Valid Until"},"visitDate":{"type":"string","format":"date-time","description":"Visit Date"},"guestCount":{"type":"integer","description":"Guest Count"},"currency":{"type":"string","description":"Currency"},"salesOwner":{"type":"string","description":"Sales Owner"},"quoteValidity":{"type":"string","description":"Quote validity"},"depositRequirement":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Deposit requirement"},"paymentSchedule":{"type":"string","description":"Payment schedule"},"cancellationPolicy":{"type":"string","description":"Cancellation policy"},"amendmentConditions":{"type":"string","description":"Amendment conditions"},"guestCountDeadline":{"type":"string","format":"date-time","description":"Guest-count deadline"},"operationalTerms":{"type":"string","description":"Operational terms"},"deliveryFormats":{"type":"array","items":{"type":"string","enum":["email","pdf","secureDigitalLink","customerPortal"]},"description":"How the proposal is delivered."},"lines":{"type":"array","description":"Quote lines","items":{"type":"object","properties":{"productService":{"type":"string","description":"Product/Service"},"description":{"type":"string","description":"Description"},"quantity":{"type":"integer","description":"Quantity"},"standardRate":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Standard rate"},"groupRate":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Group rate"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount"},"tax":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Tax"},"fee":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fee"},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Total"}}}}},"x-ticvai-record-definition":"For each line"},
"GroupQuotationBuilderProposalGenerationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Quotation Builder & Proposal Generation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"quoteNumber":{"type":"string","description":"Quote Number"},"opportunity":{"type":"string","description":"Opportunity"},"customer":{"type":"string","description":"Customer"},"contact":{"type":"string","description":"Contact"},"quoteDate":{"type":"string","format":"date-time","description":"Quote Date"},"validUntil":{"type":"string","description":"Valid Until"},"visitDate":{"type":"string","format":"date-time","description":"Visit Date"},"guestCount":{"type":"integer","description":"Guest Count"},"currency":{"type":"string","description":"Currency"},"salesOwner":{"type":"string","description":"Sales Owner"},"quoteValidity":{"type":"string","description":"Quote validity"},"depositRequirement":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Deposit requirement"},"paymentSchedule":{"type":"string","description":"Payment schedule"},"cancellationPolicy":{"type":"string","description":"Cancellation policy"},"amendmentConditions":{"type":"string","description":"Amendment conditions"},"guestCountDeadline":{"type":"string","format":"date-time","description":"Guest-count deadline"},"operationalTerms":{"type":"string","description":"Operational terms"},"deliveryFormats":{"type":"array","items":{"type":"string","enum":["email","pdf","secureDigitalLink","customerPortal"]},"description":"How the proposal is delivered."},"lines":{"type":"array","description":"Quote lines","items":{"type":"object","properties":{"productService":{"type":"string","description":"Product/Service"},"description":{"type":"string","description":"Description"},"quantity":{"type":"integer","description":"Quantity"},"standardRate":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Standard rate"},"groupRate":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Group rate"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount"},"tax":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Tax"},"fee":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fee"},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Total"}}}}}},
"GroupRequirementsAvailabilityCapacityPlannerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Requirements, Availability & Capacity Planner displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venue":{"type":"string","description":"Venue"},"eventAttraction":{"type":"string","description":"Event/Attraction"},"date":{"type":"string","format":"date-time","description":"Date"},"alternativeDates":{"type":"string","description":"Alternative Dates"},"arrivalTime":{"type":"string","format":"date-time","description":"Arrival Time"},"departureTime":{"type":"string","format":"date-time","description":"Departure Time"},"groupSize":{"type":"string","description":"Group Size"},"guestCategories":{"type":"string","description":"Guest Categories"},"accessibilityRequirements":{"type":"string","description":"Accessibility Requirements"},"seatingRequirement":{"type":"string","description":"Seating Requirement"},"resources":{"type":"string","description":"Resources"},"guides":{"type":"string","description":"Guides"},"catering":{"type":"string","description":"Catering"},"transportation":{"type":"string","description":"Transportation"},"addOns":{"type":"string","description":"Add-ons"},"eventCapacity":{"type":"integer","description":"Event Capacity"},"availableCapacity":{"type":"integer","description":"Available Capacity"},"existingGroups":{"type":"integer","description":"Existing Groups"},"publicSales":{"type":"integer","description":"Public Sales"},"operationalHolds":{"type":"integer","description":"Operational Holds"},"resourceAvailability":{"type":"string","description":"Resource Availability"},"timeslotAvailability":{"type":"string","description":"Timeslot Availability"},"cateringCapacity":{"type":"integer","description":"Catering capacity"},"resourceChecks":{"type":"array","items":{"type":"string","enum":["rooms","equipment","vehicles","meetingSpaces"]},"description":"Resource Management checks run for the request."}}},
"GroupSalesAnalyticsAiIntelligenceCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Sales Analytics & AI Intelligence Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"enquiries":{"type":"string","description":"Enquiries"},"quotes":{"type":"string","description":"Quotes"},"conversionRate":{"type":"number","description":"Conversion Rate"},"groupBookings":{"type":"string","description":"Group Bookings"},"guests":{"type":"string","description":"Guests"},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue"},"averageGroupSize":{"type":"number","description":"Average Group Size"},"averageBookingValue":{"type":"number","description":"Average Booking Value"},"discount":{"type":"number","description":"Discount %"},"revenuePerGuest":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue per Guest"},"cancellationRate":{"type":"number","description":"Cancellation Rate"},"noShowRate":{"type":"number","description":"No-Show Rate"},"outstandingReceivables":{"type":"string","description":"Outstanding Receivables"},"repeatCustomerRate":{"type":"number","description":"Repeat Customer Rate"},"additionalGroups":{"type":"string","description":"Additional groups"},"capacityUtilization":{"type":"integer","description":"Capacity utilization"},"discountCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount cost"},"expectedContribution":{"type":"string","description":"Expected contribution"}}},
"GroupSalesCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Sales Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"newEnquiries":{"type":"integer","description":"New Enquiries"},"quotationsOutstanding":{"type":"string","description":"Quotations Outstanding"},"quotesAwaitingApproval":{"type":"string","description":"Quotes Awaiting Approval"},"confirmedGroups":{"type":"integer","description":"Confirmed Groups"},"expectedGuests":{"type":"integer","description":"Expected Guests"},"pipelineValue":{"type":"string","description":"Pipeline Value"},"confirmedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Confirmed Revenue"},"conversionRate":{"type":"number","description":"Conversion Rate"},"averageGroupValue":{"type":"number","description":"Average Group Value"},"expiringQuotes":{"type":"integer","description":"Expiring Quotes"},"salesTargetAchievement":{"type":"string","description":"Sales Target Achievement"},"enquiryId":{"type":"string","description":"Enquiry ID"},"organizationCustomer":{"type":"string","description":"Organization/Customer"},"groupType":{"type":"string","description":"Group Type"},"eventAttraction":{"type":"string","description":"Event/Attraction"},"visitDate":{"type":"string","format":"date-time","description":"Visit Date"},"guestCount":{"type":"integer","description":"Guest Count"},"salesOwner":{"type":"string","description":"Sales Owner"},"estimatedValue":{"type":"string","description":"Estimated Value"},"quoteStatus":{"type":"string","description":"Quote Status"},"probability":{"type":"string","description":"Probability"},"nextAction":{"type":"string","format":"date-time","description":"Next Action"},"expectedCloseDate":{"type":"string","format":"date-time","description":"Expected Close Date"},"followUpsDue":{"type":"string","description":"Follow-ups due"},"quotesExpiring":{"type":"string","description":"Quotes expiring"},"customerResponses":{"type":"integer","description":"Customer responses"},"approvalRequests":{"type":"integer","description":"Approval requests"},"depositsPending":{"type":"integer","description":"Deposits pending"}}},
"QuoteRevisionNegotiationVersionManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Quote Revision, Negotiation & Version Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"customerRequest":{"type":"string","description":"Customer Request"},"internalResponse":{"type":"string","description":"Internal Response"},"priceChange":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price Change"},"quantityChange":{"type":"integer","description":"Quantity Change"},"packageChange":{"type":"string","description":"Package Change"},"termsChange":{"type":"string","description":"Terms Change"},"date":{"type":"string","format":"date-time","description":"Date"},"user":{"type":"string","description":"User"},"quoteNumber":{"type":"string","description":"Quote number"},"version":{"type":"integer","description":"Version"},"versionStatus":{"type":"string","enum":["draft","sent","superseded","accepted","rejected"],"description":"Version status"}}},
"QuoteToBookingConversionConfirmationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Quote-to-Booking Conversion & Confirmation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"groupBookingId":{"type":"string","description":"Group Booking ID"},"customer":{"type":"string","description":"Customer"},"visitEvent":{"type":"string","description":"Visit/Event"},"products":{"type":"string","description":"Products"},"quantity":{"type":"integer","description":"Quantity"},"agreedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Agreed Price"},"paymentSchedule":{"type":"string","description":"Payment Schedule"},"operationalRequirements":{"type":"string","description":"Operational Requirements"},"salesOwner":{"type":"string","description":"Sales Owner"},"bookingConfirmation":{"type":"string","description":"Booking Confirmation"},"paymentInstructions":{"type":"string","description":"Payment Instructions"},"depositRequest":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Deposit Request"},"nextSteps":{"type":"string","format":"date-time","description":"Next Steps"},"orderId":{"type":"string","description":"TICVAI Order"},"customerPortalLink":{"type":"string","description":"Customer Portal Link where applicable"},"failedChecks":{"type":"array","items":{"type":"string","enum":["quoteExpired","capacityUnavailable","resourcesUnavailable","priceNotApproved","approvalInvalid","customerDetailsIncomplete","depositRuleMissing","guestCountInvalid"]},"description":"Conversion checks that fail; empty means the quote converts."}}},
"UpdateGroupBookingRequest": {"type":"object","description":"Request only. Every field optional; absent means unchanged.","properties":{"packageProductId":{"type":"string","nullable":true,"description":"The school-trip format or party package."},"yearGroup":{"type":"string","maxLength":40,"nullable":true},"accessAndDietaryNeeds":{"type":"string","maxLength":1000,"nullable":true},"celebrantName":{"type":"string","maxLength":120,"nullable":true,"description":"The birthday child."},"celebrantTurningAge":{"type":"integer","minimum":1,"maximum":18,"nullable":true},"allergiesAndRequests":{"type":"string","maxLength":1000,"nullable":true},"finalHeadcountDueBy":{"type":"string","format":"date-time","nullable":true},"leaderSubjectId":{"type":"string","format":"uuid"},"organisationName":{"type":"string","maxLength":200,"nullable":true},"expectedSize":{"type":"integer","minimum":2},"confirmedSize":{"type":"integer","minimum":0},"minimumSize":{"type":"integer","minimum":1,"nullable":true},"attendeeCaptureRequired":{"type":"boolean"},"attendeeCaptureDueBy":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["confirmed","namesPending","complete","cancelled"]}}}
}
```
