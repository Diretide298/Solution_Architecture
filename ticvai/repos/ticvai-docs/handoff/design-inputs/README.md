# Design inputs from the client meetings

> **Generated** by `tools/build-design-inputs.py` from `mom-design-inputs.yaml` in this folder. Edit the index, never this file.

Every design-relevant statement the client made in the minutes, the workshops and the design reviews, with where it was said and what it applies to. **Each batch's `BRIEF.md` and `BUNDLE.md` carries the ones for its platform, modules and screens** (section *Design inputs from the client meetings*), and each app guide in `handoff/design-batches/apps/` lists the app-wide ones, so a Claude Design session is handed them rather than left to guess.

**1119 inputs: 1089 in force, 30 superseded by a later meeting.** In force: 530 agreed, 506 requested by the client and not yet confirmed, 53 open questions. By reach: 29 global, 137 platform-wide, 41 module, 882 screen-specific.

## How to add an input

The index is authored. When a new MoM, workshop output or design review arrives:

1. Open `handoff/design-inputs/mom-design-inputs.yaml` and append one entry per design statement
   (layout, navigation, components, branding, configurability, flow, states, copy, accessibility,
   Arabic/RTL, offline, device size, motion, density, what a screen must show). Skip backend,
   hosting and commercial points that change nothing a user sees.
2. Give it the next free id (`DI-` and a number; never reuse one), its `source` (`file` relative to
   `ticvai/`, `date`, `section`), a short faithful `text`, its `topic`s and the narrowest true
   `scope`: `global`, a platform (`P04`), a module (`P02/Booking & Selection`, spelled as in
   `screens/P*.yaml`) or screen ids (`GST-004`).
3. `status`: `agreed`, `client-requested` (asked for, not yet confirmed) or `open-question` (state
   the question and the default to build).
4. If it changes an earlier input, list the old id under `supersedes`. The old entry stays in the
   index as history and drops out of every bundle.
5. Run `python3 tools/build-design-inputs.py` (it validates every scope against the screens and
   rewrites this README and the app-guide blocks), then `python3 tools/export-design-batch.py
   <BATCH>` for the batches it touches, or let `tools/refresh.sh` do both.

## Sources

| source | date | inputs |
|---|---|---:|
| `sources/mom/TICVAI_Discry_Wrkshp_Day_1_Jul_28_2026.docx` | 2026-07-28 | 20 |
| `sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf` | 2026-07-29 | 32 |
| `sources/mom/TICVAI_Kickoff_MoM_30Jul2026__2_.docx` | 2026-07-30 | 3 |
| `sources/mom/TICVAI_Followup_MoM_31Jul2026.docx` | 2026-07-31 | 2 |
| `sources/mom/TICVAI_MoM_31Jul2026__1_.docx` | 2026-07-31 | 28 |
| `sources/mom/TICVAI_UIUX_MoM_03Aug2026.docx` | 2026-08-03 | 48 |
| `sources/mom/TICVAI_Kickoff_MoM_2026-08-05.docx` | 2026-08-05 | 14 |
| `sources/mom/TICVAI_BackendDeepDive_MoM_07Aug2026.docx` | 2026-08-07 | 39 |
| `sources/mom/TICVAI_Kickoff_MoM_2026-08-10.docx` | 2026-08-10 | 58 |
| `sources/mom/TICVAI_Kickoff_MoM_12Aug2026.docx` | 2026-08-12 | 34 |
| `sources/mom/TICVAI_MoM_2026-08-14.docx` | 2026-08-14 | 38 |
| `sources/mom/MoM_FnB_Retail_Procurement_Inventory_18Aug2026.docx` | 2026-08-18 | 32 |
| `sources/mom/TICVAI_MoM_2026-08-19_FnB_Retail_Procurement_Inventory.docx` | 2026-08-19 | 21 |
| `docs/active/client-design-boards-audit.md` | 2026-08-20 | 8 |
| `sources/mom/TICVAI_MoM_2026-08-20_CRM_Marketing_CMS.docx` | 2026-08-20 | 30 |
| `sources/mom/TICVAI_MoM_2026-08-21_Seat_Management_CMS.docx` | 2026-08-21 | 24 |
| `sources/mom/TICVAI_MoM_2026-08-24_Infra_Cost_Ticketing.docx` | 2026-08-24 | 6 |
| `sources/mom/TICVAI_MoM_2026-08-25_Ticketing_ProductConfig.docx` | 2026-08-25 | 37 |
| `sources/mom/TICVAI_MoM_2026-08-26_ResourceManagement.docx` | 2026-08-26 | 32 |
| `sources/mom/TICVAI_MoM_2026-08-27_WalletConfiguration.docx` | 2026-08-27 | 32 |
| `sources/mom/TICVAI_MoM_2026-08-31_CS_B2B_Groups_Waivers_SalesChannel.docx` | 2026-08-31 | 52 |
| `sources/mom/TICVAI_MoM_2026-09-01_Pricing_Upgrades_Media_Reservations_Resale.docx` | 2026-09-01 | 32 |
| `sources/mom/TICVAI_MoM_2026-09-02_AccessControl.docx` | 2026-09-02 | 30 |
| `screens/P08-venue-back-office.yaml` | 2026-09-04 | 1 |
| `screens/P11-accreditation-portal.yaml` | 2026-09-07 | 1 |
| `sources/mom/TICVAI_MoM_2026-09-07_Accreditation_Entitlements_VirtualQueue.docx` | 2026-09-07 | 41 |
| `sources/mom/TICVAI_MoM_2026-09-08_BI_Reporting_ApprovalWorkflow.docx` | 2026-09-08 | 43 |
| `docs/active/design-brief-9-september.md` | 2026-09-09 | 1 |
| `sources/mom/TICVAI_MoM_2026-09-09_Rental_POS_Licensing.docx` | 2026-09-09 | 69 |
| `sources/mom/TICVAI_MoM_2026-09-10_LicensingSubscription.docx` | 2026-09-10 | 33 |
| `sources/mom/TICVAI_MoM_2026-09-11_DAM_Gaming.docx` | 2026-09-11 | 43 |
| `sources/mom/TICVAI_MoM_2026-09-15_GuestAppReview_DeviceManagement.docx` | 2026-09-15 | 22 |
| `sources/mom/TICVAI_MoM_2026-09-17_AssetMgmt_Sandbox_API.docx` | 2026-09-17 | 24 |
| `sources/mom/TICVAI_MoM_2026-09-18_AI_Governance_ConfigAssistant_Forecasting_UX.docx` | 2026-09-18 | 28 |
| `sources/mom/TICVAI_MoM_2026-09-21_AI_Recommendation_CorePlatform_Fraud.docx` | 2026-09-21 | 15 |
| `sources/designs/guest-rev3-30-september/BUILD-YOUR-EXPERIENCE.md` | 2026-09-23 | 1 |
| `sources/designs/guest-rev3-30-september/CLIENT-RESPONSE-FEEDBACK-23SEP.md` | 2026-09-23 | 10 |
| `sources/mom/TICVAI_MoM_2026-09-24_BuildReadiness_Infra_UX.docx` | 2026-09-24 | 14 |
| `sources/designs/guest-rev3-30-september/CLIENT-RESPONSE-REV3-25SEP.md` | 2026-09-25 | 1 |
| `sources/designs/guest-rev3-30-september/CLIENT-RESPONSE-REV3-25SEP.md` | 2026-09-28 | 2 |
| `handoff/TICVAI - Decisions Register.xlsx` | 2026-09-29 | 1 |
| `sources/designs/guest-rev3-30-september/ASSETS-NEEDED.md` | 2026-09-29 | 1 |
| `sources/designs/guest-rev3-30-september/CLAUDE-CODE-GAP-FIX.md` | 2026-09-29 | 7 |
| `sources/designs/guest-rev3-30-september/CLIENT-RESPONSE-FEEDBACK-23SEP.md` | 2026-09-29 | 9 |
| `sources/designs/guest-rev3-30-september/CLIENT-RESPONSE-REV3-25SEP.md` | 2026-09-29 | 23 |
| `sources/designs/guest-rev3-30-september/DESIGN-GAP-RESPONSE-23SEP.md` | 2026-09-29 | 7 |
| `sources/designs/guest-rev3-30-september/EMAIL-TO-CLIENT.md` | 2026-09-29 | 1 |
| `sources/designs/guest-rev3-30-september/STATUS-29SEP.md` | 2026-09-29 | 4 |
| `sources/designs/guest-rev3-30-september/TICVAI Engine Controls Manual.dc.html` | 2026-09-29 | 7 |
| `sources/mom/TICVAI_MoM_2026-09-29_Licensing_B2C_Review.md` | 2026-09-29 | 23 |
| `sources/designs/guest-rev3-30-september/CLIENT-RESPONSE-30SEP.md` | 2026-09-30 | 8 |
| `sources/mom/TICVAI_MoM_2026-09-30_Tracker_MobileAppRedesign.docx` | 2026-09-30 | 21 |
| `handoff/TICVAI - Decisions Register.xlsx` | 2026-10-01 | 6 |

## Open questions

Built to the stated default until answered.

- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)* — scope: P09, P08
- **Open question.** POS catalogue: Chinmay's middle ground is an online real-time catalogue that falls back automatically to the last-synced catalogue if connectivity is lost; local-first vs online-first still to be compared (case study). *(open · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-066)* — scope: P04
- **Open question.** Qossai asked whether a cashier on a tablet could use the POS via a browser URL. A lightweight web POS will be considered; it would have no offline support (installed thick client required for offline). *(open · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-067)* — scope: P04
- **Open question.** Allam: alongside search, provide always-visible "hot function" buttons for high-frequency actions (refund, check transaction, print last receipt). Softlabs to recommend the right balance of hot buttons and search. *(open · MoM 3 Aug 2026, 3. UX Design Approach Discussion · DI-088)* — scope: P04
- **Open question.** Two selection patterns: (a) event, date, time, see availability, then product; (b) product, quantity, date, then only time slots with enough capacity. How many customization scenarios to support needs deeper UI exploration. *(open · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-118)* — scope: P01/Booking & Selection, P02/Booking & Selection
- **Open question.** Access-control scan result screens show customer photo, ticket information and validity status; details deferred to a future workshop. *(open · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-129)* — scope: SCN-003, SCN-009
- **Open question.** POS hot functions are not settled: Allam proposed a hybrid of always-visible buttons and a search-driven "magic banner" and asked Softlabs to recommend the balance; Qossai agreed a combination might be ideal and deferred. The minute names Refund, Check transaction and Print last receipt. *(open · MoM 3 Aug 2026, UX Design Approach Discussion · DI-132)* — scope: POS-002
- **Open question.** AI concierge chat design is deferred until a dedicated AI workshop settles the technical approach (third-party LLM with PII masking) and the token/billing model. *(open · MoM 10 Aug 2026, 4.2 AI Concierge Chat — Open Item · DI-195)* — scope: GST-031, GST-032, WEB-044
- **Open question.** Customisable venue map showing attractions, dining, retail and restrooms. Qossai: define image/format guidance for tenant map uploads; benchmark is the Kidzania app's interactive 3D-style map. Final guidance still open. *(open · MoM 10 Aug 2026, 4.4 Venue Map, Queueing, F&B, Retail & Parking · DI-203)* — scope: GST-021, WEB-039, BO-092
- **Open question.** Open: alongside curated pre-built packages, let guests build their own bundle in the cart, with the system detecting eligible combinations and applying an automatic discount (e.g. 5–10%). *(open · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-221)* — scope: GST-056, WEB-010, GST-009
- **Open question.** Open: publishing model — each client's own App/Play Store listing vs one universal TICVAI app where the user selects the venue; and a client module with customisation screens plus a CI/CD-linked publish action vs a canvas the client exports and publishes. Softlabs to present pros/cons. *(open · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-251)* — scope: CMS-104, P02
- **Open question.** Live workstation monitor with department-level health; proposed graphical park-map view of workstation locations and live status, depending on venue zone metadata, with manual drag-and-drop placement as fallback. *(open · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-304)* — scope: BO-128
- **Open question.** F&B dashboards are role-based: the F&B Director sees all outlets, an outlet manager sees only their own outlet. Detailed design of the role-based dashboards (Director vs. outlet-level roles) is still to be finalised. *(open · MoM 18 Aug 2026, 4.10 F&B Stock, Wastage & Requisitions; 6. Open Items · DI-318)* — scope: BO-727, P08/Food & Beverage
- **Open question.** Allam: a user's visibility must be restrictable to specific outlets (an F&B manager of one outlet should not see other outlets' items); also relevant for ticketing/event-specific access. Implementation approach still open. *(open · MoM 18 Aug 2026, 4.6 Role-Based & Outlet-Level Access Control — Open Item · DI-331)* — scope: P08
- **Open question.** Allam: support bulk stock-taking with handheld RFID scanners — scanning a batch of tagged items updates system quantities once verified and saved. Chinmay's focus is reconciling existing stock vs. newly scanned data. Device specs pending. *(open · MoM 19 Aug 2026, 4.6 RFID/Barcode-Based Bulk Stock Counting — Open Item · DI-365)* — scope: EMP-069, EMP-066
- **Open question.** Loyalty accrues points by product/spend tier (e.g. bronze/silver/gold thresholds) and unlocks tier benefits (e.g. platinum-tier discounts on F&B and ticketing). Full programme configuration (tiers, points, redemption, expiry) pending a dedicated session. *(open · MoM 20 Aug 2026, 4.5 Loyalty, Membership & Wallet · DI-382)* — scope: GST-036, WEB-043, BO-758
- **Open question.** Reusable page components per venue type are to be documented (e.g. seat-map component for stadiums/amphitheatres, park-map component for attraction venues) so one layout serves many venues with only imagery/data swapped. Documentation pending from Allam. *(open · MoM 20 Aug 2026, 4.10 CMS & White-Label; 6. Open Items · DI-395)* — scope: CMS-006, CMS-008, BO-836
- **Open question.** Open: component-count logic for the experiences/dining section on the guest-app landing page — fixed 2–3-card layout vs. a scalable N-count layout. Owner Aishwarya; to confirm with Allam's team. *(open · MoM 20 Aug 2026, 4.10 CMS & White-Label; 6. Open Items · DI-396)* — scope: GST-001
- **Open question.** Open: how the seat map builder consolidates the reference tool's separate screens (canvas, standing zone, suite, best-seats, entrances/exits) into one unified screen — Chinmay's team to confirm. *(open · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types (action) · DI-413)* — scope: BO-954, BO-955, BO-956, BO-957, BO-958, BO-960, BO-1034
- **Open question.** Open: whether donations are taxable. Allam believes they are typically not, but the system should allow enabling/disabling a tax or service fee on donations; Chinmay to confirm treatment. *(open · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies; 6. Open Items · DI-472)* — scope: BO-1190
- **Open question.** Resale lets a guest resell a ticket through a secured channel with configurable commission and eligibility (e.g. minimum time before validity date, no expired tickets). Open: TICVAI-owned secure portal vs inside each client's own B2C site/app. *(open · MoM 31 Aug 2026, 4.12 Resale Marketplace · DI-584)* — scope: ADM-279, ADM-283, GST-067
- **Open question.** Open: NFC inside a wallet pass needs Apple certification (works with any reader) vs HID SDK on the guest phone (likely HID readers only). QR-based wallet passes are straightforward. Chinmay leans to direct Apple certification unless it is a hard blocker. *(open · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-610)* — scope: BO-347, BO-348, GST-013
- **Open question.** Dynamic QR refreshes periodically to cut fraud/resale. Open: beacon-based (code hidden until the phone is near a gate beacon via Bluetooth, then refreshes ~every 2 minutes; Qossai: more secure) vs app-generated; GPS geofencing also raised. Chinmay to propose. *(open · MoM 2 Sep 2026, 4.6 Dynamic QR Code - Concept & Generation Approach · DI-630)* — scope: GST-055, BO-165, BO-168
- **Open question.** Open: how per-ride occupancy is counted (entry sensors, manual security counts, CCTV/computer vision); Allam to check with Warner Bros. World, which has a visible wait-time display. Manual count entry stays a possible source. *(open · MoM 7 Sep 2026, 4.16 Wait-Time Calculation & People-Counting Technology · DI-680)* — scope: BO-004, BO-005, EMP-032
- **Open question.** Prototype events: concert seat-map selection modelled on Coca-Cola Arena (like Platinum List); multi-day festival with day/time-slot selection; tiered show tickets (early bird, couple, group-of-4, group-of-6); all share one add-to-cart and checkout flow. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Events) · DI-685)* — scope: WEB-005, WEB-006, WEB-007, GST-049
- **Open question.** Movies: language/screen type (e.g. English, Dolby Atmos), cinema and showtime, seats, concession add-ons. Theme park: ticket-type list, guest categories (adult/child/senior/infant/people of determination with companion), per-ticket guest-name capture driven by quantity. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Movies, Theme park) · DI-686)* — scope: P01/Booking & Selection, P02/Booking & Selection, WEB-011
- **Open question.** Cabanas: category (premium, VIP, luxury, private, family, couples), date/time, guest count, amenity details. Activities: desert-safari packages (buy-one-get-one, evening, Bedouin-style), pickup point, add-ons (stroller), duration packages (2-hour/4-hour). *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Cabanas, Activities) · DI-687)* — scope: WEB-047, GST-050, GST-058, GST-074, WEB-008, GST-008
- **Open question.** Dining has two flows: book a table (date, time, group size, seating-area preference, occasion, allergy/special-request notes) and order food (delivery or pickup location, items, checkout). *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Dining) · DI-688)* — scope: GST-070, WEB-036, GST-024
- **Open question.** Resources: meeting-room booking (headcount, duration, time slot, room, add-ons tea/coffee/snacks), modelled on House of Wisdom. Merchandise: browse, cart with add/remove quantity, pickup or doorstep delivery. F&B: outlet/menu browsing; collect at counter, curbside, doorstep or priority delivery. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Resources, Merchandise, F&B) · DI-690)* — scope: WEB-048, GST-075, WEB-033, GST-026, WEB-036, GST-024
- **Open question.** Group waivers need a digital signature-capture device (stylus pad); Chinmay says a USB signature pad should integrate. Hardware reference pending from Qossai. *(open · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-756)* — scope: BO-539, BO-848
- **Open question.** Physical rental booths/stations need to appear on the live venue map; open whether the map builder already covers booth/station configuration or a dedicated addition is needed (Chinmay to check). *(open · MoM 9 Sep 2026, 4.11 Follow-Ups from Prior Sessions · DI-773)* — scope: BO-092, BO-094, BO-499
- **Open question.** Open (Chinmay): if the supervisor is unavailable, may the cashier log out with the variance logged for later review rather than being blocked? Deferred to Qossai/Allam. *(open · MoM 9 Sep 2026, 4.18 POS Prototype Review - Shift Close & Cash Variance Handling · DI-805)* — scope: POS-007
- **Open question.** Open (Qossai): many venues deliberately never show the cashier their expected sales total during the shift or at close (fraud prevention; finance's independent count catches variances). Whether the POS shows it is deferred to Qossai/Allam. *(open · MoM 9 Sep 2026, 4.18 POS Prototype Review - Shift Close & Cash Variance Handling · DI-806)* — scope: POS-007, POS-008, POS-025
- **Open question.** Post-go-live, only configuration changes tested in staging (e.g. a new product or package) should be promoted to production, never transactional data; feasibility pending the CI/CD engineer. *(open · MoM 10 Sep 2026, 4.13 Pre-Production to Production Configuration Promotion · DI-834)* — scope: ADM-023
- **Open question.** Open (Chinmay): should server/infrastructure monitoring and management be a dedicated module inside the TICVAI platform, or stay in Softlabs' own tooling (e.g. Terraform) outside the product? Input from Tejesh pending. *(open · MoM 10 Sep 2026, 4.18 Other Discussion · DI-841)* — scope: P09/Infrastructure & Resilience
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)* — scope: P01, P02, CMS-005, CMS-101
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)* — scope: P01, P02, CMS-005, CMS-006
- **Open question.** Allam expects a large volume of feedback on the guest web/mobile prototype; detailed feedback goes to a separate dedicated session with Qossai and Allam. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-888)* — scope: P01, P02
- **Open question.** Web "at the venue" section gives guests without the app on-site features in the browser: interactive maps, wait times, 3D venue maps, food ordering, virtual queue status, parking, basic directions (main gate, first aid). In progress; client review pending. *(open · MoM 15 Sep 2026, 4.2 Guest Web App - 3D Stadium Seat View & At-Venue Wayfinding · DI-891)* — scope: P01/In-venue Services, WEB-039, WEB-036, WEB-040, WEB-041
- **Open question.** Open: can health metrics such as handheld battery be read via the manufacturer's SDK in-app rather than by physical inspection? Depends on each vendor SDK; to confirm during integration. *(open · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-900)* — scope: BO-128, BO-203
- **Open question.** Open (Allam): physical tamper detection - lock out communication if a device is opened, as bank payment terminals do - worth evaluating per device type; not a requirement for every device. *(open · MoM 15 Sep 2026, 4.8 Device Security & Governance · DI-904)* — scope: BO-203
- **Open question.** Open: should AI monitoring live in one centralised AI command dashboard or be distributed as widgets in each functional module's own dashboard? Allam: Softlabs' call; the current proposal is illustrative and Softlabs may propose a better structure. *(open · MoM 18 Sep 2026, 4.4 AI Governance — Risk, Compliance & Continuous Monitoring · DI-936)* — scope: P09/Platform, P08
- **Open question.** Qossai: a guest-checkout customer may not have opted into marketing the way a registered customer accepting full terms has; how marketing consent is captured at guest checkout is unresolved. *(open · MoM 18 Sep 2026, 4.8 Guest Checkout & Profile Deduplication — Extended Discussion · DI-940)* — scope: WEB-011, GST-041
- **Open question.** Proposed (Chinmay), not finalised: each pre-configured agent carries a complexity/fitness score; when a client switches models, an assessment flags whether the new model is under- or over-powered for that agent and recommends an adjustment. Exact end-user control over model switching is still open. *(open · MoM 21 Sep 2026, 4.10 Core AI Platform — Multi-Provider AI Model Strategy · DI-967)* — scope: ADM-037
- **Open question.** Qossai proposes a POS-style interface for high-volume resellers (hotels, travel agents) instead of a B2C-style site with login: assigned tickets and partner prices after login, optional cash drawer, sent-ticket history and resend, balance view. Chinmay wireframes both options; decide after review. *(open · MoM 29 Sep 2026, 3. B2B / reseller portal · DI-1023)* — scope: P10
- **Open question.** Real venue photos, clips and logos are still to come from the client; designs use stand-ins. Slots expected: a photo per ticket card and clip per card, a square shot per extra/shop item, one landscape poster per venue for the single-event page. Photos ≥1600 px, clips mp4 6–12 s, no audio. *(open · design review 29 Sep 2026, Asset list — TICVAI Guest Booking · DI-1080)* — scope: P01, P02
- **Open question.** Open: biometric data for children. Adults with consent is compliant; for minors, either exclude biometric storage entirely or allow it with a parent/guardian-signed consent form. TICVAI to answer by email. *(open · MoM 30 Sep 2026, 4.3 Open Questions Flagged by Chinmay — Invoicing/Taxation & Biometric Consent for Minors · DI-1085)* — scope: GST-069
- **Open question.** How many supervisors come free per group (per N guests), and is it per group ticket? Default built: supervisors are a separate, free guest type, up to 1 per 10 guests, counted on the group request. *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Supervisors · DI-1114)* — scope: WEB-031, GST-072
- **Open question.** Do Tour operator and Community become their own group types or map to general? Default built: School, Corporate, Tour operator and Community shown as their own group types (platform also has general and party). *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Group types · DI-1115)* — scope: WEB-031, GST-072, BO-1024
- **Open question.** Each group ticket card shows a minimum group size; is it set per group ticket, and what values? Default built: each group ticket carries its own minimum, default 10. *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Minimum group size · DI-1116)* — scope: WEB-031, GST-072
- **Open question.** Are water-park groups booked into a session (the build picks a session first)? Default built: group requests take a date and, for session-based products, a session. *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Water-park groups by session · DI-1117)* — scope: WEB-031, GST-072
- **Open question.** Is the swim vest an add-on product, and is the splash-and-river pass a separate product offered only to non-swimmers? Default built: the swim answer filters products (as Help me choose); the vest is an add-on; the splash-and-river pass is its own product. *(open · Decisions Register 1 Oct 2026, Questions for the client — Guest safety / Swim ability · DI-1118)* — scope: WEB-005, WEB-006, WEB-008, GST-007, GST-008
- **Open question.** Should each popular-route card's starting fare, featured order and image or badge be set per route in the back office? Default built: routes carry a featured order and an image; the starting fare is computed from the lowest fare. *(open · Decisions Register 1 Oct 2026, Questions for the client — Transport / Popular routes card · DI-1119)* — scope: WEB-049, GST-076, BO-1184

## Global: every app

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

## P01 Guest Web

**Platform-wide**

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

**Account & Self-Service**

- Decision: profiles are never merged automatically. Likely duplicates are notified to the customer (push or e-mail) and merge only on the customer's confirmation; an admin review queue tracks flagged duplicates independently of the customer's response. *(agreed · MoM 20 Aug 2026, 4.2 Duplicate Detection; 5. Key Decisions · DI-377)*

**Booking & Selection**

- The prototype validated five booking-flow types (dated, multi-park, combo, annual pass, membership) and their skeleton screens; these flows are the basis for the real white-label builder. *(agreed · MoM 24 Sep 2026, 4.8 Guest Web App CMS Prototype — Feedback on Maturity & Scope Expectations · DI-989)*
- Each ticket type gets its own flow: open-dated (no calendar step, straight to guest category/quantity, valid e.g. 30-60 days), dated (date, then product), dated-with-time (date, time, product) and seated (date, time, seat selection). *(client request · MoM 18 Sep 2026, 4.13 Guest Website UX Review — Ticket Type Flows & Seat Map Selection · DI-948)*
- **Open question.** Movies: language/screen type (e.g. English, Dolby Atmos), cinema and showtime, seats, concession add-ons. Theme park: ticket-type list, guest categories (adult/child/senior/infant/people of determination with companion), per-ticket guest-name capture driven by quantity. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Movies, Theme park) · DI-686)*
- Decision: the B2C checkout shows a clear, visible step indicator — Ticket Selection → Add-ons → My Cart → Checkout. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-426)*
- Reference checkouts: Six Flags-style (product → quantity/name capture → cart summary → login/guest checkout with dual OTP validation) and Platinum List (event → date → colour-coded interactive seat map → seats → one-page checkout via Quick Order/Apple/Google, as few as four clicks, optional post-purchase profile prompt). *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-398)*
- **Open question.** Two selection patterns: (a) event, date, time, see availability, then product; (b) product, quantity, date, then only time slots with enough capacity. How many customization scenarios to support needs deeper UI exploration. *(open · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-118)*
- Navigation depends on ticket type: admission has no date/time and goes straight to quantity/cart; dated asks date only; timed asks date then time; seated asks date, then time, then seat. *(agreed · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-116)*

**Cart & Checkout**

- Decision: the B2C checkout shows a clear, visible step indicator — Ticket Selection → Add-ons → My Cart → Checkout. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-426)*
- Reference checkouts: Six Flags-style (product → quantity/name capture → cart summary → login/guest checkout with dual OTP validation) and Platinum List (event → date → colour-coded interactive seat map → seats → one-page checkout via Quick Order/Apple/Google, as few as four clicks, optional post-purchase profile prompt). *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-398)*

**Discovery & Browse**

- "Help me choose" (experience builder) is not a consent step: its questions (yes/no, age, certified or not, etc.) filter the catalogue so only suitable products are shown (Deep Dive Dubai reference). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W4 Help me choose · DI-1005)*

**In-venue Services**

- **Open question.** Web "at the venue" section gives guests without the app on-site features in the browser: interactive maps, wait times, 3D venue maps, food ordering, virtual queue status, parking, basic directions (main gate, first aid). In progress; client review pending. *(open · MoM 15 Sep 2026, 4.2 Guest Web App - 3D Stadium Seat View & At-Venue Wayfinding · DI-891)*

**Screen by screen**

`WEB-001` Home / Landing

- Existing booking settings stay: step indicator, extras step, seat picker, map view, quantities on add-ons (−/+ stepper, price multiplies), embed mode, hero banner, search in banner, single-event page. Defaults: search in banner off, seat picker = bowl. *(agreed · design review 29 Sep 2026, CFG-6 · Step indicator; Extras step; Seat picker; Map view; Quantities on add-ons; Embed mode; Hero banner; Search in banner; Single-event page · DI-1070)*
- A UI preset (L1–L6, or Custom) picks a bundle of booking-UI settings per venue type. *(agreed · design review 29 Sep 2026, CFG-1 · Preset (UI preset L1-L6, Custom) · DI-1065)*
- Multi-location attractions: the guest picks a location first (e.g. Al Barsha, Mirdif, Yas Island, Sharjah); a "Booking at" bar on later booking steps has Change location. On a switch, times and prices refresh and the selection is cleared unless the products share a family. Setting "Location switcher". *(agreed · rev 3 design review 29 Sep 2026, REV3-18 · 18. One tenant with an attraction in several locations; change location · DI-1058)*
- The date list in the event banner (for multi-date events) is a setting, "Dates in event banner", off by default. The date picker always sits at the top of the booking step. *(agreed · design review 29 Sep 2026, Settings 19. Why is there a date selection in the header? · DI-1033)*
- The B2C home page lists the ticket categories directly; clicking one opens its counters on the same screen. *(client request · design review 23 Sep 2026, Tickets 8. Show the single day ticket category on the B2C home page · DI-977)*
- The hero banner and marketing layer (images, video, search, browse-by-venue, venue info) is optional and toggled in the white-label builder: on for clients without their own marketing site (Qossai: roughly 30%), off for a lean direct-to-ticket flow. *(agreed · MoM 18 Sep 2026, 4.11 Guest Website UX Review — Page Structure & Hero Banner Flexibility · DI-945)*
- Six Flags reference for the B2C redesign (Qossai): hero-banner product video. *(client request · MoM 8 Sep 2026, 4.20 Planning & Next Steps · DI-738)*
- Ticket listings are data-driven: creating a new ticket automatically surfaces it on the relevant site according to its category configuration. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-109)*

`WEB-002` Event & Attraction Listing

- Category tiles (e.g. Permanent exhibition, Temporary exhibitions, Guided tours, Courses & workshops), then that category's tickets with Adult / Child / Student counters. Setting "Ticket categories": Category → subcategory (default) or Flat list (all tickets under category headings). *(agreed · rev 3 design review 29 Sep 2026, REV3-16 · 16. Choose category, then subcategory, configurable in the CMS · DI-1056)*
- Card layout is a choice, not free text: Stacked rows (default) · Split rows · Cards across · Poster cards. Card size: Compact (default) · Standard · Large · Extra large. Density: Compact (default) · Standard · Roomy. *(agreed · design review 29 Sep 2026, 6. Booking-flow configuration (CMS-016): card-layout options · DI-1040)*
- Clicking a ticket opens the Adult / Child / Senior / Infant counters in a side panel on the same listing or details screen (no separate "Select Tickets" step); the panel is open by default on the listing and Book goes straight into the booking. *(agreed · design review 29 Sep 2026, Tickets 5. Clicking Dated Day Pass should show the tickets on the same screen · DI-1027)*
- Read more opens with the ticket's video or photo, and every ticket in a listing has its own photo (product media: images and videos, one primary). *(agreed · design review 29 Sep 2026, Tickets 4. Video or image should show · DI-1026)*
- CMS option to list a product (e.g. training courses) with full details but no Book button; instead show "Contact sales to book" with contact details. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W3 View-only products · DI-1004)*
- Experience venues list each experience directly (e.g. author talk, calligraphy workshop, story hour, rooftop reading night), each with its own date, time and tickets; no category step. *(client request · rev 3 design review 25 Sep 2026, 12. Experience flow: show the product directly, not the ticket category · DI-999)*
- Show the ticket categories (e.g. Single day, Two-day flexible, UAE resident) directly; no intermediate "Dated day pass" step. *(client request · design review 23 Sep 2026, Tickets 7. Show the ticket category directly instead of Dated Pass -> Single Day Pass · DI-976)*
- Allam's UX benchmark (Little Explorer, Dubai): multi-location selector, a horizontal near-term date picker with full-calendar fallback, and tabbed browsing (passes / workshops / packages) on one page rather than multiple screens. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-585)*
- Products are grouped into categories for the tenant website (e.g. a diving operator's scuba diving, free diving, snorkelling, each listing its packages); package title, description, terms, age limits and images come from back-office fields and sync to the live site; choosing a package goes to checkout on the TICVAI booking platform. *(agreed · MoM 7 Aug 2026, 9. Statistical Groups & Website Content Integration · DI-161)*
- Ticket listings are data-driven: creating a new ticket automatically surfaces it on the relevant site according to its category configuration. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-109)*

`WEB-004` Attraction Details

- Qossai: ride/attraction detail pages play the video directly, with no loading screen in front of it; an info button reveals ride details and plays the video. Chinmay agreed to remove the loader. *(agreed · MoM 30 Sep 2026, 4.8 Mobile App — In-Ride Video/Info & In-Park Navigation · DI-1101)*
- The date list in the event banner (for multi-date events) is a setting, "Dates in event banner", off by default. The date picker always sits at the top of the booking step. *(agreed · design review 29 Sep 2026, Settings 19. Why is there a date selection in the header? · DI-1033)*
- Clicking a ticket opens the Adult / Child / Senior / Infant counters in a side panel on the same listing or details screen (no separate "Select Tickets" step); the panel is open by default on the listing and Book goes straight into the booking. *(agreed · design review 29 Sep 2026, Tickets 5. Clicking Dated Day Pass should show the tickets on the same screen · DI-1027)*
- Read more opens with the ticket's video or photo, and every ticket in a listing has its own photo (product media: images and videos, one primary). *(agreed · design review 29 Sep 2026, Tickets 4. Video or image should show · DI-1026)*
- Ticket cards, Read more and the listing side panel show tags (e.g. "2 Hours", "Min 1.10 m", "Free adult entry", "Valid 90 days", "Emirates ID"), each with a kind icon (clock, height, free, calendar, id), max 6. Venue-set tags win, else derived from duration, validity, height rule. Setting "Tags on tickets", default on. *(agreed · design review 29 Sep 2026, Tickets 3. 'Read more' should carry tags customisable per ticket type · DI-1025)*
- CMS option to list a product (e.g. training courses) with full details but no Book button; instead show "Contact sales to book" with contact details. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W3 View-only products · DI-1004)*
- Show the ticket categories (e.g. Single day, Two-day flexible, UAE resident) directly; no intermediate "Dated day pass" step. *(client request · design review 23 Sep 2026, Tickets 7. Show the ticket category directly instead of Dated Pass -> Single Day Pass · DI-976)*
- Single-event mode page: banner or video hero, a brief description, and a date strip of the next seven days with a calendar for later dates. *(agreed · MoM 18 Sep 2026, M18-13 · DI-953)*
- A venue selling a single event gets a dedicated page with a banner/video and brief description, showing only the near-term available dates (e.g. next 7 days) by default. *(client request · MoM 18 Sep 2026, 4.13 Guest Website UX Review — Ticket Type Flows & Seat Map Selection · DI-949)*
- Guest date picking shows a strip of the next seven days (venue setting dateStripDays, default 7, range 3-31) with a calendar icon that opens the full month for later dates. *(agreed · MoM 17 Sep 2026, M17-08 · DI-920)*
- Qossai and Allam: product pages should include short video content (e.g. a 10-15 second clip), not only static images, to give a sense of the actual experience (e.g. a ride) before booking. *(agreed · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-917)*
- Allam (ref. "Little Explorer"): show only a short near-term availability window by default (e.g. next 7 days) with a calendar icon that expands to a full calendar for later dates, instead of the flat 15-day range shown. *(agreed · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-915)*
- Six Flags reference for the B2C redesign (Qossai): hero-banner product video. *(client request · MoM 8 Sep 2026, 4.20 Planning & Next Steps · DI-738)*
- Allam's UX benchmark (Little Explorer, Dubai): multi-location selector, a horizontal near-term date picker with full-calendar fallback, and tabbed browsing (passes / workshops / packages) on one page rather than multiple screens. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-585)*
- Product cards/pages carry short descriptions with an expandable "view more details" control and a configurable hero image or video per product. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-425)*
- Platinum List reference: event page with short video + image + description → select tickets → calendar collapsed to a week view, expandable to full month → time-slot selection. *(client request · MoM 21 Aug 2026, 4.1 Reference Walkthrough — Platinum List Seat Selection & Checkout Journey · DI-408)*
- Products are grouped into categories for the tenant website (e.g. a diving operator's scuba diving, free diving, snorkelling, each listing its packages); package title, description, terms, age limits and images come from back-office fields and sync to the live site; choosing a package goes to checkout on the TICVAI booking platform. *(agreed · MoM 7 Aug 2026, 9. Statistical Groups & Website Content Integration · DI-161)*

`WEB-005` Ticket Type Selection

- **Open question.** Is the swim vest an add-on product, and is the splash-and-river pass a separate product offered only to non-swimmers? Default built: the swim answer filters products (as Help me choose); the vest is an add-on; the splash-and-river pass is its own product. *(open · Decisions Register 1 Oct 2026, Questions for the client — Guest safety / Swim ability · DI-1118)*
- The water-park swim answer changes the offer: All of us = full ride list at standard prices; Some of us = ride notes change and a "Swim vests needed" counter appears; None of us = tickets switch to a cheaper splash and river pass, slides removed from ride notes. The swim pop-up is not shown where the question is on the page. *(client request · design review 30 Sep 2026, 4. Swim ability and height gate: the answer changed nothing · DI-1108)*
- Picking a surf session adds nothing to the cart. Then "Tickets for Intermediate surf · 19:30" shows Surfer (session price), Junior surfer 10–15 and Spectator (AED 35); items reach the cart only when a quantity is set. Before a session: "Choose a session above to see its tickets and prices." *(client request · design review 30 Sep 2026, 3. Surfing session added to the cart straight away · DI-1107)*
- Guest counters take their price from the chosen park ticket and produce one line, e.g. "2 park ticket · Adult × 3 = AED 1,425" (no separate Adult × 3 line). Child and senior prices scale from the chosen ticket; infants free. *(client request · design review 30 Sep 2026, 2. Multi-park ticket adds an extra adult line · DI-1106)*
- On a guest's first booking visit, a four-step coach-mark tour highlights date, time, tickets and basket, with Back, Next / Done and End tour; a "Quick tour" button on the booking page replays it. Setting "Quick tour", default off; first-visit flag kept on the device only. *(agreed · rev 3 design review 29 Sep 2026, REV3-20 · 20. Enable or disable a Quick Tour that describes the customer journey · DI-1060)*
- Multi-location attractions: the guest picks a location first (e.g. Al Barsha, Mirdif, Yas Island, Sharjah); a "Booking at" bar on later booking steps has Change location. On a switch, times and prices refresh and the selection is cleared unless the products share a family. Setting "Location switcher". *(agreed · rev 3 design review 29 Sep 2026, REV3-18 · 18. One tenant with an attraction in several locations; change location · DI-1058)*
- Category tiles (e.g. Permanent exhibition, Temporary exhibitions, Guided tours, Courses & workshops), then that category's tickets with Adult / Child / Student counters. Setting "Ticket categories": Category → subcategory (default) or Flat list (all tickets under category headings). *(agreed · rev 3 design review 29 Sep 2026, REV3-16 · 16. Choose category, then subcategory, configurable in the CMS · DI-1056)*
- Cart & summary options: sidebar fixed right, sidebar left, slide-in right, slide-up bottom, floating cart icon (round basket button with item count opening the slide-in basket), single column. In Arabic the basket stays on the right by default (client confirmed); "Cart side in Arabic" can mirror to left. *(agreed · rev 3 design review 29 Sep 2026, REV3-10 · 10. Cart display: fixed on right, slide bar, icon, bottom; right for Arabic · DI-1051)*
- Dated flows reveal in order: date, then time (hidden until a date is picked), then tickets (hidden until a time is picked), with a hint in place telling the guest what to pick next; Continue off until both chosen. Setting "Performance reveal": Date → time → ticket (default) or All at once. *(agreed · rev 3 design review 29 Sep 2026, REV3-2 · 2. Step 1 date, step 2 time (only after the date), step 3 ticket · DI-1042)*
- Card layout is a choice, not free text: Stacked rows (default) · Split rows · Cards across · Poster cards. Card size: Compact (default) · Standard · Large · Extra large. Density: Compact (default) · Standard · Roomy. *(agreed · design review 29 Sep 2026, 6. Booking-flow configuration (CMS-016): card-layout options · DI-1040)*
- Each Adult / Child / Senior / Infant row has an (i) button showing who the ticket is for and what it includes (up to 300 characters). Setting "Extra info on cards", default on. *(agreed · design review 29 Sep 2026, Tickets 6. Extra information for each ticket in the ticket section · DI-1028)*
- Clicking a ticket opens the Adult / Child / Senior / Infant counters in a side panel on the same listing or details screen (no separate "Select Tickets" step); the panel is open by default on the listing and Book goes straight into the booking. *(agreed · design review 29 Sep 2026, Tickets 5. Clicking Dated Day Pass should show the tickets on the same screen · DI-1027)*
- Read more opens with the ticket's video or photo, and every ticket in a listing has its own photo (product media: images and videos, one primary). *(agreed · design review 29 Sep 2026, Tickets 4. Video or image should show · DI-1026)*
- Ticket cards, Read more and the listing side panel show tags (e.g. "2 Hours", "Min 1.10 m", "Free adult entry", "Valid 90 days", "Emirates ID"), each with a kind icon (clock, height, free, calendar, id), max 6. Venue-set tags win, else derived from duration, validity, height rule. Setting "Tags on tickets", default on. *(agreed · design review 29 Sep 2026, Tickets 3. 'Read more' should carry tags customisable per ticket type · DI-1025)*
- Museum workshops: after Help me choose, the guest selects the workshop first, then date/time; only relevant products are shown. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W8 Workshops (museum) · DI-1010)*
- Surf sessions follow the time-selection pattern: products (beginner, intermediate...) appear only after a time slot is chosen. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W5 Surf sessions · DI-1007)*
- CMS option to list a product (e.g. training courses) with full details but no Book button; instead show "Contact sales to book" with contact details. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W3 View-only products · DI-1004)*
- Experience venues list each experience directly (e.g. author talk, calligraphy workshop, story hour, rooftop reading night), each with its own date, time and tickets; no category step. *(client request · rev 3 design review 25 Sep 2026, 12. Experience flow: show the product directly, not the ticket category · DI-999)*
- With the "Slide in right" cart setting, the summary is a tab on the right edge that slides in from the right (not a bar at the bottom). *(client request · design review 23 Sep 2026, Cart 13. Cart summary: 'Slide in right' shows at the bottom · DI-981)*
- Season and membership packages show a quantity stepper once selected. *(client request · design review 23 Sep 2026, Cart 12. No quantity field for the selected ticket · DI-980)*
- Add-ons appear only on the Add-ons / Extras step, never in the ticket panels. Each add-on appears once (no duplicates such as 'Large locker' on two steps). *(client request · design review 23 Sep 2026, Cart 11. Show add-ons only on the Add-ons / Extras page · DI-979)*
- **Open question.** Prototype events: concert seat-map selection modelled on Coca-Cola Arena (like Platinum List); multi-day festival with day/time-slot selection; tiered show tickets (early bird, couple, group-of-4, group-of-6); all share one add-to-cart and checkout flow. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Events) · DI-685)*
- Reference details: sibling/multi-buy discount shown with a struck-through original price; workshop add-ons inline with theme/cuisine sub-selection feeding time-slot availability; a package builder for bundled experiences. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-586)*
- Decision (Qossai, Ski Dubai): instructor choice is a per-ticket-type setting — private-session products may let the guest pick a specific instructor; group-session products auto-assign without showing a choice. Private and group are separate, separately priced products (a private request on a group instructor is its own product). *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-504)*
- Quantity/purchase limits can be set per order, per guest, per account category and per sales channel (e.g. maximum 6 tickets per transaction). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-464)*
- Packages bundle any combination of ticket-type components with package-level pricing (e.g. admission + F&B item + retail item, or admission + show); F&B or retail is not required. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-435)*
- Decision: ticket types are browsed in-page, not across multiple pages; "View all ticket types" expands additional categories in place. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-427)*
- Product cards/pages carry short descriptions with an expandable "view more details" control and a configurable hero image or video per product. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-425)*
- Minimum/maximum sellable quantity per customer (e.g. a promotional bundle requiring at least two) must be enforced at selection. *(agreed · MoM 7 Aug 2026, 16. Entitlement Components: Re-entry, Expiration & Sale Restrictions · DI-172)*
- Some clients (e.g. museums with 5-6 standard configurations) start by asking the number of guests, which narrows the calendar to dates/times with sufficient availability. *(client request · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-117)*

`WEB-006` Date & Performance Selection

- **Open question.** Is the swim vest an add-on product, and is the splash-and-river pass a separate product offered only to non-swimmers? Default built: the swim answer filters products (as Help me choose); the vest is an add-on; the splash-and-river pass is its own product. *(open · Decisions Register 1 Oct 2026, Questions for the client — Guest safety / Swim ability · DI-1118)*
- The water-park swim answer changes the offer: All of us = full ride list at standard prices; Some of us = ride notes change and a "Swim vests needed" counter appears; None of us = tickets switch to a cheaper splash and river pass, slides removed from ride notes. The swim pop-up is not shown where the question is on the page. *(client request · design review 30 Sep 2026, 4. Swim ability and height gate: the answer changed nothing · DI-1108)*
- Picking a surf session adds nothing to the cart. Then "Tickets for Intermediate surf · 19:30" shows Surfer (session price), Junior surfer 10–15 and Spectator (AED 35); items reach the cart only when a quantity is set. Before a session: "Choose a session above to see its tickets and prices." *(client request · design review 30 Sep 2026, 3. Surfing session added to the cart straight away · DI-1107)*
- Swim ability is a consent question a venue attaches to a product or flow (e.g. "Are you able to swim?", "Do you hold a scuba certification?", "I accept the risk"), each with its own text and per-person or once-per- booking setting. Shown as a pop-up in the venue's theme after session/date; answers recorded. *(agreed · rev 3 design review 29 Sep 2026, REV3-26 · Built to match your examples: Swim question (water park) · DI-1062)*
- On a guest's first booking visit, a four-step coach-mark tour highlights date, time, tickets and basket, with Back, Next / Done and End tour; a "Quick tour" button on the booking page replays it. Setting "Quick tour", default off; first-visit flag kept on the device only. *(agreed · rev 3 design review 29 Sep 2026, REV3-20 · 20. Enable or disable a Quick Tour that describes the customer journey · DI-1060)*
- Multi-location attractions: the guest picks a location first (e.g. Al Barsha, Mirdif, Yas Island, Sharjah); a "Booking at" bar on later booking steps has Change location. On a switch, times and prices refresh and the selection is cleared unless the products share a family. Setting "Location switcher". *(agreed · rev 3 design review 29 Sep 2026, REV3-18 · 18. One tenant with an attraction in several locations; change location · DI-1058)*
- The guest picks a tour language (e.g. English, العربية, Français, Deutsch, 中文, Русский) and only tours in that language are listed. Cinema performances show language and format (2D/3D/subtitled) to pick from. *(agreed · rev 3 design review 29 Sep 2026, REV3-17 · 17. Guided tour times based on the tour language · DI-1057)*
- Cart & summary options: sidebar fixed right, sidebar left, slide-in right, slide-up bottom, floating cart icon (round basket button with item count opening the slide-in basket), single column. In Arabic the basket stays on the right by default (client confirmed); "Cart side in Arabic" can mirror to left. *(agreed · rev 3 design review 29 Sep 2026, REV3-10 · 10. Cart display: fixed on right, slide bar, icon, bottom; right for Arabic · DI-1051)*
- Theatre has its own auditorium seat map: stage (or screen for cinema) at front, Stalls/Circle/Balcony with curved rows, aisles and Premium/Standard/Economy pricing. Date, time, show (plus language & format for cinema) and the seat map sit on one page. Seats per guest booking default 10 (venue setting); basket lists each seat. *(agreed · rev 3 design review 29 Sep 2026, REV3-7 · 7. Theatre flow should be similar to the stadium flow · DI-1047)*
- A time bar above the seat map shows the chosen performance, lets the guest switch show and has Change date; switching releases held seats. Setting "Time bar above seat map", default on. On the selection step, time sits directly under the date, above language & format and tickets. *(agreed · rev 3 design review 29 Sep 2026, REV3-6 · 6. Time selection on top, configurable · DI-1046)*
- Seated events with one on-sale performance go straight to the seat map (Flow 1). Otherwise date and time come first (Flow 2), either as an inline step (timed-ticket style, default) or as a pop-up dialog over the seat map. Setting "Date & time on seat events". *(agreed · rev 3 design review 29 Sep 2026, REV3-4 · 4. Flow 1 (fixed date and time) and Flow 2 (select date, then time, then seat map) · DI-1044)*
- Dated flows reveal in order: date, then time (hidden until a date is picked), then tickets (hidden until a time is picked), with a hint in place telling the guest what to pick next; Continue off until both chosen. Setting "Performance reveal": Date → time → ticket (default) or All at once. *(agreed · rev 3 design review 29 Sep 2026, REV3-2 · 2. Step 1 date, step 2 time (only after the date), step 3 ticket · DI-1042)*
- More than eight times show as compact time tiles, paged with Earlier / Later (Times per page 8/12/24/all, default 24), with day-part chips (All, Morning, Afternoon, Evening) showing counts (filter on by default). Day-part boundaries are venue settings, default before 12:00 / 12:00–17:00 / from 17:00. *(agreed · rev 3 design review 29 Sep 2026, REV3-1 · 1. Many performances should resize and page; filter by morning, afternoon, evening · DI-1041)*
- On leaving selection (rides, water slides, kids club), each person declares an age band and height band; toggles only where needed (confident swimmer; guardian signature for 12–15). Per-person "Can't take part: too short, needs an adult" with Remove this guest / Choose another activity; Continue locked until all qualify. *(agreed · design review 29 Sep 2026, 3. Height and age check (WEB-006) · DI-1037)*
- Guided tours/sessions confirmed: date, then language, then time slot. Sessions come from configuration; the slot grid reflows when there are many slots. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W11 Guided tours / sessions · DI-1013)*
- Museum workshops: after Help me choose, the guest selects the workshop first, then date/time; only relevant products are shown. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W8 Workshops (museum) · DI-1010)*
- Surf sessions follow the time-selection pattern: products (beginner, intermediate...) appear only after a time slot is chosen. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W5 Surf sessions · DI-1007)*
- With the "Slide in right" cart setting, the summary is a tab on the right edge that slides in from the right (not a bar at the bottom). *(client request · design review 23 Sep 2026, Cart 13. Cart summary: 'Slide in right' shows at the bottom · DI-981)*
- A venue selling a single event gets a dedicated page with a banner/video and brief description, showing only the near-term available dates (e.g. next 7 days) by default. *(client request · MoM 18 Sep 2026, 4.13 Guest Website UX Review — Ticket Type Flows & Seat Map Selection · DI-949)*
- Guest date picking shows a strip of the next seven days (venue setting dateStripDays, default 7, range 3-31) with a calendar icon that opens the full month for later dates. *(agreed · MoM 17 Sep 2026, M17-08 · DI-920)*
- Allam (ref. "Little Explorer"): show only a short near-term availability window by default (e.g. next 7 days) with a calendar icon that expands to a full calendar for later dates, instead of the flat 15-day range shown. *(agreed · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-915)*
- **Open question.** Prototype events: concert seat-map selection modelled on Coca-Cola Arena (like Platinum List); multi-day festival with day/time-slot selection; tiered show tickets (early bird, couple, group-of-4, group-of-6); all share one add-to-cart and checkout flow. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Events) · DI-685)*
- Date-change flow detects conflicts across an existing multi-ticket cart and lets the guest shift the whole booking to a new date in one action. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-587)*
- Allam's UX benchmark (Little Explorer, Dubai): multi-location selector, a horizontal near-term date picker with full-calendar fallback, and tabbed browsing (passes / workshops / packages) on one page rather than multiple screens. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-585)*
- Start/stop-sell per channel: e.g. a distant desert safari allows no same-day online booking (next day minimum), while onsite stays open to sell-out or a cutoff (e.g. 15 minutes before a timed show). Guest date/time pickers must reflect the channel's window. *(client request · MoM 31 Aug 2026, 4.11 Sales schedule & validity · DI-583)*
- Weekday/calendar rules give different validity and pricing to weekday-only vs. all-days products (e.g. Global Village). Blockout dates exclude some ticket types (e.g. memberships) on public holidays/special days, requiring a separate ticket for those dates. *(client request · MoM 25 Aug 2026, 4.5 Validity Management & Expiry Rules · DI-452)*
- Camping/lesson-based tickets: when buying a multi-lesson package (e.g. ski or snowboard lessons on a regular schedule) the guest selects the specific class dates/performances. *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-449)*
- Time-slot (performance) tickets configure early/late entry and an entry window (e.g. from 30 minutes before start until a cut-off). Multi-day tickets are consecutive-day or flexible within a range (e.g. any 3 days within a month). *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-447)*
- Kidiya family-pass example showed a dynamic-pricing calendar applied at ticket-type level (prices shown on the calendar per date). *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-430)*
- Platinum List reference: event page with short video + image + description → select tickets → calendar collapsed to a week view, expandable to full month → time-slot selection. *(client request · MoM 21 Aug 2026, 4.1 Reference Walkthrough — Platinum List Seat Selection & Checkout Journey · DI-408)*
- Some clients (e.g. museums with 5-6 standard configurations) start by asking the number of guests, which narrows the calendar to dates/times with sufficient availability. *(client request · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-117)*
- Seat assignment flow is "select time, then select seat", with the two steps on different screens. *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-057)*

`WEB-007` Interactive Seat Selection

- Existing booking settings stay: step indicator, extras step, seat picker, map view, quantities on add-ons (−/+ stepper, price multiplies), embed mode, hero banner, search in banner, single-event page. Defaults: search in banner off, seat picker = bowl. *(agreed · design review 29 Sep 2026, CFG-6 · Step indicator; Extras step; Seat picker; Map view; Quantities on add-ons; Embed mode; Hero banner; Search in banner; Single-event page · DI-1070)*
- Theatre has its own auditorium seat map: stage (or screen for cinema) at front, Stalls/Circle/Balcony with curved rows, aisles and Premium/Standard/Economy pricing. Date, time, show (plus language & format for cinema) and the seat map sit on one page. Seats per guest booking default 10 (venue setting); basket lists each seat. *(agreed · rev 3 design review 29 Sep 2026, REV3-7 · 7. Theatre flow should be similar to the stadium flow · DI-1047)*
- A time bar above the seat map shows the chosen performance, lets the guest switch show and has Change date; switching releases held seats. Setting "Time bar above seat map", default on. On the selection step, time sits directly under the date, above language & format and tickets. *(agreed · rev 3 design review 29 Sep 2026, REV3-6 · 6. Time selection on top, configurable · DI-1046)*
- The 'view from your seat' box can sit Bottom (default), Right, Left or Top of the seat map (web only); on narrow screens and mobile it is always below the map. Setting "Seat view box". *(agreed · rev 3 design review 29 Sep 2026, REV3-5 · 5. CMS option to show the seat view right, left, top or bottom · DI-1045)*
- Seated events with one on-sale performance go straight to the seat map (Flow 1). Otherwise date and time come first (Flow 2), either as an inline step (timed-ticket style, default) or as a pop-up dialog over the seat map. Setting "Date & time on seat events". *(agreed · rev 3 design review 29 Sep 2026, REV3-4 · 4. Flow 1 (fixed date and time) and Flow 2 (select date, then time, then seat map) · DI-1044)*
- Picking a section shows the view from that section (concert mode shows the stage; closer sections see a larger stage with fewer rows in front). Use the venue's photo for the section when supplied, otherwise render the view from the imported 3D geometry. *(agreed · design review 29 Sep 2026, Seat map 14. Show the view to the stage in the small window · DI-1030)*
- Stadium/theatre seat maps show sections first with colour and price; zooming into a section shows its seats. Pinch-out / scroll-out returns to the full map so other sections can be compared. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W2 Seat maps · DI-1003)*
- Zoomed in, every nearby section shows its seats as equal-size dots: available in the section's price colour, taken in grey, picked seat highlighted. Zoom in, Zoom out and "Whole map" buttons sit under the map. *(client request · design review 23 Sep 2026, Seat map 17. When zoomed in, show the available seats across the map · DI-983)*
- Each picked seat goes into the cart with section, row, seat and price (e.g. "Section 101 · Row A, Seat 4 · AED 165"); tapping the seat again removes it. *(client request · design review 23 Sep 2026, Seat map 15. Selected seats should be added to the cart · DI-982)*
- On 3D venue maps, selecting a section takes the guest straight into that section's seats in one motion by zooming in, not via a separate pop-up, modal or new window. *(agreed · MoM 18 Sep 2026, 4.13 Guest Website UX Review — Ticket Type Flows & Seat Map Selection · DI-950)*
- Allam (ref. Platinum List Dubai): replace the tier-name list (VIP box, lower tier, upper tier) with a full colour-coded visual map of the venue upfront, each zone coloured with its price visible (e.g. gold near the stage, higher price; blue further away, lower), before drilling into the section's 2D/3D seat view. *(agreed · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-916)*
- 3D seat view: a guest booking a seated event (e.g. stadium concert) can preview the view from the selected section in 3D - built in (Three.js in React), no third-party integration; the standard 2D seat map remains the simpler option. *(agreed · MoM 15 Sep 2026, 4.2 Guest Web App - 3D Stadium Seat View & At-Venue Wayfinding · DI-889)*
- **Open question.** Prototype events: concert seat-map selection modelled on Coca-Cola Arena (like Platinum List); multi-day festival with day/time-slot selection; tiered show tickets (early bird, couple, group-of-4, group-of-6); all share one add-to-cart and checkout flow. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Events) · DI-685)*
- Decision: seats held in a cart auto-release after a configurable timeout if checkout is abandoned, and immediately if a payment attempt fails. *(agreed · MoM 21 Aug 2026, 4.6 Seat Inventory Status; 5. Key Decisions · DI-422)*
- Decision: seating rules — consecutive-seat enforcement (no single empty seat left between bookings), social-distancing buffer (auto-block adjacent seats), seat-kill rule, company/held-seat rule — are configurable per venue/event, defaulting to the venue's operational policy. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules; 5. Key Decisions · DI-416)*
- One seat map can mix section types — e.g. 8 of 10 sections seated and 2 standing ("fan pit" near the stage); suites sell either as a private bulk-priced suite or as individual seats within the suite. *(agreed · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types · DI-411)*
- Decision: three seat-selection models, selectable per section, per event: (1) zone/capacity selling with no seat numbers (guest told zone only); (2) system-assigned "best available" — guest picks section + quantity, seats disclosed later; (3) full customer seat selection. *(agreed · MoM 21 Aug 2026, 4.1 Reference Walkthrough; 4.2 Seat Map Builder; 5. Key Decisions · DI-410)*
- Platinum List reference seat step: interactive seat map colour-coded by price tier → seat selection with a live cart hold and countdown timer → checkout via Quick Order / Apple ID / Google ID. *(client request · MoM 21 Aug 2026, 4.1 Reference Walkthrough — Platinum List Seat Selection & Checkout Journey · DI-409)*
- Drag-and-drop page builder with a standardised layout (header, footer, hero/card components) that adapts to product type — seat map for seated products, standard flow for general admission. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-394)*
- Movie/cinema ticketing is in scope through the seat management module (e.g. a Kuwait museum's educational cinema: assigned seats, a film, a time slot). *(agreed · MoM 14 Aug 2026, 5. Movie Ticketing · DI-286)*
- Booking steps follow the product type: admission goes straight to quantity; dated products to a date, timed ones on to a time, then quantity; seated products to zone, then seats on a seat map, then quantity by variant (adult, child, concession). *(agreed · MoM 3 Aug 2026, Ticket Flow Variations by Product Type · DI-131)*
- Seat assignment flow is "select time, then select seat", with the two steps on different screens. *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-057)*

`WEB-008` Add-ons & Upsell

- **Open question.** Is the swim vest an add-on product, and is the splash-and-river pass a separate product offered only to non-swimmers? Default built: the swim answer filters products (as Help me choose); the vest is an add-on; the splash-and-river pass is its own product. *(open · Decisions Register 1 Oct 2026, Questions for the client — Guest safety / Swim ability · DI-1118)*
- Existing booking settings stay: step indicator, extras step, seat picker, map view, quantities on add-ons (−/+ stepper, price multiplies), embed mode, hero banner, search in banner, single-event page. Defaults: search in banner off, seat picker = bowl. *(agreed · design review 29 Sep 2026, CFG-6 · Step indicator; Extras step; Seat picker; Map view; Quantities on add-ons; Embed mode; Hero banner; Search in banner; Single-event page · DI-1070)*
- Cart & summary options: sidebar fixed right, sidebar left, slide-in right, slide-up bottom, floating cart icon (round basket button with item count opening the slide-in basket), single column. In Arabic the basket stays on the right by default (client confirmed); "Cart side in Arabic" can mirror to left. *(agreed · rev 3 design review 29 Sep 2026, REV3-10 · 10. Cart display: fixed on right, slide bar, icon, bottom; right for Arabic · DI-1051)*
- Sign-in (or the guest code when guest checkout is on) is asked when the guest leaves the Add-ons step; the basket is kept. Setting "Ask to sign in": After add-ons (default) or At payment. *(agreed · rev 3 design review 29 Sep 2026, REV3-3 · 3. The sign-in screen should appear after Add-ons · DI-1043)*
- With the "Slide in right" cart setting, the summary is a tab on the right edge that slides in from the right (not a bar at the bottom). *(client request · design review 23 Sep 2026, Cart 13. Cart summary: 'Slide in right' shows at the bottom · DI-981)*
- Add-ons appear only on the Add-ons / Extras step, never in the ticket panels. Each add-on appears once (no duplicates such as 'Large locker' on two steps). *(client request · design review 23 Sep 2026, Cart 11. Show add-ons only on the Add-ons / Extras page · DI-979)*
- "Upgrade your day" (upgrades) stays hidden until a main ticket is in the cart. *(client request · design review 23 Sep 2026, Cart 10. Show upgrades only after the main ticket is in the cart · DI-978)*
- A guest is not repeatedly re-offered something already declined (e.g. a fast pass rejected three times), and an offer ignored online is not re-presented on another channel, e.g. at POS after the guest bought it there. *(agreed · MoM 21 Sep 2026, 4.6 Personalized Offer Delivery & Omni-Channel Orchestration · DI-962)*
- What a guest is offered depends on context: a member is not offered another membership (F&B or retail add-ons instead); general admission is not offered once VIP/fast pass is selected; an expiring membership prompts a renewal rather than a new product; similar offers are not shown back-to-back (alternate F&B and experience upsells). *(client request · MoM 21 Sep 2026, 4.2 / 4.3 / 4.5 Recommendation Strategy and Decisioning · DI-960)*
- Recommendations stay within business limits, e.g. at most three recommendations shown at checkout and never a product the customer already owns; AI recommendations never override hard business rules or eligibility constraints. *(agreed · MoM 21 Sep 2026, 4.3 Recommendation Strategy — Business Priority, Conflict Suppression & Fallback · DI-959)*
- Upsell/cross-sell offers (e.g. a family pass after 2 adult + 2 child tickets are added) are a distinct "extras" step after main product selection, not inline on the ticket selection page, where guests would miss them. *(agreed · MoM 18 Sep 2026, 4.14 Guest Website UX Review — Upsell/Cross-Sell Placement & Reference Sites · DI-951)*
- **Open question.** Cabanas: category (premium, VIP, luxury, private, family, couples), date/time, guest count, amenity details. Activities: desert-safari packages (buy-one-get-one, evening, Bedouin-style), pickup point, add-ons (stroller), duration packages (2-hour/4-hour). *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Cabanas, Activities) · DI-687)*
- Reference details: sibling/multi-buy discount shown with a struck-through original price; workshop add-ons inline with theme/cuisine sub-selection feeding time-slot availability; a package builder for bundled experiences. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-586)*
- Add-ons attached to a main product can be mandatory or optional; cross-sell offers related add-on products, upsell proposes a higher tier (e.g. adult admission → membership). *(client request · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies · DI-470)*
- Decision: the add-ons step is optional/removable in configuration for products with no add-ons, collapsing the flow to Ticket Selection → Cart → Checkout. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-428)*
- System-driven upsell/cross-sell prompts, e.g. a yearly membership on top of general admission, or a family bundle when 2 adult + 2 child tickets are in the cart, each with its discount/benefit. *(client request · MoM 10 Aug 2026, 4.8 Checkout Extras — Delivery, Waiting Room, Upsell/Cross-Sell, Seating, Resources · DI-216)*

`WEB-009` Wishlist

- Duplicate screens become one implementation covering several screen IDs (mobile Transfer + Delivery & Sharing; web Wishlist / Devices & Consent; Help Centre + Help & Accessibility as one Help view with FAQ, cases, policies, accessibility tabs). Ticket-selection functions belong on GST-008. Web gets a Group Booking view. *(agreed · design review 29 Sep 2026, GAP-D3 · D. Duplicate screens merged; group booking on web · DI-1078)*
- Add bookings to Apple/Google/Outlook calendar with reminders; wishlist of F&B and retail items to buy later on-site. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-202)*

`WEB-010` Shopping Cart

- Guest counters take their price from the chosen park ticket and produce one line, e.g. "2 park ticket · Adult × 3 = AED 1,425" (no separate Adult × 3 line). Child and senior prices scale from the chosen ticket; infants free. *(client request · design review 30 Sep 2026, 2. Multi-park ticket adds an extra adult line · DI-1106)*
- Web screens carry: cart promo code (valid/invalid/expired) and empty basket with confirm; interrupted-payment recovery ("we are checking with your bank" → success/failed/unknown); reprint/resend tickets; UAE Pass sign-in, link guest checkout, sign out; support cases and Sahli handoff; FX rates with timestamp; remaining entitlements. *(agreed · design review 29 Sep 2026, GAP-B3 · B. Web — missing functions on existing screens · DI-1074)*
- Cart & summary options: sidebar fixed right, sidebar left, slide-in right, slide-up bottom, floating cart icon (round basket button with item count opening the slide-in basket), single column. In Arabic the basket stays on the right by default (client confirmed); "Cart side in Arabic" can mirror to left. *(agreed · rev 3 design review 29 Sep 2026, REV3-10 · 10. Cart display: fixed on right, slide bar, icon, bottom; right for Arabic · DI-1051)*
- Each cart line shows the date of visit: the match date for the stadium, the reservation date for dining (mobile: in the cart bar). *(agreed · design review 29 Sep 2026, Cart 9. Show the date of visit in the cart · DI-1029)*
- Each picked seat goes into the cart with section, row, seat and price (e.g. "Section 101 · Row A, Seat 4 · AED 165"); tapping the seat again removes it. *(client request · design review 23 Sep 2026, Seat map 15. Selected seats should be added to the cart · DI-982)*
- With the "Slide in right" cart setting, the summary is a tab on the right edge that slides in from the right (not a bar at the bottom). *(client request · design review 23 Sep 2026, Cart 13. Cart summary: 'Slide in right' shows at the bottom · DI-981)*
- "Upgrade your day" (upgrades) stays hidden until a main ticket is in the cart. *(client request · design review 23 Sep 2026, Cart 10. Show upgrades only after the main ticket is in the cart · DI-978)*
- Six Flags reference for the B2C redesign (Qossai): right-to-left cart drawer. *(client request · MoM 8 Sep 2026, 4.20 Planning & Next Steps · DI-737)*
- Date-change flow detects conflicts across an existing multi-ticket cart and lets the guest shift the whole booking to a new date in one action. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-587)*
- **Open question.** Open: alongside curated pre-built packages, let guests build their own bundle in the cart, with the system detecting eligible combinations and applying an automatic discount (e.g. 5–10%). *(open · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-221)*
- Dynamic offers apply automatically without a code (buy-2-get-1-free, buy-3-get-2-at-50%-off, fixed amount off a minimum quantity); the discounted item is added to the cart automatically with its price adjusted (e.g. to zero). *(agreed · MoM 7 Aug 2026, 17. Promotions & Dynamic Offers · DI-174)*
- Qossai: the POS-style right-to-left slide-in drawer could also suit the B2C cart/checkout. *(client request · MoM 3 Aug 2026, 10. Reference Material & Design Research · DI-124)*

`WEB-011` Guest Details & Attendee Forms

- Sign-in (or the guest code when guest checkout is on) is asked when the guest leaves the Add-ons step; the basket is kept. Setting "Ask to sign in": After add-ons (default) or At payment. *(agreed · rev 3 design review 29 Sep 2026, REV3-3 · 3. The sign-in screen should appear after Add-ons · DI-1043)*
- The guest-checkout email pop-up collects only the fields configured in the back end (email, phone and/or name). After the code is verified, do not ask for name/email/phone again: go straight to T&Cs and complete the booking; profile is created and can be completed later (Platinumlist pattern). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W1 Guest checkout · DI-1002)*
- **Open question.** Qossai: a guest-checkout customer may not have opted into marketing the way a registered customer accepting full terms has; how marketing consent is captured at guest checkout is unresolved. *(open · MoM 18 Sep 2026, 4.8 Guest Checkout & Profile Deduplication — Extended Discussion · DI-940)*
- Channel rules govern which actions each channel can perform (create, upgrade, cancel) and whether checkout is guest checkout (name, phone, email only) or full registration/sign-in. Customer category (corporate, travel agent/B2B, school) determines extra information collected. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-613)*
- Waiver is triggered automatically when an associated product is bought; timing is business-configurable: at checkout, post-purchase, or on-site before entry. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-573)*
- Eligibility rules are configurable: residency/nationality/geography (e.g. UAE-resident-only with Emirates ID capture), minimum age (date-of-birth check), guest-profile category (e.g. VIP-only) and minimum loyalty points/spend for a membership tier. *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-463)*
- Ticket attributes such as minimum age, ID-proof requirements (e.g. Emirates ID for UAE-resident tickets, with format validation or photo upload; passport; handicap/PoD documentation) or an embedded ID-reader for on-site verification are configurable per ticket and region, not fixed. *(agreed · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference; 5. Key Decisions · DI-443)*
- Guest information capture (name, mobile number, nationality, visit survey, etc.) is configurable per ticket type; even an open-dated admission ticket can optionally collect it. *(agreed · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough; 5. Key Decisions · DI-434)*
- Decision: season-pass/family-type products capture first and last name for each individual pass holder (not just the purchaser), via an "add guest name" step. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-429)*
- Decision: at least one of e-mail or mobile number is mandatory at profile creation (not both — some customers decline e-mail); the system supports conditional "either/or" mandatory-field rules. *(agreed · MoM 20 Aug 2026, 4.1 CRM; 5. Key Decisions · DI-372)*
- Per-ticket "ticket owner" details are captured separately from the "reservation owner" (buyer) and can enforce rules such as a minimum age per ticket holder. *(agreed · MoM 7 Aug 2026, 20. Live Point-of-Sale Transaction Walkthrough · DI-178)*
- Custom fields gate purchase where configured — e.g. a checkbox confirming a guest is not pregnant before a specific product can be bought, or a weight-range field for an activity. *(agreed · MoM 7 Aug 2026, 6. Data Mask: Flexible Custom Data Capture · DI-156)*
- UAE Pass login: customer enters mobile number, approves a push notification, confirms with biometrics; verified personal details are pulled into the booking automatically and a linked account is created. *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-123)*
- Separate "ticket holder" (per-ticket details captured where required) from "reservation owner"/buyer (single contact captured once per booking who receives the tickets by email). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-122)*

`WEB-012` Checkout — Payment

- Web screens carry: cart promo code (valid/invalid/expired) and empty basket with confirm; interrupted-payment recovery ("we are checking with your bank" → success/failed/unknown); reprint/resend tickets; UAE Pass sign-in, link guest checkout, sign out; support cases and Sahli handoff; FX rates with timestamp; remaining entitlements. *(agreed · design review 29 Sep 2026, GAP-B3 · B. Web — missing functions on existing screens · DI-1074)*
- Sign-in (or the guest code when guest checkout is on) is asked when the guest leaves the Add-ons step; the basket is kept. Setting "Ask to sign in": After add-ons (default) or At payment. *(agreed · rev 3 design review 29 Sep 2026, REV3-3 · 3. The sign-in screen should appear after Add-ons · DI-1043)*
- After the code, a match prompt shows what matched (e.g. 4 past orders, first order 12 Mar 2024, profile type), never the other profile's name or details, with "Use this profile" / "Not me – keep separate". Expired state: "This match has expired – continue as a new guest." *(agreed · design review 29 Sep 2026, 1. Guest checkout, code proof, profile matching (WEB-012) · DI-1035)*
- Guest checkout is a venue toggle, off by default: off = sign-in screen at payment ("This venue requires an account for checkout. Your basket is kept."), guest button hidden. On = "Continue as guest" with email or mobile (per "Match returning guests by") and a code; only exactly six digits accepted, copy says six. *(agreed · design review 29 Sep 2026, 1. Guest checkout, code proof, profile matching (WEB-012) · DI-1034)*
- The guest-checkout email pop-up collects only the fields configured in the back end (email, phone and/or name). After the code is verified, do not ask for name/email/phone again: go straight to T&Cs and complete the booking; profile is created and can be completed later (Platinumlist pattern). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W1 Guest checkout · DI-1002)*
- Marketing opt-in ("Send me offers and news") sits beside the T&Cs at checkout and is never pre-ticked. Open: whether a guest-checkout customer may be marketed on it; until confirmed it stays unticked and nothing is sent without it. *(agreed · MoM 18 Sep 2026, M18-15 · DI-954)*
- Checkout captures marketing/newsletter opt-in and preferred contact method (email vs phone). *(client request · MoM 1 Sep 2026, 4.13 Privacy Consent & Cookie Policy · DI-616)*
- Fees are separate from taxes: e.g. a call-center convenience fee, or a shipping fee varying by destination (Dubai, Abu Dhabi, Ras Al Khaimah, international) calculated from the checkout address; applied at transaction, item or ticket level. Checkout must show the fee once the address is entered. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-597)*
- Support both redirect to the gateway's hosted page and embedded/iframe capture (card, Apple Pay, Tabby) on the platform's own checkout preserving its look and feel, for Network International and Stripe; embedded needs extra security certification to reassure guests. *(agreed · MoM 31 Aug 2026, 4.13 Payment gateway approach · DI-589)*
- At checkout guests can sign in, register (with a visible loyalty-points incentive) or continue as guest; terms acceptance is implied by proceeding to payment, with no separate checkbox. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-588)*
- Split tender: one purchase paid with wallet balance plus another method, e.g. AED 500 from the wallet and the remaining AED 200 of a AED 700 purchase on a credit card. *(agreed · MoM 27 Aug 2026, 4.7 Split-Tender, Redemption Rules & Configuration Simulation · DI-525)*
- Donation campaigns: fixed or variable amounts, enabled per sales channel, triggered on a specific product or across all products, proceeds tracked to a separate account code. *(client request · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies · DI-471)*
- Decision: seats held in a cart auto-release after a configurable timeout if checkout is abandoned, and immediately if a payment attempt fails. *(agreed · MoM 21 Aug 2026, 4.6 Seat Inventory Status; 5. Key Decisions · DI-422)*
- Platinum List reference seat step: interactive seat map colour-coded by price tier → seat selection with a live cart hold and countdown timer → checkout via Quick Order / Apple ID / Google ID. *(client request · MoM 21 Aug 2026, 4.1 Reference Walkthrough — Platinum List Seat Selection & Checkout Journey · DI-409)*
- Once a delivery address is entered, the applicable shipping fee is shown automatically for the customer to accept before payment. *(client request · MoM 19 Aug 2026, 4.8 Online Order Fulfilment & Shipping Configuration · DI-360)*
- Checkout supports guest checkout, registered-account checkout, and single sign-on (e.g. Okta, Azure AD, a ticketing-specific SSO). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-121)*
- Apple Pay / Google Pay tap-to-pay are the primary regional digital payment methods; UPI-style QR payments may come later, not in initial scope. *(agreed · MoM 31 Jul 2026, 12. Payments & Regional Preferences · DI-079)*

`WEB-013` Booking Confirmation

- Web screens carry: cart promo code (valid/invalid/expired) and empty basket with confirm; interrupted-payment recovery ("we are checking with your bank" → success/failed/unknown); reprint/resend tickets; UAE Pass sign-in, link guest checkout, sign out; support cases and Sahli handoff; FX rates with timestamp; remaining entitlements. *(agreed · design review 29 Sep 2026, GAP-B3 · B. Web — missing functions on existing screens · DI-1074)*
- Any online purchase for a dynamic-QR event must be linked to the mobile app to show the working code; web/desktop purchases are redirected into the app for activation, not exempted. *(agreed · MoM 2 Sep 2026, 4.7 Confirmed (Pradnya's question) · DI-635)*
- Apple/Google Wallet configuration covers template design (background colour, header, footer) and the guest-facing "Add to Apple Wallet" flow after an online purchase. *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-609)*
- Ticket delivery: "Add to Wallet" (Apple or Google Wallet by device), and WhatsApp, SMS or email per the guest's chosen method, selectable at checkout/confirmation; tickets can also be emailed to a third party. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-198)*

`WEB-014` Pay for a Booking

- Amendments/cancellations/reschedules are checked against the applicable policy before being allowed. A booking's financial status (deposit required, partial payment, full payment) is tracked; schools and corporates can pay a 20-30% deposit with the balance due on or before arrival. *(agreed · MoM 1 Sep 2026, 4.12 Amendment, Cancellation & Booking Status · DI-615)*
- Send Payment Link (deposit or full) opens a B2C-style cart-review and checkout page showing the booking the sales team created. Configurable expiry (e.g. 24 hours, a week); unpaid bookings auto-cancel on expiry. Applies to B2C, schools, corporates and groups. *(agreed · MoM 31 Aug 2026, 4.8 Send Payment Link · DI-567)*

`WEB-015` Branded Queue / Waiting Room

- Branded virtual waiting room activates automatically above a configurable concurrent-buyer threshold (e.g. 500) during high-demand on-sales, shows a wait time, and follows the tenant's app theme. *(client request · MoM 10 Aug 2026, 4.8 Checkout Extras — Delivery, Waiting Room, Upsell/Cross-Sell, Seating, Resources · DI-214)*
- Waiting room behaviour: guests are held in a queue that preserves their connection, told an estimated wait time, and let through in controlled batches (e.g. 200-300 guests per minute); completed transactions must reliably trigger email confirmation and ticket delivery. *(agreed · MoM 31 Jul 2026, 5. Consistency, Replication & Disaster Recovery · DI-062)*
- Virtual waiting room page: branded with the customer's venue logo, shows estimated waiting time and progress indicators, admits customers at controlled intervals. Configured independently per customer and venue. *(agreed · MoM 28 Jul 2026, 19. Auto-scaling and Virtual Waiting Room · DI-016)*

`WEB-016` Login / Register

- Web screens carry: cart promo code (valid/invalid/expired) and empty basket with confirm; interrupted-payment recovery ("we are checking with your bank" → success/failed/unknown); reprint/resend tickets; UAE Pass sign-in, link guest checkout, sign out; support cases and Sahli handoff; FX rates with timestamp; remaining entitlements. *(agreed · design review 29 Sep 2026, GAP-B3 · B. Web — missing functions on existing screens · DI-1074)*
- Guest two-step verification is a per-venue setting, off by default. Enrolment lives on the guest's tenant-wide account; the second factor is asked only when signing in or acting at a venue that enables it. Guests never see enterprise SSO. *(agreed · design review 29 Sep 2026, GAP-B1 · B. Login: set up two-step verification; C. Security & Sign-in (step-up auth) · DI-1072)*
- Sign-in (or the guest code when guest checkout is on) is asked when the guest leaves the Add-ons step; the basket is kept. Setting "Ask to sign in": After add-ons (default) or At payment. *(agreed · rev 3 design review 29 Sep 2026, REV3-3 · 3. The sign-in screen should appear after Add-ons · DI-1043)*
- After the code, a match prompt shows what matched (e.g. 4 past orders, first order 12 Mar 2024, profile type), never the other profile's name or details, with "Use this profile" / "Not me – keep separate". Expired state: "This match has expired – continue as a new guest." *(agreed · design review 29 Sep 2026, 1. Guest checkout, code proof, profile matching (WEB-012) · DI-1035)*
- Guest checkout is a venue toggle, off by default: off = sign-in screen at payment ("This venue requires an account for checkout. Your basket is kept."), guest button hidden. On = "Continue as guest" with email or mobile (per "Match returning guests by") and a code; only exactly six digits accepted, copy says six. *(agreed · design review 29 Sep 2026, 1. Guest checkout, code proof, profile matching (WEB-012) · DI-1034)*
- The guest-checkout email pop-up collects only the fields configured in the back end (email, phone and/or name). After the code is verified, do not ask for name/email/phone again: go straight to T&Cs and complete the booking; profile is created and can be completed later (Platinumlist pattern). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W1 Guest checkout · DI-1002)*
- At checkout guests can sign in, register (with a visible loyalty-points incentive) or continue as guest; terms acceptance is implied by proceeding to payment, with no separate checkbox. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-588)*
- Decision: at least one of e-mail or mobile number is mandatory at profile creation (not both — some customers decline e-mail); the system supports conditional "either/or" mandatory-field rules. *(agreed · MoM 20 Aug 2026, 4.1 CRM; 5. Key Decisions · DI-372)*
- Sign-up by phone number or email, verified by OTP (WhatsApp or SMS/email as configured), then minimal profile (first/last name). *(client request · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-209)*
- UAE Pass login: customer enters mobile number, approves a push notification, confirms with biometrics; verified personal details are pulled into the booking automatically and a linked account is created. *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-123)*
- Checkout supports guest checkout, registered-account checkout, and single sign-on (e.g. Okta, Azure AD, a ticketing-specific SSO). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-121)*

`WEB-017` My Account Dashboard

- Web account gets device management and "sign out a lost device" (WEB-024). Face Pass stays mobile-only until the facial-reader vendor SDK supports web capture. *(agreed · design review 29 Sep 2026, GAP-D1 · D. Mobile-only features get web equivalents · DI-1077)*

`WEB-018` My Tickets

- Web screens carry: cart promo code (valid/invalid/expired) and empty basket with confirm; interrupted-payment recovery ("we are checking with your bank" → success/failed/unknown); reprint/resend tickets; UAE Pass sign-in, link guest checkout, sign out; support cases and Sahli handoff; FX rates with timestamp; remaining entitlements. *(agreed · design review 29 Sep 2026, GAP-B3 · B. Web — missing functions on existing screens · DI-1074)*
- Entitlements portfolio is used both by the guest (mobile app) and by customer service: one view of restrictions, wallet balance and all entitlements; a unified list across a visit (e.g. four admissions, two fast passes, a meal package, a parking entitlement). *(client request · MoM 7 Sep 2026, 4.9 Entitlements Portfolio - Structure, Family/Group & Assignment · DI-667)*
- Any online purchase for a dynamic-QR event must be linked to the mobile app to show the working code; web/desktop purchases are redirected into the app for activation, not exempted. *(agreed · MoM 2 Sep 2026, 4.7 Confirmed (Pradnya's question) · DI-635)*
- Upgrades must be available in the guest mobile/web app: guests view eligible upgrade options and complete the upgrade online without visiting on-site. *(agreed · MoM 1 Sep 2026, 4.9 / 5. Key Decisions · DI-606)*
- Staff can upgrade multiple tickets in one action. "Quick upgrade" is a direct single-path upgrade (gold > platinum); "flexible upgrade" lets the guest choose among several eligible targets. *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-605)*
- Qossai: where a waiver is required before entry, an incomplete waiver can block ticket download, activation, check-in or access; ticket and scan screens need a waiver-incomplete state. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-574)*
- Decision (raised by Chinmay): date-change/reschedule is a product-level on/off setting with its own policy rules (e.g. allowed up to 24 hours before the visit, denied within 24 hours), not a separate screen. Typically off for special-day tickets (e.g. New Year, 1 January only), on for standard GA. *(agreed · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive; 5. Key Decisions · DI-446)*
- Decision: deferred seat assignment — sale confirmed at purchase as section + quantity; seats allocated internally; closer to the event ops/admin trigger a bulk e-mail issuing QR tickets with final seats. Immediate seat assignment remains for venues that need it. *(agreed · MoM 21 Aug 2026, 4.7 Deferred Seat Assignment Model; 5. Key Decisions · DI-423)*

`WEB-019` Order History

- Online/app returns: customer submits a return request with a reason (and photo if applicable) → approval team → courier pickup → refund after verified receipt. Confirmed: an item bought at the POS can also be returned via the web portal, subject to approval. *(agreed · MoM 19 Aug 2026, 4.7 Returns, Refunds & Exchanges — In-Store and Online; 5. Key Decisions · DI-367)*
- Guests can request a refund from their account/profile; operations are notified and can approve, reject or ask for more information. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-254)*

`WEB-021` Wallet & Gift Cards

- Peer-to-peer transfer from one guest's wallet to another guest's wallet; a configurable venue-level toggle (allowed or not), not a default feature. *(agreed · MoM 27 Aug 2026, 4.10 Transfers, Fraud/Risk Controls · DI-536)*
- Two variants: monetary gift card (value usable on anything the venue offers) and product-specific gift voucher (redeemable only for a named product, e.g. a dolphin-show voucher). Redemption channel is configurable: online, on-site or both. *(client request · MoM 27 Aug 2026, 4.9 Gift Cards, Vouchers & Wallet Payments · DI-533)*
- Balance can move between linked family/group wallets in either direction (parent to child, child to parent); a venue-controlled toggle, not always enabled. *(agreed · MoM 27 Aug 2026, 4.8 Shared wallet transfer · DI-532)*
- Guests can create family-member profiles themselves and set spending limits directly from their own guest account, in addition to venue-side configuration. *(agreed · MoM 27 Aug 2026, 4.8 Family, Parent-Child & Corporate Wallets · DI-530)*
- A parent's wallet funds linked child wristbands/wallets with per-child spending allowances, e.g. of a AED 500 family balance one child is capped at AED 200 and another at AED 200. *(agreed · MoM 27 Aug 2026, 4.8 Family, Parent-Child & Corporate Wallets · DI-529)*
- Consumption is fully automatic FEFO (nearest expiry first). Guests see their balance and the expiry breakdown per top-up lot in their profile but cannot choose which lot is drawn down; no lot picker at payment. *(agreed · MoM 27 Aug 2026, 4.6 Stored Value, Credit Consumption & FEFO Logic · DI-523)*
- Guests must be able to configure auto-reload and recurring funding schedules themselves in the guest web/app, not only venue admins in the back office. *(agreed · MoM 27 Aug 2026, 4.5 Funding / 5. Key Decisions · DI-519)*
- Top-up rules set minimum and maximum amounts per transaction; channel/funding-source mapping restricts which payment methods each channel offers (e.g. cash top-up on-site only, not online), so each channel's top-up screen offers only its allowed methods. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-517)*
- Ownership and access rules are configurable per wallet type. Family default: only the parent/guardian can top up; children can view balance and transactions and spend, but cannot top up unless permissions are explicitly reconfigured. Guest wallet screens must hide or disable top-up for members without the right. *(agreed · MoM 27 Aug 2026, 4.2 Wallet Ownership / 4.8 Family Permission Rules · DI-509)*
- Wallet type library: multiple wallet types (guest, family, membership wallet), each assigned to a category (individual, corporate, member). Provisioning rules set the trigger that creates a wallet (membership purchase, first top-up); two patterns: gift-card style (pre-defined value products listed on the website) and open-ended "add money to wallet". *(client request · MoM 27 Aug 2026, 4.2 Wallet Type Library, Ownership & Account Association · DI-508)*
- Referral rewards may be credited as currency/points directly into the guest's wallet (like Swiggy), in addition to discount vouchers — a business-configurable option. *(agreed · MoM 25 Aug 2026, 4.7 Entitlements & Access Control; 5. Key Decisions · DI-460)*
- A combo product can bundle admission with stored-value credit the guest draws down on F&B or retail purchases (wallet mechanics in a dedicated session). *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-459)*
- Wallet balance is shared across a linked family — a parent's top-up can be drawn down by a linked child's wristband without a separate top-up. *(agreed · MoM 20 Aug 2026, 4.1 CRM; 4.5 Loyalty, Membership & Wallet · DI-374)*

`WEB-022` Membership Plans

- Season and membership packages show a quantity stepper once selected. *(client request · design review 23 Sep 2026, Cart 12. No quantity field for the selected ticket · DI-980)*
- UX reference: House of Wisdom (Sharjah library) meeting-room/"pod" booking and tiered membership plans — a simple duration-based booking flow without fixed performances/time slots — to be reviewed by Chinmay/Aishwarya. *(client request · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 6. Open Items · DI-506)*
- Membership/pass tickets: seasonal, monthly or annual classes with renewal/auto-renewal using a tokenised card-on-file billed ahead of expiry, subject to the guest's consent to terms and conditions. *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-448)*
- Membership / season pass is defined by start/end date rather than quantity, requires customer profile capture at purchase, and supports renew, upgrade, cancel and extend workflows. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-138)*

`WEB-023` Membership Management

- Account → Membership → Billing statement shows a line-by-line statement with states: soft decline (Retry now + Use another card), hard decline (Use another card only), declined again (Use another card + next automatic retry date), paid ("Your membership continues"). Use another card lists saved cards. *(agreed · design review 29 Sep 2026, 2. Billing statement and payment retry (WEB-023) · DI-1036)*
- Membership lifecycle: upgrade, downgrade, suspend (freezes validity until re-enabled), deactivate and cancel, with configurable timing windows (e.g. upgrade allowed only in the final two months before expiry). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-467)*
- Membership/pass tickets: seasonal, monthly or annual classes with renewal/auto-renewal using a tokenised card-on-file billed ahead of expiry, subject to the guest's consent to terms and conditions. *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-448)*
- Membership screen: membership ID, validity, entitlements (free entry, F&B offers, etc.), linked members (view), membership card, renewal and history. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-201)*
- Membership / season pass is defined by start/end date rather than quantity, requires customer profile capture at purchase, and supports renew, upgrade, cancel and extend workflows. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-138)*

`WEB-024` Devices, Wishlist & Consent

- Duplicate screens become one implementation covering several screen IDs (mobile Transfer + Delivery & Sharing; web Wishlist / Devices & Consent; Help Centre + Help & Accessibility as one Help view with FAQ, cases, policies, accessibility tabs). Ticket-selection functions belong on GST-008. Web gets a Group Booking view. *(agreed · design review 29 Sep 2026, GAP-D3 · D. Duplicate screens merged; group booking on web · DI-1078)*
- Web account gets device management and "sign out a lost device" (WEB-024). Face Pass stays mobile-only until the facial-reader vendor SDK supports web capture. *(agreed · design review 29 Sep 2026, GAP-D1 · D. Mobile-only features get web equivalents · DI-1077)*

`WEB-025` Help Centre / FAQ

- Duplicate screens become one implementation covering several screen IDs (mobile Transfer + Delivery & Sharing; web Wishlist / Devices & Consent; Help Centre + Help & Accessibility as one Help view with FAQ, cases, policies, accessibility tabs). Ticket-selection functions belong on GST-008. Web gets a Group Booking view. *(agreed · design review 29 Sep 2026, GAP-D3 · D. Duplicate screens merged; group booking on web · DI-1078)*
- Web screens carry: cart promo code (valid/invalid/expired) and empty basket with confirm; interrupted-payment recovery ("we are checking with your bank" → success/failed/unknown); reprint/resend tickets; UAE Pass sign-in, link guest checkout, sign out; support cases and Sahli handoff; FX rates with timestamp; remaining entitlements. *(agreed · design review 29 Sep 2026, GAP-B3 · B. Web — missing functions on existing screens · DI-1074)*
- The guest Help screen shows app status and a public, localised "what's new" (release notes). *(agreed · design review 29 Sep 2026, GAP-B2 · B. Help: app status + recent changes · DI-1073)*
- Support chat is native to TICVAI: a built-in AI chat assistant answers first, then escalates to a human "CR representative" role in the platform; offered white-labelled as a subscription add-on for smaller clients. *(agreed · MoM 12 Aug 2026, 10. Customer Support / Chat Integration Approach · DI-256)*
- Configurable FAQ section plus Terms & Conditions, Privacy Policy and Cookie Policy with an accept/deny prompt. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-191)*

`WEB-026` Survey & Feedback

- Surveys trigger at configurable points: post-purchase, post-visit, post-ticket-scan, membership renewal and case closure. *(client request · MoM 20 Aug 2026, 4.9 Surveys & Gamification · DI-391)*
- Example site showed a live integration with a government satisfaction-survey ("happiness meter") service. *(client request · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-112)*

`WEB-027` Newsletter Subscription

- Consent policy governs marketing/newsletter/survey communications; customers who do not opt in must not receive promotional communications. *(client request · MoM 20 Aug 2026, 4.3 Consent, Data Privacy & Retention · DI-378)*

`WEB-029` Error / Sold Out / Maintenance

- Customisable maintenance page shown to guests during planned maintenance/upgrades. *(client request · MoM 10 Aug 2026, 4.8 Checkout Extras — Delivery, Waiting Room, Upsell/Cross-Sell, Seating, Resources · DI-215)*

`WEB-030` Ticket Transfer

- A purchased ticket can be transferred to another guest (e.g. a friend); the system keeps the original purchaser and full transfer history. *(client request · MoM 7 Sep 2026, 4.9 Ownership and transfer · DI-669)*
- Once activated in the app a digital ticket is bound to one approved device; moving to a new device requires deactivating the prior binding. Credential transfer moves a ticket to another person's device and invalidates the original holder's copy. *(client request · MoM 2 Sep 2026, 4.8 Device Binding, Credential Transfer & Revocation · DI-636)*
- Ticket transfer by email/SMS with optional message; either keep ownership and rename the holder, or transfer both ownership and holder. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-200)*

`WEB-031` My Reservations

- **Open question.** Are water-park groups booked into a session (the build picks a session first)? Default built: group requests take a date and, for session-based products, a session. *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Water-park groups by session · DI-1117)*
- **Open question.** Each group ticket card shows a minimum group size; is it set per group ticket, and what values? Default built: each group ticket carries its own minimum, default 10. *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Minimum group size · DI-1116)*
- **Open question.** Do Tour operator and Community become their own group types or map to general? Default built: School, Corporate, Tour operator and Community shown as their own group types (platform also has general and party). *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Group types · DI-1115)*
- **Open question.** How many supervisors come free per group (per N guests), and is it per group ticket? Default built: supervisors are a separate, free guest type, up to 1 per 10 guests, counted on the group request. *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Supervisors · DI-1114)*
- Supervisors are listed separately and are free; the enquiry panel shows the estimate as e.g. "School group · Guests × 45". Water park group booking: pick a session, then enter the number of swimmers and supervisors. On mobile the headcount stepper has a +10 button. *(client request · design review 30 Sep 2026, 1. Group booking: product missing, enter the number of people · DI-1105)*
- Group / school booking starts with group ticket cards (School, Corporate, Tour operator, Community), each showing a per-person price and minimum group size. Then "How many people" is a number box the guest can type (e.g. 45) or step with − / +; no Group size dropdown. *(client request · design review 30 Sep 2026, 1. Group booking: product missing, enter the number of people · DI-1104)*
- Duplicate screens become one implementation covering several screen IDs (mobile Transfer + Delivery & Sharing; web Wishlist / Devices & Consent; Help Centre + Help & Accessibility as one Help view with FAQ, cases, policies, accessibility tabs). Ticket-selection functions belong on GST-008. Web gets a Group Booking view. *(agreed · design review 29 Sep 2026, GAP-D3 · D. Duplicate screens merged; group booking on web · DI-1078)*
- Booking statuses: draft > reserved (awaiting payment) > completed, with cancelled or expired paths. Hold policy sets how long a capacity booking is held pending payment before release to inventory. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-612)*
- Guest profile shows gift vouchers and a stored-value "money card"/wallet; "My Tickets" (all tickets) is separate from "My Reservations" (bookings holding one or more tickets) with reservation details and date modification. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-199)*

`WEB-033` Shop

- **Open question.** Resources: meeting-room booking (headcount, duration, time slot, room, add-ons tea/coffee/snacks), modelled on House of Wisdom. Merchandise: browse, cart with add/remove quantity, pickup or doorstep delivery. F&B: outlet/menu browsing; collect at counter, curbside, doorstep or priority delivery. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Resources, Merchandise, F&B) · DI-690)*
- Decision (raised by Aishwarya): F&B and retail/merchandise online sale are optional back-office-enabled modules; where enabled, the whole purchase (browse, cart, checkout, pickup-at-venue or ship-to-guest) completes inside TICVAI — guests are never sent to download a separate app. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-505)*
- Retail items (e.g. a t-shirt plus a cap) can be combined into a combo package with bundle-level pricing, presented both on-site and online with product images and descriptions. *(client request · MoM 19 Aug 2026, 4.3 Pricing, Bundles & Promotions · DI-358)*

`WEB-034` Lost & Found

- Lost & Found: guests log lost items in the app; back-office staff match and mark items found for collection, with full tracking. *(client request · MoM 10 Aug 2026, 4.6 AI Functions, Lost & Found, Reviews, Loyalty · DI-208)*

`WEB-035` Multi-Currency & Pricing

- Web screens carry: cart promo code (valid/invalid/expired) and empty basket with confirm; interrupted-payment recovery ("we are checking with your bank" → success/failed/unknown); reprint/resend tickets; UAE Pass sign-in, link guest checkout, sign out; support cases and Sahli handoff; FX rates with timestamp; remaining entitlements. *(agreed · design review 29 Sep 2026, GAP-B3 · B. Web — missing functions on existing screens · DI-1074)*
- A currency selector (AED, SAR, USD, INR, GBP) converts every displayed price. *(agreed · design review 29 Sep 2026, CFG-7 · Currency (AED/SAR/USD/INR/GBP) · DI-1071)*
- Foreign-currency display: an approximate conversion at a back-office rate so the guest sees roughly what they pay while settling in base currency, and/or full DCC at the gateway where the guest is charged in their own currency; records always in the venue base currency. *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-211)*

`WEB-036` F&B – Browse & Order

- In takeaway, delivery and café menus, Add opens a side panel for the dish: choose-one options (spice level, drink size, ice), optional priced add-ons (sides, dips, toppings, leave-outs) and quantity; total updates live and the basket line lists the choices. Shown whenever the item has modifier groups (no toggle). *(agreed · rev 3 design review 29 Sep 2026, REV3-9 · 9. Add-ons and modifiers for F&B menu items · DI-1050)*
- Dining deposit hold is a venue option, off unless enabled in Venue Management; amount and basis (per guest, per table, percentage) are venue configuration, never a hard-coded AED 100. Show the deposit step only when enabled. *(agreed · rev 3 design review 29 Sep 2026, REV3-8b · 8. deposit hold flow · DI-1049)*
- Table reservations and the waitlist do not go into the cart: after date, time and party size the guest gets a confirmation straight away ("no card needed"). *(agreed · rev 3 design review 29 Sep 2026, REV3-8 · 8. Unable to complete the table booking flow · DI-1048)*
- Delivery basket shows the fee (AED 15, free from AED 200) and "Add AED X more for free delivery"; below AED 90 checkout is refused; outside Dubai shows "We don't deliver to this address" with Change address / Switch to takeaway. A slot can close mid-flow: "That time just filled". *(agreed · design review 29 Sep 2026, 5. Takeaway and delivery (WEB-036) · DI-1039)*
- On the one-decision-per-screen layout, information blocks (notes, "what happens next", "what's included") stay on the screen before them and up to three quick choices share one screen. Table reservation and deposit hold become 1 screen; waitlist, takeaway, delivery, private dining enquiry 2; dinner deals 2 (party size with date/time). *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): Steps with nothing to decide · DI-1001)*
- **Open question.** Resources: meeting-room booking (headcount, duration, time slot, room, add-ons tea/coffee/snacks), modelled on House of Wisdom. Merchandise: browse, cart with add/remove quantity, pickup or doorstep delivery. F&B: outlet/menu browsing; collect at counter, curbside, doorstep or priority delivery. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Resources, Merchandise, F&B) · DI-690)*
- **Open question.** Dining has two flows: book a table (date, time, group size, seating-area preference, occasion, allergy/special-request notes) and order food (delivery or pickup location, items, checkout). *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Dining) · DI-688)*
- Decision (raised by Aishwarya): F&B and retail/merchandise online sale are optional back-office-enabled modules; where enabled, the whole purchase (browse, cart, checkout, pickup-at-venue or ship-to-guest) completes inside TICVAI — guests are never sent to download a separate app. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-505)*
- Out of scope: buying F&B with no admission ticket (entering only to buy food). *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-292)*
- Seated events: guest chooses pickup or delivery to seat (seat known from the booking). Open venues (beach, water park): a physical QR at each seat/location is scanned to say where food is delivered. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-288)*
- F&B: browse outlets and order; pickup location shown automatically per outlet, with delivery as an extra option (needs guest location) when the venue uses the platform's F&B module. Retail follows the same pickup/delivery model. *(client request · MoM 10 Aug 2026, 4.4 Venue Map, Queueing, F&B, Retail & Parking · DI-205)*

`WEB-037` Menu Item Detail

- In takeaway, delivery and café menus, Add opens a side panel for the dish: choose-one options (spice level, drink size, ice), optional priced add-ons (sides, dips, toppings, leave-outs) and quantity; total updates live and the basket line lists the choices. Shown whenever the item has modifier groups (no toggle). *(agreed · rev 3 design review 29 Sep 2026, REV3-9 · 9. Add-ons and modifiers for F&B menu items · DI-1050)*
- Modifiers can be free or chargeable with minimum/maximum selection rules; combo meals support component selection with upgrade options at additional cost. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-328)*

`WEB-039` Venue Map & Wait Times

- A visual venue map highlights long-queue rides vs low-queue alternatives so operations can redirect guests, e.g. a notification suggesting a nearby ride with a shorter wait. *(client request · MoM 7 Sep 2026, 4.17 AI guest flow optimization · DI-682)*
- In the app a guest with a valid ticket browses rides, sees the current wait (e.g. 60 minutes), joins the virtual queue for their party and gets a return window (e.g. 4:50-5:00 PM). Missing the window can auto-release the slot. *(client request · MoM 7 Sep 2026, 4.13 Virtual Queue - Mobile Journey & Configuration · DI-675)*
- Live wait time per ride/attraction shown in the app (e.g. "41 minutes"), fed by the venue's third-party camera/sensor system through a TICVAI API. *(agreed · MoM 10 Aug 2026, 4.4 Venue Map, Queueing, F&B, Retail & Parking · DI-204)*
- **Open question.** Customisable venue map showing attractions, dining, retail and restrooms. Qossai: define image/format guidance for tenant map uploads; benchmark is the Kidzania app's interactive 3D-style map. Final guidance still open. *(open · MoM 10 Aug 2026, 4.4 Venue Map, Queueing, F&B, Retail & Parking · DI-203)*

`WEB-040` Virtual Queue

- Proactively upsell an express/fast-lane ticket to a guest facing a long wait (e.g. "buy express ticket for [amount]"). *(agreed · MoM 7 Sep 2026, 4.17 Revenue lever / 5. Key Decisions · DI-683)*
- The return time shown to a VQ guest must be genuinely accurate and recalculate dynamically from real-time conditions across all three tiers, not a static estimate given at booking. *(agreed · MoM 7 Sep 2026, 4.15 Waiting-time honesty & recalculation · DI-679)*
- In the app a guest with a valid ticket browses rides, sees the current wait (e.g. 60 minutes), joins the virtual queue for their party and gets a return window (e.g. 4:50-5:00 PM). Missing the window can auto-release the slot. *(client request · MoM 7 Sep 2026, 4.13 Virtual Queue - Mobile Journey & Configuration · DI-675)*

`WEB-041` Parking – Reserve & Pay

- Parking is barrier integration, not space counting: one configuration screen chooses a model - no integration (TICVAI QR checked by security), ANPR (guest enters a plate at checkout, pushed to the barrier whitelist) or QR handoff to the barrier. Pay-per-hour parking is out of scope. *(agreed · MoM 14 Aug 2026, 10 · DI-316)*
- Parking supports three models: (1) no integration — TICVAI QR verified manually by security; (2) plate number at checkout pushed to the parking system's ANPR whitelist; (3) TICVAI QR passed to the barrier. Hourly pay-on-exit parking stays on the parking system's own POS. *(agreed · MoM 14 Aug 2026, 10. Parking Integrations · DI-300)*

`WEB-042` Retail & Shop and Drop

- Decision (raised by Aishwarya): F&B and retail/merchandise online sale are optional back-office-enabled modules; where enabled, the whole purchase (browse, cart, checkout, pickup-at-venue or ship-to-guest) completes inside TICVAI — guests are never sent to download a separate app. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-505)*
- Once a delivery address is entered, the applicable shipping fee is shown automatically for the customer to accept before payment. *(client request · MoM 19 Aug 2026, 4.8 Online Order Fulfilment & Shipping Configuration · DI-360)*
- Online retail offers buy-online-pickup-in-store and buy-online-ship-to-address. Shipping fees are set by region/city (e.g. Dubai, Abu Dhabi, international); decision: operations enter courier rates and margins manually, no live courier-API integration at this stage. *(agreed · MoM 19 Aug 2026, 4.3 Pricing, Bundles & Promotions; 4.8 Online Order Fulfilment & Shipping Configuration · DI-359)*
- F&B: browse outlets and order; pickup location shown automatically per outlet, with delivery as an extra option (needs guest location) when the venue uses the platform's F&B module. Retail follows the same pickup/delivery model. *(client request · MoM 10 Aug 2026, 4.4 Venue Map, Queueing, F&B, Retail & Parking · DI-205)*

`WEB-043` Loyalty & Rewards

- Gamification shows badges/status tiers (e.g. Explorer, Adventurer, Legend) earned by spend or engagement thresholds, feeding the loyalty tier structure. *(client request · MoM 20 Aug 2026, 4.9 Surveys & Gamification · DI-392)*
- **Open question.** Loyalty accrues points by product/spend tier (e.g. bronze/silver/gold thresholds) and unlocks tier benefits (e.g. platinum-tier discounts on F&B and ticketing). Full programme configuration (tiers, points, redemption, expiry) pending a dedicated session. *(open · MoM 20 Aug 2026, 4.5 Loyalty, Membership & Wallet · DI-382)*

`WEB-044` AI Concierge – Home

- The concierge (Sahli) shows as mascot art or as a plain button; setting "Concierge mascot", default on. *(agreed · design review 29 Sep 2026, CFG-5 · Sahli mascot (on/off) · DI-1069)*
- The AI chat box answers guided/predefined queries (booking status, rescheduling) and logs guest conversation history across channels (WhatsApp, web, Instagram, Facebook) with per-channel conversion attribution. *(client request · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-388)*
- AI concierge answers natural-language guest questions (ticketing, F&B, retail, venue info, timings) grounded in the venue's configured data. *(client request · MoM 10 Aug 2026, 4.6 AI Functions, Lost & Found, Reviews, Loyalty · DI-207)*
- **Open question.** AI concierge chat design is deferred until a dedicated AI workshop settles the technical approach (third-party LLM with PII masking) and the token/billing model. *(open · MoM 10 Aug 2026, 4.2 AI Concierge Chat — Open Item · DI-195)*

`WEB-045` Help Centre & Accessibility

- Duplicate screens become one implementation covering several screen IDs (mobile Transfer + Delivery & Sharing; web Wishlist / Devices & Consent; Help Centre + Help & Accessibility as one Help view with FAQ, cases, policies, accessibility tabs). Ticket-selection functions belong on GST-008. Web gets a Group Booking view. *(agreed · design review 29 Sep 2026, GAP-D3 · D. Duplicate screens merged; group booking on web · DI-1078)*
- The guest Help screen shows app status and a public, localised "what's new" (release notes). *(agreed · design review 29 Sep 2026, GAP-B2 · B. Help: app status + recent changes · DI-1073)*
- Custom content pages per venue (e.g. "Plan Your Visit", Accessibility) that follow accessibility guidelines. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-190)*

`WEB-046` In-Venue Notifications

- The in-venue notifications feed is needed in the first release on web and mobile (R242 deferral reversed). *(agreed · design review 29 Sep 2026, GAP-C1 · C. Wave 2: In-Venue Notifications · DI-1075)*
- A visual venue map highlights long-queue rides vs low-queue alternatives so operations can redirect guests, e.g. a notification suggesting a nearby ride with a shorter wait. *(client request · MoM 7 Sep 2026, 4.17 AI guest flow optimization · DI-682)*

`WEB-047` Map Booking — Cabanas & Spots

- The table/cabana screen becomes map-based booking: a venue map can carry cabanas, loungers, tables (beach or event tables) and other bookable resources, sold like cabanas. Dining tables stay F&B table reservations. *(agreed · design review 29 Sep 2026, GAP-C2 · C. Wave 2: Reserve a Table or Cabana (waitlist, notify) · DI-1076)*
- Cabanas are picked on the venue's ingested map, like stadium seats: numbered cabanas by zone (e.g. R01–R10, T01–T08, S01–S06, B01–B10) showing guests seated, sold-out greyed and marked. Tapping one adds it (e.g. "Cabana B09 · Large cabana · Beach, AED 1,855") and starts a remaining-time counter. Map on the first screen. *(agreed · rev 3 design review 29 Sep 2026, REV3-15 · 15. Book the product from the map (e.g. pick an available cabana) · DI-1055)*
- Map-based cabana booking stays optional per configuration, since not every operator uses the same flow; it uses the same map back end as theme-park F&B/locations (reusable later for in-park navigation). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W6 Cabanas · DI-1008)*
- **Open question.** Cabanas: category (premium, VIP, luxury, private, family, couples), date/time, guest count, amenity details. Activities: desert-safari packages (buy-one-get-one, evening, Bedouin-style), pickup point, add-ons (stroller), duration packages (2-hour/4-hour). *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Cabanas, Activities) · DI-687)*

`WEB-048` Book a Space by the Hour

- Meeting rooms by the hour are in scope: date → start time → length (1 hour, 2 hours, half day, full day) → room (focus pod, majlis room, boardroom, auditorium) → attendees → add-ons (coffee break, working lunch, AV technician). Price = room rate × length; the cart line shows the booked time window. *(agreed · rev 3 design review 29 Sep 2026, REV3-13 · 13. House of Wisdom: meeting room flow · DI-1053)*
- Cleaning buffer is configurable. Option A: fixed buffer (e.g. 15 min) after every booking. Option B: N cleanings per day; the system places the buffers into the day's schedule and adjusts availability. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W10 Meeting-room cleaning buffer · DI-1012)*
- Meeting-room availability is checked against date + start time + duration together; changing any of the three re-checks all rooms. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W9 Meeting rooms · DI-1011)*
- **Open question.** Resources: meeting-room booking (headcount, duration, time slot, room, add-ons tea/coffee/snacks), modelled on House of Wisdom. Merchandise: browse, cart with add/remove quantity, pickup or doorstep delivery. F&B: outlet/menu browsing; collect at counter, curbside, doorstep or priority delivery. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Resources, Merchandise, F&B) · DI-690)*
- UX reference: House of Wisdom (Sharjah library) meeting-room/"pod" booking and tiered membership plans — a simple duration-based booking flow without fixed performances/time slots — to be reviewed by Chinmay/Aishwarya. *(client request · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 6. Open Items · DI-506)*
- A bookable resource such as a meeting room can be priced per hour: total price is calculated from the booked duration and the room is blocked for that window so no other guest can book it. *(client request · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A · DI-503)*
- Resources are one-to-one (dedicated to a booking) or shared (e.g. a meeting room with bookable pods, a vehicle across sequential slots); further sales are blocked once a shared resource's capacity/slot is full and reopened if a booking is cancelled. *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-496)*

`WEB-049` Transport — Route & Schedule

- **Open question.** Should each popular-route card's starting fare, featured order and image or badge be set per route in the back office? Default built: routes carry a featured order and an image; the starting fare is computed from the lowest fare. *(open · Decisions Register 1 Oct 2026, Questions for the client — Transport / Popular routes card · DI-1119)*
- Transport "Popular routes" card view: cards per route (e.g. Dubai to Abu Dhabi, Sharjah to Dubai, Abu Dhabi to Al Ain, Dubai to Fujairah) styled like the dated ticket cards, each with the "from" fare and a Book button. Book → date → departures → passengers. On mobile it is the first transport product. *(client request · design review 30 Sep 2026, 6. Proposed UI: route cards with a Book button · DI-1111)*
- Transport passengers appear only after a departure is chosen (performance first, then tickets). *(client request · design review 30 Sep 2026, 5. Transport: route already chosen, but stations were empty · DI-1110)*
- A route flow opens with its stations filled in (e.g. Abu Dhabi Central Bus Station → Al Ain Central Bus Station, still changeable/swappable) and departures show straight away without Search Trips. Time-period buttons act as a filter; tapping one again shows all departures. *(client request · design review 30 Sep 2026, 5. Transport: route already chosen, but stations were empty · DI-1109)*
- Transport (intercity coach) follows the RTA layout: "3 Simple Steps" (Route & Schedule → Seat Selection → Payment), tabs One-way Trip / Multi-Trip / Favourite, one row with From (swap), To, Date & Time, Passengers; departure cards (arrival, duration, seats left, fare); price card beside a street map of the route. *(agreed · rev 3 design review 29 Sep 2026, REV3-21 · 21. Sell transport tickets (one trip, multi trip, favourites, stations, route map) · DI-1061)*

`WEB-050` Plan Your Visit

- A preference a day's park cannot meet is said, not filled: a "Not at this park" banner per day names the cuisine or shop and the park that has it (e.g. "No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2)."), hidden when all are met. Lunch cuisine options name the parks serving them ("Indian - Summit Peaks only"). *(agreed · MoM 30 Sep 2026, 4.7 · DI-1113)*
- Allam: multi-venue visit planner. In a multi-venue tenant the guest picks a park per chosen day ("Which park each day?", hidden otherwise); each day tab names its park and every item, swap candidate and AI-planner suggestion comes only from that park's rides, dining and shops, never another park's. *(agreed · MoM 30 Sep 2026, 4.7 · DI-1112)*
- Retail/kiosk shops are added to the planner's venue-linked options alongside F&B (previously only F&B). *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1100)*
- Allam: the planner applies multi-venue intelligence; it checks actual venue-level amenities before including a preference, e.g. if only one of several parks has an Indian restaurant. It pulls only rides, F&B and retail available at each specific venue. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1099)*
- Itinerary planner (Yas Island planner reference): party composition (adults/children with height/age), visit dates, pace (packed/balanced/relaxed) and cuisine preferences feed an auto-generated, swappable multi-day itinerary with associated costing. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1098)*
- "Plan Your Adventure": guided itinerary planner (Skidata benchmark) where the guest picks which rides/attractions and in what order ahead of time, tied to the ticket purchase and saved as a personal visit profile. *(client request · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-217)*
- Custom content pages per venue (e.g. "Plan Your Visit", Accessibility) that follow accessibility guidelines. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-190)*

## P02 Guest App

**Platform-wide**

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

**Account & Self-Service**

- Decision: profiles are never merged automatically. Likely duplicates are notified to the customer (push or e-mail) and merge only on the customer's confirmation; an admin review queue tracks flagged duplicates independently of the customer's response. *(agreed · MoM 20 Aug 2026, 4.2 Duplicate Detection; 5. Key Decisions · DI-377)*

**Booking & Selection**

- A "save and finish later" option retains an in-progress order locally. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1094)*
- Each ticket type gets its own flow: open-dated (no calendar step, straight to guest category/quantity, valid e.g. 30-60 days), dated (date, then product), dated-with-time (date, time, product) and seated (date, time, seat selection). *(client request · MoM 18 Sep 2026, 4.13 Guest Website UX Review — Ticket Type Flows & Seat Map Selection · DI-948)*
- **Open question.** Movies: language/screen type (e.g. English, Dolby Atmos), cinema and showtime, seats, concession add-ons. Theme park: ticket-type list, guest categories (adult/child/senior/infant/people of determination with companion), per-ticket guest-name capture driven by quantity. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Movies, Theme park) · DI-686)*
- Decision: season-pass/family-type products capture first and last name for each individual pass holder (not just the purchaser), via an "add guest name" step. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-429)*
- Decision: the B2C checkout shows a clear, visible step indicator — Ticket Selection → Add-ons → My Cart → Checkout. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-426)*
- Reference checkouts: Six Flags-style (product → quantity/name capture → cart summary → login/guest checkout with dual OTP validation) and Platinum List (event → date → colour-coded interactive seat map → seats → one-page checkout via Quick Order/Apple/Google, as few as four clicks, optional post-purchase profile prompt). *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-398)*
- **Open question.** Two selection patterns: (a) event, date, time, see availability, then product; (b) product, quantity, date, then only time slots with enough capacity. How many customization scenarios to support needs deeper UI exploration. *(open · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-118)*
- Navigation depends on ticket type: admission has no date/time and goes straight to quantity/cart; dated asks date only; timed asks date then time; seated asks date, then time, then seat. *(agreed · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-116)*

**Cart & Checkout**

- A "save and finish later" option retains an in-progress order locally. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1094)*
- Ticket attributes such as minimum age, ID-proof requirements (e.g. Emirates ID for UAE-resident tickets, with format validation or photo upload; passport; handicap/PoD documentation) or an embedded ID-reader for on-site verification are configurable per ticket and region, not fixed. *(agreed · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference; 5. Key Decisions · DI-443)*
- Guest information capture (name, mobile number, nationality, visit survey, etc.) is configurable per ticket type; even an open-dated admission ticket can optionally collect it. *(agreed · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough; 5. Key Decisions · DI-434)*
- Decision: season-pass/family-type products capture first and last name for each individual pass holder (not just the purchaser), via an "add guest name" step. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-429)*
- Decision: the B2C checkout shows a clear, visible step indicator — Ticket Selection → Add-ons → My Cart → Checkout. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-426)*
- Reference checkouts: Six Flags-style (product → quantity/name capture → cart summary → login/guest checkout with dual OTP validation) and Platinum List (event → date → colour-coded interactive seat map → seats → one-page checkout via Quick Order/Apple/Google, as few as four clicks, optional post-purchase profile prompt). *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-398)*

**Discovery & Browse**

- "Help me choose" (experience builder) is not a consent step: its questions (yes/no, age, certified or not, etc.) filter the catalogue so only suitable products are shown (Deep Dive Dubai reference). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W4 Help me choose · DI-1005)*

**Screen by screen**

`GST-001` Home

- The landing page offers selectable scroll animations (venue choice). *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1088)*
- Multi-location attractions: the guest picks a location first (e.g. Al Barsha, Mirdif, Yas Island, Sharjah); a "Booking at" bar on later booking steps has Change location. On a switch, times and prices refresh and the selection is cleared unless the products share a family. Setting "Location switcher". *(agreed · rev 3 design review 29 Sep 2026, REV3-18 · 18. One tenant with an attraction in several locations; change location · DI-1058)*
- Home / Discover is a venue overview: description, opening hours and types (rides, dining, events, shops); one or two sample items per type are enough. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1018)*
- The B2C home page lists the ticket categories directly; clicking one opens its counters on the same screen. *(client request · design review 23 Sep 2026, Tickets 8. Show the single day ticket category on the B2C home page · DI-977)*
- **Open question.** Open: component-count logic for the experiences/dining section on the guest-app landing page — fixed 2–3-card layout vs. a scalable N-count layout. Owner Aishwarya; to confirm with Allam's team. *(open · MoM 20 Aug 2026, 4.10 CMS & White-Label; 6. Open Items · DI-396)*
- Guest app home: logo, banner and category tabs Tickets, What's On, Plan Your Visit, Map. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-196)*

`GST-002` Explore

- Category tiles (e.g. Permanent exhibition, Temporary exhibitions, Guided tours, Courses & workshops), then that category's tickets with Adult / Child / Student counters. Setting "Ticket categories": Category → subcategory (default) or Flat list (all tickets under category headings). *(agreed · rev 3 design review 29 Sep 2026, REV3-16 · 16. Choose category, then subcategory, configurable in the CMS · DI-1056)*
- Home / Discover is a venue overview: description, opening hours and types (rides, dining, events, shops); one or two sample items per type are enough. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1018)*
- Explore cards play the product's own short clip muted in place, and show the primary image otherwise. *(agreed · MoM 17 Sep 2026, M17-10 · DI-921)*
- Purchase flow: categories (Attractions, Exhibitions, Events, Dining, Shops, Experiences) → ticket selection (from back-office config) → date/time slot → add-ons (per ticket type or generic) → review & pay → confirmation. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-197)*

`GST-003` Buy Tickets

- Category tiles (e.g. Permanent exhibition, Temporary exhibitions, Guided tours, Courses & workshops), then that category's tickets with Adult / Child / Student counters. Setting "Ticket categories": Category → subcategory (default) or Flat list (all tickets under category headings). *(agreed · rev 3 design review 29 Sep 2026, REV3-16 · 16. Choose category, then subcategory, configurable in the CMS · DI-1056)*
- Card layout is a choice, not free text: Stacked rows (default) · Split rows · Cards across · Poster cards. Card size: Compact (default) · Standard · Large · Extra large. Density: Compact (default) · Standard · Roomy. *(agreed · design review 29 Sep 2026, 6. Booking-flow configuration (CMS-016): card-layout options · DI-1040)*
- Read more opens with the ticket's video or photo, and every ticket in a listing has its own photo (product media: images and videos, one primary). *(agreed · design review 29 Sep 2026, Tickets 4. Video or image should show · DI-1026)*
- CMS option to list a product (e.g. training courses) with full details but no Book button; instead show "Contact sales to book" with contact details. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W3 View-only products · DI-1004)*
- Experience venues list each experience directly (e.g. author talk, calligraphy workshop, story hour, rooftop reading night), each with its own date, time and tickets; no category step. *(client request · rev 3 design review 25 Sep 2026, 12. Experience flow: show the product directly, not the ticket category · DI-999)*
- Show the ticket categories (e.g. Single day, Two-day flexible, UAE resident) directly; no intermediate "Dated day pass" step. *(client request · design review 23 Sep 2026, Tickets 7. Show the ticket category directly instead of Dated Pass -> Single Day Pass · DI-976)*
- Allam's UX benchmark (Little Explorer, Dubai): multi-location selector, a horizontal near-term date picker with full-calendar fallback, and tabbed browsing (passes / workshops / packages) on one page rather than multiple screens. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-585)*
- Decision: ticket types are browsed in-page, not across multiple pages; "View all ticket types" expands additional categories in place. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-427)*
- Purchase flow: categories (Attractions, Exhibitions, Events, Dining, Shops, Experiences) → ticket selection (from back-office config) → date/time slot → add-ons (per ticket type or generic) → review & pay → confirmation. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-197)*
- Qossai liked a pattern using product video rather than static images for tickets. *(client request · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-127)*

`GST-004` Item Detail

- Qossai: ride/attraction detail pages play the video directly, with no loading screen in front of it; an info button reveals ride details and plays the video. Chinmay agreed to remove the loader. *(agreed · MoM 30 Sep 2026, 4.8 Mobile App — In-Ride Video/Info & In-Park Navigation · DI-1101)*
- Item detail shows a gallery, the item's location on the 2D/3D map and proposes the relevant product, e.g. a restaurant offers "Buy meal combo", which automatically adds the required admission ticket (checkout in about 3 steps). *(agreed · design review 29 Sep 2026, Mobile app (v4) — Item detail: map location and relevant product (meal combo includes admission) · DI-1082)*
- Clicking a ticket opens the Adult / Child / Senior / Infant counters in a side panel on the same listing or details screen (no separate "Select Tickets" step); the panel is open by default on the listing and Book goes straight into the booking. *(agreed · design review 29 Sep 2026, Tickets 5. Clicking Dated Day Pass should show the tickets on the same screen · DI-1027)*
- Read more opens with the ticket's video or photo, and every ticket in a listing has its own photo (product media: images and videos, one primary). *(agreed · design review 29 Sep 2026, Tickets 4. Video or image should show · DI-1026)*
- Ticket cards, Read more and the listing side panel show tags (e.g. "2 Hours", "Min 1.10 m", "Free adult entry", "Valid 90 days", "Emirates ID"), each with a kind icon (clock, height, free, calendar, id), max 6. Venue-set tags win, else derived from duration, validity, height rule. Setting "Tags on tickets", default on. *(agreed · design review 29 Sep 2026, Tickets 3. 'Read more' should carry tags customisable per ticket type · DI-1025)*
- Item detail shows the item's location on the map and proposes the relevant product, e.g. restaurant -> "Buy meal combo", which automatically adds the required admission ticket (checkout in ~3 steps). *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1019)*
- CMS option to list a product (e.g. training courses) with full details but no Book button; instead show "Contact sales to book" with contact details. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W3 View-only products · DI-1004)*
- Show the ticket categories (e.g. Single day, Two-day flexible, UAE resident) directly; no intermediate "Dated day pass" step. *(client request · design review 23 Sep 2026, Tickets 7. Show the ticket category directly instead of Dated Pass -> Single Day Pass · DI-976)*
- Qossai and Allam: product pages should include short video content (e.g. a 10-15 second clip), not only static images, to give a sense of the actual experience (e.g. a ride) before booking. *(agreed · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-917)*
- Product cards/pages carry short descriptions with an expandable "view more details" control and a configurable hero image or video per product. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-425)*
- Qossai liked a pattern using product video rather than static images for tickets. *(client request · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-127)*

`GST-006` Item Detail – Event / Exhibition

- Platinum List reference: event page with short video + image + description → select tickets → calendar collapsed to a week view, expandable to full month → time-slot selection. *(client request · MoM 21 Aug 2026, 4.1 Reference Walkthrough — Platinum List Seat Selection & Checkout Journey · DI-408)*
- Qossai liked a pattern using product video rather than static images for tickets. *(client request · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-127)*

`GST-007` Select Date & Time

- **Open question.** Is the swim vest an add-on product, and is the splash-and-river pass a separate product offered only to non-swimmers? Default built: the swim answer filters products (as Help me choose); the vest is an add-on; the splash-and-river pass is its own product. *(open · Decisions Register 1 Oct 2026, Questions for the client — Guest safety / Swim ability · DI-1118)*
- The water-park swim answer changes the offer: All of us = full ride list at standard prices; Some of us = ride notes change and a "Swim vests needed" counter appears; None of us = tickets switch to a cheaper splash and river pass, slides removed from ride notes. The swim pop-up is not shown where the question is on the page. *(client request · design review 30 Sep 2026, 4. Swim ability and height gate: the answer changed nothing · DI-1108)*
- Picking a surf session adds nothing to the cart. Then "Tickets for Intermediate surf · 19:30" shows Surfer (session price), Junior surfer 10–15 and Spectator (AED 35); items reach the cart only when a quantity is set. Before a session: "Choose a session above to see its tickets and prices." *(client request · design review 30 Sep 2026, 3. Surfing session added to the cart straight away · DI-1107)*
- The mobile booking flow (date/day-pass selection, quantity, cross-sell, sign-in) is functionally identical to the web app. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1092)*
- Swim ability is a consent question a venue attaches to a product or flow (e.g. "Are you able to swim?", "Do you hold a scuba certification?", "I accept the risk"), each with its own text and per-person or once-per- booking setting. Shown as a pop-up in the venue's theme after session/date; answers recorded. *(agreed · rev 3 design review 29 Sep 2026, REV3-26 · Built to match your examples: Swim question (water park) · DI-1062)*
- On a guest's first booking visit, a four-step coach-mark tour highlights date, time, tickets and basket, with Back, Next / Done and End tour; a "Quick tour" button on the booking page replays it. Setting "Quick tour", default off; first-visit flag kept on the device only. *(agreed · rev 3 design review 29 Sep 2026, REV3-20 · 20. Enable or disable a Quick Tour that describes the customer journey · DI-1060)*
- Multi-location attractions: the guest picks a location first (e.g. Al Barsha, Mirdif, Yas Island, Sharjah); a "Booking at" bar on later booking steps has Change location. On a switch, times and prices refresh and the selection is cleared unless the products share a family. Setting "Location switcher". *(agreed · rev 3 design review 29 Sep 2026, REV3-18 · 18. One tenant with an attraction in several locations; change location · DI-1058)*
- The guest picks a tour language (e.g. English, العربية, Français, Deutsch, 中文, Русский) and only tours in that language are listed. Cinema performances show language and format (2D/3D/subtitled) to pick from. *(agreed · rev 3 design review 29 Sep 2026, REV3-17 · 17. Guided tour times based on the tour language · DI-1057)*
- Theatre has its own auditorium seat map: stage (or screen for cinema) at front, Stalls/Circle/Balcony with curved rows, aisles and Premium/Standard/Economy pricing. Date, time, show (plus language & format for cinema) and the seat map sit on one page. Seats per guest booking default 10 (venue setting); basket lists each seat. *(agreed · rev 3 design review 29 Sep 2026, REV3-7 · 7. Theatre flow should be similar to the stadium flow · DI-1047)*
- Seated events with one on-sale performance go straight to the seat map (Flow 1). Otherwise date and time come first (Flow 2), either as an inline step (timed-ticket style, default) or as a pop-up dialog over the seat map. Setting "Date & time on seat events". *(agreed · rev 3 design review 29 Sep 2026, REV3-4 · 4. Flow 1 (fixed date and time) and Flow 2 (select date, then time, then seat map) · DI-1044)*
- Dated flows reveal in order: date, then time (hidden until a date is picked), then tickets (hidden until a time is picked), with a hint in place telling the guest what to pick next; Continue off until both chosen. Setting "Performance reveal": Date → time → ticket (default) or All at once. *(agreed · rev 3 design review 29 Sep 2026, REV3-2 · 2. Step 1 date, step 2 time (only after the date), step 3 ticket · DI-1042)*
- More than eight times show as compact time tiles, paged with Earlier / Later (Times per page 8/12/24/all, default 24), with day-part chips (All, Morning, Afternoon, Evening) showing counts (filter on by default). Day-part boundaries are venue settings, default before 12:00 / 12:00–17:00 / from 17:00. *(agreed · rev 3 design review 29 Sep 2026, REV3-1 · 1. Many performances should resize and page; filter by morning, afternoon, evening · DI-1041)*
- On leaving selection (rides, water slides, kids club), each person declares an age band and height band; toggles only where needed (confident swimmer; guardian signature for 12–15). Per-person "Can't take part: too short, needs an adult" with Remove this guest / Choose another activity; Continue locked until all qualify. *(agreed · design review 29 Sep 2026, 3. Height and age check (WEB-006) · DI-1037)*
- Guided tours/sessions confirmed: date, then language, then time slot. Sessions come from configuration; the slot grid reflows when there are many slots. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W11 Guided tours / sessions · DI-1013)*
- Museum workshops: after Help me choose, the guest selects the workshop first, then date/time; only relevant products are shown. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W8 Workshops (museum) · DI-1010)*
- Surf sessions follow the time-selection pattern: products (beginner, intermediate...) appear only after a time slot is chosen. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W5 Surf sessions · DI-1007)*
- Guest date picking shows a strip of the next seven days (venue setting dateStripDays, default 7, range 3-31) with a calendar icon that opens the full month for later dates. *(agreed · MoM 17 Sep 2026, M17-08 · DI-920)*
- Date-change flow detects conflicts across an existing multi-ticket cart and lets the guest shift the whole booking to a new date in one action. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-587)*
- Allam's UX benchmark (Little Explorer, Dubai): multi-location selector, a horizontal near-term date picker with full-calendar fallback, and tabbed browsing (passes / workshops / packages) on one page rather than multiple screens. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-585)*
- Start/stop-sell per channel: e.g. a distant desert safari allows no same-day online booking (next day minimum), while onsite stays open to sell-out or a cutoff (e.g. 15 minutes before a timed show). Guest date/time pickers must reflect the channel's window. *(client request · MoM 31 Aug 2026, 4.11 Sales schedule & validity · DI-583)*
- Weekday/calendar rules give different validity and pricing to weekday-only vs. all-days products (e.g. Global Village). Blockout dates exclude some ticket types (e.g. memberships) on public holidays/special days, requiring a separate ticket for those dates. *(client request · MoM 25 Aug 2026, 4.5 Validity Management & Expiry Rules · DI-452)*
- Camping/lesson-based tickets: when buying a multi-lesson package (e.g. ski or snowboard lessons on a regular schedule) the guest selects the specific class dates/performances. *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-449)*
- Time-slot (performance) tickets configure early/late entry and an entry window (e.g. from 30 minutes before start until a cut-off). Multi-day tickets are consecutive-day or flexible within a range (e.g. any 3 days within a month). *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-447)*
- Kidiya family-pass example showed a dynamic-pricing calendar applied at ticket-type level (prices shown on the calendar per date). *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-430)*
- Platinum List reference: event page with short video + image + description → select tickets → calendar collapsed to a week view, expandable to full month → time-slot selection. *(client request · MoM 21 Aug 2026, 4.1 Reference Walkthrough — Platinum List Seat Selection & Checkout Journey · DI-408)*
- Purchase flow: categories (Attractions, Exhibitions, Events, Dining, Shops, Experiences) → ticket selection (from back-office config) → date/time slot → add-ons (per ticket type or generic) → review & pay → confirmation. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-197)*
- Some clients (e.g. museums with 5-6 standard configurations) start by asking the number of guests, which narrows the calendar to dates/times with sufficient availability. *(client request · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-117)*
- Seat assignment flow is "select time, then select seat", with the two steps on different screens. *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-057)*

`GST-008` Tickets & Add-ons

- **Open question.** Is the swim vest an add-on product, and is the splash-and-river pass a separate product offered only to non-swimmers? Default built: the swim answer filters products (as Help me choose); the vest is an add-on; the splash-and-river pass is its own product. *(open · Decisions Register 1 Oct 2026, Questions for the client — Guest safety / Swim ability · DI-1118)*
- The water-park swim answer changes the offer: All of us = full ride list at standard prices; Some of us = ride notes change and a "Swim vests needed" counter appears; None of us = tickets switch to a cheaper splash and river pass, slides removed from ride notes. The swim pop-up is not shown where the question is on the page. *(client request · design review 30 Sep 2026, 4. Swim ability and height gate: the answer changed nothing · DI-1108)*
- Picking a surf session adds nothing to the cart. Then "Tickets for Intermediate surf · 19:30" shows Surfer (session price), Junior surfer 10–15 and Spectator (AED 35); items reach the cart only when a quantity is set. Before a session: "Choose a session above to see its tickets and prices." *(client request · design review 30 Sep 2026, 3. Surfing session added to the cart straight away · DI-1107)*
- Guest counters take their price from the chosen park ticket and produce one line, e.g. "2 park ticket · Adult × 3 = AED 1,425" (no separate Adult × 3 line). Child and senior prices scale from the chosen ticket; infants free. *(client request · design review 30 Sep 2026, 2. Multi-park ticket adds an extra adult line · DI-1106)*
- The mobile booking flow (date/day-pass selection, quantity, cross-sell, sign-in) is functionally identical to the web app. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1092)*
- Duplicate screens become one implementation covering several screen IDs (mobile Transfer + Delivery & Sharing; web Wishlist / Devices & Consent; Help Centre + Help & Accessibility as one Help view with FAQ, cases, policies, accessibility tabs). Ticket-selection functions belong on GST-008. Web gets a Group Booking view. *(agreed · design review 29 Sep 2026, GAP-D3 · D. Duplicate screens merged; group booking on web · DI-1078)*
- Multi-location attractions: the guest picks a location first (e.g. Al Barsha, Mirdif, Yas Island, Sharjah); a "Booking at" bar on later booking steps has Change location. On a switch, times and prices refresh and the selection is cleared unless the products share a family. Setting "Location switcher". *(agreed · rev 3 design review 29 Sep 2026, REV3-18 · 18. One tenant with an attraction in several locations; change location · DI-1058)*
- Dated flows reveal in order: date, then time (hidden until a date is picked), then tickets (hidden until a time is picked), with a hint in place telling the guest what to pick next; Continue off until both chosen. Setting "Performance reveal": Date → time → ticket (default) or All at once. *(agreed · rev 3 design review 29 Sep 2026, REV3-2 · 2. Step 1 date, step 2 time (only after the date), step 3 ticket · DI-1042)*
- Each Adult / Child / Senior / Infant row has an (i) button showing who the ticket is for and what it includes (up to 300 characters). Setting "Extra info on cards", default on. *(agreed · design review 29 Sep 2026, Tickets 6. Extra information for each ticket in the ticket section · DI-1028)*
- Clicking a ticket opens the Adult / Child / Senior / Infant counters in a side panel on the same listing or details screen (no separate "Select Tickets" step); the panel is open by default on the listing and Book goes straight into the booking. *(agreed · design review 29 Sep 2026, Tickets 5. Clicking Dated Day Pass should show the tickets on the same screen · DI-1027)*
- Ticket cards, Read more and the listing side panel show tags (e.g. "2 Hours", "Min 1.10 m", "Free adult entry", "Valid 90 days", "Emirates ID"), each with a kind icon (clock, height, free, calendar, id), max 6. Venue-set tags win, else derived from duration, validity, height rule. Setting "Tags on tickets", default on. *(agreed · design review 29 Sep 2026, Tickets 3. 'Read more' should carry tags customisable per ticket type · DI-1025)*
- Museum workshops: after Help me choose, the guest selects the workshop first, then date/time; only relevant products are shown. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W8 Workshops (museum) · DI-1010)*
- Surf sessions follow the time-selection pattern: products (beginner, intermediate...) appear only after a time slot is chosen. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W5 Surf sessions · DI-1007)*
- Add-ons appear only on the Add-ons / Extras step, never in the ticket panels. Each add-on appears once (no duplicates such as 'Large locker' on two steps). *(client request · design review 23 Sep 2026, Cart 11. Show add-ons only on the Add-ons / Extras page · DI-979)*
- **Open question.** Cabanas: category (premium, VIP, luxury, private, family, couples), date/time, guest count, amenity details. Activities: desert-safari packages (buy-one-get-one, evening, Bedouin-style), pickup point, add-ons (stroller), duration packages (2-hour/4-hour). *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Cabanas, Activities) · DI-687)*
- Reference details: sibling/multi-buy discount shown with a struck-through original price; workshop add-ons inline with theme/cuisine sub-selection feeding time-slot availability; a package builder for bundled experiences. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-586)*
- Decision (Qossai, Ski Dubai): instructor choice is a per-ticket-type setting — private-session products may let the guest pick a specific instructor; group-session products auto-assign without showing a choice. Private and group are separate, separately priced products (a private request on a group instructor is its own product). *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-504)*
- Quantity/purchase limits can be set per order, per guest, per account category and per sales channel (e.g. maximum 6 tickets per transaction). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-464)*
- Decision: the add-ons step is optional/removable in configuration for products with no add-ons, collapsing the flow to Ticket Selection → Cart → Checkout. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-428)*
- Decision: ticket types are browsed in-page, not across multiple pages; "View all ticket types" expands additional categories in place. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-427)*
- Product cards/pages carry short descriptions with an expandable "view more details" control and a configurable hero image or video per product. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-425)*
- Purchase flow: categories (Attractions, Exhibitions, Events, Dining, Shops, Experiences) → ticket selection (from back-office config) → date/time slot → add-ons (per ticket type or generic) → review & pay → confirmation. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-197)*
- Minimum/maximum sellable quantity per customer (e.g. a promotional bundle requiring at least two) must be enforced at selection. *(agreed · MoM 7 Aug 2026, 16. Entitlement Components: Re-entry, Expiration & Sale Restrictions · DI-172)*
- Some clients (e.g. museums with 5-6 standard configurations) start by asking the number of guests, which narrows the calendar to dates/times with sufficient availability. *(client request · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-117)*

`GST-009` Review & Payment

- Checkout completes in 4 steps, supporting Apple Pay/card payment, and adds the resulting ticket to Apple Wallet or Google Wallet. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1096)*
- The guest-checkout email pop-up collects only the fields configured in the back end (email, phone and/or name). After the code is verified, do not ask for name/email/phone again: go straight to T&Cs and complete the booking; profile is created and can be completed later (Platinumlist pattern). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W1 Guest checkout · DI-1002)*
- Marketing opt-in ("Send me offers and news") sits beside the T&Cs at checkout and is never pre-ticked. Open: whether a guest-checkout customer may be marketed on it; until confirmed it stays unticked and nothing is sent without it. *(agreed · MoM 18 Sep 2026, M18-15 · DI-954)*
- Checkout captures marketing/newsletter opt-in and preferred contact method (email vs phone). *(client request · MoM 1 Sep 2026, 4.13 Privacy Consent & Cookie Policy · DI-616)*
- Fees are separate from taxes: e.g. a call-center convenience fee, or a shipping fee varying by destination (Dubai, Abu Dhabi, Ras Al Khaimah, international) calculated from the checkout address; applied at transaction, item or ticket level. Checkout must show the fee once the address is entered. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-597)*
- Support both redirect to the gateway's hosted page and embedded/iframe capture (card, Apple Pay, Tabby) on the platform's own checkout preserving its look and feel, for Network International and Stripe; embedded needs extra security certification to reassure guests. *(agreed · MoM 31 Aug 2026, 4.13 Payment gateway approach · DI-589)*
- At checkout guests can sign in, register (with a visible loyalty-points incentive) or continue as guest; terms acceptance is implied by proceeding to payment, with no separate checkbox. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-588)*
- Date-change flow detects conflicts across an existing multi-ticket cart and lets the guest shift the whole booking to a new date in one action. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-587)*
- Waiver is triggered automatically when an associated product is bought; timing is business-configurable: at checkout, post-purchase, or on-site before entry. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-573)*
- Split tender: one purchase paid with wallet balance plus another method, e.g. AED 500 from the wallet and the remaining AED 200 of a AED 700 purchase on a credit card. *(agreed · MoM 27 Aug 2026, 4.7 Split-Tender, Redemption Rules & Configuration Simulation · DI-525)*
- Donation campaigns: fixed or variable amounts, enabled per sales channel, triggered on a specific product or across all products, proceeds tracked to a separate account code. *(client request · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies · DI-471)*
- Decision: seats held in a cart auto-release after a configurable timeout if checkout is abandoned, and immediately if a payment attempt fails. *(agreed · MoM 21 Aug 2026, 4.6 Seat Inventory Status; 5. Key Decisions · DI-422)*
- Platinum List reference seat step: interactive seat map colour-coded by price tier → seat selection with a live cart hold and countdown timer → checkout via Quick Order / Apple ID / Google ID. *(client request · MoM 21 Aug 2026, 4.1 Reference Walkthrough — Platinum List Seat Selection & Checkout Journey · DI-409)*
- Once a delivery address is entered, the applicable shipping fee is shown automatically for the customer to accept before payment. *(client request · MoM 19 Aug 2026, 4.8 Online Order Fulfilment & Shipping Configuration · DI-360)*
- **Open question.** Open: alongside curated pre-built packages, let guests build their own bundle in the cart, with the system detecting eligible combinations and applying an automatic discount (e.g. 5–10%). *(open · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-221)*
- Foreign-currency display: an approximate conversion at a back-office rate so the guest sees roughly what they pay while settling in base currency, and/or full DCC at the gateway where the guest is charged in their own currency; records always in the venue base currency. *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-211)*
- Purchase flow: categories (Attractions, Exhibitions, Events, Dining, Shops, Experiences) → ticket selection (from back-office config) → date/time slot → add-ons (per ticket type or generic) → review & pay → confirmation. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-197)*
- Per-ticket "ticket owner" details are captured separately from the "reservation owner" (buyer) and can enforce rules such as a minimum age per ticket holder. *(agreed · MoM 7 Aug 2026, 20. Live Point-of-Sale Transaction Walkthrough · DI-178)*
- Dynamic offers apply automatically without a code (buy-2-get-1-free, buy-3-get-2-at-50%-off, fixed amount off a minimum quantity); the discounted item is added to the cart automatically with its price adjusted (e.g. to zero). *(agreed · MoM 7 Aug 2026, 17. Promotions & Dynamic Offers · DI-174)*
- Custom fields gate purchase where configured — e.g. a checkbox confirming a guest is not pregnant before a specific product can be bought, or a weight-range field for an activity. *(agreed · MoM 7 Aug 2026, 6. Data Mask: Flexible Custom Data Capture · DI-156)*
- Qossai: the POS-style right-to-left slide-in drawer could also suit the B2C cart/checkout. *(client request · MoM 3 Aug 2026, 10. Reference Material & Design Research · DI-124)*
- Separate "ticket holder" (per-ticket details captured where required) from "reservation owner"/buyer (single contact captured once per booking who receives the tickets by email). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-122)*
- Apple Pay / Google Pay tap-to-pay are the primary regional digital payment methods; UPI-style QR payments may come later, not in initial scope. *(agreed · MoM 31 Jul 2026, 12. Payments & Regional Preferences · DI-079)*

`GST-010` Booking Confirmation

- Checkout completes in 4 steps, supporting Apple Pay/card payment, and adds the resulting ticket to Apple Wallet or Google Wallet. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1096)*
- Apple/Google Wallet configuration covers template design (background colour, header, footer) and the guest-facing "Add to Apple Wallet" flow after an online purchase. *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-609)*
- Ticket delivery: "Add to Wallet" (Apple or Google Wallet by device), and WhatsApp, SMS or email per the guest's chosen method, selectable at checkout/confirmation; tickets can also be emailed to a third party. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-198)*
- Purchase flow: categories (Attractions, Exhibitions, Events, Dining, Shops, Experiences) → ticket selection (from back-office config) → date/time slot → add-ons (per ticket type or generic) → review & pay → confirmation. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-197)*

`GST-011` Wallet Overview

- Peer-to-peer transfer from one guest's wallet to another guest's wallet; a configurable venue-level toggle (allowed or not), not a default feature. *(agreed · MoM 27 Aug 2026, 4.10 Transfers, Fraud/Risk Controls · DI-536)*
- Two variants: monetary gift card (value usable on anything the venue offers) and product-specific gift voucher (redeemable only for a named product, e.g. a dolphin-show voucher). Redemption channel is configurable: online, on-site or both. *(client request · MoM 27 Aug 2026, 4.9 Gift Cards, Vouchers & Wallet Payments · DI-533)*
- Balance can move between linked family/group wallets in either direction (parent to child, child to parent); a venue-controlled toggle, not always enabled. *(agreed · MoM 27 Aug 2026, 4.8 Shared wallet transfer · DI-532)*
- Guests can create family-member profiles themselves and set spending limits directly from their own guest account, in addition to venue-side configuration. *(agreed · MoM 27 Aug 2026, 4.8 Family, Parent-Child & Corporate Wallets · DI-530)*
- A parent's wallet funds linked child wristbands/wallets with per-child spending allowances, e.g. of a AED 500 family balance one child is capped at AED 200 and another at AED 200. *(agreed · MoM 27 Aug 2026, 4.8 Family, Parent-Child & Corporate Wallets · DI-529)*
- Consumption is fully automatic FEFO (nearest expiry first). Guests see their balance and the expiry breakdown per top-up lot in their profile but cannot choose which lot is drawn down; no lot picker at payment. *(agreed · MoM 27 Aug 2026, 4.6 Stored Value, Credit Consumption & FEFO Logic · DI-523)*
- Guests must be able to configure auto-reload and recurring funding schedules themselves in the guest web/app, not only venue admins in the back office. *(agreed · MoM 27 Aug 2026, 4.5 Funding / 5. Key Decisions · DI-519)*
- Top-up rules set minimum and maximum amounts per transaction; channel/funding-source mapping restricts which payment methods each channel offers (e.g. cash top-up on-site only, not online), so each channel's top-up screen offers only its allowed methods. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-517)*
- Ownership and access rules are configurable per wallet type. Family default: only the parent/guardian can top up; children can view balance and transactions and spend, but cannot top up unless permissions are explicitly reconfigured. Guest wallet screens must hide or disable top-up for members without the right. *(agreed · MoM 27 Aug 2026, 4.2 Wallet Ownership / 4.8 Family Permission Rules · DI-509)*
- Wallet type library: multiple wallet types (guest, family, membership wallet), each assigned to a category (individual, corporate, member). Provisioning rules set the trigger that creates a wallet (membership purchase, first top-up); two patterns: gift-card style (pre-defined value products listed on the website) and open-ended "add money to wallet". *(client request · MoM 27 Aug 2026, 4.2 Wallet Type Library, Ownership & Account Association · DI-508)*
- Referral rewards may be credited as currency/points directly into the guest's wallet (like Swiggy), in addition to discount vouchers — a business-configurable option. *(agreed · MoM 25 Aug 2026, 4.7 Entitlements & Access Control; 5. Key Decisions · DI-460)*
- A combo product can bundle admission with stored-value credit the guest draws down on F&B or retail purchases (wallet mechanics in a dedicated session). *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-459)*
- Wallet balance is shared across a linked family — a parent's top-up can be drawn down by a linked child's wristband without a separate top-up. *(agreed · MoM 20 Aug 2026, 4.1 CRM; 4.5 Loyalty, Membership & Wallet · DI-374)*
- Guest profile shows gift vouchers and a stored-value "money card"/wallet; "My Tickets" (all tickets) is separate from "My Reservations" (bookings holding one or more tickets) with reservation details and date modification. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-199)*

`GST-012` My Tickets

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

`GST-013` Ticket Details

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

`GST-014` Ticket Transfer

- Duplicate screens become one implementation covering several screen IDs (mobile Transfer + Delivery & Sharing; web Wishlist / Devices & Consent; Help Centre + Help & Accessibility as one Help view with FAQ, cases, policies, accessibility tabs). Ticket-selection functions belong on GST-008. Web gets a Group Booking view. *(agreed · design review 29 Sep 2026, GAP-D3 · D. Duplicate screens merged; group booking on web · DI-1078)*
- A purchased ticket can be transferred to another guest (e.g. a friend); the system keeps the original purchaser and full transfer history. *(client request · MoM 7 Sep 2026, 4.9 Ownership and transfer · DI-669)*
- Once activated in the app a digital ticket is bound to one approved device; moving to a new device requires deactivating the prior binding. Credential transfer moves a ticket to another person's device and invalidates the original holder's copy. *(client request · MoM 2 Sep 2026, 4.8 Device Binding, Credential Transfer & Revocation · DI-636)*
- Ticket transfer by email/SMS with optional message; either keep ownership and rename the holder, or transfer both ownership and holder. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-200)*

`GST-015` Memberships

- Account → Membership → Billing statement shows a line-by-line statement with states: soft decline (Retry now + Use another card), hard decline (Use another card only), declined again (Use another card + next automatic retry date), paid ("Your membership continues"). Use another card lists saved cards. *(agreed · design review 29 Sep 2026, 2. Billing statement and payment retry (WEB-023) · DI-1036)*
- Season and membership packages show a quantity stepper once selected. *(client request · design review 23 Sep 2026, Cart 12. No quantity field for the selected ticket · DI-980)*
- UX reference: House of Wisdom (Sharjah library) meeting-room/"pod" booking and tiered membership plans — a simple duration-based booking flow without fixed performances/time slots — to be reviewed by Chinmay/Aishwarya. *(client request · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 6. Open Items · DI-506)*
- Membership lifecycle: upgrade, downgrade, suspend (freezes validity until re-enabled), deactivate and cancel, with configurable timing windows (e.g. upgrade allowed only in the final two months before expiry). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-467)*
- Membership/pass tickets: seasonal, monthly or annual classes with renewal/auto-renewal using a tokenised card-on-file billed ahead of expiry, subject to the guest's consent to terms and conditions. *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-448)*
- Membership screen: membership ID, validity, entitlements (free entry, F&B offers, etc.), linked members (view), membership card, renewal and history. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-201)*
- Membership / season pass is defined by start/end date rather than quantity, requires customer profile capture at purchase, and supports renew, upgrade, cancel and extend workflows. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-138)*

`GST-016` My Reservations

- Booking statuses: draft > reserved (awaiting payment) > completed, with cancelled or expired paths. Hold policy sets how long a capacity booking is held pending payment before release to inventory. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-612)*
- Guest profile shows gift vouchers and a stored-value "money card"/wallet; "My Tickets" (all tickets) is separate from "My Reservations" (bookings holding one or more tickets) with reservation details and date modification. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-199)*

`GST-017` Reservation Details

- Booking statuses: draft > reserved (awaiting payment) > completed, with cancelled or expired paths. Hold policy sets how long a capacity booking is held pending payment before release to inventory. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-612)*
- Decision (raised by Chinmay): date-change/reschedule is a product-level on/off setting with its own policy rules (e.g. allowed up to 24 hours before the visit, denied within 24 hours), not a separate screen. Typically off for special-day tickets (e.g. New Year, 1 January only), on for standard GA. *(agreed · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive; 5. Key Decisions · DI-446)*
- Guest profile shows gift vouchers and a stored-value "money card"/wallet; "My Tickets" (all tickets) is separate from "My Reservations" (bookings holding one or more tickets) with reservation details and date modification. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-199)*

`GST-018` Add to Calendar / Reminders

- Add bookings to Apple/Google/Outlook calendar with reminders; wishlist of F&B and retail items to buy later on-site. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-202)*

`GST-020` Saved Items / Wishlist

- Add bookings to Apple/Google/Outlook calendar with reminders; wishlist of F&B and retail items to buy later on-site. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-202)*

`GST-021` Interactive Map

- In-park 3D navigation is built natively (React Three.js) from the venue's 3D GLB model plus a metadata file of pathways and locations, combined with the guest's live GPS position; no external mapping tool. *(agreed · MoM 30 Sep 2026, 4.8 Mobile App — In-Ride Video/Info & In-Park Navigation · DI-1103)*
- In-park navigation: a live map view lets a guest navigate to a selected point (e.g. the nearest food outlet), entering a walking-navigation mode that guides the guest in real time. *(agreed · MoM 30 Sep 2026, 4.8 Mobile App — In-Ride Video/Info & In-Park Navigation · DI-1102)*
- Item detail shows the item's location on the map and proposes the relevant product, e.g. restaurant -> "Buy meal combo", which automatically adds the required admission ticket (checkout in ~3 steps). *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1019)*
- A visual venue map highlights long-queue rides vs low-queue alternatives so operations can redirect guests, e.g. a notification suggesting a nearby ride with a shorter wait. *(client request · MoM 7 Sep 2026, 4.17 AI guest flow optimization · DI-682)*
- Ride wait times come from the venue's sensor/camera counts via a live API (or a people count converted at a per-person rate) and are shown in the guest app; an AI "which ride to visit next" recommendation may follow. *(agreed · MoM 14 Aug 2026, 9. Queue Management · DI-299)*
- **Open question.** Customisable venue map showing attractions, dining, retail and restrooms. Qossai: define image/format guidance for tenant map uploads; benchmark is the Kidzania app's interactive 3D-style map. Final guidance still open. *(open · MoM 10 Aug 2026, 4.4 Venue Map, Queueing, F&B, Retail & Parking · DI-203)*

`GST-022` Attraction Wait Times

- Proactively upsell an express/fast-lane ticket to a guest facing a long wait (e.g. "buy express ticket for [amount]"). *(agreed · MoM 7 Sep 2026, 4.17 Revenue lever / 5. Key Decisions · DI-683)*
- The return time shown to a VQ guest must be genuinely accurate and recalculate dynamically from real-time conditions across all three tiers, not a static estimate given at booking. *(agreed · MoM 7 Sep 2026, 4.15 Waiting-time honesty & recalculation · DI-679)*
- In the app a guest with a valid ticket browses rides, sees the current wait (e.g. 60 minutes), joins the virtual queue for their party and gets a return window (e.g. 4:50-5:00 PM). Missing the window can auto-release the slot. *(client request · MoM 7 Sep 2026, 4.13 Virtual Queue - Mobile Journey & Configuration · DI-675)*
- Ride wait times come from the venue's sensor/camera counts via a live API (or a people count converted at a per-person rate) and are shown in the guest app; an AI "which ride to visit next" recommendation may follow. *(agreed · MoM 14 Aug 2026, 9. Queue Management · DI-299)*
- Live wait time per ride/attraction shown in the app (e.g. "41 minutes"), fed by the venue's third-party camera/sensor system through a TICVAI API. *(agreed · MoM 10 Aug 2026, 4.4 Venue Map, Queueing, F&B, Retail & Parking · DI-204)*

`GST-023` Virtual Queue

- Virtual queue join flow with a persistent status notification (e.g. "in queue, 25 minutes"). *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1090)*
- Proactively upsell an express/fast-lane ticket to a guest facing a long wait (e.g. "buy express ticket for [amount]"). *(agreed · MoM 7 Sep 2026, 4.17 Revenue lever / 5. Key Decisions · DI-683)*
- The return time shown to a VQ guest must be genuinely accurate and recalculate dynamically from real-time conditions across all three tiers, not a static estimate given at booking. *(agreed · MoM 7 Sep 2026, 4.15 Waiting-time honesty & recalculation · DI-679)*
- In the app a guest with a valid ticket browses rides, sees the current wait (e.g. 60 minutes), joins the virtual queue for their party and gets a return window (e.g. 4:50-5:00 PM). Missing the window can auto-release the slot. *(client request · MoM 7 Sep 2026, 4.13 Virtual Queue - Mobile Journey & Configuration · DI-675)*

`GST-024` F&B – Browse & Order

- In-app food ordering from venue outlets is kept deliberately simple, not built out as a full e-commerce flow. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1091)*
- In takeaway, delivery and café menus, Add opens a side panel for the dish: choose-one options (spice level, drink size, ice), optional priced add-ons (sides, dips, toppings, leave-outs) and quantity; total updates live and the basket line lists the choices. Shown whenever the item has modifier groups (no toggle). *(agreed · rev 3 design review 29 Sep 2026, REV3-9 · 9. Add-ons and modifiers for F&B menu items · DI-1050)*
- Delivery basket shows the fee (AED 15, free from AED 200) and "Add AED X more for free delivery"; below AED 90 checkout is refused; outside Dubai shows "We don't deliver to this address" with Change address / Switch to takeaway. A slot can close mid-flow: "That time just filled". *(agreed · design review 29 Sep 2026, 5. Takeaway and delivery (WEB-036) · DI-1039)*
- On the one-decision-per-screen layout, information blocks (notes, "what happens next", "what's included") stay on the screen before them and up to three quick choices share one screen. Table reservation and deposit hold become 1 screen; waitlist, takeaway, delivery, private dining enquiry 2; dinner deals 2 (party size with date/time). *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): Steps with nothing to decide · DI-1001)*
- **Open question.** Resources: meeting-room booking (headcount, duration, time slot, room, add-ons tea/coffee/snacks), modelled on House of Wisdom. Merchandise: browse, cart with add/remove quantity, pickup or doorstep delivery. F&B: outlet/menu browsing; collect at counter, curbside, doorstep or priority delivery. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Resources, Merchandise, F&B) · DI-690)*
- **Open question.** Dining has two flows: book a table (date, time, group size, seating-area preference, occasion, allergy/special-request notes) and order food (delivery or pickup location, items, checkout). *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Dining) · DI-688)*
- Decision (raised by Aishwarya): F&B and retail/merchandise online sale are optional back-office-enabled modules; where enabled, the whole purchase (browse, cart, checkout, pickup-at-venue or ship-to-guest) completes inside TICVAI — guests are never sent to download a separate app. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-505)*
- Out of scope: buying F&B with no admission ticket (entering only to buy food). *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-292)*
- Guests already inside the venue order F&B in the app without visiting the counter, choosing pickup or in-park delivery to a specified location. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-291)*
- Seated events: guest chooses pickup or delivery to seat (seat known from the booking). Open venues (beach, water park): a physical QR at each seat/location is scanned to say where food is delivered. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-288)*
- F&B: browse outlets and order; pickup location shown automatically per outlet, with delivery as an extra option (needs guest location) when the venue uses the platform's F&B module. Retail follows the same pickup/delivery model. *(client request · MoM 10 Aug 2026, 4.4 Venue Map, Queueing, F&B, Retail & Parking · DI-205)*

`GST-025` F&B – Order Tracking

- Seated events: guest chooses pickup or delivery to seat (seat known from the booking). Open venues (beach, water park): a physical QR at each seat/location is scanned to say where food is delivered. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-288)*

`GST-026` Retail / Merchandise

- **Open question.** Resources: meeting-room booking (headcount, duration, time slot, room, add-ons tea/coffee/snacks), modelled on House of Wisdom. Merchandise: browse, cart with add/remove quantity, pickup or doorstep delivery. F&B: outlet/menu browsing; collect at counter, curbside, doorstep or priority delivery. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Resources, Merchandise, F&B) · DI-690)*
- Decision (raised by Aishwarya): F&B and retail/merchandise online sale are optional back-office-enabled modules; where enabled, the whole purchase (browse, cart, checkout, pickup-at-venue or ship-to-guest) completes inside TICVAI — guests are never sent to download a separate app. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-505)*
- Retail items (e.g. a t-shirt plus a cap) can be combined into a combo package with bundle-level pricing, presented both on-site and online with product images and descriptions. *(client request · MoM 19 Aug 2026, 4.3 Pricing, Bundles & Promotions · DI-358)*
- Stock is centralised per venue across web, app, kiosk and POS and not shared across venues; sale is gated by the system-recorded stock (an outlet with no system stock cannot sell even if physically present); inter-venue stock transfer moves stock. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-294)*
- F&B: browse outlets and order; pickup location shown automatically per outlet, with delivery as an extra option (needs guest location) when the venue uses the platform's F&B module. Retail follows the same pickup/delivery model. *(client request · MoM 10 Aug 2026, 4.4 Venue Map, Queueing, F&B, Retail & Parking · DI-205)*

`GST-027` Parking – Reserve & Pay

- Parking is barrier integration, not space counting: one configuration screen chooses a model - no integration (TICVAI QR checked by security), ANPR (guest enters a plate at checkout, pushed to the barrier whitelist) or QR handoff to the barrier. Pay-per-hour parking is out of scope. *(agreed · MoM 14 Aug 2026, 10 · DI-316)*
- Parking supports three models: (1) no integration — TICVAI QR verified manually by security; (2) plate number at checkout pushed to the parking system's ANPR whitelist; (3) TICVAI QR passed to the barrier. Hourly pay-on-exit parking stays on the parking system's own POS. *(agreed · MoM 14 Aug 2026, 10. Parking Integrations · DI-300)*

`GST-028` Parking – Reservation Confirmed

- Parking supports three models: (1) no integration — TICVAI QR verified manually by security; (2) plate number at checkout pushed to the parking system's ANPR whitelist; (3) TICVAI QR passed to the barrier. Hourly pay-on-exit parking stays on the parking system's own POS. *(agreed · MoM 14 Aug 2026, 10. Parking Integrations · DI-300)*

`GST-030` In-Venue Notifications

- Virtual queue join flow with a persistent status notification (e.g. "in queue, 25 minutes"). *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1090)*
- The in-venue notifications feed is needed in the first release on web and mobile (R242 deferral reversed). *(agreed · design review 29 Sep 2026, GAP-C1 · C. Wave 2: In-Venue Notifications · DI-1075)*
- Proactively upsell an express/fast-lane ticket to a guest facing a long wait (e.g. "buy express ticket for [amount]"). *(agreed · MoM 7 Sep 2026, 4.17 Revenue lever / 5. Key Decisions · DI-683)*
- A visual venue map highlights long-queue rides vs low-queue alternatives so operations can redirect guests, e.g. a notification suggesting a nearby ride with a shorter wait. *(client request · MoM 7 Sep 2026, 4.17 AI guest flow optimization · DI-682)*

`GST-031` AI Concierge – Home

- The concierge (Sahli) shows as mascot art or as a plain button; setting "Concierge mascot", default on. *(agreed · design review 29 Sep 2026, CFG-5 · Sahli mascot (on/off) · DI-1069)*
- AI concierge answers natural-language guest questions (ticketing, F&B, retail, venue info, timings) grounded in the venue's configured data. *(client request · MoM 10 Aug 2026, 4.6 AI Functions, Lost & Found, Reviews, Loyalty · DI-207)*
- **Open question.** AI concierge chat design is deferred until a dedicated AI workshop settles the technical approach (third-party LLM with PII masking) and the token/billing model. *(open · MoM 10 Aug 2026, 4.2 AI Concierge Chat — Open Item · DI-195)*

`GST-032` AI Concierge – Chat

- The AI chat box answers guided/predefined queries (booking status, rescheduling) and logs guest conversation history across channels (WhatsApp, web, Instagram, Facebook) with per-channel conversion attribution. *(client request · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-388)*
- AI concierge answers natural-language guest questions (ticketing, F&B, retail, venue info, timings) grounded in the venue's configured data. *(client request · MoM 10 Aug 2026, 4.6 AI Functions, Lost & Found, Reviews, Loyalty · DI-207)*
- **Open question.** AI concierge chat design is deferred until a dedicated AI workshop settles the technical approach (third-party LLM with PII masking) and the token/billing model. *(open · MoM 10 Aug 2026, 4.2 AI Concierge Chat — Open Item · DI-195)*

`GST-034` Lost & Found

- Lost & Found: guests log lost items in the app; back-office staff match and mark items found for collection, with full tracking. *(client request · MoM 10 Aug 2026, 4.6 AI Functions, Lost & Found, Reviews, Loyalty · DI-208)*

`GST-035` Feedback & Ratings

- Surveys trigger at configurable points: post-purchase, post-visit, post-ticket-scan, membership renewal and case closure. *(client request · MoM 20 Aug 2026, 4.9 Surveys & Gamification · DI-391)*
- Example site showed a live integration with a government satisfaction-survey ("happiness meter") service. *(client request · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-112)*

`GST-036` Loyalty & Rewards

- Gamification shows badges/status tiers (e.g. Explorer, Adventurer, Legend) earned by spend or engagement thresholds, feeding the loyalty tier structure. *(client request · MoM 20 Aug 2026, 4.9 Surveys & Gamification · DI-392)*
- **Open question.** Loyalty accrues points by product/spend tier (e.g. bronze/silver/gold thresholds) and unlocks tier benefits (e.g. platinum-tier discounts on F&B and ticketing). Full programme configuration (tiers, points, redemption, expiry) pending a dedicated session. *(open · MoM 20 Aug 2026, 4.5 Loyalty, Membership & Wallet · DI-382)*

`GST-038` At the Venue

- In-park 3D navigation is built natively (React Three.js) from the venue's 3D GLB model plus a metadata file of pathways and locations, combined with the guest's live GPS position; no external mapping tool. *(agreed · MoM 30 Sep 2026, 4.8 Mobile App — In-Ride Video/Info & In-Park Navigation · DI-1103)*
- In-park navigation: a live map view lets a guest navigate to a selected point (e.g. the nearest food outlet), entering a walking-navigation mode that guides the guest in real time. *(agreed · MoM 30 Sep 2026, 4.8 Mobile App — In-Ride Video/Info & In-Park Navigation · DI-1102)*
- Guests already inside the venue order F&B in the app without visiting the counter, choosing pickup or in-park delivery to a specified location. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-291)*

`GST-039` Profile

- Guests can create family-member profiles themselves and set spending limits directly from their own guest account, in addition to venue-side configuration. *(agreed · MoM 27 Aug 2026, 4.8 Family, Parent-Child & Corporate Wallets · DI-530)*

`GST-040` Help & Support

- The guest Help screen shows app status and a public, localised "what's new" (release notes). *(agreed · design review 29 Sep 2026, GAP-B2 · B. Help: app status + recent changes · DI-1073)*
- Support chat is native to TICVAI: a built-in AI chat assistant answers first, then escalates to a human "CR representative" role in the platform; offered white-labelled as a subscription add-on for smaller clients. *(agreed · MoM 12 Aug 2026, 10. Customer Support / Chat Integration Approach · DI-256)*
- Configurable FAQ section plus Terms & Conditions, Privacy Policy and Cookie Policy with an accept/deny prompt. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-191)*

`GST-041` Checkout Entry

- Guest counters take their price from the chosen park ticket and produce one line, e.g. "2 park ticket · Adult × 3 = AED 1,425" (no separate Adult × 3 line). Child and senior prices scale from the chosen ticket; infants free. *(client request · design review 30 Sep 2026, 2. Multi-park ticket adds an extra adult line · DI-1106)*
- Checkout completes in 4 steps, supporting Apple Pay/card payment, and adds the resulting ticket to Apple Wallet or Google Wallet. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1096)*
- The mobile booking flow (date/day-pass selection, quantity, cross-sell, sign-in) is functionally identical to the web app. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1092)*
- Cart & summary options: sidebar fixed right, sidebar left, slide-in right, slide-up bottom, floating cart icon (round basket button with item count opening the slide-in basket), single column. In Arabic the basket stays on the right by default (client confirmed); "Cart side in Arabic" can mirror to left. *(agreed · rev 3 design review 29 Sep 2026, REV3-10 · 10. Cart display: fixed on right, slide bar, icon, bottom; right for Arabic · DI-1051)*
- Sign-in (or the guest code when guest checkout is on) is asked when the guest leaves the Add-ons step; the basket is kept. Setting "Ask to sign in": After add-ons (default) or At payment. *(agreed · rev 3 design review 29 Sep 2026, REV3-3 · 3. The sign-in screen should appear after Add-ons · DI-1043)*
- After the code, a match prompt shows what matched (e.g. 4 past orders, first order 12 Mar 2024, profile type), never the other profile's name or details, with "Use this profile" / "Not me – keep separate". Expired state: "This match has expired – continue as a new guest." *(agreed · design review 29 Sep 2026, 1. Guest checkout, code proof, profile matching (WEB-012) · DI-1035)*
- Guest checkout is a venue toggle, off by default: off = sign-in screen at payment ("This venue requires an account for checkout. Your basket is kept."), guest button hidden. On = "Continue as guest" with email or mobile (per "Match returning guests by") and a code; only exactly six digits accepted, copy says six. *(agreed · design review 29 Sep 2026, 1. Guest checkout, code proof, profile matching (WEB-012) · DI-1034)*
- Each cart line shows the date of visit: the match date for the stadium, the reservation date for dining (mobile: in the cart bar). *(agreed · design review 29 Sep 2026, Cart 9. Show the date of visit in the cart · DI-1029)*
- The guest-checkout email pop-up collects only the fields configured in the back end (email, phone and/or name). After the code is verified, do not ask for name/email/phone again: go straight to T&Cs and complete the booking; profile is created and can be completed later (Platinumlist pattern). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W1 Guest checkout · DI-1002)*
- Each picked seat goes into the cart with section, row, seat and price (e.g. "Section 101 · Row A, Seat 4 · AED 165"); tapping the seat again removes it. *(client request · design review 23 Sep 2026, Seat map 15. Selected seats should be added to the cart · DI-982)*
- **Open question.** Qossai: a guest-checkout customer may not have opted into marketing the way a registered customer accepting full terms has; how marketing consent is captured at guest checkout is unresolved. *(open · MoM 18 Sep 2026, 4.8 Guest Checkout & Profile Deduplication — Extended Discussion · DI-940)*
- Channel rules govern which actions each channel can perform (create, upgrade, cancel) and whether checkout is guest checkout (name, phone, email only) or full registration/sign-in. Customer category (corporate, travel agent/B2B, school) determines extra information collected. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-613)*
- At checkout guests can sign in, register (with a visible loyalty-points incentive) or continue as guest; terms acceptance is implied by proceeding to payment, with no separate checkbox. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-588)*
- Checkout supports guest checkout, registered-account checkout, and single sign-on (e.g. Okta, Azure AD, a ticketing-specific SSO). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-121)*

`GST-042` Simple Registration & OTP

- Sign-in (or the guest code when guest checkout is on) is asked when the guest leaves the Add-ons step; the basket is kept. Setting "Ask to sign in": After add-ons (default) or At payment. *(agreed · rev 3 design review 29 Sep 2026, REV3-3 · 3. The sign-in screen should appear after Add-ons · DI-1043)*
- After the code, a match prompt shows what matched (e.g. 4 past orders, first order 12 Mar 2024, profile type), never the other profile's name or details, with "Use this profile" / "Not me – keep separate". Expired state: "This match has expired – continue as a new guest." *(agreed · design review 29 Sep 2026, 1. Guest checkout, code proof, profile matching (WEB-012) · DI-1035)*
- Guest checkout is a venue toggle, off by default: off = sign-in screen at payment ("This venue requires an account for checkout. Your basket is kept."), guest button hidden. On = "Continue as guest" with email or mobile (per "Match returning guests by") and a code; only exactly six digits accepted, copy says six. *(agreed · design review 29 Sep 2026, 1. Guest checkout, code proof, profile matching (WEB-012) · DI-1034)*
- The guest-checkout email pop-up collects only the fields configured in the back end (email, phone and/or name). After the code is verified, do not ask for name/email/phone again: go straight to T&Cs and complete the booking; profile is created and can be completed later (Platinumlist pattern). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W1 Guest checkout · DI-1002)*
- Decision: at least one of e-mail or mobile number is mandatory at profile creation (not both — some customers decline e-mail); the system supports conditional "either/or" mandatory-field rules. *(agreed · MoM 20 Aug 2026, 4.1 CRM; 5. Key Decisions · DI-372)*
- Sign-up by phone number or email, verified by OTP (WhatsApp or SMS/email as configured), then minimal profile (first/last name). *(client request · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-209)*
- UAE Pass login: customer enters mobile number, approves a push notification, confirms with biometrics; verified personal details are pulled into the booking automatically and a linked account is created. *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-123)*
- Checkout supports guest checkout, registered-account checkout, and single sign-on (e.g. Okta, Azure AD, a ticketing-specific SSO). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-121)*

`GST-044` Multi-Currency & Pricing

- A currency selector (AED, SAR, USD, INR, GBP) converts every displayed price. *(agreed · design review 29 Sep 2026, CFG-7 · Currency (AED/SAR/USD/INR/GBP) · DI-1071)*
- Foreign-currency display: an approximate conversion at a back-office rate so the guest sees roughly what they pay while settling in base currency, and/or full DCC at the gateway where the guest is charged in their own currency; records always in the venue base currency. *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-211)*

`GST-045` Ticket Delivery & Sharing

- Duplicate screens become one implementation covering several screen IDs (mobile Transfer + Delivery & Sharing; web Wishlist / Devices & Consent; Help Centre + Help & Accessibility as one Help view with FAQ, cases, policies, accessibility tabs). Ticket-selection functions belong on GST-008. Web gets a Group Booking view. *(agreed · design review 29 Sep 2026, GAP-D3 · D. Duplicate screens merged; group booking on web · DI-1078)*
- Supporting configuration: ticket variants (adult/child/senior/VIP, configurable), waitlist, on-sale/off-sale timing and cut-offs, entitlement/access rules (single/multi-venue, entries, zones, early entry), fulfilment channels (email, WhatsApp, SMS), after-sales windows (upgrade, reschedule, cancel), dynamic/fixed pricing and promotions. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-437)*
- Ticket delivery: "Add to Wallet" (Apple or Google Wallet by device), and WhatsApp, SMS or email per the guest's chosen method, selectable at checkout/confirmation; tickets can also be emailed to a third party. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-198)*

`GST-046` Branded Queue / Waiting Room

- Branded virtual waiting room activates automatically above a configurable concurrent-buyer threshold (e.g. 500) during high-demand on-sales, shows a wait time, and follows the tenant's app theme. *(client request · MoM 10 Aug 2026, 4.8 Checkout Extras — Delivery, Waiting Room, Upsell/Cross-Sell, Seating, Resources · DI-214)*
- Waiting room behaviour: guests are held in a queue that preserves their connection, told an estimated wait time, and let through in controlled batches (e.g. 200-300 guests per minute); completed transactions must reliably trigger email confirmation and ticket delivery. *(agreed · MoM 31 Jul 2026, 5. Consistency, Replication & Disaster Recovery · DI-062)*
- Virtual waiting room page: branded with the customer's venue logo, shows estimated waiting time and progress indicators, admits customers at controlled intervals. Configured independently per customer and venue. *(agreed · MoM 28 Jul 2026, 19. Auto-scaling and Virtual Waiting Room · DI-016)*

`GST-047` Maintenance / Upgrade Page

- Customisable maintenance page shown to guests during planned maintenance/upgrades. *(client request · MoM 10 Aug 2026, 4.8 Checkout Extras — Delivery, Waiting Room, Upsell/Cross-Sell, Seating, Resources · DI-215)*

`GST-048` Upsell / Cross-Sell

- The mobile booking flow (date/day-pass selection, quantity, cross-sell, sign-in) is functionally identical to the web app. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1092)*
- "Upgrade your day" (upgrades) stays hidden until a main ticket is in the cart. *(client request · design review 23 Sep 2026, Cart 10. Show upgrades only after the main ticket is in the cart · DI-978)*
- A guest is not repeatedly re-offered something already declined (e.g. a fast pass rejected three times), and an offer ignored online is not re-presented on another channel, e.g. at POS after the guest bought it there. *(agreed · MoM 21 Sep 2026, 4.6 Personalized Offer Delivery & Omni-Channel Orchestration · DI-962)*
- What a guest is offered depends on context: a member is not offered another membership (F&B or retail add-ons instead); general admission is not offered once VIP/fast pass is selected; an expiring membership prompts a renewal rather than a new product; similar offers are not shown back-to-back (alternate F&B and experience upsells). *(client request · MoM 21 Sep 2026, 4.2 / 4.3 / 4.5 Recommendation Strategy and Decisioning · DI-960)*
- Recommendations stay within business limits, e.g. at most three recommendations shown at checkout and never a product the customer already owns; AI recommendations never override hard business rules or eligibility constraints. *(agreed · MoM 21 Sep 2026, 4.3 Recommendation Strategy — Business Priority, Conflict Suppression & Fallback · DI-959)*
- Upsell/cross-sell offers (e.g. a family pass after 2 adult + 2 child tickets are added) are a distinct "extras" step after main product selection, not inline on the ticket selection page, where guests would miss them. *(agreed · MoM 18 Sep 2026, 4.14 Guest Website UX Review — Upsell/Cross-Sell Placement & Reference Sites · DI-951)*
- Add-ons attached to a main product can be mandatory or optional; cross-sell offers related add-on products, upsell proposes a higher tier (e.g. adult admission → membership). *(client request · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies · DI-470)*
- Decision: the add-ons step is optional/removable in configuration for products with no add-ons, collapsing the flow to Ticket Selection → Cart → Checkout. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-428)*
- System-driven upsell/cross-sell prompts, e.g. a yearly membership on top of general admission, or a family bundle when 2 adult + 2 child tickets are in the cart, each with its discount/benefit. *(client request · MoM 10 Aug 2026, 4.8 Checkout Extras — Delivery, Waiting Room, Upsell/Cross-Sell, Seating, Resources · DI-216)*

`GST-049` Interactive Seat Selection

- The mobile stadium/venue seat map uses the same pinch-to-zoom-in and zoom-out interaction agreed on the web; seat rendering was glitched in this build but the behaviour is confirmed as intended. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1095)*
- Theatre has its own auditorium seat map: stage (or screen for cinema) at front, Stalls/Circle/Balcony with curved rows, aisles and Premium/Standard/Economy pricing. Date, time, show (plus language & format for cinema) and the seat map sit on one page. Seats per guest booking default 10 (venue setting); basket lists each seat. *(agreed · rev 3 design review 29 Sep 2026, REV3-7 · 7. Theatre flow should be similar to the stadium flow · DI-1047)*
- A time bar above the seat map shows the chosen performance, lets the guest switch show and has Change date; switching releases held seats. Setting "Time bar above seat map", default on. On the selection step, time sits directly under the date, above language & format and tickets. *(agreed · rev 3 design review 29 Sep 2026, REV3-6 · 6. Time selection on top, configurable · DI-1046)*
- The 'view from your seat' box can sit Bottom (default), Right, Left or Top of the seat map (web only); on narrow screens and mobile it is always below the map. Setting "Seat view box". *(agreed · rev 3 design review 29 Sep 2026, REV3-5 · 5. CMS option to show the seat view right, left, top or bottom · DI-1045)*
- Seated events with one on-sale performance go straight to the seat map (Flow 1). Otherwise date and time come first (Flow 2), either as an inline step (timed-ticket style, default) or as a pop-up dialog over the seat map. Setting "Date & time on seat events". *(agreed · rev 3 design review 29 Sep 2026, REV3-4 · 4. Flow 1 (fixed date and time) and Flow 2 (select date, then time, then seat map) · DI-1044)*
- Picking a section shows the view from that section (concert mode shows the stage; closer sections see a larger stage with fewer rows in front). Use the venue's photo for the section when supplied, otherwise render the view from the imported 3D geometry. *(agreed · design review 29 Sep 2026, Seat map 14. Show the view to the stage in the small window · DI-1030)*
- Stadium/theatre seat maps show sections first with colour and price; zooming into a section shows its seats. Pinch-out / scroll-out returns to the full map so other sections can be compared. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W2 Seat maps · DI-1003)*
- Zoomed in, every nearby section shows its seats as equal-size dots: available in the section's price colour, taken in grey, picked seat highlighted. Zoom in, Zoom out and "Whole map" buttons sit under the map. *(client request · design review 23 Sep 2026, Seat map 17. When zoomed in, show the available seats across the map · DI-983)*
- Each picked seat goes into the cart with section, row, seat and price (e.g. "Section 101 · Row A, Seat 4 · AED 165"); tapping the seat again removes it. *(client request · design review 23 Sep 2026, Seat map 15. Selected seats should be added to the cart · DI-982)*
- On 3D venue maps, selecting a section takes the guest straight into that section's seats in one motion by zooming in, not via a separate pop-up, modal or new window. *(agreed · MoM 18 Sep 2026, 4.13 Guest Website UX Review — Ticket Type Flows & Seat Map Selection · DI-950)*
- 3D seat view: a guest booking a seated event (e.g. stadium concert) can preview the view from the selected section in 3D - built in (Three.js in React), no third-party integration; the standard 2D seat map remains the simpler option. *(agreed · MoM 15 Sep 2026, 4.2 Guest Web App - 3D Stadium Seat View & At-Venue Wayfinding · DI-889)*
- **Open question.** Prototype events: concert seat-map selection modelled on Coca-Cola Arena (like Platinum List); multi-day festival with day/time-slot selection; tiered show tickets (early bird, couple, group-of-4, group-of-6); all share one add-to-cart and checkout flow. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Events) · DI-685)*
- Decision: seats held in a cart auto-release after a configurable timeout if checkout is abandoned, and immediately if a payment attempt fails. *(agreed · MoM 21 Aug 2026, 4.6 Seat Inventory Status; 5. Key Decisions · DI-422)*
- Decision: seating rules — consecutive-seat enforcement (no single empty seat left between bookings), social-distancing buffer (auto-block adjacent seats), seat-kill rule, company/held-seat rule — are configurable per venue/event, defaulting to the venue's operational policy. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules; 5. Key Decisions · DI-416)*
- One seat map can mix section types — e.g. 8 of 10 sections seated and 2 standing ("fan pit" near the stage); suites sell either as a private bulk-priced suite or as individual seats within the suite. *(agreed · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types · DI-411)*
- Decision: three seat-selection models, selectable per section, per event: (1) zone/capacity selling with no seat numbers (guest told zone only); (2) system-assigned "best available" — guest picks section + quantity, seats disclosed later; (3) full customer seat selection. *(agreed · MoM 21 Aug 2026, 4.1 Reference Walkthrough; 4.2 Seat Map Builder; 5. Key Decisions · DI-410)*
- Platinum List reference seat step: interactive seat map colour-coded by price tier → seat selection with a live cart hold and countdown timer → checkout via Quick Order / Apple ID / Google ID. *(client request · MoM 21 Aug 2026, 4.1 Reference Walkthrough — Platinum List Seat Selection & Checkout Journey · DI-409)*
- Drag-and-drop page builder with a standardised layout (header, footer, hero/card components) that adapts to product type — seat map for seated products, standard flow for general admission. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-394)*
- Movie/cinema ticketing is in scope through the seat management module (e.g. a Kuwait museum's educational cinema: assigned seats, a film, a time slot). *(agreed · MoM 14 Aug 2026, 5. Movie Ticketing · DI-286)*
- Booking steps follow the product type: admission goes straight to quantity; dated products to a date, timed ones on to a time, then quantity; seated products to zone, then seats on a seat map, then quantity by variant (adult, child, concession). *(agreed · MoM 3 Aug 2026, Ticket Flow Variations by Product Type · DI-131)*
- Seat assignment flow is "select time, then select seat", with the two steps on different screens. *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-057)*

`GST-050` Resource Booking – Cabana

- The table/cabana screen becomes map-based booking: a venue map can carry cabanas, loungers, tables (beach or event tables) and other bookable resources, sold like cabanas. Dining tables stay F&B table reservations. *(agreed · design review 29 Sep 2026, GAP-C2 · C. Wave 2: Reserve a Table or Cabana (waitlist, notify) · DI-1076)*
- Cabanas are picked on the venue's ingested map, like stadium seats: numbered cabanas by zone (e.g. R01–R10, T01–T08, S01–S06, B01–B10) showing guests seated, sold-out greyed and marked. Tapping one adds it (e.g. "Cabana B09 · Large cabana · Beach, AED 1,855") and starts a remaining-time counter. Map on the first screen. *(agreed · rev 3 design review 29 Sep 2026, REV3-15 · 15. Book the product from the map (e.g. pick an available cabana) · DI-1055)*
- Map-based cabana booking stays optional per configuration, since not every operator uses the same flow; it uses the same map back end as theme-park F&B/locations (reusable later for in-park navigation). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W6 Cabanas · DI-1008)*
- **Open question.** Cabanas: category (premium, VIP, luxury, private, family, couples), date/time, guest count, amenity details. Activities: desert-safari packages (buy-one-get-one, evening, Bedouin-style), pickup point, add-ons (stroller), duration packages (2-hour/4-hour). *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Cabanas, Activities) · DI-687)*

`GST-051` Plan

- A preference a day's park cannot meet is said, not filled: a "Not at this park" banner per day names the cuisine or shop and the park that has it (e.g. "No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2)."), hidden when all are met. Lunch cuisine options name the parks serving them ("Indian - Summit Peaks only"). *(agreed · MoM 30 Sep 2026, 4.7 · DI-1113)*
- Allam: multi-venue visit planner. In a multi-venue tenant the guest picks a park per chosen day ("Which park each day?", hidden otherwise); each day tab names its park and every item, swap candidate and AI-planner suggestion comes only from that park's rides, dining and shops, never another park's. *(agreed · MoM 30 Sep 2026, 4.7 · DI-1112)*
- Retail/kiosk shops are added to the planner's venue-linked options alongside F&B (previously only F&B). *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1100)*
- Allam: the planner applies multi-venue intelligence; it checks actual venue-level amenities before including a preference, e.g. if only one of several parks has an Indian restaurant. It pulls only rides, F&B and retail available at each specific venue. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1099)*
- Itinerary planner (Yas Island planner reference): party composition (adults/children with height/age), visit dates, pace (packed/balanced/relaxed) and cuisine preferences feed an auto-generated, swappable multi-day itinerary with associated costing. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1098)*
- The visit planner is tied to a ticket purchase and saved as a personal visit profile; benchmarked against Skidata. *(agreed · MoM 10 Aug 2026, 4.9 · DI-242)*
- Chinmay: share an itinerary with a group via an in-app QR code a friend scans to join, or an invite-to-join. *(agreed · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-218)*
- "Plan Your Adventure": guided itinerary planner (Skidata benchmark) where the guest picks which rides/attractions and in what order ahead of time, tied to the ticket purchase and saved as a personal visit profile. *(client request · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-217)*

`GST-052` Suggested Itineraries

- Itinerary planner (Yas Island planner reference): party composition (adults/children with height/age), visit dates, pace (packed/balanced/relaxed) and cuisine preferences feed an auto-generated, swappable multi-day itinerary with associated costing. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1098)*
- "Plan Your Adventure": guided itinerary planner (Skidata benchmark) where the guest picks which rides/attractions and in what order ahead of time, tied to the ticket purchase and saved as a personal visit profile. *(client request · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-217)*

`GST-053` Your Plan

- A preference a day's park cannot meet is said, not filled: a "Not at this park" banner per day names the cuisine or shop and the park that has it (e.g. "No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2)."), hidden when all are met. Lunch cuisine options name the parks serving them ("Indian - Summit Peaks only"). *(agreed · MoM 30 Sep 2026, 4.7 · DI-1113)*
- Allam: multi-venue visit planner. In a multi-venue tenant the guest picks a park per chosen day ("Which park each day?", hidden otherwise); each day tab names its park and every item, swap candidate and AI-planner suggestion comes only from that park's rides, dining and shops, never another park's. *(agreed · MoM 30 Sep 2026, 4.7 · DI-1112)*
- Retail/kiosk shops are added to the planner's venue-linked options alongside F&B (previously only F&B). *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1100)*
- Allam: the planner applies multi-venue intelligence; it checks actual venue-level amenities before including a preference, e.g. if only one of several parks has an Indian restaurant. It pulls only rides, F&B and retail available at each specific venue. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1099)*
- Itinerary planner (Yas Island planner reference): party composition (adults/children with height/age), visit dates, pace (packed/balanced/relaxed) and cuisine preferences feed an auto-generated, swappable multi-day itinerary with associated costing. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1098)*
- Itinerary group sharing: an in-app QR code a friend scans to join the itinerary (Chinmay raised, Qossai confirmed). *(agreed · MoM 10 Aug 2026, 4.9 · DI-241)*
- Chinmay: share an itinerary with a group via an in-app QR code a friend scans to join, or an invite-to-join. *(agreed · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-218)*
- "Plan Your Adventure": guided itinerary planner (Skidata benchmark) where the guest picks which rides/attractions and in what order ahead of time, tied to the ticket purchase and saved as a personal visit profile. *(client request · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-217)*

`GST-054` AI Planner

- A preference a day's park cannot meet is said, not filled: a "Not at this park" banner per day names the cuisine or shop and the park that has it (e.g. "No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2)."), hidden when all are met. Lunch cuisine options name the parks serving them ("Indian - Summit Peaks only"). *(agreed · MoM 30 Sep 2026, 4.7 · DI-1113)*
- Allam: multi-venue visit planner. In a multi-venue tenant the guest picks a park per chosen day ("Which park each day?", hidden otherwise); each day tab names its park and every item, swap candidate and AI-planner suggestion comes only from that park's rides, dining and shops, never another park's. *(agreed · MoM 30 Sep 2026, 4.7 · DI-1112)*
- Allam: the planner applies multi-venue intelligence; it checks actual venue-level amenities before including a preference, e.g. if only one of several parks has an Indian restaurant. It pulls only rides, F&B and retail available at each specific venue. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1099)*
- "Plan Your Adventure": guided itinerary planner (Skidata benchmark) where the guest picks which rides/attractions and in what order ahead of time, tied to the ticket purchase and saved as a personal visit profile. *(client request · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-217)*

`GST-055` Dynamic QR Ticket

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

`GST-056` Bundle Package

- Reference details: sibling/multi-buy discount shown with a struck-through original price; workshop add-ons inline with theme/cuisine sub-selection feeding time-slot availability; a package builder for bundled experiences. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-586)*
- Packages bundle any combination of ticket-type components with package-level pricing (e.g. admission + F&B item + retail item, or admission + show); F&B or retail is not required. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-435)*
- **Open question.** Open: alongside curated pre-built packages, let guests build their own bundle in the cart, with the system detecting eligible combinations and applying an automatic discount (e.g. 5–10%). *(open · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-221)*
- Bundle packages combine components within one attraction (ticket + meal + retail, or ticket + event ticket) at a discount — not a cross-attraction itinerary. *(agreed · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-220)*

`GST-057` Accessibility Information

- Custom content pages (e.g. accessibility information: step-free routes, facilities, what to expect) are tenant-authored and must follow accessibility-guideline compliance. *(agreed · MoM 10 Aug 2026, 4.1 · DI-243)*
- Custom content pages per venue (e.g. "Plan Your Visit", Accessibility) that follow accessibility guidelines. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-190)*

`GST-058` Resource Availability (Cabana)

- The table/cabana screen becomes map-based booking: a venue map can carry cabanas, loungers, tables (beach or event tables) and other bookable resources, sold like cabanas. Dining tables stay F&B table reservations. *(agreed · design review 29 Sep 2026, GAP-C2 · C. Wave 2: Reserve a Table or Cabana (waitlist, notify) · DI-1076)*
- Cabanas are picked on the venue's ingested map, like stadium seats: numbered cabanas by zone (e.g. R01–R10, T01–T08, S01–S06, B01–B10) showing guests seated, sold-out greyed and marked. Tapping one adds it (e.g. "Cabana B09 · Large cabana · Beach, AED 1,855") and starts a remaining-time counter. Map on the first screen. *(agreed · rev 3 design review 29 Sep 2026, REV3-15 · 15. Book the product from the map (e.g. pick an available cabana) · DI-1055)*
- Map-based cabana booking stays optional per configuration, since not every operator uses the same flow; it uses the same map back end as theme-park F&B/locations (reusable later for in-park navigation). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W6 Cabanas · DI-1008)*
- **Open question.** Cabanas: category (premium, VIP, luxury, private, family, couples), date/time, guest count, amenity details. Activities: desert-safari packages (buy-one-get-one, evening, Bedouin-style), pickup point, add-ons (stroller), duration packages (2-hour/4-hour). *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Cabanas, Activities) · DI-687)*

`GST-061` Menu Item Detail

- In takeaway, delivery and café menus, Add opens a side panel for the dish: choose-one options (spice level, drink size, ice), optional priced add-ons (sides, dips, toppings, leave-outs) and quantity; total updates live and the basket line lists the choices. Shown whenever the item has modifier groups (no toggle). *(agreed · rev 3 design review 29 Sep 2026, REV3-9 · 9. Add-ons and modifiers for F&B menu items · DI-1050)*
- Modifiers can be free or chargeable with minimum/maximum selection rules; combo meals support component selection with upgrade options at additional cost. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-328)*

`GST-062` Shop & Drop Collection

- Decision (raised by Aishwarya): F&B and retail/merchandise online sale are optional back-office-enabled modules; where enabled, the whole purchase (browse, cart, checkout, pickup-at-venue or ship-to-guest) completes inside TICVAI — guests are never sent to download a separate app. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-505)*
- Online retail offers buy-online-pickup-in-store and buy-online-ship-to-address. Shipping fees are set by region/city (e.g. Dubai, Abu Dhabi, international); decision: operations enter courier rates and margins manually, no live courier-API integration at this stage. *(agreed · MoM 19 Aug 2026, 4.3 Pricing, Bundles & Promotions; 4.8 Online Order Fulfilment & Shipping Configuration · DI-359)*

`GST-065` Newsletter & Preferences

- Consent policy governs marketing/newsletter/survey communications; customers who do not opt in must not receive promotional communications. *(client request · MoM 20 Aug 2026, 4.3 Consent, Data Privacy & Retention · DI-378)*

`GST-066` Privacy & My Data

- Qossai: use an existing major venue-group client's live app and published privacy policy as the model for how facial-recognition consent, data use and retention are explained to guests. *(client request · MoM 2 Sep 2026, 4.11 Privacy & Biometric Data Retention · DI-642)*
- Data-subject requests (access, correction, deletion) are tracked with status submitted → in progress → completed. *(client request · MoM 20 Aug 2026, 4.3 Consent, Data Privacy & Retention · DI-379)*

`GST-067` Refunds & Resale

- Approved refunds go back to the original payment method or are credited to the guest's wallet for future purchases. *(client request · MoM 7 Sep 2026, 4.11 Entitlements Usage, Upgrades & Refund/Credit Recovery · DI-673)*
- White-label resale page: guest lists a ticket and sets a price within the allowed range; buyer searches, browses and receives the new ticket after purchase; the resale summary shows the market fee TICVAI retains. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 3 · DI-621)*
- Three resale access models: (1) the client's own B2C site, where a guest requests resale within an admin-set price range (e.g. 10-20% below original); (2) a TICVAI-hosted white-label resale portal (e.g. museum.tickvai.com) for clients without B2C; (3) API for clients' own resale markets. *(agreed · MoM 1 Sep 2026, 4.14 Resale Marketplace - Detailed Follow-Up · DI-618)*
- **Open question.** Resale lets a guest resell a ticket through a secured channel with configurable commission and eligibility (e.g. minimum time before validity date, no expired tickets). Open: TICVAI-owned secure portal vs inside each client's own B2C site/app. *(open · MoM 31 Aug 2026, 4.12 Resale Marketplace · DI-584)*
- Online/app returns: customer submits a return request with a reason (and photo if applicable) → approval team → courier pickup → refund after verified receipt. Confirmed: an item bought at the POS can also be returned via the web portal, subject to approval. *(agreed · MoM 19 Aug 2026, 4.7 Returns, Refunds & Exchanges — In-Store and Online; 5. Key Decisions · DI-367)*
- Guests can request a refund from their account/profile; operations are notified and can approve, reject or ask for more information. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-254)*
- Refund policy shown to guests is tiered and driven by back-office rules per business, e.g. no refund <24h, 50% between 24–48h, 100% >48h. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-192)*

`GST-068` Help & My Cases

- Group ticket upgrades are business-configurable (off by default); where allowed a group raises an upgrade request (e.g. via chat/support) rather than self-serving like an individual. *(agreed · MoM 1 Sep 2026, 4.9 Clarified (group upgrades) · DI-607)*
- Cases can be logged from the customer app/website and from the call-centre/admin side, with category, priority, channel and SLA-based escalation rules. *(client request · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-390)*
- Support chat is native to TICVAI: a built-in AI chat assistant answers first, then escalates to a human "CR representative" role in the platform; offered white-labelled as a subscription add-on for smaller clients. *(agreed · MoM 12 Aug 2026, 10. Customer Support / Chat Integration Approach · DI-256)*

`GST-069` Face Pass

- **Open question.** Open: biometric data for children. Adults with consent is compliant; for minors, either exclude biometric storage entirely or allow it with a parent/guardian-signed consent form. TICVAI to answer by email. *(open · MoM 30 Sep 2026, 4.3 Open Questions Flagged by Chinmay — Invoicing/Taxation & Biometric Consent for Minors · DI-1085)*
- Web account gets device management and "sign out a lost device" (WEB-024). Face Pass stays mobile-only until the facial-reader vendor SDK supports web capture. *(agreed · design review 29 Sep 2026, GAP-D1 · D. Mobile-only features get web equivalents · DI-1077)*
- Qossai: use an existing major venue-group client's live app and published privacy policy as the model for how facial-recognition consent, data use and retention are explained to guests. *(client request · MoM 2 Sep 2026, 4.11 Privacy & Biometric Data Retention · DI-642)*
- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*
- Two face credentials: Face Pass (long-term, renewable, for memberships/season passes) and Face Tag (short-lived, single day or event). Retention is venue-configurable per tier. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-640)*

`GST-070` Reserve a Table

- The table/cabana screen becomes map-based booking: a venue map can carry cabanas, loungers, tables (beach or event tables) and other bookable resources, sold like cabanas. Dining tables stay F&B table reservations. *(agreed · design review 29 Sep 2026, GAP-C2 · C. Wave 2: Reserve a Table or Cabana (waitlist, notify) · DI-1076)*
- Cabanas are picked on the venue's ingested map, like stadium seats: numbered cabanas by zone (e.g. R01–R10, T01–T08, S01–S06, B01–B10) showing guests seated, sold-out greyed and marked. Tapping one adds it (e.g. "Cabana B09 · Large cabana · Beach, AED 1,855") and starts a remaining-time counter. Map on the first screen. *(agreed · rev 3 design review 29 Sep 2026, REV3-15 · 15. Book the product from the map (e.g. pick an available cabana) · DI-1055)*
- Dining deposit hold is a venue option, off unless enabled in Venue Management; amount and basis (per guest, per table, percentage) are venue configuration, never a hard-coded AED 100. Show the deposit step only when enabled. *(agreed · rev 3 design review 29 Sep 2026, REV3-8b · 8. deposit hold flow · DI-1049)*
- Table reservations and the waitlist do not go into the cart: after date, time and party size the guest gets a confirmation straight away ("no card needed"). *(agreed · rev 3 design review 29 Sep 2026, REV3-8 · 8. Unable to complete the table booking flow · DI-1048)*
- On the one-decision-per-screen layout, information blocks (notes, "what happens next", "what's included") stay on the screen before them and up to three quick choices share one screen. Table reservation and deposit hold become 1 screen; waitlist, takeaway, delivery, private dining enquiry 2; dinner deals 2 (party size with date/time). *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): Steps with nothing to decide · DI-1001)*
- Qossai asked if guests pick a specific table; Allam: table choice can be an option, but the default is the guest gives party size and the system/host allocates a table. *(agreed · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Dining) · DI-689)*
- **Open question.** Dining has two flows: book a table (date, time, group size, seating-area preference, occasion, allergy/special-request notes) and order food (delivery or pickup location, items, checkout). *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Dining) · DI-688)*

`GST-071` Payment Methods

- Full card numbers are never stored or shown; only a masked representation (e.g. last four digits) so the user can identify which card was used. *(agreed · MoM 31 Jul 2026, 10. Compliance & Data Protection · DI-069)*

`GST-072` Share & Group Booking

- **Open question.** Are water-park groups booked into a session (the build picks a session first)? Default built: group requests take a date and, for session-based products, a session. *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Water-park groups by session · DI-1117)*
- **Open question.** Each group ticket card shows a minimum group size; is it set per group ticket, and what values? Default built: each group ticket carries its own minimum, default 10. *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Minimum group size · DI-1116)*
- **Open question.** Do Tour operator and Community become their own group types or map to general? Default built: School, Corporate, Tour operator and Community shown as their own group types (platform also has general and party). *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Group types · DI-1115)*
- **Open question.** How many supervisors come free per group (per N guests), and is it per group ticket? Default built: supervisors are a separate, free guest type, up to 1 per 10 guests, counted on the group request. *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Supervisors · DI-1114)*
- Supervisors are listed separately and are free; the enquiry panel shows the estimate as e.g. "School group · Guests × 45". Water park group booking: pick a session, then enter the number of swimmers and supervisors. On mobile the headcount stepper has a +10 button. *(client request · design review 30 Sep 2026, 1. Group booking: product missing, enter the number of people · DI-1105)*
- Group / school booking starts with group ticket cards (School, Corporate, Tour operator, Community), each showing a per-person price and minimum group size. Then "How many people" is a number box the guest can type (e.g. 45) or step with − / +; no Group size dropdown. *(client request · design review 30 Sep 2026, 1. Group booking: product missing, enter the number of people · DI-1104)*
- Duplicate screens become one implementation covering several screen IDs (mobile Transfer + Delivery & Sharing; web Wishlist / Devices & Consent; Help Centre + Help & Accessibility as one Help view with FAQ, cases, policies, accessibility tabs). Ticket-selection functions belong on GST-008. Web gets a Group Booking view. *(agreed · design review 29 Sep 2026, GAP-D3 · D. Duplicate screens merged; group booking on web · DI-1078)*
- Group bookings: one shared QR for the whole group (redeemed together at the counter) or one QR per person, each of which the guest can link to their own profile in the mobile app. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-289)*

`GST-073` Security & Sign-in

- Web account gets device management and "sign out a lost device" (WEB-024). Face Pass stays mobile-only until the facial-reader vendor SDK supports web capture. *(agreed · design review 29 Sep 2026, GAP-D1 · D. Mobile-only features get web equivalents · DI-1077)*
- Guest two-step verification is a per-venue setting, off by default. Enrolment lives on the guest's tenant-wide account; the second factor is asked only when signing in or acting at a venue that enables it. Guests never see enterprise SSO. *(agreed · design review 29 Sep 2026, GAP-B1 · B. Login: set up two-step verification; C. Security & Sign-in (step-up auth) · DI-1072)*

`GST-074` Map Booking — Cabanas & Spots

- The table/cabana screen becomes map-based booking: a venue map can carry cabanas, loungers, tables (beach or event tables) and other bookable resources, sold like cabanas. Dining tables stay F&B table reservations. *(agreed · design review 29 Sep 2026, GAP-C2 · C. Wave 2: Reserve a Table or Cabana (waitlist, notify) · DI-1076)*
- Cabanas are picked on the venue's ingested map, like stadium seats: numbered cabanas by zone (e.g. R01–R10, T01–T08, S01–S06, B01–B10) showing guests seated, sold-out greyed and marked. Tapping one adds it (e.g. "Cabana B09 · Large cabana · Beach, AED 1,855") and starts a remaining-time counter. Map on the first screen. *(agreed · rev 3 design review 29 Sep 2026, REV3-15 · 15. Book the product from the map (e.g. pick an available cabana) · DI-1055)*
- Map-based cabana booking stays optional per configuration, since not every operator uses the same flow; it uses the same map back end as theme-park F&B/locations (reusable later for in-park navigation). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W6 Cabanas · DI-1008)*
- **Open question.** Cabanas: category (premium, VIP, luxury, private, family, couples), date/time, guest count, amenity details. Activities: desert-safari packages (buy-one-get-one, evening, Bedouin-style), pickup point, add-ons (stroller), duration packages (2-hour/4-hour). *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Cabanas, Activities) · DI-687)*

`GST-075` Book a Space by the Hour

- Meeting rooms by the hour are in scope: date → start time → length (1 hour, 2 hours, half day, full day) → room (focus pod, majlis room, boardroom, auditorium) → attendees → add-ons (coffee break, working lunch, AV technician). Price = room rate × length; the cart line shows the booked time window. *(agreed · rev 3 design review 29 Sep 2026, REV3-13 · 13. House of Wisdom: meeting room flow · DI-1053)*
- Cleaning buffer is configurable. Option A: fixed buffer (e.g. 15 min) after every booking. Option B: N cleanings per day; the system places the buffers into the day's schedule and adjusts availability. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W10 Meeting-room cleaning buffer · DI-1012)*
- Meeting-room availability is checked against date + start time + duration together; changing any of the three re-checks all rooms. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W9 Meeting rooms · DI-1011)*
- **Open question.** Resources: meeting-room booking (headcount, duration, time slot, room, add-ons tea/coffee/snacks), modelled on House of Wisdom. Merchandise: browse, cart with add/remove quantity, pickup or doorstep delivery. F&B: outlet/menu browsing; collect at counter, curbside, doorstep or priority delivery. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Resources, Merchandise, F&B) · DI-690)*
- UX reference: House of Wisdom (Sharjah library) meeting-room/"pod" booking and tiered membership plans — a simple duration-based booking flow without fixed performances/time slots — to be reviewed by Chinmay/Aishwarya. *(client request · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 6. Open Items · DI-506)*
- A bookable resource such as a meeting room can be priced per hour: total price is calculated from the booked duration and the room is blocked for that window so no other guest can book it. *(client request · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A · DI-503)*
- Resources are one-to-one (dedicated to a booking) or shared (e.g. a meeting room with bookable pods, a vehicle across sequential slots); further sales are blocked once a shared resource's capacity/slot is full and reopened if a booking is cancelled. *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-496)*

`GST-076` Intercity Trip — Route & Schedule

- **Open question.** Should each popular-route card's starting fare, featured order and image or badge be set per route in the back office? Default built: routes carry a featured order and an image; the starting fare is computed from the lowest fare. *(open · Decisions Register 1 Oct 2026, Questions for the client — Transport / Popular routes card · DI-1119)*
- Transport "Popular routes" card view: cards per route (e.g. Dubai to Abu Dhabi, Sharjah to Dubai, Abu Dhabi to Al Ain, Dubai to Fujairah) styled like the dated ticket cards, each with the "from" fare and a Book button. Book → date → departures → passengers. On mobile it is the first transport product. *(client request · design review 30 Sep 2026, 6. Proposed UI: route cards with a Book button · DI-1111)*
- Transport passengers appear only after a departure is chosen (performance first, then tickets). *(client request · design review 30 Sep 2026, 5. Transport: route already chosen, but stations were empty · DI-1110)*
- A route flow opens with its stations filled in (e.g. Abu Dhabi Central Bus Station → Al Ain Central Bus Station, still changeable/swappable) and departures show straight away without Search Trips. Time-period buttons act as a filter; tapping one again shows all departures. *(client request · design review 30 Sep 2026, 5. Transport: route already chosen, but stations were empty · DI-1109)*
- Transport (intercity coach) follows the RTA layout: "3 Simple Steps" (Route & Schedule → Seat Selection → Payment), tabs One-way Trip / Multi-Trip / Favourite, one row with From (swap), To, Date & Time, Passengers; departure cards (arrival, duration, seats left, fare); price card beside a street map of the route. *(agreed · rev 3 design review 29 Sep 2026, REV3-21 · 21. Sell transport tickets (one trip, multi trip, favourites, stations, route map) · DI-1061)*

`GST-077` Intercity Trip — Route & Passengers

- Transport passengers appear only after a departure is chosen (performance first, then tickets). *(client request · design review 30 Sep 2026, 5. Transport: route already chosen, but stations were empty · DI-1110)*
- A route flow opens with its stations filled in (e.g. Abu Dhabi Central Bus Station → Al Ain Central Bus Station, still changeable/swappable) and departures show straight away without Search Trips. Time-period buttons act as a filter; tapping one again shows all departures. *(client request · design review 30 Sep 2026, 5. Transport: route already chosen, but stations were empty · DI-1109)*
- Transport (intercity coach) follows the RTA layout: "3 Simple Steps" (Route & Schedule → Seat Selection → Payment), tabs One-way Trip / Multi-Trip / Favourite, one row with From (swap), To, Date & Time, Passengers; departure cards (arrival, duration, seats left, fare); price card beside a street map of the route. *(agreed · rev 3 design review 29 Sep 2026, REV3-21 · 21. Sell transport tickets (one trip, multi trip, favourites, stations, route map) · DI-1061)*

`GST-078` Intercity Trip — Multi-trip Passes

- Transport (intercity coach) follows the RTA layout: "3 Simple Steps" (Route & Schedule → Seat Selection → Payment), tabs One-way Trip / Multi-Trip / Favourite, one row with From (swap), To, Date & Time, Passengers; departure cards (arrival, duration, seats left, fare); price card beside a street map of the route. *(agreed · rev 3 design review 29 Sep 2026, REV3-21 · 21. Sell transport tickets (one trip, multi trip, favourites, stations, route map) · DI-1061)*

`GST-079` Intercity Trip — Favourite Routes

- Transport (intercity coach) follows the RTA layout: "3 Simple Steps" (Route & Schedule → Seat Selection → Payment), tabs One-way Trip / Multi-Trip / Favourite, one row with From (swap), To, Date & Time, Passengers; departure cards (arrival, duration, seats left, fare); price card beside a street map of the route. *(agreed · rev 3 design review 29 Sep 2026, REV3-21 · 21. Sell transport tickets (one trip, multi trip, favourites, stations, route map) · DI-1061)*

## P04 Venue POS

**Platform-wide**

- No driver is ever installed on the workstation OS: drivers are built into the TICVAI app; staff only connect the device and test print/scan from within the app; new models are supported by a back-end driver update, not a code release. *(agreed · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-897)*
- Qossai: dim/fade the background ("foggy") when a side panel or modal opens so the cashier's attention stays on the active task. *(client request · MoM 9 Sep 2026, 4.13 POS Prototype Review - Home Screen, Ticketing Cart & Link-to-Sale UX · DI-785)*
- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*
- Funding approval rules: a top-up above a configured threshold requires supervisor or finance approval via supervisor login. Top-up reversal (full or partial, back to the original payment method) requires manual verification/authorisation before processing. *(agreed · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-520)*
- Top-up rules set minimum and maximum amounts per transaction; channel/funding-source mapping restricts which payment methods each channel offers (e.g. cash top-up on-site only, not online), so each channel's top-up screen offers only its allowed methods. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-517)*
- Confirmed: a guest always books a product or package — never a resource (a specific room, vehicle or instructor by itself) directly — on every sales channel, including the guest/mobile app; the product's configuration determines which resources are booked behind the scenes. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-502)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*
- Staff-facing POS and tablet UIs always carry TICVAI branding, not client branding. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-296)*
- Ticketing, F&B and retail share one cart and checkout, one unified receipt and one QR/wristband per customer — no separate receipts or wristbands per product line. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-293)*
- Each device gets a unique workstation ID, but what a user sees is set by their role, not the device: e.g. a cashier sees the full park ticket range at a main-gate POS but only the F&B menu at a restaurant POS. Applies to the roaming "flying" POS too. *(agreed · MoM 12 Aug 2026, 2. Flying POS Setup and Permission Configuration · DI-246)*
- Built-in help menu with step-by-step tutorials with screenshots for common tasks (e.g. how to sell a ticket at the POS). *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-160)*
- In-system task assignment between staff (e.g. a cashier flagging something for a supervisor) without email or messaging apps. *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-159)*
- A single cart/order must take mixed purchases (e.g. family tickets plus gift vouchers) with one unified checkout and identity capture. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-141)*
- F&B is reached from the same top-level navigation as other experiences (tours, guides); table management only appears for venues with a restaurant configuration. *(client request · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-107)*
- Allam: the cashier design must work consistently across all cashier device types: POS terminals, tablets, iPads and kiosks. *(agreed · MoM 3 Aug 2026, 3. UX Design Approach Discussion · DI-101)*
- Prefer the demoed cleaner, better-spaced layout over the cluttered PDF: adequate spacing and large touch targets to prevent mis-taps on touchscreens and tablets. *(agreed · MoM 3 Aug 2026, 3. UX Design Approach Discussion · DI-100)*
- Shift-level settings: light/dark mode, currency selection (displayed pricing follows the cashier's location), language selection, screen brightness, and manual online/offline toggling. *(agreed · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-098)*
- Notification system with ticket alerts (cancellations, capacity nearing or at its limit) and system alerts (printer offline, POS offline). *(client request · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-093)*
- Embedded AI assistant the cashier can query directly, e.g. to find today's promo code, process a refund, or switch between light/night themes. *(agreed · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-092)*
- Header metrics show tickets sold and revenue for the current shift. *(client request · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-090)*
- **Open question.** Allam: alongside search, provide always-visible "hot function" buttons for high-frequency actions (refund, check transaction, print last receipt). Softlabs to recommend the right balance of hot buttons and search. *(open · MoM 3 Aug 2026, 3. UX Design Approach Discussion · DI-088)*
- A prominent search ("magic banner") lets the cashier reach functionality such as refunds or resending a ticket by searching, rather than through static menus or sidebars. *(client request · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-087)*
- Qossai's demoed cashier interface is the primary reference/baseline, to be enhanced and redesigned enough that it does not look like a copy while keeping its UX ideas; the earlier AI-generated PDF is secondary colour/theme inspiration only. *(agreed · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-086)*
- The POS/tablet application carries TICVAI's own branding and UI direction; the B2C and B2B mobile applications are white-label by design. *(agreed · MoM 31 Jul 2026, 15. Monday UI/UX Session Planning · DI-084)*
- POS product names and menus may be Arabic-only for certain regions. *(client request · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-082)*
- Selling a capacity-based product (e.g. seat-assigned tickets) while offline is blocked with a clear notification, never allowed through or silently failing; non-capacity products stay sellable offline. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-074)*
- Qossai: the POS raises an alert when a venue goes offline. *(client request · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-073)*
- Offline state must be clearly visible in the UI, e.g. a visible mode indicator or greyed-out unavailable functions; exact visual treatment to be settled in the UI/UX session. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-072)*
- Allam: the app detects loss of connectivity and switches to offline mode automatically, without cashier action, then restores online mode and syncs pending transactions automatically. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-071)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Full card numbers are never stored or shown; only a masked representation (e.g. last four digits) so the user can identify which card was used. *(agreed · MoM 31 Jul 2026, 10. Compliance & Data Protection · DI-069)*
- Allam: the platform is device-agnostic (Android, iOS and web) so sales can continue on any available device. *(agreed · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-068)*
- **Open question.** Qossai asked whether a cashier on a tablet could use the POS via a browser URL. A lightweight web POS will be considered; it would have no offline support (installed thick client required for offline). *(open · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-067)*
- **Open question.** POS catalogue: Chinmay's middle ground is an online real-time catalogue that falls back automatically to the last-synced catalogue if connectivity is lost; local-first vs online-first still to be compared (case study). *(open · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-066)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- POS: sell tickets, memberships, F&B, retail and services from one unified cashier experience. Access Control: real-time entry validation, occupancy monitoring, offline mode and gate management. *(agreed · Design Vision Book 29 Jul 2026, 07 Modules Overview (p7) - 04 Point of Sale; 03 Access Control · DI-035)*
- Selling reference layout: clean top navigation; category tabs with counts (All Events 32, Exhibitions, Guided Tours ...); sort and type chips (Price, Rating, Popular; General, Seated, Multipass, Scheduled, Rental); content cards with large image, type badge, rating, tags (LIMITED, NEW, BESTSELLER), availability ("180 available", "11 left") and "from" price; persistent cart on the right with member discount, totals and "Checkout Securely". *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, items 2-5 · DI-026)*
- POS must keep selling general admission tickets during an internet outage, and access-control apps must keep scanning and validating tickets during a connectivity failure. *(agreed · MoM 28 Jul 2026, 15. Offline POS and Access-Control Operations · DI-012)*

**Sell**

- A guest is not repeatedly re-offered something already declined (e.g. a fast pass rejected three times), and an offer ignored online is not re-presented on another channel, e.g. at POS after the guest bought it there. *(agreed · MoM 21 Sep 2026, 4.6 Personalized Offer Delivery & Omni-Channel Orchestration · DI-962)*
- Navigation depends on ticket type: admission has no date/time and goes straight to quantity/cart; dated asks date only; timed asks date then time; seated asks date, then time, then seat. *(agreed · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-116)*
- Add-to-cart offers upsell add-ons, including an AI-generated upsell prompt (e.g. suggesting the cashier add two more items to unlock a bundle discount). *(client request · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-096)*
- A "Build Your Experience" workflow helps cashiers sell bundled experiences without searching through hundreds of ticket types. *(client request · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-010)*
- POS allows notes to be added against individual tickets in the cart. *(client request · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-005)*

**Screen by screen**

`POS-000` Sign In

- Denomination/shift-open steps apply only when a cashier begins a shift - not on every login or return from break. *(agreed · MoM 9 Sep 2026, 4.12 POS Prototype Review - Login, Shift-Open, Denomination & Hardware Validation · DI-777)*
- Cashier login must not list every cashier (20+ doesn't scale): show recently logged-in cashiers as quick-tap tiles in a swipeable row (Qossai: e.g. 4 visible, swipe for more), plus a manual cashier ID + PIN option for anyone not shown. *(agreed · MoM 9 Sep 2026, 4.12 POS Prototype Review - Login, Shift-Open, Denomination & Hardware Validation · DI-774)*
- Access loads automatically at login on POS and web/admin. A user with one role logs straight in; a user with several roles (e.g. admin, cashier, supervisor, manager) is prompted to choose which role to use. *(agreed · MoM 12 Aug 2026, 4. Multiple Roles per User and Role Switching · DI-249)*
- One user per session per workstation: a second user cannot sign in over an active session; the cashier taking a break must log out or suspend their shift first. *(agreed · MoM 12 Aug 2026, 1. POS Session Management and Break Handling · DI-245)*
- A user can hold several roles and switch between them at login (e.g. cashier vs supervisor). *(agreed · MoM 7 Aug 2026, 4. Roles & User Management · DI-152)*
- Each workstation records its connected devices (receipt printer, barcode scanner, ticket printer) so a cashier signing in there gets the right hardware automatically; every workstation has its own activity log and rights. *(agreed · MoM 7 Aug 2026, 3. Operating Areas, Workstations & Permissions Hierarchy · DI-150)*

`POS-001` Begin Shift

- Hardware checks (printer, cash drawer, terminal connectivity) run automatically at shift start as a "boot-up checklist", in parallel with denomination entry, never discovered mid-transaction; a peripheral/hardware test screen validates devices before shift start. *(agreed · MoM 9 Sep 2026, 4.12 POS Prototype Review - Login, Shift-Open, Denomination & Hardware Validation · DI-778)*
- Denomination/shift-open steps apply only when a cashier begins a shift - not on every login or return from break. *(agreed · MoM 9 Sep 2026, 4.12 POS Prototype Review - Login, Shift-Open, Denomination & Hardware Validation · DI-777)*
- Denomination count (Allam): add a manual numeric entry field as an alternative to repeated increment taps (e.g. type "50" for 50 notes instead of tapping fifty times). *(agreed · MoM 9 Sep 2026, 4.12 POS Prototype Review - Login, Shift-Open, Denomination & Hardware Validation · DI-776)*
- Denomination count (Allam): show a currency note/coin image alongside each denomination, not numeric labels alone, for faster visual entry. *(agreed · MoM 9 Sep 2026, 4.12 POS Prototype Review - Login, Shift-Open, Denomination & Hardware Validation · DI-775)*
- Opening float entered either as a total amount or by denomination, configurable per venue. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-307)*
- Denominations configurable per currency/region (e.g. UAE 500, 200, 100, 50, 20; Bahrain has no 1000); amounts use 2 decimals (UAE) or 3 (Bahrain/Kuwait) with no rounding of the third decimal (2.013 stays 2.013). *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-306)*
- One user per session per workstation: a second user cannot sign in over an active session; the cashier taking a break must log out or suspend their shift first. *(agreed · MoM 12 Aug 2026, 1. POS Session Management and Break Handling · DI-245)*

`POS-002` Sell — Ticket Catalogue

- When a ticket/membership is for someone else (e.g. a parent buying a ski lesson for a child), the end user's details (name, date of birth, etc.) are captured on the ticket itself, while "link to sale" records the purchaser - who may or may not be the same person. *(client request · MoM 9 Sep 2026, 4.14 POS Prototype Review - Discounts, Membership Capture & Split Payment · DI-787)*
- All discounts and promotions (percentage, fixed amount, promo codes, employee/friends-and-family codes) are applied on the sell/cart screen, never on the payment screen, which only completes payment. *(agreed · MoM 9 Sep 2026, 4.14 POS Prototype Review - Discounts, Membership Capture & Split Payment · DI-786)*
- Mobile number (or email) is the primary search key for linking a guest - name alone is impractical (many customers named "Mohammed"); capture the mobile early and proactively suggest a match if one exists. *(agreed · MoM 9 Sep 2026, 4.13 POS Prototype Review - Home Screen, Ticketing Cart & Link-to-Sale UX · DI-784)*
- "Link to sale": a search field directly on the cart screen finds and links an existing guest profile or creates a new one inline, without leaving the cart - replacing the separate link-customer screen. *(agreed · MoM 9 Sep 2026, 4.13 POS Prototype Review - Home Screen, Ticketing Cart & Link-to-Sale UX · DI-783)*
- Multiple concurrent carts via a "+" button so the cashier can manage several customers at once. *(agreed · MoM 9 Sep 2026, 4.13 POS Prototype Review - Home Screen, Ticketing Cart & Link-to-Sale UX · DI-782)*
- Ticketing flow: category (attraction, cinema, event, passes, vouchers) -> date/time slot -> quantity -> add-ons, all feeding a persistent cart. *(agreed · MoM 9 Sep 2026, 4.13 POS Prototype Review - Home Screen, Ticketing Cart & Link-to-Sale UX · DI-781)*
- Quantity/purchase limits can be set per order, per guest, per account category and per sales channel (e.g. maximum 6 tickets per transaction). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-464)*
- Open-dated ticket: name, description, price and validity period (e.g. 1 day, 1 month, 6 months), with a configurable reservation rule controlling whether customer details (name, email, phone) are captured at point of sale. *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-445)*
- Ticket attributes such as minimum age, ID-proof requirements (e.g. Emirates ID for UAE-resident tickets, with format validation or photo upload; passport; handicap/PoD documentation) or an embedded ID-reader for on-site verification are configurable per ticket and region, not fixed. *(agreed · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference; 5. Key Decisions · DI-443)*
- Guest information capture (name, mobile number, nationality, visit survey, etc.) is configurable per ticket type; even an open-dated admission ticket can optionally collect it. *(agreed · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough; 5. Key Decisions · DI-434)*
- The UI reference for ticketing POS design is the previously shared demo software link; the earlier PDF was based on an outdated UI and no separate POS/ticketing PDF exists. *(agreed · MoM 14 Aug 2026, 13. Outstanding Deliverables and Next Steps · DI-313)*
- For small groups (2–4) the cashier can assign specific meals to specific tickets at sale; for large groups the group redeems centrally at the counter instead. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-290)*
- Group bookings: one shared QR for the whole group (redeemed together at the counter) or one QR per person, each of which the guest can link to their own profile in the mobile app. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-289)*
- Each workstation is linked to a front-end "sales board" (e.g. of ten: five ticketing, three F&B, two retail); signing in on it opens the matching front end automatically. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-247)*
- Dynamic offers apply automatically without a code (buy-2-get-1-free, buy-3-get-2-at-50%-off, fixed amount off a minimum quantity); the discounted item is added to the cart automatically with its price adjusted (e.g. to zero). *(agreed · MoM 7 Aug 2026, 17. Promotions & Dynamic Offers · DI-174)*
- Minimum/maximum sellable quantity per customer (e.g. a promotional bundle requiring at least two) must be enforced at selection. *(agreed · MoM 7 Aug 2026, 16. Entitlement Components: Re-entry, Expiration & Sale Restrictions · DI-172)*
- POS assistant: the cashier asks in their own words and stays on the screen. The minute's examples: find today's promo code, process a refund, switch to the night theme. *(client request · MoM 3 Aug 2026, Point-of-Sale (Cashier) UI Walkthrough · DI-133)*
- **Open question.** POS hot functions are not settled: Allam proposed a hybrid of always-visible buttons and a search-driven "magic banner" and asked Softlabs to recommend the balance; Qossai agreed a combination might be ideal and deferred. The minute names Refund, Check transaction and Print last receipt. *(open · MoM 3 Aug 2026, UX Design Approach Discussion · DI-132)*
- Booking steps follow the product type: admission goes straight to quantity; dated products to a date, timed ones on to a time, then quantity; seated products to zone, then seats on a seat map, then quantity by variant (adult, child, concession). *(agreed · MoM 3 Aug 2026, Ticket Flow Variations by Product Type · DI-131)*
- On the POS the cashier stays on the sell screen: date/session and seat selection are steps in a drawer on POS-002, replacing full-page navigation (POS-003, POS-004). Whether a full-screen seat map is still wanted on a tablet is undecided. *(agreed · MoM 3 Aug 2026, Point-of-Sale (Cashier) UI Walkthrough · DI-130)*
- Slide-in "drawer" for ticket details instead of full-page navigation: selecting a ticket opens a drawer showing inclusions and rules/restrictions, then date/time selection and, where relevant, seat selection. *(agreed · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-094)*
- A right-hand panel surfaces events, tour guides and packages, with filtering across exhibitions, tours and films. *(client request · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-089)*
- POS supports multiple active carts, with holding and resuming carts. *(client request · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-006)*
- POS product and ticket browsing with filtering by event type, pricing and other criteria. *(client request · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-002)*

`POS-003` Sell — Timed Entry

- When a ticket/membership is for someone else (e.g. a parent buying a ski lesson for a child), the end user's details (name, date of birth, etc.) are captured on the ticket itself, while "link to sale" records the purchaser - who may or may not be the same person. *(client request · MoM 9 Sep 2026, 4.14 POS Prototype Review - Discounts, Membership Capture & Split Payment · DI-787)*
- Multiple concurrent carts via a "+" button so the cashier can manage several customers at once. *(agreed · MoM 9 Sep 2026, 4.13 POS Prototype Review - Home Screen, Ticketing Cart & Link-to-Sale UX · DI-782)*
- Ticketing flow: category (attraction, cinema, event, passes, vouchers) -> date/time slot -> quantity -> add-ons, all feeding a persistent cart. *(agreed · MoM 9 Sep 2026, 4.13 POS Prototype Review - Home Screen, Ticketing Cart & Link-to-Sale UX · DI-781)*
- Start/stop-sell per channel: e.g. a distant desert safari allows no same-day online booking (next day minimum), while onsite stays open to sell-out or a cutoff (e.g. 15 minutes before a timed show). Guest date/time pickers must reflect the channel's window. *(client request · MoM 31 Aug 2026, 4.11 Sales schedule & validity · DI-583)*
- The UI reference for ticketing POS design is the previously shared demo software link; the earlier PDF was based on an outdated UI and no separate POS/ticketing PDF exists. *(agreed · MoM 14 Aug 2026, 13. Outstanding Deliverables and Next Steps · DI-313)*
- POS flow order: select performance/time slot (live remaining capacity) → add product → attach a reservation account (search existing or create; mandatory/optional fields from data-mask config) → add-ons → checkout → per-ticket owner details where required → payment → printed ticket and booking reference. Modern UI required. *(agreed · MoM 7 Aug 2026, 20. Live Point-of-Sale Transaction Walkthrough · DI-177)*
- POS sells a timed slot only until its "minutes on screen" window after start time closes. *(agreed · MoM 7 Aug 2026, 14. Events, Integrations & Performances (Time Slots) · DI-169)*
- On the POS the cashier stays on the sell screen: date/session and seat selection are steps in a drawer on POS-002, replacing full-page navigation (POS-003, POS-004). Whether a full-screen seat map is still wanted on a tablet is undecided. *(agreed · MoM 3 Aug 2026, Point-of-Sale (Cashier) UI Walkthrough · DI-130)*
- Slide-in "drawer" for ticket details instead of full-page navigation: selecting a ticket opens a drawer showing inclusions and rules/restrictions, then date/time selection and, where relevant, seat selection. *(agreed · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-094)*
- POS shows calendar, capacity and time-slot visibility when selling, alongside seat-selection workflows. *(client request · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-003)*

`POS-004` Sell — Seat Map

- Decision: three seat-selection models, selectable per section, per event: (1) zone/capacity selling with no seat numbers (guest told zone only); (2) system-assigned "best available" — guest picks section + quantity, seats disclosed later; (3) full customer seat selection. *(agreed · MoM 21 Aug 2026, 4.1 Reference Walkthrough; 4.2 Seat Map Builder; 5. Key Decisions · DI-410)*
- The UI reference for ticketing POS design is the previously shared demo software link; the earlier PDF was based on an outdated UI and no separate POS/ticketing PDF exists. *(agreed · MoM 14 Aug 2026, 13. Outstanding Deliverables and Next Steps · DI-313)*
- Movie/cinema ticketing is in scope through the seat management module (e.g. a Kuwait museum's educational cinema: assigned seats, a film, a time slot). *(agreed · MoM 14 Aug 2026, 5. Movie Ticketing · DI-286)*
- Qossai: for seated/zoned venues, POS terminals on the same network share real-time seat state; a disconnected network needs its own offline zone. Whether zoning is automatic or client-enabled is a per-venue setting. *(client request · MoM 5 Aug 2026, 8. Offline Selling Rules · DI-143)*
- On the POS the cashier stays on the sell screen: date/session and seat selection are steps in a drawer on POS-002, replacing full-page navigation (POS-003, POS-004). Whether a full-screen seat map is still wanted on a tablet is undecided. *(agreed · MoM 3 Aug 2026, Point-of-Sale (Cashier) UI Walkthrough · DI-130)*
- Seat selection supports configurable seating rules, e.g. requiring a group's seats to stay together. *(client request · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-095)*
- Slide-in "drawer" for ticket details instead of full-page navigation: selecting a ticket opens a drawer showing inclusions and rules/restrictions, then date/time selection and, where relevant, seat selection. *(agreed · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-094)*
- POS shows calendar, capacity and time-slot visibility when selling, alongside seat-selection workflows. *(client request · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-003)*

`POS-005` Payment

- Split payment without an "enable split" mode: enter an amount on one tender (e.g. AED 200 cash), tap "add to split", pick the next tender which auto-shows the remaining balance; the complete-transaction button enables once the full amount is allocated. *(agreed · MoM 9 Sep 2026, 4.14 POS Prototype Review - Discounts, Membership Capture & Split Payment · DI-788)*
- All discounts and promotions (percentage, fixed amount, promo codes, employee/friends-and-family codes) are applied on the sell/cart screen, never on the payment screen, which only completes payment. *(agreed · MoM 9 Sep 2026, 4.14 POS Prototype Review - Discounts, Membership Capture & Split Payment · DI-786)*
- The same wristband or enrolled face works as stored-value payment for F&B and retail: balance checked and deducted automatically at the point of sale; top-up via the same credential. *(client request · MoM 2 Sep 2026, 4.12 Media as a Payment Method · DI-643)*
- Affiliated-hotel guests get a zero-value ticket/wristband after room-number lookup and identity verification, or charge on-site purchases to their room via the same lookup (PMS such as Opera). *(client request · MoM 2 Sep 2026, 4.9 Hotel/PMS integration · DI-638)*
- For a fully dynamic-QR event, even POS-purchased tickets are delivered by email/SMS with instructions to download the app and link the ticket, not printed as a static QR on the spot. *(agreed · MoM 2 Sep 2026, 4.7 Dynamic QR Code - Business Flexibility & Exceptions · DI-634)*
- Split tender: one purchase paid with wallet balance plus another method, e.g. AED 500 from the wallet and the remaining AED 200 of a AED 700 purchase on a credit card. *(agreed · MoM 27 Aug 2026, 4.7 Split-Tender, Redemption Rules & Configuration Simulation · DI-525)*
- Donation campaigns: fixed or variable amounts, enabled per sales channel, triggered on a specific product or across all products, proceeds tracked to a separate account code. *(client request · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies · DI-471)*
- Foreign-currency tender is recorded at its base-currency equivalent at the time of sale; change and refunds are always given in base/local currency, never the tendered currency; a separate report shows each cashier's foreign-currency activity. *(agreed · MoM 14 Aug 2026, 2. Finance — Currency Locking for Refunds · DI-282)*
- POS applies the same foreign-currency display/charge logic, records in base currency, and has a report of total foreign-currency collections by currency. *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-213)*
- POS flow order: select performance/time slot (live remaining capacity) → add product → attach a reservation account (search existing or create; mandatory/optional fields from data-mask config) → add-ons → checkout → per-ticket owner details where required → payment → printed ticket and booking reference. Modern UI required. *(agreed · MoM 7 Aug 2026, 20. Live Point-of-Sale Transaction Walkthrough · DI-177)*
- "Virtual credit card" tender for standalone card terminals not integrated with the system: the cashier types the authorisation code returned by the physical terminal, keeping reporting accurate. *(client request · MoM 7 Aug 2026, 5. Base Parameters: Devices & Payment Methods · DI-154)*
- Table/seat-level structure supports flexible bill-splitting: by amount, by number of covers, or by category (e.g. one guest pays food, another drinks). *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-106)*
- Apple Pay / Google Pay tap-to-pay are the primary regional digital payment methods; UPI-style QR payments may come later, not in initial scope. *(agreed · MoM 31 Jul 2026, 12. Payments & Regional Preferences · DI-079)*
- Only cash payments are available while offline; card payment requires connectivity. *(agreed · MoM 31 Jul 2026, 12. Payments & Regional Preferences · DI-078)*
- POS cashier can associate a customer with the transaction and apply discounts and promotional benefits; checkout supports cash and other methods. *(client request · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-004)*

`POS-006` Held Orders

- Multiple in-progress carts can be held, plus a transaction history view supporting delete, expire and merge actions. *(client request · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-091)*
- POS provides cart and transaction history, order search and refund processing. *(client request · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-007)*
- POS supports multiple active carts, with holding and resuming carts. *(client request · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-006)*

`POS-007` Close Shift

- **Open question.** Open (Qossai): many venues deliberately never show the cashier their expected sales total during the shift or at close (fraud prevention; finance's independent count catches variances). Whether the POS shows it is deferred to Qossai/Allam. *(open · MoM 9 Sep 2026, 4.18 POS Prototype Review - Shift Close & Cash Variance Handling · DI-806)*
- **Open question.** Open (Chinmay): if the supervisor is unavailable, may the cashier log out with the variance logged for later review rather than being blocked? Deferred to Qossai/Allam. *(open · MoM 9 Sep 2026, 4.18 POS Prototype Review - Shift Close & Cash Variance Handling · DI-805)*
- A flagged variance routes to a supervisor for PIN-based approve/reject; if rejected the cashier rechecks and resubmits, and can only close the shift once approved. *(client request · MoM 9 Sep 2026, 4.18 POS Prototype Review - Shift Close & Cash Variance Handling · DI-804)*
- Shift close repeats the denomination count as a blind count; on a variance the cashier must pick a reason (till error, unrecorded refund, miscount, other) and add a comment before the shift can close. *(client request · MoM 9 Sep 2026, 4.18 POS Prototype Review - Shift Close & Cash Variance Handling · DI-803)*
- Denomination count (Allam): add a manual numeric entry field as an alternative to repeated increment taps (e.g. type "50" for 50 notes instead of tapping fifty times). *(agreed · MoM 9 Sep 2026, 4.12 POS Prototype Review - Login, Shift-Open, Denomination & Hardware Validation · DI-776)*
- Denomination count (Allam): show a currency note/coin image alongside each denomination, not numeric labels alone, for faster visual entry. *(agreed · MoM 9 Sep 2026, 4.12 POS Prototype Review - Login, Shift-Open, Denomination & Hardware Validation · DI-775)*
- Shift management: assignment and scheduling by cashier/department, templates and policies, opening/closing, exceptions/alerts. Allam: explore merging shift-closing and till-closing screens to reduce dashboard count. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-309)*
- Shift closure needs supervisor authorisation, prints a denomination-itemised closing receipt and emails the closing report to finance/leadership automatically. *(agreed · MoM 12 Aug 2026, 19. Cash/Shift and Till Management · DI-272)*
- Blind cash-out: when closing, the cashier does not see the expected total; the system flags shortage/overage for supervisor review and can optionally block shift closure until the variance is resolved or explained. *(agreed · MoM 12 Aug 2026, 19. Cash/Shift and Till Management · DI-271)*
- One user per session per workstation: a second user cannot sign in over an active session; the cashier taking a break must log out or suspend their shift first. *(agreed · MoM 12 Aug 2026, 1. POS Session Management and Break Handling · DI-245)*
- End-of-shift reconciliation: the cashier enters cash on hand and reviews a shift summary before confirming it for reporting and audit. *(agreed · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-099)*

`POS-008` Reports

- **Open question.** Open (Qossai): many venues deliberately never show the cashier their expected sales total during the shift or at close (fraud prevention; finance's independent count catches variances). Whether the POS shows it is deferred to Qossai/Allam. *(open · MoM 9 Sep 2026, 4.18 POS Prototype Review - Shift Close & Cash Variance Handling · DI-806)*
- Whether a cashier sees revenue/report figures is a configurable on/off permission per role: some clients let cashiers see limited metrics (e.g. tickets sold), others only what they billed; a standalone outlet manager (e.g. F&B) may see their outlet's reporting from the POS. *(agreed · MoM 9 Sep 2026, 4.17 POS Prototype Review - Reports, Settings, Peripherals & Role-Based Access · DI-802)*
- POS reports: overall sales/revenue by ticketing, F&B, retail and other categories; terminal health; outlet performance (sales, tax, averages); attraction utilisation; plus a notifications panel. *(client request · MoM 9 Sep 2026, 4.17 POS Prototype Review - Reports, Settings, Peripherals & Role-Based Access · DI-799)*
- Foreign-currency tender is recorded at its base-currency equivalent at the time of sale; change and refunds are always given in base/local currency, never the tendered currency; a separate report shows each cashier's foreign-currency activity. *(agreed · MoM 14 Aug 2026, 2. Finance — Currency Locking for Refunds · DI-282)*
- End-of-day reports: cashier shift, till, sales by location, payment type summary, cash management, variance, refund, and consolidated end-of-day (e.g. expected 8,480 AED vs deposited 8,460 AED = 20 AED shortage, posted to an overage/shortage account visible at month-end). *(agreed · MoM 12 Aug 2026, 20. End-of-Day Reports and Overage/Shortage Handling · DI-275)*
- POS applies the same foreign-currency display/charge logic, records in base currency, and has a report of total foreign-currency collections by currency. *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-213)*
- Cashier Sales Summary dashboard scoped to the signed-in cashier: transactions, payment totals, voids/refunds and a time-based activity chart. *(agreed · MoM 7 Aug 2026, 21. Dashboards & Reporting · DI-181)*

`POS-009` Staff Roster

- Shift management: assignment and scheduling by cashier/department, templates and policies, opening/closing, exceptions/alerts. Allam: explore merging shift-closing and till-closing screens to reduce dashboard count. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-309)*

`POS-010` Add to Existing Ticket

- Upgrade eligibility checks validity/usage. Cases: seated ticket to a better section same day, paying the difference at the counter; general admission to season pass with the amount paid credited. Windows: before use, after use within a window, or until a cutoff (event ticket until the guest exits). *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-603)*
- The till can add an item to an existing ticket (e.g. a locker) after the sale; not in the delivered mockups. *(agreed · MoM 14 Aug 2026, (cited as CF-58 in POS-010 notes) · DI-314)*
- Add-on entitlements (e.g. a locker) are linked to the existing ticket QR by scanning it, not issued as a new QR. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-295)*

`POS-011` Returns, Refunds & Exchanges

- Qossai: a free-text notes field alongside preset reason codes so the cashier/supervisor can document a refund's circumstances (e.g. cancelling a ticket already validated at entry) for later audit. *(agreed · MoM 9 Sep 2026, 4.16 POS Prototype Review - Retail, Refund/Void & Offline Sync · DI-797)*
- Refund/void: refund to original tender or as store credit, with a reason code (wrong item, guest cancellation, etc.); business rules configure whether an order can be cancelled once placed. *(client request · MoM 9 Sep 2026, 4.16 POS Prototype Review - Retail, Refund/Void & Offline Sync · DI-796)*
- End-of-visit unload/refund: a guest can unload the remaining balance at a counter after a balance check. Configurable venue-level toggle, not always on. *(agreed · MoM 27 Aug 2026, 4.10 Transfers, Fraud/Risk Controls · DI-535)*
- In-park returns are operational: the return policy (e.g. allowed within 1 or 7 business days) is printed on the receipt, and guests are directed to a service counter. *(client request · MoM 19 Aug 2026, 4.7 Returns, Refunds & Exchanges — In-Store and Online · DI-366)*
- Foreign-currency tender is recorded at its base-currency equivalent at the time of sale; change and refunds are always given in base/local currency, never the tendered currency; a separate report shows each cashier's foreign-currency activity. *(agreed · MoM 14 Aug 2026, 2. Finance — Currency Locking for Refunds · DI-282)*
- A refund started at the POS is routed for approval before it reaches the bank. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-253)*
- Refunds use preset time-banded percentages (e.g. full refund a set number of days before the event, less closer to/after it), support partial refunds, and let an authorised approver apply a custom override percentage. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-252)*
- POS provides cart and transaction history, order search and refund processing. *(client request · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-007)*

`POS-013` Mobile POS, Event Sales & Offline Operations

- Offline transactions sync automatically when connectivity returns (no manual sync action); while offline the cashier's transaction view shows only transactions completed locally during that offline period. *(agreed · MoM 9 Sep 2026, 4.16 POS Prototype Review - Retail, Refund/Void & Offline Sync · DI-798)*
- Offline mode switches on automatically when connectivity is lost; each offline-capable node sells from a pre-allocated quota (e.g. 100 tickets per node) that is reallocated after reconnect and sync. *(agreed · MoM 5 Aug 2026, 8. Offline Selling Rules · DI-142)*

`POS-014` Sales Exceptions, Controls & Operational Actions

- Qossai: a free-text notes field alongside preset reason codes so the cashier/supervisor can document a refund's circumstances (e.g. cancelling a ticket already validated at entry) for later audit. *(agreed · MoM 9 Sep 2026, 4.16 POS Prototype Review - Retail, Refund/Void & Offline Sync · DI-797)*
- F&B Controls configure approval workflows globally (e.g. void approval, refund approval) based on amount thresholds and user privileges. *(client request · MoM 18 Aug 2026, 4.3 Kitchen & Preparation Stations · DI-324)*

`POS-015` Cash Operations Dashboard

- Till/cash management shows total cash and card transactions and variance tracking, and supports cash-in/cash-out for mid-shift cash pickups. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-308)*
- Shift/session view shows open and closed sessions per workstation with expected cash and card totals; a live till monitor shows real-time cash status per workstation and open/close codes. *(agreed · MoM 12 Aug 2026, 19. Cash/Shift and Till Management · DI-273)*

`POS-016` Till Configuration

- Deployment info on the terminal shows terminal version, sync status and installed build. *(client request · MoM 9 Sep 2026, 4.17 POS Prototype Review - Reports, Settings, Peripherals & Role-Based Access · DI-801)*
- Terminal settings as business-optional toggles: printer, offline continuity, screen prompts, guest-facing display, key sounds, training mode. *(client request · MoM 9 Sep 2026, 4.17 POS Prototype Review - Reports, Settings, Peripherals & Role-Based Access · DI-800)*
- Hardware checks (printer, cash drawer, terminal connectivity) run automatically at shift start as a "boot-up checklist", in parallel with denomination entry, never discovered mid-transaction; a peripheral/hardware test screen validates devices before shift start. *(agreed · MoM 9 Sep 2026, 4.12 POS Prototype Review - Login, Shift-Open, Denomination & Hardware Validation · DI-778)*
- Opening float entered either as a total amount or by denomination, configurable per venue. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-307)*
- Denominations configurable per currency/region (e.g. UAE 500, 200, 100, 50, 20; Bahrain has no 1000); amounts use 2 decimals (UAE) or 3 (Bahrain/Kuwait) with no rounding of the third decimal (2.013 stays 2.013). *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-306)*
- Configurable cash-drawer limit: on a busy day the cashier unloads excess cash mid-shift; the unloaded amount is held separately (partial hold) and reconciled at final close. *(agreed · MoM 12 Aug 2026, 19. Cash/Shift and Till Management · DI-274)*

`POS-017` Cash In / Cash Out Operations

- Till/cash management shows total cash and card transactions and variance tracking, and supports cash-in/cash-out for mid-shift cash pickups. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-308)*
- Configurable cash-drawer limit: on a busy day the cashier unloads excess cash mid-shift; the unloaded amount is held separately (partial hold) and reconciled at final close. *(agreed · MoM 12 Aug 2026, 19. Cash/Shift and Till Management · DI-274)*

`POS-018` Safe Drop & Cash Transfer Management

- Configurable cash-drawer limit: on a busy day the cashier unloads excess cash mid-shift; the unloaded amount is held separately (partial hold) and reconciled at final close. *(agreed · MoM 12 Aug 2026, 19. Cash/Shift and Till Management · DI-274)*

`POS-019` Shift Templates & Policies

- Shift management: assignment and scheduling by cashier/department, templates and policies, opening/closing, exceptions/alerts. Allam: explore merging shift-closing and till-closing screens to reduce dashboard count. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-309)*

`POS-020` Shift Exceptions & Alerts

- A flagged variance routes to a supervisor for PIN-based approve/reject; if rejected the cashier rechecks and resubmits, and can only close the shift once approved. *(client request · MoM 9 Sep 2026, 4.18 POS Prototype Review - Shift Close & Cash Variance Handling · DI-804)*
- Shift management: assignment and scheduling by cashier/department, templates and policies, opening/closing, exceptions/alerts. Allam: explore merging shift-closing and till-closing screens to reduce dashboard count. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-309)*

`POS-021` Sell — Food & Drink

- Quick-service (QSR) orders capture no pickup details: guest orders, pays, gets a receipt/order number and is notified via a KDS-driven order-status board. Takeaway/delivery do need contact and timing details. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-790)*
- F&B selection: menu browsing (mains, sides, drinks, desserts), size/extras/meal-combo options, and order type (dine-in, takeaway, delivery). *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-789)*
- All discounts and promotions (percentage, fixed amount, promo codes, employee/friends-and-family codes) are applied on the sell/cart screen, never on the payment screen, which only completes payment. *(agreed · MoM 9 Sep 2026, 4.14 POS Prototype Review - Discounts, Membership Capture & Split Payment · DI-786)*
- "Link to sale": a search field directly on the cart screen finds and links an existing guest profile or creates a new one inline, without leaving the cart - replacing the separate link-customer screen. *(agreed · MoM 9 Sep 2026, 4.13 POS Prototype Review - Home Screen, Ticketing Cart & Link-to-Sale UX · DI-783)*
- Multiple concurrent carts via a "+" button so the cashier can manage several customers at once. *(agreed · MoM 9 Sep 2026, 4.13 POS Prototype Review - Home Screen, Ticketing Cart & Link-to-Sale UX · DI-782)*
- The same wristband or enrolled face works as stored-value payment for F&B and retail: balance checked and deducted automatically at the point of sale; top-up via the same credential. *(client request · MoM 2 Sep 2026, 4.12 Media as a Payment Method · DI-643)*
- Entitlements go beyond admission — e.g. a combo of park admission + an F&B item + a retail item, each redeemed by QR scan at its counter. Admission entitlements cap entries per ticket (e.g. max 2); product entitlements give a time-bound window (e.g. 60 minutes from first scan). *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-458)*
- Modifiers can be free or chargeable with minimum/maximum selection rules; combo meals support component selection with upgrade options at additional cost. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-328)*
- Menu Builder defines the front-end POS layout per outlet — categories, item tiles (image, name, price) and configurable button sizes for fast-selling items. Agreed the current (reference) layout is a reference only and the UI/UX can be improved. *(agreed · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-326)*
- For small groups (2–4) the cashier can assign specific meals to specific tickets at sale; for large groups the group redeems centrally at the counter instead. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-290)*
- Ticket + combo meal: one QR holds both admission and meal; scanned at entry and again at the F&B counter to redeem the meal; a second meal redemption is refused. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-287)*
- Each workstation is linked to a front-end "sales board" (e.g. of ten: five ticketing, three F&B, two retail); signing in on it opens the matching front end automatically. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-247)*
- Food-ordering / counter (POS) app mock-ups are to use those reference apps and the previously shared POS PDF as references. *(agreed · MoM 5 Aug 2026, 13. Mobile / POS App Design References · DI-147)*
- Support both service models: quick-service (order and pay at the counter before food is served) and fine dining (table opened, items added over the visit, bill printed and paid at the end). *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-105)*
- F&B flow: from the menu the cashier picks a category (e.g. drink or meal), then item options (e.g. sauce, size), adds to cart and pays; visuals follow the primary POS reference, not the demoed F&B screen. *(agreed · MoM 3 Aug 2026, 4. Food & Beverage Module Walkthrough · DI-102)*
- F&B items can be sold offline (stock depleted at day end by recipe); retail items need real-time inventory tracking, so offline retail sales risk overselling. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-075)*

`POS-022` Send to Kitchen

- Kitchen display lets cashier/kitchen mark orders ready, handed over or delivered, driving the guest-facing order-status board. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-794)*
- Course-wise ordering (mainly fine dining) groups an order by course (starters, main course, dessert) so the kitchen fires each course at the right time. *(client request · MoM 18 Aug 2026, 4.7 Kitchen Operations & Course-Wise Ordering · DI-333)*

`POS-023` Sell — Merchandise

- Retail follows the same add-to-cart, charge and payment pattern as ticketing and F&B. *(agreed · MoM 9 Sep 2026, 4.16 POS Prototype Review - Retail, Refund/Void & Offline Sync · DI-795)*
- All discounts and promotions (percentage, fixed amount, promo codes, employee/friends-and-family codes) are applied on the sell/cart screen, never on the payment screen, which only completes payment. *(agreed · MoM 9 Sep 2026, 4.14 POS Prototype Review - Discounts, Membership Capture & Split Payment · DI-786)*
- "Link to sale": a search field directly on the cart screen finds and links an existing guest profile or creates a new one inline, without leaving the cart - replacing the separate link-customer screen. *(agreed · MoM 9 Sep 2026, 4.13 POS Prototype Review - Home Screen, Ticketing Cart & Link-to-Sale UX · DI-783)*
- Multiple concurrent carts via a "+" button so the cashier can manage several customers at once. *(agreed · MoM 9 Sep 2026, 4.13 POS Prototype Review - Home Screen, Ticketing Cart & Link-to-Sale UX · DI-782)*
- The same wristband or enrolled face works as stored-value payment for F&B and retail: balance checked and deducted automatically at the point of sale; top-up via the same credential. *(client request · MoM 2 Sep 2026, 4.12 Media as a Payment Method · DI-643)*
- Entitlements go beyond admission — e.g. a combo of park admission + an F&B item + a retail item, each redeemed by QR scan at its counter. Admission entitlements cap entries per ticket (e.g. max 2); product entitlements give a time-bound window (e.g. 60 minutes from first scan). *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-458)*
- Retail items (e.g. a t-shirt plus a cap) can be combined into a combo package with bundle-level pricing, presented both on-site and online with product images and descriptions. *(client request · MoM 19 Aug 2026, 4.3 Pricing, Bundles & Promotions · DI-358)*
- Besides scan-and-sell, a retail item bought with a ticket (e.g. a souvenir bundle) can be redeemed on-site via a QR code scan. *(client request · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-351)*
- Retail store setup reuses the F&B department/venue/zone structure with department type "Retail" and the shop as a sub-department; retail needs no sub-classification (unlike fine dining vs. QSR) since operations are scan-and-sell. Inventory stays outlet-level. *(agreed · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-350)*
- Stock is centralised per venue across web, app, kiosk and POS and not shared across venues; sale is gated by the system-recorded stock (an outlet with no system stock cannot sell even if physically present); inter-venue stock transfer moves stock. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-294)*
- Each workstation is linked to a front-end "sales board" (e.g. of ten: five ticketing, three F&B, two retail); signing in on it opens the matching front end automatically. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-247)*
- F&B items can be sold offline (stock depleted at day end by recipe); retail items need real-time inventory tracking, so offline retail sales risk overselling. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-075)*

`POS-025` Till Home

- **Open question.** Open (Qossai): many venues deliberately never show the cashier their expected sales total during the shift or at close (fraud prevention; finance's independent count catches variances). Whether the POS shows it is deferred to Qossai/Allam. *(open · MoM 9 Sep 2026, 4.18 POS Prototype Review - Shift Close & Cash Variance Handling · DI-806)*
- Whether a cashier sees revenue/report figures is a configurable on/off permission per role: some clients let cashiers see limited metrics (e.g. tickets sold), others only what they billed; a standalone outlet manager (e.g. F&B) may see their outlet's reporting from the POS. *(agreed · MoM 9 Sep 2026, 4.17 POS Prototype Review - Reports, Settings, Peripherals & Role-Based Access · DI-802)*
- Offline transactions sync automatically when connectivity returns (no manual sync action); while offline the cashier's transaction view shows only transactions completed locally during that offline period. *(agreed · MoM 9 Sep 2026, 4.16 POS Prototype Review - Retail, Refund/Void & Offline Sync · DI-798)*
- Transaction history (Allam) opens as a large, full-screen view (hundreds of transactions a day) with filters by date/time, product and customer name/contact, for customer-service lookups (e.g. guest back with a non-working ticket). *(client request · MoM 9 Sep 2026, 4.13 POS Prototype Review - Home Screen, Ticketing Cart & Link-to-Sale UX · DI-780)*
- Home screen shows gate/terminal identity, logged-in cashier, shift start time, denomination summary, TICVAI branding, hardware status, notifications, profile and a global search bar, with quick actions (scan ticket via QR/RFID, recall held sale, open drawer, reprint, void sale) and a full module menu (ticketing, F&B, retail). *(agreed · MoM 9 Sep 2026, 4.13 POS Prototype Review - Home Screen, Ticketing Cart & Link-to-Sale UX · DI-779)*
- Each workstation is linked to a front-end "sales board" (e.g. of ten: five ticketing, three F&B, two retail); signing in on it opens the matching front end automatically. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-247)*
- POS home has configurable dashboard widgets, including transaction and refund statistics. *(client request · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-009)*

`POS-026` Receipt & Reprint

- Offline transactions sync automatically when connectivity returns (no manual sync action); while offline the cashier's transaction view shows only transactions completed locally during that offline period. *(agreed · MoM 9 Sep 2026, 4.16 POS Prototype Review - Retail, Refund/Void & Offline Sync · DI-798)*
- Transaction history (Allam) opens as a large, full-screen view (hundreds of transactions a day) with filters by date/time, product and customer name/contact, for customer-service lookups (e.g. guest back with a non-working ticket). *(client request · MoM 9 Sep 2026, 4.13 POS Prototype Review - Home Screen, Ticketing Cart & Link-to-Sale UX · DI-780)*
- For a fully dynamic-QR event, even POS-purchased tickets are delivered by email/SMS with instructions to download the app and link the ticket, not printed as a static QR on the spot. *(agreed · MoM 2 Sep 2026, 4.7 Dynamic QR Code - Business Flexibility & Exceptions · DI-634)*
- In-park returns are operational: the return policy (e.g. allowed within 1 or 7 business days) is printed on the receipt, and guests are directed to a service counter. *(client request · MoM 19 Aug 2026, 4.7 Returns, Refunds & Exchanges — In-Store and Online · DI-366)*
- Shift closure needs supervisor authorisation, prints a denomination-itemised closing receipt and emails the closing report to finance/leadership automatically. *(agreed · MoM 12 Aug 2026, 19. Cash/Shift and Till Management · DI-272)*
- Reservation lookup shows items, customer, payment method, taxes and an optional post-purchase survey, with reprint receipt and regenerate ticket PDF actions. *(agreed · MoM 7 Aug 2026, 20. Live Point-of-Sale Transaction Walkthrough · DI-179)*
- POS flow order: select performance/time slot (live remaining capacity) → add product → attach a reservation account (search existing or create; mandatory/optional fields from data-mask config) → add-ons → checkout → per-ticket owner details where required → payment → printed ticket and booking reference. Modern UI required. *(agreed · MoM 7 Aug 2026, 20. Live Point-of-Sale Transaction Walkthrough · DI-177)*
- POS provides cart and transaction history, order search and refund processing. *(client request · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-007)*

`POS-027` Guest Lookup

- When a ticket/membership is for someone else (e.g. a parent buying a ski lesson for a child), the end user's details (name, date of birth, etc.) are captured on the ticket itself, while "link to sale" records the purchaser - who may or may not be the same person. *(client request · MoM 9 Sep 2026, 4.14 POS Prototype Review - Discounts, Membership Capture & Split Payment · DI-787)*
- Mobile number (or email) is the primary search key for linking a guest - name alone is impractical (many customers named "Mohammed"); capture the mobile early and proactively suggest a match if one exists. *(agreed · MoM 9 Sep 2026, 4.13 POS Prototype Review - Home Screen, Ticketing Cart & Link-to-Sale UX · DI-784)*
- "Link to sale": a search field directly on the cart screen finds and links an existing guest profile or creates a new one inline, without leaving the cart - replacing the separate link-customer screen. *(agreed · MoM 9 Sep 2026, 4.13 POS Prototype Review - Home Screen, Ticketing Cart & Link-to-Sale UX · DI-783)*
- Affiliated-hotel guests get a zero-value ticket/wristband after room-number lookup and identity verification, or charge on-site purchases to their room via the same lookup (PMS such as Opera). *(client request · MoM 2 Sep 2026, 4.9 Hotel/PMS integration · DI-638)*
- Lost wristband/card: operations identify the guest (phone number or ID), locate the original transaction and transfer the balance to a replacement wristband/card. *(client request · MoM 27 Aug 2026, 4.10 Lost-media recovery · DI-538)*
- End-of-visit unload/refund: a guest can unload the remaining balance at a counter after a balance check. Configurable venue-level toggle, not always on. *(agreed · MoM 27 Aug 2026, 4.10 Transfers, Fraud/Risk Controls · DI-535)*
- Ticket look-up shows the ticket's full consumption history: transaction date/time, number of scans, expiry, and (if applicable) wallet balance and F&B/retail spend against that ticket. *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-462)*
- Decision: one unified customer profile across ticketing, F&B and retail gives a 360° view of guest activity and avoids duplicates; e.g. a guest who buys tickets online and later dines is matched by name/mobile to the same profile. *(agreed · MoM 18 Aug 2026, 4.9 Unified Customer Profile · DI-339)*
- Per-ticket "ticket owner" details are captured separately from the "reservation owner" (buyer) and can enforce rules such as a minimum age per ticket holder. *(agreed · MoM 7 Aug 2026, 20. Live Point-of-Sale Transaction Walkthrough · DI-178)*
- POS flow order: select performance/time slot (live remaining capacity) → add product → attach a reservation account (search existing or create; mandatory/optional fields from data-mask config) → add-ons → checkout → per-ticket owner details where required → payment → printed ticket and booking reference. Modern UI required. *(agreed · MoM 7 Aug 2026, 20. Live Point-of-Sale Transaction Walkthrough · DI-177)*
- Custom fields gate purchase where configured — e.g. a checkbox confirming a guest is not pregnant before a specific product can be bought, or a weight-range field for an activity. *(agreed · MoM 7 Aug 2026, 6. Data Mask: Flexible Custom Data Capture · DI-156)*
- Membership: search a customer by mobile number or name to link the sale; view wallet balance, loyalty points, linked family members and RFID/barcode reference; top up the member's wallet directly. *(agreed · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-097)*
- POS cashier can associate a customer with the transaction and apply discounts and promotional benefits; checkout supports cash and other methods. *(client request · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-004)*

`POS-028` Table Service

- Allam: a realistic, to-scale visual floor plan reflecting the actual hall layout and table shapes (square, rectangular) across multiple dining areas/halls, instead of a generic list. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-793)*
- Tables are colour-coded by status (vacant, occupied, reserved) and filterable by status. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-792)*
- Table service (dine-in) captures table selection (or reservation), party size, seating-area preference, special notes/occasion, and a deposit option for reservations. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-791)*
- Each table has an activity log (seated, drinks ordered, food ordered, sent to kitchen, course served, etc.) and actions Add Guest, Change Server and Transfer Table. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-338)*
- Decision: table status flow is Available → Ordered → Table Closed (after payment) → Reserved (booked in advance). No "Cleaning" status — cleaning is a manual staff task, deliberately excluded to avoid complexity. *(agreed · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining); 5. Key Decisions · DI-336)*
- A visual floor/table map (main hall, terrace, VIP lounge, etc.) shows table status, and tables can be tagged with a customer category (e.g. VIP) so staff prioritise service. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-335)*
- Course-wise ordering (mainly fine dining) groups an order by course (starters, main course, dessert) so the kitchen fires each course at the right time. *(client request · MoM 18 Aug 2026, 4.7 Kitchen Operations & Course-Wise Ordering · DI-333)*
- Food-ordering / counter (POS) app mock-ups are to use those reference apps and the previously shared POS PDF as references. *(agreed · MoM 5 Aug 2026, 13. Mobile / POS App Design References · DI-147)*
- Table/seat-level structure supports flexible bill-splitting: by amount, by number of covers, or by category (e.g. one guest pays food, another drinks). *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-106)*
- Support both service models: quick-service (order and pay at the counter before food is served) and fine dining (table opened, items added over the visit, bill printed and paid at the end). *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-105)*
- Allam: replace the dated table layout with a modern, graphical table map where two-seat and four-seat tables look visually distinct; the cashier selects a table then enters the number of covers. *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-104)*
- Table service: a "new order" flow shows the table layout; once a table is selected, the associated menu is assigned to that table for ordering. *(agreed · MoM 3 Aug 2026, 4. Food & Beverage Module Walkthrough · DI-103)*

`POS-029` Order Queue

- Kitchen display lets cashier/kitchen mark orders ready, handed over or delivered, driving the guest-facing order-status board. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-794)*
- Quick-service (QSR) orders capture no pickup details: guest orders, pays, gets a receipt/order number and is notified via a KDS-driven order-status board. Takeaway/delivery do need contact and timing details. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-790)*
- Food-ordering / counter (POS) app mock-ups are to use those reference apps and the previously shared POS PDF as references. *(agreed · MoM 5 Aug 2026, 13. Mobile / POS App Design References · DI-147)*

## P05 Guest Kiosk

**Platform-wide**

- Allam: water-park guests rarely carry phones, so a kiosk at the ride lets a guest scan their wristband to book a queue slot and get a return time, then scan the wristband again to enter. *(agreed · MoM 7 Sep 2026, 4.14 Virtual Queue - Multi-Venue Applicability · DI-677)*
- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*
- Top-up rules set minimum and maximum amounts per transaction; channel/funding-source mapping restricts which payment methods each channel offers (e.g. cash top-up on-site only, not online), so each channel's top-up screen offers only its allowed methods. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-517)*
- Confirmed: a guest always books a product or package — never a resource (a specific room, vehicle or instructor by itself) directly — on every sales channel, including the guest/mobile app; the product's configuration determines which resources are booked behind the scenes. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-502)*
- Kiosks are guest-facing: white-labelled to the client's branding like the guest website, while keeping a kiosk-specific layout. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-298)*
- Ticketing, F&B and retail share one cart and checkout, one unified receipt and one QR/wristband per customer — no separate receipts or wristbands per product line. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-293)*
- A single cart/order must take mixed purchases (e.g. family tickets plus gift vouchers) with one unified checkout and identity capture. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-141)*
- Allam: the cashier design must work consistently across all cashier device types: POS terminals, tablets, iPads and kiosks. *(agreed · MoM 3 Aug 2026, 3. UX Design Approach Discussion · DI-101)*
- Selling a capacity-based product (e.g. seat-assigned tickets) while offline is blocked with a clear notification, never allowed through or silently failing; non-capacity products stay sellable offline. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-074)*

**Sell**

- A guest is not repeatedly re-offered something already declined (e.g. a fast pass rejected three times), and an offer ignored online is not re-presented on another channel, e.g. at POS after the guest bought it there. *(agreed · MoM 21 Sep 2026, 4.6 Personalized Offer Delivery & Omni-Channel Orchestration · DI-962)*
- Navigation depends on ticket type: admission has no date/time and goes straight to quantity/cart; dated asks date only; timed asks date then time; seated asks date, then time, then seat. *(agreed · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-116)*

**Screen by screen**

`KSK-004` Choose tickets

- Quantity/purchase limits can be set per order, per guest, per account category and per sales channel (e.g. maximum 6 tickets per transaction). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-464)*
- Minimum/maximum sellable quantity per customer (e.g. a promotional bundle requiring at least two) must be enforced at selection. *(agreed · MoM 7 Aug 2026, 16. Entitlement Components: Re-entry, Expiration & Sale Restrictions · DI-172)*

`KSK-005` Choose a performance

- Start/stop-sell per channel: e.g. a distant desert safari allows no same-day online booking (next day minimum), while onsite stays open to sell-out or a cutoff (e.g. 15 minutes before a timed show). Guest date/time pickers must reflect the channel's window. *(client request · MoM 31 Aug 2026, 4.11 Sales schedule & validity · DI-583)*

`KSK-006` Review

- Custom fields gate purchase where configured — e.g. a checkbox confirming a guest is not pregnant before a specific product can be bought, or a weight-range field for an activity. *(agreed · MoM 7 Aug 2026, 6. Data Mask: Flexible Custom Data Capture · DI-156)*

`KSK-007` Payment

- Split tender: one purchase paid with wallet balance plus another method, e.g. AED 500 from the wallet and the remaining AED 200 of a AED 700 purchase on a credit card. *(agreed · MoM 27 Aug 2026, 4.7 Split-Tender, Redemption Rules & Configuration Simulation · DI-525)*
- Apple Pay / Google Pay tap-to-pay are the primary regional digital payment methods; UPI-style QR payments may come later, not in initial scope. *(agreed · MoM 31 Jul 2026, 12. Payments & Regional Preferences · DI-079)*

`KSK-011` Collect a booking

- Media swap: zero-value transaction converting a ticket's media on-site, e.g. scanning an online QR at a kiosk to issue a physical wristband instead. *(client request · MoM 2 Sep 2026, 4.9 Media swap · DI-637)*
- Sales team creates bookings for any customer type and sends a confirmation; on arrival the guest presents it to collect physical media or scans directly at access control. Dashboard: today's orders/ reservations, confirmed guests, booking status; order detail shows customer and items. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-611)*

`KSK-017` Shop

- Stock is centralised per venue across web, app, kiosk and POS and not shared across venues; sale is gated by the system-recorded stock (an outlet with no system stock cannot sell even if physically present); inter-venue stock transfer moves stock. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-294)*

## P06 Venue Staff App

**Platform-wide**

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

**Operations**

- Employee app navigation: Work Orders, Task & Assets, Inventory/Safety/Inspections, Attendance, Approvals/Requests, Incidents, Communications, Venue Map; plus employee ID/profile and preferences. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-228)*

**Stock on the Floor**

- Decision: do NOT implement every granular warehouse status (put-away, picking, packing, dispatching, etc.); keep day-to-day workflows simple and fast for end users. This principle guides UI/UX and workflow design across inventory and warehouse operations. *(agreed · MoM 18 Aug 2026, 4.12 Simplification Principle — Guiding Decision · DI-346)*

**Screen by screen**

`EMP-001` Sign in

- Access loads automatically at login on POS and web/admin. A user with one role logs straight in; a user with several roles (e.g. admin, cashier, supervisor, manager) is prompted to choose which role to use. *(agreed · MoM 12 Aug 2026, 4. Multiple Roles per User and Role Switching · DI-249)*
- Employee app login by username/password or SSO. *(client request · MoM 10 Aug 2026, 5.1 Login, Roles & Dashboard · DI-225)*
- A user can hold several roles and switch between them at login (e.g. cashier vs supervisor). *(agreed · MoM 7 Aug 2026, 4. Roles & User Management · DI-152)*

`EMP-002` Select venue & role

- Access loads automatically at login on POS and web/admin. A user with one role logs straight in; a user with several roles (e.g. admin, cashier, supervisor, manager) is prompted to choose which role to use. *(agreed · MoM 12 Aug 2026, 4. Multiple Roles per User and Role Switching · DI-249)*

`EMP-003` Home — on duty

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*
- Quick-create for maintenance, IT support, cleaning/safety/security, store, purchase and leave requests. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-230)*
- Role-based home shows task counts, work orders and inspections for the employee; the whole navigation set (approvals, inventory, etc.) is filtered by role/permissions. *(client request · MoM 10 Aug 2026, 5.1 Login, Roles & Dashboard · DI-227)*

`EMP-004` Task list

- Work orders assigned to a technician must be visible on a technician-facing mobile app so field staff see assigned tasks and act directly from their device; execution shows a repair checklist, spare parts/tools consumed, a timeline (assigned, started, part requests) and a functional-test checklist before completion. *(client request · MoM 17 Sep 2026, 4.4 Work Order Management & Execution · DI-911)*
- Maintenance work orders are assigned to the relevant department/person and are visible on the staff mobile app; repair workspace tracks cost; annual maintenance history shows lifecycle cost per item. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-769)*
- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*
- Tasks are logged with priority and scheduled date/time; work order lifecycle Created → Assigned → In progress → Review → Closed with a timer showing resolution duration. *(client request · MoM 10 Aug 2026, 5.3 Task, Work Order & Asset Management · DI-231)*
- Notifications categorised by type — action-required vs purely informational — and search across tasks and incidents. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-229)*
- In-system task assignment between staff (e.g. a cashier flagging something for a supervisor) without email or messaging apps. *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-159)*

`EMP-005` Task detail

- Work-order parts are reserved in the general inventory; the reserve action is hidden offline, and a refusal for short stock names the part. *(agreed · MoM 17 Sep 2026, M17-02 · DI-925)*
- Work orders assigned to a technician must be visible on a technician-facing mobile app so field staff see assigned tasks and act directly from their device; execution shows a repair checklist, spare parts/tools consumed, a timeline (assigned, started, part requests) and a functional-test checklist before completion. *(client request · MoM 17 Sep 2026, 4.4 Work Order Management & Execution · DI-911)*
- Maintenance work orders are assigned to the relevant department/person and are visible on the staff mobile app; repair workspace tracks cost; annual maintenance history shows lifecycle cost per item. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-769)*
- Tasks are logged with priority and scheduled date/time; work order lifecycle Created → Assigned → In progress → Review → Closed with a timer showing resolution duration. *(client request · MoM 10 Aug 2026, 5.3 Task, Work Order & Asset Management · DI-231)*

`EMP-006` Raise a task

- Photo capture is the primary way to log faulty assets without barcodes (pipes, valves, lighting); barcode scan is secondary. *(agreed · MoM 10 Aug 2026, 5.3 Task, Work Order & Asset Management · DI-232)*
- Tasks are logged with priority and scheduled date/time; work order lifecycle Created → Assigned → In progress → Review → Closed with a timer showing resolution duration. *(client request · MoM 10 Aug 2026, 5.3 Task, Work Order & Asset Management · DI-231)*
- Quick-create for maintenance, IT support, cleaning/safety/security, store, purchase and leave requests. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-230)*
- In-system task assignment between staff (e.g. a cashier flagging something for a supervisor) without email or messaging apps. *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-159)*

`EMP-009` End shift

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*

`EMP-010` Scan — ready

- A separate dedicated scanner app for devices used only for scanning (e.g. mounted at turnstiles/gates) shows only scanning functions; the same validation is also embedded in the employee app. *(agreed · MoM 10 Aug 2026, 5.7 Ticket Scanning / Access Control App · DI-239)*

`EMP-014` Ticket lookup

- Ticket lookup shows the complete scan history: purchaser, gate and timestamp for every attempt. Security can manually override to admit a guest despite a scan issue; every override is logged against the visitor's record. *(client request · MoM 2 Sep 2026, 4.16 Ticket Lookup & Manual Override · DI-649)*
- Ticket look-up shows the ticket's full consumption history: transaction date/time, number of scans, expiry, and (if applicable) wallet balance and F&B/retail spend against that ticket. *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-462)*

`EMP-015` Group scan

- Group tickets can carry one shared QR code or individual QR codes, with partial check-in tracking; family tickets bundle adult/child pricing. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-137)*

`EMP-017` Sync & reconciliation

- Scanning must be native/installable and work fully offline, storing scans locally and syncing when connectivity returns. *(agreed · MoM 10 Aug 2026, 5.7 Ticket Scanning / Access Control App · DI-240)*
- After reconnection, offline records sync in batches in the order events occurred, tagged with both the original recorded time and the sync time; syncing must not slow gate entry. *(agreed · MoM 31 Jul 2026, 7. Ticket Validation & Offline Architecture · DI-065)*

`EMP-018` Offline package

- Scanning must be native/installable and work fully offline, storing scans locally and syncing when connectivity returns. *(agreed · MoM 10 Aug 2026, 5.7 Ticket Scanning / Access Control App · DI-240)*

`EMP-019` AI assistant — home

- The AI assistant answers natural-language business queries (e.g. "what was yesterday's ticketing revenue?") only within the user's role (a CEO sees full revenue, a cashier does not), shows grounded citations naming the policy or document an answer came from, and keeps conversation context ("compare that to this week"). *(client request · MoM 21 Sep 2026, 4.8 Core AI Platform — AI Assistant (Query & Knowledge) · DI-964)*

`EMP-020` AI assistant — answer

- The AI assistant answers natural-language business queries (e.g. "what was yesterday's ticketing revenue?") only within the user's role (a CEO sees full revenue, a cashier does not), shows grounded citations naming the policy or document an answer came from, and keeps conversation context ("compare that to this week"). *(client request · MoM 21 Sep 2026, 4.8 Core AI Platform — AI Assistant (Query & Knowledge) · DI-964)*

`EMP-021` Roster

- Staff see shift timings and upcoming shifts, clock in/out, and submit leave requests in the app. *(client request · MoM 10 Aug 2026, 5.6 Roster, Leave & Break Management, Resources · DI-236)*

`EMP-022` My rota

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*
- Staff see shift timings and upcoming shifts, clock in/out, and submit leave requests in the app. *(client request · MoM 10 Aug 2026, 5.6 Roster, Leave & Break Management, Resources · DI-236)*

`EMP-023` Swap request

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*
- Staff can request a swap (e.g. break coverage) from another resource; attendance exceptions are marked manually (active, not active, absent, other). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering; 4.9 AI Optimization, Mobile App & Analytics · DI-491)*

`EMP-024` Clock in / out

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*
- Shift templates (morning/afternoon/evening) define working patterns; the system recognises which shift a staff member has logged into from the configured shift timings. Leave/absence types and quotas work as a lightweight HR module, optionally integrated with an external HR/time-and-attendance system. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-487)*
- Staff see shift timings and upcoming shifts, clock in/out, and submit leave requests in the app. *(client request · MoM 10 Aug 2026, 5.6 Roster, Leave & Break Management, Resources · DI-236)*

`EMP-025` Break management

- Staff can request a swap (e.g. break coverage) from another resource; attendance exceptions are marked manually (active, not active, absent, other). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering; 4.9 AI Optimization, Mobile App & Analytics · DI-491)*
- Break management: staff log break windows so a replacement can be scheduled (e.g. so a ticket counter is not left unstaffed). *(client request · MoM 10 Aug 2026, 5.6 Roster, Leave & Break Management, Resources · DI-237)*

`EMP-026` Incident report

- Photo capture is the primary way to log faulty assets without barcodes (pipes, valves, lighting); barcode scan is secondary. *(agreed · MoM 10 Aug 2026, 5.3 Task, Work Order & Asset Management · DI-232)*

`EMP-028` Lost & found

- Guest assistance: quick access to supervisors, announcements and venue information (e.g. opening hours), live ride/attraction status, and logging found items that surface for guest claim. *(client request · MoM 10 Aug 2026, 5.6 Roster, Leave & Break Management, Resources · DI-238)*

`EMP-029` Guest assistance

- Guest assistance: quick access to supervisors, announcements and venue information (e.g. opening hours), live ride/attraction status, and logging found items that surface for guest claim. *(client request · MoM 10 Aug 2026, 5.6 Roster, Leave & Break Management, Resources · DI-238)*

`EMP-031` Queue monitor

- Ops view shows current wait per ride with general and virtual-queue waits separately, and alerts for e.g. a growing express queue or unusually long overall queue. *(client request · MoM 7 Sep 2026, 4.17 Virtual Queue - Operations Dashboard & AI Guest Flow Optimization · DI-681)*

`EMP-032` Manual wait entry

- **Open question.** Open: how per-ride occupancy is counted (entry sensors, manual security counts, CCTV/computer vision); Allam to check with Warner Bros. World, which has a visible wait-time display. Manual count entry stays a possible source. *(open · MoM 7 Sep 2026, 4.16 Wait-Time Calculation & People-Counting Technology · DI-680)*

`EMP-034` Walk-up sale

- Selling a capacity-based product (e.g. seat-assigned tickets) while offline is blocked with a clear notification, never allowed through or silently failing; non-capacity products stay sellable offline. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-074)*

`EMP-035` Payment on device

- Apple Pay / Google Pay tap-to-pay are the primary regional digital payment methods; UPI-style QR payments may come later, not in initial scope. *(agreed · MoM 31 Jul 2026, 12. Payments & Regional Preferences · DI-079)*
- Only cash payments are available while offline; card payment requires connectivity. *(agreed · MoM 31 Jul 2026, 12. Payments & Regional Preferences · DI-078)*

`EMP-036` Issue media

- Media swap: zero-value transaction converting a ticket's media on-site, e.g. scanning an online QR at a kiosk to issue a physical wristband instead. *(client request · MoM 2 Sep 2026, 4.9 Media swap · DI-637)*

`EMP-037` Notifications

- Real-time health view of device connectivity. Device-pushed events (anti-passback attempts, power loss, network loss) are surfaced as alerts and reports, e.g. notifying the operations team when a turnstile goes offline. *(agreed · MoM 2 Sep 2026, 4.1 / 4.2 Health Monitoring & Alerts · DI-625)*
- Notifications categorised by type — action-required vs purely informational — and search across tasks and incidents. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-229)*

`EMP-039` Announcements

- Guest assistance: quick access to supervisors, announcements and venue information (e.g. opening hours), live ride/attraction status, and logging found items that surface for guest claim. *(client request · MoM 10 Aug 2026, 5.6 Roster, Leave & Break Management, Resources · DI-238)*

`EMP-052` Floor Plan & Table Map

- Allam: a realistic, to-scale visual floor plan reflecting the actual hall layout and table shapes (square, rectangular) across multiple dining areas/halls, instead of a generic list. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-793)*
- Tables are colour-coded by status (vacant, occupied, reserved) and filterable by status. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-792)*
- Qossai asked if guests pick a specific table; Allam: table choice can be an option, but the default is the guest gives party size and the system/host allocates a table. *(agreed · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Dining) · DI-689)*
- Decision: table status flow is Available → Ordered → Table Closed (after payment) → Reserved (booked in advance). No "Cleaning" status — cleaning is a manual staff task, deliberately excluded to avoid complexity. *(agreed · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining); 5. Key Decisions · DI-336)*
- A visual floor/table map (main hall, terrace, VIP lounge, etc.) shows table status, and tables can be tagged with a customer category (e.g. VIP) so staff prioritise service. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-335)*
- Allam: replace the dated table layout with a modern, graphical table map where two-seat and four-seat tables look visually distinct; the cashier selects a table then enters the number of covers. *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-104)*

`EMP-053` Table & Seating Configuration

- Allam: a realistic, to-scale visual floor plan reflecting the actual hall layout and table shapes (square, rectangular) across multiple dining areas/halls, instead of a generic list. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-793)*

`EMP-054` Reservation Calendar & Timeline

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*

`EMP-055` Create / Edit Reservation

- The client's FnB Board 4 draws a guest duplicate-match and merge process on reservation create/edit and the guest profile: proposed matches shown as candidates, and the merge confirmed by the user. *(agreed · design-brief-9-september 9 Sep 2026, 2 (f) duplicateMatch · DI-808)*
- Table reservation captures table selection (with system recommendations), customer details, guest count, location/outlet and an optional deposit adjusted against the final bill; walk-in and waitlist management are also supported. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-337)*

`EMP-056` Walk-In & Waitlist Management

- Table reservation captures table selection (with system recommendations), customer details, guest count, location/outlet and an optional deposit adjusted against the final bill; walk-in and waitlist management are also supported. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-337)*

`EMP-057` Guest Profile & Dining History

- The client's FnB Board 4 draws a guest duplicate-match and merge process on reservation create/edit and the guest profile: proposed matches shown as candidates, and the merge confirmed by the user. *(agreed · design-brief-9-september 9 Sep 2026, 2 (f) duplicateMatch · DI-808)*
- Decision: one unified customer profile across ticketing, F&B and retail gives a 360° view of guest activity and avoids duplicates; e.g. a guest who buys tickets online and later dines is matched by name/mobile to the same profile. *(agreed · MoM 18 Aug 2026, 4.9 Unified Customer Profile · DI-339)*

`EMP-058` Live Table & Service Management

- Each table has an activity log (seated, drinks ordered, food ordered, sent to kitchen, course served, etc.) and actions Add Guest, Change Server and Transfer Table. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-338)*
- Decision: table status flow is Available → Ordered → Table Closed (after payment) → Reserved (booked in advance). No "Cleaning" status — cleaning is a manual staff task, deliberately excluded to avoid complexity. *(agreed · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining); 5. Key Decisions · DI-336)*
- A visual floor/table map (main hall, terrace, VIP lounge, etc.) shows table status, and tables can be tagged with a customer category (e.g. VIP) so staff prioritise service. *(client request · MoM 18 Aug 2026, 4.8 Table Management (Fine Dining) · DI-335)*
- Support both service models: quick-service (order and pay at the counter before food is served) and fine dining (table opened, items added over the visit, bill printed and paid at the end). *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-105)*

`EMP-059` Table Order, Bill & Payment Management

- Table/seat-level structure supports flexible bill-splitting: by amount, by number of covers, or by category (e.g. one guest pays food, another drinks). *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-106)*
- Support both service models: quick-service (order and pay at the counter before food is served) and fine dining (table opened, items added over the visit, bill printed and paid at the end). *(agreed · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-105)*

`EMP-062` Store Stock & SKU Availability

- Store Stock & Availability: search by product to see stock-on-hand vs. available stock, factoring in pending online purchases awaiting pickup/shipment. *(client request · MoM 19 Aug 2026, 4.5 Inventory Management — Requisitions, Transfers & Stock Counts · DI-361)*
- Item lookup by name or barcode scan shows stock and availability across stores/warehouses; inventory count and goods receipt are done in the app. *(client request · MoM 10 Aug 2026, 5.4 Inventory & Procurement · DI-233)*

`EMP-063` Requisition & Smart Store Replenishment

- Outlets raise inter-store requisitions subject to an approval workflow before transfer; stock can be transferred between any two stores (outlet-to-outlet, warehouse-to-outlet, outlet-to-warehouse). *(client request · MoM 19 Aug 2026, 4.5 Inventory Management — Requisitions, Transfers & Stock Counts · DI-362)*
- Requisitions raised in the app flow to department-head approval then purchasing; stock falling below a par level (e.g. 100 units) auto-creates a draft requisition for review and confirmation. *(client request · MoM 10 Aug 2026, 5.4 Inventory & Procurement · DI-234)*

`EMP-064` Store-to-Store & Warehouse Transfers

- Outlets raise inter-store requisitions subject to an approval workflow before transfer; stock can be transferred between any two stores (outlet-to-outlet, warehouse-to-outlet, outlet-to-warehouse). *(client request · MoM 19 Aug 2026, 4.5 Inventory Management — Requisitions, Transfers & Stock Counts · DI-362)*

`EMP-065` Receiving

- Receiving, stock counts (monthly/weekly/as needed) and damage/loss adjustments are supported, with a fully configurable user-defined reason list extendable in the backend without development. *(client request · MoM 19 Aug 2026, 4.5 Inventory Management — Requisitions, Transfers & Stock Counts · DI-363)*
- Item lookup by name or barcode scan shows stock and availability across stores/warehouses; inventory count and goods receipt are done in the app. *(client request · MoM 10 Aug 2026, 5.4 Inventory & Procurement · DI-233)*

`EMP-066` Stock Count & Cycle Count Management

- **Open question.** Allam: support bulk stock-taking with handheld RFID scanners — scanning a batch of tagged items updates system quantities once verified and saved. Chinmay's focus is reconciling existing stock vs. newly scanned data. Device specs pending. *(open · MoM 19 Aug 2026, 4.6 RFID/Barcode-Based Bulk Stock Counting — Open Item · DI-365)*
- Receiving, stock counts (monthly/weekly/as needed) and damage/loss adjustments are supported, with a fully configurable user-defined reason list extendable in the backend without development. *(client request · MoM 19 Aug 2026, 4.5 Inventory Management — Requisitions, Transfers & Stock Counts · DI-363)*
- Item lookup by name or barcode scan shows stock and availability across stores/warehouses; inventory count and goods receipt are done in the app. *(client request · MoM 10 Aug 2026, 5.4 Inventory & Procurement · DI-233)*

`EMP-067` Damage, Loss, Shrinkage & Stock Adjustment

- Receiving, stock counts (monthly/weekly/as needed) and damage/loss adjustments are supported, with a fully configurable user-defined reason list extendable in the backend without development. *(client request · MoM 19 Aug 2026, 4.5 Inventory Management — Requisitions, Transfers & Stock Counts · DI-363)*

`EMP-068` Reservation, Allocation & Omnichannel Inventory

- Decision: stock can be reserved/held (e.g. for a VIP customer) and allocated per sales channel (e.g. 50 units online, 50 on-site), each channel selling independently against its allocation. *(agreed · MoM 19 Aug 2026, 4.5 Inventory Management; 5. Key Decisions · DI-364)*

`EMP-069` Barcode, RFID, Serialized Stock & Traceability

- Barcode, RFID, serialised stock and traceability: serialisation down to the individual item (e.g. a jewellery counter or high-value electronics). *(agreed · client-design-boards-audit 20 Aug 2026, Genuine functional gaps - Retail Board 4 Page 9 · DI-406)*
- **Open question.** Allam: support bulk stock-taking with handheld RFID scanners — scanning a batch of tagged items updates system quantities once verified and saved. Chinmay's focus is reconciling existing stock vs. newly scanned data. Device specs pending. *(open · MoM 19 Aug 2026, 4.6 RFID/Barcode-Based Bulk Stock Counting — Open Item · DI-365)*

`EMP-071` Rental Checkout Command Center

- Checkout screen shows bookings by status (in progress, checked out) and lets staff scan a QR code to pull up a reservation. *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-758)*

`EMP-072` Voucher Scan & Reservation Retrieval

- Checkout screen shows bookings by status (in progress, checked out) and lets staff scan a QR code to pull up a reservation. *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-758)*

`EMP-073` Checkout Readiness Validation

- Before handover: readiness validation (reservation, payment, inventory), a pre-rental condition checklist (e.g. bicycle brakes and tyres working) and a safety handover checklist (e.g. helmet with a bicycle). *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-759)*

`EMP-074` Equipment Assignment Workspace

- Serialized items: staff assign the specific unit (e.g. bicycle #121) at checkout by scanning its QR code or selecting it manually from available units. Multi-item checkout hands a whole group's items (e.g. 10 bicycles) out in a single action. *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-760)*

`EMP-075` Equipment Scan & Validation

- Serialized items: staff assign the specific unit (e.g. bicycle #121) at checkout by scanning its QR code or selecting it manually from available units. Multi-item checkout hands a whole group's items (e.g. 10 bicycles) out in a single action. *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-760)*

`EMP-076` Pre-Rental Condition Inspection

- Before handover: readiness validation (reservation, payment, inventory), a pre-rental condition checklist (e.g. bicycle brakes and tyres working) and a safety handover checklist (e.g. helmet with a bicycle). *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-759)*

`EMP-077` Safety & Handover Checklist

- Before handover: readiness validation (reservation, payment, inventory), a pre-rental condition checklist (e.g. bicycle brakes and tyres working) and a safety handover checklist (e.g. helmet with a bicycle). *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-759)*

`EMP-078` Deposit & Financial Handover Validation

- Rental items (e.g. strollers, wheelchairs, towels): inventory and quantity per day, check-out and check-in, with inventory updated automatically on return; a refundable deposit (with guest details) is captured at rental and refunded on return. *(client request · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management · DI-498)*

`EMP-079` Group & Multi-Item Checkout

- Serialized items: staff assign the specific unit (e.g. bicycle #121) at checkout by scanning its QR code or selecting it manually from available units. Multi-item checkout hands a whole group's items (e.g. 10 bicycles) out in a single action. *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-760)*

`EMP-081` Active Rental Operations Command Center

- Active operations view tracks all rented items and durations in real time; rental detail timeline shows booking time, handover time and expected return time per item, with extension requests and extension pricing. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-761)*

`EMP-082` Active Rental Detail & Live Timeline

- Active operations view tracks all rented items and durations in real time; rental detail timeline shows booking time, handover time and expected return time per item, with extension requests and extension pricing. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-761)*

`EMP-083` Rental Extension Request

- Active operations view tracks all rented items and durations in real time; rental detail timeline shows booking time, handover time and expected return time per item, with extension requests and extension pricing. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-761)*

`EMP-084` Extension Pricing & Confirmation

- Active operations view tracks all rented items and durations in real time; rental detail timeline shows booking time, handover time and expected return time per item, with extension requests and extension pricing. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-761)*

`EMP-085` Equipment Swap / Replacement

- Equipment swap assigns the replacement to the booking. Swap within a short threshold (e.g. 5 minutes) restarts the timer; a later swap (e.g. 15 minutes into 30) lets the operator grant that booking only a free time extension/buffer. *(agreed · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-762)*

`EMP-086` Rental Incident & Operational Exception

- Incidents (e.g. reported brake malfunction) are logged against the booking; automatic SMS/app return reminders to the customer. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-763)*

`EMP-087` Due Soon & Customer Notification Management

- Incidents (e.g. reported brake malfunction) are logged against the booking; automatic SMS/app return reminders to the customer. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-763)*

`EMP-088` Overdue Rental Management

- Overdue tracking flags bookings past expected return and applies configured overdue pricing; a group / multi-item active-rental view and an intelligence panel (utilisation, incident trends) complete the board. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-764)*

`EMP-089` Active Group Rental Management

- Overdue tracking flags bookings past expected return and applies configured overdue pricing; a group / multi-item active-rental view and an intelligence panel (utilisation, incident trends) complete the board. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-764)*

`EMP-090` Active Rental Intelligence & Operational Alerts

- Overdue tracking flags bookings past expected return and applies configured overdue pricing; a group / multi-item active-rental view and an intelligence panel (utilisation, incident trends) complete the board. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-764)*

`EMP-092` Return Scan & Rental Retrieval

- Return: staff scan or search a booking; late fee is calculated automatically from actual vs booked duration. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-765)*

`EMP-093` Return Summary & Actual Return Time

- Return: staff scan or search a booking; late fee is calculated automatically from actual vs booked duration. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-765)*
- Usage-based billing at return: excess charged on actual vs. paid duration (e.g. a wheelchair paid for one hour but used for three is charged two extra hours at return). *(client request · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management · DI-499)*

`EMP-094` Post-Rental Condition Inspection

- Post-rental condition inspection, with before/after photo capture that is optional, not mandatory. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-766)*

`EMP-095` Before vs After Condition Comparison

- Post-rental condition inspection, with before/after photo capture that is optional, not mandatory. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-766)*

`EMP-096` Damage Assessment & Charge Workflow

- Damage assessment; partial group returns (e.g. 8 of 10 bicycles back, 2 outstanding); late fees, damage fees and final settlement calculated together before deposit release (individual or group); ends with a rental completion report. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-767)*

`EMP-097` Partial Return & Missing Equipment

- Damage assessment; partial group returns (e.g. 8 of 10 bicycles back, 2 outstanding); late fees, damage fees and final settlement calculated together before deposit release (individual or group); ends with a rental completion report. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-767)*

`EMP-098` Late Fees, Damage Fees & Final Settlement

- Damage assessment; partial group returns (e.g. 8 of 10 bicycles back, 2 outstanding); late fees, damage fees and final settlement calculated together before deposit release (individual or group); ends with a rental completion report. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-767)*
- Usage-based billing at return: excess charged on actual vs. paid duration (e.g. a wheelchair paid for one hour but used for three is charged two extra hours at return). *(client request · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management · DI-499)*

`EMP-099` Deposit Release, Capture & Customer Confirmation

- Damage assessment; partial group returns (e.g. 8 of 10 bicycles back, 2 outstanding); late fees, damage fees and final settlement calculated together before deposit release (individual or group); ends with a rental completion report. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-767)*
- Rental items (e.g. strollers, wheelchairs, towels): inventory and quantity per day, check-out and check-in, with inventory updated automatically on return; a refundable deposit (with guest details) is captured at rental and refunded on return. *(client request · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management · DI-498)*

`EMP-100` Return Completion & Equipment Disposition

- Damage assessment; partial group returns (e.g. 8 of 10 bicycles back, 2 outstanding); late fees, damage fees and final settlement calculated together before deposit release (individual or group); ends with a rental completion report. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-767)*

## P07 Venue Scanner

**Platform-wide**

- Staff-facing POS and tablet UIs always carry TICVAI branding, not client branding. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-296)*
- A separate dedicated scanner app for devices used only for scanning (e.g. mounted at turnstiles/gates) shows only scanning functions; the same validation is also embedded in the employee app. *(agreed · MoM 10 Aug 2026, 5.7 Ticket Scanning / Access Control App · DI-239)*
- Two separate apps: an access-control app (handhelds or fixed terminals) scoped purely to entry validation/scanning, and an employee app (approvals, alerts/messages, matrix features) that may include a basic ticket-validity lookup but not full scanning. *(agreed · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-128)*
- Offline state must be clearly visible in the UI, e.g. a visible mode indicator or greyed-out unavailable functions; exact visual treatment to be settled in the UI/UX session. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-072)*
- Allam: the app detects loss of connectivity and switches to offline mode automatically, without cashier action, then restores online mode and syncs pending transactions automatically. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-071)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Validation works fully offline, with optional local BLE verification (Bluetooth must be on) to confirm the staff member is physically at the gate; BLE is configurable per venue. *(agreed · MoM 31 Jul 2026, 7. Ticket Validation & Offline Architecture · DI-063)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- POS: sell tickets, memberships, F&B, retail and services from one unified cashier experience. Access Control: real-time entry validation, occupancy monitoring, offline mode and gate management. *(agreed · Design Vision Book 29 Jul 2026, 07 Modules Overview (p7) - 04 Point of Sale; 03 Access Control · DI-035)*
- Preliminary perceived-performance targets: web pages load in under about 3 seconds, mobile app loads in under about 2 seconds, ticket validation responds in under 500 milliseconds. *(agreed · MoM 28 Jul 2026, 18. Performance and Scalability · DI-015)*
- During an outage the handheld validates tickets against a secure local database, stores scans locally and synchronises when connectivity returns; validation by QR format alone is not acceptable (fraud risk). *(agreed · MoM 28 Jul 2026, 15. Offline POS and Access-Control Operations · DI-013)*
- POS must keep selling general admission tickets during an internet outage, and access-control apps must keep scanning and validating tickets during a connectivity failure. *(agreed · MoM 28 Jul 2026, 15. Offline POS and Access-Control Operations · DI-012)*

**Screen by screen**

`SCN-003` Ready to scan

- Qossai: walk-in, virtual-queue and VIP guests must be distinguished at the ride; VQ guests are never merged into the VIP line (would erode paid value); VQ arrivals need their own handling, e.g. a separate line or a QR scan within the arrival window. *(agreed · MoM 7 Sep 2026, 4.15 Virtual Queue - Three-Tier Guest Model · DI-678)*
- Access decisions consider who, ticket type, where, when and context; e.g. an otherwise valid unused ticket is denied once the venue's maximum live occupancy is reached, until guests exit. Scanners need a venue-full denial state. *(agreed · MoM 2 Sep 2026, 4.16 Attribute-Based Access Control · DI-650)*
- Handheld scanners read QR, RFID or other supported media. Offline, devices validate locally from data embedded in the credential, queue the transactions and auto-sync when connectivity returns. *(agreed · MoM 2 Sep 2026, 4.13 / 4.14 Handheld Scanners & Offline Mode · DI-646)*
- A successful scan marks the ticket used even if the guest did not pass (stroller, turnstile re-locked). Genuine cases are resolved manually by security from the ticket's scan-history log, so scanner lookup must show it. *(agreed · MoM 2 Sep 2026, 4.3 Decision (scan without physical passage) · DI-627)*
- Qossai: where a waiver is required before entry, an incomplete waiver can block ticket download, activation, check-in or access; ticket and scan screens need a waiver-incomplete state. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-574)*
- If a guest exits without a matching checkout scan (e.g. a manually opened door), the system flags it and blocks the next re-entry scan until check-in/check-out is reconciled. *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-461)*
- Entitlements go beyond admission — e.g. a combo of park admission + an F&B item + a retail item, each redeemed by QR scan at its counter. Admission entitlements cap entries per ticket (e.g. max 2); product entitlements give a time-bound window (e.g. 60 minutes from first scan). *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-458)*
- **Open question.** Access-control scan result screens show customer photo, ticket information and validity status; details deferred to a future workshop. *(open · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-129)*

`SCN-007` Group admission

- Group ticket QR options: one QR valid for a defined headcount, individual QR per member, or a single rotating/multi-use QR scanned until the headcount is exhausted. *(client request · MoM 31 Aug 2026, 4.8 Group Operations, Payment Links & Check-In · DI-569)*
- Group tickets can carry one shared QR code or individual QR codes, with partial check-in tracking; family tickets bundle adult/child pricing. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-137)*

`SCN-008` Manual entry

- Ticket lookup shows the complete scan history: purchaser, gate and timestamp for every attempt. Security can manually override to admit a guest despite a scan issue; every override is logged against the visitor's record. *(client request · MoM 2 Sep 2026, 4.16 Ticket Lookup & Manual Override · DI-649)*

`SCN-009` Ticket lookup

- Ticket lookup shows the complete scan history: purchaser, gate and timestamp for every attempt. Security can manually override to admit a guest despite a scan issue; every override is logged against the visitor's record. *(client request · MoM 2 Sep 2026, 4.16 Ticket Lookup & Manual Override · DI-649)*
- A successful scan marks the ticket used even if the guest did not pass (stroller, turnstile re-locked). Genuine cases are resolved manually by security from the ticket's scan-history log, so scanner lookup must show it. *(agreed · MoM 2 Sep 2026, 4.3 Decision (scan without physical passage) · DI-627)*
- Ticket look-up shows the ticket's full consumption history: transaction date/time, number of scans, expiry, and (if applicable) wallet balance and F&B/retail spend against that ticket. *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-462)*
- **Open question.** Access-control scan result screens show customer photo, ticket information and validity status; details deferred to a future workshop. *(open · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-129)*

`SCN-013` Offline journal

- Handheld scanners read QR, RFID or other supported media. Offline, devices validate locally from data embedded in the credential, queue the transactions and auto-sync when connectivity returns. *(agreed · MoM 2 Sep 2026, 4.13 / 4.14 Handheld Scanners & Offline Mode · DI-646)*
- Scanning must be native/installable and work fully offline, storing scans locally and syncing when connectivity returns. *(agreed · MoM 10 Aug 2026, 5.7 Ticket Scanning / Access Control App · DI-240)*

`SCN-014` Sync & reconciliation

- Handheld scanners read QR, RFID or other supported media. Offline, devices validate locally from data embedded in the credential, queue the transactions and auto-sync when connectivity returns. *(agreed · MoM 2 Sep 2026, 4.13 / 4.14 Handheld Scanners & Offline Mode · DI-646)*
- Scanning must be native/installable and work fully offline, storing scans locally and syncing when connectivity returns. *(agreed · MoM 10 Aug 2026, 5.7 Ticket Scanning / Access Control App · DI-240)*
- After reconnection, offline records sync in batches in the order events occurred, tagged with both the original recorded time and the sync time; syncing must not slow gate entry. *(agreed · MoM 31 Jul 2026, 7. Ticket Validation & Offline Architecture · DI-065)*

`SCN-016` Gate mode

- Live operations dashboard: real-time attendance by venue and gate with each gate's online/offline status and entry count. Turnstile mode can be switched through the day (more entry gates in the morning, more exit in the evening). *(client request · MoM 2 Sep 2026, 4.15 Live Operations Dashboard · DI-648)*

## P08 Venue Management

**Platform-wide**

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

**Access & Venue**

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**Catalogue**

- Chinmay: reduce the number of configuration screens/pages and consolidate related settings/toggles to avoid a long, click-heavy admin flow; Allam agreed, citing the previous system's demo as a starting reference. *(agreed · MoM 25 Aug 2026, 4.11 UX Simplification & Distributed Inventory · DI-474)*

**Food & Beverage**

- Decision: F&B configuration (menus, recipes, costing, inventory) is managed at outlet level, and Retail follows the same segregation. Venue-owned homogeneous outlets (e.g. popcorn/ice-cream booths) may be set up centrally once and applied across outlets, but the model stays outlet-level. *(agreed · MoM 18 Aug 2026, 4.5 Outlet-Level vs. Venue-Level Configuration — Key Discussion · DI-330)*
- **Open question.** F&B dashboards are role-based: the F&B Director sees all outlets, an outlet manager sees only their own outlet. Detailed design of the role-based dashboards (Director vs. outlet-level roles) is still to be finalised. *(open · MoM 18 Aug 2026, 4.10 F&B Stock, Wastage & Requisitions; 6. Open Items · DI-318)*

**Orders & Money**

- AI-assisted reporting for accountants/finance managers is phase two; phase-one finance screens do not include it. *(agreed · MoM 12 Aug 2026, 6. Finance & Ledger Architecture Overview · DI-278)*
- Financial reports generated automatically: P&L (revenue per category less cost of sales), balance sheet, trial balance and ledger view, cash flow, revenue and deferred-revenue analytics, site-wise revenue; plus daily/weekly/monthly finance summaries. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-276)*
- Legal entities view lists all tenant sites with country, currency and active/inactive status. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-261)*
- Allam: Bulk QR option — for partners with no technical capability, the platform generates a bulk batch of tickets (e.g. 5,000) with a validity window, delivered as QR codes (e.g. CSV) for the partner to import and resell. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-135)*
- Full card numbers are never stored or shown; only a masked representation (e.g. last four digits) so the user can identify which card was used. *(agreed · MoM 31 Jul 2026, 10. Compliance & Data Protection · DI-069)*

**People & Access Rights**

- No role or permission is predefined: any privilege, including refund approval, can be assigned to any custom role. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-255)*
- Rights can be set at site, operating area (department, e.g. B2B, B2C, OTA, on-site POS, finance), workstation, role or user level; site-level settings (password policy, UI rights, configuration rights) cascade to everything beneath. *(agreed · MoM 7 Aug 2026, 2. System Organization: Tenant & Site Setup · DI-148)*

**Sell**

- Allam: back-end configuration is the most critical part; the screens must make visually clear how administrators configure products, pricing per channel, attributes/components, entitlements, validity and access permissions, comparable to the structured product/metric-sheet approach of an earlier reference system. *(agreed · MoM 24 Sep 2026, 4.3 Back-End Configuration Detail — Requested Format (Screens, Not Just Functional Lists) · DI-985)*
- Chinmay: reduce the number of configuration screens/pages and consolidate related settings/toggles to avoid a long, click-heavy admin flow; Allam agreed, citing the previous system's demo as a starting reference. *(agreed · MoM 25 Aug 2026, 4.11 UX Simplification & Distributed Inventory · DI-474)*
- Retail dashboard gives a consolidated real-time view across outlets — total retail sales, total and average transactions, store performance snapshot, system alerts and out-of-stock indicators — viewable by day, week or month. *(client request · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-349)*
- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*

**Setup & Go-Live**

- Go-live readiness validates end-to-end: products set up correctly, pricing displays correctly, and a full test transaction completes in the target environment. *(client request · MoM 10 Sep 2026, 4.14 Go-Live Readiness Validation · DI-835)*
- After contract, TICVAI provisions the tenant with a basic setup reflecting the tier and licensed modules (e.g. mobile app, B2C, B2B enabled as contracted) before handover; AI can assist initial product/event/ticket setup following the same process as manual setup. *(client request · MoM 10 Sep 2026, 4.12 Tenant Provisioning & Go-Live Setup · DI-833)*
- AI-created product/ticket configuration likewise asks follow-ups before finalising (e.g. is the ticket admission, time-slot or seat-assignment type; which categories and discounts apply). *(agreed · MoM 8 Sep 2026, 4.7 AI-Assisted Report & Configuration Generation · DI-713)*

**Stock & Supply**

- Decision: do NOT implement every granular warehouse status (put-away, picking, packing, dispatching, etc.); keep day-to-day workflows simple and fast for end users. This principle guides UI/UX and workflow design across inventory and warehouse operations. *(agreed · MoM 18 Aug 2026, 4.12 Simplification Principle — Guiding Decision · DI-346)*
- Decision: F&B configuration (menus, recipes, costing, inventory) is managed at outlet level, and Retail follows the same segregation. Venue-owned homogeneous outlets (e.g. popcorn/ice-cream booths) may be set up centrally once and applied across outlets, but the model stays outlet-level. *(agreed · MoM 18 Aug 2026, 4.5 Outlet-Level vs. Venue-Level Configuration — Key Discussion · DI-330)*

**Venue Operations**

- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*

**Screen by screen**

`ADM-038` Communication Service Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Communications dashboard shows activity across email, WhatsApp and SMS: delivered, pending, failed. Delivery queue tracks failed sends with automatic retry; routing/fallback rules send on an alternate channel if delivery fails. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-559)*

`ADM-040` Sender Identity, Domain & Brand Configuration

- Sender identity per brand (from and reply-to, e.g. no-reply@venue.com, customerservice@venue.com). Templates fully configurable per channel (email, SMS, WhatsApp): header, logo, footer and content, for consistent branded communications. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-560)*

`ADM-041` System Transactional Template Registry

- Sender identity per brand (from and reply-to, e.g. no-reply@venue.com, customerservice@venue.com). Templates fully configurable per channel (email, SMS, WhatsApp): header, logo, footer and content, for consistent branded communications. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-560)*

`ADM-042` Business Event & Notification Trigger Mapping

- Notification triggers must key off precise event states where needed: a post-visit survey only when the ticket was actually scanned/used, whereas a "how was your experience" follow-up can trigger off the sale. Trigger mapping must expose such event states. *(agreed · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-561)*

`ADM-043` Routing, Priority, Throttling & Fallback Rules

- Communications dashboard shows activity across email, WhatsApp and SMS: delivered, pending, failed. Delivery queue tracks failed sends with automatic retry; routing/fallback rules send on an alternate channel if delivery fails. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-559)*

`ADM-044` Consent, Preference & Communication Policy Enforcement

- Consent and communication preference tracking records marketing/newsletter opt-in status per customer. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-562)*

`ADM-045` Delivery Queue, Failure & Retry Management

- Communications dashboard shows activity across email, WhatsApp and SMS: delivered, pending, failed. Delivery queue tracks failed sends with automatic retry; routing/fallback rules send on an alternate channel if delivery fails. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-559)*

`ADM-048` Commercial Pricing Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Pricing module (~7 sub-screens): overview dashboard of all pricing setups and status; price lists per channel, segment or product category (several can coexist); price categories/rate types (adult, child, member); rate structure; product-rate association; bundle/add-on pricing; multi-market/currency pricing. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-591)*

`ADM-049` Price List Master Configuration

- Pricing module (~7 sub-screens): overview dashboard of all pricing setups and status; price lists per channel, segment or product category (several can coexist); price categories/rate types (adult, child, member); rate structure; product-rate association; bundle/add-on pricing; multi-market/currency pricing. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-591)*

`ADM-050` Price Category & Rate Type Library

- Pricing module (~7 sub-screens): overview dashboard of all pricing setups and status; price lists per channel, segment or product category (several can coexist); price categories/rate types (adult, child, member); rate structure; product-rate association; bundle/add-on pricing; multi-market/currency pricing. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-591)*

`ADM-052` Product & Service Price Assignment

- Pricing module (~7 sub-screens): overview dashboard of all pricing setups and status; price lists per channel, segment or product category (several can coexist); price categories/rate types (adult, child, member); rate structure; product-rate association; bundle/add-on pricing; multi-market/currency pricing. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-591)*
- UX reference: a competitor's pricing matrix that configures channel-and-variant pricing in one matrix view (e.g. adult/child x onsite/online/kiosk). Qossai: not to copy it, but match or improve on it. *(client request · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-582)*

`ADM-053` Package, Bundle & Add-On Pricing

- Pricing module (~7 sub-screens): overview dashboard of all pricing setups and status; price lists per channel, segment or product category (several can coexist); price categories/rate types (adult, child, member); rate structure; product-rate association; bundle/add-on pricing; multi-market/currency pricing. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-591)*

`ADM-054` Market, Venue & Currency Pricing Structure

- Pricing module (~7 sub-screens): overview dashboard of all pricing setups and status; price lists per channel, segment or product category (several can coexist); price categories/rate types (adult, child, member); rate structure; product-rate association; bundle/add-on pricing; multi-market/currency pricing. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-591)*

`ADM-055` Price Hierarchy & Inheritance Configuration

- When several rules apply to one sale (e.g. summer rate plus school-group discount) the configurable pricing hierarchy decides; there is no automatic lowest-price-wins default. *(agreed · MoM 1 Sep 2026, 4.4 Seasonal & Date-Based Pricing; Rule Priority · DI-595)*
- Price hierarchy screen sets which level (category, item, segment) takes precedence; price lists can be cloned (e.g. B2C copied and discounted for B2B); a final validation screen confirms setup is complete. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-592)*

`ADM-056` Price List Templates, Clone & Reuse

- Price hierarchy screen sets which level (category, item, segment) takes precedence; price lists can be cloned (e.g. B2C copied and discounted for B2B); a final validation screen confirms setup is complete. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-592)*

`ADM-057` Commercial Pricing Structure Validation

- Price hierarchy screen sets which level (category, item, segment) takes precedence; price lists can be cloned (e.g. B2C copied and discounted for B2B); a final validation screen confirms setup is complete. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-592)*

`ADM-058` Pricing Rule Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Pricing rules overview shows all rules, status and conflicts. Rule types: customer segment (regular, school, corporate, group), membership, residency/nationality (UAE resident vs non-resident), channel (POS, B2C, kiosk, B2B), venue/attraction/event. *(client request · MoM 1 Sep 2026, 4.2 Pricing Rules · DI-593)*

`ADM-059` Customer Segment & Profile Pricing Rules

- Pricing rules overview shows all rules, status and conflicts. Rule types: customer segment (regular, school, corporate, group), membership, residency/nationality (UAE resident vs non-resident), channel (POS, B2C, kiosk, B2B), venue/attraction/event. *(client request · MoM 1 Sep 2026, 4.2 Pricing Rules · DI-593)*

`ADM-060` Membership & Loyalty Pricing Rules

- Pricing rules overview shows all rules, status and conflicts. Rule types: customer segment (regular, school, corporate, group), membership, residency/nationality (UAE resident vs non-resident), channel (POS, B2C, kiosk, B2B), venue/attraction/event. *(client request · MoM 1 Sep 2026, 4.2 Pricing Rules · DI-593)*

`ADM-061` Residency, Nationality & Market Pricing Rules

- Pricing rules overview shows all rules, status and conflicts. Rule types: customer segment (regular, school, corporate, group), membership, residency/nationality (UAE resident vs non-resident), channel (POS, B2C, kiosk, B2B), venue/attraction/event. *(client request · MoM 1 Sep 2026, 4.2 Pricing Rules · DI-593)*

`ADM-062` Channel-Based Pricing Rules

- Pricing rules overview shows all rules, status and conflicts. Rule types: customer segment (regular, school, corporate, group), membership, residency/nationality (UAE resident vs non-resident), channel (POS, B2C, kiosk, B2B), venue/attraction/event. *(client request · MoM 1 Sep 2026, 4.2 Pricing Rules · DI-593)*
- UX reference: a competitor's pricing matrix that configures channel-and-variant pricing in one matrix view (e.g. adult/child x onsite/online/kiosk). Qossai: not to copy it, but match or improve on it. *(client request · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-582)*
- Sales channels (onsite, B2C, B2B, kiosk) configured per venue; a product is available on all channels or restricted to some. Channel-specific pricing required, e.g. online cheaper than onsite/counter. *(agreed · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-580)*

`ADM-063` Location, Venue & Event Pricing Rules

- Pricing rules overview shows all rules, status and conflicts. Rule types: customer segment (regular, school, corporate, group), membership, residency/nationality (UAE resident vs non-resident), channel (POS, B2C, kiosk, B2B), venue/attraction/event. *(client request · MoM 1 Sep 2026, 4.2 Pricing Rules · DI-593)*

`ADM-064` Quantity, Group & Volume Pricing Rules

- Tiered volume bands (up to 1,000 tickets, 1,000-5,000, above 5,000) applied automatically; seasonal pricing (low season to 30 September, high season from 1 October); date-based and time-slot/performance pricing. *(client request · MoM 1 Sep 2026, 4.3 / 4.4 Volume, Seasonal & Time-slot Pricing · DI-594)*

`ADM-065` Effective Date, Season & Day-Based Pricing Rules

- Tiered volume bands (up to 1,000 tickets, 1,000-5,000, above 5,000) applied automatically; seasonal pricing (low season to 30 September, high season from 1 October); date-based and time-slot/performance pricing. *(client request · MoM 1 Sep 2026, 4.3 / 4.4 Volume, Seasonal & Time-slot Pricing · DI-594)*

`ADM-066` Timeslot, Performance & Time-of-Day Pricing Rules

- Tiered volume bands (up to 1,000 tickets, 1,000-5,000, above 5,000) applied automatically; seasonal pricing (low season to 30 September, high season from 1 October); date-based and time-slot/performance pricing. *(client request · MoM 1 Sep 2026, 4.3 / 4.4 Volume, Seasonal & Time-slot Pricing · DI-594)*

`ADM-067` Pricing Rule Priority, Conflict Resolution & Testing

- When several rules apply to one sale (e.g. summer rate plus school-group discount) the configurable pricing hierarchy decides; there is no automatic lowest-price-wins default. *(agreed · MoM 1 Sep 2026, 4.4 Seasonal & Date-Based Pricing; Rule Priority · DI-595)*

`ADM-069` Tax Profile & Jurisdiction Configuration

- Taxes inclusive or exclusive at product or category level; tax profiles combine several taxes incl. tax-on-tax (e.g. Egypt); per-product/transaction tax exemption flag. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-596)*

`ADM-070` Tax Rule & Treatment Builder

- Taxes inclusive or exclusive at product or category level; tax profiles combine several taxes incl. tax-on-tax (e.g. Egypt); per-product/transaction tax exemption flag. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-596)*

`ADM-071` Fee & Surcharge Library

- Fees are separate from taxes: e.g. a call-center convenience fee, or a shipping fee varying by destination (Dubai, Abu Dhabi, Ras Al Khaimah, international) calculated from the checkout address; applied at transaction, item or ticket level. Checkout must show the fee once the address is entered. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-597)*

`ADM-072` Fee Applicability & Charging Rule Builder

- Fees are separate from taxes: e.g. a call-center convenience fee, or a shipping fee varying by destination (Dubai, Abu Dhabi, Ras Al Khaimah, international) calculated from the checkout address; applied at transaction, item or ticket level. Checkout must show the fee once the address is entered. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-597)*

`ADM-073` Fee Waiver, Tax Exemption & Exception Rules

- Taxes inclusive or exclusive at product or category level; tax profiles combine several taxes incl. tax-on-tax (e.g. Egypt); per-product/transaction tax exemption flag. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-596)*

`ADM-078` Pricing Governance Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-080` Bulk Pricing Update, Import & Mass Maintenance

- Price changes go through approval before publishing with version control (AED 100 > 110 > 120 tracked as versions 1.0, 1.1, 1.2); bulk updates (e.g. flat % across all retail or F&B items), bulk import, and rollback with full change history. *(client request · MoM 1 Sep 2026, 4.6 Price Governance · DI-599)*

`ADM-081` Pricing Version & Baseline Management

- Price changes go through approval before publishing with version control (AED 100 > 110 > 120 tracked as versions 1.0, 1.1, 1.2); bulk updates (e.g. flat % across all retail or F&B items), bulk import, and rollback with full change history. *(client request · MoM 1 Sep 2026, 4.6 Price Governance · DI-599)*

`ADM-083` Pricing Approval Workflow & Authority Matrix

- Price changes go through approval before publishing with version control (AED 100 > 110 > 120 tracked as versions 1.0, 1.1, 1.2); bulk updates (e.g. flat % across all retail or F&B items), bulk import, and rollback with full change history. *(client request · MoM 1 Sep 2026, 4.6 Price Governance · DI-599)*

`ADM-086` Pricing Rollback & Emergency Control Center

- Price changes go through approval before publishing with version control (AED 100 > 110 > 120 tracked as versions 1.0, 1.1, 1.2); bulk updates (e.g. flat % across all retail or F&B items), bulk import, and rollback with full change history. *(client request · MoM 1 Sep 2026, 4.6 Price Governance · DI-599)*

`ADM-087` Pricing History, Audit & Compliance Explorer

- Price changes go through approval before publishing with version control (AED 100 > 110 > 120 tracked as versions 1.0, 1.1, 1.2); bulk updates (e.g. flat % across all retail or F&B items), bulk import, and rollback with full change history. *(client request · MoM 1 Sep 2026, 4.6 Price Governance · DI-599)*

`ADM-088` Dynamic Pricing Strategy Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-089` Dynamic Pricing Strategy Builder

- Dynamic strategies: buy 2 get the 3rd free / BOGO, sibling tiers (first child full price, later children reduced), early-bird phases (e.g. 20% off a AED 200 base for the first 200 of 500, then 10% for the next 100, then full; discount and quota per phase), and price steps as capacity sells (e.g. at 50%). *(client request · MoM 1 Sep 2026, 4.7 Dynamic Pricing Strategies · DI-600)*

`ADM-092` Seasonal, Calendar, Day & Timeslot Dynamic Rules

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Dynamic pricing in two phases: first rule-based by time and capacity (e.g. +20% once capacity reaches 70%, early-booking discounts); factor-based (weather/AI-driven) later, scoped separately. *(agreed · MoM 19 Aug 2026, 4.10 Workshop Planning & Remaining Scope; 5. Key Decisions · DI-369)*

`ADM-094` Dynamic Price Bands, Ladders & Adjustment Matrix

- Dynamic strategies: buy 2 get the 3rd free / BOGO, sibling tiers (first child full price, later children reduced), early-bird phases (e.g. 20% off a AED 200 base for the first 200 of 500, then 10% for the next 100, then full; discount and quota per phase), and price steps as capacity sells (e.g. at 50%). *(client request · MoM 1 Sep 2026, 4.7 Dynamic Pricing Strategies · DI-600)*
- Dynamic pricing in two phases: first rule-based by time and capacity (e.g. +20% once capacity reaches 70%, early-booking discounts); factor-based (weather/AI-driven) later, scoped separately. *(agreed · MoM 19 Aug 2026, 4.10 Workshop Planning & Remaining Scope; 5. Key Decisions · DI-369)*

`ADM-098` AI Pricing Intelligence Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-103` Market, Tourism, Holiday & Contextual Signal Hub

- Forecast signal configuration defines which data sources and coverage periods the AI may use, e.g. historical sales over the last 36 months, real-time bookings and attendance history; seasonality, festivities and weather (e.g. forecast rain) are factored in. *(client request · MoM 18 Sep 2026, 4.9 AI Forecasting — Model Strategies & Signal Configuration · DI-942)*

`ADM-104` AI Demand Forecasting & Booking Curve Studio

- Demand forecasts show current sales pace, forecast and remaining opportunity broken down by sales channel; revenue forecasts show drivers and confidence levels. A forecast simulator models a hypothetical change (e.g. a 10% price decrease, reduced operating hours, staffing changes) before it is made. *(client request · MoM 18 Sep 2026, 4.10 AI Forecasting — Attendance, Demand, Revenue & Capacity Forecasting · DI-943)*

`ADM-106` AI Pricing Recommendation & Explainability Center

- AI forecasting recommends pricing/promotional action ahead of demand shifts (e.g. forecast rain > recommend a discount); a simulation tool previews the likely impact of a price change before it goes live. *(client request · MoM 1 Sep 2026, 4.8 AI Demand Forecasting & Pricing Simulation · DI-601)*

`ADM-107` AI Signal Registry, Data Quality & Model Governance

- Forecast signal configuration defines which data sources and coverage periods the AI may use, e.g. historical sales over the last 36 months, real-time bookings and attendance history; seasonality, festivities and weather (e.g. forecast rain) are factored in. *(client request · MoM 18 Sep 2026, 4.9 AI Forecasting — Model Strategies & Signal Configuration · DI-942)*

`ADM-108` Revenue Optimization Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-109` Pricing Simulation Studio

- AI forecasting recommends pricing/promotional action ahead of demand shifts (e.g. forecast rain > recommend a discount); a simulation tool previews the likely impact of a price change before it goes live. *(client request · MoM 1 Sep 2026, 4.8 AI Demand Forecasting & Pricing Simulation · DI-601)*

`ADM-110` Scenario Modeling & What-If Analysis

- Demand forecasts show current sales pace, forecast and remaining opportunity broken down by sales channel; revenue forecasts show drivers and confidence levels. A forecast simulator models a hypothetical change (e.g. a 10% price decrease, reduced operating hours, staffing changes) before it is made. *(client request · MoM 18 Sep 2026, 4.10 AI Forecasting — Attendance, Demand, Revenue & Capacity Forecasting · DI-943)*

`ADM-112` Revenue & Demand Impact Forecasting

- Demand forecasts show current sales pace, forecast and remaining opportunity broken down by sales channel; revenue forecasts show drivers and confidence levels. A forecast simulator models a hypothetical change (e.g. a 10% price decrease, reduced operating hours, staffing changes) before it is made. *(client request · MoM 18 Sep 2026, 4.10 AI Forecasting — Attendance, Demand, Revenue & Capacity Forecasting · DI-943)*

`ADM-118` Product Lifecycle Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Product dashboard by state (draft, pending approval, published) with a visual workflow draft > approval > approved > scheduled > active. Also bulk creation via template import/export, ownership by department/team, channel publication controls, start/stop-selling scheduler, duplication from a template library. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-577)*
- Product lifecycle dashboard shows counts of products in draft, in approval and published, filterable by venue/department; every product must be authorised before publishing online or on-site. *(client request · MoM 25 Aug 2026, 4.1 Product / Ticket Catalog Creation · DI-438)*

`ADM-119` Product Creation Workspace

- Decision: all policy types — reschedule, exchange, refund, cancellation, upgrade/downgrade, ownership transfer, membership-to-pass conversion — are managed centrally within the unified product configuration, not separate screens. Each product also maps pricing, GL account code, promotions and channel availability. *(agreed · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies; 5. Key Decisions · DI-466)*
- Decision: special product types — group (min/max size, single or multiple QR codes), family (min/max composition) and corporate/allocation tickets — are configured within the same unified product configuration screen, not separate screens. *(agreed · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships; 5. Key Decisions · DI-465)*
- Products are classified by configurable components (e.g. resident/non-resident → standard/VIP tier → adult/child/youth), not a fixed structure; components can be added and a simple venue may use only guest category. Tickets can be anonymous or require captured guest details. *(client request · MoM 25 Aug 2026, 4.4 Product Combination Matrix & Ownership · DI-450)*
- Content localisation: separate content (images, descriptions) per sales channel (POS vs. B2C/B2B) and per language (e.g. English/Arabic). *(client request · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference · DI-442)*
- Identity & classification: product name, product ID, main/sub-category, venue (multi-venue), ticket type. A category hierarchy manager groups and sorts packages and ticket types (e.g. admission > general admission > single-day, multi-day, annual pass, packages, vouchers). *(client request · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference · DI-441)*
- Product creation wizard offers four paths: create from scratch (step by step), create and save as a reusable template (e.g. an events template), clone an existing product (e.g. GA → child ticket), and import from file using a standard tenant template. *(client request · MoM 25 Aug 2026, 4.1 Product / Ticket Catalog Creation · DI-439)*
- Six core ticket types: Open-Dated (no fixed date; GA and B2B/travel-agent QR resale), Group & Family (configurable group size, single-scan or multi-scan QR), Membership/Subscription (full details per member; renew/upgrade/cancel), Event (date/time selection, resources, capacity), Gift Voucher, Money Card. *(agreed · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough; 5. Key Decisions · DI-433)*
- Ticket configuration flow runs basic information → ticket type configuration → validation → publish. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-432)*

`ADM-120` Lifecycle Status & Workflow Configuration

- Product dashboard by state (draft, pending approval, published) with a visual workflow draft > approval > approved > scheduled > active. Also bulk creation via template import/export, ownership by department/team, channel publication controls, start/stop-selling scheduler, duplication from a template library. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-577)*

`ADM-121` Bulk Product Creation & Catalogue Import

- Product dashboard by state (draft, pending approval, published) with a visual workflow draft > approval > approved > scheduled > active. Also bulk creation via template import/export, ownership by department/team, channel publication controls, start/stop-selling scheduler, duplication from a template library. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-577)*
- Product creation wizard offers four paths: create from scratch (step by step), create and save as a reusable template (e.g. an events template), clone an existing product (e.g. GA → child ticket), and import from file using a standard tenant template. *(client request · MoM 25 Aug 2026, 4.1 Product / Ticket Catalog Creation · DI-439)*

`ADM-123` Product Context, Ownership & Assignment

- Product dashboard by state (draft, pending approval, published) with a visual workflow draft > approval > approved > scheduled > active. Also bulk creation via template import/export, ownership by department/team, channel publication controls, start/stop-selling scheduler, duplication from a template library. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-577)*

`ADM-124` Channel Publication & Availability

- Sales channels (onsite, B2C, B2B, kiosk) configured per venue; a product is available on all channels or restricted to some. Channel-specific pricing required, e.g. online cheaper than onsite/counter. *(agreed · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-580)*
- Product dashboard by state (draft, pending approval, published) with a visual workflow draft > approval > approved > scheduled > active. Also bulk creation via template import/export, ownership by department/team, channel publication controls, start/stop-selling scheduler, duplication from a template library. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-577)*

`ADM-125` Publication & Activation Scheduler

- Chinmay: before a change (e.g. to ticket validity) is confirmed, show which existing bookings, reservations or promotions are affected and alert admin and customer-facing teams. Higher-risk changes can be applied from a chosen future effective date. Allam agreed. *(agreed · MoM 31 Aug 2026, 4.10 Change impact analysis · DI-579)*
- Product dashboard by state (draft, pending approval, published) with a visual workflow draft > approval > approved > scheduled > active. Also bulk creation via template import/export, ownership by department/team, channel publication controls, start/stop-selling scheduler, duplication from a template library. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-577)*

`ADM-126` Product Duplication & Template Library

- Product dashboard by state (draft, pending approval, published) with a visual workflow draft > approval > approved > scheduled > active. Also bulk creation via template import/export, ownership by department/team, channel publication controls, start/stop-selling scheduler, duplication from a template library. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-577)*
- Product creation wizard offers four paths: create from scratch (step by step), create and save as a reusable template (e.g. an events template), clone an existing product (e.g. GA → child ticket), and import from file using a standard tenant template. *(client request · MoM 25 Aug 2026, 4.1 Product / Ticket Catalog Creation · DI-439)*

`ADM-127` AI Catalogue Builder & Configuration Review

- AI-assisted draft: an AI wizard asks what ticket type to create and the relevant fields, then auto-configures a draft for review before approval/publish. Agreed extension (Chinmay): it also parses unstructured input (incl. OCR on images) and prompts the user for missing details. *(agreed · MoM 25 Aug 2026, 4.1 Product / Ticket Catalog Creation · DI-440)*

`ADM-128` Product Governance Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Changes to a published product (pricing, validity) go through approval and review, with rollback and version history. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-578)*
- Governance view shows product counts by status (draft, pending approval, approved, published); each price, terms or policy revision is a new version; publish rights are restricted to the authorised user/department; version history supports rollback to a prior published version. *(client request · MoM 25 Aug 2026, 4.10 AI Governance & Publish Workflow · DI-473)*

`ADM-129` Approval Workflow Designer

- Changes to a published product (pricing, validity) go through approval and review, with rollback and version history. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-578)*
- Governance view shows product counts by status (draft, pending approval, approved, published); each price, terms or policy revision is a new version; publish rights are restricted to the authorised user/department; version history supports rollback to a prior published version. *(client request · MoM 25 Aug 2026, 4.10 AI Governance & Publish Workflow · DI-473)*

`ADM-130` Approval Review & Decision Workspace

- The preview/publish step shows how the ticket appears on the B2C front end and — at Chinmay's request — also the PDF ticket layout and Apple Wallet / Google Wallet formats, so the reviewer sees every output format. *(agreed · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference; 5. Key Decisions · DI-444)*

`ADM-131` Product Version Management

- Changes to a published product (pricing, validity) go through approval and review, with rollback and version history. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-578)*
- Governance view shows product counts by status (draft, pending approval, approved, published); each price, terms or policy revision is a new version; publish rights are restricted to the authorised user/department; version history supports rollback to a prior published version. *(client request · MoM 25 Aug 2026, 4.10 AI Governance & Publish Workflow · DI-473)*

`ADM-132` Rollback & Recovery Management

- Changes to a published product (pricing, validity) go through approval and review, with rollback and version history. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-578)*
- Governance view shows product counts by status (draft, pending approval, approved, published); each price, terms or policy revision is a new version; publish rights are restricted to the authorised user/department; version history supports rollback to a prior published version. *(client request · MoM 25 Aug 2026, 4.10 AI Governance & Publish Workflow · DI-473)*

`ADM-133` Change Impact Analysis

- Chinmay: before a change (e.g. to ticket validity) is confirmed, show which existing bookings, reservations or promotions are affected and alert admin and customer-facing teams. Higher-risk changes can be applied from a chosen future effective date. Allam agreed. *(agreed · MoM 31 Aug 2026, 4.10 Change impact analysis · DI-579)*

`ADM-134` Change Propagation & Dependency Control

- Chinmay: before a change (e.g. to ticket validity) is confirmed, show which existing bookings, reservations or promotions are affected and alert admin and customer-facing teams. Higher-risk changes can be applied from a chosen future effective date. Allam agreed. *(agreed · MoM 31 Aug 2026, 4.10 Change impact analysis · DI-579)*

`ADM-136` Product Audit Trail & Change History

- Changes to a published product (pricing, validity) go through approval and review, with rollback and version history. *(client request · MoM 31 Aug 2026, 4.10 Product Lifecycle, Catalog & Change Governance · DI-578)*

`ADM-138` Promotion Command Center Dashboard

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-142` Campaign Calendar & Timeline

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*

`ADM-148` Promotion Rule Builder

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-158` Coupon & Promo Code Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-168` Advanced Offer Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-171` Cheapest / Lowest-Value Item Promotion

- Price Book supports date-based pricing (regular this month, promotional next month). Promotion Builder supports rules such as "buy X get Y", "buy 2 get 1 free" and "buy 3, lowest-priced item discounted" (fully or partially). *(client request · MoM 19 Aug 2026, 4.2 Product Catalog; 4.3 Pricing, Bundles & Promotions · DI-357)*

`ADM-172` Fixed-Price & “N for X” Offer Builder

- Dynamic strategies: buy 2 get the 3rd free / BOGO, sibling tiers (first child full price, later children reduced), early-bird phases (e.g. 20% off a AED 200 base for the first 200 of 500, then 10% for the next 100, then full; discount and quota per phase), and price steps as capacity sells (e.g. at 50%). *(client request · MoM 1 Sep 2026, 4.7 Dynamic Pricing Strategies · DI-600)*

`ADM-178` Bundle & Combo Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-180` Bundle Component Builder

- Multi-park / multi-attraction / multi-venue bundles are visually mapped, showing which venues, meal vouchers, VIP parking or upgrade options a bundle includes. *(client request · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies · DI-469)*

`ADM-188` Dynamic Bundle Operations Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-191` Capacity Pool & Reservation Manager

- Inventory pools split capacity by ticket type (e.g. 50% GA, 30% child, 20% senior) and/or sales channel (e.g. 50% online, 50% on-site), configurable at venue/event level, under a hierarchy global → attraction → product → variant → time slot. On cancel/refund/reschedule the business chooses whether capacity is released or held. *(agreed · MoM 25 Aug 2026, 4.6 Performances & Capacity Management; 4.11 UX Simplification & Distributed Inventory · DI-457)*

`ADM-198` Targeting & Eligibility Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-199` Eligibility Rule Builder

- Eligibility rules are configurable: residency/nationality/geography (e.g. UAE-resident-only with Emirates ID capture), minimum age (date-of-birth check), guest-profile category (e.g. VIP-only) and minimum loyalty points/spend for a membership tier. *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-463)*

`ADM-208` Stacking & Conflict Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-218` Campaign Governance & Budget Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-228` Promotion Performance Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-238` Rules & Workflow Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-248` Workflow Operations Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-249` Unified Approval Inbox & Decision Workspace

- Approval command centre/inbox shows all pending, validated and renewal requests and lets requests be assigned or reassigned to the relevant department or person. Approvals apply to any request type (new product, price change, website change). *(client request · MoM 8 Sep 2026, 4.12 Approval Workflow Recap - Inbox, SLA & Escalation · DI-723)*

`ADM-257` AI Workflow Intelligence & Autonomous Governance Center

- AI actions in progress are shown step by step in an AI action command center; if a process only partly completes (e.g. missing information) it rolls back rather than leaving a product half-configured, and a full change history records everything AI modified. *(client request · MoM 21 Sep 2026, 4.9 Core AI Platform — AI Tools, Agents & Action Orchestration · DI-965)*

`ADM-258` Sales Channel Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-259` Channel Creation & Profile Configuration

- Sales channels (onsite, B2C, B2B, kiosk) configured per venue; a product is available on all channels or restricted to some. Channel-specific pricing required, e.g. online cheaper than onsite/counter. *(agreed · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-580)*

`ADM-261` Channel Pricing & Commercial Profile Assignment

- UX reference: a competitor's pricing matrix that configures channel-and-variant pricing in one matrix view (e.g. adult/child x onsite/online/kiosk). Qossai: not to copy it, but match or improve on it. *(client request · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-582)*
- Sales channels (onsite, B2C, B2B, kiosk) configured per venue; a product is available on all channels or restricted to some. Channel-specific pricing required, e.g. online cheaper than onsite/counter. *(agreed · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-580)*

`ADM-262` Inventory, Capacity & Channel Allocation

- Inventory centralised or split per channel by percentage/quantity (e.g. 50% online / 50% onsite). Qossai: automatic migration rules, e.g. when B2C sells out pull a configured 20% from B2B, in the same configuration area. *(agreed · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-581)*
- Inventory pools split capacity by ticket type (e.g. 50% GA, 30% child, 20% senior) and/or sales channel (e.g. 50% online, 50% on-site), configurable at venue/event level, under a hierarchy global → attraction → product → variant → time slot. On cancel/refund/reschedule the business chooses whether capacity is released or held. *(agreed · MoM 25 Aug 2026, 4.6 Performances & Capacity Management; 4.11 UX Simplification & Distributed Inventory · DI-457)*

`ADM-263` Channel Sales Schedule & Availability Windows

- Start/stop-sell per channel: e.g. a distant desert safari allows no same-day online booking (next day minimum), while onsite stays open to sell-out or a cutoff (e.g. 15 minutes before a timed show). Guest date/time pickers must reflect the channel's window. *(client request · MoM 31 Aug 2026, 4.11 Sales schedule & validity · DI-583)*

`ADM-268` Channel Operations Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-272` Channel Allocation & Rebalancing Operations

- Inventory centralised or split per channel by percentage/quantity (e.g. 50% online / 50% onsite). Qossai: automatic migration rules, e.g. when B2C sells out pull a configured 20% from B2B, in the same configuration area. *(agreed · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-581)*

`ADM-278` Resale Marketplace Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-279` Resale Eligibility Rule Configuration

- Board 1 resale rules: eligibility, allowed price range, venue/tenant fees and commission, optional approval step. Board 2 resale purchase: payment, ownership transfer and settlement to the seller. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 1 / Board 2 · DI-619)*
- **Open question.** Resale lets a guest resell a ticket through a secured channel with configurable commission and eligibility (e.g. minimum time before validity date, no expired tickets). Open: TICVAI-owned secure portal vs inside each client's own B2C site/app. *(open · MoM 31 Aug 2026, 4.12 Resale Marketplace · DI-584)*

`ADM-282` Resale Pricing & Price Guardrails

- Board 1 resale rules: eligibility, allowed price range, venue/tenant fees and commission, optional approval step. Board 2 resale purchase: payment, ownership transfer and settlement to the seller. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 1 / Board 2 · DI-619)*

`ADM-283` Resale Fees, Commission & Seller Proceeds

- Board 1 resale rules: eligibility, allowed price range, venue/tenant fees and commission, optional approval step. Board 2 resale purchase: payment, ownership transfer and settlement to the seller. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 1 / Board 2 · DI-619)*
- **Open question.** Resale lets a guest resell a ticket through a secured channel with configurable commission and eligibility (e.g. minimum time before validity date, no expired tickets). Open: TICVAI-owned secure portal vs inside each client's own B2C site/app. *(open · MoM 31 Aug 2026, 4.12 Resale Marketplace · DI-584)*

`ADM-284` Listing Approval & Moderation

- Board 1 resale rules: eligibility, allowed price range, venue/tenant fees and commission, optional approval step. Board 2 resale purchase: payment, ownership transfer and settlement to the seller. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 1 / Board 2 · DI-619)*

`ADM-288` Resale Operations Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Resale listing dashboard with active / sold / expired / pending listings. Qossai: resale is expected almost exclusively for event tickets (concerts, sports), not open-dated admission tickets. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Detailed Follow-Up · DI-622)*

`ADM-289` Buyer Purchase & Resale Order Management

- Board 1 resale rules: eligibility, allowed price range, venue/tenant fees and commission, optional approval step. Board 2 resale purchase: payment, ownership transfer and settlement to the seller. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 1 / Board 2 · DI-619)*

`ADM-290` Ticket Ownership Transfer Management

- Resale keeps the original virtual ticket ID; only owner name and media (QR) change. An ownership change log shows the history against one ID (e.g. VT0010: Qossai > Allam > Chinmay). *(agreed · MoM 1 Sep 2026, 4.14 Decision (ticket ID on resale) · DI-620)*
- Board 1 resale rules: eligibility, allowed price range, venue/tenant fees and commission, optional approval step. Board 2 resale purchase: payment, ownership transfer and settlement to the seller. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 1 / Board 2 · DI-619)*

`ADM-294` Seller Settlement & Payout Management

- Board 1 resale rules: eligibility, allowed price range, venue/tenant fees and commission, optional approval step. Board 2 resale purchase: payment, ownership transfer and settlement to the seller. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 1 / Board 2 · DI-619)*

`ADM-296` Resale Audit & Ownership History

- Resale keeps the original virtual ticket ID; only owner name and media (QR) change. An ownership change log shows the history against one ID (e.g. VT0010: Qossai > Allam > Chinmay). *(agreed · MoM 1 Sep 2026, 4.14 Decision (ticket ID on resale) · DI-620)*

`ADM-298` My Tickets & Resale Marketplace Entry

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Three resale access models: (1) the client's own B2C site, where a guest requests resale within an admin-set price range (e.g. 10-20% below original); (2) a TICVAI-hosted white-label resale portal (e.g. museum.tickvai.com) for clients without B2C; (3) API for clients' own resale markets. *(agreed · MoM 1 Sep 2026, 4.14 Resale Marketplace - Detailed Follow-Up · DI-618)*

`ADM-299` Resale Eligibility & Ticket Selection

- White-label resale page: guest lists a ticket and sets a price within the allowed range; buyer searches, browses and receives the new ticket after purchase; the resale summary shows the market fee TICVAI retains. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 3 · DI-621)*

`ADM-300` Create Listing & Resale Price Selection

- White-label resale page: guest lists a ticket and sets a price within the allowed range; buyer searches, browses and receives the new ticket after purchase; the resale summary shows the market fee TICVAI retains. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 3 · DI-621)*
- Three resale access models: (1) the client's own B2C site, where a guest requests resale within an admin-set price range (e.g. 10-20% below original); (2) a TICVAI-hosted white-label resale portal (e.g. museum.tickvai.com) for clients without B2C; (3) API for clients' own resale markets. *(agreed · MoM 1 Sep 2026, 4.14 Resale Marketplace - Detailed Follow-Up · DI-618)*

`ADM-301` Fees, Seller Proceeds & Listing Confirmation

- White-label resale page: guest lists a ticket and sets a price within the allowed range; buyer searches, browses and receives the new ticket after purchase; the resale summary shows the market fee TICVAI retains. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 3 · DI-621)*

`ADM-302` My Resale Listings & Seller Dashboard

- Resale listing dashboard with active / sold / expired / pending listings. Qossai: resale is expected almost exclusively for event tickets (concerts, sports), not open-dated admission tickets. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Detailed Follow-Up · DI-622)*

`ADM-303` Official Resale Marketplace & Buyer Discovery

- White-label resale page: guest lists a ticket and sets a price within the allowed range; buyer searches, browses and receives the new ticket after purchase; the resale summary shows the market fee TICVAI retains. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 3 · DI-621)*
- Three resale access models: (1) the client's own B2C site, where a guest requests resale within an admin-set price range (e.g. 10-20% below original); (2) a TICVAI-hosted white-label resale portal (e.g. museum.tickvai.com) for clients without B2C; (3) API for clients' own resale markets. *(agreed · MoM 1 Sep 2026, 4.14 Resale Marketplace - Detailed Follow-Up · DI-618)*

`ADM-304` Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience

- White-label resale page: guest lists a ticket and sets a price within the allowed range; buyer searches, browses and receives the new ticket after purchase; the resale summary shows the market fee TICVAI retains. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 3 · DI-621)*

`ADM-305` Buyer Checkout, Inventory Hold & Secure Payment

- White-label resale page: guest lists a ticket and sets a price within the allowed range; buyer searches, browses and receives the new ticket after purchase; the resale summary shows the market fee TICVAI retains. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 3 · DI-621)*

`ADM-306` Resale Confirmation, Ownership Transfer & Ticket Delivery

- White-label resale page: guest lists a ticket and sets a price within the allowed range; buyer searches, browses and receives the new ticket after purchase; the resale summary shows the market fee TICVAI retains. *(client request · MoM 1 Sep 2026, 4.14 Resale Marketplace - Board 3 · DI-621)*

`ADM-307` White-Label Marketplace Deployment & Experience Architecture

- Three resale access models: (1) the client's own B2C site, where a guest requests resale within an admin-set price range (e.g. 10-20% below original); (2) a TICVAI-hosted white-label resale portal (e.g. museum.tickvai.com) for clients without B2C; (3) API for clients' own resale markets. *(agreed · MoM 1 Sep 2026, 4.14 Resale Marketplace - Detailed Follow-Up · DI-618)*

`ADM-308` Upgrade & Conversion Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Upgrade dashboard shows upgrade/exchange volume and upgrade revenue for a period. Paths define which product upgrades to which (adult ticket to membership; lower to higher membership tier), with downgrade paths where allowed. *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-602)*

`ADM-309` Upgrade & Conversion Path Builder

- Upgrade dashboard shows upgrade/exchange volume and upgrade revenue for a period. Paths define which product upgrades to which (adult ticket to membership; lower to higher membership tier), with downgrade paths where allowed. *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-602)*

`ADM-310` Upgrade Eligibility & Qualification Rules

- Upgrade eligibility checks validity/usage. Cases: seated ticket to a better section same day, paying the difference at the counter; general admission to season pass with the amount paid credited. Windows: before use, after use within a window, or until a cutoff (event ticket until the guest exits). *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-603)*

`ADM-311` Upgrade Timing, Usage & Ticket Status Rules

- Upgrade eligibility checks validity/usage. Cases: seated ticket to a better section same day, paying the difference at the counter; general admission to season pass with the amount paid credited. Windows: before use, after use within a window, or until a cutoff (event ticket until the guest exits). *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-603)*

`ADM-312` Upgrade Financial Treatment & Price Difference Rules

- Usage-based upgrades are pro-rata: e.g. 2 months used of a 1-year silver membership is credited and only the balance to the higher tier is charged. Attribute upgrades: a child ticket (sold by height) found to be adult on arrival is upgraded with the difference charged. *(agreed · MoM 1 Sep 2026, 4.9 Upgrade financial treatment · DI-604)*
- Upgrade eligibility checks validity/usage. Cases: seated ticket to a better section same day, paying the difference at the counter; general admission to season pass with the amount paid credited. Windows: before use, after use within a window, or until a cutoff (event ticket until the guest exits). *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-603)*

`ADM-313` Pro-Rata, Residual Value & Entitlement Credit Configuration

- Usage-based upgrades are pro-rata: e.g. 2 months used of a 1-year silver membership is credited and only the balance to the higher tier is charged. Attribute upgrades: a child ticket (sold by height) found to be adult on arrival is upgraded with the difference charged. *(agreed · MoM 1 Sep 2026, 4.9 Upgrade financial treatment · DI-604)*

`ADM-314` Person-Type, Product & Entitlement Conversion Rules

- Usage-based upgrades are pro-rata: e.g. 2 months used of a 1-year silver membership is credited and only the balance to the higher tier is charged. Attribute upgrades: a child ticket (sold by height) found to be adult on arrival is upgraded with the difference charged. *(agreed · MoM 1 Sep 2026, 4.9 Upgrade financial treatment · DI-604)*

`ADM-315` Bulk, Group & Assisted Upgrade Operations

- Group ticket upgrades are business-configurable (off by default); where allowed a group raises an upgrade request (e.g. via chat/support) rather than self-serving like an individual. *(agreed · MoM 1 Sep 2026, 4.9 Clarified (group upgrades) · DI-607)*
- Staff can upgrade multiple tickets in one action. "Quick upgrade" is a direct single-path upgrade (gold > platinum); "flexible upgrade" lets the guest choose among several eligible targets. *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-605)*

`ADM-316` Upgrade Execution, Credential Regeneration & Channel Controls

- Staff can upgrade multiple tickets in one action. "Quick upgrade" is a direct single-path upgrade (gold > platinum); "flexible upgrade" lets the guest choose among several eligible targets. *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-605)*

`ADM-320` Create Approval Workflow

- Workflow builder defines who approves a request type and how many levels (e.g. a refund needs both a department head and the finance director). *(client request · MoM 8 Sep 2026, 4.13 Approval Workflow Builder & Authority/Amount-Based Rules · DI-725)*

`ADM-322` Approval Stage Configuration

- Workflow builder defines who approves a request type and how many levels (e.g. a refund needs both a department head and the finance director). *(client request · MoM 8 Sep 2026, 4.13 Approval Workflow Builder & Authority/Amount-Based Rules · DI-725)*

`ADM-324` Approval Sequence & Parallel Routing

- Workflow builder defines who approves a request type and how many levels (e.g. a refund needs both a department head and the finance director). *(client request · MoM 8 Sep 2026, 4.13 Approval Workflow Builder & Authority/Amount-Based Rules · DI-725)*

`ADM-330` Approval Authority Matrix

- Authority rules by amount and category - e.g. refunds under AED 5,000 route to one approver, larger amounts to a higher approver - varying per tenant/venue via a tenant-and-venue approval matrix. *(client request · MoM 8 Sep 2026, 4.13 Approval Workflow Builder & Authority/Amount-Based Rules · DI-726)*

`ADM-333` Venue & Tenant Approval Matrix

- Authority rules by amount and category - e.g. refunds under AED 5,000 route to one approver, larger amounts to a higher approver - varying per tenant/venue via a tenant-and-venue approval matrix. *(client request · MoM 8 Sep 2026, 4.13 Approval Workflow Builder & Authority/Amount-Based Rules · DI-726)*

`ADM-334` Value & Threshold Routing

- Authority rules by amount and category - e.g. refunds under AED 5,000 route to one approver, larger amounts to a higher approver - varying per tenant/venue via a tenant-and-venue approval matrix. *(client request · MoM 8 Sep 2026, 4.13 Approval Workflow Builder & Authority/Amount-Based Rules · DI-726)*

`ADM-336` Approver Group & Decision Policy

- Approval groups per request type (finance group for refunds, operations group for cancellations) with N-of-M rules (Qossai): e.g. "any 2 of 5 team members" while a specific role (e.g. the CFO) must always be one of the approvers; depth can vary by amount or ticket quantity. *(agreed · MoM 8 Sep 2026, 4.14 Approval Groups & Decision Policy · DI-727)*

`ADM-339` Governance & Compliance Command Center

- Governance board manages segregation of duties, MFA policy, digital signature where applicable, data retention and audit trail, and shows identified compliance risks. *(client request · MoM 8 Sep 2026, 4.17 Governance, Security, Compliance & Audit · DI-732)*

`ADM-340` Segregation of Duties Policy Manager

- Governance board manages segregation of duties, MFA policy, digital signature where applicable, data retention and audit trail, and shows identified compliance risks. *(client request · MoM 8 Sep 2026, 4.17 Governance, Security, Compliance & Audit · DI-732)*

`ADM-342` Authentication & MFA Policy Manager

- Governance board manages segregation of duties, MFA policy, digital signature where applicable, data retention and audit trail, and shows identified compliance risks. *(client request · MoM 8 Sep 2026, 4.17 Governance, Security, Compliance & Audit · DI-732)*
- MFA / additional confirmation for sensitive approval actions is a business-configurable option (on or off), not mandatory, but the screens must support it when enabled. *(agreed · MoM 8 Sep 2026, 4.15 Execution & Decision Management · DI-729)*

`ADM-343` Sensitive Action Confirmation

- MFA / additional confirmation for sensitive approval actions is a business-configurable option (on or off), not mandatory, but the screens must support it when enabled. *(agreed · MoM 8 Sep 2026, 4.15 Execution & Decision Management · DI-729)*

`ADM-344` Digital Signature Management

- Governance board manages segregation of duties, MFA policy, digital signature where applicable, data retention and audit trail, and shows identified compliance risks. *(client request · MoM 8 Sep 2026, 4.17 Governance, Security, Compliance & Audit · DI-732)*

`ADM-346` Approval Record Retention Policy

- Governance board manages segregation of duties, MFA policy, digital signature where applicable, data retention and audit trail, and shows identified compliance risks. *(client request · MoM 8 Sep 2026, 4.17 Governance, Security, Compliance & Audit · DI-732)*

`ADM-347` Regulatory Audit & Evidence Center

- Governance board manages segregation of duties, MFA policy, digital signature where applicable, data retention and audit trail, and shows identified compliance risks. *(client request · MoM 8 Sep 2026, 4.17 Governance, Security, Compliance & Audit · DI-732)*

`ADM-353` Webhook Configuration & Subscription Manager

- Approval integration screens cover API/webhook/external workflow connections with data mapping and retry handling (e.g. resending a request the external system did not receive). *(client request · MoM 8 Sep 2026, 4.18 API/Integration for the Approval Workflow · DI-733)*

`ADM-354` External Workflow System Integration

- Approval integration screens cover API/webhook/external workflow connections with data mapping and retry handling (e.g. resending a request the external system did not receive). *(client request · MoM 8 Sep 2026, 4.18 API/Integration for the Approval Workflow · DI-733)*

`ADM-355` Data & Workflow Mapping Studio

- Approval integration screens cover API/webhook/external workflow connections with data mapping and retry handling (e.g. resending a request the external system did not receive). *(client request · MoM 8 Sep 2026, 4.18 API/Integration for the Approval Workflow · DI-733)*

`ADM-357` Integration Monitoring, Error & Retry Center

- Approval integration screens cover API/webhook/external workflow connections with data mapping and retry handling (e.g. resending a request the external system did not receive). *(client request · MoM 8 Sep 2026, 4.18 API/Integration for the Approval Workflow · DI-733)*

`ADM-359` Approval Executive KPI Dashboard

- Approval analytics shows how long each request took and overall turnaround across all logged requests. *(client request · MoM 8 Sep 2026, 4.19 Approval Analytics & the Role of AI · DI-734)*

`ADM-361` Approval Processing Time Analytics

- Approval analytics shows how long each request took and overall turnaround across all logged requests. *(client request · MoM 8 Sep 2026, 4.19 Approval Analytics & the Role of AI · DI-734)*

`ADM-362` Bottleneck Analysis & Heatmap

- Approval is human-governed (Qossai): AI is limited to analytics (turnaround, bottlenecks, individual approver performance) and must not recommend or influence whether a request is approved or rejected. *(agreed · MoM 8 Sep 2026, 4.19 Approval Analytics & the Role of AI · DI-735)*

`ADM-364` Approver & Team Performance Analytics

- Approval is human-governed (Qossai): AI is limited to analytics (turnaround, bottlenecks, individual approver performance) and must not recommend or influence whether a request is approved or rejected. *(agreed · MoM 8 Sep 2026, 4.19 Approval Analytics & the Role of AI · DI-735)*

`ADM-366` AI Approval Intelligence Center

- Approval is human-governed (Qossai): AI is limited to analytics (turnaround, bottlenecks, individual approver performance) and must not recommend or influence whether a request is approved or rejected. *(agreed · MoM 8 Sep 2026, 4.19 Approval Analytics & the Role of AI · DI-735)*

`ADM-625` Merchant Account & Settlement Calendar Manager

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*

`ADM-655` Pre-Purchase, Cart & Checkout Upsell Manager

- Add-ons attached to a main product can be mandatory or optional; cross-sell offers related add-on products, upsell proposes a higher tier (e.g. adult admission → membership). *(client request · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies · DI-470)*

`ADM-661` Product Affinity Matrix & Relationship Map

- Multi-park / multi-attraction / multi-venue bundles are visually mapped, showing which venues, meal vouchers, VIP parking or upgrade options a bundle includes. *(client request · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies · DI-469)*

`BO-001` Queue Directory

- VQ configuration: rides enabled/disabled per day, queue/express split, target wait time and return-window duration, and handling of early or late arrivals at the ride's entry scanner. *(client request · MoM 7 Sep 2026, 4.13 Virtual Queue - Mobile Journey & Configuration · DI-676)*

`BO-002` Queue Configuration

- Qossai: walk-in, virtual-queue and VIP guests must be distinguished at the ride; VQ guests are never merged into the VIP line (would erode paid value); VQ arrivals need their own handling, e.g. a separate line or a QR scan within the arrival window. *(agreed · MoM 7 Sep 2026, 4.15 Virtual Queue - Three-Tier Guest Model · DI-678)*
- Allam: water-park guests rarely carry phones, so a kiosk at the ride lets a guest scan their wristband to book a queue slot and get a return time, then scan the wristband again to enter. *(agreed · MoM 7 Sep 2026, 4.14 Virtual Queue - Multi-Venue Applicability · DI-677)*
- VQ configuration: rides enabled/disabled per day, queue/express split, target wait time and return-window duration, and handling of early or late arrivals at the ride's entry scanner. *(client request · MoM 7 Sep 2026, 4.13 Virtual Queue - Mobile Journey & Configuration · DI-676)*
- Per-ride hourly capacity (e.g. 600/hour) split across express/fast-lane, virtual queue and walk-in (illustrative 75% general split walk-in/VQ, 25%/150 express); allocation adjusts dynamically if one lane is disproportionately busy. *(client request · MoM 7 Sep 2026, 4.12 Virtual Queue - Concept & Lane/Allocation Model · DI-674)*

`BO-003` Queue Integration Setup

- Ride wait times come from the venue's sensor/camera counts via a live API (or a people count converted at a per-person rate) and are shown in the guest app; an AI "which ride to visit next" recommendation may follow. *(agreed · MoM 14 Aug 2026, 9. Queue Management · DI-299)*

`BO-004` Manual Wait Time Entry

- **Open question.** Open: how per-ride occupancy is counted (entry sensors, manual security counts, CCTV/computer vision); Allam to check with Warner Bros. World, which has a visible wait-time display. Manual count entry stays a possible source. *(open · MoM 7 Sep 2026, 4.16 Wait-Time Calculation & People-Counting Technology · DI-680)*
- The client asked for a manual wait-time entry screen: set a wait time by hand whether or not a sensor feed exists; a venue with no sensors runs entirely from it and a failed sensor falls back to it. *(client request · MoM 14 Aug 2026, (cited in BO-004 notes) · DI-315)*

`BO-005` Queue Monitor

- A visual venue map highlights long-queue rides vs low-queue alternatives so operations can redirect guests, e.g. a notification suggesting a nearby ride with a shorter wait. *(client request · MoM 7 Sep 2026, 4.17 AI guest flow optimization · DI-682)*
- Ops view shows current wait per ride with general and virtual-queue waits separately, and alerts for e.g. a growing express queue or unusually long overall queue. *(client request · MoM 7 Sep 2026, 4.17 Virtual Queue - Operations Dashboard & AI Guest Flow Optimization · DI-681)*
- **Open question.** Open: how per-ride occupancy is counted (entry sensors, manual security counts, CCTV/computer vision); Allam to check with Warner Bros. World, which has a visible wait-time display. Manual count entry stays a possible source. *(open · MoM 7 Sep 2026, 4.16 Wait-Time Calculation & People-Counting Technology · DI-680)*

`BO-006` Parking Configuration

- Parking is barrier integration, not space counting: one configuration screen chooses a model - no integration (TICVAI QR checked by security), ANPR (guest enters a plate at checkout, pushed to the barrier whitelist) or QR handoff to the barrier. Pay-per-hour parking is out of scope. *(agreed · MoM 14 Aug 2026, 10 · DI-316)*
- Parking supports three models: (1) no integration — TICVAI QR verified manually by security; (2) plate number at checkout pushed to the parking system's ANPR whitelist; (3) TICVAI QR passed to the barrier. Hourly pay-on-exit parking stays on the parking system's own POS. *(agreed · MoM 14 Aug 2026, 10. Parking Integrations · DI-300)*

`BO-007` Product Directory

- Identity & classification: product name, product ID, main/sub-category, venue (multi-venue), ticket type. A category hierarchy manager groups and sorts packages and ticket types (e.g. admission > general admission > single-day, multi-day, annual pass, packages, vouchers). *(client request · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference · DI-441)*
- Product lifecycle dashboard shows counts of products in draft, in approval and published, filterable by venue/department; every product must be authorised before publishing online or on-site. *(client request · MoM 25 Aug 2026, 4.1 Product / Ticket Catalog Creation · DI-438)*
- Ticket configuration flow runs basic information → ticket type configuration → validation → publish. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-432)*

`BO-008` Product Detail & Variants

- Decision: all policy types — reschedule, exchange, refund, cancellation, upgrade/downgrade, ownership transfer, membership-to-pass conversion — are managed centrally within the unified product configuration, not separate screens. Each product also maps pricing, GL account code, promotions and channel availability. *(agreed · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies; 5. Key Decisions · DI-466)*
- Decision: special product types — group (min/max size, single or multiple QR codes), family (min/max composition) and corporate/allocation tickets — are configured within the same unified product configuration screen, not separate screens. *(agreed · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships; 5. Key Decisions · DI-465)*
- Quantity/purchase limits can be set per order, per guest, per account category and per sales channel (e.g. maximum 6 tickets per transaction). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-464)*
- Eligibility rules are configurable: residency/nationality/geography (e.g. UAE-resident-only with Emirates ID capture), minimum age (date-of-birth check), guest-profile category (e.g. VIP-only) and minimum loyalty points/spend for a membership tier. *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-463)*
- Weekday/calendar rules give different validity and pricing to weekday-only vs. all-days products (e.g. Global Village). Blockout dates exclude some ticket types (e.g. memberships) on public holidays/special days, requiring a separate ticket for those dates. *(client request · MoM 25 Aug 2026, 4.5 Validity Management & Expiry Rules · DI-452)*
- Validity types: fixed date range, rolling (e.g. 90 days from issue) and first-use activation (starts at first scan). Confirmed: first-use tickets need a fallback expiry (e.g. issue date + 30 days) if never scanned. *(agreed · MoM 25 Aug 2026, 4.5 Validity Management & Expiry Rules · DI-451)*
- Products are classified by configurable components (e.g. resident/non-resident → standard/VIP tier → adult/child/youth), not a fixed structure; components can be added and a simple venue may use only guest category. Tickets can be anonymous or require captured guest details. *(client request · MoM 25 Aug 2026, 4.4 Product Combination Matrix & Ownership · DI-450)*
- Time-slot (performance) tickets configure early/late entry and an entry window (e.g. from 30 minutes before start until a cut-off). Multi-day tickets are consecutive-day or flexible within a range (e.g. any 3 days within a month). *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-447)*
- Decision (raised by Chinmay): date-change/reschedule is a product-level on/off setting with its own policy rules (e.g. allowed up to 24 hours before the visit, denied within 24 hours), not a separate screen. Typically off for special-day tickets (e.g. New Year, 1 January only), on for standard GA. *(agreed · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive; 5. Key Decisions · DI-446)*
- Open-dated ticket: name, description, price and validity period (e.g. 1 day, 1 month, 6 months), with a configurable reservation rule controlling whether customer details (name, email, phone) are captured at point of sale. *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-445)*
- The preview/publish step shows how the ticket appears on the B2C front end and — at Chinmay's request — also the PDF ticket layout and Apple Wallet / Google Wallet formats, so the reviewer sees every output format. *(agreed · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference; 5. Key Decisions · DI-444)*
- Ticket attributes such as minimum age, ID-proof requirements (e.g. Emirates ID for UAE-resident tickets, with format validation or photo upload; passport; handicap/PoD documentation) or an embedded ID-reader for on-site verification are configurable per ticket and region, not fixed. *(agreed · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference; 5. Key Decisions · DI-443)*
- Content localisation: separate content (images, descriptions) per sales channel (POS vs. B2C/B2B) and per language (e.g. English/Arabic). *(client request · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference · DI-442)*
- Identity & classification: product name, product ID, main/sub-category, venue (multi-venue), ticket type. A category hierarchy manager groups and sorts packages and ticket types (e.g. admission > general admission > single-day, multi-day, annual pass, packages, vouchers). *(client request · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference · DI-441)*
- Supporting configuration: ticket variants (adult/child/senior/VIP, configurable), waitlist, on-sale/off-sale timing and cut-offs, entitlement/access rules (single/multi-venue, entries, zones, early entry), fulfilment channels (email, WhatsApp, SMS), after-sales windows (upgrade, reschedule, cancel), dynamic/fixed pricing and promotions. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-437)*
- Guest information capture (name, mobile number, nationality, visit survey, etc.) is configurable per ticket type; even an open-dated admission ticket can optionally collect it. *(agreed · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough; 5. Key Decisions · DI-434)*
- Six core ticket types: Open-Dated (no fixed date; GA and B2B/travel-agent QR resale), Group & Family (configurable group size, single-scan or multi-scan QR), Membership/Subscription (full details per member; renew/upgrade/cancel), Event (date/time selection, resources, capacity), Gift Voucher, Money Card. *(agreed · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough; 5. Key Decisions · DI-433)*
- Ticket configuration flow runs basic information → ticket type configuration → validation → publish. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-432)*
- Product master holds price, stock and variant attributes (e.g. size/colour) with a distinct barcode per variant; stock is tracked per variant/size. Decision: size/variant attributes (small/medium/large) are configurable per product type in the admin panel and appear dynamically when products are added. *(agreed · MoM 19 Aug 2026, 4.2 Product Catalog, Variant & Pricing Management; 5. Key Decisions · DI-354)*
- Entitlement settings: re-entry not allowed / once per day / unlimited; expiry end of week, month, year, variable date, from first use, or by performance date/time; group tickets by fixed price or fixed quantity; one ticket may link to several events. *(agreed · MoM 7 Aug 2026, 16. Entitlement Components: Re-entry, Expiration & Sale Restrictions · DI-171)*
- Components/attributes model: a component (e.g. "ticket type") has attributes (adult, youth, senior, infant, child) each priced independently; adding an attribute creates a new sellable variant with no extra setup. Who may sell a product is restricted by site, operating area, workstation or role. *(agreed · MoM 7 Aug 2026, 12. Products Configuration: Metric Sheets, Pricing & Components · DI-164)*
- Product record holds: price (tax inclusive/exclusive), linked print template, system product code, a toggle for capturing reservation details at sale, and entitlements (upgradeable, stored-value load, linked event, re-entry, linked performance). Multiple price lists per channel and season (winter/summer). *(agreed · MoM 7 Aug 2026, 12. Products Configuration: Metric Sheets, Pricing & Components · DI-163)*

`BO-009` Pricing Rules

- Price Book supports date-based pricing (regular this month, promotional next month). Promotion Builder supports rules such as "buy X get Y", "buy 2 get 1 free" and "buy 3, lowest-priced item discounted" (fully or partially). *(client request · MoM 19 Aug 2026, 4.2 Product Catalog; 4.3 Pricing, Bundles & Promotions · DI-357)*
- Product record holds: price (tax inclusive/exclusive), linked print template, system product code, a toggle for capturing reservation details at sale, and entitlements (upgradeable, stored-value load, linked event, re-entry, linked performance). Multiple price lists per channel and season (winter/summer). *(agreed · MoM 7 Aug 2026, 12. Products Configuration: Metric Sheets, Pricing & Components · DI-163)*
- Prices are set per channel (web store, mobile app, kiosk, walk-up/POS) in one centralised "price matrix"; each channel picks up its price automatically once published. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-140)*

`BO-010` Promotions & Coupons

- Price Book supports date-based pricing (regular this month, promotional next month). Promotion Builder supports rules such as "buy X get Y", "buy 2 get 1 free" and "buy 3, lowest-priced item discounted" (fully or partially). *(client request · MoM 19 Aug 2026, 4.2 Product Catalog; 4.3 Pricing, Bundles & Promotions · DI-357)*
- Dynamic offers apply automatically without a code (buy-2-get-1-free, buy-3-get-2-at-50%-off, fixed amount off a minimum quantity); the discounted item is added to the cart automatically with its price adjusted (e.g. to zero). *(agreed · MoM 7 Aug 2026, 17. Promotions & Dynamic Offers · DI-174)*
- Coupons as one shared promo code (e.g. for social media) or a batch of unique single-use codes, with configurable reuse rules. *(agreed · MoM 7 Aug 2026, 17. Promotions & Dynamic Offers · DI-173)*

`BO-011` Packages & Bundles

- Multi-park / multi-attraction / multi-venue bundles are visually mapped, showing which venues, meal vouchers, VIP parking or upgrade options a bundle includes. *(client request · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies · DI-469)*
- Packages bundle any combination of ticket-type components with package-level pricing (e.g. admission + F&B item + retail item, or admission + show); F&B or retail is not required. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-435)*
- Retail items (e.g. a t-shirt plus a cap) can be combined into a combo package with bundle-level pricing, presented both on-site and online with product images and descriptions. *(client request · MoM 19 Aug 2026, 4.3 Pricing, Bundles & Promotions · DI-358)*
- Bundle packages combine components within one attraction (ticket + meal + retail, or ticket + event ticket) at a discount — not a cross-attraction itinerary. *(agreed · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-220)*

`BO-013` Channel & Distribution

- Catalog Builder & Store Assortment maps which products sell on which channel (on-site, online, or restricted), managed at catalog level rather than per individual product. *(client request · MoM 19 Aug 2026, 4.2 Product Catalog, Variant & Pricing Management · DI-356)*
- Prices are set per channel (web store, mobile app, kiosk, walk-up/POS) in one centralised "price matrix"; each channel picks up its price automatically once published. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-140)*

`BO-015` Performance Calendar

- Time-slot creation asks for start and end date, first and last start time of the day, interval between starts (e.g. every 30 minutes), slot length, days of the week, language and format, and previews the slots before any is created. *(agreed · MoM 24 Sep 2026, M24-01 · DI-995)*
- Example the configuration screens must show concretely: how time slots are created, including start/end dates, times and interval parameters. *(agreed · MoM 24 Sep 2026, 4.3 Back-End Configuration Detail — Requested Format (Screens, Not Just Functional Lists) · DI-986)*
- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Performance capacity is edited individually or by multi-select bulk edit; a performance can be suspended, resumed (any time before start) or cancelled — a state change, never a delete. *(agreed · MoM 7 Aug 2026, 14. Events, Integrations & Performances (Time Slots) · DI-168)*
- Performance (time-slot) creation: date range with chosen weekdays or all days, start/end time, slot duration (e.g. 30 or 60 min), "minutes on screen" (e.g. a 10:00 slot sellable at POS until 10:10), separate entry window (e.g. from 9:30, cut-off 10:20), and an on-sale date range; bulk creation across a date range. *(agreed · MoM 7 Aug 2026, 14. Events, Integrations & Performances (Time Slots) · DI-167)*

`BO-016` Performance Template

- Example the configuration screens must show concretely: how time slots are created, including start/end dates, times and interval parameters. *(agreed · MoM 24 Sep 2026, 4.3 Back-End Configuration Detail — Requested Format (Screens, Not Just Functional Lists) · DI-986)*
- Performances are created individually or from a reusable time-slot template (e.g. every 30 minutes between start and end) that auto-generates the schedule. Capacity set at event level is inherited by performances, with per-performance override (e.g. evening slots). *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-453)*
- Time-slot (performance) tickets configure early/late entry and an entry window (e.g. from 30 minutes before start until a cut-off). Multi-day tickets are consecutive-day or flexible within a range (e.g. any 3 days within a month). *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-447)*
- Event ticket setup: validity window; recurring performances; admission model (general admission, capacity control, reserved seating, resource control, none); seat map, section and quota per sales channel (shared pool or split); resources (e.g. vehicle + driver for a desert safari) checked for availability before sale. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-436)*
- Performance (time-slot) creation: date range with chosen weekdays or all days, start/end time, slot duration (e.g. 30 or 60 min), "minutes on screen" (e.g. a 10:00 slot sellable at POS until 10:10), separate entry window (e.g. from 9:30, cut-off 10:20), and an on-sale date range; bulk creation across a date range. *(agreed · MoM 7 Aug 2026, 14. Events, Integrations & Performances (Time Slots) · DI-167)*

`BO-017` Capacity Management

- Inventory pools split capacity by ticket type (e.g. 50% GA, 30% child, 20% senior) and/or sales channel (e.g. 50% online, 50% on-site), configurable at venue/event level, under a hierarchy global → attraction → product → variant → time slot. On cancel/refund/reschedule the business chooses whether capacity is released or held. *(agreed · MoM 25 Aug 2026, 4.6 Performances & Capacity Management; 4.11 UX Simplification & Distributed Inventory · DI-457)*
- Decision: venue-level admission capacity supersedes event-level capacity; a system prompt/validation prevents configuring or selling an event beyond the remaining venue capacity. Overriding is an authorisation-gated (RBAC) action for authorised users only. *(agreed · MoM 25 Aug 2026, 4.6 Performances & Capacity Management; 5. Key Decisions · DI-456)*
- Two capacity types shown distinctly: sales capacity (tickets sellable per performance) and admission capacity (a real-time, scan-based count of guests inside via entry/exit turnstiles), capping on-site attendance independent of tickets sold. *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-455)*
- AI suggestions from sales forecasts: add/remove time slots, merge under-sold adjacent slots (with guest notification of the time change), and dynamic pricing (raise when a slot is >~80% sold, lower when <~20–30%). *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-454)*
- Performances are created individually or from a reusable time-slot template (e.g. every 30 minutes between start and end) that auto-generates the schedule. Capacity set at event level is inherited by performances, with per-performance override (e.g. evening slots). *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-453)*
- "Envelopes" split a performance's capacity by channel (e.g. of 100: 30 B2C, 40 B2B, 30 on-site); each channel shows only its own share as available. Configured once and applied to all linked performances. *(agreed · MoM 7 Aug 2026, 15. Capacity Splitting via Envelopes · DI-170)*
- Performance capacity is edited individually or by multi-select bulk edit; a performance can be suspended, resumed (any time before start) or cancelled — a state change, never a delete. *(agreed · MoM 7 Aug 2026, 14. Events, Integrations & Performances (Time Slots) · DI-168)*

`BO-018` Allocation & Holds

- Inventory pools split capacity by ticket type (e.g. 50% GA, 30% child, 20% senior) and/or sales channel (e.g. 50% online, 50% on-site), configurable at venue/event level, under a hierarchy global → attraction → product → variant → time slot. On cancel/refund/reschedule the business chooses whether capacity is released or held. *(agreed · MoM 25 Aug 2026, 4.6 Performances & Capacity Management; 4.11 UX Simplification & Distributed Inventory · DI-457)*
- "Envelopes" split a performance's capacity by channel (e.g. of 100: 30 B2C, 40 B2B, 30 on-site); each channel shows only its own share as available. Configured once and applied to all linked performances. *(agreed · MoM 7 Aug 2026, 15. Capacity Splitting via Envelopes · DI-170)*

`BO-019` Closures & Blackouts

- Weekday/calendar rules give different validity and pricing to weekday-only vs. all-days products (e.g. Global Village). Blockout dates exclude some ticket types (e.g. memberships) on public holidays/special days, requiring a separate ticket for those dates. *(client request · MoM 25 Aug 2026, 4.5 Validity Management & Expiry Rules · DI-452)*

`BO-022` Order Detail

- Reservation lookup shows items, customer, payment method, taxes and an optional post-purchase survey, with reprint receipt and regenerate ticket PDF actions. *(agreed · MoM 7 Aug 2026, 20. Live Point-of-Sale Transaction Walkthrough · DI-179)*

`BO-023` Refunds & Exchanges

- Online/app returns: customer submits a return request with a reason (and photo if applicable) → approval team → courier pickup → refund after verified receipt. Confirmed: an item bought at the POS can also be returned via the web portal, subject to approval. *(agreed · MoM 19 Aug 2026, 4.7 Returns, Refunds & Exchanges — In-Store and Online; 5. Key Decisions · DI-367)*
- Bulk refunds: select and refund at event or date level (e.g. ~5,000 transactions for a cancelled event), online and on-site bookings, with one approval step before processing. *(agreed · MoM 12 Aug 2026, 18. Bulk Refund Processing and Refund Requests · DI-269)*
- Refunds use preset time-banded percentages (e.g. full refund a set number of days before the event, less closer to/after it), support partial refunds, and let an authorised approver apply a custom override percentage. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-252)*

`BO-026` Group Bookings

- Group bookings: one shared QR for the whole group (redeemed together at the counter) or one QR per person, each of which the guest can link to their own profile in the mobile app. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-289)*
- Group tickets can carry one shared QR code or individual QR codes, with partial check-in tracking; family tickets bundle adult/child pricing. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-137)*

`BO-028` Refund Approval Queue

- Refund-requests screen lists customer-initiated online requests awaiting a finance/operations decision: accept, request more information, or auto-deny. *(agreed · MoM 12 Aug 2026, 18. Bulk Refund Processing and Refund Requests · DI-270)*
- Bulk refunds: select and refund at event or date level (e.g. ~5,000 transactions for a cancelled event), online and on-site bookings, with one approval step before processing. *(agreed · MoM 12 Aug 2026, 18. Bulk Refund Processing and Refund Requests · DI-269)*
- Guests can request a refund from their account/profile; operations are notified and can approve, reject or ask for more information. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-254)*
- A refund started at the POS is routed for approval before it reaches the bank. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-253)*
- Refunds use preset time-banded percentages (e.g. full refund a set number of days before the event, less closer to/after it), support partial refunds, and let an authorised approver apply a custom override percentage. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-252)*

`BO-029` Report Builder

- Custom report templates (advanced users, SQL/scripting) exported as PDF or Excel; ticket and receipt layouts built in a drag-and-drop template builder placing dynamic variables (guest name, ticket number, QR) on a background image. *(agreed · MoM 7 Aug 2026, 22. Report & Document Template Design · DI-184)*

`BO-031` Asset Register

- A 360-degree asset view, searchable via QR code, consolidates all asset details: attached documentation (installation manuals, wiring diagrams, safety inspection reports), warranty period and full lifecycle history (installed, maintained, operational, upcoming maintenance); a location view shows where each asset physically sits. *(client request · MoM 17 Sep 2026, 4.1 Asset Registry & Classification · DI-910)*
- Corrective-maintenance priority combines a configurable weighted scoring model (e.g. P1 emergency when guest operations are affected) with a direct per-asset priority override field: "if this specific device goes down, raise this priority level". *(agreed · MoM 17 Sep 2026, 4.3 Corrective & Emergency Maintenance · DI-909)*

`BO-032` Admission Profiles

- Tiered access (e.g. Bronze/Silver/Gold): the client fills a matrix of which gates/attractions each tier may scan into; configured as location → admission profile → gate → access point, with explicit deny rules (e.g. Gold denied at the Silver/Bronze entrance). *(agreed · MoM 7 Aug 2026, 24. Tiered Ticketing & Access Control Deep Dive · DI-185)*

`BO-036` Device Registry

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

`BO-039` Shift Directory

- Shift management: assignment and scheduling by cashier/department, templates and policies, opening/closing, exceptions/alerts. Allam: explore merging shift-closing and till-closing screens to reduce dashboard count. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-309)*
- Shift/session view shows open and closed sessions per workstation with expected cash and card totals; a live till monitor shows real-time cash status per workstation and open/close codes. *(agreed · MoM 12 Aug 2026, 19. Cash/Shift and Till Management · DI-273)*

`BO-040` Variance Approval

- Blind cash-out: when closing, the cashier does not see the expected total; the system flags shortage/overage for supervisor review and can optionally block shift closure until the variance is resolved or explained. *(agreed · MoM 12 Aug 2026, 19. Cash/Shift and Till Management · DI-271)*

`BO-043` Daily Reconciliation

- End-of-day reports: cashier shift, till, sales by location, payment type summary, cash management, variance, refund, and consolidated end-of-day (e.g. expected 8,480 AED vs deposited 8,460 AED = 20 AED shortage, posted to an overage/shortage account visible at month-end). *(agreed · MoM 12 Aug 2026, 20. End-of-Day Reports and Overage/Shortage Handling · DI-275)*
- Payments screen consolidates gateway (Stripe, NI) and on-site (cash, card) payments and flags variances from a monthly reconciliation file (e.g. gateway 10,000 AED vs 9,500 AED recorded). *(agreed · MoM 12 Aug 2026, 17. Payments Reconciliation · DI-268)*
- Weekly/monthly reconciliation runs ingest → parse → match → classify → auto-resolve, so only genuinely mismatched amounts are shown for human review. *(agreed · MoM 12 Aug 2026, 11. Settlement and Reconciliation Process · DI-258)*

`BO-045` Menu Management

- Modifiers can be free or chargeable with minimum/maximum selection rules; combo meals support component selection with upgrade options at additional cost. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-328)*
- Product creation captures product name, auto-generated PLU code, category/sub-category, pricing type, inventory-tracking toggle, recipe linkage, unit of measurement and preparation time. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-327)*
- Menu & Product Command Center tracks menus, active recipes and products, and flags products without mapped recipes or with unavailable ingredients. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-325)*

`BO-048` Retail Products

- Retail Product & Catalog Command Center tracks total products per store, classification into catalogs, top products sold and product-by-category breakdowns. *(client request · MoM 19 Aug 2026, 4.2 Product Catalog, Variant & Pricing Management · DI-353)*

`BO-049` Stock Levels

- Warehouse/location structure is a customisable hierarchy (e.g. main warehouse → food warehouse → beverage warehouse), with stock received centrally or directly at an outlet/kitchen for fast-moving perishables. Expiry is tracked at batch/date level; reorder alerts notify staff at a minimum threshold. *(client request · MoM 18 Aug 2026, 4.11 Inventory & Procurement — Item Master, UOM & Costing · DI-345)*
- F&B Stock Command Center shows stock value, low-stock/critical/out-of-stock items and recipe-based ingredient consumption. *(client request · MoM 18 Aug 2026, 4.10 F&B Stock, Wastage & Requisitions · DI-340)*

`BO-050` Stock Position & Valuation

- The system must support both Weighted Average and FIFO costing methods for inventory valuation. *(agreed · MoM 18 Aug 2026, 4.11 Inventory & Procurement; 5. Key Decisions · DI-344)*
- Inventory & Procurement covers both F&B and Retail: total inventory value, item counts and out-of-stock items, broken down by department/sub-department. *(client request · MoM 18 Aug 2026, 4.11 Inventory & Procurement — Item Master, UOM & Costing · DI-342)*

`BO-051` Purchase Orders

- Flow is Purchase Request → Approval → Purchase Order, with RFQ to compare prices from multiple suppliers. Three PO types: Regular (item/quantity/price entry), Contract (pre-agreed fixed price for a period, auto-picked on later orders) and Service (non-inventory items/services). *(agreed · MoM 18 Aug 2026, 4.13 Supplier & Purchase Order Management; 5. Key Decisions · DI-348)*

`BO-052` Goods Receipt

- Warehouse/location structure is a customisable hierarchy (e.g. main warehouse → food warehouse → beverage warehouse), with stock received centrally or directly at an outlet/kitchen for fast-moving perishables. Expiry is tracked at batch/date level; reorder alerts notify staff at a minimum threshold. *(client request · MoM 18 Aug 2026, 4.11 Inventory & Procurement — Item Master, UOM & Costing · DI-345)*

`BO-054` Role Assignment

- Allam: add a "roles comparison" view letting an admin compare two roles side by side (e.g. confirm a cashier role lacks the refund/void permissions a supervisor role has). *(agreed · MoM 7 Aug 2026, 4. Roles & User Management · DI-153)*

`BO-058` Reporting Home

- Report library filterable by site, operating area, sales channel, workstation or user; e.g. Sales Report (payment-method breakdown, totals, voids, deposits, itemised ticket sales) and Payment Summary (per-cashier breakdown). *(agreed · MoM 7 Aug 2026, 21. Dashboards & Reporting · DI-183)*
- Sales reporting can be scoped to an operating area, showing all transactions from its workstations. *(agreed · MoM 7 Aug 2026, 3. Operating Areas, Workstations & Permissions Hierarchy · DI-151)*

`BO-059` Sales Reports

- End-of-day reports: cashier shift, till, sales by location, payment type summary, cash management, variance, refund, and consolidated end-of-day (e.g. expected 8,480 AED vs deposited 8,460 AED = 20 AED shortage, posted to an overage/shortage account visible at month-end). *(agreed · MoM 12 Aug 2026, 20. End-of-Day Reports and Overage/Shortage Handling · DI-275)*
- Report library filterable by site, operating area, sales channel, workstation or user; e.g. Sales Report (payment-method breakdown, totals, voids, deposits, itemised ticket sales) and Payment Summary (per-cashier breakdown). *(agreed · MoM 7 Aug 2026, 21. Dashboards & Reporting · DI-183)*
- Sales reporting can be scoped to an operating area, showing all transactions from its workstations. *(agreed · MoM 7 Aug 2026, 3. Operating Areas, Workstations & Permissions Hierarchy · DI-151)*

`BO-060` Attendance & Footfall

- Admission Summary dashboard: real-time headcount of guests inside the venue from ticket scans. *(agreed · MoM 7 Aug 2026, 21. Dashboards & Reporting · DI-182)*

`BO-063` Opening Hours & Calendar

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- The operating calendar is configurable: a midnight-to-midnight transaction day or an alternative such as 6am to 6am. *(agreed · MoM 7 Aug 2026, 2. System Organization: Tenant & Site Setup · DI-149)*

`BO-065` Venue Configuration

- Denominations configurable per currency/region (e.g. UAE 500, 200, 100, 50, 20; Bahrain has no 1000); amounts use 2 decimals (UAE) or 3 (Bahrain/Kuwait) with no rounding of the third decimal (2.013 stays 2.013). *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-306)*
- The operating calendar is configurable: a midnight-to-midnight transaction day or an alternative such as 6am to 6am. *(agreed · MoM 7 Aug 2026, 2. System Organization: Tenant & Site Setup · DI-149)*

`BO-067` Integrations

- Financial year/period setup varies by country (UAE Jan–Dec, India Apr–Mar); closing a period locks further postings. An ERP integration centre manages external connections. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-263)*

`BO-068` Audit Log

- Audit history shows logins, shift start/end and every change made (old value vs new value) on every screen and transaction; logging can be switched on/off and archived. *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-158)*

`BO-069` Asset Register

- Work-order priority is shown with its source side by side (scored by venue policy, asset override, or manual); an asset carries a "fault priority override"; a new work order leaves priority empty to be scored; the venue sets weights and bands (safety, guest operations, revenue, asset criticality, summing to 100). *(agreed · MoM 17 Sep 2026, M17-01 · DI-923)*
- A 360-degree asset view, searchable via QR code, consolidates all asset details: attached documentation (installation manuals, wiring diagrams, safety inspection reports), warranty period and full lifecycle history (installed, maintained, operational, upcoming maintenance); a location view shows where each asset physically sits. *(client request · MoM 17 Sep 2026, 4.1 Asset Registry & Classification · DI-910)*
- Corrective-maintenance priority combines a configurable weighted scoring model (e.g. P1 emergency when guest operations are affected) with a direct per-asset priority override field: "if this specific device goes down, raise this priority level". *(agreed · MoM 17 Sep 2026, 4.3 Corrective & Emergency Maintenance · DI-909)*

`BO-070` Work Orders

- Smart assignment (confirmed by the maintenance head): technicians ranked by skill, shift and load; the ranking assigns nothing and Assign on a row does; outside vendor requests listed on the work order. *(agreed · MoM 17 Sep 2026, M17-13 · DI-924)*
- Work-order priority is shown with its source side by side (scored by venue policy, asset override, or manual); an asset carries a "fault priority override"; a new work order leaves priority empty to be scored; the venue sets weights and bands (safety, guest operations, revenue, asset criticality, summing to 100). *(agreed · MoM 17 Sep 2026, M17-01 · DI-923)*
- Work orders assigned to a technician must be visible on a technician-facing mobile app so field staff see assigned tasks and act directly from their device; execution shows a repair checklist, spare parts/tools consumed, a timeline (assigned, started, part requests) and a functional-test checklist before completion. *(client request · MoM 17 Sep 2026, 4.4 Work Order Management & Execution · DI-911)*
- Corrective-maintenance priority combines a configurable weighted scoring model (e.g. P1 emergency when guest operations are affected) with a direct per-asset priority override field: "if this specific device goes down, raise this priority level". *(agreed · MoM 17 Sep 2026, 4.3 Corrective & Emergency Maintenance · DI-909)*
- Calendars must support filtering by asset category so a team only sees maintenance relevant to them, e.g. an IT team sees turnstiles, printers and POS terminals, not unrelated categories. *(agreed · MoM 17 Sep 2026, 4.2 Preventive Maintenance Planning · DI-908)*
- Device maintenance: preventive cycles (quarterly, half-yearly, seasonal) on a calendar by device type; staff log faulty devices which raise work orders; diagnostic workspace for the engineer; warranty and maintenance history; return to service. *(client request · MoM 15 Sep 2026, 4.6 Device Maintenance & Lifecycle Servicing · DI-902)*

`BO-071` Planned Maintenance

- Calendars must support filtering by asset category so a team only sees maintenance relevant to them, e.g. an IT team sees turnstiles, printers and POS terminals, not unrelated categories. *(agreed · MoM 17 Sep 2026, 4.2 Preventive Maintenance Planning · DI-908)*
- Device maintenance: preventive cycles (quarterly, half-yearly, seasonal) on a calendar by device type; staff log faulty devices which raise work orders; diagnostic workspace for the engineer; warranty and maintenance history; return to service. *(client request · MoM 15 Sep 2026, 4.6 Device Maintenance & Lifecycle Servicing · DI-902)*

`BO-073` Lost & Found Register

- Lost & Found: guests log lost items in the app; back-office staff match and mark items found for collection, with full tracking. *(client request · MoM 10 Aug 2026, 4.6 AI Functions, Lost & Found, Reviews, Loyalty · DI-208)*

`BO-074` Chart of Accounts

- Chart of accounts screen: external-system codes for ERP mapping, classification (asset, liability, income, expense), parent-account hierarchy and edit view with financial dimensions (profit centre, cost centres); plus transaction-to-account and payment/offset account mapping. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-262)*
- Chart of accounts can be created natively in TICVAI or mapped to a client's external/ERP chart of accounts. *(agreed · MoM 12 Aug 2026, 13. Chart of Accounts and Account Mapping · DI-259)*

`BO-075` Account Mapping

- Chart of accounts screen: external-system codes for ERP mapping, classification (asset, liability, income, expense), parent-account hierarchy and edit view with financial dimensions (profit centre, cost centres); plus transaction-to-account and payment/offset account mapping. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-262)*
- Chart of accounts can be created natively in TICVAI or mapped to a client's external/ERP chart of accounts. *(agreed · MoM 12 Aug 2026, 13. Chart of Accounts and Account Mapping · DI-259)*

`BO-076` Revenue Recognition

- Revenue allocation split builder splits a combo/package price across products (tickets, F&B) or legal entities (e.g. a two-venue two-day pass), by fixed amount or percentage. *(agreed · MoM 12 Aug 2026, 16. Revenue Recognition Rules and Allocation Splits · DI-267)*
- Revenue allocation screen graphs recognised vs unrecognised (wallet) revenue and holds recognition rules, e.g. F&B on sale; annual membership straight-line monthly (1,500 AED → 150 AED/month, balance at expiry). *(client request · MoM 12 Aug 2026, 16. Revenue Recognition Rules and Allocation Splits · DI-266)*

`BO-077` FX Rates & Variances

- POS applies the same foreign-currency display/charge logic, records in base currency, and has a report of total foreign-currency collections by currency. *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-213)*
- Back office supports both a manually set rate with margin (Qossai: ~90% of regional clients, e.g. 3.80 when market is 3.68) and a live third-party FX-rate feed (e.g. XE). *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-212)*

`BO-078` Requisitions

- Flow is Purchase Request → Approval → Purchase Order, with RFQ to compare prices from multiple suppliers. Three PO types: Regular (item/quantity/price entry), Contract (pre-agreed fixed price for a period, auto-picked on later orders) and Service (non-inventory items/services). *(agreed · MoM 18 Aug 2026, 4.13 Supplier & Purchase Order Management; 5. Key Decisions · DI-348)*
- Production execution & batch management shows planned vs. actual vs. yield quantity and batch losses; wastage/spoilage must be recorded per item. Outlets raise requisitions to replenish from the central warehouse. *(client request · MoM 18 Aug 2026, 4.10 F&B Stock, Wastage & Requisitions · DI-341)*
- Requisitions raised in the app flow to department-head approval then purchasing; stock falling below a par level (e.g. 100 units) auto-creates a draft requisition for review and confirmation. *(client request · MoM 10 Aug 2026, 5.4 Inventory & Procurement · DI-234)*

`BO-080` Stock Transfers

- Outlets raise inter-store requisitions subject to an approval workflow before transfer; stock can be transferred between any two stores (outlet-to-outlet, warehouse-to-outlet, outlet-to-warehouse). *(client request · MoM 19 Aug 2026, 4.5 Inventory Management — Requisitions, Transfers & Stock Counts · DI-362)*
- Stock is centralised per venue across web, app, kiosk and POS and not shared across venues; sale is gated by the system-recorded stock (an outlet with no system stock cannot sell even if physically present); inter-venue stock transfer moves stock. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-294)*

`BO-081` Inventory Items

- Warehouse/location structure is a customisable hierarchy (e.g. main warehouse → food warehouse → beverage warehouse), with stock received centrally or directly at an outlet/kitchen for fast-moving perishables. Expiry is tracked at batch/date level; reorder alerts notify staff at a minimum threshold. *(client request · MoM 18 Aug 2026, 4.11 Inventory & Procurement — Item Master, UOM & Costing · DI-345)*
- Item Master captures category, item type, status and unit of measurement, with pack-size conversions (e.g. 1 carton = 24 pieces; 1 case = 2 litres = 2000 ml). *(client request · MoM 18 Aug 2026, 4.11 Inventory & Procurement — Item Master, UOM & Costing · DI-343)*

`BO-083` Suppliers

- Suppliers are categorised (F&B, retail, engineering, etc.); the Supplier Master holds details, linked item categories, compliance documents and performance scorecards. Spend analysis shows category-, supplier- and contract-wise spend. *(client request · MoM 18 Aug 2026, 4.13 Supplier & Purchase Order Management · DI-347)*

`BO-089` Journal Entries

- Journal entry list of posted debits/credits, with manual journal entry that needs approval: a finance user posts a voucher, a finance manager/director approves, only then it hits the ledger. *(client request · MoM 12 Aug 2026, 15. Financial Transactions Ledger and Journal Entries · DI-265)*

`BO-090` Period Close

- Financial year/period setup varies by country (UAE Jan–Dec, India Apr–Mar); closing a period locks further postings. An ERP integration centre manages external connections. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-263)*

`BO-091` AI Policy & Spend

- AI operations monitoring shows health, cost/budget tracking and which AI agents consume the most resources and for what purpose, so the business can manage AI spend. *(client request · MoM 21 Sep 2026, 4.11 Core AI Platform — Operations & Consumption Monitoring · DI-968)*

`BO-092` Venue Maps

- **Open question.** Physical rental booths/stations need to appear on the live venue map; open whether the map builder already covers booth/station configuration or a dedicated addition is needed (Chinmay to check). *(open · MoM 9 Sep 2026, 4.11 Follow-Ups from Prior Sessions · DI-773)*
- **Open question.** Customisable venue map showing attractions, dining, retail and restrooms. Qossai: define image/format guidance for tenant map uploads; benchmark is the Kidzania app's interactive 3D-style map. Final guidance still open. *(open · MoM 10 Aug 2026, 4.4 Venue Map, Queueing, F&B, Retail & Parking · DI-203)*

`BO-093` Map Import & Labelling

- The 3D seat view needs the venue's actual CAD file with defined seating sections uploaded; setup is more involved than the 2D seat map. *(agreed · MoM 15 Sep 2026, 4.2 Guest Web App - 3D Stadium Seat View & At-Venue Wayfinding · DI-890)*
- Chinmay: near-term AI can generate a map/seating layout and the related ticket configuration once a venue uploads its map schema and layout image. *(client request · MoM 14 Aug 2026, 1. AI Configuration Assistant — Phase-One Scope · DI-281)*
- Qossai: AI-assisted layout generation from AutoCAD/DXF (best) or PDF (fallback, via OCR), targeting ~90–95% automation with the client correcting the rest; sample input is a PDF seating diagram plus an Excel manifest of section/row/seat numbers. *(agreed · MoM 5 Aug 2026, 9. Seat Mapping & Venue Builder · DI-145)*

`BO-094` Map Editor & Publish

- Retail/kiosk shops are added to the planner's venue-linked options alongside F&B (previously only F&B). *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1100)*
- The 3D seat view needs the venue's actual CAD file with defined seating sections uploaded; setup is more involved than the 2D seat map. *(agreed · MoM 15 Sep 2026, 4.2 Guest Web App - 3D Stadium Seat View & At-Venue Wayfinding · DI-890)*
- **Open question.** Physical rental booths/stations need to appear on the live venue map; open whether the map builder already covers booth/station configuration or a dedicated addition is needed (Chinmay to check). *(open · MoM 9 Sep 2026, 4.11 Follow-Ups from Prior Sessions · DI-773)*

`BO-095` Resources

- Optional resource module: a template defines the resource types a product needs (e.g. a vehicle and a driver); named resources have an availability calendar/roster; at sale (POS or online) both resource availability and capacity are checked before booking. *(agreed · MoM 7 Aug 2026, 18. Resource Management · DI-175)*

`BO-096` Resource Calendar

- Cleaning buffer is configurable. Option A: fixed buffer (e.g. 15 min) after every booking. Option B: N cleanings per day; the system places the buffers into the day's schedule and adjusts availability. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W10 Meeting-room cleaning buffer · DI-1012)*
- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Optional resource module: a template defines the resource types a product needs (e.g. a vehicle and a driver); named resources have an availability calendar/roster; at sale (POS or online) both resource availability and capacity are checked before booking. *(agreed · MoM 7 Aug 2026, 18. Resource Management · DI-175)*

`BO-100` Venue Home

- Offline policies and a venue-level Operations Summary dashboard aggregating department-level views into one venue overview. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-311)*
- The dashboard is the venue command centre: KPI cards (Total Revenue, Tickets Sold, Net Profit, Avg. Order Value, each with delta vs last 7 days); Live Visitors with capacity % and "Updated just now"; Revenue Overview (Day/Week/Month/Year); AI Insights (e.g. "Increase VIP ticket price by 8%"); Sales by Channel; Operational Status per area (Operational/Attention); Activity Feed; Top Events; At a Glance strip. *(agreed · Design Vision Book 29 Jul 2026, 04 Dashboard Vision (p4) - dashboard content · DI-031)*

`BO-1005` Hold Pool Creation

- Chinmay: reservations/holds are made section-wise (choose section → choose/hold seats within it), not by a freeform polygon selection as in the AI-generated reference mockup. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules & Social Distancing Configuration · DI-415)*

`BO-1008` Automatic Hold Release

- Decision: seats held in a cart auto-release after a configurable timeout if checkout is abandoned, and immediately if a payment attempt fails. *(agreed · MoM 21 Aug 2026, 4.6 Seat Inventory Status; 5. Key Decisions · DI-422)*

`BO-1013` Rules Command Center

- Decision: seating rules — consecutive-seat enforcement (no single empty seat left between bookings), social-distancing buffer (auto-block adjacent seats), seat-kill rule, company/held-seat rule — are configurable per venue/event, defaulting to the venue's operational policy. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules; 5. Key Decisions · DI-416)*

`BO-1014` Seat Kill Rules

- Decision: seating rules — consecutive-seat enforcement (no single empty seat left between bookings), social-distancing buffer (auto-block adjacent seats), seat-kill rule, company/held-seat rule — are configurable per venue/event, defaulting to the venue's operational policy. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules; 5. Key Decisions · DI-416)*

`BO-1015` Buffer Seat Rules

- Decision: seating rules — consecutive-seat enforcement (no single empty seat left between bookings), social-distancing buffer (auto-block adjacent seats), seat-kill rule, company/held-seat rule — are configurable per venue/event, defaulting to the venue's operational policy. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules; 5. Key Decisions · DI-416)*

`BO-1021` Flexible Spacing Rules

- Decision: seating rules — consecutive-seat enforcement (no single empty seat left between bookings), social-distancing buffer (auto-block adjacent seats), seat-kill rule, company/held-seat rule — are configurable per venue/event, defaulting to the venue's operational policy. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules; 5. Key Decisions · DI-416)*

`BO-1024` Group Type Configuration

- **Open question.** Do Tour operator and Community become their own group types or map to general? Default built: School, Corporate, Tour operator and Community shown as their own group types (platform also has general and party). *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Group types · DI-1115)*

`BO-1034` Best Seat Recommendations

- Best-seat ranking (e.g. last-row-is-best vs. first-row-is-best, by venue sightlines) is configurable per seat map/event so the system recommends or auto-assigns the right best available seat. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules & Social Distancing Configuration · DI-414)*
- **Open question.** Open: how the seat map builder consolidates the reference tool's separate screens (canvas, standing zone, suite, best-seats, entrances/exits) into one unified screen — Chinmay's team to confirm. *(open · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types (action) · DI-413)*

`BO-105` Stock & Supply

- Inventory & Procurement covers both F&B and Retail: total inventory value, item counts and out-of-stock items, broken down by department/sub-department. *(client request · MoM 18 Aug 2026, 4.11 Inventory & Procurement — Item Master, UOM & Costing · DI-342)*

`BO-1066` Roles, Permissions & Masking

- Allam: add a "roles comparison" view letting an admin compare two roles side by side (e.g. confirm a cashier role lacks the refund/void permissions a supervisor role has). *(agreed · MoM 7 Aug 2026, 4. Roles & User Management · DI-153)*

`BO-1073` API Access & OAuth

- Production access status is shown: sandbox only, requested (pending), approved, or rejected with the reason. Production keys only after certification; the request form says a new production key is issued and the sandbox key stays sandbox. *(agreed · MoM 17 Sep 2026, M17-06 · DI-927)*
- API scopes are picked from a list grouped by module ({module}.read / {module}.write), with unlicensed modules shown disabled rather than hidden; the API reference is grouped by licensable module, then contract. *(agreed · MoM 17 Sep 2026, M17-05, M17-12 · DI-926)*

`BO-1081` Finance Dashboard

- Finance dashboard: gross, net, recognised and deferred revenue and refunds, with charts selectable by period. Allam's screens are a base for TICVAI's design, not a template to copy. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-260)*

`BO-1083` Wallet Command Center

- Wallet dashboard gives an overview of all live wallet balances: total wallet value, total spend and total recharge activity. *(client request · MoM 27 Aug 2026, 4.1 Wallet Foundation & Dashboard · DI-507)*

`BO-1084` Wallet Type Library

- Wallet type library: multiple wallet types (guest, family, membership wallet), each assigned to a category (individual, corporate, member). Provisioning rules set the trigger that creates a wallet (membership purchase, first top-up); two patterns: gift-card style (pre-defined value products listed on the website) and open-ended "add money to wallet". *(client request · MoM 27 Aug 2026, 4.2 Wallet Type Library, Ownership & Account Association · DI-508)*

`BO-1085` Wallet Creation & Provisioning Rules

- Wallet type library: multiple wallet types (guest, family, membership wallet), each assigned to a category (individual, corporate, member). Provisioning rules set the trigger that creates a wallet (membership purchase, first top-up); two patterns: gift-card style (pre-defined value products listed on the website) and open-ended "add money to wallet". *(client request · MoM 27 Aug 2026, 4.2 Wallet Type Library, Ownership & Account Association · DI-508)*

`BO-1086` Wallet Ownership & Account Association

- Ownership and access rules are configurable per wallet type. Family default: only the parent/guardian can top up; children can view balance and transactions and spend, but cannot top up unless permissions are explicitly reconfigured. Guest wallet screens must hide or disable top-up for members without the right. *(agreed · MoM 27 Aug 2026, 4.2 Wallet Ownership / 4.8 Family Permission Rules · DI-509)*

`BO-1087` Wallet Currency & Monetary Configuration

- Currency config sets supported currencies and maximum balance; foreign-currency top-up (e.g. USD) is converted at a configured exchange rate and credited in local currency. Credit types (cash, bonus, gift-card credit) are each classified monetary or non-monetary (e.g. a meal voucher redeemable only for a specific item). *(client request · MoM 27 Aug 2026, 4.3 Currency, Credit Types & Wallet Feature Profile · DI-510)*

`BO-1088` Credit & Balance Type Configuration

- Currency config sets supported currencies and maximum balance; foreign-currency top-up (e.g. USD) is converted at a configured exchange rate and credited in local currency. Credit types (cash, bonus, gift-card credit) are each classified monetary or non-monetary (e.g. a meal voucher redeemable only for a specific item). *(client request · MoM 27 Aug 2026, 4.3 Currency, Credit Types & Wallet Feature Profile · DI-510)*

`BO-1089` Wallet Feature Profile

- Wallet feature profile (global, optionally per wallet type) lists permitted actions such as top-up allowed, refund allowed. Example: a AED 100 membership-benefit voucher is spendable but not refundable/cashable-out. *(client request · MoM 27 Aug 2026, 4.3 Wallet Feature Profile · DI-511)*

`BO-109` Menu Builder & POS Layout Designer

- Menu Builder defines the front-end POS layout per outlet — categories, item tiles (image, name, price) and configurable button sizes for fast-selling items. Agreed the current (reference) layout is a reference only and the UI/UX can be improved. *(agreed · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-326)*
- Drag-and-drop POS "sales board" designer placing products and system functions (ticket list, reservation list, transaction list, media lookup) as buttons with custom fonts and colours. Allam: the old interface is NOT a design reference — functional concept only. *(agreed · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-157)*

`BO-1090` Wallet Lifecycle Configuration

- Wallet statuses: active, suspended, blocked, closed. Every wallet must have a validity period (never open-ended); on lapse the remaining balance, monetary or non-monetary, is automatically swept to a finance-designated account. *(agreed · MoM 27 Aug 2026, 4.4 Wallet Lifecycle, Numbering & Publish Flow · DI-512)*

`BO-1091` Wallet Numbering, Identity & Digital Credentials

- Each wallet gets a unique wallet code (like a ticket number) with configurable association to physical/digital media: QR code, RFID/wristband or other media types, usable across channels. *(client request · MoM 27 Aug 2026, 4.4 Wallet Numbering / 4.9 Wallet-to-media linking · DI-513)*

`BO-1092` Wallet Configuration Preview, Validation & Publication

- A final review/publish screen summarises the completed wallet-type configuration (rules, applicable channels) before it goes live. *(client request · MoM 27 Aug 2026, 4.4 Wallet Lifecycle, Numbering & Publish Flow · DI-514)*

`BO-1093` Funding Command Center

- Top-up dashboard shows all top-ups (successful or failed) and funding-by-source breakdown (credit card, debit card, cash, etc.) with totals by day, month and year. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-515)*

`BO-1094` Funding Method Configuration

- Funding methods: cash, card, online, POS, kiosk self-service, plus manual admin funding used to issue a goodwill/service-recovery credit to a guest's wallet. Chinmay raised role-based permission for staff funding wallets. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-516)*

`BO-1095` Top-Up Rule Configuration

- Top-up rules set minimum and maximum amounts per transaction; channel/funding-source mapping restricts which payment methods each channel offers (e.g. cash top-up on-site only, not online), so each channel's top-up screen offers only its allowed methods. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-517)*
- Stored value configuration: minimum stored value, maximum top-up balance, expiry of stored balance, and refund destination (original payment method or back to wallet balance). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-468)*

`BO-1096` Channel & Funding Source Mapping

- Top-up rules set minimum and maximum amounts per transaction; channel/funding-source mapping restricts which payment methods each channel offers (e.g. cash top-up on-site only, not online), so each channel's top-up screen offers only its allowed methods. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-517)*

`BO-1097` Auto-Reload Configuration

- Auto-reload (tops up a configured amount when balance falls below a threshold) and a separate recurring funding schedule (calendar-based, e.g. a fixed amount every Monday). Allam: auto-reload is a nice-to-have without a confirmed use case; Chinmay: keep it for high-value/frequent guests. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-518)*

`BO-1098` Recurring Funding Schedule

- Auto-reload (tops up a configured amount when balance falls below a threshold) and a separate recurring funding schedule (calendar-based, e.g. a fixed amount every Monday). Allam: auto-reload is a nice-to-have without a confirmed use case; Chinmay: keep it for high-value/frequent guests. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-518)*

`BO-1099` Funding Authorization & Approval Rules

- Funding approval rules: a top-up above a configured threshold requires supervisor or finance approval via supervisor login. Top-up reversal (full or partial, back to the original payment method) requires manual verification/authorisation before processing. *(agreed · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-520)*

`BO-110` Recipe & BOM Management

- Recipe & BOM captures ingredient quantity, unit, cost (from purchase data), preparation time, yield, selling price and margin. Ingredient substitution uses an alternate ingredient automatically when the primary is out of stock; production planning aggregates recipe requirements to forecast prepared-item quantities. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-329)*
- Menu & Product Command Center tracks menus, active recipes and products, and flags products without mapped recipes or with unavailable ingredients. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-325)*

`BO-1100` Funding Reversal & Correction Management

- Funding approval rules: a top-up above a configured threshold requires supervisor or finance approval via supervisor login. Top-up reversal (full or partial, back to the original payment method) requires manual verification/authorisation before processing. *(agreed · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-520)*

`BO-1101` Funding Limits & Velocity Controls

- Funding limits and velocity controls (daily, monthly, min and max transaction thresholds), and a funding audit trail listing all top-up transactions for any period or account. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-521)*

`BO-1102` Funding Transaction Audit & Reconciliation

- Funding limits and velocity controls (daily, monthly, min and max transaction thresholds), and a funding audit trail listing all top-up transactions for any period or account. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-521)*

`BO-1104` Credit Type Definition Studio

- A combo product can bundle admission with stored-value credit the guest draws down on F&B or retail purchases (wallet mechanics in a dedicated session). *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-459)*

`BO-1105` Credit Issuance Rule Configuration

- Bonus credit tiers (e.g. AED 100 top-up earns AED 20 bonus; AED 200 earns AED 60). Bonus credit is consumed before base top-up credit and carries its own separate validity period. *(agreed · MoM 27 Aug 2026, 4.6 Stored Value, Credit Consumption & FEFO Logic · DI-524)*

`BO-1106` Credit Usage & Eligibility Rules

- Credit usage restrictions scope a credit to spend categories (e.g. usable for food & beverage, not retail), fully configurable; with no restriction the balance is spendable on anything offered. *(client request · MoM 27 Aug 2026, 4.6 Stored Value, Credit Consumption & FEFO Logic · DI-522)*

`BO-1107` Consumption Priority Engine

- Bonus credit tiers (e.g. AED 100 top-up earns AED 20 bonus; AED 200 earns AED 60). Bonus credit is consumed before base top-up credit and carries its own separate validity period. *(agreed · MoM 27 Aug 2026, 4.6 Stored Value, Credit Consumption & FEFO Logic · DI-524)*
- Consumption is fully automatic FEFO (nearest expiry first). Guests see their balance and the expiry breakdown per top-up lot in their profile but cannot choose which lot is drawn down; no lot picker at payment. *(agreed · MoM 27 Aug 2026, 4.6 Stored Value, Credit Consumption & FEFO Logic · DI-523)*

`BO-1108` Expiry & Validity Policy Configuration

- Wallet statuses: active, suspended, blocked, closed. Every wallet must have a validity period (never open-ended); on lapse the remaining balance, monetary or non-monetary, is automatically swept to a finance-designated account. *(agreed · MoM 27 Aug 2026, 4.4 Wallet Lifecycle, Numbering & Publish Flow · DI-512)*
- Stored value configuration: minimum stored value, maximum top-up balance, expiry of stored balance, and refund destination (original payment method or back to wallet balance). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-468)*

`BO-1109` FEFO & Credit Lot Management

- Consumption is fully automatic FEFO (nearest expiry first). Guests see their balance and the expiry breakdown per top-up lot in their profile but cannot choose which lot is drawn down; no lot picker at payment. *(agreed · MoM 27 Aug 2026, 4.6 Stored Value, Credit Consumption & FEFO Logic · DI-523)*

`BO-111` Ingredient Substitution, Allergen & Nutrition

- Recipe & BOM captures ingredient quantity, unit, cost (from purchase data), preparation time, yield, selling price and margin. Ingredient substitution uses an alternate ingredient automatically when the primary is out of stock; production planning aggregates recipe requirements to forecast prepared-item quantities. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-329)*

`BO-1110` Split Tender & Multi-Credit Consumption

- Split tender: one purchase paid with wallet balance plus another method, e.g. AED 500 from the wallet and the remaining AED 200 of a AED 700 purchase on a credit card. *(agreed · MoM 27 Aug 2026, 4.7 Split-Tender, Redemption Rules & Configuration Simulation · DI-525)*

`BO-1111` Credit Expiry, Extension & Forfeiture Operations

- Credit expiry and extension operations give admins a customer-level view of all wallet balances and their expiry dates to manage upcoming expiries. *(client request · MoM 27 Aug 2026, 4.7 Split-Tender, Redemption Rules & Configuration Simulation · DI-527)*

`BO-1112` Consumption Simulator, Validation & Rule Publication

- Configuration simulation/test mode lets an admin run sample transactions against a wallet configuration (e.g. spend-category restrictions) before publishing, instead of discovering errors live. *(agreed · MoM 27 Aug 2026, 4.7 Configuration simulation tool · DI-528)*

`BO-1115` Family & Household Structure Configuration

- Wallet balance is shared across a linked family — a parent's top-up can be drawn down by a linked child's wristband without a separate top-up. *(agreed · MoM 20 Aug 2026, 4.1 CRM; 4.5 Loyalty, Membership & Wallet · DI-374)*

`BO-1116` Parent–Child Stored Value Distribution

- A parent's wallet funds linked child wristbands/wallets with per-child spending allowances, e.g. of a AED 500 family balance one child is capped at AED 200 and another at AED 200. *(agreed · MoM 27 Aug 2026, 4.8 Family, Parent-Child & Corporate Wallets · DI-529)*
- Wallet balance is shared across a linked family — a parent's top-up can be drawn down by a linked child's wristband without a separate top-up. *(agreed · MoM 20 Aug 2026, 4.1 CRM; 4.5 Loyalty, Membership & Wallet · DI-374)*

`BO-1117` Allowance & Budget Allocation Engine

- A parent's wallet funds linked child wristbands/wallets with per-child spending allowances, e.g. of a AED 500 family balance one child is capped at AED 200 and another at AED 200. *(agreed · MoM 27 Aug 2026, 4.8 Family, Parent-Child & Corporate Wallets · DI-529)*

`BO-1118` Member Spending Controls & Permissions

- Ownership and access rules are configurable per wallet type. Family default: only the parent/guardian can top up; children can view balance and transactions and spend, but cannot top up unless permissions are explicitly reconfigured. Guest wallet screens must hide or disable top-up for members without the right. *(agreed · MoM 27 Aug 2026, 4.2 Wallet Ownership / 4.8 Family Permission Rules · DI-509)*

`BO-1119` Corporate Wallet & Organizational Hierarchy

- Corporate/group wallets: funds loaded and segregated across departments (e.g. marketing, operations) for company accounts. *(client request · MoM 27 Aug 2026, 4.8 Family, Parent-Child & Corporate Wallets · DI-531)*

`BO-112` Production Planning & Production Sheets

- Recipe & BOM captures ingredient quantity, unit, cost (from purchase data), preparation time, yield, selling price and margin. Ingredient substitution uses an alternate ingredient automatically when the primary is out of stock; production planning aggregates recipe requirements to forecast prepared-item quantities. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-329)*

`BO-1120` Corporate Budget, Policy & Approval Rules

- Corporate/group wallets: funds loaded and segregated across departments (e.g. marketing, operations) for company accounts. *(client request · MoM 27 Aug 2026, 4.8 Family, Parent-Child & Corporate Wallets · DI-531)*

`BO-1121` Shared Wallet Transfers & Balance Reallocation

- Balance can move between linked family/group wallets in either direction (parent to child, child to parent); a venue-controlled toggle, not always enabled. *(agreed · MoM 27 Aug 2026, 4.8 Shared wallet transfer · DI-532)*

`BO-1122` Shared Wallet Simulator, Monitoring & Audit

- Configuration simulation/test mode lets an admin run sample transactions against a wallet configuration (e.g. spend-category restrictions) before publishing, instead of discovering errors live. *(agreed · MoM 27 Aug 2026, 4.7 Configuration simulation tool · DI-528)*

`BO-1124` Gift Card Product Configuration

- Two variants: monetary gift card (value usable on anything the venue offers) and product-specific gift voucher (redeemable only for a named product, e.g. a dolphin-show voucher). Redemption channel is configurable: online, on-site or both. *(client request · MoM 27 Aug 2026, 4.9 Gift Cards, Vouchers & Wallet Payments · DI-533)*

`BO-1126` Voucher & Coupon Type Configuration

- Two variants: monetary gift card (value usable on anything the venue offers) and product-specific gift voucher (redeemable only for a named product, e.g. a dolphin-show voucher). Redemption channel is configurable: online, on-site or both. *(client request · MoM 27 Aug 2026, 4.9 Gift Cards, Vouchers & Wallet Payments · DI-533)*
- Coupons as one shared promo code (e.g. for social media) or a batch of unique single-use codes, with configurable reuse rules. *(agreed · MoM 7 Aug 2026, 17. Promotions & Dynamic Offers · DI-173)*

`BO-1127` Voucher Eligibility & Redemption Rule Studio

- Two variants: monetary gift card (value usable on anything the venue offers) and product-specific gift voucher (redeemable only for a named product, e.g. a dolphin-show voucher). Redemption channel is configurable: online, on-site or both. *(client request · MoM 27 Aug 2026, 4.9 Gift Cards, Vouchers & Wallet Payments · DI-533)*
- Partial vs full redemption is configurable per wallet/gift-card type: some allow spending part and keeping the remainder, others require full redemption in a single transaction. *(agreed · MoM 27 Aug 2026, 4.7 Split-Tender, Redemption Rules & Configuration Simulation · DI-526)*

`BO-1132` Gift Card & Voucher Simulator, Validation & Publication

- Configuration simulation/test mode lets an admin run sample transactions against a wallet configuration (e.g. spend-category restrictions) before publishing, instead of discovering errors live. *(agreed · MoM 27 Aug 2026, 4.7 Configuration simulation tool · DI-528)*

`BO-1133` Wallet Usage & Channel Command Center

- Wallet spend reported by department/category (F&B, attractions, retail, partners) and by channel (B2C, POS); payment/redemption policy can set rules such as a minimum spend to use the wallet as a payment method. *(client request · MoM 27 Aug 2026, 4.9 Gift Cards, Vouchers & Wallet Payments · DI-534)*

`BO-1135` Wallet Payment & Redemption Policy

- Wallet spend reported by department/category (F&B, attractions, retail, partners) and by channel (B2C, POS); payment/redemption policy can set rules such as a minimum spend to use the wallet as a payment method. *(client request · MoM 27 Aug 2026, 4.9 Gift Cards, Vouchers & Wallet Payments · DI-534)*
- Partial vs full redemption is configurable per wallet/gift-card type: some allow spending part and keeping the remainder, others require full redemption in a single transaction. *(agreed · MoM 27 Aug 2026, 4.7 Split-Tender, Redemption Rules & Configuration Simulation · DI-526)*

`BO-1137` Wearable Linking & Wallet Association Rules

- The same wristband or enrolled face works as stored-value payment for F&B and retail: balance checked and deducted automatically at the point of sale; top-up via the same credential. *(client request · MoM 2 Sep 2026, 4.12 Media as a Payment Method · DI-643)*
- Each wallet gets a unique wallet code (like a ticket number) with configurable association to physical/digital media: QR code, RFID/wristband or other media types, usable across channels. *(client request · MoM 27 Aug 2026, 4.4 Wallet Numbering / 4.9 Wallet-to-media linking · DI-513)*

`BO-114` Variants, Attributes, Barcode & RFID Management

- Product master holds price, stock and variant attributes (e.g. size/colour) with a distinct barcode per variant; stock is tracked per variant/size. Decision: size/variant attributes (small/medium/large) are configurable per product type in the admin panel and appear dynamically when products are added. *(agreed · MoM 19 Aug 2026, 4.2 Product Catalog, Variant & Pricing Management; 5. Key Decisions · DI-354)*

`BO-1142` Wallet Transaction Simulator, Monitoring & Channel Audit

- Configuration simulation/test mode lets an admin run sample transactions against a wallet configuration (e.g. spend-category restrictions) before publishing, instead of discovering errors live. *(agreed · MoM 27 Aug 2026, 4.7 Configuration simulation tool · DI-528)*

`BO-1144` Peer-to-Peer Transfer Configuration

- Peer-to-peer transfer from one guest's wallet to another guest's wallet; a configurable venue-level toggle (allowed or not), not a default feature. *(agreed · MoM 27 Aug 2026, 4.10 Transfers, Fraud/Risk Controls · DI-536)*

`BO-1145` Transfer Eligibility, Limits & Approval Rules

- Peer-to-peer transfer from one guest's wallet to another guest's wallet; a configurable venue-level toggle (allowed or not), not a default feature. *(agreed · MoM 27 Aug 2026, 4.10 Transfers, Fraud/Risk Controls · DI-536)*

`BO-1146` Refund-to-Wallet Policy Configuration

- Approved refunds go back to the original payment method or are credited to the guest's wallet for future purchases. *(client request · MoM 7 Sep 2026, 4.11 Entitlements Usage, Upgrades & Refund/Credit Recovery · DI-673)*
- End-of-visit unload/refund: a guest can unload the remaining balance at a counter after a balance check. Configurable venue-level toggle, not always on. *(agreed · MoM 27 Aug 2026, 4.10 Transfers, Fraud/Risk Controls · DI-535)*
- Stored value configuration: minimum stored value, maximum top-up balance, expiry of stored balance, and refund destination (original payment method or back to wallet balance). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-468)*

`BO-1149` Administrative Balance Adjustment Studio

- Funding methods: cash, card, online, POS, kiosk self-service, plus manual admin funding used to issue a goodwill/service-recovery credit to a guest's wallet. Chinmay raised role-based permission for staff funding wallets. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-516)*

`BO-115` Category, Brand & Merchandise Hierarchy

- Category, Brand & Hierarchy supports multi-level categorisation with subcategories (e.g. Apparel > Retail > Apparel > T-Shirt). *(client request · MoM 19 Aug 2026, 4.2 Product Catalog, Variant & Pricing Management · DI-355)*
- Products are grouped into categories for the tenant website (e.g. a diving operator's scuba diving, free diving, snorkelling, each listing its packages); package title, description, terms, age limits and images come from back-office fields and sync to the live site; choosing a package goes to checkout on the TICVAI booking platform. *(agreed · MoM 7 Aug 2026, 9. Statistical Groups & Website Content Integration · DI-161)*

`BO-1155` Transaction Risk Scoring Engine

- Transactions get a risk score; high-risk transactions are flagged and routed to the operations team for manual cross-verification, never auto-approved or auto-declined. *(agreed · MoM 27 Aug 2026, 4.10 Transaction risk scoring engine · DI-537)*

`BO-116` Merchandising & Product Presentation

- Catalog Builder & Store Assortment maps which products sell on which channel (on-site, online, or restricted), managed at catalog level rather than per individual product. *(client request · MoM 19 Aug 2026, 4.2 Product Catalog, Variant & Pricing Management · DI-356)*

`BO-1160` Fraud Alert & Investigation Case Management

- Transactions get a risk score; high-risk transactions are flagged and routed to the operations team for manual cross-verification, never auto-approved or auto-declined. *(agreed · MoM 27 Aug 2026, 4.10 Transaction risk scoring engine · DI-537)*

`BO-1167` Reconciliation Exception & Resolution Workbench

- A financial approval centre / controls screen surfaces transactions with exceptions or variances needing review. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-277)*
- Weekly/monthly reconciliation runs ingest → parse → match → classify → auto-resolve, so only genuinely mismatched amounts are shown for human review. *(agreed · MoM 12 Aug 2026, 11. Settlement and Reconciliation Process · DI-258)*

`BO-117` Product Import, Governance & AI Configuration Assistant

- AI-prepared configuration keeps full version history, e.g. every price change shows who suggested it, who approved it and when it was published. *(client request · MoM 18 Sep 2026, 4.7 AI Configuration Assistant — Approval, Execution & Audit Trail · DI-938)*
- The AI configuration assistant is conversational and iterative: on "I want to create a product" it asks follow-ups (ticket type, validity, date/time) and, if required information such as capacity is missing, asks for it rather than proceeding, before showing a configuration blueprint and dependency map. *(agreed · MoM 18 Sep 2026, 4.5 AI Configuration Assistant — Conversational Requirement Gathering · DI-937)*
- AI-assisted draft: an AI wizard asks what ticket type to create and the relevant fields, then auto-configures a draft for review before approval/publish. Agreed extension (Chinmay): it also parses unstructured input (incl. OCR on images) and prompts the user for missing details. *(agreed · MoM 25 Aug 2026, 4.1 Product / Ticket Catalog Creation · DI-440)*
- Phase-one AI priority is a conversational configuration assistant: the admin says e.g. "I want to configure a new product" and it asks the product type (admission, time slot, etc.) and walks through product/promotion setup. *(agreed · MoM 14 Aug 2026, 1. AI Configuration Assistant — Phase-One Scope · DI-279)*

`BO-1171` Wallet Analytics & Management Reporting

- Wallet spend reported by department/category (F&B, attractions, retail, partners) and by channel (B2C, POS); payment/redemption policy can set rules such as a minimum spend to use the wallet as a payment method. *(client request · MoM 27 Aug 2026, 4.9 Gift Cards, Vouchers & Wallet Payments · DI-534)*

`BO-1172` Finance Validation, Reporting & Audit Center

- A financial approval centre / controls screen surfaces transactions with exceptions or variances needing review. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-277)*

`BO-1175` Integration Profile & System Mapping

- Financial year/period setup varies by country (UAE Jan–Dec, India Apr–Mar); closing a period locks further postings. An ERP integration centre manages external connections. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-263)*

`BO-1177` API Security, Access & Integration Permissions

- Production access status is shown: sandbox only, requested (pending), approved, or rejected with the reason. Production keys only after certification; the request form says a new production key is issued and the sandbox key stays sandbox. *(agreed · MoM 17 Sep 2026, M17-06 · DI-927)*
- API scopes are picked from a list grouped by module ({module}.read / {module}.write), with unlicensed modules shown disabled rather than hidden; the API reference is grouped by licensable module, then contract. *(agreed · MoM 17 Sep 2026, M17-05, M17-12 · DI-926)*

`BO-1184` Transport Routes & Stops

- **Open question.** Should each popular-route card's starting fare, featured order and image or badge be set per route in the back office? Default built: routes carry a featured order and an image; the starting fare is computed from the lowest fare. *(open · Decisions Register 1 Oct 2026, Questions for the client — Transport / Popular routes card · DI-1119)*

`BO-119` Cross-Sell, Upsell & Recommendation Rules

- Recommendation analytics show response rates, drop-offs, successful purchases and conversion per recommendation, broken down by strategy type (AI-based vs rule-based). *(client request · MoM 21 Sep 2026, 4.7 Recommendation Performance Analytics · DI-963)*
- Recommendation touchpoints are configurable (cart, checkout or post-purchase, per channel), and a presentation/experience preview visually simulates how a recommendation will look to the guest before it is published. *(client request · MoM 21 Sep 2026, 4.6 Personalized Offer Delivery & Omni-Channel Orchestration · DI-961)*
- What a guest is offered depends on context: a member is not offered another membership (F&B or retail add-ons instead); general admission is not offered once VIP/fast pass is selected; an expiring membership prompts a renewal rather than a new product; similar offers are not shown back-to-back (alternate F&B and experience upsells). *(client request · MoM 21 Sep 2026, 4.2 / 4.3 / 4.5 Recommendation Strategy and Decisioning · DI-960)*
- Recommendations stay within business limits, e.g. at most three recommendations shown at checkout and never a product the customer already owns; AI recommendations never override hard business rules or eligibility constraints. *(agreed · MoM 21 Sep 2026, 4.3 Recommendation Strategy — Business Priority, Conflict Suppression & Fallback · DI-959)*

`BO-1190` Donation Campaigns

- **Open question.** Open: whether donations are taxable. Allam believes they are typically not, but the system should allow enabling/disabling a tax or service fee on donations; Chinmay to confirm treatment. *(open · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies; 6. Open Items · DI-472)*
- Donation campaigns: fixed or variable amounts, enabled per sales channel, triggered on a specific product or across all products, proceeds tracked to a separate account code. *(client request · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies · DI-471)*

`BO-120` Omnichannel Commerce & Journey Configuration

- Recommendation touchpoints are configurable (cart, checkout or post-purchase, per channel), and a presentation/experience preview visually simulates how a recommendation will look to the guest before it is published. *(client request · MoM 21 Sep 2026, 4.6 Personalized Offer Delivery & Omni-Channel Orchestration · DI-961)*

`BO-121` Personalized Offers & Guest Engagement

- Recommendation analytics show response rates, drop-offs, successful purchases and conversion per recommendation, broken down by strategy type (AI-based vs rule-based). *(client request · MoM 21 Sep 2026, 4.7 Recommendation Performance Analytics · DI-963)*

`BO-123` POS Profile Management

- Terminal settings as business-optional toggles: printer, offline continuity, screen prompts, guest-facing display, key sounds, training mode. *(client request · MoM 9 Sep 2026, 4.17 POS Prototype Review - Reports, Settings, Peripherals & Role-Based Access · DI-800)*
- POS profile & layout: link each department to its workstation types and counts; a distinct drag-and-drop product/category layout per workstation type (ticketing, F&B, retail, kiosk); sales rules limiting what a workstation sells (e.g. admission-only vs membership-only). *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-310)*
- Each workstation is linked to a front-end "sales board" (e.g. of ten: five ticketing, three F&B, two retail); signing in on it opens the matching front end automatically. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-247)*

`BO-124` Layout & Journey Builder

- POS profile & layout: link each department to its workstation types and counts; a distinct drag-and-drop product/category layout per workstation type (ticketing, F&B, retail, kiosk); sales rules limiting what a workstation sells (e.g. admission-only vs membership-only). *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-310)*
- Drag-and-drop POS "sales board" designer placing products and system functions (ticket list, reservation list, transaction list, media lookup) as buttons with custom fonts and colours. Allam: the old interface is NOT a design reference — functional concept only. *(agreed · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-157)*

`BO-125` Product & Category Button Configuration

- Menu Builder defines the front-end POS layout per outlet — categories, item tiles (image, name, price) and configurable button sizes for fast-selling items. Agreed the current (reference) layout is a reference only and the UI/UX can be improved. *(agreed · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-326)*
- POS profile & layout: link each department to its workstation types and counts; a distinct drag-and-drop product/category layout per workstation type (ticketing, F&B, retail, kiosk); sales rules limiting what a workstation sells (e.g. admission-only vs membership-only). *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-310)*
- Drag-and-drop POS "sales board" designer placing products and system functions (ticket list, reservation list, transaction list, media lookup) as buttons with custom fonts and colours. Allam: the old interface is NOT a design reference — functional concept only. *(agreed · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-157)*

`BO-128` Live Workstation Health Monitor

- Performance monitoring shows successful vs failed validations and scan response time; configurable alert rules (e.g. low battery, device offline) with escalation for unresolved alerts. *(client request · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-901)*
- **Open question.** Open: can health metrics such as handheld battery be read via the manufacturer's SDK in-app rather than by physical inspection? Depends on each vendor SDK; to confirm during integration. *(open · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-900)*
- One screen shows live online/offline status of every workstation and device (printers, turnstiles, handheld scanners); a 360 health view shows connectivity, CPU/memory, storage and temperature. *(client request · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-899)*
- Workstation health is shown as a percentage score a manager can sort by, not only a last-heartbeat timestamp. *(agreed · client-design-boards-audit 20 Aug 2026, Genuine functional gaps - workstation health score · DI-403)*
- Workstation details: six tabs, a health score, a current-operator card with role and shift, IP address, configuration profile with version and deployment date, and a today's summary (transactions, refunds, cash collected). *(agreed · client-design-boards-audit 20 Aug 2026, What the boards give us - 1C Workstation Details · DI-401)*
- Offline policies and a venue-level Operations Summary dashboard aggregating department-level views into one venue overview. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-311)*
- **Open question.** Live workstation monitor with department-level health; proposed graphical park-map view of workstation locations and live status, depending on venue zone metadata, with manual drag-and-drop placement as fallback. *(open · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-304)*
- Hardware & peripheral management per workstation (receipt printer, cash drawer, payment terminal, barcode/ticket scanner, ticket printer) with device-level status. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-303)*
- Workstation overview dashboard: all workstations for a venue (or across venues), grouped by department and sub-department, with online/offline/health status and type (mobile POS, kiosk, on-site POS). *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-301)*

`BO-129` Software, Configuration & Version Management

- Firmware: package library per device; compatibility rules limit deployment to compatible models; update wizard with phased/scheduled rollout; live monitor flags failures (e.g. device offline at deployment); rollback and update history. *(client request · MoM 15 Sep 2026, 4.7 Firmware & Software Management · DI-903)*
- Remote configuration deploys a device type's settings (e.g. receipt printers) to many workstations in one action; configuration versions can be compared and rolled back. *(client request · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-898)*
- Versioned configuration profiles with deployments: board 1F shows 1,248 workstations across four configuration versions. *(agreed · client-design-boards-audit 20 Aug 2026, Genuine functional gaps - 1F · DI-404)*
- Software configuration tracks software version and pending/completed updates per workstation. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-305)*

`BO-130` Offline Policy & Rules Configuration

- POS offline policy configuration (board 5B) and connectivity auto-switch with a threshold (board 5D): how quickly a device flips to offline is a venue setting. *(agreed · client-design-boards-audit 20 Aug 2026, Genuine functional gaps - 5B / 5D · DI-405)*
- Offline policies and a venue-level Operations Summary dashboard aggregating department-level views into one venue overview. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-311)*
- Offline mode switches on automatically when connectivity is lost; each offline-capable node sells from a pre-allocated quota (e.g. 100 tickets per node) that is reallocated after reconnect and sync. *(agreed · MoM 5 Aug 2026, 8. Offline Selling Rules · DI-142)*

`BO-131` Connectivity & Auto-Switch Settings

- POS offline policy configuration (board 5B) and connectivity auto-switch with a threshold (board 5D): how quickly a device flips to offline is a venue setting. *(agreed · client-design-boards-audit 20 Aug 2026, Genuine functional gaps - 5B / 5D · DI-405)*
- Qossai: for seated/zoned venues, POS terminals on the same network share real-time seat state; a disconnected network needs its own offline zone. Whether zoning is automatic or client-enabled is a per-venue setting. *(client request · MoM 5 Aug 2026, 8. Offline Selling Rules · DI-143)*
- Offline mode switches on automatically when connectivity is lost; each offline-capable node sells from a pre-allocated quota (e.g. 100 tickets per node) that is reallocated after reconnect and sync. *(agreed · MoM 5 Aug 2026, 8. Offline Selling Rules · DI-142)*

`BO-132` Offline Transaction Monitor & Sync Queue

- Offline mode switches on automatically when connectivity is lost; each offline-capable node sells from a pre-allocated quota (e.g. 100 tickets per node) that is reallocated after reconnect and sync. *(agreed · MoM 5 Aug 2026, 8. Offline Selling Rules · DI-142)*
- After reconnection, offline records sync in batches in the order events occurred, tagged with both the original recorded time and the sync time; syncing must not slow gate entry. *(agreed · MoM 31 Jul 2026, 7. Ticket Validation & Offline Architecture · DI-065)*

`BO-134` Kitchen & Preparation Stations

- Kitchens are divided into stations (grill, fryer, beverage, dessert, etc.), each mapped to specific printers or KDS devices. Routing rules decide where an item prints/displays by category or item, with a fallback station/device if the primary one is offline or faulty. *(client request · MoM 18 Aug 2026, 4.3 Kitchen & Preparation Stations · DI-323)*

`BO-135` Order Routing & KDS/Printer Rules

- Kitchens are divided into stations (grill, fryer, beverage, dessert, etc.), each mapped to specific printers or KDS devices. Routing rules decide where an item prints/displays by category or item, with a fallback station/device if the primary one is offline or faulty. *(client request · MoM 18 Aug 2026, 4.3 Kitchen & Preparation Stations · DI-323)*

`BO-136` F&B Global Settings & Controls

- F&B Controls configure approval workflows globally (e.g. void approval, refund approval) based on amount thresholds and user privileges. *(client request · MoM 18 Aug 2026, 4.3 Kitchen & Preparation Stations · DI-324)*

`BO-137` Recipe Consumption & Theoretical Inventory

- F&B Stock Command Center shows stock value, low-stock/critical/out-of-stock items and recipe-based ingredient consumption. *(client request · MoM 18 Aug 2026, 4.10 F&B Stock, Wastage & Requisitions · DI-340)*

`BO-138` Production Execution & Batch Management

- Production execution & batch management shows planned vs. actual vs. yield quantity and batch losses; wastage/spoilage must be recorded per item. Outlets raise requisitions to replenish from the central warehouse. *(client request · MoM 18 Aug 2026, 4.10 F&B Stock, Wastage & Requisitions · DI-341)*

`BO-139` Wastage, Spoilage, Returns & Write-Off

- Production execution & batch management shows planned vs. actual vs. yield quantity and batch losses; wastage/spoilage must be recorded per item. Outlets raise requisitions to replenish from the central warehouse. *(client request · MoM 18 Aug 2026, 4.10 F&B Stock, Wastage & Requisitions · DI-341)*

`BO-142` Store Rules, Controls & Permissions

- Components/attributes model: a component (e.g. "ticket type") has attributes (adult, youth, senior, infant, child) each priced independently; adding an attribute creates a new sellable variant with no extra setup. Who may sell a product is restricted by site, operating area, workstation or role. *(agreed · MoM 7 Aug 2026, 12. Products Configuration: Metric Sheets, Pricing & Components · DI-164)*

`BO-143` Retail Global Settings & Controls

- Online retail offers buy-online-pickup-in-store and buy-online-ship-to-address. Shipping fees are set by region/city (e.g. Dubai, Abu Dhabi, international); decision: operations enter courier rates and margins manually, no live courier-API integration at this stage. *(agreed · MoM 19 Aug 2026, 4.3 Pricing, Bundles & Promotions; 4.8 Online Order Fulfilment & Shipping Configuration · DI-359)*
- Retail POS/device assignment covers workstation name/code, receipt printer, barcode scanner and cash drawer; global retail settings include sales channels, primary/replenishment store and offline sales support. *(client request · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-352)*

`BO-144` Access Control Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Venue-wide attendance overview (open/closed gates, offline/maintenance status, graphed) and a visual map of all access-control locations across venues/tenants, including entry and exit turnstile layouts that vary by venue. *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-623)*

`BO-148` Access Point Directory

- Gate & zone management shows gates per location (e.g. three at a main entry plaza, two at a main entry zone); device inventory lists turnstiles and handhelds assignable per gate; a device is added by choosing an integrated turnstile model and entering connection details (IP address). *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-624)*
- Tiered access (e.g. Bronze/Silver/Gold): the client fills a matrix of which gates/attractions each tier may scan into; configured as location → admission profile → gate → access point, with explicit deny rules (e.g. Gold denied at the Silver/Bronze entrance). *(agreed · MoM 7 Aug 2026, 24. Tiered Ticketing & Access Control Deep Dive · DI-185)*

`BO-149` Gate & Lane Configuration

- Gate & zone management shows gates per location (e.g. three at a main entry plaza, two at a main entry zone); device inventory lists turnstiles and handhelds assignable per gate; a device is added by choosing an integrated turnstile model and entering connection details (IP address). *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-624)*

`BO-150` Access Control Graphical Map Designer

- Venue-wide attendance overview (open/closed gates, offline/maintenance status, graphed) and a visual map of all access-control locations across venues/tenants, including entry and exit turnstile layouts that vary by venue. *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-623)*

`BO-152` Operating Calendar & Special Access Days

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Validity date range plus blockout dates (e.g. public holidays, special event days); entry allowance consumption blocks use once exhausted; multi-park crossover (how many parks, same-day or one per day, consecutive or flexible days); companion rules (child ticket needs a qualifying adult). *(client request · MoM 2 Sep 2026, 4.3 / 4.4 Validity, Crossover & Companion Rules · DI-628)*

`BO-154` Access Rule Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Access rules dashboard shows active rules, drafts and status. Rules: one entry per day vs unlimited or limited re-entry; exit scan required or exit in free rotation; turnstile modes (free rotation, entry, exit); anti-passback window with exit-before-re-entry option. *(client request · MoM 2 Sep 2026, 4.3 Access Rules - Entry/Exit, Anti-Passback & Validity · DI-626)*

`BO-155` Visual Access Rule Builder

- Tiered access (e.g. Bronze/Silver/Gold): the client fills a matrix of which gates/attractions each tier may scan into; configured as location → admission profile → gate → access point, with explicit deny rules (e.g. Gold denied at the Silver/Bronze entrance). *(agreed · MoM 7 Aug 2026, 24. Tiered Ticketing & Access Control Deep Dive · DI-185)*

`BO-156` Entry, Exit & Re-entry Rules

- Access rules dashboard shows active rules, drafts and status. Rules: one entry per day vs unlimited or limited re-entry; exit scan required or exit in free rotation; turnstile modes (free rotation, entry, exit); anti-passback window with exit-before-re-entry option. *(client request · MoM 2 Sep 2026, 4.3 Access Rules - Entry/Exit, Anti-Passback & Validity · DI-626)*
- If a guest exits without a matching checkout scan (e.g. a manually opened door), the system flags it and blocks the next re-entry scan until check-in/check-out is reconciled. *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-461)*

`BO-157` Anti-Passback & Journey Sequence

- Access rules dashboard shows active rules, drafts and status. Rules: one entry per day vs unlimited or limited re-entry; exit scan required or exit in free rotation; turnstile modes (free rotation, entry, exit); anti-passback window with exit-before-re-entry option. *(client request · MoM 2 Sep 2026, 4.3 Access Rules - Entry/Exit, Anti-Passback & Validity · DI-626)*

`BO-158` Access Validity & Time Rules

- Validity date range plus blockout dates (e.g. public holidays, special event days); entry allowance consumption blocks use once exhausted; multi-park crossover (how many parks, same-day or one per day, consecutive or flexible days); companion rules (child ticket needs a qualifying adult). *(client request · MoM 2 Sep 2026, 4.3 / 4.4 Validity, Crossover & Companion Rules · DI-628)*
- Entitlements go beyond admission — e.g. a combo of park admission + an F&B item + a retail item, each redeemed by QR scan at its counter. Admission entitlements cap entries per ticket (e.g. max 2); product entitlements give a time-bound window (e.g. 60 minutes from first scan). *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-458)*
- Supporting configuration: ticket variants (adult/child/senior/VIP, configurable), waitlist, on-sale/off-sale timing and cut-offs, entitlement/access rules (single/multi-venue, entries, zones, early entry), fulfilment channels (email, WhatsApp, SMS), after-sales windows (upgrade, reschedule, cancel), dynamic/fixed pricing and promotions. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-437)*
- Entitlement settings: re-entry not allowed / once per day / unlimited; expiry end of week, month, year, variable date, from first use, or by performance date/time; group tickets by fixed price or fixed quantity; one ticket may link to several events. *(agreed · MoM 7 Aug 2026, 16. Entitlement Components: Re-entry, Expiration & Sale Restrictions · DI-171)*

`BO-159` Entitlement Consumption Engine

- Validity date range plus blockout dates (e.g. public holidays, special event days); entry allowance consumption blocks use once exhausted; multi-park crossover (how many parks, same-day or one per day, consecutive or flexible days); companion rules (child ticket needs a qualifying adult). *(client request · MoM 2 Sep 2026, 4.3 / 4.4 Validity, Crossover & Companion Rules · DI-628)*
- Entitlements go beyond admission — e.g. a combo of park admission + an F&B item + a retail item, each redeemed by QR scan at its counter. Admission entitlements cap entries per ticket (e.g. max 2); product entitlements give a time-bound window (e.g. 60 minutes from first scan). *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-458)*
- Entitlement settings: re-entry not allowed / once per day / unlimited; expiry end of week, month, year, variable date, from first use, or by performance date/time; group tickets by fixed price or fixed quantity; one ticket may link to several events. *(agreed · MoM 7 Aug 2026, 16. Entitlement Components: Re-entry, Expiration & Sale Restrictions · DI-171)*

`BO-160` Multi-Park & Crossover Rules

- Validity date range plus blockout dates (e.g. public holidays, special event days); entry allowance consumption blocks use once exhausted; multi-park crossover (how many parks, same-day or one per day, consecutive or flexible days); companion rules (child ticket needs a qualifying adult). *(client request · MoM 2 Sep 2026, 4.3 / 4.4 Validity, Crossover & Companion Rules · DI-628)*

`BO-161` Guest, Companion & Eligibility Rules

- Validity date range plus blockout dates (e.g. public holidays, special event days); entry allowance consumption blocks use once exhausted; multi-park crossover (how many parks, same-day or one per day, consecutive or flexible days); companion rules (child ticket needs a qualifying adult). *(client request · MoM 2 Sep 2026, 4.3 / 4.4 Validity, Crossover & Companion Rules · DI-628)*

`BO-162` Group Admission & Quantity Validation

- Group ticket QR options: one QR valid for a defined headcount, individual QR per member, or a single rotating/multi-use QR scanned until the headcount is exhausted. *(client request · MoM 31 Aug 2026, 4.8 Group Operations, Payment Links & Check-In · DI-569)*

`BO-163` Rule Simulation, Conflict Check & Publication

- Simulation tool validates a rule (e.g. ticket allowed in Zone A and B, not C or D) via a virtual scan before publishing, without a real transaction. *(client request · MoM 2 Sep 2026, 4.5 Rule Simulation Tool · DI-629)*

`BO-164` Digital Credential Security Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`BO-165` Dynamic QR Security Profile Builder

- Dynamic QR is chosen per event (fully dynamic, normal, or mixed); a per-product override disables it for exceptions such as physically delivered VIP invitations and B2B/reseller tickets, which fall back to standard QR or RFID. *(agreed · MoM 2 Sep 2026, 4.7 Dynamic QR Code - Business Flexibility & Exceptions · DI-633)*
- **Open question.** Dynamic QR refreshes periodically to cut fraud/resale. Open: beacon-based (code hidden until the phone is near a gate beacon via Bluetooth, then refreshes ~every 2 minutes; Qossai: more secure) vs app-generated; GPS geofencing also raised. Chinmay to propose. *(open · MoM 2 Sep 2026, 4.6 Dynamic QR Code - Concept & Generation Approach · DI-630)*

`BO-166` Credential Activation & Display Rules

- Dynamic QR is chosen per event (fully dynamic, normal, or mixed); a per-product override disables it for exceptions such as physically delivered VIP invitations and B2B/reseller tickets, which fall back to standard QR or RFID. *(agreed · MoM 2 Sep 2026, 4.7 Dynamic QR Code - Business Flexibility & Exceptions · DI-633)*
- The dynamic QR stays blurred until beacon proximity is detected, then activates and refreshes on a short interval (e.g. every 6-12 seconds); screenshot capture of the active code is prevented. *(client request · MoM 2 Sep 2026, 4.6 Credential activation and display rules · DI-632)*

`BO-167` Device Binding & Session Security

- Once activated in the app a digital ticket is bound to one approved device; moving to a new device requires deactivating the prior binding. Credential transfer moves a ticket to another person's device and invalidates the original holder's copy. *(client request · MoM 2 Sep 2026, 4.8 Device Binding, Credential Transfer & Revocation · DI-636)*

`BO-168` BLE Beacon & Geofence Configuration

- **Open question.** Dynamic QR refreshes periodically to cut fraud/resale. Open: beacon-based (code hidden until the phone is near a gate beacon via Bluetooth, then refreshes ~every 2 minutes; Qossai: more secure) vs app-generated; GPS geofencing also raised. Chinmay to propose. *(open · MoM 2 Sep 2026, 4.6 Dynamic QR Code - Concept & Generation Approach · DI-630)*

`BO-169` Credential Transfer & Rebinding

- Once activated in the app a digital ticket is bound to one approved device; moving to a new device requires deactivating the prior binding. Credential transfer moves a ticket to another person's device and invalidates the original holder's copy. *(client request · MoM 2 Sep 2026, 4.8 Device Binding, Credential Transfer & Revocation · DI-636)*

`BO-171` Offline Cryptographic Validation Profile

- Qossai: the dynamic QR must appear and work without internet, since crowded events (10,000+) suffer severe congestion; it must work offline via Bluetooth/beacon or an equivalent local mechanism. *(agreed · MoM 2 Sep 2026, 4.6 Hard requirement (offline) · DI-631)*

`BO-174` Media & Credential Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`BO-179` Media Swap & Replacement

- Media swap: zero-value transaction converting a ticket's media on-site, e.g. scanning an online QR at a kiosk to issue a physical wristband instead. *(client request · MoM 2 Sep 2026, 4.9 Media swap · DI-637)*

`BO-182` Hotel, Wallet & External Media Integration

- Affiliated-hotel guests get a zero-value ticket/wristband after room-number lookup and identity verification, or charge on-site purchases to their room via the same lookup (PMS such as Opera). *(client request · MoM 2 Sep 2026, 4.9 Hotel/PMS integration · DI-638)*

`BO-183` Media Compatibility, Testing & Publication

- Media compatibility testing validates that each supported media type works at each gate/device before go-live. *(client request · MoM 2 Sep 2026, 4.9 Media & Credential Configuration · DI-639)*

`BO-184` Biometric Access Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`BO-186` Face Pass Enrollment Configuration

- Two face credentials: Face Pass (long-term, renewable, for memberships/season passes) and Face Tag (short-lived, single day or event). Retention is venue-configurable per tier. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-640)*

`BO-187` Biometric Consent & Guardian Management

- Qossai: use an existing major venue-group client's live app and published privacy policy as the model for how facial-recognition consent, data use and retention are explained to guests. *(client request · MoM 2 Sep 2026, 4.11 Privacy & Biometric Data Retention · DI-642)*

`BO-188` Face Tag Temporary Enrollment

- Two face credentials: Face Pass (long-term, renewable, for memberships/season passes) and Face Tag (short-lived, single day or event). Retention is venue-configurable per tier. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-640)*

`BO-190` Face Change, Re-enrollment & Identity Protection

- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*

`BO-191` Biometric Validation at Gate

- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*

`BO-192` Biometric Lifecycle, Retention & Deletion

- Two face credentials: Face Pass (long-term, renewable, for memberships/season passes) and Face Tag (short-lived, single day or event). Retention is venue-configurable per tier. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-640)*

`BO-194` Device & Gate Command Center

- Device incidents get automatic severity (e.g. main-entrance controller outage = critical); adding a device goes through an approval workflow; webhooks notify external systems when a critical device goes offline. *(client request · MoM 15 Sep 2026, 4.9 Device Integration & Operation Analytics · DI-906)*
- Device analytics: total/active/inactive devices across venues (multi-tenant) with location breakdown; health, availability, fault rate and top failure reasons (communication timeout, device offline, invalid response, power issue, firmware error); SLA tracking for devices in extended maintenance. *(client request · MoM 15 Sep 2026, 4.9 Device Integration & Operation Analytics · DI-905)*
- One screen shows live online/offline status of every workstation and device (printers, turnstiles, handheld scanners); a 360 health view shows connectivity, CPU/memory, storage and temperature. *(client request · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-899)*
- Inventory counts by status (assigned, under maintenance, in stock) - e.g. 15 receipt printers broken down by ticketing, retail, F&B and in store. *(client request · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-894)*
- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Real-time health view of device connectivity. Device-pushed events (anti-passback attempts, power loss, network loss) are surfaced as alerts and reports, e.g. notifying the operations team when a turnstile goes offline. *(agreed · MoM 2 Sep 2026, 4.1 / 4.2 Health Monitoring & Alerts · DI-625)*

`BO-195` Device Type & Hardware Library

- No driver is ever installed on the workstation OS: drivers are built into the TICVAI app; staff only connect the device and test print/scan from within the app; new models are supported by a back-end driver update, not a code release. *(agreed · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-897)*
- Configuration template library: a template per model (e.g. a specific Epson receipt printer) auto-attaches the right drivers when a device of that type is added. Template attribute list pending from Allam. *(client request · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-896)*
- Gate & zone management shows gates per location (e.g. three at a main entry plaza, two at a main entry zone); device inventory lists turnstiles and handhelds assignable per gate; a device is added by choosing an integrated turnstile model and entering connection details (IP address). *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-624)*

`BO-196` Physical Device Registration & Provisioning

- Device incidents get automatic severity (e.g. main-entrance controller outage = critical); adding a device goes through an approval workflow; webhooks notify external systems when a critical device goes offline. *(client request · MoM 15 Sep 2026, 4.9 Device Integration & Operation Analytics · DI-906)*
- Asset record: purchase date, warranty status/expiry, supplier, serial, manufacturer; ownership and responsibility shown separately (venue owns, operations responsible); a visual map shows installation location. *(client request · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-895)*
- 360 device view shows status and workstation; reassign to another workstation or deactivate with a logged reason; lifecycle view tracks registration -> enrolment -> assignment -> reassignment. *(client request · MoM 15 Sep 2026, 4.3 Device Management - Registration, Enrollment & Workstation Assignment · DI-893)*
- Device directory: search and add devices (printers, scanners, customer displays, cash drawers, turnstiles, handhelds, mobile POS) capturing serial number, type and model; adding generates a secure enrolment code; devices are assigned to workstations (e.g. A has ticket printer, receipt printer and cash drawer). *(client request · MoM 15 Sep 2026, 4.3 Device Management - Registration, Enrollment & Workstation Assignment · DI-892)*
- Gate & zone management shows gates per location (e.g. three at a main entry plaza, two at a main entry zone); device inventory lists turnstiles and handhelds assignable per gate; a device is added by choosing an integrated turnstile model and entering connection details (IP address). *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-624)*

`BO-197` Turnstile & Lane Behavior Configuration

- Turnstile light/sound feedback is configurable: e.g. green light for an adult ticket, orange for a child ticket as a quick visual fraud check; some models play audio, including celebratory sounds (e.g. birthday visit). *(client request · MoM 2 Sep 2026, 4.13 Turnstile Hardware & Handheld Scanner Configuration · DI-644)*
- Access rules dashboard shows active rules, drafts and status. Rules: one entry per day vs unlimited or limited re-entry; exit scan required or exit in free rotation; turnstile modes (free rotation, entry, exit); anti-passback window with exit-before-re-entry option. *(client request · MoM 2 Sep 2026, 4.3 Access Rules - Entry/Exit, Anti-Passback & Validity · DI-626)*

`BO-198` Validation Outcome & Guest Feedback Designer

- A custom welcome message and the venue's branding/logo show on the reader on a successful scan. *(client request · MoM 2 Sep 2026, 4.13 Turnstile Hardware & Handheld Scanner Configuration · DI-645)*
- Turnstile light/sound feedback is configurable: e.g. green light for an adult ticket, orange for a child ticket as a quick visual fraud check; some models play audio, including celebratory sounds (e.g. birthday visit). *(client request · MoM 2 Sep 2026, 4.13 Turnstile Hardware & Handheld Scanner Configuration · DI-644)*

`BO-199` Reader, Scanner & Peripheral Configuration

- No driver is ever installed on the workstation OS: drivers are built into the TICVAI app; staff only connect the device and test print/scan from within the app; new models are supported by a back-end driver update, not a code release. *(agreed · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-897)*

`BO-200` Handheld & Mobile Access Device Configuration

- Handheld scanners read QR, RFID or other supported media. Offline, devices validate locally from data embedded in the credential, queue the transactions and auto-sync when connectivity returns. *(agreed · MoM 2 Sep 2026, 4.13 / 4.14 Handheld Scanners & Offline Mode · DI-646)*

`BO-201` Gate Modes, Free Spin & Emergency Controls

- Access rules dashboard shows active rules, drafts and status. Rules: one entry per day vs unlimited or limited re-entry; exit scan required or exit in free rotation; turnstile modes (free rotation, entry, exit); anti-passback window with exit-before-re-entry option. *(client request · MoM 2 Sep 2026, 4.3 Access Rules - Entry/Exit, Anti-Passback & Validity · DI-626)*

`BO-202` Device Software, Content & Remote Configuration

- Firmware: package library per device; compatibility rules limit deployment to compatible models; update wizard with phased/scheduled rollout; live monitor flags failures (e.g. device offline at deployment); rollback and update history. *(client request · MoM 15 Sep 2026, 4.7 Firmware & Software Management · DI-903)*
- Remote configuration deploys a device type's settings (e.g. receipt printers) to many workstations in one action; configuration versions can be compared and rolled back. *(client request · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-898)*
- No driver is ever installed on the workstation OS: drivers are built into the TICVAI app; staff only connect the device and test print/scan from within the app; new models are supported by a back-end driver update, not a code release. *(agreed · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-897)*
- A custom welcome message and the venue's branding/logo show on the reader on a successful scan. *(client request · MoM 2 Sep 2026, 4.13 Turnstile Hardware & Handheld Scanner Configuration · DI-645)*

`BO-203` Hardware Compatibility, Health, Testing & Deployment

- Device analytics: total/active/inactive devices across venues (multi-tenant) with location breakdown; health, availability, fault rate and top failure reasons (communication timeout, device offline, invalid response, power issue, firmware error); SLA tracking for devices in extended maintenance. *(client request · MoM 15 Sep 2026, 4.9 Device Integration & Operation Analytics · DI-905)*
- **Open question.** Open (Allam): physical tamper detection - lock out communication if a device is opened, as bank payment terminals do - worth evaluating per device type; not a requirement for every device. *(open · MoM 15 Sep 2026, 4.8 Device Security & Governance · DI-904)*
- Device maintenance: preventive cycles (quarterly, half-yearly, seasonal) on a calendar by device type; staff log faulty devices which raise work orders; diagnostic workspace for the engineer; warranty and maintenance history; return to service. *(client request · MoM 15 Sep 2026, 4.6 Device Maintenance & Lifecycle Servicing · DI-902)*
- Performance monitoring shows successful vs failed validations and scan response time; configurable alert rules (e.g. low battery, device offline) with escalation for unresolved alerts. *(client request · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-901)*
- **Open question.** Open: can health metrics such as handheld battery be read via the manufacturer's SDK in-app rather than by physical inspection? Depends on each vendor SDK; to confirm during integration. *(open · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-900)*
- One screen shows live online/offline status of every workstation and device (printers, turnstiles, handheld scanners); a 360 health view shows connectivity, CPU/memory, storage and temperature. *(client request · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-899)*
- Media compatibility testing validates that each supported media type works at each gate/device before go-live. *(client request · MoM 2 Sep 2026, 4.9 Media & Credential Configuration · DI-639)*
- Real-time health view of device connectivity. Device-pushed events (anti-passback attempts, power loss, network loss) are surfaced as alerts and reports, e.g. notifying the operations team when a turnstile goes offline. *(agreed · MoM 2 Sep 2026, 4.1 / 4.2 Health Monitoring & Alerts · DI-625)*

`BO-204` Offline & Edge Operations Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`BO-211` Reconnection, Synchronization & Conflict Resolution

- Handheld scanners read QR, RFID or other supported media. Offline, devices validate locally from data embedded in the credential, queue the transactions and auto-sync when connectivity returns. *(agreed · MoM 2 Sep 2026, 4.13 / 4.14 Handheld Scanners & Offline Mode · DI-646)*

`BO-214` Guest Journey Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`BO-215` Group & B2B Admission Profile Builder

- Group/B2B admission profile view shows entry statistics by category (general admission, group, re-entry, crossover) and attendance breakdowns for schools and other groups from scanned tickets. *(client request · MoM 2 Sep 2026, 4.15 Guest Journey, Group/B2B Profiles & Live Operations Dashboard · DI-647)*

`BO-217` Group Attendance & Partial Entry Manager

- Group/B2B admission profile view shows entry statistics by category (general admission, group, re-entry, crossover) and attendance breakdowns for schools and other groups from scanned tickets. *(client request · MoM 2 Sep 2026, 4.15 Guest Journey, Group/B2B Profiles & Live Operations Dashboard · DI-647)*
- Group tickets can carry one shared QR code or individual QR codes, with partial check-in tracking; family tickets bundle adult/child pricing. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-137)*

`BO-221` Fast Pass & Attraction Access Journey

- Qossai: walk-in, virtual-queue and VIP guests must be distinguished at the ride; VQ guests are never merged into the VIP line (would erode paid value); VQ arrivals need their own handling, e.g. a separate line or a QR scan within the arrival window. *(agreed · MoM 7 Sep 2026, 4.15 Virtual Queue - Three-Tier Guest Model · DI-678)*

`BO-224` Live Access Operations Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Live operations dashboard: real-time attendance by venue and gate with each gate's online/offline status and entry count. Turnstile mode can be switched through the day (more entry gates in the morning, more exit in the evening). *(client request · MoM 2 Sep 2026, 4.15 Live Operations Dashboard · DI-648)*
- Real-time health view of device connectivity. Device-pushed events (anti-passback attempts, power loss, network loss) are surfaced as alerts and reports, e.g. notifying the operations team when a turnstile goes offline. *(agreed · MoM 2 Sep 2026, 4.1 / 4.2 Health Monitoring & Alerts · DI-625)*

`BO-226` Ticket & Credential Investigation Console

- Ticket lookup shows the complete scan history: purchaser, gate and timestamp for every attempt. Security can manually override to admit a guest despite a scan issue; every override is logged against the visitor's record. *(client request · MoM 2 Sep 2026, 4.16 Ticket Lookup & Manual Override · DI-649)*
- A successful scan marks the ticket used even if the guest did not pass (stroller, turnstile re-locked). Genuine cases are resolved manually by security from the ticket's scan-history log, so scanner lookup must show it. *(agreed · MoM 2 Sep 2026, 4.3 Decision (scan without physical passage) · DI-627)*
- Ticket look-up shows the ticket's full consumption history: transaction date/time, number of scans, expiry, and (if applicable) wallet balance and F&B/retail spend against that ticket. *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-462)*

`BO-228` Manual Override & Supervisor Approval

- Ticket lookup shows the complete scan history: purchaser, gate and timestamp for every attempt. Security can manually override to admit a guest despite a scan issue; every override is logged against the visitor's record. *(client request · MoM 2 Sep 2026, 4.16 Ticket Lookup & Manual Override · DI-649)*

`BO-230` Live Gate Mode & Lane Control

- Live operations dashboard: real-time attendance by venue and gate with each gate's online/offline status and entry count. Turnstile mode can be switched through the day (more entry gates in the morning, more exit in the evening). *(client request · MoM 2 Sep 2026, 4.15 Live Operations Dashboard · DI-648)*

`BO-231` Queue, Throughput & Lane Optimization

- Per-ride hourly capacity (e.g. 600/hour) split across express/fast-lane, virtual queue and walk-in (illustrative 75% general split walk-in/VQ, 25%/150 express); allocation adjusts dynamically if one lane is disproportionately busy. *(client request · MoM 7 Sep 2026, 4.12 Virtual Queue - Concept & Lane/Allocation Model · DI-674)*

`BO-234` Dynamic Access Policy Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`BO-237` Context, Time, Event & Capacity Policy Builder

- Access decisions consider who, ticket type, where, when and context; e.g. an otherwise valid unused ticket is denied once the venue's maximum live occupancy is reached, until guests exit. Scanners need a venue-full denial state. *(agreed · MoM 2 Sep 2026, 4.16 Attribute-Based Access Control · DI-650)*

`BO-244` Access Security & Fraud Command Center

- Fraud monitoring shows a composite risk score per customer built from several signals: attempts and success/failure ratio (e.g. 10 attempts, 3 successes), distinct cards under one identity, refund volume or value, device/login anomalies, and repeated attempts to use an expired ticket at access control. *(agreed · MoM 21 Sep 2026, 4.12 / 4.13 AI Risk & Fraud Intelligence · DI-969)*
- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Fraud assessment view flags suspicious usage patterns or threats; live monitoring shows current attendance, in-park counts and entry/exit/crossover activity per venue in real time. *(client request · MoM 2 Sep 2026, 4.16 Fraud Detection & Live Monitoring · DI-651)*

`BO-245` Fraud Detection Rule & Signal Library

- Fraud monitoring shows a composite risk score per customer built from several signals: attempts and success/failure ratio (e.g. 10 attempts, 3 successes), distinct cards under one identity, refund volume or value, device/login anomalies, and repeated attempts to use an expired ticket at access control. *(agreed · MoM 21 Sep 2026, 4.12 / 4.13 AI Risk & Fraud Intelligence · DI-969)*

`BO-250` Access Risk Scoring & Decision Engine

- Fraud monitoring shows a composite risk score per customer built from several signals: attempts and success/failure ratio (e.g. 10 attempts, 3 successes), distinct cards under one identity, refund volume or value, device/login anomalies, and repeated attempts to use an expired ticket at access control. *(agreed · MoM 21 Sep 2026, 4.12 / 4.13 AI Risk & Fraud Intelligence · DI-969)*

`BO-254` Access Monitoring & Analytics Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Fraud assessment view flags suspicious usage patterns or threats; live monitoring shows current attendance, in-park counts and entry/exit/crossover activity per venue in real time. *(client request · MoM 2 Sep 2026, 4.16 Fraud Detection & Live Monitoring · DI-651)*

`BO-255` Live Venue Occupancy & People Counting

- Fraud assessment view flags suspicious usage patterns or threats; live monitoring shows current attendance, in-park counts and entry/exit/crossover activity per venue in real time. *(client request · MoM 2 Sep 2026, 4.16 Fraud Detection & Live Monitoring · DI-651)*
- Access decisions consider who, ticket type, where, when and context; e.g. an otherwise valid unused ticket is denied once the venue's maximum live occupancy is reached, until guests exit. Scanners need a venue-full denial state. *(agreed · MoM 2 Sep 2026, 4.16 Attribute-Based Access Control · DI-650)*
- Two capacity types shown distinctly: sales capacity (tickets sellable per performance) and admission capacity (a real-time, scan-based count of guests inside via entry/exit turnstiles), capping on-site attendance independent of tickets sold. *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-455)*
- Admission Summary dashboard: real-time headcount of guests inside the venue from ticket scans. *(agreed · MoM 7 Aug 2026, 21. Dashboards & Reporting · DI-182)*

`BO-256` Graphical Access Map & Live Gate Performance

- Venue-wide attendance overview (open/closed gates, offline/maintenance status, graphed) and a visual map of all access-control locations across venues/tenants, including entry and exit turnstile layouts that vary by venue. *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-623)*

`BO-258` Entry, Exit, Re-entry & Crossover Analytics

- Group/B2B admission profile view shows entry statistics by category (general admission, group, re-entry, crossover) and attendance breakdowns for schools and other groups from scanned tickets. *(client request · MoM 2 Sep 2026, 4.15 Guest Journey, Group/B2B Profiles & Live Operations Dashboard · DI-647)*

`BO-264` Group Sales Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- One unified flow for groups, schools and corporates: inquiry > package builder > quotation > approval > confirmed booking. *(agreed · MoM 31 Aug 2026, 4.7 Group Sales / 5. Key Decisions · DI-565)*
- Sales-team dashboard shows group inquiries, opportunities and confirmed bookings and flags items needing attention. Customer types: individual (B2C/walk-in), group, school (with subcategories e.g. by curriculum/nationality), configurable to add more. *(client request · MoM 31 Aug 2026, 4.7 Group Sales & Corporate/School Bookings · DI-563)*

`BO-265` Group Enquiry & Opportunity Capture

- Sales-team dashboard shows group inquiries, opportunities and confirmed bookings and flags items needing attention. Customer types: individual (B2C/walk-in), group, school (with subcategories e.g. by curriculum/nationality), configurable to add more. *(client request · MoM 31 Aug 2026, 4.7 Group Sales & Corporate/School Bookings · DI-563)*

`BO-266` Group Customer & Organization Profile

- Sales-team dashboard shows group inquiries, opportunities and confirmed bookings and flags items needing attention. Customer types: individual (B2C/walk-in), group, school (with subcategories e.g. by curriculum/nationality), configurable to add more. *(client request · MoM 31 Aug 2026, 4.7 Group Sales & Corporate/School Bookings · DI-563)*

`BO-268` Group Package & Experience Builder

- One unified flow for groups, schools and corporates: inquiry > package builder > quotation > approval > confirmed booking. *(agreed · MoM 31 Aug 2026, 4.7 Group Sales / 5. Key Decisions · DI-565)*
- Package builder assembles admission, meals, workshops etc. against real-time availability and generates a quotation; negotiated revisions are kept as successive versions; extra discounts go through a configurable approval workflow. *(client request · MoM 31 Aug 2026, 4.7 Group Sales & Corporate/School Bookings · DI-564)*

`BO-269` Group Quotation Builder & Proposal Generation

- One unified flow for groups, schools and corporates: inquiry > package builder > quotation > approval > confirmed booking. *(agreed · MoM 31 Aug 2026, 4.7 Group Sales / 5. Key Decisions · DI-565)*
- Package builder assembles admission, meals, workshops etc. against real-time availability and generates a quotation; negotiated revisions are kept as successive versions; extra discounts go through a configurable approval workflow. *(client request · MoM 31 Aug 2026, 4.7 Group Sales & Corporate/School Bookings · DI-564)*

`BO-270` Quote Revision, Negotiation & Version Management

- Package builder assembles admission, meals, workshops etc. against real-time availability and generates a quotation; negotiated revisions are kept as successive versions; extra discounts go through a configurable approval workflow. *(client request · MoM 31 Aug 2026, 4.7 Group Sales & Corporate/School Bookings · DI-564)*

`BO-271` Group Discount, Exception & Approval Workflow

- Package builder assembles admission, meals, workshops etc. against real-time availability and generates a quotation; negotiated revisions are kept as successive versions; extra discounts go through a configurable approval workflow. *(client request · MoM 31 Aug 2026, 4.7 Group Sales & Corporate/School Bookings · DI-564)*

`BO-272` Quote-to-Booking Conversion & Confirmation

- One unified flow for groups, schools and corporates: inquiry > package builder > quotation > approval > confirmed booking. *(agreed · MoM 31 Aug 2026, 4.7 Group Sales / 5. Key Decisions · DI-565)*

`BO-273` Group Booking 360° & Handover Workspace

- Family/dependent view shows a family ticket's composition (e.g. two adults, two children) with each dependent's entitlements; equivalent views for school and corporate bookings. *(client request · MoM 7 Sep 2026, 4.9 Entitlements Portfolio - Structure, Family/Group & Assignment · DI-668)*

`BO-274` Group Booking Operations Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Group operations view shows upcoming arrivals for the day/period and flags deposits still required; staff (e.g. tour guide, educator) can be assigned to a group ahead of arrival; participant details captured where required. *(client request · MoM 31 Aug 2026, 4.8 Group Operations, Payment Links & Check-In · DI-566)*

`BO-275` Group Operational Planning & Task Workspace

- Group operations view shows upcoming arrivals for the day/period and flags deposits still required; staff (e.g. tour guide, educator) can be assigned to a group ahead of arrival; participant details captured where required. *(client request · MoM 31 Aug 2026, 4.8 Group Operations, Payment Links & Check-In · DI-566)*

`BO-276` Participants, Guest Lists & Group Structure

- Group operations view shows upcoming arrivals for the day/period and flags deposits still required; staff (e.g. tour guide, educator) can be assigned to a group ahead of arrival; participant details captured where required. *(client request · MoM 31 Aug 2026, 4.8 Group Operations, Payment Links & Check-In · DI-566)*

`BO-277` Group Payment, Deposit & Balance Management

- Amendments/cancellations/reschedules are checked against the applicable policy before being allowed. A booking's financial status (deposit required, partial payment, full payment) is tracked; schools and corporates can pay a 20-30% deposit with the balance due on or before arrival. *(agreed · MoM 1 Sep 2026, 4.12 Amendment, Cancellation & Booking Status · DI-615)*
- Send Payment Link (deposit or full) opens a B2C-style cart-review and checkout page showing the booking the sales team created. Configurable expiry (e.g. 24 hours, a week); unpaid bookings auto-cancel on expiry. Applies to B2C, schools, corporates and groups. *(agreed · MoM 31 Aug 2026, 4.8 Send Payment Link · DI-567)*

`BO-278` Group Ticket, Seat & Entitlement Allocation

- Group ticket QR options: one QR valid for a defined headcount, individual QR per member, or a single rotating/multi-use QR scanned until the headcount is exhausted. *(client request · MoM 31 Aug 2026, 4.8 Group Operations, Payment Links & Check-In · DI-569)*

`BO-279` Group Ticket Fulfillment & Distribution

- Group fulfilment via email/WhatsApp with reprint/resend. Group check-in status (arrived/checked-in vs not yet arrived) is tracked separately from the access-control scan, to run dedicated group counters. *(agreed · MoM 31 Aug 2026, 4.8 Group Operations, Payment Links & Check-In · DI-568)*

`BO-280` Group Arrival, Check-In & Admission Operations

- Group check-in is a status distinct from the access scan: the group arrival screen records "Record group check in" separately. *(agreed · MoM 31 Aug 2026, Key Decisions · DI-590)*
- Group fulfilment via email/WhatsApp with reprint/resend. Group check-in status (arrived/checked-in vs not yet arrived) is tracked separately from the access-control scan, to run dedicated group counters. *(agreed · MoM 31 Aug 2026, 4.8 Group Operations, Payment Links & Check-In · DI-568)*

`BO-284` Membership & Annual Pass Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`BO-285` Membership Product & Tier Builder

- Membership/pass tickets: seasonal, monthly or annual classes with renewal/auto-renewal using a tokenised card-on-file billed ahead of expiry, subject to the guest's consent to terms and conditions. *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-448)*

`BO-287` Validity, Activation & Expiry Configuration

- Validity types: fixed date range, rolling (e.g. 90 days from issue) and first-use activation (starts at first scan). Confirmed: first-use tickets need a fallback expiry (e.g. issue date + 30 days) if never scanned. *(agreed · MoM 25 Aug 2026, 4.5 Validity Management & Expiry Rules · DI-451)*

`BO-292` Renewal, Auto-Renewal & Membership Continuity Configuration

- Membership/pass tickets: seasonal, monthly or annual classes with renewal/auto-renewal using a tokenised card-on-file billed ahead of expiry, subject to the guest's consent to terms and conditions. *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-448)*

`BO-294` Member Operations Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`BO-295` Member 360° Membership Account Workspace

- B2B account financial tab shows credit limit, credit days and a linked account-specific price list; accounts can be a main account with child (agent) accounts; every account shows its full sales/transaction history, as does a B2C customer profile. *(client request · MoM 7 Aug 2026, 11. Accounts Management (B2B and B2C) · DI-162)*
- Membership / season pass is defined by start/end date rather than quantity, requires customer profile capture at purchase, and supports renew, upgrade, cancel and extend workflows. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-138)*

`BO-297` Visit, Admission & Entitlement Usage Monitor

- Accreditation-holder monitoring is a filtered view inside the general entitlement monitoring, not a separate platform, so staff can quickly distinguish and support large accredited groups. *(agreed · MoM 7 Sep 2026, 4.10 Entitlements Lifecycle, Consumption Monitoring & Screen Consolidation · DI-672)*
- Entitlement statuses: active, reserved, consumed, transferred, expired, refunded/cancelled; views show entitlements nearing expiry, real-time consumption per customer, and whether a ticket has been upgraded. *(client request · MoM 7 Sep 2026, 4.10 / 4.11 Entitlements Lifecycle & Usage · DI-670)*

`BO-298` Membership Freeze, Suspension & Reactivation Management

- Membership lifecycle: upgrade, downgrade, suspend (freezes validity until re-enabled), deactivate and cancel, with configurable timing windows (e.g. upgrade allowed only in the final two months before expiry). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-467)*

`BO-299` Membership Upgrade, Downgrade & Product Migration Operations

- Membership lifecycle: upgrade, downgrade, suspend (freezes validity until re-enabled), deactivate and cancel, with configurable timing windows (e.g. upgrade allowed only in the final two months before expiry). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-467)*

`BO-304` Order & Reservation Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Sales team creates bookings for any customer type and sends a confirmation; on arrival the guest presents it to collect physical media or scans directly at access control. Dashboard: today's orders/ reservations, confirmed guests, booking status; order detail shows customer and items. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-611)*

`BO-305` Order Detail & Transaction Workspace

- Sales team creates bookings for any customer type and sends a confirmation; on arrival the guest presents it to collect physical media or scans directly at access control. Dashboard: today's orders/ reservations, confirmed guests, booking status; order detail shows customer and items. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-611)*

`BO-306` Reservation & Hold Policy Configuration

- Booking statuses: draft > reserved (awaiting payment) > completed, with cancelled or expired paths. Hold policy sets how long a capacity booking is held pending payment before release to inventory. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-612)*

`BO-307` Order & Reservation Status Lifecycle Configuration

- Booking statuses: draft > reserved (awaiting payment) > completed, with cancelled or expired paths. Hold policy sets how long a capacity booking is held pending payment before release to inventory. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-612)*

`BO-308` Order Creation & Source/Channel Configuration

- Channel rules govern which actions each channel can perform (create, upgrade, cancel) and whether checkout is guest checkout (name, phone, email only) or full registration/sign-in. Customer category (corporate, travel agent/B2B, school) determines extra information collected. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-613)*
- Sales team creates bookings for any customer type and sends a confirmation; on arrival the guest presents it to collect physical media or scans directly at access control. Dashboard: today's orders/ reservations, confirmed guests, booking status; order detail shows customer and items. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-611)*

`BO-309` Customer, Guest & Account Assignment

- Channel rules govern which actions each channel can perform (create, upgrade, cancel) and whether checkout is guest checkout (name, phone, email only) or full registration/sign-in. Customer category (corporate, travel agent/B2B, school) determines extra information collected. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-613)*

`BO-310` Order Line, Product & Entitlement Composition

- Order lines show all contents (tickets, retail, F&B) with inventory hold/availability; a completeness check confirms payment, customer and capacity before finalising; an at-risk view flags bookings nearing expiry (e.g. payment not completed). *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-614)*

`BO-312` Reservation Confirmation, Expiry & Fulfillment Readiness

- Order lines show all contents (tickets, retail, F&B) with inventory hold/availability; a completeness check confirms payment, customer and capacity before finalising; an at-risk view flags bookings nearing expiry (e.g. payment not completed). *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-614)*

`BO-313` Order Lifecycle Timeline, SLA, Exceptions & AI Operations

- Order lines show all contents (tickets, retail, F&B) with inventory hold/availability; a completeness check confirms payment, customer and capacity before finalising; an at-risk view flags bookings nearing expiry (e.g. payment not completed). *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-614)*

`BO-314` Amendment & After-Sales Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Amendments/cancellations/reschedules are checked against the applicable policy before being allowed. A booking's financial status (deposit required, partial payment, full payment) is tracked; schools and corporates can pay a 20-30% deposit with the balance due on or before arrival. *(agreed · MoM 1 Sep 2026, 4.12 Amendment, Cancellation & Booking Status · DI-615)*

`BO-316` Amendment Eligibility & Policy Rule Builder

- Amendments/cancellations/reschedules are checked against the applicable policy before being allowed. A booking's financial status (deposit required, partial payment, full payment) is tracked; schools and corporates can pay a 20-30% deposit with the balance due on or before arrival. *(agreed · MoM 1 Sep 2026, 4.12 Amendment, Cancellation & Booking Status · DI-615)*

`BO-318` Refund Policy & Refund Calculation Configuration

- Approved refunds go back to the original payment method or are credited to the guest's wallet for future purchases. *(client request · MoM 7 Sep 2026, 4.11 Entitlements Usage, Upgrades & Refund/Credit Recovery · DI-673)*
- Refunds use preset time-banded percentages (e.g. full refund a set number of days before the event, less closer to/after it), support partial refunds, and let an authorised approver apply a custom override percentage. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-252)*
- Refund policy shown to guests is tiered and driven by back-office rules per business, e.g. no refund <24h, 50% between 24–48h, 100% >48h. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-192)*

`BO-324` Payment & Order Financial Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`BO-325` Order Payment Detail & Transaction Ledger

- Transactions ledger lists all transactions with daily counts/totals and pending/failed sync status; detail shows chart-of-account mapping, payment method, product lines and whether each line is in sale, deferred or redemption status. *(client request · MoM 12 Aug 2026, 15. Financial Transactions Ledger and Journal Entries · DI-264)*

`BO-331` Payment Reconciliation & Exception Management

- Payments screen consolidates gateway (Stripe, NI) and on-site (cash, card) payments and flags variances from a monthly reconciliation file (e.g. gateway 10,000 AED vs 9,500 AED recorded). *(agreed · MoM 12 Aug 2026, 17. Payments Reconciliation · DI-268)*
- Weekly/monthly reconciliation runs ingest → parse → match → classify → auto-resolve, so only genuinely mismatched amounts are shown for human review. *(agreed · MoM 12 Aug 2026, 11. Settlement and Reconciliation Process · DI-258)*

`BO-332` Financial Traceability, Control & Audit Explorer

- Transactions ledger lists all transactions with daily counts/totals and pending/failed sync status; detail shows chart-of-account mapping, payment method, product lines and whether each line is in sale, deferred or redemption status. *(client request · MoM 12 Aug 2026, 15. Financial Transactions Ledger and Journal Entries · DI-264)*

`BO-334` Virtual Ticket Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- A ticket is always one virtual record; QR, RFID, NFC, face and future credentials (e.g. hotel room key, city transit card) are interchangeable media linked to it. Screens should show one ticket with its linked media, not separate tickets per medium. *(agreed · MoM 2 Sep 2026, 5. Key Decisions & Agreements · DI-652)*

`BO-335` Virtual Ticket Identity & Master Record Configuration

- Media = any identifier a ticket is presented by (QR, RFID/wristband, facial recognition, other). Virtual ticket media IDs configurable by prefix, suffix and length; several media can link to one ticket (e.g. a season pass by face, QR or RFID as fallbacks). *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-608)*

`BO-336` Virtual Ticket Status & Lifecycle Model

- Entitlement statuses: active, reserved, consumed, transferred, expired, refunded/cancelled; views show entitlements nearing expiry, real-time consumption per customer, and whether a ticket has been upgraded. *(client request · MoM 7 Sep 2026, 4.10 / 4.11 Entitlements Lifecycle & Usage · DI-670)*

`BO-337` Media Type & Credential Technology Registry

- Media = any identifier a ticket is presented by (QR, RFID/wristband, facial recognition, other). Virtual ticket media IDs configurable by prefix, suffix and length; several media can link to one ticket (e.g. a season pass by face, QR or RFID as fallbacks). *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-608)*

`BO-338` Multi-Media Binding & Association Rules

- A ticket is always one virtual record; QR, RFID, NFC, face and future credentials (e.g. hotel room key, city transit card) are interchangeable media linked to it. Screens should show one ticket with its linked media, not separate tickets per medium. *(agreed · MoM 2 Sep 2026, 5. Key Decisions & Agreements · DI-652)*
- Media = any identifier a ticket is presented by (QR, RFID/wristband, facial recognition, other). Virtual ticket media IDs configurable by prefix, suffix and length; several media can link to one ticket (e.g. a season pass by face, QR or RFID as fallbacks). *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-608)*

`BO-341` Media Activation, Priority & Fallback Rules

- Media = any identifier a ticket is presented by (QR, RFID/wristband, facial recognition, other). Virtual ticket media IDs configurable by prefix, suffix and length; several media can link to one ticket (e.g. a season pass by face, QR or RFID as fallbacks). *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-608)*

`BO-344` Media Design Studio Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`BO-345` Digital QR & Barcode Ticket Designer

- Ticket PDF carries a live QR code, a unique ticket number/barcode (media identifier), customisable branding/layout, terms and conditions and guest name; screens must distinguish ticket ID (one per ticket) from media code (can cover several tickets scanned as one group). *(agreed · MoM 7 Aug 2026, 20. Live Point-of-Sale Transaction Walkthrough · DI-180)*

`BO-346` PDF, Printable & POS Ticket Designer

- Custom report templates (advanced users, SQL/scripting) exported as PDF or Excel; ticket and receipt layouts built in a drag-and-drop template builder placing dynamic variables (guest name, ticket number, QR) on a background image. *(agreed · MoM 7 Aug 2026, 22. Report & Document Template Design · DI-184)*
- Ticket PDF carries a live QR code, a unique ticket number/barcode (media identifier), customisable branding/layout, terms and conditions and guest name; screens must distinguish ticket ID (one per ticket) from media code (can cover several tickets scanned as one group). *(agreed · MoM 7 Aug 2026, 20. Live Point-of-Sale Transaction Walkthrough · DI-180)*

`BO-347` Apple Wallet Pass Designer

- **Open question.** Open: NFC inside a wallet pass needs Apple certification (works with any reader) vs HID SDK on the guest phone (likely HID readers only). QR-based wallet passes are straightforward. Chinmay leans to direct Apple certification unless it is a hard blocker. *(open · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-610)*
- Apple/Google Wallet configuration covers template design (background colour, header, footer) and the guest-facing "Add to Apple Wallet" flow after an online purchase. *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-609)*

`BO-348` Google Wallet Pass Designer

- **Open question.** Open: NFC inside a wallet pass needs Apple certification (works with any reader) vs HID SDK on the guest phone (likely HID readers only). QR-based wallet passes are straightforward. Chinmay leans to direct Apple certification unless it is a hard blocker. *(open · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-610)*
- Apple/Google Wallet configuration covers template design (background colour, header, footer) and the guest-facing "Add to Apple Wallet" flow after an online purchase. *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-609)*

`BO-353` Multi-Media Preview, Testing, Approval & Publication

- The preview/publish step shows how the ticket appears on the B2C front end and — at Chinmay's request — also the PDF ticket layout and Apple Wallet / Google Wallet formats, so the reviewer sees every output format. *(agreed · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference; 5. Key Decisions · DI-444)*

`BO-354` Credential Operations Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`BO-355` Virtual Ticket & Credential 360° Workspace

- A purchased ticket can be transferred to another guest (e.g. a friend); the system keeps the original purchaser and full transfer history. *(client request · MoM 7 Sep 2026, 4.9 Ownership and transfer · DI-669)*
- A ticket is always one virtual record; QR, RFID, NFC, face and future credentials (e.g. hotel room key, city transit card) are interchangeable media linked to it. Screens should show one ticket with its linked media, not separate tickets per medium. *(agreed · MoM 2 Sep 2026, 5. Key Decisions & Agreements · DI-652)*
- Resale keeps the original virtual ticket ID; only owner name and media (QR) change. An ownership change log shows the history against one ID (e.g. VT0010: Qossai > Allam > Chinmay). *(agreed · MoM 1 Sep 2026, 4.14 Decision (ticket ID on resale) · DI-620)*

`BO-357` Credential Delivery & Distribution Operations

- Decision: deferred seat assignment — sale confirmed at purchase as section + quantity; seats allocated internally; closer to the event ops/admin trigger a bulk e-mail issuing QR tickets with final seats. Immediate seat assignment remains for venues that need it. *(agreed · MoM 21 Aug 2026, 4.7 Deferred Seat Assignment Model; 5. Key Decisions · DI-423)*

`BO-359` Credential Replacement, Reissue, Revocation & Recovery

- Lost wristband/card: operations identify the guest (phone number or ID), locate the original transaction and transfer the balance to a replacement wristband/card. *(client request · MoM 27 Aug 2026, 4.10 Lost-media recovery · DI-538)*

`BO-364` Approval Command Center Dashboard

- Approval command centre/inbox shows all pending, validated and renewal requests and lets requests be assigned or reassigned to the relevant department or person. Approvals apply to any request type (new product, price change, website change). *(client request · MoM 8 Sep 2026, 4.12 Approval Workflow Recap - Inbox, SLA & Escalation · DI-723)*

`BO-365` My Approval Inbox

- Approval command centre/inbox shows all pending, validated and renewal requests and lets requests be assigned or reassigned to the relevant department or person. Approvals apply to any request type (new product, price change, website change). *(client request · MoM 8 Sep 2026, 4.12 Approval Workflow Recap - Inbox, SLA & Escalation · DI-723)*

`BO-366` Team / Shared Approval Queue

- Approval command centre/inbox shows all pending, validated and renewal requests and lets requests be assigned or reassigned to the relevant department or person. Approvals apply to any request type (new product, price change, website change). *(client request · MoM 8 Sep 2026, 4.12 Approval Workflow Recap - Inbox, SLA & Escalation · DI-723)*

`BO-367` Approval Request Detail

- Decision view includes a business context/evidence viewer (e.g. payment information, any logged customer complaint) and an approval timeline showing when the request was initiated and when each stage was completed or is pending. *(client request · MoM 8 Sep 2026, 4.15 Execution & Decision Management · DI-728)*
- Approval screens offer Approve, Reject, Return and Request More Information, show an AI-generated approval summary beside the request, and a visible trail of who approved at each stage (e.g. IT → Ops Manager → Finance → CEO → IT publishes). *(client request · MoM 10 Aug 2026, 5.5 Multi-Stage Approval Workflow · DI-235)*

`BO-368` AI Decision Support

- Approval is human-governed (Qossai): AI is limited to analytics (turnaround, bottlenecks, individual approver performance) and must not recommend or influence whether a request is approved or rejected. *(agreed · MoM 8 Sep 2026, 4.19 Approval Analytics & the Role of AI · DI-735)*

`BO-372` Approval SLA & Workload Monitor

- Approval analytics shows how long each request took and overall turnaround across all logged requests. *(client request · MoM 8 Sep 2026, 4.19 Approval Analytics & the Role of AI · DI-734)*
- SLA reminders notify the approver (e.g. by email) as the deadline approaches; a workload view shows how many pending requests each approver currently carries. *(client request · MoM 8 Sep 2026, 4.16 Delegation, Substitute Approval & SLA Monitoring · DI-731)*

`BO-374` Approval Decision Workspace

- Decision view includes a business context/evidence viewer (e.g. payment information, any logged customer complaint) and an approval timeline showing when the request was initiated and when each stage was completed or is pending. *(client request · MoM 8 Sep 2026, 4.15 Execution & Decision Management · DI-728)*
- Approval screens offer Approve, Reject, Return and Request More Information, show an AI-generated approval summary beside the request, and a visible trail of who approved at each stage (e.g. IT → Ops Manager → Finance → CEO → IT publishes). *(client request · MoM 10 Aug 2026, 5.5 Multi-Stage Approval Workflow · DI-235)*

`BO-375` Business Context & Evidence Viewer

- Decision view includes a business context/evidence viewer (e.g. payment information, any logged customer complaint) and an approval timeline showing when the request was initiated and when each stage was completed or is pending. *(client request · MoM 8 Sep 2026, 4.15 Execution & Decision Management · DI-728)*

`BO-376` Approval Timeline & Decision Chain

- Decision view includes a business context/evidence viewer (e.g. payment information, any logged customer complaint) and an approval timeline showing when the request was initiated and when each stage was completed or is pending. *(client request · MoM 8 Sep 2026, 4.15 Execution & Decision Management · DI-728)*
- Approval screens offer Approve, Reject, Return and Request More Information, show an AI-generated approval summary beside the request, and a visible trail of who approved at each stage (e.g. IT → Ops Manager → Finance → CEO → IT publishes). *(client request · MoM 10 Aug 2026, 5.5 Multi-Stage Approval Workflow · DI-235)*

`BO-377` Approve & Sensitive Action Confirmation

- MFA / additional confirmation for sensitive approval actions is a business-configurable option (on or off), not mandatory, but the screens must support it when enabled. *(agreed · MoM 8 Sep 2026, 4.15 Execution & Decision Management · DI-729)*

`BO-378` Reject / Return / Request Information

- An approver's decision offers four actions: Approve, Reject, Return (for changes) and Request More Information. *(agreed · MoM 10 Aug 2026, 5.5 · DI-244)*

`BO-385` Delegation Management

- Delegation/availability management defines a substitute approver so requests don't stall when an approver is unavailable. *(client request · MoM 8 Sep 2026, 4.16 Delegation, Substitute Approval & SLA Monitoring · DI-730)*

`BO-386` Temporary Delegation & Availability Calendar

- Delegation/availability management defines a substitute approver so requests don't stall when an approver is unavailable. *(client request · MoM 8 Sep 2026, 4.16 Delegation, Substitute Approval & SLA Monitoring · DI-730)*

`BO-387` Out-of-Office & Substitute Routing

- Delegation/availability management defines a substitute approver so requests don't stall when an approver is unavailable. *(client request · MoM 8 Sep 2026, 4.16 Delegation, Substitute Approval & SLA Monitoring · DI-730)*

`BO-388` Approval SLA Policy Configuration

- SLA rules set how fast a request must be approved (e.g. within one day); if not actioned it auto-escalates to the next level so someone can investigate (e.g. approver on leave) and reassign. *(client request · MoM 8 Sep 2026, 4.12 Approval Workflow Recap - Inbox, SLA & Escalation · DI-724)*

`BO-389` Reminder & Breach Notification Rules

- SLA reminders notify the approver (e.g. by email) as the deadline approaches; a workload view shows how many pending requests each approver currently carries. *(client request · MoM 8 Sep 2026, 4.16 Delegation, Substitute Approval & SLA Monitoring · DI-731)*

`BO-390` Escalation Policy Builder

- SLA rules set how fast a request must be approved (e.g. within one day); if not actioned it auto-escalates to the next level so someone can investigate (e.g. approver on leave) and reassign. *(client request · MoM 8 Sep 2026, 4.12 Approval Workflow Recap - Inbox, SLA & Escalation · DI-724)*

`BO-391` Live Escalation Operations Center

- SLA rules set how fast a request must be approved (e.g. within one day); if not actioned it auto-escalates to the next level so someone can investigate (e.g. approver on leave) and reassign. *(client request · MoM 8 Sep 2026, 4.12 Approval Workflow Recap - Inbox, SLA & Escalation · DI-724)*

`BO-394` Game & Ride Operations Dashboard

- Command centre lists all games/rides with active/offline status. In the reference docs "attractions" means individual games (roller coaster, racing game, bumper cars), not venues. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-863)*

`BO-395` Game & Ride Directory

- Game directory categorised by type (skill, arcade, etc.); game profile captures description, type and location; reusable attraction-type templates (rides, skill games, video games); a game can be placed in maintenance mode for a defined period. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-864)*
- Command centre lists all games/rides with active/offline status. In the reference docs "attractions" means individual games (roller coaster, racing game, bumper cars), not venues. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-863)*

`BO-396` Attraction Profile

- Game directory categorised by type (skill, arcade, etc.); game profile captures description, type and location; reusable attraction-type templates (rides, skill games, video games); a game can be placed in maintenance mode for a defined period. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-864)*

`BO-397` Attraction Type Configuration

- Game directory categorised by type (skill, arcade, etc.); game profile captures description, type and location; reusable attraction-type templates (rides, skill games, video games); a game can be placed in maintenance mode for a defined period. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-864)*

`BO-398` Game & Ride Operational Configuration

- Game directory categorised by type (skill, arcade, etc.); game profile captures description, type and location; reusable attraction-type templates (rides, skill games, video games); a game can be placed in maintenance mode for a defined period. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-864)*

`BO-399` Wallet & Credit Acceptance Mapping

- Per game: which credit types are accepted (cash/wallet, bonus, redemption) and a configurable consumption priority (bonus first, then prepaid/cash, then others). *(agreed · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-865)*

`BO-400` Attraction / Reader Mapping

- Each game maps to its physical reader; package entitlement sets play-count limits and validity per game; a dependency log records related configuration changes. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-866)*

`BO-401` Game Package & Entitlement Association

- Each game maps to its physical reader; package entitlement sets play-count limits and validity per game; a dependency log records related configuration changes. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-866)*

`BO-403` Attraction Audit, Dependencies & Governed Actions

- Each game maps to its physical reader; package entitlement sets play-count limits and validity per game; a dependency log records related configuration changes. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-866)*

`BO-409` Retap Delay & Transaction Protection

- Retap protection: a configurable delay stops a card being charged again while a game is in progress; the reader shows e.g. "please retry again in 3 seconds". *(agreed · MoM 11 Sep 2026, 4.8 Game Reader & Device Configuration · DI-867)*

`BO-410` Free Game Glow & Reader Display Rules

- Free-game display: a distinct reader colour/theme for free games so guests recognise them immediately; reader response configuration defines what the reader shows after a validated tap. *(client request · MoM 11 Sep 2026, 4.8 Game Reader & Device Configuration · DI-868)*

`BO-411` Reader Theme & Experience Configuration

- Free-game display: a distinct reader colour/theme for free games so guests recognise them immediately; reader response configuration defines what the reader shows after a validated tap. *(client request · MoM 11 Sep 2026, 4.8 Game Reader & Device Configuration · DI-868)*
- Each game/ride has a TICVAI reader that displays pricing, branding and theme pushed from the TICVAI back end; a tap triggers a dry-contact-style start/stop signal (like a turnstile). *(agreed · MoM 11 Sep 2026, 4.6 Gaming - Reader Hardware Strategy & Vendor Sourcing · DI-862)*

`BO-412` Real-Time Tap Validation & Reader Response

- Free-game display: a distinct reader colour/theme for free games so guests recognise them immediately; reader response configuration defines what the reader shows after a validated tap. *(client request · MoM 11 Sep 2026, 4.8 Game Reader & Device Configuration · DI-868)*
- Retap protection: a configurable delay stops a card being charged again while a game is in progress; the reader shows e.g. "please retry again in 3 seconds". *(agreed · MoM 11 Sep 2026, 4.8 Game Reader & Device Configuration · DI-867)*

`BO-413` Balance Check Reader & Device Test Console

- A balance-check reader (the gameplay reader or a dedicated one) lets a guest tap to see their current balance without playing. *(client request · MoM 11 Sep 2026, 4.8 Game Reader & Device Configuration · DI-869)*

`BO-414` Wallet & Credit Management Dashboard

- Per-customer wallet view shows paid credit, bonus credit, free-game allowance and redemption credit together, with a full transaction ledger. *(client request · MoM 11 Sep 2026, 4.9 Wallet & Credit Management for Gaming · DI-870)*

`BO-416` Wallet Account & Balance View

- Per-customer wallet view shows paid credit, bonus credit, free-game allowance and redemption credit together, with a full transaction ledger. *(client request · MoM 11 Sep 2026, 4.9 Wallet & Credit Management for Gaming · DI-870)*

`BO-417` Top-Up Configuration

- Top-up configuration: minimum/maximum amounts and bonus-on-top-up rules (e.g. top up 50 get 10 bonus; top up 100 get 25). *(client request · MoM 11 Sep 2026, 4.9 Wallet & Credit Management for Gaming · DI-871)*

`BO-418` Top-Up Bonus Rule Configuration

- Top-up configuration: minimum/maximum amounts and bonus-on-top-up rules (e.g. top up 50 get 10 bonus; top up 100 get 25). *(client request · MoM 11 Sep 2026, 4.9 Wallet & Credit Management for Gaming · DI-871)*
- Bonus credit tiers (e.g. AED 100 top-up earns AED 20 bonus; AED 200 earns AED 60). Bonus credit is consumed before base top-up credit and carries its own separate validity period. *(agreed · MoM 27 Aug 2026, 4.6 Stored Value, Credit Consumption & FEFO Logic · DI-524)*

`BO-419` Bonus Usage Restrictions

- Bonus credit can be restricted to contexts - e.g. games only (not F&B), or arcade games only (not video games); bonus validity/expiry configurable. *(agreed · MoM 11 Sep 2026, 4.9 Wallet & Credit Management for Gaming · DI-872)*

`BO-420` Bonus Validity & Expiry Configuration

- Bonus credit can be restricted to contexts - e.g. games only (not F&B), or arcade games only (not video games); bonus validity/expiry configurable. *(agreed · MoM 11 Sep 2026, 4.9 Wallet & Credit Management for Gaming · DI-872)*

`BO-421` Free Game & Ride Credit Management

- An authorised supervisor can grant a discretionary bonus credit (e.g. service recovery) via card tap; balance refunds and adjustments handled on the same board. *(client request · MoM 11 Sep 2026, 4.9 Wallet & Credit Management for Gaming · DI-873)*

`BO-422` Refund, Adjustment & Manual Bonus Control

- An authorised supervisor can grant a discretionary bonus credit (e.g. service recovery) via card tap; balance refunds and adjustments handled on the same board. *(client request · MoM 11 Sep 2026, 4.9 Wallet & Credit Management for Gaming · DI-873)*

`BO-423` Wallet Credit Transaction Ledger & Audit

- Per-customer wallet view shows paid credit, bonus credit, free-game allowance and redemption credit together, with a full transaction ledger. *(client request · MoM 11 Sep 2026, 4.9 Wallet & Credit Management for Gaming · DI-870)*

`BO-424` Gameplay Validation Command Center

- At tap, validation checks the card is valid for that game and the entitlement/credit is available, applying the consumption priority; card activation starts from first top-up or a fixed date; a simulator tests configuration before publish. *(client request · MoM 11 Sep 2026, 4.10 Gameplay Validation, Entitlements & Rule Configuration · DI-874)*

`BO-425` Gameplay Validation Rule Configuration

- At tap, validation checks the card is valid for that game and the entitlement/credit is available, applying the consumption priority; card activation starts from first top-up or a fixed date; a simulator tests configuration before publish. *(client request · MoM 11 Sep 2026, 4.10 Gameplay Validation, Entitlements & Rule Configuration · DI-874)*

`BO-426` Deduction Priority & Funding Source Rules

- Per game: which credit types are accepted (cash/wallet, bonus, redemption) and a configurable consumption priority (bonus first, then prepaid/cash, then others). *(agreed · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-865)*

`BO-427` All Games & Rides Pass Configuration

- Entitlements: unlimited all games for a validity period, unlimited on a specific game, limited counted plays on a specific game; a package builder bundles several games and their entitlements into one product. *(client request · MoM 11 Sep 2026, 4.10 Gameplay Validation, Entitlements & Rule Configuration · DI-875)*
- Five gaming product types, configurable per product: pay-per-play from wallet; free play on a specific set of games; unlimited play on any game; per-game play counts (e.g. 2 on A, 5 on B, unlimited on C, none on D unless paid); fully free game. *(client request · MoM 11 Sep 2026, 4.5 Gaming Module - Concept & Use Cases · DI-861)*

`BO-428` Specific Game/Ride Unlimited Entitlement

- Entitlements: unlimited all games for a validity period, unlimited on a specific game, limited counted plays on a specific game; a package builder bundles several games and their entitlements into one product. *(client request · MoM 11 Sep 2026, 4.10 Gameplay Validation, Entitlements & Rule Configuration · DI-875)*
- Five gaming product types, configurable per product: pay-per-play from wallet; free play on a specific set of games; unlimited play on any game; per-game play counts (e.g. 2 on A, 5 on B, unlimited on C, none on D unless paid); fully free game. *(client request · MoM 11 Sep 2026, 4.5 Gaming Module - Concept & Use Cases · DI-861)*

`BO-429` Specific Game/Ride Limited Entitlement

- Entitlements: unlimited all games for a validity period, unlimited on a specific game, limited counted plays on a specific game; a package builder bundles several games and their entitlements into one product. *(client request · MoM 11 Sep 2026, 4.10 Gameplay Validation, Entitlements & Rule Configuration · DI-875)*
- Five gaming product types, configurable per product: pay-per-play from wallet; free play on a specific set of games; unlimited play on any game; per-game play counts (e.g. 2 on A, 5 on B, unlimited on C, none on D unless paid); fully free game. *(client request · MoM 11 Sep 2026, 4.5 Gaming Module - Concept & Use Cases · DI-861)*

`BO-430` Game Package Builder

- Entitlements: unlimited all games for a validity period, unlimited on a specific game, limited counted plays on a specific game; a package builder bundles several games and their entitlements into one product. *(client request · MoM 11 Sep 2026, 4.10 Gameplay Validation, Entitlements & Rule Configuration · DI-875)*
- Five gaming product types, configurable per product: pay-per-play from wallet; free play on a specific set of games; unlimited play on any game; per-game play counts (e.g. 2 on A, 5 on B, unlimited on C, none on D unless paid); fully free game. *(client request · MoM 11 Sep 2026, 4.5 Gaming Module - Concept & Use Cases · DI-861)*

`BO-431` Entitlement Validity & Activation Rules

- At tap, validation checks the card is valid for that game and the entitlement/credit is available, applying the consumption priority; card activation starts from first top-up or a fixed date; a simulator tests configuration before publish. *(client request · MoM 11 Sep 2026, 4.10 Gameplay Validation, Entitlements & Rule Configuration · DI-874)*

`BO-432` Real-Time Gameplay Authorization

- At tap, validation checks the card is valid for that game and the entitlement/credit is available, applying the consumption priority; card activation starts from first top-up or a fixed date; a simulator tests configuration before publish. *(client request · MoM 11 Sep 2026, 4.10 Gameplay Validation, Entitlements & Rule Configuration · DI-874)*

`BO-433` Validation Simulator & Exception Analysis

- At tap, validation checks the card is valid for that game and the entitlement/credit is available, applying the consumption priority; card activation starts from first top-up or a fixed date; a simulator tests configuration before publish. *(client request · MoM 11 Sep 2026, 4.10 Gameplay Validation, Entitlements & Rule Configuration · DI-874)*

`BO-435` Standard Game & Ride Price Configuration

- Game pricing by customer profile (regular vs VIP), date range and peak/off-peak (weekday/weekend, time-of-day), with exception dates excluding certain pricing (e.g. New Year's Eve). *(client request · MoM 11 Sep 2026, 4.11 Game Pricing Management & Retry Pricing · DI-876)*

`BO-437` Peak / Non-Peak Dynamic Pricing

- Game pricing by customer profile (regular vs VIP), date range and peak/off-peak (weekday/weekend, time-of-day), with exception dates excluding certain pricing (e.g. New Year's Eve). *(client request · MoM 11 Sep 2026, 4.11 Game Pricing Management & Retry Pricing · DI-876)*

`BO-438` Pricing Calendar & Exception Dates

- Game pricing by customer profile (regular vs VIP), date range and peak/off-peak (weekday/weekend, time-of-day), with exception dates excluding certain pricing (e.g. New Year's Eve). *(client request · MoM 11 Sep 2026, 4.11 Game Pricing Management & Retry Pricing · DI-876)*

`BO-439` Normal & VIP Pricing Configuration

- Game pricing by customer profile (regular vs VIP), date range and peak/off-peak (weekday/weekend, time-of-day), with exception dates excluding certain pricing (e.g. New Year's Eve). *(client request · MoM 11 Sep 2026, 4.11 Game Pricing Management & Retry Pricing · DI-876)*

`BO-440` Retry Price Configuration

- Retry pricing: after a game the reader prompts a time-limited discounted price to replay immediately (e.g. a game normally 25 offered at a reduced rate), within a configurable window. *(agreed · MoM 11 Sep 2026, 4.11 Game Pricing Management & Retry Pricing · DI-877)*

`BO-442` Effective Pricing & Reader Price Preview

- Retry pricing: after a game the reader prompts a time-limited discounted price to replay immediately (e.g. a game normally 25 offered at a reduced rate), within a configurable window. *(agreed · MoM 11 Sep 2026, 4.11 Game Pricing Management & Retry Pricing · DI-877)*
- Each game/ride has a TICVAI reader that displays pricing, branding and theme pushed from the TICVAI back end; a tap triggers a dry-contact-style start/stop signal (like a turnstile). *(agreed · MoM 11 Sep 2026, 4.6 Gaming - Reader Hardware Strategy & Vendor Sourcing · DI-862)*

`BO-444` Redemption Operations Dashboard

- Redemption points earned per game (score or level) are redeemed for prizes at a counter; per-game config of points granted or required (e.g. 200 points to play using redemption credit). *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-878)*

`BO-445` Redemption Credit Rule Configuration

- Redemption points earned per game (score or level) are redeemed for prizes at a counter; per-game config of points granted or required (e.g. 200 points to play using redemption credit). *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-878)*

`BO-446` Ticket-Based Redemption / Ticket-Eater Integration

- Physical-ticket redemption: some games dispense paper tickets by score, redeemed at a counter or ticket-counting machine. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-879)*

`BO-449` Redemption Counter / Prize Checkout

- Redemption points earned per game (score or level) are redeemed for prizes at a counter; per-game config of points granted or required (e.g. 200 points to play using redemption credit). *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-878)*

`BO-450` Prize Catalogue & Credit Cost Configuration

- Redemption points earned per game (score or level) are redeemed for prizes at a counter; per-game config of points granted or required (e.g. 200 points to play using redemption credit). *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-878)*

`BO-454` Card Lifecycle Command Center

- Card lifecycle shows each card's balance, validity and expiry rule (fixed date or rolling from last top-up/activity) and last activity, with replace, block and suspend actions. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-880)*

`BO-455` Card / Credential Profile

- Card lifecycle shows each card's balance, validity and expiry rule (fixed date or rolling from last top-up/activity) and last activity, with replace, block and suspend actions. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-880)*

`BO-456` Card Expiry Rule Configuration

- Card lifecycle shows each card's balance, validity and expiry rule (fixed date or rolling from last top-up/activity) and last activity, with replace, block and suspend actions. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-880)*

`BO-457` Last Recharge & Last Activity Tracking

- Card lifecycle shows each card's balance, validity and expiry rule (fixed date or rolling from last top-up/activity) and last activity, with replace, block and suspend actions. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-880)*

`BO-460` Card Block, Suspend & Reactivation Control

- Card lifecycle shows each card's balance, validity and expiry rule (fixed date or rolling from last top-up/activity) and last activity, with replace, block and suspend actions. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-880)*

`BO-461` Card Replacement & Wallet Relinking

- Card lifecycle shows each card's balance, validity and expiry rule (fixed date or rolling from last top-up/activity) and last activity, with replace, block and suspend actions. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-880)*
- Lost wristband/card: operations identify the guest (phone number or ID), locate the original transaction and transfer the balance to a replacement wristband/card. *(client request · MoM 27 Aug 2026, 4.10 Lost-media recovery · DI-538)*

`BO-464` Game & Ride Operations Control Center

- Live operations view: taps, rejected plays, wallet value consumed, per-game play counts, reader status and tap-validation logs (which card on which reader, when). *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-881)*

`BO-465` Live Gameplay Transaction Monitor

- Live operations view: taps, rejected plays, wallet value consumed, per-game play counts, reader status and tap-validation logs (which card on which reader, when). *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-881)*

`BO-466` Reader & Device Health Monitor

- Live operations view: taps, rejected plays, wallet value consumed, per-game play counts, reader status and tap-validation logs (which card on which reader, when). *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-881)*

`BO-467` Tap Validation & Decision Trace

- Live operations view: taps, rejected plays, wallet value consumed, per-game play counts, reader status and tap-validation logs (which card on which reader, when). *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-881)*

`BO-468` Rejected Transaction & Reason Analysis

- Rejected taps logged with reason (no entitlement, insufficient balance, etc.); entitlement-consumption monitor, offline sync/queue monitor, operational alerts; analytics for total games played, unique players, paid vs value-credit usage. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-882)*

`BO-470` Entitlement & Free-Play Consumption Monitor

- Rejected taps logged with reason (no entitlement, insufficient balance, etc.); entitlement-consumption monitor, offline sync/queue monitor, operational alerts; analytics for total games played, unique players, paid vs value-credit usage. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-882)*

`BO-471` Offline, Synchronization & Recovery Monitor

- Rejected taps logged with reason (no entitlement, insufficient balance, etc.); entitlement-consumption monitor, offline sync/queue monitor, operational alerts; analytics for total games played, unique players, paid vs value-credit usage. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-882)*

`BO-473` Operational Analytics & Reconciliation Dashboard

- Rejected taps logged with reason (no entitlement, insufficient balance, etc.); entitlement-consumption monitor, offline sync/queue monitor, operational alerts; analytics for total games played, unique players, paid vs value-credit usage. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-882)*

`BO-474` Reader Integration Command Center

- Reader integration board configures lighting/display behaviour and other device-level settings exposed via the vendor SDK. *(client request · MoM 11 Sep 2026, 4.14 Reader Integration Protocol Management · DI-884)*

`BO-476` Communication Protocol Configuration

- Reader integration board configures lighting/display behaviour and other device-level settings exposed via the vendor SDK. *(client request · MoM 11 Sep 2026, 4.14 Reader Integration Protocol Management · DI-884)*

`BO-479` Game Trigger & I/O Control Mapping

- Each game/ride has a TICVAI reader that displays pricing, branding and theme pushed from the TICVAI back end; a tap triggers a dry-contact-style start/stop signal (like a turnstile). *(agreed · MoM 11 Sep 2026, 4.6 Gaming - Reader Hardware Strategy & Vendor Sourcing · DI-862)*

`BO-480` Reader Screen, LED & Sound Output Mapping

- Reader integration board configures lighting/display behaviour and other device-level settings exposed via the vendor SDK. *(client request · MoM 11 Sep 2026, 4.14 Reader Integration Protocol Management · DI-884)*
- Each game/ride has a TICVAI reader that displays pricing, branding and theme pushed from the TICVAI back end; a tap triggers a dry-contact-style start/stop signal (like a turnstile). *(agreed · MoM 11 Sep 2026, 4.6 Gaming - Reader Hardware Strategy & Vendor Sourcing · DI-862)*

`BO-484` Self-Service Experience Command Center

- Optional self-service kiosk lets guests top up, buy gaming products and manage their card without a staffed counter. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-883)*

`BO-485` Self-Service Kiosk Profile & Channel Configuration

- Optional self-service kiosk lets guests top up, buy gaming products and manage their card without a staffed counter. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-883)*

`BO-486` Customer Card / Wallet Identification

- Optional self-service kiosk lets guests top up, buy gaming products and manage their card without a staffed counter. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-883)*

`BO-487` Customer Wallet & Balance Summary

- Optional self-service kiosk lets guests top up, buy gaming products and manage their card without a staffed counter. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-883)*

`BO-488` Self-Service Wallet Top-Up

- Optional self-service kiosk lets guests top up, buy gaming products and manage their card without a staffed counter. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-883)*

`BO-489` Bonus, Free Game & Benefit View

- Optional self-service kiosk lets guests top up, buy gaming products and manage their card without a staffed counter. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-883)*

`BO-490` Game & Ride Eligibility / “What Can I Play?”

- Optional self-service kiosk lets guests top up, buy gaming products and manage their card without a staffed counter. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-883)*

`BO-494` Rental Product Command Center

- Rental product list shows active/inactive products and distinguishes serialized items (individually tracked, e.g. numbered bicycle) from pooled inventory (quantity only, e.g. life jackets); categories show how many product variants sit under each. *(client request · MoM 9 Sep 2026, 4.1 Rental Product Configuration & Categories · DI-739)*

`BO-495` Create Rental Product Wizard

- Per product, tracking model is serialized, pooled or combined; plus whether the item must be scanned or simply picked, and whether substitution with another item is allowed if the requested one is unavailable. *(agreed · MoM 9 Sep 2026, 4.1 Rental Product Configuration & Categories · DI-740)*

`BO-497` Rental Category & Classification Setup

- Rental product list shows active/inactive products and distinguishes serialized items (individually tracked, e.g. numbered bicycle) from pooled inventory (quantity only, e.g. life jackets); categories show how many product variants sit under each. *(client request · MoM 9 Sep 2026, 4.1 Rental Product Configuration & Categories · DI-739)*

`BO-498` Inventory Tracking Model

- Per product, tracking model is serialized, pooled or combined; plus whether the item must be scanned or simply picked, and whether substitution with another item is allowed if the requested one is unavailable. *(agreed · MoM 9 Sep 2026, 4.1 Rental Product Configuration & Categories · DI-740)*

`BO-499` Rental Location Assignment

- **Open question.** Physical rental booths/stations need to appear on the live venue map; open whether the map builder already covers booth/station configuration or a dedicated addition is needed (Chinmay to check). *(open · MoM 9 Sep 2026, 4.11 Follow-Ups from Prior Sessions · DI-773)*
- Location assignment defines pickup and return points, including cross-location return (pick up at A, return at B). Duration supports fixed blocks (e.g. 1-hour or 2-hour cycle rental) with min/max duration. *(client request · MoM 9 Sep 2026, 4.2 Rental Location, Duration & Eligibility Rules · DI-741)*

`BO-500` Rental Duration & Turnaround Configuration

- Location assignment defines pickup and return points, including cross-location return (pick up at A, return at B). Duration supports fixed blocks (e.g. 1-hour or 2-hour cycle rental) with min/max duration. *(client request · MoM 9 Sep 2026, 4.2 Rental Location, Duration & Eligibility Rules · DI-741)*

`BO-501` Rental Rules & Operational Policy

- Eligibility rules: required documentation (e.g. Emirates ID collected and returned with the item), age restrictions, and which customer-profile fields must be captured at rental time. *(client request · MoM 9 Sep 2026, 4.2 Rental Location, Duration & Eligibility Rules · DI-742)*

`BO-502` Customer Requirements, Agreement & Waiver

- Eligibility rules: required documentation (e.g. Emirates ID collected and returned with the item), age restrictions, and which customer-profile fields must be captured at rental time. *(client request · MoM 9 Sep 2026, 4.2 Rental Location, Duration & Eligibility Rules · DI-742)*

`BO-503` Product Validation, Approval & Publication

- A final validation step checks pricing, duration and inventory configuration before a rental product can be published for sale on-site or online. *(client request · MoM 9 Sep 2026, 4.2 Rental Location, Duration & Eligibility Rules · DI-743)*

`BO-504` Rental Inventory Command Center

- Inventory overview shows totals by status - available, reserved, rented, in maintenance, out of service - per product. Serialized items show condition (good, in repair, in maintenance) and lifecycle history (purchase date, servicing, rental activity); pooled items show aggregate quantity only. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-744)*

`BO-505` Serialized Equipment Registry

- Inventory overview shows totals by status - available, reserved, rented, in maintenance, out of service - per product. Serialized items show condition (good, in repair, in maintenance) and lifecycle history (purchase date, servicing, rental activity); pooled items show aggregate quantity only. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-744)*

`BO-506` Equipment / Asset Profile

- Inventory overview shows totals by status - available, reserved, rented, in maintenance, out of service - per product. Serialized items show condition (good, in repair, in maintenance) and lifecycle history (purchase date, servicing, rental activity); pooled items show aggregate quantity only. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-744)*

`BO-507` Pooled Inventory Management

- Inventory overview shows totals by status - available, reserved, rented, in maintenance, out of service - per product. Serialized items show condition (good, in repair, in maintenance) and lifecycle history (purchase date, servicing, rental activity); pooled items show aggregate quantity only. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-744)*

`BO-508` Equipment Status & Condition Management

- Staff change an item's status (maintenance/repair) with a reason and an estimated return-to-service date; scanning an item's QR code pulls up its full details instantly. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-745)*
- Rental/equipment items use simplified states — available, rented, faulty/out-of-maintenance (excluded from available inventory until resolved) — not granular custom attributes. Clients supply item data at onboarding; a screen lets them update inventory and item details afterwards. *(agreed · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management; 5. Key Decisions · DI-500)*

`BO-509` QR / Barcode Equipment Identification

- Staff change an item's status (maintenance/repair) with a reason and an estimated return-to-service date; scanning an item's QR code pulls up its full details instantly. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-745)*

`BO-510` Inventory Location Allocation

- Stock is allocated per pickup location (e.g. 50 life jackets at A, 100 at B) with inter-location transfer; adjustments record damaged/lost/stolen with a reason; rebalancing view shows availability and shortages by station. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-746)*

`BO-511` Inventory Transfer Management

- Stock is allocated per pickup location (e.g. 50 life jackets at A, 100 at B) with inter-location transfer; adjustments record damaged/lost/stolen with a reason; rebalancing view shows availability and shortages by station. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-746)*

`BO-512` Inventory Adjustment & Exception Management

- Stock is allocated per pickup location (e.g. 50 life jackets at A, 100 at B) with inter-location transfer; adjustments record damaged/lost/stolen with a reason; rebalancing view shows availability and shortages by station. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-746)*

`BO-513` Inventory Intelligence & Rebalancing

- Stock is allocated per pickup location (e.g. 50 life jackets at A, 100 at B) with inter-location transfer; adjustments record damaged/lost/stolen with a reason; rebalancing view shows availability and shortages by station. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-746)*

`BO-514` Availability Command Center

- Real-time availability view shows total, available, rented and returned inventory per item and per location, alongside revenue generated. *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-747)*

`BO-515` Availability Rule Configuration

- Per-item availability rules: minimum advance booking time, maximum advance window, last-minute cutoff, same-day booking allowed, min/max booking quantity. Operating hours per station; slot inventory per window (e.g. 10 kayaks 10-11 and 11-12, then 5 at 12-1). *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-748)*

`BO-516` Operating Hours & Rental Windows

- Per-item availability rules: minimum advance booking time, maximum advance window, last-minute cutoff, same-day booking allowed, min/max booking quantity. Operating hours per station; slot inventory per window (e.g. 10 kayaks 10-11 and 11-12, then 5 at 12-1). *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-748)*

`BO-517` Timeslot & Duration Availability Setup

- Per-item availability rules: minimum advance booking time, maximum advance window, last-minute cutoff, same-day booking allowed, min/max booking quantity. Operating hours per station; slot inventory per window (e.g. 10 kayaks 10-11 and 11-12, then 5 at 12-1). *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-748)*

`BO-518` Real-Time Availability Calendar

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Real-time availability view shows total, available, rented and returned inventory per item and per location, alongside revenue generated. *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-747)*

`BO-519` Resource / Equipment Calendar

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Resource/equipment calendar shows a visual booking timeline per item across the day; blockout dates; overlap/conflict validation prevents double-booking before publish; holds/buffers per channel (online, POS, B2B) with release rules; demand forecast visual. *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-749)*

`BO-520` Blackout, Closure & Capacity Blocking

- Resource/equipment calendar shows a visual booking timeline per item across the day; blockout dates; overlap/conflict validation prevents double-booking before publish; holds/buffers per channel (online, POS, B2B) with release rules; demand forecast visual. *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-749)*

`BO-521` Overlap & Conflict Engine

- Resource/equipment calendar shows a visual booking timeline per item across the day; blockout dates; overlap/conflict validation prevents double-booking before publish; holds/buffers per channel (online, POS, B2B) with release rules; demand forecast visual. *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-749)*

`BO-522` Inventory Holds, Buffers & Release Rules

- Resource/equipment calendar shows a visual booking timeline per item across the day; blockout dates; overlap/conflict validation prevents double-booking before publish; holds/buffers per channel (online, POS, B2B) with release rules; demand forecast visual. *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-749)*

`BO-523` Availability Intelligence & AI Forecasting

- Resource/equipment calendar shows a visual booking timeline per item across the day; blockout dates; overlap/conflict validation prevents double-booking before publish; holds/buffers per channel (online, POS, B2B) with release rules; demand forecast visual. *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-749)*

`BO-524` Rental Pricing Command Center

- Rental pricing: fixed and dynamic models; top-products-by-revenue view; pricing profile valid across a date range, optionally restricted to channels; tiered duration pricing (30/60/90 min at falling per-minute rates); weekday/weekend and peak pricing; demand-based pricing within min/max bounds. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-751)*

`BO-525` Pricing Profile Builder

- Rental pricing: fixed and dynamic models; top-products-by-revenue view; pricing profile valid across a date range, optionally restricted to channels; tiered duration pricing (30/60/90 min at falling per-minute rates); weekday/weekend and peak pricing; demand-based pricing within min/max bounds. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-751)*

`BO-526` Duration & Tiered Pricing Configuration

- Rental pricing: fixed and dynamic models; top-products-by-revenue view; pricing profile valid across a date range, optionally restricted to channels; tiered duration pricing (30/60/90 min at falling per-minute rates); weekday/weekend and peak pricing; demand-based pricing within min/max bounds. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-751)*

`BO-527` Calendar, Peak & Seasonal Pricing

- Rental pricing: fixed and dynamic models; top-products-by-revenue view; pricing profile valid across a date range, optionally restricted to channels; tiered duration pricing (30/60/90 min at falling per-minute rates); weekday/weekend and peak pricing; demand-based pricing within min/max bounds. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-751)*

`BO-528` Dynamic Pricing & AI Recommendation

- Rental pricing: fixed and dynamic models; top-products-by-revenue view; pricing profile valid across a date range, optionally restricted to channels; tiered duration pricing (30/60/90 min at falling per-minute rates); weekday/weekend and peak pricing; demand-based pricing within min/max bounds. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-751)*

`BO-529` Deposit & Security Hold Policy

- Refundable deposit (fixed amount or %), payable by cash or card per business policy; auto-release on return; partial capture (deduct damage charge, refund remainder). *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-752)*

`BO-530` Deposit Lifecycle & Settlement Rules

- Refundable deposit (fixed amount or %), payable by cash or card per business policy; auto-release on return; partial capture (deduct damage charge, refund remainder). *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-752)*

`BO-531` Late Fee, Grace Period & Extension Pricing

- Late fee, grace period and extension pricing; fee waiver full or partial (amount or %), e.g. when equipment malfunctioned through no fault of the customer; a simulation tests pricing/deposit rules before publishing. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-753)*

`BO-532` Commercial Exceptions, Waivers & Overrides

- Late fee, grace period and extension pricing; fee waiver full or partial (amount or %), e.g. when equipment malfunctioned through no fault of the customer; a simulation tests pricing/deposit rules before publishing. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-753)*

`BO-533` Pricing Simulation, Validation & AI Commercial Intelligence

- Late fee, grace period and extension pricing; fee waiver full or partial (amount or %), e.g. when equipment malfunctioned through no fault of the customer; a simulation tests pricing/deposit rules before publishing. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-753)*

`BO-534` Rental Booking Command Center

- Bookings made by staff at the rental station or by the customer online use the same flow; booking dashboard shows total reservations, upcoming rentals, items awaiting arrival (online bookings not yet collected) and checked-out items. *(client request · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-754)*

`BO-535` New Rental Booking Wizard

- Bookings made by staff at the rental station or by the customer online use the same flow; booking dashboard shows total reservations, upcoming rentals, items awaiting arrival (online bookings not yet collected) and checked-out items. *(client request · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-754)*

`BO-537` Customer & Participant Information

- Group rental (e.g. 10 people on bicycles): capture each member's details and assign an item to each, tracked as one linked group booking, with a group waiver all members sign. *(client request · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-755)*
- Eligibility rules: required documentation (e.g. Emirates ID collected and returned with the item), age restrictions, and which customer-profile fields must be captured at rental time. *(client request · MoM 9 Sep 2026, 4.2 Rental Location, Duration & Eligibility Rules · DI-742)*

`BO-538` Group Rental & Participant Management

- Group rental (e.g. 10 people on bicycles): capture each member's details and assign an item to each, tracked as one linked group booking, with a group waiver all members sign. *(client request · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-755)*

`BO-539` Rental Agreement & Waiver Completion

- **Open question.** Group waivers need a digital signature-capture device (stylus pad); Chinmay says a USB signature pad should integrate. Hardware reference pending from Qossai. *(open · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-756)*
- Group rental (e.g. 10 people on bicycles): capture each member's details and assign an item to each, tracked as one linked group booking, with a group waiver all members sign. *(client request · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-755)*

`BO-540` Booking Commercial Summary & Payment

- Commercial summary shows all charges (including deposit) before payment; once paid the booking is confirmed with a QR code sent by email or other channel; bookings can be amended; reservation timeline shows products, timing, amounts paid and deposit status. *(client request · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-757)*

`BO-541` Reservation Confirmation & QR Voucher

- Commercial summary shows all charges (including deposit) before payment; once paid the booking is confirmed with a QR code sent by email or other channel; bookings can be amended; reservation timeline shows products, timing, amounts paid and deposit status. *(client request · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-757)*

`BO-542` Reservation Modification, Cancellation & No-Show

- Commercial summary shows all charges (including deposit) before payment; once paid the booking is confirmed with a QR code sent by email or other channel; bookings can be amended; reservation timeline shows products, timing, amounts paid and deposit status. *(client request · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-757)*

`BO-543` Reservation Detail, Timeline & Readiness

- Commercial summary shows all charges (including deposit) before payment; once paid the booking is confirmed with a QR code sent by email or other channel; bookings can be amended; reservation timeline shows products, timing, amounts paid and deposit status. *(client request · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-757)*

`BO-544` Rental Checkout Command Center

- Checkout screen shows bookings by status (in progress, checked out) and lets staff scan a QR code to pull up a reservation. *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-758)*

`BO-545` Voucher Scan & Reservation Retrieval

- Checkout screen shows bookings by status (in progress, checked out) and lets staff scan a QR code to pull up a reservation. *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-758)*

`BO-546` Checkout Readiness Validation

- Before handover: readiness validation (reservation, payment, inventory), a pre-rental condition checklist (e.g. bicycle brakes and tyres working) and a safety handover checklist (e.g. helmet with a bicycle). *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-759)*

`BO-547` Equipment Assignment Workspace

- Serialized items: staff assign the specific unit (e.g. bicycle #121) at checkout by scanning its QR code or selecting it manually from available units. Multi-item checkout hands a whole group's items (e.g. 10 bicycles) out in a single action. *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-760)*

`BO-548` Equipment Scan & Validation

- Serialized items: staff assign the specific unit (e.g. bicycle #121) at checkout by scanning its QR code or selecting it manually from available units. Multi-item checkout hands a whole group's items (e.g. 10 bicycles) out in a single action. *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-760)*

`BO-549` Pre-Rental Condition Inspection

- Before handover: readiness validation (reservation, payment, inventory), a pre-rental condition checklist (e.g. bicycle brakes and tyres working) and a safety handover checklist (e.g. helmet with a bicycle). *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-759)*

`BO-550` Safety & Handover Checklist

- Before handover: readiness validation (reservation, payment, inventory), a pre-rental condition checklist (e.g. bicycle brakes and tyres working) and a safety handover checklist (e.g. helmet with a bicycle). *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-759)*

`BO-551` Deposit & Financial Handover Validation

- Refundable deposit (fixed amount or %), payable by cash or card per business policy; auto-release on return; partial capture (deduct damage charge, refund remainder). *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-752)*

`BO-552` Group & Multi-Item Checkout

- Serialized items: staff assign the specific unit (e.g. bicycle #121) at checkout by scanning its QR code or selecting it manually from available units. Multi-item checkout hands a whole group's items (e.g. 10 bicycles) out in a single action. *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-760)*

`BO-554` Active Rental Operations Command Center

- Active operations view tracks all rented items and durations in real time; rental detail timeline shows booking time, handover time and expected return time per item, with extension requests and extension pricing. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-761)*

`BO-555` Active Rental Detail & Live Timeline

- Active operations view tracks all rented items and durations in real time; rental detail timeline shows booking time, handover time and expected return time per item, with extension requests and extension pricing. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-761)*

`BO-556` Rental Extension Request

- Active operations view tracks all rented items and durations in real time; rental detail timeline shows booking time, handover time and expected return time per item, with extension requests and extension pricing. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-761)*

`BO-557` Extension Pricing & Confirmation

- Active operations view tracks all rented items and durations in real time; rental detail timeline shows booking time, handover time and expected return time per item, with extension requests and extension pricing. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-761)*

`BO-558` Equipment Swap / Replacement

- Equipment swap assigns the replacement to the booking. Swap within a short threshold (e.g. 5 minutes) restarts the timer; a later swap (e.g. 15 minutes into 30) lets the operator grant that booking only a free time extension/buffer. *(agreed · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-762)*

`BO-559` Rental Incident & Operational Exception

- Incidents (e.g. reported brake malfunction) are logged against the booking; automatic SMS/app return reminders to the customer. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-763)*

`BO-560` Due Soon & Customer Notification Management

- Incidents (e.g. reported brake malfunction) are logged against the booking; automatic SMS/app return reminders to the customer. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-763)*

`BO-561` Overdue Rental Management

- Overdue tracking flags bookings past expected return and applies configured overdue pricing; a group / multi-item active-rental view and an intelligence panel (utilisation, incident trends) complete the board. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-764)*

`BO-562` Active Group Rental Management

- Overdue tracking flags bookings past expected return and applies configured overdue pricing; a group / multi-item active-rental view and an intelligence panel (utilisation, incident trends) complete the board. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-764)*

`BO-563` Active Rental Intelligence & Operational Alerts

- Overdue tracking flags bookings past expected return and applies configured overdue pricing; a group / multi-item active-rental view and an intelligence panel (utilisation, incident trends) complete the board. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-764)*

`BO-565` Return Scan & Rental Retrieval

- Return: staff scan or search a booking; late fee is calculated automatically from actual vs booked duration. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-765)*

`BO-566` Return Summary & Actual Return Time

- Return: staff scan or search a booking; late fee is calculated automatically from actual vs booked duration. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-765)*

`BO-567` Post-Rental Condition Inspection

- Post-rental condition inspection, with before/after photo capture that is optional, not mandatory. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-766)*

`BO-568` Before vs After Condition Comparison

- Post-rental condition inspection, with before/after photo capture that is optional, not mandatory. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-766)*

`BO-569` Damage Assessment & Charge Workflow

- Damage assessment; partial group returns (e.g. 8 of 10 bicycles back, 2 outstanding); late fees, damage fees and final settlement calculated together before deposit release (individual or group); ends with a rental completion report. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-767)*

`BO-570` Partial Return & Missing Equipment

- Damage assessment; partial group returns (e.g. 8 of 10 bicycles back, 2 outstanding); late fees, damage fees and final settlement calculated together before deposit release (individual or group); ends with a rental completion report. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-767)*

`BO-571` Late Fees, Damage Fees & Final Settlement

- Damage assessment; partial group returns (e.g. 8 of 10 bicycles back, 2 outstanding); late fees, damage fees and final settlement calculated together before deposit release (individual or group); ends with a rental completion report. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-767)*

`BO-572` Deposit Release, Capture & Customer Confirmation

- Damage assessment; partial group returns (e.g. 8 of 10 bicycles back, 2 outstanding); late fees, damage fees and final settlement calculated together before deposit release (individual or group); ends with a rental completion report. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-767)*
- Refundable deposit (fixed amount or %), payable by cash or card per business policy; auto-release on return; partial capture (deduct damage charge, refund remainder). *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-752)*

`BO-573` Return Completion & Equipment Disposition

- Damage assessment; partial group returns (e.g. 8 of 10 bicycles back, 2 outstanding); late fees, damage fees and final settlement calculated together before deposit release (individual or group); ends with a rental completion report. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-767)*

`BO-575` Maintenance Rule & Service Plan Configuration

- Preventive maintenance schedules (e.g. every 30 or 60 days) and periodic counts that flag shortages (e.g. 500 life jackets last month vs 495 this month). *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-768)*

`BO-576` Maintenance Calendar & Scheduling

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Calendars must support filtering by asset category so a team only sees maintenance relevant to them, e.g. an IT team sees turnstiles, printers and POS terminals, not unrelated categories. *(agreed · MoM 17 Sep 2026, 4.2 Preventive Maintenance Planning · DI-908)*
- Preventive maintenance schedules (e.g. every 30 or 60 days) and periodic counts that flag shortages (e.g. 500 life jackets last month vs 495 this month). *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-768)*

`BO-577` Maintenance Work Order

- Smart assignment (confirmed by the maintenance head): technicians ranked by skill, shift and load; the ranking assigns nothing and Assign on a row does; outside vendor requests listed on the work order. *(agreed · MoM 17 Sep 2026, M17-13 · DI-924)*
- Work-order priority is shown with its source side by side (scored by venue policy, asset override, or manual); an asset carries a "fault priority override"; a new work order leaves priority empty to be scored; the venue sets weights and bands (safety, guest operations, revenue, asset criticality, summing to 100). *(agreed · MoM 17 Sep 2026, M17-01 · DI-923)*
- Maintenance work orders are assigned to the relevant department/person and are visible on the staff mobile app; repair workspace tracks cost; annual maintenance history shows lifecycle cost per item. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-769)*

`BO-578` Technician Repair Workspace

- Maintenance work orders are assigned to the relevant department/person and are visible on the staff mobile app; repair workspace tracks cost; annual maintenance history shows lifecycle cost per item. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-769)*

`BO-579` Parts, Cost & Maintenance Expense Tracking

- Work-order parts are reserved in the general inventory; the reserve action is hidden offline, and a refusal for short stock names the part. *(agreed · MoM 17 Sep 2026, M17-02 · DI-925)*
- Maintenance work orders are assigned to the relevant department/person and are visible on the staff mobile app; repair workspace tracks cost; annual maintenance history shows lifecycle cost per item. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-769)*

`BO-580` Asset Maintenance History & Lifecycle

- Maintenance work orders are assigned to the relevant department/person and are visible on the staff mobile app; repair workspace tracks cost; annual maintenance history shows lifecycle cost per item. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-769)*

`BO-581` Return-to-Service Inspection & Approval

- Serviced items return to service; retirement/write-off records the write-off value; maintenance AI view shows at-risk assets, upcoming maintenance cost and total spend. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-770)*

`BO-582` Asset Retirement, Write-Off & Replacement Recommendation

- Serviced items return to service; retirement/write-off records the write-off value; maintenance AI view shows at-risk assets, upcoming maintenance cost and total spend. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-770)*

`BO-583` Maintenance Intelligence & Predictive AI

- In rentals AI's practical role is reporting and maintenance-scheduling recommendations; day-to-day rental operations stay staff-managed. *(agreed · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-772)*
- Serviced items return to service; retirement/write-off records the write-off value; maintenance AI view shows at-risk assets, upcoming maintenance cost and total spend. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-770)*

`BO-584` Rental Executive Command Center

- Rental command centre KPIs: realised revenue, total rentals, average utilisation, on-time return rate, damage rate, maintenance trends; further views for product performance, utilisation, equipment performance, duration/extension, damage/loss/deposit, channel/location and demand forecast. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-771)*

`BO-585` Rental Revenue & Commercial Analytics

- Rental command centre KPIs: realised revenue, total rentals, average utilisation, on-time return rate, damage rate, maintenance trends; further views for product performance, utilisation, equipment performance, duration/extension, damage/loss/deposit, channel/location and demand forecast. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-771)*

`BO-586` Utilization & Capacity Analytics

- Rental command centre KPIs: realised revenue, total rentals, average utilisation, on-time return rate, damage rate, maintenance trends; further views for product performance, utilisation, equipment performance, duration/extension, damage/loss/deposit, channel/location and demand forecast. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-771)*

`BO-587` Inventory & Equipment Performance Analytics

- Rental command centre KPIs: realised revenue, total rentals, average utilisation, on-time return rate, damage rate, maintenance trends; further views for product performance, utilisation, equipment performance, duration/extension, damage/loss/deposit, channel/location and demand forecast. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-771)*

`BO-588` Rental Duration, Extension & Return Analytics

- Rental command centre KPIs: realised revenue, total rentals, average utilisation, on-time return rate, damage rate, maintenance trends; further views for product performance, utilisation, equipment performance, duration/extension, damage/loss/deposit, channel/location and demand forecast. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-771)*

`BO-589` Damage, Loss, Deposit & Exception Analytics

- Rental command centre KPIs: realised revenue, total rentals, average utilisation, on-time return rate, damage rate, maintenance trends; further views for product performance, utilisation, equipment performance, duration/extension, damage/loss/deposit, channel/location and demand forecast. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-771)*

`BO-590` Location & Channel Performance

- Rental command centre KPIs: realised revenue, total rentals, average utilisation, on-time return rate, damage rate, maintenance trends; further views for product performance, utilisation, equipment performance, duration/extension, damage/loss/deposit, channel/location and demand forecast. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-771)*

`BO-591` Rental Forecasting & Demand Intelligence

- Rental command centre KPIs: realised revenue, total rentals, average utilisation, on-time return rate, damage rate, maintenance trends; further views for product performance, utilisation, equipment performance, duration/extension, damage/loss/deposit, channel/location and demand forecast. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-771)*

`BO-593` AI Rental Management Copilot & Action Center

- In rentals AI's practical role is reporting and maintenance-scheduling recommendations; day-to-day rental operations stay staff-managed. *(agreed · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-772)*

`BO-597` AI Configuration Workspace

- Phase-one AI priority is a conversational configuration assistant: the admin says e.g. "I want to configure a new product" and it asks the product type (admission, time slot, etc.) and walks through product/promotion setup. *(agreed · MoM 14 Aug 2026, 1. AI Configuration Assistant — Phase-One Scope · DI-279)*

`BO-598` AI Draft Review & Approval

- AI actions in progress are shown step by step in an AI action command center; if a process only partly completes (e.g. missing information) it rolls back rather than leaving a product half-configured, and a full change history records everything AI modified. *(client request · MoM 21 Sep 2026, 4.9 Core AI Platform — AI Tools, Agents & Action Orchestration · DI-965)*

`BO-615` Accreditation Command Center

- Accreditation: applicant fills a customisable form, goes through approval (with documents), and receives a credential (photo badge, QR or RFID) for event access. Dashboard shows total registered, pending review and expired documents; directory searches applications by name, company or business info. *(client request · MoM 7 Sep 2026, 4.1 Accreditation Overview & Application Directory · DI-654)*

`BO-616` Accreditation Application Directory

- Accreditation: applicant fills a customisable form, goes through approval (with documents), and receives a credential (photo badge, QR or RFID) for event access. Dashboard shows total registered, pending review and expired documents; directory searches applications by name, company or business info. *(client request · MoM 7 Sep 2026, 4.1 Accreditation Overview & Application Directory · DI-654)*

`BO-617` New Accreditation Application

- The venue creates a partner/company account (main or sub-accounts) whose users log in and submit accreditation for their members; entry can be done by the end user or by the admin team on their behalf. *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-655)*

`BO-618` Accreditation Form Builder

- Drag-and-drop form builder sets exactly which fields each form collects; categories (media, corporate, individual guest) each have their own form; programmes link a category to an event, venue or season; a requirement matrix sets documents per category (e.g. contractors need company authorisation). *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-656)*

`BO-619` Accreditation Category Management

- Drag-and-drop form builder sets exactly which fields each form collects; categories (media, corporate, individual guest) each have their own form; programmes link a category to an event, venue or season; a requirement matrix sets documents per category (e.g. contractors need company authorisation). *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-656)*

`BO-620` Accreditation Program Setup

- Drag-and-drop form builder sets exactly which fields each form collects; categories (media, corporate, individual guest) each have their own form; programmes link a category to an event, venue or season; a requirement matrix sets documents per category (e.g. contractors need company authorisation). *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-656)*

`BO-621` Applicant Type Configuration

- Drag-and-drop form builder sets exactly which fields each form collects; categories (media, corporate, individual guest) each have their own form; programmes link a category to an event, venue or season; a requirement matrix sets documents per category (e.g. contractors need company authorisation). *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-656)*

`BO-622` Application Requirements Matrix

- Drag-and-drop form builder sets exactly which fields each form collects; categories (media, corporate, individual guest) each have their own form; programmes link a category to an event, venue or season; a requirement matrix sets documents per category (e.g. contractors need company authorisation). *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-656)*

`BO-623` Accreditation Intake Monitor

- Submission tracking shows submitted, pending and missing-document applications. Upload accepts PDF, JPEG, PNG and enforces file-size/quality limits at upload time. *(client request · MoM 7 Sep 2026, 4.3 Application Requirements, Document Validation & OCR Auto-Fill · DI-657)*

`BO-625` Accreditation Holder Directory

- Accreditation-holder monitoring is a filtered view inside the general entitlement monitoring, not a separate platform, so staff can quickly distinguish and support large accredited groups. *(agreed · MoM 7 Sep 2026, 4.10 Entitlements Lifecycle, Consumption Monitoring & Screen Consolidation · DI-672)*

`BO-626` Accreditation Holder Profile

- Staff open an application to review the photo and all details and verify documents are correct, legible and valid. Duplicate passport/Emirates ID numbers are blocked, prompting the applicant to resolve or resubmit rather than silently creating a duplicate. *(agreed · MoM 7 Sep 2026, 4.4 Accreditation Profile, Identity Verification & Duplicate Prevention · DI-659)*

`BO-627` Identity Details & Verification

- Staff open an application to review the photo and all details and verify documents are correct, legible and valid. Duplicate passport/Emirates ID numbers are blocked, prompting the applicant to resolve or resubmit rather than silently creating a duplicate. *(agreed · MoM 7 Sep 2026, 4.4 Accreditation Profile, Identity Verification & Duplicate Prevention · DI-659)*
- Allam asked, Chinmay confirmed: uploading an ID (e.g. Emirates ID image or PDF from phone or laptop) auto-fills form fields (ID number, expiry) via OCR; data is stored as structured fields to track expiry and prompt renewal. *(agreed · MoM 7 Sep 2026, 4.3 OCR Auto-Fill / 5. Key Decisions · DI-658)*

`BO-629` Document Repository

- Allam asked, Chinmay confirmed: uploading an ID (e.g. Emirates ID image or PDF from phone or laptop) auto-fills form fields (ID number, expiry) via OCR; data is stored as structured fields to track expiry and prompt renewal. *(agreed · MoM 7 Sep 2026, 4.3 OCR Auto-Fill / 5. Key Decisions · DI-658)*

`BO-631` Duplicate & Identity Conflict Detection

- Staff open an application to review the photo and all details and verify documents are correct, legible and valid. Duplicate passport/Emirates ID numbers are blocked, prompting the applicant to resolve or resubmit rather than silently creating a duplicate. *(agreed · MoM 7 Sep 2026, 4.4 Accreditation Profile, Identity Verification & Duplicate Prevention · DI-659)*
- Duplicate-profile detection and merge (common because of name transliteration variants) merging two profiles with their combined transaction history; account activate/deactivate. *(agreed · MoM 7 Aug 2026, 19. Maintenance Tools · DI-176)*

`BO-632` Organization & Affiliation Management

- A main account holder (company/agent) sees the status of every application under their organisation (approved, rejected, requires resubmission), whether the credential is collected physically or sent as a soft copy by email. *(client request · MoM 7 Sep 2026, 4.4 Accreditation Profile, Identity Verification & Duplicate Prevention · DI-660)*
- The venue creates a partner/company account (main or sub-accounts) whose users log in and submit accreditation for their members; entry can be done by the end user or by the admin team on their behalf. *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-655)*

`BO-635` Accreditation Review Queue

- Multi-level approval chains per category (e.g. government vs private/corporate/media); SLA turnaround per category with alerts as backlog builds (e.g. pending media passes); auto-escalation when unactioned. *(client request · MoM 7 Sep 2026, 4.5 Approval Workflow, SLA & Escalations · DI-661)*

`BO-637` Approval Workflow Builder

- Multi-level approval chains per category (e.g. government vs private/corporate/media); SLA turnaround per category with alerts as backlog builds (e.g. pending media passes); auto-escalation when unactioned. *(client request · MoM 7 Sep 2026, 4.5 Approval Workflow, SLA & Escalations · DI-661)*

`BO-638` Approval Rules & Conditions

- Multi-level approval chains per category (e.g. government vs private/corporate/media); SLA turnaround per category with alerts as backlog builds (e.g. pending media passes); auto-escalation when unactioned. *(client request · MoM 7 Sep 2026, 4.5 Approval Workflow, SLA & Escalations · DI-661)*

`BO-641` Escalation & Exception Management

- Multi-level approval chains per category (e.g. government vs private/corporate/media); SLA turnaround per category with alerts as backlog builds (e.g. pending media passes); auto-escalation when unactioned. *(client request · MoM 7 Sep 2026, 4.5 Approval Workflow, SLA & Escalations · DI-661)*

`BO-645` Credential Generation Workspace

- Approved credential: printed photo badge, QR or RFID depending on the event's configured media; collected physically or delivered digitally to a mobile device. Access rights set zones per category (media all zones; corporate limited). *(client request · MoM 7 Sep 2026, 4.6 Credential Issuance, Access Rights & Lifecycle Management · DI-662)*

`BO-647` Badge Template Designer

- Approved credential: printed photo badge, QR or RFID depending on the event's configured media; collected physically or delivered digitally to a mobile device. Access rights set zones per category (media all zones; corporate limited). *(client request · MoM 7 Sep 2026, 4.6 Credential Issuance, Access Rights & Lifecycle Management · DI-662)*

`BO-648` Badge Printing & Print Queue

- Approved credential: printed photo badge, QR or RFID depending on the event's configured media; collected physically or delivered digitally to a mobile device. Access rights set zones per category (media all zones; corporate limited). *(client request · MoM 7 Sep 2026, 4.6 Credential Issuance, Access Rights & Lifecycle Management · DI-662)*

`BO-649` Digital & Mobile Credential Management

- Approved credential: printed photo badge, QR or RFID depending on the event's configured media; collected physically or delivered digitally to a mobile device. Access rights set zones per category (media all zones; corporate limited). *(client request · MoM 7 Sep 2026, 4.6 Credential Issuance, Access Rights & Lifecycle Management · DI-662)*

`BO-654` Accreditation Access Command Center

- Accreditation-holder monitoring is a filtered view inside the general entitlement monitoring, not a separate platform, so staff can quickly distinguish and support large accredited groups. *(agreed · MoM 7 Sep 2026, 4.10 Entitlements Lifecycle, Consumption Monitoring & Screen Consolidation · DI-672)*

`BO-656` Venue & Zone Access Matrix

- Approved credential: printed photo badge, QR or RFID depending on the event's configured media; collected physically or delivered digitally to a mobile device. Access rights set zones per category (media all zones; corporate limited). *(client request · MoM 7 Sep 2026, 4.6 Credential Issuance, Access Rights & Lifecycle Management · DI-662)*

`BO-664` Accreditation Lifecycle Command Center

- Lifecycle: activation, expiry, renewal, suspension; if a document (e.g. Emirates ID) expires before the event, a resubmission request is raised and the credential is blocked if unresolved. Applicants are notified at each status change (approved, rejected, needs validation). *(client request · MoM 7 Sep 2026, 4.6 / 4.7 Lifecycle & Notifications · DI-663)*

`BO-673` Accreditation Renewal Workspace

- Lifecycle: activation, expiry, renewal, suspension; if a document (e.g. Emirates ID) expires before the event, a resubmission request is raised and the credential is blocked if unresolved. Applicants are notified at each status change (approved, rejected, needs validation). *(client request · MoM 7 Sep 2026, 4.6 / 4.7 Lifecycle & Notifications · DI-663)*

`BO-675` Notification Rule Management

- Lifecycle: activation, expiry, renewal, suspension; if a document (e.g. Emirates ID) expires before the event, a resubmission request is raised and the credential is blocked if unresolved. Applicants are notified at each status change (approved, rejected, needs validation). *(client request · MoM 7 Sep 2026, 4.6 / 4.7 Lifecycle & Notifications · DI-663)*

`BO-680` Accreditation Bulk Import

- Bulk: a company with many members (e.g. 1,000) gets an Excel template to submit all details and documents at once; each imported record still goes through profile, documents and approval. *(client request · MoM 7 Sep 2026, 4.7 Notifications, Bulk Operations & Analytics · DI-664)*

`BO-684` Accreditation Executive Dashboard

- Accreditation analytics: approvals, upcoming expiries, per-category detail, attended vs issued (e.g. 1,000 passes issued, 700 scanned), and year-over-year or venue-over-venue comparisons. *(client request · MoM 7 Sep 2026, 4.7 Notifications, Bulk Operations & Analytics · DI-665)*

`BO-685` Accreditation Status & Portfolio Reporting

- Accreditation analytics: approvals, upcoming expiries, per-category detail, attended vs issued (e.g. 1,000 passes issued, 700 scanned), and year-over-year or venue-over-venue comparisons. *(client request · MoM 7 Sep 2026, 4.7 Notifications, Bulk Operations & Analytics · DI-665)*

`BO-686` Accreditation Utilization Analytics

- Accreditation analytics: approvals, upcoming expiries, per-category detail, attended vs issued (e.g. 1,000 passes issued, 700 scanned), and year-over-year or venue-over-venue comparisons. *(client request · MoM 7 Sep 2026, 4.7 Notifications, Bulk Operations & Analytics · DI-665)*

`BO-688` Accreditation Trend & Comparative Analysis

- Accreditation analytics: approvals, upcoming expiries, per-category detail, attended vs issued (e.g. 1,000 passes issued, 700 scanned), and year-over-year or venue-over-venue comparisons. *(client request · MoM 7 Sep 2026, 4.7 Notifications, Bulk Operations & Analytics · DI-665)*

`BO-695` Event Type & Behaviour Configuration

- Event ticket setup: validity window; recurring performances; admission model (general admission, capacity control, reserved seating, resource control, none); seat map, section and quota per sales channel (shared pool or split); resources (e.g. vehicle + driver for a desert safari) checked for availability before sale. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-436)*

`BO-697` Event Schedule Command Center

- AI suggestions from sales forecasts: add/remove time slots, merge under-sold adjacent slots (with guest notification of the time change), and dynamic pricing (raise when a slot is >~80% sold, lower when <~20–30%). *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-454)*

`BO-704` Event Capacity Profile Configuration

- Decision: venue-level admission capacity supersedes event-level capacity; a system prompt/validation prevents configuring or selling an event beyond the remaining venue capacity. Overriding is an authorisation-gated (RBAC) action for authorised users only. *(agreed · MoM 25 Aug 2026, 4.6 Performances & Capacity Management; 5. Key Decisions · DI-456)*
- Performances are created individually or from a reusable time-slot template (e.g. every 30 minutes between start and end) that auto-generates the schedule. Capacity set at event level is inherited by performances, with per-performance override (e.g. evening slots). *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-453)*
- Event ticket setup: validity window; recurring performances; admission model (general admission, capacity control, reserved seating, resource control, none); seat map, section and quota per sales channel (shared pool or split); resources (e.g. vehicle + driver for a desert safari) checked for availability before sale. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-436)*

`BO-705` Seating Mode & Reservation Configuration

- Event ticket setup: validity window; recurring performances; admission model (general admission, capacity control, reserved seating, resource control, none); seat map, section and quota per sales channel (shared pool or split); resources (e.g. vehicle + driver for a desert safari) checked for availability before sale. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-436)*
- Decision: three seat-selection models, selectable per section, per event: (1) zone/capacity selling with no seat numbers (guest told zone only); (2) system-assigned "best available" — guest picks section + quantity, seats disclosed later; (3) full customer seat selection. *(agreed · MoM 21 Aug 2026, 4.1 Reference Walkthrough; 4.2 Seat Map Builder; 5. Key Decisions · DI-410)*

`BO-711` Event Resource Requirement Configuration

- Decision: two assignment models — pre-assigned (named vehicle/instructor/room mapped to a time slot in advance) and dynamic (only type + quantity, e.g. "one SUV and one guide", with an available resource auto-assigned at sale). *(agreed · MoM 26 Aug 2026, 4.4 Resource Assignment Models; 5. Key Decisions · DI-482)*
- Event ticket setup: validity window; recurring performances; admission model (general admission, capacity control, reserved seating, resource control, none); seat map, section and quota per sales channel (shared pool or split); resources (e.g. vehicle + driver for a desert safari) checked for availability before sale. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-436)*

`BO-721` Activity Performance & Slot Template Configuration

- Clarified: time slots are not created for resources; they are created for performances/events, and resources are associated with those performance time slots. *(agreed · MoM 26 Aug 2026, 4.3 Resource Calendar & Scheduling · DI-481)*
- Performances are created individually or from a reusable time-slot template (e.g. every 30 minutes between start and end) that auto-generates the schedule. Capacity set at event level is inherited by performances, with per-performance override (e.g. evening slots). *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-453)*
- Performance (time-slot) creation: date range with chosen weekdays or all days, start/end time, slot duration (e.g. 30 or 60 min), "minutes on screen" (e.g. a 10:00 slot sellable at POS until 10:10), separate entry window (e.g. from 9:30, cut-off 10:20), and an on-sale date range; bulk creation across a date range. *(agreed · MoM 7 Aug 2026, 14. Events, Integrations & Performances (Time Slots) · DI-167)*

`BO-725` Performance Operations Command Center

- Performance capacity is edited individually or by multi-select bulk edit; a performance can be suspended, resumed (any time before start) or cancelled — a state change, never a delete. *(agreed · MoM 7 Aug 2026, 14. Events, Integrations & Performances (Time Slots) · DI-168)*

`BO-727` F&B Command Center

- F&B Command Center gives a real-time consolidated view across all outlets: total sales, orders, average order value, average preparation time, kitchen load, top-selling items, operational alerts, food cost and gross margin, with breakdowns by sales channel and by hour. *(client request · MoM 18 Aug 2026, 4.1 F&B Command Center — Overview & Outlet Setup; 4.10 F&B Stock, Wastage & Requisitions · DI-317)*

`BO-728` Outlet Management

- Retail store setup reuses the F&B department/venue/zone structure with department type "Retail" and the shop as a sub-department; retail needs no sub-classification (unlike fine dining vs. QSR) since operations are scan-and-sell. Inventory stays outlet-level. *(agreed · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-350)*
- Outlets are categorised by type (fine dining, quick service, coffee, etc.), each type switching features on or off — e.g. quick-service outlets need no table booking, fine-dining outlets need a table layout. Each outlet is linked to a department (Food & Beverage), sub-department (outlet name), cost centre and status. *(client request · MoM 18 Aug 2026, 4.1 F&B Command Center — Overview & Outlet Setup · DI-319)*

`BO-729` Create / Edit Outlet

- Retail store setup reuses the F&B department/venue/zone structure with department type "Retail" and the shop as a sub-department; retail needs no sub-classification (unlike fine dining vs. QSR) since operations are scan-and-sell. Inventory stays outlet-level. *(agreed · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-350)*
- Operating hours and service periods (breakfast, lunch, dinner, late night) are defined per outlet so revenue can be analysed by time slot. Recipe-based stock depletion is set per outlet, real-time or end-of-day, by outlet type. *(client request · MoM 18 Aug 2026, 4.2 Recipes, Operating Hours & Service Channels · DI-320)*
- Outlets are categorised by type (fine dining, quick service, coffee, etc.), each type switching features on or off — e.g. quick-service outlets need no table booking, fine-dining outlets need a table layout. Each outlet is linked to a department (Food & Beverage), sub-department (outlet name), cost centre and status. *(client request · MoM 18 Aug 2026, 4.1 F&B Command Center — Overview & Outlet Setup · DI-319)*

`BO-730` Outlet Types & Templates

- Outlets are categorised by type (fine dining, quick service, coffee, etc.), each type switching features on or off — e.g. quick-service outlets need no table booking, fine-dining outlets need a table layout. Each outlet is linked to a department (Food & Beverage), sub-department (outlet name), cost centre and status. *(client request · MoM 18 Aug 2026, 4.1 F&B Command Center — Overview & Outlet Setup · DI-319)*

`BO-731` Operating Hours & Service Periods

- Operating hours and service periods (breakfast, lunch, dinner, late night) are defined per outlet so revenue can be analysed by time slot. Recipe-based stock depletion is set per outlet, real-time or end-of-day, by outlet type. *(client request · MoM 18 Aug 2026, 4.2 Recipes, Operating Hours & Service Channels · DI-320)*

`BO-732` POS & Device Assignment

- Device directory: search and add devices (printers, scanners, customer displays, cash drawers, turnstiles, handhelds, mobile POS) capturing serial number, type and model; adding generates a secure enrolment code; devices are assigned to workstations (e.g. A has ticket printer, receipt printer and cash drawer). *(client request · MoM 15 Sep 2026, 4.3 Device Management - Registration, Enrollment & Workstation Assignment · DI-892)*
- Retail POS/device assignment covers workstation name/code, receipt printer, barcode scanner and cash drawer; global retail settings include sales channels, primary/replenishment store and offline sales support. *(client request · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-352)*
- POS & device management configures receipt printers, kitchen printers and KDS devices per outlet/terminal. *(client request · MoM 18 Aug 2026, 4.2 Recipes, Operating Hours & Service Channels · DI-321)*

`BO-733` Service Channel Configuration

- Service channel configuration enables/disables specific items per sales channel (POS, kiosk, QR ordering, online) per outlet. *(client request · MoM 18 Aug 2026, 4.2 Recipes, Operating Hours & Service Channels · DI-322)*

`BO-734` CRM Command Center

- CRM guest dashboard shows active/inactive/duplicate profile counts and lifetime value, plus guest directory/search and segmentation by source (individual, corporate, group, travel agent, OTA). *(client request · MoM 20 Aug 2026, 4.1 CRM — Customer Profiles, Unique Fields & Family/Guardian Linking · DI-370)*

`BO-735` Guest Directory

- CRM guest dashboard shows active/inactive/duplicate profile counts and lifetime value, plus guest directory/search and segmentation by source (individual, corporate, group, travel agent, OTA). *(client request · MoM 20 Aug 2026, 4.1 CRM — Customer Profiles, Unique Fields & Family/Guardian Linking · DI-370)*

`BO-736` Guest Master Configuration

- Decision: at least one of e-mail or mobile number is mandatory at profile creation (not both — some customers decline e-mail); the system supports conditional "either/or" mandatory-field rules. *(agreed · MoM 20 Aug 2026, 4.1 CRM; 5. Key Decisions · DI-372)*
- Profile fields must be fully configurable/user-defined (e.g. nationality vs. country of residence), with per-field unique and required flags; group profiles (group name, description, contact person) are configured independently. *(client request · MoM 20 Aug 2026, 4.1 CRM — Customer Profiles, Unique Fields & Family/Guardian Linking · DI-371)*

`BO-737` Customer 360 Profile

- Repeat guest checkouts with the same email (or phone) consolidate into one profile automatically; a manual merge-customer-profile function remains for edge cases (e.g. slightly different name spelling under the same email). Allam cited a system where 10 transactions created 10 profiles. *(agreed · MoM 18 Sep 2026, 4.8 Guest Checkout & Profile Deduplication — Extended Discussion · DI-941)*
- Entitlements portfolio is used both by the guest (mobile app) and by customer service: one view of restrictions, wallet balance and all entitlements; a unified list across a visit (e.g. four admissions, two fast passes, a meal package, a parking entitlement). *(client request · MoM 7 Sep 2026, 4.9 Entitlements Portfolio - Structure, Family/Group & Assignment · DI-667)*
- Decision: one unified customer profile across ticketing, F&B and retail gives a 360° view of guest activity and avoids duplicates; e.g. a guest who buys tickets online and later dines is matched by name/mobile to the same profile. *(agreed · MoM 18 Aug 2026, 4.9 Unified Customer Profile · DI-339)*

`BO-740` Family & Guardians

- Family/guardian linking is core (e.g. father, spouse, daughter as one family unit), consistent with family tickets/memberships; the same linking model extends to operations-team entitlement relationships. *(agreed · MoM 20 Aug 2026, 4.1 CRM — Customer Profiles, Unique Fields & Family/Guardian Linking · DI-373)*

`BO-741` Corporate & Groups

- One unified flow for groups, schools and corporates: inquiry > package builder > quotation > approval > confirmed booking. *(agreed · MoM 31 Aug 2026, 4.7 Group Sales / 5. Key Decisions · DI-565)*
- Corporate/B2B profiles have a self-service onboarding flow: company profile (name, address, trade licence, VAT certificate) → admin approval/rejection → rate/product setup → credential issuance. *(client request · MoM 20 Aug 2026, 4.1 CRM — Customer Profiles, Unique Fields & Family/Guardian Linking · DI-375)*

`BO-745` Identity Resolution Rules

- Duplicate review & merge: matching rules (fuzzy name similarity, exact mobile, exact e-mail) flag likely duplicates, as on the sample screen (500 profiles, ~100 matched by mobile number). *(client request · MoM 20 Aug 2026, 4.2 Duplicate Detection, Identity Resolution & Merge Rules · DI-376)*

`BO-746` Duplicate Review & Merge

- Repeat guest checkouts with the same email (or phone) consolidate into one profile automatically; a manual merge-customer-profile function remains for edge cases (e.g. slightly different name spelling under the same email). Allam cited a system where 10 transactions created 10 profiles. *(agreed · MoM 18 Sep 2026, 4.8 Guest Checkout & Profile Deduplication — Extended Discussion · DI-941)*
- Decision: profiles are never merged automatically. Likely duplicates are notified to the customer (push or e-mail) and merge only on the customer's confirmation; an admin review queue tracks flagged duplicates independently of the customer's response. *(agreed · MoM 20 Aug 2026, 4.2 Duplicate Detection; 5. Key Decisions · DI-377)*
- Duplicate review & merge: matching rules (fuzzy name similarity, exact mobile, exact e-mail) flag likely duplicates, as on the sample screen (500 profiles, ~100 matched by mobile number). *(client request · MoM 20 Aug 2026, 4.2 Duplicate Detection, Identity Resolution & Merge Rules · DI-376)*
- Duplicate-profile detection and merge (common because of name transliteration variants) merging two profiles with their combined transaction history; account activate/deactivate. *(agreed · MoM 7 Aug 2026, 19. Maintenance Tools · DI-176)*

`BO-747` Consent Policy Configuration

- Consent policy governs marketing/newsletter/survey communications; customers who do not opt in must not receive promotional communications. *(client request · MoM 20 Aug 2026, 4.3 Consent, Data Privacy & Retention · DI-378)*

`BO-750` Data Subject Requests

- Data-subject requests (access, correction, deletion) are tracked with status submitted → in progress → completed. *(client request · MoM 20 Aug 2026, 4.3 Consent, Data Privacy & Retention · DI-379)*

`BO-751` Retention & Anonymization

- Decision: data retention/archival (e.g. 3–5 years live before archival) and chat/case conversation retention (e.g. default one month, extendable) are configurable per tenant/venue at setup, with system defaults admins can override. *(agreed · MoM 20 Aug 2026, 4.3 Consent; 4.8 AI Chat Box; 5. Key Decisions · DI-380)*

`BO-755` Dynamic Segment Builder

- Dynamic segment builder supports rule-based segments (purchase value bands, product-specific purchases, recency); static lists import from CSV/Excel for migration; behavioural segments (cart-abandon, app session, campaign-open, survey-completed) feed marketing automation. *(client request · MoM 20 Aug 2026, 4.4 Audience Segmentation, Behavioural Analytics & Data Migration · DI-381)*

`BO-756` Static Lists & Imports

- Dynamic segment builder supports rule-based segments (purchase value bands, product-specific purchases, recency); static lists import from CSV/Excel for migration; behavioural segments (cart-abandon, app session, campaign-open, survey-completed) feed marketing automation. *(client request · MoM 20 Aug 2026, 4.4 Audience Segmentation, Behavioural Analytics & Data Migration · DI-381)*

`BO-757` Behavioral Segmentation

- Dynamic segment builder supports rule-based segments (purchase value bands, product-specific purchases, recency); static lists import from CSV/Excel for migration; behavioural segments (cart-abandon, app session, campaign-open, survey-completed) feed marketing automation. *(client request · MoM 20 Aug 2026, 4.4 Audience Segmentation, Behavioural Analytics & Data Migration · DI-381)*

`BO-758` Membership & Loyalty Segments

- **Open question.** Loyalty accrues points by product/spend tier (e.g. bronze/silver/gold thresholds) and unlocks tier benefits (e.g. platinum-tier discounts on F&B and ticketing). Full programme configuration (tiers, points, redemption, expiry) pending a dedicated session. *(open · MoM 20 Aug 2026, 4.5 Loyalty, Membership & Wallet · DI-382)*

`BO-764` Campaign Command Center

- Campaign tracking shows click-through, conversion and revenue attribution per campaign, with configurable success criteria (e.g. 80% conversion target). *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-383)*

`BO-765` Campaign Library & Calendar

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*

`BO-767` Audience & Offer Selection

- Decision: offer blocks in the Visual Journey Builder pick only from pre-configured, system-validated offers (product/ticket-type scoped, from the Offers module: coupon code, dynamic discount or auto-discount URL); ad-hoc discount values cannot be typed in the builder. *(agreed · MoM 20 Aug 2026, 4.6 Marketing Automation; 5. Key Decisions · DI-385)*

`BO-771` Budget, Goals & Forecast

- Campaign tracking shows click-through, conversion and revenue attribution per campaign, with configurable success criteria (e.g. 80% conversion target). *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-383)*

`BO-773` Attribution & Audit

- Campaign tracking shows click-through, conversion and revenue attribution per campaign, with configurable success criteria (e.g. 80% conversion target). *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-383)*

`BO-775` Visual Journey Builder

- Decision: offer blocks in the Visual Journey Builder pick only from pre-configured, system-validated offers (product/ticket-type scoped, from the Offers module: coupon code, dynamic discount or auto-discount URL); ad-hoc discount values cannot be typed in the builder. *(agreed · MoM 20 Aug 2026, 4.6 Marketing Automation; 5. Key Decisions · DI-385)*
- Visual Journey Builder triggers rule-based touchpoints (e.g. abandoned-cart recovery) with configurable wait periods (same-day, one week, one month), audience segment and optional incentive (e.g. coupon code). *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-384)*

`BO-776` Trigger Event Catalog

- Notification triggers must key off precise event states where needed: a post-visit survey only when the ticket was actually scanned/used, whereas a "how was your experience" follow-up can trigger off the sale. Trigger mapping must expose such event states. *(agreed · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-561)*

`BO-777` Decision Logic & Timing

- Visual Journey Builder triggers rule-based touchpoints (e.g. abandoned-cart recovery) with configurable wait periods (same-day, one week, one month), audience segment and optional incentive (e.g. coupon code). *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-384)*

`BO-778` Abandoned Cart Recovery

- Cart-abandonment triggers filter by minimum cart value and product type (e.g. only membership-ticket abandonment). Other journeys: birthday rewards, anniversary reminders, cross-sell/upsell, reservation/survey requests — all gated by customer consent. *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-386)*
- Visual Journey Builder triggers rule-based touchpoints (e.g. abandoned-cart recovery) with configurable wait periods (same-day, one week, one month), audience segment and optional incentive (e.g. coupon code). *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-384)*

`BO-779` Lifecycle Journeys

- Cart-abandonment triggers filter by minimum cart value and product type (e.g. only membership-ticket abandonment). Other journeys: birthday rewards, anniversary reminders, cross-sell/upsell, reservation/survey requests — all gated by customer consent. *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-386)*

`BO-780` Guest Engagement Journeys

- Cart-abandonment triggers filter by minimum cart value and product type (e.g. only membership-ticket abandonment). Other journeys: birthday rewards, anniversary reminders, cross-sell/upsell, reservation/survey requests — all gated by customer consent. *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-386)*

`BO-781` Cross-Sell & Service Recovery

- Cart-abandonment triggers filter by minimum cart value and product type (e.g. only membership-ticket abandonment). Other journeys: birthday rewards, anniversary reminders, cross-sell/upsell, reservation/survey requests — all gated by customer consent. *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-386)*

`BO-784` Communications Center

- Communications dashboard shows activity across email, WhatsApp and SMS: delivered, pending, failed. Delivery queue tracks failed sends with automatic retry; routing/fallback rules send on an alternate channel if delivery fails. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-559)*

`BO-785` Template Library

- Sender identity per brand (from and reply-to, e.g. no-reply@venue.com, customerservice@venue.com). Templates fully configurable per channel (email, SMS, WhatsApp): header, logo, footer and content, for consistent branded communications. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-560)*

`BO-788` Subscriptions & Preferences

- Consent and communication preference tracking records marketing/newsletter opt-in status per customer. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-562)*

`BO-789` Transactional Notification Rules

- Notification triggers must key off precise event states where needed: a post-visit survey only when the ticket was actually scanned/used, whereas a "how was your experience" follow-up can trigger off the sale. Trigger mapping must expose such event states. *(agreed · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-561)*

`BO-791` Delivery, Retry & Failover

- Communications dashboard shows activity across email, WhatsApp and SMS: delivered, pending, failed. Delivery queue tracks failed sends with automatic retry; routing/fallback rules send on an alternate channel if delivery fails. *(client request · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-559)*

`BO-793` AI Content, Translation & Audit

- Translation workflow: text entered in English, machine-translated, then reviewed and validated by the tenant's own team in the back office/CMS before publishing; applies to website, POS and mobile app. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-081)*

`BO-796` Guest Conversation 360

- The AI chat box answers guided/predefined queries (booking status, rescheduling) and logs guest conversation history across channels (WhatsApp, web, Instagram, Facebook) with per-channel conversion attribution. *(client request · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-388)*

`BO-797` AI Chatbot Configuration

- The AI chat box answers guided/predefined queries (booking status, rescheduling) and logs guest conversation history across channels (WhatsApp, web, Instagram, Facebook) with per-channel conversion attribution. *(client request · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-388)*

`BO-800` Routing & Queue Management

- Routing/queue configuration (reservation, general, membership & billing, technical support queues with priority and SLA policy) routes AI-agent conversations by detected query intent. *(agreed · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-389)*
- Decision: data retention/archival (e.g. 3–5 years live before archival) and chat/case conversation retention (e.g. default one month, extendable) are configurable per tenant/venue at setup, with system defaults admins can override. *(agreed · MoM 20 Aug 2026, 4.3 Consent; 4.8 AI Chat Box; 5. Key Decisions · DI-380)*

`BO-806` Case Creation

- Case creation captures logging channel/source, category and subcategory (e.g. ticket issue > reschedule) and supports screenshot attachments; investigation tracks all activity and actions on the case. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-541)*
- Cases can be logged from the customer app/website and from the call-centre/admin side, with category, priority, channel and SLA-based escalation rules. *(client request · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-390)*

`BO-809` SLA Policy Configuration

- Cases can be logged from the customer app/website and from the call-centre/admin side, with category, priority, channel and SLA-based escalation rules. *(client request · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-390)*

`BO-810` Escalation Rules

- Cases can be logged from the customer app/website and from the call-centre/admin side, with category, priority, channel and SLA-based escalation rules. *(client request · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-390)*

`BO-816` Survey Triggers & Distribution

- Surveys trigger at configurable points: post-purchase, post-visit, post-ticket-scan, membership renewal and case closure. *(client request · MoM 20 Aug 2026, 4.9 Surveys & Gamification · DI-391)*

`BO-826` Achievement & Badge Engine

- Gamification shows badges/status tiers (e.g. Explorer, Adventurer, Legend) earned by spend or engagement thresholds, feeding the loyalty tier structure. *(client request · MoM 20 Aug 2026, 4.9 Surveys & Gamification · DI-392)*

`BO-830` Referral & Streak Management

- Referral rewards may be credited as currency/points directly into the guest's wallet (like Swiggy), in addition to discount vouchers — a business-configurable option. *(agreed · MoM 25 Aug 2026, 4.7 Entitlements & Access Control; 5. Key Decisions · DI-460)*

`BO-834` Digital Experience Center

- The back-office Digital Experience/CMS screens duplicate the white-label CMS and are consolidated into P13 (one implementation, both ids kept), not built twice. *(agreed · MoM 24 Sep 2026, M24-03 · DI-996)*

`BO-835` Site, Brand & Domain Setup

- The back-office Digital Experience/CMS screens duplicate the white-label CMS and are consolidated into P13 (one implementation, both ids kept), not built twice. *(agreed · MoM 24 Sep 2026, M24-03 · DI-996)*
- CMS manages multiple sites/venues: branding, colour palette including custom hex codes, fonts, Google Analytics site IDs, production/staging environments. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-393)*
- One client can run multiple branded sites from the same setup, e.g. two brands sharing a footer but with distinct headers and hero banners. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-110)*

`BO-836` Design System & Components

- The back-office Digital Experience/CMS screens duplicate the white-label CMS and are consolidated into P13 (one implementation, both ids kept), not built twice. *(agreed · MoM 24 Sep 2026, M24-03 · DI-996)*
- **Open question.** Reusable page components per venue type are to be documented (e.g. seat-map component for stadiums/amphitheatres, park-map component for attraction venues) so one layout serves many venues with only imagery/data swapped. Documentation pending from Allam. *(open · MoM 20 Aug 2026, 4.10 CMS & White-Label; 6. Open Items · DI-395)*

`BO-837` Page & Landing Builder

- The back-office Digital Experience/CMS screens duplicate the white-label CMS and are consolidated into P13 (one implementation, both ids kept), not built twice. *(agreed · MoM 24 Sep 2026, M24-03 · DI-996)*
- Decision (raised by Qossai): the CMS/website builder supports two modes per client using the same builder — a full landing page plus integrated ticket-sale flow (clients without a website), or B2C-only (header, product cards, footer, checkout) embedded in/linked from an existing site. *(agreed · MoM 21 Aug 2026, 4.9 Website Builder Flexibility — Standalone vs. B2C-Only Configuration · DI-431)*
- Drag-and-drop page builder with a standardised layout (header, footer, hero/card components) that adapts to product type — seat map for seated products, standard flow for general admission. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-394)*
- Qossai: build AI-assisted site design/generation into the website builder, keeping site design (header, footer, color, font, layout) separate from content (tickets), with tickets flowing into the site's structure once published. To be explored. *(client request · MoM 3 Aug 2026, 7. AI-Assisted Website Generation · DI-115)*

`BO-838` Content, Media & Forms

- The back-office Digital Experience/CMS screens duplicate the white-label CMS and are consolidated into P13 (one implementation, both ids kept), not built twice. *(agreed · MoM 24 Sep 2026, M24-03 · DI-996)*

`BO-839` Dynamic Product Pages

- The back-office Digital Experience/CMS screens duplicate the white-label CMS and are consolidated into P13 (one implementation, both ids kept), not built twice. *(agreed · MoM 24 Sep 2026, M24-03 · DI-996)*
- Product cards/pages carry short descriptions with an expandable "view more details" control and a configurable hero image or video per product. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-425)*
- Ticket listings are data-driven: creating a new ticket automatically surfaces it on the relevant site according to its category configuration. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-109)*

`BO-840` Mobile App CMS

- The back-office Digital Experience/CMS screens duplicate the white-label CMS and are consolidated into P13 (one implementation, both ids kept), not built twice. *(agreed · MoM 24 Sep 2026, M24-03 · DI-996)*

`BO-841` Personalization & Localization

- The back-office Digital Experience/CMS screens duplicate the white-label CMS and are consolidated into P13 (one implementation, both ids kept), not built twice. *(agreed · MoM 24 Sep 2026, M24-03 · DI-996)*

`BO-842` SEO Management

- The back-office Digital Experience/CMS screens duplicate the white-label CMS and are consolidated into P13 (one implementation, both ids kept), not built twice. *(agreed · MoM 24 Sep 2026, M24-03 · DI-996)*

`BO-843` Publishing, Analytics & Audit

- The back-office Digital Experience/CMS screens duplicate the white-label CMS and are consolidated into P13 (one implementation, both ids kept), not built twice. *(agreed · MoM 24 Sep 2026, M24-03 · DI-996)*

`BO-844` Waiver Command Center

- Waiver dashboard tracks templates (published vs draft) and completion status. Templates can be cloned and are built with drag-and-drop fields (name, DOB, custom fields, T&C checkboxes). *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-570)*

`BO-845` Waiver Template Builder

- Waiver dashboard tracks templates (published vs draft) and completion status. Templates can be cloned and are built with drag-and-drop fields (name, DOB, custom fields, T&C checkboxes). *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-570)*

`BO-848` Signature Experience Setup

- **Open question.** Group waivers need a digital signature-capture device (stylus pad); Chinmay says a USB signature pad should integrate. Hardware reference pending from Qossai. *(open · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-756)*

`BO-849` Guardian & Group Signing

- Conditional fields: e.g. ask for the Emirates city only if country is UAE; ask extra questions only if age is below a threshold. Signatory config sets who signs (participant or parent/guardian). *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-572)*

`BO-851` Verification & Access Control

- Qossai: where a waiver is required before entry, an incomplete waiver can block ticket download, activation, check-in or access; ticket and scan screens need a waiver-incomplete state. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-574)*

`BO-854` Resource Management Command Center

- Resource types (rooms, staff, equipment, vehicles, etc.) carry capacity control and a reservable flag; the command centre shows total vs. active/assigned resources and current availability. *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-476)*
- Resource management command centre: calendar-based overview of all resources' booking status (e.g. an instructor booked for a lesson, date and time), filterable by resource type and venue, with a switchable revenue view; view by day, week, month or custom period (planner style). *(client request · MoM 26 Aug 2026, 4.1 Resource Management Overview · DI-475)*

`BO-855` Resource Type Configuration

- Resources are one-to-one (dedicated to a booking) or shared (e.g. a meeting room with bookable pods, a vehicle across sequential slots); further sales are blocked once a shared resource's capacity/slot is full and reopened if a booking is cancelled. *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-496)*
- Resource types (rooms, staff, equipment, vehicles, etc.) carry capacity control and a reservable flag; the command centre shows total vs. active/assigned resources and current availability. *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-476)*
- Optional resource module: a template defines the resource types a product needs (e.g. a vehicle and a driver); named resources have an availability calendar/roster; at sale (POS or online) both resource availability and capacity are checked before booking. *(agreed · MoM 7 Aug 2026, 18. Resource Management · DI-175)*

`BO-856` Resource Category Management

- Categories/subcategories are configurable hierarchies (e.g. staff → employee/operations/instructor; equipment → lighting/sound; vehicles → SUV). Resource profile: name, category, capacity, active/inactive, images, category-specific details and custom attributes (e.g. a vehicle's plate number). *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-477)*

`BO-857` Resource Creation & Profile

- Categories/subcategories are configurable hierarchies (e.g. staff → employee/operations/instructor; equipment → lighting/sound; vehicles → SUV). Resource profile: name, category, capacity, active/inactive, images, category-specific details and custom attributes (e.g. a vehicle's plate number). *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-477)*

`BO-858` Configurable Attribute Builder

- Categories/subcategories are configurable hierarchies (e.g. staff → employee/operations/instructor; equipment → lighting/sound; vehicles → SUV). Resource profile: name, category, capacity, active/inactive, images, category-specific details and custom attributes (e.g. a vehicle's plate number). *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-477)*

`BO-859` Resource Hierarchy & Parent–Child Relationships

- Resources link as main/sub-resources (e.g. "vehicle" with individual vehicles beneath). Dependency rules per product (e.g. a private ski lesson needs at least two resources, or at least one vehicle) are enforced when a resource-linked product is configured or sold. *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-478)*

`BO-860` Resource Dependency Rules

- Resources link as main/sub-resources (e.g. "vehicle" with individual vehicles beneath). Dependency rules per product (e.g. a private ski lesson needs at least two resources, or at least one vehicle) are enforced when a resource-linked product is configured or sold. *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-478)*

`BO-861` Resource Package & Bundle Configuration

- Multiple resources can be bundled to one product (e.g. a VIP Cabana package = room + attendant) so the system knows every resource needed when it is booked. *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-479)*

`BO-864` Resource Calendar Command Center

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Resource calendar is an inquiry/planning screen showing availability by date range (e.g. which of 10 vehicles are free between a start and end time), filterable and searchable across resource types. Schedules set each resource's working pattern (e.g. Monday–Friday, off weekends). *(client request · MoM 26 Aug 2026, 4.3 Resource Calendar & Scheduling · DI-480)*
- Resource management command centre: calendar-based overview of all resources' booking status (e.g. an instructor booked for a lesson, date and time), filterable by resource type and venue, with a switchable revenue view; view by day, week, month or custom period (planner style). *(client request · MoM 26 Aug 2026, 4.1 Resource Management Overview · DI-475)*

`BO-865` Calendar Filters, Search & Smart Discovery

- Resource calendar is an inquiry/planning screen showing availability by date range (e.g. which of 10 vehicles are free between a start and end time), filterable and searchable across resource types. Schedules set each resource's working pattern (e.g. Monday–Friday, off weekends). *(client request · MoM 26 Aug 2026, 4.3 Resource Calendar & Scheduling · DI-480)*

`BO-866` Resource Availability Schedule Configuration

- Resource calendar is an inquiry/planning screen showing availability by date range (e.g. which of 10 vehicles are free between a start and end time), filterable and searchable across resource types. Schedules set each resource's working pattern (e.g. Monday–Friday, off weekends). *(client request · MoM 26 Aug 2026, 4.3 Resource Calendar & Scheduling · DI-480)*

`BO-867` Resource Time-Slot Configuration

- Clarified: time slots are not created for resources; they are created for performances/events, and resources are associated with those performance time slots. *(agreed · MoM 26 Aug 2026, 4.3 Resource Calendar & Scheduling · DI-481)*

`BO-868` Advance Reservation Management

- Resources are normally booked automatically as a consequence of selling the associated package; manually reserving/blocking a specific resource outside a sale is only for exceptional cases (e.g. holding it for a future booking). *(agreed · MoM 26 Aug 2026, 4.4 Resource Assignment Models · DI-483)*

`BO-870` Operational Time & Resource Blocking

- Resources are normally booked automatically as a consequence of selling the associated package; manually reserving/blocking a specific resource outside a sale is only for exceptional cases (e.g. holding it for a future booking). *(agreed · MoM 26 Aug 2026, 4.4 Resource Assignment Models · DI-483)*

`BO-871` Multi-Event Resource Planning

- The system must prevent the same resource being double-booked or assigned to overlapping bookings (conflict detection and resolution). Multi-event planning and drag-and-drop allocation assign resources visually, alongside rule-based automatic assignment. *(agreed · MoM 26 Aug 2026, 4.4 Resource Assignment Models · DI-484)*

`BO-872` Smart Assignment & Drag-and-Drop Reallocation

- The system must prevent the same resource being double-booked or assigned to overlapping bookings (conflict detection and resolution). Multi-event planning and drag-and-drop allocation assign resources visually, alongside rule-based automatic assignment. *(agreed · MoM 26 Aug 2026, 4.4 Resource Assignment Models · DI-484)*

`BO-873` Staff Resource Directory

- Personnel (cashiers, trainers, drivers, other staff) are a resource type; command-centre view shows total personnel and how many are on duty, available or on leave. A staff profile's operational summary lists associated bookings. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-485)*

`BO-874` Staff Resource Profile

- Personnel (cashiers, trainers, drivers, other staff) are a resource type; command-centre view shows total personnel and how many are on duty, available or on leave. A staff profile's operational summary lists associated bookings. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-485)*

`BO-875` Skills & Competency Management

- Skills & competency define qualifications required for a role (e.g. level 1/2/3 ski-instructor certification for an advanced trainer); certification expiry tracking flags when recertification is due (e.g. annual renewal). *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-486)*

`BO-876` Certification & Expiry Management

- Skills & competency define qualifications required for a role (e.g. level 1/2/3 ski-instructor certification for an advanced trainer); certification expiry tracking flags when recertification is due (e.g. annual renewal). *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-486)*

`BO-879` Shift Template & Assignment Configuration

- Shift templates (morning/afternoon/evening) define working patterns; the system recognises which shift a staff member has logged into from the configured shift timings. Leave/absence types and quotas work as a lightweight HR module, optionally integrated with an external HR/time-and-attendance system. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-487)*

`BO-880` Break, Leave & Absence Configuration

- Shift templates (morning/afternoon/evening) define working patterns; the system recognises which shift a staff member has logged into from the configured shift timings. Leave/absence types and quotas work as a lightweight HR module, optionally integrated with an external HR/time-and-attendance system. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-487)*

`BO-882` Workforce Integration & Synchronization Center

- Shift templates (morning/afternoon/evening) define working patterns; the system recognises which shift a staff member has logged into from the configured shift timings. Leave/absence types and quotas work as a lightweight HR module, optionally integrated with an external HR/time-and-attendance system. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel Resource Management · DI-487)*

`BO-883` Workforce Roster Command Center

- Staffing dashboard shows checked-in, on-shift, on-leave, open-shift and closed-shift counts from check-in/out logs, plus staffing cost including overtime. *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-488)*

`BO-884` Attraction & Operational Staffing Roster

- Roster view per resource shows required vs. scheduled vs. checked-in counts for the day, surfacing discrepancies (e.g. 10 ski trainers scheduled, only 8 checked in). Minimum staffing/coverage rules are set per venue and day (e.g. minimum instructors per level). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-489)*

`BO-885` Minimum Staffing & Coverage Rule Configuration

- Roster view per resource shows required vs. scheduled vs. checked-in counts for the day, surfacing discrepancies (e.g. 10 ski trainers scheduled, only 8 checked in). Minimum staffing/coverage rules are set per venue and day (e.g. minimum instructors per level). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-489)*

`BO-886` Staffing Gap & Coverage Control Center

- If a scheduled resource fails to check in, the shortfall is flagged for operations and AI can recommend reassigning that resource's bookings. A compliance/validation centre flags events where required staffing is not met, with labour cost tracked. *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-490)*
- Roster view per resource shows required vs. scheduled vs. checked-in counts for the day, surfacing discrepancies (e.g. 10 ski trainers scheduled, only 8 checked in). Minimum staffing/coverage rules are set per venue and day (e.g. minimum instructors per level). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-489)*

`BO-887` Shift Marketplace & Workforce Requests

- Staff can request a swap (e.g. break coverage) from another resource; attendance exceptions are marked manually (active, not active, absent, other). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering; 4.9 AI Optimization, Mobile App & Analytics · DI-491)*

`BO-888` Attendance & Live Workforce Command Center

- Staffing dashboard shows checked-in, on-shift, on-leave, open-shift and closed-shift counts from check-in/out logs, plus staffing cost including overtime. *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-488)*

`BO-889` Staff Check-In, Check-Out & Attendance Exceptions

- Staff can request a swap (e.g. break coverage) from another resource; attendance exceptions are marked manually (active, not active, absent, other). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering; 4.9 AI Optimization, Mobile App & Analytics · DI-491)*

`BO-890` Workforce Compliance Validation Center

- If a scheduled resource fails to check in, the shortfall is flagged for operations and AI can recommend reassigning that resource's bookings. A compliance/validation centre flags events where required staffing is not met, with labour cost tracked. *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-490)*

`BO-891` Labor Cost & Staffing Budget Control

- Staffing dashboard shows checked-in, on-shift, on-leave, open-shift and closed-shift counts from check-in/out logs, plus staffing cost including overtime. *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-488)*

`BO-892` AI Workforce Planner & Roster Optimization

- AI forecasting from historical bookings recommends staffing levels for upcoming periods (e.g. "you will need this many resources over the next week") so leave and availability can be planned. Analytics show total cost and revenue by resource and by event. *(client request · MoM 26 Aug 2026, 4.9 AI Optimization, Mobile App & Analytics · DI-501)*

`BO-893` Experience Resource Requirement Builder

- Decision: two assignment models — pre-assigned (named vehicle/instructor/room mapped to a time slot in advance) and dynamic (only type + quantity, e.g. "one SUV and one guide", with an available resource auto-assigned at sale). *(agreed · MoM 26 Aug 2026, 4.4 Resource Assignment Models; 5. Key Decisions · DI-482)*

`BO-894` Staff-to-Experience Qualification Mapping

- An event can require a specific qualification level (e.g. advanced instructor only, excluding intermediate/beginner), enforced by the system. The resource combination builder sets required types, quantities and mandatory/optional per event (e.g. instructor, area, equipment set). *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-493)*

`BO-895` Resource Combination Builder

- An event can require a specific qualification level (e.g. advanced instructor only, excluding intermediate/beginner), enforced by the system. The resource combination builder sets required types, quantities and mandatory/optional per event (e.g. instructor, area, equipment set). *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-493)*

`BO-896` Ticket Demand & Resource Capacity Mapping

- Resource allocation is fixed-quantity or ratio-based/dynamic — e.g. one tour guide covers up to 10 tickets, and resources are added as sales grow. Whether resources are auto-assigned by type or specifically allocated can vary by sales channel. *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-494)*

`BO-897` Customer Resource Selection Configuration

- Decision (Qossai, Ski Dubai): instructor choice is a per-ticket-type setting — private-session products may let the guest pick a specific instructor; group-session products auto-assign without showing a choice. Private and group are separate, separately priced products (a private request on a group instructor is its own product). *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-504)*
- Resource allocation is fixed-quantity or ratio-based/dynamic — e.g. one tour guide covers up to 10 tickets, and resources are added as sales grow. Whether resources are auto-assigned by type or specifically allocated can vary by sales channel. *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-494)*

`BO-898` Skill-Based & Smart Resource Selection

- Decision (Chinmay): skill-based resource matching uses straightforward attribute/keyword matching (skill level, language), not a full AI-matching system. *(agreed · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment; 5. Key Decisions · DI-495)*

`BO-899` Customer / Cashier Resource Assignment Experience

- Decision (Qossai, Ski Dubai): instructor choice is a per-ticket-type setting — private-session products may let the guest pick a specific instructor; group-session products auto-assign without showing a choice. Private and group are separate, separately priced products (a private request on a group instructor is its own product). *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-504)*
- Resource allocation is fixed-quantity or ratio-based/dynamic — e.g. one tour guide covers up to 10 tickets, and resources are added as sales grow. Whether resources are auto-assigned by type or specifically allocated can vary by sales channel. *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-494)*

`BO-900` Dynamic Resource Allocation Engine

- Resources are one-to-one (dedicated to a booking) or shared (e.g. a meeting room with bookable pods, a vehicle across sequential slots); further sales are blocked once a shared resource's capacity/slot is full and reopened if a booking is cancelled. *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-496)*
- Decision: two assignment models — pre-assigned (named vehicle/instructor/room mapped to a time slot in advance) and dynamic (only type + quantity, e.g. "one SUV and one guide", with an available resource auto-assigned at sale). *(agreed · MoM 26 Aug 2026, 4.4 Resource Assignment Models; 5. Key Decisions · DI-482)*

`BO-901` Priority, Scoring & Allocation Policy

- Decision: allocation rotates across all available resources (resource 1, then 2, then 3) rather than reusing the same one; if an assigned resource becomes unavailable the system automatically replaces/reassigns it. *(agreed · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment; 5. Key Decisions · DI-497)*

`BO-902` Automatic Replacement & Assignment Recovery

- Decision: allocation rotates across all available resources (resource 1, then 2, then 3) rather than reusing the same one; if an assigned resource becomes unavailable the system automatically replaces/reassigns it. *(agreed · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment; 5. Key Decisions · DI-497)*

`BO-904` Rental Resource Configuration

- Rental/equipment items use simplified states — available, rented, faulty/out-of-maintenance (excluded from available inventory until resolved) — not granular custom attributes. Clients supply item data at onboarding; a screen lets them update inventory and item details afterwards. *(agreed · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management; 5. Key Decisions · DI-500)*
- Rental items (e.g. strollers, wheelchairs, towels): inventory and quantity per day, check-out and check-in, with inventory updated automatically on return; a refundable deposit (with guest details) is captured at rental and refunded on return. *(client request · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management · DI-498)*

`BO-905` Rental Inventory & Availability Control

- Rental/equipment items use simplified states — available, rented, faulty/out-of-maintenance (excluded from available inventory until resolved) — not granular custom attributes. Clients supply item data at onboarding; a screen lets them update inventory and item details afterwards. *(agreed · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management; 5. Key Decisions · DI-500)*
- Rental items (e.g. strollers, wheelchairs, towels): inventory and quantity per day, check-out and check-in, with inventory updated automatically on return; a refundable deposit (with guest details) is captured at rental and refunded on return. *(client request · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management · DI-498)*

`BO-906` Resource Checkout Workspace

- Rental items (e.g. strollers, wheelchairs, towels): inventory and quantity per day, check-out and check-in, with inventory updated automatically on return; a refundable deposit (with guest details) is captured at rental and refunded on return. *(client request · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management · DI-498)*

`BO-908` Rental Duration, Extension & Return Management

- Usage-based billing at return: excess charged on actual vs. paid duration (e.g. a wheelchair paid for one hour but used for three is charged two extra hours at return). *(client request · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management · DI-499)*

`BO-909` Deposit & Rental Financial Control

- Rental items (e.g. strollers, wheelchairs, towels): inventory and quantity per day, check-out and check-in, with inventory updated automatically on return; a refundable deposit (with guest details) is captured at rental and refunded on return. *(client request · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management · DI-498)*

`BO-910` Maintenance & Resource Blocking

- Rental/equipment items use simplified states — available, rented, faulty/out-of-maintenance (excluded from available inventory until resolved) — not granular custom attributes. Clients supply item data at onboarding; a screen lets them update inventory and item details afterwards. *(agreed · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management; 5. Key Decisions · DI-500)*

`BO-921` Multi-Event Allocation & Conflict Optimizer

- The system must prevent the same resource being double-booked or assigned to overlapping bookings (conflict detection and resolution). Multi-event planning and drag-and-drop allocation assign resources visually, alongside rule-based automatic assignment. *(agreed · MoM 26 Aug 2026, 4.4 Resource Assignment Models · DI-484)*

`BO-927` AI Staffing Requirement Forecast

- AI forecasting from historical bookings recommends staffing levels for upcoming periods (e.g. "you will need this many resources over the next week") so leave and availability can be planned. Analytics show total cost and revenue by resource and by event. *(client request · MoM 26 Aug 2026, 4.9 AI Optimization, Mobile App & Analytics · DI-501)*

`BO-930` Alternative & Replacement Resource

- If a scheduled resource fails to check in, the shortfall is flagged for operations and AI can recommend reassigning that resource's bookings. A compliance/validation centre flags events where required staffing is not met, with labour cost tracked. *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-490)*

`BO-933` My Resource Operations Home

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*

`BO-934` My Schedule & Assignment Calendar

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*

`BO-936` Mobile Staff Check-In & Check-Out

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*

`BO-939` Shift Change, Swap, Pickup & Release

- Staff can request a swap (e.g. break coverage) from another resource; attendance exceptions are marked manually (active, not active, absent, other). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering; 4.9 AI Optimization, Mobile App & Analytics · DI-491)*

`BO-945` Resource Cost, Revenue & Efficiency Analytics

- AI forecasting from historical bookings recommends staffing levels for upcoming periods (e.g. "you will need this many resources over the next week") so leave and availability can be planned. Analytics show total cost and revenue by resource and by event. *(client request · MoM 26 Aug 2026, 4.9 AI Optimization, Mobile App & Analytics · DI-501)*

`BO-953` Seat Map Command Center

- Movie/cinema ticketing is in scope through the seat management module (e.g. a Kuwait museum's educational cinema: assigned seats, a film, a time slot). *(agreed · MoM 14 Aug 2026, 5. Movie Ticketing · DI-286)*
- Chinmay: near-term AI can generate a map/seating layout and the related ticket configuration once a venue uploads its map schema and layout image. *(client request · MoM 14 Aug 2026, 1. AI Configuration Assistant — Phase-One Scope · DI-281)*
- Qossai: AI-assisted layout generation from AutoCAD/DXF (best) or PDF (fallback, via OCR), targeting ~90–95% automation with the client correcting the rest; sample input is a PDF seating diagram plus an Excel manifest of section/row/seat numbers. *(agreed · MoM 5 Aug 2026, 9. Seat Mapping & Venue Builder · DI-145)*
- A one-time, canvas-based venue/seat-map builder is required per venue. *(agreed · MoM 5 Aug 2026, 9. Seat Mapping & Venue Builder · DI-144)*

`BO-954` Venue Canvas

- **Open question.** Open: how the seat map builder consolidates the reference tool's separate screens (canvas, standing zone, suite, best-seats, entrances/exits) into one unified screen — Chinmay's team to confirm. *(open · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types (action) · DI-413)*
- Decision: section type (seated / non-seated-zone / standing / suite) is an attribute set at section level within ONE seat map builder screen, not separate configuration screens per type as in the reference tool. *(agreed · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types · DI-412)*
- One seat map can mix section types — e.g. 8 of 10 sections seated and 2 standing ("fan pit" near the stage); suites sell either as a private bulk-priced suite or as individual seats within the suite. *(agreed · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types · DI-411)*

`BO-955` Sections & Zones

- **Open question.** Open: how the seat map builder consolidates the reference tool's separate screens (canvas, standing zone, suite, best-seats, entrances/exits) into one unified screen — Chinmay's team to confirm. *(open · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types (action) · DI-413)*
- Decision: section type (seated / non-seated-zone / standing / suite) is an attribute set at section level within ONE seat map builder screen, not separate configuration screens per type as in the reference tool. *(agreed · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types · DI-412)*

`BO-956` Rows & Seats

- **Open question.** Open: how the seat map builder consolidates the reference tool's separate screens (canvas, standing zone, suite, best-seats, entrances/exits) into one unified screen — Chinmay's team to confirm. *(open · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types (action) · DI-413)*
- A one-time, canvas-based venue/seat-map builder is required per venue. *(agreed · MoM 5 Aug 2026, 9. Seat Mapping & Venue Builder · DI-144)*

`BO-957` Standing Zones

- **Open question.** Open: how the seat map builder consolidates the reference tool's separate screens (canvas, standing zone, suite, best-seats, entrances/exits) into one unified screen — Chinmay's team to confirm. *(open · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types (action) · DI-413)*
- Decision: section type (seated / non-seated-zone / standing / suite) is an attribute set at section level within ONE seat map builder screen, not separate configuration screens per type as in the reference tool. *(agreed · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types · DI-412)*
- One seat map can mix section types — e.g. 8 of 10 sections seated and 2 standing ("fan pit" near the stage); suites sell either as a private bulk-priced suite or as individual seats within the suite. *(agreed · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types · DI-411)*

`BO-958` Suites & Boxes

- **Open question.** Open: how the seat map builder consolidates the reference tool's separate screens (canvas, standing zone, suite, best-seats, entrances/exits) into one unified screen — Chinmay's team to confirm. *(open · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types (action) · DI-413)*
- Decision: section type (seated / non-seated-zone / standing / suite) is an attribute set at section level within ONE seat map builder screen, not separate configuration screens per type as in the reference tool. *(agreed · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types · DI-412)*
- One seat map can mix section types — e.g. 8 of 10 sections seated and 2 standing ("fan pit" near the stage); suites sell either as a private bulk-priced suite or as individual seats within the suite. *(agreed · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types · DI-411)*

`BO-960` Entrances, Exits & Aisles

- **Open question.** Open: how the seat map builder consolidates the reference tool's separate screens (canvas, standing zone, suite, best-seats, entrances/exits) into one unified screen — Chinmay's team to confirm. *(open · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types (action) · DI-413)*

`BO-962` Templates, Validation & Publish

- A one-time, canvas-based venue/seat-map builder is required per venue. *(agreed · MoM 5 Aug 2026, 9. Seat Mapping & Venue Builder · DI-144)*

`BO-964` PDF & Image Import

- Decision: besides manual drag-and-drop building, AI-assisted import — upload a PDF/image of the layout (AI recognises sections) plus an Excel/CSV of row/seat naming — generates a draft seat map for validation before publishing. *(agreed · MoM 21 Aug 2026, 4.4 AI-Assisted Seat Map Import & Layout/Template Management · DI-417)*

`BO-966` CSV & Excel Import

- Decision: besides manual drag-and-drop building, AI-assisted import — upload a PDF/image of the layout (AI recognises sections) plus an Excel/CSV of row/seat naming — generates a draft seat map for validation before publishing. *(agreed · MoM 21 Aug 2026, 4.4 AI-Assisted Seat Map Import & Layout/Template Management · DI-417)*

`BO-967` AI Section Recognition

- Decision: besides manual drag-and-drop building, AI-assisted import — upload a PDF/image of the layout (AI recognises sections) plus an Excel/CSV of row/seat naming — generates a draft seat map for validation before publishing. *(agreed · MoM 21 Aug 2026, 4.4 AI-Assisted Seat Map Import & Layout/Template Management · DI-417)*

`BO-968` AI Row & Seat Recognition

- Chinmay: near-term AI can generate a map/seating layout and the related ticket configuration once a venue uploads its map schema and layout image. *(client request · MoM 14 Aug 2026, 1. AI Configuration Assistant — Phase-One Scope · DI-281)*
- Qossai: AI-assisted layout generation from AutoCAD/DXF (best) or PDF (fallback, via OCR), targeting ~90–95% automation with the client correcting the rest; sample input is a PDF seating diagram plus an Excel manifest of section/row/seat numbers. *(agreed · MoM 5 Aug 2026, 9. Seat Mapping & Venue Builder · DI-145)*

`BO-971` Validation & Correction

- Decision: besides manual drag-and-drop building, AI-assisted import — upload a PDF/image of the layout (AI recognises sections) plus an Excel/CSV of row/seat naming — generates a draft seat map for validation before publishing. *(agreed · MoM 21 Aug 2026, 4.4 AI-Assisted Seat Map Import & Layout/Template Management · DI-417)*

`BO-972` AI Venue Designer & Publish

- Decision: besides manual drag-and-drop building, AI-assisted import — upload a PDF/image of the layout (AI recognises sections) plus an Excel/CSV of row/seat naming — generates a draft seat map for validation before publishing. *(agreed · MoM 21 Aug 2026, 4.4 AI-Assisted Seat Map Import & Layout/Template Management · DI-417)*

`BO-974` Template Library

- Decision: saved seat maps can be reused, copied in full, or partially copied (one section's layout/seating into another map); a template library and a layout version-comparison view show seat-count/configuration differences. *(agreed · MoM 21 Aug 2026, 4.4 AI-Assisted Seat Map Import & Layout/Template Management · DI-418)*

`BO-976` Clone & Inheritance

- Decision: saved seat maps can be reused, copied in full, or partially copied (one section's layout/seating into another map); a template library and a layout version-comparison view show seat-count/configuration differences. *(agreed · MoM 21 Aug 2026, 4.4 AI-Assisted Seat Map Import & Layout/Template Management · DI-418)*

`BO-977` Version Compare

- Decision: saved seat maps can be reused, copied in full, or partially copied (one section's layout/seating into another map); a template library and a layout version-comparison view show seat-count/configuration differences. *(agreed · MoM 21 Aug 2026, 4.4 AI-Assisted Seat Map Import & Layout/Template Management · DI-418)*

`BO-978` Multi-Performance Assignment

- A seat map is configured independently, then associated with one or more events/performances on a separate event-configuration screen that links seat map, pricing and performance date-time. *(client request · MoM 21 Aug 2026, 4.5 Multi-Performance Assignment, Temporary Blocking & Tiered/Early-Bird Release · DI-419)*

`BO-979` Temporary Seat Blocking

- Decision: inventory is released per section in tranches — temporary blocking (VIP/maintenance), scheduled release of held sections, and tiered/early-bird volumes (e.g. 30–40 of 100 seats at an early-bird price, then further tranches) — not full section capacity at go-live. *(agreed · MoM 21 Aug 2026, 4.5 Multi-Performance Assignment; 5. Key Decisions · DI-420)*
- Chinmay: reservations/holds are made section-wise (choose section → choose/hold seats within it), not by a freeform polygon selection as in the AI-generated reference mockup. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules & Social Distancing Configuration · DI-415)*

`BO-980` Scheduled Seat Release

- Decision: inventory is released per section in tranches — temporary blocking (VIP/maintenance), scheduled release of held sections, and tiered/early-bird volumes (e.g. 30–40 of 100 seats at an early-bird price, then further tranches) — not full section capacity at go-live. *(agreed · MoM 21 Aug 2026, 4.5 Multi-Performance Assignment; 5. Key Decisions · DI-420)*

`BO-984` Real-Time Seat Map

- Real-time seat inventory view shows per-event seat status (available, on hold, reserved, sold) with availability/holder trackers, sales & allocation tracking and audit/reconciliation reporting. *(client request · MoM 21 Aug 2026, 4.6 Seat Inventory Status, Holds & Automatic Release · DI-421)*

`BO-985` Status Model Configuration

- Real-time seat inventory view shows per-event seat status (available, on hold, reserved, sold) with availability/holder trackers, sales & allocation tracking and audit/reconciliation reporting. *(client request · MoM 21 Aug 2026, 4.6 Seat Inventory Status, Holds & Automatic Release · DI-421)*

`BO-986` Availability Tracker

- Real-time seat inventory view shows per-event seat status (available, on hold, reserved, sold) with availability/holder trackers, sales & allocation tracking and audit/reconciliation reporting. *(client request · MoM 21 Aug 2026, 4.6 Seat Inventory Status, Holds & Automatic Release · DI-421)*

`BO-987` Hold Tracker

- Real-time seat inventory view shows per-event seat status (available, on hold, reserved, sold) with availability/holder trackers, sales & allocation tracking and audit/reconciliation reporting. *(client request · MoM 21 Aug 2026, 4.6 Seat Inventory Status, Holds & Automatic Release · DI-421)*
- Chinmay: reservations/holds are made section-wise (choose section → choose/hold seats within it), not by a freeform polygon selection as in the AI-generated reference mockup. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules & Social Distancing Configuration · DI-415)*

`BO-988` Reservation Tracker

- Real-time seat inventory view shows per-event seat status (available, on hold, reserved, sold) with availability/holder trackers, sales & allocation tracking and audit/reconciliation reporting. *(client request · MoM 21 Aug 2026, 4.6 Seat Inventory Status, Holds & Automatic Release · DI-421)*

`BO-989` Sales & Allocation Tracker

- Real-time seat inventory view shows per-event seat status (available, on hold, reserved, sold) with availability/holder trackers, sales & allocation tracking and audit/reconciliation reporting. *(client request · MoM 21 Aug 2026, 4.6 Seat Inventory Status, Holds & Automatic Release · DI-421)*

`BO-992` Audit & Reconciliation

- Real-time seat inventory view shows per-event seat status (available, on hold, reserved, sold) with availability/holder trackers, sales & allocation tracking and audit/reconciliation reporting. *(client request · MoM 21 Aug 2026, 4.6 Seat Inventory Status, Holds & Automatic Release · DI-421)*

`BO-994` Choose My Seats

- Decision: three seat-selection models, selectable per section, per event: (1) zone/capacity selling with no seat numbers (guest told zone only); (2) system-assigned "best available" — guest picks section + quantity, seats disclosed later; (3) full customer seat selection. *(agreed · MoM 21 Aug 2026, 4.1 Reference Walkthrough; 4.2 Seat Map Builder; 5. Key Decisions · DI-410)*

`BO-995` Find Seats For Me

- Best-seat ranking (e.g. last-row-is-best vs. first-row-is-best, by venue sightlines) is configurable per seat map/event so the system recommends or auto-assigns the right best available seat. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules & Social Distancing Configuration · DI-414)*
- Decision: three seat-selection models, selectable per section, per event: (1) zone/capacity selling with no seat numbers (guest told zone only); (2) system-assigned "best available" — guest picks section + quantity, seats disclosed later; (3) full customer seat selection. *(agreed · MoM 21 Aug 2026, 4.1 Reference Walkthrough; 4.2 Seat Map Builder; 5. Key Decisions · DI-410)*

`BO-998` Lock Timeout & Concurrency

- Decision: seats held in a cart auto-release after a configurable timeout if checkout is abandoned, and immediately if a payment attempt fails. *(agreed · MoM 21 Aug 2026, 4.6 Seat Inventory Status; 5. Key Decisions · DI-422)*

`PTR-026` Territory, Market & Distribution Rights

- A partner has multiple agents/sub-agents who can each sell on its behalf; territory/market rights set the regions it may sell into; brand/venue association sets which venues and products it can sell, with distinct pricing per venue. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-549)*

`PTR-029` Partner Access, Roles & Permission Profile

- Partner access controls define which actions a partner may perform (e.g. refund, reschedule); the partner portal should only offer the actions granted. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-551)*

`PTR-035` Commission, Margin & Incentive Management

- Agreements overview shows active and pending agreements; partner pricing discounts configurable by quantity, amount, percentage or tiered volume bands (e.g. 10% up to 1,000 tickets, 15% from 1,000-5,000); commission rate per ticket sold. *(client request · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-554)*

`PTR-036` Credit Limit & Exposure Management

- Three partner payment models: (1) credit limit, invoiced monthly and settled by cheque/bank transfer; (2) prepayment wallet funded by bank transfer or online top-up and drawn down per sale; (3) pay-per-transaction by card. *(agreed · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-555)*
- B2B account financial tab shows credit limit, credit days and a linked account-specific price list; accounts can be a main account with child (agent) accounts; every account shows its full sales/transaction history, as does a B2C customer profile. *(client request · MoM 7 Aug 2026, 11. Accounts Management (B2B and B2C) · DI-162)*

`PTR-037` Deposit, Guarantee & Financial Security Management

- Three partner payment models: (1) credit limit, invoiced monthly and settled by cheque/bank transfer; (2) prepayment wallet funded by bank transfer or online top-up and drawn down per sale; (3) pay-per-transaction by card. *(agreed · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-555)*

`PTR-039` Commercial Allocation, Quota & Commitment Management

- Inventory can be reserved for a specific partner; booking limits cap tickets per transaction or transactions per day, per partner or overall. *(client request · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-556)*

`PTR-047` Partner Reconciliation & Exception Management

- Operations dashboard per partner: order volume, revenue, reservations and tickets on hold (booked but not yet issued). Cancellations/refund requests, statement of account (opening/closing balance, activity), reconciliation exceptions and disputes are tracked from this view. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-557)*

## P09 TICVAI Web

**Platform-wide**

- Portal access exposes TICVAI pricing, so prospects submit contact details and a trade license as proof of a real venue, reviewed and approved by TICVAI before access is granted. *(agreed · MoM 10 Sep 2026, 4.8 Customer Portal Access, Authentication & Verification · DI-827)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

**Infrastructure & Resilience**

- **Open question.** Open (Chinmay): should server/infrastructure monitoring and management be a dedicated module inside the TICVAI platform, or stay in Softlabs' own tooling (e.g. Terraform) outside the product? Input from Tejesh pending. *(open · MoM 10 Sep 2026, 4.18 Other Discussion · DI-841)*

**Platform**

- **Open question.** Open: should AI monitoring live in one centralised AI command dashboard or be distributed as widgets in each functional module's own dashboard? Allam: Softlabs' call; the current proposal is illustrative and Softlabs may propose a better structure. *(open · MoM 18 Sep 2026, 4.4 AI Governance — Risk, Compliance & Continuous Monitoring · DI-936)*

**Screen by screen**

`ADM-015` API Rate Limit & Quota Management

- Abnormal API volume is flagged, not only throttled (calls above the client's baseline, refusals outside the allow-list, calls to unused operations); a production access request requires at least one IP allow-list address. *(agreed · MoM 17 Sep 2026, M17-07 · DI-928)*
- Production access status is shown: sandbox only, requested (pending), approved, or rejected with the reason. Production keys only after certification; the request form says a new production key is issued and the sandbox key stays sandbox. *(agreed · MoM 17 Sep 2026, M17-06 · DI-927)*

`ADM-017` Domain & Certificate Management

- Guest web hosting: small tenants run under a subdomain/subpath of the TICVAI domain; larger clients get a dedicated URL on their own domain. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-283)*

`ADM-018` Interface Languages

- A new language is added as a configuration change, not development. Qossai wants a table-driven workflow like his prior project: a translation spreadsheet with a column per language reviewed by native speakers, then fed back through an AI translation pass. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-083)*
- Translation workflow: text entered in English, machine-translated, then reviewed and validated by the tenant's own team in the back office/CMS before publishing; applies to website, POS and mobile app. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-081)*

`ADM-021` Platform Role Management

- Allam: add a "roles comparison" view letting an admin compare two roles side by side (e.g. confirm a cashier role lacks the refund/void permissions a supervisor role has). *(agreed · MoM 7 Aug 2026, 4. Roles & User Management · DI-153)*

`ADM-022` Release & Version Management

- Minor releases are notified but optional and customers can postpone them. Major releases carry advance notice, a defined support lifecycle, end-of-support announcements for old versions and a mandatory upgrade (e.g. Version 3 -> End of Support Notice -> Version 4). *(agreed · MoM 30 Jul 2026, 6. Global Versioning Strategy · DI-054)*
- Releases go to staging first; customers are notified of each new version with new features, bug fixes and release notes, test in staging, and approve before promotion to production. *(agreed · MoM 30 Jul 2026, 4. Deployment Workflow Discussion · DI-053)*

`ADM-023` Staging Promotion & Approval

- **Open question.** Post-go-live, only configuration changes tested in staging (e.g. a new product or package) should be promoted to production, never transactional data; feasibility pending the CI/CD engineer. *(open · MoM 10 Sep 2026, 4.13 Pre-Production to Production Configuration Promotion · DI-834)*
- Releases go to staging first; customers are notified of each new version with new features, bug fixes and release notes, test in staging, and approve before promotion to production. *(agreed · MoM 30 Jul 2026, 4. Deployment Workflow Discussion · DI-053)*

`ADM-024` Release Notification Composer

- Releases go to staging first; customers are notified of each new version with new features, bug fixes and release notes, test in staging, and approve before promotion to production. *(agreed · MoM 30 Jul 2026, 4. Deployment Workflow Discussion · DI-053)*

`ADM-025` Tenant Upgrade Scheduler

- Minor releases are notified but optional and customers can postpone them. Major releases carry advance notice, a defined support lifecycle, end-of-support announcements for old versions and a mandatory upgrade (e.g. Version 3 -> End of Support Notice -> Version 4). *(agreed · MoM 30 Jul 2026, 6. Global Versioning Strategy · DI-054)*

`ADM-026` End-of-Support Notice Management

- Minor releases are notified but optional and customers can postpone them. Major releases carry advance notice, a defined support lifecycle, end-of-support announcements for old versions and a mandatory upgrade (e.g. Version 3 -> End of Support Notice -> Version 4). *(agreed · MoM 30 Jul 2026, 6. Global Versioning Strategy · DI-054)*

`ADM-037` AI Provider & Credentials

- The AI provider screen binds a provider to named agent tasks; model fitness warnings (underpowered / overpowered for a task) are shown, never blocking. *(agreed · MoM 21 Sep 2026, M21-03, M21-09 · DI-971)*
- AI operations monitoring shows health, cost/budget tracking and which AI agents consume the most resources and for what purpose, so the business can manage AI spend. *(client request · MoM 21 Sep 2026, 4.11 Core AI Platform — Operations & Consumption Monitoring · DI-968)*
- **Open question.** Proposed (Chinmay), not finalised: each pre-configured agent carries a complexity/fitness score; when a client switches models, an assessment flags whether the new model is under- or over-powered for that agent and recommends an adjustment. Exact end-user control over model switching is still open. *(open · MoM 21 Sep 2026, 4.10 Core AI Platform — Multi-Provider AI Model Strategy · DI-967)*
- Model selection per agent is system-managed by default (end users do not choose a model per task); a client may override the pre-selected model for an agent with its own API key, every change logged for audit. A client-hosted/private model plugs in the same way: API key plus endpoint address. *(agreed · MoM 21 Sep 2026, 4.10 Core AI Platform — Multi-Provider AI Model Strategy · DI-966)*

`ADM-068` Tax, Fee & Calculation Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`ADM-369` Commercial Command Center

- Licensing command centre: total customers, active subscriptions/tiers, MRR broken down by pricing model (tier-based, tier-plus-usage, per-ticket, per-transaction, hybrid, fixed, custom). *(client request · MoM 10 Sep 2026, 4.17 Licensing Command Center Overview · DI-838)*

`ADM-371` Customer Commercial 360°

- Per-customer billing view shows minimum billable volume (month-to-date) and variable/overage revenue; a customer profile consolidates all commercial and licensing information per client. *(client request · MoM 10 Sep 2026, 4.17 Licensing Command Center Overview · DI-839)*

`ADM-372` Operational Profile, VSI & Commercial Model Intelligence

- Further views: tier distribution (customers per tier), subscription revenue by tier, tier/conversion trends, and a renewal & retention centre flagging upcoming renewals, at-risk accounts and optimisation opportunities. *(client request · MoM 10 Sep 2026, 4.17 Licensing Command Center Overview · DI-840)*
- Tier thresholds map VSI ranges to tiers (0-30 Essential, 31-60 Professional, 61-80 Enterprise, 81-100 Enterprise Plus) with per-factor sub-thresholds (attendance 100-100,000 = 10 pts; 100,000-500,000 = 40); the system calculates the score and recommends the tier automatically. *(agreed · MoM 10 Sep 2026, 4.2 Venue Size Index (VSI) Model & Tier Threshold Configuration · DI-818)*

`ADM-373` Revenue & Commercial Model Analytics

- Further views: tier distribution (customers per tier), subscription revenue by tier, tier/conversion trends, and a renewal & retention centre flagging upcoming renewals, at-risk accounts and optimisation opportunities. *(client request · MoM 10 Sep 2026, 4.17 Licensing Command Center Overview · DI-840)*
- Licensing command centre: total customers, active subscriptions/tiers, MRR broken down by pricing model (tier-based, tier-plus-usage, per-ticket, per-transaction, hybrid, fixed, custom). *(client request · MoM 10 Sep 2026, 4.17 Licensing Command Center Overview · DI-838)*

`ADM-374` Trial & Conversion Monitor

- Back-end configuration access can optionally be added to the demo for qualified prospects at TICVAI's discretion; demo credentials can be scoped and time-limited (auto-expire after an evaluation period). *(agreed · MoM 10 Sep 2026, 4.11 Demo Environment Scope · DI-832)*
- "Try it" is a single shared, pre-configured demo (sample products, working POS/admin sales flow, reporting) entered with shared credentials - evaluation only, cannot sell real tickets; not a per-prospect trial tenant. *(agreed · MoM 10 Sep 2026, 4.11 Demo Environment Scope · DI-831)*

`ADM-375` Renewal & Retention Center

- Further views: tier distribution (customers per tier), subscription revenue by tier, tier/conversion trends, and a renewal & retention centre flagging upcoming renewals, at-risk accounts and optimisation opportunities. *(client request · MoM 10 Sep 2026, 4.17 Licensing Command Center Overview · DI-840)*

`ADM-376` Commercial Optimization & Expansion Opportunities

- Further views: tier distribution (customers per tier), subscription revenue by tier, tier/conversion trends, and a renewal & retention centre flagging upcoming renewals, at-risk accounts and optimisation opportunities. *(client request · MoM 10 Sep 2026, 4.17 Licensing Command Center Overview · DI-840)*

`ADM-379` Welcome & Start Your TICVAI Journey

- Onboarding starts from a link on the TICVAI website and walks a structured question set; first section is organisation details: venue name, industry, attraction type, currency, region/country, contact details, business type (private, semi-government, non-profit). *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-809)*

`ADM-380` Customer & Organization Registration

- Onboarding starts from a link on the TICVAI website and walks a structured question set; first section is organisation details: venue name, industry, attraction type, currency, region/country, contact details, business type (private, semi-government, non-profit). *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-809)*

`ADM-381` Venue Type & Business Profile

- Operating model question: attraction, museum, park, event, etc. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-810)*

`ADM-382` Visitor, Capacity & Operational Scale

- Visitor capacity and scale: expected annual/monthly visitors, venue capacity, entrances/exits, number of POS and access-control points, user count, estimated transaction volume, growth forecast. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-811)*

`ADM-383` Sales Channel Assessment

- Sales channels of interest (online, on-site, B2C, B2B/OTA) each with volume estimates. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-812)*

`ADM-384` Ticketing & Product Requirements

- Product/module types they plan to sell: general admission, seat-based, resource management, events, memberships, wallet, etc.; plus guest access/validation methods. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-813)*

`ADM-385` Access, Queue & Visitor Experience Assessment

- Product/module types they plan to sell: general admission, seat-based, resource management, events, memberships, wallet, etc.; plus guest access/validation methods. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-813)*

`ADM-386` Additional Business Module Assessment

- Additional modules needed (F&B, retail, membership/CRM, etc.). *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-814)*

`ADM-387` Integration, Payment & Technical Readiness

- Payment gateway/device integration needs: select from a supported list or specify an unlisted provider. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-815)*

`ADM-388` AI Assessment Summary & Handoff

- The prospect reviews then submits the assessment, which becomes the basis for the system's proposed commercial/licensing model. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-816)*

`ADM-390` VSI Model Builder

- VSI is a weighted composite of onboarding factors - annual attendance (illustrated ~30% weight), POS terminals, access-control devices, venues, users, annual transaction volume - each configurable as mandatory or optional. *(agreed · MoM 10 Sep 2026, 4.2 Venue Size Index (VSI) Model & Tier Threshold Configuration · DI-817)*

`ADM-391` VSI Scoring & Tier Threshold Configuration

- Tier thresholds map VSI ranges to tiers (0-30 Essential, 31-60 Professional, 61-80 Enterprise, 81-100 Enterprise Plus) with per-factor sub-thresholds (attendance 100-100,000 = 10 pts; 100,000-500,000 = 40); the system calculates the score and recommends the tier automatically. *(agreed · MoM 10 Sep 2026, 4.2 Venue Size Index (VSI) Model & Tier Threshold Configuration · DI-818)*

`ADM-392` Subscription Tier Configuration

- Each tier has its own price payable monthly, annually or in advance (cheque/bank transfer), with a configurable trial period; tier-included allowances (e.g. Professional up to 10 POS devices and 20 users) at the same price anywhere within the range. *(client request · MoM 10 Sep 2026, 4.3 Subscription Tiers, Allowances & Usage Thresholds · DI-819)*

`ADM-393` Tier Included Allowances

- Each tier has its own price payable monthly, annually or in advance (cheque/bank transfer), with a configurable trial period; tier-included allowances (e.g. Professional up to 10 POS devices and 20 users) at the same price anywhere within the range. *(client request · MoM 10 Sep 2026, 4.3 Subscription Tiers, Allowances & Usage Thresholds · DI-819)*

`ADM-394` Commercial & Licensing Model Configuration

- Commercial models, combinable per client: tier-based, tier plus usage, per-ticket, per-transaction, percentage-based, minimum guarantee, hybrid, fixed multi-year contract. *(agreed · MoM 10 Sep 2026, 4.4 Commercial & Licensing Pricing Models · DI-821)*

`ADM-395` Billable Unit, Minimum Guarantee & Enforcement Rules

- Billable/excludable ticket rules (e.g. complimentary, voided and refunded tickets excluded), minimum guarantee and overage rate are configured together; a commercial model simulator tests a model before it is assigned to a customer. *(client request · MoM 10 Sep 2026, 4.4 Commercial & Licensing Pricing Models · DI-822)*

`ADM-396` Overage Pricing & Capacity Packs

- Billable/excludable ticket rules (e.g. complimentary, voided and refunded tickets excluded), minimum guarantee and overage rate are configured together; a commercial model simulator tests a model before it is assigned to a customer. *(client request · MoM 10 Sep 2026, 4.4 Commercial & Licensing Pricing Models · DI-822)*

`ADM-397` Commercial Model & Rule Simulation

- Billable/excludable ticket rules (e.g. complimentary, voided and refunded tickets excluded), minimum guarantee and overage rate are configured together; a commercial model simulator tests a model before it is assigned to a customer. *(client request · MoM 10 Sep 2026, 4.4 Commercial & Licensing Pricing Models · DI-822)*

`ADM-399` Recommended Package Overview

- From onboarding data the system proposes a recommended commercial model and tier package (example: a museum recommended per-ticket plus minimum guarantee). *(client request · MoM 10 Sep 2026, 4.7 Package Builder & Module Marketplace · DI-823)*

`ADM-401` Module Marketplace

- Module marketplace lists optional add-ons (B2C, B2B, mobile app, virtual queue, CRM, seat management, etc.) with AI recommendations from stated needs (e.g. virtual queue if queue management was flagged). *(client request · MoM 10 Sep 2026, 4.7 Package Builder & Module Marketplace · DI-824)*

`ADM-402` AI Module & Package Recommendations

- Module marketplace lists optional add-ons (B2C, B2B, mobile app, virtual queue, CRM, seat management, etc.) with AI recommendations from stated needs (e.g. virtual queue if queue management was flagged). *(client request · MoM 10 Sep 2026, 4.7 Package Builder & Module Marketplace · DI-824)*

`ADM-404` Module Dependency & Compatibility Manager

- Module dependency check before allowing combinations - e.g. flag that the online/B2C module must be included before enabling virtual queue. *(client request · MoM 10 Sep 2026, 4.7 Package Builder & Module Marketplace · DI-825)*

`ADM-409` Purchase / Trial Journey Selection

- "Try it" is a single shared, pre-configured demo (sample products, working POS/admin sales flow, reporting) entered with shared credentials - evaluation only, cannot sell real tickets; not a per-prospect trial tenant. *(agreed · MoM 10 Sep 2026, 4.11 Demo Environment Scope · DI-831)*

`ADM-413` Trial Configuration & Conversion Rules

- Back-end configuration access can optionally be added to the demo for qualified prospects at TICVAI's discretion; demo credentials can be scoped and time-limited (auto-expire after an evaluation period). *(agreed · MoM 10 Sep 2026, 4.11 Demo Environment Scope · DI-832)*
- "Try it" is a single shared, pre-configured demo (sample products, working POS/admin sales flow, reporting) entered with shared credentials - evaluation only, cannot sell real tickets; not a per-prospect trial tenant. *(agreed · MoM 10 Sep 2026, 4.11 Demo Environment Scope · DI-831)*

`ADM-419` Provisioning Command Center

- After contract, TICVAI provisions the tenant with a basic setup reflecting the tier and licensed modules (e.g. mobile app, B2C, B2B enabled as contracted) before handover; AI can assist initial product/event/ticket setup following the same process as manual setup. *(client request · MoM 10 Sep 2026, 4.12 Tenant Provisioning & Go-Live Setup · DI-833)*

`ADM-423` License & Entitlement Activation

- After contract, TICVAI provisions the tenant with a basic setup reflecting the tier and licensed modules (e.g. mobile app, B2C, B2B enabled as contracted) before handover; AI can assist initial product/event/ticket setup following the same process as manual setup. *(client request · MoM 10 Sep 2026, 4.12 Tenant Provisioning & Go-Live Setup · DI-833)*

`ADM-424` Module Activation & Dependency Validation

- After contract, TICVAI provisions the tenant with a basic setup reflecting the tier and licensed modules (e.g. mobile app, B2C, B2B enabled as contracted) before handover; AI can assist initial product/event/ticket setup following the same process as manual setup. *(client request · MoM 10 Sep 2026, 4.12 Tenant Provisioning & Go-Live Setup · DI-833)*

`ADM-426` Initial Configuration & Regional Defaults

- After contract, TICVAI provisions the tenant with a basic setup reflecting the tier and licensed modules (e.g. mobile app, B2C, B2B enabled as contracted) before handover; AI can assist initial product/event/ticket setup following the same process as manual setup. *(client request · MoM 10 Sep 2026, 4.12 Tenant Provisioning & Go-Live Setup · DI-833)*

`ADM-427` Provisioning Validation & Exception Management

- Go-live readiness validates end-to-end: products set up correctly, pricing displays correctly, and a full test transaction completes in the target environment. *(client request · MoM 10 Sep 2026, 4.14 Go-Live Readiness Validation · DI-835)*

`ADM-449` Usage & License Command Center

- Usage tracking shows tickets sold, licence inventory consumption (e.g. 8 of 10 licensed POS terminals in use) and overage, signalling a possible tier upgrade or extra charges. *(client request · MoM 10 Sep 2026, 4.15 Usage & Commercial Consumption Tracking · DI-836)*

`ADM-450` Entitlement & License Inventory

- Usage tracking shows tickets sold, licence inventory consumption (e.g. 8 of 10 licensed POS terminals in use) and overage, signalling a possible tier upgrade or extra charges. *(client request · MoM 10 Sep 2026, 4.15 Usage & Commercial Consumption Tracking · DI-836)*

`ADM-451` Commercial Consumption & Billable Event Metering

- Usage tracking shows tickets sold, licence inventory consumption (e.g. 8 of 10 licensed POS terminals in use) and overage, signalling a possible tier upgrade or extra charges. *(client request · MoM 10 Sep 2026, 4.15 Usage & Commercial Consumption Tracking · DI-836)*

`ADM-452` Operational Usage & Threshold Monitor

- A configurable warning threshold (e.g. 80% of an included allowance) notifies both the customer and TICVAI before the client exceeds included usage. *(client request · MoM 10 Sep 2026, 4.3 Subscription Tiers, Allowances & Usage Thresholds · DI-820)*

`ADM-454` Minimum Guarantee & Variable Consumption Monitor

- Per-customer billing view shows minimum billable volume (month-to-date) and variable/overage revenue; a customer profile consolidates all commercial and licensing information per client. *(client request · MoM 10 Sep 2026, 4.17 Licensing Command Center Overview · DI-839)*

`ADM-455` Overage, Capacity & Temporary Exception Management

- Usage tracking shows tickets sold, licence inventory consumption (e.g. 8 of 10 licensed POS terminals in use) and overage, signalling a possible tier upgrade or extra charges. *(client request · MoM 10 Sep 2026, 4.15 Usage & Commercial Consumption Tracking · DI-836)*

`ADM-456` Usage Alerts, Reconciliation & Exception Center

- A configurable warning threshold (e.g. 80% of an included allowance) notifies both the customer and TICVAI before the client exceeds included usage. *(client request · MoM 10 Sep 2026, 4.3 Subscription Tiers, Allowances & Usage Thresholds · DI-820)*

`ADM-459` Billing & Commercial Command Center

- Billing consolidates consumption per billing cycle into an invoice with tier plus usage/overage charges; renewal is automatic (monthly/annual) or a manual contract review, per agreed terms. *(client request · MoM 10 Sep 2026, 4.16 Billing, Reconciliation & Renewal · DI-837)*

`ADM-460` Billing Calculation & Charge Breakdown

- Billing consolidates consumption per billing cycle into an invoice with tier plus usage/overage charges; renewal is automatic (monthly/annual) or a manual contract review, per agreed terms. *(client request · MoM 10 Sep 2026, 4.16 Billing, Reconciliation & Renewal · DI-837)*

`ADM-462` Invoice & Payment Management

- Billing consolidates consumption per billing cycle into an invoice with tier plus usage/overage charges; renewal is automatic (monthly/annual) or a manual contract review, per agreed terms. *(client request · MoM 10 Sep 2026, 4.16 Billing, Reconciliation & Renewal · DI-837)*

`ADM-464` Renewal Management Center

- Billing consolidates consumption per billing cycle into an invoice with tier plus usage/overage charges; renewal is automatic (monthly/annual) or a manual contract review, per agreed terms. *(client request · MoM 10 Sep 2026, 4.16 Billing, Reconciliation & Renewal · DI-837)*

`ADM-469` AI Configuration Home & Start

- Phase-one AI priority is a conversational configuration assistant: the admin says e.g. "I want to configure a new product" and it asks the product type (admission, time slot, etc.) and walks through product/promotion setup. *(agreed · MoM 14 Aug 2026, 1. AI Configuration Assistant — Phase-One Scope · DI-279)*

`ADM-481` Product Configuration Assistant

- The AI configuration assistant is conversational and iterative: on "I want to create a product" it asks follow-ups (ticket type, validity, date/time) and, if required information such as capacity is missing, asks for it rather than proceeding, before showing a configuration blueprint and dependency map. *(agreed · MoM 18 Sep 2026, 4.5 AI Configuration Assistant — Conversational Requirement Gathering · DI-937)*
- Phase-one AI priority is a conversational configuration assistant: the admin says e.g. "I want to configure a new product" and it asks the product type (admission, time slot, etc.) and walks through product/promotion setup. *(agreed · MoM 14 Aug 2026, 1. AI Configuration Assistant — Phase-One Scope · DI-279)*

`ADM-498` AI Configuration Audit & Governance

- AI-prepared configuration keeps full version history, e.g. every price change shows who suggested it, who approved it and when it was published. *(client request · MoM 18 Sep 2026, 4.7 AI Configuration Assistant — Approval, Execution & Audit Trail · DI-938)*

`ADM-500` Forecast Configuration & Forecasting Strategy

- Forecast configuration offers producer rule, statistical or ensemble, and a history window defaulting to 36 months. *(agreed · MoM 18 Sep 2026, M18-16 · DI-958)*

`ADM-503` Ticket, Product & Timeslot Demand Forecast

- AI suggestions from sales forecasts: add/remove time slots, merge under-sold adjacent slots (with guest notification of the time change), and dynamic pricing (raise when a slot is >~80% sold, lower when <~20–30%). *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-454)*

`ADM-515` F&B, Retail & Inventory Demand Forecast

- Retail intelligence shows sales and outlet performance, top-performing stores, demand forecasting (from retail sales history and online ticket booking trends) and target-vs-actual per outlet (e.g. monthly target vs. achieved, with variance). *(client request · MoM 19 Aug 2026, 4.9 Retail Intelligence & Reporting · DI-368)*

`ADM-517` Operational Scenario & Readiness Simulator

- Demand forecasts show current sales pace, forecast and remaining opportunity broken down by sales channel; revenue forecasts show drivers and confidence levels. A forecast simulator models a hypothetical change (e.g. a 10% price decrease, reduced operating hours, staffing changes) before it is made. *(client request · MoM 18 Sep 2026, 4.10 AI Forecasting — Attendance, Demand, Revenue & Capacity Forecasting · DI-943)*

`ADM-526` AI Policy Conflict, Exception & Override Management

- The AI policy screen shows each conflict and the more restrictive result it resolved to; a plan step failing a module limit is shown as governance-blocked and never applied. *(agreed · MoM 18 Sep 2026, M18-01 · DI-955)*
- AI policy testing lets administrators preview what would be allowed or blocked before a governance policy is published; policy conflicts (e.g. an AI price increase above a configured maximum) are flagged, never applied silently. *(client request · MoM 18 Sep 2026, 4.1 AI Governance — Capability Registration, Risk & Autonomy Configuration · DI-935)*

`ADM-527` AI Policy Testing & Governance Simulation

- AI policy testing lets administrators preview what would be allowed or blocked before a governance policy is published; policy conflicts (e.g. an AI price increase above a configured maximum) are flagged, never applied silently. *(client request · MoM 18 Sep 2026, 4.1 AI Governance — Capability Registration, Risk & Autonomy Configuration · DI-935)*

`ADM-530` AI Approval Requirement & Routing Configuration

- AI actions route through the shared approval matrix: the screen shows the approver's limit for the kind and amount and whether the action is within it or must escalate; escalation, delegation and SLA apply as to any approval. *(agreed · MoM 18 Sep 2026, M18-02 · DI-956)*

`ADM-531` AI Approval Review Workspace

- Approval is not binary: conditional approval lets an approver approve with restrictions, e.g. a commercial manager may approve price increases only up to a ceiling, anything higher escalates. An approver can also challenge a proposal and request evidence or alternatives. *(agreed · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-932)*
- The AI approval review workspace gives the approver everything needed to decide: current vs proposed value, impact, risk and affected objects (e.g. a weekend price increase shown with the channels it publishes to and whether future bookings are affected). *(client request · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-931)*

`ADM-532` Conditional Approval & Approval Conditions

- AI actions route through the shared approval matrix: the screen shows the approver's limit for the kind and amount and whether the action is within it or must escalate; escalation, delegation and SLA apply as to any approval. *(agreed · MoM 18 Sep 2026, M18-02 · DI-956)*
- Approval is not binary: conditional approval lets an approver approve with restrictions, e.g. a commercial manager may approve price increases only up to a ceiling, anything higher escalates. An approver can also challenge a proposal and request evidence or alternatives. *(agreed · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-932)*

`ADM-533` Human Review, Challenge & AI Clarification Workspace

- Approval is not binary: conditional approval lets an approver approve with restrictions, e.g. a commercial manager may approve price increases only up to a ceiling, anything higher escalates. An approver can also challenge a proposal and request evidence or alternatives. *(agreed · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-932)*

`ADM-534` Escalation, Delegation & Approval SLA Management

- AI actions route through the shared approval matrix: the screen shows the approver's limit for the kind and amount and whether the action is within it or must escalate; escalation, delegation and SLA apply as to any approval. *(agreed · MoM 18 Sep 2026, M18-02 · DI-956)*
- SLA rules set how fast a request must be approved (e.g. within one day); if not actioned it auto-escalates to the next level so someone can investigate (e.g. approver on leave) and reassign. *(client request · MoM 8 Sep 2026, 4.12 Approval Workflow Recap - Inbox, SLA & Escalation · DI-724)*

`ADM-535` Live AI Execution Oversight & Human Intervention

- Roll back on partial failure: plans the compensating steps in reverse dependency order, approved like any plan. *(agreed · MoM 21 Sep 2026, M21-12 · DI-972)*
- AI actions in progress are shown step by step in an AI action command center; if a process only partly completes (e.g. missing information) it rolls back rather than leaving a product half-configured, and a full change history records everything AI modified. *(client request · MoM 21 Sep 2026, 4.9 Core AI Platform — AI Tools, Agents & Action Orchestration · DI-965)*
- Live AI execution oversight lets a user watch an in-progress AI process step by step (e.g. the configuration assistant creating a venue, then products, then performances), and an authorised person can reject, modify or replace an AI decision at any point, with full intervention history. *(client request · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-933)*

`ADM-536` Human Override & Manual Control Center

- Live AI execution oversight lets a user watch an in-progress AI process step by step (e.g. the configuration assistant creating a venue, then products, then performances), and an authorised person can reject, modify or replace an AI decision at any point, with full intervention history. *(client request · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-933)*

`ADM-537` Approval & Intervention History / Decision Timeline

- Live AI execution oversight lets a user watch an in-progress AI process step by step (e.g. the configuration assistant creating a venue, then products, then performances), and an authorised person can reject, modify or replace an AI decision at any point, with full intervention history. *(client request · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-933)*

`ADM-540` AI Decision Explorer & Search

- AI decisions are searchable by venue and by customer. *(agreed · MoM 18 Sep 2026, M18-03 · DI-957)*
- Every AI decision is searchable in an AI decision explorer by customer, venue or AI capability, showing the data/model behind it, the governing rule, any human override, who approved it and when it was published. *(agreed · MoM 18 Sep 2026, 4.3 AI Governance — Explainability, Decision Trace & Audit · DI-934)*

`ADM-541` AI Decision Explanation Workspace

- Every AI decision is searchable in an AI decision explorer by customer, venue or AI capability, showing the data/model behind it, the governing rule, any human override, who approved it and when it was published. *(agreed · MoM 18 Sep 2026, 4.3 AI Governance — Explainability, Decision Trace & Audit · DI-934)*

`ADM-543` Candidate, Rule & Decision Path Trace

- Every AI decision is searchable in an AI decision explorer by customer, venue or AI capability, showing the data/model behind it, the governing rule, any human override, who approved it and when it was published. *(agreed · MoM 18 Sep 2026, 4.3 AI Governance — Explainability, Decision Trace & Audit · DI-934)*

`ADM-545` Governance, Approval & Human Decision Trace

- Every AI decision is searchable in an AI decision explorer by customer, venue or AI capability, showing the data/model behind it, the governing rule, any human override, who approved it and when it was published. *(agreed · MoM 18 Sep 2026, 4.3 AI Governance — Explainability, Decision Trace & Audit · DI-934)*

`ADM-549` AI Governance Monitoring Command Center

- AI governance shows overall AI health in production and spend by agent, with the month-end projection labelled a forecast. *(agreed · MoM 21 Sep 2026, M21-13 · DI-973)*

## P10 Partner Web

**Platform-wide**

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

**Access & Account**

- Corporate/B2B profiles have a self-service onboarding flow: company profile (name, address, trade licence, VAT certificate) → admin approval/rejection → rate/product setup → credential issuance. *(client request · MoM 20 Aug 2026, 4.1 CRM — Customer Profiles, Unique Fields & Family/Guardian Linking · DI-375)*

**Screen by screen**

`PTR-001` Partner Login / MFA

- Partner onboarding: partner signs up via a registration link/form on the B2B platform, then review and approval, with confirmation emails and back-office visibility of required next steps. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-548)*
- Partner review: operations validate documents and can reject (e.g. expired trade licence) with a message prompting resubmission; approval emails credentials with a temporary password, and the partner must set their own password at first login. *(client request · MoM 7 Aug 2026, 13. Tenant/B2B Onboarding & Self-Registration Flow · DI-166)*

`PTR-005` Inventory & Allocation View

- Partner screens never create products, prices or performances: the product catalogue (B2B pricing) is read only and the inventory view keeps its reads; partners see assigned products and partner prices. *(agreed · Decisions Register 29 Sep 2026, Rev 3 prototype feedback — M17-04 (partner API scope) · DI-1079)*
- Partners never create products, prices or capacity: partner catalogue and inventory screens are read-only (a partner may still return its own unsold allocation). *(agreed · MoM 17 Sep 2026, M17-04 · DI-930)*
- Inventory can be reserved for a specific partner; booking limits cap tickets per transaction or transactions per day, per partner or overall. *(client request · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-556)*

`PTR-006` Product Catalog (B2B Pricing)

- Partner screens never create products, prices or performances: the product catalogue (B2B pricing) is read only and the inventory view keeps its reads; partners see assigned products and partner prices. *(agreed · Decisions Register 29 Sep 2026, Rev 3 prototype feedback — M17-04 (partner API scope) · DI-1079)*
- Partners never create products, prices or capacity: partner catalogue and inventory screens are read-only (a partner may still return its own unsold allocation). *(agreed · MoM 17 Sep 2026, M17-04 · DI-930)*

`PTR-009` Group / Bulk Booking

- Amendments/cancellations/reschedules are checked against the applicable policy before being allowed. A booking's financial status (deposit required, partial payment, full payment) is tracked; schools and corporates can pay a 20-30% deposit with the balance due on or before arrival. *(agreed · MoM 1 Sep 2026, 4.12 Amendment, Cancellation & Booking Status · DI-615)*
- Allam: Bulk QR option — for partners with no technical capability, the platform generates a bulk batch of tickets (e.g. 5,000) with a validity window, delivered as QR codes (e.g. CSV) for the partner to import and resell. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-135)*

`PTR-012` Checkout / Credit Purchase

- Three partner payment models: (1) credit limit, invoiced monthly and settled by cheque/bank transfer; (2) prepayment wallet funded by bank transfer or online top-up and drawn down per sale; (3) pay-per-transaction by card. *(agreed · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-555)*

`PTR-013` Credit Limit & Balance

- Three partner payment models: (1) credit limit, invoiced monthly and settled by cheque/bank transfer; (2) prepayment wallet funded by bank transfer or online top-up and drawn down per sale; (3) pay-per-transaction by card. *(agreed · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-555)*

`PTR-016` Voucher / Ticket Download

- For partners not integrating by API, TICVAI can issue a bulk batch of pre-generated tickets (QR codes, agreed rates, defined validity) as a CSV export for the partner to import and resell. *(agreed · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-553)*
- Allam: Bulk QR option — for partners with no technical capability, the platform generates a bulk batch of tickets (e.g. 5,000) with a validity window, delivered as QR codes (e.g. CSV) for the partner to import and resell. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-135)*

`PTR-019` API Credentials & Integration

- Partners never create products, prices or capacity: partner catalogue and inventory screens are read-only (a partner may still return its own unsold allocation). *(agreed · MoM 17 Sep 2026, M17-04 · DI-930)*
- Abnormal API volume is flagged, not only throttled (calls above the client's baseline, refusals outside the allow-list, calls to unused operations); a production access request requires at least one IP allow-list address. *(agreed · MoM 17 Sep 2026, M17-07 · DI-928)*
- Production access status is shown: sandbox only, requested (pending), approved, or rejected with the reason. Production keys only after certification; the request form says a new production key is issued and the sandbox key stays sandbox. *(agreed · MoM 17 Sep 2026, M17-06 · DI-927)*
- API scopes are picked from a list grouped by module ({module}.read / {module}.write), with unlicensed modules shown disabled rather than hidden; the API reference is grouped by licensable module, then contract. *(agreed · MoM 17 Sep 2026, M17-05, M17-12 · DI-926)*

`PTR-020` Sub-Agent Management

- A partner has multiple agents/sub-agents who can each sell on its behalf; territory/market rights set the regions it may sell into; brand/venue association sets which venues and products it can sell, with distinct pricing per venue. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-549)*
- B2B account financial tab shows credit limit, credit days and a linked account-specific price list; accounts can be a main account with child (agent) accounts; every account shows its full sales/transaction history, as does a B2C customer profile. *(client request · MoM 7 Aug 2026, 11. Accounts Management (B2B and B2C) · DI-162)*

`PTR-022` Partner Management Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Partner overview lists all B2B partners with status, pending approvals and documentation state. Partner profile captures company info and a configurable partner category/type; profile fields are fully customisable. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-547)*

`PTR-023` Partner Profile & Organization Setup

- Partner overview lists all B2B partners with status, pending approvals and documentation state. Partner profile captures company info and a configurable partner category/type; profile fields are fully customisable. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-547)*
- B2B account financial tab shows credit limit, credit days and a linked account-specific price list; accounts can be a main account with child (agent) accounts; every account shows its full sales/transaction history, as does a B2C customer profile. *(client request · MoM 7 Aug 2026, 11. Accounts Management (B2B and B2C) · DI-162)*

`PTR-024` Partner Onboarding & Application Workflow

- Partner onboarding: partner signs up via a registration link/form on the B2B platform, then review and approval, with confirmation emails and back-office visibility of required next steps. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-548)*
- Partner review: operations validate documents and can reject (e.g. expired trade licence) with a message prompting resubmission; approval emails credentials with a temporary password, and the partner must set their own password at first login. *(client request · MoM 7 Aug 2026, 13. Tenant/B2B Onboarding & Self-Registration Flow · DI-166)*
- "Become a partner" link on the tenant website opens a registration form capturing company type, name, address, Emirate/state and documents (trade licence, VAT/TRN certificate); submitting creates a pending account and emails the tenant's operations team. *(client request · MoM 7 Aug 2026, 13. Tenant/B2B Onboarding & Self-Registration Flow · DI-165)*

`PTR-025` Partner Contacts & User Administration

- A partner has multiple agents/sub-agents who can each sell on its behalf; territory/market rights set the regions it may sell into; brand/venue association sets which venues and products it can sell, with distinct pricing per venue. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-549)*

`PTR-027` Partner Brand, Venue & Business Scope Assignment

- A partner has multiple agents/sub-agents who can each sell on its behalf; territory/market rights set the regions it may sell into; brand/venue association sets which venues and products it can sell, with distinct pricing per venue. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-549)*

`PTR-028` Partner Documentation & Compliance Repository

- Partner documents (e.g. trade licence, VAT certificate) follow a review/accept/reject/resubmit flow; approval status runs lead > submitted > active > suspended; a partner 360 view consolidates profile, agreement and payment information in one view. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-550)*
- "Become a partner" link on the tenant website opens a registration form capturing company type, name, address, Emirate/state and documents (trade licence, VAT/TRN certificate); submitting creates a pending account and emails the tenant's operations team. *(client request · MoM 7 Aug 2026, 13. Tenant/B2B Onboarding & Self-Registration Flow · DI-165)*

`PTR-030` Partner Approval, Status & Lifecycle Management

- Partner documents (e.g. trade licence, VAT certificate) follow a review/accept/reject/resubmit flow; approval status runs lead > submitted > active > suspended; a partner 360 view consolidates profile, agreement and payment information in one view. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-550)*
- Partner review: operations validate documents and can reject (e.g. expired trade licence) with a message prompting resubmission; approval emails credentials with a temporary password, and the partner must set their own password at first login. *(client request · MoM 7 Aug 2026, 13. Tenant/B2B Onboarding & Self-Registration Flow · DI-166)*

`PTR-031` Partner 360° Profile, Readiness & AI Review

- Partner documents (e.g. trade licence, VAT certificate) follow a review/accept/reject/resubmit flow; approval status runs lead > submitted > active > suspended; a partner 360 view consolidates profile, agreement and payment information in one view. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-550)*

`PTR-032` Commercial Agreement Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Agreements overview shows active and pending agreements; partner pricing discounts configurable by quantity, amount, percentage or tiered volume bands (e.g. 10% up to 1,000 tickets, 15% from 1,000-5,000); commission rate per ticket sold. *(client request · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-554)*

`PTR-033` Agreement & Contract Terms Builder

- Agreements overview shows active and pending agreements; partner pricing discounts configurable by quantity, amount, percentage or tiered volume bands (e.g. 10% up to 1,000 tickets, 15% from 1,000-5,000); commission rate per ticket sold. *(client request · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-554)*

`PTR-034` Partner Rate & Net Pricing Configuration

- Agreements overview shows active and pending agreements; partner pricing discounts configurable by quantity, amount, percentage or tiered volume bands (e.g. 10% up to 1,000 tickets, 15% from 1,000-5,000); commission rate per ticket sold. *(client request · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-554)*

`PTR-038` Payment Terms, Billing & Account Configuration

- Three partner payment models: (1) credit limit, invoiced monthly and settled by cheque/bank transfer; (2) prepayment wallet funded by bank transfer or online top-up and drawn down per sale; (3) pay-per-transaction by card. *(agreed · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-555)*

`PTR-040` Booking Limits, Commercial Exceptions & Approval

- Inventory can be reserved for a specific partner; booking limits cap tickets per transaction or transactions per day, per partner or overall. *(client request · MoM 31 Aug 2026, 4.4 B2B Commercial Agreements, Credit & Payment Models · DI-556)*

`PTR-041` Commercial Agreement 360°, Health & AI Review

- Partner documents (e.g. trade licence, VAT certificate) follow a review/accept/reject/resubmit flow; approval status runs lead > submitted > active > suspended; a partner 360 view consolidates profile, agreement and payment information in one view. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-550)*

`PTR-042` Partner Operations Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Operations dashboard per partner: order volume, revenue, reservations and tickets on hold (booked but not yet issued). Cancellations/refund requests, statement of account (opening/closing balance, activity), reconciliation exceptions and disputes are tracked from this view. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-557)*

`PTR-043` Partner Orders & Booking Management

- For partners not integrating by API, TICVAI can issue a bulk batch of pre-generated tickets (QR codes, agreed rates, defined validity) as a CSV export for the partner to import and resell. *(agreed · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-553)*

`PTR-045` Partner Cancellations, Refunds & Amendments

- Operations dashboard per partner: order volume, revenue, reservations and tickets on hold (booked but not yet issued). Cancellations/refund requests, statement of account (opening/closing balance, activity), reconciliation exceptions and disputes are tracked from this view. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-557)*

`PTR-046` Partner Statement & Account Activity

- Operations dashboard per partner: order volume, revenue, reservations and tickets on hold (booked but not yet issued). Cancellations/refund requests, statement of account (opening/closing balance, activity), reconciliation exceptions and disputes are tracked from this view. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-557)*

`PTR-049` Partner Disputes, Cases & Service Management

- Operations dashboard per partner: order volume, revenue, reservations and tickets on hold (booked but not yet issued). Cancellations/refund requests, statement of account (opening/closing balance, activity), reconciliation exceptions and disputes are tracked from this view. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-557)*

`PTR-050` Partner Performance Scorecard & Risk Monitoring

- AI partner performance view surfaces trends, risks and opportunities across the partner base for account-management decisions. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-558)*

`PTR-051` Partner AI Intelligence & Relationship Optimization

- AI partner performance view surfaces trends, risks and opportunities across the partner base for account-management decisions. *(client request · MoM 31 Aug 2026, 4.5 B2B Day-to-Day Operations & Settlement · DI-558)*

## P11 Accreditation Web

**Platform-wide**

- The web portal is the primary channel for accreditation; the mobile app is a secondary route for individual applicants. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-693)*
- Accreditation is primarily completed in the web portal (document upload and photo checks suit a larger screen); the same submission is also available in the guest mobile app as a secondary option for individuals. *(agreed · MoM 7 Sep 2026, 4.8 Accreditation Channel Placement & API Access · DI-666)*
- Bulk: a company with many members (e.g. 1,000) gets an Excel template to submit all details and documents at once; each imported record still goes through profile, documents and approval. *(client request · MoM 7 Sep 2026, 4.7 Notifications, Bulk Operations & Analytics · DI-664)*
- A main account holder (company/agent) sees the status of every application under their organisation (approved, rejected, requires resubmission), whether the credential is collected physically or sent as a soft copy by email. *(client request · MoM 7 Sep 2026, 4.4 Accreditation Profile, Identity Verification & Duplicate Prevention · DI-660)*
- The venue creates a partner/company account (main or sub-accounts) whose users log in and submit accreditation for their members; entry can be done by the end user or by the admin team on their behalf. *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-655)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

**Screen by screen**

`ACC-001` Landing / Programme Overview

- The landing shows three stated turnaround numbers: time to apply, time to a decision, and the cut-off before the performance (CF and MoM record that an unstated turnaround is what generates phone calls). *(agreed · screen note 7 Sep 2026, ACC-001 · DI-695)*
- Accreditation: applicant fills a customisable form, goes through approval (with documents), and receives a credential (photo badge, QR or RFID) for event access. Dashboard shows total registered, pending review and expired documents; directory searches applications by name, company or business info. *(client request · MoM 7 Sep 2026, 4.1 Accreditation Overview & Application Directory · DI-654)*

`ACC-002` Registration Form

- Uniqueness is enforced on passport and Emirates ID; a duplicate submission is blocked. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-692)*
- Identity documents are OCR'd to auto-populate the accreditation form, and extracted data is kept as fields (for expiry tracking and renewal prompts). *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-691)*
- Allam asked, Chinmay confirmed: uploading an ID (e.g. Emirates ID image or PDF from phone or laptop) auto-fills form fields (ID number, expiry) via OCR; data is stored as structured fields to track expiry and prompt renewal. *(agreed · MoM 7 Sep 2026, 4.3 OCR Auto-Fill / 5. Key Decisions · DI-658)*
- Submission tracking shows submitted, pending and missing-document applications. Upload accepts PDF, JPEG, PNG and enforces file-size/quality limits at upload time. *(client request · MoM 7 Sep 2026, 4.3 Application Requirements, Document Validation & OCR Auto-Fill · DI-657)*
- Drag-and-drop form builder sets exactly which fields each form collects; categories (media, corporate, individual guest) each have their own form; programmes link a category to an event, venue or season; a requirement matrix sets documents per category (e.g. contractors need company authorisation). *(client request · MoM 7 Sep 2026, 4.2 Accreditation Form Builder, Categories & Program Setup · DI-656)*
- Accreditation: applicant fills a customisable form, goes through approval (with documents), and receives a credential (photo badge, QR or RFID) for event access. Dashboard shows total registered, pending review and expired documents; directory searches applications by name, company or business info. *(client request · MoM 7 Sep 2026, 4.1 Accreditation Overview & Application Directory · DI-654)*

`ACC-003` Application Review & Submit

- Uniqueness is enforced on passport and Emirates ID; a duplicate submission is blocked. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-692)*
- Staff open an application to review the photo and all details and verify documents are correct, legible and valid. Duplicate passport/Emirates ID numbers are blocked, prompting the applicant to resolve or resubmit rather than silently creating a duplicate. *(agreed · MoM 7 Sep 2026, 4.4 Accreditation Profile, Identity Verification & Duplicate Prevention · DI-659)*

`ACC-004` Application Status Tracking

- Lifecycle: activation, expiry, renewal, suspension; if a document (e.g. Emirates ID) expires before the event, a resubmission request is raised and the credential is blocked if unresolved. Applicants are notified at each status change (approved, rejected, needs validation). *(client request · MoM 7 Sep 2026, 4.6 / 4.7 Lifecycle & Notifications · DI-663)*
- Submission tracking shows submitted, pending and missing-document applications. Upload accepts PDF, JPEG, PNG and enforces file-size/quality limits at upload time. *(client request · MoM 7 Sep 2026, 4.3 Application Requirements, Document Validation & OCR Auto-Fill · DI-657)*

`ACC-005` Accreditation Badge

- Approved credential: printed photo badge, QR or RFID depending on the event's configured media; collected physically or delivered digitally to a mobile device. Access rights set zones per category (media all zones; corporate limited). *(client request · MoM 7 Sep 2026, 4.6 Credential Issuance, Access Rights & Lifecycle Management · DI-662)*
- Accreditation: applicant fills a customisable form, goes through approval (with documents), and receives a credential (photo badge, QR or RFID) for event access. Dashboard shows total registered, pending review and expired documents; directory searches applications by name, company or business info. *(client request · MoM 7 Sep 2026, 4.1 Accreditation Overview & Application Directory · DI-654)*

`ACC-007` Reviewer Application Detail

- Staff open an application to review the photo and all details and verify documents are correct, legible and valid. Duplicate passport/Emirates ID numbers are blocked, prompting the applicant to resolve or resubmit rather than silently creating a duplicate. *(agreed · MoM 7 Sep 2026, 4.4 Accreditation Profile, Identity Verification & Duplicate Prevention · DI-659)*

## P12 Venue Support

**Platform-wide**

- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- Client support staff log into TICVAI to view and respond to their own tickets/chats (keeps a full audit trail); adapters to clients' own support systems are phase two. *(agreed · MoM 12 Aug 2026, 10. Customer Support / Chat Integration Approach · DI-257)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

**Screen by screen**

`SUP-001` Venue Management Sign In

- Access loads automatically at login on POS and web/admin. A user with one role logs straight in; a user with several roles (e.g. admin, cashier, supervisor, manager) is prompted to choose which role to use. *(agreed · MoM 12 Aug 2026, 4. Multiple Roles per User and Role Switching · DI-249)*

`SUP-002` Agent Dashboard

- Case dashboard shows total cases logged, due cases and per-agent case load, each governed by an SLA based on case type. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-539)*

`SUP-004` Conversation Queue

- Support chat is native to TICVAI: a built-in AI chat assistant answers first, then escalates to a human "CR representative" role in the platform; offered white-labelled as a subscription add-on for smaller clients. *(agreed · MoM 12 Aug 2026, 10. Customer Support / Chat Integration Approach · DI-256)*

`SUP-005` Live Chat Workspace

- Support chat is native to TICVAI: a built-in AI chat assistant answers first, then escalates to a human "CR representative" role in the platform; offered white-labelled as a subscription add-on for smaller clients. *(agreed · MoM 12 Aug 2026, 10. Customer Support / Chat Integration Approach · DI-256)*

`SUP-009` Customer Service Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Case dashboard shows total cases logged, due cases and per-agent case load, each governed by an SLA based on case type. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-539)*

`SUP-010` Customer 360° Service Profile

- Entitlement statuses: active, reserved, consumed, transferred, expired, refunded/cancelled; views show entitlements nearing expiry, real-time consumption per customer, and whether a ticket has been upgraded. *(client request · MoM 7 Sep 2026, 4.10 / 4.11 Entitlements Lifecycle & Usage · DI-670)*
- Family/dependent view shows a family ticket's composition (e.g. two adults, two children) with each dependent's entitlements; equivalent views for school and corporate bookings. *(client request · MoM 7 Sep 2026, 4.9 Entitlements Portfolio - Structure, Family/Group & Assignment · DI-668)*
- Entitlements portfolio is used both by the guest (mobile app) and by customer service: one view of restrictions, wallet balance and all entitlements; a unified list across a visit (e.g. four admissions, two fast passes, a meal package, a parking entitlement). *(client request · MoM 7 Sep 2026, 4.9 Entitlements Portfolio - Structure, Family/Group & Assignment · DI-667)*
- Customer profile gives agents one view of customer details, open cases and case history; a communications & transactions screen shows the full history of prior communications and actions. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-540)*

`SUP-011` Unified Interaction & Communication History

- Customer profile gives agents one view of customer details, open cases and case history; a communications & transactions screen shows the full history of prior communications and actions. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-540)*

`SUP-012` Case Creation, Classification & Intelligent Routing

- Intelligent routing assigns cases by skill, language, availability, workload and priority, showing an assignment preview that the user can manually override before confirming. *(client request · MoM 31 Aug 2026, 4.2 Contact Center Operations, AI Routing & Quality Management · DI-545)*
- Case creation captures logging channel/source, category and subcategory (e.g. ticket issue > reschedule) and supports screenshot attachments; investigation tracks all activity and actions on the case. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-541)*

`SUP-013` Case Investigation & Resolution Workspace

- Case creation captures logging channel/source, category and subcategory (e.g. ticket issue > reschedule) and supports screenshot attachments; investigation tracks all activity and actions on the case. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-541)*

`SUP-014` Order, Booking & Ticket Service Workspace

- Group ticket upgrades are business-configurable (off by default); where allowed a group raises an upgrade request (e.g. via chat/support) rather than self-serving like an individual. *(agreed · MoM 1 Sep 2026, 4.9 Clarified (group upgrades) · DI-607)*
- From the case screen agents act on the customer's bookings/tickets (date change, reschedule, resend tickets), initiate refunds/compensation, route for internal approval, or escalate to another department, which sees it on that department's mobile app. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-542)*

`SUP-015` Refund, Compensation & Service Exception Workspace

- Approved refunds go back to the original payment method or are credited to the guest's wallet for future purchases. *(client request · MoM 7 Sep 2026, 4.11 Entitlements Usage, Upgrades & Refund/Credit Recovery · DI-673)*
- From the case screen agents act on the customer's bookings/tickets (date change, reschedule, resend tickets), initiate refunds/compensation, route for internal approval, or escalate to another department, which sees it on that department's mobile app. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-542)*

`SUP-016` Escalation, Collaboration & Internal Resolution

- From the case screen agents act on the customer's bookings/tickets (date change, reschedule, resend tickets), initiate refunds/compensation, route for internal approval, or escalate to another department, which sees it on that department's mobile app. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-542)*

`SUP-017` Case Resolution, Closure & Customer Feedback

- On resolution the agent logs the outcome; an AI customer-service summariser compiles all actions taken on the case for quick review. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-543)*

`SUP-018` AI Customer Service Copilot & Knowledge Workspace

- The AI assistant answers natural-language business queries (e.g. "what was yesterday's ticketing revenue?") only within the user's role (a CEO sees full revenue, a cashier does not), shows grounded citations naming the policy or document an answer came from, and keeps conversation context ("compare that to this week"). *(client request · MoM 21 Sep 2026, 4.8 Core AI Platform — AI Assistant (Query & Knowledge) · DI-964)*
- On resolution the agent logs the outcome; an AI customer-service summariser compiles all actions taken on the case for quick review. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-543)*

`SUP-019` Contact Center Operations Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Supervisor dashboard: case volume by category (general support, refund, ticketing, membership) and status, quality scores per agent (resolution time and outcome vs SLA), customer-satisfaction results and week-over-week case-volume trends. *(client request · MoM 31 Aug 2026, 4.2 Contact Center Operations, AI Routing & Quality Management · DI-544)*

`SUP-021` Intelligent Routing, Skills & Assignment Engine

- Intelligent routing assigns cases by skill, language, availability, workload and priority, showing an assignment preview that the user can manually override before confirming. *(client request · MoM 31 Aug 2026, 4.2 Contact Center Operations, AI Routing & Quality Management · DI-545)*

`SUP-022` SLA Policy & Service-Level Management

- SLA policies per case type; agent workload view allows reassigning cases to balance load; unresolved cases can be escalated further from case monitoring. *(client request · MoM 31 Aug 2026, 4.2 Contact Center Operations, AI Routing & Quality Management · DI-546)*

`SUP-023` Agent Workload, Availability & Workforce Control

- SLA policies per case type; agent workload view allows reassigning cases to balance load; unresolved cases can be escalated further from case monitoring. *(client request · MoM 31 Aug 2026, 4.2 Contact Center Operations, AI Routing & Quality Management · DI-546)*

`SUP-024` Escalation & Critical Case Monitor

- SLA policies per case type; agent workload view allows reassigning cases to balance load; unresolved cases can be escalated further from case monitoring. *(client request · MoM 31 Aug 2026, 4.2 Contact Center Operations, AI Routing & Quality Management · DI-546)*

`SUP-025` Quality Management & Agent Evaluation

- Supervisor dashboard: case volume by category (general support, refund, ticketing, membership) and status, quality scores per agent (resolution time and outcome vs SLA), customer-satisfaction results and week-over-week case-volume trends. *(client request · MoM 31 Aug 2026, 4.2 Contact Center Operations, AI Routing & Quality Management · DI-544)*

`SUP-026` Customer Satisfaction, Feedback & Voice of Customer

- Supervisor dashboard: case volume by category (general support, refund, ticketing, membership) and status, quality scores per agent (resolution time and outcome vs SLA), customer-satisfaction results and week-over-week case-volume trends. *(client request · MoM 31 Aug 2026, 4.2 Contact Center Operations, AI Routing & Quality Management · DI-544)*

## P13 Venue CMS

**Platform-wide**

- The config side panel is a reference tool only, not the CMS. The CMS will be step-based and include header/footer, logos and banners. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W12 Config side panel · DI-1014)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- Qossai: build AI-assisted site design/generation into the website builder, keeping site design (header, footer, color, font, layout) separate from content (tickets), with tickets flowing into the site's structure once published. To be explored. *(client request · MoM 3 Aug 2026, 7. AI-Assisted Website Generation · DI-115)*
- Qossai: give clients as much design flexibility as possible within the configurable structure. *(client request · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-114)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

**White Label**

- Font, header/footer (not yet in the current wireframe build), card size and layout are configurable in the mobile app, consistent with the web app's white-labelling approach. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1097)*
- Qossai (rated the CMS prototype ~70%): a client should be able to build a working site "within 30 minutes", easily adding header, footer, fonts and its own images/graphics self-service; Allam: every CMS option must visibly change something and the interface must be intuitive to navigate. *(client request · MoM 24 Sep 2026, 4.8 Guest Web App CMS Prototype — Feedback on Maturity & Scope Expectations · DI-988)*
- The reviewed prototype is the actual guest-facing B2C site customers browse and book from, not a CMS tool. A separate, more limited white-label interface lets a client adjust colours, fonts and layout from a menu of options; not yet built in the prototype. *(agreed · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-887)*
- Base structure (header, footer, layout) is fixed across tenants; logo, colour, font and module visibility (e.g. hide Dining or Retail) are configurable per tenant, and independently for web and mobile (e.g. a different mobile header). *(agreed · MoM 14 Aug 2026, 4. White-Labeling and Customization Boundaries · DI-285)*
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)*
- Modules enabled/disabled per tenant by licence: Ticketing & Booking, Membership, Events, Attractions, Virtual Queue, F&B, Retail, Parking; add-ons (Lost & Found, AI Concierge Chat, multi-language, integrations) toggle the same way and appear automatically as new integrations are built. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-193)*
- Allam: banner, header, footer and background color are CMS-configurable per client, but site structure and navigation flow are fixed and adapt automatically to product configuration (dated, non-dated, seated, membership products surface the right fields). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-119)*
- A "powered by [platform]" footer credit is fixed and not client-editable. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-111)*
- White-label sites share one platform/template but each is configured independently: header, footer, logo, colors, fonts and hero banner are client-editable from the backend. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-108)*

**Screen by screen**

`CMS-001` Tenant Workspace

- The CMS is a step-based site builder started from the workspace; a preset keeps the minimum path short (modules, booking flows, home sections and mobile tabs proposed), so an operator supplies only a logo, four colours and Publish; aim about 30 minutes to a working site. *(agreed · MoM 24 Sep 2026, M24-05 · DI-997)*

`CMS-002` Brand Kit

- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Qossai: white-labelling needs more flexibility, e.g. setting the colour of specific interactive elements such as the "pay now" / "purchase" button independently, not only an overall palette, while the guest experience stays a standardised flow with configurable limits. *(client request · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-918)*
- CMS manages multiple sites/venues: branding, colour palette including custom hex codes, fonts, Google Analytics site IDs, production/staging environments. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-393)*
- Guest-app builder: tenant uploads client logo (multiple formats), picks colour themes, app icon and custom font, with a live preview before publishing. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-187)*

`CMS-003` Typography

- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- CMS manages multiple sites/venues: branding, colour palette including custom hex codes, fonts, Google Analytics site IDs, production/staging environments. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-393)*
- Font and image upload guardrails: size/format restrictions and pixel limits (e.g. banner image ≤ 1024px), validated on upload with an explanatory note to the tenant admin, so cursive/bold fonts cannot overflow banners or descriptions. *(agreed · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-188)*
- Guest-app builder: tenant uploads client logo (multiple formats), picks colour themes, app icon and custom font, with a live preview before publishing. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-187)*

`CMS-004` Logo & Assets

- The tenant picks which logo lockup sits in the nav bar and a logo variant (Light, Dark, Duotone) whose colours drive the theme. *(agreed · design review 29 Sep 2026, CFG-4 · Brand logo + Logo palette (Light/Dark/Duotone) · DI-1068)*
- Font and image upload guardrails: size/format restrictions and pixel limits (e.g. banner image ≤ 1024px), validated on upload with an explanatory note to the tenant admin, so cursive/bold fonts cannot overflow banners or descriptions. *(agreed · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-188)*
- Guest-app builder: tenant uploads client logo (multiple formats), picks colour themes, app icon and custom font, with a live preview before publishing. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-187)*

`CMS-005` Theme Editor

- Theme settings: surface style Glass (default) or Solid cards; button style Solid (default), Outline or Pill. *(agreed · design review 29 Sep 2026, CFG-3 · Surfaces (Glass/Solid) and Buttons (Solid/Outline/Pill) · DI-1067)*
- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Per-element colours in the theme editor: pickers for the main call to action, pay button, add to cart, Buy tickets button, links and badges, each with a live contrast warning; left empty they follow the theme. The guest flow itself stays standard. *(agreed · MoM 17 Sep 2026, M17-11 · DI-922)*
- Qossai: white-labelling needs more flexibility, e.g. setting the colour of specific interactive elements such as the "pay now" / "purchase" button independently, not only an overall palette, while the guest experience stays a standardised flow with configurable limits. *(client request · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-918)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*
- CMS manages multiple sites/venues: branding, colour palette including custom hex codes, fonts, Google Analytics site IDs, production/staging environments. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-393)*
- Layout builder: header, footer, logo, bottom-navigation icons and colours are configurable; banner sizing is configurable and promotion blocks are switched on/off by toggle. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-189)*
- Guest-app builder: tenant uploads client logo (multiple formats), picks colour themes, app icon and custom font, with a live preview before publishing. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-187)*

`CMS-006` Component Preview

- Qossai: white-labelling needs more flexibility, e.g. setting the colour of specific interactive elements such as the "pay now" / "purchase" button independently, not only an overall palette, while the guest experience stays a standardised flow with configurable limits. *(client request · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-918)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Reusable page components per venue type are to be documented (e.g. seat-map component for stadiums/amphitheatres, park-map component for attraction venues) so one layout serves many venues with only imagery/data swapped. Documentation pending from Allam. *(open · MoM 20 Aug 2026, 4.10 CMS & White-Label; 6. Open Items · DI-395)*
- Guest-app builder: tenant uploads client logo (multiple formats), picks colour themes, app icon and custom font, with a live preview before publishing. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-187)*

`CMS-007` Page Builder

- The hero banner and marketing layer (images, video, search, browse-by-venue, venue info) is optional and toggled in the white-label builder: on for clients without their own marketing site (Qossai: roughly 30%), off for a lean direct-to-ticket flow. *(agreed · MoM 18 Sep 2026, 4.11 Guest Website UX Review — Page Structure & Hero Banner Flexibility · DI-945)*
- Decision (raised by Qossai): the CMS/website builder supports two modes per client using the same builder — a full landing page plus integrated ticket-sale flow (clients without a website), or B2C-only (header, product cards, footer, checkout) embedded in/linked from an existing site. *(agreed · MoM 21 Aug 2026, 4.9 Website Builder Flexibility — Standalone vs. B2C-Only Configuration · DI-431)*
- Drag-and-drop page builder with a standardised layout (header, footer, hero/card components) that adapts to product type — seat map for seated products, standard flow for general admission. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-394)*
- Custom content pages per venue (e.g. "Plan Your Visit", Accessibility) that follow accessibility guidelines. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-190)*

`CMS-008` Content Blocks

- **Open question.** Reusable page components per venue type are to be documented (e.g. seat-map component for stadiums/amphitheatres, park-map component for attraction venues) so one layout serves many venues with only imagery/data swapped. Documentation pending from Allam. *(open · MoM 20 Aug 2026, 4.10 CMS & White-Label; 6. Open Items · DI-395)*
- Layout builder: header, footer, logo, bottom-navigation icons and colours are configurable; banner sizing is configurable and promotion blocks are switched on/off by toggle. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-189)*

`CMS-009` Navigation & Menus

- The home-screen navigation bar layout is configurable: home/explore/map/buy-tickets in different arrangements. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1087)*
- Six Flags Kidiya reference: fixed header with configurable navigation (logo, Explore/Tickets/Passes, sub-menus), every item toggleable via the CMS. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-424)*
- Allam: the venue's main website is fully venue-managed; after "Book Now" the white-label B2C flow keeps the venue's header/footer branding while product selection, cart and checkout are TICVAI-managed. Header/footer links to non-checkout pages redirect to the main venue site. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-397)*
- Layout builder: header, footer, logo, bottom-navigation icons and colours are configurable; banner sizing is configurable and promotion blocks are switched on/off by toggle. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-189)*

`CMS-010` Media Library

- Font and image upload guardrails: size/format restrictions and pixel limits (e.g. banner image ≤ 1024px), validated on upload with an explanatory note to the tenant admin, so cursive/bold fonts cannot overflow banners or descriptions. *(agreed · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-188)*

`CMS-011` Translations

- A new language is added as a configuration change, not development. Qossai wants a table-driven workflow like his prior project: a translation spreadsheet with a column per language reviewed by native speakers, then fed back through an AI translation pass. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-083)*
- Translation workflow: text entered in English, machine-translated, then reviewed and validated by the tenant's own team in the back office/CMS before publishing; applies to website, POS and mobile app. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-081)*

`CMS-014` Publishing Workflow

- Each client owns its Apple and Google developer accounts; the app is built in the CMS from a published configuration, with an in-platform guide (D-U-N-S number, opening accounts, store listing, store review). *(agreed · MoM 24 Sep 2026, M24-08 · DI-998)*
- The builder flow ends in a Review & Publish step before configuration goes live. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-194)*

`CMS-016` Site Settings

- Guest date picking shows a strip of the next seven days (venue setting dateStripDays, default 7, range 3-31) with a calendar icon that opens the full month for later dates. *(agreed · MoM 17 Sep 2026, M17-08 · DI-920)*
- CMS manages multiple sites/venues: branding, colour palette including custom hex codes, fonts, Google Analytics site IDs, production/staging environments. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-393)*
- One client can run multiple branded sites from the same setup, e.g. two brands sharing a footer but with distinct headers and hero banners. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-110)*

`CMS-017` Domain & Certificate

- Guest web hosting: small tenants run under a subdomain/subpath of the TICVAI domain; larger clients get a dedicated URL on their own domain. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-283)*

`CMS-018` Consent & Legal

- Refund policy shown to guests is tiered and driven by back-office rules per business, e.g. no refund <24h, 50% between 24–48h, 100% >48h. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-192)*
- Configurable FAQ section plus Terms & Conditions, Privacy Policy and Cookie Policy with an accept/deny prompt. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-191)*

`CMS-021` Privacy & Consent Configuration Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`CMS-025` Cookie, Tracking & Digital Technology Registry

- Configurable cookie consent banner (accept/reject) per website; some cookies flagged mandatory (non-rejectable), others optional; templated and configurable in the system. *(client request · MoM 1 Sep 2026, 4.13 Privacy Consent & Cookie Policy · DI-617)*

`CMS-026` Cookie Banner & Preference Center Designer

- Configurable cookie consent banner (accept/reject) per website; some cookies flagged mandatory (non-rejectable), others optional; templated and configurable in the system. *(client request · MoM 1 Sep 2026, 4.13 Privacy Consent & Cookie Policy · DI-617)*
- Configurable FAQ section plus Terms & Conditions, Privacy Policy and Cookie Policy with an accept/deny prompt. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-191)*

`CMS-027` Consent Capture Point & Customer Journey Configuration

- Checkout captures marketing/newsletter opt-in and preferred contact method (email vs phone). *(client request · MoM 1 Sep 2026, 4.13 Privacy Consent & Cookie Policy · DI-616)*

`CMS-031` Privacy Operations Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

`CMS-041` Waiver & Consent Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Waiver dashboard tracks templates (published vs draft) and completion status. Templates can be cloned and are built with drag-and-drop fields (name, DOB, custom fields, T&C checkboxes). *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-570)*

`CMS-042` Waiver Template Library & Master Setup

- Allam: no single standard waiver; a default/pre-set template can be offered, but the builder must stay fully configurable because each business has its own requirements. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-571)*
- Waiver dashboard tracks templates (published vs draft) and completion status. Templates can be cloned and are built with drag-and-drop fields (name, DOB, custom fields, T&C checkboxes). *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-570)*

`CMS-043` Digital Waiver & Form Builder

- Allam: no single standard waiver; a default/pre-set template can be offered, but the builder must stay fully configurable because each business has its own requirements. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-571)*
- Waiver dashboard tracks templates (published vs draft) and completion status. Templates can be cloned and are built with drag-and-drop fields (name, DOB, custom fields, T&C checkboxes). *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-570)*

`CMS-044` Dynamic Fields, Questions & Conditional Logic

- Conditional fields: e.g. ask for the Emirates city only if country is UAE; ask extra questions only if age is below a threshold. Signatory config sets who signs (participant or parent/guardian). *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-572)*

`CMS-045` Signatory, Signature & Guardian Rule Configuration

- Conditional fields: e.g. ask for the Emirates city only if country is UAE; ask extra questions only if age is below a threshold. Signatory config sets who signs (participant or parent/guardian). *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-572)*

`CMS-046` Product, Event & Experience Association

- Waiver is triggered automatically when an associated product is bought; timing is business-configurable: at checkout, post-purchase, or on-site before entry. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-573)*

`CMS-047` Waiver Trigger, Eligibility & Completion Rules

- Waiver is triggered automatically when an associated product is bought; timing is business-configurable: at checkout, post-purchase, or on-site before entry. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-573)*

`CMS-048` Versioning, Effective Dates & Legal Change Control

- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*

`CMS-049` Localization, Branding & Customer Experience Configuration

- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*

`CMS-050` Waiver Approval, Testing & Publication Workspace

- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*

`CMS-051` Waiver Operations Command Center

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Post-launch tracking shows per-participant completion status and delivery channel (email/WhatsApp/SMS), minor/guardian handling, and a verification workspace that flags missing, expired or invalid waivers. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-576)*

`CMS-052` Participant Waiver Status & Tracking

- Post-launch tracking shows per-participant completion status and delivery channel (email/WhatsApp/SMS), minor/guardian handling, and a verification workspace that flags missing, expired or invalid waivers. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-576)*

`CMS-053` Digital Signing & Collection Operations

- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*

`CMS-054` Minor, Guardian & Group Consent Management

- Post-launch tracking shows per-participant completion status and delivery channel (email/WhatsApp/SMS), minor/guardian handling, and a verification workspace that flags missing, expired or invalid waivers. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-576)*

`CMS-055` Waiver Verification & Validation Workspace

- Post-launch tracking shows per-participant completion status and delivery channel (email/WhatsApp/SMS), minor/guardian handling, and a verification workspace that flags missing, expired or invalid waivers. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-576)*

`CMS-056` Missing, Expired & Invalid Waiver Management

- Post-launch tracking shows per-participant completion status and delivery channel (email/WhatsApp/SMS), minor/guardian handling, and a verification workspace that flags missing, expired or invalid waivers. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-576)*
- Qossai: where a waiver is required before entry, an incomplete waiver can block ticket download, activation, check-in or access; ticket and scan screens need a waiver-incomplete state. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-574)*

`CMS-061` Digital Asset Management Command Center

- DAM overview shows total assets by type (images, videos, documents, brand assets); central library browses folders and subfolders (e.g. Marketing -> Campaigns -> Social Media -> Brand). *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-842)*

`CMS-062` Central Digital Asset Library

- DAM overview shows total assets by type (images, videos, documents, brand assets); central library browses folders and subfolders (e.g. Marketing -> Campaigns -> Social Media -> Brand). *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-842)*

`CMS-063` Upload & Asset Ingestion Workspace

- Upload accepts any asset type (image, video, audio, document); folder/collection workspaces group assets without duplicating files. *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-843)*

`CMS-064` Folder, Collection & Workspace Management

- Upload accepts any asset type (image, video, audio, document); folder/collection workspaces group assets without duplicating files. *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-843)*

`CMS-065` Metadata & Taxonomy Management

- Metadata links each asset to its campaign/category (e.g. promo image tagged to a summer campaign) and captures image specifications; tags (season, venue type, audience, location, indoor/outdoor) drive search and filtering. *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-844)*

`CMS-066` Tags, Keywords & Classification

- Metadata links each asset to its campaign/category (e.g. promo image tagged to a summer campaign) and captures image specifications; tags (season, venue type, audience, location, indoor/outdoor) drive search and filtering. *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-844)*

`CMS-067` Advanced Search & Discovery

- Advanced search by name, description or tag; a 360 asset detail view; bulk upload and batch changes (re-tag or re-categorise multiple selected assets at once). *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-845)*

`CMS-068` Digital Asset 360° Profile

- Activity view tracks additions, updates, missing metadata and duplicates; every asset shows a persistent digital asset ID with version control. *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-846)*
- Advanced search by name, description or tag; a 360 asset detail view; bulk upload and batch changes (re-tag or re-categorise multiple selected assets at once). *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-845)*

`CMS-069` Bulk Asset Management Workspace

- Advanced search by name, description or tag; a 360 asset detail view; bulk upload and batch changes (re-tag or re-categorise multiple selected assets at once). *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-845)*

`CMS-070` Asset Activity, Recent Assets & Library Health

- Activity view tracks additions, updates, missing metadata and duplicates; every asset shows a persistent digital asset ID with version control. *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-846)*

`CMS-072` AI Auto-Tagging & Content Understanding

- AI auto-tagging proposes tags with a confidence score shown per tag (e.g. "family" 96%, "children" 94%, "waterpark" 90%). *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-848)*

`CMS-073` Semantic & Natural-Language Asset Search

- Semantic/natural-language search finds images by visual content (e.g. "children playing in the pool"), not only filename or tags. *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-847)*

`CMS-074` Visual Similarity & Related Asset Discovery

- Visual similarity search finds similar stored images; near-duplicate detection flags near-identical uploads (e.g. 99% similarity) for a keep / replace / discard decision. *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-850)*

`CMS-075` Duplicate & Near-Duplicate Management

- Visual similarity search finds similar stored images; near-duplicate detection flags near-identical uploads (e.g. 99% similarity) for a keep / replace / discard decision. *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-850)*

`CMS-076` Asset Version Control & Revision History

- Asset ID persists across versions (e.g. 1.0 -> 1.1); before confirming a replacement the user sees a replacement-impact analysis listing the live channels (kiosk, mobile app, etc.) that use the asset. *(agreed · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-851)*

`CMS-077` Version Comparison & Replacement Impact

- Asset ID persists across versions (e.g. 1.0 -> 1.1); before confirming a replacement the user sees a replacement-impact analysis listing the live channels (kiosk, mobile app, etc.) that use the asset. *(agreed · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-851)*

`CMS-078` Transformation & Rendition Management

- One uploaded image is auto-optimised into channel renditions (mobile app, B2C website, kiosk, etc.); rendition status shows per channel whether each version is ready or missing. *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-849)*

`CMS-079` Rendition Processing & Delivery Readiness

- One uploaded image is auto-optimised into channel renditions (mobile app, B2C website, kiosk, etc.); rendition status shows per channel whether each version is ready or missing. *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-849)*

`CMS-080` AI Quality, Intelligence Review & Recommendations

- AI quality review flags low resolution, missing information, unsupported renditions or inconsistent formatting, with recommended fixes. *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-852)*

`CMS-081` DAM Governance & Rights Command Center

- Governance overview shows assets pending approval vs approved; each asset names business owner, content owner, rights owner and approver; usage rights state where it may be used (e.g. social media yes, third-party distribution no). *(client request · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-853)*

`CMS-082` Asset Ownership & Responsibility Management

- Governance overview shows assets pending approval vs approved; each asset names business owner, content owner, rights owner and approver; usage rights state where it may be used (e.g. social media yes, third-party distribution no). *(client request · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-853)*

`CMS-083` Rights, License & Usage Policy Management

- Governance overview shows assets pending approval vs approved; each asset names business owner, content owner, rights owner and approver; usage rights state where it may be used (e.g. social media yes, third-party distribution no). *(client request · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-853)*

`CMS-084` Asset Approval Workflow Management

- Publishing needs combined validation of approval status, usage rights and channel permissions before an asset can go live on a given channel. *(agreed · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-854)*

`CMS-085` Publication Eligibility & Governance Validation

- Publishing needs combined validation of approval status, usage rights and channel permissions before an asset can go live on a given channel. *(agreed · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-854)*

`CMS-086` Role-Based Asset Access & Permission Management

- Role-based access controls who can discover, preview, download, edit, approve, share or manage assets. *(client request · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-855)*

`CMS-087` Secure Internal & External Sharing

- Secure sharing: password-protected links, watermarking and download restrictions - e.g. an external agency can preview/download an approved rendition but not the original source file. *(client request · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-856)*

`CMS-088` Rights Expiry, Renewal & Usage Impact

- Rights-expiry tracking flags expiring assets and shows where they are in use; audit trail records who extended an expiry and when; AI risk view highlights e.g. an asset expiring while active in several campaigns. *(client request · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-857)*

`CMS-089` Governance Audit Trail & Compliance Evidence

- Rights-expiry tracking flags expiring assets and shows where they are in use; audit trail records who extended an expiry and when; AI risk view highlights e.g. an asset expiring while active in several campaigns. *(client request · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-857)*

`CMS-090` Governance Risk, Compliance & AI Recommendations

- Rights-expiry tracking flags expiring assets and shows where they are in use; audit trail records who extended an expiry and when; AI risk view highlights e.g. an asset expiring while active in several campaigns. *(client request · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-857)*

`CMS-091` Asset Distribution & Delivery Command Center

- Distribution board shows where and when each asset is used (e.g. a hero banner across every sales channel); channel configuration defines which rendition each channel consumes. *(client request · MoM 11 Sep 2026, 4.4 Asset Distribution, Delivery & Integration · DI-858)*

`CMS-092` Asset Usage & Distribution Map

- Distribution board shows where and when each asset is used (e.g. a hero banner across every sales channel); channel configuration defines which rendition each channel consumes. *(client request · MoM 11 Sep 2026, 4.4 Asset Distribution, Delivery & Integration · DI-858)*

`CMS-093` Channel & Distribution Configuration

- Distribution board shows where and when each asset is used (e.g. a hero banner across every sales channel); channel configuration defines which rendition each channel consumes. *(client request · MoM 11 Sep 2026, 4.4 Asset Distribution, Delivery & Integration · DI-858)*

`CMS-095` Asset Replacement & Propagation Management

- Outdated/expired assets are replaced across all live locations at a scheduled time; if a primary asset is unavailable a backup image is substituted so channels never show a broken/missing image. *(client request · MoM 11 Sep 2026, 4.4 Asset Distribution, Delivery & Integration · DI-859)*

`CMS-096` Fallback, Expiry & Distribution Continuity

- Outdated/expired assets are replaced across all live locations at a scheduled time; if a primary asset is unavailable a backup image is substituted so channels never show a broken/missing image. *(client request · MoM 11 Sep 2026, 4.4 Asset Distribution, Delivery & Integration · DI-859)*

`CMS-098` Delivery Monitoring & Integration Health

- Delivery monitoring tracks availability errors and broken references across the distribution network. *(client request · MoM 11 Sep 2026, 4.4 Asset Distribution, Delivery & Integration · DI-860)*

`CMS-101` Help Me Choose

- Help me choose needs a configuration page per venue; AI may propose the question set from the product catalogue for the operator to validate and edit. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W4 Help me choose · DI-1006)*
- "Help me choose" (experience builder) is not a consent step: its questions (yes/no, age, certified or not, etc.) filter the catalogue so only suitable products are shown (Deep Dive Dubai reference). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W4 Help me choose · DI-1005)*
- Help me choose setup per venue: up to 2 questions, 3 answers each (title, one-line description, icon, optional badge e.g. "Best value"), each answer mapped to one booking flow, a result card (title, description, image) per recommendable product, and placement (button above products, pop-up on arrival, off). *(agreed · design review 23 Sep 2026, What the venue sets up in the CMS (per venue) · DI-984)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*

`CMS-102` Site Builder

- The "Category display" configuration control is retired and has no effect: remove it. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W7 Config: Category display · DI-1009)*
- CMS option to list a product (e.g. training courses) with full details but no Book button; instead show "Contact sales to book" with contact details. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W3 View-only products · DI-1004)*
- Each client owns its Apple and Google developer accounts; the app is built in the CMS from a published configuration, with an in-platform guide (D-U-N-S number, opening accounts, store listing, store review). *(agreed · MoM 24 Sep 2026, M24-08 · DI-998)*
- The CMS is a step-based site builder started from the workspace; a preset keeps the minimum path short (modules, booking flows, home sections and mobile tabs proposed), so an operator supplies only a logo, four colours and Publish; aim about 30 minutes to a working site. *(agreed · MoM 24 Sep 2026, M24-05 · DI-997)*
- Confirmed final: cart sliding in from the right or bottom, card size options, and cart-sidebar placement left or right; Qossai specifically liked the compact card size. No further changes requested. *(agreed · MoM 24 Sep 2026, 4.10 Guest Web App — Card Layout & Cart Configuration Confirmed · DI-991)*
- The hero banner and marketing layer (images, video, search, browse-by-venue, venue info) is optional and toggled in the white-label builder: on for clients without their own marketing site (Qossai: roughly 30%), off for a lean direct-to-ticket flow. *(agreed · MoM 18 Sep 2026, 4.11 Guest Website UX Review — Page Structure & Hero Banner Flexibility · DI-945)*
- Decision (raised by Qossai): the CMS/website builder supports two modes per client using the same builder — a full landing page plus integrated ticket-sale flow (clients without a website), or B2C-only (header, product cards, footer, checkout) embedded in/linked from an existing site. *(agreed · MoM 21 Aug 2026, 4.9 Website Builder Flexibility — Standalone vs. B2C-Only Configuration · DI-431)*

`CMS-103` Booking Flows

- Step-indicator style is configurable, the same as on the web: bars, dots, counters or step names. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1093)*
- Existing booking settings stay: step indicator, extras step, seat picker, map view, quantities on add-ons (−/+ stepper, price multiplies), embed mode, hero banner, search in banner, single-event page. Defaults: search in banner off, seat picker = bowl. *(agreed · design review 29 Sep 2026, CFG-6 · Step indicator; Extras step; Seat picker; Map view; Quantities on add-ons; Embed mode; Hero banner; Search in banner; Single-event page · DI-1070)*
- A UI preset (L1–L6, or Custom) picks a bundle of booking-UI settings per venue type. *(agreed · design review 29 Sep 2026, CFG-1 · Preset (UI preset L1-L6, Custom) · DI-1065)*
- Booking-flow settings are set per tenant with a per-venue override; the CMS booking-flow settings screen must show tenant defaults and venue overrides. *(agreed · rev 3 design review 29 Sep 2026, CFG-11 · Where the settings live · DI-1063)*
- On a guest's first booking visit, a four-step coach-mark tour highlights date, time, tickets and basket, with Back, Next / Done and End tour; a "Quick tour" button on the booking page replays it. Setting "Quick tour", default off; first-visit flag kept on the device only. *(agreed · rev 3 design review 29 Sep 2026, REV3-20 · 20. Enable or disable a Quick Tour that describes the customer journey · DI-1060)*
- Multi-location attractions: the guest picks a location first (e.g. Al Barsha, Mirdif, Yas Island, Sharjah); a "Booking at" bar on later booking steps has Change location. On a switch, times and prices refresh and the selection is cleared unless the products share a family. Setting "Location switcher". *(agreed · rev 3 design review 29 Sep 2026, REV3-18 · 18. One tenant with an attraction in several locations; change location · DI-1058)*
- Category tiles (e.g. Permanent exhibition, Temporary exhibitions, Guided tours, Courses & workshops), then that category's tickets with Adult / Child / Student counters. Setting "Ticket categories": Category → subcategory (default) or Flat list (all tickets under category headings). *(agreed · rev 3 design review 29 Sep 2026, REV3-16 · 16. Choose category, then subcategory, configurable in the CMS · DI-1056)*
- Cart & summary options: sidebar fixed right, sidebar left, slide-in right, slide-up bottom, floating cart icon (round basket button with item count opening the slide-in basket), single column. In Arabic the basket stays on the right by default (client confirmed); "Cart side in Arabic" can mirror to left. *(agreed · rev 3 design review 29 Sep 2026, REV3-10 · 10. Cart display: fixed on right, slide bar, icon, bottom; right for Arabic · DI-1051)*
- A time bar above the seat map shows the chosen performance, lets the guest switch show and has Change date; switching releases held seats. Setting "Time bar above seat map", default on. On the selection step, time sits directly under the date, above language & format and tickets. *(agreed · rev 3 design review 29 Sep 2026, REV3-6 · 6. Time selection on top, configurable · DI-1046)*
- The 'view from your seat' box can sit Bottom (default), Right, Left or Top of the seat map (web only); on narrow screens and mobile it is always below the map. Setting "Seat view box". *(agreed · rev 3 design review 29 Sep 2026, REV3-5 · 5. CMS option to show the seat view right, left, top or bottom · DI-1045)*
- Seated events with one on-sale performance go straight to the seat map (Flow 1). Otherwise date and time come first (Flow 2), either as an inline step (timed-ticket style, default) or as a pop-up dialog over the seat map. Setting "Date & time on seat events". *(agreed · rev 3 design review 29 Sep 2026, REV3-4 · 4. Flow 1 (fixed date and time) and Flow 2 (select date, then time, then seat map) · DI-1044)*
- Sign-in (or the guest code when guest checkout is on) is asked when the guest leaves the Add-ons step; the basket is kept. Setting "Ask to sign in": After add-ons (default) or At payment. *(agreed · rev 3 design review 29 Sep 2026, REV3-3 · 3. The sign-in screen should appear after Add-ons · DI-1043)*
- Dated flows reveal in order: date, then time (hidden until a date is picked), then tickets (hidden until a time is picked), with a hint in place telling the guest what to pick next; Continue off until both chosen. Setting "Performance reveal": Date → time → ticket (default) or All at once. *(agreed · rev 3 design review 29 Sep 2026, REV3-2 · 2. Step 1 date, step 2 time (only after the date), step 3 ticket · DI-1042)*
- More than eight times show as compact time tiles, paged with Earlier / Later (Times per page 8/12/24/all, default 24), with day-part chips (All, Morning, Afternoon, Evening) showing counts (filter on by default). Day-part boundaries are venue settings, default before 12:00 / 12:00–17:00 / from 17:00. *(agreed · rev 3 design review 29 Sep 2026, REV3-1 · 1. Many performances should resize and page; filter by morning, afternoon, evening · DI-1041)*
- Card layout is a choice, not free text: Stacked rows (default) · Split rows · Cards across · Poster cards. Card size: Compact (default) · Standard · Large · Extra large. Density: Compact (default) · Standard · Roomy. *(agreed · design review 29 Sep 2026, 6. Booking-flow configuration (CMS-016): card-layout options · DI-1040)*
- The date list in the event banner (for multi-date events) is a setting, "Dates in event banner", off by default. The date picker always sits at the top of the booking step. *(agreed · design review 29 Sep 2026, Settings 19. Why is there a date selection in the header? · DI-1033)*
- Each Adult / Child / Senior / Infant row has an (i) button showing who the ticket is for and what it includes (up to 300 characters). Setting "Extra info on cards", default on. *(agreed · design review 29 Sep 2026, Tickets 6. Extra information for each ticket in the ticket section · DI-1028)*
- Ticket cards, Read more and the listing side panel show tags (e.g. "2 Hours", "Min 1.10 m", "Free adult entry", "Valid 90 days", "Emirates ID"), each with a kind icon (clock, height, free, calendar, id), max 6. Venue-set tags win, else derived from duration, validity, height rule. Setting "Tags on tickets", default on. *(agreed · design review 29 Sep 2026, Tickets 3. 'Read more' should carry tags customisable per ticket type · DI-1025)*
- Cleaning buffer is configurable. Option A: fixed buffer (e.g. 15 min) after every booking. Option B: N cleanings per day; the system places the buffers into the day's schedule and adjusts availability. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W10 Meeting-room cleaning buffer · DI-1012)*
- The "Category display" configuration control is retired and has no effect: remove it. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W7 Config: Category display · DI-1009)*
- Map-based cabana booking stays optional per configuration, since not every operator uses the same flow; it uses the same map back end as theme-park F&B/locations (reusable later for in-park navigation). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W6 Cabanas · DI-1008)*
- CMS option to list a product (e.g. training courses) with full details but no Book button; instead show "Contact sales to book" with contact details. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W3 View-only products · DI-1004)*
- The prototype validated five booking-flow types (dated, multi-park, combo, annual pass, membership) and their skeleton screens; these flows are the basis for the real white-label builder. *(agreed · MoM 24 Sep 2026, 4.8 Guest Web App CMS Prototype — Feedback on Maturity & Scope Expectations · DI-989)*
- Each ticket type gets its own flow: open-dated (no calendar step, straight to guest category/quantity, valid e.g. 30-60 days), dated (date, then product), dated-with-time (date, time, product) and seated (date, time, seat selection). *(client request · MoM 18 Sep 2026, 4.13 Guest Website UX Review — Ticket Type Flows & Seat Map Selection · DI-948)*
- Decision (raised by Qossai): the CMS/website builder supports two modes per client using the same builder — a full landing page plus integrated ticket-sale flow (clients without a website), or B2C-only (header, product cards, footer, checkout) embedded in/linked from an existing site. *(agreed · MoM 21 Aug 2026, 4.9 Website Builder Flexibility — Standalone vs. B2C-Only Configuration · DI-431)*
- Decision: the add-ons step is optional/removable in configuration for products with no add-ons, collapsing the flow to Ticket Selection → Cart → Checkout. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-428)*
- Allam: the venue's main website is fully venue-managed; after "Book Now" the white-label B2C flow keeps the venue's header/footer branding while product selection, cart and checkout are TICVAI-managed. Header/footer links to non-checkout pages redirect to the main venue site. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-397)*

`CMS-104` App Build & Store Publishing

- Each client owns its Apple and Google developer accounts; the app is built in the CMS from a published configuration, with an in-platform guide (D-U-N-S number, opening accounts, store listing, store review). *(agreed · MoM 24 Sep 2026, M24-08 · DI-998)*
- Self-publishing must be guided in-platform (a guided page/instruction flow rather than only a static PDF manual); Qossai suggested an AI chat-based guide that walks the client step by step through DUNS registration and store submission. *(client request · MoM 24 Sep 2026, 4.13 Mobile App Deployment — Apple Developer Account Risk & Client Guidance Approach · DI-994)*
- Each client builds its app package from the CMS once configured and submits it to the App Store and Google Play under its own developer accounts (Apple DUNS); TICVAI never publishes client apps under its own account. *(agreed · MoM 24 Sep 2026, 4.12 / 4.13 Mobile App Deployment Strategy · DI-993)*
- **Open question.** Open: publishing model — each client's own App/Play Store listing vs one universal TICVAI app where the user selects the venue; and a client module with customisation screens plus a CI/CD-linked publish action vs a canvas the client exports and publishes. Softlabs to present pros/cons. *(open · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-251)*
- Qossai: the TICVAI name must always remain visible to end users of a client-branded guest app (e.g. a "Made by TICVAI" credit) and cannot be removed by the client. *(agreed · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-250)*
- The builder flow ends in a Review & Publish step before configuration goes live. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-194)*

## P14 Developer

**Platform-wide**

- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

**Screen by screen**

`DEV-001` API Reference

- The API reference lists every operation added, changed, deprecated or removed per version, with breaking changes marked. *(agreed · MoM 17 Sep 2026, M17-14 · DI-929)*
- API scopes are picked from a list grouped by module ({module}.read / {module}.write), with unlicensed modules shown disabled rather than hidden; the API reference is grouped by licensable module, then contract. *(agreed · MoM 17 Sep 2026, M17-05, M17-12 · DI-926)*
- The developer portal includes a product/data schema reference (field requirements, min/max lengths), an interactive "try it" API tester showing live request/response, an SDK library with sample code in JavaScript, Python, Java and .NET, a Postman collection and full documentation. *(client request · MoM 17 Sep 2026, 4.9 Developer Portal & API Documentation · DI-913)*
- API documentation must be organised by module (which APIs belong to which module), so a client can see exactly which module's APIs to request, e.g. only CRM-related APIs for a CRM integration. *(agreed · MoM 17 Sep 2026, 4.13 Sandbox Environment & Partner Ecosystem Analytics · DI-912)*

`DEV-003` Clients & Credentials

- Abnormal API volume is flagged, not only throttled (calls above the client's baseline, refusals outside the allow-list, calls to unused operations); a production access request requires at least one IP allow-list address. *(agreed · MoM 17 Sep 2026, M17-07 · DI-928)*
- Production access status is shown: sandbox only, requested (pending), approved, or rejected with the reason. Production keys only after certification; the request form says a new production key is issued and the sandbox key stays sandbox. *(agreed · MoM 17 Sep 2026, M17-06 · DI-927)*
- API scopes are picked from a list grouped by module ({module}.read / {module}.write), with unlicensed modules shown disabled rather than hidden; the API reference is grouped by licensable module, then contract. *(agreed · MoM 17 Sep 2026, M17-05, M17-12 · DI-926)*
- API keys can be partner-generated or TICVAI-generated with configurable expiry; sandbox keys are shown and kept separate from production keys, and production access is granted only after certification. *(agreed · MoM 17 Sep 2026, 4.10 Developer Accounts, API Credentials & Sandbox/Production Separation · DI-914)*

`DEV-004` Sandbox

- Production access status is shown: sandbox only, requested (pending), approved, or rejected with the reason. Production keys only after certification; the request form says a new production key is issued and the sandbox key stays sandbox. *(agreed · MoM 17 Sep 2026, M17-06 · DI-927)*
- API keys can be partner-generated or TICVAI-generated with configurable expiry; sandbox keys are shown and kept separate from production keys, and production access is granted only after certification. *(agreed · MoM 17 Sep 2026, 4.10 Developer Accounts, API Credentials & Sandbox/Production Separation · DI-914)*
- The developer portal includes a product/data schema reference (field requirements, min/max lengths), an interactive "try it" API tester showing live request/response, an SDK library with sample code in JavaScript, Python, Java and .NET, a Postman collection and full documentation. *(client request · MoM 17 Sep 2026, 4.9 Developer Portal & API Documentation · DI-913)*

`DEV-006` Usage & Limits

- Abnormal API volume is flagged, not only throttled (calls above the client's baseline, refusals outside the allow-list, calls to unused operations); a production access request requires at least one IP allow-list address. *(agreed · MoM 17 Sep 2026, M17-07 · DI-928)*

`DEV-007` Marketplace Listing

- Production access status is shown: sandbox only, requested (pending), approved, or rejected with the reason. Production keys only after certification; the request form says a new production key is issued and the sandbox key stays sandbox. *(agreed · MoM 17 Sep 2026, M17-06 · DI-927)*

## P15 Kitchen Display

**Platform-wide**

- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Staff-facing POS and tablet UIs always carry TICVAI branding, not client branding. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-296)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

**Screen by screen**

`KIT-001` Kitchen Operations Command Center

- Kitchen Operations Command Center shows live order counts, items pending/firing and kitchen station status. *(client request · MoM 18 Aug 2026, 4.7 Kitchen Operations & Course-Wise Ordering · DI-332)*

`KIT-002` Kitchen Display System (KDS)

- Kitchen display lets cashier/kitchen mark orders ready, handed over or delivered, driving the guest-facing order-status board. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-794)*
- Each kitchen ticket shows a live "fired" timer counting elapsed time since the order was sent (not a countdown); it resets when a course within that ticket is completed/dished out. Not shown for quick-service outlets, which print and prepare immediately. *(client request · MoM 18 Aug 2026, 4.7 Kitchen Operations & Course-Wise Ordering · DI-334)*

`KIT-003` Order Firing & Course Management

- The kitchen pass fires courses (starters before mains), as drawn on the F&B boards. *(agreed · client-design-boards-audit 20 Aug 2026, The finding - course firing · DI-407)*
- Each kitchen ticket shows a live "fired" timer counting elapsed time since the order was sent (not a countdown); it resets when a course within that ticket is completed/dished out. Not shown for quick-service outlets, which print and prepare immediately. *(client request · MoM 18 Aug 2026, 4.7 Kitchen Operations & Course-Wise Ordering · DI-334)*
- Course-wise ordering (mainly fine dining) groups an order by course (starters, main course, dessert) so the kitchen fires each course at the right time. *(client request · MoM 18 Aug 2026, 4.7 Kitchen Operations & Course-Wise Ordering · DI-333)*

`KIT-004` Active Order Management & Fulfilment Journey

- Kitchen display lets cashier/kitchen mark orders ready, handed over or delivered, driving the guest-facing order-status board. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-794)*

`KIT-005` Kitchen Station Workload & Dynamic Routing

- Kitchens are divided into stations (grill, fryer, beverage, dessert, etc.), each mapped to specific printers or KDS devices. Routing rules decide where an item prints/displays by category or item, with a fallback station/device if the primary one is offline or faulty. *(client request · MoM 18 Aug 2026, 4.3 Kitchen & Preparation Stations · DI-323)*

`KIT-007` Guest Collection, Buzzer & Digital Notification

- Kitchen display lets cashier/kitchen mark orders ready, handed over or delivered, driving the guest-facing order-status board. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-794)*
- Quick-service (QSR) orders capture no pickup details: guest orders, pays, gets a receipt/order number and is notified via a KDS-driven order-status board. Takeaway/delivery do need contact and timing details. *(client request · MoM 9 Sep 2026, 4.15 POS Prototype Review - Food & Beverage, Tables & Kitchen Display · DI-790)*

## P16 Venue Analytics

**Platform-wide**

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

**Analytics**

- Finance board: revenue by department and cost centre, shift-closing details, and payment gateway reconciliation, shown as bar and pie charts. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-716)*

**Screen by screen**

`ANL-001` Executive Command Center

- Command centre first section: facility-wide totals for revenue, visitors, transactions and occupancy % (calculated against configured park capacity). *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-698)*
- The platform ships a standard set of default dashboards out of the box, plus the ability for the business to design additional custom dashboards without SQL or programming knowledge. *(agreed · MoM 8 Sep 2026, 4.1 Rationale for a Native BI/Reporting Platform · DI-697)*

`ANL-002` Sales, Revenue & Channel

- Sales board: product/attraction performance by sales channel, discounts, upsell/cross-sell results, deferred vs realised revenue, and sales forecast vs target. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-715)*

`ANL-003` Operational Performance

- Operations board: access-control metrics - total entries, attendance, exits, per-turnstile breakdowns, and park capacity utilisation. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-717)*

`ANL-005` Cost, Margin & Profitability

- Financial reports generated automatically: P&L (revenue per category less cost of sales), balance sheet, trial balance and ledger view, cash flow, revenue and deferred-revenue analytics, site-wise revenue; plus daily/weekly/monthly finance summaries. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-276)*

`ANL-006` Inventory & Waste Intelligence

- Retail intelligence shows sales and outlet performance, top-performing stores, demand forecasting (from retail sales history and online ticket booking trends) and target-vs-actual per outlet (e.g. monthly target vs. achieved, with variance). *(client request · MoM 19 Aug 2026, 4.9 Retail Intelligence & Reporting · DI-368)*

`ANL-007` Guest & Conversion Intelligence

- CRM board: membership/loyalty visit history; retention/churn section flagging inactive customers (e.g. an annual pass holder with no visit last quarter flagged for follow-up); campaign performance and customer behaviour analytics. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-718)*
- Further command-centre sections: revenue by sales channel; capacity utilisation by attraction/inventory item; top products by channel; conversion rate (site visits to completed purchase, cart abandonment, via Google Analytics); customer, membership and loyalty information. *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-700)*

`ANL-008` Demand Forecasting

- Demand forecasts show current sales pace, forecast and remaining opportunity broken down by sales channel; revenue forecasts show drivers and confidence levels. A forecast simulator models a hypothetical change (e.g. a 10% price decrease, reduced operating hours, staffing changes) before it is made. *(client request · MoM 18 Sep 2026, 4.10 AI Forecasting — Attendance, Demand, Revenue & Capacity Forecasting · DI-943)*
- Retail intelligence shows sales and outlet performance, top-performing stores, demand forecasting (from retail sales history and online ticket booking trends) and target-vs-actual per outlet (e.g. monthly target vs. achieved, with variance). *(client request · MoM 19 Aug 2026, 4.9 Retail Intelligence & Reporting · DI-368)*

`ANL-009` AI Assistant & Action Center

- The AI assistant answers natural-language business queries (e.g. "what was yesterday's ticketing revenue?") only within the user's role (a CEO sees full revenue, a cashier does not), shows grounded citations naming the policy or document an answer came from, and keeps conversation context ("compare that to this week"). *(client request · MoM 21 Sep 2026, 4.8 Core AI Platform — AI Assistant (Query & Knowledge) · DI-964)*

`ANL-012` Live Operations Dashboard

- Live operations view shows sales, entries and exits per tenant/venue for multi-tenant setups, with a quick-glance access-control gate status (open / closed / offline gates). *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-699)*

`ANL-014` Attendance & Footfall Intelligence

- Operations board: access-control metrics - total entries, attendance, exits, per-turnstile breakdowns, and park capacity utilisation. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-717)*

`ANL-015` Capacity & Utilization Monitor

- Operations board: access-control metrics - total entries, attendance, exits, per-turnstile breakdowns, and park capacity utilisation. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-717)*
- Further command-centre sections: revenue by sales channel; capacity utilisation by attraction/inventory item; top products by channel; conversion rate (site visits to completed purchase, cart abandonment, via Google Analytics); customer, membership and loyalty information. *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-700)*

`ANL-016` Sales & Channel Performance

- Sales board: product/attraction performance by sales channel, discounts, upsell/cross-sell results, deferred vs realised revenue, and sales forecast vs target. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-715)*
- Further command-centre sections: revenue by sales channel; capacity utilisation by attraction/inventory item; top products by channel; conversion rate (site visits to completed purchase, cart abandonment, via Google Analytics); customer, membership and loyalty information. *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-700)*

`ANL-017` Customer, Membership & Loyalty Pulse

- CRM board: membership/loyalty visit history; retention/churn section flagging inactive customers (e.g. an annual pass holder with no visit last quarter flagged for follow-up); campaign performance and customer behaviour analytics. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-718)*
- Further command-centre sections: revenue by sales channel; capacity utilisation by attraction/inventory item; top products by channel; conversion rate (site visits to completed purchase, cart abandonment, via Google Analytics); customer, membership and loyalty information. *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-700)*

`ANL-019` AI Management Insights

- An AI layer across all dashboards explains why a metric changed (e.g. why revenue dropped on a given day) and recommends management actions from sales, revenue and attendance trends. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-719)*
- Multi-site performance comparison (this month vs last month, or vs the same period last year), and AI management insights that surface possible reasons behind a change (e.g. a drop in attendance or revenue). *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-701)*

`ANL-020` Multi-Site & Performance Comparison

- Multi-site performance comparison (this month vs last month, or vs the same period last year), and AI management insights that surface possible reasons behind a change (e.g. a drop in attendance or revenue). *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-701)*

`ANL-021` Dashboard Library

- Business can build additional dashboards (e.g. separate finance, sales, operations dashboards) with role-based access so only the relevant team can view a given dashboard. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-702)*
- The platform ships a standard set of default dashboards out of the box, plus the ability for the business to design additional custom dashboards without SQL or programming knowledge. *(agreed · MoM 8 Sep 2026, 4.1 Rationale for a Native BI/Reporting Platform · DI-697)*

`ANL-022` Dashboard Creation Wizard

- The platform ships a standard set of default dashboards out of the box, plus the ability for the business to design additional custom dashboards without SQL or programming knowledge. *(agreed · MoM 8 Sep 2026, 4.1 Rationale for a Native BI/Reporting Platform · DI-697)*

`ANL-023` Drag-and-Drop Dashboard Canvas

- Allam shared the itemised dashboard-component document (chart types, drill-down tool, heat map, etc.) with a suggested reference architecture - explicitly a suggestion Softlabs may adopt, adapt or replace. *(agreed · MoM 9 Sep 2026, 4.11 Follow-Ups from Prior Sessions · DI-750)*
- Dashboard creation is drag-and-drop against predefined data sets (revenue, sales quantity, sales channel, department, etc.); the user picks a visual format (bar chart, pie chart, etc.) without writing queries. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-703)*
- The platform ships a standard set of default dashboards out of the box, plus the ability for the business to design additional custom dashboards without SQL or programming knowledge. *(agreed · MoM 8 Sep 2026, 4.1 Rationale for a Native BI/Reporting Platform · DI-697)*

`ANL-024` Widget & Visualization Library

- Allam shared the itemised dashboard-component document (chart types, drill-down tool, heat map, etc.) with a suggested reference architecture - explicitly a suggestion Softlabs may adopt, adapt or replace. *(agreed · MoM 9 Sep 2026, 4.11 Follow-Ups from Prior Sessions · DI-750)*
- Dashboard creation is drag-and-drop against predefined data sets (revenue, sales quantity, sales channel, department, etc.); the user picks a visual format (bar chart, pie chart, etc.) without writing queries. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-703)*

`ANL-025` KPI Builder

- KPI threshold configuration defines normal/warning/critical bands per metric (e.g. capacity below 80% normal, 80-90% warning, above 95% critical), shown as status on the dashboard. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-704)*

`ANL-026` Targets, Thresholds & KPI Status Rules

- KPI threshold configuration defines normal/warning/critical bands per metric (e.g. capacity below 80% normal, 80-90% warning, above 95% critical), shown as status on the dashboard. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-704)*
- Retail intelligence shows sales and outlet performance, top-performing stores, demand forecasting (from retail sales history and online ticket booking trends) and target-vs-actual per outlet (e.g. monthly target vs. achieved, with variance). *(client request · MoM 19 Aug 2026, 4.9 Retail Intelligence & Reporting · DI-368)*

`ANL-027` Data & Filter Configuration

- Date/filter configuration lets a dashboard be filtered by sales channel, department or period. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-705)*
- Dashboard creation is drag-and-drop against predefined data sets (revenue, sales quantity, sales channel, department, etc.); the user picks a visual format (bar chart, pie chart, etc.) without writing queries. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-703)*

`ANL-028` Drill-Down & Interaction Designer

- Allam shared the itemised dashboard-component document (chart types, drill-down tool, heat map, etc.) with a suggested reference architecture - explicitly a suggestion Softlabs may adopt, adapt or replace. *(agreed · MoM 9 Sep 2026, 4.11 Follow-Ups from Prior Sessions · DI-750)*
- Very large drill-down result sets (e.g. 10,000 transactions in a single day) must be handled without the interface crashing or becoming unresponsive. *(agreed · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-710)*
- Drill-down from a high-level figure to transaction detail - yearly sales -> monthly -> daily -> sales channel -> individual transaction -> transaction detail (which customer, which ticket) - only where the data has a genuine hierarchy. *(agreed · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-709)*

`ANL-029` Dashboard Access, Publishing & Versioning

- Dashboards go through an approval step before publishing. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-706)*
- Business can build additional dashboards (e.g. separate finance, sales, operations dashboards) with role-based access so only the relevant team can view a given dashboard. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-702)*

`ANL-031` Report Catalogue & Library

- Report builder provides a library of standard operations/finance reports exportable as PDF or Excel, plus custom reports built drag-and-drop (no SQL) by choosing which data-set fields appear as columns/rows. *(client request · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-708)*
- Report library filterable by site, operating area, sales channel, workstation or user; e.g. Sales Report (payment-method breakdown, totals, voids, deposits, itemised ticket sales) and Payment Summary (per-cashier breakdown). *(agreed · MoM 7 Aug 2026, 21. Dashboards & Reporting · DI-183)*

`ANL-032` Report Creation Wizard

- Report builder provides a library of standard operations/finance reports exportable as PDF or Excel, plus custom reports built drag-and-drop (no SQL) by choosing which data-set fields appear as columns/rows. *(client request · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-708)*

`ANL-034` Field & Column Selector

- Report builder provides a library of standard operations/finance reports exportable as PDF or Excel, plus custom reports built drag-and-drop (no SQL) by choosing which data-set fields appear as columns/rows. *(client request · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-708)*

`ANL-038` Report Layout & Formatting Designer

- Custom report templates (advanced users, SQL/scripting) exported as PDF or Excel; ticket and receipt layouts built in a drag-and-drop template builder placing dynamic variables (guest name, ticket number, QR) on a background image. *(agreed · MoM 7 Aug 2026, 22. Report & Document Template Design · DI-184)*

`ANL-040` Save, Run & Report Results Viewer

- Very large drill-down result sets (e.g. 10,000 transactions in a single day) must be handled without the interface crashing or becoming unresponsive. *(agreed · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-710)*
- Drill-down from a high-level figure to transaction detail - yearly sales -> monthly -> daily -> sales channel -> individual transaction -> transaction detail (which customer, which ticket) - only where the data has a genuine hierarchy. *(agreed · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-709)*

`ANL-042` Report Scheduler

- Reports can be scheduled to defined recipient groups - e.g. a daily closing/summary sales report or shift-closing report emailed each morning to operations, finance or sales - using configurable email templates with the report attached. *(client request · MoM 8 Sep 2026, 4.8 Report Distribution & Scheduling · DI-714)*

`ANL-043` Subscription Manager

- Reports can be scheduled to defined recipient groups - e.g. a daily closing/summary sales report or shift-closing report emailed each morning to operations, finance or sales - using configurable email templates with the report attached. *(client request · MoM 8 Sep 2026, 4.8 Report Distribution & Scheduling · DI-714)*

`ANL-044` Distribution & Delivery Configuration

- Reports can be scheduled to defined recipient groups - e.g. a daily closing/summary sales report or shift-closing report emailed each morning to operations, finance or sales - using configurable email templates with the report attached. *(client request · MoM 8 Sep 2026, 4.8 Report Distribution & Scheduling · DI-714)*

`ANL-045` Export & Download Center

- Report builder provides a library of standard operations/finance reports exportable as PDF or Excel, plus custom reports built drag-and-drop (no SQL) by choosing which data-set fields appear as columns/rows. *(client request · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-708)*

`ANL-052` Ask TICVAI — Natural Language Analytics

- Conversational report building (Qossai): user asks e.g. "show me the top 10 products sold last week"; the AI asks clarifying questions when timeframe, venue or metric are missing instead of guessing or regenerating. *(agreed · MoM 8 Sep 2026, 4.7 AI-Assisted Report & Configuration Generation · DI-712)*

`ANL-053` AI-Generated Dashboard Studio

- Conversational report building (Qossai): user asks e.g. "show me the top 10 products sold last week"; the AI asks clarifying questions when timeframe, venue or metric are missing instead of guessing or regenerating. *(agreed · MoM 8 Sep 2026, 4.7 AI-Assisted Report & Configuration Generation · DI-712)*

`ANL-054` AI Report Generator

- Conversational report building (Qossai): user asks e.g. "show me the top 10 products sold last week"; the AI asks clarifying questions when timeframe, venue or metric are missing instead of guessing or regenerating. *(agreed · MoM 8 Sep 2026, 4.7 AI-Assisted Report & Configuration Generation · DI-712)*

`ANL-056` Root-Cause Analysis Explorer

- An AI layer across all dashboards explains why a metric changed (e.g. why revenue dropped on a given day) and recommends management actions from sales, revenue and attendance trends. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-719)*

`ANL-058` AI Recommendation & Next-Best-Action Center

- An AI layer across all dashboards explains why a metric changed (e.g. why revenue dropped on a given day) and recommends management actions from sales, revenue and attendance trends. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-719)*

`ANL-061` BI & Analytics Administration Command Center

- KPI/benchmarking admin board defines each KPI's target, data sources and rules, and shows why a KPI is failing and what actions could help meet it. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-720)*

`ANL-062` Enterprise KPI Library

- KPI/benchmarking admin board defines each KPI's target, data sources and rules, and shows why a KPI is failing and what actions could help meet it. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-720)*

`ANL-063` KPI Targets, Thresholds & Scorecards

- KPI/benchmarking admin board defines each KPI's target, data sources and rules, and shows why a KPI is failing and what actions could help meet it. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-720)*
- KPI threshold configuration defines normal/warning/critical bands per metric (e.g. capacity below 80% normal, 80-90% warning, above 95% critical), shown as status on the dashboard. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-704)*

`ANL-064` Benchmark & Comparative Analytics Configuration

- KPI/benchmarking admin board defines each KPI's target, data sources and rules, and shows why a KPI is failing and what actions could help meet it. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-720)*

## P17 TICVAI Sign-up

**Platform-wide**

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

**Screen by screen**

`SGN-001` Welcome & Start Your TICVAI Journey

- Onboarding starts from a link on the TICVAI website and walks a structured question set; first section is organisation details: venue name, industry, attraction type, currency, region/country, contact details, business type (private, semi-government, non-profit). *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-809)*

`SGN-002` Customer & Organization Registration

- Onboarding starts from a link on the TICVAI website and walks a structured question set; first section is organisation details: venue name, industry, attraction type, currency, region/country, contact details, business type (private, semi-government, non-profit). *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-809)*

`SGN-003` Venue Type & Business Profile

- Operating model question: attraction, museum, park, event, etc. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-810)*

`SGN-004` Visitor, Capacity & Operational Scale

- Visitor capacity and scale: expected annual/monthly visitors, venue capacity, entrances/exits, number of POS and access-control points, user count, estimated transaction volume, growth forecast. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-811)*

`SGN-005` Sales Channel Assessment

- Sales channels of interest (online, on-site, B2C, B2B/OTA) each with volume estimates. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-812)*

`SGN-006` Ticketing & Product Requirements

- Product/module types they plan to sell: general admission, seat-based, resource management, events, memberships, wallet, etc.; plus guest access/validation methods. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-813)*

`SGN-007` Access, Queue & Visitor Experience Assessment

- Product/module types they plan to sell: general admission, seat-based, resource management, events, memberships, wallet, etc.; plus guest access/validation methods. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-813)*

`SGN-008` Additional Business Module Assessment

- Additional modules needed (F&B, retail, membership/CRM, etc.). *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-814)*

`SGN-009` Integration, Payment & Technical Readiness

- Payment gateway/device integration needs: select from a supported list or specify an unlisted provider. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-815)*

`SGN-010` AI Assessment Summary & Handoff

- The prospect reviews then submits the assessment, which becomes the basis for the system's proposed commercial/licensing model. *(client request · MoM 10 Sep 2026, 4.1 Customer Onboarding & Self-Assessment · DI-816)*

`SGN-011` Recommended Package Overview

- From onboarding data the system proposes a recommended commercial model and tier package (example: a museum recommended per-ticket plus minimum guarantee). *(client request · MoM 10 Sep 2026, 4.7 Package Builder & Module Marketplace · DI-823)*
- Tier thresholds map VSI ranges to tiers (0-30 Essential, 31-60 Professional, 61-80 Enterprise, 81-100 Enterprise Plus) with per-factor sub-thresholds (attendance 100-100,000 = 10 pts; 100,000-500,000 = 40); the system calculates the score and recommends the tier automatically. *(agreed · MoM 10 Sep 2026, 4.2 Venue Size Index (VSI) Model & Tier Threshold Configuration · DI-818)*

`SGN-012` Commercial Model & Tier Selection

- Commercial models, combinable per client: tier-based, tier plus usage, per-ticket, per-transaction, percentage-based, minimum guarantee, hybrid, fixed multi-year contract. *(agreed · MoM 10 Sep 2026, 4.4 Commercial & Licensing Pricing Models · DI-821)*
- Each tier has its own price payable monthly, annually or in advance (cheque/bank transfer), with a configurable trial period; tier-included allowances (e.g. Professional up to 10 POS devices and 20 users) at the same price anywhere within the range. *(client request · MoM 10 Sep 2026, 4.3 Subscription Tiers, Allowances & Usage Thresholds · DI-819)*
- Tier thresholds map VSI ranges to tiers (0-30 Essential, 31-60 Professional, 61-80 Enterprise, 81-100 Enterprise Plus) with per-factor sub-thresholds (attendance 100-100,000 = 10 pts; 100,000-500,000 = 40); the system calculates the score and recommends the tier automatically. *(agreed · MoM 10 Sep 2026, 4.2 Venue Size Index (VSI) Model & Tier Threshold Configuration · DI-818)*

`SGN-013` Module Marketplace

- Module marketplace lists optional add-ons (B2C, B2B, mobile app, virtual queue, CRM, seat management, etc.) with AI recommendations from stated needs (e.g. virtual queue if queue management was flagged). *(client request · MoM 10 Sep 2026, 4.7 Package Builder & Module Marketplace · DI-824)*
- Certified integrations (e.g. BookMyShow, Platinum List, Ticketmaster) are surfaced in a marketplace module that clients can activate after purchasing the core solution. *(agreed · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-136)*

`SGN-014` AI Module & Package Recommendations

- Module marketplace lists optional add-ons (B2C, B2B, mobile app, virtual queue, CRM, seat management, etc.) with AI recommendations from stated needs (e.g. virtual queue if queue management was flagged). *(client request · MoM 10 Sep 2026, 4.7 Package Builder & Module Marketplace · DI-824)*

`SGN-015` Module Detail & Commercial Treatment

- Certified integrations (e.g. BookMyShow, Platinum List, Ticketmaster) are surfaced in a marketplace module that clients can activate after purchasing the core solution. *(agreed · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-136)*

`SGN-016` Module Dependency & Compatibility Manager

- Module dependency check before allowing combinations - e.g. flag that the online/B2C module must be included before enabling virtual queue. *(client request · MoM 10 Sep 2026, 4.7 Package Builder & Module Marketplace · DI-825)*

`SGN-018` Purchase / Trial Journey Selection

- "Try it" is a single shared, pre-configured demo (sample products, working POS/admin sales flow, reporting) entered with shared credentials - evaluation only, cannot sell real tickets; not a per-prospect trial tenant. *(agreed · MoM 10 Sep 2026, 4.11 Demo Environment Scope · DI-831)*

`SGN-019` Contract & Billing Cycle Selection

- After accepting (or negotiating and re-proposing) a commercial model, the purchase agreement captures billing cycle, contract period, invoicing frequency (monthly/annually), legal entity information and payment method (bank transfer, card, etc.). *(client request · MoM 10 Sep 2026, 4.10 Purchase Agreement, Billing Terms & Trial/Demo Environment · DI-830)*

`SGN-020` Billing & Legal Entity Information

- After accepting (or negotiating and re-proposing) a commercial model, the purchase agreement captures billing cycle, contract period, invoicing frequency (monthly/annually), legal entity information and payment method (bank transfer, card, etc.). *(client request · MoM 10 Sep 2026, 4.10 Purchase Agreement, Billing Terms & Trial/Demo Environment · DI-830)*

`SGN-021` Payment Method & Settlement Setup

- After accepting (or negotiating and re-proposing) a commercial model, the purchase agreement captures billing cycle, contract period, invoicing frequency (monthly/annually), legal entity information and payment method (bank transfer, card, etc.). *(client request · MoM 10 Sep 2026, 4.10 Purchase Agreement, Billing Terms & Trial/Demo Environment · DI-830)*

`SGN-022` Order & Commercial Pricing Review

- After accepting (or negotiating and re-proposing) a commercial model, the purchase agreement captures billing cycle, contract period, invoicing frequency (monthly/annually), legal entity information and payment method (bank transfer, card, etc.). *(client request · MoM 10 Sep 2026, 4.10 Purchase Agreement, Billing Terms & Trial/Demo Environment · DI-830)*

`SGN-023` Commercial Agreement, Billable Definition & Customer Acceptance

- After accepting (or negotiating and re-proposing) a commercial model, the purchase agreement captures billing cycle, contract period, invoicing frequency (monthly/annually), legal entity information and payment method (bank transfer, card, etc.). *(client request · MoM 10 Sep 2026, 4.10 Purchase Agreement, Billing Terms & Trial/Demo Environment · DI-830)*

## Superseded

Kept as history; left out of every bundle.

- Qossai's earlier POS prototype is a design and functional reference only, not to be copied. Softlabs is to evaluate it and propose a more efficient, scalable UX, improving usability, layout and functionality. *(agreed · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-001)* — superseded by DI-086
- POS has a global platform search and a proposed "Magic Bar" for quickly reaching frequently used functions. *(client request · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-008)* — superseded by DI-087
- **Open question.** Uncontrolled offline selling of assigned seats, time slots and limited-capacity products is not acceptable. Qossai's channel-specific inventory pools (B2C, B2B, POS, kiosk, mobile each selling only its reserved allocation offline) are to be evaluated; no design approved. *(open · MoM 28 Jul 2026, 16. Proposed Offline Inventory Pooling · DI-014)* — superseded by DI-074
- Language priority: English, Arabic, Russian, Chinese; Spanish and others later. Design must allow additional languages without major redevelopment. *(agreed · MoM 28 Jul 2026, 27. Internationalisation and Arabic Support · DI-020)* — superseded by DI-080
- **Open question.** The shared reference (a cashier-led POS) is a baseline to enhance, not copy; Qossai noted a similar approach might also serve TICVAI's B2B customers. *(open · MoM 31 Jul 2026, 2. Reference UI Flow & Application Vision · DI-058)* — superseded by DI-086
- Flow varies by ticket type (admission, time-slot, seat-assignment): admission goes straight to a quantity selector; seat assignment requires selecting the day, then the time, then the seat. *(client request · MoM 31 Jul 2026, 2. Reference UI Flow & Application Vision · DI-059)* — superseded by DI-116
- F&B selling modelled on a cafe: a single POS handles both order-taking and payment. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-076)* — superseded by DI-105
- Allam: Softlabs need not build a full kitchen display system, only an integration point that sends order information to an existing KDS for display. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-077)* — superseded by CHG-CLN-012
- For white-label apps the focus is which elements are customizable per client (e.g. header, footer, colour scheme, calendar), not redesigning the flow; the same logic applies to the mobile app. *(client request · MoM 31 Jul 2026, 15. Monday UI/UX Session Planning · DI-085)* — superseded by DI-108
- Add-on purchases after entry can either issue a new QR code or extend the existing wristband/QR code ("entitlement add-on"). *(agreed · MoM 5 Aug 2026, 6. Entitlement, QR Codes & Encryption Architecture · DI-139)* — superseded by DI-295
- Parking in the app supports two models: platform-native purchase with a QR scanned by a handheld at the gate, or ANPR integration where the guest enters a plate number that is whitelisted so the barrier opens. *(agreed · MoM 10 Aug 2026, 4.4 Venue Map, Queueing, F&B, Retail & Parking · DI-206)* — superseded by DI-300
- Guest app structure/layout is fixed; tenants customise graphics, colours, fonts and enabled tabs/modules only, with no new custom components; checkout adapts automatically to the configured product type (seated, timed-slot, date-only). *(agreed · MoM 10 Aug 2026, 4.12 B2C App — Customisation, Ownership & Architecture (Q&A) · DI-223)* — superseded by DI-285
- **Open question.** Open: app-store ownership. Qossai's view — tenant publishes under their own Apple/Google developer account with "built by Ticvai" branding embedded; needs a simple flow to enter developer credentials and as automated a submission as possible. *(open · MoM 10 Aug 2026, 4.12 B2C App — Customisation, Ownership & Architecture (Q&A) · DI-224)* — superseded by DI-251
- Qossai: remove the manual role-selection screen after login; route the employee automatically to their role-specific home based on back-office role configuration. *(agreed · MoM 10 Aug 2026, 5.1 Login, Roles & Dashboard · DI-226)* — superseded by DI-249
- Data-dependent forecasting (demand/revenue) cannot be delivered in phase one for lack of history, though its front end, back end and data components can be built. *(agreed · MoM 14 Aug 2026, 1. AI Configuration Assistant — Phase-One Scope · DI-280)* — superseded by ADR-0051
- Decision: the B2C checkout targets a minimal, low-friction 3–4 step flow modelled on Platinum List; full profile capture is deferred to an optional post-purchase step rather than gating checkout. *(agreed · MoM 20 Aug 2026, 4.10 CMS & White-Label; 5. Key Decisions · DI-399)* — superseded by DI-426
- The dashboard designer's component catalogue must be bounded: an itemised list of supported chart types, table components, status/rule widgets, page/board limits and responsive rules (like Power BI/Zoho's bounded canvas). Allam to supply the list. *(agreed · MoM 8 Sep 2026, 4.4 Customizable Component Scope · DI-707)* — superseded by DI-750
- Checkout options are configurable per venue: guest checkout, registered checkout (login or create account) or single sign-on, often several together. Guest checkout captures minimum details (name, mobile, email) without credentials, so a returning guest re-enters details each time. *(agreed · MoM 18 Sep 2026, 4.8 Guest Checkout & Profile Deduplication — Extended Discussion · DI-939)* — superseded by DI-1002
- Allam's standard page structure for white-labelled sites: header (logo, navigation tabs, language selector, cart, account), a category/tab layer (e.g. day tickets, special offers, memberships, F&B, retail), a progress-bar layer, the product selection and summary area, help/policy links, and a footer. *(client request · MoM 18 Sep 2026, 4.11 Guest Website UX Review — Page Structure & Hero Banner Flexibility · DI-944)* — superseded by DI-990
- Allam: ticket/product categories must be displayable in both a horizontal/row layout and a grid layout, chosen by the business in the CMS rather than fixed to one pattern. *(agreed · MoM 18 Sep 2026, 4.12 Guest Website UX Review — Category Display Formats & Cart Interaction Patterns · DI-946)* — superseded by DI-1009
- Adding a product to cart must support both a slide-in-from-the-right panel and a slide-up-from-the-bottom panel; the business chooses which pattern fits its site. *(agreed · MoM 18 Sep 2026, 4.12 Guest Website UX Review — Category Display Formats & Cart Interaction Patterns · DI-947)* — superseded by DI-991
- Chinmay: the guest web app and mobile app are kept functionally identical so a guest without the app can reach nearly the same functionality on the web; mobile mirrors the web workflows, adding venue, map and service features for the in-venue context. *(agreed · MoM 21 Sep 2026, 4.15 Planning — Shift to Build Readiness & UI/UX Sign-Off · DI-970)* — superseded by DI-1086
- The mobile prototype only verifies flows (seat maps, booking steps) and mirrors the web app's configuration settings (density, compact view, etc.); some options may be reduced since not every client needs them. Header/footer and similar elements become editable in the white-label builder. *(agreed · MoM 24 Sep 2026, 4.11 Guest Mobile App — Flow Verification Scope · DI-992)* — superseded by DI-1086
- Plan tab: trip planner taking party size, heights, dates, pace (packed/relaxed), interests and cuisine, producing a proposed itinerary per day with add-ons (e.g. quick pass). *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1021)* — superseded by DI-1098
- The 2D map shows every section in its price colour with a price key; clicking a section zooms into it on the same map. In 3D, clicking a stand switches to 2D zoomed into it. Stadium: no separate "Your fixture" page; a fixture strip tops the seat step and booking opens on the map. *(agreed · design review 29 Sep 2026, Seat map 16. 2D map: show the full seat map, clicking a section shows its seats directly · DI-1031)* — superseded by DI-1003
- Setting "Category display" (Grid / Row strip, default Grid) changes how product cards are laid out. *(agreed · design review 29 Sep 2026, Settings 18. Changing the category display makes no difference · DI-1032)* — superseded by DI-1009
- School trip: pupil stepper, one free teacher/assistant per 10 pupils, invoice estimate, "Requested – quote on its way" (quote in two working days, headcount due 5 days before). Party: child's name and age turning, "Pay deposit AED X now, AED Y on the day". Both: over-package-cap and "Date no longer available" states. *(agreed · design review 29 Sep 2026, 4. School trips and parties (WEB-031) · DI-1038)* — superseded by DI-1104
- Help me choose is a venue configuration: 1–2 questions, answers, and the flow each answer opens, with a result card. Shown as a button, a pop-up on arrival, or off, and as a dark banner under the products ("Choose from the experiences above or let us help you decide", HELP ME CHOOSE). AI proposes sections; venue reviews. *(agreed · rev 3 design review 29 Sep 2026, REV3-11 · 11. Show products based on questions (Help me choose) · DI-1052)* — superseded by DI-1005
- A product can be listed as info only (or hidden): it keeps details and photo, shows an "Info only" / "Not bookable online" label (venue-editable text) and opens its details instead of adding to the basket. Setting "Show info-only products", default on. *(agreed · rev 3 design review 29 Sep 2026, REV3-14 · 14. Show a ticket category with details, with booking on or off in the CMS · DI-1054)* — superseded by DI-1004
- Surf sessions: dropdowns "Choose your experience" (surf, lessons and coaching, swim and play, sauna) and "Select surf level" (beginner to expert), each option with a short description, plus Reset, day-part chips and paging. A four-day calendar (arrows move a week) stacks sessions by time with places left and price per surfer; sold-out greyed. *(agreed · rev 3 design review 29 Sep 2026, REV3-19 · 19. Surf sessions with filters (as on The Wave) · DI-1059)* — superseded by DI-1007
