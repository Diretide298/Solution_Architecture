-- reporting — 21 tables
-- **Derived. Do not hand-edit.**

-- A rule that fired. Acknowledged rather than dismissed — an alert that disappears when clicked
-- leaves nobody accountable for what happened next
CREATE TABLE IF NOT EXISTS reporting.alert (
    id                                uuid PRIMARY KEY NOT NULL,
    rule_id                           uuid NOT NULL,
    rule_name                         text,
    metric                            text,
    raised_at                         timestamptz NOT NULL,
    severity                          text NOT NULL CONSTRAINT alert_severity_chk CHECK (severity IN ('info', 'warning', 'critical')),
    status                            text NOT NULL CONSTRAINT alert_status_chk CHECK (status IN ('raised', 'acknowledged', 'resolved', 'expired')),
    observed_value                    numeric(18,4),
    threshold                         numeric(18,4),
    scope_path                        ltree NOT NULL,
    workstation_id                    uuid,
    shift_id                          uuid,
    item_id                           uuid,
    acknowledged_by_principal_id      uuid,
    acknowledged_at                   timestamptz,
    acknowledgement_note              text CONSTRAINT alert_acknowledgement_note_chk CHECK (char_length(acknowledgement_note) <= 300),
    resolved_at                       timestamptz,
    escalated_at                      timestamptz
);

-- Raises an alert when a number leaves a range (BL-152, CF-134). MessageTrigger seen from the
-- operational side — a message trigger fires on an event, this fires on a threshold
CREATE TABLE IF NOT EXISTS reporting.alert_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    metric                            text NOT NULL,
    comparator                        text NOT NULL CONSTRAINT alert_rule_comparator_chk CHECK (comparator IN ('above', 'below', 'outsideRange', 'changesBy', 'equals')),
    threshold                         numeric(18,4) NOT NULL,
    threshold_upper                   numeric(18,4),
    window_minutes                    integer DEFAULT 15,
    severity                          text NOT NULL CONSTRAINT alert_rule_severity_chk CHECK (severity IN ('info', 'warning', 'critical')),
    deliver_to                        text[],
    recipient_role_ids                text[],
    cooldown_minutes                  integer DEFAULT 30,
    is_active                         boolean NOT NULL,
    scope_path                        ltree NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS reporting.anomaly (
    id                                uuid PRIMARY KEY,
    kpi_id                            uuid,
    metric                            text,
    scope_path                        ltree NOT NULL,
    detected_at                       timestamptz,
    observed                          numeric(18,4),
    expected                          numeric(18,4),
    deviation_sigma                   numeric(18,4),
    severity                          text CONSTRAINT anomaly_severity_chk CHECK (severity IN ('low', 'medium', 'high')),
    acknowledged_by                   uuid,
    acknowledged_at                   timestamptz
);

-- An arrangement of tiles, each resolving its own source
CREATE TABLE IF NOT EXISTS reporting.dashboard (
    name                              text NOT NULL CONSTRAINT dashboard_name_chk CHECK (char_length(name) <= 200),
    module                            text NOT NULL CONSTRAINT dashboard_module_chk CHECK (module IN ('core', 'ticketing', 'access', 'fnb', 'retail', 'inventory', 'seating', 'membership', 'marketing', 'resources', 'queue', 'games', 'maintenance', 'accreditation', 'partner', 'developerApi', 'analytics', 'ai')),
    description                       text CONSTRAINT dashboard_description_chk CHECK (char_length(description) <= 1000),
    venue_id                          uuid,
    is_shared                         boolean DEFAULT false,
    id                                uuid PRIMARY KEY NOT NULL,
    owner_principal_id                uuid NOT NULL,
    aggregate_cost                    text NOT NULL CONSTRAINT dashboard_aggregate_cost_chk CHECK (aggregate_cost IN ('low', 'medium', 'high')),
    archived_at                       timestamptz,
    created_at                        timestamptz NOT NULL
);

-- One panel, and the query behind it
CREATE TABLE IF NOT EXISTS reporting.dashboard_tile (
    dashboard_id                      uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    title                             text,
    report_id                         uuid NOT NULL,
    visualisation                     text NOT NULL CONSTRAINT dashboard_tile_visualisation_chk CHECK (visualisation IN ('number', 'line', 'area', 'bar', 'stackedBar', 'stackedBar100', 'combo', 'pie', 'donut', 'table', 'matrix', 'gauge', 'heatmap', 'funnel', 'waterfall', 'treemap', 'scatter', 'map', 'ribbon', 'decompositionTree')),
    parameters                        jsonb,
    refresh_seconds                   integer,
    position                          jsonb NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS reporting.delivery (
    id                                uuid PRIMARY KEY,
    subscription_id                   uuid,
    report_id                         uuid,
    attempted_at                      timestamptz,
    status                            text CONSTRAINT delivery_status_chk CHECK (status IN ('delivered', 'failed', 'retrying', 'suppressed')),
    recipient_count                   integer,
    failure_reason                    text,
    retry_count                       integer DEFAULT 0,
    contained_personal_data           boolean DEFAULT false,
    scope_path                        ltree NOT NULL
);

-- One run of a report definition. The result set is cached in object storage, not here
CREATE TABLE IF NOT EXISTS reporting.execution (
    id                                text PRIMARY KEY NOT NULL,
    report_id                         uuid NOT NULL,
    report_name                       text,
    definition_version                text NOT NULL,
    status                            text NOT NULL CONSTRAINT execution_status_chk CHECK (status IN ('queued', 'running', 'completed', 'failed', 'cancelled', 'expired')),
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
    format                            text NOT NULL CONSTRAINT export_format_chk CHECK (format IN ('csv', 'xlsx', 'pdf', 'json')),
    status                            text NOT NULL CONSTRAINT export_status_chk CHECK (status IN ('queued', 'generating', 'ready', 'failed', 'expired')),
    includes_personal_data            boolean,
    purpose                           text,
    download_url                      text,
    size_bytes                        integer,
    requested_by_principal_id         uuid NOT NULL,
    requested_at                      timestamptz NOT NULL,
    expires_at                        timestamptz
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS reporting.kpi_definition (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    description                       text,
    domain                            text,
    formula                           text,
    unit                              text CONSTRAINT kpi_definition_unit_chk CHECK (unit IN ('currency', 'count', 'percentage', 'duration', 'ratio', 'score')),
    higher_is_better                  boolean DEFAULT true,
    default_period                    text,
    owner                             uuid,
    scope_path                        ltree NOT NULL,
    is_active                         boolean DEFAULT true
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS reporting.kpi_target (
    kpi_id                            uuid,
    scope_path                        ltree NOT NULL,
    period                            text NOT NULL,
    target                            numeric(18,4) NOT NULL,
    amber_at                          numeric(18,4),
    red_at                            numeric(18,4),
    stretch                           numeric(18,4),
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS reporting.natural_language_query (
    id                                uuid PRIMARY KEY NOT NULL,
    conversation_id                   uuid NOT NULL,
    question                          text NOT NULL,
    interpretation                    text,
    generated_query                   jsonb NOT NULL,
    asked_by_principal_id             uuid NOT NULL,
    asked_at                          timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS reporting.pipeline (
    id                                uuid PRIMARY KEY,
    name                              text,
    source_kind                       text,
    datasets                          text[],
    schedule                          text,
    last_run_at                       timestamptz,
    last_success_at                   timestamptz,
    freshness_minutes                 integer,
    expected_freshness_minutes        integer,
    status                            text CONSTRAINT pipeline_status_chk CHECK (status IN ('healthy', 'degraded', 'stale', 'failed', 'paused')),
    last_error                        text,
    rows_last_run                     integer,
    scope_path                        ltree NOT NULL
);

-- One column of a definition, with its aggregation
CREATE TABLE IF NOT EXISTS reporting.report_column (
    report_definition_id              uuid NOT NULL,
    id                                uuid PRIMARY KEY,
    field                             text NOT NULL,
    label                             text,
    aggregation                       text DEFAULT 'none',
    sort_order                        integer,
    sort_direction                    text CONSTRAINT report_column_sort_direction_chk CHECK (sort_direction IN ('asc', 'desc')),
    format                            text
);

-- A saved question, not its answer. Columns, filters and parameters are children; a run is an
-- execution, and the result set is cached in object storage rather than here
CREATE TABLE IF NOT EXISTS reporting.report_definition (
    name                              text NOT NULL CONSTRAINT report_definition_name_chk CHECK (char_length(name) <= 200),
    description                       text CONSTRAINT report_definition_description_chk CHECK (char_length(description) <= 1000),
    category                          text NOT NULL CONSTRAINT report_definition_category_chk CHECK (category IN ('sales', 'admission', 'financial', 'inventory', 'guest', 'operations', 'marketing', 'workforce', 'compliance', 'custom')),
    data_source                       text NOT NULL CONSTRAINT report_definition_data_source_chk CHECK (data_source IN ('orders', 'orderLines', 'payments', 'refunds', 'shifts', 'scanEvents', 'entitlements', 'products', 'inventory', 'stockMovements', 'stockCounts', 'waste', 'workstations', 'devices', 'principals', 'loyalty', 'reviews', 'queueEntries', 'guests', 'campaigns', 'cases', 'ledgerEntries', 'workOrders', 'approvals', 'purchaseOrders', 'receipts', 'requisitions', 'stockBatches', 'resourceBookings', 'delegations', 'forms', 'challenges', 'wallets', 'resaleListings')),
    group_by                          text[],
    required_permission               text NOT NULL CONSTRAINT report_definition_required_permission_chk CHECK (required_permission IN ('SESSION_FORCE_LOGOUT', 'USER_MANAGE', 'ROLE_MANAGE', 'PERMISSION_GRANT', 'PERMISSION_VIEW', 'PERMISSION_MANAGE', 'PLATFORM_TENANT_VIEW', 'PLATFORM_TENANT_MANAGE', 'PLATFORM_TENANT_TERMINATE', 'PLATFORM_PLAN_MANAGE', 'PLATFORM_CELL_VIEW', 'PLATFORM_CELL_MANAGE', 'PLATFORM_BILLING_VIEW', 'PLATFORM_BILLING_MANAGE', 'PLATFORM_RELEASE_VIEW', 'PLATFORM_RELEASE_MANAGE', 'PLATFORM_RELEASE_PROMOTE', 'PLATFORM_MIGRATION_VIEW', 'PLATFORM_MIGRATION_APPLY', 'PLATFORM_TENANT_ACCESS', 'TENANT_CONFIGURE', 'TENANT_VIEW', 'TENANT_PUBLISH', 'SCOPE_VIEW', 'SCOPE_MANAGE', 'REGION_CONFIGURE', 'WORKSTATION_CONFIGURE', 'PRODUCT_VIEW', 'PRODUCT_CONFIGURE', 'PRODUCT_APPROVE', 'PRODUCT_PUBLISH', 'PRICE_VIEW', 'PRICE_CONFIGURE', 'EVENT_CONFIGURE', 'PERFORMANCE_CONFIGURE', 'CAPACITY_CONFIGURE', 'ORDER_VIEW', 'ORDER_VIEW_OTHER', 'ORDER_CREATE', 'ORDER_MODIFY', 'ORDER_DISCOUNT', 'ORDER_CANCEL', 'ORDER_VOID', 'ORDER_REFUND', 'ORDER_REFUND_APPROVE', 'ORDER_REFUND_BULK', 'ORDER_EXCHANGE', 'ORDER_RESCHEDULE', 'ORDER_REPRINT', 'PRICE_OVERRIDE', 'DISCOUNT_APPLY', 'CREDIT_MANAGE', 'CREDIT_OVERRIDE', 'WALLET_VIEW', 'WALLET_OPERATE', 'WALLET_CONFIGURE', 'PAYMENT_VIEW', 'PAYMENT_CONFIGURE', 'PAYMENT_PROVIDER_MANAGE', 'PAYMENT_DISPUTE', 'SHIFT_OPEN', 'SHIFT_CLOSE', 'SHIFT_SUSPEND', 'SHIFT_CLOSE_OTHER', 'SHIFT_APPROVE_OPEN', 'SHIFT_APPROVE_CLOSE', 'SHIFT_REOPEN', 'CASH_LIFT', 'CASH_ADD', 'CASH_NO_SALE', 'DEPOSIT_BOX_MODIFY_OWN', 'DEPOSIT_BOX_MODIFY_OTHER', 'OVERSHORT_ACCEPT', 'ACCESS_VALIDATE', 'ACCESS_OVERRIDE', 'ACCESS_POINT_CONFIGURE', 'TURNSTILE_MODE_SET', 'TICKET_LOOKUP', 'ACCREDITATION_VIEW', 'ACCREDITATION_APPLY', 'ACCREDITATION_APPROVE', 'ACCREDITATION_ISSUE', 'ACCREDITATION_MANAGE', 'ACCREDITATION_CONFIGURE', 'REPORT_VIEW_OWN', 'REPORT_VIEW_WORKSTATION', 'REPORT_VIEW_VENUE', 'REPORT_VIEW_REGION', 'REPORT_VIEW_TENANT', 'REPORT_EXPORT', 'REPORT_EXPORT_PII', 'REPORT_MANAGE', 'REPORT_SCHEDULE', 'LEDGER_VIEW', 'LEDGER_POST', 'LEDGER_APPROVE', 'TAX_CONFIGURE', 'ACCOUNT_CONFIGURE', 'SETTLEMENT_VIEW', 'SETTLEMENT_RECONCILE', 'GUEST_VIEW', 'GUEST_VIEW_PII', 'GUEST_MANAGE', 'VENUE_MAP_VIEW', 'VENUE_MAP_MANAGE', 'VENUE_MAP_PUBLISH', 'RESOURCE_VIEW', 'RESOURCE_BOOK', 'RESOURCE_MANAGE', 'RESOURCE_CONFIGURE', 'RENTAL_VIEW', 'RENTAL_BOOK', 'RENTAL_OPERATE', 'RENTAL_MANAGE', 'RENTAL_CONFIGURE', 'RENTAL_PRICE', 'RENTAL_APPROVE', 'RENTAL_OVERRIDE', 'DEVELOPER_VIEW', 'DEVELOPER_MANAGE', 'DEVELOPER_ADMIN', 'LOYALTY_ACCRUE', 'LOYALTY_REDEEM', 'LOYALTY_ADJUST', 'MARKETING_VIEW', 'MARKETING_MANAGE', 'MARKETING_SEND', 'CASE_VIEW', 'CASE_MANAGE', 'ASSET_LIBRARY_VIEW', 'ASSET_LIBRARY_MANAGE', 'ASSET_LIBRARY_APPROVE', 'ASSET_LIBRARY_SHARE', 'QUEUE_VIEW', 'QUEUE_MANAGE', 'QUEUE_REDEEM', 'QUEUE_OVERRIDE', 'ASSET_VIEW', 'ASSET_MANAGE', 'WORK_ORDER_VIEW', 'WORK_ORDER_MANAGE', 'WORK_ORDER_VERIFY', 'INSPECTION_VIEW', 'INSPECTION_SUBMIT', 'INSPECTION_MANAGE', 'INCIDENT_REPORT', 'INCIDENT_VIEW', 'INCIDENT_MANAGE', 'KIOSK_ATTEND', 'DEVICE_VIEW', 'DEVICE_CONFIGURE', 'DEVICE_MANAGE', 'APPROVAL_ACT', 'APPROVAL_DELEGATE', 'AI_USE', 'AI_CONFIGURE', 'AI_APPROVE', 'AI_AUDIT_VIEW', 'AUDIT_VIEW', 'APPROVAL_VIEW', 'APPROVAL_REQUEST', 'APPROVAL_DECIDE', 'APPROVAL_CONFIGURE', 'MAINTENANCE_EXECUTE', 'MAINTENANCE_APPROVE', 'WORKFORCE_VIEW', 'WORKFORCE_MANAGE', 'ATTENDANCE_RECORD', 'ANNOUNCEMENT_PUBLISH', 'ANNOUNCEMENT_EMERGENCY', 'PARTNER_VIEW', 'PARTNER_MANAGE', 'PARKING_CONFIGURE', 'PAYMENT_VOID', 'PROCUREMENT_VIEW', 'PROCUREMENT_REQUEST', 'PROCUREMENT_MANAGE', 'PROCUREMENT_RECEIVE')),
    max_date_range_days               integer DEFAULT 366,
    id                                uuid PRIMARY KEY NOT NULL,
    version                           text NOT NULL,
    is_system                         boolean NOT NULL,
    is_retired                        boolean NOT NULL,
    estimated_cost                    text CONSTRAINT report_definition_estimated_cost_chk CHECK (estimated_cost IN ('low', 'medium', 'high')),
    created_by_principal_id           uuid,
    created_at                        timestamptz NOT NULL,
    last_run_at                       timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS reporting.report_definition_version (
    id                                uuid PRIMARY KEY NOT NULL,
    report_id                         uuid NOT NULL,
    version                           text NOT NULL,
    definition                        jsonb NOT NULL,
    published_by_principal_id         uuid,
    published_at                      timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- A condition applied before aggregation. Hangs off: a child of reporting.report_definition;
-- reaches reporting.report_definition through its keys; references reporting.report_definition.
-- Reached by: 6 operations read it and 4 write it.
CREATE TABLE IF NOT EXISTS reporting.report_filter (
    report_definition_id              uuid NOT NULL,
    id                                uuid PRIMARY KEY,
    field                             text NOT NULL,
    operator                          text NOT NULL CONSTRAINT report_filter_operator_chk CHECK (operator IN ('equals', 'notEquals', 'greaterThan', 'lessThan', 'between', 'in', 'notIn', 'contains', 'isNull', 'isNotNull')),
    value                             text,
    values                            text[],
    is_parameter                      boolean DEFAULT false
);

-- Something the reader supplies at run time. Hangs off: reaches reporting.report_definition
-- through its keys; references reporting.report_definition. Reached by: 6 operations read it and 3
-- write it.
CREATE TABLE IF NOT EXISTS reporting.report_parameter (
    key                               text NOT NULL,
    label                             text NOT NULL,
    type                              text NOT NULL CONSTRAINT report_parameter_type_chk CHECK (type IN ('string', 'integer', 'decimal', 'money', 'boolean', 'date', 'dateTime', 'uuid', 'enum')),
    is_required                       boolean NOT NULL,
    default_value                     text,
    id                                uuid PRIMARY KEY NOT NULL,
    definition_id                     uuid NOT NULL
);

-- When a report runs and who receives it. Hangs off: reaches reporting.report_definition through
-- its keys; references identity.principal, reporting.report_definition. Reached by: 4 operations
-- read it and 3 write it; 3 tables reference it.
CREATE TABLE IF NOT EXISTS reporting.schedule (
    report_id                         uuid NOT NULL,
    name                              text CONSTRAINT schedule_name_chk CHECK (char_length(name) <= 200),
    cadence                           jsonb NOT NULL,
    parameters                        jsonb,
    format                            text NOT NULL CONSTRAINT schedule_format_chk CHECK (format IN ('csv', 'xlsx', 'pdf', 'json')),
    include_personal_data             boolean DEFAULT false,
    skip_if_empty                     boolean DEFAULT true,
    id                                uuid PRIMARY KEY NOT NULL,
    owner_principal_id                uuid NOT NULL,
    is_paused                         boolean NOT NULL,
    last_run_at                       timestamptz,
    last_run_status                   text CONSTRAINT schedule_last_run_status_chk CHECK (last_run_status IN ('queued', 'running', 'completed', 'failed', 'cancelled', 'expired')),
    next_run_at                       timestamptz,
    consecutive_failures              integer,
    created_at                        timestamptz NOT NULL
);

-- Who receives a scheduled report, which is a consent question as well as a distribution one
CREATE TABLE IF NOT EXISTS reporting.schedule_recipient (
    schedule_id                       uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT schedule_recipient_kind_chk CHECK (kind IN ('principal', 'email', 'sftp', 'webhook')),
    address                           text NOT NULL,
    principal_id                      uuid,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS reporting.semantic_model (
    version                           integer,
    published_at                      timestamptz,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS reporting.subscription (
    id                                uuid PRIMARY KEY,
    report_id                         uuid NOT NULL,
    schedule_id                       uuid,
    channel                           text CONSTRAINT subscription_channel_chk CHECK (channel IN ('email', 'sftp', 'webhook', 'inPlatform')),
    format                            text CONSTRAINT subscription_format_chk CHECK (format IN ('pdf', 'xlsx', 'csv', 'json')),
    includes_personal_data            boolean DEFAULT false,
    runs_as_principal_id              uuid,
    is_active                         boolean DEFAULT true,
    scope_path                        ltree NOT NULL
);

