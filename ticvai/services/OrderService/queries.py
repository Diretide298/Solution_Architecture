"""Generated. The declared reads and writes of each operation."""

READS = {
 "abandonCart": [
  "SELECT * FROM orders.cart LIMIT 50"
 ],
 "acceptShiftVariance": [
  "SELECT * FROM orders.shift WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "addCartLine": [
  "SELECT * FROM catalogue.channel_capacity LIMIT 50",
  "SELECT * FROM catalogue.performance LIMIT 50",
  "SELECT * FROM catalogue.variant LIMIT 50"
 ],
 "addTip": [
  "SELECT * FROM orders.payment LIMIT 50"
 ],
 "adjustDepositBoxFloat": [
  "SELECT * FROM orders.deposit_box LIMIT 50"
 ],
 "allocateDepositBox": [
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM platform.workstation WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "appendEntitlementToMedia": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.order_line LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "applyManualDiscount": [
  "SELECT * FROM orders.order_line LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "approveRefund": [
  "SELECT * FROM orders.refund LIMIT 50"
 ],
 "approveShiftOpen": [
  "SELECT * FROM orders.shift WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "authoriseStoredValue": [
  "SELECT * FROM promotions.voucher LIMIT 50",
  "SELECT * FROM retail.gift_card LIMIT 50",
  "SELECT * FROM retail.wallet LIMIT 50"
 ],
 "cancelReservation": [
  "SELECT * FROM orders.reservation LIMIT 50"
 ],
 "capturePayment": [
  "SELECT * FROM ledger.fx_rate LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50"
 ],
 "captureStoredValue": [
  "SELECT * FROM orders.stored_value_authorisation WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "checkoutCart": [
  "SELECT * FROM catalogue.inventory_hold LIMIT 50",
  "SELECT * FROM orders.cart LIMIT 50",
  "SELECT * FROM orders.cart_line LIMIT 50"
 ],
 "claimCart": [
  "SELECT * FROM orders.cart LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "claimTicketTransfer": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.ticket_transfer LIMIT 50"
 ],
 "closeDepositBoxes": [
  "SELECT * FROM ledger.fx_rate LIMIT 50",
  "SELECT * FROM orders.cash_count_line LIMIT 50",
  "SELECT * FROM orders.deposit_box LIMIT 50"
 ],
 "closeShift": [
  "SELECT * FROM ledger.fx_rate LIMIT 50",
  "SELECT * FROM orders.cash_count_line LIMIT 50",
  "SELECT * FROM orders.cash_movement LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50",
  "SELECT * FROM orders.shift WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM platform.venue_settings LIMIT 50"
 ],
 "convertReservation": [
  "SELECT * FROM orders.order_line LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "convertToTermProduct": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createBulkRefund": [
  "SELECT * FROM orders.refund LIMIT 50"
 ],
 "createCart": [
  "SELECT * FROM pii.subject LIMIT 50",
  "SELECT * FROM platform.org_unit LIMIT 50"
 ],
 "createCashMovement": [
  "SELECT * FROM orders.cash_count_line LIMIT 50",
  "SELECT * FROM orders.cash_movement LIMIT 50"
 ],
 "createOrder": [
  "SELECT * FROM orders.order_line LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createPayment": [
  "SELECT * FROM ledger.fx_rate LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createPaymentLink": [
  "SELECT * FROM orders.payment_provider WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createRefund": [
  "SELECT * FROM orders.payment LIMIT 50",
  "SELECT * FROM orders.refund LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createRefundRequest": [
  "SELECT * FROM orders.refund_policy LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createResaleListing": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.entitlement_template WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createReservation": [
  "SELECT * FROM orders.reservation LIMIT 50"
 ],
 "exchangeOrderLines": [
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "extendCart": [
  "SELECT * FROM catalogue.inventory_hold LIMIT 50",
  "SELECT * FROM orders.cart LIMIT 50"
 ],
 "extendReservation": [
  "SELECT * FROM orders.reservation LIMIT 50"
 ],
 "getB2bCredit": [
  "SELECT * FROM orders.b2b_credit WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getCart": [
  "SELECT * FROM catalogue.channel_capacity LIMIT 50",
  "SELECT * FROM catalogue.inventory_hold LIMIT 50",
  "SELECT * FROM orders.cart LIMIT 50",
  "SELECT * FROM orders.cart_line LIMIT 50",
  "SELECT * FROM promotions.promotion LIMIT 50"
 ],
 "getCurrentShift": [
  "SELECT * FROM orders.shift WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getGroupBooking": [
  "SELECT * FROM orders.group_booking LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "getMediaEntitlements": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM access.scan_event WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.entitlement_template WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "getOrder": [
  "SELECT * FROM orders.order_line LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getOrderStatement": [
  "SELECT * FROM ledger.posting LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50",
  "SELECT * FROM orders.refund LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getPaymentLink": [
  "SELECT * FROM orders.order_line LIMIT 50",
  "SELECT * FROM orders.payment_link WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.reservation LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM platform.org_unit LIMIT 50"
 ],
 "getRefundPolicy": [
  "SELECT * FROM orders.refund_policy LIMIT 50"
 ],
 "getReservation": [
  "SELECT * FROM orders.reservation LIMIT 50"
 ],
 "getShift": [
  "SELECT * FROM orders.shift WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "holdOrder": [
  "SELECT * FROM orders.order_line LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "inquirePaymentStatus": [
  "SELECT * FROM orders.payment LIMIT 50"
 ],
 "issueInvitation": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM orders.invitation_allowance LIMIT 50"
 ],
 "issueWalletPass": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.ticket_template LIMIT 50"
 ],
 "listAbandonedCarts": [
  "SELECT * FROM orders.cart LIMIT 50",
  "SELECT * FROM orders.cart_line LIMIT 50",
  "SELECT * FROM pii.subject_contact LIMIT 50"
 ],
 "listCashMovements": [
  "SELECT * FROM orders.cash_count_line LIMIT 50",
  "SELECT * FROM orders.cash_movement LIMIT 50"
 ],
 "listChargebacks": [
  "SELECT * FROM orders.chargeback LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50"
 ],
 "listDenominations": [
  "SELECT * FROM platform.denomination LIMIT 50",
  "SELECT * FROM platform.region_settings LIMIT 50"
 ],
 "listDepositBoxes": [
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM orders.deposit_box LIMIT 50"
 ],
 "listFraudRules": [
  "SELECT * FROM orders.fraud_rule WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listInvitationAllowances": [
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM orders.invitation_allowance LIMIT 50"
 ],
 "listMyOrders": [
  "SELECT * FROM orders.order_line LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "listOrderRefunds": [
  "SELECT * FROM orders.refund LIMIT 50"
 ],
 "listOrders": [
  "SELECT * FROM orders.order_line LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listPaymentProviders": [
  "SELECT * FROM orders.payment_provider WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.payment_routing WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listPaymentTokens": [
  "SELECT * FROM orders.payment_token LIMIT 50"
 ],
 "listReservations": [
  "SELECT * FROM orders.reservation LIMIT 50"
 ],
 "listShifts": [
  "SELECT * FROM orders.shift WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listSyncRejections": [
  "SELECT * FROM sync.rejection LIMIT 50"
 ],
 "modifyOrder": [
  "SELECT * FROM orders.order_line LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "openGuestCreditAccount": [
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "openShift": [
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM orders.cash_count_line LIMIT 50",
  "SELECT * FROM orders.shift WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM platform.venue_settings LIMIT 50",
  "SELECT * FROM platform.workstation WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "overrideCreditLimit": [
  "SELECT * FROM orders.b2b_credit WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.credit_override LIMIT 50"
 ],
 "payByLink": [
  "SELECT * FROM orders.payment_link WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.payment_provider WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.reservation LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "printTicketProof": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.ticket_template LIMIT 50"
 ],
 "pushWalletPassUpdate": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.wallet_pass WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "quoteUpgrade": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.price LIMIT 50",
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "recordNoSale": [
  "SELECT * FROM orders.no_sale_event LIMIT 50"
 ],
 "reissueEntitlement": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "releaseStoredValue": [
  "SELECT * FROM orders.stored_value_authorisation WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "relinquishStoredValue": [
  "SELECT * FROM orders.stored_value_authorisation WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "removeCartLine": [
  "SELECT * FROM orders.cart_line LIMIT 50"
 ],
 "reopenShift": [
  "SELECT * FROM orders.shift WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "reprintOrder": [
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "rescheduleOrder": [
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "resendPaymentLink": [
  "SELECT * FROM orders.payment_link WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "respondToChargeback": [
  "SELECT * FROM access.scan_event WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.chargeback LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "resumeOrder": [
  "SELECT * FROM orders.order_line LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "resumeShift": [
  "SELECT * FROM orders.shift WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setB2bCreditLimit": [
  "SELECT * FROM orders.b2b_credit WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setFraudRules": [
  "SELECT * FROM orders.fraud_rule WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setPaymentProvider": [
  "SELECT * FROM orders.payment_provider WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setRefundPolicy": [
  "SELECT * FROM orders.refund_policy LIMIT 50"
 ],
 "shareEntitlement": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.entitlement_template WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.delegated_access WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "splitOrder": [
  "SELECT * FROM orders.order_line LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "storePaymentToken": [
  "SELECT * FROM marketing.consent_record LIMIT 50",
  "SELECT * FROM orders.payment_provider WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "suspendShift": [
  "SELECT * FROM orders.shift WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "syncOrders": [
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "transferOrderTickets": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.ticket_transfer LIMIT 50"
 ],
 "updateCartLine": [
  "SELECT * FROM catalogue.channel_capacity LIMIT 50",
  "SELECT * FROM orders.cart_line LIMIT 50"
 ],
 "voidOrder": [
  "SELECT * FROM orders.order_line LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "voidPayment": [
  "SELECT * FROM orders.payment LIMIT 50"
 ],
 "withdrawFromDepositBox": [
  "SELECT * FROM orders.deposit_box LIMIT 50"
 ]
}

WRITES = {
 "abandonCart": [
  "SELECT id FROM catalogue.inventory_hold ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.cart ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "acceptShiftVariance": [
  "SELECT id FROM orders.shift WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.outbox WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "addCartLine": [
  "SELECT id FROM catalogue.inventory_hold ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.cart ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "addTip": [
  "SELECT id FROM orders.payment ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "adjustDepositBoxFloat": [
  "SELECT id FROM orders.cash_movement ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.deposit_box ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "allocateDepositBox": [
  "SELECT id FROM orders.cash_movement ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.deposit_box ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "appendEntitlementToMedia": [
  "SELECT id FROM access.entitlement WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.order_line ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "applyManualDiscount": [
  "SELECT id FROM orders.order_line ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.payment ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "approveRefund": [
  "SELECT id FROM orders.refund ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "approveShiftOpen": [
  "SELECT id FROM orders.shift WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "authoriseStoredValue": [
  "SELECT id FROM orders.stored_value_authorisation WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "cancelReservation": [
  "SELECT id FROM orders.reservation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "capturePayment": [
  "SELECT id FROM orders.payment ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.outbox WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "captureStoredValue": [
  "SELECT id FROM orders.stored_value_authorisation WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM retail.wallet_transaction ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "checkoutCart": [
  "SELECT id FROM orders.cart ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.order_line ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "claimCart": [
  "SELECT id FROM orders.cart ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.cart_line ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "claimTicketTransfer": [
  "SELECT id FROM access.entitlement WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.ticket_transfer ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "closeDepositBoxes": [
  "SELECT id FROM ledger.posting ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.deposit_box ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "closeShift": [
  "SELECT id FROM ledger.journal_entry ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.cash_count_line ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "convertReservation": [
  "SELECT id FROM orders.order_line ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.payment ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "convertToTermProduct": [
  "SELECT id FROM orders.sales_order WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createBulkRefund": [
  "SELECT id FROM orders.refund ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createCart": [
  "SELECT id FROM orders.cart ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createCashMovement": [
  "SELECT id FROM orders.cash_count_line ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.cash_movement ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createOrder": [
  "SELECT id FROM orders.order_line ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.payment ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createPayment": [
  "SELECT id FROM ledger.journal_entry ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM ledger.posting ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createPaymentLink": [
  "SELECT id FROM marketing.message_dispatch ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.sales_order WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createRefund": [
  "SELECT id FROM ledger.journal_entry ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM ledger.posting ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createRefundRequest": [
  "SELECT id FROM orders.refund ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createResaleListing": [
  "SELECT id FROM orders.resale_listing WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createReservation": [
  "SELECT id FROM orders.reservation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "exchangeOrderLines": [
  "SELECT id FROM orders.sales_order WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "extendCart": [
  "SELECT id FROM catalogue.inventory_hold ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.cart ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "extendReservation": [
  "SELECT id FROM orders.reservation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "holdOrder": [
  "SELECT id FROM orders.order_line ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.payment ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "inquirePaymentStatus": [
  "SELECT id FROM orders.payment ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.outbox WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "issueInvitation": [
  "SELECT id FROM access.entitlement WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.invitation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "issueWalletPass": [
  "SELECT id FROM orders.wallet_pass WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "modifyOrder": [
  "SELECT id FROM orders.order_line ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.payment ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "openShift": [
  "SELECT id FROM orders.cash_count_line ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.shift WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "overrideCreditLimit": [
  "SELECT id FROM orders.b2b_credit WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.credit_override ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "payByLink": [
  "SELECT id FROM access.entitlement WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.payment ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "pushWalletPassUpdate": [
  "SELECT id FROM orders.wallet_pass WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordNoSale": [
  "SELECT id FROM orders.no_sale_event ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reissueEntitlement": [
  "SELECT id FROM access.entitlement WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "releaseStoredValue": [
  "SELECT id FROM orders.stored_value_authorisation WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "removeCartLine": [
  "SELECT id FROM catalogue.inventory_hold ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.cart_line ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reopenShift": [
  "SELECT id FROM orders.shift WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reprintOrder": [
  "SELECT id FROM orders.sales_order WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "rescheduleOrder": [
  "SELECT id FROM orders.sales_order WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "resendPaymentLink": [
  "SELECT id FROM marketing.message_dispatch ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.payment_link WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "respondToChargeback": [
  "SELECT id FROM ledger.posting ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.chargeback ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "resumeOrder": [
  "SELECT id FROM orders.order_line ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.payment ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "resumeShift": [
  "SELECT id FROM orders.shift WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setB2bCreditLimit": [
  "SELECT id FROM orders.b2b_credit WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setFraudRules": [
  "SELECT id FROM orders.fraud_rule WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setPaymentProvider": [
  "SELECT id FROM orders.payment_provider WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.payment_routing WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setRefundPolicy": [
  "SELECT id FROM orders.refund_policy ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "shareEntitlement": [
  "SELECT id FROM access.entitlement WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM identity.delegated_access WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "splitOrder": [
  "SELECT id FROM orders.order_line ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.sales_order WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "storePaymentToken": [
  "SELECT id FROM marketing.consent_record ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.payment_token ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "suspendShift": [
  "SELECT id FROM orders.shift WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "syncOrders": [
  "SELECT id FROM orders.sales_order WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "transferOrderTickets": [
  "SELECT id FROM access.entitlement WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.ticket_transfer ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateCartLine": [
  "SELECT id FROM catalogue.inventory_hold ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.cart_line ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "voidOrder": [
  "SELECT id FROM orders.order_line ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.payment ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "voidPayment": [
  "SELECT id FROM orders.payment ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "withdrawFromDepositBox": [
  "SELECT id FROM orders.cash_movement ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.deposit_box ORDER BY id LIMIT 1 FOR UPDATE"
 ]
}

CACHE = {
 "abandonCart": [
  "cache:idempotency:bench"
 ],
 "acceptShiftVariance": [
  "cache:idempotency:bench"
 ],
 "addCartLine": [
  "cache:idempotency:bench"
 ],
 "addTip": [
  "cache:idempotency:bench"
 ],
 "adjustDepositBoxFloat": [
  "cache:idempotency:bench"
 ],
 "allocateDepositBox": [
  "cache:idempotency:bench"
 ],
 "appendEntitlementToMedia": [
  "cache:idempotency:bench"
 ],
 "applyManualDiscount": [
  "cache:idempotency:bench"
 ],
 "approveRefund": [
  "cache:idempotency:bench"
 ],
 "approveShiftOpen": [
  "cache:idempotency:bench"
 ],
 "authoriseStoredValue": [
  "cache:idempotency:bench"
 ],
 "cancelReservation": [
  "cache:idempotency:bench"
 ],
 "capturePayment": [
  "cache:idempotency:bench"
 ],
 "captureStoredValue": [
  "cache:idempotency:bench"
 ],
 "checkoutCart": [
  "cache:idempotency:bench"
 ],
 "claimCart": [
  "cache:idempotency:bench"
 ],
 "claimTicketTransfer": [
  "cache:idempotency:bench"
 ],
 "closeDepositBoxes": [
  "cache:idempotency:bench"
 ],
 "closeShift": [
  "cache:idempotency:bench"
 ],
 "convertReservation": [
  "cache:idempotency:bench"
 ],
 "convertToTermProduct": [
  "cache:idempotency:bench"
 ],
 "createBulkRefund": [
  "cache:idempotency:bench"
 ],
 "createCart": [
  "cache:idempotency:bench"
 ],
 "createCashMovement": [
  "cache:idempotency:bench"
 ],
 "createOrder": [
  "cache:idempotency:bench"
 ],
 "createPayment": [
  "cache:idempotency:bench"
 ],
 "createPaymentLink": [
  "cache:idempotency:bench"
 ],
 "createRefund": [
  "cache:idempotency:bench"
 ],
 "createRefundRequest": [
  "cache:idempotency:bench"
 ],
 "createResaleListing": [
  "cache:idempotency:bench"
 ],
 "createReservation": [
  "cache:idempotency:bench"
 ],
 "exchangeOrderLines": [
  "cache:idempotency:bench"
 ],
 "extendCart": [
  "cache:idempotency:bench"
 ],
 "extendReservation": [
  "cache:idempotency:bench"
 ],
 "getRefundPolicy": [
  "cache:resolution:bench"
 ],
 "holdOrder": [
  "cache:idempotency:bench"
 ],
 "inquirePaymentStatus": [
  "cache:idempotency:bench"
 ],
 "issueInvitation": [
  "cache:idempotency:bench"
 ],
 "issueWalletPass": [
  "cache:idempotency:bench"
 ],
 "modifyOrder": [
  "cache:idempotency:bench"
 ],
 "openGuestCreditAccount": [
  "cache:idempotency:bench"
 ],
 "openShift": [
  "cache:idempotency:bench"
 ],
 "overrideCreditLimit": [
  "cache:idempotency:bench"
 ],
 "payByLink": [
  "cache:idempotency:bench"
 ],
 "printTicketProof": [
  "cache:idempotency:bench"
 ],
 "pushWalletPassUpdate": [
  "cache:idempotency:bench"
 ],
 "recordNoSale": [
  "cache:idempotency:bench"
 ],
 "reissueEntitlement": [
  "cache:idempotency:bench"
 ],
 "releaseStoredValue": [
  "cache:idempotency:bench"
 ],
 "removeCartLine": [
  "cache:idempotency:bench"
 ],
 "reopenShift": [
  "cache:idempotency:bench"
 ],
 "reprintOrder": [
  "cache:idempotency:bench"
 ],
 "rescheduleOrder": [
  "cache:idempotency:bench"
 ],
 "resendPaymentLink": [
  "cache:idempotency:bench"
 ],
 "respondToChargeback": [
  "cache:idempotency:bench"
 ],
 "resumeOrder": [
  "cache:idempotency:bench"
 ],
 "resumeShift": [
  "cache:idempotency:bench"
 ],
 "setB2bCreditLimit": [
  "cache:idempotency:bench"
 ],
 "setFraudRules": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setPaymentProvider": [
  "cache:idempotency:bench"
 ],
 "setRefundPolicy": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "shareEntitlement": [
  "cache:idempotency:bench"
 ],
 "splitOrder": [
  "cache:idempotency:bench"
 ],
 "storePaymentToken": [
  "cache:idempotency:bench"
 ],
 "suspendShift": [
  "cache:idempotency:bench"
 ],
 "transferOrderTickets": [
  "cache:idempotency:bench"
 ],
 "updateCartLine": [
  "cache:idempotency:bench"
 ],
 "voidOrder": [
  "cache:idempotency:bench"
 ],
 "voidPayment": [
  "cache:idempotency:bench"
 ],
 "withdrawFromDepositBox": [
  "cache:idempotency:bench"
 ]
}
