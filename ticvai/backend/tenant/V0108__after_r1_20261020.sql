-- V0108 -- tenant database, after r1 (9cec72d) (20261020).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 18 table(s), 87 column(s), 71 index(es), 91 other statement(s), 17 row-level security polic(ies) re-applied.

ALTER TABLE access.access_point ADD COLUMN IF NOT EXISTS access_area_id uuid;

ALTER TABLE access.gate_mode_change ADD COLUMN IF NOT EXISTS cancelled_by_principal_id uuid;

ALTER TABLE access.gate_mode_change ADD COLUMN IF NOT EXISTS cancelled_at timestamptz;

ALTER TABLE access.gate_mode_change ADD COLUMN IF NOT EXISTS cancel_reason text CONSTRAINT gate_mode_change_cancel_reason_chk CHECK (char_length(cancel_reason) <= 200);

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'ai' AND table_name = 'activity' AND column_name = 'principal_id' AND is_nullable = 'NO') THEN ALTER TABLE ai.activity ALTER COLUMN principal_id DROP NOT NULL; END IF; END $$;

ALTER TABLE ai.activity DROP CONSTRAINT IF EXISTS activity_principal_id_when_chk;

ALTER TABLE ai.activity ADD CONSTRAINT activity_principal_id_when_chk CHECK (audience IS DISTINCT FROM 'staff' OR principal_id IS NOT NULL) NOT VALID;

ALTER TABLE ai.activity VALIDATE CONSTRAINT activity_principal_id_when_chk;

ALTER TABLE ai.activity DROP CONSTRAINT IF EXISTS activity_subject_id_when_chk;

ALTER TABLE ai.activity ADD CONSTRAINT activity_subject_id_when_chk CHECK (audience IS DISTINCT FROM 'guest' OR subject_id IS NOT NULL) NOT VALID;

ALTER TABLE ai.activity VALIDATE CONSTRAINT activity_subject_id_when_chk;

ALTER TABLE ai.chunk_embedding ADD COLUMN IF NOT EXISTS subject_id uuid;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'ai' AND table_name = 'conversation' AND column_name = 'principal_id' AND is_nullable = 'NO') THEN ALTER TABLE ai.conversation ALTER COLUMN principal_id DROP NOT NULL; END IF; END $$;

ALTER TABLE ai.conversation ADD COLUMN IF NOT EXISTS subject_id uuid;

ALTER TABLE ai.conversation ADD COLUMN IF NOT EXISTS profile_key text;

ALTER TABLE ai.conversation DROP CONSTRAINT IF EXISTS conversation_module_chk;

ALTER TABLE ai.conversation ADD CONSTRAINT conversation_module_chk CHECK (module IN ('core', 'ticketing', 'access', 'fnb', 'retail', 'inventory', 'seating', 'membership', 'marketing', 'resources', 'queue', 'transport', 'games', 'maintenance', 'accreditation', 'partner', 'developerApi', 'analytics', 'ai', 'poweredByRemoval')) NOT VALID;

ALTER TABLE ai.conversation VALIDATE CONSTRAINT conversation_module_chk;

ALTER TABLE ai.conversation DROP CONSTRAINT IF EXISTS conversation_principal_id_subject_id_one_chk;

ALTER TABLE ai.conversation ADD CONSTRAINT conversation_principal_id_subject_id_one_chk CHECK (num_nonnulls(principal_id, subject_id) = 1) NOT VALID;

ALTER TABLE ai.conversation VALIDATE CONSTRAINT conversation_principal_id_subject_id_one_chk;

ALTER TABLE ai.decision_record ADD COLUMN IF NOT EXISTS hash_version integer DEFAULT 1;

ALTER TABLE ai.index_source ADD COLUMN IF NOT EXISTS kind text CONSTRAINT index_source_kind_chk CHECK (kind IN ('product', 'entitlement', 'knowledge', 'faq', 'report', 'media'));

CREATE TABLE IF NOT EXISTS ai.outbox (
    id                                uuid NOT NULL,
    event_id                          uuid NOT NULL,
    event_name                        text NOT NULL,
    event_version                     integer,
    tenant_id                         uuid NOT NULL,
    aggregate_type                    text NOT NULL,
    aggregate_id                      uuid NOT NULL,
    payload                           jsonb NOT NULL,
    scope_path                        ltree NOT NULL,
    sequence                          integer NOT NULL,
    occurred_at                       timestamptz NOT NULL,
    trace_id                          text CONSTRAINT outbox_trace_id_chk CHECK (char_length(trace_id) <= 64),
    published_at                      timestamptz,
    attempts                          integer DEFAULT 0,
    last_error                        text,
    created_at                        timestamptz NOT NULL,
    CONSTRAINT outbox_pkey PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

CREATE TABLE IF NOT EXISTS ai.outbox_sequence (
    aggregate_id                      uuid PRIMARY KEY NOT NULL,
    last_sequence                     bigint NOT NULL,
    scope_path                        ltree NOT NULL
);

ALTER TABLE ai.policy ADD COLUMN IF NOT EXISTS glossary_terms jsonb;

ALTER TABLE ai.proposed_action ADD COLUMN IF NOT EXISTS target_kind text CONSTRAINT proposed_action_target_kind_chk CHECK (target_kind IN ('contentBlock', 'productName', 'emailTemplate', 'messageTemplate'));

ALTER TABLE ai.proposed_action ADD COLUMN IF NOT EXISTS target_ref text CONSTRAINT proposed_action_target_ref_chk CHECK (char_length(target_ref) <= 200);

ALTER TABLE ai.proposed_action ADD COLUMN IF NOT EXISTS locale text CONSTRAINT proposed_action_locale_chk CHECK (char_length(locale) <= 20);

ALTER TABLE ai.proposed_action ADD COLUMN IF NOT EXISTS field_path text CONSTRAINT proposed_action_field_path_chk CHECK (char_length(field_path) <= 300);

ALTER TABLE ai.proposed_action ADD COLUMN IF NOT EXISTS draft_text text;

CREATE TABLE IF NOT EXISTS ai.translation_job (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    target_locale                     text NOT NULL CONSTRAINT translation_job_target_locale_chk CHECK (char_length(target_locale) <= 20),
    source_locale                     text CONSTRAINT translation_job_source_locale_chk CHECK (char_length(source_locale) <= 20),
    scope                             text NOT NULL CONSTRAINT translation_job_scope_chk CHECK (scope IN ('allGaps', 'contentBlocks', 'productNames', 'emailTemplates', 'messageTemplates')),
    status                            text NOT NULL CONSTRAINT translation_job_status_chk CHECK (status IN ('running', 'completed', 'failed')),
    failure_reason                    text CONSTRAINT translation_job_failure_reason_chk CHECK (char_length(failure_reason) <= 500),
    created_by_principal_id           uuid,
    created_at                        timestamptz NOT NULL,
    completed_at                      timestamptz
);

CREATE TABLE IF NOT EXISTS ai.vector_store (
    id                                uuid PRIMARY KEY NOT NULL,
    collection_name                   text NOT NULL CONSTRAINT vector_store_collection_name_chk CHECK (char_length(collection_name) <= 200),
    alias                             text NOT NULL CONSTRAINT vector_store_alias_chk CHECK (char_length(alias) <= 200),
    model                             text NOT NULL CONSTRAINT vector_store_model_chk CHECK (char_length(model) <= 200),
    is_alias_target                   boolean DEFAULT false,
    token_issued_at                   timestamptz,
    token_expires_at                  timestamptz,
    status                            text NOT NULL CONSTRAINT vector_store_status_chk CHECK (status IN ('provisioning', 'active', 'offboarding', 'deleted', 'failed')),
    failure_reason                    text CONSTRAINT vector_store_failure_reason_chk CHECK (char_length(failure_reason) <= 500),
    created_at                        timestamptz NOT NULL,
    deleted_at                        timestamptz
);

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'decision' AND column_name = 'principal_id' AND is_nullable = 'NO') THEN ALTER TABLE approvals.decision ALTER COLUMN principal_id DROP NOT NULL; END IF; END $$;

ALTER TABLE approvals.decision ADD COLUMN IF NOT EXISTS external_approver_ref text;

ALTER TABLE approvals.decision ADD COLUMN IF NOT EXISTS external_approver_name text CONSTRAINT decision_external_approver_name_chk CHECK (char_length(external_approver_name) <= 200);

ALTER TABLE approvals.decision DROP CONSTRAINT IF EXISTS decision_decision_chk;

ALTER TABLE approvals.decision ADD CONSTRAINT decision_decision_chk CHECK (decision IN ('approve', 'reject', 'return', 'requestInformation')) NOT VALID;

ALTER TABLE approvals.decision VALIDATE CONSTRAINT decision_decision_chk;

ALTER TABLE approvals.decision DROP CONSTRAINT IF EXISTS decision_principal_id_external_approver_ref_one_chk;

ALTER TABLE approvals.decision ADD CONSTRAINT decision_principal_id_external_approver_ref_one_chk CHECK (num_nonnulls(principal_id, external_approver_ref) = 1) NOT VALID;

ALTER TABLE approvals.decision VALIDATE CONSTRAINT decision_principal_id_external_approver_ref_one_chk;

ALTER TABLE approvals.external_dispatch ADD COLUMN IF NOT EXISTS requester_reference text;

ALTER TABLE approvals.request ADD COLUMN IF NOT EXISTS attributes jsonb;

ALTER TABLE approvals.request ADD COLUMN IF NOT EXISTS assignment_note text CONSTRAINT request_assignment_note_chk CHECK (char_length(assignment_note) <= 500);

ALTER TABLE approvals.request ADD COLUMN IF NOT EXISTS approval_matrix_id uuid;

ALTER TABLE approvals.request ADD COLUMN IF NOT EXISTS rule_id uuid;

ALTER TABLE approvals.request ADD COLUMN IF NOT EXISTS cancel_reason text CONSTRAINT request_cancel_reason_chk CHECK (char_length(cancel_reason) <= 500);

ALTER TABLE assets.asset_version ADD COLUMN IF NOT EXISTS storage_key text CONSTRAINT asset_version_storage_key_chk CHECK (char_length(storage_key) <= 500);

ALTER TABLE assets.asset_version ADD COLUMN IF NOT EXISTS content_type text CONSTRAINT asset_version_content_type_chk CHECK (char_length(content_type) <= 200);

CREATE TABLE IF NOT EXISTS assets.guest_upload (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    purpose                           text NOT NULL CONSTRAINT guest_upload_purpose_chk CHECK (purpose IN ('identityDocument', 'selfie')),
    content_type                      text CONSTRAINT guest_upload_content_type_chk CHECK (char_length(content_type) <= 100),
    size_bytes                        integer,
    storage_key                       text CONSTRAINT guest_upload_storage_key_chk CHECK (char_length(storage_key) <= 500),
    status                            text NOT NULL CONSTRAINT guest_upload_status_chk CHECK (status IN ('pending', 'uploaded', 'deleted')),
    created_at                        timestamptz NOT NULL,
    deleted_at                        timestamptz
);

ALTER TABLE assets.media_asset ADD COLUMN IF NOT EXISTS extracted_text text;

ALTER TABLE assets.media_asset ADD COLUMN IF NOT EXISTS released_by_principal_id uuid;

ALTER TABLE assets.media_asset ADD COLUMN IF NOT EXISTS released_at timestamptz;

ALTER TABLE assets.media_usage DROP CONSTRAINT IF EXISTS media_usage_surface_chk;

ALTER TABLE assets.media_usage ADD CONSTRAINT media_usage_surface_chk CHECK (surface IN ('tenantBranding', 'homepageBanner', 'promoBlock', 'contentPage', 'product', 'event', 'menuItem', 'merchandise', 'workOrder', 'incident', 'inspection', 'campaign', 'aiConfigSource', 'aiHistoryImport', 'aiLayoutDraft', 'workOrderAttachment', 'seatingSection', 'transportNetworkImport', 'venueMap', 'venueMapVersion')) NOT VALID;

ALTER TABLE assets.media_usage VALIDATE CONSTRAINT media_usage_surface_chk;

CREATE TABLE IF NOT EXISTS catalogue.bundle_application (
    id                                uuid PRIMARY KEY NOT NULL,
    workstation_id                    uuid NOT NULL,
    venue_id                          uuid NOT NULL,
    bundle_version                    text NOT NULL,
    applied_at                        timestamptz NOT NULL,
    outcome                           text NOT NULL CONSTRAINT bundle_application_outcome_chk CHECK (outcome IN ('applied', 'rolledBack', 'signatureInvalid')),
    error                             text CONSTRAINT bundle_application_error_chk CHECK (char_length(error) <= 2000)
);

ALTER TABLE catalogue.group_package ADD COLUMN IF NOT EXISTS minimum_size integer;

ALTER TABLE catalogue.group_package DROP CONSTRAINT IF EXISTS group_package_kind_chk;

ALTER TABLE catalogue.group_package ADD CONSTRAINT group_package_kind_chk CHECK (kind IN ('school', 'party', 'corporate', 'tourOperator', 'community')) NOT VALID;

ALTER TABLE catalogue.group_package VALIDATE CONSTRAINT group_package_kind_chk;

CREATE TABLE IF NOT EXISTS catalogue.product_channel_text (
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid NOT NULL,
    workstation_button_label          jsonb,
    receipt_name                      jsonb,
    partner_description               jsonb,
    web_description                   jsonb,
    kiosk_label                       jsonb,
    visit_instructions                jsonb,
    terms_and_conditions              jsonb,
    scope_path                        ltree NOT NULL
);

CREATE TABLE IF NOT EXISTS catalogue.product_owner_form (
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid,
    applies_to                        text NOT NULL CONSTRAINT product_owner_form_applies_to_chk CHECK (applies_to IN ('reservationOwner', 'ticketOwner')),
    form_id                           uuid NOT NULL,
    scope_path                        ltree NOT NULL
);

CREATE TABLE IF NOT EXISTS catalogue.product_sale_permission (
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid,
    level                             text NOT NULL CONSTRAINT product_sale_permission_level_chk CHECK (level IN ('global', 'venue', 'salesChannel', 'workstation', 'role', 'principal')),
    target_id                         uuid,
    effect                            text NOT NULL CONSTRAINT product_sale_permission_effect_chk CHECK (effect IN ('ALLOW', 'DENY')),
    note                              text CONSTRAINT product_sale_permission_note_chk CHECK (char_length(note) <= 200),
    scope_path                        ltree NOT NULL,
    CONSTRAINT product_sale_permission_target_id_when_chk CHECK (level IS NULL OR level NOT IN ('venue', 'salesChannel', 'workstation', 'role', 'principal') OR target_id IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS catalogue.product_tag (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT product_tag_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT product_tag_name_chk CHECK (char_length(name) <= 80),
    name_localised                    jsonb,
    description                       jsonb,
    display_order                     integer DEFAULT 100,
    is_active                         boolean DEFAULT true,
    scope_path                        ltree NOT NULL
);

ALTER TABLE catalogue.published_bundle ADD COLUMN IF NOT EXISTS published_at timestamptz;

ALTER TABLE catalogue.published_bundle ADD COLUMN IF NOT EXISTS published_by uuid;

ALTER TABLE fnb.delivery_location ADD COLUMN IF NOT EXISTS opens_at time;

ALTER TABLE fnb.delivery_location ADD COLUMN IF NOT EXISTS closes_at time;

ALTER TABLE identity.delegated_access ADD COLUMN IF NOT EXISTS granted_by_kind text DEFAULT 'principal' CONSTRAINT delegated_access_granted_by_kind_chk CHECK (granted_by_kind IN ('principal', 'subject', 'system'));

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'granted_by_principal_id' AND is_nullable = 'NO') THEN ALTER TABLE identity.delegated_access ALTER COLUMN granted_by_principal_id DROP NOT NULL; END IF; END $$;

ALTER TABLE identity.delegated_access ADD COLUMN IF NOT EXISTS granted_by_subject_id uuid;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'permission' AND is_nullable = 'NO') THEN ALTER TABLE identity.delegated_access ALTER COLUMN permission DROP NOT NULL; END IF; END $$;

ALTER TABLE identity.delegated_access DROP CONSTRAINT IF EXISTS delegated_access_granted_by_principal_id_when_chk;

ALTER TABLE identity.delegated_access ADD CONSTRAINT delegated_access_granted_by_principal_id_when_chk CHECK (granted_by_kind IS DISTINCT FROM 'principal' OR granted_by_principal_id IS NOT NULL) NOT VALID;

ALTER TABLE identity.delegated_access VALIDATE CONSTRAINT delegated_access_granted_by_principal_id_when_chk;

ALTER TABLE identity.delegated_access DROP CONSTRAINT IF EXISTS delegated_access_granted_by_subject_id_when_chk;

ALTER TABLE identity.delegated_access ADD CONSTRAINT delegated_access_granted_by_subject_id_when_chk CHECK (granted_by_kind IS DISTINCT FROM 'subject' OR granted_by_subject_id IS NOT NULL) NOT VALID;

ALTER TABLE identity.delegated_access VALIDATE CONSTRAINT delegated_access_granted_by_subject_id_when_chk;

ALTER TABLE identity.delegated_access DROP CONSTRAINT IF EXISTS delegated_access_permission_role_id_one_chk;

ALTER TABLE identity.delegated_access ADD CONSTRAINT delegated_access_permission_role_id_one_chk CHECK (num_nonnulls(permission, role_id) = 1) NOT VALID;

ALTER TABLE identity.delegated_access VALIDATE CONSTRAINT delegated_access_permission_role_id_one_chk;

ALTER TABLE identity.guest_identity_verification ADD COLUMN IF NOT EXISTS selfie_upload_id uuid;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'mfa_challenge' AND column_name = 'principal_id' AND is_nullable = 'NO') THEN ALTER TABLE identity.mfa_challenge ALTER COLUMN principal_id DROP NOT NULL; END IF; END $$;

ALTER TABLE identity.mfa_challenge ADD COLUMN IF NOT EXISTS subject_id uuid;

ALTER TABLE identity.mfa_challenge DROP CONSTRAINT IF EXISTS mfa_challenge_principal_id_subject_id_one_chk;

ALTER TABLE identity.mfa_challenge ADD CONSTRAINT mfa_challenge_principal_id_subject_id_one_chk CHECK (num_nonnulls(principal_id, subject_id) = 1) NOT VALID;

ALTER TABLE identity.mfa_challenge VALIDATE CONSTRAINT mfa_challenge_principal_id_subject_id_one_chk;

ALTER TABLE identity.mfa_method ADD COLUMN IF NOT EXISTS subject_id uuid;

ALTER TABLE identity.mfa_method ADD COLUMN IF NOT EXISTS secret text;

ALTER TABLE identity.mfa_method ADD COLUMN IF NOT EXISTS destination text;

ALTER TABLE identity.mfa_method ADD COLUMN IF NOT EXISTS pending_expires_at timestamptz;

ALTER TABLE identity.mfa_method DROP CONSTRAINT IF EXISTS mfa_method_principal_id_subject_id_one_chk;

ALTER TABLE identity.mfa_method ADD CONSTRAINT mfa_method_principal_id_subject_id_one_chk CHECK (num_nonnulls(principal_id, subject_id) = 1) NOT VALID;

ALTER TABLE identity.mfa_method VALIDATE CONSTRAINT mfa_method_principal_id_subject_id_one_chk;

ALTER TABLE identity.mfa_recovery_code ADD COLUMN IF NOT EXISTS subject_id uuid;

ALTER TABLE identity.mfa_recovery_code DROP CONSTRAINT IF EXISTS mfa_recovery_code_principal_id_subject_id_one_chk;

ALTER TABLE identity.mfa_recovery_code ADD CONSTRAINT mfa_recovery_code_principal_id_subject_id_one_chk CHECK (num_nonnulls(principal_id, subject_id) = 1) NOT VALID;

ALTER TABLE identity.mfa_recovery_code VALIDATE CONSTRAINT mfa_recovery_code_principal_id_subject_id_one_chk;

CREATE TABLE IF NOT EXISTS identity.open_shift_marker (
    shift_id                          uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid NOT NULL,
    workstation_id                    uuid NOT NULL,
    venue_id                          uuid,
    opened_at                         timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'otp_challenge' AND column_name = 'subject_id' AND is_nullable = 'NO') THEN ALTER TABLE identity.otp_challenge ALTER COLUMN subject_id DROP NOT NULL; END IF; END $$;

ALTER TABLE identity.password_policy ADD COLUMN IF NOT EXISTS access_token_minutes integer DEFAULT 15;

ALTER TABLE identity.password_policy ADD COLUMN IF NOT EXISTS refresh_token_hours integer DEFAULT 12;

ALTER TABLE identity.password_policy ADD COLUMN IF NOT EXISTS session_max_hours integer DEFAULT 12;

CREATE TABLE IF NOT EXISTS identity.principal_external_identity (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid NOT NULL,
    sso_provider_id                   uuid NOT NULL,
    external_subject                  text NOT NULL CONSTRAINT principal_external_identity_external_subject_chk CHECK (char_length(external_subject) <= 255),
    linked_at                         timestamptz NOT NULL
);

ALTER TABLE identity.role_permission DROP CONSTRAINT IF EXISTS role_permission_permission_chk;

ALTER TABLE identity.role_permission ADD CONSTRAINT role_permission_permission_chk CHECK (permission IN ('SESSION_FORCE_LOGOUT', 'USER_MANAGE', 'ROLE_MANAGE', 'PERMISSION_GRANT', 'PERMISSION_VIEW', 'PERMISSION_MANAGE', 'PLATFORM_TENANT_VIEW', 'PLATFORM_TENANT_MANAGE', 'PLATFORM_TENANT_TERMINATE', 'PLATFORM_PLAN_MANAGE', 'PLATFORM_CELL_VIEW', 'PLATFORM_CELL_MANAGE', 'PLATFORM_BILLING_VIEW', 'PLATFORM_AI_MANAGE', 'PLATFORM_BILLING_MANAGE', 'PLATFORM_RELEASE_VIEW', 'PLATFORM_RELEASE_MANAGE', 'PLATFORM_RELEASE_PROMOTE', 'PLATFORM_MIGRATION_VIEW', 'PLATFORM_MIGRATION_APPLY', 'PLATFORM_TENANT_ACCESS', 'TENANT_CONFIGURE', 'TENANT_VIEW', 'TENANT_PUBLISH', 'SCOPE_VIEW', 'SCOPE_MANAGE', 'REGION_CONFIGURE', 'WORKSTATION_CONFIGURE', 'PRODUCT_VIEW', 'PRODUCT_CONFIGURE', 'PRODUCT_APPROVE', 'PRODUCT_PUBLISH', 'PRICE_VIEW', 'PRICE_CONFIGURE', 'EVENT_CONFIGURE', 'PERFORMANCE_CONFIGURE', 'CAPACITY_CONFIGURE', 'ORDER_VIEW', 'ORDER_VIEW_OTHER', 'ORDER_CREATE', 'ORDER_MODIFY', 'ORDER_DISCOUNT', 'ORDER_CANCEL', 'ORDER_VOID', 'ORDER_REFUND', 'ORDER_REFUND_APPROVE', 'ORDER_REFUND_BULK', 'ORDER_EXCHANGE', 'ORDER_RESCHEDULE', 'ORDER_REPRINT', 'PRICE_OVERRIDE', 'DISCOUNT_APPLY', 'CREDIT_MANAGE', 'CREDIT_OVERRIDE', 'WALLET_VIEW', 'WALLET_OPERATE', 'WALLET_CONFIGURE', 'PAYMENT_VIEW', 'PAYMENT_CONFIGURE', 'PAYMENT_PROVIDER_MANAGE', 'PAYMENT_DISPUTE', 'SHIFT_OPEN', 'SHIFT_CLOSE', 'SHIFT_SUSPEND', 'SHIFT_CLOSE_OTHER', 'SHIFT_APPROVE_OPEN', 'SHIFT_APPROVE_CLOSE', 'SHIFT_REOPEN', 'CASH_LIFT', 'CASH_ADD', 'CASH_NO_SALE', 'DEPOSIT_BOX_MODIFY_OWN', 'DEPOSIT_BOX_MODIFY_OTHER', 'OVERSHORT_ACCEPT', 'ACCESS_VALIDATE', 'ACCESS_OVERRIDE', 'ACCESS_POINT_CONFIGURE', 'TURNSTILE_MODE_SET', 'TICKET_LOOKUP', 'ACCREDITATION_VIEW', 'ACCREDITATION_APPLY', 'ACCREDITATION_APPROVE', 'ACCREDITATION_ISSUE', 'ACCREDITATION_MANAGE', 'ACCREDITATION_CONFIGURE', 'REPORT_VIEW_OWN', 'REPORT_VIEW_WORKSTATION', 'REPORT_VIEW_VENUE', 'REPORT_VIEW_REGION', 'REPORT_VIEW_TENANT', 'REPORT_EXPORT', 'REPORT_EXPORT_PII', 'REPORT_MANAGE', 'REPORT_SCHEDULE', 'LEDGER_VIEW', 'LEDGER_POST', 'LEDGER_APPROVE', 'TAX_CONFIGURE', 'ACCOUNT_CONFIGURE', 'SETTLEMENT_VIEW', 'SETTLEMENT_RECONCILE', 'GUEST_VIEW', 'GUEST_VIEW_PII', 'GUEST_MANAGE', 'VENUE_MAP_VIEW', 'VENUE_MAP_MANAGE', 'VENUE_MAP_PUBLISH', 'RESOURCE_VIEW', 'RESOURCE_BOOK', 'RESOURCE_MANAGE', 'RESOURCE_CONFIGURE', 'RENTAL_VIEW', 'RENTAL_BOOK', 'RENTAL_OPERATE', 'RENTAL_MANAGE', 'RENTAL_CONFIGURE', 'RENTAL_PRICE', 'RENTAL_APPROVE', 'RENTAL_OVERRIDE', 'DEVELOPER_VIEW', 'DEVELOPER_MANAGE', 'DEVELOPER_ADMIN', 'LOYALTY_ACCRUE', 'LOYALTY_REDEEM', 'LOYALTY_ADJUST', 'MEMBERSHIP_VIEW', 'MEMBERSHIP_MANAGE', 'MARKETING_VIEW', 'MARKETING_MANAGE', 'MARKETING_SEND', 'CASE_VIEW', 'CASE_MANAGE', 'ASSET_LIBRARY_VIEW', 'ASSET_LIBRARY_MANAGE', 'ASSET_LIBRARY_APPROVE', 'ASSET_LIBRARY_SHARE', 'QUEUE_VIEW', 'QUEUE_MANAGE', 'QUEUE_REDEEM', 'QUEUE_OVERRIDE', 'TRANSPORT_VIEW', 'TRANSPORT_MANAGE', 'TRANSPORT_PRICE', 'ASSET_VIEW', 'ASSET_MANAGE', 'WORK_ORDER_VIEW', 'WORK_ORDER_MANAGE', 'WORK_ORDER_VERIFY', 'INSPECTION_VIEW', 'INSPECTION_SUBMIT', 'INSPECTION_MANAGE', 'INCIDENT_REPORT', 'INCIDENT_VIEW', 'INCIDENT_MANAGE', 'KIOSK_ATTEND', 'DEVICE_VIEW', 'DEVICE_CONFIGURE', 'DEVICE_MANAGE', 'APPROVAL_ACT', 'APPROVAL_DELEGATE', 'AI_USE', 'AI_CONFIGURE', 'AI_APPROVE', 'AI_AUDIT_VIEW', 'RISK_REVIEW', 'RISK_INVESTIGATE', 'AUDIT_VIEW', 'APPROVAL_VIEW', 'APPROVAL_REQUEST', 'APPROVAL_DECIDE', 'APPROVAL_CONFIGURE', 'MAINTENANCE_EXECUTE', 'MAINTENANCE_APPROVE', 'WORKFORCE_VIEW', 'WORKFORCE_MANAGE', 'ATTENDANCE_RECORD', 'ANNOUNCEMENT_PUBLISH', 'ANNOUNCEMENT_EMERGENCY', 'PARTNER_VIEW', 'PARTNER_MANAGE', 'PARKING_CONFIGURE', 'PAYMENT_VOID', 'PROCUREMENT_VIEW', 'PROCUREMENT_REQUEST', 'PROCUREMENT_MANAGE', 'PROCUREMENT_RECEIVE', 'CORE_AI_PUBLISH', 'TICKETING_AI_PUBLISH', 'ACCESS_AI_PUBLISH', 'FNB_AI_PUBLISH', 'RETAIL_AI_PUBLISH', 'INVENTORY_AI_PUBLISH', 'SEATING_AI_PUBLISH', 'MEMBERSHIP_AI_PUBLISH', 'MARKETING_AI_PUBLISH', 'RESOURCES_AI_PUBLISH', 'QUEUE_AI_PUBLISH', 'TRANSPORT_AI_PUBLISH', 'GAMES_AI_PUBLISH', 'MAINTENANCE_AI_PUBLISH', 'ACCREDITATION_AI_PUBLISH', 'PARTNER_AI_PUBLISH', 'ANALYTICS_AI_PUBLISH', 'BIOMETRIC_IMAGE_VIEW', 'ACCESS_DIRECTION_SET', 'REPORT_GOVERNANCE_MANAGE')) NOT VALID;

ALTER TABLE identity.role_permission VALIDATE CONSTRAINT role_permission_permission_chk;

ALTER TABLE identity.session ADD COLUMN IF NOT EXISTS ended_at timestamptz;

ALTER TABLE identity.session ADD COLUMN IF NOT EXISTS ended_by_principal_id uuid;

ALTER TABLE identity.session ADD COLUMN IF NOT EXISTS end_reason text CONSTRAINT session_end_reason_chk CHECK (char_length(end_reason) <= 500);

ALTER TABLE identity.session ADD COLUMN IF NOT EXISTS working_venue_id uuid;

ALTER TABLE identity.sso_provider ADD COLUMN IF NOT EXISTS username_claim text CONSTRAINT sso_provider_username_claim_chk CHECK (char_length(username_claim) <= 100);

ALTER TABLE identity.sso_provider ADD COLUMN IF NOT EXISTS display_name_claim text CONSTRAINT sso_provider_display_name_claim_chk CHECK (char_length(display_name_claim) <= 100);

ALTER TABLE identity.sso_provider ADD COLUMN IF NOT EXISTS groups_claim text CONSTRAINT sso_provider_groups_claim_chk CHECK (char_length(groups_claim) <= 100);

ALTER TABLE identity.sso_provider ADD COLUMN IF NOT EXISTS default_home_scope_id uuid;

ALTER TABLE identity.sso_provider ADD COLUMN IF NOT EXISTS allowed_redirect_uris text[];

ALTER TABLE ledger.account_mapping ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE ledger.journal_entry ADD COLUMN IF NOT EXISTS legal_entity_id uuid;

ALTER TABLE ledger.journal_entry DROP CONSTRAINT IF EXISTS journal_entry_source_chk;

ALTER TABLE ledger.journal_entry ADD CONSTRAINT journal_entry_source_chk CHECK (source IN ('manual', 'order', 'refund', 'void', 'shift', 'recognition', 'settlement', 'variance', 'reversal', 'writeOff', 'chargeback', 'payment')) NOT VALID;

ALTER TABLE ledger.journal_entry VALIDATE CONSTRAINT journal_entry_source_chk;

ALTER TABLE ledger.posting DROP CONSTRAINT IF EXISTS posting_source_chk;

ALTER TABLE ledger.posting ADD CONSTRAINT posting_source_chk CHECK (source IN ('manual', 'order', 'refund', 'void', 'shift', 'recognition', 'settlement', 'variance', 'reversal', 'writeOff', 'chargeback', 'payment')) NOT VALID;

ALTER TABLE ledger.posting VALIDATE CONSTRAINT posting_source_chk;

ALTER TABLE marketing.consent_purpose DROP CONSTRAINT IF EXISTS consent_purpose_purpose_chk;

ALTER TABLE marketing.consent_purpose ADD CONSTRAINT consent_purpose_purpose_chk CHECK (purpose IN ('marketing', 'personalisation', 'profiling', 'thirdPartySharing', 'aiProcessing', 'transactional', 'storedPaymentCredential', 'facePassEnrolment')) NOT VALID;

ALTER TABLE marketing.consent_purpose VALIDATE CONSTRAINT consent_purpose_purpose_chk;

ALTER TABLE marketing.consent_record DROP CONSTRAINT IF EXISTS consent_record_purpose_chk;

ALTER TABLE marketing.consent_record ADD CONSTRAINT consent_record_purpose_chk CHECK (purpose IN ('marketing', 'personalisation', 'profiling', 'thirdPartySharing', 'aiProcessing', 'transactional', 'storedPaymentCredential', 'facePassEnrolment')) NOT VALID;

ALTER TABLE marketing.consent_record VALIDATE CONSTRAINT consent_record_purpose_chk;

ALTER TABLE marketing.cookie_scan_policy DROP CONSTRAINT IF EXISTS cookie_scan_policy_frequency_chk;

ALTER TABLE marketing.cookie_scan_policy ADD CONSTRAINT cookie_scan_policy_frequency_chk CHECK (frequency IN ('daily', 'weekly', 'monthly', 'off')) NOT VALID;

ALTER TABLE marketing.customer_badge DROP CONSTRAINT IF EXISTS customer_badge_source_type_chk;

ALTER TABLE marketing.customer_badge ADD CONSTRAINT customer_badge_source_type_chk CHECK (source_type IN ('challenge', 'purchase', 'manager') AND char_length(source_type) <= 30) NOT VALID;

ALTER TABLE marketing.customer_badge DROP CONSTRAINT IF EXISTS customer_badge_status_chk;

ALTER TABLE marketing.customer_badge ADD CONSTRAINT customer_badge_status_chk CHECK (status IN ('awarded', 'expired', 'revoked') AND char_length(status) <= 20) NOT VALID;

ALTER TABLE marketing.form_definition_field ADD COLUMN IF NOT EXISTS presentation text;

CREATE TABLE IF NOT EXISTS marketing.form_submission_sale_link (
    id                                uuid PRIMARY KEY NOT NULL,
    submission_id                     uuid,
    order_id                          uuid NOT NULL,
    owner_role                        text NOT NULL CONSTRAINT form_submission_sale_link_owner_role_chk CHECK (owner_role IN ('reservationOwner', 'ticketOwner')),
    order_line_id                     uuid,
    unit_index                        integer,
    scope_path                        ltree NOT NULL,
    CONSTRAINT form_submission_sale_link_order_line_id_when_chk CHECK (owner_role IS DISTINCT FROM 'ticketOwner' OR order_line_id IS NOT NULL),
    CONSTRAINT form_submission_sale_link_unit_index_when_chk CHECK (owner_role IS DISTINCT FROM 'ticketOwner' OR unit_index IS NOT NULL)
);

ALTER TABLE marketing.guest_device DROP CONSTRAINT IF EXISTS guest_device_token_fingerprint_chk;

ALTER TABLE marketing.guest_device ADD CONSTRAINT guest_device_token_fingerprint_chk CHECK (char_length(token_fingerprint) <= 64) NOT VALID;

ALTER TABLE marketing.guest_device ADD COLUMN IF NOT EXISTS pending_session_end_installation_id uuid;

ALTER TABLE marketing.privacy_audit_event DROP CONSTRAINT IF EXISTS privacy_audit_event_source_chk;

ALTER TABLE marketing.privacy_audit_event ADD CONSTRAINT privacy_audit_event_source_chk CHECK (source IN ('core', 'ticketing', 'access', 'fnb', 'retail', 'inventory', 'seating', 'membership', 'marketing', 'resources', 'queue', 'transport', 'games', 'maintenance', 'accreditation', 'partner', 'developerApi', 'analytics', 'ai', 'poweredByRemoval')) NOT VALID;

ALTER TABLE marketing.privacy_audit_event VALIDATE CONSTRAINT privacy_audit_event_source_chk;

ALTER TABLE marketing.privacy_exception DROP CONSTRAINT IF EXISTS privacy_exception_system_chk;

ALTER TABLE marketing.privacy_exception ADD CONSTRAINT privacy_exception_system_chk CHECK (system IN ('core', 'ticketing', 'access', 'fnb', 'retail', 'inventory', 'seating', 'membership', 'marketing', 'resources', 'queue', 'transport', 'games', 'maintenance', 'accreditation', 'partner', 'developerApi', 'analytics', 'ai', 'poweredByRemoval')) NOT VALID;

ALTER TABLE marketing.privacy_exception VALIDATE CONSTRAINT privacy_exception_system_chk;

ALTER TABLE orders.cart ADD COLUMN IF NOT EXISTS session_id uuid;

ALTER TABLE orders.cart ADD COLUMN IF NOT EXISTS workstation_id uuid;

ALTER TABLE orders.group_booking ADD COLUMN IF NOT EXISTS performance_id uuid;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_event' AND column_name = 'order_id' AND is_nullable = 'NO') THEN ALTER TABLE orders.order_event ALTER COLUMN order_id DROP NOT NULL; END IF; END $$;

ALTER TABLE orders.order_event DROP CONSTRAINT IF EXISTS order_event_reservation_id_when_chk;

ALTER TABLE orders.order_event ADD CONSTRAINT order_event_reservation_id_when_chk CHECK (order_id IS NOT NULL OR reservation_id IS NOT NULL) NOT VALID;

ALTER TABLE orders.order_event VALIDATE CONSTRAINT order_event_reservation_id_when_chk;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'payments' AND table_name = 'currency_rule' AND column_name = 'payment_policy_id' AND is_nullable = 'NO') THEN ALTER TABLE payments.currency_rule ALTER COLUMN payment_policy_id DROP NOT NULL; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'payments' AND table_name = 'eligibility_rule' AND column_name = 'payment_policy_id' AND is_nullable = 'NO') THEN ALTER TABLE payments.eligibility_rule ALTER COLUMN payment_policy_id DROP NOT NULL; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'payments' AND table_name = 'fee_rule' AND column_name = 'payment_policy_id' AND is_nullable = 'NO') THEN ALTER TABLE payments.fee_rule ALTER COLUMN payment_policy_id DROP NOT NULL; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'payments' AND table_name = 'method_config' AND column_name = 'payment_policy_id' AND is_nullable = 'NO') THEN ALTER TABLE payments.method_config ALTER COLUMN payment_policy_id DROP NOT NULL; END IF; END $$;

ALTER TABLE payments.provider_connection ADD COLUMN IF NOT EXISTS provider_id uuid;

ALTER TABLE payments.provider_event ADD COLUMN IF NOT EXISTS provider_connection_id uuid;

ALTER TABLE payments.token ADD COLUMN IF NOT EXISTS revoked_at timestamptz;

CREATE TABLE IF NOT EXISTS pii.subject_identity (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    provider                          text NOT NULL CONSTRAINT subject_identity_provider_chk CHECK (provider IN ('apple', 'google', 'uaePass')),
    provider_subject                  text NOT NULL CONSTRAINT subject_identity_provider_subject_chk CHECK (char_length(provider_subject) <= 255),
    email_at_link                     text CONSTRAINT subject_identity_email_at_link_chk CHECK (char_length(email_at_link) <= 320),
    linked_at                         timestamptz NOT NULL
);

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'audit_read' AND column_name = 'subject_id' AND is_nullable = 'NO') THEN ALTER TABLE platform.audit_read ALTER COLUMN subject_id DROP NOT NULL; END IF; END $$;

ALTER TABLE platform.audit_read ADD COLUMN IF NOT EXISTS read_at timestamptz;

ALTER TABLE platform.audit_read ADD COLUMN IF NOT EXISTS target text CONSTRAINT audit_read_target_chk CHECK (target IN ('auditRecord', 'subject'));

ALTER TABLE platform.audit_read ADD COLUMN IF NOT EXISTS filter jsonb;

ALTER TABLE platform.audit_read ADD COLUMN IF NOT EXISTS record_count integer;

ALTER TABLE platform.dead_letter ADD COLUMN IF NOT EXISTS event_id uuid;

ALTER TABLE platform.dead_letter ADD COLUMN IF NOT EXISTS tenant_id uuid;

ALTER TABLE platform.dead_letter ADD COLUMN IF NOT EXISTS aggregate_type text;

ALTER TABLE platform.dead_letter ADD COLUMN IF NOT EXISTS aggregate_id uuid;

ALTER TABLE platform.dead_letter ADD COLUMN IF NOT EXISTS sequence integer;

ALTER TABLE platform.outbox ADD COLUMN IF NOT EXISTS occurred_at timestamptz;

CREATE TABLE IF NOT EXISTS platform.outbox_sequence (
    aggregate_id                      uuid PRIMARY KEY NOT NULL,
    last_sequence                     bigint NOT NULL,
    scope_path                        ltree NOT NULL
);

ALTER TABLE platform.venue_settings ADD COLUMN IF NOT EXISTS contact jsonb;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'workstation' AND column_name = 'sale_board' AND is_nullable = 'NO') THEN ALTER TABLE platform.workstation ALTER COLUMN sale_board DROP NOT NULL; END IF; END $$;

ALTER TABLE platform.workstation ADD COLUMN IF NOT EXISTS configuration_profile_version integer;

ALTER TABLE promotions.bundle ADD COLUMN IF NOT EXISTS variant_id uuid;

ALTER TABLE reporting.dashboard DROP CONSTRAINT IF EXISTS dashboard_module_chk;

ALTER TABLE reporting.dashboard ADD CONSTRAINT dashboard_module_chk CHECK (module IN ('core', 'ticketing', 'access', 'fnb', 'retail', 'inventory', 'seating', 'membership', 'marketing', 'resources', 'queue', 'transport', 'games', 'maintenance', 'accreditation', 'partner', 'developerApi', 'analytics', 'ai', 'poweredByRemoval')) NOT VALID;

ALTER TABLE reporting.dashboard VALIDATE CONSTRAINT dashboard_module_chk;

ALTER TABLE reporting.report_definition DROP CONSTRAINT IF EXISTS report_definition_required_permission_chk;

ALTER TABLE reporting.report_definition ADD CONSTRAINT report_definition_required_permission_chk CHECK (required_permission IN ('SESSION_FORCE_LOGOUT', 'USER_MANAGE', 'ROLE_MANAGE', 'PERMISSION_GRANT', 'PERMISSION_VIEW', 'PERMISSION_MANAGE', 'PLATFORM_TENANT_VIEW', 'PLATFORM_TENANT_MANAGE', 'PLATFORM_TENANT_TERMINATE', 'PLATFORM_PLAN_MANAGE', 'PLATFORM_CELL_VIEW', 'PLATFORM_CELL_MANAGE', 'PLATFORM_BILLING_VIEW', 'PLATFORM_AI_MANAGE', 'PLATFORM_BILLING_MANAGE', 'PLATFORM_RELEASE_VIEW', 'PLATFORM_RELEASE_MANAGE', 'PLATFORM_RELEASE_PROMOTE', 'PLATFORM_MIGRATION_VIEW', 'PLATFORM_MIGRATION_APPLY', 'PLATFORM_TENANT_ACCESS', 'TENANT_CONFIGURE', 'TENANT_VIEW', 'TENANT_PUBLISH', 'SCOPE_VIEW', 'SCOPE_MANAGE', 'REGION_CONFIGURE', 'WORKSTATION_CONFIGURE', 'PRODUCT_VIEW', 'PRODUCT_CONFIGURE', 'PRODUCT_APPROVE', 'PRODUCT_PUBLISH', 'PRICE_VIEW', 'PRICE_CONFIGURE', 'EVENT_CONFIGURE', 'PERFORMANCE_CONFIGURE', 'CAPACITY_CONFIGURE', 'ORDER_VIEW', 'ORDER_VIEW_OTHER', 'ORDER_CREATE', 'ORDER_MODIFY', 'ORDER_DISCOUNT', 'ORDER_CANCEL', 'ORDER_VOID', 'ORDER_REFUND', 'ORDER_REFUND_APPROVE', 'ORDER_REFUND_BULK', 'ORDER_EXCHANGE', 'ORDER_RESCHEDULE', 'ORDER_REPRINT', 'PRICE_OVERRIDE', 'DISCOUNT_APPLY', 'CREDIT_MANAGE', 'CREDIT_OVERRIDE', 'WALLET_VIEW', 'WALLET_OPERATE', 'WALLET_CONFIGURE', 'PAYMENT_VIEW', 'PAYMENT_CONFIGURE', 'PAYMENT_PROVIDER_MANAGE', 'PAYMENT_DISPUTE', 'SHIFT_OPEN', 'SHIFT_CLOSE', 'SHIFT_SUSPEND', 'SHIFT_CLOSE_OTHER', 'SHIFT_APPROVE_OPEN', 'SHIFT_APPROVE_CLOSE', 'SHIFT_REOPEN', 'CASH_LIFT', 'CASH_ADD', 'CASH_NO_SALE', 'DEPOSIT_BOX_MODIFY_OWN', 'DEPOSIT_BOX_MODIFY_OTHER', 'OVERSHORT_ACCEPT', 'ACCESS_VALIDATE', 'ACCESS_OVERRIDE', 'ACCESS_POINT_CONFIGURE', 'TURNSTILE_MODE_SET', 'TICKET_LOOKUP', 'ACCREDITATION_VIEW', 'ACCREDITATION_APPLY', 'ACCREDITATION_APPROVE', 'ACCREDITATION_ISSUE', 'ACCREDITATION_MANAGE', 'ACCREDITATION_CONFIGURE', 'REPORT_VIEW_OWN', 'REPORT_VIEW_WORKSTATION', 'REPORT_VIEW_VENUE', 'REPORT_VIEW_REGION', 'REPORT_VIEW_TENANT', 'REPORT_EXPORT', 'REPORT_EXPORT_PII', 'REPORT_MANAGE', 'REPORT_SCHEDULE', 'LEDGER_VIEW', 'LEDGER_POST', 'LEDGER_APPROVE', 'TAX_CONFIGURE', 'ACCOUNT_CONFIGURE', 'SETTLEMENT_VIEW', 'SETTLEMENT_RECONCILE', 'GUEST_VIEW', 'GUEST_VIEW_PII', 'GUEST_MANAGE', 'VENUE_MAP_VIEW', 'VENUE_MAP_MANAGE', 'VENUE_MAP_PUBLISH', 'RESOURCE_VIEW', 'RESOURCE_BOOK', 'RESOURCE_MANAGE', 'RESOURCE_CONFIGURE', 'RENTAL_VIEW', 'RENTAL_BOOK', 'RENTAL_OPERATE', 'RENTAL_MANAGE', 'RENTAL_CONFIGURE', 'RENTAL_PRICE', 'RENTAL_APPROVE', 'RENTAL_OVERRIDE', 'DEVELOPER_VIEW', 'DEVELOPER_MANAGE', 'DEVELOPER_ADMIN', 'LOYALTY_ACCRUE', 'LOYALTY_REDEEM', 'LOYALTY_ADJUST', 'MEMBERSHIP_VIEW', 'MEMBERSHIP_MANAGE', 'MARKETING_VIEW', 'MARKETING_MANAGE', 'MARKETING_SEND', 'CASE_VIEW', 'CASE_MANAGE', 'ASSET_LIBRARY_VIEW', 'ASSET_LIBRARY_MANAGE', 'ASSET_LIBRARY_APPROVE', 'ASSET_LIBRARY_SHARE', 'QUEUE_VIEW', 'QUEUE_MANAGE', 'QUEUE_REDEEM', 'QUEUE_OVERRIDE', 'TRANSPORT_VIEW', 'TRANSPORT_MANAGE', 'TRANSPORT_PRICE', 'ASSET_VIEW', 'ASSET_MANAGE', 'WORK_ORDER_VIEW', 'WORK_ORDER_MANAGE', 'WORK_ORDER_VERIFY', 'INSPECTION_VIEW', 'INSPECTION_SUBMIT', 'INSPECTION_MANAGE', 'INCIDENT_REPORT', 'INCIDENT_VIEW', 'INCIDENT_MANAGE', 'KIOSK_ATTEND', 'DEVICE_VIEW', 'DEVICE_CONFIGURE', 'DEVICE_MANAGE', 'APPROVAL_ACT', 'APPROVAL_DELEGATE', 'AI_USE', 'AI_CONFIGURE', 'AI_APPROVE', 'AI_AUDIT_VIEW', 'RISK_REVIEW', 'RISK_INVESTIGATE', 'AUDIT_VIEW', 'APPROVAL_VIEW', 'APPROVAL_REQUEST', 'APPROVAL_DECIDE', 'APPROVAL_CONFIGURE', 'MAINTENANCE_EXECUTE', 'MAINTENANCE_APPROVE', 'WORKFORCE_VIEW', 'WORKFORCE_MANAGE', 'ATTENDANCE_RECORD', 'ANNOUNCEMENT_PUBLISH', 'ANNOUNCEMENT_EMERGENCY', 'PARTNER_VIEW', 'PARTNER_MANAGE', 'PARKING_CONFIGURE', 'PAYMENT_VOID', 'PROCUREMENT_VIEW', 'PROCUREMENT_REQUEST', 'PROCUREMENT_MANAGE', 'PROCUREMENT_RECEIVE', 'CORE_AI_PUBLISH', 'TICKETING_AI_PUBLISH', 'ACCESS_AI_PUBLISH', 'FNB_AI_PUBLISH', 'RETAIL_AI_PUBLISH', 'INVENTORY_AI_PUBLISH', 'SEATING_AI_PUBLISH', 'MEMBERSHIP_AI_PUBLISH', 'MARKETING_AI_PUBLISH', 'RESOURCES_AI_PUBLISH', 'QUEUE_AI_PUBLISH', 'TRANSPORT_AI_PUBLISH', 'GAMES_AI_PUBLISH', 'MAINTENANCE_AI_PUBLISH', 'ACCREDITATION_AI_PUBLISH', 'PARTNER_AI_PUBLISH', 'ANALYTICS_AI_PUBLISH', 'BIOMETRIC_IMAGE_VIEW', 'ACCESS_DIRECTION_SET', 'REPORT_GOVERNANCE_MANAGE')) NOT VALID;

ALTER TABLE reporting.report_definition VALIDATE CONSTRAINT report_definition_required_permission_chk;

ALTER TABLE retail.merchandise ADD COLUMN IF NOT EXISTS is_droppable boolean DEFAULT true;

ALTER TABLE retail.sale ADD COLUMN IF NOT EXISTS receipt_barcode text CONSTRAINT sale_receipt_barcode_chk CHECK (char_length(receipt_barcode) <= 64);

ALTER TABLE retail.sale ADD COLUMN IF NOT EXISTS cashier_principal_id uuid;

ALTER TABLE retail.sale_line ADD COLUMN IF NOT EXISTS override_reason text;

ALTER TABLE sync.rejection DROP CONSTRAINT IF EXISTS rejection_kind_chk;

ALTER TABLE sync.rejection ADD CONSTRAINT rejection_kind_chk CHECK (kind IN ('order', 'payment', 'refund', 'void', 'scan', 'cashMovement')) NOT VALID;

ALTER TABLE sync.rejection VALIDATE CONSTRAINT rejection_kind_chk;

CREATE TABLE IF NOT EXISTS venuemap.visit_plan_preset (
    id                                uuid PRIMARY KEY NOT NULL,
    preset_key                        text NOT NULL CONSTRAINT visit_plan_preset_preset_key_chk CHECK (char_length(preset_key) <= 64),
    name                              text NOT NULL CONSTRAINT visit_plan_preset_name_chk CHECK (char_length(name) <= 120),
    name_localised                    jsonb,
    description                       text CONSTRAINT visit_plan_preset_description_chk CHECK (char_length(description) <= 500),
    description_localised             jsonb,
    pace                              text NOT NULL CONSTRAINT visit_plan_preset_pace_chk CHECK (pace IN ('packed', 'balanced', 'relaxed')),
    interest_tags                     text[],
    must_include_point_ids            text[],
    is_built_in                       boolean NOT NULL,
    is_active                         boolean NOT NULL DEFAULT true,
    sort_order                        integer NOT NULL,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

ALTER TABLE wallet.credit_lot ADD COLUMN IF NOT EXISTS issued_credits integer;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'wallet' AND table_name = 'gift_card' AND column_name = 'subject_id' AND is_nullable = 'NO') THEN ALTER TABLE wallet.gift_card ALTER COLUMN subject_id DROP NOT NULL; END IF; END $$;

ALTER TABLE whitelabel.booking_flow DROP CONSTRAINT IF EXISTS booking_flow_flow_type_key_chk;

ALTER TABLE whitelabel.booking_flow ADD CONSTRAINT booking_flow_flow_type_key_chk CHECK (flow_type_key IN ('datedDayPass', 'timedEntry', 'openDated', 'seatedFixedPerformance', 'seatedDateTimeSeatMap', 'experienceWorkshop', 'surfSession', 'meetingRoomHourly', 'cabanaMap', 'guidedTourByLanguage', 'transport', 'tableReservation', 'membership', 'giftCard', 'multiLocation')) NOT VALID;

ALTER TABLE whitelabel.config_version ADD COLUMN IF NOT EXISTS activation_failed_at timestamptz;

ALTER TABLE whitelabel.config_version ADD COLUMN IF NOT EXISTS activation_failure text CONSTRAINT config_version_activation_failure_chk CHECK (char_length(activation_failure) <= 2000);

CREATE TABLE IF NOT EXISTS whitelabel.content_block (
    id                                uuid PRIMARY KEY NOT NULL,
    page_id                           uuid,
    kind                              text NOT NULL CONSTRAINT content_block_kind_chk CHECK (kind IN ('richText', 'image', 'video', 'gallery', 'cta', 'faq', 'form', 'embed', 'productGrid', 'countdown', 'testimonial')),
    position                          integer,
    body                              jsonb,
    locale_variants                   jsonb,
    status                            text NOT NULL CONSTRAINT content_block_status_chk CHECK (status IN ('draft', 'scheduled', 'published', 'expired', 'archived')),
    publish_at                        timestamptz,
    expire_at                         timestamptz,
    audience_segment_id               uuid,
    approved_by_principal_id          uuid,
    review_status                     text DEFAULT 'notRequired' CONSTRAINT content_block_review_status_chk CHECK (review_status IN ('notRequired', 'pending', 'approved', 'rejected')),
    scope_path                        ltree NOT NULL
);

ALTER TABLE whitelabel.footer_config_column ADD COLUMN IF NOT EXISTS sort_order integer;

ALTER TABLE whitelabel.footer_config_column ADD COLUMN IF NOT EXISTS links jsonb;

ALTER TABLE whitelabel.footer_config_social_link ADD COLUMN IF NOT EXISTS sort_order integer;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'access_point_access_area_id_fkey' AND conrelid = to_regclass('access.access_point')) THEN ALTER TABLE access.access_point ADD CONSTRAINT access_point_access_area_id_fkey FOREIGN KEY (access_area_id) REFERENCES access.access_area(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'gate_mode_change_cancelled_by_principal_id_fkey' AND conrelid = to_regclass('access.gate_mode_change')) THEN ALTER TABLE access.gate_mode_change ADD CONSTRAINT gate_mode_change_cancelled_by_principal_id_fkey FOREIGN KEY (cancelled_by_principal_id) REFERENCES identity.principal(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'translation_job_created_by_principal_id_fkey' AND conrelid = to_regclass('ai.translation_job')) THEN ALTER TABLE ai.translation_job ADD CONSTRAINT translation_job_created_by_principal_id_fkey FOREIGN KEY (created_by_principal_id) REFERENCES identity.principal(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'request_approval_matrix_id_fkey' AND conrelid = to_regclass('approvals.request')) THEN ALTER TABLE approvals.request ADD CONSTRAINT request_approval_matrix_id_fkey FOREIGN KEY (approval_matrix_id) REFERENCES approvals.matrix(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'request_rule_id_fkey' AND conrelid = to_regclass('approvals.request')) THEN ALTER TABLE approvals.request ADD CONSTRAINT request_rule_id_fkey FOREIGN KEY (rule_id) REFERENCES approvals.rule(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'media_asset_released_by_principal_id_fkey' AND conrelid = to_regclass('assets.media_asset')) THEN ALTER TABLE assets.media_asset ADD CONSTRAINT media_asset_released_by_principal_id_fkey FOREIGN KEY (released_by_principal_id) REFERENCES identity.principal(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'product_channel_text_product_id_fkey' AND conrelid = to_regclass('catalogue.product_channel_text')) THEN ALTER TABLE catalogue.product_channel_text ADD CONSTRAINT product_channel_text_product_id_fkey FOREIGN KEY (product_id) REFERENCES catalogue.product(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'product_owner_form_product_id_fkey' AND conrelid = to_regclass('catalogue.product_owner_form')) THEN ALTER TABLE catalogue.product_owner_form ADD CONSTRAINT product_owner_form_product_id_fkey FOREIGN KEY (product_id) REFERENCES catalogue.product(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'product_sale_permission_product_id_fkey' AND conrelid = to_regclass('catalogue.product_sale_permission')) THEN ALTER TABLE catalogue.product_sale_permission ADD CONSTRAINT product_sale_permission_product_id_fkey FOREIGN KEY (product_id) REFERENCES catalogue.product(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'published_bundle_published_by_fkey' AND conrelid = to_regclass('catalogue.published_bundle')) THEN ALTER TABLE catalogue.published_bundle ADD CONSTRAINT published_bundle_published_by_fkey FOREIGN KEY (published_by) REFERENCES identity.principal(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'session_ended_by_principal_id_fkey' AND conrelid = to_regclass('identity.session')) THEN ALTER TABLE identity."session" ADD CONSTRAINT session_ended_by_principal_id_fkey FOREIGN KEY (ended_by_principal_id) REFERENCES identity.principal(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'delegated_access_granted_by_subject_id_fkey' AND conrelid = to_regclass('identity.delegated_access')) THEN ALTER TABLE identity.delegated_access ADD CONSTRAINT delegated_access_granted_by_subject_id_fkey FOREIGN KEY (granted_by_subject_id) REFERENCES pii.subject(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'mfa_challenge_subject_id_fkey' AND conrelid = to_regclass('identity.mfa_challenge')) THEN ALTER TABLE identity.mfa_challenge ADD CONSTRAINT mfa_challenge_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES pii.subject(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'mfa_method_subject_id_fkey' AND conrelid = to_regclass('identity.mfa_method')) THEN ALTER TABLE identity.mfa_method ADD CONSTRAINT mfa_method_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES pii.subject(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'mfa_recovery_code_subject_id_fkey' AND conrelid = to_regclass('identity.mfa_recovery_code')) THEN ALTER TABLE identity.mfa_recovery_code ADD CONSTRAINT mfa_recovery_code_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES pii.subject(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'principal_external_identity_principal_id_fkey' AND conrelid = to_regclass('identity.principal_external_identity')) THEN ALTER TABLE identity.principal_external_identity ADD CONSTRAINT principal_external_identity_principal_id_fkey FOREIGN KEY (principal_id) REFERENCES identity.principal(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'principal_external_identity_sso_provider_id_fkey' AND conrelid = to_regclass('identity.principal_external_identity')) THEN ALTER TABLE identity.principal_external_identity ADD CONSTRAINT principal_external_identity_sso_provider_id_fkey FOREIGN KEY (sso_provider_id) REFERENCES identity.sso_provider(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'sso_provider_default_home_scope_id_fkey' AND conrelid = to_regclass('identity.sso_provider')) THEN ALTER TABLE identity.sso_provider ADD CONSTRAINT sso_provider_default_home_scope_id_fkey FOREIGN KEY (default_home_scope_id) REFERENCES platform.scope(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'journal_entry_legal_entity_id_fkey' AND conrelid = to_regclass('ledger.journal_entry')) THEN ALTER TABLE ledger.journal_entry ADD CONSTRAINT journal_entry_legal_entity_id_fkey FOREIGN KEY (legal_entity_id) REFERENCES ledger.legal_entity(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'form_submission_sale_link_submission_id_fkey' AND conrelid = to_regclass('marketing.form_submission_sale_link')) THEN ALTER TABLE marketing.form_submission_sale_link ADD CONSTRAINT form_submission_sale_link_submission_id_fkey FOREIGN KEY (submission_id) REFERENCES marketing.form_submission(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'provider_connection_provider_id_fkey' AND conrelid = to_regclass('payments.provider_connection')) THEN ALTER TABLE payments.provider_connection ADD CONSTRAINT provider_connection_provider_id_fkey FOREIGN KEY (provider_id) REFERENCES payments.provider(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'provider_event_provider_connection_id_fkey' AND conrelid = to_regclass('payments.provider_event')) THEN ALTER TABLE payments.provider_event ADD CONSTRAINT provider_event_provider_connection_id_fkey FOREIGN KEY (provider_connection_id) REFERENCES payments.provider_connection(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'subject_identity_subject_id_fkey' AND conrelid = to_regclass('pii.subject_identity')) THEN ALTER TABLE pii.subject_identity ADD CONSTRAINT subject_identity_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES pii.subject(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'bundle_variant_id_fkey' AND conrelid = to_regclass('promotions.bundle')) THEN ALTER TABLE promotions.bundle ADD CONSTRAINT bundle_variant_id_fkey FOREIGN KEY (variant_id) REFERENCES catalogue.variant(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'sale_cashier_principal_id_fkey' AND conrelid = to_regclass('retail.sale')) THEN ALTER TABLE retail.sale ADD CONSTRAINT sale_cashier_principal_id_fkey FOREIGN KEY (cashier_principal_id) REFERENCES identity.principal(id); END IF; END $$;

CREATE INDEX IF NOT EXISTS content_block_approved_by_principal_id_idx ON whitelabel.content_block (approved_by_principal_id);

CREATE INDEX IF NOT EXISTS content_block_audience_segment_id_idx ON whitelabel.content_block (audience_segment_id);

CREATE INDEX IF NOT EXISTS content_block_page_id_idx ON whitelabel.content_block (page_id);

CREATE INDEX IF NOT EXISTS chunk_embedding_subject_id_idx ON ai.chunk_embedding (subject_id);

CREATE INDEX IF NOT EXISTS index_entry_subject_id_idx ON ai.index_entry (subject_id);

CREATE INDEX IF NOT EXISTS outbox_aggregate_id_sequence_idx ON ai.outbox (aggregate_id, sequence);

CREATE INDEX IF NOT EXISTS bundle_application_workstation_id_applied_at_idx ON catalogue.bundle_application (workstation_id, applied_at);

CREATE INDEX IF NOT EXISTS open_shift_marker_principal_id_workstation_id_idx ON identity.open_shift_marker (principal_id, workstation_id);

CREATE INDEX IF NOT EXISTS payment_provider_reference_idx ON orders.payment (provider_reference);

CREATE INDEX IF NOT EXISTS outbox_aggregate_id_sequence_idx ON platform.outbox (aggregate_id, sequence);

CREATE INDEX IF NOT EXISTS profile_deployment_profile_id_version_idx ON platform.profile_deployment (profile_id, version);

CREATE INDEX IF NOT EXISTS workstation_configuration_profile_id_configuration_d7f5bd55_idx ON platform.workstation (configuration_profile_id, configuration_profile_version);

CREATE INDEX IF NOT EXISTS access_point_access_area_id_idx ON access.access_point (access_area_id);

CREATE INDEX IF NOT EXISTS gate_mode_change_cancelled_by_principal_id_idx ON access.gate_mode_change (cancelled_by_principal_id);

CREATE INDEX IF NOT EXISTS translation_job_created_by_principal_id_idx ON ai.translation_job (created_by_principal_id);

CREATE INDEX IF NOT EXISTS request_approval_matrix_id_idx ON approvals.request (approval_matrix_id);

CREATE INDEX IF NOT EXISTS request_rule_id_idx ON approvals.request (rule_id);

CREATE INDEX IF NOT EXISTS media_asset_released_by_principal_id_idx ON assets.media_asset (released_by_principal_id);

CREATE INDEX IF NOT EXISTS product_channel_text_product_id_idx ON catalogue.product_channel_text (product_id);

CREATE INDEX IF NOT EXISTS product_owner_form_product_id_idx ON catalogue.product_owner_form (product_id);

CREATE INDEX IF NOT EXISTS product_sale_permission_product_id_idx ON catalogue.product_sale_permission (product_id);

CREATE INDEX IF NOT EXISTS published_bundle_published_by_idx ON catalogue.published_bundle (published_by);

CREATE INDEX IF NOT EXISTS delegated_access_granted_by_subject_id_idx ON identity.delegated_access (granted_by_subject_id);

CREATE INDEX IF NOT EXISTS mfa_challenge_subject_id_idx ON identity.mfa_challenge (subject_id);

CREATE INDEX IF NOT EXISTS mfa_method_subject_id_idx ON identity.mfa_method (subject_id);

CREATE INDEX IF NOT EXISTS mfa_recovery_code_subject_id_idx ON identity.mfa_recovery_code (subject_id);

CREATE INDEX IF NOT EXISTS principal_external_identity_principal_id_idx ON identity.principal_external_identity (principal_id);

CREATE INDEX IF NOT EXISTS principal_external_identity_sso_provider_id_idx ON identity.principal_external_identity (sso_provider_id);

CREATE INDEX IF NOT EXISTS session_ended_by_principal_id_idx ON identity."session" (ended_by_principal_id);

CREATE INDEX IF NOT EXISTS sso_provider_default_home_scope_id_idx ON identity.sso_provider (default_home_scope_id);

CREATE INDEX IF NOT EXISTS journal_entry_legal_entity_id_idx ON ledger.journal_entry (legal_entity_id);

CREATE INDEX IF NOT EXISTS form_submission_sale_link_submission_id_idx ON marketing.form_submission_sale_link (submission_id);

CREATE INDEX IF NOT EXISTS provider_connection_provider_id_idx ON payments.provider_connection (provider_id);

CREATE INDEX IF NOT EXISTS provider_event_provider_connection_id_idx ON payments.provider_event (provider_connection_id);

CREATE INDEX IF NOT EXISTS subject_identity_subject_id_idx ON pii.subject_identity (subject_id);

CREATE INDEX IF NOT EXISTS bundle_variant_id_idx ON promotions.bundle (variant_id);

CREATE INDEX IF NOT EXISTS sale_cashier_principal_id_idx ON retail.sale (cashier_principal_id);

CREATE UNIQUE INDEX IF NOT EXISTS product_tag_scope_path_code_uniq ON catalogue.product_tag (scope_path, lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS index_source_table_name_uniq ON ai.index_source (lower(table_name));

CREATE UNIQUE INDEX IF NOT EXISTS vector_store_collection_name_uniq ON ai.vector_store (lower(collection_name));

CREATE UNIQUE INDEX IF NOT EXISTS matrix_kind_scope_path_version_uniq ON approvals.matrix (lower(kind), scope_path, version);

CREATE UNIQUE INDEX IF NOT EXISTS product_channel_text_product_id_uniq ON catalogue.product_channel_text (product_id);

CREATE UNIQUE INDEX IF NOT EXISTS product_owner_form_product_id_applies_to_uniq ON catalogue.product_owner_form (product_id, lower(applies_to));

CREATE UNIQUE INDEX IF NOT EXISTS product_sale_permission_product_id_level_target_id_uniq ON catalogue.product_sale_permission (product_id, lower(level), target_id) NULLS NOT DISTINCT;

CREATE UNIQUE INDEX IF NOT EXISTS principal_external_identity_sso_provider_id_exter_cae3c74e_uniq ON identity.principal_external_identity (sso_provider_id, external_subject);

CREATE UNIQUE INDEX IF NOT EXISTS journal_entry_legal_entity_id_entry_number_uniq ON ledger.journal_entry (legal_entity_id, lower(entry_number));

CREATE UNIQUE INDEX IF NOT EXISTS form_submission_sale_link_order_id_owner_role_ord_27062069_uniq ON marketing.form_submission_sale_link (order_id, lower(owner_role), order_line_id, unit_index) NULLS NOT DISTINCT;

CREATE UNIQUE INDEX IF NOT EXISTS subject_identity_provider_provider_subject_uniq ON pii.subject_identity (lower(provider), provider_subject);

CREATE UNIQUE INDEX IF NOT EXISTS device_assignment_device_id_uniq ON tenancy.device_assignment (device_id);

CREATE UNIQUE INDEX IF NOT EXISTS visit_plan_preset_scope_path_preset_key_uniq ON venuemap.visit_plan_preset (scope_path, lower(preset_key));

CREATE UNIQUE INDEX IF NOT EXISTS configuration_version_scope_path_version_uniq ON wallet.configuration_version (scope_path, version);

CREATE UNIQUE INDEX IF NOT EXISTS analytics_provider_venue_id_provider_uniq ON whitelabel.analytics_provider (venue_id, lower(provider)) NULLS NOT DISTINCT;

CREATE UNIQUE INDEX IF NOT EXISTS config_version_scope_path_version_uniq ON whitelabel.config_version (scope_path, lower(version));

CREATE UNIQUE INDEX IF NOT EXISTS kiosk_config_version_kiosk_config_id_version_number_uniq ON whitelabel.kiosk_config_version (kiosk_config_id, version_number);

CREATE UNIQUE INDEX IF NOT EXISTS asset_version_asset_id_uniq ON assets.asset_version (asset_id) WHERE is_current;

CREATE UNIQUE INDEX IF NOT EXISTS product_version_product_id_uniq ON catalogue.product_version (product_id) WHERE is_current;

CREATE UNIQUE INDEX IF NOT EXISTS config_version_scope_path_uniq ON whitelabel.config_version (scope_path) WHERE is_current;

CREATE UNIQUE INDEX IF NOT EXISTS kiosk_config_version_kiosk_config_id_uniq ON whitelabel.kiosk_config_version (kiosk_config_id) WHERE is_current;

CREATE INDEX IF NOT EXISTS account_mapping_scope_path_idx ON ledger.account_mapping USING gist (scope_path);

CREATE INDEX IF NOT EXISTS content_block_scope_path_idx ON whitelabel.content_block USING gist (scope_path);

CREATE INDEX IF NOT EXISTS form_submission_sale_link_scope_path_idx ON marketing.form_submission_sale_link USING gist (scope_path);

CREATE INDEX IF NOT EXISTS open_shift_marker_scope_path_idx ON identity.open_shift_marker USING gist (scope_path);

CREATE INDEX IF NOT EXISTS outbox_scope_path_idx ON ai.outbox USING gist (scope_path);

CREATE INDEX IF NOT EXISTS outbox_sequence_scope_path_idx ON ai.outbox_sequence USING gist (scope_path);

CREATE INDEX IF NOT EXISTS outbox_sequence_scope_path_idx ON platform.outbox_sequence USING gist (scope_path);

CREATE INDEX IF NOT EXISTS product_channel_text_scope_path_idx ON catalogue.product_channel_text USING gist (scope_path);

CREATE INDEX IF NOT EXISTS product_owner_form_scope_path_idx ON catalogue.product_owner_form USING gist (scope_path);

CREATE INDEX IF NOT EXISTS product_sale_permission_scope_path_idx ON catalogue.product_sale_permission USING gist (scope_path);

CREATE INDEX IF NOT EXISTS product_tag_scope_path_idx ON catalogue.product_tag USING gist (scope_path);

CREATE INDEX IF NOT EXISTS translation_job_scope_path_idx ON ai.translation_job USING gist (scope_path);

CREATE INDEX IF NOT EXISTS visit_plan_preset_scope_path_idx ON venuemap.visit_plan_preset USING gist (scope_path);

CREATE OR REPLACE FUNCTION platform.own_row(row_principal_id uuid, row_subject_id uuid)
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT (row_principal_id IS NOT NULL
            AND row_principal_id::text = NULLIF(current_setting('ticvai.principal_id', true), ''))
        OR (row_subject_id IS NOT NULL
            AND row_subject_id::text = NULLIF(current_setting('ticvai.subject_id', true), ''))
        OR platform.tenant_root_in_scope();
$$;

CREATE OR REPLACE FUNCTION platform.apply_own_row_rls(target regclass, principal_column text, subject_column text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    chk text := format('platform.own_row(%s, %s)',
                       CASE WHEN principal_column IS NULL THEN 'NULL::uuid' ELSE quote_ident(principal_column) END,
                       CASE WHEN subject_column IS NULL THEN 'NULL::uuid' ELSE quote_ident(subject_column) END);
BEGIN
    PERFORM platform.apply_split_rls(target, chk, chk);
END
$$;

CREATE OR REPLACE FUNCTION platform.signed_in()
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT cardinality(platform.current_scope_paths()) > 0
        OR NULLIF(current_setting('ticvai.subject_id', true), '') IS NOT NULL;
$$;

SELECT platform.apply_scope_rls('ai.outbox'::regclass);

SELECT platform.apply_scope_rls('ai.outbox_sequence'::regclass);

SELECT platform.apply_scope_rls('ai.translation_job'::regclass);

SELECT platform.apply_scope_rls('catalogue.product_channel_text'::regclass);

SELECT platform.apply_scope_rls('catalogue.product_owner_form'::regclass);

SELECT platform.apply_scope_rls('catalogue.product_sale_permission'::regclass);

SELECT platform.apply_scope_rls('catalogue.product_tag'::regclass);

SELECT platform.apply_scope_rls('identity.open_shift_marker'::regclass);

SELECT platform.apply_scope_rls('marketing.form_submission_sale_link'::regclass);

SELECT platform.apply_scope_rls('platform.outbox_sequence'::regclass);

SELECT platform.apply_scope_rls('venuemap.visit_plan_preset'::regclass);

SELECT platform.apply_scope_rls('whitelabel.content_block'::regclass);

SELECT platform.apply_venue_rls('catalogue.bundle_application'::regclass);

SELECT platform.drop_rls_policies('identity.delegated_access'::regclass);

SELECT platform.apply_split_rls('identity.delegated_access'::regclass, 'platform.in_scope(scope_path) OR platform.own_row(NULL::uuid, subject_id) OR platform.own_row(NULL::uuid, over_subject_id) OR platform.own_row(NULL::uuid, granted_by_subject_id)', '(platform.in_scope(scope_path) OR platform.own_row(NULL::uuid, over_subject_id))');

SELECT platform.drop_rls_policies('identity.mfa_challenge'::regclass);

SELECT platform.apply_own_row_rls('identity.mfa_challenge'::regclass, 'principal_id', 'subject_id');

SELECT platform.drop_rls_policies('identity.mfa_method'::regclass);

SELECT platform.apply_own_row_rls('identity.mfa_method'::regclass, 'principal_id', 'subject_id');

SELECT platform.drop_rls_policies('identity.mfa_recovery_code'::regclass);

SELECT platform.apply_own_row_rls('identity.mfa_recovery_code'::regclass, 'principal_id', 'subject_id');

SELECT platform.drop_rls_policies('identity.principal'::regclass);

SELECT platform.apply_grant_holder_read_rls('identity.principal'::regclass, '(platform.tenant_root_in_scope() OR EXISTS (SELECT 1 FROM platform.scope hs WHERE hs.id = home_scope_id AND platform.in_scope(hs.path)))');

SELECT platform.drop_rls_policies('identity.principal_credential'::regclass);

SELECT platform.apply_split_rls('identity.principal_credential'::regclass, '(platform.own_row(principal_id, NULL::uuid) OR EXISTS (SELECT 1 FROM identity.principal hp JOIN platform.scope hs ON hs.id = hp.home_scope_id WHERE hp.id = principal_id AND platform.in_scope(hs.path)))', '(platform.own_row(principal_id, NULL::uuid) OR EXISTS (SELECT 1 FROM identity.principal hp JOIN platform.scope hs ON hs.id = hp.home_scope_id WHERE hp.id = principal_id AND platform.in_scope(hs.path)))');

SELECT platform.drop_rls_policies('ledger.account_mapping'::regclass);

SELECT platform.apply_read_beneath_rls('ledger.account_mapping'::regclass);

SELECT platform.drop_rls_policies('marketing.badge'::regclass);

SELECT platform.apply_split_rls('marketing.badge'::regclass, 'platform.signed_in()', 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('marketing.loyalty_programme'::regclass);

SELECT platform.apply_split_rls('marketing.loyalty_programme'::regclass, 'venue_id IS NULL OR platform.venue_in_scope(venue_id)', 'platform.venue_in_scope(venue_id)');

SELECT platform.drop_rls_policies('pii.subject'::regclass);

SELECT platform.apply_split_rls('pii.subject'::regclass, 'platform.grant_holder() OR platform.own_row(NULL::uuid, id)', 'platform.own_row(NULL::uuid, id)');

SELECT platform.drop_rls_policies('wallet.gift_card'::regclass);

SELECT platform.apply_split_rls('wallet.gift_card'::regclass, 'platform.signed_in()', 'platform.subject_in_scope(subject_id)');

SELECT platform.apply_parent_rls('identity.principal_external_identity'::regclass, 'sso_provider_id', 'identity.sso_provider'::regclass, 'id');

SELECT platform.drop_rls_policies('marketing.customer_badge'::regclass);

SELECT platform.apply_split_rls('marketing.customer_badge'::regclass, '(platform.grant_holder() AND EXISTS (SELECT 1 FROM marketing.badge pr WHERE pr.id = marketing.customer_badge.badge_id)) OR platform.own_row(NULL::uuid, customer_id)', 'EXISTS (SELECT 1 FROM marketing.badge pr WHERE pr.id = marketing.customer_badge.badge_id AND (platform.in_scope(pr.scope_path)))');

SELECT platform.drop_rls_policies('marketing.loyalty_position'::regclass);

SELECT platform.apply_split_rls('marketing.loyalty_position'::regclass, '(platform.grant_holder() AND EXISTS (SELECT 1 FROM marketing.loyalty_programme pr WHERE pr.id = marketing.loyalty_position.programme_id)) OR platform.own_row(NULL::uuid, subject_id)', 'EXISTS (SELECT 1 FROM marketing.loyalty_programme pr WHERE pr.id = marketing.loyalty_position.programme_id AND (platform.venue_in_scope(pr.venue_id)))');

SELECT platform.drop_rls_policies('marketing.points_earning_rule'::regclass);

SELECT platform.apply_split_rls('marketing.points_earning_rule'::regclass, '(platform.grant_holder() AND EXISTS (SELECT 1 FROM marketing.loyalty_programme pr WHERE pr.id = marketing.points_earning_rule.loyalty_programme_id))', 'EXISTS (SELECT 1 FROM marketing.loyalty_programme pr WHERE pr.id = marketing.points_earning_rule.loyalty_programme_id AND (platform.venue_in_scope(pr.venue_id)))');

SELECT platform.drop_rls_policies('marketing.programme_tier'::regclass);

SELECT platform.apply_split_rls('marketing.programme_tier'::regclass, '(platform.grant_holder() AND EXISTS (SELECT 1 FROM marketing.loyalty_programme pr WHERE pr.id = marketing.programme_tier.loyalty_programme_id))', 'EXISTS (SELECT 1 FROM marketing.loyalty_programme pr WHERE pr.id = marketing.programme_tier.loyalty_programme_id AND (platform.venue_in_scope(pr.venue_id)))');

SELECT platform.drop_rls_policies('identity.principal_credential_history'::regclass);

SELECT platform.apply_parent_split_rls('identity.principal_credential_history'::regclass, 'principal_credential_id', 'identity.principal_credential'::regclass, 'id', '(platform.own_row(parent_row.principal_id, NULL::uuid) OR EXISTS (SELECT 1 FROM identity.principal hp JOIN platform.scope hs ON hs.id = hp.home_scope_id WHERE hp.id = parent_row.principal_id AND platform.in_scope(hs.path)))');

SELECT platform.apply_subject_rls('assets.guest_upload'::regclass);

SELECT platform.apply_subject_rls('pii.subject_identity'::regclass);

SELECT platform.apply_tenant_rls('ai.vector_store'::regclass);

SELECT platform.drop_rls_policies('platform.audit_read'::regclass);

SELECT platform.apply_append_audit_rls('platform.audit_read'::regclass);

CREATE TABLE IF NOT EXISTS ai.outbox_default PARTITION OF ai.outbox DEFAULT;

SELECT platform.ensure_month_partitions('ai.outbox'::regclass, 3);

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0108', 'after r1 (9cec72d): 18 table(s), 87 column(s), 71 index(es), 91 other statement(s), 17 row-level security polic(ies) re-applied', 'bba9d0c2593f1e9dede4dcdb28aaaed9abf862a7442945954e9fec9fc8e17400')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP TABLE IF EXISTS ai.outbox_default;
-- SELECT platform.drop_rls_policies('platform.audit_read'::regclass); SELECT platform.apply_subject_rls('platform.audit_read'::regclass);
-- SELECT platform.drop_rls_policies('identity.principal_credential_history'::regclass); SELECT platform.apply_tenant_rls('identity.principal_credential_history'::regclass);
-- SELECT platform.drop_rls_policies('marketing.programme_tier'::regclass); SELECT platform.apply_parent_rls('marketing.programme_tier'::regclass, 'loyalty_programme_id', 'marketing.loyalty_programme'::regclass, 'id');
-- SELECT platform.drop_rls_policies('marketing.points_earning_rule'::regclass); SELECT platform.apply_parent_rls('marketing.points_earning_rule'::regclass, 'loyalty_programme_id', 'marketing.loyalty_programme'::regclass, 'id');
-- SELECT platform.drop_rls_policies('marketing.loyalty_position'::regclass); SELECT platform.apply_parent_rls('marketing.loyalty_position'::regclass, 'programme_id', 'marketing.loyalty_programme'::regclass, 'id');
-- SELECT platform.drop_rls_policies('marketing.customer_badge'::regclass); SELECT platform.apply_tenant_rls('marketing.customer_badge'::regclass); SELECT platform.apply_parent_split_rls('marketing.customer_badge'::regclass, 'badge_id', 'marketing.badge'::regclass, 'id', 'platform.in_scope(parent_row.scope_path)');
-- SELECT platform.drop_rls_policies('wallet.gift_card'::regclass); SELECT platform.apply_subject_rls('wallet.gift_card'::regclass); SELECT platform.apply_grant_holder_subject_read_rls('wallet.gift_card'::regclass);
-- SELECT platform.drop_rls_policies('pii.subject'::regclass); SELECT platform.apply_tenant_rls('pii.subject'::regclass); SELECT platform.apply_grant_holder_read_rls('pii.subject'::regclass, 'platform.tenant_root_in_scope()');
-- SELECT platform.drop_rls_policies('marketing.loyalty_programme'::regclass); SELECT platform.apply_venue_rls('marketing.loyalty_programme'::regclass);
-- SELECT platform.drop_rls_policies('marketing.badge'::regclass); SELECT platform.apply_tenant_rls('marketing.badge'::regclass); SELECT platform.apply_grant_holder_read_rls('marketing.badge'::regclass, 'platform.in_scope(scope_path)');
-- SELECT platform.drop_rls_policies('ledger.account_mapping'::regclass); SELECT platform.apply_venue_rls('ledger.account_mapping'::regclass);
-- SELECT platform.drop_rls_policies('identity.principal_credential'::regclass); SELECT platform.apply_tenant_rls('identity.principal_credential'::regclass);
-- SELECT platform.drop_rls_policies('identity.principal'::regclass); SELECT platform.apply_tenant_rls('identity.principal'::regclass); SELECT platform.apply_grant_holder_read_rls('identity.principal'::regclass, 'platform.tenant_root_in_scope()');
-- SELECT platform.drop_rls_policies('identity.mfa_recovery_code'::regclass); SELECT platform.apply_tenant_rls('identity.mfa_recovery_code'::regclass);
-- SELECT platform.drop_rls_policies('identity.mfa_method'::regclass); SELECT platform.apply_tenant_rls('identity.mfa_method'::regclass);
-- SELECT platform.drop_rls_policies('identity.mfa_challenge'::regclass); SELECT platform.apply_tenant_rls('identity.mfa_challenge'::regclass);
-- SELECT platform.drop_rls_policies('identity.delegated_access'::regclass); SELECT platform.apply_scope_rls('identity.delegated_access'::regclass);
-- DROP INDEX IF EXISTS venuemap.visit_plan_preset_scope_path_idx;
-- DROP INDEX IF EXISTS ai.translation_job_scope_path_idx;
-- DROP INDEX IF EXISTS catalogue.product_tag_scope_path_idx;
-- DROP INDEX IF EXISTS catalogue.product_sale_permission_scope_path_idx;
-- DROP INDEX IF EXISTS catalogue.product_owner_form_scope_path_idx;
-- DROP INDEX IF EXISTS catalogue.product_channel_text_scope_path_idx;
-- DROP INDEX IF EXISTS platform.outbox_sequence_scope_path_idx;
-- DROP INDEX IF EXISTS ai.outbox_sequence_scope_path_idx;
-- DROP INDEX IF EXISTS ai.outbox_scope_path_idx;
-- DROP INDEX IF EXISTS identity.open_shift_marker_scope_path_idx;
-- DROP INDEX IF EXISTS marketing.form_submission_sale_link_scope_path_idx;
-- DROP INDEX IF EXISTS whitelabel.content_block_scope_path_idx;
-- DROP INDEX IF EXISTS ledger.account_mapping_scope_path_idx;
-- DROP INDEX IF EXISTS whitelabel.kiosk_config_version_kiosk_config_id_uniq;
-- DROP INDEX IF EXISTS whitelabel.config_version_scope_path_uniq;
-- DROP INDEX IF EXISTS catalogue.product_version_product_id_uniq;
-- DROP INDEX IF EXISTS assets.asset_version_asset_id_uniq;
-- DROP INDEX IF EXISTS whitelabel.kiosk_config_version_kiosk_config_id_version_number_uniq;
-- DROP INDEX IF EXISTS whitelabel.config_version_scope_path_version_uniq;
-- DROP INDEX IF EXISTS whitelabel.analytics_provider_venue_id_provider_uniq;
-- DROP INDEX IF EXISTS wallet.configuration_version_scope_path_version_uniq;
-- DROP INDEX IF EXISTS venuemap.visit_plan_preset_scope_path_preset_key_uniq;
-- DROP INDEX IF EXISTS tenancy.device_assignment_device_id_uniq;
-- DROP INDEX IF EXISTS pii.subject_identity_provider_provider_subject_uniq;
-- DROP INDEX IF EXISTS marketing.form_submission_sale_link_order_id_owner_role_ord_27062069_uniq;
-- DROP INDEX IF EXISTS ledger.journal_entry_legal_entity_id_entry_number_uniq;
-- DROP INDEX IF EXISTS identity.principal_external_identity_sso_provider_id_exter_cae3c74e_uniq;
-- DROP INDEX IF EXISTS catalogue.product_sale_permission_product_id_level_target_id_uniq;
-- DROP INDEX IF EXISTS catalogue.product_owner_form_product_id_applies_to_uniq;
-- DROP INDEX IF EXISTS catalogue.product_channel_text_product_id_uniq;
-- DROP INDEX IF EXISTS approvals.matrix_kind_scope_path_version_uniq;
-- DROP INDEX IF EXISTS ai.vector_store_collection_name_uniq;
-- DROP INDEX IF EXISTS ai.index_source_table_name_uniq;
-- DROP INDEX IF EXISTS catalogue.product_tag_scope_path_code_uniq;
-- DROP INDEX IF EXISTS retail.sale_cashier_principal_id_idx;
-- DROP INDEX IF EXISTS promotions.bundle_variant_id_idx;
-- DROP INDEX IF EXISTS pii.subject_identity_subject_id_idx;
-- DROP INDEX IF EXISTS payments.provider_event_provider_connection_id_idx;
-- DROP INDEX IF EXISTS payments.provider_connection_provider_id_idx;
-- DROP INDEX IF EXISTS marketing.form_submission_sale_link_submission_id_idx;
-- DROP INDEX IF EXISTS ledger.journal_entry_legal_entity_id_idx;
-- DROP INDEX IF EXISTS identity.sso_provider_default_home_scope_id_idx;
-- DROP INDEX IF EXISTS identity.session_ended_by_principal_id_idx;
-- DROP INDEX IF EXISTS identity.principal_external_identity_sso_provider_id_idx;
-- DROP INDEX IF EXISTS identity.principal_external_identity_principal_id_idx;
-- DROP INDEX IF EXISTS identity.mfa_recovery_code_subject_id_idx;
-- DROP INDEX IF EXISTS identity.mfa_method_subject_id_idx;
-- DROP INDEX IF EXISTS identity.mfa_challenge_subject_id_idx;
-- DROP INDEX IF EXISTS identity.delegated_access_granted_by_subject_id_idx;
-- DROP INDEX IF EXISTS catalogue.published_bundle_published_by_idx;
-- DROP INDEX IF EXISTS catalogue.product_sale_permission_product_id_idx;
-- DROP INDEX IF EXISTS catalogue.product_owner_form_product_id_idx;
-- DROP INDEX IF EXISTS catalogue.product_channel_text_product_id_idx;
-- DROP INDEX IF EXISTS assets.media_asset_released_by_principal_id_idx;
-- DROP INDEX IF EXISTS approvals.request_rule_id_idx;
-- DROP INDEX IF EXISTS approvals.request_approval_matrix_id_idx;
-- DROP INDEX IF EXISTS ai.translation_job_created_by_principal_id_idx;
-- DROP INDEX IF EXISTS access.gate_mode_change_cancelled_by_principal_id_idx;
-- DROP INDEX IF EXISTS access.access_point_access_area_id_idx;
-- DROP INDEX IF EXISTS platform.workstation_configuration_profile_id_configuration_d7f5bd55_idx;
-- DROP INDEX IF EXISTS platform.profile_deployment_profile_id_version_idx;
-- DROP INDEX IF EXISTS platform.outbox_aggregate_id_sequence_idx;
-- DROP INDEX IF EXISTS orders.payment_provider_reference_idx;
-- DROP INDEX IF EXISTS identity.open_shift_marker_principal_id_workstation_id_idx;
-- DROP INDEX IF EXISTS catalogue.bundle_application_workstation_id_applied_at_idx;
-- DROP INDEX IF EXISTS ai.outbox_aggregate_id_sequence_idx;
-- DROP INDEX IF EXISTS ai.index_entry_subject_id_idx;
-- DROP INDEX IF EXISTS ai.chunk_embedding_subject_id_idx;
-- DROP INDEX IF EXISTS whitelabel.content_block_page_id_idx;
-- DROP INDEX IF EXISTS whitelabel.content_block_audience_segment_id_idx;
-- DROP INDEX IF EXISTS whitelabel.content_block_approved_by_principal_id_idx;
-- ALTER TABLE retail.sale DROP CONSTRAINT IF EXISTS sale_cashier_principal_id_fkey;
-- ALTER TABLE promotions.bundle DROP CONSTRAINT IF EXISTS bundle_variant_id_fkey;
-- ALTER TABLE payments.provider_event DROP CONSTRAINT IF EXISTS provider_event_provider_connection_id_fkey;
-- ALTER TABLE payments.provider_connection DROP CONSTRAINT IF EXISTS provider_connection_provider_id_fkey;
-- ALTER TABLE ledger.journal_entry DROP CONSTRAINT IF EXISTS journal_entry_legal_entity_id_fkey;
-- ALTER TABLE identity.sso_provider DROP CONSTRAINT IF EXISTS sso_provider_default_home_scope_id_fkey;
-- ALTER TABLE identity.mfa_recovery_code DROP CONSTRAINT IF EXISTS mfa_recovery_code_subject_id_fkey;
-- ALTER TABLE identity.mfa_method DROP CONSTRAINT IF EXISTS mfa_method_subject_id_fkey;
-- ALTER TABLE identity.mfa_challenge DROP CONSTRAINT IF EXISTS mfa_challenge_subject_id_fkey;
-- ALTER TABLE identity.delegated_access DROP CONSTRAINT IF EXISTS delegated_access_granted_by_subject_id_fkey;
-- ALTER TABLE identity.session DROP CONSTRAINT IF EXISTS session_ended_by_principal_id_fkey;
-- ALTER TABLE catalogue.published_bundle DROP CONSTRAINT IF EXISTS published_bundle_published_by_fkey;
-- ALTER TABLE assets.media_asset DROP CONSTRAINT IF EXISTS media_asset_released_by_principal_id_fkey;
-- ALTER TABLE approvals.request DROP CONSTRAINT IF EXISTS request_rule_id_fkey;
-- ALTER TABLE approvals.request DROP CONSTRAINT IF EXISTS request_approval_matrix_id_fkey;
-- ALTER TABLE access.gate_mode_change DROP CONSTRAINT IF EXISTS gate_mode_change_cancelled_by_principal_id_fkey;
-- ALTER TABLE access.access_point DROP CONSTRAINT IF EXISTS access_point_access_area_id_fkey;
-- ALTER TABLE whitelabel.footer_config_social_link DROP COLUMN IF EXISTS sort_order;
-- ALTER TABLE whitelabel.footer_config_column DROP COLUMN IF EXISTS links;
-- ALTER TABLE whitelabel.footer_config_column DROP COLUMN IF EXISTS sort_order;
-- DROP TABLE IF EXISTS whitelabel.content_block;
-- ALTER TABLE whitelabel.config_version DROP COLUMN IF EXISTS activation_failure;
-- ALTER TABLE whitelabel.config_version DROP COLUMN IF EXISTS activation_failed_at;
-- ALTER TABLE whitelabel.booking_flow DROP CONSTRAINT IF EXISTS booking_flow_flow_type_key_chk; ALTER TABLE whitelabel.booking_flow ADD CONSTRAINT booking_flow_flow_type_key_chk CHECK (flow_type_key IN ('datedDayPass', 'timedEntry', 'openDated', 'seatedFixedPerformance', 'seatedDateTimeSeatMap', 'experienceWorkshop', 'surfSession', 'meetingRoomHourly', 'cabanaMap', 'cabanaBySize', 'guidedTourByLanguage', 'transport', 'tableReservation', 'membership', 'giftCard', 'multiLocation')) NOT VALID;
-- ALTER TABLE wallet.gift_card ALTER COLUMN subject_id SET NOT NULL;
-- ALTER TABLE wallet.credit_lot DROP COLUMN IF EXISTS issued_credits;
-- DROP TABLE IF EXISTS venuemap.visit_plan_preset;
-- ALTER TABLE sync.rejection DROP CONSTRAINT IF EXISTS rejection_kind_chk; ALTER TABLE sync.rejection ADD CONSTRAINT rejection_kind_chk CHECK (kind IN ('order', 'payment', 'refund', 'void', 'scan')) NOT VALID;
-- ALTER TABLE retail.sale_line DROP COLUMN IF EXISTS override_reason;
-- ALTER TABLE retail.sale DROP COLUMN IF EXISTS cashier_principal_id;
-- ALTER TABLE retail.sale DROP COLUMN IF EXISTS receipt_barcode;
-- ALTER TABLE retail.merchandise DROP COLUMN IF EXISTS is_droppable;
-- ALTER TABLE reporting.report_definition DROP CONSTRAINT IF EXISTS report_definition_required_permission_chk; ALTER TABLE reporting.report_definition ADD CONSTRAINT report_definition_required_permission_chk CHECK (required_permission IN ('SESSION_FORCE_LOGOUT', 'USER_MANAGE', 'ROLE_MANAGE', 'PERMISSION_GRANT', 'PERMISSION_VIEW', 'PERMISSION_MANAGE', 'PLATFORM_TENANT_VIEW', 'PLATFORM_TENANT_MANAGE', 'PLATFORM_TENANT_TERMINATE', 'PLATFORM_PLAN_MANAGE', 'PLATFORM_CELL_VIEW', 'PLATFORM_CELL_MANAGE', 'PLATFORM_BILLING_VIEW', 'PLATFORM_AI_MANAGE', 'PLATFORM_BILLING_MANAGE', 'PLATFORM_RELEASE_VIEW', 'PLATFORM_RELEASE_MANAGE', 'PLATFORM_RELEASE_PROMOTE', 'PLATFORM_MIGRATION_VIEW', 'PLATFORM_MIGRATION_APPLY', 'PLATFORM_TENANT_ACCESS', 'TENANT_CONFIGURE', 'TENANT_VIEW', 'TENANT_PUBLISH', 'SCOPE_VIEW', 'SCOPE_MANAGE', 'REGION_CONFIGURE', 'WORKSTATION_CONFIGURE', 'PRODUCT_VIEW', 'PRODUCT_CONFIGURE', 'PRODUCT_APPROVE', 'PRODUCT_PUBLISH', 'PRICE_VIEW', 'PRICE_CONFIGURE', 'EVENT_CONFIGURE', 'PERFORMANCE_CONFIGURE', 'CAPACITY_CONFIGURE', 'ORDER_VIEW', 'ORDER_VIEW_OTHER', 'ORDER_CREATE', 'ORDER_MODIFY', 'ORDER_DISCOUNT', 'ORDER_CANCEL', 'ORDER_VOID', 'ORDER_REFUND', 'ORDER_REFUND_APPROVE', 'ORDER_REFUND_BULK', 'ORDER_EXCHANGE', 'ORDER_RESCHEDULE', 'ORDER_REPRINT', 'PRICE_OVERRIDE', 'DISCOUNT_APPLY', 'CREDIT_MANAGE', 'CREDIT_OVERRIDE', 'WALLET_VIEW', 'WALLET_OPERATE', 'WALLET_CONFIGURE', 'PAYMENT_VIEW', 'PAYMENT_CONFIGURE', 'PAYMENT_PROVIDER_MANAGE', 'PAYMENT_DISPUTE', 'SHIFT_OPEN', 'SHIFT_CLOSE', 'SHIFT_SUSPEND', 'SHIFT_CLOSE_OTHER', 'SHIFT_APPROVE_OPEN', 'SHIFT_APPROVE_CLOSE', 'SHIFT_REOPEN', 'CASH_LIFT', 'CASH_ADD', 'CASH_NO_SALE', 'DEPOSIT_BOX_MODIFY_OWN', 'DEPOSIT_BOX_MODIFY_OTHER', 'OVERSHORT_ACCEPT', 'ACCESS_VALIDATE', 'ACCESS_OVERRIDE', 'ACCESS_POINT_CONFIGURE', 'TURNSTILE_MODE_SET', 'TICKET_LOOKUP', 'ACCREDITATION_VIEW', 'ACCREDITATION_APPLY', 'ACCREDITATION_APPROVE', 'ACCREDITATION_ISSUE', 'ACCREDITATION_MANAGE', 'ACCREDITATION_CONFIGURE', 'REPORT_VIEW_OWN', 'REPORT_VIEW_WORKSTATION', 'REPORT_VIEW_VENUE', 'REPORT_VIEW_REGION', 'REPORT_VIEW_TENANT', 'REPORT_EXPORT', 'REPORT_EXPORT_PII', 'REPORT_MANAGE', 'REPORT_SCHEDULE', 'LEDGER_VIEW', 'LEDGER_POST', 'LEDGER_APPROVE', 'TAX_CONFIGURE', 'ACCOUNT_CONFIGURE', 'SETTLEMENT_VIEW', 'SETTLEMENT_RECONCILE', 'GUEST_VIEW', 'GUEST_VIEW_PII', 'GUEST_MANAGE', 'VENUE_MAP_VIEW', 'VENUE_MAP_MANAGE', 'VENUE_MAP_PUBLISH', 'RESOURCE_VIEW', 'RESOURCE_BOOK', 'RESOURCE_MANAGE', 'RESOURCE_CONFIGURE', 'RENTAL_VIEW', 'RENTAL_BOOK', 'RENTAL_OPERATE', 'RENTAL_MANAGE', 'RENTAL_CONFIGURE', 'RENTAL_PRICE', 'RENTAL_APPROVE', 'RENTAL_OVERRIDE', 'DEVELOPER_VIEW', 'DEVELOPER_MANAGE', 'DEVELOPER_ADMIN', 'LOYALTY_ACCRUE', 'LOYALTY_REDEEM', 'LOYALTY_ADJUST', 'MARKETING_VIEW', 'MARKETING_MANAGE', 'MARKETING_SEND', 'CASE_VIEW', 'CASE_MANAGE', 'ASSET_LIBRARY_VIEW', 'ASSET_LIBRARY_MANAGE', 'ASSET_LIBRARY_APPROVE', 'ASSET_LIBRARY_SHARE', 'QUEUE_VIEW', 'QUEUE_MANAGE', 'QUEUE_REDEEM', 'QUEUE_OVERRIDE', 'TRANSPORT_VIEW', 'TRANSPORT_MANAGE', 'TRANSPORT_PRICE', 'ASSET_VIEW', 'ASSET_MANAGE', 'WORK_ORDER_VIEW', 'WORK_ORDER_MANAGE', 'WORK_ORDER_VERIFY', 'INSPECTION_VIEW', 'INSPECTION_SUBMIT', 'INSPECTION_MANAGE', 'INCIDENT_REPORT', 'INCIDENT_VIEW', 'INCIDENT_MANAGE', 'KIOSK_ATTEND', 'DEVICE_VIEW', 'DEVICE_CONFIGURE', 'DEVICE_MANAGE', 'APPROVAL_ACT', 'APPROVAL_DELEGATE', 'AI_USE', 'AI_CONFIGURE', 'AI_APPROVE', 'AI_AUDIT_VIEW', 'RISK_REVIEW', 'RISK_INVESTIGATE', 'AUDIT_VIEW', 'APPROVAL_VIEW', 'APPROVAL_REQUEST', 'APPROVAL_DECIDE', 'APPROVAL_CONFIGURE', 'MAINTENANCE_EXECUTE', 'MAINTENANCE_APPROVE', 'WORKFORCE_VIEW', 'WORKFORCE_MANAGE', 'ATTENDANCE_RECORD', 'ANNOUNCEMENT_PUBLISH', 'ANNOUNCEMENT_EMERGENCY', 'PARTNER_VIEW', 'PARTNER_MANAGE', 'PARKING_CONFIGURE', 'PAYMENT_VOID', 'PROCUREMENT_VIEW', 'PROCUREMENT_REQUEST', 'PROCUREMENT_MANAGE', 'PROCUREMENT_RECEIVE', 'CORE_AI_PUBLISH', 'TICKETING_AI_PUBLISH', 'ACCESS_AI_PUBLISH', 'FNB_AI_PUBLISH', 'RETAIL_AI_PUBLISH', 'INVENTORY_AI_PUBLISH', 'SEATING_AI_PUBLISH', 'MEMBERSHIP_AI_PUBLISH', 'MARKETING_AI_PUBLISH', 'RESOURCES_AI_PUBLISH', 'QUEUE_AI_PUBLISH', 'TRANSPORT_AI_PUBLISH', 'GAMES_AI_PUBLISH', 'MAINTENANCE_AI_PUBLISH', 'ACCREDITATION_AI_PUBLISH', 'PARTNER_AI_PUBLISH', 'ANALYTICS_AI_PUBLISH', 'BIOMETRIC_IMAGE_VIEW', 'ACCESS_DIRECTION_SET', 'REPORT_GOVERNANCE_MANAGE')) NOT VALID;
-- ALTER TABLE reporting.dashboard DROP CONSTRAINT IF EXISTS dashboard_module_chk; ALTER TABLE reporting.dashboard ADD CONSTRAINT dashboard_module_chk CHECK (module IN ('core', 'ticketing', 'access', 'fnb', 'retail', 'inventory', 'seating', 'membership', 'marketing', 'resources', 'queue', 'transport', 'games', 'maintenance', 'accreditation', 'partner', 'developerApi', 'analytics', 'ai')) NOT VALID;
-- ALTER TABLE promotions.bundle DROP COLUMN IF EXISTS variant_id;
-- ALTER TABLE platform.workstation DROP COLUMN IF EXISTS configuration_profile_version;
-- ALTER TABLE platform.workstation ALTER COLUMN sale_board SET NOT NULL;
-- ALTER TABLE platform.venue_settings DROP COLUMN IF EXISTS contact;
-- DROP TABLE IF EXISTS platform.outbox_sequence;
-- ALTER TABLE platform.outbox DROP COLUMN IF EXISTS occurred_at;
-- ALTER TABLE platform.dead_letter DROP COLUMN IF EXISTS sequence;
-- ALTER TABLE platform.dead_letter DROP COLUMN IF EXISTS aggregate_id;
-- ALTER TABLE platform.dead_letter DROP COLUMN IF EXISTS aggregate_type;
-- ALTER TABLE platform.dead_letter DROP COLUMN IF EXISTS tenant_id;
-- ALTER TABLE platform.dead_letter DROP COLUMN IF EXISTS event_id;
-- ALTER TABLE platform.audit_read DROP COLUMN IF EXISTS record_count;
-- ALTER TABLE platform.audit_read DROP COLUMN IF EXISTS filter;
-- ALTER TABLE platform.audit_read DROP COLUMN IF EXISTS target;
-- ALTER TABLE platform.audit_read DROP COLUMN IF EXISTS read_at;
-- ALTER TABLE platform.audit_read ALTER COLUMN subject_id SET NOT NULL;
-- DROP TABLE IF EXISTS pii.subject_identity;
-- ALTER TABLE payments.token DROP COLUMN IF EXISTS revoked_at;
-- ALTER TABLE payments.provider_event DROP COLUMN IF EXISTS provider_connection_id;
-- ALTER TABLE payments.provider_connection DROP COLUMN IF EXISTS provider_id;
-- ALTER TABLE payments.method_config ALTER COLUMN payment_policy_id SET NOT NULL;
-- ALTER TABLE payments.fee_rule ALTER COLUMN payment_policy_id SET NOT NULL;
-- ALTER TABLE payments.eligibility_rule ALTER COLUMN payment_policy_id SET NOT NULL;
-- ALTER TABLE payments.currency_rule ALTER COLUMN payment_policy_id SET NOT NULL;
-- ALTER TABLE orders.order_event DROP CONSTRAINT IF EXISTS order_event_reservation_id_when_chk;
-- ALTER TABLE orders.order_event ALTER COLUMN order_id SET NOT NULL;
-- ALTER TABLE orders.group_booking DROP COLUMN IF EXISTS performance_id;
-- ALTER TABLE orders.cart DROP COLUMN IF EXISTS workstation_id;
-- ALTER TABLE orders.cart DROP COLUMN IF EXISTS session_id;
-- ALTER TABLE marketing.privacy_exception DROP CONSTRAINT IF EXISTS privacy_exception_system_chk; ALTER TABLE marketing.privacy_exception ADD CONSTRAINT privacy_exception_system_chk CHECK (system IN ('core', 'ticketing', 'access', 'fnb', 'retail', 'inventory', 'seating', 'membership', 'marketing', 'resources', 'queue', 'transport', 'games', 'maintenance', 'accreditation', 'partner', 'developerApi', 'analytics', 'ai')) NOT VALID;
-- ALTER TABLE marketing.privacy_audit_event DROP CONSTRAINT IF EXISTS privacy_audit_event_source_chk; ALTER TABLE marketing.privacy_audit_event ADD CONSTRAINT privacy_audit_event_source_chk CHECK (source IN ('core', 'ticketing', 'access', 'fnb', 'retail', 'inventory', 'seating', 'membership', 'marketing', 'resources', 'queue', 'transport', 'games', 'maintenance', 'accreditation', 'partner', 'developerApi', 'analytics', 'ai')) NOT VALID;
-- ALTER TABLE marketing.guest_device DROP COLUMN IF EXISTS pending_session_end_installation_id;
-- ALTER TABLE marketing.guest_device DROP CONSTRAINT IF EXISTS guest_device_token_fingerprint_chk;
-- DROP TABLE IF EXISTS marketing.form_submission_sale_link;
-- ALTER TABLE marketing.form_definition_field DROP COLUMN IF EXISTS presentation;
-- ALTER TABLE marketing.customer_badge DROP CONSTRAINT IF EXISTS customer_badge_status_chk; ALTER TABLE marketing.customer_badge ADD CONSTRAINT customer_badge_status_chk CHECK (char_length(status) <= 20) NOT VALID;
-- ALTER TABLE marketing.customer_badge DROP CONSTRAINT IF EXISTS customer_badge_source_type_chk; ALTER TABLE marketing.customer_badge ADD CONSTRAINT customer_badge_source_type_chk CHECK (char_length(source_type) <= 30) NOT VALID;
-- ALTER TABLE marketing.cookie_scan_policy DROP CONSTRAINT IF EXISTS cookie_scan_policy_frequency_chk;
-- ALTER TABLE marketing.consent_record DROP CONSTRAINT IF EXISTS consent_record_purpose_chk; ALTER TABLE marketing.consent_record ADD CONSTRAINT consent_record_purpose_chk CHECK (purpose IN ('marketing', 'personalisation', 'profiling', 'thirdPartySharing', 'aiProcessing', 'transactional')) NOT VALID;
-- ALTER TABLE marketing.consent_purpose DROP CONSTRAINT IF EXISTS consent_purpose_purpose_chk; ALTER TABLE marketing.consent_purpose ADD CONSTRAINT consent_purpose_purpose_chk CHECK (purpose IN ('marketing', 'personalisation', 'profiling', 'thirdPartySharing', 'aiProcessing', 'transactional')) NOT VALID;
-- ALTER TABLE ledger.posting DROP CONSTRAINT IF EXISTS posting_source_chk; ALTER TABLE ledger.posting ADD CONSTRAINT posting_source_chk CHECK (source IN ('manual', 'order', 'refund', 'void', 'shift', 'recognition', 'settlement', 'variance', 'reversal', 'writeOff', 'chargeback')) NOT VALID;
-- ALTER TABLE ledger.journal_entry DROP CONSTRAINT IF EXISTS journal_entry_source_chk; ALTER TABLE ledger.journal_entry ADD CONSTRAINT journal_entry_source_chk CHECK (source IN ('manual', 'order', 'refund', 'void', 'shift', 'recognition', 'settlement', 'variance', 'reversal', 'writeOff', 'chargeback')) NOT VALID;
-- ALTER TABLE ledger.journal_entry DROP COLUMN IF EXISTS legal_entity_id;
-- ALTER TABLE ledger.account_mapping DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE identity.sso_provider DROP COLUMN IF EXISTS allowed_redirect_uris;
-- ALTER TABLE identity.sso_provider DROP COLUMN IF EXISTS default_home_scope_id;
-- ALTER TABLE identity.sso_provider DROP COLUMN IF EXISTS groups_claim;
-- ALTER TABLE identity.sso_provider DROP COLUMN IF EXISTS display_name_claim;
-- ALTER TABLE identity.sso_provider DROP COLUMN IF EXISTS username_claim;
-- ALTER TABLE identity.session DROP COLUMN IF EXISTS working_venue_id;
-- ALTER TABLE identity.session DROP COLUMN IF EXISTS end_reason;
-- ALTER TABLE identity.session DROP COLUMN IF EXISTS ended_by_principal_id;
-- ALTER TABLE identity.session DROP COLUMN IF EXISTS ended_at;
-- ALTER TABLE identity.role_permission DROP CONSTRAINT IF EXISTS role_permission_permission_chk; ALTER TABLE identity.role_permission ADD CONSTRAINT role_permission_permission_chk CHECK (permission IN ('SESSION_FORCE_LOGOUT', 'USER_MANAGE', 'ROLE_MANAGE', 'PERMISSION_GRANT', 'PERMISSION_VIEW', 'PERMISSION_MANAGE', 'PLATFORM_TENANT_VIEW', 'PLATFORM_TENANT_MANAGE', 'PLATFORM_TENANT_TERMINATE', 'PLATFORM_PLAN_MANAGE', 'PLATFORM_CELL_VIEW', 'PLATFORM_CELL_MANAGE', 'PLATFORM_BILLING_VIEW', 'PLATFORM_AI_MANAGE', 'PLATFORM_BILLING_MANAGE', 'PLATFORM_RELEASE_VIEW', 'PLATFORM_RELEASE_MANAGE', 'PLATFORM_RELEASE_PROMOTE', 'PLATFORM_MIGRATION_VIEW', 'PLATFORM_MIGRATION_APPLY', 'PLATFORM_TENANT_ACCESS', 'TENANT_CONFIGURE', 'TENANT_VIEW', 'TENANT_PUBLISH', 'SCOPE_VIEW', 'SCOPE_MANAGE', 'REGION_CONFIGURE', 'WORKSTATION_CONFIGURE', 'PRODUCT_VIEW', 'PRODUCT_CONFIGURE', 'PRODUCT_APPROVE', 'PRODUCT_PUBLISH', 'PRICE_VIEW', 'PRICE_CONFIGURE', 'EVENT_CONFIGURE', 'PERFORMANCE_CONFIGURE', 'CAPACITY_CONFIGURE', 'ORDER_VIEW', 'ORDER_VIEW_OTHER', 'ORDER_CREATE', 'ORDER_MODIFY', 'ORDER_DISCOUNT', 'ORDER_CANCEL', 'ORDER_VOID', 'ORDER_REFUND', 'ORDER_REFUND_APPROVE', 'ORDER_REFUND_BULK', 'ORDER_EXCHANGE', 'ORDER_RESCHEDULE', 'ORDER_REPRINT', 'PRICE_OVERRIDE', 'DISCOUNT_APPLY', 'CREDIT_MANAGE', 'CREDIT_OVERRIDE', 'WALLET_VIEW', 'WALLET_OPERATE', 'WALLET_CONFIGURE', 'PAYMENT_VIEW', 'PAYMENT_CONFIGURE', 'PAYMENT_PROVIDER_MANAGE', 'PAYMENT_DISPUTE', 'SHIFT_OPEN', 'SHIFT_CLOSE', 'SHIFT_SUSPEND', 'SHIFT_CLOSE_OTHER', 'SHIFT_APPROVE_OPEN', 'SHIFT_APPROVE_CLOSE', 'SHIFT_REOPEN', 'CASH_LIFT', 'CASH_ADD', 'CASH_NO_SALE', 'DEPOSIT_BOX_MODIFY_OWN', 'DEPOSIT_BOX_MODIFY_OTHER', 'OVERSHORT_ACCEPT', 'ACCESS_VALIDATE', 'ACCESS_OVERRIDE', 'ACCESS_POINT_CONFIGURE', 'TURNSTILE_MODE_SET', 'TICKET_LOOKUP', 'ACCREDITATION_VIEW', 'ACCREDITATION_APPLY', 'ACCREDITATION_APPROVE', 'ACCREDITATION_ISSUE', 'ACCREDITATION_MANAGE', 'ACCREDITATION_CONFIGURE', 'REPORT_VIEW_OWN', 'REPORT_VIEW_WORKSTATION', 'REPORT_VIEW_VENUE', 'REPORT_VIEW_REGION', 'REPORT_VIEW_TENANT', 'REPORT_EXPORT', 'REPORT_EXPORT_PII', 'REPORT_MANAGE', 'REPORT_SCHEDULE', 'LEDGER_VIEW', 'LEDGER_POST', 'LEDGER_APPROVE', 'TAX_CONFIGURE', 'ACCOUNT_CONFIGURE', 'SETTLEMENT_VIEW', 'SETTLEMENT_RECONCILE', 'GUEST_VIEW', 'GUEST_VIEW_PII', 'GUEST_MANAGE', 'VENUE_MAP_VIEW', 'VENUE_MAP_MANAGE', 'VENUE_MAP_PUBLISH', 'RESOURCE_VIEW', 'RESOURCE_BOOK', 'RESOURCE_MANAGE', 'RESOURCE_CONFIGURE', 'RENTAL_VIEW', 'RENTAL_BOOK', 'RENTAL_OPERATE', 'RENTAL_MANAGE', 'RENTAL_CONFIGURE', 'RENTAL_PRICE', 'RENTAL_APPROVE', 'RENTAL_OVERRIDE', 'DEVELOPER_VIEW', 'DEVELOPER_MANAGE', 'DEVELOPER_ADMIN', 'LOYALTY_ACCRUE', 'LOYALTY_REDEEM', 'LOYALTY_ADJUST', 'MARKETING_VIEW', 'MARKETING_MANAGE', 'MARKETING_SEND', 'CASE_VIEW', 'CASE_MANAGE', 'ASSET_LIBRARY_VIEW', 'ASSET_LIBRARY_MANAGE', 'ASSET_LIBRARY_APPROVE', 'ASSET_LIBRARY_SHARE', 'QUEUE_VIEW', 'QUEUE_MANAGE', 'QUEUE_REDEEM', 'QUEUE_OVERRIDE', 'TRANSPORT_VIEW', 'TRANSPORT_MANAGE', 'TRANSPORT_PRICE', 'ASSET_VIEW', 'ASSET_MANAGE', 'WORK_ORDER_VIEW', 'WORK_ORDER_MANAGE', 'WORK_ORDER_VERIFY', 'INSPECTION_VIEW', 'INSPECTION_SUBMIT', 'INSPECTION_MANAGE', 'INCIDENT_REPORT', 'INCIDENT_VIEW', 'INCIDENT_MANAGE', 'KIOSK_ATTEND', 'DEVICE_VIEW', 'DEVICE_CONFIGURE', 'DEVICE_MANAGE', 'APPROVAL_ACT', 'APPROVAL_DELEGATE', 'AI_USE', 'AI_CONFIGURE', 'AI_APPROVE', 'AI_AUDIT_VIEW', 'RISK_REVIEW', 'RISK_INVESTIGATE', 'AUDIT_VIEW', 'APPROVAL_VIEW', 'APPROVAL_REQUEST', 'APPROVAL_DECIDE', 'APPROVAL_CONFIGURE', 'MAINTENANCE_EXECUTE', 'MAINTENANCE_APPROVE', 'WORKFORCE_VIEW', 'WORKFORCE_MANAGE', 'ATTENDANCE_RECORD', 'ANNOUNCEMENT_PUBLISH', 'ANNOUNCEMENT_EMERGENCY', 'PARTNER_VIEW', 'PARTNER_MANAGE', 'PARKING_CONFIGURE', 'PAYMENT_VOID', 'PROCUREMENT_VIEW', 'PROCUREMENT_REQUEST', 'PROCUREMENT_MANAGE', 'PROCUREMENT_RECEIVE', 'CORE_AI_PUBLISH', 'TICKETING_AI_PUBLISH', 'ACCESS_AI_PUBLISH', 'FNB_AI_PUBLISH', 'RETAIL_AI_PUBLISH', 'INVENTORY_AI_PUBLISH', 'SEATING_AI_PUBLISH', 'MEMBERSHIP_AI_PUBLISH', 'MARKETING_AI_PUBLISH', 'RESOURCES_AI_PUBLISH', 'QUEUE_AI_PUBLISH', 'TRANSPORT_AI_PUBLISH', 'GAMES_AI_PUBLISH', 'MAINTENANCE_AI_PUBLISH', 'ACCREDITATION_AI_PUBLISH', 'PARTNER_AI_PUBLISH', 'ANALYTICS_AI_PUBLISH', 'BIOMETRIC_IMAGE_VIEW', 'ACCESS_DIRECTION_SET', 'REPORT_GOVERNANCE_MANAGE')) NOT VALID;
-- DROP TABLE IF EXISTS identity.principal_external_identity;
-- ALTER TABLE identity.password_policy DROP COLUMN IF EXISTS session_max_hours;
-- ALTER TABLE identity.password_policy DROP COLUMN IF EXISTS refresh_token_hours;
-- ALTER TABLE identity.password_policy DROP COLUMN IF EXISTS access_token_minutes;
-- ALTER TABLE identity.otp_challenge ALTER COLUMN subject_id SET NOT NULL;
-- DROP TABLE IF EXISTS identity.open_shift_marker;
-- ALTER TABLE identity.mfa_recovery_code DROP CONSTRAINT IF EXISTS mfa_recovery_code_principal_id_subject_id_one_chk;
-- ALTER TABLE identity.mfa_recovery_code DROP COLUMN IF EXISTS subject_id;
-- ALTER TABLE identity.mfa_method DROP CONSTRAINT IF EXISTS mfa_method_principal_id_subject_id_one_chk;
-- ALTER TABLE identity.mfa_method DROP COLUMN IF EXISTS pending_expires_at;
-- ALTER TABLE identity.mfa_method DROP COLUMN IF EXISTS destination;
-- ALTER TABLE identity.mfa_method DROP COLUMN IF EXISTS secret;
-- ALTER TABLE identity.mfa_method DROP COLUMN IF EXISTS subject_id;
-- ALTER TABLE identity.mfa_challenge DROP CONSTRAINT IF EXISTS mfa_challenge_principal_id_subject_id_one_chk;
-- ALTER TABLE identity.mfa_challenge DROP COLUMN IF EXISTS subject_id;
-- ALTER TABLE identity.mfa_challenge ALTER COLUMN principal_id SET NOT NULL;
-- ALTER TABLE identity.guest_identity_verification DROP COLUMN IF EXISTS selfie_upload_id;
-- ALTER TABLE identity.delegated_access DROP CONSTRAINT IF EXISTS delegated_access_permission_role_id_one_chk;
-- ALTER TABLE identity.delegated_access DROP CONSTRAINT IF EXISTS delegated_access_granted_by_subject_id_when_chk;
-- ALTER TABLE identity.delegated_access DROP CONSTRAINT IF EXISTS delegated_access_granted_by_principal_id_when_chk;
-- ALTER TABLE identity.delegated_access ALTER COLUMN permission SET NOT NULL;
-- ALTER TABLE identity.delegated_access DROP COLUMN IF EXISTS granted_by_subject_id;
-- ALTER TABLE identity.delegated_access ALTER COLUMN granted_by_principal_id SET NOT NULL;
-- ALTER TABLE identity.delegated_access DROP COLUMN IF EXISTS granted_by_kind;
-- ALTER TABLE fnb.delivery_location DROP COLUMN IF EXISTS closes_at;
-- ALTER TABLE fnb.delivery_location DROP COLUMN IF EXISTS opens_at;
-- ALTER TABLE catalogue.published_bundle DROP COLUMN IF EXISTS published_by;
-- ALTER TABLE catalogue.published_bundle DROP COLUMN IF EXISTS published_at;
-- DROP TABLE IF EXISTS catalogue.product_tag;
-- DROP TABLE IF EXISTS catalogue.product_sale_permission;
-- DROP TABLE IF EXISTS catalogue.product_owner_form;
-- DROP TABLE IF EXISTS catalogue.product_channel_text;
-- ALTER TABLE catalogue.group_package DROP CONSTRAINT IF EXISTS group_package_kind_chk; ALTER TABLE catalogue.group_package ADD CONSTRAINT group_package_kind_chk CHECK (kind IN ('school', 'party')) NOT VALID;
-- ALTER TABLE catalogue.group_package DROP COLUMN IF EXISTS minimum_size;
-- DROP TABLE IF EXISTS catalogue.bundle_application;
-- ALTER TABLE assets.media_usage DROP CONSTRAINT IF EXISTS media_usage_surface_chk; ALTER TABLE assets.media_usage ADD CONSTRAINT media_usage_surface_chk CHECK (surface IN ('tenantBranding', 'homepageBanner', 'promoBlock', 'contentPage', 'product', 'event', 'menuItem', 'merchandise', 'workOrder', 'incident', 'inspection', 'campaign')) NOT VALID;
-- ALTER TABLE assets.media_asset DROP COLUMN IF EXISTS released_at;
-- ALTER TABLE assets.media_asset DROP COLUMN IF EXISTS released_by_principal_id;
-- ALTER TABLE assets.media_asset DROP COLUMN IF EXISTS extracted_text;
-- DROP TABLE IF EXISTS assets.guest_upload;
-- ALTER TABLE assets.asset_version DROP COLUMN IF EXISTS content_type;
-- ALTER TABLE assets.asset_version DROP COLUMN IF EXISTS storage_key;
-- ALTER TABLE approvals.request DROP COLUMN IF EXISTS cancel_reason;
-- ALTER TABLE approvals.request DROP COLUMN IF EXISTS rule_id;
-- ALTER TABLE approvals.request DROP COLUMN IF EXISTS approval_matrix_id;
-- ALTER TABLE approvals.request DROP COLUMN IF EXISTS assignment_note;
-- ALTER TABLE approvals.request DROP COLUMN IF EXISTS attributes;
-- ALTER TABLE approvals.external_dispatch DROP COLUMN IF EXISTS requester_reference;
-- ALTER TABLE approvals.decision DROP CONSTRAINT IF EXISTS decision_principal_id_external_approver_ref_one_chk;
-- ALTER TABLE approvals.decision DROP CONSTRAINT IF EXISTS decision_decision_chk; ALTER TABLE approvals.decision ADD CONSTRAINT decision_decision_chk CHECK (decision IN ('approve', 'reject')) NOT VALID;
-- ALTER TABLE approvals.decision DROP COLUMN IF EXISTS external_approver_name;
-- ALTER TABLE approvals.decision DROP COLUMN IF EXISTS external_approver_ref;
-- ALTER TABLE approvals.decision ALTER COLUMN principal_id SET NOT NULL;
-- DROP TABLE IF EXISTS ai.vector_store;
-- DROP TABLE IF EXISTS ai.translation_job;
-- ALTER TABLE ai.proposed_action DROP COLUMN IF EXISTS draft_text;
-- ALTER TABLE ai.proposed_action DROP COLUMN IF EXISTS field_path;
-- ALTER TABLE ai.proposed_action DROP COLUMN IF EXISTS locale;
-- ALTER TABLE ai.proposed_action DROP COLUMN IF EXISTS target_ref;
-- ALTER TABLE ai.proposed_action DROP COLUMN IF EXISTS target_kind;
-- ALTER TABLE ai.policy DROP COLUMN IF EXISTS glossary_terms;
-- DROP TABLE IF EXISTS ai.outbox_sequence;
-- DROP TABLE IF EXISTS ai.outbox;
-- ALTER TABLE ai.index_source DROP COLUMN IF EXISTS kind;
-- ALTER TABLE ai.decision_record DROP COLUMN IF EXISTS hash_version;
-- ALTER TABLE ai.conversation DROP CONSTRAINT IF EXISTS conversation_principal_id_subject_id_one_chk;
-- ALTER TABLE ai.conversation DROP CONSTRAINT IF EXISTS conversation_module_chk; ALTER TABLE ai.conversation ADD CONSTRAINT conversation_module_chk CHECK (module IN ('core', 'ticketing', 'access', 'fnb', 'retail', 'inventory', 'seating', 'membership', 'marketing', 'resources', 'queue', 'transport', 'games', 'maintenance', 'accreditation', 'partner', 'developerApi', 'analytics', 'ai')) NOT VALID;
-- ALTER TABLE ai.conversation DROP COLUMN IF EXISTS profile_key;
-- ALTER TABLE ai.conversation DROP COLUMN IF EXISTS subject_id;
-- ALTER TABLE ai.conversation ALTER COLUMN principal_id SET NOT NULL;
-- ALTER TABLE ai.chunk_embedding DROP COLUMN IF EXISTS subject_id;
-- ALTER TABLE ai.activity DROP CONSTRAINT IF EXISTS activity_subject_id_when_chk;
-- ALTER TABLE ai.activity DROP CONSTRAINT IF EXISTS activity_principal_id_when_chk;
-- ALTER TABLE ai.activity ALTER COLUMN principal_id SET NOT NULL;
-- ALTER TABLE access.gate_mode_change DROP COLUMN IF EXISTS cancel_reason;
-- ALTER TABLE access.gate_mode_change DROP COLUMN IF EXISTS cancelled_at;
-- ALTER TABLE access.gate_mode_change DROP COLUMN IF EXISTS cancelled_by_principal_id;
-- ALTER TABLE access.access_point DROP COLUMN IF EXISTS access_area_id;
-- DELETE FROM platform.schema_version WHERE version = 'V0108';
