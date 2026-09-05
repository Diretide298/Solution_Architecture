-- reporting — 13 tables
-- **Derived. Do not hand-edit.**

-- A rule that fired. Acknowledged rather than dismissed — an alert that disappears when clicked
-- leaves nobody accountable for what happened next
CREATE TABLE IF NOT EXISTS reporting.alert (
    id                                uuid PRIMARY KEY NOT NULL,
    rule_id                           uuid NOT NULL,
    raised_at                         timestamptz NOT NULL,
    severity                          text NOT NULL,
    status                            text NOT NULL,
    observed_value                    numeric(18,4),
    threshold                         numeric(18,4),
    scope_path                        text,
    acknowledged_by_principal_id      uuid,
    acknowledged_at                   timestamptz,
    resolved_at                       timestamptz,
    escalated_at                      timestamptz
);

-- Raises an alert when a number leaves a range (BL-152, CF-134). MessageTrigger seen from the
-- operational side — a message trigger fires on an event, this fires on a threshold
CREATE TABLE IF NOT EXISTS reporting.alert_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    metric                            text NOT NULL,
    comparator                        text NOT NULL,
    threshold                         numeric(18,4) NOT NULL,
    threshold_upper                   numeric(18,4),
    window_minutes                    integer,
    severity                          text NOT NULL,
    deliver_to                        text[],
    recipient_role_ids                text[],
    cooldown_minutes                  integer,
    is_active                         boolean NOT NULL,
    scope_path                        text
);

-- An arrangement of tiles, each resolving its own source
CREATE TABLE IF NOT EXISTS reporting.dashboard (
    name                              text,
    description                       text,
    venue_id                          uuid,
    is_shared                         boolean,
    id                                uuid PRIMARY KEY,
    owner_principal_id                uuid,
    aggregate_cost                    text,
    created_at                        timestamptz
);

-- One panel, and the query behind it
CREATE TABLE IF NOT EXISTS reporting.dashboard_tile (
    dashboard_id                      uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    title                             text,
    report_id                         uuid NOT NULL,
    visualisation                     text NOT NULL,
    parameters                        jsonb,
    refresh_seconds                   integer,
    position                          jsonb NOT NULL
);

-- One run of a report definition. The result set is cached in object storage, not here
CREATE TABLE IF NOT EXISTS reporting.execution (
    id                                text PRIMARY KEY NOT NULL,
    report_id                         uuid NOT NULL,
    report_name                       text,
    definition_version                text NOT NULL,
    status                            text NOT NULL,
    parameters                        jsonb,
    scope_applied                     text[],
    row_count                         integer,
    duration_ms                       integer,
    error                             text,
    requested_by_principal_id         uuid NOT NULL,
    schedule_id                       uuid,
    requested_at                      timestamptz NOT NULL,
    completed_at                      timestamptz,
    expires_at                        timestamptz
);

-- A file somebody asked for, with an expiry
CREATE TABLE IF NOT EXISTS reporting.export (
    id                                text PRIMARY KEY NOT NULL,
    execution_id                      text NOT NULL,
    format                            text NOT NULL,
    status                            text NOT NULL,
    includes_personal_data            boolean,
    purpose                           text,
    download_url                      text,
    size_bytes                        integer,
    requested_by_principal_id         uuid NOT NULL,
    requested_at                      timestamptz NOT NULL,
    expires_at                        timestamptz
);

-- One column of a definition, with its aggregation
CREATE TABLE IF NOT EXISTS reporting.report_column (
    report_definition_id              uuid NOT NULL,
    id                                uuid PRIMARY KEY,
    field                             text NOT NULL,
    label                             text,
    aggregation                       text,
    sort_order                        integer,
    sort_direction                    text,
    format                            text,
    definition_id                     uuid NOT NULL
);

-- A saved question, not its answer. Columns, filters and parameters are children; a run is an
-- execution, and the result set is cached in object storage rather than here
CREATE TABLE IF NOT EXISTS reporting.report_definition (
    name                              text,
    description                       text,
    category                          text,
    data_source                       text,
    group_by                          text[],
    required_permission               text,
    max_date_range_days               integer,
    id                                uuid PRIMARY KEY,
    version                           text,
    is_system                         boolean,
    is_retired                        boolean,
    estimated_cost                    text,
    created_by_principal_id           uuid,
    created_at                        timestamptz,
    last_run_at                       timestamptz,
    scope_path                        text
);

-- Generated, not stored. ReportField declares persistence: none — metadata catalogue, generated:
-- the fields a report may use are read off the DataSource at build time, and a stored catalogue
-- and a schema that disagree is a builder offering fields that no longer exist. Retrievable so a
-- report can be found by what it answers
CREATE TABLE IF NOT EXISTS reporting.report_field (
    id                                uuid PRIMARY KEY NOT NULL,
    definition_id                     uuid NOT NULL
);

-- A condition applied before aggregation. Hangs off: a child of reporting.report_definition;
-- reaches reporting.report_definition through its keys; references reporting.report_definition.
-- Reached by: 5 operations read it and 4 write it.
CREATE TABLE IF NOT EXISTS reporting.report_filter (
    report_definition_id              uuid NOT NULL,
    id                                uuid PRIMARY KEY,
    field                             text NOT NULL,
    operator                          text NOT NULL,
    value                             text,
    values                            text[],
    is_parameter                      boolean,
    definition_id                     uuid NOT NULL
);

-- Something the reader supplies at run time. Hangs off: reaches reporting.report_definition
-- through its keys; references reporting.report_definition. Reached by: 5 operations read it and 3
-- write it.
CREATE TABLE IF NOT EXISTS reporting.report_parameter (
    key                               text NOT NULL,
    label                             text NOT NULL,
    type                              text NOT NULL,
    is_required                       boolean NOT NULL,
    default_value                     text,
    id                                uuid PRIMARY KEY NOT NULL,
    definition_id                     uuid NOT NULL
);

-- When a report runs and who receives it. Hangs off: reaches reporting.report_definition through
-- its keys; references identity.principal, reporting.report_definition. Reached by: 4 operations
-- read it and 3 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS reporting.schedule (
    report_id                         uuid,
    name                              text,
    cadence                           jsonb,
    parameters                        jsonb,
    format                            text,
    include_personal_data             boolean,
    skip_if_empty                     boolean,
    id                                uuid PRIMARY KEY,
    owner_principal_id                uuid,
    is_paused                         boolean,
    last_run_at                       timestamptz,
    last_run_status                   text,
    next_run_at                       timestamptz,
    consecutive_failures              integer,
    created_at                        timestamptz
);

-- Who receives a scheduled report, which is a consent question as well as a distribution one
CREATE TABLE IF NOT EXISTS reporting.schedule_recipient (
    kind                              text NOT NULL,
    address                           text NOT NULL,
    principal_id                      uuid,
    id                                uuid PRIMARY KEY NOT NULL
);

