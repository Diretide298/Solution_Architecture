# Package report

**Generated 2026-09-29 by `tools/build-package-report.py`.** Every figure is read from a file another tool wrote in the same refresh.

## Scale

| | |
|---|---|
| Contracts | 32 |
| Operations | 2147 |
| Screens | 2422 |
| Platforms | 16 |
| Apps | 5 |
| Tables | 683 |
| Stores | 5 |
| Foreign Keys | 615 |
| Indexes | 1491 |
| Relationships | 1490 |
| Flows | 96 |
| Boards | 218 |
| Adrs | 48 |
| Services | 17 |

## The chain

**A screen is buildable when the whole chain under it resolves.** Each link is counted separately, because they fail separately.

| Link | | | |
|---|---:|---:|---|
| Requirements in scope | 2788 / 3184 | 88% | matrix rows, less the ones deliberately parked |
| Requirements contracted | 2650 / 2788 | 95% | an operation or schema field demonstrably serves it |
| Operations declaring a service | 2147 / 2147 | 100% | the operation is owned by one of the seventeen deployables |
| Operations declaring a permission | 2042 / 2147 | 95% | the checklist a grant screen renders is built from these |
| Operations with resolved lineage | 1506 / 2147 | 70% | names the tables it reads and writes -- the join the DDL cannot make itself |
| Operations reaching a screen | 1859 / 2147 | 87% | sync, webhook and job operations legitimately have none |
| Screens naming an operation | 2314 / 2422 | 96% | the rest are static, navigation shells or workshop-blocked |
| Tables reached by an operation | 659 / 683 | 96% | a table nothing reaches is a missing operation or a table that should not exist |
| Tables carrying a relationship | 615 / 683 | 90% | either end of a declared reference |

## What crosses a service boundary

**1490 declared references. 876 stay inside one service; 614 cross two.**

**300 of the 614 crossings land on three tables** -- `identity.principal`, `platform.scope`, `pii.subject`. The crossings concentrate on the foundation tier rather than spreading, which is what the tier is for.

| From | To | Edges |
|---|---|---:|
| MarketingService | IdentityService | 43 |
| OrderService | IdentityService | 36 |
| TenancyService | IdentityService | 28 |
| VenueOpsService | TenancyService | 27 |
| FnbService | TenancyService | 24 |
| VenueOpsService | IdentityService | 23 |
| CatalogueService | TenancyService | 23 |
| OrderService | CatalogueService | 18 |
| OrderService | TenancyService | 18 |
| FnbService | IdentityService | 15 |
| MarketingService | TenancyService | 15 |
| InventoryService | IdentityService | 13 |

| Most-referenced table across a boundary | Edges |
|---|---:|
| `identity.principal` | 156 |
| `platform.scope` | 80 |
| `pii.subject` | 64 |
| `platform.outlet` | 27 |
| `orders.sales_order` | 25 |
| `platform.outbox` | 17 |
| `platform.tenant` | 13 |
| `catalogue.product` | 12 |
| `catalogue.variant` | 11 |
| `assets.media_asset` | 10 |

## Services

| Service | Tier | Ops | On a screen | Tables | Screens | Out | In |
|---|---|---:|---:|---:|---:|---:|---:|
| CatalogueService | commerce | 407 | 369 | 75 | 73 | 56 | 48 |
| OrderService | commerce | 254 | 231 | 69 | 101 | 89 | 59 |
| VenueOpsService | operations | 224 | 211 | 98 | 53 | 75 | 25 |
| MarketingService | engagement | 213 | 173 | 70 | 40 | 86 | 8 |
| PlatformService | platform | 184 | 161 | 64 | 42 | 30 | 8 |
| AccessService | commerce | 182 | 176 | 9 | 29 | 27 | 15 |
| TenancyService | foundation | 166 | 128 | 82 | 71 | 46 | 170 |
| FnbService | operations | 115 | 88 | 47 | 57 | 54 | 3 |
| IdentityService | foundation | 75 | 51 | 33 | 36 | 12 | 227 |
| LedgerService | commerce | 56 | 48 | 20 | 20 | 38 | 19 |
| WhiteLabelService | platform | 52 | 46 | 16 | 25 | 5 | 2 |
| InventoryService | operations | 51 | 50 | 21 | 28 | 29 | 19 |
| WalletService | commerce | 50 | 43 | 25 | None | 10 | 4 |
| ReportingService | platform | 44 | 42 | 22 | 31 | 14 | 2 |
| AiService | engagement | 31 | 21 | 16 | 21 | 12 | 2 |
| RetailService | operations | 25 | 17 | 13 | 19 | 24 | 1 |
| CrossRegionService | platform | 18 | 4 | 3 | 4 | 7 | 2 |

## Contracts

| Contract | Ops | On a screen | With lineage | With a permission |
|---|---:|---:|---:|---:|
| access | 182 | 176 | 35 | 179 |
| accreditation | 29 | 28 | 26 | 29 |
| ai | 31 | 21 | 31 | 31 |
| approvals | 46 | 45 | 26 | 46 |
| assets | 26 | 26 | 21 | 26 |
| catalogue | 206 | 183 | 95 | 203 |
| cross-region | 18 | 4 | 18 | 9 |
| finance | 56 | 48 | 56 | 56 |
| fnb | 115 | 88 | 115 | 104 |
| games | 35 | 35 | 31 | 32 |
| identity | 75 | 51 | 72 | 50 |
| inventory | 51 | 50 | 51 | 51 |
| maintenance | 36 | 36 | 36 | 36 |
| marketing-crm | 213 | 173 | 140 | 194 |
| orders | 192 | 170 | 102 | 174 |
| payments | 41 | 41 | 35 | 39 |
| platform-ops | 33 | 32 | 33 | 33 |
| promotions | 146 | 132 | 47 | 146 |
| public-api | 22 | 21 | 22 | 22 |
| queue | 22 | 16 | 22 | 14 |
| rental | 43 | 39 | 37 | 43 |
| reporting | 44 | 42 | 41 | 44 |
| resources | 49 | 48 | 45 | 49 |
| retail | 25 | 17 | 25 | 25 |
| seating | 55 | 54 | 49 | 55 |
| shift | 21 | 20 | 21 | 21 |
| subscription | 129 | 108 | 76 | 127 |
| tenancy | 48 | 32 | 47 | 47 |
| venue-map | 13 | 11 | 13 | 13 |
| wallet | 50 | 43 | 46 | 50 |
| white-label | 52 | 46 | 52 | 51 |
| workforce | 43 | 23 | 40 | 43 |

## Platforms

| Code | Platform | App | Screens | Naming an operation | Distinct operations |
|---|---|---|---:|---:|---:|
| P01 | Guest Web | guest-web | 46 | 46 | 155 |
| P02 | Guest App | guest-app | 71 | 70 | 157 |
| P04 | Venue POS | venue-pos | 30 | 30 | 143 |
| P05 | Guest Kiosk | guest-app | 17 | 15 | 22 |
| P06 | Venue Staff App | venue-staff-app | 96 | 94 | 208 |
| P07 | Venue Scanner | venue-scanner | 11 | 11 | 24 |
| P08 | Venue Management | venue-management-web | 1178 | 1168 | 1112 |
| P09 | TICVAI Web | ticvai-web | 676 | 588 | 538 |
| P10 | Partner Web | partner-web | 51 | 51 | 136 |
| P11 | Accreditation Web | accreditation-web | 8 | 4 | 4 |
| P12 | Venue Support | venue-support-web | 28 | 28 | 56 |
| P13 | Venue CMS | venue-management-web | 99 | 99 | 123 |
| P14 | Developer | developer-portal-web | 8 | 8 | 21 |
| P15 | Kitchen Display | kitchen-display | 10 | 10 | 24 |
| P16 | Venue Analytics | venue-management-web | 69 | 68 | 54 |
| P17 | TICVAI Sign-up | signup-web | 24 | 24 | 14 |

## Open

| | |
|---|---:|
| Conflicts Open | 9 |
| Conflicts Blocking | 0 |
| Requirements Gap Contract | 89 |
| Requirements Gap Decision | 5 |
| Requirements Partial | 44 |
| Operations No Screen | 288 |
| Screens No Operation | 108 |
| Operations No Lineage | 641 |
| Tables Not Reached | 24 |
| Permissions Without Label | 69 |
| Capability Pairs | 242 |
| Modules With Capabilities | 32 |

