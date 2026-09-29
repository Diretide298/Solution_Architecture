-- tenancy — 8 tables
-- **Derived. Do not hand-edit.**

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is. Reached by: 4 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS tenancy.data_retention_setting (
    id                                uuid PRIMARY KEY,
    data_class                        text NOT NULL,
    retain_amount                     integer,
    retain_unit                       text CONSTRAINT data_retention_setting_retain_unit_chk CHECK (retain_unit IN ('days', 'months', 'years')),
    follows_data_class                text,
    on_expiry                         text DEFAULT 'archive' CONSTRAINT data_retention_setting_on_expiry_chk CHECK (on_expiry IN ('archive', 'anonymise', 'delete')),
    updated_at                        timestamptz,
    updated_by_principal_id           uuid,
    scope_path                        ltree NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS tenancy.device_assignment (
    device_id                         uuid,
    owner_org_unit_id                 uuid,
    custodian_principal_id            uuid,
    assigned_workstation_id           uuid,
    location_scope_path               ltree,
    last_seen_location                text,
    asset_tag                         text,
    acquired_at                       date,
    warranty_expires_at               date,
    assigned_at                       timestamptz,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS tenancy.device_audit (
    id                                uuid PRIMARY KEY,
    device_id                         uuid,
    at                                timestamptz,
    kind                              text CONSTRAINT device_audit_kind_chk CHECK (kind IN ('administration', 'access', 'security')),
    action                            text,
    actor_principal_id                uuid,
    previous_value                    text,
    new_value                         text,
    source_ip                         text,
    correlation_id                    text,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS tenancy.device_credential (
    id                                uuid PRIMARY KEY,
    device_id                         uuid,
    kind                              text CONSTRAINT device_credential_kind_chk CHECK (kind IN ('clientCertificate', 'deviceToken', 'mutualTls')),
    fingerprint                       text,
    issued_at                         timestamptz,
    expires_at                        timestamptz,
    revoked_at                        timestamptz,
    revocation_reason                 text,
    scope_path                        ltree NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS tenancy.device_firmware (
    id                                uuid PRIMARY KEY,
    device_kind                       text NOT NULL,
    version                           text NOT NULL,
    vendor                            text,
    checksum_algorithm                text DEFAULT 'sha256' CONSTRAINT device_firmware_checksum_algorithm_chk CHECK (checksum_algorithm IN ('sha256', 'sha512')),
    release_notes                     text,
    artefact_asset_id                 uuid,
    checksum                          text,
    minimum_previous_version          text,
    released_at                       timestamptz,
    installed_count                   integer,
    status                            text DEFAULT 'draft' CONSTRAINT device_firmware_status_chk CHECK (status IN ('draft', 'released', 'deprecated', 'withdrawn')),
    status_reason                     text,
    scope_path                        ltree NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS tenancy.device_rollout (
    id                                uuid PRIMARY KEY,
    firmware_id                       uuid NOT NULL,
    target_scope_path                 ltree,
    target_device_ids                 text[],
    maintenance_window                jsonb,
    is_previous_version_retained      boolean DEFAULT true,
    status                            text CONSTRAINT device_rollout_status_chk CHECK (status IN ('scheduled', 'running', 'paused', 'completed', 'halted', 'rolledBack')),
    succeeded_count                   integer,
    failed_count                      integer,
    scope_path                        ltree NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS tenancy.device_tamper_event (
    id                                uuid PRIMARY KEY,
    device_id                         uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT device_tamper_event_kind_chk CHECK (kind IN ('enclosureOpened', 'locationAnomaly', 'credentialMismatch', 'firmwareUnsigned', 'clockSkew', 'physicalRemoval')),
    detected_at                       timestamptz,
    detail                            text,
    is_device_trusted                 boolean DEFAULT false,
    resolved_at                       timestamptz,
    resolved_by                       uuid,
    resolution                        text,
    scope_path                        ltree NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS tenancy.device_telemetry (
    device_id                         uuid,
    at                                timestamptz,
    battery_percent                   integer,
    battery_health_percent            integer,
    is_charging                       boolean,
    signal_strength                   integer,
    cpu_percent                       numeric(18,4),
    memory_percent                    numeric(18,4),
    storage_free_mb                   integer,
    consumables                       jsonb,
    uptime_seconds                    integer,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

