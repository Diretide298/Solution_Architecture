-- sync — 1 tables
-- **Derived. Do not hand-edit.**

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

