"""Generated. The declared reads and writes of each operation."""

READS = {
 "acceptFnbOrder": [
  "SELECT * FROM fnb.fnb_order LIMIT 50"
 ],
 "amendFnbOrder": [
  "SELECT * FROM fnb.fnb_order LIMIT 50"
 ],
 "applyMenuActions": [
  "SELECT * FROM catalogue.price LIMIT 50",
  "SELECT * FROM fnb.menu LIMIT 50",
  "SELECT * FROM fnb.menu_item LIMIT 50"
 ],
 "attachModifierGroup": [
  "SELECT * FROM fnb.menu_item LIMIT 50",
  "SELECT * FROM fnb.modifier_group WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "buildProductionPlan": [
  "SELECT * FROM ai.suggestion WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM fnb.menu_item LIMIT 50",
  "SELECT * FROM fnb.recipe LIMIT 50"
 ],
 "cancelFnbOrder": [
  "SELECT * FROM fnb.fnb_order LIMIT 50"
 ],
 "chaseStation": [
  "SELECT * FROM fnb.kitchen_station LIMIT 50",
  "SELECT * FROM fnb.kitchen_ticket LIMIT 50"
 ],
 "claimLocationSession": [
  "SELECT * FROM fnb.location_session LIMIT 50"
 ],
 "claimTableSession": [
  "SELECT * FROM fnb.table_session LIMIT 50"
 ],
 "clearTable": [
  "SELECT * FROM fnb.table LIMIT 50"
 ],
 "closeCorrectiveAction": [
  "SELECT * FROM fnb.corrective_action WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "closeTableVisit": [
  "SELECT * FROM fnb.fnb_order LIMIT 50",
  "SELECT * FROM fnb.table_visit LIMIT 50"
 ],
 "compItem": [
  "SELECT * FROM fnb.table_visit LIMIT 50",
  "SELECT * FROM orders.order_line LIMIT 50"
 ],
 "completeProductionRun": [
  "SELECT * FROM fnb.production_run LIMIT 50",
  "SELECT * FROM fnb.recipe LIMIT 50"
 ],
 "createCombo": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM fnb.menu_item LIMIT 50"
 ],
 "createFnbOrder": [
  "SELECT * FROM fnb.fnb_order LIMIT 50"
 ],
 "createGuestFnbOrder": [
  "SELECT * FROM fnb.location_session LIMIT 50",
  "SELECT * FROM fnb.menu_item LIMIT 50",
  "SELECT * FROM inventory.stock_level LIMIT 50"
 ],
 "createMenu": [
  "SELECT * FROM fnb.menu LIMIT 50",
  "SELECT * FROM fnb.menu_item LIMIT 50",
  "SELECT * FROM fnb.menu_section LIMIT 50"
 ],
 "createModifierGroup": [
  "SELECT * FROM fnb.modifier_group WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createTableReservation": [
  "SELECT * FROM fnb.table LIMIT 50",
  "SELECT * FROM fnb.table_reservation LIMIT 50"
 ],
 "enterCountLine": [
  "SELECT * FROM inventory.item LIMIT 50",
  "SELECT * FROM inventory.movement LIMIT 50"
 ],
 "escalateCorrectiveAction": [
  "SELECT * FROM fnb.corrective_action WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "fireCourse": [
  "SELECT * FROM fnb.kitchen_ticket LIMIT 50"
 ],
 "getBill": [
  "SELECT * FROM fnb.fnb_order LIMIT 50",
  "SELECT * FROM fnb.table_session LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50"
 ],
 "getFnbOrder": [
  "SELECT * FROM fnb.fnb_order LIMIT 50"
 ],
 "getGuestBill": [
  "SELECT * FROM fnb.fnb_order LIMIT 50",
  "SELECT * FROM fnb.table_session LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50"
 ],
 "getGuestMenu": [
  "SELECT * FROM fnb.modifier_group WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getGuestOrderStatus": [
  "SELECT * FROM fnb.delivery_location LIMIT 50",
  "SELECT * FROM fnb.fnb_order LIMIT 50",
  "SELECT * FROM fnb.kitchen_ticket LIMIT 50"
 ],
 "getHaccpStatus": [
  "SELECT * FROM fnb.cold_chain_event LIMIT 50",
  "SELECT * FROM fnb.corrective_action WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM fnb.temperature_log LIMIT 50"
 ],
 "getMenu": [
  "SELECT * FROM fnb.menu LIMIT 50",
  "SELECT * FROM fnb.menu_item LIMIT 50",
  "SELECT * FROM fnb.menu_section LIMIT 50"
 ],
 "getProductionRun": [
  "SELECT * FROM fnb.production_run LIMIT 50",
  "SELECT * FROM fnb.recipe LIMIT 50",
  "SELECT * FROM inventory.movement LIMIT 50"
 ],
 "getTableMap": [
  "SELECT * FROM fnb.table LIMIT 50"
 ],
 "getTableVisit": [
  "SELECT * FROM fnb.fnb_order LIMIT 50",
  "SELECT * FROM fnb.table_visit LIMIT 50"
 ],
 "holdCourse": [
  "SELECT * FROM fnb.kitchen_ticket LIMIT 50"
 ],
 "joinRestaurantWaitlist": [
  "SELECT * FROM fnb.table LIMIT 50",
  "SELECT * FROM platform.outlet LIMIT 50"
 ],
 "list86Events": [
  "SELECT * FROM fnb.eighty_six_event LIMIT 50",
  "SELECT * FROM fnb.menu_item LIMIT 50"
 ],
 "listDeliveryLocations": [
  "SELECT * FROM fnb.delivery_location LIMIT 50"
 ],
 "listDiningOutlets": [
  "SELECT * FROM fnb.fnb_order LIMIT 50",
  "SELECT * FROM fnb.menu LIMIT 50",
  "SELECT * FROM platform.outlet LIMIT 50"
 ],
 "listFnbOrders": [
  "SELECT * FROM fnb.fnb_order LIMIT 50"
 ],
 "listKitchenStations": [
  "SELECT * FROM fnb.kitchen_station LIMIT 50"
 ],
 "listKitchenTickets": [
  "SELECT * FROM fnb.kitchen_ticket LIMIT 50"
 ],
 "listMenus": [
  "SELECT * FROM fnb.menu LIMIT 50",
  "SELECT * FROM fnb.menu_section LIMIT 50"
 ],
 "listModifierGroups": [
  "SELECT * FROM fnb.modifier_group WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listProductionRuns": [
  "SELECT * FROM fnb.production_run LIMIT 50",
  "SELECT * FROM fnb.recipe LIMIT 50",
  "SELECT * FROM inventory.movement LIMIT 50"
 ],
 "listRecipes": [
  "SELECT * FROM fnb.recipe LIMIT 50"
 ],
 "listTableReservations": [
  "SELECT * FROM fnb.table LIMIT 50",
  "SELECT * FROM fnb.table_reservation LIMIT 50"
 ],
 "logColdChain": [
  "SELECT * FROM fnb.cold_chain_event LIMIT 50",
  "SELECT * FROM inventory.goods_receipt LIMIT 50"
 ],
 "logKitchenException": [
  "SELECT * FROM fnb.kitchen_station LIMIT 50"
 ],
 "logTemperature": [
  "SELECT * FROM fnb.temperature_log LIMIT 50",
  "SELECT * FROM platform.org_unit LIMIT 50"
 ],
 "markOrderCollected": [
  "SELECT * FROM fnb.fnb_order LIMIT 50",
  "SELECT * FROM fnb.kitchen_ticket LIMIT 50"
 ],
 "mergeTableVisits": [
  "SELECT * FROM fnb.fnb_order LIMIT 50",
  "SELECT * FROM fnb.table_visit LIMIT 50"
 ],
 "moveTableVisit": [
  "SELECT * FROM fnb.kitchen_ticket LIMIT 50",
  "SELECT * FROM fnb.table LIMIT 50",
  "SELECT * FROM fnb.table_visit LIMIT 50"
 ],
 "notifyServer": [
  "SELECT * FROM fnb.table_visit LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "notifyWaitlistParty": [
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "openTableVisit": [
  "SELECT * FROM fnb.fnb_order LIMIT 50",
  "SELECT * FROM fnb.table_visit LIMIT 50"
 ],
 "planProductionRun": [
  "SELECT * FROM fnb.recipe LIMIT 50",
  "SELECT * FROM inventory.stock_level LIMIT 50",
  "SELECT * FROM platform.outlet LIMIT 50"
 ],
 "printOrderLabel": [
  "SELECT * FROM fnb.kitchen_ticket LIMIT 50"
 ],
 "prioritiseKitchenTicket": [
  "SELECT * FROM fnb.kitchen_ticket LIMIT 50"
 ],
 "publishMenu": [
  "SELECT * FROM fnb.menu LIMIT 50",
  "SELECT * FROM fnb.menu_section LIMIT 50"
 ],
 "quoteWaitTime": [
  "SELECT * FROM fnb.table LIMIT 50",
  "SELECT * FROM fnb.table_visit LIMIT 50"
 ],
 "reassignServer": [
  "SELECT * FROM fnb.table_visit LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "rebalanceStationLoad": [
  "SELECT * FROM fnb.kitchen_station LIMIT 50"
 ],
 "recallKitchenTicket": [
  "SELECT * FROM fnb.kitchen_ticket LIMIT 50"
 ],
 "recordCorrectiveAction": [
  "SELECT * FROM fnb.corrective_action WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "recordOrderHandover": [
  "SELECT * FROM fnb.delivery_location LIMIT 50",
  "SELECT * FROM fnb.fnb_order LIMIT 50"
 ],
 "recordWaste": [
  "SELECT * FROM fnb.menu_item LIMIT 50",
  "SELECT * FROM platform.outlet LIMIT 50"
 ],
 "refireItem": [
  "SELECT * FROM fnb.kitchen_ticket LIMIT 50",
  "SELECT * FROM fnb.kitchen_ticket_line LIMIT 50"
 ],
 "releaseProductionPlan": [
  "SELECT * FROM fnb.production_plan LIMIT 50"
 ],
 "requestBill": [
  "SELECT * FROM fnb.table_visit LIMIT 50"
 ],
 "resolveBookingConflict": [
  "SELECT * FROM fnb.table LIMIT 50",
  "SELECT * FROM fnb.table_reservation LIMIT 50",
  "SELECT * FROM fnb.table_visit LIMIT 50"
 ],
 "rollbackMenu": [
  "SELECT * FROM fnb.menu LIMIT 50"
 ],
 "scheduleMenuPublish": [
  "SELECT * FROM fnb.menu LIMIT 50"
 ],
 "seatTableReservation": [
  "SELECT * FROM fnb.table LIMIT 50",
  "SELECT * FROM fnb.table_reservation LIMIT 50"
 ],
 "sendBookingConfirmation": [
  "SELECT * FROM fnb.table_reservation LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "sendOrderNotification": [
  "SELECT * FROM fnb.fnb_order LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "setComboSlots": [
  "SELECT * FROM fnb.combo LIMIT 50",
  "SELECT * FROM fnb.menu_item LIMIT 50"
 ],
 "setItemAvailability": [
  "SELECT * FROM fnb.menu_item LIMIT 50"
 ],
 "setKitchenStations": [
  "SELECT * FROM fnb.kitchen_station LIMIT 50"
 ],
 "setKitchenTicketStatus": [
  "SELECT * FROM fnb.kitchen_ticket LIMIT 50"
 ],
 "setMenuSections": [
  "SELECT * FROM fnb.menu LIMIT 50",
  "SELECT * FROM fnb.menu_item LIMIT 50",
  "SELECT * FROM fnb.menu_section LIMIT 50"
 ],
 "setRecipe": [
  "SELECT * FROM fnb.recipe LIMIT 50"
 ],
 "setSectionLayout": [
  "SELECT * FROM fnb.table LIMIT 50"
 ],
 "setServiceStage": [
  "SELECT * FROM fnb.table_visit LIMIT 50"
 ],
 "setSubstitutionRules": [
  "SELECT * FROM fnb.substitution_rule LIMIT 50"
 ],
 "setTableCombinations": [
  "SELECT * FROM fnb.table LIMIT 50"
 ],
 "setTableLayout": [
  "SELECT * FROM fnb.table LIMIT 50"
 ],
 "signCorrectiveAction": [
  "SELECT * FROM fnb.corrective_action WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "splitBill": [
  "SELECT * FROM fnb.bill_split LIMIT 50"
 ],
 "transferOrderItems": [
  "SELECT * FROM fnb.table_visit LIMIT 50",
  "SELECT * FROM orders.order_line LIMIT 50"
 ],
 "transferTableVisit": [
  "SELECT * FROM fnb.table_visit LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "updateMenu": [
  "SELECT * FROM fnb.menu LIMIT 50",
  "SELECT * FROM fnb.menu_item LIMIT 50",
  "SELECT * FROM fnb.menu_section LIMIT 50"
 ],
 "updateTable": [
  "SELECT * FROM fnb.table LIMIT 50",
  "SELECT * FROM fnb.table_visit LIMIT 50"
 ],
 "updateTableReservation": [
  "SELECT * FROM fnb.table_reservation LIMIT 50"
 ],
 "updateTableVisit": [
  "SELECT * FROM fnb.fnb_order LIMIT 50",
  "SELECT * FROM fnb.table_visit LIMIT 50"
 ],
 "verifyAllergens": [
  "SELECT * FROM fnb.menu_item LIMIT 50",
  "SELECT * FROM fnb.modifier_group WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM fnb.recipe LIMIT 50",
  "SELECT * FROM fnb.substitution_rule LIMIT 50"
 ]
}

WRITES = {
 "acceptFnbOrder": [
  "SELECT id FROM fnb.fnb_order ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "amendFnbOrder": [
  "SELECT id FROM fnb.fnb_order ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "applyMenuActions": [
  "SELECT id FROM catalogue.price ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM fnb.menu_item ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "attachModifierGroup": [
  "SELECT id FROM fnb.menu_item ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "buildProductionPlan": [
  "SELECT id FROM fnb.production_plan ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "cancelFnbOrder": [
  "SELECT id FROM fnb.fnb_order ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "chaseStation": [
  "SELECT id FROM fnb.kitchen_exception ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "claimLocationSession": [
  "SELECT id FROM fnb.location_session ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "claimTableSession": [
  "SELECT id FROM fnb.table_session ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "clearTable": [
  "SELECT id FROM fnb.table ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "closeCorrectiveAction": [
  "SELECT id FROM fnb.corrective_action WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "closeTableVisit": [
  "SELECT id FROM fnb.fnb_order ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM fnb.table_visit ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "compItem": [
  "SELECT id FROM orders.order_discount ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.order_line ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "completeProductionRun": [
  "SELECT id FROM fnb.production_run ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM inventory.movement ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createCombo": [
  "SELECT id FROM fnb.combo ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM fnb.combo_slot ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createFnbOrder": [
  "SELECT id FROM fnb.fnb_order ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createGuestFnbOrder": [
  "SELECT id FROM fnb.fnb_order ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM fnb.kitchen_ticket ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createMenu": [
  "SELECT id FROM fnb.menu ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM fnb.menu_item ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createModifierGroup": [
  "SELECT id FROM fnb.modifier_group WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createTable": [
  "SELECT id FROM fnb.table ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createTableReservation": [
  "SELECT id FROM fnb.table_reservation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "escalateCorrectiveAction": [
  "SELECT id FROM fnb.corrective_action WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "fireCourse": [
  "SELECT id FROM fnb.kitchen_ticket ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "holdCourse": [
  "SELECT id FROM fnb.kitchen_ticket ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "joinRestaurantWaitlist": [
  "SELECT id FROM fnb.waitlist_entry ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "logColdChain": [
  "SELECT id FROM fnb.cold_chain_event ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM fnb.corrective_action WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "logKitchenException": [
  "SELECT id FROM fnb.kitchen_exception ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "logTemperature": [
  "SELECT id FROM fnb.corrective_action WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM fnb.temperature_log ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "markOrderCollected": [
  "SELECT id FROM fnb.fnb_order ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM fnb.kitchen_ticket ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "mergeTableVisits": [
  "SELECT id FROM fnb.fnb_order ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM fnb.table_visit ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "moveTableVisit": [
  "SELECT id FROM fnb.kitchen_ticket ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM fnb.table_visit ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "notifyServer": [
  "SELECT id FROM marketing.message_dispatch ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "notifyWaitlistParty": [
  "SELECT id FROM marketing.message_dispatch ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "openTableVisit": [
  "SELECT id FROM fnb.fnb_order ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM fnb.table_visit ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "planProductionRun": [
  "SELECT id FROM fnb.production_run ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "prioritiseKitchenTicket": [
  "SELECT id FROM fnb.kitchen_ticket ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "publishMenu": [
  "SELECT id FROM catalogue.product_version ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM fnb.menu ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reassignServer": [
  "SELECT id FROM fnb.table_visit ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "rebalanceStationLoad": [
  "SELECT id FROM fnb.kitchen_station ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recallKitchenTicket": [
  "SELECT id FROM fnb.kitchen_ticket ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordCorrectiveAction": [
  "SELECT id FROM fnb.corrective_action WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordOrderHandover": [
  "SELECT id FROM fnb.fnb_order ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordWaste": [
  "SELECT id FROM inventory.movement ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "refireItem": [
  "SELECT id FROM fnb.kitchen_ticket_line ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM inventory.movement ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "releaseProductionPlan": [
  "SELECT id FROM fnb.production_plan ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM fnb.production_run ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "requestBill": [
  "SELECT id FROM fnb.table_visit ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "rollbackMenu": [
  "SELECT id FROM fnb.menu ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "scheduleMenuPublish": [
  "SELECT id FROM fnb.menu ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "seatTableReservation": [
  "SELECT id FROM fnb.table_reservation ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM fnb.table_session ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "sendBookingConfirmation": [
  "SELECT id FROM fnb.table_reservation ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM marketing.message_dispatch ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "sendOrderNotification": [
  "SELECT id FROM marketing.message_dispatch ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setComboSlots": [
  "SELECT id FROM fnb.combo_slot ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setItemAvailability": [
  "SELECT id FROM fnb.menu_item ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setKitchenStations": [
  "SELECT id FROM fnb.kitchen_station ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setKitchenTicketStatus": [
  "SELECT id FROM fnb.kitchen_ticket ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.outbox WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setMenuSections": [
  "SELECT id FROM fnb.menu ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM fnb.menu_item ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setRecipe": [
  "SELECT id FROM fnb.recipe ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setSectionLayout": [
  "SELECT id FROM fnb.table ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setServiceStage": [
  "SELECT id FROM fnb.table_visit ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setSubstitutionRules": [
  "SELECT id FROM fnb.substitution_rule ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setTableCombinations": [
  "SELECT id FROM fnb.table ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setTableLayout": [
  "SELECT id FROM fnb.table ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "signCorrectiveAction": [
  "SELECT id FROM fnb.corrective_action WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "splitBill": [
  "SELECT id FROM fnb.bill_split ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "transferOrderItems": [
  "SELECT id FROM fnb.table_visit ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.order_line ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "transferTableVisit": [
  "SELECT id FROM fnb.table_visit ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateMenu": [
  "SELECT id FROM fnb.menu ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM fnb.menu_item ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateTable": [
  "SELECT id FROM fnb.table ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateTableReservation": [
  "SELECT id FROM fnb.table_reservation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateTableVisit": [
  "SELECT id FROM fnb.fnb_order ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM fnb.table_visit ORDER BY id LIMIT 1 FOR UPDATE"
 ]
}

CACHE = {
 "acceptFnbOrder": [
  "cache:idempotency:bench"
 ],
 "amendFnbOrder": [
  "cache:idempotency:bench"
 ],
 "applyMenuActions": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "attachModifierGroup": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "buildProductionPlan": [
  "cache:idempotency:bench"
 ],
 "cancelFnbOrder": [
  "cache:idempotency:bench"
 ],
 "chaseStation": [
  "cache:idempotency:bench"
 ],
 "claimLocationSession": [
  "cache:idempotency:bench"
 ],
 "claimTableSession": [
  "cache:idempotency:bench"
 ],
 "clearTable": [
  "cache:idempotency:bench"
 ],
 "closeCorrectiveAction": [
  "cache:idempotency:bench"
 ],
 "closeTableVisit": [
  "cache:idempotency:bench"
 ],
 "compItem": [
  "cache:idempotency:bench"
 ],
 "completeProductionRun": [
  "cache:idempotency:bench"
 ],
 "createCombo": [
  "cache:idempotency:bench"
 ],
 "createFnbOrder": [
  "cache:idempotency:bench"
 ],
 "createGuestFnbOrder": [
  "cache:idempotency:bench"
 ],
 "createMenu": [
  "cache:idempotency:bench"
 ],
 "createModifierGroup": [
  "cache:idempotency:bench"
 ],
 "createTable": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "createTableReservation": [
  "cache:idempotency:bench"
 ],
 "enterCountLine": [
  "cache:idempotency:bench"
 ],
 "escalateCorrectiveAction": [
  "cache:idempotency:bench"
 ],
 "fireCourse": [
  "cache:idempotency:bench"
 ],
 "holdCourse": [
  "cache:idempotency:bench"
 ],
 "joinRestaurantWaitlist": [
  "cache:idempotency:bench"
 ],
 "logColdChain": [
  "cache:idempotency:bench"
 ],
 "logKitchenException": [
  "cache:idempotency:bench"
 ],
 "logTemperature": [
  "cache:idempotency:bench"
 ],
 "markOrderCollected": [
  "cache:idempotency:bench"
 ],
 "mergeTableVisits": [
  "cache:idempotency:bench"
 ],
 "moveTableVisit": [
  "cache:idempotency:bench"
 ],
 "notifyServer": [
  "cache:idempotency:bench"
 ],
 "notifyWaitlistParty": [
  "cache:idempotency:bench"
 ],
 "openTableVisit": [
  "cache:idempotency:bench"
 ],
 "planProductionRun": [
  "cache:idempotency:bench"
 ],
 "prioritiseKitchenTicket": [
  "cache:idempotency:bench"
 ],
 "publishMenu": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "quoteWaitTime": [
  "cache:idempotency:bench"
 ],
 "reassignServer": [
  "cache:idempotency:bench"
 ],
 "rebalanceStationLoad": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "recallKitchenTicket": [
  "cache:idempotency:bench"
 ],
 "recordCorrectiveAction": [
  "cache:idempotency:bench"
 ],
 "recordOrderHandover": [
  "cache:idempotency:bench"
 ],
 "recordWaste": [
  "cache:idempotency:bench"
 ],
 "refireItem": [
  "cache:idempotency:bench"
 ],
 "releaseProductionPlan": [
  "cache:idempotency:bench"
 ],
 "requestBill": [
  "cache:idempotency:bench"
 ],
 "requestRecount": [
  "cache:idempotency:bench"
 ],
 "rollbackMenu": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "scheduleMenuPublish": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "seatTableReservation": [
  "cache:idempotency:bench"
 ],
 "sendBookingConfirmation": [
  "cache:idempotency:bench"
 ],
 "sendOrderNotification": [
  "cache:idempotency:bench"
 ],
 "setComboSlots": [
  "cache:idempotency:bench"
 ],
 "setCourseRules": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setItemAvailability": [
  "cache:idempotency:bench"
 ],
 "setKitchenSla": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setKitchenStations": [
  "cache:idempotency:bench"
 ],
 "setKitchenTicketStatus": [
  "cache:idempotency:bench"
 ],
 "setMenuSections": [
  "cache:idempotency:bench"
 ],
 "setRecipe": [
  "cache:idempotency:bench"
 ],
 "setSectionLayout": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setServiceStage": [
  "cache:idempotency:bench"
 ],
 "setSubstitutionRules": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setTableCombinations": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setTableLayout": [
  "cache:idempotency:bench"
 ],
 "signCorrectiveAction": [
  "cache:idempotency:bench"
 ],
 "splitBill": [
  "cache:idempotency:bench"
 ],
 "transferOrderItems": [
  "cache:idempotency:bench"
 ],
 "transferTableVisit": [
  "cache:idempotency:bench"
 ],
 "updateMenu": [
  "cache:idempotency:bench"
 ],
 "updateTable": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "updateTableReservation": [
  "cache:idempotency:bench"
 ],
 "updateTableVisit": [
  "cache:idempotency:bench"
 ]
}
