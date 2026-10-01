-- V0100 -- tenant database, after r1 (a1ba956) (20261002).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (a1ba956), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 0 table(s), 31 column(s), 11 index(es), 0 other statement(s).

ALTER TABLE ledger.credit_memo ADD COLUMN IF NOT EXISTS legal_fx_rate numeric(18,6);

ALTER TABLE ledger.credit_memo ADD COLUMN IF NOT EXISTS invoice_supply_value numeric(18,4);

ALTER TABLE ledger.credit_memo ADD COLUMN IF NOT EXISTS corrected_supply_value numeric(18,4);

ALTER TABLE ledger.credit_memo ADD COLUMN IF NOT EXISTS supplier_name text;

ALTER TABLE ledger.credit_memo ADD COLUMN IF NOT EXISTS supplier_address text;

ALTER TABLE ledger.credit_memo ADD COLUMN IF NOT EXISTS supplier_tax_registration_number text;

ALTER TABLE ledger.credit_memo ADD COLUMN IF NOT EXISTS buyer_name text;

ALTER TABLE ledger.credit_memo ADD COLUMN IF NOT EXISTS buyer_address text;

ALTER TABLE ledger.credit_memo ADD COLUMN IF NOT EXISTS buyer_tax_registration_number text;

ALTER TABLE ledger.tax_invoice ADD COLUMN IF NOT EXISTS legal_currency text;

ALTER TABLE ledger.tax_invoice ADD COLUMN IF NOT EXISTS gross_amount_in_legal_currency numeric(18,4);

ALTER TABLE ledger.tax_invoice ADD COLUMN IF NOT EXISTS legal_fx_rate numeric(18,6);

ALTER TABLE ledger.tax_invoice ADD COLUMN IF NOT EXISTS legal_fx_rate_source text;

ALTER TABLE ledger.tax_invoice ADD COLUMN IF NOT EXISTS paid_currency text;

ALTER TABLE ledger.tax_invoice ADD COLUMN IF NOT EXISTS paid_amount numeric(18,4);

ALTER TABLE ledger.tax_invoice ADD COLUMN IF NOT EXISTS reverse_charge_statement text;

ALTER TABLE ledger.tax_invoice_line ADD COLUMN IF NOT EXISTS gross_amount_in_legal_currency numeric(18,4);

ALTER TABLE orders.refund ADD COLUMN IF NOT EXISTS tender_currency text;

ALTER TABLE orders.refund ADD COLUMN IF NOT EXISTS tender_amount numeric(18,4);

ALTER TABLE orders.sales_order ADD COLUMN IF NOT EXISTS charge_currency text;

ALTER TABLE orders.sales_order ADD COLUMN IF NOT EXISTS charge_fx_rate numeric(18,6);

ALTER TABLE orders.sales_order ADD COLUMN IF NOT EXISTS charge_fx_rate_id uuid;

ALTER TABLE orders.sales_order ADD COLUMN IF NOT EXISTS charge_total numeric(18,4);

ALTER TABLE orders.sales_order ADD COLUMN IF NOT EXISTS charge_rate_locked_until timestamptz;

ALTER TABLE platform.venue_settings ADD COLUMN IF NOT EXISTS charge_currencies text[];

ALTER TABLE reporting.report_column ADD COLUMN IF NOT EXISTS role text CONSTRAINT report_column_role_chk CHECK (role IN ('dimension', 'measure'));

ALTER TABLE reporting.report_column ADD COLUMN IF NOT EXISTS encoding text CONSTRAINT report_column_encoding_chk CHECK (encoding IN ('category', 'x', 'y', 'series', 'value', 'size', 'colour', 'location', 'stage', 'source', 'target', 'row', 'column', 'hierarchyLevel', 'label', 'tooltip'));

ALTER TABLE reporting.report_column ADD COLUMN IF NOT EXISTS axis text CONSTRAINT report_column_axis_chk CHECK (axis IN ('primary', 'secondary'));

ALTER TABLE reporting.report_column ADD COLUMN IF NOT EXISTS series_type text CONSTRAINT report_column_series_type_chk CHECK (series_type IN ('bar', 'line', 'area'));

ALTER TABLE reporting.report_column ADD COLUMN IF NOT EXISTS hierarchy_level integer;

ALTER TABLE reporting.report_column ADD COLUMN IF NOT EXISTS unit_label text CONSTRAINT report_column_unit_label_chk CHECK (char_length(unit_label) <= 40);

CREATE INDEX IF NOT EXISTS biometric_audit_event_device_id_idx ON access.biometric_audit_event (device_id);

CREATE INDEX IF NOT EXISTS credential_event_device_id_idx ON access.credential_event (device_id);

CREATE INDEX IF NOT EXISTS credential_sharing_case_primary_device_id_idx ON access.credential_sharing_case (primary_device_id);

CREATE INDEX IF NOT EXISTS device_binding_device_id_idx ON access.device_binding (device_id);

CREATE INDEX IF NOT EXISTS scan_event_device_id_idx ON access.scan_event (device_id);

CREATE INDEX IF NOT EXISTS security_alert_device_id_idx ON access.security_alert (device_id);

CREATE INDEX IF NOT EXISTS waiting_room_setting_venue_id_idx ON catalogue.waiting_room_setting (venue_id);

CREATE INDEX IF NOT EXISTS device_hardware_model_id_idx ON platform.device (hardware_model_id);

CREATE INDEX IF NOT EXISTS device_placement_device_id_idx ON access.device_placement (device_id);

CREATE INDEX IF NOT EXISTS waiting_room_setting_performance_id_idx ON catalogue.waiting_room_setting (performance_id);

CREATE INDEX IF NOT EXISTS waiting_room_setting_updated_by_principal_id_idx ON catalogue.waiting_room_setting (updated_by_principal_id);

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0100', 'after r1 (a1ba956): 0 table(s), 31 column(s), 11 index(es), 0 other statement(s)', 'ffd68ed3b5dfe5762c6545d92c44dc4291dd89710ba41590de14eeb5fa3e6c6f')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS catalogue.waiting_room_setting_updated_by_principal_id_idx;
-- DROP INDEX IF EXISTS catalogue.waiting_room_setting_performance_id_idx;
-- DROP INDEX IF EXISTS access.device_placement_device_id_idx;
-- DROP INDEX IF EXISTS platform.device_hardware_model_id_idx;
-- DROP INDEX IF EXISTS catalogue.waiting_room_setting_venue_id_idx;
-- DROP INDEX IF EXISTS access.security_alert_device_id_idx;
-- DROP INDEX IF EXISTS access.scan_event_device_id_idx;
-- DROP INDEX IF EXISTS access.device_binding_device_id_idx;
-- DROP INDEX IF EXISTS access.credential_sharing_case_primary_device_id_idx;
-- DROP INDEX IF EXISTS access.credential_event_device_id_idx;
-- DROP INDEX IF EXISTS access.biometric_audit_event_device_id_idx;
-- ALTER TABLE reporting.report_column DROP COLUMN IF EXISTS unit_label;
-- ALTER TABLE reporting.report_column DROP COLUMN IF EXISTS hierarchy_level;
-- ALTER TABLE reporting.report_column DROP COLUMN IF EXISTS series_type;
-- ALTER TABLE reporting.report_column DROP COLUMN IF EXISTS axis;
-- ALTER TABLE reporting.report_column DROP COLUMN IF EXISTS encoding;
-- ALTER TABLE reporting.report_column DROP COLUMN IF EXISTS role;
-- ALTER TABLE platform.venue_settings DROP COLUMN IF EXISTS charge_currencies;
-- ALTER TABLE orders.sales_order DROP COLUMN IF EXISTS charge_rate_locked_until;
-- ALTER TABLE orders.sales_order DROP COLUMN IF EXISTS charge_total;
-- ALTER TABLE orders.sales_order DROP COLUMN IF EXISTS charge_fx_rate_id;
-- ALTER TABLE orders.sales_order DROP COLUMN IF EXISTS charge_fx_rate;
-- ALTER TABLE orders.sales_order DROP COLUMN IF EXISTS charge_currency;
-- ALTER TABLE orders.refund DROP COLUMN IF EXISTS tender_amount;
-- ALTER TABLE orders.refund DROP COLUMN IF EXISTS tender_currency;
-- ALTER TABLE ledger.tax_invoice_line DROP COLUMN IF EXISTS gross_amount_in_legal_currency;
-- ALTER TABLE ledger.tax_invoice DROP COLUMN IF EXISTS reverse_charge_statement;
-- ALTER TABLE ledger.tax_invoice DROP COLUMN IF EXISTS paid_amount;
-- ALTER TABLE ledger.tax_invoice DROP COLUMN IF EXISTS paid_currency;
-- ALTER TABLE ledger.tax_invoice DROP COLUMN IF EXISTS legal_fx_rate_source;
-- ALTER TABLE ledger.tax_invoice DROP COLUMN IF EXISTS legal_fx_rate;
-- ALTER TABLE ledger.tax_invoice DROP COLUMN IF EXISTS gross_amount_in_legal_currency;
-- ALTER TABLE ledger.tax_invoice DROP COLUMN IF EXISTS legal_currency;
-- ALTER TABLE ledger.credit_memo DROP COLUMN IF EXISTS buyer_tax_registration_number;
-- ALTER TABLE ledger.credit_memo DROP COLUMN IF EXISTS buyer_address;
-- ALTER TABLE ledger.credit_memo DROP COLUMN IF EXISTS buyer_name;
-- ALTER TABLE ledger.credit_memo DROP COLUMN IF EXISTS supplier_tax_registration_number;
-- ALTER TABLE ledger.credit_memo DROP COLUMN IF EXISTS supplier_address;
-- ALTER TABLE ledger.credit_memo DROP COLUMN IF EXISTS supplier_name;
-- ALTER TABLE ledger.credit_memo DROP COLUMN IF EXISTS corrected_supply_value;
-- ALTER TABLE ledger.credit_memo DROP COLUMN IF EXISTS invoice_supply_value;
-- ALTER TABLE ledger.credit_memo DROP COLUMN IF EXISTS legal_fx_rate;
-- DELETE FROM platform.schema_version WHERE version = 'V0100';
