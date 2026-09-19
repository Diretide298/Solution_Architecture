# P15 Kitchen Display — platform

**Derived.** `python3 tools/derive-platform.py P15`. App `kitchen-display` · venue · kiosk · offline-capable

| | |
|---|---|
| Screens | 10 |
| Operations | 24 |
| Contracts | 3 |
| Modules | 1 |
| Undrawn | 0 |
| Operations with no screen | 26 |
| Waves | wave2 10 |

## Gaps

### 26 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `attachModifierGroup` | fnb | PUT | Give an item its choices |
| `closeCorrectiveAction` | fnb | POST | Close a signed finding |
| `createCombo` | fnb | POST | A meal deal, priced as one thing |
| `createModifierGroup` | fnb | POST | Create a modifier group |
| `createTable` | fnb | POST | A table as a thing, not an inference |
| `escalateCorrectiveAction` | fnb | POST | Escalate a finding |
| `rebalanceStationLoad` | fnb | POST | Move work between stations mid-service |
| `recordCorrectiveAction` | fnb | POST | Record what was done about a finding |
| `resolveBookingConflict` | fnb | GET | Two bookings, one table — and what to do about it |
| `sendBookingConfirmation` | fnb | POST | Confirm a booking, and ask them to confirm back |
| `sendOrderNotification` | fnb | POST | Tell the guest where their order is |
| `setComboSlots` | fnb | PUT | What the guest chooses, and what it costs extra |
| `setKitchenSla` | fnb | PUT | How long a ticket may sit before it is late |
| `setSectionLayout` | fnb | PUT | Divide the floor into sections and give each a server |
| `updateTable` | fnb | PUT | Change what a table is |
| `deleteReportSchedule` | reporting | DELETE | Delete a schedule |
| `listAlertRules` | reporting | GET | What raises an alert, and when |
| `updateReportSchedule` | reporting | PATCH | Amend, pause or resume a schedule |
| `issueDeviceCredential` | tenancy | POST | Give the device an identity it can prove |
| `listDeviceAuditRecords` | tenancy | GET | What was done to this device, and what it did |
| `listDeviceFirmware` | tenancy | GET | Firmware and software versions, and what is running where |
| `listDeviceTamperEvents` | tenancy | GET | Devices that report having been interfered with |
| `recordDeviceTamperEvent` | tenancy | POST | A device reports interference |
| `revokeDeviceCredential` | tenancy | DELETE | Cut a device off now |
| `rollbackDeviceFirmware` | tenancy | POST | Put the fleet back on the previous version |
| `startDeviceFirmwareRollout` | tenancy | POST | Push an update to a fleet, in waves |

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

