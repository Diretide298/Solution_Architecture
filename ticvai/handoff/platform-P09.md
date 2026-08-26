# P09 TICVAI Web — platform

**Derived.** `python3 tools/derive-platform.py P09`. App `ticvai-web` · ticvai · web

| | |
|---|---|
| Screens | 37 |
| Operations | 110 |
| Contracts | 9 |
| Modules | 2 |
| Undrawn | 0 |
| Operations with no screen | 70 |
| Waves | wave1 11 · wave2 16 · wave3 10 |

## Gaps

### 70 operations with no screen here

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
| `authoriseWalletSpend` | cross-cell | POST | Hold funds against the guest's home-cell balance |
| `captureWalletAuthorisation` | cross-cell | POST | Capture a held amount |
| `getWalletAllocation` | cross-cell | GET | The consuming cell's bounded offline allocation |
| `releaseWalletAuthorisation` | cross-cell | POST | Release a hold without capturing |
| `setWalletAllocationPolicy` | cross-cell | PUT | Set the allocation cap policy |
| `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| `setPasswordPolicy` | identity | PUT | Length, breach check, lockout and step-up |
| `setSegregationRules` | identity | PUT | Which permissions may not be held together |
| `skipRolloutCell` | platform-ops | POST | Exclude a cell from this wave |
| `cancelReportExecution` | reporting | DELETE | Cancel a running execution |
| `deleteReportSchedule` | reporting | DELETE | Delete a schedule |
| `exportReportResult` | reporting | POST | Export a completed result |
| `getReportExecution` | reporting | GET | Execution status and result |
| `getReportExport` | reporting | GET | Export status and download link |
| `getReportResult` | reporting | GET | Paged result rows |
| `listAlertRules` | reporting | GET | What raises an alert, and when |
| `listReportFields` | reporting | GET | Fields available for a data source |
| `listReportSchedules` | reporting | GET | List scheduled reports |
| `listSeededReports` | reporting | GET |  |
| `updateReportSchedule` | reporting | PATCH | Amend, pause or resume a schedule |
| `cancelInvoice` | subscription | POST | Cancel or credit an invoice |
| `cancelSubscription` | subscription | POST | Terminate a tenant subscription |
| `createPartnerUser` | subscription | POST | Add a user to a partner branch |
| `disputeInvoice` | subscription | POST | Raise a dispute |
| `executeTenantMigration` | subscription | POST | Move the tenant |
| `exportPartnerInvoice` | subscription | POST | Partner invoice and settlement, in an ERP format |
| `launchCellCluster` | subscription | POST | Launch an identical cluster |
| `listCellClusters` | subscription | GET | Clusters in a region |
| … | | | 30 more |

### 1 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **TODO** — waves 1, 2, 3

## Modules

| Module | Screens | Waves |
|---|---|---|
| TODO | 36 | 1, 2, 3 |
| AI | 1 | 1 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `ADM-001` | Platform Login / MFA | TODO | 1 | 8 | yes |
| `ADM-002` | Platform Dashboard | TODO | 1 | 6 | yes |
| `ADM-003` | Cross-Tenant Health Dashboard | TODO | 2 | 10 | yes |
| `ADM-004` | Platform Audit Log | TODO | 2 | 1 | yes |
| `ADM-005` | Tenant Directory | TODO | 1 | 15 | yes |
| `ADM-006` | Tenant Hierarchy Explorer | TODO | 1 | 9 | yes |
| `ADM-007` | Module & Feature Entitlement | TODO | 1 | 9 | yes |
| `ADM-008` | Subscription & Plan Management | TODO | 1 | 19 | yes |
| `ADM-009` | Tenant Billing & Invoicing | TODO | 2 | 9 | yes |
| `ADM-010` | Usage Metering | TODO | 2 | 7 | yes |
| `ADM-011` | Licence & Seat Management | TODO | 2 | 11 | yes |
| `ADM-012` | Tenant Isolation & Resource Pool | TODO | 1 | 8 | yes |
| `ADM-013` | Tenant Performance Monitor | TODO | 2 | 7 | yes |
| `ADM-014` | Auto-Scaling Configuration | TODO | 3 | 7 | yes |
| `ADM-015` | API Rate Limit & Quota Management | TODO | 3 | 9 | yes |
| `ADM-016` | White-Label Branding Management | TODO | 2 | 11 | yes |
| `ADM-017` | Domain & Certificate Management | TODO | 2 | 4 | yes |
| `ADM-018` | Localisation & Language Pack | TODO | 2 | 5 | yes |
| `ADM-019` | Global Configuration & Defaults | TODO | 2 | 4 | yes |
| `ADM-020` | Platform User Directory | TODO | 1 | 4 | yes |
| `ADM-021` | Platform Role Management | TODO | 1 | 2 | yes |
| `ADM-022` | Release & Version Management | TODO | 2 | 7 | yes |
| `ADM-023` | Staging Promotion & Approval | TODO | 2 | 7 | yes |
| `ADM-024` | Release Notification Composer | TODO | 3 | 2 | yes |
| `ADM-025` | Tenant Upgrade Scheduler | TODO | 2 | 2 | yes |
| `ADM-026` | End-of-Support Notice Management | TODO | 3 | 2 | yes |
| `ADM-027` | Database Migration Console | TODO | 1 | 6 | yes |
| `ADM-028` | Environment Registry | TODO | 2 | 2 | yes |
| `ADM-029` | Deployment Monitor | TODO | 2 | 12 | yes |
| `ADM-030` | Infrastructure Sizing & Scaling Policy | TODO | 3 | 7 | yes |
| `ADM-031` | Security & Compliance Dashboard | TODO | 3 | 4 | yes |
| `ADM-032` | WAF & Security Policy View | TODO | 3 | 7 | yes |
| `ADM-033` | Backup & DR Status | TODO | 2 | 7 | yes |
| `ADM-034` | Archival Job Monitor | TODO | 3 | 7 | yes |
| `ADM-035` | Support & Escalation Console | TODO | 3 | 2 | yes |
| `ADM-036` | Platform Notification Broadcast | TODO | 3 | 2 | yes |
| `ADM-037` | AI Provider & Credentials | AI | 1 | 4 | yes |

