# P16 Venue Analytics — platform

**Derived.** `python3 tools/derive-platform.py P16`. App `venue-management-web` · venue · web

| | |
|---|---|
| Screens | 10 |
| Operations | 20 |
| Contracts | 8 |
| Modules | 1 |
| Undrawn | 0 |
| Operations with no screen | 107 |
| Waves | wave3 10 |

## Gaps

### 107 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
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
| `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| `deleteGuestAccount` | identity | DELETE | Self-service account deletion |
| `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| `setPasswordPolicy` | identity | PUT | Length, breach check, lockout and step-up |
| `setSegregationRules` | identity | PUT | Which permissions may not be held together |
| `submitCountLines` | inventory | POST | Submit counted quantities |
| `activateJourney` | marketing-crm | POST | Start it, or stop it |
| `addGuestNote` | marketing-crm | POST | What the floor needs to know about this table |
| `addSuppression` | marketing-crm | POST | Suppress an address |
| `createChallenge` | marketing-crm | POST | Define a challenge, mission or streak |
| `createForm` | marketing-crm | POST | Define a waiver, survey or capture form |
| `createInvitationCampaign` | marketing-crm | POST | A quota-bounded, addressed invitation |
| … | | | 67 more |

## Modules

| Module | Screens | Waves |
|---|---|---|
| Analytics | 10 | 3 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `ANL-001` | Executive Command Center | Analytics | 3 | 4 | yes |
| `ANL-002` | Sales, Revenue & Channel | Analytics | 3 | 2 | yes |
| `ANL-003` | Operational Performance | Analytics | 3 | 5 | yes |
| `ANL-004` | Product Performance | Analytics | 3 | 3 | yes |
| `ANL-005` | Cost, Margin & Profitability | Analytics | 3 | 3 | yes |
| `ANL-006` | Inventory & Waste Intelligence | Analytics | 3 | 4 | yes |
| `ANL-007` | Guest & Conversion Intelligence | Analytics | 3 | 5 | yes |
| `ANL-008` | Demand Forecasting | Analytics | 3 | 2 | yes |
| `ANL-009` | AI Assistant & Action Center | Analytics | 3 | 8 | yes |
| `ANL-010` | Suggestions & Advice | Analytics | 3 | 2 | yes |

