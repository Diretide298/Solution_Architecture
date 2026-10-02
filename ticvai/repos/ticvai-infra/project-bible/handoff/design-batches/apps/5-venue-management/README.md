# Venue Management

> **One working file for the whole app** (decided 30 September): `return/TICVAI Venue Management.dc.html` in this folder. Every batch below adds its screens to that one file.

The venue's back office on the web: setup and daily management (P08), the CMS and flow builder (P13), analytics (P16), the support agent console (P12) and the accreditation applicant web (P11).

**Run order:** Block A batches first, in the order each section below lists them. Special folders that belong to this app: [CMS flow builder](../../CMS-FLOW-BUILDER/) (Block A, run first).

Sections: P08, P13, P16, P12, P11

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

## P08: TICVAI Venue Management, web

**What it is.** The venue's back office. Set up products, prices, access, staff, stock and outlets, and see what happened.

**Who uses it.** Venue managers, finance, operations and set-up staff, on a desktop.

### Reference design to match

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

Open the file and match it. Do not describe it in words.

### Where it stands

- **1186 screens.** 66 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

See `../../VENUE-MANAGEMENT.md` for how a batch session runs. **Block A needs the set-up screens first**: the Venue Home hub and the screens a venue fills in before it can sell.

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P08-access-venue-01`](../../P08-access-venue-01/) | P08 · Access & Venue (1 of 3) | 10 | to draw | 5 Block A; changed: BO-005 |
| [`P08-orders-money-01`](../../P08-orders-money-01/) | P08 · Orders & Money (1 of 3) | 10 | to draw | 2 Block A; changed: BO-008 |
| [`P08-orders-money-02`](../../P08-orders-money-02/) | P08 · Orders & Money (2 of 3) | 10 | to draw | 1 Block A; changed: BO-065 |
| [`P08-venue-operations-01`](../../P08-venue-operations-01/) | P08 · Venue Operations (1 of 2) | 10 | to draw | 2 Block A; changed: BO-044 |
| [`P08-access-venue-02`](../../P08-access-venue-02/) | P08 · Access & Venue (2 of 3) | 10 | to draw | 3 Block A; changed: BO-093, BO-094; 1 thin |
| [`P08-guests-marketing-01`](../../P08-guests-marketing-01/) | P08 · Guests & Marketing | 4 | to draw | 1 Block A; changed: BO-091; 1 thin |
| [`P08-people-access-rights-01`](../../P08-people-access-rights-01/) | P08 · People & Access Rights (1 of 2) | 10 | to draw | 3 Block A; changed: BO-053, BO-054, BO-087; 1 thin |
| [`P08-sell-01`](../../P08-sell-01/) | P08 · Sell (1 of 4) | 10 | to draw | 5 Block A; changed: BO-007, BO-011; 1 thin |
| [`P08-stock-supply-01`](../../P08-stock-supply-01/) | P08 · Stock & Supply (1 of 2) | 10 | to draw | 1 Block A; changed: BO-081; 1 thin |
| [`WS156`](../../WS156/) | Resource Management Configuration board 2 | 9 | to draw | 2 Block A; changed: BO-866; 4 thin |
| [`WS161`](../../WS161/) | Resource Management Configuration board 7 | 10 | to draw | 1 Block A; changed: BO-919; 5 thin |
| [`WS10`](../../WS10/) | Access Control board 10 | 10 | to draw | 3 Block A; changed: BO-234, BO-243; 6 thin |
| [`WS162`](../../WS162/) | Resource Management Configuration board 8 | 10 | to draw | 1 Block A; changed: BO-927; 8 thin |
| [`WS138`](../../WS138/) | Marketing CRM Configuration Reference v1.0 board 4 | 10 | to draw | 1 Block A; changed: BO-766; 9 thin |
| [`WS145`](../../WS145/) | Marketing CRM Configuration Reference v1.0 board 11 | 10 | to draw | 1 Block A; changed: BO-839; 9 thin |
| [`WS108`](../../WS108/) | ACCREDITATION board 1 | 10 | to draw | 1 Block A; changed: BO-618; 10 thin |
| [`WS140`](../../WS140/) | Marketing CRM Configuration Reference v1.0 board 6 | 10 | to draw | 1 Block A; changed: BO-785; 10 thin |
| [`P08-orders-money-03`](../../P08-orders-money-03/) | P08 · Orders & Money (3 of 3) | 7 | to draw | 3 Block A |
| [`P08-sell-02`](../../P08-sell-02/) | P08 · Sell (2 of 4) | 10 | to draw | 1 Block A |
| [`P08-sell-03`](../../P08-sell-03/) | P08 · Sell (3 of 4) | 10 | to draw | 2 Block A |
| [`P08-venue-operations-02`](../../P08-venue-operations-02/) | P08 · Venue Operations (2 of 2) | 5 | to draw | 1 Block A |
| [`WS60`](../../WS60/) | Ticket Media   Credential Management board 2 | 10 | to draw | 1 Block A |
| [`P08-food-beverage-01`](../../P08-food-beverage-01/) | P08 · Food & Beverage | 8 | to draw | 2 Block A; 1 thin |
| [`P08-sell-04`](../../P08-sell-04/) | P08 · Sell (4 of 4) | 6 | to draw | 1 Block A; 1 thin |
| [`WS06`](../../WS06/) | Access Control board 6 | 10 | to draw | 1 Block A; 2 thin |
| [`WS05`](../../WS05/) | Access Control board 5 | 10 | to draw | 3 Block A; 3 thin |
| [`WS59`](../../WS59/) | Ticket Media   Credential Management board 1 | 10 | to draw | 1 Block A; 3 thin |
| [`WS82`](../../WS82/) | Game and Ride board 5 | 10 | to draw | 1 Block A; 3 thin |
| [`WS125`](../../WS125/) | Event Management Configuration Backend Structure v1.0 board 1 | 3 | to draw | 1 Block A; 3 thin |
| [`WS155`](../../WS155/) | Resource Management Configuration board 1 | 10 | to draw | 2 Block A; 3 thin |
| [`WS157`](../../WS157/) | Resource Management Configuration board 3 | 10 | to draw | 1 Block A; 3 thin |
| [`WS02`](../../WS02/) | Access Control board 2 | 10 | to draw | 2 Block A; 4 thin |
| [`WS08`](../../WS08/) | Access Control board 8 | 10 | to draw | 1 Block A; 4 thin |
| [`WS03`](../../WS03/) | Access Control board 3 | 10 | to draw | 3 Block A; 5 thin |
| [`WS131`](../../WS131/) | Event Management Configuration Backend Structure v1.0 board 7 | 5 | to draw | 1 Block A; 5 thin |
| [`WS01`](../../WS01/) | Access Control board 1 | 10 | to draw | 1 Block A; 8 thin |
| [`WS144`](../../WS144/) | Marketing CRM Configuration Reference v1.0 board 10 | 10 | to draw | 2 Block A; 8 thin |
| [`WS137`](../../WS137/) | Marketing CRM Configuration Reference v1.0 board 3 | 10 | to draw | 1 Block A; 9 thin |

#### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P08-access-venue-03`](../../P08-access-venue-03/) | P08 · Access & Venue (3 of 3) | 5 | to draw |  |
| [`P08-setup-go-live-01`](../../P08-setup-go-live-01/) | P08 · Setup & Go-Live | 1 | to draw |  |
| [`P08-stock-supply-02`](../../P08-stock-supply-02/) | P08 · Stock & Supply (2 of 2) | 6 | to draw |  |
| [`P08-transport-01`](../../P08-transport-01/) | P08 · Transport | 7 | to draw |  |
| [`WS187`](../../WS187/) | Wallet Configuration Backend Structure v1.0 board 2 | 10 | to draw |  |
| [`P08-people-access-rights-02`](../../P08-people-access-rights-02/) | P08 · People & Access Rights (2 of 2) | 2 | to draw | 1 thin |
| [`WS32`](../../WS32/) | Order   Reservation Management board 2 | 9 | to draw | 1 thin |
| [`WS61`](../../WS61/) | Ticket Media   Credential Management board 3 | 10 | to draw | 1 thin |
| [`WS178`](../../WS178/) | TICVAI Finance Backend Structure Reference v1.0 board 1 | 1 | to draw | 1 thin |
| [`WS179`](../../WS179/) | TICVAI Finance Backend Structure Reference v1.0 board 2 | 1 | to draw | 1 thin |
| [`WS186`](../../WS186/) | Wallet Configuration Backend Structure v1.0 board 1 | 10 | to draw | 1 thin |
| [`WS189`](../../WS189/) | Wallet Configuration Backend Structure v1.0 board 4 | 10 | to draw | 1 thin |
| [`WS191`](../../WS191/) | Wallet Configuration Backend Structure v1.0 board 6 | 10 | to draw | 1 thin |
| [`WS192`](../../WS192/) | Wallet Configuration Backend Structure v1.0 board 7 | 10 | to draw | 1 thin |
| [`WS195`](../../WS195/) | Wallet Configuration Backend Structure v1.0 board 10 | 10 | to draw | 1 thin |
| [`WS29`](../../WS29/) | Membership   Annual Pass Management board 1 | 10 | to draw | 2 thin |
| [`WS30`](../../WS30/) | Membership   Annual Pass Management board 2 | 10 | to draw | 2 thin |
| [`WS33`](../../WS33/) | Order   Reservation Management board 3 | 10 | to draw | 2 thin |
| [`WS133`](../../WS133/) | Event Management Configuration Backend Structure v1.0 board 9 | 2 | to draw | 2 thin |
| [`WS190`](../../WS190/) | Wallet Configuration Backend Structure v1.0 board 5 | 10 | to draw | 2 thin |
| [`WS28`](../../WS28/) | Group Sales   Corporate Booking Management board 2 | 10 | to draw | 3 thin |
| [`WS31`](../../WS31/) | Order   Reservation Management board 1 | 10 | to draw | 3 thin |
| [`WS78`](../../WS78/) | Game and Ride board 1 | 10 | to draw | 3 thin |
| [`WS97`](../../WS97/) | Rental Management board 10 | 10 | to draw | 3 thin |
| [`WS126`](../../WS126/) | Event Management Configuration Backend Structure v1.0 board 2 | 3 | to draw | 3 thin |
| [`WS127`](../../WS127/) | Event Management Configuration Backend Structure v1.0 board 3 | 3 | to draw | 3 thin |
| [`WS128`](../../WS128/) | Event Management Configuration Backend Structure v1.0 board 4 | 3 | to draw | 3 thin |
| [`WS159`](../../WS159/) | Resource Management Configuration board 5 | 10 | to draw | 3 thin |
| [`WS160`](../../WS160/) | Resource Management Configuration board 6 | 10 | to draw | 3 thin |
| [`WS188`](../../WS188/) | Wallet Configuration Backend Structure v1.0 board 3 | 10 | to draw | 3 thin |
| [`WS193`](../../WS193/) | Wallet Configuration Backend Structure v1.0 board 8 | 10 | to draw | 3 thin |
| [`WS11`](../../WS11/) | Access Control board 11 | 10 | to draw | 4 thin |
| [`WS27`](../../WS27/) | Group Sales   Corporate Booking Management board 1 | 10 | to draw | 4 thin |
| [`WS79`](../../WS79/) | Game and Ride board 2 | 10 | to draw | 4 thin |
| [`WS129`](../../WS129/) | Event Management Configuration Backend Structure v1.0 board 5 | 4 | to draw | 4 thin |
| [`WS132`](../../WS132/) | Event Management Configuration Backend Structure v1.0 board 8 | 4 | to draw | 4 thin |
| [`WS164`](../../WS164/) | Resource Management Configuration board 10 | 10 | to draw | 4 thin |
| [`WS85`](../../WS85/) | Game and Ride board 8 | 9 | to draw | 5 thin |
| [`WS88`](../../WS88/) | Rental Management board 1 | 10 | to draw | 5 thin |
| [`WS90`](../../WS90/) | Rental Management board 3 | 10 | to draw | 5 thin |
| [`WS91`](../../WS91/) | Rental Management board 4 | 10 | to draw | 5 thin |
| [`WS92`](../../WS92/) | Rental Management board 5 | 10 | to draw | 5 thin |
| [`WS96`](../../WS96/) | Rental Management board 9 | 10 | to draw | 5 thin |
| [`WS158`](../../WS158/) | Resource Management Configuration board 4 | 10 | to draw | 5 thin |
| [`WS163`](../../WS163/) | Resource Management Configuration board 9 | 10 | to draw | 5 thin |
| [`WS194`](../../WS194/) | Wallet Configuration Backend Structure v1.0 board 9 | 10 | to draw | 5 thin |
| [`WS04`](../../WS04/) | Access Control board 4 | 10 | to draw | 6 thin |
| [`WS07`](../../WS07/) | Access Control board 7 | 10 | to draw | 6 thin |
| [`WS12`](../../WS12/) | Access Control board 12 | 10 | to draw | 6 thin |
| [`WS17`](../../WS17/) | Approval Workflows and Governance board 5 | 10 | to draw | 6 thin |
| [`WS80`](../../WS80/) | Game and Ride board 3 | 10 | to draw | 6 thin |
| [`WS83`](../../WS83/) | Game and Ride board 6 | 10 | to draw | 6 thin |
| [`WS89`](../../WS89/) | Rental Management board 2 | 10 | to draw | 6 thin |
| [`WS114`](../../WS114/) | ACCREDITATION board 7 | 10 | to draw | 6 thin |
| [`WS130`](../../WS130/) | Event Management Configuration Backend Structure v1.0 board 6 | 6 | to draw | 6 thin |
| [`WS134`](../../WS134/) | F&B Backend Structure Module Sample Reference v1.0 board 1 | 7 | to draw | 6 thin |
| [`WS167`](../../WS167/) | Seat Management Venue Mapping Reference v1.0 board 3 | 10 | to draw | 6 thin |
| [`WS168`](../../WS168/) | Seat Management Venue Mapping Reference v1.0 board 4 | 10 | to draw | 6 thin |
| [`WS175`](../../WS175/) | Seat Management Venue Mapping Reference v1.0 board 11 | 10 | to draw | 6 thin |
| [`WS09`](../../WS09/) | Access Control board 9 | 10 | to draw | 7 thin |
| [`WS81`](../../WS81/) | Game and Ride board 4 | 10 | to draw | 7 thin |
| [`WS84`](../../WS84/) | Game and Ride board 7 | 10 | to draw | 7 thin |
| [`WS86`](../../WS86/) | Game and Ride board 9 | 10 | to draw | 7 thin |
| [`WS87`](../../WS87/) | Game and Ride board 10 | 10 | to draw | 7 thin |
| [`WS105`](../../WS105/) | Subscription Licensing AI Self Service board 8 | 10 | to draw | 7 thin |
| [`WS113`](../../WS113/) | ACCREDITATION board 6 | 10 | to draw | 7 thin |
| [`WS115`](../../WS115/) | ACCREDITATION board 8 | 10 | to draw | 7 thin |
| [`WS142`](../../WS142/) | Marketing CRM Configuration Reference v1.0 board 8 | 10 | to draw | 7 thin |
| [`WS94`](../../WS94/) | Rental Management board 7 | 10 | to draw | 8 thin |
| [`WS104`](../../WS104/) | Subscription Licensing AI Self Service board 7 | 10 | to draw | 8 thin |
| [`WS110`](../../WS110/) | ACCREDITATION board 3 | 9 | to draw | 8 thin |
| [`WS112`](../../WS112/) | ACCREDITATION board 5 | 10 | to draw | 8 thin |
| [`WS135`](../../WS135/) | Marketing CRM Configuration Reference v1.0 board 1 | 10 | to draw | 8 thin |
| [`WS165`](../../WS165/) | Seat Management Venue Mapping Reference v1.0 board 1 | 10 | to draw | 8 thin |
| [`WS171`](../../WS171/) | Seat Management Venue Mapping Reference v1.0 board 7 | 10 | to draw | 8 thin |
| [`WS173`](../../WS173/) | Seat Management Venue Mapping Reference v1.0 board 9 | 10 | to draw | 8 thin |
| [`WS174`](../../WS174/) | Seat Management Venue Mapping Reference v1.0 board 10 | 8 | to draw | 8 thin |
| [`WS177`](../../WS177/) | Seat Management Venue Mapping Reference v1.0 board 13 | 10 | to draw | 8 thin |
| [`WS13`](../../WS13/) | Approval Workflows and Governance board 1 | 10 | to draw | 9 thin |
| [`WS16`](../../WS16/) | Approval Workflows and Governance board 4 | 10 | to draw | 9 thin |
| [`WS93`](../../WS93/) | Rental Management board 6 | 10 | to draw | 9 thin |
| [`WS95`](../../WS95/) | Rental Management board 8 | 10 | to draw | 9 thin |
| [`WS109`](../../WS109/) | ACCREDITATION board 2 | 10 | to draw | 9 thin |
| [`WS111`](../../WS111/) | ACCREDITATION board 4 | 9 | to draw | 9 thin |
| [`WS141`](../../WS141/) | Marketing CRM Configuration Reference v1.0 board 7 | 10 | to draw | 9 thin |
| [`WS172`](../../WS172/) | Seat Management Venue Mapping Reference v1.0 board 8 | 10 | to draw | 9 thin |
| [`WS176`](../../WS176/) | Seat Management Venue Mapping Reference v1.0 board 12 | 10 | to draw | 9 thin |
| [`WS136`](../../WS136/) | Marketing CRM Configuration Reference v1.0 board 2 | 10 | to draw | 10 thin |
| [`WS139`](../../WS139/) | Marketing CRM Configuration Reference v1.0 board 5 | 10 | to draw | 10 thin |
| [`WS143`](../../WS143/) | Marketing CRM Configuration Reference v1.0 board 9 | 10 | to draw | 10 thin |
| [`WS146`](../../WS146/) | Marketing CRM Configuration Reference v1.0 board 12 | 10 | to draw | 10 thin |
| [`WS166`](../../WS166/) | Seat Management Venue Mapping Reference v1.0 board 2 | 10 | to draw | 10 thin |
| [`WS169`](../../WS169/) | Seat Management Venue Mapping Reference v1.0 board 5 | 10 | to draw | 10 thin |
| [`WS170`](../../WS170/) | Seat Management Venue Mapping Reference v1.0 board 6 | 10 | to draw | 10 thin |

### Design inputs for P08

<!-- design-inputs:P08 -->
*24 inputs apply to all of P08; 509 more apply to particular modules or screens and are in each batch's BUNDLE.md. Generated from `handoff/design-inputs/mom-design-inputs.yaml`; edit the index, not this block.*

- Qossai: configuration screens should consolidate related functionality, potentially merging 3-4 previously separate screens into one, rather than the repetitive one-screen-per-concept pattern of the AI-built reference system. *(agreed · MoM 24 Sep 2026, 4.5 Screen Consolidation Philosophy · DI-987)*
- **Open question.** Open: should AI monitoring live in one centralised AI command dashboard or be distributed as widgets in each functional module's own dashboard? Allam: Softlabs' call; the current proposal is illustrative and Softlabs may propose a better structure. *(open · MoM 18 Sep 2026, 4.4 AI Governance — Risk, Compliance & Continuous Monitoring · DI-936)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- **Open question.** Allam: a user's visibility must be restrictable to specific outlets (an F&B manager of one outlet should not see other outlets' items); also relevant for ticketing/event-specific access. Implementation approach still open. *(open · MoM 18 Aug 2026, 4.6 Role-Based & Outlet-Level Access Control — Open Item · DI-331)*
- Access loads automatically at login on POS and web/admin. A user with one role logs straight in; a user with several roles (e.g. admin, cashier, supervisor, manager) is prompted to choose which role to use. *(agreed · MoM 12 Aug 2026, 4. Multiple Roles per User and Role Switching · DI-249)*
- Back office is role-driven from any device: a finance user signing in from a workstation, laptop or home sees only finance reports and related information. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-248)*
- Built-in help menu with step-by-step tutorials with screenshots for common tasks (e.g. how to sell a ticket at the POS). *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-160)*
- Custom data-capture fields ("data mask") at account, event, extended-ticket and product level: field types text, dropdown, radio, true/false; multi-language labels; validation (min/max length, required/optional); reusable value lists (e.g. country list). Standard fields come out of the box. *(agreed · MoM 7 Aug 2026, 6. Data Mask: Flexible Custom Data Capture · DI-155)*
- Load/traffic dashboards respect the tenancy model: a venue manager sees traffic for their own venue only. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-061)*
- Allam: queue management is built into the system (not third-party) so traffic entering the site can be throttled from the back office itself. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-060)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Documentation deliverable includes user guides and help content; the preview shows a TICVAI Help Center with categories (Getting Started, Events, Tickets, Orders, Payments, Memberships, Access Control, Reports, Integrations), a "Welcome to TICVAI" getting-started article and Quick Links (Create an Event, Set Pricing, Manage Access, View Reports). *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - What We Deliver / Key Deliverables Preview · DI-052)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- AI Assistant panel: a short framing ("Based on last 30 days, here are 3 actions that can improve your revenue") then actionable recommendations, each with its potential impact (e.g. "Increase pricing for VIP seats, +12%") and a chevron, plus "View all recommendations". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - AI Panels · DI-043)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Back-office shell: collapsible left sidebar with Overview, Events, Tickets, Orders, Customers, Memberships, Access Control, POS, Reports, Analytics, AI Assistant, Settings, and the signed-in user (name, role) at the bottom; top bar with global search (Cmd+K), current time and date, Notifications with unread dot, and user menu. *(agreed · Design Vision Book 29 Jul 2026, 04 Dashboard Vision (p4) - navigation shell · DI-030)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*
- Reports and historical searches must still retrieve archived transactions when required; the retention period (e.g. keep 3 of 5+ years live) is configurable per customer, archival manual or automated. *(agreed · MoM 28 Jul 2026, 23. Database Optimisation and Archiving · DI-018)*
- Back-office controls for the waiting room: configurable maximum active users and admission intervals, set per customer and venue. *(agreed · MoM 28 Jul 2026, 19. Auto-scaling and Virtual Waiting Room · DI-017)*

<!-- /design-inputs:P08 -->

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Venue Management, web. Read BRIEF.md in the batch folder first, then BUNDLE.md, whose "Screen by screen" section specifies each screen: every input (control, required, default, allowed values, format, error), every output (what is shown and in what format, what each action produces, where the user goes next), every state, the permissions, the requirements, the client's meeting inputs, the tracker items and the references; draw each screen to its block and meet its acceptance checklist; BRIEF.md outranks this prompt. Apply every item in the bundle's "Design inputs from the client meetings" section and the app-wide ones in handoff/design-batches/apps/5-venue-management/README.md: they are the client's own requirements from the meetings and win over the reference designs where they differ; an open question gets its stated default. Match the look of `sources/designs/TICVAI_POS_Terminal_client_approved.html` and `sources/designs/TICVAI_Mobile.dc.html`. This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/5-venue-management/return/TICVAI Venue Management.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the Venue Management file". Claude Code captures each of that batch's screens from `return/TICVAI Venue Management.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.

## P13: TICVAI Venue Management, CMS section

**What it is.** The white-label CMS. The venue builds and publishes its website and app: brand, pages, booking flows, the mobile app and store publishing.

**Who uses it.** The venue's marketing or digital team, and TICVAI's set-up team on day one.

### Reference design to match

- `sources/designs/guest-rev3-29-september/TICVAI Engine Controls Manual.dc.html`: the look of the controls: every configuration control, laid out and explained.
- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the configuration side panel, for the controls, and the guest booking the live preview shows.
- `sources/designs/TICVAI_White_Label_Guest_App_UI_Reference_1.pdf`: the client's White Label Builder boards.

Open the file and match it. Do not describe it in words.

### Where it stands

- **103 screens.** 25 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

**Start with the flow builder** (`../../CMS-FLOW-BUILDER/`): CMS-101 Help me choose and the new CMS-102 Site Builder, CMS-103 Booking Flows and CMS-104 App Build & Store Publishing, drawn as one flow.

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P13-white-label-03`](../../P13-white-label-03/) | P13 · White Label (3 of 3) | 3 | to draw | 3 Block A; new: CMS-102, CMS-103, CMS-104 |
| [`P13-white-label-01`](../../P13-white-label-01/) | P13 · White Label (1 of 3) | 10 | to draw | 10 Block A; changed: CMS-001, CMS-004, CMS-005, CMS-007, CMS-008, CMS-009, CMS-010; 1 thin |
| [`P13-white-label-02`](../../P13-white-label-02/) | P13 · White Label (2 of 3) | 10 | to draw | 10 Block A; changed: CMS-014, CMS-016, CMS-101; 2 thin |
| [`WS41`](../../WS41/) | Privacy  Consent   Preference Management board 1 | 10 | to draw | 2 Block A; changed: CMS-025, CMS-026; 3 thin |

#### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`WS72`](../../WS72/) | Waiver, Consent & Digital Form Management board 1 | 10 | to draw | 2 thin |
| [`WS42`](../../WS42/) | Privacy  Consent   Preference Management board 2 | 10 | to draw | 3 thin |
| [`WS74`](../../WS74/) | Digital Asset Management DAM board 1 | 10 | to draw | 3 thin |
| [`WS75`](../../WS75/) | Digital Asset Management DAM board 2 | 10 | to draw | 3 thin |
| [`WS77`](../../WS77/) | Digital Asset Management DAM board 4 | 10 | to draw | 3 thin |
| [`WS73`](../../WS73/) | Waiver, Consent & Digital Form Management board 2 | 10 | to draw | 4 thin |
| [`WS76`](../../WS76/) | Digital Asset Management DAM board 3 | 10 | to draw | 6 thin |

### Design inputs for P13

<!-- design-inputs:P13 -->
*8 inputs apply to all of P13; 100 more apply to particular modules or screens and are in each batch's BUNDLE.md. Generated from `handoff/design-inputs/mom-design-inputs.yaml`; edit the index, not this block.*

- The config side panel is a reference tool only, not the CMS. The CMS will be step-based and include header/footer, logos and banners. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W12 Config side panel · DI-1014)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- Qossai: build AI-assisted site design/generation into the website builder, keeping site design (header, footer, color, font, layout) separate from content (tickets), with tickets flowing into the site's structure once published. To be explored. *(client request · MoM 3 Aug 2026, 7. AI-Assisted Website Generation · DI-115)*
- Qossai: give clients as much design flexibility as possible within the configurable structure. *(client request · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-114)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

<!-- /design-inputs:P13 -->

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Venue Management, CMS section. Read BRIEF.md in the batch folder first, then BUNDLE.md, whose "Screen by screen" section specifies each screen: every input (control, required, default, allowed values, format, error), every output (what is shown and in what format, what each action produces, where the user goes next), every state, the permissions, the requirements, the client's meeting inputs, the tracker items and the references; draw each screen to its block and meet its acceptance checklist; BRIEF.md outranks this prompt. For every white-label screen, apply handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md: each field shows its allowed values and default, and the live preview shows the output on the guest screen it reaches (the default theme and the alternate tenant theme). Apply every item in the bundle's "Design inputs from the client meetings" section and the app-wide ones in handoff/design-batches/apps/5-venue-management/README.md: they are the client's own requirements from the meetings and win over the reference designs where they differ; an open question gets its stated default. Match the look of `sources/designs/guest-rev3-29-september/TICVAI Engine Controls Manual.dc.html` and `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`. This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of the guest site or app on the right where a screen changes what guests see. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/5-venue-management/return/TICVAI Venue Management.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the Venue Management file". Claude Code captures each of that batch's screens from `return/TICVAI Venue Management.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.

## P16: TICVAI Venue Management, analytics section

**What it is.** Venue analytics. Dashboards and reports across sales, visits, food and retail, with AI explanations.

**Who uses it.** Venue managers and analysts, on a desktop.

### Reference design to match

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

Open the file and match it. Do not describe it in words.

### Where it stands

- **70 screens.** 4 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

ANL-071 is new on 29 September (batch P16-analytics-02).

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`WS66`](../../WS66/) | Unified BI Reporting and AI Analytics Platform board 1 | 9 | to draw | 1 Block A; changed: ANL-019; 2 thin |
| [`WS71`](../../WS71/) | Unified BI Reporting and AI Analytics Platform board 10 | 10 | to draw | 1 Block A; 4 thin |
| [`WS67`](../../WS67/) | Unified BI Reporting and AI Analytics Platform board 2 | 10 | to draw | 2 Block A; 5 thin |

#### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P16-analytics-01`](../../P16-analytics-01/) | P16 · Analytics (1 of 2) | 10 | to draw |  |
| [`P16-analytics-02`](../../P16-analytics-02/) | P16 · Analytics (2 of 2) | 1 | to draw | new: ANL-071 |
| [`WS69`](../../WS69/) | Unified BI Reporting and AI Analytics Platform board 4 | 10 | to draw | 4 thin |
| [`WS68`](../../WS68/) | Unified BI Reporting and AI Analytics Platform board 3 | 10 | to draw | 6 thin |
| [`WS70`](../../WS70/) | Unified BI Reporting and AI Analytics Platform board 9 | 10 | to draw | 7 thin |

### Design inputs for P16

<!-- design-inputs:P16 -->
*14 inputs apply to all of P16; 28 more apply to particular modules or screens and are in each batch's BUNDLE.md. Generated from `handoff/design-inputs/mom-design-inputs.yaml`; edit the index, not this block.*

- One consolidated, permission-based reporting/dashboard area: a user opens "dashboards" once and sees all dashboards their access allows (finance sees finance; a CEO sees sales, admissions, access control), with dashboard settings there too - not duplicated dashboard screens inside each functional module. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-721)*
- Dashboards should refresh near-real-time (seconds) so management can monitor sales continuously rather than wait for periodic or end-of-day refreshes. *(agreed · MoM 8 Sep 2026, 4.6 Real-Time Reporting Architecture · DI-711)*
- Dashboards must be mobile-responsive so management (e.g. a CEO outside the venue) can log in from a smartphone via a URL rather than needing a laptop. *(agreed · MoM 8 Sep 2026, 4.1 Rationale for a Native BI/Reporting Platform · DI-696)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- Back office is role-driven from any device: a finance user signing in from a workstation, laptop or home sees only finance reports and related information. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-248)*
- Load/traffic dashboards respect the tenancy model: a venue manager sees traffic for their own venue only. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-061)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- AI Assistant panel: a short framing ("Based on last 30 days, here are 3 actions that can improve your revenue") then actionable recommendations, each with its potential impact (e.g. "Increase pricing for VIP seats, +12%") and a chevron, plus "View all recommendations". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - AI Panels · DI-043)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*
- Reports and historical searches must still retrieve archived transactions when required; the retention period (e.g. keep 3 of 5+ years live) is configurable per customer, archival manual or automated. *(agreed · MoM 28 Jul 2026, 23. Database Optimisation and Archiving · DI-018)*

<!-- /design-inputs:P16 -->

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Venue Management, analytics section. Read BRIEF.md in the batch folder first, then BUNDLE.md, whose "Screen by screen" section specifies each screen: every input (control, required, default, allowed values, format, error), every output (what is shown and in what format, what each action produces, where the user goes next), every state, the permissions, the requirements, the client's meeting inputs, the tracker items and the references; draw each screen to its block and meet its acceptance checklist; BRIEF.md outranks this prompt. Apply every item in the bundle's "Design inputs from the client meetings" section and the app-wide ones in handoff/design-batches/apps/5-venue-management/README.md: they are the client's own requirements from the meetings and win over the reference designs where they differ; an open question gets its stated default. Match the look of `sources/designs/TICVAI_POS_Terminal_client_approved.html` and `sources/designs/TICVAI_Mobile.dc.html`. This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/5-venue-management/return/TICVAI Venue Management.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the Venue Management file". Claude Code captures each of that batch's screens from `return/TICVAI Venue Management.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.

## P12: TICVAI Venue Management, support section

**What it is.** The support agent console. Conversations, the knowledge base and agent availability.

**Who uses it.** Venue support agents, on a desktop, often handling several chats at once.

### Reference design to match

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for operator density.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

Open the file and match it. Do not describe it in words.

### Where it stands

- **28 screens.** 1 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P12-overview-01`](../../P12-overview-01/) | P12 · Overview | 2 | to draw | 1 Block A |

#### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P12-access-availability-01`](../../P12-access-availability-01/) | P12 · Access & Availability | 2 | to draw |  |
| [`P12-conversations-01`](../../P12-conversations-01/) | P12 · Conversations | 2 | to draw |  |
| [`P12-knowledge-responses-01`](../../P12-knowledge-responses-01/) | P12 · Knowledge & Responses | 2 | to draw | 1 thin |
| [`WS25`](../../WS25/) | Customer Service board 1 | 10 | to draw | 3 thin |
| [`WS26`](../../WS26/) | Customer Service board 2 | 10 | to draw | 4 thin |

### Design inputs for P12

<!-- design-inputs:P12 -->
*7 inputs apply to all of P12; 17 more apply to particular modules or screens and are in each batch's BUNDLE.md. Generated from `handoff/design-inputs/mom-design-inputs.yaml`; edit the index, not this block.*

- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- Client support staff log into TICVAI to view and respond to their own tickets/chats (keeps a full audit trail); adapters to clients' own support systems are phase two. *(agreed · MoM 12 Aug 2026, 10. Customer Support / Chat Integration Approach · DI-257)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

<!-- /design-inputs:P12 -->

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Venue Management, support section. Read BRIEF.md in the batch folder first, then BUNDLE.md, whose "Screen by screen" section specifies each screen: every input (control, required, default, allowed values, format, error), every output (what is shown and in what format, what each action produces, where the user goes next), every state, the permissions, the requirements, the client's meeting inputs, the tracker items and the references; draw each screen to its block and meet its acceptance checklist; BRIEF.md outranks this prompt. Apply every item in the bundle's "Design inputs from the client meetings" section and the app-wide ones in handoff/design-batches/apps/5-venue-management/README.md: they are the client's own requirements from the meetings and win over the reference designs where they differ; an open question gets its stated default. Match the look of `sources/designs/TICVAI_POS_Terminal_client_approved.html` and `sources/designs/TICVAI_Mobile.dc.html`. This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/5-venue-management/return/TICVAI Venue Management.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the Venue Management file". Claude Code captures each of that batch's screens from `return/TICVAI Venue Management.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.

## P11: TICVAI Control, accreditation web

**What it is.** The public accreditation portal. Media, staff and suppliers apply for event credentials; reviewers decide.

**Who uses it.** Applicants from outside (public) and TICVAI or venue reviewers.

### Reference design to match

- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the newest client-approved public look, for forms and finish.
- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for the reviewer screens' density.

Open the file and match it. Do not describe it in words.

### Where it stands

- **8 screens.** 0 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P11-applicant-journey-01`](../../P11-applicant-journey-01/) | P11 · Applicant Journey | 5 | to draw |  |
| [`P11-reviewer-internal-01`](../../P11-reviewer-internal-01/) | P11 · Reviewer (Internal) | 3 | to draw |  |

### Design inputs for P11

<!-- design-inputs:P11 -->
*8 inputs apply to all of P11; 10 more apply to particular modules or screens and are in each batch's BUNDLE.md. Generated from `handoff/design-inputs/mom-design-inputs.yaml`; edit the index, not this block.*

- The web portal is the primary channel for accreditation; the mobile app is a secondary route for individual applicants. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-693)*
- Accreditation is primarily completed in the web portal (document upload and photo checks suit a larger screen); the same submission is also available in the guest mobile app as a secondary option for individuals. *(agreed · MoM 7 Sep 2026, 4.8 Accreditation Channel Placement & API Access · DI-666)*
- Bulk: a company with many members (e.g. 1,000) gets an Excel template to submit all details and documents at once; each imported record still goes through profile, documents and approval. *(client request · MoM 7 Sep 2026, 4.7 Notifications, Bulk Operations & Analytics · DI-664)*
- A main account holder (company/agent) sees the status of every application under their organisation (approved, rejected, requires resubmission), whether the credential is collected physically or sent as a soft copy by email. *(client request · MoM 7 Sep 2026, 4.4 Accreditation Profile, Identity Verification & Duplicate Prevention · DI-660)*
- The venue creates a partner/company account (main or sub-accounts) whose users log in and submit accreditation for their members; entry can be done by the end user or by the admin team on their behalf. *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-655)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

<!-- /design-inputs:P11 -->

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Control, accreditation web. Read BRIEF.md in the batch folder first, then BUNDLE.md, whose "Screen by screen" section specifies each screen: every input (control, required, default, allowed values, format, error), every output (what is shown and in what format, what each action produces, where the user goes next), every state, the permissions, the requirements, the client's meeting inputs, the tracker items and the references; draw each screen to its block and meet its acceptance checklist; BRIEF.md outranks this prompt. Apply every item in the bundle's "Design inputs from the client meetings" section and the app-wide ones in handoff/design-batches/apps/5-venue-management/README.md: they are the client's own requirements from the meetings and win over the reference designs where they differ; an open question gets its stated default. Match the look of `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html` and `sources/designs/TICVAI_POS_Terminal_client_approved.html`. This is a public web form flow, 1440 desktop and 390 phone widths; reviewer screens as a desktop back office. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/5-venue-management/return/TICVAI Venue Management.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the Venue Management file". Claude Code captures each of that batch's screens from `return/TICVAI Venue Management.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
