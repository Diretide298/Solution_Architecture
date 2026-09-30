# P02 Guest App — platform

**Derived.** `python3 tools/derive-platform.py P02`. App `guest-app` · guest · mobileApp · offline-capable

| | |
|---|---|
| Screens | 77 |
| Operations | 217 |
| Contracts | 19 |
| Modules | 17 |
| Undrawn | 0 |
| Operations with no screen | 19 |
| Waves | wave1 25 · wave2 35 · wave3 17 |

## Gaps

### 19 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `createParkingEntitlement` | access | POST | A guest bought parking |
| `getPlanBenefits` | catalogue | GET | Which benefits a plan grants, and how much of each |
| `listMembershipBenefits` | catalogue | GET | Benefits a plan can grant |
| `listMembershipProgrammes` | catalogue | GET | Membership schemes, the level above a plan |
| `listCustomerMemberships` | identity | GET | Memberships a customer holds |
| `checkGuestCheckoutMatch` | marketing-crm | POST | Does this contact already have a profile here |
| `decideGuestCheckoutMatch` | marketing-crm | POST | Use the existing profile or keep this booking separate |
| `getForm` | marketing-crm | GET | One form, to fill in or to edit |
| `getMyProfile` | marketing-crm | GET | A guest reading their own details |
| `listBadges` | marketing-crm | GET | Badges a guest can be awarded |
| `listCustomerBadges` | marketing-crm | GET | Badges a guest holds |
| `listLeaderboard` | marketing-crm | GET | Standings, by nickname |
| `listRewards` | marketing-crm | GET | What points can be turned into |
| `setLeaderboardNickname` | marketing-crm | PUT | Choose the name shown on the board |
| `listTicketTransfers` | orders | GET | The ticket transfers this guest sent or received |
| `revokeEntitlementShare` | orders | POST | Take back a share |
| `getUpsellSuggestions` | promotions | POST | Suggestions for a cart |
| `recordRecommendationOutcome` | promotions | POST | Shown, clicked, accepted or dismissed |
| `listMyWaitingGuests` | queue | GET | The caller's own queue entries |

### 6 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Account & Self-Service** — waves 1, 2, 3
- **Booking & Selection** — waves 1, 2, 3
- **Discovery & Browse** — waves 1, 2
- **Engagement & Support** — waves 1, 2, 3
- **In-Venue Experience** — waves 2, 3
- **In-venue Services** — waves 2, 3

## Modules

| Module | Screens | Waves |
|---|---|---|
| Account & Self-Service | 14 | 1, 2, 3 |
| Engagement & Support | 12 | 1, 2, 3 |
| Booking & Selection | 10 | 1, 2, 3 |
| In-venue Services | 10 | 2, 3 |
| Discovery & Browse | 7 | 1, 2 |
| Ticketing | 4 | 2 |
| Transport | 4 | 3 |
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
| `GST-001` | Home | Discovery & Browse | 1 | 13 | yes |
| `GST-002` | Explore | Discovery & Browse | 1 | 3 | yes |
| `GST-003` | Buy Tickets | Discovery & Browse | 1 | 5 | yes |
| `GST-004` | Item Detail | Discovery & Browse | 1 | 7 | yes |
| `GST-005` | What's On | Discovery & Browse | 1 | 2 | yes |
| `GST-006` | Item Detail – Event / Exhibition | Discovery & Browse | 1 | 2 | yes |
| `GST-007` | Select Date & Time | Booking & Selection | 1 | 9 | yes |
| `GST-008` | Tickets & Add-ons | Booking & Selection | 1 | 6 | yes |
| `GST-009` | Review & Payment | Cart & Checkout | 1 | 10 | yes |
| `GST-010` | Booking Confirmation | Cart & Checkout | 1 | 3 | yes |
| `GST-011` | Wallet Overview | Membership, Loyalty & Value | 2 | 6 | yes |
| `GST-012` | My Tickets | Account & Self-Service | 1 | 6 | yes |
| `GST-013` | Ticket Details | Account & Self-Service | 1 | 5 | yes |
| `GST-014` | Ticket Transfer | Ticketing | 2 | 3 | yes |
| `GST-015` | Memberships | Membership, Loyalty & Value | 2 | 11 | yes |
| `GST-016` | My Reservations | Ticketing | 2 | 3 | yes |
| `GST-017` | Reservation Details | Ticketing | 2 | 2 | yes |
| `GST-018` | Add to Calendar / Reminders | Account & Self-Service | 3 | 6 | yes |
| `GST-019` | Order History | Account & Self-Service | 2 | 9 | yes |
| `GST-020` | Saved Items / Wishlist | Account & Self-Service | 3 | 3 | yes |
| `GST-021` | Interactive Map | In-venue Services | 2 | 4 | yes |
| `GST-022` | Attraction Wait Times | In-venue Services | 2 | 1 | yes |
| `GST-023` | Virtual Queue | In-venue Services | 3 | 5 | yes |
| `GST-024` | F&B – Browse & Order | In-venue Services | 2 | 10 | yes |
| `GST-025` | F&B – Order Tracking | In-venue Services | 2 | 3 | yes |
| `GST-026` | Retail / Merchandise | Retail | 2 | 7 | yes |
| `GST-027` | Parking – Reserve & Pay | In-venue Services | 3 | 5 | yes |
| `GST-028` | Parking – Reservation Confirmed | In-venue Services | 3 | 2 | yes |
| `GST-029` | Venue Info & Services | In-venue Services | 2 | 3 | yes |
| `GST-030` | In-Venue Notifications | Engagement & Support | 2 | 3 | yes |
| `GST-031` | AI Concierge – Home | Engagement & Support | 2 | 5 | yes |
| `GST-032` | AI Concierge – Chat | Engagement & Support | 2 | 9 | yes |
| `GST-033` | AI Concierge – Contextual Help | Engagement & Support | 2 | 1 | yes |
| `GST-034` | Lost & Found | Support | 2 | 3 | yes |
| `GST-035` | Feedback & Ratings | Engagement & Support | 3 | 2 | yes |
| `GST-036` | Loyalty & Rewards | Membership, Loyalty & Value | 2 | 5 | yes |
| `GST-037` | Offers & Promotions | Promotions | 2 | 3 | yes |
| `GST-038` | At the Venue | In-venue Services | 3 | 3 | yes |
| `GST-039` | Profile | Account & Self-Service | 1 | 2 | yes |
| `GST-040` | Help & Support | Engagement & Support | 2 | 6 | yes |
| `GST-041` | Checkout Entry | Cart & Checkout | 1 | 12 | yes |
| `GST-042` | Simple Registration & OTP | Account & Self-Service | 1 | 13 | yes |
| `GST-043` | Arabic / RTL Experience | System States | 1 | 0 | yes |
| `GST-044` | Multi-Currency & Pricing | Ticketing | 2 | 2 | yes |
| `GST-045` | Ticket Delivery & Sharing | Account & Self-Service | 2 | 1 | yes |
| `GST-046` | Branded Queue / Waiting Room | High-Demand Access | 1 | 3 | yes |
| `GST-047` | Maintenance / Upgrade Page | System States | 1 | 1 | yes |
| `GST-048` | Upsell / Cross-Sell | Booking & Selection | 2 | 3 | yes |
| `GST-049` | Interactive Seat Selection | Booking & Selection | 2 | 5 | yes |
| `GST-050` | Resource Booking – Cabana | Booking & Selection | 3 | 3 | yes |
| `GST-051` | Plan | Engagement & Support | 1 | 4 | yes |
| `GST-052` | Suggested Itineraries | Engagement & Support | 1 | 3 | yes |
| `GST-053` | Your Plan | Engagement & Support | 1 | 7 | yes |
| `GST-054` | AI Planner | Engagement & Support | 1 | 6 | yes |
| `GST-055` | Dynamic QR Ticket | Account & Self-Service | 1 | 5 | yes |
| `GST-056` | Bundle Package | Booking & Selection | 2 | 3 | yes |
| `GST-057` | Accessibility Information | Discovery & Browse | 2 | 1 | yes |
| `GST-058` | Resource Availability (Cabana) | Booking & Selection | 3 | 2 | yes |
| `GST-059` | Plan in Progress | Engagement & Support | 1 | 4 | yes |
| `GST-061` | Menu Item Detail | In-Venue Experience | 2 | 2 | yes |
| `GST-062` | Shop & Drop Collection | In-Venue Experience | 3 | 1 | yes |
| `GST-063` | Explore – Search Results | Discovery | 1 | 1 | yes |
| `GST-065` | Newsletter & Preferences | Marketing | 3 | 4 | yes |
| `GST-066` | Privacy & My Data | Account & Self-Service | 2 | 9 | yes |
| `GST-067` | Refunds & Resale | Account & Self-Service | 2 | 3 | yes |
| `GST-068` | Help & My Cases | Engagement & Support | 2 | 3 | yes |
| `GST-069` | Face Pass | Account & Self-Service | 2 | 4 | yes |
| `GST-070` | Reserve a Table | In-venue Services | 2 | 7 | yes |
| `GST-071` | Payment Methods | Account & Self-Service | 2 | 5 | yes |
| `GST-072` | Share & Group Booking | Booking & Selection | 2 | 8 | yes |
| `GST-073` | Security & Sign-in | Account & Self-Service | 2 | 14 | yes |
| `GST-074` | Map Booking — Cabanas & Spots | Booking & Selection | 3 | 8 | yes |
| `GST-075` | Book a Space by the Hour | Booking & Selection | 3 | 4 | yes |
| `GST-076` | Intercity Trip — Route & Schedule | Transport | 3 | 4 | yes |
| `GST-077` | Intercity Trip — Route & Passengers | Transport | 3 | 6 | yes |
| `GST-078` | Intercity Trip — Multi-trip Passes | Transport | 3 | 3 | yes |
| `GST-079` | Intercity Trip — Favourite Routes | Transport | 3 | 2 | yes |

