-- maintenance — 8 tables
-- **Derived. Do not hand-edit.**

-- A physical thing with a service history — a lift, a chiller, a ride. Distinct from a resource,
-- which is bookable: an asset is maintained and a resource is reserved
CREATE TABLE IF NOT EXISTS maintenance.asset (
    asset_tag                         text,
    name                              text,
    venue_id                          uuid,
    category_id                       uuid,
    location_description              text,
    criticality                       text,
    manufacturer                      text,
    model                             text,
    serial_number                     text,
    commissioned_at                   date,
    warranty_expires_at               date,
    supplier_id                       uuid,
    linked_product_ids                text[],
    linked_access_point_id            uuid,
    requires_inspection_to_return     boolean,
    document_refs                     text[],
    id                                uuid PRIMARY KEY,
    resource_id                       uuid,
    acquisition_cost                  numeric(18,4),
    acquired_on                       date,
    depreciation                      jsonb,
    retired_on                        date,
    disposal_proceeds                 numeric(18,4),
    status                            text,
    status_reason                     text,
    open_work_order_count             integer,
    next_maintenance_due_at           timestamptz,
    is_maintenance_overdue            boolean,
    last_inspection_at                timestamptz,
    usage_counter                     numeric(18,4)
);

-- Something that happened and needs recording — distinct from a work order, which is something to
-- do
CREATE TABLE IF NOT EXISTS maintenance.incident (
    id                                text PRIMARY KEY,
    incident_number                   text,
    kind                              text,
    severity                          text,
    status                            text,
    venue_id                          uuid,
    asset_id                          uuid,
    location_description              text,
    is_reportable                     boolean,
    notification_due_at               timestamptz,
    notified_at                       timestamptz,
    assigned_to_principal_id          uuid,
    reported_by_principal_id          uuid,
    corrective_work_order_id          text,
    occurred_at                       timestamptz,
    recorded_at                       timestamptz,
    closed_at                         timestamptz,
    synced_at                         timestamptz,
    description                       text,
    investigation_note                text,
    root_cause                        text,
    corrective_actions                text,
    first_aid_given                   boolean,
    emergency_services_called         boolean,
    witness_count                     integer,
    attachment_refs                   text[]
);

-- A completed check against a template. The responses are children
CREATE TABLE IF NOT EXISTS maintenance.inspection (
    id                                text PRIMARY KEY NOT NULL,
    template_id                       uuid NOT NULL,
    template_name                     text,
    venue_id                          uuid NOT NULL,
    asset_id                          uuid,
    outcome                           text NOT NULL,
    failed_item_count                 integer,
    failed_safety_critical_count      integer,
    performed_by_principal_id         uuid NOT NULL,
    performed_at                      timestamptz NOT NULL,
    recorded_at                       timestamptz,
    synced_at                         timestamptz,
    retain_until                      date
);

-- The questions an inspection asks. Versioned, because changing them changes what past answers
-- meant
CREATE TABLE IF NOT EXISTS maintenance.inspection_template (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid,
    applies_to_asset_category_id      uuid,
    frequency                         text,
    retention_years                   integer,
    is_active                         boolean
);

-- One question, with its expected range
CREATE TABLE IF NOT EXISTS maintenance.inspection_template_item (
    inspection_template_id            uuid NOT NULL,
    key                               text NOT NULL,
    label                             text NOT NULL,
    kind                              text NOT NULL,
    is_required                       boolean NOT NULL,
    is_safety_critical                boolean,
    requires_photo_on_fail            boolean,
    min_value                         numeric(18,4),
    max_value                         numeric(18,4),
    guidance                          text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- What should be inspected, how often. Generates work orders rather than being one
CREATE TABLE IF NOT EXISTS maintenance.maintenance_plan (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    asset_id                          uuid NOT NULL,
    asset_category_id                 uuid,
    interval_days                     integer,
    usage_interval                    numeric(18,4),
    lead_time_days                    integer,
    task_template                     jsonb NOT NULL,
    last_completed_at                 timestamptz,
    next_due_at                       timestamptz,
    is_active                         boolean
);

-- Something that needs doing to an asset, raised by a person, an inspection or a schedule. The
-- evidence attaches here
CREATE TABLE IF NOT EXISTS maintenance.work_order (
    downtime_minutes                  integer,
    root_cause                        text,
    root_cause_note                   text,
    escalated_at                      timestamptz,
    escalation_level                  integer,
    id                                text PRIMARY KEY,
    work_order_number                 text,
    title                             text,
    venue_id                          uuid,
    asset_id                          uuid,
    asset_name                        text,
    status                            text,
    priority                          text,
    kind                              text,
    assigned_to_principal_id          uuid,
    raised_by_principal_id            uuid,
    elapsed_minutes                   integer,
    is_timer_running                  boolean,
    due_at                            timestamptz,
    is_overdue                        boolean,
    requires_verification             boolean,
    source_plan_id                    uuid,
    source_inspection_id              text,
    source_incident_id                text,
    created_at                        timestamptz,
    recorded_at                       timestamptz,
    completed_at                      timestamptz,
    synced_at                         timestamptz,
    description                       text,
    resolution                        text,
    resolution_code                   text,
    attachment_refs                   text[],
    labour_cost                       numeric(18,4),
    parts_cost                        numeric(18,4),
    total_cost                        numeric(18,4),
    verified_by_principal_id          uuid
);

-- Photo, video, document, note or signature against a work order. Evidence, not decoration —
-- captured offline and queued Hangs off: a child of maintenance.work_order; reaches
-- maintenance.asset through its keys; references assets.media_asset, identity.principal,
-- maintenance.work_order. Reached by: 0 operations read it and 1 write it
CREATE TABLE IF NOT EXISTS maintenance.work_order_attachment (
    id                                uuid PRIMARY KEY NOT NULL,
    work_order_id                     text NOT NULL,
    kind                              text NOT NULL,
    asset_ref                         uuid,
    text                              text,
    stage                             text,
    captured_by_principal_id          uuid,
    captured_at                       timestamptz NOT NULL,
    synced_at                         timestamptz
);

