# P12 Venue Support — platform

**Derived.** `python3 tools/derive-platform.py P12`. App `venue-support-web` · venue · web

| | |
|---|---|
| Screens | 28 |
| Operations | 54 |
| Contracts | 7 |
| Modules | 5 |
| Undrawn | 0 |
| Operations with no screen | 93 |
| Waves | wave2 2 · wave3 26 |

## Gaps

### 93 operations with no screen here

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
| `listInterEntityObligations` | finance | GET | What one entity owes another |
| `recordWriteOff` | finance | POST | Write off an uncollectable balance |
| `resolveObligationDispute` | finance | POST | Agree what is actually owed |
| `runFxRevaluation` | finance | POST | Revalue monetary balances at close |
| `setFxProvider` | finance | PUT | Which provider serves which purpose |
| `createEmergencyAccessOverride` | identity | POST | Bypass the policy, loudly |
| `evaluateAccess` | identity | POST | Decide, now, and say why |
| `getAccessPolicy` | identity | GET | One policy, at a version |
| `getAccessPolicyBundle` | identity | GET | The policies a device needs to decide for itself |
| `getMembership` | identity | GET | A membership with its history, usage and renewals |
| `getPrincipalModuleAccess` | identity | GET | What this person may do, as ticks |
| `listAccessDecisions` | identity | GET | What was decided, for whom, where and why |
| `listAccessPolicyHistory` | identity | GET | Every version, who changed it and why |
| `listAccessPolicyTemplates` | identity | GET | Reusable policy shapes |
| `listCapabilityTemplates` | identity | GET | Saved tick-sets |
| `listCustomerMemberships` | identity | GET | Memberships a customer holds |
| `listModuleCapabilities` | identity | GET | What a person can be allowed to do, per module |
| `listModules` | identity | GET | The module tree permissions are grouped under |
| `listPermissions` | identity | GET | Every permission key the contracts enforce |
| `listSegregationRules` | identity | GET | Read the conflicting-permission rules back |
| `listSegregationViolations` | identity | GET | Who already holds a conflicting pair |
| `recordBenefitUsage` | identity | POST | Consume a benefit |
| `setAccessPolicyState` | identity | POST | Submit, approve, activate or retire a policy |
| `setCapabilityTemplate` | identity | PUT | Save a tick-set under a name |
| `setPrincipalModuleAccess` | identity | PUT | Tick what they may do |
| `updateAccessPolicy` | identity | PUT | Change a policy, as a new version |
| `addGuestNote` | marketing-crm | POST | What the floor needs to know about this table |
| … | | | 53 more |

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
| `SUP-001` | Venue Management Sign In | Access & Availability | 3 | 7 | yes |
| `SUP-002` | Agent Dashboard | Overview | 3 | 9 | yes |
| `SUP-003` | Availability & Routing Settings | Access & Availability | 3 | 1 | yes |
| `SUP-004` | Conversation Queue | Conversations | 2 | 10 | yes |
| `SUP-005` | Live Chat Workspace | Conversations | 2 | 11 | yes |
| `SUP-006` | Knowledge Base Search | Knowledge & Responses | 3 | 2 | yes |
| `SUP-007` | Canned Response Management | Knowledge & Responses | 3 | 2 | yes |
| `SUP-008` | Agent Performance & SLA View | Overview | 3 | 10 | yes |
| `SUP-009` | Customer Service Command Center | Support | 3 | 2 | yes |
| `SUP-010` | Customer 360° Service Profile | Support | 3 | 2 | yes |
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

