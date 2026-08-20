# P01 Guest Web — platform

**Derived.** `python3 tools/derive-platform.py P01`. App `guest-web` · guest · web

| | |
|---|---|
| Screens | 35 |
| Operations | 77 |
| Contracts | 10 |
| Modules | 12 |
| Undrawn | 6 |
| Operations with no screen | 26 |
| Waves | wave1 20 · wave2 11 · wave3 4 |

## Gaps

### 26 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `freezeEntitlement` | catalogue | POST | Pause a membership at the guest's request |
| `getMyMemberships` | catalogue | GET | A guest's own memberships, benefits and history |
| `listGuestMemberships` | catalogue | GET | A guest's memberships, benefits and history |
| `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| `grantDelegation` | identity | POST | Let one guest act for another |
| `listDelegations` | identity | GET | Who may act for this guest, and for whom they may act |
| `createReferral` | marketing-crm | POST | Issue a referral code |
| `getMyChallenges` | marketing-crm | GET | Active challenges and how far along I am |
| `getWaiverStatus` | marketing-crm | GET | Whether this guest may be issued a ticket that requires a waiver |
| `listLostItems` | marketing-crm | GET | Reported and found, with suggested matches |
| `recordLostItem` | marketing-crm | POST | Report something lost, or hand something in |
| `redeemLoyaltyPoints` | marketing-crm | POST | Spend points |
| `respondToInvitation` | marketing-crm | POST | Accept or decline |
| `submitForm` | marketing-crm | POST | Sign a waiver, answer a survey, capture details |
| `updateMyProfile` | marketing-crm | PATCH | A guest correcting their own details |
| `uploadGuestDocument` | marketing-crm | POST | Store a guest photo, ID or signed document |
| `convertToTermProduct` | orders | POST | Turn a visit into a membership or season pass |
| `createResaleListing` | orders | POST | List an entitlement for resale |
| `issueWalletPass` | orders | POST | Generate an Apple or Google wallet pass |
| `listPaymentTokens` | orders | GET | A guest's saved payment methods |
| `quoteUpgrade` | orders | POST | What an upgrade costs, pro-rata |
| `shareEntitlement` | orders | POST | Let somebody else use this, without giving it away |
| `storePaymentToken` | orders | POST | Save a payment method for future use |
| `getRecommendations` | promotions | POST | What else this guest might want |
| `transferWalletBalance` | retail | POST | Send balance to another guest |
| `assignSeats` | seating | POST | Pick and hold the best available seats |

### 5 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Booking & Selection** — waves 1, 2, 3
- **Cart & Checkout** — waves 1, 2
- **Engagement & Support** — waves 1, 2, 3
- **Membership, Loyalty & Value** — waves 2, 3
- **Ticketing** — waves 1, 2

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
| Booking & Selection | 5 | 1, 2, 3 |
| Cart & Checkout | 5 | 1, 2 |
| Account & Self-Service | 5 | 1 |
| Discovery & Browse | 4 | 1 |
| Membership, Loyalty & Value | 4 | 2, 3 |
| Engagement & Support | 4 | 1, 2, 3 |
| Ticketing | 3 | 1, 2 |
| High-Demand Access | 1 | 2 |
| System States | 1 | 1 |
| Promotions | 1 | 2 |
| Retail | 1 | 2 |
| Support | 1 | 3 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `WEB-001` | Home / Landing | Discovery & Browse | 1 | 3 | yes |
| `WEB-002` | Event & Attraction Listing | Discovery & Browse | 1 | 3 | yes |
| `WEB-003` | Search Results | Discovery & Browse | 1 | 2 | yes |
| `WEB-004` | Event / Attraction Detail | Discovery & Browse | 1 | 2 | yes |
| `WEB-005` | Ticket Type Selection | Booking & Selection | 1 | 2 | yes |
| `WEB-006` | Date & Session Selection | Booking & Selection | 1 | 1 | yes |
| `WEB-007` | Seat Map Selection | Booking & Selection | 2 | 2 | yes |
| `WEB-008` | Add-ons & Upsell | Booking & Selection | 2 | 3 | yes |
| `WEB-009` | Wishlist | Booking & Selection | 3 | 7 | yes |
| `WEB-010` | Shopping Cart | Cart & Checkout | 1 | 9 | yes |
| `WEB-011` | Guest Details & Attendee Forms | Cart & Checkout | 1 | 9 | yes |
| `WEB-012` | Checkout — Payment | Cart & Checkout | 1 | 3 | yes |
| `WEB-013` | Order Confirmation | Cart & Checkout | 1 | 3 | yes |
| `WEB-014` | Payment Link Landing | Cart & Checkout | 2 | 2 | yes |
| `WEB-015` | Virtual Waiting Room | High-Demand Access | 2 | 3 | yes |
| `WEB-016` | Login / Register | Account & Self-Service | 1 | 22 | yes |
| `WEB-017` | My Account Dashboard | Account & Self-Service | 1 | 7 | yes |
| `WEB-018` | My Tickets | Account & Self-Service | 1 | 1 | yes |
| `WEB-019` | Order History | Account & Self-Service | 1 | 1 | yes |
| `WEB-020` | Profile & Preferences | Account & Self-Service | 1 | 7 | yes |
| `WEB-021` | Wallet & Gift Cards | Membership, Loyalty & Value | 2 | 3 | yes |
| `WEB-022` | Membership Plans | Membership, Loyalty & Value | 2 | 2 | yes |
| `WEB-023` | Membership Management | Membership, Loyalty & Value | 2 | 1 | yes |
| `WEB-024` | Loyalty & Rewards | Membership, Loyalty & Value | 3 | 7 | yes |
| `WEB-025` | Help Centre / FAQ | Engagement & Support | 1 | 1 | yes |
| `WEB-026` | Survey & Feedback | Engagement & Support | 3 | 1 | yes |
| `WEB-027` | Newsletter Subscription | Engagement & Support | 2 | 7 | yes |
| `WEB-028` | Contact & Venue Information | Engagement & Support | 1 | 1 | yes |
| `WEB-029` | Error / Sold Out / Maintenance | System States | 1 | 1 | yes |
| `WEB-030` | Ticket Transfer | Ticketing | 1 | 3 | **no** |
| `WEB-031` | My Reservations | Ticketing | 2 | 3 | **no** |
| `WEB-032` | Offers & Promotions | Promotions | 2 | 3 | **no** |
| `WEB-033` | Shop | Retail | 2 | 4 | **no** |
| `WEB-034` | Lost & Found | Support | 3 | 2 | **no** |
| `WEB-035` | Multi-Currency & Pricing | Ticketing | 1 | 2 | **no** |

