# Page Inventory

> **Purpose:** Every screen, its capability, and the APIs it calls  
> **Owner:** Chinmay + design  
> **Status:** **v3 — five platforms added from the screen hierarchy**

Part of the build handoff. See [api-list](api-list.md) and [schema](schema.md).

## What changed in v3 — CF-47 closed

v2 was rebuilt from the client UI/UX boards, which cover the **apps**. Five platforms have
no board and were therefore absent entirely: the B2C web storefront, the Platform Admin
Console, the Partner Portal, the Accreditation Portal and the Support Console.

They are in the client's own screen hierarchy (`TAIS_Phase1_Platform_and_Screen_Hierarchy`),
which is where these come from.

| Platform | v2 | v3 | Delta |
|---|---|---|---|
| White Label Builder | 20 | 20 | — |
| Guest App | 60 | 60 | — |
| Employee App | 50 | 50 | — |
| POS · Scanner · Back office | 73 | 73 | — |
| **P01 Guest Web Storefront** | — | **29** | **New** |
| **P09 Platform Admin Console** | — | **36** | **New** |
| **P10 Partner & Reseller Portal** | — | **21** | **New** |
| **P11 Accreditation Portal** | — | **8** | **New** |
| **P12 Support Agent Console** | — | **8** | **New** |
| **Total** | **203** | **305** | **+102** |

**Frontend estimates increase again.** v1 → v2 was +105%; v2 → v3 is a further +50%.

Two of the five are not a surprise in scope, only in inventory — the storefront and the
partner portal were always in the proposal. The Platform Admin Console at 36 screens is the
one worth pausing on: it is the largest single platform after the back office, it is entirely
Control Plane, and none of it was in any estimate before today.

## What changed in v2

Rebuilt against `TICVAI_White_Label_Guest_App_UI_Reference` (8 boards) and
`TICVAI_Employee_App_UI_Reference` (5 boards). **v1 undercounted by ~130 screens.**

| App | v1 | v2 | Delta |
|---|---|---|---|
| White Label Builder | — | **20** | **New context** |
| Guest App | 14 | **60** | +46 |
| Employee App | 12 | **50** | +38 |
| POS · Scanner · Back office | 73 | 73 | — |
| **Total** | **99** | **203** | |


## White Label Builder

React web — back office. **NEW CONTEXT**

| ID | Screen | Capability | APIs | Wave | Notes |
|---|---|---|---|---|---|
| WLB-001 | Tenant Dashboard (Overview) | C57 | `GET /tenant-config` | 1 | App status, active modules 18/24, active pages 42/58, recent changes |
| WLB-002 | Brand Identity – Logo & Icons | C57 | `PUT /tenant-config/brand` | 1 | Logo, favicon. PNG/SVG, max 2MB |
| WLB-003 | Splash Screen | C57 | `PUT /tenant-config/splash` | 1 | Multiple images, duration, fallback colour, loading indicator |
| WLB-004 | App Icon | C57 | `PUT /tenant-config/icons` | 1 | **Build-time.** iOS 1024, SpotLight 512, Android 512/432 |
| WLB-005 | Color Theme | C57 | `PUT /tenant-config/theme` | 1 | Primary, secondary, accent, background, text + live preview |
| WLB-006 | Font Management | C57 | `PUT /tenant-config/fonts` | 1 | **Arabic + Latin pairs.** Tajawal/Roboto. Custom font upload |
| WLB-007 | Header Configuration | C57 | `PUT /tenant-config/header` | 1 | Three layout variants, logo/menu/notification toggles |
| WLB-008 | Footer / Bottom Navigation | C57 | `PUT /tenant-config/navigation` | 1 | Nav type, ordered menu items, visibility per item |
| WLB-009 | Navigation Menu Configuration | C57 | `PUT /tenant-config/navigation` | 1 | Main menu vs More menu |
| WLB-010 | Live Preview – Mobile App | C57 | `GET /tenant-config/preview` | 1 | iOS/Android, light/dark, **EN/AR** |
| WLB-011 | Homepage Layout Builder | C105 | `PUT /tenant-config/homepage` | 1 | **Drag-and-drop sections.** Hero, quick actions, tickets, what's on, attractions, membership, dining, promotions, map, custom |
| WLB-012 | Banner Management | C105 | `GET/POST /tenant-config/banners` | 1 | Scheduled/active/expired states, date windows |
| WLB-013 | Promotional Block Management | C105 | `GET/POST /tenant-config/promo-blocks` | 1 | Active/scheduled/inactive |
| WLB-014 | Custom Content Pages | C105 | `GET/POST /tenant-config/pages` | 1 | Published/draft, slug per page |
| WLB-015 | FAQ Management | C105 | `GET/POST /tenant-config/faqs` | 2 | Categorised, surfaces in guest Help |
| WLB-016 | Policy & Terms Management | C105 | `GET/PUT /tenant-config/policies` | 1 | **Per-language versions** — EN/AR/FR. Rich text editor |
| WLB-017 | Module & Page Enablement | C75 | `PUT /tenant-config/modules` | 1 | **This is the licensing model surfaced.** Disabled modules hidden from guest app |
| WLB-018 | Tenant-Specific Features | C75 | `PUT /tenant-config/features` | 1 | Digital Companion, AI Concierge, Lost & Found, Push, Social, Multi-language, Apple Wallet, Google Pay, Cash on Delivery |
| WLB-019 | Preview & Publish | C106 | `POST /tenant-config/publish` | 1 | **Draft → Review → Preview → Publish workflow** |
| WLB-020 | Version History | C106 | `GET /tenant-config/versions` | 1 | **Restore Previous Version.** v2.3.1 etc, published-by, status |

## Guest App

React Native — white-label per tenant

| ID | Screen | Capability | APIs | Wave | Notes |
|---|---|---|---|---|---|
| GST-001 | Home – Default | C02 | `GET /catalogue, local` | 1 | Hero, quick actions, What's On |
| GST-002 | Explore Categories | C02 | `GET /catalogue` | 1 | Attractions, exhibitions, events, dining, shop, experiences |
| GST-003 | Attractions List | C02 | `GET /products` | 1 | Filter: indoor/outdoor/family/heritage. Duration shown |
| GST-004 | Attraction Details | C02 | `GET /products/{id}` | 1 | Rating, duration, best time, suitability, location |
| GST-005 | What's On | C84 | `GET /events` | 1 | Exhibitions, events, workshops |
| GST-006 | Event / Exhibition Details | C84 | `GET /events/{id}` | 1 | Hours, duration, language, age |
| GST-007 | Select Date & Time | C02, C103 | `GET /performances, POST /leases` | 1 | Calendar + time slots. **Lease acquired here** |
| GST-008 | Tickets & Add-ons | C02, C88 | `local` | 1 | Adult/child/senior tiers, add-ons |
| GST-009 | Review & Payment | C47 | `POST /orders` | 1 | Order summary, **VAT line**, payment method |
| GST-010 | Booking Confirmation | C02 | `GET /orders/{id}` | 1 | QR, booking ID, Add to Wallet |
| GST-011 | Wallet Overview | C37 | `GET /wallet` | 2 | Balance, add money, payment methods, transactions |
| GST-012 | My Tickets | C02 | `GET /tickets` | 1 | Upcoming/used/cancelled tabs, QR per booking |
| GST-013 | Ticket Details | C02 | `GET /tickets/{id}` | 1 | QR, transfer, Add to Apple Wallet |
| GST-014 | Ticket Transfer | C02 | `POST /tickets/{id}/transfer` | 2 | **Per-ticket selection**, transfer by email/phone, message |
| GST-015 | Memberships | C03 | `GET /memberships` | 2 | Tier card, benefits grid, members, renew, history |
| GST-016 | My Reservations | C02 | `GET /reservations` | 2 | Confirmed/pending states |
| GST-017 | Reservation Details | C02 | `GET /reservations/{id}` | 2 | Meeting point, reschedule, cancel |
| GST-018 | Add to Calendar / Reminders | C02 | `local` | 3 | Apple/Google/Outlook, reminder offsets |
| GST-019 | Order History (Wallet) | C21 | `GET /orders` | 2 | Payments, refunds, top-ups. **Download statement** |
| GST-020 | Saved Items / Wishlist | C58 | `GET /wishlist` | 3 |  |
| GST-021 | Interactive Map | C39 | `GET /venue-map` | 2 | Layers: attractions, dining, shops, restrooms, first aid, services, parking. **Weather chip** |
| GST-022 | Attraction Wait Times | C82 | `GET /queue/wait-times` | 3 | **Third-party feed (ADR-0012).** Height req shown |
| GST-023 | Virtual Queue / Join Queue | C82 | `POST /queue-entries` | 3 | Queue number, parties ahead, leave queue |
| GST-024 | F&B – Browse & Order | C05 | `GET /menu` | 2 | Restaurants, cafés, snacks, beverages |
| GST-025 | F&B – Order Tracking | C05, C07 | `GET /fnb-orders/{id}` | 2 | **Received→Preparing→Ready→Completed.** Pickup location, order QR |
| GST-026 | Retail / Merchandise | C08 | `GET /products?kind=retail` | 2 | Categories, best sellers, cart badge |
| GST-027 | Parking – Reserve & Pay | C23 | `POST /parking-reservations` | 3 | Date, time, vehicle type, zone |
| GST-028 | Parking – Reservation Confirmed | C23 | `GET /parking-reservations/{id}` | 3 | QR, plate, Add to Wallet, directions |
| GST-029 | Venue Info & Services | C17 | `GET /venue-info` | 2 | Restrooms, first aid, prayer room, lost & found, accessibility, wifi, ATM |
| GST-030 | In-Venue Notifications | C61 | `GET /notifications` | 2 | Alerts, offers, updates. Show starting, queue ready, weather |
| GST-031 | AI Concierge – Home | AI-02 | `POST /ai/concierge` | 2 | Popular questions |
| GST-032 | AI Concierge – Chat | AI-02 | `POST /ai/concierge` | 2 | Structured cards + quick actions |
| GST-033 | AI Concierge – Contextual Help | AI-02 | `POST /ai/concierge` | 2 | **Live wait time inside the chat** — grounded, not generated |
| GST-034 | Lost & Found | C18 | `POST /lost-found/reports` | 2 | Report vs Found tabs, **photo upload to 5**, category, last seen |
| GST-035 | Feedback & Ratings | C62 | `POST /reviews` | 3 | Star rating, aspect chips, opt-in |
| GST-036 | Loyalty & Rewards | C64 | `GET /loyalty` | 3 | Tier, points to next, benefits, transactions |
| GST-037 | Offers & Promotions | C86 | `GET /offers` | 2 | Special/member-exclusive/family tags, validity |
| GST-038 | Digital Companion Mode | C105 | `GET /tenant-config/features` | 3 | **Before / During / After visit journey.** Tenant-toggleable |
| GST-039 | Profile | C58 | `GET /guests/me` | 1 | Personal info, **family members**, payment methods, preferences, privacy |
| GST-040 | Help & Support | C17 | `GET /support` | 2 | Live chat, call, email, help centre, report a problem |
| GST-041 | Checkout Entry | C56 | `—` | 1 | **Continue as Guest** / Sign in / **UAE PASS** |
| GST-042 | Simple Registration & OTP | C56 | `POST /auth/guest/otp` | 1 | **OTP via WhatsApp or SMS** |
| GST-043 | Arabic / RTL Experience | C57 | `—` | 1 | **Full RTL mirror.** Not a translation layer |
| GST-044 | Multi-Currency & Pricing | C107 | `GET /currencies` | 2 | **Display currency ≠ settlement currency.** 'Payment processed in AED' |
| GST-045 | Ticket Delivery & Sharing | C02 | `POST /tickets/{id}/share` | 2 | WhatsApp, SMS, email, Add to Wallet |
| GST-046 | Branded Queue / Waiting Room | C98 | `GET /waiting-room` | 1 | **Virtual Waiting Room.** Queue ID, position, estimated wait |
| GST-047 | Maintenance Page | C57 | `GET /tenant-config/status` | 1 | Branded, expected-back time, social links |
| GST-048 | Upsell / Cross-Sell | C88, AI-36 | `GET /recommendations` | 2 | Membership upgrade + add-ons inline at checkout |
| GST-049 | Interactive Seat Selection | C53 | `GET /seat-maps/{id}` | 2 | **Available/selected/sold/wheelchair legend.** VIP vs regular blocks |
| GST-050 | Resource Booking – Cabana | C78 | `POST /resource-bookings` | 3 | Capacity, features, date/time, price |
| GST-051 | Plan Your Adventure – Start | AI-35 | `POST /ai/itinerary` | 3 | 4-step wizard: date, group type, interests |
| GST-052 | Suggested Itineraries | AI-35 | `GET /itineraries/suggested` | 3 | Family/thrill/culture/relaxed personas |
| GST-053 | Build Your Own Itinerary | C02 | `POST /itineraries` | 3 | Timeline, total time + **walking time** |
| GST-054 | AI Optimized Itinerary | AI-35 | `POST /ai/itinerary/optimise` | 3 | **Min wait / shortest walk / best experience.** Route drawn on map |
| GST-055 | Dynamic QR Ticket | C09 | `GET /tickets/{id}/dynamic-qr` | 1 | **Auto-refresh, countdown to expiry.** Anti-screenshot |
| GST-056 | Bundle Package | C87 | `GET /bundles/{id}` | 2 | Savings badge, itemised inclusions |
| GST-057 | Accessibility Information | C17 | `GET /accessibility` | 2 | Per attraction: wheelchair, min height, service animals, elevator |
| GST-058 | Resource Availability (Cabana) | C78 | `GET /resources/availability` | 3 | **Remaining count per unit** |
| GST-059 | Plan My Day – In Progress | C02 | `GET /itineraries/{id}` | 3 | Confirmed vs upcoming per stop |
| GST-060 | Maintenance / Upgrade Page | C57 | `GET /tenant-config/status` | 1 | Duplicate of board 7 screen 7 — consolidate |

## Employee App

React Native — offline-partial

| ID | Screen | Capability | APIs | Wave | Notes |
|---|---|---|---|---|---|
| EMP-001 | Login / SSO / Biometric | C56, C35 | `POST /auth/login` | 1 | **Biometric + SSO.** C35 was REF-tagged — now confirmed |
| EMP-002 | Role & Venue Selection | C56 | `POST /auth/select-role` | 1 | **Confirms ADR-0003.** Venue selection alongside role |
| EMP-003 | Role-Based Home Dashboard | C56 | `GET /auth/session` | 1 | Filtered by effectivePermissions |
| EMP-004 | More / Role-Based Modules | C56 | `GET /auth/session` | 1 |  |
| EMP-005 | Notification Center | C61 | `GET /notifications` | 2 |  |
| EMP-006 | Notification Detail / Action | C61 | `GET /notifications/{id}` | 2 |  |
| EMP-007 | Universal Search | AI-01 | `POST /ai/search` | 2 | **AI-powered.** Cross-module |
| EMP-008 | Create Request Hub | C15 | `POST /requests` | 2 | Single entry to all request types |
| EMP-009 | Employee Profile / Digital ID | C56 | `GET /principals/me` | 1 | **Digital employee ID — scannable** |
| EMP-010 | Settings / Preferences / Security | C36 | `GET/PUT /principals/me/settings` | 2 |  |
| EMP-011 | My Tasks & Work Orders | C11 | `GET /work-orders` | 2 |  |
| EMP-012 | Task Detail | C11 | `GET /work-orders/{id}` | 2 |  |
| EMP-013 | Work Order Detail | C11 | `GET /work-orders/{id}` | 2 |  |
| EMP-014 | Start / Pause / Complete Work Order | C11 | `PATCH /work-orders/{id}` | 2 | **Timer** |
| EMP-015 | Asset Scan | C13 | `GET /assets/{code}` | 3 |  |
| EMP-016 | Asset Detail | C13 | `GET /assets/{id}` | 3 |  |
| EMP-017 | Asset History / Documents / SOP | C94 | `GET /assets/{id}/history` | 3 | **SOP attached to asset** |
| EMP-018 | Safety Inspection / Checklist | C12 | `POST /inspections` | 2 | Opening/closing checklists |
| EMP-019 | Report Incident / Hazard | C12 | `POST /incidents` | 2 | Photo-first |
| EMP-020 | Incident Detail / Resolution | C12 | `GET /incidents/{id}` | 2 |  |
| EMP-021 | Inventory Scan / Lookup | C13 | `GET /inventory/{code}` | 3 |  |
| EMP-022 | Inventory Item Detail | C13 | `GET /inventory/{id}` | 3 |  |
| EMP-023 | Stock Count | C13 | `POST /stock-counts` | 3 |  |
| EMP-024 | Goods Receipt | C14 | `POST /goods-receipts` | 3 |  |
| EMP-025 | Stock Issue / Return | C13 | `POST /stock-movements` | 3 |  |
| EMP-026 | Inventory Transfer | C13 | `POST /stock-transfers` | 3 |  |
| EMP-027 | Low Stock / Auto-Requisition | C14, AI-43 | `GET /requisitions/suggested` | 3 | **Par-level auto-draft** |
| EMP-028 | Purchase Request | C14 | `POST /purchase-requests` | 3 |  |
| EMP-029 | Purchase Request / PO Progress | C14 | `GET /purchase-orders/{id}` | 3 |  |
| EMP-030 | Approval Center / Workflow | C15 | `GET /approvals` | 1 |  |
| EMP-031 | My Roster / Weekly Timetable | C16 | `GET /rosters` | 2 |  |
| EMP-032 | Shift Detail / Zone Assignment | C16 | `GET /shifts-roster/{id}` | 2 | **Zone assignment** |
| EMP-033 | Shift Swap / Open Shift / Overtime | C16 | `POST /shift-swaps` | 3 | **Not modelled** — swap marketplace |
| EMP-034 | Leave Request | C16 | `POST /leave-requests` | 3 |  |
| EMP-035 | Break Management | C16, C01 | `POST /breaks` | 2 | **Ties to shift suspend** — 12 Aug §1 |
| EMP-036 | Team / Supervisor View | C16 | `GET /teams` | 2 | On time / pending / absent |
| EMP-037 | Operations Communication / Announcements | C61 | `GET /announcements` | 2 |  |
| EMP-038 | Guest Services / Employee Assistance | C17 | `GET /guest-services` | 2 |  |
| EMP-039 | Attraction Status / Capacity Counter | C39 | `GET /venue-status` | 2 | **Live capacity counter** |
| EMP-040 | Lost & Found | C18 | `GET/POST /lost-found` | 2 |  |
| EMP-041 | Universal Scanner | C09, C10 | `POST /access/validate` | 1 | **7 scan types:** ticket, membership, **accreditation**, asset, inventory, employee ID, NFC |
| EMP-042 | Ticket Validation – Valid | C09 | `POST /access/validate` | 1 | Mark as Entered, Scan Next |
| EMP-043 | Ticket Validation – Invalid | C09 | `POST /access/validate` | 1 | Reason, first-scan detail, **Escalate to Supervisor** |
| EMP-044 | Membership / Accreditation Validation | C03, C30 | `POST /access/validate` | 2 | **Accreditation on the scanner** — CF-21 not deferrable |
| EMP-045 | Venue Map / Operational Map | C39 | `GET /venue-map` | 2 | Attraction status, wait time, height req, incidents, zones |
| EMP-046 | TICVAI AI Assistant (Home) | AI-06 | `POST /ai/assistant` | 2 | **Primary nav tab** |
| EMP-047 | AI – Contextual Assistance | AI-06 | `POST /ai/assistant` | 2 | **Cites source: 'F&B SOP Manual v2.1 – Section 4.3'.** Grounded |
| EMP-048 | Training / Knowledge Base | C108 | `GET /training` | 3 | **NEW.** SOPs, manuals, videos, progress, due dates |
| EMP-049 | Employee Recognition / Kudos | C109 | `POST /kudos` | 3 | **NEW.** Categories, message, recipient |
| EMP-050 | Offline & Synchronization Center | C24 | `GET /sync/status` | 1 | **Pending by category, auto-sync toggle, Sync Now** |

---

## New capabilities this surfaced

| ID | Capability | Why |
|---|---|---|
| **C105** | **Tenant content management** — homepage layout builder, banners, promo blocks, custom pages, FAQs, policies per language | 6 builder screens. C57 covered branding only |
| **C106** | **Tenant config publishing** — draft → review → preview → publish, version history with restore | 2 screens. Same problem shape as catalogue bundles; should reuse that machinery |
| **C107** | **Multi-currency display** — display currency separate from settlement currency | Guest board 7 screen 4. Not the same as ADR-0008 money scale |
| **C108** | **Training & knowledge base** — SOPs, manuals, videos, progress, due dates | Employee 48. **No requirement, no MoM** |
| **C109** | **Employee recognition** — kudos, categories, recipients | Employee 49. **No requirement, no MoM** |

C108 and C109 are tagged `DESIGN` — they appear in a rank-3 design reference only, so they
are not scope until they appear in the matrix or a MoM.

## Screens with no prior capability

| Screen | Note |
|---|---|
| Shift Swap / Open Shift / Overtime | A swap marketplace. C16 covers rostering, not trading shifts |
| Digital Companion Mode | Before/during/after visit journey. Tenant-toggleable feature |
| Dynamic QR Ticket | Auto-refresh with visible countdown. C09 has the mechanism; the guest-facing screen was not inventoried |
| Employee Digital ID | Scannable staff credential. Adjacent to accreditation |

## Confirmations

- **C35 staff authentication modes** was `REF`-tagged and unvalidated. Employee screen 1 shows biometric and SSO login — **promote to scope**
- **C39 venue map** was a candidate. Appears in both guest (screen 21) and employee (screen 45) — **confirmed**
- **Accreditation validation is on the employee scanner** (screen 44), so that domain is not safely deferrable to Wave 4
- **Module enablement toggles** are the licensing model made visible — confirms C75
- **AI is a primary nav tab in the employee app**, so the shell depends on AI-06 existing

## Cross-cutting requirements the boards make explicit

| Requirement | Evidence |
|---|---|
| **RTL is first-class** | Full Arabic mirror screen, Arabic/Latin font pairing, EN/العربية preview toggle. **Must be in `design-tokens` from Sprint 1** |
| **Dark theme** | Employee app is dark by default; builder is light. Both themes needed |
| **WCAG 2.2 Level AA** | Stated on guest board 7 |
| **PCI DSS** | Stated on guest board 7 |
| Dynamic QR | Stated as anti-screenshot with visible expiry |

---

# Platforms added in v3

These have no UI/UX board. Screen names come from the client's screen hierarchy; capability
and API mapping is ours. Where a screen has no contract behind it yet, the API column says so
rather than inventing an endpoint.

## P01 — Guest Web Storefront (B2C)

React web, public. Shares the guest app's contracts almost entirely — same catalogue, same
orders, same guest auth. **The screens differ; the API surface does not.**

| ID | Screen | Capability | APIs | Wave |
|---|---|---|---|---|
| WEB-001 | Home / Landing | C79 | `GET /tenant-config`, `GET /products` | 1 |
| WEB-002 | Event & Attraction Listing | C79 | `GET /products`, `GET /events` | 1 |
| WEB-003 | Search Results | C79 | `GET /products?search` | 1 |
| WEB-004 | Event / Attraction Detail | C79 | `GET /products/{id}`, `GET /performances` | 1 |
| WEB-005 | Ticket Type Selection | C80 | `GET /products/{id}/variants` | 1 |
| WEB-006 | Date & Session Selection | C81 | `GET /performances/{id}/availability` | 1 |
| WEB-007 | Seat Map Selection | C51 | `GET /performances/{id}/seat-availability` | 2 |
| WEB-008 | Add-ons & Upsell | C86 | `POST /upsell-suggestions` | 2 |
| WEB-009 | Wishlist | C79 | **No contract** — guest-scoped list, not yet specified | 3 |
| WEB-010 | Shopping Cart | C02 | `POST /promotions/evaluate` | 1 |
| WEB-011 | Guest Details & Attendee Forms | C03 | `POST /orders` | 1 |
| WEB-012 | Checkout — Payment | C04 | `POST /payments` | 1 |
| WEB-013 | Order Confirmation | C03 | `GET /orders/{id}` | 1 |
| WEB-014 | Payment Link Landing | C04 | `POST /payments` | 2 |
| WEB-015 | Virtual Waiting Room | — | **Q2, not Q1.** Infrastructure, not this contract (ADR-0012) | 2 |
| WEB-016 | Login / Register | C36 | `POST /auth/guest/register`, `/otp`, `/social` | 1 |
| WEB-017 | My Account Dashboard | C36 | `GET /guests/{id}` | 1 |
| WEB-018 | My Tickets | C09 | `GET /orders`, `GET /entitlements` | 1 |
| WEB-019 | Order History | C34 | `GET /orders`, `GET /orders/{id}/statement` | 1 |
| WEB-020 | Profile & Preferences | C36 | `PATCH /guests/{id}`, `POST /guests/{id}/consents` | 1 |
| WEB-021 | Wallet & Gift Cards | C21 | `GET /wallets/{id}`, `GET /gift-cards/{code}` | 2 |
| WEB-022 | Membership Plans | C31 | `GET /products?kind=membership` | 2 |
| WEB-023 | Membership Management | C31 | `GET /entitlements`, `POST /orders/{id}/modify` | 2 |
| WEB-024 | Loyalty & Rewards | C93 | `GET /guests/{id}/loyalty` | 3 |
| WEB-025 | Help Centre / FAQ | C105 | `GET /tenant-config/faqs` | 1 |
| WEB-026 | Survey & Feedback | C33 | `POST /reviews` | 3 |
| WEB-027 | Newsletter Subscription | C59 | `POST /guests/{id}/consents` | 2 |
| WEB-028 | Contact & Venue Information | C105 | `GET /tenant-config/pages` | 1 |
| WEB-029 | Error / Sold Out / Maintenance | C57 | `GET /tenant-config/status` | 1 |

**Wishlist has no contract.** It is a guest-scoped list of product references — small, but it
does not exist in `catalogue` or `marketing-crm` today. Either add it or drop the screen.

## P09 — Platform Admin Console

**Control Plane.** Runs outside any cell. Largest platform after the back office and entirely
absent from every prior estimate.

| ID | Screen | Capability | APIs | Wave |
|---|---|---|---|---|
| ADM-001 | Platform Login / MFA | C35 | `POST /auth/login`, `/auth/mfa/verify` | 1 |
| ADM-002 | Platform Dashboard | C95 | `GET /tenants` | 1 |
| ADM-003 | Cross-Tenant Health Dashboard | C95 | `GET /cells/{id}/health` | 2 |
| ADM-004 | Platform Audit Log | C97 | **No contract** — Control Plane audit not specified | 2 |
| ADM-005 | Tenant Directory | C95 | `GET /tenants` | 1 |
| ADM-006 | Tenant Hierarchy Explorer | C20 | `GET /scope-tree` | 1 |
| ADM-007 | Module & Feature Entitlement | C75 | `GET /tenants/{id}/licences` | 1 |
| ADM-008 | Subscription & Plan Management | C74 | `GET /plans`, `PUT /tenants/{id}/subscription` | 1 |
| ADM-009 | Tenant Billing & Invoicing | C74 | `GET /tenants/{id}/invoices` | 2 |
| ADM-010 | Usage Metering | C74 | `GET /tenants/{id}/usage` | 2 |
| ADM-011 | Licence & Seat Management | C75 | `GET /tenants/{id}/entitlement-usage` | 2 |
| ADM-012 | Tenant Isolation & Resource Pool | C96 | `POST /tenants/{id}/cells` | 1 |
| ADM-013 | Tenant Performance Monitor | C96 | `GET /cells/{id}/health` | 2 |
| ADM-014 | Auto-Scaling Configuration | C96 | **No contract** — infrastructure, Terraform not API | 3 |
| ADM-015 | API Rate Limit & Quota Management | — | **Blocked** — Developer & API workshop | 3 |
| ADM-016 | White-Label Branding Management | C57 | `GET /tenant-config` | 2 |
| ADM-017 | Domain & Certificate Management | C96 | **No contract** — not specified | 2 |
| ADM-018 | Localisation & Language Pack | C57 | `PUT /tenant-config/languages` | 2 |
| ADM-019 | Global Configuration & Defaults | C95 | **No contract** — platform defaults not specified | 2 |
| ADM-020 | Platform User Directory | C56 | `GET /principals` | 1 |
| ADM-021 | Platform Role Management | C56 | `GET /roles`, `POST /roles` | 1 |
| ADM-022 | Release & Version Management | C96 | **No contract** — new scope, 30 Jul | 2 |
| ADM-023 | Staging Promotion & Approval | C96 | **No contract** — new scope, 30 Jul | 2 |
| ADM-024 | Release Notification Composer | C96 | **No contract** — new scope, 30 Jul | 3 |
| ADM-025 | Tenant Upgrade Scheduler | C96 | **No contract** — new scope, 30 Jul | 2 |
| ADM-026 | End-of-Support Notice Management | C96 | **No contract** — new scope, 30 Jul | 3 |
| ADM-027 | Database Migration Console | C96 | **No contract** — **the unowned orchestrator** | 1 |
| ADM-028 | Environment Registry | C96 | **No contract** — not specified | 2 |
| ADM-029 | Deployment Monitor | C96 | `GET /cells/{id}/jobs` | 2 |
| ADM-030 | Infrastructure Sizing & Scaling Policy | C96 | **No contract** — Terraform | 3 |
| ADM-031 | Security & Compliance Dashboard | C97 | **No contract** — not specified | 3 |
| ADM-032 | WAF & Security Policy View | C96 | **No contract** — infrastructure | 3 |
| ADM-033 | Backup & DR Status | C96 | `GET /cells/{id}/health` | 2 |
| ADM-034 | Archival Job Monitor | C96 | **No contract** — retention not specified | 3 |
| ADM-035 | Support & Escalation Console | — | **No contract** — overlaps P12 | 3 |
| ADM-036 | Platform Notification Broadcast | C96 | **No contract** — not specified | 3 |

**19 of 36 have no contract behind them.** Most are the release-management and infrastructure
scope raised on 30 July and never specified. `ADM-027 Database Migration Console` is the user
interface for the orchestrator that has been unowned since the same date.

## P10 — Partner & Reseller Portal (B2B)

Settled 05 August. Credit, allocation and commission are contracted; the portal itself was
never screened.

| ID | Screen | Capability | APIs | Wave |
|---|---|---|---|---|
| PTR-001 | Partner Login / MFA | C35 | `POST /auth/login`, `/auth/mfa/verify` | 2 |
| PTR-002 | Partner Dashboard | C34 | `GET /orders`, `GET /b2b-accounts/{id}/credit` | 2 |
| PTR-003 | Profile & Company Details | C56 | `GET /principals/{id}` | 2 |
| PTR-004 | Notifications | C59 | `POST /messages` | 3 |
| PTR-005 | Inventory & Allocation View | C103 | `GET /envelopes/{id}/channel-allocations` | 2 |
| PTR-006 | Product Catalog (B2B Pricing) | C85 | `GET /products`, `GET /price-lists/{id}` | 2 |
| PTR-007 | Availability Search | C81 | `GET /performances/{id}/availability` | 2 |
| PTR-008 | Booking Creation | C02 | `POST /orders` | 2 |
| PTR-009 | Group / Bulk Booking | C54 | `POST /seat-blocks/{id}/allocate` | 3 |
| PTR-010 | Cart & Quote | C02 | `POST /promotions/evaluate` | 3 |
| PTR-011 | Quote Management | — | **No contract** — quotes are procurement-side only | 3 |
| PTR-012 | Checkout / Credit Purchase | C04 | `POST /payments` | 2 |
| PTR-013 | Credit Limit & Balance | C34 | `GET /b2b-accounts/{id}/credit` | 2 |
| PTR-014 | Settlement & Payment History | C50 | `GET /settlements` | 3 |
| PTR-015 | Order History | C34 | `GET /orders`, `GET /orders/{id}/statement` | 2 |
| PTR-016 | Voucher / Ticket Download | C09 | `POST /orders/{id}/reprints` | 2 |
| PTR-017 | Commission Statement | — | **No contract** — commission not modelled | 3 |
| PTR-018 | Reports & Sales Performance | C21 | `POST /reports/{id}/run` | 3 |
| PTR-019 | API Credentials & Integration | — | **Blocked** — Developer & API workshop | 3 |
| PTR-020 | Sub-Agent Management | C56 | `POST /grants` | 3 |
| PTR-021 | Support & Contact | C32 | `POST /cases` | 3 |

**Two genuine gaps:** B2B quotes (distinct from supplier quotations, which are procurement)
and commission. Neither is modelled anywhere.

## P11 — Accreditation Portal

**Blocked on the Accreditation workshop.** Screens listed so the platform is not forgotten in
estimates; no capability or API mapping until the domain is discussed.

| ID | Screen | Wave |
|---|---|---|
| ACC-001 | Landing / Programme Overview | 3 |
| ACC-002 | Registration Form | 3 |
| ACC-003 | Application Review & Submit | 3 |
| ACC-004 | Application Status Tracking | 3 |
| ACC-005 | Accreditation Badge | 3 |
| ACC-006 | Reviewer Queue | 3 |
| ACC-007 | Reviewer Application Detail | 3 |
| ACC-008 | Credential Register | 3 |

**Accreditation validation still appears on the employee scanner in Wave 1** (employee screen
44). The portal is Wave 3; the validation path is not, and that split is the reason this
workshop is the urgent one of the four.

## P12 — Support Agent Console

| ID | Screen | Capability | APIs | Wave |
|---|---|---|---|---|
| SUP-001 | Agent Login | C35 | `POST /auth/login` | 3 |
| SUP-002 | Agent Dashboard | C32 | `GET /cases` | 3 |
| SUP-003 | Availability & Routing Settings | — | **No contract** — agent routing not modelled | 3 |
| SUP-004 | Conversation Queue | C32 | `GET /cases` | 3 |
| SUP-005 | Live Chat Workspace | C32 | `POST /cases/{id}/messages` | 3 |
| SUP-006 | Knowledge Base Search | C105 | `GET /tenant-config/faqs` | 3 |
| SUP-007 | Canned Response Management | C60 | `GET /message-templates` | 3 |
| SUP-008 | Agent Performance & SLA View | C21 | `POST /reports/{id}/run` | 3 |

Cases, SLA and templates are all contracted. **Agent routing and presence are not** — that is
contact-centre functionality, and whether it is built or integrated is an open question.

---

# Gaps this exercise surfaced

**28 screens across the five platforms have no contract behind them.** They divide cleanly:

| Cause | Screens | Note |
|---|---|---|
| **Release & infrastructure management** | 13 | New scope from 30 Jul, never specified. All P09 |
| **Blocked on a workshop** | 3 | Developer & API, Accreditation |
| **Genuinely unmodelled** | 6 | Wishlist, B2B quotes, commission, agent routing, platform audit, retention |
| **Not an API** | 6 | Terraform, WAF, certificates — infrastructure, not endpoints |

The six unmodelled ones are small and worth adding. The thirteen release-management screens
are not small, and they are the honest answer to why the Platform Admin Console was missed:
**that scope arrived in a workshop and never reached a requirement, a contract or an
estimate.**
