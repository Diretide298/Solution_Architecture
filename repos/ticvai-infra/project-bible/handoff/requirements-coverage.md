# Requirements coverage

**3184 functional requirements across 21 domains**, plus **113 on three sheets
that have never been counted** (CF-60).

| Domain | Reqs | Contract | Ops | Status |
|---|---|---|---|---|
| F&B & Guest Management | 411 | `finance`, `marketing-crm` | 88 | Covered |
| Ticketing Sales | 343 | `orders` | 37 | Covered |
| Unified Operations Dashboard | 332 | `reporting` | 23 | Covered |
| Marketing & CRM | 319 | `marketing-crm` | 46 | Covered |
| Ticketing Catalogue | 312 | `catalogue` | 45 | Covered |
| Bundles and Promotions | 229 | `promotions` | 27 | Covered |
| Admission and Access | 201 | `access` | 19 | Covered |
| F&B POS | 151 | `fnb` | 39 | Covered |
| Seat Management & Venue Mapping | 112 | `seating` | 29 | Covered |
| Guest Mobile App & Branding | 107 | `white-label` | 41 | Covered |
| Inventory Management | 98 | `inventory` | 34 | Covered |
| Developer & API Management | 94 | — | — | **Workshop.** No contract |
| Approval Workflows & Governance | 80 | — | — | Cross-cutting. Implemented across contracts, owned by none (CF-59) |
| Retail POS | 78 | `retail` | 26 | Covered |
| Device Management | 60 | — | — | **Workshop.** No contract |
| Subscription & Licensing Management | 59 | `subscription` | 34 | Covered |
| Accreditation & Credential Management | 58 | — | — | **Workshop.** Wave 1 scanner depends on it |
| Maintenance & Safety Management | 50 | `maintenance` | 28 | Covered |
| Employee Mobile App & AI Assistant | 50 | — | — | A surface. Maps to screens; P06 has none written (CF-59) |
| Games & F&B Integration | 25 | `games` | 13 | Covered |
| Digital Asset Management | 15 | `assets` | 10 | Covered |
| **Total** | **3184** | | **618** | **89% covered** |

## The 342 without a contract

| | Reqs | Why |
|---|---|---|
| Developer & API Management | 94 | Workshop |
| Device Management | 60 | Workshop |
| Accreditation & Credential Management | 58 | Workshop. **Wave 1 scanner depends on it** |
| Approval Workflows & Governance | 80 | Cross-cutting, owned by nothing |
| Employee Mobile App & AI Assistant | 50 | A surface, not a module |

**Only 212 are workshop-blocked**, not the ~276 CF-21 originally claimed. That figure counted
a Rentals domain that does not exist — rentals and lockers are 30 requirements scattered
across seven domains, mostly `catalogue` Resource Management (1.2.8–1.2.23), which is
contracted.

The other 130 are traceability gaps rather than capability gaps. Approval workflows are
implemented in four places — refund approval, shift variance, release promotion, manual
discount — and no module claims them. That is defensible, and it still means 80 requirements
cannot be shown as covered.

## The sheets nobody counted

| Sheet | Requirements | State |
|---|---|---|
| Training, Knowledge Transfer & | 40 | Delivery scope. Training for admin, super user, operations, finance |
| Disaster Recovery & BCP | 62 | **Nothing designed.** Backup schedules, RPO and RTO are architectural |
| Compliance & Security | 11 | PCI-DSS, privacy, secrets management, enterprise controls |
| **Total** | **113** | |

Every figure quoted since 30 July — 3,184 across 21 domains — is the Functionality sheet
alone. **DR & BCP at 62 requirements is the one that matters**: recovery objectives shape the
database topology, and none of it has been designed.

## Integrations

**19 software, 16 hardware.** Previously counted as "roughly 35" and never itemised against
contracts. Software includes UAE Pass, DET, DCT, WhatsApp, SMS, email, Stripe, SSO and Azure
AD — several of which have no contract operation behind them.

