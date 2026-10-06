# Package report

**Generated 2026-10-06 by `tools/build-package-report.py`.** Every figure is read from a file another tool wrote in the same refresh.

## Scale

| | |
|---|---|
| Contracts | 33 |
| Operations | 2789 |
| Screens | 2451 |
| Platforms | 16 |
| Apps | 5 |
| Tables | 1129 |
| Stores | 10 |
| Foreign Keys | 815 |
| Indexes | 2924 |
| Relationships | 3191 |
| Flows | 98 |
| Boards | 218 |
| Adrs | 70 |
| Services | 17 |

## The chain

**A screen is buildable when the whole chain under it resolves.** Each link is counted separately, because they fail separately.

| Link | | | |
|---|---:|---:|---|
| Requirements in scope | 3165 / 3184 | 99% | matrix rows, less the ones deliberately parked |
| Requirements contracted | 3153 / 3165 | 100% | an operation or schema field demonstrably serves it |
| Operations declaring a service | 2789 / 2789 | 100% | the operation is owned by one of the seventeen deployables |
| Operations declaring a permission | 2625 / 2789 | 94% | the checklist a grant screen renders is built from these |
| Operations with resolved lineage | 2762 / 2789 | 99% | names the tables it reads and writes -- the join the DDL cannot make itself |
| Operations reaching a screen | 2551 / 2789 | 91% | sync, webhook and job operations legitimately have none |
| Screens naming an operation | 2387 / 2451 | 97% | the rest are static, navigation shells or workshop-blocked |
| Tables reached by an operation | 1124 / 1129 | 100% | a table nothing reaches is a missing operation or a table that should not exist |
| Tables carrying a relationship | 1040 / 1129 | 92% | either end of a declared reference |

## What crosses a service boundary

**3191 declared references. 1941 stay inside one service; 1250 cross two.**

**631 of the 1250 crossings land on three tables** -- `identity.principal`, `platform.scope`, `pii.subject`. The crossings concentrate on the foundation tier rather than spreading, which is what the tier is for.

| From | To | Edges |
|---|---|---:|
| MarketingService | IdentityService | 78 |
| AccessService | TenancyService | 76 |
| CatalogueService | TenancyService | 67 |
| OrderService | IdentityService | 59 |
| TenancyService | IdentityService | 52 |
| CatalogueService | IdentityService | 48 |
| AiService | IdentityService | 46 |
| AccessService | IdentityService | 37 |
| VenueOpsService | TenancyService | 35 |
| VenueOpsService | IdentityService | 32 |
| PlatformService | IdentityService | 31 |
| OrderService | CatalogueService | 30 |

| Most-referenced table across a boundary | Edges |
|---|---:|
| `identity.principal` | 352 |
| `platform.scope` | 185 |
| `pii.subject` | 94 |
| `platform.outbox` | 49 |
| `orders.sales_order` | 39 |
| `approvals.request` | 37 |
| `catalogue.product` | 33 |
| `platform.outlet` | 29 |
| `catalogue.performance` | 19 |
| `assets.media_asset` | 17 |

## Services

| Service | Tier | Ops | On a screen | Tables | Screens | Out | In |
|---|---|---:|---:|---:|---:|---:|---:|
| CatalogueService | commerce | 447 | 420 | 138 | 73 | 161 | 120 |
| OrderService | commerce | 298 | 281 | 115 | 101 | 149 | 93 |
| VenueOpsService | operations | 291 | 277 | 125 | 53 | 110 | 43 |
| MarketingService | engagement | 277 | 234 | 132 | 40 | 155 | 15 |
| AccessService | commerce | 257 | 247 | 77 | 29 | 141 | 20 |
| PlatformService | platform | 228 | 204 | 109 | 42 | 85 | 36 |
| TenancyService | foundation | 212 | 188 | 109 | 71 | 116 | 366 |
| AiService | engagement | 144 | 131 | 75 | 21 | 69 | 4 |
| FnbService | operations | 138 | 130 | 53 | 57 | 61 | 6 |
| WhiteLabelService | platform | 108 | 106 | 34 | 25 | 18 | 5 |
| IdentityService | foundation | 94 | 80 | 39 | 36 | 25 | 461 |
| LedgerService | commerce | 72 | 62 | 27 | 20 | 58 | 39 |
| WalletService | commerce | 70 | 62 | 32 | None | 17 | 8 |
| InventoryService | operations | 59 | 56 | 23 | 28 | 38 | 22 |
| ReportingService | platform | 51 | 49 | 25 | 31 | 16 | 3 |
| RetailService | operations | 25 | 22 | 13 | 19 | 24 | 7 |
| CrossRegionService | platform | 18 | 2 | 3 | 4 | 7 | 2 |

## Contracts

| Contract | Ops | On a screen | With lineage | With a permission |
|---|---:|---:|---:|---:|
| access | 257 | 247 | 254 | 251 |
| accreditation | 48 | 48 | 48 | 48 |
| ai | 144 | 131 | 144 | 140 |
| approvals | 58 | 47 | 57 | 58 |
| assets | 26 | 26 | 26 | 26 |
| catalogue | 249 | 231 | 246 | 243 |
| cross-region | 18 | 2 | 18 | 9 |
| finance | 72 | 62 | 72 | 70 |
| fnb | 138 | 130 | 136 | 125 |
| games | 40 | 35 | 40 | 36 |
| identity | 94 | 80 | 92 | 63 |
| inventory | 59 | 56 | 59 | 59 |
| maintenance | 44 | 44 | 44 | 44 |
| marketing-crm | 277 | 234 | 276 | 248 |
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
| seating | 55 | 55 | 55 | 55 |
| shift | 27 | 25 | 27 | 27 |
| subscription | 152 | 130 | 152 | 150 |
| tenancy | 57 | 47 | 57 | 54 |
| transport | 32 | 32 | 32 | 19 |
| venue-map | 22 | 22 | 21 | 17 |
| wallet | 70 | 62 | 68 | 70 |
| white-label | 108 | 106 | 101 | 98 |
| workforce | 49 | 46 | 49 | 49 |

## Platforms

| Code | Platform | App | Screens | Naming an operation | Distinct operations |
|---|---|---|---:|---:|---:|
| P01 | Guest Web | guest-web | 50 | 50 | 213 |
| P02 | Guest App | guest-app | 77 | 77 | 218 |
| P04 | Venue POS | venue-pos | 32 | 32 | 157 |
| P05 | Guest Kiosk | guest-app | 17 | 17 | 23 |
| P06 | Venue Staff App | venue-staff-app | 96 | 94 | 222 |
| P07 | Venue Scanner | venue-scanner | 11 | 11 | 24 |
| P08 | Venue Management | venue-management-web | 1661 | 1608 | 1880 |
| P09 | TICVAI Web | ticvai-web | 211 | 205 | 276 |
| P10 | Partner Web | partner-web | 43 | 43 | 118 |
| P11 | Accreditation Web | accreditation-web | 8 | 7 | 17 |
| P12 | Venue Support | venue-support-web | 28 | 28 | 67 |
| P13 | Venue CMS | venue-management-web | 104 | 104 | 207 |
| P14 | Developer | developer-portal-web | 8 | 8 | 33 |
| P15 | Kitchen Display | kitchen-display | 10 | 10 | 27 |
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
| Screens No Operation | 64 |
| Operations No Lineage | 27 |
| Tables Not Reached | 5 |
| Permissions Without Label | 70 |
| Capability Pairs | 284 |
| Modules With Capabilities | 33 |

