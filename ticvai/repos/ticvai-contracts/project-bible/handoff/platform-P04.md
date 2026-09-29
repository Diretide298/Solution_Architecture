# P04 Venue POS — platform

**Derived.** `python3 tools/derive-platform.py P04`. App `venue-pos` · venue · posTerminal · offline-capable

| | |
|---|---|
| Screens | 30 |
| Operations | 144 |
| Contracts | 20 |
| Modules | 4 |
| Undrawn | 0 |
| Operations with no screen | 153 |
| Waves | wave1 27 · wave2 3 |

## Gaps

### 153 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `approveManualOverrideSupervisor` | access | PUT | Manual Override & Supervisor Approval |
| `listAccessChanges` | access | GET | Changes made to an entitlement's access |
| `listEntryRulePoints` | access | GET | Which access points an admission rule covers |
| `verifyIdentity` | access | POST | Check the person presenting against the person entitled |
| `approveMatrixMultiLevel` | approvals | PUT | Approval Matrix & Multi-Level Approval Configuration |
| `approveRoleAuthorityDelegation` | approvals | PUT | Roles, Authority, Delegation & Approval Limits |
| `approveUnifiedDecision` | approvals | PUT | Unified Approval Inbox & Decision Workspace |
| `issueAccreditationBadge` | approvals | POST | Issue a badge |
| `listAccreditationBadges` | approvals | GET | Badges issued and their state |
| `submitApprovalRequest` | approvals | POST | Send a saved draft for approval |
| `getCatalogueImportJob` | catalogue | GET | Progress and findings of a catalogue import |
| `getPlanBenefits` | catalogue | GET | Which benefits a plan grants, and how much of each |
| `listMembershipBenefits` | catalogue | GET | Benefits a plan can grant |
| `listMembershipProgrammes` | catalogue | GET | Membership schemes, the level above a plan |
| `calculateTax` | finance | POST | Compute tax for a set of lines |
| `disputeObligation` | finance | POST | One entity disagrees with the amount |
| `getForeignTenderReport` | finance | GET | What was taken in which currency |
| `listInterEntityObligations` | finance | GET | What one entity owes another |
| `recordWriteOff` | finance | POST | Write off an uncollectable balance |
| `resolveObligationDispute` | finance | POST | Agree what is actually owed |
| `runFxRevaluation` | finance | POST | Revalue monetary balances at close |
| `setFxProvider` | finance | PUT | Which provider serves which purpose |
| `getAllergenVerification` | fnb | GET | The last allergen verdict recorded for a dish |
| `getFnbReservationPolicy` | fnb | GET | How long a table is held, by party size |
| `getFnbServiceChargePolicy` | fnb | GET | The service charge a venue applies, and on what |
| `listFnbRecommendations` | fnb | GET | Upsell and pairing suggestions for F&B |
| `listIngredientSubstitutes` | fnb | GET | Approved substitutions for a recipe's ingredients |
| `listMenuSchedules` | fnb | GET | What is scheduled to go live, and when |
| `listMenuVersions` | fnb | GET | Every published version of a menu |
| `listTemperatureCheckpoints` | fnb | GET | The units that get read, and the range each must hold |
| `resolveBookingConflict` | fnb | GET | Two bookings, one table — and what to do about it |
| `sendBookingConfirmation` | fnb | POST | Confirm a booking, and ask them to confirm back |
| `sendOrderNotification` | fnb | POST | Tell the guest where their order is |
| `evaluateAccess` | identity | POST | Decide, now, and say why |
| `getAccessPolicy` | identity | GET | One policy, at a version |
| `getAccessPolicyBundle` | identity | GET | The policies a device needs to decide for itself |
| `getMembership` | identity | GET | A membership with its history, usage and renewals |
| `getPasswordPolicy` | identity | GET | Read the password and MFA policy in force |
| `getPrincipalModuleAccess` | identity | GET | What this person may do, as ticks |
| `listAccessDecisions` | identity | GET | What was decided, for whom, where and why |
| … | | | 113 more |

### 2 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Sell** — waves 1, 2
- **Shift** — waves 1, 2

## Modules

| Module | Screens | Waves |
|---|---|---|
| Sell | 24 | 1, 2 |
| Shift | 4 | 1, 2 |
| Payment | 1 | 1 |
| Reports | 1 | 2 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `POS-000` | Sign In | Shift | 1 | 8 | yes |
| `POS-001` | Begin Shift | Shift | 1 | 17 | yes |
| `POS-002` | Sell — Ticket Catalogue | Sell | 1 | 42 | yes |
| `POS-003` | Sell — Timed Entry | Sell | 1 | 10 | yes |
| `POS-004` | Sell — Seat Map | Sell | 2 | 11 | yes |
| `POS-005` | Payment | Payment | 1 | 12 | yes |
| `POS-006` | Held Orders | Sell | 1 | 14 | yes |
| `POS-007` | Close Shift | Shift | 1 | 17 | yes |
| `POS-008` | Reports | Reports | 2 | 7 | yes |
| `POS-009` | Staff Roster | Shift | 2 | 16 | yes |
| `POS-010` | Add to Existing Ticket | Sell | 1 | 5 | yes |
| `POS-011` | Returns, Refunds & Exchanges | Sell | 1 | 9 | yes |
| `POS-012` | Omnichannel Order & Fulfilment Center | Sell | 1 | 7 | yes |
| `POS-013` | Mobile POS, Event Sales & Offline Operations | Sell | 1 | 8 | yes |
| `POS-014` | Sales Exceptions, Controls & Operational Actions | Sell | 1 | 3 | yes |
| `POS-015` | Cash Operations Dashboard | Sell | 1 | 2 | yes |
| `POS-016` | Till Configuration | Sell | 1 | 5 | yes |
| `POS-017` | Cash In / Cash Out Operations | Sell | 1 | 1 | yes |
| `POS-018` | Safe Drop & Cash Transfer Management | Sell | 1 | 5 | yes |
| `POS-019` | Shift Templates & Policies | Sell | 1 | 3 | yes |
| `POS-020` | Shift Exceptions & Alerts | Sell | 1 | 5 | yes |
| `POS-021` | Sell — Food & Drink | Sell | 1 | 6 | yes |
| `POS-022` | Send to Kitchen | Sell | 1 | 4 | yes |
| `POS-023` | Sell — Merchandise | Sell | 1 | 5 | yes |
| `POS-024` | Outlet Setup | Sell | 1 | 5 | yes |
| `POS-025` | Till Home | Sell | 1 | 5 | yes |
| `POS-026` | Receipt & Reprint | Sell | 1 | 3 | yes |
| `POS-027` | Guest Lookup | Sell | 1 | 2 | yes |
| `POS-028` | Table Service | Sell | 1 | 8 | yes |
| `POS-029` | Order Queue | Sell | 1 | 4 | yes |

