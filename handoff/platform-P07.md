# P07 Venue Scanner — platform

**Derived.** `python3 tools/derive-platform.py P07`. App `venue-scanner` · venue · handheld · offline-capable

| | |
|---|---|
| Screens | 16 |
| Operations | 40 |
| Contracts | 5 |
| Modules | 3 |
| Undrawn | 0 |
| Operations with no screen | 28 |
| Waves | wave1 16 |

## Gaps

### 28 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `enrolFacePass` | access | POST | Register a facial profile against an entitlement |
| `getFacePassEnrolment` | access | GET | Whether a pass has a face registered, and when |
| `revokeFacePass` | access | DELETE | Remove a facial profile |
| `authoriseWalletSpend` | cross-cell | POST | Hold funds against the guest's home-cell balance |
| `captureWalletAuthorisation` | cross-cell | POST | Capture a held amount |
| `createDsarRequest` | cross-cell | POST | Raise a data subject request across every linked cell |
| `createGuestLink` | cross-cell | POST | Link a guest's records across cells |
| `getDsarRequest` | cross-cell | GET | Track fan-out progress per cell |
| `getWalletAllocation` | cross-cell | GET | The consuming cell's bounded offline allocation |
| `releaseWalletAuthorisation` | cross-cell | POST | Release a hold without capturing |
| `resolveGuestLink` | cross-cell | GET | Find the link for a local subject |
| `revokeGuestLink` | cross-cell | DELETE | Sever a link on consent withdrawal |
| `revokeRedemptionRight` | cross-cell | DELETE | Revoke a right |
| `setWalletAllocationPolicy` | cross-cell | PUT | Set the allocation cap policy |
| `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| `deleteGuestAccount` | identity | DELETE | Self-service account deletion |
| `resolvePermissions` | identity | POST | Simulate a principal's effective permissions |
| `convertReservation` | orders | POST | Convert a reservation into an order |
| `createCart` | orders | POST | Start a cart |
| `createReservation` | orders | POST | Hold without payment |
| `extendReservation` | orders | POST | Extend a reservation |
| `listAbandonedCarts` | orders | GET | Carts that lapsed without checking out |
| `voidPayment` | orders | POST | Release an authorisation before it is captured |
| `adjustDepositBoxFloat` | shift | POST | Change the initial fund |
| `allocateDepositBox` | shift | POST | Give a cashier a box and a float |
| `closeDepositBoxes` | shift | POST | Close one box or all of them |
| `listDepositBoxes` | shift | GET | Cash boxes and who holds them |
| `withdrawFromDepositBox` | shift | POST | A supervisor takes cash out mid-shift |

## Modules

| Module | Screens | Waves |
|---|---|---|
| access | 14 | 1 |
| shift | 1 | 1 |
| cross-cell | 1 | 1 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `SCN-001` | Sign in | shift | 1 | 20 | yes |
| `SCN-002` | Access point & direction | access | 1 | 6 | yes |
| `SCN-003` | Ready to scan | access | 1 | 7 | yes |
| `SCN-004` | Admitted | access | 1 | 8 | yes |
| `SCN-005` | Denied | access | 1 | 7 | yes |
| `SCN-006` | Override | access | 1 | 7 | yes |
| `SCN-007` | Group admission | access | 1 | 7 | yes |
| `SCN-008` | Manual entry | access | 1 | 7 | yes |
| `SCN-009` | Ticket lookup | access | 1 | 7 | yes |
| `SCN-010` | Blacklisted | access | 1 | 3 | yes |
| `SCN-011` | Delegated right | cross-cell | 1 | 2 | yes |
| `SCN-012` | Offline scanning | access | 1 | 7 | yes |
| `SCN-013` | Offline journal | access | 1 | 7 | yes |
| `SCN-014` | Sync & reconciliation | access | 1 | 9 | yes |
| `SCN-015` | Offline package | access | 1 | 7 | yes |
| `SCN-016` | Gate mode | access | 1 | 6 | yes |

