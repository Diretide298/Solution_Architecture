# P08 Venue Management — platform

**Derived.** `python3 tools/derive-platform.py P08`. App `venue-management-web` · venue · web

| | |
|---|---|
| Screens | 363 |
| Operations | 666 |
| Contracts | 27 |
| Modules | 8 |
| Undrawn | 0 |
| Operations with no screen | 228 |
| Waves | wave1 60 · wave2 79 · wave3 224 |

## Gaps

### 228 operations with no screen here

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
| `issueAccreditationBadge` | approvals | POST | Issue a badge |
| `assessProductChange` | catalogue | POST | What a change would touch, before making it |
| `bulkChangePrices` | catalogue | POST | Reprice a category or a whole catalogue |
| `cloneProduct` | catalogue | POST | Copy a product as a new draft |
| `commitCatalogueImport` | catalogue | POST | Apply a parsed catalogue import |
| `createDonationCampaign` | catalogue | POST | Create a campaign |
| `freezeEntitlement` | catalogue | POST | Pause a membership at the guest's request |
| `listDonationCampaigns` | catalogue | GET | Campaigns a guest can give to |
| `listWaitlistEntries` | catalogue | GET | Who is waiting for capacity |
| `offerWaitlistCapacity` | catalogue | POST | Tell a waiting guest that capacity appeared |
| `reinstateEntitlement` | catalogue | POST | Lift a suspension |
| `restoreProductVersion` | catalogue | POST | Put a previous version back |
| `suspendEntitlement` | catalogue | POST | Suspend or reinstate an entitlement |
| `updateDonationCampaign` | catalogue | PATCH | Amend or close a campaign |
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
| `attachModifierGroup` | fnb | PUT | Give an item its choices |
| `clearTable` | fnb | POST | Mark a table cleared and free |
| `closeCorrectiveAction` | fnb | POST | Close a signed finding |
| … | | | 188 more |

### 8 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Access & Venue** — waves 1, 2, 3
- **Food & Beverage** — waves 1, 2
- **Guests & Marketing** — waves 1, 2
- **Orders & Money** — waves 1, 2, 3
- **People & Access Rights** — waves 1, 2, 3
- **Sell** — waves 1, 2, 3
- **Stock & Supply** — waves 1, 2
- **Venue Operations** — waves 1, 2

## Modules

| Module | Screens | Waves |
|---|---|---|
| Access & Venue | 175 | 1, 2, 3 |
| Sell | 75 | 1, 2, 3 |
| Orders & Money | 59 | 1, 2, 3 |
| Venue Operations | 15 | 1, 2 |
| Stock & Supply | 15 | 1, 2 |
| People & Access Rights | 12 | 1, 2, 3 |
| Food & Beverage | 8 | 1, 2 |
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
| `BO-047` | F&B Order Management | Orders & Money | 2 | 14 | yes |
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
| `BO-076` | Revenue Recognition | Orders & Money | 2 | 4 | yes |
| `BO-077` | FX Rates & Variances | Orders & Money | 2 | 4 | yes |
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
| `BO-097` | Check Out & Check In | Access & Venue | 2 | 4 | yes |
| `BO-098` | Qualifications | Access & Venue | 2 | 1 | yes |
| `BO-099` | Session Manifest | Access & Venue | 2 | 2 | yes |
| `BO-100` | Venue Home | Venue Operations | 1 | 2 | yes |
| `BO-101` | Orders & Money | Orders & Money | 1 | 3 | yes |
| `BO-102` | Sell | Sell | 1 | 3 | yes |
| `BO-103` | Access & Venue | Access & Venue | 1 | 3 | yes |
| `BO-104` | Food & Beverage | Food & Beverage | 1 | 3 | yes |
| `BO-105` | Stock & Supply | Stock & Supply | 1 | 4 | yes |
| `BO-106` | People & Access Rights | People & Access Rights | 1 | 2 | yes |
| `BO-107` | Guests & Marketing | Guests & Marketing | 1 | 3 | yes |
| `BO-108` | Venue Operations | Venue Operations | 1 | 4 | yes |
| `BO-109` | Menu Builder & POS Layout Designer | Sell | 2 | 3 | yes |
| `BO-110` | Recipe & BOM Management | Sell | 2 | 2 | yes |
| `BO-111` | Ingredient Substitution, Allergen & Nutrition | Sell | 2 | 4 | yes |
| `BO-112` | Production Planning & Production Sheets | Sell | 2 | 1 | yes |
| `BO-113` | Central Kitchen & Commissary Management | Sell | 2 | 2 | yes |
| `BO-114` | Variants, Attributes, Barcode & RFID Management | Sell | 2 | 2 | yes |
| `BO-115` | Category, Brand & Merchandise Hierarchy | Sell | 2 | 5 | yes |
| `BO-116` | Merchandising & Product Presentation | Sell | 2 | 7 | yes |
| `BO-117` | Product Import, Governance & AI Configuration Assistant | Sell | 2 | 5 | yes |
| `BO-118` | Campaign & Audience Management | Sell | 2 | 6 | yes |
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
| `BO-160` | Multi-Park & Crossover Rules | Access & Venue | 3 | 1 | yes |
| `BO-161` | Guest, Companion & Eligibility Rules | Access & Venue | 3 | 1 | yes |
| `BO-162` | Group Admission & Quantity Validation | Access & Venue | 3 | 1 | yes |
| `BO-163` | Rule Simulation, Conflict Check & Publication | Access & Venue | 3 | 1 | yes |
| `BO-164` | Digital Credential Security Command Center | Access & Venue | 3 | 1 | yes |
| `BO-165` | Dynamic QR Security Profile Builder | Access & Venue | 3 | 1 | yes |
| `BO-166` | Credential Activation & Display Rules | Access & Venue | 3 | 1 | yes |
| `BO-167` | Device Binding & Session Security | Access & Venue | 3 | 1 | yes |
| `BO-168` | BLE Beacon & Geofence Configuration | Access & Venue | 3 | 1 | yes |
| `BO-169` | Credential Transfer & Rebinding | Access & Venue | 3 | 1 | yes |
| `BO-170` | Credential Revocation & Lifecycle Events | Access & Venue | 3 | 1 | yes |
| `BO-171` | Offline Cryptographic Validation Profile | Access & Venue | 3 | 1 | yes |
| `BO-172` | Embedded Entitlement Payload Designer | Access & Venue | 3 | 1 | yes |
| `BO-173` | Credential Security Simulation, Audit & Publication | Access & Venue | 3 | 1 | yes |
| `BO-174` | Media & Credential Command Center | Access & Venue | 3 | 1 | yes |
| `BO-175` | Media Type & Technology Library | Access & Venue | 3 | 1 | yes |
| `BO-176` | Virtual Credential & Media Association | Access & Venue | 3 | 1 | yes |
| `BO-177` | Verification Method Selection & Locking | Access & Venue | 3 | 1 | yes |
| `BO-178` | Media Issuance & Encoding Profile | Access & Venue | 3 | 1 | yes |
| `BO-179` | Media Swap & Replacement | Access & Venue | 3 | 1 | yes |
| `BO-180` | RFID & NFC Configuration | Access & Venue | 3 | 1 | yes |
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
| `BO-220` | Multi-Park & Crossover Journey Orchestrator | Access & Venue | 3 | 1 | yes |
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
| `BO-264` | Group Sales Command Center | Sell | 3 | 1 | yes |
| `BO-265` | Group Enquiry & Opportunity Capture | Sell | 3 | 1 | yes |
| `BO-266` | Group Customer & Organization Profile | Sell | 3 | 1 | yes |
| `BO-267` | Group Requirements, Availability & Capacity Planner | Sell | 3 | 1 | yes |
| `BO-268` | Group Package & Experience Builder | Sell | 3 | 1 | yes |
| `BO-269` | Group Quotation Builder & Proposal Generation | Sell | 3 | 1 | yes |
| `BO-270` | Quote Revision, Negotiation & Version Management | Sell | 3 | 1 | yes |
| `BO-271` | Group Discount, Exception & Approval Workflow | Sell | 3 | 1 | yes |
| `BO-272` | Quote-to-Booking Conversion & Confirmation | Sell | 3 | 1 | yes |
| `BO-273` | Group Booking 360° & Handover Workspace | Sell | 3 | 1 | yes |
| `BO-274` | Group Booking Operations Command Center | Sell | 3 | 1 | yes |
| `BO-275` | Group Operational Planning & Task Workspace | Sell | 3 | 1 | yes |
| `BO-276` | Participants, Guest Lists & Group Structure | Sell | 3 | 1 | yes |
| `BO-277` | Group Payment, Deposit & Balance Management | Sell | 3 | 1 | yes |
| `BO-278` | Group Ticket, Seat & Entitlement Allocation | Sell | 3 | 1 | yes |
| `BO-279` | Group Ticket Fulfillment & Distribution | Sell | 3 | 1 | yes |
| `BO-280` | Group Arrival, Check-In & Admission Operations | Sell | 3 | 1 | yes |
| `BO-281` | Group Amendments, Cancellation & Refund Operations | Sell | 3 | 1 | yes |
| `BO-282` | Group Booking Reconciliation, Closure & Performance | Sell | 3 | 1 | yes |
| `BO-283` | Group Sales Analytics & AI Intelligence Center | Sell | 3 | 1 | yes |
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
| `BO-314` | Amendment & After-Sales Command Center | Orders & Money | 3 | 1 | yes |
| `BO-315` | Order Amendment Workspace | Orders & Money | 3 | 1 | yes |
| `BO-316` | Amendment Eligibility & Policy Rule Builder | Orders & Money | 3 | 1 | yes |
| `BO-317` | Cancellation & Partial Cancellation Policy Configuration | Orders & Money | 3 | 1 | yes |
| `BO-318` | Refund Policy & Refund Calculation Configuration | Orders & Money | 3 | 1 | yes |
| `BO-319` | Void, Reversal & Same-Day Correction Management | Orders & Money | 3 | 1 | yes |
| `BO-320` | Ticket Reissue & Fulfillment Regeneration | Orders & Money | 3 | 1 | yes |
| `BO-321` | After-Sales Financial Settlement & Adjustment Workspace | Orders & Money | 3 | 1 | yes |
| `BO-322` | Approval, Exception & Service Recovery Management | Orders & Money | 3 | 1 | yes |
| `BO-323` | Amendment History, Audit & After-Sales Analytics | Orders & Money | 3 | 1 | yes |
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
| `BO-334` | Virtual Ticket Command Center | Access & Venue | 3 | 1 | yes |
| `BO-335` | Virtual Ticket Identity & Master Record Configuration | Access & Venue | 3 | 1 | yes |
| `BO-336` | Virtual Ticket Status & Lifecycle Model | Access & Venue | 3 | 1 | yes |
| `BO-337` | Media Type & Credential Technology Registry | Access & Venue | 3 | 1 | yes |
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

