# Package report

**Generated 2026-09-21 by `tools/build-package-report.py`.** Every figure is read from a file another tool wrote in the same refresh.

## Scale

| | |
|---|---|
| Contracts | 32 |
| Operations | 2073 |
| Screens | 2427 |
| Platforms | 16 |
| Apps | 5 |
| Tables | 627 |
| Stores | 5 |
| Foreign Keys | 633 |
| Indexes | 738 |
| Relationships | 1354 |
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
| Operations declaring a service | 2073 / 2073 | 100% | the operation is owned by one of the seventeen deployables |
| Operations declaring a permission | 1979 / 2073 | 95% | the checklist a grant screen renders is built from these |
| Operations with resolved lineage | 1429 / 2073 | 69% | names the tables it reads and writes -- the join the DDL cannot make itself |
| Operations reaching a screen | 1806 / 2073 | 87% | sync, webhook and job operations legitimately have none |
| Screens naming an operation | 2319 / 2427 | 96% | the rest are static, navigation shells or workshop-blocked |
| Tables reached by an operation | 607 / 627 | 97% | a table nothing reaches is a missing operation or a table that should not exist |
| Tables carrying a relationship | 559 / 627 | 89% | either end of a declared reference |

## What crosses a service boundary

**1354 declared references. 763 stay inside one service; 591 cross two.**

**260 of the 591 crossings land on three tables** -- `identity.principal`, `platform.scope`, `pii.subject`. The crossings concentrate on the foundation tier rather than spreading, which is what the tier is for.

| From | To | Edges |
|---|---|---:|
| MarketingService | IdentityService | 36 |
| OrderService | IdentityService | 29 |
| TenancyService | IdentityService | 27 |
| VenueOpsService | TenancyService | 26 |
| CatalogueService | TenancyService | 22 |
| FnbService | TenancyService | 19 |
| OrderService | TenancyService | 18 |
| VenueOpsService | IdentityService | 15 |
| MarketingService | TenancyService | 15 |
| FnbService | IdentityService | 12 |
| OrderService | CatalogueService | 12 |
| AccessService | OrderService | 12 |

| Most-referenced table across a boundary | Edges |
|---|---:|
| `identity.principal` | 128 |
| `platform.scope` | 75 |
| `pii.subject` | 57 |
| `orders.sales_order` | 25 |
| `platform.outlet` | 22 |
| `platform.outbox` | 17 |
| `catalogue.product` | 14 |
| `access.entitlement` | 11 |
| `catalogue.variant` | 10 |
| `assets.media_asset` | 10 |

## Services

| Service | Tier | Ops | On a screen | Tables | Screens | Out | In |
|---|---|---:|---:|---:|---:|---:|---:|
| CatalogueService | commerce | 398 | 363 | 69 | 73 | 59 | 45 |
| OrderService | commerce | 233 | 213 | 57 | 101 | 79 | 58 |
| VenueOpsService | operations | 221 | 211 | 90 | 53 | 71 | 30 |
| MarketingService | engagement | 205 | 171 | 62 | 40 | 77 | 8 |
| PlatformService | platform | 184 | 161 | 62 | 42 | 30 | 11 |
| AccessService | commerce | 182 | 177 | 9 | 29 | 27 | 22 |
| TenancyService | foundation | 156 | 126 | 81 | 71 | 49 | 154 |
| FnbService | operations | 102 | 84 | 36 | 57 | 50 | 9 |
| IdentityService | foundation | 68 | 47 | 32 | 36 | 14 | 192 |
| LedgerService | commerce | 56 | 48 | 18 | 20 | 34 | 19 |
| InventoryService | operations | 51 | 49 | 21 | 28 | 34 | 19 |
| WhiteLabelService | platform | 50 | 32 | 13 | 25 | 5 | 2 |
| WalletService | commerce | 50 | 43 | 25 | None | 9 | 5 |
| ReportingService | platform | 43 | 39 | 20 | 31 | 10 | 2 |
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
| catalogue | 199 | 177 | 88 | 196 |
| cross-region | 18 | 4 | 18 | 9 |
| finance | 56 | 48 | 56 | 56 |
| fnb | 102 | 84 | 102 | 92 |
| games | 35 | 35 | 31 | 32 |
| identity | 68 | 47 | 66 | 45 |
| inventory | 51 | 49 | 51 | 51 |
| maintenance | 36 | 36 | 36 | 36 |
| marketing-crm | 205 | 171 | 132 | 188 |
| orders | 175 | 155 | 84 | 160 |
| payments | 39 | 39 | 33 | 39 |
| platform-ops | 33 | 32 | 33 | 33 |
| promotions | 145 | 132 | 46 | 145 |
| public-api | 22 | 21 | 22 | 22 |
| queue | 21 | 16 | 21 | 14 |
| rental | 43 | 39 | 37 | 43 |
| reporting | 43 | 39 | 39 | 43 |
| resources | 48 | 48 | 44 | 48 |
| retail | 25 | 17 | 25 | 25 |
| seating | 54 | 54 | 47 | 54 |
| shift | 19 | 19 | 19 | 19 |
| subscription | 129 | 108 | 76 | 127 |
| tenancy | 39 | 30 | 38 | 38 |
| venue-map | 12 | 11 | 12 | 12 |
| wallet | 50 | 43 | 46 | 50 |
| white-label | 50 | 32 | 49 | 49 |
| workforce | 43 | 23 | 40 | 43 |

## Platforms

| Code | Platform | App | Screens | Naming an operation | Distinct operations |
|---|---|---|---:|---:|---:|
| P01 | Guest Web | guest-web | 46 | 46 | 154 |
| P02 | Guest App | guest-app | 71 | 70 | 154 |
| P04 | Venue POS | venue-pos | 30 | 30 | 140 |
| P05 | Guest Kiosk | guest-app | 17 | 15 | 23 |
| P06 | Venue Staff App | venue-staff-app | 96 | 94 | 202 |
| P07 | Venue Scanner | venue-scanner | 11 | 11 | 22 |
| P08 | Venue Management | venue-management-web | 1182 | 1172 | 1083 |
| P09 | TICVAI Web | ticvai-web | 676 | 588 | 528 |
| P10 | Partner Web | partner-web | 51 | 51 | 134 |
| P11 | Accreditation Web | accreditation-web | 8 | 4 | 4 |
| P12 | Venue Support | venue-support-web | 28 | 28 | 54 |
| P13 | Venue CMS | venue-management-web | 100 | 100 | 140 |
| P14 | Developer | developer-portal-web | 8 | 8 | 21 |
| P15 | Kitchen Display | kitchen-display | 10 | 10 | 24 |
| P16 | Venue Analytics | venue-management-web | 69 | 68 | 53 |
| P17 | TICVAI Sign-up | signup-web | 24 | 24 | 14 |

## Open

| | |
|---|---:|
| Conflicts Open | 9 |
| Conflicts Blocking | 0 |
| Requirements Gap Contract | 89 |
| Requirements Gap Decision | 5 |
| Requirements Partial | 44 |
| Operations No Screen | 267 |
| Screens No Operation | 108 |
| Operations No Lineage | 644 |
| Tables Not Reached | 20 |
| Permissions Without Label | 72 |
| Capability Pairs | 232 |
| Modules With Capabilities | 32 |

