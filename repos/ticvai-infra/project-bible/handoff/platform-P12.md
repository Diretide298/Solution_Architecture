# P12 Venue Support — platform

**Derived.** `python3 tools/derive-platform.py P12`. App `venue-support-web` · venue · web

| | |
|---|---|
| Screens | 8 |
| Operations | 74 |
| Contracts | 5 |
| Modules | 1 |
| Undrawn | 0 |
| Operations with no screen | 75 |
| Waves | wave2 2 · wave3 6 |

## Gaps

### 75 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `calculateTax` | finance | POST | Compute tax for a set of lines |
| `disputeObligation` | finance | POST | One entity disagrees with the amount |
| `getUnifiedReconciliation` | finance | GET | Every money source against the ledger, in one view |
| `recordDeposit` | finance | POST | Money taken before the sale is complete |
| `recordSettlement` | finance | POST | One entity paid another |
| `recordWriteOff` | finance | POST | Write off an uncollectable balance |
| `resolveObligationDispute` | finance | POST | Agree what is actually owed |
| `settleDeposit` | finance | POST | Convert to revenue, return it, or forfeit it |
| `validateRecognitionSchedules` | finance | POST | Find product kinds claimed by more than one schedule |
| `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| `deleteGuestAccount` | identity | DELETE | Self-service account deletion |
| `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| `grantDelegation` | identity | POST | Let one guest act for another |
| `listDelegations` | identity | GET | Who may act for this guest, and for whom they may act |
| `resolvePermissions` | identity | POST | Simulate a principal's effective permissions |
| `setPasswordPolicy` | identity | PUT | Length, breach check, lockout and step-up |
| `setSegregationRules` | identity | PUT | Which permissions may not be held together |
| `activateJourney` | marketing-crm | POST | Start it, or stop it |
| `addSuppression` | marketing-crm | POST | Suppress an address |
| `createChallenge` | marketing-crm | POST | Define a challenge, mission or streak |
| `createForm` | marketing-crm | POST | Define a waiver, survey or capture form |
| `createInvitationCampaign` | marketing-crm | POST | A quota-bounded, addressed invitation |
| `createJourney` | marketing-crm | POST | Define an automated journey |
| `createLoyaltyProgramme` | marketing-crm | POST | Create a loyalty programme |
| `createReferral` | marketing-crm | POST | Issue a referral code |
| `createSegment` | marketing-crm | POST | Create a segment |
| `createUrlRedirect` | marketing-crm | POST | 301, 302 and custom redirects |
| `getJourneyPerformance` | marketing-crm | GET | Entrants, completions, goals reached |
| `getLostItemMatches` | marketing-crm | GET | Candidate matches, scored |
| `getMyChallenges` | marketing-crm | GET | Active challenges and how far along I am |
| `getSuppressionList` | marketing-crm | GET | Addresses suppressed from all sending |
| `getWaiverStatus` | marketing-crm | GET | Whether this guest may be issued a ticket that requires a waiver |
| `identifyGuest` | marketing-crm | POST | Resolve any identifier to a guest |
| `listJourneys` | marketing-crm | GET | Automated journeys |
| `listLostItems` | marketing-crm | GET | Reported and found, with suggested matches |
| `listMessageTriggers` | marketing-crm | GET | What fires a message, and when |
| `listReviews` | marketing-crm | GET | List guest reviews and ratings |
| `listSegmentMembers` | marketing-crm | GET | List guests currently matching a segment |
| `listSegments` | marketing-crm | GET | List segments |
| `matchLostItem` | marketing-crm | POST | Tie a report to a found item, or hand it back |
| … | | | 35 more |

### 1 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **TODO** — waves 2, 3

## Modules

| Module | Screens | Waves |
|---|---|---|
| TODO | 8 | 2, 3 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `SUP-001` | Agent Login | TODO | 3 | 8 | yes |
| `SUP-002` | Agent Dashboard | TODO | 3 | 9 | yes |
| `SUP-003` | Availability & Routing Settings | TODO | 3 | 1 | yes |
| `SUP-004` | Conversation Queue | TODO | 2 | 10 | yes |
| `SUP-005` | Live Chat Workspace | TODO | 2 | 11 | yes |
| `SUP-006` | Knowledge Base Search | TODO | 3 | 41 | yes |
| `SUP-007` | Canned Response Management | TODO | 3 | 2 | yes |
| `SUP-008` | Agent Performance & SLA View | TODO | 3 | 10 | yes |

