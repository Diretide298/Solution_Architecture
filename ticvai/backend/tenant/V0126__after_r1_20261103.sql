-- V0126 -- tenant database, after r1 (9cec72d) (20261103).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- 0 table(s), 5 column(s), 6 index(es), 1 other statement(s), 3 row-level security polic(ies) re-applied.

DO $$ BEGIN IF to_regclass('queue.entry') IS NOT NULL THEN
ALTER TABLE queue.entry ADD COLUMN IF NOT EXISTS call_resolved_by_principal_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('queue.entry') IS NOT NULL THEN
ALTER TABLE queue.entry ADD COLUMN IF NOT EXISTS call_resolution_reason text CONSTRAINT entry_call_resolution_reason_chk CHECK (char_length(call_resolution_reason) <= 500);
END IF; END $$;

DO $$ BEGIN IF to_regclass('queue.entry') IS NOT NULL THEN
ALTER TABLE queue.entry ADD COLUMN IF NOT EXISTS call_resolved_at timestamptz;
END IF; END $$;

DO $$ BEGIN IF to_regclass('wallet.transfer_rule') IS NOT NULL THEN
ALTER TABLE wallet.transfer_rule ADD COLUMN IF NOT EXISTS version integer NOT NULL DEFAULT 1;
END IF; END $$;

DO $$ BEGIN IF to_regclass('whitelabel.site_package') IS NOT NULL THEN
ALTER TABLE whitelabel.site_package ADD COLUMN IF NOT EXISTS failure_reason text CONSTRAINT site_package_failure_reason_chk CHECK (char_length(failure_reason) <= 500);
END IF; END $$;

DO $$ BEGIN IF to_regclass('queue.entry') IS NOT NULL AND to_regclass('identity.principal') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'queue' AND table_name = 'entry' AND column_name = 'call_resolved_by_principal_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'entry_call_resolved_by_principal_id_fkey' AND conrelid = to_regclass('queue.entry')) THEN
ALTER TABLE queue.entry ADD CONSTRAINT entry_call_resolved_by_principal_id_fkey FOREIGN KEY (call_resolved_by_principal_id) REFERENCES identity.principal(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('queue.entry') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'queue' AND table_name = 'entry' AND column_name = 'call_resolved_by_principal_id') THEN
CREATE INDEX IF NOT EXISTS entry_call_resolved_by_principal_id_idx ON queue.entry (call_resolved_by_principal_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.channel_connection') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'channel_connection' AND column_name = 'connector_name') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'channel_connection' AND column_name = 'environment') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'channel_connection' AND column_name = 'sales_channel_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS channel_connection_sales_channel_id_connector_nam_802356ac_uniq ON catalogue.channel_connection (sales_channel_id, lower(connector_name), lower(environment));
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.channel_sync') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'channel_sync' AND column_name = 'domain') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'channel_sync' AND column_name = 'sales_channel_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS channel_sync_sales_channel_id_domain_uniq ON catalogue.channel_sync (sales_channel_id, lower(domain));
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.dynamic_pricing_strategy') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'dynamic_pricing_strategy' AND column_name = 'code') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'dynamic_pricing_strategy' AND column_name = 'scope_path') THEN
CREATE UNIQUE INDEX IF NOT EXISTS dynamic_pricing_strategy_scope_path_code_uniq ON catalogue.dynamic_pricing_strategy (scope_path, lower(code));
END IF; END $$;

DO $$ BEGIN IF to_regclass('fnb.course_rule') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'fnb' AND table_name = 'course_rule' AND column_name = 'outlet_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS course_rule_outlet_id_uniq ON fnb.course_rule (outlet_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('fnb.kitchen_routing_rule') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'fnb' AND table_name = 'kitchen_routing_rule' AND column_name = 'outlet_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS kitchen_routing_rule_outlet_id_uniq ON fnb.kitchen_routing_rule (outlet_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('retail.shop_and_drop') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'retail' AND table_name = 'shop_and_drop' AND column_name = 'subject_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'retail' AND table_name = 'shop_and_drop' AND column_name = 'venue_id') THEN
PERFORM platform.drop_rls_policies('retail.shop_and_drop'::regclass);
PERFORM platform.apply_split_rls('retail.shop_and_drop'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.venue_in_scope(venue_id)) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', 'platform.venue_in_scope(venue_id)');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.ticket_transfer') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'ticket_transfer' AND column_name = 'from_subject_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'ticket_transfer' AND column_name = 'to_subject_id') THEN
PERFORM platform.drop_rls_policies('orders.ticket_transfer'::regclass);
PERFORM platform.apply_split_rls('orders.ticket_transfer'::regclass, 'EXISTS (SELECT 1 FROM orders.sales_order pr WHERE pr.id = orders.ticket_transfer.order_id) OR (from_subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)) OR (to_subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', 'EXISTS (SELECT 1 FROM orders.sales_order pr WHERE pr.id = orders.ticket_transfer.order_id AND ((pr.scope_path IS NOT NULL AND pr.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('retail.shop_and_drop_line') IS NOT NULL AND to_regclass('retail.shop_and_drop') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'retail' AND table_name = 'shop_and_drop' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'retail' AND table_name = 'shop_and_drop_line' AND column_name = 'shop_and_drop_id') THEN
PERFORM platform.drop_rls_policies('retail.shop_and_drop_line'::regclass);
PERFORM platform.apply_parent_split_rls('retail.shop_and_drop_line'::regclass, 'shop_and_drop_id', 'retail.shop_and_drop'::regclass, 'id', '(platform.venue_in_scope(parent_row.venue_id))');
END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0126', 'after r1 (9cec72d): 0 table(s), 5 column(s), 6 index(es), 1 other statement(s), 3 row-level security polic(ies) re-applied', '39e7bdcc285975f847b4778d191db519b0ee74cc3c4033c93228d00e85d0d36b')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- SELECT platform.drop_rls_policies('retail.shop_and_drop_line'::regclass); SELECT platform.apply_parent_rls('retail.shop_and_drop_line'::regclass, 'shop_and_drop_id', 'retail.shop_and_drop'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.ticket_transfer'::regclass); SELECT platform.apply_parent_rls('orders.ticket_transfer'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id'); SELECT platform.apply_parent_split_rls('orders.ticket_transfer'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id', '(parent_row.scope_path IS NOT NULL AND parent_row.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))');
-- SELECT platform.drop_rls_policies('retail.shop_and_drop'::regclass); SELECT platform.apply_venue_rls('retail.shop_and_drop'::regclass);
-- DROP INDEX IF EXISTS fnb.kitchen_routing_rule_outlet_id_uniq;
-- DROP INDEX IF EXISTS fnb.course_rule_outlet_id_uniq;
-- DROP INDEX IF EXISTS catalogue.dynamic_pricing_strategy_scope_path_code_uniq;
-- DROP INDEX IF EXISTS catalogue.channel_sync_sales_channel_id_domain_uniq;
-- DROP INDEX IF EXISTS catalogue.channel_connection_sales_channel_id_connector_nam_802356ac_uniq;
-- DROP INDEX IF EXISTS queue.entry_call_resolved_by_principal_id_idx;
-- ALTER TABLE queue.entry DROP CONSTRAINT IF EXISTS entry_call_resolved_by_principal_id_fkey;
-- ALTER TABLE whitelabel.site_package DROP COLUMN IF EXISTS failure_reason;
-- ALTER TABLE wallet.transfer_rule DROP COLUMN IF EXISTS version;
-- ALTER TABLE queue.entry DROP COLUMN IF EXISTS call_resolved_at;
-- ALTER TABLE queue.entry DROP COLUMN IF EXISTS call_resolution_reason;
-- ALTER TABLE queue.entry DROP COLUMN IF EXISTS call_resolved_by_principal_id;
-- DELETE FROM platform.schema_version WHERE version = 'V0126';
