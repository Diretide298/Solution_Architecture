-- resources — 4 tables
-- **Derived. Do not hand-edit.**

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
-- through its keys; references maintenance.asset. Reached by: 0 operations read it and 1 write it
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

