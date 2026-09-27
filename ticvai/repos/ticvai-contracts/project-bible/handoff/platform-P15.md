# P15 Kitchen Display — platform

**Derived.** `python3 tools/derive-platform.py P15`. App `kitchen-display` · venue · kiosk · offline-capable

| | |
|---|---|
| Screens | 10 |
| Operations | 24 |
| Contracts | 3 |
| Modules | 1 |
| Undrawn | 0 |
| Operations with no screen | 46 |
| Waves | wave2 10 |

## Gaps

### 46 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `attachModifierGroup` | fnb | PUT | Give an item its choices |
| `closeCorrectiveAction` | fnb | POST | Close a signed finding |
| `createCombo` | fnb | POST | A meal deal, priced as one thing |
| `createModifierGroup` | fnb | POST | Create a modifier group |
| `createTable` | fnb | POST | A table as a thing, not an inference |
| `escalateCorrectiveAction` | fnb | POST | Escalate a finding |
| `getFnbReservationPolicy` | fnb | GET | How long a table is held, by party size |
| `getFnbServiceChargePolicy` | fnb | GET | The service charge a venue applies, and on what |
| `listFnbRecommendations` | fnb | GET | Upsell and pairing suggestions for F&B |
| `listIngredientSubstitutes` | fnb | GET | Approved substitutions for a recipe's ingredients |
| `listMenuSchedules` | fnb | GET | What is scheduled to go live, and when |
| `listMenuVersions` | fnb | GET | Every published version of a menu |
| `listTemperatureCheckpoints` | fnb | GET | The units that get read, and the range each must hold |
| `rebalanceStationLoad` | fnb | POST | Move work between stations mid-service |
| `recordCorrectiveAction` | fnb | POST | Record what was done about a finding |
| `resolveBookingConflict` | fnb | GET | Two bookings, one table — and what to do about it |
| `sendBookingConfirmation` | fnb | POST | Confirm a booking, and ask them to confirm back |
| `sendOrderNotification` | fnb | POST | Tell the guest where their order is |
| `setComboSlots` | fnb | PUT | What the guest chooses, and what it costs extra |
| `setFnbReservationPolicy` | fnb | PUT | Set turn times and seating buffers |
| `setFnbServiceChargePolicy` | fnb | PUT | Set the service charge |
| `setIngredientSubstitutes` | fnb | PUT | Define approved substitutions |
| `setKitchenSla` | fnb | PUT | How long a ticket may sit before it is late |
| `setSectionLayout` | fnb | PUT | Divide the floor into sections and give each a server |
| `setTemperatureCheckpoint` | fnb | PUT | Define a checkpoint and its safe range |
| `updateTable` | fnb | PUT | Change what a table is |
| `deleteDashboard` | reporting | DELETE | Archive a dashboard |
| `deleteReportSchedule` | reporting | DELETE | Delete a schedule |
| `listAlertRules` | reporting | GET | What raises an alert, and when |
| `updateReportSchedule` | reporting | PATCH | Amend, pause or resume a schedule |
| `getConfigurationProfile` | tenancy | GET | One profile, at its latest version or at a named one |
| `getConnectivityPolicy` | tenancy | GET | The connectivity thresholds saved at one scope node |
| `getDevice` | tenancy | GET | Read one registered device |
| `getOfflinePolicy` | tenancy | GET | The offline policy saved at one scope node |
| `getOutlet` | tenancy | GET | Read an outlet |
| `issueDeviceCredential` | tenancy | POST | Give the device an identity it can prove |
| `listCellEndpoints` | tenancy | GET | Where each service answers inside a cell |
| `listConfigurationProfiles` | tenancy | GET | Every configuration profile, at its current version |
| `listDeviceAuditRecords` | tenancy | GET | What was done to this device, and what it did |
| `listDeviceFirmware` | tenancy | GET | Firmware and software versions, and what is running where |
| … | | | 6 more |

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

