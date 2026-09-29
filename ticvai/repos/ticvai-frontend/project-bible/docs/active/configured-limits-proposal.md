# Configured limits: proposed values

> **Purpose:** The one sheet of every limit the contracts call "configured", with a proposed value for the client to correct  
> **Owner:** Chinmay  
> **Status:** **Proposed, client to correct (audit R094, decided 28 September 2026)**  
> **Who corrects it:** client operations; **client finance** for the shift variance and stock-count approval thresholds

The contracts used *configured limit, threshold, window* in at least fifteen places and named no setting, no default and no column. On 28 September Chinmay adopted our default: **each limit is a venue setting with a tenant-level default**, and we send this sheet with proposed values for the client to correct.

**This sheet is the client-facing list. Each value lives in the contracts**: almost all of them on `VenueSettings` in `tenancy.yaml`, grouped as `catalogue.*`, `inventory.*`, `seating.*`, `promotions.*`, `fnb.*`, `queue.*`, `reporting.*`, `marketing.*` and `identity.*`, plus the flat names that `orders.yaml` and `shift.yaml` cite. Each carries its proposed `default` with its `minimum` and `maximum` — that is where a developer reads it and where the 400, 409 or 422 refusal is built from. The operation that applies the limit is named in the last column. When the client corrects a value here, the contract is corrected to match in the same change; if the two ever disagree, the contract is what runs and this sheet is out of date.

**How the scope works.** The tenant sets the default once with `setVenueSettingsDefaults` (read back with `getVenueSettingsDefaults`). A venue may override it within the bounds shown with `setVenueSettings`. A venue with no override — a null field — uses the tenant default. A value outside the bounds is refused `400` naming the field.

---

## The limits

| # | Limit | Setting (as the contract spells it) | Proposed default | Bounds (min – max) | Scope | Unit and meaning | Set by | Applied in |
|---|---|---|---|---|---|---|---|---|
| 1 | **Resale window** | `VenueSettings.resaleCutoffHours` | 24 | 0 – 168 | Venue, tenant default | Hours before the Performance starts after which a Ticket can no longer be listed for resale | Client operations | `orders.yaml` — `createResaleListing` (refusal `outsideResaleWindow`) |
| 2 | **Exchange window** | `VenueSettings.exchangeCutoffHours` | 24 | 0 – 720 | Venue, tenant default | Hours before the original Performance after which order lines can no longer be exchanged | Client operations | `orders.yaml` — `exchangeOrderLines` (refusal `outsideExchangeWindow`) |
| 3 | **Reschedule window** | `VenueSettings.rescheduleCutoffHours` | 24 (a transport venue: 2, "change your trip free up to two hours before departure", rev 3 REV3-21) | 0 – 720 | Venue, tenant default | Hours before the original Performance after which an Order can no longer be rescheduled | Client operations | `orders.yaml` — `rescheduleOrder` (refusal `outsideRescheduleWindow`) |
| 4 | **F&B recall window** | `VenueSettings.fnb.recallWindowMinutes` | 10 | 0 – 60 | Venue, tenant default | Minutes after a Kitchen Ticket is bumped during which it can still be recalled, never past the end of the current service; after it, the act is a refire | Client operations | `fnb.yaml` — `recallKitchenTicket` |
| 5 | **Cart hold extension length** | `VenueSettings.cartHoldExtensionMinutes` | 5 | 1 – 30 | Venue, tenant default | Minutes each extension adds to a cart's hold | Client operations | `orders.yaml` — `extendCart`, `Cart` |
| 6 | **Maximum cart extensions** | `VenueSettings.cartMaxExtensions` | 1 | 0 – 5 | Venue, tenant default | Extensions allowed per cart before `extensionCapReached` | Client operations | `orders.yaml` — `extendCart`, `Cart.maxExtensions` |
| 7 | **Product variant ceiling** | `VenueSettings.catalogue.maxVariantsPerProduct` | 200 | 1 – 2,000 | Venue, tenant default | Variants one Product may generate from its Attributes | Client operations | `catalogue.yaml` — `setProductAttributes` (409) |
| 8 | **Over-receipt tolerance** | `VenueSettings.inventory.overReceiptTolerancePercent` | 5 | 0 – 25 | Venue, tenant default | Percent above the outstanding ordered quantity a goods receipt line may record | Client operations | `inventory.yaml` — `createGoodsReceipt` |
| 9 | **Stock-count tolerance** | `VenueSettings.inventory.countVarianceTolerancePercent` | 2 | 0 – 25 | Venue, tenant default | Percent difference between counted and expected quantity per line before the line is an exception | Client operations | `inventory.yaml` — `getCountVariance` |
| 10 | **Cross-queue limit** | `VenueSettings.queue.crossQueueLimit` | 2 | 1 – 10 | Venue, tenant default | Virtual queues one guest party may be waiting in at once in the venue (`crossQueueLimitReached`) | Client operations | `queue.yaml` — `joinQueue`, `QueueJoinProblem.crossQueueLimit` |
| 11 | **Shift variance threshold** | `VenueSettings.shiftVarianceThreshold` | AED 20.00 per shift | 0 – 1,000 | Venue, tenant default | Over or short at shift close beyond which the shift waits in `pendingVariance` for `acceptShiftVariance` and `OVERSHORT_ACCEPT` | **Client finance** | `shift.yaml` — `closeShift`, `acceptShiftVariance` |
| 12 | **Dashboard refresh budget** | `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` | 24 | 1 – no maximum set | Venue, tenant default (a tenant-wide dashboard uses the tenant default) | Tile refreshes per minute, summed over a dashboard's tiles, above which the dashboard is refused | Client operations | `reporting.yaml` — `createDashboard` |
| 13 | **Report inline-run threshold** | `VenueSettings.reporting.inlineRunRowLimit` | 5,000 | 1,000 – 100,000 | Venue, tenant default | Estimated result rows above which `runReport` answers `202` and runs the report in the background | Client operations | `reporting.yaml` — `runReport` |
| 14 | **Marketing attribution window** | `VenueSettings.marketing.attributionWindowDays` | 7 | 1 – 30 | Venue, tenant default | Days after the guest's last campaign touch within which a booking is attributed to it | Client operations | `marketing-crm.yaml` — `getCampaignPerformance`, `CampaignPerformance.attributionWindowDays` |
| 15 | **Guest OTP attempt limit** | `VenueSettings.identity.guestOtpMaxAttempts` | 5 | 3 – 10 | **Tenant** (a guest code is tenant-scoped, so the tenant default is the value used) | Wrong entries allowed per one-time code before the code is invalidated and a new one must be requested | Client operations | `identity.yaml` — `verifyGuestOtp` (401) |
| 16 | **Cart lease length** | `VenueSettings.cartLeaseSeconds` | 900 (15 minutes) | 30 – 3,600 | Venue, tenant default | Seconds a cart holds capacity; the default `ttlSeconds` of an inventory hold | Client operations | `catalogue.yaml` — `acquireInventoryHold` (`ttlSeconds`) |
| 17 | **Maximum reservation extensions** | `VenueSettings.reservationMaxExtensions` | 1 | 0 – 5 | Venue, tenant default | Times one reservation may be extended | Client operations | `orders.yaml` — `extendReservation` |
| 18 | **Price variance threshold** | `RefundPolicy.varianceThreshold` | AED 5.00 per order line | None set in the contract | Venue, tenant default | Re-priced minus quoted price (CF-38) above which a variance is an exception for review rather than a routine posting | Client operations | `orders.yaml` — `RefundPolicy`; read by `finance.yaml` — `listPriceVariances` |
| 19 | **Waitlist offer hold** | `VenueSettings.catalogue.waitlistOfferHoldMinutes` | 30 | 1 – 1,440 | Venue, tenant default | Minutes a waitlist offer holds released capacity for the guest it was offered to before moving on | Client operations | `catalogue.yaml` — `offerWaitlistCapacity` |
| 20 | **Bulk price change escalation, percentage** | `VenueSettings.catalogue.bulkPriceChangeEscalationPercent` | 10 | 0 – 100 | Venue, tenant default | Percent change to any one price above which a bulk reprice needs `PRICE_CONFIGURE` rather than `PRODUCT_CONFIGURE` (audit R197) | Client operations | `catalogue.yaml` — `bulkChangePrices` (403 `price-escalation-required`) |
| 21 | **Bulk price change escalation, count** | `VenueSettings.catalogue.bulkPriceChangeEscalationCount` | 50 | 1 – no maximum set | Venue, tenant default | Prices one bulk reprice may touch before it needs `PRICE_CONFIGURE` (audit R197) | Client operations | `catalogue.yaml` — `bulkChangePrices` (403 `price-escalation-required`) |
| 22 | **Stock-count approval amount** | `VenueSettings.inventory.countVarianceApprovalAmount` | 1,000.00 in the venue currency | None set in the contract | Venue, tenant default | Total variance value of a count above which posting it needs approval | **Client finance** | `inventory.yaml` — `postStockCount` |
| 23 | **Seat hold extension length** | `VenueSettings.seating.seatHoldExtensionSeconds` | 300 | 60 – 1,800 | Venue, tenant default | Seconds each extension adds to a seat hold; no hold outlives 30 minutes in all (audit R169) | Client operations | `seating.yaml` — `extendSeatHold` |
| 24 | **Maximum seat hold extensions** | `VenueSettings.seating.seatHoldMaxExtensions` | 2 | 0 – 5 | Venue, tenant default | Times one seat hold may be extended | Client operations | `seating.yaml` — `extendSeatHold` |
| 25 | **Promotion discount cap** | `VenueSettings.promotions.maxDiscountPercent` | 30 | 0 – 100 | Venue, tenant default | Largest discount, in percent, one promotion may give (the figure the workshop pack shows) | Client operations | `promotions.yaml` — `createPromotion` (400) |
| 26 | **Near-zero line price** | `VenueSettings.promotions.nearZeroLinePrice` | AED 1.00 | None set in the contract | Venue, tenant default | Net line price below which a stacked promotion combination is flagged `isNearZero` — a warning, not a refusal (audit R096 (5)) | Client operations | `promotions.yaml` — `analysePromotionConflicts` |
| 27 | **Comp escalation amount** | `VenueSettings.fnb.compEscalationAmount` | AED 100.00 | None set in the contract | Venue, tenant default | Line value above which a comp needs `ORDER_DISCOUNT` rather than `ORDER_MODIFY` (audit R197) | Client operations | `fnb.yaml` — `compItem` (403 `comp-escalation-required`) |
| 28 | **Seats per guest booking** | `VenueSettings.seating.maxSeatsPerGuestOrder` | 10 | 1 – 50 | Venue, tenant default; **guest channels only** (staff and POS keep 10 per sale, audit R080 (c)) | Seats one guest may take for one performance in one booking on Guest Web or the Guest App, counting seats they already hold (decided 29 September, rev 3 REV3-7) | Client operations | `seating.yaml` — `createSeatHold` (422 `seat-limit-exceeded`); also `orders.yaml` — `addCartLine`, `createOrder` (422 `seatLimitExceeded`) |

Money thresholds are in the venue's trading currency; the AED figures are for a UAE venue. A venue in another currency sets its own figure rather than converting this one. Where a row says *none set in the contract* or *no maximum set*, the contract has no bound yet; the client may propose one.

---

## Not on this sheet

- **No journal approval threshold.** Finance approves every manual journal: a finance user posts it, a finance manager or director approves it, and only then does it reach the ledger (`createJournalEntry`, `approveJournalEntry` in `finance.yaml`, the approver never the poster). There is no amount below which a journal skips approval, so there is nothing to set.
- **The venue's food-safety lead** (`VenueSettings.fnb.foodSafetyLeadPrincipalId`, audit R096 (9)) sits with these settings but is a venue fact, not a limit: it has no tenant default, and while it is null `escalateCorrectiveAction` is refused `409 no-food-safety-lead`.
- **Display currencies** (`VenueSettings.displayCurrencies`, audit R120 (a)) are a venue choice of which currencies to show guests, with no default beyond the trading currency.
- **Staff password lockout** (`lockoutAfterAttempts` in `identity.yaml`) is for staff credentials, not the guest OTP.
- **Guest two-step verification** (`VenueSettings.identity.guestTwoStep`, decided 29 September, rev 3 GAP-B1, per venue) is a venue switch, not a limit: off unless the venue enables it, with a proposed list of step-up actions (change contact details, change password, manage payment methods, delete account) for the client to correct. A guest's enrolment is tenant-wide.
- **The refund approval threshold** (CF-36) is venue policy already.
- **AI proposal expiry** (7 days proposed, 24 hours approved-but-not-applied) is audit R213 (2) and lives in `ai.yaml`.

---

## What the client does

Correct any value in the *Proposed default* or *Bounds* columns, and say if any limit should be fixed at tenant level rather than overridable per venue. We then change the contract to match.
