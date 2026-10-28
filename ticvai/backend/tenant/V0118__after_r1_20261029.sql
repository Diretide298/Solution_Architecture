-- V0118 -- tenant database, after r1 (9cec72d) (20261029).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- 0 table(s), 0 column(s), 4 index(es), 0 other statement(s), 6 row-level security polic(ies) re-applied.

DO $$ BEGIN IF to_regclass('ai.proposed_action') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'ai' AND table_name = 'proposed_action' AND column_name = 'map_id') THEN
CREATE INDEX IF NOT EXISTS proposed_action_map_id_idx ON ai.proposed_action (map_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.privacy_request') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'privacy_request' AND column_name = 'approval_request_id') THEN
CREATE INDEX IF NOT EXISTS privacy_request_approval_request_id_idx ON marketing.privacy_request (approval_request_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.guest_preference') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'guest_preference' AND column_name = 'subject_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS guest_preference_subject_id_uniq ON marketing.guest_preference (subject_id) WHERE subject_id IS NOT NULL;
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.guest_profile') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'guest_profile' AND column_name = 'subject_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS guest_profile_subject_id_uniq ON marketing.guest_profile (subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.cart') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'cart' AND column_name = 'subject_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'cart' AND column_name = 'venue_id') THEN
PERFORM platform.drop_rls_policies('orders.cart'::regclass);
PERFORM platform.apply_split_rls('orders.cart'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.venue_in_scope(venue_id)) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.venue_in_scope(venue_id)) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.order_event') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_event' AND column_name = 'scope_path') THEN
PERFORM platform.drop_rls_policies('orders.order_event'::regclass);
PERFORM platform.apply_split_rls('orders.order_event'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (EXISTS (SELECT 1 FROM orders.sales_order gp WHERE gp.id = orders.order_event.order_id AND gp.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.order_line') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_line' AND column_name = 'venue_id') THEN
PERFORM platform.drop_rls_policies('orders.order_line'::regclass);
PERFORM platform.apply_split_rls('orders.order_line'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.venue_in_scope(venue_id)) OR (EXISTS (SELECT 1 FROM orders.sales_order gp WHERE gp.id = orders.order_line.sales_order_id AND gp.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))', 'platform.venue_in_scope(venue_id)');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'sales_order' AND column_name = 'scope_path') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'sales_order' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('orders.sales_order'::regclass);
PERFORM platform.apply_split_rls('orders.sales_order'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])');
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.guest_profile') IS NOT NULL AND to_regclass('marketing.segment') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'guest_profile' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('marketing.guest_profile'::regclass);
PERFORM platform.apply_split_rls('marketing.guest_profile'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND EXISTS (SELECT 1 FROM marketing.segment pr WHERE pr.id = marketing.guest_profile.segment_id)) OR platform.subject_in_scope(subject_id)', '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND EXISTS (SELECT 1 FROM marketing.segment pr WHERE pr.id = marketing.guest_profile.segment_id)) OR platform.subject_in_scope(subject_id)');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.cart_line') IS NOT NULL AND to_regclass('orders.cart') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'cart' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'cart_line' AND column_name = 'cart_id') THEN
PERFORM platform.drop_rls_policies('orders.cart_line'::regclass);
PERFORM platform.apply_parent_split_rls('orders.cart_line'::regclass, 'cart_id', 'orders.cart'::regclass, 'id', '((NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.venue_in_scope(parent_row.venue_id)) OR (parent_row.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))');
END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0118', 'after r1 (9cec72d): 0 table(s), 0 column(s), 4 index(es), 0 other statement(s), 6 row-level security polic(ies) re-applied', 'a898baaba32520ddbecb11a5da023929c706f17d34ca5d7c11bf25932e0f289d')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- SELECT platform.drop_rls_policies('orders.cart_line'::regclass); SELECT platform.apply_parent_rls('orders.cart_line'::regclass, 'cart_id', 'orders.cart'::regclass, 'id'); SELECT platform.apply_parent_split_rls('orders.cart_line'::regclass, 'cart_id', 'orders.cart'::regclass, 'id', '((platform.venue_in_scope(parent_row.venue_id)) OR (parent_row.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))');
-- SELECT platform.drop_rls_policies('marketing.guest_profile'::regclass); SELECT platform.apply_parent_rls('marketing.guest_profile'::regclass, 'segment_id', 'marketing.segment'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.sales_order'::regclass); SELECT platform.apply_scope_rls('orders.sales_order'::regclass); SELECT platform.apply_split_rls('orders.sales_order'::regclass, '(scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])');
-- SELECT platform.drop_rls_policies('orders.order_line'::regclass); SELECT platform.apply_venue_rls('orders.order_line'::regclass); SELECT platform.apply_split_rls('orders.order_line'::regclass, '(platform.venue_in_scope(venue_id)) OR (EXISTS (SELECT 1 FROM orders.sales_order gp WHERE gp.id = orders.order_line.sales_order_id AND gp.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))', 'platform.venue_in_scope(venue_id)');
-- SELECT platform.drop_rls_policies('orders.order_event'::regclass); SELECT platform.apply_scope_rls('orders.order_event'::regclass); SELECT platform.apply_split_rls('orders.order_event'::regclass, '(scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (EXISTS (SELECT 1 FROM orders.sales_order gp WHERE gp.id = orders.order_event.order_id AND gp.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])');
-- SELECT platform.drop_rls_policies('orders.cart'::regclass); SELECT platform.apply_venue_rls('orders.cart'::regclass); SELECT platform.apply_split_rls('orders.cart'::regclass, '(platform.venue_in_scope(venue_id)) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', '(platform.venue_in_scope(venue_id)) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))');
-- DROP INDEX IF EXISTS marketing.guest_profile_subject_id_uniq;
-- DROP INDEX IF EXISTS marketing.guest_preference_subject_id_uniq;
-- DROP INDEX IF EXISTS marketing.privacy_request_approval_request_id_idx;
-- DROP INDEX IF EXISTS ai.proposed_action_map_id_idx;
-- DELETE FROM platform.schema_version WHERE version = 'V0118';
