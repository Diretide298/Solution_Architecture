# P08 Venue Management — platform

**Derived.** `python3 tools/derive-platform.py P08`. App `venue-management-web` · venue · web

| | |
|---|---|
| Screens | 108 |
| Operations | 383 |
| Contracts | 23 |
| Modules | 8 |
| Undrawn | 35 |
| Operations with no screen | 240 |
| Waves | wave1 54 · wave2 50 · wave3 4 |

## Gaps

### 240 operations with no screen here

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
| `proposeTranslations` | ai | POST |  |
| `proposeWalkways` | ai | POST | Find walkable space in a drawing that has no vectors |
| `reindexSource` | ai | POST | Rebuild a source |
| `removeIndexEntry` | ai | DELETE | Remove one record from the index |
| `setIndexSource` | ai | PUT | Declare a source indexed |
| `createApprovalRequest` | approvals | POST | Raise a request |
| `assessProductChange` | catalogue | POST | What a change would touch, before making it |
| `bulkChangePrices` | catalogue | POST | Reprice a category or a whole catalogue |
| `cloneProduct` | catalogue | POST | Copy a product as a new draft |
| `commitCatalogueImport` | catalogue | POST | Apply a parsed catalogue import |
| `createDonationCampaign` | catalogue | POST | Create a campaign |
| `freezeEntitlement` | catalogue | POST | Pause a membership at the guest's request |
| `importProductCatalogue` | catalogue | POST | Parse a catalogue file into a preview |
| `joinWaitlist` | catalogue | POST | Ask to be told if capacity frees up |
| `leaveWaitlist` | catalogue | DELETE | Stop waiting |
| `listDonationCampaigns` | catalogue | GET | Campaigns a guest can give to |
| `listGuestMemberships` | catalogue | GET | A guest's memberships, benefits and history |
| `listProductVersions` | catalogue | GET | What this product used to be |
| `listWaitlistEntries` | catalogue | GET | Who is waiting for capacity |
| `offerWaitlistCapacity` | catalogue | POST | Tell a waiting guest that capacity appeared |
| `reinstateEntitlement` | catalogue | POST | Lift a suspension |
| `restoreProductVersion` | catalogue | POST | Put a previous version back |
| `suspendEntitlement` | catalogue | POST | Suspend or reinstate an entitlement |
| `updateDonationCampaign` | catalogue | PATCH | Amend or close a campaign |
| `calculateTax` | finance | POST | Compute tax for a set of lines |
| `disputeObligation` | finance | POST | One entity disagrees with the amount |
| `getUnifiedReconciliation` | finance | GET | Every money source against the ledger, in one view |
| `recordDeposit` | finance | POST | Money taken before the sale is complete |
| … | | | 200 more |

### 8 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Access & Venue** — waves 1, 2, 3
- **Food & Beverage** — waves 1, 2
- **Guests & Marketing** — waves 1, 2
- **Orders & Money** — waves 1, 2, 3
- **People & Access Rights** — waves 1, 2, 3
- **Sell** — waves 1, 2
- **Stock & Supply** — waves 1, 2
- **Venue Operations** — waves 1, 2

### 35 screens nobody has drawn

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
- `BO-092` Venue Maps — wave 2
- `BO-093` Map Import & Labelling — wave 2
- `BO-094` Map Editor & Publish — wave 2
- `BO-095` Resources — wave 2
- `BO-096` Resource Calendar — wave 2
- `BO-097` Check Out & Check In — wave 2
- `BO-098` Qualifications — wave 2
- `BO-099` Session Manifest — wave 2
- `BO-100` Venue Home — wave 1
- `BO-101` Orders & Money — wave 1
- `BO-102` Sell — wave 1
- `BO-103` Access & Venue — wave 1
- `BO-104` Food & Beverage — wave 1
- `BO-105` Stock & Supply — wave 1
- `BO-106` People & Access Rights — wave 1
- `BO-107` Guests & Marketing — wave 1
- `BO-108` Venue Operations — wave 1

## Modules

| Module | Screens | Waves |
|---|---|---|
| Orders & Money | 29 | 1, 2, 3 |
| Access & Venue | 25 | 1, 2, 3 |
| Sell | 15 | 1, 2 |
| People & Access Rights | 12 | 1, 2, 3 |
| Stock & Supply | 10 | 1, 2 |
| Venue Operations | 8 | 1, 2 |
| Food & Beverage | 5 | 1, 2 |
| Guests & Marketing | 4 | 1, 2 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `BO-001` | Queue Directory | Access & Venue | 1 | 19 | yes |
| `BO-002` | Queue Configuration | Access & Venue | 1 | 14 | yes |
| `BO-003` | Queue Integration Setup | Access & Venue | 1 | 21 | yes |
| `BO-004` | Manual Wait Time Entry | Access & Venue | 1 | 11 | yes |
| `BO-005` | Queue Monitor | Access & Venue | 1 | 19 | yes |
| `BO-006` | Parking Configuration | Access & Venue | 2 | 4 | yes |
| `BO-007` | Product Directory | Sell | 1 | 10 | yes |
| `BO-008` | Product Detail & Variants | Orders & Money | 1 | 3 | yes |
| `BO-009` | Pricing Rules | Sell | 1 | 7 | yes |
| `BO-010` | Promotions & Coupons | Sell | 2 | 15 | yes |
| `BO-011` | Packages & Bundles | Sell | 2 | 4 | yes |
| `BO-012` | Membership Products | Sell | 2 | 12 | yes |
| `BO-013` | Channel & Distribution | Sell | 2 | 6 | yes |
| `BO-014` | Catalogue Publishing | Sell | 1 | 10 | yes |
| `BO-015` | Session Calendar | Sell | 1 | 11 | yes |
| `BO-016` | Session Template | Sell | 1 | 11 | yes |
| `BO-017` | Capacity Management | Sell | 1 | 6 | yes |
| `BO-018` | Allocation & Holds | Sell | 2 | 5 | yes |
| `BO-019` | Closures & Blackouts | Sell | 2 | 11 | yes |
| `BO-020` | Timed Entry Rules | Food & Beverage | 2 | 11 | yes |
| `BO-021` | Order Search | Food & Beverage | 1 | 2 | yes |
| `BO-022` | Order Detail | Orders & Money | 1 | 14 | yes |
| `BO-023` | Refunds & Exchanges | Orders & Money | 1 | 14 | yes |
| `BO-024` | Payment Exceptions | Orders & Money | 1 | 4 | yes |
| `BO-025` | Chargebacks & Disputes | Orders & Money | 2 | 5 | yes |
| `BO-026` | Group Bookings | Orders & Money | 2 | 14 | yes |
| `BO-027` | Reissue & Media Replacement | Orders & Money | 2 | 4 | yes |
| `BO-028` | Refund Approval Queue | Orders & Money | 1 | 1 | yes |
| `BO-029` | Report Builder | Orders & Money | 2 | 9 | yes |
| `BO-030` | Access Point Directory | Access & Venue | 1 | 16 | yes |
| `BO-031` | Access Point Configuration | Access & Venue | 1 | 7 | yes |
| `BO-032` | Admission Profiles | Access & Venue | 1 | 3 | yes |
| `BO-033` | Blacklist Management | Access & Venue | 1 | 3 | yes |
| `BO-034` | Scan Activity | Access & Venue | 1 | 7 | yes |
| `BO-035` | Override Audit | Access & Venue | 1 | 7 | yes |
| `BO-036` | Device Registry | Venue Operations | 2 | 12 | yes |
| `BO-037` | Offline Package Status | Sell | 1 | 4 | yes |
| `BO-038` | Reconciliation Queue | Access & Venue | 1 | 9 | yes |
| `BO-039` | Shift Directory | Orders & Money | 1 | 13 | yes |
| `BO-040` | Variance Approval | Orders & Money | 1 | 13 | yes |
| `BO-041` | Cash Movements | Orders & Money | 2 | 13 | yes |
| `BO-042` | Banking & Safe | Orders & Money | 2 | 13 | yes |
| `BO-043` | Daily Reconciliation | Orders & Money | 1 | 7 | yes |
| `BO-044` | F&B Outlets | Venue Operations | 2 | 11 | yes |
| `BO-045` | Menu Management | Food & Beverage | 2 | 5 | yes |
| `BO-046` | Kitchen Display | Food & Beverage | 2 | 5 | yes |
| `BO-047` | F&B Order Management | Orders & Money | 2 | 14 | yes |
| `BO-048` | Retail Products | Orders & Money | 2 | 4 | yes |
| `BO-049` | Stock Levels | Stock & Supply | 2 | 2 | yes |
| `BO-050` | Stock Count | Stock & Supply | 2 | 2 | yes |
| `BO-051` | Purchase Orders | Orders & Money | 2 | 13 | yes |
| `BO-052` | Goods Receipt | Stock & Supply | 2 | 10 | yes |
| `BO-053` | Staff Directory | People & Access Rights | 1 | 4 | yes |
| `BO-054` | Role Assignment | People & Access Rights | 1 | 2 | yes |
| `BO-055` | Rota & Scheduling | People & Access Rights | 2 | 4 | yes |
| `BO-056` | Time & Attendance | People & Access Rights | 2 | 3 | yes |
| `BO-057` | Training & Certification | People & Access Rights | 3 | 1 | yes |
| `BO-058` | Reporting Home | Venue Operations | 1 | 9 | yes |
| `BO-059` | Sales Reports | Orders & Money | 1 | 9 | yes |
| `BO-060` | Attendance & Footfall | Venue Operations | 2 | 16 | yes |
| `BO-061` | Scheduled Reports | Orders & Money | 3 | 9 | yes |
| `BO-062` | Venue Profile | Orders & Money | 1 | 4 | yes |
| `BO-063` | Opening Hours & Calendar | Sell | 1 | 11 | yes |
| `BO-064` | Zones & Areas | Venue Operations | 1 | 10 | yes |
| `BO-065` | Venue Configuration | Orders & Money | 1 | 4 | yes |
| `BO-066` | Notification Settings | People & Access Rights | 2 | 4 | yes |
| `BO-067` | Integrations | Venue Operations | 2 | 0 | yes |
| `BO-068` | Audit Log | Guests & Marketing | 2 | 1 | yes |
| `BO-069` | Asset Register | Access & Venue | 2 | 11 | yes |
| `BO-070` | Work Orders | Orders & Money | 2 | 13 | yes |
| `BO-071` | Planned Maintenance | Access & Venue | 3 | 3 | yes |
| `BO-072` | Incident Log | Access & Venue | 2 | 5 | yes |
| `BO-073` | Lost & Found Register | Guests & Marketing | 2 | 2 | yes |
| `BO-074` | Chart of Accounts | Orders & Money | 1 | 8 | **no** |
| `BO-075` | Account Mapping | Orders & Money | 1 | 7 | **no** |
| `BO-076` | Revenue Recognition | Orders & Money | 2 | 4 | **no** |
| `BO-077` | FX Rates & Variances | Orders & Money | 2 | 4 | **no** |
| `BO-078` | Requisitions | Stock & Supply | 1 | 8 | **no** |
| `BO-079` | Stock Count | Stock & Supply | 1 | 6 | **no** |
| `BO-080` | Stock Transfers | Stock & Supply | 2 | 4 | **no** |
| `BO-081` | Inventory Items | Stock & Supply | 2 | 7 | **no** |
| `BO-082` | Stock Movements | Stock & Supply | 2 | 2 | **no** |
| `BO-083` | Suppliers | Stock & Supply | 2 | 3 | **no** |
| `BO-084` | Approval Inbox | People & Access Rights | 1 | 3 | **no** |
| `BO-085` | Approval Request | People & Access Rights | 1 | 5 | **no** |
| `BO-086` | Approval Matrix | People & Access Rights | 2 | 2 | **no** |
| `BO-087` | Approval Delegations | People & Access Rights | 2 | 3 | **no** |
| `BO-088` | Approval Analytics | People & Access Rights | 3 | 1 | **no** |
| `BO-089` | Journal Entries | Orders & Money | 1 | 6 | **no** |
| `BO-090` | Period Close | Orders & Money | 1 | 6 | **no** |
| `BO-091` | AI Policy & Spend | Guests & Marketing | 1 | 3 | **no** |
| `BO-092` | Venue Maps | Access & Venue | 2 | 2 | **no** |
| `BO-093` | Map Import & Labelling | Access & Venue | 2 | 3 | **no** |
| `BO-094` | Map Editor & Publish | Access & Venue | 2 | 6 | **no** |
| `BO-095` | Resources | Access & Venue | 2 | 2 | **no** |
| `BO-096` | Resource Calendar | Access & Venue | 2 | 2 | **no** |
| `BO-097` | Check Out & Check In | Access & Venue | 2 | 4 | **no** |
| `BO-098` | Qualifications | Access & Venue | 2 | 1 | **no** |
| `BO-099` | Session Manifest | Access & Venue | 2 | 2 | **no** |
| `BO-100` | Venue Home | Venue Operations | 1 | 2 | **no** |
| `BO-101` | Orders & Money | Orders & Money | 1 | 1 | **no** |
| `BO-102` | Sell | Sell | 1 | 1 | **no** |
| `BO-103` | Access & Venue | Access & Venue | 1 | 1 | **no** |
| `BO-104` | Food & Beverage | Food & Beverage | 1 | 1 | **no** |
| `BO-105` | Stock & Supply | Stock & Supply | 1 | 1 | **no** |
| `BO-106` | People & Access Rights | People & Access Rights | 1 | 1 | **no** |
| `BO-107` | Guests & Marketing | Guests & Marketing | 1 | 1 | **no** |
| `BO-108` | Venue Operations | Venue Operations | 1 | 1 | **no** |

