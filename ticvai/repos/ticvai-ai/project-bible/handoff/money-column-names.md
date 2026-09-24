# Money columns renamed to say gross or net

Done 24 September (action register N7). `naming-and-style.md` 5.1 bans `price`, `value` and `total` alone. Each column is renamed with `x-ticvai-column` on the contract field; **the API keeps its field name**, so no client or screen spec changes.

- A calculated `subtotal` is `net_amount`, a `total` is `gross_amount`.
- An entered price is `list_price`: its tax treatment comes from the tax rule's `taxInclusive`.
- Costs are before tax (`net_cost_amount`); charges to a guest include it; wallet balances are untaxed.

| Table | Was | Now | Contract field |
|---|---|---|---|
| `control.invoice` | `subtotal` | `net_amount` | `subscription.SubscriptionInvoice.subtotal` |
| `control.invoice` | `total` | `gross_amount` | `subscription.SubscriptionInvoice.total` |
| `control.licence_add_on` | `price` | `list_price` | `subscription.LicenceAddOn.price` |
| `catalogue.prepaid_minutes` | `price` | `list_price` | `catalogue.PrepaidMinutePackage.price` |
| `fnb.combo` | `price` | `list_price` | `fnb.Combo.price` |
| `fnb.menu_item` | `price` | `list_price` | `fnb.MenuItem.price` |
| `fnb.sub_bill` | `subtotal` | `net_amount` | `fnb.SubBill.subtotal` |
| `fnb.sub_bill` | `total` | `gross_amount` | `fnb.SubBill.total` |
| `inventory.goods_receipt` | `total_value` | `net_value_amount` | `inventory.GoodsReceipt.totalValue` |
| `inventory.movement` | `total_cost` | `net_cost_amount` | `inventory.StockMovement.totalCost` |
| `inventory.purchase_order` | `subtotal` | `net_amount` | `inventory.PurchaseOrder.subtotal` |
| `inventory.purchase_order` | `total` | `gross_amount` | `inventory.PurchaseOrder.total` |
| `inventory.quotation` | `total` | `gross_amount` | `inventory.Quotation.total` |
| `maintenance.work_order` | `total_cost` | `net_cost_amount` | `maintenance.WorkOrderDetail.totalCost` |
| `orders.cart` | `subtotal` | `net_amount` | `orders.Cart.subtotal` |
| `orders.cart` | `total` | `gross_amount` | `orders.Cart.total` |
| `platform.denomination` | `value` | `face_value_amount` | `shift.Denomination.value` |
| `promotions.bundle` | `price` | `list_price` | `promotions.Bundle.price` |
| `promotions.recommendation_outcome` | `value` | `attributed_gross_amount` | `promotions.RecommendationOutcome.value` |
| `rental.settlement` | `total_charged` | `gross_charged_amount` | `rental.RentalSettlement.totalCharged` |
| `retail.merchandise` | `price` | `list_price` | `retail.MerchandiseItem.price` |
| `retail.sale` | `subtotal` | `net_amount` | `retail.RetailSale.subtotal` |
| `seating.seat_hold` | `total_price` | `gross_amount` | `seating.SeatHold.totalPrice` |
| `subscription.capacity_pack` | `price` | `list_price` | `subscription.CapacityPack.price` |
| `subscription.module_listing` | `price` | `list_price` | `subscription.ModuleListing.price` |
| `wallet.balance` | `total_balance` | `balance_amount` | `wallet.WalletBalance.totalBalance` |
| `wallet.shared_wallet` | `total_budget` | `budget_amount` | `wallet.SharedWallet.totalBudget` |
| `fnb.sub_bill` | `subtotal`, `total` | `net_amount`, `gross_amount` | also `fnb.BillSplit.subBills[]` |

**Left unchanged**, because the number can be a percentage or a count depending on a `type` field: `orders.discount.value`, `payments.fee_rule.value`, `catalogue.membership_benefit.value`, `pricing.dynamic_price_action.value`, `queue.reading.value`.
