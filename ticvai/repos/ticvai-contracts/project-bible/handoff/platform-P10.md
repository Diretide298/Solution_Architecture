# P10 Partner Web — platform

**Derived.** `python3 tools/derive-platform.py P10`. App `partner-web` · partner · web

| | |
|---|---|
| Screens | 51 |
| Operations | 134 |
| Contracts | 10 |
| Modules | 9 |
| Undrawn | 0 |
| Operations with no screen | 3 |
| Waves | wave2 11 · wave3 40 |

## Gaps

### 3 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `issueApiToken` | public-api | POST | Exchange a credential for an access token |
| `createPartnerUser` | subscription | POST | Add a user to a partner branch |
| `listPartnerUsers` | subscription | GET | Users beneath a partner, by branch |

### 2 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Access & Account** — waves 2, 3
- **Booking & Quotes** — waves 2, 3

## Modules

| Module | Screens | Waves |
|---|---|---|
| Partners | 30 | 3 |
| Access & Account | 5 | 2, 3 |
| Booking & Quotes | 4 | 2, 3 |
| Inventory & Pricing | 3 | 2 |
| Reports & Settlement | 3 | 3 |
| Credit & Settlement | 2 | 2 |
| Orders & Fulfilment | 2 | 2 |
| Overview | 1 | 2 |
| Support | 1 | 3 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `PTR-001` | Partner Login / MFA | Access & Account | 2 | 11 | yes |
| `PTR-002` | Partner Dashboard | Overview | 2 | 16 | yes |
| `PTR-003` | Profile & Company Details | Access & Account | 2 | 4 | yes |
| `PTR-004` | Notifications | Access & Account | 3 | 2 | yes |
| `PTR-005` | Inventory & Allocation View | Inventory & Pricing | 2 | 19 | yes |
| `PTR-006` | Product Catalog (B2B Pricing) | Inventory & Pricing | 2 | 17 | yes |
| `PTR-007` | Availability Search | Inventory & Pricing | 2 | 1 | yes |
| `PTR-008` | Booking Creation | Booking & Quotes | 2 | 14 | yes |
| `PTR-009` | Group / Bulk Booking | Booking & Quotes | 3 | 4 | yes |
| `PTR-010` | Cart & Quote | Booking & Quotes | 3 | 10 | yes |
| `PTR-011` | Quote Management | Booking & Quotes | 3 | 4 | yes |
| `PTR-012` | Checkout / Credit Purchase | Credit & Settlement | 2 | 4 | yes |
| `PTR-013` | Credit Limit & Balance | Credit & Settlement | 2 | 3 | yes |
| `PTR-014` | Settlement & Payment History | Reports & Settlement | 3 | 5 | yes |
| `PTR-015` | Order History | Orders & Fulfilment | 2 | 14 | yes |
| `PTR-016` | Voucher / Ticket Download | Orders & Fulfilment | 2 | 13 | yes |
| `PTR-017` | Commission Statement | Reports & Settlement | 3 | 2 | yes |
| `PTR-018` | Reports & Sales Performance | Reports & Settlement | 3 | 9 | yes |
| `PTR-019` | API Credentials & Integration | Access & Account | 3 | 4 | yes |
| `PTR-020` | Sub-Agent Management | Access & Account | 3 | 3 | yes |
| `PTR-021` | Support & Contact | Support | 3 | 7 | yes |
| `PTR-022` | Partner Management Command Center | Partners | 3 | 2 | yes |
| `PTR-023` | Partner Profile & Organization Setup | Partners | 3 | 1 | yes |
| `PTR-024` | Partner Onboarding & Application Workflow | Partners | 3 | 1 | yes |
| `PTR-025` | Partner Contacts & User Administration | Partners | 3 | 1 | yes |
| `PTR-026` | Territory, Market & Distribution Rights | Partners | 3 | 1 | yes |
| `PTR-027` | Partner Brand, Venue & Business Scope Assignment | Partners | 3 | 1 | yes |
| `PTR-028` | Partner Documentation & Compliance Repository | Partners | 3 | 1 | yes |
| `PTR-029` | Partner Access, Roles & Permission Profile | Partners | 3 | 1 | yes |
| `PTR-030` | Partner Approval, Status & Lifecycle Management | Partners | 3 | 1 | yes |
| `PTR-031` | Partner 360° Profile, Readiness & AI Review | Partners | 3 | 1 | yes |
| `PTR-032` | Commercial Agreement Command Center | Partners | 3 | 2 | yes |
| `PTR-033` | Agreement & Contract Terms Builder | Partners | 3 | 1 | yes |
| `PTR-034` | Partner Rate & Net Pricing Configuration | Partners | 3 | 1 | yes |
| `PTR-035` | Commission, Margin & Incentive Management | Partners | 3 | 1 | yes |
| `PTR-036` | Credit Limit & Exposure Management | Partners | 3 | 1 | yes |
| `PTR-037` | Deposit, Guarantee & Financial Security Management | Partners | 3 | 1 | yes |
| `PTR-038` | Payment Terms, Billing & Account Configuration | Partners | 3 | 1 | yes |
| `PTR-039` | Commercial Allocation, Quota & Commitment Management | Partners | 3 | 1 | yes |
| `PTR-040` | Booking Limits, Commercial Exceptions & Approval | Partners | 3 | 1 | yes |
| `PTR-041` | Commercial Agreement 360°, Health & AI Review | Partners | 3 | 1 | yes |
| `PTR-042` | Partner Operations Command Center | Partners | 3 | 2 | yes |
| `PTR-043` | Partner Orders & Booking Management | Partners | 3 | 1 | yes |
| `PTR-044` | Reservations, Holds & Release Management | Partners | 3 | 1 | yes |
| `PTR-045` | Partner Cancellations, Refunds & Amendments | Partners | 3 | 1 | yes |
| `PTR-046` | Partner Statement & Account Activity | Partners | 3 | 1 | yes |
| `PTR-047` | Partner Reconciliation & Exception Management | Partners | 3 | 1 | yes |
| `PTR-048` | Commission Calculation & Settlement Management | Partners | 3 | 1 | yes |
| `PTR-049` | Partner Disputes, Cases & Service Management | Partners | 3 | 1 | yes |
| `PTR-050` | Partner Performance Scorecard & Risk Monitoring | Partners | 3 | 1 | yes |
| `PTR-051` | Partner AI Intelligence & Relationship Optimization | Partners | 3 | 1 | yes |

