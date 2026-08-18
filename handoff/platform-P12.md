# P12 Venue Support — platform

**Derived.** `python3 tools/derive-platform.py P12`. App `venue-support-web` · venue · web

| | |
|---|---|
| Screens | 8 |
| Operations | 74 |
| Contracts | 5 |
| Modules | 4 |
| Undrawn | 0 |
| Operations with no screen | 29 |
| Waves | wave2 2 · wave3 6 |

## Gaps

### 29 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `calculateTax` | finance | POST | Compute tax for a set of lines |
| `disputeObligation` | finance | POST | One entity disagrees with the amount |
| `recordSettlement` | finance | POST | One entity paid another |
| `resolveObligationDispute` | finance | POST | Agree what is actually owed |
| `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| `deleteGuestAccount` | identity | DELETE | Self-service account deletion |
| `resolvePermissions` | identity | POST | Simulate a principal's effective permissions |
| `addSuppression` | marketing-crm | POST | Suppress an address |
| `createLoyaltyProgramme` | marketing-crm | POST | Create a loyalty programme |
| `createSegment` | marketing-crm | POST | Create a segment |
| `getSuppressionList` | marketing-crm | GET | Addresses suppressed from all sending |
| `listReviews` | marketing-crm | GET | List guest reviews and ratings |
| `listSegmentMembers` | marketing-crm | GET | List guests currently matching a segment |
| `listSegments` | marketing-crm | GET | List segments |
| `previewSegment` | marketing-crm | POST | Estimate segment size and reachability |
| `respondToReview` | marketing-crm | POST | Respond to a review |
| `setConsentPurposes` | marketing-crm | PUT | Configure consent purposes |
| `startKioskAssist` | marketing-crm | POST | A staff member helps a guest at a kiosk, remotely |
| `cancelReportExecution` | reporting | DELETE | Cancel a running execution |
| `createReportSchedule` | reporting | POST | Schedule a report |
| `deleteReportSchedule` | reporting | DELETE | Delete a schedule |
| `exportReportResult` | reporting | POST | Export a completed result |
| `getReportExecution` | reporting | GET | Execution status and result |
| `getReportExport` | reporting | GET | Export status and download link |
| `getReportResult` | reporting | GET | Paged result rows |
| `listReportExecutions` | reporting | GET | List executions |
| `listReportFields` | reporting | GET | Fields available for a data source |
| `listReportSchedules` | reporting | GET | List scheduled reports |
| `updateReportSchedule` | reporting | PATCH | Amend, pause or resume a schedule |

### 1 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **marketing-crm** — waves 2, 3

## Modules

| Module | Screens | Waves |
|---|---|---|
| marketing-crm | 5 | 2, 3 |
| identity | 1 | 3 |
| white-label | 1 | 3 |
| reporting | 1 | 3 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `SUP-001` | Agent Login | identity | 3 | 8 | yes |
| `SUP-002` | Agent Dashboard | marketing-crm | 3 | 9 | yes |
| `SUP-003` | Availability & Routing Settings | marketing-crm | 3 | 1 | yes |
| `SUP-004` | Conversation Queue | marketing-crm | 2 | 10 | yes |
| `SUP-005` | Live Chat Workspace | marketing-crm | 2 | 11 | yes |
| `SUP-006` | Knowledge Base Search | white-label | 3 | 41 | yes |
| `SUP-007` | Canned Response Management | marketing-crm | 3 | 2 | yes |
| `SUP-008` | Agent Performance & SLA View | reporting | 3 | 10 | yes |

