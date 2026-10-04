# P12 Venue Support — platform

**Derived.** `python3 tools/derive-platform.py P12`. App `venue-support-web` · venue · web

| | |
|---|---|
| Screens | 28 |
| Operations | 67 |
| Contracts | 8 |
| Modules | 5 |
| Undrawn | 0 |
| Operations with no screen | 85 |
| Waves | wave1 4 · wave3 24 |

## Gaps

### 85 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `createKnowledgeCollection` | ai | POST | Create a collection |
| `generateVenueLayout` | ai | POST | Draft a seat map from an uploaded plan |
| `listIndexJobs` | ai | GET | Indexing in flight and recently finished |
| `listIndexSources` | ai | GET | What is indexed, and how current it is |
| `reindexSource` | ai | POST | Rebuild a source |
| `removeIndexEntry` | ai | DELETE | Remove one record from the index |
| `setAiTool` | ai | PUT | Register or change a tool (platform) |
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
| `evaluateAccess` | identity | POST | Decide, now, and say why |
| `getAuthorisationPolicy` | identity | GET | One policy, at a version |
| `getAuthorisationPolicyBundle` | identity | GET | The policies a device needs to decide for itself |
| `getMembership` | identity | GET | A membership with its history, usage and renewals |
| `getPrincipalModuleAccess` | identity | GET | What this person may do, as ticks |
| `listAccessDecisions` | identity | GET | What was decided, for whom, where and why |
| `listAuthorisationPolicyTemplates` | identity | GET | Reusable policy shapes |
| `listCustomerMemberships` | identity | GET | Memberships a customer holds |
| `listModuleCapabilities` | identity | GET | What a person can be allowed to do, per module |
| `listModules` | identity | GET | The module tree permissions are grouped under |
| `listSegregationRules` | identity | GET | Read the conflicting-permission rules back |
| `listSegregationViolations` | identity | GET | Who already holds a conflicting pair |
| `setPrincipalModuleAccess` | identity | PUT | Tick what they may do |
| `updateRole` | identity | PATCH | Rename a role or change its description |
| `actOnWaiverRequirements` | marketing-crm | POST | Send, resend or correct participant waiver requirements, one or in bulk |
| `createInvitationCampaign` | marketing-crm | POST | A quota-bounded, addressed invitation |
| `createLoyaltyProgramme` | marketing-crm | POST | Create a loyalty programme |
| `getCaseInvestigationResolution` | marketing-crm | GET | Read the case workspace |
| `getDigitalWaiverForm` | marketing-crm | GET | Load the layout of a waiver version |
| `getGuestExtraValues` | marketing-crm | GET | What a guest answered |
| `getSuppressionList` | marketing-crm | GET | Addresses suppressed from all sending |
| `getWaiverTesting` | marketing-crm | GET | Checklist, rule simulation and approval record of a waiver version |
| `issueReward` | marketing-crm | POST | Issue a reward to a guest |
| … | | | 45 more |

### 2 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Access & Availability** — waves 1, 3
- **Overview** — waves 1, 3

## Modules

| Module | Screens | Waves |
|---|---|---|
| Support | 20 | 3 |
| Access & Availability | 2 | 1, 3 |
| Overview | 2 | 1, 3 |
| Conversations | 2 | 1 |
| Knowledge & Responses | 2 | 3 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `SUP-001` | Venue Management Sign In | Access & Availability | 1 | 11 | yes |
| `SUP-002` | Agent Dashboard | Overview | 1 | 10 | yes |
| `SUP-003` | Availability & Routing Settings | Access & Availability | 3 | 1 | yes |
| `SUP-004` | Conversation Queue | Conversations | 1 | 3 | yes |
| `SUP-005` | Live Chat Workspace | Conversations | 1 | 11 | yes |
| `SUP-006` | Knowledge Base Search | Knowledge & Responses | 3 | 3 | yes |
| `SUP-007` | Canned Response Management | Knowledge & Responses | 3 | 2 | yes |
| `SUP-008` | Agent Performance & SLA View | Overview | 3 | 10 | yes |
| `SUP-009` | Customer Service Command Center | Support | 3 | 2 | yes |
| `SUP-010` | Customer 360° Service Profile | Support | 3 | 2 | yes |
| `SUP-011` | Unified Interaction & Communication History | Support | 3 | 1 | yes |
| `SUP-012` | Case Creation, Classification & Intelligent Routing | Support | 3 | 3 | yes |
| `SUP-013` | Case Investigation & Resolution Workspace | Support | 3 | 6 | yes |
| `SUP-014` | Order, Booking & Ticket Service Workspace | Support | 3 | 2 | yes |
| `SUP-015` | Refund, Compensation & Service Exception Workspace | Support | 3 | 1 | yes |
| `SUP-016` | Escalation, Collaboration & Internal Resolution | Support | 3 | 1 | yes |
| `SUP-017` | Case Resolution, Closure & Customer Feedback | Support | 3 | 2 | yes |
| `SUP-018` | AI Customer Service Copilot & Knowledge Workspace | Support | 3 | 3 | yes |
| `SUP-019` | Contact Center Operations Command Center | Support | 3 | 1 | yes |
| `SUP-020` | Queue Configuration & Management | Support | 3 | 2 | yes |
| `SUP-021` | Intelligent Routing, Skills & Assignment Engine | Support | 3 | 3 | yes |
| `SUP-022` | SLA Policy & Service-Level Management | Support | 3 | 2 | yes |
| `SUP-023` | Agent Workload, Availability & Workforce Control | Support | 3 | 2 | yes |
| `SUP-024` | Escalation & Critical Case Monitor | Support | 3 | 1 | yes |
| `SUP-025` | Quality Management & Agent Evaluation | Support | 3 | 1 | yes |
| `SUP-026` | Customer Satisfaction, Feedback & Voice of Customer | Support | 3 | 1 | yes |
| `SUP-027` | Service Analytics & Root-Cause Intelligence | Support | 3 | 1 | yes |
| `SUP-028` | AI Contact Center Intelligence & Automation Studio | Support | 3 | 1 | yes |

