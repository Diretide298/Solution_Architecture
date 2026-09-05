# P12 Venue Support — platform

**Derived.** `python3 tools/derive-platform.py P12`. App `venue-support-web` · venue · web

| | |
|---|---|
| Screens | 28 |
| Operations | 55 |
| Contracts | 7 |
| Modules | 5 |
| Undrawn | 0 |
| Operations with no screen | 82 |
| Waves | wave2 2 · wave3 26 |

## Gaps

### 82 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `createKnowledgeCollection` | ai | POST | Create a collection |
| `generateVenueLayout` | ai | POST | Draft a seat map from an uploaded plan |
| `ingestKnowledgeDocument` | ai | POST | Add a document |
| `listIndexSources` | ai | GET | What is indexed, and how current it is |
| `proposeTranslations` | ai | POST |  |
| `proposeWalkways` | ai | POST | Find walkable space in a drawing that has no vectors |
| `reindexSource` | ai | POST | Rebuild a source |
| `removeIndexEntry` | ai | DELETE | Remove one record from the index |
| `setIndexSource` | ai | PUT | Declare a source indexed |
| `setSuggestionProvider` | ai | PUT |  |
| `calculateTax` | finance | POST | Compute tax for a set of lines |
| `disputeObligation` | finance | POST | One entity disagrees with the amount |
| `getForeignTenderReport` | finance | GET | What was taken in which currency |
| `getUnifiedReconciliation` | finance | GET | Every money source against the ledger, in one view |
| `ingestFxRates` | finance | POST | Pull rates from the configured provider |
| `listInterEntityObligations` | finance | GET | What one entity owes another |
| `recordDeposit` | finance | POST | Money taken before the sale is complete |
| `recordSettlement` | finance | POST | One entity paid another |
| `recordWriteOff` | finance | POST | Write off an uncollectable balance |
| `resolveObligationDispute` | finance | POST | Agree what is actually owed |
| `runFxRevaluation` | finance | POST | Revalue monetary balances at close |
| `setFxProvider` | finance | PUT | Which provider serves which purpose |
| `validateRecognitionSchedules` | finance | POST | Find product kinds claimed by more than one schedule |
| `setPasswordPolicy` | identity | PUT | Length, breach check, lockout and step-up |
| `setSegregationRules` | identity | PUT | Which permissions may not be held together |
| `activateJourney` | marketing-crm | POST | Start it, or stop it |
| `addGuestNote` | marketing-crm | POST | What the floor needs to know about this table |
| `addSuppression` | marketing-crm | POST | Suppress an address |
| `createChallenge` | marketing-crm | POST | Define a challenge, mission or streak |
| `createForm` | marketing-crm | POST | Define a waiver, survey or capture form |
| `createInvitationCampaign` | marketing-crm | POST | A quota-bounded, addressed invitation |
| `createLoyaltyProgramme` | marketing-crm | POST | Create a loyalty programme |
| `createUrlRedirect` | marketing-crm | POST | 301, 302 and custom redirects |
| `getJourneyPerformance` | marketing-crm | GET | Entrants, completions, goals reached |
| `getLostItemMatches` | marketing-crm | GET | Candidate matches, scored |
| `getSuppressionList` | marketing-crm | GET | Addresses suppressed from all sending |
| `listMessageTriggers` | marketing-crm | GET | What fires a message, and when |
| `listReviews` | marketing-crm | GET | List guest reviews and ratings |
| `listSegmentMembers` | marketing-crm | GET | List guests currently matching a segment |
| `matchGuest` | marketing-crm | POST | Is this the same person we already have? |
| … | | | 42 more |

## Modules

| Module | Screens | Waves |
|---|---|---|
| Support | 20 | 3 |
| Access & Availability | 2 | 3 |
| Overview | 2 | 3 |
| Conversations | 2 | 2 |
| Knowledge & Responses | 2 | 3 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `SUP-001` | Agent Login | Access & Availability | 3 | 8 | yes |
| `SUP-002` | Agent Dashboard | Overview | 3 | 9 | yes |
| `SUP-003` | Availability & Routing Settings | Access & Availability | 3 | 1 | yes |
| `SUP-004` | Conversation Queue | Conversations | 2 | 10 | yes |
| `SUP-005` | Live Chat Workspace | Conversations | 2 | 11 | yes |
| `SUP-006` | Knowledge Base Search | Knowledge & Responses | 3 | 2 | yes |
| `SUP-007` | Canned Response Management | Knowledge & Responses | 3 | 2 | yes |
| `SUP-008` | Agent Performance & SLA View | Overview | 3 | 10 | yes |
| `SUP-009` | Customer Service Command Center | Support | 3 | 1 | yes |
| `SUP-010` | Customer 360° Service Profile | Support | 3 | 1 | yes |
| `SUP-011` | Unified Interaction & Communication History | Support | 3 | 1 | yes |
| `SUP-012` | Case Creation, Classification & Intelligent Routing | Support | 3 | 1 | yes |
| `SUP-013` | Case Investigation & Resolution Workspace | Support | 3 | 1 | yes |
| `SUP-014` | Order, Booking & Ticket Service Workspace | Support | 3 | 1 | yes |
| `SUP-015` | Refund, Compensation & Service Exception Workspace | Support | 3 | 1 | yes |
| `SUP-016` | Escalation, Collaboration & Internal Resolution | Support | 3 | 1 | yes |
| `SUP-017` | Case Resolution, Closure & Customer Feedback | Support | 3 | 1 | yes |
| `SUP-018` | AI Customer Service Copilot & Knowledge Workspace | Support | 3 | 1 | yes |
| `SUP-019` | Contact Center Operations Command Center | Support | 3 | 1 | yes |
| `SUP-020` | Queue Configuration & Management | Support | 3 | 1 | yes |
| `SUP-021` | Intelligent Routing, Skills & Assignment Engine | Support | 3 | 1 | yes |
| `SUP-022` | SLA Policy & Service-Level Management | Support | 3 | 1 | yes |
| `SUP-023` | Agent Workload, Availability & Workforce Control | Support | 3 | 1 | yes |
| `SUP-024` | Escalation & Critical Case Monitor | Support | 3 | 1 | yes |
| `SUP-025` | Quality Management & Agent Evaluation | Support | 3 | 1 | yes |
| `SUP-026` | Customer Satisfaction, Feedback & Voice of Customer | Support | 3 | 1 | yes |
| `SUP-027` | Service Analytics & Root-Cause Intelligence | Support | 3 | 1 | yes |
| `SUP-028` | AI Contact Center Intelligence & Automation Studio | Support | 3 | 1 | yes |

