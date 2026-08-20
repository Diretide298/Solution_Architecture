# P08 Venue Management — platform

**Derived.** `python3 tools/derive-platform.py P08`. App `venue-management-web` · venue · web

| | |
|---|---|
| Screens | 99 |
| Operations | 382 |
| Contracts | 23 |
| Modules | 8 |
| Undrawn | 26 |
| Operations with no screen | 244 |
| Waves | wave1 45 · wave2 50 · wave3 4 |

## Gaps

### 244 operations with no screen here

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
| `getMyMemberships` | catalogue | GET | A guest's own memberships, benefits and history |
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
| … | | | 204 more |

### 4 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Approvals** — waves 1, 2, 3
- **Finance** — waves 1, 2
- **Inventory** — waves 1, 2
- **Venue Operations** — waves 1, 2, 3

### 26 screens nobody has drawn

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

## Modules

| Module | Screens | Waves |
|---|---|---|
| Venue Operations | 72 | 1, 2, 3 |
| Finance | 6 | 1, 2 |
| Inventory | 6 | 1, 2 |
| Queue Management | 5 | 1 |
| Approvals | 5 | 1, 2, 3 |
| venue-map | 3 | 2 |
| Parking | 1 | 2 |
| AI | 1 | 1 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `BO-001` | Queue Directory | Queue Management | 1 | 19 | yes |
| `BO-002` | Queue Configuration | Queue Management | 1 | 14 | yes |
| `BO-003` | Queue Integration Setup | Queue Management | 1 | 21 | yes |
| `BO-004` | Manual Wait Time Entry | Queue Management | 1 | 11 | yes |
| `BO-005` | Queue Monitor | Queue Management | 1 | 19 | yes |
| `BO-006` | Parking Configuration | Parking | 2 | 4 | yes |
| `BO-007` | Product Directory | Venue Operations | 1 | 10 | yes |
| `BO-008` | Product Detail & Variants | Venue Operations | 1 | 3 | yes |
| `BO-009` | Pricing Rules | Venue Operations | 1 | 7 | yes |
| `BO-010` | Promotions & Coupons | Venue Operations | 2 | 15 | yes |
| `BO-011` | Packages & Bundles | Venue Operations | 2 | 4 | yes |
| `BO-012` | Membership Products | Venue Operations | 2 | 12 | yes |
| `BO-013` | Channel & Distribution | Venue Operations | 2 | 6 | yes |
| `BO-014` | Catalogue Publishing | Venue Operations | 1 | 10 | yes |
| `BO-015` | Session Calendar | Venue Operations | 1 | 11 | yes |
| `BO-016` | Session Template | Venue Operations | 1 | 11 | yes |
| `BO-017` | Capacity Management | Venue Operations | 1 | 6 | yes |
| `BO-018` | Allocation & Holds | Venue Operations | 2 | 5 | yes |
| `BO-019` | Closures & Blackouts | Venue Operations | 2 | 11 | yes |
| `BO-020` | Timed Entry Rules | Venue Operations | 2 | 11 | yes |
| `BO-021` | Order Search | Venue Operations | 1 | 2 | yes |
| `BO-022` | Order Detail | Venue Operations | 1 | 14 | yes |
| `BO-023` | Refunds & Exchanges | Venue Operations | 1 | 14 | yes |
| `BO-024` | Payment Exceptions | Venue Operations | 1 | 4 | yes |
| `BO-025` | Chargebacks & Disputes | Venue Operations | 2 | 5 | yes |
| `BO-026` | Group Bookings | Venue Operations | 2 | 14 | yes |
| `BO-027` | Reissue & Media Replacement | Venue Operations | 2 | 4 | yes |
| `BO-028` | Refund Approval Queue | Venue Operations | 1 | 1 | yes |
| `BO-029` | Report Builder | Venue Operations | 2 | 9 | yes |
| `BO-030` | Access Point Directory | Venue Operations | 1 | 16 | yes |
| `BO-031` | Access Point Configuration | Venue Operations | 1 | 7 | yes |
| `BO-032` | Admission Profiles | Venue Operations | 1 | 3 | yes |
| `BO-033` | Blacklist Management | Venue Operations | 1 | 3 | yes |
| `BO-034` | Scan Activity | Venue Operations | 1 | 7 | yes |
| `BO-035` | Override Audit | Venue Operations | 1 | 7 | yes |
| `BO-036` | Device Registry | Venue Operations | 2 | 12 | yes |
| `BO-037` | Offline Package Status | Venue Operations | 1 | 4 | yes |
| `BO-038` | Reconciliation Queue | Venue Operations | 1 | 9 | yes |
| `BO-039` | Shift Directory | Venue Operations | 1 | 13 | yes |
| `BO-040` | Variance Approval | Venue Operations | 1 | 13 | yes |
| `BO-041` | Cash Movements | Venue Operations | 2 | 13 | yes |
| `BO-042` | Banking & Safe | Venue Operations | 2 | 13 | yes |
| `BO-043` | Daily Reconciliation | Venue Operations | 1 | 7 | yes |
| `BO-044` | F&B Outlets | Venue Operations | 2 | 11 | yes |
| `BO-045` | Menu Management | Venue Operations | 2 | 5 | yes |
| `BO-046` | Kitchen Display | Venue Operations | 2 | 5 | yes |
| `BO-047` | F&B Order Management | Venue Operations | 2 | 14 | yes |
| `BO-048` | Retail Products | Venue Operations | 2 | 4 | yes |
| `BO-049` | Stock Levels | Venue Operations | 2 | 2 | yes |
| `BO-050` | Stock Count | Venue Operations | 2 | 2 | yes |
| `BO-051` | Purchase Orders | Venue Operations | 2 | 13 | yes |
| `BO-052` | Goods Receipt | Venue Operations | 2 | 10 | yes |
| `BO-053` | Staff Directory | Venue Operations | 1 | 4 | yes |
| `BO-054` | Role Assignment | Venue Operations | 1 | 2 | yes |
| `BO-055` | Rota & Scheduling | Venue Operations | 2 | 4 | yes |
| `BO-056` | Time & Attendance | Venue Operations | 2 | 3 | yes |
| `BO-057` | Training & Certification | Venue Operations | 3 | 1 | yes |
| `BO-058` | Reporting Home | Venue Operations | 1 | 9 | yes |
| `BO-059` | Sales Reports | Venue Operations | 1 | 9 | yes |
| `BO-060` | Attendance & Footfall | Venue Operations | 2 | 16 | yes |
| `BO-061` | Scheduled Reports | Venue Operations | 3 | 9 | yes |
| `BO-062` | Venue Profile | Venue Operations | 1 | 4 | yes |
| `BO-063` | Opening Hours & Calendar | Venue Operations | 1 | 11 | yes |
| `BO-064` | Zones & Areas | Venue Operations | 1 | 10 | yes |
| `BO-065` | Venue Configuration | Venue Operations | 1 | 4 | yes |
| `BO-066` | Notification Settings | Venue Operations | 2 | 4 | yes |
| `BO-067` | Integrations | Venue Operations | 2 | 0 | yes |
| `BO-068` | Audit Log | Venue Operations | 2 | 1 | yes |
| `BO-069` | Asset Register | Venue Operations | 2 | 11 | yes |
| `BO-070` | Work Orders | Venue Operations | 2 | 13 | yes |
| `BO-071` | Planned Maintenance | Venue Operations | 3 | 3 | yes |
| `BO-072` | Incident Log | Venue Operations | 2 | 5 | yes |
| `BO-073` | Lost & Found Register | Venue Operations | 2 | 2 | yes |
| `BO-074` | Chart of Accounts | Finance | 1 | 8 | **no** |
| `BO-075` | Account Mapping | Finance | 1 | 7 | **no** |
| `BO-076` | Revenue Recognition | Finance | 2 | 4 | **no** |
| `BO-077` | FX Rates & Variances | Finance | 2 | 4 | **no** |
| `BO-078` | Requisitions | Inventory | 1 | 8 | **no** |
| `BO-079` | Stock Count | Inventory | 1 | 6 | **no** |
| `BO-080` | Stock Transfers | Inventory | 2 | 4 | **no** |
| `BO-081` | Inventory Items | Inventory | 2 | 7 | **no** |
| `BO-082` | Stock Movements | Inventory | 2 | 2 | **no** |
| `BO-083` | Suppliers | Inventory | 2 | 3 | **no** |
| `BO-084` | Approval Inbox | Approvals | 1 | 3 | **no** |
| `BO-085` | Approval Request | Approvals | 1 | 5 | **no** |
| `BO-086` | Approval Matrix | Approvals | 2 | 2 | **no** |
| `BO-087` | Approval Delegations | Approvals | 2 | 3 | **no** |
| `BO-088` | Approval Analytics | Approvals | 3 | 1 | **no** |
| `BO-089` | Journal Entries | Finance | 1 | 6 | **no** |
| `BO-090` | Period Close | Finance | 1 | 6 | **no** |
| `BO-091` | AI Policy & Spend | AI | 1 | 3 | **no** |
| `BO-092` | Venue Maps | venue-map | 2 | 2 | **no** |
| `BO-093` | Map Import & Labelling | venue-map | 2 | 3 | **no** |
| `BO-094` | Map Editor & Publish | venue-map | 2 | 6 | **no** |
| `BO-095` | Resources | Venue Operations | 2 | 2 | **no** |
| `BO-096` | Resource Calendar | Venue Operations | 2 | 2 | **no** |
| `BO-097` | Check Out & Check In | Venue Operations | 2 | 4 | **no** |
| `BO-098` | Qualifications | Venue Operations | 2 | 1 | **no** |
| `BO-099` | Session Manifest | Venue Operations | 2 | 2 | **no** |

