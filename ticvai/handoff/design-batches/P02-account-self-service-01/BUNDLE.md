# P02-account-self-service-01 — P02 · Account & Self-Service (1 of 2)

**10 screens · 46 operations · 48 schemas · 6 permissions**

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
| `screens.json` | Every field of every screen in the batch. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW, GUEST_VIEW_PII, LEDGER_POST, LEDGER_VIEW, ORDER_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **5 of these operations work offline**: getEntitlement, getGuestSession, getOrder, listMyEntitlements, listOrders
  — and the rest do not. A surface that looks the same online and off is lying.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `GST-012` | My Tickets | listDetail | 6 | 1 | — |
| `GST-013` | Ticket Details | statusTracker | 5 | 2 | — |
| `GST-018` | Add to Calendar / Reminders | listDetail | 6 | 2 | — |
| `GST-019` | Order History | listDetail | 9 | 1 | — |
| `GST-020` | Saved Items / Wishlist | statusTracker | 3 | 2 | — |
| `GST-039` | Profile | configEditor | 2 | 1 | — |
| `GST-042` | Simple Registration & OTP | form | 13 | 8 | — |
| `GST-045` | Ticket Delivery & Sharing | configEditor | 1 | 0 | — |
| `GST-055` | Dynamic QR Ticket | configEditor | 5 | 1 | — |
| `GST-066` | Privacy & My Data | statusTracker | 9 | 3 | — |

## Thin screens in this batch

**GST-020 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "GST-012",
  "name": "My Tickets",
  "module": "Account & Self-Service",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C02",
  "implementation": {
   "app": "guest-app",
   "route": "/general/my-tickets",
   "component": "apps/guest-app/src/routes/general/MyTicketsList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-028"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-013"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-012 holds none of them. The edge carries nothing: GST-012 is opened from GST-001, so this edge is the way back and GST-001 keeps its own state"
    },
    {
     "to": "GST-013",
     "trigger": "They open the one for now",
     "provenance": "flow F50 step 4→5",
     "carries": [
      "entitlementId",
      "orderId"
     ]
    }
   ],
   "uses": [
    "appTabs"
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. My Tickets. **Declared only `transferOrderTickets` until 20 August** — a guest could give a ticket away and could not read one. Raised by Pranay. **Rewired on the 20 August review.** **Cross-surface parity, 31 August**: added getEntitlementCredential, getEntitlementHistory, listEntitlements. **The same screen on web and app was calling different operations** — one side could do something the other could not, and nothing recorded the difference as deliberate.\n\n**Mobile v4 (decided 29 September, MOB-1, MOB-7).** The **Tickets** tab root. GST-013 Ticket Details and GST-055 Dynamic QR Ticket (refresh every 30 s) are unchanged.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listMyEntitlements` reads the population and `getEntitlement` reads one of them — list, select, act",
  "purpose": "Find my tickets for this venue.",
  "gaps": [
   {
    "operation": "getEntitlementCredential",
    "why": "**`getEntitlementCredential` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.",
    "source": "contract access.yaml GET /entitlements/{entitlementId}/credential"
   },
   {
    "operation": "getEntitlementHistory",
    "why": "**`getEntitlementHistory` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.",
    "source": "contract access.yaml GET /entitlements/{entitlementId}/history"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "selectField",
       "label": "State",
       "operation": "listMyEntitlements",
       "notes": "Sends `?state=` to `listMyEntitlements`.",
       "provenance": "contract access.yaml GET /guests/me/entitlements"
      },
      {
       "kind": "toggle",
       "label": "Include shared",
       "operation": "listMyEntitlements",
       "notes": "Sends `?includeShared=` to `listMyEntitlements`.",
       "provenance": "contract access.yaml GET /guests/me/entitlements"
      },
      {
       "kind": "dataTable",
       "label": "Every entitlement",
       "bindsTo": "Entitlement",
       "columns": [
        "Entitlement.id",
        "Entitlement.templateId",
        "Entitlement.productId",
        "Entitlement.orderId",
        "Entitlement.orderLineId",
        "Entitlement.subjectId",
        "Entitlement.venueId",
        "Entitlement.scopePath",
        "Entitlement.mediaCode",
        "Entitlement.status",
        "Entitlement.statusNote",
        "Entitlement.validFrom"
       ],
       "operation": "listMyEntitlements",
       "provenance": "contract access.yaml GET /guests/me/entitlements"
      },
      {
       "kind": "dataTable",
       "label": "Entitlement history",
       "operation": "getEntitlementHistory",
       "notes": "Shows `at`, `kind`, `accessPointName`, `denyReason`, `byPrincipalName` from `getEntitlementHistory`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.",
       "provenance": "contract access.yaml GET /entitlements/{entitlementId}/history"
      },
      {
       "kind": "dataTable",
       "label": "Every entitlement",
       "bindsTo": "Entitlement",
       "columns": [
        "Entitlement.id",
        "Entitlement.templateId",
        "Entitlement.productId",
        "Entitlement.orderId",
        "Entitlement.orderLineId",
        "Entitlement.subjectId",
        "Entitlement.venueId",
        "Entitlement.scopePath",
        "Entitlement.mediaCode",
        "Entitlement.status",
        "Entitlement.statusNote",
        "Entitlement.validFrom"
       ],
       "operation": "listEntitlements",
       "provenance": "contract access.yaml GET /my/entitlements/all"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected entitlement",
       "bindsTo": "Entitlement",
       "columns": [
        "Entitlement.id",
        "Entitlement.templateId",
        "Entitlement.productId",
        "Entitlement.orderId",
        "Entitlement.orderLineId",
        "Entitlement.subjectId",
        "Entitlement.venueId",
        "Entitlement.scopePath",
        "Entitlement.mediaCode",
        "Entitlement.status",
        "Entitlement.statusNote",
        "Entitlement.validFrom",
        "Entitlement.validTo",
        "Entitlement.entriesUsed",
        "Entitlement.entriesAllowed",
        "Entitlement.lastEntryAt"
       ],
       "operation": "getEntitlement",
       "provenance": "contract access.yaml GET /entitlements/{entitlementId}"
      },
      {
       "kind": "detailPanel",
       "label": "Entitlement credential",
       "operation": "getEntitlementCredential",
       "notes": "Shows `mediaCode`, `payload`, `expiresAt` from `getEntitlementCredential`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.",
       "provenance": "contract access.yaml GET /entitlements/{entitlementId}/credential"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Transfer order tickets",
       "operation": "transferOrderTickets",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The tickets list.",
   "error": "Could not load. Names which read failed and leaves the tickets untouched.",
   "emptyFirstRun": "No tickets yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on state, includeShared and the tickets are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `listMyEntitlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Tickets already loaded stay visible with their age, and a ticket's rotating code is derived on the device from its seed, so it changes with no signal (decided 28 September, audit R230). Sharing, transferring and adding to a phone wallet need the connection."
  },
  "apis": [
   {
    "operationId": "listMyEntitlements",
    "contract": "access",
    "purpose": "Every ticket, pass and membership this guest holds",
    "trigger": "onLoad"
   },
   {
    "operationId": "getEntitlement",
    "contract": "access",
    "purpose": "One entitlement, with what remains on it",
    "trigger": "onLoad"
   },
   {
    "operationId": "transferOrderTickets",
    "contract": "orders",
    "purpose": "Transfer tickets to another guest",
    "trigger": "onAction",
    "invalidates": [
     "listMyEntitlements"
    ]
   },
   {
    "operationId": "getEntitlementCredential",
    "contract": "access",
    "purpose": "The thing that gets scanned",
    "trigger": "onLoad"
   },
   {
    "operationId": "getEntitlementHistory",
    "contract": "access",
    "purpose": "Every scan, freeze, share and reissue against it",
    "trigger": "onLoad"
   },
   {
    "operationId": "listEntitlements",
    "contract": "access",
    "purpose": "Every entitlement this guest holds, including expired",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "entitlementId",
     "from": "deepLink"
    },
    {
     "name": "orderId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A ticket link opened after the event.** Shows the entitlement with its status — expired, used, transferred — because *not found* to somebody holding a ticket is the wrong answer. **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error.",
   "preloaded": [
    "Entitlement.id",
    "Entitlement.templateId",
    "Entitlement.productId",
    "Entitlement.orderId",
    "Entitlement.orderLineId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-012",
   "prototype": {
    "file": "sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html",
    "rev": "mobile v4 (30 September build)",
    "verified": "2026-10-01",
    "match": "exact",
    "view": "Tickets tab"
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formTransferOrderTickets",
    "component": "modal",
    "trigger": "Transfer order tickets",
    "body": "**Collects what `transferOrderTickets` sends before it is called.** Required: `ticketIds`, `recipient`. Optional: `message`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transfer order tickets",
     "operation": "transferOrderTickets"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "ticketIds",
      "recipient",
      "message"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-013",
  "name": "Ticket Details",
  "module": "Account & Self-Service",
  "requiresModule": "access",
  "wave": 1,
  "capability": "C02",
  "implementation": {
   "app": "guest-app",
   "route": "/general/ticket-details",
   "component": "apps/guest-app/src/routes/general/TicketDetailsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-012"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-055"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-013 holds none of them. The edge carries nothing: GST-013 is opened from GST-001, so this edge is the way back and GST-001 keeps its own state"
    },
    {
     "to": "GST-055",
     "trigger": "The QR rotates as they walk to the gate",
     "provenance": "flow F50 step 5→6",
     "carries": [
      "credentialId",
      "entitlementId",
      "orderId"
     ]
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Ticket Details. **The credential is a separate call** — a list of tickets is a convenience and the credential admits somebody. **Rewired on the 20 August review.**\n\n**Rev 3 (decided 29 September).** Ticket tags from `Product.displayTags` when `ticketTags` is on (23SEP-3).",
  "density": "comfortable",
  "pattern": "statusTracker",
  "patternReason": "`getEntitlement` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Find ticket details for this venue.",
  "gaps": [
   {
    "operation": "getEntitlementCredential",
    "why": "**`getEntitlementCredential` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.",
    "source": "contract access.yaml GET /entitlements/{entitlementId}/credential"
   },
   {
    "operation": "getEntitlementHistory",
    "why": "**`getEntitlementHistory` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.",
    "source": "contract access.yaml GET /entitlements/{entitlementId}/history"
   }
  ],
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The entitlement",
       "bindsTo": "Entitlement",
       "columns": [
        "Entitlement.id",
        "Entitlement.templateId",
        "Entitlement.productId",
        "Entitlement.orderId",
        "Entitlement.orderLineId",
        "Entitlement.subjectId",
        "Entitlement.venueId",
        "Entitlement.scopePath",
        "Entitlement.mediaCode",
        "Entitlement.status",
        "Entitlement.statusNote",
        "Entitlement.validFrom",
        "Entitlement.validTo",
        "Entitlement.entriesUsed",
        "Entitlement.entriesAllowed",
        "Entitlement.lastEntryAt"
       ],
       "operation": "getEntitlement",
       "provenance": "contract access.yaml GET /entitlements/{entitlementId}"
      },
      {
       "kind": "detailPanel",
       "label": "Entitlement credential",
       "operation": "getEntitlementCredential",
       "notes": "Shows `mediaCode`, `payload`, `expiresAt` from `getEntitlementCredential`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one. **A rotating code derived on the device** (decided 28 September, audit R230): while online the screen fetches `rotation` (secret, `timeStepSeconds`, `digits`, `algorithm`, valid `validFrom` to `validTo`) and computes the current code from the seed and the clock, with a visible countdown to the next step; it keeps rotating with no signal. A null `rotation` (wristband, wallet pass) shows the static code.",
       "provenance": "contract access.yaml GET /entitlements/{entitlementId}/credential"
      },
      {
       "kind": "dataTable",
       "label": "Entitlement history",
       "operation": "getEntitlementHistory",
       "notes": "Shows `at`, `kind`, `accessPointName`, `denyReason`, `byPrincipalName` from `getEntitlementHistory`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.",
       "provenance": "contract access.yaml GET /entitlements/{entitlementId}/history"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Transfer order tickets",
       "operation": "transferOrderTickets",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      },
      {
       "kind": "secondaryButton",
       "label": "Bind credential device",
       "operation": "bindCredentialDevice",
       "notes": "**The guest app binds a mobile credential to the phone it is shown on** (P02 GST-055 Dynamic QR Ticket), before the dynamic QR is displayed.",
       "provenance": "contract access.yaml POST /my/credentials/{credentialId}/device-bindings"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Availability is live, never cached",
   "error": "Availability unavailable. **Selection is blocked** — overselling is worse than waiting",
   "emptyFirstRun": "**Sold out is a real answer.** Offers the next available rather than a dead end",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `getEntitlement` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Tickets already loaded stay visible with their age, and a ticket's rotating code is derived on the device from its seed, so it changes with no signal (decided 28 September, audit R230). Sharing, transferring and adding to a phone wallet need the connection."
  },
  "apis": [
   {
    "operationId": "getEntitlement",
    "contract": "access",
    "purpose": "One entitlement, with what remains on it",
    "trigger": "onLoad"
   },
   {
    "operationId": "getEntitlementCredential",
    "contract": "access",
    "purpose": "The thing that gets scanned — with the `rotation` seed the device derives the rotating code from (audit R230)",
    "trigger": "onLoad"
   },
   {
    "operationId": "getEntitlementHistory",
    "contract": "access",
    "purpose": "Every scan, freeze, share and reissue against it",
    "trigger": "onLoad"
   },
   {
    "operationId": "transferOrderTickets",
    "contract": "orders",
    "purpose": "Transfer tickets to another guest",
    "trigger": "onAction"
   },
   {
    "operationId": "bindCredentialDevice",
    "contract": "access",
    "purpose": "Bind my credential to this device",
    "trigger": "onAction",
    "invalidates": [
     "getEntitlement",
     "getEntitlementCredential",
     "getEntitlementHistory"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "entitlementId",
     "from": "deepLink"
    },
    {
     "name": "orderId",
     "from": "deepLink"
    },
    {
     "name": "credentialId",
     "from": "navigation",
     "optional": true
    }
   ],
   "coldEntry": "**A ticket link opened after the event.** Shows the entitlement with its status — expired, used, transferred — because *not found* to somebody holding a ticket is the wrong answer. **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-013",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 1 → Ticket details",
    "differences": "The YAML states come from an availability template (\"Sold out is a real answer\") and do not fit a ticket-detail screen."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formTransferOrderTickets",
    "component": "modal",
    "trigger": "Transfer order tickets",
    "body": "**Collects what `transferOrderTickets` sends before it is called.** Required: `ticketIds`, `recipient`. Optional: `message`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transfer order tickets",
     "operation": "transferOrderTickets"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "ticketIds",
      "recipient",
      "message"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formBindCredentialDevice",
    "component": "modal",
    "trigger": "Bind credential device",
    "body": "**Collects what `bindCredentialDevice` sends before it is called.** Required: `deviceId`. Optional: `deviceReference`, `appInstallationId`, `os`, `otp`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CredentialDeviceBindingInput",
    "confirm": {
     "label": "Bind credential device",
     "operation": "bindCredentialDevice"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "deviceId",
      "deviceReference",
      "appInstallationId",
      "os",
      "otp"
     ]
    },
    "provenance": "contract access.yaml POST /my/credentials/{credentialId}/device-bindings"
   }
  ],
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-018",
  "name": "Add to Calendar / Reminders",
  "module": "Account & Self-Service",
  "requiresModule": "ticketing",
  "wave": 3,
  "capability": "C02",
  "implementation": {
   "app": "guest-app",
   "route": "/general/add-to-calendar-reminders",
   "component": "apps/guest-app/src/routes/general/AddToCalendarRemindersDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-018 holds none of them. The edge carries nothing: GST-018 is opened from GST-001, so this edge is the way back and GST-001 keeps its own state"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Add to Calendar and Reminders. **`issueWalletPass` is the operation this screen is for** — a wallet pass is the calendar entry. **Rewired on the 20 August review.**",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listOrders` reads the population and `getOrder` reads one of them — list, select, act",
  "purpose": "Find add to calendar / reminders for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Venue id",
       "operation": "listOrders",
       "notes": "Sends `?venueId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Principal id",
       "operation": "listOrders",
       "notes": "Sends `?principalId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Shift id",
       "operation": "listOrders",
       "notes": "Sends `?shiftId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listOrders",
       "notes": "Sends `?status=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "datePicker",
       "label": "Created from",
       "operation": "listOrders",
       "notes": "Sends `?createdFrom=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "datePicker",
       "label": "Created to",
       "operation": "listOrders",
       "notes": "Sends `?createdTo=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "dataTable",
       "label": "Every order",
       "bindsTo": "OrderSummary",
       "columns": [
        "OrderSummary.id",
        "OrderSummary.orderNumber",
        "OrderSummary.status",
        "OrderSummary.grossAmount",
        "OrderSummary.refundedAmount",
        "OrderSummary.channel",
        "OrderSummary.lineCount"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected order",
       "bindsTo": "OrderSummary",
       "columns": [
        "OrderSummary.id",
        "OrderSummary.orderNumber",
        "OrderSummary.status",
        "OrderSummary.grossAmount",
        "OrderSummary.refundedAmount",
        "OrderSummary.channel",
        "OrderSummary.lineCount",
        "OrderSummary.principalId",
        "OrderSummary.holdLabel",
        "OrderSummary.heldUntil"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "detailPanel",
       "label": "The visit reminder",
       "bindsTo": "VisitReminder",
       "columns": [
        "VisitReminder.id",
        "VisitReminder.orderId",
        "VisitReminder.subjectId",
        "VisitReminder.enabled",
        "VisitReminder.leadTimeMinutes",
        "VisitReminder.channels",
        "VisitReminder.scopePath"
       ],
       "operation": "getVisitReminder",
       "provenance": "contract orders.yaml GET /orders/{orderId}/reminder"
      },
      {
       "kind": "detailPanel",
       "label": "The order",
       "bindsTo": "Order",
       "columns": [
        "Order.id",
        "Order.orderNumber",
        "Order.channel",
        "Order.venueId",
        "Order.scopePath",
        "Order.status",
        "Order.currency",
        "Order.currencyScale",
        "Order.grossAmount",
        "Order.taxAmount",
        "Order.netAmount",
        "Order.refundedAmount",
        "Order.totalPriceVariance",
        "Order.lines",
        "Order.payments",
        "Order.principalId"
       ],
       "operation": "getOrder",
       "provenance": "contract orders.yaml GET /orders/{orderId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Issue wallet pass",
       "operation": "issueWalletPass",
       "provenance": "contract orders.yaml POST /wallet-passes"
      },
      {
       "kind": "secondaryButton",
       "label": "Download order calendar event",
       "operation": "getOrderCalendarEvent",
       "notes": "Downloads `text/calendar`.",
       "provenance": "contract orders.yaml GET /orders/{orderId}/calendar-event"
      },
      {
       "kind": "secondaryButton",
       "label": "Save visit reminder",
       "operation": "setVisitReminder",
       "provenance": "contract orders.yaml PUT /orders/{orderId}/reminder"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The add calendar reminders list.",
   "error": "Could not load. Names which read failed and leaves the add calendar reminders untouched.",
   "emptyFirstRun": "No add calendar reminders yet. Offers Issue wallet pass (`issueWalletPass`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on venueId, principalId, shiftId, status, createdFrom, createdTo and the add calendar reminders are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `getOrderCalendarEvent` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "getOrderCalendarEvent",
    "contract": "orders",
    "purpose": "Add the visit to the phone's calendar",
    "trigger": "onAction"
   },
   {
    "operationId": "getVisitReminder",
    "contract": "orders",
    "purpose": "The reminder set for this booking",
    "trigger": "onAction"
   },
   {
    "operationId": "setVisitReminder",
    "contract": "orders",
    "purpose": "Turn a visit reminder on or off",
    "trigger": "onAction"
   },
   {
    "operationId": "getOrder",
    "contract": "orders",
    "purpose": "Read an order",
    "trigger": "onAction"
   },
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "List orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "issueWalletPass",
    "contract": "orders",
    "purpose": "Generate an Apple or Google wallet pass",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error.",
   "preloaded": [
    "OrderSummary.id",
    "OrderSummary.orderNumber",
    "OrderSummary.status",
    "OrderSummary.grossAmount",
    "OrderSummary.refundedAmount"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-018",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 3 → Add to calendar / reminders"
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetVisitReminder",
    "component": "modal",
    "trigger": "Save visit reminder",
    "body": "**Collects what `setVisitReminder` sends before it is called.** Required: `enabled`. Optional: `id`, `orderId`, `subjectId`, `leadTimeMinutes`, `channels`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "VisitReminder",
    "confirm": {
     "label": "Save visit reminder",
     "operation": "setVisitReminder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "enabled",
      "id",
      "orderId",
      "subjectId",
      "leadTimeMinutes",
      "channels",
      "scopePath"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formIssueWalletPass",
    "component": "modal",
    "trigger": "Issue wallet pass",
    "body": "**Collects what `issueWalletPass` sends before it is called.** Required: `entitlementId`, `platform`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Issue wallet pass",
     "operation": "issueWalletPass"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "entitlementId",
      "platform"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-019",
  "name": "Order History",
  "module": "Account & Self-Service",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C21",
  "implementation": {
   "app": "guest-app",
   "route": "/general/order-history-wallet",
   "component": "apps/guest-app/src/routes/general/OrderHistoryWalletDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-067"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-019 holds none of them. The edge carries nothing: GST-019 is opened from GST-001, so this edge is the way back and GST-001 keeps its own state"
    },
    {
     "to": "GST-067",
     "trigger": "Ask for a refund or resell a ticket",
     "carries": [
      "orderId"
     ],
     "provenance": "decided 29 September, rev 3 GAP-D3: GST-008 no longer reaches refunds; order history does"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Order History. **`transferOrderTickets` was the only declared operation**, which is not history. Raised by Pranay. **Rewired on the 20 August review.** **`listMyOrders` wired 24 August, raised in review.** The staff-scoped list was on this guest screen — **a guest-facing list must be scoped to the caller, not filtered by a subject parameter**, or a guest is one parameter away from somebody else’s. **Renamed 31 August** from *Order History (Wallet)*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest. **Cross-surface parity, 31 August**: added transferOrderTickets. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listOrders` reads the population and `getOrder` reads one of them — list, select, act",
  "purpose": "Find order history (wallet) for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Venue id",
       "operation": "listOrders",
       "notes": "Sends `?venueId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Principal id",
       "operation": "listOrders",
       "notes": "Sends `?principalId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Shift id",
       "operation": "listOrders",
       "notes": "Sends `?shiftId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listOrders",
       "notes": "Sends `?status=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "datePicker",
       "label": "Created from",
       "operation": "listOrders",
       "notes": "Sends `?createdFrom=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "datePicker",
       "label": "Created to",
       "operation": "listOrders",
       "notes": "Sends `?createdTo=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "dataTable",
       "label": "Every order",
       "bindsTo": "OrderSummary",
       "columns": [
        "OrderSummary.id",
        "OrderSummary.orderNumber",
        "OrderSummary.status",
        "OrderSummary.grossAmount",
        "OrderSummary.refundedAmount",
        "OrderSummary.channel",
        "OrderSummary.lineCount"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "dataTable",
       "label": "Every order",
       "bindsTo": "Order",
       "columns": [
        "Order.id",
        "Order.orderNumber",
        "Order.channel",
        "Order.venueId",
        "Order.scopePath",
        "Order.status",
        "Order.currency",
        "Order.currencyScale",
        "Order.grossAmount",
        "Order.taxAmount",
        "Order.netAmount",
        "Order.refundedAmount"
       ],
       "operation": "listMyOrders",
       "provenance": "contract orders.yaml GET /my/orders"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected order",
       "bindsTo": "OrderSummary",
       "columns": [
        "OrderSummary.id",
        "OrderSummary.orderNumber",
        "OrderSummary.status",
        "OrderSummary.grossAmount",
        "OrderSummary.refundedAmount",
        "OrderSummary.channel",
        "OrderSummary.lineCount",
        "OrderSummary.principalId",
        "OrderSummary.holdLabel",
        "OrderSummary.heldUntil"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "detailPanel",
       "label": "The order",
       "bindsTo": "Order",
       "columns": [
        "Order.id",
        "Order.orderNumber",
        "Order.channel",
        "Order.venueId",
        "Order.scopePath",
        "Order.status",
        "Order.currency",
        "Order.currencyScale",
        "Order.grossAmount",
        "Order.taxAmount",
        "Order.netAmount",
        "Order.refundedAmount",
        "Order.totalPriceVariance",
        "Order.lines",
        "Order.payments",
        "Order.principalId"
       ],
       "operation": "getOrder",
       "provenance": "contract orders.yaml GET /orders/{orderId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Transfer order tickets",
       "operation": "transferOrderTickets",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The order history list.",
   "error": "Could not load. Names which read failed and leaves the order history untouched.",
   "emptyFirstRun": "No order history yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on venueId, principalId, shiftId, status, createdFrom, createdTo and the order history are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `listOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "List orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "getOrder",
    "contract": "orders",
    "purpose": "Read an order",
    "trigger": "onAction"
   },
   {
    "operationId": "listMyOrders",
    "contract": "orders",
    "purpose": "The orders this guest placed",
    "trigger": "onLoad"
   },
   {
    "operationId": "transferOrderTickets",
    "contract": "orders",
    "purpose": "Transfer tickets to another guest",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "listTaxInvoices",
    "contract": "finance",
    "purpose": "List tax invoices",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "issueTaxInvoice",
    "contract": "finance",
    "purpose": "Issue a tax invoice",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getTaxInvoice",
    "contract": "finance",
    "purpose": "Show a tax invoice",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listCreditMemos",
    "contract": "finance",
    "purpose": "List credit memos",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getTaxDocumentRendition",
    "contract": "finance",
    "purpose": "Download the invoice / credit memo PDF",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "deepLink"
    },
    {
     "name": "documentId",
     "from": "navigation"
    },
    {
     "name": "invoiceId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error.",
   "preloaded": [
    "OrderSummary.id",
    "OrderSummary.orderNumber",
    "OrderSummary.status",
    "OrderSummary.grossAmount",
    "OrderSummary.refundedAmount"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "designed",
   "board": "wireframes/P02 Guest App.dc.html#gst-019",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "Mobile App v4, 29 September 2026",
    "match": "none",
    "note": "Mobile App v4 has no view for this screen. Drawn by Claude Code on 30 September 2026 in the v4 look (the frame on this screen's board, wireframes/frames/gst-019.html, and #GST-019 in handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html). NOT client-verified: awaiting the client's design reviewer. Build the layout from that frame and this definition. Mobile v2 (28 September, superseded by v4) showed it at: Account → All screens → Wave 2 → Order history (exact)."
   },
   "source": "Claude Code, 30 September 2026, drawn in the Mobile App v4 look",
   "note": "**Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no value for an agent-drawn frame; it is the value the eight Claude Design frames of 29 September carry. Gaps the operations leave are in handoff/design-batches/apps/1-guest-app/return/FINDINGS.md."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formTransferOrderTickets",
    "component": "modal",
    "trigger": "Transfer order tickets",
    "body": "**Collects what `transferOrderTickets` sends before it is called.** Required: `ticketIds`, `recipient`. Optional: `message`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transfer order tickets",
     "operation": "transferOrderTickets"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "ticketIds",
      "recipient",
      "message"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-020",
  "name": "Saved Items / Wishlist",
  "module": "Account & Self-Service",
  "requiresModule": "marketing",
  "wave": 3,
  "capability": "C58",
  "implementation": {
   "app": "guest-app",
   "route": "/general/saved-items-wishlist",
   "component": "apps/guest-app/src/routes/general/SavedItemsWishlistList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-011"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-020 holds none of them. The edge carries nothing: GST-020 is opened from GST-001, so this edge is the way back and GST-001 keeps its own state"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Wishlist. **Device and consent operations removed 20 August** — Pranay asked why they were here, and the answer is that seven operations were attached in bulk to three unrelated screens. **Rewired on the 20 August review.**",
  "density": "comfortable",
  "pattern": "statusTracker",
  "patternReason": "`getWishlist` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Find the right one quickly, and act on it without opening it.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The wishlist",
       "bindsTo": "Wishlist",
       "columns": [
        "Wishlist.subjectId",
        "Wishlist.items"
       ],
       "operation": "getWishlist",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/wishlist"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add to wishlist",
       "operation": "addToWishlist",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/wishlist"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove from wishlist",
       "operation": "removeFromWishlist",
       "provenance": "contract marketing-crm.yaml DELETE /guests/{subjectId}/wishlist/{itemId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRemoveFromWishlist",
    "component": "confirmDialog",
    "trigger": "Remove from wishlist",
    "body": "**Names what `removeFromWishlist` changes and what it leaves alone**, in the consequence rather than the verb. A saved items wishlist this affects should be identified in the dialog, not just counted.",
    "provenance": "client-verified"
   },
   {
    "id": "formAddToWishlist",
    "component": "modal",
    "trigger": "Add to wishlist",
    "body": "**Collects what `addToWishlist` sends before it is called.** Required: `variantId`. Optional: `performanceId`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Add to wishlist",
     "operation": "addToWishlist"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "variantId",
      "performanceId",
      "note"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "states": {
   "loading": "The saved items wishlist, read by `getWishlist`.",
   "error": "Could not load. Names which read failed and leaves the saved items wishlist untouched.",
   "emptyFirstRun": "No saved items wishlist yet. Offers Add to wishlist (`addToWishlist`).",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "getWishlist",
    "contract": "marketing-crm",
    "purpose": "Read a guest's saved items",
    "trigger": "onLoad"
   },
   {
    "operationId": "addToWishlist",
    "contract": "marketing-crm",
    "purpose": "Save an item",
    "trigger": "onAction"
   },
   {
    "operationId": "removeFromWishlist",
    "contract": "marketing-crm",
    "purpose": "Remove a saved item",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "itemId",
     "from": "deepLink"
    },
    {
     "name": "subjectId",
     "from": "GST-001"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `itemId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-020",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 3 → Saved items / wishlist"
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-039",
  "name": "Profile",
  "module": "Account & Self-Service",
  "requiresModule": "marketing",
  "wave": 1,
  "capability": "C58",
  "implementation": {
   "app": "guest-app",
   "route": "/general/profile",
   "component": "apps/guest-app/src/routes/general/ProfileDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-065",
    "GST-066",
    "GST-069",
    "GST-071",
    "GST-073"
   ],
   "transitions": [
    {
     "to": "GST-065",
     "trigger": "And their marketing preferences",
     "provenance": "flow F56 step 4→5"
    },
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-039 holds none of them. The edge carries nothing: GST-039 is opened from GST-001, so this edge is the way back and GST-001 keeps its own state"
    },
    {
     "to": "GST-069",
     "trigger": "Face Pass",
     "provenance": "derived — GST-069 declares entryState.params enrolmentId and GST-039 holds none of them. The edge carries nothing: enrolmentId only pre-selects (deep link or optional), and GST-069 opens on its own"
    },
    {
     "to": "GST-071",
     "trigger": "Payment Methods",
     "provenance": "derived — GST-071 declares entryState.params cardCode, walletId and GST-039 holds none of them. The edge carries nothing: walletId only pre-selects (deep link or optional); GST-071 opens on listPaymentTokens, and cardCode has no source on GST-071 yet (a gap in GST-071, not in this edge)"
    },
    {
     "to": "GST-073",
     "trigger": "Security & Sign-in",
     "provenance": "derived — GST-073 declares entryState.params challengeId, methodId and GST-039 holds none of them. The edge carries nothing: GST-073 finds challengeId (createMfaChallenge), methodId (enrolMfaMethod) itself, and GST-073 opens on its own"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement.\n\n**29 September (W1).** A profile created by guest checkout shows *Complete your details*.",
  "density": "comfortable",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`recordConsent`) and no read of a population — it is settings, not a list",
  "purpose": "What we hold about a guest, and what they can change.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "purpose",
       "bindsTo": "RecordConsentRequest.purpose",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/consents"
      },
      {
       "kind": "textField",
       "label": "decision",
       "bindsTo": "RecordConsentRequest.decision",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/consents"
      },
      {
       "kind": "textField",
       "label": "channels",
       "bindsTo": "RecordConsentRequest.channels",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/consents"
      },
      {
       "kind": "textField",
       "label": "noticeVersion",
       "bindsTo": "RecordConsentRequest.noticeVersion",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/consents"
      },
      {
       "kind": "textField",
       "label": "source",
       "bindsTo": "RecordConsentRequest.source",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/consents"
      },
      {
       "kind": "textField",
       "label": "recordedAt",
       "bindsTo": "RecordConsentRequest.recordedAt",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/consents"
      },
      {
       "kind": "banner",
       "label": "Complete your details",
       "operation": "updateMyProfile",
       "notes": "For a profile created by guest checkout (W1): asks for what the pop-up did not, whenever the guest likes; never blocks anything.",
       "provenance": "decided 29 September 2026, W1"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Record consent",
       "operation": "recordConsent",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/consents"
      },
      {
       "kind": "secondaryButton",
       "label": "Save my profile",
       "operation": "updateMyProfile",
       "provenance": "contract marketing-crm.yaml PATCH /guests/me/profile"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved profile.",
   "error": "Could not load. Names which read failed and leaves the profile untouched.",
   "emptyFirstRun": "No profile configured. The form opens empty and `recordConsent` saves the first one; it says what the platform does in the meantime.",
   "emptyNoAccess": "Shown when the caller lacks `GUEST_VIEW`, which `updateMyProfile` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "recordConsent",
    "contract": "marketing-crm",
    "purpose": "Record a consent decision",
    "trigger": "onAction"
   },
   {
    "operationId": "updateMyProfile",
    "contract": "marketing-crm",
    "purpose": "Change name, contact and preferences",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "subjectId",
     "from": "GST-001"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "designed",
   "board": "wireframes/P02 Guest App.dc.html#gst-039",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "Mobile App v4, 29 September 2026",
    "match": "none",
    "note": "Mobile App v4 has no view for this screen. Drawn by Claude Code on 30 September 2026 in the v4 look (the frame on this screen's board, wireframes/frames/gst-039.html, and #GST-039 in handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html). NOT client-verified: awaiting the client's design reviewer. Build the layout from that frame and this definition. Mobile v2 (28 September, superseded by v4) showed it at: Account → All screens → Wave 1 → Profile (also Account → Profile) (exact). What v2 did differently: Emirates ID upload is on Profile in the prototype; the YAML has uploadGuestDocument on GST-066. Account also has a \"Saved guests (heights on file)\" row that no screen defines."
   },
   "source": "Claude Code, 30 September 2026, drawn in the Mobile App v4 look",
   "note": "**Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no value for an agent-drawn frame; it is the value the eight Claude Design frames of 29 September carry. Gaps the operations leave are in handoff/design-batches/apps/1-guest-app/return/FINDINGS.md."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formUpdateMyProfile",
    "component": "modal",
    "trigger": "Save my profile",
    "body": "**Collects what `updateMyProfile` sends before it is called.** Nothing in the body is required. Optional: `displayName`, `email`, `phone`, `preferredLanguage`, `preferredChannel`, `dietary`, `accessibility`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save my profile",
     "operation": "updateMyProfile"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "displayName",
      "email",
      "phone",
      "preferredLanguage",
      "preferredChannel",
      "dietary",
      "accessibility"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-042",
  "name": "Simple Registration & OTP",
  "module": "Account & Self-Service",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C56",
  "implementation": {
   "app": "guest-app",
   "route": "/general/simple-registration-and-otp",
   "component": "apps/guest-app/src/routes/general/SimpleRegistrationAndOtpDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-041",
    "GST-008",
    "GST-077",
    "GST-079"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-041"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-042 holds none of them. The edge carries nothing: GST-042 is opened from GST-001, so this edge is the way back and GST-001 keeps its own state"
    },
    {
     "to": "GST-041",
     "trigger": "Signed in and verified — back to the cart",
     "precondition": "arrived from the cart",
     "carries": [
      "cartId"
     ],
     "provenance": "decided 17 September 2026 — no order against an unproven contact; rule on identity verifyGuestEmail, per-site guestCheckout off by default (matrix 2.6.28)"
    },
    {
     "to": "WEB-016",
     "trigger": "A guest who checked out anonymously links their order",
     "provenance": "flow F56 step 2→3",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "challengeId",
      "subjectId"
     ]
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Corrected 24 August**: removed getCurrentSession, logout, selectRole. **A guest surface has no roles to select and its own logout.** `selectRole` is ADR-0002 staff authorisation; `getCurrentSession` is the staff session. `guestLogout` and `getGuestSession` already existed — the screen was reaching into the staff identity surface because nothing checked that a guest platform only calls guest operations. **Rebuilt 28 September as a guest sign-in form** (decided 28 September, audit R167, R073 (a)): removed `login`, `startSsoAuthorization`, `completeSsoAuthorization`, `listSsoProviders` and the six MFA operations — guests have no enterprise SSO. **The second factor came back on 29 September, per venue** (see below). Password sign-in is `guestPasswordLogin`.\n\n**Rev 3 (decided 29 September).** **Guest two-step verification is per venue, off by default** (GAP-B1, `VenueSettings.identity.guestTwoStep`; supersedes the second part of audit R167; no enterprise SSO stands). The prompt appears only when signing in or acting at a venue that has it on; enrolment is on the guest's account (GST-073). **Sign-in gate (REV3-3):** reached from GST-008 (after add-ons) or GST-041 (at payment), returning to the basket with it kept; guest checkout and matching unchanged (DG-1).\n\n**The venue in context is sent** (decided 29 September, rev 3 GAP-B1, per venue): `verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin` and `createMfaChallenge` take an optional `venueId`, the venue the app or booking is in, so the second factor is asked only where that venue has guest two-step verification on.\n\n**29 September (W1).** The guest pop-up asks only `guestContactFields` (Email only / + name / + mobile), then the six-digit code (DG-1). After the code the guest is not asked for name, email or phone again: back to the basket and on to the T&Cs (GST-009).",
  "density": "comfortable",
  "pattern": "form",
  "patternReason": "**A sign-in form, not a list.** Four ways in (a one-time code, a password, Apple or Google, UAE Pass) and a way to register; `getGuestSession` is the one piece of context. Rebuilt 28 September: the screen had been generated as a list of MFA methods and SSO providers, neither of which a guest has (decided 28 September, audit R167, R073 (a)). The second-factor prompt is back as a step of sign-in, only at a venue that has guest two-step verification on (decided 29 September, rev 3 GAP-B1).",
  "purpose": "Get a guest into the app, fast, on a device that may be shared: a one-time code to the email or mobile, a password, Apple or Google, or UAE Pass, or register a new account. **No enterprise SSO for guests** (decided 28 September, audit R167, first part). **A second factor only where the venue enabled guest two-step verification** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of R167).",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "signIn",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Email or mobile number",
       "operation": "requestGuestOtp",
       "notes": "**Guest checkout asks only the configured fields** (W1): `BookingFlowSettings.guestContactFields` (email, mobile, name; at least the `GuestMatchPolicy.matchBy` key). Nothing else is asked.",
       "provenance": "contract identity.yaml POST /auth/guest/otp"
      },
      {
       "kind": "primaryButton",
       "label": "Send me a code",
       "operation": "requestGuestOtp",
       "provenance": "contract identity.yaml POST /auth/guest/otp"
      },
      {
       "kind": "textField",
       "label": "Code",
       "operation": "verifyGuestOtp",
       "notes": "Shown once a code has been sent; `verifyGuestOtp` returns the `GuestSession`.",
       "provenance": "contract identity.yaml POST /auth/guest/otp/verify"
      },
      {
       "kind": "primaryButton",
       "label": "Sign in with the code",
       "operation": "verifyGuestOtp",
       "provenance": "contract identity.yaml POST /auth/guest/otp/verify"
      },
      {
       "kind": "textField",
       "label": "Password",
       "operation": "guestPasswordLogin",
       "notes": "**Password sign-in** (decided 28 September, audit R073 (a)): sends `identifier`, `password` and the device's `deviceId` to `guestPasswordLogin`, which returns the same `GuestSession`. A wrong password, an unknown identifier and an account with no password are one answer (401) and the screen shows one message for all of them, never which it was. Signing in here ends this device's previous guest session.",
       "provenance": "contract identity.yaml POST /auth/guest/password"
      },
      {
       "kind": "secondaryButton",
       "label": "Sign in with password",
       "operation": "guestPasswordLogin",
       "provenance": "contract identity.yaml POST /auth/guest/password"
      },
      {
       "kind": "secondaryButton",
       "label": "Continue with Apple or Google",
       "operation": "guestSocialLogin",
       "provenance": "contract identity.yaml POST /auth/guest/social"
      },
      {
       "kind": "secondaryButton",
       "label": "Continue with UAE Pass",
       "operation": "guestUaePassLogin",
       "provenance": "contract identity.yaml POST /auth/guest/uae-pass"
      },
      {
       "kind": "secondaryButton",
       "label": "Create an account",
       "operation": "registerGuest",
       "provenance": "contract identity.yaml POST /auth/guest/register"
      },
      {
       "kind": "textField",
       "label": "Verification code",
       "notes": "Only when the returned `GuestSession` has `requiresMfa`: at a venue whose `VenueSettings.identity.guestTwoStep.enabled` is on, for a guest who enrolled a method. At any other venue nothing is asked.",
       "operation": "verifyMfaChallenge",
       "provenance": "decided 29 September, rev 3 GAP-B1 (per venue)"
      }
     ]
    },
    {
     "name": "session",
     "slot": "context",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Who is signed in on this device",
       "bindsTo": "GuestSession",
       "columns": [
        "GuestSession.subjectId",
        "GuestSession.displayName",
        "GuestSession.isVerified",
        "GuestSession.identityProviders",
        "GuestSession.preferredLanguage",
        "GuestSession.expiresAt"
       ],
       "operation": "getGuestSession",
       "notes": "Shown only when a guest session already exists on this device, with a way to sign out so a shared device is handed over clean.",
       "provenance": "contract identity.yaml GET /auth/guest/session"
      },
      {
       "kind": "secondaryButton",
       "label": "Sign out",
       "operation": "guestLogout",
       "provenance": "contract identity.yaml DELETE /auth/guest/session"
      },
      {
       "kind": "secondaryButton",
       "label": "Link an order I placed as a guest",
       "operation": "linkGuestCheckout",
       "provenance": "contract identity.yaml POST /auth/guest/link-checkout"
      },
      {
       "kind": "secondaryButton",
       "label": "Refresh token",
       "operation": "refreshToken",
       "notes": "Not a button the guest sees; the client rotates the access token before it expires.",
       "provenance": "contract identity.yaml POST /auth/refresh"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "formRegisterGuest",
    "component": "modal",
    "trigger": "Create an account",
    "body": "**Collects what `registerGuest` sends before it is called.** Required: `identifier`, `channel`. Optional: `displayName`, `password`, `preferredLanguage`, `consents`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RegisterGuestRequest",
    "confirm": {
     "label": "Register guest",
     "operation": "registerGuest"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "identifier",
      "channel",
      "displayName",
      "password",
      "preferredLanguage",
      "consents"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formGuestPasswordLogin",
    "component": "modal",
    "trigger": "Sign in with password",
    "body": "**Collects what `guestPasswordLogin` sends before it is called.** Required: `identifier`, `password`. Optional: `deviceId` (sent by the client, not typed). A 401 is one message whatever the cause; a 429 or a locked account says to try again later or use a one-time code instead (decided 28 September, audit R073 (a)). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Sign in",
     "operation": "guestPasswordLogin"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "identifier",
      "password",
      "deviceId"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formGuestSocialLogin",
    "component": "modal",
    "trigger": "Continue with Apple or Google",
    "body": "**Collects what `guestSocialLogin` sends before it is called.** Required: `provider`, `idToken`. Optional: `deviceId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Guest social login",
     "operation": "guestSocialLogin"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "provider",
      "idToken",
      "deviceId"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formGuestUaePassLogin",
    "component": "modal",
    "trigger": "Continue with UAE Pass",
    "body": "**Collects what `guestUaePassLogin` sends before it is called.** Required: `code`, `redirectUri`. Optional: `state`, `deviceId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Guest uae pass login",
     "operation": "guestUaePassLogin"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "redirectUri",
      "state",
      "deviceId"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formLinkGuestCheckout",
    "component": "modal",
    "trigger": "Link an order I placed as a guest",
    "body": "**Collects what `linkGuestCheckout` sends before it is called.** Required: `orderReference`. Optional: `verificationCode`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Link guest checkout",
     "operation": "linkGuestCheckout"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "orderReference",
      "verificationCode"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formRefreshToken",
    "component": "modal",
    "trigger": "Refresh token",
    "body": "**Collects what `refreshToken` sends before it is called.** Required: `refreshToken`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Refresh token",
     "operation": "refreshToken"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "refreshToken"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formRequestGuestOtp",
    "component": "modal",
    "trigger": "Send me a code",
    "body": "**Collects what `requestGuestOtp` sends before it is called.** Required: `identifier`, `channel`. Optional: `purpose`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Request guest OTP",
     "operation": "requestGuestOtp"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "identifier",
      "channel",
      "purpose"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formVerifyGuestOtp",
    "component": "modal",
    "trigger": "Sign in with the code",
    "body": "**Collects what `verifyGuestOtp` sends before it is called.** Required: `identifier`, `code`. Optional: `deviceId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Verify guest OTP",
     "operation": "verifyGuestOtp"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "identifier",
      "code",
      "deviceId"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "states": {
   "loading": "Checking whether this device already holds a guest session. The sign-in form stays visible.",
   "error": "Identity could not be reached. **Says so rather than saying the password or code is wrong**, and keeps what was typed.",
   "emptyFirstRun": "**Nobody signed in on this device** — the normal state. The form offers a code, a password, Apple or Google and UAE Pass, and Create an account (`registerGuest`).",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025), and this is the screen a guest who is not signed in is sent to, so it has no no-access case of its own. A session that has expired lands here with the screen it came from kept, and returns to it after sign-in.",
   "signInRefused": "**One message for every refusal of a password sign-in**: `guestPasswordLogin` answers 401 alike for a wrong password, an unknown identifier, an account with no password and a locked account, and the screen never says which. Too many attempts (429, or the lockout after `PasswordPolicy.lockoutAfterAttempts`) says to try again later and offers **Send me a code** instead (decided 28 September, audit R073 (a)).",
   "offline": "**Not available, and the offline banner says why.** Signing in, registering and verifying a code need the server."
  },
  "apis": [
   {
    "operationId": "registerGuest",
    "contract": "identity",
    "purpose": "Create a guest account",
    "trigger": "onAction",
    "invalidates": [
     "getGuestSession"
    ]
   },
   {
    "operationId": "getGuestSession",
    "contract": "identity",
    "purpose": "Read the current guest session",
    "trigger": "onLoad"
   },
   {
    "operationId": "guestLogout",
    "contract": "identity",
    "purpose": "End a guest session",
    "trigger": "onAction",
    "invalidates": [
     "getGuestSession"
    ]
   },
   {
    "operationId": "guestPasswordLogin",
    "contract": "identity",
    "purpose": "Sign in with the email or mobile and the password set at registration (identifier, password, deviceId -> GuestSession); one indistinguishable 401, lockout, 429 (decided 28 September, audit R073 (a))",
    "trigger": "onAction",
    "invalidates": [
     "getGuestSession"
    ]
   },
   {
    "operationId": "guestSocialLogin",
    "contract": "identity",
    "purpose": "Sign in with Apple or Google",
    "trigger": "onAction",
    "invalidates": [
     "getGuestSession"
    ]
   },
   {
    "operationId": "guestUaePassLogin",
    "contract": "identity",
    "purpose": "Sign in with a national identity provider",
    "trigger": "onAction",
    "invalidates": [
     "getGuestSession"
    ]
   },
   {
    "operationId": "linkGuestCheckout",
    "contract": "identity",
    "purpose": "Attach a guest checkout to an account",
    "trigger": "onAction"
   },
   {
    "operationId": "refreshToken",
    "contract": "identity",
    "purpose": "Rotate the access token",
    "trigger": "onAction"
   },
   {
    "operationId": "requestGuestOtp",
    "contract": "identity",
    "purpose": "Request a one-time code",
    "trigger": "onAction"
   },
   {
    "operationId": "verifyGuestOtp",
    "contract": "identity",
    "purpose": "Verify a one-time code and issue a session",
    "trigger": "onAction",
    "invalidates": [
     "getGuestSession"
    ]
   },
   {
    "operationId": "createMfaChallenge",
    "contract": "identity",
    "purpose": "Ask for the second factor (`action: signIn`) when the session comes back `requiresMfa` at a venue with guest two-step verification on",
    "trigger": "onAction"
   },
   {
    "operationId": "verifyMfaChallenge",
    "contract": "identity",
    "purpose": "Check the code and release the session",
    "trigger": "onAction",
    "invalidates": [
     "getGuestSession"
    ]
   },
   {
    "operationId": "claimDeviceConsent",
    "contract": "marketing-crm",
    "purpose": "Attach this device's tracking decision to the guest after sign-in or registration",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "cartId",
     "from": "session"
    },
    {
     "name": "challengeId",
     "from": "navigation"
    },
    {
     "name": "subjectId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Needs nothing.** A guest arriving cold signs in and goes Home; one sent from the cart carries `cartId` and goes back to it. The SSO deep-link parameter (`providerId`) went with the operations that used it (audit R167); a second-factor challenge is created in place, never arrives by link."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "designed",
   "board": "wireframes/P02 Guest App.dc.html#gst-042",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "Mobile App v4, 29 September 2026",
    "match": "none",
    "note": "Mobile App v4 has no view for this screen. Drawn by Claude Code on 30 September 2026 in the v4 look (the frame on this screen's board, wireframes/frames/gst-042.html, and #GST-042 in handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html). NOT client-verified: awaiting the client's design reviewer. Build the layout from that frame and this definition. Mobile v2 (28 September, superseded by v4) showed it at: Account → All screens → Wave 1 → Simple registration & OTP (same #ident screen) + \"Log in or register\" sheet from home (partial). What v2 did differently: Prototype has email code, Apple and Google only; the YAML also has password login, UAE Pass and explicit registration."
   },
   "source": "Claude Code, 30 September 2026, drawn in the Mobile App v4 look",
   "note": "**Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no value for an agent-drawn frame; it is the value the eight Claude Design frames of 29 September carry. Gaps the operations leave are in handoff/design-batches/apps/1-guest-app/return/FINDINGS.md."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 18 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-045",
  "name": "Ticket Delivery & Sharing",
  "module": "Account & Self-Service",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C02",
  "implementation": {
   "app": "guest-app",
   "route": "/general/ticket-delivery-and-sharing",
   "component": "apps/guest-app/src/routes/general/TicketDeliveryAndSharingDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-045 holds none of them. The edge carries nothing: GST-045 is opened from GST-001, so this edge is the way back and GST-001 keeps its own state"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement.\n\n**Rev 3 (decided 29 September).** GST-014 and GST-045 (and the old GST-008 transfer reading) are one implementation with several screen ids; the ids are kept (GAP-D3).",
  "density": "comfortable",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`transferOrderTickets`) and no read of a population — it is settings, not a list",
  "purpose": "Find ticket delivery & sharing for this venue.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Transfer order tickets",
       "operation": "transferOrderTickets",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "multiSelect",
       "label": "Ticket ids",
       "operation": "transferOrderTickets",
       "notes": "Required.",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      },
      {
       "kind": "textField",
       "label": "Recipient",
       "operation": "transferOrderTickets",
       "notes": "Required.",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      },
      {
       "kind": "textField",
       "label": "Message",
       "operation": "transferOrderTickets",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Availability is live, never cached",
   "error": "Availability unavailable. **Selection is blocked** — overselling is worse than waiting",
   "emptyFirstRun": "**Sold out is a real answer.** Offers the next available rather than a dead end",
   "offline": "**The offline banner shows.** Sending, claiming and listing for resale need the connection — a transfer nobody received is a ticket nobody holds. Tickets already loaded stay visible."
  },
  "apis": [
   {
    "operationId": "transferOrderTickets",
    "contract": "orders",
    "purpose": "Transfer tickets to another guest",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-045",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "partial",
    "view": "Account → All screens → Wave 2 → Ticket delivery & sharing (opens Ticket transfer)",
    "differences": "No screen of its own; it shares GST-014’s screen until the client confirms."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-055",
  "name": "Dynamic QR Ticket",
  "module": "Account & Self-Service",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C09",
  "implementation": {
   "app": "guest-app",
   "route": "/general/dynamic-qr-ticket",
   "component": "apps/guest-app/src/routes/general/DynamicQrTicketCanvas.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-013"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-055 holds none of them. The edge carries nothing: GST-055 is opened from GST-001, so this edge is the way back and GST-001 keeps its own state"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "comfortable",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`transferOrderTickets`) and no read of a population — it is settings, not a list",
  "purpose": "Find dynamic qr ticket for this venue.",
  "gaps": [
   {
    "operation": "getEntitlementCredential",
    "why": "**`getEntitlementCredential` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.",
    "source": "contract access.yaml GET /entitlements/{entitlementId}/credential"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Transfer order tickets",
       "operation": "transferOrderTickets",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      },
      {
       "kind": "secondaryButton",
       "label": "Bind credential device",
       "operation": "bindCredentialDevice",
       "notes": "**The guest app binds a mobile credential to the phone it is shown on** (P02 GST-055 Dynamic QR Ticket), before the dynamic QR is displayed.",
       "provenance": "contract access.yaml POST /my/credentials/{credentialId}/device-bindings"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every entitlement",
       "bindsTo": "Entitlement",
       "columns": [
        "Entitlement.id",
        "Entitlement.templateId",
        "Entitlement.productId",
        "Entitlement.orderId",
        "Entitlement.orderLineId",
        "Entitlement.subjectId",
        "Entitlement.venueId",
        "Entitlement.scopePath",
        "Entitlement.mediaCode",
        "Entitlement.status",
        "Entitlement.statusNote",
        "Entitlement.validFrom"
       ],
       "operation": "listMyEntitlements",
       "provenance": "contract access.yaml GET /guests/me/entitlements"
      },
      {
       "kind": "detailPanel",
       "label": "Entitlement credential",
       "operation": "getEntitlementCredential",
       "notes": "Shows `mediaCode`, `payload`, `expiresAt` from `getEntitlementCredential`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one. **A rotating code derived on the device** (decided 28 September, audit R230): while online the screen fetches `rotation` (secret, `timeStepSeconds`, `digits`, `algorithm`, valid `validFrom` to `validTo`) and computes the current code from the seed and the clock, with a visible countdown to the next step; it keeps rotating with no signal. A null `rotation` (wristband, wallet pass) shows the static code.",
       "provenance": "contract access.yaml GET /entitlements/{entitlementId}/credential"
      },
      {
       "kind": "detailPanel",
       "label": "The entitlement",
       "bindsTo": "Entitlement",
       "columns": [
        "Entitlement.id",
        "Entitlement.templateId",
        "Entitlement.productId",
        "Entitlement.orderId",
        "Entitlement.orderLineId",
        "Entitlement.subjectId",
        "Entitlement.venueId",
        "Entitlement.scopePath",
        "Entitlement.mediaCode",
        "Entitlement.status",
        "Entitlement.statusNote",
        "Entitlement.validFrom",
        "Entitlement.validTo",
        "Entitlement.entriesUsed",
        "Entitlement.entriesAllowed",
        "Entitlement.lastEntryAt"
       ],
       "operation": "getEntitlement",
       "provenance": "contract access.yaml GET /entitlements/{entitlementId}"
      },
      {
       "kind": "multiSelect",
       "label": "Ticket ids",
       "operation": "transferOrderTickets",
       "notes": "Required.",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      },
      {
       "kind": "textField",
       "label": "Recipient",
       "operation": "transferOrderTickets",
       "notes": "Required.",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      },
      {
       "kind": "textField",
       "label": "Message",
       "operation": "transferOrderTickets",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Availability is live, never cached",
   "error": "Availability unavailable. **Selection is blocked** — overselling is worse than waiting",
   "emptyFirstRun": "**Sold out is a real answer.** Offers the next available rather than a dead end",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `listMyEntitlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** A ticket already loaded shows its rotating code, derived on the device from its seed, so it changes with no signal (decided 28 September, audit R230). Transferring a ticket needs the connection."
  },
  "apis": [
   {
    "operationId": "listMyEntitlements",
    "contract": "access",
    "purpose": "The guest's tickets and passes",
    "trigger": "onLoad"
   },
   {
    "operationId": "getEntitlement",
    "contract": "access",
    "purpose": "The selected ticket",
    "trigger": "onAction"
   },
   {
    "operationId": "getEntitlementCredential",
    "contract": "access",
    "purpose": "The QR code that gets scanned, refreshed — with the `rotation` seed the device derives the rotating code from (audit R230)",
    "trigger": "onAction"
   },
   {
    "operationId": "transferOrderTickets",
    "contract": "orders",
    "purpose": "Transfer tickets to another guest",
    "trigger": "onAction"
   },
   {
    "operationId": "bindCredentialDevice",
    "contract": "access",
    "purpose": "Bind my credential to this device",
    "trigger": "onAction",
    "invalidates": [
     "listMyEntitlements"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "deepLink"
    },
    {
     "name": "entitlementId",
     "from": "navigation"
    },
    {
     "name": "credentialId",
     "from": "navigation",
     "optional": true
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-055",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 1 → Dynamic QR ticket; also the Scan tab overlay",
    "differences": "The Scan overlay also scans table codes and lockers (\"Scan a table code or locker with the same button\"), which the YAML does not cover."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formBindCredentialDevice",
    "component": "modal",
    "trigger": "Bind credential device",
    "body": "**Collects what `bindCredentialDevice` sends before it is called.** Required: `deviceId`. Optional: `deviceReference`, `appInstallationId`, `os`, `otp`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CredentialDeviceBindingInput",
    "confirm": {
     "label": "Bind credential device",
     "operation": "bindCredentialDevice"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "deviceId",
      "deviceReference",
      "appInstallationId",
      "os",
      "otp"
     ]
    },
    "provenance": "contract access.yaml POST /my/credentials/{credentialId}/device-bindings"
   }
  ],
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-066",
  "name": "Privacy & My Data",
  "module": "Account & Self-Service",
  "requiresModule": "core",
  "wave": 2,
  "capability": "read-write",
  "implementation": {
   "app": "guest-app",
   "route": "/account/privacy-my-data",
   "component": "apps/guest-app/src/routes/account/PrivacyMyData.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "GST-039"
   ],
   "entryFrom": [
    "GST-039"
   ],
   "inferred": false,
   "notes": "**Reached from GST-039** — privacy is a setting on the profile. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "GST-039",
     "trigger": "Profile",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-039 declares entryState.params subjectId and GST-066 holds subjectId, so an edge into it carries them"
    }
   ]
  },
  "notes": "**A guest can legally demand their data and its erasure, and had nowhere to ask.** `exportSubjectData` and `deleteGuestAccount` existed as guest-callable operations reachable from no guest surface — a promise the contracts made and the product did not keep.\n\n**Erasure is not a button.** `platform.dsar_request` carries a legal clock and a lifecycle; this screen starts it and shows where it has got to. **A request that silently fails is a regulatory failure with a timestamp on it** (ADR-0033).",
  "density": "comfortable",
  "offline": false,
  "pattern": "statusTracker",
  "patternReason": "`getGuestConsents` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "**A guest can legally demand their data and its erasure, and had nowhere to ask.** `exportSubjectData` and `deleteGuestAccount` existed as guest-callable operations reachable from no guest surface — a",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The consent state",
       "bindsTo": "ConsentState",
       "columns": [
        "ConsentState.subjectId",
        "ConsentState.purposes"
       ],
       "operation": "getGuestConsents",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/consents"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "destructiveButton",
       "label": "Delete guest account",
       "operation": "deleteGuestAccount",
       "provenance": "contract identity.yaml DELETE /auth/guest/account"
      },
      {
       "kind": "secondaryButton",
       "label": "Save guest preferences",
       "operation": "updateGuestPreferences",
       "provenance": "contract marketing-crm.yaml PUT /guests/{subjectId}/preferences"
      },
      {
       "kind": "secondaryButton",
       "label": "Upload guest document",
       "operation": "uploadGuestDocument",
       "provenance": "contract marketing-crm.yaml POST /guest-documents"
      },
      {
       "kind": "secondaryButton",
       "label": "Export subject data",
       "operation": "exportSubjectData",
       "provenance": "contract identity.yaml POST /guests/{subjectId}/data-export"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDeleteGuestAccount",
    "component": "confirmDialog",
    "trigger": "Delete guest account",
    "body": "**Names what `deleteGuestAccount` changes and what it leaves alone**, in the consequence rather than the verb. A privacy data this affects should be identified in the dialog, not just counted.",
    "provenance": "client-verified"
   },
   {
    "id": "formUpdateGuestPreferences",
    "component": "modal",
    "trigger": "Save guest preferences",
    "body": "**Collects what `updateGuestPreferences` sends before it is called.** Nothing in the body is required. Optional: `id`, `subjectId`, `seatingPreference`, `drinkPreferences`, `dietary`, `accessibility`, `preferredChannel`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "GuestPreferences",
    "confirm": {
     "label": "Save guest preferences",
     "operation": "updateGuestPreferences"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "subjectId",
      "seatingPreference",
      "drinkPreferences",
      "dietary",
      "accessibility",
      "preferredChannel"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formUploadGuestDocument",
    "component": "modal",
    "trigger": "Upload guest document",
    "body": "**Collects what `uploadGuestDocument` sends before it is called.** Required: `id`, `subjectId`, `kind`, `storageRef`, `retainUntil`. Optional: `contentType`, `consentPurposeId`, `uploadedAt`, `uploadedByPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "GuestDocument",
    "confirm": {
     "label": "Upload guest document",
     "operation": "uploadGuestDocument"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "subjectId",
      "kind",
      "storageRef",
      "retainUntil",
      "contentType",
      "consentPurposeId",
      "uploadedAt",
      "uploadedByPrincipalId"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "states": {
   "loading": "Content loads.",
   "error": "Could not load. **Says what failed and offers one way onward**, never a bare failure.",
   "emptyFirstRun": "**Nothing requested yet.** No export, no erasure, no document — and that is the ordinary state. **The screen explains what each request means before offering it**, because an erasure a guest did not understand is one they will phone about.",
   "emptyNoResults": "**Nothing here yet.** The scope is what narrowed it — naming the scope is what stops somebody concluding the record does not exist.",
   "emptyNoAccess": "Shown when the caller lacks `GUEST_VIEW_PII`, which `exportSubjectData` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Nothing here is offered offline, and the banner says so.** An erasure request or a device change queued and never sent is worse than one that could not be made — the legal clock starts when the platform receives it, and a device signed out offline is still signed in."
  },
  "apis": [
   {
    "operationId": "exportSubjectData",
    "contract": "identity",
    "purpose": "Everything the platform holds about one guest",
    "trigger": "onAction"
   },
   {
    "operationId": "deleteGuestAccount",
    "contract": "identity",
    "purpose": "Self-service account deletion",
    "trigger": "onAction"
   },
   {
    "operationId": "getGuestConsents",
    "contract": "marketing-crm",
    "purpose": "Read a guest's consent state",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateGuestPreferences",
    "contract": "marketing-crm",
    "purpose": "The things a regular should not have to say twice",
    "trigger": "onAction"
   },
   {
    "operationId": "uploadGuestDocument",
    "contract": "marketing-crm",
    "purpose": "Store a guest photo, ID or signed document",
    "trigger": "onAction"
   },
   {
    "operationId": "getCookieConsentRuntime",
    "contract": "marketing-crm",
    "purpose": "Tracking preferences: categories and the current decision",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listPublishedTrackingTechnologies",
    "contract": "marketing-crm",
    "purpose": "Each SDK and tracker the app uses",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getDeviceConsentHistory",
    "contract": "marketing-crm",
    "purpose": "My tracking decisions so far",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "recordDeviceConsent",
    "contract": "marketing-crm",
    "purpose": "Change or withdraw tracking preferences",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "subjectId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session.** A guest arriving cold is asked to sign in and returned here afterwards — never a 404, and never a screen that silently shows somebody else's data (ADR-0030)."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "designed",
   "board": "wireframes/P02 Guest App.dc.html#gst-066",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "Mobile App v4, 29 September 2026",
    "match": "none",
    "note": "Mobile App v4 has no view for this screen. Drawn by Claude Code on 30 September 2026 in the v4 look (the frame on this screen's board, wireframes/frames/gst-066.html, and #GST-066 in handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html). NOT client-verified: awaiting the client's design reviewer. Build the layout from that frame and this definition. Mobile v2 (28 September, superseded by v4) showed it at: Account → All screens → Wave 2 → Privacy & my data (#privacy; also Account → Data & privacy) (exact). What v2 did differently: The prototype labels this screen \"GST-070 · Your data\" (aria-label \"GST-070 Data and privacy\"), but GST-070 is Reserve a Table in the YAML, so the label is wrong. Document upload is on Profile instead."
   },
   "source": "Claude Code, 30 September 2026, drawn in the Mobile App v4 look",
   "note": "**Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no value for an agent-drawn frame; it is the value the eight Claude Design frames of 29 September carry. Gaps the operations leave are in handoff/design-batches/apps/1-guest-app/return/FINDINGS.md."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "addToWishlist": {
  "method": "POST",
  "path": "/guests/{subjectId}/wishlist",
  "contract": "marketing-crm",
  "summary": "Save an item",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Wishlist"
 },
 "bindCredentialDevice": {
  "method": "POST",
  "path": "/my/credentials/{credentialId}/device-bindings",
  "contract": "access",
  "summary": "Bind my credential to this device",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CredentialDeviceBindingInput",
  "responds": "AccessDeviceBinding"
 },
 "claimDeviceConsent": {
  "method": "POST",
  "path": "/guests/{subjectId}/consents/claim-device",
  "contract": "marketing-crm",
  "summary": "Attach a browser's cookie decision to the guest who turned out to own it",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ClaimDeviceConsentRequest",
  "responds": "ConsentState"
 },
 "createMfaChallenge": {
  "method": "POST",
  "path": "/auth/mfa/challenge",
  "contract": "identity",
  "summary": "Second factor at staff sign-in, and step-up for a sensitive action",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "deleteGuestAccount": {
  "method": "DELETE",
  "path": "/auth/guest/account",
  "contract": "identity",
  "summary": "Self-service account deletion",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "exportSubjectData": {
  "method": "POST",
  "path": "/guests/{subjectId}/data-export",
  "contract": "identity",
  "summary": "Everything the platform holds about one guest",
  "permission": "GUEST_VIEW_PII",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "getCookieConsentRuntime": {
  "method": "GET",
  "path": "/storefront/cookie-consent",
  "contract": "marketing-crm",
  "summary": "What the page must show and what it may load",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "channel",
    "in": "query",
    "required": true
   },
   {
    "name": "brandId",
    "in": "query",
    "required": false
   },
   {
    "name": "language",
    "in": "query",
    "required": false
   },
   {
    "name": "X-Consent-Key",
    "in": "header",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "CookieConsentRuntime"
 },
 "getDeviceConsentHistory": {
  "method": "GET",
  "path": "/consent/device/history",
  "contract": "marketing-crm",
  "summary": "A visitor's own cookie decisions, oldest first",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "X-Consent-Key",
    "in": "header",
    "required": true
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "getEntitlement": {
  "method": "GET",
  "path": "/entitlements/{entitlementId}",
  "contract": "access",
  "summary": "One entitlement, with what remains on it",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Entitlement"
 },
 "getEntitlementCredential": {
  "method": "GET",
  "path": "/entitlements/{entitlementId}/credential",
  "contract": "access",
  "summary": "The thing that gets scanned",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "rotate",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "getEntitlementHistory": {
  "method": "GET",
  "path": "/entitlements/{entitlementId}/history",
  "contract": "access",
  "summary": "Every scan, freeze, share and reissue against it",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": null
 },
 "getGuestConsents": {
  "method": "GET",
  "path": "/guests/{subjectId}/consents",
  "contract": "marketing-crm",
  "summary": "Read a guest's consent state",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ConsentState"
 },
 "getGuestSession": {
  "method": "GET",
  "path": "/auth/guest/session",
  "contract": "identity",
  "summary": "Read the current guest session",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestSession"
 },
 "getOrder": {
  "method": "GET",
  "path": "/orders/{orderId}",
  "contract": "orders",
  "summary": "Read an order",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Order"
 },
 "getOrderCalendarEvent": {
  "method": "GET",
  "path": "/orders/{orderId}/calendar-event",
  "contract": "orders",
  "summary": "The visit as a calendar entry",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": null
 },
 "getTaxDocumentRendition": {
  "method": "GET",
  "path": "/tax-documents/{documentId}/rendition",
  "contract": "finance",
  "summary": "The PDF of a tax invoice or credit memo, in a language",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "language",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "FinTaxDocumentRendition"
 },
 "getTaxInvoice": {
  "method": "GET",
  "path": "/tax-invoices/{invoiceId}",
  "contract": "finance",
  "summary": "One tax invoice, with its lines, VAT per rate and credit memos",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [],
  "requestBody": null,
  "responds": "FinTaxInvoice"
 },
 "getVisitReminder": {
  "method": "GET",
  "path": "/orders/{orderId}/reminder",
  "contract": "orders",
  "summary": "The guest's reminder for this booking",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VisitReminder"
 },
 "getWishlist": {
  "method": "GET",
  "path": "/guests/{subjectId}/wishlist",
  "contract": "marketing-crm",
  "summary": "Read a guest's saved items",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
  "parameters": [],
  "requestBody": null,
  "responds": "Wishlist"
 },
 "guestLogout": {
  "method": "DELETE",
  "path": "/auth/guest/session",
  "contract": "identity",
  "summary": "End a guest session",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": "allDevices",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "guestPasswordLogin": {
  "method": "POST",
  "path": "/auth/guest/password",
  "contract": "identity",
  "summary": "Sign in with an email or mobile and a password",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "GuestSession"
 },
 "guestSocialLogin": {
  "method": "POST",
  "path": "/auth/guest/social",
  "contract": "identity",
  "summary": "Sign in with Apple or Google",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "GuestSession"
 },
 "guestUaePassLogin": {
  "method": "POST",
  "path": "/auth/guest/uae-pass",
  "contract": "identity",
  "summary": "Sign in with a national identity provider",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "GuestSession"
 },
 "issueTaxInvoice": {
  "method": "POST",
  "path": "/tax-invoices",
  "contract": "finance",
  "summary": "Issue a tax invoice for one or more paid orders",
  "permission": "LEDGER_POST",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "FinIssueTaxInvoiceRequest",
  "responds": "FinTaxInvoice"
 },
 "issueWalletPass": {
  "method": "POST",
  "path": "/wallet-passes",
  "contract": "orders",
  "summary": "Generate an Apple or Google wallet pass",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WalletPass"
 },
 "linkGuestCheckout": {
  "method": "POST",
  "path": "/auth/guest/link-checkout",
  "contract": "identity",
  "summary": "Attach a guest checkout to an account",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "listCreditMemos": {
  "method": "GET",
  "path": "/credit-memos",
  "contract": "finance",
  "summary": "Credit memos issued, newest first",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "taxInvoiceId",
    "in": "query",
    "required": null
   },
   {
    "name": "refundId",
    "in": "query",
    "required": null
   },
   {
    "name": "legalEntityId",
    "in": "query",
    "required": null
   },
   {
    "name": "issuedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "issuedTo",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "listEntitlements": {
  "method": "GET",
  "path": "/my/entitlements/all",
  "contract": "access",
  "summary": "Every entitlement this guest holds, including expired",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": "includeExpired",
    "in": "query",
    "required": false
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "listMyEntitlements": {
  "method": "GET",
  "path": "/guests/me/entitlements",
  "contract": "access",
  "summary": "Every ticket, pass and membership this guest holds",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": "state",
    "in": "query",
    "required": null
   },
   {
    "name": "includeShared",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "listMyOrders": {
  "method": "GET",
  "path": "/my/orders",
  "contract": "orders",
  "summary": "The orders this guest placed",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": "since",
    "in": "query",
    "required": false
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "listOrders": {
  "method": "GET",
  "path": "/orders",
  "contract": "orders",
  "summary": "List orders",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "shiftId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "createdFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "createdTo",
    "in": "query",
    "required": null
   },
   {
    "name": "workstationId",
    "in": "query",
    "required": null
   },
   {
    "name": "subjectId",
    "in": "query",
    "required": null
   },
   {
    "name": "tender",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "listPublishedTrackingTechnologies": {
  "method": "GET",
  "path": "/storefront/cookie-consent/technologies",
  "contract": "marketing-crm",
  "summary": "The approved cookie registry, as the preference centre shows it",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "channel",
    "in": "query",
    "required": true
   },
   {
    "name": "category",
    "in": "query",
    "required": false
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "listTaxInvoices": {
  "method": "GET",
  "path": "/tax-invoices",
  "contract": "finance",
  "summary": "Tax invoices issued, newest first",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "orderId",
    "in": "query",
    "required": null
   },
   {
    "name": "legalEntityId",
    "in": "query",
    "required": null
   },
   {
    "name": "invoiceType",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "issuedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "issuedTo",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "recordConsent": {
  "method": "POST",
  "path": "/guests/{subjectId}/consents",
  "contract": "marketing-crm",
  "summary": "Record a consent decision",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RecordConsentRequest",
  "responds": "ConsentState"
 },
 "recordDeviceConsent": {
  "method": "POST",
  "path": "/consent/device",
  "contract": "marketing-crm",
  "summary": "Record a visitor's cookie decision, before anyone is known",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RecordDeviceConsentRequest",
  "responds": "DeviceConsent"
 },
 "refreshToken": {
  "method": "POST",
  "path": "/auth/refresh",
  "contract": "identity",
  "summary": "Rotate the access token",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "TokenPair"
 },
 "registerGuest": {
  "method": "POST",
  "path": "/auth/guest/register",
  "contract": "identity",
  "summary": "Create a guest account",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RegisterGuestRequest",
  "responds": "GuestSession"
 },
 "removeFromWishlist": {
  "method": "DELETE",
  "path": "/guests/{subjectId}/wishlist/{itemId}",
  "contract": "marketing-crm",
  "summary": "Remove a saved item",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "requestGuestOtp": {
  "method": "POST",
  "path": "/auth/guest/otp",
  "contract": "identity",
  "summary": "Request a one-time code",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "setVisitReminder": {
  "method": "PUT",
  "path": "/orders/{orderId}/reminder",
  "contract": "orders",
  "summary": "Turn a visit reminder on or off",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "VisitReminder",
  "responds": "VisitReminder"
 },
 "transferOrderTickets": {
  "method": "POST",
  "path": "/orders/{orderId}/transfer",
  "contract": "orders",
  "summary": "Transfer tickets to another guest",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "updateGuestPreferences": {
  "method": "PUT",
  "path": "/guests/{subjectId}/preferences",
  "contract": "marketing-crm",
  "summary": "The things a regular should not have to say twice",
  "permission": "GUEST_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "GuestPreferences",
  "responds": "GuestPreferences"
 },
 "updateMyProfile": {
  "method": "PATCH",
  "path": "/guests/me/profile",
  "contract": "marketing-crm",
  "summary": "A guest correcting their own details",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "GuestProfile"
 },
 "uploadGuestDocument": {
  "method": "POST",
  "path": "/guest-documents",
  "contract": "marketing-crm",
  "summary": "Store a guest photo, ID or signed document",
  "permission": "GUEST_VIEW_PII",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "GuestDocument",
  "responds": "GuestDocument"
 },
 "verifyGuestOtp": {
  "method": "POST",
  "path": "/auth/guest/otp/verify",
  "contract": "identity",
  "summary": "Verify a one-time code and issue a session",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "GuestSession"
 },
 "verifyMfaChallenge": {
  "method": "POST",
  "path": "/auth/mfa/challenge/{challengeId}/verify",
  "contract": "identity",
  "summary": "Complete a sign-in or step-up challenge",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessDeviceBinding": {
  "type": "object",
  "x-ticvai-persistence": "access.device_binding",
  "description": "One guest device bound to a credential, with its registration, last activation and security status; the binding policy in force is a deviceBinding row of access.credential_policy (declared 29 September, data-model close-out DM1). Written by bindCredentialDevice (the guest app) and releaseCredentialDevice; securityStatus is set by the sharing detection job (decided 29 September, writers pass).",
  "required": [
   "id",
   "entitlementId",
   "deviceId",
   "registeredAt",
   "securityStatus",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The guest (pii.subject)"
   },
   "entitlementId": {
    "type": "string",
    "format": "uuid"
   },
   "credentialBindingId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "deviceId": {
    "type": "string",
    "maxLength": 200
   },
   "deviceReference": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "appInstallationId": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "os": {
    "type": "string",
    "maxLength": 50,
    "nullable": true
   },
   "registeredAt": {
    "type": "string",
    "format": "date-time"
   },
   "lastActivatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "lastKnownVenueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "securityStatus": {
    "type": "string",
    "enum": [
     "normal",
     "suspicious",
     "blocked"
    ],
    "default": "normal"
   },
   "deactivatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Set when the binding is removed (deactivation, or a transfer of the credential)"
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "ClaimDeviceConsentRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "consentKey"
  ],
  "properties": {
   "consentKey": {
    "type": "string",
    "maxLength": 64
   }
  }
 },
 "ConsentDecision": {
  "type": "string",
  "enum": [
   "granted",
   "withdrawn",
   "notAsked"
  ]
 },
 "ConsentPurpose": {
  "type": "string",
  "enum": [
   "marketing",
   "personalisation",
   "profiling",
   "thirdPartySharing",
   "aiProcessing",
   "transactional"
  ]
 },
 "ConsentSource": {
  "type": "string",
  "enum": [
   "guestApp",
   "website",
   "kiosk",
   "pos",
   "callCentre",
   "import",
   "agentRecorded",
   "cookieBanner",
   "checkout"
  ],
  "description": "`checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents`, bound to the order and the verified contact. `cookieBanner` (29 September, build; BL-073 §4b): a decision made on the cookie banner or preference centre and moved onto the guest by `claimDeviceConsent`. Kept apart from `website`, a form submission, because the audit trail (2.6.56) has to tell the two apart."
 },
 "ConsentState": {
  "x-ticvai-persistence": "none — projection over consent_record",
  "type": "object",
  "required": [
   "subjectId",
   "purposes"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "purposes": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "purpose",
      "decision",
      "requiresRenewal"
     ],
     "properties": {
      "purpose": {
       "$ref": "#/components/schemas/ConsentPurpose"
      },
      "decision": {
       "$ref": "#/components/schemas/ConsentDecision"
      },
      "channels": {
       "type": "array",
       "items": {
        "$ref": "#/components/schemas/MessageChannel"
       }
      },
      "noticeVersion": {
       "type": "string",
       "nullable": true
      },
      "requiresRenewal": {
       "type": "boolean",
       "description": "True where the notice has been superseded since consent was given."
      },
      "decidedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "CookieBannerPreferenceCenterDesignerView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.cookie_banner_design",
  "description": "One version of a cookie banner and preference-centre design (pack 17.1.6).",
  "required": [
   "channel",
   "position",
   "languages",
   "rejectIsOneClick",
   "categories"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null for the corporate design every brand inherits."
   },
   "inheritsFromId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "channel": {
    "type": "string",
    "enum": [
     "b2cWebsite",
     "customerPortal",
     "mobileApp",
     "embeddedCheckout",
     "whiteLabelSite",
     "partnerMicrosite"
    ]
   },
   "logoAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "body": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "position": {
    "type": "string",
    "enum": [
     "top",
     "bottom",
     "popup",
     "modal"
    ]
   },
   "themeId": {
    "type": "string",
    "nullable": true,
    "description": "The white-label theme it takes colours and fonts from."
   },
   "buttons": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "action"
     ],
     "properties": {
      "action": {
       "type": "string",
       "enum": [
        "acceptAll",
        "rejectNonEssential",
        "managePreferences",
        "savePreferences",
        "doNotSellOrShare"
       ]
      },
      "label": {
       "$ref": "#/components/schemas/LocalisedText"
      }
     }
    }
   },
   "rejectIsOneClick": {
    "type": "boolean",
    "default": true,
    "description": "Must be true."
   },
   "links": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "label",
      "policyKind"
     ],
     "properties": {
      "label": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "policyKind": {
       "type": "string",
       "enum": [
        "privacy",
        "cookie",
        "termsAndConditions"
       ]
      }
     }
    }
   },
   "categories": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "category",
      "defaultOn"
     ],
     "properties": {
      "category": {
       "type": "string",
       "enum": [
        "strictlyNecessary",
        "functional",
        "analytics",
        "personalisation",
        "marketing"
       ]
      },
      "description": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "defaultOn": {
       "type": "boolean",
       "description": "True only for `strictlyNecessary`, which is always active."
      }
     }
    }
   },
   "languages": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string",
     "maxLength": 10
    },
    "description": "Every language the storefront serves; Arabic renders right to left."
   },
   "regulatoryRegimes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "gdpr",
      "ePrivacy",
      "ccpaCpra",
      "lgpd",
      "uaePdpl",
      "saudiPdpl"
     ]
    },
    "description": "2.6.60 (29 September, build). **The laws this design is published to satisfy**, so compliance is stated rather than assumed. The strictest posture (opt-in, one-click reject, every non-essential category off) already meets GDPR/ePrivacy, LGPD and both PDPLs; `ccpaCpra` adds the \"Do not sell or share\" button (`doNotSellOrShare`) and honours a Global Privacy Control signal as that opt-out."
   },
   "recordIpAddress": {
    "type": "boolean",
    "default": false,
    "description": "2.6.55, \"if legally permitted\" (29 September, build). On, `recordDeviceConsent` writes the IP address and user agent to `pii.consent_identifier`; off, they are not kept anywhere. Off by default."
   },
   "noticeVersion": {
    "type": "string",
    "readOnly": true,
    "description": "Moves with the cookie policy (white-label `setPolicy`, kind `cookie`)."
   },
   "version": {
    "type": "integer",
    "minimum": 1,
    "readOnly": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "published",
     "superseded"
    ],
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "CookieCategory": {
  "type": "string",
  "enum": [
   "strictlyNecessary",
   "functional",
   "analytics",
   "personalisation",
   "marketing"
  ],
  "description": "2.6.53. The five categories the banner design (`CookieBannerPreferenceCenterDesignerView.categories`) offers; the matrix's \"preference\" category is `personalisation` (British spelling, as `ConsentPurpose`)."
 },
 "CookieConsentChannel": {
  "type": "string",
  "enum": [
   "b2cWebsite",
   "customerPortal",
   "mobileApp",
   "embeddedCheckout",
   "whiteLabelSite",
   "partnerMicrosite"
  ],
  "description": "The six governed surfaces, as the registry and the banner design name them (pack 17.1.5-17.1.6)."
 },
 "CookieConsentRuntime": {
  "type": "object",
  "x-ticvai-persistence": "none — assembled at read time from marketing.cookie_banner_design, marketing.tracking_technology and marketing.device_consent",
  "description": "What `getCookieConsentRuntime` gives the storefront tag loader and the app SDK gate (2.6.52, 2.6.58).",
  "required": [
   "banner",
   "noticeVersion",
   "requiresDecision",
   "allowedTechnologies",
   "consentModeSignals"
  ],
  "properties": {
   "banner": {
    "$ref": "#/components/schemas/CookieBannerPreferenceCenterDesignerView"
   },
   "noticeVersion": {
    "type": "string"
   },
   "requiresDecision": {
    "type": "boolean",
    "description": "True with no decision, an expired one, or one given against a superseded notice."
   },
   "decision": {
    "allOf": [
     {
      "$ref": "#/components/schemas/DeviceConsent"
     }
    ],
    "nullable": true,
    "description": "The latest decision for the presented key; null without a key."
   },
   "allowedTechnologies": {
    "type": "array",
    "description": "Per category, the approved technologies it unlocks. Anything not listed never loads.",
    "items": {
     "type": "object",
     "required": [
      "category",
      "technologies"
     ],
     "properties": {
      "category": {
       "$ref": "#/components/schemas/CookieCategory"
      },
      "granted": {
       "type": "boolean",
       "description": "Whether the presented decision grants it; always true for `strictlyNecessary`."
      },
      "technologies": {
       "type": "array",
       "items": {
        "type": "object",
        "required": [
         "name",
         "provider"
        ],
        "properties": {
         "name": {
          "type": "string"
         },
         "provider": {
          "type": "string"
         },
         "technologyType": {
          "type": "string"
         }
        }
       }
      }
     }
    }
   },
   "consentModeSignals": {
    "type": "object",
    "description": "**The decision in Google consent-mode terms** (2.6.65), so Analytics and Tag Manager are told, not left to guess. `denied` wherever no decision grants the category.",
    "properties": {
     "adStorage": {
      "type": "string",
      "enum": [
       "granted",
       "denied"
      ]
     },
     "adUserData": {
      "type": "string",
      "enum": [
       "granted",
       "denied"
      ]
     },
     "adPersonalization": {
      "type": "string",
      "enum": [
       "granted",
       "denied"
      ]
     },
     "analyticsStorage": {
      "type": "string",
      "enum": [
       "granted",
       "denied"
      ]
     },
     "functionalityStorage": {
      "type": "string",
      "enum": [
       "granted",
       "denied"
      ]
     },
     "personalizationStorage": {
      "type": "string",
      "enum": [
       "granted",
       "denied"
      ]
     },
     "securityStorage": {
      "type": "string",
      "enum": [
       "granted"
      ]
     }
    }
   }
  }
 },
 "CredentialDeviceBindingInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; written as access.device_binding (declared 29 September, writers pass)",
  "required": [
   "deviceId"
  ],
  "properties": {
   "deviceId": {
    "type": "string",
    "maxLength": 128,
    "description": "The app's stable device identifier"
   },
   "deviceReference": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "appInstallationId": {
    "type": "string",
    "maxLength": 128,
    "nullable": true
   },
   "os": {
    "type": "string",
    "maxLength": 64,
    "nullable": true
   },
   "otp": {
    "type": "string",
    "maxLength": 12,
    "nullable": true,
    "description": "Verified one-time code, where the policy is otpVerificationRequired and this is a device change"
   }
  }
 },
 "DeviceConsent": {
  "type": "object",
  "x-ticvai-persistence": "marketing.device_consent + marketing.device_consent_category",
  "description": "**One cookie decision by a visitor nobody has identified yet** (BL-073 §4b, decided 29 September). Append-only: a change of mind is a new row. Keyed for the visitor by `consentKey`, which the platform mints; the categories are child rows. The IP address and user agent, where recorded at all, are in `pii.consent_identifier` (`ConsentCaptureIdentifier`), never here.",
  "required": [
   "consentKey",
   "channel",
   "action",
   "categories",
   "noticeVersion",
   "decidedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "consentKey": {
    "type": "string",
    "maxLength": 64,
    "readOnly": true,
    "description": "**Opaque, minted by us, not a device fingerprint.** It answers 2.6.55's \"user identifier/session ID\" and is the join key `claimDeviceConsent` needs. Shared by all the tenant's domains (2.6.62), never across tenants."
   },
   "channel": {
    "$ref": "#/components/schemas/CookieConsentChannel"
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "bannerDesignId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The published `CookieBannerPreferenceCenterDesignerView` version the visitor was shown."
   },
   "action": {
    "$ref": "#/components/schemas/DeviceConsentAction"
   },
   "categories": {
    "type": "array",
    "minItems": 1,
    "description": "Every category of the design, with the decision this row gives it.",
    "items": {
     "type": "object",
     "required": [
      "category",
      "decision"
     ],
     "properties": {
      "category": {
       "$ref": "#/components/schemas/CookieCategory"
      },
      "decision": {
       "type": "string",
       "enum": [
        "granted",
        "declined"
       ]
      }
     }
    }
   },
   "noticeVersion": {
    "type": "string",
    "description": "The cookie notice version decided against (white-label `setPolicy`, kind `cookie`)."
   },
   "language": {
    "type": "string",
    "maxLength": 10,
    "nullable": true
   },
   "globalPrivacyControl": {
    "type": "boolean",
    "default": false,
    "description": "The browser sent a Global Privacy Control signal; honoured as a CCPA/CPRA opt-out of sale and sharing."
   },
   "source": {
    "$ref": "#/components/schemas/ConsentSource"
   },
   "country": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "nullable": true,
    "readOnly": true,
    "description": "The edge's geolocation of the request, for the geographic statistics (2.6.63). The address is not kept here."
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "**A device consent expires and a subject consent does not.** Set from the tenant's device-consent term; after it the banner asks again."
   },
   "claimedBySubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "Set once, by `claimDeviceConsent`. Never cleared."
   },
   "claimedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005), tenant-scoped: a decision with no subject still belongs to one tenant."
   }
  }
 },
 "DeviceConsentAction": {
  "type": "string",
  "enum": [
   "acceptAll",
   "rejectNonEssential",
   "savePreferences",
   "withdraw",
   "doNotSellOrShare"
  ],
  "description": "What the visitor pressed. `doNotSellOrShare` is the CCPA/CPRA opt-out link, shown where the design's `regulatoryRegimes` include `ccpaCpra`."
 },
 "Entitlement": {
  "type": "object",
  "x-ticvai-persistence": "access.entitlement",
  "description": "**What a guest actually holds.** Found missing on 18 August by the schema audit — 33 tables in `orders`, seven in `access`, and none of them stored an issued ticket.\nThe package sold products, defined `EntitlementTemplate`, recorded `ScanEvent.ticketId`, transferred `ticket_transfer.ticketIds` and issued `wallet_pass.entitlementId` — **five artefacts referring to a thing that did not exist.** `validateAccess` read the *template* and never the instance, and `suspendEntitlement` suspended the template, **which would have suspended it for every guest who held one.**\n**The template is the definition and this is the instance.** A template says *an annual pass admits once a day for a year*; this says *this guest's annual pass, bought on 3 March, used eleven times, frozen for two weeks in July, valid until 2 March.*\n",
  "required": [
   "id",
   "templateId",
   "productId",
   "orderId",
   "subjectId",
   "status",
   "validFrom",
   "validTo"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "A UUIDv7, matching `TicketStatus.ticketId` — **stable for the life of the ticket and independent of the media carrying it.** A guest whose wristband broke keeps the same entitlement with a new `mediaCode`.\n**This is the ticket id.** Wherever an operation takes a `ticketId` or `ticketIds` — `lookupTicket`, `listScans`, `ScanEvent`, the offline package and `transferOrderTickets` — it is this value. An order line's `entitlementIds` are the ticket ids of that line.\n"
   },
   "templateId": {
    "type": "string",
    "format": "uuid",
    "description": "The definition it was issued against. **Pinned at issue** — a template edited next month must not change what this guest bought.\n"
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "description": "The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`)."
   },
   "orderLineId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Who holds it. **Null is legitimate** — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is claimed.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "mediaCode": {
    "type": "string",
    "description": "What is scanned — a QR payload, a wristband serial, a card number. **Rotatable without reissuing**, because a guest whose wristband broke should not need a new ticket.\n"
   },
   "status": {
    "$ref": "../spine/orders.yaml#/components/schemas/EntitlementStatus"
   },
   "statusNote": {
    "type": "string",
    "nullable": true,
    "description": "**Not `TicketStatus` — that is a validation result with a misleading name**, computed at scan time and carrying `isValid` and `isInsideVenue`. The lifecycle is `orders.EntitlementStatus`, and `states/entitlement-status.yaml` has modelled it since before this table existed.\n**Which is the finding in one line: the package had the lifecycle, the state model and the validation result, and no row to hang them on.**\n"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "description": "**Resolved at issue from the template, then owned here.** A freeze extends it, a reissue replaces it, and neither reaches back to the template.\n**What the pre-expiry notice is measured from** (29 September, build pass, group G2; 5.5.30). A daily run in access publishes `entitlement.expiringSoon` once per entitlement and `validTo` when an entitlement in `issued` or `partiallyConsumed` comes within its template's `expiryNoticeDays` (`catalogue.EntitlementTemplate`), and not for one bought inside that window. Marketing turns it into the reminder (a `MessageTrigger` on the event, or a triggered campaign on `entitlementExpiring`); access only says the date is near. A freeze or renewal that moves `validTo` raises the next notice once.\n"
   },
   "entriesUsed": {
    "type": "integer",
    "default": 0,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "**The number `validateAccess` decrements and nothing was decrementing.** A ten-entry pass with no counter is a ten-entry pass that admits forever.\n**Maintained on write**, in the same transaction as the admitting `access.scan_event` row: by `validateAccess`, `validateGroupAccess` (by the count admitted) and `syncScans` for each replayed admission the server accepts. A replayed scan the server downgrades to `denied` does not count.\n"
   },
   "entriesAllowed": {
    "type": "integer",
    "nullable": true
   },
   "lastEntryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "`recordedAt` of the latest admission counted in `entriesUsed`, written by the same writes. A scan replayed late with an earlier `recordedAt` does not move it back.\n"
   },
   "frozenDays": {
    "type": "integer",
    "default": 0,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Days added by a freeze. **Maintained on write** by the freeze operation (`freezeEntitlement`), in the same write that extends `validTo` by those days. **Held here rather than computed from a freeze log**, because a gate has to answer in under 300ms and cannot replay a history to decide validity.\n"
   },
   "suspendedReason": {
    "type": "string",
    "nullable": true
   },
   "freezeReason": {
    "type": "string",
    "nullable": true,
    "enum": [
     "travelling",
     "injury",
     "personal",
     "seasonal",
     "other"
    ],
    "description": "The `reason` of the latest `freezeEntitlement` (audit R222). Null when never frozen."
   },
   "freezeNote": {
    "type": "string",
    "nullable": true,
    "maxLength": 500,
    "description": "The `note` the latest `freezeEntitlement` took, required there when `reason` is `other` (decided 28 September, audit R222). Kept so the quarterly review of `other` notes has something to read."
   },
   "isNameBound": {
    "type": "boolean",
    "default": false
   },
   "holderName": {
    "type": "string",
    "nullable": true
   },
   "sharedWithSubjectIds": {
    "type": "array",
    "description": "`shareEntitlement`. **The owner keeps it and a second person may present it** — the asymmetry that stops a shared family pass becoming a resale chain.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "issuedVia": {
    "type": "string",
    "enum": [
     "sale",
     "invitation",
     "reissue",
     "transfer",
     "resale",
     "membership",
     "groupBooking"
    ],
    "description": "**How it came to exist, and it matters to finance.** A sold entitlement carries deferred revenue; an invitation carries a marketing cost; a reissue carries neither.\n"
   },
   "supersedesEntitlementId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a reissue or a resale. **The chain is traceable** — a ticket appearing from nowhere is indistinguishable from a fraudulent one.\n"
   },
   "walletValueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the template carries stored value. **A `retail.Wallet` bound to the entitlement, not a balance on it** (CF-126).\n"
   },
   "facePassEnrolmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "x-ticvai-derived": "onRead",
    "description": "The active `facePass` enrolment on this entitlement (`FacePassEnrolment.id`), or null when none is. **Computed on read from `pii.subject_biometric` and not stored here** — the PII split keeps the biometric on its own side, and this carries only its id. It is how a screen holding a pass finds the enrolment `getFacePassEnrolment` and `revokeFacePass` take.\n"
   }
  }
 },
 "FinCreditMemo": {
  "x-ticvai-persistence": "ledger.credit_memo + ledger.credit_memo_line",
  "type": "object",
  "description": "5.7.94. **A tax credit note against one tax invoice**, with its own series. Never edited.",
  "required": [
   "id",
   "creditMemoNumber",
   "taxInvoiceId",
   "kind",
   "reason",
   "legalEntityId",
   "issuedAt",
   "currency",
   "netAmount",
   "taxAmount",
   "grossAmount",
   "lines"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "creditMemoNumber": {
    "type": "string",
    "readOnly": true,
    "description": "Server-assigned from the legal entity's credit memo series, in sequence without gaps."
   },
   "taxInvoiceId": {
    "type": "string",
    "format": "uuid"
   },
   "taxInvoiceNumber": {
    "type": "string",
    "readOnly": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "full",
     "partial"
    ]
   },
   "reason": {
    "type": "string",
    "enum": [
     "refund",
     "cancellation",
     "priceAdjustment",
     "returnOfGoods",
     "billingError",
     "other"
    ]
   },
   "refundId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "cancelledOrderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "buyerSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmountInLegalCurrency": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "renditionAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "eInvoiceStatus": {
    "$ref": "#/components/schemas/FinEInvoiceTransmissionStatus"
   },
   "issuedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/FinCreditMemoLine"
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true
   }
  }
 },
 "FinCreditMemoLine": {
  "type": "object",
  "required": [
   "invoiceLineNumber",
   "netAmount",
   "taxAmount",
   "grossAmount"
  ],
  "properties": {
   "invoiceLineNumber": {
    "type": "integer",
    "minimum": 1
   },
   "description": {
    "type": "string",
    "maxLength": 500
   },
   "quantity": {
    "type": "number",
    "nullable": true
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxRate": {
    "type": "number"
   },
   "taxCategory": {
    "$ref": "#/components/schemas/FinTaxCategory"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "FinEInvoiceTransmissionStatus": {
  "type": "string",
  "description": "6.1.1. `notRequired` where the legal entity's provider is `disabled` or absent.",
  "enum": [
   "notRequired",
   "queued",
   "sent",
   "accepted",
   "rejected",
   "failed"
  ]
 },
 "FinIssueTaxInvoiceRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "invoiceType",
   "orderIds"
  ],
  "properties": {
   "invoiceType": {
    "$ref": "#/components/schemas/FinTaxInvoiceType"
   },
   "orderIds": {
    "type": "array",
    "minItems": 1,
    "description": "One order for `simplified` and `full`; one or more for `consolidated`. Every order must be paid, of one buyer, one legal entity and one currency.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "recipient": {
    "$ref": "#/components/schemas/FinTaxInvoiceRecipient"
   },
   "languages": {
    "type": "array",
    "description": "Overrides the template's languages for this document, within those the template offers.",
    "items": {
     "type": "string",
     "pattern": "^[a-z]{2}(-[A-Z]{2})?$"
    }
   },
   "supersedesInvoiceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A simplified invoice this full invoice replaces for the same supply. Refused unless the law allows it (make-or-break on issueTaxInvoice)."
   },
   "deliverToEmail": {
    "type": "string",
    "format": "email",
    "nullable": true,
    "description": "Sends the PDF on issue as well as returning it."
   }
  }
 },
 "FinTaxCategory": {
  "type": "string",
  "description": "How a line is treated for VAT. Taken from the tax code the line was posted with.",
  "enum": [
   "standardRated",
   "zeroRated",
   "exempt",
   "outOfScope",
   "reverseCharge"
  ]
 },
 "FinTaxDocumentRendition": {
  "x-ticvai-persistence": "none — a signed link to the stored PDF",
  "type": "object",
  "required": [
   "documentId",
   "documentKind",
   "url",
   "expiresAt"
  ],
  "properties": {
   "documentId": {
    "type": "string",
    "format": "uuid"
   },
   "documentKind": {
    "type": "string",
    "enum": [
     "taxInvoice",
     "creditMemo"
    ]
   },
   "documentNumber": {
    "type": "string"
   },
   "language": {
    "type": "string",
    "nullable": true
   },
   "contentType": {
    "type": "string",
    "default": "application/pdf"
   },
   "url": {
    "type": "string",
    "format": "uri"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "FinTaxInvoice": {
  "x-ticvai-persistence": "ledger.tax_invoice + ledger.tax_invoice_line",
  "type": "object",
  "description": "5.7.93, 5.10.3. **A guest tax invoice, as issued, never edited.** Corrections are credit memos. The supplier block is a snapshot of the legal entity at issue, so a later change of address does not change a document already given to a guest.",
  "required": [
   "id",
   "invoiceNumber",
   "invoiceType",
   "status",
   "legalEntityId",
   "issuedAt",
   "supplyDate",
   "currency",
   "netAmount",
   "taxAmount",
   "grossAmount",
   "lines"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "invoiceNumber": {
    "type": "string",
    "readOnly": true,
    "description": "Server-assigned from the legal entity's series for the document kind, in sequence and without gaps, e.g. `INV-2026-000123`. Never reused."
   },
   "invoiceType": {
    "$ref": "#/components/schemas/FinTaxInvoiceType"
   },
   "status": {
    "$ref": "#/components/schemas/FinTaxInvoiceStatus"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "templateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "supplierName": {
    "type": "string"
   },
   "supplierAddress": {
    "type": "string",
    "nullable": true
   },
   "supplierTaxRegistrationNumber": {
    "type": "string",
    "nullable": true
   },
   "buyerSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The guest the orders belong to; the key a guest's own reads filter on."
   },
   "buyerName": {
    "type": "string",
    "nullable": true
   },
   "buyerAddress": {
    "type": "string",
    "nullable": true
   },
   "buyerCountryCode": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "nullable": true
   },
   "buyerTaxRegistrationNumber": {
    "type": "string",
    "nullable": true
   },
   "customerAccountId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "supplyDate": {
    "type": "string",
    "format": "date",
    "description": "The date of supply where it differs from the issue date (the latest order's payment date on a consolidated invoice). A day in the region's time zone."
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmountInLegalCurrency": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "The tax in the legal entity's currency (AED in the UAE) where the invoice currency differs, at the rate the orders were stored at."
   },
   "creditedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "languages": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "supersedesInvoiceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "renditionAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The PDF rendered at issue; read through getTaxDocumentRendition."
   },
   "eInvoiceStatus": {
    "$ref": "#/components/schemas/FinEInvoiceTransmissionStatus"
   },
   "issuedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "Null where the platform issued it."
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/FinTaxInvoiceLine"
    }
   },
   "taxSummary": {
    "type": "array",
    "x-ticvai-persisted": false,
    "description": "VAT per rate and category, summed from the lines for the response.",
    "items": {
     "type": "object",
     "properties": {
      "taxCategory": {
       "$ref": "#/components/schemas/FinTaxCategory"
      },
      "taxRate": {
       "type": "number"
      },
      "taxableAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "taxAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Written at the scope of the venue the orders were sold at, or the region for a consolidated invoice across venues."
   }
  }
 },
 "FinTaxInvoiceLine": {
  "type": "object",
  "description": "One line as it was sold and taxed. Amounts are in the invoice currency.",
  "required": [
   "lineNumber",
   "description",
   "quantity",
   "netAmount",
   "taxAmount",
   "grossAmount",
   "taxCategory"
  ],
  "properties": {
   "lineNumber": {
    "type": "integer",
    "minimum": 1
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "orderLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "description": {
    "type": "string",
    "maxLength": 500
   },
   "quantity": {
    "type": "number"
   },
   "unitPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxCodeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "taxRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "taxCategory": {
    "$ref": "#/components/schemas/FinTaxCategory"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "creditedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "FinTaxInvoiceRecipient": {
  "x-ticvai-persistence": "none — copied onto the invoice as buyer columns",
  "type": "object",
  "description": "Who the invoice is addressed to. Required for `full` and `consolidated`.",
  "required": [
   "name"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 300
   },
   "address": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "countryCode": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "nullable": true
   },
   "taxRegistrationNumber": {
    "type": "string",
    "maxLength": 30,
    "nullable": true,
    "description": "The recipient's TRN where they are VAT-registered."
   },
   "customerAccountId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The B2B credit account (payments `B2bCreditAccount`) where a company is invoiced."
   }
  }
 },
 "FinTaxInvoiceStatus": {
  "type": "string",
  "description": "`issued` until a credit memo is issued against it; `superseded` where a full invoice replaced a simplified one for the same supply (only if the law allows it; see issueTaxInvoice).",
  "enum": [
   "issued",
   "partiallyCredited",
   "fullyCredited",
   "superseded"
  ]
 },
 "FinTaxInvoiceType": {
  "type": "string",
  "description": "5.7.93. `simplified` for one order with no recipient details, `full` for one order with them, `consolidated` for several paid orders of one buyer on one invoice.",
  "enum": [
   "simplified",
   "full",
   "consolidated"
  ]
 },
 "GuestDocument": {
  "type": "object",
  "x-ticvai-persistence": "marketing.guest_document",
  "description": "BL-133. **No store for guest photos, avatars, IDs or signed documents anywhere.**\nDeliberately separate from `assets`, which holds a tenant's media library. **A guest's passport scan is not a marketing asset** — it has a different retention clock, a different access rule and a different reason to exist, and putting it in the same store means one careless query returns both.\n",
  "required": [
   "id",
   "subjectId",
   "kind",
   "storageRef",
   "retainUntil"
  ],
  "properties": {
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "avatar",
     "idDocument",
     "visa",
     "signedWaiver",
     "medicalNote",
     "accessibilityEvidence",
     "photo",
     "other"
    ]
   },
   "storageRef": {
    "type": "string",
    "description": "**The stored object's key in the guest-document store**, which is deliberately not `assets` (BL-133). No operation in this contract issues one yet: `assets` `createUpload` is staff-only and writes the media library, so the upload step for this store is still to be designed.\n"
   },
   "contentType": {
    "type": "string"
   },
   "consentPurposeId": {
    "type": "string",
    "format": "uuid"
   },
   "retainUntil": {
    "type": "string",
    "format": "date",
    "description": "**Required, not optional.** A guest document with no deletion date is a guest document kept forever, and the retention question is the one CF-64 is open on.\n**Kept until its purpose ends, then for the period client counsel sets (decided 28 September, audit R149).** The caller sets `retainUntil` to the end of the purpose (the visit, the waiver's validity, the visa's expiry) plus that period. **The period per `kind` is an open value**: until counsel names it, it is zero, so the document is deleted when the purpose ends.\n"
   },
   "uploadedAt": {
    "readOnly": true,
    "type": "string",
    "format": "date-time"
   },
   "uploadedByPrincipalId": {
    "readOnly": true,
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "GuestPreferences": {
  "type": "object",
  "x-ticvai-persistence": "marketing.guest_preference",
  "description": "**What the guest likes, kept apart from what they permit** (consent) and from who they are (the profile). One row per subject. `dietary` and `accessibility` are here rather than as tags because BL-134 gives them their own consent purpose and retention.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "seatingPreference": {
    "type": "string",
    "nullable": true,
    "maxLength": 200
   },
   "drinkPreferences": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "dietary": {
    "type": "array",
    "description": "Also written by `updateMyProfile`.",
    "items": {
     "type": "string"
    }
   },
   "accessibility": {
    "type": "array",
    "description": "Also written by `updateMyProfile`.",
    "items": {
     "type": "string"
    }
   },
   "preferredChannel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MessageChannel"
     }
    ],
    "x-ticvai-persisted": false,
    "description": "**Stored on the profile** (`GuestProfile.preferredChannel`) — carried here because the preference screen edits it beside the rest.\n"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "GuestProfile": {
  "x-ticvai-persistence": "marketing.guest_profile",
  "type": "object",
  "required": [
   "subjectId",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "description": "Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger.\n"
   },
   "displayName": {
    "type": "string",
    "nullable": true
   },
   "email": {
    "type": "string",
    "nullable": true
   },
   "phone": {
    "type": "string",
    "nullable": true
   },
   "preferredLanguage": {
    "type": "string",
    "nullable": true
   },
   "preferredChannel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Present where the guest is linked across cells. Marketing acts locally."
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "engagementScore": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 100,
    "description": "22.2.20 and 22.2.21. **`lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not.** They are different questions: a guest who spent a lot once and a guest who visits monthly have the same LTV and need opposite treatment.\n**Recency, frequency and breadth, not spend** — spend is already `lifetimeValue`, and folding it in here would make one number twice.\n"
   },
   "engagementTier": {
    "type": "string",
    "nullable": true,
    "enum": [
     "new",
     "active",
     "occasional",
     "lapsing",
     "lapsed",
     "dormant"
    ],
    "description": "5.3.19. **Automatic classification, computed rather than assigned.** `lapsing` is the tier the whole field exists for — **a guest who has not been for a while and still might is the only one marketing can change**, and lumping them with `lapsed` wastes the window.\n"
   },
   "lifetimeValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "visitCount": {
    "type": "integer"
   },
   "lastVisitAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   },
   "mergedIntoSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "**Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`**, which retain it as a redirect rather than deleting it. A read that lands here follows it; a second merge of a profile that has one is refused as `alreadyMerged`.\n"
   },
   "mergedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "GuestSession": {
  "x-ticvai-persistence": "none — Redis session registry",
  "type": "object",
  "required": [
   "subjectId",
   "tokens",
   "isVerified",
   "expiresAt"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string",
    "nullable": true
   },
   "tokens": {
    "$ref": "#/components/schemas/TokenPair"
   },
   "isVerified": {
    "type": "boolean",
    "description": "False until an OTP or a verified provider identity confirms ownership. An unverified account may browse and fill a cart but not transact: the gate is the checkout page (ADR-0045), where `checkoutCart` refuses it until the guest verifies or proves the contact by code. UAE Pass returns a verified identity, so it starts true. Rule on `verifyGuestEmail`, decided 17 September 2026.\n"
   },
   "identityProviders": {
    "type": "array",
    "description": "Linked providers. Several may resolve to one account.",
    "items": {
     "type": "string",
     "enum": [
      "password",
      "otp",
      "apple",
      "google",
      "uaePass"
     ]
    }
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Present where the guest is linked across cells (ADR-0010)."
   },
   "requiresMfa": {
    "type": "boolean",
    "default": false,
    "description": "True only where the sign-in venue enabled guest two-step verification (`VenueSettings.identity.guestTwoStep`, in tenancy) and this guest has an active method (decided 29 September, rev 3 GAP-B1, per venue). The session is then not usable until `verifyMfaChallenge` succeeds on a `signIn` challenge. Always false for a UAE Pass sign-in, which is already a verified two-factor identity (proposed, client to correct).\n"
   },
   "mfaMethods": {
    "type": "array",
    "description": "The guest's active methods, so the client can offer the right one. Empty when `requiresMfa` is false.",
    "items": {
     "$ref": "#/components/schemas/MfaMethod"
    }
   },
   "homeCellName": {
    "type": "string",
    "nullable": true
   },
   "preferredLanguage": {
    "type": "string",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "**30 days, sliding** (decided 28 September, audit R126 (2)): each use of the session moves this to 30 days from now, and 30 days unused ends it. **One session per device**: a guest may be signed in on a phone and a laptop at once, and a new sign-in on the same `deviceId` ends that device's previous session.\n"
   }
  }
 },
 "MessageChannel": {
  "type": "string",
  "enum": [
   "email",
   "sms",
   "whatsapp",
   "push",
   "inApp",
   "post"
  ]
 },
 "MfaMethod": {
  "x-ticvai-persistence": "identity.mfa_method",
  "type": "object",
  "required": [
   "id",
   "kind",
   "isActive",
   "enrolledAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/MfaKind"
   },
   "label": {
    "type": "string",
    "nullable": true
   },
   "maskedTarget": {
    "type": "string",
    "nullable": true,
    "description": "Partially masked destination, so a person can tell two methods apart."
   },
   "isActive": {
    "type": "boolean"
   },
   "isPrimary": {
    "type": "boolean"
   },
   "enrolledAt": {
    "type": "string",
    "format": "date-time"
   },
   "lastUsedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "Order": {
  "x-ticvai-persistence": "orders.sales_order + orders.order_line",
  "type": "object",
  "required": [
   "id",
   "venueId",
   "scopePath",
   "channel",
   "status",
   "currency",
   "currencyScale",
   "grossAmount",
   "taxAmount",
   "netAmount",
   "lines",
   "createdAt",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "The client UUIDv7 from `CreateOrderRequest.id`."
   },
   "orderNumber": {
    "type": "string",
    "readOnly": true,
    "description": "The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/OrderChannel"
     }
    ],
    "description": "Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/OrderStatus"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "droppedPromotions": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n",
    "items": {
     "type": "object",
     "required": [
      "promotionId"
     ],
     "properties": {
      "promotionId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "reason": {
       "type": "string",
       "enum": [
        "budgetCapReached"
       ]
      }
     }
    }
   },
   "totalPriceVariance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Sum across lines. Zero on a normal order."
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/OrderLine"
    }
   },
   "payments": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Payment"
    }
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "shiftId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "holdLabel": {
    "type": "string",
    "maxLength": 60,
    "nullable": true,
    "readOnly": true,
    "description": "The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."
   },
   "heldUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "OrderChannel": {
  "type": "string",
  "description": "Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n",
  "enum": [
   "pos",
   "kiosk",
   "guestApp",
   "guestWeb",
   "callCentre",
   "partner",
   "api",
   "backOffice"
  ]
 },
 "OrderLine": {
  "x-ticvai-persistence": "orders.order_line + orders.order_line_eligibility + orders.order_line_discount",
  "x-ticvai-retired-columns": [
   "promotion_id",
   "name",
   "reason"
  ],
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateOrderLine"
   },
   {
    "type": "object",
    "required": [
     "serverUnitPrice",
     "taxAmount",
     "netAmount",
     "grossAmount"
    ],
    "properties": {
     "serverUnitPrice": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "What the server computed on ingest."
     },
     "priceVariance": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"
     },
     "taxAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "netAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "grossAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "entitlementIds": {
      "type": "array",
      "description": "The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "crossRegionRightIds": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Redemption rights propagated to other cells for this line."
     },
     "reprintCount": {
      "type": "integer",
      "minimum": 0,
      "default": 0,
      "readOnly": true,
      "description": "How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."
     },
     "venueId": {
      "type": "string",
      "format": "uuid",
      "readOnly": true,
      "description": "The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."
     },
     "discounts": {
      "type": "array",
      "readOnly": true,
      "description": "**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.",
      "items": {
       "$ref": "#/components/schemas/OrderLineDiscount"
      }
     }
    }
   }
  ]
 },
 "OrderStatus": {
  "type": "string",
  "enum": [
   "pending",
   "held",
   "paid",
   "partiallyPaid",
   "completed",
   "voided",
   "refunded",
   "partiallyRefunded",
   "failed"
  ],
  "description": "`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"
 },
 "OrderSummary": {
  "x-ticvai-persistence": "none — projection",
  "type": "object",
  "required": [
   "id",
   "orderNumber",
   "status",
   "grossAmount",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "orderNumber": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/OrderStatus"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/OrderChannel"
     }
    ],
    "description": "The same vocabulary as `Order.channel`, which this projects."
   },
   "lineCount": {
    "type": "integer"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "description": "The cashier who raised it — what the held-orders list shows."
   },
   "holdLabel": {
    "type": "string",
    "nullable": true,
    "description": "As `Order.holdLabel`."
   },
   "heldUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "Page": {
  "type": "object",
  "required": [
   "items",
   "hasMore"
  ],
  "properties": {
   "items": {
    "type": "array",
    "items": {}
   },
   "nextCursor": {
    "type": "string"
   },
   "hasMore": {
    "type": "boolean"
   }
  }
 },
 "Payment": {
  "x-ticvai-persistence": "orders.payment",
  "type": "object",
  "required": [
   "id",
   "orderId",
   "tender",
   "amount",
   "status",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "tender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "tenderCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"
   },
   "tenderAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "The amount in `tenderCurrency`, at that currency's own scale."
   },
   "fxRate": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ExchangeRateDecimal"
     }
    ],
    "nullable": true,
    "description": "The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"
   },
   "fxRateSource": {
    "type": "string",
    "nullable": true,
    "enum": [
     "manual",
     "feed",
     "cardScheme"
    ],
    "description": "4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"
   },
   "changeCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "description": "4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "changeAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "authorised",
     "captured",
     "pendingConfirmation",
     "declined",
     "failed",
     "voided",
     "refunded"
    ]
   },
   "providerName": {
    "type": "string",
    "nullable": true
   },
   "providerReference": {
    "type": "string",
    "nullable": true,
    "description": "The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."
   },
   "providerIdempotencyKey": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."
   },
   "terminalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The card terminal a till payment ran on (ECR flow, SD-034)."
   },
   "nextAction": {
    "type": "object",
    "nullable": true,
    "x-ticvai-persisted": false,
    "description": "**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.",
    "properties": {
     "kind": {
      "type": "string",
      "enum": [
       "redirect",
       "terminal"
      ]
     },
     "url": {
      "type": "string",
      "format": "uri",
      "nullable": true
     },
     "expiresAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
   },
   "lastInquiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "PublishedTrackingTechnology": {
  "type": "object",
  "x-ticvai-persistence": "none — the approved rows of marketing.tracking_technology, guest-facing fields only",
  "description": "One approved technology as the preference centre shows it (2.6.54).",
  "required": [
   "name",
   "provider",
   "category",
   "isThirdParty"
  ],
  "properties": {
   "name": {
    "type": "string"
   },
   "provider": {
    "type": "string"
   },
   "category": {
    "$ref": "#/components/schemas/CookieCategory"
   },
   "technologyType": {
    "type": "string"
   },
   "purpose": {
    "type": "string",
    "nullable": true
   },
   "durationDays": {
    "type": "integer",
    "nullable": true,
    "description": "Null for session storage."
   },
   "isThirdParty": {
    "type": "boolean"
   },
   "privacyInformation": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "RecordConsentRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "purpose",
   "decision",
   "noticeVersion",
   "source",
   "recordedAt"
  ],
  "properties": {
   "purpose": {
    "$ref": "#/components/schemas/ConsentPurpose"
   },
   "decision": {
    "$ref": "#/components/schemas/ConsentDecision"
   },
   "channels": {
    "type": "array",
    "description": "Omit to apply to every channel the purpose covers.",
    "items": {
     "$ref": "#/components/schemas/MessageChannel"
    }
   },
   "noticeVersion": {
    "type": "string"
   },
   "source": {
    "$ref": "#/components/schemas/ConsentSource"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "RecordDeviceConsentRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What the banner or preference centre sends to `recordDeviceConsent`.",
  "required": [
   "channel",
   "action",
   "noticeVersion",
   "decidedAt"
  ],
  "properties": {
   "consentKey": {
    "type": "string",
    "maxLength": 64,
    "nullable": true,
    "description": "The key the browser or app already holds; omitted on a first decision, and one is minted."
   },
   "channel": {
    "$ref": "#/components/schemas/CookieConsentChannel"
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "bannerDesignId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "action": {
    "$ref": "#/components/schemas/DeviceConsentAction"
   },
   "categories": {
    "type": "array",
    "description": "Required for `savePreferences`; ignored for the other actions, which decide every category themselves.",
    "items": {
     "type": "object",
     "required": [
      "category",
      "decision"
     ],
     "properties": {
      "category": {
       "$ref": "#/components/schemas/CookieCategory"
      },
      "decision": {
       "type": "string",
       "enum": [
        "granted",
        "declined"
       ]
      }
     }
    }
   },
   "noticeVersion": {
    "type": "string"
   },
   "language": {
    "type": "string",
    "maxLength": 10,
    "nullable": true
   },
   "globalPrivacyControl": {
    "type": "boolean",
    "default": false
   },
   "source": {
    "$ref": "#/components/schemas/ConsentSource"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "RegisterGuestRequest": {
  "type": "object",
  "required": [
   "identifier",
   "channel"
  ],
  "properties": {
   "identifier": {
    "type": "string",
    "maxLength": 256,
    "description": "Email address or mobile number in E.164."
   },
   "channel": {
    "type": "string",
    "enum": [
     "email",
     "sms",
     "whatsapp"
    ]
   },
   "displayName": {
    "type": "string",
    "maxLength": 200
   },
   "password": {
    "type": "string",
    "minLength": 8,
    "maxLength": 256,
    "writeOnly": true,
    "description": "Optional. OTP-only accounts are supported and are the default."
   },
   "preferredLanguage": {
    "type": "string",
    "pattern": "^[a-z]{2}$"
   },
   "consents": {
    "type": "array",
    "description": "Consent captured at registration, recorded with the notice version.",
    "items": {
     "type": "object",
     "properties": {
      "purpose": {
       "type": "string"
      },
      "granted": {
       "type": "boolean"
      },
      "noticeVersion": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "Session": {
  "type": "object",
  "required": [
   "sessionId",
   "principalId",
   "roleId",
   "scope",
   "effectivePermissions",
   "saleBoardId"
  ],
  "properties": {
   "sessionId": {
    "type": "string",
    "format": "uuid"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "roleId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string"
   },
   "scope": {
    "type": "array",
    "description": "Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/ScopeRef"
    }
   },
   "effectivePermissions": {
    "allOf": [
     {
      "$ref": "../shared/permissions.yaml#/components/schemas/PermissionSet"
     }
    ],
    "description": "Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"
   },
   "permissionsByScope": {
    "type": "array",
    "description": "Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n",
    "items": {
     "$ref": "../shared/permissions.yaml#/components/schemas/ScopedPermissions"
    }
   },
   "saleBoardId": {
    "type": "string",
    "format": "uuid",
    "description": "Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n"
   },
   "workstation": {
    "$ref": "#/components/schemas/WorkstationContext"
   },
   "openedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "TokenPair": {
  "x-ticvai-persistence": "none — transient",
  "type": "object",
  "required": [
   "accessToken",
   "refreshToken",
   "expiresIn"
  ],
  "properties": {
   "accessToken": {
    "type": "string",
    "description": "JWT carrying `sid`, validated per request against the session registry."
   },
   "refreshToken": {
    "type": "string"
   },
   "expiresIn": {
    "type": "integer",
    "description": "Seconds"
   }
  }
 },
 "VisitReminder": {
  "type": "object",
  "x-ticvai-persistence": "orders.visit_reminder",
  "description": "**One reminder per booking, set by the guest.** Not a marketing message: it is sent only for a booking the guest holds, and only on channels they still consent to.\n**One per booking per guest** (decided 28 September, audit R123 (8)): unique on `orderId` and `subjectId`. Two guests sharing a booking each keep their own reminder, and `setVisitReminder` replaces the caller's own rather than adding a second.\n",
  "required": [
   "enabled"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The guest who set it. A booking shared with others reminds only the guest who asked."
   },
   "enabled": {
    "type": "boolean"
   },
   "leadTimeMinutes": {
    "type": "integer",
    "minimum": 15,
    "maximum": 10080,
    "default": 1440,
    "description": "How long before each session starts. A day by default; a week at most."
   },
   "channels": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "push",
      "email",
      "sms"
     ]
    },
    "default": [
     "push"
    ]
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   }
  }
 },
 "WalletPass": {
  "type": "object",
  "x-ticvai-persistence": "orders.wallet_pass",
  "description": "BL-029. **`appleWallet` and `googlePay` are feature toggles on the native apps** — there is no pass generation, no update push, no serial and no authentication token.\n**A wallet pass is a live object, not a download.** The value over a PDF is that it updates: a changed gate, a cancelled performance, a time that moved. **A pass that cannot be pushed to is a screenshot with better rounding.**\n",
  "required": [
   "id",
   "entitlementId",
   "platform",
   "serialNumber",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "entitlementId": {
    "type": "string",
    "format": "uuid"
   },
   "platform": {
    "type": "string",
    "enum": [
     "apple",
     "google"
    ]
   },
   "serialNumber": {
    "type": "string"
   },
   "authenticationToken": {
    "type": "string",
    "format": "password",
    "writeOnly": true,
    "description": "**Write-only.** How the device proves it may fetch an update, and the reason a leaked serial alone is not enough to read somebody's ticket.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "issued",
     "updated",
     "voided",
     "expired"
    ]
   },
   "lastPushedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "deviceRegistrations": {
    "type": "integer",
    "description": "How many devices hold it. **A guest with the pass on a phone and a watch is one entitlement and two registrations**, and both need the update.\n"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "Wishlist": {
  "type": "object",
  "required": [
   "subjectId",
   "items"
  ],
  "x-ticvai-persistence": "none — wrapper. The items are the table, keyed by subject",
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "items": {
    "type": "array",
    "x-ticvai-persistence": "marketing.wishlist_item",
    "items": {
     "type": "object",
     "required": [
      "id",
      "variantId",
      "addedAt",
      "isAvailable"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "variantId": {
       "type": "string",
       "format": "uuid"
      },
      "productName": {
       "type": "string"
      },
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "performanceStartsAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "price": {
       "x-ticvai-column": "list_price",
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "The variant's current list price when the wishlist is read. Stored as `list_price` (naming-and-style 5.1 bans a bare `price` column); the wire keeps `price`."
      },
      "imageAssetRef": {
       "type": "string",
       "nullable": true
      },
      "isAvailable": {
       "type": "boolean",
       "description": "False where the product has been withdrawn or the performance has passed. Returned rather than dropped — a guest who saved something and finds it silently gone assumes the feature is broken.\n"
      },
      "unavailableReason": {
       "type": "string",
       "nullable": true
      },
      "note": {
       "type": "string",
       "nullable": true
      },
      "addedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   }
  }
 },
 "WorkstationContext": {
  "type": "object",
  "required": [
   "id",
   "code",
   "venueId",
   "regionId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "regionId": {
    "type": "string",
    "format": "uuid"
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid",
    "description": "Inherited from the workstation, never selected by the operator."
   },
   "devices": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "driver"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "receiptPrinter",
        "ticketPrinter",
        "cashDrawer",
        "barcodeScanner",
        "rfidReader",
        "paymentTerminal",
        "customerDisplay"
       ]
      },
      "driver": {
       "type": "string"
      },
      "identifier": {
       "type": "string"
      }
     }
    }
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4
   },
   "timezone": {
    "type": "string"
   },
   "cellName": {
    "type": "string",
    "description": "The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"
   },
   "deploymentProfile": {
    "type": "string",
    "enum": [
     "terminalLocal",
     "venueEdge",
     "thin"
    ],
    "description": "Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"
   }
  }
 }
}
```
