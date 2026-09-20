-- sync — 3 tables
-- **Derived. Do not hand-edit.**

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is.
CREATE TABLE IF NOT EXISTS sync.cell_connection (
    id                                uuid PRIMARY KEY,
    source_cell_id                    uuid NOT NULL,
    target_cell_id                    uuid NOT NULL,
    type                              text NOT NULL,
    status                            text NOT NULL,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is.
CREATE TABLE IF NOT EXISTS sync.cross_cell_request (
    id                                uuid PRIMARY KEY,
    guest_link_id                     uuid NOT NULL,
    type                              text NOT NULL,
    source_cell_id                    uuid NOT NULL,
    target_cell_id                    uuid NOT NULL,
    subject_type                      text NOT NULL,
    subject_reference_id              uuid,
    payload                           text,
    response_payload                  text,
    status                            text NOT NULL,
    correlation_id                    text,
    requested_at                      timestamptz NOT NULL,
    completed_at                      timestamptz
);

-- An offline record the server refused, with the reason. Kept, because a till that loses a
-- rejected sale silently is worse than one that reports it
CREATE TABLE IF NOT EXISTS sync.rejection (
    id                                text PRIMARY KEY NOT NULL,
    workstation_id                    uuid NOT NULL,
    kind                              text NOT NULL,
    recorded_at                       timestamptz,
    rejected_at                       timestamptz NOT NULL,
    problem                           jsonb NOT NULL,
    payload                           jsonb,
    resolved_at                       timestamptz,
    resolved_by_principal_id          uuid
);

