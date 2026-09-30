-- identity — 31 tables
-- **Derived. Do not hand-edit.**

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.access_decision (
    id                                uuid PRIMARY KEY,
    effect                            text CONSTRAINT access_decision_effect_chk CHECK (effect IN ('permit', 'deny')),
    decided_at                        timestamptz,
    decided_by                        text CONSTRAINT access_decision_decided_by_chk CHECK (decided_by IN ('central', 'deviceBundle')),
    principal_id                      uuid,
    permission                        text,
    scope_path                        ltree NOT NULL,
    observed_attributes               jsonb,
    override_id                       uuid,
    latency_ms                        integer,
    scope_path_index                  text
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.access_override (
    id                                uuid PRIMARY KEY,
    principal_id                      uuid,
    scope_path                        ltree NOT NULL,
    permissions                       text[],
    reason                            text,
    created_by                        uuid,
    created_at                        timestamptz,
    expires_at                        timestamptz,
    revoked_at                        timestamptz,
    alerted_to                        text[]
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.access_policy (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    description                       text,
    is_template                       boolean DEFAULT false,
    permissions                       text[],
    combining                         text DEFAULT 'allMustMatch' CONSTRAINT access_policy_combining_chk CHECK (combining IN ('allMustMatch', 'anyMayMatch')),
    effect                            text NOT NULL CONSTRAINT access_policy_effect_chk CHECK (effect IN ('permit', 'deny')),
    priority                          integer DEFAULT 0,
    scope_path                        ltree NOT NULL,
    applies_to_role_ids               text[],
    status                            text CONSTRAINT access_policy_status_chk CHECK (status IN ('draft', 'pendingApproval', 'active', 'suspended', 'retired')),
    version                           integer DEFAULT 1,
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    delegated_admin_role_ids          text[]
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.access_policy_version (
    policy_id                         uuid,
    version                           integer,
    changed_by                        uuid,
    changed_at                        timestamptz,
    reason                            text,
    approved_by                       uuid,
    previous_id                       uuid,
    current_id                        uuid,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.access_review_campaign (
    id                                uuid PRIMARY KEY,
    name                              text NOT NULL CONSTRAINT access_review_campaign_name_chk CHECK (char_length(name) <= 200),
    scope_path                        ltree NOT NULL,
    role_ids                          text[],
    reviewer_mode                     text NOT NULL CONSTRAINT access_review_campaign_reviewer_mode_chk CHECK (reviewer_mode IN ('lineManager', 'named')),
    reviewer_principal_ids            text[],
    due_at                            timestamptz NOT NULL,
    recurrence                        text DEFAULT 'none' CONSTRAINT access_review_campaign_recurrence_chk CHECK (recurrence IN ('none', 'quarterly', 'semiAnnual', 'annual')),
    prefill_from_findings             boolean DEFAULT true,
    lookback_days                     integer DEFAULT 90,
    status                            text CONSTRAINT access_review_campaign_status_chk CHECK (status IN ('open', 'completed', 'expired')),
    item_count                        integer,
    decided_count                     integer,
    revoked_count                     integer,
    created_by_principal_id           uuid,
    created_at                        timestamptz,
    closed_at                         timestamptz
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.access_review_item (
    id                                uuid PRIMARY KEY,
    campaign_id                       uuid NOT NULL,
    delegated_access_id               uuid NOT NULL,
    principal_id                      uuid NOT NULL,
    role_id                           uuid,
    scope_path                        ltree NOT NULL,
    reviewer_principal_id             uuid,
    finding_kind                      text DEFAULT 'none' CONSTRAINT access_review_item_finding_kind_chk CHECK (finding_kind IN ('none', 'excessive', 'conflicting')),
    last_used_at                      timestamptz,
    recommendation                    text CONSTRAINT access_review_item_recommendation_chk CHECK (recommendation IN ('certify', 'revoke', 'review')),
    status                            text NOT NULL CONSTRAINT access_review_item_status_chk CHECK (status IN ('pending', 'certified', 'revoked', 'notReviewed')),
    decided_by_principal_id           uuid,
    decided_at                        timestamptz,
    reason                            text CONSTRAINT access_review_item_reason_chk CHECK (char_length(reason) <= 1000)
);

-- Written by the authorisation layer on every call, not by an operation Hangs off: reaches
-- identity.principal through its keys; references identity.principal. Reached by: 1 operations
-- read it and 1 write it.
CREATE TABLE IF NOT EXISTS identity.authz_audit (
    id                                uuid PRIMARY KEY NOT NULL,
    actor_principal_id                uuid,
    subject_principal_id              uuid
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.benefit_usage (
    id                                uuid PRIMARY KEY,
    customer_membership_id            uuid NOT NULL,
    membership_benefit_id             uuid NOT NULL,
    quantity                          numeric(18,4) NOT NULL,
    source_type                       text CONSTRAINT benefit_usage_source_type_chk CHECK (char_length(source_type) <= 30),
    source_order_id                   uuid,
    used_at                           timestamptz NOT NULL,
    remaining_quantity                numeric(18,4),
    notes                             text CONSTRAINT benefit_usage_notes_chk CHECK (char_length(notes) <= 500)
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.capability_template (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL CONSTRAINT capability_template_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT capability_template_name_chk CHECK (char_length(name) <= 200),
    description                       text,
    capabilities                      text[] NOT NULL,
    scope_path                        ltree NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.customer_membership (
    id                                uuid PRIMARY KEY,
    customer_id                       uuid NOT NULL,
    entitlement_template_id           uuid NOT NULL,
    number                            text NOT NULL CONSTRAINT customer_membership_number_chk CHECK (char_length(number) <= 50),
    source_order_id                   uuid,
    start_at                          timestamptz NOT NULL,
    expires_at                        timestamptz,
    status                            text NOT NULL CONSTRAINT customer_membership_status_chk CHECK (char_length(status) <= 30),
    is_auto_renew                     boolean NOT NULL,
    cancelled_at                      timestamptz,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- One person acting for another, or for a scope they do not own. A parent managing a child's
-- membership, a manager covering another venue for a week. Renamed from grant, which is a verb, a
-- subsidy and a permission depending on who reads it
CREATE TABLE IF NOT EXISTS identity.delegated_access (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid,
    role_id                           uuid,
    permission                        text NOT NULL,
    subject_id                        uuid,
    over_subject_id                   uuid,
    over_object_ref                   text,
    delegation_kind                   text CONSTRAINT delegated_access_delegation_kind_chk CHECK (delegation_kind IN ('primaryHolder', 'familyMember', 'groupLeader', 'attendee', 'corporateAdmin', 'corporateMember', 'carer')),
    quota                             integer,
    is_revocable_by_subject           boolean DEFAULT true,
    scope_path                        ltree NOT NULL,
    effect                            text NOT NULL CONSTRAINT delegated_access_effect_chk CHECK (effect IN ('ALLOW', 'DENY')),
    permission_id                     uuid,
    revoked_at                        timestamptz,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    created_by_principal_id           uuid,
    created_at                        timestamptz,
    granted_by_principal_id           uuid NOT NULL,
    revoked_by_principal_id           uuid,
    scope_id                          uuid NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.guest_identity_verification (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    subject_document_id               uuid,
    document_kind                     text CONSTRAINT guest_identity_verification_document_kind_chk CHECK (document_kind IN ('passport', 'emiratesId', 'nationalId', 'drivingLicence', 'residencePermit', 'other')),
    document_number_last4             text CONSTRAINT guest_identity_verification_document_number_last4_chk CHECK (char_length(document_number_last4) <= 4),
    reason                            text CONSTRAINT guest_identity_verification_reason_chk CHECK (reason IN ('policyRequired', 'ageRestrictedPurchase', 'residentPricing', 'accountRecovery')),
    status                            text NOT NULL CONSTRAINT guest_identity_verification_status_chk CHECK (status IN ('pending', 'verified', 'rejected', 'resubmissionRequested')),
    method                            text CONSTRAINT guest_identity_verification_method_chk CHECK (method IN ('manualReview', 'documentScanner', 'provider')),
    decision_reason                   text CONSTRAINT guest_identity_verification_decision_reason_chk CHECK (char_length(decision_reason) <= 300),
    decided_by_principal_id           uuid,
    submitted_at                      timestamptz NOT NULL,
    decided_at                        timestamptz,
    document_image_deleted_at         timestamptz
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.guest_verification_policy (
    id                                uuid PRIMARY KEY,
    scope_path                        ltree NOT NULL,
    registration_requires             text[] NOT NULL,
    id_document_required_for          text[],
    wallet_top_up_limit               numeric(18,4),
    accepted_document_kinds           text[],
    uae_pass_satisfies_id_document    boolean DEFAULT true,
    is_social_login_counts_as_email_verified boolean DEFAULT true,
    is_selfie_required                boolean DEFAULT false,
    review_mode                       text DEFAULT 'manual' CONSTRAINT guest_verification_policy_review_mode_chk CHECK (review_mode IN ('manual', 'provider', 'providerThenManual')),
    document_image_retention          text DEFAULT 'deleteOnDecision' CONSTRAINT guest_verification_policy_document_image_retention_chk CHECK (document_image_retention IN ('deleteOnDecision', 'keepUntilDocumentExpiry')),
    max_resubmissions                 integer DEFAULT 3,
    updated_at                        timestamptz
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.membership_history (
    id                                uuid PRIMARY KEY,
    customer_membership_id            uuid NOT NULL,
    from_status                       text CONSTRAINT membership_history_from_status_chk CHECK (char_length(from_status) <= 30),
    to_status                         text NOT NULL CONSTRAINT membership_history_to_status_chk CHECK (char_length(to_status) <= 30),
    reason                            text CONSTRAINT membership_history_reason_chk CHECK (char_length(reason) <= 500),
    changed_by_principal_id           uuid,
    changed_at                        timestamptz NOT NULL,
    interruption_type                 text CONSTRAINT membership_history_interruption_type_chk CHECK (interruption_type IN ('freeze', 'suspension', 'administrativeHold')),
    suspension_reason                 text CONSTRAINT membership_history_suspension_reason_chk CHECK (suspension_reason IN ('paymentIssue', 'membershipMisuse', 'credentialMisuse', 'eligibilityIssue', 'chargeback', 'administrativeReview', 'other')),
    episode_start_date                date,
    episode_end_date                  date,
    validity_treatment                text CONSTRAINT membership_history_validity_treatment_chk CHECK (validity_treatment IN ('extendExpiry', 'doNotExtend')),
    new_expiry_date                   date,
    is_admission_blocked              boolean,
    is_reservations_restricted        boolean,
    is_benefits_restricted            boolean,
    is_renewal_allowed                boolean,
    is_credential_disabled            boolean,
    approval_request_id               uuid,
    ends_episode_history_id           uuid
);

-- an issued MFA challenge and its outcome Hangs off: reaches identity.principal through its keys;
-- references identity.principal. Reached by: 1 operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS identity.mfa_challenge (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid NOT NULL
);

-- A second factor a principal has enrolled. Guests may enrol too, from 26 August
CREATE TABLE IF NOT EXISTS identity.mfa_method (
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT mfa_method_kind_chk CHECK (kind IN ('totp', 'smsOtp', 'emailOtp', 'biometric', 'hardwareToken')),
    label                             text,
    masked_target                     text,
    is_active                         boolean NOT NULL,
    is_primary                        boolean,
    enrolled_at                       timestamptz NOT NULL,
    last_used_at                      timestamptz,
    principal_id                      uuid
);

-- hashed, single-use, never retrievable Hangs off: reaches identity.principal through its keys;
-- references identity.principal. Reached by: 2 operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS identity.mfa_recovery_code (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.module (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL CONSTRAINT module_code_chk CHECK (char_length(code) <= 100),
    name                              text NOT NULL CONSTRAINT module_name_chk CHECK (char_length(name) <= 150),
    description                       text CONSTRAINT module_description_chk CHECK (char_length(description) <= 500),
    parent_module_id                  uuid,
    type                              text NOT NULL CONSTRAINT module_type_chk CHECK (char_length(type) <= 30),
    sort_order                        integer NOT NULL,
    is_system_module                  boolean NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.module_access (
    principal_id                      uuid,
    module                            text NOT NULL,
    scope_path                        ltree NOT NULL,
    capabilities                      text[] NOT NULL,
    applied_template                  text,
    granted_by_principal_id           uuid,
    granted_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- a one-time code sent to a guest contact point Hangs off: reaches identity.principal through its
-- keys; references pii.subject. Reached by: 2 operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS identity.otp_challenge (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL
);

-- Length, breach check, lockout and step-up (BL-144). Modelled on NIST SP 800-63B rather than
-- habit — length beats composition, and forced rotation makes passwords worse
CREATE TABLE IF NOT EXISTS identity.password_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    min_length                        integer NOT NULL DEFAULT 12,
    require_breach_check              boolean DEFAULT true,
    max_age_days                      integer,
    recovery_methods                  text[],
    max_concurrent_sessions           integer,
    device_restriction                jsonb,
    lockout_after_attempts            integer DEFAULT 10,
    lockout_minutes                   integer DEFAULT 15,
    force_change_on_first_logon       boolean DEFAULT true,
    reuse_prevention_count            integer DEFAULT 5,
    mfa_required_for_permissions      text[]
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.permission (
    id                                uuid PRIMARY KEY,
    module_id                         uuid NOT NULL,
    code                              text NOT NULL CONSTRAINT permission_code_chk CHECK (char_length(code) <= 150),
    name                              text NOT NULL CONSTRAINT permission_name_chk CHECK (char_length(name) <= 150),
    action                            text NOT NULL CONSTRAINT permission_action_chk CHECK (char_length(action) <= 50),
    description                       text CONSTRAINT permission_description_chk CHECK (char_length(description) <= 500),
    is_system                         boolean NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.platform_staff_grant (
    id                                uuid PRIMARY KEY NOT NULL,
    operator_principal_id             uuid NOT NULL,
    operator_display_name             text,
    permissions                       text[] NOT NULL,
    reason                            text NOT NULL,
    ticket_ref                        text,
    opened_at                         timestamptz NOT NULL,
    expires_at                        timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- A person who can be authorised — staff, partner, platform operator. The most referenced table in
-- the package at 122 incoming columns, because almost everything records who did it. Not a guest:
-- a guest is a pii.subject, and ADR-0023 keeps them apart so a data-subject request has one place
-- to answer from
CREATE TABLE IF NOT EXISTS identity.principal (
    id                                uuid PRIMARY KEY NOT NULL,
    username                          text NOT NULL,
    display_name                      text NOT NULL,
    is_active                         boolean NOT NULL,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    primary_role_id                   uuid,
    last_login_at                     timestamptz,
    home_scope_id                     uuid
);

-- a credential hash has no response it belongs in Hangs off: a child of identity.principal;
-- reaches identity.principal through its keys; references identity.principal. Reached by: 3
-- operations read it and 3 write it.
CREATE TABLE IF NOT EXISTS identity.principal_credential (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.refresh_token (
    id                                uuid PRIMARY KEY,
    principal_id                      uuid NOT NULL,
    hash                              text NOT NULL CONSTRAINT refresh_token_hash_chk CHECK (char_length(hash) <= 500),
    expires_at                        timestamptz NOT NULL,
    created_at                        timestamptz NOT NULL,
    created_by_ip                     text CONSTRAINT refresh_token_created_by_ip_chk CHECK (char_length(created_by_ip) <= 50),
    revoked_at                        timestamptz,
    revoked_by_ip                     text CONSTRAINT refresh_token_revoked_by_ip_chk CHECK (char_length(revoked_by_ip) <= 50),
    revocation_reason                 text CONSTRAINT refresh_token_revocation_reason_chk CHECK (char_length(revocation_reason) <= 250),
    replaced_by_token_id              uuid
);

-- A named set of permissions, inheritable. A principal holds roles at scopes; the resolution walks
-- the org tree upward until something answers
CREATE TABLE IF NOT EXISTS identity.role (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    description                       text,
    inherits_from_role_id             uuid,
    is_system                         boolean DEFAULT false,
    principal_count                   integer,
    grant_count                       integer
);

-- child of role, returned nested Hangs off: a child of identity.role; reaches identity.principal
-- through its keys; references identity.principal, identity.role. Reached by: 6 operations read it
-- and 1 write it.
CREATE TABLE IF NOT EXISTS identity.role_permission (
    role_id                           uuid NOT NULL,
    permission                        text NOT NULL CONSTRAINT role_permission_permission_chk CHECK (permission IN ('SESSION_FORCE_LOGOUT', 'USER_MANAGE', 'ROLE_MANAGE', 'PERMISSION_GRANT', 'PERMISSION_VIEW', 'PERMISSION_MANAGE', 'PLATFORM_TENANT_VIEW', 'PLATFORM_TENANT_MANAGE', 'PLATFORM_TENANT_TERMINATE', 'PLATFORM_PLAN_MANAGE', 'PLATFORM_CELL_VIEW', 'PLATFORM_CELL_MANAGE', 'PLATFORM_BILLING_VIEW', 'PLATFORM_AI_MANAGE', 'PLATFORM_BILLING_MANAGE', 'PLATFORM_RELEASE_VIEW', 'PLATFORM_RELEASE_MANAGE', 'PLATFORM_RELEASE_PROMOTE', 'PLATFORM_MIGRATION_VIEW', 'PLATFORM_MIGRATION_APPLY', 'PLATFORM_TENANT_ACCESS', 'TENANT_CONFIGURE', 'TENANT_VIEW', 'TENANT_PUBLISH', 'SCOPE_VIEW', 'SCOPE_MANAGE', 'REGION_CONFIGURE', 'WORKSTATION_CONFIGURE', 'PRODUCT_VIEW', 'PRODUCT_CONFIGURE', 'PRODUCT_APPROVE', 'PRODUCT_PUBLISH', 'PRICE_VIEW', 'PRICE_CONFIGURE', 'EVENT_CONFIGURE', 'PERFORMANCE_CONFIGURE', 'CAPACITY_CONFIGURE', 'ORDER_VIEW', 'ORDER_VIEW_OTHER', 'ORDER_CREATE', 'ORDER_MODIFY', 'ORDER_DISCOUNT', 'ORDER_CANCEL', 'ORDER_VOID', 'ORDER_REFUND', 'ORDER_REFUND_APPROVE', 'ORDER_REFUND_BULK', 'ORDER_EXCHANGE', 'ORDER_RESCHEDULE', 'ORDER_REPRINT', 'PRICE_OVERRIDE', 'DISCOUNT_APPLY', 'CREDIT_MANAGE', 'CREDIT_OVERRIDE', 'WALLET_VIEW', 'WALLET_OPERATE', 'WALLET_CONFIGURE', 'PAYMENT_VIEW', 'PAYMENT_CONFIGURE', 'PAYMENT_PROVIDER_MANAGE', 'PAYMENT_DISPUTE', 'SHIFT_OPEN', 'SHIFT_CLOSE', 'SHIFT_SUSPEND', 'SHIFT_CLOSE_OTHER', 'SHIFT_APPROVE_OPEN', 'SHIFT_APPROVE_CLOSE', 'SHIFT_REOPEN', 'CASH_LIFT', 'CASH_ADD', 'CASH_NO_SALE', 'DEPOSIT_BOX_MODIFY_OWN', 'DEPOSIT_BOX_MODIFY_OTHER', 'OVERSHORT_ACCEPT', 'ACCESS_VALIDATE', 'ACCESS_OVERRIDE', 'ACCESS_POINT_CONFIGURE', 'TURNSTILE_MODE_SET', 'TICKET_LOOKUP', 'ACCREDITATION_VIEW', 'ACCREDITATION_APPLY', 'ACCREDITATION_APPROVE', 'ACCREDITATION_ISSUE', 'ACCREDITATION_MANAGE', 'ACCREDITATION_CONFIGURE', 'REPORT_VIEW_OWN', 'REPORT_VIEW_WORKSTATION', 'REPORT_VIEW_VENUE', 'REPORT_VIEW_REGION', 'REPORT_VIEW_TENANT', 'REPORT_EXPORT', 'REPORT_EXPORT_PII', 'REPORT_MANAGE', 'REPORT_SCHEDULE', 'LEDGER_VIEW', 'LEDGER_POST', 'LEDGER_APPROVE', 'TAX_CONFIGURE', 'ACCOUNT_CONFIGURE', 'SETTLEMENT_VIEW', 'SETTLEMENT_RECONCILE', 'GUEST_VIEW', 'GUEST_VIEW_PII', 'GUEST_MANAGE', 'VENUE_MAP_VIEW', 'VENUE_MAP_MANAGE', 'VENUE_MAP_PUBLISH', 'RESOURCE_VIEW', 'RESOURCE_BOOK', 'RESOURCE_MANAGE', 'RESOURCE_CONFIGURE', 'RENTAL_VIEW', 'RENTAL_BOOK', 'RENTAL_OPERATE', 'RENTAL_MANAGE', 'RENTAL_CONFIGURE', 'RENTAL_PRICE', 'RENTAL_APPROVE', 'RENTAL_OVERRIDE', 'DEVELOPER_VIEW', 'DEVELOPER_MANAGE', 'DEVELOPER_ADMIN', 'LOYALTY_ACCRUE', 'LOYALTY_REDEEM', 'LOYALTY_ADJUST', 'MARKETING_VIEW', 'MARKETING_MANAGE', 'MARKETING_SEND', 'CASE_VIEW', 'CASE_MANAGE', 'ASSET_LIBRARY_VIEW', 'ASSET_LIBRARY_MANAGE', 'ASSET_LIBRARY_APPROVE', 'ASSET_LIBRARY_SHARE', 'QUEUE_VIEW', 'QUEUE_MANAGE', 'QUEUE_REDEEM', 'QUEUE_OVERRIDE', 'TRANSPORT_VIEW', 'TRANSPORT_MANAGE', 'TRANSPORT_PRICE', 'ASSET_VIEW', 'ASSET_MANAGE', 'WORK_ORDER_VIEW', 'WORK_ORDER_MANAGE', 'WORK_ORDER_VERIFY', 'INSPECTION_VIEW', 'INSPECTION_SUBMIT', 'INSPECTION_MANAGE', 'INCIDENT_REPORT', 'INCIDENT_VIEW', 'INCIDENT_MANAGE', 'KIOSK_ATTEND', 'DEVICE_VIEW', 'DEVICE_CONFIGURE', 'DEVICE_MANAGE', 'APPROVAL_ACT', 'APPROVAL_DELEGATE', 'AI_USE', 'AI_CONFIGURE', 'AI_APPROVE', 'AI_AUDIT_VIEW', 'RISK_REVIEW', 'RISK_INVESTIGATE', 'AUDIT_VIEW', 'APPROVAL_VIEW', 'APPROVAL_REQUEST', 'APPROVAL_DECIDE', 'APPROVAL_CONFIGURE', 'MAINTENANCE_EXECUTE', 'MAINTENANCE_APPROVE', 'WORKFORCE_VIEW', 'WORKFORCE_MANAGE', 'ATTENDANCE_RECORD', 'ANNOUNCEMENT_PUBLISH', 'ANNOUNCEMENT_EMERGENCY', 'PARTNER_VIEW', 'PARTNER_MANAGE', 'PARKING_CONFIGURE', 'PAYMENT_VOID', 'PROCUREMENT_VIEW', 'PROCUREMENT_REQUEST', 'PROCUREMENT_MANAGE', 'PROCUREMENT_RECEIVE')),
    granted_at                        timestamptz,
    granted_by_principal_id           uuid,
    is_active                         boolean DEFAULT true,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Which permissions may not be held together (BL-147, 3.3.31). Checked at grant time, not use time
-- — discovering the conflict when somebody exercises it means it already existed
CREATE TABLE IF NOT EXISTS identity.segregation_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text,
    permission_a                      text NOT NULL,
    permission_b                      text NOT NULL,
    severity                          text NOT NULL CONSTRAINT segregation_rule_severity_chk CHECK (severity IN ('block', 'requireApproval', 'warn')),
    rationale                         text,
    scope_sensitive                   boolean DEFAULT true,
    allow_with_compensating_control   boolean DEFAULT false,
    scope_path                        ltree NOT NULL
);

-- Which provider group becomes which role. The join that stops SSO meaning manual role assignment
CREATE TABLE IF NOT EXISTS identity.sso_group_mapping (
    id                                uuid PRIMARY KEY,
    external_group                    text NOT NULL,
    role_id                           uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    provider_id                       uuid,
    scope_id                          uuid
);

-- A tenant’s own identity provider. A guest arriving through UAE Pass is verified in a way an
-- email never is
CREATE TABLE IF NOT EXISTS identity.sso_provider (
    icon_asset_ref                    text,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    display_name                      text NOT NULL,
    protocol                          text NOT NULL CONSTRAINT sso_provider_protocol_chk CHECK (protocol IN ('oidc', 'saml2')),
    metadata_url                      text,
    issuer                            text,
    client_id                         text,
    client_secret_ref                 text,
    is_auto_provision_principals      boolean DEFAULT false,
    is_enforced                       boolean DEFAULT false,
    is_active                         boolean
);

