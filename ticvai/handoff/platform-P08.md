# P08 Venue Management — platform

**Derived.** `python3 tools/derive-platform.py P08`. App `venue-management-web` · venue · web

| | |
|---|---|
| Screens | 1661 |
| Operations | 1839 |
| Contracts | 31 |
| Modules | 19 |
| Undrawn | 0 |
| Operations with no screen | 195 |
| Waves | wave1 61 · wave2 85 · wave3 1515 |

## Gaps

### 195 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `approveManualOverrideSupervisor` | access | PUT | Manual Override & Supervisor Approval |
| `getHardwareModelCertification` | access | GET | A reader model's certification and its test results |
| `listAccessChanges` | access | GET | Changes made to an entitlement's access |
| `listEntryExitRule` | access | GET | Entry, Exit & Re-entry Rules |
| `listEntryRulePoints` | access | GET | Which access points an admission rule covers |
| `listEntryTemporaryExit` | access | GET | Re-entry & Temporary Exit Journey |
| `setHardwareModelCertification` | access | PUT | Certify a reader model, or record that it failed |
| `setVirtualTicketCredential` | access | PUT | Virtual Ticket & Credential 360° Workspace |
| `verifyIdentity` | access | POST | Check the person presenting against the person entitled |
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
| … | | | 155 more |

### 8 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Access & Venue** — waves 1, 2, 3
- **Food & Beverage** — waves 1, 2
- **Guests & Marketing** — waves 1, 2
- **Orders & Money** — waves 1, 2, 3
- **People & Access Rights** — waves 1, 2, 3
- **Sell** — waves 1, 2, 3
- **Stock & Supply** — waves 1, 2
- **Venue Operations** — waves 1, 2, 3

## Modules

| Module | Screens | Waves |
|---|---|---|
| Access & Venue | 380 | 1, 2, 3 |
| Commercial | 368 | 3 |
| Rentals | 199 | 3 |
| Orders & Money | 157 | 1, 2, 3 |
| Engagement & Support | 120 | 3 |
| Sell | 111 | 1, 2, 3 |
| Games & Rides | 98 | 3 |
| Platform | 79 | 3 |
| Venue Operations | 45 | 1, 2, 3 |
| Setup & Go-Live | 21 | 3 |
| Catalogue | 20 | 3 |
| Stock & Supply | 16 | 1, 2 |
| People & Access Rights | 12 | 1, 2, 3 |
| Food & Beverage | 8 | 1, 2 |
| Partners | 8 | 3 |
| Operations | 7 | 3 |
| Transport | 7 | 2 |
| Guests & Marketing | 4 | 1, 2 |
| Setup | 1 | 3 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `ADM-038` | Communication Service Command Center | Platform | 3 | 1 | yes |
| `ADM-039` | Channel & Provider Configuration | Platform | 3 | 1 | yes |
| `ADM-040` | Sender Identity, Domain & Brand Configuration | Platform | 3 | 1 | yes |
| `ADM-041` | System Transactional Template Registry | Platform | 3 | 1 | yes |
| `ADM-042` | Business Event & Notification Trigger Mapping | Platform | 3 | 1 | yes |
| `ADM-043` | Routing, Priority, Throttling & Fallback Rules | Platform | 3 | 1 | yes |
| `ADM-044` | Consent, Preference & Communication Policy Enforcement | Platform | 3 | 1 | yes |
| `ADM-045` | Delivery Queue, Failure & Retry Management | Platform | 3 | 1 | yes |
| `ADM-046` | Provider Health, Usage & Cost Monitoring | Platform | 3 | 1 | yes |
| `ADM-047` | AI Delivery Optimization & Communication Platform Diagnostics | Platform | 3 | 2 | yes |
| `ADM-048` | Commercial Pricing Command Center | Commercial | 3 | 3 | yes |
| `ADM-049` | Price List Master Configuration | Commercial | 3 | 1 | yes |
| `ADM-050` | Price Category & Rate Type Library | Commercial | 3 | 2 | yes |
| `ADM-051` | Rate Structure Builder | Commercial | 3 | 1 | yes |
| `ADM-052` | Product & Service Price Assignment | Commercial | 3 | 1 | yes |
| `ADM-053` | Package, Bundle & Add-On Pricing | Commercial | 3 | 2 | yes |
| `ADM-054` | Market, Venue & Currency Pricing Structure | Commercial | 3 | 2 | yes |
| `ADM-055` | Price Hierarchy & Inheritance Configuration | Commercial | 3 | 1 | yes |
| `ADM-056` | Price List Templates, Clone & Reuse | Commercial | 3 | 2 | yes |
| `ADM-057` | Commercial Pricing Structure Validation | Commercial | 3 | 1 | yes |
| `ADM-058` | Pricing Rule Command Center | Commercial | 3 | 3 | yes |
| `ADM-059` | Customer Segment & Profile Pricing Rules | Commercial | 3 | 1 | yes |
| `ADM-060` | Membership & Loyalty Pricing Rules | Commercial | 3 | 1 | yes |
| `ADM-061` | Residency, Nationality & Market Pricing Rules | Commercial | 3 | 1 | yes |
| `ADM-062` | Channel-Based Pricing Rules | Commercial | 3 | 1 | yes |
| `ADM-063` | Location, Venue & Event Pricing Rules | Commercial | 3 | 1 | yes |
| `ADM-064` | Quantity, Group & Volume Pricing Rules | Commercial | 3 | 1 | yes |
| `ADM-065` | Effective Date, Season & Day-Based Pricing Rules | Commercial | 3 | 1 | yes |
| `ADM-066` | Timeslot, Performance & Time-of-Day Pricing Rules | Commercial | 3 | 1 | yes |
| `ADM-067` | Pricing Rule Priority, Conflict Resolution & Testing | Commercial | 3 | 3 | yes |
| `ADM-069` | Tax Profile & Jurisdiction Configuration | Commercial | 3 | 5 | yes |
| `ADM-070` | Tax Rule & Treatment Builder | Commercial | 3 | 1 | yes |
| `ADM-071` | Fee & Surcharge Library | Commercial | 3 | 2 | yes |
| `ADM-072` | Fee Applicability & Charging Rule Builder | Commercial | 3 | 1 | yes |
| `ADM-073` | Fee Waiver, Tax Exemption & Exception Rules | Commercial | 3 | 1 | yes |
| `ADM-074` | Price Calculation Sequence & Formula Engine | Commercial | 3 | 2 | yes |
| `ADM-075` | Currency Precision, Rounding & Monetary Rules | Commercial | 3 | 2 | yes |
| `ADM-076` | Price Breakdown, Calculation Simulation & Explainability | Commercial | 3 | 1 | yes |
| `ADM-077` | Calculation Validation, Reconciliation & Service Interface | Commercial | 3 | 4 | yes |
| `ADM-078` | Pricing Governance Command Center | Commercial | 3 | 2 | yes |
| `ADM-079` | Pricing Change Request & Workspace | Commercial | 3 | 3 | yes |
| `ADM-080` | Bulk Pricing Update, Import & Mass Maintenance | Commercial | 3 | 1 | yes |
| `ADM-081` | Pricing Version & Baseline Management | Commercial | 3 | 1 | yes |
| `ADM-082` | Pricing Change Impact Analysis | Commercial | 3 | 2 | yes |
| `ADM-083` | Pricing Approval Workflow & Authority Matrix | Commercial | 3 | 2 | yes |
| `ADM-084` | Pricing Publication & Effective-Date Scheduler | Commercial | 3 | 1 | yes |
| `ADM-085` | Pricing Distribution, Synchronization & Publication Monitor | Commercial | 3 | 1 | yes |
| `ADM-086` | Pricing Rollback & Emergency Control Center | Commercial | 3 | 3 | yes |
| `ADM-087` | Pricing History, Audit & Compliance Explorer | Commercial | 3 | 1 | yes |
| `ADM-088` | Dynamic Pricing Strategy Command Center | Commercial | 3 | 2 | yes |
| `ADM-089` | Dynamic Pricing Strategy Builder | Commercial | 3 | 3 | yes |
| `ADM-090` | Demand, Occupancy & Availability Rule Builder | Commercial | 3 | 2 | yes |
| `ADM-091` | Booking Velocity & Time-to-Event Rule Builder | Commercial | 3 | 2 | yes |
| `ADM-092` | Seasonal, Calendar, Day & Timeslot Dynamic Rules | Commercial | 3 | 2 | yes |
| `ADM-093` | Channel, Customer Segment & Location Dynamic Rules | Commercial | 3 | 1 | yes |
| `ADM-094` | Dynamic Price Bands, Ladders & Adjustment Matrix | Commercial | 3 | 2 | yes |
| `ADM-095` | Dynamic Pricing Guardrails & Commercial Protection | Commercial | 3 | 2 | yes |
| `ADM-096` | Dynamic Pricing Automation Policy & Control | Commercial | 3 | 2 | yes |
| `ADM-097` | Rule Priority, Conflict Resolution & Dynamic Pricing Test Console | Commercial | 3 | 0 | yes |
| `ADM-098` | AI Pricing Intelligence Command Center | Commercial | 3 | 1 | yes |
| `ADM-099` | Internal Demand & Booking Signal Hub | Commercial | 3 | 1 | yes |
| `ADM-100` | Weather Intelligence & Demand Impact Configuration | Commercial | 3 | 2 | yes |
| `ADM-101` | Nearby Event, Exhibition & Local Demand Intelligence | Commercial | 3 | 2 | yes |
| `ADM-102` | Competitor Pricing & Market Position Intelligence | Commercial | 3 | 2 | yes |
| `ADM-103` | Market, Tourism, Holiday & Contextual Signal Hub | Commercial | 3 | 2 | yes |
| `ADM-104` | AI Demand Forecasting & Booking Curve Studio | Commercial | 3 | 1 | yes |
| `ADM-105` | Price Elasticity & Revenue Response Intelligence | Commercial | 3 | 1 | yes |
| `ADM-106` | AI Pricing Recommendation & Explainability Center | Commercial | 3 | 2 | yes |
| `ADM-107` | AI Signal Registry, Data Quality & Model Governance | Commercial | 3 | 2 | yes |
| `ADM-108` | Revenue Optimization Command Center | Commercial | 3 | 1 | yes |
| `ADM-109` | Pricing Simulation Studio | Commercial | 3 | 1 | yes |
| `ADM-110` | Scenario Modeling & What-If Analysis | Commercial | 3 | 1 | yes |
| `ADM-111` | A/B Pricing Experiment Studio | Commercial | 3 | 1 | yes |
| `ADM-112` | Revenue & Demand Impact Forecasting | Commercial | 3 | 1 | yes |
| `ADM-113` | AI Recommendation Review & Decision Queue | Commercial | 3 | 2 | yes |
| `ADM-114` | Automation Policy & Autonomous Pricing Orchestrator | Commercial | 3 | 2 | yes |
| `ADM-115` | Live Dynamic Price Execution & Deployment Monitor | Commercial | 3 | 1 | yes |
| `ADM-116` | Dynamic Pricing Performance & Optimization Analytics | Commercial | 3 | 1 | yes |
| `ADM-117` | AI Learning, Model Performance & Optimization Feedback | Commercial | 3 | 2 | yes |
| `ADM-118` | Product Lifecycle Command Center | Catalogue | 3 | 1 | yes |
| `ADM-119` | Product Creation Workspace | Catalogue | 3 | 1 | yes |
| `ADM-120` | Lifecycle Status & Workflow Configuration | Catalogue | 3 | 1 | yes |
| `ADM-121` | Bulk Product Creation & Catalogue Import | Catalogue | 3 | 0 | yes |
| `ADM-122` | Product Import / Export & Environment Transfer | Catalogue | 3 | 1 | yes |
| `ADM-123` | Product Context, Ownership & Assignment | Catalogue | 3 | 1 | yes |
| `ADM-124` | Channel Publication & Availability | Catalogue | 3 | 1 | yes |
| `ADM-125` | Publication & Activation Scheduler | Catalogue | 3 | 2 | yes |
| `ADM-126` | Product Duplication & Template Library | Catalogue | 3 | 2 | yes |
| `ADM-127` | AI Catalogue Builder & Configuration Review | Catalogue | 3 | 1 | yes |
| `ADM-128` | Product Governance Command Center | Catalogue | 3 | 2 | yes |
| `ADM-129` | Approval Workflow Designer | Catalogue | 3 | 2 | yes |
| `ADM-130` | Approval Review & Decision Workspace | Catalogue | 3 | 2 | yes |
| `ADM-131` | Product Version Management | Catalogue | 3 | 1 | yes |
| `ADM-132` | Rollback & Recovery Management | Catalogue | 3 | 2 | yes |
| `ADM-133` | Change Impact Analysis | Catalogue | 3 | 2 | yes |
| `ADM-134` | Change Propagation & Dependency Control | Catalogue | 3 | 2 | yes |
| `ADM-135` | Product Retirement, Suspension & Archive | Catalogue | 3 | 1 | yes |
| `ADM-136` | Product Audit Trail & Change History | Catalogue | 3 | 1 | yes |
| `ADM-137` | Governance Risk, AI Monitoring & Control Center | Catalogue | 3 | 2 | yes |
| `ADM-138` | Promotion Command Center Dashboard | Commercial | 3 | 2 | yes |
| `ADM-139` | Promotion & Campaign Directory | Commercial | 3 | 5 | yes |
| `ADM-140` | Promotion Overview | Commercial | 3 | 2 | yes |
| `ADM-141` | Promotion Lifecycle & Status Manager | Commercial | 3 | 5 | yes |
| `ADM-142` | Campaign Calendar & Timeline | Commercial | 3 | 2 | yes |
| `ADM-143` | Promotion Channel & Publication Monitor | Commercial | 3 | 1 | yes |
| `ADM-144` | Promotion Alerts & Exception Center | Commercial | 3 | 1 | yes |
| `ADM-145` | Promotion Approval Inbox | Commercial | 3 | 3 | yes |
| `ADM-146` | Promotion Health & Performance Monitor | Commercial | 3 | 2 | yes |
| `ADM-147` | Promotion Audit, Activity & Version History | Commercial | 3 | 1 | yes |
| `ADM-148` | Promotion Rule Builder | Commercial | 3 | 1 | yes |
| `ADM-149` | Percentage & Fixed Discount Configurator | Commercial | 3 | 1 | yes |
| `ADM-150` | Cart & Transaction Threshold Rules | Commercial | 3 | 1 | yes |
| `ADM-151` | Volume, Bulk & Tier Discount Configurator | Commercial | 3 | 1 | yes |
| `ADM-152` | Time-Based & Seasonal Discount Rules | Commercial | 3 | 1 | yes |
| `ADM-153` | Customer, Membership & Segment Discount Rules | Commercial | 3 | 1 | yes |
| `ADM-154` | Payment Method, Bank & Partner Discount Rules | Commercial | 3 | 1 | yes |
| `ADM-155` | Special Price & Guest Offer Configurator | Commercial | 3 | 1 | yes |
| `ADM-156` | Discount Limits, Guardrails & Commercial Controls | Commercial | 3 | 1 | yes |
| `ADM-157` | Rule Test, Simulation & AI Recommendation Workspace | Commercial | 3 | 2 | yes |
| `ADM-158` | Coupon & Promo Code Command Center | Commercial | 3 | 1 | yes |
| `ADM-159` | Coupon & Promo Code Builder | Commercial | 3 | 1 | yes |
| `ADM-160` | Unique Code Generation & Batch Manager | Commercial | 3 | 3 | yes |
| `ADM-161` | Code Eligibility & Restriction Manager | Commercial | 3 | 1 | yes |
| `ADM-162` | Usage, Capacity & Frequency Control | Commercial | 3 | 1 | yes |
| `ADM-163` | Validity, Date & Time Control | Commercial | 3 | 1 | yes |
| `ADM-164` | Code Distribution & Assignment Manager | Commercial | 3 | 2 | yes |
| `ADM-165` | Redemption Monitor & Code Lookup | Commercial | 3 | 1 | yes |
| `ADM-166` | Code Security, Fraud & Exception Center | Commercial | 3 | 1 | yes |
| `ADM-167` | Redemption Analytics, Audit & AI Optimization | Commercial | 3 | 1 | yes |
| `ADM-168` | Advanced Offer Command Center | Commercial | 3 | 2 | yes |
| `ADM-169` | Buy X Get Y / BOGO Rule Builder | Commercial | 3 | 0 | yes |
| `ADM-170` | Multi-Buy & Quantity Offer Configurator | Commercial | 3 | 1 | yes |
| `ADM-171` | Cheapest / Lowest-Value Item Promotion | Commercial | 3 | 1 | yes |
| `ADM-172` | Fixed-Price & “N for X” Offer Builder | Commercial | 3 | 0 | yes |
| `ADM-173` | Gift, Free Product & Added-Value Offer Builder | Commercial | 3 | 0 | yes |
| `ADM-174` | Cross-Category Promotion Builder | Commercial | 3 | 0 | yes |
| `ADM-175` | Reward Selection, Substitution & Customer Choice | Commercial | 3 | 1 | yes |
| `ADM-176` | Advanced Offer Guardrails & Conflict Controls | Commercial | 3 | 1 | yes |
| `ADM-177` | Offer Simulation, Basket Trace & AI Optimization | Commercial | 3 | 3 | yes |
| `ADM-178` | Bundle & Combo Command Center | Commercial | 3 | 1 | yes |
| `ADM-179` | Bundle Definition & Setup | Commercial | 3 | 1 | yes |
| `ADM-180` | Bundle Component Builder | Commercial | 3 | 1 | yes |
| `ADM-181` | Guest Choice & Build-Your-Own Bundle Designer | Commercial | 3 | 1 | yes |
| `ADM-182` | Bundle Pricing & Commercial Model | Commercial | 3 | 1 | yes |
| `ADM-183` | Bundle Availability, Capacity & Validation | Commercial | 3 | 1 | yes |
| `ADM-184` | Bundle Validity, Scheduling & Redemption Rules | Commercial | 3 | 1 | yes |
| `ADM-185` | Partner & External Product Bundle Manager | Commercial | 3 | 3 | yes |
| `ADM-186` | Revenue Allocation, Cost & Settlement Rules | Commercial | 3 | 1 | yes |
| `ADM-187` | Bundle Preview, Simulation & AI Recommendation | Commercial | 3 | 2 | yes |
| `ADM-188` | Dynamic Bundle Operations Command Center | Commercial | 3 | 3 | yes |
| `ADM-189` | Component Inventory & Availability Matrix | Commercial | 3 | 2 | yes |
| `ADM-190` | Bundle Sellability & Dependency Rule Engine | Commercial | 3 | 1 | yes |
| `ADM-191` | Capacity Pool & Reservation Manager | Commercial | 3 | 3 | yes |
| `ADM-192` | Dynamic Component Substitution Engine | Commercial | 3 | 1 | yes |
| `ADM-193` | Dynamic Bundle Rule & Composition Engine | Commercial | 3 | 1 | yes |
| `ADM-194` | Real-Time Availability & Checkout Validation | Commercial | 3 | 1 | yes |
| `ADM-195` | Bundle Availability by Channel, Venue & Partner | Commercial | 3 | 3 | yes |
| `ADM-196` | Bundle Availability Forecast, Alerts & Recovery | Commercial | 3 | 1 | yes |
| `ADM-197` | Dynamic Bundle Simulation & AI Optimization | Commercial | 3 | 3 | yes |
| `ADM-198` | Targeting & Eligibility Command Center | Commercial | 3 | 1 | yes |
| `ADM-199` | Eligibility Rule Builder | Commercial | 3 | 0 | yes |
| `ADM-200` | CRM & Customer Segment Manager | Commercial | 3 | 1 | yes |
| `ADM-201` | Membership, Loyalty & Guest Eligibility | Commercial | 3 | 1 | yes |
| `ADM-202` | Behavioral & Transaction Targeting | Commercial | 3 | 1 | yes |
| `ADM-203` | Context, Location, Channel & Time Targeting | Commercial | 3 | 1 | yes |
| `ADM-204` | Partner, B2B & Payment Eligibility | Commercial | 3 | 1 | yes |
| `ADM-205` | Audience Preview, Reach & Eligibility Simulator | Commercial | 3 | 1 | yes |
| `ADM-206` | Targeting Conflict, Frequency & Exclusion Controls | Commercial | 3 | 1 | yes |
| `ADM-207` | AI Audience Discovery & Targeting Optimization | Commercial | 3 | 1 | yes |
| `ADM-208` | Stacking & Conflict Command Center | Commercial | 3 | 1 | yes |
| `ADM-209` | Promotion Priority & Hierarchy Manager | Commercial | 3 | 1 | yes |
| `ADM-210` | Promotion Stacking Rule Builder | Commercial | 3 | 1 | yes |
| `ADM-211` | Promotion Exclusion & Compatibility Matrix | Commercial | 3 | 1 | yes |
| `ADM-212` | Discount Calculation & Application Sequence | Commercial | 3 | 1 | yes |
| `ADM-213` | Best Offer & Customer Benefit Resolver | Commercial | 3 | 1 | yes |
| `ADM-214` | Discount Cap & Maximum Benefit Controller | Commercial | 3 | 1 | yes |
| `ADM-215` | Conflict Detection & Resolution Center | Commercial | 3 | 1 | yes |
| `ADM-216` | Promotion Decision Trace & Transaction Explainer | Commercial | 3 | 1 | yes |
| `ADM-217` | Conflict Simulation & AI Optimization | Commercial | 3 | 1 | yes |
| `ADM-218` | Campaign Governance & Budget Command Center | Commercial | 3 | 1 | yes |
| `ADM-219` | Campaign Budget & Financial Limit Setup | Commercial | 3 | 4 | yes |
| `ADM-220` | Redemption, Discount & Exposure Limit Manager | Commercial | 3 | 1 | yes |
| `ADM-221` | Budget Consumption & Forecast Monitor | Commercial | 3 | 1 | yes |
| `ADM-222` | Threshold Actions & Automatic Suspension | Commercial | 3 | 1 | yes |
| `ADM-223` | Campaign Approval Workflow Designer | Commercial | 3 | 2 | yes |
| `ADM-224` | Approval Inbox & Decision Workspace | Commercial | 3 | 2 | yes |
| `ADM-225` | Campaign Financial & Commercial Simulator | Commercial | 3 | 1 | yes |
| `ADM-226` | Campaign Experiment & A/B Test Manager | Commercial | 3 | 2 | yes |
| `ADM-227` | Governance Audit, AI Risk & Launch Readiness | Commercial | 3 | 1 | yes |
| `ADM-228` | Promotion Performance Command Center | Commercial | 3 | 3 | yes |
| `ADM-229` | Campaign & Promotion Performance Explorer | Commercial | 3 | 4 | yes |
| `ADM-230` | Redemption, Conversion & Funnel Analytics | Commercial | 3 | 1 | yes |
| `ADM-231` | Discount, Margin & Profitability Analytics | Commercial | 3 | 1 | yes |
| `ADM-232` | Bundle, BOGO & Advanced Offer Analytics | Commercial | 3 | 1 | yes |
| `ADM-233` | Upsell, Cross-Sell & Attach-Rate Analytics | Commercial | 3 | 1 | yes |
| `ADM-234` | Customer, Segment, Channel & Partner Analytics | Commercial | 3 | 1 | yes |
| `ADM-235` | Incrementality, Attribution & Cannibalization Analysis | Commercial | 3 | 1 | yes |
| `ADM-236` | AI Optimization & Next-Best-Action Center | Commercial | 3 | 1 | yes |
| `ADM-237` | Executive Promotion Intelligence & Reporting Studio | Commercial | 3 | 1 | yes |
| `ADM-238` | Rules & Workflow Command Center | Platform | 3 | 1 | yes |
| `ADM-239` | Visual Business Rule Builder | Platform | 3 | 1 | yes |
| `ADM-240` | Conditions, Decision Logic & Decision Tables | Platform | 3 | 1 | yes |
| `ADM-241` | Visual Workflow Designer | Platform | 3 | 1 | yes |
| `ADM-242` | Approval Matrix & Multi-Level Approval Configuration | Platform | 3 | 0 | yes |
| `ADM-243` | Roles, Authority, Delegation & Approval Limits | Platform | 3 | 3 | yes |
| `ADM-244` | SLA, Escalation, Reminder & Timeout Rules | Platform | 3 | 2 | yes |
| `ADM-245` | Trigger, Action & Cross-Module Orchestration Configuration | Platform | 3 | 1 | yes |
| `ADM-246` | Workflow Testing, Simulation & Impact Analysis | Platform | 3 | 1 | yes |
| `ADM-247` | Versioning, Governance, Approval & Publication | Platform | 3 | 3 | yes |
| `ADM-248` | Workflow Operations Command Center | Platform | 3 | 1 | yes |
| `ADM-249` | Unified Approval Inbox & Decision Workspace | Platform | 3 | 0 | yes |
| `ADM-250` | Workflow Instance Monitor & Process Timeline | Platform | 3 | 2 | yes |
| `ADM-251` | Workflow Exception, Failure & Recovery Center | Platform | 3 | 2 | yes |
| `ADM-252` | SLA, Escalation & Bottleneck Monitor | Platform | 3 | 0 | yes |
| `ADM-253` | Automation Execution & Autonomous Action Monitor | Platform | 3 | 1 | yes |
| `ADM-254` | Cross-Module Orchestration Monitor | Platform | 3 | 1 | yes |
| `ADM-255` | Workflow Analytics & Process Performance | Platform | 3 | 1 | yes |
| `ADM-256` | Process Optimization & Automation Opportunity Center | Platform | 3 | 1 | yes |
| `ADM-257` | AI Workflow Intelligence & Autonomous Governance Center | Platform | 3 | 1 | yes |
| `ADM-258` | Sales Channel Command Center | Commercial | 3 | 3 | yes |
| `ADM-259` | Channel Creation & Profile Configuration | Commercial | 3 | 1 | yes |
| `ADM-260` | Product & Catalogue Assignment | Commercial | 3 | 1 | yes |
| `ADM-261` | Channel Pricing & Commercial Profile Assignment | Commercial | 3 | 1 | yes |
| `ADM-262` | Inventory, Capacity & Channel Allocation | Commercial | 3 | 1 | yes |
| `ADM-263` | Channel Sales Schedule & Availability Windows | Commercial | 3 | 2 | yes |
| `ADM-264` | Customer & Eligibility Rules by Channel | Commercial | 3 | 2 | yes |
| `ADM-265` | Channel Sales Rules, Limits & Restrictions | Commercial | 3 | 2 | yes |
| `ADM-266` | Channel Fees, Payment & Fulfillment Configuration | Commercial | 3 | 1 | yes |
| `ADM-267` | Channel Publication, Readiness & AI Validation | Commercial | 3 | 1 | yes |
| `ADM-268` | Channel Operations Command Center | Commercial | 3 | 2 | yes |
| `ADM-269` | Channel Connection & Integration Manager | Commercial | 3 | 3 | yes |
| `ADM-270` | Product, Price & Availability Synchronization | Commercial | 3 | 2 | yes |
| `ADM-271` | Real-Time Channel Availability & Inventory Monitor | Commercial | 3 | 2 | yes |
| `ADM-272` | Channel Allocation & Rebalancing Operations | Commercial | 3 | 2 | yes |
| `ADM-273` | Channel Exceptions, Incidents & Recovery | Commercial | 3 | 3 | yes |
| `ADM-274` | Channel Performance & Commercial Analytics | Commercial | 3 | 1 | yes |
| `ADM-275` | Channel Audit, Logs & Transaction Traceability | Commercial | 3 | 1 | yes |
| `ADM-276` | Channel Governance, SLA & Partner Control | Commercial | 3 | 1 | yes |
| `ADM-277` | AI Channel Optimization & Intelligence Center | Commercial | 3 | 3 | yes |
| `ADM-278` | Resale Marketplace Command Center | Commercial | 3 | 5 | yes |
| `ADM-279` | Resale Eligibility Rule Configuration | Commercial | 3 | 1 | yes |
| `ADM-280` | Resale Policy & Marketplace Settings | Commercial | 3 | 3 | yes |
| `ADM-281` | Listing Creation & Seller Configuration | Commercial | 3 | 2 | yes |
| `ADM-282` | Resale Pricing & Price Guardrails | Commercial | 3 | 3 | yes |
| `ADM-283` | Resale Fees, Commission & Seller Proceeds | Commercial | 3 | 4 | yes |
| `ADM-284` | Listing Approval & Moderation | Commercial | 3 | 2 | yes |
| `ADM-285` | Resale Inventory & Availability Management | Commercial | 3 | 1 | yes |
| `ADM-286` | Listing Lifecycle, Expiry & Cancellation | Commercial | 3 | 1 | yes |
| `ADM-287` | AI Resale Configuration & Marketplace Recommendations | Commercial | 3 | 2 | yes |
| `ADM-288` | Resale Operations Command Center | Commercial | 3 | 2 | yes |
| `ADM-289` | Buyer Purchase & Resale Order Management | Commercial | 3 | 1 | yes |
| `ADM-290` | Ticket Ownership Transfer Management | Commercial | 3 | 1 | yes |
| `ADM-291` | Credential Revocation & Regeneration | Commercial | 3 | 1 | yes |
| `ADM-292` | Resale Fraud & Duplicate Sale Protection | Commercial | 3 | 1 | yes |
| `ADM-293` | Capacity & Inventory Reconciliation | Commercial | 3 | 1 | yes |
| `ADM-294` | Seller Settlement & Payout Management | Commercial | 3 | 3 | yes |
| `ADM-295` | Refunds, Disputes & Resale Exceptions | Commercial | 3 | 3 | yes |
| `ADM-296` | Resale Audit & Ownership History | Commercial | 3 | 2 | yes |
| `ADM-297` | Resale Analytics & AI Intelligence | Commercial | 3 | 2 | yes |
| `ADM-298` | My Tickets & Resale Marketplace Entry | Commercial | 3 | 1 | yes |
| `ADM-299` | Resale Eligibility & Ticket Selection | Commercial | 3 | 1 | yes |
| `ADM-300` | Create Listing & Resale Price Selection | Commercial | 3 | 1 | yes |
| `ADM-301` | Fees, Seller Proceeds & Listing Confirmation | Commercial | 3 | 1 | yes |
| `ADM-302` | My Resale Listings & Seller Dashboard | Commercial | 3 | 1 | yes |
| `ADM-303` | Official Resale Marketplace & Buyer Discovery | Commercial | 3 | 1 | yes |
| `ADM-304` | Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience | Commercial | 3 | 1 | yes |
| `ADM-305` | Buyer Checkout, Inventory Hold & Secure Payment | Commercial | 3 | 1 | yes |
| `ADM-306` | Resale Confirmation, Ownership Transfer & Ticket Delivery | Commercial | 3 | 1 | yes |
| `ADM-307` | White-Label Marketplace Deployment & Experience Architecture | Commercial | 3 | 1 | yes |
| `ADM-308` | Upgrade & Conversion Command Center | Commercial | 3 | 1 | yes |
| `ADM-309` | Upgrade & Conversion Path Builder | Commercial | 3 | 1 | yes |
| `ADM-310` | Upgrade Eligibility & Qualification Rules | Commercial | 3 | 1 | yes |
| `ADM-311` | Upgrade Timing, Usage & Ticket Status Rules | Commercial | 3 | 1 | yes |
| `ADM-312` | Upgrade Financial Treatment & Price Difference Rules | Commercial | 3 | 1 | yes |
| `ADM-313` | Pro-Rata, Residual Value & Entitlement Credit Configuration | Commercial | 3 | 1 | yes |
| `ADM-314` | Person-Type, Product & Entitlement Conversion Rules | Commercial | 3 | 1 | yes |
| `ADM-315` | Bulk, Group & Assisted Upgrade Operations | Commercial | 3 | 1 | yes |
| `ADM-316` | Upgrade Execution, Credential Regeneration & Channel Controls | Commercial | 3 | 2 | yes |
| `ADM-317` | Upgrade History, Exception Management & Audit Explorer | Commercial | 3 | 1 | yes |
| `ADM-319` | Approval Workflow Library | Platform | 3 | 2 | yes |
| `ADM-320` | Create Approval Workflow | Platform | 3 | 1 | yes |
| `ADM-322` | Approval Stage Configuration | Platform | 3 | 1 | yes |
| `ADM-323` | Condition & Decision Rule Builder | Platform | 3 | 2 | yes |
| `ADM-324` | Approval Sequence & Parallel Routing | Platform | 3 | 1 | yes |
| `ADM-325` | Workflow Outcome & Action Configuration | Platform | 3 | 1 | yes |
| `ADM-326` | Workflow Validation & Simulation | Platform | 3 | 1 | yes |
| `ADM-327` | Workflow Publication & Lifecycle | Platform | 3 | 2 | yes |
| `ADM-328` | Workflow Versioning & Change History | Platform | 3 | 1 | yes |
| `ADM-329` | Approval Matrix Command Center | Platform | 3 | 1 | yes |
| `ADM-330` | Approval Authority Matrix | Platform | 3 | 1 | yes |
| `ADM-331` | Organizational Hierarchy Routing | Platform | 3 | 1 | yes |
| `ADM-332` | Department-Based Approval Matrix | Platform | 3 | 1 | yes |
| `ADM-333` | Venue & Tenant Approval Matrix | Platform | 3 | 1 | yes |
| `ADM-334` | Value & Threshold Routing | Platform | 3 | 1 | yes |
| `ADM-335` | Risk-Based & Conditional Routing | Platform | 3 | 1 | yes |
| `ADM-336` | Approver Group & Decision Policy | Platform | 3 | 1 | yes |
| `ADM-337` | Routing Simulator & Conflict Detection | Platform | 3 | 2 | yes |
| `ADM-338` | AI Routing Advisor & Matrix Optimization | Platform | 3 | 1 | yes |
| `ADM-339` | Governance & Compliance Command Center | Platform | 3 | 2 | yes |
| `ADM-340` | Segregation of Duties Policy Manager | Platform | 3 | 1 | yes |
| `ADM-341` | Four-Eyes & Dual-Control Policy | Platform | 3 | 2 | yes |
| `ADM-342` | Authentication & MFA Policy Manager | Platform | 3 | 7 | yes |
| `ADM-343` | Sensitive Action Confirmation | Platform | 3 | 2 | yes |
| `ADM-344` | Digital Signature Management | Platform | 3 | 0 | yes |
| `ADM-345` | Immutable Approval Record & Tamper Detection | Platform | 3 | 1 | yes |
| `ADM-346` | Approval Record Retention Policy | Platform | 3 | 3 | yes |
| `ADM-347` | Regulatory Audit & Evidence Center | Platform | 3 | 1 | yes |
| `ADM-348` | Governance Risk & AI Compliance Advisor | Platform | 3 | 1 | yes |
| `ADM-349` | Approval Integration Command Center | Platform | 3 | 3 | yes |
| `ADM-350` | Module Integration Registry | Platform | 3 | 1 | yes |
| `ADM-351` | Approval API Management | Platform | 3 | 3 | yes |
| `ADM-352` | Workflow Event Framework | Platform | 3 | 2 | yes |
| `ADM-353` | Webhook Configuration & Subscription Manager | Platform | 3 | 0 | yes |
| `ADM-354` | External Workflow System Integration | Platform | 3 | 3 | yes |
| `ADM-355` | Data & Workflow Mapping Studio | Platform | 3 | 1 | yes |
| `ADM-356` | Integration Security & Access Control | Platform | 3 | 3 | yes |
| `ADM-357` | Integration Monitoring, Error & Retry Center | Platform | 3 | 2 | yes |
| `ADM-358` | Integration Analytics & AI Health Advisor | Platform | 3 | 1 | yes |
| `ADM-359` | Approval Executive KPI Dashboard | Platform | 3 | 1 | yes |
| `ADM-360` | Approval Volume & Outcome Analytics | Platform | 3 | 1 | yes |
| `ADM-361` | Approval Processing Time Analytics | Platform | 3 | 1 | yes |
| `ADM-362` | Bottleneck Analysis & Heatmap | Platform | 3 | 1 | yes |
| `ADM-363` | Approval Trend & Comparative Analytics | Platform | 3 | 1 | yes |
| `ADM-364` | Approver & Team Performance Analytics | Platform | 3 | 1 | yes |
| `ADM-365` | Risk & Governance Analytics | Platform | 3 | 2 | yes |
| `ADM-366` | AI Approval Intelligence Center | Platform | 3 | 2 | yes |
| `ADM-367` | AI Optimization & What-If Simulator | Platform | 3 | 1 | yes |
| `ADM-368` | AI Governance Executive Advisor | Platform | 3 | 1 | yes |
| `ADM-559` | Payment Command Center | Commercial | 3 | 2 | yes |
| `ADM-560` | Payment Method Catalogue | Commercial | 3 | 2 | yes |
| `ADM-561` | Payment Method Configuration | Commercial | 3 | 2 | yes |
| `ADM-562` | Channel & Touchpoint Payment Configuration | Commercial | 3 | 2 | yes |
| `ADM-563` | Venue, Location & Business Unit Payment Assignment | Commercial | 3 | 2 | yes |
| `ADM-564` | Currency & Payment Currency Configuration | Commercial | 3 | 2 | yes |
| `ADM-565` | Payment Eligibility & Availability Rule Builder | Commercial | 3 | 2 | yes |
| `ADM-566` | Payment Fees, Surcharges & Commercial Rules | Commercial | 3 | 2 | yes |
| `ADM-567` | Payment Policy, Governance & Approval Manager | Commercial | 3 | 4 | yes |
| `ADM-568` | Payment Configuration Simulator & Validation Center | Commercial | 3 | 2 | yes |
| `ADM-569` | Payment Orchestration Command Center | Commercial | 3 | 2 | yes |
| `ADM-570` | Gateway, PSP & Acquirer Directory | Commercial | 3 | 2 | yes |
| `ADM-571` | Provider Connection & Adapter Configuration | Commercial | 3 | 3 | yes |
| `ADM-572` | Gateway Capability & Payment Method Mapping | Commercial | 3 | 1 | yes |
| `ADM-573` | Payment Routing Rule Builder | Commercial | 3 | 2 | yes |
| `ADM-574` | Routing Strategy, Priority & Load Distribution | Commercial | 3 | 2 | yes |
| `ADM-575` | Failover, Retry & Resilience Manager | Commercial | 3 | 1 | yes |
| `ADM-576` | Provider Health, SLA & Performance Monitor | Commercial | 3 | 1 | yes |
| `ADM-577` | Provider Cost, Commercial & Routing Economics | Commercial | 3 | 1 | yes |
| `ADM-578` | Payment Routing Simulator, Decision Trace & AI Advisor | Commercial | 3 | 2 | yes |
| `ADM-579` | Terminal & Card-Present Command Center | Commercial | 3 | 1 | yes |
| `ADM-580` | Payment Terminal & Device Inventory | Commercial | 3 | 4 | yes |
| `ADM-581` | Terminal Provisioning & Device Configuration | Commercial | 3 | 2 | yes |
| `ADM-582` | POS, Kiosk & Terminal Assignment Manager | Commercial | 3 | 1 | yes |
| `ADM-583` | EMV & Card-Present Processing Configuration | Commercial | 3 | 2 | yes |
| `ADM-584` | Payment Server & Terminal Connectivity Manager | Commercial | 3 | 1 | yes |
| `ADM-585` | Card-Present Transaction Monitor & Operations | Commercial | 3 | 1 | yes |
| `ADM-586` | Degraded, Offline & Store-and-Forward Manager | Commercial | 3 | 2 | yes |
| `ADM-587` | Terminal Health, Maintenance & Incident Center | Commercial | 3 | 5 | yes |
| `ADM-588` | Terminal Simulator, Certification & AI Operations Advisor | Commercial | 3 | 3 | yes |
| `ADM-589` | Digital Payments Command Center | Commercial | 3 | 1 | yes |
| `ADM-590` | Digital & Alternative Payment Method Manager | Commercial | 3 | 2 | yes |
| `ADM-591` | Digital Wallet & Mobile Payment Configuration | Commercial | 3 | 2 | yes |
| `ADM-592` | Payment Link Builder & Configuration | Commercial | 3 | 1 | yes |
| `ADM-593` | Payment Link Distribution & Customer Journey Manager | Commercial | 3 | 2 | yes |
| `ADM-594` | Hosted Checkout, Redirect & Return Flow Configuration | Commercial | 3 | 1 | yes |
| `ADM-595` | Digital Payment Session & Transaction Monitor | Commercial | 3 | 1 | yes |
| `ADM-596` | Authentication, Tokenization & Recurring Payment Controls | Commercial | 3 | 1 | yes |
| `ADM-597` | Digital Payment Exception, Recovery & Expiry Center | Commercial | 3 | 2 | yes |
| `ADM-598` | Digital Payment Simulator, Conversion & AI Advisor | Commercial | 3 | 3 | yes |
| `ADM-599` | Mixed Tender & Credit Command Center | Commercial | 3 | 1 | yes |
| `ADM-600` | Mixed Tender Rule & Combination Builder | Commercial | 3 | 2 | yes |
| `ADM-601` | Split Payment & Tender Allocation Manager | Commercial | 3 | 3 | yes |
| `ADM-602` | B2B Credit Account & Limit Manager | Commercial | 3 | 2 | yes |
| `ADM-603` | B2B Invoice, On-Account & Payment Terms Configuration | Commercial | 3 | 4 | yes |
| `ADM-604` | Stored Value, Gift Card & Voucher Tender Controls | Commercial | 3 | 2 | yes |
| `ADM-605` | Advanced Payment Eligibility, Sequence & Restriction Rules | Commercial | 3 | 2 | yes |
| `ADM-606` | Partial Payment, Failure & Recovery Manager | Commercial | 3 | 5 | yes |
| `ADM-607` | Mixed Tender Transaction Trace & Allocation Audit | Commercial | 3 | 1 | yes |
| `ADM-608` | Mixed Tender Simulator, Credit Exposure & AI Advisor | Commercial | 3 | 2 | yes |
| `ADM-609` | Refund & Payment Adjustment Command Center | Commercial | 3 | 1 | yes |
| `ADM-610` | Refund Request & Eligibility Workspace | Commercial | 3 | 2 | yes |
| `ADM-611` | Refund Policy & Rule Configuration | Commercial | 3 | 0 | yes |
| `ADM-612` | Refund Allocation & Original Tender Manager | Commercial | 3 | 1 | yes |
| `ADM-613` | Void, Reversal & Cancellation Manager | Commercial | 3 | 2 | yes |
| `ADM-614` | Refund Approval & Exception Workflow | Commercial | 3 | 3 | yes |
| `ADM-615` | Refund Processing, Provider Status & Recovery Center | Commercial | 3 | 1 | yes |
| `ADM-616` | Payment Adjustment & Financial Correction Manager | Commercial | 3 | 2 | yes |
| `ADM-617` | Refund Transaction Trace & Audit Investigation | Commercial | 3 | 1 | yes |
| `ADM-618` | Refund Simulator, Risk Analysis & AI Advisor | Commercial | 3 | 0 | yes |
| `ADM-620` | Reconciliation Source & Import Manager | Commercial | 3 | 3 | yes |
| `ADM-621` | Transaction Matching & Reconciliation Engine | Commercial | 3 | 1 | yes |
| `ADM-622` | Reconciliation Exception & Investigation Center | Commercial | 3 | 2 | yes |
| `ADM-623` | Settlement & Payout Manager | Commercial | 3 | 1 | yes |
| `ADM-624` | Fees, Commission, FX & Settlement Economics | Commercial | 3 | 1 | yes |
| `ADM-625` | Merchant Account & Settlement Calendar Manager | Commercial | 3 | 2 | yes |
| `ADM-626` | Settlement Posting, Finance Handoff & Close Manager | Commercial | 3 | 1 | yes |
| `ADM-627` | Reconciliation Audit, Trace & Evidence Center | Commercial | 3 | 1 | yes |
| `ADM-628` | Reconciliation Simulator, Forecast & AI Operations Advisor | Commercial | 3 | 1 | yes |
| `ADM-629` | Payment Risk & Fraud Command Center | Commercial | 3 | 1 | yes |
| `ADM-630` | Payment Risk Rule & Decision Engine | Commercial | 3 | 3 | yes |
| `ADM-631` | Velocity, Behavioral & Transaction Risk Controls | Commercial | 3 | 1 | yes |
| `ADM-632` | Risk Lists, Signals & Payment Control Center | Commercial | 3 | 1 | yes |
| `ADM-633` | Fraud Alert, Investigation & Case Management | Commercial | 3 | 12 | yes |
| `ADM-634` | Chargeback & Dispute Command Center | Commercial | 3 | 7 | yes |
| `ADM-635` | Chargeback Evidence & Representment Workspace | Commercial | 3 | 2 | yes |
| `ADM-636` | Payment Performance & Conversion Analytics | Commercial | 3 | 1 | yes |
| `ADM-637` | AI Fraud, Anomaly & Payment Intelligence Center | Commercial | 3 | 5 | yes |
| `ADM-638` | Payment Executive Intelligence, Risk Simulator & AI Advisor | Commercial | 3 | 3 | yes |
| `ADM-639` | Recommendation Command Center | Commercial | 3 | 2 | yes |
| `ADM-640` | Recommendation Strategy Manager | Commercial | 3 | 3 | yes |
| `ADM-641` | Recommendation Objective & KPI Configuration | Commercial | 3 | 2 | yes |
| `ADM-642` | Recommendation Type & Product Relationship Manager | Commercial | 3 | 2 | yes |
| `ADM-643` | Recommendation Placement & Touchpoint Manager | Commercial | 3 | 2 | yes |
| `ADM-644` | Channel & Journey Strategy Manager | Commercial | 3 | 2 | yes |
| `ADM-645` | Recommendation Priority, Ranking & Suppression Manager17 | Commercial | 3 | 3 | yes |
| `ADM-646` | Recommendation Guardrails & Business Controls | Commercial | 3 | 2 | yes |
| `ADM-647` | Recommendation Policy, AI Control & Governance | Commercial | 3 | 2 | yes |
| `ADM-648` | Recommendation Strategy Simulator & AI Advisor | Commercial | 3 | 2 | yes |
| `ADM-649` | Upsell & Upgrade Command Center | Commercial | 3 | 1 | yes |
| `ADM-650` | Upgrade Path & Product Ladder Builder | Commercial | 3 | 2 | yes |
| `ADM-651` | Upsell Eligibility & Qualification Rules | Commercial | 3 | 2 | yes |
| `ADM-652` | Upgrade Price Difference & Value Proposition Manager | Commercial | 3 | 2 | yes |
| `ADM-653` | Ticket, Experience & Bundle Upgrade Manager | Commercial | 3 | 2 | yes |
| `ADM-654` | Membership & Pass Upgrade Engine | Commercial | 3 | 2 | yes |
| `ADM-655` | Pre-Purchase, Cart & Checkout Upsell Manager | Commercial | 3 | 2 | yes |
| `ADM-656` | Post-Purchase & In-Journey Upgrade Manager | Commercial | 3 | 3 | yes |
| `ADM-657` | Upsell Ranking, Propensity & AI Opportunity Engine | Commercial | 3 | 1 | yes |
| `ADM-658` | Upgrade Simulator, Comparison & AI Advisor | Commercial | 3 | 2 | yes |
| `ADM-659` | Cross-Sell Command Center | Commercial | 3 | 2 | yes |
| `ADM-660` | Cross-Sell Relationship Builder | Commercial | 3 | 2 | yes |
| `ADM-661` | Product Affinity Matrix & Relationship Map | Commercial | 3 | 1 | yes |
| `ADM-662` | Frequently Bought Together & Basket Pattern Engine | Commercial | 3 | 1 | yes |
| `ADM-663` | Cross-Category Recommendation Manager | Commercial | 3 | 2 | yes |
| `ADM-664` | Multi-Attraction, Destination & Partner Cross-Sell | Commercial | 3 | 2 | yes |
| `ADM-665` | Basket-Aware Cross-Sell & Duplicate Prevention | Commercial | 3 | 2 | yes |
| `ADM-666` | Availability, Inventory & Capacity-Aware Cross-Sell | Commercial | 3 | 2 | yes |
| `ADM-667` | AI Cross-Sell Discovery, Scoring & Ranking Engine | Commercial | 3 | 1 | yes |
| `ADM-668` | Cross-Sell Simulator & AI Opportunity Advisor | Commercial | 3 | 2 | yes |
| `ADM-669` | Journey & Context Command Center | Commercial | 3 | 1 | yes |
| `ADM-670` | Customer Journey Map & Touchpoint Designer | Commercial | 3 | 2 | yes |
| `ADM-671` | Real-Time Context Rule Engine | Commercial | 3 | 2 | yes |
| `ADM-672` | Pre-Purchase & Booking Journey Recommendation Manager | Commercial | 3 | 2 | yes |
| `ADM-673` | Post-Purchase & Pre-Visit Recommendation Manager | Commercial | 3 | 2 | yes |
| `ADM-674` | In-Venue & Location-Aware Recommendation Engine | Commercial | 3 | 2 | yes |
| `ADM-675` | Visit State, Itinerary & Time-Aware Recommendation | Commercial | 3 | 2 | yes |
| `ADM-676` | Omnichannel Recommendation Synchronization | Commercial | 3 | 1 | yes |
| `ADM-677` | Contextual Trigger, Frequency & Experience Controls | Commercial | 3 | 1 | yes |
| `ADM-678` | Journey Simulator, Decision Trace & AI Optimization | Commercial | 3 | 2 | yes |
| `ADM-679` | Personalization & NBO Command Center | Commercial | 3 | 1 | yes |
| `ADM-680` | Customer Recommendation Profile | Commercial | 3 | 3 | yes |
| `ADM-681` | Customer Feature & Signal Configuration | Commercial | 3 | 2 | yes |
| `ADM-682` | Propensity Model & Customer Intent Manager | Commercial | 3 | 1 | yes |
| `ADM-683` | Next-Best-Offer Decision Studio | Commercial | 3 | 2 | yes |
| `ADM-684` | Personalized Ranking & Decision Policy Builder | Commercial | 3 | 2 | yes |
| `ADM-685` | Customer Preference, Fatigue & Suppression Intelligence | Commercial | 3 | 1 | yes |
| `ADM-686` | Anonymous, Known & Identity-Transition Personalization.123 | Commercial | 3 | 1 | yes |
| `ADM-687` | AI Explainability, Confidence & Model Governance | Commercial | 3 | 1 | yes |
| `ADM-688` | Personalization Simulator & Next-Best-Offer Lab | Commercial | 3 | 2 | yes |
| `ADM-689` | Recommendation Performance Command Center | Commercial | 3 | 1 | yes |
| `ADM-690` | Recommendation Strategy & Placement Analytics | Commercial | 3 | 1 | yes |
| `ADM-691` | Recommendation Experiment & A/B Test Studio | Commercial | 3 | 2 | yes |
| `ADM-692` | Experiment Results & Winner Decision Workspace | Commercial | 3 | 2 | yes |
| `ADM-693` | Recommendation Attribution & Incrementality Analytics | Commercial | 3 | 1 | yes |
| `ADM-694` | AI Model Performance & Drift Monitor | Commercial | 3 | 1 | yes |
| `ADM-695` | Recommendation Governance & Deployment Control | Commercial | 3 | 2 | yes |
| `ADM-696` | AI Risk, Fairness, Explainability & Safety Center | Commercial | 3 | 3 | yes |
| `ADM-697` | Recommendation Audit, Decision Trace & Investigation | Commercial | 3 | 1 | yes |
| `ADM-698` | AI Optimization & Recommendation Intelligence Lab | Commercial | 3 | 2 | yes |
| `BO-001` | Queue Directory | Access & Venue | 1 | 13 | yes |
| `BO-002` | Queue Configuration | Access & Venue | 1 | 8 | yes |
| `BO-003` | Queue Integration Setup | Access & Venue | 1 | 4 | yes |
| `BO-004` | Manual Wait Time Entry | Access & Venue | 1 | 6 | yes |
| `BO-005` | Queue Monitor | Access & Venue | 1 | 11 | yes |
| `BO-006` | Parking Configuration | Access & Venue | 2 | 2 | yes |
| `BO-007` | Product Directory | Sell | 1 | 15 | yes |
| `BO-008` | Product Detail & Variants | Sell | 1 | 13 | yes |
| `BO-009` | Pricing Rules | Sell | 1 | 11 | yes |
| `BO-010` | Promotions & Coupons | Sell | 2 | 26 | yes |
| `BO-011` | Packages & Bundles | Sell | 2 | 11 | yes |
| `BO-012` | Membership Products | Sell | 2 | 12 | yes |
| `BO-013` | Channel & Distribution | Sell | 2 | 10 | yes |
| `BO-014` | Catalogue Publishing | Sell | 1 | 5 | yes |
| `BO-015` | Performance Calendar | Sell | 1 | 11 | yes |
| `BO-016` | Performance Template | Sell | 1 | 2 | yes |
| `BO-017` | Capacity Management | Sell | 1 | 8 | yes |
| `BO-018` | Allocation & Holds | Sell | 2 | 2 | yes |
| `BO-019` | Closures & Blackouts | Sell | 2 | 12 | yes |
| `BO-020` | F&B Order Management | Food & Beverage | 1 | 9 | yes |
| `BO-021` | Order Search | Food & Beverage | 1 | 3 | yes |
| `BO-022` | Order Detail | Orders & Money | 1 | 19 | yes |
| `BO-023` | Refunds & Exchanges | Orders & Money | 1 | 16 | yes |
| `BO-024` | Payment Exceptions | Orders & Money | 1 | 6 | yes |
| `BO-025` | Chargebacks & Disputes | Orders & Money | 2 | 10 | yes |
| `BO-026` | Group Bookings | Orders & Money | 2 | 17 | yes |
| `BO-027` | Reissue & Media Replacement | Orders & Money | 2 | 5 | yes |
| `BO-028` | Refund Approval Queue | Orders & Money | 1 | 1 | yes |
| `BO-029` | Report Builder | Orders & Money | 2 | 8 | yes |
| `BO-030` | Work Order Verification | Access & Venue | 1 | 3 | yes |
| `BO-031` | Asset Register | Access & Venue | 1 | 0 | yes |
| `BO-032` | Admission Profiles | Access & Venue | 1 | 4 | yes |
| `BO-033` | Blacklist Management | Access & Venue | 1 | 3 | yes |
| `BO-034` | Scan Activity | Access & Venue | 1 | 2 | yes |
| `BO-035` | Override Audit | Access & Venue | 1 | 3 | yes |
| `BO-036` | Device Registry | Venue Operations | 2 | 9 | yes |
| `BO-037` | Offline Package Status | Sell | 1 | 8 | yes |
| `BO-038` | Reconciliation Queue | Access & Venue | 1 | 2 | yes |
| `BO-039` | Shift Directory | Orders & Money | 1 | 4 | yes |
| `BO-040` | Variance Approval | Orders & Money | 1 | 8 | yes |
| `BO-041` | Cash Movements | Orders & Money | 2 | 4 | yes |
| `BO-042` | Banking & Safe | Orders & Money | 2 | 4 | yes |
| `BO-043` | Daily Reconciliation | Orders & Money | 1 | 12 | yes |
| `BO-044` | F&B Outlets | Venue Operations | 2 | 15 | yes |
| `BO-045` | Menu Management | Food & Beverage | 1 | 18 | yes |
| `BO-046` | Kitchen Display | Food & Beverage | 1 | 3 | yes |
| `BO-047` | Order Corrections & Exceptions | Orders & Money | 2 | 14 | yes |
| `BO-048` | Retail Products | Orders & Money | 2 | 4 | yes |
| `BO-049` | Stock Levels | Stock & Supply | 2 | 5 | yes |
| `BO-050` | Stock Position & Valuation | Stock & Supply | 2 | 2 | yes |
| `BO-051` | Purchase Orders | Stock & Supply | 2 | 7 | yes |
| `BO-052` | Goods Receipt | Stock & Supply | 2 | 5 | yes |
| `BO-053` | Staff Directory | People & Access Rights | 1 | 15 | yes |
| `BO-054` | Role Assignment | People & Access Rights | 1 | 11 | yes |
| `BO-055` | Rota & Scheduling | People & Access Rights | 2 | 5 | yes |
| `BO-056` | Time & Attendance | People & Access Rights | 2 | 3 | yes |
| `BO-057` | Training & Certification | People & Access Rights | 3 | 2 | yes |
| `BO-058` | Reporting Home | Venue Operations | 1 | 11 | yes |
| `BO-059` | Sales Reports | Orders & Money | 1 | 9 | yes |
| `BO-060` | Attendance & Footfall | Venue Operations | 2 | 16 | yes |
| `BO-061` | Scheduled Reports | Orders & Money | 3 | 5 | yes |
| `BO-062` | Venue Profile | Orders & Money | 1 | 2 | yes |
| `BO-063` | Opening Hours & Calendar | Sell | 1 | 2 | yes |
| `BO-064` | Zones & Areas | Venue Operations | 1 | 9 | yes |
| `BO-065` | Venue Configuration | Orders & Money | 1 | 9 | yes |
| `BO-066` | Notification Settings | People & Access Rights | 2 | 3 | yes |
| `BO-067` | Integrations | Venue Operations | 2 | 4 | yes |
| `BO-068` | Audit Log | Guests & Marketing | 2 | 4 | yes |
| `BO-069` | Asset Register | Access & Venue | 2 | 7 | yes |
| `BO-070` | Work Orders | Venue Operations | 2 | 13 | yes |
| `BO-071` | Planned Maintenance | Access & Venue | 3 | 4 | yes |
| `BO-072` | Incident Log | Access & Venue | 2 | 5 | yes |
| `BO-073` | Lost & Found Register | Guests & Marketing | 2 | 4 | yes |
| `BO-074` | Chart of Accounts | Orders & Money | 1 | 8 | yes |
| `BO-075` | Account Mapping | Orders & Money | 1 | 8 | yes |
| `BO-076` | Revenue Recognition | Orders & Money | 2 | 5 | yes |
| `BO-077` | FX Rates & Variances | Orders & Money | 1 | 5 | yes |
| `BO-078` | Requisitions | Stock & Supply | 1 | 10 | yes |
| `BO-079` | Stock Count | Stock & Supply | 1 | 9 | yes |
| `BO-080` | Stock Transfers | Stock & Supply | 2 | 5 | yes |
| `BO-081` | Inventory Items | Stock & Supply | 2 | 9 | yes |
| `BO-082` | Stock Movements | Stock & Supply | 1 | 4 | yes |
| `BO-083` | Suppliers | Stock & Supply | 2 | 8 | yes |
| `BO-084` | Approval Inbox | People & Access Rights | 1 | 4 | yes |
| `BO-085` | Approval Request | People & Access Rights | 1 | 4 | yes |
| `BO-086` | Approval Matrix | People & Access Rights | 2 | 2 | yes |
| `BO-087` | Approval Delegations | People & Access Rights | 2 | 3 | yes |
| `BO-088` | Approval Analytics | People & Access Rights | 3 | 1 | yes |
| `BO-089` | Journal Entries | Orders & Money | 1 | 6 | yes |
| `BO-090` | Period Close | Orders & Money | 1 | 7 | yes |
| `BO-091` | AI Policy & Spend | Guests & Marketing | 1 | 11 | yes |
| `BO-092` | Venue Maps | Access & Venue | 2 | 2 | yes |
| `BO-093` | Map Import & Labelling | Access & Venue | 2 | 5 | yes |
| `BO-094` | Map Editor & Publish | Access & Venue | 2 | 10 | yes |
| `BO-095` | Resources | Access & Venue | 2 | 2 | yes |
| `BO-096` | Resource Calendar | Access & Venue | 2 | 2 | yes |
| `BO-097` | Check Out & Check In | Access & Venue | 2 | 6 | yes |
| `BO-098` | Qualifications | Access & Venue | 2 | 2 | yes |
| `BO-099` | Performance Manifest | Access & Venue | 2 | 2 | yes |
| `BO-100` | Venue Home | Venue Operations | 1 | 3 | yes |
| `BO-1000` | Mobile & Accessible Selection | Access & Venue | 3 | 2 | yes |
| `BO-1001` | View Preview, Compare & Heat Map | Access & Venue | 3 | 2 | yes |
| `BO-1002` | AI Conversational Seat Assistant | Access & Venue | 3 | 2 | yes |
| `BO-1003` | Hold Command Center | Access & Venue | 3 | 1 | yes |
| `BO-1004` | Hold Type Master | Access & Venue | 3 | 2 | yes |
| `BO-1005` | Hold Pool Creation | Access & Venue | 3 | 2 | yes |
| `BO-1006` | Hold Rule Assignment | Access & Venue | 3 | 2 | yes |
| `BO-1007` | Expiration Rules | Access & Venue | 3 | 2 | yes |
| `BO-1008` | Automatic Hold Release | Access & Venue | 3 | 2 | yes |
| `BO-1009` | Release, Convert & Reassign | Access & Venue | 3 | 2 | yes |
| `BO-101` | Orders & Money | Orders & Money | 1 | 2 | yes |
| `BO-1010` | Hold Approval Workflow | Access & Venue | 3 | 2 | yes |
| `BO-1011` | Priority & Conflict Resolution | Access & Venue | 3 | 2 | yes |
| `BO-1012` | Hold Utilization & Audit | Access & Venue | 3 | 1 | yes |
| `BO-1013` | Rules Command Center | Access & Venue | 3 | 1 | yes |
| `BO-1014` | Seat Kill Rules | Access & Venue | 3 | 2 | yes |
| `BO-1015` | Buffer Seat Rules | Access & Venue | 3 | 2 | yes |
| `BO-1016` | Companion Seat Rules | Access & Venue | 3 | 2 | yes |
| `BO-1017` | Wheelchair Companion Rules | Access & Venue | 3 | 2 | yes |
| `BO-1018` | Accessible Seating Master | Access & Venue | 3 | 2 | yes |
| `BO-1019` | Accessible Route Mapping | Access & Venue | 3 | 2 | yes |
| `BO-102` | Sell | Sell | 1 | 3 | yes |
| `BO-1020` | Accessible Filters & Eligibility | Access & Venue | 3 | 2 | yes |
| `BO-1021` | Flexible Spacing Rules | Access & Venue | 3 | 2 | yes |
| `BO-1022` | Compliance Validation & Audit | Access & Venue | 3 | 1 | yes |
| `BO-1023` | Group Reservation Center | Access & Venue | 3 | 1 | yes |
| `BO-1024` | Group Type Configuration | Access & Venue | 3 | 1 | yes |
| `BO-1025` | Group Request Intake | Access & Venue | 3 | 2 | yes |
| `BO-1026` | Availability & Best-Fit Search | Access & Venue | 3 | 2 | yes |
| `BO-1027` | Bulk Seat Allocation | Access & Venue | 3 | 2 | yes |
| `BO-1028` | Roster & Participant Assignment | Access & Venue | 3 | 2 | yes |
| `BO-1029` | Quote, Deposit & Payment | Access & Venue | 3 | 2 | yes |
| `BO-103` | Access & Venue | Access & Venue | 1 | 3 | yes |
| `BO-1030` | Modify, Release & Cancel | Access & Venue | 3 | 2 | yes |
| `BO-1031` | Contracts & Approval Workflow | Access & Venue | 3 | 1 | yes |
| `BO-1032` | Group Reporting & Audit | Access & Venue | 3 | 1 | yes |
| `BO-1033` | Recommendation Command Center | Access & Venue | 3 | 1 | yes |
| `BO-1034` | Best Seat Recommendations | Access & Venue | 3 | 2 | yes |
| `BO-1035` | Best Value Recommendations | Access & Venue | 3 | 2 | yes |
| `BO-1036` | Closest-to-Stage Recommendations | Access & Venue | 3 | 2 | yes |
| `BO-1037` | Family Seating Recommendations | Access & Venue | 3 | 2 | yes |
| `BO-1038` | Accessibility Recommendations | Access & Venue | 3 | 2 | yes |
| `BO-1039` | Seat Upgrade Recommendations | Access & Venue | 3 | 2 | yes |
| `BO-104` | Food & Beverage | Food & Beverage | 1 | 2 | yes |
| `BO-1040` | Alternatives & Reseating | Access & Venue | 3 | 2 | yes |
| `BO-1041` | Scoring Rules & Model Governance | Access & Venue | 3 | 2 | yes |
| `BO-1042` | Performance, Feedback & Audit | Access & Venue | 3 | 1 | yes |
| `BO-1043` | Revenue Command Center | Access & Venue | 3 | 1 | yes |
| `BO-1044` | Dynamic Seat Pricing | Access & Venue | 3 | 1 | yes |
| `BO-1045` | Price Bands & Categories | Access & Venue | 3 | 3 | yes |
| `BO-1046` | Inventory Forecasting | Access & Venue | 3 | 1 | yes |
| `BO-1047` | Section Revenue Forecast | Access & Venue | 3 | 1 | yes |
| `BO-1048` | Seat Upsell Recommendations | Access & Venue | 3 | 1 | yes |
| `BO-1049` | Scenario & What-If Planning | Access & Venue | 3 | 1 | yes |
| `BO-105` | Stock & Supply | Stock & Supply | 1 | 2 | yes |
| `BO-1050` | Revenue Analytics & Audit | Access & Venue | 3 | 1 | yes |
| `BO-1051` | Seat Analytics Command Center | Access & Venue | 3 | 1 | yes |
| `BO-1052` | Occupancy Reporting | Access & Venue | 3 | 1 | yes |
| `BO-1053` | Zone Performance Reporting | Access & Venue | 3 | 1 | yes |
| `BO-1054` | Revenue by Section | Access & Venue | 3 | 1 | yes |
| `BO-1055` | Revenue by Seat Category | Access & Venue | 3 | 1 | yes |
| `BO-1056` | Seat Utilization Analytics | Access & Venue | 3 | 1 | yes |
| `BO-1057` | Hold Inventory Reporting | Access & Venue | 3 | 1 | yes |
| `BO-1058` | Sales Pace & Pick Curves | Access & Venue | 3 | 1 | yes |
| `BO-1059` | Heat Maps & Drill-Down | Access & Venue | 3 | 2 | yes |
| `BO-106` | People & Access Rights | People & Access Rights | 1 | 3 | yes |
| `BO-1060` | Report Builder, Export & Audit | Access & Venue | 3 | 2 | yes |
| `BO-1061` | Platform Command Center | Access & Venue | 3 | 2 | yes |
| `BO-1062` | Tenant & Brand Context | Access & Venue | 3 | 3 | yes |
| `BO-1063` | Venue-Specific Configuration | Access & Venue | 3 | 2 | yes |
| `BO-1064` | Naming, Numbering & Localization | Access & Venue | 3 | 2 | yes |
| `BO-1065` | Currency, Timezone & Channels | Setup | 3 | 4 | yes |
| `BO-1066` | Roles, Permissions & Masking | Access & Venue | 3 | 14 | yes |
| `BO-1067` | Seat Approval Workflows | Access & Venue | 3 | 1 | yes |
| `BO-1068` | Lifecycle & Environment Promotion | Access & Venue | 3 | 1 | yes |
| `BO-1069` | Platform Health & Observability | Access & Venue | 3 | 0 | yes |
| `BO-107` | Guests & Marketing | Guests & Marketing | 1 | 4 | yes |
| `BO-1070` | Setup, Clone & Inheritance | Access & Venue | 3 | 4 | yes |
| `BO-1071` | Integration Command Center | Access & Venue | 3 | 1 | yes |
| `BO-1072` | Seat Management APIs | Access & Venue | 3 | 0 | yes |
| `BO-1073` | API Access & OAuth | Access & Venue | 3 | 3 | yes |
| `BO-1074` | Webhook Configuration | Access & Venue | 3 | 3 | yes |
| `BO-1075` | Seat Event Catalog | Access & Venue | 3 | 1 | yes |
| `BO-1076` | Concurrency, Idempotency & Limits | Access & Venue | 3 | 1 | yes |
| `BO-1077` | Mapping & Transformation | Access & Venue | 3 | 1 | yes |
| `BO-1078` | Monitoring, Retry & Reconciliation | Access & Venue | 3 | 1 | yes |
| `BO-1079` | Immutable Seat Audit Logs | Access & Venue | 3 | 1 | yes |
| `BO-108` | Venue Operations | Venue Operations | 1 | 4 | yes |
| `BO-1080` | Integration Approval & Compliance | Access & Venue | 3 | 1 | yes |
| `BO-1081` | Finance Dashboard | Orders & Money | 3 | 6 | yes |
| `BO-1082` | Admissions Revenue | Orders & Money | 3 | 2 | yes |
| `BO-1083` | Wallet Command Center | Orders & Money | 3 | 2 | yes |
| `BO-1084` | Wallet Type Library | Orders & Money | 3 | 2 | yes |
| `BO-1085` | Wallet Creation & Provisioning Rules | Orders & Money | 3 | 3 | yes |
| `BO-1086` | Wallet Ownership & Account Association | Orders & Money | 3 | 4 | yes |
| `BO-1087` | Wallet Currency & Monetary Configuration | Orders & Money | 3 | 2 | yes |
| `BO-1088` | Credit & Balance Type Configuration | Orders & Money | 3 | 3 | yes |
| `BO-1089` | Wallet Feature Profile | Orders & Money | 3 | 2 | yes |
| `BO-109` | Menu Builder & POS Layout Designer | Sell | 2 | 5 | yes |
| `BO-1090` | Wallet Lifecycle Configuration | Orders & Money | 3 | 2 | yes |
| `BO-1091` | Wallet Numbering, Identity & Digital Credentials | Orders & Money | 3 | 3 | yes |
| `BO-1092` | Wallet Configuration Preview, Validation & Publication | Orders & Money | 3 | 2 | yes |
| `BO-1093` | Funding Command Center | Orders & Money | 3 | 2 | yes |
| `BO-1094` | Funding Method Configuration | Orders & Money | 3 | 2 | yes |
| `BO-1095` | Top-Up Rule Configuration | Orders & Money | 3 | 2 | yes |
| `BO-1096` | Channel & Funding Source Mapping | Orders & Money | 3 | 2 | yes |
| `BO-1097` | Auto-Reload Configuration | Orders & Money | 3 | 2 | yes |
| `BO-1098` | Recurring Funding Schedule | Orders & Money | 3 | 2 | yes |
| `BO-1099` | Funding Authorization & Approval Rules | Orders & Money | 3 | 2 | yes |
| `BO-110` | Recipe & BOM Management | Sell | 2 | 0 | yes |
| `BO-1100` | Funding Reversal & Correction Management | Orders & Money | 3 | 3 | yes |
| `BO-1101` | Funding Limits & Velocity Controls | Orders & Money | 3 | 2 | yes |
| `BO-1102` | Funding Transaction Audit & Reconciliation | Orders & Money | 3 | 2 | yes |
| `BO-1103` | Stored Value & Credit Command Center | Orders & Money | 3 | 2 | yes |
| `BO-1104` | Credit Type Definition Studio | Orders & Money | 3 | 3 | yes |
| `BO-1105` | Credit Issuance Rule Configuration | Orders & Money | 3 | 2 | yes |
| `BO-1106` | Credit Usage & Eligibility Rules | Orders & Money | 3 | 1 | yes |
| `BO-1107` | Consumption Priority Engine | Orders & Money | 3 | 2 | yes |
| `BO-1108` | Expiry & Validity Policy Configuration | Orders & Money | 3 | 2 | yes |
| `BO-1109` | FEFO & Credit Lot Management | Orders & Money | 3 | 1 | yes |
| `BO-111` | Ingredient Substitution, Allergen & Nutrition | Sell | 2 | 6 | yes |
| `BO-1110` | Split Tender & Multi-Credit Consumption | Orders & Money | 3 | 3 | yes |
| `BO-1111` | Credit Expiry, Extension & Forfeiture Operations | Orders & Money | 3 | 2 | yes |
| `BO-1112` | Consumption Simulator, Validation & Rule Publication | Orders & Money | 3 | 3 | yes |
| `BO-1113` | Shared Wallet Command Center | Orders & Money | 3 | 3 | yes |
| `BO-1114` | Shared Wallet Model Configuration | Orders & Money | 3 | 2 | yes |
| `BO-1115` | Family & Household Structure Configuration | Orders & Money | 3 | 2 | yes |
| `BO-1116` | Parent–Child Stored Value Distribution | Orders & Money | 3 | 4 | yes |
| `BO-1117` | Allowance & Budget Allocation Engine | Orders & Money | 3 | 2 | yes |
| `BO-1118` | Member Spending Controls & Permissions | Orders & Money | 3 | 2 | yes |
| `BO-1119` | Corporate Wallet & Organizational Hierarchy | Orders & Money | 3 | 2 | yes |
| `BO-112` | Production Planning & Production Sheets | Sell | 2 | 8 | yes |
| `BO-1120` | Corporate Budget, Policy & Approval Rules | Orders & Money | 3 | 4 | yes |
| `BO-1121` | Shared Wallet Transfers & Balance Reallocation | Orders & Money | 3 | 2 | yes |
| `BO-1122` | Shared Wallet Simulator, Monitoring & Audit | Orders & Money | 3 | 2 | yes |
| `BO-1123` | Gift Card & Digital Benefit Command Center | Orders & Money | 3 | 5 | yes |
| `BO-1124` | Gift Card Product Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1125` | Gift Card Issuance, Activation & Distribution | Orders & Money | 3 | 4 | yes |
| `BO-1126` | Voucher & Coupon Type Configuration | Orders & Money | 3 | 2 | yes |
| `BO-1127` | Voucher Eligibility & Redemption Rule Studio | Orders & Money | 3 | 2 | yes |
| `BO-1128` | Membership Benefits & Entitlement Mapping | Orders & Money | 3 | 1 | yes |
| `BO-1129` | Benefit Packaging & Digital Wallet Presentation | Orders & Money | 3 | 1 | yes |
| `BO-113` | Central Kitchen & Commissary Management | Sell | 2 | 0 | yes |
| `BO-1130` | Gift Card & Voucher Expiry Management | Orders & Money | 3 | 2 | yes |
| `BO-1131` | Gift Card Balance, Liability & Breakage Control | Orders & Money | 3 | 1 | yes |
| `BO-1132` | Gift Card & Voucher Simulator, Validation & Publication | Orders & Money | 3 | 2 | yes |
| `BO-1133` | Wallet Usage & Channel Command Center | Orders & Money | 3 | 0 | yes |
| `BO-1134` | Wallet Channel Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1135` | Wallet Payment & Redemption Policy | Orders & Money | 3 | 1 | yes |
| `BO-1136` | Wearable & Credential Type Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1137` | Wearable Linking & Wallet Association Rules | Orders & Money | 3 | 1 | yes |
| `BO-1138` | NFC, RFID & QR Interaction Rules | Orders & Money | 3 | 1 | yes |
| `BO-1139` | Digital Key & Wallet Authentication Policy | Orders & Money | 3 | 2 | yes |
| `BO-114` | Variants, Attributes, Barcode & RFID Management | Sell | 2 | 2 | yes |
| `BO-1140` | Offline Wallet & Degraded Mode Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1141` | Device, Terminal & Acceptance Point Mapping | Orders & Money | 3 | 2 | yes |
| `BO-1142` | Wallet Transaction Simulator, Monitoring & Channel Audit | Orders & Money | 3 | 2 | yes |
| `BO-1143` | Wallet Operations Command Center | Orders & Money | 3 | 2 | yes |
| `BO-1144` | Peer-to-Peer Transfer Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1145` | Transfer Eligibility, Limits & Approval Rules | Orders & Money | 3 | 1 | yes |
| `BO-1146` | Refund-to-Wallet Policy Configuration | Orders & Money | 3 | 3 | yes |
| `BO-1147` | Refund Routing & Credit Restoration Engine | Orders & Money | 3 | 4 | yes |
| `BO-1148` | Reversal & Transaction Correction Management | Orders & Money | 3 | 2 | yes |
| `BO-1149` | Administrative Balance Adjustment Studio | Orders & Money | 3 | 4 | yes |
| `BO-115` | Category, Brand & Merchandise Hierarchy | Sell | 2 | 3 | yes |
| `BO-1150` | Wallet Block, Freeze & Restriction Management | Orders & Money | 3 | 3 | yes |
| `BO-1151` | Wallet Disputes & Operational Exception Queue | Orders & Money | 3 | 4 | yes |
| `BO-1152` | Operations Simulator, Approval & Audit Trail | Orders & Money | 3 | 1 | yes |
| `BO-1153` | Wallet Security & Risk Command Center | Orders & Money | 3 | 1 | yes |
| `BO-1154` | Wallet Risk Policy Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1155` | Transaction Risk Scoring Engine | Orders & Money | 3 | 1 | yes |
| `BO-1156` | Velocity & Behavioral Rule Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1157` | Device, Credential & Account Security | Orders & Money | 3 | 2 | yes |
| `BO-1158` | AI Fraud & Anomaly Detection Studio | Orders & Money | 3 | 1 | yes |
| `BO-1159` | Automated Security Action Orchestration | Orders & Money | 3 | 2 | yes |
| `BO-116` | Merchandising & Product Presentation | Sell | 2 | 5 | yes |
| `BO-1160` | Fraud Alert & Investigation Case Management | Orders & Money | 3 | 6 | yes |
| `BO-1161` | Security Rules Testing, Simulation & AI Sandbox | Orders & Money | 3 | 0 | yes |
| `BO-1162` | Security Governance, Audit & Rule Publication | Orders & Money | 3 | 6 | yes |
| `BO-1163` | Wallet Finance & Liability Command Center | Orders & Money | 3 | 1 | yes |
| `BO-1164` | Wallet Financial Classification & Accounting Mapping | Orders & Money | 3 | 1 | yes |
| `BO-1165` | Wallet Sub-Ledger & Balance Control | Orders & Money | 3 | 1 | yes |
| `BO-1166` | Multi-Source Reconciliation Configuration | Orders & Money | 3 | 2 | yes |
| `BO-1167` | Reconciliation Exception & Resolution Workbench | Orders & Money | 3 | 2 | yes |
| `BO-1168` | Gift Card Liability Management | Orders & Money | 3 | 1 | yes |
| `BO-1169` | Breakage & Revenue Recognition Policy | Orders & Money | 3 | 1 | yes |
| `BO-117` | Product Import, Governance & AI Configuration Assistant | Sell | 2 | 3 | yes |
| `BO-1170` | Wallet Financial Period & Closing Controls | Orders & Money | 3 | 4 | yes |
| `BO-1171` | Wallet Analytics & Management Reporting | Orders & Money | 3 | 1 | yes |
| `BO-1172` | Finance Validation, Reporting & Audit Center | Orders & Money | 3 | 6 | yes |
| `BO-1173` | Wallet Integration Command Center | Orders & Money | 3 | 4 | yes |
| `BO-1174` | Wallet API Catalogue & Endpoint Configuration | Orders & Money | 3 | 0 | yes |
| `BO-1175` | Integration Profile & System Mapping | Orders & Money | 3 | 2 | yes |
| `BO-1176` | Wallet Events, Webhooks & Notification Orchestration | Orders & Money | 3 | 3 | yes |
| `BO-1177` | API Security, Access & Integration Permissions | Orders & Money | 3 | 4 | yes |
| `BO-1178` | Synchronization, Retry & Resilience Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1179` | Integration Monitoring & Exception Workbench | Orders & Money | 3 | 8 | yes |
| `BO-118` | Campaign & Audience Management | Sell | 2 | 4 | yes |
| `BO-1180` | Wallet Configuration Governance & Version Control | Orders & Money | 3 | 2 | yes |
| `BO-1181` | Approval, Publication & Change Management | Orders & Money | 3 | 4 | yes |
| `BO-1182` | Wallet Platform Health, Audit & Administration Center | Orders & Money | 3 | 1 | yes |
| `BO-1183` | Transport Stations | Transport | 2 | 3 | yes |
| `BO-1184` | Transport Routes & Stops | Transport | 2 | 6 | yes |
| `BO-1185` | Transport Fares & Passenger Types | Transport | 2 | 4 | yes |
| `BO-1186` | Transport Timetables | Transport | 2 | 6 | yes |
| `BO-1187` | Transport Departure Board | Transport | 2 | 4 | yes |
| `BO-1188` | Transport Pass Types | Transport | 2 | 4 | yes |
| `BO-1189` | Transport Network Import | Transport | 2 | 5 | yes |
| `BO-119` | Cross-Sell, Upsell & Recommendation Rules | Sell | 2 | 4 | yes |
| `BO-1190` | Donation Campaigns | Sell | 2 | 3 | yes |
| `BO-120` | Omnichannel Commerce & Journey Configuration | Sell | 2 | 2 | yes |
| `BO-121` | Personalized Offers & Guest Engagement | Sell | 2 | 2 | yes |
| `BO-122` | POS Experience Dashboard | Sell | 2 | 1 | yes |
| `BO-123` | POS Profile Management | Sell | 2 | 2 | yes |
| `BO-124` | Layout & Journey Builder | Sell | 2 | 5 | yes |
| `BO-125` | Product & Category Button Configuration | Sell | 2 | 2 | yes |
| `BO-126` | Deployment, Preview & Audit | Sell | 2 | 5 | yes |
| `BO-128` | Live Workstation Health Monitor | Venue Operations | 2 | 2 | yes |
| `BO-129` | Software, Configuration & Version Management | Venue Operations | 2 | 10 | yes |
| `BO-130` | Offline Policy & Rules Configuration | Venue Operations | 1 | 3 | yes |
| `BO-131` | Connectivity & Auto-Switch Settings | Venue Operations | 2 | 1 | yes |
| `BO-132` | Offline Transaction Monitor & Sync Queue | Venue Operations | 2 | 2 | yes |
| `BO-133` | Offline Alerts, Limits & Audit | Venue Operations | 1 | 7 | yes |
| `BO-134` | Kitchen & Preparation Stations | Food & Beverage | 2 | 5 | yes |
| `BO-135` | Order Routing & KDS/Printer Rules | Food & Beverage | 2 | 2 | yes |
| `BO-136` | F&B Global Settings & Controls | Food & Beverage | 2 | 3 | yes |
| `BO-137` | Recipe Consumption & Theoretical Inventory | Stock & Supply | 2 | 4 | yes |
| `BO-138` | Production Execution & Batch Management | Stock & Supply | 2 | 0 | yes |
| `BO-139` | Wastage, Spoilage, Returns & Write-Off | Stock & Supply | 2 | 4 | yes |
| `BO-140` | Product Availability, 86 & Operational Food Safety | Stock & Supply | 2 | 7 | yes |
| `BO-141` | Operational Alerts, AI Replenishment & Action Center | Stock & Supply | 2 | 3 | yes |
| `BO-142` | Store Rules, Controls & Permissions | Sell | 2 | 2 | yes |
| `BO-143` | Retail Global Settings & Controls | Sell | 2 | 4 | yes |
| `BO-144` | Access Control Command Center | Access & Venue | 3 | 1 | yes |
| `BO-145` | Venue & Park Access Structure | Access & Venue | 3 | 4 | yes |
| `BO-146` | Access Area & Zone Builder | Access & Venue | 3 | 1 | yes |
| `BO-147` | Attraction Access Configuration | Access & Venue | 3 | 2 | yes |
| `BO-148` | Access Point Directory | Access & Venue | 3 | 3 | yes |
| `BO-149` | Gate & Lane Configuration | Access & Venue | 3 | 1 | yes |
| `BO-150` | Access Control Graphical Map Designer | Access & Venue | 3 | 1 | yes |
| `BO-151` | Access Location Grouping | Access & Venue | 3 | 3 | yes |
| `BO-152` | Operating Calendar & Special Access Days | Access & Venue | 3 | 3 | yes |
| `BO-153` | Topology Validation & Publication | Access & Venue | 3 | 2 | yes |
| `BO-154` | Access Rule Command Center | Access & Venue | 3 | 3 | yes |
| `BO-155` | Visual Access Rule Builder | Access & Venue | 3 | 2 | yes |
| `BO-156` | Entry, Exit & Re-entry Rules | Access & Venue | 3 | 2 | yes |
| `BO-157` | Anti-Passback & Journey Sequence | Access & Venue | 3 | 3 | yes |
| `BO-158` | Access Validity & Time Rules | Access & Venue | 3 | 3 | yes |
| `BO-159` | Entitlement Consumption Engine | Access & Venue | 3 | 2 | yes |
| `BO-160` | Multi-Park & Crossover Rules | Access & Venue | 3 | 2 | yes |
| `BO-161` | Guest, Companion & Eligibility Rules | Access & Venue | 3 | 3 | yes |
| `BO-162` | Group Admission & Quantity Validation | Access & Venue | 3 | 1 | yes |
| `BO-163` | Rule Simulation, Conflict Check & Publication | Access & Venue | 3 | 2 | yes |
| `BO-164` | Digital Credential Security Command Center | Access & Venue | 3 | 2 | yes |
| `BO-165` | Dynamic QR Security Profile Builder | Access & Venue | 3 | 1 | yes |
| `BO-166` | Credential Activation & Display Rules | Access & Venue | 3 | 2 | yes |
| `BO-167` | Device Binding & Session Security | Access & Venue | 3 | 3 | yes |
| `BO-168` | BLE Beacon & Geofence Configuration | Access & Venue | 3 | 1 | yes |
| `BO-169` | Credential Transfer & Rebinding | Access & Venue | 3 | 1 | yes |
| `BO-170` | Credential Revocation & Lifecycle Events | Access & Venue | 3 | 2 | yes |
| `BO-171` | Offline Cryptographic Validation Profile | Access & Venue | 3 | 2 | yes |
| `BO-172` | Embedded Entitlement Payload Designer | Access & Venue | 3 | 1 | yes |
| `BO-173` | Credential Security Simulation, Audit & Publication | Access & Venue | 3 | 2 | yes |
| `BO-174` | Media & Credential Command Center | Access & Venue | 3 | 2 | yes |
| `BO-175` | Media Type & Technology Library | Access & Venue | 3 | 2 | yes |
| `BO-176` | Virtual Credential & Media Association | Access & Venue | 3 | 1 | yes |
| `BO-177` | Verification Method Selection & Locking | Access & Venue | 3 | 2 | yes |
| `BO-178` | Media Issuance & Encoding Profile | Access & Venue | 3 | 2 | yes |
| `BO-179` | Media Swap & Replacement | Access & Venue | 3 | 1 | yes |
| `BO-180` | RFID & NFC Configuration | Access & Venue | 3 | 1 | yes |
| `BO-181` | External & Partner Credential Mapping | Access & Venue | 3 | 1 | yes |
| `BO-182` | Hotel, Wallet & External Media Integration | Access & Venue | 3 | 2 | yes |
| `BO-183` | Media Compatibility, Testing & Publication | Access & Venue | 3 | 1 | yes |
| `BO-184` | Biometric Access Command Center | Access & Venue | 3 | 1 | yes |
| `BO-185` | Biometric Verification Profile Builder | Access & Venue | 3 | 1 | yes |
| `BO-186` | Face Pass Enrollment Configuration | Access & Venue | 3 | 1 | yes |
| `BO-187` | Biometric Consent & Guardian Management | Access & Venue | 3 | 3 | yes |
| `BO-188` | Face Tag Temporary Enrollment | Access & Venue | 3 | 2 | yes |
| `BO-189` | Face Matching & Verification Thresholds | Access & Venue | 3 | 2 | yes |
| `BO-190` | Face Change, Re-enrollment & Identity Protection | Access & Venue | 3 | 3 | yes |
| `BO-191` | Biometric Validation at Gate | Access & Venue | 3 | 1 | yes |
| `BO-192` | Biometric Lifecycle, Retention & Deletion | Access & Venue | 3 | 3 | yes |
| `BO-193` | Biometric Simulation, Audit & Publication | Access & Venue | 3 | 2 | yes |
| `BO-194` | Device & Gate Command Center | Access & Venue | 3 | 2 | yes |
| `BO-195` | Device Type & Hardware Library | Access & Venue | 3 | 2 | yes |
| `BO-196` | Physical Device Registration & Provisioning | Access & Venue | 3 | 5 | yes |
| `BO-197` | Turnstile & Lane Behavior Configuration | Access & Venue | 3 | 1 | yes |
| `BO-198` | Validation Outcome & Guest Feedback Designer | Access & Venue | 3 | 1 | yes |
| `BO-199` | Reader, Scanner & Peripheral Configuration | Access & Venue | 3 | 1 | yes |
| `BO-200` | Handheld & Mobile Access Device Configuration | Access & Venue | 3 | 1 | yes |
| `BO-201` | Gate Modes, Free Spin & Emergency Controls | Access & Venue | 3 | 2 | yes |
| `BO-202` | Device Software, Content & Remote Configuration | Access & Venue | 3 | 1 | yes |
| `BO-203` | Hardware Compatibility, Health, Testing & Deployment | Access & Venue | 3 | 3 | yes |
| `BO-204` | Offline & Edge Operations Command Center | Access & Venue | 3 | 1 | yes |
| `BO-205` | Edge Node & Local Processing Configuration | Access & Venue | 3 | 1 | yes |
| `BO-206` | Offline Validation Policy Builder | Access & Venue | 3 | 1 | yes |
| `BO-207` | Edge Package & Data Distribution | Access & Venue | 3 | 2 | yes |
| `BO-208` | Offline Credential & Revocation Cache | Access & Venue | 3 | 2 | yes |
| `BO-209` | Offline Entitlement & Usage Ledger | Access & Venue | 3 | 1 | yes |
| `BO-210` | Connectivity Failure & Degraded Mode Policy | Access & Venue | 3 | 2 | yes |
| `BO-211` | Reconnection, Synchronization & Conflict Resolution | Access & Venue | 3 | 1 | yes |
| `BO-212` | Offline Simulation & Resilience Testing | Access & Venue | 3 | 1 | yes |
| `BO-213` | Edge Security, Audit & Deployment | Access & Venue | 3 | 2 | yes |
| `BO-214` | Guest Journey Command Center | Access & Venue | 3 | 2 | yes |
| `BO-215` | Group & B2B Admission Profile Builder | Access & Venue | 3 | 1 | yes |
| `BO-216` | Group Leader & Fast B2B Validation | Access & Venue | 3 | 1 | yes |
| `BO-217` | Group Attendance & Partial Entry Manager | Access & Venue | 3 | 1 | yes |
| `BO-218` | Family, Child, POD & Companion Journey | Access & Venue | 3 | 2 | yes |
| `BO-219` | Re-entry & Temporary Exit Journey | Access & Venue | 3 | 2 | yes |
| `BO-220` | Multi-Park & Crossover Journey Orchestrator | Access & Venue | 3 | 4 | yes |
| `BO-221` | Fast Pass & Attraction Access Journey | Access & Venue | 3 | 4 | yes |
| `BO-222` | Special Event, Free View & Alternative Admission | Access & Venue | 3 | 3 | yes |
| `BO-223` | Journey Simulation, Audit & Publication | Access & Venue | 3 | 2 | yes |
| `BO-224` | Live Access Operations Command Center | Access & Venue | 3 | 1 | yes |
| `BO-225` | Podium Operations Console | Access & Venue | 3 | 4 | yes |
| `BO-226` | Ticket & Credential Investigation Console | Access & Venue | 3 | 1 | yes |
| `BO-227` | Validation Exception & Reason Code Manager | Access & Venue | 3 | 3 | yes |
| `BO-228` | Manual Override & Supervisor Approval | Access & Venue | 3 | 1 | yes |
| `BO-229` | Credential Disable, Blacklist & Whitelist Operations | Access & Venue | 3 | 3 | yes |
| `BO-230` | Live Gate Mode & Lane Control | Access & Venue | 3 | 5 | yes |
| `BO-231` | Queue, Throughput & Lane Optimization | Access & Venue | 3 | 1 | yes |
| `BO-232` | Operational Incident & Exception Workspace | Access & Venue | 3 | 1 | yes |
| `BO-233` | Operations Audit, Shift Handover & Control Summary | Access & Venue | 3 | 2 | yes |
| `BO-234` | Dynamic Access Policy Command Center | Access & Venue | 3 | 2 | yes |
| `BO-235` | Access Attribute Catalog | Access & Venue | 3 | 2 | yes |
| `BO-236` | Visual Dynamic Policy Builder | Access & Venue | 3 | 2 | yes |
| `BO-237` | Context, Time, Event & Capacity Policy Builder | Access & Venue | 3 | 1 | yes |
| `BO-238` | Identity, Membership & Accreditation Policies | Access & Venue | 3 | 3 | yes |
| `BO-239` | Policy Scope, Hierarchy & Inheritance | Access & Venue | 3 | 2 | yes |
| `BO-240` | Authorization Governance & Temporary Access | Access & Venue | 3 | 1 | yes |
| `BO-241` | Policy Evaluation Architecture & Offline Distribution | Access & Venue | 3 | 2 | yes |
| `BO-242` | Policy Simulation, Conflict & Impact Analysis | Access & Venue | 3 | 1 | yes |
| `BO-243` | Policy Approval, Audit, Analytics & AI Optimization | Access & Venue | 3 | 5 | yes |
| `BO-244` | Access Security & Fraud Command Center | Access & Venue | 3 | 4 | yes |
| `BO-245` | Fraud Detection Rule & Signal Library | Access & Venue | 3 | 2 | yes |
| `BO-246` | Credential Sharing & Concurrent Usage Detection | Access & Venue | 3 | 2 | yes |
| `BO-247` | Unified Identity & Credential Lock Manager | Access & Venue | 3 | 3 | yes |
| `BO-248` | Biometric & Identity Integrity Monitoring | Access & Venue | 3 | 5 | yes |
| `BO-249` | Relationship & Companion Fraud Monitoring | Access & Venue | 3 | 2 | yes |
| `BO-250` | Access Risk Scoring & Decision Engine | Access & Venue | 3 | 3 | yes |
| `BO-251` | Real-Time Security Response & Playbook Builder | Access & Venue | 3 | 1 | yes |
| `BO-252` | Security Investigation & Evidence Workspace | Access & Venue | 3 | 1 | yes |
| `BO-253` | Security Analytics, AI Detection & Governance | Access & Venue | 3 | 2 | yes |
| `BO-254` | Access Monitoring & Analytics Command Center | Access & Venue | 3 | 1 | yes |
| `BO-255` | Live Venue Occupancy & People Counting | Access & Venue | 3 | 1 | yes |
| `BO-256` | Graphical Access Map & Live Gate Performance | Access & Venue | 3 | 1 | yes |
| `BO-257` | Attendance & Admission Analytics | Access & Venue | 3 | 1 | yes |
| `BO-258` | Entry, Exit, Re-entry & Crossover Analytics | Access & Venue | 3 | 1 | yes |
| `BO-259` | Throughput, Queue & Validation Performance Analytics | Access & Venue | 3 | 1 | yes |
| `BO-260` | Validation Outcome & Rejection Analytics | Access & Venue | 3 | 1 | yes |
| `BO-261` | Guest Dwell Time, Length of Stay & Attraction Flow | Access & Venue | 3 | 1 | yes |
| `BO-262` | Access Reports, Scheduled Reporting & Data Export | Access & Venue | 3 | 7 | yes |
| `BO-263` | AI Access Intelligence, Forecasting & Executive Insights | Access & Venue | 3 | 1 | yes |
| `BO-264` | Group Sales Command Center | Sell | 3 | 2 | yes |
| `BO-265` | Group Enquiry & Opportunity Capture | Sell | 3 | 2 | yes |
| `BO-266` | Group Customer & Organization Profile | Sell | 3 | 2 | yes |
| `BO-267` | Group Requirements, Availability & Capacity Planner | Sell | 3 | 1 | yes |
| `BO-268` | Group Package & Experience Builder | Sell | 3 | 2 | yes |
| `BO-269` | Group Quotation Builder & Proposal Generation | Sell | 3 | 1 | yes |
| `BO-270` | Quote Revision, Negotiation & Version Management | Sell | 3 | 1 | yes |
| `BO-271` | Group Discount, Exception & Approval Workflow | Sell | 3 | 1 | yes |
| `BO-272` | Quote-to-Booking Conversion & Confirmation | Sell | 3 | 3 | yes |
| `BO-273` | Group Booking 360° & Handover Workspace | Sell | 3 | 2 | yes |
| `BO-274` | Group Booking Operations Command Center | Sell | 3 | 2 | yes |
| `BO-275` | Group Operational Planning & Task Workspace | Sell | 3 | 1 | yes |
| `BO-276` | Participants, Guest Lists & Group Structure | Sell | 3 | 2 | yes |
| `BO-277` | Group Payment, Deposit & Balance Management | Sell | 3 | 2 | yes |
| `BO-278` | Group Ticket, Seat & Entitlement Allocation | Sell | 3 | 2 | yes |
| `BO-279` | Group Ticket Fulfillment & Distribution | Sell | 3 | 2 | yes |
| `BO-280` | Group Arrival, Check-In & Admission Operations | Sell | 3 | 2 | yes |
| `BO-281` | Group Amendments, Cancellation & Refund Operations | Sell | 3 | 4 | yes |
| `BO-282` | Group Booking Reconciliation, Closure & Performance | Sell | 3 | 1 | yes |
| `BO-283` | Group Sales Analytics & AI Intelligence Center | Sell | 3 | 2 | yes |
| `BO-284` | Membership & Annual Pass Command Center | Sell | 3 | 4 | yes |
| `BO-285` | Membership Product & Tier Builder | Sell | 3 | 2 | yes |
| `BO-286` | Membership Eligibility & Qualification Rule Builder | Sell | 3 | 1 | yes |
| `BO-287` | Validity, Activation & Expiry Configuration | Sell | 3 | 1 | yes |
| `BO-288` | Membership Entitlement & Admission Benefit Builder | Sell | 3 | 5 | yes |
| `BO-289` | Membership Usage, Visit & Consumption Rules | Sell | 3 | 4 | yes |
| `BO-290` | Family, Household & Dependent Membership Configuration | Sell | 3 | 1 | yes |
| `BO-291` | Membership Commercial, Pricing & Channel Association | Sell | 3 | 5 | yes |
| `BO-292` | Renewal, Auto-Renewal & Membership Continuity Configuration | Sell | 3 | 1 | yes |
| `BO-293` | Membership Product Validation, Approval, Publication & Versioning | Sell | 3 | 3 | yes |
| `BO-294` | Member Operations Command Center | Sell | 3 | 1 | yes |
| `BO-295` | Member 360° Membership Account Workspace | Sell | 3 | 2 | yes |
| `BO-296` | Membership Activation, Assignment & Credential Management | Sell | 3 | 2 | yes |
| `BO-297` | Visit, Admission & Entitlement Usage Monitor | Sell | 3 | 1 | yes |
| `BO-298` | Membership Freeze, Suspension & Reactivation Management | Sell | 3 | 4 | yes |
| `BO-299` | Membership Upgrade, Downgrade & Product Migration Operations | Sell | 3 | 2 | yes |
| `BO-300` | Renewal Operations & Auto-Renewal Management | Sell | 3 | 2 | yes |
| `BO-301` | Member Exceptions, Overrides & Service Recovery | Sell | 3 | 5 | yes |
| `BO-302` | Member Lifecycle History, Audit & Case Timeline | Sell | 3 | 1 | yes |
| `BO-303` | Membership Analytics, Renewal Intelligence & AI Retention Center | Sell | 3 | 1 | yes |
| `BO-304` | Order & Reservation Command Center | Orders & Money | 3 | 1 | yes |
| `BO-305` | Order Detail & Transaction Workspace | Orders & Money | 3 | 2 | yes |
| `BO-306` | Reservation & Hold Policy Configuration | Orders & Money | 3 | 1 | yes |
| `BO-307` | Order & Reservation Status Lifecycle Configuration | Orders & Money | 3 | 1 | yes |
| `BO-308` | Order Creation & Source/Channel Configuration | Orders & Money | 3 | 1 | yes |
| `BO-309` | Customer, Guest & Account Assignment | Orders & Money | 3 | 1 | yes |
| `BO-310` | Order Line, Product & Entitlement Composition | Orders & Money | 3 | 1 | yes |
| `BO-311` | Capacity Reservation & Inventory Commitment | Orders & Money | 3 | 1 | yes |
| `BO-312` | Reservation Confirmation, Expiry & Fulfillment Readiness | Orders & Money | 3 | 1 | yes |
| `BO-313` | Order Lifecycle Timeline, SLA, Exceptions & AI Operations | Orders & Money | 3 | 1 | yes |
| `BO-314` | Amendment & After-Sales Command Center | Orders & Money | 3 | 2 | yes |
| `BO-315` | Order Amendment Workspace | Orders & Money | 3 | 4 | yes |
| `BO-316` | Amendment Eligibility & Policy Rule Builder | Orders & Money | 3 | 1 | yes |
| `BO-317` | Cancellation & Partial Cancellation Policy Configuration | Orders & Money | 3 | 1 | yes |
| `BO-318` | Refund Policy & Refund Calculation Configuration | Orders & Money | 3 | 3 | yes |
| `BO-319` | Void, Reversal & Same-Day Correction Management | Orders & Money | 3 | 5 | yes |
| `BO-321` | After-Sales Financial Settlement & Adjustment Workspace | Orders & Money | 3 | 1 | yes |
| `BO-322` | Approval, Exception & Service Recovery Management | Orders & Money | 3 | 1 | yes |
| `BO-323` | Amendment History, Audit & After-Sales Analytics | Orders & Money | 3 | 2 | yes |
| `BO-324` | Payment & Order Financial Command Center | Orders & Money | 3 | 3 | yes |
| `BO-325` | Order Payment Detail & Transaction Ledger | Orders & Money | 3 | 1 | yes |
| `BO-326` | Multi-Payment, Split Tender & Payment Allocation Configuration | Orders & Money | 3 | 2 | yes |
| `BO-327` | Deposit, Partial Payment & Outstanding Balance Management | Orders & Money | 3 | 5 | yes |
| `BO-328` | Order Split, Merge & Transaction Relationship Management | Orders & Money | 3 | 3 | yes |
| `BO-329` | Related Order & Transaction Relationship Explorer | Orders & Money | 3 | 1 | yes |
| `BO-330` | External Payment, Partner & Settlement Reference Mapping | Orders & Money | 3 | 3 | yes |
| `BO-331` | Payment Reconciliation & Exception Management | Orders & Money | 3 | 1 | yes |
| `BO-332` | Financial Traceability, Control & Audit Explorer | Orders & Money | 3 | 1 | yes |
| `BO-333` | Order Financial Analytics & AI Reconciliation Intelligence | Orders & Money | 3 | 1 | yes |
| `BO-334` | Virtual Ticket Command Center | Access & Venue | 3 | 1 | yes |
| `BO-335` | Virtual Ticket Identity & Master Record Configuration | Access & Venue | 3 | 1 | yes |
| `BO-336` | Virtual Ticket Status & Lifecycle Model | Access & Venue | 3 | 2 | yes |
| `BO-337` | Media Type & Credential Technology Registry | Access & Venue | 3 | 2 | yes |
| `BO-338` | Multi-Media Binding & Association Rules | Access & Venue | 3 | 3 | yes |
| `BO-339` | Credential Identity, Token & Reference Mapping | Access & Venue | 3 | 1 | yes |
| `BO-340` | Entitlement & Cross-Media Synchronization Rules | Access & Venue | 3 | 2 | yes |
| `BO-341` | Media Activation, Priority & Fallback Rules | Access & Venue | 3 | 1 | yes |
| `BO-342` | Media Replacement, Revocation & Rebinding Rules | Access & Venue | 3 | 2 | yes |
| `BO-343` | Virtual Ticket Architecture Testing, Governance & Audit | Access & Venue | 3 | 1 | yes |
| `BO-344` | Media Design Studio Command Center | Access & Venue | 3 | 5 | yes |
| `BO-345` | Digital QR & Barcode Ticket Designer | Access & Venue | 3 | 1 | yes |
| `BO-346` | PDF, Printable & POS Ticket Designer | Access & Venue | 3 | 5 | yes |
| `BO-347` | Apple Wallet Pass Designer | Access & Venue | 3 | 1 | yes |
| `BO-348` | Google Wallet Pass Designer | Access & Venue | 3 | 1 | yes |
| `BO-349` | RFID, NFC, Card & Wristband Media Designer | Access & Venue | 3 | 1 | yes |
| `BO-350` | Digital Card, Membership & Wearable Designer | Access & Venue | 3 | 1 | yes |
| `BO-351` | Dynamic Fields, Data Mapping & Content Builder | Access & Venue | 3 | 1 | yes |
| `BO-352` | Branding, Localization & Template Inheritance | Access & Venue | 3 | 2 | yes |
| `BO-353` | Multi-Media Preview, Testing, Approval & Publication | Access & Venue | 3 | 1 | yes |
| `BO-354` | Credential Operations Command Center | Access & Venue | 3 | 1 | yes |
| `BO-355` | Virtual Ticket & Credential 360° Workspace | Access & Venue | 3 | 3 | yes |
| `BO-356` | Credential Generation & Issuance Monitor | Access & Venue | 3 | 5 | yes |
| `BO-357` | Credential Delivery & Distribution Operations | Access & Venue | 3 | 2 | yes |
| `BO-358` | Media Binding, Activation & Assignment Operations | Access & Venue | 3 | 2 | yes |
| `BO-359` | Credential Replacement, Reissue, Revocation & Recovery | Access & Venue | 3 | 2 | yes |
| `BO-360` | Failed Generation, Delivery & Credential Exception Management | Access & Venue | 3 | 2 | yes |
| `BO-361` | Credential Usage & Cross-Media Traceability | Access & Venue | 3 | 1 | yes |
| `BO-362` | Credential Security, Audit & Operational Evidence | Access & Venue | 3 | 1 | yes |
| `BO-363` | Ticket Media Analytics & AI Operations Intelligence | Access & Venue | 3 | 1 | yes |
| `BO-364` | Approval Command Center Dashboard | Venue Operations | 3 | 2 | yes |
| `BO-365` | My Approval Inbox | Venue Operations | 3 | 0 | yes |
| `BO-366` | Team / Shared Approval Queue | Venue Operations | 3 | 1 | yes |
| `BO-367` | Approval Request Detail | Venue Operations | 3 | 3 | yes |
| `BO-368` | AI Decision Support | Venue Operations | 3 | 2 | yes |
| `BO-369` | High Priority & Risk Queue | Venue Operations | 3 | 2 | yes |
| `BO-370` | Escalated Approval Center | Venue Operations | 3 | 2 | yes |
| `BO-371` | Completed Approval History | Venue Operations | 3 | 1 | yes |
| `BO-372` | Approval SLA & Workload Monitor | Venue Operations | 3 | 2 | yes |
| `BO-373` | Approval Activity & Notification Center | Venue Operations | 3 | 1 | yes |
| `BO-374` | Approval Decision Workspace | Venue Operations | 3 | 2 | yes |
| `BO-375` | Business Context & Evidence Viewer | Venue Operations | 3 | 2 | yes |
| `BO-376` | Approval Timeline & Decision Chain | Venue Operations | 3 | 1 | yes |
| `BO-377` | Approve & Sensitive Action Confirmation | Venue Operations | 3 | 3 | yes |
| `BO-378` | Reject / Return / Request Information | Venue Operations | 3 | 1 | yes |
| `BO-379` | Requester Modification & Resubmission | Venue Operations | 3 | 1 | yes |
| `BO-380` | Withdrawal, Cancellation, Expiration & Reopening | Venue Operations | 3 | 1 | yes |
| `BO-381` | Segregation of Duties & Four-Eyes Control | Venue Operations | 3 | 1 | yes |
| `BO-382` | Approved Action Execution & Status | Venue Operations | 3 | 3 | yes |
| `BO-383` | Decision Record & Immutable Audit View | Venue Operations | 3 | 1 | yes |
| `BO-384` | Delegation & Escalation Command Center | Venue Operations | 3 | 3 | yes |
| `BO-385` | Delegation Management | Venue Operations | 3 | 3 | yes |
| `BO-386` | Temporary Delegation & Availability Calendar | Venue Operations | 3 | 2 | yes |
| `BO-387` | Out-of-Office & Substitute Routing | Venue Operations | 3 | 1 | yes |
| `BO-388` | Approval SLA Policy Configuration | Venue Operations | 3 | 1 | yes |
| `BO-389` | Reminder & Breach Notification Rules | Venue Operations | 3 | 0 | yes |
| `BO-390` | Escalation Policy Builder | Venue Operations | 3 | 0 | yes |
| `BO-391` | Live Escalation Operations Center | Venue Operations | 3 | 2 | yes |
| `BO-392` | SLA & Escalation Performance Analytics | Venue Operations | 3 | 1 | yes |
| `BO-393` | AI SLA & Escalation Advisor | Venue Operations | 3 | 3 | yes |
| `BO-394` | Game & Ride Operations Dashboard | Games & Rides | 3 | 5 | yes |
| `BO-395` | Game & Ride Directory | Games & Rides | 3 | 4 | yes |
| `BO-396` | Attraction Profile | Games & Rides | 3 | 3 | yes |
| `BO-397` | Attraction Type Configuration | Games & Rides | 3 | 2 | yes |
| `BO-398` | Game & Ride Operational Configuration | Games & Rides | 3 | 2 | yes |
| `BO-399` | Wallet & Credit Acceptance Mapping | Games & Rides | 3 | 1 | yes |
| `BO-400` | Attraction / Reader Mapping | Games & Rides | 3 | 3 | yes |
| `BO-401` | Game Package & Entitlement Association | Games & Rides | 3 | 1 | yes |
| `BO-402` | Configuration Health & Validation | Games & Rides | 3 | 2 | yes |
| `BO-403` | Attraction Audit, Dependencies & Governed Actions | Games & Rides | 3 | 0 | yes |
| `BO-404` | Reader Management Dashboard | Games & Rides | 3 | 1 | yes |
| `BO-405` | Reader Directory | Games & Rides | 3 | 5 | yes |
| `BO-406` | Reader Profile & Device Setup | Games & Rides | 3 | 3 | yes |
| `BO-407` | Reader Credit & Payment Configuration | Games & Rides | 3 | 4 | yes |
| `BO-408` | Reader / Attraction Assignment | Games & Rides | 3 | 1 | yes |
| `BO-409` | Retap Delay & Transaction Protection | Games & Rides | 3 | 1 | yes |
| `BO-410` | Free Game Glow & Reader Display Rules | Games & Rides | 3 | 1 | yes |
| `BO-411` | Reader Theme & Experience Configuration | Games & Rides | 3 | 1 | yes |
| `BO-412` | Real-Time Tap Validation & Reader Response | Games & Rides | 3 | 1 | yes |
| `BO-413` | Balance Check Reader & Device Test Console | Games & Rides | 3 | 1 | yes |
| `BO-414` | Wallet & Credit Management Dashboard | Games & Rides | 3 | 2 | yes |
| `BO-415` | Wallet & Credit Type Configuration | Games & Rides | 3 | 2 | yes |
| `BO-416` | Wallet Account & Balance View | Games & Rides | 3 | 8 | yes |
| `BO-417` | Top-Up Configuration | Games & Rides | 3 | 2 | yes |
| `BO-418` | Top-Up Bonus Rule Configuration | Games & Rides | 3 | 2 | yes |
| `BO-419` | Bonus Usage Restrictions | Games & Rides | 3 | 1 | yes |
| `BO-420` | Bonus Validity & Expiry Configuration | Games & Rides | 3 | 2 | yes |
| `BO-421` | Free Game & Ride Credit Management | Games & Rides | 3 | 2 | yes |
| `BO-422` | Refund, Adjustment & Manual Bonus Control | Games & Rides | 3 | 2 | yes |
| `BO-423` | Wallet Credit Transaction Ledger & Audit | Games & Rides | 3 | 1 | yes |
| `BO-424` | Gameplay Validation Command Center | Games & Rides | 3 | 2 | yes |
| `BO-425` | Gameplay Validation Rule Configuration | Games & Rides | 3 | 2 | yes |
| `BO-426` | Deduction Priority & Funding Source Rules | Games & Rides | 3 | 1 | yes |
| `BO-427` | All Games & Rides Pass Configuration | Games & Rides | 3 | 2 | yes |
| `BO-428` | Specific Game/Ride Unlimited Entitlement | Games & Rides | 3 | 1 | yes |
| `BO-429` | Specific Game/Ride Limited Entitlement | Games & Rides | 3 | 1 | yes |
| `BO-430` | Game Package Builder | Games & Rides | 3 | 2 | yes |
| `BO-431` | Entitlement Validity & Activation Rules | Games & Rides | 3 | 1 | yes |
| `BO-432` | Real-Time Gameplay Authorization | Games & Rides | 3 | 0 | yes |
| `BO-433` | Validation Simulator & Exception Analysis | Games & Rides | 3 | 1 | yes |
| `BO-434` | Game & Ride Pricing Command Center | Games & Rides | 3 | 1 | yes |
| `BO-435` | Standard Game & Ride Price Configuration | Games & Rides | 3 | 1 | yes |
| `BO-436` | Group Pricing Configuration | Games & Rides | 3 | 1 | yes |
| `BO-437` | Peak / Non-Peak Dynamic Pricing | Games & Rides | 3 | 1 | yes |
| `BO-438` | Pricing Calendar & Exception Dates | Games & Rides | 3 | 1 | yes |
| `BO-439` | Normal & VIP Pricing Configuration | Games & Rides | 3 | 1 | yes |
| `BO-440` | Retry Price Configuration | Games & Rides | 3 | 1 | yes |
| `BO-441` | Price Priority & Conflict Rules | Sell | 3 | 2 | yes |
| `BO-442` | Effective Pricing & Reader Price Preview | Games & Rides | 3 | 1 | yes |
| `BO-443` | Pricing Audit, Approval & Publication | Games & Rides | 3 | 3 | yes |
| `BO-444` | Redemption Operations Dashboard | Games & Rides | 3 | 0 | yes |
| `BO-445` | Redemption Credit Rule Configuration | Games & Rides | 3 | 1 | yes |
| `BO-446` | Ticket-Based Redemption / Ticket-Eater Integration | Games & Rides | 3 | 1 | yes |
| `BO-447` | Ticketless Redemption Game Integration | Games & Rides | 3 | 2 | yes |
| `BO-448` | Redemption Wallet & Balance View | Games & Rides | 3 | 1 | yes |
| `BO-449` | Redemption Counter / Prize Checkout | Games & Rides | 3 | 3 | yes |
| `BO-450` | Prize Catalogue & Credit Cost Configuration | Games & Rides | 3 | 3 | yes |
| `BO-451` | Prize Inventory Integration | Games & Rides | 3 | 3 | yes |
| `BO-452` | Direct-Pay / Crane & Prize Machine Configuration | Games & Rides | 3 | 4 | yes |
| `BO-453` | Redemption Transaction Ledger, Reconciliation & Audit | Games & Rides | 3 | 2 | yes |
| `BO-454` | Card Lifecycle Command Center | Games & Rides | 3 | 1 | yes |
| `BO-455` | Card / Credential Profile | Games & Rides | 3 | 1 | yes |
| `BO-456` | Card Expiry Rule Configuration | Games & Rides | 3 | 1 | yes |
| `BO-457` | Last Recharge & Last Activity Tracking | Games & Rides | 3 | 1 | yes |
| `BO-458` | Expiry Monitoring & Upcoming Expiration | Games & Rides | 3 | 0 | yes |
| `BO-459` | Card Expiry Runtime Validation | Games & Rides | 3 | 1 | yes |
| `BO-460` | Card Block, Suspend & Reactivation Control | Games & Rides | 3 | 1 | yes |
| `BO-461` | Card Replacement & Wallet Relinking | Games & Rides | 3 | 2 | yes |
| `BO-462` | Customer Balance & Credential Status View | Games & Rides | 3 | 1 | yes |
| `BO-463` | Card Lifecycle Audit & History | Games & Rides | 3 | 1 | yes |
| `BO-464` | Game & Ride Operations Control Center | Games & Rides | 3 | 1 | yes |
| `BO-465` | Live Gameplay Transaction Monitor | Games & Rides | 3 | 1 | yes |
| `BO-466` | Reader & Device Health Monitor | Games & Rides | 3 | 2 | yes |
| `BO-467` | Tap Validation & Decision Trace | Games & Rides | 3 | 1 | yes |
| `BO-468` | Rejected Transaction & Reason Analysis | Games & Rides | 3 | 1 | yes |
| `BO-469` | Wallet & Deduction Transaction Monitor | Games & Rides | 3 | 1 | yes |
| `BO-470` | Entitlement & Free-Play Consumption Monitor | Games & Rides | 3 | 1 | yes |
| `BO-471` | Offline, Synchronization & Recovery Monitor | Games & Rides | 3 | 2 | yes |
| `BO-473` | Operational Analytics & Reconciliation Dashboard | Games & Rides | 3 | 1 | yes |
| `BO-474` | Reader Integration Command Center | Games & Rides | 3 | 1 | yes |
| `BO-475` | Reader Manufacturer & Model Profile | Games & Rides | 3 | 2 | yes |
| `BO-476` | Communication Protocol Configuration | Games & Rides | 3 | 1 | yes |
| `BO-477` | Reader Command & Event Mapping | Games & Rides | 3 | 0 | yes |
| `BO-478` | Reader Configuration Deployment & Synchronization | Games & Rides | 3 | 1 | yes |
| `BO-479` | Game Trigger & I/O Control Mapping | Games & Rides | 3 | 1 | yes |
| `BO-480` | Reader Screen, LED & Sound Output Mapping | Games & Rides | 3 | 1 | yes |
| `BO-481` | Edge Cache & Offline Rule Package | Games & Rides | 3 | 1 | yes |
| `BO-482` | Device Diagnostics & Integration Logs | Games & Rides | 3 | 1 | yes |
| `BO-483` | Integration Certification & Test Console | Games & Rides | 3 | 0 | yes |
| `BO-484` | Self-Service Experience Command Center | Games & Rides | 3 | 0 | yes |
| `BO-485` | Self-Service Kiosk Profile & Channel Configuration | Games & Rides | 3 | 1 | yes |
| `BO-486` | Customer Card / Wallet Identification | Games & Rides | 3 | 1 | yes |
| `BO-487` | Customer Wallet & Balance Summary | Games & Rides | 3 | 3 | yes |
| `BO-488` | Self-Service Wallet Top-Up | Games & Rides | 3 | 2 | yes |
| `BO-489` | Bonus, Free Game & Benefit View | Games & Rides | 3 | 1 | yes |
| `BO-490` | Game & Ride Eligibility / “What Can I Play?” | Games & Rides | 3 | 1 | yes |
| `BO-491` | Redemption Balance & Prize Discovery | Games & Rides | 3 | 1 | yes |
| `BO-492` | Customer Game & Wallet Transaction History | Games & Rides | 3 | 1 | yes |
| `BO-493` | Self-Service UI Theme, Language & Journey Configuration | Games & Rides | 3 | 1 | yes |
| `BO-494` | Rental Product Command Center | Rentals | 3 | 4 | yes |
| `BO-495` | Create Rental Product Wizard | Rentals | 3 | 2 | yes |
| `BO-496` | Rental Product Profile | Rentals | 3 | 2 | yes |
| `BO-497` | Rental Category & Classification Setup | Rentals | 3 | 2 | yes |
| `BO-498` | Inventory Tracking Model | Rentals | 3 | 1 | yes |
| `BO-499` | Rental Location Assignment | Rentals | 3 | 1 | yes |
| `BO-500` | Rental Duration & Turnaround Configuration | Rentals | 3 | 1 | yes |
| `BO-501` | Rental Rules & Operational Policy | Rentals | 3 | 1 | yes |
| `BO-502` | Customer Requirements, Agreement & Waiver | Rentals | 3 | 1 | yes |
| `BO-503` | Product Validation, Approval & Publication | Rentals | 3 | 3 | yes |
| `BO-504` | Rental Inventory Command Center | Rentals | 3 | 2 | yes |
| `BO-505` | Serialized Equipment Registry | Rentals | 3 | 1 | yes |
| `BO-506` | Equipment / Asset Profile | Rentals | 3 | 2 | yes |
| `BO-507` | Pooled Inventory Management | Rentals | 3 | 3 | yes |
| `BO-508` | Equipment Status & Condition Management | Rentals | 3 | 2 | yes |
| `BO-509` | QR / Barcode Equipment Identification | Rentals | 3 | 1 | yes |
| `BO-510` | Inventory Location Allocation | Rentals | 3 | 1 | yes |
| `BO-511` | Inventory Transfer Management | Rentals | 3 | 3 | yes |
| `BO-512` | Inventory Adjustment & Exception Management | Rentals | 3 | 2 | yes |
| `BO-513` | Inventory Intelligence & Rebalancing | Rentals | 3 | 2 | yes |
| `BO-514` | Availability Command Center | Rentals | 3 | 1 | yes |
| `BO-515` | Availability Rule Configuration | Rentals | 3 | 1 | yes |
| `BO-516` | Operating Hours & Rental Windows | Rentals | 3 | 1 | yes |
| `BO-517` | Timeslot & Duration Availability Setup | Rentals | 3 | 1 | yes |
| `BO-518` | Real-Time Availability Calendar | Rentals | 3 | 2 | yes |
| `BO-519` | Resource / Equipment Calendar | Rentals | 3 | 1 | yes |
| `BO-520` | Blackout, Closure & Capacity Blocking | Rentals | 3 | 3 | yes |
| `BO-521` | Overlap & Conflict Engine | Rentals | 3 | 1 | yes |
| `BO-522` | Inventory Holds, Buffers & Release Rules | Rentals | 3 | 1 | yes |
| `BO-523` | Availability Intelligence & AI Forecasting | Rentals | 3 | 1 | yes |
| `BO-524` | Rental Pricing Command Center | Rentals | 3 | 2 | yes |
| `BO-525` | Pricing Profile Builder | Rentals | 3 | 2 | yes |
| `BO-526` | Duration & Tiered Pricing Configuration | Rentals | 3 | 1 | yes |
| `BO-527` | Calendar, Peak & Seasonal Pricing | Rentals | 3 | 1 | yes |
| `BO-528` | Dynamic Pricing & AI Recommendation | Rentals | 3 | 0 | yes |
| `BO-529` | Deposit & Security Hold Policy | Rentals | 3 | 1 | yes |
| `BO-530` | Deposit Lifecycle & Settlement Rules | Rentals | 3 | 1 | yes |
| `BO-531` | Late Fee, Grace Period & Extension Pricing | Rentals | 3 | 1 | yes |
| `BO-532` | Commercial Exceptions, Waivers & Overrides | Rentals | 3 | 1 | yes |
| `BO-533` | Pricing Simulation, Validation & AI Commercial Intelligence | Rentals | 3 | 2 | yes |
| `BO-534` | Rental Booking Command Center | Rentals | 3 | 1 | yes |
| `BO-535` | New Rental Booking Wizard | Rentals | 3 | 2 | yes |
| `BO-536` | Availability Selection & Alternative Options | Rentals | 3 | 1 | yes |
| `BO-537` | Customer & Participant Information | Rentals | 3 | 1 | yes |
| `BO-538` | Group Rental & Participant Management | Rentals | 3 | 2 | yes |
| `BO-539` | Rental Agreement & Waiver Completion | Rentals | 3 | 1 | yes |
| `BO-540` | Booking Commercial Summary & Payment | Rentals | 3 | 1 | yes |
| `BO-541` | Reservation Confirmation & QR Voucher | Rentals | 3 | 1 | yes |
| `BO-542` | Reservation Modification, Cancellation & No-Show | Rentals | 3 | 1 | yes |
| `BO-543` | Reservation Detail, Timeline & Readiness | Rentals | 3 | 1 | yes |
| `BO-544` | Rental Checkout Command Center | Rentals | 3 | 1 | yes |
| `BO-545` | Voucher Scan & Reservation Retrieval | Rentals | 3 | 1 | yes |
| `BO-546` | Checkout Readiness Validation | Rentals | 3 | 1 | yes |
| `BO-547` | Equipment Assignment Workspace | Rentals | 3 | 2 | yes |
| `BO-548` | Equipment Scan & Validation | Rentals | 3 | 2 | yes |
| `BO-549` | Pre-Rental Condition Inspection | Rentals | 3 | 1 | yes |
| `BO-550` | Safety & Handover Checklist | Rentals | 3 | 1 | yes |
| `BO-551` | Deposit & Financial Handover Validation | Rentals | 3 | 1 | yes |
| `BO-552` | Group & Multi-Item Checkout | Rentals | 3 | 1 | yes |
| `BO-553` | Checkout Confirmation & Rental Activation | Rentals | 3 | 1 | yes |
| `BO-554` | Active Rental Operations Command Center | Rentals | 3 | 2 | yes |
| `BO-555` | Active Rental Detail & Live Timeline | Rentals | 3 | 1 | yes |
| `BO-556` | Rental Extension Request | Rentals | 3 | 1 | yes |
| `BO-557` | Extension Pricing & Confirmation | Rentals | 3 | 2 | yes |
| `BO-558` | Equipment Swap / Replacement | Rentals | 3 | 1 | yes |
| `BO-559` | Rental Incident & Operational Exception | Rentals | 3 | 1 | yes |
| `BO-560` | Due Soon & Customer Notification Management | Rentals | 3 | 1 | yes |
| `BO-561` | Overdue Rental Management | Rentals | 3 | 1 | yes |
| `BO-562` | Active Group Rental Management | Rentals | 3 | 1 | yes |
| `BO-563` | Active Rental Intelligence & Operational Alerts | Rentals | 3 | 1 | yes |
| `BO-564` | Rental Return Command Center | Rentals | 3 | 1 | yes |
| `BO-565` | Return Scan & Rental Retrieval | Rentals | 3 | 1 | yes |
| `BO-566` | Return Summary & Actual Return Time | Rentals | 3 | 1 | yes |
| `BO-567` | Post-Rental Condition Inspection | Rentals | 3 | 1 | yes |
| `BO-568` | Before vs After Condition Comparison | Rentals | 3 | 1 | yes |
| `BO-569` | Damage Assessment & Charge Workflow | Rentals | 3 | 1 | yes |
| `BO-570` | Partial Return & Missing Equipment | Rentals | 3 | 1 | yes |
| `BO-571` | Late Fees, Damage Fees & Final Settlement | Rentals | 3 | 1 | yes |
| `BO-572` | Deposit Release, Capture & Customer Confirmation | Rentals | 3 | 2 | yes |
| `BO-573` | Return Completion & Equipment Disposition | Rentals | 3 | 1 | yes |
| `BO-574` | Maintenance Command Center | Rentals | 3 | 2 | yes |
| `BO-575` | Maintenance Rule & Service Plan Configuration | Rentals | 3 | 3 | yes |
| `BO-576` | Maintenance Calendar & Scheduling | Rentals | 3 | 3 | yes |
| `BO-577` | Maintenance Work Order | Rentals | 3 | 11 | yes |
| `BO-578` | Technician Repair Workspace | Rentals | 3 | 6 | yes |
| `BO-579` | Parts, Cost & Maintenance Expense Tracking | Rentals | 3 | 4 | yes |
| `BO-580` | Asset Maintenance History & Lifecycle | Rentals | 3 | 1 | yes |
| `BO-581` | Return-to-Service Inspection & Approval | Rentals | 3 | 3 | yes |
| `BO-582` | Asset Retirement, Write-Off & Replacement Recommendation | Rentals | 3 | 2 | yes |
| `BO-583` | Maintenance Intelligence & Predictive AI | Rentals | 3 | 1 | yes |
| `BO-584` | Rental Executive Command Center | Rentals | 3 | 1 | yes |
| `BO-585` | Rental Revenue & Commercial Analytics | Rentals | 3 | 1 | yes |
| `BO-586` | Utilization & Capacity Analytics | Rentals | 3 | 1 | yes |
| `BO-587` | Inventory & Equipment Performance Analytics | Rentals | 3 | 0 | yes |
| `BO-588` | Rental Duration, Extension & Return Analytics | Rentals | 3 | 1 | yes |
| `BO-589` | Damage, Loss, Deposit & Exception Analytics | Rentals | 3 | 1 | yes |
| `BO-590` | Location & Channel Performance | Rentals | 3 | 1 | yes |
| `BO-591` | Rental Forecasting & Demand Intelligence | Rentals | 3 | 1 | yes |
| `BO-592` | Audit, Governance & Operational Control | Rentals | 3 | 1 | yes |
| `BO-593` | AI Rental Management Copilot & Action Center | Rentals | 3 | 1 | yes |
| `BO-594` | Environment Ready & Handoff to AI Setup | Setup & Go-Live | 3 | 1 | yes |
| `BO-595` | AI Setup Command Center | Setup & Go-Live | 3 | 1 | yes |
| `BO-596` | Guided Setup Plan | Setup & Go-Live | 3 | 1 | yes |
| `BO-597` | AI Configuration Workspace | Setup & Go-Live | 3 | 2 | yes |
| `BO-598` | AI Draft Review & Approval | Setup & Go-Live | 3 | 3 | yes |
| `BO-599` | Manual Configuration Center | Setup & Go-Live | 3 | 0 | yes |
| `BO-600` | Venue, Calendar & Operational Setup | Setup & Go-Live | 3 | 1 | yes |
| `BO-601` | Product, Pricing & Sales Channel Setup | Setup & Go-Live | 3 | 3 | yes |
| `BO-602` | POS, Payment & Access Setup | Setup & Go-Live | 3 | 1 | yes |
| `BO-603` | Configuration Health & AI Review | Setup & Go-Live | 3 | 1 | yes |
| `BO-604` | Setup Completion & Handoff to Go-Live | Setup & Go-Live | 3 | 1 | yes |
| `BO-605` | Go-Live Readiness Command Center | Setup & Go-Live | 3 | 1 | yes |
| `BO-606` | Automated Validation Plan | Setup & Go-Live | 3 | 1 | yes |
| `BO-607` | Ticketing & Product Validation | Setup & Go-Live | 3 | 1 | yes |
| `BO-608` | End-to-End Sales Channel Testing | Setup & Go-Live | 3 | 1 | yes |
| `BO-609` | Payment & Financial Validation | Setup & Go-Live | 3 | 1 | yes |
| `BO-610` | Ticket, QR & Access Validation | Setup & Go-Live | 3 | 1 | yes |
| `BO-611` | User, Security & Integration Validation | Setup & Go-Live | 3 | 1 | yes |
| `BO-612` | Communication & Customer Journey Validation | Setup & Go-Live | 3 | 1 | yes |
| `BO-613` | Blocker, Warning & AI Resolution Center | Setup & Go-Live | 3 | 1 | yes |
| `BO-614` | Final Go-Live Approval & Production Launch | Setup & Go-Live | 3 | 1 | yes |
| `BO-615` | Accreditation Command Center | Access & Venue | 3 | 5 | yes |
| `BO-616` | Accreditation Application Directory | Access & Venue | 3 | 2 | yes |
| `BO-617` | New Accreditation Application | Access & Venue | 3 | 3 | yes |
| `BO-618` | Accreditation Form Builder | Access & Venue | 3 | 4 | yes |
| `BO-619` | Accreditation Category Management | Access & Venue | 3 | 2 | yes |
| `BO-620` | Accreditation Program Setup | Access & Venue | 3 | 4 | yes |
| `BO-621` | Applicant Type Configuration | Access & Venue | 3 | 1 | yes |
| `BO-622` | Application Requirements Matrix | Access & Venue | 3 | 1 | yes |
| `BO-623` | Accreditation Intake Monitor | Access & Venue | 3 | 2 | yes |
| `BO-624` | Registration Rules & Publication | Access & Venue | 3 | 1 | yes |
| `BO-625` | Accreditation Holder Directory | Access & Venue | 3 | 1 | yes |
| `BO-626` | Accreditation Holder Profile | Access & Venue | 3 | 1 | yes |
| `BO-627` | Identity Details & Verification | Access & Venue | 3 | 2 | yes |
| `BO-628` | Photo Management | Access & Venue | 3 | 2 | yes |
| `BO-629` | Document Repository | Access & Venue | 3 | 2 | yes |
| `BO-630` | Document Verification Queue | Access & Venue | 3 | 2 | yes |
| `BO-631` | Duplicate & Identity Conflict Detection | Access & Venue | 3 | 2 | yes |
| `BO-632` | Organization & Affiliation Management | Access & Venue | 3 | 1 | yes |
| `BO-633` | Profile Completeness & Compliance Monitor | Access & Venue | 3 | 1 | yes |
| `BO-634` | Profile History & Audit Timeline | Access & Venue | 3 | 1 | yes |
| `BO-635` | Accreditation Review Queue | Access & Venue | 3 | 3 | yes |
| `BO-636` | Application Review Workspace | Access & Venue | 3 | 5 | yes |
| `BO-637` | Approval Workflow Builder | Access & Venue | 3 | 1 | yes |
| `BO-638` | Approval Rules & Conditions | Access & Venue | 3 | 1 | yes |
| `BO-639` | Reviewer Assignment & Delegation | Access & Venue | 3 | 1 | yes |
| `BO-640` | Rejection & Resubmission Management | Access & Venue | 3 | 5 | yes |
| `BO-641` | Escalation & Exception Management | Access & Venue | 3 | 1 | yes |
| `BO-642` | Approval Decision History | Access & Venue | 3 | 1 | yes |
| `BO-643` | Approval Policy Validation & Publication | Access & Venue | 3 | 4 | yes |
| `BO-644` | Credential Issuance Command Center | Access & Venue | 3 | 3 | yes |
| `BO-645` | Credential Generation Workspace | Access & Venue | 3 | 2 | yes |
| `BO-646` | Credential Media Configuration | Access & Venue | 3 | 0 | yes |
| `BO-647` | Badge Template Designer | Access & Venue | 3 | 2 | yes |
| `BO-648` | Badge Printing & Print Queue | Access & Venue | 3 | 2 | yes |
| `BO-649` | Digital & Mobile Credential Management | Access & Venue | 3 | 2 | yes |
| `BO-650` | NFC & RFID Credential Encoding | Access & Venue | 3 | 4 | yes |
| `BO-651` | Credential Activation & Delivery | Access & Venue | 3 | 2 | yes |
| `BO-653` | Credential Registry & Credential History | Access & Venue | 3 | 2 | yes |
| `BO-654` | Accreditation Access Command Center | Access & Venue | 3 | 1 | yes |
| `BO-655` | Access Profile Management | Access & Venue | 3 | 2 | yes |
| `BO-656` | Venue & Zone Access Matrix | Access & Venue | 3 | 2 | yes |
| `BO-657` | Operational Area Permission Management | Access & Venue | 3 | 2 | yes |
| `BO-658` | Date & Time Access Rules | Access & Venue | 3 | 2 | yes |
| `BO-659` | Access Schedule Management | Access & Venue | 3 | 1 | yes |
| `BO-660` | Holder Access Assignment | Access & Venue | 3 | 3 | yes |
| `BO-661` | Temporary Access & Exception Management | Access & Venue | 3 | 1 | yes |
| `BO-662` | Access Revocation & Suspension | Access & Venue | 3 | 1 | yes |
| `BO-663` | Access Rights Preview, Impact & Synchronization | Access & Venue | 3 | 1 | yes |
| `BO-664` | Accreditation Lifecycle Command Center | Access & Venue | 3 | 1 | yes |
| `BO-665` | Accreditation Status Workflow | Access & Venue | 3 | 1 | yes |
| `BO-666` | Validity Period Configuration | Access & Venue | 3 | 1 | yes |
| `BO-667` | Event & Venue Accreditation Assignment | Access & Venue | 3 | 3 | yes |
| `BO-668` | Multi-Venue Accreditation Management | Access & Venue | 3 | 2 | yes |
| `BO-669` | Temporary & Seasonal Accreditation | Access & Venue | 3 | 0 | yes |
| `BO-670` | Suspension & Reactivation Management | Access & Venue | 3 | 1 | yes |
| `BO-671` | Accreditation Revocation Management | Access & Venue | 3 | 1 | yes |
| `BO-672` | Expiry Monitor & Expiration Rules | Access & Venue | 3 | 3 | yes |
| `BO-673` | Accreditation Renewal Workspace | Access & Venue | 3 | 2 | yes |
| `BO-674` | Accreditation Communications Command Center | Access & Venue | 3 | 0 | yes |
| `BO-675` | Notification Rule Management | Access & Venue | 3 | 1 | yes |
| `BO-676` | Expiry & Renewal Notification Scheduler | Access & Venue | 3 | 1 | yes |
| `BO-677` | Communication Template Library | Access & Venue | 3 | 0 | yes |
| `BO-678` | Channel, Language & Branding Configuration | Access & Venue | 3 | 0 | yes |
| `BO-679` | Manual & Bulk Communication Center | Access & Venue | 3 | 0 | yes |
| `BO-680` | Accreditation Bulk Import | Access & Venue | 3 | 1 | yes |
| `BO-681` | Import Validation & Processing Monitor | Access & Venue | 3 | 0 | yes |
| `BO-682` | Accreditation Export & Data Extract Center | Access & Venue | 3 | 4 | yes |
| `BO-683` | Delivery, Batch & Operational History | Access & Venue | 3 | 1 | yes |
| `BO-684` | Accreditation Executive Dashboard | Access & Venue | 3 | 2 | yes |
| `BO-685` | Accreditation Status & Portfolio Reporting | Access & Venue | 3 | 2 | yes |
| `BO-686` | Accreditation Utilization Analytics | Access & Venue | 3 | 1 | yes |
| `BO-687` | Accreditation Access Activity Reporting | Access & Venue | 3 | 1 | yes |
| `BO-688` | Accreditation Trend & Comparative Analysis | Access & Venue | 3 | 1 | yes |
| `BO-689` | Accreditation Audit Reporting | Access & Venue | 3 | 1 | yes |
| `BO-690` | Immutable Accreditation Audit Log | Access & Venue | 3 | 1 | yes |
| `BO-691` | Accreditation API Management | Access & Venue | 3 | 1 | yes |
| `BO-692` | Accreditation Webhook Management | Access & Venue | 3 | 5 | yes |
| `BO-693` | Integration & Data Exchange Monitor | Access & Venue | 3 | 1 | yes |
| `BO-694` | Event Catalogue Command Center | Sell | 3 | 1 | yes |
| `BO-695` | Event Type & Behaviour Configuration | Sell | 3 | 2 | yes |
| `BO-696` | Event Duplication & Clone Configuration | Sell | 3 | 2 | yes |
| `BO-697` | Event Schedule Command Center | Sell | 3 | 2 | yes |
| `BO-698` | Dynamic Performance Duration Configuration | Sell | 3 | 2 | yes |
| `BO-699` | Schedule Change & Rescheduling Configuration | Sell | 3 | 2 | yes |
| `BO-700` | Venue & Space Command Center | Sell | 3 | 1 | yes |
| `BO-701` | Venue Master Configuration | Sell | 3 | 2 | yes |
| `BO-702` | Space Access Rules Configuration | Sell | 3 | 2 | yes |
| `BO-703` | Seating & Capacity Command Center | Sell | 3 | 2 | yes |
| `BO-704` | Event Capacity Profile Configuration | Sell | 3 | 2 | yes |
| `BO-705` | Seating Mode & Reservation Configuration | Sell | 3 | 2 | yes |
| `BO-706` | Registration & Attendance Command Center | Sell | 3 | 2 | yes |
| `BO-707` | Attendee Data & Registration Form Configuration | Sell | 3 | 2 | yes |
| `BO-708` | Accreditation & Participant Category Configuration | Sell | 3 | 2 | yes |
| `BO-709` | Event Admission & Entry Policy Configuration | Sell | 3 | 2 | yes |
| `BO-710` | Event Resource Command Center | Sell | 3 | 1 | yes |
| `BO-711` | Event Resource Requirement Configuration | Sell | 3 | 2 | yes |
| `BO-712` | Staff & Role Assignment Configuration | Sell | 3 | 4 | yes |
| `BO-713` | Contractor & External Workforce Configuration | Sell | 3 | 2 | yes |
| `BO-714` | Event Shift & Roster Configuration | Sell | 3 | 4 | yes |
| `BO-715` | Resource Location & Deployment Configuration | Sell | 3 | 2 | yes |
| `BO-716` | Event Lifecycle & Change Command Center | Sell | 3 | 2 | yes |
| `BO-717` | Lifecycle Transition Configuration | Sell | 3 | 2 | yes |
| `BO-718` | Event Change Request Configuration | Sell | 3 | 1 | yes |
| `BO-719` | Event Cancellation Workflow Configuration | Sell | 3 | 2 | yes |
| `BO-720` | Ticket, Reservation & Customer Treatment Configuration | Sell | 3 | 2 | yes |
| `BO-721` | Activity Performance & Slot Template Configuration | Sell | 3 | 2 | yes |
| `BO-722` | Prepaid Minute Package & Customer Balance Configuration | Sell | 3 | 2 | yes |
| `BO-723` | Peak, Off-Peak & Super Prime Time Configuration | Sell | 3 | 2 | yes |
| `BO-724` | Walk-In / There-and-Then Booking Configuration | Sell | 3 | 2 | yes |
| `BO-725` | Performance Operations Command Center | Sell | 3 | 2 | yes |
| `BO-726` | Participant Photo & Video Assignment | Sell | 3 | 2 | yes |
| `BO-727` | F&B Command Center | Operations | 3 | 1 | yes |
| `BO-728` | Outlet Management | Operations | 3 | 0 | yes |
| `BO-729` | Create / Edit Outlet | Operations | 3 | 0 | yes |
| `BO-730` | Outlet Types & Templates | Operations | 3 | 2 | yes |
| `BO-731` | Operating Hours & Service Periods | Operations | 3 | 2 | yes |
| `BO-732` | POS & Device Assignment | Operations | 3 | 3 | yes |
| `BO-733` | Service Channel Configuration | Operations | 3 | 2 | yes |
| `BO-734` | CRM Command Center | Engagement & Support | 3 | 2 | yes |
| `BO-735` | Guest Directory | Engagement & Support | 3 | 7 | yes |
| `BO-736` | Guest Master Configuration | Engagement & Support | 3 | 3 | yes |
| `BO-737` | Customer 360 Profile | Engagement & Support | 3 | 6 | yes |
| `BO-738` | Activity Timeline | Engagement & Support | 3 | 3 | yes |
| `BO-739` | Contact & Preferences | Engagement & Support | 3 | 3 | yes |
| `BO-740` | Family & Guardians | Engagement & Support | 3 | 4 | yes |
| `BO-741` | Corporate & Groups | Engagement & Support | 3 | 2 | yes |
| `BO-742` | Commerce & Documents | Engagement & Support | 3 | 1 | yes |
| `BO-743` | AI Guest Intelligence | Engagement & Support | 3 | 1 | yes |
| `BO-744` | Data Governance Center | Engagement & Support | 3 | 2 | yes |
| `BO-745` | Identity Resolution Rules | Engagement & Support | 3 | 4 | yes |
| `BO-746` | Duplicate Review & Merge | Engagement & Support | 3 | 3 | yes |
| `BO-747` | Consent Policy Configuration | Engagement & Support | 3 | 4 | yes |
| `BO-748` | Consent Capture & Versions | Engagement & Support | 3 | 2 | yes |
| `BO-749` | Guest Preference Center | Engagement & Support | 3 | 2 | yes |
| `BO-750` | Data Subject Requests | Engagement & Support | 3 | 3 | yes |
| `BO-751` | Retention & Anonymization | Engagement & Support | 3 | 3 | yes |
| `BO-752` | Privacy & AI Governance | Engagement & Support | 3 | 2 | yes |
| `BO-753` | Compliance Audit Dashboard | Engagement & Support | 3 | 1 | yes |
| `BO-754` | Audience Intelligence | Engagement & Support | 3 | 2 | yes |
| `BO-755` | Dynamic Segment Builder | Engagement & Support | 3 | 3 | yes |
| `BO-756` | Static Lists & Imports | Engagement & Support | 3 | 2 | yes |
| `BO-757` | Behavioral Segmentation | Engagement & Support | 3 | 3 | yes |
| `BO-758` | Membership & Loyalty Segments | Engagement & Support | 3 | 2 | yes |
| `BO-759` | Demographic & Geographic | Engagement & Support | 3 | 1 | yes |
| `BO-760` | Revenue & Engagement Segments | Engagement & Support | 3 | 2 | yes |
| `BO-761` | AI Audience Discovery | Engagement & Support | 3 | 2 | yes |
| `BO-762` | Predictive Audiences | Engagement & Support | 3 | 4 | yes |
| `BO-763` | Activation & Governance | Engagement & Support | 3 | 2 | yes |
| `BO-764` | Campaign Command Center | Engagement & Support | 3 | 2 | yes |
| `BO-765` | Campaign Library & Calendar | Engagement & Support | 3 | 1 | yes |
| `BO-766` | Campaign Builder | Engagement & Support | 3 | 5 | yes |
| `BO-767` | Audience & Offer Selection | Engagement & Support | 3 | 2 | yes |
| `BO-768` | Multichannel Composer | Engagement & Support | 3 | 2 | yes |
| `BO-769` | Schedule & Trigger Rules | Engagement & Support | 3 | 2 | yes |
| `BO-770` | Campaign Approval Workflow | Engagement & Support | 3 | 1 | yes |
| `BO-771` | Budget, Goals & Forecast | Engagement & Support | 3 | 2 | yes |
| `BO-772` | A/B & AI Optimization | Engagement & Support | 3 | 6 | yes |
| `BO-773` | Attribution & Audit | Engagement & Support | 3 | 1 | yes |
| `BO-774` | Journey Automation Center | Engagement & Support | 3 | 2 | yes |
| `BO-775` | Visual Journey Builder | Engagement & Support | 3 | 2 | yes |
| `BO-776` | Trigger Event Catalog | Engagement & Support | 3 | 2 | yes |
| `BO-777` | Decision Logic & Timing | Engagement & Support | 3 | 2 | yes |
| `BO-778` | Abandoned Cart Recovery | Engagement & Support | 3 | 1 | yes |
| `BO-779` | Lifecycle Journeys | Engagement & Support | 3 | 1 | yes |
| `BO-780` | Guest Engagement Journeys | Engagement & Support | 3 | 1 | yes |
| `BO-781` | Cross-Sell & Service Recovery | Engagement & Support | 3 | 1 | yes |
| `BO-782` | AI Journey Optimization | Engagement & Support | 3 | 4 | yes |
| `BO-783` | Journey Analytics & Audit | Engagement & Support | 3 | 2 | yes |
| `BO-784` | Communications Center | Engagement & Support | 3 | 1 | yes |
| `BO-785` | Template Library | Engagement & Support | 3 | 4 | yes |
| `BO-786` | Newsletter Builder | Engagement & Support | 3 | 2 | yes |
| `BO-787` | Content Blocks & Product Feed | Engagement & Support | 3 | 2 | yes |
| `BO-788` | Subscriptions & Preferences | Engagement & Support | 3 | 1 | yes |
| `BO-789` | Transactional Notification Rules | Engagement & Support | 3 | 3 | yes |
| `BO-790` | Scheduling, Priority & Approval | Engagement & Support | 3 | 1 | yes |
| `BO-791` | Delivery, Retry & Failover | Engagement & Support | 3 | 2 | yes |
| `BO-792` | Deliverability & Analytics | Engagement & Support | 3 | 1 | yes |
| `BO-793` | AI Content, Translation & Audit | Engagement & Support | 3 | 3 | yes |
| `BO-794` | Omnichannel Command Center | Engagement & Support | 3 | 1 | yes |
| `BO-795` | Unified Inbox | Engagement & Support | 3 | 2 | yes |
| `BO-796` | Guest Conversation 360 | Engagement & Support | 3 | 2 | yes |
| `BO-797` | AI Chatbot Configuration | Engagement & Support | 3 | 0 | yes |
| `BO-798` | Intent & Knowledge Management | Engagement & Support | 3 | 4 | yes |
| `BO-799` | Agent Workspace | Engagement & Support | 3 | 4 | yes |
| `BO-800` | Routing & Queue Management | Engagement & Support | 3 | 5 | yes |
| `BO-801` | Sales & Service Actions | Engagement & Support | 3 | 1 | yes |
| `BO-802` | Sentiment, Quality & Escalation | Engagement & Support | 3 | 2 | yes |
| `BO-803` | Chat Analytics & Audit | Engagement & Support | 3 | 1 | yes |
| `BO-804` | Case Command Center | Engagement & Support | 3 | 1 | yes |
| `BO-805` | Case Queue & Search | Engagement & Support | 3 | 3 | yes |
| `BO-806` | Case Creation | Engagement & Support | 3 | 2 | yes |
| `BO-807` | Classification & Workflow | Engagement & Support | 3 | 2 | yes |
| `BO-808` | Assignment & Workload | Engagement & Support | 3 | 3 | yes |
| `BO-809` | SLA Policy Configuration | Engagement & Support | 3 | 2 | yes |
| `BO-810` | Escalation Rules | Engagement & Support | 3 | 1 | yes |
| `BO-811` | Case Workspace | Engagement & Support | 3 | 3 | yes |
| `BO-812` | Service Recovery | Engagement & Support | 3 | 0 | yes |
| `BO-813` | Case Analytics & Audit | Engagement & Support | 3 | 1 | yes |
| `BO-814` | Voice of Customer Center | Engagement & Support | 3 | 1 | yes |
| `BO-815` | Survey Builder | Engagement & Support | 3 | 1 | yes |
| `BO-816` | Survey Triggers & Distribution | Engagement & Support | 3 | 1 | yes |
| `BO-817` | NPS, CSAT & CES Configuration | Engagement & Support | 3 | 0 | yes |
| `BO-818` | Survey Responses & Insights | Engagement & Support | 3 | 1 | yes |
| `BO-819` | Review Collection & Rating Rules | Engagement & Support | 3 | 1 | yes |
| `BO-820` | Moderation & Publishing | Engagement & Support | 3 | 1 | yes |
| `BO-821` | AI Sentiment & Topic Analysis | Engagement & Support | 3 | 1 | yes |
| `BO-822` | Service Recovery Automation | Engagement & Support | 3 | 0 | yes |
| `BO-823` | VOC Analytics & Audit | Engagement & Support | 3 | 1 | yes |
| `BO-824` | Gamification Command Center | Engagement & Support | 3 | 0 | yes |
| `BO-825` | Challenge Builder | Engagement & Support | 3 | 4 | yes |
| `BO-826` | Achievement & Badge Engine | Engagement & Support | 3 | 3 | yes |
| `BO-827` | Points & Activity Rules | Engagement & Support | 3 | 3 | yes |
| `BO-828` | Milestones & Reward Rules | Engagement & Support | 3 | 2 | yes |
| `BO-829` | Family, Team & Event Challenges | Engagement & Support | 3 | 1 | yes |
| `BO-830` | Referral & Streak Management | Engagement & Support | 3 | 1 | yes |
| `BO-831` | Progress, Leaderboards & Hub | Engagement & Support | 3 | 1 | yes |
| `BO-832` | AI Engagement Optimization | Engagement & Support | 3 | 1 | yes |
| `BO-833` | Gamification Analytics & Audit | Engagement & Support | 3 | 3 | yes |
| `BO-834` | Digital Experience Center | Engagement & Support | 3 | 2 | yes |
| `BO-835` | Site, Brand & Domain Setup | Engagement & Support | 3 | 1 | yes |
| `BO-836` | Design System & Components | Engagement & Support | 3 | 1 | yes |
| `BO-837` | Page & Landing Builder | Engagement & Support | 3 | 2 | yes |
| `BO-838` | Content, Media & Forms | Engagement & Support | 3 | 0 | yes |
| `BO-839` | Dynamic Product Pages | Engagement & Support | 3 | 1 | yes |
| `BO-840` | Mobile App CMS | Engagement & Support | 3 | 1 | yes |
| `BO-841` | Personalization & Localization | Engagement & Support | 3 | 0 | yes |
| `BO-842` | SEO Management | Engagement & Support | 3 | 2 | yes |
| `BO-843` | Publishing, Analytics & Audit | Engagement & Support | 3 | 2 | yes |
| `BO-844` | Waiver Command Center | Engagement & Support | 3 | 1 | yes |
| `BO-845` | Waiver Template Builder | Engagement & Support | 3 | 2 | yes |
| `BO-846` | Assignment Rules | Engagement & Support | 3 | 2 | yes |
| `BO-847` | Version, Expiry & Renewal | Engagement & Support | 3 | 1 | yes |
| `BO-848` | Signature Experience Setup | Engagement & Support | 3 | 2 | yes |
| `BO-849` | Guardian & Group Signing | Engagement & Support | 3 | 1 | yes |
| `BO-850` | Pre-Arrival Completion | Engagement & Support | 3 | 2 | yes |
| `BO-851` | Verification & Access Control | Engagement & Support | 3 | 1 | yes |
| `BO-852` | Documents, Search & Retention | Engagement & Support | 3 | 3 | yes |
| `BO-853` | Legal Evidence & Audit | Engagement & Support | 3 | 1 | yes |
| `BO-854` | Resource Management Command Center | Rentals | 3 | 3 | yes |
| `BO-855` | Resource Type Configuration | Rentals | 3 | 3 | yes |
| `BO-856` | Resource Category Management | Rentals | 3 | 3 | yes |
| `BO-857` | Resource Creation & Profile | Rentals | 3 | 7 | yes |
| `BO-858` | Configurable Attribute Builder | Rentals | 3 | 2 | yes |
| `BO-859` | Resource Hierarchy & Parent–Child Relationships | Rentals | 3 | 2 | yes |
| `BO-860` | Resource Dependency Rules | Rentals | 3 | 2 | yes |
| `BO-861` | Resource Package & Bundle Configuration | Rentals | 3 | 3 | yes |
| `BO-862` | Multi-Venue Resource Assignment | Rentals | 3 | 2 | yes |
| `BO-863` | Resource Lifecycle, Governance & Audit | Rentals | 3 | 4 | yes |
| `BO-864` | Resource Calendar Command Center | Rentals | 3 | 3 | yes |
| `BO-865` | Calendar Filters, Search & Smart Discovery | Rentals | 3 | 2 | yes |
| `BO-866` | Resource Availability Schedule Configuration | Rentals | 3 | 4 | yes |
| `BO-867` | Resource Time-Slot Configuration | Rentals | 3 | 2 | yes |
| `BO-868` | Advance Reservation Management | Rentals | 3 | 3 | yes |
| `BO-869` | Recurring Reservation Configuration | Rentals | 3 | 2 | yes |
| `BO-870` | Operational Time & Resource Blocking | Rentals | 3 | 3 | yes |
| `BO-871` | Multi-Event Resource Planning | Rentals | 3 | 2 | yes |
| `BO-872` | Smart Assignment & Drag-and-Drop Reallocation | Rentals | 3 | 2 | yes |
| `BO-873` | Staff Resource Directory | Rentals | 3 | 3 | yes |
| `BO-874` | Staff Resource Profile | Rentals | 3 | 4 | yes |
| `BO-875` | Skills & Competency Management | Rentals | 3 | 2 | yes |
| `BO-876` | Certification & Expiry Management | Rentals | 3 | 2 | yes |
| `BO-877` | Qualification & Assignment Rule Engine | Rentals | 3 | 2 | yes |
| `BO-878` | Staff Availability & Working Pattern | Rentals | 3 | 4 | yes |
| `BO-879` | Shift Template & Assignment Configuration | Rentals | 3 | 4 | yes |
| `BO-880` | Break, Leave & Absence Configuration | Rentals | 3 | 6 | yes |
| `BO-881` | Overtime & Working-Hour Rules | Rentals | 3 | 1 | yes |
| `BO-882` | Workforce Integration & Synchronization Center | Rentals | 3 | 8 | yes |
| `BO-883` | Workforce Roster Command Center | Rentals | 3 | 2 | yes |
| `BO-884` | Attraction & Operational Staffing Roster | Rentals | 3 | 4 | yes |
| `BO-885` | Minimum Staffing & Coverage Rule Configuration | Rentals | 3 | 1 | yes |
| `BO-886` | Staffing Gap & Coverage Control Center | Rentals | 3 | 3 | yes |
| `BO-887` | Shift Marketplace & Workforce Requests | Rentals | 3 | 2 | yes |
| `BO-888` | Attendance & Live Workforce Command Center | Rentals | 3 | 1 | yes |
| `BO-889` | Staff Check-In, Check-Out & Attendance Exceptions | Rentals | 3 | 2 | yes |
| `BO-890` | Workforce Compliance Validation Center | Rentals | 3 | 1 | yes |
| `BO-891` | Labor Cost & Staffing Budget Control | Rentals | 3 | 3 | yes |
| `BO-892` | AI Workforce Planner & Roster Optimization | Rentals | 3 | 1 | yes |
| `BO-893` | Experience Resource Requirement Builder | Rentals | 3 | 2 | yes |
| `BO-894` | Staff-to-Experience Qualification Mapping | Rentals | 3 | 3 | yes |
| `BO-895` | Resource Combination Builder | Rentals | 3 | 3 | yes |
| `BO-896` | Ticket Demand & Resource Capacity Mapping | Rentals | 3 | 1 | yes |
| `BO-897` | Customer Resource Selection Configuration | Rentals | 3 | 1 | yes |
| `BO-898` | Skill-Based & Smart Resource Selection | Rentals | 3 | 1 | yes |
| `BO-899` | Customer / Cashier Resource Assignment Experience | Rentals | 3 | 2 | yes |
| `BO-900` | Dynamic Resource Allocation Engine | Rentals | 3 | 2 | yes |
| `BO-901` | Priority, Scoring & Allocation Policy | Rentals | 3 | 2 | yes |
| `BO-902` | Automatic Replacement & Assignment Recovery | Rentals | 3 | 1 | yes |
| `BO-903` | Equipment & Asset Command Center | Rentals | 3 | 2 | yes |
| `BO-904` | Rental Resource Configuration | Rentals | 3 | 2 | yes |
| `BO-905` | Rental Inventory & Availability Control | Rentals | 3 | 2 | yes |
| `BO-906` | Resource Checkout Workspace | Rentals | 3 | 2 | yes |
| `BO-907` | Guest & Resource Assignment | Rentals | 3 | 2 | yes |
| `BO-908` | Rental Duration, Extension & Return Management | Rentals | 3 | 2 | yes |
| `BO-909` | Deposit & Rental Financial Control | Rentals | 3 | 2 | yes |
| `BO-910` | Maintenance & Resource Blocking | Rentals | 3 | 5 | yes |
| `BO-911` | Inspection, Condition & Compliance Management | Rentals | 3 | 4 | yes |
| `BO-912` | Asset Lifecycle, Depreciation & Retirement | Rentals | 3 | 4 | yes |
| `BO-913` | Event Resource Planning Command Center | Rentals | 3 | 1 | yes |
| `BO-914` | Event Resource Requirement Builder | Rentals | 3 | 2 | yes |
| `BO-915` | Venue & Space Allocation | Rentals | 3 | 2 | yes |
| `BO-916` | Equipment & Asset Allocation | Rentals | 3 | 1 | yes |
| `BO-917` | Event Staff & Personnel Allocation | Rentals | 3 | 1 | yes |
| `BO-918` | Event Resource Template Library | Rentals | 3 | 3 | yes |
| `BO-919` | AI Event Resource Forecasting | Rentals | 3 | 3 | yes |
| `BO-920` | Event Resource Cost Estimator | Rentals | 3 | 2 | yes |
| `BO-921` | Multi-Event Allocation & Conflict Optimizer | Rentals | 3 | 1 | yes |
| `BO-922` | Event Resource Approval & Readiness Gate | Rentals | 3 | 2 | yes |
| `BO-923` | AI Resource Intelligence Command Center | Rentals | 3 | 1 | yes |
| `BO-924` | Optimal Resource Recommendation Engine | Rentals | 3 | 1 | yes |
| `BO-925` | AI Staff Recommendation & Workforce Matching | Rentals | 3 | 2 | yes |
| `BO-926` | Resource Demand Forecasting | Rentals | 3 | 2 | yes |
| `BO-927` | AI Staffing Requirement Forecast | Rentals | 3 | 6 | yes |
| `BO-928` | AI Conflict Resolution Assistant | Rentals | 3 | 4 | yes |
| `BO-929` | Automatic Schedule Optimization | Rentals | 3 | 3 | yes |
| `BO-930` | Alternative & Replacement Resource | Rentals | 3 | 1 | yes |
| `BO-931` | Operational Scenario Simulator & Digital Twin | Rentals | 3 | 2 | yes |
| `BO-932` | Conversational AI Resource Copilot | Rentals | 3 | 3 | yes |
| `BO-933` | My Resource Operations Home | Rentals | 3 | 1 | yes |
| `BO-934` | My Schedule & Assignment Calendar | Rentals | 3 | 1 | yes |
| `BO-935` | Assignment Detail & Operational Brief | Rentals | 3 | 6 | yes |
| `BO-936` | Mobile Staff Check-In & Check-Out | Rentals | 3 | 1 | yes |
| `BO-937` | Resource Collection, Handover & Return | Rentals | 3 | 2 | yes |
| `BO-938` | Employee Requests & Resource Support | Rentals | 3 | 1 | yes |
| `BO-939` | Shift Change, Swap, Pickup & Release | Rentals | 3 | 2 | yes |
| `BO-940` | Manager Mobile Approval Center | Rentals | 3 | 2 | yes |
| `BO-941` | Operational Notifications & Live Alerts | Rentals | 3 | 1 | yes |
| `BO-942` | Mobile Operations Control & Offline Sync | Rentals | 3 | 0 | yes |
| `BO-943` | Resource Analytics Command Center | Rentals | 3 | 2 | yes |
| `BO-944` | Resource Utilization & Capacity Analytics | Rentals | 3 | 1 | yes |
| `BO-945` | Resource Cost, Revenue & Efficiency Analytics | Rentals | 3 | 5 | yes |
| `BO-946` | Demand Forecast Accuracy & Planning Performance | Rentals | 3 | 1 | yes |
| `BO-947` | Resource KPI, SLA & Performance Framework | Rentals | 3 | 1 | yes |
| `BO-948` | Resource Governance & Policy Center | Rentals | 3 | 2 | yes |
| `BO-949` | Approval, Exception & Override Control Center | Rentals | 3 | 1 | yes |
| `BO-950` | Audit Trail & Resource Decision History | Rentals | 3 | 1 | yes |
| `BO-951` | Resource Integration & System Health Center | Rentals | 3 | 1 | yes |
| `BO-952` | Executive Resource Intelligence & AI Improvement Center | Rentals | 3 | 1 | yes |
| `BO-953` | Seat Map Command Center | Access & Venue | 3 | 2 | yes |
| `BO-954` | Venue Canvas | Access & Venue | 3 | 3 | yes |
| `BO-955` | Sections & Zones | Access & Venue | 3 | 5 | yes |
| `BO-956` | Rows & Seats | Access & Venue | 3 | 2 | yes |
| `BO-957` | Standing Zones | Access & Venue | 3 | 2 | yes |
| `BO-958` | Suites & Boxes | Access & Venue | 3 | 2 | yes |
| `BO-959` | Stage & Focal Point | Access & Venue | 3 | 3 | yes |
| `BO-960` | Entrances, Exits & Aisles | Access & Venue | 3 | 2 | yes |
| `BO-961` | Amenities & Obstructions | Access & Venue | 3 | 2 | yes |
| `BO-962` | Templates, Validation & Publish | Access & Venue | 3 | 4 | yes |
| `BO-963` | Import Command Center | Access & Venue | 3 | 2 | yes |
| `BO-964` | PDF & Image Import | Access & Venue | 3 | 2 | yes |
| `BO-965` | SVG & CAD Import | Access & Venue | 3 | 2 | yes |
| `BO-966` | CSV & Excel Import | Access & Venue | 3 | 2 | yes |
| `BO-967` | AI Section Recognition | Access & Venue | 3 | 2 | yes |
| `BO-968` | AI Row & Seat Recognition | Access & Venue | 3 | 2 | yes |
| `BO-969` | AI Aisle, VIP & Accessibility | Access & Venue | 3 | 2 | yes |
| `BO-970` | AI Numbering & Labeling | Access & Venue | 3 | 3 | yes |
| `BO-971` | Validation & Correction | Access & Venue | 3 | 2 | yes |
| `BO-972` | AI Venue Designer & Publish | Access & Venue | 3 | 4 | yes |
| `BO-973` | Layout Command Center | Access & Venue | 3 | 1 | yes |
| `BO-974` | Template Library | Access & Venue | 3 | 2 | yes |
| `BO-975` | Event-Specific Layout | Access & Venue | 3 | 5 | yes |
| `BO-976` | Clone & Inheritance | Access & Venue | 3 | 3 | yes |
| `BO-977` | Version Compare | Access & Venue | 3 | 1 | yes |
| `BO-978` | Multi-Performance Assignment | Access & Venue | 3 | 2 | yes |
| `BO-979` | Temporary Seat Blocking | Access & Venue | 3 | 2 | yes |
| `BO-980` | Scheduled Seat Release | Access & Venue | 3 | 2 | yes |
| `BO-981` | Conflict & Impact Simulation | Access & Venue | 3 | 1 | yes |
| `BO-982` | Approval, Publish & Rollback | Access & Venue | 3 | 4 | yes |
| `BO-983` | Inventory Command Center | Access & Venue | 3 | 1 | yes |
| `BO-984` | Real-Time Seat Map | Access & Venue | 3 | 1 | yes |
| `BO-985` | Status Model Configuration | Access & Venue | 3 | 2 | yes |
| `BO-986` | Availability Tracker | Access & Venue | 3 | 1 | yes |
| `BO-987` | Hold Tracker | Access & Venue | 3 | 2 | yes |
| `BO-988` | Reservation Tracker | Access & Venue | 3 | 1 | yes |
| `BO-989` | Sales & Allocation Tracker | Access & Venue | 3 | 2 | yes |
| `BO-990` | Maintenance & Out of Service | Access & Venue | 3 | 3 | yes |
| `BO-991` | Seat History | Access & Venue | 3 | 1 | yes |
| `BO-992` | Audit & Reconciliation | Access & Venue | 3 | 1 | yes |
| `BO-993` | Experience Command Center | Access & Venue | 3 | 2 | yes |
| `BO-994` | Choose My Seats | Access & Venue | 3 | 2 | yes |
| `BO-995` | Find Seats For Me | Access & Venue | 3 | 2 | yes |
| `BO-996` | Filters & Interactive Legend | Access & Venue | 3 | 1 | yes |
| `BO-997` | Real-Time Availability & Locking | Access & Venue | 3 | 1 | yes |
| `BO-998` | Lock Timeout & Concurrency | Access & Venue | 3 | 0 | yes |
| `BO-999` | Cart & Multi-Seat Management | Access & Venue | 3 | 2 | yes |
| `PTR-026` | Territory, Market & Distribution Rights | Partners | 3 | 2 | yes |
| `PTR-029` | Partner Access, Roles & Permission Profile | Partners | 3 | 4 | yes |
| `PTR-035` | Commission, Margin & Incentive Management | Partners | 3 | 4 | yes |
| `PTR-036` | Credit Limit & Exposure Management | Partners | 3 | 4 | yes |
| `PTR-037` | Deposit, Guarantee & Financial Security Management | Partners | 3 | 2 | yes |
| `PTR-039` | Commercial Allocation, Quota & Commitment Management | Partners | 3 | 2 | yes |
| `PTR-047` | Partner Reconciliation & Exception Management | Partners | 3 | 2 | yes |
| `PTR-048` | Commission Calculation & Settlement Management | Partners | 3 | 5 | yes |

