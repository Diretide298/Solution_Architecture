# P15 Kitchen Display — platform

**Derived.** `python3 tools/derive-platform.py P15`. App `kitchen-display` · venue · kiosk · offline-capable

| | |
|---|---|
| Screens | 10 |
| Operations | 24 |
| Contracts | 3 |
| Modules | 1 |
| Undrawn | 0 |
| Operations with no screen | 31 |
| Waves | wave2 10 |

## Gaps

### 31 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `attachModifierGroup` | fnb | PUT | Give an item its choices |
| `clearTable` | fnb | POST | Mark a table cleared and free |
| `closeCorrectiveAction` | fnb | POST | Close a signed finding |
| `createCombo` | fnb | POST | A meal deal, priced as one thing |
| `createModifierGroup` | fnb | POST | Create a modifier group |
| `createTable` | fnb | POST | A table as a thing, not an inference |
| `escalateCorrectiveAction` | fnb | POST | Escalate a finding |
| `getTableVisit` | fnb | GET | Read a visit with all its orders |
| `rebalanceStationLoad` | fnb | POST | Move work between stations mid-service |
| `recordCorrectiveAction` | fnb | POST | Record what was done about a finding |
| `requestBill` | fnb | POST | The party asked to pay |
| `resolveBookingConflict` | fnb | GET | Two bookings, one table — and what to do about it |
| `sendBookingConfirmation` | fnb | POST | Confirm a booking, and ask them to confirm back |
| `sendOrderNotification` | fnb | POST | Tell the guest where their order is |
| `setComboSlots` | fnb | PUT | What the guest chooses, and what it costs extra |
| `setKitchenSla` | fnb | PUT | How long a ticket may sit before it is late |
| `setSectionLayout` | fnb | PUT | Divide the floor into sections and give each a server |
| `updateTable` | fnb | PUT | Change what a table is |
| `cancelReportExecution` | reporting | DELETE | Cancel a running execution |
| `deleteReportSchedule` | reporting | DELETE | Delete a schedule |
| `exportReportResult` | reporting | POST | Export a completed result |
| `getReportExecution` | reporting | GET | Execution status and result |
| `getReportExport` | reporting | GET | Export status and download link |
| `getReportResult` | reporting | GET | Paged result rows |
| `listAlertRules` | reporting | GET | What raises an alert, and when |
| `listReportFields` | reporting | GET | Fields available for a data source |
| `listReportSchedules` | reporting | GET | List scheduled reports |
| `listSeededReports` | reporting | GET |  |
| `updateReportSchedule` | reporting | PATCH | Amend, pause or resume a schedule |
| `getRegionSettings` | tenancy | GET | Read region settings |
| `updateRegionSettings` | tenancy | PUT | Update region settings |

## Modules

| Module | Screens | Waves |
|---|---|---|
| Kitchen | 10 | 2 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `KIT-001` | Kitchen Operations Command Center | Kitchen | 2 | 3 | yes |
| `KIT-002` | Kitchen Display System (KDS) | Kitchen | 2 | 7 | yes |
| `KIT-003` | Order Firing & Course Management | Kitchen | 2 | 5 | yes |
| `KIT-004` | Active Order Management & Fulfilment Journey | Kitchen | 2 | 2 | yes |
| `KIT-005` | Kitchen Station Workload & Dynamic Routing | Kitchen | 2 | 2 | yes |
| `KIT-006` | Expeditor & Order Assembly | Kitchen | 2 | 5 | yes |
| `KIT-007` | Guest Collection, Buzzer & Digital Notification | Kitchen | 2 | 2 | yes |
| `KIT-008` | Exceptions, Re-Fire & Unavailable Items | Kitchen | 2 | 5 | yes |
| `KIT-009` | SLA, Priority & Service Rules | Kitchen | 2 | 2 | yes |
| `KIT-010` | Kitchen Performance, AI & Operational Optimization | Kitchen | 2 | 2 | yes |

