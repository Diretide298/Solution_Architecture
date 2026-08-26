# P05 Guest Kiosk — platform

**Derived.** `python3 tools/derive-platform.py P05`. App `guest-app` · guest · kiosk

| | |
|---|---|
| Screens | 17 |
| Operations | 22 |
| Contracts | 8 |
| Modules | 2 |
| Undrawn | 0 |
| Operations with no screen | 18 |
| Waves | wave2 17 |

## Gaps

### 18 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `freezeEntitlement` | catalogue | POST | Pause a membership at the guest's request |
| `listGuestMemberships` | catalogue | GET | A guest's memberships, benefits and history |
| `createReferral` | marketing-crm | POST | Issue a referral code |
| `getMyChallenges` | marketing-crm | GET | Active challenges and how far along I am |
| `getWaiverStatus` | marketing-crm | GET | Whether this guest may be issued a ticket that requires a waiver |
| `recordLostItem` | marketing-crm | POST | Report something lost, or hand something in |
| `respondToInvitation` | marketing-crm | POST | Accept or decline |
| `submitForm` | marketing-crm | POST | Sign a waiver, answer a survey, capture details |
| `updateGuestPreferences` | marketing-crm | PUT | The things a regular should not have to say twice |
| `uploadGuestDocument` | marketing-crm | POST | Store a guest photo, ID or signed document |
| `convertToTermProduct` | orders | POST | Turn a visit into a membership or season pass |
| `createResaleListing` | orders | POST | List an entitlement for resale |
| `getGroupBooking` | orders | GET |  |
| `listPaymentTokens` | orders | GET | A guest's saved payment methods |
| `quoteUpgrade` | orders | POST | What an upgrade costs, pro-rata |
| `shareEntitlement` | orders | POST | Let somebody else use this, without giving it away |
| `storePaymentToken` | orders | POST | Save a payment method for future use |
| `transferWalletBalance` | retail | POST | Send balance to another guest |

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
| `KSK-015` | Assistant | AI | 2 | 4 | yes |
| `KSK-016` | Order Food | Sell | 2 | 2 | yes |
| `KSK-017` | Shop | Sell | 2 | 2 | yes |

