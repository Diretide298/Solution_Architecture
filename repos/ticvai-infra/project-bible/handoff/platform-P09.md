# P09 TICVAI Web — platform

**Derived.** `python3 tools/derive-platform.py P09`. App `ticvai-web` · ticvai · web

| | |
|---|---|
| Screens | 37 |
| Operations | 128 |
| Contracts | 8 |
| Modules | 2 |
| Undrawn | 1 |
| Operations with no screen | 87 |
| Waves | wave1 11 · wave2 16 · wave3 10 |

## Gaps

### 87 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `createKnowledgeCollection` | ai | POST | Create a collection |
| `decideProposedAction` | ai | POST | Approve or reject a proposal |
| `generateConfiguration` | ai | POST | Draft a configuration from a description |
| `generateVenueLayout` | ai | POST | Draft a seat map from an uploaded plan |
| `ingestKnowledgeDocument` | ai | POST | Add a document |
| `listIndexJobs` | ai | GET | Indexing in flight and recently finished |
| `listIndexSources` | ai | GET | What is indexed, and how current it is |
| `listKnowledgeCollections` | ai | GET | Collections available to this tenant |
| `listProposedActions` | ai | GET | What the assistant has proposed and nobody has decided |
| `proposeTranslations` | ai | POST |  |
| `proposeWalkways` | ai | POST | Find walkable space in a drawing that has no vectors |
| `reindexSource` | ai | POST | Rebuild a source |
| `removeIndexEntry` | ai | DELETE | Remove one record from the index |
| `setIndexSource` | ai | PUT | Declare a source indexed |
| `authoriseWalletSpend` | cross-cell | POST | Hold funds against the guest's home-cell balance |
| `captureWalletAuthorisation` | cross-cell | POST | Capture a held amount |
| `createDsarRequest` | cross-cell | POST | Raise a data subject request across every linked cell |
| `createGuestLink` | cross-cell | POST | Link a guest's records across cells |
| `getDsarRequest` | cross-cell | GET | Track fan-out progress per cell |
| `getWalletAllocation` | cross-cell | GET | The consuming cell's bounded offline allocation |
| `releaseWalletAuthorisation` | cross-cell | POST | Release a hold without capturing |
| `resolveGuestLink` | cross-cell | GET | Find the link for a local subject |
| `revokeGuestLink` | cross-cell | DELETE | Sever a link on consent withdrawal |
| `revokeRedemptionRight` | cross-cell | DELETE | Revoke a right |
| `setWalletAllocationPolicy` | cross-cell | PUT | Set the allocation cap policy |
| `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| `deleteGuestAccount` | identity | DELETE | Self-service account deletion |
| `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| `grantDelegation` | identity | POST | Let one guest act for another |
| `listDelegations` | identity | GET | Who may act for this guest, and for whom they may act |
| `resolvePermissions` | identity | POST | Simulate a principal's effective permissions |
| `setPasswordPolicy` | identity | PUT | Length, breach check, lockout and step-up |
| `setSegregationRules` | identity | PUT | Which permissions may not be held together |
| `skipRolloutCell` | platform-ops | POST | Exclude a cell from this wave |
| `acknowledgeAlert` | reporting | POST | Take responsibility for it |
| `cancelReportExecution` | reporting | DELETE | Cancel a running execution |
| `createReportSchedule` | reporting | POST | Schedule a report |
| `deleteReportSchedule` | reporting | DELETE | Delete a schedule |
| `exportReportResult` | reporting | POST | Export a completed result |
| `getReportExecution` | reporting | GET | Execution status and result |
| … | | | 47 more |

### 1 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **TODO** — waves 1, 2, 3

### 1 screens nobody has drawn

- `ADM-037` AI Provider & Credentials — wave 1

## Modules

| Module | Screens | Waves |
|---|---|---|
| TODO | 36 | 1, 2, 3 |
| AI | 1 | 1 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `ADM-001` | Platform Login / MFA | TODO | 1 | 8 | yes |
| `ADM-002` | Platform Dashboard | TODO | 1 | 21 | yes |
| `ADM-003` | Cross-Tenant Health Dashboard | TODO | 2 | 10 | yes |
| `ADM-004` | Platform Audit Log | TODO | 2 | 1 | yes |
| `ADM-005` | Tenant Directory | TODO | 1 | 21 | yes |
| `ADM-006` | Tenant Hierarchy Explorer | TODO | 1 | 23 | yes |
| `ADM-007` | Module & Feature Entitlement | TODO | 1 | 21 | yes |
| `ADM-008` | Subscription & Plan Management | TODO | 1 | 28 | yes |
| `ADM-009` | Tenant Billing & Invoicing | TODO | 2 | 21 | yes |
| `ADM-010` | Usage Metering | TODO | 2 | 21 | yes |
| `ADM-011` | Licence & Seat Management | TODO | 2 | 21 | yes |
| `ADM-012` | Tenant Isolation & Resource Pool | TODO | 1 | 22 | yes |
| `ADM-013` | Tenant Performance Monitor | TODO | 2 | 7 | yes |
| `ADM-014` | Auto-Scaling Configuration | TODO | 3 | 7 | yes |
| `ADM-015` | API Rate Limit & Quota Management | TODO | 3 | 21 | yes |
| `ADM-016` | White-Label Branding Management | TODO | 2 | 41 | yes |
| `ADM-017` | Domain & Certificate Management | TODO | 2 | 41 | yes |
| `ADM-018` | Localisation & Language Pack | TODO | 2 | 41 | yes |
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
| `ADM-037` | AI Provider & Credentials | AI | 1 | 4 | **no** |

