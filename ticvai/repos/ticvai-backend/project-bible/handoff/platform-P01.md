# P01 Guest Web — platform

**Derived.** `python3 tools/derive-platform.py P01`. App `guest-web` · guest · web

| | |
|---|---|
| Screens | 46 |
| Operations | 115 |
| Contracts | 14 |
| Modules | 13 |
| Undrawn | 0 |
| Operations with no screen | 0 |
| Waves | wave1 21 · wave2 21 · wave3 4 |

## Gaps

### 5 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Booking & Selection** — waves 1, 2, 3
- **Engagement & Support** — waves 1, 2, 3
- **Membership, Loyalty & Value** — waves 2, 3
- **Support** — waves 2, 3
- **Ticketing** — waves 1, 2

## Modules

| Module | Screens | Waves |
|---|---|---|
| Engagement & Support | 6 | 1, 2, 3 |
| In-venue Services | 6 | 2 |
| Booking & Selection | 5 | 1, 2, 3 |
| Cart & Checkout | 5 | 1 |
| Account & Self-Service | 5 | 1 |
| Membership, Loyalty & Value | 5 | 2, 3 |
| Discovery & Browse | 4 | 1 |
| Ticketing | 3 | 1, 2 |
| Retail | 2 | 2 |
| Support | 2 | 2, 3 |
| High-Demand Access | 1 | 2 |
| System States | 1 | 1 |
| Promotions | 1 | 2 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `WEB-001` | Home / Landing | Discovery & Browse | 1 | 3 | yes |
| `WEB-002` | Event & Attraction Listing | Discovery & Browse | 1 | 4 | yes |
| `WEB-003` | Search Results | Discovery & Browse | 1 | 2 | yes |
| `WEB-004` | Attraction Details | Discovery & Browse | 1 | 4 | yes |
| `WEB-005` | Ticket Type Selection | Booking & Selection | 1 | 2 | yes |
| `WEB-006` | Date & Session Selection | Booking & Selection | 1 | 2 | yes |
| `WEB-007` | Interactive Seat Selection | Booking & Selection | 2 | 3 | yes |
| `WEB-008` | Add-ons & Upsell | Booking & Selection | 2 | 2 | yes |
| `WEB-009` | Wishlist | Booking & Selection | 3 | 3 | yes |
| `WEB-010` | Shopping Cart | Cart & Checkout | 1 | 9 | yes |
| `WEB-011` | Guest Details & Attendee Forms | Cart & Checkout | 1 | 10 | yes |
| `WEB-012` | Checkout — Payment | Cart & Checkout | 1 | 4 | yes |
| `WEB-013` | Booking Confirmation | Cart & Checkout | 1 | 3 | yes |
| `WEB-014` | Pay for a Booking | Cart & Checkout | 1 | 2 | yes |
| `WEB-015` | Branded Queue / Waiting Room | High-Demand Access | 2 | 3 | yes |
| `WEB-016` | Login / Register | Account & Self-Service | 1 | 19 | yes |
| `WEB-017` | My Account Dashboard | Account & Self-Service | 1 | 7 | yes |
| `WEB-018` | My Tickets | Account & Self-Service | 1 | 6 | yes |
| `WEB-019` | Order History | Account & Self-Service | 1 | 4 | yes |
| `WEB-020` | Profile & Preferences | Account & Self-Service | 1 | 5 | yes |
| `WEB-021` | Wallet & Gift Cards | Membership, Loyalty & Value | 2 | 3 | yes |
| `WEB-022` | Membership Plans | Membership, Loyalty & Value | 2 | 4 | yes |
| `WEB-023` | Membership Management | Membership, Loyalty & Value | 2 | 3 | yes |
| `WEB-024` | Devices, Wishlist & Consent | Membership, Loyalty & Value | 3 | 7 | yes |
| `WEB-025` | Help Centre / FAQ | Engagement & Support | 1 | 1 | yes |
| `WEB-026` | Survey & Feedback | Engagement & Support | 3 | 1 | yes |
| `WEB-027` | Newsletter Subscription | Engagement & Support | 2 | 9 | yes |
| `WEB-028` | Contact & Venue Information | Engagement & Support | 1 | 1 | yes |
| `WEB-029` | Error / Sold Out / Maintenance | System States | 1 | 1 | yes |
| `WEB-030` | Ticket Transfer | Ticketing | 1 | 3 | yes |
| `WEB-031` | My Reservations | Ticketing | 2 | 3 | yes |
| `WEB-032` | Offers & Promotions | Promotions | 2 | 3 | yes |
| `WEB-033` | Shop | Retail | 2 | 4 | yes |
| `WEB-034` | Lost & Found | Support | 3 | 3 | yes |
| `WEB-035` | Multi-Currency & Pricing | Ticketing | 1 | 2 | yes |
| `WEB-036` | F&B – Browse & Order | In-venue Services | 2 | 8 | yes |
| `WEB-037` | Menu Item Detail | In-venue Services | 2 | 2 | yes |
| `WEB-038` | F&B – Order Tracking | In-venue Services | 2 | 3 | yes |
| `WEB-039` | Venue Map & Wait Times | In-venue Services | 2 | 4 | yes |
| `WEB-040` | Virtual Queue | In-venue Services | 2 | 4 | yes |
| `WEB-041` | Parking – Reserve & Pay | In-venue Services | 2 | 3 | yes |
| `WEB-042` | Retail & Shop and Drop | Retail | 2 | 4 | yes |
| `WEB-043` | Loyalty & Rewards | Membership, Loyalty & Value | 2 | 4 | yes |
| `WEB-044` | AI Concierge – Home | Engagement & Support | 2 | 5 | yes |
| `WEB-045` | Help Centre & Accessibility | Support | 2 | 2 | yes |
| `WEB-046` | In-Venue Notifications | Engagement & Support | 2 | 1 | yes |

