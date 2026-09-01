# P02 Guest App — platform

**Derived.** `python3 tools/derive-platform.py P02`. App `guest-app` · guest · mobileApp · offline-capable

| | |
|---|---|
| Screens | 63 |
| Operations | 101 |
| Contracts | 15 |
| Modules | 16 |
| Undrawn | 0 |
| Operations with no screen | 28 |
| Waves | wave1 20 · wave2 27 · wave3 16 |

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

### 6 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Account & Self-Service** — waves 1, 2, 3
- **Booking & Selection** — waves 1, 2, 3
- **Discovery & Browse** — waves 1, 2
- **Engagement & Support** — waves 2, 3
- **In-Venue Experience** — waves 2, 3
- **In-venue Services** — waves 2, 3

## Modules

| Module | Screens | Waves |
|---|---|---|
| Engagement & Support | 11 | 2, 3 |
| Account & Self-Service | 9 | 1, 2, 3 |
| In-venue Services | 9 | 2, 3 |
| Discovery & Browse | 7 | 1, 2 |
| Booking & Selection | 7 | 1, 2, 3 |
| Ticketing | 4 | 2 |
| Cart & Checkout | 3 | 1 |
| Membership, Loyalty & Value | 3 | 2 |
| System States | 2 | 1 |
| In-Venue Experience | 2 | 2, 3 |
| Retail | 1 | 2 |
| Support | 1 | 2 |
| Promotions | 1 | 2 |
| High-Demand Access | 1 | 1 |
| Discovery | 1 | 1 |
| Marketing | 1 | 3 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `GST-001` | Home – Default | Discovery & Browse | 1 | 4 | yes |
| `GST-002` | Explore Categories | Discovery & Browse | 1 | 1 | yes |
| `GST-003` | Event & Attraction Listing | Discovery & Browse | 1 | 4 | yes |
| `GST-004` | Attraction Details | Discovery & Browse | 1 | 4 | yes |
| `GST-005` | What's On | Discovery & Browse | 1 | 2 | yes |
| `GST-006` | Event / Exhibition Details | Discovery & Browse | 1 | 2 | yes |
| `GST-007` | Select Date & Time | Booking & Selection | 1 | 2 | yes |
| `GST-008` | Tickets & Add-ons | Booking & Selection | 1 | 1 | yes |
| `GST-009` | Review & Payment | Cart & Checkout | 1 | 5 | yes |
| `GST-010` | Booking Confirmation | Cart & Checkout | 1 | 3 | yes |
| `GST-011` | Wallet Overview | Membership, Loyalty & Value | 2 | 2 | yes |
| `GST-012` | My Tickets | Account & Self-Service | 1 | 6 | yes |
| `GST-013` | Ticket Details | Account & Self-Service | 1 | 4 | yes |
| `GST-014` | Ticket Transfer | Ticketing | 2 | 3 | yes |
| `GST-015` | Memberships | Membership, Loyalty & Value | 2 | 5 | yes |
| `GST-016` | My Reservations | Ticketing | 2 | 3 | yes |
| `GST-017` | Reservation Details | Ticketing | 2 | 2 | yes |
| `GST-018` | Add to Calendar / Reminders | Account & Self-Service | 3 | 3 | yes |
| `GST-019` | Order History | Account & Self-Service | 2 | 4 | yes |
| `GST-020` | Saved Items / Wishlist | Account & Self-Service | 3 | 3 | yes |
| `GST-021` | Interactive Map | In-venue Services | 2 | 4 | yes |
| `GST-022` | Attraction Wait Times | In-venue Services | 2 | 1 | yes |
| `GST-023` | Virtual Queue | In-venue Services | 3 | 4 | yes |
| `GST-024` | F&B – Browse & Order | In-venue Services | 2 | 8 | yes |
| `GST-025` | F&B – Order Tracking | In-venue Services | 2 | 3 | yes |
| `GST-026` | Retail / Merchandise | Retail | 2 | 2 | yes |
| `GST-027` | Parking – Reserve & Pay | In-venue Services | 3 | 3 | yes |
| `GST-028` | Parking – Reservation Confirmed | In-venue Services | 3 | 2 | yes |
| `GST-029` | Venue Info & Services | In-venue Services | 2 | 2 | yes |
| `GST-030` | In-Venue Notifications | Engagement & Support | 2 | 1 | yes |
| `GST-031` | AI Concierge – Home | Engagement & Support | 2 | 5 | yes |
| `GST-032` | AI Concierge – Chat | Engagement & Support | 2 | 8 | yes |
| `GST-033` | AI Concierge – Contextual Help | Engagement & Support | 2 | 1 | yes |
| `GST-034` | Lost & Found | Support | 2 | 3 | yes |
| `GST-035` | Feedback & Ratings | Engagement & Support | 3 | 2 | yes |
| `GST-036` | Loyalty & Rewards | Membership, Loyalty & Value | 2 | 4 | yes |
| `GST-037` | Offers & Promotions | Promotions | 2 | 3 | yes |
| `GST-038` | Digital Companion Mode | In-venue Services | 3 | 3 | yes |
| `GST-039` | Profile | Account & Self-Service | 1 | 1 | yes |
| `GST-040` | Help & Support | Engagement & Support | 2 | 5 | yes |
| `GST-041` | Checkout Entry | Cart & Checkout | 1 | 2 | yes |
| `GST-042` | Simple Registration & OTP | Account & Self-Service | 1 | 18 | yes |
| `GST-043` | Arabic / RTL Experience | System States | 1 | 0 | yes |
| `GST-044` | Multi-Currency & Pricing | Ticketing | 2 | 2 | yes |
| `GST-045` | Ticket Delivery & Sharing | Account & Self-Service | 2 | 1 | yes |
| `GST-046` | Branded Queue / Waiting Room | High-Demand Access | 1 | 3 | yes |
| `GST-047` | Maintenance / Upgrade Page | System States | 1 | 1 | yes |
| `GST-048` | Upsell / Cross-Sell | Booking & Selection | 2 | 2 | yes |
| `GST-049` | Interactive Seat Selection | Booking & Selection | 2 | 3 | yes |
| `GST-050` | Resource Booking – Cabana | Booking & Selection | 3 | 3 | yes |
| `GST-051` | Plan Your Adventure – Start | Engagement & Support | 3 | 2 | yes |
| `GST-052` | Suggested Itineraries | Engagement & Support | 3 | 3 | yes |
| `GST-053` | Build Your Own Itinerary | Engagement & Support | 3 | 4 | yes |
| `GST-054` | AI Optimized Itinerary | Engagement & Support | 3 | 4 | yes |
| `GST-055` | Dynamic QR Ticket | Account & Self-Service | 1 | 1 | yes |
| `GST-056` | Bundle Package | Booking & Selection | 2 | 3 | yes |
| `GST-057` | Accessibility Information | Discovery & Browse | 2 | 1 | yes |
| `GST-058` | Resource Availability (Cabana) | Booking & Selection | 3 | 2 | yes |
| `GST-059` | Plan My Day – In Progress | Engagement & Support | 3 | 3 | yes |
| `GST-061` | Menu Item Detail | In-Venue Experience | 2 | 2 | yes |
| `GST-062` | Shop & Drop Collection | In-Venue Experience | 3 | 1 | yes |
| `GST-063` | Search | Discovery | 1 | 1 | yes |
| `GST-065` | Newsletter & Preferences | Marketing | 3 | 2 | yes |

