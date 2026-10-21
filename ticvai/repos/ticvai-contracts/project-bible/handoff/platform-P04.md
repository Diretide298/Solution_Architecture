# P04 Venue POS — platform

**Derived.** `python3 tools/derive-platform.py P04`. App `venue-pos` · venue · posTerminal · offline-capable

| | |
|---|---|
| Screens | 32 |
| Operations | 157 |
| Contracts | 18 |
| Modules | 4 |
| Undrawn | 0 |
| Operations with no screen | 168 |
| Waves | wave1 32 |

## Gaps

### 168 operations with no screen here

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
| `submitApprovalRequest` | approvals | POST | Send a saved draft, or a returned request, for approval |
| `acquireInventoryHold` | catalogue | POST | Acquire an inventory hold |
| `checkProductSalePermission` | catalogue | POST | Would this seller, here, be allowed to sell these products |
| `getBundleSigningKeys` | catalogue | GET | The public keys a till verifies catalogue bundles with |
| `getEventChangeTreatmentPolicy` | catalogue | GET | What happens to tickets, reservations and guests when an event changes, by default |
| `getPlanBenefits` | catalogue | GET | Which benefits a plan grants, and how much of each |
| `getProductChannelTexts` | catalogue | GET | The product's texts per sales channel, in each of the tenant's languages |
| `getProductDashboard` | catalogue | GET | The products dashboard's counts |
| `getProductOwnerForms` | catalogue | GET | Which form a sale of this product asks the buyer, and which it asks each ticket owner |
| `getProductSalePermissionRules` | catalogue | GET | Who can sell this product |
| `getWaitingRoomStatus` | catalogue | GET | A performance's waiting room, its setting and how it is moving |
| `listGuestMemberships` | catalogue | GET | A guest's memberships, benefits and history |
| `listMembershipBenefits` | catalogue | GET | Benefits a plan can grant |
| `listMembershipProgrammes` | catalogue | GET | Membership schemes, the level above a plan |
| `listOwnerFormCandidates` | catalogue | GET | The forms a product can link for its reservation owner or ticket owner |
| `listProductApprovalWorkflows` | catalogue | GET | The product approval workflows `approveWorkflow` saved |
| `listProductAttentionItems` | catalogue | GET | The products that need someone to act, and why |
| `listProductCategoryUsage` | catalogue | GET | How many products each category holds |
| `listProductTags` | catalogue | GET | The venue's tags, the master list products and promotions pick from |
| `listSalePermissionTargets` | catalogue | GET | What a sale permission rule can name at one level, with names |
| `listSeatPricingRules` | catalogue | GET | Seat-level dynamic pricing rules |
| `relinquishInventoryHold` | catalogue | DELETE | Return unsold units |
| `renewInventoryHold` | catalogue | POST | Extend an inventory hold's TTL |
| … | | | 128 more |

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
| `POS-003` | Sell — Timed Entry | Sell | 1 | 6 | yes |
| `POS-004` | Sell — Seat Map | Sell | 1 | 8 | yes |
| `POS-005` | Payment | Payment | 1 | 14 | yes |
| `POS-006` | Held Orders | Sell | 1 | 14 | yes |
| `POS-007` | Close Shift | Shift | 1 | 10 | yes |
| `POS-008` | Reports | Reports | 1 | 4 | yes |
| `POS-009` | Staff Roster | Shift | 1 | 3 | yes |
| `POS-010` | Add to Existing Ticket | Sell | 1 | 4 | yes |
| `POS-011` | Returns, Refunds & Exchanges | Sell | 1 | 8 | yes |
| `POS-012` | Omnichannel Order & Fulfilment Center | Sell | 1 | 6 | yes |
| `POS-013` | Mobile POS, Event Sales & Offline Operations | Sell | 1 | 3 | yes |
| `POS-014` | Sales Exceptions, Controls & Operational Actions | Sell | 1 | 4 | yes |
| `POS-015` | Cash Operations Dashboard | Sell | 1 | 2 | yes |
| `POS-016` | Till Configuration | Sell | 1 | 9 | yes |
| `POS-017` | Cash In / Cash Out Operations | Sell | 1 | 2 | yes |
| `POS-018` | Safe Drop & Cash Transfer Management | Sell | 1 | 3 | yes |
| `POS-019` | Shift Templates & Policies | Sell | 1 | 3 | yes |
| `POS-020` | Shift Exceptions & Alerts | Sell | 1 | 6 | yes |
| `POS-021` | Sell — Food & Drink | Sell | 1 | 5 | yes |
| `POS-022` | Send to Kitchen | Sell | 1 | 5 | yes |
| `POS-023` | Sell — Merchandise | Sell | 1 | 3 | yes |
| `POS-024` | Outlet Setup | Sell | 1 | 6 | yes |
| `POS-025` | Till Home | Sell | 1 | 8 | yes |
| `POS-026` | Receipt & Reprint | Sell | 1 | 8 | yes |
| `POS-027` | Guest Lookup | Sell | 1 | 5 | yes |
| `POS-028` | Table Service | Sell | 1 | 13 | yes |
| `POS-029` | Order Queue | Sell | 1 | 4 | yes |
| `POS-030` | Sales Journal | Sell | 1 | 8 | yes |
| `POS-031` | Reservations & Group Arrivals | Sell | 1 | 9 | yes |

