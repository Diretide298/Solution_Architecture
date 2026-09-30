-- workforce — 28 tables
-- **Derived. Do not hand-edit.**

-- Targeted by venue, department or role. emergency is not a louder operational Hangs off: reaches
-- workforce.employee through its keys; references identity.principal, platform.scope. Reached by:
-- 3 operations read it and 2 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS workforce.announcement (
    id                                uuid PRIMARY KEY,
    title                             text NOT NULL CONSTRAINT announcement_title_chk CHECK (char_length(title) <= 140),
    body                              text NOT NULL CONSTRAINT announcement_body_chk CHECK (char_length(body) <= 4000),
    kind                              text NOT NULL CONSTRAINT announcement_kind_chk CHECK (kind IN ('operational', 'safety', 'emergency', 'hr', 'celebration')),
    venue_ids                         text[],
    department_ids                    text[],
    role_ids                          text[],
    requires_acknowledgement          boolean,
    delivery_channels                 text[],
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
-- references access.access_point, identity.principal, platform.scope. Reached by: 5 operations
-- read it and 2 write it.
CREATE TABLE IF NOT EXISTS workforce.attendance (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid NOT NULL,
    assignment_id                     uuid,
    venue_id                          uuid,
    kind                              text NOT NULL CONSTRAINT attendance_kind_chk CHECK (kind IN ('clockIn', 'clockOut', 'breakStart', 'breakEnd')),
    occurred_at                       timestamptz NOT NULL,
    recorded_at                       timestamptz,
    access_point_id                   uuid,
    latitude                          numeric(18,4),
    longitude                         numeric(18,4),
    is_amended                        boolean,
    amended_by_principal_id           uuid,
    amendment_reason                  text,
    original_occurred_at              timestamptz,
    exception                         text CONSTRAINT attendance_exception_chk CHECK (exception IN ('late', 'earlyLeave', 'missingClockOut', 'noShow', 'outOfGeofence', 'unscheduled'))
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.attendance_amendment (
    id                                uuid PRIMARY KEY NOT NULL,
    attendance_record_id              uuid NOT NULL,
    amended_by_principal_id           uuid NOT NULL,
    amended_at                        timestamptz NOT NULL,
    occurred_at_before                timestamptz NOT NULL,
    occurred_at_after                 timestamptz NOT NULL,
    reason                            text NOT NULL CONSTRAINT attendance_amendment_reason_chk CHECK (char_length(reason) <= 300)
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.employee (
    id                                uuid PRIMARY KEY,
    tenant_id                         uuid NOT NULL,
    principal_id                      uuid,
    code                              text NOT NULL CONSTRAINT employee_code_chk CHECK (char_length(code) <= 50),
    first_name                        text NOT NULL CONSTRAINT employee_first_name_chk CHECK (char_length(first_name) <= 100),
    last_name                         text NOT NULL CONSTRAINT employee_last_name_chk CHECK (char_length(last_name) <= 100),
    email                             text CONSTRAINT employee_email_chk CHECK (char_length(email) <= 254),
    mobile                            text CONSTRAINT employee_mobile_chk CHECK (char_length(mobile) <= 30),
    date_of_joining                   date NOT NULL,
    date_of_birth                     date,
    employment_type                   text NOT NULL CONSTRAINT employee_employment_type_chk CHECK (char_length(employment_type) <= 30),
    employment_status                 text NOT NULL CONSTRAINT employee_employment_status_chk CHECK (char_length(employment_status) <= 30),
    manager_employee_id               uuid,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.employment (
    id                                uuid PRIMARY KEY,
    employee_id                       uuid NOT NULL,
    contract_type                     text NOT NULL CONSTRAINT employment_contract_type_chk CHECK (char_length(contract_type) <= 30),
    start_date                        date NOT NULL,
    end_date                          date,
    standard_hours_per_week           numeric(18,4),
    probation_end_date                date,
    status                            text NOT NULL CONSTRAINT employment_status_chk CHECK (char_length(status) <= 30),
    created_at                        timestamptz NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.field_ownership (
    id                                uuid PRIMARY KEY,
    table_name                        text NOT NULL CONSTRAINT field_ownership_table_name_chk CHECK (char_length(table_name) <= 120),
    column_name                       text NOT NULL CONSTRAINT field_ownership_column_name_chk CHECK (char_length(column_name) <= 120),
    master                            text NOT NULL CONSTRAINT field_ownership_master_chk CHECK (master IN ('ticvai', 'external')),
    source_id                         uuid,
    on_conflict                       text CONSTRAINT field_ownership_on_conflict_chk CHECK (on_conflict IN ('externalWins', 'ticvaiWins', 'flagForReview')),
    scope_path                        ltree NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.forecast_requirement (
    id                                uuid PRIMARY KEY,
    requirement_id                    uuid NOT NULL,
    version_id                        uuid NOT NULL,
    venue_id                          uuid,
    position_code                     text,
    period_start                      timestamptz NOT NULL,
    period_end                        timestamptz NOT NULL,
    quantity                          numeric(18,4) NOT NULL,
    quantity_p90                      numeric(18,4),
    unit                              text,
    received_at                       timestamptz,
    superseded_at                     timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.integration_source (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL CONSTRAINT integration_source_code_chk CHECK (char_length(code) <= 60),
    name                              text NOT NULL CONSTRAINT integration_source_name_chk CHECK (char_length(name) <= 150),
    kind                              text NOT NULL CONSTRAINT integration_source_kind_chk CHECK (kind IN ('hrms', 'workforceManagement', 'payroll', 'timeAndAttendance', 'identity', 'staffingAgency')),
    transport                         text NOT NULL CONSTRAINT integration_source_transport_chk CHECK (transport IN ('api', 'webhook', 'scheduled', 'manual', 'fileImport')),
    authentication_status             text CONSTRAINT integration_source_authentication_status_chk CHECK (authentication_status IN ('healthy', 'expiring', 'expired', 'failed', 'notConfigured')),
    last_synchronised_at              timestamptz,
    status                            text NOT NULL CONSTRAINT integration_source_status_chk CHECK (status IN ('active', 'degraded', 'suspended')),
    scope_path                        ltree NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.job_title (
    id                                uuid PRIMARY KEY,
    tenant_id                         uuid NOT NULL,
    code                              text NOT NULL CONSTRAINT job_title_code_chk CHECK (char_length(code) <= 50),
    name                              text NOT NULL CONSTRAINT job_title_name_chk CHECK (char_length(name) <= 150),
    description                       text CONSTRAINT job_title_description_chk CHECK (char_length(description) <= 500),
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.labour_budget (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    department_id                     uuid,
    period_start                      date NOT NULL,
    period_end                        date NOT NULL,
    budget_amount                     numeric(18,4) NOT NULL,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
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
    kind                              text NOT NULL CONSTRAINT leave_request_kind_chk CHECK (kind IN ('annual', 'sick', 'unpaid', 'parental', 'compassionate', 'training', 'timeOffInLieu')),
    valid_from                        date NOT NULL,
    valid_to                          date NOT NULL,
    half_day                          boolean DEFAULT false,
    reason                            text,
    status                            text CONSTRAINT leave_request_status_chk CHECK (status IN ('requested', 'approved', 'rejected', 'cancelled', 'taken')),
    approval_request_id               uuid,
    scope_path                        ltree NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.leave_type (
    id                                uuid PRIMARY KEY,
    tenant_id                         uuid NOT NULL,
    code                              text NOT NULL CONSTRAINT leave_type_code_chk CHECK (char_length(code) <= 50),
    name                              text NOT NULL CONSTRAINT leave_type_name_chk CHECK (char_length(name) <= 100),
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
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    released_by                       uuid,
    reason                            text,
    required_qualifications           text[],
    eligible_principal_count          integer,
    incentive_rate_multiplier         numeric(18,4),
    status                            text CONSTRAINT open_shift_status_chk CHECK (status IN ('open', 'claimed', 'pendingApproval', 'filled', 'expired', 'withdrawn')),
    claimed_by                        uuid,
    claimed_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.position_requirement (
    staffing_rules_id                 uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    position_code                     text NOT NULL,
    label                             text,
    venue_id                          uuid,
    attraction_id                     uuid,
    minimum_headcount                 integer NOT NULL,
    days_of_week                      text[],
    starts_at                         text,
    ends_at                           text,
    required_qualifications           text[],
    applies_when_open                 boolean,
    blocks_operation                  boolean
);

-- A person expected somewhere at a time. Not a shift — a shift is a cash session, and most people
-- on a rota never touch a till Hangs off: reaches workforce.employee through its keys; references
-- identity.principal, identity.role, platform.scope. Reached by: 10 operations read it and 2 write
-- it; 3 tables reference it.
CREATE TABLE IF NOT EXISTS workforce.rota_assignment (
    overtime_minutes                  integer,
    rest_period_before                integer,
    breaches_working_hour_limit       boolean DEFAULT false,
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
    status                            text CONSTRAINT rota_assignment_status_chk CHECK (status IN ('planned', 'published', 'confirmed', 'swapPending', 'cancelled', 'completed', 'noShow')),
    break_minutes                     integer,
    note                              text
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.shift (
    id                                uuid PRIMARY KEY,
    tenant_id                         uuid NOT NULL,
    code                              text NOT NULL CONSTRAINT shift_code_chk CHECK (char_length(code) <= 50),
    name                              text NOT NULL CONSTRAINT shift_name_chk CHECK (char_length(name) <= 100),
    start_time                        text NOT NULL,
    end_time                          text NOT NULL,
    break_minutes                     integer NOT NULL,
    crosses_midnight                  boolean NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz
);

-- Both parties agree before the supervisor sees it. Routed through approvals rather than a second
-- mechanism Hangs off: reaches workforce.employee through its keys; references approvals.request,
-- identity.principal, workforce.rota_assignment. Reached by: 2 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS workforce.shift_swap (
    id                                uuid PRIMARY KEY NOT NULL,
    assignment_id                     uuid NOT NULL,
    from_principal_id                 uuid NOT NULL,
    to_principal_id                   uuid NOT NULL,
    status                            text NOT NULL CONSTRAINT shift_swap_status_chk CHECK (status IN ('awaitingPeer', 'awaitingApproval', 'approved', 'rejected', 'withdrawn')),
    approval_request_id               uuid,
    reason                            text,
    requested_at                      timestamptz
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.shift_template (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    kind                              text CONSTRAINT shift_template_kind_chk CHECK (kind IN ('early', 'late', 'middle', 'split', 'double', 'night', 'onCall', 'overtime')),
    starts_at                         text,
    ends_at                           text,
    required_qualifications           text[],
    role_code                         text,
    cost_centre                       text,
    hourly_rate                       numeric(18,4),
    scope_path                        ltree NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.staff_conversation (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    kind                              text NOT NULL CONSTRAINT staff_conversation_kind_chk CHECK (kind IN ('direct', 'group')),
    title                             text CONSTRAINT staff_conversation_title_chk CHECK (char_length(title) <= 120),
    created_by_principal_id           uuid NOT NULL,
    created_at                        timestamptz NOT NULL,
    last_message_at                   timestamptz
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.staff_conversation_participant (
    staff_conversation_id             uuid NOT NULL,
    principal_id                      uuid NOT NULL,
    joined_at                         timestamptz NOT NULL,
    last_read_message_id              uuid,
    muted_until                       timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.staff_message (
    id                                uuid PRIMARY KEY NOT NULL,
    staff_conversation_id             uuid NOT NULL,
    sender_principal_id               uuid NOT NULL,
    body                              text NOT NULL CONSTRAINT staff_message_body_chk CHECK (char_length(body) <= 2000),
    attachment_asset_id               uuid,
    sent_at                           timestamptz NOT NULL,
    received_at                       timestamptz
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
    default_incentive_rate_multiplier numeric(18,4),
    maximum_incentive_rate_multiplier numeric(18,4),
    incentive_approval_above          numeric(18,4),
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.sync_conflict (
    id                                uuid PRIMARY KEY,
    source_id                         uuid NOT NULL,
    sync_run_id                       uuid,
    kind                              text NOT NULL CONSTRAINT sync_conflict_kind_chk CHECK (kind IN ('missingInTicvai', 'missingExternally', 'venueChangedExternally', 'certificationExpired', 'terminatedExternally', 'fieldDisagreement')),
    employee_id                       uuid,
    external_reference                text CONSTRAINT sync_conflict_external_reference_chk CHECK (char_length(external_reference) <= 200),
    detail                            text CONSTRAINT sync_conflict_detail_chk CHECK (char_length(detail) <= 1000),
    affected_assignment_ids           text[],
    status                            text NOT NULL CONSTRAINT sync_conflict_status_chk CHECK (status IN ('open', 'retried', 'reprocessed', 'escalated', 'resolved', 'ignored')),
    raised_at                         timestamptz NOT NULL,
    resolved_at                       timestamptz,
    resolved_by_principal_id          uuid,
    scope_path                        ltree NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.sync_run (
    id                                uuid PRIMARY KEY,
    source_id                         uuid NOT NULL,
    started_at                        timestamptz NOT NULL,
    finished_at                       timestamptz,
    status                            text NOT NULL CONSTRAINT sync_run_status_chk CHECK (status IN ('running', 'succeeded', 'partial', 'failed')),
    records_read                      integer,
    records_applied                   integer,
    records_failed                    integer,
    warning_count                     integer,
    mapping_error_count               integer,
    trigger                           text CONSTRAINT sync_run_trigger_chk CHECK (trigger IN ('scheduled', 'manual', 'webhook', 'fileImport')),
    scope_path                        ltree NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.training_record (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid,
    course_name                       text,
    is_required                       boolean,
    completed_at                      timestamptz,
    expires_at                        timestamptz,
    state                             text CONSTRAINT training_record_state_chk CHECK (state IN ('notStarted', 'inProgress', 'passed', 'failed', 'expired')),
    evidence_ref                      text
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS workforce.work_assignment (
    id                                uuid PRIMARY KEY,
    employee_id                       uuid NOT NULL,
    job_title_id                      uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    venue_id                          uuid,
    department_id                     uuid,
    outlet_id                         uuid,
    effective_from                    date NOT NULL,
    effective_to                      date,
    is_primary                        boolean NOT NULL,
    status                            text NOT NULL CONSTRAINT work_assignment_status_chk CHECK (char_length(status) <= 30),
    created_at                        timestamptz NOT NULL
);

