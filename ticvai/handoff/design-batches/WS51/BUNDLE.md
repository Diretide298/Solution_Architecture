# WS51 — Promotions   Bundles Management board 7

**10 screens · 11 operations · 13 schemas · 3 permissions**

Platform P09 TICVAI Web · ships as **ticvai-control** ·
platformAdmin audience · web ·
online only

## Who this is for

**platformAdmin on web.** Everything below is how you know what is
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
  `ORDER_CREATE, PRICE_CONFIGURE, PRICE_VIEW`. A control nobody can use must say so,
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
| `ADM-198` | Targeting & Eligibility Command Center | B–D | 2 | 2 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-199` | Eligibility Rule Builder | A | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-200` | CRM & Customer Segment Manager | B–D | 0 | 16 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-201` | Membership, Loyalty & Guest Eligibility | B–D | 0 | 0 | 6 | 0 | 0 | 2 | — | notStarted (generated) |
| `ADM-202` | Behavioral & Transaction Targeting | B–D | 6 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-203` | Context, Location, Channel & Time Targeting | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-204` | Partner, B2B & Payment Eligibility | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-205` | Audience Preview, Reach & Eligibility Simulator | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-206` | Targeting Conflict, Frequency & Exclusion Controls | B–D | 6 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-207` | AI Audience Discovery & Targeting Optimization | B–D | 0 | 0 | 6 | 2 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-199, ADM-200, ADM-201, ADM-203, ADM-204, ADM-207 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-198` Targeting & Eligibility Command Center

**Provide centralized visibility into all promotion audiences, eligibility rules, segments, targeting strategies, and their performance.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Each rule shows) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/targeting-eligibility-command-center-adm-198` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search targeting eligibility | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by guest type, crm segment, membership, loyalty, demographic, behavioral and 8 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Guest type | text field | — | — | `listTargetingEligibility` ?guestType |
| Crm segment | text field | — | — | `listTargetingEligibility` ?crmSegment |
| Membership | text field | — | — | `listTargetingEligibility` ?membership |
| Loyalty | text field | — | — | `listTargetingEligibility` ?loyalty |
| Demographic | text field | — | — | `listTargetingEligibility` ?demographic |
| Behavioral | text field | — | — | `listTargetingEligibility` ?behavioral |
| Transaction | text field | — | — | `listTargetingEligibility` ?transaction |
| Geographic | text field | — | — | `listTargetingEligibility` ?geographic |
| Channel | text field | — | — | `listTargetingEligibility` ?channel |
| Partner | text field | — | — | `listTargetingEligibility` ?partner |
| B2B | text field | — | — | `listTargetingEligibility` ?b2b |
| Payment | text field | — | — | `listTargetingEligibility` ?payment |
| Contextual | text field | — | — | `listTargetingEligibility` ?contextual |
| AI generated | text field | — | — | `listTargetingEligibility` ?aiGenerated |

#### Outputs: what the screen shows and produces

**Shown**

**Active Targeting Rules** (metric tile)

**Active Segments** (metric tile)

**Promotions Using Targeting** (metric tile)

**Bundles Using Targeting** (metric tile)

**Eligible Customers** (metric tile)

**Targeted Customers** (metric tile)

**Personalized Offers** (metric tile)

**Eligibility Pass Rate** (metric tile)

**Conversion Rate** (metric tile)

**Targeted Revenue** (metric tile)

**AOV Uplift** (metric tile)

**AI-Recommended Segments** (metric tile)

**Every targeting eligibility** (data table, from `listTargetingEligibility`)

| Shows | Format | Notes |
|---|---|---|
| Rule health | chip: Healthy, Warning, Conflict, No audience, Oversized audience, Expired… | Health of the targeting rule. |

**The selected targeting eligibility** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Rule health | chip: Healthy, Warning, Conflict, No audience, Oversized audience, Expired… | Health of the targeting rule. |

**Data it reads**: `listTargetingEligibility` (onLoad, Targeting & Eligibility Command Center)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-199` Eligibility Rule Builder: *Works in Eligibility Rule Builder*; calls `listTargetingEligibility`
- → `ADM-200` CRM & Customer Segment Manager: *Works in CRM & Customer Segment Manager*; calls `listTargetingEligibility`
- → `ADM-201` Membership, Loyalty & Guest Eligibility: *Works in Membership, Loyalty & Guest Eligibility*; calls `listTargetingEligibility`
- → `ADM-202` Behavioral & Transaction Targeting: *Works in Behavioral & Transaction Targeting*; calls `listTargetingEligibility`
- → `ADM-203` Context, Location, Channel & Time Targeting: *Works in Context, Location, Channel & Time Targeting*; calls `listTargetingEligibility`
- → `ADM-204` Partner, B2B & Payment Eligibility: *Works in Partner, B2B & Payment Eligibility*; calls `listTargetingEligibility`
- → `ADM-205` Audience Preview, Reach & Eligibility Simulator: *Works in Audience Preview, Reach & Eligibility Simulator*; calls `listTargetingEligibility`
- → `ADM-206` Targeting Conflict, Frequency & Exclusion Controls: *Works in Targeting Conflict, Frequency & Exclusion Controls*; calls `listTargetingEligibility`
- → `ADM-207` AI Audience Discovery & Targeting Optimization: *Works in AI Audience Discovery & Targeting Optimization*; calls `listTargetingEligibility`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The targeting eligibility list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the targeting eligibility untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No targeting eligibility yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the targeting eligibility are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listTargetingEligibility` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-198` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-198`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 1: Opens Targeting & Eligibility Command Center → Provide centralized visibility into all promotion audiences, eligibility rules, segments, targeting strategies, and their performance.
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F160 branch at step 1 (expected): when Nothing has been set up on Targeting & Eligibility Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F160 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-198?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-199`, `ADM-200`, `ADM-201`, `ADM-202`, `ADM-203`, `ADM-204`, `ADM-205`, `ADM-206`, `ADM-207`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-199` Eligibility Rule Builder

**Provide a no-code rule engine for determining promotion eligibility.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block A · ticket #20657 (APP-SETUP-ADM-199) |
| Who uses it | ticvai staff holding `ORDER_CREATE`, `PRICE_CONFIGURE` (1 operate, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/eligibility-rule-builder-adm-199` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Multiple condition sets. Each needs an operation, or needs removing from the screen; this is the Phase 3 … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Multiple condition sets (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-198` Targeting & Eligibility Command Center: *Returns to the board's landing screen*; calls `setEligibilityRule`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The eligibility rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the eligibility rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No eligibility rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the eligibility rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setEligibilityRule` → `PRICE_CONFIGURE` (configure) · staff
- `setResaleEligibilityRule` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Eligibility rules are configurable: residency/nationality/geography (e.g. UAE-resident-only with Emirates ID capture), minimum age (date-of-birth check), guest-profile category (e.g. VIP-only) and minimum loyalty points/spend for a membership tier. *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-463)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-199` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-199`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 2: Works in Eligibility Rule Builder → Provide a no-code rule engine for determining promotion eligibility.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-199?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Multiple condition sets, Cancel.
- [ ] Every transition is wired: `ADM-198`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `PRICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-200` CRM & Customer Segment Manager

**Connect promotion eligibility directly to TICVAI CRM segmentation. The board should consume CRM segments rather than recreate CRM functionality.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/crm-customer-segment-manager-adm-200` |

**Known gaps.** **CRM & Customer Segment Manager declares no operation that writes anything** — its only declared call is `listCrmCustomerSegment`, a read. The name promises authoring and the contract offers none …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every crm customer segment** (data table, from `listCrmCustomerSegment`)

| Shows | Format | Notes |
|---|---|---|
| Segment name | text | Segment name |
| Source | chip: Ticvai crm, Imported segment, External crm, External cdp, Membership, Loyalty… | Where the segment comes from. |
| Estimated audience | text | Estimated audience |
| Last refreshed | 1 Oct 2026, 14:30 | Last refreshed |
| Promotions using segment | text | Promotions using segment |
| Conversion | 1,234.5 | Conversion |
| Revenue | AED 1,234.50 | Revenue |
| Status | 1,234 | Status |

**The selected crm customer segment** (detail panel): The pack groups this record's detail under its own headings: “Segment Sources”.

| Shows | Format | Notes |
|---|---|---|
| Segment name | text | Segment name |
| Source | chip: Ticvai crm, Imported segment, External crm, External cdp, Membership, Loyalty… | Where the segment comes from. |
| Estimated audience | text | Estimated audience |
| Last refreshed | 1 Oct 2026, 14:30 | Last refreshed |
| Promotions using segment | text | Promotions using segment |
| Conversion | 1,234.5 | Conversion |
| Revenue | AED 1,234.50 | Revenue |
| Status | 1,234 | Status |

**Data it reads**: `listCrmCustomerSegment` (onLoad, CRM & Customer Segment Manager)

**Where the user goes next**

- → `ADM-198` Targeting & Eligibility Command Center: *Returns to the board's landing screen*; calls `listCrmCustomerSegment`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The crm customer segment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the crm customer segment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No crm customer segment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the crm customer segment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCrmCustomerSegment` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-200` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-200`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 4: Works in CRM & Customer Segment Manager → Connect promotion eligibility directly to TICVAI CRM segmentation. The board should consume CRM segments rather than recreate CRM functionality.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-200?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-198`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-201` Membership, Loyalty & Guest Eligibility

**Configure targeting based on membership, loyalty status, guest categories, and entitlement relationships.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/membership-loyalty-guest-eligibility-adm-201` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listMembershipLoyaltyGuest` (onLoad, Membership, Loyalty & Guest Eligibility)

**Where the user goes next**

- → `ADM-198` Targeting & Eligibility Command Center: *Returns to the board's landing screen*; calls `listMembershipLoyaltyGuest`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership loyalty guest list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership loyalty guest untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership loyalty guest yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the membership loyalty guest are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listMembershipLoyaltyGuest` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A94** Hold the loyalty workshop and define the full programme configuration (tiers, point accrual, redemption, expiry, benefit unlocks) *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'loyalty')*
- **A134** Build the eligibility rules engine (residency/nationality with ID capture, minimum age by DOB, VIP-only profiles, loyalty-points thresholds, purchase limits per order/guest/category/channel) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'loyalty')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-201` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-201`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 6: Works in Membership, Loyalty & Guest Eligibility → Configure targeting based on membership, loyalty status, guest categories, and entitlement relationships.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-201?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-198`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-202` Behavioral & Transaction Targeting

**Target promotions according to what the guest has previously purchased or done.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/behavioral-transaction-targeting-adm-202` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Last 7 days | select field | — | — | — | — | — | — |
| 30 days | select field | — | — | — | — | — | — |
| 90 days | select field | — | — | — | — | — | — |
| 12 months | select field | — | — | — | — | — | — |
| Lifetime | select field | — | — | — | — | — | — |
| Custom period | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listBehavioralTransactionTargeting` (onLoad, Behavioral & Transaction Targeting)

**Where the user goes next**

- → `ADM-198` Targeting & Eligibility Command Center: *Returns to the board's landing screen*; calls `listBehavioralTransactionTargeting`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The behavioral transaction targeting configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the behavioral transaction targeting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No behavioral transaction targeting configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listBehavioralTransactionTargeting` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-202` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-202`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 8: Works in Behavioral & Transaction Targeting → Target promotions according to what the guest has previously purchased or done.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-202?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-198`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-203` Context, Location, Channel & Time Targeting

**Determine promotion eligibility according to the customer's current commercial context.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/context-location-channel-time-targeting-adm-203` |

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Product currently viewed, Current booking. Each needs an operation, or needs removing from the screen; this … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Product currently viewed (primary button) | navigation or local | — | — | — | — |
| Current booking (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listContextLocationChannel` (onLoad, Context, Location, Channel & Time Targeting)

**Where the user goes next**

- → `ADM-198` Targeting & Eligibility Command Center: *Returns to the board's landing screen*; calls `listContextLocationChannel`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The context location channel list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the context location channel untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No context location channel yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the context location channel are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listContextLocationChannel` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-203` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-203`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 10: Works in Context, Location, Channel & Time Targeting → Determine promotion eligibility according to the customer's current commercial context.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-203?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Product currently viewed, Current booking.
- [ ] Every transition is wired: `ADM-198`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-204` Partner, B2B & Payment Eligibility

**Configure eligibility for partner, corporate, reseller, B2B, and payment-related campaigns.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/partner-b2b-payment-eligibility-adm-204` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listPartnerPaymentEligibility` (onLoad, Partner, B2B & Payment Eligibility)

**Where the user goes next**

- → `ADM-198` Targeting & Eligibility Command Center: *Returns to the board's landing screen*; calls `listPartnerPaymentEligibility`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner b2b payment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner b2b payment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner b2b payment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner b2b payment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPartnerPaymentEligibility` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-204` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-204`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 12: Works in Partner, B2B & Payment Eligibility → Configure eligibility for partner, corporate, reseller, B2B, and payment-related campaigns.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-204?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-198`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-205` Audience Preview, Reach & Eligibility Simulator

**Allow administrators to understand exactly who will qualify before activating the targeting rule. This is a critical safeguard.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Audience Metrics) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/audience-preview-reach-eligibility-simulator-adm-205` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Estimated audience** (metric tile)

**Percentage of customer base** (metric tile)

**Historical conversion** (metric tile)

**Historical AOV** (metric tile)

**Expected redemptions** (metric tile)

**Estimated promotion cost** (metric tile)

**Estimated revenue** (metric tile)

**Data it reads**: `listAudiencePreviewReach` (onLoad, Audience Preview, Reach & Eligibility Simulator)

**Where the user goes next**

- → `ADM-198` Targeting & Eligibility Command Center: *Returns to the board's landing screen*; calls `listAudiencePreviewReach`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The audience preview reach list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the audience preview reach untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No audience preview reach yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the audience preview reach are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAudiencePreviewReach` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-205` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-205`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 14: Works in Audience Preview, Reach & Eligibility Simulator → Allow administrators to understand exactly who will qualify before activating the targeting rule. This is a critical safeguard.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-205?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-198`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-206` Targeting Conflict, Frequency & Exclusion Controls

**Prevent customers from being over-targeted and prevent inappropriate promotional eligibility.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/targeting-conflict-frequency-exclusion-controls-adm-206` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Existing member, Specific CRM segment, Partner restriction, Product ownership. Each needs an operation, or …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Maximum offers per day | text field | — | — | — | — | — | — |
| Maximum offers per week | text field | — | — | — | — | — | — |
| Maximum campaigns per month | text field | — | — | — | — | — | — |
| Maximum redemptions | select field | — | — | — | — | — | — |
| Cooling-off period | select field | — | — | — | — | — | — |
| Repeat campaign restriction | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Existing member (primary button) | navigation or local | — | — | — | — |
| Specific CRM segment (secondary button) | navigation or local | — | — | — | — |
| Partner restriction (secondary button) | navigation or local | — | — | — | — |
| Product ownership (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listTargetingConflictFrequency` (onLoad, Targeting Conflict, Frequency & Exclusion Controls)

**Where the user goes next**

- → `ADM-198` Targeting & Eligibility Command Center: *Returns to the board's landing screen*; calls `listTargetingConflictFrequency`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The targeting conflict frequency configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the targeting conflict frequency untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No targeting conflict frequency configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listTargetingConflictFrequency` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-206` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-206`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 16: Works in Targeting Conflict, Frequency & Exclusion Controls → Prevent customers from being over-targeted and prevent inappropriate promotional eligibility.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-206?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Existing member, Specific CRM segment, Partner restriction, Product ownership.
- [ ] Every transition is wired: `ADM-198`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-207` AI Audience Discovery & Targeting Optimization

**Use TICVAI's AI layer to identify customer audiences and promotion opportunities that business users may not have manually defined. Board 8 shall provide TICVAI with the centralized Promotion Decision Engine responsible for determining what happens when multiple promotions, discounts, coupons, bundles, loyalty benefits, membership benefits, payment offers, BOGO mechanics, partner offers, or special prices qualify for the same transaction. This is one of the most important boards in the Promotions module because the previous boards may all produce valid offers simultaneously. For example, a guest could qualify for: Annual Pass Holder — 15% discount SUMMER20 coupon — 20% discount Emirates NBD card — 10% discount Buy 4 Pay 3 — promotional mechanic Loyalty Gold — 5% benefit Can they combine? In what order? Which promotion wins? What is the maximum permitted benefit? The matrix explicitly requires configurable promotion hierarchy, stacking and conflict resolution, including scenarios where promotions are combined, mutually exclusive, or prioritized, with clear explanation of which promotion was applied and why. Board 8 shall contain 10 backend screens.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/ai-audience-discovery-targeting-optimization-adm-207` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Audience size: 126,500. Each needs attaching to the control it gates, or the screen needs the control.

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listAudienceDiscoveryTargeting` (onLoad, AI Audience Discovery & Targeting Optimization)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The audience discovery targeting list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the audience discovery targeting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No audience discovery targeting yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the audience discovery targeting are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAudienceDiscoveryTargeting` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.31 | System shall provide customer-segment-based discount recommendations. | Unified Operations Dashboard | CONTRACTED | `listAudienceDiscoveryTargeting` |
| 22.14.11 | AI Audience Discovery | Marketing & CRM | CONTRACTED | `listAudienceDiscoveryTargeting` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-207` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-207`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 7
- Flow F160 *Promotions Bundles Management board 7: Targeting & Eligibility Command Center*, step 18: Works in AI Audience Discovery & Targeting Optimization → Use TICVAI's AI layer to identify customer audiences and promotion opportunities that business users may not have manually defined. Board 8 shall provide TICVAI with the centralized Promotion …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-207?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P09 reference designs** (from `handoff/design-batches/apps/6-ticvai-controller/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

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

### Across P09 TICVAI Web

- Portal access exposes TICVAI pricing, so prospects submit contact details and a trade license as proof of a real venue, reviewed and approved by TICVAI before access is granted. *(agreed · MoM 10 Sep 2026, 4.8 Customer Portal Access, Authentication & Verification · DI-827)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listAudienceDiscoveryTargeting": {"method":"GET","path":"/audience-discovery-targeting","contract":"promotions","summary":"AI Audience Discovery & Targeting Optimization","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiAudienceDiscoveryTargetingOptimizationView"},
"listAudiencePreviewReach": {"method":"GET","path":"/audience-preview-reach","contract":"promotions","summary":"Audience Preview, Reach & Eligibility Simulator","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AudiencePreviewReachEligibilitySimulatorView"},
"listBehavioralTransactionTargeting": {"method":"GET","path":"/behavioral-transaction-targeting","contract":"promotions","summary":"Behavioral & Transaction Targeting","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"BehavioralTransactionTargetingView"},
"listContextLocationChannel": {"method":"GET","path":"/context-location-channel","contract":"promotions","summary":"Context, Location, Channel & Time Targeting","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ContextLocationChannelTimeTargetingView"},
"listCrmCustomerSegment": {"method":"GET","path":"/crm-customer-segment","contract":"promotions","summary":"CRM & Customer Segment Manager","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CrmCustomerSegmentManagerView"},
"listMembershipLoyaltyGuest": {"method":"GET","path":"/membership-loyalty-guest","contract":"promotions","summary":"Membership, Loyalty & Guest Eligibility","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MembershipLoyaltyGuestEligibilityView"},
"listPartnerPaymentEligibility": {"method":"GET","path":"/partner-payment-eligibility","contract":"promotions","summary":"Partner, B2B & Payment Eligibility","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PartnerB2bPaymentEligibilityView"},
"listTargetingConflictFrequency": {"method":"GET","path":"/targeting-conflict-frequency","contract":"promotions","summary":"Targeting Conflict, Frequency & Exclusion Controls","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TargetingConflictFrequencyExclusionControlsView"},
"listTargetingEligibility": {"method":"GET","path":"/targeting-eligibility","contract":"promotions","summary":"Targeting & Eligibility Command Center","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"guestType","in":"query","required":false},{"name":"crmSegment","in":"query","required":false},{"name":"membership","in":"query","required":false},{"name":"loyalty","in":"query","required":false},{"name":"demographic","in":"query","required":false},{"name":"behavioral","in":"query","required":false},{"name":"transaction","in":"query","required":false},{"name":"geographic","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"partner","in":"query","required":false},{"name":"b2b","in":"query","required":false},{"name":"payment","in":"query","required":false},{"name":"contextual","in":"query","required":false},{"name":"aiGenerated","in":"query","required":false}],"requestBody":null,"responds":"TargetingEligibilityCommandCenterView"},
"setEligibilityRule": {"method":"PUT","path":"/eligibility-rule","contract":"promotions","summary":"Eligibility Rule Builder","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"EligibilityRuleBuilderInput","responds":"EligibilityRuleBuilderView"},
"setResaleEligibilityRule": {"method":"PUT","path":"/resale-eligibility-rule","contract":"orders","summary":"Resale Eligibility Rule Configuration","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"ResaleEligibilityRuleConfigurationInput","responds":"ResaleEligibilityRuleConfigurationView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiAudienceDiscoveryTargetingOptimizationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What AI Audience Discovery & Targeting Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"narrowAudience":{"type":"string","description":"Narrow audience"},"expandAudience":{"type":"string","description":"Expand audience"},"excludeLowValueSegment":{"type":"string","description":"Exclude low-value segment"},"changeEligibility":{"type":"string","description":"Change eligibility"},"changeChannel":{"type":"string","description":"Change channel"},"changeTiming":{"type":"string","description":"Change timing"},"changePromotion":{"type":"string","description":"Change promotion"},"reduceFrequency":{"type":"string","description":"Reduce frequency"},"membershipTierEligibility":{"type":"string","description":"Membership/tier eligibility"},"membershipAndLoyaltyEligibility":{"type":"string","description":"Membership and loyalty eligibility"},"audienceName":{"type":"string","description":"Discovered audience"},"audienceSize":{"type":"integer","description":"Audience size"},"suggestedOffer":{"type":"string","description":"Suggested offer"},"predictedConversion":{"type":"number","description":"Predicted conversion, percent"},"estimatedIncrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Estimated incremental revenue"},"rationale":{"type":"string","description":"Why this audience (explainable factors)"}}},
"AudiencePreviewReachEligibilitySimulatorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Audience Preview, Reach & Eligibility Simulator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"estimatedAudience":{"type":"string","description":"Estimated audience"},"percentageOfCustomerBase":{"type":"number","description":"Percentage of customer base"},"historicalConversion":{"type":"number","description":"Historical conversion"},"historicalAov":{"type":"string","description":"Historical AOV"},"expectedRedemptions":{"type":"integer","description":"Expected redemptions"},"estimatedPromotionCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Estimated promotion cost"},"estimatedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Estimated revenue"},"sampleProfileResult":{"type":"array","items":{"type":"string"},"description":"Sample profiles tested and whether each is eligible"}}},
"BehavioralTransactionTargetingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Behavioral & Transaction Targeting displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"previousProductPurchased":{"type":"string","description":"Previous product purchased"},"previousAttractionVisited":{"type":"string","description":"Previous attraction visited"},"visitFrequency":{"type":"string","description":"Visit frequency"},"daysSinceLastVisit":{"type":"string","description":"Days since last visit"},"previousPromotionRedemption":{"type":"string","description":"Previous promotion redemption"},"abandonedCart":{"type":"string","description":"Abandoned cart"},"bookingFrequency":{"type":"string","description":"Booking frequency"},"purchaseFrequency":{"type":"string","description":"Purchase frequency"},"averageTransactionValue":{"type":"number","description":"Average transaction value"},"totalCustomerValue":{"type":"integer","description":"Total customer value"},"productAffinity":{"type":"string","description":"Product affinity"},"lifetimeSpend":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Lifetime spend"},"averageBasket":{"type":"number","description":"Average basket"},"numberOfTransactions":{"type":"integer","description":"Number of transactions"},"lastPurchase":{"type":"string","format":"date-time","description":"Last purchase"},"purchaseChannel":{"type":"string","description":"Purchase channel"},"productMix":{"type":"string","description":"Product mix"},"lifetime":{"type":"string","description":"Lifetime"},"lookbackPeriod":{"type":"string","enum":["last7Days","last30Days","last90Days","lastYear","customPeriod"],"description":"Look-back period for behavioural conditions"}}},
"ContextLocationChannelTimeTargetingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Context, Location, Channel & Time Targeting displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"businessEntity":{"type":"string","description":"Business entity"},"venue":{"type":"string","description":"Venue"},"attraction":{"type":"string","description":"Attraction"},"operatingArea":{"type":"string","description":"Operating area"},"marketCountry":{"type":"string","description":"Market/country"},"salesLocation":{"type":"string","description":"Sales location"},"purchaseDate":{"type":"string","format":"date-time","description":"Purchase date"},"visitDate":{"type":"string","format":"date-time","description":"Visit date"},"day":{"type":"string","description":"Day"},"time":{"type":"string","format":"date-time","description":"Time"},"season":{"type":"string","description":"Season"},"event":{"type":"string","description":"Event"},"holiday":{"type":"string","description":"Holiday"},"campaignPeriod":{"type":"string","format":"date-time","description":"Campaign period"},"currentBasket":{"type":"string","description":"Current basket"},"productCurrentlyViewed":{"type":"string","description":"Product currently viewed"},"currentBooking":{"type":"string","description":"Current booking"},"visitState":{"type":"string","description":"Visit state"},"inVenueState":{"type":"string","description":"In-venue state where available"},"channels":{"type":"array","items":{"type":"string","enum":["b2cWebsite","mobileApp","pos","mobilePos","kiosk","b2b","callCenter","api","ota","reseller","partner"]},"description":"Channels that qualify."}}},
"CrmCustomerSegmentManagerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What CRM & Customer Segment Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"segmentName":{"type":"string","description":"Segment name"},"estimatedAudience":{"type":"string","description":"Estimated audience"},"lastRefreshed":{"type":"string","format":"date-time","description":"Last refreshed"},"promotionsUsingSegment":{"type":"string","description":"Promotions using segment"},"conversion":{"type":"number","description":"Conversion"},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue"},"status":{"type":"integer","description":"Status"},"source":{"type":"string","enum":["ticvaiCrm","importedSegment","externalCrm","externalCdp","membership","loyalty","b2bAccounts","marketingAutomation"],"description":"Where the segment comes from."}}},
"EligibilityRuleBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; saved as a `promotions.promotion_rule` row (PromotionRule, ruleType eligibility, its criteria as the condition group and ruleEffect as effect) (DM5, 29 September: data model for the agreed operations)","description":"**What Eligibility Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"guestType":{"type":"string","description":"Guest type"},"customerSegment":{"type":"string","description":"Customer segment"},"ageCategory":{"type":"string","description":"Age/category"},"membership":{"type":"string","description":"Membership"},"loyaltyTier":{"type":"string","description":"Loyalty tier"},"purchaseHistory":{"type":"string","description":"Purchase history"},"visitHistory":{"type":"string","description":"Visit history"},"transactionValue":{"type":"string","description":"Transaction value"},"productPurchased":{"type":"string","description":"Product purchased"},"channel":{"type":"string","description":"Channel"},"venue":{"type":"string","description":"Venue"},"location":{"type":"string","description":"Location"},"partner":{"type":"string","description":"Partner"},"dateTime":{"type":"string","format":"date-time","description":"Date/time"},"paymentMethod":{"type":"string","description":"Payment method"},"campaign":{"type":"string","description":"Campaign"},"customerAccountAttributes":{"type":"string","description":"Customer/account attributes"},"nestedGroups":{"type":"string","description":"Nested groups"},"multipleConditionSets":{"type":"string","description":"Multiple condition sets"},"ruleEffect":{"type":"string","enum":["include","exclude"],"description":"Whether matching guests are included or excluded."}}},
"EligibilityRuleBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Eligibility Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"guestType":{"type":"string","description":"Guest type"},"customerSegment":{"type":"string","description":"Customer segment"},"ageCategory":{"type":"string","description":"Age/category"},"membership":{"type":"string","description":"Membership"},"loyaltyTier":{"type":"string","description":"Loyalty tier"},"purchaseHistory":{"type":"string","description":"Purchase history"},"visitHistory":{"type":"string","description":"Visit history"},"transactionValue":{"type":"string","description":"Transaction value"},"productPurchased":{"type":"string","description":"Product purchased"},"channel":{"type":"string","description":"Channel"},"venue":{"type":"string","description":"Venue"},"location":{"type":"string","description":"Location"},"partner":{"type":"string","description":"Partner"},"dateTime":{"type":"string","format":"date-time","description":"Date/time"},"paymentMethod":{"type":"string","description":"Payment method"},"campaign":{"type":"string","description":"Campaign"},"customerAccountAttributes":{"type":"string","description":"Customer/account attributes"},"nestedGroups":{"type":"string","description":"Nested groups"},"multipleConditionSets":{"type":"string","description":"Multiple condition sets"},"ruleEffect":{"type":"string","enum":["include","exclude"],"description":"Whether matching guests are included or excluded."}}},
"MembershipLoyaltyGuestEligibilityView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Membership, Loyalty & Guest Eligibility displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"membershipType":{"type":"string","description":"Membership type"},"membershipTier":{"type":"string","description":"Membership tier"},"membershipStatus":{"type":"string","description":"Membership status"},"membershipStartDate":{"type":"string","format":"date-time","description":"Membership start date"},"renewalStatus":{"type":"string","description":"Renewal status"},"expiryDate":{"type":"string","format":"date-time","description":"Expiry date"},"membershipTenure":{"type":"string","description":"Membership tenure"},"loyaltyTier":{"type":"string","description":"Loyalty tier"},"pointsBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Points balance"},"pointsEarned":{"type":"string","description":"Points earned"},"pointsRedeemed":{"type":"string","description":"Points redeemed"},"loyaltyActivity":{"type":"string","description":"Loyalty activity"},"tierProgression":{"type":"string","description":"Tier progression"},"guestCategories":{"type":"array","items":{"type":"string","enum":["adult","child","senior","family","student","resident","tourist","group","vip"]},"description":"Guest categories that qualify."},"tierBenefits":{"type":"array","items":{"type":"string"},"description":"Benefit per loyalty tier, for example Bronze 5%, Silver 10%, Gold 15%"}}},
"PartnerB2bPaymentEligibilityView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Partner, B2B & Payment Eligibility displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"partner":{"type":"string","description":"Partner"},"partnerCategory":{"type":"string","description":"Partner category"},"corporateAccount":{"type":"string","description":"Corporate account"},"employer":{"type":"string","description":"Employer"},"hotel":{"type":"string","description":"Hotel"},"travelAgency":{"type":"string","description":"Travel agency"},"tourOperator":{"type":"string","description":"Tour operator"},"school":{"type":"string","description":"School"},"governmentEntity":{"type":"string","description":"Government entity"},"bank":{"type":"string","description":"Bank"},"b2bAccount":{"type":"string","description":"B2B account"},"masterAccount":{"type":"string","description":"Master account"},"subAccount":{"type":"string","description":"Sub-account"},"contract":{"type":"string","description":"Contract"},"customerGroup":{"type":"string","description":"Customer group"},"market":{"type":"string","description":"Market"},"salesChannel":{"type":"string","description":"Sales channel"},"paymentMethod":{"type":"string","description":"Payment method"},"eligibleCardProgram":{"type":"string","description":"Eligible card program"},"wallet":{"type":"string","description":"Wallet"},"loyaltyPayment":{"type":"string","description":"Loyalty payment"},"giftCard":{"type":"string","description":"Gift card"},"approvedPaymentPartner":{"type":"integer","description":"Approved payment partner"}}},
"ResaleEligibilityRuleConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; lands in `orders.resale_eligibility_rule` (DM5, 29 September)","description":"**What Resale Eligibility Rule Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"product":{"type":"string","description":"Product"},"ticketType":{"type":"string","description":"Ticket type"},"event":{"type":"string","description":"Event"},"venue":{"type":"string","description":"Venue"},"performance":{"type":"string","description":"Performance"},"membershipType":{"type":"string","description":"Membership type"},"salesChannel":{"type":"string","description":"Sales channel"},"customerSegment":{"type":"string","description":"Customer segment"},"priceCategory":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price category"},"promotion":{"type":"string","description":"Promotion"},"ticketStatus":{"type":"string","description":"Ticket status"},"paymentStatus":{"type":"string","description":"Payment status"},"ticketOwnershipStatus":{"type":"string","description":"Ticket ownership status"},"specificResaleStartEndDate":{"type":"string","format":"date-time","description":"Specific resale start/end date"},"blackoutPeriod":{"type":"string","format":"date-time","description":"Blackout period"},"maximumResaleAttempts":{"type":"integer","description":"Maximum resale attempts"},"maximumListingsPerCustomer":{"type":"string","description":"Maximum listings per customer"},"minimumOwnershipPeriod":{"type":"string","format":"date-time","description":"Minimum ownership period"},"identityVerificationRequirement":{"type":"string","description":"Identity verification requirement"},"originalPurchaserOnly":{"type":"string","description":"Original purchaser only"},"membershipRestriction":{"type":"string","description":"Membership restriction"},"resaleImmediatelyAfterPurchase":{"type":"boolean","description":"Allow resale immediately after purchase"},"requiredConditions":{"type":"array","items":{"type":"string","enum":["fullyPaid","notScanned","notExpired","eventNotStarted","notRefunded","notComplimentary","notStaff","notInternal","notBlocked","notUnderDispute"]},"description":"Conditions a ticket must meet to be listed."}}},
"ResaleEligibilityRuleConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Resale Eligibility Rule Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"product":{"type":"string","description":"Product"},"ticketType":{"type":"string","description":"Ticket type"},"event":{"type":"string","description":"Event"},"venue":{"type":"string","description":"Venue"},"performance":{"type":"string","description":"Performance"},"membershipType":{"type":"string","description":"Membership type"},"salesChannel":{"type":"string","description":"Sales channel"},"customerSegment":{"type":"string","description":"Customer segment"},"priceCategory":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price category"},"promotion":{"type":"string","description":"Promotion"},"ticketStatus":{"type":"string","description":"Ticket status"},"paymentStatus":{"type":"string","description":"Payment status"},"ticketOwnershipStatus":{"type":"string","description":"Ticket ownership status"},"specificResaleStartEndDate":{"type":"string","format":"date-time","description":"Specific resale start/end date"},"blackoutPeriod":{"type":"string","format":"date-time","description":"Blackout period"},"maximumResaleAttempts":{"type":"integer","description":"Maximum resale attempts"},"maximumListingsPerCustomer":{"type":"string","description":"Maximum listings per customer"},"minimumOwnershipPeriod":{"type":"string","format":"date-time","description":"Minimum ownership period"},"identityVerificationRequirement":{"type":"string","description":"Identity verification requirement"},"originalPurchaserOnly":{"type":"string","description":"Original purchaser only"},"membershipRestriction":{"type":"string","description":"Membership restriction"},"resaleImmediatelyAfterPurchase":{"type":"boolean","description":"Allow resale immediately after purchase"},"requiredConditions":{"type":"array","items":{"type":"string","enum":["fullyPaid","notScanned","notExpired","eventNotStarted","notRefunded","notComplimentary","notStaff","notInternal","notBlocked","notUnderDispute"]},"description":"Conditions a ticket must meet to be listed."}}},
"TargetingConflictFrequencyExclusionControlsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Targeting Conflict, Frequency & Exclusion Controls displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"maximumOffersPerDay":{"type":"string","description":"Maximum offers per day"},"maximumOffersPerWeek":{"type":"string","description":"Maximum offers per week"},"maximumCampaignsPerMonth":{"type":"string","description":"Maximum campaigns per month"},"maximumRedemptions":{"type":"string","description":"Maximum redemptions"},"coolingOffPeriod":{"type":"string","format":"date-time","description":"Cooling-off period"},"repeatCampaignRestriction":{"type":"string","description":"Repeat campaign restriction"},"alreadyPurchasedProduct":{"type":"string","description":"Already purchased product"},"alreadyRedeemedPromotion":{"type":"string","description":"Already redeemed promotion"},"existingMember":{"type":"string","description":"Existing member"},"employee":{"type":"string","description":"Employee"},"specificCrmSegment":{"type":"string","description":"Specific CRM segment"},"fraudRiskStatus":{"type":"string","description":"Fraud/risk status"},"accountType":{"type":"string","description":"Account type"},"partnerRestriction":{"type":"string","description":"Partner restriction"},"productOwnership":{"type":"string","description":"Product ownership"},"campaignExclusions":{"type":"string","description":"Campaign exclusions"},"partnerExclusions":{"type":"string","description":"Partner exclusions"},"operationalExclusions":{"type":"string","description":"Operational exclusions"}}},
"TargetingEligibilityCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Targeting & Eligibility Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"activeTargetingRules":{"type":"integer","description":"Active Targeting Rules"},"activeSegments":{"type":"integer","description":"Active Segments"},"promotionsUsingTargeting":{"type":"string","description":"Promotions Using Targeting"},"bundlesUsingTargeting":{"type":"string","description":"Bundles Using Targeting"},"eligibleCustomers":{"type":"integer","description":"Eligible Customers"},"targetedCustomers":{"type":"integer","description":"Targeted Customers"},"personalizedOffers":{"type":"integer","description":"Personalized Offers"},"eligibilityPassRate":{"type":"number","description":"Eligibility Pass Rate"},"conversionRate":{"type":"number","description":"Conversion Rate"},"targetedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Targeted Revenue"},"aovUplift":{"type":"number","description":"AOV Uplift"},"aiRecommendedSegments":{"type":"integer","description":"AI-Recommended Segments"},"ruleHealth":{"type":"string","enum":["healthy","warning","conflict","noAudience","oversizedAudience","expired","missingData"],"description":"Health of the targeting rule."}}}
}
```
