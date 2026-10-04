# P15 Kitchen Display — platform

**Derived.** `python3 tools/derive-platform.py P15`. App `kitchen-display` · venue · kiosk · offline-capable

| | |
|---|---|
| Screens | 10 |
| Operations | 27 |
| Contracts | 2 |
| Modules | 1 |
| Undrawn | 0 |
| Operations with no screen | 8 |
| Waves | wave1 10 |

## Gaps

### 8 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `createTable` | fnb | POST | A table as a thing, not an inference |
| `getPrepSheetTemplate` | fnb | GET | The venue's prep-sheet print template |
| `listFnbRecommendations` | fnb | GET | Upsell and pairing suggestions for F&B |
| `sendOrderNotification` | fnb | POST | Tell the guest where their order is |
| `setFnbReservationPolicy` | fnb | PUT | Set turn times and seating buffers |
| `setPrepSheetTemplate` | fnb | PUT | Set the prep-sheet print template |
| `updateTable` | fnb | PUT | Change what a table is |
| `listAlertRules` | reporting | GET | What raises an alert, and when |

## Modules

| Module | Screens | Waves |
|---|---|---|
| Kitchen | 10 | 1 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `KIT-001` | Kitchen Operations Command Center | Kitchen | 1 | 3 | yes |
| `KIT-002` | Kitchen Display System (KDS) | Kitchen | 1 | 5 | yes |
| `KIT-003` | Order Firing & Course Management | Kitchen | 1 | 5 | yes |
| `KIT-004` | Active Order Management & Fulfilment Journey | Kitchen | 1 | 2 | yes |
| `KIT-005` | Kitchen Station Workload & Dynamic Routing | Kitchen | 1 | 3 | yes |
| `KIT-006` | Expeditor & Order Assembly | Kitchen | 1 | 6 | yes |
| `KIT-007` | Guest Collection, Buzzer & Digital Notification | Kitchen | 1 | 1 | yes |
| `KIT-008` | Exceptions, Re-Fire & Unavailable Items | Kitchen | 1 | 5 | yes |
| `KIT-009` | SLA, Priority & Service Rules | Kitchen | 1 | 3 | yes |
| `KIT-010` | Kitchen Performance, AI & Operational Optimization | Kitchen | 1 | 4 | yes |

