# Package report

**Generated 2026-10-04 by `tools/build-package-report.py`.** Every figure is read from a file another tool wrote in the same refresh.

## Scale

| | |
|---|---|
| Contracts | 33 |
| Operations | 2758 |
| Screens | 2450 |
| Platforms | 16 |
| Apps | 5 |
| Tables | 1115 |
| Stores | 10 |
| Foreign Keys | 806 |
| Indexes | 2882 |
| Relationships | 3089 |
| Flows | 97 |
| Boards | 218 |
| Adrs | 70 |
| Services | 17 |

## The chain

**A screen is buildable when the whole chain under it resolves.** Each link is counted separately, because they fail separately.

| Link | | | |
|---|---:|---:|---|
| Requirements in scope | 3165 / 3184 | 99% | matrix rows, less the ones deliberately parked |
| Requirements contracted | 3153 / 3165 | 100% | an operation or schema field demonstrably serves it |
| Operations declaring a service | 2758 / 2758 | 100% | the operation is owned by one of the seventeen deployables |
| Operations declaring a permission | 2595 / 2758 | 94% | the checklist a grant screen renders is built from these |
| Operations with resolved lineage | 2723 / 2758 | 99% | names the tables it reads and writes -- the join the DDL cannot make itself |
| Operations reaching a screen | 2520 / 2758 | 91% | sync, webhook and job operations legitimately have none |
| Screens naming an operation | 2385 / 2450 | 97% | the rest are static, navigation shells or workshop-blocked |
| Tables reached by an operation | 1111 / 1115 | 100% | a table nothing reaches is a missing operation or a table that should not exist |
| Tables carrying a relationship | 1025 / 1115 | 92% | either end of a declared reference |

## What crosses a service boundary

**3089 declared references. 1854 stay inside one service; 1235 cross two.**

**623 of the 1235 crossings land on three tables** -- `identity.principal`, `platform.scope`, `pii.subject`. The crossings concentrate on the foundation tier rather than spreading, which is what the tier is for.

| From | To | Edges |
|---|---|---:|
| MarketingService | IdentityService | 78 |
| AccessService | TenancyService | 76 |
| CatalogueService | TenancyService | 67 |
| OrderService | IdentityService | 59 |
| TenancyService | IdentityService | 50 |
| CatalogueService | IdentityService | 47 |
| AiService | IdentityService | 46 |
| AccessService | IdentityService | 37 |
| VenueOpsService | TenancyService | 35 |
| PlatformService | IdentityService | 32 |
| OrderService | CatalogueService | 30 |
| VenueOpsService | IdentityService | 29 |

| Most-referenced table across a boundary | Edges |
|---|---:|
| `identity.principal` | 347 |
| `platform.scope` | 183 |
| `pii.subject` | 93 |
| `platform.outbox` | 49 |
| `orders.sales_order` | 39 |
| `approvals.request` | 37 |
| `catalogue.product` | 32 |
| `platform.outlet` | 29 |
| `catalogue.performance` | 19 |
| `assets.media_asset` | 17 |

## Services

| Service | Tier | Ops | On a screen | Tables | Screens | Out | In |
|---|---|---:|---:|---:|---:|---:|---:|
| CatalogueService | commerce | 446 | 420 | 137 | 73 | 160 | 118 |
| OrderService | commerce | 298 | 281 | 115 | 101 | 148 | 93 |
| VenueOpsService | operations | 290 | 276 | 124 | 53 | 105 | 43 |
| MarketingService | engagement | 275 | 233 | 132 | 40 | 155 | 15 |
| AccessService | commerce | 256 | 246 | 77 | 29 | 140 | 20 |
| PlatformService | platform | 225 | 201 | 108 | 42 | 86 | 36 |
| TenancyService | foundation | 210 | 185 | 109 | 71 | 115 | 363 |
| AiService | engagement | 144 | 131 | 75 | 21 | 69 | 4 |
| FnbService | operations | 135 | 127 | 52 | 57 | 61 | 6 |
| IdentityService | foundation | 94 | 79 | 38 | 36 | 25 | 454 |
| WhiteLabelService | platform | 93 | 91 | 27 | 25 | 13 | 5 |
| LedgerService | commerce | 72 | 62 | 27 | 20 | 58 | 38 |
| WalletService | commerce | 68 | 60 | 31 | None | 17 | 8 |
| InventoryService | operations | 58 | 55 | 22 | 28 | 36 | 22 |
| ReportingService | platform | 51 | 49 | 25 | 31 | 16 | 3 |
| RetailService | operations | 25 | 22 | 13 | 19 | 24 | 5 |
| CrossRegionService | platform | 18 | 2 | 3 | 4 | 7 | 2 |

## Contracts

| Contract | Ops | On a screen | With lineage | With a permission |
|---|---:|---:|---:|---:|
| access | 256 | 246 | 247 | 250 |
| accreditation | 47 | 47 | 47 | 47 |
| ai | 144 | 131 | 143 | 140 |
| approvals | 57 | 46 | 56 | 57 |
| assets | 26 | 26 | 26 | 26 |
| catalogue | 248 | 231 | 244 | 242 |
| cross-region | 18 | 2 | 18 | 9 |
| finance | 72 | 62 | 72 | 70 |
| fnb | 135 | 127 | 133 | 122 |
| games | 40 | 35 | 40 | 36 |
| identity | 94 | 79 | 92 | 63 |
| inventory | 58 | 55 | 58 | 58 |
| maintenance | 44 | 44 | 44 | 44 |
| marketing-crm | 275 | 233 | 274 | 246 |
| orders | 222 | 208 | 219 | 206 |
| payments | 49 | 48 | 49 | 46 |
| platform-ops | 40 | 39 | 40 | 40 |
| promotions | 143 | 134 | 143 | 143 |
| public-api | 35 | 34 | 34 | 35 |
| queue | 22 | 16 | 22 | 14 |
| rental | 43 | 40 | 43 | 43 |
| reporting | 51 | 49 | 50 | 51 |
| resources | 61 | 61 | 61 | 61 |
| retail | 25 | 22 | 25 | 25 |
| seating | 55 | 55 | 55 | 55 |
| shift | 27 | 25 | 27 | 27 |
| subscription | 150 | 128 | 150 | 148 |
| tenancy | 57 | 46 | 57 | 54 |
| transport | 32 | 32 | 32 | 19 |
| venue-map | 22 | 22 | 21 | 17 |
| wallet | 68 | 60 | 66 | 68 |
| white-label | 93 | 91 | 86 | 84 |
| workforce | 49 | 46 | 49 | 49 |

## Platforms

| Code | Platform | App | Screens | Naming an operation | Distinct operations |
|---|---|---|---:|---:|---:|
| P01 | Guest Web | guest-web | 50 | 50 | 214 |
| P02 | Guest App | guest-app | 77 | 77 | 218 |
| P04 | Venue POS | venue-pos | 32 | 32 | 152 |
| P05 | Guest Kiosk | guest-app | 17 | 17 | 22 |
| P06 | Venue Staff App | venue-staff-app | 96 | 94 | 220 |
| P07 | Venue Scanner | venue-scanner | 11 | 11 | 24 |
| P08 | Venue Management | venue-management-web | 1661 | 1607 | 1860 |
| P09 | TICVAI Web | ticvai-web | 211 | 205 | 270 |
| P10 | Partner Web | partner-web | 43 | 43 | 118 |
| P11 | Accreditation Web | accreditation-web | 8 | 7 | 17 |
| P12 | Venue Support | venue-support-web | 28 | 28 | 67 |
| P13 | Venue CMS | venue-management-web | 103 | 103 | 194 |
| P14 | Developer | developer-portal-web | 8 | 8 | 32 |
| P15 | Kitchen Display | kitchen-display | 10 | 10 | 26 |
| P16 | Venue Analytics | venue-management-web | 71 | 71 | 94 |
| P17 | TICVAI Sign-up | signup-web | 24 | 22 | 12 |

## Open

| | |
|---|---:|
| Conflicts Open | 8 |
| Conflicts Blocking | 0 |
| Requirements Gap Contract | 0 |
| Requirements Gap Decision | 0 |
| Requirements Partial | 12 |
| Operations No Screen | 238 |
| Screens No Operation | 65 |
| Operations No Lineage | 35 |
| Tables Not Reached | 4 |
| Permissions Without Label | 70 |
| Capability Pairs | 282 |
| Modules With Capabilities | 33 |

