# P07 Venue Scanner — platform

**Derived.** `python3 tools/derive-platform.py P07`. App `venue-scanner` · venue · handheld · offline-capable

| | |
|---|---|
| Screens | 11 |
| Operations | 22 |
| Contracts | 5 |
| Modules | 1 |
| Undrawn | 0 |
| Operations with no screen | 53 |
| Waves | wave1 11 |

## Gaps

### 53 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `enrolFaceTag` | access | POST | Capture a same-visit facial model that dies at close of day |
| `listAccessChanges` | access | GET | Changes made to an entitlement's access |
| `listEntryRulePoints` | access | GET | Which access points an admission rule covers |
| `setEntryRulePoints` | access | PUT | Set the access points an admission rule covers |
| `verifyIdentity` | access | POST | Check the person presenting against the person entitled |
| `authoriseWalletSpend` | cross-region | POST | Hold funds against the guest's home-cell balance |
| `captureWalletAuthorisation` | cross-region | POST | Capture a held amount |
| `getWalletAllocation` | cross-region | GET | The consuming cell's bounded offline allocation |
| `listCellConnections` | cross-region | GET | Which cells may talk to which |
| `listCrossCellRequests` | cross-region | GET | Calls that had to leave a cell |
| `relinquishWalletAuthorisation` | cross-region | POST | Release a hold without capturing |
| `setWalletAllocationPolicy` | cross-region | PUT | Set the allocation cap policy |
| `createEmergencyAccessOverride` | identity | POST | Bypass the policy, loudly |
| `evaluateAccess` | identity | POST | Decide, now, and say why |
| `getAccessPolicy` | identity | GET | One policy, at a version |
| `getAccessPolicyBundle` | identity | GET | The policies a device needs to decide for itself |
| `getMembership` | identity | GET | A membership with its history, usage and renewals |
| `getPrincipalModuleAccess` | identity | GET | What this person may do, as ticks |
| `listAccessDecisions` | identity | GET | What was decided, for whom, where and why |
| `listAccessPolicyHistory` | identity | GET | Every version, who changed it and why |
| `listAccessPolicyTemplates` | identity | GET | Reusable policy shapes |
| `listCapabilityTemplates` | identity | GET | Saved tick-sets |
| `listCustomerMemberships` | identity | GET | Memberships a customer holds |
| `listModuleCapabilities` | identity | GET | What a person can be allowed to do, per module |
| `listModules` | identity | GET | The module tree permissions are grouped under |
| `listPermissions` | identity | GET | Every permission key the contracts enforce |
| `listSegregationRules` | identity | GET | Read the conflicting-permission rules back |
| `listSegregationViolations` | identity | GET | Who already holds a conflicting pair |
| `recordBenefitUsage` | identity | POST | Consume a benefit |
| `setAccessPolicyState` | identity | POST | Submit, approve, activate or retire a policy |
| `setCapabilityTemplate` | identity | PUT | Save a tick-set under a name |
| `setPrincipalModuleAccess` | identity | PUT | Tick what they may do |
| `updateAccessPolicy` | identity | PUT | Change a policy, as a new version |
| `convertReservation` | orders | POST | Convert a reservation into an order |
| `convertToTermProduct` | orders | POST | Turn a visit into a membership or season pass |
| `createReservation` | orders | POST | Hold without payment |
| `extendReservation` | orders | POST | Extend a reservation |
| `getBillingStatement` | orders | GET | One statement, with its lines |
| `issueInvitation` | orders | POST | Issue a complimentary entitlement, with no payment expected |
| `listBillingStatements` | orders | GET | What was charged, when, and against which agreement |
| … | | | 13 more |

## Modules

| Module | Screens | Waves |
|---|---|---|
| Access | 11 | 1 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `SCN-001` | Sign in | Access | 1 | 7 | yes |
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

