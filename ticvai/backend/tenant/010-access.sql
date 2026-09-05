-- access — 7 tables
-- **Derived. Do not hand-edit.**

-- A place a credential is presented — a gate, a turnstile, a door, a scanner position. Carries the
-- rules it applies through access.admission_rules
CREATE TABLE IF NOT EXISTS access.access_point (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        text,
    operating_mode                    text,
    vehicle_location_capture          boolean,
    mode                              text NOT NULL,
    direction                         text,
    anti_passback_enabled             boolean,
    is_active                         boolean NOT NULL,
    last_heartbeat_at                 timestamptz
);

-- What a gate checks before it opens — how early, how late, how many times, and which credentials
-- count. Renamed from admission_rules, because *profile* reads as a person
CREATE TABLE IF NOT EXISTS access.admission_rules (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    open_minutes_before               integer NOT NULL,
    close_minutes_after               integer NOT NULL,
    max_duration_minutes              integer,
    requires_exit_before_reentry      boolean,
    max_reentries                     integer,
    allowed_access_point_ids          text[],
    scope_path                        text
);

-- Who may not be admitted, and by whose authority
CREATE TABLE IF NOT EXISTS access.blacklist (
    media_code                        text NOT NULL,
    reason                            text NOT NULL,
    added_at                          timestamptz NOT NULL,
    added_by_principal_id             uuid NOT NULL,
    expires_at                        timestamptz,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- What a guest actually holds — found missing 18 August. The package sold products, defined
-- EntitlementTemplate, recorded ScanEvent.ticketId, transferred ticket_ids and issued wallet
-- passes against entitlementId: five artefacts referring to a thing that did not exist.
-- validateAccess read the template and suspendEntitlement suspended it, which would have suspended
-- it for every guest who held one. Han
CREATE TABLE IF NOT EXISTS access.entitlement (
    id                                text PRIMARY KEY NOT NULL,
    template_id                       uuid NOT NULL,
    product_id                        uuid NOT NULL,
    order_id                          uuid NOT NULL,
    order_line_id                     uuid,
    subject_id                        uuid NOT NULL,
    venue_id                          uuid,
    scope_path                        text,
    media_code                        text,
    status                            text NOT NULL,
    status_note                       text,
    valid_from                        timestamptz NOT NULL,
    valid_to                          timestamptz NOT NULL,
    entries_used                      integer,
    entries_allowed                   integer,
    last_entry_at                     timestamptz,
    frozen_days                       integer,
    suspended_reason                  text,
    is_name_bound                     boolean,
    holder_name                       text,
    shared_with_subject_ids           text[],
    issued_via                        text,
    supersedes_entitlement_id         uuid,
    wallet_value_id                   uuid
);

-- A guest bought parking. Carries the plate where the mode is plateWhitelist — personal data,
-- since a plate identifies a person Hangs off: reaches access.entitlement through its keys;
-- references access.parking_facility, orders.sales_order, pii.subject. Reached by: 1 operations
-- read it and 2 write it
CREATE TABLE IF NOT EXISTS access.parking_entitlement (
    id                                uuid PRIMARY KEY,
    facility_id                       uuid NOT NULL,
    order_id                          text NOT NULL,
    subject_id                        uuid,
    plate_number                      text,
    plate_country                     text,
    media_code                        text,
    status                            text,
    pushed_at                         timestamptz,
    push_failure_reason               text,
    valid_from                        timestamptz NOT NULL,
    valid_to                          timestamptz NOT NULL
);

-- A car park and its integration mode. Three modes, and the mode decides what happens at sale
-- (CF-52) Hangs off: reaches access.entitlement through its keys; references platform.org_unit.
-- Reached by: 3 operations read it and 1 write it; 1 tables reference it
CREATE TABLE IF NOT EXISTS access.parking_facility (
    id                                uuid PRIMARY KEY,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    mode                              text NOT NULL,
    capacity                          integer,
    takes_payment                     boolean,
    vendor_swap_target_days           integer,
    vendor_name                       text,
    endpoint                          text,
    credential_ref                    text,
    push_lead_minutes                 integer,
    access_point_ids                  text[],
    is_active                         boolean
);

-- Every presentation of a credential, admitted or not. The highest-volume table in the platform
CREATE TABLE IF NOT EXISTS access.scan_event (
    id                                text PRIMARY KEY NOT NULL,
    access_point_id                   uuid NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        text,
    ticket_id                         text,
    media_code                        text,
    outcome                           text NOT NULL,
    deny_reason                       text,
    direction                         text NOT NULL,
    operator_principal_id             uuid,
    device_id                         uuid,
    overridden_by_principal_id        uuid,
    override_reason                   text,
    recorded_at                       timestamptz NOT NULL,
    synced_at                         timestamptz
);

