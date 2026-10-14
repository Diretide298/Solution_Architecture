#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""When each table first appeared, what it was called before, and what breaks if it moves.

**A workbook that cannot say "renamed" says "deleted" and "added" instead.** On 19 September
`retail.wallet`, `retail.wallet_transaction` and `retail.gift_card` became `wallet.*` when the
wallet runtime left `retail.yaml`. Nothing in the package records that they are the same three
tables, so anyone comparing this week's workbook to last week's sees three disappear and three
arrive — and the safe reading of a table disappearing is that its data was dropped.

**And the workbook's idea of what is new is a set literal typed on 14 August.** Eighteen names
in `build-schema-workbook.py`, still shown blue five weeks later, while the schema went from
378 tables to 556 — **178 tables arrived and not one of them is marked.** A highlight that
cannot go stale is a highlight nobody has to maintain; this one could, and did.

## Additive, like the lineage, and for the same reason

`handoff/schema-history.json` is appended and never rewritten. A table seen for the first time
records the date it was seen; a table that disappears is **kept**, because a name that stops
appearing is either a rename somebody must record or a deletion somebody must confirm, and a
tool cannot tell which. That is the same rule `derive-lineage` follows, arrived at the same
way: on 19 September an entry that silently vanished would have hidden three renames.

Renames are declared in `renames` by hand — a rename is a judgement about identity, not
something a diff can see, since to a diff it is exactly a delete and an add.

## Blast radius

For a table that moves, the answer to "what breaks" is already derivable: every operation that
reads or writes it, every service that owns or reaches it, every screen whose operations touch
it. `--radius <table>` prints that, so the question is answered before the rename rather than
by `check-package` three steps later.

    python3 tools/derive-schema-history.py              # report
    python3 tools/derive-schema-history.py --apply      # record what is new
    python3 tools/derive-schema-history.py --radius wallet.wallet
"""
import collections
import datetime
import glob
import io
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "handoff")
OUT = os.path.join(H, "schema-history.json")
TODAY = datetime.date.today().isoformat()

# **Seeded, not invented.** Four of the eighteen names `build-schema-workbook.py` carried as
# "new on 14 August" still exist under that name; the rest were renamed or absorbed in the
# five weeks since, which is itself the argument for recording this. Keeping these dated
# preserves the only evidence the package holds about when a table arrived. Everything else is
# recorded at the baseline — "at or before 19 September" — because there is no earlier
# evidence for it, and inventing one would be worse than saying so.
SEED_14_AUG = {
    "platform.outlet", "platform.tenant", "marketing.guest_device", "marketing.wishlist_item",
}

# A rename is a judgement about identity. Declared here, never inferred.
RENAMES = [
    {"from": "platform.org_unit", "to": "platform.scope", "on": "2026-09-20",
     "why": "scope is the word 58 of our configuration profiles already address by; org_unit is generic ERP vocabulary that appears nowhere else in our language"},
    {"from": "fnb.fnb_order", "to": "fnb.service_order", "on": "2026-09-20",
     "why": "fnb_order repeats its schema, which is the fault we ask them to fix in approvals.approval_matrix. Their name is fnb.order and we are not taking it: order is a reserved word in Postgres, so the table would need quoting in every hand-written query forever. We solved this once already with orders.sales_order, and their own purpose line calls this the operational food-service order"},
    {"from": "fnb.fnb_order_line", "to": "fnb.service_order_line", "on": "2026-09-20",
     "why": "their order_item plus our word: a line is what an order has"},
    {"from": "fnb.table", "to": "fnb.dining_table", "on": "2026-09-20",
     "why": "table alone is vague beside fnb.table_reservation and fnb.table_session"},
    {"from": "fnb.eighty_six_event", "to": "fnb.sold_out_item", "on": "2026-09-20",
     "why": "86 is US restaurant jargon and this platform ships in the Gulf"},
    {"from": "ai.interaction", "to": "ai.activity", "on": "2026-09-20",
     "why": "their purpose line: any AI request, including non-chat calls. An interaction reads as a conversation and most of these rows are not one"},
    {"from": "control.api_quota", "to": "control.api_limit", "on": "2026-09-20",
     "why": "rate limits and usage limits; quota covers only the second"},
    {"from": "queue.waiting_guest", "to": "queue.entry", "on": "2026-09-20",
     "why": "their purpose says a customer or party; waiting_guest misnames a party of six"},
    {"from": "orders.shift", "to": "orders.pos_shift", "on": "2026-09-20",
     "why": "disambiguates from workforce.shift, which they also hold"},
    {"from": "maintenance.maintenance_plan", "to": "maintenance.preventive_plan", "on": "2026-09-20",
     "why": "repeats its schema, and preventive is more specific"},
    {"from": "marketing.journey_entrant", "to": "marketing.journey_enrollment", "on": "2026-09-20",
     "why": "entrant reads as a person, not a record"},
    {"from": "orders.payment_provider", "to": "payments.provider", "on": "2026-09-20",
     "why": "decision 2: configuration belongs in payments, the transaction stays in orders"},
    {"from": "orders.payment_token", "to": "payments.token", "on": "2026-09-20",
     "why": "decision 2, same boundary"},
    {"from": "control.subscription", "to": "subscription.contract", "on": "2026-09-20",
     "why": "decision 3: subscription lived in three places. contract rather than subscription.subscription, which would repeat the schema"},
    {"from": "control.subscription_plan", "to": "subscription.plan", "on": "2026-09-20",
     "why": "decision 3, and it drops the repeated prefix"},
    {"from": "rental.category", "to": "maintenance.asset_category", "on": "2026-09-20",
     "why": "it is the asset-category master for the whole venue - maintenance.asset, maintenance_plan, inspection_template, resources.resource_category and resource_requirement all point at it. A forklift that is never rented had its category defined in rental"},
    {"from": "retail.wallet", "to": "wallet.wallet", "on": "2026-09-19",
     "why": "the wallet runtime left retail.yaml for wallet.yaml; a service that owns tables "
            "inside another service's schema is not its own service"},
    {"from": "retail.wallet_transaction", "to": "wallet.wallet_transaction", "on": "2026-09-19",
     "why": "moved with wallet.wallet"},
    {"from": "retail.gift_card", "to": "wallet.gift_card", "on": "2026-09-19",
     "why": "moved with wallet.wallet"},
    {"from": "catalogue.session_template", "to": "catalogue.performance_template", "on": "2026-09-28",
     "why": "a session in the design is a Performance (decided 28 September, audit R165)"},
    {"from": "resources.session_participant", "to": "resources.performance_participant", "on": "2026-09-28",
     "why": "audit R165: the manifest is per Performance; session_id becomes performance_id, a foreign key to catalogue.performance"},
    {"from": "control.footer_config", "to": "whitelabel.footer_config", "on": "2026-09-28",
     "why": "the footer is tenant configuration, not control plane (audit R163)"},
    {"from": "control.footer_config_column", "to": "whitelabel.footer_config_column", "on": "2026-09-28",
     "why": "moved with whitelabel.footer_config (audit R163)"},
    {"from": "control.footer_config_social_link", "to": "whitelabel.footer_config_social_link", "on": "2026-09-28",
     "why": "moved with whitelabel.footer_config (audit R163)"},
    {"from": "identity.access_policy_version", "to": "identity.authorisation_policy_version", "on": "2026-10-01",
     "why": "ADR-0068: moved with identity.authorisation_policy; each version of a staff-authorisation policy"},
    {"from": "identity.access_policy", "to": "identity.authorisation_policy", "on": "2026-10-01",
     "why": "ADR-0068: it is staff authorisation, not access. Guest admission at the gate is access.dynamic_policy, so 'access policy' now means one thing"},
    {"from": "access.access_device", "to": "access.device_placement", "on": "2026-10-01",
     "why": "ADR-0067: platform.device is the one device register; identity, versions, health and lifecycle moved there and this table keeps only where a device is placed in the gate topology. Not access.device_binding, which already names a guest's phone bound to an entitlement"},
    # CHG-R6-010 (ADAM CR-011, 12 October 2026): names naming-and-style bans in DDL. After r1, so derive-ddl
    # lists each as a rename in handoff/migration-review.md rather than generating a new table.
    {"from": "seating.seat_hold", "to": "seating.seat_reservation", "on": "2026-10-12",
     "why": "CR-011: naming-and-style 3 says a held, not-yet-paid commitment is a Reservation, never a Hold (Hold only in labels, 3.3)"},
    {"from": "seating.seat_hold_item", "to": "seating.seat_reservation_item", "on": "2026-10-12",
     "why": "CR-011: moved with seating.seat_reservation"},
    {"from": "wallet.hold", "to": "wallet.fund_reservation", "on": "2026-10-12",
     "why": "CR-011: money reserved on a wallet while an order or payment is in progress; Hold is banned in DDL, and reservation alone in the wallet schema would read as a guest's reservation"},
    {"from": "catalogue.inventory_hold", "to": "catalogue.inventory_reservation", "on": "2026-10-12",
     "why": "CR-011: capacity a cart or workstation holds until it converts or expires is a Reservation (naming-and-style 3)"},
    {"from": "resources.resource_hold", "to": "resources.resource_reservation", "on": "2026-10-12",
     "why": "CR-011: as catalogue.inventory_reservation, for bookable resources"},
    {"from": "catalogue.channel_allocation", "to": "catalogue.channel_envelope", "on": "2026-10-12",
     "why": "CR-011: a channel's capacity allocation container is an Envelope; Allocation and Pool are its banned synonyms (naming-and-style 3)"},
    {"from": "seating.recommendation_rules", "to": "seating.recommendation_rule", "on": "2026-10-12",
     "why": "CR-011: naming-and-style 6.1, a table is a singular noun"},
    {"from": "wallet.channel_rules", "to": "wallet.channel_rule", "on": "2026-10-12",
     "why": "CR-011: naming-and-style 6.1, a table is a singular noun"},
    {"from": "wallet.funding_rules", "to": "wallet.funding_rule", "on": "2026-10-12",
     "why": "CR-011: naming-and-style 6.1, a table is a singular noun"},
    {"from": "wallet.risk_rules", "to": "wallet.risk_rule_set", "on": "2026-10-12",
     "why": "CR-011: naming-and-style 6.1, a table is a singular noun. Not wallet.risk_rule, which already names its rows (one rule each); this is the published rule set they belong to"},
    {"from": "wallet.transfer_rules", "to": "wallet.transfer_rule", "on": "2026-10-12",
     "why": "CR-011: naming-and-style 6.1, a table is a singular noun"},
    # CHG-R6-018 (ADAM CR-014, 12 October 2026).
    {"from": "inventory.item", "to": "inventory.inventory_item", "on": "2026-10-12",
     "why": "CR-014: the canonical term is Inventory Item (InventoryItem), not a Product; item alone is the bare Item naming-and-style 3 bans"},
    {"from": "inventory.stock_reservation", "to": "inventory.stock_earmark", "on": "2026-10-12",
     "why": "CR-014: stock set aside for an order, a rental or a work order. Reservation is a guest's held, not-yet-paid commitment (naming-and-style 3.1), and this is not one"},
    {"from": "orders.group_customer_organization", "to": "orders.group_customer_organisation", "on": "2026-10-12",
     "why": "CR-014: one spelling throughout; the package writes organisation (organisation_type, organisation_id beside it)"},
    {"from": "orders.group_customer_organization_contact", "to": "orders.group_customer_organisation_contact", "on": "2026-10-12",
     "why": "CR-014: moved with orders.group_customer_organisation"},
]

# **A column rename is declared here too** (CHG-R6-010, 12 October 2026), by the table's name *now*. The contract
# says the new name (`x-ticvai-column` on the field, which keeps its wire name; or the parent key of a child table,
# which follows its parent's new name), and this list says it is the same column under a new name, so that
# derive-ddl lists `RENAME COLUMN` in handoff/migration-review.md rather than a new column and a dropped one, and
# check-ddl-conventions (D-BANNED-NAME) does not take the old name back as one r1 already had.
COLUMN_RENAMES = [
    # CHG-R6-010 / CHG-R6-011 (ADAM CR-011, CR-012)
    {"table": "seating.seat_reservation_item", "from": "hold_id", "to": "seat_reservation_id", "on": "2026-10-12",
     "why": "CR-011: a key names the table it references (naming-and-style 6.1)"},
    {"table": "seating.seat_reservation_item", "from": "held_price", "to": "gross_amount", "on": "2026-10-12",
     "why": "CR-011: bare money name (5.1); the seat's share of seat_reservation.gross_amount"},
    {"table": "wallet.fund_reservation", "from": "wallet_hold_amount", "to": "reserved_amount", "on": "2026-10-12",
     "why": "CR-011: Hold is banned in DDL"},
    {"table": "wallet.fund_reservation", "from": "wallet_hold_status", "to": "status", "on": "2026-10-12",
     "why": "CR-011: Hold is banned in DDL"},
    {"table": "wallet.wallet_transaction", "from": "wallet_hold_id", "to": "fund_reservation_id", "on": "2026-10-12",
     "why": "CR-011: a key names the table it references"},
    {"table": "platform.wallet_authorisation", "from": "wallet_hold_id", "to": "fund_reservation_id", "on": "2026-10-12",
     "why": "CR-011: a key names the table it references"},
    {"table": "orders.order_line", "from": "inventory_hold_id", "to": "inventory_reservation_id", "on": "2026-10-12",
     "why": "CR-011: a key names the table it references"},
    {"table": "orders.cart_line", "from": "inventory_hold_id", "to": "inventory_reservation_id", "on": "2026-10-12",
     "why": "CR-011: a key names the table it references"},
    {"table": "orders.reservation_line", "from": "inventory_hold_id", "to": "inventory_reservation_id", "on": "2026-10-12",
     "why": "CR-011: a key names the table it references"},
    {"table": "orders.order_line", "from": "resource_hold_id", "to": "resource_reservation_id", "on": "2026-10-12",
     "why": "CR-011: a key names the table it references"},
    {"table": "orders.cart_line", "from": "resource_hold_id", "to": "resource_reservation_id", "on": "2026-10-12",
     "why": "CR-011: a key names the table it references"},
    {"table": "orders.reservation_line", "from": "resource_hold_id", "to": "resource_reservation_id", "on": "2026-10-12",
     "why": "CR-011: a key names the table it references"},
    {"table": "catalogue.channel_envelope", "from": "allocation_type", "to": "envelope_type", "on": "2026-10-12",
     "why": "CR-011: Allocation is a banned synonym of Envelope; the values (sharedPool and the rest) are wire values and stay"},
    {"table": "wallet.risk_rule", "from": "risk_rules_id", "to": "risk_rule_set_id", "on": "2026-10-12",
     "why": "CR-011: the parent key follows wallet.risk_rule_set"},
    {"table": "platform.workstation", "from": "cash_drawer_limit", "to": "deposit_box_limit_amount", "on": "2026-10-12",
     "why": "CR-011: drawer is staff copy only (3.3); the cash container is the Deposit Box. Typed numeric(18,4) as Money now (was text)"},
    {"table": "platform.venue_settings", "from": "cash_drawer_limit", "to": "deposit_box_limit_amount", "on": "2026-10-12",
     "why": "CR-011: as platform.workstation.deposit_box_limit_amount"},
    {"table": "catalogue.price", "from": "amount", "to": "list_price", "on": "2026-10-12",
     "why": "CR-011: an entered price is list_price (naming-and-style 5.1)"},
    {"table": "seating.seat_price_band", "from": "amount", "to": "list_price", "on": "2026-10-12",
     "why": "CR-011: an entered price is list_price (5.1)"},
    {"table": "wallet.wallet", "from": "balance", "to": "balance_amount", "on": "2026-10-12",
     "why": "CR-011: bare money name (5.1); as wallet.balance.balance_amount"},
    {"table": "wallet.gift_card", "from": "balance", "to": "balance_amount", "on": "2026-10-12",
     "why": "CR-011: bare money name (5.1)"},
    {"table": "wallet.gift_card", "from": "face_value", "to": "face_value_amount", "on": "2026-10-12",
     "why": "CR-011: bare money name (5.1); as platform.denomination.face_value_amount"},
    {"table": "wallet.wallet_transaction", "from": "amount", "to": "transaction_amount", "on": "2026-10-12",
     "why": "CR-011: bare money name (5.1)"},
    {"table": "wallet.adjustment", "from": "amount", "to": "adjustment_amount", "on": "2026-10-12",
     "why": "CR-011: bare money name (5.1)"},
    {"table": "wallet.dispute", "from": "amount", "to": "disputed_amount", "on": "2026-10-12",
     "why": "CR-011: bare money name (5.1)"},
    {"table": "wallet.exit_settlement", "from": "amount", "to": "settled_amount", "on": "2026-10-12",
     "why": "CR-011: bare money name (5.1)"},
    # CHG-R6-018 (ADAM CR-014)
    {"table": "ledger.account", "from": "balance", "to": "balance_amount", "on": "2026-10-12",
     "why": "CR-014: bare money name (5.1)"},
    {"table": "ledger.price_variance", "from": "quoted_price", "to": "quoted_amount", "on": "2026-10-12",
     "why": "CR-014: a computed price, not an entered one, so *_amount (5.1)"},
    {"table": "ledger.price_variance", "from": "server_price", "to": "server_amount", "on": "2026-10-12",
     "why": "CR-014: as quoted_amount"},
    {"table": "ledger.price_variance", "from": "variance", "to": "variance_amount", "on": "2026-10-12",
     "why": "CR-014: bare money name (5.1)"},
    {"table": "ledger.tax_invoice_line", "from": "unit_price", "to": "unit_amount", "on": "2026-10-12",
     "why": "CR-014: an invoiced unit figure copied from the order, not an entered price (5.1)"},
    {"table": "inventory.requisition", "from": "estimated_total", "to": "estimated_amount", "on": "2026-10-12",
     "why": "CR-014: a total alone does not say what it is (5.1)"},
    {"table": "inventory.supplier", "from": "minimum_order_value", "to": "minimum_order_amount", "on": "2026-10-12",
     "why": "CR-014: value alone is banned (5.1)"},
    {"table": "inventory.inventory_item", "from": "last_purchase_price", "to": "last_purchase_cost_amount", "on": "2026-10-12",
     "why": "CR-014: a cost, before tax, as inventory.movement.net_cost_amount"},
    {"table": "orders.payment", "from": "amount", "to": "payment_amount", "on": "2026-10-12",
     "why": "CR-014: bare money name (5.1)"},
    {"table": "orders.refund", "from": "amount", "to": "refunded_amount", "on": "2026-10-12",
     "why": "CR-014: bare money name; refunded_amount is 5.1's own example"},
    {"table": "orders.cash_movement", "from": "amount", "to": "movement_amount", "on": "2026-10-12",
     "why": "CR-014: bare money name (5.1)"},
    {"table": "orders.deposit_box", "from": "variance", "to": "variance_amount", "on": "2026-10-12",
     "why": "CR-014: bare money name (5.1)"},
    {"table": "orders.deposit_box", "from": "withdrawn_total", "to": "withdrawn_amount", "on": "2026-10-12",
     "why": "CR-014: total alone does not say what it is (5.1)"},
    {"table": "orders.deposit_box", "from": "expected_total", "to": "expected_amount", "on": "2026-10-12",
     "why": "CR-014: as withdrawn_amount"},
    {"table": "orders.deposit_box", "from": "counted_total", "to": "counted_amount", "on": "2026-10-12",
     "why": "CR-014: as withdrawn_amount"},
    {"table": "orders.deposit_box_foreign_holding", "from": "variance", "to": "variance_amount", "on": "2026-10-12",
     "why": "CR-014: as orders.deposit_box.variance_amount, beside its own expected_amount and counted_amount"},
    {"table": "orders.group_customer_organisation_contact", "from": "group_customer_organization_id",
     "to": "group_customer_organisation_id", "on": "2026-10-12",
     "why": "CR-014: the parent key follows orders.group_customer_organisation"},
    {"table": "marketing.processing_purpose", "from": "data_controller_applicable_organization",
     "to": "data_controller_applicable_organisation", "on": "2026-10-12",
     "why": "CR-014: one spelling throughout"},
    {"table": "rental.agreement_item", "from": "stock_reservation_id", "to": "stock_earmark_id", "on": "2026-10-12",
     "why": "CR-014: a key names the table it references (inventory.stock_earmark)"},
    # CHG-TEN-001 (ADAM CR-080, 14 October 2026)
    {"table": "platform.sale_board_tile", "from": "page_id", "to": "sale_board_page_id", "on": "2026-10-14",
     "why": "CR-080: the tile is SaleBoard.pages[].tiles[] and its parent key is derived as sale_board_page_id; the "
            "relationship graph's old page_id would be a second key to the same page (D-DOUBLE-KEY)"},
    # CHG-DDL-006 (ADAM CR-072, 14 October 2026): the bare money names of the Sprint 1 modules built after CR-011
    # (payments, retail), settled as CR-011 and CR-014 were (naming-and-style 5.1). The wire keeps its names.
    {"table": "payments.dunning_case", "from": "amount", "to": "overdue_amount", "on": "2026-10-14",
     "why": "CR-072: bare money name (5.1); the sum the dunning case is chasing"},
    {"table": "payments.instalment", "from": "amount", "to": "due_amount", "on": "2026-10-14",
     "why": "CR-072: bare money name (5.1); what this instalment collects"},
    {"table": "payments.payment_attempt", "from": "amount", "to": "attempted_amount", "on": "2026-10-14",
     "why": "CR-072: bare money name (5.1)"},
    {"table": "payments.stored_forward", "from": "amount", "to": "transaction_amount", "on": "2026-10-14",
     "why": "CR-072: bare money name (5.1); as wallet.wallet_transaction.transaction_amount"},
    {"table": "payments.provider_cost", "from": "amount", "to": "cost_amount", "on": "2026-10-14",
     "why": "CR-072 (same rule, not on its list): bare money name (5.1)"},
    {"table": "payments.instalment_plan", "from": "total", "to": "gross_amount", "on": "2026-10-14",
     "why": "CR-072: a total is gross_amount (5.1)"},
    {"table": "payments.instalment_plan", "from": "paid_to_date", "to": "paid_amount", "on": "2026-10-14",
     "why": "CR-072: a money column says it is an amount (5.1)"},
    {"table": "payments.instalment_policy", "from": "minimum_order_value", "to": "minimum_order_amount", "on": "2026-10-14",
     "why": "CR-072: value alone is banned (5.1); as inventory.supplier.minimum_order_amount (CR-014)"},
    {"table": "payments.instalment_policy", "from": "instalment_fee", "to": "instalment_fee_amount", "on": "2026-10-14",
     "why": "CR-072: a money column says it is an amount (5.1)"},
    {"table": "retail.sale_line", "from": "unit_price", "to": "unit_amount", "on": "2026-10-14",
     "why": "CR-072: a unit figure copied onto the line at sale, not an entered price; as ledger.tax_invoice_line.unit_amount"},
    {"table": "retail.sale_line", "from": "discount", "to": "discount_amount", "on": "2026-10-14",
     "why": "CR-072: bare money name (5.1); as retail.sale.discount_amount"},
    {"table": "retail.sale_line", "from": "line_total", "to": "gross_amount", "on": "2026-10-14",
     "why": "CR-072: a total is gross_amount (5.1); as retail.sale.gross_amount"},
    {"table": "retail.return_policy", "from": "self_authorise_limit", "to": "self_authorise_limit_amount", "on": "2026-10-14",
     "why": "CR-072: a money column says it is an amount (5.1); as deposit_box_limit_amount"},
    {"table": "retail.return_policy", "from": "requires_second_user_above", "to": "second_user_above_amount",
     "on": "2026-10-14", "why": "CR-072: a money threshold named as an amount (5.1), not as a verb"},
    {"table": "retail.return_policy", "from": "requires_approval_above", "to": "approval_above_amount",
     "on": "2026-10-14", "why": "CR-072: as second_user_above_amount"},
    {"table": "retail.exchange", "from": "returned_value", "to": "returned_amount", "on": "2026-10-14",
     "why": "CR-072 (same rule, not on its list): value is banned (5.1)"},
    {"table": "retail.exchange", "from": "replacement_value", "to": "replacement_amount", "on": "2026-10-14",
     "why": "CR-072 (same rule): value is banned (5.1)"},
    {"table": "retail.exchange", "from": "difference", "to": "difference_amount", "on": "2026-10-14",
     "why": "CR-072 (same rule): a money column says it is an amount (5.1)"},
]


def tables():
    ref = os.path.join(H, "schema-reference.json")
    cols = (json.load(io.open(ref, encoding="utf-8")).get("cols") or {})
    return {t for t in cols if ":" not in t}


def load():
    try:
        return json.load(io.open(OUT, encoding="utf-8"))
    except Exception:
        return {"note": "", "firstSeen": {}, "renames": [], "withdrawn": {}}


def radius(table):
    """Everything that would have to move with it."""
    lin = json.load(io.open(os.path.join(H, "api-data-lineage.json"), encoding="utf-8"))
    dec = json.load(io.open(os.path.join(H, "service-decomposition.json"), encoding="utf-8"))
    reads = sorted(o for o, v in lin.items() if table in (v.get("reads") or []))
    writes = sorted(o for o, v in lin.items() if table in (v.get("writes") or []))
    touch = set(reads) | set(writes)
    services = sorted({lin[o].get("service") for o in touch if lin[o].get("service")})
    owner = [n for n, s in (dec.get("services") or {}).items()
             if table.split(".")[0] in (s.get("schemas") or [])]
    screens = collections.Counter()
    for f in glob.glob(os.path.join(ROOT, "screens", "P*.yaml")):
        d = yaml.safe_load(io.open(f, encoding="utf-8")) or {}
        for s in (d.get("screens") or []):
            if touch & {a.get("operationId") for a in (s.get("apis") or [])}:
                screens[(d.get("platform") or {}).get("code")] += 1
    print("  %s" % table)
    print("    owned by        %s" % (", ".join(owner) or "NO SERVICE"))
    print("    read by         %d operation(s)" % len(reads))
    print("    written by      %d operation(s)  %s" % (len(writes), ", ".join(writes[:4])))
    print("    services        %s" % ", ".join(services))
    print("    screens         %d across %s"
          % (sum(screens.values()), ", ".join(sorted(screens))))
    print()
    print("    Renaming it means every one of those lineage entries, the relationship graph,")
    print("    schema-reference and the generated DDL — derive-lineage and derive-schema both")
    print("    add without removing, so the old name survives until it is repointed at source.")
    return 0


def main():
    argv = sys.argv[1:]
    if "--radius" in argv:
        return radius(argv[argv.index("--radius") + 1])

    apply = "--apply" in argv
    hist = load()
    now = tables()
    first = hist.setdefault("firstSeen", {})
    hist["renames"] = RENAMES
    renamed_from = {r["from"] for r in RENAMES}
    renamed_to = {r["to"] for r in RENAMES}

    # **The first run knows only that everything exists, not when it arrived.** Recording
    # 552 tables as "new today" would light the whole sheet on the one run that says least.
    # The opening population is a baseline — "at or before this date" — and only what appears
    # afterwards is a change.
    baseline = hist.get("baseline")
    if not baseline and not first:
        baseline = TODAY
        hist["baseline"] = baseline

    fresh = sorted(t for t in now if t not in first)
    gone = sorted(t for t in first if t not in now and t not in renamed_from)
    for t in fresh:
        first[t] = "2026-08-14" if t in SEED_14_AUG else TODAY
    # A name that stops appearing is kept and flagged, never dropped.
    withdrawn = hist.setdefault("withdrawn", {})
    for t in gone:
        withdrawn.setdefault(t, TODAY)

    by_date = collections.Counter(first.values())
    print("  %d table(s) tracked · %d first seen today · %d rename(s) declared"
          % (len(first), sum(1 for t in fresh if first[t] == TODAY), len(RENAMES)))
    if gone:
        print("  %d name(s) no longer present and not declared as renamed — a deletion "
              "somebody must confirm:" % len(gone))
        for t in gone[:8]:
            print("      %s" % t)
    print()
    for r in RENAMES:
        state = "resolved" if r["to"] in now and r["from"] not in now else "NOT APPLIED"
        print("  rename  %-30s -> %-26s %s" % (r["from"], r["to"], state))
    print()
    print("  first seen, by date: %s"
          % ", ".join("%s %d" % (d, n) for d, n in sorted(by_date.items())))

    hist["note"] = ("When each table first appeared, and what it was called before. Appended, "
                    "never rewritten — a name that stops appearing is kept, because a tool "
                    "cannot tell a rename from a deletion and both need a person.")
    hist["generated"] = TODAY
    if not apply:
        print("\n  nothing written — pass --apply")
        return 0
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(
        json.dumps(hist, indent=1, ensure_ascii=False))
    print("  -> handoff/schema-history.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
