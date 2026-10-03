# P09 TICVAI Web — platform

**Derived.** `python3 tools/derive-platform.py P09`. App `ticvai-web` · ticvai · web

| | |
|---|---|
| Screens | 211 |
| Operations | 270 |
| Contracts | 14 |
| Modules | 13 |
| Undrawn | 0 |
| Operations with no screen | 105 |
| Waves | wave1 28 · wave2 13 · wave3 170 |

## Gaps

### 105 operations with no screen here

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
| `approveMatrixMultiLevel` | approvals | PUT | Approval Matrix & Multi-Level Approval Configuration |
| `approveRoleAuthorityDelegation` | approvals | PUT | Roles, Authority, Delegation & Approval Limits |
| `approveUnifiedDecision` | approvals | PUT | Unified Approval Inbox & Decision Workspace |
| `assignApprovalRequest` | approvals | PUT | Assign, reassign or claim a request in a shared queue |
| `cancelApprovalRequest` | approvals | POST | An administrator cancels a request nobody should decide any more |
| `issueAccreditationBadge` | approvals | POST | Issue a badge |
| `listAccreditationBadges` | approvals | GET | Badges issued and their state |
| `listAutomationExecutions` | approvals | GET | What automations ran, when, on whose rule, and the outcome |
| `reopenApprovalRequest` | approvals | POST | Reopen an expired or cancelled request as a new one |
| `submitApprovalRequest` | approvals | POST | Send a saved draft for approval |
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
| … | | | 65 more |

### 8 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Analytics** — waves 1, 3
- **Branding & Localisation** — waves 1, 2
- **Infrastructure & Resilience** — waves 2, 3
- **Overview & Health** — waves 1, 2
- **Platform** — waves 1, 3
- **Releases & Environments** — waves 1, 2, 3
- **Security & Compliance** — waves 1, 3
- **Tenants & Licensing** — waves 1, 2, 3

## Modules

| Module | Screens | Waves |
|---|---|---|
| Tenants & Licensing | 88 | 1, 2, 3 |
| Platform | 70 | 1, 3 |
| Analytics | 19 | 1, 3 |
| Releases & Environments | 8 | 1, 2, 3 |
| Overview & Health | 5 | 1, 2 |
| Access & Identity | 4 | 1 |
| Infrastructure & Resilience | 4 | 2, 3 |
| Branding & Localisation | 4 | 1, 2 |
| Security & Compliance | 2 | 1, 3 |
| Support & Communications | 2 | 3 |
| AI | 2 | 1 |
| Commercial | 2 | 3 |
| Platform Ops | 1 | 1 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `ADM-001` | Platform Login / MFA | Access & Identity | 1 | 11 | yes |
| `ADM-002` | Platform Dashboard | Overview & Health | 1 | 5 | yes |
| `ADM-003` | Cross-Tenant Health Dashboard | Overview & Health | 1 | 7 | yes |
| `ADM-004` | Platform Audit Log | Overview & Health | 2 | 6 | yes |
| `ADM-005` | Tenant Directory | Tenants & Licensing | 1 | 17 | yes |
| `ADM-006` | Tenant Hierarchy Explorer | Tenants & Licensing | 1 | 10 | yes |
| `ADM-007` | Module & Feature Entitlement | Tenants & Licensing | 1 | 8 | yes |
| `ADM-008` | Subscription & Plan Management | Tenants & Licensing | 1 | 15 | yes |
| `ADM-009` | Tenant Billing & Invoicing | Tenants & Licensing | 2 | 8 | yes |
| `ADM-010` | Usage Metering | Tenants & Licensing | 2 | 6 | yes |
| `ADM-011` | Licence & Seat Management | Tenants & Licensing | 2 | 9 | yes |
| `ADM-012` | Tenant Isolation & Resource Pool | Tenants & Licensing | 1 | 7 | yes |
| `ADM-013` | Tenant Performance Monitor | Overview & Health | 2 | 4 | yes |
| `ADM-014` | Auto-Scaling Configuration | Infrastructure & Resilience | 3 | 5 | yes |
| `ADM-015` | API Rate Limit & Quota Management | Tenants & Licensing | 3 | 13 | yes |
| `ADM-016` | White-Label Branding Management | Branding & Localisation | 1 | 16 | yes |
| `ADM-017` | Domain & Certificate Management | Branding & Localisation | 1 | 10 | yes |
| `ADM-018` | Interface Languages | Branding & Localisation | 1 | 5 | yes |
| `ADM-019` | Global Configuration & Defaults | Branding & Localisation | 2 | 5 | yes |
| `ADM-020` | Platform User Directory | Access & Identity | 1 | 7 | yes |
| `ADM-021` | Platform Role Management | Access & Identity | 1 | 5 | yes |
| `ADM-022` | Release & Version Management | Releases & Environments | 2 | 7 | yes |
| `ADM-023` | Staging Promotion & Approval | Releases & Environments | 2 | 5 | yes |
| `ADM-024` | Release Notification Composer | Releases & Environments | 3 | 3 | yes |
| `ADM-025` | Tenant Upgrade Scheduler | Releases & Environments | 2 | 2 | yes |
| `ADM-026` | End-of-Support Notice Management | Releases & Environments | 3 | 6 | yes |
| `ADM-027` | Database Migration Console | Releases & Environments | 1 | 6 | yes |
| `ADM-028` | Environment Registry | Releases & Environments | 2 | 2 | yes |
| `ADM-029` | Deployment Monitor | Overview & Health | 2 | 9 | yes |
| `ADM-030` | Infrastructure Sizing & Scaling Policy | Infrastructure & Resilience | 3 | 3 | yes |
| `ADM-031` | Security & Compliance Dashboard | Security & Compliance | 1 | 8 | yes |
| `ADM-032` | WAF & Security Policy View | Security & Compliance | 3 | 2 | yes |
| `ADM-033` | Backup & DR Status | Infrastructure & Resilience | 2 | 3 | yes |
| `ADM-034` | Archival Job Monitor | Infrastructure & Resilience | 3 | 1 | yes |
| `ADM-035` | Support & Escalation Console | Support & Communications | 3 | 2 | yes |
| `ADM-036` | Platform Notification Broadcast | Support & Communications | 3 | 2 | yes |
| `ADM-037` | AI Provider & Credentials | AI | 1 | 14 | yes |
| `ADM-068` | Tax, Fee & Calculation Command Center | Commercial | 3 | 6 | yes |
| `ADM-318` | Dead Letters | Platform Ops | 1 | 6 | yes |
| `ADM-369` | Commercial Command Center | Tenants & Licensing | 3 | 2 | yes |
| `ADM-370` | Customer Subscription & Commercial Portfolio | Tenants & Licensing | 3 | 1 | yes |
| `ADM-371` | Customer Commercial 360° | Tenants & Licensing | 3 | 2 | yes |
| `ADM-372` | Operational Profile, VSI & Commercial Model Intelligence | Tenants & Licensing | 3 | 1 | yes |
| `ADM-373` | Revenue & Commercial Model Analytics | Tenants & Licensing | 3 | 1 | yes |
| `ADM-374` | Trial & Conversion Monitor | Tenants & Licensing | 3 | 1 | yes |
| `ADM-375` | Renewal & Retention Center | Tenants & Licensing | 3 | 0 | yes |
| `ADM-376` | Commercial Optimization & Expansion Opportunities | Tenants & Licensing | 3 | 0 | yes |
| `ADM-377` | Subscription Exceptions & Commercial Alerts | Tenants & Licensing | 3 | 2 | yes |
| `ADM-378` | Executive AI Commercial Intelligence | Tenants & Licensing | 3 | 2 | yes |
| `ADM-379` | Welcome & Start Your TICVAI Journey | Tenants & Licensing | 3 | 0 | yes |
| `ADM-380` | Customer & Organization Registration | Tenants & Licensing | 3 | 3 | yes |
| `ADM-381` | Venue Type & Business Profile | Tenants & Licensing | 3 | 1 | yes |
| `ADM-382` | Visitor, Capacity & Operational Scale | Tenants & Licensing | 3 | 1 | yes |
| `ADM-383` | Sales Channel Assessment | Tenants & Licensing | 3 | 1 | yes |
| `ADM-384` | Ticketing & Product Requirements | Tenants & Licensing | 3 | 1 | yes |
| `ADM-385` | Access, Queue & Visitor Experience Assessment | Tenants & Licensing | 3 | 1 | yes |
| `ADM-386` | Additional Business Module Assessment | Tenants & Licensing | 3 | 2 | yes |
| `ADM-387` | Integration, Payment & Technical Readiness | Tenants & Licensing | 3 | 1 | yes |
| `ADM-388` | AI Assessment Summary & Handoff | Tenants & Licensing | 3 | 1 | yes |
| `ADM-389` | Commercial Rules Engine Overview | Tenants & Licensing | 3 | 1 | yes |
| `ADM-390` | VSI Model Builder | Tenants & Licensing | 3 | 2 | yes |
| `ADM-391` | VSI Scoring & Tier Threshold Configuration | Tenants & Licensing | 3 | 1 | yes |
| `ADM-392` | Subscription Tier Configuration | Tenants & Licensing | 3 | 2 | yes |
| `ADM-393` | Tier Included Allowances | Tenants & Licensing | 3 | 1 | yes |
| `ADM-394` | Commercial & Licensing Model Configuration | Tenants & Licensing | 3 | 1 | yes |
| `ADM-395` | Billable Unit, Minimum Guarantee & Enforcement Rules | Tenants & Licensing | 3 | 1 | yes |
| `ADM-396` | Overage Pricing & Capacity Packs | Tenants & Licensing | 3 | 2 | yes |
| `ADM-397` | Commercial Model & Rule Simulation | Tenants & Licensing | 3 | 1 | yes |
| `ADM-398` | Rule Versioning, Approval & Publication | Tenants & Licensing | 3 | 1 | yes |
| `ADM-399` | Recommended Package Overview | Tenants & Licensing | 3 | 1 | yes |
| `ADM-400` | Commercial Model & Tier Selection | Tenants & Licensing | 3 | 2 | yes |
| `ADM-401` | Module Marketplace | Tenants & Licensing | 3 | 1 | yes |
| `ADM-402` | AI Module & Package Recommendations | Tenants & Licensing | 3 | 1 | yes |
| `ADM-403` | Module Detail & Commercial Treatment | Tenants & Licensing | 3 | 1 | yes |
| `ADM-404` | Module Dependency & Compatibility Manager | Tenants & Licensing | 3 | 1 | yes |
| `ADM-405` | Add-Ons, Capacity & Commercial Options | Tenants & Licensing | 3 | 1 | yes |
| `ADM-406` | Commercial Package Simulator | Tenants & Licensing | 3 | 1 | yes |
| `ADM-407` | Package Review & Commercial Summary | Tenants & Licensing | 3 | 1 | yes |
| `ADM-408` | Final Package Approval & Handoff | Tenants & Licensing | 3 | 0 | yes |
| `ADM-409` | Purchase / Trial Journey Selection | Tenants & Licensing | 3 | 0 | yes |
| `ADM-410` | Contract & Billing Cycle Selection | Tenants & Licensing | 3 | 1 | yes |
| `ADM-411` | Billing & Legal Entity Information | Tenants & Licensing | 3 | 6 | yes |
| `ADM-412` | Payment Method & Settlement Setup | Tenants & Licensing | 1 | 6 | yes |
| `ADM-413` | Trial Configuration & Conversion Rules | Tenants & Licensing | 3 | 1 | yes |
| `ADM-414` | Order & Commercial Pricing Review | Tenants & Licensing | 3 | 1 | yes |
| `ADM-415` | Commercial Agreement, Billable Definition & Customer Acceptance | Tenants & Licensing | 3 | 1 | yes |
| `ADM-416` | Payment, Contract & Commercial Validation | Tenants & Licensing | 3 | 1 | yes |
| `ADM-417` | Subscription Confirmation & Commercial Activation | Tenants & Licensing | 3 | 1 | yes |
| `ADM-418` | Subscription Lifecycle & Trial-to-Paid Handoff | Tenants & Licensing | 3 | 1 | yes |
| `ADM-419` | Provisioning Command Center | Tenants & Licensing | 3 | 2 | yes |
| `ADM-420` | Tenant & Organization Provisioning | Tenants & Licensing | 3 | 5 | yes |
| `ADM-421` | Venue & Operational Structure Creation | Tenants & Licensing | 3 | 4 | yes |
| `ADM-422` | Administrator & Security Initialization | Tenants & Licensing | 3 | 7 | yes |
| `ADM-423` | License & Entitlement Activation | Tenants & Licensing | 3 | 1 | yes |
| `ADM-424` | Module Activation & Dependency Validation | Tenants & Licensing | 1 | 7 | yes |
| `ADM-425` | Venue Template Application | Tenants & Licensing | 3 | 4 | yes |
| `ADM-426` | Initial Configuration & Regional Defaults | Tenants & Licensing | 3 | 8 | yes |
| `ADM-427` | Provisioning Validation & Exception Management | Tenants & Licensing | 3 | 1 | yes |
| `ADM-449` | Usage & License Command Center | Tenants & Licensing | 3 | 1 | yes |
| `ADM-450` | Entitlement & License Inventory | Tenants & Licensing | 3 | 1 | yes |
| `ADM-451` | Commercial Consumption & Billable Event Metering | Tenants & Licensing | 3 | 1 | yes |
| `ADM-452` | Operational Usage & Threshold Monitor | Tenants & Licensing | 3 | 2 | yes |
| `ADM-453` | License Enforcement & Decision Engine | Tenants & Licensing | 3 | 1 | yes |
| `ADM-454` | Minimum Guarantee & Variable Consumption Monitor | Tenants & Licensing | 3 | 1 | yes |
| `ADM-455` | Overage, Capacity & Temporary Exception Management | Tenants & Licensing | 3 | 1 | yes |
| `ADM-456` | Usage Alerts, Reconciliation & Exception Center | Tenants & Licensing | 3 | 1 | yes |
| `ADM-457` | AI Usage Forecast & Commercial Optimization | Tenants & Licensing | 3 | 1 | yes |
| `ADM-458` | License, Metering & Commercial Synchronization Audit | Tenants & Licensing | 3 | 1 | yes |
| `ADM-459` | Billing & Commercial Command Center | Tenants & Licensing | 3 | 1 | yes |
| `ADM-460` | Billing Calculation & Charge Breakdown | Tenants & Licensing | 3 | 1 | yes |
| `ADM-461` | Consumption Reconciliation & Billing Approval | Tenants & Licensing | 3 | 2 | yes |
| `ADM-462` | Invoice & Payment Management | Tenants & Licensing | 3 | 4 | yes |
| `ADM-463` | Subscription & Commercial Change Management | Tenants & Licensing | 3 | 2 | yes |
| `ADM-464` | Renewal Management Center | Tenants & Licensing | 3 | 0 | yes |
| `ADM-465` | AI Upgrade, Downgrade & Commercial Right-Sizing | Tenants & Licensing | 3 | 2 | yes |
| `ADM-466` | Commercial Scenario Simulator | Tenants & Licensing | 3 | 1 | yes |
| `ADM-467` | Discount, Credit & Commercial Override Management | Tenants & Licensing | 3 | 4 | yes |
| `ADM-468` | Renewal Approval, Activation & Commercial Handoff | Tenants & Licensing | 3 | 1 | yes |
| `ADM-469` | AI Configuration Home & Start | Platform | 3 | 6 | yes |
| `ADM-470` | Setup Type & Business Intent Discovery | Platform | 3 | 7 | yes |
| `ADM-471` | Venue & Business Model Discovery | Platform | 3 | 6 | yes |
| `ADM-472` | Guided Question & Answer Workspace | Platform | 3 | 5 | yes |
| `ADM-473` | Product & Admission Model Discovery | Platform | 3 | 5 | yes |
| `ADM-474` | Operational Requirement Discovery | Platform | 3 | 5 | yes |
| `ADM-475` | Commercial Requirement Discovery | Platform | 3 | 5 | yes |
| `ADM-476` | Required, Recommended & Optional Decisions | Platform | 3 | 5 | yes |
| `ADM-477` | Missing Information & Clarification Center | Platform | 3 | 8 | yes |
| `ADM-478` | Configuration Blueprint & Dependency Map | Platform | 3 | 5 | yes |
| `ADM-479` | AI Configuration Build Command Center | Platform | 3 | 6 | yes |
| `ADM-480` | Venue & Organization Configuration | Platform | 3 | 6 | yes |
| `ADM-481` | Product Configuration Assistant | Platform | 3 | 6 | yes |
| `ADM-482` | Schedule, Capacity & Availability Configuration | Platform | 3 | 6 | yes |
| `ADM-483` | Pricing & Commercial Configuration | Platform | 3 | 6 | yes |
| `ADM-484` | Promotion, Bundle & Upsell Configuration | Platform | 3 | 6 | yes |
| `ADM-485` | Seating, Access & Operational Configuration | Platform | 3 | 6 | yes |
| `ADM-486` | Channel, Media & Fulfillment Configuration | Platform | 3 | 6 | yes |
| `ADM-487` | Cross-Module Conflict & Dependency Validation | Platform | 3 | 5 | yes |
| `ADM-488` | Configuration Preview & Impact Analysis | Platform | 3 | 5 | yes |
| `ADM-489` | AI Configuration Readiness Center | Platform | 3 | 7 | yes |
| `ADM-490` | Configuration Validation Results | Platform | 3 | 5 | yes |
| `ADM-491` | AI Recommendations & Best-Practice Review | Platform | 3 | 5 | yes |
| `ADM-492` | Configuration Approval Workflow | Platform | 3 | 6 | yes |
| `ADM-493` | AI Configuration Execution Center | Platform | 3 | 6 | yes |
| `ADM-494` | Execution Progress & Dependency Monitor | Platform | 3 | 7 | yes |
| `ADM-495` | Configuration Results & Object Mapping | Platform | 3 | 5 | yes |
| `ADM-496` | Configuration Change & Modification Assistant | Platform | 3 | 6 | yes |
| `ADM-497` | Configuration History, Versions & Rollback | Platform | 3 | 6 | yes |
| `ADM-498` | AI Configuration Audit & Governance | Platform | 3 | 5 | yes |
| `ADM-499` | Forecasting Command Center | Analytics | 3 | 6 | yes |
| `ADM-500` | Forecast Configuration & Forecasting Strategy | Analytics | 1 | 6 | yes |
| `ADM-501` | Forecast Data & Signal Configuration | Analytics | 3 | 6 | yes |
| `ADM-502` | Attendance & Visitation Forecast | Analytics | 3 | 6 | yes |
| `ADM-503` | Ticket, Product & Timeslot Demand Forecast | Analytics | 3 | 4 | yes |
| `ADM-504` | Channel & Booking Pace Forecast | Analytics | 3 | 4 | yes |
| `ADM-505` | Revenue & Commercial Forecast | Analytics | 3 | 4 | yes |
| `ADM-506` | Forecast Drivers, Confidence & Explainability | Analytics | 1 | 7 | yes |
| `ADM-507` | Forecast Scenario & What-If Simulator | Analytics | 3 | 6 | yes |
| `ADM-508` | Forecast Accuracy, Review & Publication Center | AI | 1 | 8 | yes |
| `ADM-509` | Operational Forecasting Command Center | Analytics | 3 | 5 | yes |
| `ADM-510` | Capacity & Occupancy Forecast | Analytics | 3 | 7 | yes |
| `ADM-511` | Attraction Utilization & Queue Forecast | Analytics | 3 | 6 | yes |
| `ADM-512` | Entry, Access & Guest Flow Forecast | Analytics | 3 | 5 | yes |
| `ADM-513` | Workforce Demand & Staffing Forecast | Analytics | 3 | 6 | yes |
| `ADM-514` | POS, Kiosk & Frontline Service Forecast | Analytics | 3 | 5 | yes |
| `ADM-515` | F&B, Retail & Inventory Demand Forecast | Analytics | 3 | 5 | yes |
| `ADM-516` | Resource, Equipment & Facility Requirement Forecast | Analytics | 3 | 5 | yes |
| `ADM-517` | Operational Scenario & Readiness Simulator | Analytics | 3 | 6 | yes |
| `ADM-518` | Operational Forecast Review, Recommendations & Handover | Analytics | 3 | 5 | yes |
| `ADM-519` | AI Governance Command Center | Platform | 3 | 8 | yes |
| `ADM-520` | AI Capability Registry & Ownership | Platform | 3 | 5 | yes |
| `ADM-521` | AI Risk Classification & Assessment | Platform | 3 | 5 | yes |
| `ADM-522` | AI Autonomy Level Configuration | Platform | 3 | 6 | yes |
| `ADM-523` | AI Action & Permission Policy Builder | Platform | 1 | 6 | yes |
| `ADM-524` | AI Data Access & Usage Policy | Platform | 3 | 7 | yes |
| `ADM-525` | Environment, Tenant & Scope Governance | Platform | 3 | 5 | yes |
| `ADM-526` | AI Policy Conflict, Exception & Override Management | Platform | 3 | 7 | yes |
| `ADM-527` | AI Policy Testing & Governance Simulation | Platform | 1 | 5 | yes |
| `ADM-528` | AI Governance Policy Publication & Effective Policy Map | Platform | 1 | 6 | yes |
| `ADM-529` | AI Human Oversight Command Center | Platform | 3 | 5 | yes |
| `ADM-530` | AI Approval Requirement & Routing Configuration | Platform | 3 | 9 | yes |
| `ADM-531` | AI Approval Review Workspace | Platform | 3 | 6 | yes |
| `ADM-532` | Conditional Approval & Approval Conditions | Platform | 3 | 7 | yes |
| `ADM-533` | Human Review, Challenge & AI Clarification Workspace | Platform | 3 | 6 | yes |
| `ADM-534` | Escalation, Delegation & Approval SLA Management | Platform | 3 | 9 | yes |
| `ADM-535` | Live AI Execution Oversight & Human Intervention | Platform | 3 | 8 | yes |
| `ADM-536` | Human Override & Manual Control Center | Platform | 3 | 10 | yes |
| `ADM-537` | Approval & Intervention History / Decision Timeline | Platform | 3 | 5 | yes |
| `ADM-538` | Human Oversight Workflow Simulator & Readiness Center | Platform | 3 | 5 | yes |
| `ADM-539` | AI Explainability & Audit Command Center | Platform | 3 | 4 | yes |
| `ADM-540` | AI Decision Explorer & Search | Platform | 3 | 5 | yes |
| `ADM-541` | AI Decision Explanation Workspace | Platform | 3 | 4 | yes |
| `ADM-542` | Data, Feature & Evidence Provenance | Platform | 3 | 4 | yes |
| `ADM-543` | Candidate, Rule & Decision Path Trace | Platform | 3 | 5 | yes |
| `ADM-544` | Model, Provider & AI Runtime Trace | Platform | 3 | 5 | yes |
| `ADM-545` | Governance, Approval & Human Decision Trace | Platform | 3 | 4 | yes |
| `ADM-546` | Execution & Business Outcome Trace | Platform | 3 | 5 | yes |
| `ADM-547` | AI Audit Record & Evidence Package | Platform | 3 | 5 | yes |
| `ADM-548` | AI Trace Investigation & Replay Simulator | Platform | 3 | 5 | yes |
| `ADM-549` | AI Governance Monitoring Command Center | Platform | 3 | 7 | yes |
| `ADM-550` | AI Risk Register & Risk Exposure Management | Platform | 3 | 5 | yes |
| `ADM-551` | AI Governance Control Library & Control Effectiveness | Platform | 3 | 5 | yes |
| `ADM-552` | AI Policy Compliance & Violation Monitoring | Platform | 3 | 5 | yes |
| `ADM-553` | AI Data, Privacy & Usage Compliance Monitoring | Platform | 3 | 5 | yes |
| `ADM-554` | AI Quality, Behavior & Governance Drift Monitoring | Platform | 1 | 9 | yes |
| `ADM-555` | AI Governance Alert & Detection Center | Platform | 3 | 6 | yes |
| `ADM-556` | AI Incident & Remediation Management | Platform | 1 | 9 | yes |
| `ADM-557` | AI Compliance, Assurance & Governance Reporting | Platform | 3 | 6 | yes |
| `ADM-558` | AI Governance Review, Action Plan & Continuous Improvement | Platform | 3 | 5 | yes |
| `ADM-619` | Reconciliation & Settlement Command Center | Commercial | 3 | 5 | yes |
| `ADM-699` | My Account & Security | Access & Identity | 1 | 9 | yes |
| `ADM-700` | Configuration Promotion | Releases & Environments | 2 | 6 | yes |

