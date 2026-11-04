# Package report

**Generated 2026-11-04 by `tools/build-package-report.py`.** Every figure is read from a file another tool wrote in the same refresh.

## Scale

| | |
|---|---|
| Contracts | 33 |
| Operations | 2873 |
| Screens | 2453 |
| Platforms | 16 |
| Apps | 6 |
| Tables | 1178 |
| Stores | 10 |
| Foreign Keys | 815 |
| Indexes | 2924 |
| Relationships | 3371 |
| Flows | 98 |
| Boards | 219 |
| Adrs | 72 |
| Services | 17 |

## The chain

**A screen is buildable when the whole chain under it resolves.** Each link is counted separately, because they fail separately.

| Link | | | |
|---|---:|---:|---|
| Requirements in scope | 3165 / 3184 | 99% | matrix rows, less the ones deliberately parked |
| Requirements contracted | 3154 / 3165 | 100% | an operation or schema field demonstrably serves it |
| Operations declaring a service | 2873 / 2873 | 100% | the operation is owned by one of the seventeen deployables |
| Operations declaring a permission | 2670 / 2873 | 93% | the checklist a grant screen renders is built from these |
| Operations with resolved lineage | 2838 / 2873 | 99% | names the tables it reads and writes -- the join the DDL cannot make itself |
| Operations reaching a screen | 2583 / 2873 | 90% | sync, webhook and job operations legitimately have none |
| Screens naming an operation | 2386 / 2453 | 97% | the rest are static, navigation shells or workshop-blocked |
| Tables reached by an operation | 1161 / 1178 | 99% | a table nothing reaches is a missing operation or a table that should not exist |
| Tables carrying a relationship | 1077 / 1178 | 91% | either end of a declared reference |

## What crosses a service boundary

**3371 declared references. 2084 stay inside one service; 1287 cross two.**

**671 of the 1287 crossings land on three tables** -- `identity.principal`, `platform.scope`, `pii.subject`. The crossings concentrate on the foundation tier rather than spreading, which is what the tier is for.

| From | To | Edges |
|---|---|---:|
| AccessService | TenancyService | 87 |
| MarketingService | IdentityService | 83 |
| OrderService | IdentityService | 68 |
| CatalogueService | TenancyService | 68 |
| TenancyService | IdentityService | 63 |
| CatalogueService | IdentityService | 51 |
| AiService | IdentityService | 49 |
| VenueOpsService | IdentityService | 40 |
| VenueOpsService | TenancyService | 38 |
| OrderService | TenancyService | 37 |
| AccessService | IdentityService | 37 |
| FnbService | TenancyService | 30 |

| Most-referenced table across a boundary | Edges |
|---|---:|
| `identity.principal` | 361 |
| `platform.scope` | 190 |
| `pii.subject` | 120 |
| `platform.outbox` | 68 |
| `approvals.request` | 41 |
| `platform.outlet` | 29 |
| `orders.sales_order` | 27 |
| `catalogue.product` | 22 |
| `assets.media_asset` | 21 |
| `catalogue.performance` | 19 |

## Services

| Service | Tier | Ops | On a screen | Tables | Screens | Out | In |
|---|---|---:|---:|---:|---:|---:|---:|
| CatalogueService | commerce | 475 | 437 | 145 | 73 | 162 | 110 |
| OrderService | commerce | 305 | 286 | 116 | 101 | 164 | 80 |
| VenueOpsService | operations | 299 | 278 | 128 | 53 | 122 | 42 |
| MarketingService | engagement | 285 | 235 | 134 | 40 | 155 | 13 |
| AccessService | commerce | 259 | 248 | 77 | 29 | 146 | 18 |
| PlatformService | platform | 235 | 205 | 119 | 42 | 57 | 36 |
| TenancyService | foundation | 214 | 190 | 110 | 71 | 138 | 383 |
| AiService | engagement | 146 | 131 | 79 | 21 | 65 | 3 |
| FnbService | operations | 138 | 130 | 54 | 57 | 67 | 4 |
| WhiteLabelService | platform | 110 | 107 | 37 | 25 | 19 | 15 |
| IdentityService | foundation | 108 | 81 | 52 | 36 | 28 | 497 |
| LedgerService | commerce | 72 | 62 | 27 | 20 | 48 | 42 |
| WalletService | commerce | 72 | 64 | 32 | None | 18 | 6 |
| InventoryService | operations | 59 | 56 | 23 | 28 | 41 | 22 |
| ReportingService | platform | 51 | 49 | 25 | 31 | 16 | 0 |
| RetailService | operations | 25 | 22 | 13 | 19 | 27 | 11 |
| CrossRegionService | platform | 20 | 2 | 7 | 4 | 14 | 5 |

## Contracts

| Contract | Ops | On a screen | With lineage | With a permission |
|---|---:|---:|---:|---:|
| access | 259 | 248 | 256 | 252 |
| accreditation | 48 | 48 | 48 | 48 |
| ai | 146 | 131 | 146 | 140 |
| approvals | 59 | 47 | 58 | 58 |
| assets | 28 | 26 | 28 | 26 |
| catalogue | 274 | 245 | 261 | 268 |
| cross-region | 20 | 2 | 20 | 9 |
| finance | 72 | 62 | 72 | 70 |
| fnb | 138 | 130 | 137 | 125 |
| games | 40 | 35 | 40 | 37 |
| identity | 108 | 81 | 107 | 64 |
| inventory | 59 | 56 | 59 | 59 |
| maintenance | 44 | 44 | 44 | 44 |
| marketing-crm | 285 | 235 | 284 | 252 |
| orders | 228 | 212 | 226 | 206 |
| payments | 49 | 48 | 49 | 46 |
| platform-ops | 40 | 39 | 40 | 40 |
| promotions | 145 | 136 | 144 | 143 |
| public-api | 38 | 35 | 37 | 34 |
| queue | 23 | 16 | 23 | 15 |
| rental | 43 | 40 | 43 | 43 |
| reporting | 51 | 49 | 50 | 51 |
| resources | 62 | 62 | 62 | 62 |
| retail | 25 | 22 | 25 | 25 |
| seating | 56 | 56 | 56 | 56 |
| shift | 28 | 26 | 28 | 28 |
| subscription | 157 | 131 | 157 | 154 |
| tenancy | 57 | 48 | 57 | 53 |
| transport | 32 | 32 | 32 | 19 |
| venue-map | 27 | 23 | 26 | 21 |
| wallet | 72 | 64 | 70 | 72 |
| white-label | 110 | 107 | 103 | 100 |
| workforce | 50 | 47 | 50 | 50 |

## Platforms

| Code | Platform | App | Screens | Naming an operation | Distinct operations |
|---|---|---|---:|---:|---:|
| P01 | Guest Web | guest-web | 50 | 50 | 208 |
| P02 | Guest App | guest-app | 77 | 77 | 217 |
| P04 | Venue POS | venue-pos | 32 | 32 | 158 |
| P05 | Guest Kiosk | guest-app | 17 | 17 | 22 |
| P06 | Venue Staff App | venue-staff-app | 96 | 94 | 221 |
| P07 | Venue Scanner | venue-scanner | 11 | 11 | 24 |
| P08 | Venue Management | venue-management-web | 1663 | 1606 | 1903 |
| P09 | TICVAI Web | ticvai-web | 211 | 208 | 267 |
| P10 | Partner Web | partner-web | 43 | 43 | 118 |
| P11 | Accreditation Web | accreditation-web | 8 | 7 | 15 |
| P12 | Venue Support | venue-support-web | 28 | 28 | 66 |
| P13 | Venue CMS | venue-management-web | 104 | 104 | 214 |
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
| Requirements Partial | 11 |
| Operations No Screen | 290 |
| Screens No Operation | 67 |
| Operations No Lineage | 35 |
| Tables Not Reached | 17 |
| Permissions Without Label | 70 |
| Capability Pairs | 290 |
| Modules With Capabilities | 33 |

