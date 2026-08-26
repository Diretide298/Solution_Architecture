# P12 Venue Support — platform

**Derived.** `python3 tools/derive-platform.py P12`. App `venue-support-web` · venue · web

| | |
|---|---|
| Screens | 8 |
| Operations | 33 |
| Contracts | 4 |
| Modules | 1 |
| Undrawn | 0 |
| Operations with no screen | 58 |
| Waves | wave2 2 · wave3 6 |

## Gaps

### 58 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `calculateTax` | finance | POST | Compute tax for a set of lines |
| `disputeObligation` | finance | POST | One entity disagrees with the amount |
| `getForeignTenderReport` | finance | GET | What was taken in which currency |
| `getUnifiedReconciliation` | finance | GET | Every money source against the ledger, in one view |
| `listInterEntityObligations` | finance | GET | What one entity owes another |
| `recordDeposit` | finance | POST | Money taken before the sale is complete |
| `recordSettlement` | finance | POST | One entity paid another |
| `recordWriteOff` | finance | POST | Write off an uncollectable balance |
| `resolveObligationDispute` | finance | POST | Agree what is actually owed |
| `runFxRevaluation` | finance | POST | Revalue monetary balances at close |
| `validateRecognitionSchedules` | finance | POST | Find product kinds claimed by more than one schedule |
| `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| `deleteGuestAccount` | identity | DELETE | Self-service account deletion |
| `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| `setPasswordPolicy` | identity | PUT | Length, breach check, lockout and step-up |
| `setSegregationRules` | identity | PUT | Which permissions may not be held together |
| `activateJourney` | marketing-crm | POST | Start it, or stop it |
| `addGuestNote` | marketing-crm | POST | What the floor needs to know about this table |
| `addSuppression` | marketing-crm | POST | Suppress an address |
| `createChallenge` | marketing-crm | POST | Define a challenge, mission or streak |
| `createForm` | marketing-crm | POST | Define a waiver, survey or capture form |
| `createInvitationCampaign` | marketing-crm | POST | A quota-bounded, addressed invitation |
| `createLoyaltyProgramme` | marketing-crm | POST | Create a loyalty programme |
| `createReferral` | marketing-crm | POST | Issue a referral code |
| `createUrlRedirect` | marketing-crm | POST | 301, 302 and custom redirects |
| `getJourneyPerformance` | marketing-crm | GET | Entrants, completions, goals reached |
| `getLostItemMatches` | marketing-crm | GET | Candidate matches, scored |
| `getMyChallenges` | marketing-crm | GET | Active challenges and how far along I am |
| `getSuppressionList` | marketing-crm | GET | Addresses suppressed from all sending |
| `getWaiverStatus` | marketing-crm | GET | Whether this guest may be issued a ticket that requires a waiver |
| `listMessageTriggers` | marketing-crm | GET | What fires a message, and when |
| `listReviews` | marketing-crm | GET | List guest reviews and ratings |
| `listSegmentMembers` | marketing-crm | GET | List guests currently matching a segment |
| `matchGuest` | marketing-crm | POST | Is this the same person we already have? |
| `mergeGuests` | marketing-crm | POST | Two records, one person |
| `recordLostItem` | marketing-crm | POST | Report something lost, or hand something in |
| `recordPrivacyIncident` | marketing-crm | POST | Log a personal-data breach and start the clock |
| `respondToReview` | marketing-crm | POST | Respond to a review |
| `retryMessageDispatch` | marketing-crm | POST | Send it again, or by another channel |
| `setCallDisposition` | marketing-crm | POST | Why the conversation ended, and any callback |
| … | | | 18 more |

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
| `SUP-006` | Knowledge Base Search | TODO | 3 | 0 | yes |
| `SUP-007` | Canned Response Management | TODO | 3 | 2 | yes |
| `SUP-008` | Agent Performance & SLA View | TODO | 3 | 10 | yes |

