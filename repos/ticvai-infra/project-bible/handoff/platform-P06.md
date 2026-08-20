# P06 Venue Staff App — platform

**Derived.** `python3 tools/derive-platform.py P06`. App `venue-staff-app` · venue · mobileApp · offline-capable

| | |
|---|---|
| Screens | 46 |
| Operations | 149 |
| Contracts | 14 |
| Modules | 1 |
| Undrawn | 0 |
| Operations with no screen | 147 |
| Waves | wave1 25 · wave2 20 · wave3 1 |

## Gaps

### 147 operations with no screen here

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
| `clearTable` | fnb | POST | Mark a table cleared and free |
| `closeTableVisit` | fnb | POST | Settle and close a visit |
| `completeProductionRun` | fnb | POST | Record what was actually made |
| `createModifierGroup` | fnb | POST | Create a modifier group |
| `createTableReservation` | fnb | POST | Book a table in advance |
| … | | | 107 more |

### 1 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Operations** — waves 1, 2, 3

## Modules

| Module | Screens | Waves |
|---|---|---|
| Operations | 46 | 1, 2, 3 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `EMP-001` | Sign in | Operations | 1 | 8 | yes |
| `EMP-002` | Select venue & role | Operations | 1 | 10 | yes |
| `EMP-003` | Home — on duty | Operations | 1 | 17 | yes |
| `EMP-004` | Task list | Operations | 1 | 16 | yes |
| `EMP-005` | Task detail | Operations | 1 | 16 | yes |
| `EMP-006` | Raise a task | Operations | 1 | 16 | yes |
| `EMP-007` | Handover notes | Operations | 2 | 4 | yes |
| `EMP-008` | Shift summary | Operations | 2 | 13 | yes |
| `EMP-009` | End shift | Operations | 1 | 13 | yes |
| `EMP-010` | Scan — ready | Operations | 1 | 7 | yes |
| `EMP-014` | Ticket lookup | Operations | 1 | 14 | yes |
| `EMP-015` | Group scan | Operations | 2 | 7 | yes |
| `EMP-017` | Sync & reconciliation | Operations | 1 | 9 | yes |
| `EMP-018` | Offline package | Operations | 1 | 4 | yes |
| `EMP-019` | AI assistant — home | Operations | 1 | 3 | yes |
| `EMP-020` | AI assistant — answer | Operations | 1 | 3 | yes |
| `EMP-021` | Roster | Operations | 1 | 4 | yes |
| `EMP-022` | My rota | Operations | 1 | 4 | yes |
| `EMP-023` | Swap request | Operations | 2 | 4 | yes |
| `EMP-024` | Clock in / out | Operations | 1 | 3 | yes |
| `EMP-025` | Break management | Operations | 2 | 3 | yes |
| `EMP-026` | Incident report | Operations | 1 | 5 | yes |
| `EMP-027` | Incident detail | Operations | 2 | 5 | yes |
| `EMP-028` | Lost & found | Operations | 2 | 7 | yes |
| `EMP-029` | Guest assistance | Operations | 2 | 12 | yes |
| `EMP-030` | Venue map | Operations | 2 | 6 | yes |
| `EMP-031` | Queue monitor | Operations | 2 | 9 | yes |
| `EMP-032` | Manual wait entry | Operations | 2 | 9 | yes |
| `EMP-033` | Capacity view | Operations | 2 | 6 | yes |
| `EMP-034` | Walk-up sale | Operations | 2 | 24 | yes |
| `EMP-035` | Payment on device | Operations | 2 | 4 | yes |
| `EMP-036` | Issue media | Operations | 2 | 3 | yes |
| `EMP-037` | Notifications | Operations | 1 | 4 | yes |
| `EMP-038` | Broadcast to team | Operations | 2 | 4 | yes |
| `EMP-039` | Announcements | Operations | 2 | 4 | yes |
| `EMP-040` | Knowledge base | Operations | 2 | 1 | yes |
| `EMP-041` | Training | Operations | 3 | 1 | yes |
| `EMP-042` | Profile | Operations | 1 | 7 | yes |
| `EMP-043` | Device settings | Operations | 1 | 12 | yes |
| `EMP-044` | Accessibility | Operations | 2 | 0 | yes |
| `EMP-045` | Arabic / RTL | Operations | 1 | 0 | yes |
| `EMP-046` | Sign out | Operations | 1 | 1 | yes |
| `EMP-047` | Emergency mode | Operations | 1 | 4 | yes |
| `EMP-048` | Opening checklist | Operations | 1 | 4 | yes |
| `EMP-049` | Hand over the journal | Operations | 1 | 2 | yes |
| `EMP-050` | Post-incident restore | Operations | 2 | 5 | yes |

