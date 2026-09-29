-- maintenance — 17 tables
-- **Derived. Do not hand-edit.**

-- A physical thing with a service history — a lift, a chiller, a ride. Distinct from a resource,
-- which is bookable: an asset is maintained and a resource is reserved
CREATE TABLE IF NOT EXISTS maintenance.asset (
    asset_tag                         text NOT NULL CONSTRAINT asset_asset_tag_chk CHECK (char_length(asset_tag) <= 64),
    name                              text NOT NULL CONSTRAINT asset_name_chk CHECK (char_length(name) <= 200),
    venue_id                          uuid NOT NULL,
    category_id                       uuid,
    location_description              text CONSTRAINT asset_location_description_chk CHECK (char_length(location_description) <= 500),
    criticality                       text NOT NULL CONSTRAINT asset_criticality_chk CHECK (criticality IN ('safetyCritical', 'revenueCritical', 'standard', 'low')),
    priority_override                 text,
    manufacturer                      text CONSTRAINT asset_manufacturer_chk CHECK (char_length(manufacturer) <= 200),
    model                             text CONSTRAINT asset_model_chk CHECK (char_length(model) <= 200),
    serial_number                     text CONSTRAINT asset_serial_number_chk CHECK (char_length(serial_number) <= 128),
    commissioned_at                   date,
    warranty_expires_at               date,
    supplier_id                       uuid,
    linked_product_ids                text[],
    linked_access_point_id            uuid,
    requires_inspection_to_return     boolean DEFAULT false,
    id                                uuid PRIMARY KEY NOT NULL,
    resource_id                       uuid,
    device_id                         uuid,
    acquisition_cost                  numeric(18,4),
    acquired_on                       date,
    depreciation                      jsonb,
    retired_on                        date,
    disposal_proceeds                 numeric(18,4),
    status                            text NOT NULL CONSTRAINT asset_status_chk CHECK (status IN ('inService', 'outOfService', 'underMaintenance', 'awaitingParts', 'retired', 'disposed')),
    status_reason                     text,
    open_work_order_count             integer,
    next_maintenance_due_at           timestamptz,
    last_inspection_at                timestamptz,
    usage_counter                     numeric(18,4)
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS maintenance.asset_category (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    description                       text,
    parent_category_id                uuid,
    icon_asset_id                     uuid,
    default_tracking_model            text,
    default_duration_minutes          integer,
    default_turnaround_minutes        integer,
    is_default_waiver_required        boolean DEFAULT false,
    default_deposit_policy_id         uuid,
    overridable_fields                text[],
    scope_path                        ltree NOT NULL,
    is_active                         boolean DEFAULT true
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS maintenance.asset_document (
    id                                uuid PRIMARY KEY NOT NULL,
    asset_id                          uuid NOT NULL,
    ref                               text NOT NULL,
    name                              text CONSTRAINT asset_document_name_chk CHECK (char_length(name) <= 200),
    kind                              text
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS maintenance.asset_status_change (
    id                                uuid PRIMARY KEY NOT NULL,
    asset_id                          uuid NOT NULL,
    from_status                       text,
    to_status                         text NOT NULL CONSTRAINT asset_status_change_to_status_chk CHECK (to_status IN ('inService', 'outOfService', 'underMaintenance', 'awaitingParts', 'retired', 'disposed')),
    reason                            text NOT NULL CONSTRAINT asset_status_change_reason_chk CHECK (char_length(reason) <= 1000),
    work_order_id                     text,
    inspection_id                     text,
    changed_by_principal_id           uuid,
    recorded_at                       timestamptz NOT NULL,
    synced_at                         timestamptz
);

-- Something that happened and needs recording — distinct from a work order, which is something to
-- do
CREATE TABLE IF NOT EXISTS maintenance.incident (
    id                                text PRIMARY KEY NOT NULL,
    incident_number                   text NOT NULL,
    kind                              text NOT NULL CONSTRAINT incident_kind_chk CHECK (kind IN ('guestInjury', 'staffInjury', 'nearMiss', 'propertyDamage', 'equipmentFailure', 'securityIncident', 'fireOrEvacuation', 'foodSafety', 'environmental', 'other')),
    severity                          text NOT NULL CONSTRAINT incident_severity_chk CHECK (severity IN ('nearMiss', 'minor', 'moderate', 'major', 'critical')),
    status                            text NOT NULL CONSTRAINT incident_status_chk CHECK (status IN ('reported', 'underInvestigation', 'actionRequired', 'closed')),
    venue_id                          uuid NOT NULL,
    asset_id                          uuid,
    location_description              text,
    is_reportable                     boolean,
    notification_due_at               timestamptz,
    notified_at                       timestamptz,
    assigned_to_principal_id          uuid,
    reported_by_principal_id          uuid NOT NULL,
    corrective_work_order_id          text,
    occurred_at                       timestamptz NOT NULL,
    recorded_at                       timestamptz,
    closed_at                         timestamptz,
    synced_at                         timestamptz,
    description                       text,
    investigation_note                text,
    root_cause                        text,
    corrective_actions                text,
    first_aid_given                   boolean,
    is_emergency_services_called      boolean,
    witness_count                     integer,
    attachment_refs                   text[]
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS maintenance.incident_authority_notification (
    id                                uuid PRIMARY KEY NOT NULL,
    incident_id                       text NOT NULL,
    authority                         text NOT NULL CONSTRAINT incident_authority_notification_authority_chk CHECK (char_length(authority) <= 200),
    reference                         text CONSTRAINT incident_authority_notification_reference_chk CHECK (char_length(reference) <= 128),
    notified_at                       timestamptz NOT NULL,
    notified_by_principal_id          uuid,
    attachment_refs                   text[],
    recorded_at                       timestamptz
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS maintenance.incident_investigation_note (
    id                                uuid PRIMARY KEY NOT NULL,
    incident_id                       text NOT NULL,
    note                              text NOT NULL CONSTRAINT incident_investigation_note_note_chk CHECK (char_length(note) <= 10000),
    written_by_principal_id           uuid,
    recorded_at                       timestamptz NOT NULL
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS maintenance.incident_involved_party (
    id                                uuid PRIMARY KEY NOT NULL,
    incident_id                       text NOT NULL,
    kind                              text NOT NULL CONSTRAINT incident_involved_party_kind_chk CHECK (kind IN ('subject', 'staff')),
    subject_id                        uuid,
    principal_id                      uuid
);

-- A completed check against a template. The responses are children
CREATE TABLE IF NOT EXISTS maintenance.inspection (
    template_name                     text,
    outcome                           text NOT NULL CONSTRAINT inspection_outcome_chk CHECK (outcome IN ('passed', 'passedWithObservations', 'failed')),
    failed_item_count                 integer,
    failed_safety_critical_count      integer,
    performed_by_principal_id         uuid NOT NULL,
    performed_at                      timestamptz NOT NULL,
    synced_at                         timestamptz,
    retain_until                      date,
    id                                text PRIMARY KEY NOT NULL,
    template_id                       uuid NOT NULL,
    venue_id                          uuid NOT NULL,
    asset_id                          uuid,
    signature_ref                     text,
    recorded_at                       timestamptz NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS maintenance.inspection_item (
    key                               text NOT NULL,
    attachment_refs                   text[],
    id                                uuid PRIMARY KEY NOT NULL,
    inspection_id                     text NOT NULL,
    template_item_id                  uuid,
    item_key                          text NOT NULL CONSTRAINT inspection_item_item_key_chk CHECK (char_length(item_key) <= 120),
    label                             text,
    value                             text,
    is_passed                         boolean,
    is_safety_critical                boolean DEFAULT false,
    note                              text CONSTRAINT inspection_item_note_chk CHECK (char_length(note) <= 1000),
    attachment_asset_ids              text[],
    recorded_at                       timestamptz
);

-- The questions an inspection asks. Versioned, because changing them changes what past answers
-- meant
CREATE TABLE IF NOT EXISTS maintenance.inspection_template (
    instructions                      text,
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT inspection_template_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT inspection_template_name_chk CHECK (char_length(name) <= 200),
    venue_id                          uuid,
    applies_to_asset_category_id      uuid,
    frequency                         text CONSTRAINT inspection_template_frequency_chk CHECK (frequency IN ('preOpening', 'postClosing', 'daily', 'weekly', 'monthly', 'annual', 'adHoc')),
    retention_years                   integer DEFAULT 7,
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
CREATE TABLE IF NOT EXISTS maintenance.preventive_plan (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL CONSTRAINT preventive_plan_name_chk CHECK (char_length(name) <= 200),
    asset_id                          uuid NOT NULL,
    asset_category_id                 uuid,
    interval_days                     integer,
    usage_interval                    numeric(18,4),
    lead_time_days                    integer DEFAULT 7,
    task_template                     jsonb NOT NULL,
    last_completed_at                 timestamptz,
    next_due_at                       timestamptz,
    is_active                         boolean
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS maintenance.priority_scoring_model (
    id                                uuid PRIMARY KEY,
    venue_id                          uuid,
    weights                           jsonb NOT NULL,
    updated_at                        timestamptz,
    updated_by_principal_id           uuid
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS maintenance.vendor_service_request (
    id                                uuid PRIMARY KEY,
    venue_id                          uuid,
    work_order_id                     text NOT NULL,
    supplier_id                       uuid NOT NULL,
    scope                             text NOT NULL CONSTRAINT vendor_service_request_scope_chk CHECK (char_length(scope) <= 2000),
    status                            text DEFAULT 'draft',
    vendor_reference                  text CONSTRAINT vendor_service_request_vendor_reference_chk CHECK (char_length(vendor_reference) <= 100),
    quoted_cost                       numeric(18,4),
    final_cost                        numeric(18,4),
    scheduled_visit_at                timestamptz,
    note                              text CONSTRAINT vendor_service_request_note_chk CHECK (char_length(note) <= 1000),
    raised_by_principal_id            uuid,
    created_at                        timestamptz,
    completed_at                      timestamptz
);

-- Something that needs doing to an asset, raised by a person, an inspection or a schedule. The
-- evidence attaches here
CREATE TABLE IF NOT EXISTS maintenance.work_order (
    downtime_minutes                  integer,
    root_cause                        text CONSTRAINT work_order_root_cause_chk CHECK (root_cause IN ('wearAndTear', 'operatorError', 'guestDamage', 'manufacturingDefect', 'environmental', 'softwareFault', 'powerFailure', 'deferredMaintenance', 'unknown')),
    root_cause_note                   text,
    escalated_at                      timestamptz,
    escalation_level                  integer DEFAULT 0,
    id                                text PRIMARY KEY NOT NULL,
    work_order_number                 text NOT NULL,
    title                             text NOT NULL,
    venue_id                          uuid NOT NULL,
    asset_id                          uuid,
    asset_name                        text,
    status                            text NOT NULL CONSTRAINT work_order_status_chk CHECK (status IN ('open', 'assigned', 'inProgress', 'paused', 'awaitingParts', 'completed', 'verified', 'closed', 'cancelled')),
    priority                          text NOT NULL CONSTRAINT work_order_priority_chk CHECK (priority IN ('low', 'normal', 'high', 'urgent', 'emergency')),
    priority_score                    integer,
    priority_source                   text CONSTRAINT work_order_priority_source_chk CHECK (priority_source IN ('scored', 'assetOverride', 'manual')),
    fault_assessment                  jsonb,
    required_qualification_codes      text[],
    kind                              text NOT NULL CONSTRAINT work_order_kind_chk CHECK (kind IN ('corrective', 'planned', 'inspectionFollowUp', 'incidentCorrective', 'improvement')),
    assigned_to_principal_id          uuid,
    raised_by_principal_id            uuid,
    category_id                       uuid,
    location_description              text CONSTRAINT work_order_location_description_chk CHECK (char_length(location_description) <= 500),
    elapsed_minutes                   integer,
    is_timer_running                  boolean,
    due_at                            timestamptz,
    requires_verification             boolean,
    source_plan_id                    uuid,
    source_inspection_id              text,
    source_incident_id                text,
    created_at                        timestamptz NOT NULL,
    recorded_at                       timestamptz,
    completed_at                      timestamptz,
    synced_at                         timestamptz,
    description                       text,
    resolution                        text,
    resolution_code                   text CONSTRAINT work_order_resolution_code_chk CHECK (resolution_code IN ('repaired', 'partReplaced', 'adjusted', 'cleaned', 'noFaultFound', 'referredExternal', 'replaced', 'deferred')),
    attachment_refs                   text[],
    labour_cost                       numeric(18,4),
    parts_cost                        numeric(18,4),
    net_cost_amount                   numeric(18,4),
    completed_by_principal_id         uuid,
    is_follow_up_required             boolean DEFAULT false,
    follow_up_note                    text CONSTRAINT work_order_follow_up_note_chk CHECK (char_length(follow_up_note) <= 1000),
    verification_outcome              text CONSTRAINT work_order_verification_outcome_chk CHECK (verification_outcome IN ('verified', 'rejected')),
    verification_note                 text CONSTRAINT work_order_verification_note_chk CHECK (char_length(verification_note) <= 1000),
    verified_at                       timestamptz,
    verified_by_principal_id          uuid,
    cancel_reason                     text CONSTRAINT work_order_cancel_reason_chk CHECK (cancel_reason IN ('raisedInError', 'duplicate', 'superseded', 'noLongerRequired')),
    cancel_note                       text CONSTRAINT work_order_cancel_note_chk CHECK (char_length(cancel_note) <= 300),
    superseded_by_work_order_id       text,
    cancelled_at                      timestamptz,
    close_outcome                     text CONSTRAINT work_order_close_outcome_chk CHECK (close_outcome IN ('completedAndVerified', 'notReproducible', 'supersededByReplacement', 'noLongerApplicable', 'duplicate')),
    close_note                        text CONSTRAINT work_order_close_note_chk CHECK (char_length(close_note) <= 500),
    duplicate_of_work_order_id        text,
    closed_at                         timestamptz,
    closed_by_principal_id            uuid
);

-- Photo, video, document, note or signature against a work order. Evidence, not decoration —
-- captured offline and queued Hangs off: a child of maintenance.work_order; reaches
-- maintenance.asset through its keys; references assets.media_asset, identity.principal,
-- maintenance.work_order. Reached by: 1 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS maintenance.work_order_attachment (
    id                                uuid PRIMARY KEY NOT NULL,
    work_order_id                     text NOT NULL,
    kind                              text NOT NULL CONSTRAINT work_order_attachment_kind_chk CHECK (kind IN ('photo', 'video', 'document', 'note', 'signature')),
    asset_ref                         uuid,
    text                              text,
    stage                             text CONSTRAINT work_order_attachment_stage_chk CHECK (stage IN ('before', 'during', 'after', 'signOff')),
    captured_by_principal_id          uuid,
    captured_at                       timestamptz NOT NULL,
    synced_at                         timestamptz
);

