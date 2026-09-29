# Package report

**Generated 2026-09-29 by `tools/build-package-report.py`.** Every figure is read from a file another tool wrote in the same refresh.

## Scale

| | |
|---|---|
| Contracts | 33 |
| Operations | 2405 |
| Screens | 2440 |
| Platforms | 16 |
| Apps | 5 |
| Tables | 983 |
| Stores | 5 |
| Foreign Keys | 675 |
| Indexes | 2494 |
| Relationships | 2603 |
| Flows | 96 |
| Boards | 218 |
| Adrs | 48 |
| Services | 17 |

## The chain

**A screen is buildable when the whole chain under it resolves.** Each link is counted separately, because they fail separately.

| Link | | | |
|---|---:|---:|---|
| Requirements in scope | 2848 / 3184 | 89% | matrix rows, less the ones deliberately parked |
| Requirements contracted | 2781 / 2848 | 98% | an operation or schema field demonstrably serves it |
| Operations declaring a service | 2405 / 2405 | 100% | the operation is owned by one of the seventeen deployables |
| Operations declaring a permission | 2284 / 2405 | 95% | the checklist a grant screen renders is built from these |
| Operations with resolved lineage | 2399 / 2405 | 100% | names the tables it reads and writes -- the join the DDL cannot make itself |
| Operations reaching a screen | 2186 / 2405 | 91% | sync, webhook and job operations legitimately have none |
| Screens naming an operation | 2337 / 2440 | 96% | the rest are static, navigation shells or workshop-blocked |
| Tables reached by an operation | 983 / 983 | 100% | a table nothing reaches is a missing operation or a table that should not exist |
| Tables carrying a relationship | 909 / 983 | 92% | either end of a declared reference |

## What crosses a service boundary

**2603 declared references. 1570 stay inside one service; 1022 cross two.**

**536 of the 1022 crossings land on three tables** -- `identity.principal`, `platform.scope`, `pii.subject`. The crossings concentrate on the foundation tier rather than spreading, which is what the tier is for.

| From | To | Edges |
|---|---|---:|
| MarketingService | IdentityService | 75 |
| CatalogueService | TenancyService | 66 |
| AccessService | TenancyService | 62 |
| OrderService | IdentityService | 54 |
| CatalogueService | IdentityService | 46 |
| TenancyService | IdentityService | 40 |
| AccessService | IdentityService | 36 |
| VenueOpsService | TenancyService | 32 |
| OrderService | CatalogueService | 31 |
| PlatformService | IdentityService | 29 |
| VenueOpsService | IdentityService | 26 |
| FnbService | TenancyService | 24 |

| Most-referenced table across a boundary | Edges |
|---|---:|
| `identity.principal` | 283 |
| `platform.scope` | 170 |
| `pii.subject` | 83 |
| `orders.sales_order` | 35 |
| `approvals.request` | 33 |
| `catalogue.product` | 29 |
| `platform.outlet` | 27 |
| `platform.outbox` | 25 |
| `catalogue.variant` | 18 |
| `catalogue.performance` | 18 |

## Services

| Service | Tier | Ops | On a screen | Tables | Screens | Out | In |
|---|---|---:|---:|---:|---:|---:|---:|
| CatalogueService | commerce | 444 | 434 | 134 | 73 | 154 | 91 |
| OrderService | commerce | 277 | 257 | 105 | 101 | 133 | 77 |
| VenueOpsService | operations | 274 | 264 | 119 | 53 | 92 | 37 |
| MarketingService | engagement | 253 | 199 | 127 | 40 | 146 | 13 |
| AccessService | commerce | 243 | 238 | 75 | 29 | 125 | 18 |
| PlatformService | platform | 202 | 180 | 96 | 42 | 80 | 34 |
| TenancyService | foundation | 172 | 152 | 98 | 71 | 78 | 296 |
| FnbService | operations | 117 | 106 | 49 | 57 | 58 | 5 |
| IdentityService | foundation | 75 | 56 | 33 | 36 | 13 | 377 |
| WhiteLabelService | platform | 60 | 57 | 19 | 25 | 6 | 2 |
| WalletService | commerce | 59 | 53 | 29 | None | 12 | 5 |
| LedgerService | commerce | 57 | 49 | 20 | 20 | 36 | 35 |
| InventoryService | operations | 51 | 50 | 21 | 28 | 29 | 21 |
| ReportingService | platform | 47 | 46 | 24 | 31 | 16 | 4 |
| AiService | engagement | 31 | 21 | 16 | 21 | 13 | 4 |
| RetailService | operations | 25 | 18 | 13 | 19 | 24 | 1 |
| CrossRegionService | platform | 18 | 6 | 3 | 4 | 7 | 2 |

## Contracts

| Contract | Ops | On a screen | With lineage | With a permission |
|---|---:|---:|---:|---:|
| access | 243 | 238 | 239 | 239 |
| accreditation | 30 | 29 | 30 | 30 |
| ai | 31 | 21 | 31 | 31 |
| approvals | 49 | 43 | 48 | 49 |
| assets | 26 | 26 | 26 | 26 |
| catalogue | 236 | 232 | 236 | 233 |
| cross-region | 18 | 6 | 18 | 9 |
| finance | 57 | 49 | 57 | 57 |
| fnb | 117 | 106 | 117 | 106 |
| games | 40 | 39 | 40 | 36 |
| identity | 75 | 56 | 75 | 50 |
| inventory | 51 | 50 | 51 | 51 |
| maintenance | 36 | 36 | 36 | 36 |
| marketing-crm | 253 | 199 | 253 | 232 |
| orders | 215 | 196 | 214 | 199 |
| payments | 41 | 41 | 41 | 39 |
| platform-ops | 33 | 32 | 33 | 33 |
| promotions | 153 | 147 | 153 | 153 |
| public-api | 24 | 23 | 24 | 24 |
| queue | 22 | 16 | 22 | 14 |
| rental | 43 | 40 | 43 | 43 |
| reporting | 47 | 46 | 47 | 47 |
| resources | 61 | 61 | 61 | 61 |
| retail | 25 | 18 | 25 | 25 |
| seating | 55 | 55 | 55 | 55 |
| shift | 21 | 20 | 21 | 21 |
| subscription | 145 | 125 | 145 | 143 |
| tenancy | 48 | 37 | 48 | 47 |
| transport | 31 | 31 | 31 | 19 |
| venue-map | 15 | 15 | 15 | 15 |
| wallet | 59 | 53 | 59 | 59 |
| white-label | 60 | 57 | 60 | 57 |
| workforce | 45 | 43 | 45 | 45 |

## Platforms

| Code | Platform | App | Screens | Naming an operation | Distinct operations |
|---|---|---|---:|---:|---:|
| P01 | Guest Web | guest-web | 49 | 49 | 186 |
| P02 | Guest App | guest-app | 77 | 76 | 189 |
| P04 | Venue POS | venue-pos | 30 | 30 | 144 |
| P05 | Guest Kiosk | guest-app | 17 | 15 | 22 |
| P06 | Venue Staff App | venue-staff-app | 96 | 94 | 212 |
| P07 | Venue Scanner | venue-scanner | 11 | 11 | 27 |
| P08 | Venue Management | venue-management-web | 1186 | 1178 | 1362 |
| P09 | TICVAI Web | ticvai-web | 676 | 588 | 583 |
| P10 | Partner Web | partner-web | 51 | 51 | 151 |
| P11 | Accreditation Web | accreditation-web | 8 | 7 | 6 |
| P12 | Venue Support | venue-support-web | 28 | 28 | 59 |
| P13 | Venue CMS | venue-management-web | 100 | 100 | 142 |
| P14 | Developer | developer-portal-web | 8 | 8 | 21 |
| P15 | Kitchen Display | kitchen-display | 10 | 10 | 27 |
| P16 | Venue Analytics | venue-management-web | 69 | 68 | 58 |
| P17 | TICVAI Sign-up | signup-web | 24 | 24 | 14 |

## Open

| | |
|---|---:|
| Conflicts Open | 9 |
| Conflicts Blocking | 0 |
| Requirements Gap Contract | 5 |
| Requirements Gap Decision | 0 |
| Requirements Partial | 62 |
| Operations No Screen | 219 |
| Screens No Operation | 103 |
| Operations No Lineage | 6 |
| Tables Not Reached | 0 |
| Permissions Without Label | 70 |
| Capability Pairs | 266 |
| Modules With Capabilities | 33 |

