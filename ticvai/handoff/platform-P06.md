# P06 Venue Staff App — platform

**Derived.** `python3 tools/derive-platform.py P06`. App `venue-staff-app` · venue · mobileApp · offline-capable

| | |
|---|---|
| Screens | 66 |
| Operations | 180 |
| Contracts | 17 |
| Modules | 3 |
| Undrawn | 0 |
| Operations with no screen | 145 |
| Waves | wave1 25 · wave2 40 · wave3 1 |

## Gaps

### 145 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `enrolFacePass` | access | POST | Register a facial profile against an entitlement |
| `getFacePassEnrolment` | access | GET | Whether a pass has a face registered, and when |
| `revokeFacePass` | access | DELETE | Remove a facial profile |
| `createKnowledgeCollection` | ai | POST | Create a collection |
| `generateVenueLayout` | ai | POST | Draft a seat map from an uploaded plan |
| `ingestKnowledgeDocument` | ai | POST | Add a document |
| `listIndexSources` | ai | GET | What is indexed, and how current it is |
| `listKnowledgeCollections` | ai | GET | Collections available to this tenant |
| `proposeTranslations` | ai | POST |  |
| `proposeWalkways` | ai | POST | Find walkable space in a drawing that has no vectors |
| `reindexSource` | ai | POST | Rebuild a source |
| `removeIndexEntry` | ai | DELETE | Remove one record from the index |
| `setIndexSource` | ai | PUT | Declare a source indexed |
| `setSuggestionProvider` | ai | PUT |  |
| `assessProductChange` | catalogue | POST | What a change would touch, before making it |
| `bulkChangePrices` | catalogue | POST | Reprice a category or a whole catalogue |
| `cloneProduct` | catalogue | POST | Copy a product as a new draft |
| `commitCatalogueImport` | catalogue | POST | Apply a parsed catalogue import |
| `createDonationCampaign` | catalogue | POST | Create a campaign |
| `freezeEntitlement` | catalogue | POST | Pause a membership at the guest's request |
| `listDonationCampaigns` | catalogue | GET | Campaigns a guest can give to |
| `listProductVersions` | catalogue | GET | What this product used to be |
| `listWaitlistEntries` | catalogue | GET | Who is waiting for capacity |
| `offerWaitlistCapacity` | catalogue | POST | Tell a waiting guest that capacity appeared |
| `reinstateEntitlement` | catalogue | POST | Lift a suspension |
| `restoreProductVersion` | catalogue | POST | Put a previous version back |
| `suspendEntitlement` | catalogue | POST | Suspend or reinstate an entitlement |
| `updateDonationCampaign` | catalogue | PATCH | Amend or close a campaign |
| `attachModifierGroup` | fnb | PUT | Give an item its choices |
| `clearTable` | fnb | POST | Mark a table cleared and free |
| `closeCorrectiveAction` | fnb | POST | Close a signed finding |
| `createCombo` | fnb | POST | A meal deal, priced as one thing |
| `createModifierGroup` | fnb | POST | Create a modifier group |
| `createTable` | fnb | POST | A table as a thing, not an inference |
| `escalateCorrectiveAction` | fnb | POST | Escalate a finding |
| `getTableVisit` | fnb | GET | Read a visit with all its orders |
| `rebalanceStationLoad` | fnb | POST | Move work between stations mid-service |
| `recordCorrectiveAction` | fnb | POST | Record what was done about a finding |
| `requestBill` | fnb | POST | The party asked to pay |
| `resolveBookingConflict` | fnb | GET | Two bookings, one table — and what to do about it |
| … | | | 105 more |

### 1 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Operations** — waves 1, 2, 3

## Modules

| Module | Screens | Waves |
|---|---|---|
| Operations | 46 | 1, 2, 3 |
| Floor Service | 10 | 2 |
| Stock on the Floor | 10 | 2 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `EMP-001` | Sign in | Operations | 1 | 5 | yes |
| `EMP-002` | Select venue & role | Operations | 1 | 6 | yes |
| `EMP-003` | Home — on duty | Operations | 1 | 17 | yes |
| `EMP-004` | Task list | Operations | 1 | 15 | yes |
| `EMP-005` | Task detail | Operations | 1 | 15 | yes |
| `EMP-006` | Raise a task | Operations | 1 | 16 | yes |
| `EMP-007` | Handover notes | Operations | 2 | 4 | yes |
| `EMP-008` | Shift summary | Operations | 2 | 5 | yes |
| `EMP-009` | End shift | Operations | 1 | 13 | yes |
| `EMP-010` | Scan — ready | Operations | 1 | 7 | yes |
| `EMP-014` | Ticket lookup | Operations | 1 | 14 | yes |
| `EMP-015` | Group scan | Operations | 2 | 7 | yes |
| `EMP-017` | Sync & reconciliation | Operations | 1 | 9 | yes |
| `EMP-018` | Offline package | Operations | 1 | 3 | yes |
| `EMP-019` | AI assistant — home | Operations | 1 | 3 | yes |
| `EMP-020` | AI assistant — answer | Operations | 1 | 3 | yes |
| `EMP-021` | Roster | Operations | 1 | 2 | yes |
| `EMP-022` | My rota | Operations | 1 | 2 | yes |
| `EMP-023` | Swap request | Operations | 2 | 2 | yes |
| `EMP-024` | Clock in / out | Operations | 1 | 3 | yes |
| `EMP-025` | Break management | Operations | 2 | 2 | yes |
| `EMP-026` | Incident report | Operations | 1 | 5 | yes |
| `EMP-027` | Incident detail | Operations | 2 | 3 | yes |
| `EMP-028` | Lost & found | Operations | 2 | 7 | yes |
| `EMP-029` | Guest assistance | Operations | 2 | 12 | yes |
| `EMP-030` | Venue map | Operations | 2 | 4 | yes |
| `EMP-031` | Queue monitor | Operations | 2 | 7 | yes |
| `EMP-032` | Manual wait entry | Operations | 2 | 5 | yes |
| `EMP-033` | Capacity view | Operations | 2 | 6 | yes |
| `EMP-034` | Walk-up sale | Operations | 2 | 22 | yes |
| `EMP-035` | Payment on device | Operations | 2 | 4 | yes |
| `EMP-036` | Issue media | Operations | 2 | 3 | yes |
| `EMP-037` | Notifications | Operations | 1 | 4 | yes |
| `EMP-038` | Broadcast to team | Operations | 2 | 4 | yes |
| `EMP-039` | Announcements | Operations | 2 | 4 | yes |
| `EMP-040` | Knowledge base | Operations | 2 | 1 | yes |
| `EMP-041` | Training | Operations | 3 | 1 | yes |
| `EMP-042` | Profile | Operations | 1 | 4 | yes |
| `EMP-043` | Device settings | Operations | 1 | 2 | yes |
| `EMP-044` | Accessibility | Operations | 2 | 0 | yes |
| `EMP-045` | Arabic / RTL | Operations | 1 | 0 | yes |
| `EMP-046` | Sign out | Operations | 1 | 1 | yes |
| `EMP-047` | Emergency mode | Operations | 1 | 4 | yes |
| `EMP-048` | Opening checklist | Operations | 1 | 4 | yes |
| `EMP-049` | Hand over the journal | Operations | 1 | 2 | yes |
| `EMP-050` | Post-incident restore | Operations | 2 | 4 | yes |
| `EMP-051` | Restaurant Service Command Center | Floor Service | 2 | 3 | yes |
| `EMP-052` | Floor Plan & Table Map | Floor Service | 2 | 2 | yes |
| `EMP-053` | Table & Seating Configuration | Floor Service | 2 | 1 | yes |
| `EMP-054` | Reservation Calendar & Timeline | Floor Service | 2 | 1 | yes |
| `EMP-055` | Create / Edit Reservation | Floor Service | 2 | 1 | yes |
| `EMP-056` | Walk-In & Waitlist Management | Floor Service | 2 | 1 | yes |
| `EMP-057` | Guest Profile & Dining History | Floor Service | 2 | 2 | yes |
| `EMP-058` | Live Table & Service Management | Floor Service | 2 | 16 | yes |
| `EMP-059` | Table Order, Bill & Payment Management | Floor Service | 2 | 7 | yes |
| `EMP-060` | Reservation & Table Performance | Floor Service | 2 | 2 | yes |
| `EMP-061` | Retail Inventory Command Center | Stock on the Floor | 2 | 2 | yes |
| `EMP-062` | Store Stock & SKU Availability | Stock on the Floor | 2 | 4 | yes |
| `EMP-063` | Requisition & Smart Store Replenishment | Stock on the Floor | 2 | 2 | yes |
| `EMP-064` | Store-to-Store & Warehouse Transfers | Stock on the Floor | 2 | 2 | yes |
| `EMP-065` | Receiving & Store Put-Away | Stock on the Floor | 2 | 4 | yes |
| `EMP-066` | Stock Count & Cycle Count Management | Stock on the Floor | 2 | 6 | yes |
| `EMP-067` | Damage, Loss, Shrinkage & Stock Adjustment | Stock on the Floor | 2 | 4 | yes |
| `EMP-068` | Reservation, Allocation & Omnichannel Inventory | Stock on the Floor | 2 | 2 | yes |
| `EMP-069` | Barcode, RFID, Serialized Stock & Traceability | Stock on the Floor | 2 | 2 | yes |
| `EMP-070` | Inventory Exceptions, AI Replenishment & Action Center | Stock on the Floor | 2 | 3 | yes |

