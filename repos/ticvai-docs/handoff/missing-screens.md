# Screens the contracts need and the boards do not have

**118 operations reach no screen**, clustered on **52 resources**.

Down from 194 on 74 resources — seventeen back-office screens were added on 17 August for
approvals, finance and inventory, which were the three worst.

| Contract | Resource | Ops |
|---|---|---|
| `fnb` | `/table-visits` | 7 |
| `reporting` | `/report-executions` | 5 |
| `seating` | `/seat-maps` | 5 |
| `games` | `/game-cards` | 4 |
| `subscription` | `/invoices` | 4 |
| `maintenance` | `/maintenance-plans` | 4 |
| `reporting` | `/report-schedules` | 4 |
| `marketing-crm` | `/segments` | 4 |
| `subscription` | `/tenant-migrations` | 4 |
| `ai` | `/index-sources` | 4 |
| `cross-cell` | `/wallet-authorisations` | 3 |
| `tenancy` | `/workstations` | 3 |
| `games` | `/games` | 3 |
| `ai` | `/collections` | 3 |
| `tenancy` | `/sale-boards` | 3 |
| `promotions` | `/upsell-rules` | 3 |
| `marketing-crm` | `/consent` | 2 |
| `orders` | `/reservations` | 2 |
| `promotions` | `/bundles` | 2 |
| `marketing-crm` | `/loyalty` | 2 |
| `fnb` | `/modifier-groups` | 2 |
| `games` | `/prizes` | 2 |
| `retail` | `/retail-returns` | 2 |
| `seating` | `/seat-categories` | 2 |
| `seating` | `/seat-map-templates` | 2 |
| `promotions` | `/voucher-batches` | 2 |
| `ai` | `/proposed-actions` | 2 |
| `ai` | `/generate` | 2 |
| `ai` | `/policy` | 2 |
| `tenancy` | `/regions` | 2 |
| `cross-cell` | `/wallet-allocations` | 2 |
| `subscription` | `/cell-clusters` | 2 |
| `ai` | `/providers` | 2 |
| `promotions` | `/allocation-splits` | 2 |
| `fnb` | `/recipes` | 2 |
| `fnb` | `/tables` | 1 |
| `approvals` | `/approval-requests` | 1 |
| `retail` | `/retail-exchanges` | 1 |
| `retail` | `/shop-and-drop` | 1 |
| `ai` | `/usage` | 1 |
| `reporting` | `/report-exports` | 1 |
| `retail` | `/gift-cards` | 1 |
| `ai` | `/index-jobs` | 1 |
| `reporting` | `/report-fields` | 1 |
| `queue` | `/queue-entries` | 1 |
| `games` | `/prize-redemptions` | 1 |
| `promotions` | `/vouchers` | 1 |
| `marketing-crm` | `/consent-purposes` | 1 |
| `fnb` | `/menu-items` | 1 |
| `inventory` | `/stock-counts` | 1 |
| `catalogue` | `/entitlements` | 1 |
| `promotions` | `/coupon-codes` | 1 |

**These cluster onto roughly a dozen screens**, because a resource with six operations is one
screen with six actions. Sizing it as an operation count would repeat the report-register error.

The seventeen added on 17 August carry `wireframe.status: notStarted` and a note saying they
are **not on the board** — they need drawing before anyone builds them.
