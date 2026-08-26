# TICVAI — External Dependency Register

**Hardware · Third-Party Software · On-Location Integration**

**Version:** 2.0
**Date:** 12 August 2026
**Supersedes:** `TICVAI_Hardware_Dependency_Register.md` v1.0
**Source:** `Ticvai_matrix_20260621_2.xlsx` (Functionality + Integrations sheets) · MoM decisions 30 Jul – 12 Aug 2026

---

## 1. Change Log from v1.0

| Change | Reason |
|---|---|
| **Added Class S — third-party software dependency** | 194 requirements depend on external systems we neither build nor buy |
| **Added Class T — on-location infrastructure** | Distinguishes venue-site dependency from device dependency |
| **Virtual Queue reclassified** | Wait-time accuracy is a third-party *feed*, not TICVAI hardware. No lab device needed — a conforming mock does |
| **Digital signage added as a device class** | 5.6.33 requires live queue display; absent from the Integrations sheet |
| **Virtual Waiting Room added** | Zero matrix requirements; exists only in the MoM record |
| **Fast Pass reclassified** | Cross-context entitlement with a consumption counter, not a queue feature |

---

## 2. Dependency Classes

Three questions, three different answers, three different mitigations:

| Class | Question | Mitigation | Reqs |
|---|---|---|---|
| **H — Hardware** | Do we need a physical device to build or accept this? | Hardware lab + driver abstraction | 998 |
| **S — Third-party software** | Do we depend on an external system we don't control? | Adapter layer + sandbox credentials | 194 |
| **T — On-location** | Do we need a real venue, network or site infrastructure? | Pilot venue + deliberate WAN severing | 316 (subset of H) |

Overlapping — Access Control is all three. What matters is that each demands a different
mitigation, and a register that only tracks hardware will under-plan the other two.

---

## 3. Class H — Hardware

### 3.1 Device classes

| Class | Devices | On Integrations sheet? |
|---|---|---|
| H-A | Turnstile readers, podium terminals, gate controllers, handhelds | Yes |
| H-B | RFID, NFC, barcode/QR scanners, magnetic stripe, wristband encoders | Yes |
| H-C | Facial readers, fingerprint scanners, Emirates ID readers | Yes |
| H-D | Ticket printers (Boca), receipt printers, card printers, mobile printers (Zebra BT) | Yes |
| H-E | Payment terminals, cash drawers, customer displays, deposit boxes | Yes |
| H-F | POS terminals, tablets, iPads, mobile/Flying POS | Partial |
| H-G | Self-service kiosks, TVMs, operator kiosks | Yes |
| H-H | Kitchen display screens, kitchen printers | Yes |
| H-I | **ANPR cameras, barrier controllers** | **No** |
| H-J | **Queue/people-counting sensors, occupancy sensors, BLE beacons** | **No** |
| H-K | **Ticket-eater machines, game readers, redemption terminals** | **No** |
| H-L | **Electronic lockers** | **No** |
| H-M | **Digital signage displays** | **No** |
| H-N | Device management across all of the above | — |

**Five classes appear in requirements but not on the Integrations sheet** — H-I, H-J,
H-K, H-L, H-M. Either the sheet is incomplete or these are out of scope. Both answers
are acceptable; the ambiguity is not.

### 3.2 Tier 1 — Device-blocked (21 sub-domains, 316 reqs)

| Domain | Sub-domain | Reqs | Classes |
|---|---|---|---|
| Admission and Access | **Access Control System** | **125** | A, B, C, D, G |
| Ticketing Sales | **Front Gate Sales** | **45** | B, D, E, F |
| Ticketing Sales | Ticket Media | 17 | B, D, F, G |
| Admission and Access | Ticket Media | 10 | B, D |
| Admission and Access | Parking Integration | 2 | **I** |
| Ticketing Sales | Ticketing POS and Kiosks | 2 | E, F |
| Ticketing Sales | Flying POS | 1 | F, G |
| F&B & Guest Mgmt | Cash Handling | 9 | E, F |
| F&B & Guest Mgmt | Shift opening and closing | 10 | E, F |
| F&B POS | Kitchen Display | 10 | H |
| Games & F&B | Game & Ride Payment & Redemption | 20 | B, E, G, **K** |
| Games & F&B | Kitchen Display & Inventory Sync | 5 | H |
| Device Management | *(all 9 sub-domains)* | 60 | A, B, D, F, G, N |

### 3.3 Tier 2 — Device-dependent for acceptance (25 sub-domains, 682 reqs)

Buildable against simulators; not signable without real devices. Largest entries:

| Sub-domain | Reqs | Classes |
|---|---|---|
| Retail POS \| Wallet | 78 | F, G |
| Ticketing Sales \| Call Center Sales | 67 | F, G |
| F&B POS \| Retail POS | 62 | A, F |
| Accreditation \| Reporting and Dashboards | 58 | B, D |
| F&B POS \| Table Reservation | 52 | B, F, **L** |
| **F&B & Guest Mgmt \| Virtual Queue** | **46** | **B, C, M** — see §5 |
| Bundles \| Wallet | 38 | B, E, F, G |
| Inventory Management \| Inventory Management | 38 | B |
| Bundles \| F&B POS - Core Ordering | 37 | F, G, H |
| Ticketing Sales \| Order Management | 36 | C, D, F |
| Ticketing Sales \| Sales Channels | 33 | B, D, E, F, G |
| F&B & Guest \| Portfolio & Entitlement | 30 | B, **L** |
| Ticketing Sales \| Membership | 23 | B, C, F, G |
| Inventory \| Warehouse Management | 22 | B |
| Marketing \| Digital Waivers & Signature | 20 | F, G |
| Bundles \| F&B POS - Menu Management | 19 | F, H |
| Ticketing Sales \| Digital Waiver Management | 18 | F, G |
| F&B POS \| Inventory Mgmt Integration | 15 | B, **L** |
| F&B & Guest \| Payment Methods | 12 | E, F, H |
| Unified Ops \| Operations Command Center | 10 | A, F, G — device health |
| Maintenance \| Asset Management | 8 | B |
| Bundles \| F&B POS - Modifiers | 6 | F |
| Employee App \| Asset Scanning · Ticket Scanning · Core | 14 | B |
| F&B & Guest \| Wallet · Receipt | 7 | D, E, H |

---

## 4. Class S — Third-Party Software

**194 requirements across 65 sub-domains** depend on external systems TICVAI neither
builds nor hosts. Different risk profile from hardware: no procurement lead time, but
sandbox access, credentials, rate limits and vendor roadmaps are outside our control.

### 4.1 External system classes

| Class | Systems | Reqs |
|---|---|---|
| **S-1 Payment** | Stripe gateway + device, NI N-Genius + device, DCT, payment-status inquiry APIs | ~35 |
| **S-2 Identity** | UAE Pass, Azure AD, MFA provider, Apple ID, Google ID, Al Hosn, SSO/SAML | ~25 |
| **S-3 Distribution** | OTAs and resellers (Viator, Klook, Headout, GetYourGuide), channel manager, B2B partner APIs | ~30 |
| **S-4 Messaging** | WhatsApp Business, SMS gateway, email gateway | ~20 |
| **S-5 Enterprise** | ERP (SAP), Oracle Accounting, Salesforce, chart-of-accounts mapping, three-way matching | ~30 |
| **S-6 Wallets** | Apple Wallet, Google Wallet | ~8 |
| **S-7 Venue systems** | **Third-party queue/camera systems**, KDS vendors, locker systems (Gantner, Metra), third-party F&B, third-party availability platforms | ~25 |
| **S-8 Platform services** | SIEM, APM, weather (Visual Crossing), dynamic pricing (Digonex), City Pass / Go City | ~12 |
| **S-9 Government** | DET, DCT, Emirates ID verification | ~9 |

### 4.2 Highest concentration

| Sub-domain | S-reqs | Systems |
|---|---|---|
| Ticketing Sales \| Pricing | 23 | ERP/SAP invoicing and reconciliation, B2B credit blocking, OTA channel manager |
| Ticketing Sales \| Call Center Sales | 13 | Payment links via WhatsApp/SMS/email, B2C engine |
| F&B & Guest \| Accounting | 11 | ERP export, invoice delivery, credit memos |
| Ticketing Catalogue \| Ticket Types | 8 | Alternative codes for third-party systems |
| Developer & API \| Reporting and Dashboards | 8 | Partner API surface |
| Retail POS \| Wallet | 7 | Payment and reporting integrations |
| Admission and Access \| Access Control System | 6 | Turnstile vendor SDKs, external ticket activation |
| F&B POS \| Table Reservation | 6 | Third-party reservation channels |

### 4.3 Standard integration pattern — settled

10 Aug §83: Chinmay asked whether all third-party integrations follow one pattern.
**Confirmed approach: TICVAI exposes a standard inbound API; the client's chosen
third-party system feeds into it. Direct integration with a named vendor is bespoke
work, quoted separately.**

This is the correct default and should be applied uniformly — it converts an unbounded
vendor matrix into one interface plus optional paid adapters.

**Exception, already agreed:** payment gateways require **full end-to-end integration
consuming all relevant APIs, not just the happy path** (12 Aug §12) — including
payment-status inquiry to recover orders where a success response never arrived, and a
background reconciler for on-site terminal failures.

---

## 5. Queue Management — Three Distinct Systems

Previously conflated in the MoM record. **CF-33.**

| | System | Dependency | Reqs | Owner |
|---|---|---|---|---|
| **Q1** | **Virtual Queue** — ride and attraction queues, Fast Pass, wait times, reservations, no-shows | **S-7** for wait-time data + **H-B/H-C** for entry validation + **H-M** for signage | 46 *(38 unique IDs)* | Product |
| **Q2** | **Virtual Waiting Room** — traffic throttling at on-sale; branded queue page above a configurable concurrent threshold (~500), batched release at 200–300/min, session preservation | **None** — in-house infrastructure | **0 in matrix** | Dinesh |
| **Q3** | **Chat queues** — agent assignment, service levels, workload balancing | S-4 | 2 | CRM |

### 5.1 The conflict

| Source | Statement |
|---|---|
| 31 Jul, Decisions | *"Built-in queue management will be developed in-house rather than sourced from a third party"* |
| 31 Jul §80 | In-house *"so that traffic entering the site can be throttled from the back office itself"* → **Q2** |
| 05 Aug §11 | *"Queue management will be scoped once the high-level architecture is finalized, with Dinesh's team owning this area"* → reads as **Q2** |
| 10 Aug §4.4, §4.11 | Live wait times *"typically depends on a third-party camera/sensor system at the venue"*; TICVAI exposes a standard API for any third-party to push into → **Q1, third-party fed** |

As written, 31 Jul says in-house and 10 Aug says third-party fed. They reconcile only if
31 Jul is read as Q2 — which the decision line does not say.

**Recommended resolution:** Q2 is in-house infrastructure owned by Dinesh. Q1 is a
product module where TICVAI builds the queue engine and exposes an inbound API; sensor
and camera data comes from the venue's chosen third party. Both prior decisions then
stand unamended.

### 5.2 Consequence for the lab

Virtual Queue needs **no sensor hardware in the lab** — a conforming mock feed against
the inbound API is sufficient. It does need scanning devices (H-B, H-C) for queue entry
validation and a signage display (H-M) for queue calls.

### 5.3 Fast Pass is not a queue feature

An **entitlement with a consumption counter**, spanning four contexts:

| Ref | Context |
|---|---|
| 3.2.40, 3.2.60 | Access control — fast pass line access; *Silver wristband limited to 3 accesses, system counts usage* |
| 7.4.9 | F&B POS — Fast Pass products |
| 4.6.34 | Kitchen order prioritisation by Fast Pass status |
| 5.6.x | Queue priority tiers |

**Model in the Product & Entitlement spine, not in the queue module.** Modelled inside
Virtual Queue, the wristband counter and kitchen prioritisation both break.

---

## 6. Class T — On-Location Infrastructure

Distinct from device dependency. Needs a real site, not just real hardware.

| Requirement | Why site-dependent | Refs |
|---|---|---|
| **Offline gate validation** | The failure mode is a real network dropping mid-transaction at a real gate. Cannot be proven on a bench | 3.2.x; 31 Jul §7 |
| **Venue edge nodes** | Local SQLite replicating access rules down and scans up; survives WAN loss | 31 Jul §146 `MOM` |
| **BLE proximity verification** | Confirms the operator is physically at the gate while scanning | 31 Jul §112 |
| **Turnstile rotation and anti-passback** | Depends on real physical throughput | 3.2.73 |
| **Venue-offline alerting** | Requires a venue that can actually go offline | 31 Jul §148 |
| **Queue sensor placement** | Accuracy depends on physical camera positioning | 10 Aug §4.11 |
| **Network topology per venue** | Standalone servers, access points, local switching | Reference architecture |

**A pilot venue is a Phase 1 requirement.** The vertical slice — *configure a timed
product → sell at POS → validate at gate offline → sync* — is not provable without one.

---

## 7. New Capabilities

| ID | Capability | Class | Refs | Wave |
|---|---|---|---|---|
| **C98** | **Virtual waiting room** — concurrency threshold detection, branded queue page, position and wait estimate, batched release, session preservation, guaranteed confirmation and delivery on completion | Infrastructure | 31 Jul §86; 10 Aug §113 `MOM` | **1** |
| **C99** | **Queue data ingestion API** — standard inbound interface for third-party queue systems and people-counting sensors | S-7 | 10 Aug §4.11 `MOM` | 2 |
| **C100** | **Digital signage integration** — live queue information and queue calls | H-M | 5.6.33 | 3 |
| **C101** | **Third-party integration adapter framework** — one inbound pattern, per-vendor adapters as bespoke work | S-all | 10 Aug §83 `MOM` | 1 |

**C98 is Wave 1 and has zero matrix requirements.** It exists only in the MoM record, it
is the mechanism that keeps the platform standing at 15,000 peak concurrent during an
on-sale, and it would have been missed entirely by a matrix-driven scope.

---

## 8. Matrix Defect

**Requirement IDs 5.6.1 through 5.6.8 appear twice with entirely different text.**
46 rows, 38 unique IDs. The first set is prose-style; the second is standard
*"System shall…"* form.

This breaks traceability — a citation to "5.6.4" is ambiguous. **Recommend auditing the
full matrix for duplicate IDs before it is used as the acceptance baseline.**

---

## 9. Risks

| Risk | Class | Impact | Mitigation |
|---|---|---|---|
| **Hardware model list outstanding** (12 Aug §24) | H | Blocks driver selection, lab procurement, estimates — gates 316 reqs | **Escalate** |
| **Turnstile SDK outstanding** (05 Aug) | H | Blocks the largest single sub-domain (125 reqs) | **Escalate** |
| Five device classes absent from Integrations sheet | H | Parking, sensors, game readers, lockers, signage may be unscoped and unbudgeted | Confirm in/out |
| **CF-33 queue ownership unresolved** | H+S | Q1 and Q2 have different owners, timelines and dependency profiles | Resolve before design |
| Payment gateway sandbox access | S-1 | End-to-end recovery flows untestable without it | Request sandbox credentials now |
| UAE Pass integration approval | S-2 | Government onboarding has lead time | Start the process early |
| OTA partner API access | S-3 | Each reseller has its own onboarding | Sequence by commercial priority |
| No pilot venue identified | T | Vertical slice unprovable | Identify with TICVAI |
| Duplicate requirement IDs | — | Traceability and acceptance ambiguity | Audit matrix |

---

## 10. Actions

| # | Action | Owner | Status |
|---|---|---|---|
| 1 | Exact hardware models and reference numbers | **Qossai / Allam** | **Outstanding — 12 Aug** |
| 2 | Turnstile and hardware SDK documents | **Qossai / Allam** | **Outstanding — 05 Aug** |
| 3 | Resolve CF-33 — Q1 vs Q2 ownership and scope | Both | New |
| 4 | Confirm scope: parking, sensors, game readers, lockers, signage | Qossai / Allam | New |
| 5 | Identify pilot venue for on-location testing | Qossai / Allam | New |
| 6 | Payment gateway sandbox credentials (Stripe, NI) | Allam | New |
| 7 | Define driver interface — access control and payment | Chinmay | High |
| 8 | Define the standard third-party inbound API pattern (C101) | Chinmay | High |
| 9 | Specify and procure Priority 1 lab | Dinesh | High |
| 10 | Build device simulators for CI ahead of hardware | Backend | High |
| 11 | Audit matrix for duplicate requirement IDs | Chinmay | New |
