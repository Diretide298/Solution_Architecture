# P13 Venue CMS — platform

**Derived.** `python3 tools/derive-platform.py P13`. App `venue-management-web` · venue · web

| | |
|---|---|
| Screens | 20 |
| Operations | 77 |
| Contracts | 8 |
| Modules | 1 |
| Undrawn | 0 |
| Operations with no screen | 118 |
| Waves | wave2 20 |

## Gaps

### 118 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `attachModifierGroup` | fnb | PUT | Give an item its choices |
| `clearTable` | fnb | POST | Mark a table cleared and free |
| `closeCorrectiveAction` | fnb | POST | Close a signed finding |
| `createCombo` | fnb | POST | A meal deal, priced as one thing |
| `createModifierGroup` | fnb | POST | Create a modifier group |
| `createTable` | fnb | POST | A table as a thing, not an inference |
| `escalateCorrectiveAction` | fnb | POST | Escalate a finding |
| `getTableVisit` | fnb | GET | Read a visit with all its orders |
| `rebalanceStationLoad` | fnb | POST | Move work between stations mid-service |
| `recordCorrectiveAction` | fnb | POST | Record what was done about a finding |
| `requestBill` | fnb | POST | The party asked to pay |
| `resolveBookingConflict` | fnb | GET | Two bookings, one table — and what to do about it |
| `sendBookingConfirmation` | fnb | POST | Confirm a booking, and ask them to confirm back |
| `sendOrderNotification` | fnb | POST | Tell the guest where their order is |
| `setComboSlots` | fnb | PUT | What the guest chooses, and what it costs extra |
| `setKitchenSla` | fnb | PUT | How long a ticket may sit before it is late |
| `setSectionLayout` | fnb | PUT | Divide the floor into sections and give each a server |
| `updateTable` | fnb | PUT | Change what a table is |
| `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| `setPasswordPolicy` | identity | PUT | Length, breach check, lockout and step-up |
| `setSegregationRules` | identity | PUT | Which permissions may not be held together |
| `updateMaintenancePlan` | maintenance | PATCH | Amend or suspend a plan |
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
| … | | | 78 more |

## Modules

| Module | Screens | Waves |
|---|---|---|
| White Label | 20 | 2 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `CMS-001` | Tenant Workspace | White Label | 2 | 21 | yes |
| `CMS-002` | Brand Kit | White Label | 2 | 4 | yes |
| `CMS-003` | Typography | White Label | 2 | 4 | yes |
| `CMS-004` | Logo & Assets | White Label | 2 | 7 | yes |
| `CMS-005` | Theme Editor | White Label | 2 | 2 | yes |
| `CMS-006` | Component Preview | White Label | 2 | 5 | yes |
| `CMS-007` | Page Builder | White Label | 2 | 2 | yes |
| `CMS-008` | Content Blocks | White Label | 2 | 2 | yes |
| `CMS-009` | Navigation & Menus | White Label | 2 | 5 | yes |
| `CMS-010` | Media Library | White Label | 2 | 12 | yes |
| `CMS-011` | Translations | White Label | 2 | 1 | yes |
| `CMS-012` | RTL Preview | White Label | 2 | 2 | yes |
| `CMS-013` | SEO & Metadata | White Label | 2 | 0 | yes |
| `CMS-014` | Publishing Workflow | White Label | 2 | 3 | yes |
| `CMS-015` | Version History | White Label | 2 | 3 | yes |
| `CMS-016` | Site Settings | White Label | 2 | 1 | yes |
| `CMS-017` | Domain & Certificate | White Label | 2 | 0 | yes |
| `CMS-018` | Consent & Legal | White Label | 2 | 11 | yes |
| `CMS-019` | User Access | White Label | 2 | 2 | yes |
| `CMS-020` | Change Log | White Label | 2 | 1 | yes |

