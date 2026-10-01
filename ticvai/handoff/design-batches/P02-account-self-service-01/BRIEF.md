# P02-account-self-service-01 — P02 · Account & Self-Service (1 of 2)

**10 screens · 45 operations · 47 schemas · 6 permissions**

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
  `GUEST_MANAGE, GUEST_VIEW, GUEST_VIEW_PII, LEDGER_POST, LEDGER_VIEW, ORDER_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **4 of these operations work offline**: getEntitlement, getGuestSession, getOrder, listMyEntitlements
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
| `GST-012` | My Tickets | A | 7 | 55 | 6 | 7 | 10 | 0 | guest | notStarted (client-verified) |
| `GST-013` | Ticket Details | A | 10 | 31 | 5 | 7 | 16 | 0 | guest | notStarted (client-verified) |
| `GST-018` | Add to Calendar / Reminders | A | 5 | 14 | 6 | 4 | 1 | 0 | guest | notStarted (client-verified) |
| `GST-019` | Order History | A | 0 | 16 | 6 | 5 | 0 | 0 | guest | notStarted (designed) |
| `GST-020` | Saved Items / Wishlist | A | 3 | 2 | 4 | 1 | 1 | 0 | guest | notStarted (client-verified) |
| `GST-039` | Profile | A | 19 | 17 | 5 | 14 | 1 | 0 | guest | notStarted (designed) |
| `GST-042` | Simple Registration & OTP | A | 36 | 6 | 6 | 13 | 8 | 0 | guest | notStarted (designed) |
| `GST-045` | Ticket Delivery & Sharing | A | 7 | 12 | 5 | 5 | 3 | 0 | guest | notStarted (client-verified) |
| `GST-055` | Dynamic QR Ticket | A | 13 | 38 | 5 | 7 | 10 | 0 | guest | notStarted (client-verified) |
| `GST-066` | Privacy & My Data | A | 12 | 2 | 6 | 16 | 2 | 4 | guest | notStarted (designed) |

## Thin screens in this batch

**GST-019, GST-020 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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

### In P02 · Account & Self-Service

- Decision: profiles are never merged automatically. Likely duplicates are notified to the customer (push or e-mail) and merge only on the customer's confirmation; an admin review queue tracks flagged duplicates independently of the customer's response. *(agreed · MoM 20 Aug 2026, 4.2 Duplicate Detection; 5. Key Decisions · DI-377)*

### Screen by screen

**`GST-012` My Tickets**

- Tickets tab: purchased tickets with a scan code (dynamic QR refreshing every 30 s), add to wallet or calendar, send/share, refund or resale. *(agreed · design review 29 Sep 2026, Mobile app (v4) — Tickets and scan · DI-1083)*
- Tickets tab shows the guest's purchased tickets and their scan code. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1022)*
- Entitlement statuses: active, reserved, consumed, transferred, expired, refunded/cancelled; views show entitlements nearing expiry, real-time consumption per customer, and whether a ticket has been upgraded. *(client request · MoM 7 Sep 2026, 4.10 / 4.11 Entitlements Lifecycle & Usage · DI-670)*
- Family/dependent view shows a family ticket's composition (e.g. two adults, two children) with each dependent's entitlements; equivalent views for school and corporate bookings. *(client request · MoM 7 Sep 2026, 4.9 Entitlements Portfolio - Structure, Family/Group & Assignment · DI-668)*
- Entitlements portfolio is used both by the guest (mobile app) and by customer service: one view of restrictions, wallet balance and all entitlements; a unified list across a visit (e.g. four admissions, two fast passes, a meal package, a parking entitlement). *(client request · MoM 7 Sep 2026, 4.9 Entitlements Portfolio - Structure, Family/Group & Assignment · DI-667)*
- Any online purchase for a dynamic-QR event must be linked to the mobile app to show the working code; web/desktop purchases are redirected into the app for activation, not exempted. *(agreed · MoM 2 Sep 2026, 4.7 Confirmed (Pradnya's question) · DI-635)*
- Upgrades must be available in the guest mobile/web app: guests view eligible upgrade options and complete the upgrade online without visiting on-site. *(agreed · MoM 1 Sep 2026, 4.9 / 5. Key Decisions · DI-606)*
- Decision: deferred seat assignment — sale confirmed at purchase as section + quantity; seats allocated internally; closer to the event ops/admin trigger a bulk e-mail issuing QR tickets with final seats. Immediate seat assignment remains for venues that need it. *(agreed · MoM 21 Aug 2026, 4.7 Deferred Seat Assignment Model; 5. Key Decisions · DI-423)*
- Group bookings: one shared QR for the whole group (redeemed together at the counter) or one QR per person, each of which the guest can link to their own profile in the mobile app. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-289)*
- Guest profile shows gift vouchers and a stored-value "money card"/wallet; "My Tickets" (all tickets) is separate from "My Reservations" (bookings holding one or more tickets) with reservation details and date modification. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-199)*

**`GST-013` Ticket Details**

- Tickets tab: purchased tickets with a scan code (dynamic QR refreshing every 30 s), add to wallet or calendar, send/share, refund or resale. *(agreed · design review 29 Sep 2026, Mobile app (v4) — Tickets and scan · DI-1083)*
- Ticket cards, Read more and the listing side panel show tags (e.g. "2 Hours", "Min 1.10 m", "Free adult entry", "Valid 90 days", "Emirates ID"), each with a kind icon (clock, height, free, calendar, id), max 6. Venue-set tags win, else derived from duration, validity, height rule. Setting "Tags on tickets", default on. *(agreed · design review 29 Sep 2026, Tickets 3. 'Read more' should carry tags customisable per ticket type · DI-1025)*
- Entitlement statuses: active, reserved, consumed, transferred, expired, refunded/cancelled; views show entitlements nearing expiry, real-time consumption per customer, and whether a ticket has been upgraded. *(client request · MoM 7 Sep 2026, 4.10 / 4.11 Entitlements Lifecycle & Usage · DI-670)*
- Family/dependent view shows a family ticket's composition (e.g. two adults, two children) with each dependent's entitlements; equivalent views for school and corporate bookings. *(client request · MoM 7 Sep 2026, 4.9 Entitlements Portfolio - Structure, Family/Group & Assignment · DI-668)*
- A ticket is always one virtual record; QR, RFID, NFC, face and future credentials (e.g. hotel room key, city transit card) are interchangeable media linked to it. Screens should show one ticket with its linked media, not separate tickets per medium. *(agreed · MoM 2 Sep 2026, 5. Key Decisions & Agreements · DI-652)*
- **Open question.** Open: NFC inside a wallet pass needs Apple certification (works with any reader) vs HID SDK on the guest phone (likely HID readers only). QR-based wallet passes are straightforward. Chinmay leans to direct Apple certification unless it is a hard blocker. *(open · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-610)*
- Apple/Google Wallet configuration covers template design (background colour, header, footer) and the guest-facing "Add to Apple Wallet" flow after an online purchase. *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-609)*
- Upgrades must be available in the guest mobile/web app: guests view eligible upgrade options and complete the upgrade online without visiting on-site. *(agreed · MoM 1 Sep 2026, 4.9 / 5. Key Decisions · DI-606)*
- Staff can upgrade multiple tickets in one action. "Quick upgrade" is a direct single-path upgrade (gold > platinum); "flexible upgrade" lets the guest choose among several eligible targets. *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-605)*
- Qossai: where a waiver is required before entry, an incomplete waiver can block ticket download, activation, check-in or access; ticket and scan screens need a waiver-incomplete state. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-574)*
- Decision (raised by Chinmay): date-change/reschedule is a product-level on/off setting with its own policy rules (e.g. allowed up to 24 hours before the visit, denied within 24 hours), not a separate screen. Typically off for special-day tickets (e.g. New Year, 1 January only), on for standard GA. *(agreed · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive; 5. Key Decisions · DI-446)*
- Decision: deferred seat assignment — sale confirmed at purchase as section + quantity; seats allocated internally; closer to the event ops/admin trigger a bulk e-mail issuing QR tickets with final seats. Immediate seat assignment remains for venues that need it. *(agreed · MoM 21 Aug 2026, 4.7 Deferred Seat Assignment Model; 5. Key Decisions · DI-423)*
- Ticket + combo meal: one QR holds both admission and meal; scanned at entry and again at the F&B counter to redeem the meal; a second meal redemption is refused. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-287)*
- Dynamic QR: the ticket QR is non-scannable until the guest is on site, then activates and refreshes continuously to prevent misuse (reconfirmed). *(agreed · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-219)*
- Ticket PDF carries a live QR code, a unique ticket number/barcode (media identifier), customisable branding/layout, terms and conditions and guest name; screens must distinguish ticket ID (one per ticket) from media code (can cover several tickets scanned as one group). *(agreed · MoM 7 Aug 2026, 20. Live Point-of-Sale Transaction Walkthrough · DI-180)*
- The ticket QR code regenerates every 15-30 seconds (configurable). *(agreed · MoM 31 Jul 2026, 7. Ticket Validation & Offline Architecture · DI-064)*

**`GST-018` Add to Calendar / Reminders**

- Add bookings to Apple/Google/Outlook calendar with reminders; wishlist of F&B and retail items to buy later on-site. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-202)*

**`GST-020` Saved Items / Wishlist**

- Add bookings to Apple/Google/Outlook calendar with reminders; wishlist of F&B and retail items to buy later on-site. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-202)*

**`GST-039` Profile**

- Guests can create family-member profiles themselves and set spending limits directly from their own guest account, in addition to venue-side configuration. *(agreed · MoM 27 Aug 2026, 4.8 Family, Parent-Child & Corporate Wallets · DI-530)*

**`GST-042` Simple Registration & OTP**

- Sign-in (or the guest code when guest checkout is on) is asked when the guest leaves the Add-ons step; the basket is kept. Setting "Ask to sign in": After add-ons (default) or At payment. *(agreed · rev 3 design review 29 Sep 2026, REV3-3 · 3. The sign-in screen should appear after Add-ons · DI-1043)*
- After the code, a match prompt shows what matched (e.g. 4 past orders, first order 12 Mar 2024, profile type), never the other profile's name or details, with "Use this profile" / "Not me – keep separate". Expired state: "This match has expired – continue as a new guest." *(agreed · design review 29 Sep 2026, 1. Guest checkout, code proof, profile matching (WEB-012) · DI-1035)*
- Guest checkout is a venue toggle, off by default: off = sign-in screen at payment ("This venue requires an account for checkout. Your basket is kept."), guest button hidden. On = "Continue as guest" with email or mobile (per "Match returning guests by") and a code; only exactly six digits accepted, copy says six. *(agreed · design review 29 Sep 2026, 1. Guest checkout, code proof, profile matching (WEB-012) · DI-1034)*
- The guest-checkout email pop-up collects only the fields configured in the back end (email, phone and/or name). After the code is verified, do not ask for name/email/phone again: go straight to T&Cs and complete the booking; profile is created and can be completed later (Platinumlist pattern). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W1 Guest checkout · DI-1002)*
- Decision: at least one of e-mail or mobile number is mandatory at profile creation (not both — some customers decline e-mail); the system supports conditional "either/or" mandatory-field rules. *(agreed · MoM 20 Aug 2026, 4.1 CRM; 5. Key Decisions · DI-372)*
- Sign-up by phone number or email, verified by OTP (WhatsApp or SMS/email as configured), then minimal profile (first/last name). *(client request · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-209)*
- UAE Pass login: customer enters mobile number, approves a push notification, confirms with biometrics; verified personal details are pulled into the booking automatically and a linked account is created. *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-123)*
- Checkout supports guest checkout, registered-account checkout, and single sign-on (e.g. Okta, Azure AD, a ticketing-specific SSO). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-121)*

**`GST-045` Ticket Delivery & Sharing**

- Duplicate screens become one implementation covering several screen IDs (mobile Transfer + Delivery & Sharing; web Wishlist / Devices & Consent; Help Centre + Help & Accessibility as one Help view with FAQ, cases, policies, accessibility tabs). Ticket-selection functions belong on GST-008. Web gets a Group Booking view. *(agreed · design review 29 Sep 2026, GAP-D3 · D. Duplicate screens merged; group booking on web · DI-1078)*
- Supporting configuration: ticket variants (adult/child/senior/VIP, configurable), waitlist, on-sale/off-sale timing and cut-offs, entitlement/access rules (single/multi-venue, entries, zones, early entry), fulfilment channels (email, WhatsApp, SMS), after-sales windows (upgrade, reschedule, cancel), dynamic/fixed pricing and promotions. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-437)*
- Ticket delivery: "Add to Wallet" (Apple or Google Wallet by device), and WhatsApp, SMS or email per the guest's chosen method, selectable at checkout/confirmation; tickets can also be emailed to a third party. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-198)*

**`GST-055` Dynamic QR Ticket**

- Tickets tab: purchased tickets with a scan code (dynamic QR refreshing every 30 s), add to wallet or calendar, send/share, refund or resale. *(agreed · design review 29 Sep 2026, Mobile app (v4) — Tickets and scan · DI-1083)*
- Tickets tab shows the guest's purchased tickets and their scan code. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1022)*
- Once activated in the app a digital ticket is bound to one approved device; moving to a new device requires deactivating the prior binding. Credential transfer moves a ticket to another person's device and invalidates the original holder's copy. *(client request · MoM 2 Sep 2026, 4.8 Device Binding, Credential Transfer & Revocation · DI-636)*
- Any online purchase for a dynamic-QR event must be linked to the mobile app to show the working code; web/desktop purchases are redirected into the app for activation, not exempted. *(agreed · MoM 2 Sep 2026, 4.7 Confirmed (Pradnya's question) · DI-635)*
- The dynamic QR stays blurred until beacon proximity is detected, then activates and refreshes on a short interval (e.g. every 6-12 seconds); screenshot capture of the active code is prevented. *(client request · MoM 2 Sep 2026, 4.6 Credential activation and display rules · DI-632)*
- Qossai: the dynamic QR must appear and work without internet, since crowded events (10,000+) suffer severe congestion; it must work offline via Bluetooth/beacon or an equivalent local mechanism. *(agreed · MoM 2 Sep 2026, 4.6 Hard requirement (offline) · DI-631)*
- **Open question.** Dynamic QR refreshes periodically to cut fraud/resale. Open: beacon-based (code hidden until the phone is near a gate beacon via Bluetooth, then refreshes ~every 2 minutes; Qossai: more secure) vs app-generated; GPS geofencing also raised. Chinmay to propose. *(open · MoM 2 Sep 2026, 4.6 Dynamic QR Code - Concept & Generation Approach · DI-630)*
- Ticket + combo meal: one QR holds both admission and meal; scanned at entry and again at the F&B counter to redeem the meal; a second meal redemption is refused. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-287)*
- Dynamic QR: the ticket QR is non-scannable until the guest is on site, then activates and refreshes continuously to prevent misuse (reconfirmed). *(agreed · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-219)*
- The ticket QR code regenerates every 15-30 seconds (configurable). *(agreed · MoM 31 Jul 2026, 7. Ticket Validation & Offline Architecture · DI-064)*

**`GST-066` Privacy & My Data**

- Qossai: use an existing major venue-group client's live app and published privacy policy as the model for how facial-recognition consent, data use and retention are explained to guests. *(client request · MoM 2 Sep 2026, 4.11 Privacy & Biometric Data Retention · DI-642)*
- Data-subject requests (access, correction, deletion) are tracked with status submitted → in progress → completed. *(client request · MoM 20 Aug 2026, 4.3 Consent, Data Privacy & Retention · DI-379)*
