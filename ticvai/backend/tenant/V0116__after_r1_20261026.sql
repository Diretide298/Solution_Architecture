-- V0116 -- tenant database, after r1 (9cec72d) (20261026).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- 6 table(s), 44 column(s), 31 index(es), 41 other statement(s), 6 row-level security polic(ies) re-applied.

DO $$ BEGIN IF to_regclass('access.entitlement') IS NOT NULL THEN
ALTER TABLE access.entitlement ADD COLUMN IF NOT EXISTS change_version bigint;
END IF; END $$;

DO $$ BEGIN IF to_regclass('access.entitlement') IS NOT NULL THEN
ALTER TABLE access.entitlement ADD COLUMN IF NOT EXISTS media_linked_at timestamptz;
END IF; END $$;

DO $$ BEGIN IF to_regclass('access.entitlement') IS NOT NULL THEN
ALTER TABLE access.entitlement ADD COLUMN IF NOT EXISTS rotation_secret_ciphertext text;
END IF; END $$;

DO $$ BEGIN IF to_regclass('ai.proposed_action') IS NOT NULL THEN
ALTER TABLE ai.proposed_action ADD COLUMN IF NOT EXISTS confidence numeric(18,4);
END IF; END $$;

DO $$ BEGIN IF to_regclass('ai.proposed_action') IS NOT NULL THEN
ALTER TABLE ai.proposed_action ADD COLUMN IF NOT EXISTS basis text CONSTRAINT proposed_action_basis_chk CHECK (basis IN ('handMarked', 'seen'));
END IF; END $$;

DO $$ BEGIN IF to_regclass('ai.proposed_action') IS NOT NULL THEN
ALTER TABLE ai.proposed_action ADD COLUMN IF NOT EXISTS reasoning text;
END IF; END $$;

DO $$ BEGIN IF to_regclass('ai.proposed_action') IS NOT NULL THEN
ALTER TABLE ai.proposed_action ADD COLUMN IF NOT EXISTS distance_metres numeric(18,4);
END IF; END $$;

DO $$ BEGIN IF to_regclass('ai.proposed_action') IS NOT NULL THEN
ALTER TABLE ai.proposed_action ADD COLUMN IF NOT EXISTS map_id uuid;
END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'request' AND column_name = 'requested_by_principal_id' AND is_nullable = 'NO') THEN ALTER TABLE approvals.request ALTER COLUMN requested_by_principal_id DROP NOT NULL; END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.request') IS NOT NULL THEN
ALTER TABLE approvals.request ADD COLUMN IF NOT EXISTS requested_by_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.request') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'request' AND column_name = 'requested_by_principal_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'request' AND column_name = 'requested_by_subject_id') THEN
ALTER TABLE approvals.request DROP CONSTRAINT IF EXISTS request_requested_by_principal_id_requested_by_sub_b31f1c6e_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.request') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'request' AND column_name = 'requested_by_principal_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'request' AND column_name = 'requested_by_subject_id') THEN
ALTER TABLE approvals.request ADD CONSTRAINT request_requested_by_principal_id_requested_by_sub_b31f1c6e_chk CHECK (num_nonnulls(requested_by_principal_id, requested_by_subject_id) = 1) NOT VALID;
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.request') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'request' AND column_name = 'requested_by_principal_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'request' AND column_name = 'requested_by_subject_id') THEN
ALTER TABLE approvals.request VALIDATE CONSTRAINT request_requested_by_principal_id_requested_by_sub_b31f1c6e_chk;
END IF; END $$;

CREATE TABLE IF NOT EXISTS approvals.request_approver (
    id                                uuid PRIMARY KEY NOT NULL,
    request_id                        uuid NOT NULL,
    level                             integer NOT NULL,
    principal_id                      uuid NOT NULL,
    is_delegate                       boolean NOT NULL
);

DO $$ BEGIN IF to_regclass('approvals.rule') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'rule' AND column_name = 'condition') THEN
ALTER TABLE approvals.rule DROP CONSTRAINT IF EXISTS rule_condition_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.rule') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'rule' AND column_name = 'condition') THEN
ALTER TABLE approvals.rule ADD CONSTRAINT rule_condition_chk CHECK (char_length(condition) <= 500) NOT VALID;
END IF; END $$;

DO $$ BEGIN IF to_regclass('assets.media_asset') IS NOT NULL THEN
ALTER TABLE assets.media_asset ADD COLUMN IF NOT EXISTS has_transparency boolean;
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.event') IS NOT NULL THEN
ALTER TABLE catalogue.event ADD COLUMN IF NOT EXISTS scheduled_lifecycle_state text CONSTRAINT event_scheduled_lifecycle_state_chk CHECK (scheduled_lifecycle_state IN ('draft', 'planned', 'onSale', 'live', 'closed', 'cancelled', 'archived'));
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.event') IS NOT NULL THEN
ALTER TABLE catalogue.event ADD COLUMN IF NOT EXISTS scheduled_lifecycle_at timestamptz;
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.event') IS NOT NULL THEN
ALTER TABLE catalogue.event ADD COLUMN IF NOT EXISTS scheduled_lifecycle_reason text CONSTRAINT event_scheduled_lifecycle_reason_chk CHECK (char_length(scheduled_lifecycle_reason) <= 500);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.product') IS NOT NULL THEN
ALTER TABLE catalogue.product ADD COLUMN IF NOT EXISTS valid_to timestamptz;
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.product') IS NOT NULL THEN
ALTER TABLE catalogue.product ADD COLUMN IF NOT EXISTS add_on_product_ids text[];
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.product') IS NOT NULL THEN
ALTER TABLE catalogue.product ADD COLUMN IF NOT EXISTS created_at timestamptz;
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.product') IS NOT NULL THEN
ALTER TABLE catalogue.product ADD COLUMN IF NOT EXISTS updated_at timestamptz;
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.product_version') IS NOT NULL THEN
ALTER TABLE catalogue.product_version ADD COLUMN IF NOT EXISTS snapshot jsonb;
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.published_bundle') IS NOT NULL THEN
ALTER TABLE catalogue.published_bundle ADD COLUMN IF NOT EXISTS note text CONSTRAINT published_bundle_note_chk CHECK (char_length(note) <= 500);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.variant') IS NOT NULL THEN
ALTER TABLE catalogue.variant ADD COLUMN IF NOT EXISTS reference_price numeric(18,4);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.delegated_access') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'delegation_kind') THEN
ALTER TABLE identity.delegated_access DROP CONSTRAINT IF EXISTS delegated_access_delegation_kind_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.delegated_access') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'delegation_kind') THEN
ALTER TABLE identity.delegated_access ADD CONSTRAINT delegated_access_delegation_kind_chk CHECK (delegation_kind IN ('primaryHolder', 'familyMember', 'groupLeader', 'attendee', 'corporateAdmin', 'corporateMember', 'carer', 'sharedEntitlement')) NOT VALID;
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.delegated_access') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'delegation_kind') THEN
ALTER TABLE identity.delegated_access VALIDATE CONSTRAINT delegated_access_delegation_kind_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.delegated_access') IS NOT NULL THEN
ALTER TABLE identity.delegated_access ADD COLUMN IF NOT EXISTS revoked_by_kind text CONSTRAINT delegated_access_revoked_by_kind_chk CHECK (revoked_by_kind IN ('principal', 'subject', 'system'));
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.delegated_access') IS NOT NULL THEN
ALTER TABLE identity.delegated_access ADD COLUMN IF NOT EXISTS revoked_by_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.delegated_access') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'revoked_by_kind') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'revoked_by_subject_id') THEN
ALTER TABLE identity.delegated_access DROP CONSTRAINT IF EXISTS delegated_access_revoked_by_subject_id_when_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.delegated_access') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'revoked_by_kind') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'revoked_by_subject_id') THEN
ALTER TABLE identity.delegated_access ADD CONSTRAINT delegated_access_revoked_by_subject_id_when_chk CHECK (revoked_by_kind IS DISTINCT FROM 'subject' OR revoked_by_subject_id IS NOT NULL) NOT VALID;
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.delegated_access') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'revoked_by_kind') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'revoked_by_subject_id') THEN
ALTER TABLE identity.delegated_access VALIDATE CONSTRAINT delegated_access_revoked_by_subject_id_when_chk;
END IF; END $$;

CREATE TABLE IF NOT EXISTS identity.redirect_host (
    id                                uuid PRIMARY KEY NOT NULL,
    domain_id                         uuid NOT NULL,
    hostname                          text NOT NULL CONSTRAINT redirect_host_hostname_chk CHECK (char_length(hostname) <= 253),
    status                            text NOT NULL CONSTRAINT redirect_host_status_chk CHECK (char_length(status) <= 40),
    uae_pass_redirect                 text CONSTRAINT redirect_host_uae_pass_redirect_chk CHECK (uae_pass_redirect IN ('ready', 'pending', 'notApplicable')),
    last_event_at                     timestamptz NOT NULL
);

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'refresh_token' AND column_name = 'principal_id' AND is_nullable = 'NO') THEN ALTER TABLE identity.refresh_token ALTER COLUMN principal_id DROP NOT NULL; END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.refresh_token') IS NOT NULL THEN
ALTER TABLE identity.refresh_token ADD COLUMN IF NOT EXISTS subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.refresh_token') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'refresh_token' AND column_name = 'principal_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'refresh_token' AND column_name = 'subject_id') THEN
ALTER TABLE identity.refresh_token DROP CONSTRAINT IF EXISTS refresh_token_principal_id_subject_id_one_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.refresh_token') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'refresh_token' AND column_name = 'principal_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'refresh_token' AND column_name = 'subject_id') THEN
ALTER TABLE identity.refresh_token ADD CONSTRAINT refresh_token_principal_id_subject_id_one_chk CHECK (num_nonnulls(principal_id, subject_id) = 1) NOT VALID;
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.refresh_token') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'refresh_token' AND column_name = 'principal_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'refresh_token' AND column_name = 'subject_id') THEN
ALTER TABLE identity.refresh_token VALIDATE CONSTRAINT refresh_token_principal_id_subject_id_one_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.role_permission') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'role_permission' AND column_name = 'permission') THEN
ALTER TABLE identity.role_permission DROP CONSTRAINT IF EXISTS role_permission_permission_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.role_permission') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'role_permission' AND column_name = 'permission') THEN
ALTER TABLE identity.role_permission ADD CONSTRAINT role_permission_permission_chk CHECK (permission IN ('SESSION_FORCE_LOGOUT', 'USER_MANAGE', 'ROLE_MANAGE', 'PERMISSION_GRANT', 'PERMISSION_VIEW', 'PERMISSION_MANAGE', 'PLATFORM_TENANT_VIEW', 'PLATFORM_TENANT_MANAGE', 'PLATFORM_TENANT_TERMINATE', 'PLATFORM_PLAN_MANAGE', 'PLATFORM_CELL_VIEW', 'PLATFORM_CELL_MANAGE', 'PLATFORM_BILLING_VIEW', 'PLATFORM_AI_MANAGE', 'PLATFORM_BILLING_MANAGE', 'PLATFORM_RELEASE_VIEW', 'PLATFORM_RELEASE_MANAGE', 'PLATFORM_RELEASE_PROMOTE', 'PLATFORM_MIGRATION_VIEW', 'PLATFORM_MIGRATION_APPLY', 'PLATFORM_TENANT_ACCESS', 'TENANT_CONFIGURE', 'TENANT_VIEW', 'TENANT_PUBLISH', 'SCOPE_VIEW', 'SCOPE_MANAGE', 'REGION_CONFIGURE', 'WORKSTATION_CONFIGURE', 'PRODUCT_VIEW', 'PRODUCT_CONFIGURE', 'PRODUCT_APPROVE', 'PRODUCT_PUBLISH', 'SALES_CHANNEL_OVERRIDE', 'PRICE_VIEW', 'PRICE_CONFIGURE', 'EVENT_CONFIGURE', 'PERFORMANCE_CONFIGURE', 'CAPACITY_CONFIGURE', 'ORDER_VIEW', 'ORDER_VIEW_OTHER', 'ORDER_CREATE', 'ORDER_MODIFY', 'ORDER_DISCOUNT', 'ORDER_CANCEL', 'ORDER_VOID', 'ORDER_REFUND', 'ORDER_REFUND_APPROVE', 'ORDER_REFUND_BULK', 'ORDER_EXCHANGE', 'ORDER_RESCHEDULE', 'ORDER_REPRINT', 'PRICE_OVERRIDE', 'DISCOUNT_APPLY', 'CREDIT_MANAGE', 'CREDIT_OVERRIDE', 'WALLET_VIEW', 'WALLET_OPERATE', 'WALLET_CONFIGURE', 'PAYMENT_VIEW', 'PAYMENT_CONFIGURE', 'PAYMENT_PROVIDER_MANAGE', 'PAYMENT_DISPUTE', 'SHIFT_OPEN', 'SHIFT_CLOSE', 'SHIFT_SUSPEND', 'SHIFT_CLOSE_OTHER', 'SHIFT_APPROVE_OPEN', 'SHIFT_APPROVE_CLOSE', 'SHIFT_REOPEN', 'CASH_LIFT', 'CASH_ADD', 'CASH_NO_SALE', 'DEPOSIT_BOX_MODIFY_OWN', 'DEPOSIT_BOX_MODIFY_OTHER', 'OVERSHORT_ACCEPT', 'ACCESS_VALIDATE', 'ACCESS_OVERRIDE', 'ACCESS_POINT_CONFIGURE', 'TURNSTILE_MODE_SET', 'TICKET_LOOKUP', 'ENTITLEMENT_USE', 'ACCREDITATION_VIEW', 'ACCREDITATION_APPLY', 'ACCREDITATION_APPROVE', 'ACCREDITATION_ISSUE', 'ACCREDITATION_MANAGE', 'ACCREDITATION_CONFIGURE', 'REPORT_VIEW_OWN', 'REPORT_VIEW_WORKSTATION', 'REPORT_VIEW_VENUE', 'REPORT_VIEW_REGION', 'REPORT_VIEW_TENANT', 'REPORT_EXPORT', 'REPORT_EXPORT_PII', 'REPORT_MANAGE', 'REPORT_SCHEDULE', 'LEDGER_VIEW', 'LEDGER_POST', 'LEDGER_APPROVE', 'TAX_CONFIGURE', 'ACCOUNT_CONFIGURE', 'SETTLEMENT_VIEW', 'SETTLEMENT_RECONCILE', 'GUEST_VIEW', 'GUEST_VIEW_PII', 'GUEST_MANAGE', 'VENUE_MAP_VIEW', 'VENUE_MAP_MANAGE', 'VENUE_MAP_PUBLISH', 'RESOURCE_VIEW', 'RESOURCE_BOOK', 'RESOURCE_MANAGE', 'RESOURCE_CONFIGURE', 'RENTAL_VIEW', 'RENTAL_BOOK', 'RENTAL_OPERATE', 'RENTAL_MANAGE', 'RENTAL_CONFIGURE', 'RENTAL_PRICE', 'RENTAL_APPROVE', 'RENTAL_OVERRIDE', 'DEVELOPER_VIEW', 'DEVELOPER_MANAGE', 'DEVELOPER_ADMIN', 'LOYALTY_ACCRUE', 'LOYALTY_REDEEM', 'LOYALTY_ADJUST', 'MEMBERSHIP_VIEW', 'MEMBERSHIP_MANAGE', 'MARKETING_VIEW', 'MARKETING_MANAGE', 'MARKETING_SEND', 'CASE_VIEW', 'CASE_MANAGE', 'ASSET_LIBRARY_VIEW', 'ASSET_LIBRARY_MANAGE', 'ASSET_LIBRARY_APPROVE', 'ASSET_LIBRARY_SHARE', 'QUEUE_VIEW', 'QUEUE_MANAGE', 'QUEUE_REDEEM', 'QUEUE_OVERRIDE', 'TRANSPORT_VIEW', 'TRANSPORT_MANAGE', 'TRANSPORT_PRICE', 'ASSET_VIEW', 'ASSET_MANAGE', 'WORK_ORDER_VIEW', 'WORK_ORDER_MANAGE', 'WORK_ORDER_VERIFY', 'INSPECTION_VIEW', 'INSPECTION_SUBMIT', 'INSPECTION_MANAGE', 'INCIDENT_REPORT', 'INCIDENT_VIEW', 'INCIDENT_MANAGE', 'KIOSK_ATTEND', 'DEVICE_VIEW', 'DEVICE_CONFIGURE', 'DEVICE_MANAGE', 'APPROVAL_ACT', 'APPROVAL_DELEGATE', 'AI_USE', 'AI_CONFIGURE', 'AI_APPROVE', 'AI_AUDIT_VIEW', 'RISK_REVIEW', 'RISK_INVESTIGATE', 'AUDIT_VIEW', 'APPROVAL_VIEW', 'APPROVAL_REQUEST', 'APPROVAL_DECIDE', 'APPROVAL_CONFIGURE', 'MAINTENANCE_EXECUTE', 'MAINTENANCE_APPROVE', 'WORKFORCE_VIEW', 'WORKFORCE_MANAGE', 'ATTENDANCE_RECORD', 'ANNOUNCEMENT_PUBLISH', 'ANNOUNCEMENT_EMERGENCY', 'PARTNER_VIEW', 'PARTNER_MANAGE', 'PARKING_CONFIGURE', 'PAYMENT_VOID', 'PROCUREMENT_VIEW', 'PROCUREMENT_REQUEST', 'PROCUREMENT_MANAGE', 'PROCUREMENT_RECEIVE', 'CORE_AI_PUBLISH', 'TICKETING_AI_PUBLISH', 'ACCESS_AI_PUBLISH', 'FNB_AI_PUBLISH', 'RETAIL_AI_PUBLISH', 'INVENTORY_AI_PUBLISH', 'SEATING_AI_PUBLISH', 'MEMBERSHIP_AI_PUBLISH', 'MARKETING_AI_PUBLISH', 'RESOURCES_AI_PUBLISH', 'QUEUE_AI_PUBLISH', 'TRANSPORT_AI_PUBLISH', 'GAMES_AI_PUBLISH', 'MAINTENANCE_AI_PUBLISH', 'ACCREDITATION_AI_PUBLISH', 'PARTNER_AI_PUBLISH', 'ANALYTICS_AI_PUBLISH', 'BIOMETRIC_IMAGE_VIEW', 'ACCESS_DIRECTION_SET', 'REPORT_GOVERNANCE_MANAGE')) NOT VALID;
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.role_permission') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'role_permission' AND column_name = 'permission') THEN
ALTER TABLE identity.role_permission VALIDATE CONSTRAINT role_permission_permission_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.session') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'session' AND column_name = 'ended_at') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'session' AND column_name = 'status') THEN
ALTER TABLE identity.session DROP CONSTRAINT IF EXISTS session_ended_at_null_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.session') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'session' AND column_name = 'ended_at') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'session' AND column_name = 'status') THEN
ALTER TABLE identity.session ADD CONSTRAINT session_ended_at_null_chk CHECK ((status IS NOT DISTINCT FROM 'active') = (ended_at IS NULL)) NOT VALID;
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.session') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'session' AND column_name = 'ended_at') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'session' AND column_name = 'status') THEN
ALTER TABLE identity.session VALIDATE CONSTRAINT session_ended_at_null_chk;
END IF; END $$;

CREATE TABLE IF NOT EXISTS identity.subject_data_export (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    format                            text NOT NULL CONSTRAINT subject_data_export_format_chk CHECK (format IN ('json', 'csv', 'pdf')),
    status                            text NOT NULL DEFAULT 'running' CONSTRAINT subject_data_export_status_chk CHECK (status IN ('awaitingApproval', 'running', 'ready', 'failed', 'rejected', 'expired')),
    file_ref                          text CONSTRAINT subject_data_export_file_ref_chk CHECK (char_length(file_ref) <= 500),
    file_size_bytes                   bigint,
    failure_reason                    text CONSTRAINT subject_data_export_failure_reason_chk CHECK (char_length(failure_reason) <= 500),
    requested_at                      timestamptz NOT NULL,
    ready_at                          timestamptz
);

DO $$ BEGIN IF to_regclass('identity.subject_holding') IS NOT NULL THEN
ALTER TABLE identity.subject_holding ADD COLUMN IF NOT EXISTS order_number text CONSTRAINT subject_holding_order_number_chk CHECK (char_length(order_number) <= 40);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.subject_holding') IS NOT NULL THEN
ALTER TABLE identity.subject_holding ADD COLUMN IF NOT EXISTS verified_contact_ref text CONSTRAINT subject_holding_verified_contact_ref_chk CHECK (char_length(verified_contact_ref) <= 128);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.privacy_request') IS NOT NULL THEN
ALTER TABLE marketing.privacy_request ADD COLUMN IF NOT EXISTS approval_request_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.group_booking') IS NOT NULL THEN
ALTER TABLE orders.group_booking ADD COLUMN IF NOT EXISTS version integer DEFAULT 1;
END IF; END $$;

CREATE TABLE IF NOT EXISTS orders.refund_line (
    id                                uuid PRIMARY KEY NOT NULL,
    refund_id                         uuid NOT NULL,
    order_line_id                     uuid NOT NULL,
    refunded_amount                   numeric(18,4) NOT NULL,
    applied_percentage                numeric(18,4)
);

CREATE TABLE IF NOT EXISTS orders.refund_payment (
    id                                uuid PRIMARY KEY NOT NULL,
    refund_id                         uuid NOT NULL,
    payment_id                        uuid NOT NULL,
    refunded_amount                   numeric(18,4) NOT NULL,
    tender_amount                     numeric(18,4)
);

DO $$ BEGIN IF to_regclass('orders.refund_policy_time_band') IS NOT NULL THEN
ALTER TABLE orders.refund_policy_time_band ADD COLUMN IF NOT EXISTS refund_type text;
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.stored_value_authorisation') IS NOT NULL THEN
ALTER TABLE orders.stored_value_authorisation ADD COLUMN IF NOT EXISTS wallet_hold_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.audit_read') IS NOT NULL THEN
ALTER TABLE platform.audit_read ADD COLUMN IF NOT EXISTS org_unit_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.venue_settings') IS NOT NULL THEN
ALTER TABLE platform.venue_settings ADD COLUMN IF NOT EXISTS step_minutes integer CONSTRAINT venue_settings_step_minutes_chk CHECK (step_minutes IN (15, 30, 60));
END IF; END $$;

DO $$ BEGIN IF to_regclass('promotions.promotion') IS NOT NULL THEN
ALTER TABLE promotions.promotion ADD COLUMN IF NOT EXISTS name_localised jsonb;
END IF; END $$;

DO $$ BEGIN IF to_regclass('promotions.promotion') IS NOT NULL THEN
ALTER TABLE promotions.promotion ADD COLUMN IF NOT EXISTS description_localised jsonb;
END IF; END $$;

DO $$ BEGIN IF to_regclass('promotions.promotion') IS NOT NULL THEN
ALTER TABLE promotions.promotion ADD COLUMN IF NOT EXISTS label jsonb;
END IF; END $$;

DO $$ BEGIN IF to_regclass('promotions.promotion') IS NOT NULL THEN
ALTER TABLE promotions.promotion ADD COLUMN IF NOT EXISTS venues jsonb;
END IF; END $$;

DO $$ BEGIN IF to_regclass('reporting.report_definition') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'reporting' AND table_name = 'report_definition' AND column_name = 'required_permission') THEN
ALTER TABLE reporting.report_definition DROP CONSTRAINT IF EXISTS report_definition_required_permission_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('reporting.report_definition') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'reporting' AND table_name = 'report_definition' AND column_name = 'required_permission') THEN
ALTER TABLE reporting.report_definition ADD CONSTRAINT report_definition_required_permission_chk CHECK (required_permission IN ('SESSION_FORCE_LOGOUT', 'USER_MANAGE', 'ROLE_MANAGE', 'PERMISSION_GRANT', 'PERMISSION_VIEW', 'PERMISSION_MANAGE', 'PLATFORM_TENANT_VIEW', 'PLATFORM_TENANT_MANAGE', 'PLATFORM_TENANT_TERMINATE', 'PLATFORM_PLAN_MANAGE', 'PLATFORM_CELL_VIEW', 'PLATFORM_CELL_MANAGE', 'PLATFORM_BILLING_VIEW', 'PLATFORM_AI_MANAGE', 'PLATFORM_BILLING_MANAGE', 'PLATFORM_RELEASE_VIEW', 'PLATFORM_RELEASE_MANAGE', 'PLATFORM_RELEASE_PROMOTE', 'PLATFORM_MIGRATION_VIEW', 'PLATFORM_MIGRATION_APPLY', 'PLATFORM_TENANT_ACCESS', 'TENANT_CONFIGURE', 'TENANT_VIEW', 'TENANT_PUBLISH', 'SCOPE_VIEW', 'SCOPE_MANAGE', 'REGION_CONFIGURE', 'WORKSTATION_CONFIGURE', 'PRODUCT_VIEW', 'PRODUCT_CONFIGURE', 'PRODUCT_APPROVE', 'PRODUCT_PUBLISH', 'SALES_CHANNEL_OVERRIDE', 'PRICE_VIEW', 'PRICE_CONFIGURE', 'EVENT_CONFIGURE', 'PERFORMANCE_CONFIGURE', 'CAPACITY_CONFIGURE', 'ORDER_VIEW', 'ORDER_VIEW_OTHER', 'ORDER_CREATE', 'ORDER_MODIFY', 'ORDER_DISCOUNT', 'ORDER_CANCEL', 'ORDER_VOID', 'ORDER_REFUND', 'ORDER_REFUND_APPROVE', 'ORDER_REFUND_BULK', 'ORDER_EXCHANGE', 'ORDER_RESCHEDULE', 'ORDER_REPRINT', 'PRICE_OVERRIDE', 'DISCOUNT_APPLY', 'CREDIT_MANAGE', 'CREDIT_OVERRIDE', 'WALLET_VIEW', 'WALLET_OPERATE', 'WALLET_CONFIGURE', 'PAYMENT_VIEW', 'PAYMENT_CONFIGURE', 'PAYMENT_PROVIDER_MANAGE', 'PAYMENT_DISPUTE', 'SHIFT_OPEN', 'SHIFT_CLOSE', 'SHIFT_SUSPEND', 'SHIFT_CLOSE_OTHER', 'SHIFT_APPROVE_OPEN', 'SHIFT_APPROVE_CLOSE', 'SHIFT_REOPEN', 'CASH_LIFT', 'CASH_ADD', 'CASH_NO_SALE', 'DEPOSIT_BOX_MODIFY_OWN', 'DEPOSIT_BOX_MODIFY_OTHER', 'OVERSHORT_ACCEPT', 'ACCESS_VALIDATE', 'ACCESS_OVERRIDE', 'ACCESS_POINT_CONFIGURE', 'TURNSTILE_MODE_SET', 'TICKET_LOOKUP', 'ENTITLEMENT_USE', 'ACCREDITATION_VIEW', 'ACCREDITATION_APPLY', 'ACCREDITATION_APPROVE', 'ACCREDITATION_ISSUE', 'ACCREDITATION_MANAGE', 'ACCREDITATION_CONFIGURE', 'REPORT_VIEW_OWN', 'REPORT_VIEW_WORKSTATION', 'REPORT_VIEW_VENUE', 'REPORT_VIEW_REGION', 'REPORT_VIEW_TENANT', 'REPORT_EXPORT', 'REPORT_EXPORT_PII', 'REPORT_MANAGE', 'REPORT_SCHEDULE', 'LEDGER_VIEW', 'LEDGER_POST', 'LEDGER_APPROVE', 'TAX_CONFIGURE', 'ACCOUNT_CONFIGURE', 'SETTLEMENT_VIEW', 'SETTLEMENT_RECONCILE', 'GUEST_VIEW', 'GUEST_VIEW_PII', 'GUEST_MANAGE', 'VENUE_MAP_VIEW', 'VENUE_MAP_MANAGE', 'VENUE_MAP_PUBLISH', 'RESOURCE_VIEW', 'RESOURCE_BOOK', 'RESOURCE_MANAGE', 'RESOURCE_CONFIGURE', 'RENTAL_VIEW', 'RENTAL_BOOK', 'RENTAL_OPERATE', 'RENTAL_MANAGE', 'RENTAL_CONFIGURE', 'RENTAL_PRICE', 'RENTAL_APPROVE', 'RENTAL_OVERRIDE', 'DEVELOPER_VIEW', 'DEVELOPER_MANAGE', 'DEVELOPER_ADMIN', 'LOYALTY_ACCRUE', 'LOYALTY_REDEEM', 'LOYALTY_ADJUST', 'MEMBERSHIP_VIEW', 'MEMBERSHIP_MANAGE', 'MARKETING_VIEW', 'MARKETING_MANAGE', 'MARKETING_SEND', 'CASE_VIEW', 'CASE_MANAGE', 'ASSET_LIBRARY_VIEW', 'ASSET_LIBRARY_MANAGE', 'ASSET_LIBRARY_APPROVE', 'ASSET_LIBRARY_SHARE', 'QUEUE_VIEW', 'QUEUE_MANAGE', 'QUEUE_REDEEM', 'QUEUE_OVERRIDE', 'TRANSPORT_VIEW', 'TRANSPORT_MANAGE', 'TRANSPORT_PRICE', 'ASSET_VIEW', 'ASSET_MANAGE', 'WORK_ORDER_VIEW', 'WORK_ORDER_MANAGE', 'WORK_ORDER_VERIFY', 'INSPECTION_VIEW', 'INSPECTION_SUBMIT', 'INSPECTION_MANAGE', 'INCIDENT_REPORT', 'INCIDENT_VIEW', 'INCIDENT_MANAGE', 'KIOSK_ATTEND', 'DEVICE_VIEW', 'DEVICE_CONFIGURE', 'DEVICE_MANAGE', 'APPROVAL_ACT', 'APPROVAL_DELEGATE', 'AI_USE', 'AI_CONFIGURE', 'AI_APPROVE', 'AI_AUDIT_VIEW', 'RISK_REVIEW', 'RISK_INVESTIGATE', 'AUDIT_VIEW', 'APPROVAL_VIEW', 'APPROVAL_REQUEST', 'APPROVAL_DECIDE', 'APPROVAL_CONFIGURE', 'MAINTENANCE_EXECUTE', 'MAINTENANCE_APPROVE', 'WORKFORCE_VIEW', 'WORKFORCE_MANAGE', 'ATTENDANCE_RECORD', 'ANNOUNCEMENT_PUBLISH', 'ANNOUNCEMENT_EMERGENCY', 'PARTNER_VIEW', 'PARTNER_MANAGE', 'PARKING_CONFIGURE', 'PAYMENT_VOID', 'PROCUREMENT_VIEW', 'PROCUREMENT_REQUEST', 'PROCUREMENT_MANAGE', 'PROCUREMENT_RECEIVE', 'CORE_AI_PUBLISH', 'TICKETING_AI_PUBLISH', 'ACCESS_AI_PUBLISH', 'FNB_AI_PUBLISH', 'RETAIL_AI_PUBLISH', 'INVENTORY_AI_PUBLISH', 'SEATING_AI_PUBLISH', 'MEMBERSHIP_AI_PUBLISH', 'MARKETING_AI_PUBLISH', 'RESOURCES_AI_PUBLISH', 'QUEUE_AI_PUBLISH', 'TRANSPORT_AI_PUBLISH', 'GAMES_AI_PUBLISH', 'MAINTENANCE_AI_PUBLISH', 'ACCREDITATION_AI_PUBLISH', 'PARTNER_AI_PUBLISH', 'ANALYTICS_AI_PUBLISH', 'BIOMETRIC_IMAGE_VIEW', 'ACCESS_DIRECTION_SET', 'REPORT_GOVERNANCE_MANAGE')) NOT VALID;
END IF; END $$;

DO $$ BEGIN IF to_regclass('reporting.report_definition') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'reporting' AND table_name = 'report_definition' AND column_name = 'required_permission') THEN
ALTER TABLE reporting.report_definition VALIDATE CONSTRAINT report_definition_required_permission_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('retail.merchandise') IS NOT NULL AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'retail' AND table_name = 'merchandise' AND column_name = 'is_published') THEN
ALTER TABLE retail.merchandise ADD COLUMN IF NOT EXISTS is_published boolean DEFAULT false;
UPDATE retail.merchandise SET is_published = true;
END IF; END $$;

DO $$ BEGIN IF to_regclass('retail.shop_and_drop') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'retail' AND table_name = 'shop_and_drop' AND column_name = 'drop_reference') THEN
ALTER TABLE retail.shop_and_drop DROP CONSTRAINT IF EXISTS shop_and_drop_drop_reference_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('retail.shop_and_drop') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'retail' AND table_name = 'shop_and_drop' AND column_name = 'drop_reference') THEN
ALTER TABLE retail.shop_and_drop ADD CONSTRAINT shop_and_drop_drop_reference_chk CHECK (char_length(drop_reference) <= 32) NOT VALID;
END IF; END $$;

DO $$ BEGIN IF to_regclass('retail.shop_and_drop') IS NOT NULL THEN
ALTER TABLE retail.shop_and_drop ADD COLUMN IF NOT EXISTS collection_note text CONSTRAINT shop_and_drop_collection_note_chk CHECK (char_length(collection_note) <= 500);
END IF; END $$;

DO $$ BEGIN IF to_regclass('tenancy.device_telemetry') IS NOT NULL THEN
ALTER TABLE tenancy.device_telemetry ADD COLUMN IF NOT EXISTS sync_backlog integer;
END IF; END $$;

DO $$ BEGIN IF to_regclass('tenancy.device_telemetry') IS NOT NULL THEN
ALTER TABLE tenancy.device_telemetry ADD COLUMN IF NOT EXISTS error_count integer;
END IF; END $$;

DO $$ BEGIN IF to_regclass('venuemap.import_job') IS NOT NULL THEN
ALTER TABLE venuemap.import_job ADD COLUMN IF NOT EXISTS source_ref uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('venuemap.import_job') IS NOT NULL THEN
ALTER TABLE venuemap.import_job ADD COLUMN IF NOT EXISTS format text CONSTRAINT import_job_format_chk CHECK (format IN ('pdfPlan', 'svgPlan', 'dwgPlan', 'dxfPlan', 'rasterPlan', 'glbModel', 'navigationFile'));
END IF; END $$;

DO $$ BEGIN IF to_regclass('venuemap.import_job') IS NOT NULL THEN
ALTER TABLE venuemap.import_job ADD COLUMN IF NOT EXISTS created_at timestamptz;
END IF; END $$;

DO $$ BEGIN IF to_regclass('whitelabel.custom_domain') IS NOT NULL THEN
ALTER TABLE whitelabel.custom_domain ADD COLUMN IF NOT EXISTS validation_expires_at timestamptz;
END IF; END $$;

DO $$ BEGIN IF to_regclass('whitelabel.site_package') IS NOT NULL THEN
ALTER TABLE whitelabel.site_package ADD COLUMN IF NOT EXISTS package_asset_ref uuid;
END IF; END $$;

CREATE TABLE IF NOT EXISTS whitelabel.ui_string_pack (
    id                                uuid PRIMARY KEY NOT NULL,
    language                          text NOT NULL,
    coverage_percent                  numeric(18,4) NOT NULL,
    status                            text NOT NULL CONSTRAINT ui_string_pack_status_chk CHECK (status IN ('complete', 'draft')),
    scope_path                        ltree NOT NULL
);

DO $$ BEGIN IF to_regclass('approvals.request') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'request' AND column_name = 'requested_by_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'request_requested_by_subject_id_fkey' AND conrelid = to_regclass('approvals.request')) THEN
ALTER TABLE approvals.request ADD CONSTRAINT request_requested_by_subject_id_fkey FOREIGN KEY (requested_by_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.request_approver') IS NOT NULL AND to_regclass('identity.principal') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'request_approver' AND column_name = 'principal_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'request_approver_principal_id_fkey' AND conrelid = to_regclass('approvals.request_approver')) THEN
ALTER TABLE approvals.request_approver ADD CONSTRAINT request_approver_principal_id_fkey FOREIGN KEY (principal_id) REFERENCES identity.principal(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.request_approver') IS NOT NULL AND to_regclass('approvals.request') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'request_approver' AND column_name = 'request_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'request_approver_request_id_fkey' AND conrelid = to_regclass('approvals.request_approver')) THEN
ALTER TABLE approvals.request_approver ADD CONSTRAINT request_approver_request_id_fkey FOREIGN KEY (request_id) REFERENCES approvals.request(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.delegated_access') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'revoked_by_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'delegated_access_revoked_by_subject_id_fkey' AND conrelid = to_regclass('identity.delegated_access')) THEN
ALTER TABLE identity.delegated_access ADD CONSTRAINT delegated_access_revoked_by_subject_id_fkey FOREIGN KEY (revoked_by_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.refresh_token') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'refresh_token' AND column_name = 'subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'refresh_token_subject_id_fkey' AND conrelid = to_regclass('identity.refresh_token')) THEN
ALTER TABLE identity.refresh_token ADD CONSTRAINT refresh_token_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.subject_data_export') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'subject_data_export' AND column_name = 'subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'subject_data_export_subject_id_fkey' AND conrelid = to_regclass('identity.subject_data_export')) THEN
ALTER TABLE identity.subject_data_export ADD CONSTRAINT subject_data_export_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.refund_line') IS NOT NULL AND to_regclass('orders.order_line') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'refund_line' AND column_name = 'order_line_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'refund_line_order_line_id_fkey' AND conrelid = to_regclass('orders.refund_line')) THEN
ALTER TABLE orders.refund_line ADD CONSTRAINT refund_line_order_line_id_fkey FOREIGN KEY (order_line_id) REFERENCES orders.order_line(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.refund_line') IS NOT NULL AND to_regclass('orders.refund') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'refund_line' AND column_name = 'refund_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'refund_line_refund_id_fkey' AND conrelid = to_regclass('orders.refund_line')) THEN
ALTER TABLE orders.refund_line ADD CONSTRAINT refund_line_refund_id_fkey FOREIGN KEY (refund_id) REFERENCES orders.refund(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.refund_payment') IS NOT NULL AND to_regclass('orders.payment') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'refund_payment' AND column_name = 'payment_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'refund_payment_payment_id_fkey' AND conrelid = to_regclass('orders.refund_payment')) THEN
ALTER TABLE orders.refund_payment ADD CONSTRAINT refund_payment_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES orders.payment(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.refund_payment') IS NOT NULL AND to_regclass('orders.refund') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'refund_payment' AND column_name = 'refund_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'refund_payment_refund_id_fkey' AND conrelid = to_regclass('orders.refund_payment')) THEN
ALTER TABLE orders.refund_payment ADD CONSTRAINT refund_payment_refund_id_fkey FOREIGN KEY (refund_id) REFERENCES orders.refund(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.audit_read') IS NOT NULL AND to_regclass('platform.scope') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'audit_read' AND column_name = 'org_unit_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'audit_read_org_unit_id_fkey' AND conrelid = to_regclass('platform.audit_read')) THEN
ALTER TABLE platform.audit_read ADD CONSTRAINT audit_read_org_unit_id_fkey FOREIGN KEY (org_unit_id) REFERENCES platform.scope(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('access.entitlement') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'access' AND table_name = 'entitlement' AND column_name = 'change_version') THEN CREATE SEQUENCE IF NOT EXISTS access.entitlement_change_version_seq; CREATE OR REPLACE FUNCTION access.entitlement_change_version_set() RETURNS trigger LANGUAGE plpgsql AS $f$ BEGIN NEW.change_version := nextval('access.entitlement_change_version_seq'); RETURN NEW; END $f$; DROP TRIGGER IF EXISTS entitlement_change_version_trg ON access.entitlement; CREATE TRIGGER entitlement_change_version_trg BEFORE INSERT OR UPDATE ON access.entitlement FOR EACH ROW EXECUTE FUNCTION access.entitlement_change_version_set(); END IF; END $$;

DO $$ BEGIN IF to_regclass('access.entitlement') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'access' AND table_name = 'entitlement' AND column_name = 'change_version') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'access' AND table_name = 'entitlement' AND column_name = 'venue_id') THEN
CREATE INDEX IF NOT EXISTS entitlement_venue_id_change_version_idx ON access.entitlement (venue_id, change_version);
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.request') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'request' AND column_name = 'requested_by_subject_id') THEN
CREATE INDEX IF NOT EXISTS request_requested_by_subject_id_idx ON approvals.request (requested_by_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.request_approver') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'request_approver' AND column_name = 'principal_id') THEN
CREATE INDEX IF NOT EXISTS request_approver_principal_id_idx ON approvals.request_approver (principal_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.request_approver') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'request_approver' AND column_name = 'request_id') THEN
CREATE INDEX IF NOT EXISTS request_approver_request_id_idx ON approvals.request_approver (request_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.delegated_access') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'revoked_by_subject_id') THEN
CREATE INDEX IF NOT EXISTS delegated_access_revoked_by_subject_id_idx ON identity.delegated_access (revoked_by_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.refresh_token') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'refresh_token' AND column_name = 'subject_id') THEN
CREATE INDEX IF NOT EXISTS refresh_token_subject_id_idx ON identity.refresh_token (subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.subject_data_export') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'subject_data_export' AND column_name = 'subject_id') THEN
CREATE INDEX IF NOT EXISTS subject_data_export_subject_id_idx ON identity.subject_data_export (subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.refund_line') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'refund_line' AND column_name = 'order_line_id') THEN
CREATE INDEX IF NOT EXISTS refund_line_order_line_id_idx ON orders.refund_line (order_line_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.refund_line') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'refund_line' AND column_name = 'refund_id') THEN
CREATE INDEX IF NOT EXISTS refund_line_refund_id_idx ON orders.refund_line (refund_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.refund_payment') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'refund_payment' AND column_name = 'payment_id') THEN
CREATE INDEX IF NOT EXISTS refund_payment_payment_id_idx ON orders.refund_payment (payment_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.refund_payment') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'refund_payment' AND column_name = 'refund_id') THEN
CREATE INDEX IF NOT EXISTS refund_payment_refund_id_idx ON orders.refund_payment (refund_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.audit_read') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'audit_read' AND column_name = 'org_unit_id') THEN
CREATE INDEX IF NOT EXISTS audit_read_org_unit_id_idx ON platform.audit_read (org_unit_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.payment_link') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'payment_link' AND column_name = 'token') THEN
CREATE UNIQUE INDEX IF NOT EXISTS payment_link_token_uniq ON orders.payment_link (token);
END IF; END $$;

DO $$ BEGIN IF to_regclass('retail.shop_and_drop') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'retail' AND table_name = 'shop_and_drop' AND column_name = 'drop_reference') THEN
CREATE UNIQUE INDEX IF NOT EXISTS shop_and_drop_drop_reference_uniq ON retail.shop_and_drop (drop_reference);
END IF; END $$;

DO $$ BEGIN IF to_regclass('retail.shop_and_drop') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'retail' AND table_name = 'shop_and_drop' AND column_name = 'order_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS shop_and_drop_order_id_uniq ON retail.shop_and_drop (order_id) WHERE order_id IS NOT NULL;
END IF; END $$;

DO $$ BEGIN IF to_regclass('retail.shop_and_drop') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'retail' AND table_name = 'shop_and_drop' AND column_name = 'sale_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS shop_and_drop_sale_id_uniq ON retail.shop_and_drop (sale_id) WHERE sale_id IS NOT NULL;
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.rule') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'rule' AND column_name = 'code') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'rule' AND column_name = 'matrix_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS rule_matrix_id_code_uniq ON approvals.rule (matrix_id, lower(code));
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.alternative_code') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'alternative_code' AND column_name = 'code') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'alternative_code' AND column_name = 'partner_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS alternative_code_partner_id_code_uniq ON catalogue.alternative_code (partner_id, lower(code));
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.group_package') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'group_package' AND column_name = 'product_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS group_package_product_id_uniq ON catalogue.group_package (product_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.product_eligibility_rule') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'product_eligibility_rule' AND column_name = 'product_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS product_eligibility_rule_product_id_uniq ON catalogue.product_eligibility_rule (product_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.published_bundle') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'published_bundle' AND column_name = 'venue_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'published_bundle' AND column_name = 'version') THEN
CREATE UNIQUE INDEX IF NOT EXISTS published_bundle_venue_id_version_uniq ON catalogue.published_bundle (venue_id, version);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.redirect_host') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'redirect_host' AND column_name = 'domain_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS redirect_host_domain_id_uniq ON identity.redirect_host (domain_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('retail.merchandise') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'retail' AND table_name = 'merchandise' AND column_name = 'barcode') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'retail' AND table_name = 'merchandise' AND column_name = 'outlet_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS merchandise_outlet_id_barcode_uniq ON retail.merchandise (outlet_id, barcode);
END IF; END $$;

DO $$ BEGIN IF to_regclass('retail.merchandise') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'retail' AND table_name = 'merchandise' AND column_name = 'outlet_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'retail' AND table_name = 'merchandise' AND column_name = 'sku') THEN
CREATE UNIQUE INDEX IF NOT EXISTS merchandise_outlet_id_sku_uniq ON retail.merchandise (outlet_id, lower(sku));
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.accessible') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'accessible' AND column_name = 'seat_map_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS accessible_seat_map_id_uniq ON seating.accessible (seat_map_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.recommendation_rule') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'recommendation_rule' AND column_name = 'performance_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'recommendation_rule' AND column_name = 'seat_map_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS recommendation_rule_seat_map_id_performance_id_uniq ON seating.recommendation_rule (seat_map_id, performance_id) NULLS NOT DISTINCT;
END IF; END $$;

DO $$ BEGIN IF to_regclass('whitelabel.ui_string_pack') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'whitelabel' AND table_name = 'ui_string_pack' AND column_name = 'language') THEN
CREATE UNIQUE INDEX IF NOT EXISTS ui_string_pack_language_uniq ON whitelabel.ui_string_pack (lower(language));
END IF; END $$;

DO $$ BEGIN IF to_regclass('whitelabel.app_build') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'whitelabel' AND table_name = 'app_build' AND column_name = 'platform') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'whitelabel' AND table_name = 'app_build' AND column_name = 'status') THEN
CREATE UNIQUE INDEX IF NOT EXISTS app_build_platform_uniq ON whitelabel.app_build (lower(platform)) WHERE status IN ('queued', 'building');
END IF; END $$;

DO $$ BEGIN IF to_regclass('whitelabel.custom_domain') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'whitelabel' AND table_name = 'custom_domain' AND column_name = 'hostname') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'whitelabel' AND table_name = 'custom_domain' AND column_name = 'status') THEN
CREATE UNIQUE INDEX IF NOT EXISTS custom_domain_hostname_uniq ON whitelabel.custom_domain (lower(hostname)) WHERE status IS DISTINCT FROM 'revoked';
END IF; END $$;

DO $$ BEGIN IF to_regclass('whitelabel.custom_domain') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'whitelabel' AND table_name = 'custom_domain' AND column_name = 'is_primary') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'whitelabel' AND table_name = 'custom_domain' AND column_name = 'kind') THEN
CREATE UNIQUE INDEX IF NOT EXISTS custom_domain_kind_uniq ON whitelabel.custom_domain (lower(kind)) WHERE is_primary;
END IF; END $$;

DO $$ BEGIN IF to_regclass('whitelabel.ui_string_pack') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'whitelabel' AND table_name = 'ui_string_pack' AND column_name = 'scope_path') THEN
CREATE INDEX IF NOT EXISTS ui_string_pack_scope_path_idx ON whitelabel.ui_string_pack USING gist (scope_path);
END IF; END $$;

CREATE OR REPLACE FUNCTION platform.apply_append_audit_read_rls(target regclass, read_check text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    base text := (SELECT left(c.relname, 55) FROM pg_class c WHERE c.oid = target);
BEGIN
    PERFORM platform.apply_append_audit_rls(target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', base || '_read', target);
    EXECUTE format('CREATE POLICY %I ON %s FOR SELECT USING (%s)', base || '_read', target, read_check);
END
$$;

DO $$ BEGIN IF to_regclass('whitelabel.ui_string_pack') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'whitelabel' AND table_name = 'ui_string_pack' AND column_name = 'scope_path') THEN
PERFORM platform.apply_scope_rls('whitelabel.ui_string_pack'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.configuration_profile') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'configuration_profile' AND column_name = 'scope_path') THEN
PERFORM platform.drop_rls_policies('platform.configuration_profile'::regclass);
PERFORM platform.apply_read_beneath_rls('platform.configuration_profile'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('tenancy.device_firmware') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'tenancy' AND table_name = 'device_firmware' AND column_name = 'scope_path') THEN
PERFORM platform.drop_rls_policies('tenancy.device_firmware'::regclass);
PERFORM platform.apply_read_beneath_rls('tenancy.device_firmware'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.request_approver') IS NOT NULL AND to_regclass('approvals.request') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'request' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'request_approver' AND column_name = 'request_id') THEN
PERFORM platform.apply_parent_rls('approvals.request_approver'::regclass, 'request_id', 'approvals.request'::regclass, 'id');
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.product_version') IS NOT NULL AND to_regclass('catalogue.product') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'product' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'product_version' AND column_name = 'product_id') THEN
PERFORM platform.drop_rls_policies('catalogue.product_version'::regclass);
PERFORM platform.apply_parent_rls('catalogue.product_version'::regclass, 'product_id', 'catalogue.product'::regclass, 'id');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.refund_line') IS NOT NULL AND to_regclass('orders.refund') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'refund' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'refund_line' AND column_name = 'refund_id') THEN
PERFORM platform.apply_parent_split_rls('orders.refund_line'::regclass, 'refund_id', 'orders.refund'::regclass, 'id', 'EXISTS (SELECT 1 FROM orders.sales_order p1 WHERE p1.id = parent_row.order_id AND ((p1.scope_path IS NOT NULL AND p1.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.refund_payment') IS NOT NULL AND to_regclass('orders.refund') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'refund' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'refund_payment' AND column_name = 'refund_id') THEN
PERFORM platform.apply_parent_split_rls('orders.refund_payment'::regclass, 'refund_id', 'orders.refund'::regclass, 'id', 'EXISTS (SELECT 1 FROM orders.sales_order p1 WHERE p1.id = parent_row.order_id AND ((p1.scope_path IS NOT NULL AND p1.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.refresh_token') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'refresh_token' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('identity.refresh_token'::regclass);
PERFORM platform.apply_subject_rls('identity.refresh_token'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.subject_data_export') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'subject_data_export' AND column_name = 'subject_id') THEN
PERFORM platform.apply_subject_rls('identity.subject_data_export'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.redirect_host') IS NOT NULL THEN
PERFORM platform.apply_tenant_rls('identity.redirect_host'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.audit_read') IS NOT NULL AND to_regclass('platform.scope') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'audit_read' AND column_name = 'org_unit_id') THEN
PERFORM platform.drop_rls_policies('platform.audit_read'::regclass);
PERFORM platform.apply_append_audit_read_rls('platform.audit_read'::regclass, 'platform.tenant_root_in_scope() OR (org_unit_id IS NOT NULL AND EXISTS (SELECT 1 FROM platform.scope au WHERE au.id = org_unit_id AND platform.in_scope(au.path)))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.audit_record') IS NOT NULL AND to_regclass('platform.scope') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'audit_record' AND column_name = 'org_unit_id') THEN
PERFORM platform.drop_rls_policies('platform.audit_record'::regclass);
PERFORM platform.apply_append_audit_read_rls('platform.audit_record'::regclass, 'platform.tenant_root_in_scope() OR (org_unit_id IS NOT NULL AND EXISTS (SELECT 1 FROM platform.scope au WHERE au.id = org_unit_id AND platform.in_scope(au.path)))');
END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'commerce') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'access') THEN GRANT USAGE ON SCHEMA access TO commerce; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'commerce') AND to_regclass('access.media_encoding_profile') IS NOT NULL THEN GRANT SELECT ON access.media_encoding_profile TO commerce; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'access') AND to_regclass('platform.workstation') IS NOT NULL THEN GRANT SELECT ON platform.workstation TO access; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'access') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'catalogue') THEN GRANT USAGE ON SCHEMA catalogue TO access; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'access') AND to_regclass('catalogue.entitlement_template') IS NOT NULL THEN GRANT SELECT ON catalogue.entitlement_template TO access; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('platform.venue_settings') IS NOT NULL THEN GRANT SELECT ON platform.venue_settings TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('platform.region_settings') IS NOT NULL THEN GRANT SELECT ON platform.region_settings TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('platform.outlet') IS NOT NULL THEN GRANT SELECT ON platform.outlet TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'commerce') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'assets') THEN GRANT USAGE ON SCHEMA assets TO commerce; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'commerce') AND to_regclass('assets.media_asset') IS NOT NULL THEN GRANT SELECT ON assets.media_asset TO commerce; END IF; END $$;

CREATE OR REPLACE FUNCTION identity.end_principal_sessions(target_principal_id uuid, ended_by uuid, reason text)
    RETURNS integer
    LANGUAGE plpgsql
    VOLATILE
    SECURITY DEFINER
    SET search_path = pg_catalog, public, pg_temp
AS $$
DECLARE
    caller_paths text := current_setting('ticvai.scope_paths', true);
    root_path text;
    ended integer := 0;
BEGIN
    IF NOT (platform.tenant_root_in_scope() OR EXISTS (
            SELECT 1 FROM identity.principal hp JOIN platform.scope hs ON hs.id = hp.home_scope_id
             WHERE hp.id = target_principal_id AND platform.in_scope(hs.path))) THEN
        RAISE EXCEPTION 'identity.end_principal_sessions: the caller may not update principal %', target_principal_id
            USING ERRCODE = '42501';
    END IF;
    SELECT s.path::text INTO root_path FROM platform.scope s WHERE s.level = 'tenant' LIMIT 1;
    PERFORM set_config('ticvai.scope_paths', COALESCE(root_path, ''), true);
    UPDATE identity.session
       SET status = 'terminated', ended_at = now(), ended_by_principal_id = ended_by, end_reason = left(reason, 500)
     WHERE principal_id = target_principal_id AND status = 'active';
    GET DIAGNOSTICS ended = ROW_COUNT;
    UPDATE identity.refresh_token
       SET revoked_at = now(), revocation_reason = left(reason, 250)
     WHERE principal_id = target_principal_id AND revoked_at IS NULL;
    PERFORM set_config('ticvai.scope_paths', COALESCE(caller_paths, ''), true);
    RETURN ended;
END
$$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0116', 'after r1 (9cec72d): 6 table(s), 44 column(s), 31 index(es), 41 other statement(s), 6 row-level security polic(ies) re-applied', 'eee82fe8cc85226d3d8720df0a7f81dfd15c5dec5f59e97d65864e4e98f146e2')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- REVOKE SELECT ON assets.media_asset FROM commerce;
-- REVOKE USAGE ON SCHEMA assets FROM commerce;
-- REVOKE SELECT ON platform.outlet FROM operations;
-- REVOKE SELECT ON platform.region_settings FROM operations;
-- REVOKE SELECT ON platform.venue_settings FROM operations;
-- REVOKE SELECT ON catalogue.entitlement_template FROM access;
-- REVOKE USAGE ON SCHEMA catalogue FROM access;
-- REVOKE SELECT ON platform.workstation FROM access;
-- REVOKE SELECT ON access.media_encoding_profile FROM commerce;
-- REVOKE USAGE ON SCHEMA access FROM commerce;
-- SELECT platform.drop_rls_policies('platform.audit_record'::regclass); SELECT platform.apply_tenant_rls('platform.audit_record'::regclass); SELECT platform.apply_append_audit_rls('platform.audit_record'::regclass);
-- SELECT platform.drop_rls_policies('platform.audit_read'::regclass); SELECT platform.apply_subject_rls('platform.audit_read'::regclass); SELECT platform.apply_append_audit_rls('platform.audit_read'::regclass);
-- SELECT platform.drop_rls_policies('identity.refresh_token'::regclass); SELECT platform.apply_tenant_rls('identity.refresh_token'::regclass);
-- SELECT platform.drop_rls_policies('catalogue.product_version'::regclass); SELECT platform.apply_tenant_rls('catalogue.product_version'::regclass);
-- SELECT platform.drop_rls_policies('tenancy.device_firmware'::regclass); SELECT platform.apply_scope_rls('tenancy.device_firmware'::regclass);
-- SELECT platform.drop_rls_policies('platform.configuration_profile'::regclass); SELECT platform.apply_scope_rls('platform.configuration_profile'::regclass);
-- DROP INDEX IF EXISTS whitelabel.ui_string_pack_scope_path_idx;
-- DROP INDEX IF EXISTS whitelabel.custom_domain_kind_uniq;
-- DROP INDEX IF EXISTS whitelabel.custom_domain_hostname_uniq;
-- DROP INDEX IF EXISTS whitelabel.app_build_platform_uniq;
-- DROP INDEX IF EXISTS whitelabel.ui_string_pack_language_uniq;
-- DROP INDEX IF EXISTS seating.recommendation_rule_seat_map_id_performance_id_uniq;
-- DROP INDEX IF EXISTS seating.accessible_seat_map_id_uniq;
-- DROP INDEX IF EXISTS retail.merchandise_outlet_id_sku_uniq;
-- DROP INDEX IF EXISTS retail.merchandise_outlet_id_barcode_uniq;
-- DROP INDEX IF EXISTS identity.redirect_host_domain_id_uniq;
-- DROP INDEX IF EXISTS catalogue.published_bundle_venue_id_version_uniq;
-- DROP INDEX IF EXISTS catalogue.product_eligibility_rule_product_id_uniq;
-- DROP INDEX IF EXISTS catalogue.group_package_product_id_uniq;
-- DROP INDEX IF EXISTS catalogue.alternative_code_partner_id_code_uniq;
-- DROP INDEX IF EXISTS approvals.rule_matrix_id_code_uniq;
-- DROP INDEX IF EXISTS retail.shop_and_drop_sale_id_uniq;
-- DROP INDEX IF EXISTS retail.shop_and_drop_order_id_uniq;
-- DROP INDEX IF EXISTS retail.shop_and_drop_drop_reference_uniq;
-- DROP INDEX IF EXISTS orders.payment_link_token_uniq;
-- DROP INDEX IF EXISTS platform.audit_read_org_unit_id_idx;
-- DROP INDEX IF EXISTS orders.refund_payment_refund_id_idx;
-- DROP INDEX IF EXISTS orders.refund_payment_payment_id_idx;
-- DROP INDEX IF EXISTS orders.refund_line_refund_id_idx;
-- DROP INDEX IF EXISTS orders.refund_line_order_line_id_idx;
-- DROP INDEX IF EXISTS identity.subject_data_export_subject_id_idx;
-- DROP INDEX IF EXISTS identity.refresh_token_subject_id_idx;
-- DROP INDEX IF EXISTS identity.delegated_access_revoked_by_subject_id_idx;
-- DROP INDEX IF EXISTS approvals.request_approver_request_id_idx;
-- DROP INDEX IF EXISTS approvals.request_approver_principal_id_idx;
-- DROP INDEX IF EXISTS approvals.request_requested_by_subject_id_idx;
-- DROP INDEX IF EXISTS access.entitlement_venue_id_change_version_idx;
-- DROP TRIGGER IF EXISTS entitlement_change_version_trg ON access.entitlement; DROP FUNCTION IF EXISTS access.entitlement_change_version_set(); DROP SEQUENCE IF EXISTS access.entitlement_change_version_seq;
-- ALTER TABLE platform.audit_read DROP CONSTRAINT IF EXISTS audit_read_org_unit_id_fkey;
-- ALTER TABLE identity.refresh_token DROP CONSTRAINT IF EXISTS refresh_token_subject_id_fkey;
-- ALTER TABLE identity.delegated_access DROP CONSTRAINT IF EXISTS delegated_access_revoked_by_subject_id_fkey;
-- ALTER TABLE approvals.request DROP CONSTRAINT IF EXISTS request_requested_by_subject_id_fkey;
-- DROP TABLE IF EXISTS whitelabel.ui_string_pack;
-- ALTER TABLE whitelabel.site_package DROP COLUMN IF EXISTS package_asset_ref;
-- ALTER TABLE whitelabel.custom_domain DROP COLUMN IF EXISTS validation_expires_at;
-- ALTER TABLE venuemap.import_job DROP COLUMN IF EXISTS created_at;
-- ALTER TABLE venuemap.import_job DROP COLUMN IF EXISTS format;
-- ALTER TABLE venuemap.import_job DROP COLUMN IF EXISTS source_ref;
-- ALTER TABLE tenancy.device_telemetry DROP COLUMN IF EXISTS error_count;
-- ALTER TABLE tenancy.device_telemetry DROP COLUMN IF EXISTS sync_backlog;
-- ALTER TABLE retail.shop_and_drop DROP COLUMN IF EXISTS collection_note;
-- ALTER TABLE retail.shop_and_drop DROP CONSTRAINT IF EXISTS shop_and_drop_drop_reference_chk;
-- ALTER TABLE retail.merchandise DROP COLUMN IF EXISTS is_published;
-- ALTER TABLE reporting.report_definition DROP CONSTRAINT IF EXISTS report_definition_required_permission_chk; ALTER TABLE reporting.report_definition ADD CONSTRAINT report_definition_required_permission_chk CHECK (required_permission IN ('SESSION_FORCE_LOGOUT', 'USER_MANAGE', 'ROLE_MANAGE', 'PERMISSION_GRANT', 'PERMISSION_VIEW', 'PERMISSION_MANAGE', 'PLATFORM_TENANT_VIEW', 'PLATFORM_TENANT_MANAGE', 'PLATFORM_TENANT_TERMINATE', 'PLATFORM_PLAN_MANAGE', 'PLATFORM_CELL_VIEW', 'PLATFORM_CELL_MANAGE', 'PLATFORM_BILLING_VIEW', 'PLATFORM_AI_MANAGE', 'PLATFORM_BILLING_MANAGE', 'PLATFORM_RELEASE_VIEW', 'PLATFORM_RELEASE_MANAGE', 'PLATFORM_RELEASE_PROMOTE', 'PLATFORM_MIGRATION_VIEW', 'PLATFORM_MIGRATION_APPLY', 'PLATFORM_TENANT_ACCESS', 'TENANT_CONFIGURE', 'TENANT_VIEW', 'TENANT_PUBLISH', 'SCOPE_VIEW', 'SCOPE_MANAGE', 'REGION_CONFIGURE', 'WORKSTATION_CONFIGURE', 'PRODUCT_VIEW', 'PRODUCT_CONFIGURE', 'PRODUCT_APPROVE', 'PRODUCT_PUBLISH', 'PRICE_VIEW', 'PRICE_CONFIGURE', 'EVENT_CONFIGURE', 'PERFORMANCE_CONFIGURE', 'CAPACITY_CONFIGURE', 'ORDER_VIEW', 'ORDER_VIEW_OTHER', 'ORDER_CREATE', 'ORDER_MODIFY', 'ORDER_DISCOUNT', 'ORDER_CANCEL', 'ORDER_VOID', 'ORDER_REFUND', 'ORDER_REFUND_APPROVE', 'ORDER_REFUND_BULK', 'ORDER_EXCHANGE', 'ORDER_RESCHEDULE', 'ORDER_REPRINT', 'PRICE_OVERRIDE', 'DISCOUNT_APPLY', 'CREDIT_MANAGE', 'CREDIT_OVERRIDE', 'WALLET_VIEW', 'WALLET_OPERATE', 'WALLET_CONFIGURE', 'PAYMENT_VIEW', 'PAYMENT_CONFIGURE', 'PAYMENT_PROVIDER_MANAGE', 'PAYMENT_DISPUTE', 'SHIFT_OPEN', 'SHIFT_CLOSE', 'SHIFT_SUSPEND', 'SHIFT_CLOSE_OTHER', 'SHIFT_APPROVE_OPEN', 'SHIFT_APPROVE_CLOSE', 'SHIFT_REOPEN', 'CASH_LIFT', 'CASH_ADD', 'CASH_NO_SALE', 'DEPOSIT_BOX_MODIFY_OWN', 'DEPOSIT_BOX_MODIFY_OTHER', 'OVERSHORT_ACCEPT', 'ACCESS_VALIDATE', 'ACCESS_OVERRIDE', 'ACCESS_POINT_CONFIGURE', 'TURNSTILE_MODE_SET', 'TICKET_LOOKUP', 'ACCREDITATION_VIEW', 'ACCREDITATION_APPLY', 'ACCREDITATION_APPROVE', 'ACCREDITATION_ISSUE', 'ACCREDITATION_MANAGE', 'ACCREDITATION_CONFIGURE', 'REPORT_VIEW_OWN', 'REPORT_VIEW_WORKSTATION', 'REPORT_VIEW_VENUE', 'REPORT_VIEW_REGION', 'REPORT_VIEW_TENANT', 'REPORT_EXPORT', 'REPORT_EXPORT_PII', 'REPORT_MANAGE', 'REPORT_SCHEDULE', 'LEDGER_VIEW', 'LEDGER_POST', 'LEDGER_APPROVE', 'TAX_CONFIGURE', 'ACCOUNT_CONFIGURE', 'SETTLEMENT_VIEW', 'SETTLEMENT_RECONCILE', 'GUEST_VIEW', 'GUEST_VIEW_PII', 'GUEST_MANAGE', 'VENUE_MAP_VIEW', 'VENUE_MAP_MANAGE', 'VENUE_MAP_PUBLISH', 'RESOURCE_VIEW', 'RESOURCE_BOOK', 'RESOURCE_MANAGE', 'RESOURCE_CONFIGURE', 'RENTAL_VIEW', 'RENTAL_BOOK', 'RENTAL_OPERATE', 'RENTAL_MANAGE', 'RENTAL_CONFIGURE', 'RENTAL_PRICE', 'RENTAL_APPROVE', 'RENTAL_OVERRIDE', 'DEVELOPER_VIEW', 'DEVELOPER_MANAGE', 'DEVELOPER_ADMIN', 'LOYALTY_ACCRUE', 'LOYALTY_REDEEM', 'LOYALTY_ADJUST', 'MEMBERSHIP_VIEW', 'MEMBERSHIP_MANAGE', 'MARKETING_VIEW', 'MARKETING_MANAGE', 'MARKETING_SEND', 'CASE_VIEW', 'CASE_MANAGE', 'ASSET_LIBRARY_VIEW', 'ASSET_LIBRARY_MANAGE', 'ASSET_LIBRARY_APPROVE', 'ASSET_LIBRARY_SHARE', 'QUEUE_VIEW', 'QUEUE_MANAGE', 'QUEUE_REDEEM', 'QUEUE_OVERRIDE', 'TRANSPORT_VIEW', 'TRANSPORT_MANAGE', 'TRANSPORT_PRICE', 'ASSET_VIEW', 'ASSET_MANAGE', 'WORK_ORDER_VIEW', 'WORK_ORDER_MANAGE', 'WORK_ORDER_VERIFY', 'INSPECTION_VIEW', 'INSPECTION_SUBMIT', 'INSPECTION_MANAGE', 'INCIDENT_REPORT', 'INCIDENT_VIEW', 'INCIDENT_MANAGE', 'KIOSK_ATTEND', 'DEVICE_VIEW', 'DEVICE_CONFIGURE', 'DEVICE_MANAGE', 'APPROVAL_ACT', 'APPROVAL_DELEGATE', 'AI_USE', 'AI_CONFIGURE', 'AI_APPROVE', 'AI_AUDIT_VIEW', 'RISK_REVIEW', 'RISK_INVESTIGATE', 'AUDIT_VIEW', 'APPROVAL_VIEW', 'APPROVAL_REQUEST', 'APPROVAL_DECIDE', 'APPROVAL_CONFIGURE', 'MAINTENANCE_EXECUTE', 'MAINTENANCE_APPROVE', 'WORKFORCE_VIEW', 'WORKFORCE_MANAGE', 'ATTENDANCE_RECORD', 'ANNOUNCEMENT_PUBLISH', 'ANNOUNCEMENT_EMERGENCY', 'PARTNER_VIEW', 'PARTNER_MANAGE', 'PARKING_CONFIGURE', 'PAYMENT_VOID', 'PROCUREMENT_VIEW', 'PROCUREMENT_REQUEST', 'PROCUREMENT_MANAGE', 'PROCUREMENT_RECEIVE', 'CORE_AI_PUBLISH', 'TICKETING_AI_PUBLISH', 'ACCESS_AI_PUBLISH', 'FNB_AI_PUBLISH', 'RETAIL_AI_PUBLISH', 'INVENTORY_AI_PUBLISH', 'SEATING_AI_PUBLISH', 'MEMBERSHIP_AI_PUBLISH', 'MARKETING_AI_PUBLISH', 'RESOURCES_AI_PUBLISH', 'QUEUE_AI_PUBLISH', 'TRANSPORT_AI_PUBLISH', 'GAMES_AI_PUBLISH', 'MAINTENANCE_AI_PUBLISH', 'ACCREDITATION_AI_PUBLISH', 'PARTNER_AI_PUBLISH', 'ANALYTICS_AI_PUBLISH', 'BIOMETRIC_IMAGE_VIEW', 'ACCESS_DIRECTION_SET', 'REPORT_GOVERNANCE_MANAGE')) NOT VALID;
-- ALTER TABLE promotions.promotion DROP COLUMN IF EXISTS venues;
-- ALTER TABLE promotions.promotion DROP COLUMN IF EXISTS label;
-- ALTER TABLE promotions.promotion DROP COLUMN IF EXISTS description_localised;
-- ALTER TABLE promotions.promotion DROP COLUMN IF EXISTS name_localised;
-- ALTER TABLE platform.venue_settings DROP COLUMN IF EXISTS step_minutes;
-- ALTER TABLE platform.audit_read DROP COLUMN IF EXISTS org_unit_id;
-- ALTER TABLE orders.stored_value_authorisation DROP COLUMN IF EXISTS wallet_hold_id;
-- ALTER TABLE orders.refund_policy_time_band DROP COLUMN IF EXISTS refund_type;
-- DROP TABLE IF EXISTS orders.refund_payment;
-- DROP TABLE IF EXISTS orders.refund_line;
-- ALTER TABLE orders.group_booking DROP COLUMN IF EXISTS version;
-- ALTER TABLE marketing.privacy_request DROP COLUMN IF EXISTS approval_request_id;
-- ALTER TABLE identity.subject_holding DROP COLUMN IF EXISTS verified_contact_ref;
-- ALTER TABLE identity.subject_holding DROP COLUMN IF EXISTS order_number;
-- DROP TABLE IF EXISTS identity.subject_data_export;
-- ALTER TABLE identity.session DROP CONSTRAINT IF EXISTS session_ended_at_null_chk;
-- ALTER TABLE identity.role_permission DROP CONSTRAINT IF EXISTS role_permission_permission_chk; ALTER TABLE identity.role_permission ADD CONSTRAINT role_permission_permission_chk CHECK (permission IN ('SESSION_FORCE_LOGOUT', 'USER_MANAGE', 'ROLE_MANAGE', 'PERMISSION_GRANT', 'PERMISSION_VIEW', 'PERMISSION_MANAGE', 'PLATFORM_TENANT_VIEW', 'PLATFORM_TENANT_MANAGE', 'PLATFORM_TENANT_TERMINATE', 'PLATFORM_PLAN_MANAGE', 'PLATFORM_CELL_VIEW', 'PLATFORM_CELL_MANAGE', 'PLATFORM_BILLING_VIEW', 'PLATFORM_AI_MANAGE', 'PLATFORM_BILLING_MANAGE', 'PLATFORM_RELEASE_VIEW', 'PLATFORM_RELEASE_MANAGE', 'PLATFORM_RELEASE_PROMOTE', 'PLATFORM_MIGRATION_VIEW', 'PLATFORM_MIGRATION_APPLY', 'PLATFORM_TENANT_ACCESS', 'TENANT_CONFIGURE', 'TENANT_VIEW', 'TENANT_PUBLISH', 'SCOPE_VIEW', 'SCOPE_MANAGE', 'REGION_CONFIGURE', 'WORKSTATION_CONFIGURE', 'PRODUCT_VIEW', 'PRODUCT_CONFIGURE', 'PRODUCT_APPROVE', 'PRODUCT_PUBLISH', 'PRICE_VIEW', 'PRICE_CONFIGURE', 'EVENT_CONFIGURE', 'PERFORMANCE_CONFIGURE', 'CAPACITY_CONFIGURE', 'ORDER_VIEW', 'ORDER_VIEW_OTHER', 'ORDER_CREATE', 'ORDER_MODIFY', 'ORDER_DISCOUNT', 'ORDER_CANCEL', 'ORDER_VOID', 'ORDER_REFUND', 'ORDER_REFUND_APPROVE', 'ORDER_REFUND_BULK', 'ORDER_EXCHANGE', 'ORDER_RESCHEDULE', 'ORDER_REPRINT', 'PRICE_OVERRIDE', 'DISCOUNT_APPLY', 'CREDIT_MANAGE', 'CREDIT_OVERRIDE', 'WALLET_VIEW', 'WALLET_OPERATE', 'WALLET_CONFIGURE', 'PAYMENT_VIEW', 'PAYMENT_CONFIGURE', 'PAYMENT_PROVIDER_MANAGE', 'PAYMENT_DISPUTE', 'SHIFT_OPEN', 'SHIFT_CLOSE', 'SHIFT_SUSPEND', 'SHIFT_CLOSE_OTHER', 'SHIFT_APPROVE_OPEN', 'SHIFT_APPROVE_CLOSE', 'SHIFT_REOPEN', 'CASH_LIFT', 'CASH_ADD', 'CASH_NO_SALE', 'DEPOSIT_BOX_MODIFY_OWN', 'DEPOSIT_BOX_MODIFY_OTHER', 'OVERSHORT_ACCEPT', 'ACCESS_VALIDATE', 'ACCESS_OVERRIDE', 'ACCESS_POINT_CONFIGURE', 'TURNSTILE_MODE_SET', 'TICKET_LOOKUP', 'ACCREDITATION_VIEW', 'ACCREDITATION_APPLY', 'ACCREDITATION_APPROVE', 'ACCREDITATION_ISSUE', 'ACCREDITATION_MANAGE', 'ACCREDITATION_CONFIGURE', 'REPORT_VIEW_OWN', 'REPORT_VIEW_WORKSTATION', 'REPORT_VIEW_VENUE', 'REPORT_VIEW_REGION', 'REPORT_VIEW_TENANT', 'REPORT_EXPORT', 'REPORT_EXPORT_PII', 'REPORT_MANAGE', 'REPORT_SCHEDULE', 'LEDGER_VIEW', 'LEDGER_POST', 'LEDGER_APPROVE', 'TAX_CONFIGURE', 'ACCOUNT_CONFIGURE', 'SETTLEMENT_VIEW', 'SETTLEMENT_RECONCILE', 'GUEST_VIEW', 'GUEST_VIEW_PII', 'GUEST_MANAGE', 'VENUE_MAP_VIEW', 'VENUE_MAP_MANAGE', 'VENUE_MAP_PUBLISH', 'RESOURCE_VIEW', 'RESOURCE_BOOK', 'RESOURCE_MANAGE', 'RESOURCE_CONFIGURE', 'RENTAL_VIEW', 'RENTAL_BOOK', 'RENTAL_OPERATE', 'RENTAL_MANAGE', 'RENTAL_CONFIGURE', 'RENTAL_PRICE', 'RENTAL_APPROVE', 'RENTAL_OVERRIDE', 'DEVELOPER_VIEW', 'DEVELOPER_MANAGE', 'DEVELOPER_ADMIN', 'LOYALTY_ACCRUE', 'LOYALTY_REDEEM', 'LOYALTY_ADJUST', 'MEMBERSHIP_VIEW', 'MEMBERSHIP_MANAGE', 'MARKETING_VIEW', 'MARKETING_MANAGE', 'MARKETING_SEND', 'CASE_VIEW', 'CASE_MANAGE', 'ASSET_LIBRARY_VIEW', 'ASSET_LIBRARY_MANAGE', 'ASSET_LIBRARY_APPROVE', 'ASSET_LIBRARY_SHARE', 'QUEUE_VIEW', 'QUEUE_MANAGE', 'QUEUE_REDEEM', 'QUEUE_OVERRIDE', 'TRANSPORT_VIEW', 'TRANSPORT_MANAGE', 'TRANSPORT_PRICE', 'ASSET_VIEW', 'ASSET_MANAGE', 'WORK_ORDER_VIEW', 'WORK_ORDER_MANAGE', 'WORK_ORDER_VERIFY', 'INSPECTION_VIEW', 'INSPECTION_SUBMIT', 'INSPECTION_MANAGE', 'INCIDENT_REPORT', 'INCIDENT_VIEW', 'INCIDENT_MANAGE', 'KIOSK_ATTEND', 'DEVICE_VIEW', 'DEVICE_CONFIGURE', 'DEVICE_MANAGE', 'APPROVAL_ACT', 'APPROVAL_DELEGATE', 'AI_USE', 'AI_CONFIGURE', 'AI_APPROVE', 'AI_AUDIT_VIEW', 'RISK_REVIEW', 'RISK_INVESTIGATE', 'AUDIT_VIEW', 'APPROVAL_VIEW', 'APPROVAL_REQUEST', 'APPROVAL_DECIDE', 'APPROVAL_CONFIGURE', 'MAINTENANCE_EXECUTE', 'MAINTENANCE_APPROVE', 'WORKFORCE_VIEW', 'WORKFORCE_MANAGE', 'ATTENDANCE_RECORD', 'ANNOUNCEMENT_PUBLISH', 'ANNOUNCEMENT_EMERGENCY', 'PARTNER_VIEW', 'PARTNER_MANAGE', 'PARKING_CONFIGURE', 'PAYMENT_VOID', 'PROCUREMENT_VIEW', 'PROCUREMENT_REQUEST', 'PROCUREMENT_MANAGE', 'PROCUREMENT_RECEIVE', 'CORE_AI_PUBLISH', 'TICKETING_AI_PUBLISH', 'ACCESS_AI_PUBLISH', 'FNB_AI_PUBLISH', 'RETAIL_AI_PUBLISH', 'INVENTORY_AI_PUBLISH', 'SEATING_AI_PUBLISH', 'MEMBERSHIP_AI_PUBLISH', 'MARKETING_AI_PUBLISH', 'RESOURCES_AI_PUBLISH', 'QUEUE_AI_PUBLISH', 'TRANSPORT_AI_PUBLISH', 'GAMES_AI_PUBLISH', 'MAINTENANCE_AI_PUBLISH', 'ACCREDITATION_AI_PUBLISH', 'PARTNER_AI_PUBLISH', 'ANALYTICS_AI_PUBLISH', 'BIOMETRIC_IMAGE_VIEW', 'ACCESS_DIRECTION_SET', 'REPORT_GOVERNANCE_MANAGE')) NOT VALID;
-- ALTER TABLE identity.refresh_token DROP CONSTRAINT IF EXISTS refresh_token_principal_id_subject_id_one_chk;
-- ALTER TABLE identity.refresh_token DROP COLUMN IF EXISTS subject_id;
-- ALTER TABLE identity.refresh_token ALTER COLUMN principal_id SET NOT NULL;
-- DROP TABLE IF EXISTS identity.redirect_host;
-- ALTER TABLE identity.delegated_access DROP CONSTRAINT IF EXISTS delegated_access_revoked_by_subject_id_when_chk;
-- ALTER TABLE identity.delegated_access DROP COLUMN IF EXISTS revoked_by_subject_id;
-- ALTER TABLE identity.delegated_access DROP COLUMN IF EXISTS revoked_by_kind;
-- ALTER TABLE identity.delegated_access DROP CONSTRAINT IF EXISTS delegated_access_delegation_kind_chk; ALTER TABLE identity.delegated_access ADD CONSTRAINT delegated_access_delegation_kind_chk CHECK (delegation_kind IN ('primaryHolder', 'familyMember', 'groupLeader', 'attendee', 'corporateAdmin', 'corporateMember', 'carer')) NOT VALID;
-- ALTER TABLE catalogue.variant DROP COLUMN IF EXISTS reference_price;
-- ALTER TABLE catalogue.published_bundle DROP COLUMN IF EXISTS note;
-- ALTER TABLE catalogue.product_version DROP COLUMN IF EXISTS snapshot;
-- ALTER TABLE catalogue.product DROP COLUMN IF EXISTS updated_at;
-- ALTER TABLE catalogue.product DROP COLUMN IF EXISTS created_at;
-- ALTER TABLE catalogue.product DROP COLUMN IF EXISTS add_on_product_ids;
-- ALTER TABLE catalogue.product DROP COLUMN IF EXISTS valid_to;
-- ALTER TABLE catalogue.event DROP COLUMN IF EXISTS scheduled_lifecycle_reason;
-- ALTER TABLE catalogue.event DROP COLUMN IF EXISTS scheduled_lifecycle_at;
-- ALTER TABLE catalogue.event DROP COLUMN IF EXISTS scheduled_lifecycle_state;
-- ALTER TABLE assets.media_asset DROP COLUMN IF EXISTS has_transparency;
-- ALTER TABLE approvals.rule DROP CONSTRAINT IF EXISTS rule_condition_chk;
-- DROP TABLE IF EXISTS approvals.request_approver;
-- ALTER TABLE approvals.request DROP CONSTRAINT IF EXISTS request_requested_by_principal_id_requested_by_sub_b31f1c6e_chk;
-- ALTER TABLE approvals.request DROP COLUMN IF EXISTS requested_by_subject_id;
-- ALTER TABLE approvals.request ALTER COLUMN requested_by_principal_id SET NOT NULL;
-- ALTER TABLE ai.proposed_action DROP COLUMN IF EXISTS map_id;
-- ALTER TABLE ai.proposed_action DROP COLUMN IF EXISTS distance_metres;
-- ALTER TABLE ai.proposed_action DROP COLUMN IF EXISTS reasoning;
-- ALTER TABLE ai.proposed_action DROP COLUMN IF EXISTS basis;
-- ALTER TABLE ai.proposed_action DROP COLUMN IF EXISTS confidence;
-- ALTER TABLE access.entitlement DROP COLUMN IF EXISTS rotation_secret_ciphertext;
-- ALTER TABLE access.entitlement DROP COLUMN IF EXISTS media_linked_at;
-- ALTER TABLE access.entitlement DROP COLUMN IF EXISTS change_version;
-- DELETE FROM platform.schema_version WHERE version = 'V0116';
