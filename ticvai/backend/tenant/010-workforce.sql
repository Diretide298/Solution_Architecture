-- workforce — 21 tables
-- **Derived. Do not hand-edit.**

-- Targeted by venue, department or role. emergency is not a louder operational Hangs off: reaches
-- workforce.employee through its keys; references identity.principal, platform.scope. Reached by:
-- 2 operations read it and 2 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS workforce.announcement (
    id                                uuid PRIMARY KEY,
    title                             text NOT NULL,
    body                              text NOT NULL,
    kind                              text NOT NULL,
    venue_ids                         text[],
    department_ids                    text[],
    role_ids                          text[],
    requires_acknowledgement          boolean,
    expires_at                        timestamptz,
    published_by_principal_id         uuid,
    published_at                      timestamptz NOT NULL,
    locale                            text,
    venue_id                          uuid NOT NULL
);

-- Delivered and acknowledged, per principal. The outstanding list is the roll call Hangs off: a
-- child of workforce.announcement; reaches workforce.employee through its keys; references
-- identity.principal, workforce.announcement. Reached by: 2 operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS workforce.announcement_receipt (
    id                                uuid PRIMARY KEY NOT NULL,
    announcement_id                   uuid NOT NULL,
    principal_id                      uuid NOT NULL
);

-- Who actually turned up. occurredAt and recordedAt are both kept — a steward clocking in offline
-- is not late because the sync was Hangs off: reaches workforce.employee through its keys;
-- references access.access_point, identity.principal, platform.scope. Reached by: 2 operations
-- read it and 2 write it.
CREATE TABLE IF NOT EXISTS workforce.attendance (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid NOT NULL,
    assignment_id                     uuid,
    venue_id                          uuid,
    kind                              text NOT NULL,
    occurred_at                       timestamptz NOT NULL,
    recorded_at                       timestamptz,
    access_point_id                   uuid,
    latitude                          numeric(18,4),
    longitude                         numeric(18,4),
    is_amended                        boolean,
    amended_by_principal_id           uuid,
    amendment_reason                  text,
    original_occurred_at              timestamptz,
    exception                         text
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.employee (
    id                                uuid PRIMARY KEY,
    tenant_id                         uuid NOT NULL,
    user_id                           uuid,
    code                              text NOT NULL,
    first_name                        text NOT NULL,
    last_name                         text NOT NULL,
    email                             text,
    mobile                            text,
    date_of_joining                   date NOT NULL,
    employment_type                   text NOT NULL,
    employment_status                 text NOT NULL,
    manager_employee_id               uuid,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.employment (
    id                                uuid PRIMARY KEY,
    employee_id                       uuid NOT NULL,
    contract_type                     text NOT NULL,
    start_date                        date NOT NULL,
    end_date                          date,
    standard_hours_per_week           numeric(18,4),
    probation_end_date                date,
    status                            text NOT NULL,
    created_at                        timestamptz NOT NULL
);

CREATE TABLE IF NOT EXISTS workforce.field_ownership (
    id                                uuid PRIMARY KEY,
    table_name                        text NOT NULL,
    column_name                       text NOT NULL,
    master                            text NOT NULL,
    source_id                         uuid,
    on_conflict                       text,
    scope_path                        text
);

CREATE TABLE IF NOT EXISTS workforce.integration_source (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    kind                              text NOT NULL,
    transport                         text NOT NULL,
    authentication_status             text,
    last_synchronised_at              timestamptz,
    status                            text NOT NULL,
    scope_path                        text
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.job_title (
    id                                uuid PRIMARY KEY,
    tenant_id                         uuid NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    description                       text,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.leave_balance (
    id                                uuid PRIMARY KEY,
    employee_id                       uuid NOT NULL,
    type_id                           uuid NOT NULL,
    period_year                       integer NOT NULL,
    entitled_days                     numeric(18,4) NOT NULL,
    used_days                         numeric(18,4) NOT NULL,
    pending_days                      numeric(18,4) NOT NULL,
    available_days                    numeric(18,4) NOT NULL,
    updated_at                        timestamptz NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.leave_request (
    id                                uuid PRIMARY KEY,
    principal_id                      uuid NOT NULL,
    kind                              text NOT NULL,
    "from"                            date NOT NULL,
    "to"                              date NOT NULL,
    half_day                          boolean,
    reason                            text,
    status                            text,
    approval_request_id               uuid,
    scope_path                        text
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.leave_type (
    id                                uuid PRIMARY KEY,
    tenant_id                         uuid NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    is_paid                           boolean NOT NULL,
    requires_approval                 boolean NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.open_shift (
    id                                uuid PRIMARY KEY,
    rota_assignment_id                uuid,
    shift_template_id                 uuid,
    venue_id                          uuid,
    position_code                     text,
    "from"                            timestamptz,
    "to"                              timestamptz,
    released_by                       uuid,
    reason                            text,
    required_qualifications           text[],
    eligible_principal_count          integer,
    incentive_rate_multiplier         numeric(18,4),
    status                            text,
    claimed_by                        uuid,
    claimed_at                        timestamptz,
    scope_path                        text
);

-- A person expected somewhere at a time. Not a shift — a shift is a cash session, and most people
-- on a rota never touch a till Hangs off: reaches workforce.employee through its keys; references
-- identity.principal, identity.role, platform.scope. Reached by: 6 operations read it and 2 write
-- it; 3 tables reference it.
CREATE TABLE IF NOT EXISTS workforce.rota_assignment (
    overtime_minutes                  integer,
    rest_period_before                integer,
    breaches_working_hour_limit       boolean,
    labour_cost                       numeric(18,4),
    id                                uuid PRIMARY KEY,
    principal_id                      uuid NOT NULL,
    display_name                      text,
    venue_id                          uuid NOT NULL,
    department_id                     uuid,
    position                          text NOT NULL,
    required_role_id                  uuid,
    workstation_id                    uuid,
    starts_at                         timestamptz NOT NULL,
    ends_at                           timestamptz NOT NULL,
    status                            text,
    break_minutes                     integer,
    note                              text
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.shift (
    id                                uuid PRIMARY KEY,
    tenant_id                         uuid NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    start_time                        text NOT NULL,
    end_time                          text NOT NULL,
    break_minutes                     integer NOT NULL,
    crosses_midnight                  boolean NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz
);

-- Both parties agree before the supervisor sees it. Routed through approvals rather than a second
-- mechanism Hangs off: reaches workforce.employee through its keys; references approvals.request,
-- identity.principal, workforce.rota_assignment. Reached by: 1 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS workforce.shift_swap (
    id                                uuid PRIMARY KEY NOT NULL,
    assignment_id                     uuid NOT NULL,
    from_principal_id                 uuid NOT NULL,
    to_principal_id                   uuid NOT NULL,
    status                            text NOT NULL,
    approval_request_id               text,
    reason                            text,
    requested_at                      timestamptz
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.shift_template (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    kind                              text,
    starts_at                         text,
    ends_at                           text,
    required_qualifications           text[],
    role_code                         text,
    cost_centre                       text,
    hourly_rate                       numeric(18,4),
    scope_path                        text
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.staffing_rules (
    maximum_hours_per_day             integer,
    maximum_hours_per_week            integer,
    minimum_rest_hours                integer,
    maximum_consecutive_days          integer,
    overtime                          jsonb,
    minimum_age_for_night_shift       integer,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

CREATE TABLE IF NOT EXISTS workforce.sync_conflict (
    id                                uuid PRIMARY KEY,
    source_id                         uuid NOT NULL,
    sync_run_id                       uuid,
    kind                              text NOT NULL,
    employee_id                       uuid,
    external_reference                text,
    detail                            text,
    affected_assignment_ids           text[],
    status                            text NOT NULL,
    raised_at                         timestamptz NOT NULL,
    resolved_at                       timestamptz,
    resolved_by_principal_id          uuid,
    scope_path                        text
);

CREATE TABLE IF NOT EXISTS workforce.sync_run (
    id                                uuid PRIMARY KEY,
    source_id                         uuid NOT NULL,
    started_at                        timestamptz NOT NULL,
    finished_at                       timestamptz,
    status                            text NOT NULL,
    records_read                      integer,
    records_applied                   integer,
    records_failed                    integer,
    warning_count                     integer,
    mapping_error_count               integer,
    trigger                           text,
    scope_path                        text
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.training_record (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid,
    course_name                       text,
    required                          boolean,
    completed_at                      timestamptz,
    expires_at                        timestamptz,
    state                             text,
    evidence_ref                      text
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.work_assignment (
    id                                uuid PRIMARY KEY,
    employee_id                       uuid NOT NULL,
    job_title_id                      uuid NOT NULL,
    scope_path                        text,
    venue_id                          uuid,
    department_id                     uuid,
    outlet_id                         uuid,
    effective_from                    date NOT NULL,
    effective_to                      date,
    is_primary                        boolean NOT NULL,
    status                            text NOT NULL,
    created_at                        timestamptz NOT NULL
);

