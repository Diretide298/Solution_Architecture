-- resources — 16 tables
-- **Derived. Do not hand-edit.**

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.allocation_policy (
    strategy                          text DEFAULT 'rotate' CONSTRAINT allocation_policy_strategy_chk CHECK (strategy IN ('rotate', 'leastUtilised', 'priorityOrder', 'nearestFirst')),
    respect_resource_priority         boolean DEFAULT true,
    scoring_weights                   jsonb,
    allow_partial_allocation          boolean DEFAULT false,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.attribute_definition (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    label                             text NOT NULL,
    data_type                         text NOT NULL CONSTRAINT attribute_definition_data_type_chk CHECK (data_type IN ('text', 'number', 'decimal', 'currency', 'date', 'dateTime', 'boolean', 'singleSelect', 'multiSelect', 'lookup', 'attachment', 'url', 'measurement', 'formula')),
    applicable_resource_type_ids      text[],
    applicable_category_ids           text[],
    is_mandatory                      boolean DEFAULT false,
    default_value                     text,
    allowed_values                    text[],
    minimum                           numeric(18,4),
    maximum                           numeric(18,4),
    validation_expression             text,
    is_searchable                     boolean DEFAULT false,
    scope_path                        ltree NOT NULL
);

-- A resource held for a window (BL-040, BL-041). Setup and teardown sit outside the booking, which
-- is what stops a calendar double-booking every turnaround
CREATE TABLE IF NOT EXISTS resources.booking (
    id                                uuid PRIMARY KEY NOT NULL,
    resource_id                       uuid NOT NULL,
    subject_id                        uuid,
    order_id                          text,
    valid_from                        timestamptz NOT NULL,
    valid_to                          timestamptz NOT NULL,
    status                            text NOT NULL CONSTRAINT booking_status_chk CHECK (status IN ('reserved', 'checkedOut', 'returned', 'overdue', 'cancelled', 'noShow')),
    recurrence_group_id               uuid,
    deposit_authorisation_id          uuid,
    checked_out_at                    timestamptz,
    due_back_at                       timestamptz,
    returned_at                       timestamptz,
    condition_out                     text,
    condition_in                      text,
    synced_at                         timestamptz
);

-- What a person resource is certified to do, and until when (BL-042). A lapsed lifeguard
-- certificate is a safety failure, not a data-quality one. Hangs off: a child of
-- resources.resource; reaches resources.resource through its keys; references assets.media_asset,
-- resources.resource. Reached by: 2 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS resources.qualification (
    resource_id                       uuid,
    code                              text NOT NULL,
    name                              text NOT NULL,
    issued_at                         date,
    expires_at                        date,
    issuer                            text,
    document_asset_id                 uuid,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A specific bookable object (CF-125, BL-039). Not a quantity of interchangeable ones — forty
-- identical strollers are forty resources, because guest twelve returned stroller twelve
CREATE TABLE IF NOT EXISTS resources.resource (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    kind                              text NOT NULL CONSTRAINT resource_kind_chk CHECK (kind IN ('cabana', 'locker', 'wheelchair', 'stroller', 'equipment', 'room', 'auditorium', 'vehicle', 'instructor', 'staff', 'table', 'pitch', 'studio', 'other')),
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    parent_resource_id                uuid,
    principal_id                      uuid,
    attributes                        jsonb,
    setup_minutes                     integer DEFAULT 0,
    teardown_minutes                  integer DEFAULT 0,
    requires_qualification            text[],
    deposit_amount                    numeric(18,4),
    status                            text CONSTRAINT resource_status_chk CHECK (status IN ('available', 'booked', 'checkedOut', 'maintenance', 'retired')),
    is_active                         boolean DEFAULT true
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.resource_audit (
    id                                uuid PRIMARY KEY,
    resource_id                       uuid,
    at                                timestamptz,
    actor_id                          uuid,
    action                            text,
    field                             text,
    previous_value                    text,
    new_value                         text,
    reason                            text,
    source_channel                    text,
    api_origin                        text,
    correlation_id                    text,
    scope_path                        ltree NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.resource_block (
    id                                uuid PRIMARY KEY,
    resource_id                       uuid NOT NULL,
    valid_from                        timestamptz NOT NULL,
    valid_to                          timestamptz NOT NULL,
    reason                            text NOT NULL CONSTRAINT resource_block_reason_chk CHECK (reason IN ('setup', 'teardown', 'maintenance', 'blackout', 'closed', 'operational', 'training')),
    note                              text,
    created_by                        uuid,
    scope_path                        ltree NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.resource_category (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    description                       text,
    parent_category_id                uuid,
    applicable_resource_type_ids      text[],
    display_order                     integer DEFAULT 0,
    tags                              text[],
    reporting_group                   text,
    cost_centre                       text,
    default_attributes                jsonb,
    default_approval_workflow_id      uuid,
    scope_path                        ltree NOT NULL,
    is_active                         boolean DEFAULT true
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.resource_dependency (
    id                                uuid PRIMARY KEY,
    kind                              text NOT NULL CONSTRAINT resource_dependency_kind_chk CHECK (kind IN ('requires', 'requiresOneOf', 'requiresAll', 'conflictsWith', 'cannotOperateSimultaneously', 'preferredWith', 'substituteFor', 'backupFor', 'sharesCapacityWith')),
    target_resource_id                uuid,
    target_resource_type_id           uuid,
    minimum_quantity                  integer DEFAULT 1,
    maximum_quantity                  integer,
    is_mandatory                      boolean DEFAULT true,
    priority                          integer DEFAULT 0,
    effective_from                    date,
    effective_to                      date,
    venue_id                          uuid,
    scope_path                        ltree NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.resource_package (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    description                       text,
    applicable_venue_ids              text[],
    allocation_priority               integer DEFAULT 0,
    effective_from                    date,
    effective_to                      date,
    minimum_minutes                   integer,
    maximum_minutes                   integer,
    requires_approval                 boolean DEFAULT false,
    internal_cost                     numeric(18,4),
    scope_path                        ltree NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.resource_relation (
    resource_id                       uuid NOT NULL,
    relation                          text NOT NULL CONSTRAINT resource_relation_relation_chk CHECK (relation IN ('contains', 'belongsTo', 'locatedIn', 'operatedBy', 'supportedBy', 'partOf', 'dedicatedTo')),
    effective_from                    date,
    priority                          integer DEFAULT 0,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.resource_requirement (
    id                                uuid PRIMARY KEY,
    resource_type_id                  uuid,
    category_id                       uuid,
    resource_id                       uuid,
    quantity                          integer NOT NULL DEFAULT 1,
    is_mandatory                      boolean DEFAULT true,
    required_qualifications           text[],
    required_attributes               jsonb,
    substitute_resource_ids           text[],
    scope_path                        ltree NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.resource_schedule (
    resource_id                       uuid,
    availability_mode                 text CONSTRAINT resource_schedule_availability_mode_chk CHECK (availability_mode IN ('alwaysAvailable', 'scheduled', 'onRequest')),
    slot_minutes                      integer,
    minimum_booking_minutes           integer,
    maximum_booking_minutes           integer,
    advance_booking_days              integer,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 19 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.resource_type (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    description                       text,
    icon                              text,
    display_colour                    text,
    nature                            text CONSTRAINT resource_type_nature_chk CHECK (nature IN ('physical', 'human', 'virtual')),
    is_reservable                     boolean DEFAULT true,
    is_rentable                       boolean DEFAULT false,
    is_capacity_controlled            boolean DEFAULT false,
    is_schedule_controlled            boolean DEFAULT true,
    is_inventory_controlled           boolean DEFAULT false,
    is_qualification_required         boolean DEFAULT false,
    is_maintenance_controlled         boolean DEFAULT false,
    is_check_in_out_supported         boolean DEFAULT false,
    is_deposit_applicable             boolean DEFAULT false,
    is_customer_selectable            boolean DEFAULT false,
    scope_path                        ltree NOT NULL,
    is_active                         boolean DEFAULT true
);

-- Who is in a session, in what order (BL-045). The running order is operational — an instructor
-- takes beginners first
CREATE TABLE IF NOT EXISTS resources.session_participant (
    id                                uuid PRIMARY KEY NOT NULL,
    session_id                        uuid NOT NULL,
    subject_id                        uuid NOT NULL,
    position                          integer NOT NULL,
    experience_level                  text CONSTRAINT session_participant_experience_level_chk CHECK (experience_level IN ('firstTime', 'beginner', 'intermediate', 'advanced')),
    package_name                      text,
    notes                             text,
    recorded_at                       timestamptz,
    synced_at                         timestamptz,
    has_signed_waiver                 boolean
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.venue_assignment (
    primary_venue_id                  uuid NOT NULL,
    secondary_venue_ids               text[],
    shared_pool                       boolean DEFAULT false,
    is_cross_venue_booking_allowed    boolean DEFAULT false,
    travel_buffer_minutes             integer DEFAULT 0,
    is_transfer_required              boolean DEFAULT false,
    effective_from                    date,
    effective_to                      date,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

