-- sync — 3 tables
-- **Derived. Do not hand-edit.**

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS sync.cell_connection (
    id                                uuid PRIMARY KEY,
    source_cell_id                    uuid NOT NULL,
    target_cell_id                    uuid NOT NULL,
    type                              text NOT NULL CONSTRAINT cell_connection_type_chk CHECK (char_length(type) <= 30),
    status                            text NOT NULL CONSTRAINT cell_connection_status_chk CHECK (char_length(status) <= 30),
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS sync.cross_cell_request (
    id                                uuid PRIMARY KEY,
    guest_link_id                     uuid NOT NULL,
    type                              text NOT NULL CONSTRAINT cross_cell_request_type_chk CHECK (char_length(type) <= 50),
    source_cell_id                    uuid NOT NULL,
    target_cell_id                    uuid NOT NULL,
    subject_type                      text NOT NULL CONSTRAINT cross_cell_request_subject_type_chk CHECK (char_length(subject_type) <= 50),
    subject_reference_id              uuid,
    payload                           text,
    response_payload                  text,
    status                            text NOT NULL CONSTRAINT cross_cell_request_status_chk CHECK (char_length(status) <= 30),
    correlation_id                    text CONSTRAINT cross_cell_request_correlation_id_chk CHECK (char_length(correlation_id) <= 100),
    requested_at                      timestamptz NOT NULL,
    completed_at                      timestamptz
);

-- An offline record the server refused, with the reason. Kept, because a till that loses a
-- rejected sale silently is worse than one that reports it
CREATE TABLE IF NOT EXISTS sync.rejection (
    id                                text PRIMARY KEY NOT NULL,
    workstation_id                    uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT rejection_kind_chk CHECK (kind IN ('order', 'payment', 'refund', 'void', 'scan')),
    recorded_at                       timestamptz,
    rejected_at                       timestamptz NOT NULL,
    problem                           jsonb NOT NULL,
    payload                           jsonb,
    resolved_at                       timestamptz,
    resolved_by_principal_id          uuid,
    resolution                        text CONSTRAINT rejection_resolution_chk CHECK (resolution IN ('posted', 'voided', 'refunded')),
    resolved_record_id                text
);

