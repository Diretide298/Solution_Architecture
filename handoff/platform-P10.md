# P10 Partner Web — platform

**Derived.** `python3 tools/derive-platform.py P10`. App `partner-web` · partner · web

| | |
|---|---|
| Screens | 21 |
| Operations | 105 |
| Contracts | 9 |
| Modules | 10 |
| Undrawn | 0 |
| Operations with no screen | 0 |
| Waves | wave2 11 · wave3 10 |

## Gaps

### 1 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **identity** — waves 2, 3

## Modules

| Module | Screens | Waves |
|---|---|---|
| orders | 7 | 2 |
| identity | 3 | 2, 3 |
| marketing-crm | 2 | 3 |
| catalogue | 2 | 2 |
| subscription | 2 | 3 |
| seating | 1 | 3 |
| promotions | 1 | 3 |
| finance | 1 | 3 |
| reporting | 1 | 3 |
| TODO | 1 | 3 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `PTR-001` | Partner Login / MFA | identity | 2 | 12 | yes |
| `PTR-002` | Partner Dashboard | orders | 2 | 16 | yes |
| `PTR-003` | Profile & Company Details | identity | 2 | 4 | yes |
| `PTR-004` | Notifications | marketing-crm | 3 | 2 | yes |
| `PTR-005` | Inventory & Allocation View | orders | 2 | 19 | yes |
| `PTR-006` | Product Catalog (B2B Pricing) | catalogue | 2 | 17 | yes |
| `PTR-007` | Availability Search | catalogue | 2 | 1 | yes |
| `PTR-008` | Booking Creation | orders | 2 | 14 | yes |
| `PTR-009` | Group / Bulk Booking | seating | 3 | 4 | yes |
| `PTR-010` | Cart & Quote | promotions | 3 | 16 | yes |
| `PTR-011` | Quote Management | subscription | 3 | 2 | yes |
| `PTR-012` | Checkout / Credit Purchase | orders | 2 | 4 | yes |
| `PTR-013` | Credit Limit & Balance | orders | 2 | 3 | yes |
| `PTR-014` | Settlement & Payment History | finance | 3 | 5 | yes |
| `PTR-015` | Order History | orders | 2 | 14 | yes |
| `PTR-016` | Voucher / Ticket Download | orders | 2 | 13 | yes |
| `PTR-017` | Commission Statement | subscription | 3 | 2 | yes |
| `PTR-018` | Reports & Sales Performance | reporting | 3 | 9 | yes |
| `PTR-019` | API Credentials & Integration | TODO | 3 | 0 | yes |
| `PTR-020` | Sub-Agent Management | identity | 3 | 3 | yes |
| `PTR-021` | Support & Contact | marketing-crm | 3 | 7 | yes |

