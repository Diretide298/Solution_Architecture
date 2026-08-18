# P05 Guest Kiosk — platform

**Derived.** `python3 tools/derive-platform.py P05`. App `guest-app` · guest · kiosk

| | |
|---|---|
| Screens | 15 |
| Operations | 18 |
| Contracts | 7 |
| Modules | 6 |
| Undrawn | 1 |
| Operations with no screen | 0 |
| Waves | wave2 15 |

## Gaps

### 1 screens nobody has drawn

- `KSK-015` Assistant — wave 2

## Modules

| Module | Screens | Waves |
|---|---|---|
| orders | 6 | 2 |
| catalogue | 4 | 2 |
| Sell | 2 | 2 |
| white-label | 1 | 2 |
| retail | 1 | 2 |
| marketing-crm | 1 | 2 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `KSK-001` | Attract Loop | Sell | 2 | 0 | yes |
| `KSK-002` | Language Select | white-label | 2 | 2 | yes |
| `KSK-003` | What are you buying | catalogue | 2 | 1 | yes |
| `KSK-004` | Choose tickets | catalogue | 2 | 2 | yes |
| `KSK-005` | Choose a session | catalogue | 2 | 2 | yes |
| `KSK-006` | Review | orders | 2 | 4 | yes |
| `KSK-007` | Payment | orders | 2 | 1 | yes |
| `KSK-008` | Payment unresolved | orders | 2 | 1 | yes |
| `KSK-009` | Ticket issued | orders | 2 | 2 | yes |
| `KSK-010` | Print failure | orders | 2 | 1 | yes |
| `KSK-011` | Collect a booking | retail | 2 | 2 | yes |
| `KSK-012` | Booking found | orders | 2 | 1 | yes |
| `KSK-013` | Call staff | marketing-crm | 2 | 1 | yes |
| `KSK-014` | Out of service | Sell | 2 | 0 | yes |
| `KSK-015` | Assistant | catalogue | 2 | 4 | **no** |

