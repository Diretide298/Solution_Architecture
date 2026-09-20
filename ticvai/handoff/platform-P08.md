# P08 Venue Management — platform

**Derived.** `python3 tools/derive-platform.py P08`. App `venue-management-web` · venue · web

| | |
|---|---|
| Screens | 1182 |
| Operations | 1081 |
| Contracts | 31 |
| Modules | 13 |
| Undrawn | 0 |
| Operations with no screen | 247 |
| Waves | wave1 60 · wave2 79 · wave3 1043 |

## Gaps

### 247 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `enrolFaceTag` | access | POST | Capture a same-visit facial model that dies at close of day |
| `listAccessChanges` | access | GET | Changes made to an entitlement's access |
| `listEntryRulePoints` | access | GET | Which access points an admission rule covers |
| `setEntryRulePoints` | access | PUT | Set the access points an admission rule covers |
| `verifyIdentity` | access | POST | Check the person presenting against the person entitled |
| `replaceAccreditationCredential` | accreditation | POST | Reissue after loss, damage or a name change |
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
| `assessProductChange` | catalogue | POST | What a change would touch, before making it |
| `bulkChangePrices` | catalogue | POST | Reprice a category or a whole catalogue |
| `cloneProduct` | catalogue | POST | Copy a product as a new draft |
| `commitCatalogueImport` | catalogue | POST | Apply a parsed catalogue import |
| `createDonationCampaign` | catalogue | POST | Create a campaign |
| `freezeEntitlement` | catalogue | POST | Pause a membership at the guest's request |
| `getDynamicPriceRule` | catalogue | GET | One rule with its conditions and actions |
| `getPlanBenefits` | catalogue | GET | Which benefits a plan grants, and how much of each |
| `listDonationCampaigns` | catalogue | GET | Campaigns a guest can give to |
| `listDynamicPriceRules` | catalogue | GET | Dynamic pricing rules |
| `listMembershipBenefits` | catalogue | GET | Benefits a plan can grant |
| `listMembershipProgrammes` | catalogue | GET | Membership schemes, the level above a plan |
| `listWaitlistEntries` | catalogue | GET | Who is waiting for capacity |
| `offerWaitlistCapacity` | catalogue | POST | Tell a waiting guest that capacity appeared |
| `reinstateEntitlement` | catalogue | POST | Lift a suspension |
| `restoreProductVersion` | catalogue | POST | Put a previous version back |
| `setDynamicPriceRule` | catalogue | PUT | Replace a rule, its conditions and its actions |
| `setMembershipBenefit` | catalogue | PUT | Define a benefit |
| `setMembershipProgramme` | catalogue | PUT | Define a membership programme |
| `setPlanBenefits` | catalogue | PUT | Replace the benefits a plan grants |
| `suspendEntitlement` | catalogue | POST | Suspend or reinstate an entitlement |
| `updateDonationCampaign` | catalogue | PATCH | Amend or close a campaign |
| `calculateTax` | finance | POST | Compute tax for a set of lines |
| `disputeObligation` | finance | POST | One entity disagrees with the amount |
| … | | | 207 more |

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
| Access & Venue | 382 | 1, 2, 3 |
| Rentals | 199 | 3 |
| Orders & Money | 161 | 1, 2, 3 |
| Engagement & Support | 120 | 3 |
| Sell | 108 | 1, 2, 3 |
| Games & Rides | 100 | 3 |
| Venue Operations | 45 | 1, 2, 3 |
| Setup & Go-Live | 21 | 3 |
| Stock & Supply | 15 | 1, 2 |
| People & Access Rights | 12 | 1, 2, 3 |
| Food & Beverage | 8 | 1, 2 |
| Operations | 7 | 3 |
| Guests & Marketing | 4 | 1, 2 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `BO-001` | Queue Directory | Access & Venue | 1 | 19 | yes |
| `BO-002` | Queue Configuration | Access & Venue | 1 | 14 | yes |
| `BO-003` | Queue Integration Setup | Access & Venue | 1 | 4 | yes |
| `BO-004` | Manual Wait Time Entry | Access & Venue | 1 | 11 | yes |
| `BO-005` | Queue Monitor | Access & Venue | 1 | 19 | yes |
| `BO-006` | Parking Configuration | Access & Venue | 2 | 4 | yes |
| `BO-007` | Product Directory | Sell | 1 | 14 | yes |
| `BO-008` | Product Detail & Variants | Orders & Money | 1 | 4 | yes |
| `BO-009` | Pricing Rules | Sell | 1 | 7 | yes |
| `BO-010` | Promotions & Coupons | Sell | 2 | 19 | yes |
| `BO-011` | Packages & Bundles | Sell | 2 | 5 | yes |
| `BO-012` | Membership Products | Sell | 2 | 12 | yes |
| `BO-013` | Channel & Distribution | Sell | 2 | 10 | yes |
| `BO-014` | Catalogue Publishing | Sell | 1 | 13 | yes |
| `BO-015` | Session Calendar | Sell | 1 | 11 | yes |
| `BO-016` | Session Template | Sell | 1 | 11 | yes |
| `BO-017` | Capacity Management | Sell | 1 | 6 | yes |
| `BO-018` | Allocation & Holds | Sell | 2 | 5 | yes |
| `BO-019` | Closures & Blackouts | Sell | 2 | 12 | yes |
| `BO-020` | F&B Order Management | Food & Beverage | 1 | 11 | yes |
| `BO-021` | Order Search | Food & Beverage | 1 | 2 | yes |
| `BO-022` | Order Detail | Orders & Money | 1 | 14 | yes |
| `BO-023` | Refunds & Exchanges | Orders & Money | 1 | 15 | yes |
| `BO-024` | Payment Exceptions | Orders & Money | 1 | 6 | yes |
| `BO-025` | Chargebacks & Disputes | Orders & Money | 2 | 5 | yes |
| `BO-026` | Group Bookings | Orders & Money | 2 | 14 | yes |
| `BO-027` | Reissue & Media Replacement | Orders & Money | 2 | 4 | yes |
| `BO-028` | Refund Approval Queue | Orders & Money | 1 | 1 | yes |
| `BO-029` | Report Builder | Orders & Money | 2 | 9 | yes |
| `BO-030` | Work Order Verification | Access & Venue | 1 | 9 | yes |
| `BO-031` | Asset Register | Access & Venue | 1 | 7 | yes |
| `BO-032` | Admission Profiles | Access & Venue | 1 | 3 | yes |
| `BO-033` | Blacklist Management | Access & Venue | 1 | 3 | yes |
| `BO-034` | Scan Activity | Access & Venue | 1 | 7 | yes |
| `BO-035` | Override Audit | Access & Venue | 1 | 8 | yes |
| `BO-036` | Device Registry | Venue Operations | 2 | 20 | yes |
| `BO-037` | Offline Package Status | Sell | 1 | 9 | yes |
| `BO-038` | Reconciliation Queue | Access & Venue | 1 | 9 | yes |
| `BO-039` | Shift Directory | Orders & Money | 1 | 13 | yes |
| `BO-040` | Variance Approval | Orders & Money | 1 | 13 | yes |
| `BO-041` | Cash Movements | Orders & Money | 2 | 13 | yes |
| `BO-042` | Banking & Safe | Orders & Money | 2 | 13 | yes |
| `BO-043` | Daily Reconciliation | Orders & Money | 1 | 7 | yes |
| `BO-044` | F&B Outlets | Venue Operations | 2 | 15 | yes |
| `BO-045` | Menu Management | Food & Beverage | 1 | 10 | yes |
| `BO-046` | Kitchen Display | Food & Beverage | 1 | 5 | yes |
| `BO-047` | Order Corrections & Exceptions | Orders & Money | 2 | 14 | yes |
| `BO-048` | Retail Products | Orders & Money | 2 | 4 | yes |
| `BO-049` | Stock Levels | Stock & Supply | 2 | 6 | yes |
| `BO-050` | Stock Position & Valuation | Stock & Supply | 2 | 2 | yes |
| `BO-051` | Purchase Orders | Orders & Money | 2 | 13 | yes |
| `BO-052` | Goods Receipt | Stock & Supply | 2 | 12 | yes |
| `BO-053` | Staff Directory | People & Access Rights | 1 | 4 | yes |
| `BO-054` | Role Assignment | People & Access Rights | 1 | 2 | yes |
| `BO-055` | Rota & Scheduling | People & Access Rights | 2 | 4 | yes |
| `BO-056` | Time & Attendance | People & Access Rights | 2 | 3 | yes |
| `BO-057` | Training & Certification | People & Access Rights | 3 | 1 | yes |
| `BO-058` | Reporting Home | Venue Operations | 1 | 11 | yes |
| `BO-059` | Sales Reports | Orders & Money | 1 | 9 | yes |
| `BO-060` | Attendance & Footfall | Venue Operations | 2 | 16 | yes |
| `BO-061` | Scheduled Reports | Orders & Money | 3 | 9 | yes |
| `BO-062` | Venue Profile | Orders & Money | 1 | 4 | yes |
| `BO-063` | Opening Hours & Calendar | Sell | 1 | 13 | yes |
| `BO-064` | Zones & Areas | Venue Operations | 1 | 10 | yes |
| `BO-065` | Venue Configuration | Orders & Money | 1 | 5 | yes |
| `BO-066` | Notification Settings | People & Access Rights | 2 | 4 | yes |
| `BO-067` | Integrations | Venue Operations | 2 | 5 | yes |
| `BO-068` | Audit Log | Guests & Marketing | 2 | 2 | yes |
| `BO-069` | Asset Register | Access & Venue | 2 | 11 | yes |
| `BO-070` | Work Orders | Orders & Money | 2 | 13 | yes |
| `BO-071` | Planned Maintenance | Access & Venue | 3 | 4 | yes |
| `BO-072` | Incident Log | Access & Venue | 2 | 5 | yes |
| `BO-073` | Lost & Found Register | Guests & Marketing | 2 | 2 | yes |
| `BO-074` | Chart of Accounts | Orders & Money | 1 | 8 | yes |
| `BO-075` | Account Mapping | Orders & Money | 1 | 7 | yes |
| `BO-076` | Revenue Recognition | Orders & Money | 2 | 5 | yes |
| `BO-077` | FX Rates & Variances | Orders & Money | 2 | 5 | yes |
| `BO-078` | Requisitions | Stock & Supply | 1 | 10 | yes |
| `BO-079` | Stock Count | Stock & Supply | 1 | 8 | yes |
| `BO-080` | Stock Transfers | Stock & Supply | 2 | 6 | yes |
| `BO-081` | Inventory Items | Stock & Supply | 2 | 7 | yes |
| `BO-082` | Stock Movements | Stock & Supply | 1 | 4 | yes |
| `BO-083` | Suppliers | Stock & Supply | 2 | 5 | yes |
| `BO-084` | Approval Inbox | People & Access Rights | 1 | 3 | yes |
| `BO-085` | Approval Request | People & Access Rights | 1 | 5 | yes |
| `BO-086` | Approval Matrix | People & Access Rights | 2 | 2 | yes |
| `BO-087` | Approval Delegations | People & Access Rights | 2 | 3 | yes |
| `BO-088` | Approval Analytics | People & Access Rights | 3 | 2 | yes |
| `BO-089` | Journal Entries | Orders & Money | 1 | 6 | yes |
| `BO-090` | Period Close | Orders & Money | 1 | 6 | yes |
| `BO-091` | AI Policy & Spend | Guests & Marketing | 1 | 4 | yes |
| `BO-092` | Venue Maps | Access & Venue | 2 | 2 | yes |
| `BO-093` | Map Import & Labelling | Access & Venue | 2 | 3 | yes |
| `BO-094` | Map Editor & Publish | Access & Venue | 2 | 6 | yes |
| `BO-095` | Resources | Access & Venue | 2 | 2 | yes |
| `BO-096` | Resource Calendar | Access & Venue | 2 | 2 | yes |
| `BO-097` | Check Out & Check In | Access & Venue | 2 | 5 | yes |
| `BO-098` | Qualifications | Access & Venue | 2 | 1 | yes |
| `BO-099` | Session Manifest | Access & Venue | 2 | 2 | yes |
| `BO-100` | Venue Home | Venue Operations | 1 | 2 | yes |
| `BO-1000` | Mobile & Accessible Selection | Access & Venue | 3 | 2 | yes |
| `BO-1001` | View Preview, Compare & Heat Map | Access & Venue | 3 | 1 | yes |
| `BO-1002` | AI Conversational Seat Assistant | Access & Venue | 3 | 1 | yes |
| `BO-1003` | Hold Command Center | Access & Venue | 3 | 1 | yes |
| `BO-1004` | Hold Type Master | Access & Venue | 3 | 2 | yes |
| `BO-1005` | Hold Pool Creation | Access & Venue | 3 | 1 | yes |
| `BO-1006` | Hold Rule Assignment | Access & Venue | 3 | 1 | yes |
| `BO-1007` | Expiration Rules | Access & Venue | 3 | 1 | yes |
| `BO-1008` | Automatic Hold Release | Access & Venue | 3 | 1 | yes |
| `BO-1009` | Release, Convert & Reassign | Access & Venue | 3 | 1 | yes |
| `BO-101` | Orders & Money | Orders & Money | 1 | 3 | yes |
| `BO-1010` | Hold Approval Workflow | Access & Venue | 3 | 2 | yes |
| `BO-1011` | Priority & Conflict Resolution | Access & Venue | 3 | 2 | yes |
| `BO-1012` | Hold Utilization & Audit | Access & Venue | 3 | 1 | yes |
| `BO-1013` | Rules Command Center | Access & Venue | 3 | 1 | yes |
| `BO-1014` | Seat Kill Rules | Access & Venue | 3 | 1 | yes |
| `BO-1015` | Buffer Seat Rules | Access & Venue | 3 | 1 | yes |
| `BO-1016` | Companion Seat Rules | Access & Venue | 3 | 1 | yes |
| `BO-1017` | Wheelchair Companion Rules | Access & Venue | 3 | 2 | yes |
| `BO-1018` | Accessible Seating Master | Access & Venue | 3 | 2 | yes |
| `BO-1019` | Accessible Route Mapping | Access & Venue | 3 | 1 | yes |
| `BO-102` | Sell | Sell | 1 | 3 | yes |
| `BO-1020` | Accessible Filters & Eligibility | Access & Venue | 3 | 1 | yes |
| `BO-1021` | Flexible Spacing Rules | Access & Venue | 3 | 1 | yes |
| `BO-1022` | Compliance Validation & Audit | Access & Venue | 3 | 1 | yes |
| `BO-1023` | Group Reservation Center | Access & Venue | 3 | 1 | yes |
| `BO-1024` | Group Type Configuration | Access & Venue | 3 | 1 | yes |
| `BO-1025` | Group Request Intake | Access & Venue | 3 | 1 | yes |
| `BO-1026` | Availability & Best-Fit Search | Access & Venue | 3 | 1 | yes |
| `BO-1027` | Bulk Seat Allocation | Access & Venue | 3 | 1 | yes |
| `BO-1028` | Roster & Participant Assignment | Access & Venue | 3 | 1 | yes |
| `BO-1029` | Quote, Deposit & Payment | Access & Venue | 3 | 2 | yes |
| `BO-103` | Access & Venue | Access & Venue | 1 | 3 | yes |
| `BO-1030` | Modify, Release & Cancel | Access & Venue | 3 | 2 | yes |
| `BO-1031` | Contracts & Approval Workflow | Access & Venue | 3 | 1 | yes |
| `BO-1032` | Group Reporting & Audit | Access & Venue | 3 | 1 | yes |
| `BO-1033` | Recommendation Command Center | Access & Venue | 3 | 1 | yes |
| `BO-1034` | Best Seat Recommendations | Access & Venue | 3 | 1 | yes |
| `BO-1035` | Best Value Recommendations | Access & Venue | 3 | 1 | yes |
| `BO-1036` | Closest-to-Stage Recommendations | Access & Venue | 3 | 1 | yes |
| `BO-1037` | Family Seating Recommendations | Access & Venue | 3 | 1 | yes |
| `BO-1038` | Accessibility Recommendations | Access & Venue | 3 | 2 | yes |
| `BO-1039` | Seat Upgrade Recommendations | Access & Venue | 3 | 1 | yes |
| `BO-104` | Food & Beverage | Food & Beverage | 1 | 3 | yes |
| `BO-1040` | Alternatives & Reseating | Access & Venue | 3 | 1 | yes |
| `BO-1041` | Scoring Rules & Model Governance | Access & Venue | 3 | 1 | yes |
| `BO-1042` | Performance, Feedback & Audit | Access & Venue | 3 | 1 | yes |
| `BO-1043` | Revenue Command Center | Access & Venue | 3 | 1 | yes |
| `BO-1044` | Dynamic Seat Pricing | Access & Venue | 3 | 1 | yes |
| `BO-1045` | Price Bands & Categories | Access & Venue | 3 | 2 | yes |
| `BO-1046` | Inventory Forecasting | Access & Venue | 3 | 1 | yes |
| `BO-1047` | Section Revenue Forecast | Access & Venue | 3 | 1 | yes |
| `BO-1048` | Seat Upsell Recommendations | Access & Venue | 3 | 1 | yes |
| `BO-1049` | Scenario & What-If Planning | Access & Venue | 3 | 1 | yes |
| `BO-105` | Stock & Supply | Stock & Supply | 1 | 4 | yes |
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
| `BO-106` | People & Access Rights | People & Access Rights | 1 | 2 | yes |
| `BO-1060` | Report Builder, Export & Audit | Access & Venue | 3 | 2 | yes |
| `BO-1061` | Platform Command Center | Access & Venue | 3 | 2 | yes |
| `BO-1062` | Tenant & Brand Context | Access & Venue | 3 | 1 | yes |
| `BO-1063` | Venue-Specific Configuration | Access & Venue | 3 | 2 | yes |
| `BO-1064` | Naming, Numbering & Localization | Access & Venue | 3 | 2 | yes |
| `BO-1065` | Currency, Timezone & Channels | Access & Venue | 3 | 1 | yes |
| `BO-1066` | Roles, Permissions & Masking | Access & Venue | 3 | 3 | yes |
| `BO-1067` | Seat Approval Workflows | Access & Venue | 3 | 1 | yes |
| `BO-1068` | Lifecycle & Environment Promotion | Access & Venue | 3 | 1 | yes |
| `BO-1069` | Platform Health & Observability | Access & Venue | 3 | 1 | yes |
| `BO-107` | Guests & Marketing | Guests & Marketing | 1 | 3 | yes |
| `BO-1070` | Setup, Clone & Inheritance | Access & Venue | 3 | 2 | yes |
| `BO-1071` | Integration Command Center | Access & Venue | 3 | 1 | yes |
| `BO-1072` | Seat Management APIs | Access & Venue | 3 | 1 | yes |
| `BO-1073` | API Access & OAuth | Access & Venue | 3 | 2 | yes |
| `BO-1074` | Webhook Configuration | Access & Venue | 3 | 2 | yes |
| `BO-1075` | Seat Event Catalog | Access & Venue | 3 | 1 | yes |
| `BO-1076` | Concurrency, Idempotency & Limits | Access & Venue | 3 | 1 | yes |
| `BO-1077` | Mapping & Transformation | Access & Venue | 3 | 1 | yes |
| `BO-1078` | Monitoring, Retry & Reconciliation | Access & Venue | 3 | 1 | yes |
| `BO-1079` | Immutable Seat Audit Logs | Access & Venue | 3 | 1 | yes |
| `BO-108` | Venue Operations | Venue Operations | 1 | 4 | yes |
| `BO-1080` | Integration Approval & Compliance | Access & Venue | 3 | 1 | yes |
| `BO-1081` | Finance Dashboard | Orders & Money | 3 | 2 | yes |
| `BO-1082` | Admissions Revenue | Orders & Money | 3 | 2 | yes |
| `BO-1083` | Wallet Command Center | Orders & Money | 3 | 2 | yes |
| `BO-1084` | Wallet Type Library | Orders & Money | 3 | 2 | yes |
| `BO-1085` | Wallet Creation & Provisioning Rules | Orders & Money | 3 | 2 | yes |
| `BO-1086` | Wallet Ownership & Account Association | Orders & Money | 3 | 2 | yes |
| `BO-1087` | Wallet Currency & Monetary Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1088` | Credit & Balance Type Configuration | Orders & Money | 3 | 3 | yes |
| `BO-1089` | Wallet Feature Profile | Orders & Money | 3 | 1 | yes |
| `BO-109` | Menu Builder & POS Layout Designer | Sell | 2 | 3 | yes |
| `BO-1090` | Wallet Lifecycle Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1091` | Wallet Numbering, Identity & Digital Credentials | Orders & Money | 3 | 2 | yes |
| `BO-1092` | Wallet Configuration Preview, Validation & Publication | Orders & Money | 3 | 1 | yes |
| `BO-1093` | Funding Command Center | Orders & Money | 3 | 2 | yes |
| `BO-1094` | Funding Method Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1095` | Top-Up Rule Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1096` | Channel & Funding Source Mapping | Orders & Money | 3 | 1 | yes |
| `BO-1097` | Auto-Reload Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1098` | Recurring Funding Schedule | Orders & Money | 3 | 1 | yes |
| `BO-1099` | Funding Authorization & Approval Rules | Orders & Money | 3 | 1 | yes |
| `BO-110` | Recipe & BOM Management | Sell | 2 | 2 | yes |
| `BO-1100` | Funding Reversal & Correction Management | Orders & Money | 3 | 1 | yes |
| `BO-1101` | Funding Limits & Velocity Controls | Orders & Money | 3 | 1 | yes |
| `BO-1102` | Funding Transaction Audit & Reconciliation | Orders & Money | 3 | 2 | yes |
| `BO-1103` | Stored Value & Credit Command Center | Orders & Money | 3 | 2 | yes |
| `BO-1104` | Credit Type Definition Studio | Orders & Money | 3 | 2 | yes |
| `BO-1105` | Credit Issuance Rule Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1106` | Credit Usage & Eligibility Rules | Orders & Money | 3 | 1 | yes |
| `BO-1107` | Consumption Priority Engine | Orders & Money | 3 | 2 | yes |
| `BO-1108` | Expiry & Validity Policy Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1109` | FEFO & Credit Lot Management | Orders & Money | 3 | 1 | yes |
| `BO-111` | Ingredient Substitution, Allergen & Nutrition | Sell | 2 | 4 | yes |
| `BO-1110` | Split Tender & Multi-Credit Consumption | Orders & Money | 3 | 2 | yes |
| `BO-1111` | Credit Expiry, Extension & Forfeiture Operations | Orders & Money | 3 | 1 | yes |
| `BO-1112` | Consumption Simulator, Validation & Rule Publication | Orders & Money | 3 | 2 | yes |
| `BO-1113` | Shared Wallet Command Center | Orders & Money | 3 | 1 | yes |
| `BO-1114` | Shared Wallet Model Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1115` | Family & Household Structure Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1116` | Parent–Child Stored Value Distribution | Orders & Money | 3 | 2 | yes |
| `BO-1117` | Allowance & Budget Allocation Engine | Orders & Money | 3 | 1 | yes |
| `BO-1118` | Member Spending Controls & Permissions | Orders & Money | 3 | 1 | yes |
| `BO-1119` | Corporate Wallet & Organizational Hierarchy | Orders & Money | 3 | 2 | yes |
| `BO-112` | Production Planning & Production Sheets | Sell | 2 | 1 | yes |
| `BO-1120` | Corporate Budget, Policy & Approval Rules | Orders & Money | 3 | 1 | yes |
| `BO-1121` | Shared Wallet Transfers & Balance Reallocation | Orders & Money | 3 | 1 | yes |
| `BO-1122` | Shared Wallet Simulator, Monitoring & Audit | Orders & Money | 3 | 2 | yes |
| `BO-1123` | Gift Card & Digital Benefit Command Center | Orders & Money | 3 | 1 | yes |
| `BO-1124` | Gift Card Product Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1125` | Gift Card Issuance, Activation & Distribution | Orders & Money | 3 | 3 | yes |
| `BO-1126` | Voucher & Coupon Type Configuration | Orders & Money | 3 | 2 | yes |
| `BO-1127` | Voucher Eligibility & Redemption Rule Studio | Orders & Money | 3 | 1 | yes |
| `BO-1128` | Membership Benefits & Entitlement Mapping | Orders & Money | 3 | 1 | yes |
| `BO-1129` | Benefit Packaging & Digital Wallet Presentation | Orders & Money | 3 | 1 | yes |
| `BO-113` | Central Kitchen & Commissary Management | Sell | 2 | 2 | yes |
| `BO-1130` | Gift Card & Voucher Expiry Management | Orders & Money | 3 | 1 | yes |
| `BO-1131` | Gift Card Balance, Liability & Breakage Control | Orders & Money | 3 | 1 | yes |
| `BO-1132` | Gift Card & Voucher Simulator, Validation & Publication | Orders & Money | 3 | 1 | yes |
| `BO-1133` | Wallet Usage & Channel Command Center | Orders & Money | 3 | 1 | yes |
| `BO-1134` | Wallet Channel Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1135` | Wallet Payment & Redemption Policy | Orders & Money | 3 | 1 | yes |
| `BO-1136` | Wearable & Credential Type Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1137` | Wearable Linking & Wallet Association Rules | Orders & Money | 3 | 1 | yes |
| `BO-1138` | NFC, RFID & QR Interaction Rules | Orders & Money | 3 | 1 | yes |
| `BO-1139` | Digital Key & Wallet Authentication Policy | Orders & Money | 3 | 1 | yes |
| `BO-114` | Variants, Attributes, Barcode & RFID Management | Sell | 2 | 2 | yes |
| `BO-1140` | Offline Wallet & Degraded Mode Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1141` | Device, Terminal & Acceptance Point Mapping | Orders & Money | 3 | 2 | yes |
| `BO-1142` | Wallet Transaction Simulator, Monitoring & Channel Audit | Orders & Money | 3 | 2 | yes |
| `BO-1143` | Wallet Operations Command Center | Orders & Money | 3 | 2 | yes |
| `BO-1144` | Peer-to-Peer Transfer Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1145` | Transfer Eligibility, Limits & Approval Rules | Orders & Money | 3 | 1 | yes |
| `BO-1146` | Refund-to-Wallet Policy Configuration | Orders & Money | 3 | 2 | yes |
| `BO-1147` | Refund Routing & Credit Restoration Engine | Orders & Money | 3 | 2 | yes |
| `BO-1148` | Reversal & Transaction Correction Management | Orders & Money | 3 | 1 | yes |
| `BO-1149` | Administrative Balance Adjustment Studio | Orders & Money | 3 | 1 | yes |
| `BO-115` | Category, Brand & Merchandise Hierarchy | Sell | 2 | 5 | yes |
| `BO-1150` | Wallet Block, Freeze & Restriction Management | Orders & Money | 3 | 1 | yes |
| `BO-1151` | Wallet Disputes & Operational Exception Queue | Orders & Money | 3 | 2 | yes |
| `BO-1152` | Operations Simulator, Approval & Audit Trail | Orders & Money | 3 | 1 | yes |
| `BO-1153` | Wallet Security & Risk Command Center | Orders & Money | 3 | 1 | yes |
| `BO-1154` | Wallet Risk Policy Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1155` | Transaction Risk Scoring Engine | Orders & Money | 3 | 1 | yes |
| `BO-1156` | Velocity & Behavioral Rule Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1157` | Device, Credential & Account Security | Orders & Money | 3 | 2 | yes |
| `BO-1158` | AI Fraud & Anomaly Detection Studio | Orders & Money | 3 | 1 | yes |
| `BO-1159` | Automated Security Action Orchestration | Orders & Money | 3 | 2 | yes |
| `BO-116` | Merchandising & Product Presentation | Sell | 2 | 7 | yes |
| `BO-1160` | Fraud Alert & Investigation Case Management | Orders & Money | 3 | 1 | yes |
| `BO-1161` | Security Rules Testing, Simulation & AI Sandbox | Orders & Money | 3 | 1 | yes |
| `BO-1162` | Security Governance, Audit & Rule Publication | Orders & Money | 3 | 1 | yes |
| `BO-1163` | Wallet Finance & Liability Command Center | Orders & Money | 3 | 1 | yes |
| `BO-1164` | Wallet Financial Classification & Accounting Mapping | Orders & Money | 3 | 1 | yes |
| `BO-1165` | Wallet Sub-Ledger & Balance Control | Orders & Money | 3 | 1 | yes |
| `BO-1166` | Multi-Source Reconciliation Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1167` | Reconciliation Exception & Resolution Workbench | Orders & Money | 3 | 2 | yes |
| `BO-1168` | Gift Card Liability Management | Orders & Money | 3 | 1 | yes |
| `BO-1169` | Breakage & Revenue Recognition Policy | Orders & Money | 3 | 1 | yes |
| `BO-117` | Product Import, Governance & AI Configuration Assistant | Sell | 2 | 5 | yes |
| `BO-1170` | Wallet Financial Period & Closing Controls | Orders & Money | 3 | 2 | yes |
| `BO-1171` | Wallet Analytics & Management Reporting | Orders & Money | 3 | 1 | yes |
| `BO-1172` | Finance Validation, Reporting & Audit Center | Orders & Money | 3 | 1 | yes |
| `BO-1173` | Wallet Integration Command Center | Orders & Money | 3 | 1 | yes |
| `BO-1174` | Wallet API Catalogue & Endpoint Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1175` | Integration Profile & System Mapping | Orders & Money | 3 | 1 | yes |
| `BO-1176` | Wallet Events, Webhooks & Notification Orchestration | Orders & Money | 3 | 1 | yes |
| `BO-1177` | API Security, Access & Integration Permissions | Orders & Money | 3 | 1 | yes |
| `BO-1178` | Synchronization, Retry & Resilience Configuration | Orders & Money | 3 | 1 | yes |
| `BO-1179` | Integration Monitoring & Exception Workbench | Orders & Money | 3 | 1 | yes |
| `BO-118` | Campaign & Audience Management | Sell | 2 | 6 | yes |
| `BO-1180` | Wallet Configuration Governance & Version Control | Orders & Money | 3 | 1 | yes |
| `BO-1181` | Approval, Publication & Change Management | Orders & Money | 3 | 2 | yes |
| `BO-1182` | Wallet Platform Health, Audit & Administration Center | Orders & Money | 3 | 1 | yes |
| `BO-119` | Cross-Sell, Upsell & Recommendation Rules | Sell | 2 | 2 | yes |
| `BO-120` | Omnichannel Commerce & Journey Configuration | Sell | 2 | 2 | yes |
| `BO-121` | Personalized Offers & Guest Engagement | Sell | 2 | 2 | yes |
| `BO-122` | POS Experience Dashboard | Sell | 2 | 1 | yes |
| `BO-123` | POS Profile Management | Sell | 2 | 2 | yes |
| `BO-124` | Layout & Journey Builder | Sell | 2 | 6 | yes |
| `BO-125` | Product & Category Button Configuration | Sell | 2 | 6 | yes |
| `BO-126` | Deployment, Preview & Audit | Sell | 2 | 7 | yes |
| `BO-127` | Hardware & Peripherals Management | Venue Operations | 2 | 3 | yes |
| `BO-128` | Live Workstation Health Monitor | Venue Operations | 2 | 3 | yes |
| `BO-129` | Software, Configuration & Version Management | Venue Operations | 2 | 6 | yes |
| `BO-130` | Offline Policy & Rules Configuration | Venue Operations | 1 | 4 | yes |
| `BO-131` | Connectivity & Auto-Switch Settings | Venue Operations | 2 | 1 | yes |
| `BO-132` | Offline Transaction Monitor & Sync Queue | Venue Operations | 2 | 2 | yes |
| `BO-133` | Offline Alerts, Limits & Audit | Venue Operations | 1 | 6 | yes |
| `BO-134` | Kitchen & Preparation Stations | Food & Beverage | 2 | 2 | yes |
| `BO-135` | Order Routing & KDS/Printer Rules | Food & Beverage | 2 | 2 | yes |
| `BO-136` | F&B Global Settings & Controls | Food & Beverage | 2 | 5 | yes |
| `BO-137` | Recipe Consumption & Theoretical Inventory | Stock & Supply | 2 | 4 | yes |
| `BO-138` | Production Execution & Batch Management | Stock & Supply | 2 | 3 | yes |
| `BO-139` | Wastage, Spoilage, Returns & Write-Off | Stock & Supply | 2 | 1 | yes |
| `BO-140` | Product Availability, 86 & Operational Food Safety | Stock & Supply | 2 | 2 | yes |
| `BO-141` | Operational Alerts, AI Replenishment & Action Center | Stock & Supply | 2 | 3 | yes |
| `BO-142` | Store Rules, Controls & Permissions | Sell | 2 | 4 | yes |
| `BO-143` | Retail Global Settings & Controls | Sell | 2 | 2 | yes |
| `BO-144` | Access Control Command Center | Access & Venue | 3 | 1 | yes |
| `BO-145` | Venue & Park Access Structure | Access & Venue | 3 | 1 | yes |
| `BO-146` | Access Area & Zone Builder | Access & Venue | 3 | 1 | yes |
| `BO-147` | Attraction Access Configuration | Access & Venue | 3 | 1 | yes |
| `BO-148` | Access Point Directory | Access & Venue | 3 | 1 | yes |
| `BO-149` | Gate & Lane Configuration | Access & Venue | 3 | 1 | yes |
| `BO-150` | Access Control Graphical Map Designer | Access & Venue | 3 | 1 | yes |
| `BO-151` | Access Location Grouping | Access & Venue | 3 | 1 | yes |
| `BO-152` | Operating Calendar & Special Access Days | Access & Venue | 3 | 1 | yes |
| `BO-153` | Topology Validation & Publication | Access & Venue | 3 | 1 | yes |
| `BO-154` | Access Rule Command Center | Access & Venue | 3 | 1 | yes |
| `BO-155` | Visual Access Rule Builder | Access & Venue | 3 | 1 | yes |
| `BO-156` | Entry, Exit & Re-entry Rules | Access & Venue | 3 | 1 | yes |
| `BO-157` | Anti-Passback & Journey Sequence | Access & Venue | 3 | 1 | yes |
| `BO-158` | Access Validity & Time Rules | Access & Venue | 3 | 1 | yes |
| `BO-159` | Entitlement Consumption Engine | Access & Venue | 3 | 1 | yes |
| `BO-160` | Multi-Park & Crossover Rules | Access & Venue | 3 | 2 | yes |
| `BO-161` | Guest, Companion & Eligibility Rules | Access & Venue | 3 | 1 | yes |
| `BO-162` | Group Admission & Quantity Validation | Access & Venue | 3 | 1 | yes |
| `BO-163` | Rule Simulation, Conflict Check & Publication | Access & Venue | 3 | 1 | yes |
| `BO-164` | Digital Credential Security Command Center | Access & Venue | 3 | 2 | yes |
| `BO-165` | Dynamic QR Security Profile Builder | Access & Venue | 3 | 1 | yes |
| `BO-166` | Credential Activation & Display Rules | Access & Venue | 3 | 1 | yes |
| `BO-167` | Device Binding & Session Security | Access & Venue | 3 | 1 | yes |
| `BO-168` | BLE Beacon & Geofence Configuration | Access & Venue | 3 | 1 | yes |
| `BO-169` | Credential Transfer & Rebinding | Access & Venue | 3 | 1 | yes |
| `BO-170` | Credential Revocation & Lifecycle Events | Access & Venue | 3 | 1 | yes |
| `BO-171` | Offline Cryptographic Validation Profile | Access & Venue | 3 | 1 | yes |
| `BO-172` | Embedded Entitlement Payload Designer | Access & Venue | 3 | 1 | yes |
| `BO-173` | Credential Security Simulation, Audit & Publication | Access & Venue | 3 | 3 | yes |
| `BO-174` | Media & Credential Command Center | Access & Venue | 3 | 3 | yes |
| `BO-175` | Media Type & Technology Library | Access & Venue | 3 | 1 | yes |
| `BO-176` | Virtual Credential & Media Association | Access & Venue | 3 | 1 | yes |
| `BO-177` | Verification Method Selection & Locking | Access & Venue | 3 | 1 | yes |
| `BO-178` | Media Issuance & Encoding Profile | Access & Venue | 3 | 1 | yes |
| `BO-179` | Media Swap & Replacement | Access & Venue | 3 | 1 | yes |
| `BO-180` | RFID & NFC Configuration | Access & Venue | 3 | 2 | yes |
| `BO-181` | External & Partner Credential Mapping | Access & Venue | 3 | 1 | yes |
| `BO-182` | Hotel, Wallet & External Media Integration | Access & Venue | 3 | 1 | yes |
| `BO-183` | Media Compatibility, Testing & Publication | Access & Venue | 3 | 1 | yes |
| `BO-184` | Biometric Access Command Center | Access & Venue | 3 | 1 | yes |
| `BO-185` | Biometric Verification Profile Builder | Access & Venue | 3 | 1 | yes |
| `BO-186` | Face Pass Enrollment Configuration | Access & Venue | 3 | 1 | yes |
| `BO-187` | Biometric Consent & Guardian Management | Access & Venue | 3 | 1 | yes |
| `BO-188` | Face Tag Temporary Enrollment | Access & Venue | 3 | 1 | yes |
| `BO-189` | Face Matching & Verification Thresholds | Access & Venue | 3 | 1 | yes |
| `BO-190` | Face Change, Re-enrollment & Identity Protection | Access & Venue | 3 | 1 | yes |
| `BO-191` | Biometric Validation at Gate | Access & Venue | 3 | 1 | yes |
| `BO-192` | Biometric Lifecycle, Retention & Deletion | Access & Venue | 3 | 1 | yes |
| `BO-193` | Biometric Simulation, Audit & Publication | Access & Venue | 3 | 1 | yes |
| `BO-194` | Device & Gate Command Center | Access & Venue | 3 | 1 | yes |
| `BO-195` | Device Type & Hardware Library | Access & Venue | 3 | 1 | yes |
| `BO-196` | Physical Device Registration & Provisioning | Access & Venue | 3 | 1 | yes |
| `BO-197` | Turnstile & Lane Behavior Configuration | Access & Venue | 3 | 1 | yes |
| `BO-198` | Validation Outcome & Guest Feedback Designer | Access & Venue | 3 | 1 | yes |
| `BO-199` | Reader, Scanner & Peripheral Configuration | Access & Venue | 3 | 1 | yes |
| `BO-200` | Handheld & Mobile Access Device Configuration | Access & Venue | 3 | 1 | yes |
| `BO-201` | Gate Modes, Free Spin & Emergency Controls | Access & Venue | 3 | 1 | yes |
| `BO-202` | Device Software, Content & Remote Configuration | Access & Venue | 3 | 1 | yes |
| `BO-203` | Hardware Compatibility, Health, Testing & Deployment | Access & Venue | 3 | 1 | yes |
| `BO-204` | Offline & Edge Operations Command Center | Access & Venue | 3 | 1 | yes |
| `BO-205` | Edge Node & Local Processing Configuration | Access & Venue | 3 | 1 | yes |
| `BO-206` | Offline Validation Policy Builder | Access & Venue | 3 | 1 | yes |
| `BO-207` | Edge Package & Data Distribution | Access & Venue | 3 | 1 | yes |
| `BO-208` | Offline Credential & Revocation Cache | Access & Venue | 3 | 1 | yes |
| `BO-209` | Offline Entitlement & Usage Ledger | Access & Venue | 3 | 1 | yes |
| `BO-210` | Connectivity Failure & Degraded Mode Policy | Access & Venue | 3 | 1 | yes |
| `BO-211` | Reconnection, Synchronization & Conflict Resolution | Access & Venue | 3 | 1 | yes |
| `BO-212` | Offline Simulation & Resilience Testing | Access & Venue | 3 | 1 | yes |
| `BO-213` | Edge Security, Audit & Deployment | Access & Venue | 3 | 1 | yes |
| `BO-214` | Guest Journey Command Center | Access & Venue | 3 | 1 | yes |
| `BO-215` | Group & B2B Admission Profile Builder | Access & Venue | 3 | 1 | yes |
| `BO-216` | Group Leader & Fast B2B Validation | Access & Venue | 3 | 1 | yes |
| `BO-217` | Group Attendance & Partial Entry Manager | Access & Venue | 3 | 1 | yes |
| `BO-218` | Family, Child, POD & Companion Journey | Access & Venue | 3 | 1 | yes |
| `BO-219` | Re-entry & Temporary Exit Journey | Access & Venue | 3 | 1 | yes |
| `BO-220` | Multi-Park & Crossover Journey Orchestrator | Access & Venue | 3 | 2 | yes |
| `BO-221` | Fast Pass & Attraction Access Journey | Access & Venue | 3 | 1 | yes |
| `BO-222` | Special Event, Free View & Alternative Admission | Access & Venue | 3 | 1 | yes |
| `BO-223` | Journey Simulation, Audit & Publication | Access & Venue | 3 | 1 | yes |
| `BO-224` | Live Access Operations Command Center | Access & Venue | 3 | 1 | yes |
| `BO-225` | Podium Operations Console | Access & Venue | 3 | 1 | yes |
| `BO-226` | Ticket & Credential Investigation Console | Access & Venue | 3 | 1 | yes |
| `BO-227` | Validation Exception & Reason Code Manager | Access & Venue | 3 | 1 | yes |
| `BO-228` | Manual Override & Supervisor Approval | Access & Venue | 3 | 1 | yes |
| `BO-229` | Credential Disable, Blacklist & Whitelist Operations | Access & Venue | 3 | 1 | yes |
| `BO-230` | Live Gate Mode & Lane Control | Access & Venue | 3 | 1 | yes |
| `BO-231` | Queue, Throughput & Lane Optimization | Access & Venue | 3 | 1 | yes |
| `BO-232` | Operational Incident & Exception Workspace | Access & Venue | 3 | 1 | yes |
| `BO-233` | Operations Audit, Shift Handover & Control Summary | Access & Venue | 3 | 1 | yes |
| `BO-234` | Dynamic Access Policy Command Center | Access & Venue | 3 | 1 | yes |
| `BO-235` | Access Attribute Catalog | Access & Venue | 3 | 1 | yes |
| `BO-236` | Visual Dynamic Policy Builder | Access & Venue | 3 | 1 | yes |
| `BO-237` | Context, Time, Event & Capacity Policy Builder | Access & Venue | 3 | 1 | yes |
| `BO-238` | Identity, Membership & Accreditation Policies | Access & Venue | 3 | 1 | yes |
| `BO-239` | Policy Scope, Hierarchy & Inheritance | Access & Venue | 3 | 1 | yes |
| `BO-240` | Authorization Governance & Temporary Access | Access & Venue | 3 | 1 | yes |
| `BO-241` | Policy Evaluation Architecture & Offline Distribution | Access & Venue | 3 | 1 | yes |
| `BO-242` | Policy Simulation, Conflict & Impact Analysis | Access & Venue | 3 | 1 | yes |
| `BO-243` | Policy Approval, Audit, Analytics & AI Optimization | Access & Venue | 3 | 1 | yes |
| `BO-244` | Access Security & Fraud Command Center | Access & Venue | 3 | 1 | yes |
| `BO-245` | Fraud Detection Rule & Signal Library | Access & Venue | 3 | 1 | yes |
| `BO-246` | Credential Sharing & Concurrent Usage Detection | Access & Venue | 3 | 1 | yes |
| `BO-247` | Unified Identity & Credential Lock Manager | Access & Venue | 3 | 1 | yes |
| `BO-248` | Biometric & Identity Integrity Monitoring | Access & Venue | 3 | 1 | yes |
| `BO-249` | Relationship & Companion Fraud Monitoring | Access & Venue | 3 | 1 | yes |
| `BO-250` | Access Risk Scoring & Decision Engine | Access & Venue | 3 | 1 | yes |
| `BO-251` | Real-Time Security Response & Playbook Builder | Access & Venue | 3 | 1 | yes |
| `BO-252` | Security Investigation & Evidence Workspace | Access & Venue | 3 | 1 | yes |
| `BO-253` | Security Analytics, AI Detection & Governance | Access & Venue | 3 | 1 | yes |
| `BO-254` | Access Monitoring & Analytics Command Center | Access & Venue | 3 | 1 | yes |
| `BO-255` | Live Venue Occupancy & People Counting | Access & Venue | 3 | 1 | yes |
| `BO-256` | Graphical Access Map & Live Gate Performance | Access & Venue | 3 | 1 | yes |
| `BO-257` | Attendance & Admission Analytics | Access & Venue | 3 | 1 | yes |
| `BO-258` | Entry, Exit, Re-entry & Crossover Analytics | Access & Venue | 3 | 1 | yes |
| `BO-259` | Throughput, Queue & Validation Performance Analytics | Access & Venue | 3 | 1 | yes |
| `BO-260` | Validation Outcome & Rejection Analytics | Access & Venue | 3 | 1 | yes |
| `BO-261` | Guest Dwell Time, Length of Stay & Attraction Flow | Access & Venue | 3 | 1 | yes |
| `BO-262` | Access Reports, Scheduled Reporting & Data Export | Access & Venue | 3 | 1 | yes |
| `BO-263` | AI Access Intelligence, Forecasting & Executive Insights | Access & Venue | 3 | 1 | yes |
| `BO-264` | Group Sales Command Center | Sell | 3 | 2 | yes |
| `BO-265` | Group Enquiry & Opportunity Capture | Sell | 3 | 1 | yes |
| `BO-266` | Group Customer & Organization Profile | Sell | 3 | 1 | yes |
| `BO-267` | Group Requirements, Availability & Capacity Planner | Sell | 3 | 1 | yes |
| `BO-268` | Group Package & Experience Builder | Sell | 3 | 1 | yes |
| `BO-269` | Group Quotation Builder & Proposal Generation | Sell | 3 | 1 | yes |
| `BO-270` | Quote Revision, Negotiation & Version Management | Sell | 3 | 1 | yes |
| `BO-271` | Group Discount, Exception & Approval Workflow | Sell | 3 | 1 | yes |
| `BO-272` | Quote-to-Booking Conversion & Confirmation | Sell | 3 | 1 | yes |
| `BO-273` | Group Booking 360° & Handover Workspace | Sell | 3 | 1 | yes |
| `BO-274` | Group Booking Operations Command Center | Sell | 3 | 2 | yes |
| `BO-275` | Group Operational Planning & Task Workspace | Sell | 3 | 1 | yes |
| `BO-276` | Participants, Guest Lists & Group Structure | Sell | 3 | 1 | yes |
| `BO-277` | Group Payment, Deposit & Balance Management | Sell | 3 | 1 | yes |
| `BO-278` | Group Ticket, Seat & Entitlement Allocation | Sell | 3 | 1 | yes |
| `BO-279` | Group Ticket Fulfillment & Distribution | Sell | 3 | 1 | yes |
| `BO-280` | Group Arrival, Check-In & Admission Operations | Sell | 3 | 1 | yes |
| `BO-281` | Group Amendments, Cancellation & Refund Operations | Sell | 3 | 1 | yes |
| `BO-282` | Group Booking Reconciliation, Closure & Performance | Sell | 3 | 1 | yes |
| `BO-283` | Group Sales Analytics & AI Intelligence Center | Sell | 3 | 2 | yes |
| `BO-284` | Membership & Annual Pass Command Center | Sell | 3 | 1 | yes |
| `BO-285` | Membership Product & Tier Builder | Sell | 3 | 1 | yes |
| `BO-286` | Membership Eligibility & Qualification Rule Builder | Sell | 3 | 1 | yes |
| `BO-287` | Validity, Activation & Expiry Configuration | Sell | 3 | 1 | yes |
| `BO-288` | Membership Entitlement & Admission Benefit Builder | Sell | 3 | 1 | yes |
| `BO-289` | Membership Usage, Visit & Consumption Rules | Sell | 3 | 1 | yes |
| `BO-290` | Family, Household & Dependent Membership Configuration | Sell | 3 | 1 | yes |
| `BO-291` | Membership Commercial, Pricing & Channel Association | Sell | 3 | 1 | yes |
| `BO-292` | Renewal, Auto-Renewal & Membership Continuity Configuration | Sell | 3 | 1 | yes |
| `BO-293` | Membership Product Validation, Approval, Publication & Versioning | Sell | 3 | 1 | yes |
| `BO-294` | Member Operations Command Center | Sell | 3 | 1 | yes |
| `BO-295` | Member 360° Membership Account Workspace | Sell | 3 | 1 | yes |
| `BO-296` | Membership Activation, Assignment & Credential Management | Sell | 3 | 1 | yes |
| `BO-297` | Visit, Admission & Entitlement Usage Monitor | Sell | 3 | 1 | yes |
| `BO-298` | Membership Freeze, Suspension & Reactivation Management | Sell | 3 | 1 | yes |
| `BO-299` | Membership Upgrade, Downgrade & Product Migration Operations | Sell | 3 | 1 | yes |
| `BO-300` | Renewal Operations & Auto-Renewal Management | Sell | 3 | 1 | yes |
| `BO-301` | Member Exceptions, Overrides & Service Recovery | Sell | 3 | 1 | yes |
| `BO-302` | Member Lifecycle History, Audit & Case Timeline | Sell | 3 | 1 | yes |
| `BO-303` | Membership Analytics, Renewal Intelligence & AI Retention Center | Sell | 3 | 1 | yes |
| `BO-304` | Order & Reservation Command Center | Orders & Money | 3 | 1 | yes |
| `BO-305` | Order Detail & Transaction Workspace | Orders & Money | 3 | 1 | yes |
| `BO-306` | Reservation & Hold Policy Configuration | Orders & Money | 3 | 1 | yes |
| `BO-307` | Order & Reservation Status Lifecycle Configuration | Orders & Money | 3 | 1 | yes |
| `BO-308` | Order Creation & Source/Channel Configuration | Orders & Money | 3 | 1 | yes |
| `BO-309` | Customer, Guest & Account Assignment | Orders & Money | 3 | 1 | yes |
| `BO-310` | Order Line, Product & Entitlement Composition | Orders & Money | 3 | 1 | yes |
| `BO-311` | Capacity Reservation & Inventory Commitment | Orders & Money | 3 | 1 | yes |
| `BO-312` | Reservation Confirmation, Expiry & Fulfillment Readiness | Orders & Money | 3 | 1 | yes |
| `BO-313` | Order Lifecycle Timeline, SLA, Exceptions & AI Operations | Orders & Money | 3 | 1 | yes |
| `BO-314` | Amendment & After-Sales Command Center | Orders & Money | 3 | 2 | yes |
| `BO-315` | Order Amendment Workspace | Orders & Money | 3 | 1 | yes |
| `BO-316` | Amendment Eligibility & Policy Rule Builder | Orders & Money | 3 | 1 | yes |
| `BO-317` | Cancellation & Partial Cancellation Policy Configuration | Orders & Money | 3 | 1 | yes |
| `BO-318` | Refund Policy & Refund Calculation Configuration | Orders & Money | 3 | 1 | yes |
| `BO-319` | Void, Reversal & Same-Day Correction Management | Orders & Money | 3 | 1 | yes |
| `BO-320` | Ticket Reissue & Fulfillment Regeneration | Orders & Money | 3 | 1 | yes |
| `BO-321` | After-Sales Financial Settlement & Adjustment Workspace | Orders & Money | 3 | 1 | yes |
| `BO-322` | Approval, Exception & Service Recovery Management | Orders & Money | 3 | 1 | yes |
| `BO-323` | Amendment History, Audit & After-Sales Analytics | Orders & Money | 3 | 2 | yes |
| `BO-324` | Payment & Order Financial Command Center | Orders & Money | 3 | 1 | yes |
| `BO-325` | Order Payment Detail & Transaction Ledger | Orders & Money | 3 | 1 | yes |
| `BO-326` | Multi-Payment, Split Tender & Payment Allocation Configuration | Orders & Money | 3 | 1 | yes |
| `BO-327` | Deposit, Partial Payment & Outstanding Balance Management | Orders & Money | 3 | 1 | yes |
| `BO-328` | Order Split, Merge & Transaction Relationship Management | Orders & Money | 3 | 1 | yes |
| `BO-329` | Related Order & Transaction Relationship Explorer | Orders & Money | 3 | 1 | yes |
| `BO-330` | External Payment, Partner & Settlement Reference Mapping | Orders & Money | 3 | 1 | yes |
| `BO-331` | Payment Reconciliation & Exception Management | Orders & Money | 3 | 1 | yes |
| `BO-332` | Financial Traceability, Control & Audit Explorer | Orders & Money | 3 | 1 | yes |
| `BO-333` | Order Financial Analytics & AI Reconciliation Intelligence | Orders & Money | 3 | 1 | yes |
| `BO-334` | Virtual Ticket Command Center | Access & Venue | 3 | 3 | yes |
| `BO-335` | Virtual Ticket Identity & Master Record Configuration | Access & Venue | 3 | 1 | yes |
| `BO-336` | Virtual Ticket Status & Lifecycle Model | Access & Venue | 3 | 1 | yes |
| `BO-337` | Media Type & Credential Technology Registry | Access & Venue | 3 | 2 | yes |
| `BO-338` | Multi-Media Binding & Association Rules | Access & Venue | 3 | 1 | yes |
| `BO-339` | Credential Identity, Token & Reference Mapping | Access & Venue | 3 | 1 | yes |
| `BO-340` | Entitlement & Cross-Media Synchronization Rules | Access & Venue | 3 | 1 | yes |
| `BO-341` | Media Activation, Priority & Fallback Rules | Access & Venue | 3 | 1 | yes |
| `BO-342` | Media Replacement, Revocation & Rebinding Rules | Access & Venue | 3 | 1 | yes |
| `BO-343` | Virtual Ticket Architecture Testing, Governance & Audit | Access & Venue | 3 | 1 | yes |
| `BO-344` | Media Design Studio Command Center | Access & Venue | 3 | 1 | yes |
| `BO-345` | Digital QR & Barcode Ticket Designer | Access & Venue | 3 | 1 | yes |
| `BO-346` | PDF, Printable & POS Ticket Designer | Access & Venue | 3 | 1 | yes |
| `BO-347` | Apple Wallet Pass Designer | Access & Venue | 3 | 1 | yes |
| `BO-348` | Google Wallet Pass Designer | Access & Venue | 3 | 1 | yes |
| `BO-349` | RFID, NFC, Card & Wristband Media Designer | Access & Venue | 3 | 1 | yes |
| `BO-350` | Digital Card, Membership & Wearable Designer | Access & Venue | 3 | 1 | yes |
| `BO-351` | Dynamic Fields, Data Mapping & Content Builder | Access & Venue | 3 | 1 | yes |
| `BO-352` | Branding, Localization & Template Inheritance | Access & Venue | 3 | 1 | yes |
| `BO-353` | Multi-Media Preview, Testing, Approval & Publication | Access & Venue | 3 | 1 | yes |
| `BO-354` | Credential Operations Command Center | Access & Venue | 3 | 1 | yes |
| `BO-355` | Virtual Ticket & Credential 360° Workspace | Access & Venue | 3 | 1 | yes |
| `BO-356` | Credential Generation & Issuance Monitor | Access & Venue | 3 | 1 | yes |
| `BO-357` | Credential Delivery & Distribution Operations | Access & Venue | 3 | 1 | yes |
| `BO-358` | Media Binding, Activation & Assignment Operations | Access & Venue | 3 | 1 | yes |
| `BO-359` | Credential Replacement, Reissue, Revocation & Recovery | Access & Venue | 3 | 1 | yes |
| `BO-360` | Failed Generation, Delivery & Credential Exception Management | Access & Venue | 3 | 1 | yes |
| `BO-361` | Credential Usage & Cross-Media Traceability | Access & Venue | 3 | 1 | yes |
| `BO-362` | Credential Security, Audit & Operational Evidence | Access & Venue | 3 | 1 | yes |
| `BO-363` | Ticket Media Analytics & AI Operations Intelligence | Access & Venue | 3 | 1 | yes |
| `BO-364` | Approval Command Center Dashboard | Venue Operations | 3 | 2 | yes |
| `BO-365` | My Approval Inbox | Venue Operations | 3 | 1 | yes |
| `BO-366` | Team / Shared Approval Queue | Venue Operations | 3 | 1 | yes |
| `BO-367` | Approval Request Detail | Venue Operations | 3 | 2 | yes |
| `BO-368` | AI Decision Support | Venue Operations | 3 | 1 | yes |
| `BO-369` | High Priority & Risk Queue | Venue Operations | 3 | 1 | yes |
| `BO-370` | Escalated Approval Center | Venue Operations | 3 | 2 | yes |
| `BO-371` | Completed Approval History | Venue Operations | 3 | 1 | yes |
| `BO-372` | Approval SLA & Workload Monitor | Venue Operations | 3 | 2 | yes |
| `BO-373` | Approval Activity & Notification Center | Venue Operations | 3 | 1 | yes |
| `BO-374` | Approval Decision Workspace | Venue Operations | 3 | 1 | yes |
| `BO-375` | Business Context & Evidence Viewer | Venue Operations | 3 | 1 | yes |
| `BO-376` | Approval Timeline & Decision Chain | Venue Operations | 3 | 1 | yes |
| `BO-377` | Approve & Sensitive Action Confirmation | Venue Operations | 3 | 3 | yes |
| `BO-378` | Reject / Return / Request Information | Venue Operations | 3 | 1 | yes |
| `BO-379` | Requester Modification & Resubmission | Venue Operations | 3 | 1 | yes |
| `BO-380` | Withdrawal, Cancellation, Expiration & Reopening | Venue Operations | 3 | 1 | yes |
| `BO-381` | Segregation of Duties & Four-Eyes Control | Venue Operations | 3 | 1 | yes |
| `BO-382` | Approved Action Execution & Status | Venue Operations | 3 | 1 | yes |
| `BO-383` | Decision Record & Immutable Audit View | Venue Operations | 3 | 1 | yes |
| `BO-384` | Delegation & Escalation Command Center | Venue Operations | 3 | 2 | yes |
| `BO-385` | Delegation Management | Venue Operations | 3 | 1 | yes |
| `BO-386` | Temporary Delegation & Availability Calendar | Venue Operations | 3 | 2 | yes |
| `BO-387` | Out-of-Office & Substitute Routing | Venue Operations | 3 | 1 | yes |
| `BO-388` | Approval SLA Policy Configuration | Venue Operations | 3 | 1 | yes |
| `BO-389` | Reminder & Breach Notification Rules | Venue Operations | 3 | 1 | yes |
| `BO-390` | Escalation Policy Builder | Venue Operations | 3 | 1 | yes |
| `BO-391` | Live Escalation Operations Center | Venue Operations | 3 | 1 | yes |
| `BO-392` | SLA & Escalation Performance Analytics | Venue Operations | 3 | 1 | yes |
| `BO-393` | AI SLA & Escalation Advisor | Venue Operations | 3 | 1 | yes |
| `BO-394` | Game & Ride Operations Dashboard | Games & Rides | 3 | 2 | yes |
| `BO-395` | Game & Ride Directory | Games & Rides | 3 | 1 | yes |
| `BO-396` | Attraction Profile | Games & Rides | 3 | 3 | yes |
| `BO-397` | Attraction Type Configuration | Games & Rides | 3 | 2 | yes |
| `BO-398` | Game & Ride Operational Configuration | Games & Rides | 3 | 1 | yes |
| `BO-399` | Wallet & Credit Acceptance Mapping | Games & Rides | 3 | 1 | yes |
| `BO-400` | Attraction / Reader Mapping | Games & Rides | 3 | 2 | yes |
| `BO-401` | Game Package & Entitlement Association | Games & Rides | 3 | 2 | yes |
| `BO-402` | Configuration Health & Validation | Games & Rides | 3 | 1 | yes |
| `BO-403` | Attraction Audit, Dependencies & Governed Actions | Games & Rides | 3 | 1 | yes |
| `BO-404` | Reader Management Dashboard | Games & Rides | 3 | 1 | yes |
| `BO-405` | Reader Directory | Games & Rides | 3 | 1 | yes |
| `BO-406` | Reader Profile & Device Setup | Games & Rides | 3 | 1 | yes |
| `BO-407` | Reader Credit & Payment Configuration | Games & Rides | 3 | 2 | yes |
| `BO-408` | Reader / Attraction Assignment | Games & Rides | 3 | 1 | yes |
| `BO-409` | Retap Delay & Transaction Protection | Games & Rides | 3 | 1 | yes |
| `BO-410` | Free Game Glow & Reader Display Rules | Games & Rides | 3 | 1 | yes |
| `BO-411` | Reader Theme & Experience Configuration | Games & Rides | 3 | 1 | yes |
| `BO-412` | Real-Time Tap Validation & Reader Response | Games & Rides | 3 | 1 | yes |
| `BO-413` | Balance Check Reader & Device Test Console | Games & Rides | 3 | 1 | yes |
| `BO-414` | Wallet & Credit Management Dashboard | Games & Rides | 3 | 2 | yes |
| `BO-415` | Wallet & Credit Type Configuration | Games & Rides | 3 | 2 | yes |
| `BO-416` | Wallet Account & Balance View | Games & Rides | 3 | 2 | yes |
| `BO-417` | Top-Up Configuration | Games & Rides | 3 | 1 | yes |
| `BO-418` | Top-Up Bonus Rule Configuration | Games & Rides | 3 | 1 | yes |
| `BO-419` | Bonus Usage Restrictions | Games & Rides | 3 | 1 | yes |
| `BO-420` | Bonus Validity & Expiry Configuration | Games & Rides | 3 | 1 | yes |
| `BO-421` | Free Game & Ride Credit Management | Games & Rides | 3 | 2 | yes |
| `BO-422` | Refund, Adjustment & Manual Bonus Control | Games & Rides | 3 | 1 | yes |
| `BO-423` | Wallet Credit Transaction Ledger & Audit | Games & Rides | 3 | 1 | yes |
| `BO-424` | Gameplay Validation Command Center | Games & Rides | 3 | 2 | yes |
| `BO-425` | Gameplay Validation Rule Configuration | Games & Rides | 3 | 1 | yes |
| `BO-426` | Deduction Priority & Funding Source Rules | Games & Rides | 3 | 1 | yes |
| `BO-427` | All Games & Rides Pass Configuration | Games & Rides | 3 | 1 | yes |
| `BO-428` | Specific Game/Ride Unlimited Entitlement | Games & Rides | 3 | 1 | yes |
| `BO-429` | Specific Game/Ride Limited Entitlement | Games & Rides | 3 | 1 | yes |
| `BO-430` | Game Package Builder | Games & Rides | 3 | 2 | yes |
| `BO-431` | Entitlement Validity & Activation Rules | Games & Rides | 3 | 1 | yes |
| `BO-432` | Real-Time Gameplay Authorization | Games & Rides | 3 | 1 | yes |
| `BO-433` | Validation Simulator & Exception Analysis | Games & Rides | 3 | 1 | yes |
| `BO-434` | Game & Ride Pricing Command Center | Games & Rides | 3 | 1 | yes |
| `BO-435` | Standard Game & Ride Price Configuration | Games & Rides | 3 | 1 | yes |
| `BO-436` | Group Pricing Configuration | Games & Rides | 3 | 1 | yes |
| `BO-437` | Peak / Non-Peak Dynamic Pricing | Games & Rides | 3 | 1 | yes |
| `BO-438` | Pricing Calendar & Exception Dates | Games & Rides | 3 | 1 | yes |
| `BO-439` | Normal & VIP Pricing Configuration | Games & Rides | 3 | 1 | yes |
| `BO-440` | Retry Price Configuration | Games & Rides | 3 | 1 | yes |
| `BO-441` | Price Priority & Conflict Rules | Games & Rides | 3 | 1 | yes |
| `BO-442` | Effective Pricing & Reader Price Preview | Games & Rides | 3 | 1 | yes |
| `BO-443` | Pricing Audit, Approval & Publication | Games & Rides | 3 | 1 | yes |
| `BO-444` | Redemption Operations Dashboard | Games & Rides | 3 | 1 | yes |
| `BO-445` | Redemption Credit Rule Configuration | Games & Rides | 3 | 1 | yes |
| `BO-446` | Ticket-Based Redemption / Ticket-Eater Integration | Games & Rides | 3 | 1 | yes |
| `BO-447` | Ticketless Redemption Game Integration | Games & Rides | 3 | 1 | yes |
| `BO-448` | Redemption Wallet & Balance View | Games & Rides | 3 | 1 | yes |
| `BO-449` | Redemption Counter / Prize Checkout | Games & Rides | 3 | 1 | yes |
| `BO-450` | Prize Catalogue & Credit Cost Configuration | Games & Rides | 3 | 2 | yes |
| `BO-451` | Prize Inventory Integration | Games & Rides | 3 | 2 | yes |
| `BO-452` | Direct-Pay / Crane & Prize Machine Configuration | Games & Rides | 3 | 1 | yes |
| `BO-453` | Redemption Transaction Ledger, Reconciliation & Audit | Games & Rides | 3 | 1 | yes |
| `BO-454` | Card Lifecycle Command Center | Games & Rides | 3 | 1 | yes |
| `BO-455` | Card / Credential Profile | Games & Rides | 3 | 1 | yes |
| `BO-456` | Card Expiry Rule Configuration | Games & Rides | 3 | 1 | yes |
| `BO-457` | Last Recharge & Last Activity Tracking | Games & Rides | 3 | 1 | yes |
| `BO-458` | Expiry Monitoring & Upcoming Expiration | Games & Rides | 3 | 1 | yes |
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
| `BO-471` | Offline, Synchronization & Recovery Monitor | Games & Rides | 3 | 1 | yes |
| `BO-472` | Operational Alerts & Exception Center | Games & Rides | 3 | 1 | yes |
| `BO-473` | Operational Analytics & Reconciliation Dashboard | Games & Rides | 3 | 1 | yes |
| `BO-474` | Reader Integration Command Center | Games & Rides | 3 | 1 | yes |
| `BO-475` | Reader Manufacturer & Model Profile | Games & Rides | 3 | 1 | yes |
| `BO-476` | Communication Protocol Configuration | Games & Rides | 3 | 1 | yes |
| `BO-477` | Reader Command & Event Mapping | Games & Rides | 3 | 1 | yes |
| `BO-478` | Reader Configuration Deployment & Synchronization | Games & Rides | 3 | 1 | yes |
| `BO-479` | Game Trigger & I/O Control Mapping | Games & Rides | 3 | 1 | yes |
| `BO-480` | Reader Screen, LED & Sound Output Mapping | Games & Rides | 3 | 1 | yes |
| `BO-481` | Edge Cache & Offline Rule Package | Games & Rides | 3 | 1 | yes |
| `BO-482` | Device Diagnostics & Integration Logs | Games & Rides | 3 | 1 | yes |
| `BO-483` | Integration Certification & Test Console | Games & Rides | 3 | 1 | yes |
| `BO-484` | Self-Service Experience Command Center | Games & Rides | 3 | 1 | yes |
| `BO-485` | Self-Service Kiosk Profile & Channel Configuration | Games & Rides | 3 | 1 | yes |
| `BO-486` | Customer Card / Wallet Identification | Games & Rides | 3 | 1 | yes |
| `BO-487` | Customer Wallet & Balance Summary | Games & Rides | 3 | 1 | yes |
| `BO-488` | Self-Service Wallet Top-Up | Games & Rides | 3 | 1 | yes |
| `BO-489` | Bonus, Free Game & Benefit View | Games & Rides | 3 | 1 | yes |
| `BO-490` | Game & Ride Eligibility / “What Can I Play?” | Games & Rides | 3 | 1 | yes |
| `BO-491` | Redemption Balance & Prize Discovery | Games & Rides | 3 | 1 | yes |
| `BO-492` | Customer Game & Wallet Transaction History | Games & Rides | 3 | 1 | yes |
| `BO-493` | Self-Service UI Theme, Language & Journey Configuration | Games & Rides | 3 | 1 | yes |
| `BO-494` | Rental Product Command Center | Rentals | 3 | 2 | yes |
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
| `BO-505` | Serialized Equipment Registry | Rentals | 3 | 2 | yes |
| `BO-506` | Equipment / Asset Profile | Rentals | 3 | 2 | yes |
| `BO-507` | Pooled Inventory Management | Rentals | 3 | 2 | yes |
| `BO-508` | Equipment Status & Condition Management | Rentals | 3 | 2 | yes |
| `BO-509` | QR / Barcode Equipment Identification | Rentals | 3 | 1 | yes |
| `BO-510` | Inventory Location Allocation | Rentals | 3 | 2 | yes |
| `BO-511` | Inventory Transfer Management | Rentals | 3 | 3 | yes |
| `BO-512` | Inventory Adjustment & Exception Management | Rentals | 3 | 2 | yes |
| `BO-513` | Inventory Intelligence & Rebalancing | Rentals | 3 | 2 | yes |
| `BO-514` | Availability Command Center | Rentals | 3 | 1 | yes |
| `BO-515` | Availability Rule Configuration | Rentals | 3 | 1 | yes |
| `BO-516` | Operating Hours & Rental Windows | Rentals | 3 | 1 | yes |
| `BO-517` | Timeslot & Duration Availability Setup | Rentals | 3 | 1 | yes |
| `BO-518` | Real-Time Availability Calendar | Rentals | 3 | 2 | yes |
| `BO-519` | Resource / Equipment Calendar | Rentals | 3 | 1 | yes |
| `BO-520` | Blackout, Closure & Capacity Blocking | Rentals | 3 | 1 | yes |
| `BO-521` | Overlap & Conflict Engine | Rentals | 3 | 1 | yes |
| `BO-522` | Inventory Holds, Buffers & Release Rules | Rentals | 3 | 1 | yes |
| `BO-523` | Availability Intelligence & AI Forecasting | Rentals | 3 | 1 | yes |
| `BO-524` | Rental Pricing Command Center | Rentals | 3 | 1 | yes |
| `BO-525` | Pricing Profile Builder | Rentals | 3 | 2 | yes |
| `BO-526` | Duration & Tiered Pricing Configuration | Rentals | 3 | 1 | yes |
| `BO-527` | Calendar, Peak & Seasonal Pricing | Rentals | 3 | 1 | yes |
| `BO-528` | Dynamic Pricing & AI Recommendation | Rentals | 3 | 1 | yes |
| `BO-529` | Deposit & Security Hold Policy | Rentals | 3 | 1 | yes |
| `BO-530` | Deposit Lifecycle & Settlement Rules | Rentals | 3 | 1 | yes |
| `BO-531` | Late Fee, Grace Period & Extension Pricing | Rentals | 3 | 1 | yes |
| `BO-532` | Commercial Exceptions, Waivers & Overrides | Rentals | 3 | 1 | yes |
| `BO-533` | Pricing Simulation, Validation & AI Commercial Intelligence | Rentals | 3 | 3 | yes |
| `BO-534` | Rental Booking Command Center | Rentals | 3 | 1 | yes |
| `BO-535` | New Rental Booking Wizard | Rentals | 3 | 2 | yes |
| `BO-536` | Availability Selection & Alternative Options | Rentals | 3 | 1 | yes |
| `BO-537` | Customer & Participant Information | Rentals | 3 | 1 | yes |
| `BO-538` | Group Rental & Participant Management | Rentals | 3 | 1 | yes |
| `BO-539` | Rental Agreement & Waiver Completion | Rentals | 3 | 1 | yes |
| `BO-540` | Booking Commercial Summary & Payment | Rentals | 3 | 1 | yes |
| `BO-541` | Reservation Confirmation & QR Voucher | Rentals | 3 | 1 | yes |
| `BO-542` | Reservation Modification, Cancellation & No-Show | Rentals | 3 | 1 | yes |
| `BO-543` | Reservation Detail, Timeline & Readiness | Rentals | 3 | 1 | yes |
| `BO-544` | Rental Checkout Command Center | Rentals | 3 | 1 | yes |
| `BO-545` | Voucher Scan & Reservation Retrieval | Rentals | 3 | 1 | yes |
| `BO-546` | Checkout Readiness Validation | Rentals | 3 | 1 | yes |
| `BO-547` | Equipment Assignment Workspace | Rentals | 3 | 1 | yes |
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
| `BO-561` | Overdue Rental Management | Rentals | 3 | 2 | yes |
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
| `BO-572` | Deposit Release, Capture & Customer Confirmation | Rentals | 3 | 1 | yes |
| `BO-573` | Return Completion & Equipment Disposition | Rentals | 3 | 2 | yes |
| `BO-574` | Maintenance Command Center | Rentals | 3 | 2 | yes |
| `BO-575` | Maintenance Rule & Service Plan Configuration | Rentals | 3 | 3 | yes |
| `BO-576` | Maintenance Calendar & Scheduling | Rentals | 3 | 2 | yes |
| `BO-577` | Maintenance Work Order | Rentals | 3 | 5 | yes |
| `BO-578` | Technician Repair Workspace | Rentals | 3 | 3 | yes |
| `BO-579` | Parts, Cost & Maintenance Expense Tracking | Rentals | 3 | 1 | yes |
| `BO-580` | Asset Maintenance History & Lifecycle | Rentals | 3 | 1 | yes |
| `BO-581` | Return-to-Service Inspection & Approval | Rentals | 3 | 2 | yes |
| `BO-582` | Asset Retirement, Write-Off & Replacement Recommendation | Rentals | 3 | 2 | yes |
| `BO-583` | Maintenance Intelligence & Predictive AI | Rentals | 3 | 1 | yes |
| `BO-584` | Rental Executive Command Center | Rentals | 3 | 1 | yes |
| `BO-585` | Rental Revenue & Commercial Analytics | Rentals | 3 | 1 | yes |
| `BO-586` | Utilization & Capacity Analytics | Rentals | 3 | 1 | yes |
| `BO-587` | Inventory & Equipment Performance Analytics | Rentals | 3 | 1 | yes |
| `BO-588` | Rental Duration, Extension & Return Analytics | Rentals | 3 | 1 | yes |
| `BO-589` | Damage, Loss, Deposit & Exception Analytics | Rentals | 3 | 1 | yes |
| `BO-590` | Location & Channel Performance | Rentals | 3 | 1 | yes |
| `BO-591` | Rental Forecasting & Demand Intelligence | Rentals | 3 | 1 | yes |
| `BO-592` | Audit, Governance & Operational Control | Rentals | 3 | 1 | yes |
| `BO-593` | AI Rental Management Copilot & Action Center | Rentals | 3 | 1 | yes |
| `BO-594` | Environment Ready & Handoff to AI Setup | Setup & Go-Live | 3 | 1 | yes |
| `BO-595` | AI Setup Command Center | Setup & Go-Live | 3 | 1 | yes |
| `BO-596` | Guided Setup Plan | Setup & Go-Live | 3 | 1 | yes |
| `BO-597` | AI Configuration Workspace | Setup & Go-Live | 3 | 1 | yes |
| `BO-598` | AI Draft Review & Approval | Setup & Go-Live | 3 | 1 | yes |
| `BO-599` | Manual Configuration Center | Setup & Go-Live | 3 | 1 | yes |
| `BO-600` | Venue, Calendar & Operational Setup | Setup & Go-Live | 3 | 1 | yes |
| `BO-601` | Product, Pricing & Sales Channel Setup | Setup & Go-Live | 3 | 2 | yes |
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
| `BO-615` | Accreditation Command Center | Access & Venue | 3 | 2 | yes |
| `BO-616` | Accreditation Application Directory | Access & Venue | 3 | 1 | yes |
| `BO-617` | New Accreditation Application | Access & Venue | 3 | 1 | yes |
| `BO-618` | Accreditation Form Builder | Access & Venue | 3 | 1 | yes |
| `BO-619` | Accreditation Category Management | Access & Venue | 3 | 1 | yes |
| `BO-620` | Accreditation Program Setup | Access & Venue | 3 | 1 | yes |
| `BO-621` | Applicant Type Configuration | Access & Venue | 3 | 1 | yes |
| `BO-622` | Application Requirements Matrix | Access & Venue | 3 | 1 | yes |
| `BO-623` | Accreditation Intake Monitor | Access & Venue | 3 | 1 | yes |
| `BO-624` | Registration Rules & Publication | Access & Venue | 3 | 1 | yes |
| `BO-625` | Accreditation Holder Directory | Access & Venue | 3 | 1 | yes |
| `BO-626` | Accreditation Holder Profile | Access & Venue | 3 | 1 | yes |
| `BO-627` | Identity Details & Verification | Access & Venue | 3 | 1 | yes |
| `BO-628` | Photo Management | Access & Venue | 3 | 1 | yes |
| `BO-629` | Document Repository | Access & Venue | 3 | 1 | yes |
| `BO-630` | Document Verification Queue | Access & Venue | 3 | 1 | yes |
| `BO-631` | Duplicate & Identity Conflict Detection | Access & Venue | 3 | 1 | yes |
| `BO-632` | Organization & Affiliation Management | Access & Venue | 3 | 1 | yes |
| `BO-633` | Profile Completeness & Compliance Monitor | Access & Venue | 3 | 1 | yes |
| `BO-634` | Profile History & Audit Timeline | Access & Venue | 3 | 1 | yes |
| `BO-635` | Accreditation Review Queue | Access & Venue | 3 | 1 | yes |
| `BO-636` | Application Review Workspace | Access & Venue | 3 | 2 | yes |
| `BO-637` | Approval Workflow Builder | Access & Venue | 3 | 1 | yes |
| `BO-638` | Approval Rules & Conditions | Access & Venue | 3 | 1 | yes |
| `BO-639` | Reviewer Assignment & Delegation | Access & Venue | 3 | 1 | yes |
| `BO-640` | Rejection & Resubmission Management | Access & Venue | 3 | 1 | yes |
| `BO-641` | Escalation & Exception Management | Access & Venue | 3 | 1 | yes |
| `BO-642` | Approval Decision History | Access & Venue | 3 | 1 | yes |
| `BO-643` | Approval Policy Validation & Publication | Access & Venue | 3 | 1 | yes |
| `BO-644` | Credential Issuance Command Center | Access & Venue | 3 | 1 | yes |
| `BO-645` | Credential Generation Workspace | Access & Venue | 3 | 1 | yes |
| `BO-646` | Credential Media Configuration | Access & Venue | 3 | 1 | yes |
| `BO-647` | Badge Template Designer | Access & Venue | 3 | 1 | yes |
| `BO-648` | Badge Printing & Print Queue | Access & Venue | 3 | 2 | yes |
| `BO-649` | Digital & Mobile Credential Management | Access & Venue | 3 | 2 | yes |
| `BO-650` | NFC & RFID Credential Encoding | Access & Venue | 3 | 1 | yes |
| `BO-651` | Credential Activation & Delivery | Access & Venue | 3 | 1 | yes |
| `BO-652` | Credential Replacement & Reissue | Access & Venue | 3 | 1 | yes |
| `BO-653` | Credential Registry & Credential History | Access & Venue | 3 | 1 | yes |
| `BO-654` | Accreditation Access Command Center | Access & Venue | 3 | 1 | yes |
| `BO-655` | Access Profile Management | Access & Venue | 3 | 2 | yes |
| `BO-656` | Venue & Zone Access Matrix | Access & Venue | 3 | 1 | yes |
| `BO-657` | Operational Area Permission Management | Access & Venue | 3 | 1 | yes |
| `BO-658` | Date & Time Access Rules | Access & Venue | 3 | 1 | yes |
| `BO-659` | Access Schedule Management | Access & Venue | 3 | 1 | yes |
| `BO-660` | Holder Access Assignment | Access & Venue | 3 | 1 | yes |
| `BO-661` | Temporary Access & Exception Management | Access & Venue | 3 | 1 | yes |
| `BO-662` | Access Revocation & Suspension | Access & Venue | 3 | 1 | yes |
| `BO-663` | Access Rights Preview, Impact & Synchronization | Access & Venue | 3 | 1 | yes |
| `BO-664` | Accreditation Lifecycle Command Center | Access & Venue | 3 | 1 | yes |
| `BO-665` | Accreditation Status Workflow | Access & Venue | 3 | 1 | yes |
| `BO-666` | Validity Period Configuration | Access & Venue | 3 | 1 | yes |
| `BO-667` | Event & Venue Accreditation Assignment | Access & Venue | 3 | 1 | yes |
| `BO-668` | Multi-Venue Accreditation Management | Access & Venue | 3 | 1 | yes |
| `BO-669` | Temporary & Seasonal Accreditation | Access & Venue | 3 | 1 | yes |
| `BO-670` | Suspension & Reactivation Management | Access & Venue | 3 | 1 | yes |
| `BO-671` | Accreditation Revocation Management | Access & Venue | 3 | 1 | yes |
| `BO-672` | Expiry Monitor & Expiration Rules | Access & Venue | 3 | 1 | yes |
| `BO-673` | Accreditation Renewal Workspace | Access & Venue | 3 | 1 | yes |
| `BO-674` | Accreditation Communications Command Center | Access & Venue | 3 | 1 | yes |
| `BO-675` | Notification Rule Management | Access & Venue | 3 | 1 | yes |
| `BO-676` | Expiry & Renewal Notification Scheduler | Access & Venue | 3 | 1 | yes |
| `BO-677` | Communication Template Library | Access & Venue | 3 | 1 | yes |
| `BO-678` | Channel, Language & Branding Configuration | Access & Venue | 3 | 1 | yes |
| `BO-679` | Manual & Bulk Communication Center | Access & Venue | 3 | 1 | yes |
| `BO-680` | Accreditation Bulk Import | Access & Venue | 3 | 1 | yes |
| `BO-681` | Import Validation & Processing Monitor | Access & Venue | 3 | 1 | yes |
| `BO-682` | Accreditation Export & Data Extract Center | Access & Venue | 3 | 1 | yes |
| `BO-683` | Delivery, Batch & Operational History | Access & Venue | 3 | 1 | yes |
| `BO-684` | Accreditation Executive Dashboard | Access & Venue | 3 | 1 | yes |
| `BO-685` | Accreditation Status & Portfolio Reporting | Access & Venue | 3 | 1 | yes |
| `BO-686` | Accreditation Utilization Analytics | Access & Venue | 3 | 1 | yes |
| `BO-687` | Accreditation Access Activity Reporting | Access & Venue | 3 | 1 | yes |
| `BO-688` | Accreditation Trend & Comparative Analysis | Access & Venue | 3 | 1 | yes |
| `BO-689` | Accreditation Audit Reporting | Access & Venue | 3 | 1 | yes |
| `BO-690` | Immutable Accreditation Audit Log | Access & Venue | 3 | 1 | yes |
| `BO-691` | Accreditation API Management | Access & Venue | 3 | 1 | yes |
| `BO-692` | Accreditation Webhook Management | Access & Venue | 3 | 1 | yes |
| `BO-693` | Integration & Data Exchange Monitor | Access & Venue | 3 | 1 | yes |
| `BO-694` | Event Catalogue Command Center | Sell | 3 | 1 | yes |
| `BO-695` | Event Type & Behaviour Configuration | Sell | 3 | 2 | yes |
| `BO-696` | Event Duplication & Clone Configuration | Sell | 3 | 1 | yes |
| `BO-697` | Event Schedule Command Center | Sell | 3 | 1 | yes |
| `BO-698` | Dynamic Performance Duration Configuration | Sell | 3 | 1 | yes |
| `BO-699` | Schedule Change & Rescheduling Configuration | Sell | 3 | 1 | yes |
| `BO-700` | Venue & Space Command Center | Sell | 3 | 1 | yes |
| `BO-701` | Venue Master Configuration | Sell | 3 | 1 | yes |
| `BO-702` | Space Access Rules Configuration | Sell | 3 | 1 | yes |
| `BO-703` | Seating & Capacity Command Center | Sell | 3 | 1 | yes |
| `BO-704` | Event Capacity Profile Configuration | Sell | 3 | 1 | yes |
| `BO-705` | Seating Mode & Reservation Configuration | Sell | 3 | 1 | yes |
| `BO-706` | Registration & Attendance Command Center | Sell | 3 | 1 | yes |
| `BO-707` | Attendee Data & Registration Form Configuration | Sell | 3 | 1 | yes |
| `BO-708` | Accreditation & Participant Category Configuration | Sell | 3 | 2 | yes |
| `BO-709` | Event Admission & Entry Policy Configuration | Sell | 3 | 1 | yes |
| `BO-710` | Event Resource Command Center | Sell | 3 | 1 | yes |
| `BO-711` | Event Resource Requirement Configuration | Sell | 3 | 1 | yes |
| `BO-712` | Staff & Role Assignment Configuration | Sell | 3 | 2 | yes |
| `BO-713` | Contractor & External Workforce Configuration | Sell | 3 | 1 | yes |
| `BO-714` | Event Shift & Roster Configuration | Sell | 3 | 2 | yes |
| `BO-715` | Resource Location & Deployment Configuration | Sell | 3 | 1 | yes |
| `BO-716` | Event Lifecycle & Change Command Center | Sell | 3 | 1 | yes |
| `BO-717` | Lifecycle Transition Configuration | Sell | 3 | 1 | yes |
| `BO-718` | Event Change Request Configuration | Sell | 3 | 1 | yes |
| `BO-719` | Event Cancellation Workflow Configuration | Sell | 3 | 1 | yes |
| `BO-720` | Ticket, Reservation & Customer Treatment Configuration | Sell | 3 | 1 | yes |
| `BO-721` | Activity Session & Slot Template Configuration | Sell | 3 | 2 | yes |
| `BO-722` | Prepaid Minute Package & Customer Balance Configuration | Sell | 3 | 2 | yes |
| `BO-723` | Peak, Off-Peak & Super Prime Time Configuration | Sell | 3 | 1 | yes |
| `BO-724` | Walk-In / There-and-Then Booking Configuration | Sell | 3 | 1 | yes |
| `BO-725` | Session Operations Command Center | Sell | 3 | 1 | yes |
| `BO-726` | Participant Photo & Video Assignment | Sell | 3 | 1 | yes |
| `BO-727` | F&B Command Center | Operations | 3 | 1 | yes |
| `BO-728` | Outlet Management | Operations | 3 | 1 | yes |
| `BO-729` | Create / Edit Outlet | Operations | 3 | 1 | yes |
| `BO-730` | Outlet Types & Templates | Operations | 3 | 1 | yes |
| `BO-731` | Operating Hours & Service Periods | Operations | 3 | 1 | yes |
| `BO-732` | POS & Device Assignment | Operations | 3 | 1 | yes |
| `BO-733` | Service Channel Configuration | Operations | 3 | 1 | yes |
| `BO-734` | CRM Command Center | Engagement & Support | 3 | 2 | yes |
| `BO-735` | Guest Directory | Engagement & Support | 3 | 2 | yes |
| `BO-736` | Guest Master Configuration | Engagement & Support | 3 | 2 | yes |
| `BO-737` | Customer 360 Profile | Engagement & Support | 3 | 2 | yes |
| `BO-738` | Activity Timeline | Engagement & Support | 3 | 3 | yes |
| `BO-739` | Contact & Preferences | Engagement & Support | 3 | 1 | yes |
| `BO-740` | Family & Guardians | Engagement & Support | 3 | 2 | yes |
| `BO-741` | Corporate & Groups | Engagement & Support | 3 | 2 | yes |
| `BO-742` | Commerce & Documents | Engagement & Support | 3 | 1 | yes |
| `BO-743` | AI Guest Intelligence | Engagement & Support | 3 | 2 | yes |
| `BO-744` | Data Governance Center | Engagement & Support | 3 | 2 | yes |
| `BO-745` | Identity Resolution Rules | Engagement & Support | 3 | 2 | yes |
| `BO-746` | Duplicate Review & Merge | Engagement & Support | 3 | 3 | yes |
| `BO-747` | Consent Policy Configuration | Engagement & Support | 3 | 2 | yes |
| `BO-748` | Consent Capture & Versions | Engagement & Support | 3 | 2 | yes |
| `BO-749` | Guest Preference Center | Engagement & Support | 3 | 2 | yes |
| `BO-750` | Data Subject Requests | Engagement & Support | 3 | 2 | yes |
| `BO-751` | Retention & Anonymization | Engagement & Support | 3 | 2 | yes |
| `BO-752` | Privacy & AI Governance | Engagement & Support | 3 | 2 | yes |
| `BO-753` | Compliance Audit Dashboard | Engagement & Support | 3 | 1 | yes |
| `BO-754` | Audience Intelligence | Engagement & Support | 3 | 2 | yes |
| `BO-755` | Dynamic Segment Builder | Engagement & Support | 3 | 2 | yes |
| `BO-756` | Static Lists & Imports | Engagement & Support | 3 | 2 | yes |
| `BO-757` | Behavioral Segmentation | Engagement & Support | 3 | 1 | yes |
| `BO-758` | Membership & Loyalty Segments | Engagement & Support | 3 | 1 | yes |
| `BO-759` | Demographic & Geographic | Engagement & Support | 3 | 1 | yes |
| `BO-760` | Revenue & Engagement Segments | Engagement & Support | 3 | 1 | yes |
| `BO-761` | AI Audience Discovery | Engagement & Support | 3 | 1 | yes |
| `BO-762` | Predictive Audiences | Engagement & Support | 3 | 2 | yes |
| `BO-763` | Activation & Governance | Engagement & Support | 3 | 2 | yes |
| `BO-764` | Campaign Command Center | Engagement & Support | 3 | 1 | yes |
| `BO-765` | Campaign Library & Calendar | Engagement & Support | 3 | 1 | yes |
| `BO-766` | Campaign Builder | Engagement & Support | 3 | 1 | yes |
| `BO-767` | Audience & Offer Selection | Engagement & Support | 3 | 2 | yes |
| `BO-768` | Multichannel Composer | Engagement & Support | 3 | 2 | yes |
| `BO-769` | Schedule & Trigger Rules | Engagement & Support | 3 | 2 | yes |
| `BO-770` | Campaign Approval Workflow | Engagement & Support | 3 | 1 | yes |
| `BO-771` | Budget, Goals & Forecast | Engagement & Support | 3 | 2 | yes |
| `BO-772` | A/B & AI Optimization | Engagement & Support | 3 | 1 | yes |
| `BO-773` | Attribution & Audit | Engagement & Support | 3 | 1 | yes |
| `BO-774` | Journey Automation Center | Engagement & Support | 3 | 1 | yes |
| `BO-775` | Visual Journey Builder | Engagement & Support | 3 | 2 | yes |
| `BO-776` | Trigger Event Catalog | Engagement & Support | 3 | 2 | yes |
| `BO-777` | Decision Logic & Timing | Engagement & Support | 3 | 1 | yes |
| `BO-778` | Abandoned Cart Recovery | Engagement & Support | 3 | 1 | yes |
| `BO-779` | Lifecycle Journeys | Engagement & Support | 3 | 1 | yes |
| `BO-780` | Guest Engagement Journeys | Engagement & Support | 3 | 1 | yes |
| `BO-781` | Cross-Sell & Service Recovery | Engagement & Support | 3 | 1 | yes |
| `BO-782` | AI Journey Optimization | Engagement & Support | 3 | 1 | yes |
| `BO-783` | Journey Analytics & Audit | Engagement & Support | 3 | 1 | yes |
| `BO-784` | Communications Center | Engagement & Support | 3 | 1 | yes |
| `BO-785` | Template Library | Engagement & Support | 3 | 2 | yes |
| `BO-786` | Newsletter Builder | Engagement & Support | 3 | 1 | yes |
| `BO-787` | Content Blocks & Product Feed | Engagement & Support | 3 | 1 | yes |
| `BO-788` | Subscriptions & Preferences | Engagement & Support | 3 | 2 | yes |
| `BO-789` | Transactional Notification Rules | Engagement & Support | 3 | 2 | yes |
| `BO-790` | Scheduling, Priority & Approval | Engagement & Support | 3 | 1 | yes |
| `BO-791` | Delivery, Retry & Failover | Engagement & Support | 3 | 2 | yes |
| `BO-792` | Deliverability & Analytics | Engagement & Support | 3 | 1 | yes |
| `BO-793` | AI Content, Translation & Audit | Engagement & Support | 3 | 1 | yes |
| `BO-794` | Omnichannel Command Center | Engagement & Support | 3 | 1 | yes |
| `BO-795` | Unified Inbox | Engagement & Support | 3 | 2 | yes |
| `BO-796` | Guest Conversation 360 | Engagement & Support | 3 | 2 | yes |
| `BO-797` | AI Chatbot Configuration | Engagement & Support | 3 | 1 | yes |
| `BO-798` | Intent & Knowledge Management | Engagement & Support | 3 | 1 | yes |
| `BO-799` | Agent Workspace | Engagement & Support | 3 | 2 | yes |
| `BO-800` | Routing & Queue Management | Engagement & Support | 3 | 2 | yes |
| `BO-801` | Sales & Service Actions | Engagement & Support | 3 | 1 | yes |
| `BO-802` | Sentiment, Quality & Escalation | Engagement & Support | 3 | 2 | yes |
| `BO-803` | Chat Analytics & Audit | Engagement & Support | 3 | 1 | yes |
| `BO-804` | Case Command Center | Engagement & Support | 3 | 2 | yes |
| `BO-805` | Case Queue & Search | Engagement & Support | 3 | 1 | yes |
| `BO-806` | Case Creation | Engagement & Support | 3 | 1 | yes |
| `BO-807` | Classification & Workflow | Engagement & Support | 3 | 1 | yes |
| `BO-808` | Assignment & Workload | Engagement & Support | 3 | 1 | yes |
| `BO-809` | SLA Policy Configuration | Engagement & Support | 3 | 2 | yes |
| `BO-810` | Escalation Rules | Engagement & Support | 3 | 1 | yes |
| `BO-811` | Case Workspace | Engagement & Support | 3 | 3 | yes |
| `BO-812` | Service Recovery | Engagement & Support | 3 | 1 | yes |
| `BO-813` | Case Analytics & Audit | Engagement & Support | 3 | 2 | yes |
| `BO-814` | Voice of Customer Center | Engagement & Support | 3 | 1 | yes |
| `BO-815` | Survey Builder | Engagement & Support | 3 | 1 | yes |
| `BO-816` | Survey Triggers & Distribution | Engagement & Support | 3 | 1 | yes |
| `BO-817` | NPS, CSAT & CES Configuration | Engagement & Support | 3 | 1 | yes |
| `BO-818` | Survey Responses & Insights | Engagement & Support | 3 | 1 | yes |
| `BO-819` | Review Collection & Rating Rules | Engagement & Support | 3 | 1 | yes |
| `BO-820` | Moderation & Publishing | Engagement & Support | 3 | 1 | yes |
| `BO-821` | AI Sentiment & Topic Analysis | Engagement & Support | 3 | 1 | yes |
| `BO-822` | Service Recovery Automation | Engagement & Support | 3 | 1 | yes |
| `BO-823` | VOC Analytics & Audit | Engagement & Support | 3 | 1 | yes |
| `BO-824` | Gamification Command Center | Engagement & Support | 3 | 1 | yes |
| `BO-825` | Challenge Builder | Engagement & Support | 3 | 1 | yes |
| `BO-826` | Achievement & Badge Engine | Engagement & Support | 3 | 1 | yes |
| `BO-827` | Points & Activity Rules | Engagement & Support | 3 | 1 | yes |
| `BO-828` | Milestones & Reward Rules | Engagement & Support | 3 | 1 | yes |
| `BO-829` | Family, Team & Event Challenges | Engagement & Support | 3 | 1 | yes |
| `BO-830` | Referral & Streak Management | Engagement & Support | 3 | 1 | yes |
| `BO-831` | Progress, Leaderboards & Hub | Engagement & Support | 3 | 1 | yes |
| `BO-832` | AI Engagement Optimization | Engagement & Support | 3 | 1 | yes |
| `BO-833` | Gamification Analytics & Audit | Engagement & Support | 3 | 1 | yes |
| `BO-834` | Digital Experience Center | Engagement & Support | 3 | 1 | yes |
| `BO-835` | Site, Brand & Domain Setup | Engagement & Support | 3 | 1 | yes |
| `BO-836` | Design System & Components | Engagement & Support | 3 | 1 | yes |
| `BO-837` | Page & Landing Builder | Engagement & Support | 3 | 2 | yes |
| `BO-838` | Content, Media & Forms | Engagement & Support | 3 | 2 | yes |
| `BO-839` | Dynamic Product Pages | Engagement & Support | 3 | 1 | yes |
| `BO-840` | Mobile App CMS | Engagement & Support | 3 | 1 | yes |
| `BO-841` | Personalization & Localization | Engagement & Support | 3 | 1 | yes |
| `BO-842` | SEO Management | Engagement & Support | 3 | 2 | yes |
| `BO-843` | Publishing, Analytics & Audit | Engagement & Support | 3 | 1 | yes |
| `BO-844` | Waiver Command Center | Engagement & Support | 3 | 1 | yes |
| `BO-845` | Waiver Template Builder | Engagement & Support | 3 | 1 | yes |
| `BO-846` | Assignment Rules | Engagement & Support | 3 | 2 | yes |
| `BO-847` | Version, Expiry & Renewal | Engagement & Support | 3 | 1 | yes |
| `BO-848` | Signature Experience Setup | Engagement & Support | 3 | 1 | yes |
| `BO-849` | Guardian & Group Signing | Engagement & Support | 3 | 1 | yes |
| `BO-850` | Pre-Arrival Completion | Engagement & Support | 3 | 1 | yes |
| `BO-851` | Verification & Access Control | Engagement & Support | 3 | 1 | yes |
| `BO-852` | Documents, Search & Retention | Engagement & Support | 3 | 2 | yes |
| `BO-853` | Legal Evidence & Audit | Engagement & Support | 3 | 1 | yes |
| `BO-854` | Resource Management Command Center | Rentals | 3 | 3 | yes |
| `BO-855` | Resource Type Configuration | Rentals | 3 | 3 | yes |
| `BO-856` | Resource Category Management | Rentals | 3 | 3 | yes |
| `BO-857` | Resource Creation & Profile | Rentals | 3 | 5 | yes |
| `BO-858` | Configurable Attribute Builder | Rentals | 3 | 2 | yes |
| `BO-859` | Resource Hierarchy & Parent–Child Relationships | Rentals | 3 | 2 | yes |
| `BO-860` | Resource Dependency Rules | Rentals | 3 | 2 | yes |
| `BO-861` | Resource Package & Bundle Configuration | Rentals | 3 | 3 | yes |
| `BO-862` | Multi-Venue Resource Assignment | Rentals | 3 | 2 | yes |
| `BO-863` | Resource Lifecycle, Governance & Audit | Rentals | 3 | 2 | yes |
| `BO-864` | Resource Calendar Command Center | Rentals | 3 | 3 | yes |
| `BO-865` | Calendar Filters, Search & Smart Discovery | Rentals | 3 | 2 | yes |
| `BO-866` | Resource Availability Schedule Configuration | Rentals | 3 | 2 | yes |
| `BO-867` | Resource Time-Slot Configuration | Rentals | 3 | 2 | yes |
| `BO-868` | Advance Reservation Management | Rentals | 3 | 3 | yes |
| `BO-869` | Recurring Reservation Configuration | Rentals | 3 | 2 | yes |
| `BO-870` | Operational Time & Resource Blocking | Rentals | 3 | 3 | yes |
| `BO-871` | Multi-Event Resource Planning | Rentals | 3 | 2 | yes |
| `BO-872` | Smart Assignment & Drag-and-Drop Reallocation | Rentals | 3 | 2 | yes |
| `BO-873` | Staff Resource Directory | Rentals | 3 | 1 | yes |
| `BO-874` | Staff Resource Profile | Rentals | 3 | 2 | yes |
| `BO-875` | Skills & Competency Management | Rentals | 3 | 1 | yes |
| `BO-876` | Certification & Expiry Management | Rentals | 3 | 2 | yes |
| `BO-877` | Qualification & Assignment Rule Engine | Rentals | 3 | 2 | yes |
| `BO-878` | Staff Availability & Working Pattern | Rentals | 3 | 2 | yes |
| `BO-879` | Shift Template & Assignment Configuration | Rentals | 3 | 2 | yes |
| `BO-880` | Break, Leave & Absence Configuration | Rentals | 3 | 2 | yes |
| `BO-881` | Overtime & Working-Hour Rules | Rentals | 3 | 1 | yes |
| `BO-882` | Workforce Integration & Synchronization Center | Rentals | 3 | 1 | yes |
| `BO-883` | Workforce Roster Command Center | Rentals | 3 | 2 | yes |
| `BO-884` | Attraction & Operational Staffing Roster | Rentals | 3 | 1 | yes |
| `BO-885` | Minimum Staffing & Coverage Rule Configuration | Rentals | 3 | 1 | yes |
| `BO-886` | Staffing Gap & Coverage Control Center | Rentals | 3 | 1 | yes |
| `BO-887` | Shift Marketplace & Workforce Requests | Rentals | 3 | 2 | yes |
| `BO-888` | Attendance & Live Workforce Command Center | Rentals | 3 | 1 | yes |
| `BO-889` | Staff Check-In, Check-Out & Attendance Exceptions | Rentals | 3 | 2 | yes |
| `BO-890` | Workforce Compliance Validation Center | Rentals | 3 | 1 | yes |
| `BO-891` | Labor Cost & Staffing Budget Control | Rentals | 3 | 1 | yes |
| `BO-892` | AI Workforce Planner & Roster Optimization | Rentals | 3 | 1 | yes |
| `BO-893` | Experience Resource Requirement Builder | Rentals | 3 | 2 | yes |
| `BO-894` | Staff-to-Experience Qualification Mapping | Rentals | 3 | 2 | yes |
| `BO-895` | Resource Combination Builder | Rentals | 3 | 2 | yes |
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
| `BO-910` | Maintenance & Resource Blocking | Rentals | 3 | 3 | yes |
| `BO-911` | Inspection, Condition & Compliance Management | Rentals | 3 | 3 | yes |
| `BO-912` | Asset Lifecycle, Depreciation & Retirement | Rentals | 3 | 2 | yes |
| `BO-913` | Event Resource Planning Command Center | Rentals | 3 | 1 | yes |
| `BO-914` | Event Resource Requirement Builder | Rentals | 3 | 1 | yes |
| `BO-915` | Venue & Space Allocation | Rentals | 3 | 2 | yes |
| `BO-916` | Equipment & Asset Allocation | Rentals | 3 | 1 | yes |
| `BO-917` | Event Staff & Personnel Allocation | Rentals | 3 | 1 | yes |
| `BO-918` | Event Resource Template Library | Rentals | 3 | 2 | yes |
| `BO-919` | AI Event Resource Forecasting | Rentals | 3 | 0 | yes |
| `BO-920` | Event Resource Cost Estimator | Rentals | 3 | 1 | yes |
| `BO-921` | Multi-Event Allocation & Conflict Optimizer | Rentals | 3 | 1 | yes |
| `BO-922` | Event Resource Approval & Readiness Gate | Rentals | 3 | 2 | yes |
| `BO-923` | AI Resource Intelligence Command Center | Rentals | 3 | 1 | yes |
| `BO-924` | Optimal Resource Recommendation Engine | Rentals | 3 | 0 | yes |
| `BO-925` | AI Staff Recommendation & Workforce Matching | Rentals | 3 | 0 | yes |
| `BO-926` | Resource Demand Forecasting | Rentals | 3 | 0 | yes |
| `BO-927` | AI Staffing Requirement Forecast | Rentals | 3 | 0 | yes |
| `BO-928` | AI Conflict Resolution Assistant | Rentals | 3 | 0 | yes |
| `BO-929` | Automatic Schedule Optimization | Rentals | 3 | 0 | yes |
| `BO-930` | Alternative & Replacement Resource | Rentals | 3 | 0 | yes |
| `BO-931` | Operational Scenario Simulator & Digital Twin | Rentals | 3 | 0 | yes |
| `BO-932` | Conversational AI Resource Copilot | Rentals | 3 | 0 | yes |
| `BO-933` | My Resource Operations Home | Rentals | 3 | 1 | yes |
| `BO-934` | My Schedule & Assignment Calendar | Rentals | 3 | 1 | yes |
| `BO-935` | Assignment Detail & Operational Brief | Rentals | 3 | 2 | yes |
| `BO-936` | Mobile Staff Check-In & Check-Out | Rentals | 3 | 1 | yes |
| `BO-937` | Resource Collection, Handover & Return | Rentals | 3 | 2 | yes |
| `BO-938` | Employee Requests & Resource Support | Rentals | 3 | 1 | yes |
| `BO-939` | Shift Change, Swap, Pickup & Release | Rentals | 3 | 2 | yes |
| `BO-940` | Manager Mobile Approval Center | Rentals | 3 | 2 | yes |
| `BO-941` | Operational Notifications & Live Alerts | Rentals | 3 | 1 | yes |
| `BO-942` | Mobile Operations Control & Offline Sync | Rentals | 3 | 1 | yes |
| `BO-943` | Resource Analytics Command Center | Rentals | 3 | 2 | yes |
| `BO-944` | Resource Utilization & Capacity Analytics | Rentals | 3 | 1 | yes |
| `BO-945` | Resource Cost, Revenue & Efficiency Analytics | Rentals | 3 | 1 | yes |
| `BO-946` | Demand Forecast Accuracy & Planning Performance | Rentals | 3 | 1 | yes |
| `BO-947` | Resource KPI, SLA & Performance Framework | Rentals | 3 | 1 | yes |
| `BO-948` | Resource Governance & Policy Center | Rentals | 3 | 2 | yes |
| `BO-949` | Approval, Exception & Override Control Center | Rentals | 3 | 1 | yes |
| `BO-950` | Audit Trail & Resource Decision History | Rentals | 3 | 1 | yes |
| `BO-951` | Resource Integration & System Health Center | Rentals | 3 | 1 | yes |
| `BO-952` | Executive Resource Intelligence & AI Improvement Center | Rentals | 3 | 1 | yes |
| `BO-953` | Seat Map Command Center | Access & Venue | 3 | 2 | yes |
| `BO-954` | Venue Canvas | Access & Venue | 3 | 3 | yes |
| `BO-955` | Sections & Zones | Access & Venue | 3 | 2 | yes |
| `BO-956` | Rows & Seats | Access & Venue | 3 | 2 | yes |
| `BO-957` | Standing Zones | Access & Venue | 3 | 1 | yes |
| `BO-958` | Suites & Boxes | Access & Venue | 3 | 1 | yes |
| `BO-959` | Stage & Focal Point | Access & Venue | 3 | 1 | yes |
| `BO-960` | Entrances, Exits & Aisles | Access & Venue | 3 | 1 | yes |
| `BO-961` | Amenities & Obstructions | Access & Venue | 3 | 1 | yes |
| `BO-962` | Templates, Validation & Publish | Access & Venue | 3 | 4 | yes |
| `BO-963` | Import Command Center | Access & Venue | 3 | 2 | yes |
| `BO-964` | PDF & Image Import | Access & Venue | 3 | 2 | yes |
| `BO-965` | SVG & CAD Import | Access & Venue | 3 | 2 | yes |
| `BO-966` | CSV & Excel Import | Access & Venue | 3 | 2 | yes |
| `BO-967` | AI Section Recognition | Access & Venue | 3 | 2 | yes |
| `BO-968` | AI Row & Seat Recognition | Access & Venue | 3 | 2 | yes |
| `BO-969` | AI Aisle, VIP & Accessibility | Access & Venue | 3 | 2 | yes |
| `BO-970` | AI Numbering & Labeling | Access & Venue | 3 | 1 | yes |
| `BO-971` | Validation & Correction | Access & Venue | 3 | 2 | yes |
| `BO-972` | AI Venue Designer & Publish | Access & Venue | 3 | 2 | yes |
| `BO-973` | Layout Command Center | Access & Venue | 3 | 1 | yes |
| `BO-974` | Template Library | Access & Venue | 3 | 2 | yes |
| `BO-975` | Event-Specific Layout | Access & Venue | 3 | 2 | yes |
| `BO-976` | Clone & Inheritance | Access & Venue | 3 | 2 | yes |
| `BO-977` | Version Compare | Access & Venue | 3 | 1 | yes |
| `BO-978` | Multi-Performance Assignment | Access & Venue | 3 | 2 | yes |
| `BO-979` | Temporary Seat Blocking | Access & Venue | 3 | 2 | yes |
| `BO-980` | Scheduled Seat Release | Access & Venue | 3 | 2 | yes |
| `BO-981` | Conflict & Impact Simulation | Access & Venue | 3 | 1 | yes |
| `BO-982` | Approval, Publish & Rollback | Access & Venue | 3 | 2 | yes |
| `BO-983` | Inventory Command Center | Access & Venue | 3 | 1 | yes |
| `BO-984` | Real-Time Seat Map | Access & Venue | 3 | 1 | yes |
| `BO-985` | Status Model Configuration | Access & Venue | 3 | 2 | yes |
| `BO-986` | Availability Tracker | Access & Venue | 3 | 1 | yes |
| `BO-987` | Hold Tracker | Access & Venue | 3 | 2 | yes |
| `BO-988` | Reservation Tracker | Access & Venue | 3 | 1 | yes |
| `BO-989` | Sales & Allocation Tracker | Access & Venue | 3 | 2 | yes |
| `BO-990` | Maintenance & Out of Service | Access & Venue | 3 | 2 | yes |
| `BO-991` | Seat History | Access & Venue | 3 | 1 | yes |
| `BO-992` | Audit & Reconciliation | Access & Venue | 3 | 1 | yes |
| `BO-993` | Experience Command Center | Access & Venue | 3 | 2 | yes |
| `BO-994` | Choose My Seats | Access & Venue | 3 | 2 | yes |
| `BO-995` | Find Seats For Me | Access & Venue | 3 | 1 | yes |
| `BO-996` | Filters & Interactive Legend | Access & Venue | 3 | 1 | yes |
| `BO-997` | Real-Time Availability & Locking | Access & Venue | 3 | 1 | yes |
| `BO-998` | Lock Timeout & Concurrency | Access & Venue | 3 | 2 | yes |
| `BO-999` | Cart & Multi-Seat Management | Access & Venue | 3 | 2 | yes |

