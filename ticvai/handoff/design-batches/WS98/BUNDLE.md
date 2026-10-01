# WS98 — Subscription Licensing AI Self Service board 1

**10 screens · 0 operations · 0 schemas · 0 permissions**

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

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
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
| `ADM-369` | Commercial Command Center | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-370` | Customer Subscription & Commercial Portfolio | B–D | 2 | 34 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-371` | Customer Commercial 360° | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-372` | Operational Profile, VSI & Commercial Model Intelligence | B–D | 0 | 0 | 6 | 2 | 2 | 0 | — | notStarted (—) |
| `ADM-373` | Revenue & Commercial Model Analytics | B–D | 0 | 10 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `ADM-374` | Trial & Conversion Monitor | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `ADM-375` | Renewal & Retention Center | B–D | 0 | 22 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-376` | Commercial Optimization & Expansion Opportunities | B–D | 0 | 12 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-377` | Subscription Exceptions & Commercial Alerts | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-378` | Executive AI Commercial Intelligence | B–D | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-371, ADM-377 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-369` Commercial Command Center

**Provide TICVAI management with a real-time executive overview of the entire subscription and commercial business.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Primary KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/tenants-licensing/commercial-command-center-adm-369` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Total Active Customers** (metric tile)

**Active Subscriptions** (metric tile)

**Active Trials** (metric tile)

**MRR / Monthly Equivalent Revenue** (metric tile)

**ARR / Annualized Contract Value** (metric tile)

**New Revenue** (metric tile)

**Expansion Revenue** (metric tile)

**Contraction Revenue** (metric tile)

**Churned Revenue** (metric tile)

**Renewal Rate** (metric tile)

**Trial-to-Paid Conversion** (metric tile)

**Average Revenue per Customer** (metric tile)

**Data it reads**: `listTenants` (onLoad, The commercial portfolio)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-370` Customer Subscription & Commercial Portfolio: *Customer Subscription & Commercial Portfolio*
- → `ADM-371` Customer Commercial 360°: *Customer Commercial 360°*
- → `ADM-372` Operational Profile, VSI & Commercial Model Intelligence: *Operational Profile, VSI & Commercial Model Intelligence*
- → `ADM-373` Revenue & Commercial Model Analytics: *Revenue & Commercial Model Analytics*
- → `ADM-374` Trial & Conversion Monitor: *Trial & Conversion Monitor*
- → `ADM-375` Renewal & Retention Center: *Renewal & Retention Center*
- → `ADM-376` Commercial Optimization & Expansion Opportunities: *Commercial Optimization & Expansion Opportunities*
- → `ADM-377` Subscription Exceptions & Commercial Alerts: *Subscription Exceptions & Commercial Alerts*
- → `ADM-378` Executive AI Commercial Intelligence: *Executive AI Commercial Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Licensing command centre: total customers, active subscriptions/tiers, MRR broken down by pricing model (tier-based, tier-plus-usage, per-ticket, per-transaction, hybrid, fixed, custom). *(client request · MoM 10 Sep 2026, 4.17 Licensing Command Center Overview · DI-838)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-369` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-369`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 1
- Flow F207 *Subscription Licensing AI Self Service board 1: Commercial Command Center*, step 1: Opens Commercial Command Center → Provide TICVAI management with a real-time executive overview of the entire subscription and commercial business.
- Flow F207 *Subscription Licensing AI Self Service board 1: Commercial Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F207 *Subscription Licensing AI Self Service board 1: Commercial Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F207 *Subscription Licensing AI Self Service board 1: Commercial Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F207 *Subscription Licensing AI Self Service board 1: Commercial Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F207 *Subscription Licensing AI Self Service board 1: Commercial Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F207 *Subscription Licensing AI Self Service board 1: Commercial Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F207 *Subscription Licensing AI Self Service board 1: Commercial Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F207 branch at step 1 (expected): when Nothing has been set up on Commercial Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F207 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-369?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-370`, `ADM-371`, `ADM-372`, `ADM-373`, `ADM-374`, `ADM-375`, `ADM-376`, `ADM-377`, `ADM-378`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-370` Customer Subscription & Commercial Portfolio

**Provide a central portfolio of every TICVAI customer and their current commercial position.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Table Columns) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/customer-subscription-commercial-portfolio-adm-370` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search customer subscription commercial | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by commercial model, operational profile, tier, country, venue, status and 6 more — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Shown**

**Every customer subscription commercial** (data table)

| Shows | Format | Notes |
|---|---|---|
| Customer | text | not in the schema: `Customer` |
| Venue / group | text | not in the schema: `Venue / Group` |
| Country | text | not in the schema: `Country` |
| VSI | text | not in the schema: `VSI` |
| Operational profile | text | not in the schema: `Operational Profile` |
| Commercial model | text | not in the schema: `Commercial Model` |
| Tier where applicable | text | not in the schema: `Tier where applicable` |
| Contracted rate | text | not in the schema: `Contracted Rate` |
| Minimum guarantee | text | not in the schema: `Minimum Guarantee` |
| Active modules | text | not in the schema: `Active Modules` |
| Monthly equivalent revenue | text | not in the schema: `Monthly Equivalent Revenue` |
| Billable volume | text | not in the schema: `Billable Volume` |
| Usage % | text | not in the schema: `Usage %` |
| Contract start | text | not in the schema: `Contract Start` |
| Renewal date | text | not in the schema: `Renewal Date` |
| Subscription status | text | not in the schema: `Subscription Status` |
| Commercial health | text | not in the schema: `Commercial Health` |

**The selected customer subscription commercial** (detail panel): The pack groups this record's detail under its own headings: “Enterprise Operational Profile”, “AED 20K/month minimum”, “Commercial Health Indicators”.

| Shows | Format | Notes |
|---|---|---|
| Customer | text | not in the schema: `Customer` |
| Venue / group | text | not in the schema: `Venue / Group` |
| Country | text | not in the schema: `Country` |
| VSI | text | not in the schema: `VSI` |
| Operational profile | text | not in the schema: `Operational Profile` |
| Commercial model | text | not in the schema: `Commercial Model` |
| Tier where applicable | text | not in the schema: `Tier where applicable` |
| Contracted rate | text | not in the schema: `Contracted Rate` |
| Minimum guarantee | text | not in the schema: `Minimum Guarantee` |
| Active modules | text | not in the schema: `Active Modules` |
| Monthly equivalent revenue | text | not in the schema: `Monthly Equivalent Revenue` |
| Billable volume | text | not in the schema: `Billable Volume` |
| Usage % | text | not in the schema: `Usage %` |
| Contract start | text | not in the schema: `Contract Start` |
| Renewal date | text | not in the schema: `Renewal Date` |
| Subscription status | text | not in the schema: `Subscription Status` |
| Commercial health | text | not in the schema: `Commercial Health` |

**Data it reads**: `listTenants` (onLoad, Subscriptions by tier)

**Where the user goes next**

- → `ADM-369` Commercial Command Center: *Back to Commercial Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer subscription commercial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer subscription commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer subscription commercial yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer subscription commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-370` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-370`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 1
- Flow F207 *Subscription Licensing AI Self Service board 1: Commercial Command Center*, step 2: Works in Customer Subscription & Commercial Portfolio → Provide a central portfolio of every TICVAI customer and their current commercial position.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (34 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-370?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-369`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-371` Customer Commercial 360°

**Provide the complete commercial, operational and subscription profile for one customer. This screen must clearly separate commercial charging from technical/operational classification.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/tenants-licensing/customer-commercial-360-adm-371` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Data it reads**: `getSubscription` (onLoad, Commercial 360); `getEntitlementUsage` (onLoad, What they consume)

**Where the user goes next**

- → `ADM-369` Commercial Command Center: *Back to Commercial Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer commercial 360° list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer commercial 360° untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer commercial 360° yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer commercial 360° are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Per-customer billing view shows minimum billable volume (month-to-date) and variable/overage revenue; a customer profile consolidates all commercial and licensing information per client. *(client request · MoM 10 Sep 2026, 4.17 Licensing Command Center Overview · DI-839)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-371` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-371`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 1
- Flow F207 *Subscription Licensing AI Self Service board 1: Commercial Command Center*, step 4: Works in Customer Commercial 360° → Provide the complete commercial, operational and subscription profile for one customer. This screen must clearly separate commercial charging from technical/operational classification.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-371?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-369`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-372` Operational Profile, VSI & Commercial Model Intelligence

**Analyze whether customers' operational profiles and commercial structures remain appropriate. This replaces the previous focus only on Tier Distribution & VSI.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/operational-profile-vsi-commercial-model-intelligence-adm-372` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Customers by VSI** (metric tile)

**Customers by Operational Profile** (metric tile)

**Customers by Commercial Model** (metric tile)

**Average VSI** (metric tile)

**Profile Misalignment** (metric tile)

**Commercial Model Optimization Candidates** (metric tile)

**Upgrade Candidates** (metric tile)

**Downgrade Candidates** (metric tile)

**Where the user goes next**

- → `ADM-369` Commercial Command Center: *Back to Commercial Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operational profile vsi list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operational profile vsi untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operational profile vsi yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the operational profile vsi are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.1 | AI Subscription Recommendations - System shall recommend optimal subscription plans. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |
| 20.8.2 | AI Module Recommendations - System shall recommend marketplace modules. | Subscription & Licensing Management | CONTRACTED | `scoreVsiAssessment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Further views: tier distribution (customers per tier), subscription revenue by tier, tier/conversion trends, and a renewal & retention centre flagging upcoming renewals, at-risk accounts and optimisation opportunities. *(client request · MoM 10 Sep 2026, 4.17 Licensing Command Center Overview · DI-840)*
- Tier thresholds map VSI ranges to tiers (0-30 Essential, 31-60 Professional, 61-80 Enterprise, 81-100 Enterprise Plus) with per-factor sub-thresholds (attendance 100-100,000 = 10 pts; 100,000-500,000 = 40); the system calculates the score and recommends the tier automatically. *(agreed · MoM 10 Sep 2026, 4.2 Venue Size Index (VSI) Model & Tier Threshold Configuration · DI-818)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-372` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-372`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 1
- Flow F207 *Subscription Licensing AI Self Service board 1: Commercial Command Center*, step 6: Works in Operational Profile, VSI & Commercial Model Intelligence → Analyze whether customers' operational profiles and commercial structures remain appropriate. This replaces the previous focus only on Tier Distribution & VSI.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-372?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-369`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-373` Revenue & Commercial Model Analytics

**Analyze TICVAI revenue across all commercial structures.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§KPIs) and a per-row directory (§Show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/revenue-commercial-model-analytics-adm-373` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**MRR / Monthly Equivalent** (metric tile)

**ARR / ACV** (metric tile)

**New Revenue** (metric tile)

**Expansion Revenue** (metric tile)

**Contraction Revenue** (metric tile)

**Churned Revenue** (metric tile)

**NRR** (metric tile)

**ARPC** (metric tile)

**Growth %** (metric tile)

**Every revenue commercial model** (data table)

| Shows | Format | Notes |
|---|---|---|
| Guaranteed revenue | text | not in the schema: `Guaranteed Revenue` |
| Actual variable revenue | text | not in the schema: `Actual Variable Revenue` |
| Guarantee shortfall protection | text | not in the schema: `Guarantee Shortfall Protection` |
| Contracts above guarantee | text | not in the schema: `Contracts Above Guarantee` |
| Contracts at guarantee | text | not in the schema: `Contracts at Guarantee` |

**The selected revenue commercial model** (detail panel): The pack groups this record's detail under its own headings: “Break down”, “Revenue by”.

| Shows | Format | Notes |
|---|---|---|
| Guaranteed revenue | text | not in the schema: `Guaranteed Revenue` |
| Actual variable revenue | text | not in the schema: `Actual Variable Revenue` |
| Guarantee shortfall protection | text | not in the schema: `Guarantee Shortfall Protection` |
| Contracts above guarantee | text | not in the schema: `Contracts Above Guarantee` |
| Contracts at guarantee | text | not in the schema: `Contracts at Guarantee` |

**Data it reads**: `getBillingReconciliation` (onLoad, Revenue against metering)

**Where the user goes next**

- → `ADM-369` Commercial Command Center: *Back to Commercial Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The revenue commercial model list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the revenue commercial model untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No revenue commercial model yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the revenue commercial model are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Further views: tier distribution (customers per tier), subscription revenue by tier, tier/conversion trends, and a renewal & retention centre flagging upcoming renewals, at-risk accounts and optimisation opportunities. *(client request · MoM 10 Sep 2026, 4.17 Licensing Command Center Overview · DI-840)*
- Licensing command centre: total customers, active subscriptions/tiers, MRR broken down by pricing model (tier-based, tier-plus-usage, per-ticket, per-transaction, hybrid, fixed, custom). *(client request · MoM 10 Sep 2026, 4.17 Licensing Command Center Overview · DI-838)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-373` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-373`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 1
- Flow F207 *Subscription Licensing AI Self Service board 1: Commercial Command Center*, step 8: Works in Revenue & Commercial Model Analytics → Analyze TICVAI revenue across all commercial structures.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-373?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-369`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-374` Trial & Conversion Monitor

**Monitor trial customers and their expected transition into paid commercial agreements.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/trial-conversion-monitor-adm-374` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Trials** (metric tile)

**New Trials** (metric tile)

**Expiring Trials** (metric tile)

**Trial-to-Paid %** (metric tile)

**Average Trial Duration** (metric tile)

**Setup Completion** (metric tile)

**Go-Live Readiness** (metric tile)

**Estimated Conversion Value** (metric tile)

**Data it reads**: `listTenants` (onLoad, Trials running)

**Where the user goes next**

- → `ADM-369` Commercial Command Center: *Back to Commercial Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The trial conversion list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the trial conversion untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No trial conversion yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the trial conversion are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Back-end configuration access can optionally be added to the demo for qualified prospects at TICVAI's discretion; demo credentials can be scoped and time-limited (auto-expire after an evaluation period). *(agreed · MoM 10 Sep 2026, 4.11 Demo Environment Scope · DI-832)*
- "Try it" is a single shared, pre-configured demo (sample products, working POS/admin sales flow, reporting) entered with shared credentials - evaluation only, cannot sell real tickets; not a per-prospect trial tenant. *(agreed · MoM 10 Sep 2026, 4.11 Demo Environment Scope · DI-831)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-374` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-374`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 1
- Flow F207 *Subscription Licensing AI Self Service board 1: Commercial Command Center*, step 10: Works in Trial & Conversion Monitor → Monitor trial customers and their expected transition into paid commercial agreements.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-374?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-369`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-375` Renewal & Retention Center

**Manage upcoming renewals and identify retention or commercial restructuring requirements.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§KPIs) and a per-row directory (§Columns) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/renewal-retention-center-adm-375` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Renewals Next 30 Days** (metric tile)

**Next 60 Days** (metric tile)

**Next 90 Days** (metric tile)

**Renewal Value** (metric tile)

**Renewal Rate** (metric tile)

**At-Risk Revenue** (metric tile)

**Auto-Renew Value** (metric tile)

**Expansion Opportunity** (metric tile)

**Optimization Opportunity** (metric tile)

**Every renewal retention** (data table)

| Shows | Format | Notes |
|---|---|---|
| Customer | text | not in the schema: `Customer` |
| Commercial model | text | not in the schema: `Commercial Model` |
| Current rate | text | not in the schema: `Current Rate` |
| Minimum guarantee | text | not in the schema: `Minimum Guarantee` |
| Monthly equivalent | text | not in the schema: `Monthly Equivalent` |
| Contract value | text | not in the schema: `Contract Value` |
| Renewal date | text | not in the schema: `Renewal Date` |
| Usage trend | text | not in the schema: `Usage Trend` |
| Payment health | text | not in the schema: `Payment Health` |
| Risk | text | not in the schema: `Risk` |
| AI recommendation | text | not in the schema: `AI Recommendation` |

**The selected renewal retention** (detail panel): The pack groups this record's detail under its own headings: “Retention Signals”.

| Shows | Format | Notes |
|---|---|---|
| Customer | text | not in the schema: `Customer` |
| Commercial model | text | not in the schema: `Commercial Model` |
| Current rate | text | not in the schema: `Current Rate` |
| Minimum guarantee | text | not in the schema: `Minimum Guarantee` |
| Monthly equivalent | text | not in the schema: `Monthly Equivalent` |
| Contract value | text | not in the schema: `Contract Value` |
| Renewal date | text | not in the schema: `Renewal Date` |
| Usage trend | text | not in the schema: `Usage Trend` |
| Payment health | text | not in the schema: `Payment Health` |
| Risk | text | not in the schema: `Risk` |
| AI recommendation | text | not in the schema: `AI Recommendation` |

**Data it reads**: `listMembershipRenewalRetention` (onLoad, Membership Analytics, Renewal Intelligence & AI Retention …)

**Where the user goes next**

- → `ADM-369` Commercial Command Center: *Back to Commercial Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The renewal retention list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the renewal retention untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No renewal retention yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the renewal retention are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Further views: tier distribution (customers per tier), subscription revenue by tier, tier/conversion trends, and a renewal & retention centre flagging upcoming renewals, at-risk accounts and optimisation opportunities. *(client request · MoM 10 Sep 2026, 4.17 Licensing Command Center Overview · DI-840)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-375` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-375`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 1
- Flow F207 *Subscription Licensing AI Self Service board 1: Commercial Command Center*, step 12: Works in Renewal & Retention Center → Manage upcoming renewals and identify retention or commercial restructuring requirements.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-375?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-369`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-376` Commercial Optimization & Expansion Opportunities

**Identify opportunities beyond traditional tier upgrades. This is a key revision from the original Upgrade, Downgrade & Expansion Opportunities screen.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Opportunity KPIs) and a per-row directory (§Show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/commercial-optimization-expansion-opportunities-adm-376` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Total Opportunities** (metric tile)

**Potential Expansion Revenue** (metric tile)

**Potential Retention Value** (metric tile)

**Model Optimization Opportunities** (metric tile)

**Module Opportunities** (metric tile)

**Cost Optimization Opportunities** (metric tile)

**Every commercial optimization expansion** (data table)

| Shows | Format | Notes |
|---|---|---|
| Current customer cost | text | not in the schema: `Current Customer Cost` |
| Proposed customer cost | text | not in the schema: `Proposed Customer Cost` |
| TICVAI revenue impact | text | not in the schema: `TICVAI Revenue Impact` |
| Minimum revenue protection | text | not in the schema: `Minimum Revenue Protection` |
| Customer saving/increase | text | not in the schema: `Customer Saving/Increase` |
| Confidence | text | not in the schema: `Confidence` |

**The selected commercial optimization expansion** (detail panel): The pack groups this record's detail under its own headings: “Opportunity Types”, “Current”, “Projected Volume”.

| Shows | Format | Notes |
|---|---|---|
| Current customer cost | text | not in the schema: `Current Customer Cost` |
| Proposed customer cost | text | not in the schema: `Proposed Customer Cost` |
| TICVAI revenue impact | text | not in the schema: `TICVAI Revenue Impact` |
| Minimum revenue protection | text | not in the schema: `Minimum Revenue Protection` |
| Customer saving/increase | text | not in the schema: `Customer Saving/Increase` |
| Confidence | text | not in the schema: `Confidence` |

**Data it reads**: `listRenewalAuto` (onLoad, Renewals due)

**Where the user goes next**

- → `ADM-369` Commercial Command Center: *Back to Commercial Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial optimization expansion list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial optimization expansion untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial optimization expansion yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial optimization expansion are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Further views: tier distribution (customers per tier), subscription revenue by tier, tier/conversion trends, and a renewal & retention centre flagging upcoming renewals, at-risk accounts and optimisation opportunities. *(client request · MoM 10 Sep 2026, 4.17 Licensing Command Center Overview · DI-840)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-376` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-376`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 1
- Flow F207 *Subscription Licensing AI Self Service board 1: Commercial Command Center*, step 14: Works in Commercial Optimization & Expansion Opportunities → Identify opportunities beyond traditional tier upgrades. This is a key revision from the original Upgrade, Downgrade & Expansion Opportunities screen.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-376?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-369`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-377` Subscription Exceptions & Commercial Alerts

**Provide management with one consolidated view of subscription, licensing, commercial, billing and metering exceptions.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/subscription-exceptions-commercial-alerts-adm-377` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-369` Commercial Command Center: *Back to Commercial Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The subscription exceptions commercial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the subscription exceptions commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No subscription exceptions commercial yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the subscription exceptions commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-377` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-377`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 1
- Flow F207 *Subscription Licensing AI Self Service board 1: Commercial Command Center*, step 16: Works in Subscription Exceptions & Commercial Alerts → Provide management with one consolidated view of subscription, licensing, commercial, billing and metering exceptions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-377?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-369`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-378` Executive AI Commercial Intelligence

**Provide TICVAI leadership with an AI-powered executive commercial intelligence layer. Allow a new customer to register, describe their venue/business, and let TICVAI intelligently determine their operational requirements before calculating the VSI, recommending a subscription tier, and suggesting modules.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Customer Metrics; Revenue Metrics; Variable Commercial Metrics) and no per-row directory — measures over a population the screen does not itself list. … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/executive-ai-commercial-intelligence-adm-378` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Board 1 — Standardized Commercial Metrics. Each needs an operation, or needs removing from the screen; this …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Customers** (metric tile)

**New Customers** (metric tile)

**Churned Customers** (metric tile)

**Trials** (metric tile)

**Conversion** (metric tile)

**MRR / Monthly Equivalent Revenue** (metric tile)

**ARR / ACV** (metric tile)

**New Revenue** (metric tile)

**Expansion** (metric tile)

**Contraction** (metric tile)

**Churn** (metric tile)

**NRR** (metric tile)

**ARPC** (metric tile)

**Billable Tickets** (metric tile)

**Billable Transactions** (metric tile)

**Eligible Transaction Value** (metric tile)

**Variable Revenue** (metric tile)

**Minimum Guaranteed Revenue** (metric tile)

**Guarantee Utilization** (metric tile)

**Revenue Above Guarantee** (metric tile)

**VSI** (metric tile)

**Operational Profile** (metric tile)

**POS Utilization** (metric tile)

**Access Utilization** (metric tile)

**User Utilization** (metric tile)

**API** (metric tile)

**Storage** (metric tile)

**Admissions** (metric tile)

**Renewal Risk** (metric tile)

**Expansion Probability** (metric tile)

**Model Optimization Opportunity** (metric tile)

**Cost Optimization** (metric tile)

**Upgrade/Downgrade Probability** (metric tile)

**Commercial Health** (metric tile)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Board 1 — Standardized Commercial Metrics (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `getLicenceEnforcement` (onLoad, Exceptions and overage); `getPlanRecommendations` (onLoad, Commercial recommendations beside the enforcement position)

**Where the user goes next**

- → `ADM-369` Commercial Command Center: *Back to Commercial Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The executive commercial intelligence list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the executive commercial intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No executive commercial intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the executive commercial intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.8.3 | AI Usage Forecasting - System shall forecast future platform consumption. | Subscription & Licensing Management | CONTRACTED | `getLicenceEnforcement` |
| 20.8.4 | AI Upgrade Recommendations - System shall recommend subscription upgrades. | Subscription & Licensing Management | CONTRACTED | `getPlanRecommendations` |
| 20.8.5 | AI Cost Optimization - System shall recommend cost optimization opportunities. | Subscription & Licensing Management | CONTRACTED | `getPlanRecommendations` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-378` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-378`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 1
- Flow F207 *Subscription Licensing AI Self Service board 1: Commercial Command Center*, step 18: Works in Executive AI Commercial Intelligence → Provide TICVAI leadership with an AI-powered executive commercial intelligence layer.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-378?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Board 1 — Standardized Commercial ….
- [ ] Every transition is wired: `ADM-369`.
- [ ] Sign-in is asked only where the spec asks for it.
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

**10 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{

}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{

}
```
