# Partner Portal

> **One working file for the whole app** (decided 30 September): `return/Partner Portal.dc.html` in this folder. It starts from the B2B option the client picks (`../../B2B-OPTIONS/return/B2B-option-A.dc.html` or `-B`), and every batch below adds its screens to that one file.

The seventh app (decided 30 September): the partner and reseller portal (P10). Before the client picks, the two options are drawn in [`B2B-OPTIONS/`](../../B2B-OPTIONS/BRIEF.md).

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

## P10: partner web

**What it is.** The reseller portal. Hotels, travel agents and other partners sell the venue's tickets at partner prices, on credit.

**Who uses it.** Partner staff (PTR-001 to PTR-021) and TICVAI's partner team (PTR-022 to PTR-051, the workshop boards WS21 to WS23).

## Reference design to match

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for Option A, the POS-style portal.
- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: for Option B, the website-style portal.

Open the file and match it. Do not describe it in words.

## Where it stands

- **51 screens.** 0 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

**Draw the two options first** ([`B2B-OPTIONS/`](../../B2B-OPTIONS/BRIEF.md)). The client picks one after review (MoM 29 September, section 3). The P10 batches below wait for that choice, because the shell and the sell screens change with it. The workshop batches WS21 to WS23 are TICVAI's internal partner screens and do not depend on it.

**Added once the option is finalised:** the partner cash drawer (Option A only), sent-ticket history, and an "opened" status on sent tickets have no operation yet. Draw them greyed out; see [`ADD-ON-FINALISE.md`](../../B2B-OPTIONS/ADD-ON-FINALISE.md).

## Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P10-booking-quotes-01`](../../P10-booking-quotes-01/) | P10 · Booking & Quotes | 4 | to draw |  |
| [`P10-orders-fulfilment-01`](../../P10-orders-fulfilment-01/) | P10 · Orders & Fulfilment | 2 | to draw |  |
| [`P10-overview-01`](../../P10-overview-01/) | P10 · Overview | 1 | to draw |  |
| [`P10-reports-settlement-01`](../../P10-reports-settlement-01/) | P10 · Reports & Settlement | 3 | to draw |  |
| [`P10-support-01`](../../P10-support-01/) | P10 · Support | 1 | to draw |  |
| [`P10-access-account-01`](../../P10-access-account-01/) | P10 · Access & Account | 5 | to draw | 1 thin |
| [`P10-credit-settlement-01`](../../P10-credit-settlement-01/) | P10 · Credit & Settlement | 2 | to draw | 1 thin |
| [`P10-inventory-pricing-01`](../../P10-inventory-pricing-01/) | P10 · Inventory & Pricing | 3 | to draw | 1 thin |
| [`WS21`](../../WS21/) | B2B, Reseller & OTA Partner Management board 1 | 10 | to draw | 2 thin |
| [`WS22`](../../WS22/) | B2B, Reseller & OTA Partner Management board 2 | 10 | to draw | 2 thin |
| [`WS23`](../../WS23/) | B2B, Reseller & OTA Partner Management board 3 | 10 | to draw | 3 thin |

## Design inputs for P10

<!-- design-inputs:P10 -->
*12 inputs apply to all of P10; 22 more apply to particular modules or screens and are in each batch's BUNDLE.md. Generated from `handoff/design-inputs/mom-design-inputs.yaml`; edit the index, not this block.*

- **Open question.** Qossai proposes a POS-style interface for high-volume resellers (hotels, travel agents) instead of a B2C-style site with login: assigned tickets and partner prices after login, optional cash drawer, sent-ticket history and resend, balance view. Chinmay wireframes both options; decide after review. *(open · MoM 29 Sep 2026, 3. B2B / reseller portal · DI-1023)*
- Qossai: partners may use the TICVAI B2B portal directly with a white-label-style B2B credential (similar to B2C), or integrate via API (preferred for OTAs such as Ticketmaster, Platinum List, BookMyShow). *(agreed · MoM 31 Aug 2026, 4.3 Clarified (integration models) · DI-552)*
- Partner access controls define which actions a partner may perform (e.g. refund, reschedule); the partner portal should only offer the actions granted. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-551)*
- Allam: B2B Portal option — partners without their own platform use a TICVAI B2B portal structured like the B2C store but behind login credentials, showing pre-configured partner pricing and products, with commission tracked the same way. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-134)*
- The POS/tablet application carries TICVAI's own branding and UI direction; the B2C and B2B mobile applications are white-label by design. *(agreed · MoM 31 Jul 2026, 15. Monday UI/UX Session Planning · DI-084)*
- Qossai: the target product is a white-label application supporting both B2C and B2B mobile use cases, built around three to four distinct flows (e.g. admission ticket flow, seat assignment flow). *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-056)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

<!-- /design-inputs:P10 -->

## The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Control, partner web. Read BRIEF.md in the batch folder first, then BUNDLE.md, whose "Screen by screen" section specifies each screen: every input (control, required, default, allowed values, format, error), every output (what is shown and in what format, what each action produces, where the user goes next), every state, the permissions, the requirements, the client's meeting inputs, the tracker items and the references; draw each screen to its block and meet its acceptance checklist; BRIEF.md outranks this prompt. Apply every item in the bundle's "Design inputs from the client meetings" section and the app-wide ones in handoff/design-batches/apps/7-partner-portal/README.md: they are the client's own requirements from the meetings and win over the reference designs where they differ; an open question gets its stated default. Match the look of `sources/designs/TICVAI_POS_Terminal_client_approved.html` and `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`. This is a desktop browser, 1440 wide; Option A is a till-like sell screen, Option B a storefront with a partner login. Save one fragment per screen to wireframes/incoming/<BATCH ID>/<screen id>.html (lower-case id, root element id="<screen id>", no <html>, <head>, <body> or <script>, over 200 bytes), then add them to the one working file for the whole app, handoff/design-batches/apps/7-partner-portal/return/Partner Portal.dc.html (it starts from the option file the client picked; keep every earlier screen working), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

## When it comes back

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
