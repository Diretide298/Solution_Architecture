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

# **A table no contract describes and nothing writes, whose rows have a home elsewhere, is retired here** (CHG-STO-008,
# Block A storage audit, 14 October 2026, check-ddl-conventions D-STUB-TABLE). derive-schema keeps every table the
# contracts do not describe, so a stub the relationship graph once made (an `id` and one key) stayed for ever and a
# reader was mapped to it. Each is a "table dropped" row in handoff/migration-review.md for the migration owner, and
# its readers read the table that holds the data.
RETIRED_TABLES = [
    {"table": "platform.device_heartbeat", "on": "2026-10-14",
     "why": "CHG-STO-008: a device's last heartbeat and status are platform.device (lastHeartbeatAt, status), written "
            "by recordDeviceHeartbeat; nothing writes a heartbeat row"},
    {"table": "orders.payment_tip", "on": "2026-10-14",
     "why": "CHG-STO-008: no contract field carries a tip on a payment and nothing writes one; a service charge is "
            "fnb's (service_charge_policy)"},
    {"table": "marketing.message_delivery", "on": "2026-10-14",
     "why": "CHG-STO-008: a message's delivery (delivered, opened, clicked, complained) is marketing.message_dispatch; "
            "nothing writes a delivery row"},
]

# A rename is a judgement about identity. Declared here, never inferred.
RENAMES = [
    # CHG-CRA-003 (ADAM CR-150, completing CR-097, 18 October 2026): the plan catalogue and the records about a
    # tenant rather than inside one leave the tenant template for the control database (ADR-0039). A move
    # between databases: the control forward migration creates the table and the tenant review drops it.
    # CHG-R8MIG-011 (R8 blocker IDENTITY-C59, the lead's answer A; the storage-sat lane's request 4): content blocks are a
    # tenant's own content, so they leave the control database for the tenant template. A move between databases the
    # other way: the tenant forward migration creates whitelabel.content_block, and the control review row copies the
    # rows across and drops control.content_block.
    # CHG-R8MIG-018 (R8 blocker APPROVALS-TENANCY-C10, the lead's answer A): a cell's endpoints are a control-plane fact,
    # moved to the control database as CR-150 moved the plan catalogue.
    {"from": "platform.cell_endpoint", "to": "control.cell_endpoint", "on": "2026-10-20",
     "why": "APPROVALS-TENANCY-C10: about a cell, not inside a tenant; the control plane writes it at provisioning"},
    {"from": "control.content_block", "to": "whitelabel.content_block", "on": "2026-10-20",
     "why": "IDENTITY-C59: a tenant's own content, read and written by White-Label in the tenant database"},
    {"from": "subscription.plan", "to": "control.plan", "on": "2026-10-18",
     "why": "CR-150: about a tenant, not inside one; Platform keeps it on its control connection"},
    {"from": "subscription.plan_limit", "to": "control.plan_limit", "on": "2026-10-18",
     "why": "CR-150: about a tenant, not inside one; Platform keeps it on its control connection"},
    {"from": "subscription.plan_module", "to": "control.plan_module", "on": "2026-10-18",
     "why": "CR-150: about a tenant, not inside one; Platform keeps it on its control connection"},
    {"from": "subscription.module_listing", "to": "control.module_listing", "on": "2026-10-18",
     "why": "CR-150: about a tenant, not inside one; Platform keeps it on its control connection"},
    {"from": "subscription.contract", "to": "control.contract", "on": "2026-10-18",
     "why": "CR-150: about a tenant, not inside one; Platform keeps it on its control connection"},
    {"from": "subscription.tier_allowance", "to": "control.tier_allowance", "on": "2026-10-18",
     "why": "CR-150: about a tenant, not inside one; Platform keeps it on its control connection"},
    {"from": "subscription.tier_module", "to": "control.tier_module", "on": "2026-10-18",
     "why": "CR-150: about a tenant, not inside one; Platform keeps it on its control connection"},
    {"from": "subscription.licensing_model", "to": "control.licensing_model", "on": "2026-10-18",
     "why": "CR-150: about a tenant, not inside one; Platform keeps it on its control connection"},
    {"from": "subscription.trial_config", "to": "control.trial_config", "on": "2026-10-18",
     "why": "CR-150: about a tenant, not inside one; Platform keeps it on its control connection"},
    {"from": "subscription.capacity_pack", "to": "control.capacity_pack", "on": "2026-10-18",
     "why": "CR-150: about a tenant, not inside one; Platform keeps it on its control connection"},
    {"from": "subscription.go_live_readiness", "to": "control.go_live_readiness", "on": "2026-10-18",
     "why": "CR-150: about a tenant, not inside one; Platform keeps it on its control connection"},
    {"from": "subscription.enforcement_policy", "to": "control.enforcement_policy", "on": "2026-10-18",
     "why": "CR-150: about a tenant, not inside one; Platform keeps it on its control connection"},
    {"from": "subscription.vsi_model", "to": "control.vsi_model", "on": "2026-10-18",
     "why": "CR-150: about a tenant, not inside one; Platform keeps it on its control connection"},
    {"from": "subscription.vsi_assessment", "to": "control.vsi_assessment", "on": "2026-10-18",
     "why": "CR-150: about a tenant, not inside one; Platform keeps it on its control connection"},

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
    # CHG-XDW-001 (14 October 2026, the lead: "Remove them now ?"): CrossRegionService's four records leave the
    # platform schema, which TenancyService owns in commerce, for sync, CrossRegionService's own schema in
    # operations. Every operation that reads or writes them is CrossRegionService's, so no write crosses a
    # deployable (ADR-0055 rule 4; XDW-001 to XDW-011 removed). The table names do not change, only the schema.
    {"from": "platform.guest_link", "to": "sync.guest_link", "on": "2026-10-14",
     "why": "CHG-XDW-001: a pseudonymous link between cells is CrossRegionService's record (createGuestLink, revokeGuestLink, resolveGuestLink); in platform, TenancyService's schema in commerce, its own writers in operations could not write it (DB-ROLES)"},
    {"from": "platform.dsar_request", "to": "sync.dsar_request", "on": "2026-10-14",
     "why": "CHG-XDW-001: moved with sync.guest_link, which its fan-out walks (schema-merge decision 10, 20 September: both go or neither does); createDsarRequest and getDsarRequest are CrossRegionService's"},
    {"from": "platform.cross_region_entitlement", "to": "sync.cross_region_entitlement", "on": "2026-10-14",
     "why": "CHG-XDW-001: CrossRegionService's record; every operation on it (consume, propagate, reconcile, revoke, get) is CrossRegionService's"},
    {"from": "platform.wallet_authorisation", "to": "sync.wallet_authorisation", "on": "2026-10-14",
     "why": "CHG-XDW-001: CrossRegionService's record of the cross-cell wallet handshake; every operation on it is CrossRegionService's"},
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
    {"table": "sync.wallet_authorisation", "from": "wallet_hold_id", "to": "fund_reservation_id", "on": "2026-10-12",
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
    # CHG-MKT-001 / CHG-MKT-002 (ADAM CR-086, CR-087, 14 October 2026)
    {"table": "marketing.guest_device", "from": "token_ref", "to": "token_ciphertext", "on": "2026-10-14",
     "why": "CR-086: the push token is stored encrypted by the application (ADR-0063 section 4), not as a vault "
            "reference; the wire keeps tokenRef"},
    {"table": "marketing.wishlist_item", "from": "price", "to": "list_price", "on": "2026-10-14",
     "why": "CR-087: the contract said list_price Money (5.1) and the table kept price text from an older run; "
            "typed numeric(18,4) as Money now (was text)"},
    # CHG-STO-005 and CHG-STO-009 (Block A storage audit, 14 October 2026): a key column is named for the table it
    # references and a boolean reads as an assertion (naming-and-style 6.1), so the r1 column is renamed, not added beside
    # the old one and dropped: each is a "column renamed" row in handoff/migration-review.md for the migration owner.
    {"table": "access.access_area", "from": "support_multi_park_environments", "to": "supports_multi_park_environments", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.access_change", "from": "old_access_id", "to": "old_entitlement_id", "on": "2026-10-14",
     "why": "CHG-STO-005: a key column is named for the table it references (naming-and-style 6.1)"},
    {"table": "access.access_change", "from": "new_access_id", "to": "new_entitlement_id", "on": "2026-10-14",
     "why": "CHG-STO-005: a key column is named for the table it references (naming-and-style 6.1)"},
    {"table": "access.access_point", "from": "vehicle_location_capture", "to": "captures_vehicle_location", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.admission_rules", "from": "same_day_only", "to": "is_same_day_only", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.attraction_access", "from": "fast_pass_support", "to": "supports_fast_pass", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.attraction_access", "from": "adult_companion_requirement", "to": "requires_adult_companion", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.attraction_access", "from": "membership_access", "to": "has_membership_access", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.attraction_access", "from": "vip_access", "to": "has_vip_access", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.attraction_access", "from": "biometric_requirement", "to": "requires_biometric", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.biometric_profile", "from": "operator_verification", "to": "requires_operator_verification", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.biometric_profile", "from": "duplicate_face_check", "to": "has_duplicate_face_check", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.biometric_profile", "from": "liveness_check", "to": "has_liveness_check", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.biometric_profile", "from": "operator_fallback", "to": "has_operator_fallback", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.consumption_rule", "from": "one_per_attraction", "to": "is_one_per_attraction", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.credential_issuance_retry_policy", "from": "automatic_retry", "to": "has_automatic_retry", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.credential_policy", "from": "before_first_validation_only", "to": "is_before_first_validation_only", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.credential_policy", "from": "return_to_sender", "to": "returns_to_sender", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.credential_security_profile", "from": "offline_ready", "to": "is_offline_ready", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.device_configuration", "from": "offline_capability", "to": "supports_offline", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.device_configuration", "from": "biometric_capability", "to": "supports_biometric", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.edge_package", "from": "signature_valid", "to": "is_signature_valid", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.edge_package", "from": "package_complete", "to": "is_package_complete", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.edge_package", "from": "version_valid", "to": "is_version_valid", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.entry_rule_point", "from": "admission_profile_id", "to": "admission_rules_id", "on": "2026-10-14",
     "why": "CHG-STO-005: a key column is named for the table it references (naming-and-style 6.1)"},
    {"table": "access.fast_pass_profile", "from": "one_per_ride", "to": "is_one_per_ride", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.fraud_rule", "from": "offline_availability", "to": "is_offline_available", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.gate_lane", "from": "re_entry", "to": "allows_re_entry", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.gate_mode_policy", "from": "automatic_notification", "to": "has_automatic_notification", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.hardware_model", "from": "offline_capability", "to": "supports_offline", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.hardware_model", "from": "screen_capability", "to": "supports_screen", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.hardware_model", "from": "sound_capability", "to": "supports_sound", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.hardware_model", "from": "light_capability", "to": "supports_light", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.hardware_model", "from": "relay_controller_support", "to": "supports_relay_controller", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.hardware_model", "from": "payment_capability", "to": "supports_payment", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.media_encoding_profile", "from": "offline_capability", "to": "supports_offline", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.media_replacement_policy", "from": "supervisor_approval", "to": "requires_supervisor_approval", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.media_replacement_policy", "from": "identity_verification", "to": "requires_identity_verification", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.media_replacement_policy", "from": "reason_mandatory", "to": "requires_reason", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.media_template_version", "from": "controlled_rollout", "to": "has_controlled_rollout", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.media_type", "from": "temporary_media", "to": "is_temporary_media", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.media_type", "from": "one_time_use", "to": "is_one_time_use", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.media_type", "from": "automatic_expiration", "to": "has_automatic_expiration", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.offline_policy", "from": "automatic_switch", "to": "has_automatic_switch", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.operating_calendar_entry", "from": "attraction_validation", "to": "requires_attraction_validation", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "access.scan_event", "from": "ticket_id", "to": "entitlement_id", "on": "2026-10-14",
     "why": "CHG-STO-005: a key column is named for the table it references (naming-and-style 6.1)"},
    {"table": "access.verification_method_policy", "from": "lock_on_first_successful_access", "to": "locks_on_first_successful_access", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "accreditation.identity_conflict", "from": "differing_access", "to": "has_differing_access", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "accreditation.validity", "from": "renewal_requires_reverification", "to": "requires_renewal_reverification", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "ai.history_import", "from": "dry_run", "to": "is_dry_run", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "ai.model", "from": "tool_calling", "to": "supports_tool_calling", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "ai.model", "from": "structured_output", "to": "supports_structured_output", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "ai.policy", "from": "cache_answers", "to": "caches_answers", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "ai.policy", "from": "guardrail_short_circuit", "to": "has_guardrail_short_circuit", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "ai.proposed_action", "from": "interaction_id", "to": "activity_id", "on": "2026-10-14",
     "why": "CHG-STO-005: a key column is named for the table it references (naming-and-style 6.1)"},
    {"table": "ai.provider", "from": "degrade_gracefully", "to": "degrades_gracefully", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "ai.risk_assessment", "from": "fell_back", "to": "did_fall_back", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "ai.tool", "from": "validate_only", "to": "is_validation_only", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "approvals.decision", "from": "used_mfa", "to": "did_use_mfa", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "approvals.request", "from": "reroute_on_no_approver", "to": "reroutes_on_no_approver", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "approvals.retention_policy", "from": "retain_signatures", "to": "retains_signatures", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "approvals.retention_policy", "from": "retain_attachments", "to": "retains_attachments", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "approvals.sla_policy", "from": "business_hours_only", "to": "is_business_hours_only", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "assets.distribution_channel", "from": "signed_urls", "to": "uses_signed_urls", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "catalogue.approval_policy", "from": "creator_cannot_give_final_approval", "to": "is_creator_barred_from_final_approval", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "catalogue.dynamic_pricing_control", "from": "exclude_protected_rates", "to": "excludes_protected_rates", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "catalogue.event_registration", "from": "capture_per_attendee", "to": "captures_per_attendee", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "catalogue.event_reschedule", "from": "refund_fees", "to": "refunds_fees", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "catalogue.event_schedule", "from": "duration_is_dynamic", "to": "is_duration_dynamic", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "catalogue.event_schedule", "from": "cascade_overrun", "to": "cascades_overrun", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "catalogue.event_type", "from": "ticket_names_date", "to": "is_ticket_dated", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "catalogue.event_type", "from": "multi_day", "to": "is_multi_day", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "catalogue.lifecycle_action", "from": "pre_action_validation", "to": "requires_pre_action_validation", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "catalogue.performance_media", "from": "participant_id", "to": "event_registration_id", "on": "2026-10-14",
     "why": "CHG-STO-005: a key column is named for the table it references (naming-and-style 6.1)"},
    {"table": "catalogue.prepaid_minutes", "from": "band_multipliers_apply", "to": "applies_band_multipliers", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "catalogue.prepaid_minutes", "from": "transferable_within_household", "to": "is_transferable_within_household", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "catalogue.price_execution", "from": "price_inconsistency", "to": "has_price_inconsistency", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "catalogue.pricing_experiment", "from": "statistical_significance", "to": "is_statistically_significant", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "catalogue.product", "from": "blocked_offline", "to": "is_blocked_offline", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "catalogue.product_eligibility_rule", "from": "refundable_if_ineligible_at_gate", "to": "is_refundable_if_ineligible_at_gate", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "control.cell_cluster", "from": "accepting_new_tenants", "to": "is_accepting_new_tenants", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "control.cell_tenant", "from": "pinned_instance", "to": "is_instance_pinned", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "control.partner_agreement", "from": "renewal_requires_approval", "to": "requires_renewal_approval", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "control.partner_billing_profile", "from": "consolidated_billing", "to": "has_consolidated_billing", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "control.partner_rate", "from": "seasonal_rate", "to": "is_seasonal_rate", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "control.partner_scope_assignment", "from": "seasonal_scope", "to": "is_seasonal_scope", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "control.seo_metadata", "from": "no_index", "to": "is_excluded_from_index", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "control.upgrade_schedule", "from": "deferred_by_tenant", "to": "is_deferred_by_tenant", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "fnb.delivery_policy", "from": "cutlery_opt_in", "to": "is_cutlery_opted_in", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "fnb.location_session", "from": "joined_existing_visit", "to": "has_joined_existing_visit", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "fnb.service_charge_policy", "from": "included_in_display_price", "to": "is_included_in_display_price", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "fnb.service_charge_policy", "from": "shown_separately", "to": "is_shown_separately", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "fnb.table_session", "from": "joined_existing_visit", "to": "has_joined_existing_visit", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "games.authorisation", "from": "decided_offline", "to": "was_decided_offline", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "games.card_expiry_rules", "from": "extend_on_recharge", "to": "extends_on_recharge", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "games.gameplay_transaction", "from": "decided_offline", "to": "was_decided_offline", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "games.redemption_rules", "from": "tickets_expire", "to": "has_expiring_tickets", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "identity.access_review_campaign", "from": "prefill_from_findings", "to": "prefills_from_findings", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "identity.guest_verification_policy", "from": "uae_pass_satisfies_id_document", "to": "accepts_uae_pass_as_id_document", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "identity.password_policy", "from": "force_change_on_first_logon", "to": "forces_change_on_first_logon", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "identity.segregation_rule", "from": "scope_sensitive", "to": "is_scope_sensitive", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "ledger.recognition_schedule", "from": "revalidate_on_validity_change", "to": "revalidates_on_validity_change", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "ledger.tax_exemption", "from": "evidence_document_id", "to": "evidence_asset_id", "on": "2026-10-14",
     "why": "CHG-STO-005: a key column is named for the table it references (naming-and-style 6.1)"},
    {"table": "maintenance.incident", "from": "first_aid_given", "to": "was_first_aid_given", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.audience_activation", "from": "enforce_consent", "to": "enforces_consent", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.campaign", "from": "optimise_channel", "to": "optimises_channel", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.case_routing_rule", "from": "respect_sla_capability", "to": "respects_sla_capability", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.case_routing_rule", "from": "sticky_ownership", "to": "has_sticky_ownership", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.communication_policy_decision", "from": "email_preference", "to": "prefers_email", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.communication_policy_decision", "from": "sms_preference", "to": "prefers_sms", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.communication_policy_decision", "from": "whatsapp_preference", "to": "prefers_whatsapp", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.communication_policy_decision", "from": "push_preference", "to": "prefers_push", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.communication_routing_rule", "from": "skip_unhealthy_providers", "to": "skips_unhealthy_providers", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.communication_routing_rule", "from": "cost_aware", "to": "is_cost_aware", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.consent_capture_point", "from": "skip_if_current_version_accepted", "to": "skips_if_current_version_accepted", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.contact_automation", "from": "kill_switch", "to": "is_kill_switch_engaged", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.conversation_message", "from": "ai_interaction_id", "to": "ai_activity_id", "on": "2026-10-14",
     "why": "CHG-STO-005: a key column is named for the table it references (naming-and-style 6.1)"},
    {"table": "marketing.cookie_banner_design", "from": "reject_is_one_click", "to": "is_reject_one_click", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.cookie_banner_design", "from": "record_ip_address", "to": "records_ip_address", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.device_consent", "from": "global_privacy_control", "to": "honours_global_privacy_control", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.guest_match_policy", "from": "offer_at_checkout", "to": "offers_at_checkout", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.guest_note", "from": "visible_to_server", "to": "is_visible_to_server", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.guest_relationship", "from": "shared_benefits", "to": "has_shared_benefits", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.minor_privacy_rule", "from": "restrict_marketing", "to": "restricts_marketing", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.minor_privacy_rule", "from": "restrict_tracking", "to": "restricts_tracking", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.minor_privacy_rule", "from": "restrict_personalisation", "to": "restricts_personalisation", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.privacy_request", "from": "at_risk", "to": "is_at_risk", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.quality_evaluation", "from": "sla_met", "to": "is_sla_met", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.review", "from": "response_is_public", "to": "is_response_public", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.service_copilot_config", "from": "reply_in_customer_language", "to": "replies_in_customer_language", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.sla_policy", "from": "business_hours_only", "to": "is_business_hours_only", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.waiver_signatory_rule", "from": "capture_relationship", "to": "captures_relationship", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.waiver_signatory_rule", "from": "guardian_signs_for_each_minor", "to": "requires_guardian_signature_per_minor", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.waiver_signature", "from": "template_id", "to": "form_definition_id", "on": "2026-10-14",
     "why": "CHG-STO-005: a key column is named for the table it references (naming-and-style 6.1)"},
    {"table": "marketing.waiver_verification", "from": "participant_match", "to": "is_participant_match", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.waiver_verification", "from": "booking_match", "to": "is_order_match", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.waiver_verification", "from": "guardian_relationship_present", "to": "is_guardian_relationship_present", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "marketing.waiver_verification", "from": "required_evidence_present", "to": "is_required_evidence_present", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "orders.after_sale_policy", "from": "void_same_business_day_only", "to": "is_void_same_business_day_only", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "orders.after_sale_policy", "from": "void_before_settlement_only", "to": "is_void_before_settlement_only", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "orders.after_sale_policy", "from": "void_before_ticket_use_only", "to": "is_void_before_ticket_use_only", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "orders.after_sale_policy", "from": "void_before_fiscal_closure_only", "to": "is_void_before_fiscal_closure_only", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "orders.after_sale_policy", "from": "void_dual_authorisation", "to": "requires_void_dual_authorisation", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "orders.group_ticket_allocation", "from": "keep_group_together", "to": "keeps_group_together", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "orders.group_ticket_allocation", "from": "vip_allocation", "to": "is_vip", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "orders.membership_migration", "from": "pro_rata", "to": "is_pro_rata", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "orders.order_line_eligibility", "from": "confident_swimmer", "to": "is_confident_swimmer", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "orders.payment_link", "from": "release_hold_on_expiry", "to": "releases_reservation_on_expiry", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "orders.resale_eligibility_rule", "from": "resale_immediately_after_purchase", "to": "allows_resale_immediately_after_purchase", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "orders.resale_eligibility_rule", "from": "original_purchaser_only", "to": "is_original_purchaser_only", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "orders.resale_fee_policy", "from": "fees_shown_to_seller", "to": "shows_fees_to_seller", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "orders.resale_marketplace_config", "from": "seller_can_edit_price", "to": "can_seller_edit_price", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "orders.reservation_hold_policy", "from": "extension_requires_approval", "to": "requires_extension_approval", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "orders.upgrade_rule", "from": "exclude_fees_from_credit", "to": "excludes_fees_from_credit", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "payments.credit_account", "from": "over_limit", "to": "is_over_limit", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "payments.failover_policy", "from": "failover_to_next_provider", "to": "fails_over_to_next_provider", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "payments.matching_rules", "from": "net_of_fees", "to": "is_net_of_fees", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "payments.provider", "from": "supports3ds", "to": "supports_3ds", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "payments.reconciliation_source", "from": "alert_if_missing", "to": "alerts_if_missing", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "promotions.recommendation_strategy", "from": "exclude_in_basket", "to": "excludes_in_basket", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "queue.queue", "from": "accessibility_priority", "to": "has_accessibility_priority", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "rental.agreement_rules", "from": "guardian_signature_for_minor", "to": "requires_guardian_signature_for_minor", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "rental.availability_rules", "from": "release_on_payment_failure", "to": "releases_on_payment_failure", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "rental.deposit_policy", "from": "inspection_required_before_release", "to": "requires_inspection_before_release", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "rental.equipment_assignment", "from": "assigned_manually", "to": "is_assigned_manually", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "rental.inventory_model", "from": "assignment_required_at_checkout", "to": "requires_assignment_at_checkout", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "reporting.delivery", "from": "contained_personal_data", "to": "did_contain_personal_data", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "reporting.kpi_definition", "from": "higher_is_better", "to": "is_higher_better", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "reporting.schedule", "from": "skip_if_empty", "to": "skips_if_empty", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "resources.allocation_policy", "from": "respect_resource_priority", "to": "respects_resource_priority", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "resources.selection_policy", "from": "ticket_type_id", "to": "ticket_product_id", "on": "2026-10-14",
     "why": "CHG-STO-005: a key column is named for the table it references (naming-and-style 6.1)"},
    {"table": "resources.venue_assignment", "from": "shared_pool", "to": "is_shared_across_venues", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "retail.shop_and_drop", "from": "collection_point_id", "to": "collection_location_id", "on": "2026-10-14",
     "why": "CHG-STO-005: a key column is named for the table it references (naming-and-style 6.1)"},
    {"table": "seating.hold_type", "from": "visible_to_guest", "to": "is_visible_to_guest", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "seating.reassignment", "from": "refund_issued", "to": "is_refund_issued", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "seating.recommendation_rule", "from": "reverse_row_order", "to": "reverses_row_order", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "seating.recommendation_rule", "from": "explain_to_guest", "to": "explains_to_guest", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "seating.seating_rules", "from": "prevent_orphan_seats", "to": "prevents_orphan_seats", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "subscription.membership_household_policy", "from": "eligibility_revalidation", "to": "requires_eligibility_revalidation", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "subscription.membership_product", "from": "promotional_pricing_eligibility", "to": "is_eligible_for_promotional_pricing", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "subscription.membership_product", "from": "separate_purchase_and_activation_rules", "to": "has_separate_purchase_and_activation_rules", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "control.tier_allowance", "from": "tier_id", "to": "plan_id", "on": "2026-10-14",
     "why": "CHG-STO-005: a key column is named for the table it references (naming-and-style 6.1)"},
    {"table": "control.tier_module", "from": "tier_id", "to": "plan_id", "on": "2026-10-14",
     "why": "CHG-STO-005: a key column is named for the table it references (naming-and-style 6.1)"},
    {"table": "control.trial_config", "from": "payment_method_required_up_front", "to": "requires_payment_method_up_front", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "sync.cross_region_entitlement", "from": "ticket_id", "to": "entitlement_id", "on": "2026-10-14",
     "why": "CHG-STO-005: a key column is named for the table it references (naming-and-style 6.1)"},
    {"table": "wallet.refund_policy", "from": "restore_to_original_lots", "to": "restores_to_original_lots", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "wallet.refund_policy", "from": "restore_original_expiry", "to": "restores_original_expiry", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "wallet.transfer_rule", "from": "within_shared_wallet_only", "to": "is_within_shared_wallet_only", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "wallet.voucher_type", "from": "single_use", "to": "is_single_use", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "wallet.wallet_type", "from": "stored_value_capability", "to": "supports_stored_value", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "wallet.wallet_type", "from": "top_up_capability", "to": "supports_top_up", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "wallet.wallet_type", "from": "transfer_capability", "to": "supports_transfer", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "wallet.wallet_type", "from": "refund_capability", "to": "supports_refund", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "wallet.wallet_type", "from": "gift_card_support", "to": "supports_gift_card", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "wallet.wallet_type", "from": "voucher_support", "to": "supports_voucher", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "wallet.wallet_type", "from": "membership_credit_support", "to": "supports_membership_credit", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "wallet.wallet_type", "from": "wearable_support", "to": "supports_wearable", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "wallet.wallet_type", "from": "holder_may_differ_from_owner", "to": "can_holder_differ_from_owner", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "whitelabel.app_build", "from": "submit_to_store", "to": "submits_to_store", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "whitelabel.site_setup_progress", "from": "minimum_path_done", "to": "is_minimum_path_done", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "workforce.leave_request", "from": "half_day", "to": "is_half_day", "on": "2026-10-14",
     "why": "CHG-STO-009: a boolean reads as an assertion (naming-and-style 6.1)"},
    {"table": "catalogue.channel_envelope", "from": "envelope_id", "to": "channel_capacity_id", "on": "2026-10-14",
     "why": "CHG-STO-005: a key column is named for the table it references (naming-and-style 6.1); the contract's channelCapacityId"},
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
