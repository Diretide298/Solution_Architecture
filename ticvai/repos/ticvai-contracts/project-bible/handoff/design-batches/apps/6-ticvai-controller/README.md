# TICVAI main controller

> **One working file for the whole app** (decided 30 September): `return/TICVAI Main Controller.dc.html` in this folder. Every batch below adds its screens to that one file.

TICVAI's own console for running the platform (P09), with tenant sign-up and purchase (P17) and the developer portal (P14).

**Run order:** Block A batches first, in the order each section below lists them. Special folders that belong to this app: none.

Sections: P09, P17, P14

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

## P09: TICVAI Control, web

**What it is.** TICVAI's own console. Tenants, licences, releases, security, platform health and the AI set-up.

**Who uses it.** TICVAI platform staff, on a desktop.

### Reference design to match

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

Open the file and match it. Do not describe it in words.

### Where it stands

- **676 screens.** 44 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P09-ai-01`](../../P09-ai-01/) | P09 · AI | 1 | to draw | 1 Block A; changed: ADM-037 |
| [`WS36`](../../WS36/) | Pricing   Revenue Management board 3 | 10 | to draw | 3 Block A; changed: ADM-069, ADM-077; 1 thin |
| [`WS151`](../../WS151/) | Payment Payment Orchestration board 5 | 10 | to draw | 1 Block A; changed: ADM-603; 2 thin |
| [`WS124`](../../WS124/) | AI Governance board 4 | 10 | to draw | 2 Block A; changed: ADM-554, ADM-556; 3 thin |
| [`WS18`](../../WS18/) | Approval Workflows and Governance board 6 | 10 | to draw | 1 Block A; changed: ADM-342; 4 thin |
| [`WS122`](../../WS122/) | AI Governance board 2 | 10 | to draw | 1 Block A; changed: ADM-536; 4 thin |
| [`WS121`](../../WS121/) | AI Governance board 1 | 10 | to draw | 5 Block A; changed: ADM-520, ADM-523, ADM-526, ADM-527, ADM-528; 5 thin |
| [`WS19`](../../WS19/) | Approval Workflows and Governance board 7 | 10 | to draw | 1 Block A; changed: ADM-354; 6 thin |
| [`WS119`](../../WS119/) | AI Forecasting and Predictive Intelligence board 1 | 10 | to draw | 1 Block A; changed: ADM-508; 7 thin |
| [`P09-branding-localisation-01`](../../P09-branding-localisation-01/) | P09 · Branding & Localisation | 4 | to draw | 3 Block A |
| [`P09-security-compliance-01`](../../P09-security-compliance-01/) | P09 · Security & Compliance | 2 | to draw | 1 Block A |
| [`P09-tenants-licensing-01`](../../P09-tenants-licensing-01/) | P09 · Tenants & Licensing | 9 | to draw | 2 Block A |
| [`WS34`](../../WS34/) | Pricing   Revenue Management board 1 | 10 | to draw | 4 Block A; 2 thin |
| [`WS38`](../../WS38/) | Pricing   Revenue Management board 5 | 10 | to draw | 3 Block A; 2 thin |
| [`WS49`](../../WS49/) | Promotions   Bundles Management board 5 | 10 | to draw | 3 Block A; 2 thin |
| [`WS48`](../../WS48/) | Promotions   Bundles Management board 4 | 10 | to draw | 4 Block A; 3 thin |
| [`WS148`](../../WS148/) | Payment Payment Orchestration board 2 | 10 | to draw | 1 Block A; 4 thin |
| [`WS46`](../../WS46/) | Promotions   Bundles Management board 2 | 10 | to draw | 1 Block A; 5 thin |
| [`WS53`](../../WS53/) | Promotions   Bundles Management board 9 | 10 | to draw | 1 Block A; 5 thin |
| [`WS47`](../../WS47/) | Promotions   Bundles Management board 3 | 10 | to draw | 2 Block A; 6 thin |
| [`WS51`](../../WS51/) | Promotions   Bundles Management board 7 | 10 | to draw | 1 Block A; 6 thin |
| [`WS102`](../../WS102/) | Subscription Licensing AI Self Service board 5 | 10 | to draw | 1 Block A; 7 thin |
| [`WS43`](../../WS43/) | Product Lifecycle   Catalogue Governance board 1 | 10 | to draw | 1 Block A; 9 thin |

#### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P09-infrastructure-resilienc-01`](../../P09-infrastructure-resilienc-01/) | P09 · Infrastructure & Resilience | 4 | to draw |  |
| [`P09-overview-health-01`](../../P09-overview-health-01/) | P09 · Overview & Health | 5 | to draw |  |
| [`P09-platform-ops-01`](../../P09-platform-ops-01/) | P09 · Platform Ops | 1 | to draw |  |
| [`P09-support-communications-01`](../../P09-support-communications-01/) | P09 · Support & Communications | 2 | to draw |  |
| [`P09-access-identity-01`](../../P09-access-identity-01/) | P09 · Access & Identity | 3 | to draw | 1 thin |
| [`WS62`](../../WS62/) | Ticket Resale Marketplace board 1 | 10 | to draw | 1 thin |
| [`P09-releases-environments-01`](../../P09-releases-environments-01/) | P09 · Releases & Environments | 7 | to draw | 2 thin |
| [`WS40`](../../WS40/) | Pricing   Revenue Management board 7 | 10 | to draw | 2 thin |
| [`WS54`](../../WS54/) | Promotions   Bundles Management board 10 | 10 | to draw | 2 thin |
| [`WS55`](../../WS55/) | Rules  Workflow  Approval   Automation Engine board 1 | 10 | to draw | 2 thin |
| [`WS57`](../../WS57/) | Sales Channel Management board 1 | 10 | to draw | 2 thin |
| [`WS58`](../../WS58/) | Sales Channel Management board 2 | 10 | to draw | 2 thin |
| [`WS63`](../../WS63/) | Ticket Resale Marketplace board 2 | 10 | to draw | 2 thin |
| [`WS98`](../../WS98/) | Subscription Licensing AI Self Service board 1 | 10 | to draw | 2 thin |
| [`WS150`](../../WS150/) | Payment Payment Orchestration board 4 | 10 | to draw | 2 thin |
| [`WS37`](../../WS37/) | Pricing   Revenue Management board 4 | 10 | to draw | 3 thin |
| [`WS45`](../../WS45/) | Promotions   Bundles Management board 1 | 10 | to draw | 3 thin |
| [`WS65`](../../WS65/) | Ticket Upgrade, Exchange & Conversion board 1 | 10 | to draw | 3 thin |
| [`WS147`](../../WS147/) | Payment Payment Orchestration board 1 | 10 | to draw | 3 thin |
| [`WS154`](../../WS154/) | Payment Payment Orchestration board 8 | 10 | to draw | 3 thin |
| [`WS183`](../../WS183/) | Upsell,CrossSellEngine board 4 | 10 | to draw | 3 thin |
| [`WS185`](../../WS185/) | Upsell,CrossSellEngine board 6 | 10 | to draw | 3 thin |
| [`WS24`](../../WS24/) | Communication & Notification Platform Services board 1 | 10 | to draw | 4 thin |
| [`WS35`](../../WS35/) | Pricing   Revenue Management board 2 | 10 | to draw | 4 thin |
| [`WS100`](../../WS100/) | Subscription Licensing AI Self Service board 3 | 10 | to draw | 4 thin |
| [`WS149`](../../WS149/) | Payment Payment Orchestration board 3 | 10 | to draw | 4 thin |
| [`WS44`](../../WS44/) | Product Lifecycle   Catalogue Governance board 2 | 10 | to draw | 5 thin |
| [`WS56`](../../WS56/) | Rules  Workflow  Approval   Automation Engine board 2 | 10 | to draw | 5 thin |
| [`WS116`](../../WS116/) | AI Configuration Assistant board 1 | 10 | to draw | 5 thin |
| [`WS181`](../../WS181/) | Upsell,CrossSellEngine board 2 | 10 | to draw | 5 thin |
| [`WS39`](../../WS39/) | Pricing   Revenue Management board 6 | 10 | to draw | 6 thin |
| [`WS50`](../../WS50/) | Promotions   Bundles Management board 6 | 10 | to draw | 6 thin |
| [`WS52`](../../WS52/) | Promotions   Bundles Management board 8 | 10 | to draw | 6 thin |
| [`WS64`](../../WS64/) | Ticket Resale Marketplace board 3 | 10 | to draw | 6 thin |
| [`WS103`](../../WS103/) | Subscription Licensing AI Self Service board 6 | 9 | to draw | 6 thin |
| [`WS107`](../../WS107/) | Subscription Licensing AI Self Service board 10 | 10 | to draw | 6 thin |
| [`WS118`](../../WS118/) | AI Configuration Assistant board 3 | 10 | to draw | 6 thin |
| [`WS152`](../../WS152/) | Payment Payment Orchestration board 6 | 10 | to draw | 6 thin |
| [`WS153`](../../WS153/) | Payment Payment Orchestration board 7 | 10 | to draw | 6 thin |
| [`WS180`](../../WS180/) | Upsell,CrossSellEngine board 1 | 10 | to draw | 6 thin |
| [`WS14`](../../WS14/) | Approval Workflows and Governance board 2 | 9 | to draw | 7 thin |
| [`WS99`](../../WS99/) | Subscription Licensing AI Self Service board 2 | 10 | to draw | 7 thin |
| [`WS117`](../../WS117/) | AI Configuration Assistant board 2 | 10 | to draw | 7 thin |
| [`WS120`](../../WS120/) | AI Forecasting and Predictive Intelligence board 2 | 10 | to draw | 7 thin |
| [`WS123`](../../WS123/) | AI Governance board 3 | 10 | to draw | 7 thin |
| [`WS182`](../../WS182/) | Upsell,CrossSellEngine board 3 | 10 | to draw | 7 thin |
| [`WS184`](../../WS184/) | Upsell,CrossSellEngine board 5 | 10 | to draw | 7 thin |
| [`WS15`](../../WS15/) | Approval Workflows and Governance board 3 | 10 | to draw | 8 thin |
| [`WS106`](../../WS106/) | Subscription Licensing AI Self Service board 9 | 10 | to draw | 8 thin |
| [`WS20`](../../WS20/) | Approval Workflows and Governance board 8 | 10 | to draw | 9 thin |
| [`WS101`](../../WS101/) | Subscription Licensing AI Self Service board 4 | 10 | to draw | 10 thin |

### Design inputs for P09

<!-- design-inputs:P09 -->
*9 inputs apply to all of P09; 61 more apply to particular modules or screens and are in each batch's BUNDLE.md. Generated from `handoff/design-inputs/mom-design-inputs.yaml`; edit the index, not this block.*

- Portal access exposes TICVAI pricing, so prospects submit contact details and a trade license as proof of a real venue, reviewed and approved by TICVAI before access is granted. *(agreed · MoM 10 Sep 2026, 4.8 Customer Portal Access, Authentication & Verification · DI-827)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

<!-- /design-inputs:P09 -->

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Control, web. Read BRIEF.md in the batch folder first, then BUNDLE.md, whose "Screen by screen" section specifies each screen: every input (control, required, default, allowed values, format, error), every output (what is shown and in what format, what each action produces, where the user goes next), every state, the permissions, the requirements, the client's meeting inputs, the tracker items and the references; draw each screen to its block and meet its acceptance checklist; BRIEF.md outranks this prompt. Apply every item in the bundle's "Design inputs from the client meetings" section and the app-wide ones in handoff/design-batches/apps/6-ticvai-controller/README.md: they are the client's own requirements from the meetings and win over the reference designs where they differ; an open question gets its stated default. Match the look of `sources/designs/TICVAI_POS_Terminal_client_approved.html` and `sources/designs/TICVAI_Mobile.dc.html`. This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/6-ticvai-controller/return/TICVAI Main Controller.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the Main Controller file". Claude Code captures each of that batch's screens from `return/TICVAI Main Controller.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.

## P17: TICVAI Control, sign-up

**What it is.** The public sign-up. A venue business finds out if TICVAI fits, builds a package, buys it and activates it.

**Who uses it.** Prospects: owners and managers of venues, not yet customers.

### Reference design to match

- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the newest client-approved public look, for finish.

Open the file and match it. Do not describe it in words.

### Where it stands

- **24 screens.** 0 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

**Every screen here declares no operation** (`apis: []`). Build from the screen content only; there is no data to seed from a schema.

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P17-onboarding-assessment-01`](../../P17-onboarding-assessment-01/) | P17 · Onboarding & Assessment | 10 | to draw | 7 thin |
| [`P17-package-builder-01`](../../P17-package-builder-01/) | P17 · Package Builder | 7 | to draw | 7 thin |
| [`P17-purchase-activation-01`](../../P17-purchase-activation-01/) | P17 · Purchase & Activation | 7 | to draw | 7 thin |

### Design inputs for P17

<!-- design-inputs:P17 -->
*10 inputs apply to all of P17; 17 more apply to particular modules or screens and are in each batch's BUNDLE.md. Generated from `handoff/design-inputs/mom-design-inputs.yaml`; edit the index, not this block.*

- The TICVAI marketing site should showcase demo versions of each platform (POS, kiosk, mobile app, menu management). *(client request · MoM 29 Sep 2026, 3. B2B / reseller portal · DI-1024)*
- Small/medium venues (e.g. 2 POS, 2 access points, basic B2C site) see pricing, subscribe and start configuring within a few days with no sales involvement; large/enterprise prospects stay sales-assisted (demo, consultative scoping) and enterprise-tier pricing is not exposed through self-service. *(agreed · MoM 10 Sep 2026, 4.9 Sales-Assisted vs. Self-Service Segmentation Philosophy · DI-829)*
- On top of the trade-license review, the applicant confirms access to the submitted domain email (link or OTP, 2FA-style) before portal access. *(agreed · MoM 10 Sep 2026, 4.8 Customer Portal Access, Authentication & Verification · DI-828)*
- Portal access exposes TICVAI pricing, so prospects submit contact details and a trade license as proof of a real venue, reviewed and approved by TICVAI before access is granted. *(agreed · MoM 10 Sep 2026, 4.8 Customer Portal Access, Authentication & Verification · DI-827)*
- Gap (Allam): screens don't show how a prospect logs into a secure portal to view their proposed package; account credentials (user ID and password) are created once onboarding is submitted so the prospect can access and track the proposal. *(client request · MoM 10 Sep 2026, 4.7 Package Builder & Module Marketplace · DI-826)*
- Prospect onboarding: a short questionnaire (venue type, user count, expected annual visitors, modules such as B2C, B2B, seat assignment) via a website/AI-assisted flow; small/medium venues auto-classified and self-configure via AI-assisted setup; enterprise routed to a sales-assisted demo. *(client request · MoM 9 Sep 2026, 4.19 Licensing & Subscription Model - Preliminary Concept · DI-807)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Small-customer self-service subscription flow: select required modules, pay online, enter venue and business details, environment is provisioned automatically, then the customer configures products, tickets, users and venue information and starts using the system. *(client request · MoM 28 Jul 2026, 6. Two Deployment and Commercial Models · DI-011)*

<!-- /design-inputs:P17 -->

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Control, sign-up. Read BRIEF.md in the batch folder first, then BUNDLE.md, whose "Screen by screen" section specifies each screen: every input (control, required, default, allowed values, format, error), every output (what is shown and in what format, what each action produces, where the user goes next), every state, the permissions, the requirements, the client's meeting inputs, the tracker items and the references; draw each screen to its block and meet its acceptance checklist; BRIEF.md outranks this prompt. Apply every item in the bundle's "Design inputs from the client meetings" section and the app-wide ones in handoff/design-batches/apps/6-ticvai-controller/README.md: they are the client's own requirements from the meetings and win over the reference designs where they differ; an open question gets its stated default. Match the look of `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`. This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/6-ticvai-controller/return/TICVAI Main Controller.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the Main Controller file". Claude Code captures each of that batch's screens from `return/TICVAI Main Controller.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.

## P14: TICVAI Control, developer portal

**What it is.** The developer portal. Partners register, get API keys, read the docs and ask for production access.

**Who uses it.** Developers at partner companies.

### Reference design to match

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for density.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish.

Open the file and match it. Do not describe it in words.

### Where it stands

- **8 screens.** 3 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P14-developer-api-01`](../../P14-developer-api-01/) | P14 · Developer & API | 8 | to draw | 3 Block A; changed: DEV-003, DEV-008 |

### Design inputs for P14

<!-- design-inputs:P14 -->
*3 inputs apply to all of P14; 7 more apply to particular modules or screens and are in each batch's BUNDLE.md. Generated from `handoff/design-inputs/mom-design-inputs.yaml`; edit the index, not this block.*

- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

<!-- /design-inputs:P14 -->

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Control, developer portal. Read BRIEF.md in the batch folder first, then BUNDLE.md, whose "Screen by screen" section specifies each screen: every input (control, required, default, allowed values, format, error), every output (what is shown and in what format, what each action produces, where the user goes next), every state, the permissions, the requirements, the client's meeting inputs, the tracker items and the references; draw each screen to its block and meet its acceptance checklist; BRIEF.md outranks this prompt. Apply every item in the bundle's "Design inputs from the client meetings" section and the app-wide ones in handoff/design-batches/apps/6-ticvai-controller/README.md: they are the client's own requirements from the meetings and win over the reference designs where they differ; an open question gets its stated default. Match the look of `sources/designs/TICVAI_POS_Terminal_client_approved.html` and `sources/designs/TICVAI_Mobile.dc.html`. This is a developer portal on a desktop browser, 1440 wide, with a docs-style left navigation. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/6-ticvai-controller/return/TICVAI Main Controller.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the Main Controller file". Claude Code captures each of that batch's screens from `return/TICVAI Main Controller.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
