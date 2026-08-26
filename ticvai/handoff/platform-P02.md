# P02 Guest App — platform

**Derived.** `python3 tools/derive-platform.py P02`. App `guest-app` · guest · mobileApp · offline-capable

| | |
|---|---|
| Screens | 63 |
| Operations | 97 |
| Contracts | 15 |
| Modules | 4 |
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

### 2 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **In-Venue Experience** — waves 2, 3
- **TODO** — waves 1, 2, 3

## Modules

| Module | Screens | Waves |
|---|---|---|
| TODO | 59 | 1, 2, 3 |
| In-Venue Experience | 2 | 2, 3 |
| Discovery | 1 | 1 |
| Marketing | 1 | 3 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `GST-001` | Home – Default | TODO | 1 | 4 | yes |
| `GST-002` | Explore Categories | TODO | 1 | 1 | yes |
| `GST-003` | Attractions List | TODO | 1 | 2 | yes |
| `GST-004` | Attraction Details | TODO | 1 | 3 | yes |
| `GST-005` | What's On | TODO | 1 | 2 | yes |
| `GST-006` | Event / Exhibition Details | TODO | 1 | 2 | yes |
| `GST-007` | Select Date & Time | TODO | 1 | 2 | yes |
| `GST-008` | Tickets & Add-ons | TODO | 1 | 1 | yes |
| `GST-009` | Review & Payment | TODO | 1 | 5 | yes |
| `GST-010` | Booking Confirmation | TODO | 1 | 2 | yes |
| `GST-011` | Wallet Overview | TODO | 2 | 2 | yes |
| `GST-012` | My Tickets | TODO | 1 | 3 | yes |
| `GST-013` | Ticket Details | TODO | 1 | 4 | yes |
| `GST-014` | Ticket Transfer | TODO | 2 | 2 | yes |
| `GST-015` | Memberships | TODO | 2 | 5 | yes |
| `GST-016` | My Reservations | TODO | 2 | 3 | yes |
| `GST-017` | Reservation Details | TODO | 2 | 2 | yes |
| `GST-018` | Add to Calendar / Reminders | TODO | 3 | 3 | yes |
| `GST-019` | Order History (Wallet) | TODO | 2 | 3 | yes |
| `GST-020` | Saved Items / Wishlist | TODO | 3 | 3 | yes |
| `GST-021` | Interactive Map | TODO | 2 | 4 | yes |
| `GST-022` | Attraction Wait Times | TODO | 2 | 1 | yes |
| `GST-023` | Virtual Queue / Join Queue | TODO | 3 | 3 | yes |
| `GST-024` | F&B – Browse & Order | TODO | 2 | 6 | yes |
| `GST-025` | F&B – Order Tracking | TODO | 2 | 3 | yes |
| `GST-026` | Retail / Merchandise | TODO | 2 | 2 | yes |
| `GST-027` | Parking – Reserve & Pay | TODO | 3 | 2 | yes |
| `GST-028` | Parking – Reservation Confirmed | TODO | 3 | 2 | yes |
| `GST-029` | Venue Info & Services | TODO | 2 | 2 | yes |
| `GST-030` | In-Venue Notifications | TODO | 2 | 1 | yes |
| `GST-031` | AI Concierge – Home | TODO | 2 | 2 | yes |
| `GST-032` | AI Concierge – Chat | TODO | 2 | 8 | yes |
| `GST-033` | AI Concierge – Contextual Help | TODO | 2 | 1 | yes |
| `GST-034` | Lost & Found | TODO | 2 | 3 | yes |
| `GST-035` | Feedback & Ratings | TODO | 3 | 2 | yes |
| `GST-036` | Loyalty & Rewards | TODO | 2 | 2 | yes |
| `GST-037` | Offers & Promotions | TODO | 2 | 3 | yes |
| `GST-038` | Digital Companion Mode | TODO | 3 | 3 | yes |
| `GST-039` | Profile | TODO | 1 | 1 | yes |
| `GST-040` | Help & Support | TODO | 2 | 5 | yes |
| `GST-041` | Checkout Entry | TODO | 1 | 2 | yes |
| `GST-042` | Simple Registration & OTP | TODO | 1 | 18 | yes |
| `GST-043` | Arabic / RTL Experience | TODO | 1 | 0 | yes |
| `GST-044` | Multi-Currency & Pricing | TODO | 2 | 2 | yes |
| `GST-045` | Ticket Delivery & Sharing | TODO | 2 | 1 | yes |
| `GST-046` | Branded Queue / Waiting Room | TODO | 1 | 1 | yes |
| `GST-047` | Maintenance / Upgrade Page | TODO | 1 | 1 | yes |
| `GST-048` | Upsell / Cross-Sell | TODO | 2 | 2 | yes |
| `GST-049` | Interactive Seat Selection | TODO | 2 | 3 | yes |
| `GST-050` | Resource Booking – Cabana | TODO | 3 | 3 | yes |
| `GST-051` | Plan Your Adventure – Start | TODO | 3 | 2 | yes |
| `GST-052` | Suggested Itineraries | TODO | 3 | 3 | yes |
| `GST-053` | Build Your Own Itinerary | TODO | 3 | 4 | yes |
| `GST-054` | AI Optimized Itinerary | TODO | 3 | 4 | yes |
| `GST-055` | Dynamic QR Ticket | TODO | 1 | 1 | yes |
| `GST-056` | Bundle Package | TODO | 2 | 3 | yes |
| `GST-057` | Accessibility Information | TODO | 2 | 1 | yes |
| `GST-058` | Resource Availability (Cabana) | TODO | 3 | 2 | yes |
| `GST-059` | Plan My Day – In Progress | TODO | 3 | 3 | yes |
| `GST-061` | Menu Item Detail | In-Venue Experience | 2 | 1 | yes |
| `GST-062` | Shop & Drop Collection | In-Venue Experience | 3 | 1 | yes |
| `GST-063` | Search | Discovery | 1 | 1 | yes |
| `GST-065` | Newsletter & Preferences | Marketing | 3 | 2 | yes |

