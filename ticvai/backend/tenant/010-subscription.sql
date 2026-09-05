-- subscription — 1 tables
-- **Derived. Do not hand-edit.**

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.partner_quote (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid,
    agreement_id                      uuid,
    total_minor                       integer,
    state                             text,
    valid_until                       timestamptz,
    created_at                        timestamptz
);

