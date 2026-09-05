"""Generated. The declared reads and writes of each operation."""

READS = {
 "activateGiftCard": [
  "SELECT * FROM retail.gift_card LIMIT 50"
 ],
 "adjustWallet": [
  "SELECT * FROM retail.wallet LIMIT 50"
 ],
 "blockGiftCard": [
  "SELECT * FROM retail.gift_card LIMIT 50"
 ],
 "cancelMerchandiseReservation": [
  "SELECT * FROM platform.org_unit LIMIT 50"
 ],
 "closeWallet": [
  "SELECT * FROM retail.wallet LIMIT 50",
  "SELECT * FROM retail.wallet_transaction LIMIT 50"
 ],
 "collectMerchandiseReservation": [
  "SELECT * FROM platform.org_unit LIMIT 50"
 ],
 "collectShopAndDrop": [
  "SELECT * FROM retail.shop_and_drop LIMIT 50"
 ],
 "createMerchandise": [
  "SELECT * FROM retail.merchandise LIMIT 50"
 ],
 "createRetailExchange": [
  "SELECT * FROM retail.exchange LIMIT 50"
 ],
 "createRetailReturn": [
  "SELECT * FROM retail.return LIMIT 50"
 ],
 "createRetailSale": [
  "SELECT * FROM retail.sale LIMIT 50"
 ],
 "createShopAndDrop": [
  "SELECT * FROM retail.shop_and_drop LIMIT 50"
 ],
 "disposeShopAndDrop": [
  "SELECT * FROM retail.shop_and_drop LIMIT 50"
 ],
 "getGiftCard": [
  "SELECT * FROM retail.gift_card LIMIT 50"
 ],
 "getOutletStock": [
  "SELECT * FROM platform.outlet LIMIT 50"
 ],
 "getRetailSale": [
  "SELECT * FROM retail.sale LIMIT 50"
 ],
 "getReturnPolicy": [
  "SELECT * FROM retail.return_policy LIMIT 50"
 ],
 "getWallet": [
  "SELECT * FROM retail.wallet LIMIT 50"
 ],
 "issueGiftCard": [
  "SELECT * FROM retail.gift_card LIMIT 50"
 ],
 "listMerchandise": [
  "SELECT * FROM retail.merchandise LIMIT 50"
 ],
 "listRetailReturns": [
  "SELECT * FROM retail.return LIMIT 50"
 ],
 "listRetailSales": [
  "SELECT * FROM retail.sale LIMIT 50"
 ],
 "listWalletTransactions": [
  "SELECT * FROM retail.wallet_transaction LIMIT 50"
 ],
 "lookupMerchandise": [
  "SELECT * FROM retail.merchandise LIMIT 50"
 ],
 "lookupRetailSale": [
  "SELECT * FROM retail.sale LIMIT 50"
 ],
 "lookupShopAndDrop": [
  "SELECT * FROM retail.shop_and_drop LIMIT 50"
 ],
 "redeemGiftCard": [
  "SELECT * FROM retail.gift_card LIMIT 50"
 ],
 "reinstateWallet": [
  "SELECT * FROM retail.wallet LIMIT 50"
 ],
 "reprintReceipt": [
  "SELECT * FROM retail.sale LIMIT 50"
 ],
 "reserveMerchandise": [
  "SELECT * FROM retail.reservation LIMIT 50"
 ],
 "setReturnPolicy": [
  "SELECT * FROM retail.return_policy LIMIT 50"
 ],
 "suspendWallet": [
  "SELECT * FROM retail.wallet LIMIT 50"
 ],
 "topUpWallet": [
  "SELECT * FROM retail.wallet LIMIT 50"
 ],
 "transferWalletBalance": [
  "SELECT * FROM pii.subject LIMIT 50",
  "SELECT * FROM retail.wallet LIMIT 50"
 ],
 "updateMerchandise": [
  "SELECT * FROM retail.merchandise LIMIT 50"
 ]
}

WRITES = {
 "activateGiftCard": [
  "SELECT id FROM retail.gift_card ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "adjustWallet": [
  "SELECT id FROM retail.wallet ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "blockGiftCard": [
  "SELECT id FROM retail.gift_card ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "cancelMerchandiseReservation": [
  "SELECT id FROM inventory.movement ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "closeWallet": [
  "SELECT id FROM retail.wallet ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "collectMerchandiseReservation": [
  "SELECT id FROM inventory.movement ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "collectShopAndDrop": [
  "SELECT id FROM retail.shop_and_drop ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createMerchandise": [
  "SELECT id FROM retail.merchandise ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createRetailExchange": [
  "SELECT id FROM retail.exchange ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createRetailReturn": [
  "SELECT id FROM retail.return ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createRetailSale": [
  "SELECT id FROM retail.sale ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createShopAndDrop": [
  "SELECT id FROM retail.shop_and_drop ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "disposeShopAndDrop": [
  "SELECT id FROM retail.shop_and_drop ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "issueGiftCard": [
  "SELECT id FROM retail.gift_card ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "redeemGiftCard": [
  "SELECT id FROM retail.gift_card ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM retail.wallet_transaction ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reinstateWallet": [
  "SELECT id FROM retail.wallet ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reprintReceipt": [
  "SELECT id FROM retail.sale ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reserveMerchandise": [
  "SELECT id FROM retail.reservation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setReturnPolicy": [
  "SELECT id FROM retail.return_policy ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "suspendWallet": [
  "SELECT id FROM retail.wallet ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "topUpWallet": [
  "SELECT id FROM retail.wallet ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "transferWalletBalance": [
  "SELECT id FROM retail.wallet ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM retail.wallet_transaction ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateMerchandise": [
  "SELECT id FROM retail.merchandise ORDER BY id LIMIT 1 FOR UPDATE"
 ]
}

CACHE = {
 "activateGiftCard": [
  "cache:idempotency:bench"
 ],
 "adjustWallet": [
  "cache:idempotency:bench"
 ],
 "blockGiftCard": [
  "cache:idempotency:bench"
 ],
 "cancelMerchandiseReservation": [
  "cache:idempotency:bench"
 ],
 "closeWallet": [
  "cache:idempotency:bench"
 ],
 "collectMerchandiseReservation": [
  "cache:idempotency:bench"
 ],
 "collectShopAndDrop": [
  "cache:idempotency:bench"
 ],
 "createMerchandise": [
  "cache:idempotency:bench"
 ],
 "createRetailExchange": [
  "cache:idempotency:bench"
 ],
 "createRetailReturn": [
  "cache:idempotency:bench"
 ],
 "createRetailSale": [
  "cache:idempotency:bench"
 ],
 "createShopAndDrop": [
  "cache:idempotency:bench"
 ],
 "disposeShopAndDrop": [
  "cache:idempotency:bench"
 ],
 "getReturnPolicy": [
  "cache:resolution:bench"
 ],
 "issueGiftCard": [
  "cache:idempotency:bench"
 ],
 "redeemGiftCard": [
  "cache:idempotency:bench"
 ],
 "reinstateWallet": [
  "cache:idempotency:bench"
 ],
 "reprintReceipt": [
  "cache:idempotency:bench"
 ],
 "reserveMerchandise": [
  "cache:idempotency:bench"
 ],
 "setReturnPolicy": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "suspendWallet": [
  "cache:idempotency:bench"
 ],
 "topUpWallet": [
  "cache:idempotency:bench"
 ],
 "transferWalletBalance": [
  "cache:idempotency:bench"
 ],
 "updateMerchandise": [
  "cache:idempotency:bench"
 ]
}
