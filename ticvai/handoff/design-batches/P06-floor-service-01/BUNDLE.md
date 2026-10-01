# P06-floor-service-01 — P06 · Floor Service

**10 screens · 38 operations · 43 schemas · 6 permissions**

Platform P06 Venue Staff App · ships as **venue-staff-mobile** ·
staff audience · mobileApp ·
offline-capable

## Who this is for

**staff on mobileApp.** Everything below is how you know what is
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
  `GUEST_MANAGE, GUEST_VIEW, ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, PRODUCT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **22 of these operations work offline**: addGuestNote, compItem, createFnbOrder, createPayment, fireCourse, getBill, getTableMap, getTableVisit
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `EMP-051` | Restaurant Service Command Center | listDetail | 3 | 0 | — |
| `EMP-052` | Floor Plan & Table Map | statusTracker | 2 | 1 | — |
| `EMP-053` | Table & Seating Configuration | configEditor | 4 | 0 | — |
| `EMP-054` | Reservation Calendar & Timeline | listDetail | 1 | 0 | — |
| `EMP-055` | Create / Edit Reservation | configEditor | 2 | 1 | — |
| `EMP-056` | Walk-In & Waitlist Management | configEditor | 2 | 1 | — |
| `EMP-057` | Guest Profile & Dining History | listDetail | 5 | 2 | — |
| `EMP-058` | Live Table & Service Management | configEditor | 17 | 14 | — |
| `EMP-059` | Table Order, Bill & Payment Management | statusTracker | 8 | 7 | — |
| `EMP-060` | Reservation & Table Performance | listDetail | 2 | 0 | — |

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

### Across P06 Venue Staff App

- From the case screen agents act on the customer's bookings/tickets (date change, reschedule, resend tickets), initiate refunds/compensation, route for internal approval, or escalate to another department, which sees it on that department's mobile app. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-542)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Staff-facing POS and tablet UIs always carry TICVAI branding, not client branding. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-296)*
- Approval screens offer Approve, Reject, Return and Request More Information, show an AI-generated approval summary beside the request, and a visible trail of who approved at each stage (e.g. IT → Ops Manager → Finance → CEO → IT publishes). *(client request · MoM 10 Aug 2026, 5.5 Multi-Stage Approval Workflow · DI-235)*
- Two separate apps: an access-control app (handhelds or fixed terminals) scoped purely to entry validation/scanning, and an employee app (approvals, alerts/messages, matrix features) that may include a basic ticket-validity lookup but not full scanning. *(agreed · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-128)*
- Offline state must be clearly visible in the UI, e.g. a visible mode indicator or greyed-out unavailable functions; exact visual treatment to be settled in the UI/UX session. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-072)*
- Allam: the app detects loss of connectivity and switches to offline mode automatically, without cashier action, then restores online mode and syncs pending transactions automatically. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-071)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Allam: the platform is device-agnostic (Android, iOS and web) so sales can continue on any available device. *(agreed · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-068)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

### Screen by screen

**`EMP-052` Floor Plan & Table Map**

- Allam: a realistic, to-scale visual floor plan reflecting the actual hall layout and table shapes (square, rectangular) across multiple dining areas/halls, instead of a generic list. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-793)*
- Tables are colour-coded by status (vacant, occupied, reserved) and filterable by status. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-792)*
- Qossai asked if guests pick a specific table; Allam: table choice can be an option, but the default is the guest gives party size and the system/host allocates a table. *(agreed · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Dining) · DI-689)*
- Decision: table status flow is Available → Ordered → Table Closed (after payment) → Reserved (booked in advance). No "Cleaning" status — cleaning is a manual staff task, deliberately excluded to avoid complexity. *(agreed · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining); 5. Key Decisions · DI-336)*
- A visual floor/table map (main hall, terrace, VIP lounge, etc.) shows table status, and tables can be tagged with a customer category (e.g. VIP) so staff prioritise service. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-335)*
- Allam: replace the dated table layout with a modern, graphical table map where two-seat and four-seat tables look visually distinct; the cashier selects a table then enters the number of covers. *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-104)*

**`EMP-053` Table & Seating Configuration**

- Allam: a realistic, to-scale visual floor plan reflecting the actual hall layout and table shapes (square, rectangular) across multiple dining areas/halls, instead of a generic list. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-793)*

**`EMP-054` Reservation Calendar & Timeline**

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*

**`EMP-055` Create / Edit Reservation**

- The client's FnB Board 4 draws a guest duplicate-match and merge process on reservation create/edit and the guest profile: proposed matches shown as candidates, and the merge confirmed by the user. *(agreed · design-brief-9-september 9 Sep 2026, 2 (f) duplicateMatch · DI-808)*
- Table reservation captures table selection (with system recommendations), customer details, guest count, location/outlet and an optional deposit adjusted against the final bill; walk-in and waitlist management are also supported. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-337)*

**`EMP-056` Walk-In & Waitlist Management**

- Table reservation captures table selection (with system recommendations), customer details, guest count, location/outlet and an optional deposit adjusted against the final bill; walk-in and waitlist management are also supported. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-337)*

**`EMP-057` Guest Profile & Dining History**

- The client's FnB Board 4 draws a guest duplicate-match and merge process on reservation create/edit and the guest profile: proposed matches shown as candidates, and the merge confirmed by the user. *(agreed · design-brief-9-september 9 Sep 2026, 2 (f) duplicateMatch · DI-808)*
- Decision: one unified customer profile across ticketing, F&B and retail gives a 360° view of guest activity and avoids duplicates; e.g. a guest who buys tickets online and later dines is matched by name/mobile to the same profile. *(agreed · MoM 18 Aug 2026, 4.9 Unified Customer Profile · DI-339)*

**`EMP-058` Live Table & Service Management**

- Each table has an activity log (seated, drinks ordered, food ordered, sent to kitchen, course served, etc.) and actions Add Guest, Change Server and Transfer Table. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-338)*
- Decision: table status flow is Available → Ordered → Table Closed (after payment) → Reserved (booked in advance). No "Cleaning" status — cleaning is a manual staff task, deliberately excluded to avoid complexity. *(agreed · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining); 5. Key Decisions · DI-336)*
- A visual floor/table map (main hall, terrace, VIP lounge, etc.) shows table status, and tables can be tagged with a customer category (e.g. VIP) so staff prioritise service. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-335)*
- Support both service models: quick-service (order and pay at the counter before food is served) and fine dining (table opened, items added over the visit, bill printed and paid at the end). *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-105)*

**`EMP-059` Table Order, Bill & Payment Management**

- Table/seat-level structure supports flexible bill-splitting: by amount, by number of covers, or by category (e.g. one guest pays food, another drinks). *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-106)*
- Support both service models: quick-service (order and pay at the counter before food is served) and fine dining (table opened, items added over the visit, bill printed and paid at the end). *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-105)*

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "EMP-051",
  "name": "Restaurant Service Command Center",
  "module": "Floor Service",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/restaurant-service-command-center",
   "component": "apps/venue-staff-app/src/routes/operations/RestaurantServiceCommandCenterDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product."
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4a`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Restaurant Service Command Center* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4a"
  ],
  "pattern": "listDetail",
  "patternReason": "`listTableReservations` reads the population and `getTableMap` reads one of them — list, select, act",
  "purpose": "Restaurant Service Command Center — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Outlet id",
       "operation": "listTableReservations",
       "notes": "Sends `?outletId=` to `listTableReservations`.",
       "provenance": "contract fnb.yaml GET /table-reservations"
      },
      {
       "kind": "datePicker",
       "label": "Date",
       "operation": "listTableReservations",
       "notes": "Sends `?date=` to `listTableReservations`.",
       "provenance": "contract fnb.yaml GET /table-reservations"
      },
      {
       "kind": "dataTable",
       "label": "Every table reservation",
       "bindsTo": "TableReservation",
       "columns": [
        "TableReservation.id",
        "TableReservation.outletId",
        "TableReservation.subjectId",
        "TableReservation.guestName",
        "TableReservation.contactPoint",
        "TableReservation.partySize",
        "TableReservation.startsAt",
        "TableReservation.durationMinutes",
        "TableReservation.tables[].tableId",
        "TableReservation.status",
        "TableReservation.groupId",
        "TableReservation.notes"
       ],
       "operation": "listTableReservations",
       "provenance": "contract fnb.yaml GET /table-reservations"
      },
      {
       "kind": "dataTable",
       "label": "Every F&B order",
       "bindsTo": "FnbOrder",
       "columns": [
        "FnbOrder.id",
        "FnbOrder.orderNumber",
        "FnbOrder.outletId",
        "FnbOrder.serviceMode",
        "FnbOrder.tableVisitId",
        "FnbOrder.status",
        "FnbOrder.lines",
        "FnbOrder.salesOrderId",
        "FnbOrder.grossAmount",
        "FnbOrder.taxAmount",
        "FnbOrder.kitchenTicketId",
        "FnbOrder.estimatedReadyAt"
       ],
       "operation": "listFnbOrders",
       "provenance": "contract fnb.yaml GET /fnb-orders"
      },
      {
       "kind": "searchField",
       "label": "Search restaurant service command center",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
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
       "label": "The selected table reservation",
       "bindsTo": "TableReservation",
       "columns": [
        "TableReservation.id",
        "TableReservation.outletId",
        "TableReservation.subjectId",
        "TableReservation.guestName",
        "TableReservation.contactPoint",
        "TableReservation.partySize",
        "TableReservation.startsAt",
        "TableReservation.durationMinutes",
        "TableReservation.tables",
        "TableReservation.status",
        "TableReservation.groupId",
        "TableReservation.notes",
        "TableReservation.actualPartySize",
        "TableReservation.tableVisitId"
       ],
       "operation": "listTableReservations",
       "provenance": "contract fnb.yaml GET /table-reservations"
      },
      {
       "kind": "detailPanel",
       "label": "The table map",
       "bindsTo": "TableMap",
       "columns": [
        "TableMap.outletId",
        "TableMap.zones",
        "TableMap.tables"
       ],
       "operation": "getTableMap",
       "provenance": "contract fnb.yaml GET /outlets/{outletId}/tables"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The restaurant service list.",
   "error": "Could not load. Names which read failed and leaves the restaurant service untouched.",
   "emptyFirstRun": "No restaurant service yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on outletId, date and the restaurant service are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `getTableMap` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "getTableMap",
    "contract": "fnb",
    "purpose": "Table map with live state",
    "trigger": "onLoad"
   },
   {
    "operationId": "listTableReservations",
    "contract": "fnb",
    "purpose": "Bookings for a service period",
    "trigger": "onLoad"
   },
   {
    "operationId": "listFnbOrders",
    "contract": "fnb",
    "purpose": "List F&B orders",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "outletId",
     "from": "EMP-003"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to.",
   "preloaded": [
    "TableReservation.id",
    "TableReservation.outletId",
    "TableReservation.subjectId",
    "TableReservation.guestName",
    "TableReservation.contactPoint"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-051",
   "derivedFrom": "wireframes/reference/FnB Board 4.dc.html",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-052",
  "name": "Floor Plan & Table Map",
  "module": "Floor Service",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/floor-plan-table-map",
   "component": "apps/venue-staff-app/src/routes/operations/FloorPlanTableMapDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product."
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4b`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Floor Plan &amp; Table Map* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4b"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getTableMap` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Floor Plan & Table Map — from the client design board, 20 August.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The table map",
       "bindsTo": "TableMap",
       "columns": [
        "TableMap.outletId",
        "TableMap.zones",
        "TableMap.tables"
       ],
       "operation": "getTableMap",
       "provenance": "contract fnb.yaml GET /outlets/{outletId}/tables"
      },
      {
       "kind": "searchField",
       "label": "Search floor plan",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
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
       "label": "Save table layout",
       "operation": "setTableLayout",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/tables"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The floor plan table, read by `getTableMap`.",
   "error": "Could not load. Names which read failed and leaves the floor plan table untouched.",
   "emptyFirstRun": "No floor plan table yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `getTableMap` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "getTableMap",
    "contract": "fnb",
    "purpose": "Table map with live state",
    "trigger": "onLoad"
   },
   {
    "operationId": "setTableLayout",
    "contract": "fnb",
    "purpose": "Configure the table layout",
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
     "name": "outletId",
     "from": "EMP-003"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-052",
   "derivedFrom": "wireframes/reference/FnB Board 4.dc.html",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetTableLayout",
    "component": "modal",
    "trigger": "Save table layout",
    "body": "**Collects what `setTableLayout` sends before it is called.** Required: `tables`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save table layout",
     "operation": "setTableLayout"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "tables"
     ]
    },
    "provenance": "contract fnb.yaml PUT /outlets/{outletId}/tables"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-053",
  "name": "Table & Seating Configuration",
  "module": "Floor Service",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/table-seating-configuration",
   "component": "apps/venue-staff-app/src/routes/operations/TableSeatingConfigurationDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product."
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4c`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Table &amp; Seating Configuration* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4c"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`setTableLayout`) and no read of a population — it is settings, not a list",
  "purpose": "Table & Seating Configuration — from the client design board, 20 August.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "id",
       "bindsTo": "TableDefinition.id",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/tables"
      },
      {
       "kind": "textField",
       "label": "label",
       "bindsTo": "TableDefinition.label",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/tables"
      },
      {
       "kind": "textField",
       "label": "capacity",
       "bindsTo": "TableDefinition.capacity",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/tables"
      },
      {
       "kind": "textField",
       "label": "zone",
       "bindsTo": "TableDefinition.zone",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/tables"
      },
      {
       "kind": "textField",
       "label": "position",
       "bindsTo": "TableDefinition.position",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/tables"
      },
      {
       "kind": "textField",
       "label": "shape",
       "bindsTo": "TableDefinition.shape",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/tables"
      },
      {
       "kind": "searchField",
       "label": "Search table",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save table layout",
       "operation": "setTableLayout",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/tables"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved table seating.",
   "error": "Could not load. Names which read failed and leaves the table seating untouched.",
   "emptyFirstRun": "No table seating configured. The form opens empty and `setTableLayout` saves the first one; it says what the platform does in the meantime.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_CONFIGURE`, which `setTableLayout` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "setTableLayout",
    "contract": "fnb",
    "purpose": "Configure the table layout",
    "trigger": "onAction"
   },
   {
    "operationId": "createTable",
    "contract": "fnb",
    "purpose": "Add a table to the floor",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "updateTable",
    "contract": "fnb",
    "purpose": "Change a table's covers, shape or section",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "setSectionLayout",
    "contract": "fnb",
    "purpose": "Arrange the outlet's sections",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "outletId",
     "from": "EMP-003"
    },
    {
     "name": "tableId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-053",
   "derivedFrom": "wireframes/reference/FnB Board 4.dc.html",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-054",
  "name": "Reservation Calendar & Timeline",
  "module": "Floor Service",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/reservation-calendar-timeline",
   "component": "apps/venue-staff-app/src/routes/operations/ReservationCalendarTimelineDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product."
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4d`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Reservation Calendar &amp; Timeline* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4d"
  ],
  "pattern": "listDetail",
  "patternReason": "`listTableReservations` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Reservation Calendar & Timeline — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "calendarView",
       "label": "Calendar",
       "operation": "listTableReservations",
       "notes": "Reservations by hour; agenda view on the handheld. Day, week, month and agenda views; the day starts at the venue's `calendarDayStartHour`. Filters the category on what it read.",
       "provenance": "decided 29 September 2026, 17 September minutes M17-03 (applied 30 September)"
      },
      {
       "kind": "textField",
       "label": "Outlet id",
       "operation": "listTableReservations",
       "notes": "Sends `?outletId=` to `listTableReservations`.",
       "provenance": "contract fnb.yaml GET /table-reservations"
      },
      {
       "kind": "datePicker",
       "label": "Date",
       "operation": "listTableReservations",
       "notes": "Sends `?date=` to `listTableReservations`.",
       "provenance": "contract fnb.yaml GET /table-reservations"
      },
      {
       "kind": "dataTable",
       "label": "Every table reservation",
       "bindsTo": "TableReservation",
       "columns": [
        "TableReservation.id",
        "TableReservation.outletId",
        "TableReservation.subjectId",
        "TableReservation.guestName",
        "TableReservation.contactPoint",
        "TableReservation.partySize",
        "TableReservation.startsAt",
        "TableReservation.durationMinutes",
        "TableReservation.tables[].tableId",
        "TableReservation.status",
        "TableReservation.groupId",
        "TableReservation.notes"
       ],
       "operation": "listTableReservations",
       "provenance": "contract fnb.yaml GET /table-reservations"
      },
      {
       "kind": "searchField",
       "label": "Search reservation calendar",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
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
       "label": "The selected table reservation",
       "bindsTo": "TableReservation",
       "columns": [
        "TableReservation.id",
        "TableReservation.outletId",
        "TableReservation.subjectId",
        "TableReservation.guestName",
        "TableReservation.contactPoint",
        "TableReservation.partySize",
        "TableReservation.startsAt",
        "TableReservation.durationMinutes",
        "TableReservation.tables[].tableId",
        "TableReservation.status",
        "TableReservation.groupId",
        "TableReservation.notes",
        "TableReservation.actualPartySize",
        "TableReservation.tableVisitId"
       ],
       "operation": "listTableReservations",
       "provenance": "contract fnb.yaml GET /table-reservations"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reservation calendar timeline list.",
   "error": "Could not load. Names which read failed and leaves the reservation calendar timeline untouched.",
   "emptyFirstRun": "No reservation calendar timeline yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on outletId, date and the reservation calendar timeline are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_MODIFY`, which `listTableReservations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "listTableReservations",
    "contract": "fnb",
    "purpose": "Bookings for a service period",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to.",
   "preloaded": [
    "TableReservation.id",
    "TableReservation.outletId",
    "TableReservation.subjectId",
    "TableReservation.guestName",
    "TableReservation.contactPoint"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-054",
   "derivedFrom": "wireframes/reference/FnB Board 4.dc.html",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-055",
  "name": "Create / Edit Reservation",
  "module": "Floor Service",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/create-edit-reservation",
   "component": "apps/venue-staff-app/src/routes/operations/CreateEditReservationDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product."
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4e`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Create / Edit Reservation* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4e"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`createTableReservation`) and no read of a population — it is settings, not a list",
  "purpose": "Create / Edit Reservation — from the client design board, 20 August.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "id",
       "bindsTo": "TableReservation.id",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "outletId",
       "bindsTo": "TableReservation.outletId",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "subjectId",
       "bindsTo": "TableReservation.subjectId",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "guestName",
       "bindsTo": "TableReservation.guestName",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "contactPoint",
       "bindsTo": "TableReservation.contactPoint",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "partySize",
       "bindsTo": "TableReservation.partySize",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "startsAt",
       "bindsTo": "TableReservation.startsAt",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "durationMinutes",
       "bindsTo": "TableReservation.durationMinutes",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "tableIds",
       "bindsTo": "TableReservation.tables[].tableId",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "status",
       "bindsTo": "TableReservation.status",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "groupId",
       "bindsTo": "TableReservation.groupId",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "notes",
       "bindsTo": "TableReservation.notes",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "actualPartySize",
       "bindsTo": "TableReservation.actualPartySize",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "textField",
       "label": "tableVisitId",
       "bindsTo": "TableReservation.tableVisitId",
       "provenance": "contract fnb.yaml POST /table-reservations"
      },
      {
       "kind": "duplicateMatch",
       "label": "Possible existing guest",
       "notes": "**Runs while the booking is being typed, not after it is saved.** A duplicate created at the podium is one somebody has to find later. Proposes only — `matchGuest` never merges, and the reason each candidate matched is shown beside it.\n"
      },
      {
       "kind": "searchField",
       "label": "Search create / edit reservation",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "duplicateMatch",
       "label": "Possible existing guest",
       "notes": "**Runs while the booking is being typed, not after it is saved.** A duplicate created at the podium is one somebody has to find later. Proposes only — `matchGuest` never merges, and the reason each candidate matched is shown beside it.\n"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create table reservation",
       "operation": "createTableReservation",
       "provenance": "contract fnb.yaml POST /table-reservations",
       "notes": "**No deposit unless the venue switched the table deposit on** (decided 29 September, rev 3 REV3-8b, superseding audit R077 (a) \"no table deposit in the first release\"; the venue sets it on BO-327). With it off, or a party below its size, the booking is `booked`, takes no payment and the copy names no fee. Where it applies, `createTableReservation` returns `awaitingDeposit` with the deposit amount, basis and `holdExpiresAt`: the screen shows them, says the cover is held until then, and names the refund cut-off and the late-cancel and no-show terms from the policy. The deposit is paid through the cart (`addCartLine` with `tableReservationId`, then `checkoutCart`), at a till or by the guest; unpaid by `holdExpiresAt`, the booking is cancelled and the cover released."
      },
      {
       "kind": "duplicateMatch",
       "label": "Possible existing guest",
       "notes": "**Runs while the booking is being typed, not after it is saved.** A duplicate created at the podium is one somebody has to find later. Proposes only — `matchGuest` never merges, and the reason each candidate matched is shown beside it.\n"
      },
      {
       "kind": "secondaryButton",
       "label": "Find matches for guest",
       "operation": "matchGuest",
       "provenance": "contract marketing-crm.yaml POST /guests/match"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved create edit reservation.",
   "error": "Could not load. Names which read failed and leaves the create edit reservation untouched.",
   "emptyFirstRun": "No create edit reservation configured. The form opens empty and `createTableReservation` saves the first one; it says what the platform does in the meantime.",
   "emptyNoAccess": "Shown when the caller lacks `GUEST_VIEW`, which `matchGuest` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "createTableReservation",
    "contract": "fnb",
    "purpose": "Book a table in advance",
    "trigger": "onAction"
   },
   {
    "operationId": "matchGuest",
    "contract": "marketing-crm",
    "purpose": "Propose existing guests who may be the same person, before a second record is created",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-055",
   "derivedFrom": "wireframes/reference/FnB Board 4.dc.html",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formMatchGuest",
    "component": "modal",
    "trigger": "Find matches for guest",
    "body": "**Collects what `matchGuest` sends before it is called.** Nothing in the body is required. Optional: `name`, `phone`, `email`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Find matches for guest",
     "operation": "matchGuest"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "phone",
      "email"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /guests/match"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-056",
  "name": "Walk-In & Waitlist Management",
  "module": "Floor Service",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/walk-in-waitlist-management",
   "component": "apps/venue-staff-app/src/routes/operations/WalkInWaitlistManagementDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product."
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4f`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Walk-In &amp; Waitlist Management* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4f"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`joinRestaurantWaitlist`) and no read of a population — it is settings, not a list",
  "purpose": "Walk-In & Waitlist Management — from the client design board, 20 August.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "id",
       "bindsTo": "RestaurantWaitlist.id",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "textField",
       "label": "outletId",
       "bindsTo": "RestaurantWaitlist.outletId",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "textField",
       "label": "subjectId",
       "bindsTo": "RestaurantWaitlist.subjectId",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "textField",
       "label": "partySize",
       "bindsTo": "RestaurantWaitlist.partySize",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "textField",
       "label": "quotedWaitMinutes",
       "bindsTo": "RestaurantWaitlist.quotedWaitMinutes",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "textField",
       "label": "seatingPreference",
       "bindsTo": "RestaurantWaitlist.seatingPreference",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "textField",
       "label": "status",
       "bindsTo": "RestaurantWaitlist.status",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "textField",
       "label": "notifiedAt",
       "bindsTo": "RestaurantWaitlist.notifiedAt",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "textField",
       "label": "holdExpiresAt",
       "bindsTo": "RestaurantWaitlist.holdExpiresAt",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "searchField",
       "label": "Search walk-in",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Join restaurant waitlist",
       "operation": "joinRestaurantWaitlist",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "destructiveButton",
       "label": "Leave waitlist",
       "operation": "leaveRestaurantWaitlist",
       "provenance": "contract fnb.yaml POST /waitlist/{entryId}/leave",
       "notes": "Takes the selected party off the list; the entry returns `cancelled`, and a party already called releases its held table at once. Not `walkedAway`, which records a party that left without saying so (decided 28 September, audit R073 (d))."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved walk-in waitlist.",
   "error": "Could not load. Names which read failed and leaves the walk-in waitlist untouched.",
   "emptyFirstRun": "No walk-in waitlist configured. The form opens empty and `joinRestaurantWaitlist` saves the first one; it says what the platform does in the meantime.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_MODIFY`, which `joinRestaurantWaitlist` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "joinRestaurantWaitlist",
    "contract": "fnb",
    "purpose": "Add a party to an outlet's waitlist",
    "trigger": "onAction"
   },
   {
    "operationId": "leaveRestaurantWaitlist",
    "contract": "fnb",
    "purpose": "Take a party off the waitlist; the entry ends cancelled (audit R073 (d))",
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
     "name": "entryId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-056",
   "derivedFrom": "wireframes/reference/FnB Board 4.dc.html",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "confirmLeaveRestaurantWaitlist",
    "component": "confirmDialog",
    "trigger": "Leave waitlist",
    "body": "**Names the party and its place in the list.** `leaveRestaurantWaitlist` ends the entry `cancelled`; a party already called releases its held table at once. Optional: `note`, why the party left (audit R073 (d)).",
    "confirm": {
     "label": "Take them off the list",
     "operation": "leaveRestaurantWaitlist",
     "carries": [
      "entryId"
     ]
    },
    "dismiss": {
     "label": "Keep them",
     "discards": [
      "note"
     ]
    },
    "provenance": "contract fnb.yaml POST /waitlist/{entryId}/leave"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-057",
  "name": "Guest Profile & Dining History",
  "module": "Floor Service",
  "requiresModule": "marketing",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/guest-profile-dining-history",
   "component": "apps/venue-staff-app/src/routes/operations/GuestProfileDiningHistoryDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product."
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Drawn 31 August** — `FnB Board 4.dc.html` frame `fnb-4g`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Guest Profile &amp; Dining History* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4g"
  ],
  "pattern": "listDetail",
  "patternReason": "`listOrders` reads the population and `getGuestProfile` reads one of them — list, select, act",
  "purpose": "Guest Profile & Dining History — from the client design board, 20 August.",
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
       "kind": "duplicateMatch",
       "label": "Possible duplicates of this guest",
       "permission": "GUEST_MANAGE",
       "notes": "Candidates from `matchGuest`, each with the rule that matched it."
      },
      {
       "kind": "confirmDialog",
       "label": "Merge these two records",
       "permission": "GUEST_MANAGE",
       "notes": "**The consequence, stated before the act.** The losing record is superseded rather than deleted so a year of orders and consents keeps resolving; the merge is reversible for thirty days; and **consent takes the narrower of the two positions**, which is the one thing about a merge that is a regulatory question rather than a data one.\n"
      },
      {
       "kind": "searchField",
       "label": "Search guest profile",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "duplicateMatch",
       "label": "Possible duplicates of this guest",
       "permission": "GUEST_MANAGE",
       "notes": "Candidates from `matchGuest`, each with the rule that matched it."
      },
      {
       "kind": "confirmDialog",
       "label": "Merge these two records",
       "permission": "GUEST_MANAGE",
       "notes": "**The consequence, stated before the act.** The losing record is superseded rather than deleted so a year of orders and consents keeps resolving; the merge is reversible for thirty days; and **consent takes the narrower of the two positions**, which is the one thing about a merge that is a regulatory question rather than a data one.\n"
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
       "kind": "duplicateMatch",
       "label": "Possible duplicates of this guest",
       "permission": "GUEST_MANAGE",
       "notes": "Candidates from `matchGuest`, each with the rule that matched it."
      },
      {
       "kind": "confirmDialog",
       "label": "Merge these two records",
       "permission": "GUEST_MANAGE",
       "notes": "**The consequence, stated before the act.** The losing record is superseded rather than deleted so a year of orders and consents keeps resolving; the merge is reversible for thirty days; and **consent takes the narrower of the two positions**, which is the one thing about a merge that is a regulatory question rather than a data one.\n"
      },
      {
       "kind": "detailPanel",
       "label": "The guest profile",
       "bindsTo": "GuestProfileDetail",
       "columns": [
        "GuestProfileDetail.id",
        "GuestProfileDetail.subjectId",
        "GuestProfileDetail.displayName",
        "GuestProfileDetail.email",
        "GuestProfileDetail.phone",
        "GuestProfileDetail.preferredLanguage",
        "GuestProfileDetail.preferredChannel",
        "GuestProfileDetail.guestLinkId",
        "GuestProfileDetail.tags",
        "GuestProfileDetail.engagementScore",
        "GuestProfileDetail.engagementTier",
        "GuestProfileDetail.lifetimeValue",
        "GuestProfileDetail.visitCount",
        "GuestProfileDetail.lastVisitAt",
        "GuestProfileDetail.isActive",
        "GuestProfileDetail.mergedIntoSubjectId"
       ],
       "operation": "getGuestProfile",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Find matches for guest",
       "operation": "matchGuest",
       "provenance": "contract marketing-crm.yaml POST /guests/match"
      },
      {
       "kind": "destructiveButton",
       "label": "Merge guests",
       "operation": "mergeGuests",
       "provenance": "contract marketing-crm.yaml POST /guests/merge"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The guest profile dining list.",
   "error": "Could not load. Names which read failed and leaves the guest profile dining untouched.",
   "emptyFirstRun": "No guest profile dining yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on venueId, principalId, shiftId, status, createdFrom, createdTo and the guest profile dining are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `GUEST_VIEW`, which `getGuestProfile` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "getGuestProfile",
    "contract": "marketing-crm",
    "purpose": "Read a guest profile",
    "trigger": "onLoad"
   },
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "List orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "matchGuest",
    "contract": "marketing-crm",
    "purpose": "Find other records that may be this same person",
    "trigger": "onAction"
   },
   {
    "operationId": "mergeGuests",
    "contract": "marketing-crm",
    "purpose": "Merge a proposed duplicate into this profile, once a person has decided",
    "trigger": "onAction"
   },
   {
    "operationId": "addGuestNote",
    "contract": "marketing-crm",
    "purpose": "What the floor needs to know about this table",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "subjectId",
     "from": "EMP-003"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to.",
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
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-057",
   "derivedFrom": "wireframes/reference/FnB Board 4.dc.html",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formMatchGuest",
    "component": "modal",
    "trigger": "Find matches for guest",
    "body": "**Collects what `matchGuest` sends before it is called.** Nothing in the body is required. Optional: `name`, `phone`, `email`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Find matches for guest",
     "operation": "matchGuest"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "phone",
      "email"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /guests/match"
   },
   {
    "id": "confirmMergeGuests",
    "component": "confirmDialog",
    "trigger": "Merge guests",
    "body": "**Names what `mergeGuests` changes and what it leaves alone**, in the consequence rather than the verb. A guest profile dining this affects should be identified in the dialog, not just counted. **Collects what `mergeGuests` sends before it is called.** Required: `keepSubjectId`, `mergeSubjectIds`. Optional: `reason`.",
    "provenance": "contract marketing-crm.yaml POST /guests/merge"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-058",
  "name": "Live Table & Service Management",
  "module": "Floor Service",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/live-table-service-management",
   "component": "apps/venue-staff-app/src/routes/operations/LiveTableServiceManagementDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "exitTo": [
    "EMP-059",
    "EMP-060"
   ],
   "transitions": [
    {
     "to": "EMP-059",
     "trigger": "Food is ordered with courses",
     "provenance": "flow F29 step 2→3",
     "carries": [
      "visitId"
     ]
    },
    {
     "to": "EMP-060",
     "trigger": "Reservation & Table Performance",
     "provenance": "flow F80 step 2→3, F94 step 1→2",
     "carries": [
      "outletId"
     ]
    },
    {
     "to": "KIT-002",
     "trigger": "One main comes back wrong",
     "provenance": "flow F29 step 5→6",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "ticketId",
      "visitId"
     ]
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens. **Cross-platform navigation removed 24 August**: KIT-002. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4a",
   "FnB Board 4.dc.html#fnb-4b",
   "FnB Board 4.dc.html#fnb-4h"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`openTableVisit`, `updateTableVisit`, `mergeTableVisits`) and no read of a population — it is settings, not a list",
  "purpose": "Live Table & Service Management — from the client design board, 20 August.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "id",
       "bindsTo": "OpenTableVisitRequest.id",
       "provenance": "contract fnb.yaml POST /table-visits"
      },
      {
       "kind": "textField",
       "label": "tableId",
       "bindsTo": "OpenTableVisitRequest.tableId",
       "provenance": "contract fnb.yaml POST /table-visits"
      },
      {
       "kind": "textField",
       "label": "covers",
       "bindsTo": "OpenTableVisitRequest.covers",
       "provenance": "contract fnb.yaml POST /table-visits"
      },
      {
       "kind": "textField",
       "label": "serverPrincipalId",
       "bindsTo": "OpenTableVisitRequest.serverPrincipalId",
       "provenance": "contract fnb.yaml POST /table-visits"
      },
      {
       "kind": "textField",
       "label": "subjectId",
       "bindsTo": "OpenTableVisitRequest.subjectId",
       "provenance": "contract fnb.yaml POST /table-visits"
      },
      {
       "kind": "textField",
       "label": "recordedAt",
       "bindsTo": "OpenTableVisitRequest.recordedAt",
       "provenance": "contract fnb.yaml POST /table-visits"
      },
      {
       "kind": "detailPanel",
       "label": "The table visit",
       "bindsTo": "TableVisit",
       "columns": [
        "TableVisit.id",
        "TableVisit.tableId",
        "TableVisit.tableLabel",
        "TableVisit.outletId",
        "TableVisit.covers",
        "TableVisit.status",
        "TableVisit.serverPrincipalId",
        "TableVisit.subjectId",
        "TableVisit.orders",
        "TableVisit.mergedIntoVisitId",
        "TableVisit.mergedFromVisitIds",
        "TableVisit.runningTotal",
        "TableVisit.gratuity",
        "TableVisit.openedAt",
        "TableVisit.closedAt"
       ],
       "operation": "getTableVisit",
       "provenance": "contract fnb.yaml GET /table-visits/{visitId}"
      },
      {
       "kind": "searchField",
       "label": "Search live table",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Open table visit",
       "operation": "openTableVisit",
       "provenance": "contract fnb.yaml POST /table-visits"
      },
      {
       "kind": "secondaryButton",
       "label": "Save table visit",
       "operation": "updateTableVisit",
       "provenance": "contract fnb.yaml PATCH /table-visits/{visitId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Merge table visits",
       "operation": "mergeTableVisits",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/merge"
      },
      {
       "kind": "secondaryButton",
       "label": "Transfer table visit",
       "operation": "transferTableVisit",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/transfer"
      },
      {
       "kind": "secondaryButton",
       "label": "Seat table reservation",
       "operation": "seatTableReservation",
       "provenance": "contract fnb.yaml POST /table-reservations/{reservationId}/seat"
      },
      {
       "kind": "secondaryButton",
       "label": "Save service stage",
       "operation": "setServiceStage",
       "provenance": "contract fnb.yaml PUT /table-visits/{visitId}/stage"
      },
      {
       "kind": "secondaryButton",
       "label": "Move table visit",
       "operation": "moveTableVisit",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/move"
      },
      {
       "kind": "secondaryButton",
       "label": "Reassign server",
       "operation": "reassignServer",
       "provenance": "contract fnb.yaml PUT /table-visits/{visitId}/server"
      },
      {
       "kind": "secondaryButton",
       "label": "Notify server",
       "operation": "notifyServer",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/notify-server"
      },
      {
       "kind": "secondaryButton",
       "label": "Create F&B order",
       "operation": "createFnbOrder",
       "provenance": "contract fnb.yaml POST /fnb-orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Fire course",
       "operation": "fireCourse",
       "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/fire"
      },
      {
       "kind": "secondaryButton",
       "label": "Hold course",
       "operation": "holdCourse",
       "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/hold"
      },
      {
       "kind": "secondaryButton",
       "label": "Save table combinations",
       "operation": "setTableCombinations",
       "provenance": "contract fnb.yaml PUT /outlets/{outletId}/table-combinations"
      },
      {
       "kind": "secondaryButton",
       "label": "Quote wait time",
       "operation": "quoteWaitTime",
       "provenance": "contract fnb.yaml POST /waitlist/{entryId}/quote"
      },
      {
       "kind": "secondaryButton",
       "label": "Join restaurant waitlist",
       "operation": "joinRestaurantWaitlist",
       "provenance": "contract fnb.yaml POST /waitlist"
      },
      {
       "kind": "secondaryButton",
       "label": "Notify waitlist party",
       "operation": "notifyWaitlistParty",
       "provenance": "contract fnb.yaml POST /waitlist/{entryId}/notify"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmMergeTableVisits",
    "component": "confirmDialog",
    "trigger": "Merge table visits",
    "body": "**Names what `mergeTableVisits` changes and what it leaves alone**, in the consequence rather than the verb. A live table service this affects should be identified in the dialog, not just counted. **Collects what `mergeTableVisits` sends before it is called.** Required: `sourceVisitId`.",
    "provenance": "contract fnb.yaml POST /table-visits/{visitId}/merge"
   },
   {
    "id": "formUpdateTableVisit",
    "component": "modal",
    "trigger": "Save table visit",
    "body": "**Collects what `updateTableVisit` sends before it is called.** Required: `recordedAt`. Optional: `covers`, `tableId`, `serverPrincipalId`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save table visit",
     "operation": "updateTableVisit"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "covers",
      "tableId",
      "serverPrincipalId",
      "note"
     ]
    },
    "provenance": "contract fnb.yaml PATCH /table-visits/{visitId}"
   },
   {
    "id": "formTransferTableVisit",
    "component": "modal",
    "trigger": "Transfer table visit",
    "body": "**Collects what `transferTableVisit` sends before it is called.** Required: `toPrincipalId`, `reason`, `recordedAt`. **`note` is collected too, and required when the reason is Other** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transfer table visit",
     "operation": "transferTableVisit"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "toPrincipalId",
      "reason",
      "recordedAt",
      "note"
     ]
    },
    "provenance": "contract fnb.yaml POST /table-visits/{visitId}/transfer"
   },
   {
    "id": "formSeatTableReservation",
    "component": "modal",
    "trigger": "Seat table reservation",
    "body": "**Collects what `seatTableReservation` sends before it is called.** Required: `tableIds`, `recordedAt`. Optional: `actualPartySize`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Seat table reservation",
     "operation": "seatTableReservation"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "tableIds",
      "recordedAt",
      "actualPartySize"
     ]
    },
    "provenance": "contract fnb.yaml POST /table-reservations/{reservationId}/seat"
   },
   {
    "id": "formSetServiceStage",
    "component": "modal",
    "trigger": "Save service stage",
    "body": "**Collects what `setServiceStage` sends before it is called.** Required: `recordedAt`, `stage`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save service stage",
     "operation": "setServiceStage"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "stage"
     ]
    },
    "provenance": "contract fnb.yaml PUT /table-visits/{visitId}/stage"
   },
   {
    "id": "formMoveTableVisit",
    "component": "modal",
    "trigger": "Move table visit",
    "body": "**Collects what `moveTableVisit` sends before it is called.** Required: `toTableId`, `recordedAt`. Optional: `reason`. **`note` is collected too, and required when the reason is Other** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Move table visit",
     "operation": "moveTableVisit"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "toTableId",
      "recordedAt",
      "reason",
      "note"
     ]
    },
    "provenance": "contract fnb.yaml POST /table-visits/{visitId}/move"
   },
   {
    "id": "formReassignServer",
    "component": "modal",
    "trigger": "Reassign server",
    "body": "**Collects what `reassignServer` sends before it is called.** Required: `recordedAt`, `serverPrincipalId`. Optional: `splitGratuity`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reassign server",
     "operation": "reassignServer"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "serverPrincipalId",
      "splitGratuity"
     ]
    },
    "provenance": "contract fnb.yaml PUT /table-visits/{visitId}/server"
   },
   {
    "id": "formNotifyServer",
    "component": "modal",
    "trigger": "Notify server",
    "body": "**Collects what `notifyServer` sends before it is called.** Nothing in the body is required. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Notify server",
     "operation": "notifyServer"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract fnb.yaml POST /table-visits/{visitId}/notify-server"
   },
   {
    "id": "formCreateFnbOrder",
    "component": "modal",
    "trigger": "Create F&B order",
    "body": "**Collects what `createFnbOrder` sends before it is called.** Required: `id`, `outletId`, `serviceMode`, `lines`, `recordedAt`. Optional: `tableVisitId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateFnbOrderRequest",
    "confirm": {
     "label": "Create F&B order",
     "operation": "createFnbOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "outletId",
      "serviceMode",
      "lines",
      "recordedAt",
      "tableVisitId"
     ]
    },
    "provenance": "contract fnb.yaml POST /fnb-orders"
   },
   {
    "id": "formFireCourse",
    "component": "modal",
    "trigger": "Fire course",
    "body": "**Collects what `fireCourse` sends before it is called.** Required: `recordedAt`, `course`. Optional: `fireAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Fire course",
     "operation": "fireCourse"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "course",
      "fireAt"
     ]
    },
    "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/fire"
   },
   {
    "id": "formHoldCourse",
    "component": "modal",
    "trigger": "Hold course",
    "body": "**Collects what `holdCourse` sends before it is called.** Required: `recordedAt`, `course`. Optional: `reason`. **`note` is collected too, and required when the reason is Other** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Hold course",
     "operation": "holdCourse"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "course",
      "reason",
      "note"
     ]
    },
    "provenance": "contract fnb.yaml POST /kitchen-tickets/{ticketId}/hold"
   },
   {
    "id": "formSetTableCombinations",
    "component": "modal",
    "trigger": "Save table combinations",
    "body": "**Collects what `setTableCombinations` sends before it is called.** Required: `combinations`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save table combinations",
     "operation": "setTableCombinations"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "combinations"
     ]
    },
    "provenance": "contract fnb.yaml PUT /outlets/{outletId}/table-combinations"
   },
   {
    "id": "formJoinRestaurantWaitlist",
    "component": "modal",
    "trigger": "Join restaurant waitlist",
    "body": "**Collects what `joinRestaurantWaitlist` sends before it is called.** Required: `id`, `outletId`, `partySize`, `status`, `recordedAt`. Optional: `subjectId`, `quotedWaitMinutes`, `seatingPreference`, `notifiedAt`, `syncedAt`, `holdExpiresAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RestaurantWaitlist",
    "confirm": {
     "label": "Join restaurant waitlist",
     "operation": "joinRestaurantWaitlist"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "outletId",
      "partySize",
      "status",
      "recordedAt",
      "subjectId",
      "quotedWaitMinutes",
      "seatingPreference",
      "notifiedAt",
      "syncedAt",
      "holdExpiresAt"
     ]
    },
    "provenance": "contract fnb.yaml POST /waitlist"
   },
   {
    "id": "formNotifyWaitlistParty",
    "component": "modal",
    "trigger": "Notify waitlist party",
    "body": "**Collects what `notifyWaitlistParty` sends before it is called.** Nothing in the body is required. Optional: `channel`, `holdMinutes`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Notify waitlist party",
     "operation": "notifyWaitlistParty"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "channel",
      "holdMinutes"
     ]
    },
    "provenance": "contract fnb.yaml POST /waitlist/{entryId}/notify"
   }
  ],
  "states": {
   "loading": "The saved live table service.",
   "error": "Could not load. Names which read failed and leaves the live table service untouched.",
   "emptyFirstRun": "No live table service configured. The form opens empty and `openTableVisit` saves the first one; it says what the platform does in the meantime.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `getTableVisit` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "openTableVisit",
    "contract": "fnb",
    "purpose": "Seat a party and open a visit",
    "trigger": "onAction"
   },
   {
    "operationId": "updateTableVisit",
    "contract": "fnb",
    "purpose": "Amend covers, move table, or reassign server",
    "trigger": "onAction"
   },
   {
    "operationId": "mergeTableVisits",
    "contract": "fnb",
    "purpose": "Merge another visit into this one",
    "trigger": "onAction"
   },
   {
    "operationId": "transferTableVisit",
    "contract": "fnb",
    "purpose": "Move a check to another server",
    "trigger": "onAction"
   },
   {
    "operationId": "seatTableReservation",
    "contract": "fnb",
    "purpose": "The party arrived and has been sat down",
    "trigger": "onAction"
   },
   {
    "operationId": "setServiceStage",
    "contract": "fnb",
    "purpose": "Where this table is in its meal",
    "trigger": "onAction"
   },
   {
    "operationId": "moveTableVisit",
    "contract": "fnb",
    "purpose": "Move a party to a different table, mid-service",
    "trigger": "onAction"
   },
   {
    "operationId": "reassignServer",
    "contract": "fnb",
    "purpose": "Hand a table to another server",
    "trigger": "onAction"
   },
   {
    "operationId": "notifyServer",
    "contract": "fnb",
    "purpose": "The kitchen calls the server to the pass",
    "trigger": "onAction"
   },
   {
    "operationId": "createFnbOrder",
    "contract": "fnb",
    "purpose": "Place an F&B order",
    "trigger": "onAction"
   },
   {
    "operationId": "fireCourse",
    "contract": "fnb",
    "purpose": "Send a held course to the pass",
    "trigger": "onAction"
   },
   {
    "operationId": "holdCourse",
    "contract": "fnb",
    "purpose": "Stop a course going out",
    "trigger": "onAction"
   },
   {
    "operationId": "setTableCombinations",
    "contract": "fnb",
    "purpose": "Which tables can be pushed together, and to what capacity",
    "trigger": "onAction"
   },
   {
    "operationId": "quoteWaitTime",
    "contract": "fnb",
    "purpose": "Tell a party how long, and mean it",
    "trigger": "onAction"
   },
   {
    "operationId": "joinRestaurantWaitlist",
    "contract": "fnb",
    "purpose": "Add a party to an outlet's waitlist",
    "trigger": "onAction"
   },
   {
    "operationId": "notifyWaitlistParty",
    "contract": "fnb",
    "purpose": "Their table is ready",
    "trigger": "onAction"
   },
   {
    "operationId": "getTableVisit",
    "contract": "fnb",
    "purpose": "Read a visit with all its orders",
    "trigger": "onAction",
    "provenance": "wiring gap, 19 September 2026 — the screen showed the noun and could not act on it"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "visitId",
     "from": "EMP-003"
    },
    {
     "name": "reservationId",
     "from": "deepLink"
    },
    {
     "name": "entryId",
     "from": "deepLink",
     "optional": true
    },
    {
     "name": "outletId",
     "from": "session",
     "optional": true
    },
    {
     "name": "ticketId",
     "from": "deepLink",
     "optional": true
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to. A booking opened from the timeline. **The host taps a reservation to seat it** — that is the only way in. A waitlist party tapped on the list. Resolves from the shift assignment. A ticket tapped on the rail."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-058",
   "derivedFrom": "wireframes/reference/FnB Board 4.dc.html",
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 16 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-059",
  "name": "Table Order, Bill & Payment Management",
  "module": "Floor Service",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/table-order-bill-payment-management",
   "component": "apps/venue-staff-app/src/routes/operations/TableOrderBillPaymentManagementDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003"
   ],
   "exitTo": [
    "EMP-058"
   ],
   "transitions": [
    {
     "to": "EMP-058",
     "trigger": "Live Table & Service Management",
     "provenance": "flow F80 step 1→2",
     "operation": "transferOrderItems",
     "carries": [
      "visitId"
     ]
    },
    {
     "to": "KIT-002",
     "trigger": "The kitchen makes the starters and bumps them",
     "provenance": "flow F29 step 3→4",
     "operation": "createFnbOrder",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "visitId"
     ]
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.** **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens.",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4j"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getBill` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Table Order, Bill & Payment Management — from the client design board, 20 August.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The bill",
       "bindsTo": "Bill",
       "columns": [
        "Bill.visitId",
        "Bill.covers",
        "Bill.lines",
        "Bill.subtotal",
        "Bill.serviceCharge",
        "Bill.taxAmount",
        "Bill.discountAmount",
        "Bill.total"
       ],
       "operation": "getBill",
       "provenance": "contract fnb.yaml GET /table-visits/{visitId}/bill"
      },
      {
       "kind": "searchField",
       "label": "Search table order, bill",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "destructiveButton",
       "label": "Close table visit",
       "operation": "closeTableVisit",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Create payment",
       "operation": "createPayment",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "secondaryButton",
       "label": "Create F&B order",
       "operation": "createFnbOrder",
       "provenance": "contract fnb.yaml POST /fnb-orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Split bill",
       "operation": "splitBill",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/bill/split"
      },
      {
       "kind": "secondaryButton",
       "label": "Comp item",
       "operation": "compItem",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/comp"
      },
      {
       "kind": "secondaryButton",
       "label": "Transfer order items",
       "operation": "transferOrderItems",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/transfer-items"
      },
      {
       "kind": "primaryButton",
       "label": "Request bill",
       "operation": "requestBill",
       "provenance": "contract fnb.yaml POST /table-visits/{visitId}/request-bill"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCloseTableVisit",
    "component": "confirmDialog",
    "trigger": "Close table visit",
    "body": "**Names what `closeTableVisit` changes and what it leaves alone**, in the consequence rather than the verb. A table order bill this affects should be identified in the dialog, not just counted. **Collects what `closeTableVisit` sends before it is called.** Required: `payments`. Optional: `gratuity`.",
    "provenance": "contract fnb.yaml POST /table-visits/{visitId}/close"
   },
   {
    "id": "formRequestBill",
    "component": "modal",
    "trigger": "Request bill",
    "body": "**Collects what `requestBill` sends before it is called.** Required: `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Request bill",
     "operation": "requestBill"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt"
     ]
    },
    "provenance": "contract fnb.yaml POST /table-visits/{visitId}/request-bill"
   },
   {
    "id": "formCreatePayment",
    "component": "modal",
    "trigger": "Create payment",
    "body": "**Collects what `createPayment` sends before it is called.** Required: `id`, `orderId`, `tender`, `amount`, `recordedAt`. Optional: `tenderCurrency`, `tenderAmount`, `walletAuthorisationId`, `deviceId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreatePaymentRequest",
    "confirm": {
     "label": "Create payment",
     "operation": "createPayment"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "orderId",
      "tender",
      "amount",
      "recordedAt",
      "tenderCurrency",
      "tenderAmount",
      "walletAuthorisationId",
      "deviceId"
     ]
    },
    "provenance": "contract orders.yaml POST /payments"
   },
   {
    "id": "formCreateFnbOrder",
    "component": "modal",
    "trigger": "Create F&B order",
    "body": "**Collects what `createFnbOrder` sends before it is called.** Required: `id`, `outletId`, `serviceMode`, `lines`, `recordedAt`. Optional: `tableVisitId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateFnbOrderRequest",
    "confirm": {
     "label": "Create F&B order",
     "operation": "createFnbOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "outletId",
      "serviceMode",
      "lines",
      "recordedAt",
      "tableVisitId"
     ]
    },
    "provenance": "contract fnb.yaml POST /fnb-orders"
   },
   {
    "id": "formSplitBill",
    "component": "modal",
    "trigger": "Split bill",
    "body": "**Collects what `splitBill` sends before it is called.** Required: `recordedAt`, `method`. Optional: `parts`, `amounts`, `lineAssignments`, `categoryAssignments`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SplitBillRequest",
    "confirm": {
     "label": "Split bill",
     "operation": "splitBill"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "method",
      "parts",
      "amounts",
      "lineAssignments",
      "categoryAssignments"
     ]
    },
    "provenance": "contract fnb.yaml POST /table-visits/{visitId}/bill/split"
   },
   {
    "id": "formCompItem",
    "component": "modal",
    "trigger": "Comp item",
    "body": "**Collects what `compItem` sends before it is called.** Required: `orderLineId`, `recordedAt`, `reason`. Optional: `note`. **When the reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Comp item",
     "operation": "compItem"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "orderLineId",
      "recordedAt",
      "reason",
      "note"
     ]
    },
    "provenance": "contract fnb.yaml POST /table-visits/{visitId}/comp"
   },
   {
    "id": "formTransferOrderItems",
    "component": "modal",
    "trigger": "Transfer order items",
    "body": "**Collects what `transferOrderItems` sends before it is called.** Required: `toVisitId`, `lineIds`, `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transfer order items",
     "operation": "transferOrderItems"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "toVisitId",
      "lineIds",
      "recordedAt"
     ]
    },
    "provenance": "contract fnb.yaml POST /table-visits/{visitId}/transfer-items"
   }
  ],
  "states": {
   "loading": "The table order bill, read by `getBill`.",
   "error": "Could not load. Names which read failed and leaves the table order bill untouched.",
   "emptyFirstRun": "No table order bill yet. Offers Create payment (`createPayment`).",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `getBill` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "closeTableVisit",
    "contract": "fnb",
    "purpose": "Settle and close a visit",
    "trigger": "onAction"
   },
   {
    "operationId": "createPayment",
    "contract": "orders",
    "purpose": "Take a payment against an order",
    "trigger": "onAction"
   },
   {
    "operationId": "createFnbOrder",
    "contract": "fnb",
    "purpose": "Place an F&B order",
    "trigger": "onAction"
   },
   {
    "operationId": "splitBill",
    "contract": "fnb",
    "purpose": "Split a bill",
    "trigger": "onAction"
   },
   {
    "operationId": "getBill",
    "contract": "fnb",
    "purpose": "Bill for a visit",
    "trigger": "onLoad"
   },
   {
    "operationId": "compItem",
    "contract": "fnb",
    "purpose": "Take a line off the bill, with a reason and a name",
    "trigger": "onAction"
   },
   {
    "operationId": "transferOrderItems",
    "contract": "fnb",
    "purpose": "Move items to another table's bill",
    "trigger": "onAction"
   },
   {
    "operationId": "requestBill",
    "contract": "fnb",
    "purpose": "The party asked to pay",
    "trigger": "onAction",
    "provenance": "wiring gap, 19 September 2026 — the screen showed the noun and could not act on it",
    "invalidates": [
     "getTableVisit"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "visitId",
     "from": "EMP-003"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-059",
   "derivedFrom": "wireframes/reference/FnB Board 4.dc.html",
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-060",
  "name": "Reservation & Table Performance",
  "module": "Floor Service",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/reservation-table-performance",
   "component": "apps/venue-staff-app/src/routes/operations/ReservationTablePerformanceDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "EMP-003",
    "EMP-058"
   ],
   "exitTo": [
    "EMP-061"
   ],
   "inferred": false,
   "notes": "**Returns to EMP-003.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "EMP-061",
     "trigger": "Retail Inventory Command Center",
     "provenance": "flow F80 step 3→4, F94 step 2→3"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** P06 had no table or stock operations at all — **twenty screens of floor work with nothing behind them** — and every operation these need already existed. **Named in the board contents and not written up in it.**",
  "density": "comfortable",
  "boardFrames": [
   "FnB Board 4.dc.html#fnb-4c"
  ],
  "pattern": "listDetail",
  "patternReason": "`listTableReservations` reads the population and `getTableMap` reads one of them — list, select, act",
  "purpose": "Reservation & Table Performance — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Outlet id",
       "operation": "listTableReservations",
       "notes": "Sends `?outletId=` to `listTableReservations`.",
       "provenance": "contract fnb.yaml GET /table-reservations"
      },
      {
       "kind": "datePicker",
       "label": "Date",
       "operation": "listTableReservations",
       "notes": "Sends `?date=` to `listTableReservations`.",
       "provenance": "contract fnb.yaml GET /table-reservations"
      },
      {
       "kind": "dataTable",
       "label": "Every table reservation",
       "bindsTo": "TableReservation",
       "columns": [
        "TableReservation.id",
        "TableReservation.outletId",
        "TableReservation.subjectId",
        "TableReservation.guestName",
        "TableReservation.contactPoint",
        "TableReservation.partySize",
        "TableReservation.startsAt",
        "TableReservation.durationMinutes",
        "TableReservation.tables[].tableId",
        "TableReservation.status",
        "TableReservation.groupId",
        "TableReservation.notes"
       ],
       "operation": "listTableReservations",
       "provenance": "contract fnb.yaml GET /table-reservations"
      },
      {
       "kind": "searchField",
       "label": "Search reservation",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "cardList",
       "notes": "**Cards rather than a table.** One thumb, arm’s length, and a person who is walking.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Confirm",
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
       "label": "The selected table reservation",
       "bindsTo": "TableReservation",
       "columns": [
        "TableReservation.id",
        "TableReservation.outletId",
        "TableReservation.subjectId",
        "TableReservation.guestName",
        "TableReservation.contactPoint",
        "TableReservation.partySize",
        "TableReservation.startsAt",
        "TableReservation.durationMinutes",
        "TableReservation.tables",
        "TableReservation.status",
        "TableReservation.groupId",
        "TableReservation.notes",
        "TableReservation.actualPartySize",
        "TableReservation.tableVisitId"
       ],
       "operation": "listTableReservations",
       "provenance": "contract fnb.yaml GET /table-reservations"
      },
      {
       "kind": "detailPanel",
       "label": "The table map",
       "bindsTo": "TableMap",
       "columns": [
        "TableMap.outletId",
        "TableMap.zones",
        "TableMap.tables"
       ],
       "operation": "getTableMap",
       "provenance": "contract fnb.yaml GET /outlets/{outletId}/tables"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reservation table performance list.",
   "error": "Could not load. Names which read failed and leaves the reservation table performance untouched.",
   "emptyFirstRun": "No reservation table performance yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on outletId, date and the reservation table performance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_MODIFY`, which `listTableReservations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Works from cache and queues what it records.** Staff walk out of coverage constantly — a stock count in a warehouse corner and a table order on a terrace both happen where the signal does not reach, and a screen that blanks there is a screen nobody uses twice."
  },
  "apis": [
   {
    "operationId": "listTableReservations",
    "contract": "fnb",
    "purpose": "Bookings for a service period",
    "trigger": "onLoad"
   },
   {
    "operationId": "getTableMap",
    "contract": "fnb",
    "purpose": "Table map with live state",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "outletId",
     "from": "EMP-003"
    }
   ],
   "coldEntry": "**Resolves from the session and the shift.** A handheld is signed into at the start of a shift, not navigated to.",
   "preloaded": [
    "TableReservation.id",
    "TableReservation.outletId",
    "TableReservation.subjectId",
    "TableReservation.guestName",
    "TableReservation.contactPoint"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-060",
   "derivedFrom": "wireframes/reference/FnB Board 4.dc.html",
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
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
 "addGuestNote": {
  "method": "POST",
  "path": "/guests/{subjectId}/notes",
  "contract": "marketing-crm",
  "summary": "What the floor needs to know about this table",
  "permission": "GUEST_MANAGE",
  "offlineCapable": true,
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
  "responds": "GuestNote"
 },
 "closeTableVisit": {
  "method": "POST",
  "path": "/table-visits/{visitId}/close",
  "contract": "fnb",
  "summary": "Settle and close a visit",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
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
 "compItem": {
  "method": "POST",
  "path": "/table-visits/{visitId}/comp",
  "contract": "fnb",
  "summary": "Take a line off the bill, with a reason and a name",
  "permission": "ORDER_MODIFY",
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
  "responds": "TableVisit"
 },
 "createFnbOrder": {
  "method": "POST",
  "path": "/fnb-orders",
  "contract": "fnb",
  "summary": "Place an F&B order",
  "permission": "ORDER_CREATE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreateFnbOrderRequest",
  "responds": "FnbOrder"
 },
 "createPayment": {
  "method": "POST",
  "path": "/payments",
  "contract": "orders",
  "summary": "Take a payment against an order",
  "permission": "ORDER_CREATE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreatePaymentRequest",
  "responds": "Payment"
 },
 "createTable": {
  "method": "POST",
  "path": "/tables",
  "contract": "fnb",
  "summary": "A table as a thing, not an inference",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "TableDefinition",
  "responds": "TableDefinition"
 },
 "createTableReservation": {
  "method": "POST",
  "path": "/table-reservations",
  "contract": "fnb",
  "summary": "Book a table in advance",
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
  "requestBody": "TableReservation",
  "responds": "TableReservation"
 },
 "fireCourse": {
  "method": "POST",
  "path": "/kitchen-tickets/{ticketId}/fire",
  "contract": "fnb",
  "summary": "Send a held course to the pass",
  "permission": "ORDER_MODIFY",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "KitchenTicket"
 },
 "getBill": {
  "method": "GET",
  "path": "/table-visits/{visitId}/bill",
  "contract": "fnb",
  "summary": "Bill for a visit",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Bill"
 },
 "getGuestProfile": {
  "method": "GET",
  "path": "/guests/{subjectId}",
  "contract": "marketing-crm",
  "summary": "Read a guest profile",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestProfileDetail"
 },
 "getTableMap": {
  "method": "GET",
  "path": "/outlets/{outletId}/tables",
  "contract": "fnb",
  "summary": "Table map with live state",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "TableMap"
 },
 "getTableVisit": {
  "method": "GET",
  "path": "/table-visits/{visitId}",
  "contract": "fnb",
  "summary": "Read a visit with all its orders",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "TableVisit"
 },
 "holdCourse": {
  "method": "POST",
  "path": "/kitchen-tickets/{ticketId}/hold",
  "contract": "fnb",
  "summary": "Stop a course going out",
  "permission": "ORDER_MODIFY",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "KitchenTicket"
 },
 "joinRestaurantWaitlist": {
  "method": "POST",
  "path": "/waitlist",
  "contract": "fnb",
  "summary": "Add a party to an outlet's waitlist",
  "permission": "ORDER_MODIFY",
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
  "requestBody": "RestaurantWaitlist",
  "responds": "RestaurantWaitlist"
 },
 "leaveRestaurantWaitlist": {
  "method": "POST",
  "path": "/waitlist/{entryId}/leave",
  "contract": "fnb",
  "summary": "Take a party off an outlet's waitlist",
  "permission": "ORDER_MODIFY",
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
  "responds": "RestaurantWaitlist"
 },
 "listFnbOrders": {
  "method": "GET",
  "path": "/fnb-orders",
  "contract": "fnb",
  "summary": "List F&B orders",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "outletId",
    "in": "query",
    "required": null
   },
   {
    "name": "tableVisitId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
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
 "listTableReservations": {
  "method": "GET",
  "path": "/table-reservations",
  "contract": "fnb",
  "summary": "Bookings for a service period",
  "permission": "ORDER_MODIFY",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "outletId",
    "in": "query",
    "required": null
   },
   {
    "name": "date",
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
 "matchGuest": {
  "method": "POST",
  "path": "/guests/match",
  "contract": "marketing-crm",
  "summary": "Is this the same person we already have?",
  "permission": "GUEST_VIEW",
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
 "mergeGuests": {
  "method": "POST",
  "path": "/guests/merge",
  "contract": "marketing-crm",
  "summary": "Two records, one person",
  "permission": "GUEST_MANAGE",
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
  "responds": "MergeResult"
 },
 "mergeTableVisits": {
  "method": "POST",
  "path": "/table-visits/{visitId}/merge",
  "contract": "fnb",
  "summary": "Merge another visit into this one",
  "permission": "ORDER_MODIFY",
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
  "responds": "TableVisit"
 },
 "moveTableVisit": {
  "method": "POST",
  "path": "/table-visits/{visitId}/move",
  "contract": "fnb",
  "summary": "Move a party to a different table, mid-service",
  "permission": "ORDER_MODIFY",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "TableVisit"
 },
 "notifyServer": {
  "method": "POST",
  "path": "/table-visits/{visitId}/notify-server",
  "contract": "fnb",
  "summary": "The kitchen calls the server to the pass",
  "permission": "ORDER_MODIFY",
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
 "notifyWaitlistParty": {
  "method": "POST",
  "path": "/waitlist/{entryId}/notify",
  "contract": "fnb",
  "summary": "Their table is ready",
  "permission": "ORDER_MODIFY",
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
  "responds": "RestaurantWaitlist"
 },
 "openTableVisit": {
  "method": "POST",
  "path": "/table-visits",
  "contract": "fnb",
  "summary": "Seat a party and open a visit",
  "permission": "ORDER_CREATE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "OpenTableVisitRequest",
  "responds": "TableVisit"
 },
 "quoteWaitTime": {
  "method": "POST",
  "path": "/waitlist/{entryId}/quote",
  "contract": "fnb",
  "summary": "Tell a party how long, and mean it",
  "permission": "ORDER_MODIFY",
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
 "reassignServer": {
  "method": "PUT",
  "path": "/table-visits/{visitId}/server",
  "contract": "fnb",
  "summary": "Hand a table to another server",
  "permission": "ORDER_MODIFY",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "TableVisit"
 },
 "requestBill": {
  "method": "POST",
  "path": "/table-visits/{visitId}/request-bill",
  "contract": "fnb",
  "summary": "The party asked to pay",
  "permission": "ORDER_MODIFY",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "TableVisit"
 },
 "seatTableReservation": {
  "method": "POST",
  "path": "/table-reservations/{reservationId}/seat",
  "contract": "fnb",
  "summary": "The party arrived and has been sat down",
  "permission": "ORDER_MODIFY",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "TableReservation"
 },
 "setSectionLayout": {
  "method": "PUT",
  "path": "/outlets/{outletId}/sections",
  "contract": "fnb",
  "summary": "Divide the floor into sections and give each a server",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "SectionLayout",
  "responds": "SectionLayout"
 },
 "setServiceStage": {
  "method": "PUT",
  "path": "/table-visits/{visitId}/stage",
  "contract": "fnb",
  "summary": "Where this table is in its meal",
  "permission": "ORDER_MODIFY",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "TableVisit"
 },
 "setTableCombinations": {
  "method": "PUT",
  "path": "/outlets/{outletId}/table-combinations",
  "contract": "fnb",
  "summary": "Which tables can be pushed together, and to what capacity",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": null,
  "responds": null
 },
 "setTableLayout": {
  "method": "PUT",
  "path": "/outlets/{outletId}/tables",
  "contract": "fnb",
  "summary": "Configure the table layout",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": null,
  "responds": "TableMap"
 },
 "splitBill": {
  "method": "POST",
  "path": "/table-visits/{visitId}/bill/split",
  "contract": "fnb",
  "summary": "Split a bill",
  "permission": "ORDER_MODIFY",
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
  "requestBody": "SplitBillRequest",
  "responds": "BillSplit"
 },
 "transferOrderItems": {
  "method": "POST",
  "path": "/table-visits/{visitId}/transfer-items",
  "contract": "fnb",
  "summary": "Move items to another table's bill",
  "permission": "ORDER_MODIFY",
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
  "responds": "TableVisit"
 },
 "transferTableVisit": {
  "method": "POST",
  "path": "/table-visits/{visitId}/transfer",
  "contract": "fnb",
  "summary": "Move a check to another server",
  "permission": "ORDER_MODIFY",
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
  "responds": "TableVisit"
 },
 "updateTable": {
  "method": "PUT",
  "path": "/tables/{tableId}",
  "contract": "fnb",
  "summary": "Change what a table is",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "TableDefinition",
  "responds": "TableDefinition"
 },
 "updateTableVisit": {
  "method": "PATCH",
  "path": "/table-visits/{visitId}",
  "contract": "fnb",
  "summary": "Amend covers, move table, or reassign server",
  "permission": "ORDER_MODIFY",
  "offlineCapable": true,
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
  "responds": "TableVisit"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AllergenCode": {
  "type": "string",
  "description": "**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n",
  "enum": [
   "gluten",
   "crustaceans",
   "eggs",
   "fish",
   "peanuts",
   "soybeans",
   "milk",
   "nuts",
   "celery",
   "mustard",
   "sesame",
   "sulphites",
   "lupin",
   "molluscs"
  ]
 },
 "Bill": {
  "x-ticvai-persistence": "none — computed from visit orders",
  "type": "object",
  "required": [
   "visitId",
   "lines",
   "subtotal",
   "taxAmount",
   "total"
  ],
  "properties": {
   "visitId": {
    "type": "string"
   },
   "covers": {
    "type": "integer"
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "lineId",
      "name",
      "quantity",
      "lineTotal"
     ],
     "properties": {
      "lineId": {
       "type": "string"
      },
      "orderId": {
       "type": "string"
      },
      "name": {
       "type": "string"
      },
      "quantity": {
       "type": "integer"
      },
      "unitPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "lineTotal": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "categoryCode": {
       "type": "string",
       "nullable": true
      },
      "seatNumber": {
       "type": "integer",
       "nullable": true
      }
     }
    }
   },
   "subtotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "serviceCharge": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "total": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "BillSplit": {
  "x-ticvai-persistence": "fnb.bill_split + fnb.sub_bill",
  "type": "object",
  "required": [
   "visitId",
   "method",
   "subBills"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "visitId": {
    "type": "string"
   },
   "method": {
    "$ref": "#/components/schemas/SplitMethod"
   },
   "subBills": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "subBillId",
      "total",
      "status"
     ],
     "properties": {
      "subBillId": {
       "type": "string"
      },
      "lineIds": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "subtotal": {
       "x-ticvai-column": "net_amount",
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "taxAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "total": {
       "x-ticvai-column": "gross_amount",
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "status": {
       "type": "string",
       "enum": [
        "unpaid",
        "paid"
       ]
      }
     }
    }
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
 "CoursingPolicy": {
  "type": "string",
  "description": "How a ticket's courses are fired. `fireAndForget` sends every course at once, which is no coursing; `holdAndFire` waits for a server to call each course; `timed` fires on a clock; `phased` staggers by course. **One vocabulary for the ticket (`KitchenTicket.coursing`) and the outlet default (`CourseRules.defaultCoursing`)** — the default said `none` for `fireAndForget` and had no `delayed` until 26 September, so a default could not be copied onto the field it defaults.\n",
  "enum": [
   "fireAndForget",
   "holdAndFire",
   "phased",
   "timed",
   "delayed"
  ]
 },
 "CreateFnbOrderLine": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "menuItemId",
   "quantity"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "menuItemId": {
    "type": "string",
    "format": "uuid"
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "modifierOptionIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "note": {
    "type": "string",
    "maxLength": 200,
    "description": "Free text to the kitchen. Allergy notes belong here and are surfaced prominently."
   },
   "seatNumber": {
    "type": "integer",
    "nullable": true,
    "description": "Which cover ordered it. Drives split-by-covers accurately."
   },
   "course": {
    "type": "integer",
    "nullable": true,
    "description": "Course grouping, so the kitchen fires in sequence."
   },
   "redeemEntitlementId": {
    "type": "string",
    "nullable": true,
    "x-ticvai-references": "access.entitlement",
    "description": "**A meal combo redeemed at the till or by a scan** (29 September, MOB-4; applied 30 September). The entitlement a bundle's `fnbMenuItem` component issued (promotions `BundleComponent.componentKind: fnbMenuItem`, `menuItemId`, `redeemAtOutletIds`). The line is priced at zero against it, `menuItemId` must be the component's menu item and the outlet one of `redeemAtOutletIds` (or any outlet with the item on a live menu when that list is empty), and the entitlement is marked used in the same step through access `validateAccess` at the outlet. An entitlement already used, for another item or outlet, or not yet valid is refused 409 `entitlementNotRedeemable`; a till that is offline queues the redemption like any sale and the replay is refused the same way if it was used meanwhile."
   }
  }
 },
 "CreateFnbOrderRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "outletId",
   "serviceMode",
   "lines",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "serviceMode": {
    "$ref": "#/components/schemas/ServiceMode"
   },
   "tableVisitId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required for table service. Absent for quick service."
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/CreateFnbOrderLine"
    }
   },
   "salesOrderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `orders.sales_order` this F&B order fulfils (SD-046, 29 September). A POS sale sends the order it took payment on; the commercial order is the sales order and this is its fulfilment."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CreatePaymentRequest": {
  "type": "object",
  "required": [
   "id",
   "orderId",
   "tender",
   "amount",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "tender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "tenderCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "description": "The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. Omit for a payment in the venue's own currency."
   },
   "tenderAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "**What the guest handed over**, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). For cash, change is the difference.\n"
   },
   "walletAuthorisationId": {
    "type": "string",
    "nullable": true,
    "description": "Cross-cell wallet hold, where the guest's home cell is elsewhere."
   },
   "walletHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table."
   },
   "returnUrl": {
    "type": "string",
    "format": "uri",
    "nullable": true,
    "description": "Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). Required for a card payment from the guest web or app."
   },
   "terminalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The card terminal to instruct, for a card payment at a till (ECR flow, SD-034)."
   },
   "deviceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ExchangeRateDecimal": {
  "type": "string",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,6)",
  "description": "**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n",
  "pattern": "^\\d+(\\.\\d{1,6})?$"
 },
 "FnbOrder": {
  "x-ticvai-persistence": "fnb.service_order + fnb.service_order_line",
  "type": "object",
  "required": [
   "id",
   "orderNumber",
   "outletId",
   "serviceMode",
   "status",
   "lines",
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
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "serviceMode": {
    "$ref": "#/components/schemas/ServiceMode"
   },
   "tableVisitId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "status": {
    "$ref": "#/components/schemas/FnbOrderStatus"
   },
   "lines": {
    "type": "array",
    "items": {
     "allOf": [
      {
       "$ref": "#/components/schemas/CreateFnbOrderLine"
      },
      {
       "type": "object",
       "properties": {
        "status": {
         "$ref": "#/components/schemas/FnbOrderStatus"
        },
        "unitPrice": {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        },
        "lineTotal": {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       }
      }
     ]
    }
   },
   "salesOrderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "orders.sales_order",
    "description": "**Retyped 29 September (SD-046)**, and `format: uuid` since ADR-0056 (30 September): every id is a uuid, so this joins `orders.sales_order.id`. **Taken from their `fnb.order`, 20 September.** We carried outlet, table visit and kitchen ticket on an F&B order and nothing joining it to what was actually sold, so an F&B line could not be reconciled to the order that paid for it.\n"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Taken from their `fnb.order`. Ours had `recordedAt` and `syncedAt`, which are both offline-sync fields, and no plain updated timestamp.\n"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "kitchenTicketId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "kitchenTickets": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "The kitchen tickets this order created, one per station (SD-046). Returned, not stored here; they are `fnb.kitchen_ticket` rows.",
    "items": {
     "$ref": "#/components/schemas/KitchenTicket"
    }
   },
   "estimatedReadyAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "FnbOrderStatus": {
  "type": "string",
  "description": "The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or `delivered` at all, which made collection and delivery indistinguishable from a server putting a plate down.\n`accepted` matters because an outlet may refuse: past last orders, out of a key ingredient, or simply too far behind. A guest whose order sat in `placed` for ten minutes and was then rejected has a worse experience than one refused immediately.\n",
  "enum": [
   "ordered",
   "accepted",
   "inPreparation",
   "ready",
   "served",
   "collected",
   "delivered",
   "cancelled",
   "refunded"
  ]
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
 "GuestNote": {
  "type": "object",
  "x-ticvai-persistence": "marketing.guest_note",
  "description": "A note on a guest, written by staff (`addGuestNote`). **Attributed and personal data**, and `isAllergy` keeps an allergy apart from every other kind so it surfaces on the order screen.\n",
  "required": [
   "id",
   "subjectId",
   "kind",
   "text",
   "recordedAt"
  ],
  "properties": {
   "id": {
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
     "allergy",
     "dietary",
     "seatingPreference",
     "occasion",
     "serviceRecovery",
     "vip",
     "general"
    ]
   },
   "text": {
    "type": "string"
   },
   "isAllergy": {
    "type": "boolean",
    "default": false
   },
   "visibleToServer": {
    "type": "boolean",
    "default": true
   },
   "authorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
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
 "GuestProfileDetail": {
  "x-ticvai-persistence": "marketing.guest_profile",
  "allOf": [
   {
    "$ref": "#/components/schemas/GuestProfile"
   },
   {
    "type": "object",
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid",
      "readOnly": true,
      "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
     },
     "consents": {
      "$ref": "#/components/schemas/ConsentState"
     },
     "loyalty": {
      "$ref": "#/components/schemas/LoyaltyPosition"
     },
     "openCaseCount": {
      "type": "integer"
     },
     "recentOrderIds": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "membershipIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "notes": {
      "type": "string",
      "nullable": true
     }
    }
   }
  ]
 },
 "KitchenTicket": {
  "x-ticvai-persistence": "fnb.kitchen_ticket + fnb.kitchen_ticket_line",
  "type": "object",
  "required": [
   "id",
   "orderId",
   "outletId",
   "status",
   "lines",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "description": "The F&B order the ticket was created from on acceptance (`FnbOrder.id`)."
   },
   "orderNumber": {
    "type": "string"
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "tableLabel": {
    "type": "string",
    "nullable": true
   },
   "serviceMode": {
    "$ref": "#/components/schemas/ServiceMode"
   },
   "coursing": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CoursingPolicy"
     }
    ],
    "nullable": true,
    "description": "BL-131. **Starters before mains is the entire job of a kitchen pass**, and the model fired everything at once.\n`holdAndFire` waits for a server to call it; `timed` fires on a clock; `phased` staggers by course. **Without this a table gets its dessert while eating its starter.**\n"
   },
   "buzzerCode": {
    "type": "string",
    "nullable": true,
    "description": "BL-128. **The pager number handed to a guest at a counter.** Recorded against the order so a lost buzzer is a lookup rather than an argument.\n"
   },
   "status": {
    "$ref": "#/components/schemas/KitchenTicketStatus"
   },
   "priority": {
    "type": "integer",
    "description": "Higher fires sooner. Raised by Fast Pass or supervisor override."
   },
   "prioritisedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "prioritiseReason": {
    "type": "string",
    "nullable": true
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "lineId",
      "name",
      "quantity",
      "status"
     ],
     "properties": {
      "lineId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "quantity": {
       "type": "integer"
      },
      "modifiers": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "note": {
       "type": "string",
       "nullable": true
      },
      "allergens": {
       "type": "array",
       "items": {
        "$ref": "#/components/schemas/AllergenCode"
       }
      },
      "refireOfLineId": {
       "type": "string",
       "format": "uuid",
       "nullable": true,
       "readOnly": true,
       "description": "**Set on a refire.** The line it remakes, which stays — food cost counts both, the bill counts one (`refireItem`)."
      },
      "refireReason": {
       "allOf": [
        {
         "$ref": "#/components/schemas/RefireReason"
        }
       ],
       "nullable": true,
       "readOnly": true
      },
      "isChargeable": {
       "type": "boolean",
       "nullable": true,
       "readOnly": true,
       "description": "A refire's `chargeable` flag. Null on a line that is not a refire."
      },
      "course": {
       "type": "integer",
       "nullable": true
      },
      "stationId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "status": {
       "$ref": "#/components/schemas/KitchenTicketStatus"
      }
     }
    }
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "targetReadyAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "elapsedSeconds": {
    "type": "integer"
   }
  }
 },
 "KitchenTicketStatus": {
  "type": "string",
  "enum": [
   "received",
   "preparing",
   "ready",
   "served",
   "recalled",
   "cancelled"
  ]
 },
 "LoyaltyPosition": {
  "x-ticvai-persistence": "marketing.loyalty_position",
  "type": "object",
  "required": [
   "subjectId",
   "programmeId",
   "pointsBalance",
   "tierCode"
  ],
  "properties": {
   "leaderboardNickname": {
    "type": "string",
    "nullable": true,
    "maxLength": 24,
    "description": "BL-173. **The name shown on a leaderboard, chosen by the guest.** Offered whenever they reach the board and changeable afterwards; `setLeaderboardNickname` is the only thing that writes it.\n**Null means the guest has not chosen one yet, and the board shows a generated `Player-4821` in its place** — never `pii.subject.display_name`, which would disclose silently on the day a guest first placed and is the case this field exists to prevent.\n**The generated name is computed at read time and not stored here.** Writing it would make *\"has this guest chosen a name\"* unanswerable, and that flag is what the prompt-on-reaching-the-board depends on.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "pointsBalance": {
    "type": "integer"
   },
   "lifetimePoints": {
    "type": "integer"
   },
   "tierId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The tier this row's `tierCode` and `tierName` are a copy of.** Added 20 September with `marketing.programme_tier`: the two strings were a cache of something that did not exist, and a cache with no source cannot be rebuilt or audited.\n"
   },
   "tierCode": {
    "type": "string"
   },
   "tierName": {
    "type": "string"
   },
   "pointsToNextTier": {
    "type": "integer",
    "nullable": true
   },
   "nextExpiryPoints": {
    "type": "integer",
    "nullable": true
   },
   "nextExpiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "MergeResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "survivingSubjectId",
   "absorbedSubjectId",
   "transferred"
  ],
  "properties": {
   "survivingSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "absorbedSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "transferred": {
    "type": "object",
    "properties": {
     "orders": {
      "type": "integer"
     },
     "cases": {
      "type": "integer"
     },
     "loyaltyPoints": {
      "type": "integer",
      "description": "The total points moved across every programme. The per-programme outcome is `loyaltyProgrammes`."
     }
    }
   },
   "loyaltyProgrammes": {
    "type": "array",
    "description": "**One entry per loyalty programme either record belonged to (decided 28 September, audit R149).** Points are added and the higher tier is kept, per programme — a single points number cannot say which programme it belongs to.\n",
    "items": {
     "type": "object",
     "required": [
      "programmeId",
      "pointsAdded",
      "resultingPoints"
     ],
     "properties": {
      "programmeId": {
       "type": "string",
       "format": "uuid"
      },
      "pointsAdded": {
       "type": "integer",
       "description": "The absorbed record's balance in this programme, added to the survivor's."
      },
      "resultingPoints": {
       "type": "integer"
      },
      "tierKept": {
       "type": "string",
       "nullable": true,
       "description": "The higher of the two records' tiers in this programme."
      }
     }
    }
   },
   "consentOutcome": {
    "type": "array",
    "description": "Per purpose, the resulting position. Where the two profiles disagreed, the more restrictive position won.\n",
    "items": {
     "type": "object",
     "properties": {
      "purpose": {
       "$ref": "#/components/schemas/ConsentPurpose"
      },
      "result": {
       "$ref": "#/components/schemas/ConsentDecision"
      },
      "wasRestricted": {
       "type": "boolean"
      }
     }
    }
   }
  }
 },
 "Money": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n",
  "required": [
   "amount",
   "currency",
   "scale"
  ],
  "properties": {
   "amount": {
    "type": "string",
    "description": "Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n",
    "pattern": "^-?\\d+(\\.\\d{1,4})?$"
   },
   "currency": {
    "type": "string",
    "description": "**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n",
    "pattern": "^[A-Z]{3}$"
   },
   "scale": {
    "type": "integer",
    "description": "Resolved from the region alongside `currency`.",
    "minimum": 0,
    "maximum": 4
   }
  }
 },
 "OpenTableVisitRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "tableId",
   "covers",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "tableId": {
    "type": "string",
    "format": "uuid"
   },
   "covers": {
    "type": "integer",
    "minimum": 1,
    "description": "Captured at seating because it drives split-by-covers at close."
   },
   "serverPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
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
 "RefireReason": {
  "type": "string",
  "description": "Why a line was made again (`refireItem`). The reasons are the data.",
  "enum": [
   "overcooked",
   "undercooked",
   "wrongItem",
   "dropped",
   "cold",
   "allergyRisk",
   "guestChangedMind",
   "lateAdd"
  ]
 },
 "RestaurantWaitlist": {
  "type": "object",
  "x-ticvai-persistence": "fnb.waitlist_entry",
  "description": "BL-130. **Distinct from `queue`, which is for rides.** A restaurant waitlist has a party size, a table preference and a walk-away point, and a guest who leaves is not the same as a guest who was served.\n",
  "required": [
   "id",
   "outletId",
   "partySize",
   "status",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
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
   "partySize": {
    "type": "integer"
   },
   "quotedWaitMinutes": {
    "type": "integer",
    "nullable": true
   },
   "seatingPreference": {
    "type": "string",
    "enum": [
     "any",
     "indoor",
     "outdoor",
     "bar",
     "booth",
     "highChair"
    ],
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "waiting",
     "notified",
     "seated",
     "walkedAway",
     "noShow",
     "cancelled"
    ]
   },
   "notifiedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "**When the party joined, on the device.** The wait a party had is measured from here to `notifiedAt` or to seating, which is the report `walkedAway` exists for. Required on a join — the operation is offline-capable."
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "holdExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**How long a table waits for somebody who was called.** Too short and a guest returning from the bathroom loses it; too long and the table sits empty at peak — which is why it is a setting rather than a constant.\n"
   }
  }
 },
 "SectionLayout": {
  "type": "object",
  "description": "An outlet's floor divided into sections, each with its server (`setSectionLayout`).",
  "required": [
   "sections"
  ],
  "properties": {
   "sections": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "name",
      "tableIds"
     ],
     "properties": {
      "name": {
       "type": "string"
      },
      "tableIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      },
      "serverPrincipalId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "servicePeriod": {
       "type": "string",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "ServiceMode": {
  "type": "string",
  "enum": [
   "quickService",
   "tableService",
   "roomService",
   "collection",
   "delivery"
  ]
 },
 "SplitBillRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "method",
   "recordedAt"
  ],
  "properties": {
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time of the split (offline-capable)."
   },
   "method": {
    "$ref": "#/components/schemas/SplitMethod"
   },
   "parts": {
    "type": "integer",
    "minimum": 2,
    "description": "For `byCovers` — defaults to the visit's cover count."
   },
   "amounts": {
    "type": "array",
    "description": "For `byAmount`. Must sum to the bill total.",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/Money"
    }
   },
   "lineAssignments": {
    "type": "array",
    "description": "For `byLine` or `bySeat`. Every line must be assigned exactly once.",
    "items": {
     "type": "object",
     "required": [
      "lineId",
      "partIndex"
     ],
     "properties": {
      "lineId": {
       "type": "string"
      },
      "partIndex": {
       "type": "integer",
       "minimum": 0
      }
     }
    }
   },
   "categoryAssignments": {
    "type": "array",
    "description": "For `byCategory` — food to one part, beverage to another.",
    "items": {
     "type": "object",
     "required": [
      "categoryCode",
      "partIndex"
     ],
     "properties": {
      "categoryCode": {
       "type": "string"
      },
      "partIndex": {
       "type": "integer",
       "minimum": 0
      }
     }
    }
   }
  }
 },
 "SplitMethod": {
  "type": "string",
  "enum": [
   "byAmount",
   "byCovers",
   "byCategory",
   "byLine",
   "bySeat"
  ]
 },
 "TableCombination": {
  "type": "object",
  "x-ticvai-persistence": "fnb.table_combination",
  "description": "**Tables that can be pushed together, and what they seat together.** Declared by a host rather than inferred from a floor plan — a pillar, a step or a service run stops two adjacent tables combining. `setTableCombinations` writes the outlet's set.\n",
  "required": [
   "tableIds",
   "combinedCovers"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "outletId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The outlet in the path."
   },
   "tableIds": {
    "type": "array",
    "minItems": 2,
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "combinedCovers": {
    "type": "integer",
    "minimum": 1
   },
   "setupMinutes": {
    "type": "integer",
    "default": 5
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `outlet` scope."
   }
  }
 },
 "TableDefinition": {
  "x-ticvai-persistence": "fnb.dining_table",
  "type": "object",
  "description": "A restaurant (dining) table, reserved with `createTableReservation`. Not a map-bookable `resources` table, which is a non-dining spot sold like a cabana (decided 29 September, rev 3 GAP-C2).",
  "required": [
   "id",
   "label",
   "capacity"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "label": {
    "type": "string",
    "maxLength": 32,
    "x-ticvai-unique": "venue",
    "description": "**The table code, unique per venue** (decided 28 September, audit R108). Two tables in one venue never share a label, across all its outlets, so *T12* names one table wherever it is read. `createTable` and `updateTable` refuse a duplicate with `409` `duplicate-code`.\n"
   },
   "capacity": {
    "type": "integer",
    "minimum": 1
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "position": {
    "type": "object",
    "properties": {
     "x": {
      "type": "number"
     },
     "y": {
      "type": "number"
     }
    }
   },
   "shape": {
    "type": "string",
    "enum": [
     "round",
     "square",
     "rectangle",
     "booth",
     "bar"
    ]
   },
   "isOutOfService": {
    "type": "boolean",
    "default": false,
    "description": "**Damaged, or its section closed.** `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`."
   }
  }
 },
 "TableMap": {
  "x-ticvai-persistence": "none — projection",
  "type": "object",
  "required": [
   "outletId",
   "tables"
  ],
  "properties": {
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "zones": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "tables": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/TableState"
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
 "TableState": {
  "x-ticvai-persistence": "none — projection over table and visit",
  "allOf": [
   {
    "$ref": "#/components/schemas/TableDefinition"
   },
   {
    "type": "object",
    "required": [
     "status"
    ],
    "properties": {
     "status": {
      "$ref": "#/components/schemas/TableStatus"
     },
     "visitId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "covers": {
      "type": "integer",
      "nullable": true
     },
     "seatedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "serverPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "billTotal": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    }
   }
  ]
 },
 "TableVisit": {
  "x-ticvai-persistence": "fnb.table_visit",
  "type": "object",
  "required": [
   "id",
   "tableId",
   "outletId",
   "covers",
   "status",
   "orders",
   "openedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "tableId": {
    "type": "string",
    "format": "uuid"
   },
   "tableLabel": {
    "type": "string"
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "covers": {
    "type": "integer"
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "billRequested",
     "settled",
     "merged",
     "cancelled"
    ]
   },
   "serverPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orders": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/FnbOrder"
    }
   },
   "mergedIntoVisitId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "mergedFromVisitIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "runningTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "gratuity": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "readOnly": true,
    "description": "The gratuity taken at `closeTableVisit`. **Not the service charge**, which is revenue (`FnbServiceChargePolicy`); this is the guest's tip, and `reassignServer` decides who shares it."
   },
   "openedAt": {
    "type": "string",
    "format": "date-time"
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "TenderKind": {
  "type": "string",
  "description": "`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n",
  "enum": [
   "cash",
   "card",
   "wallet",
   "voucher",
   "bankTransfer",
   "hotelCharge",
   "installment",
   "giftCard",
   "complimentary"
  ]
 }
}
```
