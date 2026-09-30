# TICVAI development plan

> **Purpose:** the complete plan for building TICVAI: what is built, in what order, by whom, by when, and at what cost in hours
> **Owner:** Chinmay Parab
> **Status:** Current, 30 September 2026. Supersedes the timeline in `six-month-plan-29-september.md`, whose decisions 1–13 still stand.
> **Sources:** numbers from `tools/build-plan-deck.py` (workbook `handoff/TICVAI - Build Plan.xlsx`), the Block A schedule from `tools/derive-block-a-schedule.py`, and the task sheet `handoff/service-docs/tasks.csv`. Deck: https://claude.ai/artifact/NzvBoTU53zNbwCouMgz4ch

## 1. Summary

- **When:** Monday 5 October 2026 to Friday 2 April 2027, in nine sprints of three weeks (the last is two).
- **What:** seven apps, 31 modules in 7 packages, 2,660 operations, 2,445 screens. 3,153 of the client's 3,165 in-scope requirements are specified.
- **Effort:** about **13,500 hours** (16,171 points at 0.84 hours a point).
- **Team:** 14 people. Chinmay Parab leads and is not counted in capacity.
- **Finish:** 23 April 2027 at normal hours. **Finishing on 2 April needs about 1,000 overtime hours**, 2 to 6 hours a week per person.
- **The constraint is the back end in Block A.** Screens are built by 20 November. They are wired end to end as the back end lands, between 24 December and 11 January.
- **Every AI function ships inside the six months.** Each works on day one and learns from the venue's own data.

## 2. The seven apps

| App | Screen sets | Who uses it | First built |
|---|---|---|---|
| **Guest App** | Website (P01), mobile app (P02), kiosk (P05) | Guests before and during a visit | Web and mobile in Block A; kiosk in B1 |
| **POS** | Terminal and tablet (P04), Kitchen Display (P15) | Cashiers, kitchen | Block A |
| **Scanner** | Turnstile and handheld (P07) | Gate staff | B1 |
| **Staff App** | Floor operations (P06) | Venue staff | B1 (waves 1–2), B2 (wave 3) |
| **Venue Management** | Back office (P08), CMS and flow builder (P13), analytics (P16), support console (P12), accreditation web (P11) | Venue operators | Setup screens and CMS in Block A; the rest B1–B3 |
| **TICVAI main controller** | Platform console (P09), tenant sign-up (P17), developer portal (P14) | TICVAI staff, new tenants, partners' developers | B1–B3 |
| **Partner Portal** | Partner and reseller portal (P10) | Hotels, travel agents and other resellers | B2 |

The Partner Portal became the seventh app on 30 September. It is drawn two ways first, POS-style and website-style; the client picks one, and it is built in B2.

## 3. Timeline

| Phase | Dates | What is built |
|---|---|---|
| **Block A** | 5 Oct – 20 Nov 2026 (35 working days) | POS with Kitchen Display; Guest Web; Guest App (Mobile v4 with the Plan tab); the CMS flow builder; Venue Management setup screens; the platform kernel and offline machinery; the AI gateway, concierge, Help me choose, translations, the planner agent and the baseline layer |
| **Block A tail** | to 11 Jan 2027 | Back-end work that does not fit 35 days, and wiring the screens to it (section 5) |
| **B1** | 23 Nov 2026 – 1 Jan 2027 | Scanner; Staff App waves 1–2; Kiosk; remaining CMS steps; Venue Management waves 1–2 and the first wave-3 modules; TICVAI console waves 1–2; Sign-up; the AI action pipeline, forecasting and fraud baselines |
| **B2** | 4 Jan – 12 Feb 2027 | Partner portal; Support; Accreditation; Developer Portal; Staff App wave 3; Venue Management wave 3; recommendations and the configuration assistant |
| **B3** | 15 Feb – 2 Apr 2027 | The rest of Venue Management and the console, including the AI console; Analytics and the analytics assistant; hardening |

Holidays counted: 1–3 December (Commemoration and National Day), 1 January, and Eid al-Fitr around 9–11 March (to be confirmed).

### 3.1 Sprints

| Sprint | Dates | Block | Capacity (h) | Planned (h) |
|---|---|---|---|---|
| 1 | 5 Oct 2026 – 23 Oct 2026 | A | 1,392 | 982 |
| 2 | 26 Oct 2026 – 13 Nov 2026 | A | 1,392 | 1,144 |
| 3 | 16 Nov 2026 – 4 Dec 2026 | A ends 20 Nov, B1 starts | 1,226 | 885 |
| 4 | 7 Dec 2026 – 25 Dec 2026 | B | 1,632 | 1,393 |
| 5 | 28 Dec 2026 – 15 Jan 2027 | B | 1,523 | 1,506 |
| 6 | 18 Jan 2027 – 5 Feb 2027 | B | 1,632 | 1,629 |
| 7 | 8 Feb 2027 – 26 Feb 2027 | B | 1,632 | 1,632 |
| 8 | 1 Mar 2027 – 19 Mar 2027 | B | 1,306 | 1,306 |
| 9 | 22 Mar 2027 – 2 Apr 2027 | B | 1,088 | 1,088 |

Holidays counted: 1 Dec 2026 Commemoration Day; 2 Dec 2026 National Day; 3 Dec 2026 National Day; 1 Jan 2027 New Year; 9 Mar 2027 Eid al-Fitr; 10 Mar 2027 Eid al-Fitr; 11 Mar 2027 Eid al-Fitr. Eid dates are to be confirmed.

### The build order: phases, end to end

One order from 5 October to the end: plumbing, then the foundation everything reads, the sale path, the per-module operations, engagement, and reporting last. Block A takes it from the tickets (each ticket's phase), B1 to B3 from each module's phase. A screen is built against the mock server and connected as its services land.

**Back end**

| Phase | Starts | Ends | Hours (A / B) | Main modules | People |
|---|---|---|---|---|---|
| 0 Plumbing | 5 Oct 2026 | 28 Dec 2026 | 306 / 0 | Foundation & Setup, Identity, Roles & Security, Tenancy, Venues & Devices, Transport, Reporting & Analytics | Hrushikant Patkar, Tanmay Dukhande, Pranay Shinde, Pradnya Yeram |
| 1 Foundation | 19 Oct 2026 | 24 Mar 2027 | 273 / 684 | Subscription & Licensing, Identity, Roles & Security, White Label & CMS, Approval Workflows, Platform Operations | Tanmay Dukhande, Hrushikant Patkar, Deep Khanvilkar, New full-stack developer 2 |
| 2 Commerce | 21 Oct 2026 | 5 Apr 2027 | 510 / 1,652 | Admission & Access Control, Ticketing Catalogue & Products, Orders & Reservations, Pricing, Promotions & Bundles, Finance, Ledger & Tax | Tanmay Dukhande, Pranay Shinde, Deep Khanvilkar, Hrushikant Patkar |
| 3 Operations | 28 Oct 2026 | 19 Apr 2027 | 415 / 750 | Food & Beverage, Foundation & Setup, Inventory & Procurement, Resources & Capacity, Accreditation | Hrushikant Patkar, Deep Khanvilkar, Pranay Shinde, Tanmay Dukhande |
| 4 Engagement | 5 Oct 2026 | 10 May 2027 | 177 / 2,881 | AI & Intelligence, Marketing & CRM, Foundation & Setup | Kalpita Mejari, Second AI engineer, Pranay Shinde, Deep Khanvilkar |
| 5 Reporting | 21 Dec 2026 | 3 May 2027 | 34 / 58 | Reporting & Analytics, Foundation & Setup | Hrushikant Patkar, Tanmay Dukhande, Chinmay Patkar, Sanket Keluskar |

**Front end**

| Phase | Starts | Ends | Hours (A / B) | Main modules | People |
|---|---|---|---|---|---|
| 0 Plumbing | 5 Oct 2026 | 5 Oct 2026 | 2 / 0 | White Label & CMS | Chitrangi Mestry |
| 1 Foundation | 5 Oct 2026 | 17 Mar 2027 | 158 / 883 | Subscription & Licensing, Approval Workflows, Identity, Roles & Security, White Label & CMS, Tenancy, Venues & Devices | Chitrangi Mestry, Pradnya Yeram, Pallavi Sawant, New full-stack developer 1 |
| 2 Commerce | 6 Oct 2026 | 19 Mar 2027 | 491 / 1,951 | Ticketing Catalogue & Products, Orders & Reservations, Admission & Access Control, Pricing, Promotions & Bundles, Wallet & Cashless | Chitrangi Mestry, Pradnya Yeram, Pallavi Sawant, Chinmay Patkar |
| 3 Operations | 16 Oct 2026 | 16 Apr 2027 | 315 / 1,012 | Rentals, Food & Beverage, Games & Rides, Accreditation, Resources & Capacity | Pradnya Yeram, Chitrangi Mestry, Pallavi Sawant, Chinmay Patkar |
| 4 Engagement | 22 Oct 2026 | 30 Apr 2027 | 141 / 630 | Marketing & CRM, AI & Intelligence, Foundation & Setup, White Label & CMS, Orders & Reservations | Surendra, Chitrangi Mestry, Pallavi Sawant, Pradnya Yeram |
| 5 Reporting | 26 Oct 2026 | 3 May 2027 | 33 / 191 | Reporting & Analytics, Foundation & Setup | New full-stack developer 1, New full-stack developer 2, Chinmay Patkar, Pradnya Yeram |

The rules behind the order, and how new tickets join the ones in OpenProject: `handoff/service-docs/TICKET-STRUCTURE.md`. Every link, service by service and module by module: `handoff/service-docs/TICKET-LINKS.md`.

## 4. How the plan is measured

- **Points** come from each screen's specification (operations, components, states, navigation, offline: 1 to 8 points), plus 2.2 points per back-end operation.
- **Pace** is Block A's plan of record: 3,018 points in 35 days for nine developers. That is 9.6 points per developer per day, so one point is about 0.84 hours. The measured pace replaces it on 23 October and the plan is regenerated.
- **Hours** are points times 0.84. AI engine work (models, pipelines, the learning layer) is sized in engineer-weeks by the AI review and converted at the same rate.
- **Names:** Block A comes from the task sheet. Block B is placed by a scheduler that follows skill and experience. **Loads are uneven on purpose.**
- A re-plan is a rerun of the generators, not a re-estimate.

## 5. Block A in detail

**1,056 tasks, 3,412 points, 696 operations.** The schedule is derived from the task sheet: build order, dependencies and each person's pace. Front-end tasks may start before their back end, because screens build against the generated API client and the mock server. They finish only when the back end they wire to has landed.

| Who | Block A points | Screens built | Work ends |
|---|---|---|---|
| Pradnya Yeram (POS, KDS, guest app) | 244 | 9 Nov | wired by 17 Dec |
| Chitrangi Mestry (guest app, web, white label) | 286 | 9 Nov | wired by 17 Dec |
| Chinmay Patkar (guest web, white label, back-end helper) | 399 | 20 Nov | 6 Jan |
| Pranay Shinde, Tanmay Dukhande (back end) | 441 – 446 | — | 24 Dec |
| Deep Khanvilkar (back-end helper, tasks up to 5 points) | 292 | — | 28 Dec |
| Hrushikant Patkar (back end, DevOps) | 535 | — | 11 Jan |
| Pallavi Sawant, Sanket Keluskar, Surendra (Venue Management) | 175 – 291 | 20 Nov | 11 Jan, waiting on the Venue Management back end |
| Kalpita Mejari, second AI engineer (AI engine) | 33 and 28 engineer-days | — | 20 Nov |

**Why the tail.** One developer covers about 335 points in 35 days. The back-end owners carry 440–535, including the platform kernel the system-design review added: tenant routing, idempotency, outbox and relay, the payment adapter, audit and observability.

**How to shorten it.** The two new developers take back-end tasks from 23 November. Platform tasks off the first purchase path (release flags, migration fan-out) move into B1 on purpose.

**Block A epics beyond the screens:**
- **Setup:** CI, environments, the database and migration runner, seed data, API clients, sign-in, observability.
- **Platform kernel:** request kernel and tenant routing, durable idempotency, outbox and relay, the order-paid saga, payment adapter and webhook, audit, release flags, row-level policies, observability, migration fan-out.
- **Offline:** the offline journal, signed bundles and leases, `syncOrders` with quarantine, POS-to-kitchen routing.
- **AI engine:** gateway and governance, the baseline-then-learn layer, day-one suggestions, the concierge, Help me choose question sets, translations, the planner agent, evaluation and the promotion alert.

**Sprint 1 target (by 23 October):** one web purchase and one offline POS cash sale, end to end.

## 6. Packages and modules

| Package | Modules | Requirements | Screens | Operations | Hours | Completion | Lead |
|---|---|---|---|---|---|---|---|
| **Platform Foundation** | 8 | 563 | 425 | 453 | 2,613 | 24 Mar 2027 | Hrushikant Patkar |
| **Ticketing & Guest Commerce** | 8 | 866 | 867 | 908 | 3,641 | 1 Apr 2027 | Tanmay Dukhande |
| **Food, Beverage & Retail** | 4 | 224 | 216 | 267 | 1,034 | 6 Apr 2027 | Pradnya Yeram |
| **Venue Operations** | 7 | 411 | 464 | 507 | 1,967 | 19 Apr 2027 | New full-stack developer 2 |
| **Finance & Insights** | 2 | 393 | 117 | 120 | 498 | 3 May 2027 | Hrushikant Patkar |
| **Customer & Marketing** | 1 | 421 | 219 | 264 | 940 | 22 Apr 2027 | Pranay Shinde |
| **AI & Intelligence** | 1 | 287 | 137 | 141 | 2,863 | 10 May 2027 | Kalpita Mejari |

"Completion" is at normal hours. Dates after 2 April are brought in with overtime. In the module tables, A is Block A and B is Block B.

### 6.1 Platform Foundation

Everything the apps stand on: sign-in, tenants and venues, devices, licensing, approvals, the public API.

| Module | Requirements | Screens A / B | Operations A / B | Hours A / B | Sprints | Completion | Lead | Team |
|---|---|---|---|---|---|---|---|---|
| Foundation & Setup | 0 | 0 / 0 | 0 / 0 | 840 / 0 | 1-6 | 22 Jan 2027 | Hrushikant Patkar | Hrushikant Patkar, Surendra, Sanket Keluskar, Tanmay Dukhande |
| Identity, Roles & Security | 144 | 9 / 22 | 37 / 52 | 83 / 162 | 1-8 | 19 Mar 2027 | Deep Khanvilkar | Deep Khanvilkar, Surendra, Tanmay Dukhande, Chitrangi Mestry |
| Tenancy, Venues & Devices | 126 | 5 / 30 | 18 / 37 | 46 / 137 | 1-8 | 17 Mar 2027 | New full-stack developer 2 | New full-stack developer 2, New full-stack developer 1, Hrushikant Patkar, Tanmay Dukhande |
| Platform Operations | 4 | 0 / 12 | 0 / 51 | 7 / 126 | 1-8 | 19 Mar 2027 | Pallavi Sawant | Pallavi Sawant, Pradnya Yeram, Pranay Shinde, New full-stack developer 1 |
| Subscription & Licensing | 105 | 2 / 174 | 10 / 138 | 23 / 650 | 1-9 | 24 Mar 2027 | New full-stack developer 2 | New full-stack developer 2, Hrushikant Patkar, Tanmay Dukhande, New full-stack developer 1 |
| Approval Workflows | 90 | 2 / 106 | 8 / 45 | 23 / 280 | 1-9 | 22 Mar 2027 | Pradnya Yeram | Pradnya Yeram, Pranay Shinde, Pallavi Sawant, Chitrangi Mestry |
| Developer Portal & Public API | 80 | 3 / 21 | 8 / 23 | 14 / 93 | 1-8 | 19 Mar 2027 | Chitrangi Mestry | Chitrangi Mestry, New full-stack developer 2, New full-stack developer 1, Hrushikant Patkar |
| Digital Asset Management | 14 | 1 / 38 | 10 / 16 | 26 / 104 | 1-5 | 8 Jan 2027 | Surendra | Surendra, Tanmay Dukhande, New full-stack developer 2, Hrushikant Patkar |

### 6.2 Ticketing & Guest Commerce

What a guest buys and how: catalogue, pricing, seats and maps, orders, payments, wallet, the branded storefront and app.

| Module | Requirements | Screens A / B | Operations A / B | Hours A / B | Sprints | Completion | Lead | Team |
|---|---|---|---|---|---|---|---|---|
| Ticketing Catalogue & Products | 266 | 40 / 170 | 55 / 182 | 175 / 719 | 1-9 | 22 Mar 2027 | Tanmay Dukhande | Tanmay Dukhande, Pallavi Sawant, New full-stack developer 1, Pranay Shinde |
| Pricing, Promotions & Bundles | 105 | 15 / 150 | 29 / 124 | 78 / 533 | 1-9 | 25 Mar 2027 | Tanmay Dukhande | Tanmay Dukhande, Pallavi Sawant, Chinmay Patkar, Deep Khanvilkar |
| Seat Management & Venue Maps | 100 | 12 / 93 | 20 / 55 | 73 / 272 | 1-8 | 18 Mar 2027 | Hrushikant Patkar | Hrushikant Patkar, Pradnya Yeram, Pallavi Sawant, Surendra |
| Orders & Reservations | 269 | 30 / 140 | 57 / 162 | 211 / 662 | 1-9 | 25 Mar 2027 | Pranay Shinde | Pranay Shinde, Chitrangi Mestry, Deep Khanvilkar, Pradnya Yeram |
| Payments | 9 | 4 / 51 | 6 / 42 | 26 / 187 | 1-8 | 18 Mar 2027 | Pranay Shinde | Pranay Shinde, Chitrangi Mestry, Surendra, Tanmay Dukhande |
| Wallet & Cashless | 52 | 5 / 105 | 17 / 49 | 44 / 353 | 1-9 | 22 Mar 2027 | New full-stack developer 2 | New full-stack developer 2, Sanket Keluskar, Chinmay Patkar, New full-stack developer 1 |
| White Label & CMS | 65 | 32 / 8 | 78 / 1 | 210 / 16 | 1-5 | 7 Jan 2027 | Chitrangi Mestry | Chitrangi Mestry, Tanmay Dukhande, Deep Khanvilkar, Chinmay Patkar |
| Transport | 0 | 11 / 1 | 21 / 10 | 63 / 21 | 1-9 | 1 Apr 2027 | Deep Khanvilkar | Deep Khanvilkar, Hrushikant Patkar, Sanket Keluskar, Chinmay Patkar |

### 6.3 Food, Beverage & Retail

Selling at the venue: F&B with the kitchen display, retail, rentals, stock and purchasing.

| Module | Requirements | Screens A / B | Operations A / B | Hours A / B | Sprints | Completion | Lead | Team |
|---|---|---|---|---|---|---|---|---|
| Food & Beverage | 95 | 37 / 37 | 87 / 54 | 276 / 212 | 1-10 | 5 Apr 2027 | Pradnya Yeram | Pradnya Yeram, Hrushikant Patkar, Deep Khanvilkar, Sanket Keluskar |
| Retail | 14 | 5 / 4 | 14 / 11 | 43 / 30 | 1-9 | 1 Apr 2027 | Pranay Shinde | Pranay Shinde, Chitrangi Mestry, Pradnya Yeram, Chinmay Patkar |
| Rentals | 0 | 0 / 106 | 0 / 43 | 0 / 288 | 8-10 | 6 Apr 2027 | Pradnya Yeram | Pradnya Yeram, Chitrangi Mestry, New full-stack developer 1, Chinmay Patkar |
| Inventory & Procurement | 115 | 2 / 25 | 7 / 51 | 21 / 165 | 1-9 | 31 Mar 2027 | Tanmay Dukhande | Tanmay Dukhande, Pranay Shinde, Pallavi Sawant, Chitrangi Mestry |

### 6.4 Venue Operations

Running the venue day to day: gates and access, accreditation, capacity, staff, maintenance, rides, queues.

| Module | Requirements | Screens A / B | Operations A / B | Hours A / B | Sprints | Completion | Lead | Team |
|---|---|---|---|---|---|---|---|---|
| Admission & Access Control | 108 | 23 / 149 | 38 / 208 | 101 / 730 | 1-9 | 2 Apr 2027 | Pallavi Sawant | Pallavi Sawant, Chinmay Patkar, Hrushikant Patkar, New full-stack developer 2 |
| Accreditation | 58 | 0 / 72 | 0 / 47 | 0 / 224 | 6-10 | 14 Apr 2027 | Deep Khanvilkar | Deep Khanvilkar, Surendra, Pallavi Sawant, New full-stack developer 2 |
| Resources & Capacity | 92 | 7 / 55 | 15 / 46 | 38 / 208 | 1-10 | 12 Apr 2027 | Hrushikant Patkar | Hrushikant Patkar, Pradnya Yeram, Chitrangi Mestry, New full-stack developer 2 |
| Workforce & Staff | 27 | 0 / 34 | 2 / 47 | 5 / 173 | 1-10 | 13 Apr 2027 | Chinmay Patkar | Chinmay Patkar, Tanmay Dukhande, Hrushikant Patkar, Sanket Keluskar |
| Maintenance & Safety | 75 | 1 / 28 | 1 / 41 | 7 / 170 | 1-10 | 12 Apr 2027 | New full-stack developer 2 | New full-stack developer 2, Chitrangi Mestry, Sanket Keluskar, Pranay Shinde |
| Games & Rides | 14 | 0 / 81 | 3 / 37 | 6 / 225 | 1-10 | 19 Apr 2027 | Pallavi Sawant | Pallavi Sawant, Pranay Shinde, New full-stack developer 1, Sanket Keluskar |
| Virtual Queue | 37 | 8 / 6 | 11 / 11 | 34 / 47 | 1-10 | 13 Apr 2027 | Hrushikant Patkar | Hrushikant Patkar, New full-stack developer 1, Chinmay Patkar, Pradnya Yeram |

### 6.5 Finance & Insights

The money and the numbers: ledger, VAT and e-invoicing, reports and analytics.

| Module | Requirements | Screens A / B | Operations A / B | Hours A / B | Sprints | Completion | Lead | Team |
|---|---|---|---|---|---|---|---|---|
| Finance, Ledger & Tax | 204 | 9 / 18 | 18 / 54 | 49 / 148 | 1-10 | 5 Apr 2027 | Tanmay Dukhande | Tanmay Dukhande, Hrushikant Patkar, Pradnya Yeram, Pallavi Sawant |
| Reporting & Analytics | 189 | 9 / 81 | 17 / 31 | 52 / 250 | 1-11 | 3 May 2027 | Hrushikant Patkar | Hrushikant Patkar, New full-stack developer 1, New full-stack developer 2, Chinmay Patkar |

### 6.6 Customer & Marketing

Knowing and reaching the guest: CRM, segments, campaigns, loyalty, support.

| Module | Requirements | Screens A / B | Operations A / B | Hours A / B | Sprints | Completion | Lead | Team |
|---|---|---|---|---|---|---|---|---|
| Marketing & CRM | 421 | 33 / 186 | 60 / 204 | 177 / 763 | 1-10 | 22 Apr 2027 | Pranay Shinde | Pranay Shinde, Deep Khanvilkar, Tanmay Dukhande, Surendra |

### 6.7 AI & Intelligence

The AI gateway and governance, the guest concierge, Help me choose, translations, the planner agent; forecasting, fraud and recommendations rules-first.

| Module | Requirements | Screens A / B | Operations A / B | Hours A / B | Sprints | Completion | Lead | Team |
|---|---|---|---|---|---|---|---|---|
| AI & Intelligence | 287 | 20 / 117 | 50 / 91 | 114 / 2,748 | 1-11 | 10 May 2027 | Kalpita Mejari | Kalpita Mejari, Second AI engineer, Pranay Shinde, Sanket Keluskar |

## 7. Team

| Name | Role | Areas | Pace |
|---|---|---|---|
| Hrushikant Patkar | Back end and DevOps | Services, CI, environments, database, observability | 100% |
| Pranay Shinde | Back end | Services | 100% |
| Tanmay Dukhande | Back end | Services | 100% |
| Deep Khanvilkar | Back-end helper | Tasks up to 5 points in others' services, reviewed by the owner; about 55–60% of an owner's load | 100% |
| Chinmay Patkar | Full stack | Guest web, white label, small mobile screens, back-end tasks up to 2 points | 100% |
| Chitrangi Mestry | Front end | Guest app, guest web, white label | 100% |
| Pradnya Yeram | Front end | POS, Kitchen Display, guest app | 100% |
| Pallavi Sawant | Full stack | Venue Management (leads), setup screens | 100% |
| Sanket Keluskar | Full stack | Venue Management, back-end tasks up to 3 points | 100% |
| Surendra | Full stack | Venue Management | about 60% |
| Kalpita Mejari | AI engineer | AI engine (leads) | 100% |
| Second AI engineer | AI engineer | AI engine, from 5 October | 100% |
| New full-stack developer 1 | Full stack | Block B, from 23 November | 100% |
| New full-stack developer 2 | Full stack | Block B, from 23 November | 100% |

Reviews rotate among peers in the same stack. The tester is never the person who built it, and Hrushikant is never a checker.

## 8. AI

- **Every AI function is built inside the six months** (decided 30 September). That covers:
  - gateway and governance;
  - the concierge, Help me choose, translations and the planner agent;
  - forecasting, staffing, suggestions and wait times;
  - anomaly detection, fraud and risk;
  - recommendations, marketing AI and pricing suggestions;
  - the configuration assistant, the analytics assistant and seat-map generation.
- **Day one works with no history.** It uses a venue profile set at onboarding, a starting pattern for the venue type, the UAE calendar and weather, and the venue's own imported history.
- **Stages a venue sees:**
  - **Starting:** day one.
  - **Learning:** about 4 weeks.
  - **Established:** about 3 months.
  - **Learned:** after about a season. A trained model is promoted by an admin when it beats the answer before it.
- **Rules:**
  - Models are per tenant.
  - The model never reads raw data; it gets scrubbed aggregates, or code it writes runs on the data.
  - AI writes only to its own stores.
  - Retention is tenant configuration.
- **People:** Kalpita and the second AI engineer, both from 5 October; no third. Developers build the AI screens and endpoints.
- **What cannot happen by 2 April:** a trained model going live for a venue, because that needs a season of the venue's own data. The code ships, and each venue switches later.

## 9. Overtime to finish by 2 April

| Name | Hours past 2 April | Per week |
|---|---|---|
| Pranay Shinde | 117 | 4.8 |
| Tanmay Dukhande | 100 | 4.1 |
| Deep Khanvilkar | 100 | 4.1 |
| New full-stack developer 2 | 98 | 5.6 |
| Kalpita Mejari | 98 | 4.0 |
| New full-stack developer 1 | 95 | 5.4 |
| Sanket Keluskar | 86 | 3.5 |
| Second AI engineer | 78 | 3.2 |
| Hrushikant Patkar | 77 | 3.1 |
| Pallavi Sawant | 68 | 2.8 |
| Surendra | 63 | 2.6 |
| Chinmay Patkar | 56 | 2.3 |
| Chitrangi Mestry, Pradnya Yeram | 0 | — |
| **Total** | **about 1,036** | |

Chitrangi and Pradnya finish around 24 March. They can absorb web screens after the sprint 1 rebalance.

## 10. Architecture decisions the plan rests on

| Decision | Recommendation | Status |
|---|---|---|
| Deployment shape | One .NET solution of 17 modules, deployed as five units: commerce, access, operations, ticvai-ai, workers (ADR-0055) | Decided 30 Sep |
| Key shape | UUIDv7 ids everywhere; the six busiest tables split by month; venue partitioning deferred, not cancelled (ADR-0056, amends ADR-0044). Checked against the developers' skills matrix: PostgreSQL ratings top out at 3 | Decided 30 Sep |
| Message broker and relay | One relay per region with an inbox per tenant database (ADR-0058). The broker is RabbitMQ or Kafka, behind one kernel interface; the client chooses (ADR-0057). We recommend RabbitMQ; development runs a local RabbitMQ until then | Relay decided 30 Sep; broker: client |
| .NET version | .NET 10 LTS from day one (.NET 8 support ends 10 November) | Decided 30 Sep |
| AI | Baseline first, learns per tenant (ADR-0051); phasing and slip order (ADR-0059); vectors in Qdrant from day one, one collection per tenant with its own collection-scoped token (ADR-0049) | Decided |
| CMS | A flow builder | Agreed |
| E-invoicing | A provider adapter; four questions to the client | Client |
| Availability, biometrics | 99.99% at gate and POS; face templates stay with the vendor | Client |

The decided records are in `docs/adr/`. The drafts still open (availability, replica floors, e-invoicing, encryption, per-tenant limits, the on-sale cache and waiting room, the device register, admission policy, risk ownership) are in `audit/ticvai/steps/SD/adr-drafts/`.

## 11. Release checklist

**Every sprint (Friday of week 3):**
- [ ] Every sprint ticket is Ready for QA, or moved with a reason in the ticket.
- [ ] CI is green: unit, contract and migration tests.
- [ ] Migrations run forward on a copy of staging data, and the rollback script runs back.
- [ ] Half-built work is behind a release flag per tenant.
- [ ] Staging smoke flows pass: buy a ticket, pay, scan, POS sale, kitchen bump.
- [ ] Client demo from staging; accepted and rejected items recorded in OpenProject.
- [ ] Measured pace recorded, and the plan regenerated.

**Block A go-live:**
- [ ] The client has signed off every wireframe batch (3 working days each).
- [ ] Payment sandbox: a sale, a refund and a settlement pass.
- [ ] The POS sells and the scanner admits with the network cut, and both reconcile when it returns.
- [ ] Tax invoice, credit note and VAT fields match the client's answers.
- [ ] Load test at the on-sale burst and at the venue-day mix.
- [ ] Backups restore into a clean environment, and the restore time is written down.
- [ ] Role grants reviewed per module; secrets in the vault; no test credentials in production.
- [ ] Canary tenant first, then the pilot venue; the rollback rehearsed.
- [ ] **Roll back if** payment failures pass 2% of attempts, a POS sale takes over 2 seconds at p95, or a gate admission fails for a reason the ticket does not explain.

**End of six months (2 April):** every module's acceptance is signed, and open defects are triaged into the phase-2 backlog.

## 12. Risks

| Risk | Signal | Action |
|---|---|---|
| Back-end owners overloaded | Block A work past 20 November | Deep's proportional share; new developers on back end from 23 Nov; non-critical platform tasks into B1 |
| Pace below plan | Measured pace on 23 Oct under 9.6 | Regenerate the plan; use the wave-3 deferral list on 18 Dec only if needed |
| Hiring slips | Two developers not confirmed by 23 Oct | The PM chooses scope or date |
| Second AI engineer not in place on 5 Oct | No start date this week | Kalpita starts alone; the baseline layer moves one sprint |
| Client inputs late | Sign-off over 3 days; sandbox; stations and fares; cabanas; photos | Those tickets wait in their own column and do not count against pace |
| Make-or-break answers | E-invoicing, tax fields, consent, biometrics, ID verification | Defaults are built; a different answer is a change request |
| AI estimates rough | The engine is sized from the design | Re-base on 23 Oct; the trained models move first |

## 13. Checkpoints

| Date | Checkpoint |
|---|---|
| Before sprint 1 week 2 | The client's broker choice: RabbitMQ or Kafka |
| 23 Oct | End of sprint 1: measured pace, plan regenerated, hiring confirmed; one web purchase and one offline POS sale end to end |
| 20 Nov | Block A screens built |
| 18 Dec | Deferral decision, only if needed |
| 11 Jan | Block A wired end to end |
| 2 Apr 2027 | End of the six months |

## 14. Design

Claude Design builds **one working file per app** (decided 30 September): the Guest App, POS, Scanner, Staff App, Venue Management, the TICVAI main controller and the Partner Portal. Each app's folder is in `handoff/design-batches/apps/`. Its batches are the order to build the file in, and each batch extends the same file. The CMS flow builder and the two B2B options are drawn first; the option the client picks becomes the start of the Partner Portal's file.

## 15. Before tickets go to OpenProject

- Chinmay's go on `handoff/service-docs/TICVAI_Block_A_Ticket_Review_30_September.xlsx`: 2,717 rewrites, 170 retitles, 1,252 new tickets, 35 leaving the plan.
- ADAM deployed on the box, so the ticket re-audit can run against it.

**Waiting on the B2B option (logged 30 September).** Three partner-portal gaps have no operation, ticket or hours yet: the partner cash drawer (Option A only), sent-ticket history, and an "opened" status on sent tickets. They are listed in `handoff/design-batches/B2B-OPTIONS/ADD-ON-FINALISE.md` (PA-1 to PA-3). When the client picks an option, add them to the contract backlog and the contracts, then re-run the refresh and the plan so their hours land in B2. Claude Design draws them greyed out until then.

## 16. Keeping this plan current

After any change to the package:

```
bash tools/refresh.sh                 # derives, the Block A schedule, all checks
python tools/build-plan-deck.py       # workbook and presentation source
```

Then update the figures in sections 1, 5 and 9 from `handoff/build-plan.json` and `handoff/service-docs/block-a-schedule.json`. The screen engine is Chinmay's own experiment and changes no figure in this plan.
