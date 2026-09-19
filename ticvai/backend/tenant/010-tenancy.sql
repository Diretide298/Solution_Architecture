-- tenancy — 7 tables
-- **Derived. Do not hand-edit.**

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS tenancy.device_assignment (
    device_id                         uuid,
    owner_org_unit_id                 uuid,
    custodian_principal_id            uuid,
    assigned_workstation_id           uuid,
    location_scope_path               text,
    last_seen_location                text,
    asset_tag                         text,
    acquired_at                       date,
    warranty_expires_at               date,
    assigned_at                       timestamptz,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS tenancy.device_audit (
    id                                uuid PRIMARY KEY,
    device_id                         uuid,
    at                                timestamptz,
    kind                              text,
    action                            text,
    actor_principal_id                uuid,
    previous_value                    text,
    new_value                         text,
    source_ip                         text,
    correlation_id                    text,
    scope_path                        text
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS tenancy.device_credential (
    id                                uuid PRIMARY KEY,
    device_id                         uuid,
    kind                              text,
    fingerprint                       text,
    issued_at                         timestamptz,
    expires_at                        timestamptz,
    revoked_at                        timestamptz,
    revocation_reason                 text,
    scope_path                        text
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS tenancy.device_firmware (
    id                                uuid PRIMARY KEY,
    device_kind                       text,
    version                           text,
    release_notes                     text,
    artefact_asset_id                 uuid,
    checksum                          text,
    minimum_previous_version          text,
    released_at                       timestamptz,
    installed_count                   integer,
    status                            text
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS tenancy.device_rollout (
    id                                uuid PRIMARY KEY,
    firmware_id                       uuid NOT NULL,
    target_scope_path                 text,
    target_device_ids                 text[],
    maintenance_window                jsonb,
    previous_version_retained         boolean,
    status                            text,
    succeeded_count                   integer,
    failed_count                      integer,
    scope_path                        text
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS tenancy.device_tamper_event (
    id                                uuid PRIMARY KEY,
    device_id                         uuid NOT NULL,
    kind                              text NOT NULL,
    detected_at                       timestamptz,
    detail                            text,
    device_trusted                    boolean,
    resolved_at                       timestamptz,
    resolved_by                       uuid,
    resolution                        text,
    scope_path                        text
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS tenancy.device_telemetry (
    device_id                         uuid,
    at                                timestamptz,
    battery_percent                   integer,
    battery_health_percent            integer,
    charging                          boolean,
    signal_strength                   integer,
    cpu_percent                       numeric(18,4),
    memory_percent                    numeric(18,4),
    storage_free_mb                   integer,
    consumables                       jsonb,
    uptime_seconds                    integer,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

