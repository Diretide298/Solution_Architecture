# P10 Partner Web — platform

**Derived.** `python3 tools/derive-platform.py P10`. App `partner-web` · partner · web

| | |
|---|---|
| Screens | 21 |
| Operations | 105 |
| Contracts | 9 |
| Modules | 1 |
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

### 1 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **TODO** — waves 2, 3

## Modules

| Module | Screens | Waves |
|---|---|---|
| TODO | 21 | 2, 3 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `PTR-001` | Partner Login / MFA | TODO | 2 | 12 | yes |
| `PTR-002` | Partner Dashboard | TODO | 2 | 16 | yes |
| `PTR-003` | Profile & Company Details | TODO | 2 | 4 | yes |
| `PTR-004` | Notifications | TODO | 3 | 2 | yes |
| `PTR-005` | Inventory & Allocation View | TODO | 2 | 19 | yes |
| `PTR-006` | Product Catalog (B2B Pricing) | TODO | 2 | 17 | yes |
| `PTR-007` | Availability Search | TODO | 2 | 1 | yes |
| `PTR-008` | Booking Creation | TODO | 2 | 14 | yes |
| `PTR-009` | Group / Bulk Booking | TODO | 3 | 4 | yes |
| `PTR-010` | Cart & Quote | TODO | 3 | 16 | yes |
| `PTR-011` | Quote Management | TODO | 3 | 2 | yes |
| `PTR-012` | Checkout / Credit Purchase | TODO | 2 | 4 | yes |
| `PTR-013` | Credit Limit & Balance | TODO | 2 | 3 | yes |
| `PTR-014` | Settlement & Payment History | TODO | 3 | 5 | yes |
| `PTR-015` | Order History | TODO | 2 | 14 | yes |
| `PTR-016` | Voucher / Ticket Download | TODO | 2 | 13 | yes |
| `PTR-017` | Commission Statement | TODO | 3 | 2 | yes |
| `PTR-018` | Reports & Sales Performance | TODO | 3 | 9 | yes |
| `PTR-019` | API Credentials & Integration | TODO | 3 | 0 | yes |
| `PTR-020` | Sub-Agent Management | TODO | 3 | 3 | yes |
| `PTR-021` | Support & Contact | TODO | 3 | 7 | yes |

