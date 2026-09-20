-- platform — 25 tables
-- **Derived. Do not hand-edit.**

-- PII reads only, written by the platform. Who looked at a passport number is the question a
-- regulator asks Hangs off: reaches platform.org_unit through its keys; references
-- identity.principal, pii.subject. Reached by: 0 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS platform.audit_read (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid NOT NULL,
    subject_id                        uuid NOT NULL
);

-- Written by the platform on every write, not by any one operation (ADR-0022 sits above this).
-- Naming it on 431 lineage rows would say nothing Hangs off: reaches platform.org_unit through its
-- keys; references identity.principal, platform.scope. Reached by: 1 operations read it and 2
-- write it; written by 2 contracts — inventory, tenancy.
CREATE TABLE IF NOT EXISTS platform.audit_record (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid NOT NULL,
    org_unit_id                       uuid NOT NULL
);

CREATE TABLE IF NOT EXISTS platform.cell_endpoint (
    id                                uuid PRIMARY KEY,
    cell_id                           uuid NOT NULL,
    service_name                      text NOT NULL,
    url                               text NOT NULL,
    contract_version                  text,
    authentication_type               text,
    credential_reference              text,
    status                            text NOT NULL,
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
    scope_path                        text,
    venue_kind_scope                  text[] NOT NULL,
    version                           integer NOT NULL,
    settings                          jsonb,
    status                            text NOT NULL,
    deployed_count                    integer,
    published_at                      timestamptz
);

-- When a workstation decides it is offline, and when it is back (Board 5). Asymmetric thresholds,
-- because symmetric ones make it flap across a marginal connection
CREATE TABLE IF NOT EXISTS platform.connectivity_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        text NOT NULL,
    failures_before_offline           integer,
    probe_interval_seconds            integer,
    probe_timeout_ms                  integer,
    successes_before_online           integer,
    minimum_stable_seconds            integer,
    auto_switch                       boolean
);

-- Something bought in one jurisdiction and honoured in another. ADR-0010: the guest does not move,
-- a pseudonymous link does. Renamed from cross_region_entitlement — a right to redeem what, and
-- where? Hangs off: reaches platform.org_unit through its keys; references access.admission_rules,
-- access.entitlement, platform.cross_region_entitlement. Reached by: 5 operations read it and 4
-- write it; 1 tables
CREATE TABLE IF NOT EXISTS platform.cross_region_entitlement (
    id                                uuid PRIMARY KEY,
    right_id                          text NOT NULL,
    ticket_id                         text NOT NULL,
    guest_link_id                     text,
    issuing_cell_name                 text NOT NULL,
    consuming_cell_name               text NOT NULL,
    media_codes                       text[],
    valid_from                        timestamptz NOT NULL,
    valid_to                          timestamptz NOT NULL,
    admission_rules_id                uuid,
    venue_id                          uuid,
    entries_allowed                   integer NOT NULL,
    entries_consumed                  integer NOT NULL,
    status                            text NOT NULL,
    last_consumed_at                  timestamptz,
    last_reconciled_at                timestamptz,
    admission_profile_id              uuid NOT NULL
);

-- An outbox row whose delivery failed after its retry budget (ADR-0033). Carries the payload
-- rather than a reference, because a dead letter you cannot replay is a log entry with a table's
-- overhead. A financial posting and a DSAR are never dead-lettered — both halt and alert
CREATE TABLE IF NOT EXISTS platform.dead_letter (
    id                                uuid PRIMARY KEY NOT NULL,
    outbox_id                         uuid,
    event_name                        text,
    consumer                          text,
    payload                           jsonb,
    attempts                          integer,
    last_error                        text,
    last_attempt_at                   timestamptz,
    replay_count                      integer,
    scope_path                        text,
    created_at                        timestamptz
);

-- Cash denominations per region (Tanmay, review 20 August). isActive is the field that makes this
-- a table — a note withdrawn from circulation is deactivated and stays in the count history, and a
-- JSON blob cannot deactivate anything
CREATE TABLE IF NOT EXISTS platform.denomination (
    id                                uuid PRIMARY KEY,
    currency_code                     text,
    display_name                      text,
    kind                              text,
    sort_order                        integer,
    is_active                         boolean,
    value                             numeric(18,4) NOT NULL,
    count                             integer NOT NULL
);

-- A physical thing that authenticates and does not authorise — a scanner, a printer, a kitchen
-- display. It proves which device; the person proves what they may do
CREATE TABLE IF NOT EXISTS platform.device (
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL,
    driver                            text NOT NULL,
    identifier                        text,
    workstation_id                    uuid NOT NULL,
    model                             text,
    push_token                        text,
    push_platform                     text,
    push_failure_count                integer,
    offline_scope                     text,
    firmware_version                  text,
    is_required                       boolean,
    status                            text,
    battery_percent                   integer,
    last_checked_at                   timestamptz,
    health                            text,
    last_heartbeat_at                 timestamptz
);

-- high-volume, short-lived. Trimmed by retention Hangs off: a child of platform.device; reaches
-- platform.org_unit through its keys; references platform.device. Reached by: 1 operations read it
-- and 0 write it.
CREATE TABLE IF NOT EXISTS platform.device_heartbeat (
    id                                uuid PRIMARY KEY NOT NULL,
    device_id                         uuid
);

-- A data-subject request and its progress. The reason pii is a schema of its own
CREATE TABLE IF NOT EXISTS platform.dsar_request (
    id                                uuid PRIMARY KEY,
    request_id                        text NOT NULL,
    guest_link_id                     text NOT NULL,
    kind                              text NOT NULL,
    status                            text NOT NULL,
    created_at                        timestamptz NOT NULL,
    completed_at                      timestamptz
);

-- A pseudonymous link between cells (ADR-0010). Carries no personal data, which is the point
CREATE TABLE IF NOT EXISTS platform.guest_link (
    guest_link_id                     text PRIMARY KEY NOT NULL,
    home_cell_name                    text NOT NULL,
    consent_version                   text NOT NULL,
    linked_at                         timestamptz NOT NULL,
    revoked_at                        timestamptz
);

-- What a workstation may do with no network, and for how long (Board 5). A till three days offline
-- holding 900 unsynced sales is a reconciliation nobody can do. Hangs off: reaches
-- platform.org_unit through its keys. Reached by: 1 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS platform.offline_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        text NOT NULL,
    max_offline_hours                 integer,
    allowed_offline                   text[],
    offline_value_ceiling             numeric(18,4),
    offline_transaction_ceiling       integer,
    on_ceiling_breach                 text,
    requires_manager_to_extend        boolean
);

-- Written in the same transaction as the state change, by the platform, not by an operation. That
-- is what makes it exactly-once Hangs off: reaches platform.org_unit through its keys. Reached by:
-- 2 operations read it and 22 write it; 1 tables reference it; written by 13 contracts — access,
-- approvals, catalogue, finance.
CREATE TABLE IF NOT EXISTS platform.outbox (
    id                                uuid PRIMARY KEY NOT NULL,
    event_name                        text NOT NULL,
    aggregate_type                    text,
    aggregate_id                      uuid,
    payload                           jsonb NOT NULL,
    scope_path                        text,
    sequence                          integer,
    published_at                      timestamptz,
    attempts                          integer,
    last_error                        text,
    created_at                        timestamptz NOT NULL
);

-- A commercial branch — a restaurant, a shop, a bar. A sibling of department rather than a child
-- (CF-138, ADR-0018): a department has requisitions and rotas, an outlet has a menu and stock, and
-- modelling a restaurant as a department puts it in the staffing tree
CREATE TABLE IF NOT EXISTS platform.outlet (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    kind                              text NOT NULL,
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
    strategy                          text,
    status                            text NOT NULL,
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
    date_format                       text,
    number_format                     text,
    fiscal_year_start_month           integer NOT NULL,
    placement                         jsonb,
    cell_name                         text,
    id                                uuid PRIMARY KEY NOT NULL,
    org_unit_id                       uuid
);

-- What a till shows and in what order. Configured by the venue, not by code
CREATE TABLE IF NOT EXISTS platform.sale_board (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    kind                              text NOT NULL,
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
-- off: reaches platform.org_unit through its keys; references platform.sale_board_page.
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
    level                             text NOT NULL,
    parent_id                         uuid,
    path                              text NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    is_active                         boolean NOT NULL,
    child_count                       integer
);

-- read-only projection of control.tenant, outside every cell Hangs off: reaches platform.org_unit
-- through its keys; references platform.scope. Reached by: 2 operations read it and 0 write it; 13
-- tables reference it.
CREATE TABLE IF NOT EXISTS platform.tenant (
    id                                uuid PRIMARY KEY NOT NULL,
    home_region_id                    uuid
);

-- read through composed tenancy operations Hangs off: reaches platform.org_unit through its keys;
-- references platform.scope. Reached by: 4 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS platform.venue_settings (
    id                                uuid PRIMARY KEY,
    venue_id                          uuid,
    support_hours                     jsonb,
    quiet_hours                       jsonb,
    segregated_access                 jsonb,
    alerting                          jsonb,
    org_unit_id                       uuid NOT NULL
);

-- A hold on a balance held in another jurisdiction, with the rate it converted at fixed on
-- authorisation rather than capture
CREATE TABLE IF NOT EXISTS platform.wallet_authorisation (
    mode                              text NOT NULL,
    allocated_amount                  numeric(18,4),
    drawn_amount                      numeric(18,4),
    available_amount                  numeric(18,4) NOT NULL,
    last_topped_up_at                 timestamptz,
    allocation_currency               text,
    id                                uuid PRIMARY KEY,
    authorisation_id                  text NOT NULL,
    guest_link_id                     text NOT NULL,
    amount                            numeric(18,4) NOT NULL,
    captured_amount                   numeric(18,4),
    status                            text NOT NULL,
    home_cell_name                    text,
    consuming_cell_name               text,
    order_id                          text,
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
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    region_id                         uuid NOT NULL,
    department_id                     uuid,
    scope_path                        text NOT NULL,
    sale_board                        jsonb NOT NULL,
    access_point_id                   uuid,
    time_zone                         text NOT NULL,
    deployment_profile                text,
    edge_node_id                      uuid,
    health_score                      integer,
    configuration_profile_id          uuid,
    catalogue_state                   jsonb,
    offline_capable                   boolean,
    is_active                         boolean,
    org_unit_id                       uuid NOT NULL
);

