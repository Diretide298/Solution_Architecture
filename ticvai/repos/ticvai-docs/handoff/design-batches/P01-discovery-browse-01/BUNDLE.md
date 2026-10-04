# P01-discovery-browse-01 — P01 · Discovery & Browse

**5 screens · 22 operations · 59 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `AI_USE, ORDER_VIEW, PRODUCT_VIEW`. A control nobody can use must say so,
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

### Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale)

A guest finds something to do, picks when and how many, holds capacity, pays, and receives a ticket they can show at the gate, transfer or resell. The same booking engine serves the guest website (P01, WEB-), the guest app (P02, GST-) and, through the same catalogue, cart and order operations, the kiosk (P05), the cashier at the till (P04) and the staff handheld (P06); partners book on credit through the partner portal (P10). Guest surfaces are white-label (venue logo, colours, fonts, card layouts, step indicator style, cart placement) with "Powered by TICVAI" kept; the till and handheld stay TICVAI-branded. The booking runs in a fixed order that the client set on 29 September and confirmed on 30 September: for a dated product, the date first, then the time (hidden until a date), then the tickets (hidden until a time); undated products go straight to the tickets; product-first flows (workshops) pick the product, then the date; seated events with one performance open on the seat map, sections first, zoom into a section, pinch out to compare. Choosing a date, time or session commits nothing; capacity is held only when a quantity is set (a 15-minute basket window, 8 minutes for seats and cabanas, one extension). The guest counters (adult, child, senior, infant, person of determination) belong to the chosen ticket and take its prices, so a basket line is "<ticket> · <guest type> × <n>"; group and school products start from group ticket cards and a typed headcount (minus, plus, and +10 on the app), supervisors free. Help me choose filters the catalogue on the server (never a consent step) with Show everything; consent questions such as "Are you able to swim?" are asked once after the session is picked and never again where the page already asked. Sign-in or the six-digit guest code is asked when the guest leaves Add-ons (or at payment, per venue), only the fields the venue configured; after the code, only the T&Cs tick remains (W1). Payment creates the order first and treats an unknown outcome as "checking with your bank", never a second charge; tickets issue on payment, go to Apple or Google Wallet, and a dynamic-QR event's ticket lives in the app. The guest app is deliberately not a copy of the website (30 September): its structure is Home, Explore, Plan and Tickets tabs with a persistent Buy tickets button, item pages that propose the right product (a restaurant's meal combo that includes admission), ride videos that play with no loader, a visit planner that plans each day at one park from that park's rides, dining and shops only, and in-park walking navigation; the booking flow inside it is functionally identical to the web. Vocabulary in guest copy follows the glossary's recorded exceptions (Booking, Session, QR). source: [F01, F02, F03, F07, F49, F52, F55, F57, F58, F59, MoM 29 Sep 1 (W1-W12), MoM 29 Sep 2, MoM 29 Sep 3, MoM 30 Sep 4.4-4.8, CLIENT-RESPONSE-30SEP 1-6, CLIENT-RESPONSE-REV3-25SEP, REV3-1, REV3-2, REV3-3, REV3-4, REV3-26, DI-1086 …

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Booking | An order or reservation as the guest reads it (Booking Confirmation, Group Booking, My bookings). Code says Order or Reservation. | Order (in guest copy), Purchase record, Transaction | docs/glossary.md (Recorded exceptions, Booking, audit R145) |
| Session | A dated, timed performance as the guest reads it (Pick a session, Surf sessions). Staff screens (POS, back office) keep Performance. | Slot, Showtime, Performance (in guest copy) | docs/glossary.md (Recorded exceptions, Session, rev 3 CFG-10); DI-1064 |
| Basket | The guest's unpaid selection with its held capacity (Add to basket, Your basket). Never a paid order. The till and staff screens say Cart. | Cart (in guest copy), Bag, Order (for an unpaid selection) | CLIENT-RESPONSE-REV3-25SEP (Basket, 10) … |
| Ticket | The issued instrument a guest shows at the gate. Product names from the catalogue keep their own words (Day Pass, Annual pass, 2 park ticket); the interface around them says ticket. | Admission, Voucher (for a ticket), Pass (in interface copy) | docs/glossary.md (Ticket) |
| Adult, Child, Senior, Infant, Person of determination | The guest types of a ticket, each with its age or height band shown under it (Child 3-12, Under 1.20 m). A companion of a person of determination is its own free type where the product has one. | Disabled, Handicapped, Kid, Pax | DI-686; screens/P01-guest-web-storefront.yaml#WEB-049 (Passengers notes) … |
| Held for | The countdown on held capacity ("Your seats are held for 7:42"); the release is Release hold. | Lease, Reserved for (a reservation is a different thing), Locked | contracts/spine/orders.yaml#/components/schemas/CartLine (leaseExpiresAt) … |
| Reservation | Booked and not yet paid; holds capacity and expires (My Reservations). Paid tickets are in Tickets or My Tickets. | Booking (for an unpaid hold in lists), Pending order | docs/glossary.md (Reservation); DI-199 |
| Help me choose | The venue's questions whose answers filter the products; Show everything clears them. | Quiz, Wizard, Experience builder, Consent | MoM 29 Sep W4; REV3-11 |
| Info only / Not bookable online | A product listed with full details that cannot be booked online; it shows Contact sales to book with Call sales and Email sales. | Unavailable, Sold out, Coming soon | REV3-14; MoM 29 Sep W3 |
| Guest code | The six-digit code sent to the guest's email or mobile to prove the contact at guest checkout; the copy says six digits. | OTP, PIN, Token, Verification key | DI-1034; MoM 29 Sep W1 |
| How many people | The typed headcount of a group or school booking (number box with minus and plus; +10 on the app), with Supervisors listed separately and free. | Group size (the removed dropdown), Pax | DI-1104; DI-1105; CLIENT-RESPONSE-30SEP 1 |
| Waiting room | The on-sale queue in front of a high-demand performance's sale (WEB-015, GST-046). | Virtual queue (that is the ride queue), Lobby | screens/P01-guest-web-storefront.yaml#WEB-015 notes (ADR-0066) |
| QR | The code a guest shows, in guest copy only (Dynamic QR). Staff screens say Media code. | Barcode, Serial, Media code (in guest copy) | docs/glossary.md (Recorded exceptions, QR, audit R210) |
| Not at this park | The planner's per-day notice that the day's park cannot meet a preference, naming the park that can. | Unavailable, No results | DI-1113 |
| Book this plan | Turns the whole visit plan (tickets, Fast Track, meal combos) into basket lines. | Checkout plan, Buy itinerary | screens/P02-guest-mobile-app.yaml#GST-053 (Book this plan) |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `WEB-001` | Home / Landing | A | 1 | 67 | 6 | 63 | 8 | 0 | guest | review (client-verified) |
| `WEB-002` | Event & Attraction Listing | A | 3 | 87 | 6 | 22 | 10 | 0 | guest | review (client-verified) |
| `WEB-003` | Search Results | A | 2 | 18 | 6 | 15 | 0 | 0 | guest | review (client-verified) |
| `WEB-004` | Attraction Details | A | 1 | 81 | 8 | 24 | 17 | 0 | guest | review (client-verified) |
| `WEB-050` | Plan Your Visit | A | 40 | 60 | 7 | 3 | 7 | 1 | guest | review (client-verified) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `WEB-001` Home / Landing

**Show a guest what is on and give them one obvious way to start booking.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Discovery & Browse · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #28333 (APP-WEB-WEB-001) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listProducts` reads the population and `getTenantAppStatus` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | nothing: it opens on its own · cold entry: **A cold arrival is the ordinary case.** **The venue comes from the device** (decided 28 September, audit R267): on first open the guest picks one, it is … |
| Route | `/discovery-and-browse/home-landing` |

**What the spec says about it.** **Venue selection added 28 September** (decided 28 September, audit R267): a venue picker on first open, remembered on the device, **Change venue** in the header, and a visit-day suggestion from the guest's ticket. The options come from `getTenantAppStatus.venues`, the tenant's active venues, public and cacheable. **Rev 3 (decided 29 September).** Category cards render as a grid or as one scrolling row per `BookingFlowConfig.cardLayout` (the retired `categoryDisplay` of 23SEP-18 is removed, W7). The event banner lists dates only when `BookingFlowConfig.eventBannerDates` is on (default off; 23SEP-19); the date picker always sits at the top of the booking step. The venue picked here (audit R267) is the venue whose booking-flow settings apply on every booking screen, and the booking screens' *Booking at* bar changes it (REV3-18). Every booking-flow setting named here is read from `getPublishedTenantConfig` `bookingFlow`, resolved for the venue the guest picked (audit R267): the tenant's values with that venue's `venueOverrides` entry laid over field by field (decided 29 September, rev 3 CFG-11). The UI preset stays `BookingFlowConfig.preset` (CFG-1, no change); the search box in the banner is off by default (`searchInBanner` default false, CFG-6). The in-venue notifications link is live again: WEB-046 is back in the first release (GAP-C1, reversing audit R242). **29 September.** *Plan your visit* in the header opens WEB-050 full screen (MOB-6). W7: `categoryDisplay` is retired.

**Known gaps.** Replaced by `getPublishedTenantConfig`, the guest read of the same data.

**From the White Label & CMS process.** The guest web home, entirely in the tenant's brand: header, hero, the tenant's homepage sections in its order, the ticket categories, banners, the footer with the Powered by TICVAI credit (shown by default). A first visit asks for the venue first. The one thing to get right for white-label: everything visual comes from the published configuration resolved for the chosen venue, and nothing renders for a disabled module.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- TenantConfig.venues (name as LocalisedText, from tenancy, active venues) and TenantAppStatus.venues (name as a string, published venues only) describe the same picker differently. (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): The context panel shows staff-only TenantAppStatus fields (draftVersion, hasUnpublishedChanges, counts, recentChanges) and … (CHG-GST-003); getTenantConfig (the theme, fonts, header, navigation, homepage) needs a guest session or a staff session; a first-time visitor has neither. (CHG-GST-001); The product table lists staff columns (createdByPrincipalId, approvedByPrincipalId, scopePath) and filters Kind and Is sellable as text … (CHG-GST-003).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the web homepage arranged by the same HomepageLayout as the app Home, or does it need its own (DI-285 asks web and mobile independently)?** → The client-approved web and app wireframes are the layout; change them only where the spec breaks. *(decided by Chinmay, 2026-10-02; DEC-163 / CHG-NOTE-009 / CHG-SGU-005)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Your venue | repeatable rows | optional | — | at most 200 | — | **The guest picks a venue on first open** (decided 28 September, audit R267): shown before anything else when the device has no venue remembered, and remembered on the device after that. The chosen … | `TenantAppStatus.venues` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |
| State | radio group | Usable now | Usable now · Upcoming · Expired · All | `listMyEntitlements` ?state |
| Include shared | toggle | on | — | `listMyEntitlements` ?includeShared |
| Channel | select | — | B2C website · Customer portal · Mobile app · Embedded checkout · White label site · Partner microsite | `getCookieConsentRuntime` ?channel |
| Brand | picker: choose a brand | — | — | `getCookieConsentRuntime` ?brandId |
| Language | text field | — | max length 10 | `getCookieConsentRuntime` ?language |

**Rules for these inputs** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Your venue**: On first open, before anything else, a venue picker from the tenant's published, active venues (name, city, today's hours), remembered on the device; Change venue in the header. A tenant with one venue skips it. *(source: R267; contracts/satellite/white-label.yaml#getTenantAppStatus)*
- **Language**: EN / العربية button in the header (only the tenant's enabled languages); the whole page mirrors in Arabic. *(source: DI-975; contracts/satellite/white-label.yaml#setLanguages)*

#### Outputs: what the screen shows and produces

**Shown**

**Visiting today?** (banner, from `listMyEntitlements`): **On a visit day the app suggests the ticket's venue** (decided 28 September, audit R267): for a signed-in guest, an entitlement from `listMyEntitlements` (`state=upcoming`) valid today at a venue other than the chosen one offers **Switch to that venue**; the guest decides, the app never switches by itself.

| Shows | Format | Notes |
|---|---|---|
| Venue | the name it points at, never the id | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Resolved at issue from the template, then owned here. A freeze extends it, a reissue replaces it, and neither reaches back to the template. |

**Sold out or closed today** (banner, from `getTenantAppStatus`): From `getTenantAppStatus.availability` (`open`, `soldOut`, `closed`) and `availabilityMessage` (decided 28 September, audit R073 (f)); nothing shows while it is `open`.

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

**What's on** (card list, from `listProducts`): Guest cards show name, image, from-price, tags and availability only (DI-026). The venue is the one the guest picked on Home (`venueId` from the session, audit R267), never typed. Was the generated table 'Every product'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Media | list or chips (count when long) | The product's own photos and video (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each … |
| Display tags | list or chips (count when long) | Short facts a guest reads on the ticket card and under *Read more*: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates … |

**Banner** (banner, from `getTenantAppStatus`): Only when isInMaintenance. Tenant-branded, never a generic error page

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

**Home sections** (card list, from `getPublishedTenantConfig`): The sections of the published home, from the tenant's template (`templateKey`) or its own layout, each with the card count the venue chose (`maxItems`) and its scroll animation. **The client-approved web wireframe is the layout** (decided by Chinmay, 2 October 2026; DEC-163); a tenant with its own landing page links in with deep links (DEC-548) (CHG-SGU-005).

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Search (icon button) | navigation or local | — | — | — | — |
| Sign in (secondary button) | navigation or local | — | — | — | — |
| Change venue (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Header**: HeaderConfig layout (logo left, logo centre or logo with menu) with the logoVariant lockup, navigation items from NavigationConfig, language button, single profile icon, cart. Never a date picker in the header. *(source: contracts/satellite/white-label.yaml#/components/schemas/HeaderConfig; DI-990; DI-974)*
- **Hero**: Shown when heroBanner is on (default) and embedMode is fullPage; a video hero streams with a poster fallback; the search box only when searchInBanner is on (default off). Banners with placement homepageHero rotate here in their schedule. *(source: DI-945; DI-738; DI-1070; contracts/satellite/white-label.yaml#/components/schemas/Banner)*
- **Sections**: HomepageLayout sections in sortOrder, visible ones only; a section whose module is off does not render at all (no empty frame). *(source: contracts/satellite/white-label.yaml#setHomepageLayout; screens/P01-guest-web-storefront.yaml#WEB-001)*
- **Category and product cards**: cardLayout decides the arrangement: Cards across and Poster cards wrap into an equal-height grid; Stacked rows and Split rows stay one column and the Discover rail scrolls sideways. cardSize and density scale them. Info-only products show their label when showInfoOnly is on. *(source: DI-1040; DI-1009; sources/designs/guest-rev3-30-september/TICVAI Engine Controls Manual.dc.html; DI-1054)*
- **Footer**: The tenant's columns, the legal links (always present), copyright and social links, then the "Powered by TICVAI" line unless the venue switched it off (CMS-104). *(source: contracts/satellite/white-label.yaml#setFooter; DI-111; decided 2 October 2026 by Chinmay (CHG-NOTE-009))*
- **Availability banner**: Sold out today or Closed with the tenant's message, under the header; nothing while open. *(source: R073)*
- **Layout**: The client-approved web and app wireframes are the layout; change them only where the spec breaks. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-009))*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Change venue**: Replaces the remembered venue; every venue-scoped screen and the venue's booking-setting overrides reload. *(source: R267; DI-1063)*

**Data it reads**: `getTenantAppStatus` (onLoad, Maintenance check before rendering anything); `getPublishedTenantConfig` (onLoad, The published brand, theme, fonts, header, footer …); `listProducts` (onLoad, List products); `listMyEntitlements` (onLoad, The guest's upcoming tickets, so a visit day can suggest …); `getCookieConsentRuntime` (onLoad, Cookie banner on first visit and what the tag loader may …); `decideRecommendations` (onLoad, Recommendation slot (homepage / loyalty placement …); `recordStorefrontSessionEvents` (onLoad, Runtime-shell beacon of hashed browsing behaviour for fraud …)

**Where the user goes next**

- → `WEB-002` Event & Attraction Listing: *Event & Attraction Listing*; carries `eventId`
- → `WEB-003` Search Results: *Search Results*
- → `WEB-016` Login / Register: *Login / Register*
- → `WEB-036` F&B – Browse & Order: *F&B – Browse & Order*
- → `WEB-037` Menu Item Detail: *Menu Item Detail*
- → `WEB-038` F&B – Order Tracking: *F&B – Order Tracking*
- → `WEB-039` Venue Map & Wait Times: *Venue Map & Wait Times*
- → `WEB-040` Virtual Queue: *Virtual Queue*
- → `WEB-041` Parking – Reserve & Pay: *Parking – Reserve & Pay*; carries `entitlementId`
- → `WEB-042` Retail & Shop and Drop: *Retail & Shop and Drop*
- → `WEB-043` Loyalty & Rewards: *Loyalty & Rewards*
- → `WEB-044` AI Concierge – Home: *AI Concierge – Home*
- → `WEB-045` Help Centre & Accessibility: *Help Centre & Accessibility*
- → `WEB-046` In-Venue Notifications: *In-Venue Notifications*
- → `WEB-008` Add-ons & Upsell: *Add-ons & Upsell*
- → `WEB-009` Wishlist: *Wishlist*
- → `WEB-017` My Account Dashboard: *My Account Dashboard*
- → `WEB-018` My Tickets: *My Tickets*; carries `entitlementId`, `orderId`
- → `WEB-019` Order History: *Order History*
- → `WEB-021` Wallet & Gift Cards: *Wallet & Gift Cards*
- → `WEB-022` Membership Plans: *Membership Plans*; carries `productId`
- → `WEB-023` Membership Management: *Membership Management*
- → `WEB-024` Devices, Wishlist & Consent: *Devices, Wishlist & Consent*
- → `WEB-027` Newsletter Subscription: *Newsletter Subscription*
- → `WEB-032` Offers & Promotions: *Offers & Promotions*
- → `WEB-033` Shop: *Shop*
- → `WEB-034` Lost & Found: *Lost & Found*
- → `WEB-020` Profile & Preferences: *Profile & Preferences*
- → `WEB-025` Help Centre / FAQ: *Help Centre / FAQ*
- → `WEB-026` Survey & Feedback: *Survey & Feedback*
- → `WEB-028` Contact & Venue Information: *Contact & Venue Information*
- → `WEB-029` Error / Sold Out / Maintenance: *Error / Sold Out / Maintenance*
- → `WEB-049` Transport — Route & Schedule: *Book a trip (a transport venue)*
- → `WEB-050` Plan Your Visit: *Plan your visit (header)*
- → `WEB-004` Attraction Details: *Opens a product and decides*; carries `eventId`, `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The home landing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the home landing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No home landing yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing is on sale at this venue today. Said in the tenant's voice, with **Change venue**; the homepage sections that do not list products stay. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 A field outside the batch shape (a URL with a query, free text, an unhashed id), or more than 50 interactions.; 400 No published banner design with this id for the channel, or a category the design does not offer; 409 `noticeVersion` is … |

#### Edge cases to draw

- **Tenant has never published**: getTenantConfig answers 404 not-configured; show a neutral "This site is opening soon" with Powered by TICVAI, no tenant brand. *(source: contracts/satellite/white-label.yaml#getTenantConfig)*
- **Maintenance on**: The branded maintenance page (WEB-029) replaces the home, not a banner on it. *(source: contracts/satellite/white-label.yaml#setMaintenanceMode)*
- **Embedded mode**: No venue header, hero or footer; the powered-by strip and progress stay. *(source: sources/designs/guest-rev3-30-september/TICVAI Engine Controls Manual.dc.html)*

#### Consistency with other screens

- Match `GST-001`: Same venue picker, availability banner and section order (app shows its own Home sections).
- Match `CMS-007`: What CMS-007 previews is this page.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venues:
- name: Coastal Aqua Yas Island
  city: Abu Dhabi
  hours: 10:00 – 19:00
- name: Kids Club Al Barsha
  city: Dubai
  hours: 09:00 – 21:00
- name: Kids Club Mirdif
  city: Dubai
  hours: 09:00 – 21:00
hero:
  en: Make a splash this weekend
  ar: استمتع بعطلة نهاية أسبوع مليئة بالمرح
categories:
- Day passes
- Cabanas
- Annual passes
- Gift cards
```

#### Permissions

- `getTenantAppStatus` → no permission · device, guest, staff
- `getPublishedTenantConfig` → no permission · anonymous, guest, device
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `listMyEntitlements` → `ORDER_VIEW` (read) · staff, guest
- `getCookieConsentRuntime` → no permission · anonymous, guest
- `recordDeviceConsent` → no permission · anonymous, guest
- `decideRecommendations` → `AI_USE` (operate) · staff, guest, anonymous
- `recordRecommendationEvents` → `AI_USE` (operate) · staff, guest, anonymous
- `recordStorefrontSessionEvents` → no permission · guest, anonymous

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

63 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.52 | Cookie Consent Banner Display a cookie consent banner on the first visit. Support configurable banner layouts (top, bottom, pop-up, modal). Multi-language support. Responsive design for desktop … | Ticketing Sales | CONTRACTED | `getCookieConsentRuntime` |
| 2.6.58 | Cookie Blocking Block non-essential cookies until consent is granted. Prevent loading of: - Analytics scripts - Marketing tags - Advertising trackers Enable cookies only after user approval. | Ticketing Sales | CONTRACTED | `getCookieConsentRuntime` |
| 22.13.10 | Cookie & Tracking Consent | Marketing & CRM | CONTRACTED | `getCookieConsentRuntime` |
| 2.6.51 | A Cookie Policy Management solution helps organizations comply with privacy regulations such as GDPR, ePrivacy Directive, CCPA/CPRA, and other regional data protection laws by managing user consent … | Ticketing Sales | CONTRACTED | `recordDeviceConsent` |
| 2.6.62 | Multi-Domain Support Manage cookie consent across multiple websites. Share consent preferences across related domains. Centralized administration. | Ticketing Sales | CONTRACTED | `recordDeviceConsent` |
| 2.6.65 | Non-Functional Requirements Security - Encrypt consent records. - Secure API communication. - Role-based access control. Performance - Banner should load within 1 second. - Minimal impact on website … | Ticketing Sales | CONTRACTED | `recordDeviceConsent` |
| 19.2.46 | Personalized Offers - System shall provide personalized offers. | Guest Mobile App & Branding | CONTRACTED | `decideRecommendations` |
| 1.1.33 | AI shall recommend suitable ticket products, upgrades, bundles and promotions based on guest profile, behavior and purchase history. | Ticketing Catalogue | CONTRACTED | `decideRecommendations` |
| 1.1.34 | AI shall recommend upgrades, add-ons and premium experiences during the purchasing journey. | Ticketing Catalogue | CONTRACTED | `decideRecommendations` |
| … 51 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Existing booking settings stay: step indicator, extras step, seat picker, map view, quantities on add-ons (−/+ stepper, price multiplies), embed mode, hero banner, search in banner, single-event page. Defaults: search in banner off, seat picker = bowl. *(agreed · design review 29 Sep 2026, CFG-6 · Step indicator; Extras step; Seat picker; Map view; Quantities on add-ons; Embed mode; Hero banner; Search in banner; Single-event page · DI-1070)*
- A UI preset (L1–L6, or Custom) picks a bundle of booking-UI settings per venue type. *(agreed · design review 29 Sep 2026, CFG-1 · Preset (UI preset L1-L6, Custom) · DI-1065)*
- Multi-location attractions: the guest picks a location first (e.g. Al Barsha, Mirdif, Yas Island, Sharjah); a "Booking at" bar on later booking steps has Change location. On a switch, times and prices refresh and the selection is cleared unless the products share a family. Setting "Location switcher". *(agreed · rev 3 design review 29 Sep 2026, REV3-18 · 18. One tenant with an attraction in several locations; change location · DI-1058)*
- The date list in the event banner (for multi-date events) is a setting, "Dates in event banner", off by default. The date picker always sits at the top of the booking step. *(agreed · design review 29 Sep 2026, Settings 19. Why is there a date selection in the header? · DI-1033)*
- The B2C home page lists the ticket categories directly; clicking one opens its counters on the same screen. *(client request · design review 23 Sep 2026, Tickets 8. Show the single day ticket category on the B2C home page · DI-977)*
- The hero banner and marketing layer (images, video, search, browse-by-venue, venue info) is optional and toggled in the white-label builder: on for clients without their own marketing site (Qossai: roughly 30%), off for a lean direct-to-ticket flow. *(agreed · MoM 18 Sep 2026, 4.11 Guest Website UX Review — Page Structure & Hero Banner Flexibility · DI-945)*
- Six Flags reference for the B2C redesign (Qossai): hero-banner product video. *(client request · MoM 8 Sep 2026, 4.20 Planning & Next Steps · DI-738)*
- Ticket listings are data-driven: creating a new ticket automatically surfaces it on the relevant site according to its category configuration. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-109)*

Also apply: 1 for P01 · Discovery & Browse, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Card layout (`bookingFlow.cardLayout`) | Stacked rows · Split rows · Cards across · Poster cards | Stacked rows | ticket and product cards: stacked rows, split rows, cards across, or poster cards |
| Search in banner (`bookingFlow.searchInBanner`) | — | off | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). |
| Event banner dates (`bookingFlow.eventBannerDates`) | — | off | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |
| Venue overrides (`bookingFlow.venueOverrides`) | at most 200; Per-venue overrides, at most one per venue.; A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. | — | Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. |
| Settings: card layout (`bookingFlow.venueOverrides[].settings.cardLayout`) | Stacked rows · Split rows · Cards across · Poster cards | Stacked rows | How ticket and product cards are laid out (decided 29 September, rev 3 DG-6). Was a free string; the four values are the design's Stacked rows, Split rows, Cards across and Poster cards. |
| Settings: search in banner (`bookingFlow.venueOverrides[].settings.searchInBanner`) | — | off | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). |
| Settings: event banner dates (`bookingFlow.venueOverrides[].settings.eventBannerDates`) | — | off | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |

*Homepage sections*, set in `CMS-007` Page Builder:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Landing-page template (`homepage.templateKey`) | — | — | the landing-page template the home started from (listLandingPageTemplates); a tenant with no landing page of its own starts from one, and the sections it fills stay editable |
| Sections: card count (`homepage.sections[].maxItems`) | — | — | how many cards the section shows, the counts the approved wireframe offers |

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

*Cookie banner*, set in `CMS-026` Cookie Banner & Preference Center Designer:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Brand (`cookieBanner.brandId`) | shows names, sends the id | — | Null for the corporate design every brand inherits. |
| Inherits from (`cookieBanner.inheritsFromId`) | shows names, sends the id | — | — |
| Cookie banner channel (`cookieBanner.channel`) | B2C website · Customer portal · Mobile app · Embedded checkout · White label site · Partner microsite | — | — |
| Logo (`cookieBanner.logoAssetId`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | — |
| Cookie banner title (`cookieBanner.title`) | English and Arabic (Arabic right to left) | — | — |
| Body (`cookieBanner.body`) | English and Arabic (Arabic right to left) | — | — |
| Position (`cookieBanner.position`) | Top · Bottom · Popup · Modal | — | — |
| Buttons: action (`cookieBanner.buttons[].action`) | Accept all · Reject non essential · Manage preferences · Save preferences · Do not sell or share | — | — |
| Buttons: label (`cookieBanner.buttons[].label`) | English and Arabic (Arabic right to left) | — | — |
| Reject is one click (`cookieBanner.rejectIsOneClick`) | — | on | Must be true. |
| Links: label (`cookieBanner.links[].label`) | English and Arabic (Arabic right to left) | — | — |
| Links: policy kind (`cookieBanner.links[].policyKind`) | Privacy · Cookie · Terms and conditions | — | — |
| Categories (`cookieBanner.categories`) | at least 1 | — | — |
| Categories: category (`cookieBanner.categories[].category`) | Strictly necessary · Functional · Analytics · Personalisation · Marketing | — | — |
| Categories: description (`cookieBanner.categories[].description`) | English and Arabic (Arabic right to left) | — | — |
| Categories: default on (`cookieBanner.categories[].defaultOn`) | True only for `strictlyNecessary`, which is always active. | — | True only for `strictlyNecessary`, which is always active. |
| Cookie banner languages (`cookieBanner.languages`) | at least 1 | — | Every language the storefront serves; Arabic renders right to left. |
| Regulatory regimes (`cookieBanner.regulatoryRegimes`) | Gdpr · E privacy · Ccpa cpra · Lgpd · Uae pdpl · Saudi pdpl | — | 2.6.60 (29 September, build). The laws this design is published to satisfy, so compliance is stated rather than assumed. |
| Record ip address (`cookieBanner.recordIpAddress`) | — | off | 2.6.55, "if legally permitted" (29 September, build). On, `recordDeviceConsent` writes the IP address and user agent to `pii.consent_identifier`; off, they are not kept anywhere. |

Also set there, as content the tenant writes: theme, buttons, links.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-001` · status **review** · provenance client-verified
- Prototype (rev 3 (pointer moved to the 30 September build, CHG-R1S-015), verified 2026-09-28, match partial): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Header 'Discover' (default view on load)*. Differences: No first-open venue picker remembered on the device and no 'Change venue' in the header (YAML R267); the prototype shows 'Browse by venue' tiles instead and switches venue from the Config drawer. Prototype adds a resume-booking card, a video 'Tonight in the city' panel, live queue times on cards and footer links to Contact / Accessibility / Service status. YAML emptyNoAccess/offline states are not drawn on Home (offline exists only as a demo tweak).
- Flow F01 *Guest buys a ticket online*, step 1: Lands and orients → Sees what is on, in the tenant's branding
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)
- ADR-0023 *— Personal data lives apart from the append-only ledger* (`docs/adr/0023-pii-separation.md`)
- ADR-0033 *Every asynchronous handoff has an outbox and a place to fail* (`docs/adr/0033-outbox-and-dead-letters.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (67 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-001?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Search, Sign in, Change venue.
- [ ] Every transition is wired: `WEB-002`, `WEB-003`, `WEB-016`, `WEB-036`, `WEB-037`, `WEB-038`, `WEB-039`, `WEB-040`, `WEB-041`, `WEB-042`, `WEB-043`, `WEB-044`, `WEB-045`, `WEB-046`, `WEB-008`, `WEB-009`, `WEB-017`, `WEB-018`, `WEB-019`, `WEB-021`, `WEB-022`, `WEB-023`, `WEB-024`, `WEB-027`, `WEB-032`, `WEB-033`, `WEB-034`, `WEB-020`, `WEB-025`, `WEB-026`, `WEB-028`, `WEB-029`, `WEB-049`, `WEB-050`, `WEB-004`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 8 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-002` Event & Attraction Listing

**Browse and filter everything bookable.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Discovery & Browse · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #28684 (APP-WEB-WEB-002) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listProducts` reads the population and `getWaitTimes` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `eventId` (deepLink), `venueId` (session) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation … |
| Route | `/discovery-and-browse/event-and-attraction-listing` |

**What the spec says about it.** **Cross-surface parity, 31 August**: added getWaitTimes. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations. **Rev 3 (decided 29 September).** Categories: tiles from `listProductCategories`, then `listProducts?categoryId=`, or one flat list, per `BookingFlowConfig.ticketCategories` (REV3-16); tiles as a grid or a row per `cardLayout` (`categoryDisplay` retired, W7). **Info-only products** (`Product.guestListing` `infoOnly`) are listed with `notBookableLabel` (default *Info only / Not bookable online*) and open their details instead of adding to the basket; they are hidden when `BookingFlowConfig.showInfoOnly` is off (REV3-14). Each card shows the product's own primary image (`Product.media` `isPrimary`, `searchCatalogue` `primaryMedia`; 23SEP-4). **Book** opens the ticket counters (WEB-005) as a side panel on this listing rather than a new page (23SEP-5). Card layout, size and density are the enums `cardLayout` [stackedRows, splitRows, cardsAcross, posterCards], `cardSize` [compact, standard, large, extraLarge] and `density` [compact, standard, roomy] (DG-6). Every booking-flow setting named here is read from `getPublishedTenantConfig` `bookingFlow`, resolved for the venue the guest picked (audit R267): the tenant's values with that venue's `venueOverrides` entry laid over field by field (decided 29 September, rev 3 CFG-11). **29 September.** W4: Help me choose filters this list, with *Show everything*. W3: view-only products show Call sales / Email sales. W7: `categoryDisplay` retired. …

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** The storefront's catalogue: every bookable thing at the venue the guest picked, as cards they can book from without leaving the page. Block A. The thing to get right is that a card goes straight into booking: Book opens the ticket counters as a side panel on this listing (no separate "Select tickets" page), and a dated product's panel starts with the date, not the counters.

**Fixed on main** (the package already carries these; draw what it says): The layout lists staff-style filter fields "Venue id", "Kind" (free text) and an "Is sellable" toggle, plus raw tables "Every product" … (CHG-GST-003).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should the category tiles show a product count ("Day passes · 4"), as in the 29 July selling reference?** → Drawn default accepted: Show the count on desktop tiles only. *(decided by Chinmay, 2026-10-02; DEC-114 / CHG-NOTE-007)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search events and attractions | search field | — | — | — | — | — | `searchCatalogue` |
| Category | multi select | — | — | — | — | — | — |
| Date | date picker | — | — | — | — | Picks a day; the listing keeps the events with a performance that day (`listPerformances`). | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |
| From | date and time picker | — | — | `listPerformances` ?from |
| To | date and time picker | — | — | `listPerformances` ?to |
| Category | picker: choose a category | — | — | `listPerformances` ?categoryId |
| Language | text field | — | max length 35; pattern `^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$` | `listPerformances` ?language |
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |

**Rules for these inputs** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **venue**: Never a field on this page. The venue comes from the guest's venue choice (session) and the "Booking at" bar where the location switcher is on; the contract's venueId query is filled silently. *(source: screens/P01-guest-web-storefront.yaml#WEB-002 entryState; REV3-18)*
- **category**: With ticketCategories = categoryThenSubcategory (default) the guest first sees category tiles (e.g. Day passes, Multi-park, Group and school, Annual passes) and then that category's products; with flatList all products show under category headings. Tiles carry the category's one-line description. There is no "Dated day pass" in-between step: the ticket categories show directly. *(source: REV3-16; DI-976; contracts/satellite/white-label.yaml#/components/schemas/BookingFlowSettings)*
- **search**: Free text, at least 2 characters before a search is sent; results replace the cards in place with the query shown as a removable chip. The hero search box shows only when searchInBanner is on (default off). *(source: contracts/spine/catalogue.yaml#searchCatalogue (q minLength 2); CFG-6)*
- **date**: Optional "visiting on" filter. Uses the venue's region date format (dd/MM/yyyy for UAE tenants), never a browser-locale guess. Leaving it empty lists everything on sale. *(source: screens/P01-guest-web-storefront.yaml#WEB-002 (datePicker notes))*

#### Outputs: what the screen shows and produces

**Shown**

**Category tiles** (card list, from `listProductCategories`): Shown when `BookingFlowConfig.ticketCategories` is `categoryThenSubcategory` (the default): the category tiles (name, image) first, then that category's products through `listProducts?categoryId=`. `flatList` skips the tiles. Tiles lay out as a grid or one scrolling row per `BookingFlowConfig.cardLayout` (W7).

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Name | text | — |
| Code | text | Taken from their category tables, 20 September. Ours had a uuid and a localised name, so an importer matching *Beverages* had to match on a … |
| Name localised | grouped details | — |
| Kind | chip: Category, Brand, Collection, Season, Department | — |
| Parent | the name it points at, never the id | One tree, not four. A brand under a department under a category is how a real merchandise hierarchy runs, and separate tables for each … |
| Display order | 1,234 | — |
| Image | the image or video | — |
| Description | in the reader's language | The short line a guest reads under a category option, e.g. *Surf lessons: learn on the beginner wave with a coach* (decided 29 September … |
| Booking flow | the name it points at, never the id | The booking flow for every product filed here that names none of its own (decided 29 September, W12, BO-115). |
| Is active | yes / no (icon or chip) | Deactivated rather than deleted. A category with a season behind it still names the products sold under it, and removing it rewrites last … |
| Children | list or chips (count when long) | Empty on a leaf. |
| ID | the name it points at, never the id | — |
| Name | text | — |
| Code | text | Taken from their category tables, 20 September. Ours had a uuid and a localised name, so an importer matching *Beverages* had to match on a … |
| Name localised | grouped details | — |
| Kind | chip: Category, Brand, Collection, Season, Department | — |
| Parent | the name it points at, never the id | One tree, not four. A brand under a department under a category is how a real merchandise hierarchy runs, and separate tables for each … |
| Display order | 1,234 | — |
| Image | the image or video | — |

**Card list** (card list, from `listProducts`): Cursor pagination. Infinite scroll with an explicit load-more fallback

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Family key | text | The same product at another location (decided 29 September, rev 3 REV3-18). Optional. |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |
| Category | the name it points at, never the id | Taken from their `fnb.product` and `retail.product`, 20 September. `catalogue.product_category` has existed since 20 August with two … |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | — |
| Is sellable | yes / no (icon or chip) | True only when live and carried by a published bundle. Approval and publication are different acts. |
| Is stock tracked | yes / no (icon or chip) | Taken from their `fnb.product`, 20 September. Whether a sale decrements stock, which is not what `isSellable` asks. |
| Has variants | yes / no (icon or chip) | — |
| Variant count | 1,234 | — |
| Segment tags | list or chips (count when long) | 7.3.5. A channel and a segment tag are mandatory and nothing required either. |
| Code schema | text | 7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. `Product.code` existed and nothing required a format, so a venue with three thousand … |

**Help me choose** (banner, from `getPublishedGuidedChoice`): **The answers filter the list** (W4): sent as `guidedAnswerIds` to `listProducts` (and `searchCatalogue`), so web, app and kiosk filter the same way on the server.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | UUIDv7. |
| Venue | the name it points at, never the id | From the path of `createGuidedChoice`. |
| Name | text | Staff-facing name, e.g. "Water park day planner". |
| Mode | chip: Button, Popup on arrival, Off | How the guest reaches it (rev 3 REV3-11). `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on … |
| Show banner | yes / no (icon or chip) | The dark banner under the products ("Choose from the experiences above or let us help you decide") with a Help me choose button. |
| Behaviour | chip: Filter, Recommend | `filter` (default) narrows the list; `recommend` ends on one result card (decided 29 September, W4). |
| Show everything | yes / no (icon or chip) | The "Show everything" link under a filtered list, which clears the answers (W4). |
| Questions | list or chips (count when long) | One to four questions (decided 29 September, W4: the Deep Dive reference asks three or four; rev 3 REV3-11 allowed two). |
| ID | the name it points at, never the id | UUIDv7. The row's own key. |
| Title | in the reader's language | — |
| Kind | chip: Choice, Yes no, Age, Level, Certification | What the question asks (decided 29 September, W4). `choice` free answers; `yesNo` two answers (e.g. |
| Sort order | 1,234 | — |
| Answers | list or chips (count when long) | Two to four answers; the prototype shows three (proposed, client to correct, rev 3 REV3-11). |
| ID | the name it points at, never the id | UUIDv7. The row's own key. |
| Title | in the reader's language | — |
| Body | in the reader's language | The one-liner under the title, at most 140 characters in each language. |
| Icon | text | An icon name from the guest app's icon set. |
| Badge | in the reader's language | Optional, e.g. "Best value". |
| Sort order | 1,234 | — |
| Target | grouped details | Required with `behaviour` `recommend` on the last question; optional with `filter`, where it is the card shown above the filtered list. |

**Contact sales** (card list, from `listProducts`): **View-only products** (W3): Call sales / Email sales from `Product.salesContact` instead of Book.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Family key | text | The same product at another location (decided 29 September, rev 3 REV3-18). Optional. |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |
| Category | the name it points at, never the id | Taken from their `fnb.product` and `retail.product`, 20 September. `catalogue.product_category` has existed since 20 August with two … |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | — |
| Is sellable | yes / no (icon or chip) | True only when live and carried by a published bundle. Approval and publication are different acts. |
| Is stock tracked | yes / no (icon or chip) | Taken from their `fnb.product`, 20 September. Whether a sale decrements stock, which is not what `isSellable` asks. |
| Has variants | yes / no (icon or chip) | — |
| Variant count | 1,234 | — |
| Segment tags | list or chips (count when long) | 7.3.5. A channel and a segment tag are mandatory and nothing required either. |
| Code schema | text | 7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. `Product.code` existed and nothing required a format, so a venue with three thousand … |

**The wait time** (detail panel, from `getWaitTimes`)

| Shows | Format | Notes |
|---|---|---|
| Queue name | in the reader's language | — |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Show everything (secondary button) | `listProducts` GET `/products` | — | Product (paged) | 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 403 Authenticated but not permitted at the requested scope | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **product card**: Own primary photo (or the video poster), name, one-line summary, up to six display tags with icons (e.g. "2 Hours", "Min 1.10 m", "Valid 6 days"), and a "from" price in AED with no decimals when whole (AED 245). A sold-out product stays listed and says Sold out; it is never hidden. *(source: REV3 23SEP-3; REV3 23SEP-4; contracts/spine/catalogue.yaml#searchCatalogue (isAvailable "shown rather than filtered out"))*
- **info-only product card**: Same card, with the notBookableLabel (default "Info only / Not bookable online") where the price and Book would be, and "Contact sales to book" showing Call sales / Email sales from Product.salesContact. Opens the details, never the basket. Hidden entirely when showInfoOnly is off. *(source: REV3-14; DI-1004; MoM 29 Sep W3)*
- **card layout**: Four layouts the venue picks: Stacked rows (default), Split rows, Cards across, Poster cards; sizes Compact (default), Standard, Large, Extra large; density Compact (default), Standard, Roomy. Design all four layouts at Compact; the client liked the compact size. *(source: DI-1040; DI-991; REV3 DG-6)*
- **wait time**: On attraction cards only, when the venue publishes a live wait: "25 min wait" with a clock icon. Omitted (not "0 min") when the queue feed has no reading. *(source: contracts/satellite/queue.yaml#getWaitTimes; TRACKER 30-September Old rows row 60 (A57))*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Book**: Opens WEB-005 as a side panel on the listing (counters for an undated product; for a dated product the panel opens on the date strip, then time, then tickets). Seated events with one on-sale performance go straight to the seat map (WEB-007); a cabana or spot on a venue map goes to WEB-047; a space by the hour to WEB-048. Book never adds to the basket by itself. *(source: REV3 23SEP-5; REV3-2; REV3-4; screens/P01-guest-web-storefront.yaml#WEB-004 transitions)*
- **Read more**: Opens WEB-004 (or its pop-up rendering) with the product's video playing in place. *(source: DI-1026; DI-1101)*
- **Help me choose / Show everything**: Answers filter this list on the server (guidedAnswerIds), so web, app and kiosk show the same products for the same answers. Show everything clears the answers and restores the full list. It is never a consent step. *(source: MoM 29 Sep W4; contracts/spine/catalogue.yaml#searchCatalogue (guidedAnswerIds))*

**Data it reads**: `listProducts` (onLoad, List products); `listPerformances` (onLoad, List performances of an event); `getWaitTimes` (onLoad, Wait times across a venue); `listProductCategories` (onLoad, The category tiles (a tree: parentId, displayOrder, image)); `getPublishedGuidedChoice` (onLoad, Help me choose: the questions whose answers filter this …)

**Where the user goes next**

- → `WEB-004` Attraction Details: *Attraction Details*; carries `eventId`, `productId`
- → `WEB-005` Ticket Type Selection: *Book (the ticket counters open as a side panel on the listing)*; carries `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The event attraction listing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the event attraction listing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No event attraction listing yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the search, category or date picked, and the other events are still there. Names what was picked and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 A `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 September). |

#### Edge cases to draw

- **The answers of Help me choose leave no product**: "Nothing matches your answers" with the answers listed as chips and Show everything; never an empty grid. *(source: screens/P01-guest-web-storefront.yaml#WEB-002 states.emptyNoResults)*
- **A guest arrives on a deep link to an event that has finished or is withdrawn**: The listing opens with a one-line notice ("That event has ended") and the venue's other products; never a 404. *(source: screens/P01-guest-web-storefront.yaml#WEB-002 entryState.coldEntry)*
- **Online allocation is sold out while the gate still has capacity**: The card says Sold out online; this is per-channel allocation and correct behaviour, not a defect. *(source: F01 step 3 (branch "sold out online while counter allocation remains"))*

#### Consistency with other screens

- Match `GST-002`: Same products, same filters and the same Help me choose result for the same answers; the app lays them out in its own Explore structure (mobile flow deliberately differs from web).
- Match `WEB-005`: The side panel is WEB-005; it must look identical whether opened here or on WEB-004.
- Match `KSK-003`: The kiosk filters with the same guidedAnswerIds, so a product hidden here for an answer is hidden there too.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Summit Peaks (theme park), Yas Island; Arabic name قمم القمة
categories:
- Day passes
- Multi-park
- Group and school
- Annual passes
- Fast Track
cards:
- name: Summit Peaks Day Pass
  tags:
  - Min 1.10 m
  - Valid 1 day
  from: AED 245
  badge: Popular
- name: 2 park ticket
  tags:
  - Valid 6 days
  from: AED 475
  summary: Any two Yas-side parks. Second visit within 6 days.
- name: Courses and workshops (info only)
  label: Info only / Not bookable online
  contact: Call sales +971 2 555 0142
- name: Intermediate surf (Coastal Aqua)
  tags:
  - 55 min
  from: AED 345
  waitTime: 25 min wait
```

#### Permissions

- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `listPerformances` → `PRODUCT_VIEW` (read) · staff, guest
- `searchCatalogue` → no permission · guest
- `getWaitTimes` → no permission · guest, public
- `listProductCategories` → `PRODUCT_VIEW` (read) · staff, guest
- `getPublishedGuidedChoice` → no permission · guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

22 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 19.2.34 | Time Slot Reservations - System shall support time slot reservations. | Guest Mobile App & Branding | CONTRACTED | `listPerformances` |
| 2.6.15 | - Time slots for events | Ticketing Sales | CONTRACTED | `listPerformances` |
| 2.7.16 | - Dedicated sales calendar | Ticketing Sales | CONTRACTED | `listPerformances` |
| 1.1.39 | System shall expose APIs for ticket creation, modification, pricing, inventory, reservations, validation and integrations with third-party systems. | Ticketing Catalogue | CONTRACTED | `searchCatalogue` |
| 1.2.73 | System shall expose APIs for resource management. | Ticketing Catalogue | CONTRACTED | `searchCatalogue` |
| 1.5.3 | The system should allow the user to filter the ticket by all types and available properties. For example, dated/non-dated, single-entry/multiple-entry, adult/child, standard/VIP, attraction … | Ticketing Catalogue | CONTRACTED | `searchCatalogue` |
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| … 10 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Category tiles (e.g. Permanent exhibition, Temporary exhibitions, Guided tours, Courses & workshops), then that category's tickets with Adult / Child / Student counters. Setting "Ticket categories": Category → subcategory (default) or Flat list (all tickets under category headings). *(agreed · rev 3 design review 29 Sep 2026, REV3-16 · 16. Choose category, then subcategory, configurable in the CMS · DI-1056)*
- Card layout is a choice, not free text: Stacked rows (default) · Split rows · Cards across · Poster cards. Card size: Compact (default) · Standard · Large · Extra large. Density: Compact (default) · Standard · Roomy. *(agreed · design review 29 Sep 2026, 6. Booking-flow configuration (CMS-016): card-layout options · DI-1040)*
- Clicking a ticket opens the Adult / Child / Senior / Infant counters in a side panel on the same listing or details screen (no separate "Select Tickets" step); the panel is open by default on the listing and Book goes straight into the booking. *(agreed · design review 29 Sep 2026, Tickets 5. Clicking Dated Day Pass should show the tickets on the same screen · DI-1027)*
- Read more opens with the ticket's video or photo, and every ticket in a listing has its own photo (product media: images and videos, one primary). *(agreed · design review 29 Sep 2026, Tickets 4. Video or image should show · DI-1026)*
- CMS option to list a product (e.g. training courses) with full details but no Book button; instead show "Contact sales to book" with contact details. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W3 View-only products · DI-1004)*
- Experience venues list each experience directly (e.g. author talk, calligraphy workshop, story hour, rooftop reading night), each with its own date, time and tickets; no category step. *(client request · rev 3 design review 25 Sep 2026, 12. Experience flow: show the product directly, not the ticket category · DI-999)*
- Show the ticket categories (e.g. Single day, Two-day flexible, UAE resident) directly; no intermediate "Dated day pass" step. *(client request · design review 23 Sep 2026, Tickets 7. Show the ticket category directly instead of Dated Pass -> Single Day Pass · DI-976)*
- Allam's UX benchmark (Little Explorer, Dubai): multi-location selector, a horizontal near-term date picker with full-calendar fallback, and tabbed browsing (passes / workshops / packages) on one page rather than multiple screens. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-585)*
- Products are grouped into categories for the tenant website (e.g. a diving operator's scuba diving, free diving, snorkelling, each listing its packages); package title, description, terms, age limits and images come from back-office fields and sync to the live site; choosing a package goes to checkout on the TICVAI booking platform. *(agreed · MoM 7 Aug 2026, 9. Statistical Groups & Website Content Integration · DI-161)*
- Ticket listings are data-driven: creating a new ticket automatically surfaces it on the relevant site according to its category configuration. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-109)*

Also apply: 1 for P01 · Discovery & Browse, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Card layout (`bookingFlow.cardLayout`) | Stacked rows · Split rows · Cards across · Poster cards | Stacked rows | ticket and product cards: stacked rows, split rows, cards across, or poster cards |
| Card size (`bookingFlow.cardSize`) | Compact · Standard · Large · Extra large | Compact | card size: compact, standard, large, extra large |
| Ticket categories (`bookingFlow.ticketCategories`) | Category then subcategory · Flat list | Category then subcategory | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once. |
| Show info only (`bookingFlow.showInfoOnly`) | — | on | Show info-only products (decided 29 September, rev 3 REV3-14). On, a product with `guestListing` `infoOnly` (catalogue) is listed with its not-bookable label and opens its details; off, guests are not shown it. |
| Venue overrides (`bookingFlow.venueOverrides`) | at most 200; Per-venue overrides, at most one per venue.; A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. | — | Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. |
| Settings: card layout (`bookingFlow.venueOverrides[].settings.cardLayout`) | Stacked rows · Split rows · Cards across · Poster cards | Stacked rows | How ticket and product cards are laid out (decided 29 September, rev 3 DG-6). Was a free string; the four values are the design's Stacked rows, Split rows, Cards across and Poster cards. |
| Settings: card size (`bookingFlow.venueOverrides[].settings.cardSize`) | Compact · Standard · Large · Extra large | Compact | Labels Compact, Standard, Large, Extra large (decided 29 September, rev 3 DG-6). |
| Settings: ticket categories (`bookingFlow.venueOverrides[].settings.ticketCategories`) | Category then subcategory · Flat list | Category then subcategory | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once. |
| Settings: show info only (`bookingFlow.venueOverrides[].settings.showInfoOnly`) | — | on | Show info-only products (decided 29 September, rev 3 REV3-14). On, a product with `guestListing` `infoOnly` (catalogue) is listed with its not-bookable label and opens its details; off, guests are not shown it. |

*Help me choose*, set in `CMS-101` Help Me Choose:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Help me choose name (`guidedChoices.name`) | max length 80 | — | Staff-facing name, e.g. "Water park day planner". |
| Help me choose mode (`guidedChoices.mode`) | Button · Popup on arrival · Off | Button | How the guest reaches it (rev 3 REV3-11). `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on the guest's first arrival at the booking page (whether it was seen is kept on … |
| Show banner (`guidedChoices.showBanner`) | — | on | The dark banner under the products ("Choose from the experiences above or let us help you decide") with a Help me choose button. |
| Help me choose behaviour (`guidedChoices.behaviour`) | Filter · Recommend | Filter | `filter` (default) narrows the list; `recommend` ends on one result card (decided 29 September, W4). |
| Show everything (`guidedChoices.showEverything`) | — | on | The "Show everything" link under a filtered list, which clears the answers (W4). |
| Help me choose questions (`guidedChoices.questions`) | at least 1; at most 4 | — | One to four questions (decided 29 September, W4: the Deep Dive reference asks three or four; rev 3 REV3-11 allowed two). |
| Questions: title (`guidedChoices.questions[].title`) | English and Arabic (Arabic right to left) | — | — |
| Questions: kind (`guidedChoices.questions[].kind`) | Choice · Yes no · Age · Level · Certification | Choice | What the question asks (decided 29 September, W4). `choice` free answers; `yesNo` two answers (e.g. |
| Questions: sort order (`guidedChoices.questions[].sortOrder`) | min 0 | — | — |
| Questions: answers (`guidedChoices.questions[].answers`) | at least 2; at most 4 | — | Two to four answers; the prototype shows three (proposed, client to correct, rev 3 REV3-11). |
| Answers: title (`guidedChoices.questions[].answers[].title`) | English and Arabic (Arabic right to left) | — | — |
| Answers: body (`guidedChoices.questions[].answers[].body`) | The one-liner under the title, at most 140 characters in each language. | — | The one-liner under the title, at most 140 characters in each language. |
| Answers: icon (`guidedChoices.questions[].answers[].icon`) | max length 40 | — | An icon name from the guest app's icon set. |
| Answers: badge (`guidedChoices.questions[].answers[].badge`) | At most 24 characters in each language. | — | Optional, e.g. "Best value". |
| Answers: sort order (`guidedChoices.questions[].answers[].sortOrder`) | min 0 | — | — |

Also set there, as content the tenant writes: answers: target, answers: filter, answers: consent prefill, answers: result.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-002` · status **review** · provenance client-verified
- Prototype (rev 3 (30 September build; the view as verified on the 29 September build, CHG-R1S-015), verified 2026-09-29, match exact): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Header 'What's on'*
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (87 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-002?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Show everything.
- [ ] Every transition is wired: `WEB-004`, `WEB-005`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 10 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-003` Search Results

**Find something when the guest does not know what it is called.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Discovery & Browse · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #28145 (APP-WEB-WEB-003) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `searchCatalogue` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The offline banner shows.** Results come only from what was already loaded, with a note that newer items may exist. |
| Opens with | nothing: it opens on its own |
| Route | `/discovery-and-browse/search-results` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Rev 3 (decided 29 September, rev 3 REV3-14).** `searchCatalogue` now also returns info-only products, flagged (`guestListing` `infoOnly`): the result shows `notBookableLabel` (default *Info only / Not bookable online*) and opens the details (WEB-004), never Add to basket. Hidden when `BookingFlowConfig.showInfoOnly` is off. Each result shows its own primary image (23SEP-4).

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Search for a guest who does not know what a thing is called. Block A. The prototype has no separate results page: results appear as a type-ahead under the search box and Enter lands on the listing (WEB-002) filtered by the query. Design it that way and treat WEB-003 as the type-ahead and the filtered state of WEB-002.

**Fixed on main** (the package already carries these; draw what it says): The layout shows "Venue id" as a text field and raw "Every money" / "Every product" tables. (CHG-GST-003).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search | text field | required | — | min length 2 | — | Sends `?q=` to `searchCatalogue`. | `searchCatalogue` ?q |
| Kind | select | optional | — | Product · Event · Attraction · Bundle · Membership · Merchandise · Menu item | — | Sends `?kind=` to `searchCatalogue`. | `searchCatalogue` ?kind |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |

**Rules for these inputs** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **q**: Starts searching from the 2nd character, debounced; Arabic and English both match (product names may be Arabic-only). Kind is a chip row (All, Events, Attractions, Memberships, Shop, Food), not a free-text field. *(source: contracts/spine/catalogue.yaml#searchCatalogue (q minLength 2, kind); DI-082)*

#### Outputs: what the screen shows and produces

**Shown**

**Results** (card list, from `searchCatalogue`): One card per result: name, summary, photo (`primaryMedia`), from-price (`fromPrice`), sold out shown rather than hidden (`isAvailable`), and `notBookableLabel` for an info-only product. `searchCatalogue` answers with no named schema, so the card binds none. Was the generated table 'Every money'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 …

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | text | — |
| Name | text | — |
| Summary | text | — |
| From price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Guest listing | chip: Bookable, Info only, Hidden | How a product appears to a guest (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to … |
| Not bookable label | in the reader's language | The product's label, for an `infoOnly` result; null otherwise (decided 29 September, rev 3 REV3-14). |
| Primary media | grouped details | The product's `isPrimary` media item, so each result in a listing shows its own photo (decided 29 September, 23SEP-4). |
| Asset | the image or video | A `MediaAsset` of `assets.yaml`, in status `ready`. |
| Kind | chip: Image, Video | — |
| Is primary | yes / no (icon or chip) | The item *Read more* opens on and a listing shows. Exactly one per product. |
| Display order | 1,234 | — |
| Alt text | in the reader's language | — |
| Is available | yes / no (icon or chip) | Shown rather than filtered out. A guest searching for a sold-out attraction should learn it is sold out, not that it does not exist. |

**Suggestions** (card list, from `listProducts`): Before the guest types: what is on sale at the venue. The venue is the one the guest picked on Home (`venueId` from the session, audit R267), never typed. Was the generated table 'Every product'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Media | list or chips (count when long) | The product's own photos and video (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each … |
| Display tags | list or chips (count when long) | Short facts a guest reads on the ticket card and under *Read more*: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates … |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **result row**: Thumbnail (primaryMedia), name, kind, summary, from-price. A sold-out result stays in the list with "Sold out" (isAvailable false); an info-only result shows its not-bookable label and opens the details. *(source: contracts/spine/catalogue.yaml#searchCatalogue)*
- **no results**: Names the query ("No results for 'snorkel'"), offers Clear and the category tiles; when a Help me choose filter is active, says so and offers Show everything. *(source: screens/P01-guest-web-storefront.yaml#WEB-003 states.emptyNoResults)*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Select a result**: Opens WEB-004 for that product; Enter without a selection opens WEB-002 filtered by the query. *(source: screens/P01-guest-web-storefront.yaml#WEB-003 wireframe.prototype.differences)*

**Data it reads**: `listProducts` (onLoad, List products)

**Where the user goes next**

- → `WEB-002` Event & Attraction Listing: *Event & Attraction Listing*; carries `eventId`
- → `WEB-004` Attraction Details: *Attraction Details*; carries `eventId`, `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The search results list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the search results untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No search results yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches what was typed. Names the search, suggests a shorter one and offers to clear it; a sold-out match is shown as sold out, not hidden. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** Results come only from what was already loaded, with a note that newer items may exist. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 A `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 September). |

#### Edge cases to draw

- **Offline or the search call fails**: Results only from what was already loaded, with a note that newer items may exist. *(source: screens/P01-guest-web-storefront.yaml#WEB-003 states.offline)*

#### Consistency with other screens

- Match `GST-063`: Same search, same ranking and the same sold-out and info-only treatment on the app.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
query: surf
results:
- name: Beginner surf
  kind: Attraction
  from: AED 295
- name: Intermediate surf
  kind: Attraction
  from: AED 345
- name: Expert barrels
  kind: Attraction
  from: AED 495
  availability: Sold out
```

#### Permissions

- `searchCatalogue` → no permission · guest
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.39 | System shall expose APIs for ticket creation, modification, pricing, inventory, reservations, validation and integrations with third-party systems. | Ticketing Catalogue | CONTRACTED | `searchCatalogue` |
| 1.2.73 | System shall expose APIs for resource management. | Ticketing Catalogue | CONTRACTED | `searchCatalogue` |
| 1.5.3 | The system should allow the user to filter the ticket by all types and available properties. For example, dated/non-dated, single-entry/multiple-entry, adult/child, standard/VIP, attraction … | Ticketing Catalogue | CONTRACTED | `searchCatalogue` |
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 8.8.1 | A price for a PLU is changing depending on the date of visit. I can sell today a product to be used after a price change at the new price defined in the sales calendar. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.2 | System shall support future-dated pricing schedules. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.3 | System shall support pricing by visit date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.4 | System shall support pricing by booking date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.5 | System shall support pricing calendar management. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.6 | System shall support automatic activation of future pricing. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P01 · Discovery & Browse, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Show info only (`bookingFlow.showInfoOnly`) | — | on | Show info-only products (decided 29 September, rev 3 REV3-14). On, a product with `guestListing` `infoOnly` (catalogue) is listed with its not-bookable label and opens its details; off, guests are not shown it. |
| Settings: show info only (`bookingFlow.venueOverrides[].settings.showInfoOnly`) | — | on | Show info-only products (decided 29 September, rev 3 REV3-14). On, a product with `guestListing` `infoOnly` (catalogue) is listed with its not-bookable label and opens its details; off, guests are not shown it. |

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-003` · status **review** · provenance client-verified
- Prototype (rev 3 (pointer moved to the 30 September build, CHG-R1S-015), verified 2026-09-28, match partial): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Discover → search box in the hero (opens the search panel) → Enter lands on What's on filtered by the query*. Differences: No separate results page: results render as a type-ahead overlay and then in the WEB-002 listing with the query applied. Recent and popular searches are prototype additions not in the YAML.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-003?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `WEB-002`, `WEB-004`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-004` Attraction Details

**Decide whether to book this.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Discovery & Browse · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #28685 (APP-WEB-WEB-004) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listPerformances` reads the population and `getProduct` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `eventId` (WEB-002), `productId` (WEB-001) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/discovery-and-browse/event-attraction-detail` |

**What the spec says about it.** **Renamed 31 August** from *Event / Attraction Detail*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest. **Cross-surface parity, 31 August**: added getAvailability, getWaitTimes. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations. **Rev 3 (decided 29 September).** Ticket tags from `Product.displayTags` when `BookingFlowConfig.ticketTags` is on (23SEP-3); Read more opens on the product's own video or photo (`Product.media`, 23SEP-4). An info-only product shows its `notBookableLabel` and no Book button (REV3-14). **Book** opens the ticket counters as a side panel here (23SEP-5); a dated product goes to the date and time first (WEB-006, REV3-2); a fixture with a single on-sale performance opens straight on the seat map with the fixture as a strip at its top (WEB-007, 23SEP-16, REV3-4); a product placed on a venue map opens the map booking (WEB-047, REV3-15); a product sold by the hour opens the space booking (WEB-048, REV3-13). The event banner lists dates only when `BookingFlowConfig.eventBannerDates` is on (default off, 23SEP-19). Help me choose sits on the booking step (WEB-005), where the prototype draws it, not here (REV3-11). **29 September.** W3: view-only products show Call sales / Email sales instead of Book. M18-13: in single-event mode, a banner or video hero and only the next seven days, with a calendar for later dates (M17-08). **Video plays directly (client meeting 30 …

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** The product page where a guest decides to book. Block A. It is rendered three ways in the prototype (a Read more pop-up per product, the listing's preview aside, and the single-event page behind its setting) and all three must carry the same content. The one thing to get right: the video plays in place with no loader in front of it (client, 30 September).

**Fixed on main** (the package already carries these; draw what it says): The layout puts From/To date pickers and an "Every performance" table on the details page. (CHG-GST-003); The prototype labels this screen WEB-003b. (CHG-SGU-020).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Next 7 days | date picker | — | — | — | — | **Single-event page** (M18-13): banner or video hero, a brief description, and a date strip of the next `dateStripDays` days (default 7) with a calendar icon for later dates (M17-08). | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listPerformances` ?from |
| To | date and time picker | — | — | `listPerformances` ?to |
| Category | picker: choose a category | — | — | `listPerformances` ?categoryId |
| Language | text field | — | max length 35; pattern `^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$` | `listPerformances` ?language |
| Performance | picker: choose a performance | — | — | `getAvailability` ?performanceId |
| Channel capacity | picker: choose a channel capacity | — | — | `getAvailability` ?channelCapacityId |
| Event | picker: choose an event | — | — | `getAvailability` ?eventId |
| From | date and time picker | — | — | `getAvailability` ?from |
| To | date and time picker | — | Exclusive; at most 31 days after `from`. | `getAvailability` ?to |
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |

**Rules for these inputs** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **date strip (single-event page only)**: The next dateStripDays days (default 7, venue range 3 to 31) as a strip with a calendar icon for later dates; sold-out days disabled with the reason on hover, not hidden. The event banner lists dates only when eventBannerDates is on (default off). *(source: DI-920; M17-08; REV3 23SEP-19)*

#### Outputs: what the screen shows and produces

**Shown**

**Availability** (data table, from `getAvailability`): From `getAvailability`, now a `PerformanceAvailabilityPage` (a Page of `PerformanceAvailability`, each with `startsAt`): `channelCapacityId`, `performanceId`, `startsAt`, `capacity`, `sold`, `leased`, `remaining`, `byChannel`. The time grid calls it once with `eventId`, `from` and `to` for every performance in the window (decided 29 September, rev 3 REV3-1), not once per tile.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Channel capacity | the name it points at, never the id | — |
| Performance | the name it points at, never the id | The performance this channel capacity belongs to (`ChannelCapacity.performanceId`), so rows for several performances can be told apart. |
| Starts at | 1 Oct 2026, 14:30 | The performance's start, so a time tile and its day part (morning, afternoon, evening, split at the venue's … |
| Capacity | 1,234 | — |
| Sold | 1,234 | — |
| Leased | 1,234 | Held by terminals but not yet sold. |
| Remaining | 1,234 | — |
| By channel | list or chips (count when long) | Per-channel position. A guest seeing sold out online while units remain at the counter is correct behaviour, not a defect. |
| Channel | chip: POS, Kiosk, Web, Mobile, B2B, Ota… | — |
| Allocated | 1,234 | — |
| Sold | 1,234 | — |
| Remaining | 1,234 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Banner** (banner): Shown only when withdrawn — reachable via a stale link but no longer sellable. A silent 404 on a shared link is a bad guest experience

**Ticket tags** (card list, from `getProduct`): Up to six tags (clock, height, free, calendar, id) with an icon by kind, e.g. *2 Hours*, *Min 1.10 m*, *Valid 90 days*. Where the product has none, derived on read from duration, validity and the height rule. Shown only when `BookingFlowConfig.ticketTags` is on (default on).

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Family key | text | The same product at another location (decided 29 September, rev 3 REV3-18). Optional. |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |
| Category | the name it points at, never the id | Taken from their `fnb.product` and `retail.product`, 20 September. `catalogue.product_category` has existed since 20 August with two … |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | — |
| Is sellable | yes / no (icon or chip) | True only when live and carried by a published bundle. Approval and publication are different acts. |
| Is stock tracked | yes / no (icon or chip) | Taken from their `fnb.product`, 20 September. Whether a sale decrements stock, which is not what `isSellable` asks. |
| Has variants | yes / no (icon or chip) | — |
| Variant count | 1,234 | — |
| Segment tags | list or chips (count when long) | 7.3.5. A channel and a segment tag are mandatory and nothing required either. |
| Code schema | text | 7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. `Product.code` existed and nothing required a format, so a venue with three thousand … |
| Channels | list or chips (count when long) | — |

**Photo and video** (detail panel, from `getProduct`): **The video plays directly, with no loader in front of it** (client meeting 30 September, MoM 4.8): the info button reveals the details and starts the primary video in place; the poster frame (the primary image, or the video's first frame) shows while it buffers, never a spinner or loading screen. Read more opens on the primary video or photo (`Product.media`, `isPrimary`).

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Family key | text | The same product at another location (decided 29 September, rev 3 REV3-18). Optional. |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |
| Category | the name it points at, never the id | Taken from their `fnb.product` and `retail.product`, 20 September. `catalogue.product_category` has existed since 20 August with two … |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | — |
| Is sellable | yes / no (icon or chip) | True only when live and carried by a published bundle. Approval and publication are different acts. |
| Is stock tracked | yes / no (icon or chip) | Taken from their `fnb.product`, 20 September. Whether a sale decrements stock, which is not what `isSellable` asks. |
| Has variants | yes / no (icon or chip) | — |
| Variant count | 1,234 | — |
| Segment tags | list or chips (count when long) | 7.3.5. A channel and a segment tag are mandatory and nothing required either. |
| Code schema | text | 7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. `Product.code` existed and nothing required a format, so a venue with three thousand … |
| Channels | list or chips (count when long) | — |

**The selected performance** (detail panel, from `listPerformances`)

| Shows | Format | Notes |
|---|---|---|
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Status | chip: Scheduled, On sale, Sold out, Suspended, Cancelled, Completed | — |

**The product eligibility rule** (detail panel, from `getProductEligibilityRule`)

| Shows | Format | Notes |
|---|---|---|
| Product | text | — |
| Min age years | 1,234 | — |
| Max age years | 1,234 | — |
| Min height cm | 1,234 | — |
| Max height cm | 1,234 | — |
| Height bands cm | list or chips (count when long) | Band edges the guest chooses between, e.g. under 1.20 m, 1.20–1.40 m, 1.40 m and over. |
| Accompanied below age | 1,234 | Under this age an adult must be present, e.g. 8 at the kids club. |
| Guardian signature age from | 1,234 | — |
| Guardian signature age to | 1,234 | Ages needing a guardian's signature, e.g. 12–15 on a thrill ride. |
| Waiver required | yes / no (icon or chip) | — |
| Swim ability | chip: Not required, Confident | Superseded for the guest's answer (decided 29 September, rev 3 REV3-26): the swim question is a consent, not a data field. |
| Refundable if ineligible at gate | yes / no (icon or chip) | — |

**The wait time** (detail panel, from `getWaitTimes`)

| Shows | Format | Notes |
|---|---|---|
| Queue name | in the reader's language | — |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

**The product** (detail panel, from `getProduct`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Call sales / Email sales (secondary button) | `getProduct` GET `/products/{productId}` | — | Product | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Select tickets (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **media**: Primary video (6 to 12 s mp4, no audio) or photo at the top. The poster frame (primary image, else the video's first frame) fills the area while it buffers; playback starts in place. No spinner, no overlay, no "loading" screen, and a video that cannot play just leaves the poster. The info button reveals the details and starts the video. *(source: DI-1101; MoM 30 Sep 4.8; TRACKER 30-September Tracker row 13 (S9); DI-1080)*
- **tags and eligibility**: Up to six display tags with kind icons (clock, height, free, calendar, id). Height and age limits from the eligibility rule are shown as tags ("Min 1.10 m", "Ages 3+"), not as a separate rules table. *(source: REV3 23SEP-3; screens/P01-guest-web-storefront.yaml#WEB-004 wireframe.prototype.differences)*
- **availability hint**: For a dated product, the next available date and "11 left" style scarcity only when remaining is low; per-channel remaining, never the venue total. *(source: DI-026; F01 step 3)*
- **withdrawn product**: A banner "This is no longer on sale" with the product kept readable and a link to similar products; Book is absent, not disabled. *(source: screens/P01-guest-web-storefront.yaml#WEB-004 (banner bound to Product.lifecycleState))*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Book**: Routes by product type: undated → counters side panel (WEB-005); dated → date, then time, then tickets (WEB-006 then WEB-005); seated with one on-sale performance → seat map (WEB-007); map-placed spot (cabana) → WEB-047; space by the hour → WEB-048; info-only → no Book, Contact sales instead. *(source: screens/P01-guest-web-storefront.yaml#WEB-004 transitions; DI-948; REV3-4; MoM 29 Sep W3)*
- **Call sales / Email sales**: Phone and email links (tel and mailto) from Product.salesContact, falling back to the venue contact. *(source: MoM 29 Sep W3; DI-1004)*

**Data it reads**: `getProductEligibilityRule` (onLoad, Age and height limits); `getProduct` (onLoad, Read a product); `listPerformances` (onLoad, List performances of an event); `getAvailability` (onLoad, Live remaining capacity); `getWaitTimes` (onLoad, Wait times across a venue)

**Where the user goes next**

- → `WEB-002` Event & Attraction Listing: *Event & Attraction Listing*; carries `eventId`
- → `WEB-005` Ticket Type Selection: *Chooses ticket types and quantities*; carries `productId`
- → `WEB-006` Date & Performance Selection: *Book (a dated product: date first, then time, then tickets)*; carries `productId`
- → `WEB-007` Interactive Seat Selection: *Book (a fixture with one on-sale performance opens straight on the seat map)*; carries `performanceId`
- → `WEB-047` Map Booking — Cabanas & Spots: *Book (a cabana, lounger or other spot placed on the venue map)*; carries `productId`
- → `WEB-048` Book a Space by the Hour: *Book (a space sold by the hour, e.g. a meeting room)*; carries `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | **The video is not part of loading** (client meeting 30 September, MoM 4.8): the attraction renders as it arrives and no loader or loading screen is ever drawn over the video. |
| Video buffering (`?state=videoBuffering`) | **Poster frame, not a loader** (client meeting 30 September, MoM 4.8): until the first frames arrive the poster (primary image, else the video's first frame) fills the video area and playback starts in place as soon as it can; no spinner, overlay or blocking screen. The details beside it stay usable throughout. |
| Video unavailable (`?state=videoUnavailable`) | The video cannot play (no video, a failed stream, data saver on). The poster stays and the details are unaffected; no error screen and no loader. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attraction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attraction yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | No performance in the next days shown; the strip says so and offers the calendar. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **The video cannot play (no video, failed stream, data saver)**: The poster stays, details unaffected; no error message in the media area. *(source: screens/P01-guest-web-storefront.yaml#WEB-004 states.videoUnavailable)*
- **The product is not sellable today (sold out online, outside the sales window)**: Book stays visible but disabled with the stated reason ("Online sales close 15 minutes before the show"; "Sold out online for today, tomorrow has space"). *(source: DI-583; screens/P01-guest-web-storefront.yaml#WEB-004 actionBar (Disabled with a stated reason))*

#### Consistency with other screens

- Match `GST-004`: Same content and the same no-loader video behaviour. The app adds the item's map location and the proposed product (e.g. "Buy meal combo" which brings its admission); the web page may show the map pin when the product has a venue-map location.
- Match `GST-006`: Event and exhibition details on the app follow this page's single-event rules (date strip, banner dates off).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
product: Summit Peaks Day Pass
media: Ride clip "The Drop" 10 s, poster frame the tower at sunset
tags:
- Min 1.10 m
- Valid 1 day
- Free under 3
prices: Adult AED 325, Child (3-12) AED 250, Senior (60+) AED 250, Infant (under 3) free
description: Full-day entry to every ride and show at Summit Peaks. Fast Track sold as an add-on.
```

#### Permissions

- `getProductEligibilityRule` → `PRODUCT_VIEW` (read) · staff, guest
- `getProduct` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `listPerformances` → `PRODUCT_VIEW` (read) · staff, guest
- `getAvailability` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `getWaitTimes` → no permission · guest, public

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

24 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.34 | Time Slot Reservations - System shall support time slot reservations. | Guest Mobile App & Branding | CONTRACTED | `listPerformances` |
| 2.6.15 | - Time slots for events | Ticketing Sales | CONTRACTED | `listPerformances` |
| 2.7.16 | - Dedicated sales calendar | Ticketing Sales | CONTRACTED | `listPerformances` |
| 1.2.74 | System shall support event-driven integrations. | Ticketing Catalogue | CONTRACTED | `getAvailability` |
| 2.1.4 | The system should ensure full integration of all internal sales channels. All associated information (capacity, sales, etc.) must be available to multiple operators simultaneously in real-time. | Ticketing Sales | CONTRACTED | `getAvailability` |
| 2.6.10 | - Event capacity updated in real-time | Ticketing Sales | CONTRACTED | `getAvailability` |
| 2.6.14 | - Remaining quantities | Ticketing Sales | CONTRACTED | `getAvailability` |
| 2.7.14 | - Capacity management in real time is expected | Ticketing Sales | CONTRACTED | `getAvailability` |
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| … 12 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Qossai: ride/attraction detail pages play the video directly, with no loading screen in front of it; an info button reveals ride details and plays the video. Chinmay agreed to remove the loader. *(agreed · MoM 30 Sep 2026, 4.8 Mobile App — In-Ride Video/Info & In-Park Navigation · DI-1101)*
- The date list in the event banner (for multi-date events) is a setting, "Dates in event banner", off by default. The date picker always sits at the top of the booking step. *(agreed · design review 29 Sep 2026, Settings 19. Why is there a date selection in the header? · DI-1033)*
- Clicking a ticket opens the Adult / Child / Senior / Infant counters in a side panel on the same listing or details screen (no separate "Select Tickets" step); the panel is open by default on the listing and Book goes straight into the booking. *(agreed · design review 29 Sep 2026, Tickets 5. Clicking Dated Day Pass should show the tickets on the same screen · DI-1027)*
- Read more opens with the ticket's video or photo, and every ticket in a listing has its own photo (product media: images and videos, one primary). *(agreed · design review 29 Sep 2026, Tickets 4. Video or image should show · DI-1026)*
- Ticket cards, Read more and the listing side panel show tags (e.g. "2 Hours", "Min 1.10 m", "Free adult entry", "Valid 90 days", "Emirates ID"), each with a kind icon (clock, height, free, calendar, id), max 6. Venue-set tags win, else derived from duration, validity, height rule. Setting "Tags on tickets", default on. *(agreed · design review 29 Sep 2026, Tickets 3. 'Read more' should carry tags customisable per ticket type · DI-1025)*
- CMS option to list a product (e.g. training courses) with full details but no Book button; instead show "Contact sales to book" with contact details. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W3 View-only products · DI-1004)*
- Show the ticket categories (e.g. Single day, Two-day flexible, UAE resident) directly; no intermediate "Dated day pass" step. *(client request · design review 23 Sep 2026, Tickets 7. Show the ticket category directly instead of Dated Pass -> Single Day Pass · DI-976)*
- Single-event mode page: banner or video hero, a brief description, and a date strip of the next seven days with a calendar for later dates. *(agreed · MoM 18 Sep 2026, M18-13 · DI-953)*
- A venue selling a single event gets a dedicated page with a banner/video and brief description, showing only the near-term available dates (e.g. next 7 days) by default. *(client request · MoM 18 Sep 2026, 4.13 Guest Website UX Review — Ticket Type Flows & Seat Map Selection · DI-949)*
- Guest date picking shows a strip of the next seven days (venue setting dateStripDays, default 7, range 3-31) with a calendar icon that opens the full month for later dates. *(agreed · MoM 17 Sep 2026, M17-08 · DI-920)*
- Qossai and Allam: product pages should include short video content (e.g. a 10-15 second clip), not only static images, to give a sense of the actual experience (e.g. a ride) before booking. *(agreed · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-917)*
- Allam (ref. "Little Explorer"): show only a short near-term availability window by default (e.g. next 7 days) with a calendar icon that expands to a full calendar for later dates, instead of the flat 15-day range shown. *(agreed · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-915)*
- Six Flags reference for the B2C redesign (Qossai): hero-banner product video. *(client request · MoM 8 Sep 2026, 4.20 Planning & Next Steps · DI-738)*
- Allam's UX benchmark (Little Explorer, Dubai): multi-location selector, a horizontal near-term date picker with full-calendar fallback, and tabbed browsing (passes / workshops / packages) on one page rather than multiple screens. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-585)*
- Product cards/pages carry short descriptions with an expandable "view more details" control and a configurable hero image or video per product. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-425)*
- Platinum List reference: event page with short video + image + description → select tickets → calendar collapsed to a week view, expandable to full month → time-slot selection. *(client request · MoM 21 Aug 2026, 4.1 Reference Walkthrough — Platinum List Seat Selection & Checkout Journey · DI-408)*
- Products are grouped into categories for the tenant website (e.g. a diving operator's scuba diving, free diving, snorkelling, each listing its packages); package title, description, terms, age limits and images come from back-office fields and sync to the live site; choosing a package goes to checkout on the TICVAI booking platform. *(agreed · MoM 7 Aug 2026, 9. Statistical Groups & Website Content Integration · DI-161)*

Also apply: 1 for P01 · Discovery & Browse, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Event banner dates (`bookingFlow.eventBannerDates`) | — | off | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |
| Ticket tags (`bookingFlow.ticketTags`) | — | on | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on its card. |
| Date strip days (`bookingFlow.dateStripDays`) | min 3; max 31 | 7 | The date strip (decided 17 September, M17-08). How many days from today the date step shows as a strip before the calendar icon that opens the full month; later dates are picked from the calendar. |
| Settings: event banner dates (`bookingFlow.venueOverrides[].settings.eventBannerDates`) | — | off | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |
| Settings: ticket tags (`bookingFlow.venueOverrides[].settings.ticketTags`) | — | on | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on its card. |
| Settings: date strip days (`bookingFlow.venueOverrides[].settings.dateStripDays`) | min 3; max 31 | 7 | The date strip (decided 17 September, M17-08). How many days from today the date step shows as a strip before the calendar icon that opens the full month; later dates are picked from the calendar. |

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-004` · status **review** · provenance client-verified
- Prototype (rev 3 (30 September build; the view as verified on the 29 September build, CHG-R1S-015), verified 2026-09-29, match partial): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Config → Marketing layer → 'Single-event page' on, then Book; or any product card → 'Read more' dialog; or a listing card's preview aside*. Differences: No standing attraction-detail page in the default flow: details are a banner above the booking step (behind a Config toggle), a pop-up per product, or the listing preview. Eligibility rule display (getProductEligibilityRule) appears only as tags. Prototype labels it WEB-003b, not WEB-004. **Handoff: the screen id is WEB-004**; the prototype's "WEB-003b" label is not an id (CHG-SGU-020).
- Flow F01 *Guest buys a ticket online*, step 2: Opens a product and decides → Understands what is included and roughly when it is available
- Flow F01 branch at step 2 (recoverable): when The product's published booking flow orders the steps differently (e.g. a workshop is chosen before the date, or a …, Steps 3 and 4 follow the published flow (`getPublishedBookingFlow`, W12): a product-first flow (workshop, experience) picks the product on WEB-005 and then the date and time on WEB-006 (W8); surf …
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (81 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-004?state=<state>`: loading, videoBuffering, videoUnavailable, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Call sales / Email sales, Select tickets.
- [ ] Every transition is wired: `WEB-002`, `WEB-005`, `WEB-006`, `WEB-007`, `WEB-047`, `WEB-048`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 17 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-050` Plan Your Visit

**Plan a visit on the website: answer six questions, get a day-by-day plan, edit it, and book it in one go.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Discovery & Browse · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #28200 (APP-WEB-WEB-050) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | multiStepForm (compact density): The Visit Planner prototype: six questions, then the plan with Book this plan |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `venueId` (session), `planId` (deepLink), `itemId` (navigation) · cold entry: Starts at the first question; a saved-plan link opens the plan, or says it has passed and offers to plan again. `itemId` is the plan item the guest taps Swap … |
| Route | `/plan-your-visit` |

**What the spec says about it.** **Added 29 September**: the 29 September web build has *Plan your visit* in the header, opening the planner full screen, and *Book this plan* goes straight into booking. The web twin of the Plan tab (GST-051 questions, GST-053 plan), binding the same planner operations (venue-map `generateVisitPlan`, `getVisitPlan`, `updateVisitPlan`, `listVisitPlanAlternatives`, `bookVisitPlan`). Block A (29 September re-plan, superseding R187 and GAP-C3). Rules-based; the AI planner chat is app-only for now. Hidden when the venue turns module `visitPlanner` off. **Multi-venue intelligence (client meeting 30 September, MoM 4.7, Allam).** As on the app: each day is at one park and uses only that park's rides, dining and retail (shops and kiosks, added beside F&B); a preference the park cannot meet is said, never filled from another park.

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Plan a visit on the website: six short questions, a day-by-day plan to edit, and Book this plan. Block A. Opened from "Plan your visit" in the header, full screen. Since 30 September the planner is per venue: in a multi-park tenant each day is at one park and uses only that park's rides, dining and shops; a preference a park cannot meet is said, never filled from another park.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The Visit Planner prototype is single-park (no park-per-day step, no shops, no preferenceNotAtVenue). (CHG-SGU-026)

**Fixed on main** (the package already carries these; draw what it says): The 29 September MoM names pace as packed or relaxed; the 30 September MoM as packed, balanced or relaxed. (CHG-SGU-020).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Adults and children | number field | — | — | — | — | Adults 1-8 (12+), children 0-8 (3-11). | — |
| How tall are the children? | select field | — | — | — | — | Per child; rides over the limit are left out (`ProductEligibilityRule`). | — |
| Which days are you visiting? | multi select | — | — | — | — | Up to three. | — |
| Which park each day? | repeatable rows | optional | — | at most 200 | — | **Only in a multi-venue tenant**; hidden otherwise. One choice per chosen day, defaulting to the venue picked in the header; sent as `VisitPlanRequest.dayVenues`. Each day is then planned from that … | `TenantAppStatus.venues` |
| How busy should each day be? | select field | — | — | — | — | Packed, Balanced or Relaxed. | — |
| What are you most interested in? | multi select | — | — | — | — | Interest tags of the venue. | — |
| Any shops you'd like to visit? | multi select | — | — | — | — | Shown when Shopping is chosen (client meeting 30 September, MoM 4.7: retail and kiosk shops join F&B in the planner). The `retailTags` of the chosen parks' shops and retail kiosks; sent as … | — |
| What would you like for lunch? | select field | — | — | — | — | Cuisines of the chosen parks' dining points only (restaurants, cafes, food kiosks; client meeting 30 September, MoM 4.7). In a multi-venue plan each cuisine names the park(s) that serve it, and lunch … | — |
| Add Fast Track | toggle | — | — | — | — | Per guest, with the queuing time saved. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |
| Version | number field | — | min 1 | `getVisitPlan` ?version |

**Sent by *Make my plan*** (`generateVisitPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. | `generateVisitPlan` body |
| Day venues `dayVenues` | repeatable rows | optional | — | at most 7; One entry per date that is not at `venueId`; each date of `dates` at most once. | — | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). | `generateVisitPlan` body |
| Date `dayVenues[].date` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `generateVisitPlan` body |
| Venue `dayVenues[].venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `generateVisitPlan` body |
| Dates `dates` | list of values (chips) | required | — | at least 1; at most 7 | — | — | `generateVisitPlan` body |
| Party `party` | repeatable rows | required | — | at least 1; at most 20 | — | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the fallback the rule may also state. | `generateVisitPlan` body |
| Height cm `party[].heightCm` | number field | optional | — | min 40; max 230 | — | — | `generateVisitPlan` body |
| Age years `party[].ageYears` | number field | optional | — | min 0; max 120 | — | — | `generateVisitPlan` body |
| Pace `pace` | segmented control | optional | Relaxed | Packed · Relaxed | — | — | `generateVisitPlan` body |
| Interest tags `interestTags` | list of values (chips) | optional | — | at most 12 | — | The same closed list as `VenuePoint.interestTags`. | `generateVisitPlan` body |
| Cuisine tags `cuisineTags` | list of values (chips) | optional | — | at most 8 | — | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). | `generateVisitPlan` body |
| Retail tags `retailTags` | list of values (chips) | optional | — | at most 8 | — | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options), e.g. | `generateVisitPlan` body |
| Must include points `mustIncludePointIds` | multi-picker: choose must include points | optional | — | at most 10 | — | Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never placed on another venue's day. | `generateVisitPlan` body |
| Preset `preset` | select | optional | — | Highlights · Family · Thrill seeker · Water day · Relaxed · Shows and dining | — | A ready-made day plan (GST-052 Suggested Itineraries): the preset fixes the interests and the pace, and the party still decides eligibility. | `generateVisitPlan` body |
| Preset key `presetKey` | text field | optional | — | max length 64; pattern `^[a-z][a-zA-Z0-9]*$`; An unknown key is refused 422 `unknown-preset`. | — | The ready-made plan the guest took on GST-052 (30 September, second wave of the 29 September pass, MOB-6): one of the built-in `preset` keys above, or a key of a ready-made plan … | `generateVisitPlan` body |
| Start time `startTime` | time picker | optional | — | — | HH:mm, 24-hour | When the party arrives. Null means opening time. | `generateVisitPlan` body |
| Locale `locale` | text field | optional | — | — | — | — | `generateVisitPlan` body |

**Sent by *Remove / Undo changes*** (`updateVisitPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Base version `baseVersion` | number field | required | — | min 1 | — | — | `updateVisitPlan` body |
| Changes `changes` | repeatable rows | required | — | at least 1; at most 20 | — | — | `updateVisitPlan` body |
| Op `changes[].op` | select | required | — | Swap · Remove · Add · Move · PIN · Accept add on · Decline add on · Add add on · Remove add on · Revert to | — | — | `updateVisitPlan` body |
| Item `changes[].itemId` | picker: choose an item | optional | — | — | shows names, sends the id | — | `updateVisitPlan` body |
| Date `changes[].date` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateVisitPlan` body |
| Point `changes[].pointId` | picker: choose a point | optional | — | — | shows names, sends the id | — | `updateVisitPlan` body |
| Performance `changes[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `updateVisitPlan` body |
| Starts at `changes[].startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateVisitPlan` body |
| Add on product `changes[].addOnProductId` | picker: choose an add on product | optional | — | — | shows names, sends the id | For `addAddOn` and `removeAddOn` (CHG-RUL-009): the add-on product (a catalogue product sold for the item's stop, e.g. | `updateVisitPlan` body |
| Version `changes[].version` | number field | optional | — | — | — | For `revertTo`, the earlier version to restore (undo). | `updateVisitPlan` body |

**Sent by *Book this plan*** (`bookVisitPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Base version `baseVersion` | number field | required | — | min 1 | — | The version the guest is looking at. | `bookVisitPlan` body |
| Cart `cartId` | picker: choose a cart | optional | — | — | shows names, sends the id | The guest's open cart. Null creates one. | `bookVisitPlan` body |
| Items `itemIds` | multi-picker: choose items | optional | — | — | — | Only these items. Empty books every bookable item of every day. | `bookVisitPlan` body |
| Include add ons `includeAddOns` | toggle | optional | on | — | — | Also add the add-ons the guest accepted on the plan (`VisitPlanItem.addOnAccepted`). | `bookVisitPlan` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **who**: Adults 1-8 (12+), children 0-8 (3-11). *(source: screens/P01-guest-web-storefront.yaml#WEB-050 (Adults and children))*
- **heights**: Per child, as height bands; skipped when there are no children. Rides above a child's band are left out. *(source: screens/P01-guest-web-storefront.yaml#WEB-050 progress notes)*
- **days and park per day**: Up to three days. "Which park each day?" only in a multi-venue tenant, one choice per day, defaulting to the venue picked in the header. *(source: DI-1112)*
- **pace**: Packed, Balanced or Relaxed. *(source: DI-1098)*
- **interests and shops**: The venue's interest tags; "Any shops you'd like to visit?" appears when Shopping is chosen, from the chosen parks' shops and kiosks. *(source: DI-1100; screens/P01-guest-web-storefront.yaml#WEB-050 (multiSelect shops))*
- **lunch**: Cuisines of the chosen parks' restaurants, cafes and food kiosks only; in a multi-park plan each names its parks ("Indian · Summit Peaks only"). A preference no chosen park offers is marked "Not at the parks you chose" before Make my plan. *(source: DI-1113; screens/P01-guest-web-storefront.yaml#WEB-050 states.preferenceNotAtVenue)*

#### Outputs: what the screen shows and produces

**Shown**

**Plan your visit · n of 6** (progress indicator): Who, heights (skipped with no children), days (up to 3), pace (packed, balanced or relaxed; DI-1098), interests, lunch.

**Your plan** (timeline, from `getVisitPlan`): Day tabs, each naming its park (`VisitPlan.days[].venueId`); arrival, timed items, lunch and shop or kiosk stops, every one at that day's park (`VisitPlanItem.venueId`; client meeting 30 September, MoM 4.7).

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Subject | the name it points at, never the id | The signed-in guest. From the session, never from the body. |
| Session ref | text | The anonymous device session that owns the plan until sign-in. |
| Ownership | chip: Anonymous, Account | `anonymous` while the plan belongs to a device session (built and changed only; it lapses with the session), `account` once the guest … |
| Status | chip: Draft, Booked, Archived | `booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date. |
| Source | chip: Rules, Preset, AI agent | What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. |
| Inputs | grouped details | What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050. |
| Venue | the name it points at, never the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. |
| Day venues | list or chips (count when long) | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). |
| Date | 1 Oct 2026 | — |
| Venue | the name it points at, never the id | — |
| Dates | list or chips (count when long) | — |
| Party | list or chips (count when long) | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the … |
| Height cm | 1,234 | — |
| Age years | 1,234 | — |
| Pace | chip: Packed, Relaxed | — |
| Interest tags | list or chips (count when long) | The same closed list as `VenuePoint.interestTags`. |
| Cuisine tags | list or chips (count when long) | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). |
| Retail tags | list or chips (count when long) | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner … |

**Not at this park** (banner, from `getVisitPlan`): Per day, a cuisine or shop the day's park cannot offer, and the park that can (from `availableAtVenueIds`), e.g. *No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2).* Hidden when every preference is met (client meeting 30 September, MoM 4.7).

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Subject | the name it points at, never the id | The signed-in guest. From the session, never from the body. |
| Session ref | text | The anonymous device session that owns the plan until sign-in. |
| Ownership | chip: Anonymous, Account | `anonymous` while the plan belongs to a device session (built and changed only; it lapses with the session), `account` once the guest … |
| Status | chip: Draft, Booked, Archived | `booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date. |
| Source | chip: Rules, Preset, AI agent | What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. |
| Inputs | grouped details | What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050. |
| Venue | the name it points at, never the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. |
| Day venues | list or chips (count when long) | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). |
| Date | 1 Oct 2026 | — |
| Venue | the name it points at, never the id | — |
| Dates | list or chips (count when long) | — |
| Party | list or chips (count when long) | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the … |
| Height cm | 1,234 | — |
| Age years | 1,234 | — |
| Pace | chip: Packed, Relaxed | — |
| Interest tags | list or chips (count when long) | The same closed list as `VenuePoint.interestTags`. |
| Cuisine tags | list or chips (count when long) | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). |
| Retail tags | list or chips (count when long) | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner … |

**Estimated total** (detail panel, from `getVisitPlan`): Estimate for the group; confirmed in booking.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Subject | the name it points at, never the id | The signed-in guest. From the session, never from the body. |
| Session ref | text | The anonymous device session that owns the plan until sign-in. |
| Ownership | chip: Anonymous, Account | `anonymous` while the plan belongs to a device session (built and changed only; it lapses with the session), `account` once the guest … |
| Status | chip: Draft, Booked, Archived | `booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date. |
| Source | chip: Rules, Preset, AI agent | What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. |
| Inputs | grouped details | What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050. |
| Venue | the name it points at, never the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. |
| Day venues | list or chips (count when long) | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). |
| Date | 1 Oct 2026 | — |
| Venue | the name it points at, never the id | — |
| Dates | list or chips (count when long) | — |
| Party | list or chips (count when long) | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the … |
| Height cm | 1,234 | — |
| Age years | 1,234 | — |
| Pace | chip: Packed, Relaxed | — |
| Interest tags | list or chips (count when long) | The same closed list as `VenuePoint.interestTags`. |
| Cuisine tags | list or chips (count when long) | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). |
| Retail tags | list or chips (count when long) | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Make my plan (primary button) | `generateVisitPlan` POST `/visit-plans` | VisitPlanRequest | VisitPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A venue of the plan (`venueId` or a `dayVenues` venue) has no published map, or none of its points carries a … | — |
| Swap / + Add something (secondary button) | `listVisitPlanAlternatives` GET `/visit-plans/{planId}/items/{itemId}/alternatives` | — | VisitPlanAlternative (paged) | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Remove / Undo changes (secondary button) | `updateVisitPlan` PUT `/visit-plans/{planId}` | VisitPlanUpdate | VisitPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `baseVersion` is not the current version (`plan-version-conflict`), or the plan is already `booked` … | — |
| Book this plan (primary button) | `bookVisitPlan` POST `/visit-plans/{planId}/booking` | inline | VisitPlanBooking | 403 The caller is an anonymous device session (`sign-in-required`; CHG-RUL-003). Booking is for a signed-in guest; the plan moves to the account on sign-in.; 404 The resource does not exist, or is outside the caller's … | — |
| Change answers (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **plan**: Day tabs naming their park; arrival, timed rides and shows, lunch and shop stops in time order with walking time between; Fast Track per guest with the queuing time saved; the estimated total for the group, labelled an estimate. *(source: DI-1098; DI-1112; screens/P01-guest-web-storefront.yaml#WEB-050 review)*
- **Not at this park banner**: "No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2)." Per day, hidden when every preference is met. *(source: DI-1113)*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Swap / Add something / Remove / Undo**: Swap candidates suit everyone in the group and come from that day's park only; each change is a new version so Undo goes back one. *(source: screens/P01-guest-web-storefront.yaml#WEB-050 review)*
- **Book this plan**: Turns the plan and chosen add-ons into basket lines and opens the basket (WEB-010); tickets, Fast Track and meal combos in one checkout. *(source: contracts/satellite/venue-map.yaml#bookVisitPlan; STATUS-29SEP (Visit planner on web))*

**Data it reads**: `listProducts` (onLoad, Interests and height limits of what the planner may include); `getVisitPlan` (onLoad, The plan: days, timed items and add-on suggestions, at its …); `getTenantAppStatus` (onLoad, The tenant's active venues, for the park-per-day choice in …)

**Where the user goes next**

- → `WEB-010` Shopping Cart: *Book this plan*; carries `cartId`; calls `bookVisitPlan`
- → `WEB-004` Attraction Details: *Opens an item on the plan*; carries `productId`
- → `WEB-001` Home / Landing: *Back to tickets*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The plan builds in place; the answers stay on screen. |
| Error (`?state=error`) | Could not build or load the plan. Names what failed; the answers are kept. |
| Empty, first run (`?state=emptyFirstRun`) | No plan yet: the first question is shown. |
| Empty, no results (`?state=emptyNoResults`) | Nothing suits the whole group on that day: says which answer ruled everything out and offers to change it. |
| Preference not at venue (`?state=preferenceNotAtVenue`) | **A preference a day's park cannot meet** (client meeting 30 September, MoM 4.7): before *Make my plan* the chip is marked *Not at the parks you chose* (naming a park of the tenant that has it); after it, the day shows the *Not at this park* banner and nothing from another park is placed. *Change answers* lets the guest move that day to the park that has it. |
| Permission denied (`?state=emptyNoAccess`) | A guest holds no permission. Anyone can build a plan; signing in is asked only to save it, and booking follows the cart's own sign-in gate. |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 409 `baseVersion` is not current (`plan-version-conflict`), or the cart is not the caller's or is no longer open (`cart-not-open`).; 409 `baseVersion` is not the current version (`plan-version-conflict`), or the plan is already `booked` … |

#### Edge cases to draw

- **Nothing suits the whole group on a day**: Says which answer ruled everything out (e.g. "No rides for under 1.10 m at Summit Peaks on Fri") and offers to change it. *(source: screens/P01-guest-web-storefront.yaml#WEB-050 states.emptyNoResults)*

#### Consistency with other screens

- Match `GST-053`: Same plan and editing rules; the app adds the AI planner chat (GST-054), web is rules-only.
- Match `GST-059`: The booked plan is followed on the day in the app.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
party: 2 adults, 2 children (1.05 m and 1.30 m)
days:
- Fri 2 Oct · Summit Peaks
- Sat 3 Oct · Aqua Park
pace: Balanced
lunch: Emirati · both parks; Indian · Aqua Park only
plan:
- 09:30 Arrive Main Gate
- 09:45 Falcon Coaster (Fast Track)
- 12:30 Lunch · Al Bait Kitchen
- 14:00 Toy Box shop
estimate: Estimated AED 1,840 for the group
```

#### Permissions

- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `generateVisitPlan` → no permission · guest
- `getVisitPlan` → no permission · guest
- `updateVisitPlan` → no permission · guest
- `listVisitPlanAlternatives` → no permission · guest
- `bookVisitPlan` → no permission · guest
- `getTenantAppStatus` → no permission · device, guest, staff

**A refused user sees:** A guest holds no permission. Anyone can build a plan; signing in is asked only to save it, and booking follows the cart's own sign-in gate.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A preference a day's park cannot meet is said, not filled: a "Not at this park" banner per day names the cuisine or shop and the park that has it (e.g. "No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2)."), hidden when all are met. Lunch cuisine options name the parks serving them ("Indian - Summit Peaks only"). *(agreed · MoM 30 Sep 2026, 4.7 · DI-1113)*
- Allam: multi-venue visit planner. In a multi-venue tenant the guest picks a park per chosen day ("Which park each day?", hidden otherwise); each day tab names its park and every item, swap candidate and AI-planner suggestion comes only from that park's rides, dining and shops, never another park's. *(agreed · MoM 30 Sep 2026, 4.7 · DI-1112)*
- Retail/kiosk shops are added to the planner's venue-linked options alongside F&B (previously only F&B). *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1100)*
- Allam: the planner applies multi-venue intelligence; it checks actual venue-level amenities before including a preference, e.g. if only one of several parks has an Indian restaurant. It pulls only rides, F&B and retail available at each specific venue. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1099)*
- Itinerary planner (Yas Island planner reference): party composition (adults/children with height/age), visit dates, pace (packed/balanced/relaxed) and cuisine preferences feed an auto-generated, swappable multi-day itinerary with associated costing. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1098)*
- "Plan Your Adventure": guided itinerary planner (Skidata benchmark) where the guest picks which rides/attractions and in what order ahead of time, tied to the ticket purchase and saved as a personal visit profile. *(client request · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-217)*
- Custom content pages per venue (e.g. "Plan Your Visit", Accessibility) that follow accessibility guidelines. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-190)*

Also apply: 1 for P01 · Discovery & Browse, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'plan your adventure')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Step indicator (`bookingFlow.stepIndicator`) | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | Bar | the step indicator above every booking step: bar, numbered, dots, segmented, breadcrumb, pills, ticks, or none |
| Settings: step indicator (`bookingFlow.venueOverrides[].settings.stepIndicator`) | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | Bar | — |

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

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-050` · status **review** · provenance client-verified
- Prototype (Visit Planner (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Visit Planner.dc.html`, view *Visit Planner → the six questions (defaults) → Make my plan (Your plan)*. Differences: Single-park planner: no "Which park each day?" step, no shops or kiosks as plan stops and no preferenceNotAtVenue (MoM 4.7, 30 September); these are pending in design: specified, and built from the definition until the design shows it (handoff/design-batches/apps/1-guest-app/README.md).
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (40), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (60 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-050?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, preferenceNotAtVenue, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Make my plan, Swap / + Add something, Remove / Undo changes, Book this plan, Change answers.
- [ ] Every transition is wired: `WEB-010`, `WEB-004`, `WEB-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 7 client meeting input(s) for this screen are applied; open questions are built to their default.
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
| Powered by TICVAI credit (`brand.showPoweredBy`) | `CMS-104`, `ADM-016` | — | on | the *Powered by TICVAI* credit on the launch screen, at the foot of Account and in the web footer; on by default, and switching it off needs the licence add-on (403 … |
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

### In P01 · Discovery & Browse

- "Help me choose" (experience builder) is not a consent step: its questions (yes/no, age, certified or not, etc.) filter the catalogue so only suitable products are shown (Deep Dive Dubai reference). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W4 Help me choose · DI-1005)*

**42 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"bookVisitPlan": {"method":"POST","path":"/visit-plans/{planId}/booking","contract":"venue-map","summary":"Book this plan — turn it into cart lines","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"VisitPlanBooking"},
"decideRecommendations": {"method":"POST","path":"/recommendations/decide","contract":"ai","summary":"Fill a recommendation slot","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRecommendationResult"},
"generateVisitPlan": {"method":"POST","path":"/visit-plans","contract":"venue-map","summary":"Build a visit plan from the party, the dates and what they like","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisitPlanRequest","responds":"VisitPlan"},
"getAvailability": {"method":"GET","path":"/availability","contract":"catalogue","summary":"Live remaining capacity","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"performanceId","in":"query","required":null},{"name":"channelCapacityId","in":"query","required":null},{"name":"eventId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PerformanceAvailabilityPage"},
"getCookieConsentRuntime": {"method":"GET","path":"/storefront/cookie-consent","contract":"marketing-crm","summary":"What the page must show and what it may load","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"channel","in":"query","required":true},{"name":"brandId","in":"query","required":false},{"name":"language","in":"query","required":false},{"name":"X-Consent-Key","in":"header","required":false}],"requestBody":null,"responds":"CookieConsentRuntime"},
"getProduct": {"method":"GET","path":"/products/{productId}","contract":"catalogue","summary":"Read a product","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Product"},
"getProductEligibilityRule": {"method":"GET","path":"/products/{productId}/eligibility-rule","contract":"catalogue","summary":"Who may take part: age, height, supervision","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productId","in":"path","required":true}],"requestBody":null,"responds":"ProductEligibilityRule"},
"getPublishedGuidedChoice": {"method":"GET","path":"/venues/{venueId}/guided-choice","contract":"white-label","summary":"The venue's published Help me choose","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuidedChoice"},
"getPublishedTenantConfig": {"method":"GET","path":"/storefront/tenant-config","contract":"white-label","summary":"The published guest-facing configuration, before anyone signs in","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"venueId","in":"query","required":false}],"requestBody":null,"responds":"PublishedTenantConfig"},
"getTenantAppStatus": {"method":"GET","path":"/tenant-config/status","contract":"white-label","summary":"App status and recent changes","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"TenantAppStatus"},
"getVisitPlan": {"method":"GET","path":"/visit-plans/{planId}","contract":"venue-map","summary":"A visit plan, at its current version or an earlier one","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"version","in":"query","required":null}],"requestBody":null,"responds":"VisitPlan"},
"getWaitTimes": {"method":"GET","path":"/queues/wait-times","contract":"queue","summary":"Wait times across a venue","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":true},{"name":"category","in":"query","required":null}],"requestBody":null,"responds":"WaitTime"},
"listMyEntitlements": {"method":"GET","path":"/guests/me/entitlements","contract":"access","summary":"Every ticket, pass and membership this guest holds","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"state","in":"query","required":null},{"name":"includeShared","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPerformances": {"method":"GET","path":"/events/{eventId}/performances","contract":"catalogue","summary":"List performances of an event","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"language","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductCategories": {"method":"GET","path":"/product-categories","contract":"catalogue","summary":"The merchandise hierarchy — categories, brands, collections","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProductCategoryNode"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVisitPlanAlternatives": {"method":"GET","path":"/visit-plans/{planId}/items/{itemId}/alternatives","contract":"venue-map","summary":"What could take this item's place","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"recordDeviceConsent": {"method":"POST","path":"/consent/device","contract":"marketing-crm","summary":"Record a visitor's cookie decision, before anyone is known","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RecordDeviceConsentRequest","responds":"DeviceConsent"},
"recordRecommendationEvents": {"method":"POST","path":"/recommendations/events","contract":"ai","summary":"Report what happened to recommended items","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"recordStorefrontSessionEvents": {"method":"POST","path":"/storefront/session-events","contract":"white-label","summary":"Report a batch of browsing behaviour for fraud prevention, hashed and without personal data","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WhiteLabelStorefrontSessionBatch","responds":null},
"searchCatalogue": {"method":"GET","path":"/search","contract":"catalogue","summary":"Find something by name","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"q","in":"query","required":true},{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"updateVisitPlan": {"method":"PUT","path":"/visit-plans/{planId}","contract":"venue-map","summary":"Swap, remove, add, move or undo, as a new version","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisitPlanUpdate","responds":"VisitPlan"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessibilitySettings": {"type":"object","description":"BL-065, 2.1.27. **POS and kiosk accessibility, which is a legal obligation in most jurisdictions and was unstated.**\n**A kiosk is the hard case.** A guest with low vision using a website brings their own assistive technology; a guest at a kiosk gets whatever the kiosk offers, so the settings have to be on the device rather than in the browser.\n","properties":{"largeTextAvailable":{"type":"boolean","default":true},"highContrastAvailable":{"type":"boolean","default":true},"simplifiedNavigationAvailable":{"type":"boolean","default":true},"screenReaderSupported":{"type":"boolean","default":true},"reachableHeightModeAvailable":{"type":"boolean","default":false,"description":"**Moves the interface to the lower half of the screen** for a guest using a wheelchair. A kiosk mounted at standing height is unusable otherwise, and no software setting fixes the mounting — this is the mitigation.\n"},"sessionTimeoutMultiplier":{"type":"number","default":1,"description":"**Timeouts are an accessibility barrier nobody counts.** A guest who needs three times as long to read a screen should not lose their basket to a 90-second inactivity timer.\n"}}},
"AiRecommendationItem": {"type":"object","x-ticvai-persistence":"none — held in jsonb on ai.rec_decision.items, through AiRecommendationItemList","description":"One recommended item. **Carries a Pricing price reference, never a computed price** (AIR-029).","required":["trackingId","rank"],"properties":{"trackingId":{"type":"string","format":"uuid","description":"Echoed on every `recordRecommendationEvents` event and as `orders.addCartLine.recommendationId`, so attribution never guesses."},"productId":{"type":"string","format":"uuid","nullable":true,"description":"The product recommended. **Exactly one of `productId`, `promotionId` or `couponRef`, `rewardId` or `challengeId` is set, by `kind`** (29 September, build): `offer` carries a promotion or coupon, `reward` a loyalty reward, `challenge` a challenge, every other kind a product."},"promotionId":{"type":"string","format":"uuid","nullable":true,"description":"For `offer`, a published promotion the guest is eligible for. Promotions computes the discount at the basket, never the engine."},"couponRef":{"type":"string","nullable":true,"description":"For `offer`, a coupon campaign; a code is assigned only when the guest takes it (`promotions.assignCoupon`)."},"rewardId":{"type":"string","format":"uuid","nullable":true,"description":"For `reward`, a marketing-crm loyalty reward the guest can redeem."},"challengeId":{"type":"string","format":"uuid","nullable":true,"description":"For `challenge`, a marketing-crm challenge the guest can join."},"kind":{"type":"string","enum":["upsell","crossSell","upgrade","bundle","addOn","membership","nextBestOffer","offer","reward","challenge"]},"rank":{"type":"integer","minimum":1},"priceRef":{"type":"string","nullable":true,"description":"The Pricing reference the channel resolves to a price. AI never computes a price."},"reasonTemplateKey":{"type":"string","nullable":true,"description":"The template reason (decided 29 September, decision 9): no model writes guest-visible reasons."},"reasonText":{"type":"string","nullable":true,"description":"The rendered template in the session locale, where the channel shows reasons."},"confidenceBand":{"type":"string","enum":["high","medium","low"],"description":"Design 5.6: a band, never a bare percentage."},"score":{"type":"number","nullable":true,"description":"Normalised score. **Returned to staff callers only**; a guest response omits it."}}},
"AiRecommendationResult": {"type":"object","x-ticvai-persistence":"none — written as ai.rec_decision after the response","description":"The recommendation slot's content (design 2.2 A). Empty `items` is a valid answer: the slot stays empty.","required":["decisionId","mode","items","expiresAt"],"properties":{"decisionId":{"type":"string","format":"uuid"},"placement":{"type":"string","enum":["productPage","cart","checkout","postPurchase","preVisit","inVenue","posBasket","kioskBasket","fnbMenu","retailBasket","seatUpgrade","membership","email","homepage","loyalty"]},"mode":{"type":"string","enum":["personalised","contextual","rulesOnly","fallback"]},"items":{"type":"array","items":{"$ref":"#/components/schemas/AiRecommendationItem"}},"expiresAt":{"type":"string","format":"date-time"}}},
"AppAvailability": {"type":"string","description":"**The sold-out or closed signal (decided 28 September, audit R073).** `open` is the normal state. `soldOut` shows WEB-029's sold-out state across the app while browsing still works; `closed` shows the closed state (a weather closure, a private event). Neither refuses a request on its own: it is what the guest is told, and a sale is still refused by availability where it applies. Set with `setMaintenanceMode`.\n","enum":["open","soldOut","closed"],"default":"open"},
"AppIcons": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["sourceAssetRef","changeScope"],"properties":{"sourceAssetRef":{"type":"string","format":"uuid","description":"The `MediaAsset` id of the 1024×1024 source."},"derived":{"type":"array","readOnly":true,"x-ticvai-derived":"onWrite","description":"Generated by `setAppIcons` from the source, one entry per platform and size — the iOS and Android store sets and the web favicons listed on `setAppIcons` (audit R163).","items":{"type":"object","properties":{"platform":{"type":"string","enum":["ios","android","web"]},"size":{"type":"string"},"assetRef":{"type":"string","format":"uuid"}}}},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Always `buildTime` — icons are baked into the binary."},"liveVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Icon currently shipped. Differs from the draft until the next release."},"requiresRebuild":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onRead","description":"True while the draft's source differs from the icon in `liveVersion`."}}},
"BookingFlowConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","description":"**Set per tenant, with a per-venue override (decided 29 September, rev 3 CFG-11).** One tenant with several venues (the Kids Club branches, Coastal Aqua beside Union Arena) needs them to differ. The settings in force at a venue are the tenant's, with that venue's entry in `venueOverrides` laid over them field by field. The guest app resolves them for the venue the guest picked (audit R267); `effectiveForVenueId` on `getBookingFlowConfig` returns them resolved.\n","allOf":[{"$ref":"#/components/schemas/BookingFlowSettings"},{"type":"object","properties":{"venueOverrides":{"type":"array","maxItems":200,"default":[],"description":"Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. An override for a venue later closed is kept and has no effect.","items":{"$ref":"#/components/schemas/BookingFlowVenueOverride"}}}}]},
"BrandIdentity": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","description":"Every `*AssetRef` here is a `MediaAsset` id from the `assets` library (`createUpload` then `completeUpload`), PNG or SVG and at most 2 MB (decided 28 September, audit R270).\n","required":["logoAssetRef"],"properties":{"logoAssetRef":{"type":"string","format":"uuid","description":"The primary logo."},"logoDarkAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"Used on dark backgrounds. Falls back to the primary logo."},"logoVariant":{"type":"string","enum":["light","dark","duotone"],"default":"light","description":"**Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4).** `light` uses `logoAssetRef`, `dark` uses `logoDarkAssetRef` (falling back to the primary logo), and `duotone` the two-colour reading of the primary logo.\n"},"faviconAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"The browser tab icon for the guest web app."},"splashImageAssetRefs":{"type":"array","description":"Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163).","items":{"type":"string","format":"uuid"}},"splashDurationSeconds":{"type":"integer","minimum":0,"maximum":10,"default":3},"splashBackgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"showLoadingIndicator":{"type":"boolean","default":true},"splashChangeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163)."},"introVideoAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"**The optional intro video (decided 29 September, MOB-5).** A video `MediaAsset` from the media library (CMS-010). Streamed, so a change reaches guests with the publish and needs no app build.\n"},"introVideoMode":{"type":"string","enum":["off","firstLaunch","everyLaunch"],"default":"off","description":"When GST-001 plays it full screen. \"Skip introduction\" is always shown. Anything but `off` needs `introVideoAssetRef`, or 400."},"showPoweredBy":{"type":"boolean","default":true,"description":"**\"Powered by TICVAI\", a configuration toggle, on by default** (Chinmay, 2 October, workbook Q160 and the pre-apply round; consistent with DI-297; CHG-CSA-036). Shown on the launch screen and at the foot of Account and the web footer while true. **Switching it off needs the tenant's licence to allow it**: `setBrandIdentity` refuses `false` with `403 powered-by-locked` unless the tenant's plan carries the `poweredByRemoval` add-on (subscription `LicencePosition.poweredByRemovable`)."}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"ConsentSource": {"type":"string","enum":["guestApp","website","kiosk","pos","callCentre","import","agentRecorded","cookieBanner","checkout"],"description":"`checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents`, bound to the order and the verified contact. `cookieBanner` (29 September, build; BL-073 §4b): a decision made on the cookie banner or preference centre and moved onto the guest by `claimDeviceConsent`. Kept apart from `website`, a form submission, because the audit trail (2.6.56) has to tell the two apart."},
"CookieBannerPreferenceCenterDesignerView": {"type":"object","x-ticvai-persistence":"marketing.cookie_banner_design","description":"One version of a cookie banner and preference-centre design (pack 17.1.6).","required":["channel","position","languages","rejectIsOneClick","categories"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"Null for the corporate design every brand inherits."},"inheritsFromId":{"type":"string","format":"uuid","nullable":true},"channel":{"type":"string","enum":["b2cWebsite","customerPortal","mobileApp","embeddedCheckout","whiteLabelSite","partnerMicrosite"]},"logoAssetId":{"type":"string","format":"uuid","nullable":true},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedText"},"position":{"type":"string","enum":["top","bottom","popup","modal"]},"themeId":{"type":"string","nullable":true,"description":"The white-label theme it takes colours and fonts from."},"buttons":{"type":"array","items":{"type":"object","required":["action"],"properties":{"action":{"type":"string","enum":["acceptAll","rejectNonEssential","managePreferences","savePreferences","doNotSellOrShare"]},"label":{"$ref":"#/components/schemas/LocalisedText"}}}},"rejectIsOneClick":{"type":"boolean","default":true,"description":"Must be true."},"links":{"type":"array","items":{"type":"object","required":["label","policyKind"],"properties":{"label":{"$ref":"#/components/schemas/LocalisedText"},"policyKind":{"type":"string","enum":["privacy","cookie","termsAndConditions"]}}}},"categories":{"type":"array","minItems":1,"items":{"type":"object","required":["category","defaultOn"],"properties":{"category":{"type":"string","enum":["strictlyNecessary","functional","analytics","personalisation","marketing"]},"description":{"$ref":"#/components/schemas/LocalisedText"},"defaultOn":{"type":"boolean","description":"True only for `strictlyNecessary`, which is always active."}}}},"languages":{"type":"array","minItems":1,"items":{"type":"string","maxLength":10},"description":"Every language the storefront serves; Arabic renders right to left."},"regulatoryRegimes":{"type":"array","items":{"type":"string","enum":["gdpr","ePrivacy","ccpaCpra","lgpd","uaePdpl","saudiPdpl"]},"description":"2.6.60 (29 September, build). **The laws this design is published to satisfy**, so compliance is stated rather than assumed. The strictest posture (opt-in, one-click reject, every non-essential category off) already meets GDPR/ePrivacy, LGPD and both PDPLs; `ccpaCpra` adds the \"Do not sell or share\" button (`doNotSellOrShare`) and honours a Global Privacy Control signal as that opt-out."},"recordIpAddress":{"type":"boolean","default":false,"description":"2.6.55, \"if legally permitted\" (29 September, build). On, `recordDeviceConsent` writes the IP address and user agent to `pii.consent_identifier`; off, they are not kept anywhere. Off by default."},"noticeVersion":{"type":"string","readOnly":true,"description":"Moves with the cookie policy (white-label `setPolicy`, kind `cookie`)."},"version":{"type":"integer","minimum":1,"readOnly":true},"status":{"type":"string","enum":["draft","published","superseded"],"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CookieCategory": {"type":"string","enum":["strictlyNecessary","functional","analytics","personalisation","marketing"],"description":"2.6.53. The five categories the banner design (`CookieBannerPreferenceCenterDesignerView.categories`) offers; the matrix's \"preference\" category is `personalisation` (British spelling, as `ConsentPurpose`)."},
"CookieConsentChannel": {"type":"string","enum":["b2cWebsite","customerPortal","mobileApp","embeddedCheckout","whiteLabelSite","partnerMicrosite"],"description":"The six governed surfaces, as the registry and the banner design name them (pack 17.1.5-17.1.6)."},
"CookieConsentRuntime": {"type":"object","x-ticvai-persistence":"none — assembled at read time from marketing.cookie_banner_design, marketing.tracking_technology and marketing.device_consent","description":"What `getCookieConsentRuntime` gives the storefront tag loader and the app SDK gate (2.6.52, 2.6.58).","required":["banner","noticeVersion","requiresDecision","allowedTechnologies","consentModeSignals"],"properties":{"banner":{"$ref":"#/components/schemas/CookieBannerPreferenceCenterDesignerView"},"noticeVersion":{"type":"string"},"requiresDecision":{"type":"boolean","description":"True with no decision, an expired one, or one given against a superseded notice."},"decision":{"allOf":[{"$ref":"#/components/schemas/DeviceConsent"}],"nullable":true,"description":"The latest decision for the presented key; null without a key."},"allowedTechnologies":{"type":"array","description":"Per category, the approved technologies it unlocks. Anything not listed never loads.","items":{"type":"object","required":["category","technologies"],"properties":{"category":{"$ref":"#/components/schemas/CookieCategory"},"granted":{"type":"boolean","description":"Whether the presented decision grants it; always true for `strictlyNecessary`."},"technologies":{"type":"array","items":{"type":"object","required":["name","provider"],"properties":{"name":{"type":"string"},"provider":{"type":"string"},"technologyType":{"type":"string"}}}}}}},"consentModeSignals":{"type":"object","description":"**The decision in Google consent-mode terms** (2.6.65), so Analytics and Tag Manager are told, not left to guess. `denied` wherever no decision grants the category.","properties":{"adStorage":{"type":"string","enum":["granted","denied"]},"adUserData":{"type":"string","enum":["granted","denied"]},"adPersonalization":{"type":"string","enum":["granted","denied"]},"analyticsStorage":{"type":"string","enum":["granted","denied"]},"functionalityStorage":{"type":"string","enum":["granted","denied"]},"personalizationStorage":{"type":"string","enum":["granted","denied"]},"securityStorage":{"type":"string","enum":["granted"]}}}}},
"DeviceConsent": {"type":"object","x-ticvai-persistence":"marketing.device_consent + marketing.device_consent_category","description":"**One cookie decision by a visitor nobody has identified yet** (BL-073 §4b, decided 29 September). Append-only: a change of mind is a new row. Keyed for the visitor by `consentKey`, which the platform mints; the categories are child rows. The IP address and user agent, where recorded at all, are in `pii.consent_identifier` (`ConsentCaptureIdentifier`), never here.","required":["consentKey","channel","action","categories","noticeVersion","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"consentKey":{"type":"string","maxLength":64,"readOnly":true,"description":"**Opaque, minted by us, not a device fingerprint.** It answers 2.6.55's \"user identifier/session ID\" and is the join key `claimDeviceConsent` needs. Shared by all the tenant's domains (2.6.62), never across tenants."},"channel":{"$ref":"#/components/schemas/CookieConsentChannel"},"brandId":{"type":"string","format":"uuid","nullable":true},"bannerDesignId":{"type":"string","format":"uuid","nullable":true,"description":"The published `CookieBannerPreferenceCenterDesignerView` version the visitor was shown."},"action":{"$ref":"#/components/schemas/DeviceConsentAction"},"categories":{"type":"array","minItems":1,"description":"Every category of the design, with the decision this row gives it.","items":{"type":"object","required":["category","decision"],"properties":{"category":{"$ref":"#/components/schemas/CookieCategory"},"decision":{"type":"string","enum":["granted","declined"]}}}},"noticeVersion":{"type":"string","description":"The cookie notice version decided against (white-label `setPolicy`, kind `cookie`)."},"language":{"type":"string","maxLength":10,"nullable":true},"globalPrivacyControl":{"type":"boolean","default":false,"description":"The browser sent a Global Privacy Control signal; honoured as a CCPA/CPRA opt-out of sale and sharing."},"source":{"$ref":"#/components/schemas/ConsentSource"},"country":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true,"readOnly":true,"description":"The edge's geolocation of the request, for the geographic statistics (2.6.63). The address is not kept here."},"decidedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**A device consent expires and a subject consent does not.** Set from the tenant's device-consent term; after it the banner asks again."},"claimedBySubjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Set once, by `claimDeviceConsent`. Never cleared."},"claimedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005), tenant-scoped: a decision with no subject still belongs to one tenant."}}},
"DeviceConsentAction": {"type":"string","enum":["acceptAll","rejectNonEssential","savePreferences","withdraw","doNotSellOrShare"],"description":"What the visitor pressed. `doNotSellOrShare` is the CCPA/CPRA opt-out link, shown where the design's `regulatoryRegimes` include `ccpaCpra`."},
"Entitlement": {"type":"object","x-ticvai-persistence":"access.entitlement","description":"**What a guest actually holds.** Found missing on 18 August by the schema audit — 33 tables in `orders`, seven in `access`, and none of them stored an issued ticket.\nThe package sold products, defined `EntitlementTemplate`, recorded `ScanEvent.ticketId`, transferred `ticket_transfer.ticketIds` and issued `wallet_pass.entitlementId` — **five artefacts referring to a thing that did not exist.** `validateAccess` read the *template* and never the instance, and `suspendEntitlement` suspended the template, **which would have suspended it for every guest who held one.**\n**The template is the definition and this is the instance.** A template says *an annual pass admits once a day for a year*; this says *this guest's annual pass, bought on 3 March, used eleven times, frozen for two weeks in July, valid until 2 March.*\n","required":["id","templateId","productId","orderId","subjectId","status","validFrom","validTo"],"properties":{"id":{"type":"string","format":"uuid","description":"A UUIDv7, matching `TicketStatus.ticketId` — **stable for the life of the ticket and independent of the media carrying it.** A guest whose wristband broke keeps the same entitlement with a new `mediaCode`.\n**This is the ticket id.** Wherever an operation takes a `ticketId` or `ticketIds` — `lookupTicket`, `listScans`, `ScanEvent`, the offline package and `transferOrderTickets` — it is this value. An order line's `entitlementIds` are the ticket ids of that line.\n"},"templateId":{"type":"string","format":"uuid","description":"The definition it was issued against. **Pinned at issue** — a template edited next month must not change what this guest bought.\n"},"productId":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","nullable":true,"description":"The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`). **Null for an entitlement an invitation issued** (`invitationId`; 4 October 2026, CHG-FXC-007)."},"orderLineId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Who holds it. **Null is legitimate** — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is claimed.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"mediaCode":{"type":"string","description":"What is scanned — a QR payload, a wristband serial, a card number. **Rotatable without reissuing**, because a guest whose wristband broke should not need a new ticket.\n"},"status":{"$ref":"../spine/orders.yaml#/components/schemas/EntitlementStatus"},"statusNote":{"type":"string","nullable":true,"description":"**Not `TicketStatus` — that is a validation result with a misleading name**, computed at scan time and carrying `isValid` and `isInsideVenue`. The lifecycle is `orders.EntitlementStatus`, and `states/entitlement-status.yaml` has modelled it since before this table existed.\n**Which is the finding in one line: the package had the lifecycle, the state model and the validation result, and no row to hang them on.**\n"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time","description":"**Resolved at issue from the template, then owned here.** A freeze extends it, a reissue replaces it, and neither reaches back to the template.\n**What the pre-expiry notice is measured from** (29 September, build pass, group G2; 5.5.30). A daily run in access publishes `entitlement.expiringSoon` once per entitlement and `validTo` when an entitlement in `issued` or `partiallyConsumed` comes within its template's `expiryNoticeDays` (`catalogue.EntitlementTemplate`), and not for one bought inside that window. Marketing turns it into the reminder (a `MessageTrigger` on the event, or a triggered campaign on `entitlementExpiring`); access only says the date is near. A freeze or renewal that moves `validTo` raises the next notice once.\n"},"entriesUsed":{"type":"integer","default":0,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**The number `validateAccess` decrements and nothing was decrementing.** A ten-entry pass with no counter is a ten-entry pass that admits forever.\n**Maintained on write**, in the same transaction as the admitting `access.scan_event` row: by `validateAccess`, `validateGroupAccess` (by the count admitted) and `syncScans` for each replayed admission the server accepts. A replayed scan the server downgrades to `denied` does not count.\n"},"entriesAllowed":{"type":"integer","nullable":true},"lastEntryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`recordedAt` of the latest admission counted in `entriesUsed`, written by the same writes. A scan replayed late with an earlier `recordedAt` does not move it back.\n"},"firstEntryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`recordedAt` of the first admission, written by the same writes as `lastEntryAt`; it starts a time-bound entitlement's window (DEC-232; CHG-CSP-030). A replayed earlier scan moves it back."},"timeBoundUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Where the template is time-bound, when its window closes**: `firstEntryAt` plus the validity rule's `minutesAfterFirstScan` (decided 2 October 2026, Chinmay, BO-159; DEC-232; CHG-CSP-030). Null until the first scan and on an entitlement with no time bound. A scan after it is denied (`timeBoundWindowElapsed`); it never extends `validTo`, and the earlier of the two wins."},"lifecycleLabel":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","enum":["created","pendingFulfillment","active","partiallyUsed","used","expired","suspended","cancelled","voided","reissuedSuperseded","refunded","transferred","blocked"],"description":"**The Virtual Ticket status in the client's 13 names, mapped onto the entitlement model** (decided 2 October 2026, Chinmay, critical set 2, BO-336: \"Map the pack's 13 names onto the model; add any missing states\", and BO-336/DI-670: \"Reserved maps to Pending fulfilment\"; DEC-266; CHG-CSP-033). Computed on read from `status` (orders `EntitlementStatus`), `suspendedReason`, `cancellationKind`, `issuedVia` and an active identity lock; the mapping is in `states/entitlement-status.yaml`. It is what BO-334, BO-336 and the ticket status transition matrix (`AccessTicketStatusTransition`) show; logic still reads `status`."},"cancellationKind":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","enum":["voided","refunded","performanceCancelled","superseded"],"description":"**Which act cancelled the entitlement**, so the pack's Voided, Refunded and Reissued / superseded are told apart while `status` keeps the one r1 value `cancelled` (DEC-266; CHG-CSP-033). Written with the cancelling transition: `voidEntitlement`, `createRefund`, `cancelPerformance`, or a reissue that supersedes it (`supersedesEntitlementId` on the new one). Null unless `cancelled`."},"frozenDays":{"type":"integer","default":0,"readOnly":true,"x-ticvai-derived":"onWrite","description":"Days added by a freeze. **Maintained on write** by the freeze operation (`freezeEntitlement`), in the same write that extends `validTo` by those days. **Held here rather than computed from a freeze log**, because a gate has to answer in under 300ms and cannot replay a history to decide validity.\n"},"suspendedReason":{"type":"string","nullable":true},"freezeReason":{"type":"string","nullable":true,"enum":["travelling","injury","personal","seasonal","other"],"description":"The `reason` of the latest `freezeEntitlement` (audit R222). Null when never frozen."},"freezeNote":{"type":"string","nullable":true,"maxLength":500,"description":"The `note` the latest `freezeEntitlement` took, required there when `reason` is `other` (decided 28 September, audit R222). Kept so the quarterly review of `other` notes has something to read."},"isNameBound":{"type":"boolean","default":false},"holderName":{"type":"string","nullable":true},"sharedWithSubjectIds":{"type":"array","description":"`shareEntitlement`. **The owner keeps it and a second person may present it** — the asymmetry that stops a shared family pass becoming a resale chain.\n","items":{"type":"string","format":"uuid"}},"issuedVia":{"type":"string","enum":["sale","invitation","reissue","transfer","resale","membership","groupBooking"],"description":"**How it came to exist, and it matters to finance.** A sold entitlement carries deferred revenue; an invitation carries a marketing cost; a reissue carries neither.\n"},"supersedesEntitlementId":{"type":"string","format":"uuid","nullable":true,"description":"For a reissue or a resale. **The chain is traceable** — a ticket appearing from nowhere is indistinguishable from a fraudulent one.\n"},"walletValueId":{"type":"string","format":"uuid","nullable":true,"description":"Where the template carries stored value. **A `retail.Wallet` bound to the entitlement, not a balance on it** (CF-126).\n"},"facePassEnrolmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"The active `facePass` enrolment on this entitlement (`FacePassEnrolment.id`), or null when none is. **Computed on read from `pii.subject_biometric` and not stored here** — the PII split keeps the biometric on its own side, and this carries only its id. It is how a screen holding a pass finds the enrolment `getFacePassEnrolment` and `revokeFacePass` take.\n"},"invitationId":{"type":"string","format":"uuid","nullable":true,"description":"**The invitation that issued it** (4 October 2026, CHG-FXC-007): `orders.issueInvitation` issues the entitlement without an order, because an invitation never enters the order path. Exactly one of `orderId` and `invitationId` is set."}}},
"FontConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["primaryLatin"],"properties":{"primaryLatin":{"type":"string"},"primaryArabic":{"type":"string","nullable":true,"description":"Required when `ar` is among the tenant's languages (audit R163). A Latin face alone leaves Arabic in a system fallback that will not match.\n"},"secondaryLatin":{"type":"string","nullable":true},"secondaryArabic":{"type":"string","nullable":true,"description":"Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163)."},"customFontAssetRefs":{"type":"array","description":"Uploaded font files, as `MediaAsset` ids.","items":{"type":"string","format":"uuid"}},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"x-ticvai-derived":"onRead","description":"Custom font files are `buildTime`; selecting a bundled face is `runtime`."}}},
"FooterConfig": {"type":"object","x-ticvai-persistence":"whitelabel.footer_config + whitelabel.footer_config_column + whitelabel.footer_config_social_link","description":"BL-002. **`setHeader` and `HeaderConfig` exist and the footer does not**, which looked like symmetry until you notice it is not: **a header is chrome and a footer is a link surface.**\nA footer carries the legal links — terms, privacy, accessibility statement, cookie preferences — and **those are the ones a regulator checks.** Treating it as a mirror of the header would have given it a logo and no way to reach a privacy notice.\n**Where it is stored.** `legalLinks` and `copyrightText` are columns of `whitelabel.footer_config`; each entry of `columns` is a `whitelabel.footer_config_column` row and each entry of `socialLinks` a `whitelabel.footer_config_social_link` row. Part of the working draft (see the header). **In the tenant's own database, not the control plane (decided 28 September, audit R163)**: it moved from `control.footer_config` and its two child tables.\n","required":["id","scopePath"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005), written at `tenant` scope by the server."},"columns":{"type":"array","items":{"type":"object","properties":{"heading":{"type":"string"},"links":{"type":"array","items":{"type":"object","properties":{"label":{"type":"string"},"url":{"type":"string"},"opensCookiePreferences":{"type":"boolean","default":false}}}}}}},"legalLinks":{"type":"object","description":"**Required links, held separately from the free-form columns** — a tenant reorganising their footer must not be able to remove the privacy notice by accident.\n","properties":{"termsUrl":{"type":"string"},"privacyUrl":{"type":"string"},"accessibilityUrl":{"type":"string","nullable":true},"cookiePolicyUrl":{"type":"string","nullable":true}}},"copyrightText":{"type":"string"},"socialLinks":{"type":"array","items":{"type":"object","properties":{"platform":{"type":"string"},"url":{"type":"string"}}}}}},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"GuidedChoice": {"x-ticvai-persistence":"whitelabel.guided_choice + whitelabel.guided_choice_question + whitelabel.guided_choice_answer","type":"object","description":"**Help me choose (decided 29 September, rev 3 REV3-11).** A venue's short set of questions that ends on a result card opening the booking flow, product, category or event that fits. Each question has a few answers with a title, a one-line body, an icon and an optional badge; **the answer the guest picks on the last question decides the result**, and each earlier answer carries a target too, so a one-question setting still ends on a result. Venue configuration, never hard-coded: set up in Venue Management, off unless the venue publishes one.\n**Two sources, one review.** `manual` is written by staff; `aiSuggested` is proposed by the `ai` service from the venue's uploaded products (a suggestion, reviewed and published by a person, never auto-published). Both arrive as `draft`.\n**Help me choose filters the catalogue (decided 29 September, W4).** With `behaviour` `filter`, the default, each answer's `filter` narrows the products the guest sees (web, mobile and kiosk alike, through catalogue `listProducts` and `searchCatalogue` `guidedAnswerIds`), with a \"Show everything\" link; `recommend` keeps the rev 3 result card from the last answer's `target`. **It is never a consent step**: an answer may pre-fill a REV3-26 consent question (`consentPrefill`), which the guest still confirms, so the question is not asked twice and the consent stays explicit.\n","required":["id","venueId","name","mode","questions","status","source"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"UUIDv7."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `createGuidedChoice`."},"name":{"type":"string","maxLength":80,"description":"Staff-facing name, e.g. \"Water park day planner\". Not shown to guests."},"mode":{"type":"string","enum":["button","popupOnArrival","off"],"default":"button","description":"**How the guest reaches it (rev 3 REV3-11).** `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on the guest's first arrival at the booking page (whether it was seen is kept on the device only); `off` keeps a published choice configured but not shown.\n"},"showBanner":{"type":"boolean","default":true,"description":"The dark banner under the products (\"Choose from the experiences above or let us help you decide\") with a Help me choose button. Ignored when `mode` is `off`."},"behaviour":{"type":"string","enum":["filter","recommend"],"default":"filter","description":"**`filter` (default) narrows the list; `recommend` ends on one result card (decided 29 September, W4).** With `filter`, every answer needs a `filter` and `target` is optional; with `recommend`, every answer on the last question needs a `target`. `publishGuidedChoice` refuses the other case with 422.\n"},"showEverything":{"type":"boolean","default":true,"description":"The \"Show everything\" link under a filtered list, which clears the answers (W4)."},"questions":{"type":"array","minItems":1,"maxItems":4,"description":"**One to four questions** (decided 29 September, W4: the Deep Dive reference asks three or four; rev 3 REV3-11 allowed two). Shown in `sortOrder`.\n","items":{"type":"object","required":["title","sortOrder","answers"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"UUIDv7. The row's own key."},"title":{"$ref":"#/components/schemas/LocalisedText"},"kind":{"type":"string","enum":["choice","yesNo","age","level","certification"],"default":"choice","description":"**What the question asks (decided 29 September, W4).** `choice` free answers; `yesNo` two answers (e.g. \"Can everyone swim?\"); `age` answers carrying an age range; `level` answers carrying a level tag; `certification` answers saying whether the guest holds a certificate (e.g. a diving licence). The kind decides which `filter` fields its answers use.\n"},"sortOrder":{"type":"integer","minimum":0},"answers":{"type":"array","minItems":2,"maxItems":4,"description":"Two to four answers; the prototype shows three (proposed, client to correct, rev 3 REV3-11).","items":{"type":"object","required":["title","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"UUIDv7. The row's own key."},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"The one-liner under the title, at most 140 characters in each language."},"icon":{"type":"string","maxLength":40,"nullable":true,"description":"An icon name from the guest app's icon set."},"badge":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Optional, e.g. \"Best value\". At most 24 characters in each language."},"sortOrder":{"type":"integer","minimum":0},"target":{"allOf":[{"$ref":"#/components/schemas/GuidedChoiceTarget"}],"nullable":true,"description":"Required with `behaviour` `recommend` on the last question; optional with `filter`, where it is the card shown above the filtered list."},"filter":{"type":"object","nullable":true,"description":"**What this answer keeps in the list (decided 29 September, W4).** Every field set must hold; answers to different questions are combined with AND. Required with `behaviour` `filter`. The server applies it (catalogue `guidedAnswerIds`), so web, mobile and kiosk show the same list.\n","properties":{"productIds":{"type":"array","items":{"type":"string","format":"uuid"}},"productCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"segmentTags":{"type":"array","description":"Catalogue `Product.segmentTags`, e.g. a level tag.","items":{"type":"string"}},"minAgeYears":{"type":"integer","minimum":0,"nullable":true},"maxAgeYears":{"type":"integer","minimum":0,"nullable":true,"description":"With `minAgeYears`, checked against each product's age rule (catalogue `ProductEligibilityRule`)."},"requiresSwimmer":{"type":"boolean","nullable":true,"description":"False hides products whose eligibility needs a swimmer; true keeps only those."},"certificationCode":{"type":"string","nullable":true,"maxLength":40,"description":"Keeps products that need this certificate, or with `holdsCertification` false, hides them."},"holdsCertification":{"type":"boolean","nullable":true}}},"consentPrefill":{"type":"object","nullable":true,"description":"**Pre-fills a REV3-26 consent question from this answer (decided 29 September, W4).** The guest still ticks it at the consent step; nothing is recorded as consent until they do.\n","required":["consentQuestionId","answer"],"properties":{"consentQuestionId":{"type":"string","format":"uuid"},"answer":{"type":"boolean"}}},"result":{"type":"object","nullable":true,"description":"The result card when this answer decides the result. Absent fields fall back to the target's own name, summary and image.","properties":{"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedText"},"imageAssetRef":{"type":"string","format":"uuid","nullable":true}}}}}}}}},"status":{"allOf":[{"$ref":"#/components/schemas/GuidedChoiceStatus"}],"readOnly":true},"source":{"type":"string","enum":["manual","aiSuggested"],"readOnly":true,"description":"`manual` when staff created it; `aiSuggested` when the `ai` service proposed it (a service caller). Kept after a person edits a suggestion, so a report can say how many AI proposals were published."},"suggestionRef":{"type":"string","nullable":true,"readOnly":true,"description":"For `aiSuggested`, the id of the `ai` job that proposed it. Null for `manual`."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"publishedBy":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The person who published it. Never a service."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"GuidedChoiceStatus": {"type":"string","description":"**Draft until a person publishes it (decided 29 September, rev 3 REV3-11).** Guests see only a `published` choice. An AI-proposed choice arrives as `draft` and is never published by the system. Moves as `states/guided-choice.yaml` says: `publishGuidedChoice` and `unpublishGuidedChoice`, and a publish returns the venue's previously published choice to `draft`.\n","enum":["draft","published"],"default":"draft"},
"GuidedChoiceTarget": {"x-ticvai-persistence":"none — embedded","type":"object","description":"**What an answer opens (decided 29 September, rev 3 REV3-11).** A product (its kind picks the booking flow), a product category (its tickets, as `ticketCategories` shows them), an event, or a module such as `membership`. Each id must belong to the choice's venue and be on sale or enabled when the choice is published, or `publishGuidedChoice` refuses it.\n","required":["kind"],"properties":{"kind":{"type":"string","enum":["product","productCategory","event","module","bookingFlow"]},"productId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `product`. A catalogue `Product`."},"productCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `productCategory`. A catalogue `ProductCategory`."},"eventId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `event`."},"moduleKey":{"allOf":[{"$ref":"#/components/schemas/ModuleKey"}],"nullable":true,"description":"Required when `kind` is `module`. The module must be enabled."},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `bookingFlow` (decided 29 September, W12; BUILD-YOUR-EXPERIENCE \"each answer points to one booking flow\"). One of the venue's enabled `BookingFlow`s."}}},
"HeaderConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["layout"],"properties":{"layout":{"type":"string","enum":["logoLeft","logoCentre","logoWithMenu"]},"showLogo":{"type":"boolean","default":true},"showMenu":{"type":"boolean","default":true},"showNotifications":{"type":"boolean","default":true},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},
"HomepageLayout": {"x-ticvai-persistence":"whitelabel.homepage_layout + whitelabel.homepage_section","x-ticvai-retired-columns":["whitelabel.homepage_section.homepage_section_id"],"type":"object","description":"**The client-approved web and app wireframes are the layout** (Chinmay, 2 October, workbook Q163; CHG-CSA-040): sections, their order and their options follow the approved wireframes and change only where the spec breaks. **Landing-page templates** (workbook Q41 batch 2; CHG-CSA-037): a tenant with no landing page of its own starts from a TICVAI template (`templateKey`, `listLandingPageTemplates`); a tenant with its own site links into the storefront with deep links (`getDeepLinkScheme`, `buildDeepLink`).","required":["sections"],"properties":{"templateKey":{"type":"string","nullable":true,"description":"The landing-page template this layout started from (`listLandingPageTemplates`), or null for a layout composed from scratch (CHG-CSA-037)."},"landingSource":{"type":"string","enum":["storefront","ownSite"],"default":"storefront","description":"`storefront`: this home is the tenant's landing page. `ownSite`: the tenant's own website is the landing page and links in with deep links; this home is still served at the storefront address."},"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"sections":{"type":"array","items":{"type":"object","required":["kind","sortOrder","isVisible"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"kind":{"$ref":"#/components/schemas/HomepageSectionKind"},"title":{"$ref":"#/components/schemas/LocalisedText"},"sortOrder":{"type":"integer"},"isVisible":{"type":"boolean"},"contentPageId":{"type":"string","format":"uuid","nullable":true},"maxItems":{"type":"integer","nullable":true,"description":"**How many cards the section shows, the venue's choice** (Chinmay, 2 October, workbook Q152: every customisation option of the approved wireframe, including the card count per section; CHG-CSA-040). Replaces the fixed 1 or 2 highlights of MOB-3: the CMS offers the counts the approved wireframe offers."},"scrollAnimation":{"type":"string","enum":["rise","scale","slide","blur","none"],"default":"rise","description":"**How the section enters as the guest scrolls** (Chinmay, 2 October, workbook Q153: \"must be there\"; DI-1088; CHG-CSA-040). Rise, Scale, Slide, Blur or None, as the v4 prototype offers; `none` for guests who asked the device for reduced motion is applied whatever is set."},"heroStyle":{"type":"string","nullable":true,"enum":["carousel","video","poster","split",null],"description":"For `heroBanner` only (decided 29 September, MOB-3)."}}}}}},
"LanguageConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["languages","defaultLanguage"],"properties":{"languages":{"type":"array","description":"**A tenant may add or select interface languages beyond English and Arabic** (Chinmay, 2 October, workbook Q145; CHG-CSA-039). Any ISO 639-1 language. English and Arabic ship with complete interface strings; for any other, the interface strings come as a TICVAI string pack drafted by AI translation and reviewed (T03), and a string with no translation falls back to English. Content (pages, products, banners) is the tenant's to translate (`translationGaps`).","items":{"type":"string","pattern":"^[a-z]{2}$"}},"defaultLanguage":{"type":"string","pattern":"^[a-z]{2}$"},"uiStringCoverage":{"type":"array","readOnly":true,"description":"How complete the interface strings are in each enabled language (CHG-CSA-039). English and Arabic are always complete.","items":{"type":"object","properties":{"language":{"type":"string"},"coveragePercent":{"type":"number","minimum":0,"maximum":100},"status":{"type":"string","enum":["complete","draft","missing"]}}}},"rtlLanguages":{"type":"array","readOnly":true,"x-ticvai-derived":"onRead","description":"The enabled languages written right to left — those whose Unicode CLDR character order is `right-to-left` (Arabic, `ar`, among them). Not configured; it follows from `languages`.","items":{"type":"string","pattern":"^[a-z]{2}$"}},"translationGaps":{"type":"array","readOnly":true,"description":"Content lacking a version in an enabled language.","items":{"type":"object","properties":{"language":{"type":"string"},"missingCount":{"type":"integer"},"areas":{"type":"array","items":{"type":"string"}}}}}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MinimumAppVersion": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n","properties":{"ios":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"},"android":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"}}},
"ModuleKey": {"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"NavigationConfig": {"x-ticvai-persistence":"whitelabel.navigation_config + whitelabel.navigation_item","x-ticvai-retired-columns":["whitelabel.navigation_item.navigation_item_id"],"type":"object","description":"**The mobile tab set is venue configuration (decided 29 September, MOB-1; 29 September brief decision 6).** Before a tenant saves its own, `bottomNavigation` is Home, Explore, Plan and Tickets (each an `appSection` link), with the Buy tickets button beside them; Map is an optional tab. Plan is left out while `visitPlanner` is off.\n","required":["kind","items"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"kind":{"type":"string","enum":["bottomNavigation","drawer","tabs"]},"items":{"type":"array","maxItems":12,"items":{"type":"object","required":["label","target","isVisible","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"label":{"$ref":"#/components/schemas/LocalisedText"},"icon":{"type":"string"},"target":{"$ref":"#/components/schemas/LinkTarget"},"isVisible":{"type":"boolean","description":"At most five may be visible in bottom navigation; the rest overflow."},"sortOrder":{"type":"integer"}}}},"buyButton":{"type":"object","nullable":true,"description":"**The persistent Buy tickets button (decided 29 September, MOB-2).** On every screen of the mobile app except the booking and checkout steps; it opens GST-003. Read with `bottomNavigation`.\n","properties":{"style":{"type":"string","enum":["raised","floating","flat","hidden"],"default":"raised","description":"`raised` sits in the centre of the tab bar, as the v4 prototype shows; `hidden` turns it off."},"label":{"$ref":"#/components/schemas/LocalisedText"}}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Performance": {"x-ticvai-persistence":"catalogue.performance","type":"object","required":["id","eventId","startsAt","endsAt","status"],"properties":{"id":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"description":"BL-048. **The approval chain and the occurrence lifecycle sat on different entities**, so neither was complete: `states/performance.yaml` models scheduled, onSale, soldOut, suspended, cancelled and completed properly, and nothing said which of those transitions somebody had to sign.\n**Set on the transition that needs it, not on the performance.** Publishing a performance is routine; cancelling one that has sold is the act somebody signs — and binding approval to the whole entity would have required a signature to reschedule a wet Tuesday.\n"},"requiresApprovalToCancel":{"type":"boolean","default":true,"description":"**Cancelling a sold performance is the one transition that needs a name against it.** `assessProductChange` already answers how many tickets are affected; this decides who has to look at that number before the button works.\n"},"status":{"type":"string","enum":["scheduled","onSale","soldOut","suspended","cancelled","completed"]},"admissionRulesId":{"type":"string","format":"uuid","nullable":true},"seatMapId":{"type":"string","format":"uuid","nullable":true},"language":{"type":"string","nullable":true,"maxLength":35,"pattern":"^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$","description":"The language the performance is given in, as a BCP 47 tag (`en`, `ar`, `fr`, `de`, `zh`, `ru`, `ar-AE`). **A guided tour at 10:00 in French and one at 10:00 in Arabic are two performances**, so a guest who picks a language sees only the tours in it (`listPerformances` `language`). Null when the performance is not language-specific (decided 29 September, rev 3 REV3-17).\n"},"format":{"type":"string","nullable":true,"maxLength":40,"description":"How it is presented, free text the venue chooses, e.g. `2D`, `3D`, `IMAX`, `subtitled`. A cinema screening shows language and format together. Null when it does not apply (decided 29 September, rev 3 REV3-17).\n"}}},
"PerformanceAvailability": {"type":"object","x-ticvai-persistence":"none — computed on read from catalogue.channel_capacity and live leases","description":"Remaining capacity of one channel capacity of one performance (rev 3 REV3-1).","required":["channelCapacityId","performanceId","capacity","sold","leased","remaining"],"properties":{"channelCapacityId":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid","description":"The performance this channel capacity belongs to (`ChannelCapacity.performanceId`), so rows for several performances can be told apart."},"startsAt":{"type":"string","format":"date-time","readOnly":true,"description":"The performance's start, so a time tile and its day part (morning, afternoon, evening, split at the venue's `BookingFlowConfig.dayPartBoundaries`) come from this one call (rev 3 REV3-1)."},"capacity":{"type":"integer"},"sold":{"type":"integer"},"leased":{"type":"integer","description":"Held by terminals but not yet sold."},"remaining":{"type":"integer"},"byChannel":{"type":"array","description":"Per-channel position. A guest seeing sold out online while units remain at the counter is correct behaviour, not a defect.\n","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/Channel"},"allocated":{"type":"integer"},"sold":{"type":"integer"},"remaining":{"type":"integer"}}}}}},
"PerformanceAvailabilityPage": {"x-ticvai-persistence":"none — computed on read","description":"The `getAvailability` answer (named 29 September, rev 3 REV3-1).","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Page"},{"type":"object","properties":{"items":{"type":"array","items":{"$ref":"#/components/schemas/PerformanceAvailability"}}}}]},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true},"eventId":{"type":"string","format":"uuid","nullable":true,"description":"**The event this product sells admission to** (4 October 2026, CHG-FXC-011; WEB-002, WEB-004): a product page finds its event and the event's performances (`Performance.eventId`) give it dates. Null for a product not tied to an event (merchandise, a pass, a membership)."}}},
"ProductCategory": {"type":"object","x-ticvai-persistence":"catalogue.product_category","description":"Retail Board 2 of the client's design set, 20 August. **`listSeatCategories` existed and a product category did not** — a seat category prices a seat, and a merchandise hierarchy groups a catalogue.\n**Brand sits here rather than as its own entity.** A venue with four brands and a hierarchy five levels deep can express that with a parent; a venue with one brand should not have to maintain a table containing one row.\n**`displayOrder` is not alphabetical and that is the point.** A retail category list runs in the order the merchandiser wants a guest to see it, and sorting by name puts *Accessories* above *Apparel* forever.\n","required":["id","name","kind"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"code":{"type":"string","maxLength":64,"nullable":true,"x-ticvai-unique":"tenant","description":"**Taken from their category tables, 20 September.** Ours had a uuid and a localised name, so an importer matching *Beverages* had to match on a display string that a venue is free to translate.\n**Unique per tenant where set** (decided 28 September, audit R108): two categories in one tenant never share a code, and `setProductCategories` refuses a body that would, with `409 duplicate-code`.\n"},"nameLocalised":{"type":"object","additionalProperties":{"type":"string"}},"kind":{"type":"string","enum":["category","brand","collection","season","department"]},"parentId":{"type":"string","format":"uuid","nullable":true,"description":"**One tree, not four.** A brand under a department under a category is how a real merchandise hierarchy runs, and separate tables for each level cannot express a venue that nests them differently.\n"},"scopePath":{"type":"string","readOnly":true,"description":"Set by the server from the venue the caller acts at; not sent."},"displayOrder":{"type":"integer","default":100},"imageAssetId":{"type":"string","format":"uuid","nullable":true},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The short line a guest reads under a category option, e.g. *Surf lessons: learn on the beginner wave with a coach* (decided 29 September, rev 3 REV3-19). Each language value at most 200 characters.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow for every product filed here** that names none of its own (decided 29 September, W12, BO-115). Null means the venue's flow for each product's `kind`. A white-label `BookingFlow` of the venue; `setProductCategories` refuses any other id with `422`.\n"},"isActive":{"type":"boolean","default":true,"description":"**Deactivated rather than deleted.** A category with a season behind it still names the products sold under it, and removing it rewrites last year's report.\n"}}},
"ProductCategoryNode": {"x-ticvai-persistence":"none — projection over catalogue.product_category","description":"**One node of the tree `listProductCategories` returns.** A `ProductCategory` with its children nested under it, in `displayOrder`, so no caller reassembles the hierarchy from `parentId`. `setProductCategories` still takes the flat list, because a write names each parent by id.\n","allOf":[{"$ref":"#/components/schemas/ProductCategory"},{"type":"object","required":["children"],"properties":{"children":{"type":"array","description":"Empty on a leaf.","items":{"$ref":"#/components/schemas/ProductCategoryNode"}}}}]},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductEligibilityRule": {"type":"object","x-ticvai-persistence":"catalogue.product_eligibility_rule","description":"Participation limits for one product. Absent means anyone may take part, and `getProductEligibilityRule` returns that absence as this schema with every limit null, never as a `404`.","properties":{"id":{"type":"string","format":"uuid","readOnly":true},"productId":{"type":"string","readOnly":true},"minAgeYears":{"type":"integer","minimum":0,"nullable":true},"maxAgeYears":{"type":"integer","minimum":0,"nullable":true},"minHeightCm":{"type":"integer","minimum":50,"maximum":250,"nullable":true},"maxHeightCm":{"type":"integer","minimum":50,"maximum":250,"nullable":true},"heightBandsCm":{"type":"array","items":{"type":"integer"},"default":[120,140],"description":"Band edges the guest chooses between, e.g. under 1.20 m, 1.20–1.40 m, 1.40 m and over."},"accompaniedBelowAge":{"type":"integer","nullable":true,"description":"Under this age an adult must be present, e.g. 8 at the kids club."},"guardianSignatureAgeFrom":{"type":"integer","nullable":true},"guardianSignatureAgeTo":{"type":"integer","nullable":true,"description":"Ages needing a guardian's signature, e.g. 12–15 on a thrill ride."},"waiverRequired":{"type":"boolean","default":false},"swimAbility":{"type":"string","enum":["notRequired","confident"],"default":"notRequired","deprecated":true,"description":"**Superseded for the guest's answer** (decided 29 September, rev 3 REV3-26): the swim question is a consent, not a data field. A venue attaches *Are you able to swim?* as a consent question (`Product.consentQuestionIds`), with its own text, version and whether it is asked per person or once per booking, and the answer is a consent record. Kept so existing rules read; a new product should use a consent question instead.\n"},"refundableIfIneligibleAtGate":{"type":"boolean","default":false},"requiredCertificationCode":{"type":"string","nullable":true,"maxLength":60,"description":"**A certification the participant must hold** (decided 29 September, W4; added 30 September), e.g. `padiOpenWater` for a dive. Null means none. Help me choose reads it: an answer whose `filter.certificationCode` names it with `holdsCertification: false` leaves the product out, and with `holdsCertification: true` (or no flag) keeps only products needing that certification or none. Proof, where the venue asks for it, is a consent question on the product (REV3-26), not this field."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"PublishedAnalyticsProvider": {"x-ticvai-persistence":"none — the enabled rows of whitelabel.analytics_provider, guest-facing fields only","description":"**What the tag loader needs and nothing else** (CHG-GCF-005): no reporting property, no credential, no venue or scope. The values are those of `StorefrontAnalyticsProvider`.","type":"object","required":["provider","measurementId","surfaces","consentCategory"],"properties":{"provider":{"type":"string","enum":["googleAnalytics4","googleTagManager","adobeAnalytics","metaPixel","matomo","other"]},"otherProviderName":{"type":"string","maxLength":100,"nullable":true,"description":"The provider's name, when `provider` is `other` (`StorefrontAnalyticsProvider.providerLabel`)."},"measurementId":{"type":"string","maxLength":100,"description":"What the tag or SDK reports to (GA4 `G-...`, Tag Manager `GTM-...`, a pixel id)."},"surfaces":{"type":"array","minItems":1,"items":{"type":"string","enum":["guestWeb","guestApp"]}},"consentCategory":{"type":"string","enum":["functional","analytics","personalisation","marketing"],"description":"The cookie category the visitor must grant before this provider loads (marketing-crm `CookieCategory`)."}}},
"PublishedTenantConfig": {"x-ticvai-persistence":"none — computed from the current ConfigVersion snapshot and the live status on whitelabel.tenant_config","type":"object","x-ticvai-agreed":"2 October: decided by Chinmay, fix before Block A starts (GFIX-1)","description":"**The public view of the tenant's configuration** (`getPublishedTenantConfig`, decided 2 October, GFIX-1). The published parts a guest surface renders with, from the current `ConfigVersion`, and the live status `setMaintenanceMode` writes. Nothing a guest cannot see on the page: no draft marker, no CMS counts, no sender addresses, no licensing, no person.\n","required":["tenantId","publishedVersion","publishedAt","isInMaintenance"],"properties":{"tenantId":{"type":"string","format":"uuid"},"publishedVersion":{"type":"string","description":"The `ConfigVersion.version` this answer was read from; a client holding the same version keeps its copy."},"publishedAt":{"type":"string","format":"date-time"},"brand":{"$ref":"#/components/schemas/BrandIdentity"},"appIcons":{"$ref":"#/components/schemas/AppIcons"},"theme":{"$ref":"#/components/schemas/Theme"},"fonts":{"$ref":"#/components/schemas/FontConfig"},"header":{"$ref":"#/components/schemas/HeaderConfig"},"footer":{"$ref":"#/components/schemas/FooterConfig"},"navigation":{"$ref":"#/components/schemas/NavigationConfig"},"homepage":{"$ref":"#/components/schemas/HomepageLayout"},"bookingFlow":{"allOf":[{"$ref":"#/components/schemas/BookingFlowConfig"}],"description":"The booking-flow display settings, resolved for `venueId` when one was sent (the tenant's values with that venue's `venueOverrides` entry laid over, rev 3 CFG-11)."},"languages":{"$ref":"#/components/schemas/LanguageConfig"},"accessibility":{"$ref":"#/components/schemas/AccessibilitySettings"},"enabledModules":{"type":"array","description":"The modules the tenant has enabled and published, so a guest surface hides a tab or a homepage section for a module that is off. Licensing is not shown.","items":{"$ref":"#/components/schemas/ModuleKey"}},"enabledFeatures":{"type":"array","description":"The `featureKey` of every feature toggle that is on in the published version.","items":{"type":"string"}},"isInMaintenance":{"type":"boolean","description":"Live state (`setMaintenanceMode`), as on `getTenantAppStatus`."},"maintenanceMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"$ref":"#/components/schemas/MinimumAppVersion"},"availability":{"$ref":"#/components/schemas/AppAvailability"},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"contact":{"$ref":"#/components/schemas/VenueContact"},"analyticsProviders":{"type":"array","description":"**The analytics platforms the storefront and app load** (Chinmay, 3 October 2026, Pattern 4; CHG-GCF-005): a guest reads them here instead of `listAnalyticsProviders`, which needs `TENANT_CONFIGURE`. The enabled `StorefrontAnalyticsProvider` rows in force for the venue being browsed (that venue's own rows when `venueId` was sent and it has any, else the tenant-wide ones), read live, with only what the tag loader needs. **A provider loads only once marketing-crm `getCookieConsentRuntime` says its `consentCategory` is granted**; before that nothing is sent to it (2.6.58).","items":{"$ref":"#/components/schemas/PublishedAnalyticsProvider"}},"paymentTokenisation":{"type":"object","nullable":true,"description":"**The provider the guest app tokenises cards with** (4 October 2026, CHG-FXC-010; GST-071): the `providerId` `storePaymentToken` requires, its kind and the publishable key the client SDK needs. Never a secret. Null where no provider with tokenisation is connected.","required":["providerId","providerKind"],"properties":{"providerId":{"type":"string","format":"uuid"},"providerKind":{"type":"string"},"publishableKey":{"type":"string","nullable":true}}}}},
"QueueStatus": {"type":"string","enum":["open","paused","closed","atCapacity"]},
"RecordDeviceConsentRequest": {"type":"object","x-ticvai-persistence":"none — request only","description":"What the banner or preference centre sends to `recordDeviceConsent`.","required":["channel","action","noticeVersion","decidedAt"],"properties":{"consentKey":{"type":"string","maxLength":64,"nullable":true,"description":"The key the browser or app already holds; omitted on a first decision, and one is minted."},"channel":{"$ref":"#/components/schemas/CookieConsentChannel"},"brandId":{"type":"string","format":"uuid","nullable":true},"bannerDesignId":{"type":"string","format":"uuid","nullable":true},"action":{"$ref":"#/components/schemas/DeviceConsentAction"},"categories":{"type":"array","description":"Required for `savePreferences`; ignored for the other actions, which decide every category themselves.","items":{"type":"object","required":["category","decision"],"properties":{"category":{"$ref":"#/components/schemas/CookieCategory"},"decision":{"type":"string","enum":["granted","declined"]}}}},"noticeVersion":{"type":"string"},"language":{"type":"string","maxLength":10,"nullable":true},"globalPrivacyControl":{"type":"boolean","default":false},"source":{"$ref":"#/components/schemas/ConsentSource"},"decidedAt":{"type":"string","format":"date-time"}}},
"TenantAppStatus": {"x-ticvai-persistence":"none — computed","type":"object","description":"Computed on read. The published fields come from the current `ConfigVersion`, the maintenance fields from the tenant's `tenant_config` row (`setMaintenanceMode`), and the draft fields from the working draft. **Fields marked staff only are left out of a response to a caller without a staff session** (`getTenantAppStatus`).\n","required":["tenantId","isPublished","isInMaintenance"],"properties":{"tenantId":{"type":"string","format":"uuid"},"isPublished":{"type":"boolean","x-ticvai-derived":"onRead","description":"True once any version has been published."},"publishedVersion":{"type":"string","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"draftVersion":{"type":"string","description":"Staff only."},"hasUnpublishedChanges":{"type":"boolean","x-ticvai-derived":"onRead","description":"Staff only. The working draft differs from the current version's `snapshot`."},"activeModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isEnabled` true."},"licensedModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isLicensed` true."},"activePageCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. Content pages that are `published` and enabled."},"isInMaintenance":{"type":"boolean"},"maintenanceMessage":{"$ref":"#/components/schemas/LocalisedText"},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"$ref":"#/components/schemas/MinimumAppVersion"},"contact":{"$ref":"#/components/schemas/VenueContact"},"availability":{"$ref":"#/components/schemas/AppAvailability"},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"What the sold-out or closed screen says (WEB-029). Null shows the default wording."},"venues":{"type":"array","maxItems":200,"x-ticvai-derived":"onRead","description":"**Public: the venues a guest can pick** (decided 28 September, audit R267; schema named 29 September, readiness close-out, our build plan). The source of the venue picker on WEB-001 and GST-001, returned with or without a session. **Published only**: a venue is listed when its scope node is active (`tenancy.OrgUnit.isActive`) and it is in the tenant's current published `ConfigVersion`; a venue added or reactivated since the last publish appears after the next publish, and a draft never reaches a guest. Ordered by `name`. Empty when nothing is published.\n","items":{"type":"object","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid","description":"**The venue's scope node** (`tenancy.OrgUnit.id`, level venue): what every guest screen that declares `venueId` `from: session` reads once the guest picks it."},"name":{"type":"string","maxLength":200,"description":"The venue's name (`tenancy.OrgUnit.name`)."},"city":{"type":"string","maxLength":120,"nullable":true,"description":"Shown under the name so two venues with similar names can be told apart."},"openingHoursToday":{"type":"object","nullable":true,"description":"Today's opening hours in the venue's time zone, from `tenancy.VenueSettings` opening hours. Null when the venue is closed today or has none set.","properties":{"opens":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"},"closes":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"}}}}}},"whatsNew":{"type":"array","maxItems":10,"x-ticvai-derived":"onRead","description":"**Public: the guest \"what's new\"** (decided 29 September, rev 3 GAP-B2). Newest first, at most 10, from `platform-ops.Release.guestReleaseNotes` of the releases the tenant's cell has received; a release with no guest notes is skipped. Returned with or without a staff session.\n","items":{"type":"object","required":["version","publishedAt","notes"],"properties":{"version":{"type":"string","description":"The release version."},"publishedAt":{"type":"string","format":"date-time","description":"When the release reached the tenant's cell."},"notes":{"$ref":"#/components/schemas/LocalisedText"}}}},"recentChanges":{"type":"array","description":"Staff only. Names the principal behind each change, so it never reaches a public response.","items":{"type":"object","properties":{"area":{"type":"string"},"description":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"}}}}}},
"Theme": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","x-ticvai-contrast-pairs":[{"foreground":"textColour","background":"backgroundColour","use":"text","ratio":4.5},{"foreground":"textColour","background":"backgroundColour","use":"largeText","ratio":3.0},{"foreground":"primaryColour","background":"backgroundColour","use":"nonText","ratio":3.0},{"foreground":"secondaryColour","background":"backgroundColour","use":"nonText","ratio":3.0},{"foreground":"accentColour","background":"backgroundColour","use":"nonText","ratio":3.0},{"foreground":"componentColours.*.text","background":"componentColours.*.background","use":"text","ratio":4.5},{"foreground":"componentColours.*.background","background":"backgroundColour","use":"nonText","ratio":3.0}],"required":["primaryColour","secondaryColour","backgroundColour","textColour"],"properties":{"primaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"secondaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"accentColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"textColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"darkMode":{"type":"object","deprecated":true,"description":"**Deprecated and ignored** (Chinmay, 2 October, workbook Q150 and the pre-apply round; CHG-CSA-035). White label has no dark or light mode: the venue's chosen theme is applied, on every device setting. The field is kept so a client built at r1 still parses, is accepted on `setTheme` and returned as stored, and **is never used to render anything or drawn on any screen**; the guest app has no Light/Dark switch.","properties":{"primaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"textColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},"cornerRadius":{"type":"integer","minimum":0,"maximum":32,"description":"The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). Its named palettes, font pairs and background tones are presets over the colours here and `FontConfig`, not stored values."},"surfaceStyle":{"type":"string","enum":["glass","solid"],"default":"glass","description":"Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3)."},"buttonStyle":{"type":"string","enum":["solid","outline","pill"],"default":"solid","description":"Button shape (decided 29 September, rev 3 CFG-3)."},"componentColours":{"type":"object","description":"**Colours for single interactive elements (decided 17 September, M17-11).** Each is optional and falls back to the theme colours. Every pair passes the same contrast check as the theme (`ContrastProblem`), or `setTheme` refuses it with 400. The guest flow stays the standard one; only the colours change.\n","properties":{"primaryCta":{"$ref":"#/components/schemas/ThemeComponentColour"},"payButton":{"$ref":"#/components/schemas/ThemeComponentColour"},"addToCart":{"$ref":"#/components/schemas/ThemeComponentColour"},"buyTicketsButton":{"$ref":"#/components/schemas/ThemeComponentColour"},"link":{"$ref":"#/components/schemas/ThemeComponentColour"},"badge":{"$ref":"#/components/schemas/ThemeComponentColour"}}}}},
"VenueContact": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n","properties":{"phone":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true},"whatsapp":{"type":"string","nullable":true},"address":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Prose, as the guest reads it. The bookable hours are the catalogue's."}}},
"VisitPlan": {"type":"object","x-ticvai-persistence":"venuemap.visit_plan","description":"**A guest's visit plan** (29 September, MOB-6): the Plan tab. One row per plan; its items are `venuemap.visit_plan_item` rows carrying the version they belong to, so every earlier version stays readable and undo is a new version equal to an old one. **Owned by the guest session**, like a cart: `subjectId` when signed in, `sessionRef` for an anonymous device session, claimed on sign-in.\n","required":["id","venueId","status","version","days"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","readOnly":true,"description":"Derived from `venueId`."},"subjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"marketing.guest_profile","description":"The signed-in guest. From the session, never from the body."},"sessionRef":{"type":"string","nullable":true,"readOnly":true,"description":"The anonymous device session that owns the plan until sign-in."},"ownership":{"type":"string","enum":["anonymous","account"],"readOnly":true,"description":"`anonymous` while the plan belongs to a device session (built and changed only; it lapses with the session), `account` once the guest signed in and the plan moved to their account, where it is saved and can be shared and booked (CHG-RUL-003).\n"},"status":{"type":"string","enum":["draft","booked","archived"],"readOnly":true,"description":"`booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date."},"version":{"type":"integer","minimum":1,"readOnly":true,"description":"The current version. Every `updateVisitPlan` adds one."},"source":{"type":"string","enum":["rules","preset","aiAgent"],"readOnly":true,"description":"What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. **The guest sees which**, as every AI answer says what it is based on.\n"},"inputs":{"$ref":"#/components/schemas/VisitPlanRequest"},"mapVersion":{"type":"integer","readOnly":true,"description":"The published map version the plan was laid out on."},"cartId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"orders.cart","description":"The cart `bookVisitPlan` filled."},"excluded":{"type":"array","readOnly":true,"description":"**What was left out and why**, e.g. a coaster excluded because one of the party is under its 120 cm minimum. Shown on GST-053, so the planner never looks as if it forgot.\n","items":{"type":"object","properties":{"pointId":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","enum":["heightRule","ageRule","closedOnDate","notInInterests","noTime","notAtVenue"],"description":"`notAtVenue` (30 September, MoM 4.7): a must-include point that is at none of the plan's venues, so no day could hold it.\n"}}}},"unmatchedPreferences":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"**A preference a day's venue cannot meet is said, never faked** (30 September client meeting, MoM 4.7, Allam's requirement). One entry per day and preference that no point of that day's venue matches: a cuisine (`cuisineTags`), a shop (`retailTags`) or an interest (`interestTags`). `availableAtVenueIds` names the tenant's other active venues whose published map does match, so GST-053 and WEB-050 can say *Indian food is at the other park (day 2)* instead of quietly placing a restaurant the party cannot reach. Empty when every preference is met on every day. Worked out on read for the version read (a swap can meet or lose a preference), never stored.\n","items":{"type":"object","required":["date","venueId","preference","tag"],"properties":{"date":{"type":"string","format":"date"},"venueId":{"type":"string","format":"uuid","description":"The day's venue, which has no match."},"preference":{"type":"string","enum":["cuisine","retail","interest"]},"tag":{"type":"string","maxLength":30},"availableAtVenueIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Other active venues of the tenant where the tag is matched. Empty when none is."}}}},"days":{"type":"array","readOnly":true,"description":"One per date, in order. The items of the version read.","items":{"type":"object","required":["date","venueId","items"],"properties":{"date":{"type":"string","format":"date"},"venueId":{"type":"string","format":"uuid","description":"**The venue this day is planned at** (30 September, MoM 4.7): `VisitPlanRequest.dayVenues` for the date, else `venueId`. Every item of the day is at this venue.\n"},"opensAt":{"type":"string","nullable":true},"closesAt":{"type":"string","nullable":true},"items":{"type":"array","items":{"$ref":"#/components/schemas/VisitPlanItem"}}}}},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"VisitPlanAlternative": {"type":"object","x-ticvai-persistence":"none — computed on read","description":"One candidate for a swap (29 September, MOB-6).","required":["kind","venueId","startsAt","reason"],"properties":{"kind":{"type":"string","enum":["attraction","show","meal","shop","rest"]},"venueId":{"type":"string","format":"uuid","description":"The item's day venue; an alternative is never from another venue (30 September, MoM 4.7)."},"pointId":{"type":"string","format":"uuid","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"name":{"type":"string"},"startsAt":{"type":"string","format":"date-time"},"durationMinutes":{"type":"integer"},"walkMinutes":{"type":"integer","nullable":true},"expectedWaitMinutes":{"type":"integer","nullable":true},"matchedInterests":{"type":"array","items":{"type":"string"}},"reason":{"type":"string","description":"Why it is offered, in words the sheet shows, e.g. *Same thrill level, 4 minutes closer*."}}},
"VisitPlanBooking": {"type":"object","x-ticvai-persistence":"none — computed; the lines are orders.cart_line rows","description":"What `bookVisitPlan` returns (29 September, MOB-6): the cart handoff.","required":["planId","cartId","added","notAdded"],"properties":{"planId":{"type":"string","format":"uuid"},"cartId":{"type":"string","format":"uuid"},"added":{"type":"array","items":{"type":"object","properties":{"itemId":{"type":"string","format":"uuid"},"cartLineId":{"type":"string","format":"uuid"},"leaseExpiresAt":{"type":"string","format":"date-time","nullable":true}}}},"notAdded":{"type":"array","description":"Items that could not be added, with the `addCartLine` refusal each met.","items":{"type":"object","properties":{"itemId":{"type":"string","format":"uuid"},"reason":{"type":"string","description":"The orders `CartProblem` code, e.g. `soldOutForSession`, `productInfoOnly`, `seatLimitExceeded`."}}}},"freeItems":{"type":"integer","description":"Stops that need nothing bought."}}},
"VisitPlanItem": {"type":"object","x-ticvai-persistence":"venuemap.visit_plan_item","description":"**One timed stop on a plan day** (29 September, MOB-6). Rows are kept per `planVersion`: a change writes the day's items again under the new version, and an older version's rows are never updated.\n","required":["id","planId","planVersion","date","sequence","kind","startsAt","endsAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"planId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"venuemap.visit_plan"},"planVersion":{"type":"integer","minimum":1,"readOnly":true},"date":{"type":"string","format":"date"},"sequence":{"type":"integer","minimum":1},"kind":{"type":"string","enum":["attraction","show","meal","shop","rest","travel"],"description":"`meal` is a stop at a dining point (restaurant, cafe or food kiosk); `shop` is a retail stop at a shop or a retail kiosk (30 September client meeting, MoM 4.7: retail is placed from the day venue's own points, as dining is).\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"**The venue of this stop** (30 September client meeting, MoM 4.7): always the day's venue, and the venue whose map `pointId` is on. Carried on the item so the screens, `bookVisitPlan` and the AI planner agent read it rather than infer it. **Worked out on read, not stored**: from the plan's `inputs` (`dayVenues` for the item's date, else `venueId`). A stored `venue_id` would move the item rows from the plan's own row-level policy to a venue policy and hide a second park's items from the guest who owns the plan.\n"},"pointId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"venuemap.point"},"productId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"catalogue.product","description":"What is bought for this stop, where it is bought. Null for a free stop."},"bundleId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"promotions.bundle","description":"A meal combo or package, from the point's `featuredOffer`."},"performanceId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"catalogue.performance"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"walkMinutesBefore":{"type":"integer","minimum":0,"nullable":true},"expectedWaitMinutes":{"type":"integer","minimum":0,"nullable":true,"description":"The typical wait at that hour when the plan was laid out; GST-059 replaces it with the live one."},"addOnSuggestion":{"type":"object","nullable":true,"description":"A suggested add-on for this stop, e.g. Fast Track where the wait is long. Never added by itself.","properties":{"productId":{"type":"string","format":"uuid"},"reason":{"type":"string"}}},"addOnAccepted":{"type":"boolean","default":false},"addOnProductIds":{"type":"array","readOnly":true,"description":"Add-ons the guest put on this stop with `addAddOn` (CHG-RUL-009), beside an accepted suggestion, as catalogue product ids. No price: priced at booking.\n","items":{"type":"string","format":"uuid"}},"pinned":{"type":"boolean","default":false,"description":"The guest fixed this stop; a re-lay moves other stops around it."},"note":{"type":"string","nullable":true,"maxLength":200}}},
"VisitPlanRequest": {"type":"object","x-ticvai-persistence":"none — request only; kept as `inputs` on venuemap.visit_plan","description":"What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050.\n","required":["venueId","dates","party"],"properties":{"venueId":{"type":"string","format":"uuid","description":"The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. Every date is planned at this venue unless `dayVenues` puts it somewhere else.\n"},"dayVenues":{"type":"array","maxItems":7,"description":"**Which venue on which date, in a multi-venue tenant** (30 September client meeting, MoM 4.7, Allam's requirement). One entry per date that is not at `venueId`; each date of `dates` at most once. Each venue must be an active venue of the caller's tenant (the options `getTenantAppStatus.venues` lists), else 422 `venue-not-in-tenant`. **Each day is then planned from that venue's own published map only**: its rides, its dining and its retail points, never another venue's.\n","items":{"type":"object","required":["date","venueId"],"properties":{"date":{"type":"string","format":"date"},"venueId":{"type":"string","format":"uuid"}}}},"dates":{"type":"array","minItems":1,"maxItems":7,"items":{"type":"string","format":"date"}},"party":{"type":"array","minItems":1,"maxItems":20,"description":"One entry per person. **Height where the guest knows it, age otherwise**: height is what ride eligibility rules test, and an age band is the fallback the rule may also state. Nothing here identifies a person.\n","items":{"type":"object","properties":{"heightCm":{"type":"integer","minimum":40,"maximum":230,"nullable":true},"ageYears":{"type":"integer","minimum":0,"maximum":120,"nullable":true}}}},"pace":{"type":"string","enum":["packed","relaxed"],"default":"relaxed"},"interestTags":{"type":"array","maxItems":12,"description":"The same closed list as `VenuePoint.interestTags`.","items":{"type":"string"}},"cuisineTags":{"type":"array","maxItems":8,"description":"Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). A cuisine no dining point of the day's venue serves is not forced into the day; it is reported in `VisitPlan.unmatchedPreferences`.\n","items":{"type":"string"}},"retailTags":{"type":"array","maxItems":8,"description":"**Shops the party would like to visit** (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options), e.g. `souvenirs`, `toys`, `apparel`, `essentials`. Matched per day against `VenuePoint.retailTags` of that day's venue's shops and retail kiosks; an unmatched tag is reported, as a cuisine is.\n","items":{"type":"string","maxLength":30}},"mustIncludePointIds":{"type":"array","maxItems":10,"description":"Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never placed on another venue's day.\n","items":{"type":"string","format":"uuid"}},"preset":{"type":"string","nullable":true,"enum":["highlights","family","thrillSeeker","waterDay","relaxed","showsAndDining"],"description":"A ready-made day plan (GST-052 Suggested Itineraries): the preset fixes the interests and the pace, and the party still decides eligibility.\n"},"presetKey":{"type":"string","nullable":true,"maxLength":64,"pattern":"^[a-z][a-zA-Z0-9]*$","description":"The ready-made plan the guest took on GST-052 (30 September, second wave of the 29 September pass, MOB-6): one of the built-in `preset` keys above, or a key of a ready-made plan the venue defines. **The same rules planner runs**: the preset only supplies interests, pace and must-include points, and the party still decides eligibility. When both `preset` and `presetKey` are sent they must name the same plan; `presetKey` is the field new clients send. An unknown key is refused 422 `unknown-preset`.\n"},"startTime":{"type":"string","nullable":true,"pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"When the party arrives. Null means opening time."},"locale":{"type":"string","nullable":true}}},
"VisitPlanUpdate": {"type":"object","x-ticvai-persistence":"none — request only; lands as a new version of venuemap.visit_plan_item rows","description":"What `updateVisitPlan` takes (29 September, MOB-6).","required":["baseVersion","changes"],"properties":{"baseVersion":{"type":"integer","minimum":1},"changes":{"type":"array","minItems":1,"maxItems":20,"items":{"type":"object","required":["op"],"properties":{"op":{"type":"string","enum":["swap","remove","add","move","pin","acceptAddOn","declineAddOn","addAddOn","removeAddOn","revertTo"]},"itemId":{"type":"string","format":"uuid","nullable":true},"date":{"type":"string","format":"date","nullable":true},"pointId":{"type":"string","format":"uuid","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"startsAt":{"type":"string","format":"date-time","nullable":true},"addOnProductId":{"type":"string","format":"uuid","nullable":true,"description":"For `addAddOn` and `removeAddOn` (CHG-RUL-009): the add-on product (a catalogue product sold for the item's stop, e.g. Fast Track). Priced at booking, not here.\n"},"version":{"type":"integer","nullable":true,"description":"For `revertTo`, the earlier version to restore (undo)."}}}}}},
"WaitTime": {"x-ticvai-persistence":"none — computed from readings and throughput","type":"object","required":["queueId","waitMinutes","source","asOf","isStale"],"properties":{"queueId":{"type":"string","format":"uuid"},"queueName":{"$ref":"#/components/schemas/LocalisedText"},"attractionProductId":{"type":"string","format":"uuid","nullable":true},"attractionCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. Read from catalogue, not stored here.\n"},"status":{"$ref":"#/components/schemas/QueueStatus"},"waitMinutes":{"type":"integer","nullable":true,"description":"Null where the queue is closed or no estimate is available."},"source":{"$ref":"#/components/schemas/WaitTimeSource"},"isStale":{"type":"boolean","description":"The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as current, and it is not hidden (decided 28 September, audit R080 (b)): the screen shows `waitMinutes` with its `asOf` and a stale marker.\n"},"heightRequirementCm":{"type":"integer","nullable":true},"zone":{"type":"string","nullable":true},"asOf":{"type":"string","format":"date-time","description":"When the figure was produced — the queue's `waitTimeAsOf`."}}},
"WaitTimeSource": {"type":"string","description":"Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed.\n","enum":["sensor","throughput","manual","unavailable"]},
"WhiteLabelStorefrontSessionBatch": {"type":"object","x-ticvai-persistence":"none — request only; published as storefront.sessionEvent through platform.outbox","description":"One beacon from the storefront or guest-app runtime (8.3.40; decided 29 September, build pass, group G2). **Closed shape** (`additionalProperties: false`): hashes, route families, product ids and counts only.","additionalProperties":false,"required":["batchId","sessionRef","surface","sessionStartedAt","interactions"],"properties":{"batchId":{"type":"string","format":"uuid","description":"UUIDv7 minted by the runtime; a retried beacon repeats it."},"sessionRef":{"type":"string","maxLength":128,"description":"The runtime's own session id, SHA-256 hashed in the browser; hashed again with the tenant key on arrival and published as `storefront.sessionEvent.sessionRef`. The checkout passes the same value to `ai.scoreTransactionRisk`."},"deviceIdHash":{"type":"string","maxLength":128,"nullable":true},"surface":{"type":"string","enum":["guestWeb","guestApp"]},"venueId":{"type":"string","format":"uuid","nullable":true},"sessionStartedAt":{"type":"string","format":"date-time"},"interactions":{"type":"array","minItems":1,"maxItems":50,"items":{"type":"object","additionalProperties":false,"required":["kind","at"],"properties":{"kind":{"type":"string","enum":["pageView","productView","seatMapOpened","addToCart","removeFromCart","checkoutStarted","paymentPageViewed","promoCodeTried","search"]},"pageKind":{"type":"string","nullable":true,"enum":["home","product","seatMap","cart","checkout","account","content",null]},"productId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time"},"dwellMs":{"type":"integer","minimum":0,"nullable":true}}}},"automationHints":{"type":"object","nullable":true,"additionalProperties":false,"properties":{"webdriver":{"type":"boolean"},"headless":{"type":"boolean"},"pointerEvents":{"type":"integer","minimum":0},"interactionsPerMinute":{"type":"number","minimum":0}}}}}
}
```
