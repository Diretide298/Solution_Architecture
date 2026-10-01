# P08-venue-operations-01 — P08 · Venue Operations (1 of 2)

**10 screens · 85 operations · 117 schemas · 33 permissions**

Platform P08 Venue Management · ships as **venue-management** ·
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
| `BUNDLE.md` | **The one file to hand a design session.** This brief; then **Screen by screen**, a full specification of each screen (what the user enters and picks, what it shows and produces, every state, who may do what, the requirements it meets, what the client said about it in the meetings, the tracker items, what the tenant configures, the references and an acceptance checklist); then what applies to the whole batch; then the raw data. |
| `screens.json` | Every field of every screen in the batch, as the package holds it. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 33 permissions apply here:
  `ACCESS_OVERRIDE, ACCESS_POINT_CONFIGURE, ACCESS_VALIDATE, ASSET_VIEW, AUDIT_VIEW, DEVELOPER_MANAGE, DEVELOPER_VIEW, DEVICE_CONFIGURE, DEVICE_MANAGE, DEVICE_VIEW, INCIDENT_MANAGE, INCIDENT_VIEW`…. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
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
| `BO-036` | Device Registry | B–D | 48 | 81 | 6 | 70 | 10 | 0 | — | notStarted (generated) |
| `BO-044` | F&B Outlets | A | 72 | 95 | 6 | 11 | 0 | 0 | — | notStarted (generated) |
| `BO-058` | Reporting Home | B–D | 79 | 47 | 6 | 100 | 2 | 0 | — | notStarted (generated) |
| `BO-060` | Attendance & Footfall | B–D | 99 | 70 | 6 | 153 | 1 | 0 | — | notStarted (generated) |
| `BO-064` | Zones & Areas | A | 31 | 44 | 6 | 30 | 0 | 0 | — | notStarted (generated) |
| `BO-067` | Integrations | B–D | 13 | 44 | 6 | 27 | 1 | 0 | — | notStarted (generated) |
| `BO-070` | Work Orders | B–D | 61 | 41 | 6 | 17 | 6 | 2 | — | notStarted (generated) |
| `BO-100` | Venue Home | B–D | 4 | 43 | 6 | 18 | 2 | 0 | — | notStarted (generated) |
| `BO-108` | Venue Operations | B–D | 6 | 67 | 6 | 34 | 0 | 0 | — | notStarted (generated) |
| `BO-128` | Live Workstation Health Monitor | B–D | 10 | 18 | 6 | 0 | 9 | 6 | — | notStarted (generated) |

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

### Across P08 Venue Management

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

### In P08 · Venue Operations

- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*

### Screen by screen

**`BO-036` Device Registry**

- Asset record: purchase date, warranty status/expiry, supplier, serial, manufacturer; ownership and responsibility shown separately (venue owns, operations responsible); a visual map shows installation location. *(client request · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-895)*
- Inventory counts by status (assigned, under maintenance, in stock) - e.g. 15 receipt printers broken down by ticketing, retail, F&B and in store. *(client request · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-894)*
- 360 device view shows status and workstation; reassign to another workstation or deactivate with a logged reason; lifecycle view tracks registration -> enrolment -> assignment -> reassignment. *(client request · MoM 15 Sep 2026, 4.3 Device Management - Registration, Enrollment & Workstation Assignment · DI-893)*
- Device directory: search and add devices (printers, scanners, customer displays, cash drawers, turnstiles, handhelds, mobile POS) capturing serial number, type and model; adding generates a secure enrolment code; devices are assigned to workstations (e.g. A has ticket printer, receipt printer and cash drawer). *(client request · MoM 15 Sep 2026, 4.3 Device Management - Registration, Enrollment & Workstation Assignment · DI-892)*
- Hardware and peripherals list nine device kinds, each with status, battery and last check. *(agreed · client-design-boards-audit 20 Aug 2026, What the boards give us - 1D Hardware & Peripherals · DI-402)*
- Workstation details: six tabs, a health score, a current-operator card with role and shift, IP address, configuration profile with version and deployment date, and a today's summary (transactions, refunds, cash collected). *(agreed · client-design-boards-audit 20 Aug 2026, What the boards give us - 1C Workstation Details · DI-401)*
- Hardware & peripheral management per workstation (receipt printer, cash drawer, payment terminal, barcode/ticket scanner, ticket printer) with device-level status. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-303)*
- New workstation form: name, auto-generated ID, department, mode; workstation detail: ID, department, IP address, configuration, linked devices, operator/shift activity and sales totals. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-302)*
- Workstation overview dashboard: all workstations for a venue (or across venues), grouped by department and sub-department, with online/offline/health status and type (mobile POS, kiosk, on-site POS). *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-301)*
- Each workstation records its connected devices (receipt printer, barcode scanner, ticket printer) so a cashier signing in there gets the right hardware automatically; every workstation has its own activity log and rights. *(agreed · MoM 7 Aug 2026, 3. Operating Areas, Workstations & Permissions Hierarchy · DI-150)*

**`BO-058` Reporting Home**

- Report library filterable by site, operating area, sales channel, workstation or user; e.g. Sales Report (payment-method breakdown, totals, voids, deposits, itemised ticket sales) and Payment Summary (per-cashier breakdown). *(agreed · MoM 7 Aug 2026, 21. Dashboards & Reporting · DI-183)*
- Sales reporting can be scoped to an operating area, showing all transactions from its workstations. *(agreed · MoM 7 Aug 2026, 3. Operating Areas, Workstations & Permissions Hierarchy · DI-151)*

**`BO-060` Attendance & Footfall**

- Admission Summary dashboard: real-time headcount of guests inside the venue from ticket scans. *(agreed · MoM 7 Aug 2026, 21. Dashboards & Reporting · DI-182)*

**`BO-067` Integrations**

- Financial year/period setup varies by country (UAE Jan–Dec, India Apr–Mar); closing a period locks further postings. An ERP integration centre manages external connections. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-263)*

**`BO-070` Work Orders**

- Smart assignment (confirmed by the maintenance head): technicians ranked by skill, shift and load; the ranking assigns nothing and Assign on a row does; outside vendor requests listed on the work order. *(agreed · MoM 17 Sep 2026, M17-13 · DI-924)*
- Work-order priority is shown with its source side by side (scored by venue policy, asset override, or manual); an asset carries a "fault priority override"; a new work order leaves priority empty to be scored; the venue sets weights and bands (safety, guest operations, revenue, asset criticality, summing to 100). *(agreed · MoM 17 Sep 2026, M17-01 · DI-923)*
- Work orders assigned to a technician must be visible on a technician-facing mobile app so field staff see assigned tasks and act directly from their device; execution shows a repair checklist, spare parts/tools consumed, a timeline (assigned, started, part requests) and a functional-test checklist before completion. *(client request · MoM 17 Sep 2026, 4.4 Work Order Management & Execution · DI-911)*
- Corrective-maintenance priority combines a configurable weighted scoring model (e.g. P1 emergency when guest operations are affected) with a direct per-asset priority override field: "if this specific device goes down, raise this priority level". *(agreed · MoM 17 Sep 2026, 4.3 Corrective & Emergency Maintenance · DI-909)*
- Calendars must support filtering by asset category so a team only sees maintenance relevant to them, e.g. an IT team sees turnstiles, printers and POS terminals, not unrelated categories. *(agreed · MoM 17 Sep 2026, 4.2 Preventive Maintenance Planning · DI-908)*
- Device maintenance: preventive cycles (quarterly, half-yearly, seasonal) on a calendar by device type; staff log faulty devices which raise work orders; diagnostic workspace for the engineer; warranty and maintenance history; return to service. *(client request · MoM 15 Sep 2026, 4.6 Device Maintenance & Lifecycle Servicing · DI-902)*

**`BO-100` Venue Home**

- Offline policies and a venue-level Operations Summary dashboard aggregating department-level views into one venue overview. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-311)*
- The dashboard is the venue command centre: KPI cards (Total Revenue, Tickets Sold, Net Profit, Avg. Order Value, each with delta vs last 7 days); Live Visitors with capacity % and "Updated just now"; Revenue Overview (Day/Week/Month/Year); AI Insights (e.g. "Increase VIP ticket price by 8%"); Sales by Channel; Operational Status per area (Operational/Attention); Activity Feed; Top Events; At a Glance strip. *(agreed · Design Vision Book 29 Jul 2026, 04 Dashboard Vision (p4) - dashboard content · DI-031)*

**`BO-128` Live Workstation Health Monitor**

- Performance monitoring shows successful vs failed validations and scan response time; configurable alert rules (e.g. low battery, device offline) with escalation for unresolved alerts. *(client request · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-901)*
- **Open question.** Open: can health metrics such as handheld battery be read via the manufacturer's SDK in-app rather than by physical inspection? Depends on each vendor SDK; to confirm during integration. *(open · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-900)*
- One screen shows live online/offline status of every workstation and device (printers, turnstiles, handheld scanners); a 360 health view shows connectivity, CPU/memory, storage and temperature. *(client request · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-899)*
- Workstation health is shown as a percentage score a manager can sort by, not only a last-heartbeat timestamp. *(agreed · client-design-boards-audit 20 Aug 2026, Genuine functional gaps - workstation health score · DI-403)*
- Workstation details: six tabs, a health score, a current-operator card with role and shift, IP address, configuration profile with version and deployment date, and a today's summary (transactions, refunds, cash collected). *(agreed · client-design-boards-audit 20 Aug 2026, What the boards give us - 1C Workstation Details · DI-401)*
- Offline policies and a venue-level Operations Summary dashboard aggregating department-level views into one venue overview. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-311)*
- **Open question.** Live workstation monitor with department-level health; proposed graphical park-map view of workstation locations and live status, depending on venue zone metadata, with manual drag-and-drop placement as fallback. *(open · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-304)*
- Hardware & peripheral management per workstation (receipt printer, cash drawer, payment terminal, barcode/ticket scanner, ticket printer) with device-level status. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-303)*
- Workstation overview dashboard: all workstations for a venue (or across venues), grouped by department and sub-department, with online/offline/health status and type (mobile POS, kiosk, on-site POS). *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-301)*
