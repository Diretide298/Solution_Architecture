# P13 Venue CMS — platform

**Derived.** `python3 tools/derive-platform.py P13`. App `venue-management-web` · venue · web

| | |
|---|---|
| Screens | 20 |
| Operations | 99 |
| Contracts | 8 |
| Modules | 1 |
| Undrawn | 0 |
| Operations with no screen | 116 |
| Waves | wave2 20 |

## Gaps

### 116 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `clearTable` | fnb | POST | Mark a table cleared and free |
| `closeTableVisit` | fnb | POST | Settle and close a visit |
| `completeProductionRun` | fnb | POST | Record what was actually made |
| `createModifierGroup` | fnb | POST | Create a modifier group |
| `createTableReservation` | fnb | POST | Book a table in advance |
| `getBill` | fnb | GET | Bill for a visit |
| `getTableVisit` | fnb | GET | Read a visit with all its orders |
| `joinRestaurantWaitlist` | fnb | POST | Add a party to an outlet's waitlist |
| `listModifierGroups` | fnb | GET | List modifier groups |
| `listRecipes` | fnb | GET | List recipes |
| `listTableReservations` | fnb | GET | Bookings for a service period |
| `mergeTableVisits` | fnb | POST | Merge another visit into this one |
| `openTableVisit` | fnb | POST | Seat a party and open a visit |
| `planProductionRun` | fnb | POST | Plan a batch, for one outlet or several |
| `requestBill` | fnb | POST | The party asked to pay |
| `seatTableReservation` | fnb | POST | The party arrived and has been sat down |
| `setItemAvailability` | fnb | PUT | Mark an item available or eighty-sixed |
| `setRecipe` | fnb | PUT | Define a recipe for a menu item |
| `splitBill` | fnb | POST | Split a bill |
| `transferTableVisit` | fnb | POST | Move a check to another server |
| `updateTableReservation` | fnb | PATCH | Change or cancel a booking |
| `updateTableVisit` | fnb | PATCH | Amend covers, move table, or reassign server |
| `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| `deleteGuestAccount` | identity | DELETE | Self-service account deletion |
| `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| `resolvePermissions` | identity | POST | Simulate a principal's effective permissions |
| `setPasswordPolicy` | identity | PUT | Length, breach check, lockout and step-up |
| `setSegregationRules` | identity | PUT | Which permissions may not be held together |
| `updateMaintenancePlan` | maintenance | PATCH | Amend or suspend a plan |
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
| … | | | 76 more |

## Modules

| Module | Screens | Waves |
|---|---|---|
| White Label | 20 | 2 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `CMS-001` | Tenant Workspace | White Label | 2 | 21 | yes |
| `CMS-002` | Brand Kit | White Label | 2 | 4 | yes |
| `CMS-003` | Typography | White Label | 2 | 41 | yes |
| `CMS-004` | Logo & Assets | White Label | 2 | 7 | yes |
| `CMS-005` | Theme Editor | White Label | 2 | 2 | yes |
| `CMS-006` | Component Preview | White Label | 2 | 41 | yes |
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

