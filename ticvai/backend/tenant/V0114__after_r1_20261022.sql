-- V0114 -- tenant database, after r1 (9cec72d) (20261022).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- 0 table(s), 0 column(s), 1 index(es), 3 other statement(s), 25 row-level security polic(ies) re-applied.

DO $$ BEGIN IF to_regclass('platform.idempotency_record') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'idempotency_record' AND column_name = 'status') THEN
ALTER TABLE platform.idempotency_record DROP CONSTRAINT IF EXISTS idempotency_record_status_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.idempotency_record') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'idempotency_record' AND column_name = 'status') THEN
ALTER TABLE platform.idempotency_record ADD CONSTRAINT idempotency_record_status_chk CHECK (status IN ('completed')) NOT VALID;
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.idempotency_record') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'idempotency_record' AND column_name = 'idempotency_key') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'idempotency_record' AND column_name = 'operation_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS idempotency_record_operation_id_idempotency_key_uniq ON platform.idempotency_record (operation_id, idempotency_key);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.cart') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'cart' AND column_name = 'subject_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'cart' AND column_name = 'venue_id') THEN
PERFORM platform.drop_rls_policies('orders.cart'::regclass);
PERFORM platform.apply_split_rls('orders.cart'::regclass, '(platform.venue_in_scope(venue_id)) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', '(platform.venue_in_scope(venue_id)) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.order_event') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_event' AND column_name = 'scope_path') THEN
PERFORM platform.drop_rls_policies('orders.order_event'::regclass);
PERFORM platform.apply_split_rls('orders.order_event'::regclass, '(scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (EXISTS (SELECT 1 FROM orders.sales_order gp WHERE gp.id = orders.order_event.order_id AND gp.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.order_line') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_line' AND column_name = 'venue_id') THEN
PERFORM platform.drop_rls_policies('orders.order_line'::regclass);
PERFORM platform.apply_split_rls('orders.order_line'::regclass, '(platform.venue_in_scope(venue_id)) OR (EXISTS (SELECT 1 FROM orders.sales_order gp WHERE gp.id = orders.order_line.sales_order_id AND gp.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))', 'platform.venue_in_scope(venue_id)');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'sales_order' AND column_name = 'scope_path') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'sales_order' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('orders.sales_order'::regclass);
PERFORM platform.apply_split_rls('orders.sales_order'::regclass, '(scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.cart_line') IS NOT NULL AND to_regclass('orders.cart') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'cart' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'cart_line' AND column_name = 'cart_id') THEN
PERFORM platform.drop_rls_policies('orders.cart_line'::regclass);
PERFORM platform.apply_parent_split_rls('orders.cart_line'::regclass, 'cart_id', 'orders.cart'::regclass, 'id', '((platform.venue_in_scope(parent_row.venue_id)) OR (parent_row.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.deposit') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'deposit' AND column_name = 'order_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'sales_order' AND column_name = 'id') THEN
PERFORM platform.drop_rls_policies('orders.deposit'::regclass);
PERFORM platform.apply_parent_split_rls('orders.deposit'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id', '(parent_row.scope_path IS NOT NULL AND parent_row.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.discount') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'discount' AND column_name = 'order_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'sales_order' AND column_name = 'id') THEN
PERFORM platform.drop_rls_policies('orders.discount'::regclass);
PERFORM platform.apply_parent_split_rls('orders.discount'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id', '(parent_row.scope_path IS NOT NULL AND parent_row.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.group_booking') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_booking' AND column_name = 'order_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'sales_order' AND column_name = 'id') THEN
PERFORM platform.drop_rls_policies('orders.group_booking'::regclass);
PERFORM platform.apply_parent_split_rls('orders.group_booking'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id', '(parent_row.scope_path IS NOT NULL AND parent_row.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.order_fee') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_fee' AND column_name = 'order_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'sales_order' AND column_name = 'id') THEN
PERFORM platform.drop_rls_policies('orders.order_fee'::regclass);
PERFORM platform.apply_parent_split_rls('orders.order_fee'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id', '(parent_row.scope_path IS NOT NULL AND parent_row.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.order_line_discount') IS NOT NULL AND to_regclass('orders.order_line') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_line' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_line_discount' AND column_name = 'order_line_id') THEN
PERFORM platform.drop_rls_policies('orders.order_line_discount'::regclass);
PERFORM platform.apply_parent_split_rls('orders.order_line_discount'::regclass, 'order_line_id', 'orders.order_line'::regclass, 'id', '(platform.venue_in_scope(parent_row.venue_id))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.order_line_eligibility') IS NOT NULL AND to_regclass('orders.order_line') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_line' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_line_eligibility' AND column_name = 'order_line_id') THEN
PERFORM platform.drop_rls_policies('orders.order_line_eligibility'::regclass);
PERFORM platform.apply_parent_split_rls('orders.order_line_eligibility'::regclass, 'order_line_id', 'orders.order_line'::regclass, 'id', '(platform.venue_in_scope(parent_row.venue_id))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.payment') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'payment' AND column_name = 'order_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'sales_order' AND column_name = 'id') THEN
PERFORM platform.drop_rls_policies('orders.payment'::regclass);
PERFORM platform.apply_parent_split_rls('orders.payment'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id', '(parent_row.scope_path IS NOT NULL AND parent_row.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.refund') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'refund' AND column_name = 'order_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'sales_order' AND column_name = 'id') THEN
PERFORM platform.drop_rls_policies('orders.refund'::regclass);
PERFORM platform.apply_parent_split_rls('orders.refund'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id', '(parent_row.scope_path IS NOT NULL AND parent_row.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.ticket_transfer') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'sales_order' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'ticket_transfer' AND column_name = 'order_id') THEN
PERFORM platform.drop_rls_policies('orders.ticket_transfer'::regclass);
PERFORM platform.apply_parent_split_rls('orders.ticket_transfer'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id', '(parent_row.scope_path IS NOT NULL AND parent_row.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.upgrade') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'sales_order' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'upgrade' AND column_name = 'order_id') THEN
PERFORM platform.drop_rls_policies('orders.upgrade'::regclass);
PERFORM platform.apply_parent_split_rls('orders.upgrade'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id', '(parent_row.scope_path IS NOT NULL AND parent_row.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.chargeback') IS NOT NULL AND to_regclass('orders.payment') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'chargeback' AND column_name = 'payment_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'payment' AND column_name = 'id') THEN
PERFORM platform.drop_rls_policies('orders.chargeback'::regclass);
PERFORM platform.apply_parent_split_rls('orders.chargeback'::regclass, 'payment_id', 'orders.payment'::regclass, 'id', 'EXISTS (SELECT 1 FROM orders.sales_order p1 WHERE p1.id = parent_row.order_id AND ((p1.scope_path IS NOT NULL AND p1.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.group_participant_list') IS NOT NULL AND to_regclass('orders.group_booking') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_booking' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_participant_list' AND column_name = 'group_booking_id') THEN
PERFORM platform.drop_rls_policies('orders.group_participant_list'::regclass);
PERFORM platform.apply_parent_split_rls('orders.group_participant_list'::regclass, 'group_booking_id', 'orders.group_booking'::regclass, 'id', 'EXISTS (SELECT 1 FROM orders.sales_order p1 WHERE p1.id = parent_row.order_id AND ((p1.scope_path IS NOT NULL AND p1.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.group_payment_schedule') IS NOT NULL AND to_regclass('orders.group_booking') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_booking' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_payment_schedule' AND column_name = 'group_booking_id') THEN
PERFORM platform.drop_rls_policies('orders.group_payment_schedule'::regclass);
PERFORM platform.apply_parent_split_rls('orders.group_payment_schedule'::regclass, 'group_booking_id', 'orders.group_booking'::regclass, 'id', 'EXISTS (SELECT 1 FROM orders.sales_order p1 WHERE p1.id = parent_row.order_id AND ((p1.scope_path IS NOT NULL AND p1.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.group_ticket_allocation') IS NOT NULL AND to_regclass('orders.group_booking') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_booking' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_ticket_allocation' AND column_name = 'group_booking_id') THEN
PERFORM platform.drop_rls_policies('orders.group_ticket_allocation'::regclass);
PERFORM platform.apply_parent_split_rls('orders.group_ticket_allocation'::regclass, 'group_booking_id', 'orders.group_booking'::regclass, 'id', 'EXISTS (SELECT 1 FROM orders.sales_order p1 WHERE p1.id = parent_row.order_id AND ((p1.scope_path IS NOT NULL AND p1.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.group_ticket_fulfillment') IS NOT NULL AND to_regclass('orders.group_booking') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_booking' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_ticket_fulfillment' AND column_name = 'group_booking_id') THEN
PERFORM platform.drop_rls_policies('orders.group_ticket_fulfillment'::regclass);
PERFORM platform.apply_parent_split_rls('orders.group_ticket_fulfillment'::regclass, 'group_booking_id', 'orders.group_booking'::regclass, 'id', 'EXISTS (SELECT 1 FROM orders.sales_order p1 WHERE p1.id = parent_row.order_id AND ((p1.scope_path IS NOT NULL AND p1.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.chargeback_evidence') IS NOT NULL AND to_regclass('orders.chargeback') IS NOT NULL AND to_regclass('orders.payment') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'chargeback' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'chargeback_evidence' AND column_name = 'chargeback_id') THEN
PERFORM platform.drop_rls_policies('orders.chargeback_evidence'::regclass);
PERFORM platform.apply_parent_split_rls('orders.chargeback_evidence'::regclass, 'chargeback_id', 'orders.chargeback'::regclass, 'id', 'EXISTS (SELECT 1 FROM orders.payment p2 WHERE p2.id = parent_row.payment_id AND (EXISTS (SELECT 1 FROM orders.sales_order p1 WHERE p1.id = p2.order_id AND ((p1.scope_path IS NOT NULL AND p1.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))))))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.chargeback_investigation_log') IS NOT NULL AND to_regclass('orders.chargeback') IS NOT NULL AND to_regclass('orders.payment') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'chargeback' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'chargeback_investigation_log' AND column_name = 'chargeback_id') THEN
PERFORM platform.drop_rls_policies('orders.chargeback_investigation_log'::regclass);
PERFORM platform.apply_parent_split_rls('orders.chargeback_investigation_log'::regclass, 'chargeback_id', 'orders.chargeback'::regclass, 'id', 'EXISTS (SELECT 1 FROM orders.payment p2 WHERE p2.id = parent_row.payment_id AND (EXISTS (SELECT 1 FROM orders.sales_order p1 WHERE p1.id = p2.order_id AND ((p1.scope_path IS NOT NULL AND p1.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))))))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.group_participant') IS NOT NULL AND to_regclass('orders.group_participant_list') IS NOT NULL AND to_regclass('orders.group_booking') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_participant' AND column_name = 'group_participant_list_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_participant_list' AND column_name = 'id') THEN
PERFORM platform.drop_rls_policies('orders.group_participant'::regclass);
PERFORM platform.apply_parent_split_rls('orders.group_participant'::regclass, 'group_participant_list_id', 'orders.group_participant_list'::regclass, 'id', 'EXISTS (SELECT 1 FROM orders.group_booking p2 WHERE p2.id = parent_row.group_booking_id AND (EXISTS (SELECT 1 FROM orders.sales_order p1 WHERE p1.id = p2.order_id AND ((p1.scope_path IS NOT NULL AND p1.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))))))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.group_payment_milestone') IS NOT NULL AND to_regclass('orders.group_payment_schedule') IS NOT NULL AND to_regclass('orders.group_booking') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_payment_milestone' AND column_name = 'group_payment_schedule_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_payment_schedule' AND column_name = 'id') THEN
PERFORM platform.drop_rls_policies('orders.group_payment_milestone'::regclass);
PERFORM platform.apply_parent_split_rls('orders.group_payment_milestone'::regclass, 'group_payment_schedule_id', 'orders.group_payment_schedule'::regclass, 'id', 'EXISTS (SELECT 1 FROM orders.group_booking p2 WHERE p2.id = parent_row.group_booking_id AND (EXISTS (SELECT 1 FROM orders.sales_order p1 WHERE p1.id = p2.order_id AND ((p1.scope_path IS NOT NULL AND p1.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))))))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.group_ticket_allocation_line') IS NOT NULL AND to_regclass('orders.group_ticket_allocation') IS NOT NULL AND to_regclass('orders.group_booking') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_ticket_allocation' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_ticket_allocation_line' AND column_name = 'group_ticket_allocation_id') THEN
PERFORM platform.drop_rls_policies('orders.group_ticket_allocation_line'::regclass);
PERFORM platform.apply_parent_split_rls('orders.group_ticket_allocation_line'::regclass, 'group_ticket_allocation_id', 'orders.group_ticket_allocation'::regclass, 'id', 'EXISTS (SELECT 1 FROM orders.group_booking p2 WHERE p2.id = parent_row.group_booking_id AND (EXISTS (SELECT 1 FROM orders.sales_order p1 WHERE p1.id = p2.order_id AND ((p1.scope_path IS NOT NULL AND p1.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))))))');
END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'commerce') AND to_regclass('access.entitlement') IS NOT NULL THEN GRANT SELECT ON access.entitlement TO commerce; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'commerce') AND to_regclass('access.scan_event') IS NOT NULL THEN GRANT SELECT ON access.scan_event TO commerce; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0114', 'after r1 (9cec72d): 0 table(s), 0 column(s), 1 index(es), 3 other statement(s), 25 row-level security polic(ies) re-applied', '73fdeee7833fb19cb2c73ddf9980aae705e34784280aa6caef9588d3129a27b0')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- REVOKE SELECT ON access.scan_event FROM commerce;
-- REVOKE SELECT ON access.entitlement FROM commerce;
-- SELECT platform.drop_rls_policies('orders.group_ticket_allocation_line'::regclass); SELECT platform.apply_tenant_rls('orders.group_ticket_allocation_line'::regclass); SELECT platform.apply_parent_rls('orders.group_ticket_allocation_line'::regclass, 'group_ticket_allocation_id', 'orders.group_ticket_allocation'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.group_payment_milestone'::regclass); SELECT platform.apply_tenant_rls('orders.group_payment_milestone'::regclass); SELECT platform.apply_parent_rls('orders.group_payment_milestone'::regclass, 'group_payment_schedule_id', 'orders.group_payment_schedule'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.group_participant'::regclass); SELECT platform.apply_tenant_rls('orders.group_participant'::regclass); SELECT platform.apply_parent_rls('orders.group_participant'::regclass, 'group_participant_list_id', 'orders.group_participant_list'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.chargeback_investigation_log'::regclass); SELECT platform.apply_parent_rls('orders.chargeback_investigation_log'::regclass, 'chargeback_id', 'orders.chargeback'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.chargeback_evidence'::regclass); SELECT platform.apply_parent_rls('orders.chargeback_evidence'::regclass, 'chargeback_id', 'orders.chargeback'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.group_ticket_fulfillment'::regclass); SELECT platform.apply_tenant_rls('orders.group_ticket_fulfillment'::regclass); SELECT platform.apply_parent_rls('orders.group_ticket_fulfillment'::regclass, 'group_booking_id', 'orders.group_booking'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.group_ticket_allocation'::regclass); SELECT platform.apply_tenant_rls('orders.group_ticket_allocation'::regclass); SELECT platform.apply_parent_rls('orders.group_ticket_allocation'::regclass, 'group_booking_id', 'orders.group_booking'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.group_payment_schedule'::regclass); SELECT platform.apply_tenant_rls('orders.group_payment_schedule'::regclass); SELECT platform.apply_parent_rls('orders.group_payment_schedule'::regclass, 'group_booking_id', 'orders.group_booking'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.group_participant_list'::regclass); SELECT platform.apply_tenant_rls('orders.group_participant_list'::regclass); SELECT platform.apply_parent_rls('orders.group_participant_list'::regclass, 'group_booking_id', 'orders.group_booking'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.chargeback'::regclass); SELECT platform.apply_parent_rls('orders.chargeback'::regclass, 'payment_id', 'orders.payment'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.upgrade'::regclass); SELECT platform.apply_parent_rls('orders.upgrade'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.ticket_transfer'::regclass); SELECT platform.apply_parent_rls('orders.ticket_transfer'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.refund'::regclass); SELECT platform.apply_parent_rls('orders.refund'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.payment'::regclass); SELECT platform.apply_parent_rls('orders.payment'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.order_line_eligibility'::regclass); SELECT platform.apply_parent_rls('orders.order_line_eligibility'::regclass, 'order_line_id', 'orders.order_line'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.order_line_discount'::regclass); SELECT platform.apply_parent_rls('orders.order_line_discount'::regclass, 'order_line_id', 'orders.order_line'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.order_fee'::regclass); SELECT platform.apply_parent_rls('orders.order_fee'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.group_booking'::regclass); SELECT platform.apply_parent_rls('orders.group_booking'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.discount'::regclass); SELECT platform.apply_parent_rls('orders.discount'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.deposit'::regclass); SELECT platform.apply_parent_rls('orders.deposit'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.cart_line'::regclass); SELECT platform.apply_parent_rls('orders.cart_line'::regclass, 'cart_id', 'orders.cart'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.sales_order'::regclass); SELECT platform.apply_scope_rls('orders.sales_order'::regclass);
-- SELECT platform.drop_rls_policies('orders.order_line'::regclass); SELECT platform.apply_venue_rls('orders.order_line'::regclass);
-- SELECT platform.drop_rls_policies('orders.order_event'::regclass); SELECT platform.apply_scope_rls('orders.order_event'::regclass);
-- SELECT platform.drop_rls_policies('orders.cart'::regclass); SELECT platform.apply_venue_rls('orders.cart'::regclass);
-- DROP INDEX IF EXISTS platform.idempotency_record_operation_id_idempotency_key_uniq;
-- ALTER TABLE platform.idempotency_record DROP CONSTRAINT IF EXISTS idempotency_record_status_chk; ALTER TABLE platform.idempotency_record ADD CONSTRAINT idempotency_record_status_chk CHECK (status IN ('inProgress', 'completed')) NOT VALID;
-- DELETE FROM platform.schema_version WHERE version = 'V0114';
