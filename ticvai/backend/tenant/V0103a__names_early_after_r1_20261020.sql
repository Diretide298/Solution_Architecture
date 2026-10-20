-- V0103a -- tenant database, after r1 (9cec72d) (20261020): the names the contracts use.
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), but the schema reference has renamed columns,
-- added foreign keys and stopped generating some indexes since. Migrations written from the baseline DDL
-- create the old names; this file brings a database built from them to the names the contracts use.
-- Every statement is a guarded block: it does nothing when its table, key or index is not there yet, or is
-- there already under the new name, so the file can be applied twice and in any database. A table created
-- by a migration that runs after this one copies the blocks that name it (ticket text: 'Changes this file
-- makes to your tables'). A foreign key is added NOT VALID: it checks every new write, and the owner runs
-- ALTER TABLE ... VALIDATE CONSTRAINT when the rows already there are known to be clean.
-- 18 table(s) renamed or moved, 20 column rename(s), 46 key(s) added, renamed or dropped, 34 index(es) renamed or dropped, the row-level security policies of 15 table(s) renamed.
--
-- **This file runs before V0104__after_r1_20261015.sql**: the renames the package declares (tools/derive-schema-history.py
-- RENAMES and COLUMN_RENAMES), each with the keys, indexes, checks and row-level security policies named for
-- it, so V0104__after_r1_20261015.sql and every file after it see the names the contracts use (a frozen file that applies
-- row-level security on a column by its new name stops a fresh database without it). A table moved into another
-- schema keeps its objects' names. A rename a frozen file still needs under its old name runs in the names
-- file after that one. The keys and indexes that do not follow a rename are in V0109.

-- catalogue.channel_envelope | rename table | catalogue.channel_allocation to channel_envelope
DO $$ BEGIN IF to_regclass('catalogue.channel_allocation') IS NOT NULL AND to_regclass('catalogue.channel_envelope') IS NULL THEN ALTER TABLE catalogue.channel_allocation RENAME TO channel_envelope; END IF; END $$;

-- catalogue.inventory_reservation | rename table | catalogue.inventory_hold to inventory_reservation
DO $$ BEGIN IF to_regclass('catalogue.inventory_hold') IS NOT NULL AND to_regclass('catalogue.inventory_reservation') IS NULL THEN ALTER TABLE catalogue.inventory_hold RENAME TO inventory_reservation; END IF; END $$;

-- inventory.inventory_item | rename table | inventory.item to inventory_item
DO $$ BEGIN IF to_regclass('inventory.item') IS NOT NULL AND to_regclass('inventory.inventory_item') IS NULL THEN ALTER TABLE inventory.item RENAME TO inventory_item; END IF; END $$;

-- inventory.stock_earmark | rename table | inventory.stock_reservation to stock_earmark
DO $$ BEGIN IF to_regclass('inventory.stock_reservation') IS NOT NULL AND to_regclass('inventory.stock_earmark') IS NULL THEN ALTER TABLE inventory.stock_reservation RENAME TO stock_earmark; END IF; END $$;

-- orders.group_customer_organisation | rename table | orders.group_customer_organization to group_customer_organisation
DO $$ BEGIN IF to_regclass('orders.group_customer_organization') IS NOT NULL AND to_regclass('orders.group_customer_organisation') IS NULL THEN ALTER TABLE orders.group_customer_organization RENAME TO group_customer_organisation; END IF; END $$;

-- orders.group_customer_organisation_contact | rename table | orders.group_customer_organization_contact to group_customer_organisation_contact
DO $$ BEGIN IF to_regclass('orders.group_customer_organization_contact') IS NOT NULL AND to_regclass('orders.group_customer_organisation_contact') IS NULL THEN ALTER TABLE orders.group_customer_organization_contact RENAME TO group_customer_organisation_contact; END IF; END $$;

-- resources.resource_reservation | rename table | resources.resource_hold to resource_reservation
DO $$ BEGIN IF to_regclass('resources.resource_hold') IS NOT NULL AND to_regclass('resources.resource_reservation') IS NULL THEN ALTER TABLE resources.resource_hold RENAME TO resource_reservation; END IF; END $$;

-- seating.recommendation_rule | rename table | seating.recommendation_rules to recommendation_rule
DO $$ BEGIN IF to_regclass('seating.recommendation_rules') IS NOT NULL AND to_regclass('seating.recommendation_rule') IS NULL THEN ALTER TABLE seating.recommendation_rules RENAME TO recommendation_rule; END IF; END $$;

-- seating.seat_reservation | rename table | seating.seat_hold to seat_reservation
DO $$ BEGIN IF to_regclass('seating.seat_hold') IS NOT NULL AND to_regclass('seating.seat_reservation') IS NULL THEN ALTER TABLE seating.seat_hold RENAME TO seat_reservation; END IF; END $$;

-- seating.seat_reservation_item | rename table | seating.seat_hold_item to seat_reservation_item
DO $$ BEGIN IF to_regclass('seating.seat_hold_item') IS NOT NULL AND to_regclass('seating.seat_reservation_item') IS NULL THEN ALTER TABLE seating.seat_hold_item RENAME TO seat_reservation_item; END IF; END $$;

-- sync.cross_region_entitlement | move table | platform.cross_region_entitlement to sync
DO $$ BEGIN IF to_regclass('platform.cross_region_entitlement') IS NOT NULL AND to_regclass('sync.cross_region_entitlement') IS NULL THEN ALTER TABLE platform.cross_region_entitlement SET SCHEMA sync; END IF; END $$;

-- sync.guest_link | move table | platform.guest_link to sync
DO $$ BEGIN IF to_regclass('platform.guest_link') IS NOT NULL AND to_regclass('sync.guest_link') IS NULL THEN ALTER TABLE platform.guest_link SET SCHEMA sync; END IF; END $$;

-- sync.wallet_authorisation | move table | platform.wallet_authorisation to sync
DO $$ BEGIN IF to_regclass('platform.wallet_authorisation') IS NOT NULL AND to_regclass('sync.wallet_authorisation') IS NULL THEN ALTER TABLE platform.wallet_authorisation SET SCHEMA sync; END IF; END $$;

-- wallet.channel_rule | rename table | wallet.channel_rules to channel_rule
DO $$ BEGIN IF to_regclass('wallet.channel_rules') IS NOT NULL AND to_regclass('wallet.channel_rule') IS NULL THEN ALTER TABLE wallet.channel_rules RENAME TO channel_rule; END IF; END $$;

-- wallet.fund_reservation | rename table | wallet.hold to fund_reservation
DO $$ BEGIN IF to_regclass('wallet.hold') IS NOT NULL AND to_regclass('wallet.fund_reservation') IS NULL THEN ALTER TABLE wallet.hold RENAME TO fund_reservation; END IF; END $$;

-- wallet.funding_rule | rename table | wallet.funding_rules to funding_rule
DO $$ BEGIN IF to_regclass('wallet.funding_rules') IS NOT NULL AND to_regclass('wallet.funding_rule') IS NULL THEN ALTER TABLE wallet.funding_rules RENAME TO funding_rule; END IF; END $$;

-- wallet.risk_rule_set | rename table | wallet.risk_rules to risk_rule_set
DO $$ BEGIN IF to_regclass('wallet.risk_rules') IS NOT NULL AND to_regclass('wallet.risk_rule_set') IS NULL THEN ALTER TABLE wallet.risk_rules RENAME TO risk_rule_set; END IF; END $$;

-- wallet.transfer_rule | rename table | wallet.transfer_rules to transfer_rule
DO $$ BEGIN IF to_regclass('wallet.transfer_rules') IS NOT NULL AND to_regclass('wallet.transfer_rule') IS NULL THEN ALTER TABLE wallet.transfer_rules RENAME TO transfer_rule; END IF; END $$;

-- catalogue.channel_envelope | rename column | envelope_id to channel_capacity_id
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'channel_envelope' AND column_name = 'envelope_id') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'channel_envelope' AND column_name = 'channel_capacity_id') THEN ALTER TABLE catalogue.channel_envelope RENAME COLUMN envelope_id TO channel_capacity_id; END IF; END $$;

-- catalogue.channel_envelope | rename column | allocation_type to envelope_type
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'channel_envelope' AND column_name = 'allocation_type') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'channel_envelope' AND column_name = 'envelope_type') THEN ALTER TABLE catalogue.channel_envelope RENAME COLUMN allocation_type TO envelope_type; END IF; END $$;

-- inventory.inventory_item | rename column | last_purchase_price to last_purchase_cost_amount
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'inventory' AND table_name = 'inventory_item' AND column_name = 'last_purchase_price') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'inventory' AND table_name = 'inventory_item' AND column_name = 'last_purchase_cost_amount') THEN ALTER TABLE inventory.inventory_item RENAME COLUMN last_purchase_price TO last_purchase_cost_amount; END IF; END $$;

-- orders.group_customer_organisation_contact | rename column | group_customer_organization_id to group_customer_organisation_id
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_customer_organisation_contact' AND column_name = 'group_customer_organization_id') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_customer_organisation_contact' AND column_name = 'group_customer_organisation_id') THEN ALTER TABLE orders.group_customer_organisation_contact RENAME COLUMN group_customer_organization_id TO group_customer_organisation_id; END IF; END $$;

-- seating.recommendation_rule | rename column | explain_to_guest to explains_to_guest
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'recommendation_rule' AND column_name = 'explain_to_guest') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'recommendation_rule' AND column_name = 'explains_to_guest') THEN ALTER TABLE seating.recommendation_rule RENAME COLUMN explain_to_guest TO explains_to_guest; END IF; END $$;

-- seating.recommendation_rule | rename column | reverse_row_order to reverses_row_order
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'recommendation_rule' AND column_name = 'reverse_row_order') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'recommendation_rule' AND column_name = 'reverses_row_order') THEN ALTER TABLE seating.recommendation_rule RENAME COLUMN reverse_row_order TO reverses_row_order; END IF; END $$;

-- seating.seat_reservation_item | rename column | held_price to gross_amount
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'seat_reservation_item' AND column_name = 'held_price') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'seat_reservation_item' AND column_name = 'gross_amount') THEN ALTER TABLE seating.seat_reservation_item RENAME COLUMN held_price TO gross_amount; END IF; END $$;

-- seating.seat_reservation_item | rename column | hold_id to seat_reservation_id
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'seat_reservation_item' AND column_name = 'hold_id') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'seat_reservation_item' AND column_name = 'seat_reservation_id') THEN ALTER TABLE seating.seat_reservation_item RENAME COLUMN hold_id TO seat_reservation_id; END IF; END $$;

-- sync.cross_region_entitlement | rename column | ticket_id to entitlement_id
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'sync' AND table_name = 'cross_region_entitlement' AND column_name = 'ticket_id') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'sync' AND table_name = 'cross_region_entitlement' AND column_name = 'entitlement_id') THEN ALTER TABLE sync.cross_region_entitlement RENAME COLUMN ticket_id TO entitlement_id; END IF; END $$;

-- sync.wallet_authorisation | rename column | wallet_hold_id to fund_reservation_id
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'sync' AND table_name = 'wallet_authorisation' AND column_name = 'wallet_hold_id') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'sync' AND table_name = 'wallet_authorisation' AND column_name = 'fund_reservation_id') THEN ALTER TABLE sync.wallet_authorisation RENAME COLUMN wallet_hold_id TO fund_reservation_id; END IF; END $$;

-- wallet.fund_reservation | rename column | wallet_hold_amount to reserved_amount
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'wallet' AND table_name = 'fund_reservation' AND column_name = 'wallet_hold_amount') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'wallet' AND table_name = 'fund_reservation' AND column_name = 'reserved_amount') THEN ALTER TABLE wallet.fund_reservation RENAME COLUMN wallet_hold_amount TO reserved_amount; END IF; END $$;

-- wallet.fund_reservation | rename column | wallet_hold_status to status
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'wallet' AND table_name = 'fund_reservation' AND column_name = 'wallet_hold_status') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'wallet' AND table_name = 'fund_reservation' AND column_name = 'status') THEN ALTER TABLE wallet.fund_reservation RENAME COLUMN wallet_hold_status TO status; END IF; END $$;

-- wallet.transfer_rule | rename column | within_shared_wallet_only to is_within_shared_wallet_only
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'wallet' AND table_name = 'transfer_rule' AND column_name = 'within_shared_wallet_only') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'wallet' AND table_name = 'transfer_rule' AND column_name = 'is_within_shared_wallet_only') THEN ALTER TABLE wallet.transfer_rule RENAME COLUMN within_shared_wallet_only TO is_within_shared_wallet_only; END IF; END $$;

-- access.access_change | rename column | old_access_id to old_entitlement_id
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'access' AND table_name = 'access_change' AND column_name = 'old_access_id') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'access' AND table_name = 'access_change' AND column_name = 'old_entitlement_id') THEN ALTER TABLE access.access_change RENAME COLUMN old_access_id TO old_entitlement_id; END IF; END $$;

-- access.entry_rule_point | rename column | admission_profile_id to admission_rules_id
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'access' AND table_name = 'entry_rule_point' AND column_name = 'admission_profile_id') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'access' AND table_name = 'entry_rule_point' AND column_name = 'admission_rules_id') THEN ALTER TABLE access.entry_rule_point RENAME COLUMN admission_profile_id TO admission_rules_id; END IF; END $$;

-- marketing.waiver_signature | rename column | template_id to form_definition_id
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'waiver_signature' AND column_name = 'template_id') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'waiver_signature' AND column_name = 'form_definition_id') THEN ALTER TABLE marketing.waiver_signature RENAME COLUMN template_id TO form_definition_id; END IF; END $$;

-- marketing.wishlist_item | rename column | price to list_price
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'wishlist_item' AND column_name = 'price') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'wishlist_item' AND column_name = 'list_price') THEN ALTER TABLE marketing.wishlist_item RENAME COLUMN price TO list_price; END IF; END $$;

-- platform.sale_board_tile | rename column | page_id to sale_board_page_id
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'sale_board_tile' AND column_name = 'page_id') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'sale_board_tile' AND column_name = 'sale_board_page_id') THEN ALTER TABLE platform.sale_board_tile RENAME COLUMN page_id TO sale_board_page_id; END IF; END $$;

-- platform.venue_settings | rename column | cash_drawer_limit to deposit_box_limit_amount
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'venue_settings' AND column_name = 'cash_drawer_limit') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'venue_settings' AND column_name = 'deposit_box_limit_amount') THEN ALTER TABLE platform.venue_settings RENAME COLUMN cash_drawer_limit TO deposit_box_limit_amount; END IF; END $$;

-- platform.workstation | rename column | cash_drawer_limit to deposit_box_limit_amount
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'workstation' AND column_name = 'cash_drawer_limit') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'workstation' AND column_name = 'deposit_box_limit_amount') THEN ALTER TABLE platform.workstation RENAME COLUMN cash_drawer_limit TO deposit_box_limit_amount; END IF; END $$;

-- catalogue.channel_envelope | rename index | channel_allocation_envelope_id_idx to channel_envelope_channel_capacity_id_idx
DO $$ BEGIN IF to_regclass('catalogue.channel_allocation_envelope_id_idx') IS NOT NULL AND to_regclass('catalogue.channel_envelope_channel_capacity_id_idx') IS NULL THEN ALTER INDEX catalogue.channel_allocation_envelope_id_idx RENAME TO channel_envelope_channel_capacity_id_idx; END IF; END $$;

-- catalogue.channel_envelope | rename index | channel_allocation_sales_channel_id_idx to channel_envelope_sales_channel_id_idx
DO $$ BEGIN IF to_regclass('catalogue.channel_allocation_sales_channel_id_idx') IS NOT NULL AND to_regclass('catalogue.channel_envelope_sales_channel_id_idx') IS NULL THEN ALTER INDEX catalogue.channel_allocation_sales_channel_id_idx RENAME TO channel_envelope_sales_channel_id_idx; END IF; END $$;

-- catalogue.channel_envelope | rename constraint | channel_allocation_envelope_id_fkey to channel_envelope_channel_capacity_id_fkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'channel_allocation_envelope_id_fkey' AND conrelid = to_regclass('catalogue.channel_envelope')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'channel_envelope_channel_capacity_id_fkey' AND conrelid = to_regclass('catalogue.channel_envelope')) THEN ALTER TABLE catalogue.channel_envelope RENAME CONSTRAINT channel_allocation_envelope_id_fkey TO channel_envelope_channel_capacity_id_fkey; END IF; END $$;

-- catalogue.channel_envelope | rename constraint | channel_allocation_channel_chk to channel_envelope_channel_chk
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'channel_allocation_channel_chk' AND conrelid = to_regclass('catalogue.channel_envelope')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'channel_envelope_channel_chk' AND conrelid = to_regclass('catalogue.channel_envelope')) THEN ALTER TABLE catalogue.channel_envelope RENAME CONSTRAINT channel_allocation_channel_chk TO channel_envelope_channel_chk; END IF; END $$;

-- catalogue.channel_envelope | rename constraint | channel_allocation_allocation_type_chk to channel_envelope_envelope_type_chk
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'channel_allocation_allocation_type_chk' AND conrelid = to_regclass('catalogue.channel_envelope')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'channel_envelope_envelope_type_chk' AND conrelid = to_regclass('catalogue.channel_envelope')) THEN ALTER TABLE catalogue.channel_envelope RENAME CONSTRAINT channel_allocation_allocation_type_chk TO channel_envelope_envelope_type_chk; END IF; END $$;

-- catalogue.channel_envelope | rename constraint | channel_allocation_waitlist_behavior_chk to channel_envelope_waitlist_behavior_chk
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'channel_allocation_waitlist_behavior_chk' AND conrelid = to_regclass('catalogue.channel_envelope')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'channel_envelope_waitlist_behavior_chk' AND conrelid = to_regclass('catalogue.channel_envelope')) THEN ALTER TABLE catalogue.channel_envelope RENAME CONSTRAINT channel_allocation_waitlist_behavior_chk TO channel_envelope_waitlist_behavior_chk; END IF; END $$;

-- catalogue.channel_envelope | rename constraint | channel_allocation_pkey to channel_envelope_pkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'channel_allocation_pkey' AND conrelid = to_regclass('catalogue.channel_envelope')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'channel_envelope_pkey' AND conrelid = to_regclass('catalogue.channel_envelope')) THEN ALTER TABLE catalogue.channel_envelope RENAME CONSTRAINT channel_allocation_pkey TO channel_envelope_pkey; END IF; END $$;

-- catalogue.channel_envelope | rename policy | channel_allocation_* to channel_envelope_*
DO $$ DECLARE p name; BEGIN IF to_regclass('catalogue.channel_envelope') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('catalogue.channel_envelope') AND left(polname, 19) = 'channel_allocation_' LOOP EXECUTE format('ALTER POLICY %I ON catalogue.channel_envelope RENAME TO %I', p, CASE WHEN substr(p, 19) = '_scope' THEN left('channel_envelope', 57) ELSE left('channel_envelope', 55) END || substr(p, 19)); END LOOP; END IF; END $$;

-- catalogue.inventory_reservation | rename index | inventory_hold_channel_capacity_id_idx to inventory_reservation_channel_capacity_id_idx
DO $$ BEGIN IF to_regclass('catalogue.inventory_hold_channel_capacity_id_idx') IS NOT NULL AND to_regclass('catalogue.inventory_reservation_channel_capacity_id_idx') IS NULL THEN ALTER INDEX catalogue.inventory_hold_channel_capacity_id_idx RENAME TO inventory_reservation_channel_capacity_id_idx; END IF; END $$;

-- catalogue.inventory_reservation | rename index | inventory_hold_force_released_by_principal_id_idx to inventory_reservation_force_released_by_principal_id_idx
DO $$ BEGIN IF to_regclass('catalogue.inventory_hold_force_released_by_principal_id_idx') IS NOT NULL AND to_regclass('catalogue.inventory_reservation_force_released_by_principal_id_idx') IS NULL THEN ALTER INDEX catalogue.inventory_hold_force_released_by_principal_id_idx RENAME TO inventory_reservation_force_released_by_principal_id_idx; END IF; END $$;

-- catalogue.inventory_reservation | rename index | inventory_hold_holder_cart_id_idx to inventory_reservation_holder_cart_id_idx
DO $$ BEGIN IF to_regclass('catalogue.inventory_hold_holder_cart_id_idx') IS NOT NULL AND to_regclass('catalogue.inventory_reservation_holder_cart_id_idx') IS NULL THEN ALTER INDEX catalogue.inventory_hold_holder_cart_id_idx RENAME TO inventory_reservation_holder_cart_id_idx; END IF; END $$;

-- catalogue.inventory_reservation | rename index | inventory_hold_holder_workstation_id_idx to inventory_reservation_holder_workstation_id_idx
DO $$ BEGIN IF to_regclass('catalogue.inventory_hold_holder_workstation_id_idx') IS NOT NULL AND to_regclass('catalogue.inventory_reservation_holder_workstation_id_idx') IS NULL THEN ALTER INDEX catalogue.inventory_hold_holder_workstation_id_idx RENAME TO inventory_reservation_holder_workstation_id_idx; END IF; END $$;

-- catalogue.inventory_reservation | rename constraint | inventory_hold_channel_capacity_id_fkey to inventory_reservation_channel_capacity_id_fkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_hold_channel_capacity_id_fkey' AND conrelid = to_regclass('catalogue.inventory_reservation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_reservation_channel_capacity_id_fkey' AND conrelid = to_regclass('catalogue.inventory_reservation')) THEN ALTER TABLE catalogue.inventory_reservation RENAME CONSTRAINT inventory_hold_channel_capacity_id_fkey TO inventory_reservation_channel_capacity_id_fkey; END IF; END $$;

-- catalogue.inventory_reservation | rename constraint | inventory_hold_force_released_by_principal_id_fkey to inventory_reservation_force_released_by_principal_id_fkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_hold_force_released_by_principal_id_fkey' AND conrelid = to_regclass('catalogue.inventory_reservation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_reservation_force_released_by_principal_id_fkey' AND conrelid = to_regclass('catalogue.inventory_reservation')) THEN ALTER TABLE catalogue.inventory_reservation RENAME CONSTRAINT inventory_hold_force_released_by_principal_id_fkey TO inventory_reservation_force_released_by_principal_id_fkey; END IF; END $$;

-- catalogue.inventory_reservation | rename constraint | inventory_hold_holder_workstation_id_fkey to inventory_reservation_holder_workstation_id_fkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_hold_holder_workstation_id_fkey' AND conrelid = to_regclass('catalogue.inventory_reservation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_reservation_holder_workstation_id_fkey' AND conrelid = to_regclass('catalogue.inventory_reservation')) THEN ALTER TABLE catalogue.inventory_reservation RENAME CONSTRAINT inventory_hold_holder_workstation_id_fkey TO inventory_reservation_holder_workstation_id_fkey; END IF; END $$;

-- catalogue.inventory_reservation | rename constraint | inventory_hold_holder_kind_chk to inventory_reservation_holder_kind_chk
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_hold_holder_kind_chk' AND conrelid = to_regclass('catalogue.inventory_reservation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_reservation_holder_kind_chk' AND conrelid = to_regclass('catalogue.inventory_reservation')) THEN ALTER TABLE catalogue.inventory_reservation RENAME CONSTRAINT inventory_hold_holder_kind_chk TO inventory_reservation_holder_kind_chk; END IF; END $$;

-- catalogue.inventory_reservation | rename constraint | inventory_hold_status_chk to inventory_reservation_status_chk
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_hold_status_chk' AND conrelid = to_regclass('catalogue.inventory_reservation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_reservation_status_chk' AND conrelid = to_regclass('catalogue.inventory_reservation')) THEN ALTER TABLE catalogue.inventory_reservation RENAME CONSTRAINT inventory_hold_status_chk TO inventory_reservation_status_chk; END IF; END $$;

-- catalogue.inventory_reservation | rename constraint | inventory_hold_pkey to inventory_reservation_pkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_hold_pkey' AND conrelid = to_regclass('catalogue.inventory_reservation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_reservation_pkey' AND conrelid = to_regclass('catalogue.inventory_reservation')) THEN ALTER TABLE catalogue.inventory_reservation RENAME CONSTRAINT inventory_hold_pkey TO inventory_reservation_pkey; END IF; END $$;

-- catalogue.inventory_reservation | rename policy | inventory_hold_* to inventory_reservation_*
DO $$ DECLARE p name; BEGIN IF to_regclass('catalogue.inventory_reservation') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('catalogue.inventory_reservation') AND left(polname, 15) = 'inventory_hold_' LOOP EXECUTE format('ALTER POLICY %I ON catalogue.inventory_reservation RENAME TO %I', p, CASE WHEN substr(p, 15) = '_scope' THEN left('inventory_reservation', 57) ELSE left('inventory_reservation', 55) END || substr(p, 15)); END LOOP; END IF; END $$;

-- inventory.inventory_item | rename index | item_preferred_supplier_id_idx to inventory_item_preferred_supplier_id_idx
DO $$ BEGIN IF to_regclass('inventory.item_preferred_supplier_id_idx') IS NOT NULL AND to_regclass('inventory.inventory_item_preferred_supplier_id_idx') IS NULL THEN ALTER INDEX inventory.item_preferred_supplier_id_idx RENAME TO inventory_item_preferred_supplier_id_idx; END IF; END $$;

-- inventory.inventory_item | rename index | item_venue_id_idx to inventory_item_venue_id_idx
DO $$ BEGIN IF to_regclass('inventory.item_venue_id_idx') IS NOT NULL AND to_regclass('inventory.inventory_item_venue_id_idx') IS NULL THEN ALTER INDEX inventory.item_venue_id_idx RENAME TO inventory_item_venue_id_idx; END IF; END $$;

-- inventory.inventory_item | rename constraint | item_preferred_supplier_id_fkey to inventory_item_preferred_supplier_id_fkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'item_preferred_supplier_id_fkey' AND conrelid = to_regclass('inventory.inventory_item')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_item_preferred_supplier_id_fkey' AND conrelid = to_regclass('inventory.inventory_item')) THEN ALTER TABLE inventory.inventory_item RENAME CONSTRAINT item_preferred_supplier_id_fkey TO inventory_item_preferred_supplier_id_fkey; END IF; END $$;

-- inventory.inventory_item | rename constraint | item_venue_id_fkey to inventory_item_venue_id_fkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'item_venue_id_fkey' AND conrelid = to_regclass('inventory.inventory_item')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_item_venue_id_fkey' AND conrelid = to_regclass('inventory.inventory_item')) THEN ALTER TABLE inventory.inventory_item RENAME CONSTRAINT item_venue_id_fkey TO inventory_item_venue_id_fkey; END IF; END $$;

-- inventory.inventory_item | rename constraint | item_barcode_chk to inventory_item_barcode_chk
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'item_barcode_chk' AND conrelid = to_regclass('inventory.inventory_item')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_item_barcode_chk' AND conrelid = to_regclass('inventory.inventory_item')) THEN ALTER TABLE inventory.inventory_item RENAME CONSTRAINT item_barcode_chk TO inventory_item_barcode_chk; END IF; END $$;

-- inventory.inventory_item | rename constraint | item_costing_method_chk to inventory_item_costing_method_chk
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'item_costing_method_chk' AND conrelid = to_regclass('inventory.inventory_item')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_item_costing_method_chk' AND conrelid = to_regclass('inventory.inventory_item')) THEN ALTER TABLE inventory.inventory_item RENAME CONSTRAINT item_costing_method_chk TO inventory_item_costing_method_chk; END IF; END $$;

-- inventory.inventory_item | rename constraint | item_name_chk to inventory_item_name_chk
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'item_name_chk' AND conrelid = to_regclass('inventory.inventory_item')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_item_name_chk' AND conrelid = to_regclass('inventory.inventory_item')) THEN ALTER TABLE inventory.inventory_item RENAME CONSTRAINT item_name_chk TO inventory_item_name_chk; END IF; END $$;

-- inventory.inventory_item | rename constraint | item_sku_chk to inventory_item_sku_chk
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'item_sku_chk' AND conrelid = to_regclass('inventory.inventory_item')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_item_sku_chk' AND conrelid = to_regclass('inventory.inventory_item')) THEN ALTER TABLE inventory.inventory_item RENAME CONSTRAINT item_sku_chk TO inventory_item_sku_chk; END IF; END $$;

-- inventory.inventory_item | rename constraint | item_pkey to inventory_item_pkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'item_pkey' AND conrelid = to_regclass('inventory.inventory_item')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'inventory_item_pkey' AND conrelid = to_regclass('inventory.inventory_item')) THEN ALTER TABLE inventory.inventory_item RENAME CONSTRAINT item_pkey TO inventory_item_pkey; END IF; END $$;

-- inventory.inventory_item | rename policy | item_* to inventory_item_*
DO $$ DECLARE p name; BEGIN IF to_regclass('inventory.inventory_item') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('inventory.inventory_item') AND left(polname, 5) = 'item_' LOOP EXECUTE format('ALTER POLICY %I ON inventory.inventory_item RENAME TO %I', p, CASE WHEN substr(p, 5) = '_scope' THEN left('inventory_item', 57) ELSE left('inventory_item', 55) END || substr(p, 5)); END LOOP; END IF; END $$;

-- inventory.stock_earmark | rename index | stock_reservation_item_id_idx to stock_earmark_item_id_idx
DO $$ BEGIN IF to_regclass('inventory.stock_reservation_item_id_idx') IS NOT NULL AND to_regclass('inventory.stock_earmark_item_id_idx') IS NULL THEN ALTER INDEX inventory.stock_reservation_item_id_idx RENAME TO stock_earmark_item_id_idx; END IF; END $$;

-- inventory.stock_earmark | rename index | stock_reservation_location_id_idx to stock_earmark_location_id_idx
DO $$ BEGIN IF to_regclass('inventory.stock_reservation_location_id_idx') IS NOT NULL AND to_regclass('inventory.stock_earmark_location_id_idx') IS NULL THEN ALTER INDEX inventory.stock_reservation_location_id_idx RENAME TO stock_earmark_location_id_idx; END IF; END $$;

-- inventory.stock_earmark | rename constraint | stock_reservation_source_type_chk to stock_earmark_source_type_chk
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'stock_reservation_source_type_chk' AND conrelid = to_regclass('inventory.stock_earmark')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'stock_earmark_source_type_chk' AND conrelid = to_regclass('inventory.stock_earmark')) THEN ALTER TABLE inventory.stock_earmark RENAME CONSTRAINT stock_reservation_source_type_chk TO stock_earmark_source_type_chk; END IF; END $$;

-- inventory.stock_earmark | rename constraint | stock_reservation_status_chk to stock_earmark_status_chk
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'stock_reservation_status_chk' AND conrelid = to_regclass('inventory.stock_earmark')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'stock_earmark_status_chk' AND conrelid = to_regclass('inventory.stock_earmark')) THEN ALTER TABLE inventory.stock_earmark RENAME CONSTRAINT stock_reservation_status_chk TO stock_earmark_status_chk; END IF; END $$;

-- inventory.stock_earmark | rename constraint | stock_reservation_pkey to stock_earmark_pkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'stock_reservation_pkey' AND conrelid = to_regclass('inventory.stock_earmark')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'stock_earmark_pkey' AND conrelid = to_regclass('inventory.stock_earmark')) THEN ALTER TABLE inventory.stock_earmark RENAME CONSTRAINT stock_reservation_pkey TO stock_earmark_pkey; END IF; END $$;

-- inventory.stock_earmark | rename policy | stock_reservation_* to stock_earmark_*
DO $$ DECLARE p name; BEGIN IF to_regclass('inventory.stock_earmark') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('inventory.stock_earmark') AND left(polname, 18) = 'stock_reservation_' LOOP EXECUTE format('ALTER POLICY %I ON inventory.stock_earmark RENAME TO %I', p, CASE WHEN substr(p, 18) = '_scope' THEN left('stock_earmark', 57) ELSE left('stock_earmark', 55) END || substr(p, 18)); END LOOP; END IF; END $$;

-- orders.group_customer_organisation | rename constraint | group_customer_organization_name_chk to group_customer_organisation_name_chk
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'group_customer_organization_name_chk' AND conrelid = to_regclass('orders.group_customer_organisation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'group_customer_organisation_name_chk' AND conrelid = to_regclass('orders.group_customer_organisation')) THEN ALTER TABLE orders.group_customer_organisation RENAME CONSTRAINT group_customer_organization_name_chk TO group_customer_organisation_name_chk; END IF; END $$;

-- orders.group_customer_organisation | rename constraint | group_customer_organization_organisation_type_chk to group_customer_organisation_organisation_type_chk
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'group_customer_organization_organisation_type_chk' AND conrelid = to_regclass('orders.group_customer_organisation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'group_customer_organisation_organisation_type_chk' AND conrelid = to_regclass('orders.group_customer_organisation')) THEN ALTER TABLE orders.group_customer_organisation RENAME CONSTRAINT group_customer_organization_organisation_type_chk TO group_customer_organisation_organisation_type_chk; END IF; END $$;

-- orders.group_customer_organisation | rename constraint | group_customer_organization_pkey to group_customer_organisation_pkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'group_customer_organization_pkey' AND conrelid = to_regclass('orders.group_customer_organisation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'group_customer_organisation_pkey' AND conrelid = to_regclass('orders.group_customer_organisation')) THEN ALTER TABLE orders.group_customer_organisation RENAME CONSTRAINT group_customer_organization_pkey TO group_customer_organisation_pkey; END IF; END $$;

-- orders.group_customer_organisation | rename policy | group_customer_organization_* to group_customer_organisation_*
DO $$ DECLARE p name; BEGIN IF to_regclass('orders.group_customer_organisation') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('orders.group_customer_organisation') AND left(polname, 28) = 'group_customer_organization_' LOOP EXECUTE format('ALTER POLICY %I ON orders.group_customer_organisation RENAME TO %I', p, CASE WHEN substr(p, 28) = '_scope' THEN left('group_customer_organisation', 57) ELSE left('group_customer_organisation', 55) END || substr(p, 28)); END LOOP; END IF; END $$;

-- orders.group_customer_organisation_contact | rename index | group_customer_organization_contact_group_customer_a397067a_idx to group_customer_organisation_contact_group_customer_2ad51596_idx
DO $$ BEGIN IF to_regclass('orders.group_customer_organization_contact_group_customer_a397067a_idx') IS NOT NULL AND to_regclass('orders.group_customer_organisation_contact_group_customer_2ad51596_idx') IS NULL THEN ALTER INDEX orders.group_customer_organization_contact_group_customer_a397067a_idx RENAME TO group_customer_organisation_contact_group_customer_2ad51596_idx; END IF; END $$;

-- orders.group_customer_organisation_contact | rename constraint | group_customer_organization_contact_group_custome_942e0f58_fkey to group_customer_organisation_contact_group_custome_3b68685a_fkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'group_customer_organization_contact_group_custome_942e0f58_fkey' AND conrelid = to_regclass('orders.group_customer_organisation_contact')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'group_customer_organisation_contact_group_custome_3b68685a_fkey' AND conrelid = to_regclass('orders.group_customer_organisation_contact')) THEN ALTER TABLE orders.group_customer_organisation_contact RENAME CONSTRAINT group_customer_organization_contact_group_custome_942e0f58_fkey TO group_customer_organisation_contact_group_custome_3b68685a_fkey; END IF; END $$;

-- orders.group_customer_organisation_contact | rename constraint | group_customer_organization_contact_pkey to group_customer_organisation_contact_pkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'group_customer_organization_contact_pkey' AND conrelid = to_regclass('orders.group_customer_organisation_contact')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'group_customer_organisation_contact_pkey' AND conrelid = to_regclass('orders.group_customer_organisation_contact')) THEN ALTER TABLE orders.group_customer_organisation_contact RENAME CONSTRAINT group_customer_organization_contact_pkey TO group_customer_organisation_contact_pkey; END IF; END $$;

-- orders.group_customer_organisation_contact | rename policy | group_customer_organization_contact_* to group_customer_organisation_contact_*
DO $$ DECLARE p name; BEGIN IF to_regclass('orders.group_customer_organisation_contact') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('orders.group_customer_organisation_contact') AND left(polname, 36) = 'group_customer_organization_contact_' LOOP EXECUTE format('ALTER POLICY %I ON orders.group_customer_organisation_contact RENAME TO %I', p, CASE WHEN substr(p, 36) = '_scope' THEN left('group_customer_organisation_contact', 57) ELSE left('group_customer_organisation_contact', 55) END || substr(p, 36)); END LOOP; END IF; END $$;

-- resources.resource_reservation | rename index | resource_hold_held_by_principal_id_idx to resource_reservation_held_by_principal_id_idx
DO $$ BEGIN IF to_regclass('resources.resource_hold_held_by_principal_id_idx') IS NOT NULL AND to_regclass('resources.resource_reservation_held_by_principal_id_idx') IS NULL THEN ALTER INDEX resources.resource_hold_held_by_principal_id_idx RENAME TO resource_reservation_held_by_principal_id_idx; END IF; END $$;

-- resources.resource_reservation | rename index | resource_hold_map_id_idx to resource_reservation_map_id_idx
DO $$ BEGIN IF to_regclass('resources.resource_hold_map_id_idx') IS NOT NULL AND to_regclass('resources.resource_reservation_map_id_idx') IS NULL THEN ALTER INDEX resources.resource_hold_map_id_idx RENAME TO resource_reservation_map_id_idx; END IF; END $$;

-- resources.resource_reservation | rename index | resource_hold_scope_path_idx to resource_reservation_scope_path_idx
DO $$ BEGIN IF to_regclass('resources.resource_hold_scope_path_idx') IS NOT NULL AND to_regclass('resources.resource_reservation_scope_path_idx') IS NULL THEN ALTER INDEX resources.resource_hold_scope_path_idx RENAME TO resource_reservation_scope_path_idx; END IF; END $$;

-- resources.resource_reservation | rename index | resource_hold_subject_id_idx to resource_reservation_subject_id_idx
DO $$ BEGIN IF to_regclass('resources.resource_hold_subject_id_idx') IS NOT NULL AND to_regclass('resources.resource_reservation_subject_id_idx') IS NULL THEN ALTER INDEX resources.resource_hold_subject_id_idx RENAME TO resource_reservation_subject_id_idx; END IF; END $$;

-- resources.resource_reservation | rename constraint | resource_hold_status_chk to resource_reservation_status_chk
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'resource_hold_status_chk' AND conrelid = to_regclass('resources.resource_reservation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'resource_reservation_status_chk' AND conrelid = to_regclass('resources.resource_reservation')) THEN ALTER TABLE resources.resource_reservation RENAME CONSTRAINT resource_hold_status_chk TO resource_reservation_status_chk; END IF; END $$;

-- resources.resource_reservation | rename constraint | resource_hold_pkey to resource_reservation_pkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'resource_hold_pkey' AND conrelid = to_regclass('resources.resource_reservation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'resource_reservation_pkey' AND conrelid = to_regclass('resources.resource_reservation')) THEN ALTER TABLE resources.resource_reservation RENAME CONSTRAINT resource_hold_pkey TO resource_reservation_pkey; END IF; END $$;

-- resources.resource_reservation | rename policy | resource_hold_* to resource_reservation_*
DO $$ DECLARE p name; BEGIN IF to_regclass('resources.resource_reservation') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('resources.resource_reservation') AND left(polname, 14) = 'resource_hold_' LOOP EXECUTE format('ALTER POLICY %I ON resources.resource_reservation RENAME TO %I', p, CASE WHEN substr(p, 14) = '_scope' THEN left('resource_reservation', 57) ELSE left('resource_reservation', 55) END || substr(p, 14)); END LOOP; END IF; END $$;

-- seating.recommendation_rule | rename index | recommendation_rules_performance_id_idx to recommendation_rule_performance_id_idx
DO $$ BEGIN IF to_regclass('seating.recommendation_rules_performance_id_idx') IS NOT NULL AND to_regclass('seating.recommendation_rule_performance_id_idx') IS NULL THEN ALTER INDEX seating.recommendation_rules_performance_id_idx RENAME TO recommendation_rule_performance_id_idx; END IF; END $$;

-- seating.recommendation_rule | rename index | recommendation_rules_scope_path_idx to recommendation_rule_scope_path_idx
DO $$ BEGIN IF to_regclass('seating.recommendation_rules_scope_path_idx') IS NOT NULL AND to_regclass('seating.recommendation_rule_scope_path_idx') IS NULL THEN ALTER INDEX seating.recommendation_rules_scope_path_idx RENAME TO recommendation_rule_scope_path_idx; END IF; END $$;

-- seating.recommendation_rule | rename index | recommendation_rules_seat_map_id_idx to recommendation_rule_seat_map_id_idx
DO $$ BEGIN IF to_regclass('seating.recommendation_rules_seat_map_id_idx') IS NOT NULL AND to_regclass('seating.recommendation_rule_seat_map_id_idx') IS NULL THEN ALTER INDEX seating.recommendation_rules_seat_map_id_idx RENAME TO recommendation_rule_seat_map_id_idx; END IF; END $$;

-- seating.recommendation_rule | rename constraint | recommendation_rules_pkey to recommendation_rule_pkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'recommendation_rules_pkey' AND conrelid = to_regclass('seating.recommendation_rule')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'recommendation_rule_pkey' AND conrelid = to_regclass('seating.recommendation_rule')) THEN ALTER TABLE seating.recommendation_rule RENAME CONSTRAINT recommendation_rules_pkey TO recommendation_rule_pkey; END IF; END $$;

-- seating.recommendation_rule | rename policy | recommendation_rules_* to recommendation_rule_*
DO $$ DECLARE p name; BEGIN IF to_regclass('seating.recommendation_rule') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('seating.recommendation_rule') AND left(polname, 21) = 'recommendation_rules_' LOOP EXECUTE format('ALTER POLICY %I ON seating.recommendation_rule RENAME TO %I', p, CASE WHEN substr(p, 21) = '_scope' THEN left('recommendation_rule', 57) ELSE left('recommendation_rule', 55) END || substr(p, 21)); END LOOP; END IF; END $$;

-- seating.seat_reservation | rename index | seat_hold_block_id_idx to seat_reservation_block_id_idx
DO $$ BEGIN IF to_regclass('seating.seat_hold_block_id_idx') IS NOT NULL AND to_regclass('seating.seat_reservation_block_id_idx') IS NULL THEN ALTER INDEX seating.seat_hold_block_id_idx RENAME TO seat_reservation_block_id_idx; END IF; END $$;

-- seating.seat_reservation | rename index | seat_hold_held_by_principal_id_idx to seat_reservation_held_by_principal_id_idx
DO $$ BEGIN IF to_regclass('seating.seat_hold_held_by_principal_id_idx') IS NOT NULL AND to_regclass('seating.seat_reservation_held_by_principal_id_idx') IS NULL THEN ALTER INDEX seating.seat_hold_held_by_principal_id_idx RENAME TO seat_reservation_held_by_principal_id_idx; END IF; END $$;

-- seating.seat_reservation | rename index | seat_hold_performance_id_idx to seat_reservation_performance_id_idx
DO $$ BEGIN IF to_regclass('seating.seat_hold_performance_id_idx') IS NOT NULL AND to_regclass('seating.seat_reservation_performance_id_idx') IS NULL THEN ALTER INDEX seating.seat_hold_performance_id_idx RENAME TO seat_reservation_performance_id_idx; END IF; END $$;

-- seating.seat_reservation | rename index | seat_hold_subject_id_idx to seat_reservation_subject_id_idx
DO $$ BEGIN IF to_regclass('seating.seat_hold_subject_id_idx') IS NOT NULL AND to_regclass('seating.seat_reservation_subject_id_idx') IS NULL THEN ALTER INDEX seating.seat_hold_subject_id_idx RENAME TO seat_reservation_subject_id_idx; END IF; END $$;

-- seating.seat_reservation | rename constraint | seat_hold_block_id_fkey to seat_reservation_block_id_fkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'seat_hold_block_id_fkey' AND conrelid = to_regclass('seating.seat_reservation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'seat_reservation_block_id_fkey' AND conrelid = to_regclass('seating.seat_reservation')) THEN ALTER TABLE seating.seat_reservation RENAME CONSTRAINT seat_hold_block_id_fkey TO seat_reservation_block_id_fkey; END IF; END $$;

-- seating.seat_reservation | rename constraint | seat_hold_held_by_principal_id_fkey to seat_reservation_held_by_principal_id_fkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'seat_hold_held_by_principal_id_fkey' AND conrelid = to_regclass('seating.seat_reservation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'seat_reservation_held_by_principal_id_fkey' AND conrelid = to_regclass('seating.seat_reservation')) THEN ALTER TABLE seating.seat_reservation RENAME CONSTRAINT seat_hold_held_by_principal_id_fkey TO seat_reservation_held_by_principal_id_fkey; END IF; END $$;

-- seating.seat_reservation | rename constraint | seat_hold_performance_id_fkey to seat_reservation_performance_id_fkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'seat_hold_performance_id_fkey' AND conrelid = to_regclass('seating.seat_reservation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'seat_reservation_performance_id_fkey' AND conrelid = to_regclass('seating.seat_reservation')) THEN ALTER TABLE seating.seat_reservation RENAME CONSTRAINT seat_hold_performance_id_fkey TO seat_reservation_performance_id_fkey; END IF; END $$;

-- seating.seat_reservation | rename constraint | seat_hold_subject_id_fkey to seat_reservation_subject_id_fkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'seat_hold_subject_id_fkey' AND conrelid = to_regclass('seating.seat_reservation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'seat_reservation_subject_id_fkey' AND conrelid = to_regclass('seating.seat_reservation')) THEN ALTER TABLE seating.seat_reservation RENAME CONSTRAINT seat_hold_subject_id_fkey TO seat_reservation_subject_id_fkey; END IF; END $$;

-- seating.seat_reservation | rename constraint | seat_hold_status_chk to seat_reservation_status_chk
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'seat_hold_status_chk' AND conrelid = to_regclass('seating.seat_reservation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'seat_reservation_status_chk' AND conrelid = to_regclass('seating.seat_reservation')) THEN ALTER TABLE seating.seat_reservation RENAME CONSTRAINT seat_hold_status_chk TO seat_reservation_status_chk; END IF; END $$;

-- seating.seat_reservation | rename constraint | seat_hold_pkey to seat_reservation_pkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'seat_hold_pkey' AND conrelid = to_regclass('seating.seat_reservation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'seat_reservation_pkey' AND conrelid = to_regclass('seating.seat_reservation')) THEN ALTER TABLE seating.seat_reservation RENAME CONSTRAINT seat_hold_pkey TO seat_reservation_pkey; END IF; END $$;

-- seating.seat_reservation | rename policy | seat_hold_* to seat_reservation_*
DO $$ DECLARE p name; BEGIN IF to_regclass('seating.seat_reservation') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('seating.seat_reservation') AND left(polname, 10) = 'seat_hold_' LOOP EXECUTE format('ALTER POLICY %I ON seating.seat_reservation RENAME TO %I', p, CASE WHEN substr(p, 10) = '_scope' THEN left('seat_reservation', 57) ELSE left('seat_reservation', 55) END || substr(p, 10)); END LOOP; END IF; END $$;

-- seating.seat_reservation_item | rename index | seat_hold_item_hold_id_idx to seat_reservation_item_seat_reservation_id_idx
DO $$ BEGIN IF to_regclass('seating.seat_hold_item_hold_id_idx') IS NOT NULL AND to_regclass('seating.seat_reservation_item_seat_reservation_id_idx') IS NULL THEN ALTER INDEX seating.seat_hold_item_hold_id_idx RENAME TO seat_reservation_item_seat_reservation_id_idx; END IF; END $$;

-- seating.seat_reservation_item | rename index | seat_hold_item_seat_id_idx to seat_reservation_item_seat_id_idx
DO $$ BEGIN IF to_regclass('seating.seat_hold_item_seat_id_idx') IS NOT NULL AND to_regclass('seating.seat_reservation_item_seat_id_idx') IS NULL THEN ALTER INDEX seating.seat_hold_item_seat_id_idx RENAME TO seat_reservation_item_seat_id_idx; END IF; END $$;

-- seating.seat_reservation_item | rename constraint | seat_hold_item_pkey to seat_reservation_item_pkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'seat_hold_item_pkey' AND conrelid = to_regclass('seating.seat_reservation_item')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'seat_reservation_item_pkey' AND conrelid = to_regclass('seating.seat_reservation_item')) THEN ALTER TABLE seating.seat_reservation_item RENAME CONSTRAINT seat_hold_item_pkey TO seat_reservation_item_pkey; END IF; END $$;

-- seating.seat_reservation_item | rename policy | seat_hold_item_* to seat_reservation_item_*
DO $$ DECLARE p name; BEGIN IF to_regclass('seating.seat_reservation_item') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('seating.seat_reservation_item') AND left(polname, 15) = 'seat_hold_item_' LOOP EXECUTE format('ALTER POLICY %I ON seating.seat_reservation_item RENAME TO %I', p, CASE WHEN substr(p, 15) = '_scope' THEN left('seat_reservation_item', 57) ELSE left('seat_reservation_item', 55) END || substr(p, 15)); END LOOP; END IF; END $$;

-- sync.cross_region_entitlement | rename index | cross_region_entitlement_ticket_id_idx to cross_region_entitlement_entitlement_id_idx
DO $$ BEGIN IF to_regclass('sync.cross_region_entitlement_ticket_id_idx') IS NOT NULL AND to_regclass('sync.cross_region_entitlement_entitlement_id_idx') IS NULL THEN ALTER INDEX sync.cross_region_entitlement_ticket_id_idx RENAME TO cross_region_entitlement_entitlement_id_idx; END IF; END $$;

-- sync.cross_region_entitlement | rename constraint | cross_region_entitlement_ticket_id_fkey to cross_region_entitlement_entitlement_id_fkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'cross_region_entitlement_ticket_id_fkey' AND conrelid = to_regclass('sync.cross_region_entitlement')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'cross_region_entitlement_entitlement_id_fkey' AND conrelid = to_regclass('sync.cross_region_entitlement')) THEN ALTER TABLE sync.cross_region_entitlement RENAME CONSTRAINT cross_region_entitlement_ticket_id_fkey TO cross_region_entitlement_entitlement_id_fkey; END IF; END $$;

-- sync.wallet_authorisation | rename index | wallet_authorisation_wallet_hold_id_idx to wallet_authorisation_fund_reservation_id_idx
DO $$ BEGIN IF to_regclass('sync.wallet_authorisation_wallet_hold_id_idx') IS NOT NULL AND to_regclass('sync.wallet_authorisation_fund_reservation_id_idx') IS NULL THEN ALTER INDEX sync.wallet_authorisation_wallet_hold_id_idx RENAME TO wallet_authorisation_fund_reservation_id_idx; END IF; END $$;

-- sync.wallet_authorisation | rename constraint | wallet_authorisation_wallet_hold_id_fkey to wallet_authorisation_fund_reservation_id_fkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'wallet_authorisation_wallet_hold_id_fkey' AND conrelid = to_regclass('sync.wallet_authorisation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'wallet_authorisation_fund_reservation_id_fkey' AND conrelid = to_regclass('sync.wallet_authorisation')) THEN ALTER TABLE sync.wallet_authorisation RENAME CONSTRAINT wallet_authorisation_wallet_hold_id_fkey TO wallet_authorisation_fund_reservation_id_fkey; END IF; END $$;

-- wallet.channel_rule | rename index | channel_rules_scope_path_idx to channel_rule_scope_path_idx
DO $$ BEGIN IF to_regclass('wallet.channel_rules_scope_path_idx') IS NOT NULL AND to_regclass('wallet.channel_rule_scope_path_idx') IS NULL THEN ALTER INDEX wallet.channel_rules_scope_path_idx RENAME TO channel_rule_scope_path_idx; END IF; END $$;

-- wallet.channel_rule | rename constraint | channel_rules_pkey to channel_rule_pkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'channel_rules_pkey' AND conrelid = to_regclass('wallet.channel_rule')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'channel_rule_pkey' AND conrelid = to_regclass('wallet.channel_rule')) THEN ALTER TABLE wallet.channel_rule RENAME CONSTRAINT channel_rules_pkey TO channel_rule_pkey; END IF; END $$;

-- wallet.channel_rule | rename policy | channel_rules_* to channel_rule_*
DO $$ DECLARE p name; BEGIN IF to_regclass('wallet.channel_rule') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('wallet.channel_rule') AND left(polname, 14) = 'channel_rules_' LOOP EXECUTE format('ALTER POLICY %I ON wallet.channel_rule RENAME TO %I', p, CASE WHEN substr(p, 14) = '_scope' THEN left('channel_rule', 57) ELSE left('channel_rule', 55) END || substr(p, 14)); END LOOP; END IF; END $$;

-- wallet.fund_reservation | rename index | hold_order_id_idx to fund_reservation_order_id_idx
DO $$ BEGIN IF to_regclass('wallet.hold_order_id_idx') IS NOT NULL AND to_regclass('wallet.fund_reservation_order_id_idx') IS NULL THEN ALTER INDEX wallet.hold_order_id_idx RENAME TO fund_reservation_order_id_idx; END IF; END $$;

-- wallet.fund_reservation | rename index | hold_payment_id_idx to fund_reservation_payment_id_idx
DO $$ BEGIN IF to_regclass('wallet.hold_payment_id_idx') IS NOT NULL AND to_regclass('wallet.fund_reservation_payment_id_idx') IS NULL THEN ALTER INDEX wallet.hold_payment_id_idx RENAME TO fund_reservation_payment_id_idx; END IF; END $$;

-- wallet.fund_reservation | rename index | hold_wallet_id_idx to fund_reservation_wallet_id_idx
DO $$ BEGIN IF to_regclass('wallet.hold_wallet_id_idx') IS NOT NULL AND to_regclass('wallet.fund_reservation_wallet_id_idx') IS NULL THEN ALTER INDEX wallet.hold_wallet_id_idx RENAME TO fund_reservation_wallet_id_idx; END IF; END $$;

-- wallet.fund_reservation | rename constraint | hold_order_id_fkey to fund_reservation_order_id_fkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'hold_order_id_fkey' AND conrelid = to_regclass('wallet.fund_reservation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fund_reservation_order_id_fkey' AND conrelid = to_regclass('wallet.fund_reservation')) THEN ALTER TABLE wallet.fund_reservation RENAME CONSTRAINT hold_order_id_fkey TO fund_reservation_order_id_fkey; END IF; END $$;

-- wallet.fund_reservation | rename constraint | hold_currency_code_chk to fund_reservation_currency_code_chk
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'hold_currency_code_chk' AND conrelid = to_regclass('wallet.fund_reservation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fund_reservation_currency_code_chk' AND conrelid = to_regclass('wallet.fund_reservation')) THEN ALTER TABLE wallet.fund_reservation RENAME CONSTRAINT hold_currency_code_chk TO fund_reservation_currency_code_chk; END IF; END $$;

-- wallet.fund_reservation | rename constraint | hold_wallet_hold_status_chk to fund_reservation_status_chk
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'hold_wallet_hold_status_chk' AND conrelid = to_regclass('wallet.fund_reservation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fund_reservation_status_chk' AND conrelid = to_regclass('wallet.fund_reservation')) THEN ALTER TABLE wallet.fund_reservation RENAME CONSTRAINT hold_wallet_hold_status_chk TO fund_reservation_status_chk; END IF; END $$;

-- wallet.fund_reservation | rename constraint | hold_pkey to fund_reservation_pkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'hold_pkey' AND conrelid = to_regclass('wallet.fund_reservation')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fund_reservation_pkey' AND conrelid = to_regclass('wallet.fund_reservation')) THEN ALTER TABLE wallet.fund_reservation RENAME CONSTRAINT hold_pkey TO fund_reservation_pkey; END IF; END $$;

-- wallet.fund_reservation | rename policy | hold_* to fund_reservation_*
DO $$ DECLARE p name; BEGIN IF to_regclass('wallet.fund_reservation') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('wallet.fund_reservation') AND left(polname, 5) = 'hold_' LOOP EXECUTE format('ALTER POLICY %I ON wallet.fund_reservation RENAME TO %I', p, CASE WHEN substr(p, 5) = '_scope' THEN left('fund_reservation', 57) ELSE left('fund_reservation', 55) END || substr(p, 5)); END LOOP; END IF; END $$;

-- wallet.funding_rule | rename index | funding_rules_scope_path_idx to funding_rule_scope_path_idx
DO $$ BEGIN IF to_regclass('wallet.funding_rules_scope_path_idx') IS NOT NULL AND to_regclass('wallet.funding_rule_scope_path_idx') IS NULL THEN ALTER INDEX wallet.funding_rules_scope_path_idx RENAME TO funding_rule_scope_path_idx; END IF; END $$;

-- wallet.funding_rule | rename index | funding_rules_wallet_type_id_idx to funding_rule_wallet_type_id_idx
DO $$ BEGIN IF to_regclass('wallet.funding_rules_wallet_type_id_idx') IS NOT NULL AND to_regclass('wallet.funding_rule_wallet_type_id_idx') IS NULL THEN ALTER INDEX wallet.funding_rules_wallet_type_id_idx RENAME TO funding_rule_wallet_type_id_idx; END IF; END $$;

-- wallet.funding_rule | rename constraint | funding_rules_pkey to funding_rule_pkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'funding_rules_pkey' AND conrelid = to_regclass('wallet.funding_rule')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'funding_rule_pkey' AND conrelid = to_regclass('wallet.funding_rule')) THEN ALTER TABLE wallet.funding_rule RENAME CONSTRAINT funding_rules_pkey TO funding_rule_pkey; END IF; END $$;

-- wallet.funding_rule | rename policy | funding_rules_* to funding_rule_*
DO $$ DECLARE p name; BEGIN IF to_regclass('wallet.funding_rule') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('wallet.funding_rule') AND left(polname, 14) = 'funding_rules_' LOOP EXECUTE format('ALTER POLICY %I ON wallet.funding_rule RENAME TO %I', p, CASE WHEN substr(p, 14) = '_scope' THEN left('funding_rule', 57) ELSE left('funding_rule', 55) END || substr(p, 14)); END LOOP; END IF; END $$;

-- wallet.risk_rule_set | rename index | risk_rules_scope_path_idx to risk_rule_set_scope_path_idx
DO $$ BEGIN IF to_regclass('wallet.risk_rules_scope_path_idx') IS NOT NULL AND to_regclass('wallet.risk_rule_set_scope_path_idx') IS NULL THEN ALTER INDEX wallet.risk_rules_scope_path_idx RENAME TO risk_rule_set_scope_path_idx; END IF; END $$;

-- wallet.risk_rule_set | rename constraint | risk_rules_pkey to risk_rule_set_pkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'risk_rules_pkey' AND conrelid = to_regclass('wallet.risk_rule_set')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'risk_rule_set_pkey' AND conrelid = to_regclass('wallet.risk_rule_set')) THEN ALTER TABLE wallet.risk_rule_set RENAME CONSTRAINT risk_rules_pkey TO risk_rule_set_pkey; END IF; END $$;

-- wallet.risk_rule_set | rename policy | risk_rules_* to risk_rule_set_*
DO $$ DECLARE p name; BEGIN IF to_regclass('wallet.risk_rule_set') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('wallet.risk_rule_set') AND left(polname, 11) = 'risk_rules_' LOOP EXECUTE format('ALTER POLICY %I ON wallet.risk_rule_set RENAME TO %I', p, CASE WHEN substr(p, 11) = '_scope' THEN left('risk_rule_set', 57) ELSE left('risk_rule_set', 55) END || substr(p, 11)); END LOOP; END IF; END $$;

-- wallet.transfer_rule | rename index | transfer_rules_scope_path_idx to transfer_rule_scope_path_idx
DO $$ BEGIN IF to_regclass('wallet.transfer_rules_scope_path_idx') IS NOT NULL AND to_regclass('wallet.transfer_rule_scope_path_idx') IS NULL THEN ALTER INDEX wallet.transfer_rules_scope_path_idx RENAME TO transfer_rule_scope_path_idx; END IF; END $$;

-- wallet.transfer_rule | rename constraint | transfer_rules_pkey to transfer_rule_pkey
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'transfer_rules_pkey' AND conrelid = to_regclass('wallet.transfer_rule')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'transfer_rule_pkey' AND conrelid = to_regclass('wallet.transfer_rule')) THEN ALTER TABLE wallet.transfer_rule RENAME CONSTRAINT transfer_rules_pkey TO transfer_rule_pkey; END IF; END $$;

-- wallet.transfer_rule | rename policy | transfer_rules_* to transfer_rule_*
DO $$ DECLARE p name; BEGIN IF to_regclass('wallet.transfer_rule') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('wallet.transfer_rule') AND left(polname, 15) = 'transfer_rules_' LOOP EXECUTE format('ALTER POLICY %I ON wallet.transfer_rule RENAME TO %I', p, CASE WHEN substr(p, 15) = '_scope' THEN left('transfer_rule', 57) ELSE left('transfer_rule', 55) END || substr(p, 15)); END LOOP; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0103a', 'after r1 (9cec72d), names the contracts use: 18 table(s) renamed or moved, 20 column rename(s), 46 key(s) added, renamed or dropped, 34 index(es) renamed or dropped, the row-level security policies of 15 table(s) renamed', 'dab4f46e7e2aa2752e56bb478e729a6c2081c9e5cf96ab9eafe03195054580a5')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DO $$ DECLARE p name; BEGIN IF to_regclass('wallet.transfer_rule') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('wallet.transfer_rule') AND left(polname, 14) = 'transfer_rule_' LOOP EXECUTE format('ALTER POLICY %I ON wallet.transfer_rule RENAME TO %I', p, CASE WHEN substr(p, 14) = '_scope' THEN left('transfer_rules', 57) ELSE left('transfer_rules', 55) END || substr(p, 14)); END LOOP; END IF; END $$;
-- ALTER TABLE wallet.transfer_rule RENAME CONSTRAINT transfer_rule_pkey TO transfer_rules_pkey;
-- ALTER INDEX wallet.transfer_rule_scope_path_idx RENAME TO transfer_rules_scope_path_idx;
-- DO $$ DECLARE p name; BEGIN IF to_regclass('wallet.risk_rule_set') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('wallet.risk_rule_set') AND left(polname, 14) = 'risk_rule_set_' LOOP EXECUTE format('ALTER POLICY %I ON wallet.risk_rule_set RENAME TO %I', p, CASE WHEN substr(p, 14) = '_scope' THEN left('risk_rules', 57) ELSE left('risk_rules', 55) END || substr(p, 14)); END LOOP; END IF; END $$;
-- ALTER TABLE wallet.risk_rule_set RENAME CONSTRAINT risk_rule_set_pkey TO risk_rules_pkey;
-- ALTER INDEX wallet.risk_rule_set_scope_path_idx RENAME TO risk_rules_scope_path_idx;
-- DO $$ DECLARE p name; BEGIN IF to_regclass('wallet.funding_rule') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('wallet.funding_rule') AND left(polname, 13) = 'funding_rule_' LOOP EXECUTE format('ALTER POLICY %I ON wallet.funding_rule RENAME TO %I', p, CASE WHEN substr(p, 13) = '_scope' THEN left('funding_rules', 57) ELSE left('funding_rules', 55) END || substr(p, 13)); END LOOP; END IF; END $$;
-- ALTER TABLE wallet.funding_rule RENAME CONSTRAINT funding_rule_pkey TO funding_rules_pkey;
-- ALTER INDEX wallet.funding_rule_wallet_type_id_idx RENAME TO funding_rules_wallet_type_id_idx;
-- ALTER INDEX wallet.funding_rule_scope_path_idx RENAME TO funding_rules_scope_path_idx;
-- DO $$ DECLARE p name; BEGIN IF to_regclass('wallet.fund_reservation') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('wallet.fund_reservation') AND left(polname, 17) = 'fund_reservation_' LOOP EXECUTE format('ALTER POLICY %I ON wallet.fund_reservation RENAME TO %I', p, CASE WHEN substr(p, 17) = '_scope' THEN left('hold', 57) ELSE left('hold', 55) END || substr(p, 17)); END LOOP; END IF; END $$;
-- ALTER TABLE wallet.fund_reservation RENAME CONSTRAINT fund_reservation_pkey TO hold_pkey;
-- ALTER TABLE wallet.fund_reservation RENAME CONSTRAINT fund_reservation_status_chk TO hold_wallet_hold_status_chk;
-- ALTER TABLE wallet.fund_reservation RENAME CONSTRAINT fund_reservation_currency_code_chk TO hold_currency_code_chk;
-- ALTER TABLE wallet.fund_reservation RENAME CONSTRAINT fund_reservation_order_id_fkey TO hold_order_id_fkey;
-- ALTER INDEX wallet.fund_reservation_wallet_id_idx RENAME TO hold_wallet_id_idx;
-- ALTER INDEX wallet.fund_reservation_payment_id_idx RENAME TO hold_payment_id_idx;
-- ALTER INDEX wallet.fund_reservation_order_id_idx RENAME TO hold_order_id_idx;
-- DO $$ DECLARE p name; BEGIN IF to_regclass('wallet.channel_rule') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('wallet.channel_rule') AND left(polname, 13) = 'channel_rule_' LOOP EXECUTE format('ALTER POLICY %I ON wallet.channel_rule RENAME TO %I', p, CASE WHEN substr(p, 13) = '_scope' THEN left('channel_rules', 57) ELSE left('channel_rules', 55) END || substr(p, 13)); END LOOP; END IF; END $$;
-- ALTER TABLE wallet.channel_rule RENAME CONSTRAINT channel_rule_pkey TO channel_rules_pkey;
-- ALTER INDEX wallet.channel_rule_scope_path_idx RENAME TO channel_rules_scope_path_idx;
-- ALTER TABLE sync.wallet_authorisation RENAME CONSTRAINT wallet_authorisation_fund_reservation_id_fkey TO wallet_authorisation_wallet_hold_id_fkey;
-- ALTER INDEX sync.wallet_authorisation_fund_reservation_id_idx RENAME TO wallet_authorisation_wallet_hold_id_idx;
-- ALTER TABLE sync.cross_region_entitlement RENAME CONSTRAINT cross_region_entitlement_entitlement_id_fkey TO cross_region_entitlement_ticket_id_fkey;
-- ALTER INDEX sync.cross_region_entitlement_entitlement_id_idx RENAME TO cross_region_entitlement_ticket_id_idx;
-- DO $$ DECLARE p name; BEGIN IF to_regclass('seating.seat_reservation_item') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('seating.seat_reservation_item') AND left(polname, 22) = 'seat_reservation_item_' LOOP EXECUTE format('ALTER POLICY %I ON seating.seat_reservation_item RENAME TO %I', p, CASE WHEN substr(p, 22) = '_scope' THEN left('seat_hold_item', 57) ELSE left('seat_hold_item', 55) END || substr(p, 22)); END LOOP; END IF; END $$;
-- ALTER TABLE seating.seat_reservation_item RENAME CONSTRAINT seat_reservation_item_pkey TO seat_hold_item_pkey;
-- ALTER INDEX seating.seat_reservation_item_seat_id_idx RENAME TO seat_hold_item_seat_id_idx;
-- ALTER INDEX seating.seat_reservation_item_seat_reservation_id_idx RENAME TO seat_hold_item_hold_id_idx;
-- DO $$ DECLARE p name; BEGIN IF to_regclass('seating.seat_reservation') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('seating.seat_reservation') AND left(polname, 17) = 'seat_reservation_' LOOP EXECUTE format('ALTER POLICY %I ON seating.seat_reservation RENAME TO %I', p, CASE WHEN substr(p, 17) = '_scope' THEN left('seat_hold', 57) ELSE left('seat_hold', 55) END || substr(p, 17)); END LOOP; END IF; END $$;
-- ALTER TABLE seating.seat_reservation RENAME CONSTRAINT seat_reservation_pkey TO seat_hold_pkey;
-- ALTER TABLE seating.seat_reservation RENAME CONSTRAINT seat_reservation_status_chk TO seat_hold_status_chk;
-- ALTER TABLE seating.seat_reservation RENAME CONSTRAINT seat_reservation_subject_id_fkey TO seat_hold_subject_id_fkey;
-- ALTER TABLE seating.seat_reservation RENAME CONSTRAINT seat_reservation_performance_id_fkey TO seat_hold_performance_id_fkey;
-- ALTER TABLE seating.seat_reservation RENAME CONSTRAINT seat_reservation_held_by_principal_id_fkey TO seat_hold_held_by_principal_id_fkey;
-- ALTER TABLE seating.seat_reservation RENAME CONSTRAINT seat_reservation_block_id_fkey TO seat_hold_block_id_fkey;
-- ALTER INDEX seating.seat_reservation_subject_id_idx RENAME TO seat_hold_subject_id_idx;
-- ALTER INDEX seating.seat_reservation_performance_id_idx RENAME TO seat_hold_performance_id_idx;
-- ALTER INDEX seating.seat_reservation_held_by_principal_id_idx RENAME TO seat_hold_held_by_principal_id_idx;
-- ALTER INDEX seating.seat_reservation_block_id_idx RENAME TO seat_hold_block_id_idx;
-- DO $$ DECLARE p name; BEGIN IF to_regclass('seating.recommendation_rule') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('seating.recommendation_rule') AND left(polname, 20) = 'recommendation_rule_' LOOP EXECUTE format('ALTER POLICY %I ON seating.recommendation_rule RENAME TO %I', p, CASE WHEN substr(p, 20) = '_scope' THEN left('recommendation_rules', 57) ELSE left('recommendation_rules', 55) END || substr(p, 20)); END LOOP; END IF; END $$;
-- ALTER TABLE seating.recommendation_rule RENAME CONSTRAINT recommendation_rule_pkey TO recommendation_rules_pkey;
-- ALTER INDEX seating.recommendation_rule_seat_map_id_idx RENAME TO recommendation_rules_seat_map_id_idx;
-- ALTER INDEX seating.recommendation_rule_scope_path_idx RENAME TO recommendation_rules_scope_path_idx;
-- ALTER INDEX seating.recommendation_rule_performance_id_idx RENAME TO recommendation_rules_performance_id_idx;
-- DO $$ DECLARE p name; BEGIN IF to_regclass('resources.resource_reservation') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('resources.resource_reservation') AND left(polname, 21) = 'resource_reservation_' LOOP EXECUTE format('ALTER POLICY %I ON resources.resource_reservation RENAME TO %I', p, CASE WHEN substr(p, 21) = '_scope' THEN left('resource_hold', 57) ELSE left('resource_hold', 55) END || substr(p, 21)); END LOOP; END IF; END $$;
-- ALTER TABLE resources.resource_reservation RENAME CONSTRAINT resource_reservation_pkey TO resource_hold_pkey;
-- ALTER TABLE resources.resource_reservation RENAME CONSTRAINT resource_reservation_status_chk TO resource_hold_status_chk;
-- ALTER INDEX resources.resource_reservation_subject_id_idx RENAME TO resource_hold_subject_id_idx;
-- ALTER INDEX resources.resource_reservation_scope_path_idx RENAME TO resource_hold_scope_path_idx;
-- ALTER INDEX resources.resource_reservation_map_id_idx RENAME TO resource_hold_map_id_idx;
-- ALTER INDEX resources.resource_reservation_held_by_principal_id_idx RENAME TO resource_hold_held_by_principal_id_idx;
-- DO $$ DECLARE p name; BEGIN IF to_regclass('orders.group_customer_organisation_contact') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('orders.group_customer_organisation_contact') AND left(polname, 36) = 'group_customer_organisation_contact_' LOOP EXECUTE format('ALTER POLICY %I ON orders.group_customer_organisation_contact RENAME TO %I', p, CASE WHEN substr(p, 36) = '_scope' THEN left('group_customer_organization_contact', 57) ELSE left('group_customer_organization_contact', 55) END || substr(p, 36)); END LOOP; END IF; END $$;
-- ALTER TABLE orders.group_customer_organisation_contact RENAME CONSTRAINT group_customer_organisation_contact_pkey TO group_customer_organization_contact_pkey;
-- ALTER TABLE orders.group_customer_organisation_contact RENAME CONSTRAINT group_customer_organisation_contact_group_custome_3b68685a_fkey TO group_customer_organization_contact_group_custome_942e0f58_fkey;
-- ALTER INDEX orders.group_customer_organisation_contact_group_customer_2ad51596_idx RENAME TO group_customer_organization_contact_group_customer_a397067a_idx;
-- DO $$ DECLARE p name; BEGIN IF to_regclass('orders.group_customer_organisation') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('orders.group_customer_organisation') AND left(polname, 28) = 'group_customer_organisation_' LOOP EXECUTE format('ALTER POLICY %I ON orders.group_customer_organisation RENAME TO %I', p, CASE WHEN substr(p, 28) = '_scope' THEN left('group_customer_organization', 57) ELSE left('group_customer_organization', 55) END || substr(p, 28)); END LOOP; END IF; END $$;
-- ALTER TABLE orders.group_customer_organisation RENAME CONSTRAINT group_customer_organisation_pkey TO group_customer_organization_pkey;
-- ALTER TABLE orders.group_customer_organisation RENAME CONSTRAINT group_customer_organisation_organisation_type_chk TO group_customer_organization_organisation_type_chk;
-- ALTER TABLE orders.group_customer_organisation RENAME CONSTRAINT group_customer_organisation_name_chk TO group_customer_organization_name_chk;
-- DO $$ DECLARE p name; BEGIN IF to_regclass('inventory.stock_earmark') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('inventory.stock_earmark') AND left(polname, 14) = 'stock_earmark_' LOOP EXECUTE format('ALTER POLICY %I ON inventory.stock_earmark RENAME TO %I', p, CASE WHEN substr(p, 14) = '_scope' THEN left('stock_reservation', 57) ELSE left('stock_reservation', 55) END || substr(p, 14)); END LOOP; END IF; END $$;
-- ALTER TABLE inventory.stock_earmark RENAME CONSTRAINT stock_earmark_pkey TO stock_reservation_pkey;
-- ALTER TABLE inventory.stock_earmark RENAME CONSTRAINT stock_earmark_status_chk TO stock_reservation_status_chk;
-- ALTER TABLE inventory.stock_earmark RENAME CONSTRAINT stock_earmark_source_type_chk TO stock_reservation_source_type_chk;
-- ALTER INDEX inventory.stock_earmark_location_id_idx RENAME TO stock_reservation_location_id_idx;
-- ALTER INDEX inventory.stock_earmark_item_id_idx RENAME TO stock_reservation_item_id_idx;
-- DO $$ DECLARE p name; BEGIN IF to_regclass('inventory.inventory_item') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('inventory.inventory_item') AND left(polname, 15) = 'inventory_item_' LOOP EXECUTE format('ALTER POLICY %I ON inventory.inventory_item RENAME TO %I', p, CASE WHEN substr(p, 15) = '_scope' THEN left('item', 57) ELSE left('item', 55) END || substr(p, 15)); END LOOP; END IF; END $$;
-- ALTER TABLE inventory.inventory_item RENAME CONSTRAINT inventory_item_pkey TO item_pkey;
-- ALTER TABLE inventory.inventory_item RENAME CONSTRAINT inventory_item_sku_chk TO item_sku_chk;
-- ALTER TABLE inventory.inventory_item RENAME CONSTRAINT inventory_item_name_chk TO item_name_chk;
-- ALTER TABLE inventory.inventory_item RENAME CONSTRAINT inventory_item_costing_method_chk TO item_costing_method_chk;
-- ALTER TABLE inventory.inventory_item RENAME CONSTRAINT inventory_item_barcode_chk TO item_barcode_chk;
-- ALTER TABLE inventory.inventory_item RENAME CONSTRAINT inventory_item_venue_id_fkey TO item_venue_id_fkey;
-- ALTER TABLE inventory.inventory_item RENAME CONSTRAINT inventory_item_preferred_supplier_id_fkey TO item_preferred_supplier_id_fkey;
-- ALTER INDEX inventory.inventory_item_venue_id_idx RENAME TO item_venue_id_idx;
-- ALTER INDEX inventory.inventory_item_preferred_supplier_id_idx RENAME TO item_preferred_supplier_id_idx;
-- DO $$ DECLARE p name; BEGIN IF to_regclass('catalogue.inventory_reservation') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('catalogue.inventory_reservation') AND left(polname, 22) = 'inventory_reservation_' LOOP EXECUTE format('ALTER POLICY %I ON catalogue.inventory_reservation RENAME TO %I', p, CASE WHEN substr(p, 22) = '_scope' THEN left('inventory_hold', 57) ELSE left('inventory_hold', 55) END || substr(p, 22)); END LOOP; END IF; END $$;
-- ALTER TABLE catalogue.inventory_reservation RENAME CONSTRAINT inventory_reservation_pkey TO inventory_hold_pkey;
-- ALTER TABLE catalogue.inventory_reservation RENAME CONSTRAINT inventory_reservation_status_chk TO inventory_hold_status_chk;
-- ALTER TABLE catalogue.inventory_reservation RENAME CONSTRAINT inventory_reservation_holder_kind_chk TO inventory_hold_holder_kind_chk;
-- ALTER TABLE catalogue.inventory_reservation RENAME CONSTRAINT inventory_reservation_holder_workstation_id_fkey TO inventory_hold_holder_workstation_id_fkey;
-- ALTER TABLE catalogue.inventory_reservation RENAME CONSTRAINT inventory_reservation_force_released_by_principal_id_fkey TO inventory_hold_force_released_by_principal_id_fkey;
-- ALTER TABLE catalogue.inventory_reservation RENAME CONSTRAINT inventory_reservation_channel_capacity_id_fkey TO inventory_hold_channel_capacity_id_fkey;
-- ALTER INDEX catalogue.inventory_reservation_holder_workstation_id_idx RENAME TO inventory_hold_holder_workstation_id_idx;
-- ALTER INDEX catalogue.inventory_reservation_holder_cart_id_idx RENAME TO inventory_hold_holder_cart_id_idx;
-- ALTER INDEX catalogue.inventory_reservation_force_released_by_principal_id_idx RENAME TO inventory_hold_force_released_by_principal_id_idx;
-- ALTER INDEX catalogue.inventory_reservation_channel_capacity_id_idx RENAME TO inventory_hold_channel_capacity_id_idx;
-- DO $$ DECLARE p name; BEGIN IF to_regclass('catalogue.channel_envelope') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('catalogue.channel_envelope') AND left(polname, 17) = 'channel_envelope_' LOOP EXECUTE format('ALTER POLICY %I ON catalogue.channel_envelope RENAME TO %I', p, CASE WHEN substr(p, 17) = '_scope' THEN left('channel_allocation', 57) ELSE left('channel_allocation', 55) END || substr(p, 17)); END LOOP; END IF; END $$;
-- ALTER TABLE catalogue.channel_envelope RENAME CONSTRAINT channel_envelope_pkey TO channel_allocation_pkey;
-- ALTER TABLE catalogue.channel_envelope RENAME CONSTRAINT channel_envelope_waitlist_behavior_chk TO channel_allocation_waitlist_behavior_chk;
-- ALTER TABLE catalogue.channel_envelope RENAME CONSTRAINT channel_envelope_envelope_type_chk TO channel_allocation_allocation_type_chk;
-- ALTER TABLE catalogue.channel_envelope RENAME CONSTRAINT channel_envelope_channel_chk TO channel_allocation_channel_chk;
-- ALTER TABLE catalogue.channel_envelope RENAME CONSTRAINT channel_envelope_channel_capacity_id_fkey TO channel_allocation_envelope_id_fkey;
-- ALTER INDEX catalogue.channel_envelope_sales_channel_id_idx RENAME TO channel_allocation_sales_channel_id_idx;
-- ALTER INDEX catalogue.channel_envelope_channel_capacity_id_idx RENAME TO channel_allocation_envelope_id_idx;
-- ALTER TABLE platform.workstation RENAME COLUMN deposit_box_limit_amount TO cash_drawer_limit;
-- ALTER TABLE platform.venue_settings RENAME COLUMN deposit_box_limit_amount TO cash_drawer_limit;
-- ALTER TABLE platform.sale_board_tile RENAME COLUMN sale_board_page_id TO page_id;
-- ALTER TABLE marketing.wishlist_item RENAME COLUMN list_price TO price;
-- ALTER TABLE marketing.waiver_signature RENAME COLUMN form_definition_id TO template_id;
-- ALTER TABLE access.entry_rule_point RENAME COLUMN admission_rules_id TO admission_profile_id;
-- ALTER TABLE access.access_change RENAME COLUMN old_entitlement_id TO old_access_id;
-- ALTER TABLE wallet.transfer_rule RENAME COLUMN is_within_shared_wallet_only TO within_shared_wallet_only;
-- ALTER TABLE wallet.fund_reservation RENAME COLUMN status TO wallet_hold_status;
-- ALTER TABLE wallet.fund_reservation RENAME COLUMN reserved_amount TO wallet_hold_amount;
-- ALTER TABLE sync.wallet_authorisation RENAME COLUMN fund_reservation_id TO wallet_hold_id;
-- ALTER TABLE sync.cross_region_entitlement RENAME COLUMN entitlement_id TO ticket_id;
-- ALTER TABLE seating.seat_reservation_item RENAME COLUMN seat_reservation_id TO hold_id;
-- ALTER TABLE seating.seat_reservation_item RENAME COLUMN gross_amount TO held_price;
-- ALTER TABLE seating.recommendation_rule RENAME COLUMN reverses_row_order TO reverse_row_order;
-- ALTER TABLE seating.recommendation_rule RENAME COLUMN explains_to_guest TO explain_to_guest;
-- ALTER TABLE orders.group_customer_organisation_contact RENAME COLUMN group_customer_organisation_id TO group_customer_organization_id;
-- ALTER TABLE inventory.inventory_item RENAME COLUMN last_purchase_cost_amount TO last_purchase_price;
-- ALTER TABLE catalogue.channel_envelope RENAME COLUMN envelope_type TO allocation_type;
-- ALTER TABLE catalogue.channel_envelope RENAME COLUMN channel_capacity_id TO envelope_id;
-- ALTER TABLE wallet.transfer_rule RENAME TO transfer_rules;
-- ALTER TABLE wallet.risk_rule_set RENAME TO risk_rules;
-- ALTER TABLE wallet.funding_rule RENAME TO funding_rules;
-- ALTER TABLE wallet.fund_reservation RENAME TO hold;
-- ALTER TABLE wallet.channel_rule RENAME TO channel_rules;
-- ALTER TABLE sync.wallet_authorisation SET SCHEMA platform;
-- ALTER TABLE sync.guest_link SET SCHEMA platform;
-- ALTER TABLE sync.cross_region_entitlement SET SCHEMA platform;
-- ALTER TABLE seating.seat_reservation_item RENAME TO seat_hold_item;
-- ALTER TABLE seating.seat_reservation RENAME TO seat_hold;
-- ALTER TABLE seating.recommendation_rule RENAME TO recommendation_rules;
-- ALTER TABLE resources.resource_reservation RENAME TO resource_hold;
-- ALTER TABLE orders.group_customer_organisation_contact RENAME TO group_customer_organization_contact;
-- ALTER TABLE orders.group_customer_organisation RENAME TO group_customer_organization;
-- ALTER TABLE inventory.stock_earmark RENAME TO stock_reservation;
-- ALTER TABLE inventory.inventory_item RENAME TO item;
-- ALTER TABLE catalogue.inventory_reservation RENAME TO inventory_hold;
-- ALTER TABLE catalogue.channel_envelope RENAME TO channel_allocation;
-- DELETE FROM platform.schema_version WHERE version = 'V0103a';
