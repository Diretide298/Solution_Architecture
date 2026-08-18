# P13 Venue CMS — platform

**Derived.** `python3 tools/derive-platform.py P13`. App `venue-management-web` · venue · web

| | |
|---|---|
| Screens | 20 |
| Operations | 99 |
| Contracts | 8 |
| Modules | 8 |
| Undrawn | 0 |
| Operations with no screen | 53 |
| Waves | wave2 20 |

## Gaps

### 53 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `clearTable` | fnb | POST | Mark a table cleared and free |
| `closeTableVisit` | fnb | POST | Settle and close a visit |
| `createModifierGroup` | fnb | POST | Create a modifier group |
| `createTableReservation` | fnb | POST | Book a table in advance |
| `getBill` | fnb | GET | Bill for a visit |
| `getTableVisit` | fnb | GET | Read a visit with all its orders |
| `listModifierGroups` | fnb | GET | List modifier groups |
| `listRecipes` | fnb | GET | List recipes |
| `listTableReservations` | fnb | GET | Bookings for a service period |
| `mergeTableVisits` | fnb | POST | Merge another visit into this one |
| `openTableVisit` | fnb | POST | Seat a party and open a visit |
| `requestBill` | fnb | POST | The party asked to pay |
| `seatTableReservation` | fnb | POST | The party arrived and has been sat down |
| `setItemAvailability` | fnb | PUT | Mark an item available or eighty-sixed |
| `setRecipe` | fnb | PUT | Define a recipe for a menu item |
| `splitBill` | fnb | POST | Split a bill |
| `updateTableReservation` | fnb | PATCH | Change or cancel a booking |
| `updateTableVisit` | fnb | PATCH | Amend covers, move table, or reassign server |
| `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| `deleteGuestAccount` | identity | DELETE | Self-service account deletion |
| `resolvePermissions` | identity | POST | Simulate a principal's effective permissions |
| `updateMaintenancePlan` | maintenance | PATCH | Amend or suspend a plan |
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
| `convertReservation` | orders | POST | Convert a reservation into an order |
| `createCart` | orders | POST | Start a cart |
| `createReservation` | orders | POST | Hold without payment |
| `extendReservation` | orders | POST | Extend a reservation |
| `listAbandonedCarts` | orders | GET | Carts that lapsed without checking out |
| `voidPayment` | orders | POST | Release an authorisation before it is captured |
| `cancelInvoice` | subscription | POST | Cancel or credit an invoice |
| … | | | 13 more |

## Modules

| Module | Screens | Waves |
|---|---|---|
| white-label | 12 | 2 |
| White Label | 2 | 2 |
| subscription | 1 | 2 |
| maintenance | 1 | 2 |
| fnb | 1 | 2 |
| assets | 1 | 2 |
| marketing-crm | 1 | 2 |
| identity | 1 | 2 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `CMS-001` | Tenant Workspace | subscription | 2 | 21 | yes |
| `CMS-002` | Brand Kit | white-label | 2 | 4 | yes |
| `CMS-003` | Typography | white-label | 2 | 41 | yes |
| `CMS-004` | Logo & Assets | maintenance | 2 | 7 | yes |
| `CMS-005` | Theme Editor | white-label | 2 | 2 | yes |
| `CMS-006` | Component Preview | white-label | 2 | 41 | yes |
| `CMS-007` | Page Builder | white-label | 2 | 2 | yes |
| `CMS-008` | Content Blocks | white-label | 2 | 2 | yes |
| `CMS-009` | Navigation & Menus | fnb | 2 | 5 | yes |
| `CMS-010` | Media Library | assets | 2 | 12 | yes |
| `CMS-011` | Translations | white-label | 2 | 1 | yes |
| `CMS-012` | RTL Preview | white-label | 2 | 2 | yes |
| `CMS-013` | SEO & Metadata | White Label | 2 | 0 | yes |
| `CMS-014` | Publishing Workflow | white-label | 2 | 3 | yes |
| `CMS-015` | Version History | white-label | 2 | 3 | yes |
| `CMS-016` | Site Settings | white-label | 2 | 1 | yes |
| `CMS-017` | Domain & Certificate | White Label | 2 | 0 | yes |
| `CMS-018` | Consent & Legal | marketing-crm | 2 | 11 | yes |
| `CMS-019` | User Access | identity | 2 | 2 | yes |
| `CMS-020` | Change Log | white-label | 2 | 1 | yes |

