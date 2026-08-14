# TICVAI — Complete Capability Register

**Version:** 1.0
**Date:** 12 August 2026
**Source:** `Ticvai_matrix_20260621_2.xlsx` — 3,184 requirements, 21 domains, 118 sub-domains
**Companion:** `TICVAI_AI_Application_Register.md` (AI-01 → AI-67)

---

## 1. Purpose

Every requirement in the matrix traced to a capability, a bounded context and a wave.
This is the unit of work: flows, endpoints and pages are built against capabilities,
never against job titles. Actors are compositions of capabilities, validated against a
matrix — they are not a source of diagrams.

**Coverage: 3,184 / 3,184 (100%).** Non-AI capabilities C01–C97 plus AI-01 → AI-67.

### Provenance

| Tag | Meaning | Build status |
|---|---|---|
| `MATRIX` | Traced to a Requirement ID | Build |
| `MOM` | Traced to a dated MoM decision | Build |
| `DESIGN` | Our recommendation, not yet ratified | Not a build item |

---

## 2. Bounded Contexts

| Tier | Context | Domains | Reqs |
|---|---|---|---|
| **Spine** | Tenancy & Org Hierarchy | *(cross-cutting)* | — |
| **Spine** | Identity & AuthZ | 19.2 (partial) | ~90 |
| **Spine** | Product & Entitlement | 1, 5.5 | 342 |
| **Spine** | Order & Payment | 2, 5.1 | 355 |
| **Spine** | Access Control | 3 | 201 |
| **Spine+** | Finance & Ledger | 5.7–5.12, 11 | 327 |
| Satellite | Seating | 21 | 112 |
| Satellite | F&B | 4.6–4.9, 7.2–7.5, 10.1 | 156 |
| Satellite | Retail | 6, 7.1 | 140 |
| Satellite | Promotions & Bundles | 4.1–4.5 | 150 |
| Satellite | Guest Engagement | 5.3, 5.4, 22 | 385 |
| Satellite | Inventory & Procurement | 15, 7.6, 17.6 | 113 |
| Satellite | Maintenance | 17 | 50 |
| Satellite | Resource Management | 1.2 | 84 |
| Satellite | Virtual Queue | 5.6 | 46 |
| Satellite | Accreditation | 12 | 58 |
| Satellite | Device Management | 16 | 60 |
| Satellite | Rentals | 7.6 | 15 |
| Satellite | Redemption & Games | 10.2 | 20 |
| Platform | Control Plane & Licensing | 20 | 59 |
| Platform | Developer Platform | 13 | 94 |
| Platform | AI & Analytics | 8 | 332 |
| Platform | Digital Assets | 23 | 15 |
| Platform | Guest App & Branding | 19.1 | 24 |

---

## 3. Capability Register

### 3.1 Selling — C01–C08, C27–C28, C34, C37

| ID | Capability | Context | Refs | Wave |
|---|---|---|---|---|
| C01 | **Shift & till** — float, deposit box, blind close-out, denomination count, over/short, cash lift, cash add, auto-close, supervisor approval on open and close | Order & Payment | 5.8.x, 5.9.x; 12 Aug §19 | 1 |
| C02 | **Ticket sale** — admission / dated / timed / seated, capacity, add-ons, cart hold-merge-expire, reservation lookup or create, per-ticket owner capture, payment, print/deliver | Order & Payment | 2.1, 2.2, 2.3, 2.13, 2.16 | 1 |
| C03 | **Membership & wallet at POS** — lookup, balance, top-up, loyalty points, linked family, RFID ref | Order & Payment | 2.14, 5.2, 4.3 | 1 |
| C04 | **Post-sale service** — refund, void, exchange, reschedule, upgrade/downgrade, reprint, resend. Dual-auth below threshold, supervisor override above | Order & Payment | 2.9, 2.11, 2.12 | 1 |
| C05 | **F&B quick-service order** — category → item → modifiers → cart → pay | F&B | 4.6, 4.7, 7.2 | 2 |
| C06 | **Table service** — visual table map, covers, open tab, add over visit, split by amount/covers/category | F&B | 4.9, 7.4 | 2 |
| C07 | **KDS handoff** — integration point only, not a full KDS | F&B | 7.5, 10.1 | 2 |
| C08 | **Retail sale** — real-time inventory depletion, blocked offline | Retail | 6.1, 7.1 | 2 |
| C27 | **Rental check-out/check-in** — serial assignment, deposit collect/return, duration, overdue, damage | Rentals | 7.6 | 3 |
| C28 | **Redemption counter** — credit balance, prize redemption, ticket-eater ingest, free-play grants | Redemption & Games | 10.2 | 3 |
| C34 | **Digital waiver capture** — POS, Mobile POS, kiosk, online; guardian consent for minors | Order & Payment | 2.10, 2.15, 22.12 | 2 |
| C37 | **Money card / stored value** — sale, reload, cashout, upgrade-and-load, validity | Order & Payment | 4.3, 6.1 | 2 |

### 3.2 Access Control — C09, C10, C23, C25, C26, C29

| ID | Capability | Context | Refs | Wave |
|---|---|---|---|---|
| C09 | **Access validation** — scan QR/RFID/NFC, dynamic QR refresh, entitlement + deny rules, re-entry, group/media code, optional BLE proximity, offline queue + sequential sync | Access Control | 3.1, 3.2, 3.3 | 1 |
| C10 | **Ticket validity lookup** — read-only, no scan | Access Control | 18.8 | 2 |
| C23 | **Parking ops** — handheld QR, ANPR plate whitelist | Access Control | 3.4 | 3 |
| C25 | **Turnstile mode control** — entry / re-entry / crossover / exit / free rotation / closed | Access Control | 3.2.73 | 2 |
| C26 | **Ticket override at gate** — operator-authorised entry against failed validation, logged | Access Control | 3.2.73 | 2 |
| C29 | **Biometric & ID enrolment** — Face Pass, Face Tag, Emirates ID, fingerprint | Access Control | 3.2.43–44 | 2 |

### 3.3 Catalogue & Entitlement — C20, C79–C81, C84–C86

| ID | Capability | Context | Refs | Wave |
|---|---|---|---|---|
| C20 | **Configuration** — products, price lists, performances, envelopes, access profiles, devices, data mask, users/roles, roles-comparison | Product & Entitlement | 1.1, 1.5 | 1 |
| C79 | **Product lifecycle** — versioning, owners, creators, approvers, responsible departments, retirement | Product & Entitlement | 1.4 | 2 |
| C80 | **Ticket resale marketplace** — listing, transfer, pricing controls, settlement | Product & Entitlement | 1.6 | 3 |
| C81 | **Portfolio & entitlement management** — entitlement bundles, expiry alerts, portfolio optimisation | Product & Entitlement | 5.5 | 2 |
| C84 | **Event & performance management** — creation, grouping, on-demand performances, travel-time logic, projections | Product & Entitlement | 1.3 | 1 |
| C85 | **Pricing & price lists** — per channel, seasonal, calendar-based, components/attributes variant generation | Product & Entitlement | 2.7, 2.8 | 1 |
| C86 | **Promotions & coupons** — individual and master coupons, dynamic offers, rolling discounts, bulk voucher packs | Promotions & Bundles | 3.6, 4.2 | 2 |
| C87 | **Bundles & packages** — fixed, dynamic, mandatory, optional, promotional; bundled pricing and rules | Promotions & Bundles | 3.5, 4.1 | 2 |
| C88 | **Upsell & cross-sell configuration** — rules, placement, channel sync | Promotions & Bundles | 3.7, 4.4 | 2 |
| C89 | **F&B and retail offers** — outlet-level promotions, combo pricing, happy hours | Promotions & Bundles | 4.5 | 3 |
| C90 | **Menu management** — items, modifiers, recipes, availability, production scheduling | F&B | 4.8, 7.3 | 2 |

### 3.4 Finance & Ledger — C41–C50

The largest previously unmapped block. 12 Aug 2026 was a full deep-dive on this.

| ID | Capability | Context | Refs | Wave |
|---|---|---|---|---|
| C41 | **Chart of accounts** — native creation and mapping to an externally maintained client/ERP chart; hierarchy, parent accounts, financial dimensions, profit and cost centres | Finance & Ledger | 5.7; 12 Aug §13–14 | 1 |
| C42 | **Dual-ledger posting** — transaction-level entries for reconciliation plus journal entries for trial balance, P&L and balance sheet; append-only, corrections appended never deleted | Finance & Ledger | 5.11; 12 Aug §6 | 1 |
| C43 | **Tax & VAT engine** — per line item not basket total; tax-on-tax (compound); multi-country structures; discounts inclusive or exclusive of tax; tax exemption by account; tax code matrix import | Finance & Ledger | 5.7; 12 Aug §7 | 1 |
| C44 | **Revenue recognition** — immediate for POS, on redemption for gift cards, straight-line or per-visit for annual passes, breakage on expiry; deferred revenue by visit date; **allocation split builder** across products and legal entities by fixed amount or percentage | Finance & Ledger | 5.12 (120); 12 Aug §8, §16 | 1 |
| C45 | **Settlement & reconciliation** — five-step ingest, parse, match, classify, auto-resolve; **monthly file-based** gateway comparison, not per-transaction API | Finance & Ledger | 5.7; 12 Aug §11, §17 | 2 |
| C46 | **Refund engine** — six-step ledger-to-gateway sequencing; configurable time-banded refund percentages; approver override; partial refunds; **bulk refund** at event or date level with approval; customer-initiated requests | Finance & Ledger | 5.7.91; 12 Aug §9, §18 | 1 |
| C47 | **Payment methods & gateway management** — cash, card, PayPal, bank transfer, virtual credit card, hotel charge, installment, voucher, prepaid; payment drivers per terminal; **payment-status inquiry recovery** for unconfirmed transactions | Order & Payment | 5.1; 12 Aug §12 | 1 |
| C48 | **Financial reporting** — P&L, balance sheet, trial balance, cash flow, deferred revenue and site-wise analytics; exception-based financial approval/controls view; automatable daily, weekly and monthly summaries | Finance & Ledger | 5.7; 12 Aug §21 | 2 |
| C49 | **Manual journal entry & approval** — finance user posts a voucher, finance manager or director approves, only then does it hit the ledger | Finance & Ledger | 11.1; 12 Aug §15 | 2 |
| C50 | **Fiscal setup** — legal entities by country and currency, financial year and period configuration, period close to lock postings, cost centres, statistical groups, ERP integration centre | Finance & Ledger | 5.7; 12 Aug §14 | 1 |

### 3.5 Seating — C51–C55, C91

Whole domain previously unmapped.

| ID | Capability | Context | Refs | Wave |
|---|---|---|---|---|
| C51 | **Seat map builder** — visual designer, sections, rows, seats, aisles, elevation | Seating | 21.1 | 2 |
| C52 | **Seat map import** — SVG import, layout templates, cloning across venues | Seating | 21.2, 21.3 | 2 |
| C53 | **Seat selection & assignment** — manual from map, best-seat assignment, package seat change, dual-screen map | Seating | 21.5 | 2 |
| C54 | **Seat holds, blocks & group reservations** — tracking, temporary holds, blocks, group allocation | Seating | 21.4, 21.6, 21.9 | 2 |
| C55 | **Seating rules & accessibility** — buffer seats, social distancing, accessible seating and companion rules | Seating | 21.7, 21.8 | 2 |
| C91 | **Seat revenue & analytics** — seat categories, envelope pricing, reporting, platform API | Seating | 21.11, 21.12, 21.13 | 3 |

### 3.6 Guest Identity & App — C56–C58, C92

| ID | Capability | Context | Refs | Wave |
|---|---|---|---|---|
| C56 | **Guest authentication** — social login, UAE Pass, OTP, biometric, guest checkout, account linking, MFA, session management. **83 requirements — the single largest sub-domain gap** | Identity & AuthZ | 19.2 | 1 |
| C57 | **White-label branding configuration** — theme, colours, fonts, logos, banners; upload validation with pixel and font limits; publish to config API | Guest App & Branding | 19.1; 10 Aug §31 | 1 |
| C58 | **Guest profile & relationships** — profile data, household and family links, dependants, guardians, merge duplicates, bulk anonymise | Guest Engagement | 5.3, 22.2 | 2 |
| C92 | **Guest app publishing pipeline** — per-tenant build, signing under tenant store accounts, review status, version per tenant per platform | Control Plane | 12 Aug §5 `MOM` | 2 |

### 3.7 Guest Engagement & Marketing — C32–C33, C59–C66, C82–C83

| ID | Capability | Context | Refs | Wave |
|---|---|---|---|---|
| C32 | **Case management & SLA** — assignment to agent, team or queue; severity; escalation; audit | Guest Engagement | 22.3 | 3 |
| C33 | **Campaign workflow** — creator → reviewer → approver → publisher with audit | Guest Engagement | 22.1 | 3 |
| C59 | **Audience segmentation** — rule-based segments, export and activation to campaigns, newsletters, notifications, advertising platforms | Guest Engagement | 22.14 | 3 |
| C60 | **Newsletter & email marketing** — templates, targeting, scheduling, subscriber management, audit | Guest Engagement | 22.4 | 3 |
| C61 | **Notifications & messaging** — omnichannel delivery, dynamic personalisation, event-based triggers, retries, audit | Guest Engagement | 22.9 | 2 |
| C62 | **Reviews & ratings** — collection, moderation, response, escalation | Guest Engagement | 22.5 | 3 |
| C63 | **Surveys & feedback** — design, distribution, incentives, response management | Guest Engagement | 22.7 | 3 |
| C64 | **Gamification & loyalty** — challenges, achievements, tiers, points, rewards, redemption | Guest Engagement | 22.6, 5.4 | 3 |
| C65 | **Consent management** — collection, versioning, withdrawal, data-processing consent, DSAR support | Guest Engagement | 22.13 | 1 |
| C66 | **SEO & content management** — CMS, metadata, sitemaps, search, dynamic pages, audit | Guest Engagement | 22.10, 22.11 | 3 |
| C82 | **Virtual queue** — join, position, wait times, redirect, throttling, reservations for rides and experiences | Virtual Queue | 5.6 | 2 |
| C83 | **Loyalty programme administration** — earn rules, tiers, expiry, statements | Guest Engagement | 5.4 | 3 |
| C93 | **Omnichannel inbox** — unified conversation history across WhatsApp, web chat, app chat, Messenger, Instagram, email, SMS; unified guest identification; agent workspace | Guest Engagement | 22.8 | 2 |

### 3.8 Back of House — C11–C18, C24, C30–C31, C78, C94

| ID | Capability | Context | Refs | Wave |
|---|---|---|---|---|
| C11 | **Work order & asset** — lifecycle, timer, photo-first capture, priority, schedule | Maintenance | 17.1, 17.4, 18.2, 18.3 | 2 |
| C12 | **Safety, inspection & incident** — inspections, incidents, compliance records | Maintenance | 17.3, 17.5, 18.4 | 2 |
| C13 | **Inventory operations** — lookup by name or barcode, stock across stores and warehouses, counts, goods receipt, movements | Inventory | 15.1, 15.2, 18.7 | 3 |
| C14 | **Procurement** — requisition → dept approval → PO with quotation compare → GRN → issue; three-way matching; par-level auto-draft | Inventory | 15.3, 17.6 | 3 |
| C15 | **Approvals** — approve / reject / return / RFI; trail; **delegation, out-of-office rerouting, parallel, consensus** | *(cross-cutting)* | 11.1, 18.6 | 1 |
| C16 | **Roster & attendance** — shift view, clock in/out, leave, break with replacement scheduling | Resource Mgmt | 18.9, 1.2 | 2 |
| C17 | **Guest assistance** — venue info, announcements, attraction status, supervisor contacts | *(employee app)* | 18.9 | 2 |
| C18 | **Lost & found** — staff log, desk match, guest claim, tracking | Guest Engagement | 10 Aug §4.6 `MOM` | 2 |
| C24 | **Offline overlay** — auto-detect, visible indicator, cash-only, capacity products blocked, venue-offline alert | *(cross-cutting)* | 2.3.1; 31 Jul §11 | 1 |
| C30 | **Accreditation issuance** — application → review → approval → credential → access assignment → expiry → revocation, for staff, contractors, vendors, media, VIPs, government | Accreditation | 12.1 | 3 |
| C31 | **Device lifecycle** — register, enrol, provision, remote configure, monitor, maintain, firmware, security, retire | Device Mgmt | 16.1–16.9 | 3 |
| C78 | **Resource management & scheduling** — bookable staff, venues, equipment, rooms and rental items; skills, availability calendars, max performances, block reasons, contract templates, labour costing | Resource Mgmt | 1.2 | 3 |
| C94 | **Maintenance planning & analytics** — preventive schedules, auto work-order generation, spare parts, reporting | Maintenance | 17.2, 17.7 | 3 |

### 3.9 Platform — C21, C35–C36, C74–C77, C95–C97

| ID | Capability | Context | Refs | Wave |
|---|---|---|---|---|
| C21 | **Reporting** — cashier-scoped sales summary, admission summary, report library filterable by site / operating area / channel / workstation / user; self-service builder; scheduled reports; subscriptions | *(cross-cutting)* | 6.1, 8.7 | 2 |
| C35 | **Staff authentication modes** — card login, RFID login, auto-login, AD credentials, change user, workstation lock. `REF` — needs matrix validation | Identity & AuthZ | `REF` | 2 |
| C36 | **Password & credential policy** — complexity, expiry, history, retries, end-validity date | Identity & AuthZ | 7.1 | 1 |
| C74 | **Subscription & licensing** — self-service onboarding, plans, licensing models, enforcement, renewal, usage and quota monitoring, billing | Control Plane | 20.1–20.3, 20.5–20.7 | 2 |
| C75 | **Module marketplace** — catalogue, per-tenant enablement, entitlement enforcement | Control Plane | 20.4 | 2 |
| C76 | **Developer platform** — portal, API keys, sandbox, developer role management, rate limits, business API coverage | Developer Platform | 13.1–13.3 | 3 |
| C77 | **Digital asset management** — upload, versioning, rights, distribution, search | Digital Assets | 23.1 | 3 |
| C95 | **Tenant & cell provisioning** — registry, region placement, cell deployment, migration fan-out, per-cell version register | Control Plane | `DESIGN` + 10 Aug, 12 Aug | 1 |
| C96 | **Customer support & helpdesk** — tenant-facing support cases, knowledge base | Control Plane | 20.8 | 3 |
| C97 | **Operations command centre** — real-time cross-module dashboard: attendance, occupancy, queues, attraction status, incidents, device health, staffing, sales | AI & Analytics | 8.9 | 3 |

### 3.9b Local-first POS — C102–C104

Created by [ADR-0013](../adr/0013-local-first-point-of-sale.md).

| ID | Capability | Context | Wave |
|---|---|---|---|
| C102 | **Catalogue bundle publication** — compute, version, sign, delta, publish; client-side verify and atomic apply with rollback | Product & Entitlement | **1** |
| C103 | **Inventory lease management** — grant, renew, release, expire, reconcile; two-level sub-leasing via edge node | Product & Entitlement | **1** |
| C104 | **Catalogue staleness policy** — bound beyond which a terminal refuses to trade rather than transacting against stale data | Order & Payment | **1** |

### 3.9c Tenant experience — C105–C109

Surfaced by the client UI/UX boards, 13 August.

| ID | Capability | Context | Provenance | Wave |
|---|---|---|---|---|
| C105 | **Tenant content management** — homepage layout builder, banners, promo blocks, custom pages, FAQs, multi-language policies | White Label Builder | `DESIGN` — design reference | **1** |
| C106 | **Tenant config publishing** — draft → review → preview → publish, version history with restore | White Label Builder | `DESIGN` | **1** |
| C107 | **Multi-currency display** — display currency separate from settlement currency | Guest App | `DESIGN` | 2 |
| C108 | **Training & knowledge base** — SOPs, manuals, videos, progress, due dates | Employee App | `DESIGN` — **no requirement, no MoM** | 3 |
| C109 | **Employee recognition** — kudos, categories, recipients | Employee App | `DESIGN` — **no requirement, no MoM** | 3 |

**C105 and C106 are Wave 1** because the White Label Builder is how a tenant configures the
guest app, and no tenant can go live without it. C108 and C109 are not scope until they
appear in the matrix or a MoM.

### 3.10 AI — AI-01 → AI-67

See `TICVAI_AI_Application_Register.md`. **399 requirements, 12.5% of the matrix,
spread across 19 of 21 domains.** AI-61 → AI-66 (governance) are Wave 1 preconditions;
nothing else AI ships before them.

---

## 4. Coverage by Domain

| # | Domain | Reqs | Capabilities | Coverage |
|---|---|---|---|---|
| 1 | Ticketing Catalogue | 312 | C20, C78–C81, C84 + AI-09/10/11/24/32/42/55 | 100% |
| 2 | Ticketing Sales | 343 | C01–C04, C34, C85, C22 + AI-04/07/30/31/40 | 100% |
| 3 | Admission and Access | 201 | C09, C23, C25, C26, C29, C86–C88 + AI-36/37/46 | 100% |
| 4 | Bundles and Promotions | 229 | C05–C07, C37, C86–C90 + AI-22/23/45 | 100% |
| 5 | F&B & Guest Management | 411 | C01, C41–C50, C58, C81–C83, C47 + AI-20/26/38/41/53 | 100% |
| 6 | Retail POS | 78 | C08, C21, C37 | 100% |
| 7 | F&B POS | 151 | C05–C08, C27, C36, C90 + AI-47 | 100% |
| 8 | Unified Operations Dashboard | 332 | C21, C97 + AI-19/28/35/44/57/58/61–65 | 100% |
| 9 | Games & F&B Integration | 25 | C07, C28 | 100% |
| 10 | Approval Workflows | 80 | C15, C49 + AI-48/62 | 100% |
| 11 | Accreditation | 58 | C30 | 100% |
| 12 | Developer & API Mgmt | 94 | C76 + AI-67 | 100% |
| 13 | Inventory Management | 98 | C13, C14 + AI-21/43 | 100% |
| 14 | Device Management | 60 | C31 | 100% |
| 15 | Maintenance & Safety | 50 | C11, C12, C94 | 100% |
| 16 | Employee Mobile App | 50 | C10–C17 + AI-06 | 100% |
| 17 | Guest Mobile App & Branding | 107 | C56, C57, C92 + AI-02/03 | 100% |
| 18 | Subscription & Licensing | 59 | C74, C75, C96 + AI-27/59/60 | 100% |
| 19 | Seat Mgmt & Venue Mapping | 112 | C51–C55, C91 + AI-11/25/39/54 | 100% |
| 20 | Marketing & CRM | 319 | C32, C33, C59–C66, C93 + AI-03/12–18/33/34/50–53 | 100% |
| 21 | Digital Asset Management | 15 | C77 + AI-56 | 100% |

**Total: 3,184 / 3,184 — 100%**

---

## 5. Register Totals

| | Count |
|---|---|
| Non-AI capabilities | **109** (C01–C109) |
| AI applications | **67** (AI-01 → AI-67) |
| **Total capabilities** | **176** |
| Human actors | 33 |
| Bounded contexts | 24 |
| Domains | 21 |
| Sub-domains | 118 |
| Requirements | 3,184 |

### By wave

| Wave | Non-AI | AI | Total |
|---|---|---|---|
| 1 | 27 | 6 | **33** |
| 2 | 41 | 9 | **50** |
| 3 | 29 | 52 | **81** |

---

## 6. Wave 1 — The Build Set

Everything else waits on these.

| ID | Capability | Why Wave 1 |
|---|---|---|
| C95 | Tenant & cell provisioning | Every cell and migration depends on it. Longest lead time, unowned since 30 Jul |
| C56 | Guest authentication | 83 reqs; every guest flow starts here |
| C36 | Password & credential policy | Identity spine |
| C20 | Configuration | Nothing is sellable until products exist |
| C84 | Event & performance management | Capacity and scheduling substrate |
| C85 | Pricing & price lists | Component/attribute variant generation is structural |
| C81 | Portfolio & entitlement management | Entitlement ≠ identity; settled 05 Aug |
| C02 | Ticket sale | The vertical slice |
| C01 | Shift & till | No sale without a till |
| C03 | Membership & wallet at POS | Cross-venue balance model |
| C04 | Post-sale service | Refund path touches the ledger |
| C47 | Payment methods & gateway | Including status-inquiry recovery |
| C09 | Access validation | The vertical slice, offline |
| C24 | Offline overlay | Cross-cutting on C02/C05/C08/C09 |
| C41 | Chart of accounts | Ledger cannot post without it |
| C42 | Dual-ledger posting | Orders write into it from day one |
| C43 | Tax & VAT engine | Per line, compound, multi-country |
| C44 | Revenue recognition | 120 reqs; allocation split builder |
| C46 | Refund engine | Ledger-to-gateway sequencing |
| C50 | Fiscal setup | Legal entities, periods, close |
| C15 | Approvals | Refund, price override, journal all route through it |
| C57 | White-label branding config | Guest app build pipeline depends on it |
| C65 | Consent management | PDPL/GDPR; gates AI-66 |
| C21 | Reporting *(core)* | Cashier and admission summaries |
| AI-61…66 | AI governance | Preconditions for every AI application |

---

## 7. Open Questions Arising

| Question | Owner |
|---|---|
| **C35 staff authentication modes is `REF`** — RFID/card login materially affects POS and gate throughput but has no matrix requirement. Confirm or drop | Qossai |
| **C80 ticket resale marketplace (19 reqs) has zero MoM coverage** — never discussed in any session | Chinmay |
| **C56 guest authentication is 83 requirements** — the largest single sub-domain, and the only MoM coverage is a passing mention of auth options on 03 Aug | Chinmay |
| **C44 revenue recognition rules** — Allam directed cross-checking the reference manuals for rules beyond the matrix (12 Aug §8). Narrow documented exception to the source-of-truth hierarchy | Chinmay — ongoing |
| Four domains still unworkshopped — Accreditation (58), Device Mgmt (60), Developer/API (94), Rentals (15) | Chinmay — schedule |
