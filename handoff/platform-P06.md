# P06 Venue Staff App — platform

**Derived.** `python3 tools/derive-platform.py P06`. App `venue-staff-app` · venue · mobileApp · offline-capable

| | |
|---|---|
| Screens | 50 |
| Operations | 156 |
| Contracts | 13 |
| Modules | 12 |
| Undrawn | 0 |
| Operations with no screen | 81 |
| Waves | wave1 29 · wave2 20 · wave3 1 |

## Gaps

### 81 operations with no screen here

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
| `createDonationCampaign` | catalogue | POST | Create a campaign |
| `joinWaitlist` | catalogue | POST | Ask to be told if capacity frees up |
| `leaveWaitlist` | catalogue | DELETE | Stop waiting |
| `listDonationCampaigns` | catalogue | GET | Campaigns a guest can give to |
| `listWaitlistEntries` | catalogue | GET | Who is waiting for capacity |
| `offerWaitlistCapacity` | catalogue | POST | Tell a waiting guest that capacity appeared |
| `suspendEntitlement` | catalogue | POST | Suspend or reinstate an entitlement |
| `updateDonationCampaign` | catalogue | PATCH | Amend or close a campaign |
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
| `seatTableReservation` | fnb | POST | The party arrived and has been sat down |
| `setItemAvailability` | fnb | PUT | Mark an item available or eighty-sixed |
| `setRecipe` | fnb | PUT | Define a recipe for a menu item |
| `splitBill` | fnb | POST | Split a bill |
| `updateTableReservation` | fnb | PATCH | Change or cancel a booking |
| … | | | 41 more |

### 9 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Operations** — waves 1, 2
- **access** — waves 1, 2
- **ai** — waves 1, 2, 3
- **catalogue** — waves 1, 2
- **maintenance** — waves 1, 2
- **marketing-crm** — waves 1, 2
- **orders** — waves 1, 2
- **shift** — waves 1, 2
- **workforce** — waves 1, 2

## Modules

| Module | Screens | Waves |
|---|---|---|
| workforce | 10 | 1, 2 |
| access | 8 | 1, 2 |
| maintenance | 7 | 1, 2 |
| identity | 4 | 1 |
| orders | 4 | 1, 2 |
| ai | 4 | 1, 2, 3 |
| shift | 3 | 1, 2 |
| marketing-crm | 3 | 1, 2 |
| catalogue | 2 | 1, 2 |
| queue | 2 | 2 |
| Operations | 2 | 1, 2 |
| assets | 1 | 2 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `EMP-001` | Sign in | identity | 1 | 8 | yes |
| `EMP-002` | Select venue & role | identity | 1 | 10 | yes |
| `EMP-003` | Home — on duty | shift | 1 | 17 | yes |
| `EMP-004` | Task list | maintenance | 1 | 16 | yes |
| `EMP-005` | Task detail | maintenance | 1 | 16 | yes |
| `EMP-006` | Raise a task | maintenance | 1 | 16 | yes |
| `EMP-007` | Handover notes | workforce | 2 | 4 | yes |
| `EMP-008` | Shift summary | shift | 2 | 13 | yes |
| `EMP-009` | End shift | shift | 1 | 13 | yes |
| `EMP-010` | Scan — ready | access | 1 | 7 | yes |
| `EMP-011` | Scan — admitted | access | 1 | 7 | yes |
| `EMP-012` | Scan — denied | access | 1 | 7 | yes |
| `EMP-013` | Override | access | 1 | 7 | yes |
| `EMP-014` | Ticket lookup | orders | 1 | 14 | yes |
| `EMP-015` | Group scan | access | 2 | 7 | yes |
| `EMP-016` | Offline scanning | access | 1 | 7 | yes |
| `EMP-017` | Sync & reconciliation | access | 1 | 9 | yes |
| `EMP-018` | Offline package | catalogue | 1 | 4 | yes |
| `EMP-019` | AI assistant — home | ai | 1 | 3 | yes |
| `EMP-020` | AI assistant — answer | ai | 1 | 3 | yes |
| `EMP-021` | Roster | workforce | 1 | 4 | yes |
| `EMP-022` | My rota | workforce | 1 | 4 | yes |
| `EMP-023` | Swap request | workforce | 2 | 4 | yes |
| `EMP-024` | Clock in / out | workforce | 1 | 3 | yes |
| `EMP-025` | Break management | workforce | 2 | 3 | yes |
| `EMP-026` | Incident report | maintenance | 1 | 5 | yes |
| `EMP-027` | Incident detail | maintenance | 2 | 5 | yes |
| `EMP-028` | Lost & found | marketing-crm | 2 | 7 | yes |
| `EMP-029` | Guest assistance | marketing-crm | 2 | 12 | yes |
| `EMP-030` | Venue map | orders | 2 | 4 | yes |
| `EMP-031` | Queue monitor | queue | 2 | 9 | yes |
| `EMP-032` | Manual wait entry | queue | 2 | 9 | yes |
| `EMP-033` | Capacity view | catalogue | 2 | 6 | yes |
| `EMP-034` | Walk-up sale | orders | 2 | 24 | yes |
| `EMP-035` | Payment on device | orders | 2 | 4 | yes |
| `EMP-036` | Issue media | assets | 2 | 12 | yes |
| `EMP-037` | Notifications | workforce | 1 | 4 | yes |
| `EMP-038` | Broadcast to team | workforce | 2 | 4 | yes |
| `EMP-039` | Announcements | workforce | 2 | 4 | yes |
| `EMP-040` | Knowledge base | ai | 2 | 1 | yes |
| `EMP-041` | Training | ai | 3 | 1 | yes |
| `EMP-042` | Profile | identity | 1 | 7 | yes |
| `EMP-043` | Device settings | marketing-crm | 1 | 12 | yes |
| `EMP-044` | Accessibility | Operations | 2 | 0 | yes |
| `EMP-045` | Arabic / RTL | Operations | 1 | 0 | yes |
| `EMP-046` | Sign out | identity | 1 | 1 | yes |
| `EMP-047` | Emergency mode | workforce | 1 | 4 | yes |
| `EMP-048` | Opening checklist | maintenance | 1 | 4 | yes |
| `EMP-049` | Hand over the journal | access | 1 | 2 | yes |
| `EMP-050` | Post-incident restore | maintenance | 2 | 5 | yes |

