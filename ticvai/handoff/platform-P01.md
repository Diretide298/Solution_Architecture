# P01 Guest Web — platform

**Derived.** `python3 tools/derive-platform.py P01`. App `guest-web` · guest · web

| | |
|---|---|
| Screens | 46 |
| Operations | 112 |
| Contracts | 14 |
| Modules | 13 |
| Undrawn | 0 |
| Operations with no screen | 28 |
| Waves | wave1 21 · wave2 21 · wave3 4 |

## Gaps

### 28 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `enrolFacePass` | access | POST | Register a facial profile against an entitlement |
| `getFacePassEnrolment` | access | GET | Whether a pass has a face registered, and when |
| `revokeFacePass` | access | DELETE | Remove a facial profile |
| `freezeEntitlement` | catalogue | POST | Pause a membership at the guest's request |
| `joinWaitlist` | catalogue | POST | Ask to be told if capacity frees up |
| `leaveWaitlist` | catalogue | DELETE | Stop waiting |
| `updateTableReservation` | fnb | PATCH | Change or cancel a booking |
| `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| `deleteGuestAccount` | identity | DELETE | Self-service account deletion |
| `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| `createReferral` | marketing-crm | POST | Issue a referral code |
| `getMyChallenges` | marketing-crm | GET | Active challenges and how far along I am |
| `getWaiverStatus` | marketing-crm | GET | Whether this guest may be issued a ticket that requires a waiver |
| `recordLostItem` | marketing-crm | POST | Report something lost, or hand something in |
| `respondToInvitation` | marketing-crm | POST | Accept or decline |
| `submitForm` | marketing-crm | POST | Sign a waiver, answer a survey, capture details |
| `updateGuestPreferences` | marketing-crm | PUT | The things a regular should not have to say twice |
| `uploadGuestDocument` | marketing-crm | POST | Store a guest photo, ID or signed document |
| `convertToTermProduct` | orders | POST | Turn a visit into a membership or season pass |
| `createCart` | orders | POST | Start a cart |
| `createResaleListing` | orders | POST | List an entitlement for resale |
| `getGroupBooking` | orders | GET |  |
| `listPaymentTokens` | orders | GET | A guest's saved payment methods |
| `quoteUpgrade` | orders | POST | What an upgrade costs, pro-rata |
| `shareEntitlement` | orders | POST | Let somebody else use this, without giving it away |
| `storePaymentToken` | orders | POST | Save a payment method for future use |
| `transferWalletBalance` | retail | POST | Send balance to another guest |
| `assignSeats` | seating | POST | Pick and hold the best available seats |

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
| `WEB-002` | Event & Attraction Listing | Discovery & Browse | 1 | 3 | yes |
| `WEB-003` | Search Results | Discovery & Browse | 1 | 2 | yes |
| `WEB-004` | Event / Attraction Detail | Discovery & Browse | 1 | 2 | yes |
| `WEB-005` | Ticket Type Selection | Booking & Selection | 1 | 2 | yes |
| `WEB-006` | Date & Session Selection | Booking & Selection | 1 | 2 | yes |
| `WEB-007` | Seat Map Selection | Booking & Selection | 2 | 2 | yes |
| `WEB-008` | Add-ons & Upsell | Booking & Selection | 2 | 2 | yes |
| `WEB-009` | Wishlist | Booking & Selection | 3 | 3 | yes |
| `WEB-010` | Shopping Cart | Cart & Checkout | 1 | 9 | yes |
| `WEB-011` | Guest Details & Attendee Forms | Cart & Checkout | 1 | 10 | yes |
| `WEB-012` | Checkout — Payment | Cart & Checkout | 1 | 4 | yes |
| `WEB-013` | Order Confirmation | Cart & Checkout | 1 | 3 | yes |
| `WEB-014` | Pay for a Booking | Cart & Checkout | 1 | 2 | yes |
| `WEB-015` | Virtual Waiting Room | High-Demand Access | 2 | 3 | yes |
| `WEB-016` | Login / Register | Account & Self-Service | 1 | 19 | yes |
| `WEB-017` | My Account Dashboard | Account & Self-Service | 1 | 7 | yes |
| `WEB-018` | My Tickets | Account & Self-Service | 1 | 5 | yes |
| `WEB-019` | Order History | Account & Self-Service | 1 | 2 | yes |
| `WEB-020` | Profile & Preferences | Account & Self-Service | 1 | 5 | yes |
| `WEB-021` | Wallet & Gift Cards | Membership, Loyalty & Value | 2 | 3 | yes |
| `WEB-022` | Membership Plans | Membership, Loyalty & Value | 2 | 4 | yes |
| `WEB-023` | Membership Management | Membership, Loyalty & Value | 2 | 3 | yes |
| `WEB-024` | Loyalty & Rewards | Membership, Loyalty & Value | 3 | 7 | yes |
| `WEB-025` | Help Centre / FAQ | Engagement & Support | 1 | 1 | yes |
| `WEB-026` | Survey & Feedback | Engagement & Support | 3 | 1 | yes |
| `WEB-027` | Newsletter Subscription | Engagement & Support | 2 | 7 | yes |
| `WEB-028` | Contact & Venue Information | Engagement & Support | 1 | 1 | yes |
| `WEB-029` | Error / Sold Out / Maintenance | System States | 1 | 1 | yes |
| `WEB-030` | Ticket Transfer | Ticketing | 1 | 3 | yes |
| `WEB-031` | My Reservations | Ticketing | 2 | 3 | yes |
| `WEB-032` | Offers & Promotions | Promotions | 2 | 3 | yes |
| `WEB-033` | Shop | Retail | 2 | 4 | yes |
| `WEB-034` | Lost & Found | Support | 3 | 3 | yes |
| `WEB-035` | Multi-Currency & Pricing | Ticketing | 1 | 2 | yes |
| `WEB-036` | F&B — Browse & Order | In-venue Services | 2 | 7 | yes |
| `WEB-037` | Menu Item Detail | In-venue Services | 2 | 2 | yes |
| `WEB-038` | F&B — Order Tracking | In-venue Services | 2 | 3 | yes |
| `WEB-039` | Venue Map & Wait Times | In-venue Services | 2 | 4 | yes |
| `WEB-040` | Virtual Queue | In-venue Services | 2 | 4 | yes |
| `WEB-041` | Parking — Reserve & Pay | In-venue Services | 2 | 3 | yes |
| `WEB-042` | Retail & Shop and Drop | Retail | 2 | 4 | yes |
| `WEB-043` | Loyalty & Rewards | Membership, Loyalty & Value | 2 | 4 | yes |
| `WEB-044` | AI Concierge | Engagement & Support | 2 | 4 | yes |
| `WEB-045` | Help Centre & Accessibility | Support | 2 | 2 | yes |
| `WEB-046` | In-Venue Notifications | Engagement & Support | 2 | 1 | yes |

