# Guest App

> **One working file for the whole app** (decided 30 September): `return/TICVAI Guest App.dc.html` in this folder. Every batch below adds its screens to that one file.

The guest's app on every surface: the website (P01), the mobile app (P02) and the self-service kiosk (P05). One booking engine, three screens sizes, white-labelled per venue.

**Run order:** Block A batches first, in the order each section below lists them. Special folders that belong to this app: none; the marketing-site demos are in [DEMO-SITE](../../DEMO-SITE/).

Sections: P01, P02, P05

## Design inputs from the client meetings

What the client asked for in the meetings, workshops and design reviews. **Apply them**: they are the client's own requirements and win over the reference designs where the two disagree; an open question gets the default it states. Below are the ones for the whole app; each platform section lists its platform-wide ones, and each batch's `BUNDLE.md` carries every input for its platform, modules and screens (section *Design inputs from the client meetings*). The index, and how to add an input: [`handoff/design-inputs/README.md`](../../../design-inputs/README.md).

<!-- design-inputs:global -->
*29 inputs apply to every app. Generated from `handoff/design-inputs/mom-design-inputs.yaml`; edit the index, not this block.*

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

<!-- /design-inputs:global -->

## P01: TICVAI Guest, web shell

**What it is.** The venue's own booking website. Guests browse, pick a date and tickets, pay and get their tickets. It is white-labelled: each venue's brand, not TICVAI's.

**Who uses it.** Guests, on a phone or laptop browser. Most arrive from a search or a social link, ready to buy.

### Reference design to match

- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the website. Rev 3 with the 29 September fixes and the 30 September feedback (group booking with a headcount, multi-park counters, surf session tickets, the swim-ability answer, transport stations and departures, popular route cards; `CLIENT-RESPONSE-30SEP.md` beside it). The client approved it for development once W1 to W10 are in.
- `sources/designs/guest-rev3-30-september/TICVAI Visit Planner.dc.html`: the visit planner. WEB-050 Plan Your Visit is this file.

Open the file and match it. Do not describe it in words.

### Where it stands

- **50 screens.** 50 are Block A (the first 35 days of the build, from Monday 5 October).
- **50 have a frame; 49 of those are client-verified** (a capture of the client-approved prototype).

**The 30 September return was captured on 1 October** (viewport 1440 x 900): **11 screens are views in it and now carry its frames**: WEB-005 (the multi-park counters), WEB-006 (a surf session's tickets), WEB-049 (transport, stations filled in and departures listed), the At the venue tabs WEB-036, WEB-039, WEB-040, WEB-041, WEB-042, WEB-043, WEB-046, and **WEB-050 Plan Your Visit, from the Visit Planner, which had no frame**. Do not draw these. The views and proof texts are in `tools/capture-plans/guest-web-v2.json`; the captures, with a manifest, in `wireframes/incoming/P01-web-v2/`. WEB-002, WEB-004 and WEB-007 keep their 29 September captures and the rest their rev 3 (28 September) captures: this return does not change those views.

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P01-discovery-browse-01`](../../P01-discovery-browse-01/) | P01 · Discovery & Browse | 5 | part drawn | 5 Block A; new: WEB-050 |
| [`P01-account-self-service-01`](../../P01-account-self-service-01/) | P01 · Account & Self-Service | 5 | drawn | 5 Block A; changed: WEB-016, WEB-017, WEB-018, WEB-019, WEB-020 |
| [`P01-booking-selection-01`](../../P01-booking-selection-01/) | P01 · Booking & Selection | 7 | drawn | 7 Block A; changed: WEB-005, WEB-006, WEB-007, WEB-008, WEB-047, WEB-048 |
| [`P01-cart-checkout-01`](../../P01-cart-checkout-01/) | P01 · Cart & Checkout | 5 | drawn | 5 Block A; changed: WEB-010, WEB-011, WEB-012 |
| [`P01-membership-loyalty-value-01`](../../P01-membership-loyalty-value-01/) | P01 · Membership, Loyalty & Value | 5 | drawn | 5 Block A; changed: WEB-021, WEB-023, WEB-024, WEB-043 |
| [`P01-transport-01`](../../P01-transport-01/) | P01 · Transport | 1 | drawn | 1 Block A; changed: WEB-049 |
| [`P01-engagement-support-01`](../../P01-engagement-support-01/) | P01 · Engagement & Support | 6 | drawn | 6 Block A; changed: WEB-044; 1 thin |
| [`P01-in-venue-services-01`](../../P01-in-venue-services-01/) | P01 · In-venue Services | 6 | drawn | 6 Block A |
| [`P01-promotions-01`](../../P01-promotions-01/) | P01 · Promotions | 1 | drawn | 1 Block A |
| [`P01-retail-01`](../../P01-retail-01/) | P01 · Retail | 2 | drawn | 2 Block A |
| [`P01-support-01`](../../P01-support-01/) | P01 · Support | 2 | drawn | 2 Block A |
| [`P01-ticketing-01`](../../P01-ticketing-01/) | P01 · Ticketing | 3 | drawn | 3 Block A |
| [`P01-high-demand-access-01`](../../P01-high-demand-access-01/) | P01 · High-Demand Access | 1 | drawn | 1 Block A; 1 thin |
| [`P01-system-states-01`](../../P01-system-states-01/) | P01 · System States | 1 | drawn | 1 Block A; 1 thin |

### Design inputs for P01

<!-- design-inputs:P01 -->
*39 inputs apply to all of P01; 239 more apply to particular modules or screens and are in each batch's BUNDLE.md. Generated from `handoff/design-inputs/mom-design-inputs.yaml`; edit the index, not this block.*

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

<!-- /design-inputs:P01 -->

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Guest, web shell. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Apply every item in the bundle's "Design inputs from the client meetings" section and the app-wide ones in handoff/design-batches/apps/1-guest-app/README.md: they are the client's own requirements from the meetings and win over the reference designs where they differ; an open question gets its stated default. Match the look of `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html` and `sources/designs/guest-rev3-30-september/TICVAI Visit Planner.dc.html`. This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the Guest App file". Claude Code captures each of that batch's screens from `return/TICVAI Guest App.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.

## P02: TICVAI Guest, mobile shell

**What it is.** The venue's own mobile app. Home, Explore, Plan and Tickets tabs, with a Buy tickets button on every screen. It is white-labelled per venue.

**Who uses it.** Guests before and during the visit. They plan the day, buy, show a ticket at the gate and order food in the park.

### Reference design to match

- `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`: Mobile App v4, the newest guest look (29 September, with the 30 September feedback in the booking flows). It replaces the 28 September Mobile v2 build.
- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the booking engine that runs inside the app. Keep both files in the same folder.

Open the file and match it. Do not describe it in words.

### Where it stands

- **77 screens.** 77 are Block A (the first 35 days of the build, from Monday 5 October).
- **77 have a frame; 58 of those are client-verified** (a capture of the client-approved prototype). The other 19 were drawn in the v4 look by Claude Code on 30 September and wait for the client's design reviewer (item 2 below).

**The frames were captures of the 28 September build (Mobile v2).** Mobile App v4 replaced it on 29 September. So:

1. **21 screens are views in v4** (GST-063, GST-012, GST-007, GST-008, GST-049, GST-041, GST-001, GST-002, GST-003, GST-004, GST-006, GST-051, GST-053, GST-054, GST-021, GST-022, GST-038, and the intercity transport screens GST-076, GST-077, GST-078, GST-079). **Done: captured from the 30 September return on 1 October** and re-imported (the first 17 had been captured from the 29 September build on 30 September; the transport four replace their Mobile v2 frames). **GST-021 is now the walking-navigation view**: the 3D map following the route, turn-by-turn above it. Do not draw these. The views and proof texts are in `tools/capture-plans/guest-mobile-v4.json`; the captures, with a manifest, in `wireframes/incoming/P02-mobile-v4/`.
2. **19 changed Block A screens have no v4 view** (GST-059, GST-019, GST-039, GST-042, GST-066, GST-073, GST-048, GST-050, GST-056, GST-058, GST-074, GST-075, GST-009, GST-031, GST-032, GST-052, GST-011, GST-015, GST-036). Drawn in the v4 look by Claude Code on 30 September (`designed`, not client-verified); refine them in the batches below.
3. The other 37 screens keep their Mobile v2 frames for now. Restyle them to v4 when their batch comes round.

**To capture again** (both platforms): `node tools/capture-prototype.mjs tools/capture-plans/guest-mobile-v4.json wireframes/incoming/P02-mobile-v4` and `node tools/capture-prototype.mjs tools/capture-plans/guest-web-v2.json wireframes/incoming/P01-web-v2`, then `python tools/applied/guest-30-september-return.py --apply`.

The manifest counts every P02 batch as drawn, because it counts frames on disk. It cannot see that the frames are one build old. The batches below are exported and current anyway.

**Three changes from the client meeting of 30 September, over the v4 captures.** The v4 views stay the layout; these add to them, on the web twins too (WEB-050, WEB-004).

- **Planner, multi-venue (MoM 4.7, Allam): GST-051, GST-053, GST-054, WEB-050.** In a multi-venue tenant each day is one park (a *Which park each day?* choice after the dates), and a day holds only that park's rides, dining and **retail: shops and kiosks now sit beside meals** as plan stops. A cuisine or shop the park lacks is never filled from another park: the chip says *Not at the parks you chose* before planning, and the day shows a *Not at this park* banner naming the park that has it. Draw the `preferenceNotAtVenue` state.
- **Ride detail video (MoM 4.8, Qossai): GST-004, WEB-004.** The info button reveals the details and plays the video in place. **No loader or loading screen in front of the video**: the poster frame shows while it buffers (`videoBuffering`), and a video that cannot play leaves the poster (`videoUnavailable`). Remove any spinner the v4 capture draws over the video.
- **In-park navigation in 3D (MoM 4.8, ADR-0069): GST-021, GST-038.** A 2D/3D toggle on the map; 3D shows the park model with the walking route on the paths and a live position dot, with turn-by-turn guidance to a chosen point. Draw the `map3dUnavailable` state (no 3D model: the 2D map with the same route and live position, the toggle hidden) and the `weakGps` state (an approximate position ring and *Position approximate*).

**Pending in design: what the 30 September return does not show yet.** These keep their specification and are built from it until a design shows them; the captures above stay the layout.

- **Planner, multi-venue with retail (GST-051, GST-053, GST-054, WEB-050).** The return's planner is still single-park: no *Which park each day?* step, no shops or kiosks as plan stops, no *Any shops you'd like to visit?* choice (its lunch step offers cuisines only), and no `preferenceNotAtVenue` chip or banner.
- **Ride video without a loader (GST-004, WEB-004).** The return's ride detail has no info button that plays a video in place, and no `videoBuffering` or `videoUnavailable` frame. Its only loader is on the app's intro video (*Loading video…* over the splash), which is not GST-004.
- **3D navigation, partly shown (GST-021, GST-038; web WEB-039).** Shown: the app's walking navigation in 3D (route on the paths, live position, turn-by-turn, the camera following the guest), and on the web a *3D view / 2D plan* switch. Not shown: a guest-facing 2D/3D toggle on the app (3D or 2D is a demo setting there), `map3dUnavailable` and `weakGps`.

**Also in the return, a prototype defect to raise with the design side:** on the multi-park flow the ticket's *Read more* panel still prices guests at single-park rates (Adult AED 325) and charges an infant AED 475, while the counters on the page are right (2 park ticket, Adult AED 475, infant free). The capture of WEB-005 shows the page, not the panel.

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P02-discovery-01`](../../P02-discovery-01/) | P02 · Discovery | 1 | drawn | 1 Block A; changed: GST-063 |
| [`P02-engagement-support-02`](../../P02-engagement-support-02/) | P02 · Engagement & Support (2 of 2) | 2 | drawn | 2 Block A; changed: GST-059 |
| [`P02-account-self-service-01`](../../P02-account-self-service-01/) | P02 · Account & Self-Service (1 of 2) | 10 | drawn | 10 Block A; changed: GST-012, GST-019, GST-039, GST-042, GST-066; 1 thin |
| [`P02-account-self-service-02`](../../P02-account-self-service-02/) | P02 · Account & Self-Service (2 of 2) | 4 | drawn | 4 Block A; changed: GST-073; 1 thin |
| [`P02-booking-selection-01`](../../P02-booking-selection-01/) | P02 · Booking & Selection | 10 | drawn | 10 Block A; changed: GST-007, GST-008, GST-048, GST-049, GST-050, GST-056, GST-058, GST-074, GST-075; 1 thin |
| [`P02-cart-checkout-01`](../../P02-cart-checkout-01/) | P02 · Cart & Checkout | 3 | drawn | 3 Block A; changed: GST-009, GST-041; 1 thin |
| [`P02-discovery-browse-01`](../../P02-discovery-browse-01/) | P02 · Discovery & Browse | 7 | drawn | 7 Block A; changed: GST-001, GST-002, GST-003, GST-004, GST-006; 1 thin |
| [`P02-engagement-support-01`](../../P02-engagement-support-01/) | P02 · Engagement & Support (1 of 2) | 10 | drawn | 10 Block A; changed: GST-031, GST-032, GST-051, GST-052, GST-053, GST-054; 2 thin |
| [`P02-in-venue-services-01`](../../P02-in-venue-services-01/) | P02 · In-venue Services | 10 | drawn | 10 Block A; changed: GST-021, GST-022, GST-038; 2 thin |
| [`P02-membership-loyalty-value-01`](../../P02-membership-loyalty-value-01/) | P02 · Membership, Loyalty & Value | 3 | drawn | 3 Block A; changed: GST-011, GST-015, GST-036; 2 thin |
| [`P02-marketing-01`](../../P02-marketing-01/) | P02 · Marketing | 1 | drawn | 1 Block A |
| [`P02-promotions-01`](../../P02-promotions-01/) | P02 · Promotions | 1 | drawn | 1 Block A |
| [`P02-retail-01`](../../P02-retail-01/) | P02 · Retail | 1 | drawn | 1 Block A |
| [`P02-support-01`](../../P02-support-01/) | P02 · Support | 1 | drawn | 1 Block A |
| [`P02-high-demand-access-01`](../../P02-high-demand-access-01/) | P02 · High-Demand Access | 1 | drawn | 1 Block A; 1 thin |
| [`P02-in-venue-experience-01`](../../P02-in-venue-experience-01/) | P02 · In-Venue Experience | 2 | drawn | 2 Block A; 1 thin |
| [`P02-ticketing-01`](../../P02-ticketing-01/) | P02 · Ticketing | 4 | drawn | 4 Block A; 1 thin |
| [`P02-transport-01`](../../P02-transport-01/) | P02 · Transport | 4 | drawn | 4 Block A; 1 thin |
| [`P02-system-states-01`](../../P02-system-states-01/) | P02 · System States | 2 | drawn | 2 Block A; 2 thin |

### Design inputs for P02

<!-- design-inputs:P02 -->
*41 inputs apply to all of P02; 274 more apply to particular modules or screens and are in each batch's BUNDLE.md. Generated from `handoff/design-inputs/mom-design-inputs.yaml`; edit the index, not this block.*

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

<!-- /design-inputs:P02 -->

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Guest, mobile shell. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Apply every item in the bundle's "Design inputs from the client meetings" section and the app-wide ones in handoff/design-batches/apps/1-guest-app/README.md: they are the client's own requirements from the meetings and win over the reference designs where they differ; an open question gets its stated default. Match the look of `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html` and `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`. This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the Guest App file". Claude Code captures each of that batch's screens from `return/TICVAI Guest App.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.

## P05: TICVAI Guest, kiosk shell

**What it is.** The self-service kiosk at the venue entrance. The guest product in a fixed frame, with no keyboard.

**Who uses it.** Guests at the gate who did not buy online. They want a ticket fast and a printed receipt.

### Reference design to match

- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the newest client-approved guest look. The kiosk is the same product, narrower.
- `wireframes/reference/Kiosk Board 1.dc.html`: the client's kiosk board, for layout (and Kiosk Board 2).

Open the file and match it. Do not describe it in words.

### Where it stands

- **17 screens.** 0 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P05-ai-01`](../../P05-ai-01/) | P05 · AI | 1 | to draw |  |
| [`P05-sell-02`](../../P05-sell-02/) | P05 · Sell (2 of 2) | 6 | to draw | 3 thin |
| [`P05-sell-01`](../../P05-sell-01/) | P05 · Sell (1 of 2) | 10 | to draw | 6 thin |

### Design inputs for P05

<!-- design-inputs:P05 -->
*9 inputs apply to all of P05; 11 more apply to particular modules or screens and are in each batch's BUNDLE.md. Generated from `handoff/design-inputs/mom-design-inputs.yaml`; edit the index, not this block.*

- Allam: water-park guests rarely carry phones, so a kiosk at the ride lets a guest scan their wristband to book a queue slot and get a return time, then scan the wristband again to enter. *(agreed · MoM 7 Sep 2026, 4.14 Virtual Queue - Multi-Venue Applicability · DI-677)*
- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*
- Top-up rules set minimum and maximum amounts per transaction; channel/funding-source mapping restricts which payment methods each channel offers (e.g. cash top-up on-site only, not online), so each channel's top-up screen offers only its allowed methods. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-517)*
- Confirmed: a guest always books a product or package — never a resource (a specific room, vehicle or instructor by itself) directly — on every sales channel, including the guest/mobile app; the product's configuration determines which resources are booked behind the scenes. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-502)*
- Kiosks are guest-facing: white-labelled to the client's branding like the guest website, while keeping a kiosk-specific layout. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-298)*
- Ticketing, F&B and retail share one cart and checkout, one unified receipt and one QR/wristband per customer — no separate receipts or wristbands per product line. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-293)*
- A single cart/order must take mixed purchases (e.g. family tickets plus gift vouchers) with one unified checkout and identity capture. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-141)*
- Allam: the cashier design must work consistently across all cashier device types: POS terminals, tablets, iPads and kiosks. *(agreed · MoM 3 Aug 2026, 3. UX Design Approach Discussion · DI-101)*
- Selling a capacity-based product (e.g. seat-assigned tickets) while offline is blocked with a clear notification, never allowed through or silently failing; non-capacity products stay sellable offline. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-074)*

<!-- /design-inputs:P05 -->

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Guest, kiosk shell. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Apply every item in the bundle's "Design inputs from the client meetings" section and the app-wide ones in handoff/design-batches/apps/1-guest-app/README.md: they are the client's own requirements from the meetings and win over the reference designs where they differ; an open question gets its stated default. Match the look of `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html` and `wireframes/reference/Kiosk Board 1.dc.html`. This is a portrait touch kiosk, 1080 x 1920, large touch targets, no keyboard, an attract screen when idle. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the Guest App file". Claude Code captures each of that batch's screens from `return/TICVAI Guest App.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
