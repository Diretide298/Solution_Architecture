# Package report

**Generated 2026-09-24 by `tools/build-package-report.py`.** Every figure is read from a file another tool wrote in the same refresh.

## Scale

| | |
|---|---|
| Contracts | 32 |
| Operations | 2113 |
| Screens | 2427 |
| Platforms | 16 |
| Apps | 5 |
| Tables | 639 |
| Stores | 5 |
| Foreign Keys | 635 |
| Indexes | 761 |
| Relationships | 1371 |
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
| Operations declaring a service | 2113 / 2113 | 100% | the operation is owned by one of the seventeen deployables |
| Operations declaring a permission | 2012 / 2113 | 95% | the checklist a grant screen renders is built from these |
| Operations with resolved lineage | 1473 / 2113 | 70% | names the tables it reads and writes -- the join the DDL cannot make itself |
| Operations reaching a screen | 1853 / 2113 | 88% | sync, webhook and job operations legitimately have none |
| Screens naming an operation | 2319 / 2427 | 96% | the rest are static, navigation shells or workshop-blocked |
| Tables reached by an operation | 619 / 639 | 97% | a table nothing reaches is a missing operation or a table that should not exist |
| Tables carrying a relationship | 568 / 639 | 89% | either end of a declared reference |

## What crosses a service boundary

**1371 declared references. 772 stay inside one service; 599 cross two.**

**261 of the 599 crossings land on three tables** -- `identity.principal`, `platform.scope`, `pii.subject`. The crossings concentrate on the foundation tier rather than spreading, which is what the tier is for.

| From | To | Edges |
|---|---|---:|
| MarketingService | IdentityService | 36 |
| OrderService | IdentityService | 30 |
| TenancyService | IdentityService | 27 |
| VenueOpsService | TenancyService | 26 |
| FnbService | TenancyService | 22 |
| CatalogueService | TenancyService | 22 |
| OrderService | TenancyService | 18 |
| VenueOpsService | IdentityService | 15 |
| MarketingService | TenancyService | 15 |
| OrderService | CatalogueService | 14 |
| FnbService | IdentityService | 12 |
| AccessService | OrderService | 12 |

| Most-referenced table across a boundary | Edges |
|---|---:|
| `identity.principal` | 128 |
| `platform.scope` | 75 |
| `pii.subject` | 58 |
| `platform.outlet` | 25 |
| `orders.sales_order` | 25 |
| `platform.outbox` | 17 |
| `catalogue.product` | 15 |
| `access.entitlement` | 11 |
| `catalogue.variant` | 10 |
| `assets.media_asset` | 10 |

## Services

| Service | Tier | Ops | On a screen | Tables | Screens | Out | In |
|---|---|---:|---:|---:|---:|---:|---:|
| CatalogueService | commerce | 404 | 369 | 71 | 73 | 59 | 47 |
| OrderService | commerce | 249 | 230 | 60 | 101 | 82 | 60 |
| VenueOpsService | operations | 221 | 211 | 90 | 53 | 71 | 30 |
| MarketingService | engagement | 209 | 175 | 64 | 40 | 79 | 8 |
| PlatformService | platform | 184 | 161 | 62 | 42 | 30 | 11 |
| AccessService | commerce | 182 | 177 | 9 | 29 | 27 | 22 |
| TenancyService | foundation | 156 | 126 | 81 | 71 | 49 | 157 |
| FnbService | operations | 111 | 87 | 41 | 57 | 53 | 9 |
| IdentityService | foundation | 70 | 49 | 32 | 36 | 14 | 193 |
| LedgerService | commerce | 56 | 48 | 18 | 20 | 34 | 19 |
| WhiteLabelService | platform | 52 | 46 | 13 | 25 | 5 | 2 |
| InventoryService | operations | 51 | 49 | 21 | 28 | 34 | 19 |
| WalletService | commerce | 50 | 43 | 25 | None | 9 | 5 |
| ReportingService | platform | 44 | 40 | 20 | 31 | 10 | 2 |
| AiService | engagement | 31 | 21 | 16 | 21 | 13 | 12 |
| RetailService | operations | 25 | 17 | 13 | 19 | 23 | 1 |
| CrossRegionService | platform | 18 | 4 | 3 | 4 | 7 | 2 |

## Contracts

| Contract | Ops | On a screen | With lineage | With a permission |
|---|---:|---:|---:|---:|
| access | 182 | 177 | 35 | 179 |
| accreditation | 29 | 28 | 26 | 29 |
| ai | 31 | 21 | 31 | 31 |
| approvals | 45 | 45 | 25 | 45 |
| assets | 26 | 26 | 21 | 26 |
| catalogue | 205 | 183 | 94 | 202 |
| cross-region | 18 | 4 | 18 | 9 |
| finance | 56 | 48 | 56 | 56 |
| fnb | 111 | 87 | 111 | 100 |
| games | 35 | 35 | 31 | 32 |
| identity | 70 | 49 | 68 | 46 |
| inventory | 51 | 49 | 51 | 51 |
| maintenance | 36 | 36 | 36 | 36 |
| marketing-crm | 209 | 175 | 136 | 190 |
| orders | 188 | 169 | 99 | 172 |
| payments | 41 | 41 | 35 | 39 |
| platform-ops | 33 | 32 | 33 | 33 |
| promotions | 145 | 132 | 46 | 145 |
| public-api | 22 | 21 | 22 | 22 |
| queue | 21 | 16 | 21 | 14 |
| rental | 43 | 39 | 37 | 43 |
| reporting | 44 | 40 | 40 | 44 |
| resources | 48 | 48 | 44 | 48 |
| retail | 25 | 17 | 25 | 25 |
| seating | 54 | 54 | 48 | 54 |
| shift | 20 | 20 | 20 | 20 |
| subscription | 129 | 108 | 76 | 127 |
| tenancy | 39 | 30 | 38 | 38 |
| venue-map | 12 | 11 | 12 | 12 |
| wallet | 50 | 43 | 46 | 50 |
| white-label | 52 | 46 | 52 | 51 |
| workforce | 43 | 23 | 40 | 43 |

## Platforms

| Code | Platform | App | Screens | Naming an operation | Distinct operations |
|---|---|---|---:|---:|---:|
| P01 | Guest Web | guest-web | 46 | 46 | 167 |
| P02 | Guest App | guest-app | 71 | 70 | 170 |
| P04 | Venue POS | venue-pos | 30 | 30 | 141 |
| P05 | Guest Kiosk | guest-app | 17 | 15 | 23 |
| P06 | Venue Staff App | venue-staff-app | 96 | 94 | 202 |
| P07 | Venue Scanner | venue-scanner | 11 | 11 | 22 |
| P08 | Venue Management | venue-management-web | 1182 | 1172 | 1103 |
| P09 | TICVAI Web | ticvai-web | 676 | 588 | 528 |
| P10 | Partner Web | partner-web | 51 | 51 | 134 |
| P11 | Accreditation Web | accreditation-web | 8 | 4 | 4 |
| P12 | Venue Support | venue-support-web | 28 | 28 | 54 |
| P13 | Venue CMS | venue-management-web | 100 | 100 | 123 |
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
| Operations No Screen | 260 |
| Screens No Operation | 108 |
| Operations No Lineage | 640 |
| Tables Not Reached | 20 |
| Permissions Without Label | 72 |
| Capability Pairs | 235 |
| Modules With Capabilities | 32 |

