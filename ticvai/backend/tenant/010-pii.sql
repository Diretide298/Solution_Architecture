-- pii — 5 tables
-- **Derived. Do not hand-edit.**

-- The IP address and user agent a cookie decision was made from, kept only where the published
-- banner design has record_ip_address on (ADR-0023). Held in pii and pointed at the decision,
-- never beside it, so the consent log can be read and reported without reading personal data.
-- Reached by: 0 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS pii.consent_identifier (
    id                                uuid PRIMARY KEY,
    device_consent_id                 uuid NOT NULL,
    ip_address                        text CONSTRAINT consent_identifier_ip_address_chk CHECK (char_length(ip_address) <= 45),
    user_agent                        text CONSTRAINT consent_identifier_user_agent_chk CHECK (char_length(user_agent) <= 500),
    captured_at                       timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- A guest, and the only table holding who they are. Name, and through its children the contacts,
-- documents and biometrics. Isolated deliberately — erasure is a delete here and a pseudonym
-- everywhere else, which is what makes a DSAR answerable at all
CREATE TABLE IF NOT EXISTS pii.subject (
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              pii.subject_kind NOT NULL,
    display_name                      text,
    given_name                        text,
    family_name                       text,
    date_of_birth                     date,
    nationality                       char(2),
    preferred_language                char(2),
    is_erased                         boolean NOT NULL,
    erased_at                         timestamptz,
    erasure_request_id                char(26),
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz NOT NULL
);

-- A face template, and nothing else. Separate from contact and document so consent and erasure
-- differ per kind
CREATE TABLE IF NOT EXISTS pii.subject_biometric (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    entitlement_id                    text NOT NULL,
    kind                              text NOT NULL CONSTRAINT subject_biometric_kind_chk CHECK (kind IN ('facePass', 'faceTag')),
    retention_anchor                  text,
    source                            text NOT NULL CONSTRAINT subject_biometric_source_chk CHECK (source IN ('guestApp', 'ticketCounter', 'annualPassCounter', 'entryGate')),
    captured_at                       timestamptz NOT NULL,
    consent_purpose_id                uuid,
    consent_given_at                  timestamptz,
    guardian_subject_id               uuid,
    is_active                         boolean,
    expires_at                        timestamptz
);

-- An email, a phone. The thing a marketing suppression matches on
CREATE TABLE IF NOT EXISTS pii.subject_contact (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    kind                              pii.contact_kind NOT NULL,
    value                             text NOT NULL,
    value_normalised                  text NOT NULL,
    value_hash                        text NOT NULL,
    is_primary                        boolean NOT NULL,
    is_verified                       boolean NOT NULL,
    verified_at                       timestamptz,
    created_at                        timestamptz NOT NULL
);

-- A passport or ID, and its verification state. Hangs off: a child of pii.subject; reaches
-- pii.subject through its keys; references pii.subject. Reached by: 1 operations read it and 3
-- write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS pii.subject_document (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    kind                              text NOT NULL,
    number_hash                       text NOT NULL,
    number_last4                      char(4),
    issuing_country                   char(2),
    expires_on                        date,
    document_asset_ref                text,
    verified_at                       timestamptz,
    created_at                        timestamptz NOT NULL
);

