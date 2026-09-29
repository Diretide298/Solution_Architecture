# Package report

**Generated 2026-09-29 by `tools/build-package-report.py`.** Every figure is read from a file another tool wrote in the same refresh.

## Scale

| | |
|---|---|
| Contracts | 33 |
| Operations | 2298 |
| Screens | 2440 |
| Platforms | 16 |
| Apps | 5 |
| Tables | 771 |
| Stores | 5 |
| Foreign Keys | 640 |
| Indexes | 1695 |
| Relationships | 1661 |
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
| Operations declaring a service | 2298 / 2298 | 100% | the operation is owned by one of the seventeen deployables |
| Operations declaring a permission | 2177 / 2298 | 95% | the checklist a grant screen renders is built from these |
| Operations with resolved lineage | 1647 / 2298 | 72% | names the tables it reads and writes -- the join the DDL cannot make itself |
| Operations reaching a screen | 2080 / 2298 | 91% | sync, webhook and job operations legitimately have none |
| Screens naming an operation | 2334 / 2440 | 96% | the rest are static, navigation shells or workshop-blocked |
| Tables reached by an operation | 747 / 771 | 97% | a table nothing reaches is a missing operation or a table that should not exist |
| Tables carrying a relationship | 689 / 771 | 89% | either end of a declared reference |

## What crosses a service boundary

**1661 declared references. 941 stay inside one service; 707 cross two.**

**339 of the 707 crossings land on three tables** -- `identity.principal`, `platform.scope`, `pii.subject`. The crossings concentrate on the foundation tier rather than spreading, which is what the tier is for.

| From | To | Edges |
|---|---|---:|
| MarketingService | IdentityService | 68 |
| OrderService | IdentityService | 37 |
| VenueOpsService | TenancyService | 32 |
| TenancyService | IdentityService | 28 |
| VenueOpsService | IdentityService | 26 |
| FnbService | TenancyService | 24 |
| CatalogueService | TenancyService | 24 |
| OrderService | CatalogueService | 21 |
| MarketingService | TenancyService | 19 |
| OrderService | TenancyService | 19 |
| MarketingService | OrderService | 17 |
| FnbService | IdentityService | 15 |

| Most-referenced table across a boundary | Edges |
|---|---:|
| `identity.principal` | 177 |
| `platform.scope` | 88 |
| `pii.subject` | 74 |
| `orders.sales_order` | 29 |
| `platform.outlet` | 27 |
| `platform.outbox` | 17 |
| `catalogue.variant` | 16 |
| `catalogue.product` | 15 |
| `assets.media_asset` | 13 |
| `platform.tenant` | 13 |

## Services

| Service | Tier | Ops | On a screen | Tables | Screens | Out | In |
|---|---|---:|---:|---:|---:|---:|---:|
| CatalogueService | commerce | 415 | 405 | 77 | 73 | 59 | 63 |
| VenueOpsService | operations | 270 | 260 | 113 | 53 | 91 | 36 |
| OrderService | commerce | 268 | 248 | 84 | 101 | 99 | 66 |
| MarketingService | engagement | 248 | 194 | 113 | 40 | 139 | 8 |
| AccessService | commerce | 206 | 201 | 11 | 29 | 30 | 15 |
| PlatformService | platform | 186 | 163 | 64 | 42 | 30 | 14 |
| TenancyService | foundation | 168 | 150 | 83 | 71 | 46 | 185 |
| FnbService | operations | 117 | 106 | 49 | 57 | 58 | 5 |
| IdentityService | foundation | 75 | 56 | 33 | 36 | 12 | 259 |
| WhiteLabelService | platform | 60 | 57 | 19 | 25 | 6 | 2 |
| WalletService | commerce | 59 | 53 | 28 | None | 12 | 5 |
| LedgerService | commerce | 57 | 49 | 20 | 20 | 39 | 22 |
| InventoryService | operations | 51 | 50 | 21 | 28 | 29 | 19 |
| ReportingService | platform | 44 | 43 | 22 | 31 | 14 | 3 |
| AiService | engagement | 31 | 21 | 16 | 21 | 12 | 2 |
| RetailService | operations | 25 | 18 | 13 | 19 | 24 | 1 |
| CrossRegionService | platform | 18 | 6 | 3 | 4 | 7 | 2 |

## Contracts

| Contract | Ops | On a screen | With lineage | With a permission |
|---|---:|---:|---:|---:|
| access | 206 | 201 | 38 | 203 |
| accreditation | 29 | 28 | 26 | 29 |
| ai | 31 | 21 | 31 | 31 |
| approvals | 48 | 44 | 28 | 48 |
| assets | 26 | 26 | 21 | 26 |
| catalogue | 214 | 210 | 97 | 211 |
| cross-region | 18 | 6 | 18 | 9 |
| finance | 57 | 49 | 57 | 57 |
| fnb | 117 | 106 | 117 | 106 |
| games | 39 | 39 | 34 | 36 |
| identity | 75 | 56 | 73 | 50 |
| inventory | 51 | 50 | 51 | 51 |
| maintenance | 36 | 36 | 36 | 36 |
| marketing-crm | 248 | 194 | 205 | 227 |
| orders | 206 | 187 | 116 | 188 |
| payments | 41 | 41 | 35 | 39 |
| platform-ops | 33 | 32 | 33 | 33 |
| promotions | 146 | 140 | 47 | 146 |
| public-api | 24 | 23 | 24 | 24 |
| queue | 22 | 16 | 22 | 14 |
| rental | 43 | 40 | 37 | 43 |
| reporting | 44 | 43 | 41 | 44 |
| resources | 58 | 57 | 50 | 58 |
| retail | 25 | 18 | 25 | 25 |
| seating | 55 | 55 | 49 | 55 |
| shift | 21 | 20 | 21 | 21 |
| subscription | 129 | 108 | 76 | 127 |
| tenancy | 48 | 37 | 47 | 47 |
| transport | 31 | 31 | 25 | 19 |
| venue-map | 15 | 15 | 14 | 15 |
| wallet | 59 | 53 | 54 | 59 |
| white-label | 60 | 57 | 59 | 57 |
| workforce | 43 | 41 | 40 | 43 |

## Platforms

| Code | Platform | App | Screens | Naming an operation | Distinct operations |
|---|---|---|---:|---:|---:|
| P01 | Guest Web | guest-web | 49 | 49 | 186 |
| P02 | Guest App | guest-app | 77 | 76 | 188 |
| P04 | Venue POS | venue-pos | 30 | 30 | 144 |
| P05 | Guest Kiosk | guest-app | 17 | 15 | 22 |
| P06 | Venue Staff App | venue-staff-app | 96 | 94 | 212 |
| P07 | Venue Scanner | venue-scanner | 11 | 11 | 24 |
| P08 | Venue Management | venue-management-web | 1186 | 1178 | 1303 |
| P09 | TICVAI Web | ticvai-web | 676 | 588 | 547 |
| P10 | Partner Web | partner-web | 51 | 51 | 136 |
| P11 | Accreditation Web | accreditation-web | 8 | 4 | 4 |
| P12 | Venue Support | venue-support-web | 28 | 28 | 56 |
| P13 | Venue CMS | venue-management-web | 100 | 100 | 141 |
| P14 | Developer | developer-portal-web | 8 | 8 | 21 |
| P15 | Kitchen Display | kitchen-display | 10 | 10 | 26 |
| P16 | Venue Analytics | venue-management-web | 69 | 68 | 55 |
| P17 | TICVAI Sign-up | signup-web | 24 | 24 | 14 |

## Open

| | |
|---|---:|
| Conflicts Open | 9 |
| Conflicts Blocking | 0 |
| Requirements Gap Contract | 89 |
| Requirements Gap Decision | 5 |
| Requirements Partial | 44 |
| Operations No Screen | 218 |
| Screens No Operation | 106 |
| Operations No Lineage | 651 |
| Tables Not Reached | 24 |
| Permissions Without Label | 70 |
| Capability Pairs | 260 |
| Modules With Capabilities | 33 |

