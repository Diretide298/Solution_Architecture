# CMS flow builder: brief

> **What:** the white-label CMS drawn as one flow. The operator picks booking flows, orders their steps, sets the look, and publishes.
> **Screens:** CMS-102 Site Builder, CMS-103 Booking Flows, CMS-104 App Build & Store Publishing, CMS-101 Help Me Choose, plus the step screens they open.
> **Platform:** P13 Venue CMS, a section of TICVAI Venue Management. Desktop web, 1440 wide. Online only.
> **Decided:** MoM 29 September, W4 and W12 (the CMS is step-based, not the prototype's side panel), M24-05 and M24-08.
> **Block A:** yes. All four are in the first 35 days of the build.

Read this file first. Then `BUNDLE.md` in this folder: every field of the 17 screens, the 84 operations they call, and 88 schemas. This brief outranks the bundle where they differ.

## What the operator is doing

A venue's digital lead sets up the guest website and app in about 30 minutes. They start from a preset (theme park, water park, museum, theatre and arena, single attraction, play centre, several venues). The preset proposes everything. The only things they must supply are a logo, four colours and a Publish.

The Site Builder (CMS-102) is the spine. It shows seven steps, each marked not started, in progress, done or skipped. Each step opens a full screen and comes back. Progress saves on every return.

| step | what the operator does | screen |
|---|---|---|
| 1 Venue and modules | Turn modules and features on; set guest checkout | CMS-001 |
| 2 Ticketing flows | Pick the booking flows the venue sells through | CMS-103 |
| 3 Compose steps | Order each flow's steps, with a live preview | CMS-103 |
| 4 Help me choose (may skip) | Set the filter questions | CMS-101 |
| 5 Look and feel | Header and footer, logos, banners, theme, fonts | CMS-007, CMS-002, CMS-004, CMS-008, CMS-005, CMS-003, CMS-009 |
| 6 Mobile app (may skip) | Tabs, the Buy tickets button, intro video, home sections | CMS-009, CMS-004, CMS-007 |
| 7 Preview and publish | Preview in both directions, publish, roll back | CMS-006, CMS-012, CMS-014, CMS-015 |

After the first publish, **Build the mobile app** opens CMS-104.

## Draw it as one flow

Draw the four core screens in full and the step screens as the panels the flow opens. One file, one left rail, one top bar. The operator never feels they left the builder.

### 1. Pick the booking flows (CMS-103, step 2)

- A card grid of the **16 flow types** from `listBookingFlowTypes`. The catalogue is the same for every tenant. It is in `schemas.json` under `BookingFlowType` → `x-ticvai-system-catalogue`.
- Each card shows the type's name, the product kinds it serves, and its steps as a row of chips. Each chip is marked **Required** (locked), **Optional** (a switch) or **Conditional** (a switch, with the condition in words).
- The preset has already ticked the types it proposes. Picking a type calls `createBookingFlowDefinition`.

The 16 types and their default step order (r required, o optional, c conditional):

| type | steps | order rules beyond the common ones |
|---|---|---|
| Dated day pass | location c, help me choose c, date r, tickets r, consent c, extras o, review o, payment r | |
| Timed entry | location c, help me choose c, date r, time r, tickets r, consent c, extras o, review o, payment r | date before time |
| Open-dated | location c, help me choose c, tickets r, consent c, extras o, review o, payment r | |
| Seated, fixed performance | location c, performance r, seat map r, tickets c, consent c, extras o, review o, payment r | performance before seat map |
| Seated, date and time then seat map | location c, date r, time r, seat map r, tickets c, consent c, extras o, review o, payment r | date before time before seat map |
| Experience or workshop | location c, help me choose c, product r, date r, time r, tickets r, attendees c, consent c, extras o, review o, payment r | product before date (W8); date before time |
| Surf or session | location c, date r, time r, level r, tickets r, consent c, extras o, review o, payment r | time before level (W5) |
| Meeting room by the hour | location c, date r, time r, duration r, party size o, extras o, review o, payment r | date before time before duration (W9) |
| Cabana on a map | location c, date r, resource map r, consent c, extras o, review o, payment r | date before map (W6) |
| Cabana by size | location c, date r, party size r, resource size r, consent c, extras o, review o, payment r | date and party size before size |
| Guided tour by language | location c, date r, language r, time r, tickets r, extras o, review o, payment r | language before time (W11) |
| Transport | route r, date r, time r, tickets r, extras o, review o, payment r | route and date before time |
| Table reservation | location c, date r, party size r, time r, extras o, review o, payment c | date and party size before time |
| Membership | membership plan r, attendees r, consent c, review o, payment r | plan before attendees |
| Gift card | gift card value r, recipient r, review o, payment r | |
| Several locations | location r, help me choose c, product r, date c, time c, tickets r, consent c, extras o, review o, payment r | location before product |

Common rules for every type: payment is last; location is first; help me choose comes before tickets and product; tickets come before extras and consent; review comes before payment.

Common conditions, in the words to show: location shows when the tenant has more than one active venue. Help me choose shows when the venue has a published set-up. Consent shows when the flow or a product in the cart asks a consent question, and cannot be turned off while one does. Attendees shows when a product asks attendee details.

### 2. Compose the step order (CMS-103, step 3)

- Left: the venue's flows (`listBookingFlows`). An invalid flow is marked; it blocks the site's publish.
- Middle: **the step list** of the selected flow (`getBookingFlow`), in the venue's order. Drag to reorder. **A drop that breaks a rule is refused before it lands** (`validateBookingFlow` with the proposed steps), and the rule is named in plain words: "Payment is always last." "The seat map comes after date and time."
- Each step opens its settings: its own (for example the tour languages) and, read-only with a link to Site Settings (CMS-016), the venue-wide ones it uses.
- The flow's own settings: date, time then tickets or all at once; sign in after add-ons or at payment; a seated event's date inline or over the seat map; the extras step auto, always or never; the quick tour; the flow's consent questions.
- Assign the flow to products and categories.
- Right: **a live preview of the guest booking**, a phone frame running the steps in the order on screen. It changes as the operator drags. It calls nothing and publishes nothing. Save calls `updateBookingFlowDefinition`.

### 3. Help me choose (CMS-101, step 4)

- The venue's set-ups (`listGuidedChoices`), filtered by source (written by staff, or suggested by the assistant) and status (draft, published). **Suggestions awaiting review** is the default view while any exist, and an AI suggestion is labelled as one.
- The editor: mode (a button on the booking page, a pop-up on first arrival as well, or off); the banner under the products; filter (default) or recommend; **up to four questions**, each a choice, yes or no, age, level or certification. Two to four answers each: title, one line, icon, badge.
- **The filter builder**: for each answer, what it keeps. Products, categories, segment tags, an age range, swimmers only or never, a certificate held or not, or a booking flow. "Show everything" is on by default.
- **Preview the filtered list**: for each combination of answers, the products left. An answer that leaves nothing bookable shows as a warning before publish.
- A suggestion is never published by itself. A person reviews it, edits or dismisses it, previews it and publishes it (`publishGuidedChoice`). Publishing one set-up returns the old one to draft.

### 4. The configuration panels (steps 5 and 6)

Each opens from the builder and comes back. Draw them as panels of the builder with a live preview on the right.

| what | where | written by |
|---|---|---|
| Header | CMS-007 | `setHeader` |
| Footer columns, legal links, social | CMS-007 | `setFooter` |
| Home sections and their order | CMS-007 | `setHomepageLayout` |
| Brand kit: logo, favicon, splash | CMS-002, CMS-004 | `setBrandIdentity` |
| App icons | CMS-004 | `setAppIcons` |
| Intro video (off, first launch, every launch) with Skip | CMS-004 | `setBrandIdentity` (`introVideoMode`, `introVideoAssetRef`) |
| Banners | CMS-008 | `createBanner`, `updateBanner` |
| Theme colours, incl. the Buy tickets button colour | CMS-005 | `setTheme` |
| Fonts | CMS-003 | `setFonts` |
| Menus and web navigation | CMS-009 | `setNavigation` |
| Mobile tabs (Home, Explore, Plan, Tickets by default) and the Buy tickets button style | CMS-009 | `setNavigation` (`bottomNavigation`, `buyButton`) |

### 5. Preview and publish (step 7)

- Preview link (`createPreview`), right-to-left preview (CMS-012), validate (`validateTenantConfig`).
- **Publish** (`publishTenantConfig`, needs the publish permission). Before it, a gate says what changes for guests, and names any invalid flow that blocks it.
- Version history and roll back (`listConfigVersions`, `diffConfigVersion`, `restoreConfigVersion`).

### 6. App build and store publishing (CMS-104)

- **Before the first build**: a checklist. Apple D-U-N-S number, Apple Developer account, Google Play account (**the client opens these; TICVAI cannot**), store listing, app icons, a published configuration. Each open item says what to do next (`getStoreAccounts`, `setStoreAccounts`).
- Builds by platform (`listAppBuilds`): version, build number, configuration version, status. Request a build (`requestAppBuild`, publish permission), download the signed package, or submit to the store with the client's own credential. Store review status follows: submitted, in review, approved, rejected, released.
- An app publishing guide (the assistant). Unavailable until its profile exists; the checklist works without it.

## The operations the four core screens call

| operation | method and path | permission | what it does |
|---|---|---|---|
| `getSiteSetupProgress` | GET `/tenant-config/site-setup` | configure | Where the tenant is in the Site Builder |
| `setSiteSetupProgress` | PUT `/tenant-config/site-setup` | configure | Save the builder's progress and preset |
| `listBookingFlowTypes` | GET `/booking-flow-types` | configure | The 16 flow types, with their steps |
| `listBookingFlows` | GET `/venues/{venueId}/booking-flows` | configure | The venue's flows, in the working draft |
| `createBookingFlowDefinition` | POST `/venues/{venueId}/booking-flows` | configure | Pick a flow type for a venue |
| `getBookingFlow` | GET `/booking-flows/{bookingFlowId}` | configure | One flow, every step included |
| `updateBookingFlowDefinition` | PATCH `/booking-flows/{bookingFlowId}` | configure | Reorder steps, switch optional ones, change settings |
| `validateBookingFlow` | POST `/booking-flows/{bookingFlowId}/validate` | configure | Check a flow (or a proposed order) against its type |
| `deleteBookingFlow` | DELETE `/booking-flows/{bookingFlowId}` | configure | Remove a flow |
| `getPublishedBookingFlow` | GET `/venues/{venueId}/booking-flow` | none | The published flow a product books through |
| `listGuidedChoices` | GET `/venues/{venueId}/guided-choices` | configure | The venue's Help me choose set-ups |
| `createGuidedChoice` | POST `/venues/{venueId}/guided-choices` | configure | Set one up |
| `updateGuidedChoice` | PATCH `/guided-choices/{guidedChoiceId}` | configure | Edit, or review a suggestion |
| `deleteGuidedChoice` | DELETE `/guided-choices/{guidedChoiceId}` | configure | Delete, or dismiss a suggestion |
| `publishGuidedChoice` | POST `/guided-choices/{guidedChoiceId}/publish` | publish | Publish to guests |
| `unpublishGuidedChoice` | POST `/guided-choices/{guidedChoiceId}/unpublish` | publish | Take it off |
| `suggestGuidedChoice` (ai) | POST `/venues/{venueId}/guided-choice-suggestions` | AI use | Ask the assistant for a set-up |
| `getStoreAccounts` | GET `/tenant-config/store-accounts` | configure | Store accounts and the checklist |
| `setStoreAccounts` | PUT `/tenant-config/store-accounts` | configure | Record the client's own accounts and listing |
| `listAppBuilds` | GET `/tenant-config/app-builds` | configure | Builds, newest first |
| `requestAppBuild` | POST `/tenant-config/app-builds` | publish | Build the branded app for a store |
| `getAppBuild` | GET `/tenant-config/app-builds/{appBuildId}` | configure | One build, with its package and store status |
| `validateTenantConfig` | POST `/tenant-config/validate` | configure | Validate the working draft |
| `publishTenantConfig` | POST `/tenant-config/publish` | publish | Publish the working draft |

"configure" is the tenant configure permission; "publish" is the tenant publish permission. Gate every publish control on the second. The schemas are in `schemas.json`: `BookingFlowType`, `BookingFlow`, `BookingFlowStep`, `BookingFlowLevelSettings`, `SiteSetupProgress`, `GuidedChoice`, `StorePublishingChecklist`, `AppBuild`, `BrandIdentity`, `Theme`, `NavigationConfig` and the rest.

## The look

- **Controls:** `sources/designs/guest-rev3-29-september/TICVAI Engine Controls Manual.dc.html`. It lays out every control: venue type, booking flow, brand, flow, shape and background, layout and locale. Match how it groups, labels and explains a control.
- **The configuration side panel in** `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the control styles (dropdowns, segmented switches, colour pickers, step order list). **The panel is a reference tool, not the CMS** (W12). Take its controls, not its layout.
- **The live preview** is the guest booking in that same file. Show it in a phone frame on the right.
- **Operator density:** `sources/designs/TICVAI_POS_Terminal_client_approved.html`.
- **The client's builder boards:** `sources/designs/TICVAI_White_Label_Guest_App_UI_Reference_1.pdf`.

## Seed data

A fictional UAE tenant, for example "Coastal Aqua" (water park, Abu Dhabi) and a second venue so the location step shows. Prices in AED. Products: day pass, cabana, surf session (beginner, intermediate), meal combo. No real client names or logos: do not use `logos/` from the prototype folder.

## Deliverable

1. **Into the Venue Management app file**, `handoff/design-batches/apps/5-venue-management/return/TICVAI Venue Management.dc.html` (one working file for the whole app, decided 30 September; create it if this is the first batch). Each screen opens from `#cms-102`, `#cms-103`, `#cms-101`, `#cms-104` and so on, already populated; each declared state from `#<id>?state=<state>`. The element holding a screen carries `data-screen-label="<SCREEN ID> <Screen name>"`. No external requests except Google Fonts.
2. One fragment per screen in `wireframes/incoming/CMS-FLOW-BUILDER/<screen id>.html` (no `<html>`, `<head>`, `<body>` or `<script>`; root `id` is the screen id in lower case). These import with `tools/import-design-frames.py` against the batches `P13-white-label-01`, `-02` and `-03`.
3. `return/FINDINGS.md`: anything the bundle lacks. Draw it greyed with a short note. Never invent an endpoint.

Nothing from the bundle (operation ids, field names, permission keys, screen ids) appears as text a user reads, except the `data-screen-label` attribute.
