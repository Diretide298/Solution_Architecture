# P16 Venue Analytics — platform

**Derived.** `python3 tools/derive-platform.py P16`. App `venue-management-web` · venue · web

| | |
|---|---|
| Screens | 69 |
| Operations | 58 |
| Contracts | 11 |
| Modules | 1 |
| Undrawn | 0 |
| Operations with no screen | 124 |
| Waves | wave3 69 |

## Gaps

### 124 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `approveManualOverrideSupervisor` | access | PUT | Manual Override & Supervisor Approval |
| `listAccessChanges` | access | GET | Changes made to an entitlement's access |
| `listEntryRulePoints` | access | GET | Which access points an admission rule covers |
| `verifyIdentity` | access | POST | Check the person presenting against the person entitled |
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
| `approveMatrixMultiLevel` | approvals | PUT | Approval Matrix & Multi-Level Approval Configuration |
| `approveRoleAuthorityDelegation` | approvals | PUT | Roles, Authority, Delegation & Approval Limits |
| `approveUnifiedDecision` | approvals | PUT | Unified Approval Inbox & Decision Workspace |
| `submitApprovalRequest` | approvals | POST | Send a saved draft for approval |
| `getCatalogueImportJob` | catalogue | GET | Progress and findings of a catalogue import |
| `getPlanBenefits` | catalogue | GET | Which benefits a plan grants, and how much of each |
| `listMembershipBenefits` | catalogue | GET | Benefits a plan can grant |
| `listMembershipProgrammes` | catalogue | GET | Membership schemes, the level above a plan |
| `evaluateAccess` | identity | POST | Decide, now, and say why |
| `getAccessPolicy` | identity | GET | One policy, at a version |
| `getAccessPolicyBundle` | identity | GET | The policies a device needs to decide for itself |
| `getMembership` | identity | GET | A membership with its history, usage and renewals |
| `getPasswordPolicy` | identity | GET | Read the password and MFA policy in force |
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
| `setPrincipalModuleAccess` | identity | PUT | Tick what they may do |
| `listStockReservations` | inventory | GET | Soft holds on stock |
| … | | | 84 more |

## Modules

| Module | Screens | Waves |
|---|---|---|
| Analytics | 69 | 3 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `ANL-001` | Executive Command Center | Analytics | 3 | 6 | yes |
| `ANL-002` | Sales, Revenue & Channel | Analytics | 3 | 3 | yes |
| `ANL-003` | Operational Performance | Analytics | 3 | 6 | yes |
| `ANL-004` | Product Performance | Analytics | 3 | 4 | yes |
| `ANL-005` | Cost, Margin & Profitability | Analytics | 3 | 4 | yes |
| `ANL-006` | Inventory & Waste Intelligence | Analytics | 3 | 5 | yes |
| `ANL-007` | Guest & Conversion Intelligence | Analytics | 3 | 6 | yes |
| `ANL-008` | Demand Forecasting | Analytics | 3 | 3 | yes |
| `ANL-009` | AI Assistant & Action Center | Analytics | 3 | 8 | yes |
| `ANL-010` | Suggestions & Advice | Analytics | 3 | 2 | yes |
| `ANL-012` | Live Operations Dashboard | Analytics | 3 | 2 | yes |
| `ANL-013` | Revenue Pulse | Analytics | 3 | 1 | yes |
| `ANL-014` | Attendance & Footfall Intelligence | Analytics | 3 | 1 | yes |
| `ANL-015` | Capacity & Utilization Monitor | Analytics | 3 | 1 | yes |
| `ANL-016` | Sales & Channel Performance | Analytics | 3 | 1 | yes |
| `ANL-017` | Customer, Membership & Loyalty Pulse | Analytics | 3 | 1 | yes |
| `ANL-018` | Alerts & Exception Center | Analytics | 3 | 1 | yes |
| `ANL-019` | AI Management Insights | Analytics | 3 | 2 | yes |
| `ANL-020` | Multi-Site & Performance Comparison | Analytics | 3 | 2 | yes |
| `ANL-021` | Dashboard Library | Analytics | 3 | 4 | yes |
| `ANL-022` | Dashboard Creation Wizard | Analytics | 3 | 1 | yes |
| `ANL-023` | Drag-and-Drop Dashboard Canvas | Analytics | 3 | 4 | yes |
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
| `ANL-047` | Report Access & Sharing Control | Analytics | 3 | 1 | yes |
| `ANL-048` | Delivery Monitoring & Failure Management | Analytics | 3 | 1 | yes |
| `ANL-049` | Report Audit Trail & Compliance | Analytics | 3 | 1 | yes |
| `ANL-050` | Retention, Archive & Governance Policy | Analytics | 3 | 1 | yes |
| `ANL-051` | AI Analytics Command Center | Analytics | 3 | 1 | yes |
| `ANL-052` | Ask TICVAI — Natural Language Analytics | Analytics | 3 | 2 | yes |
| `ANL-053` | AI-Generated Dashboard Studio | Analytics | 3 | 1 | yes |
| `ANL-054` | AI Report Generator | Analytics | 3 | 1 | yes |
| `ANL-055` | Anomaly Detection Center | Analytics | 3 | 1 | yes |
| `ANL-056` | Root-Cause Analysis Explorer | Analytics | 3 | 2 | yes |
| `ANL-057` | Forecasting & Predictive Analytics Studio | Analytics | 3 | 1 | yes |
| `ANL-058` | AI Recommendation & Next-Best-Action Center | Analytics | 3 | 1 | yes |
| `ANL-059` | AI Insight History, Evidence & Explainability | Analytics | 3 | 1 | yes |
| `ANL-060` | AI Analytics Governance & Model Control | Analytics | 3 | 0 | yes |
| `ANL-061` | BI & Analytics Administration Command Center | Analytics | 3 | 2 | yes |
| `ANL-062` | Enterprise KPI Library | Analytics | 3 | 2 | yes |
| `ANL-063` | KPI Targets, Thresholds & Scorecards | Analytics | 3 | 2 | yes |
| `ANL-064` | Benchmark & Comparative Analytics Configuration | Analytics | 3 | 3 | yes |
| `ANL-065` | Data Source & Integration Registry | Analytics | 3 | 1 | yes |
| `ANL-066` | Semantic Model & Business Data Catalogue | Analytics | 3 | 2 | yes |
| `ANL-067` | Data Refresh, Pipeline & Data Health Monitor | Analytics | 3 | 1 | yes |
| `ANL-068` | Embedded BI, Workspace & Tenant Administration | Analytics | 3 | 1 | yes |
| `ANL-069` | Analytics Performance, Usage & Cost Monitor | Analytics | 3 | 1 | yes |
| `ANL-070` | Analytics Governance, Security & Audit Center | Analytics | 3 | 1 | yes |

