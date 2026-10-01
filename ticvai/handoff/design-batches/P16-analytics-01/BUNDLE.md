# P16-analytics-01 — P16 · Analytics (1 of 2)

**10 screens · 25 operations · 56 schemas · 10 permissions**

Platform P16 Venue Analytics · ships as **venue-management** ·
staff audience · web ·
online only

## Who this is for

**staff on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 10 permissions apply here:
  `AI_USE, DEVICE_VIEW, LEDGER_VIEW, MARKETING_MANAGE, MARKETING_VIEW, ORDER_VIEW, PRODUCT_VIEW, REPORT_MANAGE, REPORT_VIEW_VENUE, USER_MANAGE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ANL-001` | Executive Command Center | listDetail | 7 | 2 | — |
| `ANL-002` | Sales, Revenue & Channel | statusTracker | 3 | 1 | — |
| `ANL-003` | Operational Performance | listDetail | 6 | 1 | — |
| `ANL-004` | Product Performance | listDetail | 4 | 1 | — |
| `ANL-005` | Cost, Margin & Profitability | statusTracker | 4 | 1 | — |
| `ANL-006` | Inventory & Waste Intelligence | listDetail | 6 | 1 | — |
| `ANL-007` | Guest & Conversion Intelligence | listDetail | 6 | 2 | — |
| `ANL-008` | Demand Forecasting | statusTracker | 4 | 1 | — |
| `ANL-009` | AI Assistant & Action Center | approvalInbox | 9 | 5 | — |
| `ANL-010` | Suggestions & Advice | configEditor | 2 | 1 | — |

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

### Across P16 Venue Analytics

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

### In P16 · Analytics

- Finance board: revenue by department and cost centre, shift-closing details, and payment gateway reconciliation, shown as bar and pie charts. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-716)*

### Screen by screen

**`ANL-001` Executive Command Center**

- Command centre first section: facility-wide totals for revenue, visitors, transactions and occupancy % (calculated against configured park capacity). *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-698)*
- The platform ships a standard set of default dashboards out of the box, plus the ability for the business to design additional custom dashboards without SQL or programming knowledge. *(agreed · MoM 8 Sep 2026, 4.1 Rationale for a Native BI/Reporting Platform · DI-697)*

**`ANL-002` Sales, Revenue & Channel**

- Sales board: product/attraction performance by sales channel, discounts, upsell/cross-sell results, deferred vs realised revenue, and sales forecast vs target. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-715)*

**`ANL-003` Operational Performance**

- Operations board: access-control metrics - total entries, attendance, exits, per-turnstile breakdowns, and park capacity utilisation. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-717)*

**`ANL-005` Cost, Margin & Profitability**

- Financial reports generated automatically: P&L (revenue per category less cost of sales), balance sheet, trial balance and ledger view, cash flow, revenue and deferred-revenue analytics, site-wise revenue; plus daily/weekly/monthly finance summaries. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-276)*

**`ANL-006` Inventory & Waste Intelligence**

- Retail intelligence shows sales and outlet performance, top-performing stores, demand forecasting (from retail sales history and online ticket booking trends) and target-vs-actual per outlet (e.g. monthly target vs. achieved, with variance). *(client request · MoM 19 Aug 2026, 4.9 Retail Intelligence & Reporting · DI-368)*

**`ANL-007` Guest & Conversion Intelligence**

- CRM board: membership/loyalty visit history; retention/churn section flagging inactive customers (e.g. an annual pass holder with no visit last quarter flagged for follow-up); campaign performance and customer behaviour analytics. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-718)*
- Further command-centre sections: revenue by sales channel; capacity utilisation by attraction/inventory item; top products by channel; conversion rate (site visits to completed purchase, cart abandonment, via Google Analytics); customer, membership and loyalty information. *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-700)*

**`ANL-008` Demand Forecasting**

- Demand forecasts show current sales pace, forecast and remaining opportunity broken down by sales channel; revenue forecasts show drivers and confidence levels. A forecast simulator models a hypothetical change (e.g. a 10% price decrease, reduced operating hours, staffing changes) before it is made. *(client request · MoM 18 Sep 2026, 4.10 AI Forecasting — Attendance, Demand, Revenue & Capacity Forecasting · DI-943)*
- Retail intelligence shows sales and outlet performance, top-performing stores, demand forecasting (from retail sales history and online ticket booking trends) and target-vs-actual per outlet (e.g. monthly target vs. achieved, with variance). *(client request · MoM 19 Aug 2026, 4.9 Retail Intelligence & Reporting · DI-368)*
- Data-dependent forecasting (demand/revenue) cannot be delivered in phase one for lack of history, though its front end, back end and data components can be built. *(agreed · MoM 14 Aug 2026, 1. AI Configuration Assistant — Phase-One Scope · DI-280)*

**`ANL-009` AI Assistant & Action Center**

- The AI assistant answers natural-language business queries (e.g. "what was yesterday's ticketing revenue?") only within the user's role (a CEO sees full revenue, a cashier does not), shows grounded citations naming the policy or document an answer came from, and keeps conversation context ("compare that to this week"). *(client request · MoM 21 Sep 2026, 4.8 Core AI Platform — AI Assistant (Query & Knowledge) · DI-964)*

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ANL-001",
  "name": "Executive Command Center",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/executive-command-center",
   "component": "apps/venue-management-web/src/routes/analytics/ExecutiveCommandCenterDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "isEntryPoint": true,
   "exitTo": [
    "ANL-002",
    "ANL-003",
    "ANL-004",
    "ANL-005",
    "ANL-006",
    "ANL-007",
    "ANL-008",
    "ANL-009",
    "ANL-010",
    "ANL-012",
    "ANL-013",
    "ANL-014",
    "ANL-015",
    "ANL-016",
    "ANL-017",
    "ANL-018",
    "ANL-019",
    "ANL-020",
    "ANL-021",
    "ANL-031",
    "ANL-041",
    "ANL-051",
    "ANL-061"
   ],
   "transitions": [
    {
     "to": "ANL-020",
     "trigger": "Multi-Site & Performance Comparison",
     "provenance": "structural — pack board 1 wiring, 9 September 2026"
    },
    {
     "to": "ANL-061",
     "trigger": "BI & Analytics Administration Command Center",
     "provenance": "structural — pack board 10 wiring, 9 September 2026"
    },
    {
     "to": "ANL-021",
     "trigger": "Dashboard Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "carries": [
      "dashboardId"
     ]
    },
    {
     "to": "ANL-031",
     "trigger": "Report Catalogue & Library",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ANL-041",
     "trigger": "Reporting Governance Command Center",
     "provenance": "structural — pack board 4 wiring, 9 September 2026"
    },
    {
     "to": "ANL-051",
     "trigger": "AI Analytics Command Center",
     "provenance": "structural — pack board 9 wiring, 9 September 2026"
    },
    {
     "to": "ANL-002",
     "trigger": "Sales, Revenue & Channel",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher",
     "carries": [
      "dashboardId",
      "reportId"
     ]
    },
    {
     "to": "ANL-003",
     "trigger": "Operational Performance",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher",
     "carries": [
      "dashboardId",
      "reportId"
     ]
    },
    {
     "to": "ANL-004",
     "trigger": "Product Performance",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher",
     "carries": [
      "dashboardId",
      "reportId"
     ]
    },
    {
     "to": "ANL-005",
     "trigger": "Cost, Margin & Profitability",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher",
     "carries": [
      "dashboardId",
      "reportId"
     ]
    },
    {
     "to": "ANL-006",
     "trigger": "Inventory & Waste Intelligence",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher",
     "carries": [
      "dashboardId",
      "reportId"
     ]
    },
    {
     "to": "ANL-007",
     "trigger": "Guest & Conversion Intelligence",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher",
     "carries": [
      "dashboardId",
      "reportId"
     ]
    },
    {
     "to": "ANL-008",
     "trigger": "Demand Forecasting",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher",
     "carries": [
      "dashboardId"
     ]
    },
    {
     "to": "ANL-009",
     "trigger": "AI Assistant & Action Center",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher",
     "carries": [
      "alertId",
      "reportId"
     ]
    },
    {
     "to": "ANL-010",
     "trigger": "Suggestions & Advice",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher",
     "carries": [
      "suggestionId"
     ]
    },
    {
     "to": "ANL-012",
     "trigger": "Live Operations Dashboard",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-013",
     "trigger": "Revenue Pulse",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-014",
     "trigger": "Attendance & Footfall Intelligence",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-015",
     "trigger": "Capacity & Utilization Monitor",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-016",
     "trigger": "Sales & Channel Performance",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-017",
     "trigger": "Customer, Membership & Loyalty Pulse",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher",
     "carries": [
      "dashboardId"
     ]
    },
    {
     "to": "ANL-018",
     "trigger": "Alerts & Exception Center",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    },
    {
     "to": "ANL-019",
     "trigger": "AI Management Insights",
     "provenance": "structural — ANL-001 is P16's home screen and its exits are its launcher"
    }
   ]
  },
  "notes": "**Built 20 August. Answers 3 board screens**: F&B Executive Command Center; Retail Executive Command Center; Enterprise Frontline Operations Dashboard. **Three board screens, one screen with a domain selector.** F&B, Retail and POS each drew an executive command centre and they differ only in which numbers fill the tiles. **Owns POS board frame(s) POS-6A** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Board repointed 24 August.** This screen pointed at `wireframes/POS Board 6.dc.html#pos-6a` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **`wireframe.status` corrected 25 August.** When these screens were repointed from the client pack to their own board on 24 August, the status stayed `designed` — **which claimed a client had drawn a board this package generated.** `derivedFrom` keeps the pack frame, which is where the design came from; `status` describes the file being pointed at, and those are different facts.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 6.dc.html#fnb-6a",
   "POS Board 6.dc.html#pos-6a",
   "Retail Board 6.dc.html#ret-6a"
  ],
  "pattern": "listDetail",
  "patternReason": "`listAlerts` reads the population and `getDashboard` reads one of them — list, select, act",
  "purpose": "Executive Command Center — across F&B, retail, ticketing and frontline, filtered by domain.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listAlerts",
       "notes": "Sends `?status=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "textField",
       "label": "Severity",
       "operation": "listAlerts",
       "notes": "Sends `?severity=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "textField",
       "label": "Workstation id",
       "operation": "listAlerts",
       "notes": "Sends `?workstationId=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "textField",
       "label": "Shift id",
       "operation": "listAlerts",
       "notes": "Sends `?shiftId=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "textField",
       "label": "Item id",
       "operation": "listAlerts",
       "notes": "Sends `?itemId=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "dataTable",
       "label": "Every alert",
       "bindsTo": "Alert",
       "columns": [
        "Alert.id",
        "Alert.ruleId",
        "Alert.raisedAt",
        "Alert.severity",
        "Alert.status",
        "Alert.observedValue",
        "Alert.threshold",
        "Alert.scopePath",
        "Alert.acknowledgedByPrincipalId",
        "Alert.acknowledgedAt",
        "Alert.resolvedAt",
        "Alert.escalatedAt"
       ],
       "operation": "listAlerts",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "multiSelect",
       "label": "Domain",
       "notes": "**The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching them drift.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "**Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.",
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
       "label": "The selected alert",
       "bindsTo": "Alert",
       "columns": [
        "Alert.id",
        "Alert.ruleId",
        "Alert.ruleName",
        "Alert.metric",
        "Alert.raisedAt",
        "Alert.severity",
        "Alert.status",
        "Alert.observedValue",
        "Alert.threshold",
        "Alert.scopePath",
        "Alert.workstationId",
        "Alert.shiftId",
        "Alert.itemId",
        "Alert.acknowledgedByPrincipalId",
        "Alert.acknowledgedAt",
        "Alert.acknowledgementNote"
       ],
       "operation": "listAlerts",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "detailPanel",
       "label": "The command centre",
       "bindsTo": "CommandCentre",
       "columns": [
        "CommandCentre.modules",
        "CommandCentre.resolvedAt"
       ],
       "operation": "getCommandCentre",
       "provenance": "contract reporting.yaml GET /command-centre"
      },
      {
       "kind": "detailPanel",
       "label": "The dashboard data",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Request suggestion",
       "operation": "requestSuggestion",
       "provenance": "contract ai.yaml POST /ai/suggestions"
      },
      {
       "kind": "secondaryButton",
       "label": "Run report",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tiles render in place; **each resolves on its own** so one slow source does not hold the page.",
   "error": "Could not load. **Trading is unaffected** — this reads and writes nothing.",
   "emptyFirstRun": "**A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing.",
   "emptyNoResults": "Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period.",
   "emptyNoAccess": "You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out."
  },
  "apis": [
   {
    "operationId": "getCommandCentre",
    "contract": "reporting",
    "purpose": "The modules this login is entitled to, and each module's dashboards",
    "trigger": "onLoad",
    "provenance": "command-centre decision, 22 September 2026"
   },
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAlerts",
    "contract": "reporting",
    "purpose": "What is currently raised",
    "trigger": "onLoad"
   },
   {
    "operationId": "requestSuggestion",
    "contract": "ai",
    "purpose": "requestSuggestion",
    "trigger": "onAction",
    "invalidates": [
     "listAlerts"
    ]
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listAlerts"
    ]
   },
   {
    "operationId": "recordDashboardView",
    "contract": "reporting",
    "purpose": "Record that a dashboard was opened — fired once when the dashboard renders; nothing on the screen waits for it.",
    "trigger": "background"
   },
   {
    "operationId": "listAiInsights",
    "contract": "ai",
    "purpose": "Insights and anomalies",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "domain",
     "from": "session",
     "optional": true
    },
    {
     "name": "dashboardId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries them, and from the last view where it does not.",
   "preloaded": [
    "Alert.id",
    "Alert.ruleId",
    "Alert.ruleName",
    "Alert.metric",
    "Alert.raisedAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-001",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn as POS-6A in the client POS pack.** The pack's frame is the specification — it carries operations, states, entry params and exits, and it is better specified than anything derived from the screen file.",
   "derivedFrom": "wireframes/POS Board 6.dc.html#pos-6a"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "purposeNote": "Provide senior management with an immediate consolidated view of overall organizational performance.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf, page 3 §The system shall display"
   }
  ],
  "overlays": [
   {
    "id": "formRequestSuggestion",
    "component": "modal",
    "trigger": "Request suggestion",
    "body": "**Collects what `requestSuggestion` sends before it is called.** Required: `kind`. Optional: `subjectRef`, `horizon`, `context`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Request suggestion",
     "operation": "requestSuggestion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "subjectRef",
      "horizon",
      "context"
     ]
    },
    "provenance": "contract ai.yaml POST /ai/suggestions"
   },
   {
    "id": "formRunReport",
    "component": "modal",
    "trigger": "Run report",
    "body": "**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RunReportRequest",
    "confirm": {
     "label": "Run report",
     "operation": "runReport"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "parameters",
      "venueId",
      "dateFrom",
      "dateTo",
      "forceAsync"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
   }
  ],
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-002",
  "name": "Sales, Revenue & Channel",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/sales-revenue-channel",
   "component": "apps/venue-management-web/src/routes/analytics/SalesRevenueChannelDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001"
   ],
   "exitTo": [
    "ANL-001"
   ],
   "inferred": false,
   "notes": "**Returns to ANL-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "carries": [
      "dashboardId",
      "reportId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, reportId and ANL-002 holds dashboardId, reportId, so an edge into it carries them"
    }
   ]
  },
  "notes": "**Built 20 August. Answers 2 board screens**: Sales, Revenue & Channel Analytics; Sales, Revenue & Channel Analytics. **The same screen twice in the client set, word for word.** Revenue by channel is revenue by channel whether the line is a burger or a t-shirt. **Board repointed 24 August.** This screen pointed at `wireframes/Retail Board 6.dc.html#ret-6l` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 6.dc.html#fnb-6b",
   "Retail Board 6.dc.html#ret-6l"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getDashboard` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Sales, Revenue & Channel — across F&B, retail, ticketing and frontline, filtered by domain.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The dashboard data",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      },
      {
       "kind": "multiSelect",
       "label": "Domain",
       "notes": "**The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching them drift.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "**Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run report",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tiles render in place; **each resolves on its own** so one slow source does not hold the page.",
   "error": "Could not load. **Trading is unaffected** — this reads and writes nothing.",
   "emptyFirstRun": "**A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing.",
   "emptyNoResults": "Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period.",
   "emptyNoAccess": "You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out."
  },
  "apis": [
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction"
   },
   {
    "operationId": "recordDashboardView",
    "contract": "reporting",
    "purpose": "Record that a dashboard was opened — fired once when the dashboard renders; nothing on the screen waits for it.",
    "trigger": "background"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "domain",
     "from": "session",
     "optional": true
    },
    {
     "name": "dashboardId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries them, and from the last view where it does not."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-002",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn as RET-6L in the client Retail pack.**",
   "derivedFrom": "wireframes/Retail Board 6.dc.html#ret-6l"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formRunReport",
    "component": "modal",
    "trigger": "Run report",
    "body": "**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RunReportRequest",
    "confirm": {
     "label": "Run report",
     "operation": "runReport"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "parameters",
      "venueId",
      "dateFrom",
      "dateTo",
      "forceAsync"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
   }
  ],
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-003",
  "name": "Operational Performance",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/operational-performance",
   "component": "apps/venue-management-web/src/routes/analytics/OperationalPerformanceDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001"
   ],
   "exitTo": [
    "ANL-001"
   ],
   "inferred": false,
   "notes": "**Returns to ANL-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "carries": [
      "dashboardId",
      "reportId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, reportId and ANL-003 holds dashboardId, reportId, so an edge into it carries them"
    }
   ]
  },
  "notes": "**Built 20 August. Answers 4 board screens**: Outlet, Service & Guest Performance; Store & Operational Performance; Venue Operations Dashboard and 1 more. **Four board screens.** Outlet, store, venue and department are the same question at four levels of `scope_path` — which is a filter, not four screens. **Owns POS board frame(s) POS-6B, POS-6C, POS-6D** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Board repointed 24 August.** This screen pointed at `wireframes/POS Board 6.dc.html#pos-6b` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4k",
   "FnB Board 6.dc.html#fnb-6c",
   "FnB Board 6.dc.html#fnb-6g",
   "POS Board 6.dc.html#pos-6b",
   "POS Board 6.dc.html#pos-6c",
   "POS Board 6.dc.html#pos-6d",
   "Retail Board 6.dc.html#ret-6b"
  ],
  "pattern": "listDetail",
  "patternReason": "`listAlerts` reads the population and `getDashboard` reads one of them — list, select, act",
  "purpose": "Operational Performance — across F&B, retail, ticketing and frontline, filtered by domain.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listAlerts",
       "notes": "Sends `?status=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "textField",
       "label": "Severity",
       "operation": "listAlerts",
       "notes": "Sends `?severity=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "textField",
       "label": "Workstation id",
       "operation": "listAlerts",
       "notes": "Sends `?workstationId=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "textField",
       "label": "Shift id",
       "operation": "listAlerts",
       "notes": "Sends `?shiftId=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "textField",
       "label": "Item id",
       "operation": "listAlerts",
       "notes": "Sends `?itemId=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "dataTable",
       "label": "Every alert",
       "bindsTo": "Alert",
       "columns": [
        "Alert.id",
        "Alert.ruleId",
        "Alert.raisedAt",
        "Alert.severity",
        "Alert.status",
        "Alert.observedValue",
        "Alert.threshold",
        "Alert.scopePath",
        "Alert.acknowledgedByPrincipalId",
        "Alert.acknowledgedAt",
        "Alert.resolvedAt",
        "Alert.escalatedAt"
       ],
       "operation": "listAlerts",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "dataTable",
       "label": "Every registered device",
       "bindsTo": "RegisteredDevice",
       "columns": [
        "RegisteredDevice.id",
        "RegisteredDevice.kind",
        "RegisteredDevice.driver",
        "RegisteredDevice.identifier",
        "RegisteredDevice.workstationId",
        "RegisteredDevice.model",
        "RegisteredDevice.pushToken",
        "RegisteredDevice.pushPlatform",
        "RegisteredDevice.pushFailureCount",
        "RegisteredDevice.offlineScope",
        "RegisteredDevice.firmwareVersion",
        "RegisteredDevice.isRequired"
       ],
       "operation": "listDevices",
       "provenance": "contract tenancy.yaml GET /devices"
      },
      {
       "kind": "dataTable",
       "label": "Every principal",
       "bindsTo": "Principal",
       "columns": [
        "Principal.id",
        "Principal.username",
        "Principal.displayName",
        "Principal.isActive",
        "Principal.validFrom",
        "Principal.validTo",
        "Principal.primaryRoleId",
        "Principal.roles",
        "Principal.lastLoginAt"
       ],
       "operation": "listPrincipals",
       "provenance": "contract identity.yaml GET /principals"
      },
      {
       "kind": "multiSelect",
       "label": "Domain",
       "notes": "**The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching them drift.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "**Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.",
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
       "label": "The selected alert",
       "bindsTo": "Alert",
       "columns": [
        "Alert.id",
        "Alert.ruleId",
        "Alert.ruleName",
        "Alert.metric",
        "Alert.raisedAt",
        "Alert.severity",
        "Alert.status",
        "Alert.observedValue",
        "Alert.threshold",
        "Alert.scopePath",
        "Alert.workstationId",
        "Alert.shiftId",
        "Alert.itemId",
        "Alert.acknowledgedByPrincipalId",
        "Alert.acknowledgedAt",
        "Alert.acknowledgementNote"
       ],
       "operation": "listAlerts",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "detailPanel",
       "label": "The dashboard data",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run report",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tiles render in place; **each resolves on its own** so one slow source does not hold the page.",
   "error": "Could not load. **Trading is unaffected** — this reads and writes nothing.",
   "emptyFirstRun": "**A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing.",
   "emptyNoResults": "Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period.",
   "emptyNoAccess": "You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out."
  },
  "apis": [
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listAlerts"
    ]
   },
   {
    "operationId": "listAlerts",
    "contract": "reporting",
    "purpose": "What is currently raised",
    "trigger": "onLoad"
   },
   {
    "operationId": "listDevices",
    "contract": "tenancy",
    "purpose": "List registered devices",
    "trigger": "onLoad"
   },
   {
    "operationId": "listPrincipals",
    "contract": "identity",
    "purpose": "List principals",
    "trigger": "onLoad"
   },
   {
    "operationId": "recordDashboardView",
    "contract": "reporting",
    "purpose": "Record that a dashboard was opened — fired once when the dashboard renders; nothing on the screen waits for it.",
    "trigger": "background"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "domain",
     "from": "session",
     "optional": true
    },
    {
     "name": "dashboardId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries them, and from the last view where it does not.",
   "preloaded": [
    "Alert.id",
    "Alert.ruleId",
    "Alert.ruleName",
    "Alert.metric",
    "Alert.raisedAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-003",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn as POS-6B, POS-6C, POS-6D in the client POS pack.** The pack's frame is the specification — it carries operations, states, entry params and exits, and it is better specified than anything derived from the screen file.",
   "derivedFrom": "wireframes/POS Board 6.dc.html#pos-6b"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formRunReport",
    "component": "modal",
    "trigger": "Run report",
    "body": "**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RunReportRequest",
    "confirm": {
     "label": "Run report",
     "operation": "runReport"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "parameters",
      "venueId",
      "dateFrom",
      "dateTo",
      "forceAsync"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
   }
  ],
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-004",
  "name": "Product Performance",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/product-performance",
   "component": "apps/venue-management-web/src/routes/analytics/ProductPerformanceDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001",
    "ANL-007"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-006"
   ],
   "inferred": false,
   "notes": "**Returns to ANL-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "carries": [
      "dashboardId",
      "reportId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, reportId and ANL-004 holds dashboardId, reportId, so an edge into it carries them"
    },
    {
     "to": "ANL-006",
     "trigger": "Inventory & Waste Intelligence",
     "provenance": "flow F82 step 3→4",
     "carries": [
      "dashboardId",
      "reportId"
     ]
    }
   ]
  },
  "notes": "**Built 20 August. Answers 2 board screens**: Product Performance & Menu Engineering; Product, SKU & Merchandise Performance. **Menu engineering and SKU performance are one analysis.** Both rank products by margin against volume; only the vocabulary differs. **Board repointed 24 August.** This screen pointed at `wireframes/Retail Board 6.dc.html#ret-6c` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 6.dc.html#fnb-6d",
   "Retail Board 6.dc.html#ret-6c"
  ],
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getDashboard` reads one of them — list, select, act",
  "purpose": "Product Performance — across F&B, retail, ticketing and frontline, filtered by domain.",
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
       "operation": "listProducts",
       "notes": "Sends `?venueId=` to `listProducts`.",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "textField",
       "label": "Kind",
       "operation": "listProducts",
       "notes": "Sends `?kind=` to `listProducts`.",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "toggle",
       "label": "Is sellable",
       "operation": "listProducts",
       "notes": "Sends `?isSellable=` to `listProducts`.",
       "provenance": "contract catalogue.yaml GET /products"
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
      },
      {
       "kind": "multiSelect",
       "label": "Domain",
       "notes": "**The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching them drift.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "**Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.",
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
       "label": "The selected product",
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
        "Product.onSaleTo",
        "Product.categoryId",
        "Product.lifecycleState",
        "Product.isSellable",
        "Product.isStockTracked"
       ],
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "detailPanel",
       "label": "The dashboard data",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run report",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tiles render in place; **each resolves on its own** so one slow source does not hold the page.",
   "error": "Could not load. **Trading is unaffected** — this reads and writes nothing.",
   "emptyFirstRun": "**A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing.",
   "emptyNoResults": "Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period.",
   "emptyNoAccess": "You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out."
  },
  "apis": [
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   },
   {
    "operationId": "recordDashboardView",
    "contract": "reporting",
    "purpose": "Record that a dashboard was opened — fired once when the dashboard renders; nothing on the screen waits for it.",
    "trigger": "background"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "domain",
     "from": "session",
     "optional": true
    },
    {
     "name": "dashboardId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries them, and from the last view where it does not.",
   "preloaded": [
    "Product.id",
    "Product.code",
    "Product.name",
    "Product.description",
    "Product.kind"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-004",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn as RET-6C in the client Retail pack.**",
   "derivedFrom": "wireframes/Retail Board 6.dc.html#ret-6c"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formRunReport",
    "component": "modal",
    "trigger": "Run report",
    "body": "**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RunReportRequest",
    "confirm": {
     "label": "Run report",
     "operation": "runReport"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "parameters",
      "venueId",
      "dateFrom",
      "dateTo",
      "forceAsync"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
   }
  ],
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-005",
  "name": "Cost, Margin & Profitability",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/cost-margin-profitability",
   "component": "apps/venue-management-web/src/routes/analytics/CostMarginProfitabilityDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-007"
   ],
   "inferred": false,
   "notes": "**Returns to ANL-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "carries": [
      "dashboardId",
      "reportId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, reportId and ANL-005 holds dashboardId, reportId, so an edge into it carries them"
    },
    {
     "to": "ANL-007",
     "trigger": "Guest & Conversion Intelligence",
     "provenance": "flow F82 step 1→2",
     "operation": "getStockValuation",
     "carries": [
      "dashboardId",
      "reportId"
     ]
    }
   ]
  },
  "notes": "**Built 20 August. Answers 2 board screens**: Food Cost, Margin & Profitability Intelligence; Promotion, Pricing & Margin Intelligence. Cost against price against what actually sold. **Board repointed 24 August.** This screen pointed at `wireframes/Retail Board 6.dc.html#ret-6f` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 6.dc.html#fnb-6e",
   "Retail Board 6.dc.html#ret-6f"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getDashboard` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Cost, Margin & Profitability — across F&B, retail, ticketing and frontline, filtered by domain.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The dashboard data",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      },
      {
       "kind": "detailPanel",
       "label": "The stock valuation",
       "bindsTo": "StockValuation",
       "columns": [
        "StockValuation.asAt",
        "StockValuation.total",
        "StockValuation.byLocation",
        "StockValuation.byCategory"
       ],
       "operation": "getStockValuation",
       "provenance": "contract inventory.yaml GET /stock/valuation"
      },
      {
       "kind": "multiSelect",
       "label": "Domain",
       "notes": "**The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching them drift.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "**Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run report",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tiles render in place; **each resolves on its own** so one slow source does not hold the page.",
   "error": "Could not load. **Trading is unaffected** — this reads and writes nothing.",
   "emptyFirstRun": "**A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing.",
   "emptyNoResults": "Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period.",
   "emptyNoAccess": "You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out."
  },
  "apis": [
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction"
   },
   {
    "operationId": "getStockValuation",
    "contract": "inventory",
    "purpose": "Stock value by location and category",
    "trigger": "onLoad"
   },
   {
    "operationId": "recordDashboardView",
    "contract": "reporting",
    "purpose": "Record that a dashboard was opened — fired once when the dashboard renders; nothing on the screen waits for it.",
    "trigger": "background"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "domain",
     "from": "session",
     "optional": true
    },
    {
     "name": "dashboardId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries them, and from the last view where it does not."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-005",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn as RET-6F in the client Retail pack.**",
   "derivedFrom": "wireframes/Retail Board 6.dc.html#ret-6f"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formRunReport",
    "component": "modal",
    "trigger": "Run report",
    "body": "**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RunReportRequest",
    "confirm": {
     "label": "Run report",
     "operation": "runReport"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "parameters",
      "venueId",
      "dateFrom",
      "dateTo",
      "forceAsync"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
   }
  ],
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-006",
  "name": "Inventory & Waste Intelligence",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/inventory-waste-intelligence",
   "component": "apps/venue-management-web/src/routes/analytics/InventoryWasteIntelligenceDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001",
    "ANL-004"
   ],
   "exitTo": [
    "ANL-001"
   ],
   "inferred": false,
   "notes": "**Returns to ANL-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "carries": [
      "dashboardId",
      "reportId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, reportId and ANL-006 holds dashboardId, reportId, so an edge into it carries them"
    },
    {
     "to": "BO-058",
     "trigger": "Reporting Home",
     "provenance": "flow F82 step 4→5",
     "operation": "listExpiringBatches",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "reportId"
     ]
    }
   ]
  },
  "notes": "**Built 20 August. Answers 2 board screens**: Inventory, Waste & Production Intelligence; Inventory, Sell-Through & Stock Intelligence. **Theoretical against actual is the whole analysis** — a recipe says 400 portions, the run says 380, and the gap is waste, theft or a wrong recipe. **Board repointed 24 August.** This screen pointed at `wireframes/Retail Board 6.dc.html#ret-6d` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `Retail Board 6.dc.html` frame `ret-6d`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Inventory &amp; Stock Intelligence* matched at 0.89. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 6.dc.html#fnb-6f",
   "Retail Board 6.dc.html#ret-6d"
  ],
  "pattern": "listDetail",
  "patternReason": "`listExpiringBatches` reads the population and `getDashboard` reads one of them — list, select, act",
  "purpose": "Inventory & Waste Intelligence — across F&B, retail, ticketing and frontline, filtered by domain.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "numberField",
       "label": "Within days",
       "operation": "listExpiringBatches",
       "notes": "Sends `?withinDays=` to `listExpiringBatches`.",
       "provenance": "contract inventory.yaml GET /stock-batches/expiring"
      },
      {
       "kind": "dataTable",
       "label": "Every stock batch",
       "bindsTo": "StockBatch",
       "columns": [
        "StockBatch.id",
        "StockBatch.itemId",
        "StockBatch.locationId",
        "StockBatch.batchCode",
        "StockBatch.lotNumber",
        "StockBatch.quantity",
        "StockBatch.receivedAt",
        "StockBatch.expiresAt",
        "StockBatch.supplierId",
        "StockBatch.status"
       ],
       "operation": "listExpiringBatches",
       "provenance": "contract inventory.yaml GET /stock-batches/expiring"
      },
      {
       "kind": "multiSelect",
       "label": "Domain",
       "notes": "**The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching them drift.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "**Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.",
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
       "label": "The selected stock batch",
       "bindsTo": "StockBatch",
       "columns": [
        "StockBatch.id",
        "StockBatch.itemId",
        "StockBatch.locationId",
        "StockBatch.batchCode",
        "StockBatch.lotNumber",
        "StockBatch.quantity",
        "StockBatch.receivedAt",
        "StockBatch.expiresAt",
        "StockBatch.supplierId",
        "StockBatch.status"
       ],
       "operation": "listExpiringBatches",
       "provenance": "contract inventory.yaml GET /stock-batches/expiring"
      },
      {
       "kind": "detailPanel",
       "label": "The count variance",
       "bindsTo": "CountVariance",
       "columns": [
        "CountVariance.countId",
        "CountVariance.totalVarianceValue",
        "CountVariance.exceptionCount",
        "CountVariance.lines"
       ],
       "operation": "getCountVariance",
       "provenance": "contract inventory.yaml GET /stock-counts/{countId}/variance"
      },
      {
       "kind": "detailPanel",
       "label": "The dashboard data",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run report",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tiles render in place; **each resolves on its own** so one slow source does not hold the page.",
   "error": "Could not load. **Trading is unaffected** — this reads and writes nothing.",
   "emptyFirstRun": "**A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing.",
   "emptyNoResults": "Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period.",
   "emptyNoAccess": "You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out."
  },
  "apis": [
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listExpiringBatches"
    ]
   },
   {
    "operationId": "getCountVariance",
    "contract": "inventory",
    "purpose": "Variance between counted and expected",
    "trigger": "onLoad"
   },
   {
    "operationId": "listExpiringBatches",
    "contract": "inventory",
    "purpose": "What is about to go out of date",
    "trigger": "onLoad"
   },
   {
    "operationId": "recordDashboardView",
    "contract": "reporting",
    "purpose": "Record that a dashboard was opened — fired once when the dashboard renders; nothing on the screen waits for it.",
    "trigger": "background"
   },
   {
    "operationId": "requestSuggestion",
    "contract": "ai",
    "purpose": "Waste-risk suggestion (kind wasteRisk): items at risk with a recommended action",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "domain",
     "from": "session",
     "optional": true
    },
    {
     "name": "countId",
     "from": "deepLink"
    },
    {
     "name": "dashboardId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries them, and from the last view where it does not.",
   "preloaded": [
    "StockBatch.id",
    "StockBatch.itemId",
    "StockBatch.locationId",
    "StockBatch.batchCode",
    "StockBatch.lotNumber"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-006",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 6.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing.",
   "derivedFrom": "wireframes/Retail Board 6.dc.html#ret-6d"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formRunReport",
    "component": "modal",
    "trigger": "Run report",
    "body": "**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RunReportRequest",
    "confirm": {
     "label": "Run report",
     "operation": "runReport"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "parameters",
      "venueId",
      "dateFrom",
      "dateTo",
      "forceAsync"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
   }
  ],
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-007",
  "name": "Guest & Conversion Intelligence",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/guest-conversion-intelligence",
   "component": "apps/venue-management-web/src/routes/analytics/GuestConversionIntelligenceDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001",
    "ANL-005"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-004"
   ],
   "inferred": false,
   "notes": "**Returns to ANL-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "carries": [
      "dashboardId",
      "reportId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, reportId and ANL-007 holds dashboardId, reportId, so an edge into it carries them"
    },
    {
     "to": "ANL-004",
     "trigger": "Product Performance",
     "provenance": "flow F82 step 2→3",
     "carries": [
      "dashboardId",
      "reportId"
     ]
    }
   ]
  },
  "notes": "**Built 20 August. Answers 2 board screens**: Guest, Conversion & Basket Intelligence; Kitchen, Service & Fulfilment Performance. Who bought, what else they nearly bought, and how long they waited. **Retail board operations wired 24 August.** **Board repointed 24 August.** This screen pointed at `wireframes/Retail Board 6.dc.html#ret-6e` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 6.dc.html#ret-6e"
  ],
  "pattern": "listDetail",
  "patternReason": "`listSegments` reads the population and `getDashboard` reads one of them — list, select, act",
  "purpose": "Guest & Conversion Intelligence — across F&B, retail, ticketing and frontline, filtered by domain.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "searchField",
       "label": "Search",
       "operation": "listSegments",
       "notes": "Sends `?search=` to `listSegments`.",
       "provenance": "contract marketing-crm.yaml GET /segments"
      },
      {
       "kind": "dataTable",
       "label": "Every segment",
       "bindsTo": "Segment",
       "columns": [
        "Segment.name",
        "Segment.description",
        "Segment.venueId",
        "Segment.match",
        "Segment.criteria",
        "Segment.excludeSegmentIds",
        "Segment.id",
        "Segment.lastEvaluatedSize",
        "Segment.lastEvaluatedAt"
       ],
       "operation": "listSegments",
       "provenance": "contract marketing-crm.yaml GET /segments"
      },
      {
       "kind": "multiSelect",
       "label": "Domain",
       "notes": "**The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching them drift.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "**Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.",
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
       "label": "The selected segment",
       "bindsTo": "Segment",
       "columns": [
        "Segment.name",
        "Segment.description",
        "Segment.venueId",
        "Segment.match",
        "Segment.criteria",
        "Segment.excludeSegmentIds",
        "Segment.id",
        "Segment.lastEvaluatedSize",
        "Segment.lastEvaluatedAt"
       ],
       "operation": "listSegments",
       "provenance": "contract marketing-crm.yaml GET /segments"
      },
      {
       "kind": "detailPanel",
       "label": "The dashboard data",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run report",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Create segment",
       "operation": "createSegment",
       "provenance": "contract marketing-crm.yaml POST /segments"
      },
      {
       "kind": "secondaryButton",
       "label": "Preview segment",
       "operation": "previewSegment",
       "provenance": "contract marketing-crm.yaml POST /segments/{segmentId}/preview"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tiles render in place; **each resolves on its own** so one slow source does not hold the page.",
   "error": "Could not load. **Trading is unaffected** — this reads and writes nothing.",
   "emptyFirstRun": "**A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing.",
   "emptyNoResults": "Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period.",
   "emptyNoAccess": "You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out."
  },
  "apis": [
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listSegments"
    ]
   },
   {
    "operationId": "listSegments",
    "contract": "marketing-crm",
    "purpose": "List segments",
    "trigger": "onLoad"
   },
   {
    "operationId": "createSegment",
    "contract": "marketing-crm",
    "purpose": "Create a segment",
    "trigger": "onAction",
    "invalidates": [
     "listSegments"
    ]
   },
   {
    "operationId": "previewSegment",
    "contract": "marketing-crm",
    "purpose": "Estimate segment size and reachability",
    "trigger": "onAction",
    "invalidates": [
     "listSegments"
    ]
   },
   {
    "operationId": "recordDashboardView",
    "contract": "reporting",
    "purpose": "Record that a dashboard was opened — fired once when the dashboard renders; nothing on the screen waits for it.",
    "trigger": "background"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "domain",
     "from": "session",
     "optional": true
    },
    {
     "name": "dashboardId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    },
    {
     "name": "segmentId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries them, and from the last view where it does not. A segment opened from the list.",
   "preloaded": [
    "Segment.name",
    "Segment.description",
    "Segment.venueId",
    "Segment.match",
    "Segment.criteria"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-007",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn as RET-6E in the client Retail pack.**",
   "derivedFrom": "wireframes/Retail Board 6.dc.html#ret-6e"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formRunReport",
    "component": "modal",
    "trigger": "Run report",
    "body": "**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RunReportRequest",
    "confirm": {
     "label": "Run report",
     "operation": "runReport"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "parameters",
      "venueId",
      "dateFrom",
      "dateTo",
      "forceAsync"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
   },
   {
    "id": "formCreateSegment",
    "component": "modal",
    "trigger": "Create segment",
    "body": "**Collects what `createSegment` sends before it is called.** Required: `name`, `criteria`. Optional: `description`, `venueId`, `match`, `excludeSegmentIds`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateSegmentRequest",
    "confirm": {
     "label": "Create segment",
     "operation": "createSegment"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "criteria",
      "description",
      "venueId",
      "match",
      "excludeSegmentIds"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /segments"
   }
  ],
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-008",
  "name": "Demand Forecasting",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/demand-forecasting",
   "component": "apps/venue-management-web/src/routes/analytics/DemandForecastingDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001"
   ],
   "exitTo": [
    "ANL-001"
   ],
   "inferred": false,
   "notes": "**Returns to ANL-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "carries": [
      "dashboardId",
      "reportId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, reportId and ANL-008 holds dashboardId, reportId, so an edge into it carries them"
    }
   ]
  },
  "notes": "**Built 20 August. Answers 2 board screens**: Demand Forecasting & Operational Planning; Demand Forecasting & Merchandise Planning. **A forecast is an input to a requisition, not a report.** Its value is that somebody orders differently because of it. **Board repointed 24 August.** This screen pointed at `wireframes/Retail Board 6.dc.html#ret-6g` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 6.dc.html#fnb-6h",
   "Retail Board 6.dc.html#ret-6g"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getDashboard` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Demand Forecasting — across F&B, retail, ticketing and frontline, filtered by domain.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The dashboard data",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      },
      {
       "kind": "multiSelect",
       "label": "Domain",
       "notes": "**The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching them drift.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "**Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Ask reporting question",
       "operation": "askReportingQuestion",
       "provenance": "contract reporting.yaml POST /reports/ask"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tiles render in place; **each resolves on its own** so one slow source does not hold the page.",
   "error": "Could not load. **Trading is unaffected** — this reads and writes nothing.",
   "emptyFirstRun": "**A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing.",
   "emptyNoResults": "Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period.",
   "emptyNoAccess": "You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out."
  },
  "apis": [
   {
    "operationId": "askReportingQuestion",
    "contract": "reporting",
    "purpose": "Natural-language reporting query",
    "trigger": "onAction"
   },
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onLoad"
   },
   {
    "operationId": "recordDashboardView",
    "contract": "reporting",
    "purpose": "Record that a dashboard was opened — fired once when the dashboard renders; nothing on the screen waits for it.",
    "trigger": "background"
   },
   {
    "operationId": "getForecast",
    "contract": "ai",
    "purpose": "Forecast values",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "domain",
     "from": "session",
     "optional": true
    },
    {
     "name": "dashboardId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries them, and from the last view where it does not."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-008",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn as RET-6G in the client Retail pack.**",
   "derivedFrom": "wireframes/Retail Board 6.dc.html#ret-6g"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formAskReportingQuestion",
    "component": "modal",
    "trigger": "Ask reporting question",
    "body": "**Collects what `askReportingQuestion` sends before it is called.** Required: `question`. Optional: `conversationId`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Ask reporting question",
     "operation": "askReportingQuestion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "question",
      "conversationId",
      "venueId"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/ask"
   }
  ],
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-009",
  "name": "AI Assistant & Action Center",
  "module": "Analytics",
  "requiresModule": "analytics",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/ai-assistant-action-center",
   "component": "apps/venue-management-web/src/routes/analytics/AiAssistantActionCenterDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001"
   ],
   "exitTo": [
    "ANL-001"
   ],
   "inferred": false,
   "notes": "**Returns to ANL-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "carries": [
      "reportId"
     ],
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, reportId and ANL-009 holds reportId, so an edge into it carries them"
    },
    {
     "to": "BO-010",
     "trigger": "Promotions & Coupons",
     "provenance": "flow F77 step 3→4",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "reportId"
     ]
    }
   ]
  },
  "notes": "**Built 20 August. Answers 5 board screens**: AI Recommendation, Simulation & Optimization Center; AI Assistant, Alerts & Management Action Center; Transaction & Exception Monitoring and 2 more. **Five board screens, and the collapse is the point.** Every domain drew an AI centre and an alert centre; **an alert nobody can act on from the screen showing it is a notification**, so recommendation and action are one place. **Owns POS board frame(s) POS-6E** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Retail board operations wired 24 August.** **Board repointed 24 August.** This screen pointed at `wireframes/POS Board 6.dc.html#pos-6e` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 5.dc.html#fnb-5k",
   "FnB Board 6.dc.html#fnb-6j",
   "FnB Board 6.dc.html#fnb-6k",
   "POS Board 6.dc.html#pos-6e",
   "Retail Board 5.dc.html#ret-5k",
   "Retail Board 6.dc.html#ret-6k"
  ],
  "pattern": "approvalInbox",
  "patternReason": "`decideProposedAction` decides items that `listAlerts` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "AI Assistant & Action Center — across F&B, retail, ticketing and frontline, filtered by domain.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listAlerts",
       "notes": "Sends `?status=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "textField",
       "label": "Severity",
       "operation": "listAlerts",
       "notes": "Sends `?severity=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "textField",
       "label": "Workstation id",
       "operation": "listAlerts",
       "notes": "Sends `?workstationId=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "textField",
       "label": "Shift id",
       "operation": "listAlerts",
       "notes": "Sends `?shiftId=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "textField",
       "label": "Item id",
       "operation": "listAlerts",
       "notes": "Sends `?itemId=` to `listAlerts`.",
       "provenance": "contract reporting.yaml GET /alerts"
      },
      {
       "kind": "dataTable",
       "label": "Waiting for a decision",
       "bindsTo": "Alert",
       "columns": [
        "Alert.id",
        "Alert.ruleId",
        "Alert.raisedAt",
        "Alert.severity",
        "Alert.status",
        "Alert.observedValue",
        "Alert.threshold",
        "Alert.scopePath",
        "Alert.acknowledgedByPrincipalId",
        "Alert.acknowledgedAt",
        "Alert.resolvedAt",
        "Alert.escalatedAt"
       ],
       "operation": "listAlerts",
       "provenance": "contract reporting.yaml GET /alerts"
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
        "OrderSummary.lineCount",
        "OrderSummary.principalId",
        "OrderSummary.holdLabel",
        "OrderSummary.heldUntil"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "dataTable",
       "label": "Every proposed action",
       "bindsTo": "ProposedAction",
       "columns": [
        "ProposedAction.id",
        "ProposedAction.interactionId",
        "ProposedAction.kind",
        "ProposedAction.targetContract",
        "ProposedAction.targetOperation",
        "ProposedAction.payload",
        "ProposedAction.summary",
        "ProposedAction.status",
        "ProposedAction.approvalLevel",
        "ProposedAction.decidedByPrincipalId",
        "ProposedAction.decisionReason",
        "ProposedAction.proposedAt"
       ],
       "operation": "listProposedActions",
       "notes": "**What a caller sees follows who may decide** (decided 28 September, audit R213 (3)): with `AI_APPROVE`, every open proposal at the scope; with `AI_USE` only, the caller's own proposals, which are the level 1 ones they may approve themselves.",
       "provenance": "contract ai.yaml GET /proposed-actions"
      },
      {
       "kind": "multiSelect",
       "label": "Domain",
       "notes": "**The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching them drift.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "chart",
       "notes": "**Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected alert",
       "bindsTo": "Alert",
       "columns": [
        "Alert.id",
        "Alert.ruleId",
        "Alert.raisedAt",
        "Alert.severity",
        "Alert.status",
        "Alert.observedValue",
        "Alert.threshold",
        "Alert.scopePath",
        "Alert.acknowledgedByPrincipalId",
        "Alert.acknowledgedAt",
        "Alert.resolvedAt",
        "Alert.escalatedAt"
       ],
       "operation": "listAlerts",
       "provenance": "contract reporting.yaml GET /alerts"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Ask reporting question",
       "operation": "askReportingQuestion",
       "provenance": "contract reporting.yaml POST /reports/ask"
      },
      {
       "kind": "secondaryButton",
       "label": "Acknowledge alert",
       "operation": "acknowledgeAlert",
       "provenance": "contract reporting.yaml POST /alerts/{alertId}/acknowledge"
      },
      {
       "kind": "secondaryButton",
       "label": "Run report",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Save alert rule",
       "operation": "setAlertRule",
       "provenance": "contract reporting.yaml PUT /alert-rules"
      },
      {
       "kind": "secondaryButton",
       "label": "Decide proposed action",
       "operation": "decideProposedAction",
       "notes": "Guarded as the contract is (decided 28 September, audit R213 (3)): offered on the caller's own level 1 proposals with `AI_USE`; on a level 2 proposal, or somebody else's, only with `AI_APPROVE`, and never on a level 2 proposal the caller prompted. Hidden rather than disabled where the rule already says no.",
       "provenance": "contract ai.yaml POST /proposed-actions/{actionId}/decide"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Tiles render in place; **each resolves on its own** so one slow source does not hold the page.",
   "error": "Could not load. **Trading is unaffected** — this reads and writes nothing.",
   "emptyFirstRun": "**A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing.",
   "emptyNoResults": "Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period.",
   "emptyNoAccess": "You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out."
  },
  "apis": [
   {
    "operationId": "askReportingQuestion",
    "contract": "reporting",
    "purpose": "Natural-language reporting query",
    "trigger": "onAction",
    "invalidates": [
     "listAlerts"
    ]
   },
   {
    "operationId": "listAlerts",
    "contract": "reporting",
    "purpose": "What is currently raised",
    "trigger": "onLoad"
   },
   {
    "operationId": "acknowledgeAlert",
    "contract": "reporting",
    "purpose": "Take responsibility for it",
    "trigger": "onAction",
    "invalidates": [
     "listAlerts"
    ]
   },
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "List orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listAlerts"
    ]
   },
   {
    "operationId": "setAlertRule",
    "contract": "reporting",
    "purpose": "Raise an alert when a number leaves a range",
    "trigger": "onAction",
    "invalidates": [
     "listAlerts"
    ]
   },
   {
    "operationId": "listProposedActions",
    "contract": "ai",
    "purpose": "What the assistant has proposed and nobody has decided — all of them with AI_APPROVE, the caller's own with AI_USE (audit R213 (3))",
    "trigger": "onLoad"
   },
   {
    "operationId": "decideProposedAction",
    "contract": "ai",
    "purpose": "Approve or reject a proposal — own level 1 with AI_USE, level 2 or another's with AI_APPROVE, never one's own level 2 (audit R213 (3))",
    "trigger": "onAction",
    "invalidates": [
     "listAlerts"
    ]
   },
   {
    "operationId": "getActionPlan",
    "contract": "ai",
    "purpose": "A plan with its steps",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "domain",
     "from": "session",
     "optional": true
    },
    {
     "name": "alertId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    },
    {
     "name": "actionId",
     "from": "deepLink"
    },
    {
     "name": "planId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries them, and from the last view where it does not. A proposed action opened from the queue or an alert.",
   "preloaded": [
    "Alert.id",
    "Alert.ruleId",
    "Alert.raisedAt",
    "Alert.severity",
    "Alert.status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-009",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn as POS-6E in the client POS pack.** The pack's frame is the specification — it carries operations, states, entry params and exits, and it is better specified than anything derived from the screen file.",
   "derivedFrom": "wireframes/POS Board 6.dc.html#pos-6e"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 8 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formAskReportingQuestion",
    "component": "modal",
    "trigger": "Ask reporting question",
    "body": "**Collects what `askReportingQuestion` sends before it is called.** Required: `question`. Optional: `conversationId`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Ask reporting question",
     "operation": "askReportingQuestion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "question",
      "conversationId",
      "venueId"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/ask"
   },
   {
    "id": "formAcknowledgeAlert",
    "component": "modal",
    "trigger": "Acknowledge alert",
    "body": "**Collects what `acknowledgeAlert` sends before it is called.** Nothing in the body is required. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Acknowledge alert",
     "operation": "acknowledgeAlert"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "note"
     ]
    },
    "provenance": "contract reporting.yaml POST /alerts/{alertId}/acknowledge"
   },
   {
    "id": "formRunReport",
    "component": "modal",
    "trigger": "Run report",
    "body": "**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RunReportRequest",
    "confirm": {
     "label": "Run report",
     "operation": "runReport"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "parameters",
      "venueId",
      "dateFrom",
      "dateTo",
      "forceAsync"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
   },
   {
    "id": "formSetAlertRule",
    "component": "modal",
    "trigger": "Save alert rule",
    "body": "**Collects what `setAlertRule` sends before it is called.** Required: `id`, `name`, `metric`, `comparator`, `threshold`, `severity`, `isActive`, `scopePath`. Optional: `thresholdUpper`, `windowMinutes`, `deliverTo`, `recipientRoleIds`, `cooldownMinutes`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AlertRule",
    "confirm": {
     "label": "Save alert rule",
     "operation": "setAlertRule"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "name",
      "metric",
      "comparator",
      "threshold",
      "severity",
      "isActive",
      "scopePath",
      "thresholdUpper",
      "windowMinutes",
      "deliverTo",
      "recipientRoleIds",
      "cooldownMinutes"
     ]
    },
    "provenance": "contract reporting.yaml PUT /alert-rules"
   },
   {
    "id": "formDecideProposedAction",
    "component": "modal",
    "trigger": "Decide proposed action",
    "body": "**Collects what `decideProposedAction` sends before it is called.** Required: `decision`. Optional: `reason` (asked for on a rejection). A refusal is a 403 named by its rule and shown as such (decided 28 September, audit R213 (3)): `approval-level-requires-manager` (level 2 needs a manager holding `AI_APPROVE`), `approver-is-requester` (a level 2 proposal cannot be approved by whoever prompted it), `not-own-proposal` (somebody else's level 1 proposal needs `AI_APPROVE`). An expired or already decided proposal is a 409. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Decide proposed action",
     "operation": "decideProposedAction"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "decision",
      "reason"
     ]
    },
    "provenance": "contract ai.yaml POST /proposed-actions/{actionId}/decide"
   }
  ],
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ANL-010",
  "name": "Suggestions & Advice",
  "module": "Analytics",
  "requiresModule": "ai",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/suggestions",
   "component": "apps/venue-management-web/src/routes/analytics/SuggestionsDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-001"
   ],
   "exitTo": [
    "ANL-001",
    "ANL-071"
   ],
   "inferred": false,
   "notes": "**Returns to ANL-001.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "ANL-001",
     "trigger": "Executive Command Center",
     "provenance": "derived — ANL-001 declares entryState.params dashboardId, reportId and ANL-010 holds none of them. The edge carries nothing: ANL-010 is opened from ANL-001, so this edge is the way back and ANL-001 keeps its own state"
    },
    {
     "to": "ANL-071",
     "trigger": "AI maturity",
     "provenance": "29 September pass (group A) — the stage badge links to the maturity page"
    }
   ]
  },
  "notes": "**Built 24 August.** The client F&B boards drew six suggestion endpoints — price, requisition, replenishment, scenario, SLA, demand plan. **One screen and one operation answer all six**, because a suggestion surface that differs per domain is six screens to change when the model changes. **Owns POS board frame(s) POS-6F** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Board repointed 24 August.** This screen pointed at `wireframes/POS Board 6.dc.html#pos-6f` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.",
  "density": "compact",
  "boardFrames": [
   "POS Board 6.dc.html#pos-6f"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`requestSuggestion`, `recordSuggestionOutcome`) and no read of a population — it is settings, not a list",
  "purpose": "Every open suggestion, what it is based on, and whether the venue took it.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Request suggestion",
       "operation": "requestSuggestion",
       "provenance": "contract ai.yaml POST /ai/suggestions"
      },
      {
       "kind": "secondaryButton",
       "label": "Record suggestion outcome",
       "operation": "recordSuggestionOutcome",
       "provenance": "contract ai.yaml POST /ai/suggestions/{suggestionId}/outcome"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "multiSelect",
       "label": "Kind",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "bindsTo": "Suggestion[]",
       "notes": "**The basis and the stage are on the card, not behind a tap.** Every answer shows a \"Based on\" chip (*your venue profile, UAE calendar, weather, 23 days of your sales*) and a stage badge: Starting, Learning, Established or Trained on your data (29 September, AI functions review). \"Limited historical data\" while the starting pattern carries more than half the weight. Never a bare percentage.",
       "provenance": "carried from the previous definition",
       "operation": "requestSuggestion"
      },
      {
       "kind": "detailPanel",
       "notes": "The explanation in plain words and the inputs it used. **Advice computed from data the manager cannot see is advice they will not trust.**",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Take it",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Do something else",
       "notes": "**Records the outcome either way.** A rejected suggestion is the case the current rule got wrong, which is exactly what a model is trained to beat.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "textField",
       "label": "Kind",
       "operation": "requestSuggestion",
       "notes": "Required.",
       "provenance": "contract ai.yaml POST /ai/suggestions"
      },
      {
       "kind": "textField",
       "label": "Subject ref",
       "operation": "requestSuggestion",
       "provenance": "contract ai.yaml POST /ai/suggestions"
      },
      {
       "kind": "textField",
       "label": "Horizon",
       "operation": "requestSuggestion",
       "provenance": "contract ai.yaml POST /ai/suggestions"
      },
      {
       "kind": "textField",
       "label": "Context",
       "operation": "requestSuggestion",
       "provenance": "contract ai.yaml POST /ai/suggestions"
      },
      {
       "kind": "banner",
       "label": "Missing setting",
       "operation": "requestSuggestion",
       "notes": "Shown only on a 422 `missing-setting`: names the setting (a current cost, a par level, the venue AI profile) and links to the screen that sets it. Little history is never this banner.",
       "provenance": "29 September pass (group A)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Open suggestions, newest first, grouped by kind.",
   "error": "Could not load. **Trading is unaffected** — this advises and does not act.",
   "emptyFirstRun": "**No suggestions asked for yet.** Every kind answers from day one, from the venue AI profile and the starting pattern for the venue type, and says so; the stage badge shows how much of the answer is the venue's own data. The action asks for the first one.",
   "emptyNoAccess": "You do not have AI permission at this venue.",
   "emptyNoResults": "No suggestion of this kind. Names the kind filter and offers to clear it."
  },
  "apis": [
   {
    "operationId": "requestSuggestion",
    "contract": "ai",
    "purpose": "Ask for an answer",
    "trigger": "onAction"
   },
   {
    "operationId": "recordSuggestionOutcome",
    "contract": "ai",
    "purpose": "What the venue did",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "suggestionId",
     "from": "deepLink",
     "optional": true
    }
   ],
   "coldEntry": "A bookmarked view opened weekly, or **a link from an alert naming one suggestion** — an alert that cannot take a manager to the thing it is about is a notification."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-010",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn as POS-6F in the client POS pack.** The pack's frame is the specification — it carries operations, states, entry params and exits, and it is better specified than anything derived from the screen file.",
   "derivedFrom": "wireframes/POS Board 6.dc.html#pos-6f"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formRecordSuggestionOutcome",
    "component": "modal",
    "trigger": "Record suggestion outcome",
    "body": "**Collects what `recordSuggestionOutcome` sends before it is called.** Required: `id`, `suggestionId`, `decision`. Optional: `actualValue`, `decidedByPrincipalId`, `decidedAt`, `realisedOutcome`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SuggestionOutcome",
    "confirm": {
     "label": "Record suggestion outcome",
     "operation": "recordSuggestionOutcome"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "suggestionId",
      "decision",
      "actualValue",
      "decidedByPrincipalId",
      "decidedAt",
      "realisedOutcome",
      "note"
     ]
    },
    "provenance": "contract ai.yaml POST /ai/suggestions/{suggestionId}/outcome"
   }
  ],
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
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
 "acknowledgeAlert": {
  "method": "POST",
  "path": "/alerts/{alertId}/acknowledge",
  "contract": "reporting",
  "summary": "Mark it seen",
  "permission": "REPORT_VIEW_VENUE",
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
  "responds": "Alert"
 },
 "askReportingQuestion": {
  "method": "POST",
  "path": "/reports/ask",
  "contract": "reporting",
  "summary": "Natural-language reporting query",
  "permission": "REPORT_VIEW_VENUE",
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
  "responds": "NaturalLanguageAnswer"
 },
 "createSegment": {
  "method": "POST",
  "path": "/segments",
  "contract": "marketing-crm",
  "summary": "Create a segment",
  "permission": "MARKETING_MANAGE",
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
  "requestBody": "CreateSegmentRequest",
  "responds": "Segment"
 },
 "decideProposedAction": {
  "method": "POST",
  "path": "/proposed-actions/{actionId}/decide",
  "contract": "ai",
  "summary": "Approve or reject a proposal",
  "permission": "AI_USE",
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
  "responds": "ProposedAction"
 },
 "getActionPlan": {
  "method": "GET",
  "path": "/action-plans/{planId}",
  "contract": "ai",
  "summary": "A plan with its steps",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiActionPlanDetail"
 },
 "getCommandCentre": {
  "method": "GET",
  "path": "/command-centre",
  "contract": "reporting",
  "summary": "The dashboards this login may see, grouped by module",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CommandCentre"
 },
 "getCountVariance": {
  "method": "GET",
  "path": "/stock-counts/{countId}/variance",
  "contract": "inventory",
  "summary": "Variance between counted and expected",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CountVariance"
 },
 "getDashboard": {
  "method": "GET",
  "path": "/dashboards/{dashboardId}",
  "contract": "reporting",
  "summary": "Read a dashboard with tile data",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "refresh",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DashboardData"
 },
 "getForecast": {
  "method": "GET",
  "path": "/forecasts",
  "contract": "ai",
  "summary": "Forecast values",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "definitionKey",
    "in": "query",
    "required": true
   },
   {
    "name": "versionId",
    "in": "query",
    "required": null
   },
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "to",
    "in": "query",
    "required": null
   },
   {
    "name": "dimensionKey",
    "in": "query",
    "required": null
   },
   {
    "name": "scenarioId",
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
 "getStockValuation": {
  "method": "GET",
  "path": "/stock/valuation",
  "contract": "inventory",
  "summary": "Stock value by location and category",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "asAt",
    "in": "query",
    "required": null
   },
   {
    "name": "locationId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "StockValuation"
 },
 "listAiInsights": {
  "method": "GET",
  "path": "/insights",
  "contract": "ai",
  "summary": "Insights and anomalies",
  "permission": "AI_USE",
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
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "priority",
    "in": "query",
    "required": null
   },
   {
    "name": "from",
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
 "listAlerts": {
  "method": "GET",
  "path": "/alerts",
  "contract": "reporting",
  "summary": "What is currently wrong",
  "permission": "REPORT_VIEW_VENUE",
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
    "name": "severity",
    "in": "query",
    "required": null
   },
   {
    "name": "workstationId",
    "in": "query",
    "required": null
   },
   {
    "name": "shiftId",
    "in": "query",
    "required": null
   },
   {
    "name": "itemId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Alert"
 },
 "listDevices": {
  "method": "GET",
  "path": "/devices",
  "contract": "tenancy",
  "summary": "List registered devices",
  "permission": "DEVICE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "workstationId",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
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
 "listExpiringBatches": {
  "method": "GET",
  "path": "/stock-batches/expiring",
  "contract": "inventory",
  "summary": "What is about to go out of date",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "withinDays",
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
 "listPrincipals": {
  "method": "GET",
  "path": "/principals",
  "contract": "identity",
  "summary": "List principals",
  "permission": "USER_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   },
   {
    "name": "isActive",
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
 "listProposedActions": {
  "method": "GET",
  "path": "/proposed-actions",
  "contract": "ai",
  "summary": "What the assistant has proposed and nobody has decided",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ProposedAction"
 },
 "listSegments": {
  "method": "GET",
  "path": "/segments",
  "contract": "marketing-crm",
  "summary": "List segments",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "search",
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
 "previewSegment": {
  "method": "POST",
  "path": "/segments/{segmentId}/preview",
  "contract": "marketing-crm",
  "summary": "Estimate segment size and reachability",
  "permission": "MARKETING_VIEW",
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
  "responds": "SegmentPreview"
 },
 "recordDashboardView": {
  "method": "POST",
  "path": "/dashboards/{dashboardId}/views",
  "contract": "reporting",
  "summary": "Record that a dashboard was opened",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "append",
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
 "recordSuggestionOutcome": {
  "method": "POST",
  "path": "/ai/suggestions/{suggestionId}/outcome",
  "contract": "ai",
  "summary": "What the venue actually did",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "SuggestionOutcome",
  "responds": "SuggestionOutcome"
 },
 "requestSuggestion": {
  "method": "POST",
  "path": "/ai/suggestions",
  "contract": "ai",
  "summary": "Ask for an answer, however it is currently produced",
  "permission": "AI_USE",
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
  "responds": "Suggestion"
 },
 "runReport": {
  "method": "POST",
  "path": "/reports/{reportId}/run",
  "contract": "reporting",
  "summary": "Run a report",
  "permission": "REPORT_VIEW_VENUE",
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
  "requestBody": "RunReportRequest",
  "responds": "ReportResult"
 },
 "setAlertRule": {
  "method": "PUT",
  "path": "/alert-rules",
  "contract": "reporting",
  "summary": "Watch a metric and tell somebody",
  "permission": "REPORT_MANAGE",
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
  "requestBody": "AlertRule",
  "responds": "AlertRule"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiActionPlan": {
  "type": "object",
  "x-ticvai-persistence": "ai.action_plan",
  "description": "**A plan: plan, validate, simulate, approve, execute, with rollback** (design 2.2 D, 3.8; AIC-086..107). Independent of any conversation (AIC-102). Its steps are `ai.action_step`; the change set is hashed so what was approved is what runs (AIC-181).",
  "required": [
   "origin",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "origin": {
    "type": "string",
    "enum": [
     "configurationSession",
     "generateConfiguration",
     "assistant",
     "riskCase",
     "operationalRequirement",
     "rollback"
    ]
   },
   "originRef": {
    "type": "string",
    "nullable": true
   },
   "summary": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "validated",
     "simulated",
     "awaitingApproval",
     "approved",
     "executing",
     "paused",
     "completed",
     "partiallyCompleted",
     "failed",
     "compensated",
     "cancelled",
     "rolledBack"
    ],
    "readOnly": true
   },
   "autonomyLevel": {
    "$ref": "#/components/schemas/AiAutonomyLevel"
   },
   "approvalTier": {
    "type": "integer",
    "minimum": 1,
    "maximum": 2,
    "description": "The approval tier (1 or 2), the floor the approvals matrix adds to (design 3.8). Not an autonomy level."
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The `approvals` request, where tier 2 or the matrix caught the plan."
   },
   "proposedActionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "ai.proposed_action",
    "description": "The `ai.proposed_action` the plan is presented as for a decision."
   },
   "changeSetHash": {
    "type": "string",
    "readOnly": true
   },
   "governanceOutcome": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiGovernanceOutcome"
     }
    ],
    "readOnly": true
   },
   "policyVersionRef": {
    "type": "string",
    "readOnly": true,
    "description": "The governance policy version that decided it."
   },
   "simulation": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "readOnly": true,
    "description": "Current versus proposed state, channels, future orders and issued tickets affected (flow D step 4)."
   },
   "partialCompletionAllowed": {
    "type": "boolean",
    "default": false,
    "description": "Where governance allows a partial completion; otherwise a failure compensates in reverse dependency order (AIC-098, AIC-134)."
   },
   "rollbackOfPlanId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.action_plan"
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiActionPlanDetail": {
  "type": "object",
  "x-ticvai-persistence": "none — ai.action_plan with its ai.action_step rows",
  "description": "A plan with its steps in DAG order.",
  "required": [
   "plan",
   "steps"
  ],
  "properties": {
   "plan": {
    "$ref": "#/components/schemas/AiActionPlan"
   },
   "steps": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiActionStep"
    }
   }
  }
 },
 "AiActionStep": {
  "type": "object",
  "x-ticvai-persistence": "ai.action_step",
  "description": "One step of a plan: a registered tool against `targetContract.targetOperation` at a contract version (AIC-095), with payload, provenance, compensation and the idempotency key `plan:{id}:step:{n}`. **Scoped through its plan** (`platform.apply_parent_rls`). Each step records its target object's version; drift pauses the plan (AIC-182).",
  "required": [
   "planId",
   "stepNumber",
   "toolKey",
   "targetContract",
   "targetOperation",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.action_plan"
   },
   "stepNumber": {
    "type": "integer",
    "minimum": 1
   },
   "dependsOn": {
    "type": "array",
    "items": {
     "type": "integer",
     "minimum": 1
    },
    "description": "Step numbers that must succeed first. The plan is a DAG."
   },
   "toolKey": {
    "type": "string"
   },
   "targetContract": {
    "type": "string"
   },
   "targetOperation": {
    "type": "string"
   },
   "contractVersion": {
    "type": "string"
   },
   "payload": {
    "type": "object",
    "additionalProperties": true,
    "description": "The request body of `targetOperation`, validated against it before the plan is approved."
   },
   "provenance": {
    "$ref": "#/components/schemas/AiProvenance"
   },
   "idempotencyKey": {
    "type": "string",
    "readOnly": true
   },
   "targetObjectRef": {
    "type": "string",
    "nullable": true
   },
   "targetObjectVersion": {
    "type": "string",
    "nullable": true,
    "description": "The version the step was planned against. A different version at execution is drift."
   },
   "reversible": {
    "type": "boolean"
   },
   "compensation": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "validated",
     "running",
     "succeeded",
     "failed",
     "compensated",
     "skipped",
     "paused"
    ],
    "readOnly": true
   },
   "attempts": {
    "type": "integer",
    "minimum": 0,
    "maximum": 3,
    "readOnly": true,
    "description": "Bounded at 3 (AIC-135)."
   },
   "lastError": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "resultRef": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The owning service's response: success is its answer, not a model's judgement (AIC-097)."
   },
   "startedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "AiEvidenceItemList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "The evidence of one decision record, stored with it.",
  "items": {
   "$ref": "#/components/schemas/AiEvidenceItem"
  }
 },
 "AiForecastPoint": {
  "type": "object",
  "x-ticvai-persistence": "ai.forecast_point",
  "description": "One forecast value with its interval: 10th, 50th and 90th percentile (design 5.6: a range, never a bare percentage). Partitioned by target month. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.",
  "required": [
   "versionId",
   "targetStart",
   "p50"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "versionId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.forecast_version"
   },
   "scenarioId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.forecast_scenario",
    "description": "Set where the point belongs to a what-if scenario rather than the version itself."
   },
   "targetStart": {
    "type": "string",
    "format": "date-time"
   },
   "targetEnd": {
    "type": "string",
    "format": "date-time"
   },
   "dimensionKey": {
    "type": "string",
    "nullable": true,
    "description": "Canonical key of the breakdown, e.g. `product=…;channel=web`."
   },
   "p10": {
    "type": "number",
    "nullable": true
   },
   "p50": {
    "type": "number"
   },
   "p90": {
    "type": "number",
    "nullable": true
   },
   "unit": {
    "type": "string"
   },
   "drivers": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Component decomposition or SHAP contributions, largest first (ADM-506)."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiForecastVersion": {
  "type": "object",
  "x-ticvai-persistence": "ai.forecast_version",
  "description": "**An immutable forecast version** (AIP-032): producer, model version, data cut-off, horizon and status. Nothing is overwritten; yesterday's actuals are scored against every earlier version.",
  "required": [
   "definitionId",
   "versionNumber",
   "status",
   "basis"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "definitionId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.forecast_definition"
   },
   "versionNumber": {
    "type": "integer",
    "minimum": 1
   },
   "status": {
    "type": "string",
    "enum": [
     "running",
     "draft",
     "awaitingApproval",
     "published",
     "superseded",
     "rejected",
     "failed"
    ],
    "readOnly": true
   },
   "basis": {
    "$ref": "#/components/schemas/SuggestionBasis"
   },
   "maturity": {
    "$ref": "#/components/schemas/AiMaturity"
   },
   "producerRef": {
    "type": "string"
   },
   "modelVersion": {
    "type": "string",
    "nullable": true
   },
   "dataCutoffAt": {
    "type": "string",
    "format": "date-time",
    "description": "The analytical replica watermark the snapshot was taken at."
   },
   "horizonStart": {
    "type": "string",
    "format": "date-time"
   },
   "horizonEnd": {
    "type": "string",
    "format": "date-time"
   },
   "qualityChecks": {
    "type": "object",
    "additionalProperties": true,
    "readOnly": true,
    "description": "Each gate and whether it passed."
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal",
    "description": "Null where the definition auto-published."
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiInsight": {
  "type": "object",
  "x-ticvai-persistence": "ai.insight",
  "description": "**An insight with a lifecycle** (AIP-181): new, reviewed, accepted or rejected, actioned, measured. Anomalies, forecast deviations, trends and opportunities land here; the narrative binds numbers to results, so a figure can only come from a query (design 8, 5.10).",
  "required": [
   "kind",
   "title",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "anomaly",
     "forecastDeviation",
     "trend",
     "opportunity",
     "executiveSummary",
     "rootCause",
     "forecastThreshold",
     "marketingRecommendation"
    ]
   },
   "detectorId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.anomaly_detector"
   },
   "metricKey": {
    "type": "string",
    "nullable": true
   },
   "subjectKind": {
    "type": "string",
    "nullable": true,
    "enum": [
     "campaign",
     "journey",
     "forecastDefinition",
     "venue"
    ],
    "description": "What the insight is about where it is not a KPI (29 September, build): a marketing-crm campaign or journey for `marketingRecommendation`, a forecast definition for `forecastThreshold`."
   },
   "subjectRef": {
    "type": "string",
    "nullable": true
   },
   "recommendedAction": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "For `marketingRecommendation`: `{recommendation, parameters}` as `AiMarketingRecommendation`. Applied by a person in the owning module, never here."
   },
   "expectedImpact": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "A range on a named metric (`metric`, `low`, `high`), never a single number (design 5.6)."
   },
   "title": {
    "type": "string"
   },
   "narrative": {
    "type": "string",
    "nullable": true
   },
   "evidence": {
    "$ref": "#/components/schemas/AiEvidenceItemList"
   },
   "magnitude": {
    "type": "number",
    "nullable": true
   },
   "priority": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ]
   },
   "correlationKey": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "new",
     "reviewed",
     "accepted",
     "rejected",
     "actioned",
     "measured"
    ],
    "readOnly": true
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "actionRef": {
    "type": "string",
    "nullable": true
   },
   "measuredImpact": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "readOnly": true
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "detectedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiMaturity": {
  "type": "object",
  "x-ticvai-persistence": "none — embedded as jsonb on ai.suggestion and ai.forecast_version",
  "description": "**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.",
  "required": [
   "stage",
   "basedOn"
  ],
  "properties": {
   "stage": {
    "type": "string",
    "enum": [
     "starting",
     "learning",
     "established",
     "learned"
    ],
    "description": "`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."
   },
   "basedOn": {
    "type": "string",
    "description": "The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."
   },
   "sources": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "source"
     ],
     "properties": {
      "source": {
       "type": "string",
       "enum": [
        "venueSettings",
        "startingPattern",
        "calendar",
        "weather",
        "bookingsOnHand",
        "ownHistory",
        "importedHistory",
        "configuration",
        "trainedModel"
       ]
      },
      "detail": {
       "type": "string",
       "nullable": true,
       "description": "e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."
      },
      "observations": {
       "type": "integer",
       "nullable": true
      }
     }
    }
   },
   "ownDataShare": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."
   },
   "limitedHistory": {
    "type": "boolean"
   },
   "nextStage": {
    "type": "object",
    "nullable": true,
    "description": "What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.",
    "properties": {
     "stage": {
      "type": "string",
      "enum": [
       "learning",
       "established",
       "learned"
      ]
     },
     "needs": {
      "type": "string"
     },
     "expectedBy": {
      "type": "string",
      "format": "date",
      "nullable": true
     }
    }
   }
  }
 },
 "Alert": {
  "type": "object",
  "x-ticvai-persistence": "reporting.alert",
  "description": "A raised alert. **Acknowledged rather than dismissed** — CF-134 asked for it markable, and the difference is that an acknowledgement records who saw it.\n",
  "required": [
   "id",
   "ruleId",
   "raisedAt",
   "severity",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "ruleId": {
    "type": "string",
    "format": "uuid"
   },
   "ruleName": {
    "type": "string",
    "description": "`AlertRule.name` as it stood when the alert was raised. **The line a person reads** — a list of rule ids is not an alert panel, and a screen should not need `listAlertRules` to label one.\n"
   },
   "metric": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricSource"
     }
    ],
    "description": "The rule's metric, carried so the alert says what went out of range."
   },
   "raisedAt": {
    "type": "string",
    "format": "date-time"
   },
   "severity": {
    "$ref": "#/components/schemas/AlertSeverity"
   },
   "status": {
    "$ref": "#/components/schemas/AlertStatus"
   },
   "observedValue": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "threshold": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "scopePath": {
    "type": "string"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The workstation the reading was taken for, where the metric is measured per workstation (`salesByWorkstation`). Null otherwise. `listAlerts` filters on it."
   },
   "shiftId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The till shift (`orders.pos_shift`) the reading belongs to, where it was taken for a workstation with a shift open. Null otherwise. `listAlerts` filters on it."
   },
   "itemId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The inventory item the reading is about, where the metric is measured per item (`stockAgeing`, `stockTurnover`, `wastageRate`, `inventoryValuation`). Null otherwise. **What a replenishment screen prefills a requisition from.**\n"
   },
   "acknowledgedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "acknowledgedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "acknowledgementNote": {
    "type": "string",
    "maxLength": 300,
    "nullable": true,
    "description": "The `note` given to `acknowledgeAlert`. Kept, because an acknowledgement that says what is being done about it is the one escalation can skip."
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**Set when the metric returns to range, automatically.** An alert that only a person can close is an alert list that only grows.\n"
   },
   "escalatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. **A critical alert nobody acknowledged is the case escalation exists for.**\n"
   }
  }
 },
 "AlertRule": {
  "type": "object",
  "x-ticvai-persistence": "reporting.alert_rule",
  "description": "BL-152, CF-134. **Six contracts detect their own trouble and none told a person.**\nFive sections ask for this and it is the same gap as `MessageTrigger`, seen from the operational side — **that one tells a guest something happened; this one tells an operator something is wrong.**\n**A threshold that nobody is watching is a threshold nobody set.** 6.1.57 wants an exception when a KPI leaves range, and an exception that arrives in a nightly report is an exception nobody acted on.\n",
  "required": [
   "id",
   "name",
   "metric",
   "comparator",
   "threshold",
   "severity",
   "isActive",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "metric": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricSource"
     }
    ],
    "description": "**From the closed set**, so a rule cannot watch something nothing produces — the same discipline `MetricSource` exists for.\n"
   },
   "comparator": {
    "type": "string",
    "enum": [
     "above",
     "below",
     "outsideRange",
     "changesBy",
     "equals"
    ]
   },
   "threshold": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "thresholdUpper": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true,
    "description": "**Required when `comparator` is `outsideRange`** (decided 28 September, audit R158): the range is `threshold` to `thresholdUpper`, and a rule missing either, or with the upper not above the lower, is refused by `setAlertRule` with 400. Ignored for every other comparator.\n"
   },
   "windowMinutes": {
    "type": "integer",
    "default": 15,
    "description": "**The window is what stops an alert firing on noise.** A queue that spikes for ninety seconds is not a queue that needs a manager, and a rule with no window is a rule somebody mutes within a week.\n"
   },
   "severity": {
    "$ref": "#/components/schemas/AlertSeverity"
   },
   "deliverTo": {
    "type": "array",
    "description": "CF-134. **The dashboard panel is the default and the only one that always applies.** Email or WhatsApp where the matrix names them — an operational alert arriving by email is an alert nobody sees in time.\n",
    "items": {
     "type": "string",
     "enum": [
      "dashboardPanel",
      "email",
      "whatsapp",
      "sms",
      "push"
     ]
    },
    "x-ticvai-push-note": "**`push` added 29 September** (6.1.56, 18.1.5, build pass): delivered to every staff-app handset registered for a recipient (tenancy `RegisteredDevice`, kind `mobileHandset`, with a push token). It is how a daily revenue alert reaches a manager's phone, which a panel on a web dashboard does not.\n"
   },
   "recipientRoleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "cooldownMinutes": {
    "type": "integer",
    "default": 30,
    "description": "**How long before the same rule may fire again.** Without it, a metric hovering on a threshold produces forty alerts an hour and the panel becomes something people close.\n"
   },
   "isActive": {
    "type": "boolean"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**\n\n**Required, and it is the write target.** `setAlertRule` has no id in its path and a caller may hold several venues, so the rule names the venue it watches here — inside the caller's scope, or the write is refused."
   }
  }
 },
 "AlertSeverity": {
  "type": "string",
  "description": "How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter.",
  "enum": [
   "info",
   "warning",
   "critical"
  ]
 },
 "AlertStatus": {
  "type": "string",
  "description": "Where a raised alert is. Shared by `Alert` and the `listAlerts` filter.",
  "enum": [
   "raised",
   "acknowledged",
   "resolved",
   "expired"
  ]
 },
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
 "CommandCentre": {
  "x-ticvai-persistence": "none — computed per caller from `reporting.dashboard`, the tenant's licensed modules and the principal's permissions",
  "type": "object",
  "description": "**What one login sees in the command centre.** Not stored: two principals in the same venue receive different command centres, and a stored one would be wrong the moment a role or a licence changed.",
  "required": [
   "modules",
   "resolvedAt"
  ],
  "properties": {
   "modules": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "module",
      "dashboards"
     ],
     "properties": {
      "module": {
       "$ref": "../shared/common.yaml#/components/schemas/ModuleKey"
      },
      "dashboards": {
       "type": "array",
       "description": "Shared first, then the caller's own, each by name. Tile data is not included — `getDashboard` reads one with its data when it is opened.",
       "items": {
        "$ref": "#/components/schemas/Dashboard"
       }
      },
      "canAuthor": {
       "type": "boolean",
       "description": "**Whether the caller may build a dashboard for this module** — `REPORT_MANAGE` plus entitlement to the module. Returned so the shell can offer the drag-and-drop authoring entry point only where `createDashboard` would accept it; the server still enforces it on the write."
      }
     }
    }
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "description": "When the entitlement was evaluated. A licence or role change after this is not reflected until the next read."
   }
  }
 },
 "CountVariance": {
  "x-ticvai-persistence": "none — computed at close",
  "type": "object",
  "required": [
   "countId",
   "totalVarianceValue",
   "lines"
  ],
  "properties": {
   "countId": {
    "type": "string",
    "format": "uuid"
   },
   "totalVarianceValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "exceptionCount": {
    "type": "integer",
    "description": "Lines beyond `VenueSettings.inventory.countVarianceTolerancePercent` (proposed default 2 per cent, audit R094), requiring review before posting."
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "itemId",
      "expectedQuantity",
      "countedQuantity",
      "variance",
      "isException"
     ],
     "properties": {
      "itemId": {
       "type": "string",
       "format": "uuid"
      },
      "itemName": {
       "type": "string"
      },
      "sku": {
       "type": "string"
      },
      "expectedQuantity": {
       "type": "number"
      },
      "countedQuantity": {
       "type": "number"
      },
      "variance": {
       "type": "number"
      },
      "variancePercentage": {
       "type": "number"
      },
      "varianceValue": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "isException": {
       "type": "boolean"
      },
      "recountCount": {
       "type": "integer",
       "description": "A line counted several times is itself a finding."
      },
      "note": {
       "type": "string",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "CreateSegmentRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "criteria"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "match": {
    "type": "string",
    "enum": [
     "all",
     "any"
    ],
    "default": "all"
   },
   "criteria": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/SegmentCriterion"
    }
   },
   "excludeSegmentIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "Dashboard": {
  "x-ticvai-persistence": "reporting.dashboard + reporting.dashboard_tile",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateDashboardRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "ownerPrincipalId",
     "aggregateCost",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "ownerPrincipalId": {
      "type": "string",
      "format": "uuid"
     },
     "aggregateCost": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high"
      ],
      "description": "Combined refresh load of every tile."
     },
     "archivedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "description": "**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
 },
 "DashboardData": {
  "x-ticvai-persistence": "none — computed",
  "allOf": [
   {
    "$ref": "#/components/schemas/Dashboard"
   },
   {
    "type": "object",
    "properties": {
     "tileData": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "tileId": {
         "type": "string",
         "format": "uuid"
        },
        "result": {
         "$ref": "#/components/schemas/ReportResult"
        },
        "isCached": {
         "type": "boolean"
        },
        "error": {
         "type": "string",
         "nullable": true
        }
       }
      }
     }
    }
   }
  ]
 },
 "DeviceCapability": {
  "type": "string",
  "description": "BL-179. **Something a driver reports, not something the platform provides.** The list grows as vendors are added, which is ADR-0015's whole position: adding a vendor is a driver plus configuration rather than a core change.\n**`genderClassification` is here because `VenueSettings.segregatedAccess. genderVerification` already offers `deviceAssisted` and nothing answered it** — a switch with no driver behind it. Where a venue's access hardware performs the check and the venue chooses to use it, the result is **advisory to the steward and never decisive at the turnstile** (`ValidationResult.advisory`). 3.2.45 asks for rejection; the package deviates deliberately and CF-130 records why.\n**Access's capabilities merged in** (ADR-0067, 1 October): `dynamicQr`, `rfid`, `nfc`, `facePass`, `offline` and `heightCheck` were the access register's own list, from the compatibility matrix.\n",
  "enum": [
   "genderClassification",
   "dynamicQr",
   "rfid",
   "nfc",
   "facePass",
   "offline",
   "heightCheck"
  ]
 },
 "DeviceKind": {
  "type": "string",
  "enum": [
   "receiptPrinter",
   "ticketPrinter",
   "labelPrinter",
   "cashDrawer",
   "barcodeScanner",
   "rfidReader",
   "nfcReader",
   "cardReader",
   "idReader",
   "biometricReader",
   "accessReader",
   "paymentTerminal",
   "customerDisplay",
   "signageDisplay",
   "kitchenDisplay",
   "turnstileController",
   "wristbandEncoder",
   "signaturePad",
   "scale",
   "camera",
   "mobileHandset",
   "handheldScanner",
   "accessPodium",
   "bleBeacon"
  ],
  "description": "`mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no workstation.\n**One kind vocabulary for every device** (ADR-0067, 1 October). `handheldScanner`, `accessPodium` and `bleBeacon` came from Access's register; the finer hardware type (a speed gate under `turnstileController`, a tablet under `handheldScanner`) is `RegisteredDevice.hardwareType` (common `DeviceHardwareType`).\n"
 },
 "FieldType": {
  "type": "string",
  "enum": [
   "string",
   "integer",
   "decimal",
   "money",
   "boolean",
   "date",
   "dateTime",
   "uuid",
   "enum"
  ]
 },
 "GeneratedQuery": {
  "x-ticvai-persistence": "none — embedded; stored whole in `reporting.natural_language_query`",
  "type": "object",
  "description": "The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n",
  "properties": {
   "dataSource": {
    "$ref": "#/components/schemas/DataSource"
   },
   "columns": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ReportColumn"
    }
   },
   "filters": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ReportFilter"
    }
   },
   "groupBy": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "compiledSql": {
    "type": "string",
    "nullable": true,
    "description": "The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"
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
 "MetricSource": {
  "type": "string",
  "description": "**A named metric with a verified source.** BL-053, 75 requirement rows.\n`reporting` is a generic builder, and **a generic builder makes every reporting requirement look covered** — it will happily assemble a report over data nobody produces. That is the shape to watch across the whole walk, and this enum is the answer to it: each value below was checked against the schema before being named.\n| Metric | Source | |---|---| | `occupancy` | `catalogue.channel_capacity.sold` and `leased` against `capacity` | | `capacityUtilisation` | `catalogue.channel_capacity.remaining` over the same window | | `admissionRate` | `access.scan_event.outcome`, in-direction | | `noShowRate` | Entitlements issued against scans that never arrived | | `conversion` | `orders.cart` against `orders.sales_order` | | `salesByOperator` | `orders.sales_order.principal_id` | | `salesByWorkstation` | The workstation on the shift that took it | | `waitTime` | `queue.waiting_guest.estimated_call_at` against `called_at` | | `throughput` | `queue.waiting_guest` completions per hour | | `abandonmentRate` | Queue entries that left before being called |\n**`salesByInstructor` was deliberately absent from the first cut** because it needed the staff-assignment link CL-01 covers. It was added on 18 August once `resources.Resource` produced it — see `x-ticvai-extension-note` below. Naming a metric with no source is still the defect this enum exists to prevent.\n**Money-valued metrics are listed in `x-ticvai-money-valued`.** A reading or threshold on one of them is a `Money`, never a float (`MetricValue`).\n",
  "enum": [
   "occupancy",
   "capacityUtilisation",
   "admissionRate",
   "noShowRate",
   "conversion",
   "salesByOperator",
   "salesByWorkstation",
   "waitTime",
   "throughput",
   "abandonmentRate",
   "inventoryValuation",
   "stockTurnover",
   "stockAgeing",
   "wastageRate",
   "resaleVolume",
   "resaleCommission",
   "salesByInstructor",
   "resourceUtilisation",
   "allocationUtilisation",
   "channelAllocationBurn",
   "membershipChurn",
   "membershipRenewalRate",
   "supplierDeliveryPerformance",
   "revenuePerEntitlement",
   "revenuePerVisitor",
   "assetDowntime",
   "meanTimeToRepair",
   "challengeCompletionRate",
   "attributedRevenue",
   "loyaltyActiveMembers",
   "loyaltyTierDistribution",
   "loyaltyPointsLiability",
   "loyaltyBreakageRate",
   "loyaltyMemberRetention",
   "challengeParticipationRate",
   "gamificationLoyaltyImpact",
   "gamificationMembershipImpact",
   "gamificationRetention",
   "accreditationApplications",
   "accreditationTimeToDecision",
   "accreditationCredentialsIssued",
   "accreditationActiveHolders",
   "accreditationRenewalsDue",
   "staffingShortfall"
  ],
  "x-ticvai-money-valued": [
   "inventoryValuation",
   "resaleCommission",
   "revenuePerEntitlement",
   "revenuePerVisitor",
   "attributedRevenue",
   "loyaltyPointsLiability"
  ],
  "x-ticvai-extended-29-september": "**Fourteen metrics added 29 September (build pass)**, each checked against the schema of the contract that produces it.\n\n| Metric | Source | Requirement | |---|---|---| | `loyaltyActiveMembers` | `marketing.loyalty_position` members with a `marketing.loyalty_points` movement in the period | 5.4.27 | | `loyaltyTierDistribution` | `marketing.loyalty_position.tier_id` against `marketing.programme_tier`, members per tier | 5.4.27 | | `loyaltyPointsLiability` | the balance of `ledger.journal_line` on each programme's `pointsLiabilityAccountId`, where points post on accrual and release on redemption or expiry | 5.4.27 | | `loyaltyBreakageRate` | `marketing.loyalty_points` expiry movements over points earned, in the period | 5.4.27 | | `loyaltyMemberRetention` | members with a movement in the previous period who also have one in this period | 5.4.27 | | `challengeParticipationRate` | distinct `marketing.challenge_progress.subject_id` over active loyalty members | 22.6.20 | | `gamificationLoyaltyImpact` | points earned per member, challenge participants against non-participants (`marketing.loyalty_points` split by `marketing.challenge_progress`) | 22.6.20 | | `gamificationMembershipImpact` | joins and renewals in `identity.customer_membership`, participants against non-participants | 22.6.20 | | `gamificationRetention` | return visits (`access.scan_event`, in-direction) of participants against non-participants | 22.6.20 | | `accreditationApplications` | `accreditation.application` by `status` | 12.1.50 | | `accreditationTimeToDecision` | `accreditation.application.decided_at` minus `submitted_at` | 12.1.50 | | `accreditationCredentialsIssued` | `accreditation.credential.issued_at` | 12.1.50 | | `accreditationActiveHolders` | `accreditation.holder` `active`, by `category_code` | 12.1.50 | | `accreditationRenewalsDue` | `accreditation.holder.valid_to` inside `accreditation.validity.renewal_window_days` | 12.1.50 |\n\n**`staffingShortfall` added the same evening (build pass, group G2; 8.2.49)**: the largest gap in the window between the staff rostered and the staff the forecast requires, per venue and position, from `workforce.forecast_requirement` (the handed-over AI staff requirement) against `workforce.rota_assignment` and `workforce.open_shift`, computed as `workforce.getStaffingCoverage` with `basis` `forecastRequirement`. An `AlertRule` on it with `comparator` `above` and `threshold` 0 is the staffing shortage alert; `windowMinutes` looks ahead rather than back for this metric (the rota for the coming window), and `cooldownMinutes` stops one short shift alerting every quarter hour.\n\n**Points issued, points redeemed, campaign performance and reward redemption were already served** by the `loyalty` and `campaigns` sources, and challenge completion and revenue attribution by `challengeCompletionRate` and `attributedRevenue`.\n",
  "x-ticvai-money-valued-note": "**`salesByOperator`, `salesByWorkstation` and `resaleVolume` are not listed because the package does not say whether they count sales or sum their value.** Until that is decided, a rule on them carries a plain number.\n",
  "x-ticvai-extended": "18 August 2026",
  "x-ticvai-extension-note": "**Nineteen metrics added when their upstream models landed**, which is how BL-053 was always going to close — not by changing `reporting` but by building the things it wanted to report on.\n`inventoryValuation`, `stockTurnover`, `stockAgeing` and `wastageRate` came from `inventory.StockBatch`; `resaleVolume` and `resaleCommission` from `orders.ResaleListing`; **`salesByInstructor` from `resources.Resource`, which was the one metric this enum deliberately refused to name in the morning** because nothing produced it. `allocationUtilisation` from `PartnerUser` and `ChannelListing`, `membershipChurn` from `Journey`, `supplierDeliveryPerformance` from `ProductionRun`, `assetDowntime` and `meanTimeToRepair` from `WorkOrder.downtimeMinutes`, `challengeCompletionRate` from `ChallengeProgress`, `attributedRevenue` from `AttributionTouch`.\n**Each was checked against the schema before being named.** That rule has not changed — naming a metric with no source is the defect this enum exists to prevent.\n"
 },
 "MetricValue": {
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n",
  "oneOf": [
   {
    "type": "number"
   },
   {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  ]
 },
 "NaturalLanguageAnswer": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "conversationId",
   "question",
   "interpretation",
   "result",
   "reliability"
  ],
  "properties": {
   "conversationId": {
    "type": "string"
   },
   "question": {
    "type": "string"
   },
   "interpretation": {
    "type": "string",
    "description": "What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."
   },
   "semanticSpec": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ReportingSemanticQuerySpec"
     }
    ],
    "nullable": true,
    "description": "What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"
   },
   "generatedQuery": {
    "allOf": [
     {
      "$ref": "#/components/schemas/GeneratedQuery"
     }
    ],
    "nullable": true,
    "description": "The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"
   },
   "result": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ReportResult"
     }
    ],
    "nullable": true,
    "description": "Null when the question is outside the semantic model."
   },
   "dataAsOf": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."
   },
   "reliability": {
    "$ref": "#/components/schemas/ReportingAnswerReliability"
   },
   "unavailableReason": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ReportingUnavailableReason"
     }
    ],
    "nullable": true,
    "description": "Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."
   },
   "confidence": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "deprecated": true,
    "description": "Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."
   },
   "suggestedFollowUps": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "modelVersion": {
    "type": "string"
   },
   "tokensUsed": {
    "type": "integer"
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
 "Principal": {
  "x-ticvai-persistence": "identity.principal",
  "type": "object",
  "required": [
   "id",
   "username",
   "displayName",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "username": {
    "type": "string"
   },
   "displayName": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Past this, resolution returns DENY regardless of grants."
   },
   "primaryRoleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Determines the landing screen when the principal holds several roles and picks one at login.\n"
   },
   "roles": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/RoleSummary"
    }
   },
   "lastLoginAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "ProposedAction": {
  "type": "object",
  "x-ticvai-persistence": "ai.proposed_action",
  "required": [
   "id",
   "kind",
   "targetContract",
   "targetOperation",
   "payload",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "interactionId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "pricing",
     "promotion",
     "operational",
     "financial",
     "configuration",
     "content",
     "audience"
    ],
    "description": "`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."
   },
   "targetContract": {
    "type": "string",
    "description": "Which contract would perform it. The assistant never performs it itself."
   },
   "targetOperation": {
    "type": "string"
   },
   "payload": {
    "type": "object",
    "additionalProperties": true,
    "description": "The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"
   },
   "summary": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "description": "**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n",
    "enum": [
     "proposed",
     "approved",
     "rejected",
     "applied",
     "expired"
    ]
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."
   },
   "approvalLevel": {
    "type": "integer",
    "minimum": 1,
    "maximum": 2,
    "description": "8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decisionReason": {
    "type": "string",
    "nullable": true,
    "description": "Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"
   },
   "proposedAt": {
    "type": "string",
    "format": "date-time"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "ai.action_plan",
    "description": "The plan this action presents for a decision (AI design 2.2 D, 3.8)."
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."
   },
   "changeSetHash": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."
   }
  }
 },
 "RegisteredDevice": {
  "x-ticvai-persistence": "platform.device",
  "type": "object",
  "description": "**The only device register** (ADR-0067, accepted 1 October; the register of record since 29 September). Identity (kind, hardware type, model, serial), every version (firmware, configuration, rule package, credential package), health, heartbeat and one lifecycle (`enrolmentState`: registered, enrolled, provisioned, active, deactivated, retired) for every device in the estate live on this row. The access-control device row, which repeated serial, versions, health and lifecycle, is now `access.device_placement` and holds only where an access-control device is placed. Tenancy owns and migrates this table; Access reads it only through this contract.\n",
  "required": [
   "id",
   "kind",
   "driver"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "$ref": "#/components/schemas/DeviceKind"
   },
   "driver": {
    "type": "string",
    "description": "Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change (ADR-0015).\n"
   },
   "identifier": {
    "type": "string",
    "nullable": true
   },
   "workstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control device (one with a `hardwareType`), which is placed in the gate topology by access `placeAccessDevice` rather than bound to a workstation (ADR-0067); `registerDevice` refuses either mistake with `422`.\n"
   },
   "model": {
    "type": "string",
    "nullable": true
   },
   "hardwareType": {
    "$ref": "../shared/common.yaml#/components/schemas/DeviceHardwareType",
    "nullable": true,
    "description": "**The specific hardware under `kind`** (ADR-0067, 1 October): Access's hardware types (a speed gate, a tripod turnstile, a podium) merged into the one register. Null for a device with no finer type than its kind.\n"
   },
   "hardwareModelId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The model in the hardware library (access `setHardwareModel`; ADR-0067). Access owns the library; this names a model in it.\n"
   },
   "serialNumber": {
    "type": "string",
    "nullable": true,
    "maxLength": 100,
    "description": "The manufacturer's serial (ADR-0067: was on the access-control device row, now `access.device_placement`). A serial already registered in the tenant is refused `409` by `registerDevice`.\n"
   },
   "ipNetworkReference": {
    "type": "string",
    "nullable": true,
    "description": "Network address or reference the device is reached at (ADR-0067)."
   },
   "configurationVersion": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Access configuration version the device reports running (ADR-0067)."
   },
   "localRuleVersion": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Admission rule package the device reports running (ADR-0067)."
   },
   "credentialSecurityPackageVersion": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Credential security package the device reports running (ADR-0067)."
   },
   "scannerHealth": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Component health as the device or vendor reports it on its heartbeat (ADR-0067)."
   },
   "controllerHealth": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "cameraHealth": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Where the device has a camera."
   },
   "connectivity": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Reported connectivity."
   },
   "pushToken": {
    "type": "string",
    "format": "password",
    "nullable": true,
    "writeOnly": true,
    "description": "BL-163. **Guest devices register for push and staff devices did not** — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has to walk to.\nWrite-only, and marked `writeOnly`: accepted by `registerDevice` and never returned by `listDevices` or `getDevice`. **A push token is a credential**, and the rule that no surface holds a provider key applies here too.\n"
   },
   "pushPlatform": {
    "type": "string",
    "nullable": true,
    "enum": [
     "ios",
     "android",
     "web",
     "windows"
    ]
   },
   "pushFailureCount": {
    "type": "integer",
    "default": 0,
    "readOnly": true,
    "description": "**Consecutive failures.** A token that has failed repeatedly is a device that was wiped or reassigned, and continuing to push to it is how a notification queue fills with nothing.\n"
   },
   "offlineScope": {
    "type": "string",
    "nullable": true,
    "enum": [
     "none",
     "readOnly",
     "sellAndScan",
     "fullVenue"
    ],
    "description": "BL-163. **What this device may do with no connection**, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it settled.\n**`fullVenue` on a personal handset is a decision, not a default** — a device that can do everything offline is a device that carries the whole venue's data in somebody's pocket.\n"
   },
   "firmwareVersion": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "As the device last reported it on its heartbeat."
   },
   "isRequired": {
    "type": "boolean",
    "description": "True blocks shift open when the device is unreachable."
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "online",
     "offline",
     "error",
     "consumableLow",
     "needsAttention",
     "localMode",
     "unknown"
    ],
    "description": "What the device last said on its heartbeat; `unknown` until it has. `localMode` is an access-control device validating from its offline package with its link down (ADR-0067).\n"
   },
   "batteryPercent": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "minimum": 0,
    "maximum": 100,
    "description": "Board 1 of the client's POS design set, 20 August. **A wristband encoder at 8% is a gate that stops working in an hour**, and nothing in the package carried it.\n**Null where the device has no battery**, which is most of them — a receipt printer reporting 100% forever is worse than one reporting nothing.\n"
   },
   "lastCheckedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "**Distinct from `lastHeartbeatAt`.** A heartbeat is the workstation saying the device is attached; a check is the device answering. **A printer with no paper heartbeats perfectly**, which is why the client's board shows both columns.\n"
   },
   "health": {
    "type": "string",
    "enum": [
     "healthy",
     "warning",
     "degraded",
     "offline",
     "unknown"
    ],
    "default": "unknown",
    "readOnly": true,
    "description": "**Derived, not reported.** Computed from heartbeat age, battery, firmware currency and error rate — a device does not know whether it is healthy, and asking it produces a fleet that is 100% healthy and 12% broken.\n"
   },
   "lastHeartbeatAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "capabilities": {
    "type": "array",
    "readOnly": true,
    "items": {
     "$ref": "#/components/schemas/DeviceCapability"
    },
    "description": "BL-179. **What this driver reports it can do, beyond reading media.** ADR-0015 is standards-first — the device does what the device does — and until now a venue could switch on a feature that depended on hardware without anything being able to say whether the hardware was there.\n**A capability absent is a capability unavailable**, not a capability assumed. A venue setting that requires one is refused where no device in scope reports it, rather than silently doing nothing at the gate.\n"
   },
   "enrolmentState": {
    "type": "string",
    "enum": [
     "registered",
     "enrolled",
     "provisioned",
     "active",
     "deactivated",
     "retired"
    ],
    "default": "registered",
    "readOnly": true,
    "description": "BL-160. **Where the device is in its life, which is not the same question as whether it is answering.** `enrolDevice` has taken the whole matrix — registered, enrolled, provisioned, active, deactivated, retired — since 16.1.2, and until now there was no column for it to land in, so the operation read this table and wrote nothing.\n**Distinct from `status` and from `health`.** `status` is what the device last said and `health` is what we computed from it; a decommissioned turnstile still sitting on the network is `online` and `retired` at once, and neither column contradicts the other. **A device that is `retired` is refused at the gate whatever its status says.**\nThe transition itself — who moved it, from what, and why — is a `tenancy.device_audit` record. It is not repeated here, because the latest transition stored in two places is one place to go stale.\n"
   },
   "retiredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "**Set when `enrolmentState` reaches `retired`, and null otherwise.** Derivable from `tenancy.device_audit`, and kept as a column for the same reason `maintenance.asset.retired_on` is one: a retirement date you reconstruct from an audit log is a date nobody filters a fleet by.\n"
   },
   "configurationProfileId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "**The profile this device was provisioned with.** `enrolDevice` has accepted one since 16.1.3 and there was nowhere to keep it, so the answer to *\"what is this reader configured as\"* lived only in the request that set it.\n"
   }
  }
 },
 "ReportResult": {
  "x-ticvai-persistence": "none — result set, cached in object storage",
  "type": "object",
  "required": [
   "executionId",
   "columns",
   "rows"
  ],
  "properties": {
   "executionId": {
    "type": "string"
   },
   "columns": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "key": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "type": {
       "$ref": "#/components/schemas/FieldType"
      }
     }
    }
   },
   "rows": {
    "type": "array",
    "description": "**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n",
    "items": {
     "type": "object",
     "additionalProperties": true
    }
   },
   "totals": {
    "type": "object",
    "additionalProperties": true,
    "description": "Aggregated columns only, keyed and typed as a row is."
   },
   "rowCount": {
    "type": "integer"
   },
   "nextCursor": {
    "type": "string",
    "nullable": true
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "dataAsOf": {
    "type": "string",
    "format": "date-time",
    "description": "Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"
   }
  }
 },
 "ReportingAnswerReliability": {
  "type": "string",
  "description": "**How far an analytics answer can be relied on** (decided 29 September, AI system design 5.6): a category, never a bare percentage. `grounded`: every figure comes from a result of the compiled spec. `partial`: part of the question was answered and the rest was not modelled. `conflictingSources`: the result and a cited source disagree. `insufficientEvidence`: the question could not be answered, including \"not available yet\" outside the semantic model. The same four values as `ai.yaml`'s assistant answers.\n",
  "enum": [
   "grounded",
   "partial",
   "conflictingSources",
   "insufficientEvidence"
  ]
 },
 "ReportingSemanticQuerySpec": {
  "x-ticvai-persistence": "none — embedded; stored whole in `reporting.natural_language_query`",
  "type": "object",
  "description": "**A question in the semantic model's own vocabulary** (decided 29 September, AI system design 2.2 E and 5.7). What the model returns for a live-number question instead of SQL, and what `runSemanticQuery` takes. Every code is a `SemanticModel` field code or a KPI code; Reporting validates the spec against the published model and compiles it deterministically, so the same spec compiles to the same SQL for the same model version.\n",
  "required": [
   "metric",
   "period"
  ],
  "properties": {
   "metric": {
    "type": "string",
    "description": "A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches them."
   },
   "dimensions": {
    "type": "array",
    "maxItems": 5,
    "description": "Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares.",
    "items": {
     "type": "string"
    }
   },
   "filters": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "field",
      "operator"
     ],
     "properties": {
      "field": {
       "type": "string",
       "description": "A `SemanticModel` field code."
      },
      "operator": {
       "type": "string",
       "enum": [
        "equals",
        "notEquals",
        "greaterThan",
        "lessThan",
        "between",
        "in",
        "notIn",
        "isNull",
        "isNotNull"
       ]
      },
      "values": {
       "type": "array",
       "description": "**Open on purpose; typed by the field.** One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and `notIn`, none for `isNull` and `isNotNull`.\n",
       "items": {}
      }
     }
    }
   },
   "period": {
    "type": "string",
    "description": "ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes."
   },
   "comparison": {
    "type": "string",
    "nullable": true,
    "description": "As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value.",
    "enum": [
     "previousPeriod",
     "samePeriodLastYear",
     "target",
     "benchmark"
    ]
   },
   "semanticModelVersion": {
    "type": "integer",
    "readOnly": true,
    "description": "The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting."
   }
  }
 },
 "ReportingUnavailableReason": {
  "type": "string",
  "description": "Which part of a question is outside the semantic model, so the answer is \"not available yet\" (design 5.7). A metric or field the caller may not see is reported as not modelled, so the reason does not reveal that it exists.",
  "enum": [
   "metricNotModelled",
   "dimensionNotModelled",
   "filterNotModelled",
   "comparisonNotAvailable",
   "periodOutsideHistory"
  ]
 },
 "RoleSummary": {
  "x-ticvai-persistence": "none — projection over role",
  "type": "object",
  "required": [
   "id",
   "code",
   "name"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "isPrimary": {
    "type": "boolean"
   }
  }
 },
 "RunReportRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "properties": {
   "parameters": {
    "type": "object",
    "additionalProperties": true,
    "description": "**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"
   },
   "dateFrom": {
    "type": "string",
    "format": "date",
    "description": "Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."
   },
   "dateTo": {
    "type": "string",
    "format": "date",
    "description": "Defaults to today in the venue's time zone when not sent (audit R158)."
   },
   "forceAsync": {
    "type": "boolean",
    "default": false,
    "description": "Queue regardless of size, for a result to be collected later."
   }
  }
 },
 "Segment": {
  "x-ticvai-persistence": "marketing.segment + marketing.segment_criterion",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateSegmentRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "lastEvaluatedSize": {
      "type": "integer",
      "nullable": true
     },
     "lastEvaluatedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
 },
 "SegmentCriterion": {
  "x-ticvai-persistence": "marketing.segment_criterion",
  "type": "object",
  "required": [
   "attribute",
   "operator"
  ],
  "properties": {
   "attribute": {
    "type": "string",
    "description": "Behavioural or profile attribute — visit count, last visit, lifetime value, product purchased, membership tier, venue visited, language.\n**Free-form rather than an enum, which is why 22.14.8, 5.3.19 and 5.5.17b were readable as gaps and are not.** `walletBalance`, `engagementTier` and `portfolioScope` are expressible today; what was missing was anybody saying so.\n**Three that need saying, because the naive reading is wrong:**\n`walletBalance` should segment on **`cash` credit only**. A guest with 200 dirhams of promotional credit expiring Friday is a different campaign from one with 200 of their own money, and treating them alike sends a spend-it-now message to somebody who was given it.\n`walletBalance.expiringWithinDays` is the segment that earns the attribute — **credit about to expire unspent is a guest about to be disappointed and a venue about to book breakage**, and only one of those is worth a message.\n`portfolioScope` aggregates across a `DelegatedAccess` delegation (CF-132) and **must not message every member about a household total** — that is how a venue tells a teenager what their parent spends.\n`entitlementExpiringWithinDays` (29 September, build pass, group G2; 5.5.30): the guest holds a ticket or pass in `issued` or `partiallyConsumed` whose `validTo` is within that many days, kept current from `entitlement.expiringSoon` and the entitlement read model. **Unused passes about to lapse** are this attribute with `entitlementRemainingUses` greater than zero.\n"
   },
   "operator": {
    "type": "string",
    "enum": [
     "equals",
     "notEquals",
     "greaterThan",
     "lessThan",
     "between",
     "in",
     "notIn",
     "exists",
     "notExists",
     "withinDays"
    ]
   },
   "value": {},
   "values": {
    "type": "array",
    "items": {}
   }
  }
 },
 "SegmentPreview": {
  "x-ticvai-persistence": "none — evaluated live",
  "type": "object",
  "required": [
   "segmentId",
   "matchingCount",
   "reachable"
  ],
  "properties": {
   "segmentId": {
    "type": "string",
    "format": "uuid"
   },
   "matchingCount": {
    "type": "integer"
   },
   "reachable": {
    "type": "array",
    "description": "Per channel, after consent and suppression. A segment of 50,000 with 3,000 email consents is a 3,000-person campaign.\n",
    "items": {
     "type": "object",
     "properties": {
      "channel": {
       "$ref": "#/components/schemas/MessageChannel"
      },
      "reachableCount": {
       "type": "integer"
      },
      "excludedNoConsent": {
       "type": "integer"
      },
      "excludedSuppressed": {
       "type": "integer"
      },
      "excludedNoAddress": {
       "type": "integer"
      }
     }
    }
   },
   "evaluatedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "StockBatch": {
  "type": "object",
  "x-ticvai-persistence": "inventory.stock_batch",
  "description": "BL-122. **`isPerishable` and `shelfLifeDays` are on the item, so a shelf life is declared and never instantiated.** Two deliveries of the same milk arriving a week apart are one stock level with one implied expiry, and the older one is invisible.\n**A batch is the instance that actually expires.** Without it, first-expiry-first-out is not computable and a venue discovers the problem by smell.\n",
  "required": [
   "id",
   "itemId",
   "locationId",
   "quantity",
   "receivedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "itemId": {
    "type": "string",
    "format": "uuid"
   },
   "locationId": {
    "type": "string",
    "format": "uuid"
   },
   "batchCode": {
    "type": "string",
    "nullable": true
   },
   "lotNumber": {
    "type": "string",
    "nullable": true,
    "description": "The supplier's own reference. **A recall names a lot number**, and an inventory that cannot resolve one has to discard everything.\n"
   },
   "quantity": {
    "type": "number"
   },
   "receivedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "supplierId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "available",
     "quarantined",
     "expired",
     "recalled",
     "consumed",
     "written-off"
    ]
   }
  }
 },
 "StockValuation": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "asAt",
   "total",
   "byLocation"
  ],
  "properties": {
   "asAt": {
    "type": "string",
    "format": "date"
   },
   "total": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "byLocation": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "locationId": {
       "type": "string",
       "format": "uuid"
      },
      "locationName": {
       "type": "string"
      },
      "value": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "itemCount": {
       "type": "integer"
      }
     }
    }
   },
   "byCategory": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "categoryId": {
       "type": "string",
       "format": "uuid"
      },
      "categoryName": {
       "type": "string"
      },
      "value": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "Suggestion": {
  "type": "object",
  "x-ticvai-persistence": "ai.suggestion",
  "description": "One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n",
  "required": [
   "id",
   "kind",
   "basis",
   "maturity",
   "producedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/SuggestionKind"
   },
   "basis": {
    "$ref": "#/components/schemas/SuggestionBasis"
   },
   "scopePath": {
    "type": "string"
   },
   "subjectRef": {
    "type": "string",
    "nullable": true,
    "description": "What it is about — a product, an outlet, an item, a party."
   },
   "value": {
    "type": "object",
    "additionalProperties": true,
    "description": "The suggestion itself. Shape depends on `kind`."
   },
   "confidence": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "maximum": 1,
    "description": "**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"
   },
   "explanation": {
    "type": "string",
    "description": "**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"
   },
   "inputs": {
    "type": "object",
    "additionalProperties": true,
    "description": "What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"
   },
   "producerRef": {
    "type": "string",
    "description": "The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"
   },
   "maturity": {
    "$ref": "#/components/schemas/AiMaturity"
   },
   "producedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"
   }
  }
 },
 "SuggestionBasis": {
  "type": "string",
  "description": "**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n",
  "enum": [
   "heuristic",
   "statistical",
   "model",
   "hybrid",
   "manual"
  ]
 },
 "SuggestionKind": {
  "type": "string",
  "description": "What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n",
  "enum": [
   "price",
   "replenishment",
   "requisition",
   "demandForecast",
   "prepPlan",
   "menuEngineering",
   "staffing",
   "slaTarget",
   "waitTime",
   "upsell",
   "segmentation",
   "anomaly",
   "scenario",
   "sendTime",
   "wasteRisk",
   "queueBalancing",
   "itinerary"
  ]
 },
 "SuggestionOutcome": {
  "type": "object",
  "x-ticvai-persistence": "ai.suggestion_outcome",
  "description": "**What actually happened, and this is the table that makes the swap possible at all.**\nA model needs labelled data and **the only source of labels is whether the venue took the advice and whether it worked.** A platform that suggests and never records the outcome has no training set a year later, and the swap he is planning for never happens.\n**Captured whether or not the suggestion was taken.** A rejected suggestion is a stronger signal than an accepted one — it is the case the rule got wrong.\n",
  "required": [
   "id",
   "suggestionId",
   "decision"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "suggestionId": {
    "type": "string",
    "format": "uuid"
   },
   "decision": {
    "type": "string",
    "enum": [
     "accepted",
     "modified",
     "rejected",
     "ignored",
     "expired"
    ]
   },
   "actualValue": {
    "type": "object",
    "nullable": true,
    "additionalProperties": true,
    "description": "What the venue did instead. **The label.** A suggestion of 400 units, an order of 250, and a stockout on Saturday is one training example worth more than a hundred accepted ones.\n"
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time"
   },
   "realisedOutcome": {
    "type": "object",
    "nullable": true,
    "additionalProperties": true,
    "description": "**Filled in later by a job, not by a person.** Whether the stockout happened, whether the covers arrived, whether the margin held — nobody comes back to record this by hand, so nothing that depends on them doing so should be designed.\n"
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**Added 29 September (AI design 3.1):** `ai.suggestion_outcome` had no scope column and no declared owner, so no policy. The suggestion's scope, copied when the outcome is recorded.\n"
   }
  }
 }
}
```
