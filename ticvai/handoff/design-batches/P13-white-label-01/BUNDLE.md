# P13-white-label-01 — P13 · White Label (1 of 3)

**10 screens · 58 operations · 59 schemas · 9 permissions**

Platform P13 Venue CMS · ships as **venue-management** ·
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

- **Every control that can be refused must be gated.** 9 permissions apply here:
  `AI_USE, ASSET_LIBRARY_MANAGE, ASSET_LIBRARY_VIEW, ORDER_CREATE, ORDER_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, TENANT_CONFIGURE, TENANT_PUBLISH`. A control nobody can use must say so,
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
| `CMS-001` | Tenant Workspace | A | 20 | 42 | 5 | 9 | 1 | 0 | configures | notStarted (generated) |
| `CMS-002` | Brand Kit | A | 31 | 9 | 5 | 3 | 4 | 6 | configures | notStarted (generated) |
| `CMS-003` | Typography | A | 36 | 15 | 5 | 5 | 4 | 6 | configures | notStarted (generated) |
| `CMS-004` | Logo & Assets | A | 11 | 16 | 5 | 3 | 3 | 6 | configures | notStarted (generated) |
| `CMS-005` | Theme Editor | A | 31 | 11 | 5 | 4 | 9 | 6 | configures | notStarted (generated) |
| `CMS-006` | Component Preview | A | 6 | 18 | 6 | 4 | 4 | 0 | — | notStarted (generated) |
| `CMS-007` | Page Builder | A | 38 | 16 | 5 | 15 | 4 | 6 | configures | notStarted (generated) |
| `CMS-008` | Content Blocks | A | 62 | 33 | 6 | 10 | 2 | 6 | configures | notStarted (generated) |
| `CMS-009` | Navigation & Menus | A | 55 | 17 | 6 | 8 | 4 | 6 | configures | notStarted (generated) |
| `CMS-010` | Media Library | A | 99 | 67 | 6 | 36 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**CMS-005 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `CMS-001` Tenant Workspace

**Land a tenant somewhere that shows what is live and what is not, and hold step 1 of the Site Builder (venue and modules).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `core` module |
| Block | Block A · ticket #18099 (APP-WL-CMS-001) |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getTenantAppStatus` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/white-label/tenant-workspace` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **The tenant workspace.** Lands a tenant on what is live rather than on a form. **Declared 20 August** — `isEntryPoint` existed in the schema and five platforms used none, so every screen in them read as unreachable. **Drawn 31 August** — `Marketing Board 7.dc.html` frame `crm-7f` (*Agent Workspace*), matched on title at 0.84 within this board’s platforms. **Rewired 23 September (L7).** The screen called the maintenance equipment register, guest CRM or subscription billing where its purpose names White Labelling. Its operations now match its purpose.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Version | text field | — | — | `getTenantConfig` ?version |

**Form: Save module enablement** (modal, opened by *Save module enablement*; *Save module enablement* calls `setModuleEnablement`, *Cancel* sends nothing)

**Collects what `setModuleEnablement` sends before it is called.** Required: `modules`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Modules `modules` | repeatable rows | required | — | — | — | — | `setModuleEnablement` body |
| Module key `modules[].moduleKey` | select | required | — | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | — | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown. | `setModuleEnablement` body |
| Is enabled `modules[].isEnabled` | toggle | required | — | — | — | — | `setModuleEnablement` body |

Errors to draw in the form: 400 Module not licensed, or still referenced by navigation or homepage (ModuleReferenceProblem)

**Form: Save feature toggles** (modal, opened by *Save feature toggles*; *Save feature toggles* calls `setFeatureToggles`, *Cancel* sends nothing)

**Collects what `setFeatureToggles` sends before it is called.** Required: `features`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Features `features` | repeatable rows | required | — | — | — | — | `setFeatureToggles` body |
| Feature key `features[].featureKey` | select | required | — | Digital companion mode · AI concierge chat · Lost and found · Push notifications · Social sharing · Multi language · Apple wallet · Google pay · Apple pay · Cash on delivery · Guest checkout · Uae pass login | — | The feature toggles a tenant can set — one list for `FeatureToggle` and the `setFeatureToggles` body, which took a free string where the response had this enum. | `setFeatureToggles` body |
| Is enabled `features[].isEnabled` | toggle | required | — | — | — | — | `setFeatureToggles` body |

**Form: Save maintenance mode** (modal, opened by *Save maintenance mode*; *Save maintenance mode* calls `setMaintenanceMode`, *Cancel* sends nothing)

**Collects what `setMaintenanceMode` sends before it is called.** Required: `isInMaintenance`. Optional: `message`, `expectedBackAt`, `minimumAppVersion` (`ios`, `android`), `contact` (`phone`, `email`, `whatsapp`, `address`, `openingHours`), `availability` (`open`, `soldOut`, `closed`) and `availabilityMessage`. **The live app status is set here, not published** (decided 28 September, audit R073 (b)(f)): a guest app below `minimumAppVersion` for its platform is sent to the forced upgrade (GST-047), the contact details feed WEB-028 and the availability feeds WEB-029's sold-out and closed states. A field not sent is left as it is, so clearing maintenance does not clear the contact details. …

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Is in maintenance `isInMaintenance` | toggle | required | — | — | — | — | `setMaintenanceMode` body |
| Message `message` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setMaintenanceMode` body |
| Expected back at `expectedBackAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setMaintenanceMode` body |
| Minimum app version `minimumAppVersion` | group | optional | — | — | — | The oldest guest app build still allowed to run (decided 28 September, audit R073). | `setMaintenanceMode` body |
| Ios `minimumAppVersion.ios` | text field | optional | — | pattern `^\d+\.\d+\.\d+$` | — | — | `setMaintenanceMode` body |
| Android `minimumAppVersion.android` | text field | optional | — | pattern `^\d+\.\d+\.\d+$` | — | — | `setMaintenanceMode` body |
| Contact `contact` | group | optional | — | — | — | How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). | `setMaintenanceMode` body |
| Phone `contact.phone` | phone field | optional | — | — | +971 5X XXX XXXX (E.164) | — | `setMaintenanceMode` body |
| Email `contact.email` | email field | optional | — | — | name@example.ae | — | `setMaintenanceMode` body |
| Whatsapp `contact.whatsapp` | text field | optional | — | — | — | — | `setMaintenanceMode` body |
| Address `contact.address` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setMaintenanceMode` body |
| Opening hours `contact.openingHours` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Prose, as the guest reads it. The bookable hours are the catalogue's. | `setMaintenanceMode` body |
| Availability `availability` | segmented control | optional | Open | Open · Sold out · Closed | — | The sold-out or closed signal (decided 28 September, audit R073). `open` is the normal state. | `setMaintenanceMode` body |
| Availability message `availabilityMessage` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setMaintenanceMode` body |

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
| Minimum app version | grouped details | The oldest guest app build still allowed to run (decided 28 September, audit R073). |
| Contact | grouped details | How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided … |
| Availability | chip: Open, Sold out, Closed | The sold-out or closed signal (decided 28 September, audit R073). `open` is the normal state. |
| Availability message | in the reader's language | What the sold-out or closed screen says (WEB-029). Null shows the default wording. |
| Recent changes | list or chips (count when long) | Staff only. Names the principal behind each change, so it never reaches a public response. |

**The tenant config** (detail panel, from `getTenantConfig`)

| Shows | Format | Notes |
|---|---|---|
| Is draft | yes / no (icon or chip) | True for the working draft, which is the only row. |
| Brand | grouped details | Every `*AssetRef` here is a `MediaAsset` id from the `assets` library (`createUpload` then `completeUpload`), PNG or SVG and at most 2 MB … |
| App icons | grouped details | — |
| Booking flow | grouped details | Set per tenant, with a per-venue override (decided 29 September, rev 3 CFG-11). One tenant with several venues (the Kids Club branches … |
| Theme | grouped details | — |
| Fonts | grouped details | — |
| Footer | grouped details | BL-002. `setHeader` and `HeaderConfig` exist and the footer does not, which looked like symmetry until you notice it is not: a header is … |
| Notification branding | grouped details | BL-003. `marketing-crm` holds the templates and nothing said whose identity they wear. |
| Enabled payment methods | list or chips (count when long) | BL-004. `FeatureToggle` could turn Apple Pay on and could not say which cards a tenant accepts. |
| Accessibility | grouped details | BL-065, 2.1.27. POS and kiosk accessibility, which is a legal obligation in most jurisdictions and was unstated. |
| Header | grouped details | — |
| Navigation | grouped details | The mobile tab set is venue configuration (decided 29 September, MOB-1; 29 September brief decision 6). |
| Homepage | grouped details | — |
| Modules | list or chips (count when long) | — |
| Features | list or chips (count when long) | — |
| Languages | grouped details | — |

**The module enablement** (detail panel, from `getModuleEnablement`)

| Shows | Format | Notes |
|---|---|---|
| Module key | chip: Tickets and booking, Membership, Events, Attractions, Virtual queue, Dining and fnb… | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not … |
| Display name | text | — |
| Is licensed | yes / no (icon or chip) | From the tenant's subscription. False makes enablement impossible. |
| Is enabled | yes / no (icon or chip) | — |
| Referenced by | list or chips (count when long) | Navigation items and homepage sections pointing at this module. Maintained by `setNavigation` and `setHomepageLayout` in the same … |

**The feature toggle** (detail panel, from `getFeatureToggles`)

| Shows | Format | Notes |
|---|---|---|
| Feature key | chip: Digital companion mode, AI concierge chat, Lost and found, Push notifications … | `guestCheckout` is off by default (decided 17 September 2026, matrix 2.6.28, placement settled by … |
| Display name | text | — |
| Is enabled | yes / no (icon or chip) | — |
| Change scope | chip: Runtime, Build time | Wallet and payment integrations are `buildTime` on native apps — enabling one needs a release, not a publish. |
| Requires configuration | yes / no (icon or chip) | True where the feature needs credentials or setup elsewhere first. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save module enablement (primary button) | `setModuleEnablement` PUT `/tenant-config/modules` | inline | ModuleEnablement[] | 400 Module not licensed, or still referenced by navigation or homepage (ModuleReferenceProblem) | opens modal first |
| Save feature toggles (secondary button) | `setFeatureToggles` PUT `/tenant-config/features` | inline | FeatureToggle[] | — | opens modal first |
| Save maintenance mode (secondary button) | `setMaintenanceMode` PUT `/tenant-config/status` | inline | TenantAppStatus | — | opens modal first |

**Data it reads**: `getTenantAppStatus` (onLoad, Whether the guest web and app are live); `getTenantConfig` (onLoad, The published configuration); `getModuleEnablement` (onLoad, Which modules guests can see); `getFeatureToggles` (onLoad, Which features are switched on)

**Where the user goes next**

- → `CMS-102` Site Builder: *Site Builder*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-004` Logo & Assets: *Logo & Assets*
- → `CMS-061` Digital Asset Management Command Center: *Digital Asset Management Command Center*
- → `CMS-071` AI Asset Intelligence Command Center: *AI Asset Intelligence Command Center*
- → `CMS-081` DAM Governance & Rights Command Center: *DAM Governance & Rights Command Center*
- → `CMS-091` Asset Distribution & Delivery Command Center: *Asset Distribution & Delivery Command Center*
- → `CMS-008` Content Blocks: *Content Blocks*
- → `CMS-009` Navigation & Menus: *Navigation & Menus*
- → `CMS-010` Media Library: *Media Library*
- → `CMS-011` Translations: *Translations*
- → `CMS-016` Site Settings: *Site Settings*
- → `CMS-019` User Access: *User Access*
- → `CMS-015` Version History: *Version History*; carries `version`
- → `CMS-021` Privacy & Consent Configuration Command Center: *Privacy & Consent Configuration Command Center*
- → `CMS-031` Privacy Operations Command Center: *Privacy Operations Command Center*
- → `CMS-041` Waiver & Consent Command Center: *Waiver & Consent Command Center*
- → `CMS-051` Waiver Operations Command Center: *Waiver Operations Command Center*
- → `CMS-003` Typography: *Typography*; carries `version`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tenant, read by `getTenantAppStatus`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tenant untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tenant yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getTenantConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Module not licensed, or still referenced by navigation or homepage (ModuleReferenceProblem) |

#### Permissions

- `getTenantAppStatus` → no permission · device, guest
- `getTenantConfig` → `TENANT_CONFIGURE` (configure) · staff, guest
- `getModuleEnablement` → `TENANT_CONFIGURE` (configure) · staff
- `getFeatureToggles` → `TENANT_CONFIGURE` (configure) · staff
- `setModuleEnablement` → `TENANT_CONFIGURE` (configure) · staff
- `setFeatureToggles` → `TENANT_CONFIGURE` (configure) · staff
- `setMaintenanceMode` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getTenantConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.19 | Tenant-Specific Branding - System shall support tenant-specific branding. | Guest Mobile App & Branding | CONTRACTED | `getTenantConfig` |
| 22.10.1 | Multi-Site CMS | Marketing & CRM | CONTRACTED | `getTenantConfig` |
| 22.10.3 | Multi-Brand Management | Marketing & CRM | CONTRACTED | `getTenantConfig` |
| 19.1.13 | Module Enablement - System shall allow enabling and disabling application modules. | Guest Mobile App & Branding | CONTRACTED | `setModuleEnablement` |
| 19.1.22 | Tenant-Specific Features - System shall support tenant-specific features. | Guest Mobile App & Branding | CONTRACTED | `setFeatureToggles` |
| 19.2.83 | Digital Companion Mode - System shall transform the app into an in-venue digital companion experience. | Guest Mobile App & Branding | CONTRACTED | data `FeatureToggle` |
| 1.3.30 | System shall support physical, virtual and hybrid events with configurable attendance rules and access methods. | Ticketing Catalogue | CONTRACTED | data `FeatureToggle` |
| 19.1.21 | Tenant-Specific Notifications - System shall support tenant-specific notifications. | Guest Mobile App & Branding | CONTRACTED | data `TenantConfig` |
| 19.1.23 | Tenant-Specific Payment Methods - System shall support tenant-specific payment methods. | Guest Mobile App & Branding | CONTRACTED | data `TenantConfig` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The CMS is a step-based site builder started from the workspace; a preset keeps the minimum path short (modules, booking flows, home sections and mobile tabs proposed), so an operator supplies only a logo, four colours and Publish; aim about 30 minutes to a working site. *(agreed · MoM 24 Sep 2026, M24-05 · DI-997)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Modules (`modules.modules`) | — | — | every guest screen (web, app and kiosk) | — |
| Modules: module key (`modules.modules[].moduleKey`) | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | — | WEB-050 | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown. |
| Modules: is enabled (`modules.modules[].isEnabled`) | — | — | every guest screen (web, app and kiosk) | — |
| Features (`features.features`) | — | — | every guest screen (web, app and kiosk) | — |
| Features: feature key (`features.features[].featureKey`) | Digital companion mode · AI concierge chat · Lost and found · Push notifications · Social sharing · Multi language · Apple wallet · Google pay · Apple pay · Cash on delivery · Guest checkout · Uae … | — | every guest screen (web, app and kiosk) | The feature toggles a tenant can set — one list for `FeatureToggle` and the `setFeatureToggles` body, which took a free string where the response had this enum. |
| Features: is enabled (`features.features[].isEnabled`) | — | — | every guest screen (web, app and kiosk) | — |
| Is in maintenance (`maintenance.isInMaintenance`) | — | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, WEB-001 … (13) | — |
| Availability and maintenance message (`maintenance.message`) | English and Arabic (Arabic right to left) | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, WEB-001 … (13) | — |
| Expected back at (`maintenance.expectedBackAt`) | 1 Oct 2026, 14:30 (venue time zone) | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, WEB-001 … (13) | — |
| Minimum app version (`maintenance.minimumAppVersion`) | — | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, WEB-001 … (13) | The oldest guest app build still allowed to run (decided 28 September, audit R073). |
| Minimum app version: ios (`maintenance.minimumAppVersion.ios`) | pattern `^\d+\.\d+\.\d+$` | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, WEB-001 … (13) | — |
| Minimum app version: android (`maintenance.minimumAppVersion.android`) | pattern `^\d+\.\d+\.\d+$` | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, WEB-001 … (13) | — |
| Contact (`maintenance.contact`) | — | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, WEB-001 … (13) | How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). |
| Contact: phone (`maintenance.contact.phone`) | +971 5X XXX XXXX (E.164) | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, WEB-001 … (13) | — |
| Contact: email (`maintenance.contact.email`) | name@example.ae | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, WEB-001 … (13) | — |
| Contact: whatsapp (`maintenance.contact.whatsapp`) | — | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, WEB-001 … (13) | — |
| Contact: address (`maintenance.contact.address`) | English and Arabic (Arabic right to left) | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, WEB-001 … (13) | — |
| Contact: opening hours (`maintenance.contact.openingHours`) | English and Arabic (Arabic right to left) | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, WEB-001 … (13) | Prose, as the guest reads it. The bookable hours are the catalogue's. |
| Availability (`maintenance.availability`) | Open · Sold out · Closed | Open | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, WEB-001 … (13) | The sold-out or closed signal (decided 28 September, audit R073). `open` is the normal state. |
| Availability message (`maintenance.availabilityMessage`) | English and Arabic (Arabic right to left) | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, WEB-001 … (13) | — |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-001` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Marketing Board 7.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Marketing Board 7.dc.html`
- Client design-board frames: `Marketing Board 7.dc.html#crm-7f`
- Flow F102 *A brand is set, previewed, published and rolled back*, step 1: Tenant Workspace. See what is live before changing the brand. → The current published state is known, so a change can be compared against it. Rewired 23 September (L7) from subscription and billing operations, which the screen no longer declares.
- Flow F102 branch at step 1 (medium): when The acting principal lacks the permission at this scope., **Refused at the first step, not the last.** ADR-0002 makes authorisation user-driven — a person who gets three steps in and then cannot finish has been told the wrong thing.

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (42 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-001?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save module enablement, Save feature toggles, Save maintenance mode.
- [ ] Every transition is wired: `CMS-102`, `CMS-002`, `CMS-004`, `CMS-061`, `CMS-071`, `CMS-081`, `CMS-091`, `CMS-008`, `CMS-009`, `CMS-010`, `CMS-011`, `CMS-016`, `CMS-019`, `CMS-015`, `CMS-021`, `CMS-031`, `CMS-041`, `CMS-051`, `CMS-003`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-002` Brand Kit

**Set the things every surface reads.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `core` module |
| Block | Block A · ticket #18100 (APP-WL-CMS-002) |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `TENANT_CONFIGURE` (2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getBrandIdentity` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `uploadId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/white-label/brand-kit` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**Form: Save brand identity** (modal, opened by *Save brand identity*; *Save brand identity* calls `setBrandIdentity`, *Cancel* sends nothing)

**Collects what `setBrandIdentity` sends before it is called.** Required: `logoAssetRef`. Optional: `logoVariant` (light, dark or duotone: which lockup sits in the nav bar and which colour reading of it drives the theme, decided 29 September, rev 3 CFG-4), `logoDarkAssetRef`, `faviconAssetRef`, `splashImageAssetRefs`, `splashDurationSeconds`, `splashBackgroundColour`, `showLoadingIndicator`, `splashChangeScope`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Logo `logoAssetRef` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The primary logo. | `setBrandIdentity` body |
| Logo dark image `logoDarkAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | Used on dark backgrounds. Falls back to the primary logo. | `setBrandIdentity` body |
| Logo variant `logoVariant` | segmented control | optional | Light | Light · Dark · Duotone | — | Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4). | `setBrandIdentity` body |
| Favicon `faviconAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The browser tab icon for the guest web app. | `setBrandIdentity` body |
| Splash image `splashImageAssetRefs` | media picker (several) | optional | — | — | PNG, JPG, SVG or MP4 from the media library | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). | `setBrandIdentity` body |
| Splash duration seconds `splashDurationSeconds` | stepper or slider (seconds) | optional | 3 | min 0; max 10 | — | — | `setBrandIdentity` body |
| Splash background colour `splashBackgroundColour` | colour picker | optional | — | — | #RRGGBB | — | `setBrandIdentity` body |
| Show loading indicator `showLoadingIndicator` | toggle | optional | on | — | — | — | `setBrandIdentity` body |
| Intro video `introVideoAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). | `setBrandIdentity` body |
| Intro video mode `introVideoMode` | segmented control | optional | Off | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | — | When GST-001 plays it full screen. "Skip introduction" is always shown. | `setBrandIdentity` body |

Errors to draw in the form: 400 An asset is larger than 2 MB, or is not PNG or SVG (audit R270)

**Form: Create upload** (modal, opened by *Create upload*; *Create upload* calls `createUpload`, *Cancel* sends nothing)

**Collects what `createUpload` sends before it is called.** Required: `filename`, `contentType`, `sizeBytes`. Optional: `venueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Filename `filename` | text area | required | — | max length 256 | — | — | `createUpload` body |
| Content type `contentType` | text field | required | — | — | — | — | `createUpload` body |
| Size bytes `sizeBytes` | number field | required | — | min 1 | — | — | `createUpload` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createUpload` body |

Errors to draw in the form: 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes.

**Form: Complete upload** (modal, opened by *Complete upload*; *Complete upload* calls `completeUpload`, *Cancel* sends nothing)

**Collects what `completeUpload` sends before it is called.** Nothing in the body is required. Optional: `title`, `altText`, `tags`, `collectionIds`, `rights`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `completeUpload` body |
| Alt text `altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `completeUpload` body |
| Tags `tags` | list of values (chips) | optional | — | — | — | — | `completeUpload` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | — | `completeUpload` body |
| Rights `rights` | group | optional | — | — | — | Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item. | `completeUpload` body |
| Licence kind `rights.licenceKind` | select | optional | — | Owned · Royalty free · Rights managed · Creative commons · Editorial only · Unknown | — | — | `completeUpload` body |
| Licensor `rights.licensor` | text field | optional | — | — | — | — | `completeUpload` body |
| Licence reference `rights.licenceReference` | text field | optional | — | — | — | — | `completeUpload` body |
| Valid from `rights.validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `completeUpload` body |
| Valid to `rights.validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `completeUpload` body |
| Permitted uses `rights.permittedUses` | multi-select chips | optional | — | Web · Print · Social media · In venue · Advertising · Internal | — | — | `completeUpload` body |
| Attribution required `rights.attributionRequired` | toggle | optional | off | — | — | — | `completeUpload` body |
| Attribution text `rights.attributionText` | text field | optional | — | — | — | — | `completeUpload` body |
| Permitted territories `rights.permittedTerritories` | list of values (chips) | optional | — | — | — | ISO country or region codes. Empty means unrestricted, which is a claim rather than an absence — an unknown territory and a worldwide licence are not the same thing, and … | `completeUpload` body |
| Permitted channels `rights.permittedChannels` | list of values (chips) | optional | — | — | — | Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route. | `completeUpload` body |
| Model release held `rights.modelReleaseHeld` | toggle | optional | off | — | — | — | `completeUpload` body |
| Renewal owner `rights.renewalOwner` | picker: choose a renewal owner | optional | — | — | shows names, sends the id | — | `completeUpload` body |

Errors to draw in the form: 409 The transfer never finished (`transferIncomplete`), the upload ticket expired (`uploadExpired`), or the stored file is larger than the ticket allowed … (UploadRefusedProblem)

#### Outputs: what the screen shows and produces

**Shown**

**The brand identity** (detail panel, from `getBrandIdentity`)

| Shows | Format | Notes |
|---|---|---|
| Logo | the image or video | The primary logo. |
| Logo dark image | the image or video | Used on dark backgrounds. Falls back to the primary logo. |
| Logo variant | chip: Light, Dark, Duotone | Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4). |
| Favicon | the image or video | The browser tab icon for the guest web app. |
| Splash image | list or chips (count when long) | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish … |
| Splash duration seconds | 1,234 | — |
| Splash background colour | colour swatch | — |
| Show loading indicator | yes / no (icon or chip) | — |
| Splash change scope | chip: Runtime, Build time | Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save brand identity (primary button) | `setBrandIdentity` PUT `/tenant-config/brand` | BrandIdentity | BrandIdentity | 400 An asset is larger than 2 MB, or is not PNG or SVG (audit R270) | opens modal first |
| Create upload (secondary button) | `createUpload` POST `/media/uploads` | inline | UploadTicket | 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes. | opens modal first |
| Complete upload (secondary button) | `completeUpload` POST `/media/uploads/{uploadId}/complete` | inline | MediaAsset | 409 The transfer never finished (`transferIncomplete`), the upload ticket expired (`uploadExpired`), or the stored file is larger than the ticket allowed … (UploadRefusedProblem) | opens modal first |

**Data it reads**: `getBrandIdentity` (onLoad, Read brand identity)

**Where the user goes next**

- → `CMS-005` Theme Editor: *Sets the colour theme*
- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-003` Typography: *Typography*
- → `CMS-004` Logo & Assets: *Logo & Assets*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The brand kit, read by `getBrandIdentity`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the brand kit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No brand kit yet. Offers Create upload (`createUpload`). |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getBrandIdentity` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 An asset is larger than 2 MB, or is not PNG or SVG (audit R270); 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes.; 409 The transfer never finished (`transferIncomplete`), the upload ticket expired (`uploadExpired`), or the stored file is larger than the ticket allowed … (UploadRefusedProblem) |

#### Permissions

- `getBrandIdentity` → `TENANT_CONFIGURE` (configure) · staff
- `setBrandIdentity` → `TENANT_CONFIGURE` (configure) · staff
- `createUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `completeUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getBrandIdentity` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.1 | Logo Management - System shall allow changing the mobile app logo through configuration. | Guest Mobile App & Branding | CONTRACTED | `setBrandIdentity` |
| 19.1.2 | Splash Screen Management - System shall allow changing splash screens. | Guest Mobile App & Branding | CONTRACTED | `setBrandIdentity` |
| 23.1.4 | Authorized users shall upload assets individually or in bulk through web interfaces and APIs. | Digital Asset Management | CONTRACTED | `createUpload` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Qossai: white-labelling needs more flexibility, e.g. setting the colour of specific interactive elements such as the "pay now" / "purchase" button independently, not only an overall palette, while the guest experience stays a standardised flow with configurable limits. *(client request · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-918)*
- CMS manages multiple sites/venues: branding, colour palette including custom hex codes, fonts, Google Analytics site IDs, production/staging environments. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-393)*
- Guest-app builder: tenant uploads client logo (multiple formats), picks colour themes, app icon and custom font, with a live preview before publishing. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-187)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Logo (`brand.logoAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | every guest screen (web, app and kiosk) | the logo in the header or nav bar, the splash and the footer |
| Logo dark image (`brand.logoDarkAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | every guest screen (web, app and kiosk) | the logo on dark backgrounds (falls back to the primary logo) |
| Logo variant (`brand.logoVariant`) | Light · Dark · Duotone | Light | every guest screen (web, app and kiosk) | which logo lockup sits in the nav bar, and whose colours drive the theme |
| Favicon (`brand.faviconAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | every P01 screen | the browser tab icon (website only) |
| Splash image (`brand.splashImageAssetRefs`) | PNG, JPG, SVG or MP4 from the media library | — | every P02 screen | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). |
| Splash duration seconds (`brand.splashDurationSeconds`) | min 0; max 10 | 3 | every guest screen (web, app and kiosk) | — |
| Splash background colour (`brand.splashBackgroundColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Show loading indicator (`brand.showLoadingIndicator`) | — | on | every guest screen (web, app and kiosk) | — |
| Intro video (`brand.introVideoAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | GST-001 | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode (`brand.introVideoMode`) | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | Off | GST-001 | When GST-001 plays it full screen. "Skip introduction" is always shown. |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-002` · status **notStarted** · provenance generated
- Flow F22 *A tenant rebrands their app*, step 1: Uploads the new logo and icons → **Assets, not code.** A logo change must not be a release

#### Acceptance for the design

- [ ] Every input above is drawn (31), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-002?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save brand identity, Create upload, Complete upload.
- [ ] Every transition is wired: `CMS-005`, `CMS-001`, `CMS-003`, `CMS-004`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `TENANT_CONFIGURE`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-003` Typography

**Choose the two typefaces and the scale under them.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `core` module |
| Block | Block A · ticket #18101 (APP-WL-CMS-003) |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getFonts` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `bannerId` (deepLink), `pageId` (deepLink), `policyKind` (deepLink), `version` (deepLink) · cold entry: **A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is … |
| Route | `/white-label/typography` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **37 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it.

#### Inputs: what the user enters or picks

**Form: Save fonts** (modal, opened by *Save fonts*; *Save fonts* calls `setFonts`, *Cancel* sends nothing)

**Collects what `setFonts` sends before it is called.** Required: `primaryLatin`. Optional: `primaryArabic`, `secondaryLatin`, `secondaryArabic`, `customFontAssetRefs`, `changeScope`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Primary latin `primaryLatin` | text field | required | — | — | — | — | `setFonts` body |
| Primary arabic `primaryArabic` | text field | optional | — | Required when `ar` is among the tenant's languages (audit R163). | — | Required when `ar` is among the tenant's languages (audit R163). A Latin face alone leaves Arabic in a system fallback that will not match. | `setFonts` body |
| Secondary latin `secondaryLatin` | text field | optional | — | — | — | — | `setFonts` body |
| Secondary arabic `secondaryArabic` | text field | optional | — | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). | — | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). | `setFonts` body |
| Custom font images `customFontAssetRefs` | media picker (several) | optional | — | — | PNG, JPG, SVG or MP4 from the media library | Uploaded font files, as `MediaAsset` ids. | `setFonts` body |

Errors to draw in the form: 400 `ar` is among the tenant's languages and `primaryArabic` is not set, or `secondaryLatin` is set without `secondaryArabic` (audit R163)

**Form: Save theme** (modal, opened by *Save theme*; *Save theme* calls `setTheme`, *Cancel* sends nothing)

**Collects what `setTheme` sends before it is called.** Required: `primaryColour`, `secondaryColour`, `backgroundColour`, `textColour`. Optional: `accentColour`, `darkMode`, `cornerRadius`, `surfaceStyle` (glass or solid, default glass) and `buttonStyle` (solid, outline or pill, default solid; decided 29 September, rev 3 CFG-3). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Primary colour `primaryColour` | colour picker | required | — | — | #RRGGBB | — | `setTheme` body |
| Secondary colour `secondaryColour` | colour picker | required | — | — | #RRGGBB | — | `setTheme` body |
| Accent colour `accentColour` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Background colour `backgroundColour` | colour picker | required | — | — | #RRGGBB | — | `setTheme` body |
| Text colour `textColour` | colour picker | required | — | — | #RRGGBB | — | `setTheme` body |
| Dark mode `darkMode` | group | optional | — | — | — | Optional dark variant. Derived from the light theme when absent. | `setTheme` body |
| Primary colour `darkMode.primaryColour` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Background colour `darkMode.backgroundColour` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text colour `darkMode.textColour` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Corner radius `cornerRadius` | stepper or slider | optional | — | min 0; max 32 | — | The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). | `setTheme` body |
| Surface style `surfaceStyle` | segmented control | optional | Glass | Glass · Solid | — | Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3). | `setTheme` body |
| Button style `buttonStyle` | segmented control | optional | Solid | Solid · Outline · Pill | — | Button shape (decided 29 September, rev 3 CFG-3). | `setTheme` body |
| Component colours `componentColours` | group | optional | — | — | — | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. | `setTheme` body |
| Primary CTA `componentColours.primaryCta` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.primaryCta.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.primaryCta.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Pay button `componentColours.payButton` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.payButton.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.payButton.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Add to cart `componentColours.addToCart` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.addToCart.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.addToCart.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Buy tickets button `componentColours.buyTicketsButton` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.buyTicketsButton.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.buyTicketsButton.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Link `componentColours.link` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.link.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.link.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Badge `componentColours.badge` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.badge.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.badge.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |

Errors to draw in the form: 400 A colour pair fails the contrast requirement. (ContrastProblem)

#### Outputs: what the screen shows and produces

**Shown**

**The font config** (detail panel, from `getFonts`)

| Shows | Format | Notes |
|---|---|---|
| Primary latin | text | — |
| Primary arabic | text | Required when `ar` is among the tenant's languages (audit R163). A Latin face alone leaves Arabic in a system fallback that will not match. |
| Secondary latin | text | — |
| Secondary arabic | text | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). |
| Custom font images | list or chips (count when long) | Uploaded font files, as `MediaAsset` ids. |
| Change scope | chip: Runtime, Build time | Custom font files are `buildTime`; selecting a bundled face is `runtime`. |

**The theme** (detail panel, from `getTheme`)

| Shows | Format | Notes |
|---|---|---|
| Primary colour | colour swatch | — |
| Secondary colour | colour swatch | — |
| Accent colour | colour swatch | — |
| Background colour | colour swatch | — |
| Text colour | colour swatch | — |
| Dark mode | grouped details | Optional dark variant. Derived from the light theme when absent. |
| Corner radius | 1,234 | The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). |
| Surface style | chip: Glass, Solid | Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3). |
| Button style | chip: Solid, Outline, Pill | Button shape (decided 29 September, rev 3 CFG-3). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save fonts (primary button) | `setFonts` PUT `/tenant-config/fonts` | FontConfig | FontConfig | 400 `ar` is among the tenant's languages and `primaryArabic` is not set, or `secondaryLatin` is set without `secondaryArabic` (audit R163) | opens modal first |
| Save theme (secondary button) | `setTheme` PUT `/tenant-config/theme` | Theme | Theme | 400 A colour pair fails the contrast requirement. (ContrastProblem) | opens modal first |

**Data it reads**: `getFonts` (onLoad, Read font configuration); `getTheme` (onLoad, Read colour theme)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-004` Logo & Assets: *Logo & Assets*
- → `CMS-006` Component Preview: *Component Preview*; carries `bannerId`, `pageId`, `policyKind`, `version`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The typography, read by `getFonts`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the typography untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No typography yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getFonts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A colour pair fails the contrast requirement. (ContrastProblem); 400 `ar` is among the tenant's languages and `primaryArabic` is not set, or `secondaryLatin` is set without `secondaryArabic` (audit R163) |

#### Permissions

- `getFonts` → `TENANT_CONFIGURE` (configure) · staff
- `getTheme` → `TENANT_CONFIGURE` (configure) · staff
- `setFonts` → `TENANT_CONFIGURE` (configure) · staff
- `setTheme` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getFonts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.5 | Font Management - System shall support configurable fonts. | Guest Mobile App & Branding | CONTRACTED | `setFonts` |
| 19.1.4 | Color Theme Management - System shall support configurable color palettes. | Guest Mobile App & Branding | CONTRACTED | `setTheme` |
| 2.6.50 | System shall allow administrators to upload brand assets, logos, colors, fonts, content, images, and documents, and use AI to generate a white-label website layout including homepage, menus, headers … | Ticketing Sales | CONTRACTED | `setTheme` |
| 22.4.6 | Multi-Brand Support | Marketing & CRM | CONTRACTED | `setTheme` |
| 2.6.4 | The system should offer white label e-commerce engine for B2C sales (internal CMS). The interface of e-commerce engine should have configurable theming: - Color scheme can be updated - Background … | Ticketing Sales | CONTRACTED | data `Theme` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- CMS manages multiple sites/venues: branding, colour palette including custom hex codes, fonts, Google Analytics site IDs, production/staging environments. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-393)*
- Font and image upload guardrails: size/format restrictions and pixel limits (e.g. banner image ≤ 1024px), validated on upload with an explanatory note to the tenant admin, so cursive/bold fonts cannot overflow banners or descriptions. *(agreed · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-188)*
- Guest-app builder: tenant uploads client logo (multiple formats), picks colour themes, app icon and custom font, with a live preview before publishing. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-187)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Primary colour (`theme.primaryColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | the brand colour (the `accentSolid` token): primary buttons (Book, Continue, Add to cart, Pay), the active step of the step indicator, selected date and time chips, focus rings |
| Secondary colour (`theme.secondaryColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | secondary buttons and secondary emphasis: unselected chips, secondary tabs |
| Accent colour (`theme.accentColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | highlights: badges (LIMITED, NEW, BESTSELLER), availability counts, sale prices |
| Background colour (`theme.backgroundColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | the page background behind every screen (the `ground` token) |
| Text colour (`theme.textColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | body text on the background |
| Dark mode (`theme.darkMode`) | — | — | every guest screen (web, app and kiosk) | the dark variant on a device in dark mode (mobile app); derived from the light theme when absent |
| Dark mode: primary colour (`theme.darkMode.primaryColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Dark mode: background colour (`theme.darkMode.backgroundColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Dark mode: text colour (`theme.darkMode.textColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Corner radius (`theme.cornerRadius`) | min 0; max 32 | — | every guest screen (web, app and kiosk) | the corners of cards, buttons, inputs, sheets and the cart (0 square to 22 the prototype's roundest) |
| Surface style (`theme.surfaceStyle`) | Glass · Solid | Glass | every guest screen (web, app and kiosk) | cards and panels: frosted glass (default) or opaque (the `surfaceRaised` token) |
| Button style (`theme.buttonStyle`) | Solid · Outline · Pill | Solid | every guest screen (web, app and kiosk) | every button's shape: solid fill, outline, or pill |
| Component colours (`theme.componentColours`) | — | — | every guest screen (web, app and kiosk) | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. |
| Component colours: primary CTA (`theme.componentColours.primaryCta`) | — | — | every guest screen (web, app and kiosk) | the one main call to action on each screen, when it should differ from the brand colour |
| Primary CTA: background (`theme.componentColours.primaryCta.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Primary CTA: text (`theme.componentColours.primaryCta.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: pay button (`theme.componentColours.payButton`) | — | — | every guest screen (web, app and kiosk) | the Pay button at checkout |
| Pay button: background (`theme.componentColours.payButton.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Pay button: text (`theme.componentColours.payButton.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: add to cart (`theme.componentColours.addToCart`) | — | — | every guest screen (web, app and kiosk) | every Add to cart button |
| Add to cart: background (`theme.componentColours.addToCart.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Add to cart: text (`theme.componentColours.addToCart.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: buy tickets button (`theme.componentColours.buyTicketsButton`) | — | — | every guest screen (web, app and kiosk) | the persistent Buy tickets button (mobile tab bar) |
| Buy tickets button: background (`theme.componentColours.buyTicketsButton.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Buy tickets button: text (`theme.componentColours.buyTicketsButton.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: link (`theme.componentColours.link`) | — | — | every guest screen (web, app and kiosk) | text links |
| Link: background (`theme.componentColours.link.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Link: text (`theme.componentColours.link.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: badge (`theme.componentColours.badge`) | — | — | every guest screen (web, app and kiosk) | badges on cards (LIMITED, NEW, 11 left) |
| Badge: background (`theme.componentColours.badge.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Badge: text (`theme.componentColours.badge.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Primary latin (`fonts.primaryLatin`) | — | — | every guest screen (web, app and kiosk) | headings and body text in English |
| Primary arabic (`fonts.primaryArabic`) | Required when `ar` is among the tenant's languages (audit R163). | — | every guest screen (web, app and kiosk) | headings and body text in Arabic |
| Secondary latin (`fonts.secondaryLatin`) | — | — | every guest screen (web, app and kiosk) | the secondary face (eyebrows, numbers) in English |
| Secondary arabic (`fonts.secondaryArabic`) | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). | — | every guest screen (web, app and kiosk) | the secondary face in Arabic |
| Custom font images (`fonts.customFontAssetRefs`) | PNG, JPG, SVG or MP4 from the media library | — | every guest screen (web, app and kiosk) | Uploaded font files, as `MediaAsset` ids. |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-003` · status **notStarted** · provenance generated
- Flow F102 *A brand is set, previewed, published and rolled back*, step 2: Typography. → 2 operations, 2 of them previously unwalked.

#### Acceptance for the design

- [ ] Every input above is drawn (36), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-003?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save fonts, Save theme.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-004`, `CMS-006`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-004` Logo & Assets

**Hold the marks every surface needs, at the sizes it needs them, and the mobile app's intro video (Site Builder steps 5 and 6).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `core` module |
| Block | Block A · ticket #18102 (APP-WL-CMS-004) |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getBrandIdentity` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/white-label/logo-assets` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Rewired 23 September (L7).** The screen called the maintenance equipment register, guest CRM or subscription billing where its purpose names White Labelling. Its operations now match its purpose.

#### Inputs: what the user enters or picks

**Form: Save app icons** (modal, opened by *Save app icons*; *Save app icons* calls `setAppIcons`, *Cancel* sends nothing)

**Collects what `setAppIcons` sends before it is called.** Required: `sourceAssetRef`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Source image `sourceAssetRef` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The `MediaAsset` id of the 1024×1024 source, from `assets` `createUpload` then `completeUpload`. | `setAppIcons` body |

Errors to draw in the form: 400 Source is not 1024×1024, or contains transparency

**Form: Save brand identity** (modal, opened by *Save brand identity*; *Save brand identity* calls `setBrandIdentity`, *Cancel* sends nothing)

**Collects what `setBrandIdentity` sends before it is called.** Required: `logoAssetRef`. Optional: `logoVariant` (light, dark or duotone: which lockup sits in the nav bar and which colour reading of it drives the theme, decided 29 September, rev 3 CFG-4), `logoDarkAssetRef`, `faviconAssetRef`, `splashImageAssetRefs`, `splashDurationSeconds`, `splashBackgroundColour`, `showLoadingIndicator`, `splashChangeScope`, `introVideoAssetRef` and `introVideoMode` (off, first launch or every launch; MOB-5). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Logo `logoAssetRef` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The primary logo. | `setBrandIdentity` body |
| Logo dark image `logoDarkAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | Used on dark backgrounds. Falls back to the primary logo. | `setBrandIdentity` body |
| Logo variant `logoVariant` | segmented control | optional | Light | Light · Dark · Duotone | — | Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4). | `setBrandIdentity` body |
| Favicon `faviconAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The browser tab icon for the guest web app. | `setBrandIdentity` body |
| Splash image `splashImageAssetRefs` | media picker (several) | optional | — | — | PNG, JPG, SVG or MP4 from the media library | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). | `setBrandIdentity` body |
| Splash duration seconds `splashDurationSeconds` | stepper or slider (seconds) | optional | 3 | min 0; max 10 | — | — | `setBrandIdentity` body |
| Splash background colour `splashBackgroundColour` | colour picker | optional | — | — | #RRGGBB | — | `setBrandIdentity` body |
| Show loading indicator `showLoadingIndicator` | toggle | optional | on | — | — | — | `setBrandIdentity` body |
| Intro video `introVideoAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). | `setBrandIdentity` body |
| Intro video mode `introVideoMode` | segmented control | optional | Off | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | — | When GST-001 plays it full screen. "Skip introduction" is always shown. | `setBrandIdentity` body |

Errors to draw in the form: 400 An asset is larger than 2 MB, or is not PNG or SVG (audit R270)

#### Outputs: what the screen shows and produces

**Shown**

**The brand identity** (detail panel, from `getBrandIdentity`): **Intro video (decided 29 September, MOB-5).** Picked from the media library (CMS-010); plays off, on first launch or on every launch, always with Skip introduction. Streamed, so it needs no app build, unlike the splash and icons.

| Shows | Format | Notes |
|---|---|---|
| Logo | the image or video | The primary logo. |
| Logo dark image | the image or video | Used on dark backgrounds. Falls back to the primary logo. |
| Logo variant | chip: Light, Dark, Duotone | Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4). |
| Favicon | the image or video | The browser tab icon for the guest web app. |
| Splash image | list or chips (count when long) | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish … |
| Splash duration seconds | 1,234 | — |
| Splash background colour | colour swatch | — |
| Show loading indicator | yes / no (icon or chip) | — |
| Splash change scope | chip: Runtime, Build time | Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163). |
| Intro video | the image or video | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode | chip: Off, First launch, Every launch | When GST-001 plays it full screen. "Skip introduction" is always shown. |

**The app icons** (detail panel, from `getAppIcons`)

| Shows | Format | Notes |
|---|---|---|
| Source image | the image or video | The `MediaAsset` id of the 1024×1024 source. |
| Derived | list or chips (count when long) | Generated by `setAppIcons` from the source, one entry per platform and size — the iOS and Android store sets and the web favicons listed on … |
| Change scope | chip: Runtime, Build time | Always `buildTime` — icons are baked into the binary. |
| Live version | text | Icon currently shipped. Differs from the draft until the next release. |
| Requires rebuild | yes / no (icon or chip) | True while the draft's source differs from the icon in `liveVersion`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save app icons (primary button) | `setAppIcons` PUT `/tenant-config/app-icons` | inline | AppIcons | 400 Source is not 1024×1024, or contains transparency | opens modal first |
| Save brand identity (secondary button) | `setBrandIdentity` PUT `/tenant-config/brand` | BrandIdentity | BrandIdentity | 400 An asset is larger than 2 MB, or is not PNG or SVG (audit R270) | opens modal first |

**Data it reads**: `getBrandIdentity` (onLoad, The logo, favicon and splash in use); `getAppIcons` (onLoad, The app icon set at every size)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The logo assets, read by `getBrandIdentity`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the logo assets untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No logo assets yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getBrandIdentity` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 An asset is larger than 2 MB, or is not PNG or SVG (audit R270); 400 Source is not 1024×1024, or contains transparency |

#### Permissions

- `getBrandIdentity` → `TENANT_CONFIGURE` (configure) · staff
- `getAppIcons` → `TENANT_CONFIGURE` (configure) · staff
- `setAppIcons` → `TENANT_CONFIGURE` (configure) · staff
- `setBrandIdentity` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getBrandIdentity` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.3 | App Icon Management - System shall support configurable app icons. | Guest Mobile App & Branding | CONTRACTED | `setAppIcons` |
| 19.1.1 | Logo Management - System shall allow changing the mobile app logo through configuration. | Guest Mobile App & Branding | CONTRACTED | `setBrandIdentity` |
| 19.1.2 | Splash Screen Management - System shall allow changing splash screens. | Guest Mobile App & Branding | CONTRACTED | `setBrandIdentity` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The tenant picks which logo lockup sits in the nav bar and a logo variant (Light, Dark, Duotone) whose colours drive the theme. *(agreed · design review 29 Sep 2026, CFG-4 · Brand logo + Logo palette (Light/Dark/Duotone) · DI-1068)*
- Font and image upload guardrails: size/format restrictions and pixel limits (e.g. banner image ≤ 1024px), validated on upload with an explanatory note to the tenant admin, so cursive/bold fonts cannot overflow banners or descriptions. *(agreed · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-188)*
- Guest-app builder: tenant uploads client logo (multiple formats), picks colour themes, app icon and custom font, with a live preview before publishing. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-187)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Logo (`brand.logoAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | every guest screen (web, app and kiosk) | the logo in the header or nav bar, the splash and the footer |
| Logo dark image (`brand.logoDarkAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | every guest screen (web, app and kiosk) | the logo on dark backgrounds (falls back to the primary logo) |
| Logo variant (`brand.logoVariant`) | Light · Dark · Duotone | Light | every guest screen (web, app and kiosk) | which logo lockup sits in the nav bar, and whose colours drive the theme |
| Favicon (`brand.faviconAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | every P01 screen | the browser tab icon (website only) |
| Splash image (`brand.splashImageAssetRefs`) | PNG, JPG, SVG or MP4 from the media library | — | every P02 screen | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). |
| Splash duration seconds (`brand.splashDurationSeconds`) | min 0; max 10 | 3 | every guest screen (web, app and kiosk) | — |
| Splash background colour (`brand.splashBackgroundColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Show loading indicator (`brand.showLoadingIndicator`) | — | on | every guest screen (web, app and kiosk) | — |
| Intro video (`brand.introVideoAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | GST-001 | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode (`brand.introVideoMode`) | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | Off | GST-001 | When GST-001 plays it full screen. "Skip introduction" is always shown. |
| Source image (`appIcons.sourceAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | no guest screen: the phone's home screen and the store listing | The `MediaAsset` id of the 1024×1024 source, from `assets` `createUpload` then `completeUpload`. |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-004` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-004?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save app icons, Save brand identity.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-005` Theme Editor

**Tune the theme and watch it apply everywhere at once.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `core` module |
| Block | Block A · ticket #18103 (APP-WL-CMS-005) |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getTheme` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/white-label/theme-editor` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **A failing colour contrast is refused, not warned (decided 28 September, audit R139 (a)).** `setTheme` answers `400` with a `ContrastProblem` naming each failing pair (foreground, background, ratio, the ratio required, where it is used); the theme is not saved, and the editor keeps the entered colours and marks the failing pairs so they can be corrected. There is no save-anyway.

#### Inputs: what the user enters or picks

**Form: Save theme** (modal, opened by *Save theme*; *Save theme* calls `setTheme`, *Cancel* sends nothing)

**Collects what `setTheme` sends before it is called.** Required: `primaryColour`, `secondaryColour`, `backgroundColour`, `textColour`. Optional: `accentColour`, `darkMode`, `cornerRadius`, `surfaceStyle` (glass or solid, default glass) and `buttonStyle` (solid, outline or pill, default solid; decided 29 September, rev 3 CFG-3) and `componentColours` (M17-11). **A colour pair that fails contrast is refused** (`400 ContrastProblem`, decided 28 September, audit R139 (a)): the modal stays open with the failing pairs marked. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Primary colour `primaryColour` | colour picker | required | — | — | #RRGGBB | — | `setTheme` body |
| Secondary colour `secondaryColour` | colour picker | required | — | — | #RRGGBB | — | `setTheme` body |
| Accent colour `accentColour` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Background colour `backgroundColour` | colour picker | required | — | — | #RRGGBB | — | `setTheme` body |
| Text colour `textColour` | colour picker | required | — | — | #RRGGBB | — | `setTheme` body |
| Dark mode `darkMode` | group | optional | — | — | — | Optional dark variant. Derived from the light theme when absent. | `setTheme` body |
| Primary colour `darkMode.primaryColour` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Background colour `darkMode.backgroundColour` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text colour `darkMode.textColour` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Corner radius `cornerRadius` | stepper or slider | optional | — | min 0; max 32 | — | The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). | `setTheme` body |
| Surface style `surfaceStyle` | segmented control | optional | Glass | Glass · Solid | — | Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3). | `setTheme` body |
| Button style `buttonStyle` | segmented control | optional | Solid | Solid · Outline · Pill | — | Button shape (decided 29 September, rev 3 CFG-3). | `setTheme` body |
| Component colours `componentColours` | group | optional | — | — | — | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. | `setTheme` body |
| Primary CTA `componentColours.primaryCta` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.primaryCta.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.primaryCta.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Pay button `componentColours.payButton` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.payButton.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.payButton.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Add to cart `componentColours.addToCart` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.addToCart.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.addToCart.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Buy tickets button `componentColours.buyTicketsButton` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.buyTicketsButton.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.buyTicketsButton.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Link `componentColours.link` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.link.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.link.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Badge `componentColours.badge` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.badge.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.badge.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |

Errors to draw in the form: 400 A colour pair fails the contrast requirement. (ContrastProblem)

#### Outputs: what the screen shows and produces

**Shown**

**The theme** (detail panel, from `getTheme`): **Per-element colours (decided 17 September, M17-11).** Pickers for the main call to action, the pay button, add to cart, the Buy tickets button, links and badges, each with a live contrast warning; left empty they follow the theme. The guest flow itself stays standard.

| Shows | Format | Notes |
|---|---|---|
| Primary colour | colour swatch | — |
| Secondary colour | colour swatch | — |
| Accent colour | colour swatch | — |
| Background colour | colour swatch | — |
| Text colour | colour swatch | — |
| Dark mode | grouped details | Optional dark variant. Derived from the light theme when absent. |
| Corner radius | 1,234 | The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). |
| Surface style | chip: Glass, Solid | Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3). |
| Button style | chip: Solid, Outline, Pill | Button shape (decided 29 September, rev 3 CFG-3). |
| Component colours | grouped details | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. |

**Contrast refused** (banner, from `setTheme`): Shown when `setTheme` answers 400. Lists every failing pair; the theme was not saved (decided 28 September, audit R139 (a)).

| Shows | Format | Notes |
|---|---|---|
| Failures | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save theme (primary button) | `setTheme` PUT `/tenant-config/theme` | Theme | Theme | 400 A colour pair fails the contrast requirement. (ContrastProblem) | opens modal first |

**Data it reads**: `getTheme` (onLoad, Read colour theme)

**Where the user goes next**

- → `CMS-007` Page Builder: *Rearranges the homepage*
- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*
- → `CMS-006` Component Preview: *Component Preview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The theme editor, read by `getTheme`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the theme editor untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No theme editor yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getTheme` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A colour pair fails the contrast requirement. (ContrastProblem) |

#### Permissions

- `getTheme` → `TENANT_CONFIGURE` (configure) · staff
- `setTheme` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getTheme` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.4 | Color Theme Management - System shall support configurable color palettes. | Guest Mobile App & Branding | CONTRACTED | `setTheme` |
| 2.6.50 | System shall allow administrators to upload brand assets, logos, colors, fonts, content, images, and documents, and use AI to generate a white-label website layout including homepage, menus, headers … | Ticketing Sales | CONTRACTED | `setTheme` |
| 22.4.6 | Multi-Brand Support | Marketing & CRM | CONTRACTED | `setTheme` |
| 2.6.4 | The system should offer white label e-commerce engine for B2C sales (internal CMS). The interface of e-commerce engine should have configurable theming: - Color scheme can be updated - Background … | Ticketing Sales | CONTRACTED | data `Theme` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Theme settings: surface style Glass (default) or Solid cards; button style Solid (default), Outline or Pill. *(agreed · design review 29 Sep 2026, CFG-3 · Surfaces (Glass/Solid) and Buttons (Solid/Outline/Pill) · DI-1067)*
- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Per-element colours in the theme editor: pickers for the main call to action, pay button, add to cart, Buy tickets button, links and badges, each with a live contrast warning; left empty they follow the theme. The guest flow itself stays standard. *(agreed · MoM 17 Sep 2026, M17-11 · DI-922)*
- Qossai: white-labelling needs more flexibility, e.g. setting the colour of specific interactive elements such as the "pay now" / "purchase" button independently, not only an overall palette, while the guest experience stays a standardised flow with configurable limits. *(client request · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-918)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*
- CMS manages multiple sites/venues: branding, colour palette including custom hex codes, fonts, Google Analytics site IDs, production/staging environments. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-393)*
- Layout builder: header, footer, logo, bottom-navigation icons and colours are configurable; banner sizing is configurable and promotion blocks are switched on/off by toggle. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-189)*
- Guest-app builder: tenant uploads client logo (multiple formats), picks colour themes, app icon and custom font, with a live preview before publishing. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-187)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Primary colour (`theme.primaryColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | the brand colour (the `accentSolid` token): primary buttons (Book, Continue, Add to cart, Pay), the active step of the step indicator, selected date and time chips, focus rings |
| Secondary colour (`theme.secondaryColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | secondary buttons and secondary emphasis: unselected chips, secondary tabs |
| Accent colour (`theme.accentColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | highlights: badges (LIMITED, NEW, BESTSELLER), availability counts, sale prices |
| Background colour (`theme.backgroundColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | the page background behind every screen (the `ground` token) |
| Text colour (`theme.textColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | body text on the background |
| Dark mode (`theme.darkMode`) | — | — | every guest screen (web, app and kiosk) | the dark variant on a device in dark mode (mobile app); derived from the light theme when absent |
| Dark mode: primary colour (`theme.darkMode.primaryColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Dark mode: background colour (`theme.darkMode.backgroundColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Dark mode: text colour (`theme.darkMode.textColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Corner radius (`theme.cornerRadius`) | min 0; max 32 | — | every guest screen (web, app and kiosk) | the corners of cards, buttons, inputs, sheets and the cart (0 square to 22 the prototype's roundest) |
| Surface style (`theme.surfaceStyle`) | Glass · Solid | Glass | every guest screen (web, app and kiosk) | cards and panels: frosted glass (default) or opaque (the `surfaceRaised` token) |
| Button style (`theme.buttonStyle`) | Solid · Outline · Pill | Solid | every guest screen (web, app and kiosk) | every button's shape: solid fill, outline, or pill |
| Component colours (`theme.componentColours`) | — | — | every guest screen (web, app and kiosk) | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. |
| Component colours: primary CTA (`theme.componentColours.primaryCta`) | — | — | every guest screen (web, app and kiosk) | the one main call to action on each screen, when it should differ from the brand colour |
| Primary CTA: background (`theme.componentColours.primaryCta.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Primary CTA: text (`theme.componentColours.primaryCta.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: pay button (`theme.componentColours.payButton`) | — | — | every guest screen (web, app and kiosk) | the Pay button at checkout |
| Pay button: background (`theme.componentColours.payButton.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Pay button: text (`theme.componentColours.payButton.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: add to cart (`theme.componentColours.addToCart`) | — | — | every guest screen (web, app and kiosk) | every Add to cart button |
| Add to cart: background (`theme.componentColours.addToCart.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Add to cart: text (`theme.componentColours.addToCart.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: buy tickets button (`theme.componentColours.buyTicketsButton`) | — | — | every guest screen (web, app and kiosk) | the persistent Buy tickets button (mobile tab bar) |
| Buy tickets button: background (`theme.componentColours.buyTicketsButton.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Buy tickets button: text (`theme.componentColours.buyTicketsButton.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: link (`theme.componentColours.link`) | — | — | every guest screen (web, app and kiosk) | text links |
| Link: background (`theme.componentColours.link.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Link: text (`theme.componentColours.link.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: badge (`theme.componentColours.badge`) | — | — | every guest screen (web, app and kiosk) | badges on cards (LIMITED, NEW, 11 left) |
| Badge: background (`theme.componentColours.badge.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Badge: text (`theme.componentColours.badge.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-005` · status **notStarted** · provenance generated
- Flow F22 *A tenant rebrands their app*, step 2: Sets the colour theme → **Contrast checked and enforced**: a colour pair that fails 4.5:1 is refused by `setTheme` (`400 ContrastProblem`), because a brand colour that fails it is inaccessible (decided 28 September, audit …
- Flow F22 branch at step 2 (recoverable): when The brand colour fails contrast, **Refused, not warned** (decided 28 September, audit R139 (a)). `setTheme` answers `400 ContrastProblem` naming the failing pair, and the tenant picks a shade that passes 4.5:1. Nothing inaccessible …

#### Acceptance for the design

- [ ] Every input above is drawn (31), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-005?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save theme.
- [ ] Every transition is wired: `CMS-007`, `CMS-001`, `CMS-002`, `CMS-003`, `CMS-006`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 9 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-006` Component Preview

**Check the theme against the components that carry it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `core` module |
| Block | Block A · ticket #18119 (APP-WL-CMS-006) |
| Who uses it | venue staff holding `TENANT_CONFIGURE`, `TENANT_PUBLISH` (2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listConfigVersions` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `bannerId` (deepLink), `pageId` (deepLink), `policyKind` (deepLink), `version` (deepLink) · cold entry: **A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is … |
| Route | `/white-label/component-preview` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **36 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it.

#### Inputs: what the user enters or picks

**Form: Create preview** (modal, opened by *Create preview*; *Create preview* calls `createPreview`, *Cancel* sends nothing)

**Collects what `createPreview` sends before it is called.** Nothing in the body is required. Optional: `platform`, `theme`, `language`, `expiresInHours`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Platform `platform` | segmented control | optional | — | Ios · Android · Web | — | — | `createPreview` body |
| Theme `theme` | segmented control | optional | — | Light · Dark | — | — | `createPreview` body |
| Language `language` | language picker | optional | — | — | ISO 639-1 code, shown as the language name | — | `createPreview` body |
| Expires in hours `expiresInHours` | number field (hours) | optional | 24 | min 1; max 168 | — | — | `createPreview` body |

**Form: Publish tenant config** (modal, opened by *Publish tenant config*; *Publish tenant config* calls `publishTenantConfig`, *Cancel* sends nothing)

**Collects what `publishTenantConfig` sends before it is called.** Required: `note`. Optional: `scheduledFor`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Note `note` | text area | required | — | min length 3; max length 500 | — | — | `publishTenantConfig` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Publish at a future time. Useful for a campaign launch. | `publishTenantConfig` body |

Errors to draw in the form: 409 Validation failed. (ConfigValidationProblem)

#### Outputs: what the screen shows and produces

**Shown**

**Every config version** (data table, from `listConfigVersions`)

| Shows | Format | Notes |
|---|---|---|
| Published at | 1 Oct 2026, 14:30 | — |
| Published by principal | the name it points at, never the id | — |
| Published by name | text | — |
| Note | text | — |
| Is current | yes / no (icon or chip) | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Content hash | text | — |
| Pending build time changes | list or chips (count when long) | Changes in this version that will not reach guests until the next store release. |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**The selected config version** (detail panel, from `listConfigVersions`)

| Shows | Format | Notes |
|---|---|---|
| Published at | 1 Oct 2026, 14:30 | — |
| Published by principal | the name it points at, never the id | — |
| Published by name | text | — |
| Note | text | — |
| Is current | yes / no (icon or chip) | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Content hash | text | — |
| Pending build time changes | list or chips (count when long) | Changes in this version that will not reach guests until the next store release. |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Create preview (primary button) | `createPreview` POST `/tenant-config/preview` | inline | Preview | — | opens modal first |
| Diff config version (secondary button) | `diffConfigVersion` GET `/tenant-config/versions/{version}/diff` | — | ConfigDiff | — | — |
| Publish tenant config (secondary button) | `publishTenantConfig` POST `/tenant-config/publish` | inline | ConfigVersion | 409 Validation failed. (ConfigValidationProblem) | opens modal first |
| Restore config version (secondary button) | `restoreConfigVersion` POST `/tenant-config/versions/{version}/restore` | — | TenantConfig | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listConfigVersions` (onLoad, Version history)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*; carries `bannerId`, `pageId`, `policyKind`, `version`
- → `ADM-016` White-Label Branding Management: *White-Label Branding Management*; carries `bannerId`, `pageId`, `policyKind`, `version`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The component preview list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the component preview untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No component preview yet. Offers Create preview (`createPreview`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listConfigVersions` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `listConfigVersions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Validation failed. (ConfigValidationProblem) |

#### Permissions

- `createPreview` → `TENANT_CONFIGURE` (configure) · staff
- `diffConfigVersion` → `TENANT_CONFIGURE` (configure) · staff
- `listConfigVersions` → `TENANT_CONFIGURE` (configure) · staff
- `publishTenantConfig` → `TENANT_PUBLISH` (configure) · staff
- `restoreConfigVersion` → `TENANT_PUBLISH` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `listConfigVersions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.10.30 | CMS Audit Trail | Marketing & CRM | CONTRACTED | `listConfigVersions` |
| 19.1.24 | White Label Configuration Portal - System shall provide self-service white label configuration. | Guest Mobile App & Branding | CONTRACTED | `publishTenantConfig` |
| 22.10.10 | Version Management | Marketing & CRM | CONTRACTED | `restoreConfigVersion` |
| 22.10.11 | Rollback & Recovery | Marketing & CRM | CONTRACTED | `restoreConfigVersion` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Qossai: white-labelling needs more flexibility, e.g. setting the colour of specific interactive elements such as the "pay now" / "purchase" button independently, not only an overall palette, while the guest experience stays a standardised flow with configurable limits. *(client request · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-918)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Reusable page components per venue type are to be documented (e.g. seat-map component for stadiums/amphitheatres, park-map component for attraction venues) so one layout serves many venues with only imagery/data swapped. Documentation pending from Allam. *(open · MoM 20 Aug 2026, 4.10 CMS & White-Label; 6. Open Items · DI-395)*
- Guest-app builder: tenant uploads client logo (multiple formats), picks colour themes, app icon and custom font, with a live preview before publishing. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-187)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-006` · status **notStarted** · provenance generated
- Flow F102 *A brand is set, previewed, published and rolled back*, step 3: Component Preview. → 2 operations, 2 of them previously unwalked.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-006?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Create preview, Diff config version, Publish tenant config, Restore config version, What publishing changes.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`, `ADM-016`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`, `TENANT_PUBLISH`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-007` Page Builder

**Assemble a storefront page from blocks the tenant cannot break.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `core` module |
| Block | Block A · ticket #18104 (APP-WL-CMS-007) |
| Who uses it | venue staff holding `AI_USE`, `TENANT_CONFIGURE` (1 operate, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getHomepageLayout` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `pageId` (navigation), `actionId` (navigation) |
| Route | `/white-label/page-builder` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **A section whose module is off is disabled in the builder (decided 28 September, audit R163 (4)).** The builder reads `getModuleEnablement` and applies the mapping on `HomepageSectionKind`: `tickets` needs `ticketsAndBooking`, `whatsOn` needs `events`, `attractions` needs `attractions`, `membership` needs `membership`, `dining` needs `diningAndFnb`, `shop` needs `shop`, `map` needs `map`; `heroBanner`, `quickActions`, `promotions`, `customContent` and `spacer` need none. A section whose module is off cannot be added or made visible, and says which module to switch on (on CMS-001). `setHomepageLayout` refuses such a section with 400 in any case.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | segmented control | — | Draft · Published · Archived | `listContentPages` ?status |
| Category code | text field | — | — | `listContentPages` ?categoryCode |
| Slug | text field | — | pattern `^[a-z0-9-]+$` | `listContentPages` ?slug |

**Form: Create content page** (modal, opened by *Create content page*; *Create content page* calls `createContentPage`, *Cancel* sends nothing)

**Collects what `createContentPage` sends before it is called.** Required: `id`, `slug`, `title`, `body`, `status`. Optional: `isEnabled`, `iconAssetRef`, `categoryCode`, `sortOrder`, `isReferenced`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Slug `slug` | text field | required | — | pattern `^[a-z0-9-]+$` | — | — | `createContentPage` body |
| Title `title` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createContentPage` body |
| Body `body` | rich text, one per language | required | — | — | English and Arabic (Arabic right to left) | Keyed by language code. Values are sanitised HTML. | `createContentPage` body |
| Is enabled `isEnabled` | toggle | optional | on | — | — | BL-005. Enablement is not publication. | `createContentPage` body |
| Icon `iconAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `createContentPage` body |
| Category code `categoryCode` | text field | optional | — | — | — | — | `createContentPage` body |
| Sort order `sortOrder` | number field | optional | — | — | — | — | `createContentPage` body |

Errors to draw in the form: 409 Slug already in use

**Form: Save content page** (modal, opened by *Save content page*; *Save content page* calls `updateContentPage`, *Cancel* sends nothing)

**Collects what `updateContentPage` sends before it is called.** Required: `slug`, `title`, `body`. Optional: `isEnabled`, `iconAssetRef`, `categoryCode`, `sortOrder`, `status`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Slug `slug` | text field | required | — | pattern `^[a-z0-9-]+$` | — | — | `updateContentPage` body |
| Title `title` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `updateContentPage` body |
| Body `body` | rich text, one per language | required | — | — | English and Arabic (Arabic right to left) | Keyed by language code. Values are sanitised HTML. | `updateContentPage` body |
| Is enabled `isEnabled` | toggle | optional | on | — | — | — | `updateContentPage` body |
| Icon `iconAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `updateContentPage` body |
| Category code `categoryCode` | text field | optional | — | — | — | — | `updateContentPage` body |
| Sort order `sortOrder` | number field | optional | — | — | — | — | `updateContentPage` body |
| Status `status` | segmented control | optional | — | Draft · Published · Archived | — | Only `archived` is taken — send it to withdraw a published page or abandon a draft (`states/content.yaml`). | `updateContentPage` body |

Errors to draw in the form: 409 The page is `published` and the body changes more than its status to `archived` (audit R163).

**Form: Save footer** (modal, opened by *Save footer*; *Save footer* calls `setFooter`, *Cancel* sends nothing)

**Collects what `setFooter` sends before it is called.** Required: `id`, `scopePath`. Optional: `columns`, `legalLinks`, `copyrightText`, `socialLinks`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Columns `columns` | repeatable rows | optional | — | — | — | — | `setFooter` body |
| Heading `columns[].heading` | text field | optional | — | — | — | — | `setFooter` body |
| Links `columns[].links` | repeatable rows | optional | — | — | — | — | `setFooter` body |
| Label `columns[].links[].label` | text field | optional | — | — | — | — | `setFooter` body |
| URL `columns[].links[].url` | text field | optional | — | — | — | — | `setFooter` body |
| Opens cookie preferences `columns[].links[].opensCookiePreferences` | toggle | optional | off | — | — | — | `setFooter` body |
| Legal links `legalLinks` | group | optional | — | — | — | Required links, held separately from the free-form columns — a tenant reorganising their footer must not be able to remove the privacy notice by accident. | `setFooter` body |
| Terms URL `legalLinks.termsUrl` | text field | optional | — | — | — | — | `setFooter` body |
| Privacy URL `legalLinks.privacyUrl` | text field | optional | — | — | — | — | `setFooter` body |
| Accessibility URL `legalLinks.accessibilityUrl` | text field | optional | — | — | — | — | `setFooter` body |
| Cookie policy URL `legalLinks.cookiePolicyUrl` | text field | optional | — | — | — | — | `setFooter` body |
| Copyright text `copyrightText` | text field | optional | — | — | — | — | `setFooter` body |
| Social links `socialLinks` | repeatable rows | optional | — | — | — | — | `setFooter` body |
| Platform `socialLinks[].platform` | text field | optional | — | — | — | — | `setFooter` body |
| URL `socialLinks[].url` | text field | optional | — | — | — | — | `setFooter` body |

**Form: Save homepage layout** (modal, opened by *Save homepage layout*; *Save homepage layout* calls `setHomepageLayout`, *Cancel* sends nothing)

**Collects what `setHomepageLayout` sends before it is called.** Required: `sections`. Optional: `id`. A section whose module is off is disabled here and cannot be made visible (audit R163 (4)). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Sections `sections` | repeatable rows | required | — | — | — | — | `setHomepageLayout` body |
| Kind `sections[].kind` | select | required | — | Hero banner · Quick actions · Tickets · Whats on · Attractions · Membership · Dining · Shop · Promotions · Map · Custom content · Venue overview …; `tickets` needs `ticketsAndBooking`; `whatsOn` needs `events`; `attractions` needs `attractions`; `membership` … | — | Which module each section needs, proposed, client to correct (decided 28 September, audit R163). | `setHomepageLayout` body |
| Title `sections[].title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setHomepageLayout` body |
| Sort order `sections[].sortOrder` | number field | required | — | — | — | — | `setHomepageLayout` body |
| Is visible `sections[].isVisible` | toggle | required | — | — | — | — | `setHomepageLayout` body |
| Content page `sections[].contentPageId` | picker: choose a content page | optional | — | — | shows names, sends the id | — | `setHomepageLayout` body |
| Max items `sections[].maxItems` | number field | optional | — | — | — | How many items the section shows. On the mobile Home, `attractions`, `dining`, `whatsOn` and `shop` show 1 or 2 highlights (decided 29 September, MOB-3). | `setHomepageLayout` body |
| Hero style `sections[].heroStyle` | radio group | optional | — | Carousel · Video · Poster · Split | — | For `heroBanner` only (decided 29 September, MOB-3). | `setHomepageLayout` body |

Errors to draw in the form: 400 A section references a disabled module or a missing content block

#### Outputs: what the screen shows and produces

**Shown**

**The homepage layout** (detail panel, from `getHomepageLayout`): **Also the mobile Home editor (decided 29 September, MOB-3; Site Builder steps 5 and 6).** The `venueOverview` section (description, opening hours, type tiles), the hero's style (carousel, video, poster or split) and 1 or 2 highlights for attractions, dining, what's on and shop (`maxItems`). The header and footer are set here too (`setHeader`, `setFooter`).

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Sections | list or chips (count when long) | — |

**Modules the sections need** (detail panel, from `getModuleEnablement`): A section whose module is off (mapping on `HomepageSectionKind`) is shown disabled and cannot be added or made visible (decided 28 September, audit R163 (4)).

| Shows | Format | Notes |
|---|---|---|
| Module key | chip: Tickets and booking, Membership, Events, Attractions, Virtual queue, Dining and fnb… | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not … |
| Display name | text | — |
| Is enabled | yes / no (icon or chip) | — |

**Every content page** (data table, from `listContentPages`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Slug | text | — |
| Title | in the reader's language | — |
| Body | in the reader's language | Keyed by language code. Values are sanitised HTML. |
| Is enabled | yes / no (icon or chip) | BL-005. Enablement is not publication. |
| Status | chip: Draft, Published, Archived | Created as `draft`, published by `publishTenantConfig`, archived through `updateContentPage` (`states/content.yaml`). |
| Icon | the image or video | — |
| Category code | text | — |
| Sort order | 1,234 | — |
| Is referenced | yes / no (icon or chip) | True when navigation or the homepage links to this page. Blocks deletion. |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save homepage layout (primary button) | `setHomepageLayout` PUT `/tenant-config/homepage` | HomepageLayout | HomepageLayout | 400 A section references a disabled module or a missing content block | opens modal first |
| Create content page (secondary button) | `createContentPage` POST `/tenant-config/pages` | ContentPage | ContentPage | 409 Slug already in use | opens modal first |
| Save content page (secondary button) | `updateContentPage` PUT `/tenant-config/pages/{pageId}` | UpdateContentPageRequest | ContentPage | 409 The page is `published` and the body changes more than its status to `archived` (audit R163). | opens modal first |
| Save footer (secondary button) | `setFooter` PUT `/footer` | FooterConfig | FooterConfig | — | opens modal first |

**Data it reads**: `listContentPages` (onLoad, The guest app's content pages); `getHomepageLayout` (onLoad, Read homepage layout); `getModuleEnablement` (onLoad, Which modules are on, so a section whose module is off is …)

**Where the user goes next**

- → `CMS-012` RTL Preview: *Previews in both directions*
- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*; carries `pageId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The record, read by `getHomepageLayout`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the record untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No record yet. Offers Create content page (`createContentPage`). |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `listContentPages` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A section references a disabled module or a missing content block; 409 Drafting is not allowed at this scope now: the capability is paused (`capability-paused`) or governance blocks it (`governance-blocked`, naming the policy and …; 409 Page is referenced by navigation or the homepage; 409 Slug already in use |

#### Permissions

- `listContentPages` → `TENANT_CONFIGURE` (configure) · staff, guest
- `createContentPage` → `TENANT_CONFIGURE` (configure) · staff
- `updateContentPage` → `TENANT_CONFIGURE` (configure) · staff
- `setFooter` → `TENANT_CONFIGURE` (configure) · staff
- `getHomepageLayout` → `TENANT_CONFIGURE` (configure) · staff
- `setHomepageLayout` → `TENANT_CONFIGURE` (configure) · staff
- `getModuleEnablement` → `TENANT_CONFIGURE` (configure) · staff
- `setHeader` → `TENANT_CONFIGURE` (configure) · staff
- `deleteContentPage` → `TENANT_CONFIGURE` (configure) · staff
- `proposeMarketingContent` → `AI_USE` (operate) · staff
- `decideProposedAction` → `AI_USE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `listContentPages` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.20 | Tenant-Specific Content - System shall support tenant-specific content. | Guest Mobile App & Branding | CONTRACTED | `listContentPages` |
| 2.6.19 | - General information for Guests | Ticketing Sales | CONTRACTED | `listContentPages` |
| 19.1.15 | Custom Content Pages - System shall support custom content pages. | Guest Mobile App & Branding | CONTRACTED | `createContentPage` |
| 19.1.9 | Homepage Layout Management - System shall support configurable homepage layouts. | Guest Mobile App & Branding | CONTRACTED | `setHomepageLayout` |
| 19.1.6 | Header Configuration - System shall support configurable headers. | Guest Mobile App & Branding | CONTRACTED | `setHeader` |
| 22.3.18 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.9 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.10 | AI Subject Line Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.9.17 | AI Language Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.14 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.16 | AI Website Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.17 | AI Mobile App Content Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The hero banner and marketing layer (images, video, search, browse-by-venue, venue info) is optional and toggled in the white-label builder: on for clients without their own marketing site (Qossai: roughly 30%), off for a lean direct-to-ticket flow. *(agreed · MoM 18 Sep 2026, 4.11 Guest Website UX Review — Page Structure & Hero Banner Flexibility · DI-945)*
- Decision (raised by Qossai): the CMS/website builder supports two modes per client using the same builder — a full landing page plus integrated ticket-sale flow (clients without a website), or B2C-only (header, product cards, footer, checkout) embedded in/linked from an existing site. *(agreed · MoM 21 Aug 2026, 4.9 Website Builder Flexibility — Standalone vs. B2C-Only Configuration · DI-431)*
- Drag-and-drop page builder with a standardised layout (header, footer, hero/card components) that adapts to product type — seat map for seated products, standard flow for general admission. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-394)*
- Custom content pages per venue (e.g. "Plan Your Visit", Accessibility) that follow accessibility guidelines. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-190)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Header layout (`header.layout`) | Logo left · Logo centre · Logo with menu | — | every guest screen (web, app and kiosk) | the header: logo left, logo centred, or logo with the menu |
| Show logo (`header.showLogo`) | — | on | every guest screen (web, app and kiosk) | — |
| Show menu (`header.showMenu`) | — | on | every guest screen (web, app and kiosk) | — |
| Show notifications (`header.showNotifications`) | — | on | every guest screen (web, app and kiosk) | — |
| Background colour (`header.backgroundColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Footer columns (`footer.columns`) | — | — | every website screen | — |
| Columns: heading (`footer.columns[].heading`) | — | — | every website screen | — |
| Columns: links (`footer.columns[].links`) | — | — | every website screen | — |
| Links: label (`footer.columns[].links[].label`) | — | — | every website screen | — |
| Links: uRL (`footer.columns[].links[].url`) | — | — | every website screen | — |
| Links: opens cookie preferences (`footer.columns[].links[].opensCookiePreferences`) | — | off | every website screen | — |
| Legal links (`footer.legalLinks`) | — | — | every website screen | Required links, held separately from the free-form columns — a tenant reorganising their footer must not be able to remove the privacy notice by accident. |
| Legal links: terms URL (`footer.legalLinks.termsUrl`) | — | — | every website screen | — |
| Legal links: privacy URL (`footer.legalLinks.privacyUrl`) | — | — | every website screen | — |
| Legal links: accessibility URL (`footer.legalLinks.accessibilityUrl`) | — | — | every website screen | — |
| Legal links: cookie policy URL (`footer.legalLinks.cookiePolicyUrl`) | — | — | every website screen | — |
| Copyright text (`footer.copyrightText`) | — | — | every website screen | — |
| Social links (`footer.socialLinks`) | — | — | every website screen | — |
| Social links: platform (`footer.socialLinks[].platform`) | — | — | GST-018, GST-066, GST-073, WEB-011, WEB-017, WEB-018, WEB-024, WEB-027 | — |
| Social links: uRL (`footer.socialLinks[].url`) | — | — | every website screen | — |
| Sections (`homepage.sections`) | — | — | the guest home screens | — |
| Sections: kind (`homepage.sections[].kind`) | Hero banner · Quick actions · Tickets · Whats on · Attractions · Membership · Dining · Shop · Promotions · Map · Custom content · Venue overview …; `tickets` needs `ticketsAndBooking`; `whatsOn` … | — | the guest home screens | Which module each section needs, proposed, client to correct (decided 28 September, audit R163). |
| Sections: title (`homepage.sections[].title`) | English and Arabic (Arabic right to left) | — | the guest home screens | — |
| Sections: sort order (`homepage.sections[].sortOrder`) | — | — | the guest home screens | — |
| Sections: is visible (`homepage.sections[].isVisible`) | — | — | the guest home screens | — |
| Sections: content page (`homepage.sections[].contentPageId`) | shows names, sends the id | — | the guest home screens | — |
| Sections: max items (`homepage.sections[].maxItems`) | — | — | GST-001 | How many items the section shows. On the mobile Home, `attractions`, `dining`, `whatsOn` and `shop` show 1 or 2 highlights (decided 29 September, MOB-3). |
| Sections: hero style (`homepage.sections[].heroStyle`) | Carousel · Video · Poster · Split | — | GST-001 | For `heroBanner` only (decided 29 September, MOB-3). |
| Slug (`pages.slug`) | pattern `^[a-z0-9-]+$` | — | the content and policy pages | — |
| Content pages title (`pages.title`) | English and Arabic (Arabic right to left) | — | the content and policy pages | — |
| Body (`pages.body`) | English and Arabic (Arabic right to left) | — | the content and policy pages | Keyed by language code. Values are sanitised HTML. |
| Content pages is enabled (`pages.isEnabled`) | — | on | the content and policy pages | BL-005. Enablement is not publication. |
| Icon (`pages.iconAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the content and policy pages | — |
| Category code (`pages.categoryCode`) | — | — | GST-057 | — |
| Content pages sort order (`pages.sortOrder`) | — | — | the content and policy pages | — |
| Content pages status (`pages.status`) | Draft · Published · Archived | — | the content and policy pages | Only `archived` is taken — send it to withdraw a published page or abandon a draft (`states/content.yaml`). |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-007` · status **notStarted** · provenance generated
- Flow F22 *A tenant rebrands their app*, step 3: Rearranges the homepage → Sections reordered, drag and drop
- Flow F22 branch at step 3 (recoverable): when Content exists only in English, Published anyway, with the gap listed per locale. **A CMS that blocks publishing until every locale is complete is a CMS nobody publishes from.**

#### Acceptance for the design

- [ ] Every input above is drawn (38), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-007?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save homepage layout, Create content page, Save content page, Save footer.
- [ ] Every transition is wired: `CMS-012`, `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `AI_USE`, `TENANT_CONFIGURE`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-008` Content Blocks

**Define what a block can and cannot contain, and set the banners (Site Builder step 5).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `core` module |
| Block | Block A · ticket #18105 (APP-WL-CMS-008) |
| Who uses it | venue staff holding `AI_USE`, `TENANT_CONFIGURE` (1 operate, 1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listPromoBlocks` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `bannerId` (navigation), `promoBlockId` (navigation), `actionId` (navigation) |
| Route | `/white-label/content-blocks` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| State | radio group | — | Draft · Scheduled · Active · Expired | `listBanners` ?state |

**Form: Create banner** (modal, opened by *Create banner*; *Create banner* calls `createBanner`, *Cancel* sends nothing)

**Collects what `createBanner` sends before it is called.** Required: `id`, `title`, `imageAssetRef`, `startsAt`. Optional: `subtitle`, `placement`, `linkTarget`, `endsAt`, `state`, `sortOrder`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createBanner` body |
| Subtitle `subtitle` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `createBanner` body |
| Image `imageAssetRef` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `createBanner` body |
| Placement `placement` | radio group | optional | — | Homepage hero · Homepage block · Explore · Checkout | — | — | `createBanner` body |
| Link target `linkTarget` | group | optional | — | — | — | — | `createBanner` body |
| Kind `linkTarget.kind` | select | required | — | Module · Content page · Product · Event · External URL · App section · None | — | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. | `createBanner` body |
| Module key `linkTarget.moduleKey` | select | optional | — | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | — | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown. | `createBanner` body |
| App section `linkTarget.appSection` | select | optional | — | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. | `createBanner` body |
| Content page `linkTarget.contentPageId` | picker: choose a content page | optional | — | — | shows names, sends the id | — | `createBanner` body |
| Product `linkTarget.productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `createBanner` body |
| Event `linkTarget.eventId` | picker: choose an event | optional | — | — | shows names, sends the id | — | `createBanner` body |
| URL `linkTarget.url` | text field | optional | — | — | — | — | `createBanner` body |
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createBanner` body |
| Ends at `endsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Must follow `startsAt` when set (decided 28 September, audit R163). Null runs the banner with no end. | `createBanner` body |
| Sort order `sortOrder` | number field | optional | — | — | — | — | `createBanner` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `createBanner` body |

**Form: Save banner** (modal, opened by *Save banner*; *Save banner* calls `updateBanner`, *Cancel* sends nothing)

**Collects what `updateBanner` sends before it is called.** Nothing in the body is required. Optional: `title`, `subtitle`, `imageAssetRef`, `placement`, `linkTarget`, `startsAt`, `endsAt`, `sortOrder`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateBanner` body |
| Subtitle `subtitle` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateBanner` body |
| Image `imageAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `updateBanner` body |
| Placement `placement` | radio group | optional | — | Homepage hero · Homepage block · Explore · Checkout | — | — | `updateBanner` body |
| Link target `linkTarget` | group | optional | — | — | — | — | `updateBanner` body |
| Kind `linkTarget.kind` | select | required | — | Module · Content page · Product · Event · External URL · App section · None | — | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. | `updateBanner` body |
| Module key `linkTarget.moduleKey` | select | optional | — | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | — | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown. | `updateBanner` body |
| App section `linkTarget.appSection` | select | optional | — | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. | `updateBanner` body |
| Content page `linkTarget.contentPageId` | picker: choose a content page | optional | — | — | shows names, sends the id | — | `updateBanner` body |
| Product `linkTarget.productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `updateBanner` body |
| Event `linkTarget.eventId` | picker: choose an event | optional | — | — | shows names, sends the id | — | `updateBanner` body |
| URL `linkTarget.url` | text field | optional | — | — | — | — | `updateBanner` body |
| Starts at `startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateBanner` body |
| Ends at `endsAt` | date and time picker | optional | — | When set, must follow `startsAt` (audit R163), or 400. | 1 Oct 2026, 14:30 (venue time zone) | Null runs the banner with no end. When set, must follow `startsAt` (audit R163), or 400. | `updateBanner` body |
| Sort order `sortOrder` | number field | optional | — | — | — | — | `updateBanner` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateBanner` body |

**Form: Create promo block** (modal, opened by *Create promo block*; *Create promo block* calls `createPromoBlock`, *Cancel* sends nothing)

**Collects what `createPromoBlock` sends before it is called.** Required: `id`, `title`. Optional: `description`, `iconAssetRef`, `promotionId`, `linkTarget`, `startsAt`, `endsAt`, `state`, `sortOrder`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createPromoBlock` body |
| Description `description` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `createPromoBlock` body |
| Icon `iconAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `createPromoBlock` body |
| Promotion `promotionId` | picker: choose a promotion | optional | — | — | shows names, sends the id | Presentation only. A block may point at a promotion; it does not create or price one. | `createPromoBlock` body |
| Link target `linkTarget` | group | optional | — | — | — | — | `createPromoBlock` body |
| Kind `linkTarget.kind` | select | required | — | Module · Content page · Product · Event · External URL · App section · None | — | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. | `createPromoBlock` body |
| Module key `linkTarget.moduleKey` | select | optional | — | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | — | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown. | `createPromoBlock` body |
| App section `linkTarget.appSection` | select | optional | — | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. | `createPromoBlock` body |
| Content page `linkTarget.contentPageId` | picker: choose a content page | optional | — | — | shows names, sends the id | — | `createPromoBlock` body |
| Product `linkTarget.productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `createPromoBlock` body |
| Event `linkTarget.eventId` | picker: choose an event | optional | — | — | shows names, sends the id | — | `createPromoBlock` body |
| URL `linkTarget.url` | text field | optional | — | — | — | — | `createPromoBlock` body |
| Starts at `startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPromoBlock` body |
| Ends at `endsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Must follow `startsAt` when both are set (decided 28 September, audit R163). | `createPromoBlock` body |
| Sort order `sortOrder` | number field | optional | — | — | — | — | `createPromoBlock` body |

Errors to draw in the form: 400 `endsAt` is not after `startsAt` (audit R163)

**Form: Save promo block** (modal, opened by *Save promo block*; *Save promo block* calls `updatePromoBlock`, *Cancel* sends nothing)

**Collects what `updatePromoBlock` sends before it is called.** Nothing in the body is required. Optional: `title`, `description`, `iconAssetRef`, `promotionId`, `linkTarget`, `startsAt`, `endsAt`, `sortOrder`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updatePromoBlock` body |
| Description `description` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updatePromoBlock` body |
| Icon `iconAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `updatePromoBlock` body |
| Promotion `promotionId` | picker: choose a promotion | optional | — | — | shows names, sends the id | — | `updatePromoBlock` body |
| Link target `linkTarget` | group | optional | — | — | — | — | `updatePromoBlock` body |
| Kind `linkTarget.kind` | select | required | — | Module · Content page · Product · Event · External URL · App section · None | — | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. | `updatePromoBlock` body |
| Module key `linkTarget.moduleKey` | select | optional | — | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | — | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown. | `updatePromoBlock` body |
| App section `linkTarget.appSection` | select | optional | — | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. | `updatePromoBlock` body |
| Content page `linkTarget.contentPageId` | picker: choose a content page | optional | — | — | shows names, sends the id | — | `updatePromoBlock` body |
| Product `linkTarget.productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `updatePromoBlock` body |
| Event `linkTarget.eventId` | picker: choose an event | optional | — | — | shows names, sends the id | — | `updatePromoBlock` body |
| URL `linkTarget.url` | text field | optional | — | — | — | — | `updatePromoBlock` body |
| Starts at `startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePromoBlock` body |
| Ends at `endsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePromoBlock` body |
| Sort order `sortOrder` | number field | optional | — | — | — | — | `updatePromoBlock` body |

Errors to draw in the form: 400 `endsAt` is not after `startsAt` (audit R163); 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The block is `active` or `expired`, and may only be withdrawn (audit R163).

#### Outputs: what the screen shows and produces

**Shown**

**Every promo block** (data table, from `listPromoBlocks`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Title | in the reader's language | — |
| Description | in the reader's language | — |
| Icon | the image or video | — |
| Promotion | the name it points at, never the id | Presentation only. A block may point at a promotion; it does not create or price one. |
| Link target | grouped details | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | Must follow `startsAt` when both are set (decided 28 September, audit R163). |
| State | chip: Draft, Scheduled, Active, Expired | Moved by the schedule timer at `startsAt` and `endsAt`, in the tenant's timezone, as for `Banner.state`. |
| Sort order | 1,234 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**Every banner** (data table, from `listBanners`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Title | in the reader's language | — |
| Subtitle | in the reader's language | — |
| Image | the image or video | — |
| Placement | chip: Homepage hero, Homepage block, Explore, Checkout | — |
| Link target | grouped details | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | Must follow `startsAt` when set (decided 28 September, audit R163). Null runs the banner with no end. |
| State | chip: Draft, Scheduled, Active, Expired | Moved by `updateBanner` between `draft` and `scheduled`, and by the schedule timer from `scheduled` to `active` and `active` to `expired` … |
| Sort order | 1,234 | — |
| Is active | yes / no (icon or chip) | — |

**The selected promo block** (detail panel, from `listPromoBlocks`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Title | in the reader's language | — |
| Description | in the reader's language | — |
| Icon | the image or video | — |
| Promotion | the name it points at, never the id | Presentation only. A block may point at a promotion; it does not create or price one. |
| Link target | grouped details | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | Must follow `startsAt` when both are set (decided 28 September, audit R163). |
| State | chip: Draft, Scheduled, Active, Expired | Moved by the schedule timer at `startsAt` and `endsAt`, in the tenant's timezone, as for `Banner.state`. |
| Sort order | 1,234 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create banner (primary button) | `createBanner` POST `/tenant-config/banners` | Banner | Banner | — | opens modal first |
| Save banner (secondary button) | `updateBanner` PATCH `/tenant-config/banners/{bannerId}` | inline | Banner | — | opens modal first |
| Create promo block (secondary button) | `createPromoBlock` POST `/tenant-config/promo-blocks` | PromoBlock | PromoBlock | 400 `endsAt` is not after `startsAt` (audit R163) | opens modal first |
| Save promo block (secondary button) | `updatePromoBlock` PATCH `/tenant-config/promo-blocks/{promoBlockId}` | inline | PromoBlock | 400 `endsAt` is not after `startsAt` (audit R163); 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The block is `active` or `expired`, and may only be … | opens modal first |
| Delete promo block (destructive button) | `deletePromoBlock` DELETE `/tenant-config/promo-blocks/{promoBlockId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Data it reads**: `listPromoBlocks` (onLoad, List promotional blocks); `listBanners` (onLoad, List banners)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*; carries `bannerId`

**What opens over it**

- confirmDialog *Delete promo block*: **Names what `deletePromoBlock` changes and what it leaves alone**, in the consequence rather than the verb. A content blocks this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The content blocks list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the content blocks untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No content blocks yet. Offers Create banner (`createBanner`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listPromoBlocks` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `listPromoBlocks` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `endsAt` is not after `startsAt` (audit R163); 409 Drafting is not allowed at this scope now: the capability is paused (`capability-paused`) or governance blocks it (`governance-blocked`, naming the policy and …; 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213).; 409 The block is `active` or `expired`, and may only be withdrawn … |

#### Permissions

- `createBanner` → `TENANT_CONFIGURE` (configure) · staff
- `updateBanner` → `TENANT_CONFIGURE` (configure) · staff
- `createPromoBlock` → `TENANT_CONFIGURE` (configure) · staff
- `updatePromoBlock` → `TENANT_CONFIGURE` (configure) · staff
- `deletePromoBlock` → `TENANT_CONFIGURE` (configure) · staff
- `listPromoBlocks` → `TENANT_CONFIGURE` (configure) · staff
- `listBanners` → `TENANT_CONFIGURE` (configure) · staff
- `deleteBanner` → `TENANT_CONFIGURE` (configure) · staff
- `proposeMarketingContent` → `AI_USE` (operate) · staff
- `decideProposedAction` → `AI_USE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `listPromoBlocks` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.10 | Banner Management - System shall support configurable promotional banners. | Guest Mobile App & Branding | CONTRACTED | `createBanner` |
| 19.1.11 | Promotional Block Management - System shall support configurable promotional content blocks. | Guest Mobile App & Branding | CONTRACTED | `updatePromoBlock` |
| 22.3.18 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.9 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.10 | AI Subject Line Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.9.17 | AI Language Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.14 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.16 | AI Website Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.17 | AI Mobile App Content Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 8.1.4 | Approval Before Execution AI recommendations affecting pricing or financial operations shall require approval before execution | Unified Operations Dashboard | CONTRACTED | `decideProposedAction` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Reusable page components per venue type are to be documented (e.g. seat-map component for stadiums/amphitheatres, park-map component for attraction venues) so one layout serves many venues with only imagery/data swapped. Documentation pending from Allam. *(open · MoM 20 Aug 2026, 4.10 CMS & White-Label; 6. Open Items · DI-395)*
- Layout builder: header, footer, logo, bottom-navigation icons and colours are configurable; banner sizing is configurable and promotion blocks are switched on/off by toggle. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-189)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Banners title (`banners.title`) | English and Arabic (Arabic right to left) | — | the guest home screens | — |
| Banners subtitle (`banners.subtitle`) | English and Arabic (Arabic right to left) | — | the guest home screens | — |
| Image (`banners.imageAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the guest home screens | — |
| Banners placement (`banners.placement`) | Homepage hero · Homepage block · Explore · Checkout | — | the guest home screens | — |
| Banners link target (`banners.linkTarget`) | — | — | the guest home screens | — |
| Link target: kind (`banners.linkTarget.kind`) | Module · Content page · Product · Event · External URL · App section · None | — | the guest home screens | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. |
| Link target: module key (`banners.linkTarget.moduleKey`) | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | — | WEB-050 | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown. |
| Link target: app section (`banners.linkTarget.appSection`) | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | the guest home screens | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. |
| Link target: content page (`banners.linkTarget.contentPageId`) | shows names, sends the id | — | the guest home screens | — |
| Link target: product (`banners.linkTarget.productId`) | shows names, sends the id | — | the guest home screens | — |
| Link target: event (`banners.linkTarget.eventId`) | shows names, sends the id | — | the guest home screens | — |
| Link target: uRL (`banners.linkTarget.url`) | — | — | the guest home screens | — |
| Banners starts at (`banners.startsAt`) | 1 Oct 2026, 14:30 (venue time zone) | — | the guest home screens | — |
| Banners ends at (`banners.endsAt`) | 1 Oct 2026, 14:30 (venue time zone) | — | the guest home screens | Must follow `startsAt` when set (decided 28 September, audit R163). Null runs the banner with no end. |
| Banners sort order (`banners.sortOrder`) | — | — | the guest home screens | — |
| Is active (`banners.isActive`) | — | — | the guest home screens | — |
| Promo blocks title (`promoBlocks.title`) | English and Arabic (Arabic right to left) | — | the guest home screens | — |
| Promo blocks description (`promoBlocks.description`) | English and Arabic (Arabic right to left) | — | the guest home screens | — |
| Icon (`promoBlocks.iconAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the guest home screens | — |
| Promotion (`promoBlocks.promotionId`) | shows names, sends the id | — | the guest home screens | Presentation only. A block may point at a promotion; it does not create or price one. |
| Promo blocks link target (`promoBlocks.linkTarget`) | — | — | the guest home screens | — |
| Link target: kind (`promoBlocks.linkTarget.kind`) | Module · Content page · Product · Event · External URL · App section · None | — | the guest home screens | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. |
| Link target: module key (`promoBlocks.linkTarget.moduleKey`) | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | — | WEB-050 | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown. |
| Link target: app section (`promoBlocks.linkTarget.appSection`) | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | the guest home screens | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. |
| Link target: content page (`promoBlocks.linkTarget.contentPageId`) | shows names, sends the id | — | the guest home screens | — |
| Link target: product (`promoBlocks.linkTarget.productId`) | shows names, sends the id | — | the guest home screens | — |
| Link target: event (`promoBlocks.linkTarget.eventId`) | shows names, sends the id | — | the guest home screens | — |
| Link target: uRL (`promoBlocks.linkTarget.url`) | — | — | the guest home screens | — |
| Promo blocks starts at (`promoBlocks.startsAt`) | 1 Oct 2026, 14:30 (venue time zone) | — | the guest home screens | — |
| Promo blocks ends at (`promoBlocks.endsAt`) | 1 Oct 2026, 14:30 (venue time zone) | — | the guest home screens | Must follow `startsAt` when both are set (decided 28 September, audit R163). |
| Promo blocks sort order (`promoBlocks.sortOrder`) | — | — | the guest home screens | — |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-008` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (62), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (33 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-008?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create banner, Save banner, Create promo block, Save promo block, Delete promo block.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `AI_USE`, `TENANT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-009` Navigation & Menus

**Decide what appears in the header, the footer and the mobile tab bar, with the Buy tickets button (Site Builder steps 5 and 6).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `fnb` module |
| Block | Block A · ticket #18169 (APP-WL-CMS-009) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE` (2 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listMenus` reads the population and `getMenu` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `menuId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/white-label/navigation-menus` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Outlet id | picker: choose an outlet (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?outletId=` to `listMenus`. | `listMenus` ?outletId |
| Active at | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?activeAt=` to `listMenus`. | `listMenus` ?activeAt |

**Form: Save navigation and tabs** (modal, opened by *Save navigation and tabs*; *Save navigation* calls `setNavigation`, *Cancel* sends nothing)

**Collects what `setNavigation` sends.** Required: `kind`, `items` (label, icon, target, visible, order; a mobile tab targets an `appSection`). Optional: `buyButton` (`style`, `label`). Refused `400` when a tab targets a disabled module or more than five are visible. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | segmented control | required | — | Bottom navigation · Drawer · Tabs | — | — | `setNavigation` body |
| Items `items` | repeatable rows | required | — | at most 12 | — | — | `setNavigation` body |
| Label `items[].label` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `setNavigation` body |
| Icon `items[].icon` | text field | optional | — | — | — | — | `setNavigation` body |
| Target `items[].target` | group | required | — | — | — | — | `setNavigation` body |
| Kind `items[].target.kind` | select | required | — | Module · Content page · Product · Event · External URL · App section · None | — | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. | `setNavigation` body |
| Module key `items[].target.moduleKey` | select | optional | — | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | — | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown. | `setNavigation` body |
| App section `items[].target.appSection` | select | optional | — | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. | `setNavigation` body |
| Content page `items[].target.contentPageId` | picker: choose a content page | optional | — | — | shows names, sends the id | — | `setNavigation` body |
| Product `items[].target.productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `setNavigation` body |
| Event `items[].target.eventId` | picker: choose an event | optional | — | — | shows names, sends the id | — | `setNavigation` body |
| URL `items[].target.url` | text field | optional | — | — | — | — | `setNavigation` body |
| Is visible `items[].isVisible` | toggle | required | — | At most five may be visible in bottom navigation; the rest overflow. | — | At most five may be visible in bottom navigation; the rest overflow. | `setNavigation` body |
| Sort order `items[].sortOrder` | number field | required | — | — | — | — | `setNavigation` body |
| Buy button `buyButton` | group | optional | — | — | — | The persistent Buy tickets button (decided 29 September, MOB-2). On every screen of the mobile app except the booking and checkout steps; it opens GST-003. | `setNavigation` body |
| Style `buyButton.style` | radio group | optional | Raised | Raised · Floating · Flat · Hidden | — | `raised` sits in the centre of the tab bar, as the v4 prototype shows; `hidden` turns it off. | `setNavigation` body |
| Label `buyButton.label` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setNavigation` body |

Errors to draw in the form: 400 An item targets a disabled module, or more than five are marked visible

**Form: Create menu** (modal, opened by *Create menu*; *Create menu* calls `createMenu`, *Cancel* sends nothing)

**Collects what `createMenu` sends before it is called.** Required: `code`, `name`, `outletId`. Optional: `availability`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createMenu` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createMenu` body |
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `createMenu` body |
| Availability `availability` | group | optional | — | — | — | When this menu is in force. Absent means always. | `createMenu` body |
| Days of week `availability.daysOfWeek` | list of values (chips) | optional | — | — | — | — | `createMenu` body |
| Start time `availability.startTime` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | Wall-clock time, in the Region's time zone. | `createMenu` body |
| End time `availability.endTime` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | Wall-clock time, in the Region's time zone. | `createMenu` body |
| Valid from `availability.validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Calendar day, in the Region's time zone, not UTC. | `createMenu` body |
| Valid to `availability.validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Calendar day, in the Region's time zone, not UTC. | `createMenu` body |

Errors to draw in the form: 400 Validation failed

**Form: Save menu sections** (modal, opened by *Save menu sections*; *Save menu sections* calls `setMenuSections`, *Cancel* sends nothing)

**Collects what `setMenuSections` sends before it is called.** Required: `sections`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Sections `sections` | repeatable rows | required | — | — | — | — | `setMenuSections` body |
| Code `sections[].code` | text field | required | — | — | — | — | `setMenuSections` body |
| Name `sections[].name` | text field | required | — | — | — | — | `setMenuSections` body |
| Sort order `sections[].sortOrder` | number field | required | — | — | — | — | `setMenuSections` body |
| Items `sections[].items` | repeatable rows | optional | — | — | — | The section's items, in sale-board order. An item's membership is `MenuItem.menuSectionId`. | `setMenuSections` body |
| ID `sections[].items[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setMenuSections` body |
| Product variant `sections[].items[].productVariantId` | picker: choose a product variant | required | — | — | shows names, sends the id | The catalogue variant this item sells. Pricing and tax come from there — a menu is a presentation of the catalogue, not a second catalogue. | `setMenuSections` body |
| Name `sections[].items[].name` | text field | required | — | — | — | — | `setMenuSections` body |
| Description `sections[].items[].description` | text area | optional | — | — | — | — | `setMenuSections` body |
| Price `sections[].items[].price` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setMenuSections` body |
| Sort order `sections[].items[].sortOrder` | number field | optional | — | — | — | — | `setMenuSections` body |
| Modifier groups `sections[].items[].modifierGroupIds` | multi-picker: choose modifier groups | optional | — | — | — | — | `setMenuSections` body |
| Station `sections[].items[].stationId` | picker: choose a station | optional | — | — | shows names, sends the id | — | `setMenuSections` body |
| Is stock tracked `sections[].items[].isStockTracked` | toggle | optional | — | Stock-tracked items cannot be sold offline. | — | True where a recipe exists. Stock-tracked items cannot be sold offline. | `setMenuSections` body |
| Is available `sections[].items[].isAvailable` | toggle | required | — | — | — | — | `setMenuSections` body |
| Unavailable reason `sections[].items[].unavailableReason` | text field | optional | — | — | — | — | `setMenuSections` body |
| Restore at `sections[].items[].restoreAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand. | `setMenuSections` body |
| Preparation minutes `sections[].items[].preparationMinutes` | number field (minutes) | optional | — | — | — | — | `setMenuSections` body |
| Allergens `sections[].items[].allergens` | multi-select chips | optional | — | Gluten · Crustaceans · Eggs · Fish · Peanuts · Soybeans · Milk · Nuts · Celery · Mustard · Sesame · Sulphites … | — | — | `setMenuSections` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Save menu** (modal, opened by *Save menu*; *Save menu* calls `updateMenu`, *Cancel* sends nothing)

**Collects what `updateMenu` sends before it is called.** Nothing in the body is required. Optional: `name`, `availability`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateMenu` body |
| Availability `availability` | group | optional | — | — | — | When this menu is in force. Absent means always. | `updateMenu` body |
| Days of week `availability.daysOfWeek` | list of values (chips) | optional | — | — | — | — | `updateMenu` body |
| Start time `availability.startTime` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | Wall-clock time, in the Region's time zone. | `updateMenu` body |
| End time `availability.endTime` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | Wall-clock time, in the Region's time zone. | `updateMenu` body |
| Valid from `availability.validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Calendar day, in the Region's time zone, not UTC. | `updateMenu` body |
| Valid to `availability.validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Calendar day, in the Region's time zone, not UTC. | `updateMenu` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateMenu` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

#### Outputs: what the screen shows and produces

**Shown**

**Every menu** (data table, from `listMenus`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Outlet | the name it points at, never the id | — |
| Availability | grouped details | When this menu is in force. Absent means always. |
| Sections | list or chips (count when long) | — |
| Is active | yes / no (icon or chip) | — |

**The selected menu** (detail panel, from `getMenu`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Outlet | the name it points at, never the id | — |
| Availability | grouped details | When this menu is in force. Absent means always. |
| Sections | list or chips (count when long) | — |
| Is active | yes / no (icon or chip) | — |

**Navigation and mobile tabs** (detail panel, from `getNavigation`): **The mobile tab editor (decided 29 September, MOB-1 and MOB-2).** Which tabs, their order, labels and icons; each tab is an `appSection` link. The default is Home, Explore, Plan and Tickets; Map is optional; Plan needs the `visitPlanner` module. The Buy tickets button: raised in the centre (default), floating, flat or hidden, and its label. At most five tabs are visible.

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Bottom navigation, Drawer, Tabs | — |
| Items | list or chips (count when long) | — |
| Buy button | grouped details | The persistent Buy tickets button (decided 29 September, MOB-2). On every screen of the mobile app except the booking and checkout steps … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save navigation and tabs (secondary button) | `setNavigation` PUT `/tenant-config/navigation` | NavigationConfig | NavigationConfig | 400 An item targets a disabled module, or more than five are marked visible | opens modal first |
| Create menu (primary button) | `createMenu` POST `/menus` | CreateMenuRequest | Menu | 400 Validation failed | opens modal first |
| Save menu sections (secondary button) | `setMenuSections` PUT `/menus/{menuId}/sections` | inline | Menu | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| Save menu (secondary button) | `updateMenu` PATCH `/menus/{menuId}` | inline | Menu | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |

**Data it reads**: `getNavigation` (onLoad, The navigation and the mobile tab set (MOB-1)); `listMenus` (onLoad, List menus)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The navigation menus list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the navigation menus untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No navigation menus yet. Offers Create menu (`createMenu`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on outletId, activeAt and the navigation menus are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listMenus` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 An item targets a disabled module, or more than five are marked visible; 400 Validation failed |

#### Permissions

- `getNavigation` → `TENANT_CONFIGURE` (configure) · staff
- `listMenus` → `PRODUCT_VIEW` (read) · staff
- `getMenu` → `PRODUCT_VIEW` (read) · staff
- `createMenu` → `PRODUCT_CONFIGURE` (configure) · staff
- `setMenuSections` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateMenu` → `PRODUCT_CONFIGURE` (configure) · staff
- `setNavigation` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listMenus` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.22 | The system should provide the option to split menu items by sections for specific locations of the outlet. For example: one menu section going to kitchen and the other going to the drink bar. The … | Bundles and Promotions | CONTRACTED | `setMenuSections` |
| 4.9.3 | The system should provide the option to remotely configure visibility and placement of available menu items available for sale on POS screen. The function should be limited to only users accounts … | Bundles and Promotions | CONTRACTED | `setMenuSections` |
| 4.9.4 | The system should be able to design a menu button layout page can be copied and re-used in multiple locations if the need arises | Bundles and Promotions | CONTRACTED | `setMenuSections` |
| 19.1.8 | Menu Configuration - System shall support configurable navigation menus. | Guest Mobile App & Branding | CONTRACTED | `setNavigation` |
| 19.1.12 | Navigation Label Management - System shall support configurable navigation labels. | Guest Mobile App & Branding | CONTRACTED | `setNavigation` |
| 2.1.32 | System shall allow guests to purchase food and beverage items through self-service kiosks. The kiosk shall support menu browsing, product customization, combo meals, upsell recommendations … | Ticketing Sales | CONTRACTED | data `Menu` |
| 2.1.33 | System shall allow guests to purchase retail merchandise through self-service kiosks. The kiosk shall support product browsing, inventory validation, variant selection (size, color, style) … | Ticketing Sales | CONTRACTED | data `Menu` |
| 4.6.13 | The system should have a interface for kiosks where the guest should be able to place order via the self service option all the way till completing payments. | Bundles and Promotions | CONTRACTED | data `Menu` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The home-screen navigation bar layout is configurable: home/explore/map/buy-tickets in different arrangements. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1087)*
- Six Flags Kidiya reference: fixed header with configurable navigation (logo, Explore/Tickets/Passes, sub-menus), every item toggleable via the CMS. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-424)*
- Allam: the venue's main website is fully venue-managed; after "Book Now" the white-label B2C flow keeps the venue's header/footer branding while product selection, cart and checkout are TICVAI-managed. Header/footer links to non-checkout pages redirect to the main venue site. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-397)*
- Layout builder: header, footer, logo, bottom-navigation icons and colours are configurable; banner sizing is configurable and promotion blocks are switched on/off by toggle. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-189)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A82** Design the F&B Command Center suite: a real-time cross-outlet sales/operations dashboard, the F&B Stock Command Center (stock value, low-stock alerts, recipe-based consumption, batch/wastage tracking, replenishment … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'recipe')*
- **A83** Design the Menu & Product Command Center and Menu Builder (recipe/product mapping alerts, drag-and-drop POS layout, chargeable/free modifiers with min/max rules, combo meals with upgrade options) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'menu & product')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Navigation kind (`navigation.kind`) | Bottom navigation · Drawer · Tabs | — | every guest screen (web, app and kiosk) | the main navigation: bottom tab bar, drawer, or tabs |
| Navigation items (`navigation.items`) | at most 12 | — | every guest screen (web, app and kiosk) | — |
| Items: label (`navigation.items[].label`) | English and Arabic (Arabic right to left) | — | every guest screen (web, app and kiosk) | — |
| Items: icon (`navigation.items[].icon`) | — | — | every guest screen (web, app and kiosk) | — |
| Items: target (`navigation.items[].target`) | — | — | every guest screen (web, app and kiosk) | — |
| Target: kind (`navigation.items[].target.kind`) | Module · Content page · Product · Event · External URL · App section · None | — | every guest screen (web, app and kiosk) | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. |
| Target: module key (`navigation.items[].target.moduleKey`) | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | — | WEB-050 | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown. |
| Target: app section (`navigation.items[].target.appSection`) | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | every guest screen (web, app and kiosk) | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. |
| Target: content page (`navigation.items[].target.contentPageId`) | shows names, sends the id | — | every guest screen (web, app and kiosk) | — |
| Target: product (`navigation.items[].target.productId`) | shows names, sends the id | — | every guest screen (web, app and kiosk) | — |
| Target: event (`navigation.items[].target.eventId`) | shows names, sends the id | — | every guest screen (web, app and kiosk) | — |
| Target: uRL (`navigation.items[].target.url`) | — | — | every guest screen (web, app and kiosk) | — |
| Items: is visible (`navigation.items[].isVisible`) | At most five may be visible in bottom navigation; the rest overflow. | — | every guest screen (web, app and kiosk) | At most five may be visible in bottom navigation; the rest overflow. |
| Items: sort order (`navigation.items[].sortOrder`) | — | — | every guest screen (web, app and kiosk) | — |
| Buy button (`navigation.buyButton`) | — | — | GST-003 | The persistent Buy tickets button (decided 29 September, MOB-2). On every screen of the mobile app except the booking and checkout steps; it opens GST-003. |
| Buy button: style (`navigation.buyButton.style`) | Raised · Floating · Flat · Hidden | Raised | every P02 screen | the Buy tickets button in the tab bar: raised (default), floating, flat, or hidden |
| Buy button: label (`navigation.buyButton.label`) | English and Arabic (Arabic right to left) | — | every guest screen (web, app and kiosk) | — |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-009` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (55), with its required mark, default, format and its error state (400, 403, 404, 412).
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-009?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save navigation and tabs, Create menu, Save menu sections, Save menu.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-010` Media Library

**Hold the imagery, and know where it is used.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `ticketing` module |
| Block | Block A · ticket #18146 (APP-WL-CMS-010) |
| Who uses it | venue staff holding `AI_USE`, `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`, `ORDER_CREATE`, `ORDER_VIEW` (2 operate, 1 configure, 2 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `searchMedia` reads the population and `getMediaEntitlements` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `mediaCode` (deepLink), `mediaId` (deepLink), `uploadId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/white-label/media-library` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Archive and quarantine are reversible; deletion is the only end of an asset's life (decided 28 September, audit STATE-MEDIA).** An archived asset offers **Restore** (`updateMediaAsset` with `status: ready`); a quarantined one offers **Release**, which is the same call after a reviewer has cleared the scan flag (the state model marks that move as needing approval). **Delete media asset** (`deleteMediaAsset`) removes the asset for good and is refused while it is referenced.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Kind | select | optional | — | Image · Video · Audio · Document · Vector · Font · Archive | — | Sends `?kind=` to `searchMedia`. | `searchMedia` ?kind |
| Tag | text field | optional | — | — | — | Sends `?tag=` to `searchMedia`. | `searchMedia` ?tag |
| Collection id | picker: choose a collection (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?collectionId=` to `searchMedia`. | `searchMedia` ?collectionId |
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `searchMedia`. | `searchMedia` ?venueId |
| Search | text field | optional | — | — | — | Sends `?search=` to `searchMedia`. | `searchMedia` ?search |
| Unused only | toggle | optional | off | — | — | Sends `?unusedOnly=` to `searchMedia`. | `searchMedia` ?unusedOnly |
| Rights expiring within days | number field (days) | optional | — | — | — | Sends `?rightsExpiringWithinDays=` to `searchMedia`. | `searchMedia` ?rightsExpiringWithinDays |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Within days | number field (days) | 60 | — | `getExpiringRights` ?withinDays |

**Form: Restore media asset** (confirmDialog, opened by *Restore media asset*; *Restore* calls `updateMediaAsset`, *Cancel* sends nothing)

**Returns an archived asset to `ready`**, so it can be used again (decided 28 September, audit STATE-MEDIA). Names the asset.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateMediaAsset` body |
| Description `description` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateMediaAsset` body |
| Alt text `altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Accessibility text. Required before an asset may be used in a guest-facing surface — WCAG 2.2 AA is a stated target. | `updateMediaAsset` body |
| Tags `tags` | list of values (chips) | optional | — | — | — | — | `updateMediaAsset` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | Replaces the asset's collection memberships. Stored as `MediaCollectionMember` rows, one per collection. | `updateMediaAsset` body |
| Rights `rights` | group | optional | — | — | — | Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item. | `updateMediaAsset` body |
| Licence kind `rights.licenceKind` | select | optional | — | Owned · Royalty free · Rights managed · Creative commons · Editorial only · Unknown | — | — | `updateMediaAsset` body |
| Licensor `rights.licensor` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Licence reference `rights.licenceReference` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Valid from `rights.validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateMediaAsset` body |
| Valid to `rights.validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateMediaAsset` body |
| Permitted uses `rights.permittedUses` | multi-select chips | optional | — | Web · Print · Social media · In venue · Advertising · Internal | — | — | `updateMediaAsset` body |
| Attribution required `rights.attributionRequired` | toggle | optional | off | — | — | — | `updateMediaAsset` body |
| Attribution text `rights.attributionText` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Permitted territories `rights.permittedTerritories` | list of values (chips) | optional | — | — | — | ISO country or region codes. Empty means unrestricted, which is a claim rather than an absence — an unknown territory and a worldwide licence are not the same thing, and … | `updateMediaAsset` body |
| Permitted channels `rights.permittedChannels` | list of values (chips) | optional | — | — | — | Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route. | `updateMediaAsset` body |
| Model release held `rights.modelReleaseHeld` | toggle | optional | off | — | — | — | `updateMediaAsset` body |
| Renewal owner `rights.renewalOwner` | picker: choose a renewal owner | optional | — | — | shows names, sends the id | — | `updateMediaAsset` body |
| Status `status` | segmented control | optional | — | Ready · Archived; Any transition that model does not give `updateMediaAsset` is refused with 409 `transitionNotAllowed`. | — | A lifecycle move from `states/media.yaml`. Any transition that model does not give `updateMediaAsset` is refused with 409 `transitionNotAllowed`. | `updateMediaAsset` body |

Errors to draw in the form: 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem)

**Form: Release from quarantine** (confirmDialog, opened by *Release from quarantine*; *Release* calls `updateMediaAsset`, *Cancel* sends nothing)

**Releases a quarantined asset to `ready` after review** (decided 28 September, audit STATE-MEDIA). Names the asset and the scan finding, and records the reviewer; the state model marks this reversal as needing approval.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateMediaAsset` body |
| Description `description` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateMediaAsset` body |
| Alt text `altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Accessibility text. Required before an asset may be used in a guest-facing surface — WCAG 2.2 AA is a stated target. | `updateMediaAsset` body |
| Tags `tags` | list of values (chips) | optional | — | — | — | — | `updateMediaAsset` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | Replaces the asset's collection memberships. Stored as `MediaCollectionMember` rows, one per collection. | `updateMediaAsset` body |
| Rights `rights` | group | optional | — | — | — | Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item. | `updateMediaAsset` body |
| Licence kind `rights.licenceKind` | select | optional | — | Owned · Royalty free · Rights managed · Creative commons · Editorial only · Unknown | — | — | `updateMediaAsset` body |
| Licensor `rights.licensor` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Licence reference `rights.licenceReference` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Valid from `rights.validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateMediaAsset` body |
| Valid to `rights.validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateMediaAsset` body |
| Permitted uses `rights.permittedUses` | multi-select chips | optional | — | Web · Print · Social media · In venue · Advertising · Internal | — | — | `updateMediaAsset` body |
| Attribution required `rights.attributionRequired` | toggle | optional | off | — | — | — | `updateMediaAsset` body |
| Attribution text `rights.attributionText` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Permitted territories `rights.permittedTerritories` | list of values (chips) | optional | — | — | — | ISO country or region codes. Empty means unrestricted, which is a claim rather than an absence — an unknown territory and a worldwide licence are not the same thing, and … | `updateMediaAsset` body |
| Permitted channels `rights.permittedChannels` | list of values (chips) | optional | — | — | — | Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route. | `updateMediaAsset` body |
| Model release held `rights.modelReleaseHeld` | toggle | optional | off | — | — | — | `updateMediaAsset` body |
| Renewal owner `rights.renewalOwner` | picker: choose a renewal owner | optional | — | — | shows names, sends the id | — | `updateMediaAsset` body |
| Status `status` | segmented control | optional | — | Ready · Archived; Any transition that model does not give `updateMediaAsset` is refused with 409 `transitionNotAllowed`. | — | A lifecycle move from `states/media.yaml`. Any transition that model does not give `updateMediaAsset` is refused with 409 `transitionNotAllowed`. | `updateMediaAsset` body |

Errors to draw in the form: 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem)

**Form: Append entitlement to media** (modal, opened by *Append entitlement to media*; *Append entitlement to media* calls `appendEntitlementToMedia`, *Cancel* sends nothing)

**Collects what `appendEntitlementToMedia` sends before it is called.** Required: `id`, `lines`, `recordedAt`. Optional: `paymentMethod`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the new order this creates, and its idempotency key — it must equal the `Idempotency-Key` header. | `appendEntitlementToMedia` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `appendEntitlementToMedia` body |
| Variant `lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `appendEntitlementToMedia` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `appendEntitlementToMedia` body |
| Performance `lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `appendEntitlementToMedia` body |
| Payment method `paymentMethod` | radio group | optional | — | Card · Cash · Wallet · Gift card · Charge to account | — | — | `appendEntitlementToMedia` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `appendEntitlementToMedia` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `appendEntitlementToMedia` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Media expired (`mediaExpired`), blocked (`mediaBlocked`), already surrendered at exit (`mediaSurrendered`), or the entitlement cannot share media … (AppendRefusedProblem)

**Form: Complete upload** (modal, opened by *Complete upload*; *Complete upload* calls `completeUpload`, *Cancel* sends nothing)

**Collects what `completeUpload` sends before it is called.** Nothing in the body is required. Optional: `title`, `altText`, `tags`, `collectionIds`, `rights`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `completeUpload` body |
| Alt text `altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `completeUpload` body |
| Tags `tags` | list of values (chips) | optional | — | — | — | — | `completeUpload` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | — | `completeUpload` body |
| Rights `rights` | group | optional | — | — | — | Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item. | `completeUpload` body |
| Licence kind `rights.licenceKind` | select | optional | — | Owned · Royalty free · Rights managed · Creative commons · Editorial only · Unknown | — | — | `completeUpload` body |
| Licensor `rights.licensor` | text field | optional | — | — | — | — | `completeUpload` body |
| Licence reference `rights.licenceReference` | text field | optional | — | — | — | — | `completeUpload` body |
| Valid from `rights.validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `completeUpload` body |
| Valid to `rights.validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `completeUpload` body |
| Permitted uses `rights.permittedUses` | multi-select chips | optional | — | Web · Print · Social media · In venue · Advertising · Internal | — | — | `completeUpload` body |
| Attribution required `rights.attributionRequired` | toggle | optional | off | — | — | — | `completeUpload` body |
| Attribution text `rights.attributionText` | text field | optional | — | — | — | — | `completeUpload` body |
| Permitted territories `rights.permittedTerritories` | list of values (chips) | optional | — | — | — | ISO country or region codes. Empty means unrestricted, which is a claim rather than an absence — an unknown territory and a worldwide licence are not the same thing, and … | `completeUpload` body |
| Permitted channels `rights.permittedChannels` | list of values (chips) | optional | — | — | — | Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route. | `completeUpload` body |
| Model release held `rights.modelReleaseHeld` | toggle | optional | off | — | — | — | `completeUpload` body |
| Renewal owner `rights.renewalOwner` | picker: choose a renewal owner | optional | — | — | shows names, sends the id | — | `completeUpload` body |

Errors to draw in the form: 409 The transfer never finished (`transferIncomplete`), the upload ticket expired (`uploadExpired`), or the stored file is larger than the ticket allowed … (UploadRefusedProblem)

**Form: Create collection** (modal, opened by *Create collection*; *Create collection* calls `createCollection`, *Cancel* sends nothing)

**Collects what `createCollection` sends before it is called.** Required: `name`. Optional: `description`, `venueId`, `parentCollectionId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `createCollection` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `createCollection` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createCollection` body |
| Parent collection `parentCollectionId` | picker: choose a parent collection | optional | — | — | shows names, sends the id | — | `createCollection` body |

Errors to draw in the form: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …

**Form: Create upload** (modal, opened by *Create upload*; *Create upload* calls `createUpload`, *Cancel* sends nothing)

**Collects what `createUpload` sends before it is called.** Required: `filename`, `contentType`, `sizeBytes`. Optional: `venueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Filename `filename` | text area | required | — | max length 256 | — | — | `createUpload` body |
| Content type `contentType` | text field | required | — | — | — | — | `createUpload` body |
| Size bytes `sizeBytes` | number field | required | — | min 1 | — | — | `createUpload` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createUpload` body |

Errors to draw in the form: 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes.

**Form: Replace media asset** (modal, opened by *Replace media asset*; *Replace media asset* calls `replaceMediaAsset`, *Cancel* sends nothing)

**Collects what `replaceMediaAsset` sends before it is called.** Required: `uploadId`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Upload `uploadId` | picker: choose an upload | required | — | — | shows names, sends the id | — | `replaceMediaAsset` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `replaceMediaAsset` body |

Errors to draw in the form: 409 The upload cannot be used: it is a different kind — an image cannot replace a document (`kindMismatch`) — or the transfer never finished … (UploadRefusedProblem)

**Form: Save media asset** (modal, opened by *Save media asset*; *Save media asset* calls `updateMediaAsset`, *Cancel* sends nothing)

**Collects what `updateMediaAsset` sends before it is called.** Nothing in the body is required. Optional: `title`, `description`, `altText`, `tags`, `collectionIds`, `rights`, `status`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateMediaAsset` body |
| Description `description` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateMediaAsset` body |
| Alt text `altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Accessibility text. Required before an asset may be used in a guest-facing surface — WCAG 2.2 AA is a stated target. | `updateMediaAsset` body |
| Tags `tags` | list of values (chips) | optional | — | — | — | — | `updateMediaAsset` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | Replaces the asset's collection memberships. Stored as `MediaCollectionMember` rows, one per collection. | `updateMediaAsset` body |
| Rights `rights` | group | optional | — | — | — | Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item. | `updateMediaAsset` body |
| Licence kind `rights.licenceKind` | select | optional | — | Owned · Royalty free · Rights managed · Creative commons · Editorial only · Unknown | — | — | `updateMediaAsset` body |
| Licensor `rights.licensor` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Licence reference `rights.licenceReference` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Valid from `rights.validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateMediaAsset` body |
| Valid to `rights.validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateMediaAsset` body |
| Permitted uses `rights.permittedUses` | multi-select chips | optional | — | Web · Print · Social media · In venue · Advertising · Internal | — | — | `updateMediaAsset` body |
| Attribution required `rights.attributionRequired` | toggle | optional | off | — | — | — | `updateMediaAsset` body |
| Attribution text `rights.attributionText` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Permitted territories `rights.permittedTerritories` | list of values (chips) | optional | — | — | — | ISO country or region codes. Empty means unrestricted, which is a claim rather than an absence — an unknown territory and a worldwide licence are not the same thing, and … | `updateMediaAsset` body |
| Permitted channels `rights.permittedChannels` | list of values (chips) | optional | — | — | — | Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route. | `updateMediaAsset` body |
| Model release held `rights.modelReleaseHeld` | toggle | optional | off | — | — | — | `updateMediaAsset` body |
| Renewal owner `rights.renewalOwner` | picker: choose a renewal owner | optional | — | — | shows names, sends the id | — | `updateMediaAsset` body |
| Status `status` | segmented control | optional | — | Ready · Archived; Any transition that model does not give `updateMediaAsset` is refused with 409 `transitionNotAllowed`. | — | A lifecycle move from `states/media.yaml`. Any transition that model does not give `updateMediaAsset` is refused with 409 `transitionNotAllowed`. | `updateMediaAsset` body |

Errors to draw in the form: 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem)

#### Outputs: what the screen shows and produces

**Shown**

**Every media asset** (data table, from `searchMedia`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Image, Video, Audio, Document, Vector, Font… | — |
| Status | chip: Processing, Ready, Quarantined, Failed, Archived | — |
| Filename | text | — |
| Content type | text | — |
| Size bytes | 1,234 | — |
| Title | in the reader's language | — |
| Alt text | in the reader's language | Required before use in a guest-facing surface. WCAG 2.2 AA. |
| Width | 1,234 | — |
| Height | 1,234 | — |
| Duration seconds | 1,234.5 | — |
| Custom metadata | grouped details | BL-178. `assets` is a strong contract and its metadata was fixed — kind, title, alt text, dimensions, rights. |

**Every collection** (data table, from `listCollections`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Name | text | Unique per tenant (decided 28 September, audit R108). A name already used by any collection in the tenant, at any venue or level, is … |
| Description | text | — |
| Venue | the name it points at, never the id | — |
| Parent collection | the name it points at, never the id | — |
| Asset count | 1,234 | — |
| Cover image | the image or video | — |

**The selected media asset** (detail panel, from `searchMedia`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Image, Video, Audio, Document, Vector, Font… | — |
| Status | chip: Processing, Ready, Quarantined, Failed, Archived | — |
| Filename | text | — |
| Content type | text | — |
| Size bytes | 1,234 | — |
| Title | in the reader's language | — |
| Description | in the reader's language | Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored. |
| Alt text | in the reader's language | Required before use in a guest-facing surface. WCAG 2.2 AA. |
| Width | 1,234 | — |
| Height | 1,234 | — |
| Duration seconds | 1,234.5 | — |
| Custom metadata | grouped details | BL-178. `assets` is a strong contract and its metadata was fixed — kind, title, alt text, dimensions, rights. |
| Shared with tenants | list or chips (count when long) | BL-178. Cross-tenant sharing, and it is refused by default for a reason. |
| Tags | list or chips (count when long) | — |
| Venue | the name it points at, never the id | — |

**The expiring media** (detail panel, from `getExpiringRights`)

| Shows | Format | Notes |
|---|---|---|
| Asset | the image or video | — |
| Filename | text | — |
| Thumbnail URL | text | — |
| Licensor | text | — |
| Valid to | 1 Oct 2026 | — |
| Days remaining | 1,234 | — |
| Is expired | yes / no (icon or chip) | — |
| Is in use | yes / no (icon or chip) | True while `liveUsageCount` is above zero, that is, while live (published) content references the asset (audit R106 (10)). |
| Live usage count | 1,234 | References from live (published) content only (audit R106 (10)). Expired and live is the combination that matters. |

**The media asset** (detail panel, from `getMediaAsset`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Image, Video, Audio, Document, Vector, Font… | — |
| Status | chip: Processing, Ready, Quarantined, Failed, Archived | — |
| Filename | text | — |
| Content type | text | — |
| Size bytes | 1,234 | — |
| Title | in the reader's language | — |
| Description | in the reader's language | Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored. |
| Alt text | in the reader's language | Required before use in a guest-facing surface. WCAG 2.2 AA. |
| Width | 1,234 | — |
| Height | 1,234 | — |
| Duration seconds | 1,234.5 | — |
| Custom metadata | grouped details | BL-178. `assets` is a strong contract and its metadata was fixed — kind, title, alt text, dimensions, rights. |
| Shared with tenants | list or chips (count when long) | BL-178. Cross-tenant sharing, and it is refused by default for a reason. |
| Tags | list or chips (count when long) | — |
| Venue | the name it points at, never the id | — |

**The media entitlements** (detail panel, from `getMediaEntitlements`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Media kind | chip: QR, Wristband, Card, NFC, Mobile pass | — |
| Subject | the name it points at, never the id | — |
| Is valid | yes / no (icon or chip) | — |
| Invalid reason | text | — |
| Can accept more | yes / no (icon or chip) | False where the media has been surrendered, expired or blocked. A cashier should know before taking money, not after. |
| Entitlements | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Append entitlement to media (primary button) | `appendEntitlementToMedia` POST `/media/{mediaCode}/entitlements` | AppendEntitlementRequest | AppendEntitlementResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Media expired (`mediaExpired`), blocked (`mediaBlocked`), already surrendered at exit (`mediaSurrendered`), or … | opens modal first; produces a document or message: Add something to a ticket the guest already holds |
| Complete upload (secondary button) | `completeUpload` POST `/media/uploads/{uploadId}/complete` | inline | MediaAsset | 409 The transfer never finished (`transferIncomplete`), the upload ticket expired (`uploadExpired`), or the stored file is larger than the ticket allowed … (UploadRefusedProblem) | opens modal first |
| Create collection (secondary button) | `createCollection` POST `/media/collections` | inline | Collection | 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … | opens modal first |
| Create upload (secondary button) | `createUpload` POST `/media/uploads` | inline | UploadTicket | 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes. | opens modal first |
| Delete media asset (destructive button) | `deleteMediaAsset` DELETE `/media/{mediaId}` | — | — | 409 Asset is in use. (MediaInUseProblem) | — |
| Replace media asset (secondary button) | `replaceMediaAsset` POST `/media/{mediaId}/replace` | inline | MediaReplaceResult | 409 The upload cannot be used: it is a different kind — an image cannot replace a document (`kindMismatch`) — or the transfer never finished … (UploadRefusedProblem) | opens modal first |
| Save media asset (secondary button) | `updateMediaAsset` PATCH `/media/{mediaId}` | inline | MediaAsset | 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem) | opens confirmDialog first |
| Restore media asset (secondary button) | `updateMediaAsset` PATCH `/media/{mediaId}` | inline | MediaAsset | 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem) | opens confirmDialog first |
| Release from quarantine (secondary button) | `updateMediaAsset` PATCH `/media/{mediaId}` | inline | MediaAsset | 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem) | opens confirmDialog first |

**Data it reads**: `searchMedia` (onLoad, Search the asset library); `getExpiringRights` (onLoad, Assets whose licence is expiring or expired); `listCollections` (onLoad, List collections)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*; carries `uploadId`
- → `CMS-003` Typography: *Typography*

**What opens over it**

- confirmDialog *Delete media asset*: **Names what `deleteMediaAsset` changes and what it leaves alone**, in the consequence rather than the verb. A media this affects should be identified in the dialog, not just counted. **Deletion is the only end of an asset's life and cannot be undone** (decided 28 September, audit STATE-MEDIA); the …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The media list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the media untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No media yet. Offers Create collection (`createCollection`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on kind, tag, collectionId, venueId, search, unusedOnly and the media are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getMediaEntitlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes.; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 409 Asset is in use. (MediaInUseProblem); 409 Media expired (`mediaExpired`), blocked … |

#### Permissions

- `getMediaEntitlements` → `ORDER_VIEW` (read) · staff
- `searchMedia` → `ASSET_LIBRARY_VIEW` (read) · staff
- `appendEntitlementToMedia` → `ORDER_CREATE` (operate) · staff
- `completeUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `createCollection` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `createUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `deleteMediaAsset` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `getExpiringRights` → `ASSET_LIBRARY_VIEW` (read) · staff
- `getMediaAsset` → `ASSET_LIBRARY_VIEW` (read) · staff
- `listCollections` → `ASSET_LIBRARY_VIEW` (read) · staff
- `replaceMediaAsset` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `updateMediaAsset` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `semanticSearch` → `AI_USE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getMediaEntitlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

36 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.11 | Ticket Storage - System shall store digital tickets. | Guest Mobile App & Branding | CONTRACTED | `getMediaEntitlements` |
| 2.6.18 | - Dynamic QR code | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.7.24 | The BtoB Customer can also receive simple QR Codes, vouchers or packaged PLUs. | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.13.3 | Tickets can be issued and sent either by email (PDF or M-ticket, E-ticket). | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.14.16 | Generate digital cards with QR/NFC/barcode. | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.16.2 | The system should support multiple media types for a ticket. Expected formats: - Paper/thermal tickets with QR, Barcode, RFID - Print at home tickets with QR, Barcode - Smartphones: NFC (near-field … | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.16.17 | The system shall allow multiple media types to be linked to the same guest account and entitlement simultaneously, including QR tickets, RFID wristbands, membership cards, and mobile wallets. | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 3.1.1 | Dynamic QR Code Supports: 1. Registration: Customers select "Digital Ticket" via the confirmation page, email, or ticket PDF to begin the enrollment process. 2.Activation: After registration, the … | Admission and Access | CONTRACTED | `getMediaEntitlements` |
| 3.1.2 | Unique Code per Ticket: Generate a unique QR code for every issued ticket or pass. | Admission and Access | CONTRACTED | `getMediaEntitlements` |
| 3.1.7 | Dynamic QR technology shall support memberships, annual passes, loyalty accounts, wallets, and other digital credentials in addition to standard tickets. | Admission and Access | CONTRACTED | `getMediaEntitlements` |
| 3.2.63 | It is expected that the access code created by the system is unique and randomized to improve fraud prevention. | Admission and Access | CONTRACTED | `getMediaEntitlements` |
| 5.4.18 | Provide digital loyalty card in app. | F&B & Guest Management | CONTRACTED | `getMediaEntitlements` |
| … 24 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Font and image upload guardrails: size/format restrictions and pixel limits (e.g. banner image ≤ 1024px), validated on upload with an explanatory note to the tenant admin, so cursive/bold fonts cannot overflow banners or descriptions. *(agreed · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-188)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-010` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (99), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (67 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-010?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Append entitlement to media, Complete upload, Create collection, Create upload, Delete media asset, Replace media asset, Save media asset, Restore media asset, Release from quarantine.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `AI_USE`, `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`, `ORDER_CREATE`, `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P13 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/guest-rev3-29-september/TICVAI Engine Controls Manual.dc.html`: the look of the controls: every configuration control, laid out and explained.
- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the configuration side panel, for the controls, and the guest booking the live preview shows.
- `sources/designs/TICVAI_White_Label_Guest_App_UI_Reference_1.pdf`: the client's White Label Builder boards.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P13 as a whole** (5: 0 open, 5 closed). Open first; a closed row says where it went on 30 September.

- **A47** Advise Qossai/Allam on the Apple/Google Developer account ownership model and a simplified, low-effort app-publishing workflow for white-labelled tenant apps (incl. how to reflect "Powered by TICVAI" branding) *(Pradnya Yeram · Low · Done → 30 Sep: Closed, Done (as recorded earlier) · 24 Sep 2026 · workshop tracker)*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker)*
- **A338** Build the real white-label CMS builder (client builds a site in ~30 min) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 24 Sep 2026 · workshop tracker)*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker)*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker)*

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

### Across P13 Venue CMS

- The config side panel is a reference tool only, not the CMS. The CMS will be step-based and include header/footer, logos and banners. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W12 Config side panel · DI-1014)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- Qossai: build AI-assisted site design/generation into the website builder, keeping site design (header, footer, color, font, layout) separate from content (tickets), with tickets flowing into the site's structure once published. To be explored. *(client request · MoM 3 Aug 2026, 7. AI-Assisted Website Generation · DI-115)*
- Qossai: give clients as much design flexibility as possible within the configurable structure. *(client request · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-114)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

### In P13 · White Label

- Font, header/footer (not yet in the current wireframe build), card size and layout are configurable in the mobile app, consistent with the web app's white-labelling approach. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1097)*
- Qossai (rated the CMS prototype ~70%): a client should be able to build a working site "within 30 minutes", easily adding header, footer, fonts and its own images/graphics self-service; Allam: every CMS option must visibly change something and the interface must be intuitive to navigate. *(client request · MoM 24 Sep 2026, 4.8 Guest Web App CMS Prototype — Feedback on Maturity & Scope Expectations · DI-988)*
- The reviewed prototype is the actual guest-facing B2C site customers browse and book from, not a CMS tool. A separate, more limited white-label interface lets a client adjust colours, fonts and layout from a menu of options; not yet built in the prototype. *(agreed · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-887)*
- Base structure (header, footer, layout) is fixed across tenants; logo, colour, font and module visibility (e.g. hide Dining or Retail) are configurable per tenant, and independently for web and mobile (e.g. a different mobile header). *(agreed · MoM 14 Aug 2026, 4. White-Labeling and Customization Boundaries · DI-285)*
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)*
- Modules enabled/disabled per tenant by licence: Ticketing & Booking, Membership, Events, Attractions, Virtual Queue, F&B, Retail, Parking; add-ons (Lost & Found, AI Concierge Chat, multi-language, integrations) toggle the same way and appear automatically as new integrations are built. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-193)*
- Allam: banner, header, footer and background color are CMS-configurable per client, but site structure and navigation flow are fixed and adapt automatically to product configuration (dated, non-dated, seated, membership products surface the right fields). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-119)*
- A "powered by [platform]" footer credit is fixed and not client-editable. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-111)*
- White-label sites share one platform/template but each is configured independently: header, footer, logo, colors, fonts and hero banner are client-editable from the backend. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-108)*

**36 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"appendEntitlementToMedia": {"method":"POST","path":"/media/{mediaCode}/entitlements","contract":"orders","summary":"Add something to a ticket the guest already holds","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AppendEntitlementRequest","responds":"AppendEntitlementResult"},
"completeUpload": {"method":"POST","path":"/media/uploads/{uploadId}/complete","contract":"assets","summary":"Confirm an upload and create the asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaAsset"},
"createBanner": {"method":"POST","path":"/tenant-config/banners","contract":"white-label","summary":"Create a banner","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Banner","responds":"Banner"},
"createCollection": {"method":"POST","path":"/media/collections","contract":"assets","summary":"Create a collection","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Collection"},
"createContentPage": {"method":"POST","path":"/tenant-config/pages","contract":"white-label","summary":"Create a content page","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"ContentPage","responds":"ContentPage"},
"createMenu": {"method":"POST","path":"/menus","contract":"fnb","summary":"Create a menu","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateMenuRequest","responds":"Menu"},
"createPreview": {"method":"POST","path":"/tenant-config/preview","contract":"white-label","summary":"Generate a preview link","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Preview"},
"createPromoBlock": {"method":"POST","path":"/tenant-config/promo-blocks","contract":"white-label","summary":"Create a promotional block","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PromoBlock","responds":"PromoBlock"},
"createUpload": {"method":"POST","path":"/media/uploads","contract":"assets","summary":"Request a signed upload URL","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"UploadTicket"},
"decideProposedAction": {"method":"POST","path":"/proposed-actions/{actionId}/decide","contract":"ai","summary":"Approve or reject a proposal","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProposedAction"},
"deleteBanner": {"method":"DELETE","path":"/tenant-config/banners/{bannerId}","contract":"white-label","summary":"Delete a banner","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"deleteContentPage": {"method":"DELETE","path":"/tenant-config/pages/{pageId}","contract":"white-label","summary":"Delete a content page","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"deleteMediaAsset": {"method":"DELETE","path":"/media/{mediaId}","contract":"assets","summary":"Delete an asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"deletePromoBlock": {"method":"DELETE","path":"/tenant-config/promo-blocks/{promoBlockId}","contract":"white-label","summary":"Delete a promotional block","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"diffConfigVersion": {"method":"GET","path":"/tenant-config/versions/{version}/diff","contract":"white-label","summary":"Compare a version against the working draft","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"against","in":"query","required":null}],"requestBody":null,"responds":"ConfigDiff"},
"getAppIcons": {"method":"GET","path":"/tenant-config/app-icons","contract":"white-label","summary":"Read app icon set","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"AppIcons"},
"getBrandIdentity": {"method":"GET","path":"/tenant-config/brand","contract":"white-label","summary":"Read brand identity","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"BrandIdentity"},
"getExpiringRights": {"method":"GET","path":"/media/rights-expiring","contract":"assets","summary":"Assets whose licence is expiring or expired","permission":"ASSET_LIBRARY_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"withinDays","in":"query","required":null}],"requestBody":null,"responds":"ExpiringMedia"},
"getFeatureToggles": {"method":"GET","path":"/tenant-config/features","contract":"white-label","summary":"Read tenant feature toggles","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"FeatureToggle"},
"getFonts": {"method":"GET","path":"/tenant-config/fonts","contract":"white-label","summary":"Read font configuration","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"FontConfig"},
"getHomepageLayout": {"method":"GET","path":"/tenant-config/homepage","contract":"white-label","summary":"Read homepage layout","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"HomepageLayout"},
"getMediaAsset": {"method":"GET","path":"/media/{mediaId}","contract":"assets","summary":"Read an asset with derivatives and usage","permission":"ASSET_LIBRARY_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaAssetDetail"},
"getMediaEntitlements": {"method":"GET","path":"/media/{mediaCode}/entitlements","contract":"orders","summary":"What is already on this media","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaEntitlements"},
"getMenu": {"method":"GET","path":"/menus/{menuId}","contract":"fnb","summary":"Read a menu with sections and items","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Menu"},
"getModuleEnablement": {"method":"GET","path":"/tenant-config/modules","contract":"white-label","summary":"Read module enablement","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ModuleEnablement"},
"getNavigation": {"method":"GET","path":"/tenant-config/navigation","contract":"white-label","summary":"Read navigation","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"NavigationConfig"},
"getTenantAppStatus": {"method":"GET","path":"/tenant-config/status","contract":"white-label","summary":"App status and recent changes","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"TenantAppStatus"},
"getTenantConfig": {"method":"GET","path":"/tenant-config","contract":"white-label","summary":"Full working configuration","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"version","in":"query","required":null}],"requestBody":null,"responds":"TenantConfig"},
"getTheme": {"method":"GET","path":"/tenant-config/theme","contract":"white-label","summary":"Read colour theme","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"Theme"},
"listBanners": {"method":"GET","path":"/tenant-config/banners","contract":"white-label","summary":"List banners","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"state","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCollections": {"method":"GET","path":"/media/collections","contract":"assets","summary":"List collections","permission":"ASSET_LIBRARY_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Collection"},
"listConfigVersions": {"method":"GET","path":"/tenant-config/versions","contract":"white-label","summary":"Version history","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listContentPages": {"method":"GET","path":"/tenant-config/pages","contract":"white-label","summary":"List custom content pages","permission":"TENANT_CONFIGURE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"categoryCode","in":"query","required":null},{"name":"slug","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMenus": {"method":"GET","path":"/menus","contract":"fnb","summary":"List menus","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":"activeAt","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPromoBlocks": {"method":"GET","path":"/tenant-config/promo-blocks","contract":"white-label","summary":"List promotional blocks","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"PromoBlock"},
"proposeMarketingContent": {"method":"POST","path":"/ai/content-drafts","contract":"ai","summary":"Draft marketing content for a person to edit and apply","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"publishTenantConfig": {"method":"POST","path":"/tenant-config/publish","contract":"white-label","summary":"Publish the working draft","permission":"TENANT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConfigVersion"},
"replaceMediaAsset": {"method":"POST","path":"/media/{mediaId}/replace","contract":"assets","summary":"Replace the file behind an asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaReplaceResult"},
"restoreConfigVersion": {"method":"POST","path":"/tenant-config/versions/{version}/restore","contract":"white-label","summary":"Restore a previous version","permission":"TENANT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TenantConfig"},
"searchMedia": {"method":"GET","path":"/media","contract":"assets","summary":"Search the asset library","permission":"ASSET_LIBRARY_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"tag","in":"query","required":null},{"name":"collectionId","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":"unusedOnly","in":"query","required":null},{"name":"rightsExpiringWithinDays","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"semanticSearch": {"method":"POST","path":"/search","contract":"ai","summary":"Search meaning, not words","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SearchResult"},
"setAppIcons": {"method":"PUT","path":"/tenant-config/app-icons","contract":"white-label","summary":"Set app icons","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AppIcons"},
"setBrandIdentity": {"method":"PUT","path":"/tenant-config/brand","contract":"white-label","summary":"Set logo, favicon and splash","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BrandIdentity","responds":"BrandIdentity"},
"setFeatureToggles": {"method":"PUT","path":"/tenant-config/features","contract":"white-label","summary":"Set feature toggles","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FeatureToggle"},
"setFonts": {"method":"PUT","path":"/tenant-config/fonts","contract":"white-label","summary":"Set fonts","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"FontConfig","responds":"FontConfig"},
"setFooter": {"method":"PUT","path":"/footer","contract":"white-label","summary":"Footer columns, legal links and social","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FooterConfig","responds":"FooterConfig"},
"setHeader": {"method":"PUT","path":"/tenant-config/header","contract":"white-label","summary":"Configure the header","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"HeaderConfig","responds":"HeaderConfig"},
"setHomepageLayout": {"method":"PUT","path":"/tenant-config/homepage","contract":"white-label","summary":"Set homepage section order","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"HomepageLayout","responds":"HomepageLayout"},
"setMaintenanceMode": {"method":"PUT","path":"/tenant-config/status","contract":"white-label","summary":"Enable or clear maintenance mode, and set the live app status","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TenantAppStatus"},
"setMenuSections": {"method":"PUT","path":"/menus/{menuId}/sections","contract":"fnb","summary":"Set menu sections and their item ordering","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Menu"},
"setModuleEnablement": {"method":"PUT","path":"/tenant-config/modules","contract":"white-label","summary":"Enable or disable modules","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ModuleEnablement"},
"setNavigation": {"method":"PUT","path":"/tenant-config/navigation","contract":"white-label","summary":"Set main and overflow navigation","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"NavigationConfig","responds":"NavigationConfig"},
"setTheme": {"method":"PUT","path":"/tenant-config/theme","contract":"white-label","summary":"Set colour theme","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"Theme","responds":"Theme"},
"updateBanner": {"method":"PATCH","path":"/tenant-config/banners/{bannerId}","contract":"white-label","summary":"Amend or activate a banner","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Banner"},
"updateContentPage": {"method":"PUT","path":"/tenant-config/pages/{pageId}","contract":"white-label","summary":"Amend a content page","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"UpdateContentPageRequest","responds":"ContentPage"},
"updateMediaAsset": {"method":"PATCH","path":"/media/{mediaId}","contract":"assets","summary":"Amend metadata, tags or rights","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaAsset"},
"updateMenu": {"method":"PATCH","path":"/menus/{menuId}","contract":"fnb","summary":"Amend a menu","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Menu"},
"updatePromoBlock": {"method":"PATCH","path":"/tenant-config/promo-blocks/{promoBlockId}","contract":"white-label","summary":"Amend a promotional block","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PromoBlock"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessibilitySettings": {"type":"object","description":"BL-065, 2.1.27. **POS and kiosk accessibility, which is a legal obligation in most jurisdictions and was unstated.**\n**A kiosk is the hard case.** A guest with low vision using a website brings their own assistive technology; a guest at a kiosk gets whatever the kiosk offers, so the settings have to be on the device rather than in the browser.\n","properties":{"largeTextAvailable":{"type":"boolean","default":true},"highContrastAvailable":{"type":"boolean","default":true},"simplifiedNavigationAvailable":{"type":"boolean","default":true},"screenReaderSupported":{"type":"boolean","default":true},"reachableHeightModeAvailable":{"type":"boolean","default":false,"description":"**Moves the interface to the lower half of the screen** for a guest using a wheelchair. A kiosk mounted at standing height is unusable otherwise, and no software setting fixes the mounting — this is the mitigation.\n"},"sessionTimeoutMultiplier":{"type":"number","default":1,"description":"**Timeouts are an accessibility barrier nobody counts.** A guest who needs three times as long to read a screen should not lose their basket to a 90-second inactivity timer.\n"}}},
"AppAvailability": {"type":"string","description":"**The sold-out or closed signal (decided 28 September, audit R073).** `open` is the normal state. `soldOut` shows WEB-029's sold-out state across the app while browsing still works; `closed` shows the closed state (a weather closure, a private event). Neither refuses a request on its own: it is what the guest is told, and a sale is still refused by availability where it applies. Set with `setMaintenanceMode`.\n","enum":["open","soldOut","closed"],"default":"open"},
"AppIcons": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["sourceAssetRef","changeScope"],"properties":{"sourceAssetRef":{"type":"string","format":"uuid","description":"The `MediaAsset` id of the 1024×1024 source."},"derived":{"type":"array","readOnly":true,"x-ticvai-derived":"onWrite","description":"Generated by `setAppIcons` from the source, one entry per platform and size — the iOS and Android store sets and the web favicons listed on `setAppIcons` (audit R163).","items":{"type":"object","properties":{"platform":{"type":"string","enum":["ios","android","web"]},"size":{"type":"string"},"assetRef":{"type":"string","format":"uuid"}}}},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Always `buildTime` — icons are baked into the binary."},"liveVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Icon currently shipped. Differs from the draft until the next release."},"requiresRebuild":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onRead","description":"True while the draft's source differs from the icon in `liveVersion`."}}},
"AppendEntitlementRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the new order this creates, and its idempotency key — it must equal the `Idempotency-Key` header."},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["variantId","quantity"],"properties":{"variantId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid","nullable":true}}}},"paymentMethod":{"type":"string","enum":["card","cash","wallet","giftCard","chargeToAccount"]},"note":{"type":"string","maxLength":300},"recordedAt":{"type":"string","format":"date-time"}}},
"AppendEntitlementResult": {"type":"object","x-ticvai-persistence":"none — computed","required":["order","media"],"properties":{"order":{"allOf":[{"$ref":"#/components/schemas/Order"}],"description":"A **new** order. The original is untouched — it was paid, receipted and possibly reported on, and editing it would move yesterday's revenue.\n"},"media":{"allOf":[{"$ref":"#/components/schemas/MediaEntitlements"}],"description":"The full set now on the media, so the cashier can say what the QR does."},"addedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"Banner": {"x-ticvai-persistence":"whitelabel.banner","type":"object","required":["id","title","imageAssetRef","startsAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"title":{"$ref":"#/components/schemas/LocalisedText"},"subtitle":{"$ref":"#/components/schemas/LocalisedText"},"imageAssetRef":{"type":"string","format":"uuid"},"placement":{"type":"string","enum":["homepageHero","homepageBlock","explore","checkout"]},"linkTarget":{"$ref":"#/components/schemas/LinkTarget"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time","nullable":true,"description":"Must follow `startsAt` when set (decided 28 September, audit R163). Null runs the banner with no end."},"state":{"allOf":[{"$ref":"#/components/schemas/ScheduleState"}],"readOnly":true,"x-ticvai-derived":"sweeper","description":"Moved by `updateBanner` between `draft` and `scheduled`, and by the schedule timer from `scheduled` to `active` and `active` to `expired` at `startsAt` and `endsAt`, in the tenant's timezone (`states/schedule.yaml`)."},"sortOrder":{"type":"integer"},"isActive":{"type":"boolean"}}},
"BookingFlow": {"x-ticvai-persistence":"whitelabel.booking_flow","type":"object","description":"**A venue's booking flow (decided 29 September, W12: operators pick their flows, see which steps are required, set their own order).** Made from a `BookingFlowType`; lives in the working draft and reaches guests with `publishTenantConfig`, which copies the venue's flows into the version's snapshot. A product or category names its flow (catalogue `bookingFlowId`); otherwise the venue's default for the type serving its kind applies.\n","required":["flowTypeKey","name"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `createBookingFlowDefinition`."},"flowTypeKey":{"$ref":"#/components/schemas/BookingFlowTypeKey"},"name":{"type":"string","maxLength":80,"description":"Staff-facing, e.g. \"Day pass, date first\". Not shown to guests."},"isDefaultForType":{"type":"boolean","default":false,"description":"At most one per venue and type; setting it takes it from the previous default."},"isEnabled":{"type":"boolean","default":true,"description":"A disabled flow is kept and not published; products naming it fall back to the default."},"steps":{"type":"array","maxItems":30,"description":"Every step of the type, in the venue's order. Filled from the type when left out on create.","items":{"$ref":"#/components/schemas/BookingFlowStep"}},"settings":{"$ref":"#/components/schemas/BookingFlowLevelSettings"},"isValid":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Whether the flow passes `validateBookingFlow`; worked out in the same transaction as each write. `publishTenantConfig` refuses a draft holding an invalid enabled flow."},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `venue` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"BookingFlowConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","description":"**Set per tenant, with a per-venue override (decided 29 September, rev 3 CFG-11).** One tenant with several venues (the Kids Club branches, Coastal Aqua beside Union Arena) needs them to differ. The settings in force at a venue are the tenant's, with that venue's entry in `venueOverrides` laid over them field by field. The guest app resolves them for the venue the guest picked (audit R267); `effectiveForVenueId` on `getBookingFlowConfig` returns them resolved.\n","allOf":[{"$ref":"#/components/schemas/BookingFlowSettings"},{"type":"object","properties":{"venueOverrides":{"type":"array","maxItems":200,"default":[],"description":"Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. An override for a venue later closed is kept and has no effect.","items":{"$ref":"#/components/schemas/BookingFlowVenueOverride"}}}}]},
"BrandIdentity": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","description":"Every `*AssetRef` here is a `MediaAsset` id from the `assets` library (`createUpload` then `completeUpload`), PNG or SVG and at most 2 MB (decided 28 September, audit R270).\n","required":["logoAssetRef"],"properties":{"logoAssetRef":{"type":"string","format":"uuid","description":"The primary logo."},"logoDarkAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"Used on dark backgrounds. Falls back to the primary logo."},"logoVariant":{"type":"string","enum":["light","dark","duotone"],"default":"light","description":"**Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4).** `light` uses `logoAssetRef`, `dark` uses `logoDarkAssetRef` (falling back to the primary logo), and `duotone` the two-colour reading of the primary logo.\n"},"faviconAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"The browser tab icon for the guest web app."},"splashImageAssetRefs":{"type":"array","description":"Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163).","items":{"type":"string","format":"uuid"}},"splashDurationSeconds":{"type":"integer","minimum":0,"maximum":10,"default":3},"splashBackgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"showLoadingIndicator":{"type":"boolean","default":true},"splashChangeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163)."},"introVideoAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"**The optional intro video (decided 29 September, MOB-5).** A video `MediaAsset` from the media library (CMS-010). Streamed, so a change reaches guests with the publish and needs no app build.\n"},"introVideoMode":{"type":"string","enum":["off","firstLaunch","everyLaunch"],"default":"off","description":"When GST-001 plays it full screen. \"Skip introduction\" is always shown. Anything but `off` needs `introVideoAssetRef`, or 400."}}},
"ChangeScope": {"type":"string","description":"Whether a change reaches guests on publish or needs a store release.\n","enum":["runtime","buildTime"]},
"Collection": {"x-ticvai-persistence":"assets.media_collection","type":"object","required":["id","name","assetCount"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string","x-ticvai-unique":"tenant","description":"**Unique per tenant** (decided 28 September, audit R108). A name already used by any collection in the tenant, at any venue or level, is refused with `409 duplicate-code`.\n"},"description":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"parentCollectionId":{"type":"string","format":"uuid","nullable":true},"assetCount":{"type":"integer"},"coverAssetId":{"type":"string","format":"uuid","nullable":true}}},
"ConfigDiff": {"x-ticvai-persistence":"none — computed","type":"object","required":["fromVersion","toVersion","changes"],"properties":{"fromVersion":{"type":"string"},"toVersion":{"type":"string"},"changes":{"type":"array","items":{"type":"object","required":["area","path","changeKind"],"properties":{"area":{"type":"string"},"path":{"type":"string"},"changeKind":{"type":"string","enum":["added","removed","modified"]},"before":{"type":"string","nullable":true},"after":{"type":"string","nullable":true},"changeScope":{"$ref":"#/components/schemas/ChangeScope"}}}}}},
"ConfigVersion": {"x-ticvai-persistence":"whitelabel.config_version","type":"object","required":["version","publishedAt","publishedByPrincipalId","note","isCurrent"],"properties":{"version":{"type":"string"},"publishedAt":{"type":"string","format":"date-time"},"publishedByPrincipalId":{"type":"string","format":"uuid"},"publishedByName":{"type":"string"},"note":{"type":"string"},"isCurrent":{"type":"boolean"},"scheduledFor":{"type":"string","format":"date-time","nullable":true},"contentHash":{"type":"string"},"pendingBuildTimeChanges":{"type":"array","description":"Changes in this version that will not reach guests until the next store release. Surfaced at publish so nobody expects a new icon tomorrow.\n","items":{"type":"object","properties":{"area":{"type":"string"},"description":{"type":"string"},"platforms":{"type":"array","items":{"type":"string","enum":["ios","android","web"]}}}}},"snapshot":{"type":"object","additionalProperties":true,"readOnly":true,"description":"**What this version contained.** The working draft exactly as published, in the shape `getTenantConfig` returns (`TenantConfig`) — so `restoreConfigVersion` has something to copy back and `diffConfigVersion` something to compare. Deliberately an open object here: its shape is `TenantConfig`, and a `$ref` would make it a key to a `tenant_config` row rather than a copy. Written once by `publishTenantConfig` and never changed. Left out of `listConfigVersions` items; a version's content is read with `getTenantConfig?version=`.\n"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"ContentPage": {"x-ticvai-persistence":"whitelabel.content_page","type":"object","required":["id","slug","title","body","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"slug":{"type":"string","pattern":"^[a-z0-9-]+$"},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedRichText"},"isEnabled":{"type":"boolean","default":true,"description":"BL-005. **Enablement is not publication.** A published page that is disabled exists, keeps its URL and its history, and does not render — which is what a tenant wants when a section is seasonal.\n**Unpublishing loses the version; disabling does not.** Collapsing them means a venue turning off its water-park section for winter has to republish it every spring.\n"},"status":{"allOf":[{"$ref":"#/components/schemas/ContentStatus"}],"readOnly":true,"description":"Created as `draft`, published by `publishTenantConfig`, archived through `updateContentPage` (`states/content.yaml`)."},"iconAssetRef":{"type":"string","format":"uuid","nullable":true},"categoryCode":{"type":"string","nullable":true},"sortOrder":{"type":"integer"},"isReferenced":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"True when navigation or the homepage links to this page. Blocks deletion. Maintained by `setNavigation` and `setHomepageLayout` in the same transaction as the links they write."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"ContentStatus": {"type":"string","enum":["draft","published","archived"]},
"CreateMenuRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","outletId"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"outletId":{"type":"string","format":"uuid"},"availability":{"$ref":"#/components/schemas/MenuAvailability"}}},
"EntitlementStatus": {"type":"string","description":"**What the storage layer holds, and what a guest is shown.** `MediaEntitlements` carried only `isValid` and a reason string — a boolean cannot distinguish a ticket that was used from one that expired, was refunded, or was transferred to somebody else, and those are four different conversations at a gate.\nAdded 17 August. `states/entitlement.yaml` had modelled these six since 14 August and the contract had no enum behind it, which the state checker reported correctly for three days.\n","enum":["issued","partiallyConsumed","fullyConsumed","expired","cancelled","surrendered"]},
"ExpiringMedia": {"x-ticvai-persistence":"none — computed","type":"object","required":["assetId","filename","validTo","isExpired","isInUse"],"properties":{"assetId":{"type":"string","format":"uuid"},"filename":{"type":"string"},"thumbnailUrl":{"type":"string","nullable":true},"licensor":{"type":"string","nullable":true},"validTo":{"type":"string","format":"date"},"daysRemaining":{"type":"integer"},"isExpired":{"type":"boolean"},"isInUse":{"type":"boolean","description":"True while `liveUsageCount` is above zero, that is, while live (published) content references the asset (audit R106 (10)). Drafts and collections do not count."},"liveUsageCount":{"type":"integer","description":"References from live (published) content only (audit R106 (10)). Expired and live is the combination that matters."}}},
"FeatureKey": {"type":"string","description":"The feature toggles a tenant can set — one list for `FeatureToggle` and the `setFeatureToggles` body, which took a free string where the response had this enum.\n","enum":["digitalCompanionMode","aiConciergeChat","lostAndFound","pushNotifications","socialSharing","multiLanguage","appleWallet","googlePay","applePay","cashOnDelivery","guestCheckout","uaePassLogin"]},
"FeatureToggle": {"x-ticvai-persistence":"whitelabel.feature_toggle","type":"object","required":["featureKey","isEnabled","changeScope"],"properties":{"featureKey":{"allOf":[{"$ref":"#/components/schemas/FeatureKey"}],"description":"`guestCheckout` is **off by default** (decided 17 September 2026, matrix 2.6.28, placement settled by [ADR-0045](../../docs/adr/0045-every-order-carries-a-proven-contact.md) 18 September): **the venue sets this from the configuration menu**, and it decides which routes the checkout page offers — off, the guest signs in verified at checkout; on, a guest may also check out without an account after proving their contact with a one-time code. **It gates checkout, never the cart.** The kiosk is not governed by it. Rule on `identity` `verifyGuestEmail`.\n"},"displayName":{"type":"string"},"isEnabled":{"type":"boolean"},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Wallet and payment integrations are `buildTime` on native apps — enabling one needs a release, not a publish.\n"},"requiresConfiguration":{"type":"boolean","description":"True where the feature needs credentials or setup elsewhere first."}}},
"FontConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["primaryLatin"],"properties":{"primaryLatin":{"type":"string"},"primaryArabic":{"type":"string","nullable":true,"description":"Required when `ar` is among the tenant's languages (audit R163). A Latin face alone leaves Arabic in a system fallback that will not match.\n"},"secondaryLatin":{"type":"string","nullable":true},"secondaryArabic":{"type":"string","nullable":true,"description":"Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163)."},"customFontAssetRefs":{"type":"array","description":"Uploaded font files, as `MediaAsset` ids.","items":{"type":"string","format":"uuid"}},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"x-ticvai-derived":"onRead","description":"Custom font files are `buildTime`; selecting a bundled face is `runtime`."}}},
"FooterConfig": {"type":"object","x-ticvai-persistence":"whitelabel.footer_config + whitelabel.footer_config_column + whitelabel.footer_config_social_link","description":"BL-002. **`setHeader` and `HeaderConfig` exist and the footer does not**, which looked like symmetry until you notice it is not: **a header is chrome and a footer is a link surface.**\nA footer carries the legal links — terms, privacy, accessibility statement, cookie preferences — and **those are the ones a regulator checks.** Treating it as a mirror of the header would have given it a logo and no way to reach a privacy notice.\n**Where it is stored.** `legalLinks` and `copyrightText` are columns of `whitelabel.footer_config`; each entry of `columns` is a `whitelabel.footer_config_column` row and each entry of `socialLinks` a `whitelabel.footer_config_social_link` row. Part of the working draft (see the header). **In the tenant's own database, not the control plane (decided 28 September, audit R163)**: it moved from `control.footer_config` and its two child tables.\n","required":["id","scopePath"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005), written at `tenant` scope by the server."},"columns":{"type":"array","items":{"type":"object","properties":{"heading":{"type":"string"},"links":{"type":"array","items":{"type":"object","properties":{"label":{"type":"string"},"url":{"type":"string"},"opensCookiePreferences":{"type":"boolean","default":false}}}}}}},"legalLinks":{"type":"object","description":"**Required links, held separately from the free-form columns** — a tenant reorganising their footer must not be able to remove the privacy notice by accident.\n","properties":{"termsUrl":{"type":"string"},"privacyUrl":{"type":"string"},"accessibilityUrl":{"type":"string","nullable":true},"cookiePolicyUrl":{"type":"string","nullable":true}}},"copyrightText":{"type":"string"},"socialLinks":{"type":"array","items":{"type":"object","properties":{"platform":{"type":"string"},"url":{"type":"string"}}}}}},
"HeaderConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["layout"],"properties":{"layout":{"type":"string","enum":["logoLeft","logoCentre","logoWithMenu"]},"showLogo":{"type":"boolean","default":true},"showMenu":{"type":"boolean","default":true},"showNotifications":{"type":"boolean","default":true},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},
"HomepageLayout": {"x-ticvai-persistence":"whitelabel.homepage_section","type":"object","required":["sections"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"sections":{"type":"array","items":{"type":"object","required":["kind","sortOrder","isVisible"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"kind":{"$ref":"#/components/schemas/HomepageSectionKind"},"title":{"$ref":"#/components/schemas/LocalisedText"},"sortOrder":{"type":"integer"},"isVisible":{"type":"boolean"},"contentPageId":{"type":"string","format":"uuid","nullable":true},"maxItems":{"type":"integer","nullable":true,"description":"How many items the section shows. On the mobile Home, `attractions`, `dining`, `whatsOn` and `shop` show 1 or 2 highlights (decided 29 September, MOB-3)."},"heroStyle":{"type":"string","nullable":true,"enum":["carousel","video","poster","split",null],"description":"For `heroBanner` only (decided 29 September, MOB-3)."}}}}}},
"HomepageSectionKind": {"type":"string","description":"**Which module each section needs, proposed, client to correct (decided 28 September, audit R163).** `tickets` needs `ticketsAndBooking`; `whatsOn` needs `events`; `attractions` needs `attractions`; `membership` needs `membership`; `dining` needs `diningAndFnb`; `shop` needs `shop`; `map` needs `map`. `heroBanner`, `quickActions`, `promotions`, `customContent`, `venueOverview` and `spacer` need no module. `venueOverview` (decided 29 September, MOB-3) is the mobile Home's description, opening hours (from `getTenantAppStatus`) and type tiles. `setHomepageLayout` refuses a visible section whose module is not enabled, and `setModuleEnablement` refuses to disable a module a section still needs.\n","enum":["heroBanner","quickActions","tickets","whatsOn","attractions","membership","dining","shop","promotions","map","customContent","venueOverview","spacer"]},
"LanguageConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["languages","defaultLanguage"],"properties":{"languages":{"type":"array","items":{"type":"string","pattern":"^[a-z]{2}$"}},"defaultLanguage":{"type":"string","pattern":"^[a-z]{2}$"},"rtlLanguages":{"type":"array","readOnly":true,"x-ticvai-derived":"onRead","description":"The enabled languages written right to left — those whose Unicode CLDR character order is `right-to-left` (Arabic, `ar`, among them). Not configured; it follows from `languages`.","items":{"type":"string","pattern":"^[a-z]{2}$"}},"translationGaps":{"type":"array","readOnly":true,"description":"Content lacking a version in an enabled language.","items":{"type":"object","properties":{"language":{"type":"string"},"missingCount":{"type":"integer"},"areas":{"type":"array","items":{"type":"string"}}}}}}},
"LinkTarget": {"x-ticvai-persistence":"none — embedded","type":"object","required":["kind"],"properties":{"kind":{"type":"string","enum":["module","contentPage","product","event","externalUrl","appSection","none"],"description":"`appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets."},"moduleKey":{"$ref":"#/components/schemas/ModuleKey"},"appSection":{"type":"string","enum":["home","explore","plan","tickets","map","account","buyTickets"],"description":"Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it."},"contentPageId":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid"},"url":{"type":"string"}}},
"LocalisedRichText": {"x-ticvai-persistence":"none — jsonb column","type":"object","description":"Keyed by language code. Values are sanitised HTML.","additionalProperties":{"type":"string"}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MediaAsset": {"x-ticvai-persistence":"assets.media_asset","type":"object","required":["id","kind","status","filename","contentType","sizeBytes","referenceCount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MediaKind"},"status":{"$ref":"#/components/schemas/MediaStatus"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"title":{"$ref":"#/components/schemas/LocalisedText"},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Required before use in a guest-facing surface. WCAG 2.2 AA."},"width":{"type":"integer","nullable":true},"height":{"type":"integer","nullable":true},"durationSeconds":{"type":"number","nullable":true},"customMetadata":{"type":"object","nullable":true,"additionalProperties":true,"description":"BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"},"sharedWithTenantIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"},"tags":{"type":"array","items":{"type":"string"}},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"url":{"type":"string","description":"Signed and expiring for private assets; stable CDN URL for public ones."},"thumbnailUrl":{"type":"string","nullable":true},"referenceCount":{"type":"integer","description":"How many surfaces reference this asset. Non-zero refuses deletion.\n"},"rights":{"$ref":"#/components/schemas/MediaRights"},"isRightsExpired":{"type":"boolean"},"version":{"type":"integer"},"uploadedByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"MediaAssetDetail": {"x-ticvai-persistence":"assets.media_asset","allOf":[{"$ref":"#/components/schemas/MediaAsset"},{"type":"object","properties":{"derivatives":{"type":"array","description":"Generated from the original, never uploaded separately. A new breakpoint is a re-render rather than a re-upload of everything.\n","items":{"type":"object","properties":{"label":{"type":"string"},"width":{"type":"integer"},"height":{"type":"integer"},"sizeBytes":{"type":"integer"},"url":{"type":"string"}}}},"usage":{"type":"array","description":"Every place this asset is referenced.","items":{"$ref":"#/components/schemas/MediaUsage"}},"collections":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"}}}},"previousVersions":{"type":"array","items":{"type":"object","properties":{"version":{"type":"integer"},"replacedAt":{"type":"string","format":"date-time"},"replacedByPrincipalId":{"type":"string","format":"uuid"}}}}}}]},
"MediaEntitlements": {"type":"object","x-ticvai-persistence":"none — projection over entitlement and scan history","required":["mediaCode","isValid","entitlements"],"properties":{"mediaCode":{"type":"string"},"mediaKind":{"type":"string","enum":["qr","wristband","card","nfc","mobilePass"]},"subjectId":{"type":"string","format":"uuid","nullable":true},"isValid":{"type":"boolean"},"invalidReason":{"type":"string","nullable":true},"canAcceptMore":{"type":"boolean","description":"False where the media has been surrendered, expired or blocked. A cashier should know before taking money, not after.\n"},"entitlements":{"type":"array","items":{"type":"object","properties":{"entitlementId":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","enum":["admission","locker","fnb","retail","parking","rental","experience","membership"]},"orderId":{"type":"string","format":"uuid"},"addedAt":{"type":"string","format":"date-time"},"status":{"allOf":[{"$ref":"#/components/schemas/EntitlementStatus"}],"description":"**Replaced `isRedeemed` on 17 August.** A boolean could not distinguish a ticket that was used from one that expired, was refunded, or was transferred — four different conversations at a gate, and the steward could see only \"not valid\".\n"},"entriesUsed":{"type":"integer"},"entriesAllowed":{"type":"integer","nullable":true},"redeemedAt":{"type":"string","format":"date-time","nullable":true},"transferredToSubjectId":{"type":"string","format":"uuid","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true}}}}}},
"MediaKind": {"type":"string","enum":["image","video","audio","document","vector","font","archive"]},
"MediaReplaceResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["asset","affectedSurfaces"],"properties":{"asset":{"$ref":"#/components/schemas/MediaAsset"},"affectedSurfaces":{"type":"integer","description":"How many surfaces now show the new file."},"liveSurfaces":{"type":"integer","description":"Of those, how many are published to guests right now."},"derivativesRegenerating":{"type":"boolean"}}},
"MediaRights": {"x-ticvai-persistence":"none — embedded in asset","type":"object","description":"Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item.\n","properties":{"licenceKind":{"type":"string","enum":["owned","royaltyFree","rightsManaged","creativeCommons","editorialOnly","unknown"]},"licensor":{"type":"string","nullable":true},"licenceReference":{"type":"string","nullable":true},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"permittedUses":{"type":"array","items":{"type":"string","enum":["web","print","socialMedia","inVenue","advertising","internal"]}},"attributionRequired":{"type":"boolean","default":false},"attributionText":{"type":"string","nullable":true},"permittedTerritories":{"type":"array","items":{"type":"string"},"description":"ISO country or region codes. **Empty means unrestricted, which is a claim rather than an absence** — an unknown territory and a worldwide licence are not the same thing, and `licenceKind: unknown` is how the second is said.\n"},"permittedChannels":{"type":"array","items":{"type":"string"},"description":"Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route.\n"},"modelReleaseHeld":{"type":"boolean","default":false},"renewalOwner":{"type":"string","format":"uuid","nullable":true}}},
"MediaStatus": {"type":"string","enum":["processing","ready","quarantined","failed","archived"]},
"MediaUsage": {"x-ticvai-persistence":"assets.media_usage","type":"object","description":"One place an asset is used. **`surface: product` is written by catalogue** for each item of `Product.media` (decided 29 September, rev 3 23SEP-4): `referenceId` is the product id and `isLive` is true while the product is listed to guests, which is what stops an asset in use on a ticket card being archived from under it.\n","required":["surface","referenceId"],"properties":{"extractedText":{"type":"string","description":"**Text pulled out of an uploaded document**, after extraction. The generic retrieval path for anything a tenant uploads — a PDF nobody can search is a PDF nobody reads.\n"},"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"surface":{"type":"string","enum":["tenantBranding","homepageBanner","promoBlock","contentPage","product","event","menuItem","merchandise","workOrder","incident","inspection","campaign"]},"referenceId":{"type":"string"},"label":{"type":"string"},"isLive":{"type":"boolean","description":"True where the referencing surface is published to guests."}}},
"Menu": {"x-ticvai-persistence":"fnb.menu","type":"object","required":["id","code","name","outletId","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"outletId":{"type":"string","format":"uuid"},"availability":{"$ref":"#/components/schemas/MenuAvailability"},"sections":{"type":"array","items":{"$ref":"#/components/schemas/MenuSection"}},"isActive":{"type":"boolean"},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `MenuVersion.version` live now. Null for a menu never published."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"MenuAvailability": {"x-ticvai-persistence":"none — embedded in menu","type":"object","description":"When this menu is in force. Absent means always. Days, times and dates are all read in the Region's time zone, not UTC.","properties":{"daysOfWeek":{"type":"array","items":{"type":"integer","minimum":0,"maximum":6}},"startTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Wall-clock time, in the Region's time zone."},"endTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Wall-clock time, in the Region's time zone."},"validFrom":{"type":"string","format":"date","nullable":true,"description":"Calendar day, in the Region's time zone, not UTC."},"validTo":{"type":"string","format":"date","nullable":true,"description":"Calendar day, in the Region's time zone, not UTC."}}},
"MenuItem": {"x-ticvai-persistence":"fnb.menu_item","type":"object","required":["id","productVariantId","name","price","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"productVariantId":{"type":"string","format":"uuid","description":"The catalogue variant this item sells. Pricing and tax come from there — a menu is a presentation of the catalogue, not a second catalogue.\n"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"sortOrder":{"type":"integer"},"modifierGroupIds":{"type":"array","items":{"type":"string","format":"uuid"}},"stationId":{"type":"string","format":"uuid","nullable":true},"menuSectionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The section the item sits in, set by `setMenuSections` and `applyMenuActions` (`moveSection`)."},"isStockTracked":{"type":"boolean","description":"True where a recipe exists. Stock-tracked items cannot be sold offline."},"isAvailable":{"type":"boolean"},"unavailableReason":{"type":"string","nullable":true},"restoreAt":{"type":"string","format":"date-time","nullable":true,"description":"When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand."},"preparationMinutes":{"type":"integer","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}}}},
"MenuSection": {"x-ticvai-persistence":"fnb.menu_section","type":"object","required":["code","name","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string"},"name":{"type":"string"},"sortOrder":{"type":"integer"},"items":{"type":"array","description":"The section's items, in sale-board order. An item's membership is `MenuItem.menuSectionId`.","items":{"$ref":"#/components/schemas/MenuItem"}}}},
"MinimumAppVersion": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n","properties":{"ios":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"},"android":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"}}},
"ModuleEnablement": {"x-ticvai-persistence":"whitelabel.module_enablement","type":"object","required":["moduleKey","isLicensed","isEnabled"],"properties":{"moduleKey":{"$ref":"#/components/schemas/ModuleKey"},"displayName":{"type":"string"},"isLicensed":{"type":"boolean","description":"From the tenant's subscription. False makes enablement impossible."},"isEnabled":{"type":"boolean"},"referencedBy":{"type":"array","readOnly":true,"x-ticvai-derived":"onWrite","description":"Navigation items and homepage sections pointing at this module. Maintained by `setNavigation` and `setHomepageLayout` in the same transaction as the links they write.","items":{"type":"string"}}}},
"ModuleKey": {"type":"string","enum":["ticketsAndBooking","membership","events","attractions","virtualQueue","diningAndFnb","shop","parking","gamification","photoGallery","wallet","loyalty","lostAndFound","map","visitPlanner"],"description":"`visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown."},
"NavigationConfig": {"x-ticvai-persistence":"whitelabel.navigation_item","type":"object","description":"**The mobile tab set is venue configuration (decided 29 September, MOB-1; 29 September brief decision 6).** Before a tenant saves its own, `bottomNavigation` is Home, Explore, Plan and Tickets (each an `appSection` link), with the Buy tickets button beside them; Map is an optional tab. Plan is left out while `visitPlanner` is off.\n","required":["kind","items"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"kind":{"type":"string","enum":["bottomNavigation","drawer","tabs"]},"items":{"type":"array","maxItems":12,"items":{"type":"object","required":["label","target","isVisible","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"label":{"$ref":"#/components/schemas/LocalisedText"},"icon":{"type":"string"},"target":{"$ref":"#/components/schemas/LinkTarget"},"isVisible":{"type":"boolean","description":"At most five may be visible in bottom navigation; the rest overflow."},"sortOrder":{"type":"integer"}}}},"buyButton":{"type":"object","nullable":true,"description":"**The persistent Buy tickets button (decided 29 September, MOB-2).** On every screen of the mobile app except the booking and checkout steps; it opens GST-003. Read with `bottomNavigation`.\n","properties":{"style":{"type":"string","enum":["raised","floating","flat","hidden"],"default":"raised","description":"`raised` sits in the centre of the tab bar, as the v4 prototype shows; `hidden` turns it off."},"label":{"$ref":"#/components/schemas/LocalisedText"}}}}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Preview": {"x-ticvai-persistence":"none — short-lived, cache only","type":"object","required":["previewId","url","expiresAt"],"properties":{"previewId":{"type":"string","format":"uuid"},"url":{"type":"string"},"platform":{"type":"string","enum":["ios","android","web"]},"theme":{"type":"string","enum":["light","dark"]},"language":{"type":"string","pattern":"^[a-z]{2}$"},"expiresAt":{"type":"string","format":"date-time"}}},
"PromoBlock": {"x-ticvai-persistence":"whitelabel.promo_block","type":"object","required":["id","title"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"title":{"$ref":"#/components/schemas/LocalisedText"},"description":{"$ref":"#/components/schemas/LocalisedText"},"iconAssetRef":{"type":"string","format":"uuid","nullable":true},"promotionId":{"type":"string","format":"uuid","nullable":true,"description":"Presentation only. A block may point at a promotion; it does not create or price one.\n"},"linkTarget":{"$ref":"#/components/schemas/LinkTarget"},"startsAt":{"type":"string","format":"date-time","nullable":true},"endsAt":{"type":"string","format":"date-time","nullable":true,"description":"Must follow `startsAt` when both are set (decided 28 September, audit R163)."},"state":{"allOf":[{"$ref":"#/components/schemas/ScheduleState"}],"readOnly":true,"x-ticvai-derived":"sweeper","description":"Moved by the schedule timer at `startsAt` and `endsAt`, in the tenant's timezone, as for `Banner.state`. Once `active` or `expired` the block may only be withdrawn (audit R163)."},"sortOrder":{"type":"integer"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"ScheduleState": {"type":"string","enum":["draft","scheduled","active","expired"]},
"SearchResult": {"type":"object","x-ticvai-persistence":"none — computed","properties":{"kind":{"type":"string"},"id":{"type":"string"},"title":{"type":"string"},"excerpt":{"type":"string"},"relevance":{"type":"number"},"collectionId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"assetId":{"type":"string","format":"uuid","nullable":true,"description":"For kind `media`, the asset (29 September, build; 23.1.6)."},"mediaType":{"type":"string","nullable":true,"enum":["image","video","audio","document"]},"matchedOn":{"type":"string","nullable":true,"enum":["title","description","tags","aiDescription"],"description":"Which text the match came from, so a wrong hit can be traced to a wrong tag."}}},
"TenantAppStatus": {"x-ticvai-persistence":"none — computed","type":"object","description":"Computed on read. The published fields come from the current `ConfigVersion`, the maintenance fields from the tenant's `tenant_config` row (`setMaintenanceMode`), and the draft fields from the working draft. **Fields marked staff only are left out of a response to a caller without a staff session** (`getTenantAppStatus`).\n","required":["tenantId","isPublished","isInMaintenance"],"properties":{"tenantId":{"type":"string","format":"uuid"},"isPublished":{"type":"boolean","x-ticvai-derived":"onRead","description":"True once any version has been published."},"publishedVersion":{"type":"string","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"draftVersion":{"type":"string","description":"Staff only."},"hasUnpublishedChanges":{"type":"boolean","x-ticvai-derived":"onRead","description":"Staff only. The working draft differs from the current version's `snapshot`."},"activeModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isEnabled` true."},"licensedModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isLicensed` true."},"activePageCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. Content pages that are `published` and enabled."},"isInMaintenance":{"type":"boolean"},"maintenanceMessage":{"$ref":"#/components/schemas/LocalisedText"},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"$ref":"#/components/schemas/MinimumAppVersion"},"contact":{"$ref":"#/components/schemas/VenueContact"},"availability":{"$ref":"#/components/schemas/AppAvailability"},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"What the sold-out or closed screen says (WEB-029). Null shows the default wording."},"venues":{"type":"array","maxItems":200,"x-ticvai-derived":"onRead","description":"**Public: the venues a guest can pick** (decided 28 September, audit R267; schema named 29 September, readiness close-out, our build plan). The source of the venue picker on WEB-001 and GST-001, returned with or without a session. **Published only**: a venue is listed when its scope node is active (`tenancy.OrgUnit.isActive`) and it is in the tenant's current published `ConfigVersion`; a venue added or reactivated since the last publish appears after the next publish, and a draft never reaches a guest. Ordered by `name`. Empty when nothing is published.\n","items":{"type":"object","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid","description":"**The venue's scope node** (`tenancy.OrgUnit.id`, level venue): what every guest screen that declares `venueId` `from: session` reads once the guest picks it."},"name":{"type":"string","maxLength":200,"description":"The venue's name (`tenancy.OrgUnit.name`)."},"city":{"type":"string","maxLength":120,"nullable":true,"description":"Shown under the name so two venues with similar names can be told apart."},"openingHoursToday":{"type":"object","nullable":true,"description":"Today's opening hours in the venue's time zone, from `tenancy.VenueSettings` opening hours. Null when the venue is closed today or has none set.","properties":{"opens":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"},"closes":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"}}}}}},"whatsNew":{"type":"array","maxItems":10,"x-ticvai-derived":"onRead","description":"**Public: the guest \"what's new\"** (decided 29 September, rev 3 GAP-B2). Newest first, at most 10, from `platform-ops.Release.guestReleaseNotes` of the releases the tenant's cell has received; a release with no guest notes is skipped. Returned with or without a staff session.\n","items":{"type":"object","required":["version","publishedAt","notes"],"properties":{"version":{"type":"string","description":"The release version."},"publishedAt":{"type":"string","format":"date-time","description":"When the release reached the tenant's cell."},"notes":{"$ref":"#/components/schemas/LocalisedText"}}}},"recentChanges":{"type":"array","description":"Staff only. Names the principal behind each change, so it never reaches a public response.","items":{"type":"object","properties":{"area":{"type":"string"},"description":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"}}}}}},
"TenantConfig": {"x-ticvai-persistence":"whitelabel.tenant_config","type":"object","description":"**The tenant's working draft**, one row per tenant (see the header). Published versions are `ConfigVersion.snapshot`, not further rows here.\n**Only `tenantId` and `version` are required**, because the draft is built one part at a time: the first `set*` call creates the row with that part alone. A part that is still unset is what `validateTenantConfig` reports (`missingRequiredAsset` and the like) and what blocks `publishTenantConfig` — a storage rule that every part exist would stop the first save.\n","required":["tenantId","version"],"properties":{"tenantId":{"type":"string","format":"uuid"},"version":{"type":"string","description":"The draft's working version label; the published one is `ConfigVersion.version`."},"isDraft":{"type":"boolean","readOnly":true,"description":"True for the working draft, which is the only row."},"brand":{"$ref":"#/components/schemas/BrandIdentity"},"appIcons":{"$ref":"#/components/schemas/AppIcons"},"bookingFlow":{"$ref":"#/components/schemas/BookingFlowConfig"},"bookingFlows":{"type":"array","readOnly":true,"x-ticvai-derived":"onRead","description":"Every venue's booking flows in the draft (`whitelabel.booking_flow`), so a publish snapshots them with the rest (decided 29 September, W12).","items":{"$ref":"#/components/schemas/BookingFlow"}},"theme":{"$ref":"#/components/schemas/Theme"},"fonts":{"$ref":"#/components/schemas/FontConfig"},"footer":{"$ref":"#/components/schemas/FooterConfig"},"notificationBranding":{"type":"object","nullable":true,"description":"BL-003. **`marketing-crm` holds the templates and nothing said whose identity they wear.** A message sent on behalf of a venue carries that venue's sender name, reply-to and logo — **an operational alert arriving from `noreply@ticvai.com` is one a guest marks as spam.**\nResolved on the template at send time rather than duplicated per template.\n","properties":{"senderName":{"type":"string"},"replyToEmail":{"type":"string","format":"email"},"smsSenderId":{"type":"string","nullable":true},"whatsappBusinessId":{"type":"string","nullable":true},"logoAssetId":{"type":"string","format":"uuid","nullable":true}}},"enabledPaymentMethods":{"type":"array","nullable":true,"description":"BL-004. **`FeatureToggle` could turn Apple Pay on and could not say which cards a tenant accepts.** Resolved against `orders.PaymentProvider.supportedMethods` — the tenant's choice within what the gateway offers, and **a tenant enabling a method their provider does not support should fail here rather than at checkout.**\n","items":{"type":"string"}},"accessibility":{"$ref":"#/components/schemas/AccessibilitySettings"},"header":{"$ref":"#/components/schemas/HeaderConfig"},"navigation":{"$ref":"#/components/schemas/NavigationConfig"},"homepage":{"$ref":"#/components/schemas/HomepageLayout"},"modules":{"type":"array","items":{"$ref":"#/components/schemas/ModuleEnablement"}},"features":{"type":"array","items":{"$ref":"#/components/schemas/FeatureToggle"}},"languages":{"$ref":"#/components/schemas/LanguageConfig"},"updatedAt":{"type":"string","format":"date-time"},"isInMaintenance":{"type":"boolean","default":false,"description":"Written by `setMaintenanceMode`; read by `getTenantAppStatus`."},"maintenanceMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The message on the branded maintenance screen."},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"allOf":[{"$ref":"#/components/schemas/MinimumAppVersion"}],"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"contact":{"allOf":[{"$ref":"#/components/schemas/VenueContact"}],"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"availability":{"allOf":[{"$ref":"#/components/schemas/AppAvailability"}],"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"venues":{"type":"array","x-ticvai-derived":"onRead","description":"The tenant's active venues, for the guest venue picker on WEB-001 and GST-001 (decided 28 September, audit R267). Public: returned without a session and cached with the rest of the response. Read from `tenancy` venues; a closed or archived venue is left out.\n","items":{"type":"object","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid"},"name":{"$ref":"#/components/schemas/LocalisedText"},"city":{"type":"string","nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Today's hours as shown to a guest, e.g. \"10:00 to 22:00\"."}}}}}},
"Theme": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["primaryColour","secondaryColour","backgroundColour","textColour"],"properties":{"primaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"secondaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"accentColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"textColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"darkMode":{"type":"object","description":"Optional dark variant. Derived from the light theme when absent.","properties":{"primaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"textColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},"cornerRadius":{"type":"integer","minimum":0,"maximum":32,"description":"The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). Its named palettes, font pairs and background tones are presets over the colours here and `FontConfig`, not stored values."},"surfaceStyle":{"type":"string","enum":["glass","solid"],"default":"glass","description":"Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3)."},"buttonStyle":{"type":"string","enum":["solid","outline","pill"],"default":"solid","description":"Button shape (decided 29 September, rev 3 CFG-3)."},"componentColours":{"type":"object","description":"**Colours for single interactive elements (decided 17 September, M17-11).** Each is optional and falls back to the theme colours. Every pair passes the same contrast check as the theme (`ContrastProblem`), or `setTheme` refuses it with 400. The guest flow stays the standard one; only the colours change.\n","properties":{"primaryCta":{"$ref":"#/components/schemas/ThemeComponentColour"},"payButton":{"$ref":"#/components/schemas/ThemeComponentColour"},"addToCart":{"$ref":"#/components/schemas/ThemeComponentColour"},"buyTicketsButton":{"$ref":"#/components/schemas/ThemeComponentColour"},"link":{"$ref":"#/components/schemas/ThemeComponentColour"},"badge":{"$ref":"#/components/schemas/ThemeComponentColour"}}}}},
"ThemeComponentColour": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","properties":{"background":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"text":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},
"UpdateContentPageRequest": {"x-ticvai-persistence":"none — request only; the fields land on whitelabel.content_page","type":"object","description":"The body of `updateContentPage`: the fields a tenant edits. `id`, `isReferenced` and `scopePath` are the server's, and `status` moves only to `archived` here — publishing is `publishTenantConfig` (`states/content.yaml`).\n","required":["slug","title","body"],"properties":{"slug":{"type":"string","pattern":"^[a-z0-9-]+$"},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedRichText"},"isEnabled":{"type":"boolean","default":true},"iconAssetRef":{"type":"string","format":"uuid","nullable":true},"categoryCode":{"type":"string","nullable":true},"sortOrder":{"type":"integer"},"status":{"allOf":[{"$ref":"#/components/schemas/ContentStatus"}],"description":"Only `archived` is taken — send it to withdraw a published page or abandon a draft (`states/content.yaml`). Any other value is a 400 `validation`. Omit to leave the status as it is."}}},
"UploadTicket": {"x-ticvai-persistence":"assets.media_upload","type":"object","required":["uploadId","uploadUrl","method","expiresAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"uploadId":{"type":"string","format":"uuid"},"uploadUrl":{"type":"string","description":"Signed. PUT the file here, then confirm with `/complete`."},"method":{"type":"string","enum":["PUT","POST"]},"headers":{"type":"object","additionalProperties":{"type":"string"}},"maxSizeBytes":{"type":"integer"},"expiresAt":{"type":"string","format":"date-time"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"venueId":{"type":"string","format":"uuid","nullable":true},"assetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The asset this upload became — created by `completeUpload`, or the asset whose file `replaceMediaAsset` swapped. Null while the transfer is outstanding.\n"}}},
"VenueContact": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n","properties":{"phone":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true},"whatsapp":{"type":"string","nullable":true},"address":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Prose, as the guest reads it. The bookable hours are the catalogue's."}}}
}
```
