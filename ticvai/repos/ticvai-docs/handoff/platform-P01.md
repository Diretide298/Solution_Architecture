# P01 Guest Web — platform

**Derived.** `python3 tools/derive-platform.py P01`. App `guest-web` · guest · web

| | |
|---|---|
| Screens | 50 |
| Operations | 204 |
| Contracts | 19 |
| Modules | 14 |
| Undrawn | 0 |
| Operations with no screen | 22 |
| Waves | wave1 50 |

## Gaps

### 22 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `getPlanBenefits` | catalogue | GET | Which benefits a plan grants, and how much of each |
| `listGuestMemberships` | catalogue | GET | A guest's memberships, benefits and history |
| `listMembershipBenefits` | catalogue | GET | Benefits a plan can grant |
| `listMembershipProgrammes` | catalogue | GET | Membership schemes, the level above a plan |
| `claimTableSession` | fnb | POST | Identify which table a guest is sitting at |
| `getMyIdentityVerification` | identity | GET | The guest's own latest identity verification |
| `listCustomerMemberships` | identity | GET | Memberships a customer holds |
| `submitGuestIdentityDocument` | identity | POST | Submit an identity document for verification |
| `checkGuestCheckoutMatch` | marketing-crm | POST | Does this contact already have a profile here |
| `decideGuestCheckoutMatch` | marketing-crm | POST | Use the existing profile or keep this booking separate |
| `getDeviceConsentHistory` | marketing-crm | GET | A visitor's own cookie decisions, oldest first |
| `listPublishedTrackingTechnologies` | marketing-crm | GET | The approved cookie registry, as the preference centre shows it |
| `recordDeviceConsent` | marketing-crm | POST | Record a visitor's cookie decision, before anyone is known |
| `uploadGuestDocument` | marketing-crm | POST | Store a guest photo, ID or signed document |
| `convertToTermProduct` | orders | POST | Turn a visit into a membership or season pass |
| `revokeEntitlementShare` | orders | POST | Take back a share |
| `revokePaymentToken` | orders | DELETE | Remove a saved payment method |
| `getCouponCode` | promotions | GET | Look up a code |
| `getRecommendations` | promotions | POST | What else this guest might want |
| `getUpsellSuggestions` | promotions | POST | Suggestions for a cart |
| `recordRecommendationOutcome` | promotions | POST | Shown, clicked, accepted or dismissed |
| `listMyWaitingGuests` | queue | GET | The caller's own queue entries |

## Modules

| Module | Screens | Waves |
|---|---|---|
| Booking & Selection | 7 | 1 |
| Engagement & Support | 6 | 1 |
| In-venue Services | 6 | 1 |
| Discovery & Browse | 5 | 1 |
| Cart & Checkout | 5 | 1 |
| Account & Self-Service | 5 | 1 |
| Membership, Loyalty & Value | 5 | 1 |
| Ticketing | 3 | 1 |
| Retail | 2 | 1 |
| Support | 2 | 1 |
| High-Demand Access | 1 | 1 |
| System States | 1 | 1 |
| Promotions | 1 | 1 |
| Transport | 1 | 1 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `WEB-001` | Home / Landing | Discovery & Browse | 1 | 7 | yes |
| `WEB-002` | Event & Attraction Listing | Discovery & Browse | 1 | 6 | yes |
| `WEB-003` | Search Results | Discovery & Browse | 1 | 2 | yes |
| `WEB-004` | Attraction Details | Discovery & Browse | 1 | 6 | yes |
| `WEB-005` | Ticket Type Selection | Booking & Selection | 1 | 7 | yes |
| `WEB-006` | Date & Performance Selection | Booking & Selection | 1 | 12 | yes |
| `WEB-007` | Interactive Seat Selection | Booking & Selection | 1 | 7 | yes |
| `WEB-008` | Add-ons & Upsell | Booking & Selection | 1 | 5 | yes |
| `WEB-009` | Wishlist | Booking & Selection | 1 | 3 | yes |
| `WEB-010` | Shopping Cart | Cart & Checkout | 1 | 14 | yes |
| `WEB-011` | Guest Details & Attendee Forms | Cart & Checkout | 1 | 7 | yes |
| `WEB-012` | Checkout — Payment | Cart & Checkout | 1 | 6 | yes |
| `WEB-013` | Booking Confirmation | Cart & Checkout | 1 | 5 | yes |
| `WEB-014` | Pay for a Booking | Cart & Checkout | 1 | 2 | yes |
| `WEB-015` | Branded Queue / Waiting Room | High-Demand Access | 1 | 2 | yes |
| `WEB-016` | Login / Register | Account & Self-Service | 1 | 14 | yes |
| `WEB-017` | My Account Dashboard | Account & Self-Service | 1 | 8 | yes |
| `WEB-018` | My Tickets | Account & Self-Service | 1 | 9 | yes |
| `WEB-019` | Order History | Account & Self-Service | 1 | 9 | yes |
| `WEB-020` | Profile & Preferences | Account & Self-Service | 1 | 7 | yes |
| `WEB-021` | Wallet & Gift Cards | Membership, Loyalty & Value | 1 | 9 | yes |
| `WEB-022` | Membership Plans | Membership, Loyalty & Value | 1 | 3 | yes |
| `WEB-023` | Membership Management | Membership, Loyalty & Value | 1 | 5 | yes |
| `WEB-024` | Devices, Wishlist & Consent | Membership, Loyalty & Value | 1 | 14 | yes |
| `WEB-025` | Help Centre / FAQ | Engagement & Support | 1 | 5 | yes |
| `WEB-026` | Survey & Feedback | Engagement & Support | 1 | 5 | yes |
| `WEB-027` | Newsletter Subscription | Engagement & Support | 1 | 5 | yes |
| `WEB-028` | Contact & Venue Information | Engagement & Support | 1 | 1 | yes |
| `WEB-029` | Error / Sold Out / Maintenance | System States | 1 | 2 | yes |
| `WEB-030` | Ticket Transfer | Ticketing | 1 | 4 | yes |
| `WEB-031` | My Reservations | Ticketing | 1 | 11 | yes |
| `WEB-032` | Offers & Promotions | Promotions | 1 | 2 | yes |
| `WEB-033` | Shop | Retail | 1 | 5 | yes |
| `WEB-034` | Lost & Found | Support | 1 | 4 | yes |
| `WEB-035` | Multi-Currency & Pricing | Ticketing | 1 | 2 | yes |
| `WEB-036` | F&B – Browse & Order | In-venue Services | 1 | 14 | yes |
| `WEB-037` | Menu Item Detail | In-venue Services | 1 | 1 | yes |
| `WEB-038` | F&B – Order Tracking | In-venue Services | 1 | 2 | yes |
| `WEB-039` | Venue Map & Wait Times | In-venue Services | 1 | 5 | yes |
| `WEB-040` | Virtual Queue | In-venue Services | 1 | 5 | yes |
| `WEB-041` | Parking – Reserve & Pay | In-venue Services | 1 | 4 | yes |
| `WEB-042` | Retail & Shop and Drop | Retail | 1 | 3 | yes |
| `WEB-043` | Loyalty & Rewards | Membership, Loyalty & Value | 1 | 9 | yes |
| `WEB-044` | AI Concierge – Home | Engagement & Support | 1 | 9 | yes |
| `WEB-045` | Help Centre & Accessibility | Support | 1 | 4 | yes |
| `WEB-046` | In-Venue Notifications | Engagement & Support | 1 | 2 | yes |
| `WEB-047` | Map Booking — Cabanas & Spots | Booking & Selection | 1 | 8 | yes |
| `WEB-048` | Book a Space by the Hour | Booking & Selection | 1 | 5 | yes |
| `WEB-049` | Transport — Route & Schedule | Transport | 1 | 12 | yes |
| `WEB-050` | Plan Your Visit | Discovery & Browse | 1 | 8 | yes |

