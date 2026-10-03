# P04 Venue POS — platform

**Derived.** `python3 tools/derive-platform.py P04`. App `venue-pos` · venue · posTerminal · offline-capable

| | |
|---|---|
| Screens | 32 |
| Operations | 152 |
| Contracts | 19 |
| Modules | 4 |
| Undrawn | 0 |
| Operations with no screen | 153 |
| Waves | wave1 32 |

## Gaps

### 153 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `approveManualOverrideSupervisor` | access | PUT | Manual Override & Supervisor Approval |
| `getHardwareModelCertification` | access | GET | A reader model's certification and its test results |
| `listAccessChanges` | access | GET | Changes made to an entitlement's access |
| `listEntryExitRule` | access | GET | Entry, Exit & Re-entry Rules |
| `listEntryTemporaryExit` | access | GET | Re-entry & Temporary Exit Journey |
| `setHardwareModelCertification` | access | PUT | Certify a reader model, or record that it failed |
| `setVirtualTicketCredential` | access | PUT | Virtual Ticket & Credential 360° Workspace |
| `verifyIdentity` | access | POST | Check the person presenting against the person entitled |
| `approveMatrixMultiLevel` | approvals | PUT | Approval Matrix & Multi-Level Approval Configuration |
| `approveRoleAuthorityDelegation` | approvals | PUT | Roles, Authority, Delegation & Approval Limits |
| `approveUnifiedDecision` | approvals | PUT | Unified Approval Inbox & Decision Workspace |
| `assignApprovalRequest` | approvals | PUT | Assign, reassign or claim a request in a shared queue |
| `cancelApprovalRequest` | approvals | POST | An administrator cancels a request nobody should decide any more |
| `issueAccreditationBadge` | approvals | POST | Issue a badge |
| `listAccreditationBadges` | approvals | GET | Badges issued and their state |
| `listAutomationExecutions` | approvals | GET | What automations ran, when, on whose rule, and the outcome |
| `reopenApprovalRequest` | approvals | POST | Reopen an expired or cancelled request as a new one |
| `submitApprovalRequest` | approvals | POST | Send a saved draft for approval |
| `getEventChangeTreatmentPolicy` | catalogue | GET | What happens to tickets, reservations and guests when an event changes, by default |
| `getPlanBenefits` | catalogue | GET | Which benefits a plan grants, and how much of each |
| `getWaitingRoomStatus` | catalogue | GET | A performance's waiting room, its setting and how it is moving |
| `listGuestMemberships` | catalogue | GET | A guest's memberships, benefits and history |
| `listMembershipBenefits` | catalogue | GET | Benefits a plan can grant |
| `listMembershipProgrammes` | catalogue | GET | Membership schemes, the level above a plan |
| `listProductApprovalWorkflows` | catalogue | GET | The product approval workflows `approveWorkflow` saved |
| `listSeatPricingRules` | catalogue | GET | Seat-level dynamic pricing rules |
| `relinquishInventoryHold` | catalogue | DELETE | Return unsold units |
| `renewInventoryHold` | catalogue | POST | Extend a lease TTL |
| `setEntitlementTemplateBlackoutDates` | catalogue | PUT | Set the dates a product's entitlement does not admit |
| `setEventChangeTreatmentPolicy` | catalogue | PUT | Set the default treatment per kind of event change |
| `setSeatPricingRule` | catalogue | PUT | Create or replace a seat-level dynamic pricing rule |
| `setWaitingRoomSetting` | catalogue | PUT | Switch a performance's waiting room on or off, and set how fast it releases |
| `calculateTax` | finance | POST | Compute tax for a set of lines |
| `disputeObligation` | finance | POST | One entity disagrees with the amount |
| `getForeignTenderReport` | finance | GET | What was taken in which currency |
| `listInterEntityObligations` | finance | GET | What one entity owes another |
| `recordWriteOff` | finance | POST | Write off an uncollectable balance |
| `resolveObligationDispute` | finance | POST | Agree what is actually owed |
| `runFxRevaluation` | finance | POST | Revalue monetary balances at close |
| `setFxProvider` | finance | PUT | Which provider serves which purpose |
| … | | | 113 more |

## Modules

| Module | Screens | Waves |
|---|---|---|
| Sell | 26 | 1 |
| Shift | 4 | 1 |
| Payment | 1 | 1 |
| Reports | 1 | 1 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `POS-000` | Sign In | Shift | 1 | 8 | yes |
| `POS-001` | Begin Shift | Shift | 1 | 7 | yes |
| `POS-002` | Sell — Ticket Catalogue | Sell | 1 | 32 | yes |
| `POS-003` | Sell — Timed Entry | Sell | 1 | 8 | yes |
| `POS-004` | Sell — Seat Map | Sell | 1 | 7 | yes |
| `POS-005` | Payment | Payment | 1 | 13 | yes |
| `POS-006` | Held Orders | Sell | 1 | 14 | yes |
| `POS-007` | Close Shift | Shift | 1 | 8 | yes |
| `POS-008` | Reports | Reports | 1 | 4 | yes |
| `POS-009` | Staff Roster | Shift | 1 | 3 | yes |
| `POS-010` | Add to Existing Ticket | Sell | 1 | 5 | yes |
| `POS-011` | Returns, Refunds & Exchanges | Sell | 1 | 7 | yes |
| `POS-012` | Omnichannel Order & Fulfilment Center | Sell | 1 | 6 | yes |
| `POS-013` | Mobile POS, Event Sales & Offline Operations | Sell | 1 | 3 | yes |
| `POS-014` | Sales Exceptions, Controls & Operational Actions | Sell | 1 | 4 | yes |
| `POS-015` | Cash Operations Dashboard | Sell | 1 | 2 | yes |
| `POS-016` | Till Configuration | Sell | 1 | 5 | yes |
| `POS-017` | Cash In / Cash Out Operations | Sell | 1 | 2 | yes |
| `POS-018` | Safe Drop & Cash Transfer Management | Sell | 1 | 3 | yes |
| `POS-019` | Shift Templates & Policies | Sell | 1 | 3 | yes |
| `POS-020` | Shift Exceptions & Alerts | Sell | 1 | 5 | yes |
| `POS-021` | Sell — Food & Drink | Sell | 1 | 4 | yes |
| `POS-022` | Send to Kitchen | Sell | 1 | 5 | yes |
| `POS-023` | Sell — Merchandise | Sell | 1 | 4 | yes |
| `POS-024` | Outlet Setup | Sell | 1 | 5 | yes |
| `POS-025` | Till Home | Sell | 1 | 7 | yes |
| `POS-026` | Receipt & Reprint | Sell | 1 | 6 | yes |
| `POS-027` | Guest Lookup | Sell | 1 | 5 | yes |
| `POS-028` | Table Service | Sell | 1 | 13 | yes |
| `POS-029` | Order Queue | Sell | 1 | 1 | yes |
| `POS-030` | Sales Journal | Sell | 1 | 8 | yes |
| `POS-031` | Reservations & Group Arrivals | Sell | 1 | 9 | yes |

