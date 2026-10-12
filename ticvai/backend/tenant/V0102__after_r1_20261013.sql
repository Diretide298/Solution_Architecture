-- V0102 -- tenant database, after r1 (9cec72d) (20261013).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 0 table(s), 11 column(s), 13 index(es), 2 other statement(s).

ALTER TABLE access.entitlement ADD COLUMN IF NOT EXISTS credential_format text;

ALTER TABLE access.verification_method_policy ADD COLUMN IF NOT EXISTS credential_format_override text;

ALTER TABLE catalogue.product_media ADD COLUMN IF NOT EXISTS product_id uuid;

ALTER TABLE catalogue.sales_channel ADD COLUMN IF NOT EXISTS ticket_credential_format text CONSTRAINT sales_channel_ticket_credential_format_chk CHECK (ticket_credential_format IN ('platformSignedQr', 'staticQr', 'rfidCard'));

ALTER TABLE orders.pos_shift ADD COLUMN IF NOT EXISTS business_date date;

ALTER TABLE orders.sales_order ADD COLUMN IF NOT EXISTS channel_profile_id uuid;

ALTER TABLE platform.venue_settings ADD COLUMN IF NOT EXISTS business_day_cutoff text DEFAULT '00:00';

ALTER TABLE whitelabel.store_account ADD COLUMN IF NOT EXISTS pass_type_identifier text;

ALTER TABLE whitelabel.store_account ADD COLUMN IF NOT EXISTS pass_certificate_secret_ref text;

ALTER TABLE whitelabel.store_account ADD COLUMN IF NOT EXISTS has_pass_certificate boolean;

ALTER TABLE whitelabel.store_account ADD COLUMN IF NOT EXISTS pass_certificate_expires_at timestamptz;

ALTER TABLE catalogue.product_media ADD CONSTRAINT product_media_product_id_fkey FOREIGN KEY (product_id) REFERENCES catalogue.product(id);

CREATE UNIQUE INDEX IF NOT EXISTS scope_path_uniq ON platform.scope (path);

CREATE INDEX IF NOT EXISTS product_media_product_id_idx ON catalogue.product_media (product_id);

CREATE INDEX IF NOT EXISTS scope_parent_id_idx ON platform.scope (parent_id);

CREATE UNIQUE INDEX IF NOT EXISTS scope_tenant_root_uniq ON platform.scope ((true)) WHERE level = 'tenant';

CREATE UNIQUE INDEX IF NOT EXISTS account_code_uniq ON ledger.account (code);

CREATE UNIQUE INDEX IF NOT EXISTS credit_memo_credit_memo_number_uniq ON ledger.credit_memo (credit_memo_number);

CREATE UNIQUE INDEX IF NOT EXISTS journal_entry_entry_number_uniq ON ledger.journal_entry (entry_number);

CREATE UNIQUE INDEX IF NOT EXISTS tax_code_code_uniq ON ledger.tax_code (code);

CREATE UNIQUE INDEX IF NOT EXISTS tax_invoice_invoice_number_uniq ON ledger.tax_invoice (invoice_number);

CREATE UNIQUE INDEX IF NOT EXISTS sales_order_order_number_uniq ON orders.sales_order (order_number) WHERE order_number IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS seat_category_venue_id_code_uniq ON seating.seat_category (venue_id, code);

CREATE UNIQUE INDEX IF NOT EXISTS seat_seat_map_id_section_code_row_label_seat_number_uniq ON seating.seat (seat_map_id, section_code, row_label, seat_number);

CREATE UNIQUE INDEX IF NOT EXISTS seat_price_band_seat_category_id_code_uniq ON seating.seat_price_band (seat_category_id, code);

CREATE OR REPLACE FUNCTION platform.apply_append_audit_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    base text := (SELECT left(c.relname, 55) FROM pg_class c WHERE c.oid = target);
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    -- the single FOR ALL policy apply_tenant_rls created, if the table had it
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', platform.rls_policy_name(target), target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', base || '_append', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', base || '_read', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', base || '_update', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', base || '_delete', target);
    EXECUTE format('CREATE POLICY %I ON %s FOR INSERT '
                   'WITH CHECK (cardinality(platform.current_scope_paths()) > 0)', base || '_append', target);
    EXECUTE format('CREATE POLICY %I ON %s FOR SELECT USING (platform.tenant_root_in_scope())',
                   base || '_read', target);
    EXECUTE format('CREATE POLICY %I ON %s FOR UPDATE USING (platform.tenant_root_in_scope()) '
                   'WITH CHECK (platform.tenant_root_in_scope())', base || '_update', target);
    EXECUTE format('CREATE POLICY %I ON %s FOR DELETE USING (platform.tenant_root_in_scope())',
                   base || '_delete', target);
END
$$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0102', 'after r1 (9cec72d): 0 table(s), 11 column(s), 13 index(es), 2 other statement(s)', '4687e5fd52e138d03523cca6daa147e9e391c01721c45a3d2d080efd168c338d')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS seating.seat_price_band_seat_category_id_code_uniq;
-- DROP INDEX IF EXISTS seating.seat_seat_map_id_section_code_row_label_seat_number_uniq;
-- DROP INDEX IF EXISTS seating.seat_category_venue_id_code_uniq;
-- DROP INDEX IF EXISTS orders.sales_order_order_number_uniq;
-- DROP INDEX IF EXISTS ledger.tax_invoice_invoice_number_uniq;
-- DROP INDEX IF EXISTS ledger.tax_code_code_uniq;
-- DROP INDEX IF EXISTS ledger.journal_entry_entry_number_uniq;
-- DROP INDEX IF EXISTS ledger.credit_memo_credit_memo_number_uniq;
-- DROP INDEX IF EXISTS ledger.account_code_uniq;
-- DROP INDEX IF EXISTS platform.scope_tenant_root_uniq;
-- DROP INDEX IF EXISTS platform.scope_parent_id_idx;
-- DROP INDEX IF EXISTS catalogue.product_media_product_id_idx;
-- DROP INDEX IF EXISTS platform.scope_path_uniq;
-- ALTER TABLE catalogue.product_media DROP CONSTRAINT IF EXISTS product_media_product_id_fkey;
-- ALTER TABLE whitelabel.store_account DROP COLUMN IF EXISTS pass_certificate_expires_at;
-- ALTER TABLE whitelabel.store_account DROP COLUMN IF EXISTS has_pass_certificate;
-- ALTER TABLE whitelabel.store_account DROP COLUMN IF EXISTS pass_certificate_secret_ref;
-- ALTER TABLE whitelabel.store_account DROP COLUMN IF EXISTS pass_type_identifier;
-- ALTER TABLE platform.venue_settings DROP COLUMN IF EXISTS business_day_cutoff;
-- ALTER TABLE orders.sales_order DROP COLUMN IF EXISTS channel_profile_id;
-- ALTER TABLE orders.pos_shift DROP COLUMN IF EXISTS business_date;
-- ALTER TABLE catalogue.sales_channel DROP COLUMN IF EXISTS ticket_credential_format;
-- ALTER TABLE catalogue.product_media DROP COLUMN IF EXISTS product_id;
-- ALTER TABLE access.verification_method_policy DROP COLUMN IF EXISTS credential_format_override;
-- ALTER TABLE access.entitlement DROP COLUMN IF EXISTS credential_format;
-- DELETE FROM platform.schema_version WHERE version = 'V0102';
