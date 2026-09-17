"""Generated. The declared reads and writes of each operation."""

READS = {
 "acquireInventoryHold": [
  "SELECT * FROM catalogue.channel_capacity LIMIT 50",
  "SELECT * FROM catalogue.inventory_hold LIMIT 50",
  "SELECT * FROM platform.workstation WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "allocateBlockedSeats": [
  "SELECT * FROM seating.seat_hold LIMIT 50"
 ],
 "analysePromotionConflicts": [
  "SELECT * FROM promotions.promotion LIMIT 50"
 ],
 "assessProductChange": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.cart LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "assignCoupon": [
  "SELECT * FROM promotions.coupon_code WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "assignSeats": [
  "SELECT * FROM catalogue.price LIMIT 50",
  "SELECT * FROM seating.seat LIMIT 50",
  "SELECT * FROM seating.seat_hold LIMIT 50",
  "SELECT * FROM seating.seating_rules LIMIT 50"
 ],
 "bulkChangePrices": [
  "SELECT * FROM catalogue.price_list LIMIT 50",
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "cancelPerformance": [
  "SELECT * FROM catalogue.performance LIMIT 50"
 ],
 "cloneProduct": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.variant LIMIT 50"
 ],
 "cloneSeatMap": [
  "SELECT * FROM seating.seat_map LIMIT 50",
  "SELECT * FROM seating.section WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "commitCatalogueImport": [
  "SELECT * FROM catalogue.import_job WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "commitImportJob": [
  "SELECT * FROM seating.import_job LIMIT 50"
 ],
 "copyPriceList": [
  "SELECT * FROM catalogue.price_list LIMIT 50"
 ],
 "copySeatMapSection": [
  "SELECT * FROM seating.seat_map LIMIT 50",
  "SELECT * FROM seating.section WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createBundle": [
  "SELECT * FROM promotions.allocation_component LIMIT 50",
  "SELECT * FROM promotions.bundle LIMIT 50",
  "SELECT * FROM promotions.bundle_component LIMIT 50"
 ],
 "createChannelCapacity": [
  "SELECT * FROM catalogue.channel_capacity LIMIT 50"
 ],
 "createCouponCampaign": [
  "SELECT * FROM promotions.coupon_campaign LIMIT 50"
 ],
 "createDonationCampaign": [
  "SELECT * FROM ledger.account LIMIT 50"
 ],
 "createEntitlementTemplate": [
  "SELECT * FROM catalogue.entitlement_template WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createEvent": [
  "SELECT * FROM catalogue.event WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createPerformances": [
  "SELECT * FROM catalogue.performance LIMIT 50"
 ],
 "createPriceList": [
  "SELECT * FROM catalogue.price_list LIMIT 50"
 ],
 "createProduct": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createPromotion": [
  "SELECT * FROM promotions.promotion LIMIT 50"
 ],
 "createSeatBlock": [
  "SELECT * FROM seating.seat_block WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createSeatCategory": [
  "SELECT * FROM seating.seat_category LIMIT 50"
 ],
 "createSeatHold": [
  "SELECT * FROM seating.seat_hold LIMIT 50"
 ],
 "createSeatMap": [
  "SELECT * FROM seating.seat_map LIMIT 50",
  "SELECT * FROM seating.section WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createSeatMapTemplate": [
  "SELECT * FROM seating.seat_map_template LIMIT 50"
 ],
 "createUpsellRule": [
  "SELECT * FROM promotions.upsell_rule LIMIT 50"
 ],
 "createVoucherBatch": [
  "SELECT * FROM promotions.voucher_batch LIMIT 50"
 ],
 "deleteUpsellRule": [
  "SELECT * FROM promotions.upsell_rule LIMIT 50"
 ],
 "diffSeatMapVersions": [
  "SELECT * FROM seating.seat_map LIMIT 50",
  "SELECT * FROM seating.section WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "endPromotion": [
  "SELECT * FROM promotions.promotion LIMIT 50"
 ],
 "evaluatePromotions": [
  "SELECT * FROM catalogue.price_list LIMIT 50",
  "SELECT * FROM promotions.promotion LIMIT 50"
 ],
 "extendSeatHold": [
  "SELECT * FROM seating.seat_hold LIMIT 50"
 ],
 "forceReleaseInventoryHold": [
  "SELECT * FROM catalogue.inventory_hold LIMIT 50"
 ],
 "freezeEntitlement": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "generateCouponCodes": [
  "SELECT * FROM promotions.coupon_campaign LIMIT 50"
 ],
 "getAvailability": [
  "SELECT * FROM catalogue.channel_capacity LIMIT 50",
  "SELECT * FROM catalogue.inventory_hold LIMIT 50",
  "SELECT * FROM catalogue.performance LIMIT 50"
 ],
 "getBundle": [
  "SELECT * FROM promotions.allocation_component LIMIT 50",
  "SELECT * FROM promotions.bundle LIMIT 50",
  "SELECT * FROM promotions.bundle_component LIMIT 50"
 ],
 "getChannelAllocations": [
  "SELECT * FROM catalogue.channel_allocation LIMIT 50"
 ],
 "getCouponCode": [
  "SELECT * FROM promotions.coupon_code WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getEvent": [
  "SELECT * FROM catalogue.event WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getImportJob": [
  "SELECT * FROM seating.import_job LIMIT 50"
 ],
 "getLatestBundle": [
  "SELECT * FROM catalogue.published_bundle LIMIT 50"
 ],
 "getMyMemberships": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM marketing.loyalty_position LIMIT 50"
 ],
 "getPerformance": [
  "SELECT * FROM catalogue.performance LIMIT 50"
 ],
 "getPriceList": [
  "SELECT * FROM catalogue.price_list LIMIT 50"
 ],
 "getProduct": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getPromotion": [
  "SELECT * FROM promotions.promotion LIMIT 50"
 ],
 "getPromotionUsage": [
  "SELECT * FROM promotions.promotion LIMIT 50"
 ],
 "getRecommendations": [
  "SELECT * FROM catalogue.channel_capacity LIMIT 50",
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM marketing.guest_profile LIMIT 50",
  "SELECT * FROM orders.cart LIMIT 50",
  "SELECT * FROM promotions.promotion LIMIT 50"
 ],
 "getSeatAvailability": [
  "SELECT * FROM seating.seat LIMIT 50",
  "SELECT * FROM seating.seat_category LIMIT 50",
  "SELECT * FROM seating.seat_hold LIMIT 50"
 ],
 "getSeatHold": [
  "SELECT * FROM seating.seat_hold LIMIT 50"
 ],
 "getSeatMap": [
  "SELECT * FROM seating.seat_map LIMIT 50",
  "SELECT * FROM seating.section WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getSeatMapImport": [
  "SELECT * FROM seating.seat_map LIMIT 50"
 ],
 "getSeatingRules": [
  "SELECT * FROM seating.seating_rules LIMIT 50"
 ],
 "getUpsellSuggestions": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM promotions.upsell_rule LIMIT 50"
 ],
 "importProductCatalogue": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "importSeatGeometry": [
  "SELECT * FROM seating.import_job LIMIT 50"
 ],
 "importSeatManifest": [
  "SELECT * FROM seating.import_job LIMIT 50"
 ],
 "importSeatMap": [
  "SELECT * FROM assets.media_asset LIMIT 50",
  "SELECT * FROM seating.seat_map_template LIMIT 50"
 ],
 "joinWaitlist": [
  "SELECT * FROM catalogue.channel_capacity LIMIT 50",
  "SELECT * FROM catalogue.performance LIMIT 50"
 ],
 "leaveWaitlist": [
  "SELECT * FROM catalogue.waitlist_entry LIMIT 50"
 ],
 "listAllocationSplits": [
  "SELECT * FROM promotions.allocation_component LIMIT 50",
  "SELECT * FROM promotions.allocation_split LIMIT 50"
 ],
 "listAlternativeCodes": [
  "SELECT * FROM catalogue.alternative_code LIMIT 50"
 ],
 "listBundles": [
  "SELECT * FROM promotions.bundle LIMIT 50"
 ],
 "listCatalogueBundles": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.published_bundle LIMIT 50"
 ],
 "listChannelCapacities": [
  "SELECT * FROM catalogue.channel_capacity LIMIT 50"
 ],
 "listCouponCampaigns": [
  "SELECT * FROM promotions.coupon_campaign LIMIT 50"
 ],
 "listCouponCodes": [
  "SELECT * FROM promotions.coupon_code WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listDonationCampaigns": [
  "SELECT * FROM catalogue.donation_campaign LIMIT 50"
 ],
 "listEntitlementTemplates": [
  "SELECT * FROM catalogue.entitlement_template WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listEvents": [
  "SELECT * FROM catalogue.event WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listGuestMemberships": [
  "SELECT * FROM catalogue.entitlement_template WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listInventoryHolds": [
  "SELECT * FROM catalogue.inventory_hold LIMIT 50"
 ],
 "listPerformances": [
  "SELECT * FROM catalogue.performance LIMIT 50"
 ],
 "listPriceLists": [
  "SELECT * FROM catalogue.price_list LIMIT 50"
 ],
 "listPrices": [
  "SELECT * FROM catalogue.price LIMIT 50"
 ],
 "listProductCategories": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.product_category WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listProductVariants": [
  "SELECT * FROM catalogue.variant LIMIT 50"
 ],
 "listProductVersions": [
  "SELECT * FROM catalogue.product_version LIMIT 50"
 ],
 "listProducts": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listPromotions": [
  "SELECT * FROM promotions.promotion LIMIT 50"
 ],
 "listSeatBlocks": [
  "SELECT * FROM seating.seat_block WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listSeatCategories": [
  "SELECT * FROM seating.seat_category LIMIT 50"
 ],
 "listSeatMapTemplates": [
  "SELECT * FROM seating.seat_map_template LIMIT 50"
 ],
 "listSeatMaps": [
  "SELECT * FROM seating.seat_map LIMIT 50"
 ],
 "listSeats": [
  "SELECT * FROM seating.seat LIMIT 50"
 ],
 "listUpsellRules": [
  "SELECT * FROM promotions.upsell_rule LIMIT 50"
 ],
 "listVoucherBatches": [
  "SELECT * FROM promotions.voucher_batch LIMIT 50"
 ],
 "listWaitlistEntries": [
  "SELECT * FROM catalogue.performance LIMIT 50",
  "SELECT * FROM catalogue.waitlist_entry LIMIT 50"
 ],
 "offerWaitlistCapacity": [
  "SELECT * FROM catalogue.channel_capacity LIMIT 50",
  "SELECT * FROM catalogue.waitlist_entry LIMIT 50"
 ],
 "pausePromotion": [
  "SELECT * FROM promotions.promotion LIMIT 50"
 ],
 "previewAllocationSplit": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM promotions.allocation_component LIMIT 50"
 ],
 "publishBundle": [
  "SELECT * FROM catalogue.published_bundle LIMIT 50"
 ],
 "publishPromotion": [
  "SELECT * FROM promotions.promotion LIMIT 50"
 ],
 "publishSeatMap": [
  "SELECT * FROM seating.seat_map LIMIT 50",
  "SELECT * FROM seating.section WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "recommendSeats": [
  "SELECT * FROM catalogue.performance LIMIT 50"
 ],
 "redeemVoucher": [
  "SELECT * FROM promotions.voucher LIMIT 50"
 ],
 "reinstateEntitlement": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "releaseChannelAllocation": [
  "SELECT * FROM catalogue.channel_allocation LIMIT 50"
 ],
 "releaseInventoryHold": [
  "SELECT * FROM catalogue.inventory_hold LIMIT 50"
 ],
 "releaseSeatBlock": [
  "SELECT * FROM seating.seat_block WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "releaseSeatHold": [
  "SELECT * FROM seating.seat_hold LIMIT 50"
 ],
 "relinquishInventoryHold": [
  "SELECT * FROM catalogue.inventory_hold LIMIT 50"
 ],
 "renewInventoryHold": [
  "SELECT * FROM catalogue.inventory_hold LIMIT 50"
 ],
 "reportBundleApplied": [
  "SELECT * FROM catalogue.published_bundle LIMIT 50"
 ],
 "resolveProductByCode": [
  "SELECT * FROM catalogue.variant LIMIT 50"
 ],
 "restoreProductVersion": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.product_version LIMIT 50"
 ],
 "searchCatalogue": [
  "SELECT * FROM catalogue.event WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.variant LIMIT 50"
 ],
 "setAlternativeCodes": [
  "SELECT * FROM catalogue.alternative_code LIMIT 50"
 ],
 "setChannelAllocations": [
  "SELECT * FROM catalogue.channel_allocation LIMIT 50"
 ],
 "setMapZones": [
  "SELECT * FROM seating.seat LIMIT 50",
  "SELECT * FROM seating.seat_map LIMIT 50"
 ],
 "setPrices": [
  "SELECT * FROM catalogue.price_list LIMIT 50"
 ],
 "setProductAttributes": [
  "SELECT * FROM catalogue.variant_dimension LIMIT 50"
 ],
 "setProductCategories": [
  "SELECT * FROM catalogue.product_category WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setPromotionVariants": [
  "SELECT * FROM promotions.promotion LIMIT 50"
 ],
 "setSeatingRules": [
  "SELECT * FROM seating.seating_rules LIMIT 50"
 ],
 "simulatePromotion": [
  "SELECT * FROM catalogue.price LIMIT 50",
  "SELECT * FROM orders.order_line LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM promotions.promotion LIMIT 50"
 ],
 "suspendEntitlement": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.entitlement_template WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "transitionProductLifecycle": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "unschedulePromotion": [
  "SELECT * FROM promotions.promotion LIMIT 50"
 ],
 "updateBundle": [
  "SELECT * FROM promotions.allocation_component LIMIT 50",
  "SELECT * FROM promotions.bundle LIMIT 50",
  "SELECT * FROM promotions.bundle_component LIMIT 50"
 ],
 "updateChannelCapacity": [
  "SELECT * FROM catalogue.channel_capacity LIMIT 50"
 ],
 "updateDonationCampaign": [
  "SELECT * FROM catalogue.donation_campaign LIMIT 50"
 ],
 "updateEvent": [
  "SELECT * FROM catalogue.event WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "updatePerformance": [
  "SELECT * FROM catalogue.performance LIMIT 50"
 ],
 "updatePriceList": [
  "SELECT * FROM catalogue.price_list LIMIT 50"
 ],
 "updateProduct": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "updatePromotion": [
  "SELECT * FROM promotions.promotion LIMIT 50"
 ],
 "updateSeatMap": [
  "SELECT * FROM seating.seat_map LIMIT 50",
  "SELECT * FROM seating.section WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "updateSeats": [
  "SELECT * FROM seating.seat_map LIMIT 50"
 ],
 "validateSeatMap": [
  "SELECT * FROM seating.seat_map LIMIT 50"
 ],
 "voidCouponCode": [
  "SELECT * FROM promotions.coupon_code WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "voidVoucher": [
  "SELECT * FROM promotions.voucher LIMIT 50"
 ]
}

WRITES = {
 "acquireInventoryHold": [
  "SELECT id FROM catalogue.inventory_hold ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "allocateBlockedSeats": [
  "SELECT id FROM seating.seat_hold ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "assignCoupon": [
  "SELECT id FROM promotions.coupon_code WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "assignSeats": [
  "SELECT id FROM seating.seat ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM seating.seat_hold ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "bulkChangePrices": [
  "SELECT id FROM catalogue.price_list ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM catalogue.product_version ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "cancelPerformance": [
  "SELECT id FROM catalogue.performance ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.outbox WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "cloneProduct": [
  "SELECT id FROM catalogue.product WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM catalogue.variant ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "cloneSeatMap": [
  "SELECT id FROM seating.seat_map ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM seating.section WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "commitCatalogueImport": [
  "SELECT id FROM catalogue.import_job WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM catalogue.product WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "commitImportJob": [
  "SELECT id FROM seating.import_job ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "copyPriceList": [
  "SELECT id FROM catalogue.price_list ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "copySeatMapSection": [
  "SELECT id FROM seating.section WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createBundle": [
  "SELECT id FROM promotions.allocation_component ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM promotions.bundle ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createChannelCapacity": [
  "SELECT id FROM catalogue.channel_capacity ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createCouponCampaign": [
  "SELECT id FROM promotions.coupon_campaign ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createDonationCampaign": [
  "SELECT id FROM catalogue.donation_campaign ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createEntitlementTemplate": [
  "SELECT id FROM catalogue.entitlement_template WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createEvent": [
  "SELECT id FROM catalogue.event WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createPerformances": [
  "SELECT id FROM catalogue.performance ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createPriceList": [
  "SELECT id FROM catalogue.price_list ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createProduct": [
  "SELECT id FROM catalogue.product WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createPromotion": [
  "SELECT id FROM promotions.promotion ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createSeatBlock": [
  "SELECT id FROM seating.seat_block WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createSeatCategory": [
  "SELECT id FROM seating.seat_category ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createSeatHold": [
  "SELECT id FROM seating.seat_hold ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createSeatMap": [
  "SELECT id FROM seating.seat_map ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM seating.section WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createSeatMapTemplate": [
  "SELECT id FROM seating.seat_map_template ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createUpsellRule": [
  "SELECT id FROM promotions.upsell_rule ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createVoucherBatch": [
  "SELECT id FROM promotions.voucher_batch ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "deleteUpsellRule": [
  "SELECT id FROM promotions.upsell_rule ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "endPromotion": [
  "SELECT id FROM promotions.promotion ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "extendSeatHold": [
  "SELECT id FROM seating.seat_hold ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "forceReleaseInventoryHold": [
  "SELECT id FROM catalogue.inventory_hold ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "freezeEntitlement": [
  "SELECT id FROM access.entitlement WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "generateCouponCodes": [
  "SELECT id FROM promotions.coupon_code WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "importProductCatalogue": [
  "SELECT id FROM catalogue.import_job WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "importSeatGeometry": [
  "SELECT id FROM seating.import_job ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "importSeatManifest": [
  "SELECT id FROM seating.import_job ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "importSeatMap": [
  "SELECT id FROM seating.seat_map ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM seating.section WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "joinWaitlist": [
  "SELECT id FROM catalogue.waitlist_entry ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "leaveWaitlist": [
  "SELECT id FROM catalogue.waitlist_entry ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "offerWaitlistCapacity": [
  "SELECT id FROM catalogue.inventory_hold ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM catalogue.waitlist_entry ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "pausePromotion": [
  "SELECT id FROM promotions.promotion ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "publishBundle": [
  "SELECT id FROM catalogue.published_bundle ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "publishPromotion": [
  "SELECT id FROM promotions.promotion ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "publishSeatMap": [
  "SELECT id FROM seating.seat_map ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM seating.section WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "redeemVoucher": [
  "SELECT id FROM promotions.voucher ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reinstateEntitlement": [
  "SELECT id FROM access.entitlement WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "releaseChannelAllocation": [
  "SELECT id FROM catalogue.channel_allocation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "releaseInventoryHold": [
  "SELECT id FROM catalogue.inventory_hold ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "releaseSeatBlock": [
  "SELECT id FROM seating.seat_block WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "releaseSeatHold": [
  "SELECT id FROM seating.seat_hold ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "renewInventoryHold": [
  "SELECT id FROM catalogue.inventory_hold ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reportBundleApplied": [
  "SELECT id FROM catalogue.published_bundle ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "restoreProductVersion": [
  "SELECT id FROM catalogue.product WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM catalogue.product_version ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setAlternativeCodes": [
  "SELECT id FROM catalogue.alternative_code ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setChannelAllocations": [
  "SELECT id FROM catalogue.channel_allocation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setMapZones": [
  "SELECT id FROM seating.zone ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setPrices": [
  "SELECT id FROM catalogue.price_list ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setProductAttributes": [
  "SELECT id FROM catalogue.variant_dimension ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setProductCategories": [
  "SELECT id FROM catalogue.product_category WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setPromotionVariants": [
  "SELECT id FROM promotions.promotion ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setSeatingRules": [
  "SELECT id FROM seating.seating_rules ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "suspendEntitlement": [
  "SELECT id FROM access.entitlement WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "transitionProductLifecycle": [
  "SELECT id FROM catalogue.product WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.outbox WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "unschedulePromotion": [
  "SELECT id FROM promotions.promotion ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateBundle": [
  "SELECT id FROM promotions.allocation_component ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM promotions.bundle ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateChannelCapacity": [
  "SELECT id FROM catalogue.channel_capacity ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateDonationCampaign": [
  "SELECT id FROM catalogue.donation_campaign ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateEvent": [
  "SELECT id FROM catalogue.event WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updatePerformance": [
  "SELECT id FROM catalogue.performance ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updatePriceList": [
  "SELECT id FROM catalogue.price_list ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateProduct": [
  "SELECT id FROM catalogue.product WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updatePromotion": [
  "SELECT id FROM promotions.promotion ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateSeatMap": [
  "SELECT id FROM seating.seat_map ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM seating.section WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateSeats": [
  "SELECT id FROM seating.seat_map ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "validateSeatMap": [
  "SELECT id FROM seating.seat_map ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "voidCouponCode": [
  "SELECT id FROM promotions.coupon_code WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "voidVoucher": [
  "SELECT id FROM promotions.voucher ORDER BY id LIMIT 1 FOR UPDATE"
 ]
}

CACHE = {
 "acquireInventoryHold": [
  "cache:idempotency:bench"
 ],
 "allocateBlockedSeats": [
  "cache:idempotency:bench"
 ],
 "assignCoupon": [
  "cache:idempotency:bench"
 ],
 "assignSeats": [
  "cache:idempotency:bench"
 ],
 "bulkChangePrices": [
  "cache:idempotency:bench"
 ],
 "cancelPerformance": [
  "cache:idempotency:bench"
 ],
 "cloneProduct": [
  "cache:idempotency:bench"
 ],
 "cloneSeatMap": [
  "cache:idempotency:bench"
 ],
 "commitCatalogueImport": [
  "cache:idempotency:bench"
 ],
 "commitImportJob": [
  "cache:idempotency:bench"
 ],
 "copyPriceList": [
  "cache:idempotency:bench"
 ],
 "copySeatMapSection": [
  "cache:idempotency:bench"
 ],
 "createBundle": [
  "cache:idempotency:bench"
 ],
 "createChannelCapacity": [
  "cache:idempotency:bench"
 ],
 "createCouponCampaign": [
  "cache:idempotency:bench"
 ],
 "createDonationCampaign": [
  "cache:idempotency:bench"
 ],
 "createEntitlementTemplate": [
  "cache:idempotency:bench"
 ],
 "createEvent": [
  "cache:idempotency:bench"
 ],
 "createPerformances": [
  "cache:idempotency:bench"
 ],
 "createPriceList": [
  "cache:idempotency:bench"
 ],
 "createProduct": [
  "cache:idempotency:bench"
 ],
 "createPromotion": [
  "cache:idempotency:bench"
 ],
 "createSeatBlock": [
  "cache:idempotency:bench"
 ],
 "createSeatCategory": [
  "cache:idempotency:bench"
 ],
 "createSeatHold": [
  "cache:idempotency:bench"
 ],
 "createSeatMap": [
  "cache:idempotency:bench"
 ],
 "createSeatMapTemplate": [
  "cache:idempotency:bench"
 ],
 "createUpsellRule": [
  "cache:idempotency:bench"
 ],
 "createVoucherBatch": [
  "cache:idempotency:bench"
 ],
 "deleteUpsellRule": [
  "cache:idempotency:bench"
 ],
 "endPromotion": [
  "cache:idempotency:bench"
 ],
 "evaluatePromotions": [
  "cache:idempotency:bench"
 ],
 "extendSeatHold": [
  "cache:idempotency:bench"
 ],
 "forceReleaseInventoryHold": [
  "cache:idempotency:bench"
 ],
 "freezeEntitlement": [
  "cache:idempotency:bench"
 ],
 "generateCouponCodes": [
  "cache:idempotency:bench"
 ],
 "getUpsellSuggestions": [
  "cache:idempotency:bench"
 ],
 "importProductCatalogue": [
  "cache:idempotency:bench"
 ],
 "importSeatGeometry": [
  "cache:idempotency:bench"
 ],
 "importSeatManifest": [
  "cache:idempotency:bench"
 ],
 "importSeatMap": [
  "cache:idempotency:bench"
 ],
 "joinWaitlist": [
  "cache:idempotency:bench"
 ],
 "leaveWaitlist": [
  "cache:idempotency:bench"
 ],
 "listPrices": [
  "cache:resolution:bench"
 ],
 "offerWaitlistCapacity": [
  "cache:idempotency:bench"
 ],
 "pausePromotion": [
  "cache:idempotency:bench"
 ],
 "previewAllocationSplit": [
  "cache:idempotency:bench"
 ],
 "publishBundle": [
  "cache:idempotency:bench"
 ],
 "publishPromotion": [
  "cache:idempotency:bench"
 ],
 "publishSeatMap": [
  "cache:idempotency:bench"
 ],
 "redeemVoucher": [
  "cache:idempotency:bench"
 ],
 "reinstateEntitlement": [
  "cache:idempotency:bench"
 ],
 "releaseChannelAllocation": [
  "cache:idempotency:bench"
 ],
 "releaseInventoryHold": [
  "cache:idempotency:bench"
 ],
 "releaseSeatBlock": [
  "cache:idempotency:bench"
 ],
 "releaseSeatHold": [
  "cache:idempotency:bench"
 ],
 "renewInventoryHold": [
  "cache:idempotency:bench"
 ],
 "reportBundleApplied": [
  "cache:idempotency:bench"
 ],
 "restoreProductVersion": [
  "cache:idempotency:bench"
 ],
 "setAlternativeCodes": [
  "cache:idempotency:bench"
 ],
 "setChannelAllocations": [
  "cache:idempotency:bench"
 ],
 "setMapZones": [
  "cache:idempotency:bench"
 ],
 "setPrices": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setProductAttributes": [
  "cache:idempotency:bench"
 ],
 "setProductCategories": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setPromotionVariants": [
  "cache:idempotency:bench"
 ],
 "setSeatingRules": [
  "cache:idempotency:bench"
 ],
 "suspendEntitlement": [
  "cache:idempotency:bench"
 ],
 "transitionProductLifecycle": [
  "cache:idempotency:bench"
 ],
 "unschedulePromotion": [
  "cache:idempotency:bench"
 ],
 "updateBundle": [
  "cache:idempotency:bench"
 ],
 "updateChannelCapacity": [
  "cache:idempotency:bench"
 ],
 "updateDonationCampaign": [
  "cache:idempotency:bench"
 ],
 "updateEvent": [
  "cache:idempotency:bench"
 ],
 "updatePerformance": [
  "cache:idempotency:bench"
 ],
 "updatePriceList": [
  "cache:idempotency:bench"
 ],
 "updateProduct": [
  "cache:idempotency:bench"
 ],
 "updatePromotion": [
  "cache:idempotency:bench"
 ],
 "updateSeatMap": [
  "cache:idempotency:bench"
 ],
 "updateSeats": [
  "cache:idempotency:bench"
 ],
 "validateSeatMap": [
  "cache:idempotency:bench"
 ],
 "voidCouponCode": [
  "cache:idempotency:bench"
 ],
 "voidVoucher": [
  "cache:idempotency:bench"
 ]
}
