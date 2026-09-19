# P05 Guest Kiosk — platform

**Derived.** `python3 tools/derive-platform.py P05`. App `guest-app` · guest · kiosk

| | |
|---|---|
| Screens | 17 |
| Operations | 23 |
| Contracts | 8 |
| Modules | 2 |
| Undrawn | 0 |
| Operations with no screen | 1 |
| Waves | wave2 17 |

## Gaps

### 1 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `recordRecommendationOutcome` | promotions | POST | Shown, clicked, accepted or dismissed |

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
| `KSK-017` | Shop | Sell | 2 | 4 | yes |

