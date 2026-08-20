# P05 Guest Kiosk — platform

**Derived.** `python3 tools/derive-platform.py P05`. App `guest-app` · guest · kiosk

| | |
|---|---|
| Screens | 17 |
| Operations | 22 |
| Contracts | 8 |
| Modules | 2 |
| Undrawn | 3 |
| Operations with no screen | 23 |
| Waves | wave2 17 |

## Gaps

### 23 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `freezeEntitlement` | catalogue | POST | Pause a membership at the guest's request |
| `getMyMemberships` | catalogue | GET | A guest's own memberships, benefits and history |
| `listGuestMemberships` | catalogue | GET | A guest's memberships, benefits and history |
| `joinRestaurantWaitlist` | fnb | POST | Add a party to an outlet's waitlist |
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

### 3 screens nobody has drawn

- `KSK-015` Assistant — wave 2
- `KSK-016` Order Food — wave 2
- `KSK-017` Shop — wave 2

## Modules

| Module | Screens | Waves |
|---|---|---|
| Sell | 16 | 2 |
| AI | 1 | 2 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `KSK-001` | Attract Loop | Sell | 2 | 0 | yes |
| `KSK-002` | Language Select | Sell | 2 | 2 | yes |
| `KSK-003` | What are you buying | Sell | 2 | 1 | yes |
| `KSK-004` | Choose tickets | Sell | 2 | 2 | yes |
| `KSK-005` | Choose a session | Sell | 2 | 2 | yes |
| `KSK-006` | Review | Sell | 2 | 4 | yes |
| `KSK-007` | Payment | Sell | 2 | 1 | yes |
| `KSK-008` | Payment unresolved | Sell | 2 | 1 | yes |
| `KSK-009` | Ticket issued | Sell | 2 | 2 | yes |
| `KSK-010` | Print failure | Sell | 2 | 1 | yes |
| `KSK-011` | Collect a booking | Sell | 2 | 2 | yes |
| `KSK-012` | Booking found | Sell | 2 | 1 | yes |
| `KSK-013` | Call staff | Sell | 2 | 1 | yes |
| `KSK-014` | Out of service | Sell | 2 | 0 | yes |
| `KSK-015` | Assistant | AI | 2 | 4 | **no** |
| `KSK-016` | Order Food | Sell | 2 | 2 | **no** |
| `KSK-017` | Shop | Sell | 2 | 2 | **no** |

