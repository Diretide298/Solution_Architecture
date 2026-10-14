# Package report

**Generated 2026-10-14 by `tools/build-package-report.py`.** Every figure is read from a file another tool wrote in the same refresh.

## Scale

| | |
|---|---|
| Contracts | 33 |
| Operations | 2804 |
| Screens | 2453 |
| Platforms | 16 |
| Apps | 5 |
| Tables | 1129 |
| Stores | 10 |
| Foreign Keys | 815 |
| Indexes | 2924 |
| Relationships | 3196 |
| Flows | 98 |
| Boards | 218 |
| Adrs | 71 |
| Services | 17 |

## The chain

**A screen is buildable when the whole chain under it resolves.** Each link is counted separately, because they fail separately.

| Link | | | |
|---|---:|---:|---|
| Requirements in scope | 3165 / 3184 | 99% | matrix rows, less the ones deliberately parked |
| Requirements contracted | 3153 / 3165 | 100% | an operation or schema field demonstrably serves it |
| Operations declaring a service | 2804 / 2804 | 100% | the operation is owned by one of the seventeen deployables |
| Operations declaring a permission | 2633 / 2804 | 94% | the checklist a grant screen renders is built from these |
| Operations with resolved lineage | 2776 / 2804 | 99% | names the tables it reads and writes -- the join the DDL cannot make itself |
| Operations reaching a screen | 2559 / 2804 | 91% | sync, webhook and job operations legitimately have none |
| Screens naming an operation | 2392 / 2453 | 98% | the rest are static, navigation shells or workshop-blocked |
| Tables reached by an operation | 1124 / 1129 | 100% | a table nothing reaches is a missing operation or a table that should not exist |
| Tables carrying a relationship | 1041 / 1129 | 92% | either end of a declared reference |

## What crosses a service boundary

**3196 declared references. 1966 stay inside one service; 1230 cross two.**

**637 of the 1230 crossings land on three tables** -- `identity.principal`, `platform.scope`, `pii.subject`. The crossings concentrate on the foundation tier rather than spreading, which is what the tier is for.

| From | To | Edges |
|---|---|---:|
| AccessService | TenancyService | 86 |
| MarketingService | IdentityService | 77 |
| CatalogueService | TenancyService | 67 |
| OrderService | IdentityService | 59 |
| TenancyService | IdentityService | 55 |
| CatalogueService | IdentityService | 48 |
| AiService | IdentityService | 46 |
| VenueOpsService | TenancyService | 36 |
| AccessService | IdentityService | 35 |
| VenueOpsService | IdentityService | 33 |
| OrderService | TenancyService | 32 |
| PlatformService | IdentityService | 31 |

| Most-referenced table across a boundary | Edges |
|---|---:|
| `identity.principal` | 352 |
| `platform.scope` | 187 |
| `pii.subject` | 98 |
| `platform.outbox` | 64 |
| `approvals.request` | 38 |
| `platform.outlet` | 29 |
| `orders.sales_order` | 27 |
| `assets.media_asset` | 21 |
| `catalogue.product` | 20 |
| `catalogue.variant` | 18 |

## Services

| Service | Tier | Ops | On a screen | Tables | Screens | Out | In |
|---|---|---:|---:|---:|---:|---:|---:|
| CatalogueService | commerce | 451 | 427 | 138 | 73 | 158 | 105 |
| OrderService | commerce | 299 | 282 | 114 | 101 | 147 | 82 |
| VenueOpsService | operations | 291 | 277 | 125 | 53 | 113 | 39 |
| MarketingService | engagement | 278 | 232 | 131 | 40 | 149 | 15 |
| AccessService | commerce | 258 | 248 | 77 | 29 | 143 | 18 |
| PlatformService | platform | 229 | 205 | 109 | 42 | 75 | 36 |
| TenancyService | foundation | 213 | 189 | 105 | 71 | 113 | 376 |
| AiService | engagement | 144 | 131 | 75 | 21 | 61 | 3 |
| FnbService | operations | 138 | 130 | 53 | 57 | 62 | 4 |
| WhiteLabelService | platform | 108 | 106 | 34 | 25 | 17 | 5 |
| IdentityService | foundation | 98 | 79 | 41 | 36 | 27 | 463 |
| LedgerService | commerce | 72 | 62 | 27 | 20 | 54 | 42 |
| WalletService | commerce | 70 | 62 | 32 | None | 17 | 6 |
| InventoryService | operations | 59 | 56 | 23 | 28 | 40 | 22 |
| ReportingService | platform | 51 | 49 | 25 | 31 | 16 | 0 |
| RetailService | operations | 25 | 22 | 13 | 19 | 24 | 9 |
| CrossRegionService | platform | 20 | 2 | 7 | 4 | 14 | 5 |

## Contracts

| Contract | Ops | On a screen | With lineage | With a permission |
|---|---:|---:|---:|---:|
| access | 258 | 248 | 255 | 252 |
| accreditation | 48 | 48 | 48 | 48 |
| ai | 144 | 131 | 144 | 140 |
| approvals | 58 | 47 | 57 | 58 |
| assets | 26 | 26 | 26 | 26 |
| catalogue | 252 | 237 | 249 | 246 |
| cross-region | 20 | 2 | 20 | 9 |
| finance | 72 | 62 | 72 | 70 |
| fnb | 138 | 130 | 136 | 125 |
| games | 40 | 35 | 40 | 36 |
| identity | 98 | 79 | 96 | 63 |
| inventory | 59 | 56 | 59 | 59 |
| maintenance | 44 | 44 | 44 | 44 |
| marketing-crm | 278 | 232 | 277 | 249 |
| orders | 222 | 208 | 219 | 206 |
| payments | 49 | 48 | 49 | 46 |
| platform-ops | 40 | 39 | 40 | 40 |
| promotions | 143 | 134 | 143 | 143 |
| public-api | 36 | 35 | 35 | 36 |
| queue | 22 | 16 | 22 | 14 |
| rental | 43 | 40 | 43 | 43 |
| reporting | 51 | 49 | 50 | 51 |
| resources | 62 | 62 | 62 | 62 |
| retail | 25 | 22 | 25 | 25 |
| seating | 56 | 56 | 56 | 56 |
| shift | 28 | 26 | 28 | 28 |
| subscription | 153 | 131 | 152 | 151 |
| tenancy | 58 | 48 | 58 | 54 |
| transport | 32 | 32 | 32 | 19 |
| venue-map | 22 | 22 | 21 | 17 |
| wallet | 70 | 62 | 68 | 70 |
| white-label | 108 | 106 | 101 | 98 |
| workforce | 49 | 46 | 49 | 49 |

## Platforms

| Code | Platform | App | Screens | Naming an operation | Distinct operations |
|---|---|---|---:|---:|---:|
| P01 | Guest Web | guest-web | 50 | 50 | 201 |
| P02 | Guest App | guest-app | 77 | 77 | 211 |
| P04 | Venue POS | venue-pos | 32 | 32 | 157 |
| P05 | Guest Kiosk | guest-app | 17 | 17 | 22 |
| P06 | Venue Staff App | venue-staff-app | 96 | 94 | 221 |
| P07 | Venue Scanner | venue-scanner | 11 | 11 | 24 |
| P08 | Venue Management | venue-management-web | 1663 | 1610 | 1892 |
| P09 | TICVAI Web | ticvai-web | 211 | 208 | 267 |
| P10 | Partner Web | partner-web | 43 | 43 | 118 |
| P11 | Accreditation Web | accreditation-web | 8 | 7 | 15 |
| P12 | Venue Support | venue-support-web | 28 | 28 | 66 |
| P13 | Venue CMS | venue-management-web | 104 | 104 | 209 |
| P14 | Developer | developer-portal-web | 8 | 8 | 32 |
| P15 | Kitchen Display | kitchen-display | 10 | 10 | 27 |
| P16 | Venue Analytics | venue-management-web | 71 | 71 | 84 |
| P17 | TICVAI Sign-up | signup-web | 24 | 22 | 12 |

## Open

| | |
|---|---:|
| Conflicts Open | 8 |
| Conflicts Blocking | 0 |
| Requirements Gap Contract | 0 |
| Requirements Gap Decision | 0 |
| Requirements Partial | 12 |
| Operations No Screen | 245 |
| Screens No Operation | 61 |
| Operations No Lineage | 28 |
| Tables Not Reached | 5 |
| Permissions Without Label | 70 |
| Capability Pairs | 287 |
| Modules With Capabilities | 33 |

