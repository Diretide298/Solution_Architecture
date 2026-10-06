# P13-white-label-03 — P13 · White Label (3 of 3)

**3 screens · 27 operations · 40 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `AI_USE, GUEST_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, TENANT_CONFIGURE, TENANT_PUBLISH`. A control nobody can use must say so,
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
| `CMS-102` | Site Builder | A | 20 | 15 | 6 | 2 | 7 | 6 | configures | notStarted (generated) |
| `CMS-103` | Booking Flows | A | 78 | 29 | 6 | 18 | 27 | 6 | configures | notStarted (generated) |
| `CMS-104` | App Build & Store Publishing | A | 22 | 35 | 6 | 17 | 6 | 6 | configures | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `CMS-102` Site Builder

**Build a working site in about 30 minutes: pick a preset, then walk seven saved steps (venue and modules, ticketing flows, compose steps, Help me choose, look and feel, mobile app, preview and publish), each opening the full screen for its details. **The preset keeps the minimum path short (M24-05)**: it proposes the modules, the booking flows with their default step order, the home sections and the mobile tabs, so the only things an operator must supply are a logo, four colours and a Publish; everything else keeps the preset or the contract default and can be refined later.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · ticket #27908 (APP-WL-CMS-102) |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | multiStepForm (compact density): `getSiteSetupProgress` holds the seven steps and their state, and `setSiteSetupProgress` saves each one — progress, fields per step, review, submit |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: Resolves the tenant and venue from the session and opens on the current step, or on Start from when nothing is saved. |
| Route | `/white-label/site-builder` |

**What the spec says about it.** **Added 29 September for W12 and M24-05: the CMS is a flow builder with a step-based shell.** The configuration side panel of the rev 3 prototype is a reference tool only (W12). The builder is the white-labelling builder M24-05 asks for, not a new set of editors: every step opens a screen that already exists and holds its details.

**From the White Label & CMS process.** The step-based Site Builder: pick a preset (theme park, water park, museum, theatre and arena, single attraction, play centre, several venues), then seven saved steps, each opening the full screen and coming back. The minimum path (logo, four colours, one valid booking flow, a publish) is always visible, so a client gets a working site in about 30 minutes. Every option the builder touches must visibly change something in a preview.

**Fixed on main** (the package already carries these; draw what it says): CMS-009 Navigation & Menus, which steps 5 and 6 open for the header menu, the tab bar and the Buy tickets button, is filed under module … (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which modules, flows, sections and tabs does each preset propose? No source lists them.** → Drawn default accepted: Water park proposes ticketsAndBooking, diningAndFnb, shop, map; datedDayPass and cabanaMap; heroBanner, tickets, attractions, dining; tabs Home, Explore, Map, Tickets. *(decided by Chinmay, 2026-10-02; DEC-159 / CHG-NOTE-009)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Start from | select | optional | — | Theme park · Water park · Museum · Theatre and arena · Single attraction · Play centre · Multi venue | — | Theme park, water park, museum, theatre and arena, single attraction, play centre, several venues. **Proposes, never writes**: each step opens pre-filled from the preset, and nothing changes until … | `SiteSetupProgress.presetKey` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product kind | text field | — | — | `listBookingFlowTypes` ?productKind |
| Flow type key | select | — | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour by language · Transport … | `listBookingFlows` ?flowTypeKey |

**Form: Add these flows** (modal, opened by *Add these flows*; *Add flows* calls `createBookingFlowDefinition`, *Cancel* sends nothing)

**Collects what `createBookingFlowDefinition` sends, once per ticked type.** Required: `flowTypeKey`, `name` (pre-filled from the type). `isDefaultForType` on. Steps are left out, so each flow gets the type's default steps and order. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Flow type key `flowTypeKey` | select | required | — | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour by language · Transport … | — | The flow types the system catalogue offers (decided 29 September, W12; impact.md b). | `createBookingFlowDefinition` body |
| Name `name` | text field | required | — | max length 80 | — | Staff-facing, e.g. "Day pass, date first". | `createBookingFlowDefinition` body |
| Is default for type `isDefaultForType` | toggle | optional | off | At most one per venue and type; setting it takes it from the previous default. | — | At most one per venue and type; setting it takes it from the previous default. | `createBookingFlowDefinition` body |
| Is enabled `isEnabled` | toggle | optional | on | — | — | A disabled flow is kept and not published; products naming it fall back to the default. | `createBookingFlowDefinition` body |
| Steps `steps` | repeatable rows | optional | — | at most 30 | — | Every step of the type, in the venue's order. Filled from the type when left out on create. | `createBookingFlowDefinition` body |
| Step key `steps[].stepKey` | select | required | — | Location · Help me choose · Product · Date · Time · Performance · Level · Language · Duration · Route · Party size · Resource map … | — | Every step a guest booking flow can hold (decided 29 September, W12). What each step does on WEB and MOB, and which screen draws it, is in the screen definitions of P01 and P02 … | `createBookingFlowDefinition` body |
| Enabled `steps[].enabled` | toggle | required | — | A `required` step cannot be off; the flow saves and `isValid` turns false. | — | A `required` step cannot be off; the flow saves and `isValid` turns false. | `createBookingFlowDefinition` body |
| Sort order `steps[].sortOrder` | number field | required | — | min 0 | — | — | `createBookingFlowDefinition` body |
| Settings `steps[].settings` | key and value settings | optional | — | A name the type does not give is refused with 400. | — | The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. | `createBookingFlowDefinition` body |
| Settings `settings` | group | optional | — | — | — | The settings that belong to one flow, not to the venue (decided 29 September, W12). | `createBookingFlowDefinition` body |
| Performance reveal `settings.performanceReveal` | segmented control | optional | Date time ticket | Date time ticket · All at once | — | Performance reveal (rev 3 REV3-2). `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. | `createBookingFlowDefinition` body |
| Sign in at `settings.signInAt` | segmented control | optional | After add ons | After add ons · At payment | — | Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3). | `createBookingFlowDefinition` body |
| Seat event date mode `settings.seatEventDateMode` | segmented control | optional | Inline step | Inline step · Popup on seat map; Read only by the seated flow types. | — | Date and time on a seated event (rev 3 REV3-4). `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. | `createBookingFlowDefinition` body |
| Extras step `settings.extrasStep` | segmented control | optional | Auto | Auto · Always · Never; `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. | — | `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. | `createBookingFlowDefinition` body |
| Quick tour `settings.quickTour` | toggle | optional | off | — | — | Quick tour (rev 3 REV3-20). A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. | `createBookingFlowDefinition` body |
| Consent questions `settings.consentQuestionIds` | multi-picker: choose consent questions | optional | — | at most 10; no duplicates; Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. | — | The flow's own consent questions (rev 3 REV3-26). Asked on every booking through this flow, together with those of each product in the cart, each question once. | `createBookingFlowDefinition` body |

Errors to draw in the form: 400 An unknown flow type, a step the type does not have, or a step given twice; 403 Authenticated but not permitted at the requested scope

**Sent by *Save and continue*** (`setSiteSetupProgress`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Preset key `presetKey` | select | optional | — | Theme park · Water park · Museum · Theatre and arena · Single attraction · Play centre · Multi venue | — | The starting point. Each preset proposes the modules, the booking flow types (with their default step order), the homepage sections, the mobile tabs and a booking-flow `preset` … | `setSiteSetupProgress` body |
| Current step `currentStep` | select | optional | — | Venue and modules · Ticketing flows · Compose steps · Help me choose · Look and feel · Mobile app · Preview and publish | — | The seven Site Builder steps, in order (decided 29 September, W12): venue and modules (CMS-001), ticketing flows (CMS-103), compose steps (CMS-103), Help me choose (CMS-101), look … | `setSiteSetupProgress` body |
| Steps `steps` | key and value settings | optional | — | — | — | One entry per `SiteSetupStepKey`. | `setSiteSetupProgress` body |

**Rules for these inputs** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **presetKey**: Seven picture cards; picking one proposes modules, booking flow types, homepage sections and tabs, and writes nothing until each step is accepted. *(source: contracts/satellite/white-label.yaml#/components/schemas/SiteSetupProgress; DI-997)*
- **steps[].status**: Not started / In progress / Done / Skipped; steps 4 (Help me choose) and 6 (Mobile app) may be skipped. Saved on every return. *(source: contracts/satellite/white-label.yaml#setSiteSetupProgress)*

#### Outputs: what the screen shows and produces

**Shown**

**Seven steps** (progress indicator, from `getSiteSetupProgress`): 1 Venue and modules · 2 Ticketing flows · 3 Compose steps · 4 Help me choose · 5 Look and feel · 6 Mobile app · 7 Preview and publish. Each step shows not started, in progress, done or skipped; steps 4 and 6 may be skipped. **Minimum path** (logo, colours, one valid flow, a publish) is marked, so an operator in a hurry sees what is left before the site works.

| Shows | Format | Notes |
|---|---|---|
| Current step | chip: Venue and modules, Ticketing flows, Compose steps, Help me choose, Look and feel … | The seven Site Builder steps, in order (decided 29 September, W12): venue and modules (CMS-001), ticketing flows (CMS-103), compose steps … |
| Steps | grouped details | One entry per `SiteSetupStepKey`. |
| Minimum path done | yes / no (icon or chip) | True once the minimum path is done: a logo, the four theme colours, at least one enabled valid booking flow and a published version. |

**Flow types the preset proposes** (card list, from `listBookingFlowTypes`): Step 2 in one tap: the preset's flow types, ticked; **Add these flows** creates each with the type's default steps and order (`createBookingFlowDefinition`). Composing the order is step 3, on CMS-103.

| Shows | Format | Notes |
|---|---|---|
| Key | chip: Dated day pass, Timed entry, Open dated, Seated fixed performance, Seated date time … | The flow types the system catalogue offers (decided 29 September, W12; impact.md b). |
| Name | in the reader's language | Keyed by ISO 639-1 code. Every enabled language should be present. |
| Product kinds | list or chips (count when long) | The catalogue `ProductKind` values this type books. A venue's default flow for a type serves every product of these kinds that names no … |

**Flows this venue has** (data table, from `listBookingFlows`): Steps 2 and 3 are done when every flow here is valid and each bookable product kind has one.

| Shows | Format | Notes |
|---|---|---|
| Name | text | Staff-facing, e.g. "Day pass, date first". |
| Flow type key | chip: Dated day pass, Timed entry, Open dated, Seated fixed performance, Seated date time … | The flow types the system catalogue offers (decided 29 September, W12; impact.md b). |
| Is default for type | yes / no (icon or chip) | At most one per venue and type; setting it takes it from the previous default. |
| Is valid | yes / no (icon or chip) | Whether the flow passes `validateBookingFlow`; worked out in the same transaction as each write. |

**What is live** (detail panel, from `getTenantAppStatus`)

| Shows | Format | Notes |
|---|---|---|
| Is published | yes / no (icon or chip) | True once any version has been published. |
| Published version | text | — |
| Has unpublished changes | yes / no (icon or chip) | Staff only. The working draft differs from the current version's `snapshot`. |

**What still blocks a publish** (banner, from `validateTenantConfig`): Each finding links to the step and screen that fixes it (a missing logo to CMS-004, an invalid flow to CMS-103).

| Shows | Format | Notes |
|---|---|---|
| Passed | yes / no (icon or chip) | — |
| Findings | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save and continue (primary button) | `setSiteSetupProgress` PUT `/tenant-config/site-setup` | SiteSetupProgress | SiteSetupProgress | 400 Validation failed; 409 `previewAndPublish` marked done while no version has been published | — |
| Add these flows (secondary button) | `createBookingFlowDefinition` POST `/venues/{venueId}/booking-flows` | BookingFlow | BookingFlow | 400 An unknown flow type, a step the type does not have, or a step given twice; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Check what blocks a publish (secondary button) | `validateTenantConfig` POST `/tenant-config/validate` | — | ConfigValidationReport | — | — |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Step rail**: 1 Venue and modules · 2 Ticketing flows · 3 Compose steps · 4 Help me choose · 5 Look and feel · 6 Mobile app · 7 Preview and publish, each with status and the screens it opens. *(source: contracts/satellite/white-label.yaml#/components/schemas/SiteSetupStepKey)*
- **Minimum path checklist**: Logo, four theme colours, at least one enabled valid booking flow, a published version; ticked from the server (minimumPathDone). *(source: contracts/satellite/white-label.yaml#/components/schemas/SiteSetupProgress)*
- **Live preview**: The guest Home updates as steps are accepted. *(source: DI-988)*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Add these flows**: Creates each ticked preset flow type at the venue with its default steps (isDefaultForType on). *(source: contracts/satellite/white-label.yaml#createBookingFlowDefinition)*
- **Mark Preview and publish done**: Refused 409 until a version is published. *(source: contracts/satellite/white-label.yaml#setSiteSetupProgress)*

**Data it reads**: `getSiteSetupProgress` (onLoad, Where the operator is in the seven steps, and the preset …); `listBookingFlowTypes` (onLoad, The flow types the preset proposes for step 2); `listBookingFlows` (onLoad, The venue's flows, to mark steps 2 and 3 done); `getTenantAppStatus` (onLoad, Whether the site is live, for step 7)

**Where the user goes next**

- → `CMS-105` Kiosk Builder: *Kiosks*
- → `CMS-001` Tenant Workspace: *1 Venue and modules*
- → `CMS-103` Booking Flows: *2 Ticketing flows*; carries `bookingFlowId`
- → `CMS-103` Booking Flows: *3 Compose steps*; carries `bookingFlowId`
- → `CMS-101` Help Me Choose: *4 Help me choose*
- → `CMS-007` Page Builder: *5 Look and feel — header, footer and home*
- → `CMS-009` Navigation & Menus: *5 Look and feel — navigation and menus*
- → `CMS-002` Brand Kit: *5 Look and feel — brand kit*
- → `CMS-004` Logo & Assets: *5 Look and feel — logos*
- → `CMS-008` Content Blocks: *5 Look and feel — banners*
- → `CMS-005` Theme Editor: *5 Look and feel — theme*
- → `CMS-003` Typography: *5 Look and feel — fonts*
- → `CMS-009` Navigation & Menus: *6 Mobile app — tabs and the Buy tickets button*
- → `CMS-004` Logo & Assets: *6 Mobile app — intro video*
- → `CMS-007` Page Builder: *6 Mobile app — home sections*
- → `CMS-006` Component Preview: *7 Preview*
- → `CMS-012` RTL Preview: *7 Preview right to left*
- → `CMS-014` Publishing Workflow: *7 Publish*; carries `version`
- → `CMS-015` Version History: *Roll back a version*; carries `version`
- → `CMS-104` App Build & Store Publishing: *Build the mobile app*; only when the tenant has published at least once

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The builder's progress, read by `getSiteSetupProgress`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the progress untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing set up yet.** Opens on Start from, with every step not started, and says the minimum path is a logo, four colours, the preset's flows and a publish. |
| Empty, no results (`?state=emptyNoResults`) | The venue has no flow of a type the preset proposes yet; the flow list says so and offers Add these flows rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getSiteSetupProgress` requires, and names that permission. **Never an empty form** — that reads as *there is nothing to set up*. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 An unknown flow type, a step the type does not have, or a step given twice; 400 Validation failed; 409 `previewAndPublish` marked done while no version has been published |

#### Edge cases to draw

- **Operator leaves halfway and returns a week later**: Opens on currentStep with the preset still chosen. *(source: contracts/satellite/white-label.yaml#getSiteSetupProgress)*
- **Tenant with several venues**: Steps 2 and 3 repeat per venue; the rail shows venue progress (2 of 4 venues have valid flows). *(source: contracts/satellite/white-label.yaml#listBookingFlows)*

#### Consistency with other screens

- Match `CMS-001`: Step 1 is CMS-001's module and feature switches.
- Match `CMS-104`: After the first publish, the builder offers the app build.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
preset: waterPark
steps:
  venueAndModules: done
  ticketingFlows: done
  composeSteps: inProgress
  helpMeChoose: skipped
  lookAndFeel: notStarted
  mobileApp: notStarted
  previewAndPublish: notStarted
minimumPath:
  logo: true
  colours: true
  validFlow: false
  published: false
```

#### Permissions

- `getSiteSetupProgress` → `TENANT_CONFIGURE` (configure) · staff
- `setSiteSetupProgress` → `TENANT_CONFIGURE` (configure) · staff
- `listBookingFlowTypes` → `TENANT_CONFIGURE` (configure) · staff
- `listBookingFlows` → `TENANT_CONFIGURE` (configure) · staff
- `createBookingFlowDefinition` → `TENANT_CONFIGURE` (configure) · staff
- `getTenantAppStatus` → no permission · device, guest, staff
- `validateTenantConfig` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getSiteSetupProgress` requires, and names that permission. **Never an empty form** — that reads as *there is nothing to set up*.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.10.2 | White Label Branding | Marketing & CRM | CONTRACTED | `getSiteSetupProgress` |
| 2.6.1 | B2C website should support: 1.Home page 1) Banners display packages, upgrades, and discounts 2) All available products are shown by category: Packages, Tickets, Experiences, Annual Passes, Others 3) … | Ticketing Sales | CONTRACTED | data `BookingFlow` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The "Category display" configuration control is retired and has no effect: remove it. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W7 Config: Category display · DI-1009)*
- CMS option to list a product (e.g. training courses) with full details but no Book button; instead show "Contact sales to book" with contact details. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W3 View-only products · DI-1004)*
- Each client owns its Apple and Google developer accounts; the app is built in the CMS from a published configuration, with an in-platform guide (D-U-N-S number, opening accounts, store listing, store review). *(agreed · MoM 24 Sep 2026, M24-08 · DI-998)*
- The CMS is a step-based site builder started from the workspace; a preset keeps the minimum path short (modules, booking flows, home sections and mobile tabs proposed), so an operator supplies only a logo, four colours and Publish; aim about 30 minutes to a working site. *(agreed · MoM 24 Sep 2026, M24-05 · DI-997)*
- Confirmed final: cart sliding in from the right or bottom, card size options, and cart-sidebar placement left or right; Qossai specifically liked the compact card size. No further changes requested. *(agreed · MoM 24 Sep 2026, 4.10 Guest Web App — Card Layout & Cart Configuration Confirmed · DI-991)*
- The hero banner and marketing layer (images, video, search, browse-by-venue, venue info) is optional and toggled in the white-label builder: on for clients without their own marketing site (Qossai: roughly 30%), off for a lean direct-to-ticket flow. *(agreed · MoM 18 Sep 2026, 4.11 Guest Website UX Review — Page Structure & Hero Banner Flexibility · DI-945)*
- Decision (raised by Qossai): the CMS/website builder supports two modes per client using the same builder — a full landing page plus integrated ticket-sale flow (clients without a website), or B2C-only (header, product cards, footer, checkout) embedded in/linked from an existing site. *(agreed · MoM 21 Aug 2026, 4.9 Website Builder Flexibility — Standalone vs. B2C-Only Configuration · DI-431)*

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
| Flow type key (`bookingFlows.flowTypeKey`) | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour … | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | The flow types the system catalogue offers (decided 29 September, W12; impact.md b). |
| Booking flows name (`bookingFlows.name`) | max length 80 | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Staff-facing, e.g. "Day pass, date first". |
| Is default for type (`bookingFlows.isDefaultForType`) | At most one per venue and type; setting it takes it from the previous default. | off | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | At most one per venue and type; setting it takes it from the previous default. |
| Booking flows is enabled (`bookingFlows.isEnabled`) | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | A disabled flow is kept and not published; products naming it fall back to the default. |
| Steps (`bookingFlows.steps`) | at most 30 | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Every step of the type, in the venue's order. Filled from the type when left out on create. |
| Steps: step key (`bookingFlows.steps[].stepKey`) | Location · Help me choose · Product · Date · Time · Performance · Level · Language · Duration · Route · Party size · Resource map … | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Every step a guest booking flow can hold (decided 29 September, W12). What each step does on WEB and MOB, and which screen draws it, is in the screen definitions of P01 and P02; which types carry which steps is … |
| Steps: enabled (`bookingFlows.steps[].enabled`) | A `required` step cannot be off; the flow saves and `isValid` turns false. | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | A `required` step cannot be off; the flow saves and `isValid` turns false. |
| Steps: sort order (`bookingFlows.steps[].sortOrder`) | min 0 | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Steps: settings (`bookingFlows.steps[].settings`) | A name the type does not give is refused with 400. | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. |
| Settings (`bookingFlows.settings`) | — | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | The settings that belong to one flow, not to the venue (decided 29 September, W12). |
| Settings: performance reveal (`bookingFlows.settings.performanceReveal`) | Date time ticket · All at once | Date time ticket | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Performance reveal (rev 3 REV3-2). `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. |
| Settings: sign in at (`bookingFlows.settings.signInAt`) | After add ons · At payment | After add ons | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3). |
| Settings: seat event date mode (`bookingFlows.settings.seatEventDateMode`) | Inline step · Popup on seat map; Read only by the seated flow types. | Inline step | GST-007, GST-008, GST-009, GST-041, GST-049, WEB-005, WEB-006, WEB-007 … (12) | Date and time on a seated event (rev 3 REV3-4). `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. |
| Settings: extras step (`bookingFlows.settings.extrasStep`) | Auto · Always · Never; `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. | Auto | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. |
| Settings: quick tour (`bookingFlows.settings.quickTour`) | — | off | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Quick tour (rev 3 REV3-20). A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. |
| Settings: consent questions (`bookingFlows.settings.consentQuestionIds`) | at most 10; no duplicates; Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | The flow's own consent questions (rev 3 REV3-26). Asked on every booking through this flow, together with those of each product in the cart, each question once. |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-102` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-102?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save and continue, Add these flows, Check what blocks a publish.
- [ ] Every transition is wired: `CMS-105`, `CMS-001`, `CMS-103`, `CMS-103`, `CMS-101`, `CMS-007`, `CMS-009`, `CMS-002`, `CMS-004`, `CMS-008`, `CMS-005`, `CMS-003`, `CMS-009`, `CMS-004`, `CMS-007`, `CMS-006`, `CMS-012`, `CMS-014`, `CMS-015`, `CMS-104`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 7 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-103` Booking Flows

**Pick the venue's booking flows, turn optional steps on or off, set the step order within the allowed limits with a live preview, assign flows to products and categories, and validate them before they publish with the site.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · ticket #28337 (APP-WL-CMS-103) |
| Who uses it | venue staff holding `GUEST_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE`, `TENANT_PUBLISH` (2 read, 3 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listBookingFlows` reads the venue's flows and `getBookingFlow` reads one of them to compose — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `bookingFlowId` (CMS-102), `productId` (navigation) · cold entry: Resolves the venue from the session and opens on the flow list, or on the flow named in the link. |
| Route | `/white-label/booking-flows` |

**What the spec says about it.** **Added 29 September for W12: operators pick their ticketing flows, see which steps are required, optional or conditional, and set their own order.** The catalogue (`listBookingFlowTypes`) is the same for every tenant: dated day pass, timed entry, open-dated, seated (fixed performance, or date and time then seat map), experience or workshop (product first, W8), surf or session (time then level), meeting room by the hour, cabana on a map or by size (W6), guided tour by language, transport, table reservation, membership, gift card and several locations. Flows reach guests with the rest of the site (`publishTenantConfig`); WEB-005..012, GST-007..009 and GST-041 order their steps from the published flow.

**From the White Label & CMS process.** Pick the venue's booking flows from the fixed catalogue, turn optional steps on or off, reorder within the type's constraints with a live preview, set step and flow settings, assign flows to products and categories, and validate. Flows publish with the whole site. The one thing to get right: a drag that breaks a constraint is refused before it lands, with the constraint in words.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The surfSession type's level step has a broken stepSettings note in the contract (a stray key "from the products' segmentTags" with a null value). (CHG-SGU-024)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue | select field | — | — | — | — | The venue whose flows are shown (path `venueId`); defaults to the session venue. | — |
| Flow type | select field | — | — | — | — | Sends `?flowTypeKey=`. | — |
| Consent questions this flow asks | multi-picker: choose consent questions | optional | — | at most 10; no duplicates; Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. | — | **The questions every booking in this flow asks, whatever the product** (rev 3 REV3-26), e.g. a water park's "Are you able to swim?". Options are the active questions from `listConsentQuestions` … | `BookingFlowLevelSettings.consentQuestionIds` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Flow type key | select | — | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour by language · Transport … | `listBookingFlows` ?flowTypeKey |
| Product kind | text field | — | — | `listBookingFlowTypes` ?productKind |
| Kind | radio group | — | Swim · Scuba · Risk · Custom | `listConsentQuestions` ?kind |
| Status | segmented control | — | Active · Retired | `listConsentQuestions` ?status |

**Form: Add a flow** (modal, opened by *Add a flow*; *Add flow* calls `createBookingFlowDefinition`, *Cancel* sends nothing)

**Collects what `createBookingFlowDefinition` sends.** Required: `flowTypeKey` (from the cards), `name`. Optional: `isDefaultForType`, `steps` (left out, the type's defaults), `settings`. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Flow type key `flowTypeKey` | select | required | — | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour by language · Transport … | — | The flow types the system catalogue offers (decided 29 September, W12; impact.md b). | `createBookingFlowDefinition` body |
| Name `name` | text field | required | — | max length 80 | — | Staff-facing, e.g. "Day pass, date first". | `createBookingFlowDefinition` body |
| Is default for type `isDefaultForType` | toggle | optional | off | At most one per venue and type; setting it takes it from the previous default. | — | At most one per venue and type; setting it takes it from the previous default. | `createBookingFlowDefinition` body |
| Is enabled `isEnabled` | toggle | optional | on | — | — | A disabled flow is kept and not published; products naming it fall back to the default. | `createBookingFlowDefinition` body |
| Steps `steps` | repeatable rows | optional | — | at most 30 | — | Every step of the type, in the venue's order. Filled from the type when left out on create. | `createBookingFlowDefinition` body |
| Step key `steps[].stepKey` | select | required | — | Location · Help me choose · Product · Date · Time · Performance · Level · Language · Duration · Route · Party size · Resource map … | — | Every step a guest booking flow can hold (decided 29 September, W12). What each step does on WEB and MOB, and which screen draws it, is in the screen definitions of P01 and P02 … | `createBookingFlowDefinition` body |
| Enabled `steps[].enabled` | toggle | required | — | A `required` step cannot be off; the flow saves and `isValid` turns false. | — | A `required` step cannot be off; the flow saves and `isValid` turns false. | `createBookingFlowDefinition` body |
| Sort order `steps[].sortOrder` | number field | required | — | min 0 | — | — | `createBookingFlowDefinition` body |
| Settings `steps[].settings` | key and value settings | optional | — | A name the type does not give is refused with 400. | — | The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. | `createBookingFlowDefinition` body |
| Settings `settings` | group | optional | — | — | — | The settings that belong to one flow, not to the venue (decided 29 September, W12). | `createBookingFlowDefinition` body |
| Performance reveal `settings.performanceReveal` | segmented control | optional | Date time ticket | Date time ticket · All at once | — | Performance reveal (rev 3 REV3-2). `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. | `createBookingFlowDefinition` body |
| Sign in at `settings.signInAt` | segmented control | optional | After add ons | After add ons · At payment | — | Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3). | `createBookingFlowDefinition` body |
| Seat event date mode `settings.seatEventDateMode` | segmented control | optional | Inline step | Inline step · Popup on seat map; Read only by the seated flow types. | — | Date and time on a seated event (rev 3 REV3-4). `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. | `createBookingFlowDefinition` body |
| Extras step `settings.extrasStep` | segmented control | optional | Auto | Auto · Always · Never; `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. | — | `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. | `createBookingFlowDefinition` body |
| Quick tour `settings.quickTour` | toggle | optional | off | — | — | Quick tour (rev 3 REV3-20). A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. | `createBookingFlowDefinition` body |
| Consent questions `settings.consentQuestionIds` | multi-picker: choose consent questions | optional | — | at most 10; no duplicates; Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. | — | The flow's own consent questions (rev 3 REV3-26). Asked on every booking through this flow, together with those of each product in the cart, each question once. | `createBookingFlowDefinition` body |

Errors to draw in the form: 400 An unknown flow type, a step the type does not have, or a step given twice; 403 Authenticated but not permitted at the requested scope

**Form: Remove flow** (confirmDialog, opened by *Remove flow*; *Remove* calls `deleteBookingFlow`, *Keep it* sends nothing)

Names the flow and says guests keep it until the next publish. Refused `409` while products or categories name it, and names them.

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 A product or category still names this flow, or it is the default for products on sale; the problem names them

**Form: Publish site** (confirmDialog, opened by *Publish site*; *Publish* calls `publishTenantConfig`, *Cancel* sends nothing)

**Names what goes live**: the changed flows and the products whose booking steps change, with the rest of the draft. Asks for the publish note `publishTenantConfig` requires.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Note `note` | text area | required | — | min length 3; max length 500 | — | — | `publishTenantConfig` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Publish at a future time. Useful for a campaign launch. | `publishTenantConfig` body |

Errors to draw in the form: 409 Validation failed. (ConfigValidationProblem)

**Sent by *Save flow*** (`updateBookingFlowDefinition`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 80 | — | — | `updateBookingFlowDefinition` body |
| Is default for type `isDefaultForType` | toggle | optional | — | — | — | — | `updateBookingFlowDefinition` body |
| Is enabled `isEnabled` | toggle | optional | — | — | — | — | `updateBookingFlowDefinition` body |
| Steps `steps` | repeatable rows | optional | — | at least 1; at most 30 | — | — | `updateBookingFlowDefinition` body |
| Step key `steps[].stepKey` | select | required | — | Location · Help me choose · Product · Date · Time · Performance · Level · Language · Duration · Route · Party size · Resource map … | — | Every step a guest booking flow can hold (decided 29 September, W12). What each step does on WEB and MOB, and which screen draws it, is in the screen definitions of P01 and P02 … | `updateBookingFlowDefinition` body |
| Enabled `steps[].enabled` | toggle | required | — | A `required` step cannot be off; the flow saves and `isValid` turns false. | — | A `required` step cannot be off; the flow saves and `isValid` turns false. | `updateBookingFlowDefinition` body |
| Sort order `steps[].sortOrder` | number field | required | — | min 0 | — | — | `updateBookingFlowDefinition` body |
| Settings `steps[].settings` | key and value settings | optional | — | A name the type does not give is refused with 400. | — | The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. | `updateBookingFlowDefinition` body |
| Settings `settings` | group | optional | — | — | — | The settings that belong to one flow, not to the venue (decided 29 September, W12). | `updateBookingFlowDefinition` body |
| Performance reveal `settings.performanceReveal` | segmented control | optional | Date time ticket | Date time ticket · All at once | — | Performance reveal (rev 3 REV3-2). `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. | `updateBookingFlowDefinition` body |
| Sign in at `settings.signInAt` | segmented control | optional | After add ons | After add ons · At payment | — | Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3). | `updateBookingFlowDefinition` body |
| Seat event date mode `settings.seatEventDateMode` | segmented control | optional | Inline step | Inline step · Popup on seat map; Read only by the seated flow types. | — | Date and time on a seated event (rev 3 REV3-4). `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. | `updateBookingFlowDefinition` body |
| Extras step `settings.extrasStep` | segmented control | optional | Auto | Auto · Always · Never; `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. | — | `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. | `updateBookingFlowDefinition` body |
| Quick tour `settings.quickTour` | toggle | optional | off | — | — | Quick tour (rev 3 REV3-20). A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. | `updateBookingFlowDefinition` body |
| Consent questions `settings.consentQuestionIds` | multi-picker: choose consent questions | optional | — | at most 10; no duplicates; Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. | — | The flow's own consent questions (rev 3 REV3-26). Asked on every booking through this flow, together with those of each product in the cart, each question once. | `updateBookingFlowDefinition` body |

**Sent by *Validate*** (`validateBookingFlow`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Steps `steps` | repeatable rows | optional | — | at most 30 | — | — | `validateBookingFlow` body |
| Step key `steps[].stepKey` | select | required | — | Location · Help me choose · Product · Date · Time · Performance · Level · Language · Duration · Route · Party size · Resource map … | — | Every step a guest booking flow can hold (decided 29 September, W12). What each step does on WEB and MOB, and which screen draws it, is in the screen definitions of P01 and P02 … | `validateBookingFlow` body |
| Enabled `steps[].enabled` | toggle | required | — | A `required` step cannot be off; the flow saves and `isValid` turns false. | — | A `required` step cannot be off; the flow saves and `isValid` turns false. | `validateBookingFlow` body |
| Sort order `steps[].sortOrder` | number field | required | — | min 0 | — | — | `validateBookingFlow` body |
| Settings `steps[].settings` | key and value settings | optional | — | A name the type does not give is refused with 400. | — | The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. | `validateBookingFlow` body |

**Sent by *Assign to product*** (`updateProduct`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Family key `familyKey` | text field | optional | — | max length 64; pattern `^[A-Za-z0-9_-]+$`; At most one product per venue in a family, else `409 duplicate-code`. | — | The product family across the tenant's venues (decided 29 September, rev 3 REV3-18); see `Product.familyKey`. | `updateProduct` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `updateProduct` body |
| Description `description` | text area | optional | — | — | — | — | `updateProduct` body |
| Name localised `nameLocalised` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | See `Product.nameLocalised` (CHG-R4-011). Replaces the whole map; null clears it. | `updateProduct` body |
| Description localised `descriptionLocalised` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | See `Product.descriptionLocalised` (CHG-R4-011). Replaces the whole map; null clears it. | `updateProduct` body |
| Channels `channels` | multi-select chips | optional | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `updateProduct` body |
| Data mask values `dataMaskValues` | key and value settings | optional | — | — | — | — | `updateProduct` body |
| Guest listing `guestListing` | segmented control | optional | Bookable | Bookable · Info only · Hidden; `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. | — | How a product appears to a guest (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. | `updateProduct` body |
| Not bookable label `notBookableLabel` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Keyed by ISO 639-1 code. Every enabled language should be present. | `updateProduct` body |
| Sales contact `salesContact` | group | optional | — | — | — | See `Product.salesContact` (W3, 29 September). | `updateProduct` body |
| Phone `salesContact.phone` | phone field | optional | — | max length 32 | +971 5X XXX XXXX (E.164) | — | `updateProduct` body |
| Email `salesContact.email` | email field | optional | — | max length 254 | name@example.ae | — | `updateProduct` body |
| Note `salesContact.note` | text, one per language | optional | — | At most 200 characters per language. | English and Arabic (Arabic right to left) | A line shown under the contact, e.g. *Group courses are booked by phone*. | `updateProduct` body |
| Booking flow `bookingFlowId` | picker: choose a booking flow | optional | — | — | shows names, sends the id | See `Product.bookingFlowId` (W8, W12, 29 September). | `updateProduct` body |
| Display tags `displayTags` | repeatable rows | optional | — | at most 6 | — | — | `updateProduct` body |
| Kind `displayTags[].kind` | radio group | required | — | Clock · Height · Free · Calendar · ID | — | `clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring. | `updateProduct` body |
| Label `displayTags[].label` | text, one per language | required | — | Each language value at most 40 characters. | English and Arabic (Arabic right to left) | What the guest reads, e.g. *2 Hours*. | `updateProduct` body |
| Media `media` | repeatable rows | optional | — | at most 20 | — | — | `updateProduct` body |
| Asset `media[].assetId` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | A `MediaAsset` of `assets.yaml`, in status `ready`. | `updateProduct` body |
| Kind `media[].kind` | segmented control | required | — | Image · Video | — | — | `updateProduct` body |
| Is primary `media[].isPrimary` | toggle | required | off | — | — | The item *Read more* opens on and a listing shows. Exactly one per product. | `updateProduct` body |
| Display order `media[].displayOrder` | number field | optional | 100 | — | — | — | `updateProduct` body |
| Alt text `media[].altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Keyed by ISO 639-1 code. Every enabled language should be present. | `updateProduct` body |
| Consent questions `consentQuestionIds` | multi-picker: choose consent questions | optional | — | at most 10; no duplicates | — | — | `updateProduct` body |
| Requires time window `requiresTimeWindow` | toggle | optional | — | — | — | — | `updateProduct` body |

**Sent by *Assign to category*** (`setProductCategories`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Categories `categories` | repeatable rows | required | — | — | — | — | `setProductCategories` body |
| ID `categories[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setProductCategories` body |
| Name `categories[].name` | text field | required | — | — | — | — | `setProductCategories` body |
| Code `categories[].code` | text field | optional | — | max length 64 | — | Taken from their category tables, 20 September. Ours had a uuid and a localised name, so an importer matching *Beverages* had to match on a display string that a venue is free to … | `setProductCategories` body |
| Name localised `categories[].nameLocalised` | key and value settings | optional | — | — | — | — | `setProductCategories` body |
| Kind `categories[].kind` | radio group | required | — | Category · Brand · Collection · Season · Department | — | — | `setProductCategories` body |
| Parent `categories[].parentId` | picker: choose a parent | optional | — | — | shows names, sends the id | One tree, not four. A brand under a department under a category is how a real merchandise hierarchy runs, and separate tables for each level cannot express a venue that nests them … | `setProductCategories` body |
| Display order `categories[].displayOrder` | number field | optional | 100 | — | — | — | `setProductCategories` body |
| Image `categories[].imageAssetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `setProductCategories` body |
| Description `categories[].description` | text, one per language | optional | — | Each language value at most 200 characters. | English and Arabic (Arabic right to left) | The short line a guest reads under a category option, e.g. *Surf lessons: learn on the beginner wave with a coach* (decided 29 September, rev 3 REV3-19). | `setProductCategories` body |
| Booking flow `categories[].bookingFlowId` | picker: choose a booking flow | optional | — | — | shows names, sends the id | The booking flow for every product filed here that names none of its own (decided 29 September, W12, BO-115). | `setProductCategories` body |
| Is active `categories[].isActive` | toggle | optional | on | — | — | Deactivated rather than deleted. A category with a season behind it still names the products sold under it, and removing it rewrites last year's report. | `setProductCategories` body |

**Rules for these inputs** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **flowTypeKey**: Cards for the 16 types (dated day pass, timed entry, open-dated, seated fixed performance, seated date-time-seat map, workshop, surf or session, meeting room, cabana on a map, cabana by size, guided tour by language, transport, table reservation, membership, gift card, several locations), each listing its steps with Required / Optional / Conditional marks. *(source: contracts/satellite/white-label.yaml#/components/schemas/BookingFlowType)*
- **steps[] order and enabled**: Drag handles; Required steps locked on; Conditional steps show their condition in words (e.g. "Only when the tenant has more than one venue"). Each drop is checked with validateBookingFlow and the proposed steps before it lands. *(source: contracts/satellite/white-label.yaml#validateBookingFlow)*
- **step settings**: Only the names the type gives (e.g. tour languages, room hours 1-8 by 60 minutes, party size 1-12); an unknown name is refused (400). *(source: contracts/satellite/white-label.yaml#/components/schemas/BookingFlowStep)*
- **flow settings**: Performance reveal Date then time then ticket (default) / All at once; sign in After add-ons (default) / At payment; seated date Inline (default) / Pop-up over the seat map; extras Auto / Always / Never; Quick tour off by default; up to 10 consent questions. *(source: DI-1042; DI-1043; DI-1044; DI-1060; contracts/satellite/white-label.yaml#/components/schemas/BookingFlowLevelSettings)*

#### Outputs: what the screen shows and produces

**Shown**

**The venue's flows** (data table, from `listBookingFlows`): An invalid flow is marked and blocks the site's publish until it is fixed.

| Shows | Format | Notes |
|---|---|---|
| Name | text | Staff-facing, e.g. "Day pass, date first". |
| Flow type key | chip: Dated day pass, Timed entry, Open dated, Seated fixed performance, Seated date time … | The flow types the system catalogue offers (decided 29 September, W12; impact.md b). |
| Is default for type | yes / no (icon or chip) | At most one per venue and type; setting it takes it from the previous default. |
| Is enabled | yes / no (icon or chip) | A disabled flow is kept and not published; products naming it fall back to the default. |
| Is valid | yes / no (icon or chip) | Whether the flow passes `validateBookingFlow`; worked out in the same transaction as each write. |
| Updated at | 1 Oct 2026, 14:30 | — |

**Flow types to pick from** (card list, from `listBookingFlowTypes`): Each card lists the type's steps with their required, optional or conditional mark, so the choice is made knowing what the guest will go through.

| Shows | Format | Notes |
|---|---|---|
| Key | chip: Dated day pass, Timed entry, Open dated, Seated fixed performance, Seated date time … | The flow types the system catalogue offers (decided 29 September, W12; impact.md b). |
| Name | in the reader's language | Keyed by ISO 639-1 code. Every enabled language should be present. |
| Description | in the reader's language | Keyed by ISO 639-1 code. Every enabled language should be present. |
| Product kinds | list or chips (count when long) | The catalogue `ProductKind` values this type books. A venue's default flow for a type serves every product of these kinds that names no … |
| Steps | list or chips (count when long) | In the type's default order. |

**Compose the steps** (detail panel, from `getBookingFlow`): **The step list, in the venue's order.** Each step carries its mark: *Required* (locked on), *Optional* (a switch) or *Conditional* (a switch, with the condition in words, e.g. "only when the tenant has more than one venue"). Steps are dragged to reorder; **a drop that breaks a constraint is refused before it lands** (`validateBookingFlow` with the proposed `steps`), and the constraint is named …

| Shows | Format | Notes |
|---|---|---|
| Name | text | Staff-facing, e.g. "Day pass, date first". |
| Flow type key | chip: Dated day pass, Timed entry, Open dated, Seated fixed performance, Seated date time … | The flow types the system catalogue offers (decided 29 September, W12; impact.md b). |
| Is default for type | yes / no (icon or chip) | At most one per venue and type; setting it takes it from the previous default. |
| Is enabled | yes / no (icon or chip) | A disabled flow is kept and not published; products naming it fall back to the default. |
| Steps | list or chips (count when long) | Every step of the type, in the venue's order. Filled from the type when left out on create. |
| Is valid | yes / no (icon or chip) | Whether the flow passes `validateBookingFlow`; worked out in the same transaction as each write. |

**This flow's settings** (detail panel, from `getBookingFlow`): **Moved here from Site Settings on 29 September (W12)**, because they belong to one flow: date, time then tickets or all at once (REV3-2); sign in after add-ons or at payment (REV3-3); a seated event's date inline or over the seat map (REV3-4, seated flows only); the extras step auto, always or never; the quick tour (REV3-20); the flow's consent questions (REV3-26).

| Shows | Format | Notes |
|---|---|---|
| Performance reveal | chip: Date time ticket, All at once | Performance reveal (rev 3 REV3-2). `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked … |
| Sign in at | chip: After add ons, At payment | Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3). |
| Seat event date mode | chip: Inline step, Popup on seat map | Date and time on a seated event (rev 3 REV3-4). `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a … |
| Extras step | chip: Auto, Always, Never | `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. |
| Quick tour | yes / no (icon or chip) | Quick tour (rev 3 REV3-20). A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. |
| Consent questions | list or chips (count when long) | The flow's own consent questions (rev 3 REV3-26). Asked on every booking through this flow, together with those of each product in the … |

**Preview** (live preview): **The flow as a guest meets it, step by step, on web and on mobile**, redrawn on every change and drawn from the record in hand. Calls nothing and publishes nothing; guests keep the published flow (`getPublishedBookingFlow`, shown beside it for comparison) until the site is published.

**Products and categories using this flow** (data table, from `listProducts`): Assign the flow to a product (`updateProduct` `bookingFlowId`) or a category (`setProductCategories`, the category's `bookingFlowId`). A product naming no flow uses its category's, then the venue's default for its kind. Set up also on BO-007/BO-008 and BO-115.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Category | the name it points at, never the id | Taken from their `fnb.product` and `retail.product`, 20 September. `catalogue.product_category` has existed since 20 August with two … |
| Booking flow | the name it points at, never the id | The booking flow this product is sold through (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders … |

**Why this flow cannot publish** (banner, from `validateBookingFlow`): A required step turned off, a step out of its allowed order, a condition that can never hold, each naming the step and the fix.

| Shows | Format | Notes |
|---|---|---|
| Valid | yes / no (icon or chip) | — |
| Problems | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What publishing changes (publish gate) | navigation or local | — | — | — | — |
| Add a flow (primary button) | `createBookingFlowDefinition` POST `/venues/{venueId}/booking-flows` | BookingFlow | BookingFlow | 400 An unknown flow type, a step the type does not have, or a step given twice; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Save flow (secondary button) | `updateBookingFlowDefinition` PATCH `/booking-flows/{bookingFlowId}` | inline | BookingFlow | 400 A step the type does not have, or a step given twice; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Validate (secondary button) | `validateBookingFlow` POST `/booking-flows/{bookingFlowId}/validate` | inline | BookingFlowValidation | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Assign to product (secondary button) | `updateProduct` PATCH `/products/{productId}` | UpdateProductRequest | Product | 400 `media` with no `isPrimary` item or more than one, or one asset twice.; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a … | — |
| Assign to category (secondary button) | `setProductCategories` PUT `/product-categories` | inline | ProductCategory[] | 400 The body contains a cycle — a category that is its own ancestor — or a `parentId` that names no category in the body.; 409 The body leaves out a category that products name (send it with `isActive` false rather than … | — |
| Publish site (secondary button) | `publishTenantConfig` POST `/tenant-config/publish` | inline | ConfigVersion | 409 Validation failed. (ConfigValidationProblem) | gated `TENANT_PUBLISH`; opens confirmDialog first |
| Remove flow (destructive button) | `deleteBookingFlow` DELETE `/booking-flows/{bookingFlowId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 A product or category still names this flow, or it is the default for products on sale; the problem names them | opens confirmDialog first |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Live preview**: The flow step by step on web and mobile, with the step indicator style from CMS-016, beside the published flow for comparison. *(source: screens/P13-white-label-cms.yaml#CMS-103)*
- **Validation**: Problems by kind (required step off, order broken, condition never holds, step not in type, duplicate, unknown setting) each naming the step and the fix. *(source: contracts/satellite/white-label.yaml#/components/schemas/BookingFlowValidation)*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Save flow**: Saves to the draft even when invalid (isValid false), so work can stop halfway; the publish refuses an invalid enabled flow. *(source: contracts/satellite/white-label.yaml#updateBookingFlowDefinition)*
- **Remove flow**: Refused 409 while products or categories name it or it is the default for products on sale; offer reassignment. *(source: contracts/satellite/white-label.yaml#deleteBookingFlow)*

**Data it reads**: `listBookingFlows` (onLoad, The venue's flows in the draft); `listBookingFlowTypes` (onLoad, The flow types to pick from, with their steps and order …); `listConsentQuestions` (onLoad, The consent questions a flow can ask (rev 3 REV3-26))

**Where the user goes next**

- → `CMS-102` Site Builder: *Back to the Site Builder*
- → `CMS-016` Site Settings: *Venue-wide booking settings*
- → `CMS-101` Help Me Choose: *Help me choose*
- → `CMS-014` Publishing Workflow: *Publish with the site*; carries `version`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue's flows and the flow-type catalogue, read by `listBookingFlows` and `listBookingFlowTypes`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the flows untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **No flows at this venue yet.** Guests book through each type's default order until one is picked. Offers the flow-type cards and, from the Site Builder, the preset's flows in one step. |
| Empty, no results (`?state=emptyNoResults`) | The flow-type filter matched nothing and the venue's other flows are still there. Names the filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `listBookingFlows` requires to show this screen, and names that permission (the screen's other reads need `GUEST_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `updateProduct`, `setProductCategories` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 A step the type does not have, or a step given twice; 400 An unknown flow type, a step the type does not have, or a step given twice; 400 The body contains a cycle — a category that is its own ancestor — or a `parentId` that names no … |

#### Edge cases to draw

- **Turning extras off for a flow whose products have add-ons**: Allowed; the preview shows the flow collapse to Tickets -> Cart -> Checkout. *(source: DI-428)*
- **A product names a disabled flow**: It falls back to the venue default for its kind; show which products fall back. *(source: contracts/satellite/white-label.yaml#/components/schemas/BookingFlow)*

#### Consistency with other screens

- Match `CMS-016`: Venue-wide settings shown read-only beside the step that uses them.
- Match `WEB-006`: Times per page, day parts and reveal order drawn there follow these settings.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Coastal Aqua Yas Island
flow:
  name: Day pass with cabana
  type: cabanaMap
  steps:
  - date
  - resourceMap
  - consent
  - extras
  - review
  - payment
  settings:
    signInAt: afterAddOns
    extrasStep: auto
invalidDrop: 'Payment can''t move above Review: payment is always last.'
```

#### Permissions

- `listBookingFlows` → `TENANT_CONFIGURE` (configure) · staff
- `listBookingFlowTypes` → `TENANT_CONFIGURE` (configure) · staff
- `getBookingFlow` → `TENANT_CONFIGURE` (configure) · staff
- `getPublishedBookingFlow` → no permission · guest, staff
- `createBookingFlowDefinition` → `TENANT_CONFIGURE` (configure) · staff
- `updateBookingFlowDefinition` → `TENANT_CONFIGURE` (configure) · staff
- `validateBookingFlow` → `TENANT_CONFIGURE` (configure) · staff
- `deleteBookingFlow` → `TENANT_CONFIGURE` (configure) · staff
- `publishTenantConfig` → `TENANT_PUBLISH` (configure) · staff
- `listConsentQuestions` → `GUEST_VIEW` (read) · staff
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `updateProduct` → `PRODUCT_CONFIGURE` (configure) · staff
- `listProductCategories` → `PRODUCT_VIEW` (read) · staff, guest
- `setProductCategories` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `listBookingFlows` requires to show this screen, and names that permission (the screen's other reads need `GUEST_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `updateProduct`, `setProductCategories` …

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.24 | White Label Configuration Portal - System shall provide self-service white label configuration. | Guest Mobile App & Branding | CONTRACTED | `publishTenantConfig` |
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 1.1.46 | Support multilingual product descriptions | Ticketing Catalogue | CONTRACTED | `updateProduct` |
| 1.4.18 | System shall track product owners, creators, approvers and responsible departments. | Ticketing Catalogue | CONTRACTED | `updateProduct` |
| 1.4.19 | System shall allow products to be assigned to specific sales channels, locations, venues or customer segments. | Ticketing Catalogue | CONTRACTED | `updateProduct` |
| 1.4.20 | System shall support multilingual product descriptions, content, images and sales information. | Ticketing Catalogue | CONTRACTED | `updateProduct` |
| 2.6.1 | B2C website should support: 1.Home page 1) Banners display packages, upgrades, and discounts 2) All available products are shown by category: Packages, Tickets, Experiences, Annual Passes, Others 3) … | Ticketing Sales | CONTRACTED | data `BookingFlow` |
| 8.8.1 | A price for a PLU is changing depending on the date of visit. I can sell today a product to be used after a price change at the new price defined in the sales calendar. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.2 | System shall support future-dated pricing schedules. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.3 | System shall support pricing by visit date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Step-indicator style is configurable, the same as on the web: bars, dots, counters or step names. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1093)*
- Existing booking settings stay: step indicator, extras step, seat picker, map view, quantities on add-ons (−/+ stepper, price multiplies), embed mode, hero banner, search in banner, single-event page. Defaults: search in banner off, seat picker = bowl. *(agreed · design review 29 Sep 2026, CFG-6 · Step indicator; Extras step; Seat picker; Map view; Quantities on add-ons; Embed mode; Hero banner; Search in banner; Single-event page · DI-1070)*
- A UI preset (L1–L6, or Custom) picks a bundle of booking-UI settings per venue type. *(agreed · design review 29 Sep 2026, CFG-1 · Preset (UI preset L1-L6, Custom) · DI-1065)*
- Booking-flow settings are set per tenant with a per-venue override; the CMS booking-flow settings screen must show tenant defaults and venue overrides. *(agreed · rev 3 design review 29 Sep 2026, CFG-11 · Where the settings live · DI-1063)*
- On a guest's first booking visit, a four-step coach-mark tour highlights date, time, tickets and basket, with Back, Next / Done and End tour; a "Quick tour" button on the booking page replays it. Setting "Quick tour", default off; first-visit flag kept on the device only. *(agreed · rev 3 design review 29 Sep 2026, REV3-20 · 20. Enable or disable a Quick Tour that describes the customer journey · DI-1060)*
- Multi-location attractions: the guest picks a location first (e.g. Al Barsha, Mirdif, Yas Island, Sharjah); a "Booking at" bar on later booking steps has Change location. On a switch, times and prices refresh and the selection is cleared unless the products share a family. Setting "Location switcher". *(agreed · rev 3 design review 29 Sep 2026, REV3-18 · 18. One tenant with an attraction in several locations; change location · DI-1058)*
- Category tiles (e.g. Permanent exhibition, Temporary exhibitions, Guided tours, Courses & workshops), then that category's tickets with Adult / Child / Student counters. Setting "Ticket categories": Category → subcategory (default) or Flat list (all tickets under category headings). *(agreed · rev 3 design review 29 Sep 2026, REV3-16 · 16. Choose category, then subcategory, configurable in the CMS · DI-1056)*
- Cart & summary options: sidebar fixed right, sidebar left, slide-in right, slide-up bottom, floating cart icon (round basket button with item count opening the slide-in basket), single column. In Arabic the basket stays on the right by default (client confirmed); "Cart side in Arabic" can mirror to left. *(agreed · rev 3 design review 29 Sep 2026, REV3-10 · 10. Cart display: fixed on right, slide bar, icon, bottom; right for Arabic · DI-1051)*
- A time bar above the seat map shows the chosen performance, lets the guest switch show and has Change date; switching releases held seats. Setting "Time bar above seat map", default on. On the selection step, time sits directly under the date, above language & format and tickets. *(agreed · rev 3 design review 29 Sep 2026, REV3-6 · 6. Time selection on top, configurable · DI-1046)*
- The 'view from your seat' box can sit Bottom (default), Right, Left or Top of the seat map (web only); on narrow screens and mobile it is always below the map. Setting "Seat view box". *(agreed · rev 3 design review 29 Sep 2026, REV3-5 · 5. CMS option to show the seat view right, left, top or bottom · DI-1045)*
- Seated events with one on-sale performance go straight to the seat map (Flow 1). Otherwise date and time come first (Flow 2), either as an inline step (timed-ticket style, default) or as a pop-up dialog over the seat map. Setting "Date & time on seat events". *(agreed · rev 3 design review 29 Sep 2026, REV3-4 · 4. Flow 1 (fixed date and time) and Flow 2 (select date, then time, then seat map) · DI-1044)*
- Sign-in (or the guest code when guest checkout is on) is asked when the guest leaves the Add-ons step; the basket is kept. Setting "Ask to sign in": After add-ons (default) or At payment. *(agreed · rev 3 design review 29 Sep 2026, REV3-3 · 3. The sign-in screen should appear after Add-ons · DI-1043)*
- Dated flows reveal in order: date, then time (hidden until a date is picked), then tickets (hidden until a time is picked), with a hint in place telling the guest what to pick next; Continue off until both chosen. Setting "Performance reveal": Date → time → ticket (default) or All at once. *(agreed · rev 3 design review 29 Sep 2026, REV3-2 · 2. Step 1 date, step 2 time (only after the date), step 3 ticket · DI-1042)*
- More than eight times show as compact time tiles, paged with Earlier / Later (Times per page 8/12/24/all, default 24), with day-part chips (All, Morning, Afternoon, Evening) showing counts (filter on by default). Day-part boundaries are venue settings, default before 12:00 / 12:00–17:00 / from 17:00. *(agreed · rev 3 design review 29 Sep 2026, REV3-1 · 1. Many performances should resize and page; filter by morning, afternoon, evening · DI-1041)*
- Card layout is a choice, not free text: Stacked rows (default) · Split rows · Cards across · Poster cards. Card size: Compact (default) · Standard · Large · Extra large. Density: Compact (default) · Standard · Roomy. *(agreed · design review 29 Sep 2026, 6. Booking-flow configuration (CMS-016): card-layout options · DI-1040)*
- The date list in the event banner (for multi-date events) is a setting, "Dates in event banner", off by default. The date picker always sits at the top of the booking step. *(agreed · design review 29 Sep 2026, Settings 19. Why is there a date selection in the header? · DI-1033)*
- Each Adult / Child / Senior / Infant row has an (i) button showing who the ticket is for and what it includes (up to 300 characters). Setting "Extra info on cards", default on. *(agreed · design review 29 Sep 2026, Tickets 6. Extra information for each ticket in the ticket section · DI-1028)*
- Ticket cards, Read more and the listing side panel show tags (e.g. "2 Hours", "Min 1.10 m", "Free adult entry", "Valid 90 days", "Emirates ID"), each with a kind icon (clock, height, free, calendar, id), max 6. Venue-set tags win, else derived from duration, validity, height rule. Setting "Tags on tickets", default on. *(agreed · design review 29 Sep 2026, Tickets 3. 'Read more' should carry tags customisable per ticket type · DI-1025)*
- Cleaning buffer is configurable. Option A: fixed buffer (e.g. 15 min) after every booking. Option B: N cleanings per day; the system places the buffers into the day's schedule and adjusts availability. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W10 Meeting-room cleaning buffer · DI-1012)*
- The "Category display" configuration control is retired and has no effect: remove it. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W7 Config: Category display · DI-1009)*
- Map-based cabana booking stays optional per configuration, since not every operator uses the same flow; it uses the same map back end as theme-park F&B/locations (reusable later for in-park navigation). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W6 Cabanas · DI-1008)*
- CMS option to list a product (e.g. training courses) with full details but no Book button; instead show "Contact sales to book" with contact details. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W3 View-only products · DI-1004)*
- The prototype validated five booking-flow types (dated, multi-park, combo, annual pass, membership) and their skeleton screens; these flows are the basis for the real white-label builder. *(agreed · MoM 24 Sep 2026, 4.8 Guest Web App CMS Prototype — Feedback on Maturity & Scope Expectations · DI-989)*
- Each ticket type gets its own flow: open-dated (no calendar step, straight to guest category/quantity, valid e.g. 30-60 days), dated (date, then product), dated-with-time (date, time, product) and seated (date, time, seat selection). *(client request · MoM 18 Sep 2026, 4.13 Guest Website UX Review — Ticket Type Flows & Seat Map Selection · DI-948)*
- Decision (raised by Qossai): the CMS/website builder supports two modes per client using the same builder — a full landing page plus integrated ticket-sale flow (clients without a website), or B2C-only (header, product cards, footer, checkout) embedded in/linked from an existing site. *(agreed · MoM 21 Aug 2026, 4.9 Website Builder Flexibility — Standalone vs. B2C-Only Configuration · DI-431)*
- Decision: the add-ons step is optional/removable in configuration for products with no add-ons, collapsing the flow to Ticket Selection → Cart → Checkout. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-428)*
- Allam: the venue's main website is fully venue-managed; after "Book Now" the white-label B2C flow keeps the venue's header/footer branding while product selection, cart and checkout are TICVAI-managed. Header/footer links to non-checkout pages redirect to the main venue site. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-397)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Flow type key (`bookingFlows.flowTypeKey`) | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour … | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | The flow types the system catalogue offers (decided 29 September, W12; impact.md b). |
| Booking flows name (`bookingFlows.name`) | max length 80 | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Staff-facing, e.g. "Day pass, date first". |
| Is default for type (`bookingFlows.isDefaultForType`) | At most one per venue and type; setting it takes it from the previous default. | off | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | At most one per venue and type; setting it takes it from the previous default. |
| Booking flows is enabled (`bookingFlows.isEnabled`) | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | A disabled flow is kept and not published; products naming it fall back to the default. |
| Steps (`bookingFlows.steps`) | at most 30 | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Every step of the type, in the venue's order. Filled from the type when left out on create. |
| Steps: step key (`bookingFlows.steps[].stepKey`) | Location · Help me choose · Product · Date · Time · Performance · Level · Language · Duration · Route · Party size · Resource map … | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Every step a guest booking flow can hold (decided 29 September, W12). What each step does on WEB and MOB, and which screen draws it, is in the screen definitions of P01 and P02; which types carry which steps is … |
| Steps: enabled (`bookingFlows.steps[].enabled`) | A `required` step cannot be off; the flow saves and `isValid` turns false. | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | A `required` step cannot be off; the flow saves and `isValid` turns false. |
| Steps: sort order (`bookingFlows.steps[].sortOrder`) | min 0 | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Steps: settings (`bookingFlows.steps[].settings`) | A name the type does not give is refused with 400. | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. |
| Settings (`bookingFlows.settings`) | — | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | The settings that belong to one flow, not to the venue (decided 29 September, W12). |
| Settings: performance reveal (`bookingFlows.settings.performanceReveal`) | Date time ticket · All at once | Date time ticket | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Performance reveal (rev 3 REV3-2). `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. |
| Settings: sign in at (`bookingFlows.settings.signInAt`) | After add ons · At payment | After add ons | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3). |
| Settings: seat event date mode (`bookingFlows.settings.seatEventDateMode`) | Inline step · Popup on seat map; Read only by the seated flow types. | Inline step | GST-007, GST-008, GST-009, GST-041, GST-049, WEB-005, WEB-006, WEB-007 … (12) | Date and time on a seated event (rev 3 REV3-4). `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. |
| Settings: extras step (`bookingFlows.settings.extrasStep`) | Auto · Always · Never; `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. | Auto | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. |
| Settings: quick tour (`bookingFlows.settings.quickTour`) | — | off | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Quick tour (rev 3 REV3-20). A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. |
| Settings: consent questions (`bookingFlows.settings.consentQuestionIds`) | at most 10; no duplicates; Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | The flow's own consent questions (rev 3 REV3-26). Asked on every booking through this flow, together with those of each product in the cart, each question once. |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-103` · status **notStarted** · provenance generated
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (78), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (29 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-103?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: What publishing changes, Add a flow, Save flow, Validate, Assign to product, Assign to category, Publish site, Remove flow.
- [ ] Every transition is wired: `CMS-102`, `CMS-016`, `CMS-101`, `CMS-014`.
- [ ] Every gated control is gated: `GUEST_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE`, `TENANT_PUBLISH`.
- [ ] The 27 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-104` App Build & Store Publishing

**Get the tenant's own app into the App Store and Google Play under the client's own accounts — checklist, store listing, request a build, download or submit it, follow its review — with a guide for the steps only the client can take.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · ticket #27914 (APP-WL-CMS-104) |
| Who uses it | venue staff holding `AI_USE`, `TENANT_CONFIGURE`, `TENANT_PUBLISH` (1 operate, 2 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listAppBuilds` reads the builds and `getAppBuild` reads one — list, select, act; the checklist sits above the list |
| Offline | online only |
| Opens with | `appBuildId` (navigation), `conversationId` (navigation) · cold entry: Resolves the tenant from the session and opens on the checklist and the newest build. |
| Route | `/white-label/app-publishing` |

**What the spec says about it.** **Added 29 September for M24-08.** TICVAI never publishes a client's app under its own developer account: each client opens and owns its Apple Developer account (with a D-U-N-S number) and its Google Play account, builds its app here from the published configuration, and uploads it, or lets us submit it with its own API credential. The accounts are make-or-break client inputs (`setStoreAccounts`).

**From the White Label & CMS process.** Get the tenant's branded app into the App Store and Google Play under the client's own accounts: a checklist of what only the client can do (D-U-N-S, Apple and Google developer accounts), the store listing, a build from a published version, then download to upload or submit with the client's credential, and follow store review. A guide walks the client through each outside step.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- ADR-0006 says TICVAI builds, signs and submits and tenants do not self-publish, and that shared-tier tenants get a branded PWA. (CHG-SGU-025)

**Fixed on main** (the package already carries these; draw what it says): The listing has no place for the TICVAI credit the client asked to keep visible in published apps. (CHG-SGU-011).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Where does "Powered by TICVAI" appear in the published app (launch, Account, About)?** → "Powered by TICVAI" is a configuration toggle, default on: shown unless the venue's licence allows switching it off (Pre-apply round, 2 October; DI-297 amended). *(decided by Chinmay, 2026-10-02; DEC-160 / CHG-NOTE-009 / CHG-SGU-011)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Platform | select field | — | — | — | — | Sends `?platform=`, iOS or Android. | — |
| Show "Powered by TICVAI" | toggle | optional | on | — | — | **A configuration toggle, on by default** (decided by Chinmay, 2 October 2026; DEC-160; CHG-CSA-036). The credit shows on the launch screen under the splash and at the foot of Account (DI-250 … | `BrandIdentity.showPoweredBy` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Platform | segmented control | — | Ios · Android | `listAppBuilds` ?platform |

**Form: Save store accounts and listing** (modal, opened by *Save store accounts and listing*; *Save* calls `setStoreAccounts`, *Cancel* sends nothing)

**Collects what `setStoreAccounts` sends**: per store, `accountHolderName`, `developerAccountId`, `appIdentifier`, `dunsNumber` (Apple, nine digits), optional `apiCredentialSecretRef` and the `listing` (name, subtitle, description and keywords in every tenant language, category, support and privacy links, screenshots). Refused `400` for an Apple account without a D-U-N-S number. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Accounts `accounts` | repeatable rows | required | — | at most 2 | — | — | `setStoreAccounts` body |
| Store `accounts[].store` | segmented control | required | — | Apple app store · Google play | — | — | `setStoreAccounts` body |
| Account holder name `accounts[].accountHolderName` | text field | required | — | max length 200 | — | The client's legal entity as the store knows it. | `setStoreAccounts` body |
| Duns number `accounts[].dunsNumber` | text field | optional | — | pattern `^[0-9]{9}$` | — | Required for `appleAppStore`; Apple enrols an organisation only with its D-U-N-S number. | `setStoreAccounts` body |
| Developer account `accounts[].developerAccountId` | text field | required | — | max length 64 | — | Apple Team ID, or the Google Play developer account id. | `setStoreAccounts` body |
| App identifier `accounts[].appIdentifier` | text field | required | — | max length 155; pattern `^[A-Za-z][A-Za-z0-9_]*(\.[A-Za-z0-9_]+)+$` | — | The bundle id (Apple) or application id (Google) the app is signed with. | `setStoreAccounts` body |
| API credential secret ref `accounts[].apiCredentialSecretRef` | text field | optional | — | Needed only for `submitToStore`. | — | App Store Connect API key or Play service-account key, sent once and kept in the secret store; this is its reference. | `setStoreAccounts` body |
| Listing `accounts[].listing` | group | optional | — | — | — | The store listing. | `setStoreAccounts` body |
| App name `accounts[].listing.appName` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Keyed by ISO 639-1 code. Every enabled language should be present. | `setStoreAccounts` body |
| Subtitle `accounts[].listing.subtitle` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Keyed by ISO 639-1 code. Every enabled language should be present. | `setStoreAccounts` body |
| Description `accounts[].listing.description` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Keyed by ISO 639-1 code. Every enabled language should be present. | `setStoreAccounts` body |
| Keywords `accounts[].listing.keywords` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Keyed by ISO 639-1 code. Every enabled language should be present. | `setStoreAccounts` body |
| Category `accounts[].listing.category` | text field | optional | — | — | — | — | `setStoreAccounts` body |
| Support URL `accounts[].listing.supportUrl` | URL field | optional | — | — | https:// | — | `setStoreAccounts` body |
| Privacy policy URL `accounts[].listing.privacyPolicyUrl` | URL field | optional | — | — | https:// | — | `setStoreAccounts` body |
| Screenshot images `accounts[].listing.screenshotAssetRefs` | media picker (several) | optional | — | — | PNG, JPG, SVG or MP4 from the media library | — | `setStoreAccounts` body |

Errors to draw in the form: 400 An Apple account without a nine-digit D-U-N-S number, a store given twice, or a listing text missing a tenant language

**Form: Request a build** (confirmDialog, opened by *Request a build*; *Build* calls `requestAppBuild`, *Cancel* sends nothing)

**Names the platform, the version built and the account it is signed for.** Optional release notes and Submit to the store (needs a recorded credential). Refused `409` with the reason when the account is missing, nothing is published, or a build is already running.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Platform `platform` | segmented control | required | — | Ios · Android | — | — | `requestAppBuild` body |
| Config version `configVersion` | text field | optional | — | — | — | A published `ConfigVersion.version`. Absent builds the current one. | `requestAppBuild` body |
| Release notes `releaseNotes` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Keyed by ISO 639-1 code. Every enabled language should be present. | `requestAppBuild` body |
| Submit to store `submitToStore` | toggle | optional | off | — | — | Submit with the client's recorded API credential once built. False leaves the package for the client to upload. | `requestAppBuild` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 409 No store account for the platform, nothing published yet, or a build for the platform already running; the problem says which

**Rules for these inputs** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **accounts[] (per store)**: Legal name as the store knows it; Apple needs a nine-digit D-U-N-S number (400); Team ID or Play developer id; bundle / application id (e.g. ae.coastalaqua.app); API credential optional, write-only, shown as "Credential stored". *(source: contracts/satellite/white-label.yaml#/components/schemas/StoreAccount; DI-993)*
- **listing**: App name, subtitle, description and keywords in every tenant language (400 if one is missing), category, support and privacy URLs, screenshots. *(source: contracts/satellite/white-label.yaml#setStoreAccounts)*
- **requestAppBuild {platform, configVersion, releaseNotes, submitToStore}**: Platform iOS / Android; version defaults to the current published one; release notes per language; Submit to the store only with a stored credential. *(source: contracts/satellite/white-label.yaml#requestAppBuild)*

#### Outputs: what the screen shows and produces

**Shown**

**Before the first build** (detail panel, from `getStoreAccounts`): Apple D-U-N-S number, Apple Developer account, Google Play developer account (**the client's to open; we cannot open them for them**), store listing, app icons, a published configuration. Each open item says what to do next.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Accounts | list or chips (count when long) | — |

**Builds** (data table, from `listAppBuilds`)

| Shows | Format | Notes |
|---|---|---|
| Platform | chip: Ios, Android | — |
| Version name | text | The marketing version, e.g. 1.4.0. |
| Build number | 1,234 | — |
| Config version | text | The `ConfigVersion.version` built. |
| Status | chip: Queued, Building, Built, Failed, Submitted, In review… | `queued` to `built` or `failed` is the build service's; from `submitted` on it is read from the store with the client's credential, or … |
| Requested at | 1 Oct 2026, 14:30 | — |
| Finished at | 1 Oct 2026, 14:30 | — |

**Credit shown** (detail panel, from `getBrandIdentity`): Whether the "Powered by TICVAI" credit shows now, and whether the licence lets it be switched off.

| Shows | Format | Notes |
|---|---|---|
| Show powered by | yes / no (icon or chip) | "Powered by TICVAI", a configuration toggle, on by default (Chinmay, 2 October, workbook Q160 and the pre-apply round; consistent with … |

**The selected build** (detail panel, from `getAppBuild`): Download the signed package to upload it in App Store Connect or the Play Console; with a credential recorded, the store review status follows here (submitted, in review, approved, rejected, released).

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Queued, Building, Built, Failed, Submitted, In review… | `queued` to `built` or `failed` is the build service's; from `submitted` on it is read from the store with the client's credential, or … |
| Failure reason | text | — |
| Package image | the image or video | The signed .ipa or .aab in the `assets` library, for the client to download and upload. |
| Release notes | in the reader's language | Keyed by ISO 639-1 code. Every enabled language should be present. |
| Submit to store | yes / no (icon or chip) | — |

**App publishing guide** (assistant panel, from `sendAiMessage`): **The in-platform guide M24-08 asks for**: how to get a D-U-N-S number, open each account, fill the listing and answer store review. Grounded on a store-publishing knowledge source, no tenant data. `unavailable` until the ai "app publishing guide" assistant profile exists; the checklist guidance works without it.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Conversation | the name it points at, never the id | — |
| Role | chip: User, Assistant, System | — |
| Content | text | — |
| Sources | list or chips (count when long) | The sources an answer was grounded in, stored with the answer (8.3.70). One `jsonb` column on the row that carries it — … |
| Kind | chip: Document, Product, Entitlement, Report, Record | — |
| ID | text | — |
| Title | text | — |
| Collection | the name it points at, never the id | — |
| Excerpt | text | — |
| Relevance | 1,234.5 | — |
| Confidence | 1,234.5 | 8.1.5, 8.3.67. Nullable on purpose — a provider that does not report confidence must yield null rather than an invented number, and an … |
| Rationale | text | 8.3.68, 8.3.69. |
| Proposed action | grouped details | Present where the answer suggests a change. A draft, never applied here. |
| ID | the name it points at, never the id | — |
| Interaction | the name it points at, never the id | — |
| Translation job | the name it points at, never the id | The `proposeTranslations` job that drafted this proposal; `getTranslationProposals` reads a job's rows by it. |
| Kind | chip: Pricing, Promotion, Operational, Financial, Configuration, Content… | `content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from … |
| Target contract | text | Which contract would perform it. The assistant never performs it itself. |
| Target operation | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What a build and a submission do (publish gate) | navigation or local | — | — | — | — |
| Request a build (primary button) | `requestAppBuild` POST `/tenant-config/app-builds` | inline | AppBuild | 403 Authenticated but not permitted at the requested scope; 409 No store account for the platform, nothing published yet, or a build for the platform already running; the problem says which | gated `TENANT_PUBLISH`; opens confirmDialog first |
| Save store accounts and listing (secondary button) | `setStoreAccounts` PUT `/tenant-config/store-accounts` | inline | StorePublishingChecklist | 400 An Apple account without a nine-digit D-U-N-S number, a store given twice, or a listing text missing a tenant language | opens modal first |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Checklist**: Apple D-U-N-S, Apple Developer account, Google Play account (marked "Only you can do this"), store listing, app icons, a published configuration; each open item with its next step. *(source: contracts/satellite/white-label.yaml#/components/schemas/StorePublishingChecklist; DI-994)*
- **Builds**: Platform, version name and build number, configuration version, status (Queued, Building, Built, Failed, Submitted, In review, Approved, Rejected, Released), times; download link for the signed .ipa or .aab. *(source: contracts/satellite/white-label.yaml#/components/schemas/AppBuild)*
- **Powered by TICVAI**: A configuration toggle, default on: shown on the launch screen under the splash and at the foot of Account, unless the venue's licence allows switching it off. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-009))*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Request a build**: 202 queued; 409 says which of no store account, nothing published, or a build already running. Needs TENANT_PUBLISH. *(source: contracts/satellite/white-label.yaml#requestAppBuild)*
- **Ask the guide**: The in-platform publishing guide answers; unavailable until its assistant profile exists, the checklist guidance still works. *(source: DI-994; screens/P13-white-label-cms.yaml#CMS-104)*

**Data it reads**: `getStoreAccounts` (onLoad, The client's store accounts and the checklist); `listAppBuilds` (onLoad, The builds and their store status); `getBrandIdentity` (onLoad, Whether "Powered by TICVAI" shows …)

**Where the user goes next**

- → `CMS-102` Site Builder: *Back to the Site Builder*
- → `CMS-004` Logo & Assets: *App icons and splash*
- → `CMS-014` Publishing Workflow: *Publish the configuration first*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The checklist and the builds, read by `getStoreAccounts` and `listAppBuilds`. |
| Error (`?state=error`) | Could not load. Names which read failed. |
| Empty, first run (`?state=emptyFirstRun`) | **No build yet.** Shows the checklist first: nothing can be built until the client's store account for the platform is recorded and a version is published. |
| Empty, no results (`?state=emptyNoResults`) | No build for the platform picked. Names it and offers the other. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getStoreAccounts` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AI_USE` for `createAiConversation`, `sendAiMessage`; `TENANT_PUBLISH` for `requestAppBuild`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 An Apple account without a nine-digit D-U-N-S number, a store given twice, or a listing text missing a tenant language; 400 An asset is larger than 2 MB, or is not PNG or SVG (audit R270); 409 No store account for the platform, nothing published yet, or a build for the platform already running; the problem says which; 422 The guard (the provider''s content-safety service, CHG-R1S-002) blocked … |

#### Edge cases to draw

- **Store rejects the build**: Status Rejected with the store's reason (when a credential is stored) and a link to the guide. *(source: contracts/satellite/white-label.yaml#/components/schemas/AppBuild)*
- **No credential stored**: Status stays Built after download; the client uploads by hand and the screen says the review status will not update here. *(source: contracts/satellite/white-label.yaml#/components/schemas/AppBuild)*

#### Consistency with other screens

- Match `CMS-004`: The icons and splash built come from there.
- Match `CMS-001`: After a release, the minimum app version can force older apps to update.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
apple:
  accountHolderName: Coastal Leisure Group LLC
  dunsNumber: '565123987'
  developerAccountId: 9KX2B7Q4LM
  appIdentifier: ae.coastalaqua.app
google:
  developerAccountId: '7182736455091827364'
  appIdentifier: ae.coastalaqua.app
build:
  platform: ios
  versionName: 2.4.0
  buildNumber: 41
  configVersion: '14'
  status: inReview
```

#### Permissions

- `getStoreAccounts` → `TENANT_CONFIGURE` (configure) · staff
- `setStoreAccounts` → `TENANT_CONFIGURE` (configure) · staff
- `listAppBuilds` → `TENANT_CONFIGURE` (configure) · staff
- `getAppBuild` → `TENANT_CONFIGURE` (configure) · staff
- `requestAppBuild` → `TENANT_PUBLISH` (configure) · staff
- `createAiConversation` → `AI_USE` (operate) · staff, guest
- `sendAiMessage` → `AI_USE` (operate) · staff, guest
- `getBrandIdentity` → `TENANT_CONFIGURE` (configure) · staff
- `setBrandIdentity` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getStoreAccounts` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AI_USE` for `createAiConversation`, `sendAiMessage`; `TENANT_PUBLISH` for `requestAppBuild`.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.10.22 | Mobile App CMS | Marketing & CRM | CONTRACTED | `requestAppBuild` |
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
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Each client owns its Apple and Google developer accounts; the app is built in the CMS from a published configuration, with an in-platform guide (D-U-N-S number, opening accounts, store listing, store review). *(agreed · MoM 24 Sep 2026, M24-08 · DI-998)*
- Self-publishing must be guided in-platform (a guided page/instruction flow rather than only a static PDF manual); Qossai suggested an AI chat-based guide that walks the client step by step through DUNS registration and store submission. *(client request · MoM 24 Sep 2026, 4.13 Mobile App Deployment — Apple Developer Account Risk & Client Guidance Approach · DI-994)*
- Each client builds its app package from the CMS once configured and submits it to the App Store and Google Play under its own developer accounts (Apple DUNS); TICVAI never publishes client apps under its own account. *(agreed · MoM 24 Sep 2026, 4.12 / 4.13 Mobile App Deployment Strategy · DI-993)*
- **Open question.** Open: publishing model — each client's own App/Play Store listing vs one universal TICVAI app where the user selects the venue; and a client module with customisation screens plus a CI/CD-linked publish action vs a canvas the client exports and publishes. Softlabs to present pros/cons. *(open · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-251)*
- Qossai: the TICVAI name must always remain visible to end users of a client-branded guest app (e.g. a "Made by TICVAI" credit) and cannot be removed by the client. *(agreed · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-250)*
- The builder flow ends in a Review & Publish step before configuration goes live. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-194)*

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
| Powered by TICVAI credit (`brand.showPoweredBy`) | — | on | every guest screen (web, app and kiosk) | the *Powered by TICVAI* credit on the launch screen, at the foot of Account and in the web footer; on by default, and switching it off needs the licence add-on (403 powered-by-locked) |
| Accounts (`storeAccounts.accounts`) | at most 2 | — | no guest screen: the phone's home screen and the store listing | — |
| Accounts: store (`storeAccounts.accounts[].store`) | Apple app store · Google play | — | no guest screen: the phone's home screen and the store listing | — |
| Accounts: account holder name (`storeAccounts.accounts[].accountHolderName`) | max length 200 | — | no guest screen: the phone's home screen and the store listing | The client's legal entity as the store knows it. |
| Accounts: duns number (`storeAccounts.accounts[].dunsNumber`) | pattern `^[0-9]{9}$` | — | no guest screen: the phone's home screen and the store listing | Required for `appleAppStore`; Apple enrols an organisation only with its D-U-N-S number. |
| Accounts: developer account (`storeAccounts.accounts[].developerAccountId`) | max length 64 | — | no guest screen: the phone's home screen and the store listing | Apple Team ID, or the Google Play developer account id. |
| Accounts: app identifier (`storeAccounts.accounts[].appIdentifier`) | max length 155; pattern `^[A-Za-z][A-Za-z0-9_]*(\.[A-Za-z0-9_]+)+$` | — | no guest screen: the phone's home screen and the store listing | The bundle id (Apple) or application id (Google) the app is signed with. |
| Accounts: aPI credential secret ref (`storeAccounts.accounts[].apiCredentialSecretRef`) | Needed only for `submitToStore`. | — | no guest screen: the phone's home screen and the store listing | App Store Connect API key or Play service-account key, sent once and kept in the secret store; this is its reference. |
| Accounts: listing (`storeAccounts.accounts[].listing`) | — | — | no guest screen: the phone's home screen and the store listing | The store listing. |
| Listing: app name (`storeAccounts.accounts[].listing.appName`) | English and Arabic (Arabic right to left) | — | no guest screen: the phone's home screen and the store listing | Keyed by ISO 639-1 code. Every enabled language should be present. |
| Listing: subtitle (`storeAccounts.accounts[].listing.subtitle`) | English and Arabic (Arabic right to left) | — | no guest screen: the phone's home screen and the store listing | Keyed by ISO 639-1 code. Every enabled language should be present. |
| Listing: description (`storeAccounts.accounts[].listing.description`) | English and Arabic (Arabic right to left) | — | no guest screen: the phone's home screen and the store listing | Keyed by ISO 639-1 code. Every enabled language should be present. |
| Listing: keywords (`storeAccounts.accounts[].listing.keywords`) | English and Arabic (Arabic right to left) | — | no guest screen: the phone's home screen and the store listing | Keyed by ISO 639-1 code. Every enabled language should be present. |
| Listing: category (`storeAccounts.accounts[].listing.category`) | — | — | no guest screen: the phone's home screen and the store listing | — |
| Listing: support URL (`storeAccounts.accounts[].listing.supportUrl`) | https:// | — | no guest screen: the phone's home screen and the store listing | — |
| Listing: privacy policy URL (`storeAccounts.accounts[].listing.privacyPolicyUrl`) | https:// | — | no guest screen: the phone's home screen and the store listing | — |
| Listing: screenshot images (`storeAccounts.accounts[].listing.screenshotAssetRefs`) | PNG, JPG, SVG or MP4 from the media library | — | no guest screen: the phone's home screen and the store listing | — |
| Platform (`appBuilds.platform`) | Ios · Android | — | no guest screen: the phone's home screen and the store listing | — |
| Config version (`appBuilds.configVersion`) | — | — | no guest screen: the phone's home screen and the store listing | A published `ConfigVersion.version`. Absent builds the current one. |
| Release notes (`appBuilds.releaseNotes`) | English and Arabic (Arabic right to left) | — | no guest screen: the phone's home screen and the store listing | Keyed by ISO 639-1 code. Every enabled language should be present. |
| Submit to store (`appBuilds.submitToStore`) | — | off | no guest screen: the phone's home screen and the store listing | Submit with the client's recorded API credential once built. False leaves the package for the client to upload. |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-104` · status **notStarted** · provenance generated
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (22), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (35 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-104?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: What a build and a submission do, Request a build, Save store accounts and listing.
- [ ] Every transition is wired: `CMS-102`, `CMS-004`, `CMS-014`.
- [ ] Every gated control is gated: `AI_USE`, `TENANT_CONFIGURE`, `TENANT_PUBLISH`.
- [ ] The 6 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
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

**40 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createAiConversation": {"method":"POST","path":"/conversations","contract":"ai","summary":"Open a conversation","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiConversation"},
"createBookingFlowDefinition": {"method":"POST","path":"/venues/{venueId}/booking-flows","contract":"white-label","summary":"Pick a booking flow for a venue","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BookingFlow","responds":"BookingFlow"},
"deleteBookingFlow": {"method":"DELETE","path":"/booking-flows/{bookingFlowId}","contract":"white-label","summary":"Remove a booking flow from a venue","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getAppBuild": {"method":"GET","path":"/tenant-config/app-builds/{appBuildId}","contract":"white-label","summary":"One app build, with its package and store status","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"AppBuild"},
"getBookingFlow": {"method":"GET","path":"/booking-flows/{bookingFlowId}","contract":"white-label","summary":"Read one of a venue's booking flows, every step included","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BookingFlow"},
"getBrandIdentity": {"method":"GET","path":"/tenant-config/brand","contract":"white-label","summary":"Read brand identity","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"BrandIdentity"},
"getPublishedBookingFlow": {"method":"GET","path":"/venues/{venueId}/booking-flow","contract":"white-label","summary":"The published booking flow a product or category books through","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":false},{"name":"productCategoryId","in":"query","required":false},{"name":"flowTypeKey","in":"query","required":false}],"requestBody":null,"responds":"BookingFlow"},
"getSiteSetupProgress": {"method":"GET","path":"/tenant-config/site-setup","contract":"white-label","summary":"Where the tenant is in the Site Builder","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SiteSetupProgress"},
"getStoreAccounts": {"method":"GET","path":"/tenant-config/store-accounts","contract":"white-label","summary":"The client's store accounts and the publishing checklist","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"StorePublishingChecklist"},
"getTenantAppStatus": {"method":"GET","path":"/tenant-config/status","contract":"white-label","summary":"App status and recent changes","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"TenantAppStatus"},
"listAppBuilds": {"method":"GET","path":"/tenant-config/app-builds","contract":"white-label","summary":"The tenant's app builds, newest first","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"platform","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listBookingFlowTypes": {"method":"GET","path":"/booking-flow-types","contract":"white-label","summary":"The booking flow types a venue can pick from, with their steps","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"productKind","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listBookingFlows": {"method":"GET","path":"/venues/{venueId}/booking-flows","contract":"white-label","summary":"A venue's booking flows, in the working draft","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"flowTypeKey","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listConsentQuestions": {"method":"GET","path":"/consent-questions","contract":"marketing-crm","summary":"The consent questions a venue asks at booking","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductCategories": {"method":"GET","path":"/product-categories","contract":"catalogue","summary":"The merchandise hierarchy — categories, brands, collections","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProductCategoryNode"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"publishTenantConfig": {"method":"POST","path":"/tenant-config/publish","contract":"white-label","summary":"Publish the working draft","permission":"TENANT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConfigVersion"},
"requestAppBuild": {"method":"POST","path":"/tenant-config/app-builds","contract":"white-label","summary":"Build the branded app for a store","permission":"TENANT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"sendAiMessage": {"method":"POST","path":"/conversations/{conversationId}/messages","contract":"ai","summary":"Ask","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiMessage"},
"setBrandIdentity": {"method":"PUT","path":"/tenant-config/brand","contract":"white-label","summary":"Set logo, favicon and splash","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BrandIdentity","responds":"BrandIdentity"},
"setProductCategories": {"method":"PUT","path":"/product-categories","contract":"catalogue","summary":"Define the hierarchy, in the order a guest sees it","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProductCategory"},
"setSiteSetupProgress": {"method":"PUT","path":"/tenant-config/site-setup","contract":"white-label","summary":"Save the Site Builder's progress","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SiteSetupProgress","responds":"SiteSetupProgress"},
"setStoreAccounts": {"method":"PUT","path":"/tenant-config/store-accounts","contract":"white-label","summary":"Record the client's own Apple and Google store accounts and listings","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"StorePublishingChecklist"},
"updateBookingFlowDefinition": {"method":"PATCH","path":"/booking-flows/{bookingFlowId}","contract":"white-label","summary":"Reorder a flow's steps, switch optional steps, change its settings","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"BookingFlow"},
"updateProduct": {"method":"PATCH","path":"/products/{productId}","contract":"catalogue","summary":"Update a product","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"UpdateProductRequest","responds":"Product"},
"validateBookingFlow": {"method":"POST","path":"/booking-flows/{bookingFlowId}/validate","contract":"white-label","summary":"Check a flow against its type","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"BookingFlowValidation"},
"validateTenantConfig": {"method":"POST","path":"/tenant-config/validate","contract":"white-label","summary":"Validate the working draft","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConfigValidationReport"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiConversation": {"type":"object","x-ticvai-persistence":"ai.conversation","required":["id","principalId","module","startedAt"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"module":{"$ref":"#/components/schemas/common::ModuleKey"},"locale":{"type":"string"},"messageCount":{"type":"integer"},"startedAt":{"type":"string","format":"date-time"},"lastMessageAt":{"type":"string","format":"date-time"}}},
"AiMessage": {"type":"object","x-ticvai-persistence":"ai.message","required":["id","conversationId","role","content","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"conversationId":{"type":"string","format":"uuid"},"role":{"type":"string","enum":["user","assistant","system"]},"content":{"type":"string"},"sources":{"$ref":"#/components/schemas/AiSourceList"},"confidence":{"type":"number","nullable":true,"description":"8.1.5, 8.3.67. **Nullable on purpose** — a provider that does not report confidence must yield null rather than an invented number, and an interface showing 0.9 because the code defaulted it is worse than showing nothing.\n"},"rationale":{"type":"string","nullable":true,"description":"8.3.68, 8.3.69."},"proposedAction":{"allOf":[{"$ref":"#/components/schemas/ProposedAction"}],"nullable":true,"description":"Present where the answer suggests a change. **A draft, never applied here.**"},"traceId":{"type":"string"},"provider":{"$ref":"#/components/schemas/AiProviderKind"},"model":{"type":"string"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"latencyMs":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"}}},
"AiProviderKind": {"type":"string","enum":["openai","gemini","anthropic","azureOpenai","localLlm","openaiCompatible"],"description":"`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n**Core42 Compass is reached through `openaiCompatible`** (Chinmay, 2 October: the AI residency decision, amending AI-D02; CHG-CSA-002). Compass is the provider of the `uaeOnly` residency class (common `AiResidencyClass`): Small tier Compass GPT-4.1 mini (or Seraj), Strong tier Compass GPT-5, with OpenAI UAE as the fallback. OpenAI UAE is `openai` with a UAE `endpoint`: OpenAI's UAE-region API project, `ae.api.openai.com` (in-country processing, on OpenAI sales approval), allowed under `uaeOnly` and the only endpoint a `uaeOnly` BYOK OpenAI key may use (CHG-R1S-016). **We host no model** (Chinmay, 3 October, CHG-R1S-002): there is no in-cell open-weights fallback; `localLlm` is used only where a client asks for self-hosting and runs the model on the client's estate (`onPrem`).\n**A kind is a protocol, not a vendor** (Chinmay, 2 October, contract follow-ups: BYOK accepts any provider; CHG-FUP-008). Any vendor is accepted, named in `AiProvider.vendor`: Mistral, Cohere or any other is reached through `openaiCompatible` where its API speaks it, which the compatibility test confirms before activation (`AiProviderCompatibility`). A new native adapter is a new value here, a breaking change for a client built earlier that goes out with an approval (`docs/active/breaking-changes.yaml`); until then a vendor without either protocol is refused `422 provider-protocol-unsupported`.\n"},
"AiSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**The sources an answer was grounded in, stored with the answer** (8.3.70). One `jsonb` column on the row that carries it — `ai.message.sources` and `ai.activity.sources` — because the grounding audit reads the list as it was when the answer was given, and a source is never queried on its own.\n","items":{"$ref":"#/components/schemas/AiSource"}},
"AppAvailability": {"type":"string","description":"**The sold-out or closed signal (decided 28 September, audit R073).** `open` is the normal state. `soldOut` shows WEB-029's sold-out state across the app while browsing still works; `closed` shows the closed state (a weather closure, a private event). Neither refuses a request on its own: it is what the guest is told, and a sale is still refused by availability where it applies. Set with `setMaintenanceMode`.\n","enum":["open","soldOut","closed"],"default":"open"},
"AppBuild": {"x-ticvai-persistence":"whitelabel.app_build","type":"object","description":"**One build of the tenant's branded app (decided 24 September, M24-08).** Made from a published `ConfigVersion`, signed for the client's own store account.\n","required":["id","platform","configVersion","status","requestedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"platform":{"type":"string","enum":["ios","android"]},"configVersion":{"type":"string","description":"The `ConfigVersion.version` built."},"storeAccountId":{"type":"string","format":"uuid","readOnly":true},"versionName":{"type":"string","readOnly":true,"description":"The marketing version, e.g. 1.4.0."},"buildNumber":{"type":"integer","readOnly":true},"status":{"type":"string","readOnly":true,"enum":["queued","building","built","failed","submitted","inReview","approved","rejected","released"],"description":"`queued` to `built` or `failed` is the build service's; from `submitted` on it is read from the store with the client's credential, or stays `built` when the client uploads by hand."},"failureReason":{"type":"string","nullable":true,"readOnly":true},"packageAssetRef":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The signed .ipa or .aab in the `assets` library, for the client to download and upload."},"releaseNotes":{"$ref":"#/components/schemas/white-label::LocalisedText"},"submitToStore":{"type":"boolean","default":false},"requestedAt":{"type":"string","format":"date-time","readOnly":true},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"finishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `tenant` scope."}}},
"BookingFlow": {"x-ticvai-persistence":"whitelabel.booking_flow","type":"object","description":"**A venue's booking flow (decided 29 September, W12: operators pick their flows, see which steps are required, set their own order).** Made from a `BookingFlowType`; lives in the working draft and reaches guests with `publishTenantConfig`, which copies the venue's flows into the version's snapshot. A product or category names its flow (catalogue `bookingFlowId`); otherwise the venue's default for the type serving its kind applies.\n","required":["flowTypeKey","name"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `createBookingFlowDefinition`."},"flowTypeKey":{"$ref":"#/components/schemas/BookingFlowTypeKey"},"name":{"type":"string","maxLength":80,"description":"Staff-facing, e.g. \"Day pass, date first\". Not shown to guests."},"isDefaultForType":{"type":"boolean","default":false,"description":"At most one per venue and type; setting it takes it from the previous default."},"isEnabled":{"type":"boolean","default":true,"description":"A disabled flow is kept and not published; products naming it fall back to the default."},"steps":{"type":"array","maxItems":30,"description":"Every step of the type, in the venue's order. Filled from the type when left out on create.","items":{"$ref":"#/components/schemas/BookingFlowStep"}},"settings":{"$ref":"#/components/schemas/BookingFlowLevelSettings"},"isValid":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Whether the flow passes `validateBookingFlow`; worked out in the same transaction as each write. `publishTenantConfig` refuses a draft holding an invalid enabled flow."},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `venue` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"BookingFlowLevelSettings": {"x-ticvai-persistence":"none — jsonb column on whitelabel.booking_flow","type":"object","description":"**The settings that belong to one flow, not to the venue (decided 29 September, W12).** Moved here from `BookingFlowSettings`, which keeps the venue-wide ones. Each keeps its rev 3 meaning and default. A field left out takes its default.\n","properties":{"performanceReveal":{"type":"string","enum":["dateTimeTicket","allAtOnce"],"default":"dateTimeTicket","description":"**Performance reveal (rev 3 REV3-2).** `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. Product-first (W8) is the step order of `experienceWorkshop`, not a value here.\n"},"signInAt":{"type":"string","enum":["afterAddOns","atPayment"],"default":"afterAddOns","description":"**Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3).** `afterAddOns` asks as the guest leaves the extras step; `atPayment` asks at payment. The basket is kept either way.\n"},"seatEventDateMode":{"type":"string","enum":["inlineStep","popupOnSeatMap"],"default":"inlineStep","description":"**Date and time on a seated event (rev 3 REV3-4).** `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. Read only by the seated flow types.\n"},"extrasStep":{"type":"string","enum":["auto","always","never"],"default":"auto","description":"`auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off."},"quickTour":{"type":"boolean","default":false,"description":"**Quick tour (rev 3 REV3-20).** A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. Seen-state kept on the device only.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"default":[],"description":"**The flow's own consent questions (rev 3 REV3-26).** Asked on every booking through this flow, together with those of each product in the cart, each question once. Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. A Help me choose answer may pre-fill one (`GuidedChoice` `consentPrefill`); the guest still confirms it.\n","items":{"type":"string","format":"uuid"}}}},
"BookingFlowStep": {"x-ticvai-persistence":"whitelabel.booking_flow_step","type":"object","description":"One step of a venue's flow, in the venue's order (decided 29 September, W12).","required":["stepKey","enabled","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"bookingFlowId":{"type":"string","format":"uuid","readOnly":true},"stepKey":{"$ref":"#/components/schemas/BookingFlowStepKey"},"enabled":{"type":"boolean","description":"A `required` step cannot be off; the flow saves and `isValid` turns false."},"sortOrder":{"type":"integer","minimum":0},"requirement":{"type":"string","enum":["required","optional","conditional"],"readOnly":true,"x-ticvai-derived":"onRead","description":"From the flow type, so the CMS can mark the step without a second read."},"settings":{"type":"object","additionalProperties":true,"default":{},"description":"The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. `languages` on `language`, `minHours` on `duration`). A name the type does not give is refused with 400."}}},
"BookingFlowStepKey": {"type":"string","description":"Every step a guest booking flow can hold (decided 29 September, W12). What each step does on WEB and MOB, and which screen draws it, is in the screen definitions of P01 and P02; which types carry which steps is `x-ticvai-system-catalogue` on `BookingFlowType`. `payment` is always last. Sign-in is not a step: it is asked where the flow's `signInAt` says.\n","enum":["location","helpMeChoose","product","date","time","performance","level","language","duration","route","partySize","resourceMap","resourceSize","seatMap","tickets","attendees","membershipPlan","giftCardValue","recipient","consent","extras","review","payment"]},
"BookingFlowType": {"x-ticvai-persistence":"none — system catalogue, shipped with the service and the same for every tenant","type":"object","description":"**A flow type from the system catalogue (decided 29 September, W12).** Read-only: a venue picks one (`createBookingFlowDefinition`) and orders its steps within `orderConstraints`. `requirement` is `required` (cannot be turned off), `optional` (the venue chooses) or `conditional` (shown to a guest only when `condition` holds; the venue may still turn it off where it is not also required by law or by a product, as the condition says). `settingsOwned` names the settings, venue-wide (`BookingFlowSettings`) or flow-level (`BookingFlowLevelSettings`), that the CMS shows beside the step; `stepSettings` are the step's own settings, kept in `BookingFlowStep.settings`.\n","x-ticvai-system-catalogue":{"commonConstraints":[{"kind":"last","stepKey":"payment"},{"kind":"first","stepKey":"location"},{"kind":"before","stepKey":"helpMeChoose","otherStepKey":"tickets"},{"kind":"before","stepKey":"helpMeChoose","otherStepKey":"product"},{"kind":"before","stepKey":"tickets","otherStepKey":"extras"},{"kind":"before","stepKey":"tickets","otherStepKey":"consent"},{"kind":"before","stepKey":"review","otherStepKey":"payment"}],"commonConditions":{"location":"the tenant has more than one active venue and `locationSwitcher` is on","helpMeChoose":"the venue has a published `GuidedChoice`","consent":"the flow's `consentQuestionIds` or a product in the cart asks a consent question (REV3-26); cannot be turned off while either does","attendees":"a product in the cart asks attendee details"},"types":[{"key":"datedDayPass","productKinds":["admission","datedAdmission"],"steps":[{"stepKey":"location","requirement":"conditional"},{"stepKey":"helpMeChoose","requirement":"conditional"},{"stepKey":"date","requirement":"required","settingsOwned":["dateStripDays","performanceReveal"]},{"stepKey":"tickets","requirement":"required","settingsOwned":["ticketCategories","ticketTags","cardInfo","cardLayout","cardSize","showInfoOnly"]},{"stepKey":"consent","requirement":"conditional","settingsOwned":["consentQuestionIds"]},{"stepKey":"extras","requirement":"optional","settingsOwned":["extrasStep","quantitiesOnAddOns"]},{"stepKey":"review","requirement":"optional"},{"stepKey":"payment","requirement":"required","settingsOwned":["signInAt"]}]},{"key":"timedEntry","productKinds":["timedAdmission"],"steps":[{"stepKey":"location","requirement":"conditional"},{"stepKey":"helpMeChoose","requirement":"conditional"},{"stepKey":"date","requirement":"required","settingsOwned":["dateStripDays","performanceReveal"]},{"stepKey":"time","requirement":"required","settingsOwned":["timesPerPage","dayPartFilter","dayPartBoundaries","performanceReveal"]},{"stepKey":"tickets","requirement":"required","settingsOwned":["ticketCategories","ticketTags","cardInfo","cardLayout","cardSize","showInfoOnly"]},{"stepKey":"consent","requirement":"conditional","settingsOwned":["consentQuestionIds"]},{"stepKey":"extras","requirement":"optional","settingsOwned":["extrasStep","quantitiesOnAddOns"]},{"stepKey":"review","requirement":"optional"},{"stepKey":"payment","requirement":"required","settingsOwned":["signInAt"]}],"orderConstraints":[{"kind":"before","stepKey":"date","otherStepKey":"time"}]},{"key":"openDated","productKinds":["openDated","admission"],"steps":[{"stepKey":"location","requirement":"conditional"},{"stepKey":"helpMeChoose","requirement":"conditional"},{"stepKey":"tickets","requirement":"required","settingsOwned":["ticketCategories","ticketTags","cardInfo","cardLayout","cardSize","showInfoOnly"]},{"stepKey":"consent","requirement":"conditional","settingsOwned":["consentQuestionIds"]},{"stepKey":"extras","requirement":"optional","settingsOwned":["extrasStep","quantitiesOnAddOns"]},{"stepKey":"review","requirement":"optional"},{"stepKey":"payment","requirement":"required","settingsOwned":["signInAt"]}]},{"key":"seatedFixedPerformance","productKinds":["seated"],"steps":[{"stepKey":"location","requirement":"conditional"},{"stepKey":"performance","requirement":"required","condition":"skipped for the guest when the event has one on-sale performance"},{"stepKey":"seatMap","requirement":"required","settingsOwned":["seatPicker","seatViewPosition","seatTimeBar","mapView"]},{"stepKey":"tickets","requirement":"conditional","condition":"the seat's price category has more than one ticket type (adult or child)"},{"stepKey":"consent","requirement":"conditional","settingsOwned":["consentQuestionIds"]},{"stepKey":"extras","requirement":"optional","settingsOwned":["extrasStep","quantitiesOnAddOns"]},{"stepKey":"review","requirement":"optional"},{"stepKey":"payment","requirement":"required","settingsOwned":["signInAt"]}],"orderConstraints":[{"kind":"before","stepKey":"performance","otherStepKey":"seatMap"}]},{"key":"seatedDateTimeSeatMap","productKinds":["seated"],"steps":[{"stepKey":"location","requirement":"conditional"},{"stepKey":"date","requirement":"required","settingsOwned":["dateStripDays","seatEventDateMode"]},{"stepKey":"time","requirement":"required","settingsOwned":["timesPerPage","dayPartFilter","dayPartBoundaries","seatEventDateMode"]},{"stepKey":"seatMap","requirement":"required","settingsOwned":["seatPicker","seatViewPosition","seatTimeBar","mapView","seatEventDateMode"]},{"stepKey":"tickets","requirement":"conditional","condition":"the seat's price category has more than one ticket type"},{"stepKey":"consent","requirement":"conditional","settingsOwned":["consentQuestionIds"]},{"stepKey":"extras","requirement":"optional","settingsOwned":["extrasStep","quantitiesOnAddOns"]},{"stepKey":"review","requirement":"optional"},{"stepKey":"payment","requirement":"required","settingsOwned":["signInAt"]}],"orderConstraints":[{"kind":"before","stepKey":"date","otherStepKey":"time"},{"kind":"before","stepKey":"time","otherStepKey":"seatMap"}]},{"key":"experienceWorkshop","productKinds":["timedAdmission","admission"],"steps":[{"stepKey":"location","requirement":"conditional"},{"stepKey":"helpMeChoose","requirement":"conditional"},{"stepKey":"product","requirement":"required","settingsOwned":["cardLayout","cardSize","cardInfo","showInfoOnly"]},{"stepKey":"date","requirement":"required","settingsOwned":["dateStripDays","performanceReveal"]},{"stepKey":"time","requirement":"required","settingsOwned":["timesPerPage","dayPartFilter","dayPartBoundaries"]},{"stepKey":"tickets","requirement":"required","settingsOwned":["ticketCategories","ticketTags"]},{"stepKey":"attendees","requirement":"conditional"},{"stepKey":"consent","requirement":"conditional","settingsOwned":["consentQuestionIds"]},{"stepKey":"extras","requirement":"optional","settingsOwned":["extrasStep","quantitiesOnAddOns"]},{"stepKey":"review","requirement":"optional"},{"stepKey":"payment","requirement":"required","settingsOwned":["signInAt"]}],"orderConstraints":[{"kind":"before","stepKey":"product","otherStepKey":"date"},{"kind":"before","stepKey":"date","otherStepKey":"time"}]},{"key":"surfSession","productKinds":["timedAdmission","rental"],"steps":[{"stepKey":"location","requirement":"conditional"},{"stepKey":"date","requirement":"required","settingsOwned":["dateStripDays"]},{"stepKey":"time","requirement":"required","settingsOwned":["timesPerPage","dayPartFilter","dayPartBoundaries"]},{"stepKey":"level","requirement":"required","stepSettings":[{"name":"levels","type":"string[]","note":"level tags offered","from the products' segmentTags":null}]},{"stepKey":"tickets","requirement":"required","settingsOwned":["ticketTags","cardInfo"]},{"stepKey":"consent","requirement":"conditional","settingsOwned":["consentQuestionIds"]},{"stepKey":"extras","requirement":"optional","settingsOwned":["extrasStep","quantitiesOnAddOns"]},{"stepKey":"review","requirement":"optional"},{"stepKey":"payment","requirement":"required","settingsOwned":["signInAt"]}],"orderConstraints":[{"kind":"before","stepKey":"date","otherStepKey":"time"},{"kind":"before","stepKey":"time","otherStepKey":"level"}]},{"key":"meetingRoomHourly","productKinds":["rental"],"steps":[{"stepKey":"location","requirement":"conditional"},{"stepKey":"date","requirement":"required","settingsOwned":["dateStripDays"]},{"stepKey":"time","requirement":"required","settingsOwned":["timesPerPage","dayPartFilter","dayPartBoundaries"]},{"stepKey":"duration","requirement":"required","stepSettings":[{"name":"minHours","type":"integer","default":1},{"name":"maxHours","type":"integer","default":8},{"name":"stepMinutes","type":"integer","default":60}]},{"stepKey":"partySize","requirement":"optional","stepSettings":[{"name":"minGuests","type":"integer","default":1},{"name":"maxGuests","type":"integer"}]},{"stepKey":"extras","requirement":"optional","settingsOwned":["extrasStep","quantitiesOnAddOns"]},{"stepKey":"review","requirement":"optional"},{"stepKey":"payment","requirement":"required","settingsOwned":["signInAt"]}],"orderConstraints":[{"kind":"before","stepKey":"date","otherStepKey":"time"},{"kind":"before","stepKey":"time","otherStepKey":"duration"}]},{"key":"cabanaMap","productKinds":["rental"],"steps":[{"stepKey":"location","requirement":"conditional"},{"stepKey":"date","requirement":"required","settingsOwned":["dateStripDays"]},{"stepKey":"resourceMap","requirement":"required","condition":"the venue's resource selection policy lets the guest choose (resources setResourceSelectionPolicy guestMayChoose; REV3-15)","settingsOwned":["mapView"]},{"stepKey":"consent","requirement":"conditional","settingsOwned":["consentQuestionIds"]},{"stepKey":"extras","requirement":"optional","settingsOwned":["extrasStep","quantitiesOnAddOns"]},{"stepKey":"review","requirement":"optional"},{"stepKey":"payment","requirement":"required","settingsOwned":["signInAt"]}],"orderConstraints":[{"kind":"before","stepKey":"date","otherStepKey":"resourceMap"}]},{"key":"cabanaBySize","productKinds":["rental"],"steps":[{"stepKey":"location","requirement":"conditional"},{"stepKey":"date","requirement":"required","settingsOwned":["dateStripDays"]},{"stepKey":"partySize","requirement":"required","stepSettings":[{"name":"minGuests","type":"integer","default":1},{"name":"maxGuests","type":"integer"}]},{"stepKey":"resourceSize","requirement":"required","note":"the server assigns a unit of the chosen size"},{"stepKey":"consent","requirement":"conditional","settingsOwned":["consentQuestionIds"]},{"stepKey":"extras","requirement":"optional","settingsOwned":["extrasStep","quantitiesOnAddOns"]},{"stepKey":"review","requirement":"optional"},{"stepKey":"payment","requirement":"required","settingsOwned":["signInAt"]}],"orderConstraints":[{"kind":"before","stepKey":"date","otherStepKey":"resourceSize"},{"kind":"before","stepKey":"partySize","otherStepKey":"resourceSize"}]},{"key":"guidedTourByLanguage","productKinds":["timedAdmission"],"steps":[{"stepKey":"location","requirement":"conditional"},{"stepKey":"date","requirement":"required","settingsOwned":["dateStripDays"]},{"stepKey":"language","requirement":"required","stepSettings":[{"name":"languages","type":"string[]","note":"ISO 639-1 codes the tours run in"}]},{"stepKey":"time","requirement":"required","settingsOwned":["timesPerPage","dayPartFilter","dayPartBoundaries"]},{"stepKey":"tickets","requirement":"required","settingsOwned":["ticketCategories","ticketTags"]},{"stepKey":"extras","requirement":"optional","settingsOwned":["extrasStep","quantitiesOnAddOns"]},{"stepKey":"review","requirement":"optional"},{"stepKey":"payment","requirement":"required","settingsOwned":["signInAt"]}],"orderConstraints":[{"kind":"before","stepKey":"date","otherStepKey":"time"},{"kind":"before","stepKey":"language","otherStepKey":"time"}]},{"key":"transport","productKinds":["admission","timedAdmission"],"steps":[{"stepKey":"route","requirement":"required"},{"stepKey":"date","requirement":"required","settingsOwned":["dateStripDays"]},{"stepKey":"time","requirement":"required","settingsOwned":["timesPerPage","dayPartFilter"]},{"stepKey":"tickets","requirement":"required","settingsOwned":["ticketCategories"]},{"stepKey":"extras","requirement":"optional","settingsOwned":["extrasStep"]},{"stepKey":"review","requirement":"optional"},{"stepKey":"payment","requirement":"required","settingsOwned":["signInAt"]}],"orderConstraints":[{"kind":"before","stepKey":"route","otherStepKey":"time"},{"kind":"before","stepKey":"date","otherStepKey":"time"}]},{"key":"tableReservation","productKinds":["fnb"],"steps":[{"stepKey":"location","requirement":"conditional"},{"stepKey":"date","requirement":"required","settingsOwned":["dateStripDays"]},{"stepKey":"partySize","requirement":"required","stepSettings":[{"name":"minGuests","type":"integer","default":1},{"name":"maxGuests","type":"integer","default":12}]},{"stepKey":"time","requirement":"required","settingsOwned":["timesPerPage","dayPartFilter","dayPartBoundaries"]},{"stepKey":"extras","requirement":"optional","note":"pre-order","settingsOwned":["extrasStep"]},{"stepKey":"review","requirement":"optional"},{"stepKey":"payment","requirement":"conditional","condition":"the venue takes a deposit or pre-order for the table","settingsOwned":["signInAt"]}],"orderConstraints":[{"kind":"before","stepKey":"date","otherStepKey":"time"},{"kind":"before","stepKey":"partySize","otherStepKey":"time"}]},{"key":"membership","productKinds":["membership"],"steps":[{"stepKey":"membershipPlan","requirement":"required"},{"stepKey":"attendees","requirement":"required","note":"each member's details"},{"stepKey":"consent","requirement":"conditional","settingsOwned":["consentQuestionIds"]},{"stepKey":"review","requirement":"optional"},{"stepKey":"payment","requirement":"required","settingsOwned":["signInAt"]}],"orderConstraints":[{"kind":"before","stepKey":"membershipPlan","otherStepKey":"attendees"}]},{"key":"giftCard","productKinds":["giftCard"],"steps":[{"stepKey":"giftCardValue","requirement":"required"},{"stepKey":"recipient","requirement":"required"},{"stepKey":"review","requirement":"optional"},{"stepKey":"payment","requirement":"required","settingsOwned":["signInAt"]}]},{"key":"multiLocation","productKinds":["admission","timedAdmission","datedAdmission"],"steps":[{"stepKey":"location","requirement":"required","settingsOwned":["locationSwitcher"]},{"stepKey":"helpMeChoose","requirement":"conditional"},{"stepKey":"product","requirement":"required","settingsOwned":["cardLayout","cardSize","cardInfo"]},{"stepKey":"date","requirement":"conditional","condition":"the product is dated or timed","settingsOwned":["dateStripDays","performanceReveal"]},{"stepKey":"time","requirement":"conditional","condition":"the product is timed","settingsOwned":["timesPerPage","dayPartFilter","dayPartBoundaries"]},{"stepKey":"tickets","requirement":"required","settingsOwned":["ticketCategories","ticketTags"]},{"stepKey":"consent","requirement":"conditional","settingsOwned":["consentQuestionIds"]},{"stepKey":"extras","requirement":"optional","settingsOwned":["extrasStep","quantitiesOnAddOns"]},{"stepKey":"review","requirement":"optional"},{"stepKey":"payment","requirement":"required","settingsOwned":["signInAt"]}],"orderConstraints":[{"kind":"before","stepKey":"location","otherStepKey":"product"},{"kind":"before","stepKey":"date","otherStepKey":"time"}]}]},"required":["key","name","productKinds","steps","orderConstraints"],"properties":{"key":{"$ref":"#/components/schemas/BookingFlowTypeKey"},"name":{"$ref":"#/components/schemas/white-label::LocalisedText"},"description":{"$ref":"#/components/schemas/white-label::LocalisedText"},"productKinds":{"type":"array","description":"The catalogue `ProductKind` values this type books. A venue's default flow for a type serves every product of these kinds that names no flow of its own.","items":{"type":"string"}},"steps":{"type":"array","description":"In the type's default order.","items":{"type":"object","required":["stepKey","requirement","defaultSortOrder"],"properties":{"stepKey":{"$ref":"#/components/schemas/BookingFlowStepKey"},"requirement":{"type":"string","enum":["required","optional","conditional"]},"condition":{"allOf":[{"$ref":"#/components/schemas/white-label::LocalisedText"}],"nullable":true,"description":"For `conditional`, when a guest meets the step."},"defaultEnabled":{"type":"boolean","default":true},"defaultSortOrder":{"type":"integer","minimum":0},"settingsOwned":{"type":"array","description":"Names of `BookingFlowSettings` (venue-wide) or `BookingFlowLevelSettings` (this flow) fields shown beside the step.","items":{"type":"string"}},"stepSettings":{"type":"array","description":"The step's own settings, kept in `BookingFlowStep.settings`.","items":{"type":"object","required":["name","type"],"properties":{"name":{"type":"string"},"type":{"type":"string"},"default":{"description":"The value when the venue sets none."}}}}}}},"orderConstraints":{"type":"array","description":"`first` and `last` pin a step; `before` puts `stepKey` somewhere ahead of `otherStepKey`. The common constraints (payment last, location first, Help me choose before the products) apply to every type as well as these.","items":{"type":"object","required":["kind","stepKey"],"properties":{"kind":{"type":"string","enum":["first","last","before"]},"stepKey":{"$ref":"#/components/schemas/BookingFlowStepKey"},"otherStepKey":{"allOf":[{"$ref":"#/components/schemas/BookingFlowStepKey"}],"nullable":true,"description":"Required when `kind` is `before`."}}}}}},
"BookingFlowTypeKey": {"type":"string","description":"**The flow types the system catalogue offers (decided 29 September, W12; impact.md b).** `seatedFixedPerformance` and `seatedDateTimeSeatMap` are the two seated flows; `cabanaMap` and `cabanaBySize` are the two cabana flows (W6); `experienceWorkshop` puts the product before the date (W8); `multiLocation` opens on the location switcher.\n","enum":["datedDayPass","timedEntry","openDated","seatedFixedPerformance","seatedDateTimeSeatMap","experienceWorkshop","surfSession","meetingRoomHourly","cabanaMap","cabanaBySize","guidedTourByLanguage","transport","tableReservation","membership","giftCard","multiLocation"]},
"BookingFlowValidation": {"x-ticvai-persistence":"none — computed","type":"object","required":["valid","problems"],"properties":{"valid":{"type":"boolean"},"problems":{"type":"array","items":{"type":"object","required":["kind","stepKey","message"],"properties":{"kind":{"type":"string","enum":["requiredStepDisabled","orderConstraintBroken","conditionNeverHolds","stepNotInType","duplicateStep","unknownStepSetting"]},"stepKey":{"$ref":"#/components/schemas/BookingFlowStepKey"},"otherStepKey":{"allOf":[{"$ref":"#/components/schemas/BookingFlowStepKey"}],"nullable":true,"description":"For `orderConstraintBroken`, the step it must come before or after."},"message":{"type":"string"}}}}}},
"BrandIdentity": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","description":"Every `*AssetRef` here is a `MediaAsset` id from the `assets` library (`createUpload` then `completeUpload`), PNG or SVG and at most 2 MB (decided 28 September, audit R270).\n","required":["logoAssetRef"],"properties":{"logoAssetRef":{"type":"string","format":"uuid","description":"The primary logo."},"logoDarkAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"Used on dark backgrounds. Falls back to the primary logo."},"logoVariant":{"type":"string","enum":["light","dark","duotone"],"default":"light","description":"**Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4).** `light` uses `logoAssetRef`, `dark` uses `logoDarkAssetRef` (falling back to the primary logo), and `duotone` the two-colour reading of the primary logo.\n"},"faviconAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"The browser tab icon for the guest web app."},"splashImageAssetRefs":{"type":"array","description":"Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163).","items":{"type":"string","format":"uuid"}},"splashDurationSeconds":{"type":"integer","minimum":0,"maximum":10,"default":3},"splashBackgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"showLoadingIndicator":{"type":"boolean","default":true},"splashChangeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163)."},"introVideoAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"**The optional intro video (decided 29 September, MOB-5).** A video `MediaAsset` from the media library (CMS-010). Streamed, so a change reaches guests with the publish and needs no app build.\n"},"introVideoMode":{"type":"string","enum":["off","firstLaunch","everyLaunch"],"default":"off","description":"When GST-001 plays it full screen. \"Skip introduction\" is always shown. Anything but `off` needs `introVideoAssetRef`, or 400."},"showPoweredBy":{"type":"boolean","default":true,"description":"**\"Powered by TICVAI\", a configuration toggle, on by default** (Chinmay, 2 October, workbook Q160 and the pre-apply round; consistent with DI-297; CHG-CSA-036). Shown on the launch screen and at the foot of Account and the web footer while true. **Switching it off needs the tenant's licence to allow it**: `setBrandIdentity` refuses `false` with `403 powered-by-locked` unless the tenant's plan carries the `poweredByRemoval` add-on (subscription `LicencePosition.poweredByRemovable`)."}}},
"ChangeScope": {"type":"string","description":"Whether a change reaches guests on publish or needs a store release.\n","enum":["runtime","buildTime"]},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"ConfigFindingKind": {"type":"string","enum":["missingTranslation","navigationTargetsDisabledModule","homepageReferencesMissingContent","contrastFailure","missingRequiredAsset","policyVersionMissing","noVisibleNavigationItems","unlicensedModuleEnabled","arabicFontMissing","bookingFlowInvalid","bookingFlowMissing"]},
"ConfigValidationReport": {"x-ticvai-persistence":"none — computed","type":"object","required":["passed","errorCount","warningCount","findings"],"properties":{"passed":{"type":"boolean"},"errorCount":{"type":"integer"},"warningCount":{"type":"integer"},"findings":{"type":"array","items":{"type":"object","required":["kind","severity","message"],"properties":{"kind":{"$ref":"#/components/schemas/ConfigFindingKind"},"severity":{"type":"string","enum":["error","warning"]},"message":{"type":"string"},"area":{"type":"string"},"reference":{"type":"string","nullable":true}}}}}},
"ConfigVersion": {"x-ticvai-persistence":"whitelabel.config_version","type":"object","required":["version","publishedAt","publishedByPrincipalId","note","isCurrent"],"properties":{"version":{"type":"string"},"publishedAt":{"type":"string","format":"date-time"},"publishedByPrincipalId":{"type":"string","format":"uuid"},"publishedByName":{"type":"string"},"note":{"type":"string"},"reviewStatus":{"type":"string","readOnly":true,"enum":["notRequired","pending","approved","rejected"],"default":"notRequired","description":"The review step, where the tenant's publish-review policy is on (CHG-CSA-042)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"isCurrent":{"type":"boolean"},"scheduledFor":{"type":"string","format":"date-time","nullable":true},"contentHash":{"type":"string"},"pendingBuildTimeChanges":{"type":"array","description":"Changes in this version that will not reach guests until the next store release. Surfaced at publish so nobody expects a new icon tomorrow.\n","items":{"type":"object","properties":{"area":{"type":"string"},"description":{"type":"string"},"platforms":{"type":"array","items":{"type":"string","enum":["ios","android","web"]}}}}},"snapshot":{"type":"object","additionalProperties":true,"readOnly":true,"description":"**What this version contained.** The working draft exactly as published, in the shape `getTenantConfig` returns (`TenantConfig`) — so `restoreConfigVersion` has something to copy back and `diffConfigVersion` something to compare. Deliberately an open object here: its shape is `TenantConfig`, and a `$ref` would make it a key to a `tenant_config` row rather than a copy. Written once by `publishTenantConfig` and never changed. Left out of `listConfigVersions` items; a version's content is read with `getTenantConfig?version=`.\n"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"ConsentQuestion": {"type":"object","x-ticvai-persistence":"marketing.consent_question + marketing.consent_question_version","description":"**A venue-defined consent question asked at booking** (decided 29 September, rev 3 REV3-26). Each version's text is kept in `consent_question_version`, so an answer always points at the exact words the guest saw. Attached to products by the catalogue and to booking flows by the white-label flow configuration; one or several per flow, as the venue chooses.\n","required":["id","kind","text","version","scope","required","blockingAnswer","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/ConsentQuestionKind"},"text":{"allOf":[{"$ref":"#/components/schemas/marketing-crm::LocalisedText"}],"description":"The question as the guest reads it, per locale."},"helpText":{"allOf":[{"$ref":"#/components/schemas/marketing-crm::LocalisedText"}],"nullable":true},"version":{"type":"integer","minimum":1,"readOnly":true,"description":"Raised by one each time the question changes (`updateConsentQuestion`)."},"scope":{"type":"string","enum":["perPerson","perBooking"],"default":"perPerson","description":"Asked for each declared person, or once for the whole booking."},"required":{"type":"boolean","default":true,"description":"Checkout waits until it is answered (`orders.checkoutCart` 422 `consentRequired`)."},"blockingAnswer":{"type":"string","enum":["yes","no","none"],"default":"none","description":"The answer that stops the booking, for the person or the booking it covers. `none` records the answer and blocks nothing."},"status":{"type":"string","enum":["active","retired"],"default":"active"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ConsentQuestionKind": {"type":"string","description":"What the question is about (decided 29 September, rev 3 REV3-26). `swim` feeds the derived `confidentSwimmer` on the order line; the others are recorded and checked as the venue set them.","enum":["swim","scuba","risk","custom"]},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"MinimumAppVersion": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n","properties":{"ios":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"},"android":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"nameLocalised":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true,"description":"**The product's name in each language the venue sells in** (6 October 2026, CHG-R4-011), keyed by ISO 639-1 code, e.g. `{\"en\": \"Aquarium entry\", \"ar\": \"دخول الأكواريوم\"}`. Every guest surface shows the entry for the guest's language and falls back to `name`, which stays the name staff search and reports print. Null, or a language missing from it, means `name` is shown. At most 200 characters per language, as `name`.\n"},"descriptionLocalised":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true,"description":"The product's description in each language, as `nameLocalised`; falls back to `description` (6 October 2026, CHG-R4-011).\n"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true},"eventId":{"type":"string","format":"uuid","nullable":true,"description":"**The event this product sells admission to** (4 October 2026, CHG-FXC-011; WEB-002, WEB-004): a product page finds its event and the event's performances (`Performance.eventId`) give it dates. Null for a product not tied to an event (merchandise, a pass, a membership)."}}},
"ProductCategory": {"type":"object","x-ticvai-persistence":"catalogue.product_category","description":"Retail Board 2 of the client's design set, 20 August. **`listSeatCategories` existed and a product category did not** — a seat category prices a seat, and a merchandise hierarchy groups a catalogue.\n**Brand sits here rather than as its own entity.** A venue with four brands and a hierarchy five levels deep can express that with a parent; a venue with one brand should not have to maintain a table containing one row.\n**`displayOrder` is not alphabetical and that is the point.** A retail category list runs in the order the merchandiser wants a guest to see it, and sorting by name puts *Accessories* above *Apparel* forever.\n","required":["id","name","kind"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"code":{"type":"string","maxLength":64,"nullable":true,"x-ticvai-unique":"tenant","description":"**Taken from their category tables, 20 September.** Ours had a uuid and a localised name, so an importer matching *Beverages* had to match on a display string that a venue is free to translate.\n**Unique per tenant where set** (decided 28 September, audit R108): two categories in one tenant never share a code, and `setProductCategories` refuses a body that would, with `409 duplicate-code`.\n"},"nameLocalised":{"type":"object","additionalProperties":{"type":"string"}},"kind":{"type":"string","enum":["category","brand","collection","season","department"]},"parentId":{"type":"string","format":"uuid","nullable":true,"description":"**One tree, not four.** A brand under a department under a category is how a real merchandise hierarchy runs, and separate tables for each level cannot express a venue that nests them differently.\n"},"scopePath":{"type":"string","readOnly":true,"description":"Set by the server from the venue the caller acts at; not sent."},"displayOrder":{"type":"integer","default":100},"imageAssetId":{"type":"string","format":"uuid","nullable":true},"description":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true,"description":"The short line a guest reads under a category option, e.g. *Surf lessons: learn on the beginner wave with a coach* (decided 29 September, rev 3 REV3-19). Each language value at most 200 characters.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow for every product filed here** that names none of its own (decided 29 September, W12, BO-115). Null means the venue's flow for each product's `kind`. A white-label `BookingFlow` of the venue; `setProductCategories` refuses any other id with `422`.\n"},"isActive":{"type":"boolean","default":true,"description":"**Deactivated rather than deleted.** A category with a season behind it still names the products sold under it, and removing it rewrites last year's report.\n"}}},
"ProductCategoryNode": {"x-ticvai-persistence":"none — projection over catalogue.product_category","description":"**One node of the tree `listProductCategories` returns.** A `ProductCategory` with its children nested under it, in `displayOrder`, so no caller reassembles the hierarchy from `parentId`. `setProductCategories` still takes the flat list, because a write names each parent by id.\n","allOf":[{"$ref":"#/components/schemas/ProductCategory"},{"type":"object","required":["children"],"properties":{"children":{"type":"array","description":"Empty on a leaf.","items":{"$ref":"#/components/schemas/ProductCategoryNode"}}}}]},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"translationJobId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `proposeTranslations` job that drafted this proposal; `getTranslationProposals` reads a job's rows by it. Null on every other proposal (CHG-RFM-004)."},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"SiteSetupProgress": {"x-ticvai-persistence":"whitelabel.site_setup_progress","type":"object","description":"**The Site Builder's saved progress, one row per tenant (decided 29 September, W12 and M24-05).** Not configuration and not published. `presetKey` is the starting point the operator picked; the builder pre-fills each step from it, which is what keeps the minimum path to a working site at about 30 minutes.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true},"presetKey":{"type":"string","nullable":true,"enum":["themePark","waterPark","museum","theatreAndArena","singleAttraction","playCentre","multiVenue",null],"description":"The starting point. Each preset proposes the modules, the booking flow types (with their default step order), the homepage sections, the mobile tabs and a booking-flow `preset`; nothing is written until the operator accepts a step."},"currentStep":{"allOf":[{"$ref":"#/components/schemas/SiteSetupStepKey"}],"nullable":true},"steps":{"type":"object","description":"One entry per `SiteSetupStepKey`.","additionalProperties":{"type":"object","required":["status"],"properties":{"status":{"type":"string","enum":["notStarted","inProgress","done","skipped"]},"completedAt":{"type":"string","format":"date-time","nullable":true},"completedByPrincipalId":{"type":"string","format":"uuid","nullable":true}}}},"minimumPathDone":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onRead","description":"True once the minimum path is done: a logo, the four theme colours, at least one enabled valid booking flow and a published version. Everything else keeps its preset or schema default."},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `tenant` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"SiteSetupStepKey": {"type":"string","description":"The seven Site Builder steps, in order (decided 29 September, W12): venue and modules (CMS-001), ticketing flows (CMS-103), compose steps (CMS-103), Help me choose (CMS-101), look and feel (CMS-007, CMS-009, CMS-002, CMS-004, CMS-008, CMS-005, CMS-003), mobile app (CMS-009, CMS-004, CMS-007), preview and publish (CMS-006, CMS-012, CMS-014).\n","enum":["venueAndModules","ticketingFlows","composeSteps","helpMeChoose","lookAndFeel","mobileApp","previewAndPublish"]},
"StoreAccount": {"x-ticvai-persistence":"whitelabel.store_account","type":"object","description":"**One of the client's own store accounts (decided 24 September, M24-08).** TICVAI never publishes under its own developer account.\n","required":["store","accountHolderName","developerAccountId","appIdentifier"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"store":{"type":"string","enum":["appleAppStore","googlePlay"]},"accountHolderName":{"type":"string","maxLength":200,"description":"The client's legal entity as the store knows it."},"dunsNumber":{"type":"string","nullable":true,"pattern":"^[0-9]{9}$","description":"Required for `appleAppStore`; Apple enrols an organisation only with its D-U-N-S number."},"developerAccountId":{"type":"string","maxLength":64,"description":"Apple Team ID, or the Google Play developer account id."},"appIdentifier":{"type":"string","maxLength":155,"pattern":"^[A-Za-z][A-Za-z0-9_]*(\\.[A-Za-z0-9_]+)+$","description":"The bundle id (Apple) or application id (Google) the app is signed with."},"apiCredentialSecretRef":{"type":"string","nullable":true,"writeOnly":true,"description":"App Store Connect API key or Play service-account key, sent once and kept in the secret store; this is its reference. Needed only for `submitToStore`."},"hasApiCredential":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onRead"},"listing":{"type":"object","description":"The store listing.","properties":{"appName":{"$ref":"#/components/schemas/white-label::LocalisedText"},"subtitle":{"$ref":"#/components/schemas/white-label::LocalisedText"},"description":{"$ref":"#/components/schemas/white-label::LocalisedText"},"keywords":{"$ref":"#/components/schemas/white-label::LocalisedText"},"category":{"type":"string"},"supportUrl":{"type":"string","format":"uri"},"privacyPolicyUrl":{"type":"string","format":"uri"},"screenshotAssetRefs":{"type":"array","items":{"type":"string","format":"uuid"}}}},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `tenant` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"StorePublishingChecklist": {"x-ticvai-persistence":"none — computed","type":"object","required":["accounts","items"],"properties":{"accounts":{"type":"array","items":{"$ref":"#/components/schemas/StoreAccount"}},"items":{"type":"array","items":{"type":"object","required":["item","done"],"properties":{"item":{"type":"string","enum":["appleDunsNumber","appleDeveloperAccount","googlePlayDeveloperAccount","storeListing","appIcons","publishedConfiguration"]},"done":{"type":"boolean"},"clientOwned":{"type":"boolean","description":"True for the three accounts, which only the client can open."},"guidance":{"type":"string","description":"What to do next, in the operator's language."}}}}}},
"TenantAppStatus": {"x-ticvai-persistence":"none — computed","type":"object","description":"Computed on read. The published fields come from the current `ConfigVersion`, the maintenance fields from the tenant's `tenant_config` row (`setMaintenanceMode`), and the draft fields from the working draft. **Fields marked staff only are left out of a response to a caller without a staff session** (`getTenantAppStatus`).\n","required":["tenantId","isPublished","isInMaintenance"],"properties":{"tenantId":{"type":"string","format":"uuid"},"isPublished":{"type":"boolean","x-ticvai-derived":"onRead","description":"True once any version has been published."},"publishedVersion":{"type":"string","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"draftVersion":{"type":"string","description":"Staff only."},"hasUnpublishedChanges":{"type":"boolean","x-ticvai-derived":"onRead","description":"Staff only. The working draft differs from the current version's `snapshot`."},"activeModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isEnabled` true."},"licensedModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isLicensed` true."},"activePageCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. Content pages that are `published` and enabled."},"isInMaintenance":{"type":"boolean"},"maintenanceMessage":{"$ref":"#/components/schemas/white-label::LocalisedText"},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"$ref":"#/components/schemas/MinimumAppVersion"},"contact":{"$ref":"#/components/schemas/VenueContact"},"availability":{"$ref":"#/components/schemas/AppAvailability"},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/white-label::LocalisedText"}],"nullable":true,"description":"What the sold-out or closed screen says (WEB-029). Null shows the default wording."},"venues":{"type":"array","maxItems":200,"x-ticvai-derived":"onRead","description":"**Public: the venues a guest can pick** (decided 28 September, audit R267; schema named 29 September, readiness close-out, our build plan). The source of the venue picker on WEB-001 and GST-001, returned with or without a session. **Published only**: a venue is listed when its scope node is active (`tenancy.OrgUnit.isActive`) and it is in the tenant's current published `ConfigVersion`; a venue added or reactivated since the last publish appears after the next publish, and a draft never reaches a guest. Ordered by `name`. Empty when nothing is published.\n","items":{"type":"object","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid","description":"**The venue's scope node** (`tenancy.OrgUnit.id`, level venue): what every guest screen that declares `venueId` `from: session` reads once the guest picks it."},"name":{"type":"string","maxLength":200,"description":"The venue's name (`tenancy.OrgUnit.name`)."},"city":{"type":"string","maxLength":120,"nullable":true,"description":"Shown under the name so two venues with similar names can be told apart."},"openingHoursToday":{"type":"object","nullable":true,"description":"Today's opening hours in the venue's time zone, from `tenancy.VenueSettings` opening hours. Null when the venue is closed today or has none set.","properties":{"opens":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"},"closes":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"}}}}}},"whatsNew":{"type":"array","maxItems":10,"x-ticvai-derived":"onRead","description":"**Public: the guest \"what's new\"** (decided 29 September, rev 3 GAP-B2). Newest first, at most 10, from `platform-ops.Release.guestReleaseNotes` of the releases the tenant's cell has received; a release with no guest notes is skipped. Returned with or without a staff session.\n","items":{"type":"object","required":["version","publishedAt","notes"],"properties":{"version":{"type":"string","description":"The release version."},"publishedAt":{"type":"string","format":"date-time","description":"When the release reached the tenant's cell."},"notes":{"$ref":"#/components/schemas/white-label::LocalisedText"}}}},"recentChanges":{"type":"array","description":"Staff only. Names the principal behind each change, so it never reaches a public response.","items":{"type":"object","properties":{"area":{"type":"string"},"description":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"}}}}}},
"UpdateProductRequest": {"type":"object","minProperties":1,"properties":{"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"The product family across the tenant's venues (decided 29 September, rev 3 REV3-18); see `Product.familyKey`. At most one product per venue in a family, else `409 duplicate-code`."},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"nameLocalised":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true,"description":"See `Product.nameLocalised` (CHG-R4-011). Replaces the whole map; null clears it."},"descriptionLocalised":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true,"description":"See `Product.descriptionLocalised` (CHG-R4-011). Replaces the whole map; null clears it."},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"dataMaskValues":{"type":"object","additionalProperties":true},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"See `Product.salesContact` (W3, 29 September)."},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"See `Product.bookingFlowId` (W8, W12, 29 September)."},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"}},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"}},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"}},"requiresTimeWindow":{"type":"boolean"}}},
"VenueContact": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n","properties":{"phone":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true},"whatsapp":{"type":"string","nullable":true},"address":{"allOf":[{"$ref":"#/components/schemas/white-label::LocalisedText"}],"nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/white-label::LocalisedText"}],"nullable":true,"description":"Prose, as the guest reads it. The bookable hours are the catalogue's."}}}
}
```
