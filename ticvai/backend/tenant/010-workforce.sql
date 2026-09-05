-- workforce — 6 tables
-- **Derived. Do not hand-edit.**

-- Targeted by venue, department or role. emergency is not a louder operational Hangs off: reaches
-- workforce.rota_assignment through its keys; references identity.principal, platform.org_unit.
-- Reached by: 2 operations read it and 2 write it; 1 tables reference it
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
-- child of workforce.announcement; reaches workforce.rota_assignment through its keys; references
-- identity.principal, workforce.announcement. Reached by: 2 operations read it and 2 write it
CREATE TABLE IF NOT EXISTS workforce.announcement_receipt (
    id                                uuid PRIMARY KEY NOT NULL,
    announcement_id                   uuid NOT NULL,
    principal_id                      uuid NOT NULL
);

-- Who actually turned up. occurredAt and recordedAt are both kept — a steward clocking in offline
-- is not late because the sync was Hangs off: reaches workforce.rota_assignment through its keys;
-- references access.access_point, identity.principal, workforce.rota_assignment. Reached by: 2
-- operations read it and 2 write it
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

-- A person expected somewhere at a time. Not a shift — a shift is a cash session, and most people
-- on a rota never touch a till Hangs off: a root — nothing above it in its schema; references
-- identity.principal, identity.role, platform.org_unit. Reached by: 6 operations read it and 2
-- write it; 2 tables reference it
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

-- Both parties agree before the supervisor sees it. Routed through approvals rather than a second
-- mechanism Hangs off: reaches workforce.rota_assignment through its keys; references
-- approvals.request, identity.principal, workforce.rota_assignment. Reached by: 0 operations read
-- it and 1 write it
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

