# P01-ticketing-01 — P01 · Ticketing

**3 screens · 15 operations · 30 schemas · 6 permissions**

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
| `screens.json` | Every field of every screen in the batch. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `LEDGER_VIEW, ORDER_CANCEL, ORDER_CREATE, ORDER_VIEW, PRODUCT_VIEW, RESOURCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store. Offline, a screen shows what was already loaded, under the banner below.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `WEB-030` | Ticket Transfer | listDetail | 4 | 3 | — |
| `WEB-031` | My Reservations | listDetail | 9 | 3 | — |
| `WEB-035` | Multi-Currency & Pricing | listDetail | 2 | 0 | — |

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

### Screen by screen

**`WEB-030` Ticket Transfer**

- A purchased ticket can be transferred to another guest (e.g. a friend); the system keeps the original purchaser and full transfer history. *(client request · MoM 7 Sep 2026, 4.9 Ownership and transfer · DI-669)*
- Once activated in the app a digital ticket is bound to one approved device; moving to a new device requires deactivating the prior binding. Credential transfer moves a ticket to another person's device and invalidates the original holder's copy. *(client request · MoM 2 Sep 2026, 4.8 Device Binding, Credential Transfer & Revocation · DI-636)*
- Ticket transfer by email/SMS with optional message; either keep ownership and rename the holder, or transfer both ownership and holder. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-200)*

**`WEB-031` My Reservations**

- **Open question.** Are water-park groups booked into a session (the build picks a session first)? Default built: group requests take a date and, for session-based products, a session. *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Water-park groups by session · DI-1117)*
- **Open question.** Each group ticket card shows a minimum group size; is it set per group ticket, and what values? Default built: each group ticket carries its own minimum, default 10. *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Minimum group size · DI-1116)*
- **Open question.** Do Tour operator and Community become their own group types or map to general? Default built: School, Corporate, Tour operator and Community shown as their own group types (platform also has general and party). *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Group types · DI-1115)*
- **Open question.** How many supervisors come free per group (per N guests), and is it per group ticket? Default built: supervisors are a separate, free guest type, up to 1 per 10 guests, counted on the group request. *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Supervisors · DI-1114)*
- Supervisors are listed separately and are free; the enquiry panel shows the estimate as e.g. "School group · Guests × 45". Water park group booking: pick a session, then enter the number of swimmers and supervisors. On mobile the headcount stepper has a +10 button. *(client request · design review 30 Sep 2026, 1. Group booking: product missing, enter the number of people · DI-1105)*
- Group / school booking starts with group ticket cards (School, Corporate, Tour operator, Community), each showing a per-person price and minimum group size. Then "How many people" is a number box the guest can type (e.g. 45) or step with − / +; no Group size dropdown. *(client request · design review 30 Sep 2026, 1. Group booking: product missing, enter the number of people · DI-1104)*
- Duplicate screens become one implementation covering several screen IDs (mobile Transfer + Delivery & Sharing; web Wishlist / Devices & Consent; Help Centre + Help & Accessibility as one Help view with FAQ, cases, policies, accessibility tabs). Ticket-selection functions belong on GST-008. Web gets a Group Booking view. *(agreed · design review 29 Sep 2026, GAP-D3 · D. Duplicate screens merged; group booking on web · DI-1078)*
- Booking statuses: draft > reserved (awaiting payment) > completed, with cancelled or expired paths. Hold policy sets how long a capacity booking is held pending payment before release to inventory. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-612)*
- Guest profile shows gift vouchers and a stored-value "money card"/wallet; "My Tickets" (all tickets) is separate from "My Reservations" (bookings holding one or more tickets) with reservation details and date modification. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-199)*

**`WEB-035` Multi-Currency & Pricing**

- Web screens carry: cart promo code (valid/invalid/expired) and empty basket with confirm; interrupted-payment recovery ("we are checking with your bank" → success/failed/unknown); reprint/resend tickets; UAE Pass sign-in, link guest checkout, sign out; support cases and Sahli handoff; FX rates with timestamp; remaining entitlements. *(agreed · design review 29 Sep 2026, GAP-B3 · B. Web — missing functions on existing screens · DI-1074)*
- A currency selector (AED, SAR, USD, INR, GBP) converts every displayed price. *(agreed · design review 29 Sep 2026, CFG-7 · Currency (AED/SAR/USD/INR/GBP) · DI-1071)*
- Foreign-currency display: an approximate conversion at a back-office rate so the guest sees roughly what they pay while settling in base currency, and/or full DCC at the gateway where the guest is charged in their own currency; records always in the venue base currency. *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-211)*

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "WEB-030",
  "name": "Ticket Transfer",
  "module": "Ticketing",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "guest-web",
   "route": "/ticket-transfer",
   "component": "apps/guest-web/src/routes/TicketTransfer.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "WEB-001",
    "WEB-031",
    "WEB-035"
   ],
   "inferred": true,
   "entryFrom": [
    "WEB-010"
   ],
   "transitions": [
    {
     "to": "WEB-031",
     "trigger": "My Reservations",
     "provenance": "derived — WEB-031 declares entryState.params groupBookingId, productId, reservationId, resourceId and WEB-030 holds none of them. The edge carries nothing: reservationId only pre-selects (deep link or optional); WEB-031 finds groupBookingId (requestGroupBooking), productId (listGroupPackages) itself; WEB-031 opens on listGroupPackages, and resourceId has no source on WEB-031 yet (a gap in WEB-031, not in this edge)"
    },
    {
     "to": "GST-014",
     "trigger": "The friend claims it in the app",
     "provenance": "flow F55 step 4→5",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "orderId",
      "transferId"
     ]
    }
   ]
  },
  "notes": "Added 17 August for parity with GST-014. **Not on the wireframe board** — needs drawing. CF-93.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listOrders` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Send a ticket to someone else, and see what you have sent.",
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
        "OrderSummary.lineCount"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
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
       "label": "Claim ticket transfer",
       "operation": "claimTicketTransfer",
       "provenance": "contract orders.yaml POST /ticket-transfers/{transferId}/claim"
      },
      {
       "kind": "secondaryButton",
       "label": "Create resale listing",
       "operation": "createResaleListing",
       "provenance": "contract orders.yaml POST /resale-listings"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The ticket transfer list.",
   "error": "Could not load. Names which read failed and leaves the ticket transfer untouched.",
   "emptyFirstRun": "No ticket transfer yet. Offers Create resale listing (`createResaleListing`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on venueId, principalId, shiftId, status, createdFrom, createdTo and the ticket transfer are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Sending, claiming and listing for resale need the connection — a transfer nobody received is a ticket nobody holds. Tickets already loaded stay visible."
  },
  "apis": [
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
    "operationId": "claimTicketTransfer",
    "contract": "orders",
    "purpose": "Claim transferred tickets",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "List orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "createResaleListing",
    "contract": "orders",
    "purpose": "List a ticket for resale",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "deepLink"
    },
    {
     "name": "transferId",
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
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-030",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "partial",
    "view": "Account → 'Transfer & resale'; My tickets → Manage → 'Transfer ticket'; Confirmation → 'Transfer tickets'",
    "differences": "List pane with toast actions; no recipient form. Prototype adds cancel transfer and withdraw resale listing."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateResaleListing",
    "component": "modal",
    "trigger": "Create resale listing",
    "body": "**Collects what `createResaleListing` sends before it is called.** Required: `entitlementId`, `askPrice`. Optional: `sellerSubjectId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateResaleListingRequest",
    "confirm": {
     "label": "Create resale listing",
     "operation": "createResaleListing"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "entitlementId",
      "askPrice",
      "sellerSubjectId"
     ]
    },
    "provenance": "client-verified"
   },
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
    "id": "formClaimTicketTransfer",
    "component": "modal",
    "trigger": "Claim ticket transfer",
    "body": "**Collects what `claimTicketTransfer` sends before it is called.** Required: `claimToken`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Claim ticket transfer",
     "operation": "claimTicketTransfer"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "claimToken"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "WEB-031",
  "name": "My Reservations",
  "module": "Ticketing",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "guest-web",
   "route": "/my-reservations",
   "component": "apps/guest-web/src/routes/MyReservations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "WEB-001",
    "WEB-030",
    "WEB-035"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "WEB-030",
     "trigger": "Ticket Transfer",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — WEB-030 declares entryState.params orderId, transferId and WEB-031 holds orderId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Added 17 August for parity with GST-016. **Not on the wireframe board** — needs drawing. CF-93.\n\n**Rev 3 (decided 29 September).** **Table deposit (REV3-8b):** a dining deposit is a venue option, off unless the venue enables it in Venue Management (`DepositPolicy.dining`; amount and basis are the venue's), superseding audit R077 (a). A reservation holding a deposit shows its amount, when it stops being refundable (`refundableUntil`) and the late-cancel and no-show terms. Group booking on the web is this screen (`requestGroupBooking`; GAP-D3, already); school and party requests are unchanged (DG-4).",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listReservations` reads the population and `getReservation` reads one of them — list, select, act",
  "purpose": "What you have booked and not yet paid for.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every reservations",
       "bindsTo": "Reservation",
       "columns": [
        "Reservation.id",
        "Reservation.venueId",
        "Reservation.status",
        "Reservation.lines",
        "Reservation.expiresAt",
        "Reservation.convertedOrderId"
       ],
       "operation": "listReservations",
       "provenance": "contract orders.yaml GET /reservations"
      },
      {
       "kind": "selectField",
       "label": "Kind",
       "operation": "listGroupPackages",
       "notes": "Sends `?kind=` to `listGroupPackages`.",
       "provenance": "contract catalogue.yaml GET /group-packages"
      },
      {
       "kind": "dataTable",
       "label": "Every group package definition",
       "bindsTo": "GroupPackageDefinition",
       "columns": [
        "GroupPackageDefinition.id",
        "GroupPackageDefinition.productId",
        "GroupPackageDefinition.kind",
        "GroupPackageDefinition.maxParticipants",
        "GroupPackageDefinition.durationMinutes",
        "GroupPackageDefinition.hostCount",
        "GroupPackageDefinition.pricingBasis",
        "GroupPackageDefinition.freeLeaderRatio",
        "GroupPackageDefinition.paymentMode",
        "GroupPackageDefinition.includes",
        "GroupPackageDefinition.scopePath"
       ],
       "operation": "listGroupPackages",
       "provenance": "contract catalogue.yaml GET /group-packages"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected group package definition",
       "bindsTo": "GroupPackageDefinition",
       "columns": [
        "GroupPackageDefinition.id",
        "GroupPackageDefinition.productId",
        "GroupPackageDefinition.kind",
        "GroupPackageDefinition.maxParticipants",
        "GroupPackageDefinition.durationMinutes",
        "GroupPackageDefinition.hostCount",
        "GroupPackageDefinition.pricingBasis",
        "GroupPackageDefinition.freeLeaderRatio",
        "GroupPackageDefinition.paymentMode",
        "GroupPackageDefinition.includes",
        "GroupPackageDefinition.scopePath"
       ],
       "operation": "getGroupPackageDefinition",
       "provenance": "contract catalogue.yaml GET /products/{productId}/group-package"
      },
      {
       "kind": "detailPanel",
       "label": "The group booking",
       "bindsTo": "GroupBooking",
       "columns": [
        "GroupBooking.id",
        "GroupBooking.kind",
        "GroupBooking.packageProductId",
        "GroupBooking.yearGroup",
        "GroupBooking.accessAndDietaryNeeds",
        "GroupBooking.celebrantName",
        "GroupBooking.celebrantTurningAge",
        "GroupBooking.allergiesAndRequests",
        "GroupBooking.finalHeadcountDueBy",
        "GroupBooking.quoteSentAt",
        "GroupBooking.riskAssessmentSentAt",
        "GroupBooking.preferredDate",
        "GroupBooking.orderId",
        "GroupBooking.leaderSubjectId",
        "GroupBooking.organisationName",
        "GroupBooking.expectedSize"
       ],
       "operation": "getGroupBooking",
       "provenance": "contract orders.yaml GET /group-bookings/{groupBookingId}"
      },
      {
       "kind": "detailPanel",
       "label": "The resource availability",
       "bindsTo": "ResourceAvailability",
       "columns": [
        "ResourceAvailability.resourceId",
        "ResourceAvailability.freeWindows",
        "ResourceAvailability.blockedWindows"
       ],
       "operation": "getResourceAvailability",
       "provenance": "contract resources.yaml GET /resources/{resourceId}/availability"
      },
      {
       "kind": "detailPanel",
       "label": "The reservation",
       "bindsTo": "Reservation",
       "columns": [
        "Reservation.id",
        "Reservation.venueId",
        "Reservation.subjectId",
        "Reservation.status",
        "Reservation.lines",
        "Reservation.expiresAt",
        "Reservation.convertedOrderId"
       ],
       "operation": "getReservation",
       "provenance": "contract orders.yaml GET /reservations/{reservationId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "destructiveButton",
       "label": "Cancel reservation",
       "operation": "cancelReservation",
       "provenance": "contract orders.yaml DELETE /reservations/{reservationId}"
      },
      {
       "kind": "primaryButton",
       "label": "Request group booking",
       "operation": "requestGroupBooking",
       "provenance": "contract orders.yaml POST /group-booking-requests"
      },
      {
       "kind": "secondaryButton",
       "label": "Save table reservation",
       "operation": "updateTableReservation",
       "provenance": "contract fnb.yaml PATCH /table-reservations/{reservationId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelReservation",
    "component": "confirmDialog",
    "trigger": "Cancel reservation",
    "body": "**Names what `cancelReservation` changes and what it leaves alone**, in the consequence rather than the verb. A reservations this affects should be identified in the dialog, not just counted.",
    "provenance": "client-verified"
   },
   {
    "id": "formRequestGroupBooking",
    "component": "modal",
    "trigger": "Request group booking",
    "body": "**Collects what `requestGroupBooking` sends before it is called.** Required: `kind`, `packageProductId`, `preferredDate`, `expectedSize`. Optional: `organisationName`, `yearGroup`, `accessAndDietaryNeeds`, `celebrantName`, `celebrantTurningAge`, `allergiesAndRequests`. Dismissing sends nothing; the screen behind is unchanged.\n**30 September (client feedback, CLIENT-RESPONSE-30SEP 1).** The group ticket is chosen first (`packageProductId`: cards with the per-person price and the minimum group size), then *How many people* (`expectedSize`) as a number box the guest types into or steps with − and + (+10 on the app); no Group size dropdown. The estimate reads *<ticket> · Guests × <n>*.",
    "bindsTo": "GroupBookingRequest",
    "confirm": {
     "label": "Request group booking",
     "operation": "requestGroupBooking"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "packageProductId",
      "preferredDate",
      "expectedSize",
      "organisationName",
      "yearGroup",
      "accessAndDietaryNeeds",
      "celebrantName",
      "celebrantTurningAge",
      "allergiesAndRequests"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formUpdateTableReservation",
    "component": "modal",
    "trigger": "Save table reservation",
    "body": "**Collects what `updateTableReservation` sends before it is called.** Required: `outletId`, `partySize`, `startsAt`. Optional: `id`, `subjectId`, `guestName`, `contactPoint`, `durationMinutes`, `tables`, `status`, `groupId`, `notes`, `actualPartySize`, `tableVisitId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "TableReservation",
    "confirm": {
     "label": "Save table reservation",
     "operation": "updateTableReservation"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "outletId",
      "partySize",
      "startsAt",
      "id",
      "subjectId",
      "guestName",
      "contactPoint",
      "durationMinutes",
      "tables",
      "status",
      "groupId",
      "notes",
      "actualPartySize",
      "tableVisitId"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "states": {
   "loading": "The reservations list.",
   "error": "Could not load. Names which read failed and leaves the reservations untouched.",
   "emptyFirstRun": "No reservations yet. Offers Request group booking (`requestGroupBooking`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on kind and the reservations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Reservations already loaded stay visible with their age. Booking, changing and cancelling need the connection — a table held offline is a table two people think they have."
  },
  "apis": [
   {
    "operationId": "listGroupPackages",
    "contract": "catalogue",
    "purpose": "School-trip formats and party packages",
    "trigger": "onLoad"
   },
   {
    "operationId": "getGroupPackageDefinition",
    "contract": "catalogue",
    "purpose": "What a package includes",
    "trigger": "onAction"
   },
   {
    "operationId": "requestGroupBooking",
    "contract": "orders",
    "purpose": "Ask for a school trip or a birthday party",
    "trigger": "onAction"
   },
   {
    "operationId": "listReservations",
    "contract": "orders",
    "purpose": "List reservations",
    "trigger": "onLoad"
   },
   {
    "operationId": "getReservation",
    "contract": "orders",
    "purpose": "Read a reservation",
    "trigger": "onAction"
   },
   {
    "operationId": "cancelReservation",
    "contract": "orders",
    "purpose": "Cancel a reservation",
    "trigger": "onAction",
    "invalidates": [
     "listReservations"
    ]
   },
   {
    "operationId": "getGroupBooking",
    "contract": "orders",
    "purpose": "A group booking this guest belongs to",
    "trigger": "onAction"
   },
   {
    "operationId": "getResourceAvailability",
    "contract": "resources",
    "purpose": "What is free and when",
    "trigger": "onAction"
   },
   {
    "operationId": "updateTableReservation",
    "contract": "fnb",
    "purpose": "Change or cancel it",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "reservationId",
     "from": "deepLink"
    },
    {
     "name": "groupBookingId",
     "from": "navigation"
    },
    {
     "name": "resourceId",
     "from": "navigation"
    },
    {
     "name": "productId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `reservationId`.",
   "preloaded": [
    "Reservation.id",
    "Reservation.venueId",
    "Reservation.status",
    "Reservation.lines",
    "Reservation.expiresAt"
   ]
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-031",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "partial",
    "view": "Account → 'Reservations'",
    "differences": "The prototype uses the WEB-031 label for the group booking request dialog (deposit / invoice quote) inside Kids Club → 'Birthday party / group' and 'School trip', which the YAML covers only through requestGroupBooking. 'Pay now' on a held reservation has no YAML route (WEB-014 is pay-by-link)."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "WEB-035",
  "name": "Multi-Currency & Pricing",
  "module": "Ticketing",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "guest-web",
   "route": "/multi-currency-pricing",
   "component": "apps/guest-web/src/routes/MulticurrencyPricing.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "WEB-001",
    "WEB-030",
    "WEB-031"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "WEB-030",
     "trigger": "Ticket Transfer",
     "provenance": "derived — WEB-030 declares entryState.params orderId, transferId and WEB-035 holds none of them. The edge carries nothing: orderId, transferId only pre-select (deep link or optional), and WEB-030 opens on its own"
    },
    {
     "to": "WEB-031",
     "trigger": "My Reservations",
     "carries": [
      "productId"
     ],
     "provenance": "derived — WEB-031 declares entryState.params groupBookingId, productId, reservationId, resourceId and WEB-035 holds productId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Added 17 August. **The surface the matrix names** — 2.6.33 *\"website should be able to display multi currency\"* and 2.9.1 *\"in the B2C portal for guests comparison\"*. Wave 1 against the app's Wave 2, because **the website is where an overseas guest compares before booking** and the app is where they check after. **Display only — the sale settles in base currency** (CF-37). Not on the wireframe board; needs drawing. **`getRegionSettings` deliberately not called** — a guest does not need the venue's scope configuration to pick a currency. `listFxRates` is the currency list: a rate exists only for a currency the venue enabled, so the two questions have one answer.\n\n**Rev 3 (decided 29 September, rev 3 GAP-D2).** The web and app waves of this capability differ; they are aligned to one wave once the client picks it (open, client to choose).\n\nRates carry `fetchedAt` (`listFxRates`; GAP-B3, already); the prototype's fixed demo rate is prototype-only (CFG-7, no change).",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listFxRates` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Compare prices in your own currency before you travel.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "selectField",
       "label": "Venue",
       "operation": "listFxRates",
       "notes": "Sends `?venueId=` to `listFxRates`, from the venue the guest picked (see the home screen), so the list is the region's rates narrowed to the currencies this venue shows. Rates are set per region and each venue picks which currencies it shows (decided 28 September, audit R120 (a)).",
       "provenance": "contract finance.yaml GET /fx-rates"
      },
      {
       "kind": "datePicker",
       "label": "As at",
       "operation": "listFxRates",
       "notes": "Sends `?asAt=` to `listFxRates`.",
       "provenance": "contract finance.yaml GET /fx-rates"
      },
      {
       "kind": "textField",
       "label": "Purpose",
       "operation": "listFxRates",
       "notes": "Sends `?purpose=` to `listFxRates`.",
       "provenance": "contract finance.yaml GET /fx-rates"
      },
      {
       "kind": "dataTable",
       "label": "Every FX rate",
       "bindsTo": "FxRate",
       "columns": [
        "FxRate.id",
        "FxRate.fromCurrency",
        "FxRate.toCurrency",
        "FxRate.rate",
        "FxRate.purpose",
        "FxRate.source",
        "FxRate.effectiveFrom",
        "FxRate.effectiveTo",
        "FxRate.setByPrincipalId",
        "FxRate.providerReference",
        "FxRate.fetchedAt"
       ],
       "operation": "listFxRates",
       "provenance": "contract finance.yaml GET /fx-rates"
      },
      {
       "kind": "dataTable",
       "label": "Every product",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo"
       ],
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected FX rate",
       "bindsTo": "FxRate",
       "columns": [
        "FxRate.id",
        "FxRate.fromCurrency",
        "FxRate.toCurrency",
        "FxRate.rate",
        "FxRate.purpose",
        "FxRate.source",
        "FxRate.effectiveFrom",
        "FxRate.effectiveTo",
        "FxRate.setByPrincipalId",
        "FxRate.providerReference",
        "FxRate.fetchedAt"
       ],
       "operation": "listFxRates",
       "provenance": "contract finance.yaml GET /fx-rates"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The multi-currency pricing list.",
   "error": "Could not load. Names which read failed and leaves the multi-currency pricing untouched.",
   "emptyFirstRun": "No multi-currency pricing yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on asAt, purpose and the multi-currency pricing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows. Last known rates stay, with their age.** A rate is a number a guest may act on, and an undated one they cannot judge."
  },
  "apis": [
   {
    "operationId": "listFxRates",
    "contract": "finance",
    "purpose": "The rates in force for the venue's shown currencies — always called with `venueId` (decided 28 September, audit R120 (a))",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "FxRate.id",
    "FxRate.fromCurrency",
    "FxRate.toCurrency",
    "FxRate.rate",
    "FxRate.purpose"
   ]
  },
  "wireframe": {
   "status": "review",
   "provenance": "client-verified",
   "board": "wireframes/P01 Guest Web.dc.html#web-035",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Discover → 'Prices in your currency'",
    "differences": "Matches the YAML's charged-vs-shown rule. Separately, Config → Currency switches the whole storefront currency, which contradicts 'always charged in AED'."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
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
 "cancelReservation": {
  "method": "DELETE",
  "path": "/reservations/{reservationId}",
  "contract": "orders",
  "summary": "Cancel a reservation",
  "permission": "ORDER_CANCEL",
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
 "claimTicketTransfer": {
  "method": "POST",
  "path": "/ticket-transfers/{transferId}/claim",
  "contract": "orders",
  "summary": "Claim transferred tickets",
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
  "responds": "TicketTransfer"
 },
 "createResaleListing": {
  "method": "POST",
  "path": "/resale-listings",
  "contract": "orders",
  "summary": "List an entitlement for resale",
  "permission": "ORDER_CREATE",
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
  "requestBody": "CreateResaleListingRequest",
  "responds": "ResaleListing"
 },
 "getGroupBooking": {
  "method": "GET",
  "path": "/group-bookings/{groupBookingId}",
  "contract": "orders",
  "summary": "A group, its leader and its name-capture duty",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupBooking"
 },
 "getGroupPackageDefinition": {
  "method": "GET",
  "path": "/products/{productId}/group-package",
  "contract": "catalogue",
  "summary": "A school-trip format or party package",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productId",
    "in": "path",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "GroupPackageDefinition"
 },
 "getReservation": {
  "method": "GET",
  "path": "/reservations/{reservationId}",
  "contract": "orders",
  "summary": "Read a reservation",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Reservation"
 },
 "getResourceAvailability": {
  "method": "GET",
  "path": "/resources/{resourceId}/availability",
  "contract": "resources",
  "summary": "When it is free, with conflicts already resolved",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": true
   },
   {
    "name": "to",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "ResourceAvailability"
 },
 "listFxRates": {
  "method": "GET",
  "path": "/fx-rates",
  "contract": "finance",
  "summary": "The rates in force",
  "permission": "LEDGER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "asAt",
    "in": "query",
    "required": null
   },
   {
    "name": "purpose",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
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
 "listGroupPackages": {
  "method": "GET",
  "path": "/group-packages",
  "contract": "catalogue",
  "summary": "The school-trip formats or party packages on offer",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kind",
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
 "listProducts": {
  "method": "GET",
  "path": "/products",
  "contract": "catalogue",
  "summary": "List products",
  "permission": "PRODUCT_VIEW",
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
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "isSellable",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "segmentTag",
    "in": "query",
    "required": null
   },
   {
    "name": "guidedAnswerIds",
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
 "listReservations": {
  "method": "GET",
  "path": "/reservations",
  "contract": "orders",
  "summary": "List reservations",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "expiringWithinMinutes",
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
 "requestGroupBooking": {
  "method": "POST",
  "path": "/group-booking-requests",
  "contract": "orders",
  "summary": "Ask for a school trip or a birthday party",
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
  "requestBody": "GroupBookingRequest",
  "responds": "GroupBooking"
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
 "updateTableReservation": {
  "method": "PATCH",
  "path": "/table-reservations/{reservationId}",
  "contract": "fnb",
  "summary": "Change or cancel a booking",
  "permission": null,
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
  "requestBody": "TableReservation",
  "responds": "TableReservation"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Channel": {
  "type": "string",
  "enum": [
   "pos",
   "kiosk",
   "web",
   "mobile",
   "b2b",
   "ota",
   "callCentre"
  ]
 },
 "CreateOrderLine": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "variantId",
   "quantity",
   "quotedUnitPrice"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these."
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "recommendationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Carried from the cart line at checkout; stored on `orders.order_line` and sent in `order.completed` lines.\n"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "bookedWindow": {
    "$ref": "#/components/schemas/BookedWindow"
   },
   "inventoryHoldId": {
    "type": "string",
    "nullable": true,
    "description": "Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."
   },
   "seatIds": {
    "type": "array",
    "maxItems": 50,
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."
   },
   "resourceHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."
   },
   "attributes": {
    "$ref": "#/components/schemas/OrderLineAttributes"
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "eligibilityDeclaration": {
    "type": "array",
    "nullable": true,
    "x-ticvai-note": "One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n",
    "items": {
     "type": "object",
     "properties": {
      "ageBand": {
       "type": "string",
       "enum": [
        "infant",
        "child",
        "junior",
        "adult",
        "senior"
       ],
       "description": "Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."
      },
      "ageYears": {
       "type": "integer",
       "nullable": true
      },
      "heightBandIndex": {
       "type": "integer",
       "nullable": true
      },
      "confidentSwimmer": {
       "type": "boolean",
       "nullable": true,
       "description": "**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"
      },
      "guardianSigned": {
       "type": "boolean"
      }
     }
    },
    "description": "What was declared for each guest on this line, kept as the record staff check at the gate."
   },
   "quotedUnitPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "What the client charged, from its local bundle."
   },
   "holderName": {
    "type": "string",
    "nullable": true
   },
   "dataMaskValues": {
    "type": "object",
    "additionalProperties": true,
    "description": "**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"
   }
  }
 },
 "CreateResaleListingRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "Request only; persisted as `ResaleListing`. **What a seller decides**: which entitlement, and at what price. The id, the status, the fee snapshot and the partition key are the server's, which is why `createResaleListing` no longer takes the whole listing.\n",
  "required": [
   "entitlementId",
   "askPrice"
  ],
  "properties": {
   "entitlementId": {
    "type": "string",
    "format": "uuid"
   },
   "askPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "sellerSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The holder listing it. A guest caller is always the seller and may name only themselves; a member of staff listing on a guest's behalf names the guest."
   }
  }
 },
 "FnbReservationTable": {
  "type": "object",
  "x-ticvai-persistence": "fnb.reservation_table",
  "description": "**Taken from the backend workbook, 20 September.** Maps one or more dining tables assigned to a reservation.",
  "required": [
   "reservationId",
   "tableId",
   "createdAt"
  ],
  "properties": {
   "reservationId": {
    "type": "string",
    "format": "uuid"
   },
   "tableId": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "FxRate": {
  "type": "object",
  "x-ticvai-persistence": "ledger.fx_rate",
  "description": "Also the `setFxRate` body. **Server-owned fields are `readOnly`** and ignored if sent: `id`, `setByPrincipalId`, and the provenance `ingestFxRates` writes (`source`, `providerReference`, `fetchedAt`). A rate set through `setFxRate` has `source` `manual`.\n",
  "required": [
   "fromCurrency",
   "toCurrency",
   "rate",
   "purpose",
   "effectiveFrom"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "fromCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "toCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "rate": {
    "allOf": [
     {
      "$ref": "#/components/schemas/FxRateValue"
     }
    ],
    "description": "Units of `toCurrency` per one `fromCurrency`. Six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly.\n"
   },
   "purpose": {
    "$ref": "#/components/schemas/FxRatePurpose"
   },
   "source": {
    "allOf": [
     {
      "$ref": "#/components/schemas/FxRateSource"
     }
    ],
    "readOnly": true
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "A rate change is a new row. The old one is never edited — a transaction posted last Tuesday must still reconcile at last Tuesday's rate.\n"
   },
   "setByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "note": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "description": "Why this rate, and from where. **Required when `source` is `manual`** (decided 28 September, audit R127 (4)); null on a rate `ingestFxRates` fetched."
   },
   "providerReference": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The provider's own identifier for this quote. **What makes a rate reproducible** — an auditor asking why a payment converted at 3.6725 gets an answer that is checkable against the source rather than a number somebody typed."
   },
   "fetchedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When the rate was pulled. **Distinct from `effectiveFrom`**, which is when it applies — a rate fetched at 06:00 for a business day starting at 00:00 has two different times and conflating them makes a late feed look like a backdated rate."
   }
  }
 },
 "FxRatePurpose": {
  "type": "string",
  "description": "A venue does not accept dollars at the rate it books an intercompany balance at. Separating them is what stops a spread on the counter appearing as a loss in the accounts.\n",
  "enum": [
   "tender",
   "interEntity",
   "reporting",
   "revaluation"
  ]
 },
 "FxRateSource": {
  "type": "string",
  "description": "**Where the rate came from, and which provider specifically.** `source: provider` said a feed set it and not which one — two tenants on different feeds were indistinguishable in the ledger, and a rate cannot be defended in an audit without naming its origin.\n\n**`uaeCentralBank` is the default for AED pairs.** The UAE Central Bank publishes an official daily rate and it is what a UAE auditor expects to see — a commercial feed is defensible for tender and awkward for statutory reporting.\n\n**`openExchangeRates` and `ecb` are the commercial and reference options.** ECB publishes daily reference rates free and is the usual fallback for non-AED pairs; Open Exchange Rates is the common commercial feed with intraday granularity. **The choice is per purpose, not per platform** — a tender rate wants intraday, a reporting rate wants the official daily close.",
  "enum": [
   "manual",
   "uaeCentralBank",
   "ecb",
   "openExchangeRates",
   "cardScheme",
   "provider"
  ]
 },
 "FxRateValue": {
  "x-ticvai-persistence-column": "numeric(18,6)",
  "type": "string",
  "pattern": "^\\d+(\\.\\d{1,6})?$",
  "description": "**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one (naming-and-style 5.1). Up to six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly — and stored as `numeric(18,6)` so the six places the wire carries survive the database.\n"
 },
 "GroupBooking": {
  "type": "object",
  "x-ticvai-persistence": "orders.group_booking",
  "description": "BL-028. **`BO-026 Group Bookings` ran on generic order operations** — no group size, no quota, no leader, no per-attendee capture.\n**The leader is the point.** A school booking forty places has one person who pays, one who is called if the coach is late, and forty who need names collecting — and a generic order has one guest.\n",
  "required": [
   "id",
   "orderId",
   "leaderSubjectId",
   "expectedSize",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "general",
     "school",
     "corporate",
     "party"
    ],
    "default": "general"
   },
   "packageProductId": {
    "type": "string",
    "nullable": true,
    "description": "The school-trip format or party package."
   },
   "yearGroup": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "accessAndDietaryNeeds": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "celebrantName": {
    "type": "string",
    "maxLength": 120,
    "nullable": true,
    "description": "The birthday child."
   },
   "celebrantTurningAge": {
    "type": "integer",
    "minimum": 1,
    "maximum": 18,
    "nullable": true
   },
   "allergiesAndRequests": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "finalHeadcountDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "quoteSentAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "riskAssessmentSentAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "preferredDate": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "The date the guest asked for on `requestGroupBooking` — what its `409 dateUnavailable` is checked against. Null for a group a member of staff built from an order."
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "leaderSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "organisationName": {
    "type": "string",
    "nullable": true
   },
   "expectedSize": {
    "type": "integer"
   },
   "confirmedSize": {
    "type": "integer",
    "nullable": true
   },
   "minimumSize": {
    "type": "integer",
    "nullable": true,
    "description": "**Below which the group rate does not apply.** A booking for forty that arrives as twelve is a pricing question somebody has to answer at the gate, and stating the threshold means answering it at booking instead.\n"
   },
   "attendeeCaptureRequired": {
    "type": "boolean",
    "default": false,
    "description": "**Whether names are needed before admission.** A school trip usually needs them and a corporate day out usually does not, and the difference is a safeguarding requirement rather than a preference.\n"
   },
   "attendeeCaptureDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "provisional",
     "confirmed",
     "namesPending",
     "complete",
     "cancelled"
    ]
   }
  }
 },
 "GroupBookingRequest": {
  "type": "object",
  "description": "Request only. The caller is the leader. `kind` is the same vocabulary as `GroupBooking.kind`, so a request the guest makes can be any group the venue books.",
  "required": [
   "kind",
   "packageProductId",
   "preferredDate",
   "expectedSize"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "general",
     "school",
     "corporate",
     "party"
    ]
   },
   "packageProductId": {
    "type": "string"
   },
   "preferredDate": {
    "type": "string",
    "format": "date"
   },
   "expectedSize": {
    "type": "integer",
    "minimum": 2
   },
   "organisationName": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "description": "The school."
   },
   "yearGroup": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "accessAndDietaryNeeds": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "celebrantName": {
    "type": "string",
    "maxLength": 120,
    "nullable": true,
    "description": "The birthday child."
   },
   "celebrantTurningAge": {
    "type": "integer",
    "minimum": 1,
    "maximum": 18,
    "nullable": true
   },
   "allergiesAndRequests": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   }
  }
 },
 "GroupPackageDefinition": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.group_package",
  "required": [
   "kind",
   "maxParticipants",
   "durationMinutes"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "productId": {
    "type": "string",
    "readOnly": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "school",
     "party"
    ]
   },
   "maxParticipants": {
    "type": "integer",
    "minimum": 1,
    "description": "Pupils or children, e.g. 30 or 10."
   },
   "durationMinutes": {
    "type": "integer",
    "minimum": 15
   },
   "hostCount": {
    "type": "integer",
    "minimum": 0,
    "default": 1,
    "description": "Party hosts included."
   },
   "pricingBasis": {
    "type": "string",
    "enum": [
     "perParticipant",
     "perPackage"
    ]
   },
   "freeLeaderRatio": {
    "type": "integer",
    "nullable": true,
    "default": 10,
    "description": "Schools: one teacher or assistant enters free per this many pupils."
   },
   "paymentMode": {
    "type": "string",
    "enum": [
     "invoice",
     "deposit",
     "full"
    ],
    "description": "Schools are invoiced; parties take a deposit (see `DepositPolicy`)."
   },
   "includes": {
    "type": "array",
    "items": {
     "type": "string",
     "maxLength": 120
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   }
  }
 },
 "GuestListing": {
  "type": "string",
  "enum": [
   "bookable",
   "infoOnly",
   "hidden"
  ],
  "default": "bookable",
  "description": "**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"
 },
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
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
 "Product": {
  "x-ticvai-persistence": "catalogue.product",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "kind",
   "venueId",
   "scopePath",
   "isSellable",
   "hasVariants"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "familyKey": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[A-Za-z0-9_-]+$",
    "nullable": true,
    "x-ticvai-unique": "venue",
    "description": "**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/ProductKind"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "responsibleDepartmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Who owns this product commercially. A scope node at `department` level."
   },
   "onSaleFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"
   },
   "onSaleTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"
   },
   "lifecycleState": {
    "$ref": "#/components/schemas/ProductLifecycleState"
   },
   "isSellable": {
    "type": "boolean",
    "readOnly": true,
    "description": "True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"
   },
   "isStockTracked": {
    "type": "boolean",
    "default": false,
    "description": "**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"
   },
   "hasVariants": {
    "type": "boolean"
   },
   "variantCount": {
    "type": "integer"
   },
   "segmentTags": {
    "type": "array",
    "description": "7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n",
    "items": {
     "type": "string"
    }
   },
   "codeSchema": {
    "type": "string",
    "readOnly": true,
    "description": "7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Channel"
    }
   },
   "entitlementTemplateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"
   },
   "blockedOffline": {
    "type": "boolean",
    "description": "True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"
   },
   "dataMaskValues": {
    "type": "object",
    "additionalProperties": true,
    "description": "Custom fields. JSONB-backed, defined by the venue's data mask."
   },
   "guestListing": {
    "$ref": "#/components/schemas/GuestListing"
   },
   "notBookableLabel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"
   },
   "salesContact": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProductSalesContact"
     }
    ],
    "nullable": true,
    "description": "**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"
   },
   "bookingFlowId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"
   },
   "displayTags": {
    "type": "array",
    "maxItems": 6,
    "items": {
     "$ref": "#/components/schemas/ProductDisplayTag"
    },
    "description": "**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"
   },
   "media": {
    "type": "array",
    "maxItems": 20,
    "items": {
     "$ref": "#/components/schemas/ProductMedia"
    },
    "description": "**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"
   },
   "consentQuestionIds": {
    "type": "array",
    "maxItems": 10,
    "uniqueItems": true,
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"
   },
   "requiresTimeWindow": {
    "type": "boolean",
    "default": false,
    "description": "**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"
   },
   "productOwnerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."
   },
   "operationalContact": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "description": "A principal id or a name, as the context screen takes it."
   },
   "businessUnitId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `ledger.legal_entity`, read through finance."
   },
   "attractionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "siteId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "locationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The brand, as the context screen names it (a catalogue brand category)."
   },
   "marketCode": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "salesTerritory": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   }
  }
 },
 "ProductDisplayTag": {
  "x-ticvai-persistence": "none — jsonb column on catalogue.product",
  "type": "object",
  "required": [
   "kind",
   "label"
  ],
  "description": "One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.",
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "clock",
     "height",
     "free",
     "calendar",
     "id"
    ],
    "description": "`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."
   },
   "label": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."
   },
   "derived": {
    "type": "boolean",
    "readOnly": true,
    "default": false,
    "description": "True on a tag the server derived on read because the venue set none. Never sent."
   }
  }
 },
 "ProductKind": {
  "type": "string",
  "description": "**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n",
  "enum": [
   "admission",
   "timedAdmission",
   "datedAdmission",
   "openDated",
   "seated",
   "membership",
   "bundle",
   "fnb",
   "retail",
   "rental",
   "addOn",
   "giftCard"
  ]
 },
 "ProductLifecycleState": {
  "type": "string",
  "enum": [
   "draft",
   "inReview",
   "approved",
   "live",
   "withdrawn",
   "archived"
  ]
 },
 "ProductMedia": {
  "x-ticvai-persistence": "catalogue.product_media",
  "type": "object",
  "required": [
   "assetId",
   "kind",
   "isPrimary"
  ],
  "description": "One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n",
  "properties": {
   "assetId": {
    "type": "string",
    "format": "uuid",
    "description": "A `MediaAsset` of `assets.yaml`, in status `ready`."
   },
   "kind": {
    "type": "string",
    "enum": [
     "image",
     "video"
    ]
   },
   "isPrimary": {
    "type": "boolean",
    "default": false,
    "description": "The item *Read more* opens on and a listing shows. Exactly one per product."
   },
   "displayOrder": {
    "type": "integer",
    "default": 100
   },
   "altText": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true
   }
  }
 },
 "ProductSalesContact": {
  "x-ticvai-persistence": "none — jsonb column on catalogue.product",
  "type": "object",
  "description": "Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n",
  "minProperties": 1,
  "properties": {
   "phone": {
    "type": "string",
    "maxLength": 32,
    "nullable": true
   },
   "email": {
    "type": "string",
    "format": "email",
    "maxLength": 254,
    "nullable": true
   },
   "note": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."
   }
  }
 },
 "ResaleListing": {
  "type": "object",
  "x-ticvai-persistence": "orders.resale_listing",
  "description": "BL-060. **Smaller than it first looked** — most of the machinery exists. An entitlement can already be transferred, an order can already be created, and payment already routes. What was missing is the listing itself and a cart line that can point at one.\n**A resale is a transfer with money attached**, and the venue is in the middle: the buyer becomes the owner of the same entitlement (the virtual ticket ID is preserved, MoM 1 Sep 4.14), its media is re-issued and the transfer is logged, so **the media that admits is always one the venue issued.** That is what stops a screenshot at the gate.\n",
  "required": [
   "id",
   "entitlementId",
   "sellerSubjectId",
   "askPrice",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "entitlementId": {
    "type": "string",
    "format": "uuid"
   },
   "sellerSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "askPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "priceCapPercent": {
    "type": "number",
    "nullable": true,
    "readOnly": true,
    "description": "**A ceiling as a percentage of face value**, because uncapped resale is a venue watching its own tickets sold at four times the price with its name on them. Null means uncapped, which is a venue decision rather than a default. Snapshotted from `ResaleFeePolicy` at listing.\n"
   },
   "sellerFeePercent": {
    "type": "number",
    "readOnly": true,
    "description": "Snapshotted from `ResaleFeePolicy` at listing."
   },
   "buyerFeePercent": {
    "type": "number",
    "readOnly": true,
    "description": "Snapshotted from `ResaleFeePolicy` at listing."
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "pendingReview",
     "listed",
     "reserved",
     "sold",
     "withdrawn",
     "expired",
     "rejected"
    ],
    "description": "`pendingReview` and `rejected` added 29 September (DM5): a listing the marketplace's `moderationMode` sends to review waits there until `approveListingModeration` lists or rejects it."
   },
   "listedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "soldToSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "reviewReasons": {
    "type": "array",
    "readOnly": true,
    "description": "Why the listing was sent to review (DM5, 29 September).",
    "items": {
     "type": "string",
     "enum": [
      "highResalePrice",
      "unusualDiscount",
      "highValueTicket",
      "vipTicket",
      "sellerRisk",
      "newSeller",
      "multipleListings",
      "identityIssue",
      "paymentIssue",
      "ticketOwnershipConcern",
      "fraudIndicator"
     ]
    }
   },
   "moderatedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "moderatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "moderationReason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true,
    "readOnly": true
   },
   "payoutStatus": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "pending",
     "held",
     "paid",
     "failed"
    ],
    "description": "**The seller is paid after the buyer is admitted, not after they pay.** A resale refunded at the gate for a void ticket cannot be clawed back from a seller who has already been paid.\n"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "Reservation": {
  "x-ticvai-persistence": "orders.reservation + orders.reservation_line",
  "type": "object",
  "description": "**An unpaid hold, not a booking.** It holds capacity, expires, issues no entitlement and carries no media — a paid booking is an order (naming-and-style §3.1).\n",
  "required": [
   "id",
   "venueId",
   "status",
   "expiresAt",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The guest it is held for, from `CreateReservationRequest.subjectId`. A guest caller sees only reservations carrying their own."
   },
   "status": {
    "type": "string",
    "enum": [
     "held",
     "converted",
     "expired",
     "cancelled"
    ]
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/CreateOrderLine"
    }
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "convertedOrderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "ResourceAvailability": {
  "type": "object",
  "description": "**Free windows, with setup and teardown already subtracted.** A client computing this from bookings will forget the turnaround.\n",
  "properties": {
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "freeWindows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "date-time"
      },
      "to": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "blockedWindows": {
    "type": "array",
    "description": "**With a reason, because they are not the same.** Booked and under repair need different responses from an operator looking for something free — wait, or look elsewhere.\n",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "date-time"
      },
      "to": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string",
       "enum": [
        "booked",
        "held",
        "setup",
        "teardown",
        "maintenance",
        "blackout",
        "closed",
        "cleaning"
       ],
       "description": "`held` is a live `ResourceHold` (rev 3 REV3-15): taken now, free again if it expires. `cleaning` is a cleaning the resource's `cleaningPolicy` places (W10, 29 September).\n"
      }
     }
    }
   }
  }
 },
 "TableReservation": {
  "type": "object",
  "x-ticvai-persistence": "fnb.table_reservation",
  "x-ticvai-retired-columns": [
   "table_ids"
  ],
  "required": [
   "outletId",
   "startsAt",
   "partySize"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "guestName": {
    "type": "string"
   },
   "contactPoint": {
    "type": "string"
   },
   "partySize": {
    "type": "integer",
    "minimum": 1
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "durationMinutes": {
    "type": "integer",
    "description": "**How long the cover is held.** An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked.\n"
   },
   "tables": {
    "type": "array",
    "description": "The dining tables assigned to this reservation, one row each.\n**Usually empty until seating.** Committing a specific table at booking time refuses later bookings against a constraint that did not need to exist — that was true of the `tableIds` array this replaces and it is still true, because it is about *when* a table is assigned rather than how the assignment is stored.\n**Replaces `tableIds`, retired 20 September.** An array cannot carry per-row state, which is the same reason this merge took `entry_rule_point`, `menu_item_modifier`, `seat_block_item`, `plan_benefit`, `payment_method_config` and `tier_module` from the backend workbook. A party seated across three tables that releases one early has nowhere to say so in an array, and *\"which reservations are on table 7 tonight\"* is a GIN scan over every reservation instead of an index seek.\n",
    "items": {
     "$ref": "#/components/schemas/FnbReservationTable"
    }
   },
   "status": {
    "$ref": "#/components/schemas/TableReservationStatus"
   },
   "groupId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "5.1.2. Several bookings managed as one party across adjacent tables."
   },
   "notes": {
    "type": "string",
    "description": "Allergies",
    "occasion": null,
    "accessibility.": null
   },
   "actualPartySize": {
    "type": "integer",
    "nullable": true,
    "readOnly": true
   },
   "tableVisitId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "deposit": {
    "$ref": "#/components/schemas/TableReservationDeposit"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "TableReservationDeposit": {
  "type": "object",
  "nullable": true,
  "readOnly": true,
  "x-ticvai-persistence": "fnb.table_reservation",
  "description": "**The deposit this booking holds, snapshotted from `orders.DepositPolicy.dining` when it was made** (decided 29 September, rev 3 REV3-8b). Null where no deposit applied, which is every booking while the venue leaves `dining.enabled` false (the default). A later change to the policy does not re-price a booking already made.\n",
  "required": [
   "amount",
   "basis"
  ],
  "properties": {
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "basis": {
    "type": "string",
    "enum": [
     "fixedPerGuest",
     "fixedPerTable",
     "percentOfMinimumSpend"
    ]
   },
   "holdExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "While `awaitingDeposit`, when the held cover is released if the deposit has not been authorised. The cart lease of the deposit line (15 minutes, audit R169)."
   },
   "refundableUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "`startsAt` less `dining.refundableUntilHours`. Cancelling before it releases the deposit in full."
   },
   "variantId": {
    "type": "string",
    "format": "uuid",
    "description": "The venue's table-deposit variant, `DepositPolicy.dining.depositVariantId`, which the client sends to `addCartLine` with this booking's id."
   },
   "cartLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `orders.CartLine` carrying the deposit, once added."
   },
   "depositId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `orders.deposit` row, once the payment is authorised."
   }
  }
 },
 "TableReservationStatus": {
  "type": "string",
  "description": "`awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`.",
  "enum": [
   "awaitingDeposit",
   "booked",
   "confirmed",
   "seated",
   "completed",
   "cancelled",
   "noShow"
  ]
 },
 "TicketTransfer": {
  "x-ticvai-persistence": "orders.ticket_transfer",
  "type": "object",
  "required": [
   "id",
   "orderId",
   "ticketIds",
   "status",
   "offeredAt",
   "expiresAt"
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
   "ticketIds": {
    "type": "array",
    "description": "The entitlements offered — `Entitlement.id` values, since a ticket is an entitlement. Each points at `access.entitlement`.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "fromSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "toSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Set only on claim. Ownership moves then, not at offer."
   },
   "recipientAddressMasked": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "offered",
     "claimed",
     "expired",
     "cancelled"
    ]
   },
   "claimUrl": {
    "type": "string",
    "nullable": true
   },
   "claimToken": {
    "type": "string",
    "format": "password",
    "writeOnly": true,
    "description": "**What `claimTicketTransfer` checks the presented `claimToken` against.** Carried to the recipient inside `claimUrl` and never returned — the sender reading their transfer must not be able to claim it on the recipient's behalf.\n"
   },
   "offeredAt": {
    "type": "string",
    "format": "date-time"
   },
   "claimedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "An unclaimed transfer expires and the tickets return. A transfer to a mistyped address must not strand a ticket somewhere nobody can reach.\n"
   }
  }
 }
}
```
