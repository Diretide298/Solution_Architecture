# Package report

**Generated 2026-10-21 by `tools/build-package-report.py`.** Every figure is read from a file another tool wrote in the same refresh.

## Scale

| | |
|---|---|
| Contracts | 33 |
| Operations | 2845 |
| Screens | 2453 |
| Platforms | 16 |
| Apps | 5 |
| Tables | 1149 |
| Stores | 10 |
| Foreign Keys | 815 |
| Indexes | 2924 |
| Relationships | 3250 |
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
| Operations declaring a service | 2845 / 2845 | 100% | the operation is owned by one of the seventeen deployables |
| Operations declaring a permission | 2655 / 2845 | 93% | the checklist a grant screen renders is built from these |
| Operations with resolved lineage | 2810 / 2845 | 99% | names the tables it reads and writes -- the join the DDL cannot make itself |
| Operations reaching a screen | 2570 / 2845 | 90% | sync, webhook and job operations legitimately have none |
| Screens naming an operation | 2390 / 2453 | 97% | the rest are static, navigation shells or workshop-blocked |
| Tables reached by an operation | 1138 / 1149 | 99% | a table nothing reaches is a missing operation or a table that should not exist |
| Tables carrying a relationship | 1056 / 1149 | 92% | either end of a declared reference |

## What crosses a service boundary

**3250 declared references. 2007 stay inside one service; 1243 cross two.**

**652 of the 1243 crossings land on three tables** -- `identity.principal`, `platform.scope`, `pii.subject`. The crossings concentrate on the foundation tier rather than spreading, which is what the tier is for.

| From | To | Edges |
|---|---|---:|
| AccessService | TenancyService | 86 |
| MarketingService | IdentityService | 77 |
| CatalogueService | TenancyService | 69 |
| OrderService | IdentityService | 64 |
| TenancyService | IdentityService | 55 |
| CatalogueService | IdentityService | 49 |
| AiService | IdentityService | 48 |
| OrderService | TenancyService | 36 |
| VenueOpsService | TenancyService | 36 |
| AccessService | IdentityService | 36 |
| VenueOpsService | IdentityService | 34 |
| PlatformService | IdentityService | 31 |

| Most-referenced table across a boundary | Edges |
|---|---:|
| `identity.principal` | 363 |
| `platform.scope` | 190 |
| `pii.subject` | 99 |
| `platform.outbox` | 61 |
| `approvals.request` | 38 |
| `platform.outlet` | 29 |
| `orders.sales_order` | 27 |
| `assets.media_asset` | 21 |
| `catalogue.product` | 20 |
| `catalogue.performance` | 19 |

## Services

| Service | Tier | Ops | On a screen | Tables | Screens | Out | In |
|---|---|---:|---:|---:|---:|---:|---:|
| CatalogueService | commerce | 470 | 429 | 143 | 73 | 161 | 106 |
| OrderService | commerce | 304 | 286 | 114 | 101 | 157 | 80 |
| VenueOpsService | operations | 297 | 279 | 127 | 53 | 114 | 39 |
| MarketingService | engagement | 280 | 233 | 132 | 40 | 148 | 15 |
| AccessService | commerce | 258 | 248 | 77 | 29 | 144 | 18 |
| PlatformService | platform | 229 | 205 | 113 | 42 | 69 | 36 |
| TenancyService | foundation | 214 | 189 | 105 | 71 | 116 | 375 |
| AiService | engagement | 146 | 131 | 79 | 21 | 63 | 3 |
| FnbService | operations | 138 | 130 | 53 | 57 | 62 | 4 |
| WhiteLabelService | platform | 110 | 107 | 35 | 25 | 19 | 7 |
| IdentityService | foundation | 101 | 79 | 44 | 36 | 27 | 476 |
| LedgerService | commerce | 72 | 62 | 27 | 20 | 48 | 42 |
| WalletService | commerce | 71 | 63 | 32 | None | 18 | 6 |
| InventoryService | operations | 59 | 56 | 23 | 28 | 40 | 22 |
| ReportingService | platform | 51 | 49 | 25 | 31 | 16 | 0 |
| RetailService | operations | 25 | 22 | 13 | 19 | 27 | 9 |
| CrossRegionService | platform | 20 | 2 | 7 | 4 | 14 | 5 |

## Contracts

| Contract | Ops | On a screen | With lineage | With a permission |
|---|---:|---:|---:|---:|
| access | 258 | 248 | 255 | 252 |
| accreditation | 48 | 48 | 48 | 48 |
| ai | 146 | 131 | 146 | 140 |
| approvals | 59 | 47 | 58 | 58 |
| assets | 28 | 26 | 28 | 26 |
| catalogue | 269 | 238 | 259 | 263 |
| cross-region | 20 | 2 | 20 | 9 |
| finance | 72 | 62 | 72 | 70 |
| fnb | 138 | 130 | 137 | 125 |
| games | 40 | 35 | 40 | 37 |
| identity | 101 | 79 | 100 | 62 |
| inventory | 59 | 56 | 59 | 59 |
| maintenance | 44 | 44 | 44 | 44 |
| marketing-crm | 280 | 233 | 279 | 250 |
| orders | 227 | 212 | 223 | 206 |
| payments | 49 | 48 | 49 | 46 |
| platform-ops | 40 | 39 | 40 | 40 |
| promotions | 145 | 135 | 144 | 143 |
| public-api | 36 | 35 | 35 | 34 |
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
| venue-map | 26 | 24 | 25 | 20 |
| wallet | 71 | 63 | 69 | 71 |
| white-label | 110 | 107 | 103 | 100 |
| workforce | 49 | 46 | 49 | 49 |

## Platforms

| Code | Platform | App | Screens | Naming an operation | Distinct operations |
|---|---|---|---:|---:|---:|
| P01 | Guest Web | guest-web | 50 | 50 | 204 |
| P02 | Guest App | guest-app | 77 | 77 | 217 |
| P04 | Venue POS | venue-pos | 32 | 32 | 157 |
| P05 | Guest Kiosk | guest-app | 17 | 17 | 22 |
| P06 | Venue Staff App | venue-staff-app | 96 | 94 | 221 |
| P07 | Venue Scanner | venue-scanner | 11 | 11 | 24 |
| P08 | Venue Management | venue-management-web | 1663 | 1610 | 1895 |
| P09 | TICVAI Web | ticvai-web | 211 | 208 | 267 |
| P10 | Partner Web | partner-web | 43 | 43 | 118 |
| P11 | Accreditation Web | accreditation-web | 8 | 7 | 15 |
| P12 | Venue Support | venue-support-web | 28 | 28 | 66 |
| P13 | Venue CMS | venue-management-web | 104 | 104 | 210 |
| P14 | Developer | developer-portal-web | 8 | 8 | 32 |
| P15 | Kitchen Display | kitchen-display | 10 | 10 | 27 |
| P16 | Venue Analytics | venue-management-web | 71 | 71 | 84 |
| P17 | TICVAI Sign-up | signup-web | 24 | 20 | 11 |

## Open

| | |
|---|---:|
| Conflicts Open | 8 |
| Conflicts Blocking | 0 |
| Requirements Gap Contract | 0 |
| Requirements Gap Decision | 0 |
| Requirements Partial | 12 |
| Operations No Screen | 275 |
| Screens No Operation | 63 |
| Operations No Lineage | 35 |
| Tables Not Reached | 11 |
| Permissions Without Label | 70 |
| Capability Pairs | 291 |
| Modules With Capabilities | 33 |

