-- resources — 16 tables
-- **Derived. Do not hand-edit.**

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.allocation_policy (
    strategy                          text,
    respect_resource_priority         boolean,
    scoring_weights                   jsonb,
    allow_partial_allocation          boolean,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.attribute_definition (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    label                             text NOT NULL,
    data_type                         text NOT NULL,
    applicable_resource_type_ids      text[],
    applicable_category_ids           text[],
    mandatory                         boolean,
    default_value                     text,
    allowed_values                    text[],
    minimum                           numeric(18,4),
    maximum                           numeric(18,4),
    validation_expression             text,
    searchable                        boolean,
    scope_path                        text
);

-- A resource held for a window (BL-040, BL-041). Setup and teardown sit outside the booking, which
-- is what stops a calendar double-booking every turnaround
CREATE TABLE IF NOT EXISTS resources.booking (
    id                                uuid PRIMARY KEY NOT NULL,
    resource_id                       uuid NOT NULL,
    subject_id                        uuid,
    order_id                          uuid,
    "from"                            timestamptz NOT NULL,
    "to"                              timestamptz NOT NULL,
    status                            text NOT NULL,
    recurrence_group_id               uuid,
    deposit_authorisation_id          uuid,
    checked_out_at                    timestamptz,
    due_back_at                       timestamptz,
    returned_at                       timestamptz,
    condition_out                     text,
    condition_in                      text
);

-- What a person resource is certified to do, and until when (BL-042). A lapsed lifeguard
-- certificate is a safety failure, not a data-quality one. Hangs off: reaches resources.resource
-- through its keys; references maintenance.asset. Reached by: 0 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS resources.qualification (
    code                              text NOT NULL,
    name                              text NOT NULL,
    issued_at                         date,
    expires_at                        date,
    issuer                            text,
    document_asset_id                 uuid,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A specific bookable object (CF-125, BL-039). Not a quantity of interchangeable ones — forty
-- identical strollers are forty resources, because guest twelve returned stroller twelve
CREATE TABLE IF NOT EXISTS resources.resource (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    kind                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        text,
    parent_resource_id                uuid,
    principal_id                      uuid,
    attributes                        jsonb,
    setup_minutes                     integer,
    teardown_minutes                  integer,
    requires_qualification            text[],
    deposit_amount                    numeric(18,4),
    status                            text,
    is_active                         boolean
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
    scope_path                        text
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.resource_block (
    id                                uuid PRIMARY KEY,
    resource_id                       uuid NOT NULL,
    "from"                            timestamptz NOT NULL,
    "to"                              timestamptz NOT NULL,
    reason                            text NOT NULL,
    note                              text,
    created_by                        uuid,
    scope_path                        text
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
    display_order                     integer,
    tags                              text[],
    reporting_group                   text,
    cost_centre                       text,
    default_attributes                jsonb,
    default_approval_workflow_id      uuid,
    scope_path                        text,
    is_active                         boolean
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.resource_dependency (
    id                                uuid PRIMARY KEY,
    kind                              text NOT NULL,
    target_resource_id                uuid,
    target_resource_type_id           uuid,
    minimum_quantity                  integer,
    maximum_quantity                  integer,
    mandatory                         boolean,
    priority                          integer,
    effective_from                    date,
    effective_to                      date,
    venue_id                          uuid,
    scope_path                        text
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.resource_package (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    description                       text,
    applicable_venue_ids              text[],
    allocation_priority               integer,
    effective_from                    date,
    effective_to                      date,
    minimum_minutes                   integer,
    maximum_minutes                   integer,
    requires_approval                 boolean,
    internal_cost                     numeric(18,4),
    scope_path                        text
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.resource_relation (
    resource_id                       uuid NOT NULL,
    relation                          text NOT NULL,
    effective_from                    date,
    priority                          integer,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.resource_requirement (
    id                                uuid PRIMARY KEY,
    resource_type_id                  uuid,
    category_id                       uuid,
    resource_id                       uuid,
    quantity                          integer NOT NULL,
    mandatory                         boolean,
    required_qualifications           text[],
    required_attributes               jsonb,
    substitute_resource_ids           text[],
    scope_path                        text
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.resource_schedule (
    resource_id                       uuid,
    availability_mode                 text,
    slot_minutes                      integer,
    minimum_booking_minutes           integer,
    maximum_booking_minutes           integer,
    advance_booking_days              integer,
    scope_path                        text,
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
    nature                            text,
    reservable                        boolean,
    rentable                          boolean,
    capacity_controlled               boolean,
    schedule_controlled               boolean,
    inventory_controlled              boolean,
    qualification_required            boolean,
    maintenance_controlled            boolean,
    check_in_out_supported            boolean,
    deposit_applicable                boolean,
    customer_selectable               boolean,
    scope_path                        text,
    is_active                         boolean
);

-- Who is in a session, in what order (BL-045). The running order is operational — an instructor
-- takes beginners first
CREATE TABLE IF NOT EXISTS resources.session_participant (
    id                                uuid PRIMARY KEY NOT NULL,
    session_id                        uuid NOT NULL,
    subject_id                        uuid NOT NULL,
    position                          integer NOT NULL,
    experience_level                  text,
    package_name                      text,
    notes                             text,
    has_signed_waiver                 boolean
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS resources.venue_assignment (
    primary_venue_id                  uuid NOT NULL,
    secondary_venue_ids               text[],
    shared_pool                       boolean,
    cross_venue_booking_allowed       boolean,
    travel_buffer_minutes             integer,
    transfer_required                 boolean,
    effective_from                    date,
    effective_to                      date,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

