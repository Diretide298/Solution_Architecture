# Services and stored procedures

**25 services carry 737 of 737 operations.**
8 stored procedures exist, for the operations where a round trip per row would not survive
a Saturday.

| Service | Ops |
|---|---|
| `CatalogueService` | 52 |
| `MarketingService` | 49 |
| `OrderService` | 48 |
| `LedgerService` | 46 |
| `SubscriptionService` | 46 |
| `FnbService` | 45 |
| `InventoryService` | 43 |
| `WhiteLabelService` | 41 |
| `IdentityService` | 38 |
| `MaintenanceService` | 36 |
| `PromotionsService` | 31 |
| `SeatingService` | 29 |
| `RetailService` | 26 |
| `PlatformOpsService` | 24 |
| `AccessService` | 23 |
| `ReportingService` | 23 |
| `AiService` | 22 |
| `QueueService` | 21 |
| `TenancyService` | 18 |
| `CrossCellService` | 16 |
| `ShiftService` | 13 |
| `GamesService` | 13 |
| `ApprovalService` | 13 |
| `WorkforceService` | 11 |
| `AssetsService` | 10 |

## Stored procedures

| | Operations | Why |
|---|---|---|
| `access.sp_sync_scan_batch` | 1 | — |
| `access.sp_validate_and_record` | 1 | — |
| `catalogue.sp_acquire_lease` | 1 | — |
| `inventory.sp_post_movement` | 1 | — |
| `orders.sp_capture_payment` | 1 | — |
| `orders.sp_close_shift` | 1 | — |
| `orders.sp_post_refund` | 1 | — |
| `seating.sp_hold_seats` | 1 | — |

**Everything else is application code.** A stored procedure is a decision to move logic where it
is harder to test and harder to change, and it is worth it only where the round trips are the
problem.
