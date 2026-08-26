# P07 Venue Scanner — platform

**Derived.** `python3 tools/derive-platform.py P07`. App `venue-scanner` · venue · handheld · offline-capable

| | |
|---|---|
| Screens | 11 |
| Operations | 23 |
| Contracts | 5 |
| Modules | 1 |
| Undrawn | 0 |
| Operations with no screen | 48 |
| Waves | wave1 11 |

## Gaps

### 48 operations with no screen here

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
| `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| `setPasswordPolicy` | identity | PUT | Length, breach check, lockout and step-up |
| `setSegregationRules` | identity | PUT | Which permissions may not be held together |
| `captureStoredValue` | orders | POST | Take some or all of a held balance |
| `convertReservation` | orders | POST | Convert a reservation into an order |
| `convertToTermProduct` | orders | POST | Turn a visit into a membership or season pass |
| `createCart` | orders | POST | Start a cart |
| `createPaymentLink` | orders | POST | Send a guest a link to pay later |
| `createResaleListing` | orders | POST | List an entitlement for resale |
| `createReservation` | orders | POST | Hold without payment |
| `extendReservation` | orders | POST | Extend a reservation |
| `getGroupBooking` | orders | GET |  |
| `issueInvitation` | orders | POST | Issue a complimentary entitlement, with no payment expected |
| `listAbandonedCarts` | orders | GET | Carts that lapsed without checking out |
| `listChargebacks` | orders | GET | Open disputes, by deadline |
| `listFraudRules` | orders | GET |  |
| `listInvitationAllowances` | orders | GET | Who may issue comps, and how many are left |
| `listPaymentProviders` | orders | GET | Gateways configured for this scope |
| `listPaymentTokens` | orders | GET | A guest's saved payment methods |
| `openGuestCreditAccount` | orders | POST | A credit limit for an individual booking ahead |
| `printTicketProof` | orders | POST | Print a sample without selling anything |
| `pushWalletPassUpdate` | orders | POST | Push a change to every device holding it |
| `quoteUpgrade` | orders | POST | What an upgrade costs, pro-rata |
| `reissueEntitlement` | orders | POST | Zero-value reissue of an expired entitlement for a later date |
| … | | | 8 more |

## Modules

| Module | Screens | Waves |
|---|---|---|
| Access | 11 | 1 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `SCN-001` | Sign in | Access | 1 | 8 | yes |
| `SCN-002` | Access point & direction | Access | 1 | 3 | yes |
| `SCN-003` | Ready to scan | Access | 1 | 9 | yes |
| `SCN-007` | Group admission | Access | 1 | 7 | yes |
| `SCN-008` | Manual entry | Access | 1 | 7 | yes |
| `SCN-009` | Ticket lookup | Access | 1 | 7 | yes |
| `SCN-011` | Delegated right | Access | 1 | 2 | yes |
| `SCN-013` | Offline journal | Access | 1 | 7 | yes |
| `SCN-014` | Sync & reconciliation | Access | 1 | 9 | yes |
| `SCN-015` | Offline package | Access | 1 | 7 | yes |
| `SCN-016` | Gate mode | Access | 1 | 3 | yes |

