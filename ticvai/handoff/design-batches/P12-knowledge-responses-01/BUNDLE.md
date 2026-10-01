# P12-knowledge-responses-01 — P12 · Knowledge & Responses

**2 screens · 5 operations · 8 schemas · 5 permissions**

Platform P12 Venue Support · ships as **venue-management** ·
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
  `AI_CONFIGURE, AI_USE, MARKETING_MANAGE, MARKETING_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
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
| `SUP-006` | Knowledge Base Search | B–D | 0 | 29 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `SUP-007` | Canned Response Management | B–D | 10 | 18 | 6 | 7 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**SUP-006 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `SUP-006` Knowledge Base Search

**Find something when the guest does not know what it is called.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Knowledge & Responses · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_CONFIGURE`, `AI_USE`, `TENANT_CONFIGURE` (2 configure, 1 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listKnowledgeCollections` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `bannerId` (deepLink), `pageId` (deepLink), `policyKind` (deepLink), `version` (deepLink) · cold entry: **A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is … |
| Route | `/general/knowledge-base-search` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **41 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Open · Assigned · Answered · Dismissed | `listKnowledgeGaps` ?status |
| Kind | segmented control | — | Knowledge · Analytics | `listKnowledgeGaps` ?kind |
| Audience | segmented control | — | Staff · Guest | `listKnowledgeGaps` ?audience |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every knowledge collection** (data table, from `listKnowledgeCollections`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Name | text | — |
| Description | text | — |
| Scope level | chip: Tenant, Region, Venue | — |
| Scope path | text | — |
| Document count | 1,234 | — |
| Shard key | text | The tenant boundary on shared placement (ADR-0021). A collection is shared by every tenant using the same embedding model, and the shard … |
| Retrieval | chip: Dense, Hybrid | Set at creation and not changeable. A collection created dense-only cannot gain a sparse index without a full rebuild, which is why this is … |
| Sparse model | text | The sparse signal, where `retrieval` is `hybrid`. BM25 unless a tenant needs otherwise. |
| Idf scope | chip: Shard, Tenant, Venue | Which population the sparse score measures rarity against (ADR-0021). Qdrant computes IDF statistics shard-wide by default, so a term … |
| Embedding model | text | This is what decides how many collections exist (ADR-0021). A collection carries its own vector configuration and a shard cannot, so … |
| Is active | yes / no (icon or chip) | — |

**Every faq category** (data table, from `listFaqs`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | in the reader's language | — |
| Sort order | 1,234 | — |
| Entries | list or chips (count when long) | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**The selected knowledge collection** (detail panel, from `listKnowledgeCollections`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Name | text | — |
| Description | text | — |
| Scope level | chip: Tenant, Region, Venue | — |
| Scope path | text | — |
| Document count | 1,234 | — |
| Shard key | text | The tenant boundary on shared placement (ADR-0021). A collection is shared by every tenant using the same embedding model, and the shard … |
| Retrieval | chip: Dense, Hybrid | Set at creation and not changeable. A collection created dense-only cannot gain a sparse index without a full rebuild, which is why this is … |
| Sparse model | text | The sparse signal, where `retrieval` is `hybrid`. BM25 unless a tenant needs otherwise. |
| Idf scope | chip: Shard, Tenant, Venue | Which population the sparse score measures rarity against (ADR-0021). Qdrant computes IDF statistics shard-wide by default, so a term … |
| Embedding model | text | This is what decides how many collections exist (ADR-0021). A collection carries its own vector configuration and a shard cannot, so … |
| Is active | yes / no (icon or chip) | — |

**Data it reads**: `listKnowledgeCollections` (onLoad, Collections an agent may search); `listFaqs` (onLoad, Published answers, as the guest sees them); `listKnowledgeGaps` (onLoad, Questions the assistant could not answer)

**Where the user goes next**

- → `SUP-001` Venue Management Sign In: *Agent Login*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The knowledge base search list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the knowledge base search untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No knowledge base search yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listKnowledgeCollections` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AI_CONFIGURE`, which `listKnowledgeCollections` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listKnowledgeCollections` → `AI_CONFIGURE` (configure) · staff
- `listFaqs` → `TENANT_CONFIGURE` (configure) · staff, guest
- `listKnowledgeGaps` → `AI_USE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `AI_CONFIGURE`, which `listKnowledgeCollections` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-006` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (29 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-006?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `SUP-001`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `TENANT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SUP-007` Canned Response Management

**Find canned response management for this venue.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P12 Venue Support (web) |
| Module | Knowledge & Responses · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listMessageTemplates` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/general/canned-response-management` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Channel | select | optional | — | Email · SMS · Whatsapp · Push · In app · Post | — | Sends `?channel=` to `listMessageTemplates`. | `listMessageTemplates` ?channel |

**Form: Create message template** (modal, opened by *Create message template*; *Create message template* calls `createMessageTemplate`, *Cancel* sends nothing)

**Collects what `createMessageTemplate` sends before it is called.** Required: `id`, `code`, `name`, `channel`, `bodies`. Optional: `subjects`, `mergeFields`, `missingLanguages`, `providerTemplateId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createMessageTemplate` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createMessageTemplate` body |
| Channel `channel` | select | required | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `createMessageTemplate` body |
| Subjects `subjects` | key and value settings | optional | — | — | — | Per language. Email only. | `createMessageTemplate` body |
| Bodies `bodies` | key and value settings | required | — | — | — | Per language, keyed by ISO 639-1 code. | `createMessageTemplate` body |
| Merge fields `mergeFields` | list of values (chips) | optional | — | — | — | — | `createMessageTemplate` body |
| Provider template `providerTemplateId` | text field | optional | — | — | — | Required for WhatsApp, where templates are pre-approved by the provider. | `createMessageTemplate` body |
| Brand `brandId` | picker: choose a brand | optional | — | — | shows names, sends the id | The brand whose identity the template carries; null for the tenant default. | `createMessageTemplate` body |
| Ownership `ownership` | segmented control | optional | Crm | Platform · Crm | — | `platform` = a transactional template owned by the communication service; `crm` = a marketing template owned by CRM (`listSystemTransactionalTemplate`). | `createMessageTemplate` body |

Errors to draw in the form: 400 Unknown merge field, or a required language is missing

#### Outputs: what the screen shows and produces

**Shown**

**Every message template** (data table, from `listMessageTemplates`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Subjects | grouped details | Per language. Email only. |
| Bodies | grouped details | Per language, keyed by ISO 639-1 code. |
| Merge fields | list or chips (count when long) | — |
| Missing languages | list or chips (count when long) | Enabled languages without a body. Flagged rather than silently falling back — a guest receiving English when they chose Arabic is a defect. |
| Provider template | text | Required for WhatsApp, where templates are pre-approved by the provider. |

**The selected message template** (detail panel, from `listMessageTemplates`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Subjects | grouped details | Per language. Email only. |
| Bodies | grouped details | Per language, keyed by ISO 639-1 code. |
| Merge fields | list or chips (count when long) | — |
| Missing languages | list or chips (count when long) | Enabled languages without a body. Flagged rather than silently falling back — a guest receiving English when they chose Arabic is a defect. |
| Provider template | text | Required for WhatsApp, where templates are pre-approved by the provider. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create message template (primary button) | `createMessageTemplate` POST `/message-templates` | MessageTemplate | MessageTemplate | 400 Unknown merge field, or a required language is missing | opens modal first |

**Data it reads**: `listMessageTemplates` (onLoad, from page inventory)

**Where the user goes next**

- → `SUP-001` Venue Management Sign In: *Agent Login*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The canned response list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the canned response untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No canned response yet. Offers Create message template (`createMessageTemplate`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on channel and the canned response are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `MARKETING_VIEW`, which `listMessageTemplates` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Unknown merge field, or a required language is missing |

#### Permissions

- `listMessageTemplates` → `MARKETING_VIEW` (read) · staff
- `createMessageTemplate` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `MARKETING_VIEW`, which `listMessageTemplates` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.3 | The system should support email templates for e-ticket purchase confirmation supporting dynamic parameters. The email templates should be configurable per site, per event | Ticketing Sales | CONTRACTED | `listMessageTemplates` |
| 2.6.26 | It is expected that confirmation email can be generated including the number of tickets, the cost, the order number. | Ticketing Sales | CONTRACTED | `listMessageTemplates` |
| 22.1.2 | Campaign Templates | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.1.7 | Dynamic Personalization | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.9.1 | Notification Template Management | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.9.3 | Dynamic Personalization | Marketing & CRM | CONTRACTED | `createMessageTemplate` |
| 22.9.22 | Rich Content Notifications | Marketing & CRM | CONTRACTED | `createMessageTemplate` |

#### Client meeting inputs

None names this screen.

Also apply: 7 for all of P12, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P12 Venue Support.dc.html#sup-007` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SUP-007?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create message template.
- [ ] Every transition is wired: `SUP-001`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P12 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for operator density.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

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

### Across P12 Venue Support

- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- Client support staff log into TICVAI to view and respond to their own tickets/chats (keeps a full audit trail); adapters to clients' own support systems are phase two. *(agreed · MoM 12 Aug 2026, 10. Customer Support / Chat Integration Approach · DI-257)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createMessageTemplate": {"method":"POST","path":"/message-templates","contract":"marketing-crm","summary":"Create a message template","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MessageTemplate","responds":"MessageTemplate"},
"listFaqs": {"method":"GET","path":"/tenant-config/faqs","contract":"white-label","summary":"List FAQs","permission":"TENANT_CONFIGURE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"FaqCategory"},
"listKnowledgeCollections": {"method":"GET","path":"/collections","contract":"ai","summary":"Collections available to this tenant","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"KnowledgeCollection"},
"listKnowledgeGaps": {"method":"GET","path":"/knowledge-gaps","contract":"ai","summary":"Questions the assistant could not answer","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"audience","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMessageTemplates": {"method":"GET","path":"/message-templates","contract":"marketing-crm","summary":"List message templates","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiKnowledgeGap": {"type":"object","x-ticvai-persistence":"ai.knowledge_gap","description":"**A question the assistant could not answer**, grouped so the content owner gets a task, not a log (AIC-061, AIC-062). Also written for an analytics question outside the semantic model (design 5.7).","required":["question","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"question":{"type":"string","description":"The normalised question."},"examples":{"type":"array","items":{"type":"string"},"description":"Up to ten phrasings as asked, with personal data masked."},"occurrences":{"type":"integer","minimum":1,"readOnly":true},"audience":{"type":"string","enum":["staff","guest"]},"locale":{"type":"string","nullable":true},"kind":{"type":"string","enum":["knowledge","analytics"]},"suggestedCollectionId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.knowledge_collection"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal"},"status":{"type":"string","enum":["open","assigned","answered","dismissed"]},"resolvedDocumentId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.knowledge_document"},"lastAskedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"FaqCategory": {"x-ticvai-persistence":"whitelabel.faq_category + whitelabel.faq_entry","type":"object","required":["code","name","entries"],"properties":{"code":{"type":"string"},"name":{"$ref":"#/components/schemas/LocalisedText"},"sortOrder":{"type":"integer"},"entries":{"type":"array","items":{"type":"object","required":["id","question","answer"],"properties":{"id":{"type":"string","format":"uuid"},"question":{"$ref":"#/components/schemas/LocalisedText"},"answer":{"$ref":"#/components/schemas/LocalisedRichText"},"sortOrder":{"type":"integer"},"isPublished":{"type":"boolean"}}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"KnowledgeCollection": {"type":"object","x-ticvai-persistence":"ai.knowledge_collection","required":["name","scopeLevel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string"},"description":{"type":"string"},"scopeLevel":{"type":"string","enum":["tenant","region","venue"]},"scopePath":{"type":"string","readOnly":true},"documentCount":{"type":"integer","readOnly":true},"shardKey":{"type":"string","readOnly":true,"description":"**The tenant boundary on shared placement** (ADR-0021). A collection is shared by every tenant using the same embedding model, and the shard separates them — set at provisioning from the tenant, never from a request.\nOn dedicated placement there is one shard and this is still populated, because a tenant moving from shared to dedicated moves a shard rather than being re-indexed.\n"},"retrieval":{"type":"string","enum":["dense","hybrid"],"default":"hybrid","description":"**Set at creation and not changeable.** A collection created dense-only cannot gain a sparse index without a full rebuild, which is why this is a creation decision rather than a query one.\nHybrid is the default because **a venue corpus is mostly proper nouns** — Yas Waterworld, Bronze Annual Pass, a menu item name. Dense retrieval is good at meaning and poor at exact tokens, and half our queries are exact tokens.\n"},"sparseModel":{"type":"string","nullable":true,"description":"The sparse signal, where `retrieval` is `hybrid`. BM25 unless a tenant needs otherwise."},"idfScope":{"type":"string","enum":["shard","tenant","venue"],"default":"tenant","description":"**Which population the sparse score measures rarity against** (ADR-0021). Qdrant computes IDF statistics shard-wide by default, so a term common at one venue and rare at another gets one score for both. Shard-per-tenant fixes the cross-tenant case; **inside a dedicated cell the shard is the whole tenant and venues share it**, which is what this narrows.\n"},"embeddingModel":{"type":"string","readOnly":true,"description":"**This is what decides how many collections exist** (ADR-0021). A collection carries its own vector configuration and a shard cannot, so vectors from two models cannot share one. A tenant that residency forces onto a local model therefore has its own collection — forced by the model, not chosen for isolation.\nRead-only because **changing it invalidates every embedding in the collection**, and a collection silently searched with mismatched vectors returns plausible nonsense.\n"},"isActive":{"type":"boolean"}}},
"LocalisedRichText": {"x-ticvai-persistence":"none — jsonb column","type":"object","description":"Keyed by language code. Values are sanitised HTML.","additionalProperties":{"type":"string"}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MessageTemplate": {"x-ticvai-persistence":"marketing.message_template","type":"object","required":["id","code","name","channel","bodies"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"channel":{"$ref":"#/components/schemas/MessageChannel"},"subjects":{"type":"object","description":"Per language. Email only.","additionalProperties":{"type":"string"}},"bodies":{"type":"object","description":"Per language, keyed by ISO 639-1 code.","additionalProperties":{"type":"string"}},"mergeFields":{"type":"array","items":{"type":"string"}},"missingLanguages":{"type":"array","readOnly":true,"description":"Enabled languages without a body. Flagged rather than silently falling back — a guest receiving English when they chose Arabic is a defect.\n","items":{"type":"string"}},"providerTemplateId":{"type":"string","nullable":true,"description":"Required for WhatsApp, where templates are pre-approved by the provider."},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand whose identity the template carries; null for the tenant default."},"ownership":{"type":"string","enum":["platform","crm"],"default":"crm","description":"`platform` = a transactional template owned by the communication service; `crm` = a marketing template owned by CRM (`listSystemTransactionalTemplate`). Content by language and version is in `MessageTemplateVersion`. (decided 29 September, data model for the agreed operations)"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}}
}
```
