-- access — 9 tables
-- **Derived. Do not hand-edit.**

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.access_change (
    id                                uuid PRIMARY KEY,
    old_access_id                     uuid NOT NULL,
    new_access_id                     uuid,
    type                              text NOT NULL CONSTRAINT access_change_type_chk CHECK (char_length(type) <= 30),
    order_id                          text,
    upgrade_id                        uuid,
    reason                            text CONSTRAINT access_change_reason_chk CHECK (char_length(reason) <= 500),
    changed_by_principal_id           uuid,
    changed_at                        timestamptz NOT NULL
);

-- A place a credential is presented — a gate, a turnstile, a door, a scanner position. Carries the
-- rules it applies through access.admission_rules
CREATE TABLE IF NOT EXISTS access.access_point (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    external_credential_sources       jsonb,
    scan_anomaly_rules                jsonb,
    operating_mode                    text DEFAULT 'normal' CONSTRAINT access_point_operating_mode_chk CHECK (operating_mode IN ('normal', 'freeFlow', 'dropArm', 'closed', 'podium', 'maintenance')),
    vehicle_location_capture          boolean DEFAULT false,
    mode                              text NOT NULL CONSTRAINT access_point_mode_chk CHECK (mode IN ('entry', 'reentry', 'crossover', 'exit', 'freeRotation', 'closed')),
    direction                         text CONSTRAINT access_point_direction_chk CHECK (direction IN ('entry', 'exit', 'reentry', 'crossover')),
    is_anti_passback_enabled          boolean,
    requires_exit_before_reentry      boolean DEFAULT false,
    driver                            text,
    geofence                          jsonb,
    is_active                         boolean NOT NULL,
    last_heartbeat_at                 timestamptz
);

-- What a gate checks before it opens — how early, how late, how many times, and which credentials
-- count. Renamed from admission_rules, because *profile* reads as a person
CREATE TABLE IF NOT EXISTS access.admission_rules (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT admission_rules_code_chk CHECK (char_length(code) <= 64),
    per_product_rules                 jsonb,
    name                              text NOT NULL CONSTRAINT admission_rules_name_chk CHECK (char_length(name) <= 200),
    open_minutes_before               integer NOT NULL,
    close_minutes_after               integer NOT NULL,
    max_duration_minutes              integer,
    requires_exit_before_reentry      boolean DEFAULT false,
    max_reentries                     integer,
    allowed_access_point_ids          text[],
    scope_path                        ltree NOT NULL
);

-- Who may not be admitted, and by whose authority
CREATE TABLE IF NOT EXISTS access.blacklist (
    media_code                        text NOT NULL,
    reason                            text NOT NULL,
    added_at                          timestamptz NOT NULL,
    added_by_principal_id             uuid NOT NULL,
    expires_at                        timestamptz,
    scope_path                        ltree NOT NULL,
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
    order_id                          text NOT NULL,
    order_line_id                     uuid,
    subject_id                        uuid,
    venue_id                          uuid,
    scope_path                        ltree NOT NULL,
    media_code                        text,
    status                            text NOT NULL CONSTRAINT entitlement_status_chk CHECK (status IN ('issued', 'partiallyConsumed', 'fullyConsumed', 'expired', 'cancelled', 'surrendered')),
    status_note                       text,
    valid_from                        timestamptz NOT NULL,
    valid_to                          timestamptz NOT NULL,
    entries_used                      integer DEFAULT 0,
    entries_allowed                   integer,
    last_entry_at                     timestamptz,
    frozen_days                       integer DEFAULT 0,
    suspended_reason                  text,
    is_name_bound                     boolean DEFAULT false,
    holder_name                       text,
    shared_with_subject_ids           text[],
    issued_via                        text CONSTRAINT entitlement_issued_via_chk CHECK (issued_via IN ('sale', 'invitation', 'reissue', 'transfer', 'resale', 'membership', 'groupBooking')),
    supersedes_entitlement_id         text,
    wallet_value_id                   uuid
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.entry_rule_point (
    admission_profile_id              uuid NOT NULL,
    access_point_id                   uuid NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    id                                uuid PRIMARY KEY
);

-- A guest bought parking. Carries the plate where the mode is plateWhitelist — personal data,
-- since a plate identifies a person Hangs off: reaches access.entitlement through its keys;
-- references access.parking_facility, orders.sales_order, pii.subject. Reached by: 2 operations
-- read it and 2 write it.
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
-- (CF-52) Hangs off: reaches access.entitlement through its keys; references platform.scope.
-- Reached by: 3 operations read it and 1 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS access.parking_facility (
    id                                uuid PRIMARY KEY,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    mode                              text NOT NULL CONSTRAINT parking_facility_mode_chk CHECK (mode IN ('none', 'plateWhitelist', 'qrHandoff')),
    capacity                          integer,
    takes_payment                     boolean DEFAULT false,
    vendor_swap_target_days           integer DEFAULT 5,
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
    scope_path                        ltree NOT NULL,
    ticket_id                         text,
    media_code                        text,
    outcome                           text NOT NULL CONSTRAINT scan_event_outcome_chk CHECK (outcome IN ('admitted', 'denied', 'overridden')),
    deny_reason                       text CONSTRAINT scan_event_deny_reason_chk CHECK (deny_reason IN ('notFound', 'notYetValid', 'expired', 'alreadyUsed', 'reentryLimitReached', 'exitRequiredBeforeReentry', 'wrongAccessPoint', 'wrongPerformance', 'outsideAdmissionWindow', 'entitlementSuspended', 'blacklisted', 'capacityReached', 'waiverRequired', 'accompanimentRequired', 'mediaDeactivated', 'unpaid', 'delegatedRightExhausted', 'delegatedRightRevoked')),
    direction                         text NOT NULL CONSTRAINT scan_event_direction_chk CHECK (direction IN ('entry', 'exit', 'reentry', 'crossover')),
    operator_principal_id             uuid,
    device_id                         uuid,
    overridden_by_principal_id        uuid,
    override_reason                   text,
    recorded_at                       timestamptz NOT NULL,
    synced_at                         timestamptz
);

