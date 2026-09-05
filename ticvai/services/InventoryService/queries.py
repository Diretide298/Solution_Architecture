"""Generated. The declared reads and writes of each operation."""

READS = {
 "acknowledgePurchaseOrder": [
  "SELECT * FROM inventory.purchase_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "approveRequisition": [
  "SELECT * FROM inventory.requisition LIMIT 50"
 ],
 "bulkUpdateProducts": [
  "SELECT * FROM catalogue.price LIMIT 50",
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM inventory.item LIMIT 50"
 ],
 "cancelPurchaseOrder": [
  "SELECT * FROM inventory.purchase_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "cancelRequisition": [
  "SELECT * FROM inventory.requisition LIMIT 50"
 ],
 "cancelStockCount": [
  "SELECT * FROM inventory.count LIMIT 50"
 ],
 "closePurchaseOrderShort": [
  "SELECT * FROM inventory.purchase_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "closeTransferShort": [
  "SELECT * FROM inventory.transfer WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "compareQuotations": [
  "SELECT * FROM inventory.quotation WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createGoodsReceipt": [
  "SELECT * FROM inventory.goods_receipt LIMIT 50"
 ],
 "createInventoryItem": [
  "SELECT * FROM inventory.item LIMIT 50"
 ],
 "createPurchaseOrder": [
  "SELECT * FROM inventory.purchase_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createRequisition": [
  "SELECT * FROM inventory.requisition LIMIT 50"
 ],
 "createStockLocation": [
  "SELECT * FROM inventory.location LIMIT 50"
 ],
 "createStockMovement": [
  "SELECT * FROM inventory.movement LIMIT 50"
 ],
 "createStockTransfer": [
  "SELECT * FROM inventory.transfer WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createSupplier": [
  "SELECT * FROM inventory.supplier WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getCountVariance": [
  "SELECT * FROM inventory.count LIMIT 50"
 ],
 "getInventoryItem": [
  "SELECT * FROM inventory.item LIMIT 50"
 ],
 "getPurchaseOrder": [
  "SELECT * FROM inventory.purchase_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getStockPositions": [
  "SELECT * FROM inventory.item LIMIT 50",
  "SELECT * FROM inventory.location LIMIT 50",
  "SELECT * FROM inventory.stock_level LIMIT 50"
 ],
 "getStockTransfer": [
  "SELECT * FROM fnb.cold_chain_event LIMIT 50",
  "SELECT * FROM inventory.item LIMIT 50"
 ],
 "getStockValuation": [
  "SELECT * FROM inventory.item LIMIT 50",
  "SELECT * FROM inventory.stock_level LIMIT 50",
  "SELECT * FROM ledger.account LIMIT 50"
 ],
 "getSuggestedRequisitions": [
  "SELECT * FROM inventory.requisition LIMIT 50"
 ],
 "listExpiringBatches": [
  "SELECT * FROM inventory.item LIMIT 50",
  "SELECT * FROM inventory.stock_batch LIMIT 50"
 ],
 "listGoodsReceipts": [
  "SELECT * FROM inventory.goods_receipt LIMIT 50"
 ],
 "listInventoryItems": [
  "SELECT * FROM inventory.item LIMIT 50"
 ],
 "listPurchaseOrders": [
  "SELECT * FROM inventory.purchase_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listRequisitions": [
  "SELECT * FROM inventory.requisition LIMIT 50"
 ],
 "listSerialisedItems": [
  "SELECT * FROM inventory.item LIMIT 50",
  "SELECT * FROM inventory.serialised_item LIMIT 50",
  "SELECT * FROM inventory.stock_batch LIMIT 50"
 ],
 "listStockCounts": [
  "SELECT * FROM inventory.count LIMIT 50"
 ],
 "listStockLocations": [
  "SELECT * FROM inventory.location LIMIT 50"
 ],
 "listStockMovements": [
  "SELECT * FROM inventory.movement LIMIT 50"
 ],
 "listStockTransfers": [
  "SELECT * FROM inventory.transfer WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listSuppliers": [
  "SELECT * FROM inventory.supplier WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "lookupInventoryItem": [
  "SELECT * FROM inventory.item LIMIT 50"
 ],
 "postStockCount": [
  "SELECT * FROM inventory.count LIMIT 50"
 ],
 "receiveStockTransfer": [
  "SELECT * FROM inventory.transfer WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "recordQuotation": [
  "SELECT * FROM inventory.quotation WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "recountStockCount": [
  "SELECT * FROM inventory.count LIMIT 50"
 ],
 "rejectReceivedGoods": [
  "SELECT * FROM inventory.goods_receipt LIMIT 50"
 ],
 "rejectRequisition": [
  "SELECT * FROM inventory.requisition LIMIT 50"
 ],
 "returnRequisition": [
  "SELECT * FROM inventory.requisition LIMIT 50"
 ],
 "sendPurchaseOrder": [
  "SELECT * FROM inventory.purchase_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setDailyCount": [
  "SELECT * FROM inventory.item LIMIT 50"
 ],
 "startStockCount": [
  "SELECT * FROM inventory.count LIMIT 50"
 ],
 "submitCountLines": [
  "SELECT * FROM inventory.count LIMIT 50"
 ],
 "updateInventoryItem": [
  "SELECT * FROM inventory.item LIMIT 50"
 ],
 "updateRequisitionLines": [
  "SELECT * FROM inventory.item LIMIT 50",
  "SELECT * FROM inventory.requisition LIMIT 50"
 ],
 "updateSupplier": [
  "SELECT * FROM inventory.supplier WHERE scope_path LIKE $1 LIMIT 50"
 ]
}

WRITES = {
 "acknowledgePurchaseOrder": [
  "SELECT id FROM inventory.purchase_order WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "approveRequisition": [
  "SELECT id FROM inventory.requisition ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "bulkUpdateProducts": [
  "SELECT id FROM catalogue.price ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM catalogue.product WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "cancelPurchaseOrder": [
  "SELECT id FROM inventory.purchase_order WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "cancelRequisition": [
  "SELECT id FROM inventory.requisition ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "cancelStockCount": [
  "SELECT id FROM inventory.count ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "closePurchaseOrderShort": [
  "SELECT id FROM inventory.purchase_order WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "closeTransferShort": [
  "SELECT id FROM inventory.transfer WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createGoodsReceipt": [
  "SELECT id FROM inventory.goods_receipt ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.outbox WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createInventoryItem": [
  "SELECT id FROM inventory.item ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createPurchaseOrder": [
  "SELECT id FROM inventory.purchase_order WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createRequisition": [
  "SELECT id FROM inventory.requisition ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createStockLocation": [
  "SELECT id FROM inventory.location ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createStockMovement": [
  "SELECT id FROM inventory.movement ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createStockTransfer": [
  "SELECT id FROM inventory.transfer WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createSupplier": [
  "SELECT id FROM inventory.supplier WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "postStockCount": [
  "SELECT id FROM inventory.count ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.outbox WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "receiveStockTransfer": [
  "SELECT id FROM inventory.transfer WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordQuotation": [
  "SELECT id FROM inventory.quotation WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recountStockCount": [
  "SELECT id FROM inventory.count ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "rejectReceivedGoods": [
  "SELECT id FROM inventory.goods_receipt ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "rejectRequisition": [
  "SELECT id FROM inventory.requisition ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "returnRequisition": [
  "SELECT id FROM inventory.requisition ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "sendPurchaseOrder": [
  "SELECT id FROM inventory.purchase_order WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "startStockCount": [
  "SELECT id FROM inventory.count ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "submitCountLines": [
  "SELECT id FROM inventory.count ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateInventoryItem": [
  "SELECT id FROM inventory.item ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateRequisitionLines": [
  "SELECT id FROM inventory.requisition ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateSupplier": [
  "SELECT id FROM inventory.supplier WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.audit_record ORDER BY id LIMIT 1 FOR UPDATE"
 ]
}

CACHE = {
 "acknowledgePurchaseOrder": [
  "cache:idempotency:bench"
 ],
 "approveRequisition": [
  "cache:idempotency:bench"
 ],
 "bulkUpdateProducts": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "cancelPurchaseOrder": [
  "cache:idempotency:bench"
 ],
 "cancelRequisition": [
  "cache:idempotency:bench"
 ],
 "cancelStockCount": [
  "cache:idempotency:bench"
 ],
 "closePurchaseOrderShort": [
  "cache:idempotency:bench"
 ],
 "closeTransferShort": [
  "cache:idempotency:bench"
 ],
 "createGoodsReceipt": [
  "cache:idempotency:bench"
 ],
 "createInventoryItem": [
  "cache:idempotency:bench"
 ],
 "createPurchaseOrder": [
  "cache:idempotency:bench"
 ],
 "createRequisition": [
  "cache:idempotency:bench"
 ],
 "createStockLocation": [
  "cache:idempotency:bench"
 ],
 "createStockMovement": [
  "cache:idempotency:bench"
 ],
 "createStockTransfer": [
  "cache:idempotency:bench"
 ],
 "createSupplier": [
  "cache:idempotency:bench"
 ],
 "postStockCount": [
  "cache:idempotency:bench"
 ],
 "receiveStockTransfer": [
  "cache:idempotency:bench"
 ],
 "recordQuotation": [
  "cache:idempotency:bench"
 ],
 "recountStockCount": [
  "cache:idempotency:bench"
 ],
 "rejectReceivedGoods": [
  "cache:idempotency:bench"
 ],
 "rejectRequisition": [
  "cache:idempotency:bench"
 ],
 "returnRequisition": [
  "cache:idempotency:bench"
 ],
 "sendPurchaseOrder": [
  "cache:idempotency:bench"
 ],
 "setDailyCount": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "startStockCount": [
  "cache:idempotency:bench"
 ],
 "submitCountLines": [
  "cache:idempotency:bench"
 ],
 "updateInventoryItem": [
  "cache:idempotency:bench"
 ],
 "updateRequisitionLines": [
  "cache:idempotency:bench"
 ],
 "updateSupplier": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ]
}
