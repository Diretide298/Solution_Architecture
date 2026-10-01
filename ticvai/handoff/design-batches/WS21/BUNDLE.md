# WS21 — B2B, Reseller & OTA Partner Management board 1

**10 screens · 0 operations · 0 schemas · 0 permissions**

Platform P10 Partner Web · ships as **ticvai-control** ·
partner audience · web ·
online only

## Who this is for

**partner on web.** Everything below is how you know what is
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
| `PTR-022` | Partner Management Command Center | B–D | 2 | 30 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `PTR-023` | Partner Profile & Organization Setup | B–D | 16 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `PTR-024` | Partner Onboarding & Application Workflow | B–D | 10 | 0 | 5 | 0 | 3 | 0 | — | notStarted (generated) |
| `PTR-025` | Partner Contacts & User Administration | B–D | 17 | 0 | 5 | 5 | 1 | 0 | — | notStarted (generated) |
| `PTR-026` | Territory, Market & Distribution Rights | B–D | 4 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `PTR-027` | Partner Brand, Venue & Business Scope Assignment | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `PTR-028` | Partner Documentation & Compliance Repository | B–D | 15 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `PTR-029` | Partner Access, Roles & Permission Profile | B–D | 18 | 0 | 5 | 0 | 0 | 5 | — | notStarted (generated) |
| `PTR-030` | Partner Approval, Status & Lifecycle Management | B–D | 8 | 0 | 5 | 0 | 2 | 3 | — | notStarted (generated) |
| `PTR-031` | Partner 360° Profile, Readiness & AI Review | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**PTR-027, PTR-031 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `PTR-022` Partner Management Command Center

**Provide a centralized management dashboard for all B2B, reseller, OTA and distribution partners across the TICVAI ecosystem.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as platform admin |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each partner record should display) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-management-command-center-ptr-022` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search partner | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by partner type, country, territory, brand, venue, account manager and 5 more — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Shown**

**Total Partners** (metric tile)

**Active Partners** (metric tile)

**Pending Onboarding** (metric tile)

**Pending Approval** (metric tile)

**Suspended Partners** (metric tile)

**Expiring Agreements** (metric tile)

**Documentation Issues** (metric tile)

**Partners With Credit Holds** (metric tile)

**Connected OTA/API Partners** (metric tile)

**Partner Sales YTD** (metric tile)

**Partner Revenue YTD** (metric tile)

**High-Risk Partners** (metric tile)

**Every partner** (data table, from `listPartner`)

| Shows | Format | Notes |
|---|---|---|
| Partner ID | text | not in the schema: `PartnerManagementCommandCenterView.partnerId` |
| Trading name | text | not in the schema: `PartnerManagementCommandCenterView.tradingName` |
| Legal entity | text | not in the schema: `PartnerManagementCommandCenterView.legalEntity` |
| Partner type | text | not in the schema: `PartnerManagementCommandCenterView.partnerType` |
| Country | text | not in the schema: `PartnerManagementCommandCenterView.country` |
| Territory | text | not in the schema: `PartnerManagementCommandCenterView.territory` |
| Assigned brand/venue | text | not in the schema: `Assigned Brand/Venue` |
| Commercial owner | text | not in the schema: `PartnerManagementCommandCenterView.commercialOwner` |
| Distribution channel | text | not in the schema: `PartnerManagementCommandCenterView.distributionChannel` |
| Account status | text | not in the schema: `PartnerManagementCommandCenterView.accountStatus` |
| Onboarding status | text | not in the schema: `PartnerManagementCommandCenterView.onboardingStatus` |
| Agreement status | text | not in the schema: `PartnerManagementCommandCenterView.agreementStatus` |
| Credit status | text | not in the schema: `PartnerManagementCommandCenterView.creditStatus` |
| Integration status | text | not in the schema: `PartnerManagementCommandCenterView.integrationStatus` |
| Last activity | text | not in the schema: `PartnerManagementCommandCenterView.lastActivity` |

**The selected partner** (detail panel): The pack groups this record's detail under its own headings: “Partner Attention Required”.

| Shows | Format | Notes |
|---|---|---|
| Partner ID | text | not in the schema: `PartnerManagementCommandCenterView.partnerId` |
| Trading name | text | not in the schema: `PartnerManagementCommandCenterView.tradingName` |
| Legal entity | text | not in the schema: `PartnerManagementCommandCenterView.legalEntity` |
| Partner type | text | not in the schema: `PartnerManagementCommandCenterView.partnerType` |
| Country | text | not in the schema: `PartnerManagementCommandCenterView.country` |
| Territory | text | not in the schema: `PartnerManagementCommandCenterView.territory` |
| Assigned brand/venue | text | not in the schema: `Assigned Brand/Venue` |
| Commercial owner | text | not in the schema: `PartnerManagementCommandCenterView.commercialOwner` |
| Distribution channel | text | not in the schema: `PartnerManagementCommandCenterView.distributionChannel` |
| Account status | text | not in the schema: `PartnerManagementCommandCenterView.accountStatus` |
| Onboarding status | text | not in the schema: `PartnerManagementCommandCenterView.onboardingStatus` |
| Agreement status | text | not in the schema: `PartnerManagementCommandCenterView.agreementStatus` |
| Credit status | text | not in the schema: `PartnerManagementCommandCenterView.creditStatus` |
| Integration status | text | not in the schema: `PartnerManagementCommandCenterView.integrationStatus` |
| Last activity | text | not in the schema: `PartnerManagementCommandCenterView.lastActivity` |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Create Partner, Review Application, Approve, Assign Account Manager, Suspend, Open Commercial Profile, View Users, View Documents, View Performance. Each needs attaching to the control it gates, or the screen needs the control.

**Data it reads**: `listPartner2` (onLoad, Partner Operations Command Center); `listPartner` (onLoad, Partner Management Command Center)

**Where the user goes next**

- → `PTR-023` Partner Profile & Organization Setup: *Sets up the organisation record*; calls `listPartner`
- → `PTR-024` Partner Onboarding & Application Workflow: *Reads the application the applicant submitted*; calls `listPartner`
- → `PTR-025` Partner Contacts & User Administration: *Creates the partner's first user*; calls `listPartner`
- → `PTR-027` Partner Brand, Venue & Business Scope Assignment: *Assigns the brands, venues and business scope the partner may sell*; calls `listPartner`
- → `PTR-028` Partner Documentation & Compliance Repository: *Checks the compliance and documentation file*; calls `listPartner`
- → `PTR-029` Partner Access, Roles & Permission Profile: *Chooses the permission profile the partner's own users will inherit*; calls `listPartner`
- → `PTR-030` Partner Approval, Status & Lifecycle Management: *Approves the partner and moves it to active*; calls `listPartner`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner are still there. The pack's own statuses are Suspended → Terminated → Archived — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Partner overview lists all B2B partners with status, pending approvals and documentation state. Partner profile captures company info and a configurable partner category/type; profile fields are fully customisable. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-547)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-022` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-022`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 1
- Flow F110 *A partner is onboarded onto the B2B portal*, step 2: Opens the partner command centre → Every partner and every pending application in one place
- Flow F110 *A partner is onboarded onto the B2B portal*, step 4: Returns to the command centre → Application read, nothing yet granted
- Flow F110 *A partner is onboarded onto the B2B portal*, step 6: Returns to the command centre → Organisation known, scope still unbounded
- Flow F110 *A partner is onboarded onto the B2B portal*, step 8: Returns to the command centre → Scope set, compliance unverified
- Flow F110 *A partner is onboarded onto the B2B portal*, step 10: Returns to the command centre → Compliance checked
- Flow F110 *A partner is onboarded onto the B2B portal*, step 12: Returns to the command centre → Profile chosen, nobody holding it
- Flow F110 *A partner is onboarded onto the B2B portal*, step 14: Returns to the command centre → Everything configured, nothing yet live

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-022?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `PTR-023`, `PTR-024`, `PTR-025`, `PTR-027`, `PTR-028`, `PTR-029`, `PTR-030`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-023` Partner Profile & Organization Setup

**Create the master business record for each external distribution partner.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as platform admin |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-profile-organization-setup-ptr-023` |

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Key Account, New Partner. Each needs an operation, or needs removing from the screen; this is the Phase 3 …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Partner ID | select field | — | — | — | — | — | — |
| Legal Entity Name | select field | — | — | — | — | — | — |
| Trading Name | select field | — | — | — | — | — | — |
| Partner Type | select field | — | — | — | — | — | — |
| Registration Number | select field | — | — | — | — | — | — |
| Tax/VAT Number | select field | — | — | — | — | — | — |
| Country | select field | — | — | — | — | — | — |
| City | select field | — | — | — | — | — | — |
| Registered Address | select field | — | — | — | — | — | — |
| Business Address | select field | — | — | — | — | — | — |
| Website | select field | — | — | — | — | — | — |
| Main Telephone | select field | — | — | — | — | — | — |
| General Email | select field | — | — | — | — | — | — |
| Preferred Language | select field | — | — | — | — | — | — |
| Default Currency | select field | — | — | — | — | — | — |
| Time Zone | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Key Account (primary button) | navigation or local | — | — | — | — |
| New Partner (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `PTR-022` Partner Management Command Center: *Returns to the command centre*; calls `setPartnerProfileOrganization`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner profile organization configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner profile organization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner profile organization configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Partner overview lists all B2B partners with status, pending approvals and documentation state. Partner profile captures company info and a configurable partner category/type; profile fields are fully customisable. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-547)*
- B2B account financial tab shows credit limit, credit days and a linked account-specific price list; accounts can be a main account with child (agent) accounts; every account shows its full sales/transaction history, as does a B2C customer profile. *(client request · MoM 7 Aug 2026, 11. Accounts Management (B2B and B2C) · DI-162)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-023` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-023`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 1
- Flow F110 *A partner is onboarded onto the B2B portal*, step 5: Sets up the organisation record → Legal entity, trading name, tax identity and billing address

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-023?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Key Account, New Partner.
- [ ] Every transition is wired: `PTR-022`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-024` Partner Onboarding & Application Workflow

**Manage the complete journey from a new partner application through internal review and activation.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as platform admin |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `applicationId` (navigation) |
| Route | `/partners/partner-onboarding-application-workflow-ptr-024` |

**Known gaps.** **The pack names 5 actions on this screen; 1 are served since the writers pass (29 September): Request More Information by `actOnPartnerApplicationReview`.** Still unserved: Product requirements …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Company information | select field | — | — | — | — | — | — |
| Requested partner type | select field | — | — | — | — | — | — |
| Markets | select field | — | — | — | — | — | — |
| Expected sales volume | select field | — | — | — | — | — | — |
| Requested products | select field | — | — | — | — | — | — |
| Requested venues | select field | — | — | — | — | — | — |
| Preferred distribution method | select field | — | — | — | — | — | — |
| Estimated annual business | select field | — | — | — | — | — | — |
| Contact information | select field | — | — | — | — | — | — |
| Billing requirements | select field | — | — | — | — | — | — |

**Form: Act on partner application review** (modal, opened by *Act on partner application review*; *Act on partner application review* calls `actOnPartnerApplicationReview`, *Cancel* sends nothing)

**Collects what `actOnPartnerApplicationReview` sends before it is called.** Required: `action`. Optional: `department`, `assigneePrincipalId`, `note`, `documentIds`. Dismissing sends nothing; the screen behind is unchanged.

`actOnPartnerApplicationReview` is not in any contract: draw the form greyed and list it in FINDINGS.md.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Product requirements (primary button) | navigation or local | — | — | — | — |
| Sequential approval (secondary button) | navigation or local | — | — | — | — |
| Parallel approval (secondary button) | navigation or local | — | — | — | — |
| Rejection (secondary button) | navigation or local | — | — | — | — |
| Request More Information (secondary button) | navigation or local | — | — | — | — |
| Act on partner application review (secondary button) | `actOnPartnerApplicationReview` (not in any contract) | — | — | — | — |

**Data it reads**: `listPartnerOnboardingApplication` (onLoad, Partner Onboarding & Application Workflow)

**Where the user goes next**

- → `PTR-022` Partner Management Command Center: *Returns to the command centre*; calls `listPartnerOnboardingApplication`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner onboarding application configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner onboarding application untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner onboarding application configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Partner onboarding: partner signs up via a registration link/form on the B2B platform, then review and approval, with confirmation emails and back-office visibility of required next steps. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-548)*
- Partner review: operations validate documents and can reject (e.g. expired trade licence) with a message prompting resubmission; approval emails credentials with a temporary password, and the partner must set their own password at first login. *(client request · MoM 7 Aug 2026, 13. Tenant/B2B Onboarding & Self-Registration Flow · DI-166)*
- "Become a partner" link on the tenant website opens a registration form capturing company type, name, address, Emirate/state and documents (trade licence, VAT/TRN certificate); submitting creates a pending account and emails the tenant's operations team. *(client request · MoM 7 Aug 2026, 13. Tenant/B2B Onboarding & Self-Registration Flow · DI-165)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-024` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-024`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 1
- Flow F110 *A partner is onboarded onto the B2B portal*, step 3: Reads the application the applicant submitted → The application, its documents and its declared trading intent
- Flow F110 branch at step 3 (abandonsFlow): when The applicant could not submit an application at all, `submitOnboardingApplication` is `public` and requires `TENANT_CONFIGURE`. Until that is reconciled the only working front door is `registerPartner`, and any journey that depends on the application …

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-024?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Product requirements, Sequential approval, Parallel approval, Rejection, Request More Information, Act on partner application review.
- [ ] Every transition is wired: `PTR-022`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-025` Partner Contacts & User Administration

**Manage the individuals authorized to interact with TICVAI on behalf of each partner.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as platform admin |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `partnerId` (session) |
| Route | `/partners/partner-contacts-user-administration-ptr-025` |

**Known gaps.** **The pack names 9 actions on this screen; 6 are served since the writers pass (29 September): Primary Contact, Commercial, Finance, Operations, Management, Emergency Contact by …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Name | select field | — | — | — | — | — | — |
| Position | select field | — | — | — | — | — | — |
| Department | select field | — | — | — | — | — | — |
| Email | select field | — | — | — | — | — | — |
| Mobile | select field | — | — | — | — | — | — |
| Telephone | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Time Zone | select field | — | — | — | — | — | — |
| Contact Type | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |
| Username | select field | — | — | — | — | — | — |
| Partner | select field | — | — | — | — | — | — |
| Branch | select field | — | — | — | — | — | — |
| Role | select field | — | — | — | — | — | — |
| Permissions | select field | — | — | — | — | — | — |
| Sales Location | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |

**Form: Save partner contact** (modal, opened by *Save partner contact*; *Save partner contact* calls `setPartnerContact`, *Cancel* sends nothing)

**Collects what `setPartnerContact` sends before it is called.** Required: `partnerId`. Optional: `contactId`, `action`, `name`, `position`, `department`, `email`, `mobile`, `telephone`, `language`, `timeZone`, `contactType`. Dismissing sends nothing; the screen behind is unchanged.

`setPartnerContact` is not in any contract: draw the form greyed and list it in FINDINGS.md.

**Form: Create partner user** (modal, opened by *Create partner user*; *Create partner user* calls `createPartnerUser`, *Cancel* sends nothing)

**Collects what `createPartnerUser` sends before it is called.** Required: `id`, `partnerId`, `principalId`, `branchScopePath`. Optional: `role`, `salesLocation`, `currency`, `accountExpiresAt`, `allocationQuota`, `creditLimitOverride`, `canManageUsers`. Dismissing sends nothing; the screen behind is unchanged.

`createPartnerUser` is not in any contract: draw the form greyed and list it in FINDINGS.md.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Primary Contact (primary button) | navigation or local | — | — | — | — |
| Commercial (secondary button) | navigation or local | — | — | — | — |
| Finance (secondary button) | navigation or local | — | — | — | — |
| Operations (secondary button) | navigation or local | — | — | — | — |
| Management (secondary button) | navigation or local | — | — | — | — |
| Emergency Contact (secondary button) | navigation or local | — | — | — | — |
| Password policy (secondary button) | navigation or local | — | — | — | — |
| SSO where available (secondary button) | navigation or local | — | — | — | — |
| Save partner contact (secondary button) | `setPartnerContact` (not in any contract) | — | — | — | — |
| Create partner user (secondary button) | `createPartnerUser` (not in any contract) | — | — | — | — |

**Data it reads**: `listPartnerContactUser` (onLoad, Partner Contacts & User Administration)

**Where the user goes next**

- → `PTR-022` Partner Management Command Center: *Returns to the command centre*; calls `listPartnerContactUser`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner contacts user configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner contacts user untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner contacts user configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.7.7 | Master accounts must be able to create sub-users with limited permissions to avoid sharing login credentials and security risks. | Ticketing Sales | CONTRACTED | data `PartnerUser` |
| 2.7.18 | Each BtoB Customer can ask for an account. It is expected to have the possibility to create a login and password for the BtoB Customers. | Ticketing Sales | CONTRACTED | data `PartnerUser` |
| 2.7.34 | The system should support, at minimum, the following security controls for the B2B portal: - Password protected access to the B2B portal. B2B set-up of own users/passwords. - Forgot password … | Ticketing Sales | CONTRACTED | data `PartnerUser` |
| 2.7.51 | System shall support hierarchical B2B account structures such as Master Agency, Branch, Department, and User. Permissions, quotas, credit limits, pricing, and reporting access shall be configurable … | Ticketing Sales | CONTRACTED | data `PartnerUser` |
| 3.5.7 | Support tiered B2B2C or B2B2B2C approach, White-label B2B portal with master / sub-agent user hierarchy and role controls | Admission and Access | CONTRACTED | data `PartnerUser` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A partner has multiple agents/sub-agents who can each sell on its behalf; territory/market rights set the regions it may sell into; brand/venue association sets which venues and products it can sell, with distinct pricing per venue. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-549)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-025` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-025`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 1
- Flow F110 *A partner is onboarded onto the B2B portal*, step 13: Creates the partner's first user → One identity inside the partner organisation

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-025?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Primary Contact, Commercial, Finance, Operations, Management, Emergency Contact, Password policy, SSO where available, Save partner contact, Create partner user.
- [ ] Every transition is wired: `PTR-022`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-026` Territory, Market & Distribution Rights

**Define where and through what business scope a partner is authorized to distribute TICVAI products.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `partnerId` (session) |
| Route | `/partners/territory-market-distribution-rights-ptr-026` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Sub-agents allowed | select field | — | — | — | — | — | — |
| Sub-agents prohibited | select field | — | — | — | — | — | — |
| Approval required | select field | — | — | — | — | — | — |
| Maximum hierarchy depth | select field | — | — | — | — | — | — |

**Form: Save partner distribution rights** (modal, opened by *Save partner distribution rights*; *Save partner distribution rights* calls `setPartnerDistributionRights`, *Cancel* sends nothing)

**Collects what `setPartnerDistributionRights` sends before it is called.** Required: `rights`. Dismissing sends nothing; the screen behind is unchanged.

`setPartnerDistributionRights` is not in any contract: draw the form greyed and list it in FINDINGS.md.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save partner distribution rights (primary button) | `setPartnerDistributionRights` (not in any contract) | — | — | — | — |

**Data it reads**: `listTerritoryMarketDistribution` (onLoad, Territory, Market & Distribution Rights)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The territory market distribution configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the territory market distribution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No territory market distribution configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A partner has multiple agents/sub-agents who can each sell on its behalf; territory/market rights set the regions it may sell into; brand/venue association sets which venues and products it can sell, with distinct pricing per venue. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-549)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-026` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-026`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 1

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-026?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save partner distribution rights.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-027` Partner Brand, Venue & Business Scope Assignment

**Determine which TICVAI business entities the partner relationship covers. This is deliberately separate from product assignment, which is governed through the Sales Channel and commercial configuration layers.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as platform admin |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-brand-venue-business-scope-assignment-ptr-027` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `PTR-022` Partner Management Command Center: *Returns to the command centre*; calls `setPartnerBrandVenue`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner brand venue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner brand venue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner brand venue yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner brand venue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A partner has multiple agents/sub-agents who can each sell on its behalf; territory/market rights set the regions it may sell into; brand/venue association sets which venues and products it can sell, with distinct pricing per venue. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-549)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-027` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-027`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 1
- Flow F110 *A partner is onboarded onto the B2B portal*, step 7: Assigns the brands, venues and business scope the partner may sell → **The commercial boundary**, and the one that becomes `Session.scope` for every user the partner later creates

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-027?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `PTR-022`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-028` Partner Documentation & Compliance Repository

**Maintain required partner documentation and ensure that commercial accounts remain compliant.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as platform admin |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture; Configure whether expiration should) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-documentation-compliance-repository-ptr-028` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Commercial Registration, Bank Details, Signed Agreement, API Agreement. Each needs an operation, or needs …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Document Type | select field | — | — | — | — | — | — |
| Document Number | select field | — | — | — | — | — | — |
| Issue Date | select field | — | — | — | — | — | — |
| Expiry Date | select field | — | — | — | — | — | — |
| Issuing Authority | select field | — | — | — | — | — | — |
| File | select field | — | — | — | — | — | — |
| Verification Status | select field | — | — | — | — | — | — |
| Verified By | select field | — | — | — | — | — | — |
| Verification Date | select field | — | — | — | — | — | — |
| Notes | select field | — | — | — | — | — | — |
| Warn only | select field | — | — | — | — | — | — |
| Block new bookings | select field | — | — | — | — | — | — |
| Block credit transactions | select field | — | — | — | — | — | — |
| Suspend partner | select field | — | — | — | — | — | — |
| Require manual review | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Commercial Registration (primary button) | navigation or local | — | — | — | — |
| Bank Details (secondary button) | navigation or local | — | — | — | — |
| Signed Agreement (secondary button) | navigation or local | — | — | — | — |
| API Agreement (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listPartnerDocumentationCompliance` (onLoad, Partner Documentation & Compliance Repository)

**Where the user goes next**

- → `PTR-022` Partner Management Command Center: *Returns to the command centre*; calls `listPartnerDocumentationCompliance`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner documentation compliance configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner documentation compliance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner documentation compliance configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Partner documents (e.g. trade licence, VAT certificate) follow a review/accept/reject/resubmit flow; approval status runs lead > submitted > active > suspended; a partner 360 view consolidates profile, agreement and payment information in one view. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-550)*
- "Become a partner" link on the tenant website opens a registration form capturing company type, name, address, Emirate/state and documents (trade licence, VAT/TRN certificate); submitting creates a pending account and emails the tenant's operations team. *(client request · MoM 7 Aug 2026, 13. Tenant/B2B Onboarding & Self-Registration Flow · DI-165)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-028` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-028`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 1
- Flow F110 *A partner is onboarded onto the B2B portal*, step 9: Checks the compliance and documentation file → Licences, insurance and signed agreement present or missing
- Flow F110 branch at step 9 (recoverable): when Compliance documents are missing or expired, **Onboarding pauses rather than fails.** Scope and profile stay configured and the partner sits unapproved, which is why step 15 is separated from step 11 — a partly-onboarded partner must be a …

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-028?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Commercial Registration, Bank Details, Signed Agreement, API Agreement.
- [ ] Every transition is wired: `PTR-022`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-029` Partner Access, Roles & Permission Profile

**Control what a partner organization is permitted to do, beyond individual-user permissions.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as platform admin |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure whether the partner may) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `partnerId` (session) |
| Route | `/partners/partner-access-roles-permission-profile-ptr-029` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search Availability | select field | — | — | — | — | — | — |
| Create Booking | select field | — | — | — | — | — | — |
| Hold Inventory | select field | — | — | — | — | — | — |
| Confirm Booking | select field | — | — | — | — | — | — |
| Cancel Booking | select field | — | — | — | — | — | — |
| Modify Booking | select field | — | — | — | — | — | — |
| Download Ticket | select field | — | — | — | — | — | — |
| Print Ticket | select field | — | — | — | — | — | — |
| Send Ticket | select field | — | — | — | — | — | — |
| Access Customer Details | select field | — | — | — | — | — | — |
| Use Credit | select field | — | — | — | — | — | — |
| Use Payment Card | select field | — | — | — | — | — | — |
| View Commission | select field | — | — | — | — | — | — |
| View Net Rates | select field | — | — | — | — | — | — |
| Access Reports | select field | — | — | — | — | — | — |
| Export Data | select field | — | — | — | — | — | — |
| Use API | select field | — | — | — | — | — | — |
| Create Sub-Agents | select field | — | — | — | — | — | — |

**Form: Save partner capability grants** (modal, opened by *Save partner capability grants*; *Save partner capability grants* calls `setPartnerCapabilityGrants`, *Cancel* sends nothing)

**Collects what `setPartnerCapabilityGrants` sends before it is called.** Required: `grants`. Dismissing sends nothing; the screen behind is unchanged.

`setPartnerCapabilityGrants` is not in any contract: draw the form greyed and list it in FINDINGS.md.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** ↓, Permanent, Temporary, Seasonal, Event-specific. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save partner capability grants (primary button) | `setPartnerCapabilityGrants` (not in any contract) | — | — | — | — |

**Data it reads**: `listPartnerAccessRole` (onLoad, Partner Access, Roles & Permission Profile)

**Where the user goes next**

- → `PTR-022` Partner Management Command Center: *Returns to the command centre*; calls `listPartnerAccessRole`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner access roles configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner access roles untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner access roles configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S2** Role-based access control: role and permission matrix *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'permission matrix')*
- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'rbac')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A97** Document the RBAC role-permission matrix (edit/view · view-only · hidden, per role per module, sub-permissions, default templates) *(Chinmay Parab · High · Ongoing → 30 Sep: Closed, Rolled into S2 · 20 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A130** Enforce venue-level admission capacity as superseding event capacity, with a blocking validation and an RBAC-gated override *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 25 Aug 2026 · workshop tracker · keyword 'rbac')*

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-029` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-029`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 1
- Flow F110 *A partner is onboarded onto the B2B portal*, step 11: Chooses the permission profile the partner's own users will inherit → What a partner user may do, bounded by the scope set at step 7
- Flow F110 branch at step 11 (requiresStaff): when No permission profile exists to choose, PTR-029 shows `emptyFirstRun`. The first partner onboarded on a tenant has no profile to inherit and one must be authored, which is a different and slower job than picking one.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-029?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save partner capability grants.
- [ ] Every transition is wired: `PTR-022`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-030` Partner Approval, Status & Lifecycle Management

**Govern the complete business lifecycle of a partner after onboarding.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner; in the flows as platform admin |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-approval-status-lifecycle-management-ptr-030` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Commercial | select field | — | — | — | — | — | — |
| Compliance | select field | — | — | — | — | — | — |
| Credit | select field | — | — | — | — | — | — |
| Fraud | select field | — | — | — | — | — | — |
| Contract Expiry | select field | — | — | — | — | — | — |
| Performance | select field | — | — | — | — | — | — |
| Technical | select field | — | — | — | — | — | — |
| Management Decision | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Activate, Restrict, Suspend, Reactivate, Terminate, Archive. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve (primary button) | navigation or local | — | — | — | — |

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner approval status configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner approval status untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner approval status configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Partner documents (e.g. trade licence, VAT certificate) follow a review/accept/reject/resubmit flow; approval status runs lead > submitted > active > suspended; a partner 360 view consolidates profile, agreement and payment information in one view. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-550)*
- Partner review: operations validate documents and can reject (e.g. expired trade licence) with a message prompting resubmission; approval emails credentials with a temporary password, and the partner must set their own password at first login. *(client request · MoM 7 Aug 2026, 13. Tenant/B2B Onboarding & Self-Registration Flow · DI-166)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-030` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-030`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 1
- Flow F110 *A partner is onboarded onto the B2B portal*, step 15: Approves the partner and moves it to active → **The partner can trade.** Approval is last on purpose: scope, compliance and permissions are all in place before the account can raise an order
- Flow F110 branch at step 15 (requiresStaff): when The partner is approved before scope or compliance is set, Nothing in the screens enforces the order of steps 5 to 13 — they are all spokes off one hub and reachable in any sequence. **An approved partner with unbounded scope can sell inventory it was never …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-030?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-031` Partner 360° Profile, Readiness & AI Review

**Provide one consolidated Partner 360 screen before activation and throughout the relationship. This should become one of the most useful screens for TICVAI commercial management. Board 1 established who the partner is and what they are authorized to access. Board 2 establishes the commercial rules under which that partner can transact with TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Partners · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/partners/partner-360-profile-readiness-ai-review-ptr-031` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listPartnerProfileReadiness` (onLoad, Partner 360° Profile, Readiness & AI Review)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner 360° profile list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner 360° profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner 360° profile yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner 360° profile are still there. The pack's own statuses are 8.1.9 Partner lifecycle governance — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Partner documents (e.g. trade licence, VAT certificate) follow a review/accept/reject/resubmit flow; approval status runs lead > submitted > active > suspended; a partner 360 view consolidates profile, agreement and payment information in one view. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-550)*

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-031` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-031`
- Workshop pack: B2B, Reseller & OTA Partner Management_Reference.pdf board 1

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-031?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P10 as a whole** (12: 0 open, 12 closed). Open first; a closed row says where it went on 30 September.

- **A89** Build corporate/B2B self-service onboarding (trade licence & VAT upload → approve/reject → rate setup → credential issuance) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker)*
- **A135** Manage group, family and corporate/allocation ticket types inside the unified product screen rather than separate screens *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 25 Aug 2026 · workshop tracker)*
- **A170** Build family and corporate wallets (parent-funded child wristbands, per-member allowances, parent-only top-up, guest self-service family setup, department-segregated corporate funds, bidirectional transfer as a venue … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker)*
- **A178** Build B2B partner management (configurable profiles, onboarding workflow, sub-agents, territory and distribution rights, venue association with per-venue pricing, document compliance repository, action permissions … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A179** Support all three B2B/OTA routes (direct portal · bidirectional API with external OTAs · bulk pre-generated QR CSV for non-integrating partners), with an existing OTA integration reusable by configuration *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A180** Build B2B agreements & payment models (tiered volume discounts, commission rates, credit limit vs. prepaid wallet vs. card, partner-reserved inventory, booking limits) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A181** Build B2B settlement & reconciliation (per-partner operations dashboard, statements of account, exception management for unsettled transfers, dispute handling, AI partner performance view) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A184** Build group, school and corporate sales (inquiry dashboard, configurable customer categories, package builder against live inventory and resources, versioned quotations with discount approval, conversion to confirmed … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A208** Check amendments and cancellations against policy before allowing refund, cancellation or reschedule, track booking financial status, and support deposits for school and corporate bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 1 Sep 2026 · workshop tracker)*
- **A231** Build the live operations dashboard and group/B2B admission profile (real-time attendance by venue and gate, gate status, turnstile mode reconfigurable through the day, entry stats by category) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker)*
- **C35** Share the wallet-configuration reference documentation (foundation, funding, stored value, family/corporate, gift cards, payments, fraud/risk, API) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 27 Aug 2026 · workshop tracker)*
- **C44** Confirm how B2B/reseller-issued tickets are handled under a fully-dynamic-QR event policy *(Qossai · Pending → 30 Sep: Closed, Moved to T10 · 2 Sep 2026 · workshop tracker)*

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

### Across P10 Partner Web

- **Open question.** Qossai proposes a POS-style interface for high-volume resellers (hotels, travel agents) instead of a B2C-style site with login: assigned tickets and partner prices after login, optional cash drawer, sent-ticket history and resend, balance view. Chinmay wireframes both options; decide after review. *(open · MoM 29 Sep 2026, 3. B2B / reseller portal · DI-1023)*
- Qossai: partners may use the TICVAI B2B portal directly with a white-label-style B2B credential (similar to B2C), or integrate via API (preferred for OTAs such as Ticketmaster, Platinum List, BookMyShow). *(agreed · MoM 31 Aug 2026, 4.3 Clarified (integration models) · DI-552)*
- Partner access controls define which actions a partner may perform (e.g. refund, reschedule); the partner portal should only offer the actions granted. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-551)*
- Allam: B2B Portal option — partners without their own platform use a TICVAI B2B portal structured like the B2C store but behind login credentials, showing pre-configured partner pricing and products, with commission tracked the same way. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-134)*
- The POS/tablet application carries TICVAI's own branding and UI direction; the B2C and B2B mobile applications are white-label by design. *(agreed · MoM 31 Jul 2026, 15. Monday UI/UX Session Planning · DI-084)*
- Qossai: the target product is a white-label application supporting both B2C and B2B mobile use cases, built around three to four distinct flows (e.g. admission ticket flow, seat assignment flow). *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-056)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

**15 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

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
