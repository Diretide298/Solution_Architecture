# P06 Venue Staff App — platform

**Derived.** `python3 tools/derive-platform.py P06`. App `venue-staff-app` · venue · mobileApp · offline-capable

| | |
|---|---|
| Screens | 96 |
| Operations | 222 |
| Contracts | 21 |
| Modules | 4 |
| Undrawn | 0 |
| Operations with no screen | 139 |
| Waves | wave1 30 · wave2 35 · wave3 31 |

## Gaps

### 139 operations with no screen here

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
| `createKnowledgeCollection` | ai | POST | Create a collection |
| `generateVenueLayout` | ai | POST | Draft a seat map from an uploaded plan |
| `listIndexJobs` | ai | GET | Indexing in flight and recently finished |
| `listIndexSources` | ai | GET | What is indexed, and how current it is |
| `reindexSource` | ai | POST | Rebuild a source |
| `removeIndexEntry` | ai | DELETE | Remove one record from the index |
| `setAiTool` | ai | PUT | Register or change a tool (platform) |
| `setIndexSource` | ai | PUT | Declare a source indexed |
| `setSuggestionProvider` | ai | PUT |  |
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
| `listTaxProfiles` | catalogue | GET | The tax profiles |
| `relinquishInventoryHold` | catalogue | DELETE | Return unsold units |
| `renewInventoryHold` | catalogue | POST | Extend a lease TTL |
| `setEntitlementTemplateBlackoutDates` | catalogue | PUT | Set the dates a product's entitlement does not admit |
| `setEventChangeTreatmentPolicy` | catalogue | PUT | Set the default treatment per kind of event change |
| … | | | 99 more |

### 3 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Floor Service** — waves 1, 2
- **Operations** — waves 1, 2, 3
- **Stock on the Floor** — waves 1, 2

## Modules

| Module | Screens | Waves |
|---|---|---|
| Operations | 46 | 1, 2, 3 |
| Rentals | 30 | 3 |
| Floor Service | 10 | 1, 2 |
| Stock on the Floor | 10 | 1, 2 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `EMP-001` | Sign in | Operations | 1 | 9 | yes |
| `EMP-002` | Select venue & role | Operations | 1 | 2 | yes |
| `EMP-003` | Home — on duty | Operations | 1 | 7 | yes |
| `EMP-004` | Task list | Operations | 1 | 4 | yes |
| `EMP-005` | Task detail | Operations | 1 | 14 | yes |
| `EMP-006` | Raise a task | Operations | 1 | 16 | yes |
| `EMP-007` | Handover notes | Operations | 2 | 1 | yes |
| `EMP-008` | Shift summary | Operations | 2 | 5 | yes |
| `EMP-009` | End shift | Operations | 1 | 7 | yes |
| `EMP-010` | Scan — ready | Operations | 1 | 5 | yes |
| `EMP-014` | Ticket lookup | Operations | 1 | 5 | yes |
| `EMP-015` | Group scan | Operations | 2 | 7 | yes |
| `EMP-017` | Sync & reconciliation | Operations | 1 | 8 | yes |
| `EMP-018` | Offline package | Operations | 1 | 3 | yes |
| `EMP-019` | AI assistant — home | Operations | 1 | 3 | yes |
| `EMP-020` | AI assistant — answer | Operations | 1 | 5 | yes |
| `EMP-021` | Roster | Operations | 1 | 2 | yes |
| `EMP-022` | My rota | Operations | 1 | 2 | yes |
| `EMP-023` | Swap request | Operations | 2 | 3 | yes |
| `EMP-024` | Clock in / out | Operations | 1 | 2 | yes |
| `EMP-025` | Break management | Operations | 2 | 2 | yes |
| `EMP-026` | Incident report | Operations | 1 | 6 | yes |
| `EMP-027` | Incident detail | Operations | 2 | 4 | yes |
| `EMP-028` | Lost & found | Operations | 2 | 7 | yes |
| `EMP-029` | Guest assistance | Operations | 2 | 12 | yes |
| `EMP-030` | Venue map | Operations | 2 | 2 | yes |
| `EMP-031` | Queue monitor | Operations | 2 | 8 | yes |
| `EMP-032` | Manual wait entry | Operations | 1 | 3 | yes |
| `EMP-033` | Capacity view | Operations | 2 | 3 | yes |
| `EMP-034` | Walk-up sale | Operations | 2 | 20 | yes |
| `EMP-035` | Payment on device | Operations | 2 | 4 | yes |
| `EMP-036` | Issue media | Operations | 2 | 3 | yes |
| `EMP-037` | Notifications | Operations | 1 | 8 | yes |
| `EMP-038` | Broadcast to team | Operations | 2 | 3 | yes |
| `EMP-039` | Announcements | Operations | 2 | 2 | yes |
| `EMP-040` | Knowledge base | Operations | 2 | 1 | yes |
| `EMP-041` | Training | Operations | 3 | 2 | yes |
| `EMP-042` | Profile | Operations | 1 | 6 | yes |
| `EMP-043` | Device settings | Operations | 1 | 2 | yes |
| `EMP-044` | Accessibility | Operations | 2 | 0 | yes |
| `EMP-045` | Arabic / RTL | Operations | 1 | 0 | yes |
| `EMP-046` | Sign out | Operations | 1 | 1 | yes |
| `EMP-047` | Emergency mode | Operations | 1 | 2 | yes |
| `EMP-048` | Opening checklist | Operations | 1 | 3 | yes |
| `EMP-049` | Hand over the journal | Operations | 1 | 2 | yes |
| `EMP-050` | Post-incident restore | Operations | 2 | 3 | yes |
| `EMP-051` | Restaurant Service Command Center | Floor Service | 2 | 3 | yes |
| `EMP-052` | Floor Plan & Table Map | Floor Service | 2 | 1 | yes |
| `EMP-053` | Table & Seating Configuration | Floor Service | 2 | 3 | yes |
| `EMP-054` | Reservation Calendar & Timeline | Floor Service | 2 | 2 | yes |
| `EMP-055` | Create / Edit Reservation | Floor Service | 2 | 4 | yes |
| `EMP-056` | Walk-In & Waitlist Management | Floor Service | 2 | 4 | yes |
| `EMP-057` | Guest Profile & Dining History | Floor Service | 2 | 5 | yes |
| `EMP-058` | Live Table & Service Management | Floor Service | 1 | 12 | yes |
| `EMP-059` | Table Order, Bill & Payment Management | Floor Service | 1 | 8 | yes |
| `EMP-060` | Reservation & Table Performance | Floor Service | 2 | 3 | yes |
| `EMP-061` | Retail Inventory Command Center | Stock on the Floor | 2 | 6 | yes |
| `EMP-062` | Store Stock & SKU Availability | Stock on the Floor | 2 | 3 | yes |
| `EMP-063` | Requisition & Smart Store Replenishment | Stock on the Floor | 2 | 4 | yes |
| `EMP-064` | Store-to-Store & Warehouse Transfers | Stock on the Floor | 2 | 5 | yes |
| `EMP-065` | Receiving | Stock on the Floor | 1 | 6 | yes |
| `EMP-066` | Stock Count & Cycle Count Management | Stock on the Floor | 2 | 5 | yes |
| `EMP-067` | Damage, Loss, Shrinkage & Stock Adjustment | Stock on the Floor | 1 | 6 | yes |
| `EMP-068` | Reservation, Allocation & Omnichannel Inventory | Stock on the Floor | 2 | 4 | yes |
| `EMP-069` | Barcode, RFID, Serialized Stock & Traceability | Stock on the Floor | 2 | 2 | yes |
| `EMP-070` | Inventory Exceptions, AI Replenishment & Action Center | Stock on the Floor | 2 | 3 | yes |
| `EMP-071` | Rental Checkout Command Center | Rentals | 3 | 1 | yes |
| `EMP-072` | Voucher Scan & Reservation Retrieval | Rentals | 3 | 1 | yes |
| `EMP-073` | Checkout Readiness Validation | Rentals | 3 | 1 | yes |
| `EMP-074` | Equipment Assignment Workspace | Rentals | 3 | 2 | yes |
| `EMP-075` | Equipment Scan & Validation | Rentals | 3 | 2 | yes |
| `EMP-076` | Pre-Rental Condition Inspection | Rentals | 3 | 1 | yes |
| `EMP-077` | Safety & Handover Checklist | Rentals | 3 | 1 | yes |
| `EMP-078` | Deposit & Financial Handover Validation | Rentals | 3 | 1 | yes |
| `EMP-079` | Group & Multi-Item Checkout | Rentals | 3 | 1 | yes |
| `EMP-080` | Checkout Confirmation & Rental Activation | Rentals | 3 | 1 | yes |
| `EMP-081` | Active Rental Operations Command Center | Rentals | 3 | 2 | yes |
| `EMP-082` | Active Rental Detail & Live Timeline | Rentals | 3 | 1 | yes |
| `EMP-083` | Rental Extension Request | Rentals | 3 | 1 | yes |
| `EMP-084` | Extension Pricing & Confirmation | Rentals | 3 | 2 | yes |
| `EMP-085` | Equipment Swap / Replacement | Rentals | 3 | 1 | yes |
| `EMP-086` | Rental Incident & Operational Exception | Rentals | 3 | 1 | yes |
| `EMP-087` | Due Soon & Customer Notification Management | Rentals | 3 | 1 | yes |
| `EMP-088` | Overdue Rental Management | Rentals | 3 | 1 | yes |
| `EMP-089` | Active Group Rental Management | Rentals | 3 | 1 | yes |
| `EMP-090` | Active Rental Intelligence & Operational Alerts | Rentals | 3 | 1 | yes |
| `EMP-091` | Rental Return Command Center | Rentals | 3 | 1 | yes |
| `EMP-092` | Return Scan & Rental Retrieval | Rentals | 3 | 1 | yes |
| `EMP-093` | Return Summary & Actual Return Time | Rentals | 3 | 1 | yes |
| `EMP-094` | Post-Rental Condition Inspection | Rentals | 3 | 1 | yes |
| `EMP-095` | Before vs After Condition Comparison | Rentals | 3 | 1 | yes |
| `EMP-096` | Damage Assessment & Charge Workflow | Rentals | 3 | 1 | yes |
| `EMP-097` | Partial Return & Missing Equipment | Rentals | 3 | 1 | yes |
| `EMP-098` | Late Fees, Damage Fees & Final Settlement | Rentals | 3 | 1 | yes |
| `EMP-099` | Deposit Release, Capture & Customer Confirmation | Rentals | 3 | 2 | yes |
| `EMP-100` | Return Completion & Equipment Disposition | Rentals | 3 | 1 | yes |

