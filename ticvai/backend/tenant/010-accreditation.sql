-- accreditation — 14 tables
-- **Derived. Do not hand-edit.**

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.access_profile (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    zone_ids                          text[],
    venue_ids                         text[],
    operational_areas                 text[],
    is_escort_required                boolean DEFAULT false,
    holder_count                      integer,
    scope_path                        ltree NOT NULL
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.application (
    id                                uuid PRIMARY KEY,
    reference                         text,
    programme_id                      uuid NOT NULL,
    category_code                     text,
    applicant_type                    text,
    submitted_by_principal_id         uuid,
    organisation_id                   uuid,
    subject                           jsonb,
    status                            text CONSTRAINT application_status_chk CHECK (status IN ('draft', 'submitted', 'underReview', 'informationRequested', 'approved', 'rejected', 'withdrawn', 'expired')),
    decision_reason                   text,
    approval_request_id               uuid,
    holder_id                         uuid,
    submitted_at                      timestamptz,
    decided_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.audit (
    id                                uuid PRIMARY KEY,
    at                                timestamptz,
    holder_id                         uuid,
    action                            text,
    actor_principal_id                uuid,
    previous_value                    text,
    new_value                         text,
    reason                            text,
    approval_request_id               uuid,
    previous_record_hash              text,
    record_hash                       text,
    integrity                         text CONSTRAINT audit_integrity_chk CHECK (integrity IN ('intact', 'broken', 'unverifiable')),
    scope_path                        ltree NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.badge_template (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text,
    size                              text,
    show_photo                        boolean DEFAULT true,
    show_zones                        boolean DEFAULT true,
    colour_stripe                     text,
    show_organisation                 boolean DEFAULT true,
    show_validity                     boolean DEFAULT true,
    background_asset_id               uuid,
    security_features                 text[],
    scope_path                        ltree NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.credential (
    id                                uuid PRIMARY KEY,
    holder_id                         uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT credential_kind_chk CHECK (kind IN ('printedBadge', 'mobileCredential', 'nfcCard', 'rfidCard', 'wristband')),
    serial_number                     text,
    encoded_identifier                text,
    badge_template_id                 uuid,
    issued_at                         timestamptz,
    issued_by                         uuid,
    activated_at                      timestamptz,
    status                            text CONSTRAINT credential_status_chk CHECK (status IN ('pendingPrint', 'issued', 'active', 'lost', 'replaced', 'revoked', 'expired')),
    replaces_credential_id            uuid,
    replacement_count                 integer DEFAULT 0,
    scope_path                        ltree NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.document (
    id                                uuid PRIMARY KEY,
    holder_id                         uuid,
    application_id                    uuid,
    requirement_code                  text NOT NULL,
    asset_id                          uuid NOT NULL,
    submitted_at                      timestamptz,
    status                            text CONSTRAINT document_status_chk CHECK (status IN ('submitted', 'verified', 'rejected', 'expired')),
    verified_by                       uuid,
    verified_at                       timestamptz,
    rejection_reason                  text,
    expires_at                        date,
    scope_path                        ltree NOT NULL
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.holder (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid,
    accreditation_number              text,
    full_name                         text NOT NULL,
    photo_asset_id                    uuid,
    date_of_birth                     date,
    nationality                       text,
    is_identity_document_verified     boolean DEFAULT false,
    organisation_id                   uuid,
    affiliation_role                  text,
    programme_id                      uuid,
    category_code                     text,
    status                            text CONSTRAINT holder_status_chk CHECK (status IN ('active', 'suspended', 'revoked', 'expired', 'archived')),
    valid_from                        date,
    valid_to                          date,
    completeness_percent              integer,
    scope_path                        ltree NOT NULL
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.holder_access (
    holder_id                         uuid,
    access_profile_ids                text[],
    effective_zones                   text[],
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.identity_conflict (
    id                                uuid PRIMARY KEY NOT NULL,
    holder_ids                        text[] NOT NULL,
    score                             numeric(18,4),
    matched_on                        text[],
    differing_access                  boolean,
    status                            text NOT NULL CONSTRAINT identity_conflict_status_chk CHECK (status IN ('pending', 'merged', 'rejected')),
    detected_at                       timestamptz,
    surviving_holder_id               uuid,
    resolution_reason                 text CONSTRAINT identity_conflict_resolution_reason_chk CHECK (char_length(resolution_reason) <= 500),
    resolved_by_principal_id          uuid,
    resolved_at                       timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 3 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.notification_rules (
    programme_id                      uuid,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.print_job (
    id                                uuid PRIMARY KEY,
    credential_ids                    text[],
    printer_device_id                 uuid,
    queued_at                         timestamptz,
    status                            text CONSTRAINT print_job_status_chk CHECK (status IN ('queued', 'printing', 'completed', 'partiallyFailed', 'failed')),
    printed                           integer,
    failed                            integer,
    scope_path                        ltree NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.programme (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_ids                         text[],
    event_ids                         text[],
    applicant_types                   text[],
    applications_open_at              timestamptz,
    applications_close_at             timestamptz,
    approval_workflow_id              uuid,
    status                            text CONSTRAINT programme_status_chk CHECK (status IN ('draft', 'open', 'closed', 'archived')),
    scope_path                        ltree NOT NULL
);

-- Holds 3 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.requirements (
    programme_id                      uuid,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.validity (
    programme_id                      uuid,
    validity_kind                     text CONSTRAINT validity_validity_kind_chk CHECK (validity_kind IN ('eventDuration', 'fixedPeriod', 'seasonal', 'rolling', 'permanent')),
    validity_months                   integer,
    renewal_window_days               integer,
    renewal_requires_reverification   boolean DEFAULT true,
    on_expiry                         text DEFAULT 'revokeAccess' CONSTRAINT validity_on_expiry_chk CHECK (on_expiry IN ('revokeAccess', 'gracePeriod', 'autoRenew')),
    grace_period_days                 integer,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

