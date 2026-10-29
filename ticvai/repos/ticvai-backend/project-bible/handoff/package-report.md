# Package report

**Generated 2026-10-29 by `tools/build-package-report.py`.** Every figure is read from a file another tool wrote in the same refresh.

## Scale

| | |
|---|---|
| Contracts | 33 |
| Operations | 2857 |
| Screens | 2453 |
| Platforms | 16 |
| Apps | 6 |
| Tables | 1167 |
| Stores | 10 |
| Foreign Keys | 815 |
| Indexes | 2924 |
| Relationships | 3309 |
| Flows | 98 |
| Boards | 219 |
| Adrs | 72 |
| Services | 17 |

## The chain

**A screen is buildable when the whole chain under it resolves.** Each link is counted separately, because they fail separately.

| Link | | | |
|---|---:|---:|---|
| Requirements in scope | 3165 / 3184 | 99% | matrix rows, less the ones deliberately parked |
| Requirements contracted | 3153 / 3165 | 100% | an operation or schema field demonstrably serves it |
| Operations declaring a service | 2857 / 2857 | 100% | the operation is owned by one of the seventeen deployables |
| Operations declaring a permission | 2661 / 2857 | 93% | the checklist a grant screen renders is built from these |
| Operations with resolved lineage | 2826 / 2857 | 99% | names the tables it reads and writes -- the join the DDL cannot make itself |
| Operations reaching a screen | 2570 / 2857 | 90% | sync, webhook and job operations legitimately have none |
| Screens naming an operation | 2386 / 2453 | 97% | the rest are static, navigation shells or workshop-blocked |
| Tables reached by an operation | 1151 / 1167 | 99% | a table nothing reaches is a missing operation or a table that should not exist |
| Tables carrying a relationship | 1070 / 1167 | 92% | either end of a declared reference |

## What crosses a service boundary

**3309 declared references. 2049 stay inside one service; 1260 cross two.**

**653 of the 1260 crossings land on three tables** -- `identity.principal`, `platform.scope`, `pii.subject`. The crossings concentrate on the foundation tier rather than spreading, which is what the tier is for.

| From | To | Edges |
|---|---|---:|
| AccessService | TenancyService | 86 |
| MarketingService | IdentityService | 77 |
| CatalogueService | TenancyService | 69 |
| OrderService | IdentityService | 63 |
| TenancyService | IdentityService | 59 |
| CatalogueService | IdentityService | 49 |
| AiService | IdentityService | 48 |
| VenueOpsService | TenancyService | 37 |
| OrderService | TenancyService | 36 |
| AccessService | IdentityService | 36 |
| VenueOpsService | IdentityService | 34 |
| PlatformService | IdentityService | 31 |

| Most-referenced table across a boundary | Edges |
|---|---:|
| `identity.principal` | 364 |
| `platform.scope` | 190 |
| `pii.subject` | 99 |
| `platform.outbox` | 62 |
| `approvals.request` | 39 |
| `platform.outlet` | 29 |
| `orders.sales_order` | 27 |
| `assets.media_asset` | 21 |
| `catalogue.product` | 20 |
| `catalogue.performance` | 19 |

## Services

| Service | Tier | Ops | On a screen | Tables | Screens | Out | In |
|---|---|---:|---:|---:|---:|---:|---:|
| CatalogueService | commerce | 470 | 429 | 143 | 73 | 161 | 106 |
| OrderService | commerce | 305 | 286 | 116 | 101 | 156 | 80 |
| VenueOpsService | operations | 299 | 278 | 128 | 53 | 115 | 42 |
| MarketingService | engagement | 281 | 233 | 133 | 40 | 149 | 15 |
| AccessService | commerce | 259 | 248 | 77 | 29 | 144 | 18 |
| PlatformService | platform | 234 | 205 | 119 | 42 | 69 | 36 |
| TenancyService | foundation | 214 | 189 | 107 | 71 | 130 | 377 |
| AiService | engagement | 146 | 131 | 79 | 21 | 64 | 4 |
| FnbService | operations | 138 | 130 | 53 | 57 | 62 | 4 |
| WhiteLabelService | platform | 110 | 107 | 37 | 25 | 20 | 15 |
| IdentityService | foundation | 103 | 80 | 48 | 36 | 27 | 479 |
| LedgerService | commerce | 72 | 62 | 27 | 20 | 48 | 42 |
| WalletService | commerce | 71 | 63 | 32 | None | 18 | 6 |
| InventoryService | operations | 59 | 56 | 23 | 28 | 40 | 22 |
| ReportingService | platform | 51 | 49 | 25 | 31 | 16 | 0 |
| RetailService | operations | 25 | 22 | 13 | 19 | 27 | 9 |
| CrossRegionService | platform | 20 | 2 | 7 | 4 | 14 | 5 |

## Contracts

| Contract | Ops | On a screen | With lineage | With a permission |
|---|---:|---:|---:|---:|
| access | 259 | 248 | 256 | 252 |
| accreditation | 48 | 48 | 48 | 48 |
| ai | 146 | 131 | 146 | 140 |
| approvals | 59 | 47 | 58 | 58 |
| assets | 28 | 26 | 28 | 26 |
| catalogue | 269 | 238 | 260 | 263 |
| cross-region | 20 | 2 | 20 | 9 |
| finance | 72 | 62 | 72 | 70 |
| fnb | 138 | 130 | 137 | 125 |
| games | 40 | 35 | 40 | 37 |
| identity | 103 | 80 | 102 | 63 |
| inventory | 59 | 56 | 59 | 59 |
| maintenance | 44 | 44 | 44 | 44 |
| marketing-crm | 281 | 233 | 280 | 250 |
| orders | 228 | 212 | 226 | 206 |
| payments | 49 | 48 | 49 | 46 |
| platform-ops | 40 | 39 | 40 | 40 |
| promotions | 145 | 135 | 144 | 143 |
| public-api | 38 | 35 | 37 | 34 |
| queue | 23 | 16 | 23 | 15 |
| rental | 43 | 40 | 43 | 43 |
| reporting | 51 | 49 | 50 | 51 |
| resources | 62 | 62 | 62 | 62 |
| retail | 25 | 22 | 25 | 25 |
| seating | 56 | 56 | 56 | 56 |
| shift | 28 | 26 | 28 | 28 |
| subscription | 156 | 131 | 156 | 154 |
| tenancy | 58 | 48 | 58 | 54 |
| transport | 32 | 32 | 32 | 19 |
| venue-map | 27 | 23 | 26 | 21 |
| wallet | 71 | 63 | 69 | 71 |
| white-label | 110 | 107 | 103 | 100 |
| workforce | 49 | 46 | 49 | 49 |

## Platforms

| Code | Platform | App | Screens | Naming an operation | Distinct operations |
|---|---|---|---:|---:|---:|
| P01 | Guest Web | guest-web | 50 | 50 | 206 |
| P02 | Guest App | guest-app | 77 | 77 | 217 |
| P04 | Venue POS | venue-pos | 32 | 32 | 158 |
| P05 | Guest Kiosk | guest-app | 17 | 17 | 22 |
| P06 | Venue Staff App | venue-staff-app | 96 | 94 | 221 |
| P07 | Venue Scanner | venue-scanner | 11 | 11 | 24 |
| P08 | Venue Management | venue-management-web | 1663 | 1606 | 1892 |
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
| Operations No Screen | 287 |
| Screens No Operation | 67 |
| Operations No Lineage | 31 |
| Tables Not Reached | 16 |
| Permissions Without Label | 70 |
| Capability Pairs | 291 |
| Modules With Capabilities | 33 |

