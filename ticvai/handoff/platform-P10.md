# P10 Partner Web — platform

**Derived.** `python3 tools/derive-platform.py P10`. App `partner-web` · partner · web

| | |
|---|---|
| Screens | 21 |
| Operations | 105 |
| Contracts | 9 |
| Modules | 8 |
| Undrawn | 0 |
| Operations with no screen | 3 |
| Waves | wave2 11 · wave3 10 |

## Gaps

### 3 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| `createPartnerUser` | subscription | POST | Add a user to a partner branch |
| `listPartnerUsers` | subscription | GET | Users beneath a partner, by branch |

### 2 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Access & Account** — waves 2, 3
- **Booking & Quotes** — waves 2, 3

## Modules

| Module | Screens | Waves |
|---|---|---|
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
| `PTR-001` | Partner Login / MFA | Access & Account | 2 | 12 | yes |
| `PTR-002` | Partner Dashboard | Overview | 2 | 16 | yes |
| `PTR-003` | Profile & Company Details | Access & Account | 2 | 4 | yes |
| `PTR-004` | Notifications | Access & Account | 3 | 2 | yes |
| `PTR-005` | Inventory & Allocation View | Inventory & Pricing | 2 | 19 | yes |
| `PTR-006` | Product Catalog (B2B Pricing) | Inventory & Pricing | 2 | 17 | yes |
| `PTR-007` | Availability Search | Inventory & Pricing | 2 | 1 | yes |
| `PTR-008` | Booking Creation | Booking & Quotes | 2 | 14 | yes |
| `PTR-009` | Group / Bulk Booking | Booking & Quotes | 3 | 4 | yes |
| `PTR-010` | Cart & Quote | Booking & Quotes | 3 | 16 | yes |
| `PTR-011` | Quote Management | Booking & Quotes | 3 | 2 | yes |
| `PTR-012` | Checkout / Credit Purchase | Credit & Settlement | 2 | 4 | yes |
| `PTR-013` | Credit Limit & Balance | Credit & Settlement | 2 | 3 | yes |
| `PTR-014` | Settlement & Payment History | Reports & Settlement | 3 | 5 | yes |
| `PTR-015` | Order History | Orders & Fulfilment | 2 | 14 | yes |
| `PTR-016` | Voucher / Ticket Download | Orders & Fulfilment | 2 | 13 | yes |
| `PTR-017` | Commission Statement | Reports & Settlement | 3 | 2 | yes |
| `PTR-018` | Reports & Sales Performance | Reports & Settlement | 3 | 9 | yes |
| `PTR-019` | API Credentials & Integration | Access & Account | 3 | 0 | yes |
| `PTR-020` | Sub-Agent Management | Access & Account | 3 | 3 | yes |
| `PTR-021` | Support & Contact | Support | 3 | 7 | yes |

