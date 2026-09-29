# Package report

**Generated 2026-09-29 by `tools/build-package-report.py`.** Every figure is read from a file another tool wrote in the same refresh.

## Scale

| | |
|---|---|
| Contracts | 33 |
| Operations | 2608 |
| Screens | 2440 |
| Platforms | 16 |
| Apps | 5 |
| Tables | 1076 |
| Stores | 9 |
| Foreign Keys | 763 |
| Indexes | 2775 |
| Relationships | 2966 |
| Flows | 96 |
| Boards | 218 |
| Adrs | 48 |
| Services | 17 |

## The chain

**A screen is buildable when the whole chain under it resolves.** Each link is counted separately, because they fail separately.

| Link | | | |
|---|---:|---:|---|
| Requirements in scope | 3165 / 3184 | 99% | matrix rows, less the ones deliberately parked |
| Requirements contracted | 3153 / 3165 | 100% | an operation or schema field demonstrably serves it |
| Operations declaring a service | 2608 / 2608 | 100% | the operation is owned by one of the seventeen deployables |
| Operations declaring a permission | 2474 / 2608 | 95% | the checklist a grant screen renders is built from these |
| Operations with resolved lineage | 2602 / 2608 | 100% | names the tables it reads and writes -- the join the DDL cannot make itself |
| Operations reaching a screen | 2386 / 2608 | 91% | sync, webhook and job operations legitimately have none |
| Screens naming an operation | 2433 / 2440 | 100% | the rest are static, navigation shells or workshop-blocked |
| Tables reached by an operation | 1076 / 1076 | 100% | a table nothing reaches is a missing operation or a table that should not exist |
| Tables carrying a relationship | 999 / 1076 | 93% | either end of a declared reference |

## What crosses a service boundary

**2966 declared references. 1797 stay inside one service; 1161 cross two.**

**595 of the 1161 crossings land on three tables** -- `identity.principal`, `platform.scope`, `pii.subject`. The crossings concentrate on the foundation tier rather than spreading, which is what the tier is for.

| From | To | Edges |
|---|---|---:|
| MarketingService | IdentityService | 77 |
| CatalogueService | TenancyService | 66 |
| AccessService | TenancyService | 66 |
| OrderService | IdentityService | 57 |
| CatalogueService | IdentityService | 46 |
| TenancyService | IdentityService | 46 |
| AiService | IdentityService | 45 |
| AccessService | IdentityService | 36 |
| VenueOpsService | TenancyService | 32 |
| OrderService | CatalogueService | 31 |
| PlatformService | IdentityService | 30 |
| VenueOpsService | IdentityService | 26 |

| Most-referenced table across a boundary | Edges |
|---|---:|
| `identity.principal` | 330 |
| `platform.scope` | 173 |
| `pii.subject` | 92 |
| `platform.outbox` | 42 |
| `orders.sales_order` | 38 |
| `approvals.request` | 36 |
| `catalogue.product` | 31 |
| `platform.outlet` | 27 |
| `catalogue.variant` | 18 |
| `catalogue.performance` | 18 |

## Services

| Service | Tier | Ops | On a screen | Tables | Screens | Out | In |
|---|---|---:|---:|---:|---:|---:|---:|
| CatalogueService | commerce | 444 | 431 | 134 | 73 | 154 | 114 |
| OrderService | commerce | 287 | 269 | 112 | 101 | 142 | 87 |
| VenueOpsService | operations | 274 | 264 | 119 | 53 | 93 | 40 |
| MarketingService | engagement | 263 | 211 | 132 | 40 | 151 | 15 |
| AccessService | commerce | 245 | 240 | 76 | 29 | 129 | 18 |
| PlatformService | platform | 206 | 185 | 98 | 42 | 82 | 35 |
| TenancyService | foundation | 202 | 181 | 107 | 71 | 105 | 329 |
| AiService | engagement | 133 | 120 | 69 | 21 | 66 | 6 |
| FnbService | operations | 120 | 109 | 49 | 57 | 58 | 5 |
| IdentityService | foundation | 89 | 71 | 38 | 36 | 23 | 435 |
| LedgerService | commerce | 71 | 62 | 27 | 20 | 52 | 37 |
| WhiteLabelService | platform | 64 | 61 | 20 | 25 | 7 | 3 |
| WalletService | commerce | 63 | 57 | 31 | None | 17 | 5 |
| InventoryService | operations | 56 | 55 | 22 | 28 | 35 | 21 |
| ReportingService | platform | 48 | 46 | 24 | 31 | 16 | 4 |
| RetailService | operations | 25 | 18 | 13 | 19 | 24 | 5 |
| CrossRegionService | platform | 18 | 6 | 3 | 4 | 7 | 2 |

## Contracts

| Contract | Ops | On a screen | With lineage | With a permission |
|---|---:|---:|---:|---:|
| access | 245 | 240 | 242 | 241 |
| accreditation | 47 | 46 | 47 | 47 |
| ai | 133 | 120 | 133 | 129 |
| approvals | 53 | 46 | 52 | 53 |
| assets | 26 | 26 | 26 | 26 |
| catalogue | 236 | 232 | 236 | 233 |
| cross-region | 18 | 6 | 18 | 9 |
| finance | 71 | 62 | 71 | 70 |
| fnb | 120 | 109 | 120 | 109 |
| games | 40 | 39 | 40 | 36 |
| identity | 89 | 71 | 89 | 62 |
| inventory | 56 | 55 | 56 | 56 |
| maintenance | 36 | 36 | 36 | 36 |
| marketing-crm | 263 | 211 | 263 | 237 |
| orders | 219 | 202 | 218 | 203 |
| payments | 47 | 47 | 47 | 45 |
| platform-ops | 33 | 32 | 33 | 33 |
| promotions | 153 | 144 | 153 | 153 |
| public-api | 25 | 24 | 24 | 25 |
| queue | 22 | 16 | 22 | 14 |
| rental | 43 | 40 | 43 | 43 |
| reporting | 48 | 46 | 48 | 48 |
| resources | 61 | 61 | 61 | 61 |
| retail | 25 | 18 | 25 | 25 |
| seating | 55 | 55 | 55 | 55 |
| shift | 21 | 20 | 21 | 21 |
| subscription | 148 | 129 | 148 | 146 |
| tenancy | 53 | 42 | 53 | 52 |
| transport | 31 | 31 | 31 | 19 |
| venue-map | 15 | 15 | 15 | 15 |
| wallet | 63 | 57 | 63 | 63 |
| white-label | 64 | 61 | 64 | 60 |
| workforce | 49 | 47 | 49 | 49 |

## Platforms

| Code | Platform | App | Screens | Naming an operation | Distinct operations |
|---|---|---|---:|---:|---:|
| P01 | Guest Web | guest-web | 49 | 49 | 208 |
| P02 | Guest App | guest-app | 77 | 76 | 211 |
| P04 | Venue POS | venue-pos | 30 | 30 | 148 |
| P05 | Guest Kiosk | guest-app | 17 | 15 | 23 |
| P06 | Venue Staff App | venue-staff-app | 96 | 94 | 221 |
| P07 | Venue Scanner | venue-scanner | 11 | 11 | 28 |
| P08 | Venue Management | venue-management-web | 1186 | 1186 | 1448 |
| P09 | TICVAI Web | ticvai-web | 676 | 675 | 706 |
| P10 | Partner Web | partner-web | 51 | 51 | 151 |
| P11 | Accreditation Web | accreditation-web | 8 | 7 | 16 |
| P12 | Venue Support | venue-support-web | 28 | 28 | 62 |
| P13 | Venue CMS | venue-management-web | 100 | 100 | 156 |
| P14 | Developer | developer-portal-web | 8 | 8 | 22 |
| P15 | Kitchen Display | kitchen-display | 10 | 10 | 27 |
| P16 | Venue Analytics | venue-management-web | 69 | 69 | 78 |
| P17 | TICVAI Sign-up | signup-web | 24 | 24 | 14 |

## Open

| | |
|---|---:|
| Conflicts Open | 9 |
| Conflicts Blocking | 0 |
| Requirements Gap Contract | 0 |
| Requirements Gap Decision | 0 |
| Requirements Partial | 12 |
| Operations No Screen | 222 |
| Screens No Operation | 7 |
| Operations No Lineage | 6 |
| Tables Not Reached | 0 |
| Permissions Without Label | 70 |
| Capability Pairs | 274 |
| Modules With Capabilities | 33 |

