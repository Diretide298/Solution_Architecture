-- V0102 -- tenant database, after r1 (a1ba956) (20261003).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (a1ba956), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 1 table(s), 10 column(s), 21 index(es), 1 other statement(s).

ALTER TABLE maintenance.incident ADD COLUMN IF NOT EXISTS escalation jsonb;

ALTER TABLE maintenance.incident ADD COLUMN IF NOT EXISTS reopen_count integer;

ALTER TABLE maintenance.incident_investigation_note ADD COLUMN IF NOT EXISTS kind text DEFAULT 'note' CONSTRAINT incident_investigation_note_kind_chk CHECK (kind IN ('note', 'statusChange', 'escalation', 'reopen'));

ALTER TABLE maintenance.incident_investigation_note ADD COLUMN IF NOT EXISTS from_status text;

ALTER TABLE maintenance.incident_investigation_note ADD COLUMN IF NOT EXISTS to_status text;

ALTER TABLE maintenance.incident_involved_party ADD COLUMN IF NOT EXISTS role text CONSTRAINT incident_involved_party_role_chk CHECK (role IN ('injured', 'involved', 'witness', 'reporter'));

ALTER TABLE maintenance.incident_involved_party ADD COLUMN IF NOT EXISTS is_contact_stored boolean;

CREATE TABLE IF NOT EXISTS maintenance.incident_media (
    id                                uuid PRIMARY KEY NOT NULL,
    incident_id                       uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT incident_media_kind_chk CHECK (kind IN ('photo', 'video', 'document')),
    status                            text NOT NULL CONSTRAINT incident_media_status_chk CHECK (status IN ('awaitingUpload', 'stored')),
    asset_ref                         uuid,
    caption                           text,
    captured_at                       timestamptz,
    uploaded_by_principal_id          uuid,
    created_at                        timestamptz
);

ALTER TABLE transport.fare_table ADD COLUMN IF NOT EXISTS effective_to timestamptz;

ALTER TABLE venuemap.visit_plan ADD COLUMN IF NOT EXISTS ownership text CONSTRAINT visit_plan_ownership_chk CHECK (ownership IN ('anonymous', 'account'));

ALTER TABLE venuemap.visit_plan_item ADD COLUMN IF NOT EXISTS add_on_product_ids text[];

CREATE INDEX IF NOT EXISTS hardware_certification_certified_by_principal_id_idx ON access.hardware_certification (certified_by_principal_id);

CREATE INDEX IF NOT EXISTS hardware_certification_model_id_idx ON access.hardware_certification (model_id);

CREATE INDEX IF NOT EXISTS request_assigned_to_principal_id_idx ON approvals.request (assigned_to_principal_id);

CREATE INDEX IF NOT EXISTS seat_pricing_rule_performance_id_idx ON catalogue.seat_pricing_rule (performance_id);

CREATE INDEX IF NOT EXISTS seat_pricing_rule_seat_map_id_idx ON catalogue.seat_pricing_rule (seat_map_id);

CREATE INDEX IF NOT EXISTS kitchen_routing_rule_default_station_id_idx ON fnb.kitchen_routing_rule (default_station_id);

CREATE INDEX IF NOT EXISTS kitchen_routing_rule_fallback_station_id_idx ON fnb.kitchen_routing_rule (fallback_station_id);

CREATE INDEX IF NOT EXISTS kitchen_routing_rule_outlet_id_idx ON fnb.kitchen_routing_rule (outlet_id);

CREATE INDEX IF NOT EXISTS table_reservation_taken_by_principal_id_idx ON fnb.table_reservation (taken_by_principal_id);

CREATE INDEX IF NOT EXISTS segment_owner_principal_id_idx ON marketing.segment (owner_principal_id);

CREATE INDEX IF NOT EXISTS pos_shift_recount_requested_by_principal_id_idx ON orders.pos_shift (recount_requested_by_principal_id);

CREATE INDEX IF NOT EXISTS till_shift_policy_venue_id_idx ON orders.till_shift_policy (venue_id);

CREATE INDEX IF NOT EXISTS device_approved_by_principal_id_idx ON platform.device (approved_by_principal_id);

CREATE INDEX IF NOT EXISTS device_tested_by_principal_id_idx ON platform.device (tested_by_principal_id);

CREATE INDEX IF NOT EXISTS outlet_department_id_idx ON platform.outlet (department_id);

CREATE INDEX IF NOT EXISTS outlet_sale_board_id_idx ON platform.outlet (sale_board_id);

CREATE INDEX IF NOT EXISTS workstation_outlet_id_idx ON platform.workstation (outlet_id);

CREATE INDEX IF NOT EXISTS config_version_approval_request_id_idx ON whitelabel.config_version (approval_request_id);

CREATE INDEX IF NOT EXISTS site_package_platform_staff_grant_id_idx ON whitelabel.site_package (platform_staff_grant_id);

CREATE INDEX IF NOT EXISTS site_package_requested_by_principal_id_idx ON whitelabel.site_package (requested_by_principal_id);

CREATE INDEX IF NOT EXISTS cookie_scan_finding_scan_run_id_idx ON marketing.cookie_scan_finding (scan_run_id);

SELECT platform.apply_tenant_rls('maintenance.incident_media'::regclass);

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0102', 'after r1 (a1ba956): 1 table(s), 10 column(s), 21 index(es), 1 other statement(s)', '45b0ed9f72a4e964787173bb07a94105d9b49a158cfc0cca8eb399437ddad7ff')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS marketing.cookie_scan_finding_scan_run_id_idx;
-- DROP INDEX IF EXISTS whitelabel.site_package_requested_by_principal_id_idx;
-- DROP INDEX IF EXISTS whitelabel.site_package_platform_staff_grant_id_idx;
-- DROP INDEX IF EXISTS whitelabel.config_version_approval_request_id_idx;
-- DROP INDEX IF EXISTS platform.workstation_outlet_id_idx;
-- DROP INDEX IF EXISTS platform.outlet_sale_board_id_idx;
-- DROP INDEX IF EXISTS platform.outlet_department_id_idx;
-- DROP INDEX IF EXISTS platform.device_tested_by_principal_id_idx;
-- DROP INDEX IF EXISTS platform.device_approved_by_principal_id_idx;
-- DROP INDEX IF EXISTS orders.till_shift_policy_venue_id_idx;
-- DROP INDEX IF EXISTS orders.pos_shift_recount_requested_by_principal_id_idx;
-- DROP INDEX IF EXISTS marketing.segment_owner_principal_id_idx;
-- DROP INDEX IF EXISTS fnb.table_reservation_taken_by_principal_id_idx;
-- DROP INDEX IF EXISTS fnb.kitchen_routing_rule_outlet_id_idx;
-- DROP INDEX IF EXISTS fnb.kitchen_routing_rule_fallback_station_id_idx;
-- DROP INDEX IF EXISTS fnb.kitchen_routing_rule_default_station_id_idx;
-- DROP INDEX IF EXISTS catalogue.seat_pricing_rule_seat_map_id_idx;
-- DROP INDEX IF EXISTS catalogue.seat_pricing_rule_performance_id_idx;
-- DROP INDEX IF EXISTS approvals.request_assigned_to_principal_id_idx;
-- DROP INDEX IF EXISTS access.hardware_certification_model_id_idx;
-- DROP INDEX IF EXISTS access.hardware_certification_certified_by_principal_id_idx;
-- ALTER TABLE venuemap.visit_plan_item DROP COLUMN IF EXISTS add_on_product_ids;
-- ALTER TABLE venuemap.visit_plan DROP COLUMN IF EXISTS ownership;
-- ALTER TABLE transport.fare_table DROP COLUMN IF EXISTS effective_to;
-- DROP TABLE IF EXISTS maintenance.incident_media;
-- ALTER TABLE maintenance.incident_involved_party DROP COLUMN IF EXISTS is_contact_stored;
-- ALTER TABLE maintenance.incident_involved_party DROP COLUMN IF EXISTS role;
-- ALTER TABLE maintenance.incident_investigation_note DROP COLUMN IF EXISTS to_status;
-- ALTER TABLE maintenance.incident_investigation_note DROP COLUMN IF EXISTS from_status;
-- ALTER TABLE maintenance.incident_investigation_note DROP COLUMN IF EXISTS kind;
-- ALTER TABLE maintenance.incident DROP COLUMN IF EXISTS reopen_count;
-- ALTER TABLE maintenance.incident DROP COLUMN IF EXISTS escalation;
-- DELETE FROM platform.schema_version WHERE version = 'V0102';
