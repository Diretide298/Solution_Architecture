# P08 Venue Management — platform

**Derived.** `python3 tools/derive-platform.py P08`. App `venue-management-web` · venue · web

| | |
|---|---|
| Screens | 91 |
| Operations | 368 |
| Contracts | 21 |
| Modules | 19 |
| Undrawn | 18 |
| Operations with no screen | 154 |
| Waves | wave1 45 · wave2 42 · wave3 4 |

## Gaps

### 154 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `enrolFacePass` | access | POST | Register a facial profile against an entitlement |
| `getFacePassEnrolment` | access | GET | Whether a pass has a face registered, and when |
| `revokeFacePass` | access | DELETE | Remove a facial profile |
| `createKnowledgeCollection` | ai | POST | Create a collection |
| `decideProposedAction` | ai | POST | Approve or reject a proposal |
| `generateConfiguration` | ai | POST | Draft a configuration from a description |
| `generateVenueLayout` | ai | POST | Draft a seat map from an uploaded plan |
| `ingestKnowledgeDocument` | ai | POST | Add a document |
| `listIndexJobs` | ai | GET | Indexing in flight and recently finished |
| `listIndexSources` | ai | GET | What is indexed, and how current it is |
| `listKnowledgeCollections` | ai | GET | Collections available to this tenant |
| `listProposedActions` | ai | GET | What the assistant has proposed and nobody has decided |
| `reindexSource` | ai | POST | Rebuild a source |
| `removeIndexEntry` | ai | DELETE | Remove one record from the index |
| `setIndexSource` | ai | PUT | Declare a source indexed |
| `createApprovalRequest` | approvals | POST | Raise a request |
| `createDonationCampaign` | catalogue | POST | Create a campaign |
| `joinWaitlist` | catalogue | POST | Ask to be told if capacity frees up |
| `leaveWaitlist` | catalogue | DELETE | Stop waiting |
| `listDonationCampaigns` | catalogue | GET | Campaigns a guest can give to |
| `listWaitlistEntries` | catalogue | GET | Who is waiting for capacity |
| `offerWaitlistCapacity` | catalogue | POST | Tell a waiting guest that capacity appeared |
| `suspendEntitlement` | catalogue | POST | Suspend or reinstate an entitlement |
| `updateDonationCampaign` | catalogue | PATCH | Amend or close a campaign |
| `calculateTax` | finance | POST | Compute tax for a set of lines |
| `disputeObligation` | finance | POST | One entity disagrees with the amount |
| `recordSettlement` | finance | POST | One entity paid another |
| `resolveObligationDispute` | finance | POST | Agree what is actually owed |
| `clearTable` | fnb | POST | Mark a table cleared and free |
| `closeTableVisit` | fnb | POST | Settle and close a visit |
| `createModifierGroup` | fnb | POST | Create a modifier group |
| `createTableReservation` | fnb | POST | Book a table in advance |
| `getBill` | fnb | GET | Bill for a visit |
| `getTableVisit` | fnb | GET | Read a visit with all its orders |
| `listModifierGroups` | fnb | GET | List modifier groups |
| `listRecipes` | fnb | GET | List recipes |
| `listTableReservations` | fnb | GET | Bookings for a service period |
| `mergeTableVisits` | fnb | POST | Merge another visit into this one |
| `openTableVisit` | fnb | POST | Seat a party and open a visit |
| `requestBill` | fnb | POST | The party asked to pay |
| … | | | 114 more |

### 13 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **access** — waves 1, 2
- **ai** — waves 1, 2
- **approvals** — waves 1, 2, 3
- **catalogue** — waves 1, 2
- **finance** — waves 1, 2
- **fnb** — waves 1, 2
- **identity** — waves 1, 3
- **inventory** — waves 1, 2
- **maintenance** — waves 1, 2, 3
- **marketing-crm** — waves 1, 2
- **orders** — waves 1, 2
- **reporting** — waves 1, 2, 3
- **shift** — waves 1, 2

### 18 screens nobody has drawn

- `BO-074` Chart of Accounts — wave 1
- `BO-075` Account Mapping — wave 1
- `BO-076` Revenue Recognition — wave 2
- `BO-077` FX Rates & Variances — wave 2
- `BO-078` Requisitions — wave 1
- `BO-079` Stock Count — wave 1
- `BO-080` Stock Transfers — wave 2
- `BO-081` Inventory Items — wave 2
- `BO-082` Stock Movements — wave 2
- `BO-083` Suppliers — wave 2
- `BO-084` Approval Inbox — wave 1
- `BO-085` Approval Request — wave 1
- `BO-086` Approval Matrix — wave 2
- `BO-087` Approval Delegations — wave 2
- `BO-088` Approval Analytics — wave 3
- `BO-089` Journal Entries — wave 1
- `BO-090` Period Close — wave 1
- `BO-091` AI Policy & Spend — wave 1

## Modules

| Module | Screens | Waves |
|---|---|---|
| catalogue | 13 | 1, 2 |
| orders | 11 | 1, 2 |
| finance | 9 | 1, 2 |
| inventory | 9 | 1, 2 |
| access | 6 | 1, 2 |
| fnb | 5 | 1, 2 |
| reporting | 5 | 1, 2, 3 |
| maintenance | 5 | 1, 2, 3 |
| approvals | 5 | 1, 2, 3 |
| queue | 4 | 1 |
| shift | 4 | 1, 2 |
| marketing-crm | 3 | 1, 2 |
| identity | 3 | 1, 3 |
| workforce | 3 | 2 |
| ai | 2 | 1, 2 |
| promotions | 1 | 2 |
| assets | 1 | 2 |
| retail | 1 | 2 |
| Venue Operations | 1 | 2 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `BO-001` | Queue Directory | queue | 1 | 19 | yes |
| `BO-002` | Queue Configuration | queue | 1 | 14 | yes |
| `BO-003` | Queue Integration Setup | orders | 1 | 21 | yes |
| `BO-004` | Manual Wait Time Entry | queue | 1 | 11 | yes |
| `BO-005` | Queue Monitor | marketing-crm | 1 | 19 | yes |
| `BO-006` | Parking Configuration | access | 2 | 4 | yes |
| `BO-007` | Product Directory | catalogue | 1 | 10 | yes |
| `BO-008` | Product Detail & Variants | finance | 1 | 3 | yes |
| `BO-009` | Pricing Rules | catalogue | 1 | 7 | yes |
| `BO-010` | Promotions & Coupons | promotions | 2 | 15 | yes |
| `BO-011` | Packages & Bundles | catalogue | 2 | 4 | yes |
| `BO-012` | Membership Products | catalogue | 2 | 12 | yes |
| `BO-013` | Channel & Distribution | catalogue | 2 | 6 | yes |
| `BO-014` | Catalogue Publishing | catalogue | 1 | 10 | yes |
| `BO-015` | Session Calendar | catalogue | 1 | 11 | yes |
| `BO-016` | Session Template | catalogue | 1 | 11 | yes |
| `BO-017` | Capacity Management | catalogue | 1 | 6 | yes |
| `BO-018` | Allocation & Holds | catalogue | 2 | 5 | yes |
| `BO-019` | Closures & Blackouts | catalogue | 2 | 11 | yes |
| `BO-020` | Timed Entry Rules | fnb | 2 | 11 | yes |
| `BO-021` | Order Search | fnb | 1 | 2 | yes |
| `BO-022` | Order Detail | orders | 1 | 14 | yes |
| `BO-023` | Refunds & Exchanges | orders | 1 | 14 | yes |
| `BO-024` | Payment Exceptions | orders | 1 | 4 | yes |
| `BO-025` | Chargebacks & Disputes | finance | 2 | 5 | yes |
| `BO-026` | Group Bookings | orders | 2 | 14 | yes |
| `BO-027` | Reissue & Media Replacement | assets | 2 | 12 | yes |
| `BO-028` | Refund Approval Queue | orders | 1 | 1 | yes |
| `BO-029` | Report Builder | reporting | 2 | 9 | yes |
| `BO-030` | Access Point Directory | maintenance | 1 | 16 | yes |
| `BO-031` | Access Point Configuration | maintenance | 1 | 7 | yes |
| `BO-032` | Admission Profiles | access | 1 | 3 | yes |
| `BO-033` | Blacklist Management | access | 1 | 3 | yes |
| `BO-034` | Scan Activity | access | 1 | 7 | yes |
| `BO-035` | Override Audit | access | 1 | 7 | yes |
| `BO-036` | Device Registry | marketing-crm | 2 | 12 | yes |
| `BO-037` | Offline Package Status | catalogue | 1 | 4 | yes |
| `BO-038` | Reconciliation Queue | queue | 1 | 9 | yes |
| `BO-039` | Shift Directory | shift | 1 | 13 | yes |
| `BO-040` | Variance Approval | shift | 1 | 13 | yes |
| `BO-041` | Cash Movements | shift | 2 | 13 | yes |
| `BO-042` | Banking & Safe | shift | 2 | 13 | yes |
| `BO-043` | Daily Reconciliation | finance | 1 | 7 | yes |
| `BO-044` | F&B Outlets | fnb | 2 | 11 | yes |
| `BO-045` | Menu Management | fnb | 2 | 5 | yes |
| `BO-046` | Kitchen Display | fnb | 2 | 5 | yes |
| `BO-047` | F&B Order Management | orders | 2 | 14 | yes |
| `BO-048` | Retail Products | retail | 2 | 4 | yes |
| `BO-049` | Stock Levels | inventory | 2 | 2 | yes |
| `BO-050` | Stock Count | inventory | 2 | 2 | yes |
| `BO-051` | Purchase Orders | orders | 2 | 13 | yes |
| `BO-052` | Goods Receipt | inventory | 2 | 10 | yes |
| `BO-053` | Staff Directory | identity | 1 | 4 | yes |
| `BO-054` | Role Assignment | identity | 1 | 2 | yes |
| `BO-055` | Rota & Scheduling | workforce | 2 | 4 | yes |
| `BO-056` | Time & Attendance | workforce | 2 | 3 | yes |
| `BO-057` | Training & Certification | identity | 3 | 1 | yes |
| `BO-058` | Reporting Home | reporting | 1 | 9 | yes |
| `BO-059` | Sales Reports | reporting | 1 | 9 | yes |
| `BO-060` | Attendance & Footfall | reporting | 2 | 16 | yes |
| `BO-061` | Scheduled Reports | reporting | 3 | 9 | yes |
| `BO-062` | Venue Profile | orders | 1 | 4 | yes |
| `BO-063` | Opening Hours & Calendar | catalogue | 1 | 11 | yes |
| `BO-064` | Zones & Areas | access | 1 | 10 | yes |
| `BO-065` | Venue Configuration | orders | 1 | 4 | yes |
| `BO-066` | Notification Settings | workforce | 2 | 4 | yes |
| `BO-067` | Integrations | Venue Operations | 2 | 0 | yes |
| `BO-068` | Audit Log | ai | 2 | 1 | yes |
| `BO-069` | Asset Register | maintenance | 2 | 11 | yes |
| `BO-070` | Work Orders | orders | 2 | 13 | yes |
| `BO-071` | Planned Maintenance | maintenance | 3 | 3 | yes |
| `BO-072` | Incident Log | maintenance | 2 | 5 | yes |
| `BO-073` | Lost & Found Register | marketing-crm | 2 | 2 | yes |
| `BO-074` | Chart of Accounts | finance | 1 | 8 | **no** |
| `BO-075` | Account Mapping | finance | 1 | 7 | **no** |
| `BO-076` | Revenue Recognition | finance | 2 | 4 | **no** |
| `BO-077` | FX Rates & Variances | finance | 2 | 4 | **no** |
| `BO-078` | Requisitions | inventory | 1 | 8 | **no** |
| `BO-079` | Stock Count | inventory | 1 | 6 | **no** |
| `BO-080` | Stock Transfers | inventory | 2 | 4 | **no** |
| `BO-081` | Inventory Items | inventory | 2 | 7 | **no** |
| `BO-082` | Stock Movements | inventory | 2 | 2 | **no** |
| `BO-083` | Suppliers | inventory | 2 | 3 | **no** |
| `BO-084` | Approval Inbox | approvals | 1 | 3 | **no** |
| `BO-085` | Approval Request | approvals | 1 | 5 | **no** |
| `BO-086` | Approval Matrix | approvals | 2 | 2 | **no** |
| `BO-087` | Approval Delegations | approvals | 2 | 3 | **no** |
| `BO-088` | Approval Analytics | approvals | 3 | 1 | **no** |
| `BO-089` | Journal Entries | finance | 1 | 6 | **no** |
| `BO-090` | Period Close | finance | 1 | 6 | **no** |
| `BO-091` | AI Policy & Spend | ai | 1 | 3 | **no** |

