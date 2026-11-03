-- V0127 -- tenant database, after r1 (9cec72d) (20261103).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- 2 table(s), 9 column(s), 10 index(es), 9 other statement(s), 10 row-level security polic(ies) re-applied.

DO $$ BEGIN IF to_regclass('access.entitlement') IS NOT NULL THEN
ALTER TABLE access.entitlement ADD COLUMN IF NOT EXISTS frozen_from date;
END IF; END $$;

DO $$ BEGIN IF to_regclass('access.entitlement') IS NOT NULL THEN
ALTER TABLE access.entitlement ADD COLUMN IF NOT EXISTS frozen_until date;
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.import_job') IS NOT NULL THEN
ALTER TABLE catalogue.import_job ADD COLUMN IF NOT EXISTS mode text NOT NULL DEFAULT 'createOnly' CONSTRAINT import_job_mode_chk CHECK (mode IN ('createOnly', 'upsert', 'replaceCategory'));
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.import_job') IS NOT NULL THEN
ALTER TABLE catalogue.import_job ADD COLUMN IF NOT EXISTS applied_count integer;
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.import_job') IS NOT NULL THEN
ALTER TABLE catalogue.import_job ADD COLUMN IF NOT EXISTS failed_count integer;
END IF; END $$;

CREATE TABLE IF NOT EXISTS catalogue.import_job_row (
    id                                uuid PRIMARY KEY NOT NULL,
    import_job_id                     uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    row_number                        integer NOT NULL,
    action                            text CONSTRAINT import_job_row_action_chk CHECK (action IN ('create', 'update')),
    target_product_id                 uuid,
    payload                           jsonb NOT NULL,
    is_excluded                       boolean NOT NULL DEFAULT false,
    outcome                           text NOT NULL DEFAULT 'pending' CONSTRAINT import_job_row_outcome_chk CHECK (outcome IN ('pending', 'applied', 'failed', 'excluded')),
    failure                           text,
    product_id                        uuid
);

DO $$ BEGIN IF to_regclass('catalogue.product') IS NOT NULL THEN
ALTER TABLE catalogue.product ADD COLUMN IF NOT EXISTS highlight_badge jsonb;
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.principal') IS NOT NULL THEN
ALTER TABLE identity.principal ADD COLUMN IF NOT EXISTS email text CONSTRAINT principal_email_chk CHECK (char_length(email) <= 320);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.session') IS NOT NULL THEN
ALTER TABLE identity.session ADD COLUMN IF NOT EXISTS grant_id uuid;
END IF; END $$;

CREATE TABLE IF NOT EXISTS marketing.guest_document_upload (
    id                                uuid PRIMARY KEY NOT NULL,
    storage_ref                       text NOT NULL CONSTRAINT guest_document_upload_storage_ref_chk CHECK (char_length(storage_ref) <= 500),
    subject_id                        uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT guest_document_upload_kind_chk CHECK (char_length(kind) <= 40),
    content_type                      text NOT NULL CONSTRAINT guest_document_upload_content_type_chk CHECK (content_type IN ('image/jpeg', 'image/png', 'application/pdf')),
    size_bytes                        integer NOT NULL,
    issued_by_principal_id            uuid,
    issued_at                         timestamptz NOT NULL,
    expires_at                        timestamptz NOT NULL,
    status                            text NOT NULL DEFAULT 'pending' CONSTRAINT guest_document_upload_status_chk CHECK (status IN ('pending', 'attached'))
);

DO $$ BEGIN IF to_regclass('marketing.guest_extra_field') IS NOT NULL THEN
ALTER TABLE marketing.guest_extra_field ADD COLUMN IF NOT EXISTS scope_path ltree;
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.import_job_row') IS NOT NULL AND to_regclass('catalogue.import_job') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'import_job_row' AND column_name = 'import_job_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'import_job_row_import_job_id_fkey' AND conrelid = to_regclass('catalogue.import_job_row')) THEN
ALTER TABLE catalogue.import_job_row ADD CONSTRAINT import_job_row_import_job_id_fkey FOREIGN KEY (import_job_id) REFERENCES catalogue.import_job(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.import_job_row') IS NOT NULL AND to_regclass('catalogue.product') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'import_job_row' AND column_name = 'product_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'import_job_row_product_id_fkey' AND conrelid = to_regclass('catalogue.import_job_row')) THEN
ALTER TABLE catalogue.import_job_row ADD CONSTRAINT import_job_row_product_id_fkey FOREIGN KEY (product_id) REFERENCES catalogue.product(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.import_job_row') IS NOT NULL AND to_regclass('catalogue.product') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'import_job_row' AND column_name = 'target_product_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'import_job_row_target_product_id_fkey' AND conrelid = to_regclass('catalogue.import_job_row')) THEN
ALTER TABLE catalogue.import_job_row ADD CONSTRAINT import_job_row_target_product_id_fkey FOREIGN KEY (target_product_id) REFERENCES catalogue.product(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity."session"') IS NOT NULL AND to_regclass('identity.delegated_access') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'session' AND column_name = 'grant_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'session_grant_id_fkey' AND conrelid = to_regclass('identity."session"')) THEN
ALTER TABLE identity."session" ADD CONSTRAINT session_grant_id_fkey FOREIGN KEY (grant_id) REFERENCES identity.delegated_access(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.guest_document_upload') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'guest_document_upload' AND column_name = 'subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'guest_document_upload_subject_id_fkey' AND conrelid = to_regclass('marketing.guest_document_upload')) THEN
ALTER TABLE marketing.guest_document_upload ADD CONSTRAINT guest_document_upload_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.guest_document_upload') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'guest_document_upload' AND column_name = 'issued_by_principal_id') THEN
CREATE INDEX IF NOT EXISTS guest_document_upload_issued_by_principal_id_idx ON marketing.guest_document_upload (issued_by_principal_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.import_job_row') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'import_job_row' AND column_name = 'import_job_id') THEN
CREATE INDEX IF NOT EXISTS import_job_row_import_job_id_idx ON catalogue.import_job_row (import_job_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.import_job_row') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'import_job_row' AND column_name = 'product_id') THEN
CREATE INDEX IF NOT EXISTS import_job_row_product_id_idx ON catalogue.import_job_row (product_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.import_job_row') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'import_job_row' AND column_name = 'target_product_id') THEN
CREATE INDEX IF NOT EXISTS import_job_row_target_product_id_idx ON catalogue.import_job_row (target_product_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity."session"') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'session' AND column_name = 'grant_id') THEN
CREATE INDEX IF NOT EXISTS session_grant_id_idx ON identity."session" (grant_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.guest_document_upload') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'guest_document_upload' AND column_name = 'subject_id') THEN
CREATE INDEX IF NOT EXISTS guest_document_upload_subject_id_idx ON marketing.guest_document_upload (subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.guest_document_upload') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'guest_document_upload' AND column_name = 'storage_ref') THEN
CREATE UNIQUE INDEX IF NOT EXISTS guest_document_upload_storage_ref_uniq ON marketing.guest_document_upload (lower(storage_ref));
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.import_job_row') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'import_job_row' AND column_name = 'import_job_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'import_job_row' AND column_name = 'row_number') THEN
CREATE UNIQUE INDEX IF NOT EXISTS import_job_row_import_job_id_row_number_uniq ON catalogue.import_job_row (import_job_id, row_number);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.guest_extra_field') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'guest_extra_field' AND column_name = 'scope_path') THEN
CREATE INDEX IF NOT EXISTS guest_extra_field_scope_path_idx ON marketing.guest_extra_field USING gist (scope_path);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.import_job_row') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'import_job_row' AND column_name = 'scope_path') THEN
CREATE INDEX IF NOT EXISTS import_job_row_scope_path_idx ON catalogue.import_job_row USING gist (scope_path);
END IF; END $$;

CREATE OR REPLACE FUNCTION platform.apply_split_insert_rls(target regclass, read_check text, write_check text,
                                                          insert_check text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    base text := (SELECT left(c.relname, 55) FROM pg_class c WHERE c.oid = target);
BEGIN
    PERFORM platform.apply_split_rls(target, read_check, write_check);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', base || '_append', target);
    EXECUTE format('CREATE POLICY %I ON %s FOR INSERT WITH CHECK ((%s) OR (%s))', base || '_append', target,
                   write_check, insert_check);
END
$$;

DO $$ BEGIN IF to_regclass('catalogue.import_job_row') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'import_job_row' AND column_name = 'scope_path') THEN
PERFORM platform.apply_scope_rls('catalogue.import_job_row'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('ledger.deposit') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'ledger' AND table_name = 'deposit' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('ledger.deposit'::regclass);
PERFORM platform.apply_grant_holder_subject_rls('ledger.deposit'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.guest_document') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'guest_document' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('marketing.guest_document'::regclass);
PERFORM platform.apply_grant_holder_subject_rls('marketing.guest_document'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.guest_document_upload') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'guest_document_upload' AND column_name = 'subject_id') THEN
PERFORM platform.apply_grant_holder_subject_rls('marketing.guest_document_upload'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.guest_extra_field') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'guest_extra_field' AND column_name = 'scope_path') THEN
PERFORM platform.drop_rls_policies('marketing.guest_extra_field'::regclass);
PERFORM platform.apply_grant_holder_read_rls('marketing.guest_extra_field'::regclass, 'platform.in_scope(scope_path)');
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.guest_note') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'guest_note' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('marketing.guest_note'::regclass);
PERFORM platform.apply_grant_holder_subject_rls('marketing.guest_note'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.guest_credit_account') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'guest_credit_account' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('orders.guest_credit_account'::regclass);
PERFORM platform.apply_grant_holder_subject_rls('orders.guest_credit_account'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.membership_activation_action') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'membership_activation_action' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('orders.membership_activation_action'::regclass);
PERFORM platform.apply_grant_holder_subject_rls('orders.membership_activation_action'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.order_event') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_event' AND column_name = 'event_type') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_event' AND column_name = 'scope_path') THEN
PERFORM platform.drop_rls_policies('orders.order_event'::regclass);
PERFORM platform.apply_split_insert_rls('orders.order_event'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (EXISTS (SELECT 1 FROM orders.sales_order gp WHERE gp.id = orders.order_event.order_id AND gp.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])', 'event_type = ''ticketsResent'' AND EXISTS (SELECT 1 FROM orders.sales_order gp WHERE gp.id = orders.order_event.order_id AND gp.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.venue_settings') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'venue_settings' AND column_name = 'venue_id') THEN
PERFORM platform.drop_rls_policies('platform.venue_settings'::regclass);
PERFORM platform.apply_split_rls('platform.venue_settings'::regclass, 'platform.venue_in_scope(venue_id) OR (venue_id IS NULL AND cardinality(platform.current_scope_paths()) > 0) OR NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NOT NULL', 'platform.venue_in_scope(venue_id)');
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.plan_benefit') IS NOT NULL AND to_regclass('catalogue.entitlement_template') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'entitlement_template' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'plan_benefit' AND column_name = 'entitlement_template_id') THEN
PERFORM platform.drop_rls_policies('catalogue.plan_benefit'::regclass);
PERFORM platform.apply_parent_rls('catalogue.plan_benefit'::regclass, 'entitlement_template_id', 'catalogue.entitlement_template'::regclass, 'id');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.ticket_transfer') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'ticket_transfer' AND column_name = 'from_subject_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'ticket_transfer' AND column_name = 'to_subject_id') THEN
PERFORM platform.drop_rls_policies('orders.ticket_transfer'::regclass);
PERFORM platform.apply_split_rls('orders.ticket_transfer'::regclass, 'EXISTS (SELECT 1 FROM orders.sales_order pr WHERE pr.id = orders.ticket_transfer.order_id) OR (from_subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)) OR (to_subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', 'EXISTS (SELECT 1 FROM orders.sales_order pr WHERE pr.id = orders.ticket_transfer.order_id AND ((pr.scope_path IS NOT NULL AND pr.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])))) OR (from_subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid) AND EXISTS (SELECT 1 FROM orders.sales_order pr WHERE pr.id = orders.ticket_transfer.order_id AND pr.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))');
END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('approvals.rule') IS NOT NULL THEN GRANT SELECT ON approvals.rule TO operations; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0127', 'after r1 (9cec72d): 2 table(s), 9 column(s), 10 index(es), 9 other statement(s), 10 row-level security polic(ies) re-applied', 'd8072eb5a3d90ad03f740ca534861bb0cc019bdd39dd76f0207b8f0f3964baf4')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- REVOKE SELECT ON approvals.rule FROM operations;
-- SELECT platform.drop_rls_policies('orders.ticket_transfer'::regclass); SELECT platform.apply_parent_rls('orders.ticket_transfer'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id'); SELECT platform.apply_parent_split_rls('orders.ticket_transfer'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id', '(parent_row.scope_path IS NOT NULL AND parent_row.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))'); SELECT platform.apply_split_rls('orders.ticket_transfer'::regclass, 'EXISTS (SELECT 1 FROM orders.sales_order pr WHERE pr.id = orders.ticket_transfer.order_id) OR (from_subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)) OR (to_subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', 'EXISTS (SELECT 1 FROM orders.sales_order pr WHERE pr.id = orders.ticket_transfer.order_id AND ((pr.scope_path IS NOT NULL AND pr.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))))');
-- SELECT platform.drop_rls_policies('catalogue.plan_benefit'::regclass); SELECT platform.apply_tenant_rls('catalogue.plan_benefit'::regclass);
-- SELECT platform.drop_rls_policies('platform.venue_settings'::regclass); SELECT platform.apply_venue_rls('platform.venue_settings'::regclass); SELECT platform.apply_split_rls('platform.venue_settings'::regclass, 'platform.venue_in_scope(venue_id) OR NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NOT NULL', 'platform.venue_in_scope(venue_id)');
-- SELECT platform.drop_rls_policies('orders.order_event'::regclass); SELECT platform.apply_scope_rls('orders.order_event'::regclass); SELECT platform.apply_split_rls('orders.order_event'::regclass, '(scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (EXISTS (SELECT 1 FROM orders.sales_order gp WHERE gp.id = orders.order_event.order_id AND gp.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])'); SELECT platform.apply_split_rls('orders.order_event'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (EXISTS (SELECT 1 FROM orders.sales_order gp WHERE gp.id = orders.order_event.order_id AND gp.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])');
-- SELECT platform.drop_rls_policies('orders.membership_activation_action'::regclass); SELECT platform.apply_subject_rls('orders.membership_activation_action'::regclass); SELECT platform.apply_grant_holder_subject_read_rls('orders.membership_activation_action'::regclass);
-- SELECT platform.drop_rls_policies('orders.guest_credit_account'::regclass); SELECT platform.apply_subject_rls('orders.guest_credit_account'::regclass);
-- SELECT platform.drop_rls_policies('marketing.guest_note'::regclass); SELECT platform.apply_subject_rls('marketing.guest_note'::regclass);
-- SELECT platform.drop_rls_policies('marketing.guest_extra_field'::regclass); SELECT platform.apply_tenant_rls('marketing.guest_extra_field'::regclass);
-- SELECT platform.drop_rls_policies('marketing.guest_document'::regclass); SELECT platform.apply_subject_rls('marketing.guest_document'::regclass); SELECT platform.apply_grant_holder_subject_read_rls('marketing.guest_document'::regclass);
-- SELECT platform.drop_rls_policies('ledger.deposit'::regclass); SELECT platform.apply_subject_rls('ledger.deposit'::regclass); SELECT platform.apply_grant_holder_subject_read_rls('ledger.deposit'::regclass);
-- DROP INDEX IF EXISTS catalogue.import_job_row_scope_path_idx;
-- DROP INDEX IF EXISTS marketing.guest_extra_field_scope_path_idx;
-- DROP INDEX IF EXISTS catalogue.import_job_row_import_job_id_row_number_uniq;
-- DROP INDEX IF EXISTS marketing.guest_document_upload_storage_ref_uniq;
-- DROP INDEX IF EXISTS marketing.guest_document_upload_subject_id_idx;
-- DROP INDEX IF EXISTS identity.session_grant_id_idx;
-- DROP INDEX IF EXISTS catalogue.import_job_row_target_product_id_idx;
-- DROP INDEX IF EXISTS catalogue.import_job_row_product_id_idx;
-- DROP INDEX IF EXISTS catalogue.import_job_row_import_job_id_idx;
-- DROP INDEX IF EXISTS marketing.guest_document_upload_issued_by_principal_id_idx;
-- ALTER TABLE identity.session DROP CONSTRAINT IF EXISTS session_grant_id_fkey;
-- ALTER TABLE marketing.guest_extra_field DROP COLUMN IF EXISTS scope_path;
-- DROP TABLE IF EXISTS marketing.guest_document_upload;
-- ALTER TABLE identity.session DROP COLUMN IF EXISTS grant_id;
-- ALTER TABLE identity.principal DROP COLUMN IF EXISTS email;
-- ALTER TABLE catalogue.product DROP COLUMN IF EXISTS highlight_badge;
-- DROP TABLE IF EXISTS catalogue.import_job_row;
-- ALTER TABLE catalogue.import_job DROP COLUMN IF EXISTS failed_count;
-- ALTER TABLE catalogue.import_job DROP COLUMN IF EXISTS applied_count;
-- ALTER TABLE catalogue.import_job DROP COLUMN IF EXISTS mode;
-- ALTER TABLE access.entitlement DROP COLUMN IF EXISTS frozen_until;
-- ALTER TABLE access.entitlement DROP COLUMN IF EXISTS frozen_from;
-- DELETE FROM platform.schema_version WHERE version = 'V0127';
