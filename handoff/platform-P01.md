# P01 Guest Web — platform

**Derived.** `python3 tools/derive-platform.py P01`. App `guest-web` · guest · web

| | |
|---|---|
| Screens | 35 |
| Operations | 77 |
| Contracts | 10 |
| Modules | 10 |
| Undrawn | 6 |
| Operations with no screen | 0 |
| Waves | wave1 20 · wave2 11 · wave3 4 |

## Gaps

### 4 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **catalogue** — waves 1, 2
- **marketing-crm** — waves 1, 2, 3
- **orders** — waves 1, 2
- **promotions** — waves 1, 2

### 6 screens nobody has drawn

- `WEB-030` Ticket Transfer — wave 1
- `WEB-031` My Reservations — wave 2
- `WEB-032` Offers & Promotions — wave 2
- `WEB-033` Shop — wave 2
- `WEB-034` Lost & Found — wave 3
- `WEB-035` Multi-Currency & Pricing — wave 1

## Modules

| Module | Screens | Waves |
|---|---|---|
| orders | 10 | 1, 2 |
| marketing-crm | 8 | 1, 2, 3 |
| catalogue | 5 | 1, 2 |
| white-label | 4 | 1 |
| promotions | 2 | 1, 2 |
| retail | 2 | 2 |
| seating | 1 | 2 |
| queue | 1 | 2 |
| identity | 1 | 1 |
| finance | 1 | 1 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `WEB-001` | Home / Landing | white-label | 1 | 3 | yes |
| `WEB-002` | Event & Attraction Listing | catalogue | 1 | 3 | yes |
| `WEB-003` | Search Results | catalogue | 1 | 2 | yes |
| `WEB-004` | Event / Attraction Detail | catalogue | 1 | 2 | yes |
| `WEB-005` | Ticket Type Selection | promotions | 1 | 2 | yes |
| `WEB-006` | Date & Session Selection | catalogue | 1 | 1 | yes |
| `WEB-007` | Seat Map Selection | seating | 2 | 2 | yes |
| `WEB-008` | Add-ons & Upsell | orders | 2 | 3 | yes |
| `WEB-009` | Wishlist | marketing-crm | 3 | 7 | yes |
| `WEB-010` | Shopping Cart | orders | 1 | 9 | yes |
| `WEB-011` | Guest Details & Attendee Forms | marketing-crm | 1 | 9 | yes |
| `WEB-012` | Checkout — Payment | orders | 1 | 3 | yes |
| `WEB-013` | Order Confirmation | orders | 1 | 3 | yes |
| `WEB-014` | Payment Link Landing | orders | 2 | 2 | yes |
| `WEB-015` | Virtual Waiting Room | queue | 2 | 3 | yes |
| `WEB-016` | Login / Register | identity | 1 | 22 | yes |
| `WEB-017` | My Account Dashboard | marketing-crm | 1 | 7 | yes |
| `WEB-018` | My Tickets | orders | 1 | 1 | yes |
| `WEB-019` | Order History | orders | 1 | 1 | yes |
| `WEB-020` | Profile & Preferences | marketing-crm | 1 | 7 | yes |
| `WEB-021` | Wallet & Gift Cards | retail | 2 | 3 | yes |
| `WEB-022` | Membership Plans | catalogue | 2 | 2 | yes |
| `WEB-023` | Membership Management | orders | 2 | 1 | yes |
| `WEB-024` | Loyalty & Rewards | marketing-crm | 3 | 7 | yes |
| `WEB-025` | Help Centre / FAQ | white-label | 1 | 1 | yes |
| `WEB-026` | Survey & Feedback | marketing-crm | 3 | 1 | yes |
| `WEB-027` | Newsletter Subscription | marketing-crm | 2 | 7 | yes |
| `WEB-028` | Contact & Venue Information | white-label | 1 | 1 | yes |
| `WEB-029` | Error / Sold Out / Maintenance | white-label | 1 | 1 | yes |
| `WEB-030` | Ticket Transfer | orders | 1 | 3 | **no** |
| `WEB-031` | My Reservations | orders | 2 | 3 | **no** |
| `WEB-032` | Offers & Promotions | promotions | 2 | 3 | **no** |
| `WEB-033` | Shop | retail | 2 | 4 | **no** |
| `WEB-034` | Lost & Found | marketing-crm | 3 | 2 | **no** |
| `WEB-035` | Multi-Currency & Pricing | finance | 1 | 2 | **no** |

