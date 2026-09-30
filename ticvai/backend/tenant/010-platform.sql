-- platform — 26 tables
-- **Derived. Do not hand-edit.**

-- PII reads only, written by the platform. Who looked at a passport number is the question a
-- regulator asks Hangs off: reaches platform.scope through its keys; references
-- identity.principal, pii.subject. Reached by: 0 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS platform.audit_read (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid NOT NULL,
    subject_id                        uuid NOT NULL
);

-- Written by the platform on every write, not by any one operation (ADR-0022 sits above this).
-- Naming it on 431 lineage rows would say nothing Hangs off: reaches platform.scope through its
-- keys; references identity.platform_staff_grant, identity.principal, platform.scope. Reached by:
-- 1 operations read it and 10 write it; written by 5 contracts — finance, inventory, orders,
-- payments.
CREATE TABLE IF NOT EXISTS platform.audit_record (
    id                                uuid NOT NULL,
    principal_id                      uuid,
    org_unit_id                       uuid,
    workstation_id                    uuid,
    action                            text NOT NULL,
    subject_ref                       text,
    occurred_at                       timestamptz NOT NULL,
    platform_staff_grant_id           uuid,
    CONSTRAINT audit_record_pkey PRIMARY KEY (id, occurred_at)
) PARTITION BY RANGE (occurred_at);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS platform.cell_endpoint (
    id                                uuid PRIMARY KEY,
    cell_id                           uuid NOT NULL,
    service_name                      text NOT NULL CONSTRAINT cell_endpoint_service_name_chk CHECK (char_length(service_name) <= 100),
    url                               text NOT NULL CONSTRAINT cell_endpoint_url_chk CHECK (char_length(url) <= 1000),
    contract_version                  text CONSTRAINT cell_endpoint_contract_version_chk CHECK (char_length(contract_version) <= 50),
    authentication_type               text CONSTRAINT cell_endpoint_authentication_type_chk CHECK (char_length(authentication_type) <= 50),
    credential_reference              text CONSTRAINT cell_endpoint_credential_reference_chk CHECK (char_length(credential_reference) <= 500),
    status                            text NOT NULL CONSTRAINT cell_endpoint_status_chk CHECK (char_length(status) <= 30),
    last_health_check_at              timestamptz,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- What a class of workstation is configured to be (client Board 1, 20 August). A profile is what a
-- venue changes; a version is what it deploys — conflating them means a venue cannot roll back one
-- fleet and leave another
CREATE TABLE IF NOT EXISTS platform.configuration_profile (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    scope_path                        ltree NOT NULL,
    venue_kind_scope                  text[] NOT NULL,
    version                           integer NOT NULL,
    settings                          jsonb,
    status                            text NOT NULL CONSTRAINT configuration_profile_status_chk CHECK (status IN ('draft', 'published', 'deploying', 'deployed', 'superseded', 'rolledBack')),
    deployed_count                    integer,
    published_at                      timestamptz
);

-- When a workstation decides it is offline, and when it is back (Board 5). Asymmetric thresholds,
-- because symmetric ones make it flap across a marginal connection
CREATE TABLE IF NOT EXISTS platform.connectivity_policy (
    id                                uuid PRIMARY KEY,
    scope_path                        ltree NOT NULL,
    failures_before_offline           integer DEFAULT 3,
    probe_interval_seconds            integer DEFAULT 15,
    probe_timeout_ms                  integer DEFAULT 2000,
    successes_before_online           integer DEFAULT 5,
    minimum_stable_seconds            integer DEFAULT 30,
    is_auto_switch                    boolean DEFAULT true
);

-- Something bought in one jurisdiction and honoured in another. ADR-0010: the guest does not move,
-- a pseudonymous link does. Renamed from cross_region_entitlement — a right to redeem what, and
-- where? Hangs off: reaches platform.scope through its keys; references access.admission_rules,
-- access.entitlement, platform.guest_link. Reached by: 5 operations read it and 4 write it.
CREATE TABLE IF NOT EXISTS platform.cross_region_entitlement (
    id                                uuid PRIMARY KEY,
    right_id                          uuid NOT NULL,
    ticket_id                         uuid NOT NULL,
    guest_link_id                     uuid,
    issuing_cell_name                 text NOT NULL,
    consuming_cell_name               text NOT NULL,
    media_codes                       text[],
    valid_from                        timestamptz NOT NULL,
    valid_to                          timestamptz NOT NULL,
    admission_rules_id                uuid,
    venue_id                          uuid,
    entries_allowed                   integer,
    entries_consumed                  integer NOT NULL,
    status                            text NOT NULL CONSTRAINT cross_region_entitlement_status_chk CHECK (status IN ('active', 'exhausted', 'revoked', 'expired')),
    last_consumed_at                  timestamptz,
    last_reconciled_at                timestamptz
);

-- An outbox row whose delivery failed after its retry budget (ADR-0033). Carries the payload
-- rather than a reference, because a dead letter you cannot replay is a log entry with a table's
-- overhead. A financial posting and a DSAR are never dead-lettered — both halt and alert
CREATE TABLE IF NOT EXISTS platform.dead_letter (
    id                                uuid NOT NULL,
    outbox_id                         uuid,
    event_name                        text,
    consumer                          text,
    payload                           jsonb,
    attempts                          integer,
    last_error                        text,
    last_attempt_at                   timestamptz,
    replay_count                      integer DEFAULT 0,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz NOT NULL,
    CONSTRAINT dead_letter_pkey PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- Cash denominations per region (Tanmay, review 20 August). isActive is the field that makes this
-- a table — a note withdrawn from circulation is deactivated and stays in the count history, and a
-- JSON blob cannot deactivate anything
CREATE TABLE IF NOT EXISTS platform.denomination (
    id                                uuid PRIMARY KEY,
    currency_code                     text NOT NULL,
    display_name                      text,
    kind                              text NOT NULL CONSTRAINT denomination_kind_chk CHECK (kind IN ('note', 'coin')),
    sort_order                        integer,
    is_active                         boolean DEFAULT true,
    face_value_amount                 numeric(18,4) NOT NULL
);

-- A physical thing that authenticates and does not authorise — a scanner, a printer, a kitchen
-- display. It proves which device; the person proves what they may do
CREATE TABLE IF NOT EXISTS platform.device (
    state                             text NOT NULL CONSTRAINT device_state_chk CHECK (state IN ('enrolled', 'provisioned', 'active', 'deactivated', 'retired')),
    reason                            text,
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT device_kind_chk CHECK (kind IN ('receiptPrinter', 'ticketPrinter', 'labelPrinter', 'cashDrawer', 'barcodeScanner', 'rfidReader', 'nfcReader', 'cardReader', 'idReader', 'biometricReader', 'accessReader', 'paymentTerminal', 'customerDisplay', 'signageDisplay', 'kitchenDisplay', 'turnstileController', 'wristbandEncoder', 'signaturePad', 'scale', 'camera', 'mobileHandset')),
    driver                            text NOT NULL,
    identifier                        text,
    workstation_id                    uuid,
    model                             text,
    push_token                        text,
    push_platform                     text CONSTRAINT device_push_platform_chk CHECK (push_platform IN ('ios', 'android', 'web', 'windows')),
    push_failure_count                integer DEFAULT 0,
    offline_scope                     text CONSTRAINT device_offline_scope_chk CHECK (offline_scope IN ('none', 'readOnly', 'sellAndScan', 'fullVenue')),
    firmware_version                  text,
    is_required                       boolean,
    status                            text CONSTRAINT device_status_chk CHECK (status IN ('online', 'offline', 'error', 'consumableLow', 'needsAttention', 'unknown')),
    battery_percent                   integer,
    last_checked_at                   timestamptz,
    health                            text DEFAULT 'unknown' CONSTRAINT device_health_chk CHECK (health IN ('healthy', 'warning', 'degraded', 'offline', 'unknown')),
    last_heartbeat_at                 timestamptz,
    capabilities                      text[],
    enrolment_state                   text DEFAULT 'registered' CONSTRAINT device_enrolment_state_chk CHECK (enrolment_state IN ('registered', 'enrolled', 'provisioned', 'active', 'deactivated', 'retired')),
    retired_at                        timestamptz,
    configuration_profile_id          uuid
);

-- high-volume, short-lived. Trimmed by retention Hangs off: a child of platform.device; reaches
-- platform.scope through its keys; references platform.device. Reached by: 1 operations read it
-- and 0 write it.
CREATE TABLE IF NOT EXISTS platform.device_heartbeat (
    id                                uuid PRIMARY KEY NOT NULL,
    device_id                         uuid
);

-- A data-subject request and its progress. The reason pii is a schema of its own
CREATE TABLE IF NOT EXISTS platform.dsar_request (
    id                                uuid PRIMARY KEY,
    request_id                        uuid NOT NULL,
    guest_link_id                     uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT dsar_request_kind_chk CHECK (kind IN ('access', 'rectification', 'erasure', 'portability', 'restriction')),
    status                            text NOT NULL CONSTRAINT dsar_request_status_chk CHECK (status IN ('pending', 'inProgress', 'completed', 'partiallyFailed')),
    created_at                        timestamptz NOT NULL,
    completed_at                      timestamptz
);

-- A pseudonymous link between cells (ADR-0010). Carries no personal data, which is the point
CREATE TABLE IF NOT EXISTS platform.guest_link (
    guest_link_id                     uuid PRIMARY KEY NOT NULL,
    home_cell_name                    text NOT NULL,
    consent_version                   text NOT NULL,
    linked_at                         timestamptz NOT NULL,
    revoked_at                        timestamptz
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS platform.idempotency_record (
    id                                uuid PRIMARY KEY NOT NULL,
    idempotency_key                   uuid NOT NULL,
    operation_id                      text NOT NULL CONSTRAINT idempotency_record_operation_id_chk CHECK (char_length(operation_id) <= 100),
    request_hash                      text NOT NULL CONSTRAINT idempotency_record_request_hash_chk CHECK (char_length(request_hash) <= 64),
    status                            text NOT NULL CONSTRAINT idempotency_record_status_chk CHECK (status IN ('inProgress', 'completed')),
    response_status                   integer,
    response_body                     jsonb,
    principal_id                      uuid,
    created_at                        timestamptz NOT NULL,
    expires_at                        timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- What a workstation may do with no network, and for how long (Board 5). A till three days offline
-- holding 900 unsynced sales is a reconciliation nobody can do. Hangs off: reaches platform.scope
-- through its keys. Reached by: 2 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS platform.offline_policy (
    id                                uuid PRIMARY KEY,
    scope_path                        ltree NOT NULL,
    max_offline_hours                 integer DEFAULT 24,
    allowed_offline                   text[],
    offline_value_ceiling             numeric(18,4),
    offline_transaction_ceiling       integer,
    on_ceiling_breach                 text DEFAULT 'blockNewSales' CONSTRAINT offline_policy_on_ceiling_breach_chk CHECK (on_ceiling_breach IN ('warn', 'blockNewSales', 'blockAll')),
    requires_manager_to_extend        boolean DEFAULT true
);

-- Written in the same transaction as the state change, by the platform, not by an operation. That
-- is what makes it exactly-once Hangs off: reaches platform.scope through its keys; references
-- catalogue.event, platform.tenant. Reached by: 3 operations read it and 97 write it; 1 tables
-- reference it; written by 20 contracts — access, accreditation, approvals, catalogue.
CREATE TABLE IF NOT EXISTS platform.outbox (
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
    trace_id                          text CONSTRAINT outbox_trace_id_chk CHECK (char_length(trace_id) <= 64),
    published_at                      timestamptz,
    attempts                          integer DEFAULT 0,
    last_error                        text,
    created_at                        timestamptz NOT NULL,
    CONSTRAINT outbox_pkey PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- A commercial branch — a restaurant, a shop, a bar. A sibling of department rather than a child
-- (CF-138, ADR-0018): a department has requisitions and rotas, an outlet has a menu and stock, and
-- modelling a restaurant as a department puts it in the staffing tree
CREATE TABLE IF NOT EXISTS platform.outlet (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT outlet_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT outlet_name_chk CHECK (char_length(name) <= 200),
    venue_id                          uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT outlet_kind_chk CHECK (kind IN ('shop', 'restaurant', 'bar', 'cafe', 'kiosk', 'gameFloor', 'ticketOffice', 'mobile')),
    zone                              text,
    stock_location_id                 uuid,
    cost_center_id                    uuid,
    is_active                         boolean
);

-- A profile version pushed to a fleet. onNextIdle by default — a profile landing mid-sale is a
-- guest watching a till restart
CREATE TABLE IF NOT EXISTS platform.profile_deployment (
    id                                uuid PRIMARY KEY NOT NULL,
    profile_id                        uuid NOT NULL,
    version                           integer NOT NULL,
    target_workstation_ids            text[],
    target_filter                     jsonb,
    strategy                          text DEFAULT 'onNextIdle' CONSTRAINT profile_deployment_strategy_chk CHECK (strategy IN ('immediate', 'staged', 'onNextIdle')),
    status                            text NOT NULL CONSTRAINT profile_deployment_status_chk CHECK (status IN ('queued', 'inProgress', 'completed', 'partiallyFailed', 'rolledBack')),
    succeeded_count                   integer,
    failed_count                      integer,
    failure_reasons                   jsonb,
    started_at                        timestamptz,
    completed_at                      timestamptz
);

-- Currency, scale, timezone, fiscal year. Region-scoped and not overridable below
CREATE TABLE IF NOT EXISTS platform.region_settings (
    country_code                      text NOT NULL,
    currency_code                     text NOT NULL,
    currency_scale                    integer NOT NULL,
    time_zone                         text NOT NULL,
    date_format                       text DEFAULT 'dd/MM/yyyy',
    number_format                     text DEFAULT '#,##0.00',
    fiscal_year_start_month           integer NOT NULL,
    allowed_ai_residencies            text[],
    placement                         jsonb,
    cell_name                         text,
    id                                uuid PRIMARY KEY NOT NULL,
    org_unit_id                       uuid
);

-- What a till shows and in what order. Configured by the venue, not by code
CREATE TABLE IF NOT EXISTS platform.sale_board (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT sale_board_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT sale_board_name_chk CHECK (char_length(name) <= 200),
    venue_id                          uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT sale_board_kind_chk CHECK (kind IN ('ticketing', 'fnb', 'retail', 'mixed')),
    is_active                         boolean
);

-- One page of a till board, holding tiles in position
CREATE TABLE IF NOT EXISTS platform.sale_board_page (
    sale_board_id                     uuid NOT NULL,
    name                              text NOT NULL,
    sort_order                        integer NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Child of sale_board_page, which is a child of sale_board. Two levels down, returned nested Hangs
-- off: reaches platform.scope through its keys; references platform.sale_board_page. Reached by: 1
-- operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS platform.sale_board_tile (
    id                                uuid PRIMARY KEY NOT NULL,
    page_id                           uuid
);

-- One unit of the venue structure — a tenant, a brand, a region, a venue, a department, a
-- sub-department, a workstation or an outlet. Every row has a level, a parent and a materialised
-- path, and configuration resolves by walking that path upward until something answers. Renamed
-- from org_unit on 26 August: *node* said it was a tree and hid what the tree is of. A row is an
-- org unit; a scope_path is a
CREATE TABLE IF NOT EXISTS platform.scope (
    id                                uuid PRIMARY KEY NOT NULL,
    level                             text NOT NULL CONSTRAINT scope_level_chk CHECK (level IN ('tenant', 'brand', 'region', 'venue', 'department', 'subDepartment', 'workstation', 'outlet')),
    parent_id                         uuid,
    path                              ltree NOT NULL,
    code                              text NOT NULL CONSTRAINT scope_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT scope_name_chk CHECK (char_length(name) <= 200),
    is_active                         boolean NOT NULL,
    child_count                       integer
);

-- read-only projection of control.tenant, outside every cell Hangs off: reaches platform.scope
-- through its keys; references platform.scope. Reached by: 2 operations read it and 0 write it; 19
-- tables reference it.
CREATE TABLE IF NOT EXISTS platform.tenant (
    id                                uuid PRIMARY KEY NOT NULL,
    home_region_id                    uuid
);

-- read through composed tenancy operations Hangs off: reaches platform.scope through its keys;
-- references platform.scope. Reached by: 6 operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS platform.venue_settings (
    id                                uuid PRIMARY KEY,
    venue_id                          uuid,
    calendar_day_start_hour           integer DEFAULT 6,
    currency_code                     text,
    currency_scale                    integer,
    support_hours                     jsonb,
    quiet_hours                       jsonb,
    biometrics                        jsonb,
    segregated_access                 jsonb,
    alerting                          jsonb,
    display_currencies                text[],
    cart_lease_seconds                integer DEFAULT 900,
    cart_hold_extension_minutes       integer DEFAULT 5,
    cart_max_extensions               integer DEFAULT 1,
    resale_cutoff_hours               integer DEFAULT 24,
    exchange_cutoff_hours             integer DEFAULT 24,
    reschedule_cutoff_hours           integer DEFAULT 24,
    reservation_max_extensions        integer DEFAULT 1,
    shift_variance_threshold          numeric(18,4),
    catalogue                         jsonb,
    inventory                         jsonb,
    seating                           jsonb,
    promotions                        jsonb,
    fnb                               jsonb,
    queue                             jsonb,
    reporting                         jsonb,
    marketing                         jsonb,
    identity                          jsonb,
    org_unit_id                       uuid NOT NULL
);

-- A hold on a balance held in another jurisdiction, with the rate it converted at fixed on
-- authorisation rather than capture
CREATE TABLE IF NOT EXISTS platform.wallet_authorisation (
    mode                              text NOT NULL CONSTRAINT wallet_authorisation_mode_chk CHECK (mode IN ('none', 'fixed', 'percentageOfBalance')),
    allocated_amount                  numeric(18,4),
    drawn_amount                      numeric(18,4),
    available_amount                  numeric(18,4) NOT NULL,
    last_topped_up_at                 timestamptz,
    allocation_currency               text,
    id                                uuid PRIMARY KEY,
    authorisation_id                  text NOT NULL,
    guest_link_id                     uuid NOT NULL,
    amount                            numeric(18,4) NOT NULL,
    captured_amount                   numeric(18,4),
    status                            text NOT NULL CONSTRAINT wallet_authorisation_status_chk CHECK (status IN ('held', 'captured', 'partiallyCaptured', 'released', 'expired')),
    home_cell_name                    text,
    consuming_cell_name               text,
    order_id                          uuid,
    wallet_hold_id                    uuid,
    created_at                        timestamptz NOT NULL,
    expires_at                        timestamptz NOT NULL,
    home_currency                     text,
    consuming_currency                text,
    fx_rate                           numeric(18,4),
    fx_rate_id                        uuid,
    fx_rate_source                    text,
    amount_in_consuming_currency      numeric(18,4),
    fx_purpose                        text
);

-- A till, a scanner, a kiosk — a place work happens. The lowest organisational level. Authority is
-- the person’s, not the workstation’s (ADR-0002), which is what makes a shared handheld safe
CREATE TABLE IF NOT EXISTS platform.workstation (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT workstation_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT workstation_name_chk CHECK (char_length(name) <= 200),
    venue_id                          uuid NOT NULL,
    region_id                         uuid NOT NULL,
    department_id                     uuid,
    scope_path                        ltree NOT NULL,
    sale_board                        jsonb NOT NULL,
    access_point_id                   uuid,
    time_zone                         text NOT NULL,
    deployment_profile                text CONSTRAINT workstation_deployment_profile_chk CHECK (deployment_profile IN ('terminalLocal', 'venueEdge', 'thin')),
    edge_node_id                      uuid,
    health_score                      integer,
    configuration_profile_id          uuid,
    is_offline_capable                boolean,
    is_active                         boolean,
    org_unit_id                       uuid NOT NULL
);

