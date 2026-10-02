# P01-system-states-01 — P01 · System States

**1 screens · 2 operations · 18 schemas · 0 permissions**

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

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
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

## The processes these screens belong to

Written by the owner of each process (`handoff/design-notes/`). Read before any screen: it says how the process runs end to end and which words the screens must use.

### White Label & CMS

A tenant (one operator, one or many venues) brands and arranges its own guest surfaces, the guest web (P01), the guest app (P02) and the kiosk (P05), from the Venue CMS (P13, a section of the Venue Management app), and TICVAI platform staff can do the same from the console (P09 ADM-016..018) only under a time-boxed grant into the tenant. Everything is configuration over a fixed structure: the guest flow, the page structure and the components are TICVAI's and stay the same for every tenant; the tenant chooses graphics, colours, fonts, which modules and tabs appear, the order of homepage sections and booking steps within allowed limits, copy in each language, and its domain. It never adds components. Work happens in ONE working draft per tenant; nothing a guest sees changes until a person with TENANT_PUBLISH publishes the draft as an immutable version (with a note), and a rollback is restore into the draft, review the diff, then publish, never one click. Three things are deliberately outside the draft and take effect at once: the live app status (maintenance, minimum app version, contact, sold out or closed), a venue's Help me choose publish, and policies (each save is a new version). Build-time parts (app icons, native splash, custom font files, wallet and payment integrations) reach guests only with a new store build, which the client publishes under its own Apple and Google accounts (CMS-104). Staff surfaces (POS, scanner, staff app, kitchen display) never take tenant branding; every guest surface carries the "Powered by TICVAI" credit, a toggle that is on by default (decided 2 October 2026, CHG-NOTE-009; DI-297 amended). Arabic is a first-class layout: enabling `ar` requires an Arabic font, the whole layout mirrors (numbers, times, codes and logos do not), and every authored text is a per-language value. The step-based Site Builder (CMS-102) walks a new tenant through seven steps from a venue-type preset so that a logo, four colours and a publish are enough for a working site in about 30 minutes; every step opens the full screen for its details. Vocabulary below; the element-by-element model follows; inputToOutput at the end gives worked examples.
*(source: contracts/satellite/white-label.yaml#/info; DI-223; DI-285; DI-111; DI-297; DI-296; DI-298; DI-997; DI-998; DI-1014; R139; R073; F22 step 5; F22 step 6; docs/architecture/rtl-and-theming.md)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Draft | The tenant's one working configuration. Every Save writes it; guests never see it. | Staging, Unsaved, Pending | contracts/satellite/white-label.yaml#/info |
| Publish | Make the draft the live version guests read, with a note. Needs TENANT_PUBLISH. | Go live, Deploy, Push, Save and publish | contracts/satellite/white-label.yaml#publishTenantConfig |
| Save | Write to the draft. Never publishes. | Apply, Update live | contracts/satellite/white-label.yaml#/info |
| Version | An immutable published snapshot, numbered, with who published it and the note. | Release, Revision, Backup | contracts/satellite/white-label.yaml#/components/schemas/ConfigVersion |
| Restore into draft | Copy an old version back into the draft. Publishes nothing. | Roll back, Revert, Undo | R139 |
| Live now | The changes that bypass the draft and apply at once (maintenance, availability, minimum app version, contact, Help me choose publish, policies). | Instant publish | contracts/satellite/white-label.yaml#setMaintenanceMode |
| Needs an app update | A build-time change (app icon, native splash, uploaded font, wallet or payment integration) that reaches app users only with a new store build. | Rebuild required, Build-time, Pending release | contracts/satellite/white-label.yaml#/components/schemas/ChangeScope |
| Theme | The tenant's colours, corner radius, surfaces and buttons. | Skin, Template, Style sheet | contracts/satellite/white-label.yaml#/components/schemas/Theme |
| Booking flow | The ordered steps a guest goes through to book one kind of product at one venue. | Checkout flow, Journey, Funnel, Wizard | contracts/satellite/white-label.yaml#/components/schemas/BookingFlow |
| Step | One stage of a booking flow (Date, Time, Tickets, Extras, Payment...). Marked Required, Optional or Conditional. | Page, Stage, Screen | contracts/satellite/white-label.yaml#/components/schemas/BookingFlowStepKey |
| Help me choose | The venue's short set of questions that filters the products shown. Never a consent step. | Quiz, Experience builder, Wizard, Recommender | DI-1005 |
| Module | A licensed product area a tenant switches on for guests (Dining, Shop, Map...). Off means hidden, not greyed. | Plugin, App, Feature | contracts/satellite/white-label.yaml#setModuleEnablement |
| Feature | A finer switch inside the guest app (guest checkout, AI concierge, Apple Wallet...). | Module, Add-on | contracts/satellite/white-label.yaml#setFeatureToggles |
| Buy tickets | The persistent button in the guest app that opens GST-003, and its label. | Book now, Shop, Purchase | DI-1081 |
| Powered by TICVAI | The platform credit on every guest surface; a toggle, on by default, off only where the venue's licence allows. | Built by TICVAI, Made by TICVAI | DI-297 / decided 2 October 2026 by Chinmay (CHG-NOTE-009) |
| Site Builder | The seven-step guided set-up (CMS-102). | Wizard, Onboarding, Setup assistant | DI-997 |
| Venue override | A booking setting one venue sets differently from the tenant; everything else is inherited. | Exception, Custom setting | DI-1063 |
| Sold out today / Closed | The two availability signals guests see; sold out means come another day, closed means the venue is not open. | Unavailable, Error | R073 |
| Maintenance | The tenant-branded page shown while the guest web and app are switched off, with when they are expected back. | Down, Outage, Offline | contracts/satellite/white-label.yaml#setMaintenanceMode |
| Domain | The web address the tenant's guests use; Verify proves the tenant controls it before a certificate is issued. | URL, Site address, DNS | contracts/satellite/white-label.yaml#claimCustomDomain |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `WEB-029` | Error / Sold Out / Maintenance | A | 0 | 48 | 8 | 0 | 1 | 2 | guest | review (client-verified) |

## Thin screens in this batch

**WEB-029 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `WEB-029` Error / Sold Out / Maintenance

**Say what is wrong in a way that tells the person whether to wait or leave.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | System States · wave 1 · needs the `core` module |
| Block | Block A · ticket #17819 (APP-WEB-WEB-029) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | statusTracker (compact density): `getTenantAppStatus` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **The offline banner shows instead of this page.** Being offline is the guest's connection, not the venue's — an error or maintenance page shown for a dropped signal tells a guest the venue is down. |
| Opens with | nothing: it opens on its own |
| Route | `/system-states/error-sold-out-maintenance` |

**What the spec says about it.** Tenant-branded. An unbranded error page inside a tenant's storefront reads as the tenant's failure, not ours. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Bound 28 September** — sold out and closed come from `getTenantAppStatus.availability` (`open`, `soldOut`, `closed`) and `availabilityMessage` (decided 28 September, audit R073 (f)). The forced upgrade (`minimumAppVersion`) is the app's alone, since a website is always the current version.

**From the White Label & CMS process.** The branded page that tells a guest whether to wait or leave: maintenance (come back at a time), sold out today (come another day), closed (the venue is not open), or the platform not answering. Always in the tenant's brand from the last configuration the browser holds; never a generic error.

**Fixed on main** (the package already carries these; draw what it says): The screen has no maintenance state (isInMaintenance, maintenanceMessage, expectedBackAt) though its name and the maintenance operation … (CHG-SGU-022); The prototype's sold-out page offers Join the waitlist, which this screen cannot call. (CHG-SGU-022).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Closed for maintenance** (banner, from `getPublishedTenantConfig`): The main case: `isInMaintenance` with its message and the expected-back time ("Back at 14:00"), set live on CMS-001 (DI-215).

| Shows | Format | Notes |
|---|---|---|
| Published version | text | The `ConfigVersion.version` this answer was read from; a client holding the same version keeps its copy. |
| Published at | 1 Oct 2026, 14:30 | — |
| Brand | grouped details | Every `*AssetRef` here is a `MediaAsset` id from the `assets` library (`createUpload` then `completeUpload`), PNG or SVG and at most 2 MB … |
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
| Show powered by | yes / no (icon or chip) | "Powered by TICVAI", a configuration toggle, on by default (Chinmay, 2 October, workbook Q160 and the pre-apply round; consistent with … |
| App icons | grouped details | — |
| Source image | the image or video | The `MediaAsset` id of the 1024×1024 source. |
| Derived | list or chips (count when long) | Generated by `setAppIcons` from the source, one entry per platform and size — the iOS and Android store sets and the web favicons listed on … |
| Platform | chip: Ios, Android, Web | — |
| Size | text | — |

**The tenant app status** (detail panel, from `getTenantAppStatus`)

| Shows | Format | Notes |
|---|---|---|
| Is published | yes / no (icon or chip) | True once any version has been published. |
| Published version | text | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Is in maintenance | yes / no (icon or chip) | — |
| Maintenance message | in the reader's language | — |
| Expected back at | 1 Oct 2026, 14:30 | — |
| Availability | chip: Open, Sold out, Closed | The sold-out or closed signal (decided 28 September, audit R073). `open` is the normal state. |
| Availability message | in the reader's language | What the sold-out or closed screen says (WEB-029). Null shows the default wording. |

**Sold out or closed today** (banner, from `getTenantAppStatus`): **From `getTenantAppStatus.availability`** (`open`, `soldOut`, `closed`) and its `availabilityMessage`, set live from CMS-001 through `setMaintenanceMode` (decided 28 September, audit R073 (f)). `soldOut` and `closed` read differently: sold out means come another day, closed means the venue is not open. Nothing shows while it is `open`.

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

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Maintenance**: The tenant's maintenance message and "Expected back at 22:00" in the guest's time format; no booking actions; contact links. *(source: contracts/satellite/white-label.yaml#setMaintenanceMode)*
- **Sold out today**: The tenant's availability message and a date picker for another day; browsing still works. *(source: R073; contracts/satellite/white-label.yaml#/components/schemas/AppAvailability)*
- **Closed**: The message and the opening hours from contact. *(source: R073)*
- **Platform not answering**: When the status call fails or times out; "We can't reach the booking service right now", retry, and contact; uses the cached brand. *(source: screens/P01-guest-web-storefront.yaml#WEB-029)*

**Data it reads**: `getTenantAppStatus` (onLoad, from page inventory); `getPublishedTenantConfig` (onLoad, Maintenance, message and expected-back time, readable …)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | — |
| Error (`?state=error`) | **This screen is the error state.** It distinguishes sold out, closed, and platform unavailable — three different things a guest must not confuse, because only one means come back later |
| Empty, first run (`?state=emptyFirstRun`) | — |
| Permission denied (`?state=emptyNoAccess`) | **Nothing here needs a sign-in** (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-2)): the screen reads only what the tenant has published, which is public, so there is no no-access case. A host that belongs to no tenant shows the platform's neutral holding page. |
| Offline (`?state=offline`) | **The offline banner shows instead of this page.** Being offline is the guest's connection, not the venue's — an error or maintenance page shown for a dropped signal tells a guest the venue is down. |
| Sold out (`?state=soldOut`) | **Sold out today.** `getTenantAppStatus.availability` is `soldOut`: the page says so with the tenant's `availabilityMessage` and offers another day, never a generic error (decided 28 September, audit R073 (f)). |
| Closed (`?state=closed`) | **Closed.** `getTenantAppStatus.availability` is `closed`: the page says the venue is not open, with the tenant's `availabilityMessage` and the opening hours from `contact` (decided 28 September, audit R073 (f)). |
| Maintenance (`?state=maintenance`) | The venue's maintenance message and when it expects to be back; one way onward (try again at that time). Set live on CMS-001, never published. |

#### Edge cases to draw

- **Guest's own connection drops**: The offline banner, never this page. *(source: screens/_guest-pairs.yaml)*

#### Consistency with other screens

- Match `GST-047`: The same four states and wording; the app adds the forced update.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
maintenance:
  en: We're adding new slides. Back at 22:00 tonight.
  ar: نضيف منزلقات جديدة. نعود الساعة 22:00 الليلة.
soldOut:
  en: Today is sold out. Tomorrow has space from AED 249.
  ar: نفدت تذاكر اليوم. تتوفر أماكن غدًا ابتداءً من 249 درهم.
```

#### Permissions

- `getTenantAppStatus` → no permission · device, guest, staff
- `getPublishedTenantConfig` → no permission · anonymous, guest, device

**A refused user sees:** **Nothing here needs a sign-in** (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-2)): the screen reads only what the tenant has published, which is public, so there is no no-access case. A host that belongs to no tenant shows the platform's neutral holding page.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Customisable maintenance page shown to guests during planned maintenance/upgrades. *(client request · MoM 10 Aug 2026, 4.8 Checkout Extras — Delivery, Waiting Room, Upsell/Cross-Sell, Seating, Resources · DI-215)*

Also apply: 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

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

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-029` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Footer 'Service status', or Discover → 'Service status'*. Differences: Prototype has 'Maintenance' where YAML has 'closed'; sold-out offers 'Join the waitlist' (holds a returned place for 15 minutes), which the YAML screen (getTenantAppStatus only) cannot call. **Do not draw "Join the waitlist" on the sold-out page**: this screen calls no waitlist operation; a sold-out performance waitlist belongs to the event booking screens (CHG-SGU-022).

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (48 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-029?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline, soldOut, closed, maintenance.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

## Tenant configuration on every guest screen

Every guest screen in this batch is white-label. These elements are set by the tenant in the CMS and apply to every screen of the guest app (each screen's block lists the ones particular to it). **Draw with the default theme; on the key screens add one alternate tenant theme** (below), so a reviewer sees the brand is configuration, not paint. The full map, with the input-to-output examples: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Element | Configured in | Allowed values | Default | What it changes |
|---|---|---|---|---|
| Logo (`brand.logoAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo in the header or nav bar, the splash and the footer |
| Logo dark image (`brand.logoDarkAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo on dark backgrounds (falls back to the primary logo) |
| Logo variant (`brand.logoVariant`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | Light · Dark · Duotone | Light | which logo lockup sits in the nav bar, and whose colours drive the theme |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Splash image (`brand.splashImageAssetRefs`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG, JPG, SVG or MP4 from the media library | — | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). |
| Splash duration seconds (`brand.splashDurationSeconds`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | min 0; max 10 | 3 | — |
| Splash background colour (`brand.splashBackgroundColour`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | #RRGGBB | — | — |
| Show loading indicator (`brand.showLoadingIndicator`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | — | on | — |
| Intro video (`brand.introVideoAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode (`brand.introVideoMode`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | Off | When GST-001 plays it full screen. "Skip introduction" is always shown. |
| Powered by TICVAI credit (`brand.showPoweredBy`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | — | on | the *Powered by TICVAI* credit on the launch screen, at the foot of Account and in the web footer; on by default, and switching it off needs the licence add-on (403 … |
| Primary colour (`theme.primaryColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | the brand colour (the `accentSolid` token): primary buttons (Book, Continue, Add to cart, Pay), the active step of the step indicator, selected date and time chips, focus rings |
| Secondary colour (`theme.secondaryColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | secondary buttons and secondary emphasis: unselected chips, secondary tabs |
| Accent colour (`theme.accentColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | highlights: badges (LIMITED, NEW, BESTSELLER), availability counts, sale prices |
| Background colour (`theme.backgroundColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | the page background behind every screen (the `ground` token) |
| Text colour (`theme.textColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | body text on the background |
| Corner radius (`theme.cornerRadius`) | `CMS-005`, `ADM-016` | min 0; max 32 | — | the corners of cards, buttons, inputs, sheets and the cart (0 square to 22 the prototype's roundest) |
| Surface style (`theme.surfaceStyle`) | `CMS-005`, `ADM-016` | Glass · Solid | Glass | cards and panels: frosted glass (default) or opaque (the `surfaceRaised` token) |
| Button style (`theme.buttonStyle`) | `CMS-005`, `ADM-016` | Solid · Outline · Pill | Solid | every button's shape: solid fill, outline, or pill |
| Component colours (`theme.componentColours`) | `CMS-005`, `ADM-016` | — | — | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. |
| Primary latin (`fonts.primaryLatin`) | `CMS-003` | — | — | headings and body text in English |
| Primary arabic (`fonts.primaryArabic`) | `CMS-003` | Required when `ar` is among the tenant's languages (audit R163). | — | headings and body text in Arabic |
| Secondary latin (`fonts.secondaryLatin`) | `CMS-003` | — | — | the secondary face (eyebrows, numbers) in English |
| Secondary arabic (`fonts.secondaryArabic`) | `CMS-003` | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). | — | the secondary face in Arabic |
| Custom font images (`fonts.customFontAssetRefs`) | `CMS-003` | PNG, JPG, SVG or MP4 from the media library | — | Uploaded font files, as `MediaAsset` ids. |
| Header layout (`header.layout`) | `CMS-009` | Logo left · Logo centre · Logo with menu | — | the header: logo left, logo centred, or logo with the menu |
| Show logo (`header.showLogo`) | `CMS-009` | — | on | — |
| Show menu (`header.showMenu`) | `CMS-009` | — | on | — |
| Show notifications (`header.showNotifications`) | `CMS-009` | — | on | — |
| Background colour (`header.backgroundColour`) | `CMS-009` | #RRGGBB | — | — |
| Navigation kind (`navigation.kind`) | `CMS-009` | Bottom navigation · Drawer · Tabs | — | the main navigation: bottom tab bar, drawer, or tabs |
| Navigation items (`navigation.items`) | `CMS-009` | at most 12 | — | — |
| Buy button (`navigation.buyButton`) | `CMS-009` | — | — | The persistent Buy tickets button (decided 29 September, MOB-2). On every screen of the mobile app except the booking and checkout steps; it opens GST-003. |
| Footer columns (`footer.columns`) | `CMS-009` | — | — | — |
| Legal links (`footer.legalLinks`) | `CMS-009` | — | — | Required links, held separately from the free-form columns — a tenant reorganising their footer must not be able to remove the privacy notice by accident. |
| Copyright text (`footer.copyrightText`) | `CMS-009` | — | — | — |
| Social links (`footer.socialLinks`) | `CMS-009` | — | — | — |
| Languages (`languages.languages`) | `CMS-011`, `ADM-018` | at least 1 | — | the language button in the header; Arabic flips every screen right to left |
| Default language (`languages.defaultLanguage`) | `CMS-011`, `ADM-018` | ISO 639-1 code, shown as the language name | — | the language a first visit opens in |
| Modules (`modules.modules`) | `CMS-001`, `ADM-424` | — | — | — |
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
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Component colours: primary CTA (`theme.componentColours.primaryCta`) | `CMS-005`, `ADM-016` | — | — | the one main call to action on each screen, when it should differ from the brand colour |
| Component colours: pay button (`theme.componentColours.payButton`) | `CMS-005`, `ADM-016` | — | — | the Pay button at checkout |
| Buy button: style (`navigation.buyButton.style`) | `CMS-009` | Raised · Floating · Flat · Hidden | Raised | the Buy tickets button in the tab bar: raised (default), floating, flat, or hidden |

**The alternate tenant theme (Coastal Aqua)**: Primary colour #0077B6; Secondary colour #023E8A; Accent colour #FFB703; Background colour #F5FAFC; Text colour #0B1324; Corner radius 18; Surface style Solid; Button style Pill; Logo variant Duotone; Header layout Logo centre; Step indicator Dots; Card layout Cards across; Card size Standard; Cart layout Floating icon; Fonts Poppins / Tajawal.
**Key screens to show in it:** `WEB-001`, `WEB-005`, `WEB-006`, `WEB-010`, `WEB-012`, `GST-001`, `GST-007`, `GST-041`, `KSK-002`, `KSK-003`.

**Decided for every guest screen:** **No dark or light mode.** The venue's chosen theme applies on every device setting; `Theme.darkMode` is deprecated and ignored, never drawn, and the guest app has no Light/Dark switch (Chinmay, 2 October, Q150; CHG-CSA-035). ***Powered by TICVAI* is a tenant toggle, on by default** (`brand.showPoweredBy`): shown on the launch screen, at the foot of Account and in the web footer; switching it off needs the licence add-on, or 403 `powered-by-locked` (Chinmay, 2 October, Q160; DI-297; CHG-CSA-036). **Each homepage section sets its card count and its scroll animation** (`maxItems`; `scrollAnimation` rise, scale, slide, blur or none, default rise): every customisation option of the approved wireframe (Chinmay, 2 October, Q152 and Q153; DI-1088; CHG-CSA-040). **Landing-page templates.** A tenant with no landing page of its own starts from a TICVAI template (`listLandingPageTemplates`, kept as `HomepageLayout.templateKey`); one with its own site links in with deep links (`landingSource` ownSite) (Chinmay, 2 October, batch 2 #41; CHG-CSA-037).

**Never configurable:** A dark or light mode: the guest surfaces have one theme, the venue's (Chinmay, 2 October; CHG-CSA-035). Semantic colour pairs (success, warning, danger, neutral) are not overridable: a tenant who recolours danger to their brand green has made a destructive confirmation look like a success (`screens/_design-tokens.yaml` whiteLabel). Site structure and the navigation flow are fixed and adapt to the product configuration (MoM 3 Aug, DI-119); a guest always books a product or package, never a resource (DI-502). A colour pair that fails 4.5:1 contrast is refused by the CMS, not warned (setTheme 400 ContrastProblem, audit R139).

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

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getPublishedTenantConfig": {"method":"GET","path":"/storefront/tenant-config","contract":"white-label","summary":"The published guest-facing configuration, before anyone signs in","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"venueId","in":"query","required":false}],"requestBody":null,"responds":"PublishedTenantConfig"},
"getTenantAppStatus": {"method":"GET","path":"/tenant-config/status","contract":"white-label","summary":"App status and recent changes","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"TenantAppStatus"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessibilitySettings": {"type":"object","description":"BL-065, 2.1.27. **POS and kiosk accessibility, which is a legal obligation in most jurisdictions and was unstated.**\n**A kiosk is the hard case.** A guest with low vision using a website brings their own assistive technology; a guest at a kiosk gets whatever the kiosk offers, so the settings have to be on the device rather than in the browser.\n","properties":{"largeTextAvailable":{"type":"boolean","default":true},"highContrastAvailable":{"type":"boolean","default":true},"simplifiedNavigationAvailable":{"type":"boolean","default":true},"screenReaderSupported":{"type":"boolean","default":true},"reachableHeightModeAvailable":{"type":"boolean","default":false,"description":"**Moves the interface to the lower half of the screen** for a guest using a wheelchair. A kiosk mounted at standing height is unusable otherwise, and no software setting fixes the mounting — this is the mitigation.\n"},"sessionTimeoutMultiplier":{"type":"number","default":1,"description":"**Timeouts are an accessibility barrier nobody counts.** A guest who needs three times as long to read a screen should not lose their basket to a 90-second inactivity timer.\n"}}},
"AppAvailability": {"type":"string","description":"**The sold-out or closed signal (decided 28 September, audit R073).** `open` is the normal state. `soldOut` shows WEB-029's sold-out state across the app while browsing still works; `closed` shows the closed state (a weather closure, a private event). Neither refuses a request on its own: it is what the guest is told, and a sale is still refused by availability where it applies. Set with `setMaintenanceMode`.\n","enum":["open","soldOut","closed"],"default":"open"},
"AppIcons": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["sourceAssetRef","changeScope"],"properties":{"sourceAssetRef":{"type":"string","format":"uuid","description":"The `MediaAsset` id of the 1024×1024 source."},"derived":{"type":"array","readOnly":true,"x-ticvai-derived":"onWrite","description":"Generated by `setAppIcons` from the source, one entry per platform and size — the iOS and Android store sets and the web favicons listed on `setAppIcons` (audit R163).","items":{"type":"object","properties":{"platform":{"type":"string","enum":["ios","android","web"]},"size":{"type":"string"},"assetRef":{"type":"string","format":"uuid"}}}},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Always `buildTime` — icons are baked into the binary."},"liveVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Icon currently shipped. Differs from the draft until the next release."},"requiresRebuild":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onRead","description":"True while the draft's source differs from the icon in `liveVersion`."}}},
"BookingFlowConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","description":"**Set per tenant, with a per-venue override (decided 29 September, rev 3 CFG-11).** One tenant with several venues (the Kids Club branches, Coastal Aqua beside Union Arena) needs them to differ. The settings in force at a venue are the tenant's, with that venue's entry in `venueOverrides` laid over them field by field. The guest app resolves them for the venue the guest picked (audit R267); `effectiveForVenueId` on `getBookingFlowConfig` returns them resolved.\n","allOf":[{"$ref":"#/components/schemas/BookingFlowSettings"},{"type":"object","properties":{"venueOverrides":{"type":"array","maxItems":200,"default":[],"description":"Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. An override for a venue later closed is kept and has no effect.","items":{"$ref":"#/components/schemas/BookingFlowVenueOverride"}}}}]},
"BrandIdentity": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","description":"Every `*AssetRef` here is a `MediaAsset` id from the `assets` library (`createUpload` then `completeUpload`), PNG or SVG and at most 2 MB (decided 28 September, audit R270).\n","required":["logoAssetRef"],"properties":{"logoAssetRef":{"type":"string","format":"uuid","description":"The primary logo."},"logoDarkAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"Used on dark backgrounds. Falls back to the primary logo."},"logoVariant":{"type":"string","enum":["light","dark","duotone"],"default":"light","description":"**Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4).** `light` uses `logoAssetRef`, `dark` uses `logoDarkAssetRef` (falling back to the primary logo), and `duotone` the two-colour reading of the primary logo.\n"},"faviconAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"The browser tab icon for the guest web app."},"splashImageAssetRefs":{"type":"array","description":"Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163).","items":{"type":"string","format":"uuid"}},"splashDurationSeconds":{"type":"integer","minimum":0,"maximum":10,"default":3},"splashBackgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"showLoadingIndicator":{"type":"boolean","default":true},"splashChangeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163)."},"introVideoAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"**The optional intro video (decided 29 September, MOB-5).** A video `MediaAsset` from the media library (CMS-010). Streamed, so a change reaches guests with the publish and needs no app build.\n"},"introVideoMode":{"type":"string","enum":["off","firstLaunch","everyLaunch"],"default":"off","description":"When GST-001 plays it full screen. \"Skip introduction\" is always shown. Anything but `off` needs `introVideoAssetRef`, or 400."},"showPoweredBy":{"type":"boolean","default":true,"description":"**\"Powered by TICVAI\", a configuration toggle, on by default** (Chinmay, 2 October, workbook Q160 and the pre-apply round; consistent with DI-297; CHG-CSA-036). Shown on the launch screen and at the foot of Account and the web footer while true. **Switching it off needs the tenant's licence to allow it**: `setBrandIdentity` refuses `false` with `403 powered-by-locked` unless the tenant's plan carries the `poweredByRemoval` add-on (subscription `LicencePosition.poweredByRemovable`)."}}},
"FontConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["primaryLatin"],"properties":{"primaryLatin":{"type":"string"},"primaryArabic":{"type":"string","nullable":true,"description":"Required when `ar` is among the tenant's languages (audit R163). A Latin face alone leaves Arabic in a system fallback that will not match.\n"},"secondaryLatin":{"type":"string","nullable":true},"secondaryArabic":{"type":"string","nullable":true,"description":"Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163)."},"customFontAssetRefs":{"type":"array","description":"Uploaded font files, as `MediaAsset` ids.","items":{"type":"string","format":"uuid"}},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"x-ticvai-derived":"onRead","description":"Custom font files are `buildTime`; selecting a bundled face is `runtime`."}}},
"FooterConfig": {"type":"object","x-ticvai-persistence":"whitelabel.footer_config + whitelabel.footer_config_column + whitelabel.footer_config_social_link","description":"BL-002. **`setHeader` and `HeaderConfig` exist and the footer does not**, which looked like symmetry until you notice it is not: **a header is chrome and a footer is a link surface.**\nA footer carries the legal links — terms, privacy, accessibility statement, cookie preferences — and **those are the ones a regulator checks.** Treating it as a mirror of the header would have given it a logo and no way to reach a privacy notice.\n**Where it is stored.** `legalLinks` and `copyrightText` are columns of `whitelabel.footer_config`; each entry of `columns` is a `whitelabel.footer_config_column` row and each entry of `socialLinks` a `whitelabel.footer_config_social_link` row. Part of the working draft (see the header). **In the tenant's own database, not the control plane (decided 28 September, audit R163)**: it moved from `control.footer_config` and its two child tables.\n","required":["id","scopePath"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005), written at `tenant` scope by the server."},"columns":{"type":"array","items":{"type":"object","properties":{"heading":{"type":"string"},"links":{"type":"array","items":{"type":"object","properties":{"label":{"type":"string"},"url":{"type":"string"},"opensCookiePreferences":{"type":"boolean","default":false}}}}}}},"legalLinks":{"type":"object","description":"**Required links, held separately from the free-form columns** — a tenant reorganising their footer must not be able to remove the privacy notice by accident.\n","properties":{"termsUrl":{"type":"string"},"privacyUrl":{"type":"string"},"accessibilityUrl":{"type":"string","nullable":true},"cookiePolicyUrl":{"type":"string","nullable":true}}},"copyrightText":{"type":"string"},"socialLinks":{"type":"array","items":{"type":"object","properties":{"platform":{"type":"string"},"url":{"type":"string"}}}}}},
"HeaderConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["layout"],"properties":{"layout":{"type":"string","enum":["logoLeft","logoCentre","logoWithMenu"]},"showLogo":{"type":"boolean","default":true},"showMenu":{"type":"boolean","default":true},"showNotifications":{"type":"boolean","default":true},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},
"HomepageLayout": {"x-ticvai-persistence":"whitelabel.homepage_section","type":"object","description":"**The client-approved web and app wireframes are the layout** (Chinmay, 2 October, workbook Q163; CHG-CSA-040): sections, their order and their options follow the approved wireframes and change only where the spec breaks. **Landing-page templates** (workbook Q41 batch 2; CHG-CSA-037): a tenant with no landing page of its own starts from a TICVAI template (`templateKey`, `listLandingPageTemplates`); a tenant with its own site links into the storefront with deep links (`getDeepLinkScheme`, `buildDeepLink`).","required":["sections"],"properties":{"templateKey":{"type":"string","nullable":true,"description":"The landing-page template this layout started from (`listLandingPageTemplates`), or null for a layout composed from scratch (CHG-CSA-037)."},"landingSource":{"type":"string","enum":["storefront","ownSite"],"default":"storefront","description":"`storefront`: this home is the tenant's landing page. `ownSite`: the tenant's own website is the landing page and links in with deep links; this home is still served at the storefront address."},"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"sections":{"type":"array","items":{"type":"object","required":["kind","sortOrder","isVisible"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"kind":{"$ref":"#/components/schemas/HomepageSectionKind"},"title":{"$ref":"#/components/schemas/LocalisedText"},"sortOrder":{"type":"integer"},"isVisible":{"type":"boolean"},"contentPageId":{"type":"string","format":"uuid","nullable":true},"maxItems":{"type":"integer","nullable":true,"description":"**How many cards the section shows, the venue's choice** (Chinmay, 2 October, workbook Q152: every customisation option of the approved wireframe, including the card count per section; CHG-CSA-040). Replaces the fixed 1 or 2 highlights of MOB-3: the CMS offers the counts the approved wireframe offers."},"scrollAnimation":{"type":"string","enum":["rise","scale","slide","blur","none"],"default":"rise","description":"**How the section enters as the guest scrolls** (Chinmay, 2 October, workbook Q153: \"must be there\"; DI-1088; CHG-CSA-040). Rise, Scale, Slide, Blur or None, as the v4 prototype offers; `none` for guests who asked the device for reduced motion is applied whatever is set."},"heroStyle":{"type":"string","nullable":true,"enum":["carousel","video","poster","split",null],"description":"For `heroBanner` only (decided 29 September, MOB-3)."}}}}}},
"LanguageConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["languages","defaultLanguage"],"properties":{"languages":{"type":"array","description":"**A tenant may add or select interface languages beyond English and Arabic** (Chinmay, 2 October, workbook Q145; CHG-CSA-039). Any ISO 639-1 language. English and Arabic ship with complete interface strings; for any other, the interface strings come as a TICVAI string pack drafted by AI translation and reviewed (T03), and a string with no translation falls back to English. Content (pages, products, banners) is the tenant's to translate (`translationGaps`).","items":{"type":"string","pattern":"^[a-z]{2}$"}},"defaultLanguage":{"type":"string","pattern":"^[a-z]{2}$"},"uiStringCoverage":{"type":"array","readOnly":true,"description":"How complete the interface strings are in each enabled language (CHG-CSA-039). English and Arabic are always complete.","items":{"type":"object","properties":{"language":{"type":"string"},"coveragePercent":{"type":"number","minimum":0,"maximum":100},"status":{"type":"string","enum":["complete","draft","missing"]}}}},"rtlLanguages":{"type":"array","readOnly":true,"x-ticvai-derived":"onRead","description":"The enabled languages written right to left — those whose Unicode CLDR character order is `right-to-left` (Arabic, `ar`, among them). Not configured; it follows from `languages`.","items":{"type":"string","pattern":"^[a-z]{2}$"}},"translationGaps":{"type":"array","readOnly":true,"description":"Content lacking a version in an enabled language.","items":{"type":"object","properties":{"language":{"type":"string"},"missingCount":{"type":"integer"},"areas":{"type":"array","items":{"type":"string"}}}}}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MinimumAppVersion": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n","properties":{"ios":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"},"android":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"}}},
"ModuleKey": {"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},
"NavigationConfig": {"x-ticvai-persistence":"whitelabel.navigation_item","type":"object","description":"**The mobile tab set is venue configuration (decided 29 September, MOB-1; 29 September brief decision 6).** Before a tenant saves its own, `bottomNavigation` is Home, Explore, Plan and Tickets (each an `appSection` link), with the Buy tickets button beside them; Map is an optional tab. Plan is left out while `visitPlanner` is off.\n","required":["kind","items"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"kind":{"type":"string","enum":["bottomNavigation","drawer","tabs"]},"items":{"type":"array","maxItems":12,"items":{"type":"object","required":["label","target","isVisible","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"label":{"$ref":"#/components/schemas/LocalisedText"},"icon":{"type":"string"},"target":{"$ref":"#/components/schemas/LinkTarget"},"isVisible":{"type":"boolean","description":"At most five may be visible in bottom navigation; the rest overflow."},"sortOrder":{"type":"integer"}}}},"buyButton":{"type":"object","nullable":true,"description":"**The persistent Buy tickets button (decided 29 September, MOB-2).** On every screen of the mobile app except the booking and checkout steps; it opens GST-003. Read with `bottomNavigation`.\n","properties":{"style":{"type":"string","enum":["raised","floating","flat","hidden"],"default":"raised","description":"`raised` sits in the centre of the tab bar, as the v4 prototype shows; `hidden` turns it off."},"label":{"$ref":"#/components/schemas/LocalisedText"}}}}},
"PublishedTenantConfig": {"x-ticvai-persistence":"none — computed from the current ConfigVersion snapshot and the live status on whitelabel.tenant_config","type":"object","x-ticvai-agreed":"2 October: decided by Chinmay, fix before Block A starts (GFIX-1)","description":"**The public view of the tenant's configuration** (`getPublishedTenantConfig`, decided 2 October, GFIX-1). The published parts a guest surface renders with, from the current `ConfigVersion`, and the live status `setMaintenanceMode` writes. Nothing a guest cannot see on the page: no draft marker, no CMS counts, no sender addresses, no licensing, no person.\n","required":["tenantId","publishedVersion","publishedAt","isInMaintenance"],"properties":{"tenantId":{"type":"string","format":"uuid"},"publishedVersion":{"type":"string","description":"The `ConfigVersion.version` this answer was read from; a client holding the same version keeps its copy."},"publishedAt":{"type":"string","format":"date-time"},"brand":{"$ref":"#/components/schemas/BrandIdentity"},"appIcons":{"$ref":"#/components/schemas/AppIcons"},"theme":{"$ref":"#/components/schemas/Theme"},"fonts":{"$ref":"#/components/schemas/FontConfig"},"header":{"$ref":"#/components/schemas/HeaderConfig"},"footer":{"$ref":"#/components/schemas/FooterConfig"},"navigation":{"$ref":"#/components/schemas/NavigationConfig"},"homepage":{"$ref":"#/components/schemas/HomepageLayout"},"bookingFlow":{"allOf":[{"$ref":"#/components/schemas/BookingFlowConfig"}],"description":"The booking-flow display settings, resolved for `venueId` when one was sent (the tenant's values with that venue's `venueOverrides` entry laid over, rev 3 CFG-11)."},"languages":{"$ref":"#/components/schemas/LanguageConfig"},"accessibility":{"$ref":"#/components/schemas/AccessibilitySettings"},"enabledModules":{"type":"array","description":"The modules the tenant has enabled and published, so a guest surface hides a tab or a homepage section for a module that is off. Licensing is not shown.","items":{"$ref":"#/components/schemas/ModuleKey"}},"enabledFeatures":{"type":"array","description":"The `featureKey` of every feature toggle that is on in the published version.","items":{"type":"string"}},"isInMaintenance":{"type":"boolean","description":"Live state (`setMaintenanceMode`), as on `getTenantAppStatus`."},"maintenanceMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"$ref":"#/components/schemas/MinimumAppVersion"},"availability":{"$ref":"#/components/schemas/AppAvailability"},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"contact":{"$ref":"#/components/schemas/VenueContact"}}},
"TenantAppStatus": {"x-ticvai-persistence":"none — computed","type":"object","description":"Computed on read. The published fields come from the current `ConfigVersion`, the maintenance fields from the tenant's `tenant_config` row (`setMaintenanceMode`), and the draft fields from the working draft. **Fields marked staff only are left out of a response to a caller without a staff session** (`getTenantAppStatus`).\n","required":["tenantId","isPublished","isInMaintenance"],"properties":{"tenantId":{"type":"string","format":"uuid"},"isPublished":{"type":"boolean","x-ticvai-derived":"onRead","description":"True once any version has been published."},"publishedVersion":{"type":"string","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"draftVersion":{"type":"string","description":"Staff only."},"hasUnpublishedChanges":{"type":"boolean","x-ticvai-derived":"onRead","description":"Staff only. The working draft differs from the current version's `snapshot`."},"activeModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isEnabled` true."},"licensedModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isLicensed` true."},"activePageCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. Content pages that are `published` and enabled."},"isInMaintenance":{"type":"boolean"},"maintenanceMessage":{"$ref":"#/components/schemas/LocalisedText"},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"$ref":"#/components/schemas/MinimumAppVersion"},"contact":{"$ref":"#/components/schemas/VenueContact"},"availability":{"$ref":"#/components/schemas/AppAvailability"},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"What the sold-out or closed screen says (WEB-029). Null shows the default wording."},"venues":{"type":"array","maxItems":200,"x-ticvai-derived":"onRead","description":"**Public: the venues a guest can pick** (decided 28 September, audit R267; schema named 29 September, readiness close-out, our build plan). The source of the venue picker on WEB-001 and GST-001, returned with or without a session. **Published only**: a venue is listed when its scope node is active (`tenancy.OrgUnit.isActive`) and it is in the tenant's current published `ConfigVersion`; a venue added or reactivated since the last publish appears after the next publish, and a draft never reaches a guest. Ordered by `name`. Empty when nothing is published.\n","items":{"type":"object","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid","description":"**The venue's scope node** (`tenancy.OrgUnit.id`, level venue): what every guest screen that declares `venueId` `from: session` reads once the guest picks it."},"name":{"type":"string","maxLength":200,"description":"The venue's name (`tenancy.OrgUnit.name`)."},"city":{"type":"string","maxLength":120,"nullable":true,"description":"Shown under the name so two venues with similar names can be told apart."},"openingHoursToday":{"type":"object","nullable":true,"description":"Today's opening hours in the venue's time zone, from `tenancy.VenueSettings` opening hours. Null when the venue is closed today or has none set.","properties":{"opens":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"},"closes":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"}}}}}},"whatsNew":{"type":"array","maxItems":10,"x-ticvai-derived":"onRead","description":"**Public: the guest \"what's new\"** (decided 29 September, rev 3 GAP-B2). Newest first, at most 10, from `platform-ops.Release.guestReleaseNotes` of the releases the tenant's cell has received; a release with no guest notes is skipped. Returned with or without a staff session.\n","items":{"type":"object","required":["version","publishedAt","notes"],"properties":{"version":{"type":"string","description":"The release version."},"publishedAt":{"type":"string","format":"date-time","description":"When the release reached the tenant's cell."},"notes":{"$ref":"#/components/schemas/LocalisedText"}}}},"recentChanges":{"type":"array","description":"Staff only. Names the principal behind each change, so it never reaches a public response.","items":{"type":"object","properties":{"area":{"type":"string"},"description":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"}}}}}},
"Theme": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["primaryColour","secondaryColour","backgroundColour","textColour"],"properties":{"primaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"secondaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"accentColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"textColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"darkMode":{"type":"object","deprecated":true,"description":"**Deprecated and ignored** (Chinmay, 2 October, workbook Q150 and the pre-apply round; CHG-CSA-035). White label has no dark or light mode: the venue's chosen theme is applied, on every device setting. The field is kept so a client built at r1 still parses, is accepted on `setTheme` and returned as stored, and **is never used to render anything or drawn on any screen**; the guest app has no Light/Dark switch.","properties":{"primaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"textColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},"cornerRadius":{"type":"integer","minimum":0,"maximum":32,"description":"The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). Its named palettes, font pairs and background tones are presets over the colours here and `FontConfig`, not stored values."},"surfaceStyle":{"type":"string","enum":["glass","solid"],"default":"glass","description":"Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3)."},"buttonStyle":{"type":"string","enum":["solid","outline","pill"],"default":"solid","description":"Button shape (decided 29 September, rev 3 CFG-3)."},"componentColours":{"type":"object","description":"**Colours for single interactive elements (decided 17 September, M17-11).** Each is optional and falls back to the theme colours. Every pair passes the same contrast check as the theme (`ContrastProblem`), or `setTheme` refuses it with 400. The guest flow stays the standard one; only the colours change.\n","properties":{"primaryCta":{"$ref":"#/components/schemas/ThemeComponentColour"},"payButton":{"$ref":"#/components/schemas/ThemeComponentColour"},"addToCart":{"$ref":"#/components/schemas/ThemeComponentColour"},"buyTicketsButton":{"$ref":"#/components/schemas/ThemeComponentColour"},"link":{"$ref":"#/components/schemas/ThemeComponentColour"},"badge":{"$ref":"#/components/schemas/ThemeComponentColour"}}}}},
"VenueContact": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n","properties":{"phone":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true},"whatsapp":{"type":"string","nullable":true},"address":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Prose, as the guest reads it. The bookable hours are the catalogue's."}}}
}
```
