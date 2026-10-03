# Package report

**Generated 2026-10-03 by `tools/build-package-report.py`.** Every figure is read from a file another tool wrote in the same refresh.

## Scale

| | |
|---|---|
| Contracts | 33 |
| Operations | 2738 |
| Screens | 2450 |
| Platforms | 16 |
| Apps | 5 |
| Tables | 1113 |
| Stores | 10 |
| Foreign Keys | 796 |
| Indexes | 2825 |
| Relationships | 3065 |
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
| Operations declaring a service | 2738 / 2738 | 100% | the operation is owned by one of the seventeen deployables |
| Operations declaring a permission | 2577 / 2738 | 94% | the checklist a grant screen renders is built from these |
| Operations with resolved lineage | 2705 / 2738 | 99% | names the tables it reads and writes -- the join the DDL cannot make itself |
| Operations reaching a screen | 2489 / 2738 | 91% | sync, webhook and job operations legitimately have none |
| Screens naming an operation | 2383 / 2450 | 97% | the rest are static, navigation shells or workshop-blocked |
| Tables reached by an operation | 1109 / 1113 | 100% | a table nothing reaches is a missing operation or a table that should not exist |
| Tables carrying a relationship | 1023 / 1113 | 92% | either end of a declared reference |

## What crosses a service boundary

**3065 declared references. 1842 stay inside one service; 1222 cross two.**

**621 of the 1222 crossings land on three tables** -- `identity.principal`, `platform.scope`, `pii.subject`. The crossings concentrate on the foundation tier rather than spreading, which is what the tier is for.

| From | To | Edges |
|---|---|---:|
| MarketingService | IdentityService | 78 |
| AccessService | TenancyService | 76 |
| CatalogueService | TenancyService | 67 |
| OrderService | IdentityService | 58 |
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
| `platform.scope` | 182 |
| `pii.subject` | 92 |
| `platform.outbox` | 44 |
| `orders.sales_order` | 39 |
| `approvals.request` | 37 |
| `catalogue.product` | 32 |
| `platform.outlet` | 28 |
| `catalogue.performance` | 19 |
| `assets.media_asset` | 17 |

## Services

| Service | Tier | Ops | On a screen | Tables | Screens | Out | In |
|---|---|---:|---:|---:|---:|---:|---:|
| CatalogueService | commerce | 443 | 415 | 137 | 73 | 160 | 117 |
| OrderService | commerce | 298 | 278 | 114 | 101 | 146 | 93 |
| VenueOpsService | operations | 287 | 273 | 124 | 53 | 105 | 43 |
| MarketingService | engagement | 274 | 230 | 132 | 40 | 154 | 15 |
| AccessService | commerce | 250 | 239 | 77 | 29 | 140 | 20 |
| PlatformService | platform | 221 | 197 | 108 | 42 | 86 | 36 |
| TenancyService | foundation | 209 | 183 | 108 | 71 | 111 | 355 |
| AiService | engagement | 144 | 130 | 75 | 21 | 69 | 4 |
| FnbService | operations | 133 | 124 | 51 | 57 | 59 | 6 |
| IdentityService | foundation | 94 | 79 | 38 | 36 | 23 | 453 |
| WhiteLabelService | platform | 93 | 91 | 27 | 25 | 13 | 4 |
| LedgerService | commerce | 72 | 62 | 27 | 20 | 56 | 38 |
| WalletService | commerce | 68 | 60 | 31 | None | 17 | 6 |
| InventoryService | operations | 58 | 55 | 22 | 28 | 36 | 22 |
| ReportingService | platform | 51 | 49 | 25 | 31 | 16 | 3 |
| RetailService | operations | 25 | 22 | 13 | 19 | 24 | 5 |
| CrossRegionService | platform | 18 | 2 | 3 | 4 | 7 | 2 |

## Contracts

| Contract | Ops | On a screen | With lineage | With a permission |
|---|---:|---:|---:|---:|
| access | 250 | 239 | 246 | 245 |
| accreditation | 47 | 47 | 47 | 47 |
| ai | 144 | 130 | 143 | 140 |
| approvals | 57 | 46 | 56 | 57 |
| assets | 26 | 26 | 26 | 26 |
| catalogue | 245 | 227 | 241 | 239 |
| cross-region | 18 | 2 | 18 | 9 |
| finance | 72 | 62 | 72 | 70 |
| fnb | 133 | 124 | 130 | 120 |
| games | 40 | 35 | 40 | 36 |
| identity | 94 | 79 | 90 | 63 |
| inventory | 58 | 55 | 58 | 58 |
| maintenance | 44 | 44 | 44 | 44 |
| marketing-crm | 274 | 230 | 272 | 245 |
| orders | 222 | 205 | 219 | 206 |
| payments | 49 | 48 | 49 | 46 |
| platform-ops | 40 | 39 | 40 | 40 |
| promotions | 143 | 134 | 143 | 143 |
| public-api | 31 | 30 | 30 | 31 |
| queue | 22 | 16 | 22 | 14 |
| rental | 43 | 40 | 43 | 43 |
| reporting | 51 | 49 | 50 | 51 |
| resources | 61 | 61 | 61 | 61 |
| retail | 25 | 22 | 25 | 25 |
| seating | 55 | 54 | 55 | 55 |
| shift | 27 | 25 | 27 | 27 |
| subscription | 150 | 128 | 150 | 148 |
| tenancy | 56 | 44 | 56 | 53 |
| transport | 31 | 31 | 31 | 19 |
| venue-map | 20 | 20 | 20 | 15 |
| wallet | 68 | 60 | 66 | 68 |
| white-label | 93 | 91 | 86 | 84 |
| workforce | 49 | 46 | 49 | 49 |

## Platforms

| Code | Platform | App | Screens | Naming an operation | Distinct operations |
|---|---|---|---:|---:|---:|
| P01 | Guest Web | guest-web | 50 | 50 | 210 |
| P02 | Guest App | guest-app | 77 | 77 | 214 |
| P04 | Venue POS | venue-pos | 32 | 32 | 151 |
| P05 | Guest Kiosk | guest-app | 17 | 15 | 24 |
| P06 | Venue Staff App | venue-staff-app | 96 | 94 | 220 |
| P07 | Venue Scanner | venue-scanner | 11 | 11 | 24 |
| P08 | Venue Management | venue-management-web | 1661 | 1607 | 1837 |
| P09 | TICVAI Web | ticvai-web | 211 | 205 | 269 |
| P10 | Partner Web | partner-web | 43 | 43 | 118 |
| P11 | Accreditation Web | accreditation-web | 8 | 7 | 17 |
| P12 | Venue Support | venue-support-web | 28 | 28 | 67 |
| P13 | Venue CMS | venue-management-web | 103 | 103 | 194 |
| P14 | Developer | developer-portal-web | 8 | 8 | 28 |
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
| Operations No Screen | 249 |
| Screens No Operation | 67 |
| Operations No Lineage | 33 |
| Tables Not Reached | 4 |
| Permissions Without Label | 70 |
| Capability Pairs | 282 |
| Modules With Capabilities | 33 |

