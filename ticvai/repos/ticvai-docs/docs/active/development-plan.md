# TICVAI development plan

> **Purpose:** the complete plan for building TICVAI: what is built, in what order, by whom, by when, and at what cost in hours
> **Owner:** Chinmay Parab
> **Status:** Current, 30 September 2026. Supersedes the timeline in `six-month-plan-29-september.md`, whose decisions 1–13 still stand.
> **Sources:** numbers from `tools/build-plan-deck.py` (workbook `handoff/TICVAI - Build Plan.xlsx`), the Block A schedule from `tools/derive-block-a-schedule.py`, and the task sheet `handoff/service-docs/tasks.csv`. Deck: https://claude.ai/artifact/NzvBoTU53zNbwCouMgz4ch

## 1. Summary

- **When:** Monday 5 October 2026 to Friday 2 April 2027, in nine sprints of three weeks (the last is two).
- **What:** seven apps, 31 modules in 7 packages, 2,660 operations, 2,445 screens. 3,153 of the client's 3,165 in-scope requirements are specified.
- **Effort:** about **13,559 hours** (16,238 points at 0.835 hours a point).
- **Team:** 14 people. Chinmay Parab leads and is not counted in capacity.
- **Finish:** 26 April 2027 at normal hours. **Finishing on 2 April needs about 1,270 overtime hours**, 2.2 to 5.2 hours a week per person.
- **One build order, start to end** (30 September): 0 plumbing; 1 foundation (Tenancy, Identity, Platform control, White Label); 2 commerce (Catalogue, Order, Ledger, Access, Wallet); 3 operations (Venue Ops, F&B, Inventory, Retail); 4 engagement (Marketing, AI); 5 reporting.
- **The back end is still the constraint in Block A,** but a shorter one. Screens are built by 20 November (Chinmay Patkar's last guest screens by 25 November). Block A work ends between 10 November and 25 December, depending on the person; the back end lands between 8 and 25 December, and every screen is wired end to end by 25 December (section 5).
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
| **Block A tail** | to 25 Dec 2026 | Back-end work that does not fit 35 days, and wiring the screens to it (section 5) |
| **B1** | 23 Nov 2026 – 1 Jan 2027 | Scanner; Staff App waves 1–2; Kiosk; remaining CMS steps; Venue Management waves 1–2 and the first wave-3 modules; TICVAI console waves 1–2; Sign-up; the AI action pipeline, forecasting and fraud baselines |
| **B2** | 4 Jan – 12 Feb 2027 | Partner portal; Support; Accreditation; Developer Portal; Staff App wave 3; Venue Management wave 3; recommendations and the configuration assistant |
| **B3** | 15 Feb – 2 Apr 2027 | The rest of Venue Management and the console, including the AI console; Analytics and the analytics assistant; hardening |

Holidays counted: 1–3 December (Commemoration and National Day), 1 January, and Eid al-Fitr around 9–11 March (to be confirmed).

### 3.1 Sprints

| Sprint | Dates | Block | Capacity (h) | Planned (h) |
|---|---|---|---|---|
| 1 | 5 Oct 2026 – 23 Oct 2026 | A | 1,392 | 1,281 |
| 2 | 26 Oct 2026 – 13 Nov 2026 | A | 1,392 | 1,346 |
| 3 | 16 Nov 2026 – 4 Dec 2026 | A ends 20 Nov, B1 starts | 1,226 | 935 |
| 4 | 7 Dec 2026 – 25 Dec 2026 | B | 1,632 | 1,548 |
| 5 | 28 Dec 2026 – 15 Jan 2027 | B | 1,523 | 1,523 |
| 6 | 18 Jan 2027 – 5 Feb 2027 | B | 1,632 | 1,632 |
| 7 | 8 Feb 2027 – 26 Feb 2027 | B | 1,632 | 1,632 |
| 8 | 1 Mar 2027 – 19 Mar 2027 | B | 1,306 | 1,306 |
| 9 | 22 Mar 2027 – 2 Apr 2027 | B | 1,088 | 1,088 |

Holidays counted: 1 Dec 2026 Commemoration Day; 2 Dec 2026 National Day; 3 Dec 2026 National Day; 1 Jan 2027 New Year; 9 Mar 2027 Eid al-Fitr; 10 Mar 2027 Eid al-Fitr; 11 Mar 2027 Eid al-Fitr. Eid dates are to be confirmed.

### The build order: phases, end to end

One order from 5 October to the end: plumbing, then the foundation everything reads, the sale path, the per-module operations, engagement, and reporting last. Block A takes it from the tickets (each ticket's phase), B1 to B3 from each module's phase. A screen is built against the mock server and connected as its services land.

**Back end**

| Phase | Starts | Ends | Hours (A / B) | Main modules | People |
|---|---|---|---|---|---|
| 0 Plumbing | 5 Oct 2026 | 15 Dec 2026 | 306 / 0 | Foundation & Setup, Identity, Roles & Security, Tenancy, Venues & Devices, Transport, Reporting & Analytics | Hrushikant Patkar, Tanmay Dukhande, Pranay Shinde, Pradnya Yeram |
| 1 Foundation | 8 Oct 2026 | 5 Mar 2027 | 273 / 684 | Subscription & Licensing, Identity, Roles & Security, White Label & CMS, Approval Workflows, Platform Operations | Deep Khanvilkar, Tanmay Dukhande, Sanket Keluskar, Hrushikant Patkar |
| 2 Commerce | 14 Oct 2026 | 26 Mar 2027 | 510 / 1,652 | Admission & Access Control, Ticketing Catalogue & Products, Orders & Reservations, Pricing, Promotions & Bundles, Finance, Ledger & Tax | Pranay Shinde, Tanmay Dukhande, Hrushikant Patkar, Deep Khanvilkar |
| 3 Operations | 13 Oct 2026 | 6 Apr 2027 | 415 / 750 | Food & Beverage, Foundation & Setup, Inventory & Procurement, Resources & Capacity, Accreditation | Hrushikant Patkar, Deep Khanvilkar, Pranay Shinde, Tanmay Dukhande |
| 4 Engagement | 5 Oct 2026 | 26 Apr 2027 | 177 / 2,881 | AI & Intelligence, Marketing & CRM, Foundation & Setup | Kalpita Mejari, Second AI engineer, Pranay Shinde, Tanmay Dukhande |
| 5 Reporting | 29 Oct 2026 | 23 Apr 2027 | 34 / 58 | Reporting & Analytics, Foundation & Setup | Deep Khanvilkar, Hrushikant Patkar, Chinmay Patkar, Sanket Keluskar |

**Front end**

| Phase | Starts | Ends | Hours (A / B) | Main modules | People |
|---|---|---|---|---|---|
| 0 Plumbing | 6 Oct 2026 | 6 Oct 2026 | 2 / 0 | White Label & CMS | Chitrangi Mestry |
| 1 Foundation | 5 Oct 2026 | 1 Mar 2027 | 158 / 883 | Subscription & Licensing, Approval Workflows, Identity, Roles & Security, White Label & CMS, Tenancy, Venues & Devices | Chitrangi Mestry, Pallavi Sawant, Pradnya Yeram, New full-stack developer 1 |
| 2 Commerce | 6 Oct 2026 | 8 Mar 2027 | 491 / 1,951 | Ticketing Catalogue & Products, Orders & Reservations, Admission & Access Control, Pricing, Promotions & Bundles, Wallet & Cashless | Pradnya Yeram, Chitrangi Mestry, Pallavi Sawant, Chinmay Patkar |
| 3 Operations | 9 Oct 2026 | 6 Apr 2027 | 315 / 1,012 | Rentals, Food & Beverage, Games & Rides, Accreditation, Resources & Capacity | Chitrangi Mestry, Pradnya Yeram, Pallavi Sawant, Chinmay Patkar |
| 4 Engagement | 13 Oct 2026 | 20 Apr 2027 | 141 / 630 | Marketing & CRM, AI & Intelligence, Foundation & Setup, White Label & CMS, Orders & Reservations | Chinmay Patkar, Pradnya Yeram, Sanket Keluskar, Pallavi Sawant |
| 5 Reporting | 15 Oct 2026 | 20 Apr 2027 | 33 / 191 | Reporting & Analytics, Foundation & Setup | New full-stack developer 1, Chitrangi Mestry, New full-stack developer 2, Pallavi Sawant |

**Links.** Every service waits for the platform kernel, every write for idempotency, every event for the outbox, and every report for the data it reports on. These platform waits are **soft**: Pranay and Tanmay publish the interfaces in week 1 (ITenantContext, the current user, the idempotency filter, the outbox writer), so a service starts against them from day 3 and only finishes after the kernel; reports build on seeded data. Setup, migrations and the AI engine's setup stay hard waits. **A person who is waiting takes their next ready ticket**, as ADAM's board now shows, so a ticket blocked on somebody else no longer leaves its owner idle.

The rules behind the order, and how new tickets join the ones in OpenProject: `handoff/service-docs/TICKET-STRUCTURE.md`. Every link, service by service and module by module: `handoff/service-docs/TICKET-LINKS.md`.

## 4. How the plan is measured

- **Points** come from each screen's specification (operations, components, states, navigation, offline: 1 to 8 points), plus about 2.3 points per back-end operation.
- **Pace** is Block A's plan of record: 3,018 points in 35 days for nine developers. That is 9.6 points per developer per day, so one point is about 0.84 hours. The measured pace replaces it on 23 October and the plan is regenerated.
- **Hours** are points times 0.835. AI engine work (models, pipelines, the learning layer) is sized in engineer-weeks by the AI review and converted at the same rate.
- **Names:** Block A comes from the task sheet. Block B is placed by a scheduler that follows skill and experience. **Loads are uneven on purpose.**
- A re-plan is a rerun of the generators, not a re-estimate.

## 5. Block A in detail

**870 tasks, 3,431 points, 697 operations.** The schedule is derived from the task sheet (`tools/derive-block-a-schedule.py`): build order by phase, dependencies and each person's pace. Front-end tasks may start before their back end, because screens build against the generated API client and the mock server. They finish only when the back end they wire to has landed. Back-end tasks wait softly on the platform kernel, idempotency and the outbox: they start from day 3 against the interfaces published in week 1 and finish after the kernel. A report task starts against seeded data and finishes after the services it reads. Whenever a person's next ticket is blocked, the scheduler gives them the next one that is ready.

| Who | Block A points | Screens built | Work ends |
|---|---|---|---|
| Pradnya Yeram (POS, KDS, guest app) | 244 | 10 Nov | 10 Nov; wired by 9 Dec |
| Chitrangi Mestry (guest app, web, white label) | 280 | 16 Nov | 16 Nov; wired by 14 Dec |
| Pallavi Sawant (Venue Management) | 290 | 16 Nov | 16 Nov; wired by 25 Dec, with the Venue Management back end |
| Surendra (Venue Management) | 173 | 17 Nov | 17 Nov; wired by 25 Dec |
| Deep Khanvilkar (back-end helper, tasks up to 5 points) | 287 | — | 8 Dec |
| Kalpita Mejari, second AI engineer (AI engine) | 33 engineer-days each | — | 8 Dec |
| Sanket Keluskar (Venue Management, back-end tasks up to 3 points) | 290 | 12 Nov | 15 Dec; his screens wired by 25 Dec |
| Chinmay Patkar (guest web, white label, back-end helper) | 405 | 25 Nov | 15 Dec |
| Tanmay Dukhande (back end) | 453 | — | 16 Dec |
| Pranay Shinde (back end) | 457 | — | 18 Dec |
| Hrushikant Patkar (back end, DevOps) | 540 | — | 25 Dec |

**Why the tail.** One developer covers about 335 points in 35 days. The back-end owners carry 450–540, including the platform kernel the system-design review added: tenant routing, idempotency, outbox and relay, the payment adapter, audit and observability. The tail is shorter than in the plan of the morning of 30 September (which ran to 11 January) for three reasons: the work now follows the phases, so foundation and commerce come first; the platform waits are soft, so services no longer queue behind the whole kernel; and nobody sits idle while waiting, because they take their next ready ticket. Chinmay Patkar's last guest screens (engagement phase) run to 25 November.

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
| **Platform Foundation** | 8 | 563 | 425 | 453 | 2,613 | 5 Mar 2027 | Pallavi Sawant |
| **Ticketing & Guest Commerce** | 8 | 866 | 867 | 908 | 3,641 | 16 Mar 2027 | Tanmay Dukhande |
| **Food, Beverage & Retail** | 4 | 224 | 216 | 267 | 1,034 | 29 Mar 2027 | Chitrangi Mestry |
| **Venue Operations** | 7 | 411 | 464 | 507 | 1,967 | 6 Apr 2027 | Hrushikant Patkar |
| **Finance & Insights** | 2 | 393 | 117 | 120 | 498 | 23 Apr 2027 | New full-stack developer 1 |
| **Customer & Marketing** | 1 | 421 | 219 | 264 | 940 | 15 Apr 2027 | Tanmay Dukhande |
| **AI & Intelligence** | 1 | 287 | 137 | 141 | 2,863 | 26 Apr 2027 | Kalpita Mejari |

"Completion" is at normal hours. Dates after 2 April are brought in with overtime. In the module tables, A is Block A and B is Block B.

### 6.1 Platform Foundation

Everything the apps stand on: sign-in, tenants and venues, devices, licensing, approvals, the public API.

| Module | Requirements | Screens A / B | Operations A / B | Hours A / B | Sprints | Completion | Lead | Team |
|---|---|---|---|---|---|---|---|---|
| Foundation & Setup | 0 | 0 / 0 | 0 / 0 | 840 / 0 | 1-4 | 25 Dec 2026 | Pallavi Sawant | Pallavi Sawant, Hrushikant Patkar, Sanket Keluskar, Tanmay Dukhande |
| Identity, Roles & Security | 144 | 9 / 22 | 37 / 52 | 83 / 162 | 1-8 | 5 Mar 2027 | Hrushikant Patkar | Hrushikant Patkar, Surendra, Pallavi Sawant, Tanmay Dukhande |
| Tenancy, Venues & Devices | 126 | 5 / 30 | 18 / 37 | 46 / 137 | 1-8 | 3 Mar 2027 | New full-stack developer 2 | New full-stack developer 2, New full-stack developer 1, Deep Khanvilkar, Tanmay Dukhande |
| Platform Operations | 4 | 0 / 12 | 0 / 51 | 7 / 126 | 1-8 | 5 Mar 2027 | Pallavi Sawant | Pallavi Sawant, Pradnya Yeram, Pranay Shinde, New full-stack developer 1 |
| Subscription & Licensing | 105 | 2 / 174 | 10 / 138 | 23 / 650 | 1-8 | 5 Mar 2027 | Surendra | Surendra, Deep Khanvilkar, Chitrangi Mestry, Hrushikant Patkar |
| Approval Workflows | 90 | 2 / 106 | 8 / 45 | 23 / 280 | 1-8 | 2 Mar 2027 | New full-stack developer 2 | New full-stack developer 2, Pradnya Yeram, Chitrangi Mestry, Sanket Keluskar |
| Developer Portal & Public API | 80 | 3 / 21 | 8 / 23 | 14 / 93 | 1-8 | 3 Mar 2027 | New full-stack developer 1 | New full-stack developer 1, Pallavi Sawant, Hrushikant Patkar, Deep Khanvilkar |
| Digital Asset Management | 14 | 1 / 38 | 10 / 16 | 26 / 104 | 1-5 | 30 Dec 2026 | Pallavi Sawant | Pallavi Sawant, Deep Khanvilkar, Pradnya Yeram, Hrushikant Patkar |

### 6.2 Ticketing & Guest Commerce

What a guest buys and how: catalogue, pricing, seats and maps, orders, payments, wallet, the branded storefront and app.

| Module | Requirements | Screens A / B | Operations A / B | Hours A / B | Sprints | Completion | Lead | Team |
|---|---|---|---|---|---|---|---|---|
| Ticketing Catalogue & Products | 266 | 40 / 170 | 55 / 182 | 175 / 719 | 1-8 | 4 Mar 2027 | Tanmay Dukhande | Tanmay Dukhande, Pranay Shinde, Chitrangi Mestry, Chinmay Patkar |
| Pricing, Promotions & Bundles | 105 | 15 / 150 | 29 / 124 | 78 / 533 | 1-8 | 12 Mar 2027 | Tanmay Dukhande | Tanmay Dukhande, Deep Khanvilkar, Chinmay Patkar, Pallavi Sawant |
| Seat Management & Venue Maps | 100 | 12 / 93 | 20 / 55 | 73 / 272 | 1-8 | 3 Mar 2027 | Hrushikant Patkar | Hrushikant Patkar, Pradnya Yeram, Pallavi Sawant, Sanket Keluskar |
| Orders & Reservations | 269 | 30 / 140 | 57 / 162 | 211 / 662 | 1-8 | 12 Mar 2027 | Pranay Shinde | Pranay Shinde, Chitrangi Mestry, New full-stack developer 1, New full-stack developer 2 |
| Payments | 9 | 4 / 51 | 6 / 42 | 26 / 187 | 1-8 | 5 Mar 2027 | Pranay Shinde | Pranay Shinde, Sanket Keluskar, Pradnya Yeram, Chinmay Patkar |
| Wallet & Cashless | 52 | 5 / 105 | 17 / 49 | 44 / 353 | 1-8 | 12 Mar 2027 | Chinmay Patkar | Chinmay Patkar, Pallavi Sawant, Chitrangi Mestry, New full-stack developer 1 |
| White Label & CMS | 65 | 32 / 8 | 78 / 1 | 210 / 16 | 1-4 | 23 Dec 2026 | Chitrangi Mestry | Chitrangi Mestry, Tanmay Dukhande, Deep Khanvilkar, Chinmay Patkar |
| Transport | 0 | 11 / 1 | 21 / 10 | 63 / 21 | 1-8 | 16 Mar 2027 | Hrushikant Patkar | Hrushikant Patkar, New full-stack developer 1, Sanket Keluskar, Chinmay Patkar |

### 6.3 Food, Beverage & Retail

Selling at the venue: F&B with the kitchen display, retail, rentals, stock and purchasing.

| Module | Requirements | Screens A / B | Operations A / B | Hours A / B | Sprints | Completion | Lead | Team |
|---|---|---|---|---|---|---|---|---|
| Food & Beverage | 95 | 37 / 37 | 87 / 54 | 276 / 212 | 1-9 | 24 Mar 2027 | Deep Khanvilkar | Deep Khanvilkar, Pradnya Yeram, Hrushikant Patkar, Chitrangi Mestry |
| Retail | 14 | 5 / 4 | 14 / 11 | 43 / 30 | 1-8 | 18 Mar 2027 | New full-stack developer 1 | New full-stack developer 1, Pranay Shinde, Pradnya Yeram, Chinmay Patkar |
| Rentals | 0 | 0 / 106 | 0 / 43 | 0 / 288 | 7-9 | 29 Mar 2027 | Chitrangi Mestry | Chitrangi Mestry, Tanmay Dukhande, Pradnya Yeram, New full-stack developer 2 |
| Inventory & Procurement | 115 | 2 / 25 | 7 / 51 | 21 / 165 | 1-9 | 22 Mar 2027 | Pallavi Sawant | Pallavi Sawant, Hrushikant Patkar, New full-stack developer 1, Chinmay Patkar |

### 6.4 Venue Operations

Running the venue day to day: gates and access, accreditation, capacity, staff, maintenance, rides, queues.

| Module | Requirements | Screens A / B | Operations A / B | Hours A / B | Sprints | Completion | Lead | Team |
|---|---|---|---|---|---|---|---|---|
| Admission & Access Control | 108 | 23 / 149 | 38 / 208 | 101 / 730 | 1-9 | 22 Mar 2027 | Hrushikant Patkar | Hrushikant Patkar, Sanket Keluskar, Pradnya Yeram, New full-stack developer 2 |
| Accreditation | 58 | 0 / 72 | 0 / 47 | 0 / 224 | 5-9 | 30 Mar 2027 | Pranay Shinde | Pranay Shinde, New full-stack developer 1, Chinmay Patkar, Pallavi Sawant |
| Resources & Capacity | 92 | 7 / 55 | 15 / 46 | 38 / 208 | 1-9 | 31 Mar 2027 | Hrushikant Patkar | Hrushikant Patkar, Pradnya Yeram, Pallavi Sawant, Deep Khanvilkar |
| Workforce & Staff | 27 | 0 / 34 | 2 / 47 | 5 / 173 | 1-9 | 1 Apr 2027 | New full-stack developer 2 | New full-stack developer 2, Chitrangi Mestry, Pradnya Yeram, Tanmay Dukhande |
| Maintenance & Safety | 75 | 1 / 28 | 1 / 41 | 7 / 170 | 1-10 | 5 Apr 2027 | Surendra | Surendra, Pranay Shinde, Chinmay Patkar, Tanmay Dukhande |
| Games & Rides | 14 | 0 / 81 | 3 / 37 | 6 / 225 | 1-10 | 6 Apr 2027 | Deep Khanvilkar | Deep Khanvilkar, Sanket Keluskar, New full-stack developer 1, Chinmay Patkar |
| Virtual Queue | 37 | 8 / 6 | 11 / 11 | 34 / 47 | 1-9 | 1 Apr 2027 | Pallavi Sawant | Pallavi Sawant, Chinmay Patkar, Tanmay Dukhande, Chitrangi Mestry |

### 6.5 Finance & Insights

The money and the numbers: ledger, VAT and e-invoicing, reports and analytics.

| Module | Requirements | Screens A / B | Operations A / B | Hours A / B | Sprints | Completion | Lead | Team |
|---|---|---|---|---|---|---|---|---|
| Finance, Ledger & Tax | 204 | 9 / 18 | 18 / 54 | 49 / 148 | 1-9 | 26 Mar 2027 | Surendra | Surendra, Chinmay Patkar, Pradnya Yeram, Pallavi Sawant |
| Reporting & Analytics | 189 | 9 / 81 | 17 / 31 | 52 / 250 | 1-11 | 23 Apr 2027 | New full-stack developer 1 | New full-stack developer 1, Chitrangi Mestry, Deep Khanvilkar, New full-stack developer 2 |

### 6.6 Customer & Marketing

Knowing and reaching the guest: CRM, segments, campaigns, loyalty, support.

| Module | Requirements | Screens A / B | Operations A / B | Hours A / B | Sprints | Completion | Lead | Team |
|---|---|---|---|---|---|---|---|---|
| Marketing & CRM | 421 | 33 / 186 | 60 / 204 | 177 / 763 | 1-10 | 15 Apr 2027 | Tanmay Dukhande | Tanmay Dukhande, Pranay Shinde, Deep Khanvilkar, New full-stack developer 2 |

### 6.7 AI & Intelligence

The AI gateway and governance, the guest concierge, Help me choose, translations, the planner agent; forecasting, fraud and recommendations rules-first.

| Module | Requirements | Screens A / B | Operations A / B | Hours A / B | Sprints | Completion | Lead | Team |
|---|---|---|---|---|---|---|---|---|
| AI & Intelligence | 287 | 20 / 117 | 50 / 91 | 114 / 2,748 | 1-11 | 26 Apr 2027 | Kalpita Mejari | Kalpita Mejari, Second AI engineer, Pranay Shinde, Sanket Keluskar |

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
| Pranay Shinde | 126 | 5.1 |
| Deep Khanvilkar | 115 | 4.7 |
| Hrushikant Patkar | 113 | 4.6 |
| Sanket Keluskar | 113 | 4.6 |
| Pallavi Sawant | 106 | 4.3 |
| Kalpita Mejari | 98 | 4.0 |
| New full-stack developer 1 | 91 | 5.2 |
| New full-stack developer 2 | 91 | 5.2 |
| Tanmay Dukhande | 90 | 3.6 |
| Second AI engineer | 78 | 3.2 |
| Chinmay Patkar | 71 | 2.9 |
| Chitrangi Mestry | 63 | 2.5 |
| Pradnya Yeram | 58 | 2.3 |
| Surendra | 55 | 2.2 |
| **Total** | **about 1,268** | |

Everyone now has some work past 2 April, from Surendra's 55 hours to Pranay's 126: the scheduler fills each person's waiting time with their next ready ticket, so the load is shared rather than parked. The new developers' figure is higher per week because they join on 23 November. Rerun on 23 October with the measured pace.

## 10. Architecture decisions the plan rests on

| Decision | Recommendation | Status |
|---|---|---|
| Deployment shape | One .NET solution of 17 modules, deployed as five units: commerce, access, operations, ticvai-ai, workers (ADR-0055) | Decided 30 Sep |
| Key shape | UUIDv7 ids everywhere; the six busiest tables split by month; venue partitioning deferred, not cancelled (ADR-0056, amends ADR-0044). Checked against the developers' skills matrix: PostgreSQL ratings top out at 3 | Decided 30 Sep |
| Message broker and relay | One relay per region with an inbox per tenant database (ADR-0058). The broker is RabbitMQ or Kafka, behind one kernel interface; the client chooses (ADR-0057). We recommend RabbitMQ; development runs a local RabbitMQ until then | Relay decided 30 Sep; broker: client |
| .NET version | .NET 10 LTS from day one (.NET 8 support ends 10 November) | Decided 30 Sep |
| AI | Baseline first, learns per tenant (ADR-0051); phasing and slip order (ADR-0059); vectors in Qdrant from day one, hosted only in the UAE, one collection per tenant with its own collection-scoped token (ADR-0049) | Decided |
| CMS | A flow builder | Agreed |
| E-invoicing | A provider adapter; four questions to the client | Client |
| Availability, biometrics | 99.99% at gate and POS; face templates stay with the vendor | Client |

The client's open questions (30, with hardware and suppliers added on 30 September) are in `handoff/TICVAI - Decisions Register.xlsx`. The architecture decisions are in `docs/adr/` (index: `docs/adr/README.md`). On 1 October ADR-0052, 0053, 0054, 0061 (replica floors), 0064 (per-tenant limits), 0066 (the on-sale waiting room), 0067 (one device register) and 0068 (admission policy in Access) were accepted there; four are still **Proposed** in the same folder and wait on a decision: ADR-0060 (availability and HA), ADR-0062 (e-invoicing), ADR-0063 (encryption and biometric templates) and ADR-0065 (the on-sale availability cache).

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
| Back-end owners overloaded | Block A back end not in by 25 December | Soft platform waits and gap filling are already in the plan; Deep's proportional share; new developers on back end from 23 Nov; non-critical platform tasks into B1 |
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
| 25 Dec | Block A back end in; every Block A screen wired end to end |
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
