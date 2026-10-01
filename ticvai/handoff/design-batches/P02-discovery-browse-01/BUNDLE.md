# P02-discovery-browse-01 — P02 · Discovery & Browse

**7 screens · 23 operations · 65 schemas · 6 permissions**

Platform P02 Guest App · ships as **guest** ·
guest audience · mobileApp ·
offline-capable

## Who this is for

**guest on mobileApp.** Everything below is how you know what is
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
  `AI_USE, GUEST_VIEW, ORDER_VIEW, PRODUCT_VIEW, TENANT_CONFIGURE, VENUE_MAP_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **14 of these operations work offline**: getBundle, getPerformance, getProduct, getPublishedGuidedChoice, getPublishedTenantConfig, getTenantAppStatus, getVenueMap, getWaitTimes
  — and the rest do not. A surface that looks the same online and off is lying.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
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
| `GST-001` | Home | A | 2 | 111 | 7 | 62 | 6 | 0 | guest | notStarted (client-verified) |
| `GST-002` | Explore | A | 1 | 44 | 6 | 15 | 4 | 0 | guest | notStarted (client-verified) |
| `GST-003` | Buy Tickets | A | 1 | 53 | 6 | 24 | 10 | 0 | guest | notStarted (client-verified) |
| `GST-004` | Item Detail | A | 1 | 103 | 8 | 29 | 11 | 0 | guest | notStarted (client-verified) |
| `GST-005` | What's On | A | 2 | 10 | 6 | 17 | 0 | 0 | guest | notStarted (client-verified) |
| `GST-006` | Item Detail – Event / Exhibition | A | 0 | 25 | 5 | 11 | 2 | 0 | guest | notStarted (client-verified) |
| `GST-057` | Accessibility Information | A | 0 | 4 | 6 | 0 | 2 | 0 | guest | notStarted (client-verified) |

## Thin screens in this batch

**GST-006, GST-057 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `GST-001` Home

**The Home tab: what this venue is, when it is open and what there is to do, with one or two highlights per type, from which everything else is entered.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Discovery & Browse · wave 1 · needs the `marketing` module |
| Block | Block A · ticket #17971 (APP-MOB-GST-001) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | listDetail (comfortable density): `listMyEntitlements` reads the population and `getTenantAppStatus` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `subjectId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. **The venue comes from the device** (decided 28 September, audit R267): on first open the guest … |
| Route | `/general/home-default` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Landing. **Declared only a health check.** Pranay asked for guest details and tickets; Chitrangi asked for search. All three existed and none were wired. **Rewired on the 20 August review.** **Venue selection added 28 September** (decided 28 September, audit R267) — a venue picker on first open, remembered on the device, **Change venue**, and a visit-day suggestion from the guest's ticket (`listMyEntitlements`). Nothing in `getTenantAppStatus.venues` supplies the options, the tenant's active venues, public and cacheable. **Rev 3 (decided 29 September).** The in-venue notifications feed (GST-030) is back in the first release (GAP-C1, reversing audit R242). A transport venue's home opens the trip search (GST-076, REV3-21). The venue picked here (audit R267) is the venue whose booking-flow settings apply; the booking screens' *Booking at* bar changes it (REV3-18). Every booking-flow setting named here is read from `getTenantConfig` `bookingFlow`, resolved for the venue the guest picked (audit R267): the tenant's values with that venue's `venueOverrides` entry laid over field by field (decided 29 September, rev 3 CFG-11). **Mobile v4 (decided 29 September, MOB-1, MOB-3, MOB-5).** Retitled **Home** and made the Home tab root: hero (carousel, video, poster or split), the venue overview (description, opening hours, info), type tiles and one or two highlights per type; tapping a highlight opens Item Detail …

**Known gaps.** Replaced by `getPublishedTenantConfig`, the guest read of the same data. Replaced by `getMyProfile`, the guest's own profile; `getGuestProfile` is the staff read by subject and returns the CRM fields (engagement score, lifetime value, tags).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Your venue | repeatable rows | optional | — | at most 200 | — | **The guest picks a venue on first open** (decided 28 September, audit R267): shown before anything else when the device has no venue remembered, and remembered on the device after that. The chosen … | `TenantAppStatus.venues` |
| Search the venue | search field | — | — | — | — | Opens Explore search (GST-063) with what was typed. | `searchCatalogue` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| State | radio group | Usable now | Usable now · Upcoming · Expired · All | `listMyEntitlements` ?state |
| Include shared | toggle | on | — | `listMyEntitlements` ?includeShared |
| Channel | select | — | B2C website · Customer portal · Mobile app · Embedded checkout · White label site · Partner microsite | `getCookieConsentRuntime` ?channel |
| Brand | picker: choose a brand | — | — | `getCookieConsentRuntime` ?brandId |
| Language | text field | — | max length 10 | `getCookieConsentRuntime` ?language |
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |

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

**Your upcoming tickets** (card list, from `listMyEntitlements`): Only when signed in: `listMyEntitlements` with `state=upcoming`, fixed by the screen. Was the generated table 'Every entitlement'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Product | the name it points at, never the id | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Resolved at issue from the template, then owned here. A freeze extends it, a reissue replaces it, and neither reaches back to the template. |
| Status | chip: Issued, Partially consumed, Fully consumed, Expired, Cancelled, Surrendered | What the storage layer holds, and what a guest is shown. `MediaEntitlements` carried only `isValid` and a reason string — a boolean cannot … |
| Entries used | 1,234 | The number `validateAccess` decrements and nothing was decrementing. A ten-entry pass with no counter is a ten-entry pass that admits … |
| Entries allowed | 1,234 | — |

**Hero** (banner, from `getPublishedTenantConfig`): The venue hero in the style the venue set on the Home section (`heroStyle`: carousel, video, poster or split). Video heroes stream; a missing asset falls back to the poster image.

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
| App icons | grouped details | — |
| Source image | the image or video | The `MediaAsset` id of the 1024×1024 source. |
| Derived | list or chips (count when long) | Generated by `setAppIcons` from the source, one entry per platform and size — the iOS and Android store sets and the web favicons listed on … |
| Platform | chip: Ios, Android, Web | — |
| Size | text | — |
| Asset ref | the image or video | — |

**Venue overview** (detail panel, from `getTenantAppStatus`): **Home is a venue overview** (MOB-3): the venue description, today's opening hours (from `getTenantAppStatus.venues`), getting here and before-you-go info.

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

**Type tiles** (card list, from `listProductCategories`): Rides, dining, events and shops (the venue's own categories). A tile opens Explore (GST-002) on that type.

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

**Highlights per type** (card list, from `listProducts`): One or two items per type (`HomepageLayout.sections[].maxItems`, 1-2, set on CMS-007); a highlight opens Item Detail.

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

**Your greeting** (detail panel, from `getMyProfile`): Only when signed in: the greeting by name. Engagement score, lifetime value and tags are staff CRM fields and never reach a guest (MATRIX 19.2.7; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Display name | text | — |
| Preferred language | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Change venue (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getTenantAppStatus` (onLoad, App status and recent changes); `getMyProfile` (onLoad, The signed-in guest's own name and language for the …); `listMyEntitlements` (onLoad, Every ticket, pass and membership this guest holds; on a …); `getPublishedTenantConfig` (onLoad, The published brand, theme, fonts, header, footer …); `getCookieConsentRuntime` (onLoad, Tracking consent prompt on first launch and the SDK gate); `listAnalyticsProviders` (onLoad, Analytics SDKs to start once their consent category is …); `decideRecommendations` (onLoad, Recommendation slot (homepage / loyalty placement …); `recordStorefrontSessionEvents` (onLoad, App-shell beacon of hashed browsing behaviour for fraud …); `listProducts` (onLoad, One or two highlights per type (rides, dining, events …); `listProductCategories` (onLoad, The type tiles on Home (rides, dining, events, shops))

**Where the user goes next**

- → `GST-002` Explore: *Explore Categories*
- → `GST-003` Buy Tickets: *Event & Attraction Listing*; carries `eventId`
- → `GST-004` Item Detail: *Attraction Details*; carries `productId`
- → `GST-005` What's On: *What's On*
- → `GST-006` Item Detail – Event / Exhibition: *Event / Exhibition Details*; carries `productId`
- → `GST-007` Select Date & Time: *Select Date & Time*; carries `eventId`
- → `GST-008` Tickets & Add-ons: *Tickets & Add-ons*; carries `productId`
- → `GST-009` Review & Payment: *Review & Payment*; carries `orderId`
- → `GST-010` Booking Confirmation: *Booking Confirmation*; carries `orderId`
- → `GST-011` Wallet Overview: *Wallet Overview*; carries `subjectId`
- → `GST-012` My Tickets: *My Tickets*; carries `entitlementId`, `orderId`
- → `GST-013` Ticket Details: *Ticket Details*; carries `entitlementId`, `orderId`
- → `GST-014` Ticket Transfer: *Ticket Transfer*; carries `orderId`
- → `GST-015` Memberships: *Memberships*; carries `subjectId`
- → `GST-016` My Reservations: *My Reservations*
- → `GST-017` Reservation Details: *Reservation Details*
- → `GST-018` Add to Calendar / Reminders: *Add to Calendar / Reminders*; carries `orderId`
- → `GST-019` Order History: *Order History*; carries `orderId`
- → `GST-020` Saved Items / Wishlist: *Saved Items / Wishlist*; carries `subjectId`
- → `GST-021` Interactive Map: *Interactive Map*
- → `GST-023` Virtual Queue: *Virtual Queue*
- → `GST-024` F&B – Browse & Order: *F&B – Browse & Order*; carries `orderId`
- → `GST-025` F&B – Order Tracking: *F&B – Order Tracking*; carries `orderId`
- → `GST-026` Retail / Merchandise: *Retail / Merchandise*
- → `GST-027` Parking – Reserve & Pay: *Parking – Reserve & Pay*; carries `entitlementId`
- → `GST-031` AI Concierge – Home: *AI Concierge – Home*
- → `GST-032` AI Concierge – Chat: *AI Concierge – Chat*; carries `orderId`
- → `GST-033` AI Concierge – Contextual Help: *AI Concierge – Contextual Help*
- → `GST-034` Lost & Found: *Lost & Found*; carries `orderId`
- → `GST-037` Offers & Promotions: *Offers & Promotions*
- → `GST-039` Profile: *Profile*; carries `subjectId`
- → `GST-040` Help & Support: *Help & Support*
- → `GST-041` Checkout Entry: *Checkout Entry*; carries `productId`
- → `GST-042` Simple Registration & OTP: *Simple Registration & OTP*; carries `subjectId`
- → `GST-045` Ticket Delivery & Sharing: *Ticket Delivery & Sharing*; carries `orderId`
- → `GST-049` Interactive Seat Selection: *Interactive Seat Selection*
- → `GST-052` Suggested Itineraries: *Suggested Itineraries*
- → `GST-054` AI Planner: *AI Optimized Itinerary*
- → `GST-055` Dynamic QR Ticket: *Dynamic QR Ticket*; carries `entitlementId`, `orderId`
- → `GST-056` Bundle Package: *Bundle Package*
- → `GST-059` Plan in Progress: *Plan My Day – In Progress*
- → `GST-061` Menu Item Detail: *Menu Item Detail*
- → `GST-070` Reserve a Table: *Reserve a Table*
- → `GST-022` Attraction Wait Times: *Attraction Wait Times*
- → `GST-028` Parking – Reservation Confirmed: *Parking – Reservation Confirmed*; carries `orderId`
- → `GST-029` Venue Info & Services: *Venue Info & Services*
- → `GST-030` In-Venue Notifications: *In-Venue Notifications*
- → `GST-035` Feedback & Ratings: *Feedback & Ratings*
- → `GST-036` Loyalty & Rewards: *Loyalty & Rewards*
- → `GST-038` At the Venue: *Digital Companion Mode*
- → `GST-043` Arabic / RTL Experience: *Arabic / RTL Experience*
- → `GST-044` Multi-Currency & Pricing: *Multi-Currency & Pricing*
- → `GST-047` Maintenance / Upgrade Page: *Maintenance / Upgrade Page*
- → `GST-048` Upsell / Cross-Sell: *Upsell / Cross-Sell*
- → `GST-050` Resource Booking – Cabana: *Resource Booking – Cabana*
- → `GST-051` Plan: *Plan Your Adventure – Start*
- → `GST-053` Your Plan: *Build Your Own Itinerary*
- → `GST-057` Accessibility Information: *Accessibility Information*
- → `GST-058` Resource Availability (Cabana): *Resource Availability (Cabana)*
- → `GST-062` Shop & Drop Collection: *Shop & Drop Collection*
- → `GST-063` Explore – Search Results: *Search*
- → `GST-068` Help & My Cases: *Help & My Cases*
- → `GST-076` Intercity Trip — Route & Schedule: *Book a trip (a transport venue)*
- → `GST-004` Item Detail: *Opens a highlight (Item Detail)*; carries `productId`
- → `GST-051` Plan: *Plan tab*

**What opens over it**

- modal *App start, when `BrandIdentity.introVideoMode` is `firstLaunch` (first open on …*: The venue's intro video, full screen and muted, streamed from `BrandIdentity.introVideoAssetRef` so a new video needs no app rebuild. **Skip introduction** is always shown; the video ending has the same effect.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The home default list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the home default untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No home default yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing is on sale at this venue today. Said in the tenant's voice, with **Change venue**; the venue overview and the type tiles stay. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Intro video (`?state=introVideo`) | First-launch state (MOB-5): the intro video overlay plays over Home while Home loads behind it; Skip introduction reveals Home. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 A `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 September).; 400 A field outside the batch shape (a URL with a query, free text, an unhashed id), or more than 50 interactions.; 400 No … |

#### Permissions

- `getTenantAppStatus` → no permission · device, guest
- `getMyProfile` → `GUEST_VIEW` (read) · guest
- `listMyEntitlements` → `ORDER_VIEW` (read) · staff, guest
- `searchCatalogue` → no permission · guest
- `getPublishedTenantConfig` → no permission · anonymous, guest, device
- `getCookieConsentRuntime` → no permission · anonymous, guest
- `recordDeviceConsent` → no permission · anonymous, guest
- `listAnalyticsProviders` → `TENANT_CONFIGURE` (configure) · staff, guest
- `decideRecommendations` → `AI_USE` (operate) · staff, guest, anonymous
- `recordRecommendationEvents` → `AI_USE` (operate) · staff, guest, anonymous
- `recordStorefrontSessionEvents` → no permission · guest, anonymous
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `listProductCategories` → `PRODUCT_VIEW` (read) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

62 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.39 | System shall expose APIs for ticket creation, modification, pricing, inventory, reservations, validation and integrations with third-party systems. | Ticketing Catalogue | CONTRACTED | `searchCatalogue` |
| 1.2.73 | System shall expose APIs for resource management. | Ticketing Catalogue | CONTRACTED | `searchCatalogue` |
| 1.5.3 | The system should allow the user to filter the ticket by all types and available properties. For example, dated/non-dated, single-entry/multiple-entry, adult/child, standard/VIP, attraction … | Ticketing Catalogue | CONTRACTED | `searchCatalogue` |
| 2.6.52 | Cookie Consent Banner Display a cookie consent banner on the first visit. Support configurable banner layouts (top, bottom, pop-up, modal). Multi-language support. Responsive design for desktop … | Ticketing Sales | CONTRACTED | `getCookieConsentRuntime` |
| 2.6.58 | Cookie Blocking Block non-essential cookies until consent is granted. Prevent loading of: - Analytics scripts - Marketing tags - Advertising trackers Enable cookies only after user approval. | Ticketing Sales | CONTRACTED | `getCookieConsentRuntime` |
| 22.13.10 | Cookie & Tracking Consent | Marketing & CRM | CONTRACTED | `getCookieConsentRuntime` |
| 2.6.51 | A Cookie Policy Management solution helps organizations comply with privacy regulations such as GDPR, ePrivacy Directive, CCPA/CPRA, and other regional data protection laws by managing user consent … | Ticketing Sales | CONTRACTED | `recordDeviceConsent` |
| 2.6.62 | Multi-Domain Support Manage cookie consent across multiple websites. Share consent preferences across related domains. Centralized administration. | Ticketing Sales | CONTRACTED | `recordDeviceConsent` |
| 2.6.65 | Non-Functional Requirements Security - Encrypt consent records. - Secure API communication. - Role-based access control. Performance - Banner should load within 1 second. - Minimal impact on website … | Ticketing Sales | CONTRACTED | `recordDeviceConsent` |
| 19.2.46 | Personalized Offers - System shall provide personalized offers. | Guest Mobile App & Branding | CONTRACTED | `decideRecommendations` |
| 1.1.33 | AI shall recommend suitable ticket products, upgrades, bundles and promotions based on guest profile, behavior and purchase history. | Ticketing Catalogue | CONTRACTED | `decideRecommendations` |
| 1.1.34 | AI shall recommend upgrades, add-ons and premium experiences during the purchasing journey. | Ticketing Catalogue | CONTRACTED | `decideRecommendations` |
| … 50 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The landing page offers selectable scroll animations (venue choice). *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1088)*
- Multi-location attractions: the guest picks a location first (e.g. Al Barsha, Mirdif, Yas Island, Sharjah); a "Booking at" bar on later booking steps has Change location. On a switch, times and prices refresh and the selection is cleared unless the products share a family. Setting "Location switcher". *(agreed · rev 3 design review 29 Sep 2026, REV3-18 · 18. One tenant with an attraction in several locations; change location · DI-1058)*
- Home / Discover is a venue overview: description, opening hours and types (rides, dining, events, shops); one or two sample items per type are enough. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1018)*
- The B2C home page lists the ticket categories directly; clicking one opens its counters on the same screen. *(client request · design review 23 Sep 2026, Tickets 8. Show the single day ticket category on the B2C home page · DI-977)*
- **Open question.** Open: component-count logic for the experiences/dining section on the guest-app landing page — fixed 2–3-card layout vs. a scalable N-count layout. Owner Aishwarya; to confirm with Allam's team. *(open · MoM 20 Aug 2026, 4.10 CMS & White-Label; 6. Open Items · DI-396)*
- Guest app home: logo, banner and category tabs Tickets, What's On, Plan Your Visit, Map. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-196)*

Also apply: 1 for P02 · Discovery & Browse, 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Brand: logo, splash, intro video*, set in `CMS-002` Brand Kit, `CMS-004` Logo & Assets, `ADM-016` White-Label Branding Management:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Intro video (`brand.introVideoAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode (`brand.introVideoMode`) | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | Off | When GST-001 plays it full screen. "Skip introduction" is always shown. |

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Venue overrides (`bookingFlow.venueOverrides`) | at most 200; Per-venue overrides, at most one per venue.; A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. | — | Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. |

*Homepage sections*, set in `CMS-007` Page Builder:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Sections: hero style (`homepage.sections[].heroStyle`) | Carousel · Video · Poster · Split | — | For `heroBanner` only (decided 29 September, MOB-3). |

Also set there, as content the tenant writes: sections: max items.

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

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-001` · status **notStarted** · provenance client-verified
- Prototype (mobile v4 (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`, view *Home tab (Summit Peaks, after the intro)*. Differences: The v4 home shows no ticket strip; `listMyEntitlements` feeds the visit-day venue suggestion only.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0023 *— Personal data lives apart from the append-only ledger* (`docs/adr/0023-pii-separation.md`)
- ADR-0033 *Every asynchronous handoff has an outbox and a place to fail* (`docs/adr/0033-outbox-and-dead-letters.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (111 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-001?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline, introVideo.
- [ ] Every action is wired with its success and its failure: Change venue.
- [ ] Every transition is wired: `GST-002`, `GST-003`, `GST-004`, `GST-005`, `GST-006`, `GST-007`, `GST-008`, `GST-009`, `GST-010`, `GST-011`, `GST-012`, `GST-013`, `GST-014`, `GST-015`, `GST-016`, `GST-017`, `GST-018`, `GST-019`, `GST-020`, `GST-021`, `GST-023`, `GST-024`, `GST-025`, `GST-026`, `GST-027`, `GST-031`, `GST-032`, `GST-033`, `GST-034`, `GST-037`, `GST-039`, `GST-040`, `GST-041`, `GST-042`, `GST-045`, `GST-049`, `GST-052`, `GST-054`, `GST-055`, `GST-056`, `GST-059`, `GST-061`, `GST-070`, `GST-022`, `GST-028`, `GST-029`, `GST-030`, `GST-035`, `GST-036`, `GST-038`, `GST-043`, `GST-044`, `GST-047`, `GST-048`, `GST-050`, `GST-051`, `GST-053`, `GST-057`, `GST-058`, `GST-062`, `GST-063`, `GST-068`, `GST-076`, `GST-004`, `GST-051`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 6 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-002` Explore

**The Explore tab: search the venue, browse its categories and preview items before opening one.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Discovery & Browse · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #17858 (APP-MOB-GST-002) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | listDetail (comfortable density): `listProducts` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | nothing: it opens on its own |
| Route | `/general/explore-categories` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Rev 3 (decided 29 September).** Category → subcategory tiles or a flat list per `ticketCategories` (REV3-16); grid or row per `cardLayout` (the retired `categoryDisplay` is removed, W7). Info-only products are listed with their label and open details (REV3-14). Every booking-flow setting named here is read from `getTenantConfig` `bookingFlow`, resolved for the venue the guest picked (audit R267): the tenant's values with that venue's `venueOverrides` entry laid over field by field (decided 29 September, rev 3 CFG-11). **Mobile v4 (decided 29 September, MOB-1).** Retitled **Explore** and made the Explore tab root: search, category tiles and inline video previews. **GST-063 Search is its search-results state: one implementation, both ids kept** (as GAP-D3). Rows versus grid is `cardLayout`; `categoryDisplay` is retired (W7).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search the venue | text field | required | — | min length 2 | — | Sends `?q=` to `searchCatalogue`; results replace the tiles in place (GST-063, the same implementation). | `searchCatalogue` ?q |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |

#### Outputs: what the screen shows and produces

**Shown**

**Category tiles** (card list, from `listProductCategories`): `BookingFlowConfig.ticketCategories` `categoryThenSubcategory` (default): the category tiles, then that category's products (`listProducts?categoryId=`); `flatList` skips them. Grid or one scrolling row per `cardLayout` (W7).

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

**Things to do** (card list, from `listProducts`): The venue is the one the guest picked on Home (`venueId` from the session, audit R267), never typed. Was the generated table 'Every product'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Media | list or chips (count when long) | The product's own photos and video (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each … |
| Display tags | list or chips (count when long) | Short facts a guest reads on the ticket card and under *Read more*: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates … |

**Inline video previews** (card list, from `listProducts`): Cards play the product's own short clip muted in place (`Product.media` kind video, M17-10) and show the primary image otherwise; a card opens Item Detail (GST-004).

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

**Data it reads**: `listProducts` (onLoad, List products); `listProductCategories` (onLoad, The category tiles (a tree, with images and descriptions))

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `GST-003` Buy Tickets: *Event & Attraction Listing*
- → `GST-004` Item Detail: *Attraction Details*; carries `productId`
- → `GST-063` Explore – Search Results: *Searches (results in place)*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The explore categories list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the explore categories untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No explore categories yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing in the category picked; the other categories are still there. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 A `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 September). |

#### Permissions

- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `listProductCategories` → `PRODUCT_VIEW` (read) · staff, guest
- `searchCatalogue` → no permission · guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 1.1.39 | System shall expose APIs for ticket creation, modification, pricing, inventory, reservations, validation and integrations with third-party systems. | Ticketing Catalogue | CONTRACTED | `searchCatalogue` |
| 1.2.73 | System shall expose APIs for resource management. | Ticketing Catalogue | CONTRACTED | `searchCatalogue` |
| 1.5.3 | The system should allow the user to filter the ticket by all types and available properties. For example, dated/non-dated, single-entry/multiple-entry, adult/child, standard/VIP, attraction … | Ticketing Catalogue | CONTRACTED | `searchCatalogue` |
| 8.8.1 | A price for a PLU is changing depending on the date of visit. I can sell today a product to be used after a price change at the new price defined in the sales calendar. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.2 | System shall support future-dated pricing schedules. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.3 | System shall support pricing by visit date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.4 | System shall support pricing by booking date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.5 | System shall support pricing calendar management. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.6 | System shall support automatic activation of future pricing. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Category tiles (e.g. Permanent exhibition, Temporary exhibitions, Guided tours, Courses & workshops), then that category's tickets with Adult / Child / Student counters. Setting "Ticket categories": Category → subcategory (default) or Flat list (all tickets under category headings). *(agreed · rev 3 design review 29 Sep 2026, REV3-16 · 16. Choose category, then subcategory, configurable in the CMS · DI-1056)*
- Home / Discover is a venue overview: description, opening hours and types (rides, dining, events, shops); one or two sample items per type are enough. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1018)*
- Explore cards play the product's own short clip muted in place, and show the primary image otherwise. *(agreed · MoM 17 Sep 2026, M17-10 · DI-921)*
- Purchase flow: categories (Attractions, Exhibitions, Events, Dining, Shops, Experiences) → ticket selection (from back-office config) → date/time slot → add-ons (per ticket type or generic) → review & pay → confirmation. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-197)*

Also apply: 1 for P02 · Discovery & Browse, 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Card layout (`bookingFlow.cardLayout`) | Stacked rows · Split rows · Cards across · Poster cards | Stacked rows | ticket and product cards: stacked rows, split rows, cards across, or poster cards |
| Ticket categories (`bookingFlow.ticketCategories`) | Category then subcategory · Flat list | Category then subcategory | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once. |
| Venue overrides (`bookingFlow.venueOverrides`) | at most 200; Per-venue overrides, at most one per venue.; A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. | — | Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. |
| Settings: card layout (`bookingFlow.venueOverrides[].settings.cardLayout`) | Stacked rows · Split rows · Cards across · Poster cards | Stacked rows | How ticket and product cards are laid out (decided 29 September, rev 3 DG-6). Was a free string; the four values are the design's Stacked rows, Split rows, Cards across and Poster cards. |
| Settings: ticket categories (`bookingFlow.venueOverrides[].settings.ticketCategories`) | Category then subcategory · Flat list | Category then subcategory | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once. |

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-002` · status **notStarted** · provenance client-verified
- Prototype (mobile v4 (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`, view *Explore tab*
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-002?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `GST-001`, `GST-003`, `GST-004`, `GST-063`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-003` Buy Tickets

**Every bookable product and booking flow of the venue, one tap from any screen.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Discovery & Browse · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #17949 (APP-MOB-GST-003) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | listDetail (comfortable density): `listProducts` reads the population and `getWaitTimes` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `eventId` (deepLink), `venueId` (session) · cold entry: **Named, expired or withdrawn — never a 404** (ADR-0030). A guest holding a link that no longer resolves did nothing wrong; the screen says what happened and … |
| Route | `/general/attractions-list` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Cross-platform navigation removed 24 August**: BO-005. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Renamed 31 August** from *Attractions List*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest. **Cross-surface parity, 31 August**: added listPerformances, searchCatalogue. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations. **Rev 3 (decided 29 September).** **Info-only products** (`Product.guestListing` `infoOnly`) show `notBookableLabel` (default *Info only / Not bookable online*) and open their details instead of adding to the basket; hidden when `BookingFlowConfig.showInfoOnly` is off (REV3-14). Categories per `ticketCategories` (REV3-16). Each product shows its own primary image (`Product.media`, 23SEP-4). Card layout, size and density are the enums of DG-6. Every booking-flow setting named here is read from `getTenantConfig` `bookingFlow`, resolved for the venue the guest picked (audit R267): the tenant's values with that venue's `venueOverrides` entry laid over field by field (decided 29 September, rev 3 CFG-11). **Mobile v4 (decided 29 …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search tickets | search field | — | — | — | — | Finds a ticket by name among what is on sale. | `searchCatalogue` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |
| From | date and time picker | — | — | `listPerformances` ?from |
| To | date and time picker | — | — | `listPerformances` ?to |
| Category | picker: choose a category | — | — | `listPerformances` ?categoryId |
| Language | text field | — | max length 35; pattern `^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$` | `listPerformances` ?language |

#### Outputs: what the screen shows and produces

**Shown**

**Tickets and passes** (card list, from `listProducts`): The venue is the one the guest picked on Home (`venueId` from the session, audit R267), never typed. Was the generated table 'Every product'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Media | list or chips (count when long) | The product's own photos and video (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each … |
| Display tags | list or chips (count when long) | Short facts a guest reads on the ticket card and under *Read more*: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates … |

**Help me choose** (banner, from `getPublishedGuidedChoice`): **Help me choose filters the list** (W4): the answers are sent as `guidedAnswerIds` to `listProducts` and only the suitable products stay; `GuidedChoice.behaviour` `recommend` opens one product instead. It is never a consent step.

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

**Contact sales** (card list, from `listProducts`): **View-only products** (W3): a product with `guestListing` `infoOnly` shows its details and, instead of Book, **Call sales** and **Email sales** from `Product.salesContact` (the venue contact when it has none). Hidden when `showInfoOnly` is off.

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

**Next times** (card list, from `listPerformances`): The next times of a dated event, on its card.

| Shows | Format | Notes |
|---|---|---|
| Starts at | 1 Oct 2026, 14:30 | — |
| Language | text | The language the performance is given in, as a BCP 47 tag (`en`, `ar`, `fr`, `de`, `zh`, `ru`, `ar-AE`). |

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
| Show everything (secondary button) | `listProducts` GET `/products` | — | Product (paged) | 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 403 Authenticated but not permitted at the requested scope | works offline |

**Data it reads**: `listProducts` (onLoad, List products); `getWaitTimes` (onLoad, Wait times across a venue); `listPerformances` (onLoad, List performances of an event); `getPublishedGuidedChoice` (onLoad, Help me choose: the venue's questions whose answers filter …)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `GST-004` Item Detail: *Attraction Details*; carries `eventId`, `productId`
- → `GST-007` Select Date & Time: *Book (a dated product: date, then time, then tickets)*; carries `productId`
- → `GST-008` Tickets & Add-ons: *Book (an undated product, or a product-first flow such as a workshop)*; carries `productId`
- → `GST-074` Map Booking — Cabanas & Spots: *Book (a spot on the venue map, where the flow picks on the map)*; carries `productId`
- → `GST-075` Book a Space by the Hour: *Book (a space by the hour)*; carries `productId`
- → `GST-056` Bundle Package: *Book a bundle (e.g. meal combo with admission)*
- → `BO-005` Queue Monitor: *A supervisor sees the queue building*; carries `queueId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The event attraction listing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the event attraction listing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No event attraction listing yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches what was typed or picked; the other tickets are still there. Names it and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 A `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 September). |

#### Permissions

- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `getWaitTimes` → no permission · guest, public
- `listPerformances` → `PRODUCT_VIEW` (read) · staff, guest
- `searchCatalogue` → no permission · guest
- `getPublishedGuidedChoice` → no permission · guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

24 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 19.2.34 | Time Slot Reservations - System shall support time slot reservations. | Guest Mobile App & Branding | CONTRACTED | `listPerformances` |
| 2.6.15 | - Time slots for events | Ticketing Sales | CONTRACTED | `listPerformances` |
| 2.7.16 | - Dedicated sales calendar | Ticketing Sales | CONTRACTED | `listPerformances` |
| 1.1.39 | System shall expose APIs for ticket creation, modification, pricing, inventory, reservations, validation and integrations with third-party systems. | Ticketing Catalogue | CONTRACTED | `searchCatalogue` |
| 1.2.73 | System shall expose APIs for resource management. | Ticketing Catalogue | CONTRACTED | `searchCatalogue` |
| … 12 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Category tiles (e.g. Permanent exhibition, Temporary exhibitions, Guided tours, Courses & workshops), then that category's tickets with Adult / Child / Student counters. Setting "Ticket categories": Category → subcategory (default) or Flat list (all tickets under category headings). *(agreed · rev 3 design review 29 Sep 2026, REV3-16 · 16. Choose category, then subcategory, configurable in the CMS · DI-1056)*
- Card layout is a choice, not free text: Stacked rows (default) · Split rows · Cards across · Poster cards. Card size: Compact (default) · Standard · Large · Extra large. Density: Compact (default) · Standard · Roomy. *(agreed · design review 29 Sep 2026, 6. Booking-flow configuration (CMS-016): card-layout options · DI-1040)*
- Read more opens with the ticket's video or photo, and every ticket in a listing has its own photo (product media: images and videos, one primary). *(agreed · design review 29 Sep 2026, Tickets 4. Video or image should show · DI-1026)*
- CMS option to list a product (e.g. training courses) with full details but no Book button; instead show "Contact sales to book" with contact details. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W3 View-only products · DI-1004)*
- Experience venues list each experience directly (e.g. author talk, calligraphy workshop, story hour, rooftop reading night), each with its own date, time and tickets; no category step. *(client request · rev 3 design review 25 Sep 2026, 12. Experience flow: show the product directly, not the ticket category · DI-999)*
- Show the ticket categories (e.g. Single day, Two-day flexible, UAE resident) directly; no intermediate "Dated day pass" step. *(client request · design review 23 Sep 2026, Tickets 7. Show the ticket category directly instead of Dated Pass -> Single Day Pass · DI-976)*
- Allam's UX benchmark (Little Explorer, Dubai): multi-location selector, a horizontal near-term date picker with full-calendar fallback, and tabbed browsing (passes / workshops / packages) on one page rather than multiple screens. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-585)*
- Decision: ticket types are browsed in-page, not across multiple pages; "View all ticket types" expands additional categories in place. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-427)*
- Purchase flow: categories (Attractions, Exhibitions, Events, Dining, Shops, Experiences) → ticket selection (from back-office config) → date/time slot → add-ons (per ticket type or generic) → review & pay → confirmation. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-197)*
- Qossai liked a pattern using product video rather than static images for tickets. *(client request · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-127)*

Also apply: 1 for P02 · Discovery & Browse, 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Navigation: menu, tab bar, Buy tickets button*, set in `CMS-009` Navigation & Menus:

Also set there, as content the tenant writes: buy button.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Ticket categories (`bookingFlow.ticketCategories`) | Category then subcategory · Flat list | Category then subcategory | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once. |
| Show info only (`bookingFlow.showInfoOnly`) | — | on | Show info-only products (decided 29 September, rev 3 REV3-14). On, a product with `guestListing` `infoOnly` (catalogue) is listed with its not-bookable label and opens its details; off, guests are not shown it. |
| Venue overrides (`bookingFlow.venueOverrides`) | at most 200; Per-venue overrides, at most one per venue.; A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. | — | Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. |
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

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-003` · status **notStarted** · provenance client-verified
- Prototype (mobile v4 (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`, view *Buy tickets (the centre tab)*
- Flow F21 *A ride queue fills and a guest is redirected*, step 2: Picks something shorter from the attractions list → Or joins a virtual queue for the long one. **Repointed from GST-059 Plan My Day on 17 August (CF-101)** — the itinerary planner is deferred to a later release (wave 4, decided 28 September, audit …
- Flow F21 branch at step 2 (requiresStaff): when The guest joins two virtual queues at once, Allowed or not is a venue policy nobody has stated. **Allowing it lets one guest hold two places while standing in neither.**
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0030 *A deep link is a pointer, not authorisation* (`docs/adr/0030-deep-link-cold-entry.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (53 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-003?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Show everything.
- [ ] Every transition is wired: `GST-001`, `GST-004`, `GST-007`, `GST-008`, `GST-074`, `GST-075`, `GST-056`, `BO-005`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 10 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-004` Item Detail

**One detail screen for a ride, show, restaurant or shop: what it is, where it is on the map, and the product to buy for it.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Discovery & Browse · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #17950 (APP-MOB-GST-004) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | listDetail (comfortable density): `listPerformances` reads the population and `getProduct` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `productId` (deepLink), `eventId` (deepLink), `mapId` (session), `bundleId` (navigation) · cold entry: **A shared product link after the product retired.** Shows what replaced it where a successor exists, and the catalogue where none does. |
| Route | `/general/attraction-details` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Cross-surface parity, 31 August**: added listPerformances. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations. **Rev 3 (decided 29 September).** Ticket tags (23SEP-3) and the product's own photo or video (23SEP-4); an info-only product shows its label and no Book (REV3-14). Book goes to the date and time (GST-007) for a dated product (REV3-2), straight to the seat map for a single-performance fixture (23SEP-16, REV3-4), to the map booking for a spot on a venue map (GST-074, REV3-15), or to the space booking (GST-075, REV3-13). Help me choose sits on the booking step (GST-008), not here (REV3-11). The event banner lists dates only when `eventBannerDates` is on (23SEP-19). **Mobile v4 (decided 29 September, MOB-4).** GST-004 and GST-006 become one **Item Detail** screen for rides, shows, restaurants and shops: **one implementation, both ids kept** (as GAP-D3). Gallery, the 2D/3D map pin (`getVenueMap`) and a product card from `VenuePoint.featuredOffer` (product or bundle). *Buy meal combo* adds the required admission because the bundle carries it. **W3:** an info-only product shows Call sales / Email sales instead of Book. **Video plays directly (client meeting 30 September, MoM 4.8, Qossai; agreed by Chinmay).** On a ride or attraction the info button reveals the details and plays the video straight away; the loader …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Where it is | seat map | — | — | — | — | The item's pin on the venue map, 2D or 3D per the venue; tapping it opens At the Venue on the Map view (GST-038 / GST-021) with directions. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Performance | picker: choose a performance | — | — | `getAvailability` ?performanceId |
| Channel capacity | picker: choose a channel capacity | — | — | `getAvailability` ?channelCapacityId |
| Event | picker: choose an event | — | — | `getAvailability` ?eventId |
| From | date and time picker | — | — | `getAvailability` ?from |
| To | date and time picker | — | Exclusive; at most 31 days after `from`. | `getAvailability` ?to |
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |
| From | date and time picker | — | — | `listPerformances` ?from |
| To | date and time picker | — | — | `listPerformances` ?to |
| Category | picker: choose a category | — | — | `listPerformances` ?categoryId |
| Language | text field | — | max length 35; pattern `^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$` | `listPerformances` ?language |
| Version | number field | — | — | `getVenueMap` ?version |
| Draft | toggle | off | Staff only, and it needs `VENUE_MAP_MANAGE`, because the draft is unfinished work that must never reach a guest. | `getVenueMap` ?draft |

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

**Ticket tags** (card list, from `getProduct`): Up to six tags with an icon by kind (clock, height, free, calendar, id); derived on read where the product has none. Only when `BookingFlowConfig.ticketTags` is on.

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

**Photo and video** (detail panel, from `getProduct`): **The video plays directly, with no loader in front of it** (client meeting 30 September, MoM 4.8, Qossai; agreed by Chinmay). The info button reveals the ride details and starts the primary video in place, as the header video does elsewhere; while it buffers the poster frame (the primary image, or the video's first frame) shows, never a spinner or loading screen. Read more opens on the primary …

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

**Gallery** (detail panel, from `getVenueMap`): Photos and clips from `VenuePoint.media` (else `Product.media`), with the point's description. A clip plays in place from its poster frame, with no loader (client meeting 30 September, MoM 4.8).

| Shows | Format | Notes |
|---|---|---|
| Description | grouped details | What the guest reads on Item Detail (29 September, MOB-4). Keyed by locale, like `nameLocalised`. |
| Media | list or chips (count when long) | The gallery on Item Detail (29 September, MOB-4): images and short clips from the asset library, first `isPrimary` shown on the map card. |

**The product for it** (card list, from `getBundle`): **The right product** (MOB-4): `VenuePoint.featuredOffer` names a product (`getProduct`) or a bundle (`getBundle`), on any kind of point. A restaurant proposes **Buy meal combo**: a bundle with an admission component and a meal component, so the park ticket is included and checkout is about three steps (GST-056 → GST-041).

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Venue | the name it points at, never the id | — |
| Kind | chip: Fixed, Dynamic, Mandatory, Optional, Promotional | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Components | list or chips (count when long) | — |
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Variant | the name it points at, never the id | — |
| Component kind | chip: Admission, Fnb menu item, Retail, Add on, Other | What a bundle component entitles the guest to (decided 29 September, MOB-4). `admission` is a ticket; `fnbMenuItem` is a meal redeemed at … |
| Menu item | the name it points at, never the id | The F&B menu item a `fnbMenuItem` component entitles the guest to (decided 29 September, MOB-4): the meal of a *meal combo with admission*. |
| Redeem at outlets | list or chips (count when long) | Outlets that redeem an `fnbMenuItem` component; empty means any outlet of the component's venue that has the menu item on a live menu … |
| Quantity | 1,234 | — |
| Is optional | yes / no (icon or chip) | — |
| Substitute variants | list or chips (count when long) | For dynamic bundles — guest chooses among these. |
| Substitution triggers | list or chips (count when long) | When a substitute from `substituteVariantIds` may replace this component (Dynamic Component Substitution Engine). |
| Substitution price effect | chip: Same price, Surcharge, Reduced price | What a substitution does to the bundle price. |
| Substitution approval | chip: None, Customer, Operator | Who must accept a substitution before it stands. Customer by default, because a substitution the guest did not choose is a complaint at the … |
| Venue | the name it points at, never the id | Where this component is redeemed. Differs from the selling venue for multi-venue passes, which is why the allocation split exists. |
| Choice groups | list or chips (count when long) | Dynamic bundles (3.5.10). A bundle may carry fixed components and choice groups at once — a family pass with fixed parking and two groups … |

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
| Call sales / Email sales (secondary button) | `getProduct` GET `/products/{productId}` | — | Product | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline |

**Data it reads**: `getProductEligibilityRule` (onLoad, Age and height limits); `getProduct` (onLoad, Read a product); `getAvailability` (onLoad, Live remaining capacity); `getWaitTimes` (onLoad, Wait times across a venue); `listPerformances` (onLoad, List performances of an event); `getVenueMap` (onLoad, The item's point on the 2D/3D venue map, with its …); `getBundle` (onLoad, The featured offer when it is a bundle, e.g. meal combo …)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `GST-003` Buy Tickets: *Event & Attraction Listing*; carries `eventId`
- → `GST-007` Select Date & Time: *Book (a dated product: date, then time, then tickets)*; carries `eventId`
- → `GST-008` Tickets & Add-ons: *Book (an undated product: tickets straight away)*; carries `productId`
- → `GST-049` Interactive Seat Selection: *Book (a fixture with one on-sale performance opens straight on the seat map)*; carries `performanceId`
- → `GST-074` Map Booking — Cabanas & Spots: *Book (a cabana, lounger or other spot on the venue map)*; carries `productId`
- → `GST-075` Book a Space by the Hour: *Book (a space sold by the hour)*; carries `productId`
- → `GST-056` Bundle Package: *Buy meal combo (a bundle that includes admission)*; carries `bundleId`
- → `GST-038` At the Venue: *Show on the map (At the Venue, Map view)*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | **The video is not part of loading** (client meeting 30 September, MoM 4.8): the attraction renders as it arrives and no loader or loading screen is ever drawn over the video. |
| Video buffering (`?state=videoBuffering`) | **Poster frame, not a loader** (client meeting 30 September, MoM 4.8): from the info button until the first frames arrive the ride's poster (primary image, else the video's first frame) fills the video area and playback starts in place as soon as it can; no spinner, overlay or blocking screen. The details beside it stay usable throughout. |
| Video unavailable (`?state=videoUnavailable`) | The video cannot play (no video, a failed stream, data saver on). The poster stays and the details are unaffected; no error screen and no loader. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attraction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attraction yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | No performance in the next days shown; the strip says so and offers the calendar. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `getProductEligibilityRule` → `PRODUCT_VIEW` (read) · staff, guest
- `getProduct` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `getAvailability` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `getWaitTimes` → no permission · guest, public
- `listPerformances` → `PRODUCT_VIEW` (read) · staff, guest
- `getVenueMap` → `VENUE_MAP_VIEW` (read) · staff, guest
- `getBundle` → `PRODUCT_VIEW` (read) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

29 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.74 | System shall support event-driven integrations. | Ticketing Catalogue | CONTRACTED | `getAvailability` |
| 2.1.4 | The system should ensure full integration of all internal sales channels. All associated information (capacity, sales, etc.) must be available to multiple operators simultaneously in real-time. | Ticketing Sales | CONTRACTED | `getAvailability` |
| 2.6.10 | - Event capacity updated in real-time | Ticketing Sales | CONTRACTED | `getAvailability` |
| 2.6.14 | - Remaining quantities | Ticketing Sales | CONTRACTED | `getAvailability` |
| 2.7.14 | - Capacity management in real time is expected | Ticketing Sales | CONTRACTED | `getAvailability` |
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 19.2.34 | Time Slot Reservations - System shall support time slot reservations. | Guest Mobile App & Branding | CONTRACTED | `listPerformances` |
| 2.6.15 | - Time slots for events | Ticketing Sales | CONTRACTED | `listPerformances` |
| 2.7.16 | - Dedicated sales calendar | Ticketing Sales | CONTRACTED | `listPerformances` |
| … 17 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Qossai: ride/attraction detail pages play the video directly, with no loading screen in front of it; an info button reveals ride details and plays the video. Chinmay agreed to remove the loader. *(agreed · MoM 30 Sep 2026, 4.8 Mobile App — In-Ride Video/Info & In-Park Navigation · DI-1101)*
- Item detail shows a gallery, the item's location on the 2D/3D map and proposes the relevant product, e.g. a restaurant offers "Buy meal combo", which automatically adds the required admission ticket (checkout in about 3 steps). *(agreed · design review 29 Sep 2026, Mobile app (v4) — Item detail: map location and relevant product (meal combo includes admission) · DI-1082)*
- Clicking a ticket opens the Adult / Child / Senior / Infant counters in a side panel on the same listing or details screen (no separate "Select Tickets" step); the panel is open by default on the listing and Book goes straight into the booking. *(agreed · design review 29 Sep 2026, Tickets 5. Clicking Dated Day Pass should show the tickets on the same screen · DI-1027)*
- Read more opens with the ticket's video or photo, and every ticket in a listing has its own photo (product media: images and videos, one primary). *(agreed · design review 29 Sep 2026, Tickets 4. Video or image should show · DI-1026)*
- Ticket cards, Read more and the listing side panel show tags (e.g. "2 Hours", "Min 1.10 m", "Free adult entry", "Valid 90 days", "Emirates ID"), each with a kind icon (clock, height, free, calendar, id), max 6. Venue-set tags win, else derived from duration, validity, height rule. Setting "Tags on tickets", default on. *(agreed · design review 29 Sep 2026, Tickets 3. 'Read more' should carry tags customisable per ticket type · DI-1025)*
- Item detail shows the item's location on the map and proposes the relevant product, e.g. restaurant -> "Buy meal combo", which automatically adds the required admission ticket (checkout in ~3 steps). *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1019)*
- CMS option to list a product (e.g. training courses) with full details but no Book button; instead show "Contact sales to book" with contact details. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W3 View-only products · DI-1004)*
- Show the ticket categories (e.g. Single day, Two-day flexible, UAE resident) directly; no intermediate "Dated day pass" step. *(client request · design review 23 Sep 2026, Tickets 7. Show the ticket category directly instead of Dated Pass -> Single Day Pass · DI-976)*
- Qossai and Allam: product pages should include short video content (e.g. a 10-15 second clip), not only static images, to give a sense of the actual experience (e.g. a ride) before booking. *(agreed · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-917)*
- Product cards/pages carry short descriptions with an expandable "view more details" control and a configurable hero image or video per product. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-425)*
- Qossai liked a pattern using product video rather than static images for tickets. *(client request · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-127)*

Also apply: 1 for P02 · Discovery & Browse, 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Event banner dates (`bookingFlow.eventBannerDates`) | — | off | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |
| Ticket tags (`bookingFlow.ticketTags`) | — | on | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on its card. |
| Settings: event banner dates (`bookingFlow.venueOverrides[].settings.eventBannerDates`) | — | off | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |
| Settings: ticket tags (`bookingFlow.venueOverrides[].settings.ticketTags`) | — | on | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on its card. |

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-004` · status **notStarted** · provenance client-verified
- Prototype (mobile v4 (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`, view *Explore → Summit Coaster (Item detail)*
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (103 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-004?state=<state>`: loading, videoBuffering, videoUnavailable, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Call sales / Email sales.
- [ ] Every transition is wired: `GST-001`, `GST-003`, `GST-007`, `GST-008`, `GST-049`, `GST-074`, `GST-075`, `GST-056`, `GST-038`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 11 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-005` What's On

**Find what's on for this venue.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Discovery & Browse · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #17859 (APP-MOB-GST-005) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | listDetail (comfortable density): `listPerformances` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `eventId` (deepLink) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation … |
| Route | `/general/whats-on` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Drawn 31 August** — `Guest Mobile Board 1.dc.html` frame `gm-1b`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *What's On* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?from=` to `listPerformances`. | `listPerformances` ?from |
| To | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?to=` to `listPerformances`. | `listPerformances` ?to |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `listPerformances` ?categoryId |
| Language | text field | — | max length 35; pattern `^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$` | `listPerformances` ?language |
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |

#### Outputs: what the screen shows and produces

**Shown**

**Every performance** (data table, from `listPerformances`)

| Shows | Format | Notes |
|---|---|---|
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Status | chip: Scheduled, On sale, Sold out, Suspended, Cancelled, Completed | — |

**Every product** (data table, from `listProducts`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |

**The selected performance** (detail panel, from `listPerformances`)

| Shows | Format | Notes |
|---|---|---|
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Status | chip: Scheduled, On sale, Sold out, Suspended, Cancelled, Completed | — |

**Data it reads**: `listPerformances` (onLoad, List performances of an event); `listProducts` (onLoad, List products)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `GST-003` Buy Tickets: *Event & Attraction Listing*; carries `eventId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The what's list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the what's untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No what's yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on from, to and the what's are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 … |

#### Permissions

- `listPerformances` → `PRODUCT_VIEW` (read) · staff, guest
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.34 | Time Slot Reservations - System shall support time slot reservations. | Guest Mobile App & Branding | CONTRACTED | `listPerformances` |
| 2.6.15 | - Time slots for events | Ticketing Sales | CONTRACTED | `listPerformances` |
| 2.7.16 | - Dedicated sales calendar | Ticketing Sales | CONTRACTED | `listPerformances` |
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 1.3.19 | System shall support event lifecycle states including Draft, Pending Approval, Approved, Published, On Sale, Sold Out, Completed, Cancelled and Archived. | Ticketing Catalogue | CONTRACTED | data `Performance` |
| 7.4.45 | Support Draft, Review, Approval, Published, Suspended and Archived statuses. Prevent publishing without required approvals and maintain lifecycle history. | F&B POS | CONTRACTED | data `Performance` |
| 8.8.1 | A price for a PLU is changing depending on the date of visit. I can sell today a product to be used after a price change at the new price defined in the sales calendar. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.2 | System shall support future-dated pricing schedules. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.3 | System shall support pricing by visit date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.4 | System shall support pricing by booking date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P02 · Discovery & Browse, 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-005` · status **notStarted** · provenance client-verified · **Drawn by Claude Design on `Guest Mobile Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been …
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 1 → What’s on*
- Derived from `wireframes/reference/Guest Mobile Board 1.dc.html`
- Client design-board frames: `Guest Mobile Board 1.dc.html#gm-1b`
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-005?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `GST-001`, `GST-003`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-006` Item Detail – Event / Exhibition

**See event / exhibition details for this venue.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Discovery & Browse · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #17860 (APP-MOB-GST-006) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (comfortable density): `getPerformance` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `performanceId` (deepLink), `productId` (deepLink) · cold entry: **A link to a performance that has happened.** Offers the next performance of the same event. **A shared product link after the product retired.** Shows what … |
| Route | `/general/event-exhibition-details` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Mobile v4 (decided 29 September, MOB-4).** The event and exhibition reading of **Item Detail**: **one implementation with GST-004, both ids kept** (as GAP-D3). Book follows the event's published booking flow (W12).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**The performance** (detail panel, from `getPerformance`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Event | the name it points at, never the id | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Approval request | the name it points at, never the id | BL-048. The approval chain and the occurrence lifecycle sat on different entities, so neither was complete: `states/performance.yaml` … |
| Requires approval to cancel | yes / no (icon or chip) | Cancelling a sold performance is the one transition that needs a name against it. |
| Status | chip: Scheduled, On sale, Sold out, Suspended, Cancelled, Completed | — |
| Admission rules | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |

**The product** (detail panel, from `getProduct`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Created by principal | the name it points at, never the id | 1.4.18. The approval gate refuses an approver who is the author, and nothing recorded either. |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |
| Category | the name it points at, never the id | Taken from their `fnb.product` and `retail.product`, 20 September. `catalogue.product_category` has existed since 20 August with two … |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | — |
| Is sellable | yes / no (icon or chip) | True only when live and carried by a published bundle. Approval and publication are different acts. |
| Is stock tracked | yes / no (icon or chip) | Taken from their `fnb.product`, 20 September. Whether a sale decrements stock, which is not what `isSellable` asks. |

**Data it reads**: `getPerformance` (onLoad, Read a performance); `getProduct` (onLoad, Read a product)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `GST-003` Buy Tickets: *Event & Attraction Listing*; carries `eventId`
- → `GST-007` Select Date & Time: *Book (date, then time, then tickets)*; carries `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The event exhibition, read by `getPerformance`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the event exhibition untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No event exhibition yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |

#### Permissions

- `getPerformance` → `PRODUCT_VIEW` (read) · staff, guest
- `getProduct` → `PRODUCT_VIEW` (read) · staff, guest, partner

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.19 | System shall support event lifecycle states including Draft, Pending Approval, Approved, Published, On Sale, Sold Out, Completed, Cancelled and Archived. | Ticketing Catalogue | CONTRACTED | data `Performance` |
| 7.4.45 | Support Draft, Review, Approval, Published, Suspended and Archived statuses. Prevent publishing without required approvals and maintain lifecycle history. | F&B POS | CONTRACTED | data `Performance` |
| 8.8.1 | A price for a PLU is changing depending on the date of visit. I can sell today a product to be used after a price change at the new price defined in the sales calendar. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.2 | System shall support future-dated pricing schedules. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.3 | System shall support pricing by visit date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.4 | System shall support pricing by booking date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.5 | System shall support pricing calendar management. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.6 | System shall support automatic activation of future pricing. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.7 | System shall support overlapping pricing schedules with priority rules. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.8 | System shall maintain pricing schedule history. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.9 | System shall provide pricing schedule audit trails. | Unified Operations Dashboard | CONTRACTED | data `Product` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Platinum List reference: event page with short video + image + description → select tickets → calendar collapsed to a week view, expandable to full month → time-slot selection. *(client request · MoM 21 Aug 2026, 4.1 Reference Walkthrough — Platinum List Seat Selection & Checkout Journey · DI-408)*
- Qossai liked a pattern using product video rather than static images for tickets. *(client request · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-127)*

Also apply: 1 for P02 · Discovery & Browse, 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-006` · status **notStarted** · provenance client-verified
- Prototype (mobile v4 (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`, view *Explore → Shows → Night of Nine → More info (Item detail, an event)*
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (25 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-006?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `GST-001`, `GST-003`, `GST-007`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-057` Accessibility Information

**Step-free routes, facilities and what to expect.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Discovery & Browse · wave 2 · needs the `core` module |
| Block | Block A · ticket #18093 (APP-MOB-GST-057) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · light, dark theme |
| Pattern | listDetail (comfortable density): `listContentPages` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The offline banner shows.** Help already loaded stays readable, marked with its age. **Raising a case is disabled offline** — it needs the connection (decided 28 September, audit R148) — and the screen says how to reach staff in person instead: the guest services desk, or any member of staff. |
| Opens with | nothing: it opens on its own |
| Route | `/general/accessibility-information` |

**What the spec says about it.** Minuted 10 Aug §4.1: custom content pages *"with accessibility-guideline compliance to be followed"*. **Tenant-authored content, not a built feature.**

**Known gaps.** Replaced by `listPublishedContentPages`, the guest read of the same data.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category code | text field | — | — | `listPublishedContentPages` ?categoryCode |
| Slug | text field | — | pattern `^[a-z0-9-]+$` | `listPublishedContentPages` ?slug |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Accessibility pages** (card list, from `listPublishedContentPages`): The live pages in the `accessibility` category, a value the screen sends and the guest never types. Was the generated table 'Every content page'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Title | in the reader's language | — |
| Icon | the image or video | — |

**The page** (detail panel, from `listPublishedContentPages`)

| Shows | Format | Notes |
|---|---|---|
| Title | in the reader's language | — |
| Body | in the reader's language | Keyed by language code. Values are sanitised HTML. |

**Data it reads**: `listPublishedContentPages` (onLoad, The live accessibility pages (`categoryCode` fixed by the …)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `GST-003` Buy Tickets: *Event & Attraction Listing*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accessibility information list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accessibility information untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accessibility information yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: the screen sends no filter a guest chose, so an empty list is the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | **Nothing here needs a sign-in** (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-2)): the screen reads only what the tenant has published, which is public, so there is no no-access case. A host that belongs to no tenant shows the platform's neutral holding page. |
| Offline (`?state=offline`) | **The offline banner shows.** Help already loaded stays readable, marked with its age. **Raising a case is disabled offline** — it needs the connection (decided 28 September, audit R148) — and the screen says how to reach staff in person instead: the guest services desk, or any member of staff. |

#### Permissions

- `listPublishedContentPages` → no permission · anonymous, guest, device

**A refused user sees:** **Nothing here needs a sign-in** (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-2)): the screen reads only what the tenant has published, which is public, so there is no no-access case. A host that belongs to no tenant shows the platform's neutral holding page.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Custom content pages (e.g. accessibility information: step-free routes, facilities, what to expect) are tenant-authored and must follow accessibility-guideline compliance. *(agreed · MoM 10 Aug 2026, 4.1 · DI-243)*
- Custom content pages per venue (e.g. "Plan Your Visit", Accessibility) that follow accessibility guidelines. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-190)*

Also apply: 1 for P02 · Discovery & Browse, 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Content pages*, set in `CMS-007` Page Builder:

Also set there, as content the tenant writes: category code.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-057` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 2 → Accessibility information*

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-057?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `GST-001`, `GST-003`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

## Tenant configuration on every guest screen

Every guest screen in this batch is white-label. These elements are set by the tenant in the CMS and apply to every screen of the guest app (each screen's block lists the ones particular to it). **Draw with the default theme; on the key screens add one alternate tenant theme** (below), so a reviewer sees the brand is configuration, not paint. The full map, with the input-to-output examples: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Element | Configured in | Allowed values | Default | What it changes |
|---|---|---|---|---|
| Logo (`brand.logoAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo in the header or nav bar, the splash and the footer |
| Logo dark image (`brand.logoDarkAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo on dark backgrounds (falls back to the primary logo) |
| Logo variant (`brand.logoVariant`) | `CMS-002`, `CMS-004`, `ADM-016` | Light · Dark · Duotone | Light | which logo lockup sits in the nav bar, and whose colours drive the theme |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Splash image (`brand.splashImageAssetRefs`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG, JPG, SVG or MP4 from the media library | — | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). |
| Splash duration seconds (`brand.splashDurationSeconds`) | `CMS-002`, `CMS-004`, `ADM-016` | min 0; max 10 | 3 | — |
| Splash background colour (`brand.splashBackgroundColour`) | `CMS-002`, `CMS-004`, `ADM-016` | #RRGGBB | — | — |
| Show loading indicator (`brand.showLoadingIndicator`) | `CMS-002`, `CMS-004`, `ADM-016` | — | on | — |
| Intro video (`brand.introVideoAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode (`brand.introVideoMode`) | `CMS-002`, `CMS-004`, `ADM-016` | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | Off | When GST-001 plays it full screen. "Skip introduction" is always shown. |
| Primary colour (`theme.primaryColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | the brand colour (the `accentSolid` token): primary buttons (Book, Continue, Add to cart, Pay), the active step of the step indicator, selected date and time chips, focus rings |
| Secondary colour (`theme.secondaryColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | secondary buttons and secondary emphasis: unselected chips, secondary tabs |
| Accent colour (`theme.accentColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | highlights: badges (LIMITED, NEW, BESTSELLER), availability counts, sale prices |
| Background colour (`theme.backgroundColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | the page background behind every screen (the `ground` token) |
| Text colour (`theme.textColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | body text on the background |
| Dark mode (`theme.darkMode`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | the dark variant on a device in dark mode (mobile app); derived from the light theme when absent |
| Corner radius (`theme.cornerRadius`) | `CMS-005`, `CMS-003`, `ADM-016` | min 0; max 32 | — | the corners of cards, buttons, inputs, sheets and the cart (0 square to 22 the prototype's roundest) |
| Surface style (`theme.surfaceStyle`) | `CMS-005`, `CMS-003`, `ADM-016` | Glass · Solid | Glass | cards and panels: frosted glass (default) or opaque (the `surfaceRaised` token) |
| Button style (`theme.buttonStyle`) | `CMS-005`, `CMS-003`, `ADM-016` | Solid · Outline · Pill | Solid | every button's shape: solid fill, outline, or pill |
| Component colours (`theme.componentColours`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. |
| Primary latin (`fonts.primaryLatin`) | `CMS-003` | — | — | headings and body text in English |
| Primary arabic (`fonts.primaryArabic`) | `CMS-003` | Required when `ar` is among the tenant's languages (audit R163). | — | headings and body text in Arabic |
| Secondary latin (`fonts.secondaryLatin`) | `CMS-003` | — | — | the secondary face (eyebrows, numbers) in English |
| Secondary arabic (`fonts.secondaryArabic`) | `CMS-003` | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). | — | the secondary face in Arabic |
| Custom font images (`fonts.customFontAssetRefs`) | `CMS-003` | PNG, JPG, SVG or MP4 from the media library | — | Uploaded font files, as `MediaAsset` ids. |
| Header layout (`header.layout`) | `CMS-007` | Logo left · Logo centre · Logo with menu | — | the header: logo left, logo centred, or logo with the menu |
| Show logo (`header.showLogo`) | `CMS-007` | — | on | — |
| Show menu (`header.showMenu`) | `CMS-007` | — | on | — |
| Show notifications (`header.showNotifications`) | `CMS-007` | — | on | — |
| Background colour (`header.backgroundColour`) | `CMS-007` | #RRGGBB | — | — |
| Navigation kind (`navigation.kind`) | `CMS-009` | Bottom navigation · Drawer · Tabs | — | the main navigation: bottom tab bar, drawer, or tabs |
| Navigation items (`navigation.items`) | `CMS-009` | at most 12 | — | — |
| Buy button (`navigation.buyButton`) | `CMS-009` | — | — | The persistent Buy tickets button (decided 29 September, MOB-2). On every screen of the mobile app except the booking and checkout steps; it opens GST-003. |
| Footer columns (`footer.columns`) | `CMS-007` | — | — | — |
| Legal links (`footer.legalLinks`) | `CMS-007` | — | — | Required links, held separately from the free-form columns — a tenant reorganising their footer must not be able to remove the privacy notice by accident. |
| Copyright text (`footer.copyrightText`) | `CMS-007` | — | — | — |
| Social links (`footer.socialLinks`) | `CMS-007` | — | — | — |
| Languages (`languages.languages`) | `CMS-011`, `ADM-018` | at least 1 | — | the language button in the header; Arabic flips every screen right to left |
| Default language (`languages.defaultLanguage`) | `CMS-011`, `ADM-018` | ISO 639-1 code, shown as the language name | — | the language a first visit opens in |
| Modules (`modules.modules`) | `CMS-001` | — | — | — |
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
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Component colours: primary CTA (`theme.componentColours.primaryCta`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | the one main call to action on each screen, when it should differ from the brand colour |
| Component colours: pay button (`theme.componentColours.payButton`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | the Pay button at checkout |
| Buy button: style (`navigation.buyButton.style`) | `CMS-009` | Raised · Floating · Flat · Hidden | Raised | the Buy tickets button in the tab bar: raised (default), floating, flat, or hidden |

**The alternate tenant theme (Coastal Aqua)**: Primary colour #0077B6; Secondary colour #023E8A; Accent colour #FFB703; Background colour #F5FAFC; Text colour #0B1324; Corner radius 18; Surface style Solid; Button style Pill; Logo variant Duotone; Header layout Logo centre; Step indicator Dots; Card layout Cards across; Card size Standard; Cart layout Floating icon; Fonts Poppins / Tajawal.
**Key screens to show in it:** `WEB-001`, `WEB-005`, `WEB-006`, `WEB-010`, `WEB-012`, `GST-001`, `GST-007`, `GST-041`, `KSK-002`, `KSK-003`.

**Never configurable:** The *Powered by TICVAI* credit in the footer is fixed and never client-editable (MoM 3 Aug, DI-111; MoM 12 Aug, DI-250). Semantic colour pairs (success, warning, danger, neutral) are not overridable: a tenant who recolours danger to their brand green has made a destructive confirmation look like a success (`screens/_design-tokens.yaml` whiteLabel). Site structure and the navigation flow are fixed and adapt to the product configuration (MoM 3 Aug, DI-119); a guest always books a product or package, never a resource (DI-502). A colour pair that fails 4.5:1 contrast is refused by the CMS, not warned (setTheme 400 ContrastProblem, audit R139).

## Reference designs and the trackers for this platform

**P02 reference designs** (from `handoff/design-batches/apps/1-guest-app/README.md`)

- `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`: Mobile App v4, the newest guest look (29 September, with the 30 September feedback in the booking flows). It replaces the 28 September Mobile v2 build.
- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the booking engine that runs inside the app. Keep both files in the same folder.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-026, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-038, DI-040, DI-042, DI-044, DI-045, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P02 as a whole** (30: 3 open, 27 closed). Open first; a closed row says where it went on 30 September.

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker)*
- **S9** Final UI/UX for the website and the mobile app *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **T1** Feedback on the revised website and mobile wireframes *(Allam / Qossai · Open · due 1 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A28** Review the 'Viva Ticket' website as a reference for ticket-flow variations *(Softlabs Design Team · Low · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A29** Collate design references/inspiration and share with TICVAI, organized by mobile app, website, and admin/back-office pages *(Softlabs (Sahil & Aishwarya) · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A55** Implement per-tenant module visibility toggles (e.g., hide Dining, Retail, or other services) configurable independently for the guest website and mobile app *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker)*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker)*
- **A115** Apply HA selectively to revenue-critical components (ticketing, POS, B2C) same-region, with multi-region DR as an optional add-on *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 24 Aug 2026 · workshop tracker)*
- **A118** Commission the third-party penetration test before go-live (ticketing, B2C, B2B, mobile apps) and resolve all severities *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 24 Aug 2026 · workshop tracker)*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker)*
- … 16 more in `handoff/design-inputs/task-tracker-index.json`

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

### Across P02 Guest App

- Font, header/footer (not yet in the current wireframe build), card size and layout are configurable in the mobile app, consistent with the web app's white-labelling approach. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1097)*
- Step-indicator style is configurable, the same as on the web: bars, dots, counters or step names. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1093)*
- Products can be presented in multiple card layout styles: carousel, video poster, split, etc. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1089)*
- The home-screen navigation bar layout is configurable: home/explore/map/buy-tickets in different arrangements. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1087)*
- The revised mobile app design is approved in direction: Qossai liked the opening video and visual polish, Allam the UI/graphics quality. Its flow is deliberately different from the web application (after front-end team input), not a reused structure. Detailed feedback to follow. *(agreed · MoM 30 Sep 2026, 4.4 Guest Mobile App — Revised Design Walkthrough · DI-1086)*
- Every web product and flow stays bookable in the mobile app (incl. cabanas, surf, 2D/3D stadium, theatre plan, bus route map), each with its own step order; a toggle switches back to one decision per screen. *(agreed · design review 29 Sep 2026, Mobile app (v4) — All web products and flows available · DI-1084)*
- Mobile app must not open straight into booking (client found it unclear). Tabs: Home · Explore · Plan · Tickets (Yas Island / Six Flags references), with a persistent "Buy tickets" button on every screen (raised centre button, or floating / flat per venue). *(agreed · design review 29 Sep 2026, Mobile app (v4) — Tabs Home · Explore · Plan · Tickets, persistent Buy tickets · DI-1081)*
- **Open question.** Real venue photos, clips and logos are still to come from the client; designs use stand-ins. Slots expected: a photo per ticket card and clip per card, a square shot per extra/shop item, one landscape poster per venue for the single-event page. Photos ≥1600 px, clips mp4 6–12 s, no audio. *(open · design review 29 Sep 2026, Asset list — TICVAI Guest Booking · DI-1080)*
- The tenant picks which logo lockup sits in the nav bar and a logo variant (Light, Dark, Duotone) whose colours drive the theme. *(agreed · design review 29 Sep 2026, CFG-4 · Brand logo + Logo palette (Light/Dark/Duotone) · DI-1068)*
- Theme settings: surface style Glass (default) or Solid cards; button style Solid (default), Outline or Pill. *(agreed · design review 29 Sep 2026, CFG-3 · Surfaces (Glass/Solid) and Buttons (Solid/Outline/Pill) · DI-1067)*
- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Guest-facing copy may say "session" (surf sessions, timed sessions) as a glossary exception, like "Booking". *(agreed · design review 29 Sep 2026, CFG-10 · 'Sessions can be added, edited or closed from Config -> Sessions' · DI-1064)*
- Optional intro video on opening the app, with a "Skip introduction" control. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1020)*
- A persistent "Buy tickets" button appears on every screen of the mobile app. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1017)*
- Mobile tabs: Home, Explore, Plan, Tickets (Yas Island / Six Flags references). *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1016)*
- The current mobile build goes straight into the booking journey and the client finds it unclear: redesign the UI. All web products and flows, including cabanas and surf, must remain available. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1015)*
- Never ask the same thing twice: table zone is picked on the table map (no zone step before it); height is asked once (height bands on the water-park day pass are the eligibility check); party/school summaries prefill headcount, child's name and age from the earlier form. *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): repeated steps removed · DI-1000)*
- Headers are reserved for standard elements only (venue image, category tabs, language bar, profile icon), applied consistently; date/availability selection belongs in the main content below the header, never in the header. Header/layout patterns must be adapted for mobile, which looks and behaves differently. *(agreed · MoM 24 Sep 2026, 4.9 Guest Web App — Specific UX Feedback (Header/Date Placement Standardization) · DI-990)*
- A language button (EN / العربية) sits in the header next to the profile icon, web and mobile. Arabic flips the whole layout right-to-left and switches interface text (navigation, buttons, booking steps, ticket names and tags, cart, seat map, checkout, account). Venue, show and dish names stay as written. *(client request · design review 23 Sep 2026, Header 2. Language icon in the header · DI-975)*
- Replace "Sign in / Create account" in the header with a single profile icon. It opens one screen with Log in and Register tabs; signed-in guests get their account menu from the same icon. *(client request · design review 23 Sep 2026, Header 1. One profile icon in the header that opens login / register · DI-974)*
- Allam's model reference: a simple card-based family-entertainment-centre site with minimal clicks, a right-side cart drawer, "help me choose", clear categories, video that autoplays when a guest taps "read more", adapting seamlessly between desktop and mobile. Allam and Qossai want this simplicity to guide the guest experience. *(client request · MoM 18 Sep 2026, 4.14 Guest Website UX Review — Upsell/Cross-Sell Placement & Reference Sites · DI-952)*
- **Open question.** Allam expects a large volume of feedback on the guest web/mobile prototype; detailed feedback goes to a separate dedicated session with Qossai and Allam. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-888)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*
- Allam: most guests book from a smartphone, so the mobile version of the booking flows is the higher priority to validate (only desktop shown). *(client request · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough · DI-684)*
- Accreditation is primarily completed in the web portal (document upload and photo checks suit a larger screen); the same submission is also available in the guest mobile app as a secondary option for individuals. *(agreed · MoM 7 Sep 2026, 4.8 Accreditation Channel Placement & API Access · DI-666)*
- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*
- Confirmed: a guest always books a product or package — never a resource (a specific room, vehicle or instructor by itself) directly — on every sales channel, including the guest/mobile app; the product's configuration determines which resources are booked behind the scenes. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-502)*
- Ticketing, F&B and retail share one cart and checkout, one unified receipt and one QR/wristband per customer — no separate receipts or wristbands per product line. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-293)*
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)*
- **Open question.** Open: publishing model — each client's own App/Play Store listing vs one universal TICVAI app where the user selects the venue; and a client module with customisation screens plus a CI/CD-linked publish action vs a canvas the client exports and publishes. Softlabs to present pros/cons. *(open · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-251)*
- Qossai: the TICVAI name must always remain visible to end users of a client-branded guest app (e.g. a "Made by TICVAI" credit) and cannot be removed by the client. *(agreed · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-250)*
- Qossai: present products with video rather than static images (as Talabat-style apps do); see benchmark app "222" for further inspiration. *(client request · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-222)*
- Qossai shared reference apps (Al Qadiya / Six Flags Saudi Arabia, and "The District" by Zomato) and cited their use of video over static images as design inspiration. *(client request · MoM 5 Aug 2026, 13. Mobile / POS App Design References · DI-146)*
- A single cart/order must take mixed purchases (e.g. family tickets plus gift vouchers) with one unified checkout and identity capture. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-141)*
- Base ticket-booking UX (web and mobile) on current market best practice rather than the demoed references as-is; Allam recommends the "Viva Ticket" website as a reference for the flow variations. *(agreed · MoM 3 Aug 2026, 10. Reference Material & Design Research · DI-125)*
- The POS/tablet application carries TICVAI's own branding and UI direction; the B2C and B2B mobile applications are white-label by design. *(agreed · MoM 31 Jul 2026, 15. Monday UI/UX Session Planning · DI-084)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Qossai: the target product is a white-label application supporting both B2C and B2B mobile use cases, built around three to four distinct flows (e.g. admission ticket flow, seat assignment flow). *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-056)*
- Selling reference layout: clean top navigation; category tabs with counts (All Events 32, Exhibitions, Guided Tours ...); sort and type chips (Price, Rating, Popular; General, Seated, Multipass, Scheduled, Rental); content cards with large image, type badge, rating, tags (LIMITED, NEW, BESTSELLER), availability ("180 available", "11 left") and "from" price; persistent cart on the right with member discount, totals and "Checkout Securely". *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, items 2-5 · DI-026)*
- Preliminary perceived-performance targets: web pages load in under about 3 seconds, mobile app loads in under about 2 seconds, ticket validation responds in under 500 milliseconds. *(agreed · MoM 28 Jul 2026, 18. Performance and Scalability · DI-015)*

### In P02 · Discovery & Browse

- "Help me choose" (experience builder) is not a consent step: its questions (yes/no, age, certified or not, etc.) filter the catalogue so only suitable products are shown (Deep Dive Dubai reference). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W4 Help me choose · DI-1005)*

**35 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"decideRecommendations": {"method":"POST","path":"/recommendations/decide","contract":"ai","summary":"Fill a recommendation slot","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRecommendationResult"},
"getAvailability": {"method":"GET","path":"/availability","contract":"catalogue","summary":"Live remaining capacity","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"performanceId","in":"query","required":null},{"name":"channelCapacityId","in":"query","required":null},{"name":"eventId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PerformanceAvailabilityPage"},
"getBundle": {"method":"GET","path":"/bundles/{bundleId}","contract":"promotions","summary":"Read a bundle with components and allocation","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Bundle"},
"getCookieConsentRuntime": {"method":"GET","path":"/storefront/cookie-consent","contract":"marketing-crm","summary":"What the page must show and what it may load","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"channel","in":"query","required":true},{"name":"brandId","in":"query","required":false},{"name":"language","in":"query","required":false},{"name":"X-Consent-Key","in":"header","required":false}],"requestBody":null,"responds":"CookieConsentRuntime"},
"getMyProfile": {"method":"GET","path":"/guests/me/profile","contract":"marketing-crm","summary":"A guest reading their own details","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[],"requestBody":null,"responds":null},
"getPerformance": {"method":"GET","path":"/performances/{performanceId}","contract":"catalogue","summary":"Read a performance","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Performance"},
"getProduct": {"method":"GET","path":"/products/{productId}","contract":"catalogue","summary":"Read a product","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Product"},
"getProductEligibilityRule": {"method":"GET","path":"/products/{productId}/eligibility-rule","contract":"catalogue","summary":"Who may take part: age, height, supervision","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productId","in":"path","required":true}],"requestBody":null,"responds":"ProductEligibilityRule"},
"getPublishedGuidedChoice": {"method":"GET","path":"/venues/{venueId}/guided-choice","contract":"white-label","summary":"The venue's published Help me choose","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuidedChoice"},
"getPublishedTenantConfig": {"method":"GET","path":"/storefront/tenant-config","contract":"white-label","summary":"The published guest-facing configuration, before anyone signs in","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"venueId","in":"query","required":false}],"requestBody":null,"responds":"PublishedTenantConfig"},
"getTenantAppStatus": {"method":"GET","path":"/tenant-config/status","contract":"white-label","summary":"App status and recent changes","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"TenantAppStatus"},
"getVenueMap": {"method":"GET","path":"/venue-maps/{mapId}","contract":"venue-map","summary":"A map with its points and paths","permission":"VENUE_MAP_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"version","in":"query","required":null},{"name":"draft","in":"query","required":null}],"requestBody":null,"responds":"VenueMapDetail"},
"getWaitTimes": {"method":"GET","path":"/queues/wait-times","contract":"queue","summary":"Wait times across a venue","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":true},{"name":"category","in":"query","required":null}],"requestBody":null,"responds":"WaitTime"},
"listAnalyticsProviders": {"method":"GET","path":"/tenant-config/analytics-providers","contract":"white-label","summary":"The analytics platforms the storefront and app report to","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMyEntitlements": {"method":"GET","path":"/guests/me/entitlements","contract":"access","summary":"Every ticket, pass and membership this guest holds","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"state","in":"query","required":null},{"name":"includeShared","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPerformances": {"method":"GET","path":"/events/{eventId}/performances","contract":"catalogue","summary":"List performances of an event","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"language","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductCategories": {"method":"GET","path":"/product-categories","contract":"catalogue","summary":"The merchandise hierarchy — categories, brands, collections","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProductCategoryNode"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPublishedContentPages": {"method":"GET","path":"/storefront/pages","contract":"white-label","summary":"The live content pages, readable before sign-in","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"categoryCode","in":"query","required":false},{"name":"slug","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"recordDeviceConsent": {"method":"POST","path":"/consent/device","contract":"marketing-crm","summary":"Record a visitor's cookie decision, before anyone is known","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RecordDeviceConsentRequest","responds":"DeviceConsent"},
"recordRecommendationEvents": {"method":"POST","path":"/recommendations/events","contract":"ai","summary":"Report what happened to recommended items","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"recordStorefrontSessionEvents": {"method":"POST","path":"/storefront/session-events","contract":"white-label","summary":"Report a batch of browsing behaviour for fraud prevention, hashed and without personal data","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WhiteLabelStorefrontSessionBatch","responds":null},
"searchCatalogue": {"method":"GET","path":"/search","contract":"catalogue","summary":"Find something by name","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"q","in":"query","required":true},{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
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
"BrandIdentity": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","description":"Every `*AssetRef` here is a `MediaAsset` id from the `assets` library (`createUpload` then `completeUpload`), PNG or SVG and at most 2 MB (decided 28 September, audit R270).\n","required":["logoAssetRef"],"properties":{"logoAssetRef":{"type":"string","format":"uuid","description":"The primary logo."},"logoDarkAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"Used on dark backgrounds. Falls back to the primary logo."},"logoVariant":{"type":"string","enum":["light","dark","duotone"],"default":"light","description":"**Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4).** `light` uses `logoAssetRef`, `dark` uses `logoDarkAssetRef` (falling back to the primary logo), and `duotone` the two-colour reading of the primary logo.\n"},"faviconAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"The browser tab icon for the guest web app."},"splashImageAssetRefs":{"type":"array","description":"Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163).","items":{"type":"string","format":"uuid"}},"splashDurationSeconds":{"type":"integer","minimum":0,"maximum":10,"default":3},"splashBackgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"showLoadingIndicator":{"type":"boolean","default":true},"splashChangeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163)."},"introVideoAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"**The optional intro video (decided 29 September, MOB-5).** A video `MediaAsset` from the media library (CMS-010). Streamed, so a change reaches guests with the publish and needs no app build.\n"},"introVideoMode":{"type":"string","enum":["off","firstLaunch","everyLaunch"],"default":"off","description":"When GST-001 plays it full screen. \"Skip introduction\" is always shown. Anything but `off` needs `introVideoAssetRef`, or 400."}}},
"Bundle": {"x-ticvai-persistence":"promotions.bundle + promotions.bundle_component","allOf":[{"$ref":"#/components/schemas/CreateBundleRequest"},{"type":"object","required":["id","savingsAmount","isActive","hasBeenSold"],"properties":{"id":{"type":"string","format":"uuid"},"savingsAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum of component list prices less the bundle price."},"savingsPercentage":{"type":"number"},"hasBeenSold":{"type":"boolean","description":"True locks components and allocation against amendment."},"isActive":{"type":"boolean"}}}]},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"ConsentSource": {"type":"string","enum":["guestApp","website","kiosk","pos","callCentre","import","agentRecorded","cookieBanner","checkout"],"description":"`checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents`, bound to the order and the verified contact. `cookieBanner` (29 September, build; BL-073 §4b): a decision made on the cookie banner or preference centre and moved onto the guest by `claimDeviceConsent`. Kept apart from `website`, a form submission, because the audit trail (2.6.56) has to tell the two apart."},
"CookieBannerPreferenceCenterDesignerView": {"type":"object","x-ticvai-persistence":"marketing.cookie_banner_design","description":"One version of a cookie banner and preference-centre design (pack 17.1.6).","required":["channel","position","languages","rejectIsOneClick","categories"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"Null for the corporate design every brand inherits."},"inheritsFromId":{"type":"string","format":"uuid","nullable":true},"channel":{"type":"string","enum":["b2cWebsite","customerPortal","mobileApp","embeddedCheckout","whiteLabelSite","partnerMicrosite"]},"logoAssetId":{"type":"string","format":"uuid","nullable":true},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedText"},"position":{"type":"string","enum":["top","bottom","popup","modal"]},"themeId":{"type":"string","nullable":true,"description":"The white-label theme it takes colours and fonts from."},"buttons":{"type":"array","items":{"type":"object","required":["action"],"properties":{"action":{"type":"string","enum":["acceptAll","rejectNonEssential","managePreferences","savePreferences","doNotSellOrShare"]},"label":{"$ref":"#/components/schemas/LocalisedText"}}}},"rejectIsOneClick":{"type":"boolean","default":true,"description":"Must be true."},"links":{"type":"array","items":{"type":"object","required":["label","policyKind"],"properties":{"label":{"$ref":"#/components/schemas/LocalisedText"},"policyKind":{"type":"string","enum":["privacy","cookie","termsAndConditions"]}}}},"categories":{"type":"array","minItems":1,"items":{"type":"object","required":["category","defaultOn"],"properties":{"category":{"type":"string","enum":["strictlyNecessary","functional","analytics","personalisation","marketing"]},"description":{"$ref":"#/components/schemas/LocalisedText"},"defaultOn":{"type":"boolean","description":"True only for `strictlyNecessary`, which is always active."}}}},"languages":{"type":"array","minItems":1,"items":{"type":"string","maxLength":10},"description":"Every language the storefront serves; Arabic renders right to left."},"regulatoryRegimes":{"type":"array","items":{"type":"string","enum":["gdpr","ePrivacy","ccpaCpra","lgpd","uaePdpl","saudiPdpl"]},"description":"2.6.60 (29 September, build). **The laws this design is published to satisfy**, so compliance is stated rather than assumed. The strictest posture (opt-in, one-click reject, every non-essential category off) already meets GDPR/ePrivacy, LGPD and both PDPLs; `ccpaCpra` adds the \"Do not sell or share\" button (`doNotSellOrShare`) and honours a Global Privacy Control signal as that opt-out."},"recordIpAddress":{"type":"boolean","default":false,"description":"2.6.55, \"if legally permitted\" (29 September, build). On, `recordDeviceConsent` writes the IP address and user agent to `pii.consent_identifier`; off, they are not kept anywhere. Off by default."},"noticeVersion":{"type":"string","readOnly":true,"description":"Moves with the cookie policy (white-label `setPolicy`, kind `cookie`)."},"version":{"type":"integer","minimum":1,"readOnly":true},"status":{"type":"string","enum":["draft","published","superseded"],"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CookieCategory": {"type":"string","enum":["strictlyNecessary","functional","analytics","personalisation","marketing"],"description":"2.6.53. The five categories the banner design (`CookieBannerPreferenceCenterDesignerView.categories`) offers; the matrix's \"preference\" category is `personalisation` (British spelling, as `ConsentPurpose`)."},
"CookieConsentChannel": {"type":"string","enum":["b2cWebsite","customerPortal","mobileApp","embeddedCheckout","whiteLabelSite","partnerMicrosite"],"description":"The six governed surfaces, as the registry and the banner design name them (pack 17.1.5-17.1.6)."},
"CookieConsentRuntime": {"type":"object","x-ticvai-persistence":"none — assembled at read time from marketing.cookie_banner_design, marketing.tracking_technology and marketing.device_consent","description":"What `getCookieConsentRuntime` gives the storefront tag loader and the app SDK gate (2.6.52, 2.6.58).","required":["banner","noticeVersion","requiresDecision","allowedTechnologies","consentModeSignals"],"properties":{"banner":{"$ref":"#/components/schemas/CookieBannerPreferenceCenterDesignerView"},"noticeVersion":{"type":"string"},"requiresDecision":{"type":"boolean","description":"True with no decision, an expired one, or one given against a superseded notice."},"decision":{"allOf":[{"$ref":"#/components/schemas/DeviceConsent"}],"nullable":true,"description":"The latest decision for the presented key; null without a key."},"allowedTechnologies":{"type":"array","description":"Per category, the approved technologies it unlocks. Anything not listed never loads.","items":{"type":"object","required":["category","technologies"],"properties":{"category":{"$ref":"#/components/schemas/CookieCategory"},"granted":{"type":"boolean","description":"Whether the presented decision grants it; always true for `strictlyNecessary`."},"technologies":{"type":"array","items":{"type":"object","required":["name","provider"],"properties":{"name":{"type":"string"},"provider":{"type":"string"},"technologyType":{"type":"string"}}}}}}},"consentModeSignals":{"type":"object","description":"**The decision in Google consent-mode terms** (2.6.65), so Analytics and Tag Manager are told, not left to guess. `denied` wherever no decision grants the category.","properties":{"adStorage":{"type":"string","enum":["granted","denied"]},"adUserData":{"type":"string","enum":["granted","denied"]},"adPersonalization":{"type":"string","enum":["granted","denied"]},"analyticsStorage":{"type":"string","enum":["granted","denied"]},"functionalityStorage":{"type":"string","enum":["granted","denied"]},"personalizationStorage":{"type":"string","enum":["granted","denied"]},"securityStorage":{"type":"string","enum":["granted"]}}}}},
"CreateBundleRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","venueId","kind","price","components","allocation"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/BundleKind"},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"components":{"type":"array","minItems":0,"items":{"$ref":"#/components/schemas/BundleComponent"}},"choiceGroups":{"type":"array","description":"Dynamic bundles (3.5.10). A bundle may carry fixed components and choice groups at once — a family pass with fixed parking and two groups the guest chooses from. **The bundle price does not move with the choice** (ADR-0019).\n","items":{"$ref":"#/components/schemas/BundleChoiceGroup"}},"allocation":{"type":"object","required":["method","components"],"properties":{"method":{"allOf":[{"$ref":"#/components/schemas/AllocationMethod"}],"default":"proRataListPrice","description":"Proportional to list price by default. The rounding remainder in the currency's minor unit goes to the first component (decided 28 September, audit R101).\n"},"components":{"type":"array","items":{"$ref":"#/components/schemas/AllocationComponent"}}}},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"campaignId":{"type":"string","format":"uuid","nullable":true,"description":"The commercial campaign (`promotions.campaign`) the bundle is sold under. (DM5, 29 September: data model for the agreed operations)"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The bundle owner (Bundle Definition & Setup). (DM5, 29 September: data model for the agreed operations)"},"category":{"type":"string","maxLength":100,"nullable":true,"description":"The bundle category the setup screen files it under. (DM5, 29 September: data model for the agreed operations)"},"isStandaloneProduct":{"type":"boolean","default":true,"description":"Whether the bundle appears as a product in its own right, or only as an offer on another product. (DM5, 29 September: data model for the agreed operations)"},"isRecommendedAtCheckout":{"type":"boolean","default":false,"description":"Whether checkout recommends the bundle. (DM5, 29 September: data model for the agreed operations)"},"requiredVariantIds":{"type":"array","nullable":true,"items":{"type":"string","format":"uuid"},"description":"Products that must already be in the basket for the bundle to be sold (the setup screen's \"requires another product\"). (DM5, 29 September: data model for the agreed operations)"}}},
"DeviceConsent": {"type":"object","x-ticvai-persistence":"marketing.device_consent + marketing.device_consent_category","description":"**One cookie decision by a visitor nobody has identified yet** (BL-073 §4b, decided 29 September). Append-only: a change of mind is a new row. Keyed for the visitor by `consentKey`, which the platform mints; the categories are child rows. The IP address and user agent, where recorded at all, are in `pii.consent_identifier` (`ConsentCaptureIdentifier`), never here.","required":["consentKey","channel","action","categories","noticeVersion","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"consentKey":{"type":"string","maxLength":64,"readOnly":true,"description":"**Opaque, minted by us, not a device fingerprint.** It answers 2.6.55's \"user identifier/session ID\" and is the join key `claimDeviceConsent` needs. Shared by all the tenant's domains (2.6.62), never across tenants."},"channel":{"$ref":"#/components/schemas/CookieConsentChannel"},"brandId":{"type":"string","format":"uuid","nullable":true},"bannerDesignId":{"type":"string","format":"uuid","nullable":true,"description":"The published `CookieBannerPreferenceCenterDesignerView` version the visitor was shown."},"action":{"$ref":"#/components/schemas/DeviceConsentAction"},"categories":{"type":"array","minItems":1,"description":"Every category of the design, with the decision this row gives it.","items":{"type":"object","required":["category","decision"],"properties":{"category":{"$ref":"#/components/schemas/CookieCategory"},"decision":{"type":"string","enum":["granted","declined"]}}}},"noticeVersion":{"type":"string","description":"The cookie notice version decided against (white-label `setPolicy`, kind `cookie`)."},"language":{"type":"string","maxLength":10,"nullable":true},"globalPrivacyControl":{"type":"boolean","default":false,"description":"The browser sent a Global Privacy Control signal; honoured as a CCPA/CPRA opt-out of sale and sharing."},"source":{"$ref":"#/components/schemas/ConsentSource"},"country":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true,"readOnly":true,"description":"The edge's geolocation of the request, for the geographic statistics (2.6.63). The address is not kept here."},"decidedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**A device consent expires and a subject consent does not.** Set from the tenant's device-consent term; after it the banner asks again."},"claimedBySubjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Set once, by `claimDeviceConsent`. Never cleared."},"claimedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005), tenant-scoped: a decision with no subject still belongs to one tenant."}}},
"DeviceConsentAction": {"type":"string","enum":["acceptAll","rejectNonEssential","savePreferences","withdraw","doNotSellOrShare"],"description":"What the visitor pressed. `doNotSellOrShare` is the CCPA/CPRA opt-out link, shown where the design's `regulatoryRegimes` include `ccpaCpra`."},
"Entitlement": {"type":"object","x-ticvai-persistence":"access.entitlement","description":"**What a guest actually holds.** Found missing on 18 August by the schema audit — 33 tables in `orders`, seven in `access`, and none of them stored an issued ticket.\nThe package sold products, defined `EntitlementTemplate`, recorded `ScanEvent.ticketId`, transferred `ticket_transfer.ticketIds` and issued `wallet_pass.entitlementId` — **five artefacts referring to a thing that did not exist.** `validateAccess` read the *template* and never the instance, and `suspendEntitlement` suspended the template, **which would have suspended it for every guest who held one.**\n**The template is the definition and this is the instance.** A template says *an annual pass admits once a day for a year*; this says *this guest's annual pass, bought on 3 March, used eleven times, frozen for two weeks in July, valid until 2 March.*\n","required":["id","templateId","productId","orderId","subjectId","status","validFrom","validTo"],"properties":{"id":{"type":"string","format":"uuid","description":"A UUIDv7, matching `TicketStatus.ticketId` — **stable for the life of the ticket and independent of the media carrying it.** A guest whose wristband broke keeps the same entitlement with a new `mediaCode`.\n**This is the ticket id.** Wherever an operation takes a `ticketId` or `ticketIds` — `lookupTicket`, `listScans`, `ScanEvent`, the offline package and `transferOrderTickets` — it is this value. An order line's `entitlementIds` are the ticket ids of that line.\n"},"templateId":{"type":"string","format":"uuid","description":"The definition it was issued against. **Pinned at issue** — a template edited next month must not change what this guest bought.\n"},"productId":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","description":"The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`)."},"orderLineId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Who holds it. **Null is legitimate** — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is claimed.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"mediaCode":{"type":"string","description":"What is scanned — a QR payload, a wristband serial, a card number. **Rotatable without reissuing**, because a guest whose wristband broke should not need a new ticket.\n"},"status":{"$ref":"../spine/orders.yaml#/components/schemas/EntitlementStatus"},"statusNote":{"type":"string","nullable":true,"description":"**Not `TicketStatus` — that is a validation result with a misleading name**, computed at scan time and carrying `isValid` and `isInsideVenue`. The lifecycle is `orders.EntitlementStatus`, and `states/entitlement-status.yaml` has modelled it since before this table existed.\n**Which is the finding in one line: the package had the lifecycle, the state model and the validation result, and no row to hang them on.**\n"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time","description":"**Resolved at issue from the template, then owned here.** A freeze extends it, a reissue replaces it, and neither reaches back to the template.\n**What the pre-expiry notice is measured from** (29 September, build pass, group G2; 5.5.30). A daily run in access publishes `entitlement.expiringSoon` once per entitlement and `validTo` when an entitlement in `issued` or `partiallyConsumed` comes within its template's `expiryNoticeDays` (`catalogue.EntitlementTemplate`), and not for one bought inside that window. Marketing turns it into the reminder (a `MessageTrigger` on the event, or a triggered campaign on `entitlementExpiring`); access only says the date is near. A freeze or renewal that moves `validTo` raises the next notice once.\n"},"entriesUsed":{"type":"integer","default":0,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**The number `validateAccess` decrements and nothing was decrementing.** A ten-entry pass with no counter is a ten-entry pass that admits forever.\n**Maintained on write**, in the same transaction as the admitting `access.scan_event` row: by `validateAccess`, `validateGroupAccess` (by the count admitted) and `syncScans` for each replayed admission the server accepts. A replayed scan the server downgrades to `denied` does not count.\n"},"entriesAllowed":{"type":"integer","nullable":true},"lastEntryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`recordedAt` of the latest admission counted in `entriesUsed`, written by the same writes. A scan replayed late with an earlier `recordedAt` does not move it back.\n"},"frozenDays":{"type":"integer","default":0,"readOnly":true,"x-ticvai-derived":"onWrite","description":"Days added by a freeze. **Maintained on write** by the freeze operation (`freezeEntitlement`), in the same write that extends `validTo` by those days. **Held here rather than computed from a freeze log**, because a gate has to answer in under 300ms and cannot replay a history to decide validity.\n"},"suspendedReason":{"type":"string","nullable":true},"freezeReason":{"type":"string","nullable":true,"enum":["travelling","injury","personal","seasonal","other"],"description":"The `reason` of the latest `freezeEntitlement` (audit R222). Null when never frozen."},"freezeNote":{"type":"string","nullable":true,"maxLength":500,"description":"The `note` the latest `freezeEntitlement` took, required there when `reason` is `other` (decided 28 September, audit R222). Kept so the quarterly review of `other` notes has something to read."},"isNameBound":{"type":"boolean","default":false},"holderName":{"type":"string","nullable":true},"sharedWithSubjectIds":{"type":"array","description":"`shareEntitlement`. **The owner keeps it and a second person may present it** — the asymmetry that stops a shared family pass becoming a resale chain.\n","items":{"type":"string","format":"uuid"}},"issuedVia":{"type":"string","enum":["sale","invitation","reissue","transfer","resale","membership","groupBooking"],"description":"**How it came to exist, and it matters to finance.** A sold entitlement carries deferred revenue; an invitation carries a marketing cost; a reissue carries neither.\n"},"supersedesEntitlementId":{"type":"string","format":"uuid","nullable":true,"description":"For a reissue or a resale. **The chain is traceable** — a ticket appearing from nowhere is indistinguishable from a fraudulent one.\n"},"walletValueId":{"type":"string","format":"uuid","nullable":true,"description":"Where the template carries stored value. **A `retail.Wallet` bound to the entitlement, not a balance on it** (CF-126).\n"},"facePassEnrolmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"The active `facePass` enrolment on this entitlement (`FacePassEnrolment.id`), or null when none is. **Computed on read from `pii.subject_biometric` and not stored here** — the PII split keeps the biometric on its own side, and this carries only its id. It is how a screen holding a pass finds the enrolment `getFacePassEnrolment` and `revokeFacePass` take.\n"}}},
"FontConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["primaryLatin"],"properties":{"primaryLatin":{"type":"string"},"primaryArabic":{"type":"string","nullable":true,"description":"Required when `ar` is among the tenant's languages (audit R163). A Latin face alone leaves Arabic in a system fallback that will not match.\n"},"secondaryLatin":{"type":"string","nullable":true},"secondaryArabic":{"type":"string","nullable":true,"description":"Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163)."},"customFontAssetRefs":{"type":"array","description":"Uploaded font files, as `MediaAsset` ids.","items":{"type":"string","format":"uuid"}},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"x-ticvai-derived":"onRead","description":"Custom font files are `buildTime`; selecting a bundled face is `runtime`."}}},
"FooterConfig": {"type":"object","x-ticvai-persistence":"whitelabel.footer_config + whitelabel.footer_config_column + whitelabel.footer_config_social_link","description":"BL-002. **`setHeader` and `HeaderConfig` exist and the footer does not**, which looked like symmetry until you notice it is not: **a header is chrome and a footer is a link surface.**\nA footer carries the legal links — terms, privacy, accessibility statement, cookie preferences — and **those are the ones a regulator checks.** Treating it as a mirror of the header would have given it a logo and no way to reach a privacy notice.\n**Where it is stored.** `legalLinks` and `copyrightText` are columns of `whitelabel.footer_config`; each entry of `columns` is a `whitelabel.footer_config_column` row and each entry of `socialLinks` a `whitelabel.footer_config_social_link` row. Part of the working draft (see the header). **In the tenant's own database, not the control plane (decided 28 September, audit R163)**: it moved from `control.footer_config` and its two child tables.\n","required":["id","scopePath"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005), written at `tenant` scope by the server."},"columns":{"type":"array","items":{"type":"object","properties":{"heading":{"type":"string"},"links":{"type":"array","items":{"type":"object","properties":{"label":{"type":"string"},"url":{"type":"string"},"opensCookiePreferences":{"type":"boolean","default":false}}}}}}},"legalLinks":{"type":"object","description":"**Required links, held separately from the free-form columns** — a tenant reorganising their footer must not be able to remove the privacy notice by accident.\n","properties":{"termsUrl":{"type":"string"},"privacyUrl":{"type":"string"},"accessibilityUrl":{"type":"string","nullable":true},"cookiePolicyUrl":{"type":"string","nullable":true}}},"copyrightText":{"type":"string"},"socialLinks":{"type":"array","items":{"type":"object","properties":{"platform":{"type":"string"},"url":{"type":"string"}}}}}},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"GuestPreferences": {"type":"object","x-ticvai-persistence":"marketing.guest_preference","description":"**What the guest likes, kept apart from what they permit** (consent) and from who they are (the profile). One row per subject. `dietary` and `accessibility` are here rather than as tags because BL-134 gives them their own consent purpose and retention.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true},"subjectId":{"type":"string","format":"uuid","readOnly":true},"seatingPreference":{"type":"string","nullable":true,"maxLength":200},"drinkPreferences":{"type":"array","items":{"type":"string"}},"dietary":{"type":"array","description":"Also written by `updateMyProfile`.","items":{"type":"string"}},"accessibility":{"type":"array","description":"Also written by `updateMyProfile`.","items":{"type":"string"}},"preferredChannel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"x-ticvai-persisted":false,"description":"**Stored on the profile** (`GuestProfile.preferredChannel`) — carried here because the preference screen edits it beside the rest.\n"},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"GuestProfile": {"x-ticvai-persistence":"marketing.guest_profile","type":"object","required":["subjectId","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"subjectId":{"type":"string","format":"uuid","description":"Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger.\n"},"displayName":{"type":"string","nullable":true},"email":{"type":"string","nullable":true},"phone":{"type":"string","nullable":true},"preferredLanguage":{"type":"string","nullable":true},"preferredChannel":{"$ref":"#/components/schemas/MessageChannel"},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells. Marketing acts locally."},"tags":{"type":"array","items":{"type":"string"}},"engagementScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"description":"22.2.20 and 22.2.21. **`lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not.** They are different questions: a guest who spent a lot once and a guest who visits monthly have the same LTV and need opposite treatment.\n**Recency, frequency and breadth, not spend** — spend is already `lifetimeValue`, and folding it in here would make one number twice.\n"},"engagementTier":{"type":"string","nullable":true,"enum":["new","active","occasional","lapsing","lapsed","dormant"],"description":"5.3.19. **Automatic classification, computed rather than assigned.** `lapsing` is the tier the whole field exists for — **a guest who has not been for a while and still might is the only one marketing can change**, and lumping them with `lapsed` wastes the window.\n"},"lifetimeValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"visitCount":{"type":"integer"},"lastVisitAt":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"},"mergedIntoSubjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`**, which retain it as a redirect rather than deleting it. A read that lands here follows it; a second merge of a profile that has one is refused as `alreadyMerged`.\n"},"mergedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"GuidedChoice": {"x-ticvai-persistence":"whitelabel.guided_choice + whitelabel.guided_choice_question + whitelabel.guided_choice_answer","type":"object","description":"**Help me choose (decided 29 September, rev 3 REV3-11).** A venue's short set of questions that ends on a result card opening the booking flow, product, category or event that fits. Each question has a few answers with a title, a one-line body, an icon and an optional badge; **the answer the guest picks on the last question decides the result**, and each earlier answer carries a target too, so a one-question setting still ends on a result. Venue configuration, never hard-coded: set up in Venue Management, off unless the venue publishes one.\n**Two sources, one review.** `manual` is written by staff; `aiSuggested` is proposed by the `ai` service from the venue's uploaded products (a suggestion, reviewed and published by a person, never auto-published). Both arrive as `draft`.\n**Help me choose filters the catalogue (decided 29 September, W4).** With `behaviour` `filter`, the default, each answer's `filter` narrows the products the guest sees (web, mobile and kiosk alike, through catalogue `listProducts` and `searchCatalogue` `guidedAnswerIds`), with a \"Show everything\" link; `recommend` keeps the rev 3 result card from the last answer's `target`. **It is never a consent step**: an answer may pre-fill a REV3-26 consent question (`consentPrefill`), which the guest still confirms, so the question is not asked twice and the consent stays explicit.\n","required":["id","venueId","name","mode","questions","status","source"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"UUIDv7."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `createGuidedChoice`."},"name":{"type":"string","maxLength":80,"description":"Staff-facing name, e.g. \"Water park day planner\". Not shown to guests."},"mode":{"type":"string","enum":["button","popupOnArrival","off"],"default":"button","description":"**How the guest reaches it (rev 3 REV3-11).** `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on the guest's first arrival at the booking page (whether it was seen is kept on the device only); `off` keeps a published choice configured but not shown.\n"},"showBanner":{"type":"boolean","default":true,"description":"The dark banner under the products (\"Choose from the experiences above or let us help you decide\") with a Help me choose button. Ignored when `mode` is `off`."},"behaviour":{"type":"string","enum":["filter","recommend"],"default":"filter","description":"**`filter` (default) narrows the list; `recommend` ends on one result card (decided 29 September, W4).** With `filter`, every answer needs a `filter` and `target` is optional; with `recommend`, every answer on the last question needs a `target`. `publishGuidedChoice` refuses the other case with 422.\n"},"showEverything":{"type":"boolean","default":true,"description":"The \"Show everything\" link under a filtered list, which clears the answers (W4)."},"questions":{"type":"array","minItems":1,"maxItems":4,"description":"**One to four questions** (decided 29 September, W4: the Deep Dive reference asks three or four; rev 3 REV3-11 allowed two). Shown in `sortOrder`.\n","items":{"type":"object","required":["title","sortOrder","answers"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"UUIDv7. The row's own key."},"title":{"$ref":"#/components/schemas/LocalisedText"},"kind":{"type":"string","enum":["choice","yesNo","age","level","certification"],"default":"choice","description":"**What the question asks (decided 29 September, W4).** `choice` free answers; `yesNo` two answers (e.g. \"Can everyone swim?\"); `age` answers carrying an age range; `level` answers carrying a level tag; `certification` answers saying whether the guest holds a certificate (e.g. a diving licence). The kind decides which `filter` fields its answers use.\n"},"sortOrder":{"type":"integer","minimum":0},"answers":{"type":"array","minItems":2,"maxItems":4,"description":"Two to four answers; the prototype shows three (proposed, client to correct, rev 3 REV3-11).","items":{"type":"object","required":["title","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"UUIDv7. The row's own key."},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"The one-liner under the title, at most 140 characters in each language."},"icon":{"type":"string","maxLength":40,"nullable":true,"description":"An icon name from the guest app's icon set."},"badge":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Optional, e.g. \"Best value\". At most 24 characters in each language."},"sortOrder":{"type":"integer","minimum":0},"target":{"allOf":[{"$ref":"#/components/schemas/GuidedChoiceTarget"}],"nullable":true,"description":"Required with `behaviour` `recommend` on the last question; optional with `filter`, where it is the card shown above the filtered list."},"filter":{"type":"object","nullable":true,"description":"**What this answer keeps in the list (decided 29 September, W4).** Every field set must hold; answers to different questions are combined with AND. Required with `behaviour` `filter`. The server applies it (catalogue `guidedAnswerIds`), so web, mobile and kiosk show the same list.\n","properties":{"productIds":{"type":"array","items":{"type":"string","format":"uuid"}},"productCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"segmentTags":{"type":"array","description":"Catalogue `Product.segmentTags`, e.g. a level tag.","items":{"type":"string"}},"minAgeYears":{"type":"integer","minimum":0,"nullable":true},"maxAgeYears":{"type":"integer","minimum":0,"nullable":true,"description":"With `minAgeYears`, checked against each product's age rule (catalogue `ProductEligibilityRule`)."},"requiresSwimmer":{"type":"boolean","nullable":true,"description":"False hides products whose eligibility needs a swimmer; true keeps only those."},"certificationCode":{"type":"string","nullable":true,"maxLength":40,"description":"Keeps products that need this certificate, or with `holdsCertification` false, hides them."},"holdsCertification":{"type":"boolean","nullable":true}}},"consentPrefill":{"type":"object","nullable":true,"description":"**Pre-fills a REV3-26 consent question from this answer (decided 29 September, W4).** The guest still ticks it at the consent step; nothing is recorded as consent until they do.\n","required":["consentQuestionId","answer"],"properties":{"consentQuestionId":{"type":"string","format":"uuid"},"answer":{"type":"boolean"}}},"result":{"type":"object","nullable":true,"description":"The result card when this answer decides the result. Absent fields fall back to the target's own name, summary and image.","properties":{"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedText"},"imageAssetRef":{"type":"string","format":"uuid","nullable":true}}}}}}}}},"status":{"allOf":[{"$ref":"#/components/schemas/GuidedChoiceStatus"}],"readOnly":true},"source":{"type":"string","enum":["manual","aiSuggested"],"readOnly":true,"description":"`manual` when staff created it; `aiSuggested` when the `ai` service proposed it (a service caller). Kept after a person edits a suggestion, so a report can say how many AI proposals were published."},"suggestionRef":{"type":"string","nullable":true,"readOnly":true,"description":"For `aiSuggested`, the id of the `ai` job that proposed it. Null for `manual`."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"publishedBy":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The person who published it. Never a service."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"GuidedChoiceStatus": {"type":"string","description":"**Draft until a person publishes it (decided 29 September, rev 3 REV3-11).** Guests see only a `published` choice. An AI-proposed choice arrives as `draft` and is never published by the system. Moves as `states/guided-choice.yaml` says: `publishGuidedChoice` and `unpublishGuidedChoice`, and a publish returns the venue's previously published choice to `draft`.\n","enum":["draft","published"],"default":"draft"},
"GuidedChoiceTarget": {"x-ticvai-persistence":"none — embedded","type":"object","description":"**What an answer opens (decided 29 September, rev 3 REV3-11).** A product (its kind picks the booking flow), a product category (its tickets, as `ticketCategories` shows them), an event, or a module such as `membership`. Each id must belong to the choice's venue and be on sale or enabled when the choice is published, or `publishGuidedChoice` refuses it.\n","required":["kind"],"properties":{"kind":{"type":"string","enum":["product","productCategory","event","module","bookingFlow"]},"productId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `product`. A catalogue `Product`."},"productCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `productCategory`. A catalogue `ProductCategory`."},"eventId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `event`."},"moduleKey":{"allOf":[{"$ref":"#/components/schemas/ModuleKey"}],"nullable":true,"description":"Required when `kind` is `module`. The module must be enabled."},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `bookingFlow` (decided 29 September, W12; BUILD-YOUR-EXPERIENCE \"each answer points to one booking flow\"). One of the venue's enabled `BookingFlow`s."}}},
"HeaderConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["layout"],"properties":{"layout":{"type":"string","enum":["logoLeft","logoCentre","logoWithMenu"]},"showLogo":{"type":"boolean","default":true},"showMenu":{"type":"boolean","default":true},"showNotifications":{"type":"boolean","default":true},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},
"HomepageLayout": {"x-ticvai-persistence":"whitelabel.homepage_section","type":"object","required":["sections"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"sections":{"type":"array","items":{"type":"object","required":["kind","sortOrder","isVisible"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"kind":{"$ref":"#/components/schemas/HomepageSectionKind"},"title":{"$ref":"#/components/schemas/LocalisedText"},"sortOrder":{"type":"integer"},"isVisible":{"type":"boolean"},"contentPageId":{"type":"string","format":"uuid","nullable":true},"maxItems":{"type":"integer","nullable":true,"description":"How many items the section shows. On the mobile Home, `attractions`, `dining`, `whatsOn` and `shop` show 1 or 2 highlights (decided 29 September, MOB-3)."},"heroStyle":{"type":"string","nullable":true,"enum":["carousel","video","poster","split",null],"description":"For `heroBanner` only (decided 29 September, MOB-3)."}}}}}},
"LanguageConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["languages","defaultLanguage"],"properties":{"languages":{"type":"array","items":{"type":"string","pattern":"^[a-z]{2}$"}},"defaultLanguage":{"type":"string","pattern":"^[a-z]{2}$"},"rtlLanguages":{"type":"array","readOnly":true,"x-ticvai-derived":"onRead","description":"The enabled languages written right to left — those whose Unicode CLDR character order is `right-to-left` (Arabic, `ar`, among them). Not configured; it follows from `languages`.","items":{"type":"string","pattern":"^[a-z]{2}$"}},"translationGaps":{"type":"array","readOnly":true,"description":"Content lacking a version in an enabled language.","items":{"type":"object","properties":{"language":{"type":"string"},"missingCount":{"type":"integer"},"areas":{"type":"array","items":{"type":"string"}}}}}}},
"LocalisedRichText": {"x-ticvai-persistence":"none — jsonb column","type":"object","description":"Keyed by language code. Values are sanitised HTML.","additionalProperties":{"type":"string"}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MinimumAppVersion": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n","properties":{"ios":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"},"android":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"}}},
"ModuleKey": {"type":"string","enum":["ticketsAndBooking","membership","events","attractions","virtualQueue","diningAndFnb","shop","parking","gamification","photoGallery","wallet","loyalty","lostAndFound","map","visitPlanner"],"description":"`visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown."},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"NavigationConfig": {"x-ticvai-persistence":"whitelabel.navigation_item","type":"object","description":"**The mobile tab set is venue configuration (decided 29 September, MOB-1; 29 September brief decision 6).** Before a tenant saves its own, `bottomNavigation` is Home, Explore, Plan and Tickets (each an `appSection` link), with the Buy tickets button beside them; Map is an optional tab. Plan is left out while `visitPlanner` is off.\n","required":["kind","items"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"kind":{"type":"string","enum":["bottomNavigation","drawer","tabs"]},"items":{"type":"array","maxItems":12,"items":{"type":"object","required":["label","target","isVisible","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"label":{"$ref":"#/components/schemas/LocalisedText"},"icon":{"type":"string"},"target":{"$ref":"#/components/schemas/LinkTarget"},"isVisible":{"type":"boolean","description":"At most five may be visible in bottom navigation; the rest overflow."},"sortOrder":{"type":"integer"}}}},"buyButton":{"type":"object","nullable":true,"description":"**The persistent Buy tickets button (decided 29 September, MOB-2).** On every screen of the mobile app except the booking and checkout steps; it opens GST-003. Read with `bottomNavigation`.\n","properties":{"style":{"type":"string","enum":["raised","floating","flat","hidden"],"default":"raised","description":"`raised` sits in the centre of the tab bar, as the v4 prototype shows; `hidden` turns it off."},"label":{"$ref":"#/components/schemas/LocalisedText"}}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Performance": {"x-ticvai-persistence":"catalogue.performance","type":"object","required":["id","eventId","startsAt","endsAt","status"],"properties":{"id":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"description":"BL-048. **The approval chain and the occurrence lifecycle sat on different entities**, so neither was complete: `states/performance.yaml` models scheduled, onSale, soldOut, suspended, cancelled and completed properly, and nothing said which of those transitions somebody had to sign.\n**Set on the transition that needs it, not on the performance.** Publishing a performance is routine; cancelling one that has sold is the act somebody signs — and binding approval to the whole entity would have required a signature to reschedule a wet Tuesday.\n"},"requiresApprovalToCancel":{"type":"boolean","default":true,"description":"**Cancelling a sold performance is the one transition that needs a name against it.** `assessProductChange` already answers how many tickets are affected; this decides who has to look at that number before the button works.\n"},"status":{"type":"string","enum":["scheduled","onSale","soldOut","suspended","cancelled","completed"]},"admissionRulesId":{"type":"string","format":"uuid","nullable":true},"seatMapId":{"type":"string","format":"uuid","nullable":true},"language":{"type":"string","nullable":true,"maxLength":35,"pattern":"^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$","description":"The language the performance is given in, as a BCP 47 tag (`en`, `ar`, `fr`, `de`, `zh`, `ru`, `ar-AE`). **A guided tour at 10:00 in French and one at 10:00 in Arabic are two performances**, so a guest who picks a language sees only the tours in it (`listPerformances` `language`). Null when the performance is not language-specific (decided 29 September, rev 3 REV3-17).\n"},"format":{"type":"string","nullable":true,"maxLength":40,"description":"How it is presented, free text the venue chooses, e.g. `2D`, `3D`, `IMAX`, `subtitled`. A cinema screening shows language and format together. Null when it does not apply (decided 29 September, rev 3 REV3-17).\n"}}},
"PerformanceAvailability": {"type":"object","x-ticvai-persistence":"none — computed on read from catalogue.channel_capacity and live leases","description":"Remaining capacity of one channel capacity of one performance (rev 3 REV3-1).","required":["channelCapacityId","performanceId","capacity","sold","leased","remaining"],"properties":{"channelCapacityId":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid","description":"The performance this channel capacity belongs to (`ChannelCapacity.performanceId`), so rows for several performances can be told apart."},"startsAt":{"type":"string","format":"date-time","readOnly":true,"description":"The performance's start, so a time tile and its day part (morning, afternoon, evening, split at the venue's `BookingFlowConfig.dayPartBoundaries`) come from this one call (rev 3 REV3-1)."},"capacity":{"type":"integer"},"sold":{"type":"integer"},"leased":{"type":"integer","description":"Held by terminals but not yet sold."},"remaining":{"type":"integer"},"byChannel":{"type":"array","description":"Per-channel position. A guest seeing sold out online while units remain at the counter is correct behaviour, not a defect.\n","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/Channel"},"allocated":{"type":"integer"},"sold":{"type":"integer"},"remaining":{"type":"integer"}}}}}},
"PerformanceAvailabilityPage": {"x-ticvai-persistence":"none — computed on read","description":"The `getAvailability` answer (named 29 September, rev 3 REV3-1).","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Page"},{"type":"object","properties":{"items":{"type":"array","items":{"$ref":"#/components/schemas/PerformanceAvailability"}}}}]},
"PlacedResource": {"type":"object","x-ticvai-persistence":"venuemap.placed_resource","description":"**A bookable resource where it stands on the map** (decided 29 September, rev 3 REV3-15 and GAP-C2): cabana B09 on the Beach, 15 guests, Large. The resource itself, its bookings and its holds live in `resources`; this row says where it is drawn and what the guest sees. Written into the working draft by `importVenueGeometry` or `setPlacedResource`, copied into the `VenueMapVersion` snapshot at publish. A guest picks one on the published map, holds it with `resources.createResourceHold` and buys it. **Supersedes audit R073 (c) and the 26 August minute for resources on an ingested map.**\n","required":["id","mapId","resourceId","label","kind","zone","capacity","priceBandCode","position"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes it."},"resourceId":{"type":"string","format":"uuid","x-ticvai-references":"resources.Resource","description":"The `resources.Resource` this is. **Availability, holds and bookings are keyed by this**, so a republished map with the cabana moved keeps its bookings.\n"},"label":{"type":"string","maxLength":40,"x-ticvai-unique":"map","description":"What the guest sees and taps, e.g. `B09`. **Unique on the map**, compared without case after digit normalisation; normally the resource's `code`.\n"},"kind":{"type":"string","enum":["cabana","lounger","table","pitch","other"],"description":"A subset of `resources.ResourceKind`, the kinds a guest books from a map. A `table` here is a non-dining spot (a beach or event table) sold like a cabana; restaurant tables stay `fnb` table reservations (decided 29 September, rev 3 GAP-C2)."},"zone":{"type":"string","maxLength":80,"description":"The area the guest reads it by, e.g. `Beach`, `River`, `Terrace`."},"capacity":{"type":"integer","minimum":1,"maximum":500,"description":"Guests it takes, e.g. 15. Shown on the map and checked against the party at hold."},"priceBandCode":{"type":"string","maxLength":40,"description":"The band it sells in, e.g. `Large`, one of the `priceBands` given at import. The band's `variantId` prices it; the map holds no price.\n"},"variantId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"catalogue.ProductVariant","description":"Resolved from the price band. What a cart line for this resource names."},"position":{"type":"object","required":["x","y"],"description":"Drawing coordinates of its label anchor, as on `VenuePoint`.","properties":{"x":{"type":"number"},"y":{"type":"number"}}},"boundary":{"type":"array","nullable":true,"description":"The shape drawn, as a polygon in drawing coordinates. Null for a pin.","items":{"type":"object","properties":{"x":{"type":"number"},"y":{"type":"number"}}}},"isBookable":{"type":"boolean","default":true,"description":"False keeps it on the map and off sale, e.g. a cabana kept for staff use. Shown greyed.\n"}}},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true}}},
"ProductCategory": {"type":"object","x-ticvai-persistence":"catalogue.product_category","description":"Retail Board 2 of the client's design set, 20 August. **`listSeatCategories` existed and a product category did not** — a seat category prices a seat, and a merchandise hierarchy groups a catalogue.\n**Brand sits here rather than as its own entity.** A venue with four brands and a hierarchy five levels deep can express that with a parent; a venue with one brand should not have to maintain a table containing one row.\n**`displayOrder` is not alphabetical and that is the point.** A retail category list runs in the order the merchandiser wants a guest to see it, and sorting by name puts *Accessories* above *Apparel* forever.\n","required":["id","name","kind"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"code":{"type":"string","maxLength":64,"nullable":true,"x-ticvai-unique":"tenant","description":"**Taken from their category tables, 20 September.** Ours had a uuid and a localised name, so an importer matching *Beverages* had to match on a display string that a venue is free to translate.\n**Unique per tenant where set** (decided 28 September, audit R108): two categories in one tenant never share a code, and `setProductCategories` refuses a body that would, with `409 duplicate-code`.\n"},"nameLocalised":{"type":"object","additionalProperties":{"type":"string"}},"kind":{"type":"string","enum":["category","brand","collection","season","department"]},"parentId":{"type":"string","format":"uuid","nullable":true,"description":"**One tree, not four.** A brand under a department under a category is how a real merchandise hierarchy runs, and separate tables for each level cannot express a venue that nests them differently.\n"},"scopePath":{"type":"string","readOnly":true,"description":"Set by the server from the venue the caller acts at; not sent."},"displayOrder":{"type":"integer","default":100},"imageAssetId":{"type":"string","format":"uuid","nullable":true},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The short line a guest reads under a category option, e.g. *Surf lessons: learn on the beginner wave with a coach* (decided 29 September, rev 3 REV3-19). Each language value at most 200 characters.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow for every product filed here** that names none of its own (decided 29 September, W12, BO-115). Null means the venue's flow for each product's `kind`. A white-label `BookingFlow` of the venue; `setProductCategories` refuses any other id with `422`.\n"},"isActive":{"type":"boolean","default":true,"description":"**Deactivated rather than deleted.** A category with a season behind it still names the products sold under it, and removing it rewrites last year's report.\n"}}},
"ProductCategoryNode": {"x-ticvai-persistence":"none — projection over catalogue.product_category","description":"**One node of the tree `listProductCategories` returns.** A `ProductCategory` with its children nested under it, in `displayOrder`, so no caller reassembles the hierarchy from `parentId`. `setProductCategories` still takes the flat list, because a write names each parent by id.\n","allOf":[{"$ref":"#/components/schemas/ProductCategory"},{"type":"object","required":["children"],"properties":{"children":{"type":"array","description":"Empty on a leaf.","items":{"$ref":"#/components/schemas/ProductCategoryNode"}}}}]},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductEligibilityRule": {"type":"object","x-ticvai-persistence":"catalogue.product_eligibility_rule","description":"Participation limits for one product. Absent means anyone may take part, and `getProductEligibilityRule` returns that absence as this schema with every limit null, never as a `404`.","properties":{"id":{"type":"string","format":"uuid","readOnly":true},"productId":{"type":"string","readOnly":true},"minAgeYears":{"type":"integer","minimum":0,"nullable":true},"maxAgeYears":{"type":"integer","minimum":0,"nullable":true},"minHeightCm":{"type":"integer","minimum":50,"maximum":250,"nullable":true},"maxHeightCm":{"type":"integer","minimum":50,"maximum":250,"nullable":true},"heightBandsCm":{"type":"array","items":{"type":"integer"},"default":[120,140],"description":"Band edges the guest chooses between, e.g. under 1.20 m, 1.20–1.40 m, 1.40 m and over."},"accompaniedBelowAge":{"type":"integer","nullable":true,"description":"Under this age an adult must be present, e.g. 8 at the kids club."},"guardianSignatureAgeFrom":{"type":"integer","nullable":true},"guardianSignatureAgeTo":{"type":"integer","nullable":true,"description":"Ages needing a guardian's signature, e.g. 12–15 on a thrill ride."},"waiverRequired":{"type":"boolean","default":false},"swimAbility":{"type":"string","enum":["notRequired","confident"],"default":"notRequired","deprecated":true,"description":"**Superseded for the guest's answer** (decided 29 September, rev 3 REV3-26): the swim question is a consent, not a data field. A venue attaches *Are you able to swim?* as a consent question (`Product.consentQuestionIds`), with its own text, version and whether it is asked per person or once per booking, and the answer is a consent record. Kept so existing rules read; a new product should use a consent question instead.\n"},"refundableIfIneligibleAtGate":{"type":"boolean","default":false},"requiredCertificationCode":{"type":"string","nullable":true,"maxLength":60,"description":"**A certification the participant must hold** (decided 29 September, W4; added 30 September), e.g. `padiOpenWater` for a dive. Null means none. Help me choose reads it: an answer whose `filter.certificationCode` names it with `holdsCertification: false` leaves the product out, and with `holdsCertification: true` (or no flag) keeps only products needing that certification or none. Proof, where the venue asks for it, is a consent question on the product (REV3-26), not this field."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"PublishedContentPage": {"x-ticvai-persistence":"none — a public projection of whitelabel.content_page","type":"object","x-ticvai-agreed":"2 October: decided by Chinmay, fix before Block A starts (GFIX-2)","description":"A live content page as a guest reads it (`listPublishedContentPages`). Only published and enabled pages exist in this view, so it carries no status.","required":["id","slug","title","body"],"properties":{"id":{"type":"string","format":"uuid"},"slug":{"type":"string","pattern":"^[a-z0-9-]+$"},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedRichText"},"iconAssetRef":{"type":"string","format":"uuid","nullable":true},"categoryCode":{"type":"string","nullable":true},"sortOrder":{"type":"integer"}}},
"PublishedTenantConfig": {"x-ticvai-persistence":"none — computed from the current ConfigVersion snapshot and the live status on whitelabel.tenant_config","type":"object","x-ticvai-agreed":"2 October: decided by Chinmay, fix before Block A starts (GFIX-1)","description":"**The public view of the tenant's configuration** (`getPublishedTenantConfig`, decided 2 October, GFIX-1). The published parts a guest surface renders with, from the current `ConfigVersion`, and the live status `setMaintenanceMode` writes. Nothing a guest cannot see on the page: no draft marker, no CMS counts, no sender addresses, no licensing, no person.\n","required":["tenantId","publishedVersion","publishedAt","isInMaintenance"],"properties":{"tenantId":{"type":"string","format":"uuid"},"publishedVersion":{"type":"string","description":"The `ConfigVersion.version` this answer was read from; a client holding the same version keeps its copy."},"publishedAt":{"type":"string","format":"date-time"},"brand":{"$ref":"#/components/schemas/BrandIdentity"},"appIcons":{"$ref":"#/components/schemas/AppIcons"},"theme":{"$ref":"#/components/schemas/Theme"},"fonts":{"$ref":"#/components/schemas/FontConfig"},"header":{"$ref":"#/components/schemas/HeaderConfig"},"footer":{"$ref":"#/components/schemas/FooterConfig"},"navigation":{"$ref":"#/components/schemas/NavigationConfig"},"homepage":{"$ref":"#/components/schemas/HomepageLayout"},"bookingFlow":{"allOf":[{"$ref":"#/components/schemas/BookingFlowConfig"}],"description":"The booking-flow display settings, resolved for `venueId` when one was sent (the tenant's values with that venue's `venueOverrides` entry laid over, rev 3 CFG-11)."},"languages":{"$ref":"#/components/schemas/LanguageConfig"},"accessibility":{"$ref":"#/components/schemas/AccessibilitySettings"},"enabledModules":{"type":"array","description":"The modules the tenant has enabled and published, so a guest surface hides a tab or a homepage section for a module that is off. Licensing is not shown.","items":{"$ref":"#/components/schemas/ModuleKey"}},"enabledFeatures":{"type":"array","description":"The `featureKey` of every feature toggle that is on in the published version.","items":{"type":"string"}},"isInMaintenance":{"type":"boolean","description":"Live state (`setMaintenanceMode`), as on `getTenantAppStatus`."},"maintenanceMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"$ref":"#/components/schemas/MinimumAppVersion"},"availability":{"$ref":"#/components/schemas/AppAvailability"},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"contact":{"$ref":"#/components/schemas/VenueContact"}}},
"QueueStatus": {"type":"string","enum":["open","paused","closed","atCapacity"]},
"RecordDeviceConsentRequest": {"type":"object","x-ticvai-persistence":"none — request only","description":"What the banner or preference centre sends to `recordDeviceConsent`.","required":["channel","action","noticeVersion","decidedAt"],"properties":{"consentKey":{"type":"string","maxLength":64,"nullable":true,"description":"The key the browser or app already holds; omitted on a first decision, and one is minted."},"channel":{"$ref":"#/components/schemas/CookieConsentChannel"},"brandId":{"type":"string","format":"uuid","nullable":true},"bannerDesignId":{"type":"string","format":"uuid","nullable":true},"action":{"$ref":"#/components/schemas/DeviceConsentAction"},"categories":{"type":"array","description":"Required for `savePreferences`; ignored for the other actions, which decide every category themselves.","items":{"type":"object","required":["category","decision"],"properties":{"category":{"$ref":"#/components/schemas/CookieCategory"},"decision":{"type":"string","enum":["granted","declined"]}}}},"noticeVersion":{"type":"string"},"language":{"type":"string","maxLength":10,"nullable":true},"globalPrivacyControl":{"type":"boolean","default":false},"source":{"$ref":"#/components/schemas/ConsentSource"},"decidedAt":{"type":"string","format":"date-time"}}},
"StorefrontAnalyticsProvider": {"type":"object","x-ticvai-persistence":"whitelabel.analytics_provider","description":"**One analytics platform the storefront or app reports to** (22.10.29, 29 September build). Venue configuration: a null `venueId` is the tenant-wide default a venue's own row replaces.","required":["provider","measurementId","surfaces","consentCategory","isEnabled"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","nullable":true},"provider":{"type":"string","enum":["googleAnalytics4","googleTagManager","adobeAnalytics","metaPixel","matomo","other"]},"providerLabel":{"type":"string","maxLength":100,"nullable":true,"description":"The name, when `provider` is `other`."},"measurementId":{"type":"string","maxLength":100,"description":"What the tag or SDK reports to (GA4 `G-...`, Tag Manager `GTM-...`, a pixel id)."},"surfaces":{"type":"array","minItems":1,"items":{"type":"string","enum":["guestWeb","guestApp"]}},"consentCategory":{"type":"string","enum":["functional","analytics","personalisation","marketing"],"default":"analytics","description":"The cookie category the visitor must grant before this provider loads (marketing-crm `CookieCategory`)."},"isEnabled":{"type":"boolean","default":true},"reportingPropertyId":{"type":"string","maxLength":100,"nullable":true,"description":"The property `getStorefrontInsights` asks the reporting API about (a GA4 property id). Staff only."},"reportingCredentialRef":{"type":"string","maxLength":200,"nullable":true,"writeOnly":true,"description":"The vault reference of the reporting credential. Accepted, never returned."},"hasReportingCredential":{"type":"boolean","readOnly":true,"description":"Whether a reporting credential is held, since the reference itself is never returned."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"TenantAppStatus": {"x-ticvai-persistence":"none — computed","type":"object","description":"Computed on read. The published fields come from the current `ConfigVersion`, the maintenance fields from the tenant's `tenant_config` row (`setMaintenanceMode`), and the draft fields from the working draft. **Fields marked staff only are left out of a response to a caller without a staff session** (`getTenantAppStatus`).\n","required":["tenantId","isPublished","isInMaintenance"],"properties":{"tenantId":{"type":"string","format":"uuid"},"isPublished":{"type":"boolean","x-ticvai-derived":"onRead","description":"True once any version has been published."},"publishedVersion":{"type":"string","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"draftVersion":{"type":"string","description":"Staff only."},"hasUnpublishedChanges":{"type":"boolean","x-ticvai-derived":"onRead","description":"Staff only. The working draft differs from the current version's `snapshot`."},"activeModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isEnabled` true."},"licensedModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isLicensed` true."},"activePageCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. Content pages that are `published` and enabled."},"isInMaintenance":{"type":"boolean"},"maintenanceMessage":{"$ref":"#/components/schemas/LocalisedText"},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"$ref":"#/components/schemas/MinimumAppVersion"},"contact":{"$ref":"#/components/schemas/VenueContact"},"availability":{"$ref":"#/components/schemas/AppAvailability"},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"What the sold-out or closed screen says (WEB-029). Null shows the default wording."},"venues":{"type":"array","maxItems":200,"x-ticvai-derived":"onRead","description":"**Public: the venues a guest can pick** (decided 28 September, audit R267; schema named 29 September, readiness close-out, our build plan). The source of the venue picker on WEB-001 and GST-001, returned with or without a session. **Published only**: a venue is listed when its scope node is active (`tenancy.OrgUnit.isActive`) and it is in the tenant's current published `ConfigVersion`; a venue added or reactivated since the last publish appears after the next publish, and a draft never reaches a guest. Ordered by `name`. Empty when nothing is published.\n","items":{"type":"object","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid","description":"**The venue's scope node** (`tenancy.OrgUnit.id`, level venue): what every guest screen that declares `venueId` `from: session` reads once the guest picks it."},"name":{"type":"string","maxLength":200,"description":"The venue's name (`tenancy.OrgUnit.name`)."},"city":{"type":"string","maxLength":120,"nullable":true,"description":"Shown under the name so two venues with similar names can be told apart."},"openingHoursToday":{"type":"object","nullable":true,"description":"Today's opening hours in the venue's time zone, from `tenancy.VenueSettings` opening hours. Null when the venue is closed today or has none set.","properties":{"opens":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"},"closes":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"}}}}}},"whatsNew":{"type":"array","maxItems":10,"x-ticvai-derived":"onRead","description":"**Public: the guest \"what's new\"** (decided 29 September, rev 3 GAP-B2). Newest first, at most 10, from `platform-ops.Release.guestReleaseNotes` of the releases the tenant's cell has received; a release with no guest notes is skipped. Returned with or without a staff session.\n","items":{"type":"object","required":["version","publishedAt","notes"],"properties":{"version":{"type":"string","description":"The release version."},"publishedAt":{"type":"string","format":"date-time","description":"When the release reached the tenant's cell."},"notes":{"$ref":"#/components/schemas/LocalisedText"}}}},"recentChanges":{"type":"array","description":"Staff only. Names the principal behind each change, so it never reaches a public response.","items":{"type":"object","properties":{"area":{"type":"string"},"description":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"}}}}}},
"Theme": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["primaryColour","secondaryColour","backgroundColour","textColour"],"properties":{"primaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"secondaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"accentColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"textColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"darkMode":{"type":"object","description":"Optional dark variant. Derived from the light theme when absent.","properties":{"primaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"textColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},"cornerRadius":{"type":"integer","minimum":0,"maximum":32,"description":"The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). Its named palettes, font pairs and background tones are presets over the colours here and `FontConfig`, not stored values."},"surfaceStyle":{"type":"string","enum":["glass","solid"],"default":"glass","description":"Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3)."},"buttonStyle":{"type":"string","enum":["solid","outline","pill"],"default":"solid","description":"Button shape (decided 29 September, rev 3 CFG-3)."},"componentColours":{"type":"object","description":"**Colours for single interactive elements (decided 17 September, M17-11).** Each is optional and falls back to the theme colours. Every pair passes the same contrast check as the theme (`ContrastProblem`), or `setTheme` refuses it with 400. The guest flow stays the standard one; only the colours change.\n","properties":{"primaryCta":{"$ref":"#/components/schemas/ThemeComponentColour"},"payButton":{"$ref":"#/components/schemas/ThemeComponentColour"},"addToCart":{"$ref":"#/components/schemas/ThemeComponentColour"},"buyTicketsButton":{"$ref":"#/components/schemas/ThemeComponentColour"},"link":{"$ref":"#/components/schemas/ThemeComponentColour"},"badge":{"$ref":"#/components/schemas/ThemeComponentColour"}}}}},
"VenueContact": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n","properties":{"phone":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true},"whatsapp":{"type":"string","nullable":true},"address":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Prose, as the guest reads it. The bookable hours are the catalogue's."}}},
"VenueMap": {"type":"object","x-ticvai-persistence":"venuemap.map","description":"A park map, or a floor plan. **Several per venue** — a guest on the second floor should not be shown the ground floor's toilets.\n","required":["id","name","venueId","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","readOnly":true,"description":"Derived from `venueId`. Not sent by a client."},"kind":{"type":"string","enum":["park","floor","zone","parking"]},"floorLevel":{"type":"integer","nullable":true},"status":{"type":"string","enum":["draft","published","archived"],"readOnly":true,"description":"`draft` on create. Moves through `publishVenueMap` (`states/venue-map.yaml`), never by sending a value.\n"},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `VenueMapVersion.version` guests are served. Null until the first publish.\n"},"graphVersion":{"type":"integer","readOnly":true,"description":"**Bumped by a publish or a closure**, and returned as `VenueMapGraph.version`. Separate from `publishedVersion` because a closure changes the routes without creating a map version, and a closure that looked like a publish would lie about what changed.\n"},"isGeoreferenced":{"type":"boolean","readOnly":true,"description":"**Whether a guest can be located on it.** Without a georeference the map is a picture — useful, and not navigable.\n"},"baseAssetId":{"type":"string","format":"uuid","nullable":true,"description":"**The illustrated map a guest actually sees**, held in `assets` like any other media.\n**This is not the CAD drawing.** The drawing gives geometry — where things are, and how they connect. The base image is a designed illustration with the venue's own styling, and the two are different artefacts that happen to describe the same place. A park hands you an architect's plan and a beautiful painted map, and **the guest wants the second while the platform needs the first.**\nNull is valid. A map with geometry and no illustration renders as shapes — plain, and navigable.\n","x-ticvai-references":"assets.MediaAsset"},"baseImageAlignment":{"type":"object","nullable":true,"description":"**How the illustration lines up with the geometry.** They are drawn at different scales by different people, and a point placed on the plan lands in the wrong place on the painting unless something reconciles them.\nTwo known points is enough. **Without this the illustration is a picture behind the map rather than the map itself.**\n","properties":{"imageWidthPx":{"type":"integer"},"imageHeightPx":{"type":"integer"},"anchors":{"type":"array","minItems":2,"maxItems":4,"items":{"type":"object","properties":{"planX":{"type":"number"},"planY":{"type":"number"},"imageX":{"type":"number"},"imageY":{"type":"number"}}}}}},"tileSetRef":{"type":"string","nullable":true,"readOnly":true,"description":"Where a base image is large enough to need zoom levels. **A 12,000-pixel park map is not something a phone downloads on arrival**, and a guest opening the map on venue wifi at the gate is the worst moment to send twenty megabytes.\nGenerated from the base asset. Null means the image is small enough to serve whole.\n"},"boundsGeoJson":{"type":"string","nullable":true},"graphStatus":{"type":"string","readOnly":true,"enum":["notBuilt","connected","disconnected","partial"],"description":"**Whether every public point can actually be reached.** Computed at publish.\n`disconnected` means a point has no path to it at all — a toilet nobody can walk to is a toilet that does not exist. `partial` means every point is reachable and at least one only by steps, which is a different and quieter failure: **the map works until a wheelchair user opens it.**\n"}}},
"VenueMapDetail": {"type":"object","description":"19.2.55. **The whole map in one call**, so a client caches it and filters locally.","properties":{"version":{"type":"integer","nullable":true,"readOnly":true,"description":"**The published version these points and paths belong to**, which is the number a client caches and sends back as `version`. It can differ from `map.publishedVersion` when an older version was asked for. Null when the draft was read.\n"},"map":{"$ref":"#/components/schemas/VenueMap"},"points":{"type":"array","items":{"$ref":"#/components/schemas/VenuePoint"}},"paths":{"type":"array","items":{"$ref":"#/components/schemas/VenuePath"}},"resources":{"type":"array","description":"The bookable resources placed on this version of the map (rev 3 REV3-15). Empty on a map that carries none.\n","items":{"$ref":"#/components/schemas/PlacedResource"}}}},
"VenuePath": {"type":"object","x-ticvai-persistence":"venuemap.path","description":"19.2.56. **The navigation graph.** The map supplies it; routing over it is a client concern, because a phone with the map cached routes offline and a server round-trip per step does not.\n","required":["id","mapId","fromPointId","toPointId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes the path."},"fromPointId":{"type":"string","format":"uuid"},"toPointId":{"type":"string","format":"uuid"},"geometry":{"type":"string","nullable":true,"description":"The centreline this edge follows, as an encoded polyline. **A walkway in a drawing is a polygon and a route is a line down the middle of it**, so extraction thins the polygon to a centreline and splits it at every fork.\nNull where the path was drawn on screen as a straight connection, which is normal for a venue with no walkway layer.\n"},"distanceMetres":{"type":"number","nullable":true,"readOnly":true,"description":"Computed by the server from `geometry` and the georeference. **Along the centreline, not point to point.** A path that curves round a lake is longer than the distance between its ends, and a guest told 80 metres who walks 200 stops trusting the map.\nRequires a georeference for real units; without one, distances are in drawing units and routing still works because **only the ratios matter to a shortest path.**\n"},"isStepFree":{"type":"boolean","default":true,"description":"**The single most important attribute on this object.** A wheelchair user routed up a staircase has been failed by the map, not by the venue.\n"},"isIndoor":{"type":"boolean","default":false},"restrictedByPointId":{"type":"string","format":"uuid","nullable":true,"description":"**Where a path is one-way, it is because of a thing on it — not because of the path.** Removed `isOneWay` on 18 August: a pedestrian walkway has no direction, and the three cases that look one-way are all a gate or a queue.\nA turnstile is one-way and `access.AccessPoint.direction` already says so. A queue line is one-way and `queue` owns it. **Putting the restriction on the path duplicated both and would have drifted from them** — a gate reconfigured to bidirectional would leave a path still marked one-way, and nothing would have noticed.\nSet where a path passes through an access point. The router reads the direction from the point.\n"},"closedReason":{"type":"string","nullable":true,"readOnly":true,"description":"Set by `setPathClosure` during works or an incident, never by sending it here. **A closed path removes routes rather than hiding the path**, so a guest sees why rather than wondering where it went.\n"}}},
"VenuePoint": {"type":"object","x-ticvai-persistence":"venuemap.point","description":"19.2.57 to 19.2.60. **What a venue places on the map**, and what a guest taps.\n","required":["id","mapId","kind","name","position"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes the point."},"kind":{"type":"string","enum":["ride","attraction","show","restaurant","cafe","shop","kiosk","toilet","babyCare","prayerRoom","firstAid","atm","lockers","entrance","exit","emergencyExit","assemblyPoint","parking","guestServices","smokingArea","waterFountain","chargingPoint","photoSpot","junction","other"],"description":"**A closed set, and `emergencyExit` is separate from `exit` on purpose.** An exit is where a guest leaves; an emergency exit is where they are sent, and a map that cannot tell them apart is a map that routes a normal departure through a fire door.\n**`junction` is the one that is not a point of interest.** A path connects two points, so a fork in a walkway with nothing at it still needs a node — otherwise every bend has to be named as a destination, and a guest browsing the map sees forty entries called *Path junction 12*.\n**Junctions are hidden from guests and present in the graph.** Generated by extraction where paths meet; a venue never places one by hand.\n"},"name":{"type":"string","x-ticvai-unique":"venue","description":"**Unique per venue** (decided 28 September, audit R108). Two points on a venue's maps never share a name, compared without case, so *Toilets North* names one place; `setVenuePoint` refuses a duplicate with `409` `duplicate-code`. Junctions are named by extraction and are exempt.\n"},"nameLocalised":{"type":"object","nullable":true,"additionalProperties":{"type":"string"}},"position":{"type":"object","required":["x","y"],"description":"Drawing coordinates. **Latitude and longitude are derived from the georeference**, not stored, so a map that is re-georeferenced does not need every point moved.\n","properties":{"x":{"type":"number"},"y":{"type":"number"}}},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"For a restaurant, cafe, shop or kiosk. **Tapping it should open the menu**, and that only works if the map knows which outlet it is.\n"},"productId":{"type":"string","format":"uuid","nullable":true,"description":"For a ride or show — links to wait times and to booking. **What a guest is offered from any point, including a restaurant or a shop, is `featuredOffer`** (29 September, MOB-4); this link stays for wait times.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"For an entrance or exit. **This is what makes 3.2.64 work** — live admission statistics drawn on the point they came from.\n"},"isStepFree":{"type":"boolean","default":true,"description":"Whether the point itself can be reached without steps. **The same name as `VenuePath.isStepFree`, because it is the same concept** (it was `isAccessible` until the 26 September audit). **Placed on the point rather than inferred from the path**, because a step-free route to a building with steps at the door is not a step-free route.\n"},"openingHours":{"type":"string","nullable":true},"iconRef":{"type":"string","nullable":true},"isActive":{"type":"boolean","default":true},"isNavigable":{"type":"boolean","default":true,"description":"Whether a route may pass through it. **False for a point that marks a place without being reachable** — a stage a guest cannot walk onto, a zone label.\n"},"isDestination":{"type":"boolean","default":true,"description":"**Whether a guest may be routed *to* it, and whether it appears in a list of places.** False for a `junction`, which exists in the graph and nowhere else.\nSeparate from `isNavigable` because the two differ: a junction is navigable and not a destination, and a fenced landmark is a destination you can be shown but not walked into.\n"},"description":{"type":"object","nullable":true,"additionalProperties":{"type":"string","maxLength":1000},"description":"**What the guest reads on Item Detail** (29 September, MOB-4). Keyed by locale, like `nameLocalised`. One screen now serves rides, shows, restaurants and shops (GST-004 and GST-006 merged), and it opens from the map pin, so the point carries the words rather than each kind borrowing them from a different module. Set on BO-094.\n"},"media":{"type":"array","maxItems":12,"description":"**The gallery on Item Detail** (29 September, MOB-4): images and short clips from the asset library, first `isPrimary` shown on the map card. Assets are referenced, never copied, so a replaced photo changes everywhere.\n","items":{"type":"object","required":["assetId","kind"],"properties":{"assetId":{"type":"string","format":"uuid","x-ticvai-references":"assets.media_asset"},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false},"altText":{"type":"string","nullable":true,"maxLength":200}}}},"featuredOffer":{"type":"object","nullable":true,"required":["kind","id"],"description":"**The product card on Item Detail, for every kind of point** (29 September, MOB-4). `productId` above links a ride or show to its wait times; this is what the guest is offered from the point, and it may be a bundle: a restaurant offers *meal combo with admission* (`promotions` bundle with an admission and a meal component), which checks out in about three steps (GST-004 → GST-056 → GST-041). A point with none shows no card. **Referenced, not priced here**: the card reads `catalogue.getProduct` or `promotions.getBundle` for the live price and availability.\n","properties":{"kind":{"type":"string","enum":["product","bundle"]},"id":{"type":"string","format":"uuid","description":"The `catalogue.product` id or the `promotions.bundle` id, by `kind`."},"label":{"type":"string","nullable":true,"maxLength":40,"description":"The button text, e.g. *Buy meal combo*. Null uses the product's own call to action."}}},"typicalDurationMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":600,"description":"**How long a visit to this point usually takes**, ride time and queue excluded (29 September, MOB-6). The visit planner lays out a day with it; the queue comes from `queue.getWaitTimes` on the day. Null for a point the planner never places (a toilet).\n"},"interestTags":{"type":"array","maxItems":12,"description":"**What a guest who says they like this would like here** (29 September, MOB-6): the planner matches the guest's interests against these. A closed list so that the Plan tab's interest chips and the venue's tags are the same words.\n","items":{"type":"string","enum":["thrill","family","kids","water","animals","shows","culture","shopping","dining","relaxing","photo","adventure","sport","nightlife","indoor"]}},"cuisineTags":{"type":"array","maxItems":8,"description":"**For dining points** (restaurant, cafe, kiosk; 29 September, MOB-6). The planner places meals at points whose cuisine the party chose, at meal times. Free text codes such as `arabic`, `indian`, `italian`, `fastFood`, `vegetarian`, `halal` — cuisines are too many to close, and a wrong enum is worse than an unmatched tag. **Read per venue**: the planner matches a guest's cuisine only against the points of the venue that day is at (30 September, MoM 4.7).\n","items":{"type":"string","maxLength":30}},"retailTags":{"type":"array","maxItems":8,"description":"**For retail points** (shop, and a kiosk that sells goods rather than food; 30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options). The planner places a shop stop at points whose tags the party chose, on the day of this point's venue only. Free text codes such as `souvenirs`, `toys`, `apparel`, `photo`, `essentials`, for the same reason as `cuisineTags`. A kiosk may carry both lists.\n","items":{"type":"string","maxLength":30}}}},
"WaitTime": {"x-ticvai-persistence":"none — computed from readings and throughput","type":"object","required":["queueId","waitMinutes","source","asOf","isStale"],"properties":{"queueId":{"type":"string","format":"uuid"},"queueName":{"$ref":"#/components/schemas/LocalisedText"},"attractionProductId":{"type":"string","format":"uuid","nullable":true},"attractionCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. Read from catalogue, not stored here.\n"},"status":{"$ref":"#/components/schemas/QueueStatus"},"waitMinutes":{"type":"integer","nullable":true,"description":"Null where the queue is closed or no estimate is available."},"source":{"$ref":"#/components/schemas/WaitTimeSource"},"isStale":{"type":"boolean","description":"The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as current, and it is not hidden (decided 28 September, audit R080 (b)): the screen shows `waitMinutes` with its `asOf` and a stale marker.\n"},"heightRequirementCm":{"type":"integer","nullable":true},"zone":{"type":"string","nullable":true},"asOf":{"type":"string","format":"date-time","description":"When the figure was produced — the queue's `waitTimeAsOf`."}}},
"WaitTimeSource": {"type":"string","description":"Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed.\n","enum":["sensor","throughput","manual","unavailable"]},
"WhiteLabelStorefrontSessionBatch": {"type":"object","x-ticvai-persistence":"none — request only; published as storefront.sessionEvent through platform.outbox","description":"One beacon from the storefront or guest-app runtime (8.3.40; decided 29 September, build pass, group G2). **Closed shape** (`additionalProperties: false`): hashes, route families, product ids and counts only.","additionalProperties":false,"required":["batchId","sessionRef","surface","sessionStartedAt","interactions"],"properties":{"batchId":{"type":"string","format":"uuid","description":"UUIDv7 minted by the runtime; a retried beacon repeats it."},"sessionRef":{"type":"string","maxLength":128,"description":"The runtime's own session id, SHA-256 hashed in the browser; hashed again with the tenant key on arrival and published as `storefront.sessionEvent.sessionRef`. The checkout passes the same value to `ai.scoreTransactionRisk`."},"deviceIdHash":{"type":"string","maxLength":128,"nullable":true},"surface":{"type":"string","enum":["guestWeb","guestApp"]},"venueId":{"type":"string","format":"uuid","nullable":true},"sessionStartedAt":{"type":"string","format":"date-time"},"interactions":{"type":"array","minItems":1,"maxItems":50,"items":{"type":"object","additionalProperties":false,"required":["kind","at"],"properties":{"kind":{"type":"string","enum":["pageView","productView","seatMapOpened","addToCart","removeFromCart","checkoutStarted","paymentPageViewed","promoCodeTried","search"]},"pageKind":{"type":"string","nullable":true,"enum":["home","product","seatMap","cart","checkout","account","content",null]},"productId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time"},"dwellMs":{"type":"integer","minimum":0,"nullable":true}}}},"automationHints":{"type":"object","nullable":true,"additionalProperties":false,"properties":{"webdriver":{"type":"boolean"},"headless":{"type":"boolean"},"pointerEvents":{"type":"integer","minimum":0},"interactionsPerMinute":{"type":"number","minimum":0}}}}}
}
```
