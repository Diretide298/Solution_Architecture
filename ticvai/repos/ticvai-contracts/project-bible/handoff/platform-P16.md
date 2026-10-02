# P16 Venue Analytics — platform

**Derived.** `python3 tools/derive-platform.py P16`. App `venue-management-web` · venue · web

| | |
|---|---|
| Screens | 71 |
| Operations | 94 |
| Contracts | 10 |
| Modules | 1 |
| Undrawn | 0 |
| Operations with no screen | 121 |
| Waves | wave3 71 |

## Gaps

### 121 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `createKnowledgeCollection` | ai | POST | Create a collection |
| `generateVenueLayout` | ai | POST | Draft a seat map from an uploaded plan |
| `listIndexJobs` | ai | GET | Indexing in flight and recently finished |
| `listIndexSources` | ai | GET | What is indexed, and how current it is |
| `proposeWalkways` | ai | POST | Find walkable space in a drawing that has no vectors |
| `reindexSource` | ai | POST | Rebuild a source |
| `removeIndexEntry` | ai | DELETE | Remove one record from the index |
| `setAiTool` | ai | PUT | Register or change a tool (platform) |
| `setIndexSource` | ai | PUT | Declare a source indexed |
| `setSuggestionProvider` | ai | PUT |  |
| `getCatalogueImportJob` | catalogue | GET | Progress and findings of a catalogue import |
| `getEventChangeTreatmentPolicy` | catalogue | GET | What happens to tickets, reservations and guests when an event changes, by default |
| `getPlanBenefits` | catalogue | GET | Which benefits a plan grants, and how much of each |
| `getWaitingRoomStatus` | catalogue | GET | A performance's waiting room, its setting and how it is moving |
| `listGuestMemberships` | catalogue | GET | A guest's memberships, benefits and history |
| `listMembershipBenefits` | catalogue | GET | Benefits a plan can grant |
| `listMembershipProgrammes` | catalogue | GET | Membership schemes, the level above a plan |
| `listProductApprovalWorkflows` | catalogue | GET | The product approval workflows `approveWorkflow` saved |
| `listSeatPricingRules` | catalogue | GET | Seat-level dynamic pricing rules |
| `relinquishInventoryHold` | catalogue | DELETE | Return unsold units |
| `renewInventoryHold` | catalogue | POST | Extend a lease TTL |
| `setEntitlementTemplateBlackoutDates` | catalogue | PUT | Set the dates a product's entitlement does not admit |
| `setEventChangeTreatmentPolicy` | catalogue | PUT | Set the default treatment per kind of event change |
| `setSeatPricingRule` | catalogue | PUT | Create or replace a seat-level dynamic pricing rule |
| `setWaitingRoomSetting` | catalogue | PUT | Switch a performance's waiting room on or off, and set how fast it releases |
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
| … | | | 81 more |

## Modules

| Module | Screens | Waves |
|---|---|---|
| Analytics | 71 | 3 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `ANL-001` | Executive Command Center | Analytics | 3 | 7 | yes |
| `ANL-002` | Sales, Revenue & Channel | Analytics | 3 | 3 | yes |
| `ANL-003` | Operational Performance | Analytics | 3 | 6 | yes |
| `ANL-004` | Product Performance | Analytics | 3 | 4 | yes |
| `ANL-005` | Cost, Margin & Profitability | Analytics | 3 | 4 | yes |
| `ANL-006` | Inventory & Waste Intelligence | Analytics | 3 | 6 | yes |
| `ANL-007` | Guest & Conversion Intelligence | Analytics | 3 | 6 | yes |
| `ANL-008` | Demand Forecasting | Analytics | 3 | 4 | yes |
| `ANL-009` | AI Assistant & Action Center | Analytics | 3 | 9 | yes |
| `ANL-010` | Suggestions & Advice | Analytics | 3 | 2 | yes |
| `ANL-012` | Live Operations Dashboard | Analytics | 3 | 2 | yes |
| `ANL-013` | Revenue Pulse | Analytics | 3 | 1 | yes |
| `ANL-014` | Attendance & Footfall Intelligence | Analytics | 3 | 1 | yes |
| `ANL-015` | Capacity & Utilization Monitor | Analytics | 3 | 1 | yes |
| `ANL-016` | Sales & Channel Performance | Analytics | 3 | 1 | yes |
| `ANL-017` | Customer, Membership & Loyalty Pulse | Analytics | 3 | 2 | yes |
| `ANL-018` | Alerts & Exception Center | Analytics | 3 | 1 | yes |
| `ANL-019` | AI Management Insights | Analytics | 3 | 4 | yes |
| `ANL-020` | Multi-Site & Performance Comparison | Analytics | 3 | 2 | yes |
| `ANL-021` | Dashboard Library | Analytics | 3 | 4 | yes |
| `ANL-022` | Dashboard Creation Wizard | Analytics | 3 | 1 | yes |
| `ANL-023` | Drag-and-Drop Dashboard Canvas | Analytics | 3 | 6 | yes |
| `ANL-024` | Widget & Visualization Library | Analytics | 3 | 1 | yes |
| `ANL-025` | KPI Builder | Analytics | 3 | 2 | yes |
| `ANL-026` | Targets, Thresholds & KPI Status Rules | Analytics | 3 | 2 | yes |
| `ANL-027` | Data & Filter Configuration | Analytics | 3 | 2 | yes |
| `ANL-028` | Drill-Down & Interaction Designer | Analytics | 3 | 1 | yes |
| `ANL-029` | Dashboard Access, Publishing & Versioning | Analytics | 3 | 1 | yes |
| `ANL-030` | Dashboard Preview, Validation & Health | Analytics | 3 | 3 | yes |
| `ANL-031` | Report Catalogue & Library | Analytics | 3 | 2 | yes |
| `ANL-032` | Report Creation Wizard | Analytics | 3 | 1 | yes |
| `ANL-033` | Data Domain & Dataset Selector | Analytics | 3 | 1 | yes |
| `ANL-034` | Field & Column Selector | Analytics | 3 | 1 | yes |
| `ANL-035` | Filter & Parameter Builder | Analytics | 3 | 1 | yes |
| `ANL-036` | Grouping, Aggregation & Calculation Builder | Analytics | 3 | 1 | yes |
| `ANL-037` | Cross-Domain Report Composer | Analytics | 3 | 2 | yes |
| `ANL-038` | Report Layout & Formatting Designer | Analytics | 3 | 1 | yes |
| `ANL-039` | Report Preview, Test & Validation | Analytics | 3 | 3 | yes |
| `ANL-040` | Save, Run & Report Results Viewer | Analytics | 3 | 2 | yes |
| `ANL-041` | Reporting Governance Command Center | Analytics | 3 | 2 | yes |
| `ANL-042` | Report Scheduler | Analytics | 3 | 2 | yes |
| `ANL-043` | Subscription Manager | Analytics | 3 | 2 | yes |
| `ANL-044` | Distribution & Delivery Configuration | Analytics | 3 | 1 | yes |
| `ANL-045` | Export & Download Center | Analytics | 3 | 2 | yes |
| `ANL-046` | Report API & Data Delivery Manager | Analytics | 3 | 1 | yes |
| `ANL-047` | Report Access & Sharing Control | Analytics | 3 | 4 | yes |
| `ANL-048` | Delivery Monitoring & Failure Management | Analytics | 3 | 1 | yes |
| `ANL-049` | Report Audit Trail & Compliance | Analytics | 3 | 1 | yes |
| `ANL-050` | Retention, Archive & Governance Policy | Analytics | 3 | 2 | yes |
| `ANL-051` | AI Analytics Command Center | Analytics | 3 | 1 | yes |
| `ANL-052` | Ask TICVAI — Natural Language Analytics | Analytics | 3 | 2 | yes |
| `ANL-053` | AI-Generated Dashboard Studio | Analytics | 3 | 1 | yes |
| `ANL-054` | AI Report Generator | Analytics | 3 | 1 | yes |
| `ANL-055` | Anomaly Detection Center | Analytics | 3 | 3 | yes |
| `ANL-056` | Root-Cause Analysis Explorer | Analytics | 3 | 3 | yes |
| `ANL-057` | Forecasting & Predictive Analytics Studio | Analytics | 3 | 5 | yes |
| `ANL-058` | AI Recommendation & Next-Best-Action Center | Analytics | 3 | 2 | yes |
| `ANL-059` | AI Insight History, Evidence & Explainability | Analytics | 3 | 5 | yes |
| `ANL-060` | AI Analytics Governance & Model Control | Analytics | 3 | 7 | yes |
| `ANL-061` | BI & Analytics Administration Command Center | Analytics | 3 | 2 | yes |
| `ANL-062` | Enterprise KPI Library | Analytics | 3 | 2 | yes |
| `ANL-063` | KPI Targets, Thresholds & Scorecards | Analytics | 3 | 2 | yes |
| `ANL-064` | Benchmark & Comparative Analytics Configuration | Analytics | 3 | 3 | yes |
| `ANL-065` | Data Source & Integration Registry | Analytics | 3 | 1 | yes |
| `ANL-066` | Semantic Model & Business Data Catalogue | Analytics | 3 | 2 | yes |
| `ANL-067` | Data Refresh, Pipeline & Data Health Monitor | Analytics | 3 | 1 | yes |
| `ANL-068` | Embedded BI, Workspace & Tenant Administration | Analytics | 3 | 1 | yes |
| `ANL-069` | Analytics Performance, Usage & Cost Monitor | Analytics | 3 | 1 | yes |
| `ANL-070` | Analytics Governance, Security & Audit Center | Analytics | 3 | 5 | yes |
| `ANL-071` | AI Maturity & Learning | Analytics | 3 | 6 | yes |
| `ANL-072` | Finance Dashboard | Analytics | 3 | 5 | yes |

