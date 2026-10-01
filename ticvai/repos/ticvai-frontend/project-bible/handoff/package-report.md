# Package report

**Generated 2026-10-01 by `tools/build-package-report.py`.** Every figure is read from a file another tool wrote in the same refresh.

## Scale

| | |
|---|---|
| Contracts | 33 |
| Operations | 2668 |
| Screens | 2445 |
| Platforms | 16 |
| Apps | 5 |
| Tables | 1095 |
| Stores | 10 |
| Foreign Keys | 796 |
| Indexes | 2825 |
| Relationships | 3048 |
| Flows | 97 |
| Boards | 218 |
| Adrs | 69 |
| Services | 17 |

## The chain

**A screen is buildable when the whole chain under it resolves.** Each link is counted separately, because they fail separately.

| Link | | | |
|---|---:|---:|---|
| Requirements in scope | 3165 / 3184 | 99% | matrix rows, less the ones deliberately parked |
| Requirements contracted | 3153 / 3165 | 100% | an operation or schema field demonstrably serves it |
| Operations declaring a service | 2668 / 2668 | 100% | the operation is owned by one of the seventeen deployables |
| Operations declaring a permission | 2519 / 2668 | 94% | the checklist a grant screen renders is built from these |
| Operations with resolved lineage | 2659 / 2668 | 100% | names the tables it reads and writes -- the join the DDL cannot make itself |
| Operations reaching a screen | 2436 / 2668 | 91% | sync, webhook and job operations legitimately have none |
| Screens naming an operation | 2438 / 2445 | 100% | the rest are static, navigation shells or workshop-blocked |
| Tables reached by an operation | 1091 / 1095 | 100% | a table nothing reaches is a missing operation or a table that should not exist |
| Tables carrying a relationship | 1012 / 1095 | 92% | either end of a declared reference |

## What crosses a service boundary

**3048 declared references. 1840 stay inside one service; 1207 cross two.**

**611 of the 1207 crossings land on three tables** -- `identity.principal`, `platform.scope`, `pii.subject`. The crossings concentrate on the foundation tier rather than spreading, which is what the tier is for.

| From | To | Edges |
|---|---|---:|
| MarketingService | IdentityService | 77 |
| AccessService | TenancyService | 76 |
| CatalogueService | TenancyService | 67 |
| OrderService | IdentityService | 57 |
| CatalogueService | IdentityService | 47 |
| TenancyService | IdentityService | 47 |
| AiService | IdentityService | 46 |
| AccessService | IdentityService | 36 |
| VenueOpsService | TenancyService | 35 |
| PlatformService | IdentityService | 32 |
| OrderService | CatalogueService | 30 |
| VenueOpsService | IdentityService | 28 |

| Most-referenced table across a boundary | Edges |
|---|---:|
| `identity.principal` | 338 |
| `platform.scope` | 181 |
| `pii.subject` | 92 |
| `platform.outbox` | 44 |
| `orders.sales_order` | 39 |
| `approvals.request` | 36 |
| `catalogue.product` | 32 |
| `platform.outlet` | 27 |
| `catalogue.performance` | 19 |
| `assets.media_asset` | 17 |

## Services

| Service | Tier | Ops | On a screen | Tables | Screens | Out | In |
|---|---|---:|---:|---:|---:|---:|---:|
| CatalogueService | commerce | 449 | 433 | 135 | 73 | 160 | 116 |
| OrderService | commerce | 288 | 269 | 113 | 101 | 143 | 91 |
| VenueOpsService | operations | 285 | 275 | 123 | 53 | 104 | 43 |
| MarketingService | engagement | 264 | 211 | 130 | 40 | 153 | 16 |
| AccessService | commerce | 246 | 240 | 76 | 29 | 139 | 20 |
| PlatformService | platform | 216 | 195 | 104 | 42 | 86 | 36 |
| TenancyService | foundation | 204 | 181 | 108 | 71 | 108 | 353 |
| AiService | engagement | 141 | 128 | 74 | 21 | 70 | 4 |
| FnbService | operations | 120 | 109 | 48 | 57 | 57 | 6 |
| IdentityService | foundation | 89 | 71 | 38 | 36 | 23 | 443 |
| WhiteLabelService | platform | 79 | 77 | 25 | 25 | 10 | 4 |
| LedgerService | commerce | 72 | 62 | 27 | 20 | 54 | 37 |
| WalletService | commerce | 66 | 57 | 31 | None | 17 | 6 |
| InventoryService | operations | 58 | 58 | 22 | 28 | 36 | 22 |
| ReportingService | platform | 48 | 46 | 24 | 31 | 16 | 3 |
| RetailService | operations | 25 | 18 | 13 | 19 | 24 | 5 |
| CrossRegionService | platform | 18 | 6 | 3 | 4 | 7 | 2 |

## Contracts

| Contract | Ops | On a screen | With lineage | With a permission |
|---|---:|---:|---:|---:|
| access | 246 | 240 | 243 | 241 |
| accreditation | 47 | 46 | 47 | 47 |
| ai | 141 | 128 | 141 | 137 |
| approvals | 53 | 46 | 52 | 53 |
| assets | 26 | 26 | 26 | 26 |
| catalogue | 241 | 234 | 239 | 235 |
| cross-region | 18 | 6 | 18 | 9 |
| finance | 72 | 62 | 72 | 70 |
| fnb | 120 | 109 | 120 | 109 |
| games | 40 | 39 | 40 | 36 |
| identity | 89 | 71 | 89 | 62 |
| inventory | 58 | 58 | 58 | 58 |
| maintenance | 42 | 42 | 42 | 42 |
| marketing-crm | 264 | 211 | 264 | 237 |
| orders | 219 | 202 | 218 | 203 |
| payments | 48 | 47 | 48 | 45 |
| platform-ops | 37 | 36 | 37 | 37 |
| promotions | 153 | 144 | 153 | 153 |
| public-api | 31 | 30 | 30 | 31 |
| queue | 22 | 16 | 22 | 14 |
| rental | 43 | 40 | 43 | 43 |
| reporting | 48 | 46 | 48 | 48 |
| resources | 61 | 61 | 61 | 61 |
| retail | 25 | 18 | 25 | 25 |
| seating | 55 | 55 | 55 | 55 |
| shift | 21 | 20 | 21 | 21 |
| subscription | 148 | 129 | 148 | 146 |
| tenancy | 55 | 42 | 55 | 52 |
| transport | 31 | 31 | 31 | 19 |
| venue-map | 20 | 20 | 20 | 15 |
| wallet | 66 | 57 | 66 | 66 |
| white-label | 79 | 77 | 78 | 74 |
| workforce | 49 | 47 | 49 | 49 |

## Platforms

| Code | Platform | App | Screens | Naming an operation | Distinct operations |
|---|---|---|---:|---:|---:|
| P01 | Guest Web | guest-web | 50 | 50 | 216 |
| P02 | Guest App | guest-app | 77 | 76 | 219 |
| P04 | Venue POS | venue-pos | 30 | 30 | 148 |
| P05 | Guest Kiosk | guest-app | 17 | 15 | 23 |
| P06 | Venue Staff App | venue-staff-app | 96 | 94 | 224 |
| P07 | Venue Scanner | venue-scanner | 11 | 11 | 28 |
| P08 | Venue Management | venue-management-web | 1186 | 1186 | 1460 |
| P09 | TICVAI Web | ticvai-web | 676 | 675 | 722 |
| P10 | Partner Web | partner-web | 51 | 51 | 142 |
| P11 | Accreditation Web | accreditation-web | 8 | 7 | 16 |
| P12 | Venue Support | venue-support-web | 28 | 28 | 62 |
| P13 | Venue CMS | venue-management-web | 103 | 103 | 176 |
| P14 | Developer | developer-portal-web | 8 | 8 | 28 |
| P15 | Kitchen Display | kitchen-display | 10 | 10 | 27 |
| P16 | Venue Analytics | venue-management-web | 70 | 70 | 84 |
| P17 | TICVAI Sign-up | signup-web | 24 | 24 | 14 |

## Open

| | |
|---|---:|
| Conflicts Open | 9 |
| Conflicts Blocking | 0 |
| Requirements Gap Contract | 0 |
| Requirements Gap Decision | 0 |
| Requirements Partial | 12 |
| Operations No Screen | 232 |
| Screens No Operation | 7 |
| Operations No Lineage | 9 |
| Tables Not Reached | 4 |
| Permissions Without Label | 70 |
| Capability Pairs | 274 |
| Modules With Capabilities | 33 |

