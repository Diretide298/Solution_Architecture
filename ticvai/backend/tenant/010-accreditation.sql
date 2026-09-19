-- accreditation — 13 tables
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
    escort_required                   boolean,
    holder_count                      integer,
    scope_path                        text
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
    status                            text,
    decision_reason                   text,
    approval_request_id               uuid,
    holder_id                         uuid,
    submitted_at                      timestamptz,
    decided_at                        timestamptz,
    scope_path                        text
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
    integrity                         text,
    scope_path                        text
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.badge_template (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text,
    size                              text,
    show_photo                        boolean,
    show_zones                        boolean,
    colour_stripe                     text,
    show_organisation                 boolean,
    show_validity                     boolean,
    background_asset_id               uuid,
    security_features                 text[],
    scope_path                        text
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.credential (
    id                                uuid PRIMARY KEY,
    holder_id                         uuid NOT NULL,
    kind                              text NOT NULL,
    serial_number                     text,
    encoded_identifier                text,
    badge_template_id                 uuid,
    issued_at                         timestamptz,
    issued_by                         uuid,
    activated_at                      timestamptz,
    status                            text,
    replaces_credential_id            uuid,
    replacement_count                 integer,
    scope_path                        text
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
    status                            text,
    verified_by                       uuid,
    verified_at                       timestamptz,
    rejection_reason                  text,
    expires_at                        date,
    scope_path                        text
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
    identity_document_verified        boolean,
    organisation_id                   uuid,
    affiliation_role                  text,
    programme_id                      uuid,
    category_code                     text,
    status                            text,
    valid_from                        date,
    valid_to                          date,
    completeness_percent              integer,
    scope_path                        text
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.holder_access (
    holder_id                         uuid,
    access_profile_ids                text[],
    effective_zones                   text[],
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 3 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.notification_rules (
    programme_id                      uuid,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.print_job (
    id                                uuid PRIMARY KEY,
    credential_ids                    text[],
    printer_device_id                 uuid,
    queued_at                         timestamptz,
    status                            text,
    printed                           integer,
    failed                            integer,
    scope_path                        text
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
    status                            text,
    scope_path                        text
);

-- Holds 3 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.requirements (
    programme_id                      uuid,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS accreditation.validity (
    programme_id                      uuid,
    validity_kind                     text,
    validity_months                   integer,
    renewal_window_days               integer,
    renewal_requires_reverification   boolean,
    on_expiry                         text,
    grace_period_days                 integer,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

